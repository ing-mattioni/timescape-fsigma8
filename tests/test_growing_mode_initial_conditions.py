"""Regular growing-mode initial conditions (review finding F1).

A06: absolute budgets use rtol=0; relative budgets use atol=0.  Budgets:
* 5e-5 / 5e-6 for four- / five-decimal reference values quoted in
  reports/phase1f_c_r_post_remediation_independent_audit.md (independent code);
* 1e-9 for agreement of the logarithmic-rate integration with the frozen
  linear systems (solver tolerances 1e-12 / 2e-13; far-past start offset
  damped below 1e-11);
* 1e-11 for start-fraction and G/time-unit invariance of the same integrator.
"""

import inspect
import json
import sys
from dataclasses import replace
from functools import partial
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import solve_ivp

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.growth import (
    AnchoredDiagnosticAssumptions,
    AnchorProvenanceKind,
    ExternalDensityAmplitudeAnchor,
    GrowthD3Branch,
    GrowthProvenance,
    GrowthSystem,
    anchored_density_growth_diagnostic,
)
from timescape_fsigma8.perturbations import (
    EDS_COMOVING_EFFECTIVE_RATIO,
    EDS_GROWING_LOG_RATE,
    PHASE1C_EPOCH_ROOT,
    PLANCK_2018_QPLUS_RECIPE,
    REGULAR_GROWING_MODE_REFERENCE_CONFIG,
    UPSTREAM_NOTEBOOK_TIME_UNIT,
    BarotropicScenario,
    CleanPerturbationSystem,
    D3Branch,
    EpochChoice,
    EpochScenario,
    GrowingModeConfig,
    GrowingModeInitialConditions,
    InitialConditionScenario,
    RateUnitConvention,
    ResolvedEpoch,
    TiltForm,
    WavenumberConvention,
    comoving_rhs,
    meszaros_rhs,
    regular_growing_mode_coefficients,
    resolve_growing_mode_initial_conditions,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from growth_test_utils import barotropic_scenario, clean_scenario, run_cached  # noqa: E402


PARAMS = TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0)
CONFIG = REGULAR_GROWING_MODE_REFERENCE_CONFIG
GROWING = RateUnitConvention.TIMESCAPE_REGULAR_GROWING_MODE
TIGHT = dict(method="DOP853", rtol=2e-13, atol=1e-30)


def epoch(choice: EpochChoice, params: TrackerParams = PARAMS) -> ResolvedEpoch:
    return EpochScenario(
        choice=choice, time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT, root=PHASE1C_EPOCH_ROOT
    ).resolve(params)


def resolve(system, choice=EpochChoice.UPSTREAM_0P218_GYR, config=CONFIG, G=1.0):
    return resolve_growing_mode_initial_conditions(
        PARAMS,
        recipe=PLANCK_2018_QPLUS_RECIPE,
        system=system,
        epoch=epoch(choice),
        config=config,
        G=G,
    )


def far_past_linear_solution(system, t_end):
    """Frozen linear RHS integrated from deep EdS with the EdS growing state."""
    t_far = 1e-4 * epoch(EpochChoice.DRESSED_Z20).time
    if system is CleanPerturbationSystem.COMOVING:
        rhs = partial(comoving_rhs, params=PARAMS, G=1.0)
        y0 = [t_far ** (2 / 3), -(2 / 3) * t_far ** (-1 / 3), 0.2 * t_far ** (2 / 3)]
    else:
        rhs = partial(meszaros_rhs, params=PARAMS, G=1.0)
        y0 = [t_far ** (2 / 3), (2 / 3) * t_far ** (-1 / 3)]
    return solve_ivp(rhs, (t_far, t_end), y0, dense_output=True, **TIGHT)


def linear_log_rate(system, state, t):
    rate = -state[1] / state[0] if system is CleanPerturbationSystem.COMOVING else state[1] / state[0]
    return t * rate


# ---------------------------------------------------------------- reference values


