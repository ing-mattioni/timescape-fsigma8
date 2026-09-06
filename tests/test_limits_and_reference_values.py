"""Limiting cases, dimensional scaling, and published reference values.

References: [GM] = arXiv:2511.17160v2; [W09] = arXiv:0909.0749.
Tolerances stated per test (AGENTS.md rule 9).
"""

# A06: absolute budgets use rtol=0; relative budgets use atol=0.
# Previously implicit algebraic comparisons use rtol=2e-12, atol=1e-14
# in the fixture units (roundoff allowance); explicit convergence budgets remain.

import numpy as np
import pytest

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams


# ---------------------------------------------------------------------
# Normalisations at t0
# ---------------------------------------------------------------------

def test_present_day_values(params):
    t0 = params.t0
    assert bg.fv(t0, params) == pytest.approx(params.fv0, rel=1e-14, abs=0.0)
    assert bg.H_D(t0, params) == pytest.approx(params.HD0, rel=1e-14, abs=0.0)
    assert bg.a_D(t0, params) == pytest.approx(1.0 + params.fv0 / 2.0, rel=1e-14, abs=0.0)
    assert bg.gamma_w(t0, params) == pytest.approx(1.0 + params.fv0 / 2.0, rel=1e-14, abs=0.0)
    assert bg.redshift(t0, params) == pytest.approx(0.0, abs=1e-12, rel=0.0)


def test_dressed_bare_H0_relation():
    """HD0 = 2 H0 (2+fv0)/(4 fv0^2 + fv0 + 4), [GM] text p. 25 — round trip."""
    p = TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0)
    assert p.HD0 == pytest.approx(2.0 * 2.737 / (4.0 * 0.737**2 + 0.737 + 4.0), rel=1e-15, abs=0.0)
    assert p.H0_dressed == pytest.approx(1.0, rel=1e-14, abs=0.0)


# ---------------------------------------------------------------------
# Limiting cases
# ---------------------------------------------------------------------

def test_early_time_EdS_limit(params):
    """t -> 0: f_v -> 0 and the model approaches Einstein-de Sitter:
    H -> 2/(3t), a proportional to t^(2/3), Omega_m -> 1, w_eff -> -1/2,
    cs2_eff -> -1/2. Early-time deviations are O(f_v)."""
    t = 1e-8 * params.t0
    f = bg.fv(t, params)
    assert f < 1e-7
    assert bg.H_D(t, params) == pytest.approx(2.0 / (3.0 * t), rel=2.0 * f, abs=0.0)
    ratio = bg.a_D(2.0 * t, params) / bg.a_D(t, params)
    assert ratio == pytest.approx(2.0 ** (2.0 / 3.0), rel=2.0 * f, abs=0.0)
    assert bg.Omega_m(t, params) == pytest.approx(1.0, abs=3.0 * f, rel=0.0)
    assert bg.w_eff(t, params) == pytest.approx(-0.5, abs=f, rel=0.0)
    assert bg.cs2_eff(t, params) == pytest.approx(-0.5, abs=f, rel=0.0)


def test_void_dominated_Milne_limit():
    """f_v -> 1: empty (Milne-like) limit, H -> 1/t, Omega_R -> 1,
    Omega_m, Omega_Q -> 0. Realised at late times for fv0 -> 1."""
    p = TrackerParams(fv0=0.999999, HD0=1.0)
    t = 1e6 * p.t0  # far future: f_v -> 1
    f = bg.fv(t, p)
    assert f > 1.0 - 1e-6
    assert bg.H_D(t, p) == pytest.approx(1.0 / t, rel=1e-6, abs=0.0)
    assert bg.Omega_R(t, p) == pytest.approx(1.0, abs=1e-5, rel=0.0)
    assert bg.Omega_m(t, p) == pytest.approx(0.0, abs=1e-5, rel=0.0)
    assert bg.Omega_Q(t, p) == pytest.approx(0.0, abs=1e-5, rel=0.0)


