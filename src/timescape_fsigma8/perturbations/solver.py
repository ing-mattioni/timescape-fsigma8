"""Numerical solver layer with explicit methods and tolerances.

No solver method or tolerance has a function default.  Named configurations
are immutable records whose values remain visible at every call site.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from typing import Literal

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.integrate import solve_ivp

from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations.initial_conditions import (
    PerturbationInitialConditions,
)
from timescape_fsigma8.perturbations.systems import comoving_rhs, meszaros_rhs


SolverMethod = Literal["RK45", "DOP853", "Radau"]


@dataclass(frozen=True)
class SolverConfig:
    """Every solve_ivp numerical choice used by the B1 solver layer."""

    method: SolverMethod
    rtol: float
    atol: float
    max_step: float
    first_step: float | None

    def __post_init__(self) -> None:
        if self.method not in {"RK45", "DOP853", "Radau"}:
            raise ValueError(f"unsupported solver method: {self.method}")
        if self.rtol <= 0.0 or self.atol <= 0.0:
            raise ValueError("solver tolerances must be positive")
        if self.max_step <= 0.0:
            raise ValueError("max_step must be positive")
        if self.first_step is not None and self.first_step <= 0.0:
            raise ValueError("first_step must be positive or None")


# Upstream used solve_ivp defaults. Values are spelled out here so the
# reproduction never depends on the installed SciPy defaults.
UPSTREAM_RK45_DEFAULTS = SolverConfig(
    method="RK45", rtol=1e-3, atol=1e-6, max_step=np.inf, first_step=None
)
TIGHT_RK45 = SolverConfig(
    method="RK45", rtol=1e-10, atol=1e-12, max_step=np.inf, first_step=None
)
TIGHT_DOP853 = SolverConfig(
    method="DOP853", rtol=1e-11, atol=1e-13, max_step=np.inf, first_step=None
)
TIGHT_RADAU = SolverConfig(
    method="Radau", rtol=1e-10, atol=1e-12, max_step=np.inf, first_step=None
)


@dataclass(frozen=True)
class PerturbationSolution:
    """Typed, immutable view of a successful solve_ivp result."""

    system: Literal["meszaros", "comoving"]
    t: NDArray[np.float64]
    y: NDArray[np.float64]
    config: SolverConfig
    nfev: int
    njev: int
    nlu: int
    message: str


def _evaluation_times(t_eval: ArrayLike) -> NDArray[np.float64]:
    times = np.asarray(t_eval, dtype=np.float64)
    if times.ndim != 1 or times.size < 2:
        raise ValueError("t_eval must be a one-dimensional array with at least two points")
    if not np.all(np.isfinite(times)) or np.any(times <= 0.0):
        raise ValueError("t_eval must contain finite, positive times")
    if np.any(np.diff(times) <= 0.0):
        raise ValueError("t_eval must be strictly increasing")
    return times


def _solve(
    *,
    system: Literal["meszaros", "comoving"],
    rhs,
    y0: NDArray[np.float64],
    t_eval: ArrayLike,
    config: SolverConfig,
) -> PerturbationSolution:
    times = _evaluation_times(t_eval)
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
        raise RuntimeError(f"{system} integration failed: {result.message}")
    return PerturbationSolution(
        system=system,
        t=np.asarray(result.t, dtype=np.float64),
        y=np.asarray(result.y, dtype=np.float64),
        config=config,
        nfev=int(result.nfev),
        njev=int(result.njev),
        nlu=int(result.nlu),
        message=str(result.message),
    )


def solve_meszaros(
    *,
    params: TrackerParams,
    initial_conditions: PerturbationInitialConditions,
    t_eval: ArrayLike,
    config: SolverConfig,
    G: float,
) -> PerturbationSolution:
    """Solve Eq. (4.27) of arXiv:2511.17160v2 with explicit numerics."""
    rhs = partial(meszaros_rhs, params=params, G=G)
    return _solve(
        system="meszaros",
        rhs=rhs,
        y0=initial_conditions.meszaros_vector(),
        t_eval=t_eval,
        config=config,
    )


def solve_comoving(
    *,
    params: TrackerParams,
    initial_conditions: PerturbationInitialConditions,
    t_eval: ArrayLike,
    config: SolverConfig,
    G: float,
) -> PerturbationSolution:
    """Solve Eqs. (4.21)-(4.23) of [GM] with explicit numerics."""
    rhs = partial(comoving_rhs, params=params, G=G)
    return _solve(
        system="comoving",
        rhs=rhs,
        y0=initial_conditions.comoving_vector(),
        t_eval=t_eval,
        config=config,
    )
