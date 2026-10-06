"""Phase 1G-H: conditional global-mean linear variance (experimental runtime).

Independent checks of ``timescape_fsigma8.global_variance`` against routes
that do not reuse its formulas: direct mass/volume bookkeeping, finite
differences of the exact identities, an independent tracker implementation
of [GM] Eqs. (5.4)-(5.6) and text p. 25, the exact spherical (closed-FLRW)
wall solution, a real-space pair-density integral, Monte Carlo sampling and
the published 1G-D / 1G-F values.  Report: reports/phase1g_h_global_variance_closure.md.
"""

from __future__ import annotations

import dataclasses
import inspect
import math
import re
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import simpson
from scipy.optimize import brentq
from scipy.special import spherical_jn
from scipy.stats import multivariate_normal, norm

import timescape_fsigma8.global_variance as gv
import timescape_fsigma8.lagrangian_sigma as ls
from timescape_fsigma8 import scientific_status
from timescape_fsigma8.perturbations.initial_conditions import PLANCK_2018_QPLUS_RECIPE, qplus
from timescape_fsigma8.presets import PAPER_REFERENCE

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NA = ls.NOT_APPLICABLE
G = 1.0
Z_LS = 1090.0
OMEGA_M_LCDM = PLANCK_2018_QPLUS_RECIPE.omega_m * PLANCK_2018_QPLUS_RECIPE.h ** 2
MATCHING = gv.LastScatteringMatching(z_last_scattering=Z_LS, provenance="1G-D a_LS = 1/1091")
CHECKS = gv.TWO_PHASE_GROWTH_REFERENCE_CHECKS
# Test quadratures: the 1G-B reference grid and a seed grid reaching k = 1e4 Mpc^-1.
QUAD = ls.LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE
SEED_QUAD = ls.LagrangianSigmaQuadrature(
    k_min_per_Mpc=1e-6, k_max_per_Mpc=1e4, grid_points=12001, comparison_grid_points=6001,
    self_convergence_tolerance=1e-6, truncation_tolerance=1e-8)


def spectrum(A_s: float = 2.100e-9) -> ls.EarlySpectrumImport:
    return ls.EarlySpectrumImport(
        A_s=A_s, n_s=0.9649, k_pivot_per_Mpc=0.05, baryon_fraction=0.02237 / OMEGA_M_LCDM,
        T_cmb_K=2.7255, transfer_model=ls.EarlyTransferModel.EH98_ZERO_BARYON_OSCILLATION,
        provenance="Planck 2018 (test)", import_status=ls.EARLY_SPECTRUM_IMPORT_STATUS)


GM = ls.TimescapeTrackerInput.from_reference_preset(preset=PAPER_REFERENCE)
NW15 = ls.TimescapeTrackerInput(label="NW15_CMB_FIT", fv0=0.627, H0_dressed_km_s_Mpc=61.0,
                                source="Nazer & Wiltshire, arXiv:1410.3470 (test)")


def radius(kind: str, length: float = 8.0) -> ls.LagrangianRadiusSpec:
    C = ls.LagrangianRadiusConvention
    if kind == "a":
        return ls.LagrangianRadiusSpec(
            convention=C.EQUAL_LAGRANGIAN_MASS_TO_REFERENCE, length_h_inverse_Mpc=NA,
            reference_omega_m=OMEGA_M_LCDM,
            reference_radius_Mpc=length / PLANCK_2018_QPLUS_RECIPE.h, explicit_radius_Mpc=NA)
    if kind == "explicit":
        return ls.LagrangianRadiusSpec(convention=C.EXPLICIT_PHOTON_NORMALISED_RADIUS,
                                       length_h_inverse_Mpc=NA, reference_omega_m=NA,
                                       reference_radius_Mpc=NA, explicit_radius_Mpc=length)
    conv = {"b": C.DRESSED_WALL_COMOVING_LENGTH, "c": C.BARE_VOLUME_AVERAGE_PROPER_LENGTH}[kind]
    return ls.LagrangianRadiusSpec(convention=conv, length_h_inverse_Mpc=length,
                                   reference_omega_m=NA, reference_radius_Mpc=NA,
                                   explicit_radius_Mpc=NA)


def constant(p: float) -> gv.ConstantVoidShare:
    return gv.ConstantVoidShare(share=p, provenance="test", evidence_class="TEST_INPUT")


def run(bg_in, closure, rad, A_s: float = 2.100e-9) -> gv.ConditionalGlobalLinearSigma:
    return gv.conditional_global_linear_sigma(
        background=bg_in, matching=MATCHING, growth_checks=CHECKS, void_share_closure=closure,
        early_spectrum=spectrum(A_s), radius=rad, quadrature=QUAD,
        seed_quadrature=NA if isinstance(closure, gv.ConstantVoidShare) else SEED_QUAD,
        density_identity_tolerance=1e-13, G=G)


@pytest.fixture(scope="module")
def growth_gm() -> gv.TwoPhaseGlobalGrowth:
    return gv.two_phase_global_growth(background=GM, matching=MATCHING, checks=CHECKS, G=G)


def tracker_seed(bg_in, growth, present_radius_h_mpc: float, compression) -> gv.GaussianThresholdSeedVoidShare:
    h = bg_in.H0_dressed_km_s_Mpc / 100.0
    rs = gv.tracker_consistent_seed_radius(
        present_void_radius_volume_average_proper_Mpc=present_radius_h_mpc / h,
        f_v_seed=growth.f_v_ls, fv0=growth.fv0, gamma_w0=growth.gamma_w0)
    return gv.GaussianThresholdSeedVoidShare(seed_radius_Mpc=rs, seed_radius_provenance="test",
                                             compression=compression)


