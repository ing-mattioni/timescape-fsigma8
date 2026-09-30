"""Numerical evidence for the Phase 1G owner decisions of 2026-09-30.

Records (sections cited as [OD-A], [OD-D], [OD-E]):
reports/phase1g_a_owner_decisions_successor.md,
reports/phase1g_d_owner_decisions_successor.md,
reports/phase1g_e_owner_decisions_successor.md.
Writes artifacts/independent/phase1g_owner_decisions.json (git-ignored).

Scope.  This script recomputes only what the ticked owner decisions change.
Every equation, initial condition, unit, normalisation and tolerance of the
frozen phase scripts is reused unchanged: they are imported by path and never
edited.  The new ingredients are input choices that the decisions name:

- GA-OD2 (i): the [NW15] row with [NW15]'s own early-universe inputs
  (f_b = Omega_B0/Omega_M0 = 0.039/0.215, n_s = 0.992, as read by the 1G-A
  adversarial audit, Sec. 4.6) as a sensitivity; Planck's A_s is kept because
  [NW15] fit none.  The Planck early universe stays the declared primary.
- GA-OD3: the WKB exponent alpha*k at kR = 1 under the 1G-A Sec. 6.4 radius
  conventions (a)-(c), next to the hybrid chain of the frozen report.
- GA-OD4 (GA-F8): the (5.1) regional reading of convention (b),
  R = (8/h)/[gamma_w0 (1 - f_v0)^(1/3)].
- GD-OD1, OD2, OD6, OD7: the 1G-D peak-background-split void response with the
  tracker-consistent seed R_seed = R_void (f_vi/f_v0)^(1/3)/gamma_w0
  (primary) and [SvdW04]'s factor 1.72 (alternative), f_vi = f_v(t_LS) of
  the tracker, delta_L = the total contrast of the region at last
  scattering, and each parameter set's own equal-mass radius.
- GE-OD1 to OD5: the two-phase variance with the mass-conserving wall weight
  sigma^2 = delta_v^2 sigma_part^2 + (f_w - f_v delta_v)^2 sigma_int^2
  (1G-E adversarial audit, GE-F1), the photon-frame compression s = D_wall as
  the primary E4 frame (lead observation L1), the equal-mass radius beside
  convention (b), the 1G-F derived population as the reference, and the
  Monte Carlo precision as a scatter across seeds.

References: [GM] arXiv:2511.17160v2; [W09] arXiv:0909.0749v2; [NW15]
arXiv:1410.3470; [SvdW04] astro-ph/0311260; [EH98] astro-ph/9709112.
Outputs are conditional, model-internal numbers.  None is an observational
sigma_8, and SIGMA8_AUTHORIZATION stays NOT_GRANTED.
"""

from __future__ import annotations

import importlib.util
import json
import math
import platform
import statistics
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import norm

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations.initial_conditions import PLANCK_2018_QPLUS_RECIPE, qplus
from timescape_fsigma8.presets import PAPER_REFERENCE

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
ARTIFACT = ROOT / "artifacts" / "independent" / "phase1g_owner_decisions.json"

# The frozen 1G-F script imports the Unix-only ``resource`` module; the
# Windows stand-in (owner approval 2026-09-30) is a no-op where it exists.
sys.path.insert(0, str(SCRIPTS))
import _portable_resource  # noqa: E402

RESOURCE_MODULE = _portable_resource.install()


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


g1a = _load("phase1g_a_numerics", "phase1g_a_sigma8_path_numerics.py")
g1d = _load("phase1g_d_numerics", "phase1g_d_separate_universe_numerics.py")
g1e = _load("phase1g_e_numerics", "phase1g_e_two_phase_sigma_numerics.py")
g1f = _load("phase1g_f_numerics", "phase1g_f_void_population_numerics.py")

# ------------------------------------------------------------------ budgets
# Explicit tolerances (AGENTS.md rule 9).
FROZEN_REPRO_RTOL = 1e-12        # generalised functions vs the frozen functions, same inputs
PRINTED_HALF_UNIT_SLACK = 1e-12  # float slack added to half a unit of a printed last digit
MC_REL_GATE = g1e.MC_REL_GATE    # the frozen [1G-E] gate (5%), evaluated per seed, never changed
MC_GATED_MIN_XI = g1e.MC_GATED_MIN_XI

# ------------------------------------------------------------------ inputs
# [NW15] cmb1.tex table (ll. 1526-1568) as read by the 1G-A adversarial audit
# (Sec. 4.6; GA-F2): bare Omega_B0 = 0.039, Omega_M0 = 0.215; n_s = 0.992.
NW15_BARE_OMEGA_B0, NW15_BARE_OMEGA_M0 = 0.039, 0.215
NW15_BARYON_FRACTION = NW15_BARE_OMEGA_B0 / NW15_BARE_OMEGA_M0
NW15_N_S = 0.992
R_VOID_H_MPC = g1d.W09_VOID_DIAMETER_H_MPC / 2.0   # [W09] l. 277: 30 h^-1 Mpc diameter
Z_LAST_SCATTERING = 1.0 / g1d.A_LS - 1.0            # 1090, as [1G-D] and [1G-F]
AUDIT_FVI = g1d.W09_FVI_RANGE                      # the 1G-D audit's rows (1e-4, 1e-2)
VOID_RADII_H_MPC = g1e.VOID_RADII_H_MPC            # [1G-E] a = 5 ... 30 h^-1 Mpc
DELTA_V_VALUES = g1e.VOID_INTERIOR_CONTRASTS       # -1, -0.9, -0.8
MC_SEEDS = (g1e.MC_SEED,) + tuple(range(1, 16))    # the 1G-E audit's 16 seeds (GE-F5)
PRIMARY_CASES = ("PAPER_REFERENCE", "NW15_CMB_FIT")

