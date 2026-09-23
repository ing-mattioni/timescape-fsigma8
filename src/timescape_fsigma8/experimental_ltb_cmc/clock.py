"""External tracker-clock adapter, never a source or fitting target for CMC.

W09 = Wiltshire, arXiv:0909.0749v2, Eqs. (B2), (B3), (B6), (B7),
(B12), translated to the user's b via f=t/(t+b). No use of a homonymous
paper parameter or the project's differently parametrized frozen API.
The CMC core neither imports this module nor knows t, b, C, H_D or rho_D.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from .geometry import (Array, LTBModel, LTBDomainError, LTBNumericalError,
                       Numerics, dimensional, scalar)
from .solver import CMCSolution, _readonly, solve_cmc


@dataclass(frozen=True)
class ClockComparison:
    """Instantaneous residuals only; no existence/matching boolean.

    t,b,C,tau_w use solution.model.length_unit (= time unit, c=1);
    N,ell are dimensionless; H values inverse length; rho values
    mass/length**3; Q_ell,R_ell inverse length squared. C is external.
    gamma in solution is dust/section tilt, not the tracker wall gamma.
    """

    solution: CMCSolution
    t: float
    b: float
    C: float
    f: float
    alpha_W: float
    tau_w: float
    N: Array
    ell: Array
    H_Omega: float
    rho_ell: float
    Q_ell: float
    R_ell: float
    H_D: float
    rho_D: float
    H_residual: float
    log_density_ratio: float


def tracker_clock(t: float, b: float, C: float) -> tuple[float, float, float, float]:
    """Return (f, alpha_W, tau_w, s_c); same supplied unit for t,b,C.

    W09 (B2), (B7), (B12), with tau_w(0)=0 and s_c=tau_w+C.
    The additive offset and selection of this clock are external closure.
    Branches avoid t+b overflow and loss of the small-x clock term.
    """
    t, b, C = scalar(t, "t"), scalar(b, "b"), scalar(C, "C")
    if t <= 0 or b <= 0:
        raise LTBDomainError("Require t>0 and b>0 in one common unit")
    if t <= b:
        q = t / b
        z = 1.5 * q
        ratio = math.log1p(z) / z if z else 1.0
        f = q / (1 + q)
        tau = t * (2 / 3 + ratio / 3)
    else:
        q = b / t
        logz = math.log(1.5) + math.log(t) - math.log(b)
        logterm = logz + math.log1p(math.exp(-logz))
        f = 1 / (1 + q)
        tau = t * (2 / 3 + (2 / 9) * q * logterm)
    s_c = tau + C
    if not math.isfinite(s_c) or tau < np.finfo(float).tiny:
        raise LTBNumericalError("Selected clock not representable in normal binary64")
    if s_c <= 0:
        raise LTBDomainError("Selected central age tau_w+C must be positive")
    # Reject cancellation-dominated age selection; this is an engineering
    # resolution guard, not an error enclosure or a physical bound.
    if s_c <= 64 * np.finfo(float).eps * max(tau, abs(C)):
        raise LTBNumericalError("Selected positive age unresolved after offset cancellation")
    return f, 2 / (2 + f), tau, s_c


def solve_at_tracker_clock(t: float, b: float, C: float, model: LTBModel,
                           numerics: Numerics = Numerics()) -> ClockComparison:
    """Select s_c, solve geometry, then compute non-fitting residuals.

    W09 (B3),(B6) give H_D and rho_D; BMR arXiv:1912.04213v2
    (4.12),(4.18),(4.20),(E.2) give the clock rescalings. ell=N/gamma
    is not the ADM lapse; N=alpha_W*N_c is the normal lapse here.
    """
    f, alpha, tau, s_c = tracker_clock(t, b, C)
    solution = solve_cmc(s_c, model, numerics)
    a = solution.averages
    H_D = dimensional((2 + f) / 3, t, -1)
    # Evaluate log(1-f) independently; f may legitimately round to one.
    log_beta = (-math.log1p(t / b) if t <= b else
                math.log(b) - math.log(t) - math.log1p(b / t))
    log_rho = log_beta - math.log(6 * math.pi) - math.log(model.G) - 2 * math.log(t)
    if not math.log(np.finfo(float).tiny) <= log_rho <= math.log(np.finfo(float).max):
        raise LTBNumericalError("Tracker density not representable in normal binary64")
    rho_D = math.exp(log_rho)
    H = dimensional(a.J, alpha, 1)
    logratio = log_rho + math.log(a.V) - math.log(a.M_rest)
    return ClockComparison(solution, float(t), float(b), float(C), f, alpha, tau,
                           _readonly(dimensional(solution.N_c, alpha, 1)),
                           _readonly(dimensional(solution.lambda_, alpha, 1)), H,
                           dimensional(a.rho_lambda, alpha, 2),
                           dimensional(a.Q_lambda, alpha, 2), dimensional(a.R_lambda, alpha, 2),
                           H_D, rho_D, H - H_D, logratio)
