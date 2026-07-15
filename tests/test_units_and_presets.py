"""Audited unit conversions and immutable presets.

Tolerances (AGENTS.md rule 9): conversions among exact-by-definition
constants are tested at rtol 1e-12 (rounding only); comparisons against
externally *quoted* values use the precision of the quote.
"""

import dataclasses
import math

import pytest

from timescape_fsigma8 import units
from timescape_fsigma8.background import TrackerParams, H_dressed
from timescape_fsigma8.presets import (
    NOTEBOOK_REFERENCE,
    PAPER_REFERENCE,
    ReferencePreset,
)

RTOL = 1e-12


# ---------------------------------------------------------------------
# units.py: primary constants and conversions
# ---------------------------------------------------------------------

def test_primary_constants_exact():
    assert units.AU_KM == 149_597_870.700          # IAU 2012 B2, exact
    assert units.DAY_S == 86_400.0                 # exact
    assert units.JULIAN_YEAR_S == 31_557_600.0     # 365.25 * 86400, exact
    assert units.GYR_S == 3.15576e16               # exact


def test_megaparsec_matches_iau_quoted_value():
    """Derived Mpc vs the IAU/CODATA quoted 3.0856775814913673e19 km."""
    assert units.MPC_KM == pytest.approx(3.0856775814913673e19, rel=1e-15)
    assert units.PC_KM == pytest.approx(units.AU_KM * 648000.0 / math.pi, rel=0)


def test_round_trips():
    for H in (0.07, 73.23, 100.0):
        assert units.per_gyr_to_kms_per_mpc(
            units.kms_per_mpc_to_per_gyr(H)) == pytest.approx(H, rel=RTOL)
        assert units.per_s_to_per_gyr(
            units.per_gyr_to_per_s(H)) == pytest.approx(H, rel=RTOL)


def test_kms_per_mpc_chain_consistency():
    """km/s/Mpc -> s^-1 -> Gyr^-1 equals the direct conversion."""
    H = 73.23
    via_s = units.per_s_to_per_gyr(units.kms_per_mpc_to_per_s(H))
    assert via_s == pytest.approx(units.kms_per_mpc_to_per_gyr(H), rel=RTOL)


def test_reference_conversion_values():
    """H0 = 100 km/s/Mpc = 3.240779e-18 s^-1; Hubble time 9.777922 Gyr."""
    assert units.kms_per_mpc_to_per_s(100.0) == pytest.approx(3.2407792894443648e-18, rel=1e-12)
    assert units.HUBBLE_TIME_GYR_AT_H100 == pytest.approx(9.77792222, rel=1e-8)


def test_upstream_9778_is_approximation_only():
    """The upstream 9.778 Gyr Hubble-time convention differs from the exact
    value by ~8e-6 relative — documented comparison, not used in conversions."""
    exact = units.HUBBLE_TIME_GYR_AT_H100
    rel = abs(units.UPSTREAM_HUBBLE_TIME_GYR_AT_H100 - exact) / exact
    assert 1e-6 < rel < 1e-4


# ---------------------------------------------------------------------
# presets.py: immutability, derivation, units
# ---------------------------------------------------------------------

def test_preset_values():
    assert PAPER_REFERENCE.fv0 == 0.737
    assert PAPER_REFERENCE.H0_dressed_km_s_Mpc == 73.03
    assert NOTEBOOK_REFERENCE.fv0 == 0.737
    assert NOTEBOOK_REFERENCE.H0_dressed_km_s_Mpc == 73.23


def test_presets_are_immutable():
    for preset in (PAPER_REFERENCE, NOTEBOOK_REFERENCE):
        with pytest.raises(dataclasses.FrozenInstanceError):
            preset.fv0 = 0.5  # type: ignore[misc]


@pytest.mark.parametrize("preset", [PAPER_REFERENCE, NOTEBOOK_REFERENCE],
                         ids=lambda p: p.name)
def test_HD0_is_derived_not_inserted(preset: ReferencePreset):
    """HD0 comes from the dressed-to-bare relation ([GM] p. 25) applied to
    the stored dressed H0 — in both km/s/Mpc and Gyr^-1 forms."""
    f, H0 = preset.fv0, preset.H0_dressed_km_s_Mpc
    expected = 2.0 * H0 * (2.0 + f) / (4.0 * f**2 + f + 4.0)
    assert preset.HD0_bare_km_s_Mpc == pytest.approx(expected, rel=1e-15)
    p_gyr = preset.tracker_params_gyr
    assert p_gyr.HD0 == pytest.approx(
        units.kms_per_mpc_to_per_gyr(expected), rel=1e-14)
    # round trip: the TrackerParams' dressed H0 reproduces the preset value
    assert units.per_gyr_to_kms_per_mpc(p_gyr.H0_dressed) == pytest.approx(
        preset.H0_dressed_km_s_Mpc, rel=1e-14)


def test_bare_H0_reference_values():
    """[GM] p. 25 quotes H_D,0 ~ 58.01 km/s/Mpc — reproduced by the
    NOTEBOOK preset (73.23); the PAPER preset (73.03) gives 57.86,
    which is the H0-discrepancy evidence of the Phase 1A/1B audits."""
    assert NOTEBOOK_REFERENCE.HD0_bare_km_s_Mpc == pytest.approx(58.01, abs=0.005)
    assert PAPER_REFERENCE.HD0_bare_km_s_Mpc == pytest.approx(57.86, abs=0.005)


@pytest.mark.parametrize("preset", [PAPER_REFERENCE, NOTEBOOK_REFERENCE],
                         ids=lambda p: p.name)
def test_tracker_params_gyr_units(preset: ReferencePreset):
    """tracker_params_gyr yields Gyr units: t0 ~ 15.4 Gyr and
    H_dressed(t0) equals the preset's dressed H0 in Gyr^-1."""
    p = preset.tracker_params_gyr
    assert isinstance(p, TrackerParams)
    assert 15.0 < p.t0 < 15.8   # volume-average age in Gyr
    assert float(H_dressed(p.t0, p)) == pytest.approx(
        preset.H0_dressed_per_gyr, rel=1e-14)


def test_notebook_preset_age_matches_phase1a_value():
    """Phase 1A audit: t0 ~ 15.38 Gyr with the notebook conversions.
    With audited (exact) conversions the value differs only in the 5th
    digit (upstream used the 9.778 approximation)."""
    assert NOTEBOOK_REFERENCE.tracker_params_gyr.t0 == pytest.approx(15.38, abs=0.01)
