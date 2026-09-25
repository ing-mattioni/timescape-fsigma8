"""d/dkappa_star of one accepted LTB--CMC background; conditional checks only.

References: Sussman arXiv:1002.0173v2 (1)--(3), (A.1); Gourgoulhon
gr-qc/0703035 (4.63), (6.90); BMR 1912.04213v2 (4.5), (4.9), (4.12),
(4.16), (4.18), (4.20). The linearized equations are conditional research
derivations, not published theorems.

Finite differences in kappa_star are TEST tools only: independent
background solves at fixed s_c, m0, r_c, r_o, G and labels r, compared at
knots common to every TIGHT sample grid (no interpolation). Background,
linearized-BVP and quadrature errors are measured separately. The
differentiated identities (local mass density, local and averaged
Hamilton constraints) are ALGEBRAIC checks and do not replace them.
Tolerances are explicit engineering bounds with margin, not certificates.
"""

from dataclasses import fields, replace
import importlib
import inspect
import math
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.interpolate import CubicSpline

from timescape_fsigma8.experimental_ltb_cmc import (
    LTBModel, LTBDomainError, LTBNumericalError, Numerics, solve_cmc, solve_kappa_sensitivity,
)
from timescape_fsigma8.experimental_ltb_cmc.geometry import Geometry, chi_profile, curvature
from timescape_fsigma8.experimental_ltb_cmc.kappa_sensitivity import _run
from timescape_fsigma8.experimental_ltb_cmc.solver import _checked_background


BASE = LTBModel(0.2, 0.2, 0.25, 0.7, 1.7, "time=length", "mass")
SECOND = LTBModel(.08, .4, .2, .8, 2.3, "T", "M")
FLAT = replace(BASE, kappa_star=0.0)
TIGHT = Numerics(bvp_tol=1e-8, bc_tol=1e-12, check_tol=2e-6,
                 initial_nodes=101, check_nodes=601, quadrature_order=48)
KNOTS = np.linspace(0, 1, TIGHT.check_nodes)  # present in every TIGHT sample grid
STEPS = (4e-3, 2e-3, 1e-3)
SCALARS = ("delta_K_star", "delta_K_s", "delta_ln_V", "delta_ln_M_rest", "delta_ln_rho0",
           "delta_J", "delta_rho_lambda", "delta_Q_lambda", "delta_R_lambda")
PROFILES = ("delta_S", "delta_xi", "delta_gamma", "delta_N_c", "delta_lambda")


def _knots(solution, values, nodes=KNOTS):
    """Values at exact knots of a sample grid; no interpolation."""
    idx = np.searchsorted(solution.r, nodes - 1e-14)
    assert np.all(np.abs(solution.r[idx] - nodes) <= 1e-15)
    return np.asarray(values)[idx]


def _scalars(sol):
    a = sol.averages
    return np.array([sol.K_star, sol.K_s, math.log(a.V), math.log(a.M_rest), math.log(a.rho0),
                     a.J, a.rho_lambda, a.Q_lambda, a.R_lambda])


def _profiles(sol):
    return [_knots(sol, v) for v in (sol.S, sol.xi, sol.gamma, sol.N_c, sol.lambda_)]


def _chi_scalar(model):
    """Separate scalar chi implementation, for independent quad integrals."""
    def chi(r):
        z = (r - model.r_c) / (model.r_o - model.r_c)
        return 0.0 if z <= 0 else 1.0 if z >= 1 else (
            math.exp(-1 / z) / (math.exp(-1 / z) + math.exp(-1 / (1 - z))))
    return chi


@pytest.fixture(scope="module")
def base():
    return solve_kappa_sensitivity(1.0, BASE, TIGHT)


@pytest.fixture(scope="module")
def nearby():
    # Central differences at FIXED s_c and m0: only kappa_star moves.
    return {h: (solve_cmc(1.0, replace(BASE, kappa_star=BASE.kappa_star - h), TIGHT),
                solve_cmc(1.0, replace(BASE, kappa_star=BASE.kappa_star + h), TIGHT))
            for h in STEPS}


