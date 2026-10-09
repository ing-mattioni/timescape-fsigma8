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
import functools
import inspect
import json
import math
import re
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import quad, simpson
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
        mom = gv.bivariate_normal_orthant_moments(correlation=rho, threshold=c, nodes=32,
                                                  tolerance=1e-12)
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
    mom = gv.bivariate_normal_orthant_moments(correlation=rho, threshold=c, nodes=32,
                                              tolerance=1e-12)
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
               gv.two_barrier_global_linear_bias, gv.bivariate_normal_orthant_moments,
               gv.bivariate_normal_orthant_probability):
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
        gv.bivariate_normal_orthant_moments(correlation=1.0, threshold=0.0, nodes=64,
                                            tolerance=1e-12)


def test_records_reject_tampering():
    res = run(GM, constant(0.05), radius("c"))
    # Each targeted invariant fires before the recomputation binding (GH-DF2),
    # so its own message is required (delta audit mutants N3 and siblings).
    with pytest.raises(gv.GlobalVarianceContractError, match="effective_propagator must be"):
        dataclasses.replace(res, effective_propagator=res.effective_propagator * 1.01)
    with pytest.raises(gv.GlobalVarianceContractError, match="amplitude_status must be"):
        dataclasses.replace(res, amplitude_status="OBSERVATIONAL")
    with pytest.raises(gv.GlobalVarianceContractError, match="void_response_regime"):
        dataclasses.replace(res, void_response_regime=gv.VOID_RESPONSE_NONPERTURBATIVE)
    with pytest.raises(gv.GlobalVarianceContractError, match=r"violate \(H8\)"):
        dataclasses.replace(res.growth, void_share_growth=res.growth.void_share_growth * 1.001)
    # The concrete probes of the independent audit (GH-F9) and their siblings.
    with pytest.raises(gv.GlobalVarianceContractError, match="closure's share"):
        dataclasses.replace(res.void_share, share_k0=0.95)
    pbs = run(GM, tracker_seed(GM, res.growth, 15.0, gv.SeedVolumeCompression.COMPRESSED_WITH_REGION),
              radius("c"))
    inconsistent = "inconsistent with \\(H12\\)"
    for field, value, message in (("threshold_share_k0", float("nan"), "must be finite"),
                                  ("threshold_share_k0", pbs.void_share.threshold_share_k0 * 1.01,
                                   inconsistent),
                                  ("compression_share", 0.0, inconsistent),
                                  ("nu", pbs.void_share.nu + 1e-6, inconsistent),
                                  ("kind", "constant", "kind must be")):
        with pytest.raises(gv.GlobalVarianceContractError, match=message):
            dataclasses.replace(pbs.void_share, **{field: value})
    for field, value, message in (
            ("t_ls_over_t0", 2.0, "tracker ordering"),
            ("t_ls_over_t0", res.growth.t_ls_over_t0 * 1.001, "tracker identities"),
            ("diagnostics", tuple((k, float("nan")) for k, _ in res.growth.diagnostics),
             "must be finite"),
            ("diagnostics", res.growth.diagnostics[1:], "missing or failed")):
        with pytest.raises(gv.GlobalVarianceContractError, match=message):
            dataclasses.replace(res.growth, **{field: value})
    for field, value, message in (
            ("propagator_k0", res.propagator_k0 * 1.01, "propagator_k0 violates"),
            ("flat_wall_capacity_ratio", res.flat_wall_capacity_ratio * 1.01,
             "flat_wall_capacity_ratio violates"),
            ("quadrature_relative_change", 2.0 * res.quadrature_relative_change + 1e-12,
             "quadrature diagnostics")):
        with pytest.raises(gv.GlobalVarianceContractError, match=message):
            dataclasses.replace(res, **{field: value})
    premise = gv.HomogeneityPremise(radius=radius("c", 100.0), max_linear_rms=0.1, provenance="test")
    iv = gv.admissible_global_linear_interval(target=res, premise=premise)
    for field, value, message in (("upper", float("inf"), "must be finite"),
                                  ("share_upper", float("nan"), "must be finite"),
                                  ("share_lower", -0.1, r"violate \(H15\)"),
                                  ("upper", iv.upper * 1.01, r"violate \(H15\)"),
                                  ("lower", iv.lower * 0.99, r"violate \(H15\)"),
                                  ("premise_compatible", not iv.premise_compatible,
                                   r"violate \(H15\)")):
        with pytest.raises(gv.GlobalVarianceContractError, match=message):
            dataclasses.replace(iv, **{field: value})
    # Strict JSON: the records serialise without non-finite numbers.
    for record in (res, pbs, iv):
        json.dumps(record.to_json_dict(), allow_nan=False)


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


# ------------------------------------------- audit remediation (2026-10-07)
@functools.lru_cache(maxsize=1)
def _evidence():
    """The evidence script as a module (its functions are tested directly)."""
    import importlib.util

    path = PROJECT_ROOT / "scripts" / "phase1g_h_global_variance_closure_numerics.py"
    spec_ = importlib.util.spec_from_file_location("_phase1g_h_numerics", path)
    module = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(module)
    return module


def test_gh_f1_mean_derivative_of_the_exact_identity_is_not_the_tangent():
    """The audit's two-state example: why D1 defines the formal tangent statistic."""
    f_v, h = 0.737, 1e-6

    def contrast(s_):
        return float(gv.empty_void_region_contrast(void_volume_fraction=f_v,
                                                   wall_density_contrast=s_,
                                                   void_volume_contrast=0.0))

    states = (-1.0 / 3.0, 1.0)
    assert np.mean([1.0 / (1.0 + contrast(s_)) for s_ in states]) == pytest.approx(
        1.0, rel=1e-14, abs=0.0)                                  # equal-mass ensemble
    mean_derivative = float(np.mean([(contrast(s_ + h) - contrast(s_ - h)) / (2 * h)
                                     for s_ in states]))
    tangent = (contrast(h) - contrast(-h)) / (2 * h)
    assert mean_derivative == pytest.approx(0.274683481680, rel=1e-8, abs=0.0)
    assert tangent == pytest.approx(1.0 - f_v, rel=1e-8, abs=0.0)
    assert mean_derivative / tangent - 1.0 > 0.04