def test_dimensional_rescaling(params, tgrid):
    """Changing time units: with HD0 -> lambda*HD0 and t -> t/lambda,
    dimensionless quantities are invariant and dimensionful ones scale
    by their power of time. Guards against hidden unit assumptions
    (AGENTS.md rule 4)."""
    lam = 3.7
    p2 = TrackerParams(fv0=params.fv0, HD0=lam * params.HD0)
    t2 = tgrid / lam
    np.testing.assert_allclose(bg.fv(t2, p2), bg.fv(tgrid, params), rtol=1e-13, atol=0.0)
    np.testing.assert_allclose(bg.w_eff(t2, p2), bg.w_eff(tgrid, params), rtol=1e-13, atol=0.0)
    np.testing.assert_allclose(bg.a_D(t2, p2), bg.a_D(tgrid, params), rtol=1e-13, atol=0.0)
    np.testing.assert_allclose(bg.H_D(t2, p2), lam * bg.H_D(tgrid, params), rtol=1e-13, atol=0.0)
    np.testing.assert_allclose(bg.R_D(t2, p2), lam**2 * bg.R_D(tgrid, params), rtol=1e-13, atol=0.0)
    np.testing.assert_allclose(bg.Q_D(t2, p2), lam**2 * bg.Q_D(tgrid, params), rtol=1e-13, atol=0.0)


# ---------------------------------------------------------------------
# Published reference values
# ---------------------------------------------------------------------

def test_HD0_paper_value():
    """[GM] p. 25: 'HD,0 ~ 58.01 km/(s Mpc)' — consistent with the dressed
    H0 = 73.23 km/s/Mpc actually used by the upstream code (see
    reports/upstream_reproducibility.md §11.1 for the 73.03/73.23
    discrepancy in the paper text)."""
    p = TrackerParams.from_dressed_H0(fv0=0.737, H0=73.23)
    assert p.HD0 == pytest.approx(58.01, abs=0.005, rel=0.0)


def test_aD0_over_aw0_paper_value(params):
    """[GM] p. 25: 'a_D,0/a_w,0 = 1 + f_v,0/2 ~ 1.37'."""
    assert bg.a_D(params.t0, params) == pytest.approx(1.37, abs=0.005, rel=0.0)


def test_bare_omegas_today_match_paper_fig1(params):
    """[GM] Fig. 1 (left) endpoint values at aD/aw0 ~ 1.37 (read off the
    published figure, tolerance 0.01): Omega_m ~ 0.14, Omega_R ~ 0.89,
    Omega_Q ~ -0.03. Closed forms: [W09] (B3)-(B5) at fv0 = 0.737."""
    t0 = params.t0
    assert bg.Omega_m(t0, params) == pytest.approx(0.1404, abs=0.001, rel=0.0)
    assert bg.Omega_R(t0, params) == pytest.approx(0.8854, abs=0.001, rel=0.0)
    assert bg.Omega_Q(t0, params) == pytest.approx(-0.0259, abs=0.001, rel=0.0)


def test_w_eff_today_matches_paper_fig1(params):
    """[GM] Fig. 1 (right) w_eff endpoint ~ -0.373 (and w_eff < -1/3
    always, [GM] Sec. 5.1.1 text)."""
    assert bg.w_eff(params.t0, params) == pytest.approx(-0.3735, abs=0.001, rel=0.0)
    t = np.linspace(0.001 * params.t0, params.t0, 200)
    assert np.all(bg.w_eff(t, params) < -1.0 / 3.0)


def test_cs2_eff_today_documented_deviation_D2(params):
    """Deviation (D2): correct c^2_s,eff(t0) = -(2+2fv0-fv0^2)/(2+fv0)^2
    ~ -0.3912, distinct from the upstream/published Fig. 1 value ~ -0.3452
    produced by the upstream dQDdt defect. Both pinned here so any change
    in either understanding fails loudly."""
    ours = bg.cs2_eff(params.t0, params)
    assert ours == pytest.approx(-0.39124, abs=0.0005, rel=0.0)
    upstream_buggy_value = -0.34516
    assert abs(ours - upstream_buggy_value) > 0.04


def test_age_of_universe_in_Gyr():
    """Volume-average age t0 = (2+fv0)/(3 HD0) with the upstream unit
    conversions (h = 0.7323, 1/H0 = 9.778/h Gyr): ~ 15.38 Gyr. Reference
    value from our Phase 1A audit (reports/upstream_reproducibility.md §5),
    cross-checked against the notebook's t0 in code units."""
    p = TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0)
    hubble_time_gyr = 9.778 / 0.7323
    assert p.t0 * hubble_time_gyr == pytest.approx(15.38, abs=0.01, rel=0.0)
