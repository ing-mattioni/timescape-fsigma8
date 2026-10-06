"""Shared helpers for the Phase 1G owner-decisions regressions (2026-09-30).

Used by tests/test_phase1g_{a,c,d,e}_owner_decisions.py.  Successor records:
reports/phase1g_{a,c,d,e}_owner_decisions_successor.md and their canonical
inventories.  Evidence: scripts/phase1g_owner_decisions_numerics.py, whose
git-ignored artifact artifacts/independent/phase1g_owner_decisions.json is
optional (its checks skip when it is absent, as the other generated-artifact
tests do).

Tolerances: a number quoted in a record is compared with the artifact at
half a unit of its last recorded digit (explicit ``abs``, ``rel=0``);
everything else is exact.
"""

from __future__ import annotations

import hashlib
import json
import sys
from decimal import Decimal
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

ARTIFACT = PROJECT_ROOT / "artifacts" / "independent" / "phase1g_owner_decisions.json"
APPROVAL_DATE = "2026-09-30"
APPROVALS_VERBATIM = [
    "Create the local branch `phase-1g-owner-decisions` from `main` and commit there.",
    "Apply the owner decisions ticked `[x]` in Sec. 3, exactly as ticked. An unticked decision "
    "is **not** approved: leave it open and list it at the end.",
]
NOT_APPROVED_VERBATIM = [
    "[ ] Create signed annotated tags **locally** for the phases that Sec. 5 finds ready.",
    "[ ] Push `phase-1g-owner-decisions` and open ONE pull request against `main`.",
    "[ ] Merge that pull request (merge commit, as PR #1 and PR #2).",
    "[ ] Push the tags created under approval 3.",
]
# Current values, including the separately approved 2026-10-02 D successor.
# Historical 2026-09-30 records remain pinned independently below.
PHASE1G_TOKENS = {
    "UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY": "REFUTED_HADAMARD_ILL_POSED",
    "TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW": "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION",
    "SUPER_CELL_TO_SUB_CELL_GROWTH_TRANSITION": "NOT_DERIVED",
    "GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY": "FAILED_FOR_TIMESCAPE_TRACKER",
    "TWO_SCALE_SUPER_CELL_GROWTH_LAW": "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION",
    "VOID_ONSET_RESPONSE": "EXTERNAL_CLOSURE_INPUT",
    "LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC": "NOT_DERIVED",
    "TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC": "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION",
    "SIGMA8_AUTHORIZATION": "NOT_GRANTED",
    "FSIGMA8_AUTHORIZATION": "NOT_GRANTED",
    "OBSERVATIONAL_AUTHORIZATION": "NOT_GRANTED",
    "UNIQUE_TIMESCAPE_PREDICTION": "NOT_GRANTED",
}


def record_path(phase: str) -> Path:
    return PROJECT_ROOT / "reports" / f"phase1g_{phase}_owner_decisions_successor_inventory.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_lf(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def half_unit(value: float) -> float:
    return 0.5 * 10.0 ** Decimal(repr(value)).normalize().as_tuple().exponent


def status_source() -> str:
    return (PROJECT_ROOT / "src" / "timescape_fsigma8" / "scientific_status.py").read_text(encoding="utf-8")


def check_record(phase: str, ticks: dict, unticked: list, comments_changed: list) -> dict:
    """The record is canonical, carries the ticks verbatim and states its scope."""
    import validate_phase1f_c_r_astra_remediation as remediation

    path = record_path(phase)
    record = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=remediation.unique_pairs)
    assert path.read_bytes() == remediation.canonical(record)
    assert record["classification"] == "OWNER_DECISIONS_SUCCESSOR_RECORD"
    assert record["date"] == APPROVAL_DATE
    assert record["phase"] == f"1G-{phase.upper()}"
    assert (PROJECT_ROOT / record["report"]).is_file()
    approval = record["human_approval"]
    assert approval["date"] == APPROVAL_DATE
    assert approval["verbatim"] == APPROVALS_VERBATIM
    assert approval["not_approved_verbatim"] == NOT_APPROVED_VERBATIM
    assert sorted(record["decisions"]) == sorted(ticks)
    for decision_id, tick in ticks.items():
        entry = record["decisions"][decision_id]
        assert entry["tick_verbatim"] == tick, decision_id
        assert entry["applied"] is True
    assert record["unticked_not_applied"] == unticked
    scope = record["scope"]
    assert scope["status_token_values_changed"] is False
    assert scope["equations_changed"] is False
    assert scope["tolerances_changed"] is False
    assert scope["frozen_reports_inventories_or_phase_scripts_edited"] is False
    assert scope["status_token_comments_changed"] == comments_changed
    # Every frozen file the record supersedes is byte-identical (LF-normalised).
    assert record["frozen_files_sha256_lf"]
    for name, digest in record["frozen_files_sha256_lf"].items():
        assert sha256_lf(PROJECT_ROOT / name) == digest, name
    return record


def artifact_or_skip() -> dict:
    if not ARTIFACT.is_file():
        pytest.skip("owner-decisions artifact absent (run scripts/phase1g_owner_decisions_numerics.py)")
    return load(ARTIFACT)


def check_quoted_numbers(phase: str) -> None:
    """Every number the record quotes from the artifact equals it at its recorded digits."""
    art = artifact_or_skip()
    assert art["gates"] and all(gate["pass"] is True for gate in art["gates"])
    assert art["status"].startswith("OWNER_DECISION_EVIDENCE") and "NOT_SIGMA8" in art["status"]
    quoted = load(record_path(phase))["numbers_from_artifact"]
    assert quoted
    for path, value in quoted.items():
        got = art["results"]
        for key in path.split("|"):
            got = got[int(key)] if isinstance(got, list) else got[key]
        assert got == pytest.approx(value, rel=0.0, abs=half_unit(value)), path
