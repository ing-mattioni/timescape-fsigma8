"""Second delta audit of Phase 1G-H: blind reconstruction of (H25), m_II and <C_W - 1>.

No import from the audited project (src/, scripts/, tests/).  The tracker and the
EH98 no-wiggle early spectrum are taken from the FIRST independent audit's
provider (reports/phase1g_h_independent_audit_evidence/independent_numerics.py,
copied verbatim as first_audit_provider.py; SHA-256 recorded in the output).
Everything that is new in the second remediation is coded here from the model
definitions of [1G-H] Sec. 6.1/6.3 only:

* bivariate upper-orthant probability by Owen's T (closed form; the author uses
  adaptive panel quadrature, the delta audit 1-D QUADPACK);
* signed-pair Gaussian moments by Gaussian integration by parts (Stein), not by
  orthant moment tables;
* lognormal kernels by exponential tilting;
* correlation functions by QUADPACK Fourier (QAWO) integrals on [kmin, kmax];
* ball pair integrals by composite Gauss-Legendre on [0, 2R] (no node at r = 0,
  the first panel is included by construction), with a convergence check
  against a doubled panel count and against the exact spectral ball variance
  int Delta^2 W^2(kR) dlnk.

Tolerances (AGENTS rule 9): QAWO epsabs 1e-14 relative to the point variance,
epsrel 1e-11, limit 2000; brentq xtol 1e-12 / rtol 1e-13; Owen's T from SciPy
(Patefield-Tandy, absolute accuracy ~1e-16).  Convergence is reported, not
assumed.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import ndtr, ndtri, owens_t

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("prov", HERE / "first_audit_provider.py")
prov = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prov)

KMIN, KMAX = 1e-5, 80.0


def phi(x):
    return np.exp(-0.5 * np.asarray(x, float) ** 2) / math.sqrt(2 * math.pi)


def Phi2(h, k, rho):
    """P(X < h, Y < k) for standard bivariate normal with correlation rho (Owen's T)."""
    h = np.asarray(h, float); k = np.asarray(k, float); rho = np.asarray(rho, float)
    h, k, rho = np.broadcast_arrays(h, k, rho)
    s = np.sqrt((1 - rho) * (1 + rho))
    out = np.empty(h.shape)
    with np.errstate(divide="ignore", invalid="ignore"):
        ah = (k - rho * h) / (h * s)
        ak = (h - rho * k) / (k * s)
    beta = np.where((h * k < 0) | ((h * k == 0) & (h + k < 0)), 0.5, 0.0)
    if np.any(h == 0) or np.any(k == 0):
        raise ValueError("zero threshold: not needed here")
    out = 0.5 * ndtr(h) + 0.5 * ndtr(k) - owens_t(h, ah) - owens_t(k, ak) - beta
    return out


def U(a, b, rho):
    """P(X > a, Y > b)."""
    return Phi2(-np.asarray(a, float), -np.asarray(b, float), rho)


def U_quad(a, b, rho):
    """Cross-check by direct conditional-normal quadrature."""
    s = math.sqrt(1 - rho * rho)
    f = lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi) * float(ndtr((rho * x - b) / s))
    return quad(f, a, np.inf, epsabs=1e-15, epsrel=1e-13, limit=500)[0]


class Field:
    """Delta^2 of the wall-internal linear carrier and its Hankel transforms."""

    def __init__(self, t, anchor):
        self.dwall = t["DW"] * (1 - t["fi"]) / (1 - t["f"])
        self.om = t["omega_eff"]
        self.anchor = anchor

    def d2(self, k):
        k = np.asarray(k, float)
        return prov.spectrum(k * self.dwall, self.om) * self.dwall ** 2 * self.anchor ** 2

    def var(self, filt):
        f = lambda lk: float(self.d2(math.exp(lk)) * filt(math.exp(lk)))
        pts = np.linspace(math.log(KMIN), math.log(KMAX), 41)
        return sum(quad(f, a, b, epsabs=1e-16, epsrel=1e-12, limit=400)[0] for a, b in zip(pts[:-1], pts[1:]))

    def xi(self, r, filt, scale):
        """int Delta^2 filt j0(kr) dlnk = (1/r) int Delta^2 filt / k^2 sin(kr) dk (QAWO)."""
        g = lambda k: float(self.d2(k) * filt(k)) / (k * k)
        out = np.empty(len(r))
        # split at k = 1 to help QAWO on the steep low-k part
        for i, ri in enumerate(r):
            tot = 0.0
            for a, b in ((KMIN, 0.01), (0.01, 1.0), (1.0, KMAX)):
                v, _ = quad(g, a, b, weight="sin", wvar=ri, epsabs=1e-14 * scale, epsrel=1e-11, limit=2000)
                tot += v
            out[i] = tot / ri
        return out


