"""Regression for the Phase 1G-E owner decisions GE-OD1 to GE-OD6 (2026-09-30).

Record: reports/phase1g_e_owner_decisions_successor.md and its inventory.
Findings: reports/phase1g_e_adversarial_audit.md (GE-F1 to GE-F7).  No token
value or comment changes; the recorded meaning of
TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC is corrected in the record (GE-OD6).
Tolerances: see tests/phase1g_owner_decisions_test_utils.py.
"""

from __future__ import annotations

from phase1g_owner_decisions_test_utils import (
    PHASE1G_TOKENS,
    check_quoted_numbers,
    check_record,
)

from timescape_fsigma8.scientific_status import CURRENT_SCIENTIFIC_STATUS

TICKS = {
    "GE-OD1": "[x] Adopt `σ² = δ_v²σ²_part + (f_w − f_v δ_v)²σ²_int`. Update the δ_v table "
              "(−0.8: 1.298/1.142), the \"−9%\" reading and the range (0.9–2.1 becomes 0.8–2.1).",
    "GE-OD2": "[x] Adopt the 1G-F derived population as the reference (σ ≈ 0.99) and relabel the "
              "single 15 h⁻¹ Mpc radius as an idealisation.",
    "GE-OD3": "[x] photon-frame compression `s = D_wall` as primary (σ = 1.759 / 1.523 at a = 15);",
    "GE-OD4": "[x] Report the equal-mass values (1.437/1.419) beside convention (b).",
    "GE-OD5": "[x] Restate the precision as the scatter across seeds, and correct the first-run "
              "sentence.",
    "GE-OD6": "[x] Record the four corrections of the audit's Sec. 4.8 in a successor note. The "
              "value is unchanged.",
}
UNTICKED = [
    "[ ] Restrict 1G-E to δ_v = −1.",
    "[ ] Keep the single radius as an explicit idealisation, not attributed to [W09].",
    "[ ] Use the auditor's [W09]-consistent population (σ ≈ 1.0–1.2).",
    "[ ] keep `s = f_w^{1/3}` with its frame stated.",
    "[ ] Justify (b) for the Planck comparison.",
]


def test_record_is_canonical_carries_the_ticks_and_pins_the_frozen_files():
    record = check_record("e", TICKS, UNTICKED, comments_changed=[])
    decisions = record["decisions"]
    assert decisions["GE-OD1"]["formula"] == "sigma^2 = delta_v^2 sigma_part^2 + (f_w - f_v delta_v)^2 sigma_int^2"
    assert decisions["GE-OD3"]["primary_compression"] == "s = D_wall (photon frame)"
    token = record["token_meaning_successor"]["TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC"]
    assert token["value"] == "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
    assert sorted(token["corrections"]) == ["1_formula", "2_E2_idealisation", "3_E4_sensitivity", "4_hybrid"]


def test_token_values_are_unchanged():
    for token, value in PHASE1G_TOKENS.items():
        assert CURRENT_SCIENTIFIC_STATUS[token] == value


def test_quoted_numbers_equal_the_evidence_artifact():
    check_quoted_numbers("e")
