"""Conditional clock-anchored scalar-normal wall kinematics for Phase 1F-C.

Reference keys: W09 is Wiltshire, Phys. Rev. D 80, 123512 (2009),
arXiv:0909.0749; BMR is Buchert--Mourier--Roy, arXiv:1912.04213v2; BDE is
Bruni--Dunsby--Ellis, ApJ 395 (1992) 34.
"""

from __future__ import annotations

import numpy as np

from timescape_fsigma8.phase1f_c.models import (
    AUGMENTED_FULL_METRIC_RUNTIME_RANK,
    COMMON_PERTURBED_4D_SPACETIME,
    DERIVED_FROM_GENERIC_GR,
    DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION,
    DRIVER_ONLY_DIFFERENTIAL_STATE_RANK,
    FROZEN_PHASE_1F_B_DIFFERENTIAL_STATE_RANK,
    GLOBAL_PERTURBED_DRESSED_SPACETIME,
    OPTIONAL_METRIC_RECONSTRUCTION_DIFFERENTIAL_RANK,
    REALIZATION_ID,
    WALL_GEOMETRY_DRIVER,
    WALL_SHEAR,
    WALL_VORTICITY,
    ClockAnchoredWallGeometryScenario,
    MetricTraceBackgroundSplit,
    Phase1FCClockError,
    Phase1FCCompatibilityError,
    Phase1FCMetricReconstructionError,
    Phase1FCNumerics,
    ScalarMetricTraceDiagnostics,
    ScalarMetricTraceInitialData,
    ScalarMetricTraceResult,
    WallKinematicGeometryDiagnostics,
    WallKinematicGeometryResult,
)


def _weighted_mean(values: np.ndarray, weights: np.ndarray) -> np.ndarray:
    return np.sum(values * weights[np.newaxis, :], axis=1) / np.sum(weights)


def _maximum(values: np.ndarray) -> float:
    return float(np.max(np.abs(values))) if values.size else 0.0


