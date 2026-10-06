"""Phase 1G-H evidence: conditional global-mean linear matter variance.

Report: ``reports/phase1g_h_global_variance_closure.md`` ([1G-H]); equations
(H1)-(H24) there.  Runtime: ``timescape_fsigma8.global_variance`` (experimental,
conditional).  Writes the git-ignored
``artifacts/independent/phase1g_h_global_variance_closure.json`` and figures
under ``artifacts/independent/phase1g_h/``; prints a summary and exits
nonzero if a declared gate fails.

Scenarios (declared, never combined): [GM] PAPER_REFERENCE (f_v0 = 0.737,
H0 = 73.03) and the [NW15] Timescape CMB fit (f_v0 = 0.627, H0 = 61.0, as in
1G-A/B/D).  Early universe: Planck 2018 A_s, n_s, k_p and baryon fraction
(script-level explicit inputs, PROVISIONAL_MODEL_IMPORT; [NW15] l. 1422 leave
A_s unconstrained), EH98 zero-baryon transfer at the per-photon omega_m,eff.
Matching epoch z = 1090 (1G-D, 1G-F).  Every number is CONDITIONAL,
MODEL-INTERNAL and NON_OBSERVATIONAL; none is an observational amplitude.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

import numpy as np
from scipy.integrate import simpson
from scipy.optimize import brentq
from scipy.special import ndtri, spherical_jn

import timescape_fsigma8.global_variance as gv
import timescape_fsigma8.lagrangian_sigma as ls
from timescape_fsigma8 import scientific_status
from timescape_fsigma8.perturbations.initial_conditions import PLANCK_2018_QPLUS_RECIPE, qplus
from timescape_fsigma8.presets import PAPER_REFERENCE

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "independent" / "phase1g_h_global_variance_closure.json"
FIGURES = ROOT / "artifacts" / "independent" / "phase1g_h"
E_OWNER_INVENTORY = ROOT / "reports" / "phase1g_e_owner_decisions_successor_inventory.json"

NA = ls.NOT_APPLICABLE
G = 1.0                                   # cancels everywhere; explicit (no package default)
IDENTITY_RTOL = 1e-13                     # per-photon density identity (as 1G-B)
Z_LS = 1090.0                             # 1G-D / 1G-F matching redshift (a_LS = 1/1091)
MATCHING = gv.LastScatteringMatching(
    z_last_scattering=Z_LS,
    provenance="1G-D Sec. 6 and 1G-F: photon-normalised last scattering, a_LS = 1/1091")
CHECKS = gv.TWO_PHASE_GROWTH_REFERENCE_CHECKS

# Planck 2018 early-universe inputs (as the 1G-B validation driver).
OMEGA_M_LCDM = PLANCK_2018_QPLUS_RECIPE.omega_m * PLANCK_2018_QPLUS_RECIPE.h ** 2
H_LCDM = PLANCK_2018_QPLUS_RECIPE.h
PRIMARY_FB = 0.02237 / OMEGA_M_LCDM
PLANCK_PROVENANCE = "Planck 2018 VI (arXiv:1807.06209) Table 2, TT,TE,EE+lowE+lensing"
ANCHOR = 0.8111
ANCHOR_TOLERANCE = 0.05
ANCHOR_RATIONALE = (
    "EH98 zero-baryon-oscillation fit omits BAO wiggles and the 0.06 eV neutrino "
    "suppression; anchored ratios cancel the common bias ([1G-A] Sec. 6.3)")

# Quadratures (explicit; AGENTS.md rule 9).  Main: the 1G-B reference grid.
# Seed: the seed radius is ~0.1-15 Mpc, so k reaches 1e4 Mpc^-1.
QUAD = ls.LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE
SEED_QUAD = ls.LagrangianSigmaQuadrature(
    k_min_per_Mpc=1e-6, k_max_per_Mpc=1e4, grid_points=12001,
    comparison_grid_points=6001, self_convergence_tolerance=1e-6,
    truncation_tolerance=1e-8)
# Large radii (the flat-wall capacity root, 20-3000 Mpc): a dense low-k grid.
LARGE_R_QUAD = ls.LagrangianSigmaQuadrature(
    k_min_per_Mpc=1e-7, k_max_per_Mpc=30.0, grid_points=32001,
    comparison_grid_points=16001, self_convergence_tolerance=1e-6,
    truncation_tolerance=1e-8)
REFINED_QUAD = ls.LagrangianSigmaQuadrature(
    k_min_per_Mpc=1e-7, k_max_per_Mpc=1e3, grid_points=16001,
    comparison_grid_points=8001, self_convergence_tolerance=1e-7,
    truncation_tolerance=1e-10)

# Void sizes and seeds.
W09_VOID_DIAMETER_H_MPC = 30.0            # [W09] l. 277
SVDW_FACTOR = 1.72                        # [SvdW04] shell-crossing radius factor as 1G-D
F_MEDIAN_RADIUS_H_MPC = {"PAPER_REFERENCE": 2.40456, "NW15_CMB_FIT": 2.80045}  # 1G-F successor Sec. 2
# Two-barrier thresholds (1G-F successor Sec. 2; [JLH13] (A8)-(A12)).
DELTA_C_EDS = 3.0 * (12.0 * math.pi) ** (2.0 / 3.0) / 20.0
DELTA_V_SHELL = -2.7171803438378705
X_SHELL = 0.20472233400490963

# Homogeneity-premise readings of [W09] ll. 327-335, 455-458 (sphere radius
# in the target's convention, max linear rms).
PREMISES = {
    "W09_10pct_at_100": (100.0, 0.10),
    "W09_10pct_at_150": (150.0, 0.10),
    "W09_several_pct_6pct_at_100": (100.0, 0.06),
    "cell_side_100_as_sphere_62": (100.0 * (3.0 / (4.0 * math.pi)) ** (1.0 / 3.0), 0.10),
}
RADIUS_SCAN_H_MPC = (6.0, 7.0, 8.0, 9.0, 10.0, 12.0)
A_S_FACTORS = (0.5, 2.0)

GATES = {
    "D_owner_A_v_printed_digits": 0.5,           # A_v 1169 / 1185 (integers)
    "D_owner_X_SU_printed_digits": 5e-4,         # X_SU 1.263 / 1.285 (3 decimals)
    "constant_share_A_s_scaling_rel": 1e-10,     # sigma^2 proportional to A_s at fixed p
    "pbs_void_term_A_s_independence_rel": 2e-3,  # window shape at fixed R_s only
    "refined_quadrature_rel": 2e-6,              # main vs refined grid
    "E_reference_reproduction_abs": 6e-4,        # sqrt(sp^2 + si^2) vs printed 4 decimals
    "gt_orthant_P11_vs_bivariate_cdf_abs": 1e-10,
    "m3_bias_finite_difference_rel": 1e-6,
}


def early_spectrum(A_s: float = 2.100e-9) -> ls.EarlySpectrumImport:
    return ls.EarlySpectrumImport(
        A_s=A_s, n_s=0.9649, k_pivot_per_Mpc=0.05, baryon_fraction=PRIMARY_FB,
        T_cmb_K=2.7255, transfer_model=ls.EarlyTransferModel.EH98_ZERO_BARYON_OSCILLATION,
        provenance=PLANCK_PROVENANCE + "; T_cmb 2.7255 K",
        import_status=ls.EARLY_SPECTRUM_IMPORT_STATUS)


def backgrounds() -> dict[str, ls.TimescapeTrackerInput]:
    return {
        "PAPER_REFERENCE": ls.TimescapeTrackerInput.from_reference_preset(preset=PAPER_REFERENCE),
        "NW15_CMB_FIT": ls.TimescapeTrackerInput(
            label="NW15_CMB_FIT", fv0=0.627, H0_dressed_km_s_Mpc=61.0,
            source="Nazer & Wiltshire, arXiv:1410.3470v2 (Timescape CMB fit; as 1G-A/B/D)"),
    }


def radius_spec(kind: str, length: float) -> ls.LagrangianRadiusSpec:
    C = ls.LagrangianRadiusConvention
    if kind == "a_equal_mass":
        return ls.LagrangianRadiusSpec(
            convention=C.EQUAL_LAGRANGIAN_MASS_TO_REFERENCE, length_h_inverse_Mpc=NA,
            reference_omega_m=OMEGA_M_LCDM, reference_radius_Mpc=length / H_LCDM,
            explicit_radius_Mpc=NA)
    convention = {"c_bare_volume_average": C.BARE_VOLUME_AVERAGE_PROPER_LENGTH,
                  "b_dressed_wall_comoving": C.DRESSED_WALL_COMOVING_LENGTH}[kind]
    return ls.LagrangianRadiusSpec(convention=convention, length_h_inverse_Mpc=length,
                                   reference_omega_m=NA, reference_radius_Mpc=NA,
                                   explicit_radius_Mpc=NA)


CONVENTIONS = ("c_bare_volume_average", "a_equal_mass", "b_dressed_wall_comoving")


def seed_radii(bg_in: ls.TimescapeTrackerInput, growth: gv.TwoPhaseGlobalGrowth) -> dict:
    h = bg_in.H0_dressed_km_s_Mpc / 100.0
    g0 = growth.gamma_w0

    def tracker(present_proper_Mpc: float) -> float:
        return gv.tracker_consistent_seed_radius(
            present_void_radius_volume_average_proper_Mpc=present_proper_Mpc,
            f_v_seed=growth.f_v_ls, fv0=growth.fv0, gamma_w0=g0)

    w09 = (W09_VOID_DIAMETER_H_MPC / 2.0) / h
    return {
        "tracker_seed_W09_15": (tracker(w09), "GD-OD1 tracker-consistent seed, [W09] l. 277 "
                                "30 h^-1 Mpc diameter with dressed h (1G-D primary)"),
        "tracker_seed_F_median": (
            tracker(F_MEDIAN_RADIUS_H_MPC[bg_in.label] * g0 / h),
            "GD-OD1 mapping of the 1G-F volume-weighted median radius (photon-comoving "
            "h^-1 Mpc, times gamma_w0 for volume-average proper length)"),
        "tracker_seed_W09_7.5": (tracker(w09 / 2.0), "half the [W09] radius (sensitivity)"),
        "tracker_seed_W09_30": (tracker(2.0 * w09), "twice the [W09] radius (sensitivity)"),
        "svdw04_factor_1.72": (w09 / SVDW_FACTOR, "1G-D alternative: [W09] radius over the "
                               "[SvdW04] shell-crossing factor 1.72"),
    }


def closures(growth: gv.TwoPhaseGlobalGrowth, seeds: dict) -> dict:
    C = gv.SeedVolumeCompression
    out = {
        "wall_mode_p0": gv.ConstantVoidShare(
            share=0.0, provenance="1G-D wall-curvature mode (S1), void volume untouched",
            evidence_class="REFERENCE_BOUND"),
        "monotone_lower_p_fvLS": gv.ConstantVoidShare(
            share=growth.f_v_ls, provenance="H-A7 monotone lower end: void fraction not "
            "increasing with the overdensity", evidence_class="REFERENCE_BOUND"),
        "strict_flat_walls_p1": gv.ConstantVoidShare(
            share=1.0, provenance="[GM] l. 620 flat walls read regionally (no wall mode)",
            evidence_class="REFERENCE_BOUND"),
    }
    r_primary, prov = seeds["tracker_seed_W09_15"]
    out["pbs_tracker_seed_compressed"] = gv.GaussianThresholdSeedVoidShare(
        seed_radius_Mpc=r_primary, seed_radius_provenance=prov,
        compression=C.COMPRESSED_WITH_REGION)
    out["pbs_tracker_seed_threshold_only_1G_D"] = gv.GaussianThresholdSeedVoidShare(
        seed_radius_Mpc=r_primary, seed_radius_provenance=prov,
        compression=C.THRESHOLD_SHIFT_ONLY)
    r_alt, prov_alt = seeds["svdw04_factor_1.72"]
    out["pbs_svdw04_seed_compressed"] = gv.GaussianThresholdSeedVoidShare(
        seed_radius_Mpc=r_alt, seed_radius_provenance=prov_alt,
        compression=C.COMPRESSED_WITH_REGION)
    r_f, prov_f = seeds["tracker_seed_F_median"]
    out["pbs_tracker_seed_F_median_compressed"] = gv.GaussianThresholdSeedVoidShare(
        seed_radius_Mpc=r_f, seed_radius_provenance=prov_f,
        compression=C.COMPRESSED_WITH_REGION)
    return out


def run_case(bg_in, closure, spec, radius, quadrature=QUAD):
    seed_q = NA if isinstance(closure, gv.ConstantVoidShare) else SEED_QUAD
    return gv.conditional_global_linear_sigma(
        background=bg_in, matching=MATCHING, growth_checks=CHECKS,
        void_share_closure=closure, early_spectrum=spec, radius=radius,
        quadrature=quadrature, seed_quadrature=seed_q,
        density_identity_tolerance=IDENTITY_RTOL, G=G)


def summary(r: gv.ConditionalGlobalLinearSigma, anchor_factor: float, g_lcdm: float) -> dict:
    return {"radius_Mpc": r.radius.radius_Mpc, "unit_growth_sigma": r.unit_growth_sigma,
            "share_k0": r.void_share.share_k0, "propagator_k0": r.propagator_k0,
            "effective_propagator": r.effective_propagator,
            "scale_dependence_rel": r.effective_propagator / r.propagator_k0 - 1.0,
            "growth_ratio_to_lcdm_X": r.propagator_k0 / g_lcdm,
            "linear_sigma_direct_A_s": r.linear_sigma,
            "linear_sigma_planck_anchored": r.linear_sigma * anchor_factor,
            "wall_share_rms": r.wall_share_rms, "void_share_rms": r.void_share_rms,
            "share_terms_coherence": r.share_terms_coherence,
            "void_volume_response_rms": r.void_volume_response_rms,
            "void_response_regime": r.void_response_regime,
            "flat_wall_capacity_ratio": r.flat_wall_capacity_ratio,
            "quadrature_relative_change": r.quadrature_relative_change,
            "void_onset_response_A_v": r.void_share.void_onset_response,
            "nu": r.void_share.nu, "sigma_seed": r.void_share.sigma_seed}


# ---------------------------------------------------------------- anchoring
def anchor_factor() -> dict:
    ref = ls.lcdm_reference_linear_sigma(recipe=PLANCK_2018_QPLUS_RECIPE,
                                         early_spectrum=early_spectrum(),
                                         radius_Mpc=8.0 / H_LCDM, quadrature=QUAD)
    offset = ref.linear_sigma / ANCHOR - 1.0
    if not abs(offset) <= ANCHOR_TOLERANCE:
        raise AssertionError(f"LCDM reference offset {offset:+.3%} exceeds the anchor tolerance")
    return {"lcdm_eh98_linear_sigma": ref.linear_sigma, "anchor": ANCHOR,
            "anchor_provenance": PLANCK_PROVENANCE, "anchor_rationale": ANCHOR_RATIONALE,
            "factor": ANCHOR / ref.linear_sigma, "offset": offset,
            "g_lcdm_qplus0": ref.growth_today_photon_normalised,
            "meaning": "multiplies the direct A_s-normalised EH98 value by the "
                       "Boltzmann-to-EH98 ratio at the Planck parameters; late-time LCDM "
                       "growth cancels exactly"}


# ---------------------------------------------------------- flat-wall capacity
def flat_wall_capacity_radius(bg_in, growth, density, spec) -> dict:
    """Radius where the matching-epoch rms equals the flat-wall cap (H13)."""
    cap = gv.strict_flat_wall_contrast_cap(void_volume_fraction=growth.f_v_ls)
    om = density.omega_m_per_photon

    def excess(log_r):
        sigma_u = gv.unit_growth_lagrangian_sigma(radius_Mpc=math.exp(log_r), omega_m=om,
                                                  early_spectrum=spec, quadrature=LARGE_R_QUAD)
        return sigma_u / (1.0 + Z_LS) - cap

    log_r = brentq(excess, math.log(20.0), math.log(3000.0), xtol=1e-10)
    R = math.exp(log_r)
    return {"cap_f_v_ls_over_f_w_ls": cap, "radius_Mpc": R,
            "radius_bare_h_inv_Mpc": R * growth.gamma_w0 * density.h_bare,
            "radius_dressed_h_inv_Mpc": R * density.h_dressed}


# ------------------------------------------------------------- A_s scaling
def a_s_scaling(bg_in, growth_closures, radius) -> dict:
    out = {}
    base_spec = early_spectrum()
    for name in ("monotone_lower_p_fvLS", "pbs_tracker_seed_compressed"):
        clo = growth_closures[name]
        base = run_case(bg_in, clo, base_spec, radius)
        rows = {}
        for factor in A_S_FACTORS:
            r = run_case(bg_in, clo, early_spectrum(2.100e-9 * factor), radius)
            rows[f"x{factor:g}"] = {
                "linear_sigma_ratio": r.linear_sigma / base.linear_sigma,
                "sqrt_A_s_ratio": math.sqrt(factor),
                "wall_share_rms_ratio": r.wall_share_rms / base.wall_share_rms,
                "void_share_rms_ratio": (r.void_share_rms / base.void_share_rms
                                         if base.void_share_rms > 0 else NA),
                "share_k0_ratio": r.void_share.share_k0 / base.void_share.share_k0,
                "d_ln_sigma_d_ln_A_s": math.log(r.linear_sigma / base.linear_sigma)
                / math.log(factor)}
        out[name] = rows
    return out


# ---------------------------------------------------------- two-barrier (M3)
def m3_alternative(growth, density, spec, radius_record) -> dict:
    """Excursion-set M3 response (H22) with the C1 wall clock (1G-F)."""
    out = {"delta_c": DELTA_C_EDS, "delta_v": DELTA_V_SHELL, "x_shell": X_SHELL}
    d_wall0 = growth.wall_share_growth * (1.0 - growth.f_v_ls) / (1.0 - growth.fv0)
    out["C1_clock_growth_today"] = d_wall0
    for resp in gv.WallLongModeResponse:
        b = gv.two_barrier_global_linear_bias(
            collapse_threshold=DELTA_C_EDS, void_threshold=DELTA_V_SHELL,
            void_to_wall_density_ratio=X_SHELL, wall_response=resp)
        g_m3 = b["bias"] * d_wall0
        p_eq = (g_m3 - growth.wall_share_growth) / (growth.void_share_growth
                                                     - growth.wall_share_growth)
        out[resp.value] = {**b, "global_growth_today": g_m3,
                           "equivalent_tracker_share": p_eq,
                           "linear_sigma_direct_A_s": g_m3 * radius_record.unit_growth_sigma}
    # Finite-difference check of the bias against the exact M3 budget.
    h = 1e-6
    m0 = gv.two_barrier_void_mass_fraction(collapse_threshold=DELTA_C_EDS,
                                           void_threshold=DELTA_V_SHELL, long_mode_contrast=0.0)

    def contrast(dl, w):
        m = gv.two_barrier_void_mass_fraction(collapse_threshold=DELTA_C_EDS,
                                              void_threshold=DELTA_V_SHELL, long_mode_contrast=dl)
        z0 = 1.0 - m0 + m0 / X_SHELL
        zl = 1.0 - m + m / X_SHELL
        return (1.0 + w * dl) * z0 / zl - 1.0

    for resp, w in ((gv.WallLongModeResponse.COMPRESSED_WITH_LONG_MODE, 1.0),
                    (gv.WallLongModeResponse.UNIVERSAL_WALL_DENSITY, 0.0)):
        fd = (contrast(h, w) - contrast(-h, w)) / (2.0 * h)
        out[resp.value]["finite_difference_bias"] = fd
    out["note"] = ("1G-F's M3 budget: void volume fraction 0.751969 (not the tracker's f_v0), "
                   "finite-density voids x = 0.2047; a different conditional model, compared "
                   "by its equivalent tracker share only")
    return out


# --------------------------------------------- Gaussian-threshold constructive pair
def _xi_table(k, lnk, d2, r, w1=None, w2=None):
    weight = np.ones_like(k) if w1 is None else w1 * (np.ones_like(k) if w2 is None else w2)
    out = np.empty_like(r)
    for i, ri in enumerate(r):
        out[i] = simpson(d2 * weight * spherical_jn(0, k * ri), x=lnk)
    return out


def gt_pair(bg_in, growth, density, R: float, target_sigma_part: float,
            anchor: float) -> dict:
    """Two admissible joint laws with equal acquired constraints (H21).

    Partition: voids = {g < c}, Phi(c) = f_v0, g the wall field smoothed with a
    Gaussian of width ell (calibrated so the partition rms in the ball equals
    the 1G-E/F reference value).  Wall field: the 1G-E/F wall-internal linear
    field (growth D_wall(t0), photon-frame compression s = D_wall, Planck
    anchored).  Law I: g independent of the wall field; law II: g is the
    smoothed wall field itself.  Both have the same f_v0, the same partition
    covariance and the same wall-field covariance, and both are normalised
    conditionally (E[chi_w delta_w] = 0).
    """
    f_v0 = growth.fv0
    f_w = 1.0 - f_v0
    d_wall0 = growth.wall_share_growth * (1.0 - growth.f_v_ls) / f_w
    s = d_wall0
    lnk = np.linspace(math.log(1e-5), math.log(80.0), 6001)
    k = np.exp(lnk)
    spec = early_spectrum()
    d2 = np.asarray(ls.matter_era_linear_amplitude(
        k_per_Mpc=k * s, early_spectrum=spec, omega_m=density.omega_m_per_photon,
        growth_today_photon_normalised=d_wall0)) * anchor ** 2
    u = np.linspace(0.0, 2.0 * R, 481)[1:]
    pair = (3.0 * u ** 2 / R ** 3) * (1.0 - 3.0 * u / (4.0 * R) + u ** 3 / (16.0 * R ** 3))
    pair_norm = float(simpson(pair, x=u))
    xi_w = _xi_table(k, lnk, d2, u)
    xi_w0 = float(simpson(d2, x=lnk))
    c = float(ndtri(f_v0))           # voids g < c

    def tables(ell):
        gauss = np.exp(-0.5 * (k * ell) ** 2)
        var_l = float(simpson(d2 * gauss ** 2, x=lnk))
        rho_g = _xi_table(k, lnk, d2, u, gauss, gauss) / var_l
        cross0 = float(simpson(d2 * gauss, x=lnk)) / math.sqrt(var_l)
        cross = _xi_table(k, lnk, d2, u, gauss) / math.sqrt(var_l)
        return rho_g, cross0, cross

    def partition_sigma(ell):
        rho_g, _, _ = tables(ell)
        p11 = np.array([gv.bivariate_normal_orthant_moments(
            correlation=min(rg, 1.0 - 1e-12), threshold=c, nodes=200)["P11"] for rg in rho_g])
        return math.sqrt(float(simpson(pair * (p11 - f_w ** 2), x=u)) / f_w ** 2)

    ell = brentq(lambda e: partition_sigma(e) - target_sigma_part, 0.02, 20.0, xtol=1e-8)
    rho_g, cross0, cross = tables(ell)
    mu = cross0 * math.exp(-0.5 * c * c) / math.sqrt(2.0 * math.pi) / f_w   # E[w | g > c]
    laws = {}
    for law, correlated in (("I_independent", False), ("II_same_field", True)):
        c_chi, k_ww, k_xw = [], [], []
        for i in range(len(u)):
            mom = gv.bivariate_normal_orthant_moments(
                correlation=min(rho_g[i], 1.0 - 1e-12), threshold=c, nodes=200)
            p11 = mom["P11"]
            if correlated:
                cgg = np.array([[1.0, rho_g[i]], [rho_g[i], 1.0]])
                cwg = np.array([[cross0, cross[i]], [cross[i], cross0]])
                B = cwg @ np.linalg.inv(cgg)
                mg = np.array([[mom["E_g1g1"], mom["E_g1g2"]], [mom["E_g1g2"], mom["E_g1g1"]]])
                m1 = np.array([mom["E_g1"], mom["E_g2"]])
                e_bb = float((B @ mg @ B.T)[0, 1])
                e_b1, e_b2 = (B @ m1)
                cee = xi_w[i] - float((B @ cwg.T)[0, 1])
                e11ww = e_bb + p11 * cee
                kww = e11ww - mu * (e_b1 + e_b2) + mu * mu * p11
                kxw = e_b2 - mu * p11
            else:
                kww = p11 * xi_w[i]
                kxw = 0.0
            c_chi.append(p11 - f_w ** 2)
            k_ww.append(kww)
            k_xw.append(kxw)
        c_chi, k_ww, k_xw = map(np.asarray, (c_chi, k_ww, k_xw))
        var_part = float(simpson(pair * c_chi, x=u))
        wall = float(simpson(pair * k_ww, x=u))
        cross_pw = float(simpson(pair * k_xw, x=u))
        moments = gv.TwoPhaseSmoothedMoments(
            var_partition=var_part, wall_field=wall, void_field=0.0,
            partition_wall=cross_pw, partition_void=0.0, wall_void=0.0,
            provenance=f"Gaussian-threshold law {law}; empty voids (no void field)")
        var = gv.two_phase_global_variance(void_volume_fraction=f_v0,
                                           void_to_wall_density_ratio=0.0, moments=moments)
        laws[law] = {"sigma_partition": math.sqrt(var["partition_term"]),
                     "sigma_wall_field": math.sqrt(var["wall_field_term"]),
                     "cross_term": var["cross_terms"], "sigma_total": var["rms"],
                     "cauchy_schwarz": gv.cauchy_schwarz_total_rms_interval(
                         partition_rms=math.sqrt(var["partition_term"]),
                         field_rms=math.sqrt(var["wall_field_term"]))}
    return {"radius_Mpc": R, "pair_density_norm": pair_norm, "threshold_c": c,
            "partition_smoothing_ell_Mpc": ell, "target_sigma_partition": target_sigma_part,
            "wall_field_rms_point": math.sqrt(xi_w0), "wall_growth_D_wall": d_wall0,
            "conditional_wall_mean_mu_law_II": mu, "laws": laws,
            "sigma_ratio_II_over_I": laws["II_same_field"]["sigma_total"]
            / laws["I_independent"]["sigma_total"]}


# -------------------------------------------------------------------- figures
def figures(results: dict) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    FIGURES.mkdir(parents=True, exist_ok=True)
    written = []
    # 1. sigma versus the void share with the admissible interval.
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for name, colour in (("PAPER_REFERENCE", "tab:blue"), ("NW15_CMB_FIT", "tab:orange")):
        case = results["cases"][name]
        conv = case["conventions"]["c_bare_volume_average"]
        su = conv["closures"]["wall_mode_p0"]["unit_growth_sigma"]
        d_w, d_v = case["growth"]["wall_share_growth"], case["growth"]["void_share_growth"]
        p = np.linspace(0.0, 0.3, 301)
        ax.plot(p, (d_w + (d_v - d_w) * p) * su, color=colour, label=f"{name} (H9)")
        iv = conv["intervals"]["W09_10pct_at_100"]
        ax.axhspan(iv["lower"], iv["upper"], color=colour, alpha=0.12,
                   label=f"{name} admissible interval (H15), 10% at 100 h^-1 Mpc")
        prim = conv["closures"]["pbs_tracker_seed_compressed"]
        ax.plot([prim["share_k0"]], [prim["linear_sigma_direct_A_s"]], "o", color=colour,
                label=f"{name} PBS seed, [W09] void radius")
        fmed = conv["closures"]["pbs_tracker_seed_F_median_compressed"]
        ax.plot([fmed["share_k0"]], [fmed["linear_sigma_direct_A_s"]], "s", color=colour,
                label=f"{name} PBS seed, 1G-F median radius")
    ax.set_xlabel("void share p (k -> 0)")
    ax.set_ylabel("global-mean linear rms at 8 / h_bare Mpc (c)")
    ax.set_title("Conditional global linear statistic vs the void-share closure")
    ax.legend(fontsize=6.5)
    fig.tight_layout()
    path = FIGURES / "sigma_vs_void_share.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    written.append(str(path.relative_to(ROOT)))
    # 2. Radius scan.
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for name, colour in (("PAPER_REFERENCE", "tab:blue"), ("NW15_CMB_FIT", "tab:orange")):
        scan = results["cases"][name]["conventions"]["c_bare_volume_average"]["radius_scan"]
        L = [row["length_h_inverse_Mpc"] for row in scan]
        ax.plot(L, [row["pbs_tracker_seed_compressed"] for row in scan], "-", color=colour,
                label=f"{name} PBS tracker seed")
        ax.plot(L, [row["monotone_lower_p_fvLS"] for row in scan], "--", color=colour,
                label=f"{name} monotone lower")
    ax.set_xlabel("L (h_bare^-1 Mpc, convention c)")
    ax.set_ylabel("global-mean linear rms")
    ax.legend(fontsize=8)
    fig.tight_layout()
    path = FIGURES / "radius_scan.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    written.append(str(path.relative_to(ROOT)))
    # 3. Propagator scale dependence for the seeds.
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for name, colour in (("PAPER_REFERENCE", "tab:blue"), ("NW15_CMB_FIT", "tab:orange")):
        prop = results["cases"][name]["propagator_k_dependence"]
        k = np.asarray(prop["k_per_Mpc"])
        for key, style in (("pbs_tracker_seed_compressed", "-"), ("pbs_svdw04_seed_compressed", ":")):
            ax.semilogx(k, np.asarray(prop[key]) / prop[key][0], style, color=colour,
                        label=f"{name} {key}")
    ax.axvspan(0.05, 0.4, color="grey", alpha=0.12, label="bulk of the R8 top-hat weight")
    ax.set_xlabel("k (Mpc^-1, photon-normalised comoving)")
    ax.set_ylabel("G(k)/G(k->0)")
    ax.legend(fontsize=7)
    fig.tight_layout()
    path = FIGURES / "propagator_scale_dependence.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    written.append(str(path.relative_to(ROOT)))
    return written


# ------------------------------------------------------------------------ main
def environment() -> dict:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                          text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", "src", "scripts", "tests"],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return {"python": sys.version.split()[0], "implementation": platform.python_implementation(),
            "platform": platform.platform(), "numpy": version("numpy"),
            "scipy": version("scipy"), "matplotlib": version("matplotlib"),
            "git_head": head, "src_scripts_tests_dirty": bool(dirty)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--no-figures", action="store_true", help="skip the figures")
    args = parser.parse_args(argv)
    failures: list[str] = []
    gates_seen: dict[str, dict] = {}

    def gate(name: str, value: float, limit: float, *, kind: str) -> None:
        ok = bool(value <= limit)
        gates_seen.setdefault(kind, {})[name] = {"value": value, "limit": limit, "pass": ok}
        if not ok:
            failures.append(f"{kind}: {name} = {value:.3e} > {limit:.3e}")

    anchor = anchor_factor()
    g_lcdm = float(qplus(0.0, PLANCK_2018_QPLUS_RECIPE))
    spec = early_spectrum()
    e_owner = json.loads(E_OWNER_INVENTORY.read_text(encoding="utf-8"))
    results: dict = {"phase": gv.PHASE, "module_status": gv.MODULE_STATUS,
                     "classification": gv.SCIENTIFIC_CLASSIFICATION,
                     "observational": gv.OBSERVATIONAL_STATUS,
                     "amplitude_identity": gv.AMPLITUDE_STATUS,
                     "status_tokens_read": {
                         k: scientific_status.CURRENT_SCIENTIFIC_STATUS[k]
                         for k in ("LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC", "VOID_ONSET_RESPONSE",
                                   "SIGMA8_AUTHORIZATION", "FSIGMA8_AUTHORIZATION",
                                   "RSD_AUTHORIZATION", "OBSERVATIONAL_AUTHORIZATION",
                                   "UNIQUE_TIMESCAPE_PREDICTION")},
                     "anchoring": anchor, "g_lcdm_qplus0": g_lcdm,
                     "matching": MATCHING.to_metadata(), "cases": {}}
    printed_d = {"PAPER_REFERENCE": (1169, 1.263), "NW15_CMB_FIT": (1185, 1.285)}
    for name, bg_in in backgrounds().items():
        growth = gv.two_phase_global_growth(background=bg_in, matching=MATCHING, checks=CHECKS, G=G)
        density = ls.early_matter_density_per_photon(background=bg_in,
                                                     identity_tolerance=IDENTITY_RTOL, G=G)
        seeds = seed_radii(bg_in, growth)
        clos = closures(growth, seeds)
        case = {"growth": growth.to_json_dict(),
                "omega_m_per_photon": density.omega_m_per_photon,
                "h_dressed": density.h_dressed, "h_bare": density.h_bare,
                "seed_radii_Mpc": {k: {"R_s_Mpc": v[0], "provenance": v[1]}
                                   for k, v in seeds.items()},
                "conventions": {}}
        for conv in CONVENTIONS:
            radius = radius_spec(conv, 8.0)
            rows = {}
            records = {}
            for cname, clo in clos.items():
                r = run_case(bg_in, clo, spec, radius)
                records[cname] = r
                rows[cname] = summary(r, anchor["factor"], g_lcdm)
            intervals = {}
            for pname, (L_hom, eta) in PREMISES.items():
                prem = gv.HomogeneityPremise(
                    radius=radius_spec(conv, L_hom), max_linear_rms=eta,
                    provenance=f"[W09] ll. 327-335, 455-458 read as rms <= {eta} in the "
                               f"Lagrangian top hat of L = {L_hom:.4g} h^-1 Mpc ({conv})")
                iv = gv.admissible_global_linear_interval(
                    target=records["pbs_tracker_seed_compressed"], premise=prem)
                intervals[pname] = {**iv.to_json_dict(),
                                    "lower_anchored": iv.lower * anchor["factor"],
                                    "upper_anchored": iv.upper * anchor["factor"]}
            scan = []
            for L in RADIUS_SCAN_H_MPC:
                rr = radius_spec(conv, L)
                row = {"length_h_inverse_Mpc": L}
                for cname in ("monotone_lower_p_fvLS", "pbs_tracker_seed_compressed",
                              "pbs_svdw04_seed_compressed"):
                    row[cname] = run_case(bg_in, clos[cname], spec, rr).linear_sigma
                row["radius_Mpc"] = resolve_radius(rr, density)
                scan.append(row)
            case["conventions"][conv] = {"closures": rows, "intervals": intervals,
                                         "radius_scan": scan}
            if conv == "c_bare_volume_average":
                primary_record = records["pbs_tracker_seed_compressed"]
                refined = run_case(bg_in, clos["pbs_tracker_seed_compressed"], spec, radius,
                                   quadrature=REFINED_QUAD)
                gate(f"{name} refined quadrature", abs(refined.linear_sigma
                                                       / primary_record.linear_sigma - 1.0),
                     GATES["refined_quadrature_rel"], kind="numerics")
                case["refined_quadrature_linear_sigma"] = refined.linear_sigma
                case["m3_two_barrier_alternative"] = m3_alternative(growth, density, spec,
                                                                    primary_record)
                case["a_s_scaling"] = a_s_scaling(bg_in, clos, radius)
                k_tab = np.geomspace(1e-4, 10.0, 121)
                prop = {"k_per_Mpc": k_tab.tolist()}
                for cname in ("pbs_tracker_seed_compressed", "pbs_svdw04_seed_compressed",
                              "pbs_tracker_seed_F_median_compressed"):
                    prop[cname] = np.asarray(gv.global_linear_propagator(
                        growth=primary_record.growth if cname == "pbs_tracker_seed_compressed"
                        else records[cname].growth,
                        void_share=records[cname].void_share, k_per_Mpc=k_tab)).tolist()
                case["propagator_k_dependence"] = prop
                # Seed-radius sensitivity (PBS, compressed).
                sens = {}
                for sname, (rs, prov) in seeds.items():
                    clo = gv.GaussianThresholdSeedVoidShare(
                        seed_radius_Mpc=rs, seed_radius_provenance=prov,
                        compression=gv.SeedVolumeCompression.COMPRESSED_WITH_REGION)
                    try:
                        rr = run_case(bg_in, clo, spec, radius)
                        sens[sname] = {"R_s_Mpc": rs, **summary(rr, anchor["factor"], g_lcdm)}
                    except gv.GlobalVarianceContractError as exc:
                        sens[sname] = {"R_s_Mpc": rs, "refused": str(exc)}
                case["seed_radius_sensitivity"] = sens
                case["flat_wall_capacity"] = flat_wall_capacity_radius(bg_in, growth, density, spec)
        # Reproduction of the 1G-D owner-decision numbers (threshold-only S2).
        d_row = case["conventions"]["a_equal_mass"]["closures"]["pbs_tracker_seed_threshold_only_1G_D"]
        gate(f"{name} A_v vs 1G-D printed", abs(d_row["void_onset_response_A_v"]
                                                 - printed_d[name][0]),
             GATES["D_owner_A_v_printed_digits"], kind="reproduction")
        gate(f"{name} X_SU vs 1G-D printed", abs(d_row["growth_ratio_to_lcdm_X"]
                                                  - printed_d[name][1]),
             GATES["D_owner_X_SU_printed_digits"], kind="reproduction")
        # A_s scaling gates.
        for factor_key, row in case["a_s_scaling"]["monotone_lower_p_fvLS"].items():
            gate(f"{name} constant share A_s scaling {factor_key}",
                 abs(row["linear_sigma_ratio"] / row["sqrt_A_s_ratio"] - 1.0),
                 GATES["constant_share_A_s_scaling_rel"], kind="physics")
        for factor_key, row in case["a_s_scaling"]["pbs_tracker_seed_compressed"].items():
            gate(f"{name} PBS void term A_s independence {factor_key}",
                 abs(row["void_share_rms_ratio"] - 1.0),
                 GATES["pbs_void_term_A_s_independence_rel"], kind="physics")
        for resp in gv.WallLongModeResponse:
            row = case["m3_two_barrier_alternative"][resp.value]
            gate(f"{name} M3 bias finite difference {resp.value}",
                 abs(row["finite_difference_bias"] / row["bias"] - 1.0),
                 GATES["m3_bias_finite_difference_rel"], kind="physics")
        results["cases"][name] = case

    # Two-phase covariance: 1G-E/F reference reproduction, bounds, GT pair.
    ref_keys = {"PAPER_REFERENCE": "GE_reference_population_1G_F|PAPER_REFERENCE|b_dressed_8_over_h|",
                "NW15_CMB_FIT": "GE_reference_population_1G_F|NW15_CMB_FIT|b_dressed_8_over_h|"}
    cov = {}
    for name, bg_in in backgrounds().items():
        quoted = e_owner["numbers_from_artifact"]
        sp = float(quoted[ref_keys[name] + "sigma_part"])
        si = float(quoted[ref_keys[name] + "sigma_int_photon_frame_D_wall"])
        stot = float(quoted[ref_keys[name] + "sigma_photon_frame_D_wall_empty_voids"])
        fv0 = bg_in.fv0
        f_w = 1.0 - fv0
        e3 = gv.TwoPhaseSmoothedMoments(
            var_partition=(sp * f_w) ** 2, wall_field=(si * f_w) ** 2, void_field=0.0,
            partition_wall=0.0, partition_void=0.0, wall_void=0.0,
            provenance="1G-E/F reference population at convention (b): E3 independence, "
                       "empty voids")
        var = gv.two_phase_global_variance(void_volume_fraction=fv0,
                                           void_to_wall_density_ratio=0.0, moments=e3)
        gate(f"{name} E reference reproduction", abs(var["rms"] - stot),
             GATES["E_reference_reproduction_abs"], kind="reproduction")
        growth = gv.two_phase_global_growth(background=bg_in, matching=MATCHING, checks=CHECKS, G=G)
        density = ls.early_matter_density_per_photon(background=bg_in,
                                                     identity_tolerance=IDENTITY_RTOL, G=G)
        R_b = resolve_radius(radius_spec("b_dressed_wall_comoving", 8.0), density)
        gtp = gt_pair(bg_in, growth, density, R_b, sp, anchor["factor"])
        # Finite-density weights at the shell-crossing ratio (H17).
        weights = gv.two_phase_global_variance(
            void_volume_fraction=fv0, void_to_wall_density_ratio=X_SHELL,
            moments=gv.TwoPhaseSmoothedMoments(var_partition=0.0, wall_field=0.0, void_field=0.0,
                                               partition_wall=0.0, partition_void=0.0,
                                               wall_void=0.0, provenance="weights only"))
        cov[name] = {"E_reference": {"sigma_part": sp, "sigma_int": si, "sigma_printed": stot,
                                     "reproduced": var["rms"]},
                     "cauchy_schwarz_on_E_reference": gv.cauchy_schwarz_total_rms_interval(
                         partition_rms=sp, field_rms=si),
                     "gaussian_threshold_pair": gtp,
                     "finite_density_weights_x_shell": {
                         k: weights[k] for k in ("partition_weight", "wall_weight", "void_weight",
                                                 "void_contrast_global")}}
    # Orthant-moment gate against the bivariate normal CDF.
    from scipy.stats import multivariate_normal
    worst = 0.0
    for rho in (-0.6, 0.0, 0.3, 0.9, 0.999):
        for cthr in (-1.0, 0.0, 0.634, 2.0):
            mom = gv.bivariate_normal_orthant_moments(correlation=rho, threshold=cthr, nodes=400)
            exact = float(multivariate_normal(mean=[0.0, 0.0], cov=[[1.0, rho], [rho, 1.0]]).cdf(
                [-cthr, -cthr]))
            worst = max(worst, abs(mom["P11"] - exact))
    gate("orthant P11 vs bivariate CDF", worst, GATES["gt_orthant_P11_vs_bivariate_cdf_abs"],
         kind="numerics")
    results["two_phase_covariance"] = cov
    results["gates"] = gates_seen
    results["gate_definitions"] = GATES
    results["environment"] = environment()
    if not args.no_figures:
        results["figures"] = figures(results)
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(results, indent=2, sort_keys=True, default=_json_default) + "\n"
    ARTIFACT.write_bytes(payload.encode("utf-8"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    _print_summary(results, digest)
    if failures:
        print("GATE FAILURES:")
        for f in failures:
            print("  " + f)
        return 1
    print(f"all {sum(len(v) for v in gates_seen.values())} gates pass")
    return 0


def resolve_radius(spec: ls.LagrangianRadiusSpec, density) -> float:
    return ls.resolve_lagrangian_radius(spec=spec, density=density).radius_Mpc


def _json_default(obj):
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    raise TypeError(f"not JSON serialisable: {type(obj)}")


def _print_summary(results: dict, digest: str) -> None:
    print(f"wrote {ARTIFACT.relative_to(ROOT)} (sha256 {digest[:16]}...)")
    print(f"anchor factor (Boltzmann/EH98 at Planck) = {results['anchoring']['factor']:.6f}")
    for name, case in results["cases"].items():
        g = case["growth"]
        print(f"\n{name}: D_W = {g['wall_share_growth']:.6f}  D_V = {g['void_share_growth']:.6f}  "
              f"f_v,LS = {g['f_v_ls']:.6e}")
        for conv, block in case["conventions"].items():
            print(f"  [{conv}]  R = {block['closures']['wall_mode_p0']['radius_Mpc']:.4f} Mpc, "
                  f"sigma_u = {block['closures']['wall_mode_p0']['unit_growth_sigma']:.5f}")
            for cname, row in block["closures"].items():
                print(f"    {cname:42s} p0 = {row['share_k0']:.5f}  G0 = {row['propagator_k0']:.5f}"
                      f"  sigma = {row['linear_sigma_direct_A_s']:.4f} "
                      f"(anchored {row['linear_sigma_planck_anchored']:.4f})  "
                      f"eps_rms = {row['void_volume_response_rms']:.3f}")
            for pname, iv in block["intervals"].items():
                print(f"    interval {pname:30s} [{iv['lower']:.4f}, {iv['upper']:.4f}] "
                      f"p <= {iv['share_upper']:.4f}; primary inside: {iv['target_inside']}; "
                      f"primary rms at premise = {iv['target_premise_rms']:.4f}")
        m3 = case["m3_two_barrier_alternative"]
        for resp in ("compressed_with_long_mode", "universal_wall_density"):
            print(f"  M3 {resp}: b = {m3[resp]['bias']:.5f}, G = {m3[resp]['global_growth_today']:.5f},"
                  f" p_eq = {m3[resp]['equivalent_tracker_share']:.5f}")
        print(f"  flat-wall capacity radius: {case['flat_wall_capacity']['radius_Mpc']:.2f} Mpc")
    for name, cov in results["two_phase_covariance"].items():
        gtp = cov["gaussian_threshold_pair"]
        print(f"\n{name} GT pair at R = {gtp['radius_Mpc']:.4f} Mpc, ell = "
              f"{gtp['partition_smoothing_ell_Mpc']:.4f} Mpc:")
        for law, row in gtp["laws"].items():
            print(f"  {law:15s} sigma_part = {row['sigma_partition']:.4f}  sigma_wall = "
                  f"{row['sigma_wall_field']:.4f}  cross = {row['cross_term']:+.4f}  total = "
                  f"{row['sigma_total']:.4f}")


if __name__ == "__main__":
    raise SystemExit(main())
