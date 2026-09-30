"""Phase 1G-B: conditional, model-internal, mass-labelled linear sigma(M).

Validation record: reports/phase1g_b_lagrangian_sigma_validation.md.
Reference values: reports/phase1g_a_sigma8_derivation_path_audit.md ([1G-A])
and its inventory (rounded to the printed digits), plus a full-precision
cross-check against the committed 1G-A evidence script.

A06: absolute budgets use rtol=0 / rel=0; relative budgets use atol=0 / abs=0.
Tolerances for printed 1G-A values are half a unit of the last printed digit
(e.g. abs 5e-7 for six decimals).  Machine-precision identities use rel 1e-13
(round-off allowance for a few dozen float64 operations).  Cross-unit /
cross-G comparisons of the adaptive growing-mode integration use rel 1e-10
(the integration controls are rtol 1e-12; step selection differs in the last
bits between unit systems).
"""

from __future__ import annotations

import dataclasses
import importlib.util
import inspect
import json
import math
from functools import lru_cache
from pathlib import Path

import numpy as np
import pytest

import timescape_fsigma8.background as bg
import timescape_fsigma8.lagrangian_sigma as ls
from timescape_fsigma8 import scientific_status, units
from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.growth import GrowthSystem
from timescape_fsigma8.perturbations.growing_mode import CleanPerturbationSystem
from timescape_fsigma8.perturbations.initial_conditions import PLANCK_2018_QPLUS_RECIPE
from timescape_fsigma8.presets import NOTEBOOK_REFERENCE, PAPER_REFERENCE

ROOT = Path(__file__).resolve().parents[1]
NA = ls.NOT_APPLICABLE
COMOVING = CleanPerturbationSystem.COMOVING
MESZAROS = CleanPerturbationSystem.MESZAROS
CGI = ls.GrowthLaw.VOLUME_AVERAGE_CGI
WALL = ls.GrowthLaw.WALL_REGIONAL_EDS_COMMON_TIME
CGI_NUMERICS = ls.VOLUME_AVERAGE_GROWTH_REFERENCE_NUMERICS
WALL_CHECKS = ls.WALL_REGIONAL_GROWTH_REFERENCE_CHECKS
QUADRATURE = ls.LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE
IDENTITY_RTOL = 1e-13

# Planck 2018 VI (arXiv:1807.06209) Table 2 inputs used by [1G-A] Sec. 6.3;
# test-local on purpose: the package ships no Planck parameter set or anchor.
OMEGA_M_LCDM = PLANCK_2018_QPLUS_RECIPE.omega_m * PLANCK_2018_QPLUS_RECIPE.h ** 2
R_LCDM = 8.0 / PLANCK_2018_QPLUS_RECIPE.h
PRIMARY_FB = 0.02237 / OMEGA_M_LCDM
ANCHOR = 0.8111
# [1G-A] Sec. 6.3: EH98 + these inputs is +3.03% from the anchor; the first
# run failed a 3% gate, the gate is 5% because EH98 omits BAO wiggles and the
# Planck 0.06 eV neutrino suppression (about -1.5%).
ANCHOR_TOLERANCE = 0.05
ANCHOR_RATIONALE = ("EH98 zero-baryon-oscillation fit omits BAO wiggles and the "
                    "0.06 eV neutrino suppression; anchored ratios cancel the common bias")


def early_spectrum(**overrides) -> ls.EarlySpectrumImport:
    fields = dict(A_s=2.100e-9, n_s=0.9649, k_pivot_per_Mpc=0.05, baryon_fraction=PRIMARY_FB,
                  T_cmb_K=2.7255,
                  transfer_model=ls.EarlyTransferModel.EH98_ZERO_BARYON_OSCILLATION,
                  provenance="Planck 2018 VI Table 2 (test fixture)",
                  import_status=ls.EARLY_SPECTRUM_IMPORT_STATUS)
    fields.update(overrides)
    return ls.EarlySpectrumImport(**fields)


SPEC = early_spectrum()
BACKGROUNDS = {
    "PAPER_REFERENCE": ls.TimescapeTrackerInput.from_reference_preset(preset=PAPER_REFERENCE),
    "NOTEBOOK_REFERENCE": ls.TimescapeTrackerInput.from_reference_preset(preset=NOTEBOOK_REFERENCE),
    "NW15_CMB_FIT": ls.TimescapeTrackerInput(
        label="NW15_CMB_FIT", fv0=0.627, H0_dressed_km_s_Mpc=61.0,
        source="Nazer & Wiltshire, arXiv:1410.3470 (Timescape CMB fit)"),
}


def radius_spec(kind: str) -> ls.LagrangianRadiusSpec:
    C = ls.LagrangianRadiusConvention
    if kind == "equal_mass":
        return ls.LagrangianRadiusSpec(
            convention=C.EQUAL_LAGRANGIAN_MASS_TO_REFERENCE, length_h_inverse_Mpc=NA,
            reference_omega_m=OMEGA_M_LCDM, reference_radius_Mpc=R_LCDM, explicit_radius_Mpc=NA)
    if kind == "dressed":
        return ls.LagrangianRadiusSpec(
            convention=C.DRESSED_WALL_COMOVING_LENGTH, length_h_inverse_Mpc=8.0,
            reference_omega_m=NA, reference_radius_Mpc=NA, explicit_radius_Mpc=NA)
    if kind == "bare":
        return ls.LagrangianRadiusSpec(
            convention=C.BARE_VOLUME_AVERAGE_PROPER_LENGTH, length_h_inverse_Mpc=8.0,
            reference_omega_m=NA, reference_radius_Mpc=NA, explicit_radius_Mpc=NA)
    raise AssertionError(kind)


def explicit_radius(value: float) -> ls.LagrangianRadiusSpec:
    return ls.LagrangianRadiusSpec(
        convention=ls.LagrangianRadiusConvention.EXPLICIT_PHOTON_NORMALISED_RADIUS,
        length_h_inverse_Mpc=NA, reference_omega_m=NA, reference_radius_Mpc=NA,
        explicit_radius_Mpc=value)


LAWS = {
    "comoving": (CGI, COMOVING, CGI_NUMERICS),
    "meszaros": (CGI, MESZAROS, CGI_NUMERICS),
    "wall": (WALL, NA, WALL_CHECKS),
}


