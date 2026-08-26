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
from timescape_fsigma8.phase1f_b import (
    BOOST_SPECIFIC_BOUNDARY_MODEL,
    CONDITIONAL_SCALAR_DUST_TO_WALL_BOOST,
    MATHEMATICAL_OPERATOR_FIXTURE_ONLY,
    PERTURBATIVE_WALL_LAPSE_POTENTIAL,
    SYNTHETIC_VALIDATION_ONLY,
    TRANSVERSE_SECTOR_EXCLUDED,
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
    Phase1FBPropagationError,
    Phase1FBStateIntegrityError,
    ScalarBoostSector,
    ScalarDustWallBoostNumerics,
    ScalarDustWallBoostScenario,
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
        inherited_from_h1_density_transmission=False,
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
        wall_proper_time_rate=np.ones(nt),
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
        scalar_hypersurface_orthogonal=True,
        vorticity_dust_zero=True,
        vorticity_wall_zero=True,
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


def test_independent_propagation_residual_can_fail_closed() -> None:
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
