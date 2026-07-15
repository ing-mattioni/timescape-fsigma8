"""Full error statistics: independent implementation vs the upstream oracle.

Reads artifacts/upstream/oracle_background.json (produced by
scripts/extract_upstream_oracle.py; 501 samples of 21 upstream background
quantities in upstream code units) and computes, for every quantity:

  max_abs_err   max_t |ours - upstream|          (units of the quantity)
  max_rel_err   max_t |ours - upstream| / |upstream|
  rms_rel_err   sqrt(mean_t of the squared relative error)
  t_at_max_rel  time of the maximum relative error (code units and Gyr)

Quantities are split into two tables:

  EQUIVALENT      same mathematics on both sides (different algebra);
                  agreement is expected at double-precision rounding.
  D2_DISCREPANCY  upstream quantities affected by the notebook's dQDdt
                  algebra defect (documented deviation D2): dQDdt, dKDdt,
                  drhoEffdt, dpEffdt, cs2Eff. These are NOT equivalent by
                  design; the same statistics quantify the *expected*
                  discrepancy of upstream w.r.t. the correct derivatives.

The morphon potential/kinetic energies U_D, K_D and their derivatives are
not part of our package's public API ([GM] does not use them; they are the
notebook's intermediate route to rho_eff/p_eff). They are compared here as
derived combinations of our functions (mapping documented inline) so that
every oracle quantity is covered.

Output: artifacts/independent/oracle_comparison_stats.json (machine-
readable; also embeds environment and oracle provenance) and a markdown
table on stdout for pasting into reports/background_validation.md.
Exit code 1 if any EQUIVALENT quantity exceeds RTOL_GATE.
"""

from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import timescape_fsigma8.background as bg               # noqa: E402
from timescape_fsigma8.background import TrackerParams  # noqa: E402

ORACLE_PATH = PROJECT_ROOT / "artifacts" / "upstream" / "oracle_background.json"
OUT_PATH = PROJECT_ROOT / "artifacts" / "independent" / "oracle_comparison_stats.json"

# Gate for equivalent quantities (same as tests): generous vs the measured
# ~1e-15 level, strict vs any real defect.
RTOL_GATE = 1e-9


def our_values(name: str, t: np.ndarray, p: TrackerParams, G: float) -> np.ndarray:
    """Map an upstream oracle quantity to our implementation.

    U_D, K_D and derivatives are the notebook's morphon intermediates
    (cell 7): U_D = -<R>_D/(24 pi G), K_D = -Q_D/(8 pi G) + U_D (c = 1),
    reconstructed here from our R_D/Q_D (both independently validated).
    """
    direct = {
        "fv": lambda: bg.fv(t, p),
        "dfvdt": lambda: bg.dfv_dt(t, p),
        "d2fvdt": lambda: bg.d2fv_dt2(t, p),
        "a": lambda: bg.a_D(t, p),
        "daDdt": lambda: bg.da_D_dt(t, p),
        "Theta": lambda: bg.Theta(t, p),
        "RD": lambda: bg.R_D(t, p),
        "QD": lambda: bg.Q_D(t, p),
        "dRDdt": lambda: bg.dR_D_dt(t, p),
        "dQDdt": lambda: bg.dQ_D_dt(t, p),
        "rhod": lambda: bg.rho_d(t, p, G),
        "rhoEff": lambda: bg.rho_eff(t, p, G),
        "pEff": lambda: bg.p_eff(t, p, G),
        "drhoEffdt": lambda: bg.drho_eff_dt(t, p, G),
        "dpEffdt": lambda: bg.dp_eff_dt(t, p, G),
        "wEff": lambda: bg.w_eff(t, p),
        "cs2Eff": lambda: bg.cs2_eff(t, p),
        # morphon intermediates (derived combinations):
        "UD": lambda: -bg.R_D(t, p) / (24.0 * np.pi * G),
        "KD": lambda: -bg.Q_D(t, p) / (8.0 * np.pi * G) - bg.R_D(t, p) / (24.0 * np.pi * G),
        "dUDdt": lambda: -bg.dR_D_dt(t, p) / (24.0 * np.pi * G),
        "dKDdt": lambda: -bg.dQ_D_dt(t, p) / (8.0 * np.pi * G) - bg.dR_D_dt(t, p) / (24.0 * np.pi * G),
    }
    return np.asarray(direct[name]())