GATES: list[dict] = []


def _gate_abs(name: str, value: float, expected: float, tol: float) -> None:
    ok = abs(value - expected) <= tol
    GATES.append({"name": name, "value": value, "expected": expected, "abs_tol": tol, "pass": ok})
    if not ok:
        raise AssertionError(f"{name}: {value!r} vs {expected!r} (abs tol {tol})")


def _gate_printed(name: str, value: float, printed: float, decimals: int) -> None:
    """``value`` rounds to the printed number: |value - printed| <= half a unit."""
    _gate_abs(name, value, printed, 0.5 * 10.0 ** (-decimals) + PRINTED_HALF_UNIT_SLACK)


def _gate_rel(name: str, value: float, expected: float, rtol: float) -> None:
    ok = abs(value / expected - 1.0) <= rtol
    GATES.append({"name": name, "value": value, "expected": expected, "rtol": rtol, "pass": ok})
    if not ok:
        raise AssertionError(f"{name}: {value!r} vs {expected!r} (rtol {rtol})")


def _planck_reference():
    om_L, h_L = g1a.PLANCK["omega_m_total_Om_h2"], g1a.PLANCK["h"]
    g_L = float(qplus(0.0, PLANCK_2018_QPLUS_RECIPE))
    R_L = g1a.R8_H_MPC / h_L
    sig_L = g1a.sigma_converged(R_L, om_L, g1a.BARYON_FRACTION_PRIMARY, g1a.PLANCK["n_s"], g_L)
    return {"omega_m": om_L, "h": h_L, "g_lcdm": g_L, "R_Mpc": R_L, "sigma_eh98": sig_L,
            "anchor_factor": g1a.PLANCK["sigma8_linear"] / sig_L}


def _radii(dens: dict, ref: dict) -> dict:
    """[1G-A] Sec. 6.4 conventions, photon-normalised comoving Mpc (as the frozen script)."""
    h_d, h_b = dens["H0_dressed_km_s_Mpc"] / 100.0, dens["HD0_bare_km_s_Mpc"] / 100.0
    return {"a_equal_mass": ref["R_Mpc"] * (ref["omega_m"] / dens["omega_m_per_photon"]) ** (1 / 3),
            "b_dressed_8_over_h": g1a.R8_H_MPC / h_d,
            "c_bare_8_over_hbar": (g1a.R8_H_MPC / h_b) / dens["gamma_w0"]}


# ============================================================ A. Phase 1G-A
def ga_od2_nw15_own_inputs(ref: dict) -> dict:
    """[NW15] row: Planck hybrid primary vs [NW15]'s own f_b and n_s (sensitivity)."""
    p = g1a._cases()["NW15_CMB_FIT"]
    dens = g1a.per_photon_matter_density(p)
    growth = g1a.growth_summary(p)
    om, g0, fv0 = dens["omega_m_per_photon"], dens["gamma_w0"], dens["fv0"]
    laws = {"cgi_comoving": g0 * growth["comoving"]["g_TS_vs_volume_average_EdS"],
            "cgi_meszaros": g0 * growth["meszaros"]["g_TS_vs_volume_average_EdS"],
            "wall_regional": g0 * (1.0 - fv0) ** (1.0 / 3.0)}
    inputs = {"planck_hybrid_primary": (g1a.BARYON_FRACTION_PRIMARY, g1a.PLANCK["n_s"]),
              "nw15_baryon_fraction": (NW15_BARYON_FRACTION, g1a.PLANCK["n_s"]),
              "nw15_baryon_fraction_and_n_s": (NW15_BARYON_FRACTION, NW15_N_S)}
    radii = _radii(dens, ref)
    out = {"baryon_fraction_nw15": NW15_BARYON_FRACTION, "n_s_nw15": NW15_N_S,
           "A_s": "Planck 2018 (unchanged; [NW15] leave A_s unconstrained)",
           "radii_Mpc": radii, "anchored": {}}
    for key, (f_b, n_s) in inputs.items():
        out["anchored"][key] = {
            law: {conv: g1a.sigma_converged(R, om, f_b, n_s, growth_today) / ref["sigma_eh98"]
                  * g1a.PLANCK["sigma8_linear"] for conv, R in radii.items()}
            for law, growth_today in laws.items()}
    a = out["anchored"]
    # Frozen [1G-A] values (the Planck hybrid) and the 1G-A audit's EH98 values.
    _gate_printed("GA-OD2 frozen NW15 comoving (a)", a["planck_hybrid_primary"]["cgi_comoving"]["a_equal_mass"], 0.6687, 4)
    _gate_printed("GA-OD2 frozen NW15 wall (a)", a["planck_hybrid_primary"]["wall_regional"]["a_equal_mass"], 0.9347, 4)
    _gate_printed("GA-OD2 audit NW15 f_b comoving (a)", a["nw15_baryon_fraction"]["cgi_comoving"]["a_equal_mass"], 0.637, 3)
    _gate_printed("GA-OD2 audit NW15 f_b+n_s comoving (a)", a["nw15_baryon_fraction_and_n_s"]["cgi_comoving"]["a_equal_mass"], 0.643, 3)
    _gate_printed("GA-OD2 audit NW15 f_b wall (a)", a["nw15_baryon_fraction"]["wall_regional"]["a_equal_mass"], 0.890, 3)
    _gate_printed("GA-OD2 audit NW15 f_b+n_s wall (a)", a["nw15_baryon_fraction_and_n_s"]["wall_regional"]["a_equal_mass"], 0.899, 3)
    return out