# ---------------------------------------------------------------- (H1)-(H5)
def test_empty_void_contrast_equals_direct_mass_volume_bookkeeping():
    """(H3) against M/V of explicit wall elements and void bubbles."""
    rng = np.random.default_rng(7)
    for _ in range(50):
        f_v = rng.uniform(0.05, 0.95)
        rho_w = rng.uniform(0.5, 3.0)                 # global wall density
        masses = rng.uniform(0.1, 1.0, size=20)       # wall elements of the region
        dens = rho_w * rng.uniform(0.6, 1.6, size=20)
        bubbles = rng.uniform(0.0, 2.0, size=7)       # void bubble volumes
        M, V_w, V_v = masses.sum(), (masses / dens).sum(), bubbles.sum()
        direct = (M / (V_w + V_v)) / ((1.0 - f_v) * rho_w) - 1.0
        V_w0 = M / rho_w
        V_v0 = V_w0 * f_v / (1.0 - f_v)
        value = gv.empty_void_region_contrast(void_volume_fraction=f_v,
                                              wall_density_contrast=V_w0 / V_w - 1.0,
                                              void_volume_contrast=V_v0 / V_v - 1.0)
        assert float(value) == pytest.approx(direct, rel=1e-12, abs=1e-14)


def test_finite_density_contrast_equals_bookkeeping_and_reduces_to_empty_voids():
    rng = np.random.default_rng(11)
    for _ in range(50):
        f_v, x = rng.uniform(0.05, 0.95), rng.uniform(0.0, 0.9)
        f_vl, rw, rv = rng.uniform(0.0, 1.0), rng.uniform(0.2, 2.0), rng.uniform(0.0, 3.0)
        rho_w = 1.7
        V = 3.3                                     # any region volume
        M = rho_w * rw * (1 - f_vl) * V + x * rho_w * rv * f_vl * V
        direct = (M / V) / (rho_w * ((1 - f_v) + f_v * x)) - 1.0
        value = gv.two_phase_region_contrast(
            void_volume_fraction=f_v, void_to_wall_density_ratio=x,
            region_void_volume_fraction=f_vl, region_wall_density_ratio=rw,
            region_void_density_ratio=rv)
        assert float(value) == pytest.approx(direct, rel=1e-12, abs=1e-14)
    # x = 0: (H2) in terms of the region's void fraction equals (H3).
    f_v, d_w, eps = 0.7, 0.13, -0.21
    f_wl_over = (1 - f_v) / (1 + d_w)
    f_vl = (f_v / (1 + eps)) / (f_wl_over + f_v / (1 + eps))
    via_h2 = gv.two_phase_region_contrast(
        void_volume_fraction=f_v, void_to_wall_density_ratio=0.0,
        region_void_volume_fraction=f_vl, region_wall_density_ratio=1 + d_w,
        region_void_density_ratio=1.0)
    via_h3 = gv.empty_void_region_contrast(void_volume_fraction=f_v, wall_density_contrast=d_w,
                                           void_volume_contrast=eps)
    assert float(via_h2) == pytest.approx(float(via_h3), rel=1e-13, abs=0.0)


def test_linear_coefficients_match_central_differences_of_the_exact_identity():
    f_v, x, h = 0.737, 0.2047, 1e-6
    c = gv.linear_two_phase_contrast_coefficients(void_volume_fraction=f_v,
                                                  void_to_wall_density_ratio=x)

    def exact(dw, dv, dfv):
        return float(gv.two_phase_region_contrast(
            void_volume_fraction=f_v, void_to_wall_density_ratio=x,
            region_void_volume_fraction=f_v + dfv, region_wall_density_ratio=1 + dw,
            region_void_density_ratio=1 + dv))

    assert (exact(h, 0, 0) - exact(-h, 0, 0)) / (2 * h) == pytest.approx(c["wall_density"], rel=1e-8, abs=0.0)
    assert (exact(0, h, 0) - exact(0, -h, 0)) / (2 * h) == pytest.approx(c["void_density"], rel=1e-8, abs=0.0)
    assert (exact(0, 0, h) - exact(0, 0, -h)) / (2 * h) == pytest.approx(
        c["void_volume_fraction"], rel=1e-8, abs=0.0)
    # Empty voids: delta_L = f_w delta_w + f_v epsilon (H4), by central differences of (H3).
    for f_v in (0.1, 0.5, 0.737):
        def e3(dw, eps):
            return float(gv.empty_void_region_contrast(void_volume_fraction=f_v,
                                                       wall_density_contrast=dw,
                                                       void_volume_contrast=eps))
        assert (e3(h, 0) - e3(-h, 0)) / (2 * h) == pytest.approx(1 - f_v, rel=1e-8, abs=0.0)
        assert (e3(0, h) - e3(0, -h)) / (2 * h) == pytest.approx(f_v, rel=1e-8, abs=0.0)


def test_strict_flat_wall_cap_is_the_supremum_over_void_volumes():
    for f_v in (1e-4, 0.3, 0.737):
        cap = gv.strict_flat_wall_contrast_cap(void_volume_fraction=f_v)
        eps = np.geomspace(1e-3, 1e12, 400)
        vals = np.asarray(gv.empty_void_region_contrast(
            void_volume_fraction=f_v, wall_density_contrast=np.zeros_like(eps),
            void_volume_contrast=eps))
        assert np.all(vals < cap)
        assert vals[-1] == pytest.approx(cap, rel=1e-9, abs=0.0)
        assert cap == pytest.approx(f_v / (1 - f_v), rel=1e-15, abs=0.0)


