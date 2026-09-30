"""Numerical evidence for the report-only Phase 1G-F void-population audit.

Report: reports/phase1g_f_void_population.md (sections cited as [1G-F]).
Writes artifacts/independent/phase1g_f_void_population.json (git-ignored).

Question ([1G-E] Sec. 6 item 1): replace the single void radius of the 1G-E
two-phase model by a void size distribution derived from the same early
spectrum (the 1G-A EH98 import, per-photon omega_m,eff, Planck A_s, n_s, f_b)
and test whether it reproduces the tracker's present void fraction f_v0 with
near-empty voids.

Ingredients, each cited to its source (printed equation numbers of the two
void papers were reconstructed from their arXiv LaTeX sources):
- [SvdW04] Sheth & van de Weygaert, MNRAS 350, 517 (astro-ph/0311260):
  two-barrier first-crossing distribution Eq. (1) with D of Eq. (2); void
  mass fraction 1 - D, Eq. (3) and (C8); Laplace transform (C7) of the
  single-barrier density (C1)-(C2); void volume v = 1.7^3 m/rho, Eq. (7);
  EdS tophat void, Eqs. (A26)-(A31); collapse/turnaround thresholds
  (A21)-(A22).
- [JLH13] Jennings, Li & Hu, MNRAS 434, 2167 (arXiv:1304.6087): the same
  first crossing in the form of Eq. (6)-(7); the volume-fraction overflow
  F(0) = (r_NL/r_L)^3 (1 - D), Eq. (14); the volume-conserving model,
  Eqs. (15)-(17); the corrected EdS shell-crossing numbers, Eqs. (A8)-(A12)
  (eta_sc = 3.488, 1 + Delta = 0.2047, r_NL/r_L = 1.697, delta_v = -2.717).
- Growth clocks (an explicit closure, [1G-F] Sec. 4): EdS in the common time
  t (the [1G-C] wall law), the [1G-A] volume-average CGI growth, and the
  [1G-D] separate-universe void-onset response.
- Boolean model of polydisperse balls (standard stochastic geometry, e.g.
  Chiu, Stoyan, Kendall & Mecke, Stochastic Geometry and its Applications,
  3rd ed., 2013, Sec. 3.1): P(both points uncovered) = exp(-int n(rho)
  [2V(rho) - gamma_rho(r)] drho); checked here by Monte Carlo.
- The [1G-E] variance decomposition and its sigma_int machinery (imported).

No package module, status token or tolerance changes.  All outputs are
conditional, nonlinear, model-internal numbers; none is an observational
sigma_8 (SIGMA8_AUTHORIZATION stays NOT_GRANTED).
"""

from __future__ import annotations

import importlib.util
import json
import math
import platform
import resource
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad, simpson
from scipy.optimize import brentq
from scipy.spatial import cKDTree
from scipy.stats import norm

import timescape_fsigma8.background as bg

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "independent" / "phase1g_f_void_population.json"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


g1a = _load("phase1g_a_numerics", "phase1g_a_sigma8_path_numerics.py")
g1d = _load("phase1g_d_numerics", "phase1g_d_separate_universe_numerics.py")
g1e = _load("phase1g_e_numerics", "phase1g_e_two_phase_sigma_numerics.py")

# ---------------------------------------------------------------- budgets
# Explicit tolerances (AGENTS.md rule 9).
ROOT_XTOL = 1e-15                   # brentq on the tophat development angle
PRINTED_JLH13 = {"eta_sc": (3.488, 1e-3), "one_plus_delta_sc": (0.2047, 1e-4),
                 "r_nl_over_r_l": (1.697, 1e-3), "delta_v": (-2.717, 1e-3)}   # value, last digit
PRINTED_SVDW04 = {"theta_sc": 3.53, "one_plus_delta_sc": 0.1982, "r_nl_over_r_l": 1.7151,
                  "delta_v": -2.81}                                            # reported, not gated
SERIES_TERMS = 60                   # images / Fourier terms in the production evaluation
SERIES_CHECK_TERMS = 400            # both series with many terms on the overlap region
SERIES_AGREEMENT_ATOL = 1e-13       # images vs Fourier (absolute, f_lnsigma <= 1)
NORMALISATION_ATOL = 1e-11          # int f dln sigma = 1 - D ([SvdW04] Eq. (3), (C8))
QUAD_EPSABS = 1e-14
SIGMA_X_BOUNDS = (1e-4, 200.0)      # x = kR range (as [1G-D])
SIGMA_X_POINTS = (20001, 40001)
SIGMA_TABLE_RTOL = 1e-8             # sigma and d ln sigma / d ln R grid convergence
RL_GRID = (1e-3, 300.0, 481)        # Lagrangian radius grid, photon-normalised Mpc (log)
FV_TRACKER_RTOL = 1e-13             # f_v(t) = t/(t+tau) inherited ([1G-D] Sec. 3)
PAIR_QUAD_RTOL = 1e-9               # composite Gauss-Legendre vs quad for sigma_part
MONODISPERSE_RTOL = 1e-13           # polydisperse formula with one radius vs [1G-E]
REPRO_1G_E_RTOL = 1e-6              # [1G-E] a = 15 sigma values reproduced
MC_SEED = 29092026
MC_POINTS = 1_000_000
MC_BALLS, MC_POINTS_PER_BALL = 8000, 1000
MC_BALL_JACKKNIFE_SIGMAS = 3.0      # ball variance: gate max(MC_REL_GATE, 3 jackknife errors)
MC_SEPARATIONS_OVER_MEDIAN = (0.25, 0.5, 1.0, 2.0)
MC_SEPARATIONS_OVER_R = (0.5, 1.0, 1.5)   # spans the pair density P_R(r) on [0, 2R]
MC_CLASS_RATIO = 1.25               # radius-class width of the exact coverage test
MC_QUERY_CHUNK = 500_000            # points per coverage query batch (memory bound only)
MC_BALL_CHUNK = 500                 # balls per point-generation batch (memory bound only)
MC_REL_GATE = 0.05                  # Monte Carlo vs analytic, same gate as [1G-E]
MC_GATED_MIN_XI = 0.2               # covariance gated only where the analytic xi_w >= 0.2
MC_TRUNCATED_VOLUME_MAX = 0.02      # smallest voids dropped from the MC: <= 2% of void volume
MC_BOX_OVER_R95 = 20.0              # box side / 95th-percentile void radius (periodic box)
MC_BOX_OVER_R = 20.0                # box side / ball radius R

