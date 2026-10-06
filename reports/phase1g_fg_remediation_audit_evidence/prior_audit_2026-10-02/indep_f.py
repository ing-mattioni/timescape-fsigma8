"""Independent re-computation for the 1G-F successor audit (auditor's code, not the audited code).

Nothing is imported from the project (no timescape_fsigma8, no scripts/).  Inputs are
the published constants only:
  * tracker closed forms, [GM] arXiv:2511.17160v2 Sec. 5.1 text and Eqs. (5.5)-(5.6):
      f_v(t) = t/(t+tau), tau = t0 (1-f_v0)/f_v0, gamma_w = 1 + f_v/2,
      H_D0 = 2 H0 (2+f_v0)/(4+f_v0+4 f_v0^2), <rho>_0 = 12 H_D0^2 (1-f_v0)/[8 pi G (2+f_v0)^2],
      1+z = a_w0/a_w with a_w = a_D/gamma_w and a_D from (5.5);
  * Planck 2018 inputs as recorded by 1G-A (Om=0.315, h=0.674, omega_b=0.02237, n_s=0.9649,
    sigma8=0.8111); A_s cancels in the anchor ratio;
  * EH98 no-wiggle transfer (Eisenstein & Hu 1998, Eqs. 26, 28-31), re-typed;
  * JLH13 shell-crossing: re-derived numerically from Lagrangian shells (dr/dR_i = 0),
    not from the closed-form condition (A8).
The two-barrier absorption probability is derived here from the eigenfunction
solution of the diffusion equation on (delta_v, delta_c) with absorbing ends:
  P_v(S) = (1-D) - sum_j (2/(j pi)) sin(j pi D) exp(-j^2 pi^2 S/(2 w^2)),  w = dc+|dv|,
cross-checked against an image (erfc) form.  Cumulatives are closed forms (no grid
quadrature of f_lnsigma), so the 481-node trapezoid of the audited code is also tested.
"""
from __future__ import annotations

import json
import math
import sys

import numpy as np
from scipy import integrate, optimize, special

# ----------------------------------------------------------------- tolerances (explicit)
QUAD_EPSREL = 1e-10
ROOT_XTOL = 1e-14
SERIES_J = 4000          # Fourier terms for P_v (large-S side)
IMAGE_N = 60             # image terms for P_v (small-S side)

C_KM_S = 299792.458
T_CMB = 2.7255
PL = dict(Om=0.315, h=0.674, omega_b=0.02237, n_s=0.9649, sigma8=0.8111, k_pivot=0.05)
PL["omega_m"] = PL["Om"] * PL["h"] ** 2
F_B = PL["omega_b"] / PL["omega_m"]
CASES = {"PAPER_REFERENCE": dict(fv0=0.737, H0=73.03), "NW15_CMB_FIT": dict(fv0=0.627, H0=61.0)}


# ------------------------------------------------------------------ spherical void model
def shell(eta, d):
    """Parametric EdS underdense shell (JLH13 A4-A5), d = |5 Delta_i/3|, H_i = 1, R_i = 1."""
    R = 0.5 / d * (math.cosh(eta) - 1.0)
    t = 0.5 * d ** -1.5 * (math.sinh(eta) - eta)
    return R, t


def eta_at_time(t, d):
    return optimize.brentq(lambda e: shell(e, d)[1] - t, 1e-9, 200.0, xtol=1e-15, rtol=1e-15)


