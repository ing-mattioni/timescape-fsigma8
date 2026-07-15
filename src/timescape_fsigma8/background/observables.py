"""Wall-observer (dressed) quantities and observables.

The timescape phenomenology distinguishes the volume-average (bare) frame
— time t, scale factor a_D, Hubble rate H_D — from the wall-observer
(dressed) frame — proper time tau_w, scale factor a_w, Hubble rate H.
The lapse gamma_w = dt/dtau_w connects them. References:
[GM] = arXiv:2511.17160v2 (Eq. (5.4) and text pp. 24-25);
[W09] = arXiv:0909.0749 (Eqs. (28), (38), (B7), (B8), (B12)).

`gamma_w` and `redshift` are verbatim from the pre-split module
(equivalence pinned in tests/test_refactor_equivalence.py); the wall/
dressed quantities `dgamma_w_dt`, `a_w`, `dtau_w_dt`, `tau_w`, `H_dressed`
are additions of the Phase 1B gap-closure task, validated in
tests/test_wall_observables.py.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

from timescape_fsigma8.background.parameters import TrackerParams, _t
from timescape_fsigma8.background.tracker import a_D, fv


def gamma_w(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Wall-observer lapse gamma_w(t) = 1 + f_v(t)/2.

    [GM] text p. 25 ("gamma_w(t) = 1 + f_v(t)/2"); [W09] Eq. (B7)
    (written there as (2 + f_v)/2).
    """
    return 1.0 + fv(t, p) / 2.0


def dgamma_w_dt(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """d gamma_w/dt = (1/2) df_v/dt = f_v (1 - f_v) / (2 t)   (derived).

    Differentiating gamma_w = 1 + f_v/2 ([GM] p. 25; [W09] (B7)) with the
    tracker identity df_v/dt = f_v(1-f_v)/t. Validated against numerical
    differentiation in tests.
    """
    t = _t(t)
    f = fv(t, p)
    return f * (1.0 - f) / (2.0 * t)


def a_w(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Dressed (wall-geometry) scale factor a_w(t) = a_D(t) / gamma_w(t).

    [GM] Eq. (5.4), a_w = gamma_w^{-1} a_D. With a_D normalised via
    a_{D,0} = 1 + fv0/2 = gamma_w(t0) (TrackerParams.aD0), a_w(t0) = 1
    exactly, i.e. a_w is in units of a_{w,0}.
    """
    return a_D(t, p) / gamma_w(t, p)


def dtau_w_dt(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Wall proper-time rate dtau_w/dt = 1/gamma_w(t) = 2/(2 + f_v(t)).

    From the definition of the lapse, gamma_w := dt/dtau_w
    ([GM] text after Eq. (5.4); [W09] Sec. II).
    """
    return 1.0 / gamma_w(t, p)


def tau_w(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Wall-observer proper time tau_w(t), with tau_w(0) = 0.

    tau_w(t) = (2/3) t + [2 (2+fv0)(1-fv0) / (27 fv0 HD0)]
                       * ln(1 + 9 fv0 HD0 t / (2 (2+fv0)(1-fv0)))
    [W09] Eq. (B12). Derivation (validated in tests): integrate
    dtau_w/dt = 2/(2 + f_v) with the tracker f_v of [GM] (5.6); the
    integration constant is fixed by tau_w(0) = 0. Implemented with
    log1p, exact at t = 0. Domain t >= 0 (sole function admitting t = 0).
    """
    t = _t(t, allow_zero=True)
    b = (2.0 + p.fv0) * (1.0 - p.fv0)
    return (2.0 / 3.0) * t + (2.0 * b / (27.0 * p.fv0 * p.HD0)) * np.log1p(
        9.0 * p.fv0 * p.HD0 * t / (2.0 * b))


def H_dressed(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Dressed Hubble parameter H(t) = gamma_w H_D - dgamma_w/dt.

    [W09] Eq. (28) (equivalently (B8)): the expansion rate a wall
    observer infers, H = (1/a_w) da_w/dtau_w. Tracker closed form
    (derived): H = (4 + f_v + 4 f_v^2) / (6 t). Cross-checked in tests
    against the defining combination gamma_w H_D - dgamma_w/dt, against
    [W09] (B8) in the form H = (4 f_v^2 + f_v + 4) H_D / (2 (2 + f_v)),
    and against (gamma_w / a_w) da_w/dt with numerical da_w/dt.
    H_dressed(t0) equals TrackerParams.H0_dressed exactly.
    """
    t = _t(t)
    f = fv(t, p)
    return (4.0 + f + 4.0 * f**2) / (6.0 * t)


def redshift(t: ArrayLike, p: TrackerParams) -> NDArray[np.float64]:
    """Observed (dressed) cosmological redshift z(t) of the tracker.

    1 + z = (2 + f_v) f_v^(1/3) / (3 f_{v,0}^(1/3) HD0 t)
    [W09] Eq. (38); equivalent to [GM] text p. 25,
    1 + z = a_{w,0}/a_w = gamma_w (a_D/a_{w,0})^{-1}, i.e. 1 + z = 1/a_w
    with our normalisation a_w(t0) = 1 (tested identity).
    """
    t = _t(t)
    f = fv(t, p)
    return (2.0 + f) * np.cbrt(f) / (3.0 * np.cbrt(p.fv0) * p.HD0 * t) - 1.0
