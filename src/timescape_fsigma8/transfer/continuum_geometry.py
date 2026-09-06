"""Explicit geometry and morphology contracts for Phase 1E-G.

The types in this module describe the human-authorised model extension
``H1-1E-G-COMOVING-CGI-ELLIPTIC-TRANSMISSION-V1``.  They do not assert that
the reference torus or a supplied morphology is a physical Timescape
topology or wall/void junction.  The pullback/measure equations have no
paper equation number: they are explicitly authorised closure equations in
the Phase 1E-G specification, sections 5--9, rather than equations copied
from the unlicensed upstream notebook.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

import numpy as np
from numpy.typing import ArrayLike, NDArray

from timescape_fsigma8.transfer.h1_realization import H1Configuration


FloatArray = NDArray[np.float64]
BoolArray = NDArray[np.bool_]

REALIZATION_ID_1E_G = "H1-1E-G-COMOVING-CGI-ELLIPTIC-TRANSMISSION-V1"
ROLE_1E_G = "CONTINUUM_GEOMETRIC_REALIZATION_OF_1E_F_H1_CONTRACT"
FRAMEWORK_STATUS_1E_G = (
    "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION;EXPLICIT_MODEL_EXTENSION"
)
SCIENTIFIC_STATUS_1E_G = "CONDITIONALLY_DERIVED_CONTINUUM_REALIZATION"
IMPLEMENTATION_STATUS_1E_G = "CONDITIONAL_RESEARCH_RUNTIME"
CARRIER_PHYSICAL_STATUS = "COMPUTATIONAL_REFERENCE_CARRIER_ONLY"
INTERFACE_PHYSICAL_STATUS = "MATHEMATICAL_TRANSFER_INTERFACE"
COMMON_REFERENCE_NORMAL_WALL_TO_VOID_1E_G = (
    "COMMON_REFERENCE_NORMAL_WALL_TO_VOID"
)
FIXED_REFERENCE_BRANCH = "FIXED_LAGRANGIAN_REFERENCE_DOMAINS"
HOMOGENEOUS_CLOCK_BRANCH = "HOMOGENEOUS_BACKGROUND_CLOCK_MAP"
DERIVED_FROM_NORMALIZED_METRIC = "DERIVED_FROM_NORMALIZED_METRIC"
EXTERNALLY_SUPPLIED_REFERENCE_VOLUME = (
    "EXTERNALLY_SUPPLIED_REFERENCE_VOLUME"
)
MORPHOLOGY_NORM_TARGET_METRIC_L2 = "TARGET_METRIC_WEIGHTED_L2"
PHYSICAL_VOLUME_DIMENSION = 3
# Float64 determinant/volume consistency, relative to the metric's own scale.
# This is a numerical contract tolerance, not a physical perturbation limit.
METRIC_MEASURE_RTOL = 2e-12
METRIC_MEASURE_ATOL = 0.0
PHYSICAL_VOLUME_SEMANTICS = "PHYSICAL_TIMESCAPE_THREE_VOLUME_ONLY"
REDUCED_DIMENSIONAL_MEASURE_ONLY = "REDUCED_DIMENSIONAL_METRIC_MEASURE_ONLY"
PHYSICAL_NORMALIZATION_COVARIANCE = "PHYSICAL_NORMALIZATION_COVARIANCE"
CONVERGED_EQUAL_GEOMETRY_MASK_PLACEMENT_DIAGNOSTIC = (
    "CONVERGED_EQUAL_GEOMETRY_MASK_PLACEMENT_DIAGNOSTIC"
)


class ContinuumContractError(ValueError):
    """An explicit continuum geometry, morphology, or branch contract failed."""


class ContinuumDegeneracyError(ContinuumContractError):
    """The requested data lie outside the selected nondegenerate branch."""


class ContinuumDimensionalContractError(ContinuumContractError):
    """A reduced-dimensional measure was requested as a physical 3-volume."""


class ContinuumStateIntegrityError(ContinuumContractError):
    """Validated continuum scientific state changed after operator assembly."""


def _readonly_float(values: ArrayLike, name: str) -> FloatArray:
    array = np.array(values, dtype=np.float64, copy=True)
    if not np.all(np.isfinite(array)):
        raise ContinuumContractError(f"{name} must contain only finite values")
    array.setflags(write=False)
    return array


def _readonly_bool(values: ArrayLike, name: str) -> BoolArray:
    array = np.array(values, dtype=np.bool_, copy=True)
    if array.ndim == 0:
        raise ContinuumContractError(f"{name} must be an array")
    array.setflags(write=False)
    return array


@dataclass(frozen=True)
class RegionalMetricNormalization:
    """Required provenance tying ``gamma_r``, ``a_r`` and ``V_r,i``.

    This is the human-approved Phase 1E-G v2/v3 normalization closure. It has
    no paper equation number and is not inferred from Timescape.  The runtime
    never rescales a metric to satisfy this record. The historically named
    ``reference_comoving_volume`` stores a literal metric reference measure
    during reduced-dimensional operator validation; it acquires physical
    regional three-volume semantics only when the carrier dimension is three.
    """

    normalization_id: str
    scale_factor_reference_epoch: str
    scale_factor_reference_value: float
    metric_scale_convention: str
    reference_comoving_volume: float
    volume_provenance: str
    consistency_tolerance: float

    def __post_init__(self) -> None:
        required = (
            self.normalization_id,
            self.scale_factor_reference_epoch,
            self.metric_scale_convention,
        )
        if not all(isinstance(value, str) and value.strip() for value in required):
            raise ContinuumContractError(
                "metric normalization provenance identifiers are required"
            )
        if (
            not np.isfinite(self.scale_factor_reference_value)
            or self.scale_factor_reference_value <= 0.0
        ):
            raise ContinuumContractError(
                "scale_factor_reference_value must be finite and positive"
            )
        if (
            not np.isfinite(self.reference_comoving_volume)
            or self.reference_comoving_volume <= 0.0
        ):
            raise ContinuumContractError(
                "reference_comoving_volume must be finite and positive"
            )
        if self.volume_provenance not in {
            DERIVED_FROM_NORMALIZED_METRIC,
            EXTERNALLY_SUPPLIED_REFERENCE_VOLUME,
        }:
            raise ContinuumContractError("unsupported reference-volume provenance")
        if (
            not np.isfinite(self.consistency_tolerance)
            or self.consistency_tolerance < 0.0
        ):
            raise ContinuumContractError(
                "normalization consistency_tolerance must be finite and nonnegative"
            )


@dataclass(frozen=True)
class RegionalGeometrySpec:
    """A regional comoving pullback metric on the reference carrier.

    ``metric_volume_ratio`` is
    ``J_r=dmu_(Phi_r^* gamma_r)/dmu_0`` and ``metric_inverse`` is
    ``(Phi_r^* gamma_r)^(-1)``.  Consequently the weak-form tensor density is
    ``K_r=J_r metric_inverse``.  These are Phase 1E-G specification Eqs. in
    sections 7--8 (explicit model extension; no paper equation number).

    Phase 1F-C-R A01 makes the selected reference density explicit:
    ``dmu_0 = d^d x`` (unit coordinate density), with quadrature cell weights
    ``prod(dx)``. For ``g=Phi_r^* gamma_r``, ``J=sqrt(det(g))`` and
    ``J*sqrt(det(metric_inverse))=1`` pointwise. Independent weighted
    diffusion is outside this Riemannian contract. The determinant check uses
    relative tolerance 2e-12 and zero absolute tolerance in float64.
    """

    region_id: str
    metric_inverse: FloatArray
    metric_volume_ratio: FloatArray
    curvature_class: str
    pullback_provenance: str
    metric_time_independent: bool
    isotropic_reference_backend: bool
    normalization: RegionalMetricNormalization
    metadata: Mapping[str, str]

    def __post_init__(self) -> None:
        inverse = _readonly_float(self.metric_inverse, "metric_inverse")
        ratio = _readonly_float(
            self.metric_volume_ratio, "metric_volume_ratio"
        )
        if inverse.ndim < 3 or inverse.shape[-1] != inverse.shape[-2]:
            raise ContinuumContractError(
                "metric_inverse must have grid_shape + (dimension, dimension)"
            )
        dimension = inverse.shape[-1]
        if ratio.shape != inverse.shape[:-2]:
            raise ContinuumContractError(
                "metric_volume_ratio must match the metric grid shape"
            )
        if np.any(ratio <= 0.0):
            raise ContinuumDegeneracyError(
                "metric_volume_ratio must be strictly positive"
            )
        symmetric = 0.5 * (inverse + np.swapaxes(inverse, -1, -2))
        if not np.allclose(inverse, symmetric, rtol=0.0, atol=1e-13):
            raise ContinuumContractError("metric_inverse must be symmetric")
        eigenvalues = np.linalg.eigvalsh(symmetric.reshape((-1, dimension, dimension)))
        if np.min(eigenvalues) <= 0.0:
            raise ContinuumDegeneracyError("metric_inverse must be SPD")
        if not isinstance(self.metric_time_independent, bool):
            raise ContinuumContractError(
                "metric_time_independent must be declared explicitly"
            )
        if not isinstance(self.isotropic_reference_backend, bool):
            raise ContinuumContractError(
                "isotropic_reference_backend must be declared explicitly"
            )
        if not isinstance(self.normalization, RegionalMetricNormalization):
            raise ContinuumContractError(
                "regional metric-normalization provenance is required"
            )
        object.__setattr__(self, "metric_inverse", inverse)
        object.__setattr__(self, "metric_volume_ratio", ratio)
        self.validate_metric_measure()
        object.__setattr__(
            self, "metadata", MappingProxyType(dict(self.metadata))
        )

    def validate_metric_measure(self) -> None:
        """Revalidate the pointwise A01 relation, including at operator assembly.

        Logarithms avoid determinant/product overflow. The bounds are exactly
        ``1-rtol <= J/sqrt(det(g)) <= 1+rtol`` with zero absolute tolerance.
        This is the authorized Riemannian contract, not weighted diffusion.
        """
        sign, logdet = np.linalg.slogdet(self.metric_inverse)
        ratio = self.metric_volume_ratio
        if np.any(ratio <= 0.0) or not np.all(np.isfinite(ratio)) or np.any(sign <= 0.0):
            raise ContinuumContractError("pointwise metric/measure data are invalid")
        log_relative = np.log(ratio) + 0.5 * logdet
        if not np.all(np.isfinite(log_relative)) or np.any(
            (log_relative < np.log1p(-METRIC_MEASURE_RTOL))
            | (log_relative > np.log1p(METRIC_MEASURE_RTOL))
        ):
            raise ContinuumContractError(
                "pointwise metric/measure mismatch: J must equal sqrt(det(g)) "
                "for unit reference coordinate density"
            )

    @property
    def grid_shape(self) -> tuple[int, ...]:
        return self.metric_volume_ratio.shape

    @property
    def dimension(self) -> int:
        return self.metric_inverse.shape[-1]

    @property
    def elliptic_tensor_density(self) -> FloatArray:
        """Return ``K_r^{ij}=J_r gamma_hat_r^{ij}`` (Phase 1E-G section 7)."""
        result = (
            self.metric_volume_ratio[..., np.newaxis, np.newaxis]
            * self.metric_inverse
        )
        result.setflags(write=False)
        return result

    @property
    def inverse_metric_eigenvalue_bounds(self) -> tuple[float, float]:
        values = np.linalg.eigvalsh(
            self.metric_inverse.reshape((-1, self.dimension, self.dimension))
        )
        return float(np.min(values)), float(np.max(values))

    @property
    def tensor_density_eigenvalue_bounds(self) -> tuple[float, float]:
        values = np.linalg.eigvalsh(
            self.elliptic_tensor_density.reshape(
                (-1, self.dimension, self.dimension)
            )
        )
        return float(np.min(values)), float(np.max(values))


@dataclass(frozen=True)
class ContinuumCarrierSpec:
    """Periodic computational carrier and separately named target geometry."""

    dimension: int
    grid_shape: tuple[int, ...]
    periodicity: tuple[bool, ...]
    reference_measure_weights: FloatArray
    grid_spacing: tuple[float, ...]
    target_geometry: RegionalGeometrySpec
    topology: str
    physical_status: str
    target_scalarization_id: str

    def __post_init__(self) -> None:
        if self.dimension not in (1, 2, 3):
            raise ContinuumContractError("reference backend supports dimensions 1, 2, 3")
        if len(self.grid_shape) != self.dimension or any(n < 3 for n in self.grid_shape):
            raise ContinuumContractError(
                "grid_shape must contain at least three cells per dimension"
            )
        if len(self.periodicity) != self.dimension or not all(self.periodicity):
            raise ContinuumContractError(
                "only an explicitly periodic T3/Td reference backend is supported"
            )
        if len(self.grid_spacing) != self.dimension or any(
            not np.isfinite(h) or h <= 0.0 for h in self.grid_spacing
        ):
            raise ContinuumContractError("grid_spacing must be finite and positive")
        weights = _readonly_float(
            self.reference_measure_weights, "reference_measure_weights"
        )
        if weights.shape != self.grid_shape or np.any(weights <= 0.0):
            raise ContinuumContractError(
                "reference_measure_weights must be positive on the grid"
            )
        if not np.allclose(weights, weights.flat[0], rtol=0.0, atol=1e-15):
            raise ContinuumContractError(
                "the structured reference backend currently requires uniform dmu_0 weights"
            )
        if not np.allclose(
            weights, np.prod(self.grid_spacing),
            rtol=METRIC_MEASURE_RTOL, atol=METRIC_MEASURE_ATOL,
        ):
            raise ContinuumContractError(
                "reference measure requires unit coordinate density: weights=prod(dx)"
            )
        if self.target_geometry.grid_shape != self.grid_shape:
            raise ContinuumContractError("target geometry grid does not match the carrier")
        if self.target_geometry.dimension != self.dimension:
            raise ContinuumContractError("target geometry dimension does not match")
        if self.topology != "PERIODIC_REFERENCE_TORUS":
            raise ContinuumContractError("unsupported topology")
        if self.physical_status != CARRIER_PHYSICAL_STATUS:
            raise ContinuumContractError(
                "carrier must remain COMPUTATIONAL_REFERENCE_CARRIER_ONLY"
            )
        if not self.target_scalarization_id:
            raise ContinuumContractError("target scalarization must be separately named")
        object.__setattr__(self, "reference_measure_weights", weights)

    @property
    def physical_volume_semantics_authorized(self) -> bool:
        """Whether literal metric measure may represent a physical 3-volume."""
        return self.dimension == PHYSICAL_VOLUME_DIMENSION

    def require_physical_volume_semantics(self, *, context: str) -> None:
        """Fail closed unless physical Timescape three-volume semantics apply.

        Under the human-approved Phase 1E-G v3 dimensional contract
        ``gamma'=c^2 gamma`` gives ``mu'_d=c^d mu_d``. With ``a'=a/c``,
        ``mu'_d (a')^3=c^(d-3) mu_d a^3``. There is no paper equation number:
        this is the explicit v3 model-extension guard supplied by the user.
        """
        if not self.physical_volume_semantics_authorized:
            raise ContinuumDimensionalContractError(
                f"{context} requires spatial_dimension == 3; dimension "
                f"{self.dimension} supplies only a literal reduced-dimensional "
                "metric measure and has no validated 3-D lift provenance"
            )


@dataclass(frozen=True)
class MorphologySpec:
    """Required external wall/void morphology and pullback provenance."""

    morphology_id: str
    wall_domain: BoolArray
    void_domain: BoolArray
    interface_id: str
    wall_pullback_id: str
    void_pullback_id: str
    normal_convention: str
    interface_physical_status: str
    fixed_reference_partition: bool
    fixed_interface: bool
    pullbacks_time_independent: bool
    connected_carrier: bool
    source_injection_provenance: Mapping[str, str]

    def __post_init__(self) -> None:
        wall = _readonly_bool(self.wall_domain, "wall_domain")
        void = _readonly_bool(self.void_domain, "void_domain")
        if wall.shape != void.shape:
            raise ContinuumContractError("regional domains must share a grid")
        if np.any(wall & void):
            raise ContinuumContractError("wall and void domains overlap")
        if not np.all(wall | void):
            raise ContinuumContractError("wall and void domains do not cover the carrier")
        if not np.any(wall) or not np.any(void):
            raise ContinuumDegeneracyError("both regional domains must be nonempty")
        if self.normal_convention != COMMON_REFERENCE_NORMAL_WALL_TO_VOID_1E_G:
            raise ContinuumContractError("unsupported common-normal convention")
        if self.interface_physical_status != INTERFACE_PHYSICAL_STATUS:
            raise ContinuumContractError(
                "Gamma must remain a MATHEMATICAL_TRANSFER_INTERFACE"
            )
        flags = (
            self.fixed_reference_partition,
            self.fixed_interface,
            self.pullbacks_time_independent,
            self.connected_carrier,
        )
        if not all(isinstance(flag, bool) for flag in flags):
            raise ContinuumContractError("morphology branch flags must be explicit booleans")
        if not self.connected_carrier:
            raise ContinuumDegeneracyError(
                "disconnected morphology would introduce extra kernel modes"
            )
        if set(self.source_injection_provenance) != {"wall", "void"}:
            raise ContinuumContractError(
                "wall and void source injection provenance are required"
            )
        if not all(
            (
                self.morphology_id,
                self.interface_id,
                self.wall_pullback_id,
                self.void_pullback_id,
            )
        ):
            raise ContinuumContractError("morphology provenance identifiers are required")
        object.__setattr__(self, "wall_domain", wall)
        object.__setattr__(self, "void_domain", void)
        object.__setattr__(
            self,
            "source_injection_provenance",
            MappingProxyType(dict(self.source_injection_provenance)),
        )


@dataclass(frozen=True)
class FixedReferenceBranchSpec:
    """The explicit branch from which ``A_dot=A_ddot=J_f=0`` follows.

    This is the authorised Phase 1E-G specification sections 18--20; it is
    not a universal Timescape identity and has no paper equation number.
    """

    branch_id: str
    fixed_reference_partition: bool
    fixed_interface: bool
    fixed_comoving_pullback_geometries: bool
    fixed_target_scalarization: bool
    homogeneous_background_clock_map: bool
    spatial_clock_perturbation: bool

    def validate_selected_branch(self) -> None:
        if self.branch_id != FIXED_REFERENCE_BRANCH:
            raise ContinuumContractError("unsupported reference-domain branch")
        if not all(
            (
                self.fixed_reference_partition,
                self.fixed_interface,
                self.fixed_comoving_pullback_geometries,
                self.fixed_target_scalarization,
                self.homogeneous_background_clock_map,
            )
        ):
            raise ContinuumContractError(
                "moving/time-dependent Phase 1E-G geometry is unsupported"
            )
        if self.spatial_clock_perturbation:
            raise ContinuumContractError(
                "spatially varying clock lapse is unsupported on the selected branch"
            )


@dataclass(frozen=True)
class ContinuumEllipticClosureConfig:
    """Every scientific/numerical tolerance is caller supplied; no defaults."""

    ellipticity_min: float
    coercivity_min: float
    source_compatibility_tolerance: float
    global_mean_tolerance: float
    interface_value_tolerance: float
    interface_flux_tolerance: float
    volume_fraction_tolerance: float
    equal_geometry_identity_tolerance: float
    convergence_l2_min_rate: float
    convergence_energy_min_rate: float
    morphology_sensitivity_norm: str
    morphology_sensitivity_reference_scale: float
    morphology_sensitivity_floor: float
    morphology_convergence_tolerance: float
    kernel_tolerance: float
    symmetry_tolerance: float
    downstream_configuration: H1Configuration

    def __post_init__(self) -> None:
        positive = (
            "ellipticity_min",
            "coercivity_min",
            "morphology_sensitivity_reference_scale",
            "morphology_sensitivity_floor",
            "kernel_tolerance",
        )
        nonnegative = (
            "source_compatibility_tolerance",
            "global_mean_tolerance",
            "interface_value_tolerance",
            "interface_flux_tolerance",
            "volume_fraction_tolerance",
            "equal_geometry_identity_tolerance",
            "convergence_l2_min_rate",
            "convergence_energy_min_rate",
            "symmetry_tolerance",
            "morphology_convergence_tolerance",
        )
        for name in positive:
            value = float(getattr(self, name))
            if not np.isfinite(value) or value <= 0.0:
                raise ContinuumContractError(f"{name} must be finite and positive")
        for name in nonnegative:
            value = float(getattr(self, name))
            if not np.isfinite(value) or value < 0.0:
                raise ContinuumContractError(f"{name} must be finite and nonnegative")
        if not isinstance(self.downstream_configuration, H1Configuration):
            raise ContinuumContractError("explicit Phase 1E-F configuration is required")
        if self.morphology_sensitivity_norm != MORPHOLOGY_NORM_TARGET_METRIC_L2:
            raise ContinuumContractError(
                "unsupported morphology sensitivity norm definition"
            )


def conformal_regional_geometry(
    *,
    region_id: str,
    conformal_factor: ArrayLike,
    dimension: int,
    curvature_class: str,
    pullback_provenance: str,
    normalization: RegionalMetricNormalization,
    metadata: Mapping[str, str],
) -> RegionalGeometrySpec:
    """Construct ``gamma=lambda^2 I``, ``J=lambda^d``, and its inverse.

    This metric identity is the explicit Phase 1E-G model-extension contract
    in sections 7 and 27 (no paper equation number).  In two dimensions,
    ``lambda=2/(1-r^2)`` is the Poincare-disk metric of scalar curvature -2
    (Gaussian curvature -1) on ``r<1``.
    """
    factor = _readonly_float(conformal_factor, "conformal_factor")
    if factor.ndim != dimension or np.any(factor <= 0.0):
        raise ContinuumContractError(
            "conformal_factor must be positive with rank equal to dimension"
        )
    inverse = np.zeros(factor.shape + (dimension, dimension), dtype=np.float64)
    inverse_scalar = factor**-2
    for axis in range(dimension):
        inverse[..., axis, axis] = inverse_scalar
    return RegionalGeometrySpec(
        region_id=region_id,
        metric_inverse=inverse,
        metric_volume_ratio=factor**dimension,
        curvature_class=curvature_class,
        pullback_provenance=pullback_provenance,
        metric_time_independent=True,
        isotropic_reference_backend=True,
        normalization=normalization,
        metadata=metadata,
    )


def flat_regional_geometry(
    *,
    region_id: str,
    grid_shape: tuple[int, ...],
    pullback_provenance: str,
    normalization: RegionalMetricNormalization,
    metadata: Mapping[str, str],
) -> RegionalGeometrySpec:
    """Return the unit flat comoving metric (Phase 1E-G section 7 closure)."""
    return conformal_regional_geometry(
        region_id=region_id,
        conformal_factor=np.ones(grid_shape, dtype=np.float64),
        dimension=len(grid_shape),
        curvature_class="FLAT_COMOVING",
        pullback_provenance=pullback_provenance,
        normalization=normalization,
        metadata=metadata,
    )


def layered_morphology(
    *,
    morphology_id: str,
    grid_shape: tuple[int, ...],
    axis: int,
    wall_cell_count: int,
    wall_pullback_id: str,
    void_pullback_id: str,
) -> MorphologySpec:
    """Build an explicit layered validation morphology, never a physical default."""
    if axis < 0 or axis >= len(grid_shape):
        raise ContinuumContractError("layer axis is outside the carrier dimension")
    if wall_cell_count <= 0 or wall_cell_count >= grid_shape[axis]:
        raise ContinuumContractError("wall_cell_count must leave two nonempty regions")
    coordinate = np.indices(grid_shape)[axis]
    wall = coordinate < wall_cell_count
    return MorphologySpec(
        morphology_id=morphology_id,
        wall_domain=wall,
        void_domain=~wall,
        interface_id=f"{morphology_id}:periodic-layer-interface",
        wall_pullback_id=wall_pullback_id,
        void_pullback_id=void_pullback_id,
        normal_convention=COMMON_REFERENCE_NORMAL_WALL_TO_VOID_1E_G,
        interface_physical_status=INTERFACE_PHYSICAL_STATUS,
        fixed_reference_partition=True,
        fixed_interface=True,
        pullbacks_time_independent=True,
        connected_carrier=True,
        source_injection_provenance={
            "wall": f"{morphology_id}:wall-mask-injection",
            "void": f"{morphology_id}:void-mask-injection",
        },
    )


def island_morphology(
    *,
    morphology_id: str,
    grid_shape: tuple[int, int],
    void_lower: tuple[int, int],
    void_upper: tuple[int, int],
    wall_pullback_id: str,
    void_pullback_id: str,
) -> MorphologySpec:
    """Build an explicit connected 2-D island comparator morphology."""
    if any(lo < 1 for lo in void_lower) or any(
        hi >= n - 1 for hi, n in zip(void_upper, grid_shape, strict=True)
    ):
        raise ContinuumContractError(
            "island must stay inside the periodic carrier for a connected wall region"
        )
    if any(lo >= hi for lo, hi in zip(void_lower, void_upper, strict=True)):
        raise ContinuumContractError("void island bounds are malformed")
    indices = np.indices(grid_shape)
    void = np.ones(grid_shape, dtype=np.bool_)
    for axis in range(2):
        void &= (indices[axis] >= void_lower[axis]) & (
            indices[axis] < void_upper[axis]
        )
    return MorphologySpec(
        morphology_id=morphology_id,
        wall_domain=~void,
        void_domain=void,
        interface_id=f"{morphology_id}:closed-island-interface",
        wall_pullback_id=wall_pullback_id,
        void_pullback_id=void_pullback_id,
        normal_convention=COMMON_REFERENCE_NORMAL_WALL_TO_VOID_1E_G,
        interface_physical_status=INTERFACE_PHYSICAL_STATUS,
        fixed_reference_partition=True,
        fixed_interface=True,
        pullbacks_time_independent=True,
        connected_carrier=True,
        source_injection_provenance={
            "wall": f"{morphology_id}:wall-mask-injection",
            "void": f"{morphology_id}:void-mask-injection",
        },
    )
