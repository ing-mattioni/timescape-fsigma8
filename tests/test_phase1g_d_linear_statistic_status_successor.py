"""Owner-approved FGA-D1 transition; exact provenance and API comparisons."""

import copy
import json
from pathlib import Path
import sys

import pytest

from timescape_fsigma8.scientific_status import CURRENT_SCIENTIFIC_STATUS

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_phase1f_c_r_astra_remediation as registry

TOKEN = "LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC"
RECORD = Path("reports/phase1g_d_linear_statistic_status_successor_inventory.json")


@pytest.fixture()
def inputs(monkeypatch):
    monkeypatch.chdir(ROOT)
    frozen = json.loads(registry.INVENTORY.read_text(encoding="utf-8"))["current_scientific_status"]
    return frozen, registry.successor_status_changes(), registry.successor_status_additions()


def test_approved_transition_preserves_both_historical_states_and_authorizations(inputs):
    frozen, changes, additions = inputs
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    assert RECORD.read_bytes() == registry.canonical(record)
    assert record["human_approval"]["verbatim"] == "si confermo"
    assert record["human_approval"]["date"] == "2026-10-02"
    assert TOKEN not in frozen
    assert additions[TOKEN]["value"] == "NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY"
    assert changes[TOKEN]["old_token"] == additions[TOKEN]["value"]
    assert changes[TOKEN]["new_token"] == "NOT_DERIVED"
    registry.check_current_scientific_status(frozen, CURRENT_SCIENTIFIC_STATUS, changes, additions=additions)
    for key in ("SIGMA8_AUTHORIZATION", "FSIGMA8_AUTHORIZATION", "RSD_AUTHORIZATION",
                "OBSERVATIONAL_AUTHORIZATION", "UNIQUE_TIMESCAPE_PREDICTION"):
        assert CURRENT_SCIENTIFIC_STATUS[key] == frozen[key] == "NOT_GRANTED"


@pytest.mark.parametrize("mutation, message", [
    ("missing_link", "both changed and added"),
    ("wrong_link", "adding predecessor record"),
    ("same_record", "same record"),
    ("wrong_old_value", "does not hold the superseded token"),
    ("missing_addition", "added by no successor record"),
    ("missing_change", "live value differs"),
])
def test_a_later_change_cannot_bypass_the_original_addition(inputs, mutation, message):
    frozen, changes, additions = copy.deepcopy(inputs)
    if mutation == "missing_link":
        changes[TOKEN].pop("added_by_record")
    elif mutation == "wrong_link":
        changes[TOKEN]["added_by_record"] = "unregistered.json"
    elif mutation == "same_record":
        changes[TOKEN]["record"] = additions[TOKEN]["record"]
    elif mutation == "wrong_old_value":
        changes[TOKEN]["old_token"] = "DERIVED"
    elif mutation == "missing_addition":
        additions.pop(TOKEN)
    else:
        changes.pop(TOKEN)
    with pytest.raises(AssertionError, match=message):
        registry.check_current_scientific_status(frozen, CURRENT_SCIENTIFIC_STATUS, changes, additions=additions)


def test_duplicate_transition_records_still_fail(inputs, monkeypatch):
    monkeypatch.setattr(registry, "STATUS_SUCCESSOR_RECORDS", (*registry.STATUS_SUCCESSOR_RECORDS, RECORD))
    with pytest.raises(AssertionError, match="superseded by more than one successor record"):
        registry.successor_status_changes()