def test_chi_profile_is_direct_and_matches_curvature():
    r = np.concatenate((np.linspace(0, 1, 401), [np.nextafter(BASE.r_c, 1), np.nextafter(BASE.r_o, 0)]))
    chi, chi_r = chi_profile(r, BASE)
    k, kr = curvature(r, BASE)
    # exp(log kappa_star + log chi) vs kappa_star*exp(log chi): rounding of
    # |log chi| ~ 600 in the exponentially small tails allows ~1e-13 relative.
    np.testing.assert_allclose(BASE.kappa_star * chi, k, rtol=1e-12, atol=1e-300)
    np.testing.assert_allclose(BASE.kappa_star * chi_r, kr, rtol=1e-12, atol=1e-300)
    np.testing.assert_array_equal(chi == 0, k == 0)
    np.testing.assert_array_equal(chi_r == 0, kr == 0)
    # Defined at kappa_star=0, where kappa/kappa_star would be 0/0.
    chi0, chi0_r = chi_profile(r, FLAT)
    np.testing.assert_array_equal(chi0, chi)
    np.testing.assert_array_equal(chi0_r, chi_r)
    assert np.all(curvature(r, FLAT)[0] == 0) and chi0[-1] == 1 and chi0[0] == 0


def test_parabolic_limits_and_continuity_of_age_derivatives():
    # S10 (2) at k=0: a_k=a**2/(10*m0), a_kk=-3*a**3/(350*m0**2).
    r = np.array([0.0, 0.1, 0.25, 0.5, 1.0])
    for model in (BASE, FLAT):
        geom = Geometry(model, 1.0, TIGHT)
        g, t = geom.kappa_terms(np.ones_like(r), r)
        flat = curvature(r, model)[0] == 0
        np.testing.assert_allclose(g.a_kappa[flat], g.a[flat]**2 / (10 * geom.m), rtol=2e-15, atol=0)
        np.testing.assert_allclose(t.a_kk[flat], -3 * g.a[flat]**3 / (350 * geom.m**2),
                                   rtol=2e-15, atol=0)
    defects = []
    for k in (1e-4, 1e-5):
        geom = Geometry(replace(BASE, kappa_star=k), 1.0, TIGHT)
        g, t = geom.kappa_terms(np.ones(1), np.ones(1))
        defects.append(t.a_kk[0] + 3 * g.a[0]**3 / (350 * geom.m**2))
    # Curved quadrature branch joins the analytic limit linearly in k.
    assert abs(defects[0]) < 1e-3 and 8 < defects[0] / defects[1] < 12


