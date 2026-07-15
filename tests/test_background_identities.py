"""Internal consistency of the tracker background implementation.

Each test enforces one of the governing equations of the scientific
specification ([GM] = arXiv:2511.17160v2, [W09] = arXiv:0909.0749) as an
identity on a time grid. Tolerances (AGENTS.md rule 9): identities between
closed forms are algebraically exact and tested at RTOL_EXACT = 1e-12
(double-precision rounding only); comparisons against numerical
differentiation use central differences with step h = 1e-6 * t, whose
truncation error dominates, tested at RTOL_NUM = 1e-7.
"""

import numpy as np
import pytest

import timescape_fsigma8.background as bg

RTOL_EXACT = 1e-12
RTOL_NUM = 1e-7
G = 1.0


def num_deriv(f, t, rel_step=1e-6):
    """Central finite difference with relative step."""
    h = rel_step * t
    return (f(t + h) - f(t - h)) / (2.0 * h)


# ---------------------------------------------------------------------
# Buchert system: [GM] Eqs. (3.8)-(3.11), (3.17)
# ---------------------------------------------------------------------

def test_hamiltonian_constraint_3_8(params, tgrid):
    """3 H_D^2 = 8 pi G rho_d - <R>_D/2 - Q_D/2  (Lambda = 0), [GM] (3.8)."""
    lhs = 3.0 * bg.H_D(tgrid, params) ** 2
    rhs = (8.0 * np.pi * G * bg.rho_d(tgrid, params, G)
           - 0.5 * bg.R_D(tgrid, params) - 0.5 * bg.Q_D(tgrid, params))
    np.testing.assert_allclose(lhs, rhs, rtol=RTOL_EXACT)


def test_raychaudhuri_3_9(params, tgrid):
    """3 addot_D/a_D = -4 pi G rho_d + Q_D  (Lambda = 0), [GM] (3.9).

    addot via numerical differentiation of the analytic da_D/dt.
    """
    addot = num_deriv(lambda t: bg.da_D_dt(t, params), tgrid)
    lhs = 3.0 * addot / bg.a_D(tgrid, params)
    rhs = -4.0 * np.pi * G * bg.rho_d(tgrid, params, G) + bg.Q_D(tgrid, params)
    np.testing.assert_allclose(lhs, rhs, rtol=RTOL_NUM)


def test_mass_conservation_3_10(params, tgrid):
    """drho_d/dt + 3 H_D rho_d = 0, [GM] (3.10). Exact in closed forms."""
    lhs = bg.drho_d_dt(tgrid, params, G)
    rhs = -3.0 * bg.H_D(tgrid, params) * bg.rho_d(tgrid, params, G)
    np.testing.assert_allclose(lhs, rhs, rtol=RTOL_EXACT)


def test_integrability_condition_3_11(params, tgrid):
    """a^-6 (a^6 Q)' + a^-2 (a^2 <R>)' = 0, [GM] (3.11).

    Expanded: dQ/dt + 6 H Q + d<R>/dt + 2 H <R> = 0. This couples our
    derived dQ_D_dt and dR_D_dt to Q_D, R_D, H_D — a strong algebraic
    cross-check of deviation (D2). Residual normalised by |d<R>/dt|.
    """
    H = bg.H_D(tgrid, params)
    resid = (bg.dQ_D_dt(tgrid, params) + 6.0 * H * bg.Q_D(tgrid, params)
             + bg.dR_D_dt(tgrid, params) + 2.0 * H * bg.R_D(tgrid, params))
    scale = np.abs(bg.dR_D_dt(tgrid, params))
    np.testing.assert_array_less(np.abs(resid), RTOL_EXACT * scale)


def test_effective_conservation_3_17(params, tgrid):
    """drho_eff/dt + 3 H_D (rho_eff + p_eff) = 0, [GM] (3.17). Exact."""
    lhs = bg.drho_eff_dt(tgrid, params, G)
    rhs = -3.0 * bg.H_D(tgrid, params) * (
        bg.rho_eff(tgrid, params, G) + bg.p_eff(tgrid, params, G))
    np.testing.assert_allclose(lhs, rhs, rtol=RTOL_EXACT)


# ---------------------------------------------------------------------
# Effective fluid definitions: [GM] Eqs. (3.12), (3.13), Sec. 4 text
# ---------------------------------------------------------------------

def test_rho_eff_definition_3_12(params, tgrid):
    """rho_eff = -(Q_D + <R>_D)/(16 pi G) with K_D = 0, [GM] (3.12)."""
    lhs = bg.rho_eff(tgrid, params, G)
    rhs = -(bg.Q_D(tgrid, params) + bg.R_D(tgrid, params)) / (16.0 * np.pi * G)
    np.testing.assert_allclose(lhs, rhs, rtol=RTOL_EXACT)


