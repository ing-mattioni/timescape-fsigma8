"""Regular (growing-mode) initial conditions for the clean Timescape systems.

Motivation: post-remediation review finding F1
(reports/phase1f_c_r_post_remediation_independent_audit.md).  The paper's
initial rate ``Z(t_i)`` is the flat-LCDM growing-mode rate at z=20, which is
not the growing mode of the Timescape tracker background at ``t_i``; it
excites the decaying solution.  This module supplies the explicit,
non-default alternative ``RateUnitConvention.TIMESCAPE_REGULAR_GROWING_MODE``
for the two scale-independent systems:

* Mészáros, Eq. (4.27) of arXiv:2511.17160v2 ([GM]);
* comoving closure, [GM] Eqs. (4.20)-(4.23).

References use [GM] for Galoppo & Mourier, JCAP 02 (2026) 066.

Derivation (logarithmic-rate form of the frozen systems).  Write
``s = ln t`` and define, along a solution with ``Delta_d != 0``,

    u := t dln(Delta_d)/dt = -t Z/Delta_d      (Z = -dDelta_d/dt, [GM] (4.21))
    q := Delta_eff/Delta_d                     (comoving only)

with the dimensionless background coefficients

    T := t Theta,  A := t^2 4 pi G rho_d,  B := t^2 4 pi G rho_eff,  w := w_eff,

evaluated from the same frozen Phase 1B functions that the RHS of
``systems.py`` uses.  Substituting [GM] (4.21)-(4.23) gives

    du/ds = u - u^2 - (2/3) T u + A + B q,
    dq/ds = (1 + w) u + w T q - q u,

and [GM] (4.27) gives the Mészáros equation ``du/ds = u - u^2 - (2/3) T u
+ A`` (there ``u = t dln(Delta_d)/dt`` with ``Delta_d`` the Mészáros
variable).  In the Einstein-de Sitter limit of the tracker (``f_v -> 0``:
``T -> 2``, ``A -> 2/3``, ``B -> 0``, ``w -> -1/2``) the fixed point with
``u > 0`` is ``u* = 2/3`` (``Delta_d ~ t^(2/3)``) and ``q* = (1+w)u*/(u* -
w T) = 1/5``.  The linearisation there has the double eigenvalue ``-5/3`` in
``s``, i.e. every deviation from the regular solution decays as
``t^(-5/3)`` relative to it (the decaying dust mode and the homogeneous
``Delta_eff`` mode).  Integrating forward in ``s`` from that fixed point at
an early start time therefore converges to the unique regular (growing)
solution; an ``O(epsilon)`` start offset is damped by
``(t_start/t)^(5/3)``.

The regular solution is scale-independent, and so are the resulting ICs.  The
barotropic closure is deliberately excluded: its early-time solution depends on
``k`` and on the D3 branch, and with the negative corrected ``c^2_s,eff`` the
system has an exponentially growing gradient mode, so a regular growing
mode of the tracker is not a unique object there.  Selecting one would be
new modelling, which this module does not introduce.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.integrate import solve_ivp

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations.initial_conditions import (
    LCDMGrowthRecipe,
    PerturbationInitialConditions,
    RateUnitConvention,
    qplus,
)
from timescape_fsigma8.perturbations.scenarios import ResolvedEpoch


class CleanPerturbationSystem(str, Enum):
    """Mandatory choice of the clean system whose growing mode is used."""

    MESZAROS = "meszaros"
    COMOVING = "comoving"


# Einstein-de Sitter fixed point of the logarithmic-rate system (module
# docstring): u* = 2/3 is the positive root of u^2 + u/3 - 2/3 = 0 and
# q* = (1+w)u*/(u* - w T) with w = -1/2, T = 2.
EDS_GROWING_LOG_RATE = 2.0 / 3.0
EDS_COMOVING_EFFECTIVE_RATIO = 1.0 / 5.0

# EdS-limit values of the dimensionless coefficients T, A, B, w.
_EDS_T = 2.0
_EDS_A = 2.0 / 3.0
_EDS_B = 0.0
_EDS_W = -0.5

_METHODS = {"DOP853", "Radau", "RK45"}


@dataclass(frozen=True)
class GrowingModeConfig:
    """Explicit numerics of the regular-solution integration.

    ``start_fraction``: the integration starts at
    ``t_start = start_fraction * min(requested times)`` from the EdS fixed
    point; the start offset is damped by ``start_fraction^(5/3)``.
    ``eds_limit_tolerance``: maximum admitted deviation of each of ``T``,
    ``A``, ``B`` and ``w`` from its EdS limit at ``t_start``; a larger
    deviation fails closed rather than starting from an invalid fixed point.
    ``method``/``rtol``/``atol``: the ``solve_ivp`` controls for the
    ``O(1)`` variables ``u`` and ``q``.  No field has a default.
    """

    start_fraction: float
    eds_limit_tolerance: float
    method: str
    rtol: float
    atol: float

    def __post_init__(self) -> None:
        if not (np.isfinite(self.start_fraction) and 0.0 < self.start_fraction < 1.0):
            raise ValueError("start_fraction must lie in (0, 1)")
        if not (np.isfinite(self.eds_limit_tolerance) and self.eds_limit_tolerance > 0.0):
            raise ValueError("eds_limit_tolerance must be finite and positive")
        if self.method not in _METHODS:
            raise ValueError(f"unsupported method: {self.method!r}")
        for name in ("rtol", "atol"):
            value = getattr(self, name)
            if not (np.isfinite(value) and value > 0.0):
                raise ValueError(f"{name} must be finite and positive")

    def to_metadata(self) -> dict:
        return {
            "start_fraction": self.start_fraction,
            "eds_limit_tolerance": self.eds_limit_tolerance,
            "method": self.method,
            "rtol": self.rtol,
            "atol": self.atol,
        }


# Named, immutable reference configuration (explicitly passed; not a
# function default).  start_fraction=1e-6 damps the start offset by
# (1e-6)^(5/3) ~ 1e-10; the validation report records the convergence study.
REGULAR_GROWING_MODE_REFERENCE_CONFIG = GrowingModeConfig(
    start_fraction=1e-6,
    eds_limit_tolerance=1e-5,
    method="DOP853",
    rtol=1e-12,
    atol=1e-14,
)


def _require_system(system) -> CleanPerturbationSystem:
    if not isinstance(system, CleanPerturbationSystem):
        raise ValueError(
            "system must be an explicit CleanPerturbationSystem; the barotropic "
            "closure has no regular growing mode in this module"
        )
    return system


def _coefficients(t: float, params: TrackerParams, G: float) -> tuple[float, float, float, float]:
    """Return ``(T, A, B, w)`` from the frozen Phase 1B background.

    ``T = t Theta`` ([GM] Eq. (3.6)), ``A = t^2 4 pi G rho_d`` and
    ``B = t^2 4 pi G rho_eff`` ([GM] Eqs. (3.12), (3.16)), and
    ``w = w_eff``: the coefficients of [GM] (4.21)-(4.23) and (4.27).
    """
    four_pi_G = 4.0 * np.pi * G
    return (
        t * float(bg.Theta(t, params)),
        t * t * four_pi_G * float(bg.rho_d(t, params, G)),
        t * t * four_pi_G * float(bg.rho_eff(t, params, G)),
        float(bg.w_eff(t, params)),
    )


def _meszaros_rhs(s: float, y, params: TrackerParams, G: float) -> list[float]:
    """Logarithmic-rate form of [GM] Eq. (4.27): ``du/ds``."""
    T, A, _, _ = _coefficients(float(np.exp(s)), params, G)
    u = y[0]
    return [u - u * u - (2.0 / 3.0) * T * u + A]


def _comoving_rhs(s: float, y, params: TrackerParams, G: float) -> list[float]:
    """Logarithmic-rate form of [GM] Eqs. (4.21)-(4.23): ``(du/ds, dq/ds)``."""
    T, A, B, w = _coefficients(float(np.exp(s)), params, G)
    u, q = y
    return [
        u - u * u - (2.0 / 3.0) * T * u + A + B * q,
        (1.0 + w) * u + w * T * q - q * u,
    ]


@dataclass(frozen=True)
class RegularGrowingModeCoefficients:
    """The regular solution's ``u = t dlnDelta_d/dt`` and ``q = Delta_eff/Delta_d``.

    ``effective_ratio`` is ``None`` for the Mészáros system, whose state has
    no ``Delta_eff``.  ``eds_limit_deviation`` is the largest deviation of
    ``T``, ``A``, ``B``, ``w`` from their EdS limits at ``start_time``.
    """

    system: CleanPerturbationSystem
    times: NDArray[np.float64]
    log_rate: NDArray[np.float64]
    effective_ratio: NDArray[np.float64] | None
    start_time: float
    eds_limit_deviation: float
    nfev: int
    config: GrowingModeConfig


def _readonly(values) -> NDArray[np.float64]:
    out = np.array(values, dtype=np.float64)
    out.flags.writeable = False
    return out


def regular_growing_mode_coefficients(
    params: TrackerParams,
    *,
    system: CleanPerturbationSystem,
    times: ArrayLike,
    config: GrowingModeConfig,
    G: float,
) -> RegularGrowingModeCoefficients:
    """Integrate the logarithmic-rate system from the EdS fixed point.

    Implements the logarithmic-rate form (module docstring) of [GM] Eq.
    (4.27) (Mészáros) or Eqs. (4.21)-(4.23) (comoving), on the frozen Phase
    1B tracker background.  ``times`` must be finite, positive and strictly
    increasing, in the unit of ``1/params.HD0``.
    """
    system = _require_system(system)
    if not isinstance(config, GrowingModeConfig):
        raise ValueError("config must be an explicit GrowingModeConfig")
    if not (np.isfinite(G) and G > 0.0):
        raise ValueError("G must be finite and positive")
    requested = np.asarray(times, dtype=np.float64)
    if requested.ndim != 1 or requested.size < 1:
        raise ValueError("times must be a nonempty one-dimensional array")
    if not np.all(np.isfinite(requested)) or np.any(requested <= 0.0):
        raise ValueError("times must be finite and positive")
    if np.any(np.diff(requested) <= 0.0):
        raise ValueError("times must be strictly increasing")

    start_time = config.start_fraction * float(requested[0])
    T, A, B, w = _coefficients(start_time, params, G)
    deviations = [abs(T - _EDS_T), abs(A - _EDS_A)]
    if system is CleanPerturbationSystem.COMOVING:
        deviations += [abs(B - _EDS_B), abs(w - _EDS_W)]
    eds_deviation = max(deviations)
    if eds_deviation > config.eds_limit_tolerance:
        raise ValueError(
            f"start time {start_time} is not in the EdS regime: coefficient "
            f"deviation {eds_deviation} exceeds {config.eds_limit_tolerance}"
        )

    if system is CleanPerturbationSystem.MESZAROS:
        rhs, y0 = _meszaros_rhs, [EDS_GROWING_LOG_RATE]
    else:
        rhs, y0 = _comoving_rhs, [EDS_GROWING_LOG_RATE, EDS_COMOVING_EFFECTIVE_RATIO]
    s_eval = np.log(requested)
    result = solve_ivp(
        rhs,
        (float(np.log(start_time)), float(s_eval[-1])),
        y0,
        method=config.method,
        t_eval=s_eval,
        dense_output=False,
        events=None,
        vectorized=False,
        args=(params, G),
        rtol=config.rtol,
        atol=config.atol,
        max_step=np.inf,
        first_step=None,
    )
    if not result.success:
        raise RuntimeError(f"regular growing-mode integration failed: {result.message}")
    return RegularGrowingModeCoefficients(
        system=system,
        times=_readonly(requested),
        log_rate=_readonly(result.y[0]),
        effective_ratio=(
            _readonly(result.y[1]) if system is CleanPerturbationSystem.COMOVING else None
        ),
        start_time=float(start_time),
        eds_limit_deviation=float(eds_deviation),
        nfev=int(result.nfev),
        config=config,
    )


@dataclass(frozen=True)
class GrowingModeInitialConditions(PerturbationInitialConditions):
    """Initial conditions on the regular growing solution of one clean system.

    ``delta_d`` is the unchanged recipe amplitude, bit-identical to the
    legacy conventions, so conventions differ only in ``Z`` and
    ``Delta_eff``.  The record is bound to its system and its initial time:
    the state vector of the other clean system is refused, and integration
    must start at ``initial_time`` (the growth layer does so).  For the
    Mészáros system ``delta_eff`` is ``0.0`` only because the field is
    required; it is not part of the Mészáros state and is never used.
    """

    system: CleanPerturbationSystem
    initial_time: float
    log_rate: float
    effective_ratio: float | None
    config: GrowingModeConfig

    def comoving_vector(self) -> NDArray[np.float64]:
        if self.system is not CleanPerturbationSystem.COMOVING:
            raise ValueError(
                "these growing-mode ICs belong to the Mészáros system; the "
                "comoving growing mode differs (Delta_eff feeds back on Z)"
            )
        return super().comoving_vector()

    def meszaros_vector(self) -> NDArray[np.float64]:
        if self.system is not CleanPerturbationSystem.MESZAROS:
            raise ValueError(
                "these growing-mode ICs belong to the comoving system; use "
                "system=MESZAROS for the Mészáros growing mode"
            )
        return super().meszaros_vector()


def resolve_growing_mode_initial_conditions(
    params: TrackerParams,
    *,
    recipe: LCDMGrowthRecipe,
    system: CleanPerturbationSystem,
    epoch: ResolvedEpoch,
    config: GrowingModeConfig,
    G: float,
) -> GrowingModeInitialConditions:
    """Resolve ``RateUnitConvention.TIMESCAPE_REGULAR_GROWING_MODE``.

    ``Delta_d(t_i) = cmb_factor * qplus(initial_redshift)`` (the unchanged
    [GM] Sec. 5.1.2 amplitude recipe), ``Z(t_i) = -(u(t_i)/t_i) Delta_d(t_i)``
    from ``Z = -dDelta_d/dt`` ([GM] Eq. (4.21)), and, for the comoving
    system, ``Delta_eff(t_i) = q(t_i) Delta_d(t_i)`` on the regular solution
    of [GM] (4.22) instead of the paper's ``Delta_eff(t_i) = 0``.
    """
    system = _require_system(system)
    if not isinstance(recipe, LCDMGrowthRecipe):
        raise ValueError("recipe must be an explicit LCDMGrowthRecipe")
    if not isinstance(epoch, ResolvedEpoch):
        raise ValueError("epoch must be an explicit ResolvedEpoch")
    t_i = float(epoch.time)
    coefficients = regular_growing_mode_coefficients(
        params, system=system, times=[t_i], config=config, G=G
    )
    u = float(coefficients.log_rate[0])
    delta_d = float(recipe.cmb_factor * qplus(recipe.initial_redshift, recipe))
    if system is CleanPerturbationSystem.COMOVING:
        q = float(coefficients.effective_ratio[0])
        delta_eff = q * delta_d
    else:
        q = None
        delta_eff = 0.0
    return GrowingModeInitialConditions(
        delta_d=delta_d,
        expansion_gradient=-(u / t_i) * delta_d,
        delta_eff=delta_eff,
        rate_units=RateUnitConvention.TIMESCAPE_REGULAR_GROWING_MODE,
        system=system,
        initial_time=t_i,
        log_rate=u,
        effective_ratio=q,
        config=config,
    )
