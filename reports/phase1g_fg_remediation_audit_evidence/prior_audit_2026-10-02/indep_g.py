"""Auditor's independent checks of G1-G12 (no project imports).

Exact-rational identity checks (fractions.Fraction) replace a CAS (sympy is not installed in
any available interpreter; no dependency was added).  Kinetic counterexamples integrate the
discrete Smoluchowski equation [L03] (2.2) directly.
"""
import json
import math
import sys
from fractions import Fraction as Fr

import numpy as np
from scipy.integrate import solve_ivp

RTOL, ATOL = 1e-10, 1e-13      # explicit ODE controls
out = {}

# ---------------------------------------------------------------- F1-F3 exact identities
def F2(mA, m, x):
    return mA / (x * (1 - m) + m)


def F3(mA, x):
    return mA / (x * (1 - mA) + mA)


chk = []
for m, x, a, b in [(Fr(2, 10), Fr(2, 10), Fr(1, 10), Fr(1, 10)), (Fr(383, 1000), Fr(2047, 10000), Fr(7, 1000), Fr(31, 100)),
                   (Fr(1, 3), Fr(1, 7), Fr(1, 9), Fr(2, 9))]:
    # direct accounting: mass M=1, wall density 1 -> V_w = 1-m, V_A = a/x, V_B = b/x, V_rest = (m-a-b)/x
    V = (1 - m) + m / x
    chk.append(dict(additive=F2(a, m, x) + F2(b, m, x) == F2(a + b, m, x),
                    direct=F2(a, m, x) == (a / x) / V,
                    F3_not_additive=F3(a, x) + F3(b, x) != F3(a + b, x),
                    F3_ge_F2=F3(a, x) >= F2(a, m, x),
                    partition=(1 - m) / V + F2(m, m, x) == 1))
out["F1_F3_exact"] = chk
out["F3_example_5_7_vs_5_9"] = [str(F3(Fr(1, 10), Fr(1, 5)) * 2), str(F2(Fr(2, 10), Fr(2, 10), Fr(1, 5)))]

# ---------------------------------------------------------------- G3-G5 exact identities
g = []
for t, tau in [(Fr(1, 3), Fr(5, 7)), (Fr(2), Fr(3, 11)), (Fr(9, 4), Fr(9, 4))]:
    f = t / (t + tau)
    fdot_exact = tau / (t + tau) ** 2          # d/dt [t/(t+tau)]
    Hv, Hw = 1 / t, Fr(2, 3) / t
    g.append(dict(G3=fdot_exact == 3 * f * (1 - f) * (Hv - Hw),
                  G4=(lambda fref, tref: fref * (t / tref) / (1 - fref + fref * (t / tref)) == f)(Fr(1, 2), tau)))
out["G3_G4_exact"] = g
# G5: volume ODE with transfer, finite differences on exact solution of linear system
def g5_check(fv, Hv, Hw, JV):
    V = 1.0
    Vv, Vw = fv * V, (1 - fv) * V
    dVv, dVw = 3 * Hv * Vv + JV * V, 3 * Hw * Vw - JV * V
    dV = dVv + dVw
    fdot = dVv / V - Vv * dV / V ** 2
    return fdot - (3 * fv * (1 - fv) * (Hv - Hw) + JV)
out["G5_residual"] = max(abs(g5_check(*a)) for a in [(0.737, 0.9, 0.6, 0.01), (0.2, 1.3, 0.2, -0.3)])

# ---------------------------------------------------------------- G6 and cohort ageing
def g_vel(eta):
    return math.sinh(eta) * (math.sinh(eta) - eta) / (math.cosh(eta) - 1) ** 2


def eta_of_density(xr):
    from scipy.optimize import brentq
    return brentq(lambda e: 4.5 * (math.sinh(e) - e) ** 2 / (math.cosh(e) - 1) ** 3 - xr, 0.1, 60, xtol=1e-15)


eta_sc = eta_of_density(0.2047223340049)
ages = {}
for ratio in (1.0, 1.5, 2.0, 4.0, 10.0):
    # cohort crossing at t_sc: t ~ sinh(eta)-eta at fixed amplitude
    from scipy.optimize import brentq
    tsc = math.sinh(eta_sc) - eta_sc
    e = brentq(lambda e: (math.sinh(e) - e) - ratio * tsc, eta_sc * 0.5, 200)
    ages[f"t/t_sc={ratio:g}"] = dict(Hv_t=g_vel(e), J_required_over_tracker_rate=1 - (3 * g_vel(e) - 2))
