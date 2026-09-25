"""Conditional LTB--CMC checks; none authorize a Timescape embedding.

References: Sussman arXiv:1002.0173v2 (1)--(3),(5),(7),(A.1),(A.2);
Gourgoulhon gr-qc/0703035 (4.63),(6.90); BMR 1912.04213v2
(4.9),(4.12),(4.16),(4.18),(4.20); W09 0909.0749v2 (B2),(B6),(B12).
Exact-sector/asymptotic expectations are independent analytic reductions,
not previously published numerical values for this newly specified BVP.
"""

from dataclasses import fields, replace
import importlib
import inspect
import math
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import quad, simpson
from scipy.interpolate import CubicSpline

from timescape_fsigma8.experimental_ltb_cmc import (
    LTBModel, LTBDomainError, LTBNumericalError, Numerics, solve_cmc,
)
from timescape_fsigma8.experimental_ltb_cmc.clock import (
    solve_at_tracker_clock, tracker_clock,
)
from timescape_fsigma8.experimental_ltb_cmc.geometry import Geometry, curvature


BASE = LTBModel(0.2, 0.2, 0.25, 0.7, 1.7, "time=length", "mass")
TIGHT = Numerics(bvp_tol=1e-8, bc_tol=1e-12, check_tol=2e-6,
                 initial_nodes=101, check_nodes=601, quadrature_order=48)


@pytest.fixture(scope="module")
def curved():
    return solve_cmc(1.0, BASE)


@pytest.fixture(scope="module")
def tight():
    return solve_cmc(1.0, BASE, TIGHT)


@pytest.fixture(scope="module")
def flat():
    return solve_cmc(1.3, replace(BASE, kappa_star=0), TIGHT)


def test_flat_geometry_and_averages(flat):
    # S10 (A.1), reduced exactly, and BMR (4.12),(4.20).
    s, m, G = flat.s_c, BASE.m0, BASE.G
    a0 = (4.5 * m)**(1 / 3) * s**(2 / 3)
    rho = 1 / (6 * math.pi * G * s**2)
    for actual, expected in ((flat.S, s), (flat.xi, 0), (flat.gamma, 1),
                             (flat.A, a0), (flat.R, flat.r * a0),
                             (flat.Theta, 2 / s), (flat.rho, rho),
                             (flat.N_c, 1), (flat.lambda_, 1),
                             (flat.k_perp, -2 / (3 * s)),
                             (flat.k_parallel, -2 / (3 * s))):
        np.testing.assert_allclose(actual, expected, rtol=2e-9, atol=2e-10)
    assert flat.K_star == pytest.approx(-2 / s, rel=2e-12, abs=2e-13)
    assert flat.K_s == pytest.approx(2 / s**2, rel=2e-9, abs=2e-10)
    a = flat.averages
    assert a.V == pytest.approx(6 * math.pi * m * s**2, rel=2e-12, abs=1e-13)
    assert a.M_rest == pytest.approx(m / G, rel=2e-12, abs=1e-14)
    assert a.rho0 == pytest.approx(rho, rel=2e-12, abs=1e-14)
    assert a.rho_lambda == pytest.approx(rho, rel=2e-9, abs=1e-12)
    assert a.J == pytest.approx(2 / (3 * s), rel=2e-9, abs=1e-11)
    assert abs(a.Q_lambda) < 1e-18  # variance of a numerically constant lapse
    assert a.R_lambda == 0


def _flat_basis(mu, r):
    """Stable analytic G07 (6.90) flat-ball Dirichlet Green basis.

    expm1 avoids sinh overflow; the central value is the analytic limit.
    Test range mu>0.01, so the final phi subtraction is well conditioned.
    """
    logden = math.log(-math.expm1(-2 * mu))
    logw = np.empty_like(r)
    positive = r > 0
    logw[positive] = (mu * (r[positive] - 1) + np.log(-np.expm1(-2 * mu * r[positive]))
                     - np.log(r[positive]) - logden)
    logw[~positive] = math.log(2 * mu) - mu - logden
    return np.exp(logw), -np.expm1(logw)


def test_flat_lapse_basis(flat):
    # User's flat-ball solution of G07 (6.90), independently evaluated.
    s = flat.s_c
    a0 = (4.5 * BASE.m0)**(1 / 3) * s**(2 / 3)
    mu = math.sqrt(2) * a0 / s
    w, one_minus_w = _flat_basis(mu, flat.r)
    np.testing.assert_allclose(flat.w0, w, rtol=3e-9, atol=3e-10)
    np.testing.assert_allclose(flat.phi, s**2 / 2 * one_minus_w, rtol=3e-9, atol=3e-10)
    assert flat.phi[0] > 0 and flat.w0[0] > 0
    np.testing.assert_allclose(flat.U, 2 / s**2, rtol=2e-12, atol=1e-13)