def shell_crossing_independent():
    """Find eta at which an exterior shell just outside the tophat edge catches the edge.

    Exterior Delta_i(R_i) = d0 (R0/R_i)^3.  r(R_i, t) = R_i * A(d(R_i), t).  First crossing
    at the edge when d ln A / d ln d = 1/3 at d = d0 (fixed t).  Evaluated by central
    differences in ln d of the *parametric* solution, root-found in t.
    """
    d0 = 1.0

    def dlnA_dlnd(t, h=1e-5):
        vals = []
        for s in (-1, 1):
            d = d0 * math.exp(s * h)
            vals.append(math.log(shell(eta_at_time(t, d), d)[0]))
        return (vals[1] - vals[0]) / (2 * h)

    # bracket in time using the boundary shell's eta
    t_lo, t_hi = shell(2.0, d0)[1], shell(6.0, d0)[1]
    t_sc = optimize.brentq(lambda t: dlnA_dlnd(t) - 1.0 / 3.0, t_lo, t_hi, xtol=1e-13)
    eta = eta_at_time(t_sc, d0)
    one_plus = 4.5 * (math.sinh(eta) - eta) ** 2 / (math.cosh(eta) - 1.0) ** 3
    # density by direct volume accounting: R/R_i relative to background a/a_i = (3t/2)^(2/3)
    R, t = shell(eta, d0)
    a_bg = (1.5 * t) ** (2.0 / 3.0)          # EdS background, same leading order: a/a_i = (3 H_i t/2)^(2/3)
    one_plus_direct = (a_bg / R) ** 3        # enclosed mass fixed: density ratio = (a_bg/R)^3 at leading order
    delta_lin = -(3.0 / 20.0) * (6.0 * (math.sinh(eta) - eta)) ** (2.0 / 3.0)
    # interior Hubble rate times t by finite difference of ln R vs ln t
    he = 1e-6
    (R1, t1), (R2, t2) = shell(eta - he, d0), shell(eta + he, d0)
    hv_t = (math.log(R2) - math.log(R1)) / (math.log(t2) - math.log(t1))
    return dict(eta_sc=eta, one_plus_delta_sc=one_plus, one_plus_delta_direct_leading_order=one_plus_direct,
                delta_v=delta_lin, r_nl_over_r_l=one_plus ** (-1.0 / 3.0), Hv_t=hv_t,
                closed_form_A8_residual=math.sinh(eta) * (math.sinh(eta) - eta) / (math.cosh(eta) - 1) ** 2 - 8 / 9)


# ---------------------------------------------------------------- two-barrier absorption
def P_void_fourier(S, dv_abs, dc, J=SERIES_J):
    w = dc + dv_abs
    D = dv_abs / w
    j = np.arange(1, J + 1, dtype=float)
    S = np.atleast_1d(np.asarray(S, dtype=float))[:, None]
    tail = (2.0 / (j * math.pi)) * np.sin(j * math.pi * D) * np.exp(-(j * math.pi) ** 2 * S / (2 * w * w))
    return (1.0 - D) - tail.sum(axis=1)


def P_void_images(S, dv_abs, dc, N=IMAGE_N):
    w = dc + dv_abs
    S = np.atleast_1d(np.asarray(S, dtype=float))[:, None]
    n = np.arange(N, dtype=float)
    a1 = (dv_abs + 2 * n * w) / np.sqrt(2 * S)
    a2 = (dv_abs + 2 * dc + 2 * n * w) / np.sqrt(2 * S)
    return (special.erfc(a1) - special.erfc(a2)).sum(axis=1)


def P_void(S, dv_abs, dc):
    S = np.atleast_1d(np.asarray(S, dtype=float))
    w = dc + dv_abs
    small = S < 0.5 * w * w
    out = np.empty_like(S)
    if small.any():
        out[small] = P_void_images(S[small], dv_abs, dc)
    if (~small).any():
        out[~small] = P_void_fourier(S[~small], dv_abs, dc)
    return out


# --------------------------------------------------------------------- linear spectrum
def eh98_nowiggle(k, omega_m, f_b):
    """Eisenstein & Hu 1998 ApJ 496, 605: Eq. (26) s, (31) alpha_Gamma, (30) Gamma_eff, (28) q, (29) L0,C0."""
    omega_b = f_b * omega_m
    th = T_CMB / 2.7
    s = 44.5 * math.log(9.83 / omega_m) / math.sqrt(1 + 10 * omega_b ** 0.75)
    ag = 1 - 0.328 * math.log(431 * omega_m) * f_b + 0.38 * math.log(22.3 * omega_m) * f_b ** 2
    geff = omega_m * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))  # Omega_m h * Gamma_eff/(Omega_m h) -> in h units * h
    q = k * th ** 2 / geff
    L0 = np.log(2 * math.e + 1.8 * q)
    C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)


def W_tophat(x):
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    sm = np.abs(x) < 1e-2
    xs = x[~sm]
    out[~sm] = 3 * (np.sin(xs) - xs * np.cos(xs)) / xs ** 3
    xx = x[sm] ** 2
    out[sm] = 1 - xx / 10 + xx * xx / 280 - xx ** 3 / 15120
    return out


