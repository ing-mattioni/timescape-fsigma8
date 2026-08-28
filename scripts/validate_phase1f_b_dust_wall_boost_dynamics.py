"""Deterministic synthetic validation for conditional Phase 1F-B dynamics.

No fixture in this script has observational, tracer, RSD, interface-material,
or unique Timescape-prediction semantics.
"""

from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path

import numpy as np

from timescape_fsigma8.phase1f_a.operators import (
    apply_regional_laplace_beltrami,
    assemble_regional_elliptic_system,
)

from validate_phase1f_a_h1_closure import (
    boundary as phase1f_a_boundary,
    domain,
    fields,
    make_realization,
    numerics as phase1f_a_numerics,
    supported,
    zero_mode,
)
from timescape_fsigma8.phase1f_b import (
    BOOST_BOUNDARY_RUNTIME_ENFORCEMENT,
    BOOST_SPECIFIC_BOUNDARY_MODEL,
    EXPLICIT_EXTERNAL_NO_PENETRATION_CLOSURE,
    EXPANSION_COMPATIBILITY_EVIDENCE,
    HARMONIC_VECTOR_SECTOR_EXCLUDED,
    HARMONIC_VECTOR_ZERO_NOT_GRANTED,
    PERTURBATIVE_WALL_LAPSE_POTENTIAL,
    PROPAGATION_CONSTRUCTION_DIAGNOSTIC,
    SYNTHETIC_VALIDATION_ONLY,
    TIME_INTEGRATOR_CONVERGENCE_CLASSIFICATION,
    WALL_BACKGROUND_SHEAR_EXCLUDED,
    WALL_PROPER_TIME_RATE_ROLE,
    BoostBoundaryKernelPolicy,
    BoostBoundaryKind,
    BoostGeometryProvenance,
    BoostInitializationMode,
    CommonSpacetimeWallGeometryClosure,
    LapseKernelMode,
    Phase1FBCompatibilityError,
    Phase1FBContractError,
    Phase1FBGeometryClosureError,
    Phase1FBKernelCompatibilityError,
    Phase1FBLinearRegimeError,
    ScalarBoostSector,
    ScalarDustWallBoostNumerics,
    ScalarDustWallBoostScenario,
    WallBackgroundGeometrySector,
    propagate_scalar_dust_wall_boost,
)


OUTPUT_DEFAULT = Path(
    "artifacts/independent/phase1f_b_dust_wall_boost_dynamics_validation.json"
)


def numerics(
    *, propagation_tolerance: float = 2e-10, linear_threshold: float = 0.1
) -> ScalarDustWallBoostNumerics:
    return ScalarDustWallBoostNumerics(
        expansion_compatibility_tolerance=5e-10,
        propagation_residual_tolerance=propagation_tolerance,
        potential_mean_tolerance=2e-11,
        lapse_mean_tolerance=2e-11,
        scale_factor_rate_tolerance=2e-11,
        off_domain_tolerance=2e-14,
        boundary_normal_velocity_tolerance=2e-11,
        boundary_normal_acceleration_tolerance=2e-11,
        boundary_normal_velocity_tolerance_units=(
            "REFERENCE_LENGTH_PER_COMMON_TIME"
        ),
        boundary_normal_acceleration_tolerance_units="INVERSE_COMMON_TIME",
        linear_velocity_ratio_threshold=linear_threshold,
        speed_of_light=1.0,
        speed_of_light_units="REFERENCE_LENGTH_PER_COMMON_TIME",
        residual_norm_floor=1e-14,
        integration_method="EXPLICIT_TRAPEZOIDAL_COMMON_TIME_GRID",
    )


def boost_boundary() -> BoostBoundaryKernelPolicy:
    return BoostBoundaryKernelPolicy(
        domain_id="wall",
        boundary_kind=BoostBoundaryKind.WALL_INTERIOR_NO_FLUX_PERIODIC_TANGENTIAL,
        nullspace_handling="SINGLE_WALL_CONSTANT_REMOVED",
        compatibility_condition="WALL_SOURCE_MEAN_ZERO",
        provenance="EXPLICIT_VALIDATION_BOOST_BOUNDARY",
        classification=BOOST_SPECIFIC_BOUNDARY_MODEL,
        physical_boundary_condition=EXPLICIT_EXTERNAL_NO_PENETRATION_CLOSURE,
        derived_from_timescape=False,
        inherited_from_h1_density_transmission=False,
        physical_interface_claim="NOT_GRANTED",
    )


