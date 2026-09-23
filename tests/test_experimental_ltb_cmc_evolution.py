"""Single-age d/ds_c of the LTB--CMC section family; conditional checks only.

References: Gourgoulhon gr-qc/0703035 (4.63),(6.90); BMR 1912.04213v2
(4.5),(4.9),(4.12); Sussman arXiv:1002.0173v2 (1)--(3); W09 0909.0749v2
(B2),(B3),(B6),(B7),(B12).  The differentiated equations are conditional
research derivations of the user contract, not published theorems.

Finite differences are TEST tools only.  Nearby-age differences keep the
physical m0 (and every other model parameter) fixed; homothety tests scale
s_c and m0 together and are a different check.  Solves are compared at radii
that are knots of every sampled grid (linspace(0, 1, check_nodes)), so the
time differences carry no spatial interpolation error; interpolation and
BVP (default vs TIGHT) errors are measured separately.  Tolerances are
explicit engineering bounds with margin over the observed errors, not
certificates.  None of these checks authorizes an embedding or H1 claim.
"""

from dataclasses import fields, replace
import importlib
import inspect
import math
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import simpson
from scipy.interpolate import CubicSpline

from timescape_fsigma8.experimental_ltb_cmc import (
    LTBModel, LTBDomainError, LTBNumericalError, Numerics, solve_cmc, solve_cmc_evolution,
)
from timescape_fsigma8.experimental_ltb_cmc.clock import (
    _signed_product, solve_at_tracker_clock, solve_evolution_at_tracker_clock, tracker_clock,
)


BASE = LTBModel(0.2, 0.2, 0.25, 0.7, 1.7, "time=length", "mass")
SECOND = LTBModel(.08, .4, .2, .8, 2.3, "T", "M")
FLAT = replace(BASE, kappa_star=0)
TIGHT = Numerics(bvp_tol=1e-8, bc_tol=1e-12, check_tol=2e-6,
                 initial_nodes=101, check_nodes=601, quadrature_order=48)
KNOTS = np.linspace(0, 1, TIGHT.check_nodes)  # present in every TIGHT sample grid
CLOCK = (1.0, 2.0, 0.1)
STEPS = (4e-3, 2e-3, 1e-3)


def _knots(solution, values, nodes=KNOTS):
    """Values at exact knots of a sample grid; no interpolation."""
    idx = np.searchsorted(solution.r, nodes - 1e-14)
    assert np.all(np.abs(solution.r[idx] - nodes) <= 1e-15)
    return np.asarray(values)[idx]


@pytest.fixture(scope="module")
def evolution():
    return solve_cmc_evolution(1.0, BASE, TIGHT)


@pytest.fixture(scope="module")
def default_evolution():
    return solve_cmc_evolution(1.0, BASE)


@pytest.fixture(scope="module")
def nearby():
    # Central differences at FIXED physical m0: only the section age moves.
    return {h: (solve_cmc(1 - h, BASE, TIGHT), solve_cmc(1 + h, BASE, TIGHT)) for h in STEPS}


@pytest.fixture(scope="module")
def clock_evolution():
    return solve_evolution_at_tracker_clock(*CLOCK, BASE, TIGHT)


def test_flat_benchmark():
    # Exact EdS reduction of the contract: every new profile vanishes.
    s = 1.3
    ev = solve_cmc_evolution(s, FLAT, TIGHT)
    sol = ev.solution
    for actual, expected in ((sol.S, s), (sol.gamma, 1), (sol.N_c, 1), (sol.lambda_, 1)):
        np.testing.assert_allclose(actual, expected, rtol=2e-9, atol=2e-10)
    assert sol.K_star == pytest.approx(-2 / s, rel=2e-12, abs=2e-13)
    assert sol.K_s == pytest.approx(2 / s**2, rel=2e-9, abs=2e-10)
    assert ev.K_ss == pytest.approx(-4 / s**3, rel=2e-9, abs=2e-10)
    for profile in (ev.N_c_s, ev.lambda_s, ev.gamma_s):
        np.testing.assert_allclose(profile, 0, rtol=0, atol=2e-10)
    assert ev.P_lambda == pytest.approx(0, rel=0, abs=2e-10)
    assert sol.averages.J == pytest.approx(2 / (3 * s), rel=2e-9, abs=1e-11)
    assert ev.J_s == pytest.approx(-2 / (3 * s**2), rel=2e-9, abs=1e-11)
    assert ev.q_c == pytest.approx(0.5, rel=2e-9, abs=1e-11)
    assert ev.lambda2_D == pytest.approx(2 / s**2, rel=2e-9, abs=1e-11)
    assert ev.var_E == pytest.approx(0, rel=0, abs=1e-18)


