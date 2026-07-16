"""Validate clean Timescape perturbations against oracle and solver changes.

Reads the local upstream numerical oracle, runs the independent Mészáros and
comoving systems, and writes three git-ignored machine-readable outputs:

* ``phase1c_b1_oracle_comparison.json``;
* ``phase1c_b1_convergence.json``;
* ``phase1c_b1_scenario_effects.json``.

No upstream source is imported or reproduced by this script.
"""

from __future__ import annotations

import json
import platform
import sys
from dataclasses import asdict
from importlib.metadata import version
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from timescape_fsigma8.background import TrackerParams  # noqa: E402
from timescape_fsigma8.perturbations import (  # noqa: E402
    PHASE1C_EPOCH_ROOT,
    PLANCK_2018_QPLUS_RECIPE,
    TIGHT_DOP853,
    TIGHT_RADAU,
    TIGHT_RK45,
    UPSTREAM_NOTEBOOK_TIME_UNIT,
    UPSTREAM_RK45_DEFAULTS,
    EpochChoice,
    EpochScenario,
    InitialConditionScenario,
    RateUnitConvention,
    SolverConfig,
    solve_comoving,
    solve_meszaros,
)


ORACLE_PATH = PROJECT_ROOT / "artifacts" / "upstream" / "oracle_clean_perturbations.json"
OUT_DIR = PROJECT_ROOT / "artifacts" / "independent"
COMPARISON_PATH = OUT_DIR / "phase1c_b1_oracle_comparison.json"
CONVERGENCE_PATH = OUT_DIR / "phase1c_b1_convergence.json"
SCENARIO_PATH = OUT_DIR / "phase1c_b1_scenario_effects.json"

REFERENCE_DOP853 = SolverConfig(
    method="DOP853", rtol=2e-13, atol=2e-15, max_step=np.inf, first_step=None
)
MEDIUM_DOP853 = SolverConfig(
    method="DOP853", rtol=1e-8, atol=1e-10, max_step=np.inf, first_step=None
)
MEDIUM_RK45 = SolverConfig(
    method="RK45", rtol=1e-6, atol=1e-8, max_step=np.inf, first_step=None
)

# Gates are numerical validation criteria, not physical-precision claims.
ORACLE_NORMALIZED_LINF_GATE = 2e-8
TIGHT_EXPLICIT_GATE = 2e-8
IMPLICIT_CROSSCHECK_GATE = 2e-8


def config_record(config: SolverConfig) -> dict:
    record = asdict(config)
    if np.isinf(record["max_step"]):
        record["max_step"] = "inf"
    return record


def component_stats(ours: np.ndarray, reference: np.ndarray) -> dict:
    absolute = np.abs(ours - reference)
    reference_scale = float(np.max(np.abs(reference)))
    relative_floor = max(1e-14 * reference_scale, 1e-300)
    mask = np.abs(reference) > relative_floor
    relative = absolute[mask] / np.abs(reference[mask])
    index = int(np.argmax(absolute))
    endpoint_scale = max(abs(float(reference[-1])), relative_floor)
    return {
        "max_abs": float(np.max(absolute)),
        "normalized_linf": float(np.max(absolute) / max(reference_scale, 1e-300)),
        "max_rel_excluding_floor": float(np.max(relative)) if relative.size else 0.0,
        "rms_rel_excluding_floor": float(np.sqrt(np.mean(relative**2))) if relative.size else 0.0,
        "relative_floor": relative_floor,
        "index_at_max_abs": index,
        "endpoint_abs": float(absolute[-1]),
        "endpoint_rel": float(absolute[-1] / endpoint_scale),
        "ours_endpoint": float(ours[-1]),
        "reference_endpoint": float(reference[-1]),
    }


def trajectory_stats(
    ours: np.ndarray, reference: np.ndarray, component_names: list[str]
) -> dict:
    if ours.shape != reference.shape:
        raise ValueError(f"trajectory shape mismatch: {ours.shape} != {reference.shape}")
    return {
        name: component_stats(ours[index], reference[index])
        for index, name in enumerate(component_names)
    }


def solution_record(solution) -> dict:
    return {
        "config": config_record(solution.config),
        "nfev": solution.nfev,
        "njev": solution.njev,
        "nlu": solution.nlu,
        "message": solution.message,
    }


def solve_pair(params, initial, t_eval, config, G):
    return {
        "comoving": solve_comoving(
            params=params,
            initial_conditions=initial,
            t_eval=t_eval,
            config=config,
            G=G,
        ),
        "meszaros": solve_meszaros(
            params=params,
            initial_conditions=initial,
            t_eval=t_eval,
            config=config,
            G=G,
        ),
    }


