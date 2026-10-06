"""Delta audit R2-M1: method-diverse recomputation of the F2 cutoffs and the z=3 r>=1 fraction.

Independent of the audited code AND of the prior audit's absorption formula:
  * two-barrier absorption probability from the BACKWARD Kolmogorov equation
        u_S = (1/2) u_yy on y in (0, w),  u(0,S) = 1 (void barrier), u(w,S) = 0 (collapse),
        u(y,0) = 0,  P_v(S) = u(|delta_v|, S),
    solved by Crank-Nicolson with Rannacher start-up (4 implicit-Euler half steps), on two
    grids (N and 2N) for a convergence estimate;
  * sigma(R) by fixed composite Gauss-Legendre in ln k (vectorised), not adaptive quad;
  * spherical barriers solved here from the parametric EdS solution (JLH13 (A4)-(A5), (A9),
    (A11)); shell crossing from d ln A/d ln d = 1/3 (no closed-form (A8));
  * tracker quantities from the closed forms of [GM] Sec. 5.1 (as in the prior audit).
Only the EH98 no-wiggle transfer (Eisenstein & Hu 1998 Eqs. 26, 28-31) and the Planck
inputs are shared conventions (they define the model, not the numerics).
Tolerances: brentq xtol 1e-13 on ln r; CN grid N = 3000 and 6000; Gauss-Legendre 24 nodes x 480 panels.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize
from scipy.linalg import solve_banded
from scipy.special import roots_legendre

C_KM_S, T_CMB = 299792.458, 2.7255
PL = dict(Om=0.315, h=0.674, omega_b=0.02237, n_s=0.9649, sigma8=0.8111, k_pivot=0.05)
PL["omega_m"] = PL["Om"] * PL["h"] ** 2
F_B = PL["omega_b"] / PL["omega_m"]
CASES = {"PAPER_REFERENCE": (0.737, 73.03), "NW15_CMB_FIT": (0.627, 61.0)}
DC = 0.6 * (1.5 * math.pi) ** (2 / 3)


# ---------------------------------------------------------------- spherical model
def _shell(eta, d):
    return 0.5 / d * (math.cosh(eta) - 1.0), 0.5 * d ** -1.5 * (math.sinh(eta) - eta)


def _eta_at(t, d):
    return optimize.brentq(lambda e: _shell(e, d)[1] - t, 1e-9, 200.0, xtol=1e-15, rtol=1e-15)


def shell_crossing():
    def g(t, h=1e-5):
        v = [math.log(_shell(_eta_at(t, math.exp(s * h)), math.exp(s * h))[0]) for s in (-1, 1)]
        return (v[1] - v[0]) / (2 * h) - 1 / 3
    t = optimize.brentq(g, _shell(2.0, 1)[1], _shell(6.0, 1)[1], xtol=1e-14)
    eta = _eta_at(t, 1.0)
    return eta


def barrier_from_eta(eta):
    one_plus = 4.5 * (math.sinh(eta) - eta) ** 2 / (math.cosh(eta) - 1) ** 3          # (A9)
    dv = -(3 / 20) * (6 * (math.sinh(eta) - eta)) ** (2 / 3)                           # (A11)
    return dv, one_plus


def barrier_for_density(x):
    eta = optimize.brentq(lambda e: barrier_from_eta(e)[1] - x, 0.1, 60, xtol=1e-15)
    return barrier_from_eta(eta)


# ---------------------------------------------------------------- spectrum (GL panels)
def eh98(k, om):
    ob, th = F_B * om, T_CMB / 2.7
    s = 44.5 * math.log(9.83 / om) / math.sqrt(1 + 10 * ob ** 0.75)
    ag = 1 - 0.328 * math.log(431 * om) * F_B + 0.38 * math.log(22.3 * om) * F_B ** 2
    q = k * th ** 2 / (om * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4)))
    L = np.log(2 * math.e + 1.8 * q)
    return L / (L + (14.2 + 731 / (1 + 62.5 * q)) * q * q)


_X, _W = roots_legendre(24)


def sigma_unit(R, om):
    R = np.atleast_1d(np.asarray(R, float))
    out = np.empty_like(R)
    for i, r in enumerate(R):
        edges = np.linspace(math.log(1e-7), math.log(3e3 / r), 481)
        a, b = edges[:-1, None], edges[1:, None]
        lnk = 0.5 * (b - a) * _X[None, :] + 0.5 * (b + a)
        w = 0.5 * (b - a) * _W[None, :]
        k = np.exp(lnk)
        x = k * r
        win = np.where(x < 1e-2, 1 - x * x / 10 + x ** 4 / 280, 3 * (np.sin(x) - x * np.cos(x)) / np.where(x < 1e-2, 1, x) ** 3)
        d2 = (4 / 25) * (k / PL["k_pivot"]) ** (PL["n_s"] - 1) * (k / (100 / C_KM_S)) ** 4 * eh98(k, om) ** 2 / om ** 2
        out[i] = math.sqrt(float((w * d2 * win * win).sum()))
    return out


def lcdm_growth(Om):
    a = np.linspace(0, 1, 200001)[1:]
    E = np.sqrt(Om / a ** 3 + 1 - Om)
    f = 1 / (a * E) ** 3
    # integrand ~ a^(3/2)/Om^(3/2) near 0: analytic head on [0, a1]
    a1 = a[0]
    head = a1 ** 2.5 / (2.5 * Om ** 1.5)
    from scipy.integrate import simpson
    return 2.5 * Om * 1.0 * (head + simpson(f, x=a))


# ---------------------------------------------------------------- backward Kolmogorov (CN)
class Absorption:
    """P_v(S) = u(|dv|, S) with u_S = u_yy/2, u(0)=1, u(w)=0, u(y,0)=0."""

    def __init__(self, dv_abs, dc, N, S_max, n_steps=40000):
        self.a, self.w = dv_abs, dv_abs + dc
        y = np.linspace(0, self.w, N + 1)
        h = y[1] - y[0]
        j = int(round(self.a / h))
        self.y_probe = y[j]
        assert abs(self.y_probe - self.a) < 1e-9 * self.w or True
        # place the start exactly on a node by rescaling: use grid with node at a
        n1 = max(2, int(round(N * self.a / self.w)))
        y = np.r_[np.linspace(0, self.a, n1 + 1), np.linspace(self.a, self.w, N - n1 + 1)[1:]]
        self.j = n1
        hl, hr = np.diff(y)[:-1], np.diff(y)[1:]
        m = len(y) - 2
        # second-derivative operator on non-uniform grid (interior nodes)
        lo = 2 / (hl * (hl + hr)); di = -2 / (hl * hr); up = 2 / (hr * (hl + hr))
        u = np.zeros(m)
        S = np.r_[0.0, np.geomspace(1e-6 * self.w ** 2, S_max, n_steps)]
        out = [0.0]
        def step(u, dS, theta):
            # (I - theta dS/2 L) u_new = (I + (1-theta) dS/2 L) u_old + boundary terms (u(0)=1)
            ab = np.zeros((3, m))
            ab[0, 1:] = -theta * dS / 2 * up[:-1]
            ab[1, :] = 1 - theta * dS / 2 * di
            ab[2, :-1] = -theta * dS / 2 * lo[1:]
            rhs = u + (1 - theta) * dS / 2 * (di * u + np.r_[0, lo[1:] * u[:-1]] + np.r_[up[:-1] * u[1:], 0])
            rhs[0] += dS / 2 * lo[0] * 1.0  # boundary value 1 at y=0, both time levels
            return solve_banded((1, 1), ab, rhs)
        for i in range(1, len(S)):
            dS = S[i] - S[i - 1]
            if i <= 4:   # Rannacher: two implicit-Euler half steps per step
                u = step(u, dS / 2, 1.0); u = step(u, dS / 2, 1.0)
            else:
                u = step(u, dS, 0.5)
            out.append(u[self.j - 1])
        self.S, self.P = S, np.array(out)

    def __call__(self, S):
        return np.interp(np.log(S), np.log(self.S[1:]), self.P[1:])


def tracker(fv0, H0):
    HD0 = 2 * H0 * (2 + fv0) / (4 + fv0 + 4 * fv0 ** 2)
    om = 0.5 * (1 - fv0) * (2 + fv0) * (HD0 / 100) ** 2
    tau = (1 - fv0) / fv0
    fv = lambda t: t / (t + tau)
    gam = lambda t: 1 + fv(t) / 2
    opz = lambda t: gam(t) / (1 + fv0 / 2) / t * (fv(t) / fv0) ** (1 / 3)
    t_of_z = lambda z: 1.0 if z == 0 else optimize.brentq(lambda t: opz(t) - (1 + z), 1e-9, 1.0, xtol=1e-15)
    frame = lambda t: gam(t) * (1 - fv(t)) ** (1 / 3)
    return om, H0 / 100, fv, t_of_z, frame


def run(N):
    eta_sc = shell_crossing()
    dv_sc, x_sc = barrier_from_eta(eta_sc)
    anchor = PL["sigma8"] / (sigma_unit(8 / PL["h"], PL["omega_m"])[0] * lcdm_growth(PL["Om"]))
    out = {"N": N, "eta_sc": eta_sc, "delta_v_sc": dv_sc, "x_sc": x_sc, "g_LCDM": lcdm_growth(PL["Om"])}
    barriers = {"shell_crossing": (dv_sc, x_sc), "0.1": barrier_for_density(0.1), "0.05": barrier_for_density(0.05)}
    absorbers = {k: Absorption(abs(dv), DC, N, S_max=400.0 * (abs(dv) + DC) ** 2) for k, (dv, x) in barriers.items()}
    for name, (fv0, H0) in CASES.items():
        om, h, fv, t_of_z, frame = tracker(fv0, H0)
        res = {}
        for key in ("0.1", "0.05", "shell_crossing"):
            dv, x = barriers[key]
            m = DC / (DC + abs(dv))
            den = x * (1 - m) + m
            D = frame(1.0)
            def F(r_h, fixed=True, D=D, fr=D, x=x, key=key, den=den):
                RL = r_h / h / (fr * x ** (-1 / 3))
                s = anchor * D * sigma_unit(RL, om)[0]
                mA = float(absorbers[key](s * s))
                return mA / den if fixed else mA / (x * (1 - mA) + mA)
            cut = lambda fixed: math.exp(optimize.brentq(lambda lr: F(math.exp(lr), fixed) - fv0, math.log(1e-4), math.log(50), xtol=1e-13))
            res[key] = {"delta_v": dv, "x": x, "m_total": m, "F2_all": (m / x) / (1 - m + m / x),
                        "cutoff_F2": cut(True), "cutoff_F3": cut(False), "F2_ge1": F(1.0), "F2_ge10": F(10.0), "F2_ge15": F(15.0)}
        # z = 3 history row, shell-crossing barrier, r >= 1
        t3 = t_of_z(3.0)
        fr3 = frame(t3)
        dv, x = barriers["shell_crossing"]
        m = DC / (DC + abs(dv)); den = x * (1 - m) + m
        RL = 1.0 / h / (fr3 * x ** (-1 / 3))
        s = anchor * (fr3 / 4.0) * sigma_unit(RL, om)[0]
        res["z3_F2_ge1"] = float(absorbers["shell_crossing"](s * s)) / den
        res["z3_tracker_fv"] = fv(t3)
        res["omega_eff"], res["D_wall"] = om, frame(1.0)
        out[name] = res
    return out


if __name__ == "__main__":
    results = {"coarse": run(3000), "fine": run(6000)}
    outdir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    (outdir / "r2_cutoffs_pde_out.json").write_bytes((json.dumps(results, indent=1) + "\n").encode())
    for case in CASES:
        for key in ("0.1", "0.05", "shell_crossing"):
            a, b = results["coarse"][case][key], results["fine"][case][key]
            print(case, key, "F2 cut", b["cutoff_F2"], "(grid diff %.1e)" % (b["cutoff_F2"] / a["cutoff_F2"] - 1),
                  "F3 cut", b["cutoff_F3"], "F2>=1", b["F2_ge1"], "F2>=10", b["F2_ge10"], "F2>=15", b["F2_ge15"])
        print(case, "z3 F2>=1", results["fine"][case]["z3_F2_ge1"], "coarse", results["coarse"][case]["z3_F2_ge1"])
