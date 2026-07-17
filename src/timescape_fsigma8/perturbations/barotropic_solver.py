"""Explicit scenario and solver layer for the Timescape barotropic closure."""

from __future__ import annotations

from dataclasses import dataclass
from functools import partial

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.integrate import solve_ivp

from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations.barotropic import (
    D3Branch,
    ResolvedWavenumber,
    TiltForm,
    WavenumberConvention,
    _require_enum,
    barotropic_rhs,
    resolve_wavenumber,
)
from timescape_fsigma8.perturbations.initial_conditions import (
    InitialConditionScenario,
    LCDMGrowthRecipe,
    PerturbationInitialConditions,
    RateUnitConvention,
)
from timescape_fsigma8.perturbations.scenarios import (
    EpochChoice,
    EpochRootConfig,
    EpochScenario,
    ResolvedEpoch,
    TimeUnit,
)
from timescape_fsigma8.perturbations.solver import SolverConfig


@dataclass(frozen=True)
class BarotropicScenario:
    """Complete mandatory scientific interpretation of one barotropic run.

    Every unresolved Phase 1C choice is required and has no default.  The D3
    labels identify equation provenance only; this record does not rank them.
    """

    k: float
    branch: D3Branch
    tilt_form: TiltForm
    rate_convention: RateUnitConvention
    epoch_choice: EpochChoice
    wavenumber_convention: WavenumberConvention
    timescape_h: float
    lcdm_h: float

    def __post_init__(self) -> None:
        if not np.isfinite(self.k) or self.k <= 0.0:
            raise ValueError("scenario k must be finite and positive")
        _require_enum(self.branch, D3Branch, "branch")
        _require_enum(self.tilt_form, TiltForm, "tilt_form")
        _require_enum(
            self.rate_convention, RateUnitConvention, "rate_convention"
        )
        _require_enum(self.epoch_choice, EpochChoice, "epoch_choice")
        _require_enum(
            self.wavenumber_convention,
            WavenumberConvention,
            "wavenumber_convention",
        )
        if not np.isfinite(self.timescape_h) or self.timescape_h <= 0.0:
            raise ValueError("timescape_h must be finite and positive")
        if not np.isfinite(self.lcdm_h) or self.lcdm_h <= 0.0:
            raise ValueError("lcdm_h must be finite and positive")

    @property
    def identifier(self) -> str:
        """Return a complete stable identifier for tables, JSON, and figures."""
        return (
            f"branch={self.branch.value}|tilt={self.tilt_form.value}|"
            f"rate={self.rate_convention.value}|epoch={self.epoch_choice.value}|"
            f"k_convention={self.wavenumber_convention.value}|"
            f"k={self.k:.17g}|h_ts={self.timescape_h:.17g}|"
            f"h_lcdm={self.lcdm_h:.17g}"
        )


@dataclass(frozen=True)
class BarotropicSolution:
    """Typed result of integrating [GM] Eqs. (4.14)-(4.17)."""

    t: NDArray[np.float64]
    y: NDArray[np.float64]
    config: SolverConfig
    scenario: BarotropicScenario
    epoch: ResolvedEpoch
    initial_conditions: PerturbationInitialConditions
    wavenumber: ResolvedWavenumber
    nfev: int
    njev: int
    nlu: int
    message: str


def _evaluation_times(t_eval: ArrayLike, epoch: ResolvedEpoch) -> NDArray[np.float64]:
    times = np.asarray(t_eval, dtype=np.float64)
    if times.ndim != 1 or times.size < 2:
        raise ValueError("t_eval must be one-dimensional with at least two points")
    if not np.all(np.isfinite(times)) or np.any(times <= 0.0):
        raise ValueError("t_eval must contain finite positive times")
    if np.any(np.diff(times) <= 0.0):
        raise ValueError("t_eval must be strictly increasing")
    start_tolerance = max(1e-14, 16.0 * np.finfo(np.float64).eps * epoch.time)
    if not np.isclose(times[0], epoch.time, rtol=0.0, atol=start_tolerance):
        raise ValueError(
            f"t_eval starts at {times[0]}, but explicit epoch "
            f"{epoch.choice.value} resolves to {epoch.time}"
        )
    return times


def solve_barotropic(
    *,
    params: TrackerParams,
    scenario: BarotropicScenario,
    recipe: LCDMGrowthRecipe,
    time_unit: TimeUnit,
    epoch_root: EpochRootConfig,
    t_eval: ArrayLike,
    config: SolverConfig,
    G: float,
) -> BarotropicSolution:
    """Solve [GM] Eqs. (4.14)-(4.17) for one fully explicit scenario.

    ``Delta_eff(t_i)=0`` and ``Vtilde(t_i)=0`` are the initial conditions in
    [GM] Sec. 5.1.2.  Since ``1+w_eff`` is finite, the unrescaled ``V`` also
    starts at zero.  The rate and epoch interpretations are mandatory fields
    of ``scenario`` rather than solver defaults.
    """
    if not isinstance(scenario, BarotropicScenario):
        raise ValueError("scenario must be an explicit BarotropicScenario")
    if G <= 0.0 or not np.isfinite(G):
        raise ValueError("G must be finite and positive")
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
    times = _evaluation_times(t_eval, epoch)
    y0 = np.array(
        [initial.delta_d, initial.expansion_gradient, initial.delta_eff, 0.0],
        dtype=np.float64,
    )
    wavenumber = resolve_wavenumber(
        scenario.k,
        params=params,
        convention=scenario.wavenumber_convention,
        timescape_h=scenario.timescape_h,
        lcdm_h=scenario.lcdm_h,
    )
    rhs = partial(
        barotropic_rhs,
        params=params,
        G=G,
        k=scenario.k,
        branch=scenario.branch,
        tilt_form=scenario.tilt_form,
        wavenumber_convention=scenario.wavenumber_convention,
        timescape_h=scenario.timescape_h,
        lcdm_h=scenario.lcdm_h,
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
            f"barotropic integration failed for {scenario.identifier}: "
            f"{result.message}"
        )
    return BarotropicSolution(
        t=np.asarray(result.t, dtype=np.float64),
        y=np.asarray(result.y, dtype=np.float64),
        config=config,
        scenario=scenario,
        epoch=epoch,
        initial_conditions=initial,
        wavenumber=wavenumber,
        nfev=int(result.nfev),
        njev=int(result.njev),
        nlu=int(result.nlu),
        message=str(result.message),
    )