def expansion_history(runtime, amplitudes: np.ndarray):
    shape = runtime.scientific_state.operator.carrier.grid_shape
    _, laplacian, _ = fields(shape)
    return tuple(
        runtime.reconstruct_expansion(
            z_cgi=supported(runtime, amplitude * laplacian, "wall"),
            regional_geometry=domain(runtime, "wall"),
            boundary_policy=phase1f_a_boundary("wall"),
            zero_mode_closure=zero_mode("wall"),
            background_expansion_identity="bar_Theta_d,w=3H_d,w",
            provenance=f"PHASE1F_B_SYNTHETIC_DUST_EXPANSION_{index}",
        )
        for index, amplitude in enumerate(amplitudes)
    )


def scenario(
    *,
    time: np.ndarray,
    potential_amplitudes: np.ndarray,
    lapse_amplitudes: np.ndarray,
    dust_amplitudes: np.ndarray,
    scale_factor: np.ndarray,
    hubble: np.ndarray,
    initialization_mode: BoostInitializationMode,
    lapse_kernel_mode: LapseKernelMode,
    reverse_sign: bool = False,
):
    runtime = make_realization((4, 4, 4))
    scalar, laplacian, _ = fields((4, 4, 4))
    mask = runtime.scientific_state.operator.morphology.wall_domain.reshape(-1)
    dust = dust_amplitudes[:, None] * scalar.reshape(1, -1)
    physical_laplacian = (
        potential_amplitudes[:, None]
        * laplacian.reshape(1, -1)
        / scale_factor[:, None] ** 2
    )
    wall = dust + (1.0 if reverse_sign else -1.0) * physical_laplacian
    lapse = lapse_amplitudes[:, None] * scalar.reshape(1, -1)
    wall[:, ~mask] = 0.0
    lapse[:, ~mask] = 0.0
    boost_zero_mode = replace(
        zero_mode("wall"), scale_factor=float(scale_factor[0])
    )
    closure = CommonSpacetimeWallGeometryClosure(
        wall_domain=domain(runtime, "wall"),
        common_spacetime_id="SYNTHETIC_COMMON_SPACETIME_PHASE1F_B_VALIDATION",
        wall_congruence_id="SYNTHETIC_NORMAL_WALL_OBSERVER",
        regional_wall_dust_congruence_id="REGIONAL_WALL_DUST_CONGRUENCE",
        h1_wall_embedding_id=runtime.scientific_state.operator.morphology.wall_pullback_id,
        common_time_coordinate_id="SYNTHETIC_COMMON_TIME_T",
        wall_proper_time_mapping_id="EXPLICIT_SYNTHETIC_DTAU_W_DT",
        spatial_geometry_operator_id="wall-validation",
        dust_expansion_background_identity="bar_Theta_d,w=3H_d,w",
        domain_id="wall",
        time_grid=time,
        wall_scale_factor=scale_factor,
        wall_hubble_rate=hubble,
        wall_proper_time_rate=np.ones(time.size),
        wall_proper_time_rate_role=WALL_PROPER_TIME_RATE_ROLE,
        wall_expansion_perturbation=wall,
        wall_lapse_perturbation=lapse,
        lapse_driver_kind=PERTURBATIVE_WALL_LAPSE_POTENTIAL,
        common_time_units="COMMON_TIME",
        wall_expansion_units="INVERSE_COMMON_TIME",
        wall_hubble_units="INVERSE_COMMON_TIME",
        wall_scale_factor_units="DIMENSIONLESS",
        wall_lapse_units="DIMENSIONLESS_PERTURBATION",
        unit_system="GEOMETRIZED_C_EQUALS_ONE",
        interpolation_policy="PIECEWISE_LINEAR_NO_EXTRAPOLATION",
        provenance=BoostGeometryProvenance.SYNTHETIC_VALIDATION_ONLY,
        selected_background_geometry_sector=(
            WallBackgroundGeometrySector.SHEAR_FREE_QUASI_FLRW_COMMON_SPACETIME
        ),
        scalar_hypersurface_orthogonal=True,
        vorticity_dust_zero=True,
        vorticity_wall_zero=True,
        wall_background_shear_free=True,
        normalization_kernel_identity=boost_zero_mode.provenance,
        scientific_classification=SYNTHETIC_VALIDATION_ONLY,
    )
    initial = (
        supported(runtime, potential_amplitudes[0] * scalar, "wall")
        if initialization_mode is BoostInitializationMode.SUPPLIED_INITIAL_BOOST
        else None
    )
    return ScalarDustWallBoostScenario(
        geometry_closure=closure,
        dust_expansion_history=expansion_history(runtime, dust_amplitudes),
        dust_expansion_time_grid=time,
        dust_expansion_time_coordinate_id="SYNTHETIC_COMMON_TIME_T",
        regional_elliptic_numerics=phase1f_a_numerics(),
        initialization_mode=initialization_mode,
        initial_scalar_potential=initial,
        initial_potential_provenance=(
            "SUPPLIED_SYNTHETIC_INITIAL_BOOST"
            if initial is not None
            else "EXPANSION_MATCHED_SYNTHETIC_INITIAL_BOOST"
        ),
        initial_potential_units="REFERENCE_LENGTH_SQUARED_PER_COMMON_TIME",
        boundary_policy=boost_boundary(),
        zero_mode_closure=boost_zero_mode,
        lapse_kernel_mode=lapse_kernel_mode,
        requested_sector=ScalarBoostSector.SCALAR_LONGITUDINAL_HYPERSURFACE_ORTHOGONAL,
        scientific_classification=SYNTHETIC_VALIDATION_ONLY,
    )


