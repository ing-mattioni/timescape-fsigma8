"""External tracker-clock adapter, never a source or fitting target for CMC.

W09 = Wiltshire, arXiv:0909.0749v2, Eqs. (B2), (B3), (B6), (B7),
(B12), translated to the user's b via f=t/(t+b). No use of a homonymous
paper parameter or the project's differently parametrized frozen API.
The CMC core neither imports this module nor knows t, b, C, H_D or rho_D.

The evolution adapter (``solve_evolution_at_tracker_clock``) adds the
single-age tracker comparison of the section-family evolution after the
geometric calculation.  Its differentiated clock relations are conditional
research derivations of the user contract, not published equations.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from .evolution import CMCEvolution, solve_cmc_evolution
from .geometry import (Array, LTBModel, LTBDomainError, LTBNumericalError,
                       Numerics, dimensional, finite, scalar)
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
    return _comparison(solution, t, b, C, f, alpha, tau)


def _log_one_minus_f(t: float, b: float) -> float:
    """log(1-f) = log(b/(t+b)), evaluated independently of f."""
    return (-math.log1p(t / b) if t <= b else
            math.log(b) - math.log(t) - math.log1p(b / t))


def _comparison(solution: CMCSolution, t: float, b: float, C: float, f: float,
                alpha: float, tau: float) -> ClockComparison:
    """Preexisting instantaneous comparison for an already accepted solution."""
    model = solution.model
    a = solution.averages
    H_D = dimensional((2 + f) / 3, t, -1)
    # Evaluate log(1-f) independently; f may legitimately round to one.
    log_beta = _log_one_minus_f(t, b)
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


@dataclass(frozen=True)
class EvolutionClockComparison:
    """Instantaneous tracker comparison of the section-family evolution.

    ``comparison`` holds the preexisting quantities for the SAME accepted
    solution (e_H = H_residual, e_rho = log_density_ratio).  Units (c=1):
    alpha_dot and J_D inverse length; P_ell, H_dot, H_D_dot and
    H_dot_residual inverse length squared; q_required, q_residual
    dimensionless.  These are single-age interpretation tools: a small
    q_residual at one instant does not show compatibility over an interval.
    There is no embedding, existence or all-time compatibility flag.
    """

    comparison: ClockComparison
    evolution: CMCEvolution
    alpha_dot: float
    P_ell: float
    H_dot: float
    H_D_dot: float
    H_dot_residual: float
    J_D: float
    q_required: float
    q_residual: float


def _signed_product(*factors: float) -> float:
    """Product via logarithms; zero if any factor is zero, else the package's
    normal-binary64 representability policy (no avoidable overflow, no
    silently lost nonzero)."""
    if any(factor == 0 for factor in factors):
        return 0.0
    sign = -1.0 if sum(factor < 0 for factor in factors) % 2 else 1.0
    log_value = sum(math.log(abs(factor)) for factor in factors)
    limits = np.finfo(float)
    if not math.log(limits.tiny) <= log_value <= math.log(limits.max):
        raise LTBNumericalError("Clock evolution term outside normal binary64 range")
    return sign * math.exp(log_value)


def solve_evolution_at_tracker_clock(t: float, b: float, C: float, model: LTBModel,
                                     numerics: Numerics = Numerics()
                                     ) -> EvolutionClockComparison:
    """Select s_c=tau_w+C, solve the geometric evolution, then compare.

    alpha=2/(2+f), f=t/(t+b), alpha_dot=-2*b/(3*t+2*b)**2 (W09 (B2),(B7)
    translated to b).  With H_Omega=alpha*J and ds_c/dt=alpha:
    H_dot=alpha_dot*J+alpha**2*J_s, P_ell=alpha**2*P_lambda+3*alpha_dot*J,
    H_D_dot=-(2+f**2)/(3*t**2), J_D=H_D/alpha,
    q_required=(1-f)*(2-5*f)/(2+f)**2, q_residual=q_c-q_required.
    The geometric solve never receives t, b or C; nothing is fed back.
    """
    f, alpha, tau, s_c = tracker_clock(t, b, C)
    evolution = solve_cmc_evolution(s_c, model, numerics)
    comparison = _comparison(evolution.solution, t, b, C, f, alpha, tau)
    t, b = float(t), float(b)
    # Scaled clock variables: no overflow in squares, 1-f kept from b directly.
    scale = max(t, b)
    tt, bb = t / scale, b / scale
    three_t_plus_two_b = 3 * tt + 2 * bb  # in units of scale; >= 2
    log_sum = math.log(scale) + math.log(three_t_plus_two_b)
    log_alpha_dot = math.log(2) + math.log(b) - 2 * log_sum
    limits = np.finfo(float)
    if not math.log(limits.tiny) <= log_alpha_dot <= math.log(limits.max):
        raise LTBNumericalError("alpha_dot outside normal binary64 range")
    alpha_dot = -math.exp(log_alpha_dot)
    J = evolution.solution.averages.J
    H_dot = (_signed_product(alpha_dot, J)
             + _signed_product(alpha, alpha, evolution.J_s))
    P_ell = (_signed_product(alpha, alpha, evolution.P_lambda)
             + _signed_product(3.0, alpha_dot, J))
    H_D_dot = dimensional(-(2 + f**2) / 3, t, -2)
    J_D = dimensional((2 + f)**2 / 6, t, -1)
    # q_required=(1-f)(2-5f)/(2+f)**2 with 1-f=b/(t+b), 2-5f=(2b-3t)/(t+b),
    # 2+f=(3t+2b)/(t+b); log(1-f) is evaluated independently of f.
    numerator = 2 * bb - 3 * tt
    if numerator == 0:
        q_required = 0.0
    else:
        log_q = (_log_one_minus_f(t, b) + math.log(abs(numerator))
                 - math.log(tt + bb) - 2 * (math.log(three_t_plus_two_b) - math.log(tt + bb)))
        if not math.log(limits.tiny) <= log_q <= math.log(limits.max):
            raise LTBNumericalError("q_required outside normal binary64 range")
        q_required = math.copysign(math.exp(log_q), numerator)
    q_residual = evolution.q_c - q_required
    H_dot_residual = H_dot - H_D_dot
    finite(alpha_dot, H_dot, P_ell, H_D_dot, J_D, q_required, q_residual, H_dot_residual)
    return EvolutionClockComparison(comparison, evolution, alpha_dot, P_ell, H_dot,
                                    H_D_dot, H_dot_residual, J_D, q_required,
                                    q_residual)
