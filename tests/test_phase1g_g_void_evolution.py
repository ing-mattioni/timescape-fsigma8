"""Physical moments and independent ODE checks of the report-only 1G-G benchmark."""

from pathlib import Path
import math
import sys

import numpy as np
import pytest
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from phase1g_g_void_evolution_numerics import (
    build_evidence, constant_kernel_counts, constant_kernel_volume_tail,
    fraction_rate, tracker_fraction, void_mass_fraction,
)
from phase1g_f_volume_budget_successor_numerics import FixedDomainBudget


@pytest.mark.parametrize("u", [0.0, 0.1, 1.0, 10.0, 100.0])
def test_number_and_volume_moments_with_exact_tail(u):
    n0 = 3.7
    n = constant_kernel_counts(classes=500, initial_number_density=n0, merger_exposure=u)
    k = np.arange(1, 501)
    q = u / (1.0 + u)
    assert n.sum() + n0 / (1.0 + u) * q ** 500 == pytest.approx(n0 / (1.0 + u), rel=0.0, abs=2e-13)
    tail = constant_kernel_volume_tail(minimum_class=501, merger_exposure=u)
    assert k @ n / n0 + tail == pytest.approx(1.0, rel=0.0, abs=2e-12)
    assert constant_kernel_volume_tail(minimum_class=1, merger_exposure=u) == 1.0
    assert not n.flags.writeable


def test_published_constant_kernel_solution_against_independent_kinetic_integration():
    # [L03] (2.2), K=1, N0=1, t=2 -> u=1; implement collision sums,
    # not the analytic time derivative. Exact total N obeys N'=-N^2/2.
    size = 32
    def rhs(t, state):
        n, total = state[:-1], state[-1]
        gain = np.r_[0.0, 0.5 * np.convolve(n, n)[:size - 1]]
        return np.r_[gain - n * total, -0.5 * total ** 2]
    initial = np.r_[1.0, np.zeros(size - 1), 1.0]
    solution = solve_ivp(rhs, (0.0, 2.0), initial, method="DOP853", rtol=2e-11, atol=2e-13)
    assert solution.success
    actual = solution.y[:-1, -1]
    expected = constant_kernel_counts(classes=size, initial_number_density=1.0, merger_exposure=1.0)
    np.testing.assert_allclose(actual, expected, rtol=1e-8, atol=2e-12)
    assert actual[0] == pytest.approx(0.25, rel=0.0, abs=2e-12)  # [L03] (4.10), t=2


def test_mergers_change_sizes_but_not_volume_at_fixed_epoch():
    early = constant_kernel_volume_tail(minimum_class=125, merger_exposure=0.0)
    late = constant_kernel_volume_tail(minimum_class=125, merger_exposure=100.0)
    assert early == 0.0 and late > 0.6
    for u in (0.0, 100.0):
        assert constant_kernel_volume_tail(minimum_class=1, merger_exposure=u) == 1.0


def test_time_units_and_conditional_tracker_ode():
    def rhs(t, f):
        return [fraction_rate(fraction=float(f[0]), h_void=1/t, h_wall=2/(3*t), transfer_over_domain_volume=0.0)]
    solution = solve_ivp(rhs, (0.2, 3.0), [0.17], method="DOP853", rtol=2e-11, atol=2e-13)
    assert solution.success
    for t, f in zip(solution.t, solution.y[0]):
        exact = tracker_fraction(time=float(t), reference_time=0.2, reference_fraction=0.17)
        assert f == pytest.approx(exact, rel=0.0, abs=3e-11)
        assert tracker_fraction(time=1000*t, reference_time=200.0, reference_fraction=0.17) == pytest.approx(exact, rel=0.0, abs=2e-15)
    rate = fraction_rate(fraction=0.4, h_void=0.8, h_wall=0.6, transfer_over_domain_volume=0.01)
    scaled = fraction_rate(fraction=0.4, h_void=0.8/1000, h_wall=0.6/1000, transfer_over_domain_volume=0.01/1000)
    assert scaled * 1000 == pytest.approx(rate, rel=0.0, abs=2e-15)