@pytest.mark.parametrize("model", [BASE, SECOND, FLAT], ids=["base", "second", "flat"])
def test_local_kappa_terms_against_fixed_age_differences(model):
    # d/dkappa_star at FIXED dust age s and r; forward FD at kappa_star=0.
    r = np.array([0.0, 0.1, 0.25, 0.3, 0.4, 0.5, 0.55, 0.6, 0.69, 0.7, 0.85, 1.0])
    s = np.array([1.0, 0.99, 1.02, 0.97, 1.01, 0.95, 1.03, 0.98, 1.0, 1.05, 0.96, 1.0])
    g, t = Geometry(model, 1.0, TIGHT).kappa_terms(s, r)
    pick = {"a": lambda G, T: G.a, "R_r": lambda G, T: G.R_r, "A": lambda G, T: G.A,
            "Hp": lambda G, T: T.Hp, "Hl": lambda G, T: T.Hl, "Theta": lambda G, T: G.Theta,
            "ln_rho": lambda G, T: np.log(G.G_rho), "extra": lambda G, T: G.radial_extra,
            "sigma2": lambda G, T: G.sigma2, "R_u": lambda G, T: G.R_u,
            "ln_F": lambda G, T: np.log(G.sqrt_energy), "a_k": lambda G, T: G.a_kappa,
            "a_sk": lambda G, T: T.a_sk}
    exact = {"a": t.d_a, "R_r": t.d_R_r, "A": t.d_A, "Hp": t.d_Hp, "Hl": t.d_Hl,
             "Theta": t.d_Theta, "ln_rho": t.d_ln_rho, "extra": t.d_radial_extra,
             "sigma2": t.d_sigma2, "R_u": t.d_R_u, "ln_F": t.d_ln_F,
             "a_k": t.chi * t.a_kk, "a_sk": t.chi * t.a_skk}

    def at(k):
        return Geometry(replace(model, kappa_star=k), 1.0, TIGHT).kappa_terms(s, r)

    fd = []
    for h in (2e-3, 1e-3):
        if model.kappa_star == 0:
            (g1, t1), (g2, t2) = at(h), at(2 * h)
            fd.append({n: (-3 * f(g, t) + 4 * f(g1, t1) - f(g2, t2)) / (2 * h) for n, f in pick.items()})
        else:
            (gp, tp), (gm, tm) = at(model.kappa_star + h), at(model.kappa_star - h)
            fd.append({n: (f(gp, tp) - f(gm, tm)) / (2 * h) for n, f in pick.items()})
    # Central Richardson leaves O(h**4) (observed <=5e-11); the one-sided
    # second-order rule at kappa_star=0 leaves O(h**3) (observed <=3.5e-7).
    rtol, atol = (1e-6, 1e-6) if model.kappa_star == 0 else (1e-9, 1e-10)
    for name in pick:
        err = [np.max(np.abs(d[name] - exact[name])) for d in fd]
        assert 3.5 < err[0] / err[1] < 4.5, name
        np.testing.assert_allclose((4 * fd[1][name] - fd[0][name]) / 3, exact[name],
                                   rtol=rtol, atol=atol, err_msg=name)


def test_local_age_derivatives_and_algebraic_identities():
    r = np.array([0.0, 0.2, 0.3, 0.45, 0.6, 0.72, 0.9, 1.0])
    s = np.array([1.0, 1.01, 0.98, 1.02, 0.97, 1.0, 1.03, 1.0])
    geom = Geometry(SECOND, 1.0, TIGHT)
    g, t = geom.kappa_terms(s, r)
    h = 1e-4
    (gp, tp), (gm, tm) = geom.kappa_terms(s + h, r), geom.kappa_terms(s - h, r)
    for fd, exact in (((tp.Hp - tm.Hp), t.Hp_s), ((tp.Hl - tm.Hl), t.Hl_s),
                      ((gp.radial_extra - gm.radial_extra), t.radial_extra_s),
                      ((gp.sigma2 - gm.sigma2), t.sigma2_s), ((gp.R_u - gm.R_u), t.R_u_s),
                      ((gp.Theta - gm.Theta), -t.D), ((gp.A - gm.A), g.A * t.Hl),
                      ((np.log(gp.G_rho) - np.log(gm.G_rho)), -g.Theta)):
        np.testing.assert_allclose(fd / (2 * h), exact, rtol=1e-6, atol=5e-7)
    # ALGEBRAIC: differentiated local Hamilton constraint (S10/BMR (4.16))
    # and rho*A*R**2 = 3*m0*r**2/(4*pi*G*F) at fixed age.
    four = 16 * np.pi * g.G_rho
    np.testing.assert_allclose((4 / 3) * g.Theta * t.d_Theta - 2 * t.d_sigma2 + t.d_R_u,
                               four * t.d_ln_rho, rtol=1e-13, atol=1e-13)
    np.testing.assert_allclose((4 / 3) * g.Theta * (-t.D) - 2 * t.sigma2_s + t.R_u_s,
                               -four * g.Theta, rtol=1e-13, atol=1e-13)
    np.testing.assert_allclose(t.d_ln_rho + t.d_A / g.A + 2 * t.d_a / g.a,
                               -r**2 * t.chi / (2 * g.sqrt_energy**2), rtol=1e-13, atol=1e-15)


