"""Timescape tracker-solution background quantities.

Independent implementation from the published equations. Scientific
specification (in order of precedence):

  [GM]  M. Galoppo & P. Mourier, "Cosmological perturbations on an averaged
        background", JCAP 02 (2026) 066, arXiv:2511.17160v2.
        Background scheme: Eqs. (3.6)-(3.18); timescape tracker: Sec. 5.1.1,
        Eqs. (5.3)-(5.7) and surrounding text.
  [W09] D. L. Wiltshire, "Average observational quantities in the timescape
        cosmology", PRD 80, 123512 (2009), arXiv:0909.0749.
        Tracker solution: Appendix B, Eqs. (B1)-(B12); Eqs. (15)-(20), (38).

Every function cites its equation number(s) (AGENTS.md rule 2). Closed
forms marked "derived" are our own algebra from the cited equations; each
is validated in tests/ against numerical differentiation, the Buchert
identities (3.8)-(3.11), (3.17), and the upstream oracle.

DOCUMENTED DEVIATIONS FROM PRINTED SOURCES (flagged for human review; see
reports/background_equation_audit.md for the full evidence):

  (D1) [GM] Eq. (5.7) prints <R>_D(t) = -6 f_{v,0}^{-2/3} f_v(t)/t^2. The
       f_{v,0}^{-2/3} prefactor is inconsistent with the Hamiltonian
       constraint (3.8) applied to (5.5)-(5.6), with [W09] (B4)+(B6), and
       with the upstream notebook. We implement <R>_D = -6 f_v(t)/t^2
       (no prefactor) and treat the printed prefactor as a typo.

  (D2) The upstream notebook's d(Q_D)/dt (cell 6, `dQDdt`) multiplies by
       3 f_v (1-f_v) where the quotient rule requires dividing by it. We
       implement the correct derivative. Consequently our c^2_{s,eff}
       (:= dp_eff/dt / drho_eff/dt, [GM] Sec. 4 text) intentionally
       DISAGREES with the upstream notebook and with the published Fig. 1
       (right panel): upstream c^2_{s,eff}(t0) ~ -0.3452, correct value
       -(2 + 2 f_v0 - f_v0^2)/(2 + f_v0)^2 ~ -0.3912.

Conventions: c = 1; Lambda = 0; K_D = 0 ([GM] Sec. 5 preamble), so the
curvature deviation W_D := <R>_D - 6 K_D / a_D^2 equals <R>_D. Time t is
the Buchert volume-average (cosmic) time in any unit consistent with
1/HD0; all outputs carry the corresponding powers of that unit. G enters
only densities and is passed explicitly (AGENTS.md rule 4: no hidden
unit choices). The tracker domain is t > 0.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray


@dataclass(frozen=True)
class TrackerParams:
    """The two free parameters of the timescape tracker ([GM] Sec. 5.1.1).

    fv0 : present-day void volume fraction, 0 < fv0 < 1.
    HD0 : present-day *bare* (volume-average) Hubble parameter H_{D,0},
          in inverse units of the time variable passed to all functions.
    """

    fv0: float
    HD0: float

    def __post_init__(self) -> None:
        if not 0.0 < self.fv0 < 1.0:
            raise ValueError(f"fv0 must be in (0, 1), got {self.fv0}")
        if self.HD0 <= 0.0:
            raise ValueError(f"HD0 must be positive, got {self.HD0}")

    @classmethod
    def from_dressed_H0(cls, fv0: float, H0: float) -> "TrackerParams":
        """Construct from the dressed (observed) Hubble constant H0.

        H_{D,0} = 2 H0 (2 + fv0) / (4 fv0^2 + fv0 + 4)
        [GM] text p. 25 ("one gets at present time the relation..."),
        equivalent to [W09] (B8)-(B9) at t = t0.
        """
        return cls(fv0=fv0, HD0=2.0 * H0 * (2.0 + fv0) / (4.0 * fv0**2 + fv0 + 4.0))

    @property
    def H0_dressed(self) -> float:
        """Dressed Hubble constant H0 = H_{D,0} (4 fv0^2 + fv0 + 4) / (2 (2+fv0)).

        Inverse of the relation in `from_dressed_H0`; [W09] (B8) at t0.
        """
        return self.HD0 * (4.0 * self.fv0**2 + self.fv0 + 4.0) / (2.0 * (2.0 + self.fv0))

    @property
    def t0(self) -> float:
        """Present volume-average age, t0 = (2 + fv0) / (3 H_{D,0}).

        [W09] text after (B5); equivalently H_D(t0) = HD0 in [W09] (B6).
        """
        return (2.0 + self.fv0) / (3.0 * self.HD0)

    @property
    def aD0(self) -> float:
        """Present-day scale-factor normalisation a_{D,0}/a_{w,0} = 1 + fv0/2.

        From the wall-lapse closure gamma_w = 1 + f_v/2 evaluated today,
        with a_w = gamma_w^{-1} a_D normalised to a_{w,0} = 1:
        [GM] Eq. (5.4) and text p. 25 ("a_{D,0}/a_{w,0} = 1 + f_{v,0}/2");
        [W09] (B7).
        """
        return 1.0 + self.fv0 / 2.0


def _t(t: ArrayLike) -> NDArray[np.float64]:
    return np.asarray(t, dtype=np.float64)


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
    prefactor — documented deviation (D1), see module docstring.
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
    (documented deviation (D2), see module docstring). Validated via
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
# Effective (backreaction + curvature) fluid, [GM] Eqs. (3.12)-(3.13)
# --------------------------------------------------------------------------

def rho_eff(t: ArrayLike, p: TrackerParams, G: float = 1.0) -> NDArray[np.float64]:
    """Effective fluid energy density rho_eff = -(Q_D + W_D) / (16 pi G).

    [GM] Eq. (3.12) with W_D = <R>_D (K_D = 0). Tracker closed form
    (derived): rho_eff = f_v (8 + f_v) / (24 pi G t^2).
    """
    t = _t(t)
    f = fv(t, p)
    return f * (8.0 + f) / (24.0 * np.pi * G * t**2)


def p_eff(t: ArrayLike, p: TrackerParams, G: float = 1.0) -> NDArray[np.float64]:
    """Effective fluid pressure p_eff = -Q_D/(16 pi G) + W_D/(48 pi G).

    [GM] Eq. (3.13) with W_D = <R>_D (K_D = 0). Tracker closed form
    (derived): p_eff = -f_v (4 - f_v) / (24 pi G t^2).
    """
    t = _t(t)
    f = fv(t, p)
    return -f * (4.0 - f) / (24.0 * np.pi * G * t**2)


def drho_eff_dt(t: ArrayLike, p: TrackerParams, G: float = 1.0) -> NDArray[np.float64]:
    """d rho_eff/dt = -f_v (2 + f_v)^2 / (12 pi G t^3)   (derived).

    Differentiating the rho_eff closed form with df_v/dt = f_v(1-f_v)/t.
    Equals -3 H_D (rho_eff + p_eff) exactly ([GM] Eq. (3.17)).
    """
    t = _t(t)
    f = fv(t, p)
    return -f * (2.0 + f) ** 2 / (12.0 * np.pi * G * t**3)


def dp_eff_dt(t: ArrayLike, p: TrackerParams, G: float = 1.0) -> NDArray[np.float64]:
    """d p_eff/dt = f_v (2 + 2 f_v - f_v^2) / (12 pi G t^3)   (derived).

    Differentiating the p_eff closed form with df_v/dt = f_v(1-f_v)/t.
    """
    t = _t(t)
    f = fv(t, p)
    return f * (2.0 + 2.0 * f - f**2) / (12.0 * np.pi * G * t**3)


def w_eff(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Effective equation of state w_eff := p_eff / rho_eff.

    Definition: [GM] Sec. 4 text (p. 13). Tracker closed form (derived):
    w_eff = -(4 - f_v) / (8 + f_v); G-independent. Limits: -1/2 as
    f_v -> 0 (early times), -(4-fv0)/(8+fv0) today.
    """
    t = _t(t)
    f = fv(t, p)
    return -(4.0 - f) / (8.0 + f)


