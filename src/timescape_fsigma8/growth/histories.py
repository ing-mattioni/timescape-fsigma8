"""Dust-mode extraction and sampled growth histories (Phase 1D-B).

One explicit dust-mode representation for all three frozen perturbation
systems.  State-convention normalisation (1D-B specification Sec. 7):

* Mészáros solution:  Delta_d = y[0], Z = -y[1]  (y[1] = dDelta_d/dt;
  the sign follows Z = -dDelta_d/dt, [GM] Eq. (4.14)/(4.21));
* comoving solution:   Delta_d = y[0], Z = y[1];
* barotropic solution: Delta_d = y[0], Z = y[1].

The perturbation-system label is always explicit; nothing is inferred from
array shapes.  Arrays are immutable and the solver time unit is preserved.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

import timescape_fsigma8.background as bg
from timescape_fsigma8.perturbations import (
    PHASE1C_EPOCH_ROOT,
    PLANCK_2018_QPLUS_RECIPE,
    REGULAR_GROWING_MODE_REFERENCE_CONFIG,
    BarotropicScenario,
    CleanPerturbationSystem,
    D3Branch,
    EpochScenario,
    GrowingModeInitialConditions,
    InitialConditionScenario,
    PerturbationInitialConditions,
    RateUnitConvention,
    ResolvedEpoch,
    ResolvedWavenumber,
    TiltForm,
    WavenumberConvention,
    resolve_growing_mode_initial_conditions,
    solve_barotropic,
    solve_comoving,
    solve_meszaros,
)
from timescape_fsigma8.growth.scenarios import (
    GrowthNumericsConfig,
    GrowthScenario,
    GrowthSystem,
    GrowthD3Branch,
    GrowthTiltForm,
    GrowthWavenumberConvention,
    ResolvedBackground,
    resolve_background,
)


def _frozen_array(values) -> NDArray[np.float64]:
    out = np.array(values, dtype=np.float64)
    out.flags.writeable = False
    return out


@dataclass(frozen=True)
class GrowthProvenance:
    """Caller-supplied provenance identifying the exact validated state."""

    repository_commit: str
    upstream_commit: str
    upstream_notebook_sha256: str

    def to_metadata(self) -> dict:
        return {
            "repository_commit": self.repository_commit,
            "upstream_commit": self.upstream_commit,
            "upstream_notebook_sha256": self.upstream_notebook_sha256,
        }


def map_d3_branch(branch: GrowthD3Branch) -> D3Branch:
    """Map the growth-layer label onto the frozen Phase 1C-B2 enum."""
    if branch is GrowthD3Branch.PRINTED_4_15:
        return D3Branch.PRINTED_4_15
    if branch is GrowthD3Branch.DERIVED_4_10:
        return D3Branch.DERIVED_4_10
    raise ValueError(f"no frozen D3 branch for {branch!r}")


def map_tilt_form(tilt: GrowthTiltForm) -> TiltForm:
    if tilt is GrowthTiltForm.UNRESCALED_V:
        return TiltForm.UNRESCALED_V
    if tilt is GrowthTiltForm.RESCALED_VTILDE:
        return TiltForm.RESCALED_VTILDE
    raise ValueError(f"no frozen tilt form for {tilt!r}")


def map_wavenumber_convention(
    convention: GrowthWavenumberConvention,
) -> WavenumberConvention:
    if convention is GrowthWavenumberConvention.UPSTREAM_TIMESCAPE_K:
        return WavenumberConvention.UPSTREAM_TIMESCAPE_K
    if convention is GrowthWavenumberConvention.PAPER_LCDM_HUBBLE_K:
        return WavenumberConvention.PAPER_LCDM_HUBBLE_K
    raise ValueError(f"no frozen wavenumber convention for {convention!r}")


def extract_dust_mode(
    *,
    system: GrowthSystem,
    y: NDArray[np.float64],
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Return immutable (Delta_d, Z) for an explicit system label.

    Mészáros stores dDelta_d/dt in y[1], so Z = -y[1] there
    (Z = -dDelta_d/dt, [GM] (4.14)); the comoving and barotropic states
    store Z directly in y[1].  The system is never inferred from shape.
    """
    if not isinstance(system, GrowthSystem):
        raise ValueError("system must be an explicit GrowthSystem")
    y = np.asarray(y, dtype=np.float64)
    if y.ndim != 2 or y.shape[0] < 2:
        raise ValueError("y must be a (n_components, n_samples) state array")
    if system is GrowthSystem.MESZAROS:
        if y.shape[0] != 2:
            raise ValueError("meszaros state must have exactly 2 components")
        return _frozen_array(y[0]), _frozen_array(-y[1])
    if system is GrowthSystem.COMOVING:
        if y.shape[0] != 3:
            raise ValueError("comoving state must have exactly 3 components")
        return _frozen_array(y[0]), _frozen_array(y[1])
    if system is GrowthSystem.BAROTROPIC:
        if y.shape[0] != 4:
            raise ValueError("barotropic state must have exactly 4 components")
        return _frozen_array(y[0]), _frozen_array(y[1])
    raise ValueError(f"unsupported system: {system!r}")  # pragma: no cover


