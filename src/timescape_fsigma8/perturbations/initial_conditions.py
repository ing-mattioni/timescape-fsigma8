"""Planck-2018 growing-mode initial conditions for Phase 1C-B1.

The recipe reconstructs the two 17-digit values used in the pinned upstream
notebook while making the unresolved expansion-gradient unit choice explicit.
No option has a scientific default.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np
from numpy.typing import NDArray
from scipy import special

from timescape_fsigma8.background import TrackerParams


class RateUnitConvention(str, Enum):
    """Mandatory convention for the dimensionful initial ``Z`` value.

    ``UPSTREAM_UNCONVERTED`` reproduces the notebook's unchanged numerical
    injection. ``LCDM_TO_TIMESCAPE_CONVERTED`` converts the rate from the
    Planck-2018 H0 unit (h=0.674) to the Timescape H0 unit (h=0.7323).
    """

    UPSTREAM_UNCONVERTED = "upstream_unconverted"
    LCDM_TO_TIMESCAPE_CONVERTED = "lcdm_to_timescape_converted"


@dataclass(frozen=True)
class LCDMGrowthRecipe:
    """All numerical choices entering the flat-LCDM growing-mode recipe."""

    omega_m: float
    omega_lambda: float
    h: float
    cmb_factor: float
    initial_redshift: float
    finite_difference_epsilon: float

    def __post_init__(self) -> None:
        if self.omega_m <= 0.0 or self.omega_lambda <= 0.0:
            raise ValueError("omega_m and omega_lambda must be positive")
        if not np.isclose(self.omega_m + self.omega_lambda, 1.0, rtol=0.0, atol=1e-15):
            raise ValueError("the qplus recipe requires flat LCDM: omega_m + omega_lambda = 1")
        if self.h <= 0.0 or self.cmb_factor <= 0.0:
            raise ValueError("h and cmb_factor must be positive")
        if self.initial_redshift < 0.0 or self.finite_difference_epsilon <= 0.0:
            raise ValueError("initial_redshift must be nonnegative and epsilon positive")


# Planck-2018 parameters and numerical choices established in the Phase 1C-A
# audit. The value is named, immutable, and must still be passed explicitly to
# InitialConditionScenario; it is not a function default.
PLANCK_2018_QPLUS_RECIPE = LCDMGrowthRecipe(
    omega_m=0.315,
    omega_lambda=1.0 - 0.315,
    h=0.674,
    cmb_factor=6.6e-2,
    initial_redshift=20.0,
    finite_difference_epsilon=1e-5,
)


def qplus(z: float, recipe: LCDMGrowthRecipe) -> np.float64:
    """Return the flat-LCDM growing mode used for the initial amplitude.

    Independently obtained by reduction of order of the growth equation,
    Eq. (3) of Short & Coles, arXiv:astro-ph/0605013v2:
    ``D=(5/2) Omega_m E(a) integral_0^a dx/[x^3 E(x)^3]``, ``D/a -> 1``.
    Substituting ``x_beta=Omega_L a^3/(Omega_m+Omega_L a^3)`` gives the
    implemented incomplete beta with indices (5/6, 2/3).
    This is NOT a literal transcription of printed Eqs. (11)-(12): their
    cube-root prefactor contains an extra a^-1, their square root contains
    a^-6 instead of a^-3, and their beta denominator uses a^6 instead of
    a^3. They also normalize at an initial epoch rather than D/a -> 1.
    See the Phase 1F-C-R successor report for the independent derivation.
    It is evaluated with the explicitly supplied Planck-2018 parameters,
    as described for the dust IC construction in Sec. 5.1.2 of
    arXiv:2511.17160v2.
    """
    if z < 0.0:
        raise ValueError(f"qplus requires z >= 0, got {z}")
    u = (1.0 + z) ** -3
    x = recipe.omega_lambda * u / (recipe.omega_m + recipe.omega_lambda * u)
    const = (5.0 / 6.0) * ((recipe.omega_m / recipe.omega_lambda) ** (1.0 / 3.0))
    incomplete_beta = special.beta(5.0 / 6.0, 2.0 / 3.0) * special.betainc(
        5.0 / 6.0, 2.0 / 3.0, x
    )
    factor = np.sqrt(1.0 + recipe.omega_m / (recipe.omega_lambda * u))
    return np.float64(const * incomplete_beta * factor)


def qplus_prime(z: float, recipe: LCDMGrowthRecipe) -> np.float64:
    """Return the explicitly forward-differenced ``dqplus/dz``.

    The growing mode is the independently derived solution of Short &
    Coles Eq. (3), arXiv:astro-ph/0605013v2; see qplus for the printed
    formula discrepancy. The forward step is intentionally the audited
    ``epsilon=1e-5`` recipe used to generate the published/upstream IC; it
    is not a derivative used by the perturbation solver.
    """
    epsilon = recipe.finite_difference_epsilon
    return np.float64((qplus(z + epsilon, recipe) - qplus(z, recipe)) / epsilon)


def lcdm_hubble_normalized(z: float, recipe: LCDMGrowthRecipe) -> np.float64:
    """Return ``H(z)/H0`` for the explicitly flat LCDM recipe.

    This is Eq. (14) of Hogg, arXiv:astro-ph/9905116, specialised to
    ``Omega_k=0`` and a cosmological constant.
    """
    if z < 0.0:
        raise ValueError(f"LCDM H(z) requires z >= 0, got {z}")
    return np.float64(
        np.sqrt(recipe.omega_lambda + recipe.omega_m * (1.0 + z) ** 3)
    )


def qplus_dot(z: float, recipe: LCDMGrowthRecipe) -> np.float64:
    """Return ``dqplus/dt`` in units where the recipe's LCDM ``H0=1``.

    Uses ``dz/dt = -(1+z)H(z)`` with Hogg's Eq. (14)
    (arXiv:astro-ph/9905116) and the independently derived growing mode
    described in qplus. The sign of the resulting IC
    is fixed by ``Z=-dDelta_d/dt``, Eq. (4.21) of arXiv:2511.17160v2.
    """
    dz_dt = -(1.0 + z) * lcdm_hubble_normalized(z, recipe)
    return np.float64(qplus_prime(z, recipe) * dz_dt)


@dataclass(frozen=True)
class PerturbationInitialConditions:
    """Resolved ``(Delta_d, Z, Delta_eff)`` in the background time unit."""

    delta_d: float
    expansion_gradient: float
    delta_eff: float
    rate_units: RateUnitConvention

    def comoving_vector(self) -> NDArray[np.float64]:
        """Return the state ordering of Eqs. (4.21)-(4.23) of [GM]."""
        return np.array(
            [self.delta_d, self.expansion_gradient, self.delta_eff], dtype=np.float64
        )

    def meszaros_vector(self) -> NDArray[np.float64]:
        """Return ``(Delta_d, dDelta_d/dt)`` for Eq. (4.27) of [GM].

        The sign flip follows ``Z=-dDelta_d/dt``, Eq. (4.21).
        """
        return np.array([self.delta_d, -self.expansion_gradient], dtype=np.float64)


@dataclass(frozen=True)
class InitialConditionScenario:
    """Mandatory, explicit initial-condition interpretation.

    ``params.H0_dressed`` supplies the inverse unit of the target time
    variable. ``timescape_h`` identifies the physical Timescape Hubble
    normalisation used when the LCDM rate is converted.
    """

    recipe: LCDMGrowthRecipe
    rate_units: RateUnitConvention
    timescape_h: float

    def __post_init__(self) -> None:
        if self.timescape_h <= 0.0:
            raise ValueError("timescape_h must be positive")

    def resolve(self, params: TrackerParams) -> PerturbationInitialConditions:
        """Construct the ICs described in Sec. 5.1.2 of [GM].

        The dust/expansion sign relation is Eq. (4.21) of
        arXiv:2511.17160v2.  ``Delta_eff(t_i)=0`` is the explicit
        Timescape prescription in [GM] Sec. 5.1.2.
        """
        z = self.recipe.initial_redshift
        delta_d = self.recipe.cmb_factor * qplus(z, self.recipe)
        z_lcdm_h0_units = -self.recipe.cmb_factor * qplus_dot(z, self.recipe)
        if self.rate_units is RateUnitConvention.UPSTREAM_UNCONVERTED:
            rate_factor = 1.0
        elif self.rate_units is RateUnitConvention.LCDM_TO_TIMESCAPE_CONVERTED:
            rate_factor = self.recipe.h / self.timescape_h
        else:  # defensive against non-Enum construction
            raise ValueError(f"unsupported rate-unit convention: {self.rate_units!r}")
        expansion_gradient = z_lcdm_h0_units * rate_factor * params.H0_dressed
        return PerturbationInitialConditions(
            delta_d=float(delta_d),
            expansion_gradient=float(expansion_gradient),
            delta_eff=0.0,
            rate_units=self.rate_units,
        )
