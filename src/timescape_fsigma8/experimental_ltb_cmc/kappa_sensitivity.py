"""Single-age sensitivity d/dkappa_star of ONE accepted LTB--CMC background.

``delta_X`` is the partial derivative with respect to kappa_star at fixed
central age s_c, m0, r_c, r_o, G, material labels r and domain [0,1], with
kappa(r)=kappa_star*chi(r) for the already selected profile. At
kappa_star=0 it is a right derivative (the model domain is kappa_star>=0).
Profiles are total variations on the section at fixed r:
delta_X = delta_geom_X + X_s*delta_S, where delta_geom is the local
d/dkappa_star at fixed dust age (``Geometry.kappa_terms``, analytic
differentiation of the S10 age equation) and X_s the dust proper-age
derivative. No finite difference is used in production.

Provenance: linearization of the first solver's CMC reduction of G07
(4.63), of its G07 (6.90) lapse flux problem, and of the BMR
arXiv:1912.04213v2 (4.5), (4.9), (4.12), (4.18), (4.20) intrinsic averages
with measure 4*pi*A*R**2 dr. Conditional research derivation, NOT a
published theorem and NOT derived from the frozen Timescape runtime.
Classification: DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION. This is neither
a perturbation to a physically different Timescape geometry, nor an H1
response, nor a mass-compensated family: m0 is held fixed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

import numpy as np
from scipy.integrate import solve_bvp

from .geometry import (Array, LocalGeometry, LocalKappaTerms, LTBModel, LTBNumericalError,
                       Numerics, dimensional, finite, gauss)
from .solver import CMCSolution, _Background, _checked_background, _readonly


@dataclass(frozen=True)
class KappaSensitivityResiduals:
    """Dimensionless sampled/resolution diagnostics, NOT rigorous bounds.

    ``cmc_equation``/``lapse_equation``: residuals of the two linearized
    ODE pairs on nodes, midpoints and the sample grid, each normalized by
    max(1, absolute contributing terms). ``boundary``: delta_S(0),
    delta_S(1), delta_xi(0), delta_N_c(0), delta_z(0) and
    delta_N_c(1)-delta_gamma(1). ``lambda_boundary``: reconstructed
    delta_lambda(0), delta_lambda(1). ``quadrature``: Gauss orders n vs 2n
    for all averaged sensitivities. ``mass_identity``: local
    delta_ln_rho+eta+r**2*chi/(2*(1+r**2*kappa)). ``local_hamilton`` and
    ``hamilton``: differentiated local and averaged Hamilton constraints.
    Both identities are ALGEBRAIC checks sharing the construction; they do
    not replace independent derivative checks. ``phi_center`` is the
    background phi(0) (internal units): delta_K_s is fixed through it.
    """

    cmc_bvp_rms: float
    lapse_bvp_rms: float
    cmc_equation: float
    lapse_equation: float
    boundary: float
    lambda_boundary: float
    quadrature: float
    mass_identity: float
    local_hamilton: float
    hamilton: float
    background_J: float
    phi_center: float
    cmc_nodes: int
    lapse_nodes: int


@dataclass(frozen=True)
class KappaSensitivity:
    """Accepted d/dkappa_star at one central age; never an embedding.

    ``solution`` is the accepted background (solved once, not re-solved).
    Profiles are sampled on ``solution.r`` and read-only. kappa_star is
    dimensionless, so each delta_X has the dimensions of X (c=1):
    delta_K_star length**-1; delta_K_s length**-2; delta_S length;
    delta_xi, delta_gamma, delta_N_c, delta_lambda and the delta_ln_*
    dimensionless; delta_J length**-1; delta_rho_lambda mass/length**3;
    delta_Q_lambda and delta_R_lambda length**-2. ``one_sided`` is True at
    kappa_star=0 (right derivative). No sign is imposed on any output.
    """

    solution: CMCSolution
    one_sided: bool
    delta_K_star: float
    delta_K_s: float
    delta_S: Array
    delta_xi: Array
    delta_gamma: Array
    delta_N_c: Array
    delta_lambda: Array
    delta_ln_V: float
    delta_ln_M_rest: float
    delta_ln_rho0: float
    delta_J: float
    delta_rho_lambda: float
    delta_Q_lambda: float
    delta_R_lambda: float
    residuals: KappaSensitivityResiduals

    scientific_classification: ClassVar[str] = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"


def solve_kappa_sensitivity(s_c: float, model: LTBModel,
                            numerics: Numerics = Numerics()) -> KappaSensitivity:
    """Solve the background once, then the two linearized BVPs in sequence.

    1. CMC (G07 (4.63) reduction), unknowns delta_S, delta_xi, delta_K:
       delta_S_r = delta_A*xi/gamma + A*delta_xi/gamma**3,
       delta_xi_r = -delta_A*(K+gamma*Theta) - A*(delta_K + delta_gamma*Theta
                    + gamma*delta_Theta) - 2*delta_e*xi - 2*e*delta_xi - 2*delta_xi/r,
       e=R_r/R-1/r; delta_S(0)=delta_S(1)=delta_xi(0)=0.
    2. Lapse flux (G07 (6.90)), unknowns delta_N_c, delta_z, delta_K_s:
       delta_N_r = delta_d*z + d*delta_z,
       delta_z_r = delta_e2*(U*N_c-K_s) + e2*(delta_U*N_c + U*delta_N_c - delta_K_s)
                   - 2*delta_z/r,
       d=B/a**2, e2=B*a**2; delta_N_c(0)=0, delta_z(0)=0,
       delta_N_c(1)=delta_gamma(1).
    Both singular terms use SciPy's singular-matrix mechanism, as the first
    solver. Invalid input raises LTBDomainError; numerical or
    representability failure raises LTBNumericalError; nothing partial is
    returned.
    """
    return _run(_checked_background(s_c, model, numerics), numerics)


def _run(background: _Background, numerics: Numerics) -> KappaSensitivity:
    try:
        with np.errstate(over="raise", divide="raise", invalid="raise"):
            return _sensitivity(background, numerics)
    except (FloatingPointError, OverflowError, ZeroDivisionError, RuntimeWarning) as exc:
        raise LTBNumericalError(f"Arithmetic/representation failure: {exc}") from exc


@dataclass(frozen=True)
class _Section:
    """Background section quantities at radii r, with local kappa terms."""

    r: Array
    xi: Array
    gamma: Array
    g: LocalGeometry
    t: LocalKappaTerms
    B: Array
    kp: Array
    kl: Array
    U: Array
    N: Array
    z: Array


def _sensitivity(bg: _Background, num: Numerics) -> KappaSensitivity:
    m, K, K_s, gamma_b = bg.geometry.m, bg.K, bg.K_s, bg.gamma_b
    a_center = (4.5 * m) ** (1 / 3)  # flat EdS centre at internal age 1
    xi_over_r0 = -a_center * (K + 2) / 3
    cache: dict[bytes, _Section] = {}

    def section(r: Array) -> _Section:
        key = r.tobytes()
        if key in cache:
            return cache[key]
        y, _, gamma, B, kp, kl, U = bg.section(r)
        g, t = bg.geometry.kappa_terms(y[0], r)
        basis = bg.lapse.sol(r)
        N = gamma_b * basis[2] + K_s * basis[0]
        z = gamma_b * basis[3] + K_s * basis[1]  # same superposition as N_c
        result = _Section(r, y[1], gamma, g, t, B, kp, kl, U, N, z)
        if len(cache) > 16:
            cache.clear()
        cache[key] = result
        return result

    def cmc_terms(c: _Section, dS: Array, dxi: Array, dK: float):
        g, t, xi, gamma = c.g, c.t, c.xi, c.gamma
        dA = t.d_A + g.A * t.Hl * dS
        d_gamma = xi * dxi / gamma
        d_theta = t.d_Theta - t.D * dS
        d_extra = t.d_radial_extra + t.radial_extra_s * dS
        f1 = (dA * xi / gamma, g.A * dxi / gamma**3)
        f2 = (-dA * (K + gamma * g.Theta), -g.A * dK, -g.A * d_gamma * g.Theta,
              -g.A * gamma * d_theta, -2 * d_extra * xi, -2 * g.radial_extra * dxi)
        return f1, f2

    def cmc_rhs(r: Array, y: Array, p: Array) -> Array:
        f1, f2 = cmc_terms(section(r), y[0], y[1], p[0])
        return np.array([sum(f1), sum(f2)])  # S matrix adds -2*delta_xi/r

    def cmc_bc(left: Array, right: Array, p: Array) -> Array:
        return np.array([left[0], right[0], left[1]])

    dcmc = solve_bvp(cmc_rhs, cmc_bc, bg.cmc.x, np.zeros((2, bg.cmc.x.size)),
                     p=np.array([0.0]), S=np.diag([0.0, -2.0]), tol=num.bvp_tol,
                     bc_tol=num.bc_tol, max_nodes=num.max_nodes, fun_jac=None,
                     bc_jac=None, verbose=0)
    if not dcmc.success:
        raise LTBNumericalError(f"Sensitivity CMC BVP status {dcmc.status}: {dcmc.message}")
    dK = float(dcmc.p[0])

    def lapse_terms(c: _Section, dS: Array, dxi: Array, dN: Array, dz: Array, dKs: float):
        g, t, xi, gamma, r = c.g, c.t, c.xi, c.gamma, c.r
        centre = r == 0
        r_safe = np.where(centre, 1.0, r)  # no 0/0: centre uses exact limits
        d_gamma, d_a, dA, d_ln_rho, _ = _variations(c, dS, dxi)
        d_ln_d = dA / g.A - d_gamma / gamma - 2 * d_a / g.a
        d_ln_e = dA / g.A - d_gamma / gamma + 2 * d_a / g.a
        d, e = c.B / g.a**2, c.B * g.a**2
        d_Hp = t.d_Hp + t.Hp_s * dS
        xi_over_r = np.where(centre, xi_over_r0, xi / r_safe)
        dxi_over_r = np.where(centre, -a_center * dK / 3, dxi / r_safe)
        F_over_a = g.sqrt_energy / g.a
        d_F_over_a = F_over_a * (t.d_ln_F - d_a / g.a)
        d_kp = np.where(centre, dK / 3,
                        -(d_gamma * t.Hp + gamma * d_Hp + dxi_over_r * F_over_a
                          + xi_over_r * d_F_over_a))
        d_kl = dK - 2 * d_kp
        four_pi_G_rho = 4 * np.pi * g.G_rho
        d_U = (2 * c.kl * d_kl + 4 * c.kp * d_kp
               + four_pi_G_rho * (d_ln_rho * (2 * gamma**2 - 1) + 4 * gamma * d_gamma))
        g1 = (d * d_ln_d * c.z, d * dz)
        g2 = (e * d_ln_e * (c.U * c.N - K_s), e * d_U * c.N, e * c.U * dN, -e * dKs)
        return g1, g2

    def lapse_rhs(r: Array, y: Array, p: Array) -> Array:
        dS, dxi = dcmc.sol(r)
        g1, g2 = lapse_terms(section(r), dS, dxi, y[0], y[1], p[0])
        return np.array([sum(g1), sum(g2)])  # S matrix adds -2*delta_z/r

    xi_1 = float(bg.cmc.sol(np.array([1.0]))[1, 0])
    dxi_1 = float(dcmc.sol(np.array([1.0]))[1, 0])
    d_gamma_1 = xi_1 * dxi_1 / float(np.hypot(1, xi_1))

    def lapse_bc(left: Array, right: Array, p: Array) -> Array:
        return np.array([left[0], left[1], right[0] - d_gamma_1])

    mesh = np.unique(np.concatenate((bg.lapse.x, dcmc.x)))
    mesh = mesh[np.r_[True, np.diff(mesh) > 64 * np.finfo(float).eps]]
    dlapse = solve_bvp(lapse_rhs, lapse_bc, mesh, np.zeros((2, mesh.size)),
                       p=np.array([0.0]), S=np.diag([0.0, -2.0]), tol=num.bvp_tol,
                       bc_tol=num.bc_tol, max_nodes=num.max_nodes, fun_jac=None,
                       bc_jac=None, verbose=0)
    if not dlapse.success:
        raise LTBNumericalError(f"Sensitivity lapse BVP status {dlapse.status}: {dlapse.message}")
    dKs = float(dlapse.p[0])

    def over_r(value: Array, deriv: Array, r: Array) -> Array:
        out = np.divide(value, r, out=np.zeros_like(r), where=r != 0)
        out[r == 0] = deriv[r == 0]
        return out

    def residual(deriv: Array, singular: Array, terms: tuple) -> float:
        total = deriv + singular - sum(terms)
        scale = np.max(np.abs(np.array((deriv, singular, *terms))), axis=0)
        return float(np.max(np.abs(total) / np.maximum(1, scale)))

    # Post-checks on the sample grid, both BVP node sets and midpoints.
    r = np.unique(np.concatenate((bg.solution.r, dcmc.x, dlapse.x,
                                  (dcmc.x[:-1] + dcmc.x[1:]) / 2,
                                  (dlapse.x[:-1] + dlapse.x[1:]) / 2)))
    r = r[np.r_[True, np.diff(r) > 64 * np.finfo(float).eps]]
    bg.sample(r)  # background acceptance bounds on the extended grid
    c = section(r)
    (dS, dxi), (dS_r, dxi_r) = dcmc.sol(r), dcmc.sol(r, 1)
    (dN, dz), (dN_r, dz_r) = dlapse.sol(r), dlapse.sol(r, 1)
    finite(dS, dxi, dS_r, dxi_r, dN, dz, dN_r, dz_r, dK, dKs)
    f1, f2 = cmc_terms(c, dS, dxi, dK)
    g1, g2 = lapse_terms(c, dS, dxi, dN, dz, dKs)
    d_gamma = _variations(c, dS, dxi)[0]
    zero = np.zeros_like(r)
    cmc_equation = max(residual(dS_r, zero, f1),
                       residual(dxi_r, 2 * over_r(dxi, dxi_r, r), f2))
    lapse_equation = max(residual(dN_r, zero, g1),
                         residual(dz_r, 2 * over_r(dz, dz_r, r), g2))
    boundary = float(max(abs(dS[0]), abs(dS[-1]), abs(dxi[0]), abs(dN[0]),
                         abs(dz[0]), abs(dN[-1] - d_gamma_1)))
    lam = c.N / c.gamma
    d_lambda = dN / c.gamma - lam * d_gamma / c.gamma
    lambda_boundary = float(max(abs(d_lambda[0]), abs(d_lambda[-1])))
    mass_identity_grid = _mass_identity(c, dS, dxi)

    def averages(order: int) -> tuple[Array, float, float, float]:
        z, w = gauss(order)
        model = bg.solution.model
        edges = (0.0, model.r_c, model.r_o, 1.0)
        rq = np.concatenate([a + (b - a) * z for a, b in zip(edges[:-1], edges[1:])])
        weights = np.concatenate([(b - a) * w for a, b in zip(edges[:-1], edges[1:])])
        bg.sample(rq)
        q = section(rq)
        g, t = q.g, q.t
        qS, qxi = dcmc.sol(rq)
        qN, qz = dlapse.sol(rq)
        q_dgamma, _, _, q_dlnrho, eta = _variations(q, qS, qxi)
        lam_q = q.N / q.gamma
        dlam = qN / q.gamma - lam_q * q_dgamma / q.gamma
        # BMR (4.5), (4.9), (4.12): intrinsic measure 4*pi*A*R**2 dr, A NOT B.
        measure = weights * 4 * np.pi * g.A * g.R**2
        V = float(np.sum(measure))

        def avg(value: Array) -> float:
            return float(np.dot(measure, value) / V)

        eta_c = eta - avg(eta)

        def cov(value: Array) -> float:  # centred Cov(X, eta)
            return avg((value - avg(value)) * eta_c)

        rho = g.G_rho
        E = lam_q * g.Theta
        dE = dlam * g.Theta + lam_q * (t.d_Theta - t.D * qS)
        E_c = E - avg(E)
        J = avg(E) / 3
        dJ = (avg(dE) + cov(E)) / 3
        d_rho_lam = avg(2 * lam_q * dlam * rho + lam_q**2 * rho * q_dlnrho) + cov(lam_q**2 * rho)
        d_var = 2 * avg(E_c * dE) + cov(E_c**2)
        sigma2 = g.sigma2
        d_sigma2 = t.d_sigma2 + t.sigma2_s * qS
        d_l2s = avg(2 * lam_q * dlam * sigma2 + lam_q**2 * d_sigma2) + cov(lam_q**2 * sigma2)
        dQ = (2 / 3) * d_var - 2 * d_l2s
        Ru = g.R_u
        d_Ru = t.d_R_u + t.R_u_s * qS
        dR = avg(2 * lam_q * dlam * Ru + lam_q**2 * d_Ru) + cov(lam_q**2 * Ru)
        d_ln_V = avg(eta)
        d_ln_M = avg(rho * (eta + q_dlnrho)) / avg(rho)
        # Differentiated averaged Hamilton constraint 3J**2=8*pi*rho-(R+Q)/2.
        ham_terms = np.array([6 * J * dJ, 8 * np.pi * d_rho_lam, dR / 2, dQ / 2])
        hamilton = abs(ham_terms[0] - ham_terms[1] + ham_terms[2] + ham_terms[3]) / max(
            1, float(np.max(np.abs(ham_terms))))
        J_background = bg.solution.averages.J * bg.s_c
        J_check = abs(J - J_background) / max(1, abs(J_background))
        values = np.array([d_ln_V, d_ln_M, dJ, d_rho_lam, dQ, dR])
        return values, float(hamilton), _mass_identity(q, qS, qxi), float(J_check)

    coarse, _, _, _ = averages(num.quadrature_order)
    fine, hamilton, mass_identity_q, background_J = averages(2 * num.quadrature_order)
    finite(coarse, fine)
    quadrature = float(np.max(np.abs(fine - coarse) / np.maximum(1, np.abs(fine))))
    mass_identity = max(mass_identity_grid, mass_identity_q)
    lh_terms = (np.abs((4 / 3) * c.g.Theta * c.t.d_Theta), np.abs(2 * c.t.d_sigma2),
                np.abs(c.t.d_R_u), np.abs(16 * np.pi * c.g.G_rho * c.t.d_ln_rho))
    local_hamilton = float(np.max(
        np.abs((4 / 3) * c.g.Theta * c.t.d_Theta - 2 * c.t.d_sigma2 + c.t.d_R_u
               - 16 * np.pi * c.g.G_rho * c.t.d_ln_rho)
        / np.maximum(1, np.max(np.array(lh_terms), axis=0))))
    phi_center = float(bg.lapse.sol(np.array([0.0]))[0, 0])
    finite(cmc_equation, lapse_equation, boundary, lambda_boundary, quadrature,
           mass_identity, local_hamilton, hamilton, background_J)
    lambda_gate = 4 * num.bc_tol * (1 + abs(d_gamma_1))
    if (boundary > 4 * num.bc_tol or lambda_boundary > lambda_gate
            or max(cmc_equation, lapse_equation, quadrature, mass_identity,
                   local_hamilton, hamilton, background_J) > num.check_tol):
        raise LTBNumericalError(
            f"Unresolved sensitivity checks: cmc={cmc_equation:g}, lapse={lapse_equation:g}, "
            f"boundary={boundary:g}, lambda_boundary={lambda_boundary:g}, "
            f"quadrature={quadrature:g}, mass_identity={mass_identity:g}, "
            f"local_hamilton={local_hamilton:g}, hamilton={hamilton:g}, "
            f"background_J={background_J:g}")

    s_c, model = bg.s_c, bg.solution.model
    grid = bg.solution.r
    cg = section(grid)
    gS, gxi = dcmc.sol(grid)
    gN, _ = dlapse.sol(grid)
    g_dgamma = cg.xi * gxi / cg.gamma
    g_lambda = gN / cg.gamma - (cg.N / cg.gamma) * g_dgamma / cg.gamma
    d_ln_V, d_ln_M, dJ, d_rho_lam, dQ, dR = (float(x) for x in fine)
    residuals = KappaSensitivityResiduals(
        float(np.max(dcmc.rms_residuals)), float(np.max(dlapse.rms_residuals)),
        cmc_equation, lapse_equation, boundary, lambda_boundary, quadrature,
        mass_identity, local_hamilton, hamilton, background_J, phi_center,
        len(dcmc.x), len(dlapse.x))
    finite(gS, gxi, gN, g_dgamma, g_lambda)
    return KappaSensitivity(
        bg.solution, model.kappa_star == 0,
        dimensional(dK, s_c, -1), dimensional(dKs, s_c, -2),
        _readonly(dimensional(gS, s_c, 1)), _readonly(gxi), _readonly(g_dgamma),
        _readonly(gN), _readonly(g_lambda),
        d_ln_V, d_ln_M, d_ln_M - d_ln_V,
        dimensional(dJ, s_c, -1), dimensional(d_rho_lam, s_c, -2, model.G),
        dimensional(dQ, s_c, -2), dimensional(dR, s_c, -2),
        residuals,
    )


def _variations(c: _Section, dS: Array, dxi: Array) -> tuple[Array, ...]:
    """Total variations on the section: delta_gamma, delta_a, delta_A,
    delta_ln_rho and eta = delta_A/A + 2*delta_R/R (delta ln of 4*pi*A*R**2),
    each delta_geom + (d/ds)*delta_S; R = r*a, A_s = A*Hparallel,
    (ln rho)_s = -Theta."""
    g, t = c.g, c.t
    d_gamma = c.xi * dxi / c.gamma
    d_a = t.d_a + g.a_s * dS
    dA = t.d_A + g.A * t.Hl * dS
    d_ln_rho = t.d_ln_rho - g.Theta * dS
    eta = dA / g.A + 2 * d_a / g.a
    return d_gamma, d_a, dA, d_ln_rho, eta


def _mass_identity(c: _Section, dS: Array, dxi: Array) -> float:
    """Local delta_ln_rho + eta + r**2*chi/(2*(1+r**2*kappa)): ALGEBRAIC check.

    rho*A*R**2 = 3*m0*r**2/(4*pi*G*F) holds on every section (S10 (3)), so
    its total kappa_star variation is -delta_ln_F, independent of delta_S.
    """
    _, _, _, d_ln_rho, eta = _variations(c, dS, dxi)
    target = -c.t.d_ln_F
    total = d_ln_rho + eta - target
    scale = np.max(np.abs(np.array((d_ln_rho, eta, target))), axis=0)
    return float(np.max(np.abs(total) / np.maximum(1, scale)))
