"""Phase 1F-B conditional common-spacetime scalar boost dynamics tests."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import inspect

import numpy as np
import pytest

from phase1f_a_test_utils import (
    boundary,
    domain,
    make_realization,
    manufactured_laplacian,
    manufactured_scalar,
    numerics as phase1f_a_numerics,
    regional_full,
    zero_mode,
)
import timescape_fsigma8.phase1f_b as phase1f_b
from timescape_fsigma8.phase1f_a.operators import (
    apply_regional_laplace_beltrami,
    assemble_regional_elliptic_system,
)
from timescape_fsigma8.phase1f_b import (
    BOOST_BOUNDARY_RUNTIME_ENFORCEMENT,
    BOOST_SPECIFIC_BOUNDARY_MODEL,
    CONDITIONAL_SCALAR_DUST_TO_WALL_BOOST,
    EXPLICIT_EXTERNAL_NO_PENETRATION_CLOSURE,
    EXPANSION_COMPATIBILITY_EVIDENCE,
    HARMONIC_VECTOR_SECTOR_EXCLUDED,
    HARMONIC_VECTOR_ZERO_NOT_GRANTED,
    MATHEMATICAL_OPERATOR_FIXTURE_ONLY,
    PERTURBATIVE_WALL_LAPSE_POTENTIAL,
    PROPAGATION_CONSTRUCTION_DIAGNOSTIC,
    SYNTHETIC_VALIDATION_ONLY,
    TIME_INTEGRATOR_CONVERGENCE_CLASSIFICATION,
    TRANSVERSE_SECTOR_EXCLUDED,
    WALL_BACKGROUND_SHEAR_EXCLUDED,
    WALL_PROPER_TIME_RATE_PROVENANCE,
    WALL_PROPER_TIME_RATE_ROLE,
    WALL_SHEAR_ZERO_NOT_GRANTED,
    COMMON_TIME_PROPAGATION,
    BoostBoundaryKernelPolicy,
    BoostBoundaryKind,
    BoostGeometryProvenance,
    BoostInitializationMode,
    CommonSpacetimeWallGeometryClosure,
    LapseKernelMode,
    Phase1FBBoundaryCompatibilityError,
    Phase1FBCompatibilityError,
    Phase1FBContractError,
    Phase1FBGeometryClosureError,
    Phase1FBKernelCompatibilityError,
    Phase1FBLinearRegimeError,
    Phase1FBPropagationError,
    Phase1FBStateIntegrityError,
    ScalarBoostSector,
    ScalarDustWallBoostNumerics,
    ScalarDustWallBoostScenario,
    WallBackgroundGeometrySector,
    propagate_scalar_dust_wall_boost,
)


def boost_numerics(
    *,
    propagation_tolerance: float = 2e-10,
    linear_threshold: float = 0.1,
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
        provenance="EXPLICIT_PHASE1F_B_WALL_INTERIOR_BOOST_BOUNDARY",
        classification=BOOST_SPECIFIC_BOUNDARY_MODEL,
        physical_boundary_condition=EXPLICIT_EXTERNAL_NO_PENETRATION_CLOSURE,
        derived_from_timescape=False,
        inherited_from_h1_density_transmission=False,
        physical_interface_claim="NOT_GRANTED",
    )


def scalar_profile(shape: tuple[int, ...]) -> np.ndarray:
    if len(shape) == 2:
        coordinates = np.indices(shape, dtype=float)
        return np.sin(2.0 * np.pi * coordinates[-1] / shape[-1])
    return manufactured_scalar(shape)


def laplacian_profile(shape: tuple[int, ...]) -> np.ndarray:
    if len(shape) == 2:
        coordinates = np.indices(shape, dtype=float)
        eigenvalue = -4.0 * np.sin(np.pi / shape[-1]) ** 2 / (1.0 / shape[-1]) ** 2
        return eigenvalue * np.sin(2.0 * np.pi * coordinates[-1] / shape[-1])
    return manufactured_laplacian(shape)


def expansion_history(realization, amplitudes: np.ndarray):
    shape = realization.scientific_state.operator.carrier.grid_shape
    source_shape = laplacian_profile(shape)
    return tuple(
        realization.reconstruct_expansion(
            z_cgi=regional_full(amplitude * source_shape, realization, "wall"),
            regional_geometry=domain(realization, "wall"),
            boundary_policy=boundary("wall"),
            zero_mode_closure=zero_mode("wall"),
            background_expansion_identity="bar_Theta_d,w=3H_d,w",
            provenance=f"SYNTHETIC_PHASE1F_B_DUST_EXPANSION_{index}",
        )
        for index, amplitude in enumerate(amplitudes)
    )


def make_case(
    *,
    shape: tuple[int, ...] = (4, 4, 4),
    time: np.ndarray | None = None,
    potential_amplitudes: np.ndarray | None = None,
    lapse_amplitudes: np.ndarray | None = None,
    dust_amplitudes: np.ndarray | None = None,
    scale_factor: np.ndarray | None = None,
    hubble: np.ndarray | None = None,
    initialization_mode: BoostInitializationMode = BoostInitializationMode.SUPPLIED_INITIAL_BOOST,
    lapse_kernel_mode: LapseKernelMode = LapseKernelMode.REQUIRE_MEAN_ZERO,
    reverse_expansion_sign: bool = False,
    proper_time_rate: np.ndarray | None = None,
):
    realization = make_realization(shape)
    time = np.array([0.0, 0.25, 0.5], dtype=float) if time is None else np.asarray(time, dtype=float)
    nt = time.size
    potential_amplitudes = (
        np.full(nt, 0.002, dtype=float)
        if potential_amplitudes is None
        else np.asarray(potential_amplitudes, dtype=float)
    )
    lapse_amplitudes = (
        np.zeros(nt, dtype=float)
        if lapse_amplitudes is None
        else np.asarray(lapse_amplitudes, dtype=float)
    )
    dust_amplitudes = (
        np.full(nt, 0.01, dtype=float)
        if dust_amplitudes is None
        else np.asarray(dust_amplitudes, dtype=float)
    )
    scale_factor = (
        np.ones(nt, dtype=float)
        if scale_factor is None
        else np.asarray(scale_factor, dtype=float)
    )
    hubble = (
        np.zeros(nt, dtype=float)
        if hubble is None
        else np.asarray(hubble, dtype=float)
    )
    shape_grid = realization.scientific_state.operator.carrier.grid_shape
    scalar = scalar_profile(shape_grid)
    laplacian = laplacian_profile(shape_grid)
    dust = dust_amplitudes[:, None] * scalar.reshape(1, -1)
    physical_laplacian = (
        potential_amplitudes[:, None] * laplacian.reshape(1, -1)
        / scale_factor[:, None] ** 2
    )
    sign = 1.0 if reverse_expansion_sign else -1.0
    wall_expansion = dust + sign * physical_laplacian
    lapse = lapse_amplitudes[:, None] * scalar.reshape(1, -1)
    mask = realization.scientific_state.operator.morphology.wall_domain.reshape(-1)
    wall_expansion[:, ~mask] = 0.0
    lapse[:, ~mask] = 0.0
    closure = CommonSpacetimeWallGeometryClosure(
        wall_domain=domain(realization, "wall"),
        common_spacetime_id="SYNTHETIC_COMMON_SPACETIME_PHASE1F_B",
        wall_congruence_id="SYNTHETIC_HYPERSURFACE_NORMAL_WALL_OBSERVER",
        regional_wall_dust_congruence_id="REGIONAL_WALL_DUST_CONGRUENCE",
        h1_wall_embedding_id=realization.scientific_state.operator.morphology.wall_pullback_id,
        common_time_coordinate_id="SYNTHETIC_COMMON_TIME_T",
        wall_proper_time_mapping_id="EXPLICIT_SYNTHETIC_DTAU_W_DT",
        spatial_geometry_operator_id="wall-normalization",
        dust_expansion_background_identity="bar_Theta_d,w=3H_d,w",
        domain_id="wall",
        time_grid=time,
        wall_scale_factor=scale_factor,
        wall_hubble_rate=hubble,
        wall_proper_time_rate=(
            np.ones(nt) if proper_time_rate is None
            else np.asarray(proper_time_rate, dtype=float)
        ),
        wall_proper_time_rate_role=WALL_PROPER_TIME_RATE_ROLE,
        wall_proper_time_rate_provenance=WALL_PROPER_TIME_RATE_PROVENANCE,
        wall_expansion_perturbation=wall_expansion,
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
        normalization_kernel_identity=zero_mode("wall", scale_factor[0]).provenance,
        scientific_classification=SYNTHETIC_VALIDATION_ONLY,
    )
    initial = (
        regional_full(potential_amplitudes[0] * scalar, realization, "wall")
        if initialization_mode is BoostInitializationMode.SUPPLIED_INITIAL_BOOST
        else None
    )
    scenario = ScalarDustWallBoostScenario(
        geometry_closure=closure,
        dust_expansion_history=expansion_history(realization, dust_amplitudes),
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
        zero_mode_closure=zero_mode("wall", scale_factor[0]),
        lapse_kernel_mode=lapse_kernel_mode,
        requested_sector=ScalarBoostSector.SCALAR_LONGITUDINAL_HYPERSURFACE_ORTHOGONAL,
        scientific_classification=SYNTHETIC_VALIDATION_ONLY,
    )
    return realization, scenario, scalar, laplacian


def normal_varying_case(
    *,
    initial_profile: np.ndarray,
    lapse_profile: np.ndarray,
    proper_time_rate: np.ndarray | None = None,
) -> tuple[object, ScalarDustWallBoostScenario, np.ndarray]:
    """Build a genuine 3-D wall-interior boundary fixture.

    The field varies along the layer normal.  Its evolution follows the
    Phase 1F-B scalar law derived from BDE Eqs. (14)--(16), while the
    no-penetration trace is the explicit external boost closure approved for
    v2 rather than a Timescape interface equation.
    """
    shape = (8, 4, 4)
    time = np.array([0.0, 0.25, 0.5], dtype=np.float64)
    realization, base, _, _ = make_case(
        shape=shape, time=time, proper_time_rate=proper_time_rate
    )
    alpha = (
        np.ones(time.size) if proper_time_rate is None
        else np.asarray(proper_time_rate, dtype=float)
    )
    mask_grid = base.geometry_closure.wall_domain.mask.reshape(shape)
    wall_x = np.flatnonzero(np.any(mask_grid, axis=(1, 2)))
    if initial_profile.shape != wall_x.shape or lapse_profile.shape != wall_x.shape:
        raise ValueError("normal profiles must cover the wall-layer x cells")
    initial_grid = np.zeros(shape, dtype=np.float64)
    lapse_grid = np.zeros(shape, dtype=np.float64)
    initial_grid[wall_x, :, :] = initial_profile[:, None, None]
    lapse_grid[wall_x, :, :] = lapse_profile[:, None, None]
    initial_full = (0.002 * initial_grid).reshape(-1)
    lapse_amplitude = np.array([0.0, 1.0e-4, 2.0e-4], dtype=np.float64)
    lapse_full = lapse_amplitude[:, None] * lapse_grid.reshape(1, -1)
    driver_full = alpha[:, None] * lapse_full
    potential_full = np.empty_like(lapse_full)
    potential_full[0] = initial_full
    for index, step in enumerate(np.diff(time)):
        potential_full[index + 1] = potential_full[index] - 0.5 * step * (
            driver_full[index] + driver_full[index + 1]
        )

    wall_domain = base.geometry_closure.wall_domain
    system = assemble_regional_elliptic_system(
        domain=wall_domain,
        boundary_policy=boundary("wall"),
        numerics=phase1f_a_numerics(),
    )
    dust_regional = np.stack(
        [item.regional_values for item in base.dust_expansion_history]
    )
    wall_expansion = np.zeros_like(lapse_full)
    for index in range(time.size):
        laplacian = apply_regional_laplace_beltrami(
            system=system,
            field=potential_full[index, system.regional_indices],
        )
        wall_expansion[index, system.regional_indices] = (
            dust_regional[index] - laplacian
        )
    closure = replace(
        base.geometry_closure,
        wall_expansion_perturbation=wall_expansion,
        wall_lapse_perturbation=lapse_full,
    )
    scenario = replace(
        base,
        geometry_closure=closure,
        initial_scalar_potential=initial_full,
    )
    return realization, scenario, potential_full


def test_v1_zero_driver_preserves_nonzero_initial_scalar_boost() -> None:
    realization, scenario, _, _ = make_case()
    result = propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())
    mask = scenario.geometry_closure.wall_domain.mask
    assert np.max(np.abs(result.scalar_potential[0, mask])) > 0.0
    np.testing.assert_allclose(
        result.scalar_potential[1:],
        np.broadcast_to(result.scalar_potential[0], result.scalar_potential[1:].shape),
        atol=1e-14,
    )
    np.testing.assert_allclose(
        result.dust_velocity_relative_to_wall[1:],
        np.broadcast_to(
            result.dust_velocity_relative_to_wall[0],
            result.dust_velocity_relative_to_wall[1:].shape,
        ),
        atol=1e-14,
    )
    assert result.diagnostics.propagation_residual_max_abs <= 2e-10
    assert result.velocity_units == "REFERENCE_LENGTH_PER_COMMON_TIME"
    assert (
        result.velocity_component_representation
        == "WALL_REFERENCE_METRIC_ORTHONORMAL_CHOLESKY_COMPONENTS"
    )
    assert result.scientific_classification == CONDITIONAL_SCALAR_DUST_TO_WALL_BOOST
    assert realization.scientific_state.operator.carrier.dimension == 3


def test_v2_manufactured_lapse_solution_and_q0_projection() -> None:
    time = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    expected = 0.002 + 0.001 * time - 0.0002 * time**2
    lapse = -0.001 + 0.0004 * time
    _, scenario, scalar, _ = make_case(
        time=time,
        potential_amplitudes=expected,
        lapse_amplitudes=lapse,
        lapse_kernel_mode=LapseKernelMode.EXPLICIT_Q0_PROJECTION,
    )
    result = propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())
    mask = scenario.geometry_closure.wall_domain.mask
    np.testing.assert_allclose(
        result.scalar_potential[:, mask],
        expected[:, None] * scalar.reshape(-1)[mask],
        atol=2e-12,
    )
    assert result.diagnostics.lapse_raw_mean_max_abs <= 2e-15


def test_v3_expansion_compatibility_perturbation_fails_closed() -> None:
    _, scenario, _, _ = make_case()
    changed = np.array(scenario.geometry_closure.wall_expansion_perturbation, copy=True)
    changed[1, scenario.geometry_closure.wall_domain.mask] += 1e-4
    tampered = replace(scenario.geometry_closure, wall_expansion_perturbation=changed)
    bad = replace(scenario, geometry_closure=tampered)
    with pytest.raises(Phase1FBCompatibilityError, match="compatibility residual"):
        propagate_scalar_dust_wall_boost(scenario=bad, numerics=boost_numerics())


def test_v4_sign_sensitive_expansion_difference_rejects_reversed_rhs() -> None:
    _, scenario, _, _ = make_case(reverse_expansion_sign=True)
    with pytest.raises(Phase1FBCompatibilityError, match="compatibility residual"):
        propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())


def test_v5_background_timescape_lapse_cannot_be_geometry_driver() -> None:
    _, scenario, _, _ = make_case()
    with pytest.raises(Phase1FBGeometryClosureError, match="background gamma_w"):
        replace(
            scenario.geometry_closure,
            lapse_driver_kind="BACKGROUND_TIMESCAPE_GAMMA_W",
        )
    signature = inspect.signature(CommonSpacetimeWallGeometryClosure)
    assert "background_gamma_w" not in signature.parameters


def test_v6_no_implicit_initial_boost_mode_or_zero() -> None:
    _, scenario, _, _ = make_case()
    with pytest.raises(Phase1FBContractError, match="initialization_mode"):
        replace(scenario, initialization_mode=None)  # type: ignore[arg-type]
    signature = inspect.signature(ScalarDustWallBoostScenario)
    assert signature.parameters["initialization_mode"].default is inspect.Parameter.empty


def test_v7_transverse_request_is_rejected_not_zero_filled() -> None:
    _, scenario, _, _ = make_case()
    with pytest.raises(Phase1FBContractError, match="transverse/vector"):
        replace(scenario, requested_sector="TRANSVERSE")  # type: ignore[arg-type]
    result = propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())
    assert result.transverse_sector_status == TRANSVERSE_SECTOR_EXCLUDED
    assert not hasattr(result, "transverse_velocity")


def test_v8_kernel_incompatibility_and_explicit_q0_policy() -> None:
    _, scenario, _, _ = make_case()
    lapse = np.array(scenario.geometry_closure.wall_lapse_perturbation, copy=True)
    lapse[:, scenario.geometry_closure.wall_domain.mask] += 0.01
    closure = replace(scenario.geometry_closure, wall_lapse_perturbation=lapse)
    require_zero = replace(scenario, geometry_closure=closure)
    with pytest.raises(Phase1FBKernelCompatibilityError, match="wall lapse"):
        propagate_scalar_dust_wall_boost(scenario=require_zero, numerics=boost_numerics())
    projected = replace(require_zero, lapse_kernel_mode=LapseKernelMode.EXPLICIT_Q0_PROJECTION)
    # The explicit projection is accepted only if the independently supplied
    # wall expansion remains compatible with the projected trajectory.
    result = propagate_scalar_dust_wall_boost(scenario=projected, numerics=boost_numerics())
    assert result.diagnostics.lapse_q0_correction_max_abs == pytest.approx(0.01)


def test_v8_supplied_initial_potential_mean_mismatch_fails_closed() -> None:
    _, scenario, _, _ = make_case()
    changed = np.array(scenario.initial_scalar_potential, copy=True)
    changed[scenario.geometry_closure.wall_domain.mask] += 0.01
    bad = replace(scenario, initial_scalar_potential=changed)
    with pytest.raises(Phase1FBKernelCompatibilityError, match="initial boost"):
        propagate_scalar_dust_wall_boost(scenario=bad, numerics=boost_numerics())


def test_v8_supplied_initial_potential_outside_wall_is_rejected() -> None:
    _, scenario, _, _ = make_case()
    changed = np.array(scenario.initial_scalar_potential, copy=True)
    changed[~scenario.geometry_closure.wall_domain.mask] = 1e-4
    bad = replace(scenario, initial_scalar_potential=changed)
    with pytest.raises(Phase1FBKernelCompatibilityError, match="outside wall"):
        propagate_scalar_dust_wall_boost(scenario=bad, numerics=boost_numerics())


def test_v8_expansion_matched_source_mean_mismatch_fails_closed() -> None:
    _, scenario, _, _ = make_case(
        initialization_mode=BoostInitializationMode.EXPANSION_MATCHED_INITIAL_BOOST
    )
    changed = np.array(scenario.geometry_closure.wall_expansion_perturbation, copy=True)
    changed[0, scenario.geometry_closure.wall_domain.mask] += 0.01
    bad = replace(
        scenario,
        geometry_closure=replace(
            scenario.geometry_closure, wall_expansion_perturbation=changed
        ),
    )
    with pytest.raises(Phase1FBKernelCompatibilityError, match="initial source"):
        propagate_scalar_dust_wall_boost(scenario=bad, numerics=boost_numerics())


def test_v9_h1_density_interface_boundary_inheritance_is_forbidden() -> None:
    with pytest.raises(Phase1FBContractError, match="inheritance is forbidden"):
        replace(boost_boundary(), inherited_from_h1_density_transmission=True)


def test_v10_linear_regime_gate_fails_for_excessive_amplitude() -> None:
    _, scenario, _, _ = make_case(potential_amplitudes=np.full(3, 1.0))
    with pytest.raises(Phase1FBLinearRegimeError, match="linear-regime"):
        propagate_scalar_dust_wall_boost(
            scenario=scenario,
            numerics=boost_numerics(linear_threshold=0.01),
        )


def test_v11_comoving_operator_requires_explicit_a_squared_conversion() -> None:
    scale = np.full(3, 2.0)
    _, scenario, _, _ = make_case(scale_factor=scale)
    result = propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())
    assert result.diagnostics.expansion_compatibility_max_abs <= 5e-10
    wrong = np.array(scenario.geometry_closure.wall_expansion_perturbation, copy=True)
    lap = laplacian_profile((4, 4, 4)).reshape(-1)
    mask = scenario.geometry_closure.wall_domain.mask
    # Omitting the 1/a_w^2 physical conversion is a load-bearing error.
    wrong[:, mask] -= 0.002 * lap[mask] * (1.0 - 1.0 / scale[:, None] ** 2)
    bad = replace(
        scenario,
        geometry_closure=replace(
            scenario.geometry_closure, wall_expansion_perturbation=wrong
        ),
    )
    with pytest.raises(Phase1FBCompatibilityError):
        propagate_scalar_dust_wall_boost(scenario=bad, numerics=boost_numerics())


def test_v12_common_spacetime_alignment_rejected_before_evaluation() -> None:
    _, scenario, _, _ = make_case()
    with pytest.raises(Phase1FBGeometryClosureError, match="embedding identity"):
        replace(scenario.geometry_closure, h1_wall_embedding_id="MISMATCHED_EMBEDDING")
    with pytest.raises(Phase1FBGeometryClosureError, match="operator identity"):
        replace(scenario.geometry_closure, spatial_geometry_operator_id="OTHER_METRIC")
    with pytest.raises(Phase1FBContractError, match="time grids must match"):
        replace(
            scenario,
            dust_expansion_time_grid=scenario.dust_expansion_time_grid + 0.01,
        )
    with pytest.raises(Phase1FBContractError, match="time-coordinate identities"):
        replace(scenario, dust_expansion_time_coordinate_id="OTHER_COMMON_TIME")
    with pytest.raises(Phase1FBGeometryClosureError, match="domain_id"):
        replace(scenario.geometry_closure, domain_id="void")


def test_nonfinite_geometry_driver_and_time_history_mismatch_fail_closed() -> None:
    _, scenario, _, _ = make_case()
    nonfinite = np.array(scenario.geometry_closure.wall_lapse_perturbation, copy=True)
    nonfinite[0, 0] = np.nan
    with pytest.raises(Phase1FBContractError, match="finite"):
        replace(scenario.geometry_closure, wall_lapse_perturbation=nonfinite)
    with pytest.raises(Phase1FBContractError, match="match time grid"):
        replace(scenario, dust_expansion_history=scenario.dust_expansion_history[:-1])


def test_public_scientific_constructors_have_no_defaults() -> None:
    constructors = (
        CommonSpacetimeWallGeometryClosure,
        ScalarDustWallBoostScenario,
        ScalarDustWallBoostNumerics,
        BoostBoundaryKernelPolicy,
    )
    for constructor in constructors:
        for parameter in inspect.signature(constructor).parameters.values():
            assert parameter.default is inspect.Parameter.empty
    for parameter in inspect.signature(propagate_scalar_dust_wall_boost).parameters.values():
        assert parameter.default is inspect.Parameter.empty


def test_expansion_matched_initialization_solves_sign_correct_constraint() -> None:
    _, scenario, scalar, _ = make_case(
        initialization_mode=BoostInitializationMode.EXPANSION_MATCHED_INITIAL_BOOST
    )
    result = propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())
    mask = scenario.geometry_closure.wall_domain.mask
    np.testing.assert_allclose(
        result.scalar_potential[0, mask], 0.002 * scalar.reshape(-1)[mask], atol=2e-12
    )


def test_propagation_construction_diagnostic_can_fail_its_numerical_gate() -> None:
    time = np.array([0.0, 1.0])
    scale = np.exp(time)
    _, scenario, _, _ = make_case(
        time=time,
        potential_amplitudes=np.full(2, 0.002),
        lapse_amplitudes=np.zeros(2),
        dust_amplitudes=np.full(2, 0.01),
        scale_factor=scale,
        hubble=np.ones(2),
    )
    with pytest.raises(Phase1FBPropagationError, match="propagation residual"):
        propagate_scalar_dust_wall_boost(
            scenario=scenario,
            numerics=boost_numerics(propagation_tolerance=1e-12),
        )


def test_supplied_normal_varying_no_penetration_potential_is_accepted() -> None:
    _, scenario, _ = normal_varying_case(
        initial_profile=np.array([-1.0, -1.0, 1.0, 1.0]),
        lapse_profile=np.zeros(4),
    )
    result = propagate_scalar_dust_wall_boost(
        scenario=scenario, numerics=boost_numerics()
    )
    diagnostics = result.diagnostics
    assert diagnostics.initial_boundary_normal_velocity_max_abs <= 2e-11
    assert diagnostics.propagated_boundary_normal_velocity_max_abs <= 2e-11
    assert diagnostics.boundary_condition_classification == BOOST_SPECIFIC_BOUNDARY_MODEL
    assert diagnostics.boundary_runtime_enforcement == BOOST_BOUNDARY_RUNTIME_ENFORCEMENT


def test_supplied_normal_varying_penetrating_potential_is_rejected() -> None:
    _, scenario, _ = normal_varying_case(
        initial_profile=np.array([-1.5, -0.5, 0.5, 1.5]),
        lapse_profile=np.zeros(4),
    )
    with pytest.raises(
        Phase1FBBoundaryCompatibilityError, match="initial scalar boost"
    ):
        propagate_scalar_dust_wall_boost(
            scenario=scenario, numerics=boost_numerics()
        )


def test_boundary_incompatible_time_dependent_lapse_driver_is_rejected() -> None:
    _, scenario, _ = normal_varying_case(
        initial_profile=np.array([-1.0, -1.0, 1.0, 1.0]),
        lapse_profile=np.array([-1.5, -0.5, 0.5, 1.5]),
    )
    with pytest.raises(
        Phase1FBBoundaryCompatibilityError, match="wall lapse driver"
    ):
        propagate_scalar_dust_wall_boost(
            scenario=scenario, numerics=boost_numerics()
        )


def test_boundary_compatible_driver_preserves_no_penetration_for_all_times() -> None:
    _, scenario, expected = normal_varying_case(
        initial_profile=np.array([-1.0, -1.0, 1.0, 1.0]),
        lapse_profile=np.array([-1.0, -1.0, 1.0, 1.0]),
    )
    result = propagate_scalar_dust_wall_boost(
        scenario=scenario, numerics=boost_numerics()
    )
    np.testing.assert_allclose(result.scalar_potential, expected, atol=2e-14)
    assert result.diagnostics.driver_boundary_normal_acceleration_max_abs <= 2e-11
    assert result.diagnostics.propagated_boundary_normal_velocity_max_abs <= 2e-11


def test_normal_varying_fixture_distinguishes_broken_and_unbroken_operators() -> None:
    _, scenario, expected = normal_varying_case(
        initial_profile=np.array([-1.0, -1.0, 1.0, 1.0]),
        lapse_profile=np.zeros(4),
    )
    result = propagate_scalar_dust_wall_boost(
        scenario=scenario, numerics=boost_numerics()
    )
    shape = scenario.geometry_closure.wall_domain.operator.carrier.grid_shape
    spacing = scenario.geometry_closure.wall_domain.operator.carrier.grid_spacing
    field = expected[0].reshape(shape)
    unbroken = np.zeros(shape, dtype=np.float64)
    for axis, step in enumerate(spacing):
        unbroken += (
            np.roll(field, 1, axis=axis)
            - 2.0 * field
            + np.roll(field, -1, axis=axis)
        ) / step**2
    wall_mask = scenario.geometry_closure.wall_domain.mask
    difference = np.max(
        np.abs(result.physical_laplacian_of_potential[0, wall_mask] - unbroken.reshape(-1)[wall_mask])
    )
    assert difference == pytest.approx(0.128)


def test_shear_free_sector_is_explicit_and_nonzero_shear_is_rejected() -> None:
    _, scenario, _, _ = make_case()
    assert scenario.geometry_closure.wall_background_shear_free is True
    with pytest.raises(Phase1FBGeometryClosureError, match="shear-free"):
        replace(scenario.geometry_closure, wall_background_shear_free=False)
    with pytest.raises(Phase1FBGeometryClosureError, match="shear-free"):
        replace(  # type: ignore[arg-type]
            scenario.geometry_closure,
            selected_background_geometry_sector="NONZERO_WALL_SHEAR",
        )


def test_harmonic_vector_sector_is_excluded_not_normalized_to_zero() -> None:
    _, scenario, _, _ = make_case()
    result = propagate_scalar_dust_wall_boost(
        scenario=scenario, numerics=boost_numerics()
    )
    assert result.harmonic_vector_sector_status == HARMONIC_VECTOR_SECTOR_EXCLUDED
    assert (
        result.harmonic_vector_zero_as_timescape_prediction
        == HARMONIC_VECTOR_ZERO_NOT_GRANTED
    )
    assert not hasattr(result, "harmonic_vector_velocity")


def test_residual_evidence_hierarchy_is_explicit() -> None:
    _, scenario, _, _ = make_case()
    result = propagate_scalar_dust_wall_boost(
        scenario=scenario, numerics=boost_numerics()
    )
    assert (
        result.diagnostics.expansion_compatibility_evidence_classification
        == EXPANSION_COMPATIBILITY_EVIDENCE
    )
    assert (
        result.diagnostics.propagation_evidence_classification
        == PROPAGATION_CONSTRUCTION_DIAGNOSTIC
    )
    assert "CONSTRUCTION_INVARIANT" in result.diagnostics.curl_status


def _clock_case(alpha: np.ndarray, amplitude: np.ndarray, time: np.ndarray):
    """Manufacture a scenario whose analytic psi amplitude is ``amplitude``."""
    return make_case(
        time=time,
        potential_amplitudes=amplitude,
        lapse_amplitudes=-0.001 + 0.0004 * time,
        proper_time_rate=alpha,
        lapse_kernel_mode=LapseKernelMode.EXPLICIT_Q0_PROJECTION,
    )


def test_t1_unit_clock_rate_reproduces_the_wall_proper_time_evolution() -> None:
    # alpha_W=1: d psi/dt = -Q0 nu, integral of (-0.001+0.0004 t).
    time = np.linspace(0.0, 1.0, 5)
    analytic = 0.002 + 0.001 * time - 0.0002 * time**2
    _, scenario, scalar, _ = _clock_case(np.ones(time.size), analytic, time)
    result = propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())
    mask = scenario.geometry_closure.wall_domain.mask
    np.testing.assert_allclose(
        result.scalar_potential[:, mask],
        analytic[:, None] * scalar.reshape(-1)[mask],
        atol=2e-12,
    )
    assert result.diagnostics.wall_proper_time_rate_min == 1.0
    assert result.common_time_propagation == COMMON_TIME_PROPAGATION


@pytest.mark.parametrize("rate", [2.0, 0.5])
def test_t2_t3_constant_non_unit_clock_rate_scales_the_evolution(rate: float) -> None:
    # d psi/dt = -alpha Q0 nu; analytic integral, never the production loop.
    time = np.linspace(0.0, 1.0, 5)
    analytic = 0.002 + rate * (0.001 * time - 0.0002 * time**2)
    _, scenario, scalar, _ = _clock_case(np.full(time.size, rate), analytic, time)
    result = propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())
    mask = scenario.geometry_closure.wall_domain.mask
    np.testing.assert_allclose(
        result.scalar_potential[:, mask],
        analytic[:, None] * scalar.reshape(-1)[mask],
        atol=2e-12,
    )
    unit = 0.002 + 0.001 * time - 0.0002 * time**2
    assert np.max(np.abs(analytic - unit)) > 1e-4
    assert result.diagnostics.wall_proper_time_rate_max == rate


def test_t4_time_dependent_clock_rate_matches_the_analytic_integral() -> None:
    # alpha_W(t)=1+t with a constant lapse amplitude keeps the driver linear in
    # t, so the analytic integral -int (1+s)(-0.001) ds is exact here.
    time = np.linspace(0.0, 1.0, 5)
    alpha = 1.0 + time
    analytic = 0.002 + 0.001 * (time + 0.5 * time**2)
    _, scenario, scalar, _ = make_case(
        time=time,
        potential_amplitudes=analytic,
        lapse_amplitudes=np.full(time.size, -0.001),
        proper_time_rate=alpha,
        lapse_kernel_mode=LapseKernelMode.EXPLICIT_Q0_PROJECTION,
    )
    result = propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())
    mask = scenario.geometry_closure.wall_domain.mask
    np.testing.assert_allclose(
        result.scalar_potential[:, mask],
        analytic[:, None] * scalar.reshape(-1)[mask],
        atol=2e-12,
    )
    # The 0.5 t^2 term is exactly the chain-rule contribution of alpha_W(t).
    assert np.max(np.abs(analytic - (0.002 + 0.001 * time))) == pytest.approx(0.0005)


@pytest.mark.parametrize("bad", [0.0, -1.0, np.nan, np.inf])
def test_t5_invalid_clock_rate_fails_closed(bad: float) -> None:
    _, scenario, _, _ = make_case()
    rate = np.ones(3); rate[1] = bad
    with pytest.raises(Phase1FBContractError):
        replace(scenario.geometry_closure, wall_proper_time_rate=rate)


def test_t5_spatially_varying_clock_rate_is_rejected() -> None:
    _, scenario, _, _ = make_case()
    size = scenario.geometry_closure.wall_domain.operator.size
    with pytest.raises(Phase1FBGeometryClosureError, match="match time_grid"):
        replace(scenario.geometry_closure, wall_proper_time_rate=np.ones((3, size)))


def test_t5_clock_provenance_must_be_the_external_closure() -> None:
    _, scenario, _, _ = make_case()
    assert (
        scenario.geometry_closure.wall_proper_time_rate_provenance
        == WALL_PROPER_TIME_RATE_PROVENANCE
    )
    with pytest.raises(Phase1FBGeometryClosureError, match="external closure"):
        replace(
            scenario.geometry_closure,
            wall_proper_time_rate_provenance="TIMESCAPE_PREDICTED_CLOCK_DRIVER",
        )


def test_t6_non_unit_clock_preserves_no_penetration_boundary() -> None:
    alpha = np.array([1.5, 1.5, 1.5])
    _, scenario, expected = normal_varying_case(
        initial_profile=np.array([-1.0, -1.0, 1.0, 1.0]),
        lapse_profile=np.array([-1.0, -1.0, 1.0, 1.0]),
        proper_time_rate=alpha,
    )
    result = propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())
    np.testing.assert_allclose(result.scalar_potential, expected, atol=2e-14)
    assert result.diagnostics.propagated_boundary_normal_velocity_max_abs <= 2e-11
    assert result.diagnostics.driver_boundary_normal_acceleration_max_abs <= 2e-11
    _, unit_scenario, unit_expected = normal_varying_case(
        initial_profile=np.array([-1.0, -1.0, 1.0, 1.0]),
        lapse_profile=np.array([-1.0, -1.0, 1.0, 1.0]),
    )
    assert np.max(np.abs(expected[-1] - unit_expected[-1])) > 0.0


def test_wall_proper_time_rate_is_load_bearing_not_metadata() -> None:
    # A nonzero lapse driver is required for the clock rate to act at all: the
    # v2 invariance claim held only because alpha_W multiplied a zero driver.
    time = np.linspace(0.0, 1.0, 5)
    analytic = 0.002 + 0.001 * time - 0.0002 * time**2
    _, scenario, scalar, _ = _clock_case(np.ones(time.size), analytic, time)
    original = propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())
    changed = replace(
        scenario,
        geometry_closure=replace(
            scenario.geometry_closure,
            wall_proper_time_rate=np.full(time.size, 2.0),
        ),
    )
    with pytest.raises(Phase1FBCompatibilityError):
        # The fixture's wall expansion is built for alpha_W=1, so doubling the
        # clock rate must change the evolution and break compatibility.
        propagate_scalar_dust_wall_boost(scenario=changed, numerics=boost_numerics())
    assert original.wall_proper_time_rate_role == WALL_PROPER_TIME_RATE_ROLE
    assert original.diagnostics.wall_hubble_time_convention == (
        "COMMON_TIME_LOGARITHMIC_SCALE_FACTOR_RATE"
    )


def test_zero_driver_evolution_is_clock_rate_independent() -> None:
    # With nu_W=0 the chain-rule factor multiplies zero, so a non-unit clock
    # legitimately leaves psi unchanged.  This is the only regime in which the
    # superseded v2 invariance assertion was true.
    _, scenario, _, _ = make_case()
    changed = replace(
        scenario,
        geometry_closure=replace(
            scenario.geometry_closure, wall_proper_time_rate=np.full(3, 2.0)
        ),
    )
    baseline = propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())
    scaled = propagate_scalar_dust_wall_boost(scenario=changed, numerics=boost_numerics())
    np.testing.assert_array_equal(baseline.scalar_potential, scaled.scalar_potential)


def test_boundary_closure_is_external_and_never_a_physical_interface_claim() -> None:
    policy = boost_boundary()
    assert policy.physical_boundary_condition == EXPLICIT_EXTERNAL_NO_PENETRATION_CLOSURE
    assert policy.derived_from_timescape is False
    assert policy.inherited_from_h1_density_transmission is False
    assert policy.physical_interface_claim == "NOT_GRANTED"
    with pytest.raises(Phase1FBContractError, match="not derived from Timescape"):
        replace(policy, derived_from_timescape=True)


def test_evidence_only_convergence_classification_is_public() -> None:
    assert (
        TIME_INTEGRATOR_CONVERGENCE_CLASSIFICATION
        == "SECOND_ORDER_NUMERICAL_SELF_CONVERGENCE_OF_THE_IMPLEMENTED_TIME_INTEGRATOR"
    )


def test_nonzero_hubble_homogeneous_propagation_passes_when_resolved() -> None:
    time = np.linspace(0.0, 1.0, 101)
    hubble = np.full(time.size, 0.05)
    scale = np.exp(0.05 * time)
    _, scenario, _, _ = make_case(
        time=time,
        potential_amplitudes=np.full(time.size, 0.002),
        lapse_amplitudes=np.zeros(time.size),
        dust_amplitudes=np.full(time.size, 0.01),
        scale_factor=scale,
        hubble=hubble,
    )
    result = propagate_scalar_dust_wall_boost(
        scenario=scenario,
        numerics=boost_numerics(propagation_tolerance=1e-9),
    )
    assert result.diagnostics.propagation_residual_max_abs < 1e-9
    assert result.diagnostics.scale_factor_rate_residual_max_abs < 2e-11


def test_state_integrity_and_nested_arrays_fail_closed() -> None:
    _, scenario, _, _ = make_case()
    with pytest.raises(FrozenInstanceError):
        scenario.geometry_closure = scenario.geometry_closure  # type: ignore[misc]
    with pytest.raises(ValueError, match="read-only"):
        scenario.geometry_closure.wall_lapse_perturbation.flat[0] = 1.0
    changed = np.array(scenario.geometry_closure.wall_lapse_perturbation, copy=True)
    changed[0, scenario.geometry_closure.wall_domain.mask] += 1e-5
    object.__setattr__(scenario.geometry_closure, "wall_lapse_perturbation", changed)
    with pytest.raises(Phase1FBStateIntegrityError, match="validated construction"):
        propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())


def test_numerics_and_boundary_low_level_tamper_are_detected() -> None:
    _, scenario, _, _ = make_case()
    numerical_policy = boost_numerics()
    object.__setattr__(numerical_policy, "expansion_compatibility_tolerance", 1.0)
    with pytest.raises(Phase1FBStateIntegrityError, match="validated construction"):
        propagate_scalar_dust_wall_boost(
            scenario=scenario, numerics=numerical_policy
        )
    boundary_policy = scenario.boundary_policy
    object.__setattr__(boundary_policy, "inherited_from_h1_density_transmission", True)
    with pytest.raises(Phase1FBStateIntegrityError, match="validated construction"):
        propagate_scalar_dust_wall_boost(
            scenario=scenario, numerics=boost_numerics()
        )


def test_result_integrity_detects_low_level_tamper() -> None:
    _, scenario, _, _ = make_case()
    result = propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())
    changed = np.array(result.scalar_potential, copy=True)
    changed[0, 0] += 1e-4
    object.__setattr__(result, "scalar_potential", changed)
    with pytest.raises(Phase1FBStateIntegrityError, match="validated construction"):
        result.validate_integrity()


def test_reduced_dimension_remains_mathematical_only() -> None:
    _, scenario, _, _ = make_case(shape=(4, 4))
    result = propagate_scalar_dust_wall_boost(scenario=scenario, numerics=boost_numerics())
    assert result.scientific_classification == MATHEMATICAL_OPERATOR_FIXTURE_ONLY


def test_scale_factor_hubble_mismatch_fails_closed() -> None:
    _, scenario, _, _ = make_case()
    bad = replace(
        scenario,
        geometry_closure=replace(
            scenario.geometry_closure, wall_hubble_rate=np.ones(3)
        ),
    )
    with pytest.raises(Phase1FBGeometryClosureError, match="scale factor"):
        propagate_scalar_dust_wall_boost(scenario=bad, numerics=boost_numerics())


def test_public_firewalls_and_state_rank_are_explicit() -> None:
    assert phase1f_b.FROZEN_DIFFERENTIAL_STATE_RANK == 4
    assert phase1f_b.SELECTED_SCALAR_REALIZATION_DIFFERENTIAL_STATE_RANK == 5
    public = {name.lower() for name in phase1f_b.__all__}
    forbidden = {
        "sigma8",
        "sigma_8",
        "sigmar",
        "sigma_r",
        "fsigma8",
        "f_sigma_8",
        "rsd",
        "kaiser",
        "tracer_velocity",
        "galaxy_velocity",
        "observational_k",
        "likelihood",
        "zero_boost_closure",
        "predict_timescape_boost",
    }
    assert public.isdisjoint(forbidden)
    assert not hasattr(phase1f_b, "ZeroBoostClosure")