@pytest.mark.parametrize("s", [1.0, 1.3])
def test_flat_limits(s):
    sens = solve_kappa_sensitivity(s, FLAT, TIGHT)
    a = (4.5 * FLAT.m0 * s**2)**(1 / 3)
    assert sens.one_sided is True
    assert sens.delta_Q_lambda == pytest.approx(0, rel=0, abs=1e-12 / s**2)
    assert sens.delta_R_lambda == pytest.approx(-6 / a**2, rel=1e-12, abs=0)
    assert sens.delta_lambda[[0, -1]] == pytest.approx([0, 0], rel=0, abs=4e-12)
    # delta ln M_rest = -(3/2) int r**4 chi dr on the flat ball (S10 (3)).
    integral, error = quad(lambda r: r**4 * _chi_scalar(FLAT)(r), 0, 1,
                           points=[FLAT.r_c, FLAT.r_o], epsabs=1e-14, epsrel=1e-13, limit=200)
    assert error < 1e-13
    assert sens.delta_ln_M_rest == pytest.approx(-1.5 * integral, rel=1e-12, abs=1e-14)


def test_flat_right_derivative_against_forward_differences():
    sens = solve_kappa_sensitivity(1.0, FLAT, TIGHT)
    exact = np.array([getattr(sens, name) for name in SCALARS])
    f0 = _scalars(solve_cmc(1.0, FLAT, TIGHT))
    fd = []
    for h in STEPS:
        f1 = _scalars(solve_cmc(1.0, replace(FLAT, kappa_star=h), TIGHT))
        f2 = _scalars(solve_cmc(1.0, replace(FLAT, kappa_star=2 * h), TIGHT))
        fd.append((-3 * f0 + 4 * f1 - f2) / (2 * h))
    errors = [np.abs(d - exact) for d in fd]
    assert np.all((3.5 < errors[0] / errors[1]) & (errors[0] / errors[1] < 4.5))
    # One-sided rule: Richardson leaves an O(h**3) remainder (observed use of
    # rtol=1e-7 about 0.6), hence the wider bound.
    np.testing.assert_allclose((4 * fd[2] - fd[1]) / 3, exact, rtol=5e-7, atol=5e-9)


@pytest.mark.parametrize("case", [(1.0, BASE), (0.7, SECOND)], ids=["base", "second"])
def test_curved_scalars_against_central_differences(case):
    s, model = case
    sens = solve_kappa_sensitivity(s, model, TIGHT)
    exact = np.array([getattr(sens, name) for name in SCALARS])
    fd = []
    for h in STEPS:
        lo = solve_cmc(s, replace(model, kappa_star=model.kappa_star - h), TIGHT)
        hi = solve_cmc(s, replace(model, kappa_star=model.kappa_star + h), TIGHT)
        assert lo.model.m0 == hi.model.m0 == model.m0 and lo.s_c == hi.s_c == s
        fd.append((_scalars(hi) - _scalars(lo)) / (2 * h))
    errors = [np.abs(d - exact) for d in fd]
    assert np.all((3.8 < errors[0] / errors[1]) & (errors[0] / errors[1] < 4.2))
    assert np.all((3.8 < errors[1] / errors[2]) & (errors[1] / errors[2] < 4.2))
    # atol covers the small Q_lambda sensitivity (~3.8e-4, Richardson ~7e-12).
    np.testing.assert_allclose((4 * fd[2] - fd[1]) / 3, exact, rtol=1e-8, atol=5e-11)
    # Independent quad of d/dkappa_star int 3*m0*r**2/(G*F) dr (S10 (3)).
    chi = _chi_scalar(model)
    mass, e1 = quad(lambda r: 3 * model.m0 * r**2 / math.sqrt(1 + r**2 * model.kappa_star * chi(r)),
                    0, 1, points=[model.r_c, model.r_o], epsabs=1e-14, epsrel=1e-13, limit=200)
    d_mass, e2 = quad(lambda r: -1.5 * model.m0 * r**4 * chi(r)
                      / (1 + r**2 * model.kappa_star * chi(r))**1.5,
                      0, 1, points=[model.r_c, model.r_o], epsabs=1e-14, epsrel=1e-13, limit=200)
    assert max(e1, e2) < 1e-13
    assert sens.delta_ln_M_rest == pytest.approx(d_mass / mass, rel=1e-12, abs=1e-14)


