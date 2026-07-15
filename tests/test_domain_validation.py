"""Input-domain validation: the tracker is defined for t > 0 only.

Background functions must reject t <= 0 with ValueError instead of
returning silent infinities/NaNs (input validation, not a formula change —
AGENTS.md rule 3). Exception: tau_w admits t = 0, where its closed form
has the exact finite limit tau_w(0) = 0 ([W09] (B12)).
"""

import numpy as np
import pytest

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams

P = TrackerParams(fv0=0.737, HD0=1.0)

REJECTS_NONPOSITIVE = [
    bg.fv, bg.dfv_dt, bg.d2fv_dt2, bg.a_D, bg.H_D, bg.da_D_dt, bg.Theta,
    bg.R_D, bg.Q_D, bg.dR_D_dt, bg.dQ_D_dt, bg.rho_d, bg.drho_d_dt,
    bg.rho_eff, bg.p_eff, bg.drho_eff_dt, bg.dp_eff_dt, bg.w_eff,
    bg.cs2_eff, bg.Omega_m, bg.Omega_R, bg.Omega_Q, bg.gamma_w,
    bg.dgamma_w_dt, bg.a_w, bg.dtau_w_dt, bg.H_dressed, bg.redshift,
]


@pytest.mark.parametrize("func", REJECTS_NONPOSITIVE, ids=lambda f: f.__name__)
@pytest.mark.parametrize("bad_t", [0.0, -1.0], ids=["zero", "negative"])
def test_rejects_nonpositive_scalar(func, bad_t):
    with pytest.raises(ValueError):
        func(bad_t, P)


@pytest.mark.parametrize("func", [bg.fv, bg.a_D, bg.H_dressed],
                         ids=lambda f: f.__name__)
def test_rejects_array_containing_nonpositive(func):
    with pytest.raises(ValueError):
        func(np.array([0.5, 1.0, 0.0]), P)
    with pytest.raises(ValueError):
        func(np.array([0.5, -0.1, 1.0]), P)


def test_tau_w_admits_zero_rejects_negative():
    assert float(bg.tau_w(0.0, P)) == 0.0
    np.testing.assert_allclose(bg.tau_w(np.array([0.0, P.t0]), P)[0], 0.0)
    with pytest.raises(ValueError):
        bg.tau_w(-1e-9, P)
    with pytest.raises(ValueError):
        bg.tau_w(np.array([0.0, -1.0]), P)


def test_positive_domain_unaffected():
    """Validation must not disturb valid inputs (scalar and array)."""
    assert np.isfinite(float(bg.fv(P.t0, P)))
    vals = bg.fv(np.linspace(0.01, P.t0, 5), P)
    assert np.all(np.isfinite(vals))
