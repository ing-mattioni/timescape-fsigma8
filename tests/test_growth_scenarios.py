"""Scenario model tests: enums, serialization, no defaults, applicability."""

# A06: absolute budgets use rtol=0; relative budgets use atol=0.
# Previously implicit algebraic comparisons use rtol=2e-12, atol=1e-14
# in the fixture units (roundoff allowance); explicit convergence budgets remain.

import dataclasses

import numpy as np
import pytest

from timescape_fsigma8.perturbations import EpochChoice, RateUnitConvention
from timescape_fsigma8.perturbations.scenarios import PHASE1C_EPOCH_ROOT
from timescape_fsigma8.growth import (
    DensityContrastMapping,
    GrowthBackgroundPreset,
    GrowthCoordinate,
    GrowthD3Branch,
    GrowthReference,
    GrowthReferenceCoordinate,
    GrowthScenario,
    GrowthSystem,
    GrowthTiltForm,
    GrowthWavenumberConvention,
    resolve_background,
)
from growth_test_utils import barotropic_scenario, clean_scenario


EXPECTED_ENUM_VALUES = {
    GrowthSystem: {"meszaros", "comoving", "barotropic"},
    GrowthBackgroundPreset: {"paper_reference", "notebook_reference"},
    GrowthD3Branch: {"not_applicable", "printed_4_15", "derived_4_10"},
    GrowthTiltForm: {"not_applicable", "unrescaled_V", "rescaled_Vtilde"},
    GrowthWavenumberConvention: {
        "not_applicable",
        "upstream_timescape_k",
        "paper_lcdm_hubble_k",
    },
    GrowthCoordinate: {"bare_aD", "dressed_redshift"},
    DensityContrastMapping: {
        "keep_Delta_d",
        "map_to_delta_m_via_minus_k_code2",
    },
    GrowthReferenceCoordinate: {"bare_time_solver_units", "dressed_redshift"},
}


def test_every_scenario_enum_value_is_exactly_the_required_label():
    for enum_type, expected in EXPECTED_ENUM_VALUES.items():
        assert {member.value for member in enum_type} == expected, enum_type


def test_scenario_serialization_round_trips_every_field():
    scenario = barotropic_scenario(
        GrowthD3Branch.PRINTED_4_15, 2.0 * np.pi, "2pi"
    )
    meta = scenario.to_metadata()
    assert meta["perturbation_system"] == "barotropic"
    assert meta["d3_branch"] == "printed_4_15"
    assert meta["tilt_form"] == "unrescaled_V"
    assert meta["rate_unit_convention"] == "upstream_unconverted"
    assert meta["epoch_choice"] == "upstream_0p218_gyr"
    assert meta["wavenumber_convention"] == "upstream_timescape_k"
    assert meta["growth_coordinate"] == "bare_aD"
    assert meta["density_contrast_mapping"] == "keep_Delta_d"
    assert meta["supplied_mode_k"] == pytest.approx(2.0 * np.pi, rel=2e-12, abs=1e-14)
    assert meta["mode_label"] == "2pi"
    assert "system=barotropic" in scenario.identifier
    assert "d3=printed_4_15" in scenario.identifier


def test_scenario_has_no_scientific_field_defaults():
    for field in dataclasses.fields(GrowthScenario):
        assert field.default is dataclasses.MISSING, field.name
        assert field.default_factory is dataclasses.MISSING, field.name


def test_growth_reference_has_no_defaults():
    for field in dataclasses.fields(GrowthReference):
        assert field.default is dataclasses.MISSING, field.name


def test_scenario_is_immutable():
    scenario = clean_scenario(GrowthSystem.MESZAROS)
    with pytest.raises(dataclasses.FrozenInstanceError):
        scenario.growth_coordinate = GrowthCoordinate.DRESSED_REDSHIFT


@pytest.mark.parametrize(
    "kwargs, match",
    [
        # real D3 branch for a clean system
        (dict(d3_branch=GrowthD3Branch.PRINTED_4_15), "d3_branch=not_applicable"),
        # real tilt form for a clean system
        (dict(tilt_form=GrowthTiltForm.UNRESCALED_V), "tilt_form=not_applicable"),
        # real wavenumber convention for a clean scale-independent run
        (
            dict(
                wavenumber_convention=(
                    GrowthWavenumberConvention.UPSTREAM_TIMESCAPE_K
                )
            ),
            "wavenumber_convention",
        ),
    ],
)
def test_clean_system_rejects_barotropic_only_choices(kwargs, match):
    base = clean_scenario(GrowthSystem.COMOVING).to_metadata()
    fields = dict(
        perturbation_system=GrowthSystem.COMOVING,
        background_preset=GrowthBackgroundPreset.NOTEBOOK_REFERENCE,
        d3_branch=GrowthD3Branch.NOT_APPLICABLE,
        tilt_form=GrowthTiltForm.NOT_APPLICABLE,
        rate_unit_convention=RateUnitConvention.UPSTREAM_UNCONVERTED,
        epoch_choice=EpochChoice.UPSTREAM_0P218_GYR,
        wavenumber_convention=GrowthWavenumberConvention.NOT_APPLICABLE,
        growth_coordinate=GrowthCoordinate.BARE_AD,
        density_contrast_mapping=DensityContrastMapping.KEEP_DELTA_D,
        supplied_mode_k=None,
        mode_label=None,
    )
    fields.update(kwargs)
    with pytest.raises(ValueError, match=match):
        GrowthScenario(**fields)
    assert base["d3_branch"] == "not_applicable"


