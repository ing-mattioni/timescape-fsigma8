"""Independent equation-residual diagnostics for the comoving system.

Only the Lambda=0 Timescape specialisation is implemented.  This avoids
silently adjudicating the unrelated Lambda-coefficient typos identified in
the Phase 1C-A audit.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations.systems import comoving_matrix


def _vector(values: ArrayLike, name: str) -> NDArray[np.float64]:
    vector = np.asarray(values, dtype=np.float64)
    if vector.shape != (3,):
        raise ValueError(f"{name} must have shape (3,), got {vector.shape}")
    if not np.all(np.isfinite(vector)):
        raise ValueError(f"{name} must contain only finite values")
    return vector


def _theta_dot(t: float, params: TrackerParams) -> float:
    """Return ``dTheta/dt`` for the tracker background.

    Derived by differentiating ``Theta=(2+f_v)/t``, which combines
    Eq. (3.6) and Eqs. (5.5)-(5.6) of arXiv:2511.17160v2 (equivalently
    Eq. (B6) of arXiv:0909.0749), using the Phase 1B derivative of (5.6).
    """
    f_v = float(bg.fv(t, params))
    return -(2.0 + f_v**2) / t**2


def _w_eff_dot(t: float, params: TrackerParams) -> float:
    """Return ``dw_eff/dt`` from effective-fluid conservation.

    The identity ``wdot=-Theta(1+w)(cs2-w)`` follows from Eq. (3.17) of
    arXiv:2511.17160v2 and the Sec. 4 definition
    ``cs2=dp_eff/dt / (drho_eff/dt)``.  The sound speed here is the
    independently validated, D2-free Phase 1B quantity.
    """
    theta = float(bg.Theta(t, params))
    w_eff = float(bg.w_eff(t, params))
    cs2_eff = float(bg.cs2_eff(t, params))
    return -theta * (1.0 + w_eff) * (cs2_eff - w_eff)


def comoving_second_derivative(
    t: float,
    state: ArrayLike,
    *,
    params: TrackerParams,
    G: float,
) -> NDArray[np.float64]:
    """Return the exact second derivative implied by Eqs. (4.21)-(4.23).

    For ``ydot=A(t)y``, this evaluates ``yddot=Adot*y+A*ydot``.  Every
    entry of ``A`` is Eqs. (4.21)-(4.23) of arXiv:2511.17160v2; its time
    derivative uses background conservation Eq. (3.17), dust conservation
    Eq. (3.10), and the tracker expansion from Eqs. (5.5)-(5.6).
    """
    if G <= 0.0:
        raise ValueError(f"G must be positive, got {G}")
    y = _vector(state, "state")
    matrix = comoving_matrix(t, params=params, G=G)
    theta = float(bg.Theta(t, params))
    theta_dot = _theta_dot(t, params)
    w_eff = float(bg.w_eff(t, params))
    w_eff_dot = _w_eff_dot(t, params)
    four_pi_G = 4.0 * np.pi * G
    matrix_dot = np.array(
        [
            [0.0, 0.0, 0.0],
            [
                -four_pi_G * float(bg.drho_d_dt(t, params, G)),
                -(2.0 / 3.0) * theta_dot,
                -four_pi_G * float(bg.drho_eff_dt(t, params, G)),
            ],
            [0.0, -w_eff_dot, w_eff_dot * theta + w_eff * theta_dot],
        ],
        dtype=np.float64,
    )
    state_dot = matrix @ y
    return matrix_dot @ y + matrix @ state_dot


@dataclass(frozen=True)
class ComovingResiduals:
    """Residuals of Eqs. (4.24), (4.25), and (4.26), in that order."""

    eq_4_24: float
    eq_4_25: float
    eq_4_26: float


def comoving_second_order_residuals(
    t: float,
    state: ArrayLike,
    state_dot: ArrayLike,
    state_ddot: ArrayLike,
    *,
    params: TrackerParams,
    G: float,
) -> ComovingResiduals:
    """Evaluate the Lambda=0 forms of [GM] Eqs. (4.24)-(4.26).

    The return values are left-hand side minus right-hand side for
    Eqs. (4.24) and (4.25), and the full left-hand side for Eq. (4.26),
    all from arXiv:2511.17160v2.  No barotropic closure is involved.
    """
    if G <= 0.0:
        raise ValueError(f"G must be positive, got {G}")
    y = _vector(state, "state")
    y_dot = _vector(state_dot, "state_dot")
    y_ddot = _vector(state_ddot, "state_ddot")
    delta_d, expansion_gradient, delta_eff = y
    delta_d_dot, expansion_gradient_dot, delta_eff_dot = y_dot
    delta_d_ddot, expansion_gradient_ddot, delta_eff_ddot = y_ddot

    theta = float(bg.Theta(t, params))
    rho_d = float(bg.rho_d(t, params, G))
    rho_eff = float(bg.rho_eff(t, params, G))
    w_eff = float(bg.w_eff(t, params))
    cs2_eff = float(bg.cs2_eff(t, params))
    four_pi_G = 4.0 * np.pi * G

    residual_4_24 = (
        delta_d_ddot
        + (2.0 / 3.0) * theta * delta_d_dot
        - four_pi_G * rho_d * delta_d
        - four_pi_G * rho_eff * delta_eff
    )

    coefficient_4_25 = (
        (cs2_eff - (4.0 / 3.0) * w_eff) * theta**2
        + four_pi_G * rho_d * w_eff
        - four_pi_G * rho_eff * (1.0 - 3.0 * w_eff**2)
    )
    residual_4_25 = (
        delta_eff_ddot
        + ((2.0 / 3.0) + cs2_eff - 2.0 * w_eff) * theta * delta_eff_dot
        + coefficient_4_25 * delta_eff
        - four_pi_G * rho_d * (1.0 + w_eff) * delta_d
    )

    coefficient_4_26 = (
        (4.0 / 9.0) * theta**2
        - (20.0 * np.pi * G / 3.0) * rho_d
        - (four_pi_G / 3.0) * rho_eff * (5.0 + 9.0 * w_eff)
    )
    residual_4_26 = (
        expansion_gradient_ddot
        + (5.0 / 3.0) * theta * expansion_gradient_dot
        + coefficient_4_26 * expansion_gradient
    )
    return ComovingResiduals(
        eq_4_24=float(residual_4_24),
        eq_4_25=float(residual_4_25),
        eq_4_26=float(residual_4_26),
    )
