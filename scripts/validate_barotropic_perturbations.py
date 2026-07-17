"""Run Phase 1C-B2 barotropic reproduction and controlled factor analyses.

The public scientific package supplies corrected-sound-speed trajectories.
The script-local ``_phase1c_b2_forensic`` module is used only for the upstream
D2 reproduction and the explicit D2 factors.  Outputs are git-ignored JSON
files under ``artifacts/independent``.
"""

from __future__ import annotations

import json
import hashlib
import platform
import sys
from dataclasses import asdict, replace
from importlib.metadata import version
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import _phase1c_b2_forensic as forensic  # noqa: E402
import timescape_fsigma8.background as bg  # noqa: E402
from timescape_fsigma8.background import TrackerParams  # noqa: E402
from timescape_fsigma8.perturbations import (  # noqa: E402
    PHASE1C_EPOCH_ROOT,
    PLANCK_2018_QPLUS_RECIPE,
    TIGHT_DOP853,
    TIGHT_RADAU,
    TIGHT_RK45,
    UPSTREAM_NOTEBOOK_TIME_UNIT,
    UPSTREAM_RK45_DEFAULTS,
    BarotropicScenario,
    D3Branch,
    EpochChoice,
    EpochScenario,
    RateUnitConvention,
    SolverConfig,
    TiltForm,
    WavenumberConvention,
    solve_barotropic,
    transform_barotropic_state,
)


ORACLE_PATH = PROJECT_ROOT / "artifacts" / "upstream" / "oracle_barotropic_perturbations.json"
OUT_DIR = PROJECT_ROOT / "artifacts" / "independent"
ORACLE_COMPARISON_PATH = OUT_DIR / "phase1c_b2_oracle_comparison.json"
CONVERGENCE_PATH = OUT_DIR / "phase1c_b2_convergence.json"
FACTORIAL_PATH = OUT_DIR / "phase1c_b2_d2_d3_factorial.json"
SCENARIO_PATH = OUT_DIR / "phase1c_b2_scenario_effects.json"
ENDPOINT_PATH = OUT_DIR / "phase1c_b2_figure_endpoints.json"

K_VALUES = (2.0 * np.pi, 5.0 * np.pi, 10.0 * np.pi)
COMPONENTS = ("Delta_d", "Z", "Delta_eff", "tilt")
REFERENCE_DOP853 = SolverConfig(
    method="DOP853", rtol=2e-13, atol=2e-15, max_step=np.inf, first_step=None
)
MEDIUM_DOP853 = SolverConfig(
    method="DOP853", rtol=1e-8, atol=1e-10, max_step=np.inf, first_step=None
)
MEDIUM_RK45 = SolverConfig(
    method="RK45", rtol=1e-6, atol=1e-8, max_step=np.inf, first_step=None
)

ORACLE_GATE = 2e-8
# Numerical validation gates, not physics uncertainties.  The all-mode study
# measured 3.14e-9 (tight explicit) and 2.71e-11 (Radau); 2e-8 preserves a
# factor-six margin while remaining below the medium-RK errors and the
# high-k medium-DOP853 errors that expose tolerance sensitivity.
TIGHT_EXPLICIT_GATE = 2e-8
IMPLICIT_CROSSCHECK_GATE = 2e-8

RUN_RECORD_SCHEMA_VERSION = "phase1c_b2_run_record_v1"
SOUND_SPEED_PROVENANCE = frozenset(
    {"corrected_phase1b", "upstream_d2_corrupted"}
)


def config_record(config: SolverConfig) -> dict:
    """Serialize every solve_ivp setting used by a B2 numerical run."""
    record = asdict(config)
    if np.isinf(record["max_step"]):
        record["max_step"] = "inf"
    record.update(
        dense_output=False,
        events=None,
        vectorized=False,
    )
    return record


