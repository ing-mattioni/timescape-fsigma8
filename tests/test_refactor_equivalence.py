"""Refactor-equivalence regression: the background package must reproduce
the pre-split monolith bit-for-bit (to floating-point portability).

The GOLDEN values below were computed from the *pre-split* single-module
implementation (src/timescape_fsigma8/background.py at commit 56f22ba)
with TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0), G = 1, at
t = [0.05, 0.4, 1.0] * t0, before the background/ package split
(AGENTS.md rule 3: numerical refactoring must be demonstrably
equivalent). Tolerance: rtol = 1e-13, atol = 1e-15 — tight enough to
catch any formula or operation-order change, loose enough to tolerate
libm differences across CPython builds (this suite runs under both 3.14
and 3.11).

Also asserts backwards-compatible imports: every public name reachable
from `timescape_fsigma8.background` before the split must remain
importable from the same location.
"""

# A06: absolute budgets use rtol=0; relative budgets use atol=0.
# Previously implicit algebraic comparisons use rtol=2e-12, atol=1e-14
# in the fixture units (roundoff allowance); explicit convergence budgets remain.

import numpy as np
import pytest

import timescape_fsigma8
import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams

RTOL = 1e-13
ATOL = 1e-15

GOLDEN_T = [0.05758063333333333, 0.46064506666666666, 1.1516126666666666]

GOLDEN = {
    "fv": [0.12289478072369514, 0.5285048404446038, 0.737],
    "dfv_dt": [1.872012295706543, 0.5409533111347645, 0.168312667627252],
    "d2fv_dt2": [-7.990899970172267, -1.2412873341206978, -0.2154308295346145],
    "a_D": [0.12431575036369436, 0.6115673609492303, 1.3685],
    "H_D": [12.289402748978072, 1.829684083916962, 0.7922223849569793],
    "da_D_dt": [1.527766324260857, 1.1189750665719063, 1.0841563338136262],
    "Theta": [36.868208246934216, 5.489052251750886, 2.3766671548709377],
    "R_D": [-222.39847994802832, -14.944017616622515, -3.334309210620816],
    "Q_D": [21.674096391281363, 0.7828924411720094, 0.09743592471036386],
    "dR_D_dt": [4337.050114208383, 49.58699205873824, 5.029204060087643],
    "dQ_D_dt": [-468.93133116046897, -3.4960047271083496, -0.2093207939707507],
    "w_eff": [-0.47730585264713726, -0.4070461616076684, -0.37346915417191257],
    "cs2_eff": [-0.49497308897391923, -0.4344667632294126, -0.39123813653116096],
    "Omega_m": [0.7784930648453438, 0.2949916011645442, 0.14043202068996175],
    "Omega_R": [0.24542511877942788, 0.7439845211119474, 0.8854425791221637],
    "Omega_Q": [-0.023918183624771473, -0.03897612227649141, -0.025874599812125452],
    "gamma_w": [1.0614473903618475, 1.2642524202223018, 1.3685],
    "redshift": [7.538317849962773, 1.0672333105874419, 2.220446049250313e-16],
}

GOLDEN_WITH_G = {
    "rho_d": [14.034524319947543, 0.11788085215736685, 0.010520630293340678],
    "drho_d_dt": [-517.4277652744887, -0.6470541569727077, -0.025004036466722987],
    "rho_eff": [3.9932847302662298, 0.28172663392700403, 0.0643955479518443],
    "p_eff": [-1.9060181730425165, -0.1146757449626357, -0.02404975082601212],
    "drho_eff_dt": [-76.95377809858526, -0.9169510582268527, -0.09588853086605158],
    "dp_eff_dt": [38.09004925367029, 0.3983847583076054, 0.03751525013074473],
}

# Public API of the pre-split module (must remain importable, same place).
PRE_SPLIT_API = sorted(GOLDEN) + sorted(GOLDEN_WITH_G) + ["TrackerParams"]


@pytest.fixture(scope="module")
def gparams() -> TrackerParams:
    return TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0)


def test_golden_params_unchanged(gparams):
    assert gparams.t0 == pytest.approx(1.1516126666666666, rel=1e-15, abs=0.0)
    assert gparams.HD0 == pytest.approx(0.7922223849569792, rel=1e-15, abs=0.0)
    np.testing.assert_allclose(
        GOLDEN_T, [0.05 * gparams.t0, 0.4 * gparams.t0, 1.0 * gparams.t0], rtol=1e-15, atol=0.0)


@pytest.mark.parametrize("name", sorted(GOLDEN))
def test_golden_values(gparams, name):
    val = getattr(bg, name)(np.asarray(GOLDEN_T), gparams)
    np.testing.assert_allclose(val, GOLDEN[name], rtol=RTOL, atol=ATOL)


@pytest.mark.parametrize("name", sorted(GOLDEN_WITH_G))
def test_golden_values_with_G(gparams, name):
    val = getattr(bg, name)(np.asarray(GOLDEN_T), gparams, 1.0)
    np.testing.assert_allclose(val, GOLDEN_WITH_G[name], rtol=RTOL, atol=ATOL)


def test_backwards_compatible_imports():
    """Every pre-split public name is still importable from
    timescape_fsigma8.background, and TrackerParams from the top level."""
    for name in PRE_SPLIT_API:
        assert hasattr(bg, name), f"missing from timescape_fsigma8.background: {name}"
    assert timescape_fsigma8.TrackerParams is TrackerParams
    # __all__ (if defined) must cover the pre-split API
    if hasattr(bg, "__all__"):
        missing = set(PRE_SPLIT_API) - set(bg.__all__)
        assert not missing, f"__all__ missing pre-split names: {missing}"
