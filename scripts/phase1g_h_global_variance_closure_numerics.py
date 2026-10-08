"""Phase 1G-H evidence: conditional global-mean linear matter variance.

Report: ``reports/phase1g_h_global_variance_closure.md`` ([1G-H]); equations
(H1)-(H25) there.  Runtime: ``timescape_fsigma8.global_variance`` (experimental,
conditional).  Writes the git-ignored
``artifacts/independent/phase1g_h_global_variance_closure.json`` and figures
under ``artifacts/independent/phase1g_h/``; prints a summary and exits
nonzero if a declared gate fails.

Scenarios (declared, never combined): [GM] PAPER_REFERENCE (f_v0 = 0.737,
H0 = 73.03) and the [NW15] Timescape CMB fit (f_v0 = 0.627, H0 = 61.0, as in
1G-A/B/D).  Early universe: Planck 2018 A_s, n_s, k_p and baryon fraction
(script-level explicit inputs, PROVISIONAL_MODEL_IMPORT; [NW15] l. 1422 leave
A_s unconstrained), the EH98 zero-baryon-oscillation (no-wiggle) transfer
with the baryon shape suppression, Eqs. (26), (28)-(31), at the per-photon
omega_m,eff (``lagrangian_sigma``).  Matching epoch z = 1090 (1G-D, 1G-F).
Every number is CONDITIONAL, MODEL-INTERNAL and NON_OBSERVATIONAL; none is an
observational amplitude.

Audit remediation (2026-10-07; reports/phase1g_h_audit_remediation.md): the
statistic is the formal tangent statistic (owner decision D1) with
seed-indexed void accounting (D2); the evidence adds the GH-F1 two-state
example, the scale-separation ratios (GH-F2), a step-kernel counterexample
to an unrestricted (H15) (GH-F4), the negative-density probabilities of the
signed Gaussian pair and a nonnegative lognormal pair (GH-F5, D3), the PBS
reclosure under a rescaled input spectrum (GH-F6, D4), the Gaussian fraction
above the flat-wall cap (GH-F7), orthant analytic cases (GH-F10) and the
rounding-budget gate of the 1G-E/F reference (GH-F11).

Delta-audit remediation (2026-10-08; reports/phase1g_h_delta_audit_remediation.md):
the lognormal pairs share f_v0, P11(r) and the latent carrier law, not the
conditionally normalised wall-density covariance, whose law-II normaliser
ratio m_II is reported (GH-DF1); identity (H25) gives the total from P11(r)
and the both-walls conditional covariance C_W(r); the ball pair integrals
include the first radial panel and carry a refinement gate; the rounding
budget of the 1G-E/F reference is a function the tests exercise (GH-DF5).
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
from scipy.special import ndtr, ndtri, spherical_jn

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
    "suppression ([1G-A] Sec. 6.3); owner decision D4 (2026-10-07): the factor is an "
    "empirical post-hoc output normalisation at fixed closure, reported beside the "
    "direct values (primary) and the reclosure variant")
# Orthant integrals: absolute accuracy target of the refined quadrature (audit
# GH-F10).  The moments are O(1); 1e-12 is far below every printed digit and
# the Monte Carlo checks, and above the double-precision floor of the sums.
ORTHANT_TOLERANCE = 1e-12
ORTHANT_START_NODES = 32
# Ball pair integrals of the constructive pairs: uniform Simpson grid on
# [0, 2R] with this many intervals (even), including the first panel; every
# other node gives the half-resolution estimate of the refinement gate.  At
# R = 11-13 Mpc the spacing is 0.015-0.018 Mpc, against the mask smoothing
# ell = 0.29-0.60 Mpc.
RADIAL_INTERVALS = 1440

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
    # sqrt(sp^2 + si^2) vs the printed total: half a unit of the fourth decimal,
    # propagated exactly through the formula per scenario (GH-F11); the gate
    # limit is (sp/s + si/s + 1) times this half unit.
    "E_reference_printed_half_unit": 5e-5,
    "gt_orthant_P11_vs_bivariate_cdf_abs": 1e-10,
    "orthant_analytic_cases_abs": 1e-12,         # rho = 0, c = 0 and c = -100 (GH-F10)
    "m3_bias_finite_difference_rel": 1e-6,
    "lognormal_ball_variance_calibration_rel": 1e-9,
    # lam -> 0 limit of the lognormal pair vs the signed pair: O(lam sigma_w)
    # tilt corrections (~1e-2 at latent variance 1e-4) and the cancellation of
    # O(f_w^2) terms at orthant accuracy 1e-12 in O(lam^2) moments.
    "lognormal_linear_limit_rel": 5e-2,
    "step_kernel_premise_ratio": 1.0,            # sigma(R_hom)/eta <= 1 (GH-F4)
    "reclosure_constant_share_rel": 1e-10,       # constant share: reclosure = post-hoc
    # Declared 2026-10-08 before their first evaluation (delta audit).  Radial
    # refinement: every rms of the constructive pairs on RADIAL_INTERVALS vs
    # half of them; 1e-5 protects the printed fourth decimal by a factor 5.
    "radial_refinement_rel": 1e-5,
    # (H25) against the (H17)-(H19) assembly: an algebraic identity of the same
    # quadrature sums (round-off only).
    "h25_identity_rel": 1e-12,
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


def e_reference_rounding_budget(*, sigma_partition: float, sigma_internal: float,
                                sigma_total: float, half_unit: float) -> float:
    """Rounding budget of the 1G-E/F reference reproduction (audit GH-F11).

    The components sigma_part and sigma_int and the printed total are known to
    four decimals (half a unit ``half_unit``).  First-order propagation of the
    input rounding through ``sigma = sqrt(sp^2 + si^2)`` gives
    ``half (sp + si)/sigma``; the printed total adds its own half unit, hence
    ``half (sp/sigma + si/sigma + 1)`` (the output term is exercised by a test,
    delta audit GH-DF5).
    """
    return half_unit * (sigma_partition / sigma_total + sigma_internal / sigma_total + 1.0)


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
            "meaning": "empirical post-hoc output normalisation at fixed closure (owner "
                       "decision D4): multiplies a finished direct value by the ratio of "
                       "the Planck sigma at 8 Mpc/h to the EH98 value at the Planck "
                       "parameters.  It is not a verified transfer recalibration: a "
                       "rescaled input spectrum changes the PBS share (see "
                       "pbs_reclosure_under_spectrum_rescaling), and the late-time growth "
                       "cancels only for a common scale-independent growth"}


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


def _orthant(rho: float, c: float) -> dict:
    return gv.bivariate_normal_orthant_moments(
        correlation=min(rho, 1.0 - 1e-12), threshold=c, nodes=ORTHANT_START_NODES,
        tolerance=ORTHANT_TOLERANCE)


def _orthant_p(rho: float, c1: float, c2: float) -> float:
    return gv.bivariate_normal_orthant_probability(
        correlation=min(rho, 1.0 - 1e-12), threshold_1=c1, threshold_2=c2,
        nodes=ORTHANT_START_NODES, tolerance=ORTHANT_TOLERANCE)


# Nonnegative lognormal pairs (owner decision D3 on GH-F5): resolution radii of
# the latent Gaussian smoothing (declared construction parameters, not physics)
# and the latent point variance of the linear-limit check.
LOGNORMAL_RESOLUTIONS_MPC = (1.0, 2.0, 4.0)
LOGNORMAL_LINEAR_LIMIT_LATENT_VARIANCE = 1e-4


class _Ball:
    """Ball pair-density integrals on [0, 2R] with a half-resolution companion.

    Uniform Simpson grid of ``RADIAL_INTERVALS`` intervals that includes the
    first panel at u = 0 (delta audit 2026-10-08: the earlier grid started at
    2R/480 and dropped it).  The pair density of two points in a ball vanishes
    as u^2 at u = 0 and every kernel is bounded there, so the u = 0 integrand
    is exactly 0; kernels are evaluated for u > 0 only (zero separation means
    unit mask correlation, outside the orthant functions' |rho| < 1).  The
    same kernel values on every other node give the half-resolution estimate
    for the radial refinement gate.
    """

    def __init__(self, R: float):
        self.R = R
        self.u_full = np.linspace(0.0, 2.0 * R, RADIAL_INTERVALS + 1)
        self.u = self.u_full[1:]
        u = self.u
        self.pair = (3.0 * u ** 2 / R ** 3) * (1.0 - 3.0 * u / (4.0 * R) + u ** 3 / (16.0 * R ** 3))

    def integral(self, values, coarse: bool = False) -> float:
        y = np.concatenate(([0.0], self.pair * np.asarray(values, dtype=float)))
        if coarse:
            return float(simpson(y[::2], x=self.u_full[::2]))
        return float(simpson(y, x=self.u_full))


def _law_summary(f_v0: float, ball: _Ball, c_chi, k_ww, k_pw, provenance: str) -> dict:
    """One two-phase law from its separation kernels, (H17)-(H19) and (H25).

    ``c_chi = P11 - f_w^2``, ``k_ww = E[chi1 chi2 (psi1 - 1)(psi2 - 1)]`` and
    ``k_pw = Cov(chi1, chi2 (psi2 - 1))`` for empty voids and a wall density
    ``psi`` normalised by ``E[psi | wall] = 1``.  (H25): the ball variance is
    ``< P11(r) C_W(r)/f_w^2 - 1 >`` with ``C_W = E[psi1 psi2 | both in walls]
    = 1 + (k_ww + 2 k_pw)/P11``, so P11 and C_W fix the total.  Reports the
    pair-weighted both-walls conditional covariance ``<P11 (C_W - 1)>/<P11>``
    and the relative change of every rms under radial refinement.
    """
    f_w = 1.0 - f_v0
    c_chi, k_ww, k_pw = (np.asarray(a, dtype=float) for a in (c_chi, k_ww, k_pw))
    levels = {}
    for coarse in (False, True):
        moments = gv.TwoPhaseSmoothedMoments(
            var_partition=ball.integral(c_chi, coarse), wall_field=ball.integral(k_ww, coarse),
            void_field=0.0, partition_wall=ball.integral(k_pw, coarse), partition_void=0.0,
            wall_void=0.0, provenance=provenance)
        var = gv.two_phase_global_variance(void_volume_fraction=f_v0,
                                           void_to_wall_density_ratio=0.0, moments=moments)
        levels[coarse] = (moments, var, {
            "sigma_partition": math.sqrt(var["partition_term"]),
            "sigma_wall_field": math.sqrt(var["wall_field_term"]), "sigma_total": var["rms"]})
    moments, var, sig = levels[False]
    sig_coarse = levels[True][2]
    refinement = max(abs(sig[key] / sig_coarse[key] - 1.0) for key in sig if sig_coarse[key] > 0.0)
    p11 = c_chi + f_w ** 2
    return {**sig, "cross_term": var["cross_terms"],
            "wall_moment": moments.wall_field, "partition_wall_moment": moments.partition_wall,
            "sigma_total_from_H25": math.sqrt(ball.integral(c_chi + k_ww + 2.0 * k_pw) / f_w ** 2),
            "both_walls_conditional_density_covariance_ball":
                ball.integral(k_ww + 2.0 * k_pw) / ball.integral(p11),
            "radial_refinement_rel": refinement}


def lognormal_mask_kernels(*, rho: float, c: float, f_w: float, lam: float, xi_lat_r: float,
                           kappa0: float, kappa_r: float) -> tuple[float, float, float]:
    """(P11, K_ww, K_pw) at one separation for the lognormal wall density (GH-F5).

    chi = 1{g > c}; psi = exp(a)/E[exp(a) | wall] with a = lam s; rho the mask
    correlation, xi_lat_r the latent carrier covariance, kappa0 = Cov(g, a) at
    one point and kappa_r = Cov(g(x), a(y)) (0 for an independent mask).
    ``K_ww = E[chi1 chi2 (psi1 - 1)(psi2 - 1)]``,
    ``K_pw = Cov(chi1, chi2 (psi2 - 1))``; exponential tilting of
    (g1, g2, a1, a2) gives the closed forms of ``_lognormal_laws``.
    """
    q0 = float(ndtr(-(c - kappa0)))
    p11 = _orthant(rho, c)["P11"]
    m = kappa0 + kappa_r
    e_pp = math.exp(lam * lam * xi_lat_r) * f_w ** 2 * _orthant_p(rho, c - m, c - m) / q0 ** 2
    e_p = f_w * _orthant_p(rho, c - kappa_r, c - kappa0) / q0
    return p11, e_pp - 2.0 * e_p + p11, e_p - p11


def _lognormal_laws(f_v0: float, c: float, ball: _Ball, rho_g, lam: float, xi_lat,
                    cross0_lat: float, cross_lat) -> dict:
    """Laws I and II for the wall density proportional to exp(lam s(x)), [1G-H] Sec. 6.3.

    s is the latent Gaussian carrier (covariance ``xi_lat``); the walls are
    {g > c}, g a unit Gaussian mask field with correlation ``rho_g`` that is
    independent of s (law I) or has ``Cov(g(x), s(y)) = cross_lat(r)`` (law II).
    With ``psi = exp(a)/E[exp(a) | wall]`` (nonnegative, conditionally
    normalised), a = lam s, kappa(r) = lam cross_lat(r), m = kappa0 + kappa(r)
    and Q0 = P(Z > c - kappa0), exponential tilting of (g1, g2, a1, a2) gives
    ``E[chi1 chi2 psi1 psi2] = exp(lam^2 xi_lat) f_w^2 P(Z1 > c-m, Z2 > c-m)/Q0^2``
    and ``E[chi1 chi2 psi2] = f_w P(Z1 > c-kappa(r), Z2 > c-kappa0)/Q0``.
    The conditional normaliser of law II exceeds law I's by
    ``m_II = Q0/f_w`` (delta audit GH-DF1), so the unconditional covariance of
    its conditionally normalised density is law I's divided by m_II^2.
    """
    f_w = 1.0 - f_v0
    kappa0, kappa = lam * cross0_lat, lam * np.asarray(cross_lat)
    laws = {}
    for law, correlated in (("I_independent", False), ("II_same_field", True)):
        c_chi, k_ww, k_pw = [], [], []
        for i in range(len(ball.u)):
            p11, kww, kpw = lognormal_mask_kernels(
                rho=float(rho_g[i]), c=c, f_w=f_w, lam=lam, xi_lat_r=float(xi_lat[i]),
                kappa0=kappa0 if correlated else 0.0,
                kappa_r=float(kappa[i]) if correlated else 0.0)
            c_chi.append(p11 - f_w ** 2)
            k_ww.append(kww)
            k_pw.append(kpw)
        laws[law] = _law_summary(f_v0, ball, c_chi, k_ww, k_pw,
                                 f"lognormal threshold law {law}; empty voids")
        laws[law]["conditional_normaliser_ratio_m"] = (
            float(ndtr(-(c - kappa0))) / f_w if correlated else 1.0)
    return laws


def lognormal_pairs(f_v0: float, c: float, ball: _Ball, k, lnk, d2, ell: float, xi_w,
                    rho_g, signed_moments: dict) -> dict:
    """Nonnegative lognormal pairs at a fixed latent carrier law (D3; GH-DF1).

    Latent carrier ``s = w`` smoothed with a Gaussian of radius r_s (the
    resolution of the lognormal transform, a free construction parameter);
    wall density ``psi = exp(lam s)/E[exp(lam s) | wall]``, conditionally
    normalised on the walls, hence nonnegative.  Law II takes the signed
    pair's mask (w smoothed at the calibrated ell); law I an independent mask
    with the same covariance.  Shared by I and II: f_v0, the partition
    covariance P11(r), the latent carrier law (covariance lam^2 xi_s;
    equivalently the unconditionally normalised carrier exp(lam s)/E[exp(lam s)],
    covariance exp(lam^2 xi_s) - 1) and the convention E[psi | wall] = 1.  Not
    shared (delta audit GH-DF1): the conditionally normalised wall density
    itself, whose unconditional covariance in law II is law I's divided by
    m_II^2 (``conditional_normaliser_ratio_m``), and the both-walls
    conditional covariance C_W(r) - 1 that, with P11, fixes the total by
    (H25).  For each r_s, lam (a free calibration choice) makes the ball
    variance of the unconditionally normalised carrier equal to the signed
    carrier's.  The linear-limit member (unsmoothed carrier, latent point
    variance 1e-4) is a local numerical check, at one small amplitude, that
    the signed pair is the lam -> 0 limit: wall moments over lam^2 and
    partition-wall moments over lam approach the signed ones.
    """
    g_ell = np.exp(-0.5 * (k * ell) ** 2)
    var_g = float(simpson(d2 * g_ell ** 2, x=lnk))
    ball_target = ball.integral(xi_w)
    members = {}
    for rs in LOGNORMAL_RESOLUTIONS_MPC:
        g_s = np.exp(-0.5 * (k * rs) ** 2)
        var_s = float(simpson(d2 * g_s ** 2, x=lnk))
        xi_s = _xi_table(k, lnk, d2, ball.u, g_s, g_s)
        cross0 = float(simpson(d2 * g_s * g_ell, x=lnk)) / math.sqrt(var_g)
        cross = _xi_table(k, lnk, d2, ball.u, g_s, g_ell) / math.sqrt(var_g)

        def carrier_ball(lam2: float) -> float:
            return ball.integral(np.expm1(lam2 * xi_s))

        lam2 = brentq(lambda l2: carrier_ball(l2) - ball_target, 1e-8, 50.0, xtol=1e-15,
                      rtol=1e-14)
        laws = _lognormal_laws(f_v0, c, ball, rho_g, math.sqrt(lam2), xi_s, cross0, cross)
        m_ii = laws["II_same_field"]["conditional_normaliser_ratio_m"]
        members[f"r_s_{rs:g}_Mpc"] = {
            "resolution_radius_Mpc": rs, "latent_scale_lambda": math.sqrt(lam2),
            "latent_point_variance": lam2 * var_s,
            "density_point_variance": math.expm1(lam2 * var_s),
            "ball_variance_unconditionally_normalised_carrier": carrier_ball(lam2),
            "calibration_rel": abs(carrier_ball(lam2) / ball_target - 1.0),
            "conditional_normaliser_ratio_m_II": m_ii,
            "conditional_density_covariance_ratio_II_over_I": 1.0 / m_ii ** 2,
            "ball_variance_unmasked_conditional_density_II": carrier_ball(lam2) / m_ii ** 2,
            "unconditional_mean_conditional_contrast_II": 1.0 / m_ii - 1.0,
            "laws": laws,
            "sigma_ratio_II_over_I": laws["II_same_field"]["sigma_total"]
            / laws["I_independent"]["sigma_total"]}
    # Linear limit: unsmoothed carrier, tiny latent variance.
    xi_w0 = float(simpson(d2, x=lnk))
    lam = math.sqrt(LOGNORMAL_LINEAR_LIMIT_LATENT_VARIANCE / xi_w0)
    cross0 = float(simpson(d2 * g_ell, x=lnk)) / math.sqrt(var_g)
    cross = _xi_table(k, lnk, d2, ball.u, g_ell) / math.sqrt(var_g)
    small = _lognormal_laws(f_v0, c, ball, rho_g, lam, xi_w, cross0, cross)
    limit = {}
    for law in ("I_independent", "II_same_field"):
        ref = signed_moments[law]
        limit[law] = {"wall_moment_over_lam2": small[law]["wall_moment"] / lam ** 2,
                      "signed_wall_moment": ref["wall_moment"],
                      "partition_wall_moment_over_lam": small[law]["partition_wall_moment"] / lam,
                      "signed_partition_wall_moment": ref["partition_wall_moment"]}
    rel = max(abs(limit[law]["wall_moment_over_lam2"] / limit[law]["signed_wall_moment"] - 1.0)
              for law in limit)
    return {"pair_class": "NONNEGATIVE_LOGNORMAL_DENSITY_LAWS",
            "negative_wall_density_probability": 0.0,
            "ball_variance_signed_carrier": ball_target,
            "shared_constraints": [
                "f_v0", "partition covariance (identical P11(r))",
                "latent Gaussian carrier law (covariance lam^2 xi_s); equivalently the "
                "unconditionally normalised carrier exp(lam s)/E[exp(lam s)], covariance "
                "exp(lam^2 xi_s) - 1",
                "normalisation convention E[psi | wall] = 1"],
            "not_shared": [
                "the conditionally normalised wall density: its unconditional covariance in "
                "law II is law I's divided by m_II^2 (conditional_normaliser_ratio_m_II)",
                "the both-walls conditional covariance C_W(r) - 1, which with P11 fixes the "
                "total by (H25)"],
            "free_construction_choices": [
                "latent smoothing radius r_s (1, 2, 4 Mpc)",
                "lam calibrated to the ball variance of the signed carrier"],
            "members": members,
            "linear_limit": {"latent_point_variance": LOGNORMAL_LINEAR_LIMIT_LATENT_VARIANCE,
                             "latent_scale_lambda": lam, "laws": limit,
                             "max_wall_moment_rel_difference": rel,
                             "scope": "local numerical check at one small amplitude with an "
                                      "empirical gate; not an asymptotic theorem"}}


def gt_pair(bg_in, growth, density, R: float, target_sigma_part: float,
            anchor: float) -> dict:
    """Two constructive joint-law pairs at fixed partition and carrier laws, [1G-H] Sec. 6.3.

    Partition: voids = {g < c}, Phi(c) = f_v0, g the wall carrier smoothed with
    a Gaussian of width ell (calibrated so the partition rms in the ball
    equals the 1G-E/F reference value).  Carrier: the 1G-E/F wall-internal
    linear field (growth D_wall(t0), photon-frame compression s = D_wall,
    Planck anchored).  Law I: g independent of the carrier; law II: g is the
    smoothed carrier itself.  Both pairs hold f_v0, P11(r) and the carrier law
    fixed; by (H25) they differ through the both-walls conditional density
    covariance C_W(r) - 1, i.e. the joint law of geometry and density.

    * Signed Gaussian pair (owner decision D3 on audit GH-F5): the wall
      density is ``1 + w - mu`` with the conditional recentring mu, a signed
      surrogate; the shared covariance is that of the unconditional carrier,
      and the phase-conditioned (masked) wall covariance differs between I and
      II.  ``negative_wall_density_probability`` gives P(rho < 0 | wall).
    * Nonnegative lognormal pair (D3; GH-DF1): ``lognormal_pairs``.
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
    ball = _Ball(R)
    u = ball.u
    pair_norm = ball.integral(np.ones_like(u))
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
        p11 = np.array([_orthant(rg, c)["P11"] for rg in rho_g])
        return math.sqrt(ball.integral(p11 - f_w ** 2) / f_w ** 2)

    ell = brentq(lambda e: partition_sigma(e) - target_sigma_part, 0.02, 20.0, xtol=1e-8)
    rho_g, cross0, cross = tables(ell)
    mu = cross0 * math.exp(-0.5 * c * c) / math.sqrt(2.0 * math.pi) / f_w   # E[w | g > c]
    laws = {}
    for law, correlated in (("I_independent", False), ("II_same_field", True)):
        c_chi, k_ww, k_xw = [], [], []
        for i in range(len(u)):
            mom = _orthant(rho_g[i], c)
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
        laws[law] = _law_summary(f_v0, ball, c_chi, k_ww, k_xw,
                                 f"Gaussian-threshold law {law}; empty voids (no void field)")
        laws[law]["cauchy_schwarz"] = gv.cauchy_schwarz_total_rms_interval(
            partition_rms=laws[law]["sigma_partition"], field_rms=laws[law]["sigma_wall_field"])
    # P(rho < 0 | wall) of the signed laws (GH-F5): law I, delta_w = w with the
    # mask independent; law II, delta_w = w - mu with corr(w, g) = cross0/sigma_w.
    sigma_w = math.sqrt(xi_w0)
    r_wg = cross0 / sigma_w
    negative = {"I_independent": float(ndtr(-1.0 / sigma_w)),
                "II_same_field": _orthant_p(-r_wg, (1.0 - mu) / sigma_w, c) / f_w}
    lognormal = lognormal_pairs(f_v0, c, ball, k, lnk, d2, ell, xi_w, rho_g, laws)
    refinement = max([law["radial_refinement_rel"] for law in laws.values()]
                     + [law["radial_refinement_rel"] for m in lognormal["members"].values()
                        for law in m["laws"].values()])
    h25 = max([abs(law["sigma_total_from_H25"] / law["sigma_total"] - 1.0)
               for law in laws.values()]
              + [abs(law["sigma_total_from_H25"] / law["sigma_total"] - 1.0)
                 for m in lognormal["members"].values() for law in m["laws"].values()])
    return {"radius_Mpc": R, "pair_density_norm": pair_norm, "threshold_c": c,
            "radial_intervals": RADIAL_INTERVALS,
            "radial_refinement_max_rel": refinement, "h25_identity_max_rel": h25,
            "partition_smoothing_ell_Mpc": ell, "target_sigma_partition": target_sigma_part,
            "wall_field_rms_point": sigma_w, "wall_growth_D_wall": d_wall0,
            "conditional_wall_mean_mu_law_II": mu,
            "pair_class": "SIGNED_GAUSSIAN_CARRIER_SURROGATE",
            "negative_wall_density_probability": negative,
            "laws": laws,
            "sigma_ratio_II_over_I": laws["II_same_field"]["sigma_total"]
            / laws["I_independent"]["sigma_total"],
            "nonnegative_lognormal_pair": lognormal}


