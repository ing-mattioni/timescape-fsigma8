"""Initial-condition provenance and explicit scenario choices for Phase 1C-B1."""

# A06: absolute budgets use rtol=0; relative budgets use atol=0.
# Previously implicit algebraic comparisons use rtol=2e-12, atol=1e-14
# in the fixture units (roundoff allowance); explicit convergence budgets remain.

import inspect

import pytest
import scipy

from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations import (
    GYR_TIME_UNIT,
    PHASE1C_EPOCH_ROOT,
    PLANCK_2018_QPLUS_RECIPE,
    UPSTREAM_NOTEBOOK_TIME_UNIT,
    EpochChoice,
    EpochScenario,
    InitialConditionScenario,
    RateUnitConvention,
    qplus,
    qplus_dot,
    solve_comoving,
)
from timescape_fsigma8.presets import NOTEBOOK_REFERENCE


UPSTREAM_DELTA_D = 0.0031427229788258105
UPSTREAM_Z = -0.16974050039281288


def test_qplus_recipe_reproduces_upstream_ics_bit_exactly():
    """[GM] Sec. 5.1.2 ICs using the independently derived flat-LCDM mode.

    SciPy 1.18 (the oracle environment) is bit-exact. SciPy 1.17 differs in
    Z by 1.56e-10 because qplus_prime subtracts incomplete-beta evaluations
    only epsilon=1e-5 apart; that cross-version drift is bounded explicitly.
    """
    recipe = PLANCK_2018_QPLUS_RECIPE
    assert recipe.cmb_factor * qplus(20.0, recipe) == UPSTREAM_DELTA_D
    z_initial = -recipe.cmb_factor * qplus_dot(20.0, recipe)
    assert z_initial == pytest.approx(UPSTREAM_Z, rel=0.0, abs=2e-10)
    if scipy.__version__.startswith("1.18."):
        assert z_initial == UPSTREAM_Z


def test_qplus_cmb_amplitude_matches_published_reference():
    """[GM] Sec. 5.1.2 quotes a typical CMB amplitude of about 6e-5."""
    recipe = PLANCK_2018_QPLUS_RECIPE
    amplitude = recipe.cmb_factor * qplus(1090.0, recipe)
    assert amplitude == pytest.approx(6.05e-5, rel=2e-4, abs=0.0)


def test_rate_unit_scenarios_are_separate_and_explicit():
    params = TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0)
    upstream = InitialConditionScenario(
        recipe=PLANCK_2018_QPLUS_RECIPE,
        rate_units=RateUnitConvention.UPSTREAM_UNCONVERTED,
        timescape_h=0.7323,
    ).resolve(params)
    converted = InitialConditionScenario(
        recipe=PLANCK_2018_QPLUS_RECIPE,
        rate_units=RateUnitConvention.LCDM_TO_TIMESCAPE_CONVERTED,
        timescape_h=0.7323,
    ).resolve(params)

    assert upstream.delta_d == UPSTREAM_DELTA_D
    assert upstream.expansion_gradient == pytest.approx(UPSTREAM_Z, rel=0.0, abs=2e-10)
    assert converted.delta_d == upstream.delta_d
    assert converted.expansion_gradient == pytest.approx(
        upstream.expansion_gradient * (0.674 / 0.7323), rel=1e-15, abs=0.0
    )
    assert converted.expansion_gradient == pytest.approx(
        -0.15622708898642074, rel=0.0, abs=2e-10
    )
    assert converted.delta_eff == upstream.delta_eff == 0.0


def test_meszaros_ic_sign_is_eq_4_21():
    params = TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0)
    initial = InitialConditionScenario(
        recipe=PLANCK_2018_QPLUS_RECIPE,
        rate_units=RateUnitConvention.UPSTREAM_UNCONVERTED,
        timescape_h=0.7323,
    ).resolve(params)
    assert initial.comoving_vector()[0] == UPSTREAM_DELTA_D
    assert initial.comoving_vector()[1] == pytest.approx(UPSTREAM_Z, rel=0.0, abs=2e-10)
    assert initial.comoving_vector()[2] == 0.0
    assert initial.meszaros_vector()[0] == UPSTREAM_DELTA_D
    assert initial.meszaros_vector()[1] == pytest.approx(-UPSTREAM_Z, rel=0.0, abs=2e-10)


def test_epoch_scenarios_reproduce_both_interpretations():
    params_code = TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0)
    upstream = EpochScenario(
        choice=EpochChoice.UPSTREAM_0P218_GYR,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        root=PHASE1C_EPOCH_ROOT,
    ).resolve(params_code)
    dressed_code = EpochScenario(
        choice=EpochChoice.DRESSED_Z20,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        root=PHASE1C_EPOCH_ROOT,
    ).resolve(params_code)
    assert upstream.time == 0.218 * (0.7323 / 9.778)
    assert upstream.time_gyr == pytest.approx(0.218, rel=1e-15, abs=0.0)
    assert upstream.dressed_redshift == pytest.approx(18.58647, abs=1e-5, rel=0.0)
    assert dressed_code.dressed_redshift == pytest.approx(20.0, abs=2e-12, rel=0.0)
    assert dressed_code.time_gyr == pytest.approx(0.19620643, abs=1e-8, rel=0.0)

    # The science interpretation uses the audited exact Gyr conversion in
    # the frozen NOTEBOOK_REFERENCE Phase 1B preset.
    params_gyr = NOTEBOOK_REFERENCE.tracker_params_gyr
    dressed_gyr = EpochScenario(
        choice=EpochChoice.DRESSED_Z20,
        time_unit=GYR_TIME_UNIT,
        root=PHASE1C_EPOCH_ROOT,
    ).resolve(params_gyr)
    assert dressed_gyr.time == pytest.approx(0.19620486433482934, rel=2e-13, abs=0.0)
    assert dressed_gyr.dressed_redshift == pytest.approx(20.0, abs=2e-12, rel=0.0)


def test_scientific_scenario_and_solver_arguments_have_no_defaults():
    ic_signature = inspect.signature(InitialConditionScenario)
    epoch_signature = inspect.signature(EpochScenario)
    solve_signature = inspect.signature(solve_comoving)
    for parameter in ic_signature.parameters.values():
        assert parameter.default is inspect.Parameter.empty
    for parameter in epoch_signature.parameters.values():
        assert parameter.default is inspect.Parameter.empty
    for name in ("params", "initial_conditions", "t_eval", "config", "G"):
        assert solve_signature.parameters[name].default is inspect.Parameter.empty
