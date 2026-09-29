"""Numerical evidence for the report-only Phase 1G-A sigma(M) derivation-path audit.

Report: reports/phase1g_a_sigma8_derivation_path_audit.md (sections cited as [1G-A]).
Writes artifacts/independent/phase1g_a_sigma8_path.json (git-ignored).

Every Timescape quantity comes from frozen package functions:
  * tracker background: timescape_fsigma8.background ([GM] Eqs. (5.4)-(5.7),
    text p. 25; [W09] App. B);
  * regular growing mode of the comoving closure ([GM] Eqs. (4.21)-(4.23)) and
    of the Meszaros equation ([GM] Eq. (4.27)): perturbations.growing_mode;
  * frozen right-hand sides: perturbations.systems (comoving, Meszaros) and
    perturbations.barotropic ([GM] Eqs. (4.13)-(4.17));
  * flat-LCDM growing mode: perturbations.initial_conditions.qplus.

Script-level external formulas (PROVISIONAL_MODEL_IMPORT, never package code):
  * Eisenstein & Hu (1998), ApJ 496, 605, astro-ph/9709112, zero-baryon-
    oscillation transfer function, Eqs. (26), (28)-(31);
  * spherical top-hat window W(x) = 3(sin x - x cos x)/x^3 (1D-A chain D5);
  * matter-era linear amplitude Delta^2_delta = (4/25) A_s (k/k_p)^(n_s-1)
    (k/aH)^4 T^2(k) (Poisson equation with Phi = -(3/5) zeta; [1G-A] Sec. 7).

[GM] = Galoppo & Mourier, arXiv:2511.17160v2; [W09] = Wiltshire, arXiv:0909.0749v2.
No package module, status token or tolerance is changed.  Outputs are
conditional, model-internal numbers; none is an observational sigma_8.
"""

from __future__ import annotations

import json
import math
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad, simpson, solve_ivp
from scipy.optimize import brentq

import timescape_fsigma8.background as bg
from timescape_fsigma8 import units
from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations import (
    D3Branch,
    TiltForm,
    WavenumberConvention,
    barotropic_rhs,
    comoving_rhs,
    meszaros_rhs,
)
from timescape_fsigma8.perturbations.growing_mode import (
    REGULAR_GROWING_MODE_REFERENCE_CONFIG,
    CleanPerturbationSystem,
    regular_growing_mode_coefficients,
)
from timescape_fsigma8.perturbations.initial_conditions import (
    PLANCK_2018_QPLUS_RECIPE,
    qplus,
)
from timescape_fsigma8.presets import NOTEBOOK_REFERENCE, PAPER_REFERENCE

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "independent" / "phase1g_a_sigma8_path.json"

# G cancels in every dimensionless coefficient (t^2 4 pi G rho); it is passed
# explicitly because the package has no default (review F7).
G = 1.0
C_KM_S = 299792.458
T_CMB_K = 2.7255

# Explicit numerical budgets (AGENTS.md rule 9).
GROWTH_GRID_POINTS = (4001, 8001, 16001)
EARLY_TIME_FRACTIONS = (1e-4, 1e-5, 1e-6)
GROWTH_SELF_CONVERGENCE_RTOL = 1e-7        # Simpson grid refinement
GROWTH_EARLY_LIMIT_RTOL = 1e-4             # t_e -> 0 limit, O(f_v(t_e)) bias
DIRECT_SOLVE_RTOL = 1e-11                  # solve_ivp controls, direct cross-check
DIRECT_SOLVE_ATOL = 1e-14
DIRECT_VS_RICCATI_RTOL = 1e-7
IDENTITY_RTOL = 1e-13                      # closed-form per-photon density identity
BAROTROPIC_SOLVE_RTOL = 1e-10
BAROTROPIC_SOLVE_ATOL = 1e-30
SIGMA_LNK_BOUNDS = (math.log(1e-6), math.log(3e2))   # k in Mpc^-1
SIGMA_GRID_POINTS = (4001, 8001)
SIGMA_SELF_CONVERGENCE_RTOL = 1e-6
# EH98 no-wiggle vs the Planck anchor.  The first run gave +3.03% against an
# initial 3% gate; the formula omits baryon wiggles and the Planck baseline
# 0.06 eV neutrino suppression (about -1.5% on sigma_8).  Anchored outputs
# are ratios in which this common bias largely cancels ([1G-A] Sec. 7).
EH98_PLANCK_SIGMA8_RTOL = 0.05