# ---------------------------------------------------------------- inputs
R_H_MPC = 8.0                       # the "8" of 8 h^-1 Mpc (dressed h, 1G-A convention (b))
R_MIN_H_MPC = (1.0, 2.0, 5.0)       # minimum Eulerian void radii for clock-dependent fractions
DOMINANT_R_H_MPC = (10.0, 15.0)     # [W09] line 277: 30 h^-1 Mpc diameter voids fill 40-50%
W09_DOMINANT_FILL = (0.40, 0.50)
NEAR_EMPTY_INTERIOR = (0.1, 0.05)   # rho_v / rho_background of "near-empty" voids
HISTORY_REDSHIFTS = (0.0, 0.5, 1.0, 2.0, 3.0)
A_LS = g1d.A_LS


# =============================================================== A. tophat
def _open_density(eta: float) -> float:
    """1 + Delta of a tophat underdensity in EdS ([SvdW04] (A26); [JLH13] (A9))."""
    return 4.5 * (math.sinh(eta) - eta) ** 2 / (math.cosh(eta) - 1.0) ** 3


def _open_linear(eta: float) -> float:
    """Linearly extrapolated contrast ([JLH13] (A11); [SvdW04] (A27))."""
    return -(3.0 / 20.0) * (6.0 * (math.sinh(eta) - eta)) ** (2.0 / 3.0)


def _velocity_function(eta: float) -> float:
    """g(Theta) of [SvdW04] (A15): H_shell = H_u g(Theta_r)/g(Theta_u), g_EdS = 2/3."""
    return math.sinh(eta) * (math.sinh(eta) - eta) / (math.cosh(eta) - 1.0) ** 2


def spherical_model() -> dict:
    """EdS tophat void and collapse thresholds, re-derived from the parametric solution."""
    eta_sc = brentq(lambda e: _velocity_function(e) - 8.0 / 9.0, 1.0, 10.0, xtol=ROOT_XTOL)
    sc = {"eta_sc": eta_sc, "one_plus_delta_sc": _open_density(eta_sc),
          "delta_v": _open_linear(eta_sc)}
    sc["r_nl_over_r_l"] = sc["one_plus_delta_sc"] ** (-1.0 / 3.0)
    sc["shell_hubble_over_background"] = _velocity_function(eta_sc) / (2.0 / 3.0)
    for key, (value, digit) in PRINTED_JLH13.items():
        if abs(sc[key] - value) > 0.5 * digit:
            raise AssertionError(f"{key}: {sc[key]} does not round to [JLH13]'s {value}")
    svdw_residual = _velocity_function(PRINTED_SVDW04["theta_sc"]) - 8.0 / 9.0
    near_empty = {}
    for x in NEAR_EMPTY_INTERIOR:
        eta = brentq(lambda e: _open_density(e) - x, 0.1, 60.0, xtol=ROOT_XTOL)
        near_empty[f"{x:g}"] = {"interior_density_ratio": x, "eta": eta,
                                "delta_v": _open_linear(eta), "r_nl_over_r_l": x ** (-1.0 / 3.0),
                                "beyond_shell_crossing": eta > eta_sc}
    # The homogeneous interior is an open FLRW region: as eta -> infinity it
    # tends to an empty Milne region with H_v/H_background -> 3/2, the tracker's
    # H_v/H_w = (1/t)/(2/(3t)) ([1G-C] Sec. 3).
    milne = {f"eta={e:g}": _velocity_function(e) / (2.0 / 3.0) for e in (5.0, 10.0, 20.0, 40.0)}
    if abs(milne["eta=40"] - 1.5) > 1e-12:
        raise AssertionError("tophat interior does not approach the Milne rate 3/2")
    thresholds = {"turnaround": 0.6 * (3.0 * math.pi / 4.0) ** (2.0 / 3.0),     # (A21)
                  "collapse": 0.6 * (3.0 * math.pi / 2.0) ** (2.0 / 3.0)}       # (A22)
    return {"shell_crossing": sc, "svdw04_printed": PRINTED_SVDW04,
            "svdw04_theta_sc_residual_of_A29": svdw_residual,
            "near_empty": near_empty, "interior_hubble_ratio_limit": milne,
            "delta_c": thresholds}


# ====================================================== B. two-barrier walks
def f_lnsigma_images(sigma, dv_abs: float, dc: float, n_terms: int):
    """Void first crossing per ln sigma by images: inverse of [SvdW04] (C7) term by term.

    sinh(dc s)/sinh(w s) = sum_n [exp(-(|dv| + 2nw) s) - exp(-(|dv| + 2dc + 2nw) s)],
    w = dc + |dv|, s = sqrt(2t); each exponential is the Laplace transform (C2) of
    the single-barrier density (C1).  With f_lnsigma = 2 S F ([JLH13] below (7)).
    """
    s = np.atleast_1d(np.asarray(sigma, dtype=float))[None, :]
    w = dv_abs + dc
    n = np.arange(n_terms, dtype=float)[:, None]

    def g(b):
        return math.sqrt(2.0 / math.pi) * b / s * np.exp(-b * b / (2.0 * s * s))
    return (g(dv_abs + 2.0 * n * w) - g(dv_abs + 2.0 * dc + 2.0 * n * w)).sum(axis=0)


def f_lnsigma_fourier(sigma, dv_abs: float, dc: float, n_terms: int):
    """[JLH13] Eq. (6) = 2 x [SvdW04] Eq. (1): 2 sum_j exp(-(j pi x)^2/2) j pi x^2 sin(j pi D)."""
    d = dv_abs / (dc + dv_abs)
    x = d * np.atleast_1d(np.asarray(sigma, dtype=float))[None, :] / dv_abs
    j = np.arange(1, n_terms + 1, dtype=float)[:, None]
    return (2.0 * np.exp(-(j * math.pi * x) ** 2 / 2.0) * j * math.pi * x ** 2
            * np.sin(j * math.pi * d)).sum(axis=0)