@dataclass(frozen=True)
class DustModeHistory:
    """Immutable sampled dust-mode trajectory with complete metadata.

    ``t`` is in the preset's solver time unit; ``time_unit_per_gyr`` converts
    to Gyr through the documented upstream 9.778 approximation of the
    preset's time unit (t_gyr = t / time_unit_per_gyr).
    """

    scenario: GrowthScenario
    background: ResolvedBackground
    numerics: GrowthNumericsConfig
    epoch: ResolvedEpoch
    initial_conditions: PerturbationInitialConditions
    t: NDArray[np.float64]
    delta_d: NDArray[np.float64]
    z_expansion: NDArray[np.float64]
    resolved_k_code: float | None
    resolved_wavenumber: ResolvedWavenumber | None
    solver_nfev: int
    solver_message: str
    provenance: GrowthProvenance | None

    @property
    def time_unit_per_gyr(self) -> float:
        return self.background.time_unit.target_time_per_gyr

    def t_gyr(self) -> NDArray[np.float64]:
        return _frozen_array(self.t / self.time_unit_per_gyr)

    def dressed_redshift(self) -> NDArray[np.float64]:
        return _frozen_array(bg.redshift(self.t, self.background.params))

    def _initial_conditions_metadata(self) -> dict:
        ics = self.initial_conditions
        record = {
            "delta_d": ics.delta_d,
            "expansion_gradient": ics.expansion_gradient,
            "delta_eff": ics.delta_eff,
            "rate_units": ics.rate_units.value,
        }
        if isinstance(ics, GrowingModeInitialConditions):
            record["regular_growing_mode"] = {
                "system": ics.system.value,
                "initial_time": ics.initial_time,
                "log_rate": ics.log_rate,
                "effective_ratio": ics.effective_ratio,
                "config": ics.config.to_metadata(),
            }
        return record

    def to_metadata(self) -> dict:
        return {
            "scenario": self.scenario.to_metadata(),
            "scenario_identifier": self.scenario.identifier,
            "background_preset_source": self.background.source_preset_name,
            "timescape_h": self.background.timescape_h,
            "lcdm_h": self.background.lcdm_h,
            "time_unit": self.background.time_unit.name,
            "time_unit_per_gyr": self.time_unit_per_gyr,
            "numerics": self.numerics.to_metadata(),
            "epoch": {
                "choice": self.epoch.choice.value,
                "time": self.epoch.time,
                "time_gyr": self.epoch.time_gyr,
                "dressed_redshift": self.epoch.dressed_redshift,
            },
            "initial_conditions": self._initial_conditions_metadata(),
            "integration_interval_solver_units": [float(self.t[0]), float(self.t[-1])],
            "resolved_k_code": self.resolved_k_code,
            "solver_nfev": self.solver_nfev,
            "provenance": (
                self.provenance.to_metadata() if self.provenance else None
            ),
        }


def resolve_epoch_and_ics(
    scenario: GrowthScenario, background: ResolvedBackground, *, G: float
) -> tuple[ResolvedEpoch, PerturbationInitialConditions]:
    """Resolve the frozen Phase 1C epoch and IC scenarios for this run.

    ``TIMESCAPE_REGULAR_GROWING_MODE`` (clean systems only; the scenario
    rejects barotropic use) is resolved at the resolved epoch with the named
    immutable ``REGULAR_GROWING_MODE_REFERENCE_CONFIG`` and the explicit
    ``G``; the two LCDM-rate conventions use the frozen
    ``InitialConditionScenario`` unchanged and do not use ``G``.
    """
    epoch = EpochScenario(
        choice=scenario.epoch_choice,
        time_unit=background.time_unit,
        root=PHASE1C_EPOCH_ROOT,
    ).resolve(background.params)
    if (
        scenario.rate_unit_convention
        is RateUnitConvention.TIMESCAPE_REGULAR_GROWING_MODE
    ):
        system = {
            GrowthSystem.MESZAROS: CleanPerturbationSystem.MESZAROS,
            GrowthSystem.COMOVING: CleanPerturbationSystem.COMOVING,
        }.get(scenario.perturbation_system)
        if system is None:  # pragma: no cover - GrowthScenario rejects it
            raise ValueError("the regular growing mode is defined for clean systems only")
        ics = resolve_growing_mode_initial_conditions(
            background.params,
            recipe=PLANCK_2018_QPLUS_RECIPE,
            system=system,
            epoch=epoch,
            config=REGULAR_GROWING_MODE_REFERENCE_CONFIG,
            G=G,
        )
        return epoch, ics
    ics = InitialConditionScenario(
        recipe=PLANCK_2018_QPLUS_RECIPE,
        rate_units=scenario.rate_unit_convention,
        timescape_h=background.timescape_h,
    ).resolve(background.params)
    return epoch, ics


