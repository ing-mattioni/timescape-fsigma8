"""Flux-conservative structured reference backend for Phase 1E-G.

The continuum statement is the weak Laplace--Beltrami transmission form in
the human-approved Phase 1E-G specification, sections 8--10.  The finite
volume/graph assembly below is only a numerical reference discretisation.
It is not a physical FEM mesh, a unique Timescape morphology, or a spacetime
junction.  The weak-form and transfer equations have no paper equation
number because they are explicit Phase 1E-G model-extension equations.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass, fields, is_dataclass
from types import MappingProxyType
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import linalg as scipy_linalg
from scipy import sparse
from scipy.sparse import linalg as sparse_linalg

from timescape_fsigma8.transfer.continuum_geometry import (
    COMMON_REFERENCE_NORMAL_WALL_TO_VOID_1E_G,
    DERIVED_FROM_NORMALIZED_METRIC,
    PHYSICAL_VOLUME_SEMANTICS,
    REDUCED_DIMENSIONAL_MEASURE_ONLY,
    ContinuumCarrierSpec,
    ContinuumContractError,
    ContinuumDegeneracyError,
    ContinuumEllipticClosureConfig,
    ContinuumStateIntegrityError,
    FixedReferenceBranchSpec,
    MorphologySpec,
    RegionalGeometrySpec,
)
from timescape_fsigma8.transfer.matrix_backend import (
    JointTransmissionState,
    ScalarJet,
    TransmissionSolution,
    VectorJet,
)


FloatArray = NDArray[np.float64]


def _array_fingerprint(values: NDArray[np.generic]) -> tuple[object, ...]:
    """Return a detached deterministic description of one numerical array."""
    array = np.ascontiguousarray(values)
    digest = hashlib.sha256(array.view(np.uint8)).hexdigest()
    return (array.dtype.str, tuple(array.shape), digest)


def _sparse_fingerprint(matrix: sparse.spmatrix) -> tuple[object, ...]:
    """Return a detached deterministic description of one sparse matrix."""
    csr = matrix.tocsr(copy=False)
    return (
        tuple(csr.shape),
        _array_fingerprint(csr.indptr),
        _array_fingerprint(csr.indices),
        _array_fingerprint(csr.data),
    )


def _canonical_state(value: object) -> object:
    """Detach dataclass/configuration state from all live mutable references."""
    if isinstance(value, np.ndarray):
        return ("array",) + _array_fingerprint(value)
    if sparse.issparse(value):
        return ("sparse",) + _sparse_fingerprint(value)
    if is_dataclass(value) and not isinstance(value, type):
        return (
            type(value).__module__,
            type(value).__qualname__,
            tuple(
                (field.name, _canonical_state(getattr(value, field.name)))
                for field in fields(value)
            ),
        )
    if isinstance(value, Mapping):
        return tuple(
            sorted(
                (
                    (_canonical_state(key), _canonical_state(item))
                    for key, item in value.items()
                ),
                key=repr,
            )
        )
    if isinstance(value, (tuple, list)):
        return tuple(_canonical_state(item) for item in value)
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (str, int, float, bool, type(None))):
        return value
    raise TypeError(f"unsupported assembled-state value {type(value)!r}")


@dataclass(frozen=True, slots=True)
class _AssemblyStateSnapshot:
    """Immutable validated assembly identity and detached numerical content."""

    object_identities: tuple[int, ...]
    state: tuple[object, ...]


def _readonly_vector(values: ArrayLike, name: str, size: int) -> FloatArray:
    vector = np.array(values, dtype=np.float64, copy=True).reshape(-1)
    if vector.shape != (size,) or not np.all(np.isfinite(vector)):
        raise ContinuumContractError(f"{name} must be a finite carrier field")
    vector.setflags(write=False)
    return vector


def _max_abs(values: ArrayLike) -> float:
    array = np.asarray(values, dtype=np.float64)
    return float(np.max(np.abs(array))) if array.size else 0.0


@dataclass(frozen=True)
class InterfaceFace:
    """One wall-to-void face with the frozen common-reference normal."""

    wall_index: int
    void_index: int
    axis: int
    orientation_sign: int
    wall_coefficient: float
    void_coefficient: float
    spacing: float


@dataclass(frozen=True)
class SourceProjectionDiagnostics:
    """Dual projection diagnostics, distinct from solution normalisation."""

    mean_before_projection: float
    mean_after_projection: float
    raw_integral: float
    projected_integral: float


@dataclass(frozen=True)
class MetricNormalizationDiagnostics:
    """Construction/provenance check for one literal metric reference measure."""

    region_id: str
    normalization_id: str
    volume_provenance: str
    consistency_classification: str
    spatial_dimension: int
    measure_semantics: str
    physical_three_volume_authorized: bool
    metric_reference_measure: float
    declared_reference_measure: float
    relative_residual: float


@dataclass(frozen=True)
class InterfaceDiagnostics:
    value_jump: FloatArray
    flux_jump: FloatArray
    wall_common_flux: FloatArray
    void_common_flux: FloatArray
    wall_outward_flux: FloatArray
    void_outward_flux: FloatArray

    @property
    def maximum_value_jump(self) -> float:
        return _max_abs(self.value_jump)

    @property
    def maximum_flux_jump(self) -> float:
        return _max_abs(self.flux_jump)


@dataclass(frozen=True)
class ContinuumTransferResponse:
    """One source -> potential -> target-scalarized transfer response."""

    provenance: str
    region: str
    raw_source_provenance: str
    projected_admissible_source_support: str
    raw_source_density: FloatArray
    raw_source_load: FloatArray
    projected_source_load: FloatArray
    potential: FloatArray
    transferred_field: FloatArray
    source_projection: SourceProjectionDiagnostics
    solution_global_mean: float
    interface: InterfaceDiagnostics
    provenance_roundtrip_error: float


@dataclass(frozen=True)
class ContinuumTransferJetResponse:
    provenance: str
    region: str
    potential: VectorJet
    transferred_field: VectorJet
    components: tuple[ContinuumTransferResponse, ...]


class ContinuumH1Operator:
    """Conservative discretisation of the selected continuum weak operator.

    The continuum equation is
    ``a(U,V)=sum_r integral K_r^{ij} partial_i U partial_j V dmu_0``
    (Phase 1E-G specification section 8, explicit model extension; no paper
    equation number).  The reference backend currently admits only isotropic
    coefficient tensors and uses harmonic normal transmissibility at regional
    faces.  Full anisotropic tensors fail closed.
    """

    scientific_role = "FLUX_CONSERVATIVE_STRUCTURED_REFERENCE_DISCRETIZATION"

    def __setattr__(self, name: str, value: object) -> None:
        """Seal validated scientific dependencies after successful assembly."""
        if self.__dict__.get("_assembly_sealed", False):
            raise ContinuumStateIntegrityError(
                "assembled continuum scientific state is immutable; "
                "construct a new ContinuumH1Operator"
            )
        object.__setattr__(self, name, value)

    def __init__(
        self,
        *,
        carrier: ContinuumCarrierSpec,
        morphology: MorphologySpec,
        wall_geometry: RegionalGeometrySpec,
        void_geometry: RegionalGeometrySpec,
        branch: FixedReferenceBranchSpec,
        configuration: ContinuumEllipticClosureConfig,
        continuum_coercivity_bound: float,
    ) -> None:
        branch.validate_selected_branch()
        if not carrier.target_geometry.metric_time_independent:
            raise ContinuumContractError(
                "time-dependent target metric/scalarization is unsupported"
            )
        if morphology.wall_domain.shape != carrier.grid_shape:
            raise ContinuumContractError("morphology does not match carrier grid")
        for geometry, name in (
            (wall_geometry, "wall"),
            (void_geometry, "void"),
        ):
            if geometry.grid_shape != carrier.grid_shape:
                raise ContinuumContractError(f"{name} geometry grid mismatch")
            if geometry.dimension != carrier.dimension:
                raise ContinuumContractError(f"{name} geometry dimension mismatch")
            if not geometry.metric_time_independent:
                raise ContinuumContractError(
                    "time-dependent comoving pullback geometry is unsupported"
                )
            if not geometry.isotropic_reference_backend:
                raise ContinuumContractError(
                    "unsupported anisotropic structured discretization"
                )
        if not morphology.fixed_reference_partition or not morphology.fixed_interface:
            raise ContinuumContractError("moving interface/partition is unsupported")
        if not morphology.pullbacks_time_independent:
            raise ContinuumContractError("time-dependent Phi_r is unsupported")
        if (
            not np.isfinite(continuum_coercivity_bound)
            or continuum_coercivity_bound <= 0.0
        ):
            raise ContinuumContractError(
                "continuum_coercivity_bound must be explicitly positive"
            )
        if continuum_coercivity_bound < configuration.coercivity_min:
            raise ContinuumDegeneracyError(
                "continuum coercivity assumption is below coercivity_min"
            )

        self.carrier = carrier
        self.morphology = morphology
        self.wall_geometry = wall_geometry
        self.void_geometry = void_geometry
        self.branch = branch
        self.configuration = configuration
        self.continuum_coercivity_assumption = float(continuum_coercivity_bound)
        self._size = int(np.prod(carrier.grid_shape))
        self._weights = carrier.reference_measure_weights.reshape(-1)
        self._wall_mask = morphology.wall_domain.reshape(-1)
        self._void_mask = morphology.void_domain.reshape(-1)

        wall_scalar = self._isotropic_tensor_density(wall_geometry, "wall")
        void_scalar = self._isotropic_tensor_density(void_geometry, "void")
        target_scalar = self._isotropic_tensor_density(
            carrier.target_geometry, "target"
        )
        self._regional_coefficient = np.where(
            morphology.wall_domain, wall_scalar, void_scalar
        ).reshape(-1)
        self._target_coefficient = target_scalar.reshape(-1)
        self._metric_volume_ratio = np.where(
            morphology.wall_domain,
            wall_geometry.metric_volume_ratio,
            void_geometry.metric_volume_ratio,
        ).reshape(-1)
        self._target_volume_ratio = (
            carrier.target_geometry.metric_volume_ratio.reshape(-1)
        )
        self._metric_normalization_diagnostics = MappingProxyType(
            {
                "wall": self._validate_metric_normalization(
                    wall_geometry, self._wall_mask, "wall"
                ),
                "void": self._validate_metric_normalization(
                    void_geometry, self._void_mask, "void"
                ),
                "target": self._validate_metric_normalization(
                    carrier.target_geometry,
                    np.ones(self.size, dtype=np.bool_),
                    "target",
                ),
            }
        )

        inverse_min = min(
            wall_geometry.inverse_metric_eigenvalue_bounds[0],
            void_geometry.inverse_metric_eigenvalue_bounds[0],
        )
        inverse_max = max(
            wall_geometry.inverse_metric_eigenvalue_bounds[1],
            void_geometry.inverse_metric_eigenvalue_bounds[1],
        )
        if inverse_min < configuration.ellipticity_min:
            raise ContinuumDegeneracyError(
                "geometric ellipticity is below ellipticity_min"
            )
        self.ellipticity_lower_bound = float(inverse_min)
        self.ellipticity_upper_bound = float(inverse_max)

        self._stiffness, self._faces = self._assemble_stiffness(
            self._regional_coefficient
        )
        self._target_stiffness, _ = self._assemble_stiffness(
            self._target_coefficient, collect_interface=False
        )
        if not self._faces:
            raise ContinuumContractError("morphology has no discrete interface faces")
        self._validate_symmetric(self._stiffness, "regional stiffness")
        self._validate_symmetric(self._target_stiffness, "target stiffness")

        dense = self._stiffness.toarray()
        eigenvalues = np.linalg.eigvalsh(0.5 * (dense + dense.T))
        self.global_kernel_dimension = int(
            np.count_nonzero(np.abs(eigenvalues) <= configuration.kernel_tolerance)
        )
        if self.global_kernel_dimension != 1:
            raise ContinuumDegeneracyError(
                "unexpected extra kernel modes: connected operator must have one constant"
            )
        basis = scipy_linalg.null_space(self._weights[np.newaxis, :])
        reduced = basis.T @ dense @ basis
        self.ordinary_euclidean_constrained_stiffness_eigenvalue = float(
            np.min(np.linalg.eigvalsh(0.5 * (reduced + reduced.T)))
        )
        if (
            self.ordinary_euclidean_constrained_stiffness_eigenvalue
            <= configuration.kernel_tolerance
        ):
            raise ContinuumDegeneracyError(
                "constrained discrete operator is not coercive"
            )
        mass = np.diag(self._weights * self._metric_volume_ratio)
        reduced_mass = basis.T @ mass @ basis
        # Human-approved Phase 1E-G v2 numerical diagnostic K x=lambda M x;
        # no paper equation number and no continuum-coercivity proof claim.
        generalized = scipy_linalg.eigvalsh(
            0.5 * (reduced + reduced.T),
            0.5 * (reduced_mass + reduced_mass.T),
        )
        self.generalized_mass_weighted_laplacian_eigenvalue = float(
            np.min(generalized)
        )
        # Backward-compatible v1 name: explicitly an ordinary Euclidean
        # stiffness diagnostic, never a continuum coercivity constant.
        self.discrete_spectral_lower_bound = (
            self.ordinary_euclidean_constrained_stiffness_eigenvalue
        )
        self._mean_basis = basis
        self._assembly_snapshot = self._capture_assembled_state()
        self._assembly_sealed = True
        self._validate_assembled_state_integrity()

    def _capture_assembled_state(self) -> _AssemblyStateSnapshot:
        """Capture scientific identities and detached content validated here.

        The snapshot deliberately contains no aliases to mutable numerical
        state.  Object identities make isolated replacement detectable even
        when a replacement happens to have equal values, while numerical
        digests detect representative in-place tampering.
        """
        identities = tuple(
            id(value)
            for value in (
                self.carrier,
                self.carrier.target_geometry,
                self.carrier.target_geometry.normalization,
                self.carrier.reference_measure_weights,
                self.wall_geometry,
                self.wall_geometry.normalization,
                self.wall_geometry.metric_inverse,
                self.wall_geometry.metric_volume_ratio,
                self.void_geometry,
                self.void_geometry.normalization,
                self.void_geometry.metric_inverse,
                self.void_geometry.metric_volume_ratio,
                self.morphology,
                self.morphology.wall_domain,
                self.morphology.void_domain,
                self.branch,
                self.configuration,
                self.configuration.downstream_configuration,
                self._weights,
                self._wall_mask,
                self._void_mask,
                self._regional_coefficient,
                self._target_coefficient,
                self._metric_volume_ratio,
                self._target_volume_ratio,
                self._stiffness,
                self._target_stiffness,
                self._mean_basis,
                self._metric_normalization_diagnostics,
            )
        )
        state = (
            ("carrier", _canonical_state(self.carrier)),
            ("wall_geometry", _canonical_state(self.wall_geometry)),
            ("void_geometry", _canonical_state(self.void_geometry)),
            ("morphology", _canonical_state(self.morphology)),
            ("branch", _canonical_state(self.branch)),
            ("configuration", _canonical_state(self.configuration)),
            (
                "normalization_diagnostics",
                _canonical_state(self._metric_normalization_diagnostics),
            ),
            (
                "internal_arrays",
                tuple(
                    _canonical_state(value)
                    for value in (
                        self._weights,
                        self._wall_mask,
                        self._void_mask,
                        self._regional_coefficient,
                        self._target_coefficient,
                        self._metric_volume_ratio,
                        self._target_volume_ratio,
                        self._mean_basis,
                    )
                ),
            ),
            ("regional_stiffness", _canonical_state(self._stiffness)),
            ("target_stiffness", _canonical_state(self._target_stiffness)),
            ("interface_faces", _canonical_state(self._faces)),
            (
                "assembly_scalars",
                (
                    self._size,
                    self.continuum_coercivity_assumption,
                    self.ellipticity_lower_bound,
                    self.ellipticity_upper_bound,
                    self.global_kernel_dimension,
                    self.ordinary_euclidean_constrained_stiffness_eigenvalue,
                    self.generalized_mass_weighted_laplacian_eigenvalue,
                    self.discrete_spectral_lower_bound,
                    tuple(self._stiffness.shape),
                    tuple(self._target_stiffness.shape),
                ),
            ),
        )
        return _AssemblyStateSnapshot(object_identities=identities, state=state)

    def _validate_assembled_state_integrity(self) -> None:
        """Fail closed if live scientific state differs from validated assembly."""
        if not self.__dict__.get("_assembly_sealed", False):
            return
        expected = self.__dict__.get("_assembly_snapshot")
        try:
            current = self._capture_assembled_state()
        except Exception as exc:
            raise ContinuumStateIntegrityError(
                "assembled continuum state cannot be validated"
            ) from exc
        if current != expected:
            raise ContinuumStateIntegrityError(
                "live continuum scientific state differs from validated assembly"
            )

    @property
    def size(self) -> int:
        self._validate_assembled_state_integrity()
        return self._size

    @property
    def metric_normalization_diagnostics(
        self,
    ) -> Mapping[str, MetricNormalizationDiagnostics]:
        """Return immutable diagnostics for the exact validated normalizations."""
        self._validate_assembled_state_integrity()
        return self._metric_normalization_diagnostics

    @property
    def stiffness_matrix(self) -> sparse.csr_matrix:
        self._validate_assembled_state_integrity()
        return self._stiffness.copy()

    @property
    def target_stiffness_matrix(self) -> sparse.csr_matrix:
        self._validate_assembled_state_integrity()
        return self._target_stiffness.copy()

    @property
    def interface_faces(self) -> tuple[InterfaceFace, ...]:
        self._validate_assembled_state_integrity()
        return self._faces

    @property
    def reference_weights(self) -> FloatArray:
        self._validate_assembled_state_integrity()
        result = self._weights.copy()
        result.setflags(write=False)
        return result

    @property
    def metric_volume_ratio(self) -> FloatArray:
        self._validate_assembled_state_integrity()
        result = self._metric_volume_ratio.copy()
        result.setflags(write=False)
        return result

    @property
    def target_volume_ratio(self) -> FloatArray:
        self._validate_assembled_state_integrity()
        result = self._target_volume_ratio.copy()
        result.setflags(write=False)
        return result

    @property
    def target_measure_weights(self) -> FloatArray:
        """Return ``w_i J_D,i`` for target-metric discrete L2 diagnostics."""
        self._validate_assembled_state_integrity()
        result = self._weights * self._target_volume_ratio
        result = np.array(result, dtype=np.float64, copy=True)
        result.setflags(write=False)
        return result

    @property
    def operator_first_derivative(self) -> sparse.csr_matrix:
        """Return A_dot=0 from the fixed-comoving branch, not a hidden default."""
        self._validate_assembled_state_integrity()
        self.branch.validate_selected_branch()
        return sparse.csr_matrix(self._stiffness.shape, dtype=np.float64)

    @property
    def operator_second_derivative(self) -> sparse.csr_matrix:
        """Return A_ddot=0 from Phase 1E-G section 19 branch metadata."""
        self._validate_assembled_state_integrity()
        self.branch.validate_selected_branch()
        return sparse.csr_matrix(self._stiffness.shape, dtype=np.float64)

    @property
    def target_scalarization_first_derivative(self) -> sparse.csr_matrix:
        """Return ``L_D_dot=0`` only on the fixed-target selected branch."""
        self._validate_assembled_state_integrity()
        self.branch.validate_selected_branch()
        if not self.carrier.target_geometry.metric_time_independent:
            raise ContinuumContractError("target scalarization is time dependent")
        return sparse.csr_matrix(self._target_stiffness.shape, dtype=np.float64)

    @property
    def target_scalarization_second_derivative(self) -> sparse.csr_matrix:
        """Return ``L_D_ddot=0`` only on the fixed-target selected branch."""
        self._validate_assembled_state_integrity()
        self.branch.validate_selected_branch()
        if not self.carrier.target_geometry.metric_time_independent:
            raise ContinuumContractError("target scalarization is time dependent")
        return sparse.csr_matrix(self._target_stiffness.shape, dtype=np.float64)

    def _validate_metric_normalization(
        self,
        geometry: RegionalGeometrySpec,
        domain_mask: NDArray[np.bool_],
        role: str,
    ) -> MetricNormalizationDiagnostics:
        """Compare the metric-derived and explicitly declared reference measure.

        This is the human-approved Phase 1E-G v2/v3 construction consistency
        equation, not an independent Timescape prediction and not a solver
        rescaling operation. For ``d<3`` both operands remain literal
        reduced-dimensional measures; agreement never grants physical-volume
        semantics or an effective-three-dimensional lift.
        """
        metric_measure = float(
            np.sum(
                self._weights
                * geometry.metric_volume_ratio.reshape(-1)
                * domain_mask
            )
        )
        declared = float(geometry.normalization.reference_comoving_volume)
        relative = abs(metric_measure - declared) / max(metric_measure, declared)
        if relative > geometry.normalization.consistency_tolerance:
            raise ContinuumContractError(
                f"{role} normalized metric/reference-measure consistency failed"
            )
        if self.carrier.physical_volume_semantics_authorized:
            classification = (
                "CONSTRUCTION_CONSISTENCY_CHECK"
                if geometry.normalization.volume_provenance
                == DERIVED_FROM_NORMALIZED_METRIC
                else "EXTERNAL_REFERENCE_VOLUME_CONSISTENCY_CHECK"
            )
            semantics = PHYSICAL_VOLUME_SEMANTICS
        else:
            classification = "REDUCED_DIMENSIONAL_MEASURE_CONSISTENCY_CHECK"
            semantics = REDUCED_DIMENSIONAL_MEASURE_ONLY
        return MetricNormalizationDiagnostics(
            region_id=role,
            normalization_id=geometry.normalization.normalization_id,
            volume_provenance=geometry.normalization.volume_provenance,
            consistency_classification=classification,
            spatial_dimension=self.carrier.dimension,
            measure_semantics=semantics,
            physical_three_volume_authorized=(
                self.carrier.physical_volume_semantics_authorized
            ),
            metric_reference_measure=metric_measure,
            declared_reference_measure=declared,
            relative_residual=relative,
        )

    def _isotropic_tensor_density(
        self, geometry: RegionalGeometrySpec, name: str
    ) -> FloatArray:
        tensor = geometry.elliptic_tensor_density
        dimension = geometry.dimension
        diagonal = np.diagonal(tensor, axis1=-2, axis2=-1)
        off_diagonal = tensor.copy()
        for axis in range(dimension):
            off_diagonal[..., axis, axis] = 0.0
        if _max_abs(off_diagonal) > self.configuration.symmetry_tolerance:
            raise ContinuumContractError(
                f"unsupported anisotropic {name} tensor: off-diagonal terms"
            )
        if not np.allclose(
            diagonal,
            diagonal[..., :1],
            rtol=0.0,
            atol=self.configuration.symmetry_tolerance,
        ):
            raise ContinuumContractError(
                f"unsupported anisotropic {name} tensor: unequal principal values"
            )
        scalar = np.array(diagonal[..., 0], dtype=np.float64, copy=True)
        if np.any(scalar <= 0.0):
            raise ContinuumDegeneracyError(f"{name} tensor density is not SPD")
        return scalar

    def _assemble_stiffness(
        self,
        coefficient: FloatArray,
        *,
        collect_interface: bool = True,
    ) -> tuple[sparse.csr_matrix, tuple[InterfaceFace, ...]]:
        rows: list[int] = []
        columns: list[int] = []
        data: list[float] = []
        faces: list[InterfaceFace] = []
        shape = self.carrier.grid_shape
        cell_volume = float(self._weights[0])
        for index in np.ndindex(shape):
            left = int(np.ravel_multi_index(index, shape))
            for axis, spacing in enumerate(self.carrier.grid_spacing):
                neighbor_tuple = list(index)
                neighbor_tuple[axis] = (neighbor_tuple[axis] + 1) % shape[axis]
                neighbor_index = tuple(neighbor_tuple)
                right = int(np.ravel_multi_index(neighbor_index, shape))
                k_left = float(coefficient.reshape(shape)[index])
                k_right = float(coefficient.reshape(shape)[neighbor_index])
                harmonic = 2.0 * k_left * k_right / (k_left + k_right)
                conductance = harmonic * cell_volume / spacing**2
                rows.extend((left, left, right, right))
                columns.extend((left, right, left, right))
                data.extend((conductance, -conductance, -conductance, conductance))
                if collect_interface:
                    left_wall = bool(self._wall_mask[left])
                    right_wall = bool(self._wall_mask[right])
                    if left_wall != right_wall:
                        if left_wall:
                            wall_index, void_index, sign = left, right, 1
                            wall_k, void_k = k_left, k_right
                        else:
                            wall_index, void_index, sign = right, left, -1
                            wall_k, void_k = k_right, k_left
                        faces.append(
                            InterfaceFace(
                                wall_index=wall_index,
                                void_index=void_index,
                                axis=axis,
                                orientation_sign=sign,
                                wall_coefficient=wall_k,
                                void_coefficient=void_k,
                                spacing=float(spacing),
                            )
                        )
        matrix = sparse.coo_matrix(
            (data, (rows, columns)), shape=(self.size, self.size)
        ).tocsr()
        return matrix, tuple(faces)

    def _validate_symmetric(self, matrix: sparse.csr_matrix, name: str) -> None:
        asymmetry = matrix - matrix.T
        magnitude = _max_abs(asymmetry.data)
        if magnitude > self.configuration.symmetry_tolerance:
            raise ContinuumContractError(f"{name} is not symmetric: {magnitude}")

    def source_load(
        self,
        source_density: ArrayLike,
        *,
        region: str,
    ) -> FloatArray:
        """Return ``J_r s_r dmu_0`` (Phase 1E-G section 8 source functional).

        The production API has no branch that omits ``J_r``. The deliberately
        wrong unweighted oracle is constructed independently in the tests.
        """
        self._validate_assembled_state_integrity()
        source = _readonly_vector(source_density, "source_density", self.size)
        if region == "wall":
            mask = self._wall_mask
            ratio = self.wall_geometry.metric_volume_ratio.reshape(-1)
        elif region == "void":
            mask = self._void_mask
            ratio = self.void_geometry.metric_volume_ratio.reshape(-1)
        elif region == "global":
            mask = np.ones(self.size, dtype=np.bool_)
            ratio = self._metric_volume_ratio
        else:
            raise ContinuumContractError("region must be wall, void, or global")
        load = self._weights * ratio * source * mask
        load.setflags(write=False)
        return load

    def project_dual_source(
        self, raw_load: ArrayLike
    ) -> tuple[FloatArray, SourceProjectionDiagnostics]:
        """Apply the single global dual projection ``<Qb,1>=0``.

        Phase 1E-G specification section 13; explicit model extension, no
        paper equation number.  This is not solution mean normalisation.
        """
        self._validate_assembled_state_integrity()
        raw = _readonly_vector(raw_load, "raw_load", self.size)
        volume = float(np.sum(self._weights))
        raw_integral = float(np.sum(raw))
        projected = raw - (raw_integral / volume) * self._weights
        projected_integral = float(np.sum(projected))
        diagnostics = SourceProjectionDiagnostics(
            mean_before_projection=raw_integral / volume,
            mean_after_projection=projected_integral / volume,
            raw_integral=raw_integral,
            projected_integral=projected_integral,
        )
        if abs(diagnostics.mean_after_projection) > (
            self.configuration.source_compatibility_tolerance
        ):
            raise ContinuumContractError("dual source compatibility projection failed")
        projected.setflags(write=False)
        return projected, diagnostics

    def _solve_mean_zero(
        self, matrix: sparse.csr_matrix, right_hand_side: ArrayLike
    ) -> FloatArray:
        self._validate_assembled_state_integrity()
        rhs = _readonly_vector(right_hand_side, "right_hand_side", self.size)
        weights_column = sparse.csr_matrix(self._weights[:, np.newaxis])
        kkt = sparse.bmat(
            [[matrix, weights_column], [weights_column.T, None]], format="csr"
        )
        augmented_rhs = np.concatenate((rhs, np.array([0.0])))
        try:
            solution = sparse_linalg.spsolve(kkt, augmented_rhs)
        except Exception as exc:  # SciPy exposes backend-specific subclasses.
            raise ContinuumDegeneracyError("constrained elliptic solve failed") from exc
        field = np.asarray(solution[:-1], dtype=np.float64)
        if not np.all(np.isfinite(field)):
            raise ContinuumDegeneracyError("constrained elliptic solve is nonfinite")
        mean = self.global_mean(field)
        if abs(mean) > self.configuration.global_mean_tolerance:
            raise ContinuumContractError("one global solution normalization failed")
        field.setflags(write=False)
        return field

    def solve_projected_load(self, projected_load: ArrayLike) -> FloatArray:
        """Solve ``A_Gamma psi=-Q(Js)`` on the one-mean-zero space.

        This is Phase 1E-G specification section 14.  The minus sign follows
        ``A=-Delta_gamma`` and the authorised reconstruction equation
        ``A psi=-s``; no upstream source code is used.
        """
        self._validate_assembled_state_integrity()
        projected = _readonly_vector(projected_load, "projected_load", self.size)
        if abs(float(np.sum(projected))) > (
            self.configuration.source_compatibility_tolerance
        ):
            raise ContinuumContractError("source does not annihilate the constant mode")
        return self._solve_mean_zero(self._stiffness, -projected)

    def global_mean(self, field: ArrayLike) -> float:
        self._validate_assembled_state_integrity()
        vector = _readonly_vector(field, "field", self.size)
        return float(self._weights @ vector / np.sum(self._weights))

    def target_scalarization(self, potential: ArrayLike) -> FloatArray:
        """Apply separately named ``L_D=Delta_gamma_D`` (section 12)."""
        self._validate_assembled_state_integrity()
        field = _readonly_vector(potential, "potential", self.size)
        result = -(
            self._target_stiffness @ field
        ) / (self._weights * self._target_volume_ratio)
        result = np.asarray(result, dtype=np.float64)
        result.setflags(write=False)
        return result

    def recover_potential_from_transfer(self, transferred: ArrayLike) -> FloatArray:
        """Invert target scalarization only on its global mean-zero range."""
        self._validate_assembled_state_integrity()
        field = _readonly_vector(transferred, "transferred", self.size)
        rhs = -(self._weights * self._target_volume_ratio * field)
        rhs, _ = self.project_dual_source(rhs)
        return self._solve_mean_zero(self._target_stiffness, rhs)

    def apply_weak_operator(self, potential: ArrayLike) -> FloatArray:
        self._validate_assembled_state_integrity()
        field = _readonly_vector(potential, "potential", self.size)
        result = np.asarray(self._stiffness @ field, dtype=np.float64)
        result.setflags(write=False)
        return result

    def interface_diagnostics(self, potential: ArrayLike) -> InterfaceDiagnostics:
        """Evaluate common-normal value and conormal traces on interface faces.

        Harmonic transmissibility gives one interface trace.  With
        ``n_Gamma`` wall->void, ``q_w-q_v=0`` is equivalent to
        ``j_w_out+j_v_out=0`` because ``n_v_out=-n_Gamma`` (Phase 1E-G
        specification section 5; no paper equation number).
        """
        self._validate_assembled_state_integrity()
        field = _readonly_vector(potential, "potential", self.size)
        value_jumps: list[float] = []
        flux_jumps: list[float] = []
        wall_common: list[float] = []
        void_common: list[float] = []
        wall_outward: list[float] = []
        void_outward: list[float] = []
        for face in self._faces:
            wall_value = float(field[face.wall_index])
            void_value = float(field[face.void_index])
            harmonic = (
                2.0
                * face.wall_coefficient
                * face.void_coefficient
                / (face.wall_coefficient + face.void_coefficient)
            )
            q = harmonic * (void_value - wall_value) / face.spacing
            trace_wall = (
                wall_value
                + q * face.spacing / (2.0 * face.wall_coefficient)
            )
            trace_void = (
                void_value
                - q * face.spacing / (2.0 * face.void_coefficient)
            )
            q_wall = (
                face.wall_coefficient
                * 2.0
                * (trace_wall - wall_value)
                / face.spacing
            )
            q_void = (
                face.void_coefficient
                * 2.0
                * (void_value - trace_void)
                / face.spacing
            )
            value_jumps.append(trace_wall - trace_void)
            flux_jumps.append(q_wall - q_void)
            wall_common.append(q_wall)
            void_common.append(q_void)
            wall_outward.append(q_wall)
            void_outward.append(-q_void)
        return InterfaceDiagnostics(
            value_jump=np.asarray(value_jumps, dtype=np.float64),
            flux_jump=np.asarray(flux_jumps, dtype=np.float64),
            wall_common_flux=np.asarray(wall_common, dtype=np.float64),
            void_common_flux=np.asarray(void_common, dtype=np.float64),
            wall_outward_flux=np.asarray(wall_outward, dtype=np.float64),
            void_outward_flux=np.asarray(void_outward, dtype=np.float64),
        )

    @staticmethod
    def explicit_trace_residuals(
        *,
        wall_trace: ArrayLike,
        void_trace: ArrayLike,
        wall_common_flux: ArrayLike,
        void_common_flux: ArrayLike,
        normal_convention: str,
    ) -> tuple[FloatArray, FloatArray]:
        """Diagnose independently supplied traces, including adversarial data."""
        if normal_convention != COMMON_REFERENCE_NORMAL_WALL_TO_VOID_1E_G:
            raise ContinuumContractError("unsupported common-normal convention")
        wall_value = np.asarray(wall_trace, dtype=np.float64)
        void_value = np.asarray(void_trace, dtype=np.float64)
        wall_flux = np.asarray(wall_common_flux, dtype=np.float64)
        void_flux = np.asarray(void_common_flux, dtype=np.float64)
        if wall_value.shape != void_value.shape or wall_flux.shape != void_flux.shape:
            raise ContinuumContractError("explicit interface traces must have paired shapes")
        return wall_value - void_value, wall_flux - void_flux

    def metric_derived_regional_reference_measures(self) -> tuple[float, float]:
        """Integrate literal ``dmu_gamma_r`` measures in the carrier dimension."""
        self._validate_assembled_state_integrity()
        wall_ratio = self.wall_geometry.metric_volume_ratio.reshape(-1)
        void_ratio = self.void_geometry.metric_volume_ratio.reshape(-1)
        wall_measure = float(np.sum(self._weights * wall_ratio * self._wall_mask))
        void_measure = float(np.sum(self._weights * void_ratio * self._void_mask))
        return wall_measure, void_measure

    def require_physical_volume_dimension(self, *, context: str) -> None:
        """Delegate the explicit Phase 1E-G v3 ``d==3`` physical-volume guard."""
        self._validate_assembled_state_integrity()
        self.carrier.require_physical_volume_semantics(context=context)

    def metric_derived_regional_comoving_volumes(self) -> tuple[float, float]:
        """Return metric-derived physical ``V_w,i,V_v,i`` only for ``d==3``."""
        self._validate_assembled_state_integrity()
        self.require_physical_volume_dimension(
            context="metric-derived regional comoving volumes"
        )
        return self.metric_derived_regional_reference_measures()

    def regional_comoving_volumes(self) -> tuple[float, float]:
        """Return declared physical ``V_w,i,V_v,i`` only for ``d==3``.

        ``EXTERNALLY_SUPPLIED_REFERENCE_VOLUME`` remains normalization
        provenance for a valid three-dimensional geometry. It is not a
        reduced-dimensional lift and cannot bypass this guard.
        """
        self._validate_assembled_state_integrity()
        self.require_physical_volume_dimension(
            context="declared regional comoving volumes"
        )
        return (
            self.wall_geometry.normalization.reference_comoving_volume,
            self.void_geometry.normalization.reference_comoving_volume,
        )

    def physical_regional_volumes(
        self, *, a_w: float, a_v: float
    ) -> tuple[float, float]:
        """Evaluate physical ``V_r=V_r,i a_r^3`` on the 3-D branch only.

        This is the human-approved Phase 1E-G section 22/v3 closure equation;
        it has no paper equation number. No length/area promotion is defined.
        """
        self._validate_assembled_state_integrity()
        self.require_physical_volume_dimension(
            context="physical regional volume assembly V_r=V_r,i*a_r^3"
        )
        if not np.isfinite(a_w) or not np.isfinite(a_v) or a_w <= 0.0 or a_v <= 0.0:
            raise ContinuumContractError("regional scale factors must be positive")
        wall_initial, void_initial = self.regional_comoving_volumes()
        return wall_initial * a_w**3, void_initial * a_v**3

    def geometric_void_fraction(self, *, a_w: float, a_v: float) -> float:
        """Evaluate ``V_v/(V_v+V_w)`` from the declared normalized volumes.

        This is the human-approved Phase 1E-G section 22 closure equation,
        not an independently predicted Timescape volume fraction.
        """
        self._validate_assembled_state_integrity()
        wall_volume, void_volume = self.physical_regional_volumes(a_w=a_w, a_v=a_v)
        return float(void_volume / (void_volume + wall_volume))


class ContinuumTransfer:
    """Implement ``T_r=-L_D G_Gamma Q_Gamma J_source,r``.

    The formula is the explicit Phase 1E-G transfer definition in section 14
    (no paper equation number).  ``metric_volume_ratio`` and
    ``regional_source_injection`` remain distinct concepts in the API.
    """

    def __setattr__(self, name: str, value: object) -> None:
        if self.__dict__.get("_assembly_sealed", False):
            raise ContinuumStateIntegrityError(
                "continuum transfer is bound immutably to its assembled operator"
            )
        object.__setattr__(self, name, value)

    def __init__(self, operator: ContinuumH1Operator) -> None:
        operator._validate_assembled_state_integrity()
        self.operator = operator
        self._operator_identity = id(operator)
        self._assembly_sealed = True

    def _validate_assembled_state_integrity(self) -> None:
        if id(self.operator) != self._operator_identity:
            raise ContinuumStateIntegrityError(
                "continuum transfer operator differs from validated assembly"
            )
        self.operator._validate_assembled_state_integrity()

    def transfer_source(
        self,
        source_density: ArrayLike,
        *,
        region: str,
        provenance: str,
    ) -> ContinuumTransferResponse:
        self._validate_assembled_state_integrity()
        raw_source = _readonly_vector(
            source_density, "source_density", self.operator.size
        )
        raw_load = self.operator.source_load(raw_source, region=region)
        projected, projection = self.operator.project_dual_source(raw_load)
        if region == "wall":
            raw_mask = self.operator.morphology.wall_domain.reshape(-1)
        elif region == "void":
            raw_mask = self.operator.morphology.void_domain.reshape(-1)
        else:
            raw_mask = np.ones(self.operator.size, dtype=np.bool_)
        outside_support = _max_abs(projected[~raw_mask]) if np.any(~raw_mask) else 0.0
        projected_support = (
            "GLOBAL_AFTER_CONSTANT_COMPATIBILITY_CORRECTION"
            if outside_support > self.operator.configuration.source_compatibility_tolerance
            else "UNCHANGED_RAW_SUPPORT"
        )
        potential = self.operator.solve_projected_load(projected)
        transferred = self.operator.target_scalarization(potential)
        interface = self.operator.interface_diagnostics(potential)
        if interface.maximum_value_jump > (
            self.operator.configuration.interface_value_tolerance
        ):
            raise ContinuumContractError("transmission value jump exceeds tolerance")
        if interface.maximum_flux_jump > (
            self.operator.configuration.interface_flux_tolerance
        ):
            raise ContinuumContractError("transmission flux jump exceeds tolerance")
        recovered = -self.operator.apply_weak_operator(potential)
        roundtrip_error = _max_abs(recovered - projected)
        if roundtrip_error > (
            self.operator.configuration.downstream_configuration.source_roundtrip_tolerance
        ):
            raise ContinuumContractError("continuum provenance roundtrip failed")
        response = ContinuumTransferResponse(
            provenance=provenance,
            region=region,
            raw_source_provenance=region,
            projected_admissible_source_support=projected_support,
            raw_source_density=raw_source,
            raw_source_load=raw_load,
            projected_source_load=projected,
            potential=potential,
            transferred_field=transferred,
            source_projection=projection,
            solution_global_mean=self.operator.global_mean(potential),
            interface=interface,
            provenance_roundtrip_error=roundtrip_error,
        )
        self._validate_assembled_state_integrity()
        return response

    def transfer_jet(
        self,
        source: VectorJet,
        *,
        region: str,
        provenance: str,
    ) -> ContinuumTransferJetResponse:
        """Use ``T[s]``, ``T[s_dot]``, ``T[s_ddot]`` analytically.

        This derivative commutation follows from
        ``A_dot=A_ddot=L_D_dot=L_D_ddot=0`` on the selected fixed-comoving
        branch (Phase 1E-G sections 19--20 plus the human-approved v2 target
        guard; no paper equation number). Canonical runtime finite differences
        are absent.
        """
        self._validate_assembled_state_integrity()
        components = tuple(
            self.transfer_source(
                values,
                region=region,
                provenance=f"{provenance}:{derivative}",
            )
            for values, derivative in zip(
                (source.value, source.first, source.second),
                ("value", "first", "second"),
                strict=True,
            )
        )
        response = ContinuumTransferJetResponse(
            provenance=provenance,
            region=region,
            potential=VectorJet(*(item.potential for item in components)),
            transferred_field=VectorJet(
                *(item.transferred_field for item in components)
            ),
            components=components,
        )
        self._validate_assembled_state_integrity()
        return response

    def transfer_regional_amplitude(
        self,
        amplitude: ScalarJet,
        *,
        region: str,
        provenance: str,
    ) -> ContinuumTransferJetResponse:
        self._validate_assembled_state_integrity()
        if region == "wall":
            injection = self.operator.morphology.wall_domain.reshape(-1).astype(float)
        elif region == "void":
            injection = self.operator.morphology.void_domain.reshape(-1).astype(float)
        else:
            raise ContinuumContractError("regional amplitude requires wall or void")
        return self.transfer_jet(
            VectorJet(
                injection * amplitude.value,
                injection * amplitude.first,
                injection * amplitude.second,
            ),
            region=region,
            provenance=provenance,
        )


class ContinuumPhase1EBackendAdapter:
    """Duck-typed Phase 1E-F backend backed by continuum transfer responses.

    ``field`` is the target-scalarized transfer.  For Phase 1E-F transmission
    diagnostics and provenance recovery the adapter reconstructs the
    mean-zero transmission potential, then applies the continuum weak
    operator.  This is not a target-only physical inverse: it is a constrained
    solver/operator identity with preserved source provenance.
    """

    def __setattr__(self, name: str, value: object) -> None:
        if self.__dict__.get("_assembly_sealed", False):
            raise ContinuumStateIntegrityError(
                "Phase 1E-F adapter is bound immutably to its continuum transfer"
            )
        object.__setattr__(self, name, value)

    def __init__(self, transfer: ContinuumTransfer) -> None:
        transfer._validate_assembled_state_integrity()
        self.transfer = transfer
        self._transfer_identity = id(transfer)
        self._assembly_sealed = True

    def _validate_assembled_state_integrity(self) -> None:
        if id(self.transfer) != self._transfer_identity:
            raise ContinuumStateIntegrityError(
                "Phase 1E-F adapter transfer differs from validated assembly"
            )
        self.transfer._validate_assembled_state_integrity()

    @property
    def size(self) -> int:
        self._validate_assembled_state_integrity()
        return self.transfer.operator.size

    @property
    def coercivity_lower_bound(self) -> float:
        self._validate_assembled_state_integrity()
        return self.transfer.operator.continuum_coercivity_assumption

    def _solution(
        self, amplitude: ScalarJet, *, region: str, provenance: str
    ) -> TransmissionSolution:
        self._validate_assembled_state_integrity()
        response = self.transfer.transfer_regional_amplitude(
            amplitude, region=region, provenance=provenance
        )
        raw = VectorJet(
            *(item.raw_source_load for item in response.components)
        )
        projected = VectorJet(
            *(item.projected_source_load for item in response.components)
        )
        return TransmissionSolution(
            provenance=f"{region}:{provenance}",
            field=response.transferred_field,
            raw_source=raw,
            injected_source=projected,
        )

    def solve_joint(
        self,
        wall_amplitude: ScalarJet,
        void_amplitude: ScalarJet,
        *,
        source_name: str,
    ) -> JointTransmissionState:
        self._validate_assembled_state_integrity()
        wall = self._solution(
            wall_amplitude, region="wall", provenance=source_name
        )
        void = self._solution(
            void_amplitude, region="void", provenance=source_name
        )
        carrier = VectorJet(
            wall.field.value + void.field.value,
            wall.field.first + void.field.first,
            wall.field.second + void.field.second,
        )
        return JointTransmissionState(wall=wall, void=void, carrier_field=carrier)

    def _potential(self, transferred: ArrayLike) -> FloatArray:
        self._validate_assembled_state_integrity()
        return self.transfer.operator.recover_potential_from_transfer(transferred)

    def value_jump(self, transferred: ArrayLike) -> FloatArray:
        self._validate_assembled_state_integrity()
        return self.transfer.operator.interface_diagnostics(
            self._potential(transferred)
        ).value_jump

    def flux_jump(self, transferred: ArrayLike) -> FloatArray:
        self._validate_assembled_state_integrity()
        return self.transfer.operator.interface_diagnostics(
            self._potential(transferred)
        ).flux_jump

    def apply_coupled_operator_jet(self, field: VectorJet) -> VectorJet:
        self._validate_assembled_state_integrity()
        recovered: list[FloatArray] = []
        for transferred in (field.value, field.first, field.second):
            potential = self._potential(transferred)
            recovered.append(-self.transfer.operator.apply_weak_operator(potential))
        return VectorJet(*recovered)

    def project_source(self, source: ArrayLike) -> FloatArray:
        self._validate_assembled_state_integrity()
        projected, _ = self.transfer.operator.project_dual_source(source)
        return projected

    def global_mean(self, field: ArrayLike) -> float:
        self._validate_assembled_state_integrity()
        return self.transfer.operator.global_mean(field)


def normalized_difference(
    first: ArrayLike, second: ArrayLike, *, normalization: float
) -> float:
    """Return the legacy finite-grid Euclidean diagnostic, explicitly named.

    This v1 compatibility helper is not the primary Phase 1E-G v2 scientific
    morphology measure.
    """
    if not np.isfinite(normalization) or normalization <= 0.0:
        raise ContinuumContractError("sensitivity normalization must be positive")
    difference = np.asarray(first, dtype=np.float64) - np.asarray(
        second, dtype=np.float64
    )
    return float(np.linalg.norm(difference) / normalization)


def target_metric_weighted_l2_difference(
    first: ArrayLike,
    second: ArrayLike,
    *,
    target_measure_weights: ArrayLike,
    reference_scale: float,
    normalization_floor: float,
) -> float:
    """Approximate ``||Y1-Y2||_L2(dmu_D)`` with explicit normalization.

    The norm is the human-approved Phase 1E-G v2 morphology diagnostic; no
    paper equation number exists.  It is morphology sensitivity, not error.
    """
    weights = np.asarray(target_measure_weights, dtype=np.float64).reshape(-1)
    difference = np.asarray(first, dtype=np.float64).reshape(-1) - np.asarray(
        second, dtype=np.float64
    ).reshape(-1)
    if weights.shape != difference.shape or np.any(weights <= 0.0):
        raise ContinuumContractError("target L2 weights must be positive and aligned")
    if (
        not np.isfinite(reference_scale)
        or reference_scale <= 0.0
        or not np.isfinite(normalization_floor)
        or normalization_floor <= 0.0
    ):
        raise ContinuumContractError("morphology L2 normalization must be positive")
    numerator = float(np.sqrt(np.sum(weights * difference**2)))
    return numerator / max(float(reference_scale), float(normalization_floor))


def require_no_generic_spectral_label(labels: Iterable[str]) -> None:
    """Fail closed on an unlabeled generic ``k`` spectral API."""
    if any(label == "k" for label in labels):
        raise ContinuumContractError("unlabeled generic k is forbidden")
