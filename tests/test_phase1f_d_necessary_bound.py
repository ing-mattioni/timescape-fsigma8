"""Independent scalar references for the authorized Phase 1F-D criterion.

Equation lineage: W09 (B2), (B6), (B7), (B12), arXiv:0909.0749v2;
BMR (4.9), (4.12), (4.14), arXiv:1912.04213v2, plus the explicit anchor.
Decimal references use the direct dimensional margin, not the stable
implementation. 400 digits resolve its cancellation even for x~1e308.
Float comparisons state both tolerances; relative budgets below are
roundoff allowances, except the explicitly truncation-limited derivatives
and the published-value comparison. They are not scientific certificates.
"""

from dataclasses import FrozenInstanceError, fields
from decimal import Decimal, localcontext
import math

import numpy as np
import pytest
from scipy.integrate import quad

from timescape_fsigma8 import background as bg
from timescape_fsigma8.phase1f_d import (
    MIN_MARGIN_RTOL,
    NecessaryBoundDecision as Decision,
    NecessaryBoundDomainError,
    NecessaryBoundNumericalError,
    diagnose_positive_core_bound,
)
from timescape_fsigma8.scientific_status import CURRENT_SCIENTIFIC_STATUS


def evaluate(t=1.0, b=1.0, C=0.0, *, margin_rtol=1e-12, time_unit="test_time"):
    return diagnose_positive_core_bound(
        t=t, b=b, C=C, time_unit=time_unit, margin_rtol=margin_rtol,
    )


def decimal_reference(t, b, C):
    """Direct W09 clock and original bound with 400-digit intermediates."""
    with localcontext() as ctx:
        ctx.prec = 400
        dt, db, dc = (Decimal.from_float(float(v)) for v in (t, b, C))
        f = dt / (dt + db)
        alpha = 2 / (2 + f)
        tau = 2*dt/3 + 2*db/9 * (1 + 3*dt/(2*db)).ln()
        age = tau + dc
        limit = 6*dt/(2 + f)**2
        return {"f": f, "alpha_W": alpha, "tau_w": tau, "s_w": age,
                "H_D": (2+f)/(3*dt), "H_bound": alpha/age,
                "margin": limit-age, "d": (tau-limit)/db,
                "threshold_C": limit-tau}


@pytest.mark.parametrize("t,b,C", [
    (0.01, 2.0, 0.0), (1.0, 1.0, -0.2), (3.0, 1.0, 0.0),
    (4.0, 1.0, 0.0), (8.0, 2.0, 0.25),
    (1e-250, 1.0, 0.0), (1e250, 1.0, 0.0),
    (1.6e307, 0.1, 0.0),  # 1.5*x and polynomial powers would overflow.
])
def test_against_independent_high_precision_dimensional_form(t, b, C):
    result = evaluate(t, b, C)
    expected = decimal_reference(t, b, C)
    for name in ("f", "alpha_W", "tau_w", "s_w", "H_D", "H_bound", "margin", "d"):
        assert getattr(result, name) == pytest.approx(float(expected[name]), rel=5e-13, abs=0.0)
    assert result.margin == pytest.approx(-b*result.d-C, rel=5e-13, abs=0.0)
    assert result.normalized_margin == result.margin/result.margin_scale


@pytest.mark.parametrize("t", [0.01, 0.2, 1.0, 3.0, 100.0])
def test_clock_integral_fixes_normalization_and_matches_frozen(t):
    b = 2.3
    # Integrate d tau/dt=2*(t+b)/(3*t+2*b), from W09 (B2), (B7),
    # starting at zero. epsabs is in test_time; epsrel is dimensionless.
    reference, _ = quad(lambda u: 2*(u+b)/(3*u+2*b), 0.0, t,
                        epsabs=2e-13*b, epsrel=2e-13, limit=100)
    result = evaluate(t, b)
    assert result.tau_w == pytest.approx(reference, rel=5e-13, abs=0.0)
    # Exact convention bridge: b=(2+fv0)*(1-fv0)/(3*fv0*HD0).
    fv0 = 0.6
    params = bg.TrackerParams(fv0=fv0, HD0=(2+fv0)*(1-fv0)/(3*fv0*b))
    assert result.f == pytest.approx(float(bg.fv(t, params)), rel=2e-14, abs=0.0)
    assert result.tau_w == pytest.approx(float(bg.tau_w(t, params)), rel=2e-14, abs=0.0)
    assert result.alpha_W == pytest.approx(float(bg.dtau_w_dt(t, params)), rel=2e-14, abs=0.0)
    assert result.H_D == pytest.approx(float(bg.H_D(t, params)), rel=2e-14, abs=0.0)


@pytest.mark.parametrize("t", [0.01, 0.2, 1.0, 3.0, 100.0])
def test_clock_derivative_is_alpha(t):
    b = 1.7
    h = 1e-5*t  # Symmetric derivative, truncation/roundoff budget 2e-9.
    derivative = (evaluate(t+h, b).tau_w-evaluate(t-h, b).tau_w)/(2*h)
    assert derivative == pytest.approx(2*(t+b)/(3*t+2*b), rel=2e-9, abs=0.0)