# --------------------------------------------------------------- (H6)-(H9)
def _independent_tracker(fv0: float):
    """[GM] (5.5)-(5.6), text p. 25, in dressed H0 = 1 units, coded here."""
    H_D0 = 2.0 * (2.0 + fv0) / (4.0 + fv0 + 4.0 * fv0 ** 2)
    t0 = (2.0 + fv0) / (3.0 * H_D0)
    tau = (2.0 + fv0) * (1.0 - fv0) / (3.0 * fv0 * H_D0)

    def f_v(t):
        return t / (t + tau)

    def a_D(t):
        return t * (fv0 / f_v(t)) ** (1.0 / 3.0)

    def z(t):
        gw, gw0 = 1.0 + f_v(t) / 2.0, 1.0 + fv0 / 2.0
        return gw * a_D(t0) / (gw0 * a_D(t)) - 1.0

    return t0, f_v, z


@pytest.mark.parametrize("bg_in", [GM, NW15], ids=["GM", "NW15"])
def test_growth_factors_against_an_independent_tracker(bg_in):
    growth = gv.two_phase_global_growth(background=bg_in, matching=MATCHING, checks=CHECKS, G=G)
    t0, f_v, z = _independent_tracker(bg_in.fv0)
    t_ls = brentq(lambda t: z(t) - Z_LS, 1e-12 * t0, t0, xtol=1e-18 * t0, rtol=1e-15)
    d_w = ((1 - f_v(t0)) / (1 - f_v(t_ls))) * (t0 / t_ls) ** (2.0 / 3.0) / (1.0 + Z_LS)
    d_v = (f_v(t0) / f_v(t_ls)) / (1.0 + Z_LS)
    assert growth.t_ls_over_t0 == pytest.approx(t_ls / t0, rel=1e-11, abs=0.0)
    assert growth.f_v_ls == pytest.approx(f_v(t_ls), rel=1e-11, abs=0.0)
    assert growth.wall_share_growth == pytest.approx(d_w, rel=1e-11, abs=0.0)
    assert growth.void_share_growth == pytest.approx(d_v, rel=1e-11, abs=0.0)
    assert dict(growth.diagnostics)["wall_share_ode_vs_closed_form_rel"] <= 1e-8


def test_small_void_fraction_limit_is_einstein_de_sitter():
    """D_W -> 1 - (5/6) f_v0 as f_v0 -> 0: the EdS photon-normalised growth."""
    for fv0 in (1e-3, 1e-4):
        bg_in = ls.TimescapeTrackerInput(label="small", fv0=fv0, H0_dressed_km_s_Mpc=70.0,
                                         source="limit test")
        growth = gv.two_phase_global_growth(background=bg_in, matching=MATCHING, checks=CHECKS, G=G)
        assert (growth.wall_share_growth - 1.0) / fv0 == pytest.approx(-5.0 / 6.0, abs=2.0 * fv0, rel=0.0)


def _theta_minus_sin(theta: float) -> float:
    """theta - sin(theta) without cancellation (Maclaurin series below 0.1)."""
    if theta >= 0.1:
        return theta - math.sin(theta)
    t2 = theta * theta
    return theta ** 3 / 6.0 * (1 - t2 / 20 * (1 - t2 / 42 * (1 - t2 / 72 * (1 - t2 / 110))))


def _one_minus_cos(theta: float) -> float:
    return 2.0 * math.sin(0.5 * theta) ** 2


def _closed_flrw_contrast(delta_lin_start: float, growth_factor: float) -> float:
    """Exact simultaneous-bang spherical (closed dust) contrast vs EdS in common time.

    1 + delta = 9 (theta - sin theta)^2 / [2 (1 - cos theta)^3], with
    t proportional to theta - sin theta and the linear growing mode
    delta_lin = (3/20) [6 (theta - sin theta)]^(2/3).
    """
    def lin(theta):
        return 0.15 * (6.0 * _theta_minus_sin(theta)) ** (2.0 / 3.0)

    th0 = brentq(lambda th: lin(th) / delta_lin_start - 1.0, 1e-9, 3.0, xtol=1e-18, rtol=1e-15)
    target = _theta_minus_sin(th0) * growth_factor ** 1.5      # t1/t0 = growth^(3/2)
    th1 = brentq(lambda th: _theta_minus_sin(th) / target - 1.0, 1e-9, 2 * math.pi - 1e-9,
                 xtol=1e-18, rtol=1e-15)
    return 4.5 * _theta_minus_sin(th1) ** 2 / _one_minus_cos(th1) ** 3 - 1.0


def test_linear_propagator_is_the_small_amplitude_limit_of_the_exact_region(growth_gm):
    """(H3) with the exact spherical wall solution and constant epsilon -> (H9)."""
    g = growth_gm
    t_ratio = 1.0 / g.t_ls_over_t0
    p = 0.11
    G_lin = (1 - p) * g.wall_share_growth + p * g.void_share_growth
    errors = []
    for amp in (1e-5, 1e-6, 1e-7):                 # delta_L at last scattering
        d_w_ls = (1 - p) * amp / (1 - g.f_v_ls)
        eps = p * amp / g.f_v_ls
        d_w_now = _closed_flrw_contrast(d_w_ls, t_ratio ** (2.0 / 3.0))
        exact = float(gv.empty_void_region_contrast(void_volume_fraction=g.fv0,
                                                    wall_density_contrast=d_w_now,
                                                    void_volume_contrast=eps))
        predicted = G_lin * (1.0 + Z_LS) * amp
        errors.append(abs(exact / predicted - 1.0))
    assert errors[-1] < 1e-4
    assert errors[0] / errors[1] == pytest.approx(10.0, rel=0.05, abs=0.0)     # O(amplitude)
    assert errors[1] / errors[2] == pytest.approx(10.0, rel=0.05, abs=0.0)