def test_flat_adapter_keeps_alpha_dot_term():
    comp = solve_evolution_at_tracker_clock(*CLOCK, FLAT, TIGHT)
    f, alpha, _, s = tracker_clock(*CLOCK)
    t, b, _ = CLOCK
    assert comp.alpha_dot == pytest.approx(-2 * b / (3 * t + 2 * b)**2, rel=2e-15, abs=0)
    assert comp.alpha_dot == pytest.approx(-2 * f * (1 - f) / (t * (2 + f)**2), rel=2e-14, abs=0)
    assert comp.P_ell == pytest.approx(2 * comp.alpha_dot / s, rel=2e-9, abs=1e-12)
    assert comp.H_dot == pytest.approx(2 * comp.alpha_dot / (3 * s) - 2 * alpha**2 / (3 * s**2),
                                       rel=2e-9, abs=1e-12)
    # Dropping alpha_dot*J would move H_dot by |2*alpha_dot/(3*s)| ~ 0.05 and
    # leave P_ell ~ 0; both are far outside the tolerances above.
    assert abs(comp.P_ell) > 0.1 and abs(2 * comp.alpha_dot / (3 * s)) > 0.03


@pytest.mark.parametrize("case", [(1.0, BASE), (0.7, SECOND)])
def test_nearby_age_scalars_at_fixed_m0(case):
    # K_ss vs d(K_s)/ds_c and J_s vs dJ/ds_c from independent background solves.
    s, model = case
    ev = solve_cmc_evolution(s, model, TIGHT)
    derivs = []
    for h in STEPS:
        lo, hi = solve_cmc(s - h, model, TIGHT), solve_cmc(s + h, model, TIGHT)
        assert hi.model.m0 == lo.model.m0 == model.m0
        derivs.append(((hi.K_s - lo.K_s) / (2 * h), (hi.averages.J - lo.averages.J) / (2 * h)))
    for k, exact in enumerate((ev.K_ss, ev.J_s)):
        errors = [abs(d[k] - exact) for d in derivs]
        # Truncation-dominated second-order differencing, not the solver floor.
        assert 3.8 < errors[0] / errors[1] < 4.2 and 3.8 < errors[1] / errors[2] < 4.2
        richardson = (4 * derivs[2][k] - derivs[1][k]) / 3
        assert richardson == pytest.approx(exact, rel=3e-9, abs=3e-10)
    q_fd = -1 - ((4 * derivs[2][1] - derivs[1][1]) / 3) / ev.solution.averages.J**2
    assert q_fd == pytest.approx(ev.q_c, rel=3e-9, abs=3e-10)


def test_nearby_age_profiles_without_interpolation(evolution, nearby):
    # N_c_s, lambda_s, gamma_s vs differences of the background profiles at
    # FIXED r and m0, sampled at common knots (zero interpolation error).
    for name, deriv in (("N_c", "N_c_s"), ("lambda_", "lambda_s"), ("gamma", "gamma_s")):
        exact = _knots(evolution.solution, getattr(evolution, deriv))
        fd = {h: (_knots(hi, getattr(hi, name)) - _knots(lo, getattr(lo, name))) / (2 * h)
              for h, (lo, hi) in nearby.items()}
        errors = [np.max(np.abs(fd[h] - exact)) for h in STEPS]
        assert 3.8 < errors[0] / errors[1] < 4.2 and 3.8 < errors[1] / errors[2] < 4.2
        assert errors[2] < 2e-10  # |profiles| ~ 3e-4 here
        np.testing.assert_allclose((4 * fd[1e-3] - fd[2e-3]) / 3, exact, rtol=0, atol=5e-12)
    # P_lambda from finite-difference lambda_s, independent Simpson average.
    sol = evolution.solution
    dust = _knots(sol, 4 * math.pi * sol.A * sol.R**2)
    lo2, hi2 = nearby[2e-3]
    lo1, hi1 = nearby[1e-3]
    lam_s = (4 * (_knots(hi1, hi1.lambda_) - _knots(lo1, lo1.lambda_)) / 2e-3
             - (_knots(hi2, hi2.lambda_) - _knots(lo2, lo2.lambda_)) / 4e-3) / 3
    P_fd = simpson(dust * _knots(sol, sol.Theta) * lam_s, x=KNOTS) / simpson(dust, x=KNOTS)
    assert P_fd == pytest.approx(evolution.P_lambda, rel=1e-7, abs=1e-12)
    assert abs(evolution.P_lambda) > 1e-4  # not an analytically null benchmark


