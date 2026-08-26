"""Conditional Phase 1F-B scalar-normal dust-to-wall boost propagation.

Implemented scientific chain:

* ``Z_w = Delta_gamma_w deltaTheta_d,w`` from GM Eqs. (2.20)--(2.24);
* ``Theta_W = Theta_d + D_a xi^a`` under the destination-minus-source
  convention audited against BDE Eqs. (14)--(16) and DBE Eqs. (14)--(15),
  so ``D^2 psi = deltaTheta_d,w - deltaTheta_W`` for
  ``u_d = u_W + D psi``;
* ``A_W + dot(v) + H_W v = 0`` from the same first-order acceleration
  transformation with dust geodesicity from GM Eq. (2.9);
* ``dot(psi) = -Q0 nu_W`` in the explicitly approved scalar-normal
  representative.

The common spacetime, wall congruence, lapse perturbation, wall expansion,
boundary model, normalization, and initial data are external closures.  No
background Timescape lapse or observational velocity enters this module.
"""

from __future__ import annotations

import numpy as np

from timescape_fsigma8.phase1f_a import (
    NO_FLUX_REGIONAL_INTERFACE_PERIODIC_CARRIER,
    REGIONAL_SOURCE_MEAN_ZERO,
    SINGLE_REGIONAL_CONSTANT_REMOVED,
    BoundaryKernelPolicy,
    Phase1FAContractError,
    Phase1FADegeneracyError,
)
from timescape_fsigma8.phase1f_a.boost import _regional_gradient
from timescape_fsigma8.phase1f_a.operators import (
    apply_regional_laplace_beltrami,
    assemble_regional_elliptic_system,
    embed_regional_field,
    solve_regional_laplace_beltrami,
)
from timescape_fsigma8.phase1f_b.models import (
    CONDITIONAL_SCALAR_DUST_TO_WALL_BOOST,
    MATHEMATICAL_OPERATOR_FIXTURE_ONLY,
    REALIZATION_ID,
    TRANSVERSE_SECTOR_EXCLUDED,
    TRANSVERSE_ZERO_NOT_GRANTED,
    BoostInitializationMode,
    LapseKernelMode,
    Phase1FBCompatibilityError,
    Phase1FBContractError,
    Phase1FBGeometryClosureError,
    Phase1FBKernelCompatibilityError,
    Phase1FBLinearRegimeError,
    Phase1FBPropagationError,
    ScalarDustWallBoostDiagnostics,
    ScalarDustWallBoostNumerics,
    ScalarDustWallBoostResult,
    ScalarDustWallBoostScenario,
)


def _phase1f_a_boundary(scenario: ScalarDustWallBoostScenario) -> BoundaryKernelPolicy:
    """Adapt an explicit boost BC to the frozen regional matrix implementation."""
    return BoundaryKernelPolicy(
        domain="wall",
        boundary_condition_kind=NO_FLUX_REGIONAL_INTERFACE_PERIODIC_CARRIER,
        nullspace_handling=SINGLE_REGIONAL_CONSTANT_REMOVED,
        compatibility_condition=REGIONAL_SOURCE_MEAN_ZERO,
        provenance=f"BOOST_SPECIFIC:{scenario.boundary_policy.provenance}",
    )


def _weighted_mean(values: np.ndarray, mass: np.ndarray) -> float:
    return float(np.dot(mass, values) / np.sum(mass))


def _worst_scalar(residual: np.ndarray) -> tuple[float, tuple[int, ...]]:
    absolute = np.abs(residual)
    flat = int(np.argmax(absolute))
    return float(absolute.reshape(-1)[flat]), np.unravel_index(flat, absolute.shape)


def _worst_vector(residual: np.ndarray) -> tuple[float, tuple[int, ...]]:
    magnitude = np.linalg.norm(residual, axis=-1)
    flat = int(np.argmax(magnitude))
    return float(magnitude.reshape(-1)[flat]), np.unravel_index(flat, magnitude.shape)