@pytest.mark.parametrize(
    ("choice", "system", "rate", "ratio"),
    [
        (EpochChoice.UPSTREAM_0P218_GYR, CleanPerturbationSystem.COMOVING, 40.0878, 0.20005),
        (EpochChoice.UPSTREAM_0P218_GYR, CleanPerturbationSystem.MESZAROS, 39.8503, None),
        (EpochChoice.DRESSED_Z20, CleanPerturbationSystem.COMOVING, 44.6209, 0.20005),
        (EpochChoice.DRESSED_Z20, CleanPerturbationSystem.MESZAROS, 44.3828, None),
    ],
)
def test_growing_mode_rates_match_independent_review_values(choice, system, rate, ratio):
    ics = resolve(system, choice)
    assert -ics.expansion_gradient / ics.delta_d == pytest.approx(rate, rel=0.0, abs=5e-5)
    if ratio is None:
        assert ics.effective_ratio is None
        assert ics.delta_eff == 0.0
    else:
        assert ics.effective_ratio == pytest.approx(ratio, rel=0.0, abs=5e-6)
        assert ics.delta_eff == ics.effective_ratio * ics.delta_d


def test_amplitude_is_the_unchanged_recipe_amplitude():
    legacy = InitialConditionScenario(
        recipe=PLANCK_2018_QPLUS_RECIPE,
        rate_units=RateUnitConvention.UPSTREAM_UNCONVERTED,
        timescape_h=0.7323,
    ).resolve(PARAMS)
    for system in CleanPerturbationSystem:
        ics = resolve(system)
        assert ics.delta_d == legacy.delta_d
        assert ics.rate_units is GROWING
        assert ics.initial_time == epoch(EpochChoice.UPSTREAM_0P218_GYR).time


# ----------------------------------------------- independent route and no decay


@pytest.mark.parametrize("system", list(CleanPerturbationSystem))
def test_log_rate_integration_matches_far_past_linear_solution(system):
    times = np.linspace(epoch(EpochChoice.DRESSED_Z20).time, PARAMS.t0, 200)
    linear = far_past_linear_solution(system, PARAMS.t0)
    coefficients = regular_growing_mode_coefficients(
        PARAMS, system=system, times=times, config=CONFIG, G=1.0
    )
    states = linear.sol(times)
    u_linear = linear_log_rate(system, states, times)
    np.testing.assert_allclose(coefficients.log_rate, u_linear, rtol=0.0, atol=1e-9)
    if system is CleanPerturbationSystem.COMOVING:
        np.testing.assert_allclose(
            coefficients.effective_ratio, states[2] / states[0], rtol=0.0, atol=1e-9
        )


@pytest.mark.parametrize("system", list(CleanPerturbationSystem))
def test_growing_mode_trajectory_carries_no_decaying_admixture(system):
    ics = resolve(system)
    t_i = ics.initial_time
    times = np.linspace(t_i, PARAMS.t0, 300)
    if system is CleanPerturbationSystem.COMOVING:
        rhs, y0 = partial(comoving_rhs, params=PARAMS, G=1.0), ics.comoving_vector()
    else:
        rhs, y0 = partial(meszaros_rhs, params=PARAMS, G=1.0), ics.meszaros_vector()
    grown = solve_ivp(rhs, (t_i, PARAMS.t0), y0, t_eval=times, **TIGHT)
    expected = regular_growing_mode_coefficients(
        PARAMS, system=system, times=times, config=CONFIG, G=1.0
    ).log_rate
    np.testing.assert_allclose(
        linear_log_rate(system, grown.y, times), expected, rtol=0.0, atol=1e-9
    )

    legacy = InitialConditionScenario(
        recipe=PLANCK_2018_QPLUS_RECIPE,
        rate_units=RateUnitConvention.UPSTREAM_UNCONVERTED,
        timescape_h=0.7323,
    ).resolve(PARAMS)
    legacy_y0 = (
        legacy.comoving_vector()
        if system is CleanPerturbationSystem.COMOVING
        else legacy.meszaros_vector()
    )
    contaminated = solve_ivp(rhs, (t_i, PARAMS.t0), legacy_y0, t_eval=times, **TIGHT)
    deviation = np.abs(linear_log_rate(system, contaminated.y, times) - expected)
    assert deviation[0] > 0.2  # the review's F1 decaying-mode signature