def test_spatial_interpolation_error_is_separate(evolution, nearby):
    # Off-knot radii need interpolation of the public grids; the added error
    # must stay small compared with the time-truncation error at h=1e-3.
    lo, hi = nearby[1e-3]
    mid = (KNOTS[:-1] + KNOTS[1:]) / 2
    off = mid[~np.isin(mid, evolution.solution.r) & ~np.isin(mid, lo.r) & ~np.isin(mid, hi.r)]
    assert off.size > 100
    for name, deriv in (("N_c", "N_c_s"), ("lambda_", "lambda_s"), ("gamma", "gamma_s")):
        fd_knots = (_knots(hi, getattr(hi, name)) - _knots(lo, getattr(lo, name))) / 2e-3
        knot_error = np.max(np.abs(fd_knots - _knots(evolution.solution, getattr(evolution, deriv))))
        fd_off = (CubicSpline(hi.r, getattr(hi, name))(off)
                  - CubicSpline(lo.r, getattr(lo, name))(off)) / 2e-3
        off_error = np.max(np.abs(
            fd_off - CubicSpline(evolution.solution.r, getattr(evolution, deriv))(off)))
        assert off_error < 1.5 * knot_error + 1e-12


def test_bvp_resolution_error_is_separate(evolution, default_evolution):
    # Same age and model, different collocation/quadrature resolutions.
    tight, coarse = evolution, default_evolution
    assert coarse.K_ss == pytest.approx(tight.K_ss, rel=2e-9, abs=2e-10)
    for name in ("J_s", "P_lambda", "lambda2_D", "var_E", "q_c"):
        assert getattr(coarse, name) == pytest.approx(getattr(tight, name), rel=1e-7, abs=1e-10)
    nodes = np.linspace(0, 1, 71)
    for name in ("N_c_s", "lambda_s", "gamma_s"):
        np.testing.assert_allclose(CubicSpline(coarse.solution.r, getattr(coarse, name))(nodes),
                                   CubicSpline(tight.solution.r, getattr(tight, name))(nodes),
                                   rtol=0, atol=1e-10)
    assert tight.residuals.bvp_rms < coarse.residuals.bvp_rms
    assert tight.residuals.equation < coarse.residuals.equation


def test_independent_averages_measure_and_raychaudhuri(evolution):
    # Independent Simpson averages on returned profiles; distinguish A and B.
    sol, ev = evolution.solution, evolution
    D = sol.Theta**2 / 3 + 2 * sol.sigma2 + 4 * math.pi * BASE.G * sol.rho
    E = sol.lambda_ * sol.Theta
    results = {}
    for label, dust in (("A", 4 * math.pi * sol.A * sol.R**2),
                        ("B", 4 * math.pi * sol.A * sol.R**2 / sol.gamma)):
        avg = lambda value: simpson(dust * value, x=sol.r) / simpson(dust, x=sol.r)
        var = avg((E - avg(E))**2)
        results[label] = (avg(sol.Theta * ev.lambda_s), avg(sol.lambda_**2 * D), var,
                          (avg(sol.Theta * ev.lambda_s) - avg(sol.lambda_**2 * D) + var) / 3)
    P, L2D, var, J_s = results["A"]
    assert P == pytest.approx(ev.P_lambda, rel=1e-7, abs=1e-12)
    assert L2D == pytest.approx(ev.lambda2_D, rel=3e-10, abs=3e-12)
    assert var == pytest.approx(ev.var_E, rel=1e-6, abs=1e-12)
    assert J_s == pytest.approx(ev.J_s, rel=3e-10, abs=3e-12)
    assert abs(results["B"][3] - ev.J_s) > 1e-8  # measure swap would be detectable
    # ALGEBRAIC averaged Raychaudhuri identity: shares the J_s formula's
    # identities and does not by itself validate lambda_s.
    a = sol.averages
    terms = (3 * ev.J_s, 3 * a.J**2, 4 * math.pi * BASE.G * a.rho_lambda, a.Q_lambda, ev.P_lambda)
    assert abs(terms[0] + terms[1] + terms[2] - terms[3] - terms[4]) < 1e-12 * max(map(abs, terms))
    assert ev.residuals.raychaudhuri < 1e-12
    assert ev.q_c == pytest.approx(-1 - ev.J_s / a.J**2, rel=2e-15, abs=2e-16)


