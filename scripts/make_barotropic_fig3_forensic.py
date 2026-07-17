"""Generate separate Figure-3 views from the pinned upstream oracle.

This deliberately forensic script is the only Figure-3 plotter that consumes
upstream-derived trajectories.  It emits both the notebook's raw effective
contrast and the paper-caption Delta_eff/k^2 interpretation.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from _phase1c_b2_plot_styles import style_for_k  # noqa: E402


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ORACLE_PATH = (
    PROJECT_ROOT / "artifacts" / "upstream" / "oracle_barotropic_perturbations.json"
)
OUT_DIR = PROJECT_ROOT / "artifacts" / "independent"
COLORS = ("royalblue", "crimson", "forestgreen")


def complete_identifier(k: float) -> str:
    """Identify every convention in the pinned notebook run."""
    return (
        "sound=upstream_d2_corrupted|branch=printed_4_15|"
        "tilt=unrescaled_V|rate=upstream_unconverted|"
        "epoch=upstream_0p218_gyr|k_convention=upstream_timescape_k|"
        f"k={k:.17g}|h_ts=0.73229999999999995|h_lcdm=0.67400000000000004"
    )


def make_figure(oracle: dict, *, divide_effective_by_k2: bool) -> Path:
    """Plot only oracle data; no scientific-package trajectory is overlaid."""
    constants = oracle["constants"]
    fv0 = float(constants["fv0"])
    hd0 = float(constants["HD0"])
    t0 = float(constants["t0"])
    # [GM] Eqs. (5.5)-(5.6), used only to recover the upstream plot
    # coordinate from the oracle constants, not as scientific package code.
    t_eval = np.asarray(oracle["t_eval"], dtype=np.float64)
    x = 3.0 * fv0 * hd0 * t_eval
    fv = x / (x + (2.0 + fv0) * (1.0 - fv0))
    a_d0 = 1.0 + fv0 / 2.0
    a_d = a_d0 * (t_eval / t0) * np.cbrt(fv0 / fv)
    if not np.all(np.isfinite(a_d)):  # pragma: no cover - provenance guard
        raise ValueError("invalid pinned tracker constants")

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 7.6))
    identifiers = []
    for k, color in zip(oracle["k_values"], COLORS, strict=True):
        k = float(k)
        style = style_for_k(k)
        description = style.pop("description")
        key = format(k, ".17g")
        y = np.asarray(oracle["barotropic"][key]["y"], dtype=np.float64)
        label = rf"$k={k / np.pi:g}\pi$ ({description})"
        axes[0].plot(
            a_d, np.abs(y[0]), color=color, lw=2, label=label, **style
        )
        divisor = k**2 if divide_effective_by_k2 else 1.0
        axes[1].plot(
            a_d,
            np.abs(y[2]) / divisor,
            color=color,
            lw=2,
            label=label,
            **style,
        )
        identifiers.append(complete_identifier(k))

    for axis in axes:
        axis.set_yscale("log")
        axis.set_xlim(float(a_d[0]), float(a_d[-1]))
        axis.set_xlabel(r"$a_{\mathcal{D}}/a_{w,0}$")
        axis.grid(alpha=0.3)
        axis.legend()
    axes[0].set_ylabel(r"$|\Delta^{(d)}_{\rm bar}|$")
    axes[1].set_ylabel(
        r"$|\Delta^{(\rm eff)}_{\rm bar}|/k^2$"
        if divide_effective_by_k2
        else r"$|\Delta^{(\rm eff)}_{\rm bar}|$ (raw, notebook cell 19)"
    )
    right_label = "Delta_eff/k^2" if divide_effective_by_k2 else "raw Delta_eff"
    fig.suptitle(
        "FORENSIC ONLY: pinned upstream [GM] Figure 3 trajectories\n"
        f"right panel={right_label}; solve_ivp RK45 defaults",
        fontsize=12,
    )
    provenance = oracle["provenance"]
    fig.text(
        0.01,
        0.008,
        "\n".join(identifiers)
        + f"\ncommit={provenance['upstream_commit_before']}|"
        f"notebook_sha256={provenance['upstream_notebook_sha256_before']}",
        ha="left",
        va="bottom",
        fontsize=5.8,
        family="monospace",
    )
    fig.tight_layout(rect=(0.0, 0.17, 1.0, 0.94))
    suffix = "over_k2" if divide_effective_by_k2 else "raw"
    base = OUT_DIR / f"fig3_forensic_upstream_{suffix}"
    fig.savefig(base.with_suffix(".png"), dpi=200)
    fig.savefig(base.with_suffix(".pdf"))
    plt.close(fig)
    return base


def main() -> int:
    if not ORACLE_PATH.exists():
        print(f"ERROR: missing {ORACLE_PATH}; run the extraction script first")
        return 2
    oracle = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for divide in (False, True):
        base = make_figure(oracle, divide_effective_by_k2=divide)
        print(f"Written: {base.relative_to(PROJECT_ROOT)}.png / .pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