def ga_od3_exponent_chains(ref: dict) -> dict:
    """alpha*k at kR = 1 for the hybrid chain and the photon-normalised conventions."""
    p = TrackerParams.from_dressed_H0(fv0=PAPER_REFERENCE.fv0, H0=1.0)
    t_i = g1a.t_of_redshift(p, 20.0)
    alpha, alpha_err = quad(
        lambda t: math.sqrt(-float(bg.cs2_eff(t, p))) / float(bg.a_D(t, p)),
        t_i, p.t0, epsabs=0.0, epsrel=1e-12, limit=400)          # as the frozen script
    dens = g1a.per_photon_matter_density(PAPER_REFERENCE.tracker_params_gyr)
    h = PAPER_REFERENCE.H0_dressed_km_s_Mpc / 100.0
    hubble_length = g1a.C_KM_S / (100.0 * h)                        # c/H0 (dressed), Mpc
    radii = _radii(dens, ref)
    log_max = math.log(np.finfo(float).max)
    chains = {"1G-A_hybrid_aD0_k_phys0_D_R_8_over_h": p.aD0 * hubble_length / (g1a.R8_H_MPC / h)}
    chains.update({f"photon_normalised_{conv}": hubble_length / R for conv, R in radii.items()})
    out = {"alpha": alpha, "alpha_quad_abserr": alpha_err, "aD0_dressed_H0_1": p.aD0,
           "float64_log_max": log_max, "radii_Mpc": radii, "chains": {}}
    for label, k in chains.items():
        out["chains"][label] = {"k_code_at_kR_1": k, "alpha_k": alpha * k,
                                "kR_where_alpha_k_reaches_float64_log_max": log_max / (alpha * k),
                                "representable_at_kR_1": alpha * k < log_max}
    out["hybrid_photon_normalised_radius_Mpc"] = (g1a.R8_H_MPC / h) / p.aD0
    c = out["chains"]
    _gate_printed("GA-OD3 hybrid alpha k (test pin 875.4)", c["1G-A_hybrid_aD0_k_phys0_D_R_8_over_h"]["alpha_k"], 875.4, 1)
    _gate_printed("GA-OD3 audit hybrid alpha k", c["1G-A_hybrid_aD0_k_phys0_D_R_8_over_h"]["alpha_k"], 875.378, 3)
    _gate_printed("GA-OD3 audit (a)", c["photon_normalised_a_equal_mass"]["alpha_k"], 557.44, 2)
    _gate_printed("GA-OD3 audit (b)", c["photon_normalised_b_dressed_8_over_h"]["alpha_k"], 639.66, 2)
    _gate_printed("GA-OD3 audit (c)", c["photon_normalised_c_bare_8_over_hbar"]["alpha_k"], 693.49, 2)
    return out


def ga_f8_regional_radius(ref: dict) -> dict:
    """GA-F8: convention (b) with the (5.1) regional wall scale, R = (8/h)/D_wall."""
    out = {}
    printed = {"PAPER_REFERENCE": (12.494, 0.526, 0.837), "NW15_CMB_FIT": (13.871, 0.613, 0.857)}
    for name in PRIMARY_CASES:
        p = g1a._cases()[name]
        dens = g1a.per_photon_matter_density(p)
        growth = g1a.growth_summary(p)
        om, g0, fv0 = dens["omega_m_per_photon"], dens["gamma_w0"], dens["fv0"]
        d_wall = g0 * (1.0 - fv0) ** (1.0 / 3.0)
        R = (g1a.R8_H_MPC / (dens["H0_dressed_km_s_Mpc"] / 100.0)) / d_wall

        def anchored(growth_today):
            return (g1a.sigma_converged(R, om, g1a.BARYON_FRACTION_PRIMARY, g1a.PLANCK["n_s"],
                                        growth_today) / ref["sigma_eh98"] * g1a.PLANCK["sigma8_linear"])
        out[name] = {"R_Mpc": R,
                     "cgi_comoving": anchored(g0 * growth["comoving"]["g_TS_vs_volume_average_EdS"]),
                     "wall_regional": anchored(d_wall)}
        _gate_printed(f"GA-F8 {name} R", R, printed[name][0], 3)
        _gate_printed(f"GA-F8 {name} comoving", out[name]["cgi_comoving"], printed[name][1], 3)
        _gate_printed(f"GA-F8 {name} wall", out[name]["wall_regional"], printed[name][2], 3)
    return out


# ============================================================ D. Phase 1G-D
def pbs_amplitude(r_seed: float, f_vi: float, omega_m: float) -> dict:
    """[1G-D] Sec. 7 peak-background split, A_v = phi(nu)/(sigma_seed Phi(-nu)), unchanged."""
    sigma_seed = g1d.sigma_large_R(r_seed, omega_m, g1d.A_LS)
    nu = float(-norm.ppf(f_vi))
    return {"R_seed_Mpc": r_seed, "sigma_seed_LS": sigma_seed, "f_vi": f_vi, "nu": nu,
            "A_v": float(norm.pdf(nu) / (sigma_seed * norm.sf(nu)))}


