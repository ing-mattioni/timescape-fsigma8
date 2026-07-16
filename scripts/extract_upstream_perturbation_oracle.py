"""Extract the clean Timescape perturbation trajectories as a local oracle.

The pinned, unlicensed upstream notebook is read only.  In memory, this
runner executes just cells 0-8 and 13-16 (background, comoving closure,
Mészáros equation, ICs, and solves), then appends an independent sampling
cell that serialises numerical arrays.  It neither writes an executed
notebook nor imports upstream source into the publication package.

Output: ``artifacts/upstream/oracle_clean_perturbations.json`` (git-ignored).
The script verifies the source notebook's SHA-256 before and after execution.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from importlib.metadata import version
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_NOTEBOOK = (
    PROJECT_ROOT
    / ".reference"
    / "Linear-Perturbations-in-averaged-cosmological-models"
    / "ACPT_Timescape.ipynb"
)
UPSTREAM_LOCK = PROJECT_ROOT / "UPSTREAM.lock"
ORACLE_PATH = PROJECT_ROOT / "artifacts" / "upstream" / "oracle_clean_perturbations.json"

# Exact source cells from the Phase 1C-A audit. Cell 12 (barotropic) and all
# plotting cells are deliberately excluded from the B1 oracle.
SOURCE_CELLS = [*range(0, 9), 13, 14, 15, 16]
CELL_TIMEOUT_S = 600

SAMPLING_SOURCE = r"""
import json as _json

_payload = {
    "constants": {
        "fv0": float(fv0), "h": float(h), "GyrstoHT": float(GyrstoHT),
        "G": float(G), "H0": float(H0), "HD0": float(HD0),
        "t0": float(t0), "a0": float(a0),
    },
    "initial_conditions": [float(x) for x in ic],
    "t_eval": [float(x) for x in t_eval],
    "comoving": {
        "t": [float(x) for x in sol_comoving.t],
        "y": [[float(x) for x in row] for row in sol_comoving.y],
        "success": bool(sol_comoving.success),
        "message": str(sol_comoving.message),
        "nfev": int(sol_comoving.nfev), "njev": int(sol_comoving.njev),
        "nlu": int(sol_comoving.nlu),
    },
    "meszaros": {
        "t": [float(x) for x in sol_mezaros.t],
        "y": [[float(x) for x in row] for row in sol_mezaros.y],
        "success": bool(sol_mezaros.success),
        "message": str(sol_mezaros.message),
        "nfev": int(sol_mezaros.nfev), "njev": int(sol_mezaros.njev),
        "nlu": int(sol_mezaros.nlu),
    },
}
print("CLEAN_PERTURBATION_ORACLE_BEGIN")
print(_json.dumps(_payload))
print("CLEAN_PERTURBATION_ORACLE_END")
"""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locked_commit() -> str:
    for line in UPSTREAM_LOCK.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("commit"):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("UPSTREAM.lock contains no commit entry")


def main() -> int:
    import nbformat
    from nbclient import NotebookClient

    if not UPSTREAM_NOTEBOOK.exists():
        print(f"ERROR: missing upstream notebook: {UPSTREAM_NOTEBOOK}", file=sys.stderr)
        return 2

    hash_before = sha256(UPSTREAM_NOTEBOOK)
    source = nbformat.read(UPSTREAM_NOTEBOOK, as_version=4)
    notebook = nbformat.v4.new_notebook(metadata=source.metadata)
    notebook.cells = [source.cells[index] for index in SOURCE_CELLS]
    notebook.cells.append(nbformat.v4.new_code_cell(SAMPLING_SOURCE))

    # Warning visibility only; no warning is suppressed (AGENTS.md rule 10).
    os.environ["PYTHONWARNINGS"] = "default"
    client = NotebookClient(
        notebook,
        timeout=CELL_TIMEOUT_S,
        kernel_name=source.metadata.get("kernelspec", {}).get("name", "python3"),
        allow_errors=False,
        record_timing=True,
        resources={"metadata": {"path": str(ORACLE_PATH.parent)}},
    )
    client.execute()

    payload_text = None
    for output in notebook.cells[-1].get("outputs", []):
        if output.output_type != "stream":
            continue
        stream = "".join(output.get("text", ""))
        if "CLEAN_PERTURBATION_ORACLE_BEGIN" in stream:
            payload_text = stream.split("CLEAN_PERTURBATION_ORACLE_BEGIN", 1)[1].split(
                "CLEAN_PERTURBATION_ORACLE_END", 1
            )[0].strip()
    if payload_text is None:
        print("ERROR: oracle sampling cell produced no payload", file=sys.stderr)
        return 1

    hash_after = sha256(UPSTREAM_NOTEBOOK)
    if hash_after != hash_before:
        print("FATAL: upstream notebook changed during extraction", file=sys.stderr)
        return 3

    data = json.loads(payload_text)
    data["provenance"] = {
        "upstream_commit": locked_commit(),
        "upstream_notebook_sha256": hash_before,
        "source_cells": SOURCE_CELLS,
        "notebook_unmodified": True,
        "extractor": str(Path(__file__).resolve().relative_to(PROJECT_ROOT)),
        "numpy": version("numpy"),
        "scipy": version("scipy"),
        "solver_convention": {
            "method": "RK45",
            "rtol": 1e-3,
            "atol": 1e-6,
            "max_step": "inf",
            "first_step": None,
            "source": "scipy.integrate.solve_ivp defaults made explicit",
        },
    }
    ORACLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    ORACLE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(
        f"Oracle written: {ORACLE_PATH.relative_to(PROJECT_ROOT)} "
        f"({len(data['t_eval'])} samples; notebook unchanged)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
