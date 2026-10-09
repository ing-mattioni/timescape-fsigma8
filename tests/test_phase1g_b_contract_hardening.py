"""Phase 1G-B contract-hardening successor (2026-10-09).

Finding GH-D3F4 of the third 1G-H delta audit: ``LCDMReferenceLinearSigma``
accepted non-finite quadrature diagnostics and ``AnchoredLagrangianSigmaRatio``
accepted derived factors unrelated to its stored records.  Both now validate
these fields against the expressions of their factories; computed values are
unchanged.  Record: reports/phase1g_b_contract_hardening_successor.md.
"""

from __future__ import annotations

import dataclasses
import json
import math
from decimal import Decimal
from functools import lru_cache

import pytest

import timescape_fsigma8.lagrangian_sigma as ls
from timescape_fsigma8.perturbations.growing_mode import CleanPerturbationSystem
from timescape_fsigma8.perturbations.initial_conditions import PLANCK_2018_QPLUS_RECIPE
from timescape_fsigma8.presets import PAPER_REFERENCE

NA = ls.NOT_APPLICABLE
QUADRATURE = ls.LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE
BACKGROUND = ls.TimescapeTrackerInput.from_reference_preset(preset=PAPER_REFERENCE)
OMEGA_M_LCDM = PLANCK_2018_QPLUS_RECIPE.omega_m * PLANCK_2018_QPLUS_RECIPE.h ** 2
SPEC = ls.EarlySpectrumImport(
    A_s=2.100e-9, n_s=0.9649, k_pivot_per_Mpc=0.05, baryon_fraction=0.02237 / OMEGA_M_LCDM,
    T_cmb_K=2.7255, transfer_model=ls.EarlyTransferModel.EH98_ZERO_BARYON_OSCILLATION,
    provenance="Planck 2018 (test)", import_status=ls.EARLY_SPECTRUM_IMPORT_STATUS)
R_LCDM = 8.0 / PLANCK_2018_QPLUS_RECIPE.h


@lru_cache(maxsize=None)
def reference() -> ls.LCDMReferenceLinearSigma:
    return ls.lcdm_reference_linear_sigma(recipe=PLANCK_2018_QPLUS_RECIPE, early_spectrum=SPEC,
                                          radius_Mpc=R_LCDM, quadrature=QUADRATURE)


@lru_cache(maxsize=None)
def anchored() -> ls.AnchoredLagrangianSigmaRatio:
    timescape = ls.conditional_lagrangian_linear_sigma(
        background=BACKGROUND, growth_law=ls.GrowthLaw.WALL_REGIONAL_EDS_COMMON_TIME,
        closure=NA, growth_numerics=ls.WALL_REGIONAL_GROWTH_REFERENCE_CHECKS,
        early_spectrum=dataclasses.replace(SPEC, n_s=0.97), radius=ls.LagrangianRadiusSpec(
            convention=ls.LagrangianRadiusConvention.EXPLICIT_PHOTON_NORMALISED_RADIUS,
            length_h_inverse_Mpc=NA, reference_omega_m=NA, reference_radius_Mpc=NA,
            explicit_radius_Mpc=10.0),
        quadrature=QUADRATURE, density_identity_tolerance=1e-13, G=1.0)
    return ls.anchor_lagrangian_sigma(
        timescape=timescape, reference=reference(), anchor_value=reference().linear_sigma,
        anchor_provenance="the reference itself (test fixture)",
        anchor_consistency_tolerance=1e-12, anchor_consistency_rationale="test fixture")


def test_genuine_records_are_accepted_unchanged():
    for record in (reference(), anchored()):
        assert dataclasses.replace(record) == record
        json.dumps(record.to_json_dict(), allow_nan=False)
    assert anchored().early_spectrum_differences == ("n_s",)


@pytest.mark.parametrize("field", ["quadrature_relative_change", "truncation_envelope_fraction"])
@pytest.mark.parametrize("value, message", [
    (float("nan"), "must be finite"), (float("inf"), "must be finite"),
    (float("-inf"), "must be finite"), (-1e-12, "must be nonnegative"),
    (Decimal("0"), "must be a real scalar")])