def derive_clock_anchored_wall_kinematic_geometry(
    *,
    scenario: ClockAnchoredWallGeometryScenario,
    numerics: Phase1FCNumerics,
) -> WallKinematicGeometryResult:
    """Derive the selected local wall-normal kinematics, fail closed.

    Implemented equations and sources:

    * ``alpha_W=1/gamma_w`` follows from W09 Eq. (B7) only after the explicit
      clock identifications encoded by :class:`TimescapeWallClockBridge`.
    * ``N_W=alpha_W(1+nu_W)`` is the authorised first-order lapse split of
      the ADM metric in BMR Eq. (2.5), with zero shift selected explicitly.
    * ``A_W,i=D_W,i nu_W`` is the first-order normal-congruence acceleration
      from BMR Eq. (2.6).
    * ``deltaTheta_W=deltaTheta_d,w-D_W^2 psi_dw`` has the sign fixed by the
      frame expansion law BDE Eqs. (14)--(16).
    * ``partial_t psi_dw=-alpha_W Q0 nu_W`` applies the explicit clock chain
      rule in BMR Eqs. (2.29)--(2.30) to frozen Phase 1F-B v3.

    These are kinematic identities conditional on the external lapse and
    spatial pullback.  They are not a perturbed Timescape Einstein closure.
    """
    if not isinstance(scenario, ClockAnchoredWallGeometryScenario):
        raise Phase1FCCompatibilityError("explicit Phase 1F-C scenario required")
    if not isinstance(numerics, Phase1FCNumerics):
        raise Phase1FCCompatibilityError("explicit Phase 1F-C numerics required")
    numerics.validate_integrity()
    scenario.validate_integrity()
    boost = scenario.boost_result
    closure_b = boost.scenario.geometry_closure
    pullback = scenario.spatial_pullback
    clock = scenario.clock_bridge
    lapse_closure = scenario.lapse_closure

    alpha = clock.background_wall_proper_time_rate
    alpha_b = closure_b.wall_proper_time_rate
    clock_alignment = alpha - alpha_b
    clock_alignment_max = _maximum(clock_alignment)
    if clock_alignment_max > numerics.clock_alignment_tolerance:
        raise Phase1FCClockError(
            "selected alpha_W=1/gamma_w does not match the frozen Phase 1F-B clock"
        )

    source_lapse = pullback.pullback(closure_b.wall_lapse_perturbation)
    lapse = lapse_closure.perturbative_wall_lapse
    lapse_alignment = lapse - source_lapse
    lapse_alignment_max = _maximum(lapse_alignment)
    if lapse_alignment_max > numerics.lapse_alignment_tolerance:
        raise Phase1FCCompatibilityError(
            "external Phase 1F-C nu_W differs from the lapse that drove Phase 1F-B"
        )
    lapse_max = _maximum(lapse)
    if lapse_max > numerics.lapse_linear_regime_threshold:
        raise Phase1FCCompatibilityError("nu_W violates the explicit linear-regime gate")

    weights = pullback.wall_measure_weights
    lapse_mean = _weighted_mean(lapse, weights)
    projected_lapse = lapse - lapse_mean[:, np.newaxis]
    potential = pullback.pullback(boost.scalar_potential)
    potential_dot = pullback.pullback(boost.scalar_potential_time_derivative)
    clock_residual = potential_dot + alpha[:, np.newaxis] * projected_lapse
    clock_residual_max = _maximum(clock_residual)
    if clock_residual_max > numerics.boost_clock_residual_tolerance:
        raise Phase1FCCompatibilityError(
            "frozen boost violates partial_t psi=-alpha_W Q0 nu_W after pullback"
        )

    wall_scale_factor = closure_b.wall_scale_factor
    laplacian = np.asarray(
        potential @ pullback.wall_reference_laplace_beltrami_operator.T
        / wall_scale_factor[:, np.newaxis] ** 2,
        dtype=np.float64,
    )
    dust = np.stack(
        [pullback.pullback(item.delta_theta) for item in boost.scenario.dust_expansion_history]
    )
    wall_expansion = dust - laplacian
    frozen_wall_expansion = pullback.pullback(closure_b.wall_expansion_perturbation)
    expansion_residual = laplacian - dust + frozen_wall_expansion
    expansion_max = _maximum(expansion_residual)
    expansion_norm = expansion_max / max(
        _maximum(dust) + _maximum(frozen_wall_expansion),
        numerics.residual_norm_floor,
    )
    if expansion_max > numerics.expansion_compatibility_tolerance:
        raise Phase1FCCompatibilityError(
            "derived deltaTheta_W is incompatible with the frozen Phase 1F-B geometry"
        )

    acceleration = np.einsum(
        "aij,tj->tia",
        pullback.wall_reference_gradient_operators,
        lapse,
        optimize=True,
    ) / wall_scale_factor[:, np.newaxis, np.newaxis]
    adm_lapse = alpha[:, np.newaxis] * (1.0 + lapse)
    if np.any(adm_lapse <= 0.0):
        raise Phase1FCCompatibilityError("first-order ADM lapse must stay positive")

    diagnostics = WallKinematicGeometryDiagnostics(
        clock_alignment_max_abs=clock_alignment_max,
        lapse_alignment_max_abs=lapse_alignment_max,
        boost_clock_residual_max_abs=clock_residual_max,
        expansion_compatibility_max_abs=expansion_max,
        expansion_compatibility_normalized_linf=expansion_norm,
        lapse_perturbation_max_abs=lapse_max,
        acceleration_max_abs=_maximum(acceleration),
        clock_alignment_tolerance=numerics.clock_alignment_tolerance,
        lapse_alignment_tolerance=numerics.lapse_alignment_tolerance,
        boost_clock_residual_tolerance=numerics.boost_clock_residual_tolerance,
        expansion_compatibility_tolerance=numerics.expansion_compatibility_tolerance,
        lapse_linear_regime_threshold=numerics.lapse_linear_regime_threshold,
        dimensional_contract_status=(
            "SYNTHETIC_VALIDATION_ONLY_3D"
            if pullback.spatial_dimension == 3
            else "MATHEMATICAL_OPERATOR_FIXTURE_ONLY"
        ),
        state_integrity_status="VALIDATED_AT_OPERATION_TIME",
    )
    result = WallKinematicGeometryResult(
        time_grid=boost.time_grid,
        background_wall_proper_time_rate=alpha,
        adm_lapse_first_order=adm_lapse,
        perturbative_wall_lapse=lapse,
        wall_acceleration_covector=acceleration,
        wall_expansion_perturbation=wall_expansion,
        wall_laplacian_of_boost_potential=laplacian,
        expansion_compatibility_residual=expansion_residual,
        boost_clock_residual=clock_residual,
        diagnostics=diagnostics,
        scenario=scenario,
        numerics=numerics,
        realization_id=REALIZATION_ID,
        acceleration_classification=DERIVED_FROM_GENERIC_GR,
        expansion_classification=DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION,
        vorticity_status=WALL_VORTICITY,
        shear_status=WALL_SHEAR,
        common_spacetime_status=COMMON_PERTURBED_4D_SPACETIME,
        global_dressed_spacetime_status=GLOBAL_PERTURBED_DRESSED_SPACETIME,
        wall_geometry_driver_status=WALL_GEOMETRY_DRIVER,
        frozen_phase1f_b_rank=FROZEN_PHASE_1F_B_DIFFERENTIAL_STATE_RANK,
        driver_only_rank=DRIVER_ONLY_DIFFERENTIAL_STATE_RANK,
    )
    result.validate_integrity()
    return result