def test_gh_f3_void_share_is_f_v_minus_the_regional_fraction_derivative(growth_gm):
    """p delta = f_v epsilon equals p = f_v - d f_v,L/d delta_L (explicit volumes)."""
    f_v, h = 0.2, 1e-7
    f_w = 1.0 - f_v
    for p in (0.0, 0.05, 0.3, 1.0):
        def state(delta):
            eps, d_w = p * delta / f_v, (1.0 - p) * delta / f_w
            v_w0 = 1.0                                     # region's reference wall volume
            v_w, v_v = v_w0 / (1.0 + d_w), v_w0 * (f_v / f_w) / (1.0 + eps)
            v_l = v_w + v_v
            return v_v / v_l, v_w0 / (f_w * v_l) - 1.0     # f_v,L and delta_L (M_L = rho_w v_w0)
        (fp, dp), (fm, dm) = state(h), state(-h)
        assert f_v - (fp - fm) / (dp - dm) == pytest.approx(p, rel=1e-6, abs=1e-9)
    density = ls.early_matter_density_per_photon(background=growth_gm.background,
                                                 identity_tolerance=1e-13, G=G)
    for compression in gv.SeedVolumeCompression:
        share = gv.evaluate_void_share(closure=tracker_seed(GM, growth_gm, 15.0, compression),
                                       growth=growth_gm, density=density,
                                       early_spectrum=spectrum(), seed_quadrature=SEED_QUAD)
        offset = 1.0 if compression is gv.SeedVolumeCompression.COMPRESSED_WITH_REGION else 0.0
        assert share.share_k0 == pytest.approx(
            growth_gm.f_v_ls * (offset + share.void_onset_response), rel=1e-12, abs=0.0)


def test_gh_f4_scale_dependent_share_escapes_the_constant_share_interval(growth_gm):
    density = ls.early_matter_density_per_photon(background=growth_gm.background,
                                                 identity_tolerance=1e-13, G=G)
    r8 = ls.resolve_lagrangian_radius(spec=radius("c"), density=density).radius_Mpc
    r_hom = ls.resolve_lagrangian_radius(spec=radius("c", 100.0), density=density).radius_Mpc
    s8, s_hom = (gv.unit_growth_lagrangian_sigma(radius_Mpc=r, omega_m=density.omega_m_per_photon,
                                                 early_spectrum=spectrum(), quadrature=QUAD)
                 for r in (r8, r_hom))
    upper = min(0.1 / s_hom, growth_gm.void_share_growth) * s8          # (H15), constant share
    out = _evidence().step_share_counterexample(growth_gm, density, spectrum(), target_R=r8,
                                                premise_R=r_hom, eta=0.1,
                                                constant_share_upper=upper)
    assert out["share_low_k"] == growth_gm.f_v_ls and out["share_high_k"] == 1.0  # inside H-A7
    assert out["premise_rms"] <= 0.1
    assert out["target_rms"] > 5.0 * upper


def test_gh_f5_lognormal_mask_kernels_by_monte_carlo():
    """Closed forms of the nonnegative lognormal laws against 4-variate sampling."""
    ev = _evidence()
    rng = np.random.default_rng(23)
    f_v = 0.737
    f_w, c = 1.0 - f_v, norm.ppf(f_v)
    rho, lam, xs0, xsr, g0, gr = 0.6, 0.8, 1.0, 0.45, 0.5, 0.3
    for correlated in (False, True):
        k0, kr = (g0, gr) if correlated else (0.0, 0.0)
        cov = np.array([[1, rho, k0, kr], [rho, 1, kr, k0], [k0, kr, xs0, xsr], [kr, k0, xsr, xs0]])
        z = rng.multivariate_normal(np.zeros(4), cov, size=2_000_000)
        chi1, chi2 = z[:, 0] > c, z[:, 1] > c
        n_w = math.exp(0.5 * lam * lam * xs0) * norm.sf(c - lam * k0) / f_w   # E[e^a | wall]
        psi1, psi2 = np.exp(lam * z[:, 2]) / n_w, np.exp(lam * z[:, 3]) / n_w
        assert psi1.min() >= 0.0
        norm_mc = chi1 * (psi1 - 1.0)                                         # E[chi (psi-1)] = 0
        assert abs(norm_mc.mean()) <= 5 * norm_mc.std() / math.sqrt(norm_mc.size)
        p11, kww, kpw = ev.lognormal_mask_kernels(rho=rho, c=c, f_w=f_w, lam=lam, xi_lat_r=xsr,
                                                  kappa0=lam * k0, kappa_r=lam * kr)
        kww_mc = chi1 * chi2 * (psi1 - 1.0) * (psi2 - 1.0)
        kpw_mc = (chi1 - f_w) * chi2 * (psi2 - 1.0)
        assert abs(kww - kww_mc.mean()) <= 5 * kww_mc.std() / math.sqrt(kww_mc.size)
        assert abs(kpw - kpw_mc.mean()) <= 5 * kpw_mc.std() / math.sqrt(kpw_mc.size)
        assert p11 == pytest.approx(float(np.mean(chi1 & chi2)), abs=2e-3, rel=0.0)


def test_gh_f6_post_hoc_anchoring_differs_from_pbs_reclosure(growth_gm):
    factor = 0.97
    const, const_re = (run(GM, constant(0.05), radius("c"), A_s=a) for a in (2.1e-9, 2.1e-9 * factor ** 2))
    assert const_re.linear_sigma == pytest.approx(const.linear_sigma * factor, rel=1e-10, abs=0.0)
    seed = tracker_seed(GM, growth_gm, 15.0, gv.SeedVolumeCompression.COMPRESSED_WITH_REGION)
    pbs, pbs_re = (run(GM, seed, radius("c"), A_s=a) for a in (2.1e-9, 2.1e-9 * factor ** 2))
    assert pbs_re.void_share.share_k0 > pbs.void_share.share_k0      # threshold term ~ 1/sigma_s
    assert pbs_re.linear_sigma / (pbs.linear_sigma * factor) - 1.0 > 0.01


