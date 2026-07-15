"""Wall/dressed-frame observables: a_w, tau_w, gamma_w, H_dressed, redshift.

References: [GM] Eq. (5.4) and text pp. 24-25; [W09] Eqs. (28), (38),
(B7), (B8), (B12). Tolerances (AGENTS.md rule 9): closed-form identities
at RTOL_EXACT = 1e-12; comparisons against central-difference numerical
derivatives (relative step 1e-6, truncation-limited) at RTOL_NUM = 1e-7.
"""

import numpy as np
import pytest

import timescape_fsigma8.background as bg
from timescape_fsigma8.presets import NOTEBOOK_REFERENCE, PAPER_REFERENCE

RTOL_EXACT = 1e-12
RTOL_NUM = 1e-7

PRESETS = pytest.mark.parametrize(
    "preset", [PAPER_REFERENCE, NOTEBOOK_REFERENCE], ids=lambda p: p.name)


def num_deriv(f, t, rel_step=1e-6):
    h = rel_step * t
    return (f(t + h) - f(t - h)) / (2.0 * h)


@pytest.fixture(scope="module")
def gyr_grid():
    """Time grid in Gyr spanning the upstream figure range to today."""
    def make(preset):
        p = preset.tracker_params_gyr
        return p, np.linspace(0.18, p.t0, 300)
    return make


# ---------------------------------------------------------------------
# Required test 1: a_w(t0) = 1
# ---------------------------------------------------------------------

@PRESETS
def test_a_w_today_is_unity(preset):
    """a_w(t0) = 1 exactly: [GM] (5.4) with a_D(t0) = 1 + fv0/2 = gamma_w(t0)."""
    p = preset.tracker_params_gyr
    assert float(bg.a_w(p.t0, p)) == pytest.approx(1.0, rel=RTOL_EXACT)


# ---------------------------------------------------------------------
# Required test 2: dtau_w/dt = 1/gamma_w
# ---------------------------------------------------------------------

@PRESETS
def test_dtau_w_dt_is_inverse_lapse(preset, gyr_grid):
    """dtau_w/dt = 1/gamma_w = 2/(2 + f_v), from gamma_w := dt/dtau_w."""
    p, t = gyr_grid(preset)
    np.testing.assert_allclose(
        bg.dtau_w_dt(t, p), 1.0 / bg.gamma_w(t, p), rtol=RTOL_EXACT)
    np.testing.assert_allclose(
        bg.dtau_w_dt(t, p), 2.0 / (2.0 + bg.fv(t, p)), rtol=RTOL_EXACT)


# ---------------------------------------------------------------------
# Required test 3: numerical d(tau_w)/dt agrees with dtau_w_dt
# ---------------------------------------------------------------------

@PRESETS
def test_tau_w_numerical_derivative(preset, gyr_grid):
    """[W09] (B12) closed form differentiates back to 1/gamma_w."""
    p, t = gyr_grid(preset)
    num = num_deriv(lambda s: bg.tau_w(s, p), t)
    np.testing.assert_allclose(bg.dtau_w_dt(t, p), num, rtol=RTOL_NUM)


def test_dgamma_w_dt_numerical_derivative():
    """dgamma_w/dt (derived) vs numerical differentiation of gamma_w."""
    p = NOTEBOOK_REFERENCE.tracker_params_gyr
    t = np.linspace(0.18, p.t0, 300)
    num = num_deriv(lambda s: bg.gamma_w(s, p), t)
    np.testing.assert_allclose(bg.dgamma_w_dt(t, p), num, rtol=RTOL_NUM)


# ---------------------------------------------------------------------
# Required test 4: H_dressed = (1/a_w) da_w/dtau_w
# ---------------------------------------------------------------------

@PRESETS
def test_H_dressed_is_wall_frame_expansion_rate(preset, gyr_grid):
    """H = (1/a_w) da_w/dtau_w = (gamma_w/a_w) da_w/dt (da_w/dt numerical)."""
    p, t = gyr_grid(preset)
    daw_dt = num_deriv(lambda s: bg.a_w(s, p), t)
    lhs = bg.H_dressed(t, p)
    rhs = bg.gamma_w(t, p) * daw_dt / bg.a_w(t, p)
    np.testing.assert_allclose(lhs, rhs, rtol=RTOL_NUM)


