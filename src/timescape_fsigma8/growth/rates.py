"""Exact analytic growth rates and non-logarithmic derivatives (Phase 1D-B).

Primary formulas (1D-A audit Secs. 7-8, derivation chains D3-D4; [GM]
(4.14) with the validated Phase 1B tracker background of [W09]):

    Z = -dDelta_d/dt                       [GM (4.14)]
    d ln a_D/dt = Theta/3                  [GM (3.6); Phase 1B tracker]
    f_bare  = -3 Z / (Theta Delta_d)                       (exact)
    f_dressed = f_bare (2+f_v)^2/(4+f_v+4f_v^2)            (exact tracker)
    dDelta_d/d ln a_D    = -3 Z / Theta                     (finite always)
    dDelta_d/d ln a_obs  = (-3 Z / Theta)(2+f_v)^2/(4+f_v+4f_v^2)

with a_obs = 1/(1+z_dressed) = a_w/a_w0 ([GM] p. 25; [W09] (38); 1D-A
Sec. 7).  No finite differences, gradients, splines, or fits appear here;
the state vector already contains the exact derivative.

Crossing policy (1D-A Sec. 8): at amplitude roots the logarithmic rates are
undefined — they are returned as NaN under an explicit near-zero mask with
crossing metadata carried separately; no silent +/-inf and no interpolated
finite value.  The non-logarithmic derivatives remain finite there.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams


def _frozen(values) -> NDArray[np.float64]:
    out = np.array(values, dtype=np.float64)
    out.flags.writeable = False
    return out


def dressed_chain_factor(t: ArrayLike, params: TrackerParams) -> NDArray[np.float64]:
    """Exact tracker conversion f_dressed/f_bare = (2+f_v)^2/(4+f_v+4f_v^2).

    1D-A Sec. 7 (equation chain D3, sympy checks S3b-S3f): equals
    gamma_w H_D / H_dressed with the validated Phase 1B forms
    gamma_w = 1+f_v/2 ([GM] p. 25; [W09] (B7)),
    H_D = (2+f_v)/(3t) ([W09] (B6)), and
    H_dressed = (4+f_v+4f_v^2)/(6t) ([W09] (28)/(B8)).
    """
    f_v = bg.fv(t, params)
    return _frozen((2.0 + f_v) ** 2 / (4.0 + f_v + 4.0 * f_v**2))


def amplitude_near_zero_mask(
    amplitude: NDArray[np.float64], *, near_zero_rel_floor: float
) -> NDArray[np.bool_]:
    """Explicit, scale-free near-zero policy mask.

    A sample is near zero iff it is exactly zero or its magnitude is at or
    below ``near_zero_rel_floor`` times the larger neighbouring sample
    magnitude.  The neighbour-local scale makes the policy valid across
    the many-decade dynamic range of barotropic trajectories: a sample
    sitting essentially on a crossing is tiny relative to its neighbours,
    whereas a uniformly small early-time epoch is not flagged.  A sampled
    value that is zero only through rounding is therefore flagged and is
    never treated as a solver-independent root by itself.
    """
    mag = np.abs(np.asarray(amplitude, dtype=np.float64))
    if mag.size < 2:
        raise ValueError("near-zero policy needs at least 2 samples")
    left = np.empty_like(mag)
    right = np.empty_like(mag)
    left[0], left[1:] = mag[1], mag[:-1]
    right[-1], right[:-1] = mag[-2], mag[1:]
    local_scale = np.maximum(left, right)
    mask = (mag == 0.0) | (mag <= near_zero_rel_floor * local_scale)
    mask.flags.writeable = False
    return mask


def f_bare(
    delta_d: NDArray[np.float64],
    z_expansion: NDArray[np.float64],
    t: NDArray[np.float64],
    params: TrackerParams,
    *,
    near_zero_rel_floor: float,
) -> NDArray[np.float64]:
    """Exact bare logarithmic growth rate f_bare = -3Z/(Theta Delta_d).

    [GM] (4.14) + tracker Theta ([W09] (B6)); 1D-A chain D4, sympy S4.
    Vectorised; NaN (never +/-inf) where |Delta_d| falls under the explicit
    near-zero floor, since d ln D/d ln a_D is undefined at amplitude roots.
    Identical for Delta_d and the mapped delta_m coefficient because the
    constant harmonic factor cancels from the logarithmic derivative.
    """
    delta_d = np.asarray(delta_d, dtype=np.float64)
    z_expansion = np.asarray(z_expansion, dtype=np.float64)
    theta = np.asarray(bg.Theta(t, params), dtype=np.float64)
    mask = amplitude_near_zero_mask(
        delta_d, near_zero_rel_floor=near_zero_rel_floor
    )
    out = np.full(delta_d.shape, np.nan, dtype=np.float64)
    ok = ~mask
    out[ok] = -3.0 * z_expansion[ok] / (theta[ok] * delta_d[ok])
    out.flags.writeable = False
    return out


def f_dressed(
    delta_d: NDArray[np.float64],
    z_expansion: NDArray[np.float64],
    t: NDArray[np.float64],
    params: TrackerParams,
    *,
    near_zero_rel_floor: float,
) -> NDArray[np.float64]:
    """Exact dressed rate f_dressed = f_bare (2+f_v)^2/(4+f_v+4f_v^2).

    Dressed growth is with respect to a_obs = 1/(1+z_dressed) = a_w/a_w0
    ([GM] p. 25; [W09] (38); 1D-A Sec. 7, chain D3).  Same NaN policy as
    ``f_bare`` at amplitude roots.
    """
    return _frozen(
        f_bare(
            delta_d,
            z_expansion,
            t,
            params,
            near_zero_rel_floor=near_zero_rel_floor,
        )
        * dressed_chain_factor(t, params)
    )


def dDelta_d_dln_aD(
    z_expansion: NDArray[np.float64],
    t: NDArray[np.float64],
    params: TrackerParams,
) -> NDArray[np.float64]:
    """Non-logarithmic bare derivative dDelta_d/d ln a_D = -3Z/Theta.

    Finite through every Delta_d crossing (1D-A Sec. 8, chain D4).
    """
    theta = np.asarray(bg.Theta(t, params), dtype=np.float64)
    return _frozen(-3.0 * np.asarray(z_expansion, dtype=np.float64) / theta)


def dDelta_d_dln_aobs(
    z_expansion: NDArray[np.float64],
    t: NDArray[np.float64],
    params: TrackerParams,
) -> NDArray[np.float64]:
    """Non-logarithmic dressed derivative: -3Z/Theta times the chain factor."""
    return _frozen(
        dDelta_d_dln_aD(z_expansion, t, params) * dressed_chain_factor(t, params)
    )


@dataclass(frozen=True)
class GrowthRates:
    """Immutable analytic rates of one history, with the explicit mask.

    ``near_zero_mask`` marks samples where |Delta_d| is under the explicit
    near-zero floor; there the logarithmic rates are NaN by policy while
    the non-logarithmic derivatives remain finite.
    """

    f_bare: NDArray[np.float64]
    f_dressed: NDArray[np.float64]
    dDelta_d_dln_aD: NDArray[np.float64]
    dDelta_d_dln_aobs: NDArray[np.float64]
    chain_factor: NDArray[np.float64]
    near_zero_mask: NDArray[np.bool_]
    near_zero_rel_floor: float


def evaluate_rates(
    *,
    delta_d: NDArray[np.float64],
    z_expansion: NDArray[np.float64],
    t: NDArray[np.float64],
    params: TrackerParams,
    near_zero_rel_floor: float,
) -> GrowthRates:
    """Evaluate every analytic rate and derivative for one sampled history."""
    return GrowthRates(
        f_bare=f_bare(
            delta_d, z_expansion, t, params, near_zero_rel_floor=near_zero_rel_floor
        ),
        f_dressed=f_dressed(
            delta_d, z_expansion, t, params, near_zero_rel_floor=near_zero_rel_floor
        ),
        dDelta_d_dln_aD=dDelta_d_dln_aD(z_expansion, t, params),
        dDelta_d_dln_aobs=dDelta_d_dln_aobs(z_expansion, t, params),
        chain_factor=dressed_chain_factor(t, params),
        near_zero_mask=amplitude_near_zero_mask(
            delta_d, near_zero_rel_floor=near_zero_rel_floor
        ),
        near_zero_rel_floor=near_zero_rel_floor,
    )
