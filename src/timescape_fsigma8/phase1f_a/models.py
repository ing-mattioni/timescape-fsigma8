"""Typed scientific contracts for the conditional Phase 1F-A realization.

The model-extension equations in this package are the explicitly authorised
Phase 1F-A specification (2026-08-24).  The inherited CGI definitions are
from Eqs. (2.2), (2.19)--(2.24) of Galoppo & Mourier,
arXiv:2511.17160v2.  No code from the unlicensed upstream notebook is used.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, fields, is_dataclass
from types import MappingProxyType
from typing import Mapping

import numpy as np
from numpy.typing import ArrayLike, NDArray

from timescape_fsigma8.transfer import ContinuumH1Operator


FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]

REALIZATION_ID = "H1-1F-A-BROKEN-DENSITY-SPECTRAL-LONGITUDINAL-BOOST-V1"
REALIZATION_ROLE = "CONDITIONAL_THEORETICAL_FORWARD_REALIZATION"
SCIENTIFIC_READINESS = "IMPLEMENTED_CONDITIONALLY"
DIFFERENTIAL_STATE_RANK = 4

DERIVED = "DERIVED"
CONDITIONAL = "CONDITIONAL"
EXTERNAL_CLOSURE = "EXTERNAL_CLOSURE"
SYNTHETIC_VALIDATION_ONLY = "SYNTHETIC_VALIDATION_ONLY"
MATHEMATICAL_OPERATOR_FIXTURE_ONLY = "MATHEMATICAL_OPERATOR_FIXTURE_ONLY"
NOT_GRANTED = "NOT_GRANTED"
NOT_EVALUABLE = "NOT_EVALUABLE"
NOT_APPLICABLE = "NOT_APPLICABLE"
TRANSVERSE_SECTOR_UNRESOLVED = "TRANSVERSE_SECTOR_UNRESOLVED"
EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE = (
    "EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE"
)
PHYSICAL_H1_CARRIER_DENSITY = "PHYSICAL_H1_CARRIER_DENSITY_CONDITIONAL_3D_ONLY"
DUST_EXPANSION_FIELD_RECONSTRUCTED_CONDITIONALLY = (
    "DUST_EXPANSION_FIELD_RECONSTRUCTED_CONDITIONALLY"
)
LONGITUDINAL_RELATIVE_DUST_TO_WALL_VELOCITY = (
    "LONGITUDINAL_RELATIVE_DUST_TO_WALL_VELOCITY"
)
NOT_EVALUABLE_WITHOUT_CODOMAIN_ADAPTER = (
    "NOT_EVALUABLE_WITHOUT_CODOMAIN_ADAPTER"
)

REGIONAL_METRIC_MEAN_ZERO = "REGIONAL_METRIC_MEAN_ZERO"
NO_FLUX_REGIONAL_INTERFACE_PERIODIC_CARRIER = (
    "NO_FLUX_REGIONAL_INTERFACE_PERIODIC_CARRIER"
)
SINGLE_REGIONAL_CONSTANT_REMOVED = "SINGLE_REGIONAL_CONSTANT_REMOVED"
REGIONAL_SOURCE_MEAN_ZERO = "REGIONAL_SOURCE_MEAN_ZERO"


class Phase1FAContractError(ValueError):
    """A required Phase 1F-A scientific contract was absent or inconsistent."""


class Phase1FADegeneracyError(Phase1FAContractError):
    """An elliptic or spectral operation lies outside its valid branch."""


class Phase1FADimensionalContractError(Phase1FAContractError):
    """Reduced-dimensional data were requested with physical 3-D semantics."""


class Phase1FAStateIntegrityError(Phase1FAContractError):
    """Validated Phase 1F-A scientific state changed after construction."""


def readonly_float(values: ArrayLike, name: str) -> FloatArray:
    """Return a finite defensive float64 copy with writes disabled."""
    result = np.array(values, dtype=np.float64, copy=True)
    if not np.all(np.isfinite(result)):
        raise Phase1FAContractError(f"{name} must contain only finite values")
    result.setflags(write=False)
    return result


def readonly_int(values: ArrayLike, name: str) -> IntArray:
    """Return a defensive integer copy with writes disabled."""
    result = np.array(values, dtype=np.int64, copy=True)
    result.setflags(write=False)
    return result


def array_fingerprint(values: NDArray[np.generic]) -> tuple[object, ...]:
    """Return a detached deterministic digest of an array."""
    array = np.ascontiguousarray(values)
    return (
        array.dtype.str,
        tuple(array.shape),
        hashlib.sha256(array.view(np.uint8)).hexdigest(),
    )


def canonical_state(value: object) -> object:
    """Detach supported scientific state from mutable Python references."""
    if isinstance(value, np.ndarray):
        return ("array",) + array_fingerprint(value)
    if is_dataclass(value) and not isinstance(value, type):
        return (
            type(value).__qualname__,
            tuple(
                (item.name, canonical_state(getattr(value, item.name)))
                for item in fields(value)
                if item.name != "_integrity_token"
            ),
        )
    if isinstance(value, Mapping):
        return tuple(
            sorted((str(key), canonical_state(item)) for key, item in value.items())
        )
    if isinstance(value, (tuple, list)):
        return tuple(canonical_state(item) for item in value)
    if isinstance(value, (str, int, float, bool, type(None))):
        return value
    return (type(value).__qualname__, id(value))


def seal_integrity(instance: object, state: object) -> None:
    object.__setattr__(instance, "_integrity_token", canonical_state(state))


def validate_integrity(instance: object, state: object) -> None:
    expected = getattr(instance, "_integrity_token", None)
    if expected != canonical_state(state):
        raise Phase1FAStateIntegrityError(
            "live Phase 1F-A scientific state differs from validated construction"
        )


def require_nonempty(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise Phase1FAContractError(f"{name} must be an explicit nonempty token")


def require_positive(value: float, name: str) -> None:
    if not np.isfinite(value) or value <= 0.0:
        raise Phase1FAContractError(f"{name} must be finite and positive")


@dataclass(frozen=True, slots=True, kw_only=True)
class Phase1FANumerics:
    """All Phase 1F-A numerical tolerances; there are no scientific defaults."""

    elliptic_residual_tolerance: float
    mean_tolerance: float
    source_compatibility_tolerance: float
    volume_consistency_tolerance: float
    carrier_mean_tolerance: float
    intertwining_tolerance: float
    eigenpair_tolerance: float
    basis_normalization_tolerance: float
    boost_residual_tolerance: float
    dressed_mean_tolerance: float
    residual_norm_floor: float
    maximum_condition_number: float

    def __post_init__(self) -> None:
        for item in fields(self):
            require_positive(float(getattr(self, item.name)), item.name)


@dataclass(frozen=True, slots=True, kw_only=True)
class RegionalZeroModeClosure:
    """Explicit regional mean-zero closure for the CGI kernel.

    The need for a homogeneous-mode closure follows from the Laplacian CGI
    definitions in Eqs. (2.2), (2.19)--(2.24) of arXiv:2511.17160v2.
    The selected mean-zero value itself is an external, human-authorised
    Phase 1F-A closure rather than a unique Timescape prediction.
    """

    mean_condition: str
    spatial_measure_identity: str
    scale_factor: float
    provenance: str
    classification: str
    frame: str
    domain: str

    def __post_init__(self) -> None:
        for name in (
            "spatial_measure_identity",
            "provenance",
            "frame",
            "domain",
        ):
            require_nonempty(getattr(self, name), name)
        require_positive(self.scale_factor, "scale_factor")
        if self.mean_condition != REGIONAL_METRIC_MEAN_ZERO:
            raise Phase1FAContractError("V1 requires REGIONAL_METRIC_MEAN_ZERO")
        if self.classification != EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE:
            raise Phase1FAContractError(
                "regional zero-mode normalization must remain an explicit external closure"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class BoundaryKernelPolicy:
    """Explicit regional boundary, compatibility, and nullspace policy."""

    domain: str
    boundary_condition_kind: str
    nullspace_handling: str
    compatibility_condition: str
    provenance: str

    def __post_init__(self) -> None:
        require_nonempty(self.domain, "domain")
        require_nonempty(self.provenance, "provenance")
        if self.boundary_condition_kind != NO_FLUX_REGIONAL_INTERFACE_PERIODIC_CARRIER:
            raise Phase1FAContractError("unsupported V1 regional boundary condition")
        if self.nullspace_handling != SINGLE_REGIONAL_CONSTANT_REMOVED:
            raise Phase1FAContractError("V1 removes exactly one regional constant")
        if self.compatibility_condition != REGIONAL_SOURCE_MEAN_ZERO:
            raise Phase1FAContractError("V1 requires regional source mean zero")


@dataclass(frozen=True, kw_only=True)
class Phase1FAScientificState:
    """Sealed binding to one already-validated Phase 1E-G operator."""

    operator: ContinuumH1Operator
    morphology_provenance: str
    normalization_provenance: str
    scientific_classification: str
    realization_id: str = field(init=False, default=REALIZATION_ID)
    differential_state_rank: int = field(init=False, default=DIFFERENTIAL_STATE_RANK)
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if not isinstance(self.operator, ContinuumH1Operator):
            raise Phase1FAContractError("a validated ContinuumH1Operator is required")
        self.operator._validate_assembled_state_integrity()
        for name in (
            "morphology_provenance",
            "normalization_provenance",
            "scientific_classification",
        ):
            require_nonempty(getattr(self, name), name)
        seal_integrity(self, self._live_state())

    def _live_state(self) -> object:
        return (
            id(self.operator),
            id(self.operator.morphology),
            self.operator.carrier.dimension,
            tuple(self.operator.carrier.grid_shape),
            self.operator.morphology.morphology_id,
            self.morphology_provenance,
            self.normalization_provenance,
            self.scientific_classification,
            self.realization_id,
            self.differential_state_rank,
        )

    def validate_integrity(self) -> None:
        self.operator._validate_assembled_state_integrity()
        validate_integrity(self, self._live_state())

    def require_physical_three_dimensions(self, *, context: str) -> None:
        self.validate_integrity()
        try:
            self.operator.require_physical_volume_dimension(context=context)
        except Exception as exc:
            raise Phase1FADimensionalContractError(str(exc)) from exc


@dataclass(frozen=True, kw_only=True)
class RegionalDomainSpec:
    """One explicit wall or void domain bound to a sealed continuum operator."""

    scientific_state: Phase1FAScientificState
    region: str
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.scientific_state.validate_integrity()
        if self.region not in {"wall", "void"}:
            raise Phase1FAContractError("region must be wall or void")
        seal_integrity(self, self._live_state())

    def _live_state(self) -> object:
        return (id(self.scientific_state), self.region)

    def validate_integrity(self) -> None:
        self.scientific_state.validate_integrity()
        validate_integrity(self, self._live_state())

    @property
    def operator(self) -> ContinuumH1Operator:
        self.validate_integrity()
        return self.scientific_state.operator

    @property
    def geometry(self):
        self.validate_integrity()
        return (
            self.operator.wall_geometry
            if self.region == "wall"
            else self.operator.void_geometry
        )

    @property
    def mask(self) -> NDArray[np.bool_]:
        self.validate_integrity()
        values = (
            self.operator.morphology.wall_domain
            if self.region == "wall"
            else self.operator.morphology.void_domain
        )
        result = np.array(values, dtype=np.bool_, copy=True).reshape(-1)
        result.setflags(write=False)
        return result


@dataclass(frozen=True, kw_only=True)
class ExternalBoostDivergenceClosure:
    """Explicit external scalar divergence; never an implicit zero boost."""

    divergence: FloatArray
    source_frame: str
    destination_frame: str
    time_coordinate: str
    spatial_metric_identity: str
    units: str
    domain: str
    normalization_closure_id: str
    provenance: str
    classification: str
    closure_kind: str = field(init=False, default="EXTERNAL_SCALAR_DIVERGENCE_SOURCE")
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "divergence", readonly_float(self.divergence, "divergence"))
        self._validate_metadata()
        seal_integrity(self, self._live_state())

    def _validate_metadata(self) -> None:
        for item in (
            "source_frame", "destination_frame", "time_coordinate",
            "spatial_metric_identity", "units", "domain",
            "normalization_closure_id", "provenance",
        ):
            require_nonempty(getattr(self, item), item)
        if self.classification not in {EXTERNAL_CLOSURE, SYNTHETIC_VALIDATION_ONLY}:
            raise Phase1FAContractError("boost classification must remain external")

    def _live_state(self) -> object:
        return tuple(
            getattr(self, item.name)
            for item in fields(self)
            if item.name != "_integrity_token"
        )

    def validate_integrity(self) -> None:
        validate_integrity(self, self._live_state())


@dataclass(frozen=True, kw_only=True)
class ExternalBoostPotentialClosure:
    """Explicit external scalar velocity potential with metric provenance."""

    potential: FloatArray
    source_frame: str
    destination_frame: str
    time_coordinate: str
    spatial_metric_identity: str
    units: str
    domain: str
    normalization_closure_id: str
    provenance: str
    classification: str
    closure_kind: str = field(init=False, default="EXTERNAL_SCALAR_VELOCITY_POTENTIAL")
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "potential", readonly_float(self.potential, "potential"))
        for item in (
            "source_frame", "destination_frame", "time_coordinate",
            "spatial_metric_identity", "units", "domain",
            "normalization_closure_id", "provenance",
        ):
            require_nonempty(getattr(self, item), item)
        if self.classification not in {EXTERNAL_CLOSURE, SYNTHETIC_VALIDATION_ONLY}:
            raise Phase1FAContractError("boost classification must remain external")
        seal_integrity(self, self._live_state())

    def _live_state(self) -> object:
        return tuple(
            getattr(self, item.name)
            for item in fields(self)
            if item.name != "_integrity_token"
        )

    def validate_integrity(self) -> None:
        validate_integrity(self, self._live_state())


@dataclass(frozen=True, kw_only=True)
class DressedSpacetimeMapClosure:
    """Explicit carrier-to-dressed pullback data; no public default exists."""

    source_frame: str
    destination_frame: str
    time_mapping: str
    spatial_mapping: str
    destination_spatial_metric: str
    destination_source_indices: IntArray
    destination_reference_weights: FloatArray
    destination_metric_volume_ratio: FloatArray
    destination_measure_jacobian: FloatArray
    provenance: str
    scientific_classification: str
    spatial_dimension: int
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for name in (
            "source_frame", "destination_frame", "time_mapping",
            "spatial_mapping", "destination_spatial_metric", "provenance",
        ):
            require_nonempty(getattr(self, name), name)
        indices = readonly_int(self.destination_source_indices, "destination_source_indices")
        weights = readonly_float(self.destination_reference_weights, "destination_reference_weights")
        ratio = readonly_float(self.destination_metric_volume_ratio, "destination_metric_volume_ratio")
        jacobian = readonly_float(self.destination_measure_jacobian, "destination_measure_jacobian")
        if indices.ndim != 1 or weights.shape != indices.shape or ratio.shape != indices.shape or jacobian.shape != indices.shape:
            raise Phase1FAContractError("dressed mapping arrays must share one explicit destination shape")
        if np.any(weights <= 0.0) or np.any(ratio <= 0.0) or np.any(jacobian <= 0.0):
            raise Phase1FAContractError("dressed destination measure data must be positive")
        if self.spatial_dimension != 3:
            raise Phase1FADimensionalContractError("physical dressed density requires spatial_dimension == 3")
        if self.scientific_classification not in {EXTERNAL_CLOSURE, SYNTHETIC_VALIDATION_ONLY}:
            raise Phase1FAContractError("dressed map must remain an explicit external closure")
        object.__setattr__(self, "destination_source_indices", indices)
        object.__setattr__(self, "destination_reference_weights", weights)
        object.__setattr__(self, "destination_metric_volume_ratio", ratio)
        object.__setattr__(self, "destination_measure_jacobian", jacobian)
        seal_integrity(self, self._live_state())

    def _live_state(self) -> object:
        return tuple(
            getattr(self, item.name)
            for item in fields(self)
            if item.name != "_integrity_token"
        )

    def validate_integrity(self) -> None:
        validate_integrity(self, self._live_state())


def immutable_metadata(values: Mapping[str, str]) -> Mapping[str, str]:
    """Defensively freeze provenance metadata."""
    result = dict(values)
    if not all(isinstance(key, str) and isinstance(value, str) for key, value in result.items()):
        raise Phase1FAContractError("metadata keys and values must be strings")
    return MappingProxyType(result)