def test_legacy_decaying_mode_excess_matches_review_headline():
    ics = resolve(CleanPerturbationSystem.COMOVING)
    rhs = partial(comoving_rhs, params=PARAMS, G=1.0)
    growing = solve_ivp(rhs, (ics.initial_time, PARAMS.t0), ics.comoving_vector(), **TIGHT)
    legacy = InitialConditionScenario(
        recipe=PLANCK_2018_QPLUS_RECIPE,
        rate_units=RateUnitConvention.UPSTREAM_UNCONVERTED,
        timescape_h=0.7323,
    ).resolve(PARAMS)
    contaminated = solve_ivp(
        rhs, (ics.initial_time, PARAMS.t0), legacy.comoving_vector(), **TIGHT
    )
    assert contaminated.y[0, -1] / growing.y[0, -1] == pytest.approx(
        1.1312, rel=0.0, abs=5e-5
    )


# ------------------------------------------------------------- limits and scaling


@pytest.mark.parametrize("system", list(CleanPerturbationSystem))
def test_einstein_de_sitter_limit(system):
    nearly_eds = TrackerParams.from_dressed_H0(fv0=1e-7, H0=1.0)
    times = np.array([0.01, 0.1, 1.0]) * nearly_eds.t0
    coefficients = regular_growing_mode_coefficients(
        nearly_eds, system=system, times=times, config=CONFIG, G=1.0
    )
    np.testing.assert_allclose(
        coefficients.log_rate, EDS_GROWING_LOG_RATE, rtol=0.0, atol=1e-6
    )
    if system is CleanPerturbationSystem.COMOVING:
        np.testing.assert_allclose(
            coefficients.effective_ratio, EDS_COMOVING_EFFECTIVE_RATIO, rtol=0.0, atol=1e-6
        )
    assert EDS_GROWING_LOG_RATE**2 + EDS_GROWING_LOG_RATE / 3 - 2 / 3 == pytest.approx(
        0.0, rel=0.0, abs=1e-15
    )


@pytest.mark.parametrize("system", list(CleanPerturbationSystem))
def test_time_unit_rescaling_and_G_invariance(system):
    scale = 13.7
    rescaled = TrackerParams(fv0=PARAMS.fv0, HD0=scale * PARAMS.HD0)
    times = np.array([0.02, 0.3, 1.0]) * PARAMS.t0
    base = regular_growing_mode_coefficients(PARAMS, system=system, times=times, config=CONFIG, G=1.0)
    other = regular_growing_mode_coefficients(
        rescaled, system=system, times=times / scale, config=CONFIG, G=1.0
    )
    heavy_g = regular_growing_mode_coefficients(
        PARAMS, system=system, times=times, config=CONFIG, G=4.49e-15
    )
    np.testing.assert_allclose(other.log_rate, base.log_rate, rtol=0.0, atol=1e-11)
    np.testing.assert_allclose(heavy_g.log_rate, base.log_rate, rtol=0.0, atol=1e-11)

    # Z is a rate: it scales with the inverse time unit.
    t_i = epoch(EpochChoice.UPSTREAM_0P218_GYR).time
    ref_epoch = ResolvedEpoch(
        choice=EpochChoice.UPSTREAM_0P218_GYR, time=t_i, time_gyr=0.218,
        dressed_redshift=float(bg.redshift(t_i, PARAMS)), time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
    )
    scaled_epoch = ResolvedEpoch(
        choice=EpochChoice.UPSTREAM_0P218_GYR, time=t_i / scale, time_gyr=0.218,
        dressed_redshift=float(bg.redshift(t_i / scale, rescaled)), time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
    )
    first = resolve_growing_mode_initial_conditions(
        PARAMS, recipe=PLANCK_2018_QPLUS_RECIPE, system=system, epoch=ref_epoch, config=CONFIG, G=1.0
    )
    second = resolve_growing_mode_initial_conditions(
        rescaled, recipe=PLANCK_2018_QPLUS_RECIPE, system=system, epoch=scaled_epoch, config=CONFIG, G=1.0
    )
    assert second.expansion_gradient == pytest.approx(
        scale * first.expansion_gradient, rel=1e-11, abs=0.0
    )


