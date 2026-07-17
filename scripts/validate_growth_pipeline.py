"""Phase 1D-B growth-pipeline validation study.

Produces ``artifacts/independent/phase1d_b_growth_validation.json`` using
only the independent local package and the frozen perturbation
infrastructure.  The upstream notebook is neither executed nor modified.

Studies (controlled, one factor at a time — never an uncontrolled
Cartesian product):

  V1 baseline crossing checks against the frozen Phase 1D-A sampled-grid
     brackets (clean systems + both D3 branches x three modes);
  V2 analytic-identity diagnostics (f*D = dD/dlna, chain factor,
     G_Delta = G_m, mapped -1/k_code^2 factor);
  V3 solver convergence against an independent high-accuracy DOP853
     reference (rtol=2e-13, atol=2e-15, every option explicit);
  V4 root convergence across solver methods and sampling densities
     (explicit gate declared before the study, reported unrelaxed);
  V5 tilt-form equivalence diagnostics;
  V6 scale-independence/dependence diagnostics;
  V7 one-factor scenario studies from the declared `validation_baseline`
     (a validation label only - not a public API default and not a
     scientific preference).

The final JSON separates the uncertainty taxonomy: numerical
sampling/root uncertainty, solver method/tolerance uncertainty,
unresolved-convention spread, and model/closure dependence.  No
spectrum-normalisation category exists because spectra and normalisation
are not implemented in this phase.  A convention spread is never a
confidence interval.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import replace
from importlib.metadata import version
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import timescape_fsigma8.background as bg  # noqa: E402
from timescape_fsigma8.perturbations import (  # noqa: E402
    TIGHT_DOP853,
    TIGHT_RADAU,
    TIGHT_RK45,
    EpochChoice,
    RateUnitConvention,
)
from timescape_fsigma8.perturbations.scenarios import PHASE1C_EPOCH_ROOT  # noqa: E402
from timescape_fsigma8.perturbations.solver import SolverConfig  # noqa: E402
from timescape_fsigma8.growth import (  # noqa: E402
    DenseSolveConfig,
    DensityContrastMapping,
    GrowthBackgroundPreset,
    GrowthCoordinate,
    GrowthD3Branch,
    GrowthNumericsConfig,
    GrowthProvenance,
    GrowthReference,
    GrowthReferenceCoordinate,
    GrowthScenario,
    GrowthSystem,
    GrowthTiltForm,
    GrowthWavenumberConvention,
    RootRefineConfig,
    run_growth_pipeline,
)

OUTPUT = PROJECT_ROOT / "artifacts" / "independent" / "phase1d_b_growth_validation.json"
UPSTREAM_NOTEBOOK = (
    PROJECT_ROOT
    / ".reference"
    / "Linear-Perturbations-in-averaged-cosmological-models"
    / "ACPT_Timescape.ipynb"
)
EXPECTED_UPSTREAM_COMMIT = "590c6fd5332acb15f5683ebf392a0d7ce54983c5"

# ----------------------------------------------------------------- numerics
REFERENCE_SOLVER = SolverConfig(
    method="DOP853", rtol=2e-13, atol=2e-15, max_step=np.inf, first_step=None
)
DENSE = DenseSolveConfig(
    method="DOP853", rtol=1e-11, atol=1e-13, max_step=np.inf, first_step=None
)
ROOT = RootRefineConfig(
    xtol=1e-13, rtol=8.9e-16, maxiter=100, residual_scale_gate=1e-6
)
NEAR_ZERO_REL_FLOOR = 1e-9


def numerics(
    solver: SolverConfig = TIGHT_DOP853, n_samples: int = 1000
) -> GrowthNumericsConfig:
    return GrowthNumericsConfig(
        solver=solver,
        n_samples=n_samples,
        G=1.0,
        dense=DENSE,
        root=ROOT,
        near_zero_rel_floor=NEAR_ZERO_REL_FLOOR,
    )


# Validation reference epoch: dressed z = 10 (an explicit validation choice
# recorded here; not a package default, not a scientific preference).
REFERENCE_Z10 = GrowthReference(
    coordinate=GrowthReferenceCoordinate.DRESSED_REDSHIFT,
    value=10.0,
    root=PHASE1C_EPOCH_ROOT,
    amplitude_floor_rel=1e-10,
)

# Explicit gates, declared before the studies run and never relaxed:
GATES = {
    "root_inside_frozen_1da_bracket": True,
    "root_residual_over_scale_max": 1e-9,
    "root_convergence_spread_code_time_max": 1e-8,
    "analytic_identity_rel_max": 1e-11,
    "chain_factor_identity_rel_max": 1e-12,
    "g_delta_equals_g_m_rel_max": 1e-14,
    "solver_convergence_normalized_linf_max": 2e-8,
    "tilt_history_normalized_linf_max": 1e-8,
    "tilt_root_time_abs_max": 1e-8,
    "clean_scale_independence_exact": True,
}
GATE_JUSTIFICATION = {
    "root_convergence_spread_code_time_max": (
        "brentq xtol=1e-13 on a dense rtol=1e-11 representation gives root "
        "reproducibility well under 1e-9 code units; 1e-8 adds a safety "
        "decade and is declared before the study"
    ),
    "solver_convergence_normalized_linf_max": (
        "same normalized-Linf gate as the frozen Phase 1C-B2 convergence "
        "study for tight explicit methods against the DOP853 reference"
    ),
}

FROZEN_1DA_BRACKETS = {
    ("printed_4_15", "2pi"): {"Delta_d": None, "Z": None},
    ("printed_4_15", "5pi"): {
        "Delta_d": (0.22770117509286744, 0.2288375975917282),
        "Z": (0.1401966426805888, 0.14133306517944957),
    },
    ("printed_4_15", "10pi"): {
        "Delta_d": (0.07769340524324692, 0.07882982774210769),
        "Z": (0.05723780026375321, 0.058374222762613975),
    },
    ("derived_4_10", "2pi"): {
        "Delta_d": (0.7845481995346406, 0.7856846220335013),
        "Z": (0.3390705799812221, 0.34020700248008284),
    },
    ("derived_4_10", "5pi"): {
        "Delta_d": (0.15042444517033565, 0.1515608676691964),
        "Z": (0.09701258772387987, 0.09814901022274063),
    },
    ("derived_4_10", "10pi"): {
        "Delta_d": (0.06746560275350007, 0.06860202525236082),
        "Z": (0.05041926527058864, 0.0515556877694494),
    },
}
MODES = [("2pi", 2.0 * np.pi), ("5pi", 5.0 * np.pi), ("10pi", 10.0 * np.pi)]


def clean_scenario(system: GrowthSystem, **overrides) -> GrowthScenario:
    fields = dict(
        perturbation_system=system,
        background_preset=GrowthBackgroundPreset.NOTEBOOK_REFERENCE,
        d3_branch=GrowthD3Branch.NOT_APPLICABLE,
        tilt_form=GrowthTiltForm.NOT_APPLICABLE,
        rate_unit_convention=RateUnitConvention.UPSTREAM_UNCONVERTED,
        epoch_choice=EpochChoice.UPSTREAM_0P218_GYR,
        wavenumber_convention=GrowthWavenumberConvention.NOT_APPLICABLE,
        growth_coordinate=GrowthCoordinate.BARE_AD,
        density_contrast_mapping=DensityContrastMapping.KEEP_DELTA_D,
        supplied_mode_k=None,
        mode_label=None,
    )
    fields.update(overrides)
    return GrowthScenario(**fields)


def barotropic_scenario(
    branch: GrowthD3Branch, k: float, label: str, **overrides
) -> GrowthScenario:
    fields = dict(
        perturbation_system=GrowthSystem.BAROTROPIC,
        background_preset=GrowthBackgroundPreset.NOTEBOOK_REFERENCE,
        d3_branch=branch,
        tilt_form=GrowthTiltForm.UNRESCALED_V,
        rate_unit_convention=RateUnitConvention.UPSTREAM_UNCONVERTED,
        epoch_choice=EpochChoice.UPSTREAM_0P218_GYR,
        wavenumber_convention=GrowthWavenumberConvention.UPSTREAM_TIMESCAPE_K,
        growth_coordinate=GrowthCoordinate.BARE_AD,
        density_contrast_mapping=DensityContrastMapping.KEEP_DELTA_D,
        supplied_mode_k=k,
        mode_label=label,
    )
    fields.update(overrides)
    return GrowthScenario(**fields)


def repo_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def notebook_sha256() -> str:
    return hashlib.sha256(UPSTREAM_NOTEBOOK.read_bytes()).hexdigest()


def error_metrics(reference, other, t, roots) -> dict:
    """Documented denominator policy: per-array global max |reference|.

    Relative error is never taken at a true zero; the normalized-Linf
    denominator is the array's maximum magnitude (a single global scale),
    exactly as in the frozen Phase 1C-B2 metric.
    """
    reference = np.asarray(reference, dtype=np.float64)
    other = np.asarray(other, dtype=np.float64)
    diff = np.abs(reference - other)
    finite = np.isfinite(diff)
    diff = np.where(finite, diff, 0.0)
    scale = max(float(np.nanmax(np.abs(reference))), 1e-300)
    worst = int(np.argmax(diff))
    worst_t = float(t[worst])
    near = min(
        (abs(worst_t - r) for r in roots), default=float("inf")
    )
    dt = float(t[1] - t[0])
    return {
        "max_abs_error": float(np.max(diff)),
        "normalized_linf": float(np.max(diff) / scale),
        "rms_error": float(np.sqrt(np.mean(diff**2))),
        "denominator_policy": "global max |reference| per array",
        "worst_time_solver_units": worst_t,
        "worst_is_near_crossing": bool(near <= 2.0 * dt),
    }


def main() -> int:
    provenance = GrowthProvenance(
        repository_commit=repo_commit(),
        upstream_commit=EXPECTED_UPSTREAM_COMMIT,
        upstream_notebook_sha256=notebook_sha256(),
    )
    gate_failures: list[str] = []
    report: dict = {
        "schema_note": "phase1d_b_growth_validation, v1",
        "provenance": provenance.to_metadata(),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": version("numpy"),
            "scipy": version("scipy"),
        },
        "numerical_configuration": {
            "study_numerics": numerics().to_metadata(),
            "reference_solver": {
                "method": REFERENCE_SOLVER.method,
                "rtol": REFERENCE_SOLVER.rtol,
                "atol": REFERENCE_SOLVER.atol,
                "max_step": "inf",
                "first_step": None,
            },
            "validation_reference_epoch": {
                "coordinate": REFERENCE_Z10.coordinate.value,
                "value": REFERENCE_Z10.value,
                "amplitude_floor_rel": REFERENCE_Z10.amplitude_floor_rel,
                "note": (
                    "explicit validation choice; not a package default and "
                    "not a scientific preference"
                ),
            },
        },
        "gates_declared_before_study": GATES,
        "gate_justification": GATE_JUSTIFICATION,
    }

    # ---------------------------------------------------------------- V1
    print("V1: baseline crossing checks ...")
    v1: dict = {"clean": {}, "barotropic": {}}
    baseline_runs: dict = {}
    for system in (GrowthSystem.MESZAROS, GrowthSystem.COMOVING):
        run = run_growth_pipeline(
            scenario=clean_scenario(system),
            reference=REFERENCE_Z10,
            numerics=numerics(),
            provenance=provenance,
        )
        baseline_runs[system.value] = run
        ok = (
            not run.crossings.delta_d_roots
            and not run.crossings.z_roots
            and len(run.validity_intervals) == 1
        )
        if not ok:
            gate_failures.append(f"clean crossings: {system.value}")
        v1["clean"][system.value] = {
            "delta_d_roots": len(run.crossings.delta_d_roots),
            "z_roots": len(run.crossings.z_roots),
            "validity_intervals": len(run.validity_intervals),
            "no_crossing_gate_passed": ok,
            "run": run.to_json_dict(),
        }
    for branch in (GrowthD3Branch.PRINTED_4_15, GrowthD3Branch.DERIVED_4_10):
        for label, k in MODES:
            run = run_growth_pipeline(
                scenario=barotropic_scenario(branch, k, label),
                reference=REFERENCE_Z10,
                numerics=numerics(),
                provenance=provenance,
            )
            baseline_runs[(branch.value, label)] = run
            frozen = FROZEN_1DA_BRACKETS[(branch.value, label)]
            checks = {}
            for component, roots in (
                ("Delta_d", run.crossings.delta_d_roots),
                ("Z", run.crossings.z_roots),
            ):
                bracket = frozen[component]
                expected = 0 if bracket is None else 1
                count_ok = len(roots) == expected
                inside_ok = True
                residual_ok = True
                if roots and bracket is not None:
                    r = roots[0]
                    inside_ok = bracket[0] < r.t_root < bracket[1]
                    residual_ok = (
                        r.residual
                        <= GATES["root_residual_over_scale_max"]
                        * r.residual_scale
                    )
                if not (count_ok and inside_ok and residual_ok):
                    gate_failures.append(
                        f"V1 {branch.value} {label} {component}: "
                        f"count_ok={count_ok} inside={inside_ok} "
                        f"residual={residual_ok}"
                    )
                checks[component] = {
                    "expected_roots": expected,
                    "found_roots": len(roots),
                    "frozen_1da_bracket": bracket,
                    "refined": [r.to_metadata() for r in roots],
                    "inside_frozen_bracket": inside_ok,
                    "residual_gate_passed": residual_ok,
                }
            v1["barotropic"][f"{branch.value}|{label}"] = {
                "checks": checks,
                "run": run.to_json_dict(),
            }
    report["v1_baseline_crossings"] = v1

    # ---------------------------------------------------------------- V2
    print("V2: analytic identities ...")
    v2 = {}
    for key in ("meszaros", "comoving", ("printed_4_15", "2pi"),
                ("derived_4_10", "10pi")):
        run = baseline_runs[key]
        h = run.history
        params = h.background.params
        ok_mask = ~run.rates.near_zero_mask
        fD = run.rates.f_bare[ok_mask] * h.delta_d[ok_mask]
        dd = run.rates.dDelta_d_dln_aD[ok_mask]
        scale = float(np.max(np.abs(dd)))
        id1 = float(np.max(np.abs(fD - dd)) / scale)
        fDo = run.rates.f_dressed[ok_mask] * h.delta_d[ok_mask]
        ddo = run.rates.dDelta_d_dln_aobs[ok_mask]
        id2 = float(np.max(np.abs(fDo - ddo)) / float(np.max(np.abs(ddo))))
        f_v = np.asarray(bg.fv(h.t, params))
        chain_expected = (2.0 + f_v) ** 2 / (4.0 + f_v + 4.0 * f_v**2)
        with np.errstate(invalid="ignore"):
            chain_measured = run.rates.f_dressed / run.rates.f_bare
        finite = np.isfinite(chain_measured)
        id3 = float(
            np.max(
                np.abs(chain_measured[finite] - chain_expected[finite])
                / chain_expected[finite]
            )
        )
        label = key if isinstance(key, str) else f"{key[0]}|{key[1]}"
        entry = {
            "f_bare_times_D_equals_dD_dln_aD_rel": id1,
            "f_dressed_times_D_equals_dD_dln_aobs_rel": id2,
            "chain_factor_identity_rel": id3,
        }
        if id1 > GATES["analytic_identity_rel_max"] or id2 > GATES[
            "analytic_identity_rel_max"
        ]:
            gate_failures.append(f"V2 identity: {label}")
        if id3 > GATES["chain_factor_identity_rel_max"]:
            gate_failures.append(f"V2 chain factor: {label}")
        v2[label] = entry
    # mapped-coefficient identities on a dedicated mapped run
    mapped_run = run_growth_pipeline(
        scenario=barotropic_scenario(
            GrowthD3Branch.PRINTED_4_15,
            2.0 * np.pi,
            "2pi",
            density_contrast_mapping=(
                DensityContrastMapping.MAP_TO_DELTA_M_VIA_MINUS_K_CODE2
            ),
        ),
        reference=REFERENCE_Z10,
        numerics=numerics(),
        provenance=provenance,
    )
    g_rel = float(
        np.max(
            np.abs(
                mapped_run.mapped.relative_growth
                - mapped_run.relative_growth_delta_d
            )
        )
        / float(np.max(np.abs(mapped_run.relative_growth_delta_d)))
    )
    k2 = mapped_run.mapped.harmonic.k_code ** 2
    map_factor_rel = float(
        np.max(
            np.abs(
                mapped_run.mapped.d_delta_m_dln_aD
                + mapped_run.rates.dDelta_d_dln_aD / k2
            )
        )
        / float(np.max(np.abs(mapped_run.rates.dDelta_d_dln_aD) / k2))
    )
    if g_rel > GATES["g_delta_equals_g_m_rel_max"]:
        gate_failures.append("V2 G_Delta = G_m")
    v2["mapped_printed_4_15_2pi"] = {
        "g_delta_equals_g_m_rel": g_rel,
        "mapped_derivative_minus_inverse_k2_factor_rel": map_factor_rel,
    }
    report["v2_analytic_identities"] = v2

    # ---------------------------------------------------------------- V3
    print("V3: solver convergence ...")
    v3 = {}
    for key in ("meszaros", "comoving", ("printed_4_15", "2pi"),
                ("derived_4_10", "10pi")):
        label = key if isinstance(key, str) else f"{key[0]}|{key[1]}"
        scen = (
            clean_scenario(GrowthSystem(key))
            if isinstance(key, str)
            else barotropic_scenario(
                GrowthD3Branch(key[0]),
                dict(MODES)[key[1]],
                key[1],
            )
        )
        ref_run = run_growth_pipeline(
            scenario=scen,
            reference=REFERENCE_Z10,
            numerics=numerics(solver=REFERENCE_SOLVER),
            provenance=provenance,
        )
        roots = [r.t_root for r in ref_run.crossings.delta_d_roots]
        v3[label] = {}
        for sname, solver in (
            ("tight_DOP853", TIGHT_DOP853),
            ("tight_RK45", TIGHT_RK45),
            ("tight_Radau", TIGHT_RADAU),
        ):
            other = run_growth_pipeline(
                scenario=scen,
                reference=REFERENCE_Z10,
                numerics=numerics(solver=solver),
                provenance=provenance,
            )
            entry = {
                "Delta_d": error_metrics(
                    ref_run.history.delta_d,
                    other.history.delta_d,
                    ref_run.history.t,
                    roots,
                ),
                "Z": error_metrics(
                    ref_run.history.z_expansion,
                    other.history.z_expansion,
                    ref_run.history.t,
                    roots,
                ),
                "relative_growth": error_metrics(
                    ref_run.relative_growth_delta_d,
                    other.relative_growth_delta_d,
                    ref_run.history.t,
                    roots,
                ),
                "dDelta_d_dln_aD": error_metrics(
                    ref_run.rates.dDelta_d_dln_aD,
                    other.rates.dDelta_d_dln_aD,
                    ref_run.history.t,
                    roots,
                ),
            }
            worst = max(v["normalized_linf"] for v in entry.values())
            entry["worst_normalized_linf"] = worst
            if worst > GATES["solver_convergence_normalized_linf_max"]:
                gate_failures.append(f"V3 {label} {sname}: {worst}")
            v3[label][sname] = entry
    report["v3_solver_convergence"] = v3

    # ---------------------------------------------------------------- V4
    print("V4: root convergence ...")
    v4 = {}
    root_scenarios = [
        (b, lab, k)
        for b in (GrowthD3Branch.PRINTED_4_15, GrowthD3Branch.DERIVED_4_10)
        for lab, k in MODES
        if FROZEN_1DA_BRACKETS[(b.value, lab)]["Delta_d"] is not None
    ]
    for branch, label, k in root_scenarios:
        entries = {}
        for sname, solver in (
            ("DOP853", TIGHT_DOP853),
            ("Radau", TIGHT_RADAU),
        ):
            for n in (600, 1000, 2000):
                run = run_growth_pipeline(
                    scenario=barotropic_scenario(branch, k, label),
                    reference=REFERENCE_Z10,
                    numerics=numerics(solver=solver, n_samples=n),
                    provenance=provenance,
                )
                for comp, roots in (
                    ("Delta_d", run.crossings.delta_d_roots),
                    ("Z", run.crossings.z_roots),
                ):
                    r = roots[0]
                    entries.setdefault(comp, []).append(
                        {
                            "solver": sname,
                            "n_samples": n,
                            "t_root": r.t_root,
                            "t_root_gyr": r.t_root_gyr,
                            "dressed_redshift": r.dressed_redshift,
                            "residual": r.residual,
                            "bracket": [r.bracket_left, r.bracket_right],
                            "distance_from_left_sample": r.t_root
                            - r.bracket_left,
                        }
                    )
        summary = {}
        for comp, rows in entries.items():
            times = [row["t_root"] for row in rows]
            spread = max(times) - min(times)
            not_left = all(
                abs(row["distance_from_left_sample"]) > 1e-10 for row in rows
            )
            passed = spread <= GATES["root_convergence_spread_code_time_max"]
            if not (passed and not_left):
                gate_failures.append(
                    f"V4 {branch.value} {label} {comp}: spread={spread} "
                    f"not_left={not_left}"
                )
            summary[comp] = {
                "rows": rows,
                "spread_code_time": spread,
                "spread_gyr": spread
                / run.history.time_unit_per_gyr,
                "dressed_z_spread": max(
                    row["dressed_redshift"] for row in rows
                )
                - min(row["dressed_redshift"] for row in rows),
                "never_the_left_sample": not_left,
                "gate_passed": bool(passed),
            }
        v4[f"{branch.value}|{label}"] = summary
    report["v4_root_convergence"] = v4

    # ---------------------------------------------------------------- V5
    print("V5: tilt-form equivalence ...")
    tilt_runs = {}
    for tilt in (GrowthTiltForm.UNRESCALED_V, GrowthTiltForm.RESCALED_VTILDE):
        tilt_runs[tilt.value] = run_growth_pipeline(
            scenario=barotropic_scenario(
                GrowthD3Branch.PRINTED_4_15, 5.0 * np.pi, "5pi", tilt_form=tilt
            ),
            reference=REFERENCE_Z10,
            numerics=numerics(),
            provenance=provenance,
        )
    a = tilt_runs["unrescaled_V"]
    b = tilt_runs["rescaled_Vtilde"]
    scale = float(np.max(np.abs(a.history.delta_d)))
    hist_linf = float(
        np.max(np.abs(a.history.delta_d - b.history.delta_d)) / scale
    )
    root_diffs = [
        abs(ra.t_root - rb.t_root)
        for ra, rb in zip(
            a.crossings.delta_d_roots + a.crossings.z_roots,
            b.crossings.delta_d_roots + b.crossings.z_roots,
        )
    ]
    ok_mask = ~(a.rates.near_zero_mask | b.rates.near_zero_mask)
    rate_rel = float(
        np.nanmax(
            np.abs(a.rates.f_bare[ok_mask] - b.rates.f_bare[ok_mask])
            / np.abs(a.rates.f_bare[ok_mask])
        )
    )
    if hist_linf > GATES["tilt_history_normalized_linf_max"]:
        gate_failures.append(f"V5 history: {hist_linf}")
    if root_diffs and max(root_diffs) > GATES["tilt_root_time_abs_max"]:
        gate_failures.append(f"V5 roots: {max(root_diffs)}")
    report["v5_tilt_equivalence"] = {
        "scenario": "printed_4_15|5pi (both tilt labels retained)",
        "history_normalized_linf": hist_linf,
        "root_time_abs_diffs": root_diffs,
        "f_bare_rel_diff_max": rate_rel,
        "labels": ["unrescaled_V", "rescaled_Vtilde"],
    }

    # ---------------------------------------------------------------- V6
    print("V6: scale independence / dependence ...")
    meta_runs = [
        run_growth_pipeline(
            scenario=clean_scenario(
                GrowthSystem.COMOVING,
                density_contrast_mapping=(
                    DensityContrastMapping.MAP_TO_DELTA_M_VIA_MINUS_K_CODE2
                ),
                supplied_mode_k=kk,
                mode_label=lbl,
            ),
            reference=REFERENCE_Z10,
            numerics=numerics(),
            provenance=provenance,
        )
        for kk, lbl in ((7.0, "meta7"), (13.0, "meta13"))
    ]
    identical = bool(
        np.array_equal(
            meta_runs[0].relative_growth_delta_d,
            meta_runs[1].relative_growth_delta_d,
        )
    )
    if not identical:
        gate_failures.append("V6 clean scale independence")
    end2 = baseline_runs[("printed_4_15", "2pi")].relative_growth_delta_d[-1]
    end5 = baseline_runs[("printed_4_15", "5pi")].relative_growth_delta_d[-1]
    end10 = baseline_runs[("printed_4_15", "10pi")].relative_growth_delta_d[-1]
    report["v6_scale_dependence"] = {
        "clean_relative_growth_identical_across_harmonic_metadata": identical,
        "barotropic_relative_growth_endpoints_printed_4_15": {
            "2pi": float(end2),
            "5pi": float(end5),
            "10pi": float(end10),
        },
        "note": (
            "deterministic per-mode dependence of the audited three-mode "
            "normalisation; no physical power-spectrum scale dependence is "
            "inferred"
        ),
    }

    # ---------------------------------------------------------------- V7
    print("V7: one-factor scenario studies ...")
    validation_baseline = barotropic_scenario(
        GrowthD3Branch.PRINTED_4_15, 2.0 * np.pi, "2pi"
    )
    base_run = baseline_runs[("printed_4_15", "2pi")]
    factors = {
        "background_preset": dict(
            background_preset=GrowthBackgroundPreset.PAPER_REFERENCE
        ),
        "rate_unit_convention": dict(
            rate_unit_convention=(
                RateUnitConvention.LCDM_TO_TIMESCAPE_CONVERTED
            )
        ),
        "epoch_choice": dict(epoch_choice=EpochChoice.DRESSED_Z20),
        "growth_coordinate": dict(
            growth_coordinate=GrowthCoordinate.DRESSED_REDSHIFT
        ),
        "d3_branch": dict(d3_branch=GrowthD3Branch.DERIVED_4_10),
        "tilt_form": dict(tilt_form=GrowthTiltForm.RESCALED_VTILDE),
        "wavenumber_convention": dict(
            wavenumber_convention=(
                GrowthWavenumberConvention.PAPER_LCDM_HUBBLE_K
            )
        ),
        "density_contrast_mapping": dict(
            density_contrast_mapping=(
                DensityContrastMapping.MAP_TO_DELTA_M_VIA_MINUS_K_CODE2
            )
        ),
    }
    v7 = {
        "validation_baseline": {
            "label": "validation_baseline",
            "note": (
                "named validation baseline for one-factor studies only; "
                "not a public API default and not a scientific preference"
            ),
            "scenario": validation_baseline.to_metadata(),
            "endpoint_relative_growth": float(
                base_run.relative_growth_delta_d[-1]
            ),
            "endpoint_f_bare": (
                None
                if np.isnan(base_run.rates.f_bare[-1])
                else float(base_run.rates.f_bare[-1])
            ),
        },
        "factors": {},
        "envelope_note": (
            "any envelope across these deltas is a convention spread, not a "
            "confidence interval or statistical uncertainty"
        ),
    }
    for fname, override in factors.items():
        scen = barotropic_scenario(
            GrowthD3Branch.PRINTED_4_15, 2.0 * np.pi, "2pi", **override
        )
        run = run_growth_pipeline(
            scenario=scen,
            reference=REFERENCE_Z10,
            numerics=numerics(),
            provenance=provenance,
        )
        base_end = float(base_run.relative_growth_delta_d[-1])
        end = float(run.relative_growth_delta_d[-1])
        f_base = base_run.rates.f_bare[-1]
        f_end_attr = (
            run.rates.f_dressed
            if fname == "growth_coordinate"
            else run.rates.f_bare
        )
        f_other = f_end_attr[-1]
        v7["factors"][fname] = {
            "changed_to": {
                key: getattr(scen, key).value for key in override
            },
            "endpoint_relative_growth": end,
            "endpoint_relative_growth_delta_vs_baseline": (
                (end - base_end) / abs(base_end)
            ),
            "endpoint_rate": None if np.isnan(f_other) else float(f_other),
            "endpoint_rate_baseline_f_bare": (
                None if np.isnan(f_base) else float(f_base)
            ),
            "delta_d_root_count": len(run.crossings.delta_d_roots),
            "note": "single factor changed; every other field held fixed",
        }
    v7["signed_delta_notes"] = {
        "d3_branch": (
            "the d3_branch -> derived_4_10 endpoint relative-growth delta "
            "(approx -230.2%) is a SIGNED endpoint-growth difference that "
            "spans a trajectory sign reversal (baseline G_end > 0; "
            "derived_4_10 G_end < 0 with one Delta_d root); it is a signed "
            "difference of endpoint growth, not an uncertainty magnitude or "
            "error bar"
        ),
        "wavenumber_convention": (
            "the wavenumber_convention -> paper_lcdm_hubble_k change flips "
            "the sign of the endpoint growth rate (positive under "
            "upstream_timescape_k, negative under paper_lcdm_hubble_k); this "
            "is a rate sign flip, not an uncertainty magnitude or error bar"
        ),
    }
    report["v7_one_factor_studies"] = v7

    # ---------------------------------------- independent root corroboration
    # Recorded separately from the V4 study (not a V4 quantity and not part
    # of the V4 numerical data): the Phase 1D-B compliance audit reproduced
    # every production root by an independent path.
    report["independent_root_corroboration"] = {
        "source": (
            "Phase 1D-B compliance audit "
            "(reports/phase1d_b_compliance_audit.md); corroborating evidence "
            "separate from V4, not a V4 quantity and not part of the V4 study"
        ),
        "method": (
            "scipy.integrate.solve_ivp event detection under Radau and under "
            "LSODA; each integrator used its own local continuous "
            "interpolation for the event root (not the growth-layer dense "
            "DOP853 solution and not brentq-on-dense)"
        ),
        "all_ten_production_roots_reproduced": True,
        "worst_abs_root_time_difference_solver_units": 9.6e-12,
        "printed_4_15_2pi_zero_events_both_components": True,
    }

    # -------------------------------------------------------------- taxonomy
    report["uncertainty_taxonomy"] = {
        "numerical_sampling_root_uncertainty": (
            "V4 demonstrates sampling-grid convergence (refined root stable "
            "as the sampled grid is refined 600->1000->2000), sampled-bracket "
            "robustness, and reproducibility of the Brent refinement on one "
            "fixed dense DOP853 continuous representation; per-root "
            "uncertainty diagnostic xtol + rtol*|root| per refined root"
        ),
        "solver_method_tolerance_uncertainty": (
            "V3 normalized-Linf deltas of tight explicit/implicit methods "
            "against the independent DOP853 rtol=2e-13/atol=2e-15 reference. "
            "V4 alone does NOT measure cross-method root agreement: for each "
            "root the DOP853 and Radau sampled rows refine against the same "
            "dense DOP853 representation, so their root values coincide by "
            "construction rather than as an independent cross-method check. "
            "Independent cross-method root corroboration is recorded "
            "separately in independent_root_corroboration"
        ),
        "unresolved_convention_spread": (
            "V7 one-factor deltas for preset, rate units, epoch, growth "
            "coordinate, D3 branch, tilt representation, wavenumber "
            "convention, and density mapping; a spread across these is a "
            "convention spread, never a confidence interval"
        ),
        "model_closure_dependence": (
            "differences between meszaros, comoving, and barotropic runs "
            "(V1/V6); the Meszaros system remains a mathematical comparison "
            "system, not physically validated for Timescape"
        ),
        "spectrum_normalization_uncertainty": (
            "intentionally absent: spectra and normalisation are not "
            "implemented in Phase 1D-B"
        ),
    }

    report["gate_failures"] = gate_failures
    report["all_gates_passed"] = not gate_failures

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(
        f"written {OUTPUT.relative_to(PROJECT_ROOT)}; "
        f"gates {'PASSED' if not gate_failures else 'FAILED'}"
    )
    for failure in gate_failures:
        print("GATE FAILURE:", failure)
    return 0 if not gate_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
