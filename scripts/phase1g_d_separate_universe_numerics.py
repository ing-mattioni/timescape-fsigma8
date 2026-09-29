"""Numerical evidence for the report-only Phase 1G-D separate-universe audit.

Report: reports/phase1g_d_separate_universe_growth.md (sections cited as [1G-D]).
Writes artifacts/independent/phase1g_d_separate_universe.json (git-ignored).

Every Timescape background quantity comes from frozen package functions
(timescape_fsigma8.background; [GM] Eqs. (3.12)-(3.13), (5.1), (5.3)-(5.7));
the comoving regular growing mode from perturbations.growing_mode.  The
separate-universe perturbations are the analytic two-region formulas of
[1G-D] Sec. 3 (derived from [W09] Eq. (Q1) and the [GM] definitions).  The
early spectrum reuses the 1G-A EH98 import unchanged.

[GM] = Galoppo & Mourier, arXiv:2511.17160v2; [W09] = Wiltshire,
arXiv:0909.0749v2; [SvdW04] = Sheth & van de Weygaert, MNRAS 350, 517
(astro-ph/0311260).  No package module, status token or tolerance changes.
"""

from __future__ import annotations

import importlib.util
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import cumulative_simpson, simpson
from scipy.optimize import brentq
from scipy.stats import norm

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations.growing_mode import (
    REGULAR_GROWING_MODE_REFERENCE_CONFIG,
    CleanPerturbationSystem,
    regular_growing_mode_coefficients,
)
from timescape_fsigma8.perturbations.initial_conditions import PLANCK_2018_QPLUS_RECIPE, qplus

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "independent" / "phase1g_d_separate_universe.json"
_spec = importlib.util.spec_from_file_location(
    "phase1g_a_numerics", ROOT / "scripts" / "phase1g_a_sigma8_path_numerics.py")
g1a = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g1a)

G = 1.0
# Explicit budgets (AGENTS.md rule 9).
ONE_SCALE_RTOL = 1e-13               # f_v = t/(t+tau)
RAYCHAUDHURI_RTOL = 1e-12            # [GM] (4.11) residual / largest term, analytic derivatives
EPS_MODE_PACKAGE_RTOL = 1e-5         # linear eps-mode vs package at tau(1+1e-7): O(eps) + FD
EPS_PROBE = 1e-7
SIGMA_X_BOUNDS = (1e-4, 200.0)       # x = kR range of the large-R sigma quadrature
SIGMA_X_POINTS = (20001, 40001)
SIGMA_X_RTOL = 1e-8
GROWTH_GRID = 40001
EARLY_FRACTION = 1e-7
A_LS = 1.0 / 1091.0                  # photon-normalised scale factor at last scattering
SVDW_SHELL_CROSSING_RADIUS_FACTOR = 1.72   # [SvdW04]: R_Eul = 1.72 R_Lag at shell crossing
W09_VOID_DIAMETER_H_MPC = 30.0             # [W09] line 277
W09_FVI_RANGE = (1e-4, 1e-2)               # [W09] line 1815
W09_DELTA_H_RANGE = (1e-5, 1e-6)           # [W09] line 1814 (|delta_H|)


def tau_of(p: TrackerParams) -> float:
    """Void-onset time tau = (2+f_v0)(1-f_v0)/(3 f_v0 H_D0) (= Phase 1F-D's b)."""
    return (2.0 + p.fv0) * (1.0 - p.fv0) / (3.0 * p.fv0 * p.HD0)


def one_scale_check(p: TrackerParams) -> dict:
    t = np.geomspace(1e-7 * p.t0, p.t0, 4001)
    tau = tau_of(p)
    f = np.asarray(bg.fv(t, p))
    err = float(np.max(np.abs(f - t / (t + tau)) / f))
    if err > ONE_SCALE_RTOL:
        raise AssertionError(f"f_v = t/(t+tau) failed: {err}")
    return {"tau_over_t0": tau / p.t0, "max_rel_err": err}


def _background(t: float, p: TrackerParams) -> dict:
    f = float(bg.fv(t, p))
    return {"f": f, "fw": 1.0 - f, "Hv": 1.0 / t, "Hw": 2.0 / (3.0 * t), "Rv": -6.0 / t ** 2,
            "rho_d": float(bg.rho_d(t, p, G)), "rho_eff": float(bg.rho_eff(t, p, G)),
            "p_eff": float(bg.p_eff(t, p, G)), "Theta": float(bg.Theta(t, p)),
            "cs2": float(bg.cs2_eff(t, p)), "tau": tau_of(p)}