def r_star(A: float, omega_m: float, h: float, f_v0: float) -> dict:
    """R* criteria of [1G-D] Sec. 8, with the frozen bracket and root finder."""
    entry = {}
    for crit_label, target in (("eps=1", 1.0), ("void_fraction_10pct", 0.1 / (1.0 - f_v0)),
                               ("density_10pct", 0.1 / f_v0)):
        lo, hi = 5.0, 3.0e4
        if (A * g1d.sigma_large_R(hi, omega_m, g1d.A_LS) - target) > 0.0:
            entry[crit_label] = {"R_Mpc": None, "R_h_inv_Mpc": None}
            continue
        R = brentq(lambda r: A * g1d.sigma_large_R(r, omega_m, g1d.A_LS) - target, lo, hi, xtol=1e-6)
        entry[crit_label] = {"R_Mpc": R, "R_h_inv_Mpc": R * h}
    return entry


def x_su(base: float, A: float, f_v0: float, f_v_ls: float, g_lcdm: float) -> dict:
    """X_SU for the two readings of delta_L in [1G-D] S2 (GD-OD6).

    wall-mode amplitude (frozen): delta_w(LS) = delta_L, eps = A_v delta_L, so
      D_SU = f_w0 D_wall + A_v a_LS f_v0;
    total contrast (owner decision): the region's contrast at last scattering
      (1 - f_vLS) delta_w(LS) + f_vLS A_v delta_L equals delta_L, so the wall term
      is scaled by (1 - A_v f_vLS)/(1 - f_vLS).
    """
    void_term = A * g1d.A_LS * f_v0
    return {"A_v_f_v_LS": A * f_v_ls,
            "wall_mode_amplitude_frozen": (base + void_term) / g_lcdm,
            "total_contrast_at_LS": (base * (1.0 - A * f_v_ls) / (1.0 - f_v_ls) + void_term) / g_lcdm}