@lru_cache(maxsize=None)
def sigma(case: str, law: str, radius: str) -> ls.ConditionalLagrangianSigma:
    growth_law, closure, numerics = LAWS[law]
    return ls.conditional_lagrangian_linear_sigma(
        background=BACKGROUNDS[case], growth_law=growth_law, closure=closure,
        growth_numerics=numerics, early_spectrum=SPEC, radius=radius_spec(radius),
        quadrature=QUADRATURE, density_identity_tolerance=IDENTITY_RTOL, G=1.0)


@lru_cache(maxsize=None)
def reference() -> ls.LCDMReferenceLinearSigma:
    return ls.lcdm_reference_linear_sigma(
        recipe=PLANCK_2018_QPLUS_RECIPE, early_spectrum=SPEC, radius_Mpc=R_LCDM,
        quadrature=QUADRATURE)


def anchored(case: str, law: str, radius: str) -> ls.AnchoredLagrangianSigmaRatio:
    return ls.anchor_lagrangian_sigma(
        timescape=sigma(case, law, radius), reference=reference(), anchor_value=ANCHOR,
        anchor_provenance="Planck 2018 VI Table 2 linear amplitude (test fixture)",
        anchor_consistency_tolerance=ANCHOR_TOLERANCE,
        anchor_consistency_rationale=ANCHOR_RATIONALE)


def growth(params: TrackerParams, law: str, G: float = 1.0) -> ls.TimescapeGrowthFactor:
    growth_law, closure, numerics = LAWS[law]
    return ls.timescape_growth_factor(params=params, growth_law=growth_law, closure=closure,
                                      numerics=numerics, G=G)


def dimensionless(fv0: float) -> TrackerParams:
    return TrackerParams.from_dressed_H0(fv0=fv0, H0=1.0)


# ------------------------------------------------------------ 1G-A reference values
# [1G-A] Sec. 5.2 table and inventory growth_ratio (six decimals).
@pytest.mark.parametrize("case, law, g_ref, x_ref", [
    ("PAPER_REFERENCE", "comoving", 0.402663, 0.699461),
    ("PAPER_REFERENCE", "meszaros", 0.341694, 0.593553),
    ("NW15_CMB_FIT", "comoving", 0.514953, 0.858568),
    ("NW15_CMB_FIT", "meszaros", 0.458563, 0.764551),
])
def test_volume_average_growth_reproduces_1g_a(case, law, g_ref, x_ref):
    result = anchored(case, law, "equal_mass")
    g = result.timescape.growth
    assert g.growth_relative_to_volume_average_eds == pytest.approx(g_ref, rel=0.0, abs=5e-7)
    assert result.growth_ratio == pytest.approx(x_ref, rel=0.0, abs=5e-7)
    assert result.reference.growth_today_photon_normalised == pytest.approx(
        0.787813, rel=0.0, abs=5e-7)
    # [1G-A] Sec. 5.2 convergence: grid refinement <= 4e-15 (budget 1e-7),
    # early limit <= 2e-5 (budget 1e-4).
    assert g.diagnostic("log_growth_grid_refinement_change") <= 1e-14
    assert g.diagnostic("log_growth_early_limit_change") <= 2e-5


# Lead's scope addition / [1G-A] Sec. 8 and inventory two_scale_bracket.
@pytest.mark.parametrize("case, x_wall", [("PAPER_REFERENCE", 1.112945),
                                          ("NW15_CMB_FIT", 1.200172)])
def test_wall_regional_growth_reproduces_1g_a_and_closed_form(case, x_wall):
    result = anchored(case, "wall", "equal_mass")
    g = result.timescape.growth
    fv0 = BACKGROUNDS[case].fv0
    assert result.growth_ratio == pytest.approx(x_wall, rel=0.0, abs=5e-7)
    closed = 0.5 * (2.0 + fv0) * (1.0 - fv0) ** (1.0 / 3.0)
    assert g.growth_today_photon_normalised == pytest.approx(closed, rel=IDENTITY_RTOL, abs=0.0)
    assert g.growth_relative_to_volume_average_eds == pytest.approx(
        (1.0 - fv0) ** (1.0 / 3.0), rel=IDENTITY_RTOL, abs=0.0)
    for name in ("closed_form_vs_tracker_rel", "regional_scale_over_t23_rel_spread",
                 "regional_density_eds_max_rel", "finite_te_identity_rel"):
        assert g.diagnostic(name) <= IDENTITY_RTOL, name
    # The uncorrected limit (t0/t_e)^(2/3)/(1+z_e) approaches the closed form
    # from below as -f_v(t_e)/6 (derived in the validation report, Sec. 4.2).
    fv_te = g.diagnostic("fv_at_te")
    assert g.diagnostic("uncorrected_finite_te_limit_rel") == pytest.approx(
        -fv_te / 6.0, rel=1e-6, abs=0.0)
    assert g.evidence_class == "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
    assert g.closure == NA


@pytest.mark.parametrize("case, omega_ref, omega_rel_planck", [
    ("PAPER_REFERENCE", 0.12048, 0.842),
    ("NOTEBOOK_REFERENCE", 0.12114, 0.847),
    ("NW15_CMB_FIT", 0.13094, 0.915),
])
def test_per_photon_density_reproduces_1g_a(case, omega_ref, omega_rel_planck):
    density = ls.early_matter_density_per_photon(
        background=BACKGROUNDS[case], identity_tolerance=IDENTITY_RTOL, G=1.0)
    assert density.omega_m_per_photon == pytest.approx(omega_ref, rel=0.0, abs=5e-6)
    assert density.omega_m_per_photon / OMEGA_M_LCDM == pytest.approx(
        omega_rel_planck, rel=0.0, abs=5e-4)
    assert density.closed_form == pytest.approx(
        density.omega_m_per_photon, rel=IDENTITY_RTOL, abs=0.0)
    assert density.identity_relative_residual <= IDENTITY_RTOL