def test_curved_profiles_against_central_differences(base, nearby):
    exact = [_knots(base.solution, getattr(base, name)) for name in PROFILES]
    fd = {h: [(p_hi - p_lo) / (2 * h) for p_lo, p_hi in zip(_profiles(lo), _profiles(hi))]
          for h, (lo, hi) in nearby.items()}
    for i, (name, atol) in enumerate(zip(PROFILES, (5e-9, 3e-8, 5e-10, 1e-9, 1e-9))):
        errors = [np.max(np.abs(fd[h][i] - exact[i])) for h in STEPS]
        assert 3.8 < errors[0] / errors[1] < 4.2 and 3.8 < errors[1] / errors[2] < 4.2, name
        np.testing.assert_allclose((4 * fd[1e-3][i] - fd[2e-3][i]) / 3, exact[i],
                                   rtol=0, atol=atol, err_msg=name)


def test_error_sources_are_separated(base):
    # Background, linearized-BVP and quadrature errors at the same age.
    bg_tight = _checked_background(1.0, BASE, TIGHT)
    bg_default = _checked_background(1.0, BASE, Numerics())
    reference = _run(bg_tight, TIGHT)
    for name in SCALARS:
        assert getattr(reference, name) == getattr(base, name)
    bvp = _run(bg_tight, Numerics())           # only the linearized BVPs change
    background = _run(bg_default, TIGHT)       # only the background changes
    quadrature = _run(bg_tight, replace(TIGHT, quadrature_order=16))  # only averages change
    nodes = np.linspace(0, 1, 71)
    for other in (bvp, background):
        for name in SCALARS:
            assert getattr(other, name) == pytest.approx(getattr(reference, name), rel=1e-8, abs=1e-11)
        for name in PROFILES:
            np.testing.assert_allclose(
                CubicSpline(other.solution.r, getattr(other, name))(nodes),
                CubicSpline(reference.solution.r, getattr(reference, name))(nodes),
                rtol=0, atol=1e-9, err_msg=name)
    for name in ("delta_K_star", "delta_K_s"):
        assert getattr(quadrature, name) == getattr(reference, name)
    for name in PROFILES:
        np.testing.assert_array_equal(getattr(quadrature, name), getattr(reference, name))
    for name in SCALARS[2:]:  # deliberately coarse order 16: up to ~6e-10 absolute
        assert getattr(quadrature, name) == pytest.approx(getattr(reference, name), rel=3e-8, abs=3e-11)
    assert quadrature.residuals.quadrature > reference.residuals.quadrature


@pytest.mark.parametrize("scale", [1e-4, 1e4])
def test_dimensional_powers(base, scale):
    # Scales s_c and m0 together (G fixed): a homothety, not a kappa_star test.
    scaled = solve_kappa_sensitivity(scale, replace(BASE, m0=BASE.m0 * scale), TIGHT)
    for name, power in zip(SCALARS, (-1, -2, 0, 0, 0, -1, -2, -2, -2)):
        assert getattr(scaled, name) / scale**power == pytest.approx(
            getattr(base, name), rel=3e-11, abs=1e-15)
    nodes = np.linspace(0, 1, 71)
    for name, power in zip(PROFILES, (1, 0, 0, 0, 0)):
        np.testing.assert_allclose(
            CubicSpline(scaled.solution.r, getattr(scaled, name) / scale**power)(nodes),
            CubicSpline(base.solution.r, getattr(base, name))(nodes), rtol=3e-11, atol=1e-13)
    heavy = solve_kappa_sensitivity(1.0, replace(BASE, G=3 * BASE.G), TIGHT)
    assert heavy.delta_rho_lambda * 3 == pytest.approx(base.delta_rho_lambda, rel=2e-15, abs=0)
    for name in SCALARS:
        if name != "delta_rho_lambda":
            assert getattr(heavy, name) == getattr(base, name)


