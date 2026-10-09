"""Run extra mutants exactly as the second delta audit's campaign does (one copy each).

    OPENBLAS_NUM_THREADS=1 python -B run_extra_mutants.py REPO PYTHON WORKDIR DEFS.json OUT.json
"""
import hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

REPO, PY, WORK, DEFS, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5])
SCR = "scripts/phase1g_h_global_variance_closure_numerics.py"
BASE = WORK / "base"
if BASE.exists():
    shutil.rmtree(BASE)
(BASE / "tests").mkdir(parents=True)
for name in ("src", "scripts"):
    shutil.copytree(REPO / name, BASE / name, ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"))
for name in ("test_phase1g_h_global_variance.py", "conftest.py"):
    shutil.copy2(REPO / "tests" / name, BASE / "tests" / name)
shutil.copy2(REPO / "pyproject.toml", BASE / "pyproject.toml")
(BASE / "reports").symlink_to(REPO / "reports", target_is_directory=True)


def summary_line(text):
    return next((ln for ln in reversed(text.splitlines()) if re.search(r"\b(passed|failed|error)\b", ln)), "")


rows = []
for m in json.loads(DEFS.read_text()):
    dest = WORK / "m" / m["id"]
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(BASE, dest, symlinks=True)
    row = dict(m)
    text = (dest / m["file"]).read_text()
    row["replacements"] = text.count(m["old"])
    if not row["replacements"]:
        row["outcome"] = "NOT_APPLIED"
        rows.append(row)
        continue
    (dest / m["file"]).write_text(text.replace(m["old"], m["new"]))
    row["mutated_sha256"] = hashlib.sha256((dest / m["file"]).read_bytes()).hexdigest()
    env = dict(os.environ, PYTHONPATH=str(dest / "src"), PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
    t = subprocess.run([PY, "-B", "-W", "error", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=line",
                        "tests/test_phase1g_h_global_variance.py"], cwd=dest, env=env, text=True, capture_output=True)
    row["tests_rc"], row["tests_summary"] = t.returncode, summary_line(t.stdout)
    row["failed_tests"] = re.findall(r"^FAILED (\S+)", t.stdout, re.M)
    if m["file"] == SCR or t.returncode == 0:
        e = subprocess.run([PY, "-B", "-W", "error", SCR, "--no-figures"], cwd=dest, env=env, text=True,
                           capture_output=True)
        row["evidence_rc"] = e.returncode
        row["evidence_failures"] = [ln.strip() for ln in e.stdout.splitlines() if "FAIL" in ln][:8]
    row["outcome"] = ("KILLED_BY_TESTS" if t.returncode != 0 else
                      "KILLED_BY_EVIDENCE_ONLY" if row.get("evidence_rc", 0) != 0 else "SURVIVED")
    shutil.rmtree(dest, ignore_errors=True)
    rows.append(row)
    print(json.dumps({k: row.get(k) for k in ("id", "outcome", "tests_summary", "evidence_rc")}), flush=True)
OUT.write_text(json.dumps(rows, indent=1) + "\n")