def delta2_unit(k, omega_m):
    """Matter-era Delta^2(k) per unit growth, A_s set to 1 (cancels in the anchor)."""
    h100 = 100.0 / C_KM_S
    return (4 / 25) * (k / PL["k_pivot"]) ** (PL["n_s"] - 1) * (k / h100) ** 4 * eh98_nowiggle(k, omega_m, F_B) ** 2 / omega_m ** 2


def sigma_unit(R, omega_m):
    """sigma(R) per unit growth and unit A_s; Gauss-Kronrod in ln k on fixed decades."""
    f = lambda lnk: float(delta2_unit(np.exp([lnk]), omega_m)[0] * W_tophat(np.exp([lnk]) * R)[0] ** 2)
    lo, hi = math.log(1e-7), math.log(2e3 / R)
    edges = np.linspace(lo, hi, 60)
    tot = 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        tot += integrate.quad(f, a, b, epsabs=0.0, epsrel=QUAD_EPSREL, limit=200)[0]
    return math.sqrt(tot)


def lcdm_growth_today(Om):
    """D(a=1) for flat LCDM, D/a -> 1 early: D = (5 Om/2) E(a) int_0^a da'/(a' E)^3."""
    OL = 1 - Om
    E = lambda a: math.sqrt(Om / a ** 3 + OL)
    I = integrate.quad(lambda a: 1.0 / (a * E(a)) ** 3, 0.0, 1.0, epsabs=0.0, epsrel=1e-13, limit=400)[0]
    return 2.5 * Om * E(1.0) * I


# --------------------------------------------------------------------------- tracker
def tracker(fv0, H0):
    HD0 = 2 * H0 * (2 + fv0) / (4 + fv0 + 4 * fv0 ** 2)
    omega_eff = 0.5 * (1 - fv0) * (2 + fv0) * (HD0 / 100) ** 2
    t0 = 1.0
    tau = t0 * (1 - fv0) / fv0
    fv = lambda t: t / (t + tau)
    gam = lambda t: 1 + fv(t) / 2
    gam0 = 1 + fv0 / 2

    def one_plus_z(t):
        # 1+z = a_w0/a_w, a_w = a_D/gamma_w, a_D/a_D0 = (t/t0) (fv0/fv)^(1/3) using H_D0 t0 = (2+fv0)/3
        return (gam(t) / gam0) * (t0 / t) * (fv(t) / fv0) ** (1 / 3)

    def t_of_z(z):
        if z == 0:
            return t0
        return optimize.brentq(lambda t: one_plus_z(t) - (1 + z), 1e-9, t0, xtol=1e-15, rtol=1e-15)

    def frame(t):
        return gam(t) * (1 - fv(t)) ** (1 / 3)

    return dict(HD0=HD0, omega_eff=omega_eff, h=H0 / 100, fv=fv, t_of_z=t_of_z, frame=frame,
                HD0_t0_check=(2 + fv0) / 3)


# ------------------------------------------------------------------------ population
class Population:
    def __init__(self, omega_eff, anchor, D, frame, h, dv_abs, dc, x):
        self.omega, self.anchor, self.D, self.frame, self.h = omega_eff, anchor, D, frame, h
        self.dv, self.dc, self.x = dv_abs, dc, x
        self.m_total = dc / (dc + dv_abs)
        self.denom_F2 = x * (1 - self.m_total) + self.m_total
        self._cache = {}

    def R_L_of_r(self, r_h):
        """Lagrangian radius (photon comoving Mpc) for Eulerian radius r in h^-1 Mpc."""
        return r_h / self.h / (self.frame * self.x ** (-1 / 3))

    def sigma(self, R_L):
        key = round(math.log(R_L), 12)
        if key not in self._cache:
            self._cache[key] = self.anchor * sigma_unit(R_L, self.omega) * self.D
        return self._cache[key]

    def mass_above(self, r_h):
        s = self.sigma(self.R_L_of_r(r_h))
        return float(P_void(s * s, self.dv, self.dc)[0])

    def F2(self, r_h):
        return self.mass_above(r_h) / self.denom_F2

    def F3(self, r_h):
        m = self.mass_above(r_h)
        return m / (self.x * (1 - m) + m)

    def median(self):
        g = lambda lnr: self.mass_above(math.exp(lnr)) - 0.5 * self.m_total
        return math.exp(optimize.brentq(g, math.log(1e-4), math.log(1e3), xtol=1e-10))

    def cutoff(self, target, fixed_domain=True):
        fn = self.F2 if fixed_domain else self.F3
        g = lambda lnr: fn(math.exp(lnr)) - target
        lo, hi = math.log(1e-4), math.log(1e3)
        if g(lo) < 0 or g(hi) > 0:
            return None
        return math.exp(optimize.brentq(g, lo, hi, xtol=1e-10))