def gd_void_response(ref: dict) -> dict:
    out = {}
    for name in PRIMARY_CASES:
        p = g1a._cases()[name]
        dens = g1a.per_photon_matter_density(p)
        om, fv0, g0 = dens["omega_m_per_photon"], dens["fv0"], dens["gamma_w0"]
        h = dens["H0_dressed_km_s_Mpc"] / 100.0
        t_ls = g1a.t_of_redshift(p, Z_LAST_SCATTERING)
        f_v_ls = float(bg.fv(t_ls, p))
        growth = g1d.growth_histories(p)
        base = growth["f_w0_D_wall_t0"]
        R8_own = _radii(dens, ref)["a_equal_mass"]
        sigma_r8_own = g1d.sigma_large_R(R8_own, om, g1d.A_LS)
        seeds = {"svdw04_factor_1.72": lambda f_vi: R_VOID_H_MPC / g1d.SVDW_SHELL_CROSSING_RADIUS_FACTOR / h,
                 "tracker_consistent": lambda f_vi: (R_VOID_H_MPC / h) * (f_vi / fv0) ** (1 / 3) / g0}

        def variant(seed: str, f_vi: float, *, with_r_star: bool) -> dict:
            pbs = pbs_amplitude(seeds[seed](f_vi), f_vi, om)
            A = pbs["A_v"]
            row = {**pbs, "A_v_sigma_LSS_R8_own": A * sigma_r8_own,
                   "X_SU": x_su(base, A, fv0, f_v_ls, ref["g_lcdm"])}
            if with_r_star:
                row["R_star"] = r_star(A, om, h, fv0)
            return row

        # 1. Frozen reproduction: the generalised functions equal [1G-D]'s own.
        frozen = g1d.transition_scales(dens)
        frozen_su = g1d.super_cell_growth(p, growth, frozen)
        for f_vi in AUDIT_FVI:
            mine = variant("svdw04_factor_1.72", f_vi, with_r_star=True)
            key = f"f_vi={f_vi:g}"
            _gate_rel(f"GD frozen A_v {name} {key}", mine["A_v"], frozen["pbs"][key]["A_v"], FROZEN_REPRO_RTOL)
            _gate_rel(f"GD frozen X_SU {name} {key}", mine["X_SU"]["wall_mode_amplitude_frozen"],
                      frozen_su[f"PBS_{key}"]["X_SU"], FROZEN_REPRO_RTOL)
            for crit, val in frozen["R_star"][f"PBS_{key}"].items():
                if crit != "A_v":
                    _gate_rel(f"GD frozen R* {name} {key} {crit}", mine["R_star"][crit]["R_Mpc"],
                              val["R_Mpc"], FROZEN_REPRO_RTOL)
        case = {"f_v0": fv0, "h_dressed": h, "gamma_w0": g0, "t_LS_over_t0": t_ls / p.t0,
                "f_v_at_LS": f_v_ls, "f_w0_D_wall_t0": base,
                "X_SU_A_v_zero_needs_wall_curvature": base / ref["g_lcdm"],
                "R8_equal_mass_own_Mpc": R8_own, "sigma_LSS_R8_own": sigma_r8_own,
                "sigma_LSS_R8_frozen_12.57": frozen["sigma_LSS_R8"],
                "frozen_pbs_A_v": {f"f_vi={f_vi:g}": frozen["pbs"][f"f_vi={f_vi:g}"]["A_v"]
                                   for f_vi in AUDIT_FVI},
                "frozen_pbs_at_own_radius": {
                    f"f_vi={f_vi:g}": frozen["pbs"][f"f_vi={f_vi:g}"]["A_v"] * sigma_r8_own
                    for f_vi in AUDIT_FVI},
                "variants": {}}
        # 2. The audit's tracker-consistent rows (f_vi = 1e-4, 1e-2; wall-mode S2).
        for f_vi in AUDIT_FVI:
            case["variants"][f"audit_tracker_seed_f_vi={f_vi:g}"] = variant(
                "tracker_consistent", f_vi, with_r_star=True)
        # 3. Owner decisions: f_vi = f_v(t_LS) (GD-OD2), own radius (GD-OD7),
        #    delta_L = total contrast (GD-OD6); tracker seed primary (GD-OD1),
        #    [SvdW04] factor as the quoted alternative.
        case["variants"]["primary_tracker_seed_f_vi_LS"] = variant(
            "tracker_consistent", f_v_ls, with_r_star=True)
        case["variants"]["alternative_svdw04_factor_f_vi_LS"] = variant(
            "svdw04_factor_1.72", f_v_ls, with_r_star=True)
        out[name] = case
    # Gates: the frozen report at [NW15]'s own radius (errata E-1GD-1..3), the
    # 1G-D audit's rows (GD-F1, GD-F2, GD-F6), 1G-F L3 (A_v 1169 / 1185).
    nw = out["NW15_CMB_FIT"]
    _gate_printed("GD-OD7 NW15 sigma_LSS(R8 own) (x1e4)", nw["sigma_LSS_R8_own"] * 1e4, 9.336, 3)
    _gate_printed("GD-OD7 NW15 PBS 1e-4 at own R8", nw["frozen_pbs_at_own_radius"]["f_vi=0.0001"], 4.410, 3)
    _gate_printed("GD-OD7 NW15 PBS 1e-2 at own R8", nw["frozen_pbs_at_own_radius"]["f_vi=0.01"], 2.969, 3)
    audit_rows = {  # (A_v, A_v sigma, X_SU, R* eps=1, R* 10% void fraction, R* 10% density)
        ("PAPER_REFERENCE", 1e-4): (1172, 1.05, 1.30, 9.9, 32.6, 84.3),
        ("PAPER_REFERENCE", 1e-2): (1465, 1.32, 1.55, 13.6, 40.8, 100.8),
        ("NW15_CMB_FIT", 1e-4): (1235, 1.15, 1.35, 9.2, 40.0, 63.0),
        ("NW15_CMB_FIT", 1e-2): (1623, 1.52, 1.63, 13.1, 51.1, 78.5)}
    for (name, f_vi), vals in audit_rows.items():
        row = out[name]["variants"][f"audit_tracker_seed_f_vi={f_vi:g}"]
        tag = f"GD-F1 audit {name} f_vi={f_vi:g}"
        _gate_printed(f"{tag} A_v", row["A_v"], vals[0], 0)
        _gate_printed(f"{tag} A_v sigma", row["A_v_sigma_LSS_R8_own"], vals[1], 2)
        _gate_printed(f"{tag} X_SU", row["X_SU"]["wall_mode_amplitude_frozen"], vals[2], 2)
        for crit, v in zip(("eps=1", "void_fraction_10pct", "density_10pct"), vals[3:]):
            _gate_printed(f"{tag} R* {crit}", row["R_star"][crit]["R_h_inv_Mpc"], v, 1)
    for name, (A_v, x_frozen) in {"PAPER_REFERENCE": (4274, 3.96), "NW15_CMB_FIT": (4914, 4.03)}.items():
        row = out[name]["variants"]["alternative_svdw04_factor_f_vi_LS"]
        _gate_printed(f"GD-F2 audit {name} A_v", row["A_v"], A_v, 0)
        _gate_printed(f"GD-F2 audit {name} X_SU", row["X_SU"]["wall_mode_amplitude_frozen"], x_frozen, 2)
    alt_nw = out["NW15_CMB_FIT"]["variants"]["alternative_svdw04_factor_f_vi_LS"]
    _gate_printed("GD-F2 audit NW15 A_v sigma(R8)", alt_nw["A_v_sigma_LSS_R8_own"], 4.59, 2)
    # The audit inventory's recorded digits (its report rounds 171.5 to "172").
    for crit, v, dec in zip(("eps=1", "void_fraction_10pct", "density_10pct"),
                            (42.44, 121.1, 171.5), (2, 1, 1)):
        _gate_printed(f"GD-F2 audit NW15 R* {crit}", alt_nw["R_star"][crit]["R_h_inv_Mpc"], v, dec)
    # GD-F6: the frozen PBS amplitudes (seed factor 1.72, f_vi = 1e-4, 1e-2) with
    # the tracker's f_v(t_LS) in the last-scattering contrast.
    gm = out["PAPER_REFERENCE"]
    for f_vi, xf, xt in ((1e-4, 3.95, 3.83), (1e-2, 2.75, 2.67)):
        A = gm["frozen_pbs_A_v"][f"f_vi={f_vi:g}"]
        xs = x_su(gm["f_w0_D_wall_t0"], A, gm["f_v0"], gm["f_v_at_LS"], ref["g_lcdm"])
        gm[f"GD-F6_frozen_pbs_f_vi={f_vi:g}"] = xs
        _gate_printed(f"GD-F6 audit GM f_vi={f_vi:g} frozen S2", xs["wall_mode_amplitude_frozen"], xf, 2)
        _gate_printed(f"GD-F6 audit GM f_vi={f_vi:g} total contrast", xs["total_contrast_at_LS"], xt, 2)
    for name, printed in {"PAPER_REFERENCE": 1169, "NW15_CMB_FIT": 1185}.items():
        _gate_printed(f"1G-F L3 {name} tracker-seed A_v",
                      out[name]["variants"]["primary_tracker_seed_f_vi_LS"]["A_v"], printed, 0)
    return out


