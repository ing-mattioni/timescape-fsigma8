"""Delta audit R2-M4: product kernel K=ij, monodisperse c_1(0)=1 ([L03] Sec. 4.5).

Checks the remediation erratum: sol mass 1/t is the Stockmayer solution ([L03] (4.77));
the Flory solution ([L03] (4.74)-(4.76)) has M1 = exp(-zeta), zeta/(1-exp(-zeta)) = t,
equivalently q = exp[-t(1-q)].  Also shows what a finite truncation does near t_gel = 1.
Truncated kinetics (own code): gain_k = 1/2 sum_{i+j=k} (i c_i)(j c_j);
  Stockmayer-type loss: k c_k * sum_{j<=N} j c_j (clusters beyond N are an inert gel);
  Flory-type loss:      k c_k * 1 (sol also reacts with the gel; total mass fixed by fiat).
ODE: LSODA rtol 1e-10, atol 1e-14.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import gammaln

TIMES = (0.5, 1.0, 1.5, 2.0, 3.0)


def flory_q(t):
    if t <= 1:
        return 1.0
    return brentq(lambda q: q - math.exp(-t * (1 - q)), 1e-12, 1 - 1e-12, xtol=1e-15)


def flory_zeta(t):
    if t <= 1:
        return 0.0
    z = brentq(lambda z: z / (1 - math.exp(-z)) - t, 1e-12, 50, xtol=1e-15)
    return math.exp(-z)


def stockmayer_closed(t, J=200000):
    """sum_j j c_j with (4.77) for t >= 1; c_j = j^(j-3) e^-j / (j-1)! / t; plus tail ~ j^-3/2."""
    j = np.arange(1, J + 1, dtype=float)
    log_c = (j - 3) * np.log(j) - j - gammaln(j)
    s = float(np.sum(j * np.exp(log_c)))
    tail = 2.0 / math.sqrt(2 * math.pi * J)   # sum_{j>J} j^{-3/2}/sqrt(2 pi)
    return (s + tail) / t


def truncated(N, model, times=TIMES):
    k = np.arange(1, N + 1, dtype=float)

    def rhs(t, c):
        jc = k * c
        conv = np.convolve(jc, jc)[: N - 1]          # index i -> cluster size i+2
        gain = np.r_[0.0, 0.5 * conv]
        mass = jc.sum() if model == "stockmayer" else 1.0
        return gain - k * c * mass

    c0 = np.zeros(N); c0[0] = 1.0
    sol = solve_ivp(rhs, (0, max(times)), c0, t_eval=times, method="LSODA", rtol=1e-10, atol=1e-14)
    return {f"{t:g}": float((k * y).sum()) for t, y in zip(sol.t, sol.y.T)}


out = {"flory_q": {f"{t:g}": flory_q(t) for t in TIMES},
       "flory_via_L03_4_76": {f"{t:g}": flory_zeta(t) for t in TIMES},
       "stockmayer_closed_4_77": {f"{t:g}": (stockmayer_closed(t) if t >= 1 else None) for t in TIMES},
       "stockmayer_exact_1_over_t": {f"{t:g}": (1 / t if t >= 1 else 1.0) for t in TIMES},
       "truncated_stockmayer": {}, "truncated_flory": {}}
for N in (60, 120, 240, 480, 960):
    out["truncated_stockmayer"][N] = truncated(N, "stockmayer")
    out["truncated_flory"][N] = truncated(N, "flory")
out["prior_audit_value_N120_t1"] = 0.9530986737238387
Path(sys.argv[1]).write_bytes((json.dumps(out, indent=1) + "\n").encode())
print("Flory q:", out["flory_q"]); print("Flory via (4.76):", out["flory_via_L03_4_76"])
print("Stockmayer (4.77) closed:", out["stockmayer_closed_4_77"])
for N in out["truncated_stockmayer"]:
    print("N", N, "stockmayer-type", {t: round(v, 6) for t, v in out["truncated_stockmayer"][N].items()},
          "flory-type", {t: round(v, 6) for t, v in out["truncated_flory"][N].items()})
