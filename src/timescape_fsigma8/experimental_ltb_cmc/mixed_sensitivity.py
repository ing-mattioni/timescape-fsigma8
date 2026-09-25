"""Single-age mixed sensitivity delta(d/dc) of ONE accepted LTB--CMC background.

``delta`` is d/dkappa_star at fixed central age c=s_c, m0, r_c, r_o, G,
material labels r and domain [0,1] (right derivative at kappa_star=0);
``_c`` (``_s`` in the evolution module) is d/dc at fixed physical
parameters along the CMC section family. In internal units the length scale
L = s_c of the evaluated point stays fixed: neither L nor m0/L is
differentiated. With N = N_c, X = N_c_c, Z = z_c, K1 = K_s, K2 = K_ss and
the kappa_star sensitivities n = delta_N_c, zeta = delta_z, k1 = delta_K_s,
the unknowns are MX = delta_X, MZ = delta_Z and MK2 = delta_K2:

    MX_r = d*MZ + delta_d*Z + d_c*zeta + delta_d_c*z
    MZ_r = e*(U*MX - MK2) - 2*MZ/r + source
    source = delta_e*(U*X-K2) + e*delta_U*X + delta_e_c*(U*N-K1)
             + e_c*(delta_U*N + U*n - k1) + delta_e*U_c*N + e*delta_U_c*N + e*U_c*n
    MX(0) = 0, MZ(0) = 0, MX(1) = delta_gamma_c(1)

with d = B/a**2, e = B*a**2, B = A/gamma. The homogeneous problem is
L[MX] = MK2 (positive sign), so MK2 is fixed through phi(0) > 0.
delta_d_c, delta_e_c, delta_U_c and delta_gamma_c are the analytic
kappa_star derivatives of the evolution coefficients, built from the
accepted background, evolution and kappa_star states; derivatives in r of
delta quantities come from their equations, never from differentiating
interpolants of public sampled profiles. No finite difference is used.

Provenance: linearization of the evolution flux BVP (G07 (6.90)) and of the
BMR arXiv:1912.04213v2 (4.5), (4.9), (4.12) intrinsic averages with measure
4*pi*A*R**2 dr. Conditional research derivation of the user contract; NOT
a published theorem and NOT derived from the frozen Timescape runtime.
Classification: DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

import numpy as np
from scipy.integrate import solve_bvp

from .evolution import CMCEvolution, _EvolutionState, _evolve_state
from .geometry import (Array, LTBModel, LTBNumericalError, Numerics, dimensional,
                       finite, gauss)
from .kappa_sensitivity import (KappaSensitivity, _KappaState, _sensitivity_state,
                                _variations)
from .solver import CMCSolution, _Background, _checked_background, _readonly


@dataclass(frozen=True)
class MixedSensitivityResiduals:
    """Dimensionless sampled/resolution diagnostics, NOT rigorous bounds.

    ``equation``: residuals of both mixed ODEs on nodes, midpoints and the
    sample grid, each normalized by max(1, absolute contributing terms).
    ``boundary``: MX(0), MZ(0), MX(1)-delta_gamma_c(1). ``lambda_boundary``:
    reconstructed delta_lambda_c(0), delta_lambda_c(1). ``quadrature``:
    Gauss orders n vs 2n. ``raychaudhuri``: the differentiated averaged
    Raychaudhuri identity, an ALGEBRAIC check sharing the construction.
    ``consistency``: J, P_lambda, J_c, delta_J, delta_rho_lambda and
    delta_Q_lambda recomputed here against the accepted background,
    evolution and kappa_star results. ``phi_center``: background phi(0)
    (internal units), through which MK2 is fixed.
    """

    bvp_rms: float
    equation: float
    boundary: float
    lambda_boundary: float
    quadrature: float
    raychaudhuri: float
    consistency: float
    phi_center: float
    nodes: int


@dataclass(frozen=True)
class MixedSensitivity:
    """Accepted delta(d/dc) at one central age; never an embedding.

    ``solution``, ``evolution`` and ``kappa`` are the accepted background,
    evolution and kappa_star sensitivity (background solved once). Profiles
    are sampled on ``solution.r`` and read-only. Dimensions (c=1):
    delta_K2 length**-3; delta_N_c_c, delta_gamma_c, delta_lambda_c
    length**-1; delta_P_lambda, delta_J_c, delta_lambda2_D (delta of
    <lambda**2 D>) and delta_var_E (delta Var(lambda*Theta)) length**-2;
    delta_q_c dimensionless. ``one_sided`` is True at kappa_star=0. No sign
    is imposed on any output.
    """

    solution: CMCSolution
    evolution: CMCEvolution
    kappa: KappaSensitivity
    one_sided: bool
    delta_K2: float
    delta_N_c_c: Array
    delta_gamma_c: Array
    delta_lambda_c: Array
    delta_P_lambda: float
    delta_J_c: float
    delta_q_c: float
    delta_lambda2_D: float
    delta_var_E: float
    residuals: MixedSensitivityResiduals

    scientific_classification: ClassVar[str] = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"


def solve_mixed_sensitivity(s_c: float, model: LTBModel,
                            numerics: Numerics = Numerics()) -> MixedSensitivity:
    """Solve the background once; reuse its evolution and kappa_star states.

    Then solve the mixed flux BVP (module docstring) with SciPy's
    singular-matrix treatment of -2*MZ/r, reconstruct
    delta_lambda_c = (MX - lambda_c*delta_gamma - gamma_c*delta_lambda
    - lambda*delta_gamma_c)/gamma and average directly. Invalid input raises
    LTBDomainError; numerical or representability failure raises
    LTBNumericalError; nothing partial is returned.
    """
    return _run(_checked_background(s_c, model, numerics), numerics)


def _run(background: _Background, numerics: Numerics) -> MixedSensitivity:
    try:
        with np.errstate(over="raise", divide="raise", invalid="raise"):
            evolution = _evolve_state(background, numerics)
            kappa = _sensitivity_state(background, numerics)
            return _mixed(background, evolution, kappa, numerics)
    except (FloatingPointError, OverflowError, ZeroDivisionError, RuntimeWarning) as exc:
        raise LTBNumericalError(f"Arithmetic/representation failure: {exc}") from exc


@dataclass(frozen=True)
class _MixedCoefficients:
    """Coefficients of the mixed BVP and reconstruction at radii r (internal)."""

    r: Array
    gamma: Array
    lam: Array
    lam_c: Array
    Theta: Array
    D: Array
    G_rho: Array
    sigma2: Array
    A: Array
    R: Array
    d: Array
    e: Array
    U: Array
    N: Array
    z: Array
    X: Array
    Z: Array
    gamma_c: Array
    d_c: Array
    e_c: Array
    U_c: Array
    zeta: Array
    n: Array
    d_gamma: Array
    d_lam: Array
    d_Theta: Array
    d_ln_rho: Array
    d_sigma2: Array
    eta: Array
    d_d: Array
    d_e: Array
    d_U: Array
    d_gamma_c: Array
    d_d_c: Array
    d_e_c: Array
    d_U_c: Array


def _mixed(bg: _Background, evo: _EvolutionState, kap: _KappaState,
           num: Numerics) -> MixedSensitivity:
    m, K, K1 = bg.geometry.m, bg.K, bg.K_s
    K2, dK, dK1 = evo.K_ss, kap.dK, kap.dKs
    a_center = (4.5 * m) ** (1 / 3)  # flat EdS centre at internal age 1
    cache: dict[bytes, _MixedCoefficients] = {}

    def coefficients(r: Array) -> _MixedCoefficients:
        key = r.tobytes()
        if key in cache:
            return cache[key]
        ce = evo.coefficients(r)          # background + evolution coefficients
        cs = kap.section(r)               # background + local kappa_star terms
        t = cs.t
        X, Z = evo.bvp.sol(r)
        dS, dxi = kap.dcmc.sol(r)
        n, zeta = kap.dlapse.sol(r)
        w = kap.lapse_variations(cs, dS, dxi)
        eta = _variations(cs, dS, dxi)[4]
        gamma, lam, Theta, A = ce.gamma, ce.lam, ce.Theta, ce.A
        centre = r == 0
        r_safe = np.where(centre, 1.0, r)  # no 0/0: centre uses exact limits
        # Total kappa_star variations on the section: d_geom + (d/ds)*delta_S.
        d_Hl = t.d_Hl + t.Hl_s * dS
        d_Theta = t.d_Theta - t.D * dS
        d_sigma2 = t.d_sigma2 + t.sigma2_s * dS
        d_lam = n / gamma - lam * w.d_gamma / gamma
        # r-derivatives of delta quantities from their own equations.
        f1, f2 = kap.cmc_terms(cs, dS, dxi, dK)
        dxi_r = np.where(centre, sum(f2) / 3, sum(f2) - 2 * dxi / r_safe)
        dN_r = w.d * w.d_ln_d * cs.z + w.d * zeta
        d_gamma_r = ((dxi * ce.xi_r + ce.xi * dxi_r) / gamma
                     - ce.xi * ce.xi_r * w.d_gamma / gamma**2)
        d_lam_r = (dN_r - d_lam * ce.gamma_r - lam * d_gamma_r - ce.lam_r * w.d_gamma) / gamma
        # delta of v_c, gamma_c, xi_c (v = xi/gamma, delta_v = delta_xi/gamma**3).
        d_v = dxi / gamma**3
        d_v_c = (d_lam_r / A - ce.lam_r * w.dA / A**2
                 - (d_v * ce.Hl * lam + ce.v * d_Hl * lam + ce.v * ce.Hl * d_lam))
        d_gamma_c = np.where(centre, 0.0, 3 * gamma**2 * w.d_gamma * ce.v * ce.v_s
                             + gamma**3 * (d_v * ce.v_s + ce.v * d_v_c))
        d_xi_c = 3 * gamma**2 * w.d_gamma * ce.v_s + gamma**3 * d_v_c
        d_xi_c_over_r = np.where(centre, -(a_center / 3) * ((2 / 3) * dK + dK1),
                                 d_xi_c / r_safe)
        # delta of kperp_c; Hp_age = -m/a**3 - Hp**2 at fixed r.
        d_Hp_age = 3 * m * w.d_a / ce.a**4 - 2 * ce.Hp * w.d_Hp
        d_kp_c = np.where(
            centre, dK1 / 3,
            -(d_gamma_c * ce.Hp + ce.gamma_s * w.d_Hp)
            - (w.d_gamma * ce.Hp_age * lam + gamma * d_Hp_age * lam + gamma * ce.Hp_age * d_lam)
            - (w.d_F_over_a * ce.xi_s_over_r + ce.F_over_a * d_xi_c_over_r)
            + w.dxi_over_r * ce.F_over_a * ce.Hp * lam
            + ce.xi_over_r * (w.d_F_over_a * ce.Hp * lam
                              + ce.F_over_a * (w.d_Hp * lam + ce.Hp * d_lam)))
        d_kl_c = dK1 - 2 * d_kp_c
        four_pi_G_rho = 4 * np.pi * ce.G_rho
        tilt = 2 * gamma**2 - 1
        bracket = -Theta * lam * tilt + 4 * gamma * ce.gamma_s
        d_bracket = (-d_Theta * lam * tilt - Theta * d_lam * tilt
                     - 4 * Theta * lam * gamma * w.d_gamma
                     + 4 * w.d_gamma * ce.gamma_s + 4 * gamma * d_gamma_c)
        d_U_c = np.where(
            centre, (2 / 3) * (dK * K1 + K * dK1),
            2 * w.d_kl * ce.kl_s + 2 * ce.kl * d_kl_c + 4 * w.d_kp * ce.kp_s
            + 4 * ce.kp * d_kp_c + four_pi_G_rho * (w.d_ln_rho * bracket + d_bracket))
        ratio_d = (ce.Hl - 2 * ce.Hp) * lam - ce.gamma_s / gamma
        ratio_e = Theta * lam - ce.gamma_s / gamma
        d_ratio = -d_gamma_c / gamma + ce.gamma_s * w.d_gamma / gamma**2
        d_d_c = (ce.d * w.d_ln_d * ratio_d
                 + ce.d * ((d_Hl - 2 * w.d_Hp) * lam + (ce.Hl - 2 * ce.Hp) * d_lam + d_ratio))
        d_e_c = ce.e * w.d_ln_e * ratio_e + ce.e * (d_Theta * lam + Theta * d_lam + d_ratio)
        lam_c = X / gamma - lam * ce.gamma_s / gamma
        finite(X, Z, n, zeta, dxi_r, d_lam_r, d_v_c, d_gamma_c, d_kp_c, d_U_c, d_d_c, d_e_c)
        result = _MixedCoefficients(
            r, gamma, lam, lam_c, Theta, ce.D, ce.G_rho, ce.sigma2, A, ce.R, ce.d, ce.e,
            ce.U, ce.N, ce.z, X, Z, ce.gamma_s, ce.d_s, ce.e_s, ce.U_s, zeta, n,
            w.d_gamma, d_lam, d_Theta, w.d_ln_rho, d_sigma2, eta,
            ce.d * w.d_ln_d, ce.e * w.d_ln_e, w.d_U, d_gamma_c, d_d_c, d_e_c, d_U_c)
        if len(cache) > 16:
            cache.clear()
        cache[key] = result
        return result

    def terms(c: _MixedCoefficients, MX: Array, MZ: Array, MK2: float):
        g1 = (c.d * MZ, c.d_d * c.Z, c.d_c * c.zeta, c.d_d_c * c.z)
        g2 = (c.e * c.U * MX, -c.e * MK2,
              c.d_e * (c.U * c.X - K2), c.e * c.d_U * c.X,
              c.d_e_c * (c.U * c.N - K1), c.e_c * (c.d_U * c.N + c.U * c.n - dK1),
              c.d_e * c.U_c * c.N, c.e * c.d_U_c * c.N, c.e * c.U_c * c.n)
        return g1, g2

    def rhs(r: Array, y: Array, p: Array) -> Array:
        g1, g2 = terms(coefficients(r), y[0], y[1], p[0])
        return np.array([sum(g1), sum(g2)])  # S matrix adds -2*MZ/r

    d_gamma_c_1 = float(coefficients(np.array([1.0])).d_gamma_c[0])

    def bc(left: Array, right: Array, p: Array) -> Array:
        return np.array([left[0], left[1], right[0] - d_gamma_c_1])

    mesh = np.unique(np.concatenate((evo.bvp.x, kap.dlapse.x)))
    mesh = mesh[np.r_[True, np.diff(mesh) > 64 * np.finfo(float).eps]]
    mixed = solve_bvp(rhs, bc, mesh, np.zeros((2, mesh.size)), p=np.array([0.0]),
                      S=np.diag([0.0, -2.0]), tol=num.bvp_tol, bc_tol=num.bc_tol,
                      max_nodes=num.max_nodes, fun_jac=None, bc_jac=None, verbose=0)
    if not mixed.success:
        raise LTBNumericalError(f"Mixed sensitivity BVP status {mixed.status}: {mixed.message}")
    MK2 = float(mixed.p[0])

    def d_lambda_c(c: _MixedCoefficients, MX: Array) -> Array:
        return (MX - c.lam_c * c.d_gamma - c.gamma_c * c.d_lam - c.lam * c.d_gamma_c) / c.gamma

    # Post-checks on the sample grid, the node set and its midpoints.
    r = np.unique(np.concatenate((bg.solution.r, mixed.x, (mixed.x[:-1] + mixed.x[1:]) / 2)))
    r = r[np.r_[True, np.diff(r) > 64 * np.finfo(float).eps]]
    bg.sample(r)  # background acceptance bounds on the extended grid
    c = coefficients(r)
    (MX, MZ), (MX_r, MZ_r) = mixed.sol(r), mixed.sol(r, 1)
    finite(MX, MZ, MX_r, MZ_r, MK2)
    g1, g2 = terms(c, MX, MZ, MK2)
    MZ_over_r = np.divide(MZ, r, out=np.zeros_like(r), where=r != 0)
    MZ_over_r[r == 0] = MZ_r[r == 0]

    def residual(deriv: Array, singular: Array, parts: tuple) -> float:
        total = deriv + singular - sum(parts)
        scale = np.max(np.abs(np.array((deriv, singular, *parts))), axis=0)
        return float(np.max(np.abs(total) / np.maximum(1, scale)))

    equation = max(residual(MX_r, np.zeros_like(r), g1), residual(MZ_r, 2 * MZ_over_r, g2))
    boundary = float(max(abs(MX[0]), abs(MZ[0]), abs(MX[-1] - d_gamma_c_1)))
    dlc = d_lambda_c(c, MX)
    lambda_boundary = float(max(abs(dlc[0]), abs(dlc[-1])))

    def averages(order: int) -> tuple[Array, Array]:
        z, w = gauss(order)
        model = bg.solution.model
        edges = (0.0, model.r_c, model.r_o, 1.0)
        rq = np.concatenate([a + (b - a) * z for a, b in zip(edges[:-1], edges[1:])])
        weights = np.concatenate([(b - a) * w for a, b in zip(edges[:-1], edges[1:])])
        bg.sample(rq)
        q = coefficients(rq)
        # BMR (4.5), (4.9), (4.12): intrinsic measure 4*pi*A*R**2 dr, A NOT B.
        measure = weights * 4 * np.pi * q.A * q.R**2
        V = float(np.sum(measure))

        def avg(value: Array) -> float:
            return float(np.dot(measure, value) / V)

        eta_c = q.eta - avg(q.eta)

        def cov(value: Array) -> float:  # centred Cov(X, eta)
            return avg((value - avg(value)) * eta_c)

        dlam_c = d_lambda_c(q, mixed.sol(rq)[0])
        E = q.lam * q.Theta
        dE = q.d_lam * q.Theta + q.lam * q.d_Theta
        E_c = E - avg(E)
        J = avg(E) / 3
        dJ = (avg(dE) + cov(E)) / 3
        P = avg(q.Theta * q.lam_c)
        dP = avg(q.d_Theta * q.lam_c + q.Theta * dlam_c) + cov(q.Theta * q.lam_c)
        L2D = avg(q.lam**2 * q.D)
        dD = ((2 / 3) * q.Theta * q.d_Theta + 2 * q.d_sigma2
              + 4 * np.pi * q.G_rho * q.d_ln_rho)
        dL2D = avg(2 * q.lam * q.d_lam * q.D + q.lam**2 * dD) + cov(q.lam**2 * q.D)
        var = avg(E_c**2)
        d_var = 2 * avg(E_c * dE) + cov(E_c**2)
        J_c = (P - L2D + var) / 3
        dJ_c = (dP - dL2D + d_var) / 3
        d_rho = (avg(2 * q.lam * q.d_lam * q.G_rho + q.lam**2 * q.G_rho * q.d_ln_rho)
                 + cov(q.lam**2 * q.G_rho))
        d_l2s = (avg(2 * q.lam * q.d_lam * q.sigma2 + q.lam**2 * q.d_sigma2)
                 + cov(q.lam**2 * q.sigma2))
        dQ = (2 / 3) * d_var - 2 * d_l2s
        values = np.array([dP, dJ_c, dL2D, d_var])
        extra = np.array([J, dJ, P, J_c, d_rho, dQ])
        return values, extra

    coarse, _ = averages(num.quadrature_order)
    fine, (J, dJ, P, J_c, d_rho, dQ) = averages(2 * num.quadrature_order)
    finite(coarse, fine)
    quadrature = float(np.max(np.abs(fine - coarse) / np.maximum(1, np.abs(fine))))
    dP, dJ_c, dL2D, d_var = (float(x) for x in fine)
    # ALGEBRAIC: delta of 3*(J_c+J**2) + 4*pi*G*rho_lambda - Q - P = 0.
    ray_terms = np.array([3 * dJ_c, 6 * J * dJ, 4 * np.pi * d_rho, dQ, dP])
    raychaudhuri = float(abs(ray_terms[0] + ray_terms[1] + ray_terms[2] - ray_terms[3]
                             - ray_terms[4]) / max(1, np.max(np.abs(ray_terms))))
    s_c, model = bg.s_c, bg.solution.model
    ev, ks = evo.result, kap.result
    accepted = np.array([bg.solution.averages.J * s_c, ev.P_lambda * s_c**2, ev.J_s * s_c**2,
                         ks.delta_J * s_c, ks.delta_rho_lambda * model.G * s_c**2,
                         ks.delta_Q_lambda * s_c**2])
    recomputed = np.array([J, P, J_c, dJ, d_rho, dQ])
    consistency = float(np.max(np.abs(recomputed - accepted) / np.maximum(1, np.abs(accepted))))
    if not J > 0:
        raise LTBNumericalError("Nonpositive mean expansion rate; delta_q_c undefined")
    d_q_c = -dJ_c / J**2 + 2 * J_c * dJ / J**3
    phi_center = float(bg.lapse.sol(np.array([0.0]))[0, 0])
    finite(equation, boundary, lambda_boundary, quadrature, raychaudhuri, consistency, d_q_c)
    lambda_gate = 4 * num.bc_tol * (1 + abs(d_gamma_c_1))
    if (boundary > 4 * num.bc_tol or lambda_boundary > lambda_gate
            or max(equation, quadrature, raychaudhuri, consistency) > num.check_tol):
        raise LTBNumericalError(
            f"Unresolved mixed sensitivity checks: equation={equation:g}, boundary={boundary:g}, "
            f"lambda_boundary={lambda_boundary:g}, quadrature={quadrature:g}, "
            f"raychaudhuri={raychaudhuri:g}, consistency={consistency:g}")

    grid = bg.solution.r
    cg = coefficients(grid)
    MX_grid = mixed.sol(grid)[0]
    residuals = MixedSensitivityResiduals(
        float(np.max(mixed.rms_residuals)), equation, boundary, lambda_boundary,
        quadrature, raychaudhuri, consistency, phi_center, len(mixed.x))
    return MixedSensitivity(
        bg.solution, ev, ks, model.kappa_star == 0,
        dimensional(MK2, s_c, -3),
        _readonly(dimensional(MX_grid, s_c, -1)),
        _readonly(dimensional(cg.d_gamma_c, s_c, -1)),
        _readonly(dimensional(d_lambda_c(cg, MX_grid), s_c, -1)),
        dimensional(dP, s_c, -2), dimensional(dJ_c, s_c, -2), float(d_q_c),
        dimensional(dL2D, s_c, -2), dimensional(d_var, s_c, -2),
        residuals,
    )