def common_metadata(oracle: dict) -> dict:
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": version("numpy"),
        "scipy": version("scipy"),
        "oracle_provenance": oracle["provenance"],
        "note": (
            "Numerical error gates validate deterministic trajectories for the stated "
            "parameters and solver settings; they are not physical uncertainty estimates."
        ),
    }


def main() -> int:
    if not ORACLE_PATH.exists():
        print(
            f"ERROR: missing {ORACLE_PATH}; run extract_upstream_perturbation_oracle.py",
            file=sys.stderr,
        )
        return 2
    oracle = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))
    constants = oracle["constants"]
    params = TrackerParams(fv0=constants["fv0"], HD0=constants["HD0"])
    G = float(constants["G"])
    t_eval = np.asarray(oracle["t_eval"], dtype=np.float64)

    initial_upstream = InitialConditionScenario(
        recipe=PLANCK_2018_QPLUS_RECIPE,
        rate_units=RateUnitConvention.UPSTREAM_UNCONVERTED,
        timescape_h=constants["h"],
    ).resolve(params)
    epoch_upstream = EpochScenario(
        choice=EpochChoice.UPSTREAM_0P218_GYR,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        root=PHASE1C_EPOCH_ROOT,
    ).resolve(params)
    if t_eval[0] != epoch_upstream.time:
        raise RuntimeError(
            f"oracle start {t_eval[0]} does not equal resolved upstream epoch {epoch_upstream.time}"
        )

    # 1. Like-for-like upstream reproduction with every solve_ivp default explicit.
    reproduced = solve_pair(params, initial_upstream, t_eval, UPSTREAM_RK45_DEFAULTS, G)
    component_names = {
        "comoving": ["Delta_d", "Z", "Delta_eff"],
        "meszaros": ["Delta_d", "Delta_d_dot"],
    }
    oracle_stats = {}
    worst_oracle = 0.0
    for system, solution in reproduced.items():
        reference = np.asarray(oracle[system]["y"], dtype=np.float64)
        stats = trajectory_stats(solution.y, reference, component_names[system])
        worst_oracle = max(
            worst_oracle,
            max(item["normalized_linf"] for item in stats.values()),
        )
        oracle_stats[system] = {
            "statistics": stats,
            "independent_solver": solution_record(solution),
            "upstream_solver": {
                key: oracle[system][key] for key in ("success", "message", "nfev", "njev", "nlu")
            },
        }
    comparison = {
        **common_metadata(oracle),
        "scenario": {
            "epoch": epoch_upstream.choice.value,
            "rate_units": initial_upstream.rate_units.value,
            "t_initial": epoch_upstream.time,
            "t_initial_gyr": epoch_upstream.time_gyr,
            "initial_conditions": initial_upstream.comoving_vector().tolist(),
        },
        "gate_normalized_linf": ORACLE_NORMALIZED_LINF_GATE,
        "worst_normalized_linf": worst_oracle,
        "systems": oracle_stats,
    }

    # 2. Convergence and an independent implicit-solver cross-check.
    configurations = {
        "upstream_RK45": UPSTREAM_RK45_DEFAULTS,
        "medium_RK45": MEDIUM_RK45,
        "tight_RK45": TIGHT_RK45,
        "medium_DOP853": MEDIUM_DOP853,
        "tight_DOP853": TIGHT_DOP853,
        "tight_Radau": TIGHT_RADAU,
        "reference_DOP853": REFERENCE_DOP853,
    }
    reference = solve_pair(params, initial_upstream, t_eval, REFERENCE_DOP853, G)
    convergence_systems = {"comoving": {}, "meszaros": {}}
    for label, config in configurations.items():
        solutions = reference if label == "reference_DOP853" else solve_pair(
            params, initial_upstream, t_eval, config, G
        )
        for system, solution in solutions.items():
            convergence_systems[system][label] = {
                "statistics_vs_reference": trajectory_stats(
                    solution.y, reference[system].y, component_names[system]
                ),
                "solver": solution_record(solution),
            }
    convergence = {
        **common_metadata(oracle),
        "reference": config_record(REFERENCE_DOP853),
        "gates": {
            "tight_explicit_normalized_linf": TIGHT_EXPLICIT_GATE,
            "implicit_crosscheck_normalized_linf": IMPLICIT_CROSSCHECK_GATE,
        },
        "systems": convergence_systems,
    }

    # 3. One-factor-at-a-time IC-unit and epoch effects using tight DOP853.
    initial_converted = InitialConditionScenario(
        recipe=PLANCK_2018_QPLUS_RECIPE,
        rate_units=RateUnitConvention.LCDM_TO_TIMESCAPE_CONVERTED,
        timescape_h=constants["h"],
    ).resolve(params)
    epoch_dressed = EpochScenario(
        choice=EpochChoice.DRESSED_Z20,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        root=PHASE1C_EPOCH_ROOT,
    ).resolve(params)

    common_eval = t_eval
    base = solve_pair(params, initial_upstream, common_eval, TIGHT_DOP853, G)
    rate_changed = solve_pair(params, initial_converted, common_eval, TIGHT_DOP853, G)
    # The z=20 solution begins earlier; include its initial time and compare
    # only the shared [0.218 Gyr, t0] evaluation grid.
    dressed_eval = np.concatenate(([epoch_dressed.time], common_eval))
    epoch_changed_full = solve_pair(
        params, initial_upstream, dressed_eval, TIGHT_DOP853, G
    )
    both_changed_full = solve_pair(
        params, initial_converted, dressed_eval, TIGHT_DOP853, G
    )
    scenario_systems = {}
    for system in ("comoving", "meszaros"):
        epoch_shared = epoch_changed_full[system].y[:, 1:]
        both_shared = both_changed_full[system].y[:, 1:]
        scenario_systems[system] = {
            "rate_units_only": trajectory_stats(
                rate_changed[system].y, base[system].y, component_names[system]
            ),
            "epoch_only": trajectory_stats(
                epoch_shared, base[system].y, component_names[system]
            ),
            "rate_units_and_epoch": trajectory_stats(
                both_shared, base[system].y, component_names[system]
            ),
        }
    scenarios = {
        **common_metadata(oracle),
        "solver": config_record(TIGHT_DOP853),
        "baseline": {
            "epoch": epoch_upstream.choice.value,
            "rate_units": initial_upstream.rate_units.value,
            "t_initial": epoch_upstream.time,
            "t_initial_gyr": epoch_upstream.time_gyr,
            "Z_initial": initial_upstream.expansion_gradient,
        },
        "alternatives": {
            "epoch": epoch_dressed.choice.value,
            "t_initial": epoch_dressed.time,
            "t_initial_gyr": epoch_dressed.time_gyr,
            "dressed_redshift": epoch_dressed.dressed_redshift,
            "rate_units": initial_converted.rate_units.value,
            "Z_initial": initial_converted.expansion_gradient,
        },
        "comparison_interval": [float(common_eval[0]), float(common_eval[-1])],
        "systems": scenario_systems,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    COMPARISON_PATH.write_text(json.dumps(comparison, indent=2), encoding="utf-8")
    CONVERGENCE_PATH.write_text(json.dumps(convergence, indent=2), encoding="utf-8")
    SCENARIO_PATH.write_text(json.dumps(scenarios, indent=2), encoding="utf-8")

    tight_values = []
    radau_values = []
    for system in convergence_systems.values():
        tight_values.extend(
            value["normalized_linf"]
            for value in system["tight_RK45"]["statistics_vs_reference"].values()
        )
        tight_values.extend(
            value["normalized_linf"]
            for value in system["tight_DOP853"]["statistics_vs_reference"].values()
        )
        radau_values.extend(
            value["normalized_linf"]
            for value in system["tight_Radau"]["statistics_vs_reference"].values()
        )
    worst_tight = max(tight_values)
    worst_radau = max(radau_values)
    print(f"Oracle worst normalized L-inf : {worst_oracle:.3e}")
    print(f"Tight explicit vs reference   : {worst_tight:.3e}")
    print(f"Radau vs reference            : {worst_radau:.3e}")
    print(f"Written: {COMPARISON_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Written: {CONVERGENCE_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Written: {SCENARIO_PATH.relative_to(PROJECT_ROOT)}")

    if worst_oracle > ORACLE_NORMALIZED_LINF_GATE:
        print("FAIL: upstream reproduction gate exceeded", file=sys.stderr)
        return 1
    if worst_tight > TIGHT_EXPLICIT_GATE:
        print("FAIL: tight explicit convergence gate exceeded", file=sys.stderr)
        return 1
    if worst_radau > IMPLICIT_CROSSCHECK_GATE:
        print("FAIL: implicit cross-check gate exceeded", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