@pytest.mark.parametrize("eta", [0.2, 1.0, 3.0])
def test_published_hyperbolic_parametric_reference(eta):
    # S10 Eq. (A.2), E_S10=r**2*kappa, M=m0*r**3.
    m, k = 0.2, 0.35
    s = m / k**1.5 * (math.sinh(eta) - eta)
    expected_a = m / k * (math.cosh(eta) - 1)
    g = Geometry(replace(BASE, kappa_star=k), 1.0, TIGHT).at(np.array([s]), np.array([1.0]))
    assert g.a[0] == pytest.approx(expected_a, rel=4e-12, abs=2e-14)


def test_local_derivatives_and_constraint():
    # Derivatives in S10 (2),(3),(5),(7), checked independently of ak/as.
    geom = Geometry(BASE, 1.0, TIGHT)
    r = np.array([0.0, 0.1, 0.4, 0.55, 0.9])
    g = geom.at(np.ones_like(r), r)
    h = 1e-4
    plus = geom.at(np.full_like(r, 1 + h), r)
    minus = geom.at(np.full_like(r, 1 - h), r)
    np.testing.assert_allclose((plus.a - minus.a) / (2 * h), g.a_s, rtol=2e-8, atol=2e-10)
    gp = Geometry(replace(BASE, kappa_star=BASE.kappa_star + h), 1, TIGHT).at(np.ones_like(r), r)
    gm = Geometry(replace(BASE, kappa_star=BASE.kappa_star - h), 1, TIGHT).at(np.ones_like(r), r)
    chi = curvature(r, BASE)[0] / BASE.kappa_star
    np.testing.assert_allclose((gp.a - gm.a) / (2 * h), g.a_kappa * chi, rtol=3e-8, atol=3e-10)
    rp = np.array([0.35, 0.5, 0.65, 0.9])
    g0 = geom.at(np.ones_like(rp), rp)
    derivative = (geom.at(np.ones_like(rp), rp + h).R - geom.at(np.ones_like(rp), rp - h).R) / (2 * h)
    np.testing.assert_allclose(derivative, g0.R_r, rtol=2e-6, atol=2e-7)
    np.testing.assert_allclose((2 / 3) * g.Theta**2 - 2 * g.sigma2 + g.R_u,
                               16 * math.pi * g.G_rho, rtol=2e-12, atol=2e-12)


def test_profile_smooth_endpoints_and_derivative():
    r = np.array([0.0, BASE.r_c, 0.4, 0.5, BASE.r_o, 1.0])
    k, kr = curvature(r, BASE)
    assert k[0] == k[1] == 0 and k[-1] == k[-2] == BASE.kappa_star
    assert kr[0] == kr[1] == kr[-2] == kr[-1] == 0
    h = 1e-6
    fd = (curvature(r[2:4] + h, BASE)[0] - curvature(r[2:4] - h, BASE)[0]) / (2 * h)
    np.testing.assert_allclose(fd, kr[2:4], rtol=2e-9, atol=2e-10)
    # Adjacent representable radii must not produce NaN/inf in the tails.
    tail = np.array([np.nextafter(BASE.r_c, 1), np.nextafter(BASE.r_o, 0)])
    kt, krt = curvature(tail, BASE)
    assert np.all(np.isfinite(kt)) and np.all(np.isfinite(krt))


@pytest.mark.parametrize("case", [(1.0, BASE), (0.7, LTBModel(.08, .4, .2, .8, 2.3, "T", "M"))])
def test_nonhomogeneous_residuals_bounds_and_convergence(case):
    s, model = case
    coarse = solve_cmc(s, model)
    fine = solve_cmc(s, model, TIGHT)
    for sol in (coarse, fine):
        assert 2 <= -sol.K_star * s < 3
        assert np.all((sol.S > 2 * s / 3) & (sol.S < 1.5 * s))
        assert np.all(np.abs(sol.v) < 1)
        assert np.all(sol.R_r > 0) and np.all(sol.rho > 0)
        assert np.min(sol.N_c) >= sol.residuals.lapse_lower_bound - 2e-6
        assert np.min(sol.lambda_) > 0
        assert sol.S[[0, -1]] == pytest.approx([s, s], rel=0, abs=2e-12)
        assert sol.N_c[[0, -1]] == pytest.approx([1, sol.gamma[-1]], rel=0, abs=2e-10)
        assert sol.k_perp[0] == pytest.approx(sol.K_star / 3, rel=2e-12, abs=2e-13)
        assert sol.k_parallel[0] == pytest.approx(sol.K_star / 3, rel=2e-12, abs=2e-13)
        assert max(sol.residuals.cmc_equation, sol.residuals.lapse_equation) < 2e-6
        assert sol.residuals.hamilton < 2e-12
        assert sol.residuals.mass < 2e-12
        assert sol.residuals.quadrature < 1e-7
    for field in fields(fine.averages):
        assert getattr(coarse.averages, field.name) == pytest.approx(
            getattr(fine.averages, field.name), rel=2e-6, abs=2e-9)
    assert fine.residuals.cmc_rms < coarse.residuals.cmc_rms
    assert fine.residuals.lapse_rms < coarse.residuals.lapse_rms