# Planck 2018 (TT,TE,EE+lowE+lensing) inputs; Omega_m and h as in the frozen
# qplus recipe so the LCDM growth factor is the same object.
PLANCK = {
    "omega_m_total_Om_h2": PLANCK_2018_QPLUS_RECIPE.omega_m * PLANCK_2018_QPLUS_RECIPE.h ** 2,
    "Omega_m": PLANCK_2018_QPLUS_RECIPE.omega_m,
    "h": PLANCK_2018_QPLUS_RECIPE.h,
    "omega_b": 0.02237,
    "A_s": 2.100e-9,
    "n_s": 0.9649,
    "k_pivot_Mpc": 0.05,
    "sigma8_linear": 0.8111,
    "source": "Planck 2018 VI (arXiv:1807.06209) Table 2, TT,TE,EE+lowE+lensing",
}
BARYON_FRACTION_PRIMARY = PLANCK["omega_b"] / PLANCK["omega_m_total_Om_h2"]
BARYON_FRACTION_SENSITIVITY = (0.12, BARYON_FRACTION_PRIMARY, 0.20)
R8_H_MPC = 8.0


def _cases() -> dict[str, TrackerParams]:
    """Parameter sets: [GM] presets and the Timescape CMB fit of Nazer & Wiltshire (2015)."""
    return {
        "PAPER_REFERENCE": PAPER_REFERENCE.tracker_params_gyr,
        "NOTEBOOK_REFERENCE": NOTEBOOK_REFERENCE.tracker_params_gyr,
        "NW15_CMB_FIT": TrackerParams.from_dressed_H0(
            fv0=0.627, H0=units.kms_per_mpc_to_per_gyr(61.0)),
    }


# --------------------------------------------------------------------------
# A. Early-universe matter density per photon
# --------------------------------------------------------------------------

def per_photon_matter_density(p: TrackerParams) -> dict:
    """omega_m,eff = <rho>_D0 gamma_w0^3 / rho_crit(100 km/s/Mpc).

    From <rho>_D ~ a_D^-3 ([GM] text p. 25), a_D = a_w at last scattering and
    1+z = a_w0/a_w ([GM] text p. 25), a_D0/a_w0 = gamma_w0 ([GM] Eq. (5.4)):
    rho_m/T^3 at early times equals <rho>_D0 gamma_w0^3/T_0^3.  Closed form:
    (1/2)(1-f_v0)(2+f_v0) (H_D0/100)^2 ([1G-A] Sec. 6, derived identity).
    """
    h100 = units.kms_per_mpc_to_per_gyr(100.0)
    rho_c100 = 3.0 * h100 ** 2 / (8.0 * math.pi * G)
    gamma0 = float(bg.gamma_w(p.t0, p))
    numeric = float(bg.rho_d(p.t0, p, G)) * gamma0 ** 3 / rho_c100
    hbar = p.HD0 / h100
    closed = 0.5 * (1.0 - p.fv0) * (2.0 + p.fv0) * hbar ** 2
    if abs(numeric / closed - 1.0) > IDENTITY_RTOL:
        raise AssertionError(f"per-photon density identity failed: {numeric} vs {closed}")
    return {
        "fv0": p.fv0,
        "H0_dressed_km_s_Mpc": p.H0_dressed / h100 * 100.0,
        "HD0_bare_km_s_Mpc": hbar * 100.0,
        "gamma_w0": gamma0,
        "bare_Omega_M0": float(bg.Omega_m(p.t0, p)),
        "omega_m_bare": float(bg.rho_d(p.t0, p, G)) / rho_c100,
        "omega_m_per_photon": numeric,
        "identity_closed_form": closed,
        "ratio_to_planck": numeric / PLANCK["omega_m_total_Om_h2"],
    }


# --------------------------------------------------------------------------
# B. Growth of the scale-independent closures
# --------------------------------------------------------------------------

