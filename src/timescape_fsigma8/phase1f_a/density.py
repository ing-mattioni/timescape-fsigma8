"""Regional and sharp-carrier matter-density realization for Phase 1F-A.

CGI density scalarization follows Eqs. (2.2), (2.19)--(2.24) of
arXiv:2511.17160v2.  Carrier assembly and broken intertwining are the
explicit human-approved Phase 1F-A closure equations; they are not a unique
Timescape morphology or physical junction law.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import ArrayLike

from timescape_fsigma8.phase1f_a.models import (
    CONDITIONAL,
    MATHEMATICAL_OPERATOR_FIXTURE_ONLY,
    PHYSICAL_H1_CARRIER_DENSITY,
    BoundaryKernelPolicy,
    FloatArray,
    Phase1FAContractError,
    Phase1FANumerics,
    Phase1FAScientificState,
    RegionalDomainSpec,
    RegionalZeroModeClosure,
    canonical_state,
    readonly_float,
    seal_integrity,
    validate_integrity,
)
from timescape_fsigma8.phase1f_a.operators import (
    RegionalEllipticDiagnostics,
    RegionalEllipticSystem,
    apply_regional_laplace_beltrami,
    assemble_regional_elliptic_system,
    embed_regional_field,
    solve_regional_laplace_beltrami,
)


@dataclass(frozen=True, kw_only=True)
class RegionalDensityReconstruction:
    """Conditionally reconstructed regional ``delta_m`` nonzero modes."""

    delta_m: FloatArray
    delta_cgi: FloatArray
    regional_values: FloatArray
    regional_source: FloatArray
    regional_indices: np.ndarray
    domain: RegionalDomainSpec
    zero_mode_closure: RegionalZeroModeClosure
    boundary_policy: BoundaryKernelPolicy
    diagnostics: RegionalEllipticDiagnostics
    metric_frame_identity: str
    provenance: str
    scientific_classification: str
    _system: RegionalEllipticSystem = field(repr=False, compare=False)
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for name in ("delta_m", "delta_cgi", "regional_values", "regional_source"):
            object.__setattr__(self, name, readonly_float(getattr(self, name), name))
        indices = np.array(self.regional_indices, dtype=np.int64, copy=True)
        indices.setflags(write=False)
        object.__setattr__(self, "regional_indices", indices)
        seal_integrity(self, self._live_state())

    def _live_state(self) -> object:
        return (
            self.delta_m,
            self.delta_cgi,
            self.regional_values,
            self.regional_source,
            self.regional_indices,
            id(self.domain),
            self.zero_mode_closure,
            self.boundary_policy,
            self.diagnostics,
            self.metric_frame_identity,
            self.provenance,
            self.scientific_classification,
            id(self._system),
        )

    def validate_integrity(self) -> None:
        self.domain.validate_integrity()
        validate_integrity(self, self._live_state())


@dataclass(frozen=True, kw_only=True)
class CarrierDensityDiagnostics:
    wall_physical_volume_consistency_residual: float
    void_physical_volume_consistency_residual: float
    partition_residual: float
    carrier_volume_additivity_residual: float
    background_density_assembly_residual: float
    global_mean_residual: float
    wall_intertwining_residual: float
    void_intertwining_residual: float
    maximum_interface_density_jump: float
    dimensional_contract_status: str
    state_integrity_status: str
    frozen_delta_comparison_status: str


@dataclass(frozen=True, kw_only=True)
class CarrierDensityResult:
    """Physical sharp-carrier density assembled without H1 potential aliasing."""

    rho_wall: FloatArray
    rho_void: FloatArray
    rho_carrier: FloatArray
    rho_bar_carrier: float
    delta_m_carrier: FloatArray
    b_wall: float
    b_void: float
    f_wall: float
    f_void: float
    wall_physical_volume: float
    void_physical_volume: float
    diagnostics: CarrierDensityDiagnostics
    morphology_provenance: str
    normalization_provenance: str
    scientific_classification: str
    scientific_state: Phase1FAScientificState = field(repr=False, compare=False)
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for name in ("rho_wall", "rho_void", "rho_carrier", "delta_m_carrier"):
            object.__setattr__(self, name, readonly_float(getattr(self, name), name))
        seal_integrity(self, self._live_state())

    def _live_state(self) -> object:
        return (
            self.rho_wall,
            self.rho_void,
            self.rho_carrier,
            self.rho_bar_carrier,
            self.delta_m_carrier,
            self.b_wall,
            self.b_void,
            self.f_wall,
            self.f_void,
            self.wall_physical_volume,
            self.void_physical_volume,
            self.diagnostics,
            self.morphology_provenance,
            self.normalization_provenance,
            self.scientific_classification,
            id(self.scientific_state),
        )

    def validate_integrity(self) -> None:
        self.scientific_state.validate_integrity()
        validate_integrity(self, self._live_state())


def reconstruct_regional_density(
    *,
    delta_cgi: ArrayLike,
    regional_geometry: RegionalDomainSpec,
    boundary_policy: BoundaryKernelPolicy,
    zero_mode_closure: RegionalZeroModeClosure,
    numerics: Phase1FANumerics,
    provenance: str,
) -> RegionalDensityReconstruction:
    """Solve ``Delta_gamma_r delta_m,r = Delta_r``.

    This is the configuration-space form of the density CGI relation in
    Eqs. (2.2), (2.19)--(2.20) of arXiv:2511.17160v2.  No global ``k`` or
    H1 transmission potential is used.  The homogeneous mode is fixed only
    by the explicit ``RegionalZeroModeClosure`` supplied by the caller.
    """
    regional_geometry.validate_integrity()
    if zero_mode_closure is None:  # defensive runtime gate beyond signature.
        raise Phase1FAContractError("regional zero-mode closure is required")
    if not provenance.strip():
        raise Phase1FAContractError("density reconstruction provenance is required")
    source_full = readonly_float(delta_cgi, "delta_cgi").reshape(-1)
    if source_full.shape != (regional_geometry.operator.size,):
        raise Phase1FAContractError("delta_cgi must use the complete carrier grid")
    system = assemble_regional_elliptic_system(
        domain=regional_geometry,
        boundary_policy=boundary_policy,
        numerics=numerics,
    )
    source_regional = source_full[system.regional_indices]
    solution, diagnostics = solve_regional_laplace_beltrami(
        source=source_regional,
        system=system,
        zero_mode_closure=zero_mode_closure,
        numerics=numerics,
    )
    embedded = embed_regional_field(system=system, regional_field=solution)
    source_embedded = embed_regional_field(
        system=system, regional_field=source_regional
    )
    classification = (
        CONDITIONAL
        if regional_geometry.operator.carrier.dimension == 3
        else MATHEMATICAL_OPERATOR_FIXTURE_ONLY
    )
    return RegionalDensityReconstruction(
        delta_m=embedded,
        delta_cgi=source_embedded,
        regional_values=solution,
        regional_source=source_regional,
        regional_indices=system.regional_indices,
        domain=regional_geometry,
        zero_mode_closure=zero_mode_closure,
        boundary_policy=boundary_policy,
        diagnostics=diagnostics,
        metric_frame_identity=(
            f"{regional_geometry.region}:"
            f"{regional_geometry.geometry.normalization.normalization_id}:"
            "COMOVING_REGIONAL_DUST_FRAME"
        ),
        provenance=provenance,
        scientific_classification=classification,
        _system=system,
    )


def _relative_residual(actual: float, expected: float) -> float:
    return abs(actual - expected) / max(abs(actual), abs(expected), np.finfo(float).tiny)


def assemble_carrier_density(
    *,
    wall_density: RegionalDensityReconstruction,
    void_density: RegionalDensityReconstruction,
    wall_background_density: float,
    void_background_density: float,
    wall_physical_volume: float,
    void_physical_volume: float,
    h1_partition,
    scientific_state: Phase1FAScientificState,
    numerics: Phase1FANumerics,
) -> CarrierDensityResult:
    """Assemble ``rho_C`` and ``delta_m,C`` from regional physical densities.

    ``rho_r=bar(rho_r)(1+delta_m,r)`` is the density definition associated
    with GM Eq. (2.2).  The sharp carrier equations, including
    ``delta_m,C|r=(b_r-1)+b_r delta_m,r``, are the explicitly approved
    Phase 1F-A sections 7--8 model extension (no paper equation number).
    The H1 transmission potential is never consulted.
    """
    scientific_state.validate_integrity()
    scientific_state.require_physical_three_dimensions(
        context="physical Phase 1F-A carrier density"
    )
    wall_density.validate_integrity()
    void_density.validate_integrity()
    if wall_density.domain.scientific_state is not scientific_state or void_density.domain.scientific_state is not scientific_state:
        raise Phase1FAContractError("regional densities must share the carrier scientific state")
    if wall_density.domain.region != "wall" or void_density.domain.region != "void":
        raise Phase1FAContractError("wall/void density provenance is reversed")
    if h1_partition is not scientific_state.operator.morphology:
        raise Phase1FAContractError("carrier density partition must be the validated H1 morphology")
    for value, name in (
        (wall_background_density, "wall_background_density"),
        (void_background_density, "void_background_density"),
        (wall_physical_volume, "wall_physical_volume"),
        (void_physical_volume, "void_physical_volume"),
    ):
        if not np.isfinite(value) or value <= 0.0:
            raise Phase1FAContractError(f"{name} must be finite and positive")
    expected_wall, expected_void = scientific_state.operator.physical_regional_volumes(
        a_w=wall_density.zero_mode_closure.scale_factor,
        a_v=void_density.zero_mode_closure.scale_factor,
    )
    wall_volume_residual = _relative_residual(wall_physical_volume, expected_wall)
    void_volume_residual = _relative_residual(void_physical_volume, expected_void)
    if max(wall_volume_residual, void_volume_residual) > numerics.volume_consistency_tolerance:
        raise Phase1FAContractError("regional physical-volume consistency failed")

    total_volume = wall_physical_volume + void_physical_volume
    f_wall = wall_physical_volume / total_volume
    f_void = void_physical_volume / total_volume
    rho_bar = f_wall * wall_background_density + f_void * void_background_density
    b_wall = wall_background_density / rho_bar
    b_void = void_background_density / rho_bar
    wall_mask = scientific_state.operator.morphology.wall_domain.reshape(-1)
    void_mask = scientific_state.operator.morphology.void_domain.reshape(-1)
    partition_residual = float(
        np.max(np.abs(wall_mask.astype(float) + void_mask.astype(float) - 1.0))
    )

    rho_wall = np.zeros(scientific_state.operator.size, dtype=np.float64)
    rho_void = np.zeros_like(rho_wall)
    rho_wall[wall_mask] = wall_background_density * (
        1.0 + wall_density.delta_m[wall_mask]
    )
    rho_void[void_mask] = void_background_density * (
        1.0 + void_density.delta_m[void_mask]
    )
    if np.any(rho_wall[wall_mask] <= 0.0) or np.any(rho_void[void_mask] <= 0.0):
        raise Phase1FAContractError(
            "physical regional density must remain strictly positive on the selected linear fixture"
        )
    rho_carrier = rho_wall + rho_void
    delta_carrier = rho_carrier / rho_bar - 1.0

    # Human-approved Phase 1F-A broken intertwining; the constant background
    # offset is deliberately retained and annihilated region by region.
    wall_delta_regional = delta_carrier[wall_density.regional_indices]
    void_delta_regional = delta_carrier[void_density.regional_indices]
    wall_broken = apply_regional_laplace_beltrami(
        system=wall_density._system, field=wall_delta_regional
    )
    void_broken = apply_regional_laplace_beltrami(
        system=void_density._system, field=void_delta_regional
    )
    wall_intertwining = float(
        np.max(np.abs(wall_broken - b_wall * wall_density.regional_source))
    )
    void_intertwining = float(
        np.max(np.abs(void_broken - b_void * void_density.regional_source))
    )
    if max(wall_intertwining, void_intertwining) > numerics.intertwining_tolerance:
        raise Phase1FAContractError("broken density intertwining residual exceeds tolerance")

    operator = scientific_state.operator
    weights = operator.reference_weights
    metric_ratio = operator.metric_volume_ratio
    scale_field = np.where(
        wall_mask,
        wall_density.zero_mode_closure.scale_factor**3,
        void_density.zero_mode_closure.scale_factor**3,
    )
    physical_weights = weights * metric_ratio * scale_field
    global_mean = float(
        np.dot(physical_weights, delta_carrier) / np.sum(physical_weights)
    )
    if abs(global_mean) > numerics.carrier_mean_tolerance:
        raise Phase1FAContractError("carrier density contrast global mean failed")
    integrated_mean = float(np.dot(physical_weights, rho_carrier) / total_volume)
    background_residual = integrated_mean - rho_bar
    if abs(background_residual) > numerics.carrier_mean_tolerance:
        raise Phase1FAContractError("carrier background-density assembly failed")
    volume_additivity = float(np.sum(physical_weights) - total_volume)
    if abs(volume_additivity) > numerics.volume_consistency_tolerance:
        raise Phase1FAContractError("carrier physical-volume additivity failed")

    jumps = [
        abs(rho_carrier[face.wall_index] - rho_carrier[face.void_index])
        for face in operator.interface_faces
    ]
    diagnostics = CarrierDensityDiagnostics(
        wall_physical_volume_consistency_residual=wall_volume_residual,
        void_physical_volume_consistency_residual=void_volume_residual,
        partition_residual=partition_residual,
        carrier_volume_additivity_residual=volume_additivity,
        background_density_assembly_residual=background_residual,
        global_mean_residual=global_mean,
        wall_intertwining_residual=wall_intertwining,
        void_intertwining_residual=void_intertwining,
        maximum_interface_density_jump=max(jumps, default=0.0),
        dimensional_contract_status="CONDITIONAL_3D_ONLY",
        state_integrity_status="VALIDATED_FAIL_CLOSED",
        frozen_delta_comparison_status="NOT_EVALUABLE_WITHOUT_CODOMAIN_ADAPTER",
    )
    return CarrierDensityResult(
        rho_wall=rho_wall,
        rho_void=rho_void,
        rho_carrier=rho_carrier,
        rho_bar_carrier=rho_bar,
        delta_m_carrier=delta_carrier,
        b_wall=b_wall,
        b_void=b_void,
        f_wall=f_wall,
        f_void=f_void,
        wall_physical_volume=wall_physical_volume,
        void_physical_volume=void_physical_volume,
        diagnostics=diagnostics,
        morphology_provenance=scientific_state.morphology_provenance,
        normalization_provenance=scientific_state.normalization_provenance,
        scientific_classification=PHYSICAL_H1_CARRIER_DENSITY,
        scientific_state=scientific_state,
    )