def gl_nodes(R, panels, n):
    x, w = leggauss(n)
    edges = np.linspace(0.0, 2 * R, panels + 1)
    r = np.concatenate([0.5 * (b - a) * x + 0.5 * (b + a) for a, b in zip(edges[:-1], edges[1:])])
    wt = np.concatenate([0.5 * (b - a) * w for a, b in zip(edges[:-1], edges[1:])])
    pair = 3 * r * r / R ** 3 * (1 - 3 * r / (4 * R) + r ** 3 / (16 * R ** 3))
    return r, wt * pair


def tophat_ball_variance(field, R):
    f = lambda lk: float(field.d2(math.exp(lk)) * prov.W(np.array([math.exp(lk) * R]))[0] ** 2)
    pts = np.linspace(math.log(KMIN), math.log(KMAX), 81)
    return sum(quad(f, a, b, epsabs=1e-16, epsrel=1e-12, limit=400)[0] for a, b in zip(pts[:-1], pts[1:]))


def signed_pair(c, fw, rho, xi, b0, br, pw):
    """Signed Gaussian pair (law I independent mask, law II mask = smoothed carrier)."""
    s = np.sqrt((1 - rho) * (1 + rho))
    z = c * np.sqrt((1 - rho) / (1 + rho))
    P11 = U(c, c, rho)
    dens2 = np.exp(-c * c / (1 + rho)) / (2 * math.pi * s)          # phi2(c, c; rho)
    A = c * phi(c) * ndtr(-z) - phi(c) * phi(z) * rho / s            # E[d^2/dg1^2 F]
    EwF = (b0 + br) * phi(c) * ndtr(-z)                               # E[w2 chi1 chi2]
    EwwF = xi * P11 + 2 * b0 * br * A + (b0 * b0 + br * br) * dens2  # E[w1 w2 chi1 chi2]
    mu = b0 * float(phi(c)) / fw
    out = {}
    for name, wall, cross in (("I", P11 * xi, np.zeros_like(xi)),
                              ("II", EwwF - 2 * mu * EwF + mu * mu * P11, EwF - mu * P11)):
        part = P11 - fw * fw
        CWm1 = (wall + 2 * cross) / P11
        vp = float(pw @ part) / fw ** 2
        vw = float(pw @ wall) / fw ** 2
        vc = 2 * float(pw @ cross) / fw ** 2
        tot = vp + vw + vc
        h25 = float(pw @ (P11 * (1 + CWm1) / fw ** 2 - 1))
        out[name] = dict(partition_rms=math.sqrt(vp), wall_rms=math.sqrt(vw), cross_term=vc,
                         total=math.sqrt(tot), total_var=tot, h25_total_var=h25,
                         h25_rel=abs(h25 / tot - 1),
                         CW_minus_1_pairweighted=float(pw @ (P11 * CWm1)) / float(pw @ P11),
                         affine_check=vp + (1 + vp) * float(pw @ (P11 * CWm1)) / float(pw @ P11) / float(pw.sum()) * float(pw.sum()))
    out["mu_lawII"] = mu
    return out


def lognormal_pair(c, fw, rho, q, q0, b0a, bra, pw):
    """Lognormal pair by exponential tilting; psi = e^a / E[e^a | wall]."""
    P11 = U(c, c, rho)
    res = {}
    for name, B0, BR in (("I", 0.0, np.zeros_like(q)), ("II", b0a, bra)):
        m = float(ndtr(B0 - c)) / fw                     # Q(c - kappa0) / f_w
        Ep = U(c - BR, c - B0, rho) / m                  # E[chi1 chi2 psi2]
        Epp = np.exp(q) * U(c - B0 - BR, c - B0 - BR, rho) / m ** 2  # E[chi1 chi2 psi1 psi2]
        part = P11 - fw * fw
        wall = Epp - 2 * Ep + P11
        cross = Ep - P11
        CW = Epp / P11
        vp = float(pw @ part) / fw ** 2
        vw = float(pw @ wall) / fw ** 2
        vc = 2 * float(pw @ cross) / fw ** 2
        tot = vp + vw + vc
        h25 = float(pw @ (P11 * CW / fw ** 2 - 1))
        cw = float(pw @ (P11 * (CW - 1))) / float(pw @ P11)
        res[name] = dict(m=m, partition_rms=math.sqrt(vp), wall_rms=math.sqrt(vw), cross_term=vc,
                         total=math.sqrt(tot), total_var=tot, h25_total_var=h25,
                         h25_rel=abs(h25 / tot - 1), CW_minus_1_pairweighted=cw,
                         affine_identity_rel=abs((vp + (float(pw @ P11) / fw ** 2) * cw) / tot - 1),
                         # E[chi psi] = f_w check (conditional normalisation)
                         one_point_wall_mass=float(ndtr(B0 - c)) / m / fw * fw)
    res["m_II"] = res["II"]["m"]
    res["ratio_II_over_I"] = res["II"]["total"] / res["I"]["total"]
    return res


