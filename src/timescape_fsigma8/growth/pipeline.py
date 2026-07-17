"""Phase 1D-B growth-pipeline orchestration and provenance output.

One pipeline run performs, in order: frozen-solver sampled integration,
dense re-integration (continuous representation), explicit reference-epoch
resolution, crossing scan + bracket-preserving refinement, maximal
validity-interval construction, signed relative growth, analytic rates,
and (when selected) the solver-harmonic delta_m coefficient mapping.

Serialization never joins logarithmic-rate arrays across a Delta_d pole:
rates are emitted as per-validity-interval segments (1D-B spec Sec. 12).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import brentq

import timescape_fsigma8.background as bg
from timescape_fsigma8.growth.crossings import (
    CrossingAnalysis,
    DenseDustSolution,
    DUST_COMPONENT,
    ValidityInterval,
    analyse_crossings,
    build_dense_solution,
    build_validity_intervals,
)
from timescape_fsigma8.growth.histories import (
    DustModeHistory,
    GrowthProvenance,
    compute_history,
)
from timescape_fsigma8.growth.mapping import (
    HarmonicMetadata,
    HarmonicSignConvention,
    map_delta_m,
    map_delta_m_dln_a_derivative,
)
from timescape_fsigma8.growth.rates import GrowthRates, evaluate_rates
from timescape_fsigma8.growth.scenarios import (
    DensityContrastMapping,
    GrowthNumericsConfig,
    GrowthReference,
    GrowthReferenceCoordinate,
    GrowthScenario,
)


def _frozen(values) -> NDArray[np.float64]:
    out = np.array(values, dtype=np.float64)
    out.flags.writeable = False
    return out


@dataclass(frozen=True)
class ResolvedGrowthReference:
    """The mandatory reference epoch resolved to every coordinate.

    The reference amplitude is evaluated on the documented dense continuous
    solution (identical frozen RHS re-integrated with ``dense_output=True``)
    and must exceed the explicit relative amplitude floor; a reference at or
    numerically indistinguishable from a crossing is rejected.
    """

    specification: GrowthReference
    t_solver_units: float
    t_gyr: float
    dressed_redshift: float
    a_D: float
    a_obs: float
    amplitude_delta_d: float
    amplitude_over_max: float

    def to_metadata(self) -> dict:
        return {
            "coordinate": self.specification.coordinate.value,
            "requested_value": self.specification.value,
            "amplitude_floor_rel": self.specification.amplitude_floor_rel,
            "t_solver_units": self.t_solver_units,
            "t_gyr": self.t_gyr,
            "dressed_redshift": self.dressed_redshift,
            "a_D": self.a_D,
            "a_obs": self.a_obs,
            "amplitude_delta_d": self.amplitude_delta_d,
            "amplitude_over_max": self.amplitude_over_max,
        }


def resolve_reference(
    *,
    history: DustModeHistory,
    dense: DenseDustSolution,
    reference: GrowthReference,
    delta_roots: tuple = (),
) -> ResolvedGrowthReference:
    """Resolve the explicit reference epoch; reject invalid references.

    A dressed-redshift reference is converted to bare solver time with the
    validated Phase 1B ``redshift`` mapping and an explicitly configured
    bracketed Brent solve on the integrated interval.  References outside
    the integrated solution are rejected.

    Zero-crossing rejection policy (explicit tolerance
    ``amplitude_floor_rel``, expressed as a fraction of the integrated
    span): the reference is rejected when (i) the dense amplitude is
    exactly zero, (ii) its linearised time distance to the nearest zero,
    |Delta_d|/|Z| (Newton estimate; exact relation Z = -dDelta_d/dt), is
    at or below ``amplitude_floor_rel`` times the integrated span, or
    (iii) any refined ``Delta_d`` root lies within that same time
    tolerance of the reference.  This makes "numerically indistinguishable
    from a zero crossing" an explicit, scale-free statement valid across
    the many-decade dynamic range of barotropic trajectories.
    """
    if not isinstance(reference, GrowthReference):
        raise ValueError("reference must be an explicit GrowthReference")
    params = history.background.params
    t_lo = float(history.t[0])
    t_hi = float(history.t[-1])
    span = t_hi - t_lo
    if reference.coordinate is GrowthReferenceCoordinate.BARE_TIME_SOLVER_UNITS:
        t_ref = float(reference.value)
        if not (t_lo <= t_ref <= t_hi):
            raise ValueError(
                f"reference time {t_ref} lies outside the integrated "
                f"solution [{t_lo}, {t_hi}]"
            )
    else:
        z_target = float(reference.value)
        z_lo = float(bg.redshift(t_hi, params))
        z_hi = float(bg.redshift(t_lo, params))
        if not (z_lo <= z_target <= z_hi):
            raise ValueError(
                f"reference dressed redshift {z_target} lies outside the "
                f"integrated solution range [{z_lo}, {z_hi}]"
            )
        t_ref = float(
            brentq(
                lambda tt: float(bg.redshift(tt, params)) - z_target,
                t_lo,
                t_hi,
                xtol=reference.root.xtol,
                rtol=reference.root.rtol,
                maxiter=reference.root.maxiter,
                disp=True,
            )
        )
    amplitude = dense.component_scalar(DUST_COMPONENT, t_ref)
    time_tolerance = reference.amplitude_floor_rel * span
    if amplitude == 0.0:
        raise ValueError(
            "reference amplitude is exactly zero: the reference sits on a "
            "Delta_d crossing"
        )
    z_at_ref = dense.component_scalar("Z", t_ref)
    if z_at_ref != 0.0:
        newton_distance = abs(amplitude) / abs(z_at_ref)
        if newton_distance <= time_tolerance:
            raise ValueError(
                f"reference amplitude {amplitude} is numerically "
                "indistinguishable from a zero crossing: linearised distance "
                f"to the nearest zero {newton_distance} <= "
                f"{reference.amplitude_floor_rel} * span {span}"
            )
    for root in delta_roots:
        if abs(t_ref - root.t_root) <= time_tolerance:
            raise ValueError(
                f"reference time {t_ref} lies within the explicit tolerance "
                f"{time_tolerance} of the refined Delta_d root {root.t_root}; "
                "choose a reference inside a validity interval"
            )
    max_amp = float(np.max(np.abs(history.delta_d)))
    return ResolvedGrowthReference(
        specification=reference,
        t_solver_units=t_ref,
        t_gyr=t_ref / history.time_unit_per_gyr,
        dressed_redshift=float(bg.redshift(t_ref, params)),
        a_D=float(bg.a_D(t_ref, params)),
        a_obs=float(bg.a_w(t_ref, params)),
        amplitude_delta_d=amplitude,
        amplitude_over_max=abs(amplitude) / max_amp,
    )


def relative_growth(
    *, history: DustModeHistory, resolved_reference: ResolvedGrowthReference
) -> NDArray[np.float64]:
    """Signed relative growth G_Delta(t;t_ref) = Delta_d(t)/Delta_d(t_ref).

    1D-A Sec. 6: no logarithm is taken; the signed ratio is well defined
    everywhere for a nonzero reference amplitude, and equals the delta_m
    relative growth G_m for the same mode because the constant harmonic
    factor cancels.
    """
    return _frozen(history.delta_d / resolved_reference.amplitude_delta_d)


@dataclass(frozen=True)
class MappedDensityContrast:
    """Optional solver-harmonic delta_m coefficient outputs (pure mapping)."""

    harmonic: HarmonicMetadata
    delta_m: NDArray[np.float64]
    d_delta_m_dln_aD: NDArray[np.float64]
    d_delta_m_dln_aobs: NDArray[np.float64]
    relative_growth: NDArray[np.float64]


@dataclass(frozen=True)
class GrowthPipelineResult:
    """Immutable complete result of one Phase 1D-B pipeline run."""

    history: DustModeHistory
    dense_nfev: int
    reference: ResolvedGrowthReference
    crossings: CrossingAnalysis
    validity_intervals: tuple[ValidityInterval, ...]
    relative_growth_delta_d: NDArray[np.float64]
    rates: GrowthRates
    mapped: MappedDensityContrast | None

    def rate_segments(self) -> list[dict]:
        """Per-validity-interval logarithmic-rate segments.

        Serialization deliberately splits at every Delta_d pole; arrays are
        never joined across a pole (1D-B spec Sec. 12).
        """
        segments = []
        for interval in self.validity_intervals:
            lo, hi = interval.sample_start_index, interval.sample_end_index
            if lo < 0:
                segments.append(
                    {"interval": interval.to_metadata(), "n_samples": 0}
                )
                continue
            sl = slice(lo, hi + 1)
            mask = self.rates.near_zero_mask[sl]
            segments.append(
                {
                    "interval": interval.to_metadata(),
                    "n_samples": int(hi - lo + 1),
                    "t_solver_units": self.history.t[sl].tolist(),
                    "f_bare": _nanlist(self.rates.f_bare[sl]),
                    "f_dressed": _nanlist(self.rates.f_dressed[sl]),
                    "near_zero_mask": mask.tolist(),
                }
            )
        return segments

    def to_json_dict(self) -> dict:
        """Machine-readable record; log-rates only as interval segments."""
        return {
            "history": self.history.to_metadata(),
            "dense_nfev": self.dense_nfev,
            "reference": self.reference.to_metadata(),
            "delta_d_roots": [r.to_metadata() for r in self.crossings.delta_d_roots],
            "z_roots": [r.to_metadata() for r in self.crossings.z_roots],
            "endpoint_roots": [
                {
                    "component": e.component,
                    "index": e.index,
                    "t": e.t,
                    "value": e.value,
                    "near_zero_floor_abs": e.near_zero_floor_abs,
                }
                for e in self.crossings.endpoint_roots
            ],
            "validity_intervals": [
                iv.to_metadata() for iv in self.validity_intervals
            ],
            "endpoint_summary": {
                "t_end_solver_units": float(self.history.t[-1]),
                "delta_d_end": float(self.history.delta_d[-1]),
                "z_end": float(self.history.z_expansion[-1]),
                "relative_growth_end": float(self.relative_growth_delta_d[-1]),
                "dDelta_d_dln_aD_end": float(self.rates.dDelta_d_dln_aD[-1]),
                "dDelta_d_dln_aobs_end": float(self.rates.dDelta_d_dln_aobs[-1]),
                "f_bare_end": _nanfloat(self.rates.f_bare[-1]),
                "f_dressed_end": _nanfloat(self.rates.f_dressed[-1]),
            },
            "rate_segments": self.rate_segments(),
            "non_logarithmic_derivatives": {
                "dDelta_d_dln_aD": self.rates.dDelta_d_dln_aD.tolist(),
                "dDelta_d_dln_aobs": self.rates.dDelta_d_dln_aobs.tolist(),
            },
            "mapped_delta_m": (
                None
                if self.mapped is None
                else {
                    "harmonic": self.mapped.harmonic.to_metadata(),
                    "endpoint_delta_m": float(self.mapped.delta_m[-1]),
                    "endpoint_relative_growth": float(
                        self.mapped.relative_growth[-1]
                    ),
                }
            ),
        }


def _nanfloat(x: float) -> float | None:
    return None if np.isnan(x) else float(x)


def _nanlist(arr: NDArray[np.float64]) -> list:
    return [None if np.isnan(v) else float(v) for v in arr]


def run_growth_pipeline(
    *,
    scenario: GrowthScenario,
    reference: GrowthReference,
    numerics: GrowthNumericsConfig,
    provenance: GrowthProvenance | None,
) -> GrowthPipelineResult:
    """Execute one fully explicit Phase 1D-B growth analysis."""
    history = compute_history(
        scenario=scenario, numerics=numerics, provenance=provenance
    )
    dense = build_dense_solution(history, numerics.dense)
    crossings = analyse_crossings(history=history, dense=dense)
    resolved_reference = resolve_reference(
        history=history,
        dense=dense,
        reference=reference,
        delta_roots=crossings.delta_d_roots,
    )
    intervals = build_validity_intervals(
        history=history,
        delta_roots=list(crossings.delta_d_roots),
        reference_time=resolved_reference.t_solver_units,
    )
    growth = relative_growth(
        history=history, resolved_reference=resolved_reference
    )
    rates = evaluate_rates(
        delta_d=history.delta_d,
        z_expansion=history.z_expansion,
        t=history.t,
        params=history.background.params,
        near_zero_rel_floor=numerics.near_zero_rel_floor,
    )
    mapped: MappedDensityContrast | None = None
    if (
        scenario.density_contrast_mapping
        is DensityContrastMapping.MAP_TO_DELTA_M_VIA_MINUS_K_CODE2
    ):
        harmonic = HarmonicMetadata(
            mode_label=str(scenario.mode_label),
            k_code=float(history.resolved_k_code),
            wavenumber_convention=scenario.wavenumber_convention,
            sign_convention=HarmonicSignConvention.NEGATIVE_LAPLACIAN_EIGENVALUE,
            k_com_D_H0TS_over_c=float(history.resolved_k_code),
            k_phys0_D_H0TS_over_c=float(history.resolved_k_code)
            / history.background.params.aD0,
        )
        delta_m = map_delta_m(history.delta_d, harmonic=harmonic)
        mapped = MappedDensityContrast(
            harmonic=harmonic,
            delta_m=delta_m,
            d_delta_m_dln_aD=map_delta_m_dln_a_derivative(
                rates.dDelta_d_dln_aD, harmonic=harmonic
            ),
            d_delta_m_dln_aobs=map_delta_m_dln_a_derivative(
                rates.dDelta_d_dln_aobs, harmonic=harmonic
            ),
            relative_growth=_frozen(
                delta_m
                / (
                    resolved_reference.amplitude_delta_d
                    / (-harmonic.k_code**2)
                )
            ),
        )
    return GrowthPipelineResult(
        history=history,
        dense_nfev=dense.nfev,
        reference=resolved_reference,
        crossings=crossings,
        validity_intervals=tuple(intervals),
        relative_growth_delta_d=growth,
        rates=rates,
        mapped=mapped,
    )