def run_record(
    scenario: BarotropicScenario,
    config: SolverConfig,
    sound_speed_provenance: str,
) -> dict:
    """Return the self-contained schema-v1 record for one B2 run.

    The identifier is SHA-256 of canonical JSON containing every scientific
    choice, both Hubble normalisations, sound-speed provenance, and every
    explicit solve_ivp option.  It ranks neither D3 branch.  Consequently any
    change to a solver or scientific field changes the identifier.
    """
    if sound_speed_provenance not in SOUND_SPEED_PROVENANCE:
        raise ValueError(
            "sound_speed_provenance must be corrected_phase1b or "
            "upstream_d2_corrupted"
        )
    payload = {
        "schema_version": RUN_RECORD_SCHEMA_VERSION,
        "branch": scenario.branch.value,
        "tilt_form": scenario.tilt_form.value,
        "rate_unit_convention": scenario.rate_convention.value,
        "epoch_choice": scenario.epoch_choice.value,
        "wavenumber_convention": scenario.wavenumber_convention.value,
        "numerical_k": scenario.k,
        "timescape_h": scenario.timescape_h,
        "lcdm_h": scenario.lcdm_h,
        "sound_speed_provenance": sound_speed_provenance,
        "solver": config_record(config),
    }
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return {
        **payload,
        "run_identifier": (
            "phase1c_b2_run_v1:" + hashlib.sha256(canonical).hexdigest()
        ),
    }


def run_record_schema() -> dict:
    """Document the exact machine-readable B2 run-record contract."""
    return {
        "schema_version": RUN_RECORD_SCHEMA_VERSION,
        "required_scientific_fields": [
            "branch",
            "tilt_form",
            "rate_unit_convention",
            "epoch_choice",
            "wavenumber_convention",
            "numerical_k",
            "timescape_h",
            "lcdm_h",
            "sound_speed_provenance",
        ],
        "sound_speed_provenance_values": sorted(SOUND_SPEED_PROVENANCE),
        "required_solver_fields": [
            "method",
            "rtol",
            "atol",
            "max_step",
            "first_step",
            "dense_output",
            "events",
            "vectorized",
        ],
        "identifier_field": "run_identifier",
        "identifier_algorithm": (
            "phase1c_b2_run_v1: + SHA-256 of UTF-8 canonical JSON "
            "(sort_keys=true, separators=(',', ':'), allow_nan=false) over "
            "all fields except run_identifier"
        ),
    }


def validate_run_record(record: dict) -> None:
    """Raise ValueError unless a record exactly satisfies schema v1."""
    schema = run_record_schema()
    required = {
        "schema_version",
        *schema["required_scientific_fields"],
        "solver",
        "run_identifier",
    }
    if set(record) != required:
        raise ValueError(
            f"run-record fields differ: missing={required - set(record)}, "
            f"extra={set(record) - required}"
        )
    if record["schema_version"] != RUN_RECORD_SCHEMA_VERSION:
        raise ValueError("unexpected B2 run-record schema version")
    if record["sound_speed_provenance"] not in SOUND_SPEED_PROVENANCE:
        raise ValueError("invalid sound-speed provenance")
    if set(record["solver"]) != set(schema["required_solver_fields"]):
        raise ValueError("run-record solver fields differ from schema v1")
    payload = {key: value for key, value in record.items() if key != "run_identifier"}
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    expected = "phase1c_b2_run_v1:" + hashlib.sha256(canonical).hexdigest()
    if record["run_identifier"] != expected:
        raise ValueError("run_identifier does not match its complete record")


def collect_run_records(value) -> list[dict]:
    """Recursively collect and validate all schema-v1 records in JSON data."""
    records = []
    if isinstance(value, dict):
        if (
            value.get("schema_version") == RUN_RECORD_SCHEMA_VERSION
            and "run_identifier" in value
        ):
            validate_run_record(value)
            records.append(value)
        else:
            for child in value.values():
                records.extend(collect_run_records(child))
    elif isinstance(value, list):
        for child in value:
            records.extend(collect_run_records(child))
    return records


def component_stats(ours: np.ndarray, reference: np.ndarray) -> dict:
    absolute = np.abs(ours - reference)
    reference_scale = float(np.max(np.abs(reference)))
    relative_floor = max(1e-14 * reference_scale, 1e-300)
    mask = np.abs(reference) > relative_floor
    relative = absolute[mask] / np.abs(reference[mask])
    endpoint_scale = max(abs(float(reference[-1])), relative_floor)
    return {
        "max_abs": float(np.max(absolute)),
        "normalized_linf": float(np.max(absolute) / max(reference_scale, 1e-300)),
        "max_rel_excluding_floor": float(np.max(relative)) if relative.size else 0.0,
        "rms_rel_excluding_floor": (
            float(np.sqrt(np.mean(relative**2))) if relative.size else 0.0
        ),
        "relative_floor": relative_floor,
        "endpoint_abs": float(absolute[-1]),
        "endpoint_rel": float(absolute[-1] / endpoint_scale),
        "ours_endpoint": float(ours[-1]),
        "reference_endpoint": float(reference[-1]),
    }