# ------------------------------------------------- audit remediation evidence
def ensemble_vs_tangent_example() -> dict:
    """GH-F1: averaging the derivative of (H3) is not the zero-amplitude tangent.

    Two equal-mass regions with f_v = 0.737, epsilon = 0 and wall contrasts
    -1/3 and 1 (the audit's example): the mass-weighted mean of
    1/(1 + delta_L) is exactly 1, the mean derivative d delta_L/d delta_w is
    0.27468, the tangent at zero amplitude is f_w = 0.263.  This is why the
    statistic is defined as the formal tangent (D1), not as the ensemble-mean
    response of the true contrast.
    """
    f_v, h = 0.737, 1e-6

    def contrast(s):
        return float(gv.empty_void_region_contrast(void_volume_fraction=f_v,
                                                   wall_density_contrast=s,
                                                   void_volume_contrast=0.0))

    states = (-1.0 / 3.0, 1.0)
    derivs = [(contrast(s + h) - contrast(s - h)) / (2.0 * h) for s in states]
    return {"void_volume_fraction": f_v, "wall_contrasts": list(states),
            "mean_reciprocal_density": float(np.mean([1.0 / (1.0 + contrast(s))
                                                      for s in states])),
            "mean_derivative_central_difference": float(np.mean(derivs)),
            "mean_derivative_exact": float(np.mean([(1.0 - f_v) / (1.0 + f_v * s) ** 2
                                                    for s in states])),
            "tangent_at_zero_amplitude": 1.0 - f_v}