# --------------------------------------------------------------- (H10)-(H12)
def test_variance_equals_real_space_pair_density_integral():
    """(H10) in Fourier space equals int P_R(r) xi(r) dr (H11), computed here."""
    res = run(GM, constant(0.07), radius("explicit", 10.0))
    G_k = res.propagator_k0
    lnk = np.linspace(math.log(1e-5), math.log(60.0), 20001)
    k = np.exp(lnk)
    d2 = np.asarray(ls.matter_era_linear_amplitude(
        k_per_Mpc=k, early_spectrum=spectrum(), omega_m=res.density.omega_m_per_photon,
        growth_today_photon_normalised=G_k))
    R = 10.0
    r = np.linspace(0.0, 2 * R, 1201)[1:]
    xi = np.array([simpson(d2 * spherical_jn(0, k * ri), x=lnk) for ri in r])
    pair = (3 * r ** 2 / R ** 3) * (1 - 3 * r / (4 * R) + r ** 3 / (16 * R ** 3))
    assert simpson(pair, x=r) == pytest.approx(1.0, abs=1e-6, rel=0.0)
    sigma_real = math.sqrt(simpson(pair * xi, x=r))
    assert sigma_real == pytest.approx(res.linear_sigma, rel=2e-5, abs=0.0)


def test_unit_growth_sigma_matches_lagrangian_sigma_runtime():
    """G = 1 reproduces the validated 1G-B quadrature (same import, same window)."""
    res = run(GM, constant(0.0), radius("a"))
    ref = ls.conditional_lagrangian_linear_sigma(
        background=GM, growth_law=ls.GrowthLaw.WALL_REGIONAL_EDS_COMMON_TIME, closure=NA,
        growth_numerics=ls.WALL_REGIONAL_GROWTH_REFERENCE_CHECKS, early_spectrum=spectrum(),
        radius=radius("a"), quadrature=QUAD, density_identity_tolerance=1e-13, G=G)
    assert res.unit_growth_sigma == pytest.approx(ref.sigma_unit_growth, rel=1e-13, abs=0.0)
    assert res.radius.radius_Mpc == ref.radius.radius_Mpc


def test_gaussian_threshold_share_independent_evaluation(growth_gm):
    closure = tracker_seed(GM, growth_gm, 15.0, gv.SeedVolumeCompression.COMPRESSED_WITH_REGION)
    res = run(GM, closure, radius("c"))
    rs = closure.seed_radius_Mpc
    om = res.density.omega_m_per_photon

    # Independent quadrature: variable x = k R_s, uniform in ln x, own window code.
    lnx = np.linspace(math.log(1e-6 * rs), math.log(2e4 * rs), 400001)
    x = np.exp(lnx)
    amp = np.asarray(ls.matter_era_linear_amplitude(
        k_per_Mpc=x / rs, early_spectrum=spectrum(), omega_m=om,
        growth_today_photon_normalised=1.0))
    w = np.where(x > 1e-3, 3 * (np.sin(x) - x * np.cos(x)) / np.maximum(x, 1e-3) ** 3,
                 1 - x * x / 10)
    sigma_s = math.sqrt(simpson(amp * w * w, x=lnx)) / (1 + Z_LS)
    nu = norm.isf(growth_gm.f_v_ls)
    p0 = growth_gm.f_v_ls + norm.pdf(nu) / sigma_s
    assert res.void_share.sigma_seed == pytest.approx(sigma_s, rel=1e-6, abs=0.0)
    assert res.void_share.nu == pytest.approx(nu, rel=1e-12, abs=0.0)
    assert res.void_share.share_k0 == pytest.approx(p0, rel=1e-6, abs=0.0)
    # Scale dependence only through the seed window: p(k) -> p0 as k -> 0.
    pk = np.asarray(res.void_share.share(np.array([0.0, 1e-4, 1.0 / rs, 1e4 / rs])))
    assert pk[0] == pytest.approx(p0, rel=1e-6, abs=0.0)
    assert pk[1] == pytest.approx(p0, rel=1e-9, abs=0.0)
    # Far inside the seed scale only the compression term remains (|W(1e4)| < 4e-8).
    assert pk[3] == pytest.approx(growth_gm.f_v_ls, abs=1e-6 * p0, rel=0.0)


@pytest.mark.parametrize("bg_in,printed_A_v,printed_X", [(GM, 1169, 1.263), (NW15, 1185, 1.285)],
                         ids=["GM", "NW15"])
def test_reproduces_1g_d_owner_decision_void_response(bg_in, printed_A_v, printed_X):
    """1G-D owner decisions (GD-OD1/OD2/OD6/OD7): A_v and X_SU to their printed digits."""
    growth = gv.two_phase_global_growth(background=bg_in, matching=MATCHING, checks=CHECKS, G=G)
    closure = tracker_seed(bg_in, growth, 15.0, gv.SeedVolumeCompression.THRESHOLD_SHIFT_ONLY)
    res = run(bg_in, closure, radius("a"))
    g_lcdm = float(qplus(0.0, PLANCK_2018_QPLUS_RECIPE))
    assert abs(res.void_share.void_onset_response - printed_A_v) <= 0.5
    assert abs(res.propagator_k0 / g_lcdm - printed_X) <= 5e-4