def su_mode(t: float, p: TrackerParams, mode: str) -> dict:
    """Separate-universe (k -> 0) perturbation of one two-region cell ([1G-D] Sec. 3).

    wall mode: delta_w = (t/t0)^(2/3) (EdS growing mode of the walls), voids untouched;
    eps mode:  tau -> tau(1+eps), eps = 1 (void-onset shift), walls untouched.
    Q = 6 f_v f_w (H_v - H_w)^2 ([W09] Q1), <R> = f_v R_v + f_w R_w,
    rho_eff = -(Q+<R>)/(16 pi G), p_eff = -Q/(16 pi G) + <R>/(48 pi G) ([GM] 3.12-3.13).
    """
    b = _background(t, p)
    f, fw, tau = b["f"], b["fw"], b["tau"]
    dHvHw = b["Hv"] - b["Hw"]
    if mode == "wall":
        dw = (t / p.t0) ** (2.0 / 3.0)
        dw1, dw2 = (2.0 / 3.0) * dw / t, -(2.0 / 9.0) * dw / t ** 2
        fw1, fw2 = -tau / (t + tau) ** 2, 2.0 * tau / (t + tau) ** 3
        dd, dd1, dd2 = fw * dw, fw1 * dw + fw * dw1, fw2 * dw + 2 * fw1 * dw1 + fw * dw2
        dfv = f * fw * dw
        dHw = -dw1 / 3.0
        dRw = 10.0 * b["Hw"] ** 2 * dw
    elif mode == "eps":
        dd, dd1, dd2 = f, tau / (t + tau) ** 2, -2.0 * tau / (t + tau) ** 3
        dfv = -f * fw
        dHw = 0.0
        dRw = 0.0
    else:
        raise ValueError(mode)
    dQ = 6.0 * (1.0 - 2.0 * f) * dHvHw ** 2 * dfv + 12.0 * f * fw * dHvHw * (-dHw)
    dR = b["Rv"] * dfv + fw * dRw
    drho_eff = -(dQ + dR) / (16.0 * math.pi * G)
    dp_eff = (-dQ + dR / 3.0) / (16.0 * math.pi * G)
    Z, Zdot = -dd1, -dd2
    terms = [Zdot, (2.0 / 3.0) * b["Theta"] * Z, 4 * math.pi * G * b["rho_d"] * dd,
             4 * math.pi * G * drho_eff, 12 * math.pi * G * dp_eff]
    return {"delta_d": dd, "Delta_eff_over_Delta_d": drho_eff / b["rho_eff"] / dd,
            "Ptilde_over_Delta_d": dp_eff / b["rho_eff"] / dd,
            "Ptilde_over_Delta_eff": dp_eff / drho_eff,
            "raychaudhuri_4_11_rel_residual": abs(sum(terms)) / max(abs(x) for x in terms),
            "cs2_eff_background": b["cs2"]}


def eps_mode_package_check(p: TrackerParams) -> dict:
    """eps mode = neighbouring tracker with tau(1+eps): compare with package functions."""
    tau_new = tau_of(p) * (1.0 + EPS_PROBE)
    fv0_new = brentq(lambda f: (2 + f) * (1 - f) / (3 * f * p.HD0) - tau_new, 1e-3, 1 - 1e-3,
                     xtol=1e-16, rtol=4 * np.finfo(float).eps, maxiter=500)
    q = TrackerParams(fv0=fv0_new, HD0=p.HD0)
    out = []
    for frac in (1e-3, 0.1, 0.5, 1.0):
        t = frac * p.t0
        lin = su_mode(t, p, "eps")
        pkg_rho = (float(bg.rho_d(t, q, G)) / float(bg.rho_d(t, p, G)) - 1.0) / EPS_PROBE
        pkg_eff = (float(bg.rho_eff(t, q, G)) / float(bg.rho_eff(t, p, G)) - 1.0) / EPS_PROBE
        pkg_p = (float(bg.p_eff(t, q, G)) - float(bg.p_eff(t, p, G))) / float(bg.rho_eff(t, p, G)) / EPS_PROBE
        rel = [abs(pkg_rho / lin["delta_d"] - 1),
               abs(pkg_eff / (lin["Delta_eff_over_Delta_d"] * lin["delta_d"]) - 1),
               abs(pkg_p / (lin["Ptilde_over_Delta_d"] * lin["delta_d"]) - 1)]
        if max(rel) > EPS_MODE_PACKAGE_RTOL:
            raise AssertionError(f"eps mode vs package at t/t0={frac}: {rel}")
        out.append({"t_over_t0": frac, "max_rel_diff": max(rel)})
    return {"probe_eps": EPS_PROBE, "rows": out}


