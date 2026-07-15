"""Execute the pinned upstream ACPT_Timescape.ipynb from a clean kernel.

Phase 1A reproducibility runner. This script:

  * reads the upstream notebook from .reference/ (never writes to it, and
    verifies via SHA-256 that the file is byte-identical afterwards);
  * executes every cell in order in a fresh Jupyter kernel whose working
    directory is artifacts/upstream/ (so figures the notebook saves with
    relative paths land there, not in the reference clone);
  * writes the executed copy to artifacts/upstream/ACPT_Timescape.executed.ipynb
    (also on failure, for inspection of partial output);
  * captures per-cell stdout/stderr, warnings, execution duration, Python and
    package versions, platform info, and the upstream commit SHA into
    artifacts/upstream/execution_log.json;
  * exits nonzero if any cell fails.

The notebook's scientific content (equations, constants, initial conditions,
solver options, plotting) is executed exactly as published — nothing is
modified. PYTHONWARNINGS=default is set for the kernel so that warnings the
authors' environment may have hidden are surfaced and can be audited
(AGENTS.md rule 10); this changes warning *visibility* only, not numerics.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
import traceback
from importlib.metadata import PackageNotFoundError, version as pkg_version
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_DIR = PROJECT_ROOT / ".reference" / "Linear-Perturbations-in-averaged-cosmological-models"
UPSTREAM_NOTEBOOK = UPSTREAM_DIR / "ACPT_Timescape.ipynb"
ARTIFACT_DIR = PROJECT_ROOT / "artifacts" / "upstream"
EXECUTED_NOTEBOOK = ARTIFACT_DIR / "ACPT_Timescape.executed.ipynb"
EXECUTION_LOG = ARTIFACT_DIR / "execution_log.json"

CELL_TIMEOUT_S = 1800  # generous per-cell timeout; the notebook needs far less

LOGGED_PACKAGES = [
    "numpy",
    "scipy",
    "matplotlib",
    "nbformat",
    "nbclient",
    "ipykernel",
    "jupyter_client",
    "jupyter_core",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def upstream_commit() -> str:
    out = subprocess.run(
        ["git", "-C", str(UPSTREAM_DIR), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def package_versions() -> dict[str, str]:
    versions = {}
    for name in LOGGED_PACKAGES:
        try:
            versions[name] = pkg_version(name)
        except PackageNotFoundError:
            versions[name] = "NOT INSTALLED"
    return versions


def collect_cell_outputs(nb) -> tuple[list[dict], list[str], list[dict]]:
    """Return (per-cell stream/error records, warning lines, error records)."""
    cells = []
    warnings_found: list[str] = []
    errors: list[dict] = []
    for idx, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        rec = {"cell_index": idx, "execution_count": cell.get("execution_count"),
               "stdout": "", "stderr": "", "error": None,
               "output_types": [o.output_type for o in cell.get("outputs", [])]}
        for out in cell.get("outputs", []):
            if out.output_type == "stream":
                text = "".join(out.get("text", ""))
                if out.get("name") == "stderr":
                    rec["stderr"] += text
                else:
                    rec["stdout"] += text
            elif out.output_type == "error":
                err = {"cell_index": idx, "ename": out.get("ename"),
                       "evalue": out.get("evalue"),
                       "traceback": out.get("traceback", [])}
                rec["error"] = {"ename": err["ename"], "evalue": err["evalue"]}
                errors.append(err)
        for line in rec["stderr"].splitlines():
            if "Warning" in line or "warn" in line.lower():
                warnings_found.append(f"cell {idx}: {line.strip()}")
        cells.append(rec)
    return cells, warnings_found, errors


def main() -> int:
    import nbformat
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError

    if not UPSTREAM_NOTEBOOK.exists():
        print(f"ERROR: upstream notebook not found: {UPSTREAM_NOTEBOOK}", file=sys.stderr)
        return 2

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    hash_before = sha256(UPSTREAM_NOTEBOOK)
    commit = upstream_commit()
    pdfs_before = {p.name for p in ARTIFACT_DIR.glob("*.pdf")}

    nb = nbformat.read(UPSTREAM_NOTEBOOK, as_version=4)

    # Surface all warnings in the kernel (visibility only; no numerical effect).
    os.environ["PYTHONWARNINGS"] = "default"

    client = NotebookClient(
        nb,
        timeout=CELL_TIMEOUT_S,
        kernel_name=nb.metadata.get("kernelspec", {}).get("name", "python3"),
        allow_errors=False,
        record_timing=True,
        resources={"metadata": {"path": str(ARTIFACT_DIR)}},
    )

    print(f"Executing {UPSTREAM_NOTEBOOK.name} at upstream commit {commit}")
    started = datetime.datetime.now(datetime.timezone.utc)
    t0 = time.perf_counter()
    exec_error: dict | None = None
    try:
        client.execute()
    except CellExecutionError:
        # First failing cell: nbclient stops here; partial outputs remain in nb.
        exec_error = {"type": "CellExecutionError",
                      "traceback": traceback.format_exc()}
    except Exception:
        exec_error = {"type": "ExecutionInfrastructureError",
                      "traceback": traceback.format_exc()}
    duration_s = time.perf_counter() - t0

    # Always write the executed (possibly partial) copy for inspection.
    nbformat.write(nb, EXECUTED_NOTEBOOK)

    hash_after = sha256(UPSTREAM_NOTEBOOK)
    if hash_after != hash_before:
        print("FATAL: upstream notebook file changed during execution!", file=sys.stderr)
        return 3

    cells, warning_lines, cell_errors = collect_cell_outputs(nb)
    pdfs_after = sorted(
        {p.name for p in ARTIFACT_DIR.glob("*.pdf")} - pdfs_before
        | {p.name for p in ARTIFACT_DIR.glob("*.pdf")
           if p.stat().st_mtime >= started.timestamp() - 1}
    )

    first_failing = cell_errors[0]["cell_index"] if cell_errors else None
    success = exec_error is None and not cell_errors

    log = {
        "run_started_utc": started.isoformat(),
        "duration_seconds": round(duration_s, 3),
        "success": success,
        "first_failing_cell": first_failing,
        "upstream": {
            "notebook": str(UPSTREAM_NOTEBOOK.relative_to(PROJECT_ROOT)),
            "commit": commit,
            "notebook_sha256": hash_before,
            "notebook_unmodified": hash_after == hash_before,
        },
        "environment": {
            "python_version": sys.version,
            "python_executable": sys.executable,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "packages": package_versions(),
            "pythonwarnings": os.environ.get("PYTHONWARNINGS"),
        },
        "figures_written": pdfs_after,
        "warnings": warning_lines,
        "cell_errors": cell_errors,
        "runner_error": exec_error,
        "cells": cells,
    }
    EXECUTION_LOG.write_text(json.dumps(log, indent=2), encoding="utf-8")

    print(f"Executed copy : {EXECUTED_NOTEBOOK.relative_to(PROJECT_ROOT)}")
    print(f"Execution log : {EXECUTION_LOG.relative_to(PROJECT_ROOT)}")
    print(f"Duration      : {duration_s:.1f} s")
    print(f"Figures       : {', '.join(pdfs_after) if pdfs_after else '(none)'}")
    print(f"Warnings      : {len(warning_lines)}")
    if not success:
        print(f"FAILED — first failing cell: {first_failing}", file=sys.stderr)
        if exec_error:
            print(exec_error["traceback"], file=sys.stderr)
        return 1
    print("SUCCESS — all cells executed without error.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
