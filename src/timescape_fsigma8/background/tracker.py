"""Tracker-solution geometry and dust sector.

Void fraction, scale factor, expansion, averaged curvature, kinematical
backreaction, dust density, and the bare density parameters. Formulas are
verbatim from the pre-split module (equivalence pinned in
tests/test_refactor_equivalence.py). References: [GM] = arXiv:2511.17160v2;
[W09] = arXiv:0909.0749. Documented deviations (D1), (D2): see the package
docstring.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

from timescape_fsigma8.background.parameters import TrackerParams, _t

# --------------------------------------------------------------------------
# Void fraction and its time derivatives
# --------------------------------------------------------------------------

def fv(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Void fraction f_v(t) of the tracker solution.

    f_v(t) = 3 fv0 HD0 t / [3 fv0 HD0 t + (2 + fv0)(1 - fv0)]
    [GM] Eq. (5.6); [W09] Eq. (B2).
    """
    t = _t(t)
    x = 3.0 * p.fv0 * p.HD0 * t
    return x / (x + (2.0 + p.fv0) * (1.0 - p.fv0))


def dfv_dt(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """d f_v / d t = f_v (1 - f_v) / t   (derived).

    Differentiating [GM] (5.6): with x = 3 fv0 HD0 t and
    c = (2+fv0)(1-fv0), df_v/dt = x c / [t (x + c)^2] = f_v (1 - f_v)/t.
    Validated against numerical differentiation in tests.
    """
    t = _t(t)
    f = fv(t, p)
    return f * (1.0 - f) / t


def d2fv_dt2(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """d^2 f_v / d t^2 = -2 f_v^2 (1 - f_v) / t^2   (derived).

    Differentiating dfv_dt: d/dt [f_v(1-f_v)/t]
      = [f_v(1-f_v)(1-2f_v) - f_v(1-f_v)] / t^2 = -2 f_v^2 (1-f_v)/t^2.
    """
    t = _t(t)
    f = fv(t, p)
    return -2.0 * f**2 * (1.0 - f) / t**2


# --------------------------------------------------------------------------
# Scale factor and expansion
# --------------------------------------------------------------------------

def a_D(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Volume-average scale factor a_D(t), normalised to a_{w,0} = 1.

    a_D(t) = [3 a_{D,0} HD0 t / (2 + fv0)] * [fv0 / f_v(t)]^(1/3)
    [GM] Eq. (5.5); equivalent to [W09] Eq. (B1). a_{D,0} = 1 + fv0/2
    (see TrackerParams.aD0), so a_D is in units of a_{w,0}.
    """
    t = _t(t)
    return (3.0 * p.aD0 * p.HD0 * t / (2.0 + p.fv0)) * np.cbrt(p.fv0 / fv(t, p))


def H_D(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Bare (volume-average) Hubble parameter H_D = da_D/dt / a_D.

    H_D(t) = (2 + f_v(t)) / (3 t)
    [W09] Eq. (B6); definition [GM] Eq. (3.6). Follows from (5.5)-(5.6):
    d ln a_D/dt = 1/t - (df_v/dt)/(3 f_v) = 1/t - (1 - f_v)/(3t).
    """
    t = _t(t)
    return (2.0 + fv(t, p)) / (3.0 * t)


def da_D_dt(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Time derivative of the scale factor, da_D/dt = a_D H_D.

    [GM] Eq. (3.6) rearranged; components cited in `a_D` and `H_D`.
    """
    return a_D(t, p) * H_D(t, p)


def Theta(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Averaged expansion scalar <Theta>_D = 3 H_D. [GM] Eq. (3.6)."""
    return 3.0 * H_D(t, p)


# --------------------------------------------------------------------------
# Curvature, backreaction, and their time derivatives
# --------------------------------------------------------------------------

def R_D(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Averaged spatial curvature <R>_D(t) = -6 f_v(t) / t^2.

    [GM] Eq. (5.7), first member, WITHOUT the printed f_{v,0}^{-2/3}
    prefactor — documented deviation (D1), see the package docstring.
    Cross-checked: [W09] (B4) Omega_k = 9 f_v/(2+f_v)^2 with
    Omega_k = -<R>_D/(6 H_D^2) ([GM] (3.18)) and H_D = (2+f_v)/(3t)
    gives exactly <R>_D = -6 f_v/t^2. Validated against the Hamiltonian
    constraint (3.8) and the upstream oracle in tests.
    """
    t = _t(t)
    return -6.0 * fv(t, p) / t**2


def Q_D(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Kinematical backreaction Q_D(t) = 2 (df_v/dt)^2 / [3 f_v (1 - f_v)].

    [GM] Eq. (5.7), second member; [W09] Eq. (15). With the tracker
    identity df_v/dt = f_v(1-f_v)/t this reduces to the closed form
    Q_D = 2 f_v (1 - f_v) / (3 t^2)   (derived), used here.
    """
    t = _t(t)
    f = fv(t, p)
    return 2.0 * f * (1.0 - f) / (3.0 * t**2)


def dR_D_dt(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """d<R>_D/dt = 6 f_v (1 + f_v) / t^3   (derived).

    d/dt[-6 f_v/t^2] = -6[f_v(1-f_v)/t^3 - 2 f_v/t^3] = 6 f_v(1+f_v)/t^3.
    Validated via the integrability condition [GM] (3.11) in tests.
    """
    t = _t(t)
    f = fv(t, p)
    return 6.0 * f * (1.0 + f) / t**3


def dQ_D_dt(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """dQ_D/dt = -2 f_v (1 - f_v)(1 + 2 f_v) / (3 t^3)   (derived).

    d/dt[2 f_v(1-f_v)/(3t^2)] with df_v/dt = f_v(1-f_v)/t:
      = (2/3)[f_v(1-f_v)(1-2f_v) - 2 f_v(1-f_v)]/t^3
      = -2 f_v (1-f_v)(1+2f_v)/(3 t^3).
    NOTE: intentionally differs from the upstream notebook's `dQDdt`
    (documented deviation (D2), see the package docstring). Validated via
    numerical differentiation of Q_D and the integrability condition
    [GM] (3.11) in tests.
    """
    t = _t(t)
    f = fv(t, p)
    return -2.0 * f * (1.0 - f) * (1.0 + 2.0 * f) / (3.0 * t**3)


# --------------------------------------------------------------------------
# Dust density
# --------------------------------------------------------------------------

def rho_d(t: ArrayLike, p: TrackerParams, G: float = 1.0) -> NDArray[np.float64]:
    """Averaged dust density <rho_d>_D(t) = (1 - f_v(t)) / (6 pi G t^2)  (derived).

    From a_D^{-3} scaling ([GM] Eq. (3.16)) with normalisation
    <rho_d>_D(t0) = 12 HD0^2 (1 - fv0) / [8 pi G (2 + fv0)^2]
    ([GM] text after Eq. (5.7)). Closed form: 8 pi G rho_d = 3 H_D^2
    Omega_m with Omega_m = 4(1-f_v)/(2+f_v)^2 ([W09] (B3)) and
    H_D = (2+f_v)/(3t) gives 8 pi G rho_d = 4 (1-f_v)/(3 t^2).
    Validated against the a_D^{-3} scaling law in tests.
    """
    t = _t(t)
    return (1.0 - fv(t, p)) / (6.0 * np.pi * G * t**2)


def drho_d_dt(t: ArrayLike, p: TrackerParams, G: float = 1.0) -> NDArray[np.float64]:
    """d<rho_d>_D/dt = -(1 - f_v)(2 + f_v) / (6 pi G t^3)   (derived).

    d/dt[(1-f_v)/(6 pi G t^2)] = [-f_v(1-f_v) - 2(1-f_v)]/(6 pi G t^3).
    Equals -3 H_D rho_d exactly (mass conservation, [GM] Eq. (3.10)).
    """
    t = _t(t)
    f = fv(t, p)
    return -(1.0 - f) * (2.0 + f) / (6.0 * np.pi * G * t**3)


# --------------------------------------------------------------------------
# Density parameters, [GM] Eq. (3.18)
# --------------------------------------------------------------------------

def Omega_m(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Bare matter density parameter Omega_d^D := 8 pi G <rho_d>_D / (3 H_D^2).

    [GM] Eq. (3.18); tracker closed form Omega_m = 4 (1 - f_v)/(2 + f_v)^2,
    [W09] Eq. (B3).
    """
    t = _t(t)
    f = fv(t, p)
    return 4.0 * (1.0 - f) / (2.0 + f) ** 2


def Omega_R(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Bare curvature density parameter Omega_R^D := -<R>_D / (6 H_D^2).

    [GM] Eq. (3.18); tracker closed form Omega_R = 9 f_v/(2 + f_v)^2,
    [W09] Eq. (B4).
    """
    t = _t(t)
    f = fv(t, p)
    return 9.0 * f / (2.0 + f) ** 2


def Omega_Q(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Bare backreaction density parameter Omega_Q^D := -Q_D / (6 H_D^2).

    [GM] Eq. (3.18); tracker closed form Omega_Q = -f_v (1 - f_v)/(2 + f_v)^2,
    [W09] Eq. (B5).
    """
    t = _t(t)
    f = fv(t, p)
    return -f * (1.0 - f) / (2.0 + f) ** 2
