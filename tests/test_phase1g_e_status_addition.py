"""Regression for the approved Phase 1G-E status-token addition.

Successor record: reports/phase1g_e_status_addition_successor.md and its
inventory (human approval dated 2026-09-29).  Proposal:
reports/phase1g_e_two_phase_sigma.md Sec. 6 item 3 ([1G-E]); evidence [1G-E]
Sec. 2 (the two-phase model and its assumptions E1-E4).

The token is an *addition*: neither the frozen 1F-C-R snapshot
(reports/phase1f_c_r_astra_audit_remediation_inventory.json) nor the two
earlier successor records hold it.  The 1F-C-R validator accepts it only
through the registered record and still rejects an undeclared token, an
addition the frozen snapshot already holds, a live value that differs from
the record, and a token claimed twice.  Every comparison here is exact string
or key equality; no numerical tolerance is involved (AGENTS.md rule 9).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from timescape_fsigma8 import scientific_status
from timescape_fsigma8.scientific_status import CURRENT_SCIENTIFIC_STATUS

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

TOKEN = "TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC"
VALUE = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
RECORD_JSON = "reports/phase1g_e_status_addition_successor_inventory.json"
RECORD_MD = PROJECT_ROOT / "reports" / "phase1g_e_status_addition_successor.md"
BAROTROPIC_RECORD_JSON = "reports/phase1g_a_barotropic_status_successor_inventory.json"
SIX_RECORD_JSON = "reports/phase1g_status_additions_successor_inventory.json"
FROZEN_1F_C_R_INVENTORY = PROJECT_ROOT / "reports" / "phase1f_c_r_astra_audit_remediation_inventory.json"
REPORT_1G_E = "reports/phase1g_e_two_phase_sigma.md"
INVENTORY_1G_E = PROJECT_ROOT / "reports" / "phase1g_e_two_phase_sigma_inventory.json"
SECTION = 2
BAROTROPIC_TOKEN = "UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY"
NOT_GRANTED = ("UNIQUE_TIMESCAPE_PREDICTION", "OBSERVATIONAL_AUTHORIZATION",
               "RSD_AUTHORIZATION", "SIGMA8_AUTHORIZATION", "FSIGMA8_AUTHORIZATION")
APPROVAL_DATE = "2026-09-29"
APPROVALS_VERBATIM = [
    "Add the status token TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC = "
    "\"DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION\" (reports/phase1g_e_two_phase_sigma.md "
    "§6 item 3; assumptions E1–E4).",
    "Commit to this session's working branch, push that branch, and open ONE draft "
    "pull request against main at the end.",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture()
def remediation(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(PROJECT_ROOT)
    import validate_phase1f_c_r_astra_remediation as module
    return module


@pytest.fixture()
def frozen() -> dict:
    return load_json(FROZEN_1F_C_R_INVENTORY)["current_scientific_status"]


def test_token_is_an_addition_with_the_approved_value(frozen: dict) -> None:
    assert getattr(scientific_status, TOKEN) == VALUE
    assert CURRENT_SCIENTIFIC_STATUS[TOKEN] == VALUE
    assert TOKEN not in frozen
    earlier = load_json(PROJECT_ROOT / SIX_RECORD_JSON)["status_additions"]
    assert TOKEN not in earlier and len(earlier) == 6
    # Live keys: the frozen snapshot, the six earlier additions and this one.
    assert set(CURRENT_SCIENTIFIC_STATUS) == set(frozen) | set(earlier) | {TOKEN}
    for token, value in frozen.items():
        live = CURRENT_SCIENTIFIC_STATUS[token]
        live = list(live) if isinstance(live, tuple) else live
        if token == BAROTROPIC_TOKEN:
            assert (value, live) == ("NOT_DERIVED", "REFUTED_HADAMARD_ILL_POSED")
        else:
            assert live == value, token
    for token, addition in earlier.items():
        # The original D addition is still pinned in its historical record;
        # its live value follows the separately registered 2026-10-02 change.
        expected = "NOT_DERIVED" if token == "LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC" else addition["value"]
        assert CURRENT_SCIENTIFIC_STATUS[token] == expected
    for token in NOT_GRANTED:
        assert CURRENT_SCIENTIFIC_STATUS[token] == "NOT_GRANTED"


def test_record_is_canonical_and_matches_the_proposal(remediation) -> None:
    path = PROJECT_ROOT / RECORD_JSON
    record = json.loads(path.read_text(encoding="utf-8"),
                        object_pairs_hook=remediation.unique_pairs)
    assert path.read_bytes() == remediation.canonical(record)
    assert record["classification"] == "APPROVED_SCIENTIFIC_STATUS_ADDITION_SUCCESSOR_RECORD"
    assert record["report"] == "reports/phase1g_e_status_addition_successor.md"
    assert record["parent_commit"] == "6f7937ce5681900898f5e0a6482a953f0fa3e5a0"
    assert record["status_changes"] == {}
    assert list(record["status_additions"]) == [TOKEN]
    approval = record["human_approval"]
    assert approval["date"] == APPROVAL_DATE
    assert approval["verbatim"] == APPROVALS_VERBATIM
    addition = record["status_additions"][TOKEN]
    assert addition["value"] == VALUE
    assert addition["module"] == "src/timescape_fsigma8/scientific_status.py"
    assert addition["report"] == REPORT_1G_E
    assert addition["section"] == f"Sec. {SECTION}"
    # The cited section exists, and [1G-E] and its frozen inventory proposed
    # exactly this token and value under assumptions E1-E4.
    report = (PROJECT_ROOT / REPORT_1G_E).read_text(encoding="utf-8")
    inventory = load_json(INVENTORY_1G_E)
    assert f"\n## {SECTION}. " in report
    assert f'`{TOKEN} = "{VALUE}"`' in report
    assert f"status token {TOKEN} = {VALUE}" in inventory["recommendations_require_human_approval"]
    assert addition["assumptions"] == inventory["model"]["assumptions"]
    assert sorted(addition["assumptions"]) == ["E1", "E2", "E3", "E4"]
    text = RECORD_MD.read_text(encoding="utf-8")
    assert f"`{TOKEN}`" in text and f"`{VALUE}`" in text
    for verbatim in APPROVALS_VERBATIM:
        assert verbatim in text
    scope = record["scope"]
    assert scope["existing_status_tokens_changed"] is False
    assert scope["equations_changed"] is False
    assert scope["tolerances_changed"] is False
    assert scope["frozen_historical_reports_or_inventories_edited"] is False
    assert scope["not_granted_tokens"] == sorted(NOT_GRANTED)


def test_validator_accepts_the_addition_through_the_registered_record(
    remediation, frozen: dict,
) -> None:
    assert remediation.STATUS_SUCCESSOR_RECORDS == (
        Path(BAROTROPIC_RECORD_JSON), Path(SIX_RECORD_JSON), Path(RECORD_JSON),
        Path("reports/phase1g_d_linear_statistic_status_successor_inventory.json"))
    additions = remediation.successor_status_additions()
    assert additions[TOKEN] == {"value": VALUE, "record": RECORD_JSON}
    assert [key for key, value in additions.items() if value["record"] == RECORD_JSON] == [TOKEN]
    changes = remediation.successor_status_changes()
    assert set(changes) == {BAROTROPIC_TOKEN, "LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC"}
    remediation.check_current_scientific_status(
        frozen, CURRENT_SCIENTIFIC_STATUS, changes, additions=additions)


def test_validator_rejects_the_token_when_undeclared_or_inconsistent(
    remediation, frozen: dict,
) -> None:
    changes = remediation.successor_status_changes()
    additions = remediation.successor_status_additions()
    undeclared = {key: value for key, value in additions.items() if key != TOKEN}
    with pytest.raises(AssertionError, match=f"{TOKEN}: token absent from the frozen snapshot"):
        remediation.check_current_scientific_status(
            frozen, CURRENT_SCIENTIFIC_STATUS, changes, additions=undeclared)
    with pytest.raises(AssertionError, match=f"{TOKEN}: frozen snapshot already holds"):
        remediation.check_current_scientific_status(
            {**frozen, TOKEN: VALUE}, CURRENT_SCIENTIFIC_STATUS, changes, additions=additions)
    with pytest.raises(AssertionError, match=f"{TOKEN}: live value differs from the successor"):
        remediation.check_current_scientific_status(
            frozen, {**CURRENT_SCIENTIFIC_STATUS, TOKEN: "NOT_DERIVED"}, changes,
            additions=additions)
    live = {key: value for key, value in CURRENT_SCIENTIFIC_STATUS.items() if key != TOKEN}
    with pytest.raises(AssertionError, match="adds a token the live module lacks"):
        remediation.check_current_scientific_status(frozen, live, changes, additions=additions)


def test_validator_rejects_a_double_claim_and_a_tampered_record(
    remediation, frozen: dict, monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    record = load_json(PROJECT_ROOT / RECORD_JSON)
    # The same token claimed by the precedent record as well is rejected.
    six = load_json(PROJECT_ROOT / SIX_RECORD_JSON)
    six["status_additions"][TOKEN] = {"value": VALUE}
    six_path = tmp_path / "six_claims_token.json"
    six_path.write_text(json.dumps(six), encoding="utf-8")
    monkeypatch.setattr(remediation, "STATUS_SUCCESSOR_RECORDS",
                        (Path(BAROTROPIC_RECORD_JSON), six_path, Path(RECORD_JSON)))
    with pytest.raises(AssertionError, match=f"{TOKEN}: added by more than one successor record"):
        remediation.successor_status_additions()
    # A tampered record value no longer matches the live module.
    tampered = json.loads(json.dumps(record))
    tampered["status_additions"][TOKEN]["value"] = "DERIVED_FROM_VERIFIED_DEFINITIONS"
    tampered_path = tmp_path / "tampered_value.json"
    tampered_path.write_text(json.dumps(tampered), encoding="utf-8")
    monkeypatch.setattr(remediation, "STATUS_SUCCESSOR_RECORDS",
                        (Path(BAROTROPIC_RECORD_JSON), Path(SIX_RECORD_JSON), tampered_path,
                         Path("reports/phase1g_d_linear_statistic_status_successor_inventory.json")))
    with pytest.raises(AssertionError, match=f"{TOKEN}: live value differs"):
        remediation.check_current_scientific_status(
            frozen, CURRENT_SCIENTIFIC_STATUS, remediation.successor_status_changes(),
            additions=remediation.successor_status_additions())