def trajectory_stats(ours: np.ndarray, reference: np.ndarray) -> dict:
    if ours.shape != reference.shape:
        raise ValueError(f"trajectory shape mismatch: {ours.shape} != {reference.shape}")
    return {
        name: component_stats(ours[index], reference[index])
        for index, name in enumerate(COMPONENTS)
    }


def count_sign_changes(values: np.ndarray) -> int:
    signs = np.sign(values)
    nonzero = signs[signs != 0.0]
    return int(np.count_nonzero(nonzero[1:] != nonzero[:-1])) if nonzero.size else 0


def trajectory_diagnostics(t: np.ndarray, y: np.ndarray) -> dict:
    initial_dust_scale = max(abs(float(y[0, 0])), 1e-300)
    result = {}
    for index, name in enumerate(COMPONENTS):
        values = y[index]
        crossing_indices = np.flatnonzero(values[:-1] * values[1:] < 0.0)
        result[name] = {
            "min": float(np.min(values)),
            "max": float(np.max(values)),
            "max_abs": float(np.max(np.abs(values))),
            "endpoint": float(values[-1]),
            "sign_changes": count_sign_changes(values),
            "first_strict_zero_crossing_time": (
                float(t[crossing_indices[0]]) if crossing_indices.size else None
            ),
            "loss_of_positivity": bool(np.any(values < 0.0)),
            "amplification_vs_initial_dust": float(
                np.max(np.abs(values)) / initial_dust_scale
            ),
        }
    return result


def solution_record(solution) -> dict:
    return {
        "config": config_record(solution.config),
        "nfev": solution.nfev,
        "njev": solution.njev,
        "nlu": solution.nlu,
        "message": solution.message,
        "diagnostics": trajectory_diagnostics(solution.t, solution.y),
    }


def scenario_record(scenario: BarotropicScenario, params: TrackerParams) -> dict:
    if scenario.wavenumber_convention is WavenumberConvention.UPSTREAM_TIMESCAPE_K:
        matrix_k = scenario.k
    else:
        matrix_k = scenario.k * params.aD0 * scenario.lcdm_h / scenario.timescape_h
    return {
        "identifier": scenario.identifier,
        "k": scenario.k,
        "matrix_k": matrix_k,
        "branch": scenario.branch.value,
        "tilt_form": scenario.tilt_form.value,
        "rate_convention": scenario.rate_convention.value,
        "epoch": scenario.epoch_choice.value,
        "wavenumber_convention": scenario.wavenumber_convention.value,
        "timescape_h": scenario.timescape_h,
        "lcdm_h": scenario.lcdm_h,
    }


def common_metadata(oracle: dict) -> dict:
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": version("numpy"),
        "scipy": version("scipy"),
        "oracle_provenance": oracle["provenance"],
        "run_record_schema": run_record_schema(),
        "metric": (
            "per-component normalized_linf = max(abs(ours-reference)) / "
            "max(max(abs(reference)), 1e-300)"
        ),
    }


def baseline_scenario(k: float, branch: D3Branch) -> BarotropicScenario:
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


def solve_mode(
    *,
    params: TrackerParams,
    scenario: BarotropicScenario,
    t_eval: np.ndarray,
    config: SolverConfig,
    G: float,
    sound_speed_mode: forensic._ForensicSoundSpeed,
):
    if sound_speed_mode is forensic._ForensicSoundSpeed.CORRECTED_PHASE1B:
        return solve_barotropic(
            params=params,
            scenario=scenario,
            recipe=PLANCK_2018_QPLUS_RECIPE,
            time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
            epoch_root=PHASE1C_EPOCH_ROOT,
            t_eval=t_eval,
            config=config,
            G=G,
        )
    return forensic._solve_forensic_barotropic(
        params=params,
        scenario=scenario,
        sound_speed_mode=sound_speed_mode,
        recipe=PLANCK_2018_QPLUS_RECIPE,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        epoch_root=PHASE1C_EPOCH_ROOT,
        t_eval=t_eval,
        config=config,
        G=G,
    )