def test_representability_even_when_background_is_accepted():
    # Homothetic copy (m0=0.02*s_c) with an explicit extreme G: the largest
    # background density-type output is rho(0)=1/(6*pi*G*s_c**2), while
    # |delta_rho_lambda| is about 1.37 times larger for this model.
    s = 1e-50
    model = LTBModel(0.02 * s, 0.2, 0.25, 0.7, 3.5e-210, "L", "M")
    background = solve_cmc(s, model)
    assert np.max(background.rho) < np.finfo(float).max
    reference = solve_kappa_sensitivity(s, replace(model, G=1.7))
    log_value = (math.log(abs(reference.delta_rho_lambda)) + math.log(1.7) - math.log(model.G))
    assert log_value > math.log(np.finfo(float).max)
    with pytest.raises(LTBNumericalError, match="Dimensional output outside normal binary64 range"):
        solve_kappa_sensitivity(s, model)
    with pytest.raises(LTBNumericalError):
        solve_kappa_sensitivity(1e200, replace(BASE, m0=2e199))  # background itself fails


def test_numerical_controls_and_boundaries(base):
    res, num = base.residuals, TIGHT
    assert res.boundary <= 4 * num.bc_tol
    assert res.lambda_boundary <= 4 * num.bc_tol * (1 + abs(base.delta_gamma[-1]))
    assert max(res.cmc_equation, res.lapse_equation, res.quadrature, res.mass_identity,
               res.local_hamilton, res.hamilton, res.background_J) <= num.check_tol
    assert max(res.cmc_bvp_rms, res.lapse_bvp_rms) < 10 * num.bvp_tol
    # Analytically null boundary values: absolute tolerances, s_c = 1 here.
    assert base.delta_S[[0, -1]] == pytest.approx([0, 0], rel=0, abs=4e-12)
    assert base.delta_xi[0] == pytest.approx(0, rel=0, abs=4e-12)
    assert base.delta_N_c[0] == pytest.approx(0, rel=0, abs=4e-12)
    assert base.delta_N_c[-1] == pytest.approx(base.delta_gamma[-1], rel=0, abs=4e-12)
    assert base.delta_lambda[[0, -1]] == pytest.approx([0, 0], rel=0, abs=4e-12)
    assert base.delta_ln_rho0 == pytest.approx(base.delta_ln_M_rest - base.delta_ln_V,
                                               rel=2e-15, abs=2e-16)
    assert res.phi_center == pytest.approx(base.solution.phi[0], rel=2e-15, abs=0)
    assert base.one_sided is False
    for name in PROFILES:
        profile = getattr(base, name)
        assert np.all(np.isfinite(profile)) and profile.shape == base.solution.r.shape
        with pytest.raises(ValueError):
            profile[0] = 99


def test_single_background_solve_and_no_production_differencing(monkeypatch):
    solver = importlib.import_module("timescape_fsigma8.experimental_ltb_cmc.solver")
    calls = []
    original = solver._solve_background

    def counting(*args):
        calls.append(args[0])
        return original(*args)

    monkeypatch.setattr(solver, "_solve_background", counting)
    sens = solve_kappa_sensitivity(1.0, BASE)
    assert calls == [1.0]
    monkeypatch.undo()
    reference = solve_cmc(1.0, BASE)
    assert sens.solution.K_star == reference.K_star and sens.solution.K_s == reference.K_s
    source = Path(importlib.import_module(
        "timescape_fsigma8.experimental_ltb_cmc.kappa_sensitivity").__file__).read_text(encoding="utf-8")
    assert "solve_cmc(" not in source and "replace(" not in source


