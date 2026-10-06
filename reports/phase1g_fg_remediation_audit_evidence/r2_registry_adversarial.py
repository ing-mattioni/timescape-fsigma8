"""Delta audit R2-M3: adversarial checks of the status-successor registry (read-only on the repo).

Run with cwd = repository root:  python r2_registry_adversarial.py <out_json>
Imports scripts/validate_phase1f_c_r_astra_remediation.py by path, never writes to the repo;
mutated records live in a temporary directory.  Each case states the expected outcome.
"""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
spec = importlib.util.spec_from_file_location("reg", ROOT / "scripts/validate_phase1f_c_r_astra_remediation.py")
reg = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(ROOT / "scripts"))
spec.loader.exec_module(reg)
from timescape_fsigma8.scientific_status import CURRENT_SCIENTIFIC_STATUS as LIVE  # noqa: E402

TOKEN = "LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC"
D = Path("reports/phase1g_d_linear_statistic_status_successor_inventory.json")
SIX = Path("reports/phase1g_status_additions_successor_inventory.json")
E = Path("reports/phase1g_e_status_addition_successor_inventory.json")
A = Path("reports/phase1g_a_barotropic_status_successor_inventory.json")
FROZEN = json.loads(reg.INVENTORY.read_text(encoding="utf-8"))["current_scientific_status"]
ORIG = tuple(reg.STATUS_SUCCESSOR_RECORDS)
tmp = Path(tempfile.mkdtemp(prefix="r2reg_"))


def rec(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(name, obj):
    p = tmp / name
    p.write_text(json.dumps(obj), encoding="utf-8")
    return p


def run(records, live=LIVE):
    reg.STATUS_SUCCESSOR_RECORDS = tuple(records)
    try:
        ch, ad, rm = reg.successor_status_changes(), reg.successor_status_additions(), reg.successor_status_removals()
        reg.check_current_scientific_status(FROZEN, live, ch, additions=ad, removals=rm)
        return "PASS", ""
    except (AssertionError, KeyError, ValueError) as exc:
        return "FAIL", f"{type(exc).__name__}: {str(exc)[:160]}"
    finally:
        reg.STATUS_SUCCESSOR_RECORDS = ORIG


cases = {}
def case(name, expected, records, live=LIVE):
    outcome, msg = run(records, live)
    cases[name] = {"expected": expected, "observed": outcome, "message": msg, "as_expected": outcome == expected}


d = rec(D)
case("baseline_registered_records", "PASS", ORIG)
x = copy.deepcopy(d); x["status_changes"][TOKEN].pop("added_by_record")
case("change_without_predecessor_link", "FAIL", (A, SIX, E, write("nolink.json", x)))
x = copy.deepcopy(d); x["status_changes"][TOKEN]["added_by_record"] = "reports/unregistered.json"
case("link_to_unregistered_record", "FAIL", (A, SIX, E, write("badlink.json", x)))
x = copy.deepcopy(d); x["status_changes"][TOKEN]["added_by_record"] = E.as_posix()
case("link_to_wrong_registered_record", "FAIL", (A, SIX, E, write("wronglink.json", x)))
x = copy.deepcopy(d); x["status_changes"][TOKEN]["old_token"] = "NOT_DERIVED"
case("old_token_inconsistent_with_addition", "FAIL", (A, SIX, E, write("badold.json", x)))
x = copy.deepcopy(d); x["status_additions"] = {TOKEN: {"value": "NOT_DERIVED"}}
case("successor_also_re_adds_token", "FAIL", (A, SIX, E, write("readd.json", x)))
case("same_change_registered_twice", "FAIL", (A, SIX, E, D, D))
x = copy.deepcopy(d); x["status_changes"][TOKEN].update(old_token="NOT_DERIVED", new_token="SOMETHING_ELSE")
case("chained_second_change", "FAIL", (A, SIX, E, D, write("chain.json", x)))
live_old = dict(LIVE); live_old[TOKEN] = "NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY"
case("live_module_not_updated", "FAIL", ORIG, live_old)
live_other = dict(LIVE); live_other[TOKEN] = "DERIVED"
case("live_module_other_value", "FAIL", ORIG, live_other)
x = copy.deepcopy(d); x["status_changes"] = {"D3_VERDICT": {"old_token": FROZEN["D3_VERDICT"], "new_token": "X", "added_by_record": SIX.as_posix()}}
live_d3 = dict(LIVE); live_d3["D3_VERDICT"] = "X"
case("predecessor_link_on_frozen_token", "FAIL", (A, SIX, E, write("frozenlink.json", x)), live_d3)
x = copy.deepcopy(d); x["status_changes"] = {}; x["status_removals"] = {TOKEN: {"old_token": "NOT_DERIVED"}}
live_rm = {k: v for k, v in LIVE.items() if k != TOKEN}
case("removal_of_added_token", "FAIL", (A, SIX, E, write("remove.json", x)), live_rm)
case("order_swapped_D_before_addition", "PASS_OR_FAIL (order not specified)", (A, D, SIX, E))
# History rewrite: edit the ORIGINAL addition value and drop the D change. The validator alone
# cannot see this; protection must come from tests pinning the original record and from Git.
six = rec(SIX); six["status_additions"][TOKEN]["value"] = "NOT_DERIVED"
case("history_rewrite_of_original_addition_without_change", "PASS (validator-only blind spot)", (A, write("six_rewritten.json", six), E))
other = dict(LIVE); other["VOID_ONSET_RESPONSE"] = "DERIVED"
case("unrelated_token_changed_in_live_module", "FAIL", ORIG, other)

# Provenance facts
facts = {
    "original_addition_record_blob_equals_HEAD": subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", SIX.as_posix()]).returncode == 0,
    "original_addition_value": rec(SIX)["status_additions"][TOKEN]["value"],
    "D_record_canonical": D.read_bytes() == reg.canonical(rec(D)),
    "registered_records": [p.as_posix() for p in ORIG],
}
try:
    reg.check_successor_records_canonical(ORIG)
    facts["all_registered_records_canonical"] = True
except AssertionError as exc:
    facts["all_registered_records_canonical"] = str(exc)
out = {"cases": cases, "facts": facts, "all_as_expected": all(c["as_expected"] for k, c in cases.items()
                                                                if c["expected"] in ("PASS", "FAIL"))}
Path(sys.argv[1]).write_bytes((json.dumps(out, indent=1) + "\n").encode())
for k, c in cases.items():
    print(f"{k:55s} expected={c['expected']:<34s} observed={c['observed']:<5s} {c['message'][:90]}")
print(json.dumps(facts, indent=1))
print("all_as_expected", out["all_as_expected"])
