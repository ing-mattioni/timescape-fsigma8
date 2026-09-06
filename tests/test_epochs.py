"""Epoch calculations for both presets: dressed redshift at the upstream
start times, and the time of z_dressed = 20.

Context (reports/background_equation_audit.md §6): the upstream notebook
integrates perturbations from t = 0.218 Gyr and plots the background from
t = 0.18 Gyr, while the paper says figures start from z = 20. These tests
pin what those epochs actually are under each preset.

Method: dressed redshift from [W09] (38) (validated in
test_wall_observables.py); t(z = 20) via scipy.optimize.brentq on
z(t) - 20 over the bracket [1e-4, t0] Gyr with xtol = 1e-12 Gyr and
rtol = 8.9e-16 (documented solver and tolerances; the root is verified
in-test by evaluating z at the solution).

Regression tolerances are numerical (rel 1e-10: both sides are
deterministic closed forms/root-finds), NOT physical-precision claims —
the input parameters carry only 3-4 significant figures. The reported
values (reports/background_validation.md §4) are therefore quoted to
~5 significant digits with that caveat.

Cross-check encoded below: z depends on t only through the product
HD0 * t, so t(z = 20) scales exactly as 1/HD0 between presets.
"""

# A06: absolute budgets use rtol=0; relative budgets use atol=0.
# Previously implicit algebraic comparisons use rtol=2e-12, atol=1e-14
# in the fixture units (roundoff allowance); explicit convergence budgets remain.

import pytest
from scipy.optimize import brentq

import timescape_fsigma8.background as bg
from timescape_fsigma8.presets import NOTEBOOK_REFERENCE, PAPER_REFERENCE

BRENTQ_KW = dict(xtol=1e-12, rtol=8.9e-16)

# Regression values computed by this implementation (audited Gyr units).
EXPECTED = {
    "PAPER_REFERENCE": {          # H0_dressed = 73.03 km/s/Mpc
        "z_at_0.180": 21.27345264694118,
        "z_at_0.218": 18.621831258547562,
        "t_at_z20": 0.1967421910891354,
    },
    "NOTEBOOK_REFERENCE": {       # H0_dressed = 73.23 km/s/Mpc
        "z_at_0.180": 21.2331561139696,
        "z_at_0.218": 18.586371851633583,
        "t_at_z20": 0.19620486433482934,
    },
}

PRESETS = pytest.mark.parametrize(
    "preset", [PAPER_REFERENCE, NOTEBOOK_REFERENCE], ids=lambda p: p.name)


@PRESETS
def test_z_dressed_at_background_start_0p180_Gyr(preset):
    p = preset.tracker_params_gyr
    z = float(bg.redshift(0.180, p))
    assert z == pytest.approx(EXPECTED[preset.name]["z_at_0.180"], rel=1e-10, abs=0.0)
    # Neither preset puts 0.18 Gyr at z = 20.
    assert z > 21.0


@PRESETS
def test_z_dressed_at_perturbation_start_0p218_Gyr(preset):
    p = preset.tracker_params_gyr
    z = float(bg.redshift(0.218, p))
    assert z == pytest.approx(EXPECTED[preset.name]["z_at_0.218"], rel=1e-10, abs=0.0)
    # The upstream perturbation start is z ~ 18.6, not the paper's z = 20.
    assert 18.5 < z < 18.7


@PRESETS
def test_t_at_z_dressed_20(preset):
    p = preset.tracker_params_gyr
    t20 = brentq(lambda t: float(bg.redshift(t, p)) - 20.0, 1e-4, p.t0, **BRENTQ_KW)
    assert t20 == pytest.approx(EXPECTED[preset.name]["t_at_z20"], rel=1e-10, abs=0.0)
    # verify the root and that it differs from both upstream start times
    assert float(bg.redshift(t20, p)) == pytest.approx(20.0, abs=1e-9, rel=0.0)
    assert abs(t20 - 0.218) > 0.02
    assert abs(t20 - 0.180) > 0.015


def test_t_at_z20_scales_inversely_with_HD0():
    """z(t) is a function of HD0*t alone ([W09] (38) with (5.6)), so
    t(z=20) must scale exactly as 1/HD0 between the presets."""
    ratio = (EXPECTED["PAPER_REFERENCE"]["t_at_z20"]
             / EXPECTED["NOTEBOOK_REFERENCE"]["t_at_z20"])
    HD0_ratio = (NOTEBOOK_REFERENCE.tracker_params_gyr.HD0
                 / PAPER_REFERENCE.tracker_params_gyr.HD0)
    assert ratio == pytest.approx(HD0_ratio, rel=1e-9, abs=0.0)
