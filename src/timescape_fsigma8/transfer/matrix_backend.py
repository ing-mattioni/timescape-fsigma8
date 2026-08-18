"""Finite-dimensional reference backend for the Phase 1E-F H1 contract.

The matrices in this module are research-validation analogues of the
continuum transmission operator.  They are not a spatial discretisation of
Timescape and carry no observational interpretation.

Scientific authority: the user-approved Phase 1E-F specification sections
``h1-functional-contract``, ``implementation-architecture`` and
``provenance-preserving-realization``.  The inverse derivative identity
``d(A^-1)/dt = -A^-1 A_dot A^-1`` is the explicitly authorised operator
contract; it is not imported from the unlicensed upstream notebook.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]


def _readonly_vector(values: ArrayLike, name: str) -> FloatArray:
    vector = np.array(values, dtype=np.float64, copy=True)
    if vector.ndim != 1 or not np.all(np.isfinite(vector)):
        raise ValueError(f"{name} must be a finite one-dimensional array")
    vector.setflags(write=False)
    return vector


def _readonly_matrix(values: ArrayLike, name: str) -> FloatArray:
    matrix = np.array(values, dtype=np.float64, copy=True)
    if matrix.ndim != 2 or not np.all(np.isfinite(matrix)):
        raise ValueError(f"{name} must be a finite two-dimensional array")
    matrix.setflags(write=False)
    return matrix


@dataclass(frozen=True)
class ScalarJet:
    """Value and first two analytic common-time derivatives of a scalar."""

    value: float
    first: float
    second: float

    def __post_init__(self) -> None:
        values = np.asarray((self.value, self.first, self.second), dtype=np.float64)
        if not np.all(np.isfinite(values)):
            raise ValueError("ScalarJet entries must be finite")
        object.__setattr__(self, "value", float(self.value))
        object.__setattr__(self, "first", float(self.first))
        object.__setattr__(self, "second", float(self.second))


@dataclass(frozen=True)
class VectorJet:
    """Value and first two analytic common-time derivatives of a vector."""

    value: FloatArray
    first: FloatArray
    second: FloatArray

    def __post_init__(self) -> None:
        value = _readonly_vector(self.value, "VectorJet.value")
        first = _readonly_vector(self.first, "VectorJet.first")
        second = _readonly_vector(self.second, "VectorJet.second")
        if first.shape != value.shape or second.shape != value.shape:
            raise ValueError("VectorJet entries must have identical shapes")
        object.__setattr__(self, "value", value)
        object.__setattr__(self, "first", first)
        object.__setattr__(self, "second", second)


@dataclass(frozen=True)
class MatrixJet:
    """Value and first two analytic common-time derivatives of a matrix."""

    value: FloatArray
    first: FloatArray
    second: FloatArray

    def __post_init__(self) -> None:
        value = _readonly_matrix(self.value, "MatrixJet.value")
        first = _readonly_matrix(self.first, "MatrixJet.first")
        second = _readonly_matrix(self.second, "MatrixJet.second")
        if first.shape != value.shape or second.shape != value.shape:
            raise ValueError("MatrixJet entries must have identical shapes")
        object.__setattr__(self, "value", value)
        object.__setattr__(self, "first", first)
        object.__setattr__(self, "second", second)


@dataclass(frozen=True)
class TransmissionSolution:
    """One provenance-preserving source response and its carrier solution."""

    provenance: str
    field: VectorJet
    raw_source: VectorJet
    injected_source: VectorJet


@dataclass(frozen=True)
class JointTransmissionState:
    """Wall, void and combined responses of one coupled transmission solve."""

    wall: TransmissionSolution
    void: TransmissionSolution
    carrier_field: VectorJet


class DenseH1TransmissionBackend:
    """Constrained matrix analogue of the H1 coupled transmission operator.

    The fixed admissible subspace is the null space of the explicitly supplied
    value-jump rows, conormal-flux-jump rows, and exactly one global mean row.
    No wall-only or void-only constant projection exists.  On that subspace,
    ``A_reduced = Q.T @ A @ Q`` represents ``A_Gamma`` and is solved jointly.

    Source: user-approved Phase 1E-F specification
    ``h1-functional-contract``.  This is a compatible imported mathematical
    contract, not an equation copied from the pinned upstream source.
    """

    scientific_role = "NONPHYSICAL_MATRIX_OPERATOR_CONTRACT_REFERENCE_BACKEND"

    def __init__(
        self,
        *,
        operator: MatrixJet,
        wall_source_injection: ArrayLike,
        void_source_injection: ArrayLike,
        value_jump_operator: ArrayLike,
        flux_jump_operator: ArrayLike,
        global_mean_weights: ArrayLike,
        constraint_rank_tolerance: float,
        symmetry_tolerance: float,
        operator_time_regularity: str,
        fixed_reference_constraints: bool,
        interval_coercivity_lower_bound: float,
    ) -> None:
        if operator.value.shape[0] != operator.value.shape[1]:
            raise ValueError("operator matrices must be square")
        if not np.isfinite(constraint_rank_tolerance) or constraint_rank_tolerance <= 0.0:
            raise ValueError("constraint_rank_tolerance must be finite and positive")
        if not np.isfinite(symmetry_tolerance) or symmetry_tolerance < 0.0:
            raise ValueError("symmetry_tolerance must be finite and nonnegative")
        if operator_time_regularity != "C2_COMMON_TIME":
            raise ValueError(
                "operator_time_regularity must explicitly be C2_COMMON_TIME"
            )
        if fixed_reference_constraints is not True:
            raise ValueError(
                "this backend requires explicitly fixed Lagrangian interface constraints"
            )
        if (
            not np.isfinite(interval_coercivity_lower_bound)
            or interval_coercivity_lower_bound <= 0.0
        ):
            raise ValueError(
                "interval_coercivity_lower_bound must be finite and positive"
            )

        size = operator.value.shape[0]
        wall = _readonly_vector(wall_source_injection, "wall_source_injection")
        void = _readonly_vector(void_source_injection, "void_source_injection")
        mean = _readonly_vector(global_mean_weights, "global_mean_weights")
        value_jump = _readonly_matrix(value_jump_operator, "value_jump_operator")
        flux_jump = _readonly_matrix(flux_jump_operator, "flux_jump_operator")
        if wall.shape != (size,) or void.shape != (size,) or mean.shape != (size,):
            raise ValueError("source injections and global mean weights must match operator size")
        if value_jump.shape[1] != size or flux_jump.shape[1] != size:
            raise ValueError("jump operators must match operator size")
        if value_jump.shape[0] == 0 or flux_jump.shape[0] == 0:
            raise ValueError("value and flux jump operators must each contain a row")
        if not np.any(wall) or not np.any(void):
            raise ValueError("wall and void source injections must both be nonzero")
        if not np.any(mean):
            raise ValueError("global_mean_weights must be nonzero")
        if np.sum(mean) == 0.0:
            raise ValueError("global_mean_weights must have a nonzero total weight")

        interface_constraints = np.vstack((value_jump, flux_jump))
        all_constraints = np.vstack((interface_constraints, mean[np.newaxis, :]))
        normalized = all_constraints.copy()
        norms = np.linalg.norm(normalized, axis=1)
        if np.any(norms == 0.0):
            raise ValueError("constraint rows must be nonzero")
        normalized /= norms[:, np.newaxis]

        interface_rank = int(
            np.linalg.matrix_rank(interface_constraints, tol=constraint_rank_tolerance)
        )
        full_rank = int(np.linalg.matrix_rank(normalized, tol=constraint_rank_tolerance))
        if full_rank - interface_rank != 1:
            raise ValueError(
                "the single global mean constraint must remove exactly one additional mode"
            )
        _, singular_values, vh = np.linalg.svd(normalized, full_matrices=True)
        rank = int(np.count_nonzero(singular_values > constraint_rank_tolerance))
        basis = vh[rank:].T
        if basis.shape[1] == 0:
            raise ValueError("transmission constraints leave no admissible degrees of freedom")

        reduced = tuple(basis.T @ matrix @ basis for matrix in (
            operator.value,
            operator.first,
            operator.second,
        ))
        for index, matrix in enumerate(reduced):
            asymmetry = np.linalg.norm(matrix - matrix.T, ord=np.inf)
            if asymmetry > symmetry_tolerance:
                raise ValueError(
                    f"reduced operator derivative {index} is not symmetric within "
                    f"symmetry_tolerance: {asymmetry}"
                )
        instantaneous_coercivity = float(
            np.min(np.linalg.eigvalsh(0.5 * (reduced[0] + reduced[0].T)))
        )
        if interval_coercivity_lower_bound > instantaneous_coercivity + symmetry_tolerance:
            raise ValueError(
                "declared interval coercivity lower bound exceeds the current "
                "reduced-operator eigenvalue bound"
            )

        self._operator = operator
        self._wall_injection = wall
        self._void_injection = void
        self._value_jump = value_jump
        self._flux_jump = flux_jump
        self._mean = mean
        self._basis = np.array(basis, dtype=np.float64, copy=True)
        self._basis.setflags(write=False)
        self._reduced = MatrixJet(*reduced)
        self._constraint_rank_tolerance = float(constraint_rank_tolerance)
        self._symmetry_tolerance = float(symmetry_tolerance)
        self._operator_time_regularity = operator_time_regularity
        self._fixed_reference_constraints = fixed_reference_constraints
        self._interval_coercivity_lower_bound = float(
            interval_coercivity_lower_bound
        )
        self._instantaneous_coercivity_lower_bound = instantaneous_coercivity
        self._interface_constraint_rank = interface_rank
        self._constraint_rank = full_rank

    @property
    def size(self) -> int:
        return self._operator.value.shape[0]

    @property
    def admissible_dimension(self) -> int:
        return self._basis.shape[1]

    @property
    def interface_constraint_rank(self) -> int:
        return self._interface_constraint_rank

    @property
    def total_constraint_rank(self) -> int:
        return self._constraint_rank

    @property
    def global_mean_constraint_count(self) -> int:
        """The H1 contract removes the coupled constant exactly once."""
        return 1

    @property
    def coercivity_lower_bound(self) -> float:
        """Declared uniform lower bound on the configured realization interval."""
        return self._interval_coercivity_lower_bound

    @property
    def instantaneous_coercivity_lower_bound(self) -> float:
        return self._instantaneous_coercivity_lower_bound

    @property
    def operator_time_regularity(self) -> str:
        return self._operator_time_regularity

    @property
    def fixed_reference_constraints(self) -> bool:
        return self._fixed_reference_constraints

    def project_source(self, source: ArrayLike) -> FloatArray:
        """Project a source into ``V_Gamma,0*`` using the joint basis."""
        vector = _readonly_vector(source, "source")
        if vector.shape != (self.size,):
            raise ValueError("source must match backend size")
        return self._basis @ (self._basis.T @ vector)

    def _source_from_amplitude(self, injection: FloatArray, amplitude: ScalarJet) -> VectorJet:
        return VectorJet(
            injection * amplitude.value,
            injection * amplitude.first,
            injection * amplitude.second,
        )

    def solve_source_jet(self, source: VectorJet, *, provenance: str) -> TransmissionSolution:
        """Solve ``A_Gamma u=s`` and its first two analytic derivatives.

        The first derivative is the authorised identity
        ``u_dot=G_Gamma(s_dot-A_Gamma_dot u)``.  Differentiating it once more
        gives ``u_ddot=G_Gamma(s_ddot-A_ddot u-2 A_dot u_dot)``.  These are
        the Phase 1E-F operator-contract equations, not finite differences.
        """
        if source.value.shape != (self.size,):
            raise ValueError("source jet must match backend size")
        reduced_source = VectorJet(
            self._basis.T @ source.value,
            self._basis.T @ source.first,
            self._basis.T @ source.second,
        )
        try:
            value = np.linalg.solve(self._reduced.value, reduced_source.value)
            first = np.linalg.solve(
                self._reduced.value,
                reduced_source.first - self._reduced.first @ value,
            )
            second = np.linalg.solve(
                self._reduced.value,
                reduced_source.second
                - self._reduced.second @ value
                - 2.0 * self._reduced.first @ first,
            )
        except np.linalg.LinAlgError as exc:
            raise ValueError("coupled transmission operator is singular") from exc
        field = VectorJet(self._basis @ value, self._basis @ first, self._basis @ second)
        injected = VectorJet(
            self._basis @ reduced_source.value,
            self._basis @ reduced_source.first,
            self._basis @ reduced_source.second,
        )
        return TransmissionSolution(
            provenance=provenance,
            field=field,
            raw_source=source,
            injected_source=injected,
        )

    def solve_joint(
        self,
        wall_amplitude: ScalarJet,
        void_amplitude: ScalarJet,
        *,
        source_name: str,
    ) -> JointTransmissionState:
        """Return separate wall/void responses and their joint carrier field."""
        wall = self.solve_source_jet(
            self._source_from_amplitude(self._wall_injection, wall_amplitude),
            provenance=f"wall:{source_name}",
        )
        void = self.solve_source_jet(
            self._source_from_amplitude(self._void_injection, void_amplitude),
            provenance=f"void:{source_name}",
        )
        carrier = VectorJet(
            wall.field.value + void.field.value,
            wall.field.first + void.field.first,
            wall.field.second + void.field.second,
        )
        return JointTransmissionState(wall=wall, void=void, carrier_field=carrier)

    def apply_coupled_operator(self, field: ArrayLike) -> FloatArray:
        """Apply the constrained operator for the provenance roundtrip claim."""
        vector = _readonly_vector(field, "field")
        if vector.shape != (self.size,):
            raise ValueError("field must match backend size")
        coordinates = self._basis.T @ vector
        return self._basis @ (self._reduced.value @ coordinates)

    def apply_inverse_derivative(self, source: ArrayLike) -> FloatArray:
        """Evaluate -G_Gamma A_Gamma_dot G_Gamma on a fixed source.

        Source: the explicitly authorized Phase 1E-F operator-derivative
        contract. This method evaluates the inverse-family derivative and
        makes no physical discretization claim.
        """
        vector = _readonly_vector(source, "source")
        if vector.shape != (self.size,):
            raise ValueError("source must match backend size")
        reduced_source = self._basis.T @ vector
        try:
            solution = np.linalg.solve(self._reduced.value, reduced_source)
            derivative = np.linalg.solve(
                self._reduced.value,
                -self._reduced.first @ solution,
            )
        except np.linalg.LinAlgError as exc:
            raise ValueError("coupled transmission operator is singular") from exc
        return self._basis @ derivative

    def apply_coupled_operator_jet(self, field: VectorJet) -> VectorJet:
        """Apply the operator through second analytic common-time order."""
        if field.value.shape != (self.size,):
            raise ValueError("field jet must match backend size")
        coordinates = VectorJet(
            self._basis.T @ field.value,
            self._basis.T @ field.first,
            self._basis.T @ field.second,
        )
        value = self._reduced.value @ coordinates.value
        first = (
            self._reduced.first @ coordinates.value
            + self._reduced.value @ coordinates.first
        )
        second = (
            self._reduced.second @ coordinates.value
            + 2.0 * self._reduced.first @ coordinates.first
            + self._reduced.value @ coordinates.second
        )
        return VectorJet(
            self._basis @ value,
            self._basis @ first,
            self._basis @ second,
        )

    def value_jump(self, field: ArrayLike) -> FloatArray:
        vector = _readonly_vector(field, "field")
        if vector.shape != (self.size,):
            raise ValueError("field must match backend size")
        return self._value_jump @ vector

    def flux_jump(self, field: ArrayLike) -> FloatArray:
        vector = _readonly_vector(field, "field")
        if vector.shape != (self.size,):
            raise ValueError("field must match backend size")
        return self._flux_jump @ vector

    def global_mean(self, field: ArrayLike) -> float:
        vector = _readonly_vector(field, "field")
        if vector.shape != (self.size,):
            raise ValueError("field must match backend size")
        return float(self._mean @ vector / np.sum(self._mean))


class DenseCarrierOperator:
    """Explicit linear carrier operator with analytic time derivatives."""

    def __init__(self, operator: MatrixJet) -> None:
        self._operator = operator

    @property
    def input_size(self) -> int:
        return self._operator.value.shape[1]

    @property
    def output_size(self) -> int:
        return self._operator.value.shape[0]

    def evaluate(self, inputs: VectorJet) -> VectorJet:
        """Apply ``M(t)`` using the exact product-rule derivative jet."""
        if inputs.value.shape != (self.input_size,):
            raise ValueError("carrier-operator input has the wrong size")
        value = self._operator.value @ inputs.value
        first = self._operator.first @ inputs.value + self._operator.value @ inputs.first
        second = (
            self._operator.second @ inputs.value
            + 2.0 * self._operator.first @ inputs.first
            + self._operator.value @ inputs.second
        )
        return VectorJet(value, first, second)
