"""Effective (backreaction + curvature) fluid, [GM] Eqs. (3.12)-(3.13).

Formulas verbatim from the pre-split module (equivalence pinned in
tests/test_refactor_equivalence.py). References: [GM] = arXiv:2511.17160v2;
[W09] = arXiv:0909.0749. Deviation (D2) affects `cs2_eff` relative to the
upstream notebook and published Fig. 1 — see the package docstring.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

from timescape_fsigma8.background.parameters import TrackerParams, _t
from timescape_fsigma8.background.tracker import fv


def rho_eff(t: ArrayLike, p: TrackerParams, G: float) -> NDArray[np.float64]:
    """Effective fluid energy density rho_eff = -(Q_D + W_D) / (16 pi G).

    [GM] Eq. (3.12) with W_D = <R>_D (K_D = 0). Tracker closed form
    (derived): rho_eff = f_v (8 + f_v) / (24 pi G t^2).
    """
    t = _t(t)
    f = fv(t, p)
    return f * (8.0 + f) / (24.0 * np.pi * G * t**2)


def p_eff(t: ArrayLike, p: TrackerParams, G: float) -> NDArray[np.float64]:
    """Effective fluid pressure p_eff = -Q_D/(16 pi G) + W_D/(48 pi G).

    [GM] Eq. (3.13) with W_D = <R>_D (K_D = 0). Tracker closed form
    (derived): p_eff = -f_v (4 - f_v) / (24 pi G t^2).
    """
    t = _t(t)
    f = fv(t, p)
    return -f * (4.0 - f) / (24.0 * np.pi * G * t**2)


def drho_eff_dt(t: ArrayLike, p: TrackerParams, G: float) -> NDArray[np.float64]:
    """d rho_eff/dt = -f_v (2 + f_v)^2 / (12 pi G t^3)   (derived).

    Differentiating the rho_eff closed form with df_v/dt = f_v(1-f_v)/t.
    Equals -3 H_D (rho_eff + p_eff) exactly ([GM] Eq. (3.17)).
    """
    t = _t(t)
    f = fv(t, p)
    return -f * (2.0 + f) ** 2 / (12.0 * np.pi * G * t**3)


def dp_eff_dt(t: ArrayLike, p: TrackerParams, G: float) -> NDArray[np.float64]:
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
    dQDdt defect — documented deviation (D2), see the package docstring.
    """
    t = _t(t)
    f = fv(t, p)
    return -(2.0 + 2.0 * f - f**2) / (2.0 + f) ** 2
