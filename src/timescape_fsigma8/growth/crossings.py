"""Zero-crossing detection, dense refinement, and validity intervals.

Procedure (1D-B specification Secs. 11-12; 1D-A Sec. 8 policy):

1. scan consecutive frozen-solver samples for strict sign changes
   (y[i]*y[i+1] < 0, both samples above the explicit near-zero floor);
2. preserve the original left/right sample bracket;
3. refine each root with bracket-preserving Brent iteration on a dense
   (continuous) re-integration of the identical frozen RHS with
   ``dense_output=True`` and explicit tolerances;
4. verify the refined root lies inside the original bracket, record the
   dense-component residual at the root and the root-uncertainty
   diagnostic;
5. sampled values under the near-zero floor are flagged, never promoted to
   solver-independent roots; endpoint roots are reported separately.

The Phase 1D-A crossing locations are sampled-grid brackets only and are
never copied as roots; every refined root here is derived from the solver.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import partial

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import timescape_fsigma8.background as bg
from timescape_fsigma8.perturbations import barotropic_rhs
from timescape_fsigma8.perturbations.systems import comoving_rhs, meszaros_rhs
from timescape_fsigma8.growth.histories import (
    DustModeHistory,
    build_barotropic_scenario,
    map_d3_branch,
    map_tilt_form,
    map_wavenumber_convention,
)
from timescape_fsigma8.growth.rates import amplitude_near_zero_mask
from timescape_fsigma8.growth.scenarios import (
    DenseSolveConfig,
    GrowthSystem,
    RootRefineConfig,
)


DUST_COMPONENT = "Delta_d"
EXPANSION_COMPONENT = "Z"


@dataclass(frozen=True)
class DenseDustSolution:
    """Continuous dust-mode representation from a dense re-integration.

    Wraps ``scipy.integrate.OdeSolution`` and applies the same explicit
    state-convention normalisation as ``extract_dust_mode`` (Mészáros:
    Z = -y[1]; comoving/barotropic: Z = y[1]).
    """

    system: GrowthSystem
    interpolant: object
    t_start: float
    t_end: float
    config: DenseSolveConfig
    nfev: int

    def component(self, name: str, t) -> np.ndarray:
        state = np.atleast_2d(np.asarray(self.interpolant(t), dtype=np.float64))
        if state.ndim == 1:  # pragma: no cover - scalar t handling
            state = state[:, None]
        if name == DUST_COMPONENT:
            return state[0]
        if name == EXPANSION_COMPONENT:
            sign = -1.0 if self.system is GrowthSystem.MESZAROS else 1.0
            return sign * state[1]
        raise ValueError(f"unsupported component: {name!r}")

    def component_scalar(self, name: str, t: float) -> float:
        return float(np.asarray(self.component(name, [t]))[0])


def build_dense_solution(
    history: DustModeHistory, dense: DenseSolveConfig
) -> DenseDustSolution:
    """Dense re-integration of the identical frozen RHS for refinement.

    Uses the frozen public RHS functions (``meszaros_rhs``, ``comoving_rhs``,
    ``barotropic_rhs``) with the identical resolved initial conditions and
    interval, and explicit dense tolerances.  No frozen module is modified
    and no scientific equation is redefined; this is the controlled
    continuous representation required by the root-refinement policy.
    """
    scenario = history.scenario
    params = history.background.params
    ics = history.initial_conditions
    if scenario.perturbation_system is GrowthSystem.MESZAROS:
        rhs = partial(meszaros_rhs, params=params, G=history.numerics.G)
        y0 = ics.meszaros_vector()
    elif scenario.perturbation_system is GrowthSystem.COMOVING:
        rhs = partial(comoving_rhs, params=params, G=history.numerics.G)
        y0 = ics.comoving_vector()
    else:
        b2 = build_barotropic_scenario(scenario, history.background)
        rhs = partial(
            barotropic_rhs,
            params=params,
            G=history.numerics.G,
            k=b2.k,
            branch=map_d3_branch(scenario.d3_branch),
            tilt_form=map_tilt_form(scenario.tilt_form),
            wavenumber_convention=map_wavenumber_convention(
                scenario.wavenumber_convention
            ),
            timescape_h=b2.timescape_h,
            lcdm_h=b2.lcdm_h,
        )
        y0 = np.array(
            [ics.delta_d, ics.expansion_gradient, ics.delta_eff, 0.0],
            dtype=np.float64,
        )
    t_start = float(history.t[0])
    t_end = float(history.t[-1])
    result = solve_ivp(
        rhs,
        (t_start, t_end),
        y0,
        method=dense.method,
        dense_output=True,
        t_eval=None,
        events=None,
        vectorized=False,
        rtol=dense.rtol,
        atol=dense.atol,
        max_step=dense.max_step,
        first_step=dense.first_step,
    )
    if not result.success:
        raise RuntimeError(
            f"dense re-integration failed for {scenario.identifier}: "
            f"{result.message}"
        )
    return DenseDustSolution(
        system=scenario.perturbation_system,
        interpolant=result.sol,
        t_start=t_start,
        t_end=t_end,
        config=dense,
        nfev=int(result.nfev),
    )


@dataclass(frozen=True)
class SignChangeBracket:
    """A strict sampled sign change with its original bracket preserved."""

    component: str
    left_index: int
    right_index: int
    t_left: float
    t_right: float
    y_left: float
    y_right: float


@dataclass(frozen=True)
class EndpointRoot:
    """An integration-endpoint sample under the near-zero floor.

    Reported separately from strict interior sign changes; never refined.
    """

    component: str
    index: int
    t: float
    value: float
    near_zero_floor_abs: float


def scan_sign_changes(
    *,
    component: str,
    t: NDArray[np.float64],
    y: NDArray[np.float64],
    near_zero_rel_floor: float,
) -> tuple[list[SignChangeBracket], list[EndpointRoot], NDArray[np.bool_]]:
    """Strict sign-change scan with the explicit near-zero policy.

    Returns (interior brackets, endpoint roots, near-zero sample mask).
    A strict change requires y[i]*y[i+1] < 0, which by construction never
    involves an exactly-zero sample.  Samples flagged by the neighbour-
    local near-zero policy (``amplitude_near_zero_mask``) are reported via
    the mask and as endpoint roots when they occur at the integration
    endpoints; a sampled rounding-zero is never promoted to a
    solver-independent root by itself.
    """
    t = np.asarray(t, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    near_zero = amplitude_near_zero_mask(
        y, near_zero_rel_floor=near_zero_rel_floor
    )
    brackets: list[SignChangeBracket] = []
    for i in range(y.size - 1):
        if y[i] * y[i + 1] < 0.0:
            brackets.append(
                SignChangeBracket(
                    component=component,
                    left_index=i,
                    right_index=i + 1,
                    t_left=float(t[i]),
                    t_right=float(t[i + 1]),
                    y_left=float(y[i]),
                    y_right=float(y[i + 1]),
                )
            )
    endpoints = [
        EndpointRoot(
            component=component,
            index=int(i),
            t=float(t[i]),
            value=float(y[i]),
            near_zero_floor_abs=float(
                near_zero_rel_floor
                * max(abs(y[1] if i == 0 else y[-2]), 0.0)
            ),
        )
        for i in (0, y.size - 1)
        if near_zero[i]
    ]
    return brackets, endpoints, near_zero


@dataclass(frozen=True)
class RefinedRoot:
    """A bracket-preserving refined root with complete metadata."""

    component: str
    t_root: float
    t_root_gyr: float
    dressed_redshift: float
    a_D: float
    a_obs: float
    bracket_left: float
    bracket_right: float
    root_uncertainty: float
    residual: float
    residual_scale: float
    brentq_iterations: int
    brentq_converged: bool
    dense_config: DenseSolveConfig
    root_config: RootRefineConfig
    scenario_identifier: str

    def to_metadata(self) -> dict:
        return {
            "component": self.component,
            "t_root_solver_units": self.t_root,
            "t_root_gyr": self.t_root_gyr,
            "dressed_redshift": self.dressed_redshift,
            "a_D": self.a_D,
            "a_obs": self.a_obs,
            "bracket_solver_units": [self.bracket_left, self.bracket_right],
            "root_uncertainty_solver_units": self.root_uncertainty,
            "residual": self.residual,
            "residual_scale": self.residual_scale,
            "residual_over_scale": self.residual / self.residual_scale,
            "brentq_iterations": self.brentq_iterations,
            "brentq_converged": self.brentq_converged,
            "scenario_identifier": self.scenario_identifier,
        }


def refine_root(
    *,
    bracket: SignChangeBracket,
    dense: DenseDustSolution,
    history: DustModeHistory,
    root_config: RootRefineConfig,
) -> RefinedRoot:
    """Refine one sampled sign change on the dense continuous solution.

    Brent iteration is bracket-preserving by construction; the refined root
    is additionally verified to lie strictly inside the original sampled
    bracket, and the dense-component residual at the root is recorded and
    gated against ``residual_scale_gate`` times the bracket's larger sample
    magnitude.  The result is derived from the solver, never copied from
    any frozen sampled table.
    """
    func = lambda tt: dense.component_scalar(bracket.component, tt)
    f_left = func(bracket.t_left)
    f_right = func(bracket.t_right)
    if f_left * f_right >= 0.0:
        raise RuntimeError(
            "dense solution does not change sign inside the sampled bracket "
            f"[{bracket.t_left}, {bracket.t_right}] for {bracket.component}; "
            "sampled and dense representations disagree - investigate"
        )
    root, results = brentq(
        func,
        bracket.t_left,
        bracket.t_right,
        xtol=root_config.xtol,
        rtol=root_config.rtol,
        maxiter=root_config.maxiter,
        full_output=True,
        disp=True,
    )
    root = float(root)
    if not (bracket.t_left <= root <= bracket.t_right):
        raise RuntimeError(
            f"refined root {root} escaped its bracket "
            f"[{bracket.t_left}, {bracket.t_right}]"
        )
    residual = abs(func(root))
    scale = max(abs(bracket.y_left), abs(bracket.y_right))
    if residual > root_config.residual_scale_gate * scale:
        raise RuntimeError(
            f"root residual {residual} exceeds gate "
            f"{root_config.residual_scale_gate} * {scale}"
        )
    params = history.background.params
    uncertainty = root_config.xtol + root_config.rtol * abs(root)
    a_w0_rescaled = float(bg.a_w(root, params))
    return RefinedRoot(
        component=bracket.component,
        t_root=root,
        t_root_gyr=root / history.time_unit_per_gyr,
        dressed_redshift=float(bg.redshift(root, params)),
        a_D=float(bg.a_D(root, params)),
        a_obs=a_w0_rescaled,
        bracket_left=bracket.t_left,
        bracket_right=bracket.t_right,
        root_uncertainty=uncertainty,
        residual=residual,
        residual_scale=scale,
        brentq_iterations=int(results.iterations),
        brentq_converged=bool(results.converged),
        dense_config=dense.config,
        root_config=root_config,
        scenario_identifier=history.scenario.identifier,
    )


@dataclass(frozen=True)
class ValidityInterval:
    """One maximal interval on which the logarithmic rate is defined.

    Boundaries are the integration start/end (closed endpoints) and refined
    ``Delta_d`` roots (open endpoints); the rate is valid strictly inside
    and undefined at amplitude roots.  A ``Z`` root never splits an
    interval; it appears as a stationary point (rate zero) inside one.
    """

    start: float
    end: float
    start_open: bool
    end_open: bool
    start_gyr: float
    end_gyr: float
    start_dressed_redshift: float
    end_dressed_redshift: float
    amplitude_sign: int
    sample_start_index: int
    sample_end_index: int
    contains_reference: bool

    def to_metadata(self) -> dict:
        return {
            "start_solver_units": self.start,
            "end_solver_units": self.end,
            "start_open": self.start_open,
            "end_open": self.end_open,
            "start_gyr": self.start_gyr,
            "end_gyr": self.end_gyr,
            "start_dressed_redshift": self.start_dressed_redshift,
            "end_dressed_redshift": self.end_dressed_redshift,
            "amplitude_sign": self.amplitude_sign,
            "sample_index_range": [self.sample_start_index, self.sample_end_index],
            "contains_reference": self.contains_reference,
        }


def build_validity_intervals(
    *,
    history: DustModeHistory,
    delta_roots: list[RefinedRoot],
    reference_time: float | None,
) -> list[ValidityInterval]:
    """Construct maximal logarithmic-rate validity intervals.

    Interval boundaries: integration start, every refined ``Delta_d`` root,
    integration end.  Endpoint semantics are explicit: closed at the
    integration endpoints, open at amplitude roots.
    """
    t = history.t
    params = history.background.params
    unit = history.time_unit_per_gyr
    boundaries = (
        [float(t[0])]
        + sorted(r.t_root for r in delta_roots if r.component == DUST_COMPONENT)
        + [float(t[-1])]
    )
    intervals: list[ValidityInterval] = []
    for i in range(len(boundaries) - 1):
        lo, hi = boundaries[i], boundaries[i + 1]
        inside = (t > lo) & (t < hi)
        # include closed integration endpoints in their intervals
        if i == 0:
            inside = inside | (t == lo)
        if i == len(boundaries) - 2:
            inside = inside | (t == hi)
        idx = np.nonzero(inside)[0]
        if idx.size:
            interior = history.delta_d[idx]
            nonzero = interior[np.abs(interior) > 0.0]
            sign = int(np.sign(nonzero[np.abs(nonzero).argmax()])) if nonzero.size else 0
            sample_start, sample_end = int(idx[0]), int(idx[-1])
        else:  # pragma: no cover - sub-sample interval between close roots
            sign = 0
            sample_start, sample_end = -1, -1
        contains_ref = (
            reference_time is not None and lo < reference_time < hi
        ) or (
            reference_time is not None
            and ((i == 0 and reference_time == lo)
                 or (i == len(boundaries) - 2 and reference_time == hi))
        )
        intervals.append(
            ValidityInterval(
                start=lo,
                end=hi,
                start_open=(i != 0),
                end_open=(i != len(boundaries) - 2),
                start_gyr=lo / unit,
                end_gyr=hi / unit,
                start_dressed_redshift=float(bg.redshift(lo, params)),
                end_dressed_redshift=float(bg.redshift(hi, params)),
                amplitude_sign=sign,
                sample_start_index=sample_start,
                sample_end_index=sample_end,
                contains_reference=bool(contains_ref),
            )
        )
    return intervals


@dataclass(frozen=True)
class CrossingAnalysis:
    """Complete crossing record of one history."""

    delta_d_brackets: tuple[SignChangeBracket, ...]
    z_brackets: tuple[SignChangeBracket, ...]
    delta_d_roots: tuple[RefinedRoot, ...]
    z_roots: tuple[RefinedRoot, ...]
    endpoint_roots: tuple[EndpointRoot, ...]
    delta_d_near_zero_mask: NDArray[np.bool_]
    z_near_zero_mask: NDArray[np.bool_]


def analyse_crossings(
    *, history: DustModeHistory, dense: DenseDustSolution
) -> CrossingAnalysis:
    """Scan and refine every strict Delta_d and Z sign change."""
    numerics = history.numerics
    d_brackets, d_endpoints, d_mask = scan_sign_changes(
        component=DUST_COMPONENT,
        t=history.t,
        y=history.delta_d,
        near_zero_rel_floor=numerics.near_zero_rel_floor,
    )
    z_brackets, z_endpoints, z_mask = scan_sign_changes(
        component=EXPANSION_COMPONENT,
        t=history.t,
        y=history.z_expansion,
        near_zero_rel_floor=numerics.near_zero_rel_floor,
    )
    d_roots = tuple(
        refine_root(
            bracket=b, dense=dense, history=history, root_config=numerics.root
        )
        for b in d_brackets
    )
    z_roots = tuple(
        refine_root(
            bracket=b, dense=dense, history=history, root_config=numerics.root
        )
        for b in z_brackets
    )
    return CrossingAnalysis(
        delta_d_brackets=tuple(d_brackets),
        z_brackets=tuple(z_brackets),
        delta_d_roots=d_roots,
        z_roots=z_roots,
        endpoint_roots=tuple(d_endpoints + z_endpoints),
        delta_d_near_zero_mask=d_mask,
        z_near_zero_mask=z_mask,
    )