def scale_separation(bg_in, growth, density) -> dict:
    """GH-F2: present void radius over the present proper region radius, convention (c)."""
    h_d, h_bare, g0 = density.h_dressed, density.h_bare, growth.gamma_w0
    region = 8.0 / h_bare
    radii = {"F_median": F_MEDIAN_RADIUS_H_MPC[bg_in.label] * g0 / h_d,
             "W09_15": (W09_VOID_DIAMETER_H_MPC / 2.0) / h_d}
    return {"present_proper_region_radius_Mpc": region,
            **{f"{k}_present_void_radius_Mpc": v for k, v in radii.items()},
            **{f"{k}_ratio": v / region for k, v in radii.items()}}


STEP_K_RANGE = (1e-7, 1e3)
STEP_GRID = 8001
STEP_SELF_CONVERGENCE = 1e-6
STEP_PREMISE_MARGIN = 1e-3


def step_share_counterexample(growth, density, spec, target_R: float, premise_R: float,
                              eta: float, constant_share_upper: float) -> dict:
    """GH-F4: a pointwise-monotone, scale-dependent share outside the (H15) bound.

    ``p(k) = f_v,LS`` for k < k_cut and 1 above (inside H-A7 at every k); k_cut
    makes the premise rms eta (1 - 1e-3).  The variance integral is split at
    k_cut, each part on its own log grid, with a self-convergence check.
    """
    om = density.omega_m_per_photon
    d_w, d_v = growth.wall_share_growth, growth.void_share_growth
    g_lo, g_hi = d_w + (d_v - d_w) * growth.f_v_ls, d_v

    def sigma(R: float, k_cut: float, n: int) -> float:
        total = 0.0
        for ka, kb, g in ((STEP_K_RANGE[0], k_cut, g_lo), (k_cut, STEP_K_RANGE[1], g_hi)):
            lnk = np.linspace(math.log(ka), math.log(kb), n)
            kk = np.exp(lnk)
            amp = np.asarray(ls.matter_era_linear_amplitude(
                k_per_Mpc=kk, early_spectrum=spec, omega_m=om, growth_today_photon_normalised=1.0))
            w = np.asarray(ls.top_hat_window(x=kk * R))
            total += g * g * float(simpson(amp * w * w, x=lnk))
        return math.sqrt(total)

    def checked(R: float, k_cut: float) -> float:
        fine, coarse = sigma(R, k_cut, STEP_GRID), sigma(R, k_cut, STEP_GRID // 2 + 1)
        if not abs(fine / coarse - 1.0) <= STEP_SELF_CONVERGENCE:
            raise AssertionError("step-kernel variance not converged")
        return fine

    target = eta * (1.0 - STEP_PREMISE_MARGIN)
    log_k = brentq(lambda lk: checked(premise_R, math.exp(lk)) - target,
                   math.log(1e-3), math.log(1.0), xtol=1e-12)
    k_cut = math.exp(log_k)
    s_hom, s_target = checked(premise_R, k_cut), checked(target_R, k_cut)
    return {"share_low_k": growth.f_v_ls, "share_high_k": 1.0, "k_cut_per_Mpc": k_cut,
            "premise_radius_Mpc": premise_R, "premise_eta": eta, "premise_rms": s_hom,
            "target_radius_Mpc": target_R, "target_rms": s_target,
            "constant_share_upper": constant_share_upper,
            "ratio_to_constant_share_upper": s_target / constant_share_upper}


def pbs_reclosure(bg_in, clos, radius, anchor_factor: float, rows: dict, conv: str) -> dict:
    """GH-F6: rescale the input spectrum by the anchor factor and recompute p.

    A uniform rescaling of the early spectrum amplitude (A_s times the factor
    squared) changes sigma_s and therefore the PBS threshold share; the
    post-hoc normalisation multiplies the finished value at fixed closure.
    For a constant share both agree exactly.  Under reclosure the (H15) upper
    end is unchanged at fixed eta and the lower end scales with the factor.
    """
    spec_re = early_spectrum(2.100e-9 * anchor_factor ** 2)
    out = {"A_s_factor": anchor_factor ** 2}
    records = {}
    for cname in ("monotone_lower_p_fvLS", "pbs_tracker_seed_compressed",
                  "pbs_tracker_seed_F_median_compressed"):
        r = run_case(bg_in, clos[cname], spec_re, radius)
        records[cname] = r
        post = rows[cname]["linear_sigma_planck_anchored"]
        out[cname] = {"direct": rows[cname]["linear_sigma_direct_A_s"],
                      "post_hoc_fixed_closure": post, "reclosure": r.linear_sigma,
                      "share_k0_direct": rows[cname]["share_k0"],
                      "share_k0_reclosure": r.void_share.share_k0,
                      "reclosure_over_post_hoc": r.linear_sigma / post}
    L_hom, eta = PREMISES["W09_10pct_at_100"]
    prem = gv.HomogeneityPremise(radius=radius_spec(conv, L_hom), max_linear_rms=eta,
                                 provenance="[W09] read as rms <= 0.10 at 100 (reclosure)")
    iv = gv.admissible_global_linear_interval(target=records["pbs_tracker_seed_compressed"],
                                              premise=prem)
    out["interval_W09_10pct_at_100_reclosure"] = {"lower": iv.lower, "upper": iv.upper,
                                                  "share_upper": iv.share_upper}
    return out


# -------------------------------------------------------------------- figures
def figures(results: dict) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    FIGURES.mkdir(parents=True, exist_ok=True)
    written = []
    # 1. sigma versus the void share with the constant-share interval.
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
                   label=f"{name} constant-share interval (H15), adopted 10%-at-100 reading")
        prim = conv["closures"]["pbs_tracker_seed_compressed"]
        ax.plot([prim["share_k0"]], [prim["linear_sigma_direct_A_s"]], "o", color=colour,
                label=f"{name} PBS seed, [W09] void radius")
        fmed = conv["closures"]["pbs_tracker_seed_F_median_compressed"]
        ax.plot([fmed["share_k0"]], [fmed["linear_sigma_direct_A_s"]], "s", color=colour,
                label=f"{name} PBS seed, 1G-F median radius")
    ax.set_xlabel("void share p (k -> 0)")
    ax.set_ylabel("global-mean linear rms at 8 / h_bare Mpc (c)")
    ax.set_title("Formal tangent statistic vs the void-share closure (conditional)")
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
            if conv in ("c_bare_volume_average", "a_equal_mass"):
                reclosure = pbs_reclosure(bg_in, clos, radius, anchor["factor"], rows, conv)
                case["conventions"][conv]["pbs_reclosure_under_spectrum_rescaling"] = reclosure
                row = reclosure["monotone_lower_p_fvLS"]
                gate(f"{name} {conv} constant share reclosure equals post-hoc",
                     abs(row["reclosure_over_post_hoc"] - 1.0),
                     GATES["reclosure_constant_share_rel"], kind="physics")
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
                # Audit remediation evidence (GH-F2, GH-F4, GH-F7).
                case["scale_separation"] = scale_separation(bg_in, growth, density)
                ratio = rows["wall_mode_p0"]["flat_wall_capacity_ratio"]
                case["flat_wall_cap_exceedance"] = {
                    "capacity_ratio_at_target": ratio,
                    "gaussian_fraction_above_cap": float(ndtr(-1.0 / ratio)),
                    "meaning": "fraction of the matching-epoch Gaussian contrast above the "
                               "strict flat-wall cap (H13), not the whole overdense half"}
                L_hom, eta = PREMISES["W09_10pct_at_100"]
                step = step_share_counterexample(
                    growth, density, spec, target_R=primary_record.radius.radius_Mpc,
                    premise_R=resolve_radius(radius_spec(conv, L_hom), density), eta=eta,
                    constant_share_upper=intervals["W09_10pct_at_100"]["upper"])
                case["step_share_counterexample"] = step
                gate(f"{name} step kernel satisfies the premise",
                     step["premise_rms"] / step["premise_eta"],
                     GATES["step_kernel_premise_ratio"], kind="physics")
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
        budget = e_reference_rounding_budget(
            sigma_partition=sp, sigma_internal=si, sigma_total=var["rms"],
            half_unit=GATES["E_reference_printed_half_unit"])
        gate(f"{name} E reference reproduction within its rounding budget",
             abs(var["rms"] - stot), budget, kind="reproduction")
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
        lognormal = gtp["nonnegative_lognormal_pair"]
        gate(f"{name} lognormal ball-variance calibration",
             max(m["calibration_rel"] for m in lognormal["members"].values()),
             GATES["lognormal_ball_variance_calibration_rel"], kind="numerics")
        gate(f"{name} lognormal linear limit reproduces the signed pair",
             lognormal["linear_limit"]["max_wall_moment_rel_difference"],
             GATES["lognormal_linear_limit_rel"], kind="physics")
        gate(f"{name} constructive pairs radial refinement", gtp["radial_refinement_max_rel"],
             GATES["radial_refinement_rel"], kind="numerics")
        gate(f"{name} constructive pairs (H25) identity", gtp["h25_identity_max_rel"],
             GATES["h25_identity_rel"], kind="physics")
        cov[name] = {"E_reference": {"sigma_part": sp, "sigma_int": si, "sigma_printed": stot,
                                     "reproduced": var["rms"], "rounding_budget": budget},
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
            mom = _orthant(rho, cthr)
            exact = float(multivariate_normal(mean=[0.0, 0.0], cov=[[1.0, rho], [rho, 1.0]]).cdf(
                [-cthr, -cthr]))
            worst = max(worst, abs(mom["P11"] - exact))
    gate("orthant P11 vs bivariate CDF", worst, GATES["gt_orthant_P11_vs_bivariate_cdf_abs"],
         kind="numerics")
    # Analytic special cases of the audit (GH-F10): independence, c = 0 and a
    # far threshold, including near-singular correlations.
    analytic = {"rho0_c_minus100": (_orthant(0.0, -100.0)["P11"], 1.0),
                "rho0_c0p634": (_orthant(0.0, 0.634)["P11"], float(ndtr(-0.634)) ** 2)}
    for rho in (0.999999, -0.999999, 0.5):
        analytic[f"c0_rho{rho:+g}"] = (gv.bivariate_normal_orthant_probability(
            correlation=rho, threshold_1=0.0, threshold_2=0.0, nodes=ORTHANT_START_NODES,
            tolerance=ORTHANT_TOLERANCE), 0.25 + math.asin(rho) / (2.0 * math.pi))
    worst_analytic = max(abs(a - b) for a, b in analytic.values())
    gate("orthant analytic special cases", worst_analytic, GATES["orthant_analytic_cases_abs"],
         kind="numerics")
    results["orthant_analytic_cases"] = {k: {"value": a, "exact": b}
                                         for k, (a, b) in analytic.items()}
    results["ensemble_vs_tangent_example"] = ensemble_vs_tangent_example()
    results["two_phase_covariance"] = cov
    results["gates"] = gates_seen
    results["gate_definitions"] = GATES
    results["environment"] = environment()
    if not args.no_figures:
        results["figures"] = figures(results)
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(results, indent=2, sort_keys=True, default=_json_default,
                         allow_nan=False) + "\n"
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
        ex = case["flat_wall_cap_exceedance"]
        print(f"  fraction above the flat-wall cap at R8: {ex['gaussian_fraction_above_cap']:.4f}")
        sep = case["scale_separation"]
        print(f"  void/region radius (c): F median {sep['F_median_ratio']:.3f}, "
              f"W09 {sep['W09_15_ratio']:.3f}")
        st = case["step_share_counterexample"]
        print(f"  step kernel: k_cut = {st['k_cut_per_Mpc']:.6g}, premise rms "
              f"{st['premise_rms']:.5f}, target rms {st['target_rms']:.4f} (constant-share "
              f"upper {st['constant_share_upper']:.4f})")
        for conv in ("c_bare_volume_average", "a_equal_mass"):
            rec = case["conventions"][conv]["pbs_reclosure_under_spectrum_rescaling"]
            for cname in ("pbs_tracker_seed_compressed", "pbs_tracker_seed_F_median_compressed"):
                row = rec[cname]
                print(f"  [{conv}] {cname}: direct {row['direct']:.4f}, post-hoc "
                      f"{row['post_hoc_fixed_closure']:.4f}, reclosure {row['reclosure']:.4f}")
    for name, cov in results["two_phase_covariance"].items():
        gtp = cov["gaussian_threshold_pair"]
        print(f"\n{name} GT pair at R = {gtp['radius_Mpc']:.4f} Mpc, ell = "
              f"{gtp['partition_smoothing_ell_Mpc']:.4f} Mpc:")
        for law, row in gtp["laws"].items():
            print(f"  signed {law:15s} sigma_part = {row['sigma_partition']:.4f}  sigma_wall = "
                  f"{row['sigma_wall_field']:.4f}  cross = {row['cross_term']:+.4f}  total = "
                  f"{row['sigma_total']:.4f}  P(rho<0|wall) = "
                  f"{gtp['negative_wall_density_probability'][law]:.4f}  <C_W - 1> = "
                  f"{row['both_walls_conditional_density_covariance_ball']:.4f}")
        ln = gtp["nonnegative_lognormal_pair"]
        for mname, mem in ln["members"].items():
            print(f"  lognormal {mname}: lambda = {mem['latent_scale_lambda']:.4f}, latent point "
                  f"variance {mem['latent_point_variance']:.3f}, density point variance "
                  f"{mem['density_point_variance']:.2f}; II/I = {mem['sigma_ratio_II_over_I']:.4f}; "
                  f"m_II = {mem['conditional_normaliser_ratio_m_II']:.4f} (covariance ratio "
                  f"{mem['conditional_density_covariance_ratio_II_over_I']:.4f})")
            for law, row in mem["laws"].items():
                print(f"    {law:15s} sigma_part = {row['sigma_partition']:.4f}  sigma_wall = "
                      f"{row['sigma_wall_field']:.4f}  cross = {row['cross_term']:+.4f}  total = "
                      f"{row['sigma_total']:.4f}  <C_W - 1> = "
                      f"{row['both_walls_conditional_density_covariance_ball']:.4f}")
        print(f"  lognormal linear limit: max wall-moment rel. difference "
              f"{ln['linear_limit']['max_wall_moment_rel_difference']:.2e}")
        print(f"  radial refinement max rel. change {gtp['radial_refinement_max_rel']:.2e} "
              f"({gtp['radial_intervals']} intervals); (H25) max rel. "
              f"{gtp['h25_identity_max_rel']:.1e}")


if __name__ == "__main__":
    raise SystemExit(main())
