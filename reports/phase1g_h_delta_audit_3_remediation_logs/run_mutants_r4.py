"""Round-4 mutants in disposable copies (one exact string replacement each).

    OPENBLAS_NUM_THREADS=1 python -B run_mutants_r4.py REPO PYTHON WORKDIR DEFS.json OUT.json

Each mutant names the test files to run; H-module or evidence-script mutants
that survive the tests also run the evidence script (--no-figures).
"""
import concurrent.futures as cf, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

REPO, PY, WORK, DEFS, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5])
SCR = "scripts/phase1g_h_global_variance_closure_numerics.py"
H_TESTS = "tests/test_phase1g_h_global_variance.py"
BASE = WORK / "base"
if BASE.exists():
    shutil.rmtree(BASE)
(BASE / "tests").mkdir(parents=True)
for name in ("src", "scripts"):
    shutil.copytree(REPO / name, BASE / name, ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"))
for name in ("conftest.py", "test_phase1g_h_global_variance.py", "test_phase1g_b_lagrangian_sigma.py",
             "test_phase1g_b_owner_decisions.py", "test_phase1g_b_contract_hardening.py"):
    shutil.copy2(REPO / "tests" / name, BASE / "tests" / name)
shutil.copy2(REPO / "pyproject.toml", BASE / "pyproject.toml")
for name in ("reports", "CLAUDE.md", "AGENTS.md"):
    (BASE / name).symlink_to(REPO / name)


def summary_line(text):
    return next((ln for ln in reversed(text.splitlines()) if re.search(r"\b(passed|failed|error)\b", ln)), "")


def run(m):
    dest = WORK / "m" / m["id"]
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(BASE, dest, symlinks=True)
    row = dict(m)
    if m.get("file"):
        text = (dest / m["file"]).read_text()
        row["replacements"] = text.count(m["old"])
        if not row["replacements"]:
            row["outcome"] = "NOT_APPLIED"
            return row
        (dest / m["file"]).write_text(text.replace(m["old"], m["new"]))
        row["mutated_sha256"] = hashlib.sha256((dest / m["file"]).read_bytes()).hexdigest()
    env = dict(os.environ, PYTHONPATH=str(dest / "src"), PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
    t = subprocess.run([PY, "-B", "-W", "error", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=line",
                        *m["tests"]], cwd=dest, env=env, text=True, capture_output=True)
    row["tests_rc"], row["tests_summary"] = t.returncode, summary_line(t.stdout)
    row["failed_tests"] = re.findall(r"^FAILED (\S+)", t.stdout, re.M)
    h_side = m.get("file") in (SCR, "src/timescape_fsigma8/global_variance.py")
    if m.get("file") and h_side and t.returncode == 0:
        e = subprocess.run([PY, "-B", "-W", "error", SCR, "--no-figures"], cwd=dest, env=env, text=True,
                           capture_output=True)
        row["evidence_rc"] = e.returncode
        row["evidence_failures"] = [ln.strip() for ln in e.stdout.splitlines() if "FAIL" in ln][:8]
    if not m.get("file"):
        row["outcome"] = "BASELINE_PASS" if t.returncode == 0 else "BASELINE_FAIL"
    else:
        row["outcome"] = ("KILLED_BY_TESTS" if t.returncode != 0 else
                          "KILLED_BY_EVIDENCE_ONLY" if row.get("evidence_rc", 0) != 0 else "SURVIVED")
    shutil.rmtree(dest, ignore_errors=True)
    return row


defs = json.loads(DEFS.read_text())
rows = []
with cf.ThreadPoolExecutor(max_workers=int(os.environ.get("WORKERS", "1"))) as pool:
    for row in pool.map(run, defs):
        rows.append(row)
        print(json.dumps({k: row.get(k) for k in ("id", "outcome", "tests_summary", "evidence_rc")}), flush=True)
OUT.write_text(json.dumps(rows, indent=1) + "\n")
