"""Conditional LTB geometry, independent of every Timescape clock/background.

S10 = Sussman, arXiv:1002.0173v2, Eqs. (1)--(3): here M=m and
E_S10=2*E_LTB=r**2*kappa (S10's gravitational kappa is NOT our profile).
The fixed profile and simultaneous bang are the user-authorized sector,
not published Timescape equations. All computations use c=1; G is explicit.
No upstream source is used. See reports/experimental_ltb_cmc.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import math
from numbers import Real

import numpy as np
from numpy.typing import NDArray
from numpy.polynomial.legendre import leggauss

Array = NDArray[np.float64]


class LTBDomainError(ValueError):
    """Input outside the mathematical/API domain."""


class LTBNumericalError(ArithmeticError):
    """Numerical failure; NOT a statement of geometric non-existence."""


def scalar(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise LTBDomainError(f"{name} must be a finite real scalar")
    try:
        result = float(value)
    except OverflowError as exc:
        raise LTBNumericalError(f"{name} is not representable") from exc
    if not math.isfinite(result):
        raise LTBDomainError(f"{name} must be finite")
    return result


def finite(*values: object) -> None:
    if any(not np.all(np.isfinite(v)) for v in values):
        raise LTBNumericalError("Non-finite intermediate or output")


def dimensional(value: Array | float, scale: float, power: int,
                divisor: float = 1.0) -> Array | float:
    """Rescale without avoidable intermediate overflow; reject lost nonzeros."""
    v = np.asarray(value, dtype=float)
    finite(v)
    nonzero = v != 0
    out = np.zeros_like(v)
    logs = np.log(np.abs(v[nonzero])) + power * math.log(scale) - math.log(divisor)
    limits = np.finfo(float)
    if np.any(logs > math.log(limits.max)) or np.any(logs < math.log(limits.tiny)):
        raise LTBNumericalError("Dimensional output outside normal binary64 range")
    out[nonzero] = np.sign(v[nonzero]) * np.exp(logs)
    finite(out)
    return float(out) if out.ndim == 0 else out


@dataclass(frozen=True)
class LTBModel:
    """External closure: m0 in length units, G in length/mass units (c=1).

    r, kappa_star, r_c, r_o are dimensionless. Unit names are mandatory
    metadata, not conversions. There is no default numerical value of G.
    Spherical symmetry/simultaneous bang: MODEL_SECTOR_RESTRICTION.
    Profile/anchors: EXTERNAL_CLOSURE_INPUT.
    """

    m0: float
    kappa_star: float
    r_c: float
    r_o: float
    G: float
    length_unit: str
    mass_unit: str

    def __post_init__(self) -> None:
        for name in ("m0", "kappa_star", "r_c", "r_o", "G"):
            object.__setattr__(self, name, scalar(getattr(self, name), name))
        if self.m0 <= 0 or self.G <= 0 or self.kappa_star < 0:
            raise LTBDomainError("Require m0>0, G>0, kappa_star>=0")
        if not 0 < self.r_c < self.r_o < 1:
            raise LTBDomainError("Require 0<r_c<r_o<1")
        for unit in (self.length_unit, self.mass_unit):
            if not isinstance(unit, str) or not unit.strip():
                raise LTBDomainError("Explicit length and mass unit names required")


@dataclass(frozen=True)
class Numerics:
    """Explicit dimensionless engineering tolerances, not error certificates.

    bvp_tol: SciPy's relative RMS collocation residual; bc_tol: absolute
    residual after scaling lengths by s_c. age_rtol: relative age integral
    and its quadrature comparison. check_tol: normalized sampled residual,
    conservation and quadrature checks (denominator max(1, |terms|)).
    quadrature_order is doubled for the accepted calculation; the lower
    order supplies an independent resolution check. No hidden root scan.
    """

    bvp_tol: float = 2e-7
    bc_tol: float = 2e-10
    age_rtol: float = 2e-12
    check_tol: float = 2e-5
    initial_nodes: int = 81
    max_nodes: int = 4000
    check_nodes: int = 401
    quadrature_order: int = 32
    age_maxiter: int = 60

    def __post_init__(self) -> None:
        for name in ("bvp_tol", "bc_tol", "age_rtol", "check_tol"):
            value = scalar(getattr(self, name), name)
            if not 64 * np.finfo(float).eps <= value < 0.1:
                raise LTBDomainError(f"{name} must be in [64*eps, 0.1)")
        for name in ("initial_nodes", "max_nodes", "check_nodes",
                     "quadrature_order", "age_maxiter"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 4:
                raise LTBDomainError(f"{name} must be an integer >=4")
        if self.max_nodes < self.initial_nodes + 11:
            raise LTBDomainError("max_nodes must allow the initial transition mesh")


@lru_cache(maxsize=16)
def gauss(order: int) -> tuple[Array, Array]:
    z, w = leggauss(order)
    z, w = (z + 1) / 2, w / 2
    z.setflags(write=False)
    w.setflags(write=False)
    return z, w


def curvature(r: Array, model: LTBModel) -> tuple[Array, Array]:
    """User's fixed chi and analytic first derivative; S10 Eq. (2) closure.

    Logistic evaluation avoids exp/exp and 1-chi cancellation. Tails
    |logit|>~10**6 round to their endpoints: even finite binary64 kappa
    and an inverse representable transition width cannot rescue them.
    Smooth exponential-tail underflow is harmless; bulk loss is not.
    """
    r = np.asarray(r, dtype=float)
    k = np.zeros_like(r)
    kr = np.zeros_like(r)
    if model.kappa_star == 0:
        return k, kr
    z = (r - model.r_c) / (model.r_o - model.r_c)
    k[z >= 1 - 1e-6] = model.kappa_star
    mask = (z > 1e-6) & (z < 1 - 1e-6)
    u = z[mask]
    h = 1 / (1 - u) - 1 / u
    logchi = -np.logaddexp(0, -h)
    logother = -np.logaddexp(0, h)
    loghp = np.logaddexp(-2 * np.log(u), -2 * np.log1p(-u))
    k[mask] = np.exp(math.log(model.kappa_star) + logchi)
    kr[mask] = np.exp(math.log(model.kappa_star) + logchi + logother
                      + loghp - math.log(model.r_o - model.r_c))
    finite(k, kr)
    return k, kr


@dataclass(frozen=True)
class LocalGeometry:
    """Internal values with length unit s_c; density is G*rho, not rho."""

    a: Array
    a_kappa: Array
    a_s: Array
    A: Array
    R: Array
    R_r: Array
    radial_extra: Array  # R_r/R - 1/r, regular at the centre
    Theta: Array
    sigma2: Array
    G_rho: Array
    R_u: Array
    sqrt_energy: Array


class Geometry:
    """Internal evaluator; s and m are divided by the supplied central age."""

    def __init__(self, model: LTBModel, s_c: float, numerics: Numerics):
        self.model, self.numerics = model, numerics
        self.m = dimensional(model.m0, s_c, -1)

    def _integrals(self, a: Array, k: Array, order: int) -> tuple[Array, Array]:
        # S10 Eq. (2), y=a*z**2 in the age integral and its k derivative.
        z, w = gauss(order)
        h = k * a / (2 * self.m)
        den = np.sqrt(1 + h[:, None] * z**2)
        age = (a * np.sqrt(a / (2 * self.m))) * (2 * (z**2 / den) @ w)
        integral = (a * (a / (2 * self.m))**1.5) * (2 * (z**4 / den**3) @ w)
        return age, integral

    def at(self, s: Array, r: Array) -> LocalGeometry:
        """S10 Eqs. (1)--(3), and their analytic time/radial derivatives.

        Expansion/curvature: S10 Eq. (5); shear: S10 Eqs. (6),(7),
        sigma2=3*Sigma_S10**2. They obey BMR 1912.04213v2 Eq. (4.16).
        R=r*a removes all centre 0/0 expressions. a_kappa is obtained by
        differentiating the age integral at fixed s, never along the graph.
        """
        s, r = np.broadcast_arrays(np.asarray(s, float), np.asarray(r, float))
        if s.ndim != 1 or np.any(s <= 0):
            raise LTBNumericalError("BVP trial age outside positive regular domain")
        finite(s, r)
        k, kr = curvature(r, self.model)
        a0 = np.exp((math.log(4.5) + math.log(self.m) + 2 * np.log(s)) / 3)
        a = a0.copy()
        ak = a0**2 / (10 * self.m)  # differentiated parabolic limit, S10 (2)
        curved = k > 0
        if np.any(curved):
            ss, kk = s[curved], k[curved]
            lo = a0[curved].copy()
            hi = lo + ss * np.sqrt(kk)
            aa = (lo + hi) / 2
            order = 2 * self.numerics.quadrature_order
            for _ in range(self.numerics.age_maxiter):
                age, integ = self._integrals(aa, kk, order)
                error = age - ss
                if np.max(np.abs(error) / ss) <= self.numerics.age_rtol:
                    break
                lo = np.where(error < 0, aa, lo)
                hi = np.where(error >= 0, aa, hi)
                trial = aa - error * np.sqrt(2 * self.m / aa + kk)
                aa = np.where((trial > lo) & (trial < hi), trial, (lo + hi) / 2)
            else:
                raise LTBNumericalError("LTB age inversion did not converge")
            age_low, int_low = self._integrals(aa, kk, order // 2)
            qerr = max(np.max(np.abs(age_low - age) / ss),
                       np.max(np.abs(int_low - integ) / integ))
            if qerr > self.numerics.age_rtol * 8:
                raise LTBNumericalError("LTB age quadrature is under-resolved")
            a[curved] = aa
            ak[curved] = np.sqrt(2 * self.m / aa + kk) * integ / 2
        a_s = np.sqrt(2 * self.m / a + k)
        a_sk = (1 - 2 * self.m * ak / a**2) / (2 * a_s)
        rr = a + r * ak * kr
        rsr = a_s + r * a_sk * kr
        sqrt_energy = np.sqrt(1 + r**2 * k)
        hp, hl = a_s / a, rsr / rr
        rho = 3 * self.m / (4 * np.pi * a**2 * rr)
        ru = -2 * (3 * k * a + r * kr * (a + k * ak)) / (a**2 * rr)
        finite(a, ak, rr, rsr, rho, ru, sqrt_energy, hp, hl)
        if np.any(rr <= 0) or np.any(rho <= 0):
            raise LTBNumericalError("Lost positive R_r or density")
        return LocalGeometry(a, ak, a_s, rr / sqrt_energy, r * a, rr,
                             ak * kr / a, hl + 2 * hp, (hl - hp)**2 / 3,
                             rho, ru, sqrt_energy)