def closure_comparison(p: TrackerParams) -> list:
    times = np.array([1e-3, 1e-2, 0.1, 0.3, 1.0]) * p.t0
    coeff = regular_growing_mode_coefficients(
        p, system=CleanPerturbationSystem.COMOVING, times=times,
        config=REGULAR_GROWING_MODE_REFERENCE_CONFIG, G=G)
    rows = []
    for i, t in enumerate(times):
        wall, eps = su_mode(float(t), p, "wall"), su_mode(float(t), p, "eps")
        for m in (wall, eps):
            if m["raychaudhuri_4_11_rel_residual"] > RAYCHAUDHURI_RTOL:
                raise AssertionError(f"(4.11) residual {m['raychaudhuri_4_11_rel_residual']}")
        rows.append({
            "t_over_t0": float(t / p.t0),
            "su_wall": {k: wall[k] for k in ("Delta_eff_over_Delta_d", "Ptilde_over_Delta_eff",
                                             "raychaudhuri_4_11_rel_residual")},
            "su_eps": {k: eps[k] for k in ("Delta_eff_over_Delta_d", "Ptilde_over_Delta_eff",
                                           "raychaudhuri_4_11_rel_residual")},
            "gm_comoving": {"Delta_eff_over_Delta_d": float(coeff.effective_ratio[i]),
                            "Ptilde": 0.0},
            "gm_meszaros": {"Delta_eff": 0.0},
            "gm_barotropic": {"Ptilde_over_Delta_eff_cs2": wall["cs2_eff_background"]},
        })
    return rows


def growth_histories(p: TrackerParams) -> dict:
    """Photon-normalised D_CGI(t), D_wall(t) and the CGI-implied void response r(t)."""
    t_e = EARLY_FRACTION * p.t0
    tg = np.geomspace(t_e, p.t0, GROWTH_GRID)
    a_ph = 1.0 / (1.0 + np.asarray(bg.redshift(tg, p)))
    fv = np.asarray(bg.fv(tg, p))
    d_wall = a_ph[0] * (tg / t_e) ** (2.0 / 3.0)
    out = {"D_wall_t0": float(d_wall[-1]), "f_w0_D_wall_t0": float((1 - fv[-1]) * d_wall[-1])}
    g_lcdm = float(qplus(0.0, PLANCK_2018_QPLUS_RECIPE))
    out["X_SU_min_beta0"] = out["f_w0_D_wall_t0"] / g_lcdm
    for system in CleanPerturbationSystem:
        c = regular_growing_mode_coefficients(
            p, system=system, times=tg, config=REGULAR_GROWING_MODE_REFERENCE_CONFIG, G=G)
        d_cgi = a_ph[0] * np.exp(cumulative_simpson(c.log_rate, x=np.log(tg), initial=0.0))
        r = (d_cgi - (1 - fv) * d_wall) / fv
        idx = np.searchsorted(tg, np.array([1e-3, 1e-2, 0.1, 0.3, 1.0]) * p.t0).clip(0, len(tg) - 1)
        out[system.value] = {
            "D_CGI_t0": float(d_cgi[-1]),
            "implied_void_response_r_t": {f"{tg[i] / p.t0:.3g}": float(r[i]) for i in idx},
            "r_t0_over_r_early": float(r[idx[-1]] / r[idx[0]]),
        }
    return out


def sigma_x(R_mpc, omega_m, growth, n):
    """sigma_R with x = kR quadrature (large R), 1G-A amplitude and EH98 transfer."""
    x = np.exp(np.linspace(math.log(SIGMA_X_BOUNDS[0]), math.log(SIGMA_X_BOUNDS[1]), n))
    k = x / R_mpc
    amp = (4 / 25) * g1a.PLANCK["A_s"] * (k / g1a.PLANCK["k_pivot_Mpc"]) ** (g1a.PLANCK["n_s"] - 1)
    d2 = amp * (k / (100.0 / g1a.C_KM_S)) ** 4 * g1a.eh98_nowiggle_transfer(
        k, omega_m, g1a.BARYON_FRACTION_PRIMARY) ** 2 * growth ** 2 / omega_m ** 2
    return math.sqrt(simpson(d2 * g1a.tophat(x) ** 2, x=np.log(x)))


def sigma_large_R(R_mpc, omega_m, growth):
    a, b = (sigma_x(R_mpc, omega_m, growth, n) for n in SIGMA_X_POINTS)
    if abs(a / b - 1) > SIGMA_X_RTOL:
        raise AssertionError(f"large-R sigma not converged at R={R_mpc}")
    return b


