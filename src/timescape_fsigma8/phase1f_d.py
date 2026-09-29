"""Conditional scalar necessary-bound diagnostic, positive-core Phase 1F-D.

Sources: BMR = Buchert--Mourier--Roy, arXiv:1912.04213v2, Eqs. (4.9),
(4.12), (4.14), (E.2); W09 = Wiltshire, arXiv:0909.0749v2, Eqs. (B2),
(B6), (B7), (B12). The bound is derived from these equations ONLY with
the additional, user-authorized branch assumptions; it is not a published
Timescape embedding theorem. See reports/phase1f_d_necessary_bound.md.

Assumptions (not checked by this scalar API): GR, geodesic irrotational
dust, Lambda=0, rho>=0; regular material domain of finite positive intrinsic
dust volume; spacelike uniform-proper-expansion slices; a local flat-dust
core obeying Theta_w=2/s_w, with positive density and intrinsic volume;
and the prescribed tracker wall-clock anchor. ell=N/gamma is not generally
the ADM lapse. The core is not identified with the whole Timescape wall,
finite infinity, H1, or dressed geometry. Matching H_Omega to H_D is an
additional assumption, not a consequence of the coordinate choice.

Only M>0 is tested. A positive result does not establish existence,
sufficiency, H1 compatibility, an embedding, or any observable. There are
no geometry/perturbation solvers, time scans, or root searches here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math
from numbers import Real
import sys
from typing import ClassVar


# Explicit engineering guard for binary64 arithmetic, NOT a rigorous error
# enclosure. The caller must also supply a dimensionless margin tolerance.
MIN_MARGIN_RTOL = 64.0 * sys.float_info.epsilon


class NecessaryBoundDomainError(ValueError):
    """An input violates the scalar contract, or the core age is negative."""


class NecessaryBoundNumericalError(ArithmeticError):
    """Binary64 range/conditioning does not allow this evaluation."""


class NecessaryBoundDecision(str, Enum):
    """Numerical decisions about one necessary condition, never existence."""

    NOT_EXCLUDED_BY_NECESSARY_CONDITION = "NOT_EXCLUDED_BY_NECESSARY_CONDITION"
    NUMERICAL_VIOLATION = "NUMERICAL_VIOLATION"
    UNRESOLVED_THRESHOLD = "UNRESOLVED_THRESHOLD"


@dataclass(frozen=True)
class NecessaryBoundResult:
    """Scalar values in the caller's explicitly named time unit.

    tau_w, s_w, margin and margin_scale have time units; H_D and H_bound
    have inverse time units. x, f, alpha_W, d, normalized_margin and
    margin_rtol are dimensionless. margin is M, not an existence residual.
    No result constitutes a certified floating-point exclusion.
    """

    time_unit: str
    x: float
    f: float
    alpha_W: float
    tau_w: float
    s_w: float
    H_D: float
    H_bound: float
    d: float
    margin: float
    margin_scale: float
    normalized_margin: float
    margin_rtol: float
    decision: NecessaryBoundDecision

    scientific_classification: ClassVar[str] = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
    existence_status: ClassVar[str] = "NOT_DERIVED"


def _finite_scalar(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise NecessaryBoundDomainError(f"{name} must be a real scalar, not a bool or array")
    try:
        result = float(value)
    except OverflowError as exc:
        raise NecessaryBoundNumericalError(f"{name} cannot be represented in binary64") from exc
    if not math.isfinite(result):
        raise NecessaryBoundDomainError(f"{name} must be finite")
    return result


def _normal_positive(value: float, name: str) -> None:
    if not math.isfinite(value) or value < sys.float_info.min:
        raise NecessaryBoundNumericalError(
            f"{name} must be positive, finite and normal in binary64; "
            "this evaluation is outside the supported numerical range"
        )


def diagnose_positive_core_bound(
    *, t: float, b: float, C: float, time_unit: str, margin_rtol: float,
) -> NecessaryBoundResult:
    """Evaluate only the positive-core necessary condition M>0.

    t>0, b>0 and finite C use the SAME time unit (label only, no conversion).
    C is external. Here b is defined by f=t/(t+b), equivalently
    b=(2+fv0)*(1-fv0)/(3*fv0*HD0) from W09 Eq. (B2); no other b convention
    is imported. W09 Eq. (B12) fixes tau_w(0)=0, with no additive constant.

    From BMR Eq. (4.14), D>=Theta**2/3; the additional anchor gives
    ell=2*alpha_W/(s_w**2*D). BMR Eqs. (4.9), (4.12) then give
    H_Omega<alpha_W/s_w for a positive-volume positive-density core.
    Using W09 Eqs. (B6), (B7), matching requires
    M=6*t/(2+f)**2-s_w>0. The stable evaluation uses M=Q-L-C, where
    L=b*(2/9)*log1p(3*x/2), Q=b*2*x*(6*x+5)/(3*(3*x+2)**2).
    Thus d=(L-Q)/b and M=-b*d-C; these are derived algebraic identities,
    not separately numbered equations in either source paper.

    Numerical policy: S=max(L,Q,abs(C)) is a time scale built from the
    terms of the stable margin. normalized_margin=M/S. The caller supplies
    dimensionless MIN_MARGIN_RTOL<=margin_rtol<1. Values with |M/S|<=rtol
    are UNRESOLVED_THRESHOLD (including equality); the implied absolute
    band is rtol*S in time units. This is a heuristic resolution policy,
    NOT an error certificate. S scales with a change of time units.

    Nonfinite/domain-invalid inputs raise NecessaryBoundDomainError.
    Unrepresentable/subnormal x, positive clock/age/rates or S raise
    NecessaryBoundNumericalError; so does cancellation too near s_w=0
    (64*epsilon relative to its summands). A subnormal margin is allowed
    only inside the unresolved band. No infinities, clipping or warnings
    suppression are used to rescue an invalid evaluation.
    """
    t = _finite_scalar(t, "t")
    b = _finite_scalar(b, "b")
    C = _finite_scalar(C, "C")
    margin_rtol = _finite_scalar(margin_rtol, "margin_rtol")
    if t <= 0.0 or b <= 0.0:
        raise NecessaryBoundDomainError("t and b must be strictly positive")
    if not isinstance(time_unit, str) or not time_unit.strip():
        raise NecessaryBoundDomainError("time_unit must explicitly name the common time unit")
    if not MIN_MARGIN_RTOL <= margin_rtol < 1.0:
        raise NecessaryBoundDomainError("margin_rtol must satisfy MIN_MARGIN_RTOL <= rtol < 1")

    x = t / b
    _normal_positive(x, "x=t/b")
    # Algebraic forms of W09 (B2), (B12) and the derived gap above.
    # Reciprocal arguments avoid overflowing 3*x, x**2 or 1.5*x.
    if x <= 1.0:
        f = x / (1.0 + x)
        log_term = (2.0 / 9.0) * math.log1p(1.5 * x)
        rational_term = x * (2.0 * (6.0*x + 5.0) / (3.0 * (3.0*x + 2.0)**2))
    else:
        y = 1.0 / x
        f = 1.0 / (1.0 + y)
        log_term = (2.0 / 9.0) * (math.log(x) + math.log(1.5 + y))
        rational_term = 2.0 * (6.0 + 5.0*y) / (3.0 * (3.0 + 2.0*y)**2)
    L, Q = b * log_term, b * rational_term
    proper_linear_term = (2.0 / 3.0) * t  # W09 (B12), normalized at zero.
    try:
        tau_w = math.fsum((proper_linear_term, L))
        s_w = math.fsum((proper_linear_term, L, C))
    except OverflowError as exc:
        raise NecessaryBoundNumericalError("clock or age exceeds binary64 range") from exc
    age_scale = max(proper_linear_term, L, abs(C))
    if abs(s_w) / age_scale <= MIN_MARGIN_RTOL:
        raise NecessaryBoundNumericalError("s_w=0 boundary is unresolved at binary64 precision")
    if s_w < 0.0:
        raise NecessaryBoundDomainError("s_w must be strictly positive")
    _normal_positive(tau_w, "tau_w")
    _normal_positive(s_w, "s_w")

    try:
        margin = math.fsum((Q, -L, -C))
    except OverflowError as exc:
        raise NecessaryBoundNumericalError("margin exceeds binary64 range") from exc

    alpha_W = 2.0 / (2.0 + f)  # W09 (B7), reciprocal tracker wall clock.
    H_D = ((2.0 + f) / 3.0) / t  # W09 (B6); avoid overflowing 3*t.
    H_bound = alpha_W / s_w  # Derived from BMR (4.12), (4.14) + anchor.
    _normal_positive(H_D, "H_D")
    _normal_positive(H_bound, "H_bound")
    margin_scale = max(L, Q, abs(C))
    _normal_positive(margin_scale, "margin_scale")
    normalized_margin = margin / margin_scale
    if abs(normalized_margin) <= margin_rtol:
        decision = NecessaryBoundDecision.UNRESOLVED_THRESHOLD
    elif 0.0 < abs(margin) < sys.float_info.min:
        raise NecessaryBoundNumericalError("resolved margin would be subnormal in binary64")
    elif normalized_margin > 0.0:
        decision = NecessaryBoundDecision.NOT_EXCLUDED_BY_NECESSARY_CONDITION
    else:
        decision = NecessaryBoundDecision.NUMERICAL_VIOLATION
    return NecessaryBoundResult(
        time_unit=time_unit, x=x, f=f, alpha_W=alpha_W, tau_w=tau_w,
        s_w=s_w, H_D=H_D, H_bound=H_bound,
        d=math.fsum((log_term, -rational_term)), margin=margin,
        margin_scale=margin_scale, normalized_margin=normalized_margin,
        margin_rtol=margin_rtol, decision=decision,
    )