def test_gh_f10_orthant_quadrature_meets_its_accuracy_contract():
    tol = 1e-12

    def prob(rho, c1, c2):
        return gv.bivariate_normal_orthant_probability(correlation=rho, threshold_1=c1,
                                                       threshold_2=c2, nodes=16, tolerance=tol)

    assert prob(0.0, -100.0, -100.0) == pytest.approx(1.0, abs=1e-12, rel=0.0)
    for rho in (0.999999, -0.999999, 0.3, -0.7):
        assert prob(rho, 0.0, 0.0) == pytest.approx(0.25 + math.asin(rho) / (2 * math.pi),
                                                    abs=1e-12, rel=0.0)
    for c1, c2 in ((0.634, -1.2), (2.0, 0.5), (-3.0, 4.0)):
        assert prob(0.0, c1, c2) == pytest.approx(norm.sf(c1) * norm.sf(c2), abs=1e-12, rel=0.0)
        for rho in (-0.5, 0.4, 0.95):
            exact = multivariate_normal(mean=[0, 0], cov=[[1, rho], [rho, 1]]).cdf([-c1, -c2])
            assert prob(rho, c1, c2) == pytest.approx(exact, abs=1e-8, rel=0.0)
    c = 0.634
    q, phi = norm.sf(c), norm.pdf(c)
    mom = gv.bivariate_normal_orthant_moments(correlation=0.0, threshold=c, nodes=16, tolerance=tol)
    for key, value in (("P11", q * q), ("E_g1", phi * q), ("E_g2", phi * q),
                       ("E_g1g1", (c * phi + q) * q), ("E_g1g2", phi * phi)):
        assert mom[key] == pytest.approx(value, abs=1e-12, rel=0.0), key
    with pytest.raises(gv.GlobalVarianceNumericalError, match="not converged"):
        gv.bivariate_normal_orthant_moments(correlation=0.5, threshold=0.0,
                                            nodes=gv.ORTHANT_MAX_NODES, tolerance=tol)
    with pytest.raises(gv.GlobalVarianceContractError, match="double precision"):
        gv.bivariate_normal_orthant_probability(correlation=0.5, threshold_1=0.0, threshold_2=0.0,
                                                nodes=16, tolerance=1e-16)


def test_gh_f11_1g_e_reference_reproduces_within_its_rounding_budget():
    quoted = json.loads((PROJECT_ROOT / "reports" / "phase1g_e_owner_decisions_successor_inventory.json")
                        .read_text(encoding="utf-8"))["numbers_from_artifact"]
    for label, fv0 in (("PAPER_REFERENCE", 0.737), ("NW15_CMB_FIT", 0.627)):
        key = f"GE_reference_population_1G_F|{label}|b_dressed_8_over_h|"
        sp, si, total = (float(quoted[key + k]) for k in (
            "sigma_part", "sigma_int_photon_frame_D_wall", "sigma_photon_frame_D_wall_empty_voids"))
        f_w = 1.0 - fv0
        var = gv.two_phase_global_variance(
            void_volume_fraction=fv0, void_to_wall_density_ratio=0.0,
            moments=gv.TwoPhaseSmoothedMoments(var_partition=(sp * f_w) ** 2,
                                               wall_field=(si * f_w) ** 2, void_field=0.0,
                                               partition_wall=0.0, partition_void=0.0,
                                               wall_void=0.0, provenance="1G-E/F reference, E3"))
        budget = _evidence().e_reference_rounding_budget(
            sigma_partition=sp, sigma_internal=si, sigma_total=var["rms"], half_unit=5e-5)
        assert budget == pytest.approx(5e-5 * (sp / var["rms"] + si / var["rms"] + 1.0),
                                       rel=1e-15, abs=0.0)            # half a unit, propagated
        assert abs(var["rms"] - total) <= budget < 1.2e-4


# --------------------------------------- delta-audit remediation (2026-10-08)
def test_gh_df2_records_bind_results_to_their_inputs():
    """The delta audit's five accepted replacements are refused (GH-DF2)."""
    res = run(GM, constant(0.05), radius("c"))
    pbs = run(GM, tracker_seed(GM, res.growth, 15.0, gv.SeedVolumeCompression.COMPRESSED_WITH_REGION),
              radius("c"))
    premise = gv.HomogeneityPremise(radius=radius("c", 100.0), max_linear_rms=0.1, provenance="test")
    iv = gv.admissible_global_linear_interval(target=res, premise=premise)
    # Unchanged copies of genuine records are accepted.
    for record in (res, pbs, pbs.void_share, res.growth, iv):
        assert dataclasses.replace(record) == record
    with pytest.raises(gv.GlobalVarianceContractError, match="early spectrum"):
        dataclasses.replace(res, early_spectrum=spectrum(4.0 * 2.1e-9))
    with pytest.raises(gv.GlobalVarianceContractError, match="recomputation"):
        dataclasses.replace(res, radius=ls.resolve_lagrangian_radius(spec=radius("c", 16.0),
                                                                     density=res.density))
    with pytest.raises(gv.GlobalVarianceContractError, match="do not reproduce a valid result"):
        dataclasses.replace(res, quadrature=dataclasses.replace(QUAD, grid_points=33,
                                                                comparison_grid_points=17))
    seed2 = dataclasses.replace(pbs.void_share.closure,
                                seed_radius_Mpc=2.0 * pbs.void_share.closure.seed_radius_Mpc)
    with pytest.raises(gv.GlobalVarianceContractError, match="recomputation"):
        dataclasses.replace(pbs.void_share, closure=seed2)
    with pytest.raises(gv.GlobalVarianceContractError, match="recomputation"):
        dataclasses.replace(pbs.void_share, early_spectrum=spectrum(4.0 * 2.1e-9))
    with pytest.raises(gv.GlobalVarianceContractError, match="recomputation"):
        dataclasses.replace(iv, target_premise_rms=999.0)
    with pytest.raises(gv.GlobalVarianceContractError, match="recomputation"):
        dataclasses.replace(res.growth, diagnostics=tuple(
            (k, 0.0 if k.endswith("_rel") else v) for k, v in res.growth.diagnostics))
    with pytest.raises(gv.GlobalVarianceContractError, match="assumptions"):
        dataclasses.replace(res.growth, assumptions=("none",))
    with pytest.raises(gv.GlobalVarianceContractError, match="caveats"):
        dataclasses.replace(res, caveats=("observational",))
    # A resolved radius relabelled with another length (same radius_Mpc) leaves
    # every integral unchanged; only its re-resolution exposes it.
    forged = dataclasses.replace(res.radius, spec=radius("c", 9.0))
    with pytest.raises(gv.GlobalVarianceContractError, match="resolution of its specification"):
        dataclasses.replace(res, radius=forged)