def transition_scales(case_density: dict) -> dict:
    """R_* where the linear void-onset response A_v sigma_LSS(R) reaches a criterion."""
    om = case_density["omega_m_per_photon"]
    h = case_density["H0_dressed_km_s_Mpc"] / 100.0
    f_v0 = case_density["fv0"]
    f_w0 = 1.0 - f_v0
    check = sigma_large_R(12.57, om, 1.0) / g1a.sigma_converged(
        12.57, om, g1a.BARYON_FRACTION_PRIMARY, g1a.PLANCK["n_s"], 1.0) - 1.0
    # Peak-background-split (Gaussian threshold) amplification at the void seed scale.
    R_seed = (W09_VOID_DIAMETER_H_MPC / 2.0) / SVDW_SHELL_CROSSING_RADIUS_FACTOR / h
    sigma_seed = sigma_large_R(R_seed, om, A_LS)
    pbs = {}
    for fvi in W09_FVI_RANGE:
        nu = float(-norm.ppf(fvi))
        pbs[f"f_vi={fvi:g}"] = {"nu": nu, "A_v": float(norm.pdf(nu) / (sigma_seed * norm.sf(nu)))}
    amps = {"W09_single_perturbation_|dH|=1e-5": 1e5, "W09_single_perturbation_|dH|=1e-6": 1e6}
    amps.update({f"PBS_{k}": v["A_v"] for k, v in pbs.items()})
    rows = {}
    for label, A in amps.items():
        entry = {"A_v": A}
        # eps = 1: void onset fully non-perturbative; |delta f_v/f_v| = f_w0 eps = 0.1:
        # 10% void-fraction fluctuation; delta = f_v0 eps = 0.1: 10% density contrast
        # from the void mode today ([W09] homogeneity criterion, line 455).
        for crit_label, target in (("eps=1", 1.0),
                                   ("void_fraction_10pct", 0.1 / f_w0),
                                   ("density_10pct", 0.1 / f_v0)):
            lo, hi = 5.0, 3.0e4
            if (A * sigma_large_R(hi, om, A_LS) - target) > 0.0:
                entry[crit_label] = {"R_Mpc": None, "R_h_inv_Mpc": None,
                                     "note": f"beyond {hi:g} Mpc search bracket"}
                continue
            R = brentq(lambda r: A * sigma_large_R(r, om, A_LS) - target, lo, hi, xtol=1e-6)
            entry[crit_label] = {"R_Mpc": R, "R_h_inv_Mpc": R * h}
        rows[label] = entry
    return {"large_R_vs_1G-A_quadrature_rel": check, "seed_radius_Mpc": R_seed,
            "sigma_seed_LSS": sigma_seed, "pbs": pbs, "R_star": rows,
            "sigma_LSS_R8": sigma_large_R(12.57, om, A_LS),
            "void_response_at_R8": {k: v["A_v"] * sigma_large_R(12.57, om, A_LS)
                                    for k, v in rows.items()}}


def super_cell_growth(p: TrackerParams, growth: dict, scales: dict) -> dict:
    """D_SU(t0) = f_w0 D_wall(t0) + A_v a_LS f_v0 for super-cell (R > R_*) modes ([1G-D] Sec. 6)."""
    g_lcdm = float(qplus(0.0, PLANCK_2018_QPLUS_RECIPE))
    base = growth["f_w0_D_wall_t0"]
    out = {"beta0": {"D_SU_t0": base, "X_SU": base / g_lcdm}}
    for label, v in scales["pbs"].items():
        d = base + v["A_v"] * A_LS * p.fv0
        out[f"PBS_{label}"] = {"A_v_a_LS": v["A_v"] * A_LS, "D_SU_t0": d, "X_SU": d / g_lcdm}
    return out


def main() -> int:
    cases = g1a._cases()
    density = {name: g1a.per_photon_matter_density(p) for name, p in cases.items()}
    results = {}
    for name, p in cases.items():
        growth = growth_histories(p)
        scales = transition_scales(density[name])
        results[name] = {
            "one_scale": one_scale_check(p),
            "eps_mode_vs_package": eps_mode_package_check(p),
            "closure_comparison": closure_comparison(p),
            "growth": growth,
            "transition_scales": scales,
            "super_cell_growth": super_cell_growth(p, growth, scales),
        }
    payload = {"phase": "1G-D",
               "status": "REPORT_ONLY_AUDIT_EVIDENCE; CONDITIONAL; NOT_OBSERVATIONAL; NOT_SIGMA8",
               "environment": {"python": sys.version.split()[0], "numpy": np.__version__,
                               "scipy": scipy.__version__, "platform": platform.platform()},
               "results": results}
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {ARTIFACT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
