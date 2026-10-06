"""Auditor: F2 vs F3 values for frozen 1G-F statements not explicitly rectified by the successor.

Frozen Sec. 1 item 5 / Sec. 8.2: C1 near-empty barriers (x = 0.1, 0.05), r_min reproducing f_v0.
Frozen Sec. 1 item 6 / Sec. 9: C1 shell crossing, voids >= 1 h^-1 Mpc at z = 0...3.
Uses the auditor's closed-form module indep_f (no project code).
"""
import json
import math
import sys

from scipy.optimize import brentq

sys.path.insert(0, __file__.rsplit("\\", 1)[0])
import indep_f as F


def barrier(xr):
    eta = brentq(lambda e: 4.5 * (math.sinh(e) - e) ** 2 / (math.cosh(e) - 1) ** 3 - xr, 0.1, 60, xtol=1e-15)
    return abs(-(3 / 20) * (6 * (math.sinh(eta) - eta)) ** (2 / 3))


dc = 0.6 * (1.5 * math.pi) ** (2 / 3)
gL = F.lcdm_growth_today(F.PL["Om"])
anchor = F.PL["sigma8"] / (F.sigma_unit(8 / F.PL["h"], F.PL["omega_m"]) * gL)
out = {}
for name, c in F.CASES.items():
    tr = F.tracker(c["fv0"], c["H0"])
    D = tr["frame"](1.0)
    row = {}
    for xr in (0.1, 0.05):
        dv = barrier(xr)
        pop = F.Population(tr["omega_eff"], anchor, D, D, tr["h"], dv, dc, xr)
        row[f"x={xr}"] = dict(delta_v=-dv, F2_all=(pop.m_total / xr) / (1 - pop.m_total + pop.m_total / xr),
                              rmin_F2=pop.cutoff(c["fv0"], True), rmin_F3=pop.cutoff(c["fv0"], False),
                              F2_ge1=pop.F2(1.0), F3_ge1=pop.F3(1.0))
    sc = F.shell_crossing_independent()
    hist = []
    for z in (0.0, 0.5, 1.0, 2.0, 3.0):
        t = tr["t_of_z"](z)
        fr = tr["frame"](t)
        pop = F.Population(tr["omega_eff"], anchor, fr / (1 + z), fr, tr["h"], abs(sc["delta_v"]), dc, sc["one_plus_delta_sc"])
        hist.append(dict(z=z, tracker=tr["fv"](t), F2_ge1=pop.F2(1.0), F3_ge1=pop.F3(1.0)))
    out[name] = dict(near_empty=row, history_ge1=hist)
print(json.dumps(out, indent=1))
with open(sys.argv[1], "wb") as fh:
    fh.write((json.dumps(out, indent=1) + "\n").encode())