@pytest.mark.parametrize("factor", [1e-100, 0.03125, 7.0, 1e100])
@pytest.mark.parametrize("t,b,C", [(2.0, 1.0, -0.1), (4.0, 1.0, 0.05)])
def test_change_of_time_unit_preserves_judgment(factor, t, b, C):
    original = evaluate(t, b, C, time_unit="original_time")
    scaled = evaluate(factor*t, factor*b, factor*C, time_unit="rescaled_time")
    for name in ("tau_w", "s_w", "margin", "margin_scale"):
        assert getattr(scaled, name) == pytest.approx(factor*getattr(original, name), rel=3e-14, abs=0.0)
    for name in ("H_D", "H_bound"):
        assert getattr(scaled, name) == pytest.approx(getattr(original, name)/factor, rel=3e-14, abs=0.0)
    assert scaled.normalized_margin == pytest.approx(original.normalized_margin, rel=3e-14, abs=0.0)
    assert scaled.decision is original.decision


def test_gap_monotonicity_and_opposite_signs():
    # Analytic derivative from the authorized gap (derived from cited
    # W09/BMR equations): 2*(x+1)*(3*x-2)/(3*x+2)**3.
    decreasing = [evaluate(x).d for x in (0.01, 0.2, 0.5, 2/3)]
    increasing = [evaluate(x).d for x in (2/3, 1.0, 3.0, 4.0, 100.0)]
    assert all(right < left for left, right in zip(decreasing, decreasing[1:]))
    assert all(right > left for left, right in zip(increasing, increasing[1:]))
    assert evaluate(3.0).d < 0.0 < evaluate(4.0).d
    assert evaluate(3.0).decision is Decision.NOT_EXCLUDED_BY_NECESSARY_CONDITION
    assert evaluate(4.0).decision is Decision.NUMERICAL_VIOLATION
    for x in (0.1, 0.4, 2/3, 1.0, 3.0, 4.0, 10.0):
        h = 1e-5  # Absolute step in x; derivative budget 2e-9 in d/x.
        derivative = (evaluate(x+h).d-evaluate(x-h).d)/(2*h)
        analytic = 2*(x+1)*(3*x-2)/(3*x+2)**3
        assert derivative == pytest.approx(analytic, rel=0.0, abs=2e-9)


def test_early_and_late_limits_without_direct_margin_cancellation():
    early = evaluate(1e-10)
    # O(x) corrections to tau/t=1, alpha=1, t*HD=2/3, M/t=1/2.
    assert early.tau_w/1e-10 == pytest.approx(1.0, rel=3e-10, abs=0.0)
    assert early.alpha_W == pytest.approx(1.0, rel=3e-10, abs=0.0)
    assert early.H_D*1e-10 == pytest.approx(2/3, rel=3e-10, abs=0.0)
    assert early.margin/1e-10 == pytest.approx(0.5, rel=3e-10, abs=0.0)
    late = evaluate(1e100)
    assert late.tau_w/1e100 == pytest.approx(2/3, rel=2e-15, abs=0.0)
    assert late.H_D*1e100 == pytest.approx(1.0, rel=2e-15, abs=0.0)
    # The leading linear terms would erase the logarithmic obstruction.
    direct = 6*(1e100/(2+late.f)**2)-late.s_w
    assert direct >= 0.0  # Zero or a spurious positive sign, not the obstruction.
    assert late.margin == pytest.approx(
        float(decimal_reference(1e100, 1.0, 0.0)['margin']), rel=2e-14, abs=0.0,
    )
    assert late.margin < -40.0
    assert late.decision is Decision.NUMERICAL_VIOLATION


def test_offset_is_external_and_age_domain_is_checked():
    base = evaluate()
    later = evaluate(C=0.2)
    earlier = evaluate(C=-0.2)
    assert later.s_w-base.s_w == pytest.approx(0.2, rel=0.0, abs=2e-16)
    assert base.margin-later.margin == pytest.approx(0.2, rel=0.0, abs=2e-16)
    assert earlier.margin-base.margin == pytest.approx(0.2, rel=0.0, abs=2e-16)
    assert later.decision is Decision.NUMERICAL_VIOLATION
    assert earlier.decision is Decision.NOT_EXCLUDED_BY_NECESSARY_CONDITION
    with pytest.raises(NecessaryBoundDomainError, match="s_w"):
        evaluate(C=-2.0)
    # Check the age domain before a margin sum could overflow.
    with pytest.raises(NecessaryBoundDomainError, match="s_w"):
        evaluate(t=1e307, b=1e308, C=-1.79e308)
    with pytest.raises(NecessaryBoundNumericalError, match="s_w=0"):
        evaluate(C=-float(decimal_reference(1.0, 1.0, 0.0)["tau_w"]))