def test_constant_share_variance_scales_with_A_s_and_pbs_void_term_does_not():
    rad = radius("c")
    base = run(GM, constant(0.08), rad)
    for factor in (0.5, 2.0):
        r = run(GM, constant(0.08), rad, A_s=2.100e-9 * factor)
        assert r.linear_sigma / base.linear_sigma == pytest.approx(math.sqrt(factor), rel=1e-10, abs=0.0)
    growth = gv.two_phase_global_growth(background=GM, matching=MATCHING, checks=CHECKS, G=G)
    clo = tracker_seed(GM, growth, 15.0, gv.SeedVolumeCompression.THRESHOLD_SHIFT_ONLY)
    b = run(GM, clo, rad)
    for factor in (0.5, 2.0):
        r = run(GM, clo, rad, A_s=2.100e-9 * factor)
        # p ~ 1/sigma_s ~ A_s^(-1/2): the void term is amplitude-independent (H16).
        assert r.void_share_rms / b.void_share_rms == pytest.approx(1.0, rel=1e-10, abs=0.0)
        assert r.wall_share_rms / b.wall_share_rms != pytest.approx(1.0, rel=1e-3, abs=0.0)


def test_terms_of_the_propagator_add_coherently_for_a_constant_share():
    res = run(NW15, constant(0.05), radius("c"))
    assert res.share_terms_coherence == pytest.approx(1.0, abs=1e-10, rel=0.0)
    assert res.linear_sigma == pytest.approx(res.wall_share_rms + res.void_share_rms, rel=1e-10, abs=0.0)
    zero = run(NW15, constant(0.0), radius("c"))
    assert zero.share_terms_coherence == NA and zero.void_share_rms == 0.0
    assert zero.linear_sigma == pytest.approx(zero.growth.wall_share_growth
                                              * zero.unit_growth_sigma, rel=1e-12, abs=0.0)


def test_admissible_interval_logic(growth_gm):
    target = run(GM, tracker_seed(GM, growth_gm, 15.0,
                                  gv.SeedVolumeCompression.COMPRESSED_WITH_REGION), radius("c"))
    premise = gv.HomogeneityPremise(radius=radius("c", 100.0), max_linear_rms=0.1,
                                    provenance="[W09] 10% at 100 h^-1 Mpc (test)")
    iv = gv.admissible_global_linear_interval(target=target, premise=premise)
    g = target.growth
    assert iv.lower == pytest.approx((g.wall_share_growth + (g.void_share_growth
                                      - g.wall_share_growth) * g.f_v_ls)
                                     * target.unit_growth_sigma, rel=1e-13, abs=0.0)
    assert iv.upper == pytest.approx(0.1 * target.unit_growth_sigma
                                     / iv.unit_growth_sigma_at_premise, rel=1e-13, abs=0.0)
    # The premise radius is checked directly with the closure's own propagator.
    assert (iv.target_premise_rms <= 0.1) == (target.linear_sigma <= iv.upper * (1 + 3e-3))
    tight = gv.HomogeneityPremise(radius=radius("c", 100.0), max_linear_rms=1e-4,
                                  provenance="incompatible (test)")
    bad = gv.admissible_global_linear_interval(target=target, premise=tight)
    assert not bad.premise_compatible and not bad.target_inside
    with pytest.raises(gv.GlobalVarianceContractError, match="convention"):
        gv.admissible_global_linear_interval(target=target, premise=gv.HomogeneityPremise(
            radius=radius("b", 100.0), max_linear_rms=0.1, provenance="mismatch"))


# ------------------------------------------------------------ (H17)-(H21)
def test_two_phase_variance_assembly_on_a_synthetic_field():
    """(H18) equals the sample variance of block-averaged contrasts (any cross terms)."""
    rng = np.random.default_rng(3)
    n_blocks, n_cells = 4000, 64
    g = rng.standard_normal((n_blocks, n_cells)) + 0.8 * rng.standard_normal((n_blocks, 1))
    chi_v = (g < 0.4).astype(float)
    chi_w = 1.0 - chi_v
    f_v = chi_v.mean()
    raw_w = 0.5 * g + rng.standard_normal(g.shape) * 0.3          # correlated with g
    raw_v = -0.2 * g + rng.standard_normal(g.shape) * 0.1
    d_w = raw_w - (chi_w * raw_w).sum() / chi_w.sum()               # conditional normalisation
    d_v = raw_v - (chi_v * raw_v).sum() / chi_v.sum()
    x = 0.2
    a_w = 1.0 / ((1 - f_v) + f_v * x)
    rho = a_w * chi_w * (1 + d_w) + x * a_w * chi_v * (1 + d_v)
    assert rho.mean() == pytest.approx(1.0, abs=1e-12, rel=0.0)              # mass normalisation
    delta_R = rho.mean(axis=1) - 1.0
    A = chi_w.mean(axis=1) - (1 - f_v)
    B = (chi_w * d_w).mean(axis=1)
    C = (chi_v * d_v).mean(axis=1)
    mom = gv.TwoPhaseSmoothedMoments(
        var_partition=float(np.mean(A * A)), wall_field=float(np.mean(B * B)),
        void_field=float(np.mean(C * C)), partition_wall=float(np.mean(A * B)),
        partition_void=float(np.mean(A * C)), wall_void=float(np.mean(B * C)),
        provenance="synthetic test")
    out = gv.two_phase_global_variance(void_volume_fraction=f_v, void_to_wall_density_ratio=x,
                                       moments=mom)
    assert out["variance"] == pytest.approx(float(np.mean(delta_R ** 2)), rel=1e-10, abs=0.0)
    assert abs(out["cross_terms"]) > 1e-3 * out["variance"]          # cross terms matter