def cs2_eff(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Effective squared sound speed c^2_{s,eff} := (dp_eff/dt)/(drho_eff/dt).

    Definition: [GM] Sec. 4 text (p. 13). Tracker closed form (derived):
    c^2_{s,eff} = -(2 + 2 f_v - f_v^2) / (2 + f_v)^2; G-independent.
    Limits: -1/2 as f_v -> 0.
    NOTE: intentionally differs from the upstream notebook's `cs2Eff`
    and from [GM] Fig. 1 (right panel), both affected by the upstream
    dQDdt defect — documented deviation (D2), see module docstring.
    """
    t = _t(t)
    f = fv(t, p)
    return -(2.0 + 2.0 * f - f**2) / (2.0 + f) ** 2


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


# --------------------------------------------------------------------------
# Observables / auxiliary relations
# --------------------------------------------------------------------------

def gamma_w(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Wall-observer lapse gamma_w(t) = 1 + f_v(t)/2.

    [GM] text p. 25 ("gamma_w(t) = 1 + f_v(t)/2"); [W09] Eq. (B7)
    (written there as (2 + f_v)/2).
    """
    return 1.0 + fv(t, p) / 2.0


def redshift(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Observed (dressed) cosmological redshift z(t) of the tracker.

    1 + z = (2 + f_v) f_v^(1/3) / (3 f_{v,0}^(1/3) HD0 t)
    [W09] Eq. (38); equivalent to [GM] text p. 25,
    1 + z = a_{w,0}/a_w = gamma_w (a_D/a_{w,0})^{-1}.
    """
    t = _t(t)
    f = fv(t, p)
    return (2.0 + f) * np.cbrt(f) / (3.0 * np.cbrt(p.fv0) * p.HD0 * t) - 1.0