def test_void_mass_volume_conversion_and_vacuum_limit():
    for fv in (0.0, 0.2, 0.737, 1.0):
        m = void_mass_fraction(volume_fraction=fv, density_ratio=0.2047)
        b = FixedDomainBudget(total_void_mass_fraction=m, density_ratio=0.2047)
        assert b.total_void_volume_fraction == pytest.approx(fv, rel=0.0, abs=2e-15)
    assert void_mass_fraction(volume_fraction=0.737, density_ratio=0.0) == 0.0
    with pytest.raises(ValueError):
        void_mass_fraction(volume_fraction=1.0, density_ratio=0.0)


def test_shell_crossing_rate_requires_transfer_to_match_tracker_instantaneously():
    # [JLH13] (A8) gives H_v*t=8/9, while the tracker takes 1.
    fv, t = 0.737, 7.0
    closed = fraction_rate(fraction=fv, h_void=8/(9*t), h_wall=2/(3*t), transfer_over_domain_volume=0.0)
    target = fv * (1-fv) / t
    assert closed / target == pytest.approx(2/3, rel=0.0, abs=2e-15)
    source = target / 3
    assert fraction_rate(fraction=fv, h_void=8/(9*t), h_wall=2/(3*t), transfer_over_domain_volume=source) == pytest.approx(target, rel=0.0, abs=2e-15)


def test_existing_tracker_reference_and_published_shell_crossing():
    evidence = build_evidence()
    assert evidence["spherical_shell_crossing"]["H_v_times_t"] == pytest.approx(8/9, rel=0.0, abs=2e-14)
    for case in evidence["cases"].values():
        assert max(abs(row["residual"]) for row in case["history"]) < 2e-14
        assert case["mass_fraction_if_shell_density_at_f_v0"] > 0.25
        assert case["mass_fraction_if_exact_vacuum_at_f_v0"] == 0.0


def test_shell_crossing_from_lagrangian_trajectories_without_imposing_A8():
    """JLH13 (A4)-(A5), exterior Delta_i proportional to R_i^-3.

    Absorb positive dimensional constants into units: r=R_i^4(cosh eta-1),
    t=R_i^(9/2)(sinh eta-eta). Locate dr/dR_i|t=0 by finite differences,
    independently of the production root equation H_v*t=8/9. Using R_i=2
    keeps both neighboring shells exterior to the seed R_0=1. This locates
    crossing for that shell; the first crossing is at the seed boundary.
    Root xtol=5e-14; step-halving absolute H_v*t budget 2e-7 covers finite
    differences and root cancellation, not a physical uncertainty.
    """
    def radius(label, time):
        eta = brentq(lambda e: math.sinh(e)-e-time/label**4.5, 0.1, 15.0, xtol=5e-14)
        return label**4 * (math.cosh(eta)-1.0)

    estimates = []
    label = 2.0
    for step in (1e-4, 5e-5):
        def shell_jacobian(eta):
            time = label**4.5 * (math.sinh(eta)-eta)
            return (radius(label+step, time)-radius(label-step, time))/(2*step)
        eta = brentq(shell_jacobian, 2.0, 5.0, xtol=5e-14)
        time = label**4.5 * (math.sinh(eta)-eta)
        dt = 1e-5*time
        hvt = time*(radius(label, time+dt)-radius(label, time-dt))/(2*dt*radius(label,time))
        estimates.append(hvt)
    np.testing.assert_allclose(estimates, [8/9, 8/9], rtol=0.0, atol=2e-7)
    assert abs(estimates[0]-estimates[1]) < 2e-7
    production = build_evidence()["spherical_shell_crossing"]["H_v_times_t"]
    assert production == pytest.approx(estimates[1], rel=0.0, abs=2e-7)


@pytest.mark.parametrize("u", [-1.0, float("nan"), float("inf")])
def test_invalid_merger_clock_fails_closed(u):
    with pytest.raises(ValueError):
        constant_kernel_counts(classes=5, initial_number_density=1.0, merger_exposure=u)
    with pytest.raises(ValueError):
        constant_kernel_volume_tail(minimum_class=2, merger_exposure=u)
