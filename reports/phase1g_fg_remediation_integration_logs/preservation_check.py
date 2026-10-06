"""Integration-session preservation and perimeter checks (read-only). Run from the repo root.

Compares the working tree with the checksum taken at session start (tree_start.sha256),
re-verifies audit files, evidence MANIFEST, frozen-file pins, status values and that the
scientific_status.py edit is docstring-only (AST equality after removing the module docstring,
and reconstruction of the pre-edit bytes).
"""
import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path

R3 = Path(sys.argv[1])
out = {}
start = {}
for line in (R3 / "tree_start.sha256").read_text(encoding="utf-8").splitlines():
    h, p = line.split(" ", 1)
    start[p.lstrip("*")] = h
now = {}
skip = ("./.venv/", "./.venv311/", "./.git/", "./.pytest_cache/")
for p in sorted(Path(".").rglob("*")):
    s = "./" + p.as_posix()
    if p.is_file() and not s.startswith(skip) and "/__pycache__/" not in s:
        now[s] = hashlib.sha256(p.read_bytes()).hexdigest()
changed = sorted(f for f in start if now.get(f) != start[f])
added = sorted(set(now) - set(start))
removed = sorted(set(start) - set(now))
allowed_changed = {"./CLAUDE.md", "./README.md", "./.gitattributes", "./src/timescape_fsigma8/scientific_status.py",
                   "./reports/phase1g_f_volume_budget_successor.md", "./reports/phase1g_f_volume_budget_successor_inventory.json",
                   "./reports/phase1g_g_void_evolution.md", "./reports/phase1g_g_void_evolution_inventory.json"}
allowed_added_prefix = ("./reports/phase1g_fg_remediation_integration",)
out["changed_vs_session_start"] = changed
out["added_vs_session_start"] = added
out["removed_vs_session_start"] = removed
out["changed_within_perimeter"] = set(changed) <= allowed_changed
out["added_within_perimeter"] = all(a.startswith(allowed_added_prefix) for a in added)
out["artifacts_unchanged"] = all(now.get(f) == h for f, h in start.items() if f.startswith("./artifacts/"))
out["n_artifact_files"] = sum(1 for f in start if f.startswith("./artifacts/"))
tracked_reports = subprocess.check_output(["git", "ls-files", "reports"], text=True).split()
out["tracked_reports_unchanged_vs_HEAD"] = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", "reports"]).returncode == 0
out["n_tracked_reports"] = len(tracked_reports)
audits = {"reports/phase1g_fg_independent_scientific_audit.md": "6bb8edecf394989186c86e3ead7f401bcbcc0ac1977bc395008db7019a0c063d",
          "reports/phase1g_fg_independent_scientific_audit_inventory.json": "3503a602413cb15f8daed58bf0a6d31a6c0defcc222527ce528753812d888aae",
          "reports/phase1g_fg_remediation_independent_audit.md": "46f3aef7f27240f03eb4ef530cebc16a2365f703a93308e165b0c75680389a25",
          "reports/phase1g_fg_remediation_independent_audit_inventory.json": "ebe7918272d2f3cb5ffcc0c00bbbe14971a2f00dd28609378c1e22e46b17f214",
          "reports/phase1g_fg_audit_remediation.md": start["./reports/phase1g_fg_audit_remediation.md"],
          "reports/phase1g_fg_audit_remediation_inventory.json": start["./reports/phase1g_fg_audit_remediation_inventory.json"],
          "reports/phase1g_d_linear_statistic_status_successor.md": start["./reports/phase1g_d_linear_statistic_status_successor.md"],
          "reports/phase1g_d_linear_statistic_status_successor_inventory.json": start["./reports/phase1g_d_linear_statistic_status_successor_inventory.json"],
          "reports/phase1g_fg_successor_validation.md": start["./reports/phase1g_fg_successor_validation.md"]}
out["audit_and_record_files_intact"] = {k: hashlib.sha256(Path(k).read_bytes()).hexdigest() == v for k, v in audits.items()}
ev = Path("reports/phase1g_fg_remediation_audit_evidence")
bad = []
for line in (ev / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
    h, p = line.split(" ", 1)
    if hashlib.sha256((ev / p.lstrip("*")).read_bytes()).hexdigest() != h:
        bad.append(p)
out["evidence_manifest_entries"] = len((ev / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines())
out["evidence_manifest_mismatches"] = bad
out["evidence_files_unchanged_vs_session_start"] = all(now.get(f) == h for f, h in start.items() if f.startswith("./reports/phase1g_fg_remediation_audit_evidence/"))
inv1 = json.loads(Path("reports/phase1g_fg_independent_scientific_audit_inventory.json").read_bytes())
out["prior_14_evidence_hashes_match_first_audit"] = all(
    hashlib.sha256((ev / "prior_audit_2026-10-02" / n).read_bytes()).hexdigest() == h for n, h in inv1["auditor_evidence"]["sha256"].items())
pins = json.loads(Path("reports/phase1g_f_volume_budget_successor_inventory.json").read_bytes())["frozen_sha256"]
out["frozen_sha256_pins_ok"] = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in pins.items()}
# scientific_status.py: docstring-only edit
src = Path("src/timescape_fsigma8/scientific_status.py").read_text(encoding="utf-8")
added_text = ("  The registered, owner-approved successor of 2026-10-02\n"
              "(reports/phase1g_d_linear_statistic_status_successor.md and its canonical\n"
              "inventory) changes one of the six added tokens,\n"
              "LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC, to NOT_DERIVED through an explicit\n"
              "link to its adding record, which keeps the historical value.  No\n"
              "observational authorization changes.")
pre = src.replace("value." + added_text + "\n\"\"\"", "value.\n\"\"\"", 1)
out["status_module_pre_edit_reconstruction_matches_session_start"] = (
    hashlib.sha256(pre.encode("utf-8")).hexdigest() == start["./src/timescape_fsigma8/scientific_status.py"])
def body(s):
    t = ast.parse(s)
    t.body = t.body[1:]
    return ast.dump(t, include_attributes=False)
out["status_module_AST_without_docstring_identical_to_pre_edit"] = body(src) == body(pre)
sys.path.insert(0, "src")
from timescape_fsigma8.scientific_status import CURRENT_SCIENTIFIC_STATUS as S  # noqa: E402
out["observational_authorizations"] = {k: S[k] for k in ("SIGMA8_AUTHORIZATION", "FSIGMA8_AUTHORIZATION", "RSD_AUTHORIZATION",
                                                          "OBSERVATIONAL_AUTHORIZATION", "UNIQUE_TIMESCAPE_PREDICTION")}
out["D_token"] = S["LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC"]
head_src = subprocess.check_output(["git", "show", "HEAD:src/timescape_fsigma8/scientific_status.py"], text=True, encoding="utf-8")
def assigns(s):
    return {t.id: ast.unparse(n.value) for n in ast.parse(s).body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)}
a, b = assigns(head_src), assigns(src)
out["assignments_differing_from_HEAD"] = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
code_files = [f for f in changed if f.endswith(".py")]
out["python_files_changed_this_session"] = code_files
print(json.dumps(out, indent=1))
(R3 / "preservation_check.json").write_bytes((json.dumps(out, indent=1) + "\n").encode())