def normal_varying_scenario(
    *, initial_profile: np.ndarray, lapse_profile: np.ndarray
) -> tuple[ScalarDustWallBoostScenario, np.ndarray, float]:
    """Create the genuine 3-D normal-varying boundary validation fixture."""
    shape = (8, 4, 4)
    time = np.array([0.0, 0.25, 0.5], dtype=np.float64)
    runtime = make_realization(shape)
    wall_domain = domain(runtime, "wall")
    mask_grid = wall_domain.mask.reshape(shape)
    wall_x = np.flatnonzero(np.any(mask_grid, axis=(1, 2)))
    initial_grid = np.zeros(shape, dtype=np.float64)
    lapse_grid = np.zeros(shape, dtype=np.float64)
    initial_grid[wall_x, :, :] = initial_profile[:, None, None]
    lapse_grid[wall_x, :, :] = lapse_profile[:, None, None]
    initial_full = (0.002 * initial_grid).reshape(-1)
    lapse_amplitude = np.array([0.0, 1.0e-4, 2.0e-4], dtype=np.float64)
    lapse_full = lapse_amplitude[:, None] * lapse_grid.reshape(1, -1)
    potential_full = np.empty_like(lapse_full)
    potential_full[0] = initial_full
    for index, step in enumerate(np.diff(time)):
        potential_full[index + 1] = potential_full[index] - 0.5 * step * (
            lapse_full[index] + lapse_full[index + 1]
        )

    dust_history = expansion_history(runtime, np.full(time.size, 0.01))
    system = assemble_regional_elliptic_system(
        domain=wall_domain,
        boundary_policy=phase1f_a_boundary("wall"),
        numerics=phase1f_a_numerics(),
    )
    wall_expansion = np.zeros_like(lapse_full)
    for index, expansion in enumerate(dust_history):
        laplacian = apply_regional_laplace_beltrami(
            system=system,
            field=potential_full[index, system.regional_indices],
        )
        wall_expansion[index, system.regional_indices] = (
            expansion.regional_values - laplacian
        )
    boost_zero_mode = zero_mode("wall")
    closure = CommonSpacetimeWallGeometryClosure(
        wall_domain=wall_domain,
        common_spacetime_id="SYNTHETIC_NORMAL_VARYING_COMMON_SPACETIME",
        wall_congruence_id="SYNTHETIC_NORMAL_WALL_OBSERVER",
        regional_wall_dust_congruence_id="REGIONAL_WALL_DUST_CONGRUENCE",
        h1_wall_embedding_id=(
            runtime.scientific_state.operator.morphology.wall_pullback_id
        ),
        common_time_coordinate_id="SYNTHETIC_COMMON_TIME_T",
        wall_proper_time_mapping_id="EXPLICIT_SYNTHETIC_DTAU_W_DT",
        spatial_geometry_operator_id="wall-validation",
        dust_expansion_background_identity="bar_Theta_d,w=3H_d,w",
        domain_id="wall",
        time_grid=time,
        wall_scale_factor=np.ones(time.size),
        wall_hubble_rate=np.zeros(time.size),
        wall_proper_time_rate=np.ones(time.size),
        wall_proper_time_rate_role=WALL_PROPER_TIME_RATE_ROLE,
        wall_expansion_perturbation=wall_expansion,
        wall_lapse_perturbation=lapse_full,
        lapse_driver_kind=PERTURBATIVE_WALL_LAPSE_POTENTIAL,
        common_time_units="COMMON_TIME",
        wall_expansion_units="INVERSE_COMMON_TIME",
        wall_hubble_units="INVERSE_COMMON_TIME",
        wall_scale_factor_units="DIMENSIONLESS",
        wall_lapse_units="DIMENSIONLESS_PERTURBATION",
        unit_system="GEOMETRIZED_C_EQUALS_ONE",
        interpolation_policy="PIECEWISE_LINEAR_NO_EXTRAPOLATION",
        provenance=BoostGeometryProvenance.SYNTHETIC_VALIDATION_ONLY,
        selected_background_geometry_sector=(
            WallBackgroundGeometrySector.SHEAR_FREE_QUASI_FLRW_COMMON_SPACETIME
        ),
        scalar_hypersurface_orthogonal=True,
        vorticity_dust_zero=True,
        vorticity_wall_zero=True,
        wall_background_shear_free=True,
        normalization_kernel_identity=boost_zero_mode.provenance,
        scientific_classification=SYNTHETIC_VALIDATION_ONLY,
    )
    item = ScalarDustWallBoostScenario(
        geometry_closure=closure,
        dust_expansion_history=dust_history,
        dust_expansion_time_grid=time,
        dust_expansion_time_coordinate_id="SYNTHETIC_COMMON_TIME_T",
        regional_elliptic_numerics=phase1f_a_numerics(),
        initialization_mode=BoostInitializationMode.SUPPLIED_INITIAL_BOOST,
        initial_scalar_potential=initial_full,
        initial_potential_provenance="SUPPLIED_NORMAL_VARYING_INITIAL_BOOST",
        initial_potential_units="REFERENCE_LENGTH_SQUARED_PER_COMMON_TIME",
        boundary_policy=boost_boundary(),
        zero_mode_closure=boost_zero_mode,
        lapse_kernel_mode=LapseKernelMode.REQUIRE_MEAN_ZERO,
        requested_sector=(
            ScalarBoostSector.SCALAR_LONGITUDINAL_HYPERSURFACE_ORTHOGONAL
        ),
        scientific_classification=SYNTHETIC_VALIDATION_ONLY,
    )
    field = potential_full[0].reshape(shape)
    unbroken = np.zeros(shape, dtype=np.float64)
    for axis, spacing in enumerate(
        runtime.scientific_state.operator.carrier.grid_spacing
    ):
        unbroken += (
            np.roll(field, 1, axis=axis)
            - 2.0 * field
            + np.roll(field, -1, axis=axis)
        ) / spacing**2
    broken = np.zeros(np.prod(shape), dtype=np.float64)
    broken[system.regional_indices] = apply_regional_laplace_beltrami(
        system=system,
        field=potential_full[0, system.regional_indices],
    )
    distinction = float(
        np.max(
            np.abs(
                broken[wall_domain.mask]
                - unbroken.reshape(-1)[wall_domain.mask]
            )
        )
    )
    return item, potential_full, distinction


