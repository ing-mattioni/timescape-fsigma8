"""First radial panel [0, 2R/480] contribution and unnormalised signed wall moments.

Reuses blind_h25_mII_cw.py (own code) and the calibrated ell of a finished
run; no project import.  Prints, per scenario, the signed law-II wall moment
E-weighted int pair * wall_kernel (not divided by f_w^2), its first-panel part,
and the relative size of that part, plus the lognormal analogue.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.special import ndtri

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blind_h25_mII_cw as B  # noqa: E402  (own module)

run = json.loads(Path(sys.argv[1]).read_text())
out = {}
for name, f, H in (("GM", .737, 73.03), ("NW15", .627, 61.0)):
    from scipy.integrate import quad
    om_l = .315
    growth = 2.5 * om_l * quad(lambda a: 1 / (a ** 3 * (om_l / a ** 3 + 1 - om_l) ** 1.5), 0, 1, epsabs=1e-13)[0]
    anchor = .8111 / (B.prov.sig(B.prov.spectrum(B.prov.K, B.prov.OMREF), 8 / .674) * growth)
    t = B.prov.tracker(f, H)
    fld = B.Field(t, anchor)
    R = 800 / H
    fw = 1 - f
    c = float(ndtri(f))
    ell = run[name]["ell_Mpc"]
    h = 2 * R / 480
    res = {}
    for label, (a, b) in (("first_panel", (0.0, h)), ("rest", (h, 2 * R))):
        x, w = np.polynomial.legendre.leggauss(64)
        sub = np.linspace(a, b, 9 if label == "first_panel" else int(sys.argv[2]) + 1)
        r = np.concatenate([0.5 * (q - p) * x + 0.5 * (q + p) for p, q in zip(sub[:-1], sub[1:])])
        wt = np.concatenate([0.5 * (q - p) * w for p, q in zip(sub[:-1], sub[1:])])
        pw = wt * 3 * r * r / R ** 3 * (1 - 3 * r / (4 * R) + r ** 3 / (16 * R ** 3))
        v0 = fld.var(lambda k: 1.0)
        xi = fld.xi(r, lambda k: 1.0, v0)
        vl = fld.var(lambda k: math.exp(-(k * ell) ** 2))
        rho = fld.xi(r, lambda k: math.exp(-(k * ell) ** 2), vl) / vl
        b0 = fld.var(lambda k: math.exp(-0.5 * (k * ell) ** 2)) / math.sqrt(vl)
        br = fld.xi(r, lambda k: math.exp(-0.5 * (k * ell) ** 2), v0) / math.sqrt(vl)
        s = B.signed_pair(c, fw, rho, xi, b0, br, pw)
        res[label] = {law: {"wall_moment_unnormalised": s[law]["wall_rms"] ** 2 * fw ** 2,
                            "cross_moment_unnormalised": s[law]["cross_term"] / 2 * fw ** 2,
                            "partition_moment_unnormalised": s[law]["partition_rms"] ** 2 * fw ** 2}
                      for law in ("I", "II")}
        res[label]["pair_weight"] = float(pw.sum())
    tot = res["first_panel"]["II"]["wall_moment_unnormalised"] + res["rest"]["II"]["wall_moment_unnormalised"]
    res["signed_II_wall_moment_total"] = tot
    res["first_panel_share_of_signed_II_wall"] = res["first_panel"]["II"]["wall_moment_unnormalised"] / tot
    res["first_panel_pair_weight"] = res["first_panel"]["pair_weight"]
    out[name] = res
print(json.dumps(out, indent=1))
