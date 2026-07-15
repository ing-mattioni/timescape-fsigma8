"""Sample the upstream notebook's background functions as a numerical oracle.

Executes the *background* cells (0-8: imports, constants, function
definitions) of the pinned upstream ACPT_Timescape.ipynb, unmodified, in a
fresh kernel, then runs an appended sampling cell (our code) in the same
kernel that evaluates every background function on a fixed time grid and
dumps the values to artifacts/upstream/oracle_background.json.

The original notebook is never modified (the executed object lives only in
memory and is not written back). The oracle file contains numerical values
only; it stays under the git-ignored artifacts/upstream/ directory because
it derives from unlicensed upstream code.

Used by tests/test_vs_upstream_oracle.py to validate the independent
implementation in src/timescape_fsigma8/background.py.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_DIR = PROJECT_ROOT / ".reference" / "Linear-Perturbations-in-averaged-cosmological-models"
UPSTREAM_NOTEBOOK = UPSTREAM_DIR / "ACPT_Timescape.ipynb"
ORACLE_PATH = PROJECT_ROOT / "artifacts" / "upstream" / "oracle_background.json"

# Upstream cells that define the background: imports (0), constants (1-3),
# background functions (4-8). Perturbation/plotting cells are not needed.
BACKGROUND_CELLS = range(0, 9)

# Our sampling code, executed in the upstream kernel after cells 0-8.
# It only *calls* upstream functions; every name it references is defined
# by the upstream cells above.
SAMPLING_SOURCE = """
import json as _json
import numpy as _np

# Time grid in upstream code units (H0 = 1): the notebook's own background
# range, 0.18 Gyr to t0 (cell 9 uses the same endpoints).
_ts = _np.linspace(0.18 * GyrstoHT, t0, 501)

_funcs = {
    "fv": fv, "dfvdt": dfvdt, "d2fvdt": d2fvdt,
    "a": a, "daDdt": daDdt, "Theta": Theta,
    "rhod": rhod, "RD": RD, "QD": QD, "dRDdt": dRDdt, "dQDdt": dQDdt,
    "UD": UD, "KD": KD, "dUDdt": dUDdt, "dKDdt": dKDdt,
    "rhoEff": rhoEff, "pEff": pEff, "drhoEffdt": drhoEffdt,
    "dpEffdt": dpEffdt, "wEff": wEff, "cs2Eff": cs2Eff,
}
_out = {
    "t": _ts.tolist(),
    "constants": {
        "fv0": fv0, "h": h, "G": G, "H0": H0, "c": c,
        "GyrstoHT": GyrstoHT, "MpctoHL": MpctoHL,
        "HD0": HD0, "rho0": rho0, "a0": a0, "alpha": alpha, "t0": t0,
    },
    "values": {name: [float(f(_t)) for _t in _ts] for name, f in _funcs.items()},
}
print("ORACLE_JSON_BEGIN")
print(_json.dumps(_out))
print("ORACLE_JSON_END")
"""


def main() -> int:
    import nbformat
    from nbclient import NotebookClient

    src = nbformat.read(UPSTREAM_NOTEBOOK, as_version=4)
    commit = subprocess.run(
        ["git", "-C", str(UPSTREAM_DIR), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()

    nb = nbformat.v4.new_notebook(metadata=src.metadata)
    nb.cells = [src.cells[i] for i in BACKGROUND_CELLS]
    nb.cells.append(nbformat.v4.new_code_cell(SAMPLING_SOURCE))

    client = NotebookClient(nb, timeout=600, kernel_name="python3")
    client.execute()

    payload = None
    for out in nb.cells[-1].outputs:
        if out.output_type == "stream":
            text = "".join(out.text)
            if "ORACLE_JSON_BEGIN" in text:
                payload = text.split("ORACLE_JSON_BEGIN")[1].split("ORACLE_JSON_END")[0].strip()
    if payload is None:
        print("ERROR: sampling cell produced no oracle payload", file=sys.stderr)
        return 1

    data = json.loads(payload)
    data["upstream_commit"] = commit
    data["upstream_notebook_sha256"] = hashlib.sha256(UPSTREAM_NOTEBOOK.read_bytes()).hexdigest()
    data["source_cells"] = list(BACKGROUND_CELLS)

    ORACLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    ORACLE_PATH.write_text(json.dumps(data), encoding="utf-8")
    n = len(data["t"])
    print(f"Oracle written: {ORACLE_PATH.relative_to(PROJECT_ROOT)} "
          f"({n} time samples, {len(data['values'])} quantities, commit {commit[:12]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
