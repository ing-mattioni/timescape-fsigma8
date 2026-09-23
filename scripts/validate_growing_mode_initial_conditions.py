"""Validation of the regular growing-mode IC convention (review finding F1).

Writes ``artifacts/independent/phase1f_c_r_f1_growing_mode_ic_validation.json``
using only the independent package.  The upstream notebook is not used.

Studies:
  G1 growing-mode coefficients (u, -Z/Delta_d, q) per preset, epoch, system;
  G2 numerical convergence: start fraction and integration method;
  G3 independent route: frozen linear RHS integrated from the deep EdS era;
  G4 forward trajectories: growing-mode ICs carry no decaying admixture,
     legacy ICs do;
  G5 the review's F1 convention study restated relative to the growing mode;
  G6 growth pipeline and Candidate A with the growing mode, including the
     collapse of the epoch/rate convention spread.

Every tolerance is explicit and declared before evaluation; the script exits
nonzero if any gate fails.  Synthetic Candidate A anchors are validation-only.
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from dataclasses import replace
from functools import partial
from importlib.metadata import version
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import timescape_fsigma8.background as bg
from timescape_fsigma8.growth import (
    AnchoredDiagnosticAssumptions,
    AnchorProvenanceKind,
    DenseSolveConfig,
    DensityContrastMapping,
    ExternalDensityAmplitudeAnchor,
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
    anchored_density_growth_diagnostic,
    resolve_background,
    run_growth_pipeline,
)
from timescape_fsigma8.perturbations import (
    PHASE1C_EPOCH_ROOT,
    PLANCK_2018_QPLUS_RECIPE,
    REGULAR_GROWING_MODE_REFERENCE_CONFIG,
    TIGHT_DOP853,
    CleanPerturbationSystem,
    EpochChoice,
    EpochScenario,
    GrowingModeConfig,
    InitialConditionScenario,
    RateUnitConvention,
    comoving_rhs,
    meszaros_rhs,
    regular_growing_mode_coefficients,
    resolve_growing_mode_initial_conditions,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "artifacts" / "independent" / "phase1f_c_r_f1_growing_mode_ic_validation.json"

CONFIG = REGULAR_GROWING_MODE_REFERENCE_CONFIG
G = 1.0
LINEAR = dict(method="DOP853", rtol=2e-13, atol=1e-30)  # frozen-RHS reference solves
GROWING = RateUnitConvention.TIMESCAPE_REGULAR_GROWING_MODE
LEGACY_RATES = (
    RateUnitConvention.UPSTREAM_UNCONVERTED,
    RateUnitConvention.LCDM_TO_TIMESCAPE_CONVERTED,
)
EPOCHS = (EpochChoice.UPSTREAM_0P218_GYR, EpochChoice.DRESSED_Z20)
SYSTEMS = {
    CleanPerturbationSystem.MESZAROS: GrowthSystem.MESZAROS,
    CleanPerturbationSystem.COMOVING: GrowthSystem.COMOVING,
}

# Gates, declared before any evaluation (absolute, on O(1) log-rates u, q).
GATES = {
    "G2_start_fraction_spread": 1e-11,
    "G2_method_spread": 5e-9,
    "G3_far_past_linear_agreement": 1e-9,
    "G4_growing_trajectory_log_rate": 1e-9,
    "G4_legacy_initial_log_rate_deviation_min": 0.2,
    "G6_pipeline_f_bare_vs_regular_solution": 1e-9,
    "G6_epoch_spread_of_candidate_a_growth_rel": 1e-9,
}

NUMERICS = GrowthNumericsConfig(
    solver=TIGHT_DOP853,
    n_samples=1000,
    G=G,
    dense=DenseSolveConfig(method="DOP853", rtol=1e-11, atol=1e-13, max_step=np.inf, first_step=None),
    root=RootRefineConfig(xtol=1e-13, rtol=8.9e-16, maxiter=100, residual_scale_gate=1e-6),
    near_zero_rel_floor=1e-9,
)
REFERENCE_Z10 = GrowthReference(
    coordinate=GrowthReferenceCoordinate.DRESSED_REDSHIFT,
    value=10.0,
    root=PHASE1C_EPOCH_ROOT,
    amplitude_floor_rel=1e-10,
)


def git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def resolved_epoch(params, preset_background, choice):
    return EpochScenario(
        choice=choice, time_unit=preset_background.time_unit, root=PHASE1C_EPOCH_ROOT
    ).resolve(params)


def rhs_for(system, params):
    if system is CleanPerturbationSystem.COMOVING:
        return partial(comoving_rhs, params=params, G=G)
    return partial(meszaros_rhs, params=params, G=G)


def state_vector(system, ics):
    return ics.comoving_vector() if system is CleanPerturbationSystem.COMOVING else ics.meszaros_vector()


def log_rate(system, y, t):
    """u = t dln(Delta_d)/dt from a frozen-solver state (Z = -dDelta_d/dt)."""
    rate = -y[1] / y[0] if system is CleanPerturbationSystem.COMOVING else y[1] / y[0]
    return t * rate


def legacy_ics(rate, timescape_h, params):
    return InitialConditionScenario(
        recipe=PLANCK_2018_QPLUS_RECIPE, rate_units=rate, timescape_h=timescape_h
    ).resolve(params)


def time_at_redshift(params, z_target, lower):
    return brentq(lambda t: float(bg.redshift(t, params)) - z_target, lower, params.t0,
                  xtol=1e-16, rtol=8.9e-16, maxiter=200)


def study_coefficients():
    rows = []
    for preset in GrowthBackgroundPreset:
        background = resolve_background(preset)
        params = background.params
        for choice in EPOCHS:
            ep = resolved_epoch(params, background, choice)
            for system in CleanPerturbationSystem:
                ics = resolve_growing_mode_initial_conditions(
                    params, recipe=PLANCK_2018_QPLUS_RECIPE, system=system,
                    epoch=ep, config=CONFIG, G=G,
                )
                coefficients = regular_growing_mode_coefficients(
                    params, system=system, times=[ep.time], config=CONFIG, G=G
                )
                rows.append({
                    "preset": preset.value, "epoch": choice.value, "system": system.value,
                    "t_i_solver_units": ep.time, "t_i_gyr": ep.time_gyr,
                    "dressed_redshift": ep.dressed_redshift,
                    "log_rate_u": ics.log_rate, "minus_Z_over_Delta_d": -ics.expansion_gradient / ics.delta_d,
                    "effective_ratio_q": ics.effective_ratio,
                    "delta_d": ics.delta_d, "Z": ics.expansion_gradient, "delta_eff": ics.delta_eff,
                    "eds_limit_deviation_at_start": coefficients.eds_limit_deviation,
                    "nfev": coefficients.nfev,
                })
    return rows


def study_convergence(params, times):
    reference = {s: regular_growing_mode_coefficients(params, system=s, times=times, config=CONFIG, G=G)
                 for s in CleanPerturbationSystem}
    out = {"start_fraction": [], "method": []}
    for fraction in (1e-4, 1e-6, 1e-8, 1e-10):
        cfg = GrowingModeConfig(start_fraction=fraction, eds_limit_tolerance=1e-5,
                                method="DOP853", rtol=1e-12, atol=1e-14)
        for system in CleanPerturbationSystem:
            c = regular_growing_mode_coefficients(params, system=system, times=times, config=cfg, G=G)
            spread = float(np.max(np.abs(c.log_rate - reference[system].log_rate)))
            if system is CleanPerturbationSystem.COMOVING:
                spread = max(spread, float(np.max(np.abs(c.effective_ratio - reference[system].effective_ratio))))
            out["start_fraction"].append({"start_fraction": fraction, "system": system.value, "max_abs_diff": spread})
    for method, rtol, atol in (("RK45", 1e-11, 1e-13), ("Radau", 1e-11, 1e-13), ("DOP853", 1e-13, 1e-15)):
        cfg = GrowingModeConfig(start_fraction=1e-6, eds_limit_tolerance=1e-5, method=method, rtol=rtol, atol=atol)
        for system in CleanPerturbationSystem:
            c = regular_growing_mode_coefficients(params, system=system, times=times, config=cfg, G=G)
            spread = float(np.max(np.abs(c.log_rate - reference[system].log_rate)))
            if system is CleanPerturbationSystem.COMOVING:
                spread = max(spread, float(np.max(np.abs(c.effective_ratio - reference[system].effective_ratio))))
            out["method"].append({"method": method, "rtol": rtol, "atol": atol, "system": system.value, "max_abs_diff": spread})
    return out


def study_far_past(params, times):
    t_far = 1e-4 * times[0]
    rows = []
    for system in CleanPerturbationSystem:
        if system is CleanPerturbationSystem.COMOVING:
            y0 = [t_far ** (2 / 3), -(2 / 3) * t_far ** (-1 / 3), 0.2 * t_far ** (2 / 3)]
        else:
            y0 = [t_far ** (2 / 3), (2 / 3) * t_far ** (-1 / 3)]
        linear = solve_ivp(rhs_for(system, params), (t_far, times[-1]), y0, t_eval=times, **LINEAR)
        c = regular_growing_mode_coefficients(params, system=system, times=times, config=CONFIG, G=G)
        du = float(np.max(np.abs(c.log_rate - log_rate(system, linear.y, times))))
        dq = (float(np.max(np.abs(c.effective_ratio - linear.y[2] / linear.y[0])))
              if system is CleanPerturbationSystem.COMOVING else None)
        rows.append({"system": system.value, "t_far_over_t_first": 1e-4,
                     "max_abs_log_rate_diff": du, "max_abs_effective_ratio_diff": dq})
    return rows


def study_trajectories(params, background):
    rows = []
    ep = resolved_epoch(params, background, EpochChoice.UPSTREAM_0P218_GYR)
    times = np.linspace(ep.time, params.t0, 400)
    for system in CleanPerturbationSystem:
        expected = regular_growing_mode_coefficients(params, system=system, times=times, config=CONFIG, G=G).log_rate
        grown_ics = resolve_growing_mode_initial_conditions(
            params, recipe=PLANCK_2018_QPLUS_RECIPE, system=system, epoch=ep, config=CONFIG, G=G)
        grown = solve_ivp(rhs_for(system, params), (ep.time, params.t0), state_vector(system, grown_ics), t_eval=times, **LINEAR)
        legacy = legacy_ics(RateUnitConvention.UPSTREAM_UNCONVERTED, background.timescape_h, params)
        contaminated = solve_ivp(rhs_for(system, params), (ep.time, params.t0), state_vector(system, legacy), t_eval=times, **LINEAR)
        rows.append({
            "system": system.value,
            "growing_max_abs_log_rate_deviation": float(np.max(np.abs(log_rate(system, grown.y, times) - expected))),
            "legacy_initial_log_rate_deviation": float(abs(log_rate(system, contaminated.y, times)[0] - expected[0])),
            "legacy_final_log_rate_deviation": float(abs(log_rate(system, contaminated.y, times)[-1] - expected[-1])),
        })
    return rows


def study_restated_conventions(params, background):
    """F1 table: each legacy convention against the growing mode at the same epoch."""
    rows, decomposition = [], None
    for choice in EPOCHS:
        ep = resolved_epoch(params, background, choice)
        t_ref = time_at_redshift(params, 10.0, ep.time)
        z_times = {z: (params.t0 if z == 0 else time_at_redshift(params, z, ep.time)) for z in (0, 1, 2, 5)}
        for system in CleanPerturbationSystem:
            g_ics = resolve_growing_mode_initial_conditions(
                params, recipe=PLANCK_2018_QPLUS_RECIPE, system=system, epoch=ep, config=CONFIG, G=G)
            grown = solve_ivp(rhs_for(system, params), (ep.time, params.t0), state_vector(system, g_ics),
                              dense_output=True, **LINEAR)
            for rate in LEGACY_RATES:
                l_ics = legacy_ics(rate, background.timescape_h, params)
                legacy = solve_ivp(rhs_for(system, params), (ep.time, params.t0), state_vector(system, l_ics),
                                   dense_output=True, **LINEAR)
                y_g, y_l = grown.sol(params.t0), legacy.sol(params.t0)
                G_g = y_g[0] / grown.sol(t_ref)[0]
                G_l = y_l[0] / legacy.sol(t_ref)[0]
                f_bias = {}
                for z, t in z_times.items():
                    f_bias[f"z{z}"] = float(
                        log_rate(system, legacy.sol(t), t) / log_rate(system, grown.sol(t), t) - 1.0)
                row = {
                    "preset": background.preset.value, "epoch": choice.value, "system": system.value,
                    "legacy_rate_convention": rate.value,
                    "delta_d_t0_ratio_legacy_over_growing": float(y_l[0] / y_g[0]),
                    "relative_growth_t0_zref10_legacy": float(G_l),
                    "relative_growth_t0_zref10_growing": float(G_g),
                    "relative_growth_bias": float(G_l / G_g - 1.0),
                    "f_bare_bias": f_bias,
                }
                if system is CleanPerturbationSystem.COMOVING:
                    row["delta_eff_t0_ratio_legacy_over_growing"] = float(y_l[2] / y_g[2])
                rows.append(row)
            if (system is CleanPerturbationSystem.COMOVING and choice is EpochChoice.UPSTREAM_0P218_GYR):
                legacy = legacy_ics(RateUnitConvention.UPSTREAM_UNCONVERTED, background.timescape_h, params)
                reference_end = grown.sol(params.t0)[0]
                variants = {
                    "growing_mode_Z_with_paper_zero_delta_eff": [g_ics.delta_d, g_ics.expansion_gradient, 0.0],
                    "legacy_Z_with_regular_delta_eff": [legacy.delta_d, legacy.expansion_gradient, g_ics.delta_eff],
                    "legacy_Z_with_paper_zero_delta_eff": list(legacy.comoving_vector()),
                }
                decomposition = {}
                for name, y0 in variants.items():
                    end = solve_ivp(rhs_for(system, params), (ep.time, params.t0), y0, **LINEAR).y[0, -1]
                    decomposition[name] = float(end / reference_end)
    return rows, decomposition


def synthetic_anchor(result):
    return ExternalDensityAmplitudeAnchor(
        sigma8_anchor_at_reference=0.8,
        provenance_label="synthetic growing-mode validation amplitude",
        provenance_kind=AnchorProvenanceKind.SYNTHETIC_VALIDATION_ONLY,
        resolved_reference=result.reference,
        smoothing_radius_definition="synthetic fixed radius label only",
        h_convention="synthetic fixed h-convention label",
        spatial_frame="synthetic matched spatial-frame label",
        reciprocal_units_statement="synthetic reciprocal units in one frame",
    )


ASSUMPTIONS = AnchoredDiagnosticAssumptions(
    a1_linear_evolution_acknowledged=True,
    a2_scale_independent_growth_acknowledged=True,
    a3_fixed_reference_spectrum_shape_acknowledged=True,
    a4_fixed_smoothing_convention_acknowledged=True,
    a5_positive_differentiable_growth_acknowledged=True,
    a6_anchor_at_resolved_reference_acknowledged=True,
)


def study_pipeline(head):
    provenance = GrowthProvenance(
        repository_commit=head,
        upstream_commit="590c6fd5332acb15f5683ebf392a0d7ce54983c5",
        upstream_notebook_sha256="not used by this study",
    )
    rows = []
    max_f_error = 0.0
    for preset in GrowthBackgroundPreset:
        for growth_system in (GrowthSystem.COMOVING, GrowthSystem.MESZAROS):
            clean = (CleanPerturbationSystem.COMOVING if growth_system is GrowthSystem.COMOVING
                     else CleanPerturbationSystem.MESZAROS)
            for rate in (GROWING,) + LEGACY_RATES:
                for choice in EPOCHS:
                    scenario = GrowthScenario(
                        perturbation_system=growth_system, background_preset=preset,
                        d3_branch=GrowthD3Branch.NOT_APPLICABLE, tilt_form=GrowthTiltForm.NOT_APPLICABLE,
                        rate_unit_convention=rate, epoch_choice=choice,
                        wavenumber_convention=GrowthWavenumberConvention.NOT_APPLICABLE,
                        growth_coordinate=GrowthCoordinate.BARE_AD,
                        density_contrast_mapping=DensityContrastMapping.KEEP_DELTA_D,
                        supplied_mode_k=None, mode_label=None,
                    )
                    result = run_growth_pipeline(scenario=scenario, reference=REFERENCE_Z10,
                                                 numerics=NUMERICS, provenance=provenance)
                    diagnostic = anchored_density_growth_diagnostic(
                        growth_result=result, anchor=synthetic_anchor(result), assumptions=ASSUMPTIONS)
                    history = result.history
                    if rate is GROWING:
                        u = regular_growing_mode_coefficients(
                            history.background.params, system=clean, times=history.t, config=CONFIG, G=G).log_rate
                        expected = 3.0 * u / (history.t * bg.Theta(history.t, history.background.params))
                        max_f_error = max(max_f_error, float(np.max(np.abs(result.rates.f_bare - expected))))
                    rows.append({
                        "preset": preset.value, "system": growth_system.value,
                        "rate_convention": rate.value, "epoch": choice.value,
                        "relative_growth_t0": float(diagnostic.relative_growth[-1]),
                        "f_bare_t0": float(result.rates.f_bare[-1]),
                        "f_dressed_t0": float(result.rates.f_dressed[-1]),
                        "anchored_amplitude_t0": float(diagnostic.anchored_density_amplitude[-1]),
                        "anchored_growth_bare_t0": float(diagnostic.anchored_density_growth[-1]),
                        "delta_d_t0": float(history.delta_d[-1]),
                    })
    spread = {}
    for preset in GrowthBackgroundPreset:
        for growth_system in (GrowthSystem.COMOVING, GrowthSystem.MESZAROS):
            for rate in (GROWING,) + LEGACY_RATES:
                values = [r["relative_growth_t0"] for r in rows if r["preset"] == preset.value
                          and r["system"] == growth_system.value and r["rate_convention"] == rate.value]
                spread[f"{preset.value}|{growth_system.value}|{rate.value}"] = float(
                    (max(values) - min(values)) / abs(np.mean(values)))
    return rows, max_f_error, spread


def main() -> int:
    head = git_head()
    notebook_background = resolve_background(GrowthBackgroundPreset.NOTEBOOK_REFERENCE)
    params = notebook_background.params
    z20 = resolved_epoch(params, notebook_background, EpochChoice.DRESSED_Z20).time
    grid = np.linspace(z20, params.t0, 300)

    coefficients = study_coefficients()
    convergence = study_convergence(params, grid)
    far_past = study_far_past(params, grid)
    trajectories = study_trajectories(params, notebook_background)
    restated, decomposition = study_restated_conventions(params, notebook_background)
    pipeline_rows, pipeline_f_error, epoch_spread = study_pipeline(head)

    results = {
        "G2_start_fraction_spread": max(r["max_abs_diff"] for r in convergence["start_fraction"]),
        "G2_method_spread": max(r["max_abs_diff"] for r in convergence["method"]),
        "G3_far_past_linear_agreement": max(
            max(r["max_abs_log_rate_diff"], r["max_abs_effective_ratio_diff"] or 0.0) for r in far_past),
        "G4_growing_trajectory_log_rate": max(r["growing_max_abs_log_rate_deviation"] for r in trajectories),
        "G4_legacy_initial_log_rate_deviation_min": min(r["legacy_initial_log_rate_deviation"] for r in trajectories),
        "G6_pipeline_f_bare_vs_regular_solution": pipeline_f_error,
        "G6_epoch_spread_of_candidate_a_growth_rel": max(
            v for k, v in epoch_spread.items() if k.endswith(GROWING.value)),
    }
    gate_status = {}
    for name, gate in GATES.items():
        value = results[name]
        passed = value >= gate if name.endswith("_min") else value <= gate
        gate_status[name] = {"gate": gate, "measured": value, "passed": bool(passed)}

    artifact = {
        "schema_version": 1,
        "title": "Regular growing-mode initial conditions (review finding F1) validation",
        "provenance": {
            "repository_head": head,
            "python": platform.python_version(),
            "numpy": version("numpy"), "scipy": version("scipy"),
            "platform": platform.platform(),
        },
        "reference_config": CONFIG.to_metadata(),
        "linear_reference_solver": LINEAR,
        "growth_numerics": NUMERICS.to_metadata(),
        "G1_coefficients": coefficients,
        "G2_convergence": convergence,
        "G3_far_past_linear_route": far_past,
        "G4_trajectories": trajectories,
        "G5_restated_convention_study": restated,
        "G5_delta_eff_decomposition_comoving_notebook_0p218": decomposition,
        "G6_pipeline_and_candidate_a": pipeline_rows,
        "G6_epoch_spread_rel_by_preset_system_rate": epoch_spread,
        "gates": gate_status,
        "all_gates_passed": all(v["passed"] for v in gate_status.values()),
        "scope": {
            "systems": ["meszaros", "comoving"],
            "barotropic": "REJECTED_FAIL_CLOSED (k- and D3-dependent early solution)",
            "candidate_a_anchor": "SYNTHETIC_VALIDATION_ONLY",
            "observational_interpretation": "NOT_GRANTED",
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(artifact, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(f"written {OUTPUT.relative_to(ROOT)}")
    for name, status in gate_status.items():
        print(f"{name}: measured {status['measured']:.3e} gate {status['gate']:.1e} "
              f"{'PASS' if status['passed'] else 'FAIL'}")
    return 0 if artifact["all_gates_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