def test_e3_special_case_is_the_1g_e_mass_conserving_formula():
    for f_v, x in ((0.737, 0.0), (0.627, 0.0), (0.737, 0.1), (0.5, 0.3)):
        f_w = 1 - f_v
        sp, si = 0.33, 0.93                          # 1G-E normalisation: Var(A)/f_w^2, Var(B)/f_w^2
        mom = gv.TwoPhaseSmoothedMoments(var_partition=(sp * f_w) ** 2,
                                         wall_field=(si * f_w) ** 2, void_field=0.0,
                                         partition_wall=0.0, partition_void=0.0, wall_void=0.0,
                                         provenance="E3")
        out = gv.two_phase_global_variance(void_volume_fraction=f_v,
                                           void_to_wall_density_ratio=x, moments=mom)
        delta_v = x / (f_w + f_v * x) - 1.0          # void contrast vs the global mean
        e_formula = delta_v ** 2 * sp ** 2 + (f_w - f_v * delta_v) ** 2 * si ** 2
        assert out["variance"] == pytest.approx(e_formula, rel=1e-13, abs=0.0)
        assert out["void_contrast_global"] == pytest.approx(delta_v, rel=1e-13, abs=0.0)
        assert f_w * out["wall_weight"] + f_v * out["void_weight"] == pytest.approx(1.0, rel=1e-14, abs=0.0)


def test_two_phase_variance_refuses_unrealisable_moments():
    with pytest.raises(gv.GlobalVarianceContractError, match="positive semidefinite"):
        gv.two_phase_global_variance(void_volume_fraction=0.7, void_to_wall_density_ratio=0.0,
                                     moments=gv.TwoPhaseSmoothedMoments(
                                         var_partition=0.01, wall_field=0.01, void_field=0.0,
                                         partition_wall=0.05, partition_void=0.0, wall_void=0.0,
                                         provenance="violates Cauchy-Schwarz"))
    with pytest.raises(gv.GlobalVarianceContractError, match="f_v f_w"):
        gv.two_phase_global_variance(void_volume_fraction=0.7, void_to_wall_density_ratio=0.0,
                                     moments=gv.TwoPhaseSmoothedMoments(
                                         var_partition=0.3, wall_field=0.0, void_field=0.0,
                                         partition_wall=0.0, partition_void=0.0, wall_void=0.0,
                                         provenance="indicator variance too large"))


def test_cauchy_schwarz_interval_contains_every_joint_law():
    rng = np.random.default_rng(5)
    a, b = 0.33, 0.93
    iv = gv.cauchy_schwarz_total_rms_interval(partition_rms=a, field_rms=b)
    for rho in (-1.0, -0.5, 0.0, 0.5, 1.0):
        u = rng.standard_normal(200000)
        v = rho * u + math.sqrt(max(0.0, 1 - rho * rho)) * rng.standard_normal(200000)
        total = math.sqrt(np.mean((a * u + b * v) ** 2))
        assert iv["lower"] - 0.01 <= total <= iv["upper"] + 0.01
    assert iv["independent"] == pytest.approx(math.hypot(a, b), rel=1e-12, abs=0.0)


def test_orthant_moments_against_bivariate_cdf_and_monte_carlo():
    rng = np.random.default_rng(9)
    for rho, c in ((0.0, 0.634), (0.6, -0.5), (0.95, 0.634), (-0.4, 1.2)):
        mom = gv.bivariate_normal_orthant_moments(correlation=rho, threshold=c, nodes=400)
        exact = multivariate_normal(mean=[0, 0], cov=[[1, rho], [rho, 1]]).cdf([-c, -c])
        assert mom["P11"] == pytest.approx(exact, abs=1e-9, rel=0.0)
        z = rng.multivariate_normal([0, 0], [[1, rho], [rho, 1]], size=2_000_000)
        ind = (z[:, 0] > c) & (z[:, 1] > c)
        for key, sample in (("E_g1", ind * z[:, 0]), ("E_g2", ind * z[:, 1]),
                            ("E_g1g1", ind * z[:, 0] ** 2), ("E_g1g2", ind * z[:, 0] * z[:, 1])):
            err = 5.0 * sample.std() / math.sqrt(sample.size)
            assert abs(mom[key] - sample.mean()) <= err, key