def test_centre_series(curved):
    # G07 (4.63), user's regular centre expansion; no epsilon-start BVP.
    r = curved.r[1:4]
    a0 = (4.5 * BASE.m0)**(1 / 3)
    coeff = -a0 * (curved.K_star + 2) / 3
    np.testing.assert_allclose(curved.xi[1:4] / r, coeff, rtol=2e-5, atol=2e-7)
    np.testing.assert_allclose((curved.S[1:4] - 1) / r**2,
                               a0 * coeff / 2, rtol=3e-5, atol=5e-7)


def test_independent_volume_mass_integrals(tight):
    # Independent Simpson integration on returned profiles; distinguish A/B.
    sol = tight
    dust = 4 * math.pi * sol.A * sol.R**2
    V = simpson(dust, x=sol.r)
    mass = simpson(dust * sol.rho, x=sol.r)
    induced_V = simpson(dust / sol.gamma, x=sol.r)
    assert V == pytest.approx(sol.averages.V, rel=3e-8, abs=1e-10)
    assert mass == pytest.approx(sol.averages.M_rest, rel=3e-8, abs=1e-11)
    assert abs(induced_V - V) > 1e-5  # measure swap would be detectable
    assert sol.averages.M_rest < BASE.m0 / BASE.G
    # Quad uses a separate scalar chi implementation, with explicit tolerance.
    def mass_integrand(r):
        z = (r - BASE.r_c) / (BASE.r_o - BASE.r_c)
        chi = 0 if z <= 0 else 1 if z >= 1 else (
            math.exp(-1 / z) / (math.exp(-1 / z) + math.exp(-1 / (1 - z))))
        return 3 * BASE.m0 * r**2 / math.sqrt(1 + r**2 * BASE.kappa_star * chi) / BASE.G
    expected, error = quad(mass_integrand, 0, 1, epsabs=1e-12, epsrel=1e-12,
                           points=[BASE.r_c, BASE.r_o], limit=100)
    assert error < 1e-11
    assert expected == pytest.approx(sol.averages.M_rest, rel=2e-11, abs=2e-12)


def test_nearby_age_derivatives_and_mass(tight):
    # BMR (4.9),(4.12): independent differencing of solved volumes.
    # G07 (6.90): independently test K_s and lambda=dS/ds_c.
    estimates = []
    for h in (2e-3, 1e-3):
        lo, hi = (solve_cmc(1 - h, BASE, TIGHT), solve_cmc(1 + h, BASE, TIGHT))
        estimates.append((math.log(hi.averages.V) - math.log(lo.averages.V)) / (2 * h))
        assert hi.averages.M_rest == pytest.approx(lo.averages.M_rest, rel=3e-12, abs=3e-13)
        assert (hi.K_star - lo.K_star) / (2 * h) == pytest.approx(tight.K_s, rel=5e-6, abs=1e-8)
        nodes = np.linspace(0, 1, 71)
        derivative = (CubicSpline(hi.r, hi.S)(nodes) - CubicSpline(lo.r, lo.S)(nodes)) / (2 * h)
        np.testing.assert_allclose(derivative, CubicSpline(tight.r, tight.lambda_)(nodes),
                                   rtol=2e-6, atol=2e-7)
    errors = [abs(v - 3 * tight.averages.J) for v in estimates]
    assert errors[1] < 0.3 * errors[0]  # second-order differencing, not solver floor
    richardson = (4 * estimates[1] - estimates[0]) / 3
    assert richardson == pytest.approx(3 * tight.averages.J, rel=3e-9, abs=3e-10)