def test_clock_against_nearby_tracker_times(clock_evolution):
    # H_dot, d(e_rho)/dt=3*e_H and d(e_H)/dt from background-only solves at
    # nearby t with b, C and the model fixed in their roles.
    t, b, C = CLOCK
    comp = clock_evolution
    derivs = []
    for h in STEPS[1:]:
        lo, hi = (solve_at_tracker_clock(t - h, b, C, BASE, TIGHT),
                  solve_at_tracker_clock(t + h, b, C, BASE, TIGHT))
        derivs.append(np.array([(hi.H_Omega - lo.H_Omega) / (2 * h),
                                (hi.log_density_ratio - lo.log_density_ratio) / (2 * h),
                                (hi.H_residual - lo.H_residual) / (2 * h)]))
    exact = np.array([comp.H_dot, 3 * comp.comparison.H_residual, comp.H_dot_residual])
    errors = [np.abs(d - exact) for d in derivs]
    assert np.all((3.8 < errors[0] / errors[1]) & (errors[0] / errors[1] < 4.2))
    np.testing.assert_allclose((4 * derivs[1] - derivs[0]) / 3, exact, rtol=1e-8, atol=1e-9)


def test_clock_algebra_and_propagation_identity(clock_evolution):
    comp = clock_evolution
    t, b, C = CLOCK
    f, alpha, tau, s = tracker_clock(*CLOCK)
    ev, cmp_ = comp.evolution, comp.comparison
    assert cmp_.solution is ev.solution  # one accepted background, not re-solved
    assert ev.solution.s_c == s
    J = ev.solution.averages.J
    assert comp.alpha_dot == pytest.approx(-2 * f * (1 - f) / (t * (2 + f)**2), rel=2e-14, abs=0)
    assert comp.H_dot == pytest.approx(comp.alpha_dot * J + alpha**2 * ev.J_s, rel=2e-14, abs=0)
    assert comp.P_ell == pytest.approx(alpha**2 * ev.P_lambda + 3 * comp.alpha_dot * J,
                                       rel=2e-14, abs=0)
    assert comp.H_D_dot == pytest.approx(-(2 + f**2) / (3 * t**2), rel=2e-15, abs=0)
    assert comp.J_D == pytest.approx(cmp_.H_D / alpha, rel=2e-15, abs=0)
    assert comp.q_required == pytest.approx((1 - f) * (2 - 5 * f) / (2 + f)**2, rel=2e-14, abs=0)
    assert comp.q_residual == pytest.approx(ev.q_c - comp.q_required, rel=2e-15, abs=0)
    assert comp.H_dot_residual == pytest.approx(comp.H_dot - comp.H_D_dot, rel=2e-15, abs=0)
    # Contract propagation identity for d(e_H)/dt (algebraic consequence).
    rhs = ((comp.alpha_dot / alpha - alpha * (1 + comp.q_required) * (J + comp.J_D))
           * cmp_.H_residual - alpha**2 * J**2 * comp.q_residual)
    assert rhs == pytest.approx(comp.H_dot_residual, rel=2e-12, abs=2e-14)


def test_clock_keeps_one_minus_f_and_exact_zero():
    # f rounds to one: q_required=b*(2b-3t)/(3t+2b)**2 must not collapse to 0.
    t, b = 1e20, 1.0
    f, alpha, tau, s = tracker_clock(t, b, 0)
    assert f == 1.0
    comp = solve_evolution_at_tracker_clock(t, b, 0, replace(BASE, m0=0.2 * s))
    assert comp.q_required == pytest.approx(b * (2 * b - 3 * t) / (3 * t + 2 * b)**2, rel=2e-14, abs=0)
    assert comp.q_required < 0
    assert comp.alpha_dot == pytest.approx(-2 * b / (3 * t + 2 * b)**2, rel=2e-14, abs=0)
    assert comp.H_D_dot == pytest.approx(-1 / t**2, rel=2e-15, abs=0)
    # 3t=2b: q_required vanishes exactly.
    t, b = 2.0, 3.0
    s = tracker_clock(t, b, 0)[3]
    comp = solve_evolution_at_tracker_clock(t, b, 0, replace(BASE, m0=0.2 * s))
    assert comp.q_required == 0.0
    assert comp.q_residual == comp.evolution.q_c