def test_p_eff_definition_3_13(params, tgrid):
    """p_eff = -Q_D/(16 pi G) + <R>_D/(48 pi G) with K_D = 0, [GM] (3.13)."""
    lhs = bg.p_eff(tgrid, params, G)
    rhs = (-bg.Q_D(tgrid, params) / (16.0 * np.pi * G)
           + bg.R_D(tgrid, params) / (48.0 * np.pi * G))
    np.testing.assert_allclose(lhs, rhs, rtol=RTOL_EXACT)


def test_w_eff_definition(params, tgrid):
    """w_eff = p_eff / rho_eff, [GM] Sec. 4 text."""
    lhs = bg.w_eff(tgrid, params)
    rhs = bg.p_eff(tgrid, params, G) / bg.rho_eff(tgrid, params, G)
    np.testing.assert_allclose(lhs, rhs, rtol=RTOL_EXACT)


def test_cs2_eff_definition(params, tgrid):
    """c^2_s,eff = (dp_eff/dt)/(drho_eff/dt), [GM] Sec. 4 text."""
    lhs = bg.cs2_eff(tgrid, params)
    rhs = bg.dp_eff_dt(tgrid, params, G) / bg.drho_eff_dt(tgrid, params, G)
    np.testing.assert_allclose(lhs, rhs, rtol=RTOL_EXACT)


# ---------------------------------------------------------------------
# Derived analytic derivatives vs numerical differentiation
# ---------------------------------------------------------------------

@pytest.mark.parametrize("func,deriv", [
    (bg.fv, bg.dfv_dt),
    (bg.dfv_dt, bg.d2fv_dt2),
    (bg.a_D, bg.da_D_dt),
    (bg.R_D, bg.dR_D_dt),
    (bg.Q_D, bg.dQ_D_dt),
], ids=["dfv_dt", "d2fv_dt2", "da_D_dt", "dR_D_dt", "dQ_D_dt"])
def test_analytic_derivatives(params, tgrid, func, deriv):
    num = num_deriv(lambda t: func(t, params), tgrid)
    np.testing.assert_allclose(deriv(tgrid, params), num, rtol=RTOL_NUM)


@pytest.mark.parametrize("func,deriv", [
    (bg.rho_d, bg.drho_d_dt),
    (bg.rho_eff, bg.drho_eff_dt),
    (bg.p_eff, bg.dp_eff_dt),
], ids=["drho_d_dt", "drho_eff_dt", "dp_eff_dt"])
def test_analytic_derivatives_with_G(params, tgrid, func, deriv):
    num = num_deriv(lambda t: func(t, params, G), tgrid)
    np.testing.assert_allclose(deriv(tgrid, params, G), num, rtol=RTOL_NUM)


# ---------------------------------------------------------------------
# Density parameters: [GM] Eq. (3.18) and closure
# ---------------------------------------------------------------------

def test_omega_definitions_3_18(params, tgrid):
    """Closed-form Omegas equal their definitions [GM] (3.18)."""
    H2 = bg.H_D(tgrid, params) ** 2
    np.testing.assert_allclose(
        bg.Omega_m(tgrid, params),
        8.0 * np.pi * G * bg.rho_d(tgrid, params, G) / (3.0 * H2), rtol=RTOL_EXACT)
    np.testing.assert_allclose(
        bg.Omega_R(tgrid, params),
        -bg.R_D(tgrid, params) / (6.0 * H2), rtol=RTOL_EXACT)
    np.testing.assert_allclose(
        bg.Omega_Q(tgrid, params),
        -bg.Q_D(tgrid, params) / (6.0 * H2), rtol=RTOL_EXACT)


def test_omega_sum_is_unity(params, tgrid):
    """Omega_m + Omega_R + Omega_Q = 1 (Lambda = 0), [GM] (3.18)."""
    total = (bg.Omega_m(tgrid, params) + bg.Omega_R(tgrid, params)
             + bg.Omega_Q(tgrid, params))
    np.testing.assert_allclose(total, 1.0, rtol=RTOL_EXACT)


# ---------------------------------------------------------------------
# Dust density scaling: [GM] Eq. (3.16) and normalisation
# ---------------------------------------------------------------------

def test_rho_d_scaling_and_normalisation(params, tgrid):
    """rho_d proportional to a_D^-3 ([GM] (3.16)) with the [GM] Sec. 5.1.1
    normalisation rho_d(t0) = 12 HD0^2 (1-fv0)/(8 pi G (2+fv0)^2)."""
    rho0 = 12.0 * params.HD0**2 * (1.0 - params.fv0) / (
        8.0 * np.pi * G * (2.0 + params.fv0) ** 2)
    expected = rho0 * (bg.a_D(params.t0, params) / bg.a_D(tgrid, params)) ** 3
    np.testing.assert_allclose(bg.rho_d(tgrid, params, G), expected, rtol=RTOL_EXACT)