def reconstruct_optional_scalar_metric_trace(
    *,
    geometry: WallKinematicGeometryResult,
    initial_data: ScalarMetricTraceInitialData,
    numerics: Phase1FCNumerics,
) -> ScalarMetricTraceResult:
    """Reconstruct optional local ``C_W`` from explicit initial data.

    With BMR Eq. (3.1), its ``K_ij=-h_i^a h_j^b nabla_a n_b`` convention,
    BMR Eqs. (2.37)--(2.39), and the authorised local scalar metric,

    ``partial_t C_W = H_W^(t) nu_W + alpha_W deltaTheta_W/3``.

    ``H_W^(t)`` is already a common-time rate; no second ``alpha_W`` is
    applied.  This optional local trace is not the global W09 dressed metric.
    """
    if not isinstance(geometry, WallKinematicGeometryResult):
        raise Phase1FCMetricReconstructionError("derived wall geometry required")
    if not isinstance(initial_data, ScalarMetricTraceInitialData):
        raise Phase1FCMetricReconstructionError("explicit C_W initial data required")
    if not isinstance(numerics, Phase1FCNumerics):
        raise Phase1FCMetricReconstructionError("explicit numerics required")
    numerics.validate_integrity()
    geometry.validate_integrity()
    initial_data.validate_integrity()
    pullback = geometry.scenario.spatial_pullback
    if initial_data.initial_metric_trace.shape != (pullback.wall_size,):
        raise Phase1FCMetricReconstructionError("C_W initial field shape mismatch")
    if initial_data.initial_time != float(geometry.time_grid[0]):
        raise Phase1FCMetricReconstructionError("C_W initial time must equal first grid time")
    if initial_data.spatial_measure_id != pullback.wall_measure_id:
        raise Phase1FCMetricReconstructionError("C_W spatial measure identity mismatch")
    if initial_data.frame_id != geometry.scenario.wall_congruence_id:
        raise Phase1FCMetricReconstructionError("C_W frame identity mismatch")
    if (
        initial_data.background_split_policy
        is not MetricTraceBackgroundSplit.EXPLICIT_WEIGHTED_MEAN_ZERO_PERTURBATION
    ):
        raise Phase1FCMetricReconstructionError("unsupported C_W background split")

    weights = pullback.wall_measure_weights
    initial_mean = float(np.dot(weights, initial_data.initial_metric_trace) / np.sum(weights))
    if abs(initial_mean) > numerics.metric_trace_mean_tolerance:
        raise Phase1FCMetricReconstructionError(
            "initial C_W violates the explicit weighted-mean-zero split"
        )
    closure_b = geometry.scenario.boost_result.scenario.geometry_closure
    hubble_common = closure_b.wall_hubble_rate
    derivative = (
        hubble_common[:, np.newaxis] * geometry.perturbative_wall_lapse
        + geometry.background_wall_proper_time_rate[:, np.newaxis]
        * geometry.wall_expansion_perturbation
        / 3.0
    )
    derivative_mean = _weighted_mean(derivative, weights)
    if _maximum(derivative_mean) > numerics.metric_trace_mean_tolerance:
        raise Phase1FCMetricReconstructionError(
            "C_W driver violates the explicit background/perturbation split"
        )
    time = geometry.time_grid
    trace = np.empty_like(derivative)
    trace[0] = initial_data.initial_metric_trace
    for index in range(1, time.size):
        dt = float(time[index] - time[index - 1])
        trace[index] = trace[index - 1] + 0.5 * dt * (
            derivative[index - 1] + derivative[index]
        )
    means = _weighted_mean(trace, weights)
    if _maximum(means) > numerics.metric_trace_mean_tolerance:
        raise Phase1FCMetricReconstructionError("reconstructed C_W mean split drifted")
    interval_residuals = []
    for index in range(1, time.size):
        dt = float(time[index] - time[index - 1])
        interval_residuals.append(
            (trace[index] - trace[index - 1]) / dt
            - 0.5 * (derivative[index - 1] + derivative[index])
        )
    evolution_residual = (
        np.stack(interval_residuals)
        if interval_residuals
        else np.zeros((0, pullback.wall_size), dtype=np.float64)
    )
    evolution_max = _maximum(evolution_residual)
    if evolution_max > numerics.metric_trace_residual_tolerance:
        raise Phase1FCMetricReconstructionError("C_W integration residual exceeds tolerance")
    diagnostics = ScalarMetricTraceDiagnostics(
        initial_weighted_mean_residual=initial_mean,
        reconstructed_weighted_mean_max_abs=_maximum(means),
        evolution_residual_max_abs=evolution_max,
        mean_tolerance=numerics.metric_trace_mean_tolerance,
        evolution_tolerance=numerics.metric_trace_residual_tolerance,
        integration_method=numerics.metric_trace_integration_method,
    )
    result = ScalarMetricTraceResult(
        time_grid=time,
        metric_trace_perturbation=trace,
        metric_trace_time_derivative=derivative,
        diagnostics=diagnostics,
        geometry=geometry,
        initial_data=initial_data,
        differential_rank_contribution=OPTIONAL_METRIC_RECONSTRUCTION_DIFFERENTIAL_RANK,
        augmented_runtime_rank=AUGMENTED_FULL_METRIC_RUNTIME_RANK,
        scientific_classification=DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION,
        global_dressed_spacetime_status=GLOBAL_PERTURBED_DRESSED_SPACETIME,
    )
    result.validate_integrity()
    return result
