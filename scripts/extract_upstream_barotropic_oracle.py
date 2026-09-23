"""Extract pinned upstream Timescape barotropic trajectories read-only.

Only notebook cells 0-8, 12, and 15 are executed in memory.  A new sampling
cell runs the three Figure-3 modes and serialises numerical trajectories; no
executed notebook or upstream source is written.  Both upstream commit and
notebook SHA-256 are checked before and after execution and against the
validated Phase 1C-B1 provenance.

Output: ``artifacts/upstream/oracle_barotropic_perturbations.json``.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_ROOT = (
    PROJECT_ROOT
    / ".reference"
    / "Linear-Perturbations-in-averaged-cosmological-models"
)
UPSTREAM_NOTEBOOK = UPSTREAM_ROOT / "ACPT_Timescape.ipynb"
UPSTREAM_LOCK = PROJECT_ROOT / "UPSTREAM.lock"
ORACLE_PATH = PROJECT_ROOT / "artifacts" / "upstream" / "oracle_barotropic_perturbations.json"
SOURCE_CELLS = [*range(0, 9), 12, 15]
CELL_TIMEOUT_S = 600
EXPECTED_COMMIT = "590c6fd5332acb15f5683ebf392a0d7ce54983c5"
# Line-ending-independent notebook pin (UPSTREAM.lock ``notebook_sha256_lf``,
# review finding F6): SHA-256 of the bytes with CRLF normalised to LF, equal to
# the committed Git blob.  The raw hash depends on core.autocrlf and is only
# recorded.
EXPECTED_NOTEBOOK_SHA256_LF = (
    "628c441288d67854e0380518841dede3680bddab610e9ef5cea04937455cea2a"
)

SAMPLING_SOURCE = r"""
import json as _json

_k_values = [2*np.pi, 5*np.pi, 10*np.pi]
_solutions = {float(_k): solnum_barotropic(_k, t_eval, ic) for _k in _k_values}
_payload = {
    "constants": {
        "fv0": float(fv0), "h": float(h), "GyrstoHT": float(GyrstoHT),
        "G": float(G), "H0": float(H0), "HD0": float(HD0),
        "t0": float(t0), "a0": float(a0),
    },
    "initial_conditions": [float(x) for x in ic],
    "t_eval": [float(x) for x in t_eval],
    "k_values": [float(x) for x in _k_values],
    "barotropic": {
        format(_k, ".17g"): {
            "t": [float(x) for x in _solutions[_k].t],
            "y": [[float(x) for x in row] for row in _solutions[_k].y],
            "success": bool(_solutions[_k].success),
            "message": str(_solutions[_k].message),
            "nfev": int(_solutions[_k].nfev),
            "njev": int(_solutions[_k].njev),
            "nlu": int(_solutions[_k].nlu),
        }
        for _k in _k_values
    },
}
print("BAROTROPIC_ORACLE_BEGIN")
print(_json.dumps(_payload))
print("BAROTROPIC_ORACLE_END")
"""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_lf(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def lock_value(name: str) -> str:
    for line in UPSTREAM_LOCK.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith(f"{name}") and "=" in line:
            return line.split("=", 1)[1].strip()
    raise RuntimeError(f"UPSTREAM.lock contains no {name} entry")


def upstream_commit() -> str:
    result = subprocess.run(
        [
            "git",
            f"--git-dir={UPSTREAM_ROOT / '.git'}",
            f"--work-tree={UPSTREAM_ROOT}",
            "rev-parse",
            "HEAD",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> int:
    import nbformat
    from nbclient import NotebookClient

    if not UPSTREAM_NOTEBOOK.exists():
        print(f"ERROR: missing upstream notebook: {UPSTREAM_NOTEBOOK}", file=sys.stderr)
        return 2
    locked_commit = lock_value("commit")
    locked_path = lock_value("local_path")
    locked_lf_hash = lock_value("notebook_sha256_lf")
    expected_relative = str(UPSTREAM_NOTEBOOK.relative_to(PROJECT_ROOT)).replace("\\", "/")
    if (
        locked_commit != EXPECTED_COMMIT
        or locked_path != expected_relative
        or locked_lf_hash != EXPECTED_NOTEBOOK_SHA256_LF
    ):
        print("FATAL: UPSTREAM.lock no longer matches validated B1 provenance", file=sys.stderr)
        return 3

    commit_before = upstream_commit()
    hash_before = sha256(UPSTREAM_NOTEBOOK)
    lf_hash_before = sha256_lf(UPSTREAM_NOTEBOOK)
    if commit_before != EXPECTED_COMMIT or lf_hash_before != EXPECTED_NOTEBOOK_SHA256_LF:
        print("FATAL: upstream commit or notebook hash differs before extraction", file=sys.stderr)
        return 4

    source = nbformat.read(UPSTREAM_NOTEBOOK, as_version=4)
    notebook = nbformat.v4.new_notebook(metadata=source.metadata)
    notebook.cells = [source.cells[index] for index in SOURCE_CELLS]
    notebook.cells.append(nbformat.v4.new_code_cell(SAMPLING_SOURCE))
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
        if "BAROTROPIC_ORACLE_BEGIN" in stream:
            payload_text = stream.split("BAROTROPIC_ORACLE_BEGIN", 1)[1].split(
                "BAROTROPIC_ORACLE_END", 1
            )[0].strip()
    if payload_text is None:
        print("ERROR: oracle sampling cell produced no payload", file=sys.stderr)
        return 5

    commit_after = upstream_commit()
    hash_after = sha256(UPSTREAM_NOTEBOOK)
    lf_hash_after = sha256_lf(UPSTREAM_NOTEBOOK)
    if (
        commit_after != commit_before
        or hash_after != hash_before
        or lf_hash_after != lf_hash_before
    ):
        print("FATAL: upstream commit or notebook hash changed during extraction", file=sys.stderr)
        return 6

    data = json.loads(payload_text)
    data["provenance"] = {
        "upstream_commit_before": commit_before,
        "upstream_commit_after": commit_after,
        "upstream_notebook_path": expected_relative,
        "upstream_notebook_sha256_before": hash_before,
        "upstream_notebook_sha256_after": hash_after,
        "upstream_notebook_sha256_lf_normalized_before": lf_hash_before,
        "upstream_notebook_sha256_lf_normalized_after": lf_hash_after,
        "source_cells": SOURCE_CELLS,
        "notebook_unmodified": True,
        "extractor": str(Path(__file__).resolve().relative_to(PROJECT_ROOT)).replace(
            "\\", "/"
        ),
        "numpy": version("numpy"),
        "scipy": version("scipy"),
        "scenario": {
            "sound_speed": "upstream_d2_corrupted",
            "branch": "printed_4_15",
            "tilt_form": "unrescaled_V",
            "rate_convention": "upstream_unconverted",
            "epoch": "upstream_0p218_gyr",
            "wavenumber_convention": "upstream_timescape_k",
        },
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
        f"({len(data['t_eval'])} samples x {len(data['k_values'])} modes; "
        "commit/hash unchanged)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