def test_gh_df5_defensive_invariants_are_exercised(growth_gm, monkeypatch):
    """Each defensive check that survived the delta audit's mutants has its own test."""
    with pytest.raises(gv.GlobalVarianceContractError, match="fv0 must be the background"):
        dataclasses.replace(growth_gm, background=NW15)
    res = run(GM, constant(0.05), radius("c"))
    premise = gv.HomogeneityPremise(radius=radius("c", 100.0), max_linear_rms=0.1, provenance="test")
    iv = gv.admissible_global_linear_interval(target=res, premise=premise)
    with pytest.raises(gv.GlobalVarianceContractError, match="target_inside is inconsistent"):
        dataclasses.replace(iv, target_inside=not iv.target_inside)

    # A quadrature that returns an impossible probability is refused (Frechet bounds),
    # and moments that break E[1 1 g1] = E[1 1 g2] are refused.
    def broken(values):
        return lambda rho, c1, c2, nodes, tolerance: (np.array(values), nodes, 0.0)

    monkeypatch.setattr(gv, "_orthant_integrals", broken([1.5, 0.1, 0.1, 0.1, 0.1]))
    with pytest.raises(gv.GlobalVarianceNumericalError, match="outside its bounds"):
        gv.bivariate_normal_orthant_probability(correlation=0.3, threshold_1=0.0,
                                                threshold_2=0.0, nodes=32, tolerance=1e-12)
    with pytest.raises(gv.GlobalVarianceNumericalError, match="outside its bounds"):
        gv.bivariate_normal_orthant_moments(correlation=0.3, threshold=0.0, nodes=32,
                                            tolerance=1e-12)
    monkeypatch.setattr(gv, "_orthant_integrals", broken([0.3, 0.1, 0.2, 0.1, 0.1]))
    with pytest.raises(gv.GlobalVarianceNumericalError, match="E\\[1 1 g1\\] = E\\[1 1 g2\\]"):
        gv.bivariate_normal_orthant_moments(correlation=0.3, threshold=0.0, nodes=32,
                                            tolerance=1e-12)


def test_gh_df5_rounding_budget_needs_the_output_half_unit():
    """The printed total's own half unit is part of the GH-F11 budget (mutant N13)."""
    sp, si, half = 0.3, 0.9, 5e-5
    total = math.hypot(sp, si)
    budget = _evidence().e_reference_rounding_budget(sigma_partition=sp, sigma_internal=si,
                                                     sigma_total=total, half_unit=half)
    assert budget == pytest.approx(half * (sp / total + si / total + 1.0), rel=1e-15, abs=0.0)
    # A total printed 1e-4 away is within the budget only with the output term.
    assert half * (sp / total + si / total) < 1e-4 <= budget


def test_gh_df1_lognormal_laws_share_the_carrier_not_the_conditional_density():
    """GH-DF1: the latent carrier law is shared; the conditionally normalised density is not.

    4-variate sampling of (g1, g2, a1/lam, a2/lam): in both laws the
    unconditionally normalised carrier exp(a)/E[exp(a)] has covariance
    exp(lam^2 xi) - 1; the conditionally normalised density psi has that
    covariance divided by m^2, m = Q(c - kappa0)/f_w (1 in law I).  (H25): the
    total kernel is E[chi1 chi2 psi1 psi2] - f_w^2 = K_ww + 2 K_pw + P11 - f_w^2.
    """
    ev = _evidence()
    rng = np.random.default_rng(29)
    f_v = 0.737
    f_w, c = 1.0 - f_v, norm.ppf(f_v)
    rho, lam, xs0, xsr, g0, gr = 0.6, 0.8, 1.0, 0.45, 0.5, 0.3
    shared = math.expm1(lam * lam * xsr)
    for correlated in (False, True):
        k0, kr = (g0, gr) if correlated else (0.0, 0.0)
        m = norm.sf(c - lam * k0) / f_w                                     # E[carrier | wall]
        if correlated:
            assert m > 1.2                       # law II: an order-unity change of normaliser
        else:
            assert m == pytest.approx(1.0, rel=1e-12, abs=0.0)
        cov = np.array([[1, rho, k0, kr], [rho, 1, kr, k0], [k0, kr, xs0, xsr], [kr, k0, xsr, xs0]])
        z = rng.multivariate_normal(np.zeros(4), cov, size=2_000_000)
        carrier1 = np.exp(lam * z[:, 2] - 0.5 * lam * lam * xs0)          # exp(a)/E[exp(a)]
        carrier2 = np.exp(lam * z[:, 3] - 0.5 * lam * lam * xs0)
        prod = carrier1 * carrier2 - 1.0
        assert abs(prod.mean() - shared) <= 5 * prod.std() / math.sqrt(prod.size)
        psi1, psi2 = carrier1 / m, carrier2 / m                            # E[psi | wall] = 1
        conn = (psi1 - psi1.mean()) * (psi2 - psi2.mean())
        assert abs(conn.mean() - shared / m ** 2) <= 5 * conn.std() / math.sqrt(conn.size)
        chi1, chi2 = z[:, 0] > c, z[:, 1] > c
        p11, kww, kpw = ev.lognormal_mask_kernels(rho=rho, c=c, f_w=f_w, lam=lam, xi_lat_r=xsr,
                                                  kappa0=lam * k0, kappa_r=lam * kr)
        e_pp = math.exp(lam * lam * xsr) * f_w ** 2 * ev._orthant_p(
            rho, c - lam * (k0 + kr), c - lam * (k0 + kr)) / (m * f_w) ** 2
        assert kww + 2.0 * kpw + p11 == pytest.approx(e_pp, rel=1e-10, abs=0.0)   # (H25)
        both = chi1 * chi2 * psi1 * psi2
        assert abs(both.mean() - e_pp) <= 5 * both.std() / math.sqrt(both.size)