def transformed_v_to_vtilde(solution, params: TrackerParams) -> np.ndarray:
    return np.column_stack(
        [
            transform_barotropic_state(
                float(t),
                solution.y[:, index],
                params=params,
                from_tilt_form=TiltForm.UNRESCALED_V,
                to_tilt_form=TiltForm.RESCALED_VTILDE,
            )
            for index, t in enumerate(solution.t)
        ]
    )


def oracle_comparison(oracle: dict, params: TrackerParams, G: float, t_eval: np.ndarray) -> dict:
    modes = {}
    worst = 0.0
    for k in K_VALUES:
        selected = baseline_scenario(k, D3Branch.PRINTED_4_15)
        solution = solve_mode(
            params=params,
            scenario=selected,
            t_eval=t_eval,
            config=UPSTREAM_RK45_DEFAULTS,
            G=G,
            sound_speed_mode=forensic._ForensicSoundSpeed.UPSTREAM_D2_CORRUPTED,
        )
        key = format(k, ".17g")
        reference = np.asarray(oracle["barotropic"][key]["y"], dtype=np.float64)
        stats = trajectory_stats(solution.y, reference)
        worst = max(worst, max(value["normalized_linf"] for value in stats.values()))
        modes[key] = {
            "scenario": scenario_record(selected, params),
            "sound_speed": "upstream_d2_corrupted",
            "statistics": stats,
            "independent_run_record": run_record(
                selected, UPSTREAM_RK45_DEFAULTS, "upstream_d2_corrupted"
            ),
            "upstream_oracle_run_record": run_record(
                selected, UPSTREAM_RK45_DEFAULTS, "upstream_d2_corrupted"
            ),
            "independent_solver": solution_record(solution),
            "upstream_solver": {
                name: oracle["barotropic"][key][name]
                for name in ("success", "message", "nfev", "njev", "nlu")
            },
        }
    return {
        **common_metadata(oracle),
        "gate_normalized_linf": ORACLE_GATE,
        "worst_normalized_linf": worst,
        "modes": modes,
    }


def convergence_study(oracle: dict, params: TrackerParams, G: float, t_eval: np.ndarray) -> dict:
    configs = {
        "upstream_RK45": UPSTREAM_RK45_DEFAULTS,
        "medium_RK45": MEDIUM_RK45,
        "tight_RK45": TIGHT_RK45,
        "medium_DOP853": MEDIUM_DOP853,
        "tight_DOP853": TIGHT_DOP853,
        "tight_Radau": TIGHT_RADAU,
        "reference_DOP853": REFERENCE_DOP853,
    }
    modes = {}
    tight_values = []
    radau_values = []
    for branch in D3Branch:
        for k in K_VALUES:
            selected = baseline_scenario(k, branch)
            reference = solve_mode(
                params=params,
                scenario=selected,
                t_eval=t_eval,
                config=REFERENCE_DOP853,
                G=G,
                sound_speed_mode=forensic._ForensicSoundSpeed.CORRECTED_PHASE1B,
            )
            runs = {}
            for label, config in configs.items():
                solution = reference if label == "reference_DOP853" else solve_mode(
                    params=params,
                    scenario=selected,
                    t_eval=t_eval,
                    config=config,
                    G=G,
                    sound_speed_mode=forensic._ForensicSoundSpeed.CORRECTED_PHASE1B,
                )
                stats = trajectory_stats(solution.y, reference.y)
                runs[label] = {
                    "run_record": run_record(
                        selected, config, "corrected_phase1b"
                    ),
                    "statistics_vs_reference": stats,
                    "solver": solution_record(solution),
                }
                if label in {"tight_RK45", "tight_DOP853"}:
                    tight_values.extend(v["normalized_linf"] for v in stats.values())
                if label == "tight_Radau":
                    radau_values.extend(v["normalized_linf"] for v in stats.values())
            rk_nfev = runs["tight_RK45"]["solver"]["nfev"]
            radau_nfev = runs["tight_Radau"]["solver"]["nfev"]
            modes[selected.identifier] = {
                "scenario": scenario_record(selected, params),
                "runs": runs,
                "stiffness_diagnostic": {
                    "tight_RK45_to_Radau_nfev_ratio": rk_nfev / max(radau_nfev, 1),
                    "classified_stiff_by_nfev_ratio_gt_5": bool(
                        rk_nfev / max(radau_nfev, 1) > 5.0
                    ),
                    "definition": (
                        "empirical only: tight RK45 nfev / tight Radau nfev; "
                        "ratio > 5 is flagged, not asserted as a formal stiffness proof"
                    ),
                },
            }
    return {
        **common_metadata(oracle),
        "reference": config_record(REFERENCE_DOP853),
        "gates": {
            "tight_explicit_normalized_linf": TIGHT_EXPLICIT_GATE,
            "implicit_crosscheck_normalized_linf": IMPLICIT_CROSSCHECK_GATE,
        },
        "worst_tight_explicit_normalized_linf": max(tight_values),
        "worst_radau_normalized_linf": max(radau_values),
        "modes": modes,
    }


