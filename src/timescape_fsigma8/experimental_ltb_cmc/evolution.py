"""Single-age evolution of the CMC section family in ONE fixed LTB geometry.

Suffix ``_s`` means d/ds_c at fixed r and fixed physical model parameters
(m0, kappa profile, G) along the family S(s_c, r) of CMC sections; suffix
``_age`` is a local derivative with respect to dust proper age.  This is
neither a perturbation between geometries nor a unit rescaling/homothety.
No tracker quantity (t, b, C) enters this module.

Provenance: the differentiated equations below are conditional research
derivations of the user-supplied contract, built on the ADM trace equation
of Gourgoulhon, gr-qc/0703035, Eq. (6.90) (G07), the intrinsic averages of
Buchert--Mourier--Roy, arXiv:1912.04213v2 (BMR) Eqs. (4.5), (4.9), (4.12),
and the LTB relations of Sussman, arXiv:1002.0173v2, already used by the
background solver.  They are NOT published theorems and NOT derived from the
frozen Timescape runtime.  Classification:
DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION.

Normalization: everything is evaluated in the background solver's internal
units, lengths divided by L = s_c of the evaluated section, with central age
u = s_c/L = 1 and m0/L held FIXED while differentiating in u.  Then
dK_hat/du = L**2 K_s, d2K_hat/du2 = L**3 K_ss, dN_c/du = L N_c_s and
dlambda/du = L lambda_s; physical outputs restore these powers of s_c.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

import numpy as np
from scipy.integrate import solve_bvp

from .geometry import (Array, LTBModel, LTBNumericalError, Numerics,
                       dimensional, finite, gauss)
from .solver import CMCSolution, _Background, _checked_background, _readonly


@dataclass(frozen=True)
class EvolutionResiduals:
    """Dimensionless sampled/resolution diagnostics, NOT rigorous bounds.

    All values use the s_c-scaled internal variables.  ``equation`` is the
    maximum residual of both flux ODEs on the check grid, each normalized by
    max(1, absolute contributing terms).  ``boundary`` covers X(0), Z(0) and
    X(1)-gamma_s(1); ``lambda_s_boundary`` the reconstructed lambda_s(0),
    lambda_s(1).  ``quadrature`` compares Gauss orders n and 2n for J,
    P_lambda, <lambda**2 D>, Var(E) and J_s (denominator max(1, |value|)).
    ``raychaudhuri`` is the ALGEBRAIC averaged-Raychaudhuri identity, which
    shares identities with the J_s formula and does not validate lambda_s by
    itself.  ``background_J`` compares J with the accepted background J.
    ``phi_center`` is the background phi(0) (internal units): K_ss is
    determined through division by it, so a small value signals poor
    conditioning of K_ss; it is a diagnostic, not a certificate.
    """

    bvp_rms: float
    equation: float
    boundary: float
    lambda_s_boundary: float
    quadrature: float
    raychaudhuri: float
    background_J: float
    phi_center: float
    nodes: int


@dataclass(frozen=True)
class CMCEvolution:
    """Accepted single-age d/ds_c of the section family; never an embedding.

    ``solution`` is the accepted background (not re-solved).  Profiles are
    sampled on ``solution.r`` and read-only.  Dimensions (c=1): K_ss is
    length**-3; N_c_s, lambda_s and gamma_s are length**-1; P_lambda, J_s,
    lambda2_D (= <lambda**2 D>) and var_E (= Var(lambda*Theta)) are
    length**-2; q_c is dimensionless.  No sign is imposed on K_ss, N_c_s,
    lambda_s or P_lambda.  No all-time, existence or embedding claim.
    """

    solution: CMCSolution
    K_ss: float
    N_c_s: Array
    lambda_s: Array
    gamma_s: Array
    P_lambda: float
    J_s: float
    q_c: float
    lambda2_D: float
    var_E: float
    residuals: EvolutionResiduals

    scientific_classification: ClassVar[str] = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"


@dataclass(frozen=True)
class _Coefficients:
    """Background coefficients of the evolution BVP at radii r (internal units)."""

    r: Array
    gamma: Array
    lam: Array
    Theta: Array
    D: Array
    A: Array
    R: Array
    G_rho: Array
    sigma2: Array
    N: Array
    z: Array
    U: Array
    d: Array
    e: Array
    gamma_s: Array
    U_s: Array
    d_s: Array
    e_s: Array


def solve_cmc_evolution(s_c: float, model: LTBModel,
                        numerics: Numerics = Numerics()) -> CMCEvolution:
    """Solve the background once, then the linear flux BVP for d/ds_c.

    Unknowns X=N_c_s, Z=z_s and the eigenparameter K_ss:
    X_r = d*Z + d_s*z;  Z_r = e*(U*X-K_ss) + e_s*(U*N_c-K_s) + e*U_s*N_c - 2*Z/r;
    X(0)=0, Z(0)=0, X(1)=gamma_s(1).  The singular term uses the same
    SciPy singular-matrix mechanism as the background lapse.  Invalid input
    raises LTBDomainError; any numerical failure raises LTBNumericalError and
    no partial evolution is returned.
    """
    background = _checked_background(s_c, model, numerics)
    try:
        with np.errstate(over="raise", divide="raise", invalid="raise"):
            return _evolve(background, numerics)
    except (FloatingPointError, OverflowError, ZeroDivisionError, RuntimeWarning) as exc:
        raise LTBNumericalError(f"Arithmetic/representation failure: {exc}") from exc


def _evolve(bg: _Background, num: Numerics) -> CMCEvolution:
    m, K, K_s, gamma_b = bg.geometry.m, bg.K, bg.K_s, bg.gamma_b
    # Regular central limits at internal central age 1 (flat EdS centre).
    a_center = (4.5 * m) ** (1 / 3)
    xi_over_r0 = -a_center * (K + 2) / 3
    xi_s_over_r0 = -(a_center / 3) * ((2 / 3) * (K + 2) + K_s - 2)
    U_s0 = 2 * K * K_s / 3 - 4 / 3
    cache: dict[bytes, _Coefficients] = {}

    def coefficients(r: Array) -> _Coefficients:
        key = r.tobytes()
        if key in cache:
            return cache[key]
        y, g, gamma, B, kp, kl, U = bg.section(r)
        basis = bg.lapse.sol(r)
        N = gamma_b * basis[2] + K_s * basis[0]
        z = gamma_b * basis[3] + K_s * basis[1]  # same superposition as N_c
        lam = N / gamma
        xi = y[1]
        centre = r == 0
        r_safe = np.where(centre, 1.0, r)  # no 0/0: centre uses exact limits
        xi_over_r = np.where(centre, xi_over_r0, xi / r_safe)
        Hp = g.a_s / g.a
        Theta = g.Theta
        Hl = Theta - 2 * Hp
        four_pi_G_rho = 4 * np.pi * g.G_rho
        Hp_age = -m / g.a**3 - Hp**2
        D = Theta**2 / 3 + 2 * g.sigma2 + four_pi_G_rho
        d, e = B / g.a**2, B * g.a**2
        # CMC ODE for xi_r (G07 4.63 reduction) and the lapse flux for N_c_r.
        xi_r = np.where(centre, xi_over_r0,
                        -g.A * (K + gamma * Theta) - 2 * xi_over_r
                        - 2 * g.radial_extra * xi)
        gamma_r = xi * xi_r / gamma
        lam_r = (d * z - lam * gamma_r) / gamma
        v = xi / gamma
        v_s = lam_r / g.A - v * Hl * lam
        xi_s = gamma**3 * v_s
        gamma_s = np.where(centre, 0.0, gamma**3 * v * v_s)
        xi_s_over_r = np.where(centre, xi_s_over_r0, xi_s / r_safe)
        F_over_a = g.sqrt_energy / g.a
        kp_s = np.where(centre, K_s / 3,
                        -gamma_s * Hp - gamma * Hp_age * lam
                        - F_over_a * xi_s_over_r + xi_over_r * F_over_a * Hp * lam)
        kl_s = K_s - 2 * kp_s
        U_s = np.where(centre, U_s0,
                       2 * kl * kl_s + 4 * kp * kp_s
                       + four_pi_G_rho * (-Theta * lam * (2 * gamma**2 - 1)
                                          + 4 * gamma * gamma_s))
        d_s = d * ((Hl - 2 * Hp) * lam - gamma_s / gamma)
        e_s = e * (Theta * lam - gamma_s / gamma)
        finite(N, z, lam, xi_r, lam_r, gamma_s, kp_s, U_s, d_s, e_s)
        result = _Coefficients(r, gamma, lam, Theta, D, g.A, g.R, g.G_rho,
                               g.sigma2, N, z, U, d, e, gamma_s, U_s, d_s, e_s)
        if len(cache) > 16:
            cache.clear()
        cache[key] = result
        return result

    gamma_s_1 = float(coefficients(np.array([1.0])).gamma_s[0])

    def rhs(r: Array, y: Array, p: Array) -> Array:
        c = coefficients(r)
        # The singular matrix supplies -2*Z/r; Z=z_s is NOT the flux of X alone.
        return np.array([c.d * y[1] + c.d_s * c.z,
                         c.e * (c.U * y[0] - p[0]) + c.e_s * (c.U * c.N - K_s)
                         + c.e * c.U_s * c.N])

    def bc(left: Array, right: Array, p: Array) -> Array:
        return np.array([left[0], left[1], right[0] - gamma_s_1])

    mesh = bg.lapse.x  # reuse the accepted background collocation mesh
    evolution = solve_bvp(rhs, bc, mesh, np.zeros((2, mesh.size)), p=np.array([-4.0]),
                          S=np.diag([0.0, -2.0]), tol=num.bvp_tol, bc_tol=num.bc_tol,
                          max_nodes=num.max_nodes, fun_jac=None, bc_jac=None, verbose=0)
    if not evolution.success:
        raise LTBNumericalError(
            f"Evolution BVP status {evolution.status}: {evolution.message}")
    K_ss = float(evolution.p[0])

    def lambda_s_at(c: _Coefficients, X: Array) -> Array:
        return X / c.gamma - c.lam * c.gamma_s / c.gamma

    # Post-checks on nodes, midpoints and the background sample grid.
    r = np.unique(np.concatenate((bg.solution.r, evolution.x,
                                  (evolution.x[:-1] + evolution.x[1:]) / 2)))
    r = r[np.r_[True, np.diff(r) > 64 * np.finfo(float).eps]]
    bg.sample(r)  # background acceptance bounds on the extended grid
    c = coefficients(r)
    values, derivs = evolution.sol(r), evolution.sol(r, 1)
    X, Z = values
    finite(values, derivs, K_ss)
    Z_over_r = np.divide(Z, r, out=np.zeros_like(r), where=r != 0)
    Z_over_r[r == 0] = derivs[1, r == 0]
    eq_X = (derivs[0], c.d * Z, c.d_s * c.z)
    eq_Z = (derivs[1], 2 * Z_over_r, c.e * c.U * X, c.e * K_ss,
            c.e_s * (c.U * c.N - K_s), c.e * c.U_s * c.N)
    res_X = np.abs(eq_X[0] - eq_X[1] - eq_X[2]) / np.maximum(
        1, np.max(np.abs(np.array(eq_X)), axis=0))
    res_Z = np.abs(eq_Z[0] + eq_Z[1] - eq_Z[2] + eq_Z[3] - eq_Z[4] - eq_Z[5]) / np.maximum(
        1, np.max(np.abs(np.array(eq_Z)), axis=0))
    equation = float(max(np.max(res_X), np.max(res_Z)))
    boundary = float(max(abs(X[0]), abs(Z[0]), abs(X[-1] - gamma_s_1)))
    lambda_s = lambda_s_at(c, X)
    lambda_s_boundary = float(max(abs(lambda_s[0]), abs(lambda_s[-1])))

    def averages(order: int) -> Array:
        z, w = gauss(order)
        model = bg.solution.model
        edges = (0.0, model.r_c, model.r_o, 1.0)
        rq = np.concatenate([a + (b - a) * z for a, b in zip(edges[:-1], edges[1:])])
        weights = np.concatenate([(b - a) * w for a, b in zip(edges[:-1], edges[1:])])
        bg.sample(rq)
        q = coefficients(rq)
        lam_s = lambda_s_at(q, evolution.sol(rq)[0])
        # BMR (4.5), (4.9), (4.12): dust-intrinsic measure 4*pi*A*R**2 dr, A NOT B.
        measure = weights * 4 * np.pi * q.A * q.R**2
        V = float(np.sum(measure))

        def avg(value: Array) -> float:
            return float(np.dot(measure, value) / V)

        E = q.lam * q.Theta
        mean_E = avg(E)
        var_E = avg((E - mean_E)**2)  # centred variance
        P = avg(q.Theta * lam_s)
        L2D = avg(q.lam**2 * q.D)
        J = mean_E / 3
        J_s = (P - L2D + var_E) / 3
        rho_lam = avg(q.lam**2 * q.G_rho)
        Q = (2 / 3) * var_E - 2 * avg(q.lam**2 * q.sigma2)
        return np.array([J, P, L2D, var_E, J_s, rho_lam, Q])

    coarse, fine = averages(num.quadrature_order), averages(2 * num.quadrature_order)
    finite(coarse, fine)
    quadrature = float(np.max(np.abs(fine[:5] - coarse[:5]) / np.maximum(1, np.abs(fine[:5]))))
    J, P, L2D, var_E, J_s, rho_lam, Q = (float(x) for x in fine)
    ray_terms = np.array([3 * J_s, 3 * J**2, 4 * np.pi * rho_lam, Q, P])
    raychaudhuri = float(abs(3 * (J_s + J**2) + 4 * np.pi * rho_lam - Q - P)
                         / max(1, np.max(np.abs(ray_terms))))
    J_background = bg.solution.averages.J * bg.s_c
    background_J = abs(J - J_background) / max(1, abs(J_background))
    if not J > 0:
        raise LTBNumericalError("Nonpositive mean expansion rate; q_c undefined")
    q_c = -1 - J_s / J**2
    phi_center = float(bg.lapse.sol(np.array([0.0]))[0, 0])
    finite(equation, boundary, lambda_s_boundary, quadrature, raychaudhuri,
           background_J, q_c)
    lambda_s_gate = 4 * num.bc_tol * (1 + abs(gamma_s_1))
    if (boundary > 4 * num.bc_tol or lambda_s_boundary > lambda_s_gate
            or max(equation, quadrature, raychaudhuri, background_J) > num.check_tol):
        raise LTBNumericalError(
            f"Unresolved evolution checks: equation={equation:g}, boundary={boundary:g}, "
            f"lambda_s_boundary={lambda_s_boundary:g}, quadrature={quadrature:g}, "
            f"raychaudhuri={raychaudhuri:g}, background_J={background_J:g}")

    s_c = bg.s_c
    grid = bg.solution.r
    cg = coefficients(grid)
    X_grid = evolution.sol(grid)[0]
    residuals = EvolutionResiduals(float(np.max(evolution.rms_residuals)), equation,
                                   boundary, lambda_s_boundary, quadrature,
                                   raychaudhuri, background_J, phi_center,
                                   len(evolution.x))
    return CMCEvolution(
        bg.solution,
        dimensional(K_ss, s_c, -3),
        _readonly(dimensional(X_grid, s_c, -1)),
        _readonly(dimensional(lambda_s_at(cg, X_grid), s_c, -1)),
        _readonly(dimensional(cg.gamma_s, s_c, -1)),
        dimensional(P, s_c, -2),
        dimensional(J_s, s_c, -2),
        float(q_c),
        dimensional(L2D, s_c, -2),
        dimensional(var_E, s_c, -2),
        residuals,
    )