out["cohort_ageing"] = ages
out["Hv_t_near_empty"] = {f"x={xr}": g_vel(eta_of_density(xr)) for xr in (0.1, 0.05)}
for name, fv in (("GM", Fr(737, 1000)), ("NW15", Fr(627, 1000))):
    out[f"G6_tJ_over_V_{name}"] = float(fv * (1 - fv) / 3)
# F population's own all-size history: f const (0.7519694) -> J/V*t needed relative to shell-crossing interiors
fF = 0.7519694338440862
out["F_all_size_history_implied_tJ_over_V"] = -(3 * (8 / 9 - 2 / 3)) * fF * (1 - fF)
out["F_all_size_history_effective_Hv_minus_Hw"] = 0.0

# ---------------------------------------------------------------- G7-G9 exact
x = Fr(2047223340049, 10 ** 13)
g7 = {}
for name, fv in (("GM", Fr(737, 1000)), ("NW15", Fr(627, 1000))):
    m = fv * x / (1 - fv + fv * x)
    back = (m / x) / (1 - m + m / x)
    g7[name] = dict(m=float(m), inverse_ok=back == fv)
out["G7"] = g7
t, tau, m = Fr(3, 5), Fr(7, 13), Fr(1, 4)
f = t / (t + tau)
x9 = m * (1 - f) / ((1 - m) * f)
out["G9_exact"] = x9 == (m / (1 - m)) * tau / t
out["G9_x_le_1_requires_t_ge"] = "tau*m/(1-m)"

# ---------------------------------------------------------------- G10-G11 exact
def tail_exact(u, kmin, kmax):
    beta = Fr(u) / (1 + Fr(u))
    s = sum(k * beta ** (k - 1) for k in range(kmin, kmax + 1)) * (1 - beta) ** 2
    rem = beta ** kmax * (1 + kmax * (1 - beta))      # exact remainder sum_{k>kmax}
    return s + rem


def tail_formula(u, kmin):
    beta = Fr(u) / (1 + Fr(u))
    return beta ** (kmin - 1) * (1 + (kmin - 1) * (1 - beta))


out["G11_exact"] = {f"u={u}": dict(equal=tail_exact(u, 125, 900) == tail_formula(u, 125), value=float(tail_formula(u, 125)))
                    for u in (1, 10, 100)}
out["G10_table"] = {f"u={u}": dict(N_over_N0=1 / (1 + u), radius_at_mean_volume=(1 + u) ** (1 / 3)) for u in (0, 1, 10, 100)}


# ---------------------------------------------------------------- kinetic counterexamples
def smoluchowski(kernel, size, t_end, n_out=9):
    k = np.arange(1, size + 1, dtype=float)
    Kmat = kernel(k[:, None], k[None, :])

    def rhs(t, c):
        gain = np.zeros(size)
        # gain_k = 1/2 sum_{i+j=k} K_ij c_i c_j
        for kk in range(2, size + 1):
            i = np.arange(1, kk)
            gain[kk - 1] = 0.5 * np.sum(Kmat[i - 1, kk - i - 1] * c[i - 1] * c[kk - i - 1])
        loss = c * (Kmat @ c)
        return gain - loss

    c0 = np.zeros(size)
    c0[0] = 1.0
    ts = np.linspace(0, t_end, n_out)
    sol = solve_ivp(rhs, (0, t_end), c0, t_eval=ts, method="LSODA", rtol=RTOL, atol=ATOL)
    return [(float(t), float((k * c).sum())) for t, c in zip(sol.t, sol.y.T)]


out["kinetic_Q1_constant_K"] = smoluchowski(lambda a, b: np.ones_like(a * b), 120, 2.0)
out["kinetic_Q1_additive_K"] = smoluchowski(lambda a, b: a + b, 120, 1.0)
out["kinetic_Q1_product_K_gelling"] = smoluchowski(lambda a, b: a * b, 120, 2.0)
print(json.dumps(out, indent=1, default=str))
with open(sys.argv[1], "wb") as fh:
    fh.write((json.dumps(out, indent=1, default=str) + "\n").encode())