def test_H_dressed_defining_combination():
    """H = gamma_w H_D - dgamma_w/dt ([W09] (28)) — exact in closed forms."""
    p = NOTEBOOK_REFERENCE.tracker_params_gyr
    t = np.linspace(0.18, p.t0, 300)
    rhs = bg.gamma_w(t, p) * bg.H_D(t, p) - bg.dgamma_w_dt(t, p)
    np.testing.assert_allclose(bg.H_dressed(t, p), rhs, rtol=RTOL_EXACT)


# ---------------------------------------------------------------------
# Required test 5: H_dressed(t0) equals the preset dressed H0
# ---------------------------------------------------------------------

@PRESETS
def test_H_dressed_today_equals_preset_H0(preset):
    p = preset.tracker_params_gyr
    assert float(bg.H_dressed(p.t0, p)) == pytest.approx(
        preset.H0_dressed_per_gyr, rel=1e-13)
    assert float(bg.H_dressed(p.t0, p)) == pytest.approx(p.H0_dressed, rel=1e-13)


# ---------------------------------------------------------------------
# Required test 6: H_dressed agrees with [W09] (B8)
# ---------------------------------------------------------------------

@PRESETS
def test_H_dressed_matches_W09_B8(preset, gyr_grid):
    """[W09] (B8): H = (4 f_v^2 + f_v + 4) H_D / (2 (2 + f_v))."""
    p, t = gyr_grid(preset)
    f = bg.fv(t, p)
    rhs = (4.0 * f**2 + f + 4.0) * bg.H_D(t, p) / (2.0 * (2.0 + f))
    np.testing.assert_allclose(bg.H_dressed(t, p), rhs, rtol=RTOL_EXACT)


# ---------------------------------------------------------------------
# Required tests 7-8: redshift = 1/a_w - 1 and [W09] (38)
# ---------------------------------------------------------------------

@PRESETS
def test_redshift_is_inverse_dressed_scale_factor(preset, gyr_grid):
    """1 + z = a_{w,0}/a_w = 1/a_w ([GM] p. 25 via Eq. (5.4))."""
    p, t = gyr_grid(preset)
    np.testing.assert_allclose(
        bg.redshift(t, p), 1.0 / bg.a_w(t, p) - 1.0, rtol=RTOL_EXACT)


@PRESETS
def test_redshift_matches_W09_38(preset, gyr_grid):
    """[W09] (38): 1 + z = (2+f_v) f_v^(1/3) / (3 f_v0^(1/3) HD0 t),
    spelled out independently of the implementation."""
    p, t = gyr_grid(preset)
    f = bg.fv(t, p)
    z38 = (2.0 + f) * np.cbrt(f) / (3.0 * np.cbrt(p.fv0) * p.HD0 * t) - 1.0
    np.testing.assert_allclose(bg.redshift(t, p), z38, rtol=RTOL_EXACT)


# ---------------------------------------------------------------------
# tau_w physical properties
# ---------------------------------------------------------------------

def test_tau_w_zero_at_zero_and_less_than_t():
    """tau_w(0) = 0 exactly; gamma_w > 1 for t > 0 implies tau_w(t) < t
    (wall clocks run slow relative to volume-average time)."""
    p = NOTEBOOK_REFERENCE.tracker_params_gyr
    assert float(bg.tau_w(0.0, p)) == 0.0
    t = np.linspace(0.01, p.t0, 100)
    tau = bg.tau_w(t, p)
    assert np.all(np.diff(tau) > 0.0)
    assert np.all(tau < t)


def test_tau_w_today_reference_value():
    """Wall age of the universe today: tau_w(t0) = 12.262 Gyr for the
    notebook preset (regression value of this implementation with audited
    units — no published value is claimed; [W09] quotes wall ages for
    different best-fit parameters). Below the volume-average age 15.38 Gyr,
    as required by gamma_w > 1."""
    p = NOTEBOOK_REFERENCE.tracker_params_gyr
    tau0 = float(bg.tau_w(p.t0, p))
    assert tau0 < p.t0
    assert tau0 == pytest.approx(12.262, abs=0.005)
