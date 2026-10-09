"""Check the new test's error estimates with independent paired influences.

This reuses its declared synthetic distribution and fixed seed, not its
analytical normalizer as a sampling input. Proper standard errors account
for the correlated two observations contributed by each Gaussian pair.
Usage: python -B -W error THIS_FILE REPO OUT.json
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.special import ndtr
from scipy.stats import norm

REPO, OUT = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(REPO / "src"))
spec = importlib.util.spec_from_file_location("audit_mc_helpers", REPO / "tests/test_phase1g_h_global_variance.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
ev = t._evidence()
rng = np.random.default_rng(31)
f_v, rho, lam, xs0, xsr, g0, gr = 0.737, 0.6, 0.8, 1.0, 0.45, 0.5, 0.3
f_w, c, size = 1.0 - f_v, norm.ppf(f_v), 2_000_000
rows = []
for law, shared in (("I_independent", False), ("II_same_field", True)):
    k0, kr = (g0, gr) if shared else (0.0, 0.0)
    cov = np.array([[1, rho, k0, kr], [rho, 1, kr, k0], [k0, kr, xs0, xsr], [kr, k0, xsr, xs0]])
    z = rng.multivariate_normal(np.zeros(4), cov, size=size)
    chi1, chi2 = z[:, 0] > c, z[:, 1] > c
    x1, x2 = np.exp(lam * z[:, 2] - 0.5 * lam * lam * xs0), np.exp(lam * z[:, 3] - 0.5 * lam * lam * xs0)
    walls = np.concatenate((x1[chi1], x2[chi2]))
    m_s = walls.mean()
    se_m_test = walls.std() / math.sqrt(walls.size)
    count_wall = chi1.astype(float) + chi2
    influence_m = (chi1 * (x1 - m_s) + chi2 * (x2 - m_s)) / count_wall.mean()
    se_m_pair = influence_m.std() / math.sqrt(size)
    both = chi1 & chi2
    y = x1[both] * x2[both] / m_s ** 2
    c_s = y.mean()
    # Influence of the both-wall ratio, including normalizer covariance.
    influence_c = both * (x1 * x2 / m_s ** 2 - c_s) / both.mean() - 2.0 * c_s * influence_m / m_s
    se_c_pair = influence_c.std() / math.sqrt(size)
    budget_test = y.std() / math.sqrt(y.size) + 2.0 * c_s * se_m_test / m_s
    m_exact = ndtr(-(c - lam * k0)) / f_w
    p11, kww, kpw = ev.lognormal_mask_kernels(rho=rho, c=c, f_w=f_w, lam=lam,
                                             xi_lat_r=xsr, kappa0=lam*k0, kappa_r=lam*kr)
    c_exact = 1.0 + (kww + 2.0 * kpw) / p11
    rows.append({"law": law, "sample_normalizer": float(m_s), "analytic_normalizer": float(m_exact),
        "naive_normalizer_se": float(se_m_test), "pair_aware_normalizer_se": float(se_m_pair),
        "pair_over_naive_normalizer_se": float(se_m_pair / se_m_test),
        "normalizer_error_in_pair_se": float(abs(m_s-m_exact) / se_m_pair),
        "sample_cw": float(c_s), "analytic_cw": float(c_exact),
        "test_cw_error_budget": float(budget_test), "pair_aware_cw_se": float(se_c_pair),
        "test_budget_over_pair_se": float(budget_test / se_c_pair),
        "cw_error_in_pair_se": float(abs(c_s-c_exact) / se_c_pair),
        "test_cw_relative_5budget": float(5.0 * budget_test / c_exact)})
OUT.write_text(json.dumps({"scope": "synthetic two-point test error budgets; empirical, fixed seed", "results": rows}, indent=1) + "\n")
print(json.dumps(rows, indent=1))