def main():
    out = {"python": sys.version.split()[0], "numpy": np.__version__}
    sc = shell_crossing_independent()
    out["shell_crossing_independent"] = sc
    dv_abs, x = abs(sc["delta_v"]), sc["one_plus_delta_sc"]
    dc = 0.6 * (1.5 * math.pi) ** (2 / 3)
    out["delta_c"] = dc
    # series cross-check
    w = dv_abs + dc
    Sgrid = (np.geomspace(0.05, 20, 200) * w) ** 2
    out["P_void_images_vs_fourier_max_abs"] = float(np.max(np.abs(P_void_images(Sgrid, dv_abs, dc, 200) - P_void_fourier(Sgrid, dv_abs, dc, 20000))))
    m = dc / (dc + dv_abs)
    Z = 1 - m + m / x
    out["m_total"], out["Z"], out["Fv_all"] = m, Z, (m / x) / Z
    gL = lcdm_growth_today(PL["Om"])
    sig8_unit = sigma_unit(8 / PL["h"], PL["omega_m"])
    anchor = PL["sigma8"] / (sig8_unit * gL)
    out["g_LCDM"], out["anchor_per_unit_As"] = gL, anchor
    res = {}
    for name, c in CASES.items():
        tr = tracker(c["fv0"], c["H0"])
        rows = []
        for z in (0.0, 0.5, 1.0, 2.0, 3.0):
            t = tr["t_of_z"](z)
            fr = tr["frame"](t)
            D = fr / (1 + z)
            pop = Population(tr["omega_eff"], anchor, D, fr, tr["h"], dv_abs, dc, x)
            row = dict(z=z, t_over_t0=t, fv=tr["fv"](t), frame=fr, D=D)
            row["F2"] = {f"r>={r:g}": pop.F2(r) for r in (1, 2, 5, 10, 15)}
            row["F3"] = {f"r>={r:g}": pop.F3(r) for r in (1, 2, 5, 10, 15)}
            row["median_h_inv_Mpc"] = pop.median()
            row["cutoff_F2"] = pop.cutoff(tr["fv"](t), True)
            row["cutoff_F3"] = pop.cutoff(tr["fv"](t), False)
            rows.append(row)
        # fixed-cutoff test: hold the z=0 F2 cutoff and evaluate at every epoch
        rc = rows[0]["cutoff_F2"]
        fixed = []
        for row in rows:
            t = row["t_over_t0"]
            pop = Population(tr["omega_eff"], anchor, row["D"], row["frame"], tr["h"], dv_abs, dc, x)
            fixed.append(dict(z=row["z"], tracker=row["fv"], F2_at_z0_cutoff=pop.F2(rc)))
        res[name] = dict(omega_eff=tr["omega_eff"], HD0=tr["HD0"], h=tr["h"], history=rows,
                         fixed_z0_cutoff=rc, fixed_cutoff_track=fixed)
    out["cases"] = res
    return out


if __name__ == "__main__":
    result = main()
    path = sys.argv[1] if len(sys.argv) > 1 else "indep_f_out.json"
    with open(path, "wb") as fh:
        fh.write((json.dumps(result, indent=1, default=float) + "\n").encode())
    print(json.dumps({k: result[k] for k in ("shell_crossing_independent", "m_total", "Z", "Fv_all", "anchor_per_unit_As", "g_LCDM", "P_void_images_vs_fourier_max_abs")}, indent=1))
    for name, c in result["cases"].items():
        r0 = c["history"][0]
        print(name, "omega_eff", c["omega_eff"], "F2>=10", r0["F2"]["r>=10"], "F3>=10", r0["F3"]["r>=10"], "median", r0["median_h_inv_Mpc"])
        for row in c["history"]:
            print("  z", row["z"], "fv", round(row["fv"], 6), "cutF2", row["cutoff_F2"], "cutF3", row["cutoff_F3"], "F2", {k: round(v, 6) for k, v in row["F2"].items()})
        print("  fixed z0 cutoff", c["fixed_z0_cutoff"], [(f["z"], round(f["tracker"], 4), round(f["F2_at_z0_cutoff"], 4)) for f in c["fixed_cutoff_track"]])