def factorial_study(oracle: dict, params: TrackerParams, G: float, t_eval: np.ndarray) -> dict:
    modes = {}
    for k in K_VALUES:
        runs = {}
        arrays = {}
        for sound_mode in forensic._ForensicSoundSpeed:
            for branch in D3Branch:
                selected = baseline_scenario(k, branch)
                solution = solve_mode(
                    params=params,
                    scenario=selected,
                    t_eval=t_eval,
                    config=TIGHT_DOP853,
                    G=G,
                    sound_speed_mode=sound_mode,
                )
                label = f"sound={sound_mode.value}|branch={branch.value}"
                arrays[label] = solution.y
                runs[label] = {
                    "scenario": scenario_record(selected, params),
                    "sound_speed": sound_mode.value,
                    "run_record": run_record(
                        selected, TIGHT_DOP853, sound_mode.value
                    ),
                    "solver": solution_record(solution),
                }
        clean_printed = arrays["sound=corrected_phase1b|branch=printed_4_15"]
        clean_derived = arrays["sound=corrected_phase1b|branch=derived_4_10"]
        d2_printed = arrays["sound=upstream_d2_corrupted|branch=printed_4_15"]
        d2_derived = arrays["sound=upstream_d2_corrupted|branch=derived_4_10"]
        interaction = d2_derived - d2_printed - clean_derived + clean_printed
        modes[format(k, ".17g")] = {
            "runs": runs,
            "d2_only_at_printed_branch": trajectory_stats(d2_printed, clean_printed),
            "d3_only_with_corrected_sound_speed": trajectory_stats(
                clean_derived, clean_printed
            ),
            "d2_only_at_derived_branch": trajectory_stats(d2_derived, clean_derived),
            "d3_only_with_d2_sound_speed": trajectory_stats(d2_derived, d2_printed),
            "interaction": {
                name: {
                    "endpoint": float(interaction[index, -1]),
                    "max_abs": float(np.max(np.abs(interaction[index]))),
                    "endpoint_normalized_to_corrected_printed": float(
                        interaction[index, -1]
                        / max(abs(float(clean_printed[index, -1])), 1e-300)
                    ),
                }
                for index, name in enumerate(COMPONENTS)
            },
        }
    return {
        **common_metadata(oracle),
        "design": (
            "2x2: sound speed {corrected_phase1b, upstream_d2_corrupted} x "
            "D3 branch {printed_4_15, derived_4_10}; all other choices fixed "
            "to the upstream baseline; tight DOP853"
        ),
        "modes": modes,
    }


def tilt_study(
    params: TrackerParams,
    G: float,
    t_eval: np.ndarray,
    k: float,
    branch: D3Branch,
    sound_mode: forensic._ForensicSoundSpeed,
) -> dict:
    selected_v = baseline_scenario(k, branch)
    selected_tilde = replace(selected_v, tilt_form=TiltForm.RESCALED_VTILDE)
    solution_v = solve_mode(
        params=params,
        scenario=selected_v,
        t_eval=t_eval,
        config=TIGHT_DOP853,
        G=G,
        sound_speed_mode=sound_mode,
    )
    solution_tilde = solve_mode(
        params=params,
        scenario=selected_tilde,
        t_eval=t_eval,
        config=TIGHT_DOP853,
        G=G,
        sound_speed_mode=sound_mode,
    )
    transformed = transformed_v_to_vtilde(solution_v, params)
    return {
        "sound_speed": sound_mode.value,
        "unrescaled_scenario": scenario_record(selected_v, params),
        "rescaled_scenario": scenario_record(selected_tilde, params),
        "unrescaled_run_record": run_record(
            selected_v, TIGHT_DOP853, sound_mode.value
        ),
        "rescaled_run_record": run_record(
            selected_tilde, TIGHT_DOP853, sound_mode.value
        ),
        "statistics_rescaled_vs_transformed_unrescaled": trajectory_stats(
            solution_tilde.y, transformed
        ),
        "unrescaled_solver": solution_record(solution_v),
        "rescaled_solver": solution_record(solution_tilde),
    }