def test_gh_df1_law_summary_satisfies_h25_and_includes_the_first_radial_panel():
    """(H25) against the (H17)-(H19) assembly, and the ball pair density on [0, 2R]."""
    ev = _evidence()
    ball = ev._Ball(10.0)
    assert ball.u_full[0] == 0.0 and ball.u_full[-1] == 20.0
    assert ball.integral(np.ones_like(ball.u)) == pytest.approx(1.0, rel=0.0, abs=1e-10)
    f_v = 0.627
    f_w = 1.0 - f_v
    u = ball.u
    c_chi = 0.05 * np.exp(-u / 0.6)
    k_ww = 0.2 * np.exp(-u / 3.0) * (c_chi + f_w ** 2)
    k_pw = 0.01 * np.exp(-u / 1.5)
    out = ev._law_summary(f_v, ball, c_chi, k_ww, k_pw, "synthetic kernels")
    assert out["sigma_total_from_H25"] == pytest.approx(out["sigma_total"], rel=1e-12, abs=0.0)
    expected = math.sqrt((ball.integral(c_chi) + ball.integral(k_ww)
                          + 2.0 * ball.integral(k_pw)) / f_w ** 2)
    assert out["sigma_total"] == pytest.approx(expected, rel=1e-12, abs=0.0)
    assert out["radial_refinement_rel"] < 1e-6


class _FewPointBall:
    """A coarse stand-in for the evidence script's ball quadrature (fast kernel tests)."""

    def __init__(self):
        self.u = np.linspace(0.25, 4.0, 9)

    def integral(self, values, coarse=False):
        pair = self.u ** 2 * np.exp(-self.u)
        step = 2 if coarse else 1
        return float(simpson(pair[::step] * np.asarray(values)[::step], x=self.u[::step]))


def test_gh_df1_lognormal_laws_report_the_law_ii_normaliser():
    """The evidence script's laws carry m_II = Q(c - kappa0)/f_w and m_I = 1 (GH-DF1)."""
    ev = _evidence()
    ball = _FewPointBall()
    f_v, lam, cross0 = 0.737, 0.8, 0.5
    c = norm.ppf(f_v)
    u = ball.u
    rho_g = np.exp(-u / 1.5)
    xi_lat = np.exp(-u / 2.0)
    cross = cross0 * np.exp(-u / 1.8)
    laws = ev._lognormal_laws(f_v, c, ball, rho_g, lam, xi_lat, cross0, cross)
    assert laws["I_independent"]["conditional_normaliser_ratio_m"] == 1.0
    assert laws["II_same_field"]["conditional_normaliser_ratio_m"] == pytest.approx(
        norm.sf(c - lam * cross0) / (1.0 - f_v), rel=1e-12, abs=0.0)
    for law in laws.values():
        assert law["sigma_total_from_H25"] == pytest.approx(law["sigma_total"], rel=1e-12, abs=0.0)


def test_gh_df5_pbs_reclosure_rescales_the_input_spectrum_by_the_factor_squared(growth_gm):
    """The evidence helper: reclosure equals post-hoc for a constant share only (mutant N10)."""
    ev = _evidence()
    factor = 0.97
    clos = ev.closures(growth_gm, ev.seed_radii(GM, growth_gm))
    spec = ev.radius_spec("c_bare_volume_average", 8.0)
    names = ("monotone_lower_p_fvLS", "pbs_tracker_seed_compressed",
             "pbs_tracker_seed_F_median_compressed")
    rows = {name: ev.summary(ev.run_case(GM, clos[name], ev.early_spectrum(), spec), factor, 1.0)
            for name in names}
    out = ev.pbs_reclosure(GM, clos, spec, factor, rows, "c_bare_volume_average")
    assert out["A_s_factor"] == pytest.approx(factor ** 2, rel=1e-15, abs=0.0)
    assert out["monotone_lower_p_fvLS"]["reclosure_over_post_hoc"] == pytest.approx(
        1.0, rel=1e-10, abs=0.0)
    for name in names[1:]:
        assert out[name]["share_k0_reclosure"] > out[name]["share_k0_direct"]
        assert out[name]["reclosure_over_post_hoc"] > 1.005


# -------------------------------- second delta-audit remediation (2026-10-08)
def test_gh_d2f2_law_summary_reports_the_pair_weighted_both_walls_covariance():
    """<P11 (C_W - 1)>/<P11>, C_W = E[psi1 psi2 | both walls] (mutant A18), and (H25).

    Synthetic kernels.  C_W is formed pointwise from its definition,
    ``C_W = E[chi1 chi2 psi1 psi2]/P11 = 1 + (K_ww + 2 K_pw)/P11``, and the
    ball variance from ``1 + xi_delta = P11 C_W/f_w^2`` (empty voids).
    """
    ev = _evidence()
    ball = ev._Ball(11.0)
    f_v = 0.737
    f_w = 1.0 - f_v
    u = ball.u
    c_chi = f_v * f_w * np.exp(-u / 0.8)                 # P11 falls from f_w to f_w^2
    p11 = c_chi + f_w ** 2
    k_ww = 0.3 * np.exp(-u / 2.5) * p11
    k_pw = 0.02 * np.exp(-u / 1.2)
    out = ev._law_summary(f_v, ball, c_chi, k_ww, k_pw, "synthetic kernels")
    c_w = 1.0 + (k_ww + 2.0 * k_pw) / p11
    assert out["both_walls_product_moment_excess_ball"] == pytest.approx(
        ball.integral(p11 * (c_w - 1.0)) / ball.integral(p11), rel=1e-12, abs=0.0)
    assert out["sigma_total"] ** 2 == pytest.approx(
        ball.integral(p11 * c_w / f_w ** 2 - 1.0), rel=1e-11, abs=0.0)