# [1G-A] Sec. 7 table / inventory conditional_sigma_M8 (four decimals) and
# the wall-regional rows of Sec. 8 (inventory two_scale_bracket).
SIGMA_TABLE = [
    ("PAPER_REFERENCE", "comoving", "equal_mass", 12.5702, 0.9238, 0.5241),
    ("PAPER_REFERENCE", "comoving", "dressed", 10.9544, 1.0104, 0.5733),
    ("PAPER_REFERENCE", "comoving", "bare", 10.1041, 1.0634, 0.6033),
    ("PAPER_REFERENCE", "meszaros", "equal_mass", 12.5702, 0.9238, 0.4447),
    ("PAPER_REFERENCE", "meszaros", "dressed", 10.9544, 1.0104, 0.4865),
    ("PAPER_REFERENCE", "meszaros", "bare", 10.1041, 1.0634, 0.5119),
    ("PAPER_REFERENCE", "wall", "equal_mass", 12.5702, 0.9238, 0.8339),
    ("PAPER_REFERENCE", "wall", "dressed", 10.9544, 1.0104, 0.9121),
    ("PAPER_REFERENCE", "wall", "bare", 10.1041, 1.0634, 0.9599),
    ("NW15_CMB_FIT", "comoving", "equal_mass", 12.2260, 0.9602, 0.6687),
    ("NW15_CMB_FIT", "comoving", "dressed", 13.1148, 0.9153, 0.6374),
    ("NW15_CMB_FIT", "comoving", "bare", 11.7814, 0.9844, 0.6855),
    ("NW15_CMB_FIT", "meszaros", "equal_mass", 12.2260, 0.9602, 0.5954),
    ("NW15_CMB_FIT", "meszaros", "dressed", 13.1148, 0.9153, 0.5676),
    ("NW15_CMB_FIT", "meszaros", "bare", 11.7814, 0.9844, 0.6104),
    ("NW15_CMB_FIT", "wall", "equal_mass", 12.2260, 0.9602, 0.9347),
    ("NW15_CMB_FIT", "wall", "dressed", 13.1148, 0.9153, 0.8910),
    ("NW15_CMB_FIT", "wall", "bare", 11.7814, 0.9844, 0.9582),
]


@pytest.mark.parametrize("case, law, radius, r_ref, e_ref, sigma_ref", SIGMA_TABLE)
def test_anchored_sigma_table_reproduces_1g_a(case, law, radius, r_ref, e_ref, sigma_ref):
    result = anchored(case, law, radius)
    assert result.timescape.radius.radius_Mpc == pytest.approx(r_ref, rel=0.0, abs=5e-5)
    assert result.early_spectrum_factor == pytest.approx(e_ref, rel=0.0, abs=5e-5)
    assert result.anchored_linear_sigma == pytest.approx(sigma_ref, rel=0.0, abs=5e-5)
    assert result.sigma_ratio == pytest.approx(
        result.growth_ratio * result.early_spectrum_factor, rel=IDENTITY_RTOL, abs=0.0)
    assert result.early_spectrum_differences == ()


def test_lcdm_reference_normalisation_within_documented_gate():
    ref = reference()
    # [1G-A] Sec. 6.3: EH98 Planck value 0.8357, +3.03% from the 0.8111 anchor.
    assert ref.linear_sigma == pytest.approx(0.8357, rel=0.0, abs=5e-5)
    result = anchored("PAPER_REFERENCE", "comoving", "equal_mass")
    assert result.reference_offset_from_anchor == pytest.approx(0.0303, rel=0.0, abs=5e-5)
    assert abs(result.reference_offset_from_anchor) <= ANCHOR_TOLERANCE
    assert ref.radius_Mpc == pytest.approx(11.869436, rel=0.0, abs=5e-7)
    # The original 3% gate fails closed, exactly as recorded in [1G-A].
    with pytest.raises(ls.LagrangianSigmaContractError, match="from the anchor"):
        ls.anchor_lagrangian_sigma(
            timescape=sigma("PAPER_REFERENCE", "comoving", "equal_mass"), reference=ref,
            anchor_value=ANCHOR, anchor_provenance="fixture",
            anchor_consistency_tolerance=0.03, anchor_consistency_rationale="initial gate")


def test_baryon_fraction_sensitivity_matches_1g_a_band():
    # [1G-A] Sec. 7: f_b 0.12 -> 0.20 moves each entry by about +7% / -8%;
    # the LCDM reference keeps the primary f_b (the anchor's model).
    base = anchored("PAPER_REFERENCE", "comoving", "equal_mass").anchored_linear_sigma
    values = {}
    for f_b in (0.12, 0.20):
        ts = ls.conditional_lagrangian_linear_sigma(
            background=BACKGROUNDS["PAPER_REFERENCE"], growth_law=CGI, closure=COMOVING,
            growth_numerics=CGI_NUMERICS, early_spectrum=early_spectrum(baryon_fraction=f_b),
            radius=radius_spec("equal_mass"), quadrature=QUADRATURE,
            density_identity_tolerance=IDENTITY_RTOL, G=1.0)
        result = ls.anchor_lagrangian_sigma(
            timescape=ts, reference=reference(), anchor_value=ANCHOR, anchor_provenance="fixture",
            anchor_consistency_tolerance=ANCHOR_TOLERANCE,
            anchor_consistency_rationale=ANCHOR_RATIONALE)
        assert result.early_spectrum_differences == ("baryon_fraction",)
        values[f_b] = result.anchored_linear_sigma
    assert 1.06 <= values[0.12] / base <= 1.08
    assert 0.91 <= values[0.20] / base <= 0.93


# ------------------------------------------------ full-precision script cross-check
@lru_cache(maxsize=None)
def script_module():
    path = ROOT / "scripts" / "phase1g_a_sigma8_path_numerics.py"
    spec = importlib.util.spec_from_file_location("_phase1g_a_numerics", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)   # defines functions only; main() is not run
    return module


def test_full_precision_agreement_with_1g_a_evidence_script():
    script = script_module()
    p_gyr = PAPER_REFERENCE.tracker_params_gyr
    # Growth: identical Simpson/regular-growing-mode route on identical params.
    for system in CleanPerturbationSystem:
        expected = math.exp(script._riccati_log_growth_excess(p_gyr, system, 1e-6 * p_gyr.t0, 16001))
        ours = ls.timescape_growth_factor(params=p_gyr, growth_law=CGI, closure=system,
                                          numerics=CGI_NUMERICS, G=1.0)
        assert ours.growth_relative_to_volume_average_eds == pytest.approx(
            expected, rel=1e-13, abs=0.0)
    # Per-photon density: script evaluates it in Gyr units, the package in km/s/Mpc.
    expected = script.per_photon_matter_density(p_gyr)["omega_m_per_photon"]
    density = ls.early_matter_density_per_photon(
        background=BACKGROUNDS["PAPER_REFERENCE"], identity_tolerance=IDENTITY_RTOL, G=1.0)
    assert density.omega_m_per_photon == pytest.approx(expected, rel=IDENTITY_RTOL, abs=0.0)
    # Quadrature: same grid, same formulas (window series differs below |x|<0.1).
    ours = sigma("PAPER_REFERENCE", "comoving", "equal_mass")
    expected = script.sigma_converged(ours.radius.radius_Mpc, ours.density.omega_m_per_photon,
                                      PRIMARY_FB, 0.9649,
                                      ours.growth.growth_today_photon_normalised)
    assert ours.linear_sigma == pytest.approx(expected, rel=1e-12, abs=0.0)
    expected_ref = script.sigma_converged(R_LCDM, OMEGA_M_LCDM, PRIMARY_FB, 0.9649,
                                          reference().growth_today_photon_normalised)
    assert reference().linear_sigma == pytest.approx(expected_ref, rel=1e-12, abs=0.0)