def test_gaussian_threshold_pair_covariance_formulas_by_monte_carlo():
    """Law II of [1G-H] Sec. 6.3: K_ww and K_chi_w against direct 4-variate sampling."""
    rng = np.random.default_rng(13)
    f_v = 0.737
    f_w = 1 - f_v
    c = norm.ppf(f_v)
    rho, g0, gr, x0, xr = 0.8, 0.9, 0.7, 1.3, 0.9
    cov = np.array([[1, rho, g0, gr], [rho, 1, gr, g0], [g0, gr, x0, xr], [gr, g0, xr, x0]])
    z = rng.multivariate_normal(np.zeros(4), cov, size=3_000_000)
    mu = g0 * norm.pdf(c) / f_w
    i1, i2 = z[:, 0] > c, z[:, 1] > c
    kww_mc = i1 * i2 * (z[:, 2] - mu) * (z[:, 3] - mu)
    kxw_mc = (i1 - f_w) * i2 * (z[:, 3] - mu)
    mom = gv.bivariate_normal_orthant_moments(correlation=rho, threshold=c, nodes=300)
    B = np.array([[g0, gr], [gr, g0]]) @ np.linalg.inv(np.array([[1, rho], [rho, 1]]))
    mg = np.array([[mom["E_g1g1"], mom["E_g1g2"]], [mom["E_g1g2"], mom["E_g1g1"]]])
    m1 = np.array([mom["E_g1"], mom["E_g2"]])
    cee = xr - float((B @ np.array([[g0, gr], [gr, g0]]).T)[0, 1])
    kww = float((B @ mg @ B.T)[0, 1]) + mom["P11"] * cee - mu * float(np.sum(B @ m1)) \
        + mu * mu * mom["P11"]
    kxw = float((B @ m1)[1]) - mu * mom["P11"]
    assert abs(kww - kww_mc.mean()) <= 5 * kww_mc.std() / math.sqrt(kww_mc.size)
    assert abs(kxw - kxw_mc.mean()) <= 5 * kxw_mc.std() / math.sqrt(kxw_mc.size)
    # Conditional normalisation: E[chi_w (w - mu)] = 0 although E[w] = 0 already.
    cond = i1 * (z[:, 2] - mu)
    assert abs(cond.mean()) <= 5 * cond.std() / math.sqrt(cond.size)


# ------------------------------------------------------------------- (H22)
def test_two_barrier_mass_fraction_and_global_bias():
    d_c = 3 * (12 * math.pi) ** (2 / 3) / 20
    d_v, x = -2.7171803438378705, 0.20472233400490963
    m = gv.two_barrier_void_mass_fraction(collapse_threshold=d_c, void_threshold=d_v,
                                          long_mode_contrast=0.0)
    assert m == pytest.approx(0.3829709426561785, rel=1e-12, abs=0.0)          # 1G-F successor Sec. 2
    out = gv.two_barrier_global_linear_bias(collapse_threshold=d_c, void_threshold=d_v,
                                            void_to_wall_density_ratio=x,
                                            wall_response=gv.WallLongModeResponse.COMPRESSED_WITH_LONG_MODE)
    assert out["void_volume_fraction"] == pytest.approx(0.7519694338440862, rel=1e-12, abs=0.0)
    # Gambler's ruin by a discrete symmetric walk started at delta_l (independent).
    h = 0.05
    for dl in (-0.5, 0.0, 0.7):
        n_up, n_down = round((d_c - dl) / h), round((dl - d_v) / h)
        assert n_up / (n_up + n_down) == pytest.approx(
            gv.two_barrier_void_mass_fraction(collapse_threshold=d_c, void_threshold=d_v,
                                              long_mode_contrast=dl), abs=h / (d_c - d_v), rel=0.0)
    universal = gv.two_barrier_global_linear_bias(
        collapse_threshold=d_c, void_threshold=d_v, void_to_wall_density_ratio=x,
        wall_response=gv.WallLongModeResponse.UNIVERSAL_WALL_DENSITY)
    assert out["bias"] - universal["bias"] == pytest.approx(1.0, rel=1e-15, abs=0.0)
    assert out["mass_fraction_response"] == pytest.approx(-1 / (d_c - d_v), rel=1e-15, abs=0.0)


# ------------------------------------------------------- contracts, naming
def test_every_scientific_argument_is_mandatory_and_keyword_only():
    for fn in (gv.conditional_global_linear_sigma, gv.two_phase_global_growth,
               gv.evaluate_void_share, gv.admissible_global_linear_interval,
               gv.two_phase_global_variance, gv.global_linear_propagator,
               gv.two_barrier_global_linear_bias):
        for param in inspect.signature(fn).parameters.values():
            assert param.kind is inspect.Parameter.KEYWORD_ONLY
            assert param.default is inspect.Parameter.empty, (fn.__name__, param.name)
    for cls in (gv.LastScatteringMatching, gv.TwoPhaseGrowthChecks, gv.ConstantVoidShare,
                gv.GaussianThresholdSeedVoidShare, gv.HomogeneityPremise,
                gv.TwoPhaseSmoothedMoments):
        for f in dataclasses.fields(cls):
            assert f.default is dataclasses.MISSING and f.default_factory is dataclasses.MISSING