def test_injected_failures_return_no_partial_sensitivity(monkeypatch):
    module = importlib.import_module("timescape_fsigma8.experimental_ltb_cmc.kappa_sensitivity")
    original = module.solve_bvp

    def unconverged(fun, bc, x, y, **kwargs):
        return original(fun, bc, x, y, **{**kwargs, "tol": 1e-13, "max_nodes": x.size})

    monkeypatch.setattr(module, "solve_bvp", unconverged)
    with pytest.raises(LTBNumericalError, match="Sensitivity CMC BVP status"):
        solve_kappa_sensitivity(1.0, BASE)
    calls = []

    def second_unconverged(fun, bc, x, y, **kwargs):
        calls.append(1)
        if len(calls) == 2:
            kwargs = {**kwargs, "tol": 1e-13, "max_nodes": x.size}
        return original(fun, bc, x, y, **kwargs)

    monkeypatch.setattr(module, "solve_bvp", second_unconverged)
    with pytest.raises(LTBNumericalError, match="Sensitivity lapse BVP status"):
        solve_kappa_sensitivity(1.0, BASE)

    def wrong_eigenvalue(*args, **kwargs):
        result = original(*args, **kwargs)
        result.p = result.p + 1e-3 * (1 + abs(result.p))
        return result

    monkeypatch.setattr(module, "solve_bvp", wrong_eigenvalue)
    with pytest.raises(LTBNumericalError, match="Unresolved sensitivity checks"):
        solve_kappa_sensitivity(1.0, BASE)
    monkeypatch.undo()
    with pytest.raises(LTBNumericalError, match="BVP status"):
        solve_kappa_sensitivity(1, BASE, Numerics(bvp_tol=1e-10, initial_nodes=12, max_nodes=24))


@pytest.mark.parametrize("age", [0, -1, math.nan, math.inf, True, [1]])
def test_invalid_age(age):
    with pytest.raises(LTBDomainError):
        solve_kappa_sensitivity(age, BASE)


def test_invalid_types_and_model_domain():
    with pytest.raises(LTBDomainError):
        solve_kappa_sensitivity(1.0, "model")
    with pytest.raises(LTBDomainError):
        solve_kappa_sensitivity(1.0, BASE, {"bvp_tol": 1e-8})
    with pytest.raises(LTBDomainError):
        replace(BASE, kappa_star=-1e-3)  # left of kappa_star=0 is outside the model domain


def test_firewall(base):
    assert base.scientific_classification == "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
    forbidden = {"embedding", "exists", "H1", "nu_W", "observable", "all_time_compatible",
                 "compatible", "delta_P_lambda", "P_lambda", "sigma8", "fsigma8", "RSD",
                 "mass_compensated", "m_profile"}
    for record in (base, base.residuals):
        assert not forbidden & {f.name for f in fields(record)}
    package = "timescape_fsigma8.experimental_ltb_cmc"
    solver = importlib.import_module(f"{package}.solver")
    evolution = importlib.import_module(f"{package}.evolution")
    clock = importlib.import_module(f"{package}.clock")
    sensitivity = importlib.import_module(f"{package}.kappa_sensitivity")
    geometry = importlib.import_module(f"{package}.geometry")
    assert list(inspect.signature(sensitivity.solve_kappa_sensitivity).parameters) == [
        "s_c", "model", "numerics"]
    assert list(inspect.signature(solver.solve_cmc).parameters) == ["s_c", "model", "numerics"]
    assert list(inspect.signature(evolution.solve_cmc_evolution).parameters) == [
        "s_c", "model", "numerics"]
    for name in ("solve_at_tracker_clock", "solve_evolution_at_tracker_clock"):
        assert list(inspect.signature(getattr(clock, name)).parameters) == [
            "t", "b", "C", "model", "numerics"]
    assert list(inspect.signature(geometry.curvature).parameters) == ["r", "model"]
    assert list(inspect.signature(geometry.Geometry.at).parameters) == ["self", "s", "r"]
    source = Path(sensitivity.__file__).read_text(encoding="utf-8")
    for token in ("from .clock", "from .evolution", "tracker_clock", "phase1f_d",
                  "scientific_status"):
        assert token not in source
    status = importlib.import_module("timescape_fsigma8.scientific_status")
    for name in ("REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING",
                 "ALL_TIME_TRANSFER_CONSTITUTIVE_COMPATIBILITY", "PHYSICAL_TIMESCAPE_TRAJECTORY_EXISTENCE"):
        assert getattr(status, name) == "NOT_DERIVED"
    for name in ("UNIQUE_TIMESCAPE_PREDICTION", "OBSERVATIONAL_AUTHORIZATION", "RSD_AUTHORIZATION",
                 "SIGMA8_AUTHORIZATION", "FSIGMA8_AUTHORIZATION"):
        assert getattr(status, name) == "NOT_GRANTED"