@pytest.mark.parametrize(
    "kwargs, match",
    [
        (dict(d3_branch=GrowthD3Branch.NOT_APPLICABLE), "real d3_branch"),
        (dict(tilt_form=GrowthTiltForm.NOT_APPLICABLE), "real tilt_form"),
        (
            dict(
                wavenumber_convention=GrowthWavenumberConvention.NOT_APPLICABLE
            ),
            "real wavenumber_convention",
        ),
        (dict(supplied_mode_k=None, mode_label=None), "supplied_mode_k"),
    ],
)
def test_barotropic_rejects_missing_mandatory_choices(kwargs, match):
    fields = dict(
        perturbation_system=GrowthSystem.BAROTROPIC,
        background_preset=GrowthBackgroundPreset.NOTEBOOK_REFERENCE,
        d3_branch=GrowthD3Branch.PRINTED_4_15,
        tilt_form=GrowthTiltForm.UNRESCALED_V,
        rate_unit_convention=RateUnitConvention.UPSTREAM_UNCONVERTED,
        epoch_choice=EpochChoice.UPSTREAM_0P218_GYR,
        wavenumber_convention=GrowthWavenumberConvention.UPSTREAM_TIMESCAPE_K,
        growth_coordinate=GrowthCoordinate.BARE_AD,
        density_contrast_mapping=DensityContrastMapping.KEEP_DELTA_D,
        supplied_mode_k=2.0 * np.pi,
        mode_label="2pi",
    )
    fields.update(kwargs)
    with pytest.raises(ValueError, match=match):
        GrowthScenario(**fields)


@pytest.mark.parametrize("bad_k", [0.0, -1.0, np.nan, np.inf])
def test_nonfinite_or_zero_mode_k_is_rejected(bad_k):
    with pytest.raises(ValueError, match="finite and positive"):
        barotropic_scenario(GrowthD3Branch.PRINTED_4_15, bad_k, "bad")


def test_string_lookalikes_are_rejected_for_every_enum_field():
    with pytest.raises(ValueError, match="explicit GrowthSystem"):
        GrowthScenario(
            perturbation_system="meszaros",
            background_preset=GrowthBackgroundPreset.NOTEBOOK_REFERENCE,
            d3_branch=GrowthD3Branch.NOT_APPLICABLE,
            tilt_form=GrowthTiltForm.NOT_APPLICABLE,
            rate_unit_convention=RateUnitConvention.UPSTREAM_UNCONVERTED,
            epoch_choice=EpochChoice.UPSTREAM_0P218_GYR,
            wavenumber_convention=GrowthWavenumberConvention.NOT_APPLICABLE,
            growth_coordinate=GrowthCoordinate.BARE_AD,
            density_contrast_mapping=DensityContrastMapping.KEEP_DELTA_D,
            supplied_mode_k=None,
            mode_label=None,
        )


def test_clean_mapping_requires_explicit_harmonic_k():
    with pytest.raises(ValueError, match="harmonic"):
        clean_scenario(
            GrowthSystem.COMOVING,
            mapping=DensityContrastMapping.MAP_TO_DELTA_M_VIA_MINUS_K_CODE2,
        )


def test_clean_mode_k_without_mapping_is_rejected():
    with pytest.raises(ValueError, match="supplied_mode_k only together"):
        clean_scenario(GrowthSystem.MESZAROS, mode_k=7.0, mode_label="test")


def test_mode_label_required_with_mode_k_and_vice_versa():
    with pytest.raises(ValueError, match="mode_label"):
        clean_scenario(
            GrowthSystem.MESZAROS,
            mapping=DensityContrastMapping.MAP_TO_DELTA_M_VIA_MINUS_K_CODE2,
            mode_k=7.0,
            mode_label=None,
        )


def test_reference_validation():
    with pytest.raises(ValueError, match="positive"):
        GrowthReference(
            coordinate=GrowthReferenceCoordinate.BARE_TIME_SOLVER_UNITS,
            value=-1.0,
            root=PHASE1C_EPOCH_ROOT,
            amplitude_floor_rel=1e-10,
        )
    with pytest.raises(ValueError, match="amplitude_floor_rel"):
        GrowthReference(
            coordinate=GrowthReferenceCoordinate.DRESSED_REDSHIFT,
            value=10.0,
            root=PHASE1C_EPOCH_ROOT,
            amplitude_floor_rel=2.0,
        )


def test_background_presets_resolve_to_frozen_phase1b_parameters():
    nb = resolve_background(GrowthBackgroundPreset.NOTEBOOK_REFERENCE)
    pp = resolve_background(GrowthBackgroundPreset.PAPER_REFERENCE)
    assert nb.params.fv0 == 0.737 and pp.params.fv0 == 0.737
    assert nb.params.H0_dressed == pytest.approx(1.0, rel=1e-12, abs=0.0)
    assert nb.timescape_h == pytest.approx(0.7323, rel=2e-12, abs=1e-14)
    assert pp.timescape_h == pytest.approx(0.7303, rel=2e-12, abs=1e-14)
    assert nb.lcdm_h == pytest.approx(0.674, rel=2e-12, abs=1e-14)
    assert nb.time_unit.target_time_per_gyr == pytest.approx(0.7323 / 9.778, rel=2e-12, abs=1e-14)
    assert pp.time_unit.target_time_per_gyr == pytest.approx(0.7303 / 9.778, rel=2e-12, abs=1e-14)