def _physical_orthonormal_gradient(
    *, domain, scalar_field: np.ndarray, scale_factor: float
) -> np.ndarray:
    """Return physical orthonormal gradient components on the fixed metric.

    BDE Eq. (74) and footnote 22 give the physical/comoving ``a^-2``
    Laplacian relation.  If ``q^i=gamma^ij partial_j f`` is the existing
    reference contravariant gradient, ``L^T partial f / a`` with
    ``gamma^-1=L L^T`` has the physical norm
    ``|D f|^2=a^-2 gamma^ij partial_i f partial_j f``.
    """
    reference_contravariant = _regional_gradient(
        domain=domain, potential_full=scalar_field
    )
    dimension = domain.operator.carrier.dimension
    inverse_metric = domain.geometry.metric_inverse.reshape(
        (domain.operator.size, dimension, dimension)
    )
    covector = np.linalg.solve(inverse_metric, reference_contravariant[..., None])[
        ..., 0
    ]
    cholesky = np.linalg.cholesky(inverse_metric)
    result = np.einsum("nji,nj->ni", cholesky, covector, optimize=True)
    result /= scale_factor
    result[~domain.mask, :] = 0.0
    return result


def propagate_scalar_dust_wall_boost(
    *,
    scenario: ScalarDustWallBoostScenario,
    numerics: ScalarDustWallBoostNumerics,
) -> ScalarDustWallBoostResult:
    """Propagate the selected conditional scalar dust-to-wall boost.

    The comoving regional operator obeys
    ``L_w=a_w^2 D_w^2=Delta_gamma_w`` (GM Eqs. (2.2),
    (2.20)--(2.24), with the physical/comoving harmonic distinction in BDE
    Eq. (74) and footnote 22).  Therefore the sign-sensitive constraint is
    ``L_w psi=a_w^2(deltaTheta_d,w-deltaTheta_W)``.  The time update uses
    the approved normalized scalar law ``dot(psi)=-Q0 nu_W`` derived from
    the BDE Eqs. (14)--(16) frame law and GM Eq. (2.9) dust geodesicity.
    """
    if not isinstance(scenario, ScalarDustWallBoostScenario):
        raise Phase1FBContractError("explicit ScalarDustWallBoostScenario required")
    if not isinstance(numerics, ScalarDustWallBoostNumerics):
        raise Phase1FBContractError("explicit ScalarDustWallBoostNumerics required")
    numerics.validate_integrity()
    scenario.validate_integrity()
    closure = scenario.geometry_closure
    domain = closure.wall_domain
    operator = domain.operator
    mask = domain.mask
    outside = ~mask
    if np.max(np.abs(closure.wall_expansion_perturbation[:, outside])) > numerics.off_domain_tolerance:
        raise Phase1FBGeometryClosureError("wall expansion has support outside wall domain")
    if np.max(np.abs(closure.wall_lapse_perturbation[:, outside])) > numerics.off_domain_tolerance:
        raise Phase1FBGeometryClosureError("wall lapse has support outside wall domain")

    time = closure.time_grid
    scale = closure.wall_scale_factor
    hubble = closure.wall_hubble_rate
    dt = np.diff(time)
    # H_W=d ln(a_w)/dt is the background part of the acceleration-frame law;
    # the identity follows W09 Eq. (28), while this common-time grid is an
    # explicit external Phase 1F-B closure.
    rate_residual = np.log(scale[1:] / scale[:-1]) / dt - 0.5 * (
        hubble[1:] + hubble[:-1]
    )
    rate_max = float(np.max(np.abs(rate_residual)))
    if rate_max > numerics.scale_factor_rate_tolerance:
        raise Phase1FBGeometryClosureError(
            "wall scale factor and Hubble driver are inconsistent"
        )
    if abs(scenario.zero_mode_closure.scale_factor - scale[0]) > numerics.scale_factor_rate_tolerance:
        raise Phase1FBGeometryClosureError(
            "initial regional scale factor does not match zero-mode closure"
        )

    system = assemble_regional_elliptic_system(
        domain=domain,
        boundary_policy=_phase1f_a_boundary(scenario),
        numerics=scenario.regional_elliptic_numerics,
    )
    regional = system.regional_indices
    mass_reference = system.mass_weights
    nt = time.size
    lapse_regional = closure.wall_lapse_perturbation[:, regional]
    projected_lapse = np.empty_like(lapse_regional)
    raw_means = np.empty(nt, dtype=np.float64)
    for index in range(nt):
        physical_mass = mass_reference * scale[index] ** 3
        raw_means[index] = _weighted_mean(lapse_regional[index], physical_mass)
        if scenario.lapse_kernel_mode is LapseKernelMode.REQUIRE_MEAN_ZERO:
            if abs(raw_means[index]) > numerics.lapse_mean_tolerance:
                raise Phase1FBKernelCompatibilityError(
                    "wall lapse violates declared mean-zero kernel representative"
                )
            projected_lapse[index] = lapse_regional[index]
        else:
            projected_lapse[index] = lapse_regional[index] - raw_means[index]

    dust_regional = np.stack(
        [item.regional_values for item in scenario.dust_expansion_history]
    )
    wall_regional = closure.wall_expansion_perturbation[:, regional]
    difference = dust_regional - wall_regional
    potential = np.empty_like(difference)
    if scenario.initialization_mode is BoostInitializationMode.SUPPLIED_INITIAL_BOOST:
        if scenario.initial_scalar_potential is None:
            raise Phase1FBContractError(
                "validated supplied-initial-boost state lost its potential"
            )
        potential[0] = scenario.initial_scalar_potential[regional]
        if (
            np.max(np.abs(scenario.initial_scalar_potential[outside]))
            > numerics.off_domain_tolerance
        ):
            raise Phase1FBKernelCompatibilityError(
                "supplied initial boost has support outside wall domain"
            )
        initial_mass = mass_reference * scale[0] ** 3
        initial_mean = _weighted_mean(potential[0], initial_mass)
        if abs(initial_mean) > numerics.potential_mean_tolerance:
            raise Phase1FBKernelCompatibilityError(
                "supplied initial boost violates mean-zero representative"
            )
    else:
        source = scale[0] ** 2 * difference[0]
        try:
            potential[0], _ = solve_regional_laplace_beltrami(
                source=source,
                system=system,
                zero_mode_closure=scenario.zero_mode_closure,
                numerics=scenario.regional_elliptic_numerics,
            )
        except (Phase1FAContractError, Phase1FADegeneracyError) as exc:
            raise Phase1FBKernelCompatibilityError(
                "expansion-matched initial source violates boost kernel contract"
            ) from exc
    for index, step in enumerate(dt):
        potential[index + 1] = potential[index] - 0.5 * step * (
            projected_lapse[index] + projected_lapse[index + 1]
        )

    potential_dot_regional = -projected_lapse
    laplacian_regional = np.stack(
        [apply_regional_laplace_beltrami(system=system, field=row) for row in potential]
    )
    physical_laplacian_regional = laplacian_regional / scale[:, np.newaxis] ** 2
    compatibility_regional = difference - physical_laplacian_regional
    compatibility_max, compatibility_where = _worst_scalar(compatibility_regional)
    compatibility_scale = max(
        float(np.max(np.abs(difference))), numerics.residual_norm_floor
    )
    compatibility_normalized = compatibility_max / compatibility_scale
    if compatibility_max > numerics.expansion_compatibility_tolerance:
        raise Phase1FBCompatibilityError(
            "expansion-difference compatibility residual exceeds tolerance"
        )

    potential_full = np.stack(
        [embed_regional_field(system=system, regional_field=row) for row in potential]
    )
    potential_dot_full = np.stack(
        [embed_regional_field(system=system, regional_field=row) for row in potential_dot_regional]
    )
    projected_lapse_full = np.stack(
        [embed_regional_field(system=system, regional_field=row) for row in projected_lapse]
    )
    physical_laplacian_full = np.stack(
        [embed_regional_field(system=system, regional_field=row) for row in physical_laplacian_regional]
    )
    compatibility_full = np.stack(
        [embed_regional_field(system=system, regional_field=row) for row in compatibility_regional]
    )

    velocity = np.stack(
        [
            _physical_orthonormal_gradient(
                domain=domain, scalar_field=potential_full[index], scale_factor=scale[index]
            )
            for index in range(nt)
        ]
    )
    acceleration = np.stack(
        [
            _physical_orthonormal_gradient(
                domain=domain,
                scalar_field=projected_lapse_full[index],
                scale_factor=scale[index],
            )
            for index in range(nt)
        ]
    )
    propagation = (
        (velocity[1:] - velocity[:-1]) / dt[:, np.newaxis, np.newaxis]
        + 0.5 * (hubble[1:] + hubble[:-1])[:, np.newaxis, np.newaxis]
        * 0.5
        * (velocity[1:] + velocity[:-1])
        + 0.5 * (acceleration[1:] + acceleration[:-1])
    )
    propagation_max, propagation_where = _worst_vector(propagation)
    propagation_scale = max(
        float(np.max(np.linalg.norm(acceleration, axis=-1))),
        float(np.max(np.abs(hubble[:, np.newaxis]) * np.linalg.norm(velocity, axis=-1))),
        numerics.residual_norm_floor,
    )
    propagation_normalized = propagation_max / propagation_scale
    if propagation_max > numerics.propagation_residual_tolerance:
        raise Phase1FBPropagationError(
            "dust-geodesic propagation residual exceeds tolerance"
        )

    potential_means = np.array(
        [
            _weighted_mean(potential[index], mass_reference * scale[index] ** 3)
            for index in range(nt)
        ]
    )
    potential_mean_max = float(np.max(np.abs(potential_means)))
    if potential_mean_max > numerics.potential_mean_tolerance:
        raise Phase1FBKernelCompatibilityError(
            "propagated potential left its mean-zero representative"
        )
    velocity_ratio = float(
        np.max(np.linalg.norm(velocity, axis=-1)) / numerics.speed_of_light
    )
    if velocity_ratio >= numerics.linear_velocity_ratio_threshold:
        raise Phase1FBLinearRegimeError(
            "relative dust-to-wall velocity violates the explicit linear-regime gate"
        )

    propagation_full = np.zeros(
        (nt - 1, operator.size, operator.carrier.dimension), dtype=np.float64
    )
    propagation_full[:, regional, :] = propagation[:, regional, :]
    classification = (
        CONDITIONAL_SCALAR_DUST_TO_WALL_BOOST
        if operator.carrier.dimension == 3
        else MATHEMATICAL_OPERATOR_FIXTURE_ONLY
    )
    diagnostics = ScalarDustWallBoostDiagnostics(
        expansion_compatibility_max_abs=compatibility_max,
        expansion_compatibility_normalized_linf=compatibility_normalized,
        expansion_compatibility_tolerance=numerics.expansion_compatibility_tolerance,
        expansion_compatibility_worst_time=float(time[compatibility_where[0]]),
        expansion_compatibility_worst_spatial_index=int(regional[compatibility_where[1]]),
        propagation_residual_max_abs=propagation_max,
        propagation_residual_normalized_linf=propagation_normalized,
        propagation_residual_tolerance=numerics.propagation_residual_tolerance,
        propagation_worst_time=float(
            0.5 * (time[propagation_where[0]] + time[propagation_where[0] + 1])
        ),
        propagation_worst_spatial_index=int(regional[propagation_where[1]]),
        potential_mean_max_abs=potential_mean_max,
        lapse_raw_mean_max_abs=float(np.max(np.abs(raw_means))),
        lapse_q0_correction_max_abs=(
            float(np.max(np.abs(raw_means)))
            if scenario.lapse_kernel_mode is LapseKernelMode.EXPLICIT_Q0_PROJECTION
            else 0.0
        ),
        scale_factor_rate_residual_max_abs=rate_max,
        maximum_velocity_to_light_speed_ratio=velocity_ratio,
        linear_velocity_ratio_threshold=numerics.linear_velocity_ratio_threshold,
        curl_status="CONSTRUCTION_INVARIANT_NOT_INDEPENDENT_NUMERICAL_EVIDENCE",
        dimensional_contract_status=(
            "CONDITIONAL_PHYSICAL_3D_ONLY"
            if operator.carrier.dimension == 3
            else MATHEMATICAL_OPERATOR_FIXTURE_ONLY
        ),
        state_integrity_status="VALIDATED_FAIL_CLOSED",
    )
    result = ScalarDustWallBoostResult(
        time_grid=time,
        scalar_potential=potential_full,
        scalar_potential_time_derivative=potential_dot_full,
        projected_wall_lapse_perturbation=projected_lapse_full,
        dust_velocity_relative_to_wall=velocity,
        physical_laplacian_of_potential=physical_laplacian_full,
        expansion_compatibility_residual=compatibility_full,
        propagation_geodesic_residual=propagation_full,
        diagnostics=diagnostics,
        scenario=scenario,
        numerics=numerics,
        realization_id=REALIZATION_ID,
        scientific_classification=classification,
        transverse_sector_status=TRANSVERSE_SECTOR_EXCLUDED,
        transverse_zero_as_timescape_prediction=TRANSVERSE_ZERO_NOT_GRANTED,
        conditional_forward_uniqueness="GRANTED",
        unique_from_frozen_y_alone="NOT_GRANTED",
        unique_timescape_prediction="NOT_GRANTED",
        observational_authorization="NOT_GRANTED",
        scalar_potential_units="REFERENCE_LENGTH_SQUARED_PER_COMMON_TIME",
        velocity_units="REFERENCE_LENGTH_PER_COMMON_TIME",
        scalar_potential_time_derivative_units=(
            "REFERENCE_LENGTH_SQUARED_PER_COMMON_TIME_SQUARED"
        ),
        velocity_component_representation=(
            "WALL_REFERENCE_METRIC_ORTHONORMAL_CHOLESKY_COMPONENTS"
        ),
    )
    result.validate_integrity()
    return result