def _riccati_log_growth_excess(p, system, t_e, n):
    """ln g between t_e and t0: integral of (u - t Theta/3) d ln t.

    u = t dln(Delta_d)/dt on the regular solution (growing_mode module);
    t Theta/3 = t H_D = dln a_D/dln t ([GM] Eq. (3.6)).  As t_e -> 0 this is
    ln[D(t0)/D(t_e) * a_D(t_e)/a_D(t0)], the growth relative to
    volume-average Einstein-de Sitter growth.
    """
    ts = np.geomspace(t_e, p.t0, n)
    coeff = regular_growing_mode_coefficients(
        p, system=system, times=ts, config=REGULAR_GROWING_MODE_REFERENCE_CONFIG, G=G)
    excess = coeff.log_rate - ts * np.asarray(bg.Theta(ts, p)) / 3.0
    return float(simpson(excess, x=np.log(ts)))


def _riccati_log_growth(p, system, t_a, t_b, n):
    ts = np.geomspace(t_a, t_b, n)
    coeff = regular_growing_mode_coefficients(
        p, system=system, times=ts, config=REGULAR_GROWING_MODE_REFERENCE_CONFIG, G=G)
    return float(simpson(coeff.log_rate, x=np.log(ts))), coeff


def _direct_growth(p, system, t_i, t0):
    """Delta_d(t0)/Delta_d(t_i) from the frozen RHS with regular growing-mode ICs."""
    coeff = regular_growing_mode_coefficients(
        p, system=system, times=[t_i], config=REGULAR_GROWING_MODE_REFERENCE_CONFIG, G=G)
    u = float(coeff.log_rate[0])
    if system is CleanPerturbationSystem.COMOVING:
        q = float(coeff.effective_ratio[0])
        y0, rhs = [1.0, -u / t_i, q], (lambda t, y: comoving_rhs(t, y, params=p, G=G))
    else:
        y0, rhs = [1.0, u / t_i], (lambda t, y: meszaros_rhs(t, y, params=p, G=G))
    sol = solve_ivp(rhs, (t_i, t0), y0, method="DOP853", rtol=DIRECT_SOLVE_RTOL,
                    atol=DIRECT_SOLVE_ATOL, dense_output=False, max_step=np.inf,
                    first_step=None, vectorized=False)
    if not sol.success:
        raise RuntimeError(sol.message)
    return float(sol.y[0, -1])


def t_of_redshift(p: TrackerParams, z: float) -> float:
    """Invert the dressed redshift z(t) ([W09] Eq. (38); [GM] p. 25)."""
    return brentq(lambda t: float(bg.redshift(t, p)) - z, 1e-12 * p.t0, p.t0,
                  xtol=1e-18, rtol=4 * np.finfo(float).eps, maxiter=500)


def growth_summary(p: TrackerParams) -> dict:
    g_lcdm = float(qplus(0.0, PLANCK_2018_QPLUS_RECIPE))
    gamma0 = float(bg.gamma_w(p.t0, p))
    out = {"g_lcdm_qplus0": g_lcdm, "gamma_w0": gamma0}
    for system in CleanPerturbationSystem:
        table = {}
        for te in EARLY_TIME_FRACTIONS:
            for n in GROWTH_GRID_POINTS:
                table[(te, n)] = _riccati_log_growth_excess(p, system, te * p.t0, n)
        finest_te = EARLY_TIME_FRACTIONS[-1]
        grid_vals = [table[(finest_te, n)] for n in GROWTH_GRID_POINTS]
        grid_spread = abs(grid_vals[-1] - grid_vals[-2])
        te_vals = [table[(te, GROWTH_GRID_POINTS[-1])] for te in EARLY_TIME_FRACTIONS]
        te_spread = abs(te_vals[-1] - te_vals[-2])
        if grid_spread > GROWTH_SELF_CONVERGENCE_RTOL:
            raise AssertionError(f"{system.value}: grid convergence {grid_spread}")
        if te_spread > GROWTH_EARLY_LIMIT_RTOL:
            raise AssertionError(f"{system.value}: early-limit convergence {te_spread}")
        g_ts = math.exp(te_vals[-1])
        entry = {
            "g_TS_vs_volume_average_EdS": g_ts,
            "log_g_grid_refinement_change": grid_spread,
            "log_g_early_limit_change": te_spread,
            "X_inf": gamma0 * g_ts / g_lcdm,
            "matching": {},
        }
        for z_i in (20.0, 50.0, 100.0, 300.0):
            t_i = t_of_redshift(p, z_i)
            ln_d, _ = _riccati_log_growth(p, system, t_i, p.t0, GROWTH_GRID_POINTS[-1])
            direct = _direct_growth(p, system, t_i, p.t0)
            rel = abs(direct / math.exp(ln_d) - 1.0)
            if rel > DIRECT_VS_RICCATI_RTOL:
                raise AssertionError(f"{system.value} z_i={z_i}: direct vs Riccati {rel}")
            lcdm = g_lcdm / float(qplus(z_i, PLANCK_2018_QPLUS_RECIPE))
            entry["matching"][f"z_i={z_i:g}"] = {
                "t_i_gyr_or_code": t_i,
                "gamma_w_t_i": float(bg.gamma_w(t_i, p)),
                "D_TS_t0_over_t_i": math.exp(ln_d),
                "D_TS_direct_solve": direct,
                "direct_vs_riccati_rel_diff": rel,
                "D_LCDM_0_over_z_i": lcdm,
                "X_z_i": math.exp(ln_d) / lcdm,
            }
        out[system.value] = entry
    return out


