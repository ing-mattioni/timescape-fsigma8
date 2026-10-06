"""Delta audit R2-M5: probe the remediation's Lagrangian shell-crossing test (re-implemented here).

The audited test (tests/test_phase1g_g_void_evolution.py) uses r = R_i^4 (cosh eta - 1),
t = R_i^(9/2) (sinh eta - eta) for an exterior profile Delta_i ~ R_i^-3, finds dr/dR_i = 0 at
fixed t by central differences in R_i, then measures H t = d ln r / d ln t.
Probes:
 (1) convergence in the label step h and the time step, and label independence (self-similarity);
 (2) non-circularity: for an exterior profile Delta_i ~ R_i^-p, the same algorithm must return
     H t = 2(1+p)/(3p) (derived here by hand from (A4)-(A5)); p = 3 gives 8/9, p = 4 gives 5/6,
     p = 6 gives 7/9.  A procedure that imposed 8/9 could not pass p != 3.
Root tolerances as in the audited test (xtol 5e-14).
"""
import json
import math
import sys
from pathlib import Path

from scipy.optimize import brentq


def make(p):
    a, b = 1.0 + p, 1.5 * p

    def radius(label, time):
        eta = brentq(lambda e: math.sinh(e) - e - time / label ** b, 1e-6, 40.0, xtol=5e-14)
        return label ** a * (math.cosh(eta) - 1.0)

    def ht_at_crossing(label, step, dt_rel=1e-5):
        def jac(eta):
            time = label ** b * (math.sinh(eta) - eta)
            return (radius(label + step, time) - radius(label - step, time)) / (2 * step)
        eta = brentq(jac, 0.5, 30.0, xtol=5e-14)
        time = label ** b * (math.sinh(eta) - eta)
        dt = dt_rel * time
        ht = time * (radius(label, time + dt) - radius(label, time - dt)) / (2 * dt * radius(label, time))
        return eta, ht
    return ht_at_crossing


out = {"p3_convergence": [], "p3_labels": [], "other_profiles": []}
f3 = make(3)
for step in (1e-2, 1e-3, 1e-4, 5e-5, 1e-5):
    eta, ht = f3(2.0, step)
    out["p3_convergence"].append({"step": step, "eta": eta, "Ht": ht, "err_vs_8_9": ht - 8 / 9})
for label in (1.05, 2.0, 5.0):
    eta, ht = f3(label, 1e-4 * label)
    out["p3_labels"].append({"label": label, "eta": eta, "Ht": ht, "err_vs_8_9": ht - 8 / 9})
for p in (4.0, 6.0):
    eta, ht = make(p)(2.0, 1e-4)
    target = 2 * (1 + p) / (3 * p)
    out["other_profiles"].append({"p": p, "eta": eta, "Ht": ht, "analytic": target, "err": ht - target})
Path(sys.argv[1]).write_bytes((json.dumps(out, indent=1) + "\n").encode())
print(json.dumps(out, indent=1))
