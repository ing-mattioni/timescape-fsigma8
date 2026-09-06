"""Phase 1F-C conditional clock-anchored wall-geometry tests."""

# A06: absolute budgets use rtol=0; relative budgets use atol=0.
# Previously implicit algebraic comparisons use rtol=2e-12, atol=1e-14
# in the fixture units (roundoff allowance); explicit convergence budgets remain.

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from functools import cache
import inspect

import numpy as np
import pytest

from timescape_fsigma8.components import ComponentRepresentation

from test_phase1f_b_dust_wall_boost_dynamics import (
    boost_numerics,
    make_case as make_phase1f_b_case,
)
from timescape_fsigma8.phase1f_b import (
    LapseKernelMode,
    propagate_scalar_dust_wall_boost,
)
import timescape_fsigma8.phase1f_c as phase1f_c
from timescape_fsigma8.phase1f_c import (
    AUGMENTED_FULL_METRIC_RUNTIME_RANK,
    DERIVED_FROM_GENERIC_GR,
    DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION,
    DRIVER_ONLY_DIFFERENTIAL_STATE_RANK,
    EXTERNAL_CLOSURE_INPUT,
    FROZEN_PHASE_1F_B_DIFFERENTIAL_STATE_RANK,
    GAUGE_CHOICE,
    GLOBAL_PERTURBED_DRESSED_SPACETIME,
    MODEL_SECTOR_RESTRICTION,
    OPTIONAL_METRIC_RECONSTRUCTION_DIFFERENTIAL_RANK,
    ClockAnchoredWallGeometryScenario,
    ClockMapBranch,
    ExternalWallLapsePerturbationClosure,
    H1ToWallSpatialPullback,
    LapseClosureProvenance,
    MetricTraceBackgroundSplit,
    Phase1FCClockError,
    Phase1FCCompatibilityError,
    Phase1FCContractError,
    Phase1FCLapseClosureError,
    Phase1FCMetricReconstructionError,
    Phase1FCNumerics,
    Phase1FCSpatialClosureError,
    Phase1FCStateIntegrityError,
    ScalarMetricTraceInitialData,
    ShiftGauge,
    SpatialClosureProvenance,
    SpatialOperatorInputSemantics,
    TimescapeWallClockBridge,
    WallNormalSector,
    derive_clock_anchored_wall_kinematic_geometry,
    reconstruct_optional_scalar_metric_trace,
)


def numerics() -> Phase1FCNumerics:
    return Phase1FCNumerics(
        clock_alignment_tolerance=2e-13,
        lapse_alignment_tolerance=2e-13,
        boost_clock_residual_tolerance=2e-11,
        expansion_compatibility_tolerance=5e-10,
        lapse_linear_regime_threshold=0.05,
        metric_trace_mean_tolerance=2e-11,
        metric_trace_residual_tolerance=2e-13,
        residual_norm_floor=1e-14,
        metric_trace_integration_method="EXPLICIT_TRAPEZOIDAL_COMMON_TIME_GRID",
    )


def _periodic_reference_operators(
    shape: tuple[int, ...], spacing: tuple[float, ...]
) -> tuple[np.ndarray, np.ndarray]:
    size = int(np.prod(shape))
    gradient = np.zeros((len(shape), size, size), dtype=np.float64)
    laplacian = np.zeros((size, size), dtype=np.float64)
    for index in np.ndindex(shape):
        row = int(np.ravel_multi_index(index, shape))
        for axis, step in enumerate(spacing):
            plus = list(index)
            minus = list(index)
            plus[axis] = (plus[axis] + 1) % shape[axis]
            minus[axis] = (minus[axis] - 1) % shape[axis]
            plus_row = int(np.ravel_multi_index(tuple(plus), shape))
            minus_row = int(np.ravel_multi_index(tuple(minus), shape))
            gradient[axis, row, plus_row] += 1.0 / (2.0 * step)
            gradient[axis, row, minus_row] -= 1.0 / (2.0 * step)
            laplacian[row, plus_row] += 1.0 / step**2
            laplacian[row, row] -= 2.0 / step**2
            laplacian[row, minus_row] += 1.0 / step**2
    return gradient, laplacian