# Upstream quantities downstream of the dQDdt defect (D2).
D2_AFFECTED = ["dQDdt", "dKDdt", "drhoEffdt", "dpEffdt", "cs2Eff"]


def stats(ours: np.ndarray, theirs: np.ndarray, t: np.ndarray,
          gyrs_per_code_unit: float) -> dict:
    abs_err = np.abs(ours - theirs)
    rel_err = abs_err / np.abs(theirs)
    i = int(np.argmax(rel_err))
    return {
        "max_abs_err": float(abs_err.max()),
        "max_rel_err": float(rel_err.max()),
        "rms_rel_err": float(np.sqrt(np.mean(rel_err**2))),
        "t_at_max_rel_code_units": float(t[i]),
        "t_at_max_rel_gyr": float(t[i] * gyrs_per_code_unit),
        "index_at_max_rel": i,
    }


def fmt_row(name: str, s: dict) -> str:
    return (f"| `{name}` | {s['max_abs_err']:.3e} | {s['max_rel_err']:.3e} "
            f"| {s['rms_rel_err']:.3e} | {s['t_at_max_rel_gyr']:.4f} |")


def main() -> int:
    if not ORACLE_PATH.exists():
        print(f"ERROR: oracle not found: {ORACLE_PATH}\n"
              "Run scripts/extract_upstream_oracle.py first.", file=sys.stderr)
        return 2

    oracle = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))
    t = np.asarray(oracle["t"])
    c = oracle["constants"]
    p = TrackerParams(fv0=c["fv0"], HD0=c["HD0"])  # upstream code units
    G = c["G"]
    gyr_per_cu = 1.0 / c["GyrstoHT"]  # upstream's own Gyr<->code-unit factor

    equivalent, d2 = {}, {}
    for name, ref in oracle["values"].items():
        s = stats(our_values(name, t, p, G), np.asarray(ref), t, gyr_per_cu)
        (d2 if name in D2_AFFECTED else equivalent)[name] = s

    worst = max(s["max_rel_err"] for s in equivalent.values())
    result = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "oracle": {
            "path": str(ORACLE_PATH.relative_to(PROJECT_ROOT)),
            "samples": int(t.size),
            "upstream_commit": oracle.get("upstream_commit"),
            "upstream_notebook_sha256": oracle.get("upstream_notebook_sha256"),
        },
        "note": ("Equivalent quantities: same mathematics, independent "
                 "algebra; agreement expected at double-precision rounding. "
                 "D2_discrepancy quantities: upstream values affected by the "
                 "notebook's dQDdt defect (deviation D2) — statistics "
                 "quantify the documented upstream error, not our error. "
                 "Times in Gyr use the upstream notebook's own 9.778/h "
                 "convention (oracle grid definition)."),
        "rtol_gate_equivalent": RTOL_GATE,
        "worst_equivalent_max_rel_err": worst,
        "equivalent": equivalent,
        "d2_discrepancy": d2,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")

    header = ("| quantity | max abs err | max rel err | RMS rel err | t(max rel) [Gyr] |\n"
              "|---|---|---|---|---|")
    print(f"Oracle: {t.size} samples, commit {oracle.get('upstream_commit', '?')[:12]}\n")
    print("EQUIVALENT quantities (ours vs upstream; agreement expected):\n")
    print(header)
    for name in sorted(equivalent):
        print(fmt_row(name, equivalent[name]))
    print(f"\nWorst equivalent max_rel_err: {worst:.3e} (gate {RTOL_GATE:.0e})\n")
    print("D2-AFFECTED upstream quantities (documented discrepancy, not error of ours):\n")
    print(header)
    for name in sorted(d2):
        print(fmt_row(name, d2[name]))
    print(f"\nWritten: {OUT_PATH.relative_to(PROJECT_ROOT)}")

    if worst > RTOL_GATE:
        print(f"FAIL: equivalent quantity exceeds gate {RTOL_GATE}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
