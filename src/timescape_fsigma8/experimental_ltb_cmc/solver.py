"""Single-age conditional LTB--CMC BVP. No tracker or Phase 1F-D imports.

G07 = Gourgoulhon, arXiv:gr-qc/0703035, Eqs. (4.63)--(4.65), (6.90).
BMR = Buchert--Mourier--Roy, arXiv:1912.04213v2, Eqs. (4.5), (4.9),
(4.12), (4.16), (4.18), (4.20), (E.2). The radial equations below are
conditional reductions of these equations, with the user's external
profile and anchors. They are NOT published Timescape embedding equations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, ClassVar

import numpy as np
from scipy.integrate import solve_bvp

from .geometry import (Array, Geometry, LTBModel, LTBDomainError,
                       LTBNumericalError, Numerics, dimensional, finite,
                       gauss, scalar)


@dataclass(frozen=True)
class Averages:
    """Dust-intrinsic averages, not induced-slice-volume averages.

    V: length**3; M_rest: mass; rho0/rho_lambda: mass/length**3;
    J: 1/length; Q_lambda/R_lambda: 1/length**2 (c=1).
    """

    V: float
    M_rest: float
    rho0: float
    J: float
    rho_lambda: float
    Q_lambda: float
    R_lambda: float


@dataclass(frozen=True)
class Residuals:
    """Dimensionless sampled/resolution diagnostics, NOT rigorous bounds.

    Equation residuals use max(1, absolute contributing terms); mass uses
    M_rest, Hamilton uses max(1, absolute terms), after scaling by s_c.
    bvp_rms values use SciPy's documented RMS normalization.
    """

    cmc_rms: float
    lapse_rms: float
    cmc_equation: float
    lapse_equation: float
    boundary: float
    mass: float
    hamilton: float
    quadrature: float
    cmc_nodes: int
    lapse_nodes: int
    lapse_lower_bound: float


@dataclass(frozen=True)
class CMCSolution:
    """Numerically accepted conditional background, never an embedding.

    Arrays are sampled on r and read-only. S,A,R have length units;
    Theta,K_star,k_perp,k_parallel have inverse length; sigma2,R_u,U,K_s
    inverse length squared; phi length squared; rho mass/length cubed.
    xi,gamma,v,N_c,lambda_,w0 are dimensionless. R_r is at fixed proper
    age. lambda_ is dS/ds_c, not a physical wall lapse. No all-time claim.
    """

    model: LTBModel
    numerics: Numerics
    s_c: float
    K_star: float
    K_s: float
    r: Array
    S: Array
    xi: Array
    gamma: Array
    v: Array
    A: Array
    R: Array
    R_r: Array
    Theta: Array
    sigma2: Array
    rho: Array
    R_u: Array
    k_perp: Array
    k_parallel: Array
    U: Array
    phi: Array
    w0: Array
    N_c: Array
    lambda_: Array
    averages: Averages
    residuals: Residuals

    scientific_classification: ClassVar[str] = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"


def _readonly(value: Array) -> Array:
    value = np.array(value, dtype=float, copy=True)
    value.setflags(write=False)
    return value


@dataclass(frozen=True)
class _Background:
    """Internal accepted background in s_c-scaled units; never public output.

    It keeps the dense collocation interpolants (``cmc.sol``, ``lapse.sol``)
    and the section/sample evaluators of one accepted solve, so that later
    single-age computations reuse them instead of re-solving or
    differentiating the public sampled grids.  ``K`` and ``K_s`` are the
    dimensionless eigenparameters (lengths divided by s_c).
    """

    s_c: float
    geometry: Geometry
    cmc: Any
    lapse: Any
    K: float
    K_s: float
    gamma_b: float
    section: Callable[[Array], tuple]
    sample: Callable[[Array], tuple]
    solution: CMCSolution


def solve_cmc(s_c: float, model: LTBModel,
              numerics: Numerics = Numerics()) -> CMCSolution:
    """Solve one age with S(0)=S(1)=s_c and unknown K=-div(n).

    G07 Eqs. (4.63), (6.90), with the specified LTB metric/profile.
    Everything is internally scaled by s_c. Adaptive singular-endpoint
    collocation avoids assuming a regular shooting bracket. SciPy's
    forward-difference Jacobian is used (fun_jac=None); all solver
    tolerances/node limits are explicit. Non-convergence, an invalid
    trial or an under-resolved check raises LTBNumericalError, not a
    non-existence verdict. No partial solution is returned.
    """
    return _checked_background(s_c, model, numerics).solution


def _checked_background(s_c: float, model: LTBModel, numerics: Numerics) -> _Background:
    """Validated accepted background with its internal dense state.

    Same input validation and arithmetic policy as ``solve_cmc``; used by
    the separate single-age evolution module without a second solve.
    """
    s_c = scalar(s_c, "s_c")
    if s_c <= 0:
        raise LTBDomainError("s_c must be positive")
    if not isinstance(model, LTBModel) or not isinstance(numerics, Numerics):
        raise LTBDomainError("Require LTBModel and Numerics instances")
    try:
        with np.errstate(over="raise", divide="raise", invalid="raise"):
            return _solve_background(s_c, model, numerics)
    except (FloatingPointError, OverflowError, ZeroDivisionError, RuntimeWarning) as exc:
        raise LTBNumericalError(f"Arithmetic/representation failure: {exc}") from exc


def _solve(s_c: float, model: LTBModel, num: Numerics) -> CMCSolution:
    return _solve_background(s_c, model, num).solution


def _solve_background(s_c: float, model: LTBModel, num: Numerics) -> _Background:
    geometry = Geometry(model, s_c, num)
    transition = np.linspace(model.r_c, model.r_o, 11)
    if len(np.unique(transition)) != 11:
        raise LTBNumericalError("Transition width is not spatially representable")
    mesh = np.unique(np.concatenate((np.linspace(0, 1, num.initial_nodes), transition)))
    # Coalesce roundoff-neighbours from the two grids before collocation.
    mesh = mesh[np.r_[True, np.diff(mesh) > 64 * np.finfo(float).eps]]

    def cmc_rhs(r: Array, y: Array, p: Array) -> Array:
        # G07 (4.63), K=-div(n), n=gamma*d_s+(xi/A)*d_r.
        # The singular matrix supplies -2*xi/r; R_r is at FIXED s.
        g = geometry.at(y[0], r)
        gamma = np.hypot(1, y[1])
        return np.array([g.A * y[1] / gamma,
                         -g.A * (p[0] + gamma * g.Theta) - 2 * g.radial_extra * y[1]])

    def cmc_bc(left: Array, right: Array, p: Array) -> Array:
        return np.array([left[0] - 1, right[0] - 1, left[1]])

    initial = np.array([np.ones_like(mesh), np.zeros_like(mesh)])
    cmc = solve_bvp(cmc_rhs, cmc_bc, mesh, initial, p=np.array([-2.0]),
                    S=np.diag([0.0, -2.0]), tol=num.bvp_tol, bc_tol=num.bc_tol,
                    max_nodes=num.max_nodes, fun_jac=None, bc_jac=None, verbose=0)
    if not cmc.success:
        raise LTBNumericalError(f"CMC BVP status {cmc.status}: {cmc.message}")
    K = float(cmc.p[0])

    def section(r: Array):
        y = cmc.sol(r)
        g = geometry.at(y[0], r)
        xi = y[1]
        gamma = np.hypot(1, xi)
        B = g.A / gamma
        # G07 (4.63); exact regular centre is K/3, no 0/0 evaluation.
        xi_over_r = np.divide(xi, r, out=np.zeros_like(r), where=r != 0)
        kp = -(gamma * g.a_s / g.a + xi_over_r * g.sqrt_energy / g.a)
        kp = np.where(r == 0, K / 3, kp)
        kl = K - 2 * kp
        # G07 (6.90), restoring G: E+stress = rho*(2*gamma**2-1).
        U = kl**2 + 2 * kp**2 + 4 * np.pi * g.G_rho * (2 * gamma**2 - 1)
        finite(y, gamma, B, kp, kl, U)
        return y, g, gamma, B, kp, kl, U

    def lapse_rhs(r: Array, y: Array) -> Array:
        _, g, _, B, _, _, U = section(r)
        # G07 (6.90), flux z=(a**2/B)*y'; singular part -2*z/r.
        return np.array([B / g.a**2 * y[1], B * g.a**2 * (U * y[0] - 1),
                         B / g.a**2 * y[3], B * g.a**2 * U * y[2]])

    def lapse_bc(left: Array, right: Array) -> Array:
        return np.array([left[1], left[3], right[0], right[2] - 1])

    guess = np.array([0.1 * (1 - cmc.x**2), np.zeros_like(cmc.x),
                      np.ones_like(cmc.x), np.zeros_like(cmc.x)])
    lapse = solve_bvp(lapse_rhs, lapse_bc, cmc.x, guess,
                      S=np.diag([0.0, -2.0, 0.0, -2.0]), tol=num.bvp_tol,
                      bc_tol=num.bc_tol, max_nodes=num.max_nodes,
                      fun_jac=None, bc_jac=None, verbose=0)
    if not lapse.success:
        raise LTBNumericalError(f"Lapse BVP status {lapse.status}: {lapse.message}")
    phi0, w00 = float(lapse.sol(0)[0]), float(lapse.sol(0)[2])
    gamma_b = float(np.hypot(1, cmc.sol(1)[1]))
    if min(phi0, w00) < np.finfo(float).tiny:
        raise LTBNumericalError("Positive central lapse basis not resolved/representable")
    # Linear superposition of G07 (6.90) with both anchor derivatives.
    K_s = (1 - gamma_b * w00) / phi0
    lower_bound = min(1.0, gamma_b * w00)

    def sample(r: Array):
        y, g, gamma, B, kp, kl, U = section(r)
        basis = lapse.sol(r)
        N = gamma_b * basis[2] + K_s * basis[0]
        lam = N / gamma
        finite(N, lam, basis)
        if (np.any(y[0] <= 2 / 3) or np.any(y[0] >= 1.5)
                or np.any(N <= 0) or np.any(lam <= 0)
                or np.any(np.abs(y[1] / gamma) >= 1)):
            raise LTBNumericalError("Sampled age/tilt/lapse bounds failed; investigate numerics")
        if np.min(N) < lower_bound - num.check_tol * max(1, lower_bound):
            raise LTBNumericalError("Sampled analytic lapse lower bound not resolved")
        if np.any(g.Theta * y[0] < 2 - num.check_tol) or np.any(g.Theta * y[0] >= 3):
            raise LTBNumericalError("Local expansion bounds failed")
        return y, g, gamma, B, kp, kl, U, basis, N, lam

    def integrate(order: int) -> tuple[Array, float]:
        z, w = gauss(order)
        edges = (0.0, model.r_c, model.r_o, 1.0)
        r = np.concatenate([a + (b - a) * z for a, b in zip(edges[:-1], edges[1:])])
        weights = np.concatenate([(b - a) * w for a, b in zip(edges[:-1], edges[1:])])
        _, g, _, _, _, _, _, _, _, lam = sample(r)
        # BMR (4.5), (4.9), (4.12), (4.18), (4.20): A, NOT B.
        measure = weights * 4 * np.pi * g.A * g.R**2
        V = float(np.sum(measure))
        avg = lambda value: float(np.dot(measure, value) / V)
        h = lam * g.Theta
        mean_h = avg(h)
        J = mean_h / 3
        rho_lam = avg(lam**2 * g.G_rho)
        Q = (2 / 3) * avg((h - mean_h)**2) - 2 * avg(lam**2 * g.sigma2)
        Ru = avg(lam**2 * g.R_u)
        # S10 (3) and BMR intrinsic measure: proper REST mass, not m(1)/G.
        mass = float(np.dot(weights, 3 * geometry.m * r**2 / g.sqrt_energy))
        mass_res = abs(float(np.dot(measure, g.G_rho)) - mass) / mass
        return np.array([V, mass, J, rho_lam, Q, Ru]), mass_res

    coarse, _ = integrate(num.quadrature_order)
    fine, mass_res = integrate(2 * num.quadrature_order)
    qerr = float(np.max(np.abs(fine - coarse) / np.maximum(1, np.abs(fine))))
    V, mass, J, rho_lam, Q, Ru = fine
    ham_terms = np.array([3 * J**2, 8 * np.pi * rho_lam, (Ru + Q) / 2])
    ham_res = float(abs(ham_terms[0] - ham_terms[1] + ham_terms[2])
                    / max(1, np.max(np.abs(ham_terms))))

    r = np.unique(np.concatenate((np.linspace(0, 1, num.check_nodes), cmc.x, lapse.x,
                                  (cmc.x[:-1] + cmc.x[1:]) / 2,
                                  (lapse.x[:-1] + lapse.x[1:]) / 2)))
    r = r[np.r_[True, np.diff(r) > 64 * np.finfo(float).eps]]
    y, g, gamma, B, kp, kl, U, basis, N, lam = sample(r)
    yd = cmc.sol(r, 1)
    xi_over_r = np.divide(y[1], r, out=np.zeros_like(r), where=r != 0)
    xi_over_r[0] = yd[1, 0]
    reconstructed = -(gamma * g.Theta + yd[1] / g.A
                       + 2 * (xi_over_r + g.radial_extra * y[1]) / g.A)
    cmc_error = float(max(np.max(np.abs(reconstructed - K) / max(1, abs(K))),
                          np.max(np.abs(yd[0] - g.A * y[1] / gamma)
                                 / np.maximum(1, g.A))))
    bd = lapse.sol(r, 1)
    lapse_error = 0.0
    for value, flux, deriv, source in ((basis[0], basis[1], bd[1], 1.0),
                                       (basis[2], basis[3], bd[3], 0.0),
                                       (N, gamma_b * basis[3] + K_s * basis[1],
                                        gamma_b * bd[3] + K_s * bd[1], K_s)):
        flux_over_r = np.divide(flux, r, out=np.zeros_like(r), where=r != 0)
        flux_over_r[0] = deriv[0]
        applied = -(deriv + 2 * flux_over_r) / (B * g.a**2) + U * value
        denom = np.maximum(1, np.maximum(abs(source), np.abs(U * value)))
        lapse_error = max(lapse_error, float(np.max(np.abs(applied - source) / denom)))
    # Include the flux-definition residual, independent of the source equation.
    for value_d, flux in ((bd[0], basis[1]), (bd[2], basis[3])):
        lapse_error = max(lapse_error, float(np.max(
            np.abs(value_d - B / g.a**2 * flux) / np.maximum(1, np.abs(value_d)))))
    boundary = float(max(abs(y[0, 0] - 1), abs(y[0, -1] - 1), abs(y[1, 0]),
                         abs(N[0] - 1), abs(N[-1] - gamma_b), abs(basis[0, -1]),
                         abs(basis[2, -1] - 1), abs(basis[1, 0]), abs(basis[3, 0])))
    finite(fine, K, K_s, cmc_error, lapse_error, ham_res, mass_res, qerr)
    if not 2 - num.check_tol <= -K < 3:
        raise LTBNumericalError("CMC necessary K bound failed")
    if boundary > num.bc_tol * 4 or max(cmc_error, lapse_error, ham_res, mass_res, qerr) > num.check_tol:
        raise LTBNumericalError(
            f"Unresolved checks: CMC={cmc_error:g}, lapse={lapse_error:g}, "
            f"boundary={boundary:g}, mass={mass_res:g}, Hamilton={ham_res:g}, quadrature={qerr:g}")

    averages = Averages(dimensional(V, s_c, 3), dimensional(mass, s_c, 1, model.G),
                        dimensional(mass / V, s_c, -2, model.G), dimensional(J, s_c, -1),
                        dimensional(rho_lam, s_c, -2, model.G), dimensional(Q, s_c, -2),
                        dimensional(Ru, s_c, -2))
    residuals = Residuals(float(np.max(cmc.rms_residuals)), float(np.max(lapse.rms_residuals)),
                          cmc_error, lapse_error, boundary, mass_res, ham_res, qerr,
                          len(cmc.x), len(lapse.x), lower_bound)
    solution = CMCSolution(model, num, s_c, dimensional(K, s_c, -1), dimensional(K_s, s_c, -2),
                           _readonly(r), _readonly(dimensional(y[0], s_c, 1)), _readonly(y[1]),
                           _readonly(gamma), _readonly(y[1] / gamma),
                           _readonly(dimensional(g.A, s_c, 1)), _readonly(dimensional(g.R, s_c, 1)),
                           _readonly(dimensional(g.R_r, s_c, 1)), _readonly(dimensional(g.Theta, s_c, -1)),
                           _readonly(dimensional(g.sigma2, s_c, -2)),
                           _readonly(dimensional(g.G_rho, s_c, -2, model.G)),
                           _readonly(dimensional(g.R_u, s_c, -2)), _readonly(dimensional(kp, s_c, -1)),
                           _readonly(dimensional(kl, s_c, -1)), _readonly(dimensional(U, s_c, -2)),
                           _readonly(dimensional(basis[0], s_c, 2)), _readonly(basis[2]),
                           _readonly(N), _readonly(lam), averages, residuals)
    return _Background(s_c, geometry, cmc, lapse, K, K_s, gamma_b, section, sample, solution)