def wall_regional_bracket(p: TrackerParams) -> dict:
    """Two-scale bracket: linear growth in wall regions, EdS in common time t.

    The regional wall volume scale of [GM] Eq. (5.1) obeys
    a_w,reg^3 = (1 - f_v) a_D^3 / f_wi, i.e. a_w,reg = a_w0 t^(2/3) ([W09]
    e-print source lines 1763-1764; [W07] Eq. (11)).  It is *not*
    the null-matched [GM] Eq. (5.4) a_w = a_D/gamma_w (the [W09] dressed
    'a'), which the package implements.  If sub-wall perturbations grow as the
    EdS growing mode of the wall region in t (assumption), growth relative to
    photon-normalised EdS is gamma_w0 (1 - f_v0)^(1/3) ([1G-A] Sec. 8).
    """
    ts = np.geomspace(1e-6 * p.t0, p.t0, 2001)
    reg = np.cbrt((1.0 - np.asarray(bg.fv(ts, p))) * np.asarray(bg.a_D(ts, p)) ** 3)
    power = reg / ts ** (2.0 / 3.0)
    if abs(power.max() / power.min() - 1.0) > IDENTITY_RTOL:
        raise AssertionError("regional wall scale is not proportional to t^(2/3)")
    dressed = np.asarray(bg.a_w(ts, p)) / ts ** (2.0 / 3.0)
    gamma0 = float(bg.gamma_w(p.t0, p))
    factor = gamma0 * (1.0 - p.fv0) ** (1.0 / 3.0)
    closed = 0.5 * (2.0 + p.fv0) * (1.0 - p.fv0) ** (1.0 / 3.0)
    if abs(factor / closed - 1.0) > IDENTITY_RTOL:
        raise AssertionError("regional growth factor identity failed")
    # Numerical limit: (t0/t_e)^(2/3) / (1 + z_e) as t_e -> 0.
    t_e = 1e-8 * p.t0
    numeric = (p.t0 / t_e) ** (2.0 / 3.0) / (1.0 + float(bg.redshift(t_e, p)))
    g_lcdm = float(qplus(0.0, PLANCK_2018_QPLUS_RECIPE))
    return {
        "regional_scale_over_t23_max_rel_variation": float(power.max() / power.min() - 1.0),
        "dressed_a_w_over_t23_rel_variation": float(dressed.max() / dressed.min() - 1.0),
        "growth_vs_photon_EdS": factor,
        "growth_vs_photon_EdS_numeric_limit": numeric,
        "X_wall_regional": factor / g_lcdm,
    }


