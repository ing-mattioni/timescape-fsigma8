"""Generate corrected-sound-speed Figure-3 variants independently.

This script imports only the scientific package.  It never reads the upstream
oracle.  The two unresolved D3 branches are emitted as separate, equally
labelled outputs; each has a raw-Delta_eff and Delta_eff/k^2 right panel.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import timescape_fsigma8.background as bg  # noqa: E402
from _phase1c_b2_plot_styles import style_for_k  # noqa: E402
from timescape_fsigma8.background import TrackerParams  # noqa: E402
from timescape_fsigma8.perturbations import (  # noqa: E402
    PHASE1C_EPOCH_ROOT,
    PLANCK_2018_QPLUS_RECIPE,
    TIGHT_DOP853,
    UPSTREAM_NOTEBOOK_TIME_UNIT,
    BarotropicScenario,
    D3Branch,
    EpochChoice,
    EpochScenario,
    RateUnitConvention,
    TiltForm,
    WavenumberConvention,
    solve_barotropic,
)


OUT_DIR = PROJECT_ROOT / "artifacts" / "independent"
K_VALUES = (2.0 * np.pi, 5.0 * np.pi, 10.0 * np.pi)
COLORS = ("royalblue", "crimson", "forestgreen")
N_POINTS = 1000


def scenario(k: float, branch: D3Branch) -> BarotropicScenario:
    """Return the fully identified corrected-background comparison scenario."""
    return BarotropicScenario(
        k=k,
        branch=branch,
        tilt_form=TiltForm.UNRESCALED_V,
        rate_convention=RateUnitConvention.UPSTREAM_UNCONVERTED,
        epoch_choice=EpochChoice.UPSTREAM_0P218_GYR,
        wavenumber_convention=WavenumberConvention.UPSTREAM_TIMESCAPE_K,
        timescape_h=0.7323,
        lcdm_h=0.674,
    )


def setup():
    params = TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0)
    epoch = EpochScenario(
        choice=EpochChoice.UPSTREAM_0P218_GYR,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        root=PHASE1C_EPOCH_ROOT,
    ).resolve(params)
    t_eval = np.linspace(epoch.time, params.t0, N_POINTS)
    return params, t_eval


def make_figure(branch: D3Branch, *, divide_effective_by_k2: bool) -> Path:
    """Plot [GM] Figure 3 for one explicit D3 branch and right-panel choice."""
    params, t_eval = setup()
    solutions = []
    scenarios = []
    for k in K_VALUES:
        selected = scenario(k, branch)
        scenarios.append(selected)
        solutions.append(
            solve_barotropic(
                params=params,
                scenario=selected,
                recipe=PLANCK_2018_QPLUS_RECIPE,
                time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
                epoch_root=PHASE1C_EPOCH_ROOT,
                t_eval=t_eval,
                config=TIGHT_DOP853,
                G=1.0,
            )
        )

    x = bg.a_D(t_eval, params)
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 7.6))
    for selected, solution, color in zip(scenarios, solutions, COLORS, strict=True):
        style = style_for_k(selected.k)
        description = style.pop("description")
        label = rf"$k={selected.k / np.pi:g}\pi$ ({description})"
        axes[0].plot(
            x, np.abs(solution.y[0]), color=color, lw=2, label=label, **style
        )
        divisor = selected.k**2 if divide_effective_by_k2 else 1.0
        axes[1].plot(
            x,
            np.abs(solution.y[2]) / divisor,
            color=color,
            lw=2,
            label=label,
            **style,
        )

    for axis in axes:
        axis.set_yscale("log")
        axis.set_xlim(float(x[0]), float(x[-1]))
        axis.set_xlabel(r"$a_{\mathcal{D}}/a_{w,0}$")
        axis.grid(alpha=0.3)
        axis.legend()
    axes[0].set_ylabel(r"$|\Delta^{(d)}_{\rm bar}|$")
    axes[1].set_ylabel(
        r"$|\Delta^{(\rm eff)}_{\rm bar}|/k^2$"
        if divide_effective_by_k2
        else r"$|\Delta^{(\rm eff)}_{\rm bar}|$ (raw, not divided by $k^2$)"
    )
    right_label = "Delta_eff/k^2" if divide_effective_by_k2 else "raw Delta_eff"
    fig.suptitle(
        "Independent corrected-$c_s^2$ [GM] Figure 3\n"
        f"D3 branch={branch.value}; right panel={right_label}",
        fontsize=12,
    )
    # Every plotted mode carries its complete scenario identifier in the
    # figure itself, not only in a sidecar or terminal message.
    identifiers = "\n".join(selected.identifier for selected in scenarios)
    fig.text(
        0.01,
        0.008,
        identifiers
        + f"\nsolver=DOP853|rtol={TIGHT_DOP853.rtol:.17g}|"
        f"atol={TIGHT_DOP853.atol:.17g}|sound_speed=corrected_phase1b",
        ha="left",
        va="bottom",
        fontsize=5.8,
        family="monospace",
    )
    fig.tight_layout(rect=(0.0, 0.17, 1.0, 0.94))
    suffix = "over_k2" if divide_effective_by_k2 else "raw"
    base = OUT_DIR / f"fig3_corrected_{branch.value}_{suffix}"
    fig.savefig(base.with_suffix(".png"), dpi=200)
    fig.savefig(base.with_suffix(".pdf"))
    plt.close(fig)
    return base


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for branch in D3Branch:
        for divide in (False, True):
            base = make_figure(branch, divide_effective_by_k2=divide)
            print(f"Written: {base.relative_to(PROJECT_ROOT)}.png / .pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