@pytest.mark.parametrize("system", list(CleanPerturbationSystem))
def test_start_fraction_convergence_and_eds_guard(system):
    times = np.array([epoch(EpochChoice.UPSTREAM_0P218_GYR).time, PARAMS.t0])
    results = [
        regular_growing_mode_coefficients(
            PARAMS,
            system=system,
            times=times,
            config=GrowingModeConfig(
                start_fraction=fraction, eds_limit_tolerance=1e-5,
                method="DOP853", rtol=1e-12, atol=1e-14,
            ),
            G=1.0,
        ).log_rate
        for fraction in (1e-4, 1e-6, 1e-8)
    ]
    np.testing.assert_allclose(results[0], results[2], rtol=0.0, atol=1e-11)
    np.testing.assert_allclose(results[1], results[2], rtol=0.0, atol=1e-11)
    with pytest.raises(ValueError, match="not in the EdS regime"):
        regular_growing_mode_coefficients(
            PARAMS,
            system=system,
            times=times,
            config=GrowingModeConfig(
                start_fraction=0.5, eds_limit_tolerance=1e-5,
                method="DOP853", rtol=1e-12, atol=1e-14,
            ),
            G=1.0,
        )


# ------------------------------------------------------------ fail-closed contract


def test_system_binding_and_barotropic_rejection():
    comoving = resolve(CleanPerturbationSystem.COMOVING)
    meszaros = resolve(CleanPerturbationSystem.MESZAROS)
    assert isinstance(comoving, GrowingModeInitialConditions)
    with pytest.raises(ValueError, match="belong to the comoving system"):
        comoving.meszaros_vector()
    with pytest.raises(ValueError, match="belong to the Mészáros system"):
        meszaros.comoving_vector()
    assert comoving.comoving_vector()[2] == comoving.delta_eff
    with pytest.raises(ValueError, match="clean system and the resolved epoch"):
        InitialConditionScenario(
            recipe=PLANCK_2018_QPLUS_RECIPE, rate_units=GROWING, timescape_h=0.7323
        ).resolve(PARAMS)
    with pytest.raises(ValueError, match="only for the clean"):
        BarotropicScenario(
            k=2.0 * np.pi, branch=D3Branch.DERIVED_4_10, tilt_form=TiltForm.UNRESCALED_V,
            rate_convention=GROWING, epoch_choice=EpochChoice.UPSTREAM_0P218_GYR,
            wavenumber_convention=WavenumberConvention.UPSTREAM_TIMESCAPE_K,
            timescape_h=0.7323, lcdm_h=0.674,
        )
    with pytest.raises(ValueError, match="only for the clean"):
        barotropic_scenario(
            branch=GrowthD3Branch.DERIVED_4_10, mode_k=2.0 * np.pi, mode_label="2pi", rate=GROWING
        )
    with pytest.raises(ValueError, match="CleanPerturbationSystem"):
        resolve("comoving")


def test_explicit_arguments_without_defaults():
    for function in (regular_growing_mode_coefficients, resolve_growing_mode_initial_conditions):
        for parameter in inspect.signature(function).parameters.values():
            assert parameter.default is inspect.Parameter.empty
    for parameter in inspect.signature(GrowingModeConfig).parameters.values():
        assert parameter.default is inspect.Parameter.empty
    for bad in (
        dict(start_fraction=0.0), dict(start_fraction=1.0), dict(eds_limit_tolerance=0.0),
        dict(method="LSODA"), dict(rtol=0.0), dict(atol=float("nan")),
    ):
        values = dict(start_fraction=1e-6, eds_limit_tolerance=1e-5, method="DOP853", rtol=1e-12, atol=1e-14)
        values.update(bad)
        with pytest.raises(ValueError):
            GrowingModeConfig(**values)
    for bad_times in ([], [0.0], [0.2, 0.1], [[0.1]]):
        with pytest.raises(ValueError):
            regular_growing_mode_coefficients(
                PARAMS, system=CleanPerturbationSystem.COMOVING, times=bad_times, config=CONFIG, G=1.0
            )