# ------------------------------------------------------ dimensions and self-similarity
def test_growth_is_independent_of_H0_time_unit_and_G():
    gyr = PAPER_REFERENCE.tracker_params_gyr
    kms = TrackerParams.from_dressed_H0(fv0=0.737, H0=73.03)
    for law in ("comoving", "meszaros", "wall"):
        base = growth(dimensionless(0.737), law).growth_today_photon_normalised
        for params, G in ((gyr, 1.0), (kms, 1.0), (dimensionless(0.737), 4.30091e-9)):
            other = growth(params, law, G=G).growth_today_photon_normalised
            assert other == pytest.approx(base, rel=1e-10, abs=0.0), (law, params, G)
    # Paper and notebook presets (same f_v0, different H0) give the same X.
    x_paper = anchored("PAPER_REFERENCE", "comoving", "equal_mass").growth_ratio
    x_notebook = anchored("NOTEBOOK_REFERENCE", "comoving", "equal_mass").growth_ratio
    assert x_notebook == pytest.approx(x_paper, rel=1e-10, abs=0.0)


def test_per_photon_density_scales_as_H0_squared_and_is_G_independent():
    base = ls.early_matter_density_per_photon(
        background=BACKGROUNDS["PAPER_REFERENCE"], identity_tolerance=IDENTITY_RTOL, G=1.0)
    doubled = ls.early_matter_density_per_photon(
        background=dataclasses.replace(BACKGROUNDS["PAPER_REFERENCE"],
                                       H0_dressed_km_s_Mpc=2.0 * 73.03),
        identity_tolerance=IDENTITY_RTOL, G=1.0)
    other_G = ls.early_matter_density_per_photon(
        background=BACKGROUNDS["PAPER_REFERENCE"], identity_tolerance=IDENTITY_RTOL,
        G=4.30091e-9)
    assert doubled.omega_m_per_photon == pytest.approx(
        4.0 * base.omega_m_per_photon, rel=IDENTITY_RTOL, abs=0.0)
    assert other_G.omega_m_per_photon == pytest.approx(
        base.omega_m_per_photon, rel=IDENTITY_RTOL, abs=0.0)
    # H_D0 from the dressed H0 ([GM] p. 25) agrees with the frozen preset path.
    assert base.HD0_bare_km_s_Mpc == pytest.approx(
        PAPER_REFERENCE.HD0_bare_km_s_Mpc, rel=IDENTITY_RTOL, abs=0.0)
    assert base.gamma_w0 == pytest.approx(1.0 + 0.737 / 2.0, rel=IDENTITY_RTOL, abs=0.0)
    # Gyr-unit route of the 1G-A script: rho_crit(100) via the audited units.
    p = PAPER_REFERENCE.tracker_params_gyr
    h100 = units.kms_per_mpc_to_per_gyr(100.0)
    gyr_value = float(bg.rho_d(p.t0, p, 1.0)) * 1.3685 ** 3 / (3.0 * h100 ** 2 / (8.0 * math.pi))
    assert gyr_value == pytest.approx(base.omega_m_per_photon, rel=IDENTITY_RTOL, abs=0.0)


def test_radius_conventions_and_mass_label():
    density = sigma("PAPER_REFERENCE", "comoving", "equal_mass").density
    equal = ls.resolve_lagrangian_radius(spec=radius_spec("equal_mass"), density=density)
    dressed = ls.resolve_lagrangian_radius(spec=radius_spec("dressed"), density=density)
    bare = ls.resolve_lagrangian_radius(spec=radius_spec("bare"), density=density)
    # Equal Lagrangian mass: omega R^3 is the reference value.
    assert equal.omega_m_R_cubed_Mpc3 == pytest.approx(
        OMEGA_M_LCDM * R_LCDM ** 3, rel=IDENTITY_RTOL, abs=0.0)
    assert dressed.radius_Mpc == pytest.approx(8.0 / 0.7303, rel=IDENTITY_RTOL, abs=0.0)
    assert bare.radius_Mpc == pytest.approx(
        8.0 / density.h_bare / density.gamma_w0, rel=IDENTITY_RTOL, abs=0.0)
    # Linear in the explicit length L (no hidden 8 h^-1 Mpc).
    twelve = dataclasses.replace(radius_spec("dressed"), length_h_inverse_Mpc=12.0)
    assert ls.resolve_lagrangian_radius(spec=twelve, density=density).radius_Mpc == (
        pytest.approx(1.5 * dressed.radius_Mpc, rel=IDENTITY_RTOL, abs=0.0))
    explicit = ls.resolve_lagrangian_radius(spec=explicit_radius(9.5), density=density)
    assert explicit.radius_Mpc == 9.5
    assert {equal.convention_status, dressed.convention_status} == {"CONVENTION_DEPENDENT"}


def test_sigma_is_linear_in_growth_and_scales_as_sqrt_A_s():
    base = sigma("PAPER_REFERENCE", "comoving", "equal_mass")
    assert base.linear_sigma == (
        base.growth.growth_today_photon_normalised * base.sigma_unit_growth)
    quadrupled = ls.conditional_lagrangian_linear_sigma(
        background=BACKGROUNDS["PAPER_REFERENCE"], growth_law=CGI, closure=COMOVING,
        growth_numerics=CGI_NUMERICS, early_spectrum=early_spectrum(A_s=4.0 * 2.100e-9),
        radius=radius_spec("equal_mass"), quadrature=QUADRATURE,
        density_identity_tolerance=IDENTITY_RTOL, G=1.0)
    assert quadrupled.linear_sigma == pytest.approx(
        2.0 * base.linear_sigma, rel=IDENTITY_RTOL, abs=0.0)
    k = np.geomspace(1e-4, 10.0, 7)
    one = ls.matter_era_linear_amplitude(k_per_Mpc=k, early_spectrum=SPEC, omega_m=0.14,
                                         growth_today_photon_normalised=1.0)
    three = ls.matter_era_linear_amplitude(k_per_Mpc=k, early_spectrum=SPEC, omega_m=0.14,
                                           growth_today_photon_normalised=3.0)
    np.testing.assert_allclose(three, 9.0 * one, rtol=IDENTITY_RTOL, atol=0.0)