def f_lnsigma(sigma, dv_abs: float, dc: float):
    """Images for sigma <= dc + |dv| (fast there), Fourier above (fast there)."""
    s = np.atleast_1d(np.asarray(sigma, dtype=float))
    w = dv_abs + dc
    return np.where(s <= w, f_lnsigma_images(s, dv_abs, dc, SERIES_TERMS),
                    f_lnsigma_fourier(s, dv_abs, dc, SERIES_TERMS))


def first_crossing_checks(barriers: dict, thresholds: dict) -> dict:
    out = {}
    for bkey, barrier in barriers.items():
        for ckey, dc in thresholds.items():
            a = abs(barrier["delta_v"])
            w = a + dc
            s = np.exp(np.linspace(math.log(0.2 * w), math.log(5.0 * w), 301))
            diff = float(np.max(np.abs(f_lnsigma_images(s, a, dc, SERIES_CHECK_TERMS)
                                       - f_lnsigma_fourier(s, a, dc, SERIES_CHECK_TERMS))))
            prod = float(np.max(np.abs(f_lnsigma(s, a, dc)
                                       - f_lnsigma_images(s, a, dc, SERIES_CHECK_TERMS))))
            total = quad(lambda ln_s: float(f_lnsigma(math.exp(ln_s), a, dc)[0]),
                         math.log(w / 40.0), math.log(40.0 * w),
                         epsabs=QUAD_EPSABS, epsrel=0.0, limit=500)[0]
            mass_fraction = dc / (dc + a)
            if max(diff, prod) > SERIES_AGREEMENT_ATOL:
                raise AssertionError(f"{bkey}/{ckey}: series disagree {diff} {prod}")
            if abs(total - mass_fraction) > NORMALISATION_ATOL:
                raise AssertionError(f"{bkey}/{ckey}: normalisation {total} vs {mass_fraction}")
            out[f"{bkey}/{ckey}"] = {"delta_v": barrier["delta_v"], "delta_c": dc,
                                     "D": a / (a + dc), "void_mass_fraction_1_minus_D": mass_fraction,
                                     "integral_f_dlnsigma": total,
                                     "images_vs_fourier_max_abs": diff,
                                     "production_vs_reference_max_abs": prod}
    return out


# ================================================== C. linear sigma(R) table
def _sigma_and_slope(R_mpc: float, omega_m: float, n_points: int):
    """sigma_1(R) (unit photon-normalised growth, EH98 as [1G-A]) and d ln sigma/d ln R.

    The slope uses the exact window derivative W'(x) = (3/x)(sin x/x - W(x)),
    not a finite difference.
    """
    x = np.exp(np.linspace(math.log(SIGMA_X_BOUNDS[0]), math.log(SIGMA_X_BOUNDS[1]), n_points))
    k = x / R_mpc
    amp = (4.0 / 25.0) * g1a.PLANCK["A_s"] * (k / g1a.PLANCK["k_pivot_Mpc"]) ** (g1a.PLANCK["n_s"] - 1.0)
    d2 = amp * (k / (100.0 / g1a.C_KM_S)) ** 4 * g1a.eh98_nowiggle_transfer(
        k, omega_m, g1a.BARYON_FRACTION_PRIMARY) ** 2 / omega_m ** 2
    w = g1a.tophat(x)
    small = x < 1e-3
    xs = np.where(small, 1.0, x)
    wp = np.where(small, -x / 5.0, (3.0 / xs) * (np.sin(xs) / xs - w))
    s2 = simpson(d2 * w * w, x=np.log(x))
    ds2 = simpson(d2 * 2.0 * w * wp * x, x=np.log(x))
    return math.sqrt(s2), 0.5 * ds2 / s2


def sigma_table(omega_m: float, anchor: float) -> dict:
    radii = np.exp(np.linspace(math.log(RL_GRID[0]), math.log(RL_GRID[1]), RL_GRID[2]))
    sig, slope, worst = [], [], 0.0
    for R in radii:
        (s_a, d_a), (s_b, d_b) = (_sigma_and_slope(R, omega_m, n) for n in SIGMA_X_POINTS)
        worst = max(worst, abs(s_a / s_b - 1.0), abs(d_a / d_b - 1.0))
        sig.append(s_b * anchor)
        slope.append(d_b)
    if worst > SIGMA_TABLE_RTOL:
        raise AssertionError(f"sigma table not converged: {worst}")
    return {"R_L_Mpc": radii, "sigma_1_anchored": np.array(sig),
            "dlnsigma_dlnR": np.array(slope), "grid_convergence": worst}


