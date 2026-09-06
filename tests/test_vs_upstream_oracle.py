"""Validation against the upstream notebook as a numerical oracle.

Requires artifacts/upstream/oracle_background.json, produced by
    .venv/Scripts/python scripts/extract_upstream_oracle.py
(needs the git-ignored upstream clone; tests are skipped when absent).

The oracle and our implementation share the same physics but reach it
through algebraically different routes (upstream composes generic
expressions; we use tracker-reduced closed forms), so agreement is a
meaningful cross-check, not a tautology. Tolerance for equivalent
quantities: RTOL_ORACLE = 1e-9 (both sides are closed-form double
arithmetic; measured differences are <= 1.5e-15 relative — see
artifacts/independent/oracle_comparison_stats.json — dominated by
rounding in different orders of operations).

Two upstream quantities are NOT equivalent by design:

  dQDdt (and everything downstream of it: dKDdt, drhoEffdt, dpEffdt,
  cs2Eff) — upstream defect, documented deviation (D2) in
  src/timescape_fsigma8/background.py. For these we assert:
    (a) our derivative matches numerical differentiation of the ORACLE's
        own validated QD / rhoEff / pEff samples (i.e. upstream data
        contradicts upstream's derivative code, and supports ours);
    (b) the discrepancy with upstream has the predicted magnitude.
"""

# A06: absolute budgets use rtol=0; relative budgets use atol=0.
# Previously implicit algebraic comparisons use rtol=2e-12, atol=1e-14
# in the fixture units (roundoff allowance); explicit convergence budgets remain.

import json
from pathlib import Path

import numpy as np
import pytest

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams

ORACLE_PATH = Path(__file__).resolve().parent.parent / "artifacts" / "upstream" / "oracle_background.json"

RTOL_ORACLE = 1e-9

pytestmark = pytest.mark.skipif(
    not ORACLE_PATH.exists(),
    reason="upstream oracle not extracted (run scripts/extract_upstream_oracle.py)",
)


@pytest.fixture(scope="module")
def oracle():
    data = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))
    data["t"] = np.asarray(data["t"])
    data["values"] = {k: np.asarray(v) for k, v in data["values"].items()}
    return data


@pytest.fixture(scope="module")
def oparams(oracle) -> TrackerParams:
    c = oracle["constants"]
    return TrackerParams(fv0=c["fv0"], HD0=c["HD0"])


@pytest.fixture(scope="module")
def oG(oracle) -> float:
    return oracle["constants"]["G"]


def test_oracle_constants_consistency(oracle, oparams):
    """Upstream derived constants match our parameter object."""
    c = oracle["constants"]
    assert oparams.t0 == pytest.approx(c["t0"], rel=1e-14, abs=0.0)
    assert oparams.aD0 == pytest.approx(c["a0"], rel=1e-14, abs=0.0)
    assert oparams.H0_dressed == pytest.approx(c["H0"], rel=1e-13, abs=0.0)


@pytest.mark.parametrize("ours,theirs,needs_G", [
    (bg.fv, "fv", False),
    (bg.dfv_dt, "dfvdt", False),
    (bg.d2fv_dt2, "d2fvdt", False),
    (bg.a_D, "a", False),
    (bg.da_D_dt, "daDdt", False),
    (bg.Theta, "Theta", False),
    (bg.R_D, "RD", False),   # [D1] regression: upstream RD has no f_v0^(-2/3)
    (bg.Q_D, "QD", False),
    (bg.dR_D_dt, "dRDdt", False),
    (bg.rho_d, "rhod", True),
    (bg.rho_eff, "rhoEff", True),
    (bg.p_eff, "pEff", True),
    (bg.w_eff, "wEff", False),
], ids=lambda x: x if isinstance(x, str) else "")
def test_equivalent_quantities_match_oracle(oracle, oparams, oG, ours, theirs, needs_G):
    t = oracle["t"]
    ref = oracle["values"][theirs]
    val = ours(t, oparams, oG) if needs_G else ours(t, oparams)
    np.testing.assert_allclose(val, ref, rtol=RTOL_ORACLE, atol=0.0)


# Interior window for np.gradient comparisons: the second-order gradient
# has relative truncation error ~ (dt/t)^2, which reaches ~4e-2 at the
# earliest oracle samples (t ~ 5 dt); from sample 50 (t > 0.1 t0) it is
# < 4e-4. Measured maxima for our closed forms on this window: 3.7e-4.
GRAD_WINDOW = slice(50, -1)
GRAD_RTOL = 1e-3


def test_dQ_D_dt_matches_oracle_data_not_oracle_code(oracle, oparams):
    """(D2): our dQ_D/dt matches d/dt of the oracle's own QD samples to
    grid accuracy; upstream's dQDdt is off by a median 54% (measured
    0.42-0.79 on this window)."""
    t = oracle["t"]
    num = np.gradient(oracle["values"]["QD"], t)
    ours = bg.dQ_D_dt(t, oparams)
    theirs = oracle["values"]["dQDdt"]
    np.testing.assert_allclose(ours[GRAD_WINDOW], num[GRAD_WINDOW], rtol=GRAD_RTOL, atol=0.0)
    rel_err_theirs = np.abs(theirs - num)[GRAD_WINDOW] / np.abs(num)[GRAD_WINDOW]
    assert np.median(rel_err_theirs) > 0.3


@pytest.mark.parametrize("ours,theirs,source,min_median", [
    (bg.drho_eff_dt, "drhoEffdt", "rhoEff", 0.02),   # measured median 0.035
    (bg.dp_eff_dt, "dpEffdt", "pEff", 0.05),          # measured median 0.085
], ids=["drho_eff_dt", "dp_eff_dt"])
def test_effective_derivatives_match_oracle_data(oracle, oparams, oG, ours, theirs,
                                                 source, min_median):
    """(D2) downstream: our drho_eff/dt, dp_eff/dt match d/dt of the
    oracle's own rho_eff/p_eff samples; upstream's inherit the dQDdt
    defect (measured: drhoEffdt off 3.4-5.1%, dpEffdt off 7.9-10.6%)."""
    t = oracle["t"]
    num = np.gradient(oracle["values"][source], t)
    val = ours(t, oparams, oG)
    np.testing.assert_allclose(val[GRAD_WINDOW], num[GRAD_WINDOW], rtol=GRAD_RTOL, atol=0.0)
    rel_err_theirs = (np.abs(oracle["values"][theirs] - num)
                      / np.abs(num))[GRAD_WINDOW]
    assert np.median(rel_err_theirs) > min_median


def test_cs2_eff_deviation_D2_quantified(oracle, oparams):
    """(D2): upstream cs2Eff differs from the correct ratio of derivatives.
    Measured relative deviation grows from 4.6% at the first oracle sample
    (t = 0.18 Gyr, f_v ~ 0.03) to 13.4% today: -0.34516 (upstream/published
    Fig. 1) vs -0.39124 (correct). Both endpoints pinned."""
    t = oracle["t"]
    ours = bg.cs2_eff(t, oparams)
    theirs = oracle["values"]["cs2Eff"]
    rel_dev = np.abs(ours - theirs) / np.abs(theirs)
    assert rel_dev[0] < 0.06          # small (but nonzero) early on
    assert rel_dev[-1] > 0.10         # large today
    assert theirs[-1] == pytest.approx(-0.34516, abs=0.0005, rel=0.0)
    assert ours[-1] == pytest.approx(-0.39124, abs=0.0005, rel=0.0)
