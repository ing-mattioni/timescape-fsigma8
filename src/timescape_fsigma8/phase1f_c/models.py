"""Typed contracts for the conditional Phase 1F-C wall geometry.

This module does not solve a perturbed Einstein system.  It binds the frozen
Phase 1F-B scalar boost to an explicitly selected background clock, an
explicit H1-to-wall spatial realization, and an external perturbative wall
lapse.  The kinematic equations evaluated by :mod:`phase1f_c.geometry` are
cited at their implementation sites.

Reference keys: W09 is Wiltshire, Phys. Rev. D 80, 123512 (2009),
arXiv:0909.0749; BMR is Buchert--Mourier--Roy, arXiv:1912.04213v2; BDE is
Bruni--Dunsby--Ellis, ApJ 395 (1992) 34.
"""

from __future__ import annotations

from timescape_fsigma8.components import ComponentRepresentation
from timescape_fsigma8.scientific_status import REMAINING_SCIENTIFIC_CLOSURES

from dataclasses import dataclass, field, fields
from enum import Enum
from types import MappingProxyType
from typing import Mapping

import numpy as np
from numpy.typing import ArrayLike, NDArray

from timescape_fsigma8.phase1f_a.models import (
    RegionalDomainSpec,
    canonical_state,
)
from timescape_fsigma8.phase1f_b import ScalarDustWallBoostResult


FloatArray = NDArray[np.float64]

PHASE = "1F-C"
REALIZATION_ID = (
    "H1-1F-C-CLOCK-ANCHORED-SCALAR-NORMAL-KINEMATIC-GEOMETRY-V1"
)
SHORT_REALIZATION_ID = "H1-1F-C-CA-SNKG-V1"
SCIENTIFIC_REALIZATION_READINESS = "READY_FOR_CONDITIONAL_IMPLEMENTATION"
PHASE_1F_C_SCIENTIFIC_VERDICT = (
    "PARTIAL_GEOMETRIC_CLOSURE_DERIVED_NEW_PERTURBED_GEOMETRIC_DYNAMICS_REQUIRED"
)

DERIVED_FROM_FROZEN_TIMESCAPE = "DERIVED_FROM_FROZEN_TIMESCAPE"
DERIVED_FROM_GENERIC_GR = "DERIVED_FROM_GENERIC_GR"
DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION = (
    "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
)
EXTERNAL_CLOSURE_INPUT = "EXTERNAL_CLOSURE_INPUT"
GAUGE_CHOICE = "GAUGE_CHOICE"
MODEL_SECTOR_RESTRICTION = "MODEL_SECTOR_RESTRICTION"
NOT_DERIVED = "NOT_DERIVED"
REJECTED_UNSUPPORTED = "REJECTED_UNSUPPORTED"

COMMON_BACKGROUND_CLOCK = "CONDITIONALLY_CLOSED"
COMMON_BACKGROUND_CLOCK_RATE = (
    "alpha_W_EQUALS_INVERSE_gamma_w_UNDER_SELECTED_CLOCK_MAP"
)
COMMON_PERTURBED_4D_SPACETIME = "CONDITIONALLY_PARAMETERIZED_LOCALLY"
GLOBAL_PERTURBED_DRESSED_SPACETIME = "NOT_DERIVED"
PERTURBED_WALL_CONGRUENCE = "CONDITIONALLY_DEFINED_AS_HYPERSURFACE_NORMAL"
WALL_ADM_LAPSE_BACKGROUND = "CONDITIONALLY_DERIVED"
WALL_LAPSE_PERTURBATION = "NOT_DERIVED_FROM_FROZEN_TIMESCAPE"
WALL_ACCELERATION = "CONDITIONALLY_DERIVED_FROM_LAPSE_PERTURBATION"
WALL_EXPANSION_PERTURBATION = (
    "CONDITIONALLY_DERIVED_FROM_FROZEN_COMPATIBILITY"
)
WALL_VORTICITY = "ZERO_IN_SELECTED_NORMAL_BRANCH"
WALL_SHEAR = "ZERO_BY_MODEL_SECTOR_RESTRICTION"
H1_TO_WALL_SPATIAL_PULLBACK = "REQUIRED_EXTERNAL_CLOSURE_INPUT"
SPATIAL_OPERATOR_INPUT_SEMANTICS = "REFERENCE_COMOVING"
PHYSICAL_LAPLACIAN_SCALING = "APPLIED_BY_PHASE_1F_C"
# Physical/reference derivative relation from BDE Eq. (74).
PHYSICAL_LAPLACIAN = "D_W^2 = a_W^-2 Delta_reference"
CALLBACK_NUMERICAL_SEMANTICS_VERIFIABLE_AT_RUNTIME = "NO"
CALLER_OPERATOR_SPACE_DECLARATION = "MANDATORY_TYPED_CONTRACT"
SILENT_OPERATOR_SPACE_DEFAULT = "FORBIDDEN"
ALREADY_PHYSICAL_OPERATOR_AS_REFERENCE_INPUT = "CALLER_CONTRACT_VIOLATION"
WALL_GEOMETRY_DRIVER = (
    "PARTIALLY_DERIVED_REDUCED_EXTERNAL_GEOMETRIC_CLOSURE_REQUIRED"
)
IRREDUCIBLE_GEOMETRIC_INPUT = (
    "NOT_ESTABLISHED_AS_AN_EXHAUSTIVE_IRREDUCIBLE_INPUT_SET"
)
FROZEN_PHASE_1F_B_DIFFERENTIAL_STATE_RANK = 5
DRIVER_ONLY_DIFFERENTIAL_STATE_RANK = 5
OPTIONAL_METRIC_RECONSTRUCTION_DIFFERENTIAL_RANK = 1
AUGMENTED_FULL_METRIC_RUNTIME_RANK = 6
CONDITIONAL_FORWARD_UNIQUENESS = "GRANTED"
UNIQUE_FROM_FROZEN_Y_ALONE = "NOT_GRANTED"
UNIQUE_TIMESCAPE_PREDICTION = "NOT_GRANTED"
FULL_GEOMETRIC_CLOSURE_DERIVED = "NO"
NEW_PERTURBED_GEOMETRIC_DYNAMICS_REQUIRED = "YES"
PHYSICAL_INTERFACE_CLAIM = "NOT_GRANTED"
OBSERVATIONAL_AUTHORIZATION = "NOT_GRANTED"
RSD_AUTHORIZATION = "NOT_GRANTED"
SIGMA8_AUTHORIZATION = "NOT_GRANTED"
FSIGMA8_AUTHORIZATION = "NOT_GRANTED"