# ------------------------------------------------------- growth layer and Candidate A


@pytest.mark.parametrize(
    ("system", "clean", "f_today"),
    [
        (GrowthSystem.COMOVING, CleanPerturbationSystem.COMOVING, 0.42491),
        (GrowthSystem.MESZAROS, CleanPerturbationSystem.MESZAROS, 0.31000),
    ],
)
def test_growth_pipeline_history_is_the_regular_solution(system, clean, f_today):
    result = run_cached(clean_scenario(system, rate=GROWING))
    history = result.history
    assert isinstance(history.initial_conditions, GrowingModeInitialConditions)
    assert history.initial_conditions.system is clean
    u = regular_growing_mode_coefficients(
        history.background.params, system=clean, times=history.t, config=CONFIG, G=1.0
    ).log_rate
    expected_f = 3.0 * u / (history.t * bg.Theta(history.t, history.background.params))
    np.testing.assert_allclose(result.rates.f_bare, expected_f, rtol=0.0, atol=1e-9)
    assert result.rates.f_bare[-1] == pytest.approx(f_today, rel=0.0, abs=5e-6)
    metadata = history.to_metadata()["initial_conditions"]
    assert metadata["rate_units"] == "timescape_regular_growing_mode"
    assert metadata["regular_growing_mode"]["system"] == clean.value
    json.dumps(history.to_metadata(), allow_nan=False)


def candidate_a(result):
    """Candidate A with a synthetic validation-only anchor (never observational)."""
    result = replace(
        result,
        history=replace(
            result.history,
            provenance=GrowthProvenance(
                repository_commit="test-fixture",
                upstream_commit="590c6fd5332acb15f5683ebf392a0d7ce54983c5",
                upstream_notebook_sha256="not-used-by-this-test",
            ),
        ),
    )
    return anchored_density_growth_diagnostic(
        growth_result=result,
        anchor=ExternalDensityAmplitudeAnchor(
            sigma8_anchor_at_reference=0.8,
            provenance_label="synthetic growing-mode validation amplitude",
            provenance_kind=AnchorProvenanceKind.SYNTHETIC_VALIDATION_ONLY,
            resolved_reference=result.reference,
            smoothing_radius_definition="synthetic fixed radius label only",
            h_convention="synthetic fixed h-convention label",
            spatial_frame="synthetic matched spatial-frame label",
            reciprocal_units_statement="synthetic reciprocal units in one frame",
        ),
        assumptions=AnchoredDiagnosticAssumptions(
            a1_linear_evolution_acknowledged=True,
            a2_scale_independent_growth_acknowledged=True,
            a3_fixed_reference_spectrum_shape_acknowledged=True,
            a4_fixed_smoothing_convention_acknowledged=True,
            a5_positive_differentiable_growth_acknowledged=True,
            a6_anchor_at_resolved_reference_acknowledged=True,
        ),
    )


def test_candidate_a_growth_is_epoch_independent_on_the_growing_mode():
    values = {}
    for choice in (EpochChoice.UPSTREAM_0P218_GYR, EpochChoice.DRESSED_Z20):
        result = run_cached(clean_scenario(GrowthSystem.COMOVING, rate=GROWING, epoch=choice))
        values[choice] = float(candidate_a(result).relative_growth[-1])
    baseline = values[EpochChoice.UPSTREAM_0P218_GYR]
    assert baseline == pytest.approx(6.164012, rel=0.0, abs=5e-6)
    assert values[EpochChoice.DRESSED_Z20] == pytest.approx(baseline, rel=1e-9, abs=0.0)