def _rejected(callable_) -> bool:
    try:
        callable_()
    except (Phase1FBContractError, TypeError):
        return True
    return False


def validate() -> dict[str, object]:
    time = np.linspace(0.0, 1.0, 5)
    zero_driver = scenario(
        time=time,
        potential_amplitudes=np.full(time.size, 0.002),
        lapse_amplitudes=np.zeros(time.size),
        dust_amplitudes=np.full(time.size, 0.01),
        scale_factor=np.ones(time.size),
        hubble=np.zeros(time.size),
        initialization_mode=BoostInitializationMode.SUPPLIED_INITIAL_BOOST,
        lapse_kernel_mode=LapseKernelMode.REQUIRE_MEAN_ZERO,
    )
    zero_result = propagate_scalar_dust_wall_boost(
        scenario=zero_driver, numerics=numerics()
    )

    expected_amplitude = 0.002 + 0.001 * time - 0.0002 * time**2
    lapse_amplitude = -0.001 + 0.0004 * time
    manufactured = scenario(
        time=time,
        potential_amplitudes=expected_amplitude,
        lapse_amplitudes=lapse_amplitude,
        dust_amplitudes=np.full(time.size, 0.01),
        scale_factor=np.ones(time.size),
        hubble=np.zeros(time.size),
        initialization_mode=BoostInitializationMode.SUPPLIED_INITIAL_BOOST,
        lapse_kernel_mode=LapseKernelMode.EXPLICIT_Q0_PROJECTION,
    )
    manufactured_result = propagate_scalar_dust_wall_boost(
        scenario=manufactured, numerics=numerics()
    )
    scalar, _, _ = fields((4, 4, 4))
    mask = manufactured.geometry_closure.wall_domain.mask
    manufactured_error = float(
        np.max(
            np.abs(
                manufactured_result.scalar_potential[:, mask]
                - expected_amplitude[:, None] * scalar.reshape(-1)[mask]
            )
        )
    )
    expansion_matched = scenario(
        time=time,
        potential_amplitudes=expected_amplitude,
        lapse_amplitudes=lapse_amplitude,
        dust_amplitudes=np.full(time.size, 0.01),
        scale_factor=np.ones(time.size),
        hubble=np.zeros(time.size),
        initialization_mode=BoostInitializationMode.EXPANSION_MATCHED_INITIAL_BOOST,
        lapse_kernel_mode=LapseKernelMode.REQUIRE_MEAN_ZERO,
    )
    expansion_matched_result = propagate_scalar_dust_wall_boost(
        scenario=expansion_matched, numerics=numerics()
    )
    expansion_matched_initial_error = float(
        np.max(
            np.abs(
                expansion_matched_result.scalar_potential[0, mask]
                - expected_amplitude[0] * scalar.reshape(-1)[mask]
            )
        )
    )

    changed_wall = np.array(
        manufactured.geometry_closure.wall_expansion_perturbation, copy=True
    )
    changed_wall[2, mask] += 1e-4
    expansion_adversary = replace(
        manufactured,
        geometry_closure=replace(
            manufactured.geometry_closure,
            wall_expansion_perturbation=changed_wall,
        ),
    )
    compatibility_rejected = _rejected(
        lambda: propagate_scalar_dust_wall_boost(
            scenario=expansion_adversary, numerics=numerics()
        )
    )
    reversed_scenario = scenario(
        time=time,
        potential_amplitudes=expected_amplitude,
        lapse_amplitudes=lapse_amplitude,
        dust_amplitudes=np.full(time.size, 0.01),
        scale_factor=np.ones(time.size),
        hubble=np.zeros(time.size),
        initialization_mode=BoostInitializationMode.SUPPLIED_INITIAL_BOOST,
        lapse_kernel_mode=LapseKernelMode.REQUIRE_MEAN_ZERO,
        reverse_sign=True,
    )
    sign_reversed_rejected = _rejected(
        lambda: propagate_scalar_dust_wall_boost(
            scenario=reversed_scenario, numerics=numerics()
        )
    )
    background_lapse_rejected = _rejected(
        lambda: replace(
            manufactured.geometry_closure,
            lapse_driver_kind="BACKGROUND_TIMESCAPE_GAMMA_W",
        )
    )
    no_initial_mode_rejected = _rejected(
        lambda: replace(manufactured, initialization_mode=None)
    )
    transverse_rejected = _rejected(
        lambda: replace(manufactured, requested_sector="TRANSVERSE")
    )
    lapse_with_mean = np.array(
        manufactured.geometry_closure.wall_lapse_perturbation, copy=True
    )
    lapse_with_mean[:, mask] += 0.01
    kernel_bad = replace(
        manufactured,
        geometry_closure=replace(
            manufactured.geometry_closure,
            wall_lapse_perturbation=lapse_with_mean,
        ),
        lapse_kernel_mode=LapseKernelMode.REQUIRE_MEAN_ZERO,
    )
    kernel_rejected = _rejected(
        lambda: propagate_scalar_dust_wall_boost(
            scenario=kernel_bad, numerics=numerics()
        )
    )
    interface_inheritance_rejected = _rejected(
        lambda: replace(
            boost_boundary(), inherited_from_h1_density_transmission=True
        )
    )
    large = scenario(
        time=time,
        potential_amplitudes=np.ones(time.size),
        lapse_amplitudes=np.zeros(time.size),
        dust_amplitudes=np.full(time.size, 0.01),
        scale_factor=np.ones(time.size),
        hubble=np.zeros(time.size),
        initialization_mode=BoostInitializationMode.SUPPLIED_INITIAL_BOOST,
        lapse_kernel_mode=LapseKernelMode.REQUIRE_MEAN_ZERO,
    )
    linear_rejected = _rejected(
        lambda: propagate_scalar_dust_wall_boost(
            scenario=large, numerics=numerics(linear_threshold=0.01)
        )
    )
    scale_two = scenario(
        time=time,
        potential_amplitudes=np.full(time.size, 0.002),
        lapse_amplitudes=np.zeros(time.size),
        dust_amplitudes=np.full(time.size, 0.01),
        scale_factor=np.full(time.size, 2.0),
        hubble=np.zeros(time.size),
        initialization_mode=BoostInitializationMode.SUPPLIED_INITIAL_BOOST,
        lapse_kernel_mode=LapseKernelMode.REQUIRE_MEAN_ZERO,
    )
    scale_result = propagate_scalar_dust_wall_boost(
        scenario=scale_two, numerics=numerics()
    )
    _, laplacian, _ = fields((4, 4, 4))
    wrong_scale_wall = np.array(
        scale_two.geometry_closure.wall_expansion_perturbation, copy=True
    )
    wrong_scale_wall[:, mask] -= (
        0.002 * laplacian.reshape(-1)[mask] * (1.0 - 1.0 / 4.0)
    )
    wrong_scale_scenario = replace(
        scale_two,
        geometry_closure=replace(
            scale_two.geometry_closure,
            wall_expansion_perturbation=wrong_scale_wall,
        ),
    )
    wrong_scale_factor_rejected = _rejected(
        lambda: propagate_scalar_dust_wall_boost(
            scenario=wrong_scale_scenario, numerics=numerics()
        )
    )
    coarse_time = np.array([0.0, 1.0])
    coarse_propagation = scenario(
        time=coarse_time,
        potential_amplitudes=np.full(2, 0.002),
        lapse_amplitudes=np.zeros(2),
        dust_amplitudes=np.full(2, 0.01),
        scale_factor=np.exp(coarse_time),
        hubble=np.ones(2),
        initialization_mode=BoostInitializationMode.SUPPLIED_INITIAL_BOOST,
        lapse_kernel_mode=LapseKernelMode.REQUIRE_MEAN_ZERO,
    )
    propagation_residual_rejected = _rejected(
        lambda: propagate_scalar_dust_wall_boost(
            scenario=coarse_propagation,
            numerics=numerics(propagation_tolerance=1e-12),
        )
    )
    alignment_rejected = _rejected(
        lambda: replace(
            manufactured.geometry_closure,
            h1_wall_embedding_id="MISMATCHED_EMBEDDING",
        )
    )
    mutated = scenario(
        time=time,
        potential_amplitudes=expected_amplitude,
        lapse_amplitudes=lapse_amplitude,
        dust_amplitudes=np.full(time.size, 0.01),
        scale_factor=np.ones(time.size),
        hubble=np.zeros(time.size),
        initialization_mode=BoostInitializationMode.SUPPLIED_INITIAL_BOOST,
        lapse_kernel_mode=LapseKernelMode.REQUIRE_MEAN_ZERO,
    )
    object.__setattr__(mutated.geometry_closure, "wall_congruence_id", "MUTATED")
    mutation_rejected = _rejected(
        lambda: propagate_scalar_dust_wall_boost(
            scenario=mutated, numerics=numerics()
        )
    )

    admissible_profile = np.array([-1.0, -1.0, 1.0, 1.0])
    penetrating_profile = np.array([-1.5, -0.5, 0.5, 1.5])
    normal_admissible, expected_normal, broken_unbroken_difference = (
        normal_varying_scenario(
            initial_profile=admissible_profile,
            lapse_profile=admissible_profile,
        )
    )
    normal_result = propagate_scalar_dust_wall_boost(
        scenario=normal_admissible, numerics=numerics()
    )
    normal_potential_error = float(
        np.max(np.abs(normal_result.scalar_potential - expected_normal))
    )
    normal_bad_initial, _, _ = normal_varying_scenario(
        initial_profile=penetrating_profile,
        lapse_profile=np.zeros(4),
    )
    boundary_initial_rejected = _rejected(
        lambda: propagate_scalar_dust_wall_boost(
            scenario=normal_bad_initial, numerics=numerics()
        )
    )
    normal_bad_driver, _, _ = normal_varying_scenario(
        initial_profile=admissible_profile,
        lapse_profile=penetrating_profile,
    )
    boundary_driver_rejected = _rejected(
        lambda: propagate_scalar_dust_wall_boost(
            scenario=normal_bad_driver, numerics=numerics()
        )
    )
    nonzero_shear_rejected = _rejected(
        lambda: replace(
            manufactured.geometry_closure,
            wall_background_shear_free=False,
        )
    )

    convergence: list[dict[str, float | int]] = []
    for intervals in (4, 8, 16, 32):
        grid = np.linspace(0.0, 1.0, intervals + 1)
        exact = 0.002 + 0.0002 * grid**3
        lapse = -0.0006 * grid**2
        discrete = np.empty_like(grid)
        discrete[0] = exact[0]
        for step_index, step in enumerate(np.diff(grid)):
            discrete[step_index + 1] = discrete[step_index] - 0.5 * step * (
                lapse[step_index] + lapse[step_index + 1]
            )
        item = scenario(
            time=grid,
            potential_amplitudes=discrete,
            lapse_amplitudes=lapse,
            dust_amplitudes=np.full(grid.size, 0.01),
            scale_factor=np.ones(grid.size),
            hubble=np.zeros(grid.size),
            initialization_mode=BoostInitializationMode.SUPPLIED_INITIAL_BOOST,
            lapse_kernel_mode=LapseKernelMode.REQUIRE_MEAN_ZERO,
        )
        result = propagate_scalar_dust_wall_boost(scenario=item, numerics=numerics())
        error = float(
            np.max(
                np.abs(
                    result.scalar_potential[:, mask]
                    - exact[:, None] * scalar.reshape(-1)[mask]
                )
            )
        )
        convergence.append({"intervals": intervals, "max_potential_error": error})
    for index in range(1, len(convergence)):
        convergence[index]["observed_rate"] = float(
            np.log(
                float(convergence[index - 1]["max_potential_error"])
                / float(convergence[index]["max_potential_error"])
            )
            / np.log(2.0)
        )

    return {
        "realization_id": "H1-1F-B-COMMON-SPACETIME-SCALAR-NORMAL-BOOST-DYNAMICS-V1",
        "scientific_classification": SYNTHETIC_VALIDATION_ONLY,
        "zero_driver_nonzero_initial_boost": {
            "initial_velocity_max": float(
                np.max(np.linalg.norm(zero_result.dust_velocity_relative_to_wall[0], axis=-1))
            ),
            "potential_change_max": float(
                np.max(
                    np.abs(
                        zero_result.scalar_potential[-1]
                        - zero_result.scalar_potential[0]
                    )
                )
            ),
        },
        "manufactured_lapse_solution": {
            "potential_max_error": manufactured_error,
            "compatibility_max_abs": manufactured_result.diagnostics.expansion_compatibility_max_abs,
            "compatibility_normalized_linf": manufactured_result.diagnostics.expansion_compatibility_normalized_linf,
            "propagation_max_abs": manufactured_result.diagnostics.propagation_residual_max_abs,
            "propagation_normalized_linf": manufactured_result.diagnostics.propagation_residual_normalized_linf,
            "velocity_to_light_speed_max": manufactured_result.diagnostics.maximum_velocity_to_light_speed_ratio,
            "potential_mean_max_abs": manufactured_result.diagnostics.potential_mean_max_abs,
            "compatibility_tolerance": manufactured_result.diagnostics.expansion_compatibility_tolerance,
            "compatibility_worst_time": manufactured_result.diagnostics.expansion_compatibility_worst_time,
            "compatibility_worst_spatial_index": manufactured_result.diagnostics.expansion_compatibility_worst_spatial_index,
            "propagation_tolerance": manufactured_result.diagnostics.propagation_residual_tolerance,
            "propagation_worst_time": manufactured_result.diagnostics.propagation_worst_time,
            "propagation_worst_spatial_index": manufactured_result.diagnostics.propagation_worst_spatial_index,
            "scale_factor_rate_residual": manufactured_result.diagnostics.scale_factor_rate_residual_max_abs,
            "lapse_raw_mean_max_abs": manufactured_result.diagnostics.lapse_raw_mean_max_abs,
            "lapse_q0_correction_max_abs": manufactured_result.diagnostics.lapse_q0_correction_max_abs,
        },
        "expansion_matched_initialization": {
            "initial_potential_max_error": expansion_matched_initial_error,
            "compatibility_max_abs": expansion_matched_result.diagnostics.expansion_compatibility_max_abs,
        },
        "operator_scale_conversion": {
            "identity": "D_w^2 psi = L_w psi / a_w^2",
            "scale_factor": 2.0,
            "compatibility_max_abs": scale_result.diagnostics.expansion_compatibility_max_abs,
        },
        "convergence": {
            "classification": TIME_INTEGRATOR_CONVERGENCE_CLASSIFICATION,
            "independent_physical_validation": "NO",
            "interpretation": (
                "CLOSED_FORM_TRAPEZOIDAL_TRUNCATION_SCALING_OF_THE_"
                "IMPLEMENTED_RULE"
            ),
            "sequence": convergence,
        },
        "normal_varying_boundary": {
            "fixture_classification": "SYNTHETIC_VALIDATION_ONLY",
            "spatial_dimension": 3,
            "initial_normal_velocity_max_abs": (
                normal_result.diagnostics.initial_boundary_normal_velocity_max_abs
            ),
            "driver_normal_acceleration_max_abs": (
                normal_result.diagnostics.driver_boundary_normal_acceleration_max_abs
            ),
            "propagated_normal_velocity_max_abs": (
                normal_result.diagnostics.propagated_boundary_normal_velocity_max_abs
            ),
            "normal_velocity_tolerance": (
                normal_result.diagnostics.initial_boundary_normal_velocity_tolerance
            ),
            "normal_acceleration_tolerance": (
                normal_result.diagnostics.driver_boundary_normal_acceleration_tolerance
            ),
            "potential_max_error": normal_potential_error,
            "broken_vs_unbroken_laplacian_max_difference": (
                broken_unbroken_difference
            ),
            "admissible_initial_and_driver_passed": True,
        },
        "fail_closed": {
            "expansion_perturbation_rejected": compatibility_rejected,
            "reversed_sign_rejected": sign_reversed_rejected,
            "background_gamma_w_rejected": background_lapse_rejected,
            "absent_initial_mode_rejected": no_initial_mode_rejected,
            "transverse_request_rejected": transverse_rejected,
            "kernel_incompatibility_rejected": kernel_rejected,
            "h1_interface_inheritance_rejected": interface_inheritance_rejected,
            "linear_regime_violation_rejected": linear_rejected,
            "common_spacetime_mismatch_rejected": alignment_rejected,
            "post_construction_mutation_rejected": mutation_rejected,
            "propagation_residual_failure_rejected": propagation_residual_rejected,
            "wrong_operator_scale_factor_rejected": wrong_scale_factor_rejected,
            "normal_varying_initial_boundary_rejected": boundary_initial_rejected,
            "normal_varying_driver_boundary_rejected": boundary_driver_rejected,
            "nonzero_background_shear_rejected": nonzero_shear_rejected,
        },
        "evidence_classification": {
            "expansion_compatibility": EXPANSION_COMPATIBILITY_EVIDENCE,
            "propagation": PROPAGATION_CONSTRUCTION_DIAGNOSTIC,
            "curl": "CONSTRUCTION_INVARIANT_NOT_INDEPENDENT_NUMERICAL_EVIDENCE",
            "boundary": BOOST_SPECIFIC_BOUNDARY_MODEL,
            "boundary_runtime_enforcement": BOOST_BOUNDARY_RUNTIME_ENFORCEMENT,
            "wall_proper_time_rate": WALL_PROPER_TIME_RATE_ROLE,
            "wall_background_shear": WALL_BACKGROUND_SHEAR_EXCLUDED,
            "harmonic_vector_sector": HARMONIC_VECTOR_SECTOR_EXCLUDED,
            "harmonic_vector_zero_as_timescape_prediction": (
                HARMONIC_VECTOR_ZERO_NOT_GRANTED
            ),
            "geometry": "SYNTHETIC_VALIDATION_ONLY",
            "prediction": "NOT_GRANTED",
            "observational_authorization": "NOT_GRANTED",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT_DEFAULT)
    args = parser.parse_args()
    result = validate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