class Phase1FCContractError(ValueError):
    """A Phase 1F-C scientific input contract was violated."""


class Phase1FCClockError(Phase1FCContractError):
    """The explicit common-time/wall-clock contract was violated."""


class Phase1FCSpatialClosureError(Phase1FCContractError):
    """The external H1-to-wall spatial realization was invalid."""


class Phase1FCLapseClosureError(Phase1FCContractError):
    """The external perturbative wall-lapse closure was invalid."""


class Phase1FCCompatibilityError(Phase1FCContractError):
    """Frozen boost and supplied wall geometry are incompatible."""


class Phase1FCMetricReconstructionError(Phase1FCContractError):
    """Optional scalar metric-trace reconstruction failed closed."""


class Phase1FCStateIntegrityError(Phase1FCContractError):
    """Live scientific state differs from the validated state."""


class ClockMapBranch(Enum):
    """No implicit alternative clock branch is available."""

    TIMESCAPE_COMMON_TIME_TO_BACKGROUND_WALL_PROPER_TIME = (
        "TIMESCAPE_COMMON_TIME_TO_BACKGROUND_WALL_PROPER_TIME"
    )


class SpatialClosureProvenance(Enum):
    EXTERNAL_GEOMETRIC_CLOSURE = "EXTERNAL_GEOMETRIC_CLOSURE"
    SYNTHETIC_VALIDATION_ONLY = "SYNTHETIC_VALIDATION_ONLY"


class SpatialOperatorInputSemantics(Enum):
    """Declared metric/coordinate space of supplied wall operators.

    Phase 1F-C accepts only ``REFERENCE_COMOVING`` operators.  The
    ``WALL_PHYSICAL`` member exists so an unsupported declaration is explicit
    and rejected rather than coerced.  There is no implicit operator-space
    default.
    """

    REFERENCE_COMOVING = "REFERENCE_COMOVING"
    WALL_PHYSICAL = "WALL_PHYSICAL"


class LapseClosureProvenance(Enum):
    EXTERNAL_GEOMETRIC_CLOSURE = "EXTERNAL_GEOMETRIC_CLOSURE"
    SYNTHETIC_VALIDATION_ONLY = "SYNTHETIC_VALIDATION_ONLY"


class WallNormalSector(Enum):
    SCALAR_LONGITUDINAL_HYPERSURFACE_NORMAL_SHEAR_FREE_LOCAL = (
        "SCALAR_LONGITUDINAL_HYPERSURFACE_NORMAL_SHEAR_FREE_LOCAL"
    )


class ShiftGauge(Enum):
    ZERO_SHIFT = "ZERO_SHIFT"


class MetricTraceBackgroundSplit(Enum):
    EXPLICIT_WEIGHTED_MEAN_ZERO_PERTURBATION = (
        "EXPLICIT_WEIGHTED_MEAN_ZERO_PERTURBATION"
    )


def _readonly_float(values: ArrayLike, name: str) -> FloatArray:
    result = np.array(values, dtype=np.float64, copy=True)
    if not np.all(np.isfinite(result)):
        raise Phase1FCContractError(f"{name} must contain only finite values")
    result.setflags(write=False)
    return result