def scenario_effects(oracle: dict, params: TrackerParams, G: float, t_eval: np.ndarray) -> dict:
    modes = {}
    for k in K_VALUES:
        baseline = baseline_scenario(k, D3Branch.PRINTED_4_15)
        base_solution = solve_mode(
            params=params,
            scenario=baseline,
            t_eval=t_eval,
            config=TIGHT_DOP853,
            G=G,
            sound_speed_mode=forensic._ForensicSoundSpeed.CORRECTED_PHASE1B,
        )
        rate_scenario = replace(
            baseline,
            rate_convention=RateUnitConvention.LCDM_TO_TIMESCAPE_CONVERTED,
        )
        k_scenario = replace(
            baseline,
            wavenumber_convention=WavenumberConvention.PAPER_LCDM_HUBBLE_K,
        )
        epoch_scenario = replace(baseline, epoch_choice=EpochChoice.DRESSED_Z20)
        dressed_epoch = EpochScenario(
            choice=epoch_scenario.epoch_choice,
            time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
            root=PHASE1C_EPOCH_ROOT,
        ).resolve(params)
        dressed_eval = np.concatenate(([dressed_epoch.time], t_eval))
        rate_solution = solve_mode(
            params=params,
            scenario=rate_scenario,
            t_eval=t_eval,
            config=TIGHT_DOP853,
            G=G,
            sound_speed_mode=forensic._ForensicSoundSpeed.CORRECTED_PHASE1B,
        )
        k_solution = solve_mode(
            params=params,
            scenario=k_scenario,
            t_eval=t_eval,
            config=TIGHT_DOP853,
            G=G,
            sound_speed_mode=forensic._ForensicSoundSpeed.CORRECTED_PHASE1B,
        )
        epoch_full = solve_mode(
            params=params,
            scenario=epoch_scenario,
            t_eval=dressed_eval,
            config=TIGHT_DOP853,
            G=G,
            sound_speed_mode=forensic._ForensicSoundSpeed.CORRECTED_PHASE1B,
        )
        modes[format(k, ".17g")] = {
            "baseline": {
                "scenario": scenario_record(baseline, params),
                "sound_speed": "corrected_phase1b",
                "run_record": run_record(
                    baseline, TIGHT_DOP853, "corrected_phase1b"
                ),
                "solver": solution_record(base_solution),
            },
            "initial_Z_rate_only": {
                "scenario": scenario_record(rate_scenario, params),
                "run_record": run_record(
                    rate_scenario, TIGHT_DOP853, "corrected_phase1b"
                ),
                "statistics_vs_baseline": trajectory_stats(
                    rate_solution.y, base_solution.y
                ),
                "solver": solution_record(rate_solution),
            },
            "initial_epoch_only": {
                "scenario": scenario_record(epoch_scenario, params),
                "run_record": run_record(
                    epoch_scenario, TIGHT_DOP853, "corrected_phase1b"
                ),
                "comparison_interval": [float(t_eval[0]), float(t_eval[-1])],
                "statistics_vs_baseline": trajectory_stats(
                    epoch_full.y[:, 1:], base_solution.y
                ),
                "solver": solution_record(epoch_full),
            },
            "wavenumber_normalisation_only": {
                "scenario": scenario_record(k_scenario, params),
                "run_record": run_record(
                    k_scenario, TIGHT_DOP853, "corrected_phase1b"
                ),
                "statistics_vs_baseline": trajectory_stats(
                    k_solution.y, base_solution.y
                ),
                "solver": solution_record(k_solution),
            },
            "tilt_forms": {
                f"sound={sound.value}|branch={branch.value}": tilt_study(
                    params, G, t_eval, k, branch, sound
                )
                for sound in forensic._ForensicSoundSpeed
                for branch in D3Branch
            },
        }
    return {
        **common_metadata(oracle),
        "baseline_definition": (
            "corrected Phase 1B sound speed, printed_4_15, unrescaled_V, "
            "upstream_unconverted, upstream_0p218_gyr, upstream_timescape_k, "
            "tight DOP853"
        ),
        "modes": modes,
    }