def test_gh_d2f2_lognormal_pairs_report_the_inverse_square_of_the_law_ii_normaliser():
    """1/m_II^2, carrier/m_II^2 and 1/m_II - 1 of ``lognormal_pairs`` (mutant A20).

    A synthetic spectrum on a few separations; m_II = Q(c - kappa0)/f_w is
    re-derived from lam and the one-point mask-carrier covariance.
    """
    ev = _evidence()
    ball = _FewPointBall()
    f_v = 0.737
    f_w, c = 1.0 - f_v, float(norm.ppf(f_v))
    lnk = np.linspace(math.log(1e-3), math.log(30.0), 1201)
    k = np.exp(lnk)
    d2 = 0.4 * (k / 0.3) ** 3 / (1.0 + (k / 0.3) ** 3) * np.exp(-(k / 3.0) ** 2)
    ell = 0.5
    g_ell = np.exp(-0.5 * (k * ell) ** 2)
    var_g = float(simpson(d2 * g_ell ** 2, x=lnk))
    rho_g = ev._xi_table(k, lnk, d2, ball.u, g_ell, g_ell) / var_g
    xi_w = ev._xi_table(k, lnk, d2, ball.u)
    signed = {law: {"wall_moment": 0.01, "partition_wall_moment": 0.001}
              for law in ("I_independent", "II_same_field")}
    out = ev.lognormal_pairs(f_v, c, ball, k, lnk, d2, ell, xi_w, rho_g, signed)
    assert set(out["members"]) == {"r_s_1_Mpc", "r_s_2_Mpc", "r_s_4_Mpc"}
    for member in out["members"].values():
        lam, rs = member["latent_scale_lambda"], member["resolution_radius_Mpc"]
        g_s = np.exp(-0.5 * (k * rs) ** 2)
        kappa0 = lam * float(simpson(d2 * g_s * g_ell, x=lnk)) / math.sqrt(var_g)
        m = norm.sf(c - kappa0) / f_w                                  # E[carrier | wall]
        assert m > 1.2
        assert member["conditional_normaliser_ratio_m_II"] == pytest.approx(m, rel=1e-12, abs=0.0)
        assert (member["laws"]["II_same_field"]["conditional_normaliser_ratio_m"]
                == member["conditional_normaliser_ratio_m_II"])
        assert member["conditional_density_covariance_ratio_II_over_I"] == pytest.approx(
            1.0 / m ** 2, rel=1e-12, abs=0.0)
        assert member["ball_variance_unmasked_conditional_density_II"] == pytest.approx(
            member["ball_variance_unconditionally_normalised_carrier"] / m ** 2, rel=1e-12, abs=0.0)
        assert member["unconditional_mean_conditional_contrast_II"] == pytest.approx(
            1.0 / m - 1.0, rel=1e-12, abs=0.0)
        assert member["ball_variance_unconditionally_normalised_carrier"] == pytest.approx(
            out["ball_variance_signed_carrier"], rel=1e-9, abs=0.0)


def test_gh_d2f2_conditional_wall_density_by_sample_normalised_monte_carlo():
    """C_W(r), m_II and the m_II^-2 covariance against sampling (second delta audit).

    psi is the carrier divided by its *sample* mean on the walls, so neither
    the normaliser nor the covariance ratio is put in by construction.  The
    normaliser uses the first point of each draw only (independent samples).
    Each budget is conservative: five times the sum of the independent-sample
    standard errors of the statistic and of the normaliser term, with no
    credit for their correlation (third delta audit GH-D3F3).
    """
    ev = _evidence()
    rng = np.random.default_rng(31)
    f_v = 0.737
    f_w, c = 1.0 - f_v, norm.ppf(f_v)
    rho, lam, xs0, xsr, g0, gr = 0.6, 0.8, 1.0, 0.45, 0.5, 0.3
    ball = _FewPointBall()
    ones = np.ones_like(ball.u)
    laws = ev._lognormal_laws(f_v, c, ball, rho * ones, lam, xsr * ones, g0, gr * ones)
    shared = math.expm1(lam * lam * xsr)
    for law, correlated in (("I_independent", False), ("II_same_field", True)):
        k0, kr = (g0, gr) if correlated else (0.0, 0.0)
        cov = np.array([[1, rho, k0, kr], [rho, 1, kr, k0], [k0, kr, xs0, xsr], [kr, k0, xsr, xs0]])
        z = rng.multivariate_normal(np.zeros(4), cov, size=2_000_000)
        chi1, chi2 = z[:, 0] > c, z[:, 1] > c
        carrier1 = np.exp(lam * z[:, 2] - 0.5 * lam * lam * xs0)       # exp(a)/E[exp(a)]
        carrier2 = np.exp(lam * z[:, 3] - 0.5 * lam * lam * xs0)
        on_wall = carrier1[chi1]                                        # one point per draw
        m_s = on_wall.mean()                                            # sample E[carrier | wall]
        se_m = on_wall.std() / math.sqrt(on_wall.size)
        m = laws[law]["conditional_normaliser_ratio_m"]
        assert abs(m_s - m) <= 5 * se_m
        both = chi1 & chi2
        cw_mc = carrier1[both] * carrier2[both] / m_s ** 2               # psi1 psi2 | both walls
        p11, kww, kpw = ev.lognormal_mask_kernels(rho=rho, c=c, f_w=f_w, lam=lam, xi_lat_r=xsr,
                                                  kappa0=lam * k0, kappa_r=lam * kr)
        c_w = 1.0 + (kww + 2.0 * kpw) / p11
        budget = cw_mc.std() / math.sqrt(cw_mc.size) + 2.0 * cw_mc.mean() * se_m / m_s
        assert abs(cw_mc.mean() - c_w) <= 5 * budget
        psi1, psi2 = carrier1 / m_s, carrier2 / m_s
        conn = (psi1 - psi1.mean()) * (psi2 - psi2.mean())
        budget = conn.std() / math.sqrt(conn.size) + 2.0 * abs(conn.mean()) * se_m / m_s
        assert abs(conn.mean() - shared / m ** 2) <= 5 * budget


