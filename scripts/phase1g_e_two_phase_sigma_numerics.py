"""Numerical evidence for the report-only Phase 1G-E two-phase mass-variance audit.

Report: reports/phase1g_e_two_phase_sigma.md (sections cited as [1G-E]).
Writes artifacts/independent/phase1g_e_two_phase_sigma.json (git-ignored).

Model ([1G-E] Sec. 3): empty voids (the tracker's rho_v = 0, [1G-C] Sec. 3)
filling f_v0 of the volume as a Boolean model of Poisson-placed balls of
radius a; walls carry all the mass at rho_w = <rho>/f_w plus the linear
wall-internal field of [1G-C] (growth D_wall(t0) = gamma_w0 (1-f_v0)^(1/3)).
The mass variance in a ball of radius R is
    sigma^2 = sigma_part^2 + sigma_int^2,
    sigma_part^2 = int P_R(r) xi_w(r) dr,            xi_w(r) = exp(lambda gamma(r)) - 1,
    sigma_int^2  = int P_R(r) (1 + xi_w(r)) xi_E(r) dr,
with gamma(r) the ball covariogram, P_R the pair-separation density in a
ball, and xi_E the wall-internal correlation function in Eulerian
coordinates.  The Boolean covariance is standard stochastic geometry (e.g.
Chiu, Stoyan, Kendall & Mecke, Stochastic Geometry and its Applications,
3rd ed., 2013, Sec. 3.1); it is checked here against a Monte Carlo
realisation.  The early spectrum reuses the 1G-A EH98 import unchanged.
No package module, status token or tolerance changes.  Outputs are
conditional, model-internal numbers; none is an observational sigma_8.
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
from scipy.integrate import quad, simpson
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "independent" / "phase1g_e_two_phase_sigma.json"
_spec = importlib.util.spec_from_file_location(
    "phase1g_a_numerics", ROOT / "scripts" / "phase1g_a_sigma8_path_numerics.py")
g1a = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g1a)

# Explicit budgets and model inputs (AGENTS.md rule 9).
QUAD_RTOL = 1e-11
IDENTITY_RTOL = 1e-10            # pair-density identity int P_R j0 = W^2 (quadrature check)
K_POINTS = 4001
K_X_BOUNDS = (1e-4, 300.0)       # x = kR range for sigma_int
R_PANELS, R_NODES = 400, 16      # composite Gauss-Legendre in r for K(k)
MC_SEED = 20260929
MC_BOX = 30.0                    # box side in units of a (periodic)
MC_POINTS = 2_000_000
MC_BALLS, MC_POINTS_PER_BALL = 4000, 1500
MC_REL_GATE = 0.05               # Monte Carlo vs analytic (statistical, fixed seed)
MC_GATED_MIN_XI = 0.4            # covariance points gated only where xi_w >= 0.4 (noise)
R_H_MPC = 8.0                    # the "8" of 8 h^-1 Mpc, explicit
VOID_RADII_H_MPC = (5.0, 7.5, 10.0, 15.0, 20.0, 30.0)   # [W09] line 277: 30 h^-1 Mpc diameter
VOID_INTERIOR_CONTRASTS = (-1.0, -0.9, -0.8)            # -1 is the tracker (rho_v = 0)


def covariogram_ratio(u):
    """gamma(r)/V_ball for a ball of radius a, u = r/a (zero beyond u = 2)."""
    u = np.asarray(u, dtype=float)
    return np.where(u < 2.0, 1.0 - 0.75 * u + u ** 3 / 16.0, 0.0)


def xi_wall_indicator(r, a, f_v):
    """Boolean-model wall-indicator correlation exp(lambda gamma(r)) - 1, lambda V = -ln f_w."""
    return np.expm1(-math.log(1.0 - f_v) * covariogram_ratio(np.asarray(r) / a))


def pair_density(r, R):
    """Pair-separation density of two uniform points in a ball of radius R (int = 1)."""
    x = np.asarray(r, dtype=float) / R
    return np.where(x <= 2.0, 3.0 * np.asarray(r) ** 2 / R ** 3 * (1 - 0.75 * x + x ** 3 / 16), 0.0)


def sigma2_partition(R, a, f_v):
    return quad(lambda r: float(pair_density(r, R) * xi_wall_indicator(r, a, f_v)),
                0.0, 2.0 * R, epsabs=0.0, epsrel=QUAD_RTOL, limit=400)[0]


def _r_nodes(R):
    x, w = np.polynomial.legendre.leggauss(R_NODES)
    edges = np.linspace(0.0, 2.0 * R, R_PANELS + 1)
    mid, half = 0.5 * (edges[1:] + edges[:-1]), 0.5 * (edges[1:] - edges[:-1])
    return (mid[:, None] + half[:, None] * x[None, :]).ravel(), (half[:, None] * w[None, :]).ravel()


def kernel(k, R, weight):
    """K(k) = int P_R(r) weight(r) j0(k r) dr, composite Gauss-Legendre in r."""
    r, w = _r_nodes(R)
    base = pair_density(r, R) * weight(r) * w
    kr = np.outer(k, r)
    return (np.sinc(kr / math.pi) * base[None, :]).sum(axis=1)


def pair_identity_check(R):
    """int P_R(r) j0(kr) dr must equal W_TH(kR)^2 (exact identity)."""
    k = np.array([0.01, 0.3, 1.0, 3.0, 10.0, 60.0]) / R
    got = kernel(k, R, lambda r: np.ones_like(r))
    want = g1a.tophat(k * R) ** 2
    err = float(np.max(np.abs(got - want) / np.maximum(want, 1e-12)))
    if err > IDENTITY_RTOL and np.max(np.abs(got - want)) > 1e-12:
        raise AssertionError(f"pair-density identity failed: {err}")
    return err


def monte_carlo_boolean(a, f_v, R):
    """Independent check: Poisson balls in a periodic box; covariance and ball variance."""
    rng = np.random.default_rng(MC_SEED)
    L = MC_BOX * a
    lam = -math.log(1.0 - f_v) / (4.0 / 3.0 * math.pi * a ** 3)
    centres = rng.uniform(0.0, L, size=(rng.poisson(lam * L ** 3), 3))
    # Compare with the formula at the realisation's own intensity, so the
    # Poisson fluctuation of the ball count is not mistaken for a model error.
    f_v_eff = 1.0 - math.exp(-len(centres) / L ** 3 * (4.0 / 3.0 * math.pi * a ** 3))
    tree = cKDTree(centres, boxsize=L)

    def in_wall(points):
        d, _ = tree.query(np.mod(points, L), k=1)
        return d > a

    x = rng.uniform(0.0, L, size=(MC_POINTS, 3))
    wx = in_wall(x)
    f_w_mc = float(wx.mean())
    cov = {}
    for u in (0.25, 0.5, 1.0, 1.5):
        n = rng.normal(size=(MC_POINTS, 3))
        y = x + u * a * n / np.linalg.norm(n, axis=1)[:, None]
        both = float((wx & in_wall(y)).mean())
        cov[f"u={u}"] = {"mc": both / f_w_mc ** 2 - 1.0,
                         "analytic": float(xi_wall_indicator(u * a, a, f_v_eff))}
    # Variance of the wall-volume fraction in balls of radius R.
    centres_b = rng.uniform(0.0, L, size=(MC_BALLS, 3))
    v = rng.normal(size=(MC_BALLS, MC_POINTS_PER_BALL, 3))
    v /= np.linalg.norm(v, axis=2)[:, :, None]
    rad = R * rng.uniform(size=(MC_BALLS, MC_POINTS_PER_BALL, 1)) ** (1.0 / 3.0)
    pts = (centres_b[:, None, :] + rad * v).reshape(-1, 3)
    wfrac = in_wall(pts).reshape(MC_BALLS, MC_POINTS_PER_BALL).mean(axis=1)
    raw = float(wfrac.var(ddof=1))
    shot = float(np.mean(wfrac * (1 - wfrac)) / (MC_POINTS_PER_BALL - 1))
    sig2_mc = (raw - shot) / f_w_mc ** 2
    sig2_an = sigma2_partition(R, a, f_v_eff)
    out = {"n_balls": len(centres), "f_v_nominal": f_v, "f_v_realisation": f_v_eff,
           "f_w_mc": f_w_mc, "f_w_realisation_analytic": 1.0 - f_v_eff, "covariance": cov,
           "sigma2_part_mc": sig2_mc, "sigma2_part_analytic_realisation": sig2_an}
    errs = [abs(f_w_mc / (1 - f_v_eff) - 1), abs(sig2_mc / sig2_an - 1)]
    errs += [abs(c["mc"] / c["analytic"] - 1) for c in cov.values() if c["analytic"] >= MC_GATED_MIN_XI]
    out["max_rel_err_gated"] = float(max(errs))
    out["ungated_small_xi"] = {k: abs(c["mc"] / c["analytic"] - 1) for k, c in cov.items()
                               if c["analytic"] < MC_GATED_MIN_XI}
    if out["max_rel_err_gated"] > MC_REL_GATE:
        raise AssertionError(f"Monte Carlo disagrees with Boolean formula: {out['max_rel_err_gated']}")
    return out


def sigma2_internal(R_mpc, a_mpc, f_v, omega_m, growth, compression):
    """sigma_int^2 = int dlnk Delta^2_E(k) K(k), Delta^2_E(k) = Delta^2_L(k * compression)."""
    x = np.exp(np.linspace(math.log(K_X_BOUNDS[0]), math.log(K_X_BOUNDS[1]), K_POINTS))
    k = x / R_mpc
    kl = k * compression
    amp = (4 / 25) * g1a.PLANCK["A_s"] * (kl / g1a.PLANCK["k_pivot_Mpc"]) ** (g1a.PLANCK["n_s"] - 1)
    d2 = amp * (kl / (100.0 / g1a.C_KM_S)) ** 4 * g1a.eh98_nowiggle_transfer(
        kl, omega_m, g1a.BARYON_FRACTION_PRIMARY) ** 2 * growth ** 2 / omega_m ** 2
    K = kernel(k, R_mpc, lambda r: 1.0 + xi_wall_indicator(r, a_mpc, f_v))
    return float(simpson(d2 * K, x=np.log(x)))


def main() -> int:
    cases = g1a._cases()
    density = {n: g1a.per_photon_matter_density(p) for n, p in cases.items()}
    om_L, h_L = g1a.PLANCK["omega_m_total_Om_h2"], g1a.PLANCK["h"]
    sig_L = g1a.sigma_converged(8.0 / h_L, om_L, g1a.BARYON_FRACTION_PRIMARY, g1a.PLANCK["n_s"],
                                float(g1a.qplus(0.0, g1a.PLANCK_2018_QPLUS_RECIPE)))
    anchor = g1a.PLANCK["sigma8_linear"] / sig_L       # EH98 -> Planck anchoring (1G-A Sec. 6.3)
    results = {"eh98_anchor_factor": anchor, "cases": {}}
    for name in ("PAPER_REFERENCE", "NW15_CMB_FIT"):
        dens = density[name]
        f_v, h = dens["fv0"], dens["H0_dressed_km_s_Mpc"] / 100.0
        gamma0 = dens["gamma_w0"]
        d_wall = gamma0 * (1 - f_v) ** (1.0 / 3.0)
        R = R_H_MPC / h
        case = {"f_v0": f_v, "h_dressed": h, "R_Mpc": R, "D_wall_t0": d_wall,
                "pair_identity_rel_err": pair_identity_check(R),
                "monte_carlo_a15": monte_carlo_boolean(15.0 / h, f_v, R),
                "rows": []}
        for a_h in VOID_RADII_H_MPC:
            a = a_h / h
            s2p = sigma2_partition(R, a, f_v)
            row = {"void_radius_h_inv_Mpc": a_h, "sigma_part": math.sqrt(s2p)}
            for label, comp in (("compressed_fw13", (1 - f_v) ** (1.0 / 3.0)), ("uncompressed", 1.0)):
                s2i = sigma2_internal(R, a, f_v, dens["omega_m_per_photon"], d_wall, comp) * anchor ** 2
                row[f"sigma_int_{label}"] = math.sqrt(s2i)
                for dv in VOID_INTERIOR_CONTRASTS:
                    row[f"sigma_total_{label}_dv{dv:+.1f}"] = math.sqrt(dv * dv * s2p + s2i)
            case["rows"].append(row)
        # Reference: wall-internal field alone in the ball without partition weighting.
        case["sigma_wall_internal_no_partition"] = math.sqrt(
            sigma2_internal(R, 1.0, 1e-300, dens["omega_m_per_photon"], d_wall, 1.0)) * anchor
        results["cases"][name] = case
    payload = {"phase": "1G-E",
               "status": "REPORT_ONLY_AUDIT_EVIDENCE; CONDITIONAL; NOT_OBSERVATIONAL; NOT_SIGMA8",
               "environment": {"python": sys.version.split()[0], "numpy": np.__version__,
                               "scipy": scipy.__version__, "platform": platform.platform()},
               "planck_linear_sigma8_anchor": g1a.PLANCK["sigma8_linear"],
               "results": results}
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {ARTIFACT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