def build_barotropic_scenario(
    scenario: GrowthScenario, background: ResolvedBackground
) -> BarotropicScenario:
    """Construct the frozen Phase 1C-B2 scenario for a barotropic run."""
    return BarotropicScenario(
        k=float(scenario.supplied_mode_k),
        branch=map_d3_branch(scenario.d3_branch),
        tilt_form=map_tilt_form(scenario.tilt_form),
        rate_convention=scenario.rate_unit_convention,
        epoch_choice=scenario.epoch_choice,
        wavenumber_convention=map_wavenumber_convention(
            scenario.wavenumber_convention
        ),
        timescape_h=background.timescape_h,
        lcdm_h=background.lcdm_h,
    )


def compute_history(
    *,
    scenario: GrowthScenario,
    numerics: GrowthNumericsConfig,
    provenance: GrowthProvenance | None,
) -> DustModeHistory:
    """Integrate the frozen system for [t_i, t0] and extract the dust mode.

    Uses the frozen Phase 1C solvers unchanged (no RHS is redefined here);
    the sampled grid is a uniform ``n_samples``-point grid on [t_i, t0] in
    solver units.
    """
    if not isinstance(scenario, GrowthScenario):
        raise ValueError("scenario must be an explicit GrowthScenario")
    if not isinstance(numerics, GrowthNumericsConfig):
        raise ValueError("numerics must be an explicit GrowthNumericsConfig")
    background = resolve_background(scenario.background_preset)
    epoch, ics = resolve_epoch_and_ics(scenario, background, G=numerics.G)
    t_eval = np.linspace(epoch.time, background.t0, numerics.n_samples)

    resolved_k_code: float | None = None
    resolved_wavenumber: ResolvedWavenumber | None = None
    if scenario.perturbation_system is GrowthSystem.BAROTROPIC:
        b2_scenario = build_barotropic_scenario(scenario, background)
        solution = solve_barotropic(
            params=background.params,
            scenario=b2_scenario,
            recipe=PLANCK_2018_QPLUS_RECIPE,
            time_unit=background.time_unit,
            epoch_root=PHASE1C_EPOCH_ROOT,
            t_eval=t_eval,
            config=numerics.solver,
            G=numerics.G,
        )
        resolved_wavenumber = solution.wavenumber
        resolved_k_code = float(solution.wavenumber.matrix_k)
        t = solution.t
        y = solution.y
        nfev, message = solution.nfev, solution.message
    else:
        solver = (
            solve_meszaros
            if scenario.perturbation_system is GrowthSystem.MESZAROS
            else solve_comoving
        )
        solution = solver(
            params=background.params,
            initial_conditions=ics,
            t_eval=t_eval,
            config=numerics.solver,
            G=numerics.G,
        )
        t = solution.t
        y = solution.y
        nfev, message = solution.nfev, solution.message
        if scenario.supplied_mode_k is not None:
            # Clean-system per-mode harmonic label: metadata only, supplied
            # directly as k_code; it never enters the dynamics.
            resolved_k_code = float(scenario.supplied_mode_k)

    delta_d, z_expansion = extract_dust_mode(
        system=scenario.perturbation_system, y=y
    )
    return DustModeHistory(
        scenario=scenario,
        background=background,
        numerics=numerics,
        epoch=epoch,
        initial_conditions=ics,
        t=_frozen_array(t),
        delta_d=delta_d,
        z_expansion=z_expansion,
        resolved_k_code=resolved_k_code,
        resolved_wavenumber=resolved_wavenumber,
        solver_nfev=nfev,
        solver_message=message,
        provenance=provenance,
    )