def figure_endpoints(
    oracle: dict,
    params: TrackerParams,
    G: float,
    t_eval: np.ndarray,
) -> dict:
    modes = {}
    for k in K_VALUES:
        key = format(k, ".17g")
        entry = {
            "upstream_oracle": {
                "run_record": run_record(
                    baseline_scenario(k, D3Branch.PRINTED_4_15),
                    UPSTREAM_RK45_DEFAULTS,
                    "upstream_d2_corrupted",
                ),
                "Delta_d_endpoint": float(oracle["barotropic"][key]["y"][0][-1]),
                "Delta_eff_raw_endpoint": float(
                    oracle["barotropic"][key]["y"][2][-1]
                ),
                "Delta_eff_over_k2_endpoint": float(
                    oracle["barotropic"][key]["y"][2][-1] / k**2
                ),
            }
        }
        for branch in D3Branch:
            selected = baseline_scenario(k, branch)
            solution = solve_mode(
                params=params,
                scenario=selected,
                t_eval=t_eval,
                config=TIGHT_DOP853,
                G=G,
                sound_speed_mode=forensic._ForensicSoundSpeed.CORRECTED_PHASE1B,
            )
            entry[f"corrected_{branch.value}"] = {
                "scenario": scenario_record(selected, params),
                "run_record": run_record(
                    selected, TIGHT_DOP853, "corrected_phase1b"
                ),
                "solver": solution_record(solution),
                "Delta_d_endpoint": float(solution.y[0, -1]),
                "Delta_eff_raw_endpoint": float(solution.y[2, -1]),
                "Delta_eff_over_k2_endpoint": float(solution.y[2, -1] / k**2),
            }
        modes[key] = entry
    return {
        **common_metadata(oracle),
        "right_panel_note": (
            "Both raw Delta_eff (notebook cell 19) and Delta_eff/k^2 "
            "([GM] Figure 3 caption) are recorded explicitly."
        ),
        "modes": modes,
    }


def main() -> int:
    if not ORACLE_PATH.exists():
        print(
            f"ERROR: missing {ORACLE_PATH}; run extract_upstream_barotropic_oracle.py",
            file=sys.stderr,
        )
        return 2
    oracle = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))
    constants = oracle["constants"]
    params = TrackerParams(fv0=constants["fv0"], HD0=constants["HD0"])
    G = float(constants["G"])
    t_eval = np.asarray(oracle["t_eval"], dtype=np.float64)

    comparison = oracle_comparison(oracle, params, G, t_eval)
    convergence = convergence_study(oracle, params, G, t_eval)
    factorial = factorial_study(oracle, params, G, t_eval)
    scenarios = scenario_effects(oracle, params, G, t_eval)
    endpoints = figure_endpoints(oracle, params, G, t_eval)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        ORACLE_COMPARISON_PATH: comparison,
        CONVERGENCE_PATH: convergence,
        FACTORIAL_PATH: factorial,
        SCENARIO_PATH: scenarios,
        ENDPOINT_PATH: endpoints,
    }
    for path, data in outputs.items():
        records = collect_run_records(data)
        if not records:
            raise ValueError(f"no B2 run records found in {path.name}")
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"Written: {path.relative_to(PROJECT_ROOT)}")

    print(f"Oracle worst normalized L-inf: {comparison['worst_normalized_linf']:.3e}")
    print(
        "Tight explicit worst vs reference: "
        f"{convergence['worst_tight_explicit_normalized_linf']:.3e}"
    )
    print(
        "Radau worst vs reference: "
        f"{convergence['worst_radau_normalized_linf']:.3e}"
    )
    if comparison["worst_normalized_linf"] > ORACLE_GATE:
        print("FAIL: upstream reproduction gate exceeded", file=sys.stderr)
        return 1
    if convergence["worst_tight_explicit_normalized_linf"] > TIGHT_EXPLICIT_GATE:
        print("FAIL: tight explicit convergence gate exceeded", file=sys.stderr)
        return 1
    if convergence["worst_radau_normalized_linf"] > IMPLICIT_CROSSCHECK_GATE:
        print("FAIL: implicit cross-check gate exceeded", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