# ------------------------------------------------------------------ limiting cases
def test_transfer_function_limits():
    k = np.geomspace(1e-9, 1e2, 400)
    T = ls.eh98_zero_baryon_transfer(k_per_Mpc=k, omega_m=0.143, baryon_fraction=PRIMARY_FB,
                                     T_cmb_K=2.7255)
    assert T[0] == pytest.approx(1.0, rel=0.0, abs=1e-12)          # small-k limit T -> 1
    assert np.all(T > 0.0) and np.all(T <= 1.0)
    assert np.all(np.diff(T) < 0.0)                                  # monotone suppression
    # f_b = 0 reduces EH98 Eqs. (30)-(31) to Gamma_eff h = omega_m (alpha_Gamma = 1).
    no_baryon = ls.eh98_zero_baryon_transfer(k_per_Mpc=k, omega_m=0.143, baryon_fraction=0.0,
                                             T_cmb_K=2.7)
    q = k / 0.143
    L0 = np.log(2.0 * math.e + 1.8 * q)
    np.testing.assert_allclose(no_baryon, L0 / (L0 + (14.2 + 731.0 / (1.0 + 62.5 * q)) * q ** 2),
                               rtol=IDENTITY_RTOL, atol=0.0)


def test_top_hat_window_limits_series_and_envelope():
    assert float(ls.top_hat_window(x=0.0)) == 1.0
    # 1 - x^2/10 + x^4/280 at x = 1e-4, to a few float64 ulps near 1.
    assert float(ls.top_hat_window(x=1e-4)) == pytest.approx(1.0 - 1e-9, rel=0.0, abs=5e-16)
    threshold = ls.TOP_HAT_SERIES_THRESHOLD
    below = float(ls.top_hat_window(x=np.nextafter(threshold, 0.0)))
    above = float(ls.top_hat_window(x=threshold))
    # Series/closed-form continuity; the residual is the closed form's
    # cancellation error ~eps/x^2 at the threshold (measured 2.6e-14).
    assert below == pytest.approx(above, rel=1e-13, abs=0.0)
    x = np.linspace(0.2, 50.0, 997)
    exact = 3.0 * (np.sin(x) - x * np.cos(x)) / x ** 3
    np.testing.assert_allclose(ls.top_hat_window(x=x), exact, rtol=0.0, atol=0.0)
    assert np.all(np.abs(ls.top_hat_window(x=x)) <= 3.0 / x ** 2 + 3.0 / x ** 3)
    # Even function.  Not asserted bitwise: NumPy's vectorised ``x ** 3`` is
    # not exactly odd on every platform (AVX-512 builds differ by one ulp for
    # some -x vs x; sin/cos stay exactly odd/even), so W(-x) and W(x) may
    # differ by a few ulps (measured <= 2.9e-16 relative on Linux AVX-512).
    # Phase 1G-B adversarial audit GB-F1, option A (test only), owner
    # decision 2026-09-30; the implementation is unchanged.
    np.testing.assert_allclose(ls.top_hat_window(x=-x), ls.top_hat_window(x=x),
                               rtol=1e-15, atol=0.0)


@pytest.mark.parametrize("law, coefficient", [("meszaros", -3.0 / 4.0),
                                              ("comoving", -13.0 / 20.0)])
def test_small_void_fraction_limit_of_volume_average_growth(law, coefficient):
    # First order in f_v of the logarithmic-rate equations (validation report
    # Sec. 4.1): ln g_TS = c f_v0 + O(f_v0^2), c = -3/4 (Meszaros), -13/20
    # (comoving); gamma_w0 -> 1.
    for fv0 in (1e-4, 1e-3):
        g = growth(dimensionless(fv0), law)
        assert g.log_growth_relative_to_volume_average_eds / fv0 == pytest.approx(
            coefficient, rel=0.0, abs=fv0)
        assert g.gamma_w0 == pytest.approx(1.0, rel=0.0, abs=fv0)
        wall = growth(dimensionless(fv0), "wall")
        assert wall.log_growth_relative_to_volume_average_eds / fv0 == pytest.approx(
            -1.0 / 3.0, rel=0.0, abs=fv0)


def test_growth_ordering_meszaros_comoving_wall():
    for fv0 in (0.627, 0.737):
        values = {law: growth(dimensionless(fv0), law).growth_today_photon_normalised
                  for law in LAWS}
        assert values["meszaros"] < values["comoving"] < values["wall"]


def test_early_limit_bias_estimate_is_consistent_with_first_order_tail():
    # The omitted early piece of Eq. (2) is c f_v(t_e) to first order.
    p = PAPER_REFERENCE.tracker_params_gyr
    g = growth(p, "comoving")
    tail = -(13.0 / 20.0) * float(bg.fv(1e-6 * p.t0, p))
    assert g.diagnostic("log_growth_early_limit_linear_bias_estimate") == pytest.approx(
        -tail, rel=1e-3, abs=0.0)


def test_tiny_radius_fails_the_truncation_check():
    # W -> 1 across the k range as R -> 0: the k_max end is no longer
    # negligible and the quadrature fails closed instead of truncating.
    with pytest.raises(ls.LagrangianSigmaNumericalError, match="truncates"):
        ls.conditional_lagrangian_linear_sigma(
            background=BACKGROUNDS["PAPER_REFERENCE"], growth_law=WALL, closure=NA,
            growth_numerics=WALL_CHECKS, early_spectrum=SPEC, radius=explicit_radius(1e-4),
            quadrature=QUADRATURE, density_identity_tolerance=IDENTITY_RTOL, G=1.0)


def test_sigma_decreases_with_radius():
    values = [ls.conditional_lagrangian_linear_sigma(
        background=BACKGROUNDS["PAPER_REFERENCE"], growth_law=WALL, closure=NA,
        growth_numerics=WALL_CHECKS, early_spectrum=SPEC, radius=explicit_radius(r),
        quadrature=QUADRATURE, density_identity_tolerance=IDENTITY_RTOL, G=1.0).linear_sigma
        for r in (4.0, 8.0, 16.0, 32.0)]
    assert all(a > b for a, b in zip(values, values[1:]))


# ------------------------------------------------------------------ API contracts
def _public_functions():
    return [getattr(ls, name) for name in ls.__all__
            if inspect.isfunction(getattr(ls, name))]


