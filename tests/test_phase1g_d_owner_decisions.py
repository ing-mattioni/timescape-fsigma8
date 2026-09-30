"""Regression for the Phase 1G-D owner decisions GD-OD1 to GD-OD7 (2026-09-30).

Record: reports/phase1g_d_owner_decisions_successor.md and its inventory.
Findings: reports/phase1g_d_adversarial_audit.md (GD-F1 to GD-F10).  Two
token comments change (GD-OD5, GD-OD7); no value.  The recomputed void
response is checked against the evidence artifact
(scripts/phase1g_owner_decisions_numerics.py).  Tolerances: see
tests/phase1g_owner_decisions_test_utils.py.
"""

from __future__ import annotations

from phase1g_owner_decisions_test_utils import (
    PHASE1G_TOKENS,
    check_quoted_numbers,
    check_record,
    status_source,
)

from timescape_fsigma8.scientific_status import CURRENT_SCIENTIFIC_STATUS

TICKS = {
    "GD-OD1": "[x] Tracker-consistent primary, `R_seed = R_void (f_vi/f_v0)^{1/3}/γ_w0`, giving "
              "A_v σ(R8) 1.05–1.5 and X_SU 1.30–1.63. Quote the [SvdW04]-factor values as the "
              "alternative.",
    "GD-OD2": "[x] Restrict f_vi to the tracker's f_v(t_LS): 9.47e−5 ([GM]) and 5.07e−5 ([NW15]).",
    "GD-OD3": "[x] Reclassify the SU-mode identification as `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` "
              "(S1), cite [GM] l. 620, and condition the headline and the X_SU lower bound on S1.",
    "GD-OD4": "[x] Reword \"[W09] internally inconsistent\" as the auditor proposes.",
    "GD-OD5": "[x] Correct the Mészáros/barotropic characterisation in the report, the inventory "
              "and the `GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY` comment. The value is "
              "unchanged.",
    "GD-OD6": "[x] Total contrast at last scattering.",
    "GD-OD7": "[x] Recompute σ_LSS(R8) at [NW15]'s own radius (12.226 Mpc) in the new numerics "
              "script, and update the \"2.6–4.3\" token comment accordingly.",
}
UNTICKED = [
    "[ ] Keep the [SvdW04] factor as an explicit additional assumption, and quote both ranges.",
    "[ ] In either case, rebase the rationale comment of `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` "
    "on the \"R8 < R_void partition\" argument. The value is unchanged.",
    "[ ] Keep 10⁻², marked as outside the tracker.",
    "[ ] Wall-mode amplitude.",
]


def test_record_is_canonical_carries_the_ticks_and_pins_the_frozen_files():
    record = check_record("d", TICKS, UNTICKED, comments_changed=[
        "GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY", "LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC"])
    decisions = record["decisions"]
    assert decisions["GD-OD1"]["primary_seed"] == "tracker_consistent"
    assert decisions["GD-OD2"]["f_vi"] == "f_v(t_LS)"
    assert decisions["GD-OD3"]["identification_class"] == "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
    assert decisions["GD-OD6"]["delta_L"] == "total_contrast_at_last_scattering"


def test_token_comments_changed_as_ticked_and_values_are_unchanged():
    source = status_source()
    # GD-OD5: Meszaros is delta Q = 0; no growing SU mode satisfies it or the barotropic closure.
    assert "Meszaros (Delta_eff = 0)" not in source
    assert "iff delta Q = 0" in source and "no\n# growing separate-universe mode" in source
    # GD-OD7: the void-response figure at each case's own equal-mass R8.
    assert "A_v sigma_LSS(R8) = 2.6-4.3 for the peak-background split" not in source
    assert "1.05-1.11" in source and "3.8-4.6" in source and "own equal-mass R8" in source
    # The rationale is not rebased (that GD-OD1 sub-option is unticked).
    assert "R8 < R_void" not in source
    for token, value in PHASE1G_TOKENS.items():
        assert CURRENT_SCIENTIFIC_STATUS[token] == value


def test_quoted_numbers_equal_the_evidence_artifact():
    check_quoted_numbers("d")
