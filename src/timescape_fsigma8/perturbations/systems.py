"""Pure right-hand sides for the clean Timescape perturbation systems.

References use [GM] for Galoppo & Mourier, JCAP 02 (2026) 066,
arXiv:2511.17160v2.  The independent variable is Buchert volume-average
time ``t`` in the same unit as ``1 / TrackerParams.HD0``.  State vectors are

``meszaros``: ``(Delta_d, dDelta_d/dt)``;
``comoving``: ``(Delta_d, Z, Delta_eff)``.

The sign convention is ``Z = -dDelta_d/dt`` ([GM] Eq. (4.21)).
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams


FloatArray = NDArray[np.float64]


def _state(y: ArrayLike, size: int, system: str) -> FloatArray:
    """Validate a one-dimensional perturbation state (numerical validation)."""
    state = np.asarray(y, dtype=np.float64)
    if state.shape != (size,):
        raise ValueError(f"{system} state must have shape ({size},), got {state.shape}")
    if not np.all(np.isfinite(state)):
        raise ValueError(f"{system} state must contain only finite values")
    return state


def meszaros_rhs(
    t: float,
    y: ArrayLike,
    *,
    params: TrackerParams,
    G: float,
) -> FloatArray:
    """Return the effective-Mészáros first-order RHS.

    Implements

        d²Delta_d/dt² + (2/3) Theta dDelta_d/dt
        - 4 pi G rho_d Delta_d = 0,

    Eq. (4.27) of arXiv:2511.17160v2, rewritten as a two-component
    first-order system.  [GM] Sec. 5.1.1 states that this approximation is
    formally inapplicable to Timescape and uses it only for comparison.
    """
    if G <= 0.0:
        raise ValueError(f"G must be positive, got {G}")
    delta_d, delta_d_dot = _state(y, 2, "meszaros")
    theta = float(bg.Theta(t, params))
    rho_d = float(bg.rho_d(t, params, G))
    delta_d_ddot = 4.0 * np.pi * G * rho_d * delta_d - (2.0 / 3.0) * theta * delta_d_dot
    return np.array([delta_d_dot, delta_d_ddot], dtype=np.float64)


def comoving_matrix(t: float, *, params: TrackerParams, G: float) -> FloatArray:
    """Return the comoving-closure coefficient matrix.

    This is the first-order system of Eqs. (4.21)-(4.23) of
    arXiv:2511.17160v2 after imposing the comoving closure
    ``V_eff = 0`` of Eq. (4.20).  The matrix acts on
    ``(Delta_d, Z, Delta_eff)`` and contains no sound speed, wavenumber,
    D2-affected quantity, or D3 branch.
    """
    if G <= 0.0:
        raise ValueError(f"G must be positive, got {G}")
    theta = float(bg.Theta(t, params))
    rho_d = float(bg.rho_d(t, params, G))
    rho_eff = float(bg.rho_eff(t, params, G))
    w_eff = float(bg.w_eff(t, params))
    four_pi_G = 4.0 * np.pi * G
    return np.array(
        [
            [0.0, -1.0, 0.0],
            [-four_pi_G * rho_d, -(2.0 / 3.0) * theta, -four_pi_G * rho_eff],
            [0.0, -(1.0 + w_eff), w_eff * theta],
        ],
        dtype=np.float64,
    )


def comoving_rhs(
    t: float,
    y: ArrayLike,
    *,
    params: TrackerParams,
    G: float,
) -> FloatArray:
    """Return ``d(Delta_d, Z, Delta_eff)/dt`` for the comoving closure.

    Implements Eqs. (4.21)-(4.23) of arXiv:2511.17160v2 with the closure
    of Eq. (4.20).  In particular, the first component enforces the exact
    convention ``Z = -dDelta_d/dt`` from Eq. (4.21).
    """
    state = _state(y, 3, "comoving")
    return comoving_matrix(t, params=params, G=G) @ state