# =========================================================== D. growth clocks
def growth_clocks(p, dens: dict) -> dict:
    """D(t0) of each clock in photon-normalised units (D/a_photon -> 1 early).

    C1  wall EdS in common time t ([1G-C] Sec. 5): gamma_w0 (1 - f_v0)^(1/3).
    C2  volume-average CGI growth ([1G-A] Sec. 5): gamma_w0 g_TS (comoving; Meszaros).
    C3  separate-universe void onset ([1G-D] Sec. 6): f_w0 D_wall + A_v a_LS f_v0,
        with A_v = 0 (lower bound) or the peak-background-split values of [1G-D] Sec. 7.
    """
    f_v, g0 = dens["fv0"], dens["gamma_w0"]
    d_wall = g0 * (1.0 - f_v) ** (1.0 / 3.0)
    growth = g1a.growth_summary(p)
    clocks = {
        "C1_WALL_EDS_COMMON_TIME": {"D_t0": d_wall, "source": "[1G-C] Sec. 5"},
        "C2_VOLUME_AVERAGE_CGI_COMOVING": {
            "D_t0": g0 * growth["comoving"]["g_TS_vs_volume_average_EdS"], "source": "[1G-A] Sec. 5.2"},
        "C2_VOLUME_AVERAGE_CGI_MESZAROS": {
            "D_t0": g0 * growth["meszaros"]["g_TS_vs_volume_average_EdS"], "source": "[1G-A] Sec. 5.2"},
        "C3_SEPARATE_UNIVERSE_A_V_ZERO": {
            "D_t0": (1.0 - f_v) * d_wall, "source": "[1G-D] Sec. 6, A_v = 0 lower bound"},
    }
    scales = g1d.transition_scales(dens)
    for key, pbs in scales["pbs"].items():
        clocks[f"C3_SEPARATE_UNIVERSE_PBS_{key.upper().replace('=', '_')}"] = {
            "D_t0": (1.0 - f_v) * d_wall + pbs["A_v"] * A_LS * f_v, "A_v": pbs["A_v"],
            "source": "[1G-D] Secs. 6-7 (outside its R > R* validity domain here)"}
    # Sensitivity from the Phase 1G-D adversarial audit (GD-F1, GD-F2; owner
    # decision pending): the tracker's own f_v at last scattering as f_vi and a
    # tracker-consistent seed radius R_seed = R_void (f_vi/f_v0)^(1/3)/gamma_w0,
    # with the [1G-D] Sec. 7 peak-background-split formula unchanged.
    h = dens["H0_dressed_km_s_Mpc"] / 100.0
    t_ls = g1a.t_of_redshift(p, 1.0 / A_LS - 1.0)
    f_vi = float(bg.fv(t_ls, p))
    r_seed = (g1d.W09_VOID_DIAMETER_H_MPC / 2.0 / h) * (f_vi / f_v) ** (1.0 / 3.0) / g0
    sigma_seed = g1d.sigma_large_R(r_seed, dens["omega_m_per_photon"], A_LS)
    nu = float(-norm.ppf(f_vi))
    a_v = float(norm.pdf(nu) / (sigma_seed * norm.sf(nu)))
    clocks["C3_SEPARATE_UNIVERSE_PBS_TRACKER_SEED"] = {
        "D_t0": (1.0 - f_v) * d_wall + a_v * A_LS * f_v, "A_v": a_v, "f_vi_tracker_LS": f_vi,
        "R_seed_Mpc": r_seed, "sigma_seed_LS": sigma_seed, "nu": nu,
        "source": "[1G-D] Secs. 6-7 with the GD-F1/GD-F2 tracker-consistent seed (audit sensitivity)"}
    return {"clocks": clocks, "D_wall_t0": d_wall,
            "R_star_eps1_h_inv_Mpc": {k: v["eps=1"]["R_h_inv_Mpc"]
                                      for k, v in scales["R_star"].items() if k.startswith("PBS")}}


# ======================================================== E. void population
def void_population(table: dict, D: float, barrier: dict, dc: float, frame: float, h: float) -> dict:
    """Excursion-set void population for one clock, barrier and collapse threshold.

    Lagrangian: F_L(>R_L) = int_0^{sigma(R_L)} f_lnsigma dln sigma ([JLH13] (15)).
    Eulerian radius (photon-normalised comoving Mpc, the 1G-A convention (b)):
    r = frame * x^(-1/3) R_L, with x the void interior density ratio and
    frame = a_w,reg/a_photon (t0) = D_wall the wall-to-photon frame factor ([1G-F] Sec. 3).
    """
    a = abs(barrier["delta_v"])
    x = barrier["interior_density_ratio"]
    R_L = table["R_L_Mpc"]
    sig = D * table["sigma_1_anchored"]
    dF_dlnR = f_lnsigma(sig, a, dc) * np.abs(table["dlnsigma_dlnR"])
    lnR = np.log(R_L)
    # cumulative from the largest radius down (trapezoid on the fine log grid)
    seg = 0.5 * (dF_dlnR[1:] + dF_dlnR[:-1]) * np.diff(lnR)
    F_gt = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    mass_fraction = dc / (dc + a)
    # the part of the void mass below the grid (R_L < 1e-3 Mpc) from the exact total
    resolved = float(F_gt[0])
    r_h = frame * x ** (-1.0 / 3.0) * R_L * h

    def frac_gt(r_min_h: float) -> float:
        return float(np.interp(math.log(r_min_h), np.log(r_h), F_gt))

    def budget(M: float) -> float:       # two-scale volume budget, [1G-F] Sec. 5 (M3)
        return (M / x) / (1.0 - M + M / x)

    median = float(np.exp(np.interp(0.5 * mass_fraction, F_gt[::-1], np.log(r_h)[::-1])))

    def r_min_for(target: float):
        """Smallest-void radius at which the M3 budget of voids >= r equals target (None if never)."""
        m3 = np.array([budget(v) for v in F_gt])        # decreasing in r
        if not m3[0] >= target > m3[-1]:
            return None
        return float(np.exp(np.interp(target, m3[::-1], np.log(r_h)[::-1])))
    rows = {"all_sizes": mass_fraction}
    rows.update({f"r>={r:g}": frac_gt(r) for r in R_MIN_H_MPC + DOMINANT_R_H_MPC})
    return {
        "delta_v": barrier["delta_v"], "interior_density_ratio": x, "delta_c": dc,
        "void_mass_fraction_1_minus_D": mass_fraction,
        "resolved_mass_fraction_on_grid": resolved,
        "unresolved_below_grid": mass_fraction - resolved,
        "volume_weighted_median_radius_h_inv_Mpc": median,
        "lagrangian_fraction": rows,
        "M1_svdw_number_conserving": {k: v / x for k, v in rows.items()},
        "M2_jlh13_volume_conserving": dict(rows),
        "M3_two_scale_volume_budget": {k: budget(v) for k, v in rows.items()},
        "M3_r_min_h_inv_Mpc_reproducing": {"GM_f_v0=0.737": r_min_for(0.737),
                                           "NW15_f_v0=0.627": r_min_for(0.627)},
        # radius grid and volume-weighted density (for the Boolean model)
        "_r_h": r_h, "_dF_dlnr": dF_dlnR,
    }


# ===================================================== F. polydisperse Boolean
def _rho_weights(pop: dict, h: float):
    """Volume-weighted radius distribution p_i (sums to the resolved share of 1)."""
    r_mpc = pop["_r_h"] / h
    lnr = np.log(r_mpc)
    w = np.zeros_like(r_mpc)
    d = np.diff(lnr)
    w[1:] += 0.5 * d * pop["_dF_dlnr"][1:]
    w[:-1] += 0.5 * d * pop["_dF_dlnr"][:-1]
    return r_mpc, w / pop["void_mass_fraction_1_minus_D"]


def covariogram_average(r, rho, p):
    """E_V[gamma_rho(r)/V_rho] = sum_i p_i (1 - 3u/4 + u^3/16), u = r/rho_i < 2."""
    u = np.asarray(r, dtype=float)[:, None] / rho[None, :]
    return (np.where(u < 2.0, 1.0 - 0.75 * u + u ** 3 / 16.0, 0.0) * p[None, :]).sum(axis=1)