@cache
def make_case(
    scale_factor_value: float = 1.0,
    alpha_values: tuple[float, ...] | None = None,
    time_values: tuple[float, ...] | None = None,
    scale_factor_values: tuple[float, ...] | None = None,
    hubble_values: tuple[float, ...] | None = None,
    lapse_amplitude_values: tuple[float, ...] | None = None,
    initial_potential_amplitude: float = 0.002,
):
    time = (
        np.linspace(0.0, 1.0, 5)
        if time_values is None
        else np.asarray(time_values, dtype=np.float64)
    )
    alpha = (
        np.ones(time.size)
        if alpha_values is None
        else np.asarray(alpha_values, dtype=np.float64)
    )
    lapse_amplitude = (
        -0.001 + 0.0004 * time
        if lapse_amplitude_values is None
        else np.asarray(lapse_amplitude_values, dtype=np.float64)
    )
    scale_factor = (
        np.full(time.size, scale_factor_value)
        if scale_factor_values is None
        else np.asarray(scale_factor_values, dtype=np.float64)
    )
    hubble = (
        np.zeros(time.size)
        if hubble_values is None
        else np.asarray(hubble_values, dtype=np.float64)
    )
    potential_amplitude = np.empty(time.size, dtype=np.float64)
    potential_amplitude[0] = initial_potential_amplitude
    driver = alpha * lapse_amplitude
    for index, dt in enumerate(np.diff(time), start=1):
        potential_amplitude[index] = potential_amplitude[index - 1] - 0.5 * dt * (
            driver[index - 1] + driver[index]
        )
    _, boost_scenario, _, _ = make_phase1f_b_case(
        time=time,
        potential_amplitudes=potential_amplitude,
        lapse_amplitudes=lapse_amplitude,
        proper_time_rate=alpha,
        scale_factor=scale_factor,
        hubble=hubble,
        lapse_kernel_mode=LapseKernelMode.EXPLICIT_Q0_PROJECTION,
    )
    boost = propagate_scalar_dust_wall_boost(
        scenario=boost_scenario, numerics=boost_numerics()
    )
    source_domain = boost.scenario.geometry_closure.wall_domain
    source_shape = source_domain.operator.carrier.grid_shape
    source_mask = source_domain.mask
    wall_indices = np.flatnonzero(source_mask)
    wall_shape = (source_shape[0] // 2, *source_shape[1:])
    selector = np.zeros((wall_indices.size, source_domain.operator.size))
    selector[np.arange(wall_indices.size), wall_indices] = 1.0
    spacing = source_domain.operator.carrier.grid_spacing
    gradient, laplacian = _periodic_reference_operators(wall_shape, spacing)
    pullback = H1ToWallSpatialPullback(
        h1_wall_domain=source_domain,
        pullback_matrix=selector,
        operator_input_semantics=(
            SpatialOperatorInputSemantics.REFERENCE_COMOVING
        ),
        wall_reference_gradient_operators=gradient,
        wall_gradient_component_representation=ComponentRepresentation.COORDINATE_COVECTOR,
        wall_reference_metric_inverse=np.broadcast_to(np.eye(3), (wall_indices.size, 3, 3)),
        wall_reference_laplace_beltrami_operator=laplacian,
        wall_measure_weights=np.full(wall_indices.size, 1.0 / wall_indices.size),
        wall_grid_shape=wall_shape,
        spatial_dimension=3,
        h1_geometry_id=source_domain.geometry.normalization.normalization_id,
        wall_geometry_id="SYNTHETIC_LOCAL_WALL_GEOMETRY",
        pullback_id="EXPLICIT_H1_TO_SYNTHETIC_WALL_PULLBACK",
        morphology_id=source_domain.operator.morphology.morphology_id,
        domain_id="SYNTHETIC_LOCAL_WALL_PATCH",
        boundary_realization_id="EXPLICIT_PERIODIC_SYNTHETIC_WALL_DOMAIN",
        wall_metric_id="SYNTHETIC_FLAT_WALL_REFERENCE_METRIC",
        wall_measure_id="SYNTHETIC_FLAT_WALL_REFERENCE_MEASURE",
        gradient_units="INVERSE_REFERENCE_WALL_LENGTH",
        laplacian_units="INVERSE_REFERENCE_WALL_LENGTH_SQUARED",
        scale_factor_relation=(
            "D_W=a_W^-1 D_gamma_W; D_W^2=a_W^-2 Delta_gamma_W"
        ),
        wall_scale_factor_mapping_id=(
            "EXPLICIT_PHASE1F_B_WALL_SCALE_TO_SELECTED_LOCAL_WALL_PATCH"
        ),
        wall_hubble_mapping_id=(
            "EXPLICIT_PHASE1F_B_COMMON_TIME_HUBBLE_TO_SELECTED_LOCAL_WALL_PATCH"
        ),
        scale_factor_mapping_classification=EXTERNAL_CLOSURE_INPUT,
        provenance=SpatialClosureProvenance.SYNTHETIC_VALIDATION_ONLY,
        scientific_classification=EXTERNAL_CLOSURE_INPUT,
        constant_preservation_tolerance=2e-13,
        operator_symmetry_tolerance=2e-13,
        operator_kernel_tolerance=2e-12,
        operator_coercivity_minimum=1e-8,
    )
    closure_b = boost.scenario.geometry_closure
    lapse_wall = pullback.pullback(closure_b.wall_lapse_perturbation)
    lapse = ExternalWallLapsePerturbationClosure(
        perturbative_wall_lapse=lapse_wall,
        time_grid=time,
        common_spacetime_id=closure_b.common_spacetime_id,
        wall_congruence_id=closure_b.wall_congruence_id,
        common_time_coordinate_id=closure_b.common_time_coordinate_id,
        wall_geometry_id=pullback.wall_geometry_id,
        wall_metric_id=pullback.wall_metric_id,
        domain_id=pullback.domain_id,
        provider_id="SYNTHETIC_VALIDATION_NU_W",
        provenance=LapseClosureProvenance.SYNTHETIC_VALIDATION_ONLY,
        scientific_classification=EXTERNAL_CLOSURE_INPUT,
        lapse_units="DIMENSIONLESS_PERTURBATION",
        interpolation_policy="PIECEWISE_LINEAR_NO_EXTRAPOLATION",
    )
    clock = TimescapeWallClockBridge(
        branch=ClockMapBranch.TIMESCAPE_COMMON_TIME_TO_BACKGROUND_WALL_PROPER_TIME,
        timescape_background_lapse=1.0 / alpha,
        time_grid=time,
        common_time_coordinate_id=closure_b.common_time_coordinate_id,
        timescape_time_coordinate_id=closure_b.common_time_coordinate_id,
        background_wall_proper_time_id="SYNTHETIC_TAU_W",
        timescape_wall_proper_time_id="SYNTHETIC_TAU_W",
        provenance="SELECTED_SYNTHETIC_TIMESCAPE_CLOCK_ANCHOR",
        scientific_classification=DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION,
    )
    scenario = ClockAnchoredWallGeometryScenario(
        boost_result=boost,
        clock_bridge=clock,
        spatial_pullback=pullback,
        lapse_closure=lapse,
        common_spacetime_id=closure_b.common_spacetime_id,
        wall_congruence_id=closure_b.wall_congruence_id,
        regional_wall_dust_congruence_id=closure_b.regional_wall_dust_congruence_id,
        selected_sector=(
            WallNormalSector.SCALAR_LONGITUDINAL_HYPERSURFACE_NORMAL_SHEAR_FREE_LOCAL
        ),
        shift_gauge=ShiftGauge.ZERO_SHIFT,
        metric_signature="(-,+,+,+)",
        extrinsic_curvature_sign="K_ij=-(1/2)L_n h_ij; Theta_W=-K",
        wall_congruence_classification=MODEL_SECTOR_RESTRICTION,
        shift_classification=GAUGE_CHOICE,
        vorticity_classification=DERIVED_FROM_GENERIC_GR,
        shear_classification=MODEL_SECTOR_RESTRICTION,
        local_metric_scope="LOCAL_WALL_PATCH_NOT_GLOBAL_W09_DRESSED_METRIC",
        morphology_classification=EXTERNAL_CLOSURE_INPUT,
        boundary_classification=EXTERNAL_CLOSURE_INPUT,
    )
    result = derive_clock_anchored_wall_kinematic_geometry(
        scenario=scenario, numerics=numerics()
    )
    return scenario, result


def test_clock_bridge_is_explicit_reciprocal_and_has_no_lapse_inference() -> None:
    scenario, _ = make_case()
    clock = scenario.clock_bridge
    np.testing.assert_allclose(
        clock.background_wall_proper_time_rate,
        1.0 / clock.timescape_background_lapse,
        atol=0.0, rtol=0.0,
    )
    assert not hasattr(clock, "perturbative_wall_lapse")
    for parameter in inspect.signature(TimescapeWallClockBridge).parameters.values():
        assert parameter.default is inspect.Parameter.empty


@pytest.mark.parametrize("bad", [0.0, -1.0, np.nan, np.inf])
def test_nonpositive_or_nonfinite_timescape_lapse_is_rejected(bad: float) -> None:
    scenario, _ = make_case()
    gamma = np.array(scenario.clock_bridge.timescape_background_lapse, copy=True)
    gamma[1] = bad
    with pytest.raises((Phase1FCClockError, Phase1FCContractError)):
        replace(scenario.clock_bridge, timescape_background_lapse=gamma)


def test_selected_clock_branch_and_identifications_are_required() -> None:
    scenario, _ = make_case()
    with pytest.raises(Phase1FCClockError):
        replace(scenario.clock_bridge, branch="LOOKALIKE")  # type: ignore[arg-type]
    with pytest.raises(Phase1FCClockError, match="t_common"):
        replace(scenario.clock_bridge, timescape_time_coordinate_id="OTHER_TIME")


def test_first_order_adm_lapse_and_no_hidden_zero_provider() -> None:
    scenario, result = make_case()
    alpha = scenario.clock_bridge.background_wall_proper_time_rate
    expected = alpha[:, None] * (1.0 + scenario.lapse_closure.perturbative_wall_lapse)
    np.testing.assert_allclose(result.adm_lapse_first_order, expected, atol=0.0, rtol=0.0)
    signature = inspect.signature(ClockAnchoredWallGeometryScenario)
    assert signature.parameters["lapse_closure"].default is inspect.Parameter.empty
    with pytest.raises((Phase1FCLapseClosureError, Phase1FCContractError)):
        replace(scenario, lapse_closure=None)  # type: ignore[arg-type]
    strict = replace(numerics(), lapse_linear_regime_threshold=1e-4)
    with pytest.raises(Phase1FCCompatibilityError, match="linear-regime"):
        derive_clock_anchored_wall_kinematic_geometry(
            scenario=scenario, numerics=strict
        )


def test_validation_lapse_is_external_and_synthetic_only() -> None:
    scenario, _ = make_case()
    closure = scenario.lapse_closure
    assert closure.provenance is LapseClosureProvenance.SYNTHETIC_VALIDATION_ONLY
    assert closure.scientific_classification == EXTERNAL_CLOSURE_INPUT
    assert "gamma" not in closure.provider_id.lower()


def test_metric_trace_nonzero_hubble_has_no_double_alpha_factor() -> None:
    """Numerically distinguish the frozen BMR metric-trace equation.

    The independent expected arrays implement BMR Eq. (3.1) and BMR
    Eqs. (2.37)--(2.39); ``H_W^(t)`` is already a common-time rate.
    """

    time = np.linspace(0.0, 1.0, 101)
    alpha = 1.0 + 0.2 * time
    hubble = np.full(time.size, 0.05)
    scale_factor = np.exp(0.05 * time)
    lapse_amplitude = -0.0001 + 0.00004 * time
    _, geometry = make_case(
        alpha_values=tuple(alpha),
        time_values=tuple(time),
        scale_factor_values=tuple(scale_factor),
        hubble_values=tuple(hubble),
        lapse_amplitude_values=tuple(lapse_amplitude),
        initial_potential_amplitude=0.0002,
    )
    initial = ScalarMetricTraceInitialData(
        linear_regime_limit=0.05,  # Explicit synthetic first-order validity budget.
        initial_metric_trace=np.zeros(geometry.scenario.spatial_pullback.wall_size),
        initial_time=float(geometry.time_grid[0]),
        background_split_policy=(
            MetricTraceBackgroundSplit.EXPLICIT_WEIGHTED_MEAN_ZERO_PERTURBATION
        ),
        spatial_measure_id=geometry.scenario.spatial_pullback.wall_measure_id,
        frame_id=geometry.scenario.wall_congruence_id,
        provenance="SYNTHETIC_NONZERO_H_METRIC_TRACE_REGRESSION",
        scientific_classification=EXTERNAL_CLOSURE_INPUT,
    )
    result = reconstruct_optional_scalar_metric_trace(
        geometry=geometry, initial_data=initial, numerics=numerics()
    )
    lapse = geometry.perturbative_wall_lapse
    expansion = geometry.wall_expansion_perturbation
    correct = hubble[:, None] * lapse + alpha[:, None] * expansion / 3.0
    double_alpha_adversary = (
        alpha[:, None] * hubble[:, None] * lapse
        + alpha[:, None] * expansion / 3.0
    )
    np.testing.assert_allclose(
        result.metric_trace_time_derivative, correct, rtol=0.0, atol=2e-15
    )
    assert (
        np.max(
            np.abs(
                result.metric_trace_time_derivative - double_alpha_adversary
            )
        )
        > 1e-7
    )


def test_nonunit_clock_rate_is_load_bearing_and_first_order_consistent() -> None:
    time = np.linspace(0.0, 1.0, 5)
    alpha = tuple(1.0 + 0.2 * time)
    scenario, result = make_case(1.0, alpha)
    np.testing.assert_allclose(
        result.background_wall_proper_time_rate,
        np.asarray(alpha),
        atol=2e-15, rtol=0.0,
    )
    assert result.diagnostics.boost_clock_residual_max_abs <= 2e-11
    assert np.max(np.abs(result.boost_clock_residual)) <= 2e-11


def test_explicit_spatial_pullback_has_no_default_or_h1_operator_alias() -> None:
    scenario, _ = make_case()
    parameter = inspect.signature(ClockAnchoredWallGeometryScenario).parameters[
        "spatial_pullback"
    ]
    assert parameter.default is inspect.Parameter.empty
    pullback = scenario.spatial_pullback
    assert pullback.wall_geometry_id != pullback.h1_geometry_id
    assert not hasattr(pullback, "identity_map_default")
    assert (
        pullback.wall_reference_laplace_beltrami_operator.shape
        != pullback.h1_wall_domain.operator.stiffness_matrix.shape
    )
    with pytest.raises(Phase1FCSpatialClosureError, match="dimensions"):
        replace(pullback, spatial_dimension=2, wall_grid_shape=(4, 8))


def test_spatial_operator_semantics_are_mandatory_typed_and_reference_only() -> None:
    pullback = make_case()[0].spatial_pullback
    parameter = inspect.signature(H1ToWallSpatialPullback).parameters[
        "operator_input_semantics"
    ]
    assert parameter.default is inspect.Parameter.empty
    assert (
        pullback.operator_input_semantics
        is SpatialOperatorInputSemantics.REFERENCE_COMOVING
    )
    assert phase1f_c.SPATIAL_OPERATOR_INPUT_SEMANTICS == "REFERENCE_COMOVING"
    assert phase1f_c.PHYSICAL_LAPLACIAN_SCALING == "APPLIED_BY_PHASE_1F_C"
    assert phase1f_c.PHYSICAL_LAPLACIAN == "D_W^2 = a_W^-2 Delta_reference"
    assert (
        phase1f_c.CALLER_OPERATOR_SPACE_DECLARATION
        == "MANDATORY_TYPED_CONTRACT"
    )
    assert phase1f_c.SILENT_OPERATOR_SPACE_DEFAULT == "FORBIDDEN"
    assert (
        phase1f_c.CALLBACK_NUMERICAL_SEMANTICS_VERIFIABLE_AT_RUNTIME == "NO"
    )
    with pytest.raises(Phase1FCSpatialClosureError, match="REFERENCE_COMOVING"):
        replace(
            pullback,
            operator_input_semantics=SpatialOperatorInputSemantics.WALL_PHYSICAL,
        )
    with pytest.raises(Phase1FCSpatialClosureError, match="REFERENCE_COMOVING"):
        replace(
            pullback,
            operator_input_semantics="REFERENCE_COMOVING",  # type: ignore[arg-type]
        )


def test_reference_to_physical_operator_uses_exact_scale_factor_powers() -> None:
    scenario, result = make_case(2.0)
    reference_laplacian = (
        scenario.spatial_pullback.pullback(scenario.boost_result.scalar_potential)
        @ scenario.spatial_pullback.wall_reference_laplace_beltrami_operator.T
    )
    np.testing.assert_allclose(
        result.wall_laplacian_of_boost_potential,
        reference_laplacian / 4.0,
        atol=2e-14, rtol=0.0,
    )
    reference_acceleration = np.einsum(
        "aij,tj->tia",
        scenario.spatial_pullback.wall_reference_gradient_operators,
        scenario.lapse_closure.perturbative_wall_lapse,
    )
    np.testing.assert_allclose(
        result.wall_acceleration_orthonormal,
        reference_acceleration / 2.0,
        atol=2e-14, rtol=0.0,
    )
    assert np.max(np.abs(reference_laplacian - result.wall_laplacian_of_boost_potential)) > 1.0e-3
    assert np.max(np.abs(reference_acceleration - result.wall_acceleration_orthonormal)) > 1.0e-4
    with pytest.raises(Phase1FCSpatialClosureError, match="scale-factor"):
        replace(scenario.spatial_pullback, scale_factor_relation="D_W^2=Delta_gamma_W")


def test_reference_operator_stays_comoving_across_wall_scale_factors() -> None:
    base_scenario, base_result = make_case(1.0)
    reference = (
        base_scenario.spatial_pullback.wall_reference_laplace_beltrami_operator
    )
    for scale_factor in (2.0, 3.0):
        scenario, result = make_case(scale_factor)
        np.testing.assert_array_equal(
            scenario.spatial_pullback.wall_reference_laplace_beltrami_operator,
            reference,
        )
        np.testing.assert_allclose(
            result.wall_laplacian_of_boost_potential,
            base_result.wall_laplacian_of_boost_potential / scale_factor**2,
            rtol=0.0,
            atol=2e-14,
        )


def test_falsely_labelled_physical_operator_is_a_caller_contract_violation() -> None:
    """Expose the opaque-operator limit without promising introspection.

    At ``a_W=2`` an already-physical ``L_ref/4`` matrix falsely declared
    ``REFERENCE_COMOVING`` is deliberate caller misrepresentation.  The typed
    contract prevents accidental selection of ``WALL_PHYSICAL`` but cannot
    inspect arbitrary numerical semantics.  Phase 1F-C therefore applies the
    BDE Eq. (74) factor again, producing ``L_ref/16`` rather than ``L_ref/4``.
    """

    scenario, _ = make_case(2.0)
    pullback = scenario.spatial_pullback
    reference = pullback.wall_reference_laplace_beltrami_operator
    deliberately_mislabelled = replace(
        pullback,
        operator_input_semantics=SpatialOperatorInputSemantics.REFERENCE_COMOVING,
        wall_reference_laplace_beltrami_operator=reference / 4.0,
    )
    potential = deliberately_mislabelled.pullback(
        scenario.boost_result.scalar_potential
    )
    correct_physical = potential @ reference.T / 4.0
    double_scaled = (
        potential
        @ deliberately_mislabelled.wall_reference_laplace_beltrami_operator.T
        / 4.0
    )
    np.testing.assert_allclose(double_scaled, correct_physical / 4.0, atol=2e-15, rtol=0.0)
    assert np.max(np.abs(double_scaled - correct_physical)) > 1e-3
    with pytest.raises(Phase1FCCompatibilityError, match="incompatible"):
        derive_clock_anchored_wall_kinematic_geometry(
            scenario=replace(scenario, spatial_pullback=deliberately_mislabelled),
            numerics=numerics(),
        )


def test_acceleration_is_wall_gradient_of_external_lapse() -> None:
    scenario, result = make_case()
    expected = np.einsum(
        "aij,tj->tia",
        scenario.spatial_pullback.wall_reference_gradient_operators,
        scenario.lapse_closure.perturbative_wall_lapse,
    ) / scenario.boost_result.scenario.geometry_closure.wall_scale_factor[:, None, None]
    np.testing.assert_allclose(result.wall_acceleration_orthonormal, expected, atol=2e-15, rtol=0.0)
    assert result.acceleration_classification == DERIVED_FROM_GENERIC_GR
    assert np.max(np.abs(result.wall_acceleration_orthonormal)) > 0.0


def test_spatially_homogeneous_lapse_has_zero_acceleration() -> None:
    scenario, _ = make_case()
    homogeneous = np.full_like(scenario.lapse_closure.perturbative_wall_lapse, 1e-4)
    lapse = replace(scenario.lapse_closure, perturbative_wall_lapse=homogeneous)
    # This constructor accepts the explicit closure; operation-time alignment
    # then correctly prevents substituting it for the lapse that drove 1F-B.
    changed = replace(scenario, lapse_closure=lapse)
    expected = np.einsum(
        "aij,tj->tia",
        changed.spatial_pullback.wall_reference_gradient_operators,
        homogeneous,
    )
    assert np.max(np.abs(expected)) <= 2e-13
    with pytest.raises(Phase1FCCompatibilityError, match="differs"):
        derive_clock_anchored_wall_kinematic_geometry(
            scenario=changed, numerics=numerics()
        )


def test_wall_expansion_sign_and_wall_dust_distinction() -> None:
    scenario, result = make_case()
    dust = np.stack(
        [
            scenario.spatial_pullback.pullback(item.delta_theta)
            for item in scenario.boost_result.scenario.dust_expansion_history
        ]
    )
    np.testing.assert_allclose(
        result.wall_laplacian_of_boost_potential
        - dust
        + result.wall_expansion_perturbation,
        0.0,
        atol=2e-14, rtol=0.0,
    )
    assert result.diagnostics.expansion_compatibility_max_abs <= 5e-10
    assert np.max(np.abs(result.wall_expansion_perturbation - dust)) > 0.0
    assert scenario.wall_congruence_id != scenario.regional_wall_dust_congruence_id


def test_opposite_expansion_sign_fails_closed() -> None:
    scenario, _ = make_case()
    boost = scenario.boost_result
    closure_b = boost.scenario.geometry_closure
    dust = np.stack(
        [item.delta_theta for item in boost.scenario.dust_expansion_history]
    )
    reversed_wall_expansion = dust + boost.physical_laplacian_of_potential
    changed_closure = replace(
        closure_b, wall_expansion_perturbation=reversed_wall_expansion
    )
    changed_boost_scenario = replace(
        boost.scenario, geometry_closure=changed_closure
    )
    changed_boost = replace(boost, scenario=changed_boost_scenario)
    bad = replace(scenario, boost_result=changed_boost)
    with pytest.raises(Phase1FCCompatibilityError, match="incompatible"):
        derive_clock_anchored_wall_kinematic_geometry(
            scenario=bad, numerics=numerics()
        )


def test_compatibility_constraint_contains_no_clock_factor() -> None:
    """Behaviorally enforce the frozen BDE constraint's clock independence."""

    time = np.linspace(0.0, 1.0, 5)
    lapse_a = -0.001 + 0.0004 * time
    alpha_a = np.ones(time.size)
    alpha_b = np.full(time.size, 2.0)
    # Keeping alpha*nu fixed keeps the frozen psi history fixed while changing
    # alpha materially; the compatibility equation itself contains no alpha.
    lapse_b = lapse_a / 2.0
    scenario_a, result_a = make_case(
        alpha_values=tuple(alpha_a),
        lapse_amplitude_values=tuple(lapse_a),
    )
    scenario_b, result_b = make_case(
        alpha_values=tuple(alpha_b),
        lapse_amplitude_values=tuple(lapse_b),
    )
    np.testing.assert_allclose(
        scenario_a.boost_result.scalar_potential,
        scenario_b.boost_result.scalar_potential,
        rtol=0.0,
        atol=2e-15,
    )
    np.testing.assert_array_equal(
        scenario_a.spatial_pullback.pullback_matrix,
        scenario_b.spatial_pullback.pullback_matrix,
    )
    np.testing.assert_array_equal(
        scenario_a.spatial_pullback.wall_reference_laplace_beltrami_operator,
        scenario_b.spatial_pullback.wall_reference_laplace_beltrami_operator,
    )
    dust_a = np.stack(
        [
            scenario_a.spatial_pullback.pullback(item.delta_theta)
            for item in scenario_a.boost_result.scenario.dust_expansion_history
        ]
    )
    dust_b = np.stack(
        [
            scenario_b.spatial_pullback.pullback(item.delta_theta)
            for item in scenario_b.boost_result.scenario.dust_expansion_history
        ]
    )
    np.testing.assert_allclose(dust_a, dust_b, rtol=0.0, atol=2e-15)
    expected_a = dust_a - result_a.wall_laplacian_of_boost_potential
    expected_b = dust_b - result_b.wall_laplacian_of_boost_potential
    np.testing.assert_allclose(
        result_a.wall_expansion_perturbation, expected_a, rtol=0.0, atol=2e-15
    )
    np.testing.assert_allclose(
        result_b.wall_expansion_perturbation, expected_b, rtol=0.0, atol=2e-15
    )
    np.testing.assert_allclose(
        result_a.wall_expansion_perturbation,
        result_b.wall_expansion_perturbation,
        rtol=0.0,
        atol=2e-15,
    )
    spurious_alpha_adversary = (
        dust_b - alpha_b[:, None] * result_b.wall_laplacian_of_boost_potential
    )
    assert (
        np.max(
            np.abs(
                result_b.wall_expansion_perturbation - spurious_alpha_adversary
            )
        )
        > 1e-3
    )


def test_metric_trace_requires_explicit_initial_data_and_split() -> None:
    _, geometry = make_case()
    signature = inspect.signature(reconstruct_optional_scalar_metric_trace)
    assert signature.parameters["initial_data"].default is inspect.Parameter.empty
    with pytest.raises(Phase1FCMetricReconstructionError):
        reconstruct_optional_scalar_metric_trace(
            geometry=geometry, initial_data=None, numerics=numerics()  # type: ignore[arg-type]
        )
    with pytest.raises(Phase1FCMetricReconstructionError):
        ScalarMetricTraceInitialData(
            linear_regime_limit=0.05,
            initial_metric_trace=np.zeros(geometry.scenario.spatial_pullback.wall_size),
            initial_time=geometry.time_grid[0],
            background_split_policy="MEAN_ZERO",  # type: ignore[arg-type]
            spatial_measure_id=geometry.scenario.spatial_pullback.wall_measure_id,
            frame_id=geometry.scenario.wall_congruence_id,
            provenance="SYNTHETIC_EXPLICIT_C_W_INITIAL_DATA",
            scientific_classification=EXTERNAL_CLOSURE_INPUT,
        )


def test_optional_metric_trace_equations_and_rank() -> None:
    _, geometry = make_case()
    initial = ScalarMetricTraceInitialData(
        linear_regime_limit=0.05,  # Numerical validity choice, not a prediction.
        initial_metric_trace=np.zeros(geometry.scenario.spatial_pullback.wall_size),
        initial_time=float(geometry.time_grid[0]),
        background_split_policy=(
            MetricTraceBackgroundSplit.EXPLICIT_WEIGHTED_MEAN_ZERO_PERTURBATION
        ),
        spatial_measure_id=geometry.scenario.spatial_pullback.wall_measure_id,
        frame_id=geometry.scenario.wall_congruence_id,
        provenance="SYNTHETIC_EXPLICIT_C_W_INITIAL_DATA",
        scientific_classification=EXTERNAL_CLOSURE_INPUT,
    )
    result = reconstruct_optional_scalar_metric_trace(
        geometry=geometry, initial_data=initial, numerics=numerics()
    )
    closure_b = geometry.scenario.boost_result.scenario.geometry_closure
    expected = (
        closure_b.wall_hubble_rate[:, None] * geometry.perturbative_wall_lapse
        + geometry.background_wall_proper_time_rate[:, None]
        * geometry.wall_expansion_perturbation
        / 3.0
    )
    np.testing.assert_allclose(result.metric_trace_time_derivative, expected, atol=0.0, rtol=0.0)
    assert result.diagnostics.evolution_residual_max_abs <= 2e-13
    assert result.differential_rank_contribution == 1
    assert result.augmented_runtime_rank == 6
    assert result.global_dressed_spacetime_status == GLOBAL_PERTURBED_DRESSED_SPACETIME


def test_sector_gauge_vorticity_shear_and_rank_classifications() -> None:
    scenario, result = make_case()
    assert scenario.wall_congruence_classification == MODEL_SECTOR_RESTRICTION
    assert scenario.shift_classification == GAUGE_CHOICE
    assert scenario.vorticity_classification == DERIVED_FROM_GENERIC_GR
    assert scenario.shear_classification == MODEL_SECTOR_RESTRICTION
    assert result.frozen_phase1f_b_rank == FROZEN_PHASE_1F_B_DIFFERENTIAL_STATE_RANK == 5
    assert result.driver_only_rank == DRIVER_ONLY_DIFFERENTIAL_STATE_RANK == 5
    assert OPTIONAL_METRIC_RECONSTRUCTION_DIFFERENTIAL_RANK == 1
    assert AUGMENTED_FULL_METRIC_RUNTIME_RANK == 6


def test_unsupported_sector_and_silent_identifications_are_rejected() -> None:
    scenario, _ = make_case()
    with pytest.raises(Phase1FCContractError, match="unsupported"):
        replace(scenario, selected_sector="FULL_VECTOR")  # type: ignore[arg-type]
    with pytest.raises(Phase1FCContractError, match="wall-dust"):
        replace(
            scenario,
            regional_wall_dust_congruence_id=scenario.wall_congruence_id,
        )


def test_clock_lapse_spatial_and_frame_mismatches_fail_at_intended_gates() -> None:
    scenario, _ = make_case()
    changed_clock = replace(
        scenario.clock_bridge,
        timescape_background_lapse=np.full(scenario.boost_result.time_grid.size, 2.0),
    )
    with pytest.raises(Phase1FCClockError, match="does not match"):
        derive_clock_anchored_wall_kinematic_geometry(
            scenario=replace(scenario, clock_bridge=changed_clock), numerics=numerics()
        )
    with pytest.raises(Phase1FCLapseClosureError, match="geometry"):
        replace(
            scenario,
            lapse_closure=replace(scenario.lapse_closure, wall_geometry_id="WRONG"),
        )
    with pytest.raises(Phase1FCSpatialClosureError, match="morphology"):
        replace(scenario.spatial_pullback, morphology_id="WRONG")


def test_state_is_immutable_and_low_level_array_tamper_is_detected() -> None:
    scenario, _ = make_case()
    with pytest.raises(FrozenInstanceError):
        scenario.clock_bridge.provenance = "CHANGED"  # type: ignore[misc]
    with pytest.raises(ValueError):
        scenario.lapse_closure.perturbative_wall_lapse[0, 0] = 9.0
    isolated_clock = replace(scenario.clock_bridge)
    isolated_scenario = replace(scenario, clock_bridge=isolated_clock)
    tampered = np.array(isolated_clock.timescape_background_lapse, copy=True)
    object.__setattr__(isolated_clock, "timescape_background_lapse", tampered)
    tampered[0] = 2.0
    with pytest.raises(Phase1FCStateIntegrityError):
        derive_clock_anchored_wall_kinematic_geometry(
            scenario=isolated_scenario, numerics=numerics()
        )


def test_no_predictive_gr_interface_or_observational_public_api() -> None:
    forbidden = (
        "predict_timescape",
        "einstein_source",
        "cmc",
        "physical_gamma_junction",
        "tracer_velocity",
        "redshift_space",
        "likelihood",
        "observational_k",
    )
    public = tuple(name.lower() for name in phase1f_c.__all__)
    for token in forbidden:
        assert all(token not in name for name in public)
    assert phase1f_c.PHYSICAL_INTERFACE_CLAIM == "NOT_GRANTED"
    assert phase1f_c.UNIQUE_TIMESCAPE_PREDICTION == "NOT_GRANTED"
    assert phase1f_c.OBSERVATIONAL_AUTHORIZATION == "NOT_GRANTED"


def test_realization_state_ceiling_is_exact() -> None:
    assert phase1f_c.PHASE == "1F-C"
    assert (
        phase1f_c.REALIZATION_ID
        == "H1-1F-C-CLOCK-ANCHORED-SCALAR-NORMAL-KINEMATIC-GEOMETRY-V1"
    )
    assert phase1f_c.SCIENTIFIC_REALIZATION_READINESS == "READY_FOR_CONDITIONAL_IMPLEMENTATION"
    assert phase1f_c.FULL_GEOMETRIC_CLOSURE_DERIVED == "NO"
    assert phase1f_c.NEW_PERTURBED_GEOMETRIC_DYNAMICS_REQUIRED == "YES"


def test_source_provenance_metadata_not_mathematical_proof() -> None:
    """Citation retention only; behavior/sign tests independently test equations."""
    model_source = inspect.getsource(phase1f_c.TimescapeWallClockBridge)
    spatial_source = inspect.getsource(phase1f_c.H1ToWallSpatialPullback)
    derive_source = inspect.getsource(
        phase1f_c.derive_clock_anchored_wall_kinematic_geometry
    )
    metric_source = inspect.getsource(
        phase1f_c.reconstruct_optional_scalar_metric_trace
    )
    assert "W09 Eq. (B7)" in model_source
    assert "BDE Eq. (74)" in spatial_source
    for citation in (
        "W09 Eq. (B7)",
        "BMR Eq. (2.5)",
        "BMR Eq. (2.6)",
        "BMR Eq. (2.7)",
        "BMR Eqs. (2.29)--(2.30)",
    ):
        assert citation in derive_source
    assert "BMR Eq. (3.1)" in metric_source
    assert "BMR Eqs. (2.37)--(2.39)" in metric_source