@pytest.mark.parametrize("offset,decision", [
    (-1e-8, Decision.NOT_EXCLUDED_BY_NECESSARY_CONDITION),
    (-1e-14, Decision.UNRESOLVED_THRESHOLD),
    (0.0, Decision.UNRESOLVED_THRESHOLD),
    (1e-14, Decision.UNRESOLVED_THRESHOLD),
    (1e-8, Decision.NUMERICAL_VIOLATION),
])
def test_threshold_uses_declared_band(offset, decision):
    critical_C = float(decimal_reference(1.0, 1.0, 0.0)["threshold_C"])
    result = evaluate(C=critical_C+offset)
    assert result.decision is decision
    if decision is Decision.UNRESOLVED_THRESHOLD:
        assert abs(result.normalized_margin) <= result.margin_rtol


def test_larger_tolerance_does_not_promote_near_threshold_candidate():
    critical_C = float(decimal_reference(1.0, 1.0, 0.0)["threshold_C"])
    assert evaluate(C=critical_C-1e-8).decision is Decision.NOT_EXCLUDED_BY_NECESSARY_CONDITION
    assert evaluate(C=critical_C-1e-8, margin_rtol=1e-6).decision is Decision.UNRESOLVED_THRESHOLD


@pytest.mark.parametrize("change", [
    {"t": 0.0}, {"t": -1.0}, {"b": 0.0}, {"b": -1.0},
    {"t": math.nan}, {"t": math.inf}, {"b": math.nan}, {"b": math.inf},
    {"C": math.nan}, {"C": math.inf}, {"C": -math.inf},
    {"t": True}, {"b": "1"}, {"t": np.array([1.0])},
    {"time_unit": ""}, {"time_unit": "  "},
    {"margin_rtol": 0.0}, {"margin_rtol": MIN_MARGIN_RTOL/2},
    {"margin_rtol": 1.0}, {"margin_rtol": math.nan},
])
def test_invalid_inputs_fail_explicitly(change):
    with pytest.raises(NecessaryBoundDomainError):
        evaluate(**change)


@pytest.mark.parametrize("t,b,C", [
    (1e308, 1e-308, 0.0),  # x overflow
    (1e-308, 1e308, 0.0),  # x underflow
    (1e-310, 1.0, 0.0),   # subnormal x
    (1e308, 1e308, 0.0),  # subnormal Hubble rate
    (1e308, 1e308, 1e308), # age overflow
    (1e-308, 1e-308, 0.0),# subnormal clock
    (10**400, 1.0, 0.0),  # finite integer outside binary64
])
def test_unrepresentable_evaluations_are_not_domain_or_feasibility_verdicts(t, b, C):
    with pytest.raises(NecessaryBoundNumericalError):
        evaluate(t, b, C)


def test_published_tracker_reference_and_explicit_b_bridge():
    # Existing published reference: GM arXiv:2511.17160v2, p.25, ~58.01;
    # W09 (B8)-(B9), using H0=73.23 as documented in the frozen background
    # audit. The rounded reference has absolute tolerance 0.005 km/s/Mpc.
    params = bg.TrackerParams.from_dressed_H0(fv0=0.737, H0=73.23)
    b = (2+params.fv0)*(1-params.fv0)/(3*params.fv0*params.HD0)
    result = evaluate(params.t0, b, time_unit="Mpc s/km")
    assert result.H_D == pytest.approx(58.01, rel=0.0, abs=0.005)
    assert result.f == pytest.approx(0.737, rel=2e-14, abs=0.0)
    assert result.alpha_W == pytest.approx(2/2.737, rel=2e-14, abs=0.0)


def test_positive_margin_carries_no_existence_or_global_promotion():
    before = dict(CURRENT_SCIENTIFIC_STATUS)
    result = evaluate()
    assert result.margin > 0.0
    assert result.decision is Decision.NOT_EXCLUDED_BY_NECESSARY_CONDITION
    assert result.existence_status == "NOT_DERIVED"
    assert result.scientific_classification == "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
    assert not {"feasible", "exists", "certified"}.intersection(f.name for f in fields(result))
    with pytest.raises(FrozenInstanceError):
        result.margin = 0.0
    assert dict(CURRENT_SCIENTIFIC_STATUS) == before
    for name in ("REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING",
                 "ALL_TIME_TRANSFER_CONSTITUTIVE_COMPATIBILITY"):
        assert CURRENT_SCIENTIFIC_STATUS[name] == "NOT_DERIVED"
    for name in ("UNIQUE_TIMESCAPE_PREDICTION", "OBSERVATIONAL_AUTHORIZATION",
                 "RSD_AUTHORIZATION", "SIGMA8_AUTHORIZATION", "FSIGMA8_AUTHORIZATION"):
        assert CURRENT_SCIENTIFIC_STATUS[name] == "NOT_GRANTED"
