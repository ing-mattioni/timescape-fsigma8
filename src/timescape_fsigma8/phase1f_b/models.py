"""Immutable scientific contracts for the conditional Phase 1F-B branch.

The frozen CGI expansion definition is from Eqs. (2.2), (2.20)--(2.24) of
Galoppo & Mourier, arXiv:2511.17160v2.  The first-order frame transformation
uses the observer-boost conventions audited against Eqs. (14)--(16) of
Bruni, Dunsby & Ellis, ApJ 395 (1992) 34 and Eqs. (14), (15), (27) of
Dunsby, Bruni & Ellis, ApJ 395 (1992) 54.  The common-spacetime wall closure
and scalar-normal restrictions are the explicitly human-approved Phase 1F-B
model extension; they are not predicted by Timescape.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from enum import Enum

import numpy as np
from numpy.typing import ArrayLike, NDArray

from timescape_fsigma8.phase1f_a import (
    EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE,
    REGIONAL_METRIC_MEAN_ZERO,
    Phase1FANumerics,
    RegionalDomainSpec,
    RegionalExpansionReconstruction,
    RegionalZeroModeClosure,
)
from timescape_fsigma8.phase1f_a.models import canonical_state


FloatArray = NDArray[np.float64]

REALIZATION_ID = (
    "H1-1F-B-COMMON-SPACETIME-SCALAR-NORMAL-BOOST-DYNAMICS-V1"
)
SCIENTIFIC_REALIZATION_READINESS = "IMPLEMENTED_CONDITIONALLY"
PHASE_1F_B_SCIENTIFIC_VERDICT = (
    "PARTIAL_CLOSURE_NEW_GEOMETRIC_DYNAMICS_REQUIRED"
)
FROZEN_DIFFERENTIAL_STATE_RANK = 4
SELECTED_SCALAR_REALIZATION_DIFFERENTIAL_STATE_RANK = 5

EXTERNAL_GEOMETRIC_CLOSURE = "EXTERNAL_GEOMETRIC_CLOSURE"
SYNTHETIC_VALIDATION_ONLY = "SYNTHETIC_VALIDATION_ONLY"
MATHEMATICAL_OPERATOR_FIXTURE_ONLY = "MATHEMATICAL_OPERATOR_FIXTURE_ONLY"
CONDITIONAL_SCALAR_DUST_TO_WALL_BOOST = (
    "CONDITIONAL_SCALAR_LONGITUDINAL_REGIONAL_DUST_VELOCITY_RELATIVE_TO_"
    "EXPLICIT_WALL_OBSERVER_CONGRUENCE"
)
TRANSVERSE_SECTOR_EXCLUDED = (
    "EXCLUDED_BY_EXPLICIT_SCALAR_MODEL_RESTRICTION"
)
TRANSVERSE_ZERO_NOT_GRANTED = "NOT_GRANTED"
HARMONIC_VECTOR_SECTOR_EXCLUDED = (
    "EXCLUDED_BY_EXPLICIT_SCALAR_MODEL_RESTRICTION"
)
HARMONIC_VECTOR_ZERO_NOT_GRANTED = "NOT_GRANTED"
WALL_BACKGROUND_SHEAR_EXCLUDED = (
    "EXCLUDED_BY_EXPLICIT_SELECTED_GEOMETRIC_SECTOR"
)
WALL_SHEAR_ZERO_NOT_GRANTED = "NOT_GRANTED"
BOOST_SPECIFIC_BOUNDARY_MODEL = "EXPLICIT_EXTERNAL_BOOST_BOUNDARY_CLOSURE"
EXPLICIT_EXTERNAL_NO_PENETRATION_CLOSURE = (
    "EXPLICIT_EXTERNAL_NO_PENETRATION_CLOSURE"
)
BOOST_BOUNDARY_RUNTIME_ENFORCEMENT = "FAIL_CLOSED"
PHYSICAL_INTERFACE_NOT_GRANTED = "NOT_GRANTED"
PROPAGATION_CONSTRUCTION_DIAGNOSTIC = (
    "CONSTRUCTION_INVARIANT_WITH_TIME_DISCRETIZATION_ERROR"
)
EXPANSION_COMPATIBILITY_EVIDENCE = (
    "INDEPENDENT_SCIENTIFIC_COMPATIBILITY_GATE"
)
TIME_INTEGRATOR_CONVERGENCE_CLASSIFICATION = (
    "SECOND_ORDER_NUMERICAL_SELF_CONVERGENCE_OF_THE_IMPLEMENTED_TIME_INTEGRATOR"
)
WALL_PROPER_TIME_RATE_ROLE = "PROVENANCE_ONLY_NON_DYNAMICAL_METADATA"
H1_DENSITY_TRANSMISSION_BC_TO_BOOST_BC = "FORBIDDEN_INHERITANCE"
PERTURBATIVE_WALL_LAPSE_POTENTIAL = "PERTURBATIVE_WALL_LAPSE_POTENTIAL"
COMMON_TIME_GRID_EVALUATION_ONLY = "COMMON_TIME_GRID_EVALUATION_ONLY"
PIECEWISE_LINEAR_NO_EXTRAPOLATION = "PIECEWISE_LINEAR_NO_EXTRAPOLATION"
MEAN_ZERO_WALL_METRIC = "MEAN_ZERO_WALL_METRIC"
SINGLE_WALL_CONSTANT_REMOVED = "SINGLE_WALL_CONSTANT_REMOVED"
WALL_SOURCE_MEAN_ZERO = "WALL_SOURCE_MEAN_ZERO"
BOOST_WALL_INTERIOR_NO_FLUX_PERIODIC_TANGENTIAL = (
    "BOOST_WALL_INTERIOR_NO_FLUX_PERIODIC_TANGENTIAL"
)


class Phase1FBContractError(ValueError):
    """A required Phase 1F-B scientific closure or invariant failed."""


class Phase1FBGeometryClosureError(Phase1FBContractError):
    """The external common-spacetime/wall geometry closure is invalid."""


class Phase1FBKernelCompatibilityError(Phase1FBContractError):
    """A scalar source or representative violates the declared kernel policy."""


class Phase1FBCompatibilityError(Phase1FBContractError):
    """The expansion-difference constraint failed its explicit tolerance."""


class Phase1FBPropagationError(Phase1FBContractError):
    """The propagation construction/time-discretisation diagnostic failed."""


class Phase1FBBoundaryCompatibilityError(Phase1FBContractError):
    """The explicit external no-penetration boost closure failed."""


class Phase1FBLinearRegimeError(Phase1FBContractError):
    """The conditional relative velocity lies outside the declared linear gate."""


class Phase1FBStateIntegrityError(Phase1FBContractError):
    """Validated Phase 1F-B state changed after construction."""


class BoostGeometryProvenance(Enum):
    EXTERNAL_GEOMETRIC_CLOSURE = EXTERNAL_GEOMETRIC_CLOSURE
    SYNTHETIC_VALIDATION_ONLY = SYNTHETIC_VALIDATION_ONLY


class BoostInitializationMode(Enum):
    SUPPLIED_INITIAL_BOOST = "SUPPLIED_INITIAL_BOOST"
    EXPANSION_MATCHED_INITIAL_BOOST = "EXPANSION_MATCHED_INITIAL_BOOST"


class LapseKernelMode(Enum):
    REQUIRE_MEAN_ZERO = "REQUIRE_MEAN_ZERO"
    EXPLICIT_Q0_PROJECTION = "EXPLICIT_Q0_PROJECTION"


class ScalarBoostSector(Enum):
    SCALAR_LONGITUDINAL_HYPERSURFACE_ORTHOGONAL = (
        "SCALAR_LONGITUDINAL_HYPERSURFACE_ORTHOGONAL"
    )


class WallBackgroundGeometrySector(Enum):
    SHEAR_FREE_QUASI_FLRW_COMMON_SPACETIME = (
        "SHEAR_FREE_QUASI_FLRW_COMMON_SPACETIME"
    )


class BoostBoundaryKind(Enum):
    WALL_INTERIOR_NO_FLUX_PERIODIC_TANGENTIAL = (
        BOOST_WALL_INTERIOR_NO_FLUX_PERIODIC_TANGENTIAL
    )


def _readonly_float(values: ArrayLike, name: str) -> FloatArray:
    result = np.array(values, dtype=np.float64, copy=True)
    if not np.all(np.isfinite(result)):
        raise Phase1FBContractError(f"{name} must contain only finite values")
    result.setflags(write=False)
    return result


def _require_token(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise Phase1FBContractError(f"{name} must be an explicit nonempty token")


def _require_positive(value: float, name: str) -> None:
    if not np.isfinite(value) or value <= 0.0:
        raise Phase1FBContractError(f"{name} must be finite and positive")


def _seal(instance: object, state: object) -> None:
    object.__setattr__(instance, "_integrity_token", canonical_state(state))


def _validate(instance: object, state: object) -> None:
    if getattr(instance, "_integrity_token", None) != canonical_state(state):
        raise Phase1FBStateIntegrityError(
            "live Phase 1F-B scientific state differs from validated construction"
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class ScalarDustWallBoostNumerics:
    """Explicit numerical/scientific gates; no field has a hidden default."""

    expansion_compatibility_tolerance: float
    propagation_residual_tolerance: float
    potential_mean_tolerance: float
    lapse_mean_tolerance: float
    scale_factor_rate_tolerance: float
    off_domain_tolerance: float
    boundary_normal_velocity_tolerance: float
    boundary_normal_acceleration_tolerance: float
    boundary_normal_velocity_tolerance_units: str
    boundary_normal_acceleration_tolerance_units: str
    linear_velocity_ratio_threshold: float
    speed_of_light: float
    speed_of_light_units: str
    residual_norm_floor: float
    integration_method: str
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for item in fields(self):
            if item.name in {
                "integration_method",
                "speed_of_light_units",
                "boundary_normal_velocity_tolerance_units",
                "boundary_normal_acceleration_tolerance_units",
                "_integrity_token",
            }:
                continue
            _require_positive(float(getattr(self, item.name)), item.name)
        if self.speed_of_light_units != "REFERENCE_LENGTH_PER_COMMON_TIME":
            raise Phase1FBContractError("speed_of_light_units mismatch")
        if (
            self.boundary_normal_velocity_tolerance_units
            != "REFERENCE_LENGTH_PER_COMMON_TIME"
        ):
            raise Phase1FBContractError(
                "boundary normal-velocity tolerance units mismatch"
            )
        if (
            self.boundary_normal_acceleration_tolerance_units
            != "INVERSE_COMMON_TIME"
        ):
            raise Phase1FBContractError(
                "boundary normal-acceleration tolerance units mismatch"
            )
        if self.integration_method != "EXPLICIT_TRAPEZOIDAL_COMMON_TIME_GRID":
            raise Phase1FBContractError(
                "V1 supports only EXPLICIT_TRAPEZOIDAL_COMMON_TIME_GRID"
            )
        _seal(self, self._live_state())

    def _live_state(self) -> object:
        return tuple(
            getattr(self, item.name)
            for item in fields(self)
            if item.name != "_integrity_token"
        )

    def validate_integrity(self) -> None:
        _validate(self, self._live_state())


@dataclass(frozen=True, slots=True, kw_only=True)
class BoostBoundaryKernelPolicy:
    """External wall-interior no-penetration and constant-kernel contract.

    The numerical no-flux realization reuses the Phase 1F-A regional matrix,
    but this record is a new explicit boost modeling choice.  It is never
    inherited from the H1 density/transmission interface and does not make
    that mathematical interface a physical material wall.  The spatial
    derivative convention follows BDE Eq. (74); ``D_n psi=0`` is the explicit
    human-approved Phase 1F-B boundary closure, not a Timescape prediction.
    """

    domain_id: str
    boundary_kind: BoostBoundaryKind
    nullspace_handling: str
    compatibility_condition: str
    provenance: str
    classification: str
    physical_boundary_condition: str
    derived_from_timescape: bool
    inherited_from_h1_density_transmission: bool
    physical_interface_claim: str
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        _require_token(self.domain_id, "domain_id")
        _require_token(self.provenance, "provenance")
        if not isinstance(self.boundary_kind, BoostBoundaryKind):
            raise Phase1FBContractError("boundary_kind must be a BoostBoundaryKind")
        if self.domain_id != "wall":
            raise Phase1FBContractError("V1 boost boundary domain must be wall")
        if self.nullspace_handling != SINGLE_WALL_CONSTANT_REMOVED:
            raise Phase1FBContractError("V1 removes exactly one wall constant")
        if self.compatibility_condition != WALL_SOURCE_MEAN_ZERO:
            raise Phase1FBContractError("V1 requires wall source mean zero")
        if self.classification != BOOST_SPECIFIC_BOUNDARY_MODEL:
            raise Phase1FBContractError("boost boundary must be explicitly classified")
        if (
            self.physical_boundary_condition
            != EXPLICIT_EXTERNAL_NO_PENETRATION_CLOSURE
        ):
            raise Phase1FBContractError(
                "boost boundary must declare the external no-penetration closure"
            )
        if not isinstance(self.derived_from_timescape, bool):
            raise Phase1FBContractError(
                "Timescape boundary-derivation status must be an explicit boolean"
            )
        if self.derived_from_timescape:
            raise Phase1FBContractError(
                "boost no-penetration boundary is not derived from Timescape"
            )
        if not isinstance(self.inherited_from_h1_density_transmission, bool):
            raise Phase1FBContractError(
                "boundary inheritance status must be an explicit boolean"
            )
        if self.inherited_from_h1_density_transmission:
            raise Phase1FBContractError(
                "H1 density/transmission boundary inheritance is forbidden"
            )
        if self.physical_interface_claim != PHYSICAL_INTERFACE_NOT_GRANTED:
            raise Phase1FBContractError(
                "explicit boost boundary does not grant a physical interface claim"
            )
        _seal(self, self._live_state())

    def _live_state(self) -> object:
        return (
            self.domain_id,
            self.boundary_kind,
            self.nullspace_handling,
            self.compatibility_condition,
            self.provenance,
            self.classification,
            self.physical_boundary_condition,
            self.derived_from_timescape,
            self.inherited_from_h1_density_transmission,
            self.physical_interface_claim,
        )

    def validate_integrity(self) -> None:
        _validate(self, self._live_state())


@dataclass(frozen=True, kw_only=True)
class CommonSpacetimeWallGeometryClosure:
    """External common-spacetime geometry driving the scalar-normal boost.

    ``A_W,a=D_a nu_W`` is the normal-congruence lapse identity used with the
    acceleration frame law audited from BDE Eqs. (14)--(16) and dust
    geodesicity from GM Eq. (2.9).  The local lapse perturbation is external;
    the background Timescape lapse ``gamma_w=dt/dtau_w`` ([W09] Eq. (B7))
    cannot populate this record.
    """

    wall_domain: RegionalDomainSpec
    common_spacetime_id: str
    wall_congruence_id: str
    regional_wall_dust_congruence_id: str
    h1_wall_embedding_id: str
    common_time_coordinate_id: str
    wall_proper_time_mapping_id: str
    spatial_geometry_operator_id: str
    dust_expansion_background_identity: str
    domain_id: str
    time_grid: FloatArray
    wall_scale_factor: FloatArray
    wall_hubble_rate: FloatArray
    wall_proper_time_rate: FloatArray
    wall_proper_time_rate_role: str
    wall_expansion_perturbation: FloatArray
    wall_lapse_perturbation: FloatArray
    lapse_driver_kind: str
    common_time_units: str
    wall_expansion_units: str
    wall_hubble_units: str
    wall_scale_factor_units: str
    wall_lapse_units: str
    unit_system: str
    interpolation_policy: str
    provenance: BoostGeometryProvenance
    selected_background_geometry_sector: WallBackgroundGeometrySector
    scalar_hypersurface_orthogonal: bool
    vorticity_dust_zero: bool
    vorticity_wall_zero: bool
    wall_background_shear_free: bool
    normalization_kernel_identity: str
    scientific_classification: str
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if not isinstance(self.wall_domain, RegionalDomainSpec):
            raise Phase1FBGeometryClosureError("validated wall RegionalDomainSpec required")
        self.wall_domain.validate_integrity()
        if self.wall_domain.region != "wall":
            raise Phase1FBGeometryClosureError("common-spacetime closure requires wall domain")
        for name in (
            "common_spacetime_id",
            "wall_congruence_id",
            "regional_wall_dust_congruence_id",
            "h1_wall_embedding_id",
            "common_time_coordinate_id",
            "wall_proper_time_mapping_id",
            "spatial_geometry_operator_id",
            "dust_expansion_background_identity",
            "domain_id",
            "common_time_units",
            "wall_expansion_units",
            "wall_hubble_units",
            "wall_scale_factor_units",
            "wall_lapse_units",
            "unit_system",
            "wall_proper_time_rate_role",
            "normalization_kernel_identity",
            "scientific_classification",
        ):
            _require_token(getattr(self, name), name)
        if not isinstance(self.provenance, BoostGeometryProvenance):
            raise Phase1FBGeometryClosureError(
                "provenance must be explicit external or synthetic validation geometry"
            )
        if self.scientific_classification != self.provenance.value:
            raise Phase1FBGeometryClosureError(
                "geometry scientific classification must retain external provenance"
            )
        if self.domain_id != "wall":
            raise Phase1FBGeometryClosureError("domain_id must be wall")
        operator = self.wall_domain.operator
        if self.h1_wall_embedding_id != operator.morphology.wall_pullback_id:
            raise Phase1FBGeometryClosureError("H1 wall embedding identity mismatch")
        expected_spatial = self.wall_domain.geometry.normalization.normalization_id
        if self.spatial_geometry_operator_id != expected_spatial:
            raise Phase1FBGeometryClosureError("wall spatial operator identity mismatch")
        if self.lapse_driver_kind != PERTURBATIVE_WALL_LAPSE_POTENTIAL:
            raise Phase1FBGeometryClosureError(
                "background gamma_w cannot substitute for perturbative wall lapse"
            )
        if self.interpolation_policy != PIECEWISE_LINEAR_NO_EXTRAPOLATION:
            raise Phase1FBGeometryClosureError(
                "V1 requires explicit piecewise-linear no-extrapolation policy"
            )
        if self.wall_proper_time_rate_role != WALL_PROPER_TIME_RATE_ROLE:
            raise Phase1FBGeometryClosureError(
                "wall_proper_time_rate is provenance-only non-dynamical metadata"
            )
        if not isinstance(
            self.selected_background_geometry_sector,
            WallBackgroundGeometrySector,
        ):
            raise Phase1FBGeometryClosureError(
                "the explicit shear-free quasi-FLRW background sector is required"
            )
        restrictions = (
            self.scalar_hypersurface_orthogonal,
            self.vorticity_dust_zero,
            self.vorticity_wall_zero,
            self.wall_background_shear_free,
        )
        if not all(isinstance(value, bool) for value in restrictions):
            raise Phase1FBGeometryClosureError(
                "scalar/vorticity restrictions must be explicit booleans"
            )
        if not all(
            (
                self.scalar_hypersurface_orthogonal,
                self.vorticity_dust_zero,
                self.vorticity_wall_zero,
                self.wall_background_shear_free,
            )
        ):
            raise Phase1FBGeometryClosureError(
                "V1 requires the explicit scalar, vorticity-free, shear-free sector"
            )
        arrays = {
            "time_grid": _readonly_float(self.time_grid, "time_grid"),
            "wall_scale_factor": _readonly_float(
                self.wall_scale_factor, "wall_scale_factor"
            ),
            "wall_hubble_rate": _readonly_float(
                self.wall_hubble_rate, "wall_hubble_rate"
            ),
            "wall_proper_time_rate": _readonly_float(
                self.wall_proper_time_rate, "wall_proper_time_rate"
            ),
            "wall_expansion_perturbation": _readonly_float(
                self.wall_expansion_perturbation, "wall_expansion_perturbation"
            ),
            "wall_lapse_perturbation": _readonly_float(
                self.wall_lapse_perturbation, "wall_lapse_perturbation"
            ),
        }
        time = arrays["time_grid"]
        if time.ndim != 1 or time.size < 2 or np.any(np.diff(time) <= 0.0):
            raise Phase1FBGeometryClosureError(
                "time_grid must be a strictly increasing one-dimensional grid"
            )
        nt = time.size
        size = operator.size
        for name in ("wall_scale_factor", "wall_hubble_rate", "wall_proper_time_rate"):
            if arrays[name].shape != (nt,):
                raise Phase1FBGeometryClosureError(f"{name} must match time_grid")
        for name in ("wall_expansion_perturbation", "wall_lapse_perturbation"):
            if arrays[name].shape != (nt, size):
                raise Phase1FBGeometryClosureError(
                    f"{name} must have shape (time, complete carrier grid)"
                )
        if np.any(arrays["wall_scale_factor"] <= 0.0):
            raise Phase1FBGeometryClosureError("wall_scale_factor must be positive")
        if np.any(arrays["wall_proper_time_rate"] <= 0.0):
            raise Phase1FBGeometryClosureError("wall_proper_time_rate must be positive")
        if self.common_time_units != "COMMON_TIME":
            raise Phase1FBGeometryClosureError("common time units must be explicit")
        if self.wall_expansion_units != "INVERSE_COMMON_TIME":
            raise Phase1FBGeometryClosureError("wall expansion units mismatch")
        if self.wall_hubble_units != "INVERSE_COMMON_TIME":
            raise Phase1FBGeometryClosureError("wall Hubble units mismatch")
        if self.wall_scale_factor_units != "DIMENSIONLESS":
            raise Phase1FBGeometryClosureError("wall scale factor units mismatch")
        if self.wall_lapse_units != "DIMENSIONLESS_PERTURBATION":
            raise Phase1FBGeometryClosureError("wall lapse perturbation units mismatch")
        if self.unit_system != "GEOMETRIZED_C_EQUALS_ONE":
            raise Phase1FBGeometryClosureError("V1 requires explicit geometrized units")
        for name, values in arrays.items():
            object.__setattr__(self, name, values)
        _seal(self, self._live_state())

    def _live_state(self) -> object:
        return (
            id(self.wall_domain),
            self.common_spacetime_id,
            self.wall_congruence_id,
            self.regional_wall_dust_congruence_id,
            self.h1_wall_embedding_id,
            self.common_time_coordinate_id,
            self.wall_proper_time_mapping_id,
            self.spatial_geometry_operator_id,
            self.dust_expansion_background_identity,
            self.domain_id,
            self.time_grid,
            self.wall_scale_factor,
            self.wall_hubble_rate,
            self.wall_proper_time_rate,
            self.wall_proper_time_rate_role,
            self.wall_expansion_perturbation,
            self.wall_lapse_perturbation,
            self.lapse_driver_kind,
            self.common_time_units,
            self.wall_expansion_units,
            self.wall_hubble_units,
            self.wall_scale_factor_units,
            self.wall_lapse_units,
            self.unit_system,
            self.interpolation_policy,
            self.provenance,
            self.selected_background_geometry_sector,
            self.scalar_hypersurface_orthogonal,
            self.vorticity_dust_zero,
            self.vorticity_wall_zero,
            self.wall_background_shear_free,
            self.normalization_kernel_identity,
            self.scientific_classification,
        )

    def validate_integrity(self) -> None:
        self.wall_domain.validate_integrity()
        _validate(self, self._live_state())


@dataclass(frozen=True, kw_only=True)
class ScalarDustWallBoostScenario:
    """All scientific choices for one conditionally unique scalar problem."""

    geometry_closure: CommonSpacetimeWallGeometryClosure
    dust_expansion_history: tuple[RegionalExpansionReconstruction, ...]
    dust_expansion_time_grid: FloatArray
    dust_expansion_time_coordinate_id: str
    regional_elliptic_numerics: Phase1FANumerics
    initialization_mode: BoostInitializationMode
    initial_scalar_potential: FloatArray | None
    initial_potential_provenance: str
    initial_potential_units: str
    boundary_policy: BoostBoundaryKernelPolicy
    zero_mode_closure: RegionalZeroModeClosure
    lapse_kernel_mode: LapseKernelMode
    requested_sector: ScalarBoostSector
    scientific_classification: str
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if not isinstance(self.geometry_closure, CommonSpacetimeWallGeometryClosure):
            raise Phase1FBContractError("common-spacetime geometry closure is required")
        self.geometry_closure.validate_integrity()
        _require_token(
            self.dust_expansion_time_coordinate_id,
            "dust_expansion_time_coordinate_id",
        )
        expansion_time = _readonly_float(
            self.dust_expansion_time_grid, "dust_expansion_time_grid"
        )
        if not np.array_equal(expansion_time, self.geometry_closure.time_grid):
            raise Phase1FBContractError(
                "dust expansion and common-spacetime time grids must match exactly"
            )
        if (
            self.dust_expansion_time_coordinate_id
            != self.geometry_closure.common_time_coordinate_id
        ):
            raise Phase1FBContractError(
                "dust expansion and common-spacetime time-coordinate identities mismatch"
            )
        if not isinstance(self.initialization_mode, BoostInitializationMode):
            raise Phase1FBContractError("initialization_mode must be explicit")
        if not isinstance(self.regional_elliptic_numerics, Phase1FANumerics):
            raise Phase1FBContractError(
                "explicit frozen-compatible regional elliptic numerics are required"
            )
        if not isinstance(self.lapse_kernel_mode, LapseKernelMode):
            raise Phase1FBContractError("lapse_kernel_mode must be explicit")
        if not isinstance(self.requested_sector, ScalarBoostSector):
            raise Phase1FBContractError("transverse/vector dynamics are unsupported")
        if not isinstance(self.boundary_policy, BoostBoundaryKernelPolicy):
            raise Phase1FBContractError("boost-specific boundary policy is required")
        self.boundary_policy.validate_integrity()
        if not isinstance(self.zero_mode_closure, RegionalZeroModeClosure):
            raise Phase1FBContractError("explicit mean-zero closure is required")
        _require_token(self.initial_potential_provenance, "initial_potential_provenance")
        if self.initial_potential_units != "REFERENCE_LENGTH_SQUARED_PER_COMMON_TIME":
            raise Phase1FBContractError("initial scalar-potential units mismatch")
        _require_token(self.scientific_classification, "scientific_classification")
        if (
            self.scientific_classification
            != self.geometry_closure.scientific_classification
        ):
            raise Phase1FBContractError(
                "scenario classification must retain geometry provenance"
            )
        for item in fields(self.regional_elliptic_numerics):
            value = float(getattr(self.regional_elliptic_numerics, item.name))
            if not np.isfinite(value) or value <= 0.0:
                raise Phase1FBContractError(
                    "regional elliptic numerics changed after validation"
                )
        if self.zero_mode_closure.mean_condition != REGIONAL_METRIC_MEAN_ZERO:
            raise Phase1FBContractError("boost zero-mode mean condition mismatch")
        if (
            self.zero_mode_closure.classification
            != EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE
        ):
            raise Phase1FBContractError("boost zero-mode classification mismatch")
        if (
            not np.isfinite(self.zero_mode_closure.scale_factor)
            or self.zero_mode_closure.scale_factor <= 0.0
        ):
            raise Phase1FBContractError("boost zero-mode scale factor is invalid")
        history = tuple(self.dust_expansion_history)
        nt = self.geometry_closure.time_grid.size
        if len(history) != nt:
            raise Phase1FBContractError("dust expansion history must match time grid")
        for expansion in history:
            if not isinstance(expansion, RegionalExpansionReconstruction):
                raise Phase1FBContractError(
                    "dust expansion history must contain Phase 1F-A reconstructions"
                )
            expansion.validate_integrity()
            if expansion.domain.region != "wall":
                raise Phase1FBContractError("dust expansion history must be wall regional")
            if (
                expansion.domain.scientific_state
                is not self.geometry_closure.wall_domain.scientific_state
            ):
                raise Phase1FBContractError(
                    "dust expansion and common geometry must share sealed H1 state"
                )
            if (
                expansion.background_expansion_identity
                != self.geometry_closure.dust_expansion_background_identity
            ):
                raise Phase1FBContractError(
                    "dust expansion background/time identity does not match closure"
                )
        if self.boundary_policy.domain_id != self.geometry_closure.domain_id:
            raise Phase1FBContractError("boost boundary domain mismatch")
        if self.zero_mode_closure.domain != "wall":
            raise Phase1FBContractError("boost zero-mode closure must be wall regional")
        if (
            self.geometry_closure.normalization_kernel_identity
            != self.zero_mode_closure.provenance
        ):
            raise Phase1FBContractError("normalization/kernel provenance mismatch")
        if self.initialization_mode is BoostInitializationMode.SUPPLIED_INITIAL_BOOST:
            if self.initial_scalar_potential is None:
                raise Phase1FBContractError("supplied initial boost requires a potential")
            potential = _readonly_float(
                self.initial_scalar_potential, "initial_scalar_potential"
            ).reshape(-1)
            if potential.shape != (self.geometry_closure.wall_domain.operator.size,):
                raise Phase1FBContractError(
                    "initial scalar potential must use complete carrier grid"
                )
            object.__setattr__(self, "initial_scalar_potential", potential)
        else:
            if self.initial_scalar_potential is not None:
                raise Phase1FBContractError(
                    "expansion-matched initialization reconstructs rather than accepts potential"
                )
        object.__setattr__(self, "dust_expansion_history", history)
        object.__setattr__(self, "dust_expansion_time_grid", expansion_time)
        _seal(self, self._live_state())

    def _live_state(self) -> object:
        return (
            id(self.geometry_closure),
            tuple(id(item) for item in self.dust_expansion_history),
            self.dust_expansion_time_grid,
            self.dust_expansion_time_coordinate_id,
            self.regional_elliptic_numerics,
            self.initialization_mode,
            self.initial_scalar_potential,
            self.initial_potential_provenance,
            self.initial_potential_units,
            self.boundary_policy,
            self.zero_mode_closure,
            self.lapse_kernel_mode,
            self.requested_sector,
            self.scientific_classification,
        )

    def validate_integrity(self) -> None:
        self.geometry_closure.validate_integrity()
        for expansion in self.dust_expansion_history:
            expansion.validate_integrity()
        _validate(self, self._live_state())


@dataclass(frozen=True, slots=True, kw_only=True)
class ScalarDustWallBoostDiagnostics:
    expansion_compatibility_evidence_classification: str
    expansion_compatibility_max_abs: float
    expansion_compatibility_normalized_linf: float
    expansion_compatibility_tolerance: float
    expansion_compatibility_worst_time: float
    expansion_compatibility_worst_spatial_index: int
    propagation_evidence_classification: str
    propagation_residual_max_abs: float
    propagation_residual_normalized_linf: float
    propagation_residual_tolerance: float
    propagation_worst_time: float
    propagation_worst_spatial_index: int
    initial_boundary_normal_velocity_max_abs: float
    initial_boundary_normal_velocity_tolerance: float
    initial_boundary_worst_spatial_index: int
    initial_boundary_worst_axis: int
    driver_boundary_normal_acceleration_max_abs: float
    driver_boundary_normal_acceleration_tolerance: float
    driver_boundary_worst_time: float
    driver_boundary_worst_spatial_index: int
    driver_boundary_worst_axis: int
    propagated_boundary_normal_velocity_max_abs: float
    propagated_boundary_normal_velocity_tolerance: float
    propagated_boundary_worst_time: float
    propagated_boundary_worst_spatial_index: int
    propagated_boundary_worst_axis: int
    boundary_condition_classification: str
    boundary_runtime_enforcement: str
    potential_mean_max_abs: float
    lapse_raw_mean_max_abs: float
    lapse_q0_correction_max_abs: float
    scale_factor_rate_residual_max_abs: float
    maximum_velocity_to_light_speed_ratio: float
    linear_velocity_ratio_threshold: float
    curl_status: str
    dimensional_contract_status: str
    state_integrity_status: str


@dataclass(frozen=True, kw_only=True)
class ScalarDustWallBoostResult:
    """Conditional scalar dust velocity relative to the supplied wall observer."""

    time_grid: FloatArray
    scalar_potential: FloatArray
    scalar_potential_time_derivative: FloatArray
    projected_wall_lapse_perturbation: FloatArray
    dust_velocity_relative_to_wall: FloatArray
    physical_laplacian_of_potential: FloatArray
    expansion_compatibility_residual: FloatArray
    propagation_geodesic_residual: FloatArray
    diagnostics: ScalarDustWallBoostDiagnostics
    scenario: ScalarDustWallBoostScenario = field(repr=False, compare=False)
    numerics: ScalarDustWallBoostNumerics = field(repr=False, compare=False)
    realization_id: str
    scientific_classification: str
    transverse_sector_status: str
    transverse_zero_as_timescape_prediction: str
    harmonic_vector_sector_status: str
    harmonic_vector_zero_as_timescape_prediction: str
    wall_background_shear_status: str
    wall_shear_zero_as_timescape_prediction: str
    wall_proper_time_rate_role: str
    conditional_forward_uniqueness: str
    unique_from_frozen_y_alone: str
    unique_timescape_prediction: str
    observational_authorization: str
    scalar_potential_units: str
    velocity_units: str
    scalar_potential_time_derivative_units: str
    velocity_component_representation: str
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for name in (
            "time_grid",
            "scalar_potential",
            "scalar_potential_time_derivative",
            "projected_wall_lapse_perturbation",
            "dust_velocity_relative_to_wall",
            "physical_laplacian_of_potential",
            "expansion_compatibility_residual",
            "propagation_geodesic_residual",
        ):
            object.__setattr__(self, name, _readonly_float(getattr(self, name), name))
        if self.realization_id != REALIZATION_ID:
            raise Phase1FBContractError("Phase 1F-B realization identity changed")
        if self.transverse_sector_status != TRANSVERSE_SECTOR_EXCLUDED:
            raise Phase1FBContractError("transverse sector must remain explicitly excluded")
        if self.transverse_zero_as_timescape_prediction != TRANSVERSE_ZERO_NOT_GRANTED:
            raise Phase1FBContractError("transverse zero prediction is not granted")
        if self.harmonic_vector_sector_status != HARMONIC_VECTOR_SECTOR_EXCLUDED:
            raise Phase1FBContractError(
                "harmonic vector sector must remain outside the scalar-gradient state"
            )
        if (
            self.harmonic_vector_zero_as_timescape_prediction
            != HARMONIC_VECTOR_ZERO_NOT_GRANTED
        ):
            raise Phase1FBContractError("harmonic-vector zero prediction is not granted")
        if self.wall_background_shear_status != WALL_BACKGROUND_SHEAR_EXCLUDED:
            raise Phase1FBContractError(
                "wall background shear must be excluded by the selected sector"
            )
        if self.wall_shear_zero_as_timescape_prediction != WALL_SHEAR_ZERO_NOT_GRANTED:
            raise Phase1FBContractError("wall-shear zero prediction is not granted")
        if self.wall_proper_time_rate_role != WALL_PROPER_TIME_RATE_ROLE:
            raise Phase1FBContractError(
                "wall proper-time rate must remain provenance-only metadata"
            )
        if self.scalar_potential_units != "REFERENCE_LENGTH_SQUARED_PER_COMMON_TIME":
            raise Phase1FBContractError("result scalar-potential units mismatch")
        if self.velocity_units != "REFERENCE_LENGTH_PER_COMMON_TIME":
            raise Phase1FBContractError("result velocity units mismatch")
        if (
            self.scalar_potential_time_derivative_units
            != "REFERENCE_LENGTH_SQUARED_PER_COMMON_TIME_SQUARED"
        ):
            raise Phase1FBContractError("result potential-derivative units mismatch")
        if (
            self.velocity_component_representation
            != "WALL_REFERENCE_METRIC_ORTHONORMAL_CHOLESKY_COMPONENTS"
        ):
            raise Phase1FBContractError("result velocity component representation mismatch")
        _seal(self, self._live_state())

    def _live_state(self) -> object:
        return (
            self.time_grid,
            self.scalar_potential,
            self.scalar_potential_time_derivative,
            self.projected_wall_lapse_perturbation,
            self.dust_velocity_relative_to_wall,
            self.physical_laplacian_of_potential,
            self.expansion_compatibility_residual,
            self.propagation_geodesic_residual,
            self.diagnostics,
            id(self.scenario),
            self.numerics,
            self.realization_id,
            self.scientific_classification,
            self.transverse_sector_status,
            self.transverse_zero_as_timescape_prediction,
            self.harmonic_vector_sector_status,
            self.harmonic_vector_zero_as_timescape_prediction,
            self.wall_background_shear_status,
            self.wall_shear_zero_as_timescape_prediction,
            self.wall_proper_time_rate_role,
            self.conditional_forward_uniqueness,
            self.unique_from_frozen_y_alone,
            self.unique_timescape_prediction,
            self.observational_authorization,
            self.scalar_potential_units,
            self.velocity_units,
            self.scalar_potential_time_derivative_units,
            self.velocity_component_representation,
        )

    def validate_integrity(self) -> None:
        self.scenario.validate_integrity()
        _validate(self, self._live_state())