def test_lcdm_reference_diagnostics_must_be_finite_and_nonnegative(field, value, message):
    with pytest.raises(ls.LagrangianSigmaContractError, match=message):
        dataclasses.replace(reference(), **{field: value})


def test_lcdm_reference_diagnostics_are_bound_to_the_quadrature():
    ref = reference()
    for field, value in (("quadrature_relative_change", 2.0 * ref.quadrature_relative_change + 1e-15),
                         ("quadrature_relative_change", 2.0 * QUADRATURE.self_convergence_tolerance),
                         ("truncation_envelope_fraction", 2.0 * QUADRATURE.truncation_tolerance)):
        with pytest.raises(ls.LagrangianSigmaContractError, match="quadrature diagnostics"):
            dataclasses.replace(ref, **{field: value})


@pytest.mark.parametrize("field", ["growth_ratio", "early_spectrum_factor",
                                   "reference_offset_from_anchor"])
def test_anchored_ratio_factors_are_bound_to_the_stored_records(field):
    record = anchored()
    with pytest.raises(ls.LagrangianSigmaContractError, match="must be the ratios"):
        dataclasses.replace(record, **{field: getattr(record, field) * (1.0 + 1e-9) + 1e-12})


def test_anchored_ratio_refuses_a_consistent_but_unbound_sigma_ratio():
    """The audit's factor-999 probe, kept consistent with anchored_linear_sigma."""
    record = anchored()
    sigma_ratio = 999.0
    with pytest.raises(ls.LagrangianSigmaContractError, match="must be the ratios"):
        dataclasses.replace(record, sigma_ratio=sigma_ratio,
                            anchored_linear_sigma=sigma_ratio * record.anchor_value)
    for field in ("growth_ratio", "early_spectrum_factor"):
        with pytest.raises(ls.LagrangianSigmaContractError, match="must be the ratios"):
            dataclasses.replace(record, **{field: 999.0})


def test_anchored_ratio_names_exactly_the_differing_early_spectrum_inputs():
    with pytest.raises(ls.LagrangianSigmaContractError, match="early_spectrum_differences"):
        dataclasses.replace(anchored(), early_spectrum_differences=())
    with pytest.raises(ls.LagrangianSigmaContractError, match="early_spectrum_differences"):
        dataclasses.replace(anchored(), early_spectrum_differences=("n_s", "A_s"))


def test_the_decomposition_holds_to_rounding():
    record = anchored()
    assert record.sigma_ratio == pytest.approx(record.growth_ratio * record.early_spectrum_factor,
                                               rel=1e-14, abs=0.0)


@pytest.mark.parametrize("field", ["growth_ratio", "early_spectrum_factor",
                                   "reference_offset_from_anchor"])
def test_anchored_ratio_binding_of_native_floats_is_exact_to_one_ulp(field):
    """A native float one ULP away from the factory expression is refused.

    The equalities are exact for native floats (fourth delta audit, mutant X11;
    the owner kept this policy, option (a) of 2026-10-09). A numpy.float32
    rounding is a separate, documented limit (successor record, Sec. 3).
    """
    record = anchored()
    value = getattr(record, field)
    for changed in (math.nextafter(value, math.inf), math.nextafter(value, -math.inf)):
        with pytest.raises(ls.LagrangianSigmaContractError, match="must be the ratios"):
            dataclasses.replace(record, **{field: changed})


def test_lcdm_relative_change_binding_of_native_floats_is_exact_to_one_ulp():
    ref = reference()
    value = ref.quadrature_relative_change
    for changed in (math.nextafter(value, math.inf), math.nextafter(value, -math.inf)):
        with pytest.raises(ls.LagrangianSigmaContractError, match="quadrature diagnostics"):
            dataclasses.replace(ref, quadrature_relative_change=changed)
