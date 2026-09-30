"""Regression for the Phase 1G-A owner decisions GA-OD1 to GA-OD4 (2026-09-30).

Record: reports/phase1g_a_owner_decisions_successor.md and its inventory.
Findings: reports/phase1g_a_adversarial_audit.md (GA-F1 to GA-F11).
Tolerances: see tests/phase1g_owner_decisions_test_utils.py.
"""

from __future__ import annotations

from phase1g_owner_decisions_test_utils import (
    PHASE1G_TOKENS,
    PROJECT_ROOT,
    check_quoted_numbers,
    check_record,
)

from timescape_fsigma8 import scientific_status
from timescape_fsigma8.scientific_status import CURRENT_SCIENTIFIC_STATUS

TICKS = {
    "GA-OD1": "[x] Accept: record it as convention-dependent, qualify \"only the comoving closure "
              "(and Mészáros) can define a linear σ\", and add an author question on the (B.4) sign.",
    "GA-OD2": "[x] (i) Keep the Planck early universe as a declared hybrid primary. Correct the f_b "
              "justification and add [NW15]'s own inputs as a sensitivity (σ 0.637–0.645; wall law "
              "0.89–0.90).",
    "GA-OD3": "[x] Name the unit chain, give 557–694 under the report's own radius conventions, "
              "and keep the test pin with a comment naming the chain.",
    "GA-OD4": "[x] Accept all, in one successor note.",
}
UNTICKED = [
    "[ ] (ii) Switch the [NW15] primary to [NW15]'s own inputs and propagate the change to the "
    "1G-C, 1G-E and 1G-F quotes and to CLAUDE.md.",
]


def test_record_is_canonical_carries_the_ticks_and_pins_the_frozen_files():
    record = check_record("a", TICKS, UNTICKED, comments_changed=[])
    assert record["decisions"]["GA-OD1"]["classification_current"] == "CONVENTION_DEPENDENT"
    assert "B.4" in record["author_questions"][0]


def test_token_values_are_unchanged():
    for token, value in PHASE1G_TOKENS.items():
        assert CURRENT_SCIENTIFIC_STATUS[token] == value
        assert getattr(scientific_status, token) == value
    assert scientific_status.D3_VERDICT == "RESOLVED_DERIVED_4_10"


def test_ga_od3_test_pin_is_kept_and_its_comment_names_the_chain():
    source = (PROJECT_ROOT / "tests" / "test_barotropic_hadamard_refutation.py").read_text(encoding="utf-8")
    assert "EXPONENT_KR1_R8_1G_A = 875.4" in source
    assert "EXPONENT_KR1_R8_ATOL = 0.05" in source
    assert "(1D-A Sec. 10 unit chain, as in [1G-A])" not in source
    assert "hybrid chain" in source and "k_phys0_D" in source
    assert "557.4 / 639.7 / 693.5" in source


def test_quoted_numbers_equal_the_evidence_artifact():
    check_quoted_numbers("a")
