"""Independent reproduction of [GM] Fig. 1 from our package only.

Generates, for each preset (PAPER_REFERENCE, NOTEBOOK_REFERENCE):

  artifacts/independent/fig1_reproduction_<PRESET>.png/.pdf
    Left panel:  bare density parameters Omega_m, Omega_R, Omega_Q vs
                 a_D/a_{w,0}  ([GM] Fig. 1 left).
    Right panel: w_eff and the CORRECTED c^2_{s,eff} ([GM] Fig. 1 right).
                 The published right panel embeds the upstream dQDdt
                 defect (deviation D2); our curve is the independently
                 derived correct one and INTENTIONALLY differs from the
                 published figure.

and one forensic comparison (only if the local oracle exists):

  artifacts/independent/fig1_right_forensic_D2.png/.pdf
    Correct c^2_{s,eff} (ours) overlaid with the D2-affected upstream
    curve sampled from the oracle, endpoints annotated.

Every plotted value comes from timescape_fsigma8 (independent
implementation); the oracle JSON is read only for the forensic overlay.
No upstream plotting code is used.

Note on presets: both share f_v0 = 0.737, and every curve here is a
dimensionless quantity plotted against the dimensionless a_D/a_{w,0}, so
the two presets' curves coincide identically; the H0 difference changes
only the physical time/redshift mapping of the axis (annotated on each
figure). Both are still emitted, parameter-stamped, for traceability.

Colors match the published figure's semantics for side-by-side
comparability (its red/green pairing is not CVD-safe: deutan dE ~ 3);
identity is therefore never encoded by color alone — every curve has a
distinct linestyle and a legend entry.

Time range: t = 0.18 Gyr (upstream background start, converted per
preset) to t0, 2000 points.
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

import timescape_fsigma8.background as bg               # noqa: E402
from timescape_fsigma8.presets import (                 # noqa: E402
    NOTEBOOK_REFERENCE,
    PAPER_REFERENCE,
)

OUT_DIR = PROJECT_ROOT / "artifacts" / "independent"
ORACLE_PATH = PROJECT_ROOT / "artifacts" / "upstream" / "oracle_background.json"

# Published-figure color semantics (comparability); linestyles carry
# identity independently of color.
C_OMEGA_M, C_OMEGA_R, C_OMEGA_Q = "forestgreen", "crimson", "royalblue"
C_WEFF, C_CS2 = "royalblue", "crimson"

T_START_GYR = 0.18   # upstream background-figure start (Phase 1A audit §5)
N_PTS = 2000


def make_fig1(preset) -> Path:
    p = preset.tracker_params_gyr
    t = np.linspace(T_START_GYR, p.t0, N_PTS)
    x = bg.a_D(t, p)

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    axL.plot(x, bg.Omega_m(t, p), color=C_OMEGA_M, lw=2, ls="-",
             label=r"$\Omega^{\mathcal{D}}_{d}$")
    axL.plot(x, bg.Omega_R(t, p), color=C_OMEGA_R, lw=2, ls="--",
             label=r"$\Omega^{\mathcal{D}}_{R}$")
    axL.plot(x, bg.Omega_Q(t, p), color=C_OMEGA_Q, lw=2, ls="-.",
             label=r"$\Omega^{\mathcal{D}}_{Q}$")
    axL.axhline(0.0, color="k", ls=":", lw=0.8)
    axL.set_xlabel(r"$a_{\mathcal{D}}/a_{w,0}$", fontsize=12)
    axL.set_ylabel(r"$\Omega^{\mathcal{D}}_{i}$", fontsize=12)
    axL.set_xlim(x[0], x[-1])
    axL.legend(fontsize=10, loc="center right")
    axL.grid(alpha=0.3)

    axR.plot(x, bg.w_eff(t, p), color=C_WEFF, lw=2, ls="-",
             label=r"$w_{\mathrm{eff},\mathcal{D}}$")
    axR.plot(x, bg.cs2_eff(t, p), color=C_CS2, lw=2, ls="--",
             label=r"$c^{2}_{s,\mathrm{eff},\mathcal{D}}$ (corrected; D2)")
    axR.set_xlabel(r"$a_{\mathcal{D}}/a_{w,0}$", fontsize=12)
    axR.set_ylabel(r"$w$, $c_{s}^{2}$", fontsize=12)
    axR.set_xlim(x[0], x[-1])
    axR.legend(fontsize=10, loc="lower right")
    axR.grid(alpha=0.3)

    fig.suptitle(
        f"Independently derived timescape background — {preset.name} "
        f"($f_{{v,0}}$ = {preset.fv0}, $H_0$ = "
        f"{preset.H0_dressed_km_s_Mpc} km/s/Mpc)\n"
        "timescape_fsigma8 reproduction of [GM] Fig. 1; right panel uses the "
        "corrected $c^2_{s,\\mathrm{eff}}$ and intentionally differs from the "
        "published curve (deviation D2)",
        fontsize=10)
    fig.text(0.99, 0.01,
             f"t = {T_START_GYR} Gyr (z = {float(bg.redshift(T_START_GYR, p)):.2f}) "
             f"to t0 = {p.t0:.3f} Gyr; dimensionless curves are preset-independent "
             "(shared f_v0); H0 changes only the time/redshift mapping",
             ha="right", va="bottom", fontsize=7, color="0.35")
    fig.tight_layout(rect=(0, 0.03, 1, 0.90))

    base = OUT_DIR / f"fig1_reproduction_{preset.name}"
    fig.savefig(base.with_suffix(".png"), dpi=200)
    fig.savefig(base.with_suffix(".pdf"))
    plt.close(fig)
    return base


def make_forensic() -> Path | None:
    if not ORACLE_PATH.exists():
        print("Oracle absent — skipping forensic D2 figure "
              "(run scripts/extract_upstream_oracle.py to enable).")
        return None
    oracle = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))
    t_cu = np.asarray(oracle["t"])                     # upstream code units
    c = oracle["constants"]
    op = bg.TrackerParams(fv0=c["fv0"], HD0=c["HD0"])  # same units as oracle
    x = bg.a_D(t_cu, op)
    ours = bg.cs2_eff(t_cu, op)
    theirs = np.asarray(oracle["values"]["cs2Eff"])

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(x, bg.w_eff(t_cu, op), color="0.55", lw=1.5, ls="-",
            label=r"$w_{\mathrm{eff},\mathcal{D}}$ (context; both agree)")
    ax.plot(x, ours, color=C_CS2, lw=2.2, ls="-",
            label=r"$c^{2}_{s,\mathrm{eff}}$ correct (this work)")
    ax.plot(x, theirs, color="k", lw=2.2, ls=":",
            label=r"$c^{2}_{s,\mathrm{eff}}$ upstream/published (D2-affected)")
    ax.annotate(f"{ours[-1]:.4f} (correct)", (x[-1], ours[-1]),
                xytext=(-115, -16), textcoords="offset points",
                fontsize=9, color=C_CS2)
    ax.annotate(f"{theirs[-1]:.4f} (published Fig. 1)", (x[-1], theirs[-1]),
                xytext=(-150, -16), textcoords="offset points",
                fontsize=9, color="k")
    ax.set_xlabel(r"$a_{\mathcal{D}}/a_{w,0}$", fontsize=12)
    ax.set_ylabel(r"$c_{s}^{2}$, $w$", fontsize=12)
    ax.set_xlim(x[0], x[-1])
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(alpha=0.3)
    ax.set_title(
        "Forensic comparison (deviation D2): effective sound speed\n"
        "upstream dQDdt defect vs correct derivative ($f_{v,0}$ = 0.737)",
        fontsize=10)
    fig.tight_layout()

    base = OUT_DIR / "fig1_right_forensic_D2"
    fig.savefig(base.with_suffix(".png"), dpi=200)
    fig.savefig(base.with_suffix(".pdf"))
    plt.close(fig)
    return base


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for preset in (PAPER_REFERENCE, NOTEBOOK_REFERENCE):
        base = make_fig1(preset)
        print(f"Written: {base}.png / .pdf")
    forensic = make_forensic()
    if forensic:
        print(f"Written: {forensic}.png / .pdf")
    return 0


if __name__ == "__main__":
    sys.exit(main())