def _token(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise Phase1FCContractError(f"{name} must be an explicit nonempty token")


def _positive(value: float, name: str) -> None:
    if not np.isfinite(value) or value <= 0.0:
        raise Phase1FCContractError(f"{name} must be finite and positive")


def _seal(instance: object, state: object) -> None:
    object.__setattr__(instance, "_integrity_token", canonical_state(state))


def _validate(instance: object, state: object) -> None:
    if getattr(instance, "_integrity_token", None) != canonical_state(state):
        raise Phase1FCStateIntegrityError(
            "Phase 1F-C scientific state changed after validation; construct a new object"
        )


@dataclass(frozen=True, kw_only=True)
class TimescapeWallClockBridge:
    """Selected background clock relation ``alpha_W=1/gamma_w``.

    The Timescape lapse is ``gamma_w=dt/dtau_w`` in W09 Eq. (B7).  Only the
    explicitly selected branch identifying common time with Timescape time
    and background wall-observer proper time with ``tau_w`` permits its
    reciprocal to define ``alpha_W=dtau_W/dt``.  This record has no field from
    which a perturbative ADM lapse can be inferred.
    """

    branch: ClockMapBranch
    timescape_background_lapse: FloatArray
    time_grid: FloatArray
    common_time_coordinate_id: str
    timescape_time_coordinate_id: str
    background_wall_proper_time_id: str
    timescape_wall_proper_time_id: str
    provenance: str
    scientific_classification: str
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if not isinstance(self.branch, ClockMapBranch):
            raise Phase1FCClockError("an explicit supported clock branch is required")
        for name in (
            "common_time_coordinate_id",
            "timescape_time_coordinate_id",
            "background_wall_proper_time_id",
            "timescape_wall_proper_time_id",
            "provenance",
        ):
            _token(getattr(self, name), name)
        if self.common_time_coordinate_id != self.timescape_time_coordinate_id:
            raise Phase1FCClockError("selected branch requires t_common=t_Timescape")
        if self.background_wall_proper_time_id != self.timescape_wall_proper_time_id:
            raise Phase1FCClockError("selected branch requires bar(tau_W)=tau_w")
        if self.scientific_classification != DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION:
            raise Phase1FCClockError("clock bridge classification changed")
        time = _readonly_float(self.time_grid, "time_grid")
        gamma = _readonly_float(
            self.timescape_background_lapse, "timescape_background_lapse"
        )
        if time.ndim != 1 or time.size < 2 or np.any(np.diff(time) <= 0.0):
            raise Phase1FCClockError("time_grid must be one-dimensional and increasing")
        if gamma.shape != time.shape or np.any(gamma <= 0.0):
            raise Phase1FCClockError("gamma_w must be finite, positive, and match time")
        object.__setattr__(self, "time_grid", time)
        object.__setattr__(self, "timescape_background_lapse", gamma)
        _seal(self, self._live_state())

    @property
    def background_wall_proper_time_rate(self) -> FloatArray:
        """Return ``alpha_W=1/gamma_w`` for the selected W09 Eq. (B7) map."""
        self.validate_integrity()
        value = np.array(1.0 / self.timescape_background_lapse, copy=True)
        value.setflags(write=False)
        return value

    def _live_state(self) -> object:
        return (
            self.branch,
            self.timescape_background_lapse,
            self.time_grid,
            self.common_time_coordinate_id,
            self.timescape_time_coordinate_id,
            self.background_wall_proper_time_id,
            self.timescape_wall_proper_time_id,
            self.provenance,
            self.scientific_classification,
        )

    def validate_integrity(self) -> None:
        _validate(self, self._live_state())


@dataclass(frozen=True, kw_only=True)
class H1ToWallSpatialPullback:
    """Explicit external realization of ``D_W`` and ``D_W^2``.

    The dense matrices are an intentionally explicit operator contract.  No
    identity pullback and no H1 regional Laplacian are supplied by default.
    The supplied gradient and Laplace--Beltrami matrices MUST be operators on
    the declared reference/comoving wall geometry.  Phase 1F-C, not the
    caller, converts coordinate covectors to the positive-diagonal Cholesky
    frame of the supplied inverse reference metric, then applies
    ``D_W=a_W^-1 D_gamma_W`` to these orthonormal components and
    ``D_W^2=a_W^-2 Delta_gamma_W`` following BDE Eq. (74).  Already-physical
    operators are unsupported inputs because they would be scaled twice.

    This typed declaration is structural contract enforcement.  Numerical
    matrices (and, more generally, opaque operator implementations) cannot be
    inspected to prove that a caller did not secretly include ``a_W^-1`` or
    ``a_W^-2``.  Falsely declaring an already-physical operator as
    ``REFERENCE_COMOVING`` is therefore a caller contract violation, not a
    runtime-detectable scientific state.

    The gradient input MUST contain lower coordinate scalar derivatives.
    ``wall_reference_metric_inverse=L L^T`` fixes the reference frame:
    ``A_hat=L^T partial(nu)/a``, ``A_i=partial_i nu``, and
    ``A^i=a^-2 gamma^ij partial_j nu`` (BMR Eq. (2.6), tensor conversion).
    No flat metric or unspecified tetrad is silently supplied.
    """

    h1_wall_domain: RegionalDomainSpec
    pullback_matrix: FloatArray
    operator_input_semantics: SpatialOperatorInputSemantics
    wall_reference_gradient_operators: FloatArray
    wall_gradient_component_representation: ComponentRepresentation
    wall_reference_metric_inverse: FloatArray
    wall_reference_laplace_beltrami_operator: FloatArray
    wall_measure_weights: FloatArray
    wall_grid_shape: tuple[int, ...]
    spatial_dimension: int
    h1_geometry_id: str
    wall_geometry_id: str
    pullback_id: str
    morphology_id: str
    domain_id: str
    boundary_realization_id: str
    wall_metric_id: str
    wall_measure_id: str
    gradient_units: str
    laplacian_units: str
    scale_factor_relation: str
    wall_scale_factor_mapping_id: str
    wall_hubble_mapping_id: str
    scale_factor_mapping_classification: str
    provenance: SpatialClosureProvenance
    scientific_classification: str
    constant_preservation_tolerance: float
    operator_symmetry_tolerance: float
    operator_kernel_tolerance: float
    operator_coercivity_minimum: float
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if not isinstance(self.h1_wall_domain, RegionalDomainSpec):
            raise Phase1FCSpatialClosureError("sealed H1 wall domain required")
        self.h1_wall_domain.validate_integrity()
        if self.h1_wall_domain.region != "wall":
            raise Phase1FCSpatialClosureError("source domain must be H1 wall region")
        if (
            self.h1_geometry_id
            != self.h1_wall_domain.geometry.normalization.normalization_id
        ):
            raise Phase1FCSpatialClosureError("H1 geometry identity mismatch")
        if self.morphology_id != self.h1_wall_domain.operator.morphology.morphology_id:
            raise Phase1FCSpatialClosureError("H1 morphology identity mismatch")
        if not isinstance(self.provenance, SpatialClosureProvenance):
            raise Phase1FCSpatialClosureError("explicit spatial provenance required")
        if (
            not isinstance(self.operator_input_semantics, SpatialOperatorInputSemantics)
            or self.operator_input_semantics
            is not SpatialOperatorInputSemantics.REFERENCE_COMOVING
        ):
            raise Phase1FCSpatialClosureError(
                "only explicitly declared REFERENCE_COMOVING wall operators are supported"
            )
        if self.scientific_classification != EXTERNAL_CLOSURE_INPUT:
            raise Phase1FCSpatialClosureError("spatial pullback is an external closure")
        for name in (
            "h1_geometry_id",
            "wall_geometry_id",
            "pullback_id",
            "morphology_id",
            "domain_id",
            "boundary_realization_id",
            "wall_metric_id",
            "wall_measure_id",
            "scale_factor_relation",
            "wall_scale_factor_mapping_id",
            "wall_hubble_mapping_id",
        ):
            _token(getattr(self, name), name)
        if self.gradient_units != "INVERSE_REFERENCE_WALL_LENGTH":
            raise Phase1FCSpatialClosureError("wall gradient units mismatch")
        if self.laplacian_units != "INVERSE_REFERENCE_WALL_LENGTH_SQUARED":
            raise Phase1FCSpatialClosureError("wall Laplacian units mismatch")
        if (
            self.scale_factor_relation
            != "D_W=a_W^-1 D_gamma_W; D_W^2=a_W^-2 Delta_gamma_W"
        ):
            raise Phase1FCSpatialClosureError("wall scale-factor relation mismatch")
        if self.scale_factor_mapping_classification != EXTERNAL_CLOSURE_INPUT:
            raise Phase1FCSpatialClosureError(
                "local wall scale/Hubble mapping must remain an external closure"
            )
        _positive(self.constant_preservation_tolerance, "constant_preservation_tolerance")
        _positive(self.operator_symmetry_tolerance, "operator_symmetry_tolerance")
        _positive(self.operator_kernel_tolerance, "operator_kernel_tolerance")
        _positive(self.operator_coercivity_minimum, "operator_coercivity_minimum")
        if not isinstance(self.spatial_dimension, int) or self.spatial_dimension < 1:
            raise Phase1FCSpatialClosureError("positive integer dimension required")
        if self.spatial_dimension != self.h1_wall_domain.operator.carrier.dimension:
            raise Phase1FCSpatialClosureError(
                "H1 source and local wall spatial dimensions must agree"
            )
        if len(self.wall_grid_shape) != self.spatial_dimension:
            raise Phase1FCSpatialClosureError("wall grid rank/dimension mismatch")
        if any(not isinstance(n, int) or n < 2 for n in self.wall_grid_shape):
            raise Phase1FCSpatialClosureError("wall grid extents must be >=2")
        target_size = int(np.prod(self.wall_grid_shape))
        source_size = self.h1_wall_domain.operator.size
        pullback = _readonly_float(self.pullback_matrix, "pullback_matrix")
        gradient = _readonly_float(
            self.wall_reference_gradient_operators,
            "wall_reference_gradient_operators",
        )
        laplacian = _readonly_float(
            self.wall_reference_laplace_beltrami_operator,
            "wall_reference_laplace_beltrami_operator",
        )
        weights = _readonly_float(self.wall_measure_weights, "wall_measure_weights")
        if pullback.shape != (target_size, source_size):
            raise Phase1FCSpatialClosureError("pullback matrix shape mismatch")
        if gradient.shape != (self.spatial_dimension, target_size, target_size):
            raise Phase1FCSpatialClosureError("gradient operator shape mismatch")
        if self.wall_gradient_component_representation is not ComponentRepresentation.COORDINATE_COVECTOR:
            raise Phase1FCSpatialClosureError("reference gradient must return COORDINATE_COVECTOR derivatives")
        inverse = _readonly_float(self.wall_reference_metric_inverse, "wall_reference_metric_inverse")
        if inverse.shape != (target_size, self.spatial_dimension, self.spatial_dimension):
            raise Phase1FCSpatialClosureError("wall inverse metric shape mismatch")
        # Numerical symmetry tolerance, absolute in the supplied metric units.
        if not np.allclose(inverse, inverse.swapaxes(-1, -2), rtol=0.0, atol=self.operator_symmetry_tolerance):
            raise Phase1FCSpatialClosureError("wall inverse metric must be symmetric")
        if np.min(np.linalg.eigvalsh(inverse)) <= 0.0:
            raise Phase1FCSpatialClosureError("wall inverse metric must be SPD for the Cholesky frame")
        if laplacian.shape != (target_size, target_size):
            raise Phase1FCSpatialClosureError("Laplacian operator shape mismatch")
        if weights.shape != (target_size,) or np.any(weights <= 0.0):
            raise Phase1FCSpatialClosureError("wall measure weights must be positive")
        source_mask = self.h1_wall_domain.mask
        outside = ~source_mask
        if np.any(outside) and np.max(np.abs(pullback[:, outside])) > self.constant_preservation_tolerance:
            raise Phase1FCSpatialClosureError("pullback consumes values outside H1 wall region")
        ones_source = source_mask.astype(np.float64)
        constant_error = np.max(np.abs(pullback @ ones_source - 1.0))
        if constant_error > self.constant_preservation_tolerance:
            raise Phase1FCSpatialClosureError("pullback does not preserve wall constants")
        if np.max(np.abs(gradient @ np.ones(target_size))) > self.constant_preservation_tolerance:
            raise Phase1FCSpatialClosureError("wall gradient does not annihilate constants")
        if np.max(np.abs(laplacian @ np.ones(target_size))) > self.constant_preservation_tolerance:
            raise Phase1FCSpatialClosureError("wall Laplacian does not annihilate constants")
        weighted_negative_laplacian = -weights[:, np.newaxis] * laplacian
        if (
            np.max(
                np.abs(
                    weighted_negative_laplacian
                    - weighted_negative_laplacian.T
                )
            )
            > self.operator_symmetry_tolerance
        ):
            raise Phase1FCSpatialClosureError(
                "wall Laplacian is not self-adjoint in the declared measure"
            )
        eigenvalues = np.linalg.eigvalsh(weighted_negative_laplacian)
        kernel_dimension = int(
            np.count_nonzero(np.abs(eigenvalues) <= self.operator_kernel_tolerance)
        )
        if kernel_dimension != 1:
            raise Phase1FCSpatialClosureError(
                "wall Laplacian must have exactly one scalar constant kernel"
            )
        positive = eigenvalues[eigenvalues > self.operator_kernel_tolerance]
        if (
            positive.size != target_size - 1
            or float(np.min(positive)) < self.operator_coercivity_minimum
        ):
            raise Phase1FCSpatialClosureError(
                "wall Laplacian is not coercive off its declared constant kernel"
            )
        for name, value in (
            ("pullback_matrix", pullback),
            ("wall_reference_gradient_operators", gradient),
            ("wall_reference_metric_inverse", inverse),
            ("wall_reference_laplace_beltrami_operator", laplacian),
            ("wall_measure_weights", weights),
        ):
            object.__setattr__(self, name, value)
        object.__setattr__(self, "wall_grid_shape", tuple(self.wall_grid_shape))
        _seal(self, self._live_state())

    @property
    def wall_size(self) -> int:
        self.validate_integrity()
        return int(np.prod(self.wall_grid_shape))

    def pullback(self, values: ArrayLike) -> FloatArray:
        self.validate_integrity()
        source = _readonly_float(values, "H1 source field")
        if source.shape[-1] != self.h1_wall_domain.operator.size:
            raise Phase1FCSpatialClosureError("H1 field size does not match pullback")
        result = np.asarray(source @ self.pullback_matrix.T, dtype=np.float64)
        result.setflags(write=False)
        return result

    def _live_state(self) -> object:
        return (
            id(self.h1_wall_domain),
            self.pullback_matrix,
            self.operator_input_semantics,
            self.wall_reference_gradient_operators,
            self.wall_gradient_component_representation,
            self.wall_reference_metric_inverse,
            self.wall_reference_laplace_beltrami_operator,
            self.wall_measure_weights,
            self.wall_grid_shape,
            self.spatial_dimension,
            self.h1_geometry_id,
            self.wall_geometry_id,
            self.pullback_id,
            self.morphology_id,
            self.domain_id,
            self.boundary_realization_id,
            self.wall_metric_id,
            self.wall_measure_id,
            self.gradient_units,
            self.laplacian_units,
            self.scale_factor_relation,
            self.wall_scale_factor_mapping_id,
            self.wall_hubble_mapping_id,
            self.scale_factor_mapping_classification,
            self.provenance,
            self.scientific_classification,
            self.constant_preservation_tolerance,
            self.operator_symmetry_tolerance,
            self.operator_kernel_tolerance,
            self.operator_coercivity_minimum,
        )

    def validate_integrity(self) -> None:
        self.h1_wall_domain.validate_integrity()
        _validate(self, self._live_state())


@dataclass(frozen=True, kw_only=True)
class ExternalWallLapsePerturbationClosure:
    """Mandatory external ``nu_W(t,x)`` for the ADM lapse.

    ``N_W=bar(alpha_W) exp(nu_W)`` is the lapse parameterization in BMR
    Eq. (2.5); Phase 1F-C retains its first-order form.  The perturbation is
    never inferred from W09's background ``gamma_w``.
    """

    perturbative_wall_lapse: FloatArray
    time_grid: FloatArray
    common_spacetime_id: str
    wall_congruence_id: str
    common_time_coordinate_id: str
    wall_geometry_id: str
    wall_metric_id: str
    domain_id: str
    provider_id: str
    provenance: LapseClosureProvenance
    scientific_classification: str
    lapse_units: str
    interpolation_policy: str
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for name in (
            "common_spacetime_id",
            "wall_congruence_id",
            "common_time_coordinate_id",
            "wall_geometry_id",
            "wall_metric_id",
            "domain_id",
            "provider_id",
        ):
            _token(getattr(self, name), name)
        if not isinstance(self.provenance, LapseClosureProvenance):
            raise Phase1FCLapseClosureError("explicit lapse provenance required")
        if self.scientific_classification != EXTERNAL_CLOSURE_INPUT:
            raise Phase1FCLapseClosureError("nu_W must remain external")
        if self.lapse_units != "DIMENSIONLESS_PERTURBATION":
            raise Phase1FCLapseClosureError("nu_W units mismatch")
        if self.interpolation_policy != "PIECEWISE_LINEAR_NO_EXTRAPOLATION":
            raise Phase1FCLapseClosureError("explicit no-extrapolation policy required")
        time = _readonly_float(self.time_grid, "time_grid")
        lapse = _readonly_float(self.perturbative_wall_lapse, "perturbative_wall_lapse")
        if time.ndim != 1 or time.size < 2 or np.any(np.diff(time) <= 0.0):
            raise Phase1FCLapseClosureError("time_grid must be increasing")
        if lapse.ndim != 2 or lapse.shape[0] != time.size:
            raise Phase1FCLapseClosureError("nu_W must have shape (time, wall-space)")
        object.__setattr__(self, "time_grid", time)
        object.__setattr__(self, "perturbative_wall_lapse", lapse)
        _seal(self, self._live_state())

    def _live_state(self) -> object:
        return tuple(getattr(self, item.name) for item in fields(self) if not item.name.startswith("_"))

    def validate_integrity(self) -> None:
        _validate(self, self._live_state())


@dataclass(frozen=True, kw_only=True)
class Phase1FCNumerics:
    """Explicit numerical gates; none selects a scientific branch."""

    clock_alignment_tolerance: float
    lapse_alignment_tolerance: float
    boost_clock_residual_tolerance: float
    expansion_compatibility_tolerance: float
    lapse_linear_regime_threshold: float
    metric_trace_mean_tolerance: float
    metric_trace_residual_tolerance: float
    residual_norm_floor: float
    metric_trace_integration_method: str
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for item in fields(self):
            if item.name == "metric_trace_integration_method" or item.name.startswith("_"):
                continue
            _positive(float(getattr(self, item.name)), item.name)
        if self.lapse_linear_regime_threshold >= 1.0:
            raise Phase1FCContractError("lapse threshold must be perturbative (<1)")
        if self.metric_trace_integration_method != "EXPLICIT_TRAPEZOIDAL_COMMON_TIME_GRID":
            raise Phase1FCContractError("unsupported metric-trace integrator")
        _seal(self, self._live_state())

    def _live_state(self) -> object:
        return tuple(
            getattr(self, item.name)
            for item in fields(self)
            if not item.name.startswith("_")
        )

    def validate_integrity(self) -> None:
        _validate(self, self._live_state())


@dataclass(frozen=True, kw_only=True)
class ClockAnchoredWallGeometryScenario:
    """Runtime choices for a conditional Phase 1F-C kinematic realization.

    ID checks do not derive regional/common Timescape background coincidence,
    physical source embedding or all-time constitutive compatibility. Those
    remain NOT_DERIVED in CURRENT_SCIENTIFIC_STATUS.
    """

    boost_result: ScalarDustWallBoostResult
    clock_bridge: TimescapeWallClockBridge
    spatial_pullback: H1ToWallSpatialPullback
    lapse_closure: ExternalWallLapsePerturbationClosure
    common_spacetime_id: str
    wall_congruence_id: str
    regional_wall_dust_congruence_id: str
    selected_sector: WallNormalSector
    shift_gauge: ShiftGauge
    metric_signature: str
    extrinsic_curvature_sign: str
    wall_congruence_classification: str
    shift_classification: str
    vorticity_classification: str
    shear_classification: str
    local_metric_scope: str
    morphology_classification: str
    boundary_classification: str
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if not isinstance(self.boost_result, ScalarDustWallBoostResult):
            raise Phase1FCContractError("sealed Phase 1F-B result required")
        if not isinstance(self.clock_bridge, TimescapeWallClockBridge):
            raise Phase1FCClockError("explicit clock bridge required")
        if not isinstance(self.spatial_pullback, H1ToWallSpatialPullback):
            raise Phase1FCSpatialClosureError("explicit spatial pullback required")
        if not isinstance(self.lapse_closure, ExternalWallLapsePerturbationClosure):
            raise Phase1FCLapseClosureError("explicit perturbative lapse required")
        self.boost_result.validate_integrity()
        self.clock_bridge.validate_integrity()
        self.spatial_pullback.validate_integrity()
        self.lapse_closure.validate_integrity()
        for name in (
            "common_spacetime_id",
            "wall_congruence_id",
            "regional_wall_dust_congruence_id",
            "local_metric_scope",
        ):
            _token(getattr(self, name), name)
        if self.selected_sector is not WallNormalSector.SCALAR_LONGITUDINAL_HYPERSURFACE_NORMAL_SHEAR_FREE_LOCAL:
            raise Phase1FCContractError("unsupported wall geometry sector")
        if self.shift_gauge is not ShiftGauge.ZERO_SHIFT:
            raise Phase1FCContractError("V1 supports only explicit zero-shift gauge")
        if self.metric_signature != "(-,+,+,+)":
            raise Phase1FCContractError("ADM signature must be (-,+,+,+)")
        if self.extrinsic_curvature_sign != "K_ij=-(1/2)L_n h_ij; Theta_W=-K":
            raise Phase1FCContractError("ADM extrinsic-curvature sign changed")
        expected_classes = {
            "wall_congruence_classification": MODEL_SECTOR_RESTRICTION,
            "shift_classification": GAUGE_CHOICE,
            "vorticity_classification": DERIVED_FROM_GENERIC_GR,
            "shear_classification": MODEL_SECTOR_RESTRICTION,
            "morphology_classification": EXTERNAL_CLOSURE_INPUT,
            "boundary_classification": EXTERNAL_CLOSURE_INPUT,
        }
        for name, expected in expected_classes.items():
            if getattr(self, name) != expected:
                raise Phase1FCContractError(f"{name} must be {expected}")
        if self.local_metric_scope != "LOCAL_WALL_PATCH_NOT_GLOBAL_W09_DRESSED_METRIC":
            raise Phase1FCContractError("local wall metric scope was broadened")
        closure = self.boost_result.scenario.geometry_closure
        if self.common_spacetime_id != closure.common_spacetime_id:
            raise Phase1FCContractError("common-spacetime identity mismatch")
        if self.wall_congruence_id != closure.wall_congruence_id:
            raise Phase1FCContractError("wall-congruence identity mismatch")
        if self.regional_wall_dust_congruence_id != closure.regional_wall_dust_congruence_id:
            raise Phase1FCContractError("wall-dust congruence identity mismatch")
        if self.wall_congruence_id == self.regional_wall_dust_congruence_id:
            raise Phase1FCContractError(
                "wall-observer and wall-dust congruences must remain distinct"
            )
        if self.spatial_pullback.h1_wall_domain is not closure.wall_domain:
            raise Phase1FCSpatialClosureError("pullback must bind the sealed Phase 1F-B H1 wall domain")
        if self.clock_bridge.common_time_coordinate_id != closure.common_time_coordinate_id:
            raise Phase1FCClockError("clock and Phase 1F-B common time differ")
        if not np.array_equal(self.clock_bridge.time_grid, self.boost_result.time_grid):
            raise Phase1FCClockError("clock and boost time grids differ")
        lapse = self.lapse_closure
        if not np.array_equal(lapse.time_grid, self.boost_result.time_grid):
            raise Phase1FCLapseClosureError("lapse and boost time grids differ")
        if lapse.common_spacetime_id != self.common_spacetime_id:
            raise Phase1FCLapseClosureError("lapse common-spacetime mismatch")
        if lapse.wall_congruence_id != self.wall_congruence_id:
            raise Phase1FCLapseClosureError("lapse wall-congruence mismatch")
        if lapse.common_time_coordinate_id != self.clock_bridge.common_time_coordinate_id:
            raise Phase1FCLapseClosureError("lapse time-coordinate mismatch")
        if lapse.wall_geometry_id != self.spatial_pullback.wall_geometry_id:
            raise Phase1FCLapseClosureError("lapse wall-geometry mismatch")
        if lapse.wall_metric_id != self.spatial_pullback.wall_metric_id:
            raise Phase1FCLapseClosureError("lapse wall-metric mismatch")
        if lapse.domain_id != self.spatial_pullback.domain_id:
            raise Phase1FCLapseClosureError("lapse domain mismatch")
        if lapse.perturbative_wall_lapse.shape[1] != self.spatial_pullback.wall_size:
            raise Phase1FCLapseClosureError("lapse spatial size mismatch")
        _seal(self, self._live_state())

    def _live_state(self) -> object:
        return (
            id(self.boost_result),
            id(self.clock_bridge),
            id(self.spatial_pullback),
            id(self.lapse_closure),
            self.common_spacetime_id,
            self.wall_congruence_id,
            self.regional_wall_dust_congruence_id,
            self.selected_sector,
            self.shift_gauge,
            self.metric_signature,
            self.extrinsic_curvature_sign,
            self.wall_congruence_classification,
            self.shift_classification,
            self.vorticity_classification,
            self.shear_classification,
            self.local_metric_scope,
            self.morphology_classification,
            self.boundary_classification,
        )

    def validate_integrity(self) -> None:
        self.boost_result.validate_integrity()
        self.clock_bridge.validate_integrity()
        self.spatial_pullback.validate_integrity()
        self.lapse_closure.validate_integrity()
        _validate(self, self._live_state())


@dataclass(frozen=True, slots=True, kw_only=True)
class WallKinematicGeometryDiagnostics:
    clock_alignment_max_abs: float
    lapse_alignment_max_abs: float
    boost_clock_residual_max_abs: float
    expansion_compatibility_max_abs: float
    expansion_compatibility_normalized_linf: float
    lapse_perturbation_max_abs: float
    acceleration_max_abs: float
    clock_alignment_tolerance: float
    lapse_alignment_tolerance: float
    boost_clock_residual_tolerance: float
    expansion_compatibility_tolerance: float
    lapse_linear_regime_threshold: float
    dimensional_contract_status: str
    state_integrity_status: str

    def __post_init__(self) -> None:
        for item in fields(self):
            value = getattr(self, item.name)
            if item.name.endswith("status"):
                _token(value, item.name)
            elif not np.isfinite(float(value)) or float(value) < 0.0:
                raise Phase1FCContractError(
                    f"{item.name} must be finite and nonnegative"
                )
        if self.state_integrity_status != "VALIDATED_AT_OPERATION_TIME":
            raise Phase1FCContractError("diagnostic integrity status changed")


@dataclass(frozen=True, kw_only=True)
class WallKinematicGeometryResult:
    """Local kinematics for supplied data; physical background embedding unproved.

    Two immediate callbacks are not an exhaustive physical closure inventory;
    see REMAINING_SCIENTIFIC_CLOSURES and the 1F-C-R successor record.
    Ranks 4/5/+1 count differential field species, not free admissible initial
    functions after constraints and prescribed histories.
    """

    time_grid: FloatArray
    background_wall_proper_time_rate: FloatArray
    adm_lapse_first_order: FloatArray
    perturbative_wall_lapse: FloatArray
    wall_acceleration_orthonormal: FloatArray
    wall_acceleration_coordinate_covector: FloatArray
    wall_acceleration_coordinate_contravariant: FloatArray
    wall_expansion_perturbation: FloatArray
    wall_laplacian_of_boost_potential: FloatArray
    expansion_compatibility_residual: FloatArray
    boost_clock_residual: FloatArray
    diagnostics: WallKinematicGeometryDiagnostics
    scenario: ClockAnchoredWallGeometryScenario = field(repr=False, compare=False)
    numerics: Phase1FCNumerics = field(repr=False, compare=False)
    realization_id: str
    acceleration_classification: str
    expansion_classification: str
    vorticity_status: str
    shear_status: str
    common_spacetime_status: str
    global_dressed_spacetime_status: str
    wall_geometry_driver_status: str
    frozen_phase1f_b_rank: int
    driver_only_rank: int
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if not isinstance(self.scenario, ClockAnchoredWallGeometryScenario):
            raise Phase1FCContractError("validated Phase 1F-C scenario required")
        if not isinstance(self.numerics, Phase1FCNumerics):
            raise Phase1FCContractError("validated Phase 1F-C numerics required")
        self.scenario.validate_integrity()
        self.numerics.validate_integrity()
        if not isinstance(self.diagnostics, WallKinematicGeometryDiagnostics):
            raise Phase1FCContractError("wall geometry diagnostics required")
        for name in (
            "time_grid",
            "background_wall_proper_time_rate",
            "adm_lapse_first_order",
            "perturbative_wall_lapse",
            "wall_acceleration_orthonormal",
            "wall_acceleration_coordinate_covector",
            "wall_acceleration_coordinate_contravariant",
            "wall_expansion_perturbation",
            "wall_laplacian_of_boost_potential",
            "expansion_compatibility_residual",
            "boost_clock_residual",
        ):
            object.__setattr__(self, name, _readonly_float(getattr(self, name), name))
        if self.realization_id != REALIZATION_ID:
            raise Phase1FCContractError("Phase 1F-C realization identity changed")
        if self.acceleration_classification != DERIVED_FROM_GENERIC_GR:
            raise Phase1FCContractError("acceleration evidence classification changed")
        if self.expansion_classification != DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION:
            raise Phase1FCContractError("expansion evidence classification changed")
        if self.vorticity_status != WALL_VORTICITY or self.shear_status != WALL_SHEAR:
            raise Phase1FCContractError("selected wall-sector status changed")
        if self.common_spacetime_status != COMMON_PERTURBED_4D_SPACETIME:
            raise Phase1FCContractError("local spacetime status changed")
        if self.global_dressed_spacetime_status != GLOBAL_PERTURBED_DRESSED_SPACETIME:
            raise Phase1FCContractError("global dressed status changed")
        if self.wall_geometry_driver_status != WALL_GEOMETRY_DRIVER:
            raise Phase1FCContractError("geometry-driver ceiling changed")
        if self.frozen_phase1f_b_rank != FROZEN_PHASE_1F_B_DIFFERENTIAL_STATE_RANK:
            raise Phase1FCContractError("frozen Phase 1F-B rank changed")
        if self.driver_only_rank != DRIVER_ONLY_DIFFERENTIAL_STATE_RANK:
            raise Phase1FCContractError("driver-only rank changed")
        nt = self.scenario.boost_result.time_grid.size
        wall_size = self.scenario.spatial_pullback.wall_size
        if self.time_grid.shape != (nt,) or not np.array_equal(
            self.time_grid, self.scenario.boost_result.time_grid
        ):
            raise Phase1FCContractError("result time grid mismatch")
        scalar_shape = (nt, wall_size)
        for name in (
            "adm_lapse_first_order",
            "perturbative_wall_lapse",
            "wall_expansion_perturbation",
            "wall_laplacian_of_boost_potential",
            "expansion_compatibility_residual",
            "boost_clock_residual",
        ):
            if getattr(self, name).shape != scalar_shape:
                raise Phase1FCContractError(f"{name} shape mismatch")
        if self.background_wall_proper_time_rate.shape != (nt,):
            raise Phase1FCContractError("background wall clock shape mismatch")
        if any(getattr(self, name).shape != (
            nt,
            wall_size,
            self.scenario.spatial_pullback.spatial_dimension,
        ) for name in self.acceleration_component_representations):
            raise Phase1FCContractError("wall acceleration shape mismatch")
        tolerance_pairs = (
            (
                self.diagnostics.clock_alignment_tolerance,
                self.numerics.clock_alignment_tolerance,
            ),
            (
                self.diagnostics.lapse_alignment_tolerance,
                self.numerics.lapse_alignment_tolerance,
            ),
            (
                self.diagnostics.boost_clock_residual_tolerance,
                self.numerics.boost_clock_residual_tolerance,
            ),
            (
                self.diagnostics.expansion_compatibility_tolerance,
                self.numerics.expansion_compatibility_tolerance,
            ),
            (
                self.diagnostics.lapse_linear_regime_threshold,
                self.numerics.lapse_linear_regime_threshold,
            ),
        )
        if any(left != right for left, right in tolerance_pairs):
            raise Phase1FCContractError("diagnostic/numerics tolerance mismatch")
        _seal(self, self._live_state())

    @property
    def acceleration_component_representations(self) -> Mapping[str, ComponentRepresentation]:
        """Each public acceleration array's exact basis and index semantics."""
        return MappingProxyType({
            "wall_acceleration_orthonormal": ComponentRepresentation.PHYSICAL_ORTHONORMAL,
            "wall_acceleration_coordinate_covector": ComponentRepresentation.COORDINATE_COVECTOR,
            "wall_acceleration_coordinate_contravariant": ComponentRepresentation.COORDINATE_CONTRAVARIANT,
        })

    @property
    def acceleration_component_realization_classification(self) -> str:
        return DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION

    def _live_state(self) -> object:
        return tuple(
            id(getattr(self, item.name))
            if item.name == "scenario"
            else getattr(self, item.name)
            for item in fields(self)
            if not item.name.startswith("_")
        )

    def validate_integrity(self) -> None:
        self.scenario.validate_integrity()
        self.numerics.validate_integrity()
        _validate(self, self._live_state())


@dataclass(frozen=True, kw_only=True)
class ScalarMetricTraceInitialData:
    """Initial representative and caller-declared reconstruction validity.

    ``linear_regime_limit`` bounds ``abs(C_W)`` at every accepted output.
    Like the existing lapse policy, it must be positive and below one, and
    must be chosen small enough for the caller's first-order error budget.
    It is a numerical/model-validity criterion, not a Timescape prediction.
    Positivity of ``1+2C_W`` (the metric ansatz based on BMR Eq. (2.5)) is
    independently necessary and is enforced with a strict zero threshold.
    """

    initial_metric_trace: FloatArray
    linear_regime_limit: float
    initial_time: float
    background_split_policy: MetricTraceBackgroundSplit
    spatial_measure_id: str
    frame_id: str
    provenance: str
    scientific_classification: str
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if not isinstance(self.background_split_policy, MetricTraceBackgroundSplit):
            raise Phase1FCMetricReconstructionError("explicit background split required")
        if self.scientific_classification != EXTERNAL_CLOSURE_INPUT:
            raise Phase1FCMetricReconstructionError("C_W initial data are external")
        for name in ("spatial_measure_id", "frame_id", "provenance"):
            _token(getattr(self, name), name)
        if not np.isfinite(self.initial_time):
            raise Phase1FCMetricReconstructionError("initial_time must be finite")
        object.__setattr__(
            self,
            "initial_metric_trace",
            _readonly_float(self.initial_metric_trace, "initial_metric_trace").reshape(-1),
        )
        if not np.isfinite(self.linear_regime_limit) or not 0.0 < self.linear_regime_limit < 1.0:
            raise Phase1FCMetricReconstructionError("explicit C_W linear-regime limit must be finite and between zero and one")
        self.validate_field(self.initial_metric_trace)
        _seal(self, self._live_state())

    def validate_field(self, values: FloatArray) -> None:
        """Necessary positive-metric and declared first-order-domain gates."""
        if not np.all(np.isfinite(values)):
            raise Phase1FCMetricReconstructionError("C_W must be finite")
        if np.any(1.0 + 2.0 * values <= 0.0):
            raise Phase1FCMetricReconstructionError("C_W violates positive metric: 1+2C_W > 0 required")
        if np.any(np.abs(values) > self.linear_regime_limit):
            raise Phase1FCMetricReconstructionError("C_W exits the declared linear-regime limit")

    def _live_state(self) -> object:
        return (
            self.initial_metric_trace,
            self.linear_regime_limit,
            self.initial_time,
            self.background_split_policy,
            self.spatial_measure_id,
            self.frame_id,
            self.provenance,
            self.scientific_classification,
        )

    def validate_integrity(self) -> None:
        _validate(self, self._live_state())


@dataclass(frozen=True, slots=True, kw_only=True)
class ScalarMetricTraceDiagnostics:
    initial_weighted_mean_residual: float
    reconstructed_weighted_mean_max_abs: float
    evolution_residual_max_abs: float
    mean_tolerance: float
    evolution_tolerance: float
    integration_method: str
    linear_regime_limit: float
    metric_trace_max_abs: float
    minimum_metric_factor: float

    def __post_init__(self) -> None:
        for name in (
            "initial_weighted_mean_residual",
            "reconstructed_weighted_mean_max_abs",
            "evolution_residual_max_abs",
            "linear_regime_limit",
            "metric_trace_max_abs",
            "minimum_metric_factor",
        ):
            if not np.isfinite(float(getattr(self, name))):
                raise Phase1FCMetricReconstructionError(
                    f"{name} must be finite"
                )
        _positive(self.mean_tolerance, "mean_tolerance")
        _positive(self.evolution_tolerance, "evolution_tolerance")
        if not 0.0 < self.linear_regime_limit < 1.0:
            raise Phase1FCMetricReconstructionError("diagnostic linear-regime limit invalid")
        if not 0.0 <= self.metric_trace_max_abs <= self.linear_regime_limit or self.minimum_metric_factor <= 0.0:
            raise Phase1FCMetricReconstructionError("diagnostic metric validity domain failed")
        if self.integration_method != "EXPLICIT_TRAPEZOIDAL_COMMON_TIME_GRID":
            raise Phase1FCMetricReconstructionError("diagnostic integrator mismatch")


@dataclass(frozen=True, kw_only=True)
class ScalarMetricTraceResult:
    time_grid: FloatArray
    metric_trace_perturbation: FloatArray
    metric_trace_time_derivative: FloatArray
    diagnostics: ScalarMetricTraceDiagnostics
    geometry: WallKinematicGeometryResult = field(repr=False, compare=False)
    initial_data: ScalarMetricTraceInitialData = field(repr=False, compare=False)
    differential_rank_contribution: int
    augmented_runtime_rank: int
    scientific_classification: str
    global_dressed_spacetime_status: str
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if not isinstance(self.geometry, WallKinematicGeometryResult):
            raise Phase1FCMetricReconstructionError("validated wall geometry required")
        if not isinstance(self.initial_data, ScalarMetricTraceInitialData):
            raise Phase1FCMetricReconstructionError("validated C_W initial data required")
        self.geometry.validate_integrity()
        self.initial_data.validate_integrity()
        if not isinstance(self.diagnostics, ScalarMetricTraceDiagnostics):
            raise Phase1FCMetricReconstructionError("metric trace diagnostics required")
        for name in (
            "time_grid",
            "metric_trace_perturbation",
            "metric_trace_time_derivative",
        ):
            object.__setattr__(self, name, _readonly_float(getattr(self, name), name))
        if self.differential_rank_contribution != OPTIONAL_METRIC_RECONSTRUCTION_DIFFERENTIAL_RANK:
            raise Phase1FCMetricReconstructionError("optional rank contribution changed")
        if self.augmented_runtime_rank != AUGMENTED_FULL_METRIC_RUNTIME_RANK:
            raise Phase1FCMetricReconstructionError("augmented runtime rank changed")
        if self.scientific_classification != DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION:
            raise Phase1FCMetricReconstructionError("metric reconstruction classification changed")
        if self.global_dressed_spacetime_status != GLOBAL_PERTURBED_DRESSED_SPACETIME:
            raise Phase1FCMetricReconstructionError("local trace promoted to global metric")
        nt = self.geometry.time_grid.size
        wall_size = self.geometry.scenario.spatial_pullback.wall_size
        if self.time_grid.shape != (nt,) or not np.array_equal(
            self.time_grid, self.geometry.time_grid
        ):
            raise Phase1FCMetricReconstructionError("metric trace time grid mismatch")
        if self.metric_trace_perturbation.shape != (nt, wall_size):
            raise Phase1FCMetricReconstructionError("metric trace field shape mismatch")
        if self.metric_trace_time_derivative.shape != (nt, wall_size):
            raise Phase1FCMetricReconstructionError("metric trace derivative shape mismatch")
        self.initial_data.validate_field(self.metric_trace_perturbation)
        if self.diagnostics.linear_regime_limit != self.initial_data.linear_regime_limit:
            raise Phase1FCMetricReconstructionError("C_W diagnostic validity-limit mismatch")
        _seal(self, self._live_state())

    def _live_state(self) -> object:
        return (
            self.time_grid,
            self.metric_trace_perturbation,
            self.metric_trace_time_derivative,
            self.diagnostics,
            id(self.geometry),
            id(self.initial_data),
            self.differential_rank_contribution,
            self.augmented_runtime_rank,
            self.scientific_classification,
            self.global_dressed_spacetime_status,
        )

    def validate_integrity(self) -> None:
        self.geometry.validate_integrity()
        self.initial_data.validate_integrity()
        _validate(self, self._live_state())