def test_small_curvature_asymptotics():
    # Conditional expansion of S10 (2),(5) + BMR (4.20), not runtime perturbations.
    eps = (0.01, 0.005, 0.0025)
    fine = [solve_cmc(1, replace(BASE, kappa_star=e), TIGHT) for e in eps]
    coarse = solve_cmc(1, replace(BASE, kappa_star=eps[-1]))
    a0 = (4.5 * BASE.m0)**(1 / 3)
    defects = [s.averages.R_lambda + 6 * e / a0**2 for s, e in zip(fine, eps)]
    assert 3.8 < defects[0] / defects[1] < 4.2
    assert 3.8 < defects[1] / defects[2] < 4.2
    # An O(epsilon**2) bound, NOT an assumed nonzero quadratic coefficient.
    assert max(abs(s.averages.Q_lambda) / e**2 for s, e in zip(fine, eps)) < 3e-5
    assert abs(coarse.averages.R_lambda - fine[-1].averages.R_lambda) < abs(defects[-1]) * 1e-4
    assert abs(coarse.averages.Q_lambda - fine[-1].averages.Q_lambda) < abs(fine[-1].averages.Q_lambda) * 0.01


@pytest.mark.parametrize("scale", [1e-4, 1e4])
def test_dimensional_scaling(tight, scale):
    scaled = solve_cmc(scale, replace(BASE, m0=BASE.m0 * scale), TIGHT)
    nodes = np.linspace(0, 1, 71)
    for name, power in (("S", 1), ("A", 1), ("R", 1), ("R_r", 1), ("Theta", -1),
                        ("rho", -2), ("R_u", -2), ("sigma2", -2), ("phi", 2),
                        ("N_c", 0), ("lambda_", 0), ("gamma", 0)):
        np.testing.assert_allclose(CubicSpline(scaled.r, getattr(scaled, name) / scale**power)(nodes),
                                   CubicSpline(tight.r, getattr(tight, name))(nodes), rtol=3e-8, atol=3e-9)
    for name, power in (("V", 3), ("M_rest", 1), ("rho0", -2), ("rho_lambda", -2),
                        ("J", -1), ("Q_lambda", -2), ("R_lambda", -2)):
        assert getattr(scaled.averages, name) / scale**power == pytest.approx(
            getattr(tight.averages, name), rel=3e-8, abs=3e-10)
    assert scaled.K_star * scale == pytest.approx(tight.K_star, rel=3e-9, abs=3e-10)
    assert scaled.K_s * scale**2 == pytest.approx(tight.K_s, rel=3e-9, abs=3e-10)


def test_explicit_G_does_not_change_geometry(curved):
    other = solve_cmc(1, replace(BASE, G=3 * BASE.G))
    assert other.K_star == curved.K_star
    assert other.averages.J == curved.averages.J
    assert other.averages.M_rest * 3 == pytest.approx(curved.averages.M_rest, rel=2e-14, abs=2e-15)
    np.testing.assert_allclose(other.rho * 3, curved.rho, rtol=2e-14, atol=2e-15)


def test_clock_normalization_derivative_and_adapter():
    f, alpha, tau, s = tracker_clock(1, 2, .1)
    assert tau == pytest.approx(2 / 3 + 4 / 9 * math.log1p(.75), rel=2e-15, abs=2e-16)
    assert s == tau + .1
    h = 1e-4
    derivative = (tracker_clock(1+h, 2, 0)[2] - tracker_clock(1-h, 2, 0)[2]) / (2*h)
    assert derivative == pytest.approx(alpha, rel=2e-9, abs=2e-10)
    assert tracker_clock(1e-300, 1e300, 0)[2] == pytest.approx(1e-300, rel=2e-15, abs=0)
    comparison = solve_at_tracker_clock(1, 2, .1, BASE, TIGHT)
    scaled = solve_at_tracker_clock(10, 20, 1, replace(BASE, m0=2), TIGHT)
    assert comparison.solution.s_c == s
    assert comparison.H_D == pytest.approx(7 / 9, rel=2e-15, abs=2e-16)
    assert comparison.rho_D == pytest.approx((2 / 3) / (6 * math.pi * BASE.G), rel=2e-15, abs=2e-16)
    assert comparison.H_Omega == pytest.approx(alpha * comparison.solution.averages.J, rel=2e-15, abs=2e-16)
    np.testing.assert_allclose(comparison.ell, alpha * comparison.solution.lambda_, rtol=2e-15, atol=2e-16)
    np.testing.assert_allclose(comparison.N, alpha * comparison.solution.N_c, rtol=2e-15, atol=2e-16)
    for name, power in (("tau_w", 1), ("H_Omega", -1), ("H_D", -1), ("H_residual", -1),
                        ("rho_D", -2), ("rho_ell", -2), ("Q_ell", -2), ("R_ell", -2)):
        assert getattr(scaled, name) / 10**power == pytest.approx(getattr(comparison, name), rel=3e-8, abs=3e-10)
    assert scaled.log_density_ratio == pytest.approx(comparison.log_density_ratio, rel=3e-8, abs=3e-10)
    a = comparison.solution.averages
    assert comparison.log_density_ratio == pytest.approx(math.log(comparison.rho_D*a.V/a.M_rest), rel=2e-14, abs=2e-15)