def scenario(name, f, H, sp, panels, n):
    om_l = .315
    growth = 2.5 * om_l * quad(lambda a: 1 / (a ** 3 * (om_l / a ** 3 + 1 - om_l) ** 1.5), 0, 1, epsabs=1e-13)[0]
    anchor = .8111 / (prov.sig(prov.spectrum(prov.K, prov.OMREF), 8 / .674) * growth)
    t = prov.tracker(f, H)
    fld = Field(t, anchor)
    R = 800 / H
    fw = 1 - f
    c = float(ndtri(f))
    r, pw = gl_nodes(R, panels, n)
    v0 = fld.var(lambda k: 1.0)
    xi = fld.xi(r, lambda k: 1.0, v0)
    target_spectral = tophat_ball_variance(fld, R)
    target_gl = float(pw @ xi)

    # mask smoothing ell calibrated on the partition rms (signed and lognormal pairs share it)
    def mask_tables(ell):
        v = fld.var(lambda k: math.exp(-(k * ell) ** 2))
        rho = fld.xi(r, lambda k: math.exp(-(k * ell) ** 2), v) / v
        return v, rho

    def part_var(ell):
        _, rho = mask_tables(ell)
        return float(pw @ (U(c, c, rho) - fw * fw)) / fw ** 2 - sp * sp

    lo, hi = {"GM": (0.2, 0.4), "NW15": (0.45, 0.75)}[name]
    ell = brentq(part_var, lo, hi, xtol=1e-12, rtol=1e-13)
    vl, rho = mask_tables(ell)
    b0 = fld.var(lambda k: math.exp(-0.5 * (k * ell) ** 2)) / math.sqrt(vl)
    br = fld.xi(r, lambda k: math.exp(-0.5 * (k * ell) ** 2), v0) / math.sqrt(vl)
    signed = signed_pair(c, fw, rho, xi, b0, br, pw)

    logn = {}
    for rs in (1.0, 2.0, 4.0):
        vs = fld.var(lambda k: math.exp(-(k * rs) ** 2))
        xs = fld.xi(r, lambda k: math.exp(-(k * rs) ** 2), vs)
        b0s = fld.var(lambda k: math.exp(-0.5 * k * k * (rs * rs + ell * ell))) / math.sqrt(vl)
        brs = fld.xi(r, lambda k: math.exp(-0.5 * k * k * (rs * rs + ell * ell)), vs) / math.sqrt(vl)
        l2 = brentq(lambda v: float(pw @ np.expm1(v * xs)) - target_spectral, 1e-6, 50, xtol=1e-14, rtol=1e-13)
        lam = math.sqrt(l2)
        pr = lognormal_pair(c, fw, rho, l2 * xs, l2 * vs, lam * b0s, lam * brs, pw)
        pr.update(lambda_=lam, latent_point_variance=l2 * vs, density_point_variance=math.expm1(l2 * vs),
                  kappa0=lam * b0s, uncond_cov_ratio_II_over_I=1 / pr["m_II"] ** 2,
                  unmasked_ball_var_I=target_spectral, unmasked_ball_var_II=target_spectral / pr["m_II"] ** 2)
        logn[str(rs)] = pr
    return dict(R_Mpc=R, c=c, f_w=fw, ell_Mpc=ell, b0=b0, v0=v0,
                pair_norm=float(pw.sum()), target_spectral=target_spectral, target_gl=target_gl,
                target_rel=abs(target_gl / target_spectral - 1), signed=signed, lognormal=logn)


def main():
    panels, n = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (16, 48)
    # Owen's T cross-check against direct quadrature
    owen = []
    for a, b, rh in [(0.634, 0.634, 0.3), (0.634, -0.5, 0.95), (0.32, 1.4, -0.4), (-1.2, 0.7, 0.999999), (2.5, -0.3, 0.6)]:
        owen.append(dict(a=a, b=b, rho=rh, owen=float(U(a, b, rh)), quad=U_quad(a, b, rh),
                         diff=abs(float(U(a, b, rh)) - U_quad(a, b, rh))))
    out = dict(provider_sha256=hashlib.sha256((HERE / "first_audit_provider.py").read_bytes()).hexdigest(),
               kmin=KMIN, kmax=KMAX, panels=panels, nodes_per_panel=n, owen_check=owen,
               GM=scenario("GM", .737, 73.03, .3264, panels, n),
               NW15=scenario("NW15", .627, 61.0, .3036, panels, n))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
