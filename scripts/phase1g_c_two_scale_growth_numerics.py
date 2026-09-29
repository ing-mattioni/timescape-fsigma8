"""Numerical evidence for the report-only Phase 1G-C two-scale growth-law audit.

Report: reports/phase1g_c_two_scale_growth_law.md (sections cited as [1G-C]).
Writes artifacts/independent/phase1g_c_two_scale_growth.json (git-ignored).

Every Timescape quantity comes from frozen package functions
(timescape_fsigma8.background: [GM] Eqs. (5.1), (5.3)-(5.7) and text p. 25;
[W09] App. B).  The sigma machinery (EH98 early spectrum, radius conventions)
is reused unchanged from scripts/phase1g_a_sigma8_path_numerics.py.

[GM] = Galoppo & Mourier, arXiv:2511.17160v2; [W09] = Wiltshire,
arXiv:0909.0749v2.  No package module, status token or tolerance is changed.
Outputs are conditional, model-internal numbers; none is an observational sigma_8.
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
from scipy.integrate import solve_ivp

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations.growing_mode import CleanPerturbationSystem
from timescape_fsigma8.perturbations.initial_conditions import PLANCK_2018_QPLUS_RECIPE, qplus

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "independent" / "phase1g_c_two_scale_growth.json"

_spec = importlib.util.spec_from_file_location(
    "phase1g_a_numerics", ROOT / "scripts" / "phase1g_a_sigma8_path_numerics.py")
g1a = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g1a)

G = 1.0
# Explicit budgets (AGENTS.md rule 9).
DECOMPOSITION_RTOL = 1e-13        # exact algebraic identities of the tracker
REGIONAL_SOLVE_RTOL = 1e-12       # solve_ivp controls for the wall-region equation
REGIONAL_SOLVE_ATOL = 1e-15
REGIONAL_VS_T23_RTOL = 1e-8       # numerical wall growth vs exact t^(2/3)
EARLY_START_FRACTION = 1e-8       # start of the wall-region integration, in t0


def decomposition(p: TrackerParams) -> dict:
    """Exact two-region structure of the tracker in the common time t ([1G-C] Sec. 3).

    Regional volumes from [GM] Eq. (5.1): V_v/V_D = f_v, V_w/V_D = 1 - f_v, so
    a_v^3 = f_v a_D^3/f_vi and a_w,reg^3 = (1-f_v) a_D^3/f_wi.
    """
    t = np.geomspace(1e-7 * p.t0, p.t0, 4001)
    f = np.asarray(bg.fv(t, p))
    aD = np.asarray(bg.a_D(t, p))
    HD = np.asarray(bg.H_D(t, p))
    rho = np.asarray(bg.rho_d(t, p, G))
    Q = np.asarray(bg.Q_D(t, p))
    R = np.asarray(bg.R_D(t, p))
    gam = np.asarray(bg.gamma_w(t, p))

    def rel_variation(x):
        return float(x.max() / x.min() - 1.0)

    def max_rel(a, b):
        return float(np.max(np.abs(a - b) / np.abs(b)))

    Hv, Hw = 1.0 / t, 2.0 / (3.0 * t)
    rho_w = 1.0 / (6.0 * math.pi * G * t ** 2)
    checks = {
        "void_scale_a_v3_over_t3_variation": rel_variation(f * aD ** 3 / t ** 3),
        "wall_scale_a_w3_over_t2_variation": rel_variation((1 - f) * aD ** 3 / t ** 2),
        "H_D_vs_fv_Hv_plus_fw_Hw": max_rel(f * Hv + (1 - f) * Hw, HD),
        "mean_density_vs_fw_rho_w": max_rel((1 - f) * rho_w, rho),
        "Q_D_vs_6_fv_fw_(Hv-Hw)^2": max_rel(6 * f * (1 - f) * (Hv - Hw) ** 2, Q),
        "R_D_vs_fv_times_milne_curvature": max_rel(f * (-6.0 * Hv ** 2), R),
        "uniform_quasilocal_flow_gamma_w_Hw_vs_H_D": max_rel(gam * Hw, HD),
    }
    for name, value in checks.items():
        if value > DECOMPOSITION_RTOL:
            raise AssertionError(f"decomposition identity {name} failed: {value}")
    g0 = float(bg.gamma_w(p.t0, p))
    return {
        "identities_max_rel": checks,
        "wall_overdensity_today_rho_w_over_mean": 1.0 / (1.0 - p.fv0),
        "proper_time_flat_dust_residual_today": g0 ** 2 - 1.0,
        "gamma_w0": g0,
    }


def wall_regional_growth(p: TrackerParams) -> dict:
    """Integrate the regional wall equation with package-derived coefficients.

    [GM] dust-frame CGI system (4.9)-(4.12) on the wall regional background,
    where rho_eff = 0 (flat, no internal backreaction; [W09] line 510), reduces
    to [GM] Eq. (4.27) with the regional coefficients:
        Delta'' + 2 H_w Delta' - 4 pi G rho_w Delta = 0,
    H_w = H_D - fdot_v/(3(1-f_v)),  rho_w = <rho>/(1-f_v)   (from [GM] (5.1)).
    """
    def coeffs(t):
        f = float(bg.fv(t, p))
        Hw = float(bg.H_D(t, p)) - float(bg.dfv_dt(t, p)) / (3.0 * (1.0 - f))
        rho_w = float(bg.rho_d(t, p, G)) / (1.0 - f)
        return Hw, rho_w

    def rhs(t, y):
        Hw, rho_w = coeffs(t)
        return [y[1], 4.0 * math.pi * G * rho_w * y[0] - 2.0 * Hw * y[1]]

    t_e = EARLY_START_FRACTION * p.t0
    y0 = [1.0, (2.0 / 3.0) / t_e]            # EdS growing mode at t_e
    ts = np.geomspace(t_e, p.t0, 9)
    sol = solve_ivp(rhs, (t_e, p.t0), y0, method="DOP853", t_eval=ts,
                    rtol=REGIONAL_SOLVE_RTOL, atol=REGIONAL_SOLVE_ATOL,
                    dense_output=False, max_step=np.inf, first_step=None, vectorized=False)
    if not sol.success:
        raise RuntimeError(sol.message)
    exact = (ts / t_e) ** (2.0 / 3.0)
    dev = float(np.max(np.abs(sol.y[0] / exact - 1.0)))
    if dev > REGIONAL_VS_T23_RTOL:
        raise AssertionError(f"wall regional growth deviates from t^(2/3): {dev}")
    Hw0, _ = coeffs(p.t0)
    return {"max_rel_dev_from_t23": dev, "H_w_t0_times_t0": Hw0 * p.t0}


def summary() -> dict:
    cases = g1a._cases()
    g_lcdm = float(qplus(0.0, PLANCK_2018_QPLUS_RECIPE))
    density = {name: g1a.per_photon_matter_density(p) for name, p in cases.items()}
    growth = {name: g1a.growth_summary(p) for name, p in cases.items()}
    sigma = g1a.spectrum_and_sigma(density, growth)
    out = {}
    for name, p in cases.items():
        wall_factor = float(bg.gamma_w(p.t0, p)) * (1.0 - p.fv0) ** (1.0 / 3.0)
        x_wall = wall_factor / g_lcdm
        entry = {
            "decomposition": decomposition(p),
            "wall_regional_growth_numeric": wall_regional_growth(p),
            "g_wall_vs_volume_average_EdS": (1.0 - p.fv0) ** (1.0 / 3.0),
            "X_wall": x_wall,
            "closures": {},
        }
        conv_E = sigma["cases"][name]["closures"]["comoving"]["conventions"]
        entry["sigma_wall_planck_anchored"] = {
            label: x_wall * cv["E_early_spectrum_factor"] * g1a.PLANCK["sigma8_linear"]
            for label, cv in conv_E.items()}
        for system in CleanPerturbationSystem:
            x_cgi = growth[name][system.value]["X_inf"]
            entry["closures"][system.value] = {
                "X_volume_average_cgi": x_cgi,
                "power_step_(X_wall/X_cgi)^2": (x_wall / x_cgi) ** 2,
                "amplitude_step_X_wall/X_cgi": x_wall / x_cgi,
            }
        out[name] = entry
    scan = []
    for fv0 in (0.50, 0.60, 0.627, 0.695, 0.737, 0.80):
        p = TrackerParams.from_dressed_H0(fv0=fv0, H0=1.0)
        x_wall = (1.0 + fv0 / 2.0) * (1.0 - fv0) ** (1.0 / 3.0) / g_lcdm
        row = {"fv0": fv0, "X_wall": x_wall}
        for system in CleanPerturbationSystem:
            g = math.exp(g1a._riccati_log_growth_excess(
                p, system, g1a.EARLY_TIME_FRACTIONS[-1] * p.t0, g1a.GROWTH_GRID_POINTS[-1]))
            row[f"X_cgi_{system.value}"] = (1.0 + fv0 / 2.0) * g / g_lcdm
            row[f"power_step_{system.value}"] = (x_wall / row[f"X_cgi_{system.value}"]) ** 2
        scan.append(row)
    return {"g_lcdm": g_lcdm, "cases": out, "fv0_scan": scan}


def main() -> int:
    payload = {
        "phase": "1G-C",
        "status": "REPORT_ONLY_AUDIT_EVIDENCE; CONDITIONAL; NOT_OBSERVATIONAL; NOT_SIGMA8",
        "environment": {"python": sys.version.split()[0], "numpy": np.__version__,
                        "scipy": scipy.__version__, "platform": platform.platform()},
        "results": summary(),
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {ARTIFACT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