@pytest.mark.parametrize("name,value", [("m0", 0), ("m0", -1), ("G", 0), ("G", math.nan),
                                        ("kappa_star", -1), ("kappa_star", math.inf),
                                        ("r_c", 0), ("r_c", .8), ("r_o", 1),
                                        ("length_unit", ""), ("mass_unit", ""), ("m0", True)])
def test_invalid_model(name, value):
    with pytest.raises(LTBDomainError):
        replace(BASE, **{name: value})


@pytest.mark.parametrize("age", [0, -1, math.nan, math.inf, True, [1]])
def test_invalid_age(age):
    with pytest.raises(LTBDomainError):
        solve_cmc(age, BASE)


@pytest.mark.parametrize("name,value", [("bvp_tol", 0), ("bc_tol", math.nan),
                                        ("age_rtol", 1e-18), ("check_tol", .2),
                                        ("initial_nodes", 3), ("max_nodes", 81),
                                        ("quadrature_order", 8.5), ("check_nodes", True)])
def test_invalid_controls(name, value):
    with pytest.raises(LTBDomainError):
        Numerics(**{name: value})


@pytest.mark.parametrize("args", [(0, 1, 0), (1, 0, 0), (1, 1, -2), (1, 1, math.nan)])
def test_invalid_clock(args):
    with pytest.raises(LTBDomainError):
        tracker_clock(*args)


def test_clock_cancellation_and_output_range():
    tau = tracker_clock(1, 1, 0)[2]
    with pytest.raises(LTBNumericalError, match="cancellation"):
        tracker_clock(1, 1, -tau + 1e-15)
    with pytest.raises(LTBNumericalError):
        solve_cmc(1e200, replace(BASE, m0=2e199))  # volume not representable
    with pytest.raises(LTBNumericalError):
        solve_cmc(1e-200, replace(BASE, m0=2e-201))
    with pytest.raises(LTBNumericalError):
        solve_cmc(1e-300, BASE)  # intermediate scale separation unsupported


def test_failure_has_no_partial_solution():
    with pytest.raises(LTBNumericalError, match="BVP status"):
        solve_cmc(1, BASE, Numerics(bvp_tol=1e-10, initial_nodes=12, max_nodes=24))
    with pytest.raises(LTBNumericalError, match="quadrature"):
        solve_cmc(1, replace(BASE, kappa_star=10), Numerics(quadrature_order=4))
    with pytest.raises(LTBNumericalError, match="representable"):
        solve_cmc(1, replace(BASE, r_o=np.nextafter(BASE.r_c, 1)))


def test_firewall_and_readonly_profiles(curved):
    assert curved.scientific_classification == "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
    names = {f.name for f in fields(curved)}
    assert not {"embedding", "exists", "H1", "nu_W", "observable", "all_time_compatible"} & names
    with pytest.raises(ValueError):
        curved.S[0] = 99
    solver = importlib.import_module("timescape_fsigma8.experimental_ltb_cmc.solver")
    assert list(inspect.signature(solver.solve_cmc).parameters) == ["s_c", "model", "numerics"]
    source = Path(solver.__file__).read_text(encoding="utf-8")
    assert "from .clock" not in source and "from timescape_fsigma8.phase1f_d" not in source
    status = importlib.import_module("timescape_fsigma8.scientific_status")
    for name in ("REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING",
                 "ALL_TIME_TRANSFER_CONSTITUTIVE_COMPATIBILITY", "PHYSICAL_TIMESCAPE_TRAJECTORY_EXISTENCE"):
        assert getattr(status, name) == "NOT_DERIVED"
    for name in ("UNIQUE_TIMESCAPE_PREDICTION", "OBSERVATIONAL_AUTHORIZATION", "RSD_AUTHORIZATION",
                 "SIGMA8_AUTHORIZATION", "FSIGMA8_AUTHORIZATION"):
        assert getattr(status, name) == "NOT_GRANTED"