def _public_dataclasses():
    return [getattr(ls, name) for name in ls.__all__
            if inspect.isclass(getattr(ls, name)) and dataclasses.is_dataclass(getattr(ls, name))]


def test_every_argument_is_mandatory_and_keyword_only():
    functions = _public_functions()
    assert len(functions) == 9
    for function in functions:
        for parameter in inspect.signature(function).parameters.values():
            assert parameter.kind is inspect.Parameter.KEYWORD_ONLY, (function, parameter)
            assert parameter.default is inspect.Parameter.empty, (function, parameter)
    classes = _public_dataclasses()
    assert len(classes) == 12
    for cls in classes:
        for field in dataclasses.fields(cls):
            assert field.default is dataclasses.MISSING, (cls, field.name)
            assert field.default_factory is dataclasses.MISSING, (cls, field.name)
            assert field.kw_only, (cls, field.name)
    sig = inspect.signature(ls.TimescapeTrackerInput.from_reference_preset)
    assert all(p.kind is inspect.Parameter.KEYWORD_ONLY and p.default is inspect.Parameter.empty
               for p in sig.parameters.values())


@pytest.mark.parametrize("closure", [GrowthSystem.BAROTROPIC, "barotropic", "Barotropic"])
@pytest.mark.parametrize("law", [CGI, WALL])
def test_barotropic_closure_is_refused_citing_1g_a(closure, law):
    with pytest.raises(ls.BarotropicClosureRefusedError,
                       match=r"Hadamard ill-posed.*Phase 1G-A Sec\. 4\.1"):
        ls.conditional_lagrangian_linear_sigma(
            background=BACKGROUNDS["PAPER_REFERENCE"], growth_law=law, closure=closure,
            growth_numerics=CGI_NUMERICS, early_spectrum=SPEC, radius=radius_spec("equal_mass"),
            quadrature=QUADRATURE, density_identity_tolerance=IDENTITY_RTOL, G=1.0)
    with pytest.raises(ls.BarotropicClosureRefusedError):
        ls.timescape_growth_factor(params=dimensionless(0.737), growth_law=law, closure=closure,
                                   numerics=CGI_NUMERICS, G=1.0)


@pytest.mark.parametrize("law, closure, numerics, message", [
    (CGI, NA, CGI_NUMERICS, "requires an explicit CleanPerturbationSystem"),
    (CGI, "comoving", CGI_NUMERICS, "requires an explicit CleanPerturbationSystem"),
    (CGI, GrowthSystem.COMOVING, CGI_NUMERICS, "requires an explicit CleanPerturbationSystem"),
    (WALL, COMOVING, WALL_CHECKS, "pass closure=NOT_APPLICABLE"),
    (WALL, "not_applicable", WALL_CHECKS, "pass closure=NOT_APPLICABLE"),
    (CGI, COMOVING, WALL_CHECKS, "requires VolumeAverageGrowthNumerics"),
    (WALL, NA, CGI_NUMERICS, "requires WallRegionalGrowthChecks"),
    ("volume_average_cgi", COMOVING, CGI_NUMERICS, "explicit GrowthLaw member"),
])
def test_growth_law_closure_and_numerics_must_pair_explicitly(law, closure, numerics, message):
    with pytest.raises(ls.LagrangianSigmaContractError, match=message):
        ls.timescape_growth_factor(params=dimensionless(0.737), growth_law=law, closure=closure,
                                   numerics=numerics, G=1.0)


FORBIDDEN_TOKENS = ("sigma_8", "sigma8", "8hmpc")
NEGATIVE_STATUS_VALUES = {ls.SIGMA8_STATUS, ls.FSIGMA8_STATUS}


def _walk(node, keys, strings):
    if isinstance(node, dict):
        for key, value in node.items():
            keys.append(str(key))
            _walk(value, keys, strings)
    elif isinstance(node, (list, tuple)):
        for value in node:
            _walk(value, keys, strings)
    elif isinstance(node, str):
        strings.append(node)


def test_naming_firewall_of_1d_c_section_19():
    for name in ls.__all__:
        obj = getattr(ls, name)
        if inspect.isfunction(obj) or inspect.isclass(obj):
            assert not any(token in name.lower() for token in FORBIDDEN_TOKENS), name
            for member, _ in inspect.getmembers(obj):
                if not member.startswith("_"):
                    assert not any(t in member.lower() for t in FORBIDDEN_TOKENS), (name, member)
    for law in LAWS:
        keys, strings = [], []
        _walk(anchored("PAPER_REFERENCE", law, "equal_mass").to_json_dict(), keys, strings)
        assert not any(t in key.lower() for key in keys for t in FORBIDDEN_TOKENS)
        flagged = {s for s in strings if any(t in s.lower() for t in FORBIDDEN_TOKENS)}
        assert flagged <= NEGATIVE_STATUS_VALUES, flagged
    assert ls.SIGMA8_STATUS.startswith("NOT_") and ls.FSIGMA8_STATUS.startswith("NOT_")
    # No packaged observational anchor or Planck parameter set.
    for name in vars(ls):
        assert "planck" not in name.lower(), name
        assert not (name.isupper() and "ANCHOR" in name), name


def test_status_tokens_are_fixed_and_authorizations_unchanged():
    result = anchored("PAPER_REFERENCE", "comoving", "equal_mass")
    for record in (result, result.timescape, result.reference):
        assert record.classification == "CONDITIONAL_MODEL_INTERNAL_LINEAR_SIGMA_M"
        assert record.observational_status == "NON_OBSERVATIONAL"
        assert record.amplitude_status == "NOT_OBSERVATIONAL_SIGMA_8"
        assert record.growth_rate_product_status == "NOT_FSIGMA8"
        assert record.early_spectrum_status == "PROVISIONAL_MODEL_IMPORT"
        with pytest.raises(ls.LagrangianSigmaContractError, match="not relabelled"):
            dataclasses.replace(record, observational_status="OBSERVATIONAL")
        with pytest.raises(ls.LagrangianSigmaContractError, match="not relabelled"):
            dataclasses.replace(record, classification="PREDICTION")
    for token in ("SIGMA8_AUTHORIZATION", "FSIGMA8_AUTHORIZATION",
                  "OBSERVATIONAL_AUTHORIZATION", "UNIQUE_TIMESCAPE_PREDICTION"):
        assert getattr(scientific_status, token) == "NOT_GRANTED"
    assert scientific_status.REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING == "NOT_DERIVED"


