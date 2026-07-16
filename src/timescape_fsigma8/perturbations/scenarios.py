"""Explicit initial-epoch and time-unit scenarios for Phase 1C-B1."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from scipy.optimize import brentq

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams


class EpochChoice(str, Enum):
    """Mandatory choice between the two unresolved initial epochs."""

    UPSTREAM_0P218_GYR = "upstream_0p218_gyr"
    DRESSED_Z20 = "dressed_z20"


@dataclass(frozen=True)
class TimeUnit:
    """Mapping between physical Gyr and the time variable used by an RHS."""

    name: str
    target_time_per_gyr: float

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("time-unit name must be nonempty")
        if self.target_time_per_gyr <= 0.0:
            raise ValueError("target_time_per_gyr must be positive")


@dataclass(frozen=True)
class EpochRootConfig:
    """Fully explicit Brent root-finder controls for the dressed-z epoch."""

    xtol: float
    rtol: float
    maxiter: int
    lower_t0_fraction: float

    def __post_init__(self) -> None:
        if self.xtol <= 0.0 or self.rtol <= 0.0:
            raise ValueError("root tolerances must be positive")
        if self.maxiter <= 0:
            raise ValueError("maxiter must be positive")
        if not 0.0 < self.lower_t0_fraction < 1.0:
            raise ValueError("lower_t0_fraction must lie in (0, 1)")


@dataclass(frozen=True)
class ResolvedEpoch:
    """An epoch expressed in both the RHS time unit and physical Gyr."""

    choice: EpochChoice
    time: float
    time_gyr: float
    dressed_redshift: float
    time_unit: TimeUnit


# Upstream cell 2 uses t_code = t_Gyr * h/9.778 with h=0.7323.  This
# reproduction-only approximation is explicitly distinct from the exact IAU
# conversion in timescape_fsigma8.units.
UPSTREAM_NOTEBOOK_TIME_UNIT = TimeUnit(
    name="upstream H0=1 code time (h=0.7323; 9.778 Gyr approximation)",
    target_time_per_gyr=0.7323 / 9.778,
)

GYR_TIME_UNIT = TimeUnit(name="Gyr", target_time_per_gyr=1.0)

# scipy.optimize.brentq controls. rtol is just above the documented minimum
# 4*machine-epsilon; no library default is relied upon.
PHASE1C_EPOCH_ROOT = EpochRootConfig(
    xtol=1e-14,
    rtol=8.9e-16,
    maxiter=100,
    lower_t0_fraction=1e-10,
)


@dataclass(frozen=True)
class EpochScenario:
    """Mandatory epoch choice with explicit unit and root controls."""

    choice: EpochChoice
    time_unit: TimeUnit
    root: EpochRootConfig

    def resolve(self, params: TrackerParams) -> ResolvedEpoch:
        """Resolve the selected initial epoch.

        ``DRESSED_Z20`` solves the dressed redshift relation, Eq. (38) of
        Wiltshire, arXiv:0909.0749 (implemented by Phase 1B ``redshift``).
        ``UPSTREAM_0P218_GYR`` reproduces the unexplained notebook cell-15
        epoch and is explicitly not claimed to represent z=20.
        """
        if self.choice is EpochChoice.UPSTREAM_0P218_GYR:
            time = 0.218 * self.time_unit.target_time_per_gyr
        elif self.choice is EpochChoice.DRESSED_Z20:
            lower = self.root.lower_t0_fraction * params.t0
            time = brentq(
                lambda t: float(bg.redshift(t, params)) - 20.0,
                lower,
                params.t0,
                xtol=self.root.xtol,
                rtol=self.root.rtol,
                maxiter=self.root.maxiter,
                disp=True,
            )
        else:  # defensive against non-Enum construction
            raise ValueError(f"unsupported epoch choice: {self.choice!r}")
        return ResolvedEpoch(
            choice=self.choice,
            time=float(time),
            time_gyr=float(time / self.time_unit.target_time_per_gyr),
            dressed_redshift=float(bg.redshift(time, params)),
            time_unit=self.time_unit,
        )
