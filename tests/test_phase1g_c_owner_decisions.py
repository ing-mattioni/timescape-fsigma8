"""Regression for the Phase 1G-C owner decisions GC-OD1 to GC-OD7 (2026-09-30).

Record: reports/phase1g_c_owner_decisions_successor.md and its inventory.
Findings: reports/phase1g_c_adversarial_audit.md (GC-F1 to GC-F9).  All
decisions are text only; the one code-side change is the comment of
TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW (GC-OD3).  Every comparison here
is exact.
"""

from __future__ import annotations

from phase1g_owner_decisions_test_utils import PHASE1G_TOKENS, check_record, status_source

from timescape_fsigma8.scientific_status import CURRENT_SCIENTIFIC_STATUS

TICKS = {
    "GC-OD1": "[x] Accept, and withdraw \"supersedes … for σ8-scale statistics\".",
    "GC-OD2": "[x] Split the evidence class: kinematics `VERIFIED_FROM_PRIMARY_SOURCE` (+ derived); "
              "dynamics `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`. Align CLAUDE.md and README.",
    "GC-OD3": "[x] Add assumption A5 (\"the wall matter clocks the common time t\") to Secs. 5–6 and "
              "to the `TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW` comment. The value is unchanged.",
    "GC-OD4": "[x] Extend the superseded-readings table and qualify CLAUDE.md and README.",
    "GC-OD5": "[x] drop the \"0.83–0.96 / +3% to +18%\" envelope; or",
    "GC-OD6-OD7": "[x] Describe the checks as \"algebraic consistency checks\", and apply the "
                  "governance and wording changes.",
}
UNTICKED = ["[ ] Accept, and keep \"supersedes\" in narrowed form.", "[ ] add a wall-adapted convention."]


def test_record_is_canonical_carries_the_ticks_and_pins_the_frozen_files():
    record = check_record("c", TICKS, UNTICKED,
                          comments_changed=["TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW"])
    assert record["decisions"]["GC-OD1"]["supersedes_withdrawn"] is True
    assert record["decisions"]["GC-OD3"]["assumption_added"] == "A5"
    assert record["decisions"]["GC-OD5"]["envelope_dropped"] == ["0.83–0.96", "+3% to +18%"]


def test_gc_od3_the_wall_law_comment_names_a5_and_the_value_is_unchanged():
    source = status_source()
    assert "assumptions A1-A5" in source
    assert "the wall matter clocks the common time t" in source
    assert "A1-A4" not in source
    for token, value in PHASE1G_TOKENS.items():
        assert CURRENT_SCIENTIFIC_STATUS[token] == value