def test_closures_and_inputs_fail_closed(growth_gm):
    with pytest.raises(gv.GlobalVarianceContractError):
        constant(1.2)
    with pytest.raises(gv.GlobalVarianceContractError):
        constant(-0.1)
    with pytest.raises(gv.GlobalVarianceContractError, match="exceed 1"):
        gv.LastScatteringMatching(z_last_scattering=0.5, provenance="x")
    with pytest.raises(gv.GlobalVarianceContractError):
        gv.GaussianThresholdSeedVoidShare(seed_radius_Mpc=1.0, seed_radius_provenance="x",
                                          compression="compressed_with_region")
    twin = ls.TimescapeTrackerInput(label=GM.label, fv0=GM.fv0,
                                    H0_dressed_km_s_Mpc=GM.H0_dressed_km_s_Mpc, source=GM.source)
    density = ls.early_matter_density_per_photon(background=twin, identity_tolerance=1e-13, G=G)
    with pytest.raises(gv.GlobalVarianceContractError, match="background object"):
        gv.evaluate_void_share(closure=constant(0.1), growth=growth_gm, density=density,
                               early_spectrum=spectrum(), seed_quadrature=NA)
    own_density = ls.early_matter_density_per_photon(background=growth_gm.background,
                                                     identity_tolerance=1e-13, G=G)
    with pytest.raises(gv.GlobalVarianceContractError, match="NOT_APPLICABLE"):
        gv.evaluate_void_share(closure=constant(0.1), growth=growth_gm, density=own_density,
                               early_spectrum=spectrum(), seed_quadrature=SEED_QUAD)
    with pytest.raises(gv.GlobalVarianceContractError, match="seed_quadrature"):
        gv.evaluate_void_share(
            closure=gv.GaussianThresholdSeedVoidShare(
                seed_radius_Mpc=0.7, seed_radius_provenance="x",
                compression=gv.SeedVolumeCompression.COMPRESSED_WITH_REGION),
            growth=growth_gm, density=own_density, early_spectrum=spectrum(),
            seed_quadrature=NA)
    # A seed so large that p0 > 1 leaves the monotone class: refused.
    with pytest.raises(gv.GlobalVarianceContractError, match="monotone"):
        gv.evaluate_void_share(
            closure=gv.GaussianThresholdSeedVoidShare(
                seed_radius_Mpc=400.0, seed_radius_provenance="x",
                compression=gv.SeedVolumeCompression.COMPRESSED_WITH_REGION),
            growth=growth_gm, density=own_density, early_spectrum=spectrum(),
            seed_quadrature=SEED_QUAD)
    with pytest.raises(gv.GlobalVarianceContractError):
        gv.two_barrier_void_mass_fraction(collapse_threshold=1.686, void_threshold=-2.7,
                                          long_mode_contrast=2.0)
    with pytest.raises(gv.GlobalVarianceContractError):
        gv.bivariate_normal_orthant_moments(correlation=1.0, threshold=0.0, nodes=64)


def test_records_reject_tampering():
    res = run(GM, constant(0.05), radius("c"))
    with pytest.raises(gv.GlobalVarianceContractError):
        dataclasses.replace(res, effective_propagator=res.effective_propagator * 1.01)
    with pytest.raises(gv.GlobalVarianceContractError):
        dataclasses.replace(res, amplitude_status="OBSERVATIONAL")
    with pytest.raises(gv.GlobalVarianceContractError):
        dataclasses.replace(res, void_response_regime=gv.VOID_RESPONSE_NONPERTURBATIVE)
    with pytest.raises(gv.GlobalVarianceContractError):
        dataclasses.replace(res.growth, void_share_growth=res.growth.void_share_growth * 1.001)


FORBIDDEN = ("sigma8", "sigma_8", "8hmpc")


def _keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _keys(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _keys(v)


def test_naming_rule_statuses_and_isolation():
    assert not [n for n in gv.__all__ if any(t in n.lower() for t in FORBIDDEN)]
    public = [n for n in dir(gv) if not n.startswith("_")]
    assert not [n for n in public if any(t in n.lower() for t in FORBIDDEN)]
    res = run(GM, constant(0.05), radius("c"))
    payload = res.to_json_dict()
    assert not [k for k in _keys(payload) if any(t in k.lower() for t in FORBIDDEN)]
    assert payload["status"]["observational"] == "NON_OBSERVATIONAL"
    assert payload["status"]["amplitude_identity"] == "NOT_OBSERVATIONAL_SIGMA_8"
    assert payload["status"]["module"] == "EXPERIMENTAL_CONDITIONAL_RESEARCH_RUNTIME"
    # The experimental module is imported by no other package module.
    src = PROJECT_ROOT / "src" / "timescape_fsigma8"
    importers = [p for p in src.rglob("*.py") if p.name != "global_variance.py"
                 and re.search(r"global_variance", p.read_text(encoding="utf-8"))]
    assert importers == []
    # No status token or authorisation is changed by this phase.
    status = scientific_status.CURRENT_SCIENTIFIC_STATUS
    assert status["LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC"] == "NOT_DERIVED"
    assert status["VOID_ONSET_RESPONSE"] == "EXTERNAL_CLOSURE_INPUT"
    for token in ("SIGMA8_AUTHORIZATION", "FSIGMA8_AUTHORIZATION", "RSD_AUTHORIZATION",
                  "OBSERVATIONAL_AUTHORIZATION", "UNIQUE_TIMESCAPE_PREDICTION"):
        assert status[token] == "NOT_GRANTED"


def test_example_configurations_run_and_require_every_choice(tmp_path):
    import importlib.util
    import json

    path = PROJECT_ROOT / "scripts" / "phase1g_h_global_variance_case.py"
    spec_ = importlib.util.spec_from_file_location("_phase1g_h_case", path)
    module = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(module)
    config = json.loads((PROJECT_ROOT / "scripts" / "phase1g_h_configs"
                         / "nw15_equal_mass_constant_share.json").read_text(encoding="utf-8"))
    out = module.run(config)
    direct = run(NW15, constant(0.05), radius("a"))
    assert out["record"]["linear_sigma"] == pytest.approx(direct.linear_sigma, rel=1e-14, abs=0.0)
    for key in ("void_share", "radius", "homogeneity_premise"):
        broken = {k: v for k, v in config.items() if k != key}
        with pytest.raises(SystemExit, match="mandatory"):
            module.run(broken)