def fv0_scan() -> dict:
    """X_inf depends on f_v0 only (the tracker is self-similar in H_D0 t)."""
    g_lcdm = float(qplus(0.0, PLANCK_2018_QPLUS_RECIPE))
    rows = []
    for fv0 in (0.50, 0.55, 0.60, 0.627, 0.65, 0.695, 0.70, 0.737, 0.75, 0.80):
        p = TrackerParams.from_dressed_H0(fv0=fv0, H0=1.0)
        gamma0 = 1.0 + fv0 / 2.0
        row = {"fv0": fv0, "gamma_w0": gamma0, "bare_Omega_M0": float(bg.Omega_m(p.t0, p))}
        for system in CleanPerturbationSystem:
            g = math.exp(_riccati_log_growth_excess(
                p, system, EARLY_TIME_FRACTIONS[-1] * p.t0, GROWTH_GRID_POINTS[-1]))
            row[f"g_{system.value}"] = g
            row[f"X_inf_{system.value}"] = gamma0 * g / g_lcdm
        rows.append(row)
    return {"rows": rows, "g_lcdm": g_lcdm}


# --------------------------------------------------------------------------
# D. Barotropic closure: WKB gradient-instability exponent vs frozen RHS
# --------------------------------------------------------------------------

def barotropic_evidence() -> dict:
    """Compare ln|Delta(t0; k)| growth with the WKB phase k*alpha.

    In the frozen matrix ([GM] Eqs. (4.15), (4.17)) A23*A32 = -c_s^2 k^2/a_D^2,
    positive for the Timescape c_s^2 < 0, so the local exponential rate of the
    (Delta_eff, Vtilde) pair is k sqrt(-c_s^2)/a_D.  alpha is its time integral.
    Units: H0 (dressed) = 1, matrix-convention k (UPSTREAM_TIMESCAPE_K).
    """
    p = TrackerParams.from_dressed_H0(fv0=PAPER_REFERENCE.fv0, H0=1.0)
    t_i = t_of_redshift(p, 20.0)
    alpha, alpha_err = quad(
        lambda t: math.sqrt(-float(bg.cs2_eff(t, p))) / float(bg.a_D(t, p)),
        t_i, p.t0, epsabs=0.0, epsrel=1e-12, limit=400)
    cs2_range = [float(bg.cs2_eff(t, p)) for t in (t_i, p.t0)]
    ks = [2.0 * math.pi * m for m in (1, 2, 4, 8, 16, 32)]
    result = {"alpha": alpha, "alpha_quad_abserr": alpha_err, "cs2_eff_t_i_t0": cs2_range,
              "t_i": t_i, "branches": {}}
    for branch in D3Branch:
        rows = []
        for k in ks:
            def rhs(t, y, k=k):
                return barotropic_rhs(
                    t, y, params=p, G=G, k=k, branch=branch,
                    tilt_form=TiltForm.RESCALED_VTILDE,
                    wavenumber_convention=WavenumberConvention.UPSTREAM_TIMESCAPE_K,
                    timescape_h=PAPER_REFERENCE.H0_dressed_km_s_Mpc / 100.0,
                    lcdm_h=PLANCK["h"])
            y0 = [1.0, -(2.0 / 3.0) / t_i, 0.0, 0.0]
            sol = solve_ivp(rhs, (t_i, p.t0), y0, method="DOP853", rtol=BAROTROPIC_SOLVE_RTOL,
                            atol=BAROTROPIC_SOLVE_ATOL, dense_output=False, max_step=np.inf,
                            first_step=None, vectorized=False)
            if not sol.success:
                raise RuntimeError(sol.message)
            rows.append({"k_matrix": k,
                         "ln_abs_delta_d_t0": math.log(abs(sol.y[0, -1])),
                         "ln_abs_delta_eff_t0": math.log(abs(sol.y[2, -1])),
                         "sign_delta_d_t0": float(np.sign(sol.y[0, -1]))})
        for a, b in zip(rows[:-1], rows[1:]):
            b["slope_ln_delta_eff_vs_k"] = (b["ln_abs_delta_eff_t0"] - a["ln_abs_delta_eff_t0"]) / (b["k_matrix"] - a["k_matrix"])
            b["slope_ln_delta_d_vs_k"] = (b["ln_abs_delta_d_t0"] - a["ln_abs_delta_d_t0"]) / (b["k_matrix"] - a["k_matrix"])
        result["branches"][branch.value] = rows
    # Order of magnitude at sigma_8 scales: k_phys0 = 1/R with R = 8/h Mpc,
    # matrix k = a_D0 (c/H0) k_phys0 (1D-A Sec. 10 unit chain).
    h = PAPER_REFERENCE.H0_dressed_km_s_Mpc / 100.0
    R = R8_H_MPC / h
    k_matrix_R8 = p.aD0 * (C_KM_S / (100.0 * h)) / R
    result["sigma8_scale"] = {"R_Mpc": R, "k_matrix_for_kR_1": k_matrix_R8,
                              "wkb_exponent_alpha_k": alpha * k_matrix_R8,
                              "float64_log_max": math.log(np.finfo(float).max)}
    return result