def test_records_are_frozen_and_arrays_read_only():
    result = anchored("PAPER_REFERENCE", "wall", "equal_mass")
    for record in (result, result.timescape, result.timescape.growth, result.timescape.density,
                   result.timescape.radius, SPEC, QUADRATURE, CGI_NUMERICS, WALL_CHECKS,
                   BACKGROUNDS["NW15_CMB_FIT"], radius_spec("bare"), result.reference):
        with pytest.raises(dataclasses.FrozenInstanceError):
            setattr(record, dataclasses.fields(record)[0].name, None)
    arrays = (ls.top_hat_window(x=np.array([0.0, 1.0])),
              ls.eh98_zero_baryon_transfer(k_per_Mpc=np.array([0.1]), omega_m=0.14,
                                           baryon_fraction=0.15, T_cmb_K=2.7255),
              ls.matter_era_linear_amplitude(k_per_Mpc=np.array([0.1]), early_spectrum=SPEC,
                                             omega_m=0.14, growth_today_photon_normalised=1.0))
    for array in arrays:
        assert not array.flags.writeable
        with pytest.raises(ValueError):
            array[...] = 0.0


def test_result_consistency_is_validated_on_construction():
    result = sigma("PAPER_REFERENCE", "comoving", "equal_mass")
    with pytest.raises(ls.LagrangianSigmaContractError, match="linear_sigma must equal"):
        dataclasses.replace(result, linear_sigma=result.linear_sigma * 1.01)
    with pytest.raises(ls.LagrangianSigmaContractError, match="model_caveat"):
        dataclasses.replace(result, model_caveat="other")
    with pytest.raises(ls.LagrangianSigmaContractError, match="exact background object"):
        dataclasses.replace(result, background=dataclasses.replace(result.background))
    g = result.growth
    with pytest.raises(ls.LagrangianSigmaContractError, match="gamma_w0"):
        dataclasses.replace(g, growth_today_photon_normalised=1.0)
    with pytest.raises(ls.LagrangianSigmaContractError, match="evidence_class"):
        dataclasses.replace(g, evidence_class=ls.WALL_REGIONAL_EVIDENCE_CLASS)
    ratio = anchored("PAPER_REFERENCE", "comoving", "equal_mass")
    with pytest.raises(ls.LagrangianSigmaContractError, match="anchored_linear_sigma"):
        dataclasses.replace(ratio, anchored_linear_sigma=0.9)


def test_json_serialisation_is_deterministic_and_complete():
    result = anchored("NW15_CMB_FIT", "comoving", "dressed")
    first = json.dumps(result.to_json_dict(), sort_keys=True)
    second = json.dumps(anchored("NW15_CMB_FIT", "comoving", "dressed").to_json_dict(),
                        sort_keys=True)
    assert first == second
    payload = json.loads(first)
    ts = payload["timescape"]
    assert ts["frames"] == {"growth_background": "volume_average_D",
                            "radius": "photon_normalised_comoving_Mpc",
                            "mass_label": "lagrangian_omega_m_eff_R3"}
    assert ts["early_spectrum"]["import_status"] == "PROVISIONAL_MODEL_IMPORT"
    assert ts["radius"]["convention_status"] == "CONVENTION_DEPENDENT"
    assert ts["growth"]["closure"] == "comoving"
    assert any("Phase 1G-C" in item for item in ts["limitations"])
    wall = anchored("NW15_CMB_FIT", "wall", "dressed").to_json_dict()["timescape"]
    assert wall["growth"]["closure"] == "NOT_APPLICABLE"
    assert wall["frames"]["growth_background"] == "wall_regional_common_time"


# ------------------------------------------------------------ invalid inputs fail closed
@pytest.mark.parametrize("overrides, message", [
    ({"A_s": 0.0}, "A_s must be positive"),
    ({"A_s": True}, "real scalar"),
    ({"n_s": float("nan")}, "n_s must be finite"),
    ({"k_pivot_per_Mpc": -0.05}, "k_pivot_per_Mpc must be positive"),
    ({"baryon_fraction": 1.0}, r"baryon_fraction must lie in \[0, 1\)"),
    ({"baryon_fraction": -0.1}, r"baryon_fraction must lie in \[0, 1\)"),
    ({"T_cmb_K": 0.0}, "T_cmb_K must be positive"),
    ({"transfer_model": "eisenstein_hu_1998_zero_baryon_oscillation"}, "EarlyTransferModel"),
    ({"import_status": "DERIVED"}, "PROVISIONAL_MODEL_IMPORT"),
    ({"provenance": " "}, "provenance"),
])
def test_invalid_early_spectrum_is_refused(overrides, message):
    with pytest.raises(ls.LagrangianSigmaContractError, match=message):
        early_spectrum(**overrides)


@pytest.mark.parametrize("fields, message", [
    ({"fv0": 0.0}, r"fv0 must lie in \(0, 1\)"),
    ({"fv0": 1.0}, r"fv0 must lie in \(0, 1\)"),
    ({"H0_dressed_km_s_Mpc": -70.0}, "must be positive"),
    ({"H0_dressed_km_s_Mpc": np.inf}, "must be finite"),
    ({"label": ""}, "label"),
])
def test_invalid_background_is_refused(fields, message):
    base = dict(label="x", fv0=0.7, H0_dressed_km_s_Mpc=70.0, source="test")
    base.update(fields)
    with pytest.raises(ls.LagrangianSigmaContractError, match=message):
        ls.TimescapeTrackerInput(**base)


def test_invalid_radius_specs_are_refused():
    C = ls.LagrangianRadiusConvention
    with pytest.raises(ls.LagrangianSigmaContractError, match="required by"):
        ls.LagrangianRadiusSpec(convention=C.DRESSED_WALL_COMOVING_LENGTH,
                                length_h_inverse_Mpc=NA, reference_omega_m=NA,
                                reference_radius_Mpc=NA, explicit_radius_Mpc=NA)
    with pytest.raises(ls.LagrangianSigmaContractError, match="pass NOT_APPLICABLE"):
        ls.LagrangianRadiusSpec(convention=C.DRESSED_WALL_COMOVING_LENGTH,
                                length_h_inverse_Mpc=8.0, reference_omega_m=0.14,
                                reference_radius_Mpc=NA, explicit_radius_Mpc=NA)
    with pytest.raises(ls.LagrangianSigmaContractError, match="pass NOT_APPLICABLE"):
        ls.LagrangianRadiusSpec(convention=C.BARE_VOLUME_AVERAGE_PROPER_LENGTH,
                                length_h_inverse_Mpc=8.0, reference_omega_m=None,
                                reference_radius_Mpc=NA, explicit_radius_Mpc=NA)
    with pytest.raises(ls.LagrangianSigmaContractError, match="must be positive"):
        explicit_radius(-1.0)
    with pytest.raises(ls.LagrangianSigmaContractError, match="LagrangianRadiusConvention"):
        ls.LagrangianRadiusSpec(convention="explicit_photon_normalised_comoving_radius",
                                length_h_inverse_Mpc=NA, reference_omega_m=NA,
                                reference_radius_Mpc=NA, explicit_radius_Mpc=9.0)


