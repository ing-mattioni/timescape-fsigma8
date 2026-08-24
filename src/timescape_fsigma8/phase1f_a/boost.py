"""Explicit scalar-longitudinal dust-to-wall boost closure for Phase 1F-A."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from timescape_fsigma8.phase1f_a.models import (
    LONGITUDINAL_RELATIVE_DUST_TO_WALL_VELOCITY,
    MATHEMATICAL_OPERATOR_FIXTURE_ONLY,
    TRANSVERSE_SECTOR_UNRESOLVED,
    BoundaryKernelPolicy,
    ExternalBoostDivergenceClosure,
    ExternalBoostPotentialClosure,
    FloatArray,
    Phase1FAContractError,
    Phase1FANumerics,
    RegionalDomainSpec,
    RegionalZeroModeClosure,
    readonly_float,
    seal_integrity,
    validate_integrity,
)
from timescape_fsigma8.phase1f_a.operators import (
    apply_regional_laplace_beltrami,
    assemble_regional_elliptic_system,
    embed_regional_field,
    solve_regional_laplace_beltrami,
)


BoostClosure = ExternalBoostDivergenceClosure | ExternalBoostPotentialClosure


@dataclass(frozen=True, kw_only=True)
class LongitudinalRelativeVelocityResult:
    """Longitudinal relative dust-to-wall velocity; transverse part unresolved."""

    scalar_potential: FloatArray
    longitudinal_relative_dust_to_wall_velocity: FloatArray
    reconstructed_divergence: FloatArray
    supplied_divergence: FloatArray
    boost_residual_max_abs: float
    closure_kind: str
    source_frame: str
    destination_frame: str
    time_coordinate: str
    spatial_metric_identity: str
    units: str
    provenance: str
    scientific_classification: str
    transverse_sector_status: str
    domain: RegionalDomainSpec = field(repr=False, compare=False)
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for name in (
            "scalar_potential",
            "longitudinal_relative_dust_to_wall_velocity",
            "reconstructed_divergence",
            "supplied_divergence",
        ):
            object.__setattr__(self, name, readonly_float(getattr(self, name), name))
        if self.transverse_sector_status != TRANSVERSE_SECTOR_UNRESOLVED:
            raise Phase1FAContractError("V1 must retain the unresolved transverse sector")
        seal_integrity(self, self._live_state())

    def _live_state(self) -> object:
        return (
            self.scalar_potential,
            self.longitudinal_relative_dust_to_wall_velocity,
            self.reconstructed_divergence,
            self.supplied_divergence,
            self.boost_residual_max_abs,
            self.closure_kind,
            self.source_frame,
            self.destination_frame,
            self.time_coordinate,
            self.spatial_metric_identity,
            self.units,
            self.provenance,
            self.scientific_classification,
            self.transverse_sector_status,
            id(self.domain),
        )

    def validate_integrity(self) -> None:
        self.domain.validate_integrity()
        validate_integrity(self, self._live_state())


def _regional_gradient(
    *, domain: RegionalDomainSpec, potential_full: FloatArray
) -> FloatArray:
    """Return the reference-grid gradient used for ``v_dw,L=D psi_dw``.

    The scalar-longitudinal decomposition is the explicit Phase 1F-A
    section 13 closure.  GM Eqs. (2.9)--(2.11) define the spatial derivative
    convention inherited by the CGI variables; no tracer/observational frame
    identification is made here.
    """
    operator = domain.operator
    shape = operator.carrier.grid_shape
    mask = domain.mask.reshape(shape)
    potential = potential_full.reshape(shape)
    covariant_gradient = np.zeros(
        (operator.size, operator.carrier.dimension), dtype=np.float64
    )
    for index in np.ndindex(shape):
        if not mask[index]:
            continue
        flat = int(np.ravel_multi_index(index, shape))
        for axis, spacing in enumerate(operator.carrier.grid_spacing):
            plus = list(index)
            minus = list(index)
            plus[axis] = (plus[axis] + 1) % shape[axis]
            minus[axis] = (minus[axis] - 1) % shape[axis]
            plus_t = tuple(plus)
            minus_t = tuple(minus)
            if mask[plus_t] and mask[minus_t]:
                derivative = (potential[plus_t] - potential[minus_t]) / (2.0 * spacing)
            elif mask[plus_t]:
                derivative = (potential[plus_t] - potential[index]) / spacing
            elif mask[minus_t]:
                derivative = (potential[index] - potential[minus_t]) / spacing
            else:
                derivative = 0.0
            covariant_gradient[flat, axis] = derivative
    inverse_metric = domain.geometry.metric_inverse.reshape(
        (operator.size, operator.carrier.dimension, operator.carrier.dimension)
    )
    gradient = np.einsum(
        "nij,nj->ni", inverse_metric, covariant_gradient, optimize=True
    )
    gradient[~domain.mask, :] = 0.0
    gradient.setflags(write=False)
    return gradient


def reconstruct_longitudinal_relative_velocity(
    *,
    regional_or_wall_geometry: RegionalDomainSpec,
    boost_closure: BoostClosure,
    boundary_policy: BoundaryKernelPolicy,
    zero_mode_closure: RegionalZeroModeClosure,
    numerics: Phase1FANumerics,
) -> LongitudinalRelativeVelocityResult:
    """Reconstruct only ``v_dw,L^a=D^a psi_dw`` from an external closure.

    For divergence input, ``D_a D^a psi_dw=vartheta_dw`` is the explicit
    human-approved Phase 1F-A section 13 equation.  It is not a Timescape
    prediction and has no paper equation number.  The spatial-derivative
    convention is compatible with GM Eqs. (2.9)--(2.11).  No zero-boost,
    transverse, tracer, line-of-sight, or redshift-space closure is supplied.
    """
    regional_or_wall_geometry.validate_integrity()
    if boost_closure is None:
        raise Phase1FAContractError("an explicit boost closure is required")
    boost_closure.validate_integrity()
    if boost_closure.domain != regional_or_wall_geometry.region:
        raise Phase1FAContractError("boost closure domain does not match geometry")
    if boost_closure.normalization_closure_id != zero_mode_closure.provenance:
        raise Phase1FAContractError("boost normalization provenance does not match")
    expected_metric = regional_or_wall_geometry.geometry.normalization.normalization_id
    if boost_closure.spatial_metric_identity != expected_metric:
        raise Phase1FAContractError("boost spatial metric identity does not match geometry")
    system = assemble_regional_elliptic_system(
        domain=regional_or_wall_geometry,
        boundary_policy=boundary_policy,
        numerics=numerics,
    )
    size = regional_or_wall_geometry.operator.size
    if isinstance(boost_closure, ExternalBoostDivergenceClosure):
        supplied_full = readonly_float(boost_closure.divergence, "boost divergence").reshape(-1)
        if supplied_full.shape != (size,):
            raise Phase1FAContractError("boost divergence must use the complete carrier grid")
        supplied_regional = supplied_full[system.regional_indices]
        potential_regional, _ = solve_regional_laplace_beltrami(
            source=supplied_regional,
            system=system,
            zero_mode_closure=zero_mode_closure,
            numerics=numerics,
        )
    elif isinstance(boost_closure, ExternalBoostPotentialClosure):
        potential_full_input = readonly_float(boost_closure.potential, "boost potential").reshape(-1)
        if potential_full_input.shape != (size,):
            raise Phase1FAContractError("boost potential must use the complete carrier grid")
        potential_regional = potential_full_input[system.regional_indices]
        physical_mass = system.mass_weights * zero_mode_closure.scale_factor**3
        mean = float(np.dot(physical_mass, potential_regional) / np.sum(physical_mass))
        if abs(mean) > numerics.mean_tolerance:
            raise Phase1FAContractError("external boost potential violates its mean-zero normalization")
        supplied_regional = apply_regional_laplace_beltrami(
            system=system, field=potential_regional
        )
    else:  # pragma: no cover - defensive against runtime type erasure.
        raise Phase1FAContractError("unsupported boost closure kind")
    reconstructed_regional = apply_regional_laplace_beltrami(
        system=system, field=potential_regional
    )
    residual = float(np.max(np.abs(reconstructed_regional - supplied_regional)))
    if residual > numerics.boost_residual_tolerance:
        raise Phase1FAContractError("longitudinal boost divergence residual exceeds tolerance")
    potential_full = embed_regional_field(system=system, regional_field=potential_regional)
    reconstructed_full = embed_regional_field(
        system=system, regional_field=reconstructed_regional
    )
    supplied_full = embed_regional_field(system=system, regional_field=supplied_regional)
    classification = (
        LONGITUDINAL_RELATIVE_DUST_TO_WALL_VELOCITY
        if regional_or_wall_geometry.operator.carrier.dimension == 3
        else MATHEMATICAL_OPERATOR_FIXTURE_ONLY
    )
    return LongitudinalRelativeVelocityResult(
        scalar_potential=potential_full,
        longitudinal_relative_dust_to_wall_velocity=_regional_gradient(
            domain=regional_or_wall_geometry, potential_full=potential_full
        ),
        reconstructed_divergence=reconstructed_full,
        supplied_divergence=supplied_full,
        boost_residual_max_abs=residual,
        closure_kind=boost_closure.closure_kind,
        source_frame=boost_closure.source_frame,
        destination_frame=boost_closure.destination_frame,
        time_coordinate=boost_closure.time_coordinate,
        spatial_metric_identity=boost_closure.spatial_metric_identity,
        units=boost_closure.units,
        provenance=boost_closure.provenance,
        scientific_classification=classification,
        transverse_sector_status=TRANSVERSE_SECTOR_UNRESOLVED,
        domain=regional_or_wall_geometry,
    )