def test_gh_d2f2_ball_half_resolution_estimate_has_the_simpson_error_ratio():
    """The coarse estimate is Simpson's rule at twice the spacing (mutants A15, A16).

    The ball pair density is a quintic in u with unit integral, so the
    composite Simpson error is exactly ``(h^4/180)[f'''(2R) - f'''(0)] =
    (h^4/180) 45/R^4`` and the coarse error is 16 times the fine one; for a
    kernel with a sub-Mpc scale the ratio tends to 16 with an O(h^2) correction
    (15.96 here).  Tolerances: round-off is about 1e-4 of the 9.3e-13 error.
    """
    ev = _evidence()
    R = 10.0
    ball = ev._Ball(R)
    h = 2.0 * R / ev.RADIAL_INTERVALS
    ones = np.ones_like(ball.u)
    error = h ** 4 / 180.0 * 45.0 / R ** 4
    assert ball.integral(ones) - 1.0 == pytest.approx(error, rel=2e-3, abs=0.0)
    assert ball.integral(ones, coarse=True) - 1.0 == pytest.approx(16.0 * error, rel=2e-3, abs=0.0)
    a = 0.3

    def integrand(x):
        return (3.0 * x ** 2 / R ** 3) * (1.0 - 3.0 * x / (4.0 * R) + x ** 3 / (16.0 * R ** 3)) \
            * math.exp(-x / a)

    exact = quad(integrand, 0.0, 2.0 * R, epsabs=0.0, epsrel=1e-13, limit=400,
                 points=[0.5, 1.0, 2.0, 5.0])[0]
    kernel = np.exp(-ball.u / a)
    ratio = (ball.integral(kernel, coarse=True) - exact) / (ball.integral(kernel) - exact)
    assert ratio == pytest.approx(16.0, rel=5e-3, abs=0.0)


def test_gh_d2f2_binding_boundary_and_record_identities():
    """2 RECORD_IDENTITY_RTOL is refused, a quarter of it accepted (A01); A07; A09."""
    res = run(GM, constant(0.05), radius("c"))
    rtol = gv.RECORD_IDENTITY_RTOL
    eps_rms = res.void_volume_response_rms           # checked by the binding only
    with pytest.raises(gv.GlobalVarianceContractError, match="void_volume_response_rms differs"):
        dataclasses.replace(res, void_volume_response_rms=eps_rms * (1.0 + 2.0 * rtol))
    near = dataclasses.replace(res, void_volume_response_rms=eps_rms * (1.0 + 0.25 * rtol))
    assert near.void_volume_response_rms != eps_rms
    premise = gv.HomogeneityPremise(radius=radius("c", 100.0), max_linear_rms=0.1, provenance="test")
    iv = gv.admissible_global_linear_interval(target=res, premise=premise)
    with pytest.raises(gv.GlobalVarianceContractError,
                       match="class_assumptions must be the module's interval assumptions"):
        dataclasses.replace(iv, class_assumptions=("x",))
    # An equal copy of the background reproduces every value, so only the
    # identity check refuses a density built on it.
    pbs = run(GM, tracker_seed(GM, res.growth, 15.0, gv.SeedVolumeCompression.COMPRESSED_WITH_REGION),
              radius("c"))
    density = dataclasses.replace(pbs.void_share.density, background=dataclasses.replace(GM))
    assert density == pbs.void_share.density
    with pytest.raises(gv.GlobalVarianceContractError,
                       match="density and growth must share the background object"):
        dataclasses.replace(pbs.void_share, density=density)


def test_gh_d2f2_evidence_thresholds_are_pinned():
    """Every declared gate threshold and grid (mutants A22, A23): a change is a recorded decision."""
    ev = _evidence()
    assert ev.GATES == {
        "D_owner_A_v_printed_digits": 0.5, "D_owner_X_SU_printed_digits": 5e-4,
        "constant_share_A_s_scaling_rel": 1e-10, "pbs_void_term_A_s_independence_rel": 2e-3,
        "refined_quadrature_rel": 2e-6, "E_reference_printed_half_unit": 5e-5,
        "gt_orthant_P11_vs_bivariate_cdf_abs": 1e-10, "orthant_analytic_cases_abs": 1e-12,
        "m3_bias_finite_difference_rel": 1e-6, "lognormal_ball_variance_calibration_rel": 1e-9,
        "lognormal_linear_limit_rel": 5e-2, "step_kernel_premise_ratio": 1.0,
        "reclosure_constant_share_rel": 1e-10, "radial_refinement_rel": 1e-5,
        "h25_identity_rel": 1e-12}
    assert (ev.RADIAL_INTERVALS, ev.ORTHANT_TOLERANCE, ev.ORTHANT_START_NODES) == (1440, 1e-12, 32)
    assert gv.RECORD_IDENTITY_RTOL == 1e-12                         # GH-D3F3 (mutant B01)