def xi_wall_poly(r, rho, p, f_cov: float):
    """Wall-indicator correlation of a polydisperse Boolean model at covered fraction f_cov."""
    return np.expm1(-math.log(1.0 - f_cov) * covariogram_average(r, rho, p))


class PairKernel:
    """The [1G-E] r- and k-quadratures for one ball radius R, built once.

    Nodes and weights are [1G-E]'s composite Gauss-Legendre in r and its log-k
    grid; J[k, r] = j0(k r) P_R(r) w_r is tabulated once so that
    K(k) = int P_R (1 + xi_w) j0(kr) dr = J @ (1 + xi_w(r)) is a product
    (numerically identical to g1e.kernel, which forms the same sum).
    """

    def __init__(self, R: float):
        self.R = R
        self.r, w = g1e._r_nodes(R)
        self.base = g1e.pair_density(self.r, R) * w
        self.x = np.exp(np.linspace(math.log(g1e.K_X_BOUNDS[0]), math.log(g1e.K_X_BOUNDS[1]),
                                    g1e.K_POINTS))
        self.k = self.x / R
        self.J = np.sinc(np.outer(self.k, self.r) / math.pi) * self.base[None, :]

    def sigma2_part(self, xi):
        return float((self.base * xi).sum())

    def sigma2_int(self, xi, omega_m, growth, compression, anchor):
        """[1G-E] sigma_int^2 = int dlnk Delta^2_E(k) K(k), Delta^2_E(k) = Delta^2_L(k s)."""
        kl = self.k * compression
        amp = (4 / 25) * g1a.PLANCK["A_s"] * (kl / g1a.PLANCK["k_pivot_Mpc"]) ** (g1a.PLANCK["n_s"] - 1)
        d2 = amp * (kl / (100.0 / g1a.C_KM_S)) ** 4 * g1a.eh98_nowiggle_transfer(
            kl, omega_m, g1a.BARYON_FRACTION_PRIMARY) ** 2 * growth ** 2 / omega_m ** 2
        K = self.J @ (1.0 + xi)
        return float(simpson(d2 * K, x=np.log(self.x))) * anchor ** 2


def sigma2_part_poly(R, rho, p, f_cov):
    r, w = g1e._r_nodes(R)
    return float((g1e.pair_density(r, R) * xi_wall_poly(r, rho, p, f_cov) * w).sum())


def total_sigma(s2p, s2i, f_cov, delta_v):
    """sigma^2 = delta_v^2 sigma_part^2 + [f_w (1 + delta_W)]^2 sigma_int^2 ([1G-F] Sec. 7).

    Mass conservation fixes the wall density: f_w (1 + delta_W) = 1 - f (1 + delta_v);
    for empty voids (E1) the factor is 1 and this is exactly [1G-E]'s formula.
    """
    wall = 1.0 - f_cov * (1.0 + delta_v)
    return math.sqrt(delta_v ** 2 * s2p + wall ** 2 * s2i)


def monodisperse_checks(kern: PairKernel, a, f_v, omega_m, d_wall, anchor) -> dict:
    """One-radius limit equals [1G-E] (formula and its a = 15 numbers)."""
    R = kern.R
    rho, p = np.array([a]), np.array([1.0])
    r = np.linspace(0.0, 2.2 * a, 997)
    rel = float(np.max(np.abs(xi_wall_poly(r, rho, p, f_v) - g1e.xi_wall_indicator(r, a, f_v))
                       / np.maximum(np.abs(g1e.xi_wall_indicator(r, a, f_v)), 1e-300)))
    if rel > MONODISPERSE_RTOL:
        raise AssertionError(f"monodisperse xi_w differs from [1G-E]: {rel}")
    s2p = sigma2_part_poly(R, rho, p, f_v)
    s2p_quad = g1e.sigma2_partition(R, a, f_v)
    if abs(s2p / s2p_quad - 1.0) > PAIR_QUAD_RTOL:
        raise AssertionError(f"Gauss-Legendre vs quad sigma_part: {s2p} {s2p_quad}")
    s2i = kern.sigma2_int(xi_wall_poly(kern.r, rho, p, f_v), omega_m, d_wall,
                          (1.0 - f_v) ** (1.0 / 3.0), anchor)
    s2i_1ge = g1e.sigma2_internal(R, a, f_v, omega_m, d_wall, (1.0 - f_v) ** (1.0 / 3.0)) * anchor ** 2
    if abs(s2i / s2i_1ge - 1.0) > REPRO_1G_E_RTOL:
        raise AssertionError("sigma_int differs from [1G-E]")
    # The same [1G-E] a = 15 case with the compression that matches its own
    # radius convention (R = 8/h in photon-normalised comoving Mpc): wall matter
    # there is compressed by a_w,reg/a_photon = D_wall, not f_w^(1/3) ([1G-F] Sec. 3).
    xi = xi_wall_poly(kern.r, rho, p, f_v)
    s2i_ph = kern.sigma2_int(xi, omega_m, d_wall, d_wall, anchor)
    s2i_un = kern.sigma2_int(xi, omega_m, d_wall, 1.0, anchor)
    return {"xi_w_max_rel_vs_1G-E": rel, "sigma_part": math.sqrt(s2p),
            "sigma_part_quad_rel": abs(s2p / s2p_quad - 1.0),
            "sigma_int_compressed_fw13": math.sqrt(s2i),
            "sigma_total_empty_voids": total_sigma(s2p, s2i, f_v, -1.0),
            "sigma_int_photon_frame_Dwall": math.sqrt(s2i_ph),
            "sigma_total_photon_frame_Dwall_empty_voids": total_sigma(s2p, s2i_ph, f_v, -1.0),
            "sigma_int_uncompressed": math.sqrt(s2i_un),
            "sigma_total_uncompressed_empty_voids": total_sigma(s2p, s2i_un, f_v, -1.0),
            "sigma_total_fw13_delta_v_-0.8_mass_conserving": total_sigma(s2p, s2i, f_v, -0.8),
            "sigma_total_fw13_delta_v_-0.8_as_1G-E": math.sqrt(0.64 * s2p + s2i)}