@pytest.mark.parametrize("fields, message", [
    ({"grid_points": 16000}, "odd integer"),
    ({"grid_points": 16001.0}, "must be an integer"),
    ({"comparison_grid_points": 16001}, "smaller than grid_points"),
    ({"early_time_fraction": 0.0}, r"early_time_fraction must lie in \(0, 1\)"),
    ({"comparison_early_time_fraction": 1e-7}, "must exceed early_time_fraction"),
    ({"grid_refinement_tolerance": 0.0}, "must be positive"),
    ({"growing_mode": None}, "GrowingModeConfig"),
])
def test_invalid_growth_numerics_are_refused(fields, message):
    base = dict(grid_points=16001, comparison_grid_points=8001, early_time_fraction=1e-6,
                comparison_early_time_fraction=1e-5, grid_refinement_tolerance=1e-7,
                early_limit_tolerance=1e-4, growing_mode=CGI_NUMERICS.growing_mode)
    base.update(fields)
    with pytest.raises(ls.LagrangianSigmaContractError, match=message):
        ls.VolumeAverageGrowthNumerics(**base)


@pytest.mark.parametrize("fields, message", [
    ({"k_max_per_Mpc": 1e-6}, "must exceed k_min_per_Mpc"),
    ({"k_min_per_Mpc": 0.0}, "must be positive"),
    ({"grid_points": 2}, "odd integer"),
    ({"comparison_grid_points": 9001}, "smaller than grid_points"),
    ({"truncation_tolerance": -1.0}, "must be positive"),
])
def test_invalid_quadrature_is_refused(fields, message):
    base = dict(k_min_per_Mpc=1e-6, k_max_per_Mpc=3e2, grid_points=8001,
                comparison_grid_points=4001, self_convergence_tolerance=1e-6,
                truncation_tolerance=1e-8)
    base.update(fields)
    with pytest.raises(ls.LagrangianSigmaContractError, match=message):
        ls.LagrangianSigmaQuadrature(**base)


def test_convergence_and_identity_budgets_fail_closed(monkeypatch):
    tight = dataclasses.replace(CGI_NUMERICS, early_limit_tolerance=1e-9)
    with pytest.raises(ls.LagrangianSigmaNumericalError, match="early-limit change"):
        ls.timescape_growth_factor(params=dimensionless(0.737), growth_law=CGI,
                                   closure=COMOVING, numerics=tight, G=1.0)
    with pytest.raises(ls.LagrangianSigmaNumericalError, match="wall-regional identity"):
        ls.timescape_growth_factor(params=dimensionless(0.737), growth_law=WALL, closure=NA,
                                   numerics=dataclasses.replace(WALL_CHECKS,
                                                                identity_tolerance=1e-18),
                                   G=1.0)
    coarse = dataclasses.replace(QUADRATURE, grid_points=41, comparison_grid_points=21)
    with pytest.raises(ls.LagrangianSigmaNumericalError, match="not converged"):
        ls.lcdm_reference_linear_sigma(recipe=PLANCK_2018_QPLUS_RECIPE, early_spectrum=SPEC,
                                       radius_Mpc=R_LCDM, quadrature=coarse)
    # A corrupted density function must break the closed-form identity.
    original = bg.rho_d
    monkeypatch.setattr(bg, "rho_d", lambda t, p, G: 1.001 * original(t, p, G))
    with pytest.raises(ls.LagrangianSigmaNumericalError, match="identity residual"):
        ls.early_matter_density_per_photon(background=BACKGROUNDS["PAPER_REFERENCE"],
                                           identity_tolerance=IDENTITY_RTOL, G=1.0)


def test_anchor_contracts_fail_closed():
    ts = sigma("PAPER_REFERENCE", "comoving", "equal_mass")
    ref = reference()
    kwargs = dict(anchor_value=ANCHOR, anchor_provenance="fixture",
                  anchor_consistency_tolerance=ANCHOR_TOLERANCE,
                  anchor_consistency_rationale=ANCHOR_RATIONALE)
    other_quadrature = dataclasses.replace(QUADRATURE, grid_points=8003)
    with pytest.raises(ls.LagrangianSigmaContractError, match="same quadrature"):
        ls.anchor_lagrangian_sigma(timescape=ts, reference=ls.lcdm_reference_linear_sigma(
            recipe=PLANCK_2018_QPLUS_RECIPE, early_spectrum=SPEC, radius_Mpc=R_LCDM,
            quadrature=other_quadrature), **kwargs)
    with pytest.raises(ls.LagrangianSigmaContractError, match="T_cmb differs"):
        ls.anchor_lagrangian_sigma(timescape=ts, reference=ls.lcdm_reference_linear_sigma(
            recipe=PLANCK_2018_QPLUS_RECIPE, early_spectrum=early_spectrum(T_cmb_K=2.7),
            radius_Mpc=R_LCDM, quadrature=QUADRATURE), **kwargs)
    with pytest.raises(ls.LagrangianSigmaContractError, match="must match the LCDM reference"):
        ls.anchor_lagrangian_sigma(timescape=ts, reference=ls.lcdm_reference_linear_sigma(
            recipe=PLANCK_2018_QPLUS_RECIPE, early_spectrum=SPEC, radius_Mpc=1.01 * R_LCDM,
            quadrature=QUADRATURE), **kwargs)
    for bad, message in (({"anchor_value": 0.0}, "anchor_value must be positive"),
                         ({"anchor_provenance": ""}, "anchor_provenance"),
                         ({"anchor_consistency_rationale": ""}, "rationale")):
        with pytest.raises(ls.LagrangianSigmaContractError, match=message):
            ls.anchor_lagrangian_sigma(timescape=ts, reference=ref, **{**kwargs, **bad})
    # Non-equal-mass conventions do not tie the radius to the reference.
    dressed = ls.anchor_lagrangian_sigma(
        timescape=sigma("PAPER_REFERENCE", "comoving", "dressed"), reference=ref, **kwargs)
    assert dressed.timescape.radius.spec.convention.value.startswith("dressed")