# ============================================================ E. Phase 1G-E
def mass_conserving_sigma(s2p: float, s2i: float, f_v: float, delta_v: float) -> float:
    """GE-F1: sigma^2 = delta_v^2 sigma_part^2 + (f_w - f_v delta_v)^2 sigma_int^2."""
    return math.sqrt(delta_v ** 2 * s2p + ((1.0 - f_v) - f_v * delta_v) ** 2 * s2i)


def ge_single_radius(ref: dict) -> dict:
    """[1G-E] one-radius Boolean model under the owner decisions (E4 frames, both radii)."""
    out = {}
    for name in PRIMARY_CASES:
        p = g1a._cases()[name]
        dens = g1a.per_photon_matter_density(p)
        f_v, h, om = dens["fv0"], dens["H0_dressed_km_s_Mpc"] / 100.0, dens["omega_m_per_photon"]
        d_wall = dens["gamma_w0"] * (1.0 - f_v) ** (1.0 / 3.0)
        frames = {"photon_frame_D_wall": d_wall, "a_D_frame_fw13": (1.0 - f_v) ** (1.0 / 3.0),
                  "uncompressed": 1.0}
        radii = {"b_dressed_8_over_h": g1a.R8_H_MPC / h,
                 "a_equal_mass": _radii(dens, ref)["a_equal_mass"]}
        case = {"f_v0": f_v, "D_wall_t0": d_wall, "compressions": frames, "radii_Mpc": radii,
                "rows": {}}
        for conv, R in radii.items():
            for a_h in VOID_RADII_H_MPC:
                a = a_h / h
                s2p = g1e.sigma2_partition(R, a, f_v)
                row = {"sigma_part": math.sqrt(s2p)}
                for frame, s in frames.items():
                    s2i = g1e.sigma2_internal(R, a, f_v, om, d_wall, s) * ref["anchor_factor"] ** 2
                    row[f"sigma_int_{frame}"] = math.sqrt(s2i)
                    for dv in DELTA_V_VALUES:
                        row[f"sigma_{frame}_dv{dv:+.1f}_mass_conserving"] = mass_conserving_sigma(s2p, s2i, f_v, dv)
                        row[f"sigma_{frame}_dv{dv:+.1f}_frozen_formula"] = math.sqrt(dv * dv * s2p + s2i)
                case["rows"][f"{conv}/a={a_h:g}"] = row
        out[name] = case
    # Ranges over a = 5-30 and delta_v in {-1, -0.8} (mass-conserving).
    ranges = {}
    for label, frames in (("audit_set_fw13_and_uncompressed", ("a_D_frame_fw13", "uncompressed")),
                          ("all_three_frames", ("a_D_frame_fw13", "photon_frame_D_wall", "uncompressed")),
                          ("photon_frame_only", ("photon_frame_D_wall",))):
        for conv in ("b_dressed_8_over_h", "a_equal_mass"):
            vals = {name: [out[name]["rows"][f"{conv}/a={a_h:g}"][f"sigma_{fr}_dv{dv:+.1f}_mass_conserving"]
                           for a_h in VOID_RADII_H_MPC for fr in frames for dv in (-1.0, -0.8)]
                    for name in PRIMARY_CASES}
            ranges[f"{label}/{conv}"] = {name: [min(v), max(v)] for name, v in vals.items()}
    out["ranges_mass_conserving_a5_30_dv_-1_-0.8"] = ranges
    gm, nw = out["PAPER_REFERENCE"]["rows"], out["NW15_CMB_FIT"]["rows"]
    b15, a15 = "b_dressed_8_over_h/a=15", "a_equal_mass/a=15"
    # The a = 15 values recorded (to four decimals) in the frozen 1G-F inventory,
    # headline.<case>.monodisperse_a15_1G-E_reevaluated: [1G-E] itself, lead
    # observation L1 (photon frame) and the 1G-E audit's GE-F1 values.
    recorded = json.loads((ROOT / "reports" / "phase1g_f_void_population_inventory.json")
                          .read_text(encoding="utf-8"))["headline"]
    for mine, theirs in (("sigma_part", "sigma_part"),
                         ("sigma_int_a_D_frame_fw13", "sigma_int_compressed_fw13"),
                         ("sigma_int_photon_frame_D_wall", "sigma_int_photon_frame_Dwall"),
                         ("sigma_int_uncompressed", "sigma_int_uncompressed"),
                         ("sigma_a_D_frame_fw13_dv-1.0_mass_conserving", "sigma_total_empty_voids"),
                         ("sigma_photon_frame_D_wall_dv-1.0_mass_conserving",
                          "sigma_total_photon_frame_Dwall_empty_voids"),
                         ("sigma_uncompressed_dv-1.0_mass_conserving", "sigma_total_uncompressed_empty_voids"),
                         ("sigma_a_D_frame_fw13_dv-0.8_frozen_formula", "sigma_total_fw13_delta_v_-0.8_as_1G-E"),
                         ("sigma_a_D_frame_fw13_dv-0.8_mass_conserving",
                          "sigma_total_fw13_delta_v_-0.8_mass_conserving")):
        for name, rows in (("PAPER_REFERENCE", gm), ("NW15_CMB_FIT", nw)):
            _gate_printed(f"GE a=15 (b) {name} {mine}", rows[b15][mine],
                          recorded[name]["monodisperse_a15_1G-E_reevaluated"][theirs], 4)
    _gate_printed("GE-F1 audit GM dv -0.9", gm[b15]["sigma_a_D_frame_fw13_dv-0.9_mass_conserving"], 1.435, 3)
    _gate_printed("GE-F1 audit NW15 dv -0.9", nw[b15]["sigma_a_D_frame_fw13_dv-0.9_mass_conserving"], 1.249, 3)
    _gate_printed("GE-F4 audit GM equal mass", gm[a15]["sigma_a_D_frame_fw13_dv-1.0_mass_conserving"], 1.437, 3)
    _gate_printed("GE-F4 audit NW15 equal mass", nw[a15]["sigma_a_D_frame_fw13_dv-1.0_mass_conserving"], 1.419, 3)
    audit = ranges["audit_set_fw13_and_uncompressed/b_dressed_8_over_h"]
    _gate_printed("GE-F1 audit GM range low", audit["PAPER_REFERENCE"][0], 0.82, 2)
    _gate_printed("GE-F1 audit GM range high", audit["PAPER_REFERENCE"][1], 2.12, 2)
    _gate_printed("GE-F1 audit NW15 range low", audit["NW15_CMB_FIT"][0], 0.80, 2)
    _gate_printed("GE-F1 audit NW15 range high", audit["NW15_CMB_FIT"][1], 1.74, 2)
    return out


