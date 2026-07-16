"""Clean Timescape perturbation systems implemented in Phase 1C-B1.

This package deliberately contains only the D2-free and D3-free systems:

* the effective Mészáros approximation, Eq. (4.27) of arXiv:2511.17160;
* the comoving effective-fluid closure, Eqs. (4.20)-(4.23) of the same paper.

The barotropic closure, the D2-corrupted upstream sound speed, the unresolved
D3 branch, f-sigma-8 observables, and likelihoods are outside this package's
scope.  The validated Phase 1B background is consumed read-only.
"""

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