class CoverageTester:
    """Exact coverage test for polydisperse balls in a periodic box.

    x is covered iff min_i (|x - c_i|^2 - rho_i^2) < 0.  Radii are split into
    narrow classes (rho_hi/rho_lo <= MC_CLASS_RATIO); in each class the lifted
    centres (c_i, sqrt(rho_hi^2 - rho_i^2)) and the query (x, 0) have squared
    4D distance |x - c_i|^2 + rho_hi^2 - rho_i^2, so one nearest-neighbour
    query per class decides coverage exactly.  Classes are tested from the
    largest radius down and covered points leave the query set.
    """

    def __init__(self, centres, radii, L):
        self.L = L
        self.classes = []
        edges = [float(radii.max())]
        while edges[-1] > radii.min():
            edges.append(edges[-1] / MC_CLASS_RATIO)
        for hi, lo in zip(edges[:-1], edges[1:]):
            sel = (radii <= hi) & (radii > lo) if lo > radii.min() else (radii <= hi)
            if not np.any(sel):
                continue
            r_hi = float(radii[sel].max())
            lifted = np.column_stack([centres[sel], np.sqrt(np.maximum(r_hi ** 2 - radii[sel] ** 2, 0.0))])
            self.classes.append((r_hi, cKDTree(lifted, boxsize=[L, L, L, 4.0 * r_hi])))
            if lo <= radii.min():
                break

    def uncovered(self, points):
        out = np.empty(len(points), dtype=bool)
        for start in range(0, len(points), MC_QUERY_CHUNK):   # bounded memory
            q = np.mod(points[start:start + MC_QUERY_CHUNK], self.L)
            free = np.ones(len(q), dtype=bool)
            for r_hi, tree in self.classes:
                idx = np.flatnonzero(free)
                if idx.size == 0:
                    break
                d, _ = tree.query(np.column_stack([q[idx], np.zeros(idx.size)]), k=1)
                free[idx[d * d < r_hi ** 2]] = False
            out[start:start + MC_QUERY_CHUNK] = free
        return out


def monte_carlo_poly(rho_mpc, p, f_cov, R, seed_offset: int) -> dict:
    """Polydisperse Poisson balls in a periodic box versus the analytic Boolean formula.

    The smallest voids (<= MC_TRUNCATED_VOLUME_MAX of the void volume) are
    dropped to keep the ball count finite; the analytic comparison uses the
    realisation's own balls (radius sample and covered fraction), as [1G-E]
    does for its intensity.
    """
    rng = np.random.default_rng(MC_SEED + seed_offset)
    vol = 4.0 / 3.0 * math.pi * rho_mpc ** 3
    order = np.argsort(rho_mpc)
    cum = np.cumsum(p[order])
    keep_from = int(np.searchsorted(cum, MC_TRUNCATED_VOLUME_MAX * cum[-1]))
    keep = np.sort(order[keep_from:])
    rho_k, p_k = rho_mpc[keep], p[keep]
    truncated_share = 1.0 - float(p_k.sum() / p.sum())
    # Boolean intensity measure: n_i V_i = -ln(1 - f) p_i, so the kept voids
    # have total number density -ln(1 - f) sum_kept p_i / V_i.
    number_weight = p_k / vol[keep]
    lam = -math.log(1.0 - f_cov) * float(number_weight.sum())
    number_pdf = number_weight / number_weight.sum()
    r95 = float(np.interp(0.95, np.cumsum(p_k) / p_k.sum(), rho_k))
    L = max(MC_BOX_OVER_R95 * r95, MC_BOX_OVER_R * R)
    n_balls = int(rng.poisson(lam * L ** 3))
    radii = rng.choice(rho_k, size=n_balls, p=number_pdf)
    centres = rng.uniform(0.0, L, size=(n_balls, 3))
    tester = CoverageTester(centres, radii, L)
    f_real = 1.0 - math.exp(-float((4.0 / 3.0 * math.pi * radii ** 3).sum()) / L ** 3)
    p_real = np.bincount(np.searchsorted(rho_k, radii), weights=4.0 / 3.0 * math.pi * radii ** 3,
                         minlength=len(rho_k))
    p_real = p_real / p_real.sum()

    x = rng.uniform(0.0, L, size=(MC_POINTS, 3))
    wx = tester.uncovered(x)
    f_w_mc = float(wx.mean())
    cov = {}
    median = float(np.interp(0.5, np.cumsum(p_real), rho_k))
    separations = {f"r={u}*median": u * median for u in MC_SEPARATIONS_OVER_MEDIAN}
    separations.update({f"r={u}*R": u * R for u in MC_SEPARATIONS_OVER_R})
    for key, sep in separations.items():
        n = rng.normal(size=(MC_POINTS, 3))
        y = x + sep * n / np.linalg.norm(n, axis=1)[:, None]
        both = float((wx & tester.uncovered(y)).mean())
        cov[key] = {"separation_Mpc": sep, "mc": both / f_w_mc ** 2 - 1.0,
                    "analytic": float(xi_wall_poly([sep], rho_k, p_real, f_real)[0])}
    centres_b = rng.uniform(0.0, L, size=(MC_BALLS, 3))
    wfrac = np.empty(MC_BALLS)
    for start in range(0, MC_BALLS, MC_BALL_CHUNK):          # bounded memory
        stop = min(start + MC_BALL_CHUNK, MC_BALLS)
        v = rng.normal(size=(stop - start, MC_POINTS_PER_BALL, 3))
        v /= np.linalg.norm(v, axis=2)[:, :, None]
        rad = R * rng.uniform(size=(stop - start, MC_POINTS_PER_BALL, 1)) ** (1.0 / 3.0)
        pts = (centres_b[start:stop, None, :] + rad * v).reshape(-1, 3)
        wfrac[start:stop] = tester.uncovered(pts).reshape(stop - start, MC_POINTS_PER_BALL).mean(axis=1)

    def ball_variance(sel):
        w = wfrac[sel]
        return (float(w.var(ddof=1)) - float(np.mean(w * (1 - w)) / (MC_POINTS_PER_BALL - 1))) / f_w_mc ** 2

    s2_mc = ball_variance(np.ones(MC_BALLS, dtype=bool))
    s2_an = sigma2_part_poly(R, rho_k, p_real, f_real)
    # The ball estimator averages over only about (L/2R)^3 independent volumes
    # of one realisation; its own error is estimated by a leave-one-octant-out
    # jackknife over the ball centres.
    octant = (np.floor(2.0 * centres_b / L).astype(int) * np.array([4, 2, 1])).sum(axis=1)
    loo = np.array([ball_variance(octant != o) for o in range(8)])
    s2_jk = float(math.sqrt(7.0 / 8.0 * ((loo - loo.mean()) ** 2).sum()))
    ball_err = abs(s2_mc / s2_an - 1.0)
    ball_budget = max(MC_REL_GATE, MC_BALL_JACKKNIFE_SIGMAS * s2_jk / s2_an)
    # Expected relative realisation fluctuation of the uncovered fraction of
    # one box: Var(f_w,box)/f_w^2 = int xi_w d^3r / L^3 (Boolean model).
    r_grid = np.linspace(0.0, 2.0 * float(rho_k.max()), 4001)
    xi_int = 4.0 * math.pi * float(simpson(xi_wall_poly(r_grid, rho_k, p_real, f_real) * r_grid ** 2, x=r_grid))
    fw_expected_rel = math.sqrt(xi_int / L ** 3)
    errs = [abs(f_w_mc / (1.0 - f_real) - 1.0)]
    errs += [abs(c["mc"] / c["analytic"] - 1.0) for c in cov.values() if c["analytic"] >= MC_GATED_MIN_XI]
    out = {"box_side_Mpc": L, "n_balls": n_balls, "n_radius_classes": len(tester.classes),
           "truncated_void_volume_share": truncated_share,
           "radius_range_Mpc": [float(radii.min()), float(radii.max())],
           "volume_weighted_median_radius_Mpc": median,
           "f_cov_nominal": f_cov, "f_cov_realisation": f_real, "f_w_mc": f_w_mc,
           "covariance": cov, "sigma2_part_mc": s2_mc, "sigma2_part_analytic_realisation": s2_an,
           "sigma2_part_mc_jackknife_error": s2_jk, "sigma2_part_rel_err": ball_err,
           "sigma2_part_budget": ball_budget,
           "independent_R_volumes_in_box": (L / (2.0 * R)) ** 3,
           "f_w_expected_realisation_rel_fluctuation": fw_expected_rel,
           "f_w_rel_err": abs(f_w_mc / (1.0 - f_real) - 1.0),
           "max_rel_err_gated": float(max(errs)),
           "ungated_small_xi": {k: abs(c["mc"] / c["analytic"] - 1.0) for k, c in cov.items()
                                if c["analytic"] < MC_GATED_MIN_XI}}
    if truncated_share > MC_TRUNCATED_VOLUME_MAX + 1e-12:
        raise AssertionError("Monte Carlo truncation exceeds its budget")
    if out["max_rel_err_gated"] > MC_REL_GATE:
        raise AssertionError(f"Monte Carlo disagrees with the polydisperse formula: {out['max_rel_err_gated']}")
    if ball_err > ball_budget:
        raise AssertionError(f"Monte Carlo ball variance off by {ball_err} (budget {ball_budget})")
    return out