@pytest.mark.parametrize("scale", [1e-4, 1e4])
def test_homothety_powers(evolution, scale):
    # Scales s_c and m0 together (G, dimensionless profile fixed); this is
    # NOT a substitute for the fixed-m0 nearby-age tests above.
    scaled = solve_cmc_evolution(scale, replace(BASE, m0=BASE.m0 * scale), TIGHT)
    for name, power in (("K_ss", -3), ("P_lambda", -2), ("J_s", -2),
                        ("lambda2_D", -2), ("var_E", -2), ("q_c", 0)):
        assert getattr(scaled, name) / scale**power == pytest.approx(
            getattr(evolution, name), rel=3e-8, abs=3e-12)
    nodes = np.linspace(0, 1, 71)
    for name in ("N_c_s", "lambda_s", "gamma_s"):
        np.testing.assert_allclose(
            CubicSpline(scaled.solution.r, getattr(scaled, name) * scale)(nodes),
            CubicSpline(evolution.solution.r, getattr(evolution, name))(nodes),
            rtol=3e-8, atol=3e-12)


@pytest.mark.parametrize("scale", [1e-3, 10.0])
def test_adapter_homothety_powers(clock_evolution, scale):
    t, b, C = CLOCK
    scaled = solve_evolution_at_tracker_clock(t * scale, b * scale, C * scale,
                                              replace(BASE, m0=BASE.m0 * scale), TIGHT)
    for name, power in (("alpha_dot", -1), ("J_D", -1), ("P_ell", -2), ("H_dot", -2),
                        ("H_D_dot", -2), ("H_dot_residual", -2),
                        ("q_required", 0), ("q_residual", 0)):
        assert getattr(scaled, name) / scale**power == pytest.approx(
            getattr(clock_evolution, name), rel=3e-8, abs=3e-12)


def test_numerical_controls_and_boundaries(evolution):
    ev, num = evolution, TIGHT
    res = ev.residuals
    assert res.boundary <= 4 * num.bc_tol
    assert res.lambda_s_boundary <= 4 * num.bc_tol * (1 + abs(ev.gamma_s[-1]))
    assert max(res.equation, res.quadrature, res.raychaudhuri, res.background_J) <= num.check_tol
    assert res.bvp_rms < 10 * num.bvp_tol and num.initial_nodes < res.nodes <= num.max_nodes
    # Analytically null boundary values: absolute tolerances, s_c = 1 here.
    assert ev.N_c_s[0] == pytest.approx(0, rel=0, abs=4e-12)
    assert ev.gamma_s[0] == 0
    assert ev.N_c_s[-1] == pytest.approx(ev.gamma_s[-1], rel=0, abs=4e-12)
    assert ev.lambda_s[[0, -1]] == pytest.approx([0, 0], rel=0, abs=4e-12)
    # Conditioning diagnostic of K_ss (division by phi(0)); no certificate.
    s = ev.solution.s_c
    assert res.phi_center == pytest.approx(ev.solution.phi[0] / s**2, rel=2e-15, abs=0)
    assert res.phi_center > 0.1
    for profile in (ev.N_c_s, ev.lambda_s, ev.gamma_s):
        assert np.all(np.isfinite(profile)) and profile.shape == ev.solution.r.shape
        with pytest.raises(ValueError):
            profile[0] = 99


def test_single_background_solve(monkeypatch):
    solver = importlib.import_module("timescape_fsigma8.experimental_ltb_cmc.solver")
    calls = []
    original = solver._solve_background

    def counting(*args):
        calls.append(args[0])
        return original(*args)

    monkeypatch.setattr(solver, "_solve_background", counting)
    ev = solve_cmc_evolution(1.0, BASE)
    assert calls == [1.0]
    solve_evolution_at_tracker_clock(*CLOCK, BASE)
    assert calls == [1.0, tracker_clock(*CLOCK)[3]]
    monkeypatch.undo()
    reference = solve_cmc(1.0, BASE)
    assert ev.solution.K_star == reference.K_star and ev.solution.K_s == reference.K_s
    np.testing.assert_array_equal(ev.solution.N_c, reference.N_c)


