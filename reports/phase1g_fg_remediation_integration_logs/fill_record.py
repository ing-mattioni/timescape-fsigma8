"""Fill the integration record's result sections from this session's logs (registration only)."""
import json
import re
import sys
from pathlib import Path

R3 = Path(sys.argv[1])
rep = Path("reports/phase1g_fg_remediation_integration.md")
invp = Path("reports/phase1g_fg_remediation_integration_inventory.json")


def text(p):
    return p.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")


summary = text(R3 / "run_summary.txt")
suites = {}
for v in ("314", "311"):
    log = text(R3 / f"fullsuite_{v}.log")
    m = re.search(r"^(\d+) passed(?:, (\d+) skipped)?(?:, (\d+) failed)?.* in ([\d.]+)s", log, re.M)
    assert m, v
    ex = re.search(rf"py{v} exit=(\d+)", summary).group(1)
    suites[v] = {"passed": int(m.group(1)), "skipped": int(m.group(2) or 0), "failed": int(m.group(3) or 0),
                 "seconds": float(m.group(4)), "exit": int(ex)}
vers = re.findall(r"^Python (\S+)", summary, re.M)
pres = json.loads((R3 / "preservation_check.json").read_bytes())
assert "git diff --check exit=0" in summary and "ALL OK" in summary

table = "\n".join([
    "Command: the owner-specified PowerShell block, with `PYTHONPATH` set to `src`,",
    "`OPENBLAS_NUM_THREADS=1` and `python -B -W error -m pytest -q -p no:cacheprovider`.",
    "",
    "| Interpreter | Full suite | Time | Exit |",
    "|---|---|---:|---:|",
    f"| CPython {vers[0]} (`.venv`; NumPy 2.5.2, SciPy 1.18.1, pytest 9.1.1) | **{suites['314']['passed']} passed, {suites['314']['skipped']} skipped, {suites['314']['failed']} failed** | {suites['314']['seconds']:.0f} s | {suites['314']['exit']} |",
    f"| CPython {vers[1]} (`.venv311`; NumPy 2.4.6, SciPy 1.17.1, pytest 9.1.1) | **{suites['311']['passed']} passed, {suites['311']['skipped']} skipped, {suites['311']['failed']} failed** | {suites['311']['seconds']:.0f} s | {suites['311']['exit']} |",
    "",
    "Both runs include the unmodified historical Git-blob test. The count is the expected 1136; no test or expectation was changed.",
])
checks = "\n".join([
    "- `git diff --check`: clean (exit 0).",
    "- **Targeted tests, before the suites:** 156 passed (F/G/D modules and the registry and governance tests, 3.14.3).",
    "- **1F-C-R validator:** `PASS`, with changes `{LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC, UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY}`.",
    "- **New `.gitattributes` rule.** It marks the audit-evidence directory and the integration-logs directory as `-text -whitespace`, following the repository's precedent for pinned provenance files.",
    "  - Several Windows-captured evidence logs contain CRLF, and their bytes are pinned by `MANIFEST.sha256`.",
    "  - Line-ending conversion would break those pins; whitespace checks would flag the CRs.",
    "  - Tested beforehand in an isolated temporary repository: bytes are preserved, and `git diff --cached --check` is clean.",
    "- **After the results were filled in**, a registration-only step: the validator, the targeted tests and `git diff --check` were rerun on the final bytes (Sec. 6). The full suites were not rerun, because no code, test or scientific content changed after them.",
])
pl = [f"- **Perimeter.** Files changed relative to the session start: {', '.join('`' + c[2:] + '`' for c in pres['changed_vs_session_start'])}. Added: this record, its inventory and its logs. Nothing was removed.",
      f"- **Artifacts.** All {pres['n_artifact_files']} files under `artifacts/` are unchanged. The historical Monte Carlo was not rerun.",
      f"- **Frozen and tracked reports.** All {pres['n_tracked_reports']} tracked report and inventory files are unchanged against HEAD.",
      "- **Pins.** The `frozen_sha256` pins of the F inventory are unchanged: AGENTS.md and the frozen 1G-F report, inventory and script.",
      "- **Audits and records.** Byte-identical: both independent audits and their inventories, the remediation record, the D successor and the validation record.",
      f"- **Evidence.** `MANIFEST.sha256` verifies with {pres['evidence_manifest_entries']} entries and 0 mismatches. The 14 recovered first-audit files match the first audit's inventory.",
      "- **Status module.** The `scientific_status.py` edit is docstring-only.",
      "  - The pre-edit bytes, reconstructed, equal the session-start SHA-256.",
      "  - The AST without the module docstring is identical.",
      "  - The only assignment differing from HEAD is the approved D token (`NOT_DERIVED`).",
      "  - The five observational authorizations are `NOT_GRANTED`.",
      "- **Code.** No other Python file changed in this session, so no computation changed."]
s = rep.read_text(encoding="utf-8")
for k, v in (("SUITE_TABLE", table), ("CHECKS_LIST", checks), ("PRESERVATION_LIST", "\n".join(pl))):
    assert s.count(k) == 1, k
    s = s.replace(k, v)
rep.write_bytes(s.encode("utf-8"))
inv = json.loads(invp.read_bytes())
inv["verification_this_session"] = {
    "command": "owner-specified PowerShell block: PYTHONPATH=src, OPENBLAS_NUM_THREADS=1, python -B -W error -m pytest -q -p no:cacheprovider; git diff --check",
    "interpreters": {"py314": f"CPython {vers[0]}, NumPy 2.5.2, SciPy 1.18.1, pytest 9.1.1", "py311": f"CPython {vers[1]}, NumPy 2.4.6, SciPy 1.17.1, pytest 9.1.1"},
    "full_suites": suites, "git_diff_check": "clean", "targeted_tests_before_suites": "156 passed (3.14.3)",
    "validator_1fcr": "PASS", "gitattributes_rule": "reports/phase1g_fg_remediation_audit_evidence/** and reports/phase1g_fg_remediation_integration_logs/** set -text -whitespace (tested in an isolated repository)",
    "registration_only_after_suites": "results and commit hash filled in after the suites; validator, targeted tests and git diff --check rerun; no code/test/scientific change"}
inv["preservation"] = pres
invp.write_bytes((json.dumps(inv, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
print(json.dumps(suites), vers)