# ================================================================ G. history
def history(p, table, dens, barrier, dc, h) -> list:
    """C1 clock at earlier times vs the tracker f_v(t) = t/(t+tau) ([1G-D] Sec. 3)."""
    tau = g1d.tau_of(p)
    rows = []
    for z in HISTORY_REDSHIFTS:
        t = g1a.t_of_redshift(p, z) if z > 0 else p.t0
        f_v = float(bg.fv(t, p))
        if abs(f_v / (t / (t + tau)) - 1.0) > FV_TRACKER_RTOL:
            raise AssertionError("one-scale identity failed in the history check")
        frame = float(bg.gamma_w(t, p)) * (1.0 - f_v) ** (1.0 / 3.0)   # a_w,reg/a_photon
        D = frame / (1.0 + z)                                           # EdS growth in t
        pop = void_population(table, D, barrier, dc, frame, h)
        rows.append({"z": z, "t_over_t0": t / p.t0, "tracker_f_v": f_v, "D_wall": D,
                     "M3_all_sizes": pop["M3_two_scale_volume_budget"]["all_sizes"],
                     "M3_r>=1": pop["M3_two_scale_volume_budget"]["r>=1"],
                     "M3_r>=5": pop["M3_two_scale_volume_budget"]["r>=5"],
                     "median_radius_h_inv_Mpc": pop["volume_weighted_median_radius_h_inv_Mpc"]})
    return rows


