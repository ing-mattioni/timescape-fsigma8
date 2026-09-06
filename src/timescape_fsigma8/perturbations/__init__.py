"""Independently implemented Timescape perturbation systems.

The package contains the validated Phase 1C-B1 clean systems:

* the effective Mészáros approximation, Eq. (4.27) of arXiv:2511.17160;
* the comoving effective-fluid closure, Eqs. (4.20)-(4.23) of the same paper.

Phase 1C-B2 adds the barotropic closure, Eqs. (4.13)-(4.17), with both
derived and forensic D3 equation branches and both tilt variables explicit.
The accepted scientific adjudication is RESOLVED_DERIVED_4_10.
Only the corrected Phase 1B sound speed is available here.  The upstream D2
defect remains isolated in a non-exported forensic script.  F-sigma-8,
normalisation, likelihoods, and parameter fitting remain outside scope.
"""

from timescape_fsigma8.perturbations.barotropic import (
    D3Branch,
    ResolvedWavenumber,
    TiltForm,
    WavenumberConvention,
    barotropic_matrix,
    barotropic_rhs,
    resolve_wavenumber,
    tilt_state_transform,
    tilt_state_transform_dot,
    transform_barotropic_state,
)
from timescape_fsigma8.perturbations.barotropic_solver import (
    BarotropicScenario,
    BarotropicSolution,
    solve_barotropic,
)

from timescape_fsigma8.perturbations.initial_conditions import (
    PLANCK_2018_QPLUS_RECIPE,
    InitialConditionScenario,
    LCDMGrowthRecipe,
    PerturbationInitialConditions,
    RateUnitConvention,
    lcdm_hubble_normalized,
    qplus,
    qplus_dot,
    qplus_prime,
)
from timescape_fsigma8.perturbations.scenarios import (
    GYR_TIME_UNIT,
    PHASE1C_EPOCH_ROOT,
    UPSTREAM_NOTEBOOK_TIME_UNIT,
    EpochChoice,
    EpochRootConfig,
    EpochScenario,
    ResolvedEpoch,
    TimeUnit,
)
from timescape_fsigma8.perturbations.solver import (
    TIGHT_DOP853,
    TIGHT_RADAU,
    TIGHT_RK45,
    UPSTREAM_RK45_DEFAULTS,
    PerturbationSolution,
    SolverConfig,
    solve_comoving,
    solve_meszaros,
)
from timescape_fsigma8.perturbations.residuals import (
    ComovingResiduals,
    comoving_second_derivative,
    comoving_second_order_residuals,
)
from timescape_fsigma8.perturbations.systems import (
    comoving_matrix,
    comoving_rhs,
    meszaros_rhs,
)

__all__ = [
    "D3Branch",
    "ResolvedWavenumber",
    "TiltForm",
    "WavenumberConvention",
    "barotropic_matrix",
    "barotropic_rhs",
    "resolve_wavenumber",
    "tilt_state_transform",
    "tilt_state_transform_dot",
    "transform_barotropic_state",
    "BarotropicScenario",
    "BarotropicSolution",
    "solve_barotropic",
    "PLANCK_2018_QPLUS_RECIPE",
    "InitialConditionScenario",
    "LCDMGrowthRecipe",
    "PerturbationInitialConditions",
    "RateUnitConvention",
    "lcdm_hubble_normalized",
    "qplus",
    "qplus_dot",
    "qplus_prime",
    "GYR_TIME_UNIT",
    "PHASE1C_EPOCH_ROOT",
    "UPSTREAM_NOTEBOOK_TIME_UNIT",
    "EpochChoice",
    "EpochRootConfig",
    "EpochScenario",
    "ResolvedEpoch",
    "TimeUnit",
    "TIGHT_DOP853",
    "TIGHT_RADAU",
    "TIGHT_RK45",
    "UPSTREAM_RK45_DEFAULTS",
    "PerturbationSolution",
    "SolverConfig",
    "solve_comoving",
    "solve_meszaros",
    "ComovingResiduals",
    "comoving_second_derivative",
    "comoving_second_order_residuals",
    "comoving_matrix",
    "comoving_rhs",
    "meszaros_rhs",
]