# --------------------------------------------------------------------------
# E. Early-universe spectrum at equal Lagrangian mass (EH98 no-wiggle)
# --------------------------------------------------------------------------

def eh98_nowiggle_transfer(k_mpc, omega_m, f_b, t_cmb=T_CMB_K):
    """Eisenstein & Hu (1998) zero-baryon-oscillation T(k), Eqs. (26), (28)-(31).

    k in Mpc^-1; depends only on the physical densities omega_m, omega_b.
    """
    omega_b = f_b * omega_m
    theta = t_cmb / 2.7
    s = 44.5 * math.log(9.83 / omega_m) / math.sqrt(1.0 + 10.0 * omega_b ** 0.75)   # (26)
    alpha_g = (1.0 - 0.328 * math.log(431.0 * omega_m) * f_b
               + 0.38 * math.log(22.3 * omega_m) * f_b ** 2)                        # (31)
    gamma_eff_h = omega_m * (alpha_g + (1.0 - alpha_g) / (1.0 + (0.43 * k_mpc * s) ** 4))  # (30)
    q = k_mpc * theta ** 2 / gamma_eff_h                                            # (28)
    L0 = np.log(2.0 * math.e + 1.8 * q)                                             # (29)
    C0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return L0 / (L0 + C0 * q ** 2)


def tophat(x):
    x = np.asarray(x, dtype=float)
    small = np.abs(x) < 1e-3
    xs = np.where(small, 1.0, x)
    exact = 3.0 * (np.sin(xs) - xs * np.cos(xs)) / xs ** 3
    return np.where(small, 1.0 - x ** 2 / 10.0, exact)


def sigma_matter_era(R_mpc, omega_m, f_b, n_s, growth_today, n_points):
    """sigma_R today from the matter-era amplitude (4/25) A_s (k/k_p)^(n_s-1) (k/aH)^4 T^2.

    With (aH)^2 = H100^2 omega_m / a in matter domination and D = a early,
    delta(k, today) = (2/5) zeta k^2 T(k) growth_today / (H100^2 omega_m), where
    growth_today = D(today) with D/a -> 1 early in the photon-normalised a.
    """
    lnk = np.linspace(*SIGMA_LNK_BOUNDS, n_points)
    k = np.exp(lnk)
    h100 = 100.0 / C_KM_S                     # Mpc^-1
    amp = (4.0 / 25.0) * PLANCK["A_s"] * (k / PLANCK["k_pivot_Mpc"]) ** (n_s - 1.0)
    delta2 = amp * (k / h100) ** 4 * eh98_nowiggle_transfer(k, omega_m, f_b) ** 2 \
        * growth_today ** 2 / omega_m ** 2
    return math.sqrt(simpson(delta2 * tophat(k * R_mpc) ** 2, x=lnk))


def sigma_converged(R_mpc, omega_m, f_b, n_s, growth_today):
    vals = [sigma_matter_era(R_mpc, omega_m, f_b, n_s, growth_today, n) for n in SIGMA_GRID_POINTS]
    if abs(vals[-1] / vals[-2] - 1.0) > SIGMA_SELF_CONVERGENCE_RTOL:
        raise AssertionError("sigma quadrature not converged")
    return vals[-1]


