"""Reproduce the clean content of [GM] Figure 2 independently.

Canonical output uses only ``timescape_fsigma8`` with the upstream-compatible
epoch/IC interpretation and the converged DOP853 configuration.  If the local
git-ignored numerical oracle exists, a separate forensic overlay is emitted;
the canonical figure never reads upstream data or code.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import timescape_fsigma8.background as bg  # noqa: E402
from timescape_fsigma8.background import TrackerParams  # noqa: E402
from timescape_fsigma8.perturbations import (  # noqa: E402
    PHASE1C_EPOCH_ROOT,
    PLANCK_2018_QPLUS_RECIPE,
    TIGHT_DOP853,
    UPSTREAM_NOTEBOOK_TIME_UNIT,
    UPSTREAM_RK45_DEFAULTS,
    EpochChoice,
    EpochScenario,
    InitialConditionScenario,
    RateUnitConvention,
    solve_comoving,
    solve_meszaros,
)


OUT_DIR = PROJECT_ROOT / "artifacts" / "independent"
ORACLE_PATH = PROJECT_ROOT / "artifacts" / "upstream" / "oracle_clean_perturbations.json"
N_POINTS = 1000


def setup():
    params = TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0)
    epoch = EpochScenario(
        choice=EpochChoice.UPSTREAM_0P218_GYR,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        root=PHASE1C_EPOCH_ROOT,
    ).resolve(params)
    initial = InitialConditionScenario(
        recipe=PLANCK_2018_QPLUS_RECIPE,
        rate_units=RateUnitConvention.UPSTREAM_UNCONVERTED,
        timescape_h=0.7323,
    ).resolve(params)
    t_eval = np.linspace(epoch.time, params.t0, N_POINTS)
    return params, epoch, initial, t_eval


def style_axis(ax, x):
    ax.set_xlabel(r"$a_{\mathcal{D}}/a_{w,0}$", fontsize=12)
    ax.set_ylabel(r"$\Delta$", fontsize=12)
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(1e-3, 1e-1)
    ax.set_yscale("log")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=10)


def make_canonical() -> Path:
    params, epoch, initial, t_eval = setup()
    comoving = solve_comoving(
        params=params, initial_conditions=initial, t_eval=t_eval,
        config=TIGHT_DOP853, G=1.0
    )
    meszaros = solve_meszaros(
        params=params, initial_conditions=initial, t_eval=t_eval,
        config=TIGHT_DOP853, G=1.0
    )
    x = bg.a_D(t_eval, params)
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.plot(x, comoving.y[0], color="crimson", lw=2, ls="-",
            label=r"$\Delta^{(d)}_{\rm com}$")
    ax.plot(x, meszaros.y[0], color="royalblue", lw=2, ls="-.",
            label=r"$\Delta^{(d)}_{\rm mz}$")
    ax.plot(x, comoving.y[2], color="forestgreen", lw=2, ls="--",
            label=r"$\Delta^{(\rm eff)}_{\rm com}$")
    style_axis(ax, x)
    ax.set_title("Independent, converged reproduction of [GM] Figure 2\n"
                 "upstream epoch and unconverted-Z scenario", fontsize=10)
    fig.text(
        0.99, 0.01,
        f"DOP853 rtol={TIGHT_DOP853.rtol:.0e}, atol={TIGHT_DOP853.atol:.0e}; "
        f"t_i={epoch.time_gyr:.3f} Gyr (dressed z={epoch.dressed_redshift:.3f})",
        ha="right", fontsize=7, color="0.35",
    )
    fig.tight_layout(rect=(0.0, 0.035, 1.0, 1.0))
    base = OUT_DIR / "fig2_clean_independent"
    fig.savefig(base.with_suffix(".png"), dpi=200)
    fig.savefig(base.with_suffix(".pdf"))
    plt.close(fig)
    return base


def make_forensic() -> Path | None:
    if not ORACLE_PATH.exists():
        print("Oracle absent: skipping forensic Figure-2 overlay")
        return None
    oracle = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))
    params, _, initial, t_eval = setup()
    comoving = solve_comoving(
        params=params, initial_conditions=initial, t_eval=t_eval,
        config=UPSTREAM_RK45_DEFAULTS, G=oracle["constants"]["G"]
    )
    meszaros = solve_meszaros(
        params=params, initial_conditions=initial, t_eval=t_eval,
        config=UPSTREAM_RK45_DEFAULTS, G=oracle["constants"]["G"]
    )
    x = bg.a_D(t_eval, params)
    oracle_comoving = np.asarray(oracle["comoving"]["y"])
    oracle_meszaros = np.asarray(oracle["meszaros"]["y"])

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.plot(x, comoving.y[0], color="crimson", lw=2, label="independent comoving dust")
    ax.plot(x, meszaros.y[0], color="royalblue", lw=2, ls="-.",
            label="independent Mészáros dust")
    ax.plot(x, comoving.y[2], color="forestgreen", lw=2, ls="--",
            label="independent comoving effective")
    ax.plot(x, oracle_comoving[0], color="black", lw=1, ls=":",
            label="upstream oracle overlays")
    ax.plot(x, oracle_meszaros[0], color="black", lw=1, ls=":")
    ax.plot(x, oracle_comoving[2], color="black", lw=1, ls=":")
    style_axis(ax, x)
    ax.set_title("Forensic Figure-2 overlay: independent vs upstream oracle", fontsize=10)
    fig.tight_layout()
    base = OUT_DIR / "fig2_forensic_upstream_overlay"
    fig.savefig(base.with_suffix(".png"), dpi=200)
    fig.savefig(base.with_suffix(".pdf"))
    plt.close(fig)
    return base


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    canonical = make_canonical()
    print(f"Written: {canonical}.png / .pdf")
    forensic = make_forensic()
    if forensic is not None:
        print(f"Written: {forensic}.png / .pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