def ge_reference_population(ref: dict) -> dict:
    """GE-OD2: the 1G-F self-consistent population (C1 wall clock, shell crossing,
    collapse threshold, f = f_v0, empty voids) at convention (b) and equal mass (a)."""
    sph = g1f.spherical_model()
    barrier = {"delta_v": sph["shell_crossing"]["delta_v"],
               "interior_density_ratio": sph["shell_crossing"]["one_plus_delta_sc"]}
    dc = sph["delta_c"]["collapse"]
    out = {"clock": "C1_WALL_EDS_COMMON_TIME", "barrier": "shell_crossing", "delta_c": dc,
           "normalisation": "tracker_f_v0", "void_interior": "empty (E1)"}
    for name in PRIMARY_CASES:
        p = g1a._cases()[name]
        dens = g1a.per_photon_matter_density(p)
        f_v, h, om = dens["fv0"], dens["H0_dressed_km_s_Mpc"] / 100.0, dens["omega_m_per_photon"]
        d_wall = dens["gamma_w0"] * (1.0 - f_v) ** (1.0 / 3.0)
        table = g1f.sigma_table(om, ref["anchor_factor"])
        pop = g1f.void_population(table, d_wall, barrier, dc, d_wall, h)
        rho, pw = g1f._rho_weights(pop, h)
        case = {"volume_weighted_median_radius_h_inv_Mpc": pop["volume_weighted_median_radius_h_inv_Mpc"]}
        for conv, R in (("b_dressed_8_over_h", g1a.R8_H_MPC / h),
                        ("a_equal_mass", _radii(dens, ref)["a_equal_mass"])):
            kern = g1f.PairKernel(R)
            xi = g1f.xi_wall_poly(kern.r, rho, pw, f_v)
            s2p = kern.sigma2_part(xi)
            row = {"R_Mpc": R, "sigma_part": math.sqrt(s2p)}
            for frame, s in (("photon_frame_D_wall", d_wall), ("a_D_frame_fw13", (1.0 - f_v) ** (1 / 3))):
                s2i = kern.sigma2_int(xi, om, d_wall, s, ref["anchor_factor"])
                row[f"sigma_int_{frame}"] = math.sqrt(s2i)
                row[f"sigma_{frame}_empty_voids"] = g1f.total_sigma(s2p, s2i, f_v, -1.0)
            case[conv] = row
        out[name] = case
    # The frozen 1G-F inventory (four decimals), headline.<case>.
    # variance_tracker_normalised["C1_WALL_EDS_COMMON_TIME/shell_crossing"].
    recorded = json.loads((ROOT / "reports" / "phase1g_f_void_population_inventory.json")
                          .read_text(encoding="utf-8"))["headline"]
    for name in PRIMARY_CASES:
        row = out[name]["b_dressed_8_over_h"]
        rec = recorded[name]["variance_tracker_normalised"]["C1_WALL_EDS_COMMON_TIME/shell_crossing"]
        for mine, theirs in (("sigma_part", "sigma_part"),
                             ("sigma_int_photon_frame_D_wall", "sigma_int_photon_frame"),
                             ("sigma_photon_frame_D_wall_empty_voids", "sigma_total_empty_voids_photon_frame"),
                             ("sigma_a_D_frame_fw13_empty_voids", "sigma_total_empty_voids_1G-E_fw13")):
            _gate_printed(f"GE-OD2 1G-F {name} {mine}", row[mine], rec[theirs], 4)
    return out


