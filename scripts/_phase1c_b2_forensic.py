"""Non-exported Phase 1C-B2 forensic compatibility machinery.

This module is intentionally outside ``timescape_fsigma8``.  It reimplements
the upstream D2-corrupted sound-speed expression solely to reproduce the
pinned notebook and quantify D2.  Scientific runs must use the public package,
which exposes only the corrected Phase 1B background sound speed.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from functools import partial

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.integrate import solve_ivp

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations.barotropic import (
    D3Branch,
    TiltForm,
    WavenumberConvention,
    resolve_wavenumber,
)
from timescape_fsigma8.perturbations.barotropic_solver import BarotropicScenario
from timescape_fsigma8.perturbations.initial_conditions import (
    InitialConditionScenario,
    LCDMGrowthRecipe,
)
from timescape_fsigma8.perturbations.scenarios import (
    EpochRootConfig,
    EpochScenario,
    TimeUnit,
)
from timescape_fsigma8.perturbations.solver import SolverConfig


class _ForensicSoundSpeed(str, Enum):
    CORRECTED_PHASE1B = "corrected_phase1b"
    UPSTREAM_D2_CORRUPTED = "upstream_d2_corrupted"


def _upstream_d2_corrupted_cs2(
    t: ArrayLike, params: TrackerParams
) -> NDArray[np.float64]:
    """Return the D2-corrupted notebook sound speed for forensics only.

    This tracker closed form was independently derived in the Phase 1C-A
    audit from the cell-6 ``dQDdt`` multiplication defect and the [GM] Sec. 4
    definition ``cs2_eff=dp_eff/dt / drho_eff/dt``.  It is not scientific
    package code and is never exported through ``timescape_fsigma8``.
    """
    f = bg.fv(t, params)
    numerator = (
        18.0 * f**6
        - 54.0 * f**5
        + 54.0 * f**4
        - 18.0 * f**3
        - f**2
        - 2.0
    )
    denominator = (
        18.0 * f**6
        - 54.0 * f**5
        + 54.0 * f**4
        - 18.0 * f**3
        - f**2
        + 6.0 * f
        + 4.0
    )
    return np.asarray(numerator / denominator, dtype=np.float64)


def _sound_speed(
    t: float,
    params: TrackerParams,
    mode: _ForensicSoundSpeed,
) -> float:
    if not isinstance(mode, _ForensicSoundSpeed):
        raise ValueError("mode must be an explicit _ForensicSoundSpeed")
    if mode is _ForensicSoundSpeed.CORRECTED_PHASE1B:
        return float(bg.cs2_eff(t, params))
    if mode is _ForensicSoundSpeed.UPSTREAM_D2_CORRUPTED:
        return float(_upstream_d2_corrupted_cs2(t, params))
    raise ValueError(f"unsupported forensic sound-speed mode: {mode!r}")


def _forensic_barotropic_matrix(
    t: float,
    *,
    params: TrackerParams,
    G: float,
    scenario: BarotropicScenario,
    sound_speed_mode: _ForensicSoundSpeed,
) -> NDArray[np.float64]:
    """Build [GM] Eqs. (4.14)-(4.17) for a stated forensic sound speed.

    The rescaled and unrescaled tilt forms are implemented directly, as in
    the independent scientific matrix.  With the D2 value, they intentionally
    cease to be related by the exact [GM] Eq. (3.17) ``w_dot`` identity.
    """
    if G <= 0.0 or not np.isfinite(G):
        raise ValueError("G must be finite and positive")
    if not isinstance(scenario, BarotropicScenario):
        raise ValueError("scenario must be an explicit BarotropicScenario")
    resolved_k = resolve_wavenumber(
        scenario.k,
        params=params,
        convention=scenario.wavenumber_convention,
        timescape_h=scenario.timescape_h,
        lcdm_h=scenario.lcdm_h,
    )
    theta = float(bg.Theta(t, params))
    rho_d = float(bg.rho_d(t, params, G))
    rho_eff = float(bg.rho_eff(t, params, G))
    w_eff = float(bg.w_eff(t, params))
    cs2_eff = _sound_speed(t, params, sound_speed_mode)
    scale_factor = float(bg.a_D(t, params))
    one_plus_w = 1.0 + w_eff
    four_pi_G = 4.0 * np.pi * G
    matrix = np.zeros((4, 4), dtype=np.float64)
    # [GM] Eq. (4.14).
    matrix[0, 1] = -1.0
    # [GM] Eq. (4.16).
    matrix[1, 0] = -four_pi_G * rho_d
    matrix[1, 1] = -(2.0 / 3.0) * theta
    matrix[1, 2] = -four_pi_G * rho_eff * (1.0 + 3.0 * cs2_eff)
    # [GM] Eq. (4.15), with the forensic-versus-derived branch explicit.
    matrix[2, 1] = -one_plus_w
    branch_sign = 1.0 if scenario.branch is D3Branch.PRINTED_4_15 else -1.0
    matrix[2, 2] = (w_eff + branch_sign * cs2_eff) * theta
    k2_over_a = resolved_k.matrix_k**2 / scale_factor
    if scenario.tilt_form is TiltForm.RESCALED_VTILDE:
        # [GM] Eqs. (4.15) and (4.17).
        matrix[2, 3] = k2_over_a
        matrix[3, 2] = -cs2_eff / scale_factor
        matrix[3, 3] = (theta / 3.0) * (3.0 * w_eff - 1.0)
    elif scenario.tilt_form is TiltForm.UNRESCALED_V:
        # [GM] Eq. (4.15) transformed to V and Eq. (4.8) plus (4.13).
        matrix[2, 3] = k2_over_a * one_plus_w
        matrix[3, 2] = -cs2_eff / (scale_factor * one_plus_w)
        matrix[3, 3] = (theta / 3.0) * (3.0 * cs2_eff - 1.0)
    else:  # pragma: no cover - scenario validation is exhaustive
        raise ValueError(f"unsupported tilt form: {scenario.tilt_form!r}")
    return matrix


def _forensic_barotropic_rhs(
    t: float,
    state: ArrayLike,
    *,
    params: TrackerParams,
    G: float,
    scenario: BarotropicScenario,
    sound_speed_mode: _ForensicSoundSpeed,
) -> NDArray[np.float64]:
    values = np.asarray(state, dtype=np.float64)
    if values.shape != (4,) or not np.all(np.isfinite(values)):
        raise ValueError("forensic barotropic state must be a finite shape-(4,) array")
    return _forensic_barotropic_matrix(
        t,
        params=params,
        G=G,
        scenario=scenario,
        sound_speed_mode=sound_speed_mode,
    ) @ values


@dataclass(frozen=True)
class _ForensicSolution:
    t: NDArray[np.float64]
    y: NDArray[np.float64]
    scenario: BarotropicScenario
    sound_speed_mode: _ForensicSoundSpeed
    config: SolverConfig
    nfev: int
    njev: int
    nlu: int
    message: str


def _solve_forensic_barotropic(
    *,
    params: TrackerParams,
    scenario: BarotropicScenario,
    sound_speed_mode: _ForensicSoundSpeed,
    recipe: LCDMGrowthRecipe,
    time_unit: TimeUnit,
    epoch_root: EpochRootConfig,
    t_eval: ArrayLike,
    config: SolverConfig,
    G: float,
) -> _ForensicSolution:
    """Integrate a forensic [GM] (4.14)-(4.17) scenario with explicit numerics."""
    if not isinstance(sound_speed_mode, _ForensicSoundSpeed):
        raise ValueError("sound_speed_mode must be explicit")
    initial = InitialConditionScenario(
        recipe=recipe,
        rate_units=scenario.rate_convention,
        timescape_h=scenario.timescape_h,
    ).resolve(params)
    epoch = EpochScenario(
        choice=scenario.epoch_choice,
        time_unit=time_unit,
        root=epoch_root,
    ).resolve(params)
    times = np.asarray(t_eval, dtype=np.float64)
    if times.ndim != 1 or times.size < 2 or np.any(np.diff(times) <= 0.0):
        raise ValueError("t_eval must be a strictly increasing one-dimensional grid")
    if not np.isclose(times[0], epoch.time, rtol=0.0, atol=1e-14):
        raise ValueError("t_eval start does not match the explicit epoch")
    y0 = np.array(
        [initial.delta_d, initial.expansion_gradient, initial.delta_eff, 0.0],
        dtype=np.float64,
    )
    rhs = partial(
        _forensic_barotropic_rhs,
        params=params,
        G=G,
        scenario=scenario,
        sound_speed_mode=sound_speed_mode,
    )
    result = solve_ivp(
        rhs,
        (float(times[0]), float(times[-1])),
        y0,
        method=config.method,
        t_eval=times,
        dense_output=False,
        events=None,
        vectorized=False,
        rtol=config.rtol,
        atol=config.atol,
        max_step=config.max_step,
        first_step=config.first_step,
    )
    if not result.success:
        raise RuntimeError(
            f"forensic integration failed for {scenario.identifier}, "
            f"sound_speed={sound_speed_mode.value}: {result.message}"
        )
    return _ForensicSolution(
        t=np.asarray(result.t, dtype=np.float64),
        y=np.asarray(result.y, dtype=np.float64),
        scenario=scenario,
        sound_speed_mode=sound_speed_mode,
        config=config,
        nfev=int(result.nfev),
        njev=int(result.njev),
        nlu=int(result.nlu),
        message=str(result.message),
    )