def test_gh_d2f4_float_results_must_be_floats_and_scalar_inputs_are_stored_as_floats(growth_gm):
    """An equal Fraction no longer passes the binding; inputs are coerced (strict JSON)."""
    res = run(GM, constant(0.05), radius("c"))
    with pytest.raises(gv.GlobalVarianceContractError,
                       match="linear_sigma must be a float, not Fraction"):
        dataclasses.replace(res, linear_sigma=Fraction(res.linear_sigma))
    with pytest.raises(gv.GlobalVarianceContractError, match="must be a real scalar"):
        dataclasses.replace(res, linear_sigma=Decimal(repr(res.linear_sigma)))
    nfev_as_int = tuple((k, int(v)) if k.endswith("_nfev") else (k, v)
                        for k, v in growth_gm.diagnostics)
    with pytest.raises(gv.GlobalVarianceContractError, match="diagnostics differs"):
        dataclasses.replace(growth_gm, diagnostics=nfev_as_int)
    checks = dataclasses.replace(CHECKS, identity_tolerance=Fraction(1, 10 ** 12))
    assert type(checks.identity_tolerance) is float and checks == CHECKS
    growth = dataclasses.replace(growth_gm, G=Fraction(1), checks=checks)
    assert type(growth.G) is float and growth == growth_gm
    json.dumps(growth.to_json_dict(), allow_nan=False)


# --------------------------------- third delta-audit remediation (2026-10-09)
def test_gh_d3f3_every_growth_check_and_g_are_stored_as_floats(growth_gm):
    """All five TwoPhaseGrowthChecks tolerances and G are stored as native floats (mutant B10)."""
    names = ("identity_tolerance", "ode_rtol", "ode_atol", "ode_cross_check_tolerance",
             "root_xtol_fraction")
    checks = dataclasses.replace(CHECKS, **{name: Fraction(getattr(CHECKS, name)) for name in names})
    for name in names:
        assert type(getattr(checks, name)) is float
        assert getattr(checks, name) == getattr(CHECKS, name)
    growth = dataclasses.replace(growth_gm, G=Fraction(1), checks=checks)
    assert type(growth.G) is float and growth == growth_gm
    json.dumps(growth.to_json_dict(), allow_nan=False)


def test_gh_d3f3_float_results_accept_float64_and_subclasses_but_not_float32():
    """numpy.float64 and float subclasses are floats; numpy.float32 is not (mutants B02, B03)."""
    res = run(GM, constant(0.5), radius("c"))

    class _Float(float):
        pass

    for value in (np.float64(res.linear_sigma), _Float(res.linear_sigma)):
        assert dataclasses.replace(res, linear_sigma=value).linear_sigma == res.linear_sigma
    # 0.5 is exact in float32, so only the type policy can refuse it.
    with pytest.raises(gv.GlobalVarianceContractError,
                       match="share_k0 must be a float, not float32"):
        dataclasses.replace(res.void_share, share_k0=np.float32(0.5))


def test_gh_d3f3_binding_tolerance_boundary_with_a_literal_rtol():
    """1.05e-12 relative is refused and 0.95e-12 accepted, independently of the constant (B01)."""
    res = run(GM, constant(0.05), radius("c"))
    eps_rms = res.void_volume_response_rms
    with pytest.raises(gv.GlobalVarianceContractError, match="void_volume_response_rms differs"):
        dataclasses.replace(res, void_volume_response_rms=eps_rms * (1.0 + 1.05e-12))
    dataclasses.replace(res, void_volume_response_rms=eps_rms * (1.0 + 0.95e-12))


def test_gh_d3f2_nested_inputs_must_export_as_strict_json():
    """A Fraction, float32 or int64 inside a nested 1G-B input record is refused (GH-D3F2).

    The values are equal, so the recomputation binding accepts them; only the
    strict-JSON check of the export refuses the record.
    """
    res = run(GM, constant(0.05), radius("c"))
    for field, value in (("k_min_per_Mpc", Fraction(QUAD.k_min_per_Mpc)),
                         ("truncation_tolerance", np.float32(QUAD.truncation_tolerance)),
                         ("grid_points", np.int64(QUAD.grid_points))):
        quadrature = dataclasses.replace(QUAD, **{field: value})
        with pytest.raises(gv.GlobalVarianceContractError, match="export is not strict JSON"):
            dataclasses.replace(res, quadrature=quadrature)
    premise = gv.HomogeneityPremise(radius=radius("c", 100.0), max_linear_rms=0.1, provenance="test")
    iv = gv.admissible_global_linear_interval(target=res, premise=premise)
    for record in (res, res.growth, res.void_share, iv):
        json.dumps(record.to_json_dict(), allow_nan=False)
    for record in (res.growth.matching, res.growth.checks, res.void_share.closure, premise):
        json.dumps(record.to_metadata(), allow_nan=False)


def test_gh_d4f1_seed_share_and_interval_exports_must_be_strict_json(growth_gm):
    """The seed-share and interval records refuse an equal Fraction in a nested input (GH-D4F1).

    Each refusal must come from that record's own check (mutants X02, X04 of
    the fourth delta audit remove one of them).
    """
    density = ls.early_matter_density_per_photon(background=growth_gm.background,
                                                 identity_tolerance=1e-13, G=G)
    seed_quadrature = dataclasses.replace(
        SEED_QUAD, truncation_tolerance=Fraction(SEED_QUAD.truncation_tolerance))
    with pytest.raises(gv.GlobalVarianceContractError, match="^void share: the export is not strict JSON"):
        gv.evaluate_void_share(
            closure=tracker_seed(GM, growth_gm, 15.0, gv.SeedVolumeCompression.COMPRESSED_WITH_REGION),
            growth=growth_gm, density=density, early_spectrum=spectrum(), seed_quadrature=seed_quadrature)
    res = run(GM, constant(0.05), radius("c"))
    premise = gv.HomogeneityPremise(radius=radius("c", 100.0), max_linear_rms=0.1, provenance="test")
    iv = gv.admissible_global_linear_interval(target=res, premise=premise)
    premise_radius = dataclasses.replace(iv.premise_radius,
                                         radius_Mpc=Fraction(iv.premise_radius.radius_Mpc))
    with pytest.raises(gv.GlobalVarianceContractError,
                       match="^interval record: the export is not strict JSON"):
        dataclasses.replace(iv, premise_radius=premise_radius)