def ge_mc_seed_scatter() -> dict:
    """GE-OD5: the frozen [1G-E] Monte Carlo (a = 15 h^-1 Mpc) over 16 seeds.

    The frozen ``monte_carlo_boolean`` reads the module globals MC_SEED and
    MC_REL_GATE at call time.  For each seed MC_SEED is set, and MC_REL_GATE is
    set to +inf in memory only so that a seed above the gate still returns its
    numbers; the frozen 5% gate is then evaluated here, per seed, unchanged.
    Both globals are restored afterwards.  The script file is not modified.
    """
    saved = (g1e.MC_SEED, g1e.MC_REL_GATE)
    out = {"seeds": list(MC_SEEDS), "gate": MC_REL_GATE, "gated_min_xi": MC_GATED_MIN_XI}
    try:
        g1e.MC_REL_GATE = math.inf
        for name in PRIMARY_CASES:
            p = g1a._cases()[name]
            dens = g1a.per_photon_matter_density(p)
            f_v, h = dens["fv0"], dens["H0_dressed_km_s_Mpc"] / 100.0
            a, R = 15.0 / h, g1a.R8_H_MPC / h
            sig2_nominal = g1e.sigma2_partition(R, a, f_v)
            rows = []
            for seed in MC_SEEDS:
                g1e.MC_SEED = seed
                mc = g1e.monte_carlo_boolean(a, f_v, R)
                nominal = [abs(mc["f_w_mc"] / (1.0 - f_v) - 1.0),
                           abs(mc["sigma2_part_mc"] / sig2_nominal - 1.0)]
                for key, cov in mc["covariance"].items():
                    xi_nom = float(g1e.xi_wall_indicator(float(key[2:]) * a, a, f_v))
                    if xi_nom >= MC_GATED_MIN_XI:
                        nominal.append(abs(cov["mc"] / xi_nom - 1.0))
                rows.append({"seed": seed, "n_balls": mc["n_balls"],
                             "gated_max_realised": mc["max_rel_err_gated"],
                             "gated_max_nominal": max(nominal),
                             "sigma2_part_rel_realised": mc["sigma2_part_mc"] / mc["sigma2_part_analytic_realisation"] - 1.0,
                             "fails_gate_realised": mc["max_rel_err_gated"] > MC_REL_GATE,
                             "fails_gate_nominal": max(nominal) > MC_REL_GATE})
            gated = [r["gated_max_realised"] for r in rows]
            out[name] = {"rows": rows,
                         "gated_max_realised_min_median_max": [min(gated), statistics.median(gated), max(gated)],
                         "seeds_failing_realised": sum(r["fails_gate_realised"] for r in rows),
                         "seeds_failing_nominal": sum(r["fails_gate_nominal"] for r in rows),
                         "sigma2_part_rel_sd": statistics.stdev(r["sigma2_part_rel_realised"] for r in rows),
                         "first_run_note_f_w_shift_for_2pct_fewer_balls": -math.log(1.0 - f_v) * 0.02}
    finally:
        g1e.MC_SEED, g1e.MC_REL_GATE = saved
    for name, (lo, med, hi, fails, fails_nom) in {"PAPER_REFERENCE": (0.0100, 0.031, 0.0503, 1, 3),
                                                  "NW15_CMB_FIT": (0.0016, 0.0097, 0.0395, 0, 1)}.items():
        s = out[name]
        _gate_printed(f"GE-F5 audit {name} min", s["gated_max_realised_min_median_max"][0], lo, 4)
        _gate_printed(f"GE-F5 audit {name} median", s["gated_max_realised_min_median_max"][1], med, 4 if name == "NW15_CMB_FIT" else 3)
        _gate_printed(f"GE-F5 audit {name} max", s["gated_max_realised_min_median_max"][2], hi, 4)
        _gate_abs(f"GE-F5 audit {name} seeds failing (realised)", s["seeds_failing_realised"], fails, 0)
        _gate_abs(f"GE-F5 audit {name} seeds failing (nominal)", s["seeds_failing_nominal"], fails_nom, 0)
    _gate_printed("GE-F5 first-run GM", out["PAPER_REFERENCE"]["first_run_note_f_w_shift_for_2pct_fewer_balls"], 0.027, 3)
    _gate_printed("GE-F5 first-run NW15", out["NW15_CMB_FIT"]["first_run_note_f_w_shift_for_2pct_fewer_balls"], 0.020, 3)
    return out


def main() -> int:
    ref = _planck_reference()
    results = {
        "planck_reference": ref,
        "GA_OD2_nw15_own_early_universe_inputs": ga_od2_nw15_own_inputs(ref),
        "GA_OD3_wkb_exponent_chains": ga_od3_exponent_chains(ref),
        "GA_F8_regional_radius_reading": ga_f8_regional_radius(ref),
        "GD_void_response": gd_void_response(ref),
        "GE_single_radius": ge_single_radius(ref),
        "GE_reference_population_1G_F": ge_reference_population(ref),
        "GE_mc_seed_scatter": ge_mc_seed_scatter(),
    }
    payload = {"phase": "1G owner decisions (2026-09-30)",
               "status": ("OWNER_DECISION_EVIDENCE; CONDITIONAL; MODEL_INTERNAL; "
                          "NOT_OBSERVATIONAL; NOT_SIGMA8"),
               "environment": {"python": sys.version.split()[0], "numpy": np.__version__,
                               "scipy": scipy.__version__, "platform": platform.platform(),
                               "resource_module": RESOURCE_MODULE},
               "budgets": {"FROZEN_REPRO_RTOL": FROZEN_REPRO_RTOL,
                           "PRINTED_HALF_UNIT_SLACK": PRINTED_HALF_UNIT_SLACK,
                           "MC_REL_GATE": MC_REL_GATE, "MC_GATED_MIN_XI": MC_GATED_MIN_XI},
               "gates": GATES,
               "results": g1f._clean(results)}
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
                        encoding="utf-8")
    print(f"{sum(g['pass'] for g in GATES)}/{len(GATES)} gates pass")
    print(f"wrote {ARTIFACT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