# ==================================================================== main
def _clean(obj):
    if isinstance(obj, dict):
        return {k: _clean(v) for k, v in obj.items() if not k.startswith("_")}
    if isinstance(obj, (list, tuple)):
        return [_clean(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    return obj


def _progress(message: str) -> None:
    """Progress line on stderr (not part of the artifact): elapsed time and peak RSS."""
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    print(f"[{time.monotonic() - _T0:7.1f} s, peak {rss:7.1f} MB] {message}", file=sys.stderr, flush=True)


_T0 = time.monotonic()


def main() -> int:
    sph = spherical_model()
    barriers = {"shell_crossing": {"delta_v": sph["shell_crossing"]["delta_v"],
                                   "interior_density_ratio": sph["shell_crossing"]["one_plus_delta_sc"]}}
    for key, row in sph["near_empty"].items():
        barriers[f"near_empty_{key}"] = {"delta_v": row["delta_v"],
                                         "interior_density_ratio": row["interior_density_ratio"]}
    thresholds = sph["delta_c"]
    crossing = first_crossing_checks(barriers, thresholds)

    cases = g1a._cases()
    om_L, h_L = g1a.PLANCK["omega_m_total_Om_h2"], g1a.PLANCK["h"]
    sig_L = g1a.sigma_converged(R_H_MPC / h_L, om_L, g1a.BARYON_FRACTION_PRIMARY, g1a.PLANCK["n_s"],
                                float(g1a.qplus(0.0, g1a.PLANCK_2018_QPLUS_RECIPE)))
    anchor = g1a.PLANCK["sigma8_linear"] / sig_L       # EH98 -> Planck anchor ([1G-A] Sec. 6.3)
    results = {"spherical_model": sph, "first_crossing": crossing, "eh98_anchor_factor": anchor,
               "cases": {}}
    for name in ("PAPER_REFERENCE", "NW15_CMB_FIT"):
        p = cases[name]
        dens = g1a.per_photon_matter_density(p)
        f_v0, h, om = dens["fv0"], dens["H0_dressed_km_s_Mpc"] / 100.0, dens["omega_m_per_photon"]
        clk = growth_clocks(p, dens)
        d_wall = clk["D_wall_t0"]
        table = sigma_table(om, anchor)
        R = R_H_MPC / h
        kern = PairKernel(R)
        case = {"f_v0": f_v0, "h_dressed": h, "R_Mpc": R, "D_wall_t0": d_wall,
                "frame_factor_wall_to_photon_t0": d_wall,
                "compression_photon_frame": d_wall,
                "compression_1G-E_fw13": (1.0 - f_v0) ** (1.0 / 3.0),
                "clocks": clk["clocks"], "R_star_eps1_h_inv_Mpc": clk["R_star_eps1_h_inv_Mpc"],
                "sigma_table_grid_convergence": table["grid_convergence"],
                "monodisperse_a15_vs_1G-E": monodisperse_checks(kern, 15.0 / h, f_v0, om, d_wall, anchor),
                "populations": {}, "variance": {}, "monte_carlo": {}}
        pops = {}
        for ckey, clock in clk["clocks"].items():
            for bkey, barrier in barriers.items():
                for tkey, dc in thresholds.items():
                    pop = void_population(table, clock["D_t0"], barrier, dc, d_wall, h)
                    pops[(ckey, bkey, tkey)] = pop
                    case["populations"][f"{ckey}/{bkey}/{tkey}"] = pop
        # Variance at 8 h^-1 Mpc: collapse threshold (primary) for every clock and barrier.
        for (ckey, bkey, tkey), pop in pops.items():
            if tkey != "collapse" or ckey == "C3_SEPARATE_UNIVERSE_A_V_ZERO":
                continue
            rho, pw = _rho_weights(pop, h)
            x = pop["interior_density_ratio"]
            norms = {"tracker_f_v0": f_v0,
                     "M3_predicted_all_sizes": pop["M3_two_scale_volume_budget"]["all_sizes"],
                     "M2_predicted_all_sizes": pop["M2_jlh13_volume_conserving"]["all_sizes"]}
            row = {}
            for nkey, f_cov in norms.items():
                xi = xi_wall_poly(kern.r, rho, pw, f_cov)
                s2p = kern.sigma2_part(xi)
                entry = {"f_cov": f_cov, "sigma_part": math.sqrt(s2p)}
                dv_barrier = x / (1.0 - f_cov + x * f_cov) - 1.0
                for comp_key, comp in (("photon_frame_Dwall", d_wall),
                                       ("1G-E_fw13", (1.0 - f_cov) ** (1.0 / 3.0)),
                                       ("uncompressed", 1.0)):
                    s2i = kern.sigma2_int(xi, om, d_wall, comp, anchor)
                    entry[f"sigma_int_{comp_key}"] = math.sqrt(s2i)
                    entry[f"sigma_total_{comp_key}_empty_voids"] = total_sigma(s2p, s2i, f_cov, -1.0)
                    entry[f"sigma_total_{comp_key}_barrier_interior"] = total_sigma(s2p, s2i, f_cov, dv_barrier)
                entry["delta_v_barrier_interior"] = dv_barrier
                row[nkey] = entry
            case["variance"][f"{ckey}/{bkey}/{tkey}"] = row
        _progress(f"{name}: populations and variance done")
        # Monte Carlo of the polydisperse Boolean covariance (tracker normalisation).
        for i, ckey in enumerate(("C1_WALL_EDS_COMMON_TIME",
                                  "C3_SEPARATE_UNIVERSE_PBS_F_VI_0.01")):
            rho, pw = _rho_weights(pops[(ckey, "shell_crossing", "collapse")], h)
            case["monte_carlo"][f"{ckey}/shell_crossing/collapse"] = monte_carlo_poly(
                rho, pw, f_v0, R, seed_offset=10 * i + (0 if name == "PAPER_REFERENCE" else 1))
            _progress(f"{name}: Monte Carlo {ckey} done")
        case["history_C1"] = {
            f"{bkey}/{tkey}": history(p, table, dens, barriers[bkey], thresholds[tkey], h)
            for bkey in ("shell_crossing", "near_empty_0.1") for tkey in thresholds}
        results["cases"][name] = case

    payload = {"phase": "1G-F",
               "status": ("REPORT_ONLY_AUDIT_EVIDENCE; CONDITIONAL; NONLINEAR_MODEL_INTERNAL; "
                          "NOT_OBSERVATIONAL; NOT_SIGMA8"),
               "environment": {"python": sys.version.split()[0], "numpy": np.__version__,
                               "scipy": scipy.__version__, "platform": platform.platform()},
               "budgets": {"ROOT_XTOL": ROOT_XTOL, "SERIES_TERMS": SERIES_TERMS,
                           "SERIES_AGREEMENT_ATOL": SERIES_AGREEMENT_ATOL,
                           "NORMALISATION_ATOL": NORMALISATION_ATOL,
                           "SIGMA_TABLE_RTOL": SIGMA_TABLE_RTOL, "PAIR_QUAD_RTOL": PAIR_QUAD_RTOL,
                           "MONODISPERSE_RTOL": MONODISPERSE_RTOL, "REPRO_1G_E_RTOL": REPRO_1G_E_RTOL,
                           "MC_REL_GATE": MC_REL_GATE, "MC_GATED_MIN_XI": MC_GATED_MIN_XI,
                           "MC_TRUNCATED_VOLUME_MAX": MC_TRUNCATED_VOLUME_MAX, "MC_SEED": MC_SEED,
                           "MC_POINTS": MC_POINTS, "MC_BALLS": MC_BALLS,
                           "MC_POINTS_PER_BALL": MC_POINTS_PER_BALL,
                           "MC_BALL_JACKKNIFE_SIGMAS": MC_BALL_JACKKNIFE_SIGMAS,
                           "MC_CLASS_RATIO": MC_CLASS_RATIO},
               "results": _clean(results)}
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
                        encoding="utf-8")
    print(f"wrote {ARTIFACT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