def test_injected_failures_return_no_partial_evolution(monkeypatch):
    module = importlib.import_module("timescape_fsigma8.experimental_ltb_cmc.evolution")
    original = module.solve_bvp

    def unconverged(fun, bc, x, y, **kwargs):
        return original(fun, bc, x, y, **{**kwargs, "tol": 1e-13, "max_nodes": x.size})

    monkeypatch.setattr(module, "solve_bvp", unconverged)
    with pytest.raises(LTBNumericalError, match="Evolution BVP status"):
        solve_cmc_evolution(1.0, BASE)

    def wrong_eigenvalue(*args, **kwargs):
        result = original(*args, **kwargs)
        result.p = result.p * (1 + 1e-3)
        return result

    monkeypatch.setattr(module, "solve_bvp", wrong_eigenvalue)
    with pytest.raises(LTBNumericalError, match="Unresolved evolution checks"):
        solve_cmc_evolution(1.0, BASE)
    with pytest.raises(LTBNumericalError, match="Unresolved evolution checks"):
        solve_evolution_at_tracker_clock(*CLOCK, BASE)
    monkeypatch.undo()
    # A background failure propagates; nothing evolutionary is returned.
    with pytest.raises(LTBNumericalError, match="BVP status"):
        solve_cmc_evolution(1, BASE, Numerics(bvp_tol=1e-10, initial_nodes=12, max_nodes=24))


@pytest.mark.parametrize("age", [0, -1, math.nan, math.inf, True, [1]])
def test_invalid_age(age):
    with pytest.raises(LTBDomainError):
        solve_cmc_evolution(age, BASE)


def test_invalid_types_and_clock():
    with pytest.raises(LTBDomainError):
        solve_cmc_evolution(1.0, "model")
    with pytest.raises(LTBDomainError):
        solve_cmc_evolution(1.0, BASE, {"bvp_tol": 1e-8})
    for args in ((0, 1, 0), (1, 0, 0), (1, 1, -2), (1, 1, math.nan)):
        with pytest.raises(LTBDomainError):
            solve_evolution_at_tracker_clock(*args, BASE)


def test_representability_policy():
    with pytest.raises(LTBNumericalError):
        solve_cmc_evolution(1e200, replace(BASE, m0=2e199))
    with pytest.raises(LTBNumericalError):
        solve_cmc_evolution(1e-200, replace(BASE, m0=2e-201))
    with pytest.raises(LTBNumericalError):
        _signed_product(1e200, 1e200)
    with pytest.raises(LTBNumericalError):
        _signed_product(1e-200, -1e-200)  # would silently lose a nonzero
    assert _signed_product(0.0, 1e300, 1e300) == 0.0
    assert _signed_product(-2.0, 3.0) == pytest.approx(-6.0, rel=2e-15, abs=0)
    assert _signed_product(-2.0, -3.0, 0.5) == pytest.approx(3.0, rel=2e-15, abs=0)


def test_firewall(evolution, clock_evolution):
    assert evolution.scientific_classification == "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
    forbidden = {"embedding", "exists", "H1", "nu_W", "observable", "all_time_compatible",
                 "compatible", "Q_lambda_s", "R_lambda_s", "sigma8", "fsigma8"}
    for record in (evolution, evolution.residuals, clock_evolution):
        assert not forbidden & {f.name for f in fields(record)}
    package = "timescape_fsigma8.experimental_ltb_cmc"
    solver = importlib.import_module(f"{package}.solver")
    evolution_module = importlib.import_module(f"{package}.evolution")
    clock = importlib.import_module(f"{package}.clock")
    assert list(inspect.signature(solver.solve_cmc).parameters) == ["s_c", "model", "numerics"]
    assert list(inspect.signature(evolution_module.solve_cmc_evolution).parameters) == [
        "s_c", "model", "numerics"]
    assert list(inspect.signature(clock.solve_evolution_at_tracker_clock).parameters) == [
        "t", "b", "C", "model", "numerics"]
    assert list(inspect.signature(clock.solve_at_tracker_clock).parameters) == [
        "t", "b", "C", "model", "numerics"]
    for module in (solver, evolution_module):
        source = Path(module.__file__).read_text(encoding="utf-8")
        assert "from .clock" not in source and "tracker_clock" not in source
        assert "phase1f_d" not in source and "scientific_status" not in source
    status = importlib.import_module("timescape_fsigma8.scientific_status")
    for name in ("REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING",
                 "ALL_TIME_TRANSFER_CONSTITUTIVE_COMPATIBILITY", "PHYSICAL_TIMESCAPE_TRAJECTORY_EXISTENCE"):
        assert getattr(status, name) == "NOT_DERIVED"
    for name in ("UNIQUE_TIMESCAPE_PREDICTION", "OBSERVATIONAL_AUTHORIZATION", "RSD_AUTHORIZATION",
                 "SIGMA8_AUTHORIZATION", "FSIGMA8_AUTHORIZATION"):
        assert getattr(status, name) == "NOT_GRANTED"