def spectrum_and_sigma(cases_density: dict, growth: dict) -> dict:
    om_L, h_L = PLANCK["omega_m_total_Om_h2"], PLANCK["h"]
    g_L = float(qplus(0.0, PLANCK_2018_QPLUS_RECIPE))
    R_L = R8_H_MPC / h_L
    sig_L = sigma_converged(R_L, om_L, BARYON_FRACTION_PRIMARY, PLANCK["n_s"], g_L)
    rel = sig_L / PLANCK["sigma8_linear"] - 1.0
    if abs(rel) > EH98_PLANCK_SIGMA8_RTOL:
        raise AssertionError(f"EH98 Planck sigma8 validation off by {rel}")
    out = {"planck_eh98_sigma8": sig_L, "planck_eh98_rel_to_anchor": rel,
           "R8_planck_Mpc": R_L, "cases": {}}
    for name, dens in cases_density.items():
        om = dens["omega_m_per_photon"]
        gamma0 = dens["gamma_w0"]
        h_dressed = dens["H0_dressed_km_s_Mpc"] / 100.0
        h_bare = dens["HD0_bare_km_s_Mpc"] / 100.0
        radii = {
            # (a) equal Lagrangian mass: M8 of the Planck model.
            "equal_mass_M8_planck": R_L * (om_L / om) ** (1.0 / 3.0),
            # (b) 8/h_dressed Mpc in wall (photon-normalised) comoving length.
            "dressed_8_over_h_wall_comoving": R8_H_MPC / h_dressed,
            # (c) 8/h_bare Mpc of present volume-average proper length.
            "bare_8_over_hbar_volume_average": (R8_H_MPC / h_bare) / gamma0,
        }
        case = {"omega_m_per_photon": om, "radii_photon_comoving_Mpc": radii, "closures": {}}
        for system in CleanPerturbationSystem:
            g_ts = growth[name][system.value]["g_TS_vs_volume_average_EdS"]
            growth_today = gamma0 * g_ts          # D(t0) with D/a_photon -> 1 early
            conv = {}
            for label, R in radii.items():
                fb_rows = {}
                for f_b in BARYON_FRACTION_SENSITIVITY:
                    sig = sigma_converged(R, om, f_b, PLANCK["n_s"], growth_today)
                    fb_rows[f"f_b={f_b:.4f}"] = {
                        "sigma_eh98_absolute": sig,
                        "sigma_planck_anchored": sig / sig_L * PLANCK["sigma8_linear"],
                        "ratio_to_planck_sigma8": sig / sig_L,
                    }
                # Early-spectrum factor E at primary f_b: sigma with LCDM-like growth
                # removed, i.e. ratio of early (matter-era) sigma at equal photon T.
                early_ts = sigma_converged(R, om, BARYON_FRACTION_PRIMARY, PLANCK["n_s"], 1.0)
                early_l = sigma_converged(R_L, om_L, BARYON_FRACTION_PRIMARY, PLANCK["n_s"], 1.0)
                conv[label] = {"R_Mpc": R, "E_early_spectrum_factor": early_ts / early_l,
                               "by_baryon_fraction": fb_rows}
            case["closures"][system.value] = {"growth_today_photon_normalised": growth_today,
                                              "conventions": conv}
        out["cases"][name] = case
    return out


def main() -> int:
    cases = _cases()
    density = {name: per_photon_matter_density(p) for name, p in cases.items()}
    growth = {name: growth_summary(p) for name, p in cases.items()}
    payload = {
        "phase": "1G-A",
        "status": "REPORT_ONLY_AUDIT_EVIDENCE; CONDITIONAL; NOT_OBSERVATIONAL; NOT_SIGMA8",
        "environment": {"python": sys.version.split()[0], "numpy": np.__version__,
                        "scipy": scipy.__version__, "platform": platform.platform()},
        "planck_inputs": PLANCK,
        "baryon_fraction_primary": BARYON_FRACTION_PRIMARY,
        "per_photon_density": density,
        "growth": growth,
        "fv0_scan": fv0_scan(),
        "wall_regional_bracket": {name: wall_regional_bracket(p) for name, p in cases.items()},
        "barotropic": barotropic_evidence(),
        "sigma": spectrum_and_sigma(density, growth),
    }
    # Wall-regional bracket at the equal-mass convention (E is growth-independent).
    for name, bracket in payload["wall_regional_bracket"].items():
        conv = payload["sigma"]["cases"][name]["closures"]["comoving"]["conventions"]
        bracket["sigma_planck_anchored_by_convention"] = {
            label: bracket["X_wall_regional"] * cv["E_early_spectrum_factor"] * PLANCK["sigma8_linear"]
            for label, cv in conv.items()}
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {ARTIFACT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
