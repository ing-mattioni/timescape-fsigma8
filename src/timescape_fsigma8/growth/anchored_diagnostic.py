"""Externally anchored conditional density-growth diagnostic (Phase 1D-D).

This module implements only Candidate A of the frozen Phase 1D-C closure
audit.  Given an already resolved clean-system :class:`GrowthPipelineResult`,
it evaluates the Phase 1D-A equations (D6a)--(D6b)

    A_anchor(t) = sigma8_anchor(t_ref) G(t; t_ref),
    Q_anchor(t) = f(t) A_anchor(t)
                = sigma8_anchor(t_ref) dG/d ln(a_coordinate).

The supplied scalar is an external normalization at the same resolved
reference epoch.  It is not predicted by Timescape.  No spectrum, smoothing
integral, observational redshift-space mapping, or likelihood is evaluated.
Only the clean, scale-independent comoving and Meszaros systems are eligible;
the latter is retained solely as a comparison baseline with the mandatory
physical caveat recorded in every result.

Scientific references: reports/phase1d_a_growth_observable_audit.md,
Secs. 6--9 and equations (D6a)--(D6b); [GM] Eq. (4.14) for
``Z = -dDelta_d/dt``; the tracker bare/dressed conversion audited in Phase
1D-A Sec. 7.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum

import numpy as np
from numpy.typing import NDArray

import timescape_fsigma8.background as bg
from timescape_fsigma8.growth.histories import GrowthProvenance
from timescape_fsigma8.growth.pipeline import (
    GrowthPipelineResult,
    ResolvedGrowthReference,
)
from timescape_fsigma8.growth.scenarios import (
    DensityContrastMapping,
    GrowthCoordinate,
    GrowthScenario,
    GrowthSystem,
)


_PHASE1D_D_T_CHECKPOINT = "f960a9054ae9db3a7c378557ac3a2938c5ff7ef0"

_ASSUMPTION_DEFINITIONS = {
    "A1": "linear evolution throughout the evaluated interval",
    "A2": (
        "scale-independent growth over the matched-frame smoothing-kernel "
        "support: a k-free operator and k-independent initial mode mixture"
    ),
    "A3": (
        "fixed spectrum shape at the reference epoch, with only the common "
        "growth factor changing that shape"
    ),
    "A4": (
        "one fixed smoothing convention with explicit radius, h convention, "
        "spatial frame, and reciprocal k/radius units"
    ),
    "A5": (
        "positive differentiable relative growth throughout the evaluated "
        "interval"
    ),
    "A6": (
        "the supplied anchor is a consistent normalization at exactly the "
        "resolved growth reference"
    ),
}

_GENERIC_LIMITATIONS = (
    "externally anchored conditional density-growth diagnostic",
    "the Timescape evolution does not predict the supplied anchor",
    "no sigma8 integral or spectrum normalization is computed",
    "no standard observational f sigma8 quantity is computed",
    "no RSD interpretation, likelihood, fit, or data comparison is supplied",
    "valid only under the explicitly acknowledged A1--A6 conditions",
)

_COMOVING_CAVEAT = (
    "comoving_primary: clean scale-independent system used as the primary "
    "conditional diagnostic carrier"
)

_MESZAROS_CAVEAT = (
    "comparison_baseline_only: the Meszaros approximation is formally "
    "inapplicable to the Timescape framework and is retained only as a "
    "comparison baseline"
)


def _require_nonempty(value: str, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be an explicit nonempty string")
    return value


def _frozen_float64(values) -> NDArray[np.float64]:
    out = np.array(values, dtype=np.float64, copy=True)
    out.flags.writeable = False
    return out


class AnchorProvenanceKind(str, Enum):
    """Allowed provenance of the externally supplied normalization."""

    EXTERNAL_IMPORT = "external_import"
    SYNTHETIC_VALIDATION_ONLY = "synthetic_validation_only"


class AnchoredGrowthModelRole(str, Enum):
    """Scientific role of an eligible clean perturbation system."""

    COMOVING_PRIMARY = "comoving_primary"
    MESZAROS_COMPARISON_ONLY = "meszaros_comparison_only"


class AnchoredDiagnosticClassification(str, Enum):
    """Mandatory interpretation token carried by every result."""

    CONDITIONAL_ANCHORED_DIAGNOSTIC_NOT_OBSERVATIONAL_PREDICTION = (
        "CONDITIONAL_ANCHORED_DIAGNOSTIC_NOT_OBSERVATIONAL_PREDICTION"
    )


@dataclass(frozen=True)
class AnchoredDiagnosticAssumptions:
    """Mandatory explicit acknowledgement of Phase 1D-A conditions A1--A6.

    Every field is required and must be the boolean value ``True``.  A2 and
    A5 are also checked independently against the supplied pipeline result;
    the boolean fields never substitute for those runtime checks.
    """

    a1_linear_evolution_acknowledged: bool
    a2_scale_independent_growth_acknowledged: bool
    a3_fixed_reference_spectrum_shape_acknowledged: bool
    a4_fixed_smoothing_convention_acknowledged: bool
    a5_positive_differentiable_growth_acknowledged: bool
    a6_anchor_at_resolved_reference_acknowledged: bool

    def __post_init__(self) -> None:
        for field in fields(self):
            value = getattr(self, field.name)
            if type(value) is not bool:  # bool only; reject integers/lookalikes
                raise ValueError(f"{field.name} must be an explicit bool")
            if not value:
                raise ValueError(
                    f"{field.name} must be explicitly acknowledged as True"
                )

    def to_metadata(self) -> dict:
        """Return A1--A6 definitions and explicit acknowledgement values."""
        values = [getattr(self, field.name) for field in fields(self)]
        return {
            key: {"definition": definition, "acknowledged": values[index]}
            for index, (key, definition) in enumerate(
                _ASSUMPTION_DEFINITIONS.items()
            )
        }


@dataclass(frozen=True)
class ExternalDensityAmplitudeAnchor:
    """Immutable external sigma8 anchor bound to one resolved reference.

    ``sigma8_anchor_at_reference`` is positive, finite, and dimensionless.
    The smoothing metadata are declarations supplied by the caller; the
    package neither infers nor evaluates a smoothing radius or spectrum.
    The direct :class:`ResolvedGrowthReference` binding avoids a second,
    unchecked copy of the reference epoch.
    """

    sigma8_anchor_at_reference: float
    provenance_label: str
    provenance_kind: AnchorProvenanceKind
    resolved_reference: ResolvedGrowthReference
    smoothing_radius_definition: str
    h_convention: str
    spatial_frame: str
    reciprocal_units_statement: str

    def __post_init__(self) -> None:
        value = float(self.sigma8_anchor_at_reference)
        if not np.isfinite(value) or value <= 0.0:
            raise ValueError(
                "sigma8_anchor_at_reference must be finite and positive"
            )
        object.__setattr__(self, "sigma8_anchor_at_reference", value)
        if not isinstance(self.provenance_kind, AnchorProvenanceKind):
            raise ValueError(
                "provenance_kind must be an explicit AnchorProvenanceKind"
            )
        if not isinstance(self.resolved_reference, ResolvedGrowthReference):
            raise ValueError(
                "resolved_reference must be an explicit "
                "ResolvedGrowthReference"
            )
        for name in (
            "provenance_label",
            "smoothing_radius_definition",
            "h_convention",
            "spatial_frame",
            "reciprocal_units_statement",
        ):
            _require_nonempty(getattr(self, name), name)

    def to_metadata(self) -> dict:
        """Return complete anchor, convention, and reference provenance."""
        return {
            "sigma8_anchor_at_reference": self.sigma8_anchor_at_reference,
            "provenance_label": self.provenance_label,
            "provenance_kind": self.provenance_kind.value,
            "resolved_reference": self.resolved_reference.to_metadata(),
            "smoothing_radius_definition": self.smoothing_radius_definition,
            "h_convention": self.h_convention,
            "spatial_frame": self.spatial_frame,
            "reciprocal_units_statement": self.reciprocal_units_statement,
        }


@dataclass(frozen=True)
class AnchoredDensityGrowthDiagnosticResult:
    """Immutable result of the Phase 1D-D conditional diagnostic.

    The two evaluations of ``Q_anchor`` implement Phase 1D-A (D6b): the
    product ``f A_anchor`` and the non-logarithmic form
    ``anchor * dG/d ln(a_coordinate)`` derived from [GM] Eq. (4.14).
    """

    scenario_identifier: str
    scenario: GrowthScenario
    perturbation_system: GrowthSystem
    model_role: AnchoredGrowthModelRole
    model_caveat: str
    growth_coordinate: GrowthCoordinate
    resolved_reference: ResolvedGrowthReference
    anchor: ExternalDensityAmplitudeAnchor
    assumptions: AnchoredDiagnosticAssumptions
    source_growth_provenance: GrowthProvenance
    phase1d_d_t_checkpoint: str
    scientific_definition_source: str
    classification: AnchoredDiagnosticClassification
    limitations: tuple[str, ...]
    delta_d_crossing_count: int
    z_crossing_count: int
    validity_interval_count: int
    reference_is_sampled_grid_point: bool
    reference_nearest_sample_index: int
    reference_nearest_sample_time_offset: float
    continuous_reference_growth: float
    continuous_reference_anchored_amplitude: float
    t_solver_units: NDArray[np.float64]
    t_gyr: NDArray[np.float64]
    dressed_redshift: NDArray[np.float64]
    a_D: NDArray[np.float64]
    a_obs: NDArray[np.float64]
    relative_growth: NDArray[np.float64]
    selected_growth_rate: NDArray[np.float64]
    anchored_density_amplitude: NDArray[np.float64]
    anchored_density_growth: NDArray[np.float64]
    alternative_nonlogarithmic_evaluation: NDArray[np.float64]
    identity_absolute_residual: NDArray[np.float64]
    identity_relative_residual: NDArray[np.float64]
    identity_relative_scale: float

    def __post_init__(self) -> None:
        if not isinstance(self.scenario, GrowthScenario):
            raise ValueError("scenario must be an explicit GrowthScenario")
        if self.scenario_identifier != self.scenario.identifier:
            raise ValueError("scenario_identifier must match scenario.identifier")
        if not isinstance(self.perturbation_system, GrowthSystem):
            raise ValueError("perturbation_system must be an explicit GrowthSystem")
        if not isinstance(self.model_role, AnchoredGrowthModelRole):
            raise ValueError("model_role must be an explicit AnchoredGrowthModelRole")
        if not isinstance(self.growth_coordinate, GrowthCoordinate):
            raise ValueError("growth_coordinate must be an explicit GrowthCoordinate")
        if not isinstance(self.classification, AnchoredDiagnosticClassification):
            raise ValueError(
                "classification must be an explicit "
                "AnchoredDiagnosticClassification"
            )
        if not isinstance(self.resolved_reference, ResolvedGrowthReference):
            raise ValueError("resolved_reference must be ResolvedGrowthReference")
        if not isinstance(self.anchor, ExternalDensityAmplitudeAnchor):
            raise ValueError("anchor must be ExternalDensityAmplitudeAnchor")
        if not isinstance(self.assumptions, AnchoredDiagnosticAssumptions):
            raise ValueError("assumptions must be AnchoredDiagnosticAssumptions")
        if not isinstance(self.source_growth_provenance, GrowthProvenance):
            raise ValueError("source_growth_provenance must be GrowthProvenance")
        _require_nonempty(self.model_caveat, "model_caveat")
        _require_nonempty(
            self.scientific_definition_source,
            "scientific_definition_source",
        )
        if self.perturbation_system is not self.scenario.perturbation_system:
            raise ValueError(
                "perturbation_system must match scenario.perturbation_system"
            )
        if self.growth_coordinate is not self.scenario.growth_coordinate:
            raise ValueError(
                "growth_coordinate must match scenario.growth_coordinate"
            )
        if self.perturbation_system is GrowthSystem.COMOVING:
            expected_role = AnchoredGrowthModelRole.COMOVING_PRIMARY
            expected_caveat = _COMOVING_CAVEAT
        elif self.perturbation_system is GrowthSystem.MESZAROS:
            expected_role = AnchoredGrowthModelRole.MESZAROS_COMPARISON_ONLY
            expected_caveat = _MESZAROS_CAVEAT
        else:
            raise ValueError(
                "diagnostic result accepts only comoving or Meszaros systems"
            )
        if self.model_role is not expected_role:
            raise ValueError(
                "model_role is inconsistent with perturbation_system"
            )
        if self.model_caveat != expected_caveat:
            raise ValueError(
                "model_caveat is inconsistent with perturbation_system"
            )
        if self.resolved_reference != self.anchor.resolved_reference:
            raise ValueError(
                "resolved_reference must equal anchor.resolved_reference"
            )
        if self.phase1d_d_t_checkpoint != _PHASE1D_D_T_CHECKPOINT:
            raise ValueError(
                "phase1d_d_t_checkpoint must equal the frozen checkpoint"
            )
        if type(self.reference_nearest_sample_index) is not int:
            raise ValueError("reference_nearest_sample_index must be an integer")
        if not np.isfinite(self.reference_nearest_sample_time_offset):
            raise ValueError(
                "reference_nearest_sample_time_offset must be finite"
            )
        if type(self.reference_is_sampled_grid_point) is not bool:
            raise ValueError("reference_is_sampled_grid_point must be a bool")
        for name in (
            "delta_d_crossing_count",
            "z_crossing_count",
            "validity_interval_count",
        ):
            value = getattr(self, name)
            if type(value) is not int or value < 0:
                raise ValueError(f"{name} must be a nonnegative integer")
        array_names = (
            "t_solver_units",
            "t_gyr",
            "dressed_redshift",
            "a_D",
            "a_obs",
            "relative_growth",
            "selected_growth_rate",
            "anchored_density_amplitude",
            "anchored_density_growth",
            "alternative_nonlogarithmic_evaluation",
            "identity_absolute_residual",
            "identity_relative_residual",
        )
        shapes = set()
        for name in array_names:
            array = _frozen_float64(getattr(self, name))
            if array.ndim != 1:
                raise ValueError(f"{name} must be one-dimensional")
            if not np.all(np.isfinite(array)):
                raise ValueError(f"{name} must contain only finite values")
            object.__setattr__(self, name, array)
            shapes.add(array.shape)
        if len(shapes) != 1:
            raise ValueError("all diagnostic arrays must share one sampling grid")
        sample_count = self.t_solver_units.size
        if sample_count < 2:
            raise ValueError("diagnostic arrays must contain at least two samples")
        if not 0 <= self.reference_nearest_sample_index < sample_count:
            raise ValueError(
                "reference_nearest_sample_index is outside the sampling grid"
            )
        if not isinstance(self.limitations, tuple) or not self.limitations:
            raise ValueError("limitations must be a nonempty immutable tuple")
        if any(not isinstance(item, str) or not item for item in self.limitations):
            raise ValueError("every limitation must be a nonempty string")
        if expected_caveat not in self.limitations:
            raise ValueError(
                "limitations must contain the mandatory system caveat"
            )
        if not np.isfinite(self.identity_relative_scale) or (
            self.identity_relative_scale <= 0.0
        ):
            raise ValueError("identity_relative_scale must be finite and positive")
        if self.continuous_reference_growth != 1.0:
            raise ValueError("continuous reference growth must equal exactly one")
        if self.continuous_reference_anchored_amplitude != (
            self.anchor.sigma8_anchor_at_reference
        ):
            raise ValueError(
                "continuous reference anchored amplitude must equal the anchor"
            )

    @property
    def max_identity_absolute_residual(self) -> float:
        return float(np.max(self.identity_absolute_residual))

    @property
    def max_identity_relative_residual(self) -> float:
        return float(np.max(self.identity_relative_residual))

    def to_json_dict(self) -> dict:
        """Serialize deterministically to JSON-compatible Python values."""
        return {
            "scenario_identifier": self.scenario_identifier,
            "scenario": {
                "scientific_choices": self.scenario.to_metadata(),
                "perturbation_system": self.perturbation_system.value,
                "model_role": self.model_role.value,
                "model_caveat": self.model_caveat,
                "growth_coordinate": self.growth_coordinate.value,
            },
            "resolved_reference": self.resolved_reference.to_metadata(),
            "anchor": self.anchor.to_metadata(),
            "assumptions": self.assumptions.to_metadata(),
            "provenance": {
                "source_growth_result": self.source_growth_provenance.to_metadata(),
                "phase1d_d_t_checkpoint": self.phase1d_d_t_checkpoint,
                "scientific_definition_source": self.scientific_definition_source,
            },
            "classification": self.classification.value,
            "limitations": list(self.limitations),
            "crossing_metadata": {
                "delta_d_crossing_count": self.delta_d_crossing_count,
                "z_crossing_count": self.z_crossing_count,
                "validity_interval_count": self.validity_interval_count,
            },
            "continuous_reference_check": {
                "reference_is_sampled_grid_point": (
                    self.reference_is_sampled_grid_point
                ),
                "nearest_sample_index": self.reference_nearest_sample_index,
                "nearest_sample_time_offset": (
                    self.reference_nearest_sample_time_offset
                ),
                "growth_at_continuous_reference": (
                    self.continuous_reference_growth
                ),
                "anchored_amplitude_at_continuous_reference": (
                    self.continuous_reference_anchored_amplitude
                ),
            },
            "sampling_grid": {
                "t_solver_units": self.t_solver_units.tolist(),
                "t_gyr": self.t_gyr.tolist(),
                "dressed_redshift": self.dressed_redshift.tolist(),
                "a_D": self.a_D.tolist(),
                "a_obs": self.a_obs.tolist(),
            },
            "quantities": {
                "relative_growth": self.relative_growth.tolist(),
                "selected_growth_rate": self.selected_growth_rate.tolist(),
                "anchored_density_amplitude": (
                    self.anchored_density_amplitude.tolist()
                ),
                "anchored_density_growth": self.anchored_density_growth.tolist(),
                "alternative_nonlogarithmic_evaluation": (
                    self.alternative_nonlogarithmic_evaluation.tolist()
                ),
            },
            "identity_residuals": {
                "absolute": self.identity_absolute_residual.tolist(),
                "relative_to_global_term_scale": (
                    self.identity_relative_residual.tolist()
                ),
                "global_term_scale": self.identity_relative_scale,
                "max_absolute": self.max_identity_absolute_residual,
                "max_relative": self.max_identity_relative_residual,
            },
        }


def anchored_density_growth_diagnostic(
    *,
    growth_result: GrowthPipelineResult,
    anchor: ExternalDensityAmplitudeAnchor,
    assumptions: AnchoredDiagnosticAssumptions,
) -> AnchoredDensityGrowthDiagnosticResult:
    """Evaluate the Phase 1D-A (D6a)--(D6b) anchored diagnostic.

    Scientific inputs are keyword-only and mandatory.  The function consumes
    an already resolved Phase 1D-B result and never integrates, interpolates,
    differentiates, smooths, or renormalizes a trajectory.  The analytic
    derivative comes from [GM] Eq. (4.14) through the frozen rate layer.
    """
    if not isinstance(growth_result, GrowthPipelineResult):
        raise ValueError("growth_result must be one GrowthPipelineResult")
    if not isinstance(anchor, ExternalDensityAmplitudeAnchor):
        raise ValueError("anchor must be ExternalDensityAmplitudeAnchor")
    if not isinstance(assumptions, AnchoredDiagnosticAssumptions):
        raise ValueError("assumptions must be AnchoredDiagnosticAssumptions")

    history = growth_result.history
    scenario = history.scenario
    system = scenario.perturbation_system
    if system is GrowthSystem.COMOVING:
        role = AnchoredGrowthModelRole.COMOVING_PRIMARY
        model_caveat = _COMOVING_CAVEAT
    elif system is GrowthSystem.MESZAROS:
        role = AnchoredGrowthModelRole.MESZAROS_COMPARISON_ONLY
        model_caveat = _MESZAROS_CAVEAT
    else:
        raise ValueError(
            "anchored diagnostic accepts only clean comoving or Meszaros "
            "GrowthPipelineResult inputs"
        )

    if history.provenance is None:
        raise ValueError(
            "growth_result must carry explicit frozen-result provenance"
        )
    if anchor.resolved_reference != growth_result.reference:
        raise ValueError(
            "anchor resolved_reference does not match the growth result "
            "reference"
        )

    # A5 is independently enforced on the actual resolved trajectory.  A
    # Delta_d root or endpoint root makes a global positive differentiable
    # history unavailable even if a sparse sampled array happened to miss it.
    if growth_result.crossings.delta_d_roots:
        raise ValueError("A5 fails: the growth history has a Delta_d crossing")
    if any(
        endpoint.component == "Delta_d"
        for endpoint in growth_result.crossings.endpoint_roots
    ):
        raise ValueError("A5 fails: Delta_d vanishes at an interval endpoint")

    reference_amplitude = growth_result.reference.amplitude_delta_d
    expected_growth = (
        np.asarray(history.delta_d, dtype=np.float64) / reference_amplitude
    )
    growth = np.asarray(growth_result.relative_growth_delta_d, dtype=np.float64)
    if not np.all(np.isfinite(growth)) or np.any(growth <= 0.0):
        raise ValueError("A5 fails: relative growth must be finite and positive")
    if expected_growth.shape != growth.shape:
        raise ValueError(
            "relative_growth_delta_d shape is inconsistent with history.delta_d"
        )
    growth_consistency_scale = max(
        float(np.max(np.abs(expected_growth))),
        np.finfo(np.float64).tiny,
    )
    growth_consistency_residual = float(
        np.max(np.abs(growth - expected_growth)) / growth_consistency_scale
    )
    if not np.isfinite(growth_consistency_residual) or (
        growth_consistency_residual > 1.0e-14
    ):
        raise ValueError(
            "relative_growth_delta_d is inconsistent with "
            "history.delta_d / reference.amplitude_delta_d"
        )

    coordinate = scenario.growth_coordinate
    if coordinate is GrowthCoordinate.BARE_AD:
        selected_rate = np.asarray(growth_result.rates.f_bare, dtype=np.float64)
        delta_derivative = np.asarray(
            growth_result.rates.dDelta_d_dln_aD, dtype=np.float64
        )
    elif coordinate is GrowthCoordinate.DRESSED_REDSHIFT:
        selected_rate = np.asarray(
            growth_result.rates.f_dressed, dtype=np.float64
        )
        delta_derivative = np.asarray(
            growth_result.rates.dDelta_d_dln_aobs, dtype=np.float64
        )
    else:  # pragma: no cover - frozen enum is exhaustive
        raise ValueError(f"unsupported growth coordinate: {coordinate!r}")
    if not np.all(np.isfinite(selected_rate)):
        raise ValueError("A5 fails: selected logarithmic rate is not finite")
    if not np.all(np.isfinite(delta_derivative)):
        raise ValueError("A5 fails: non-logarithmic derivative is not finite")

    if (
        scenario.density_contrast_mapping
        is DensityContrastMapping.MAP_TO_DELTA_M_VIA_MINUS_K_CODE2
    ):
        if growth_result.mapped is None:
            raise ValueError("mapped density basis selected but output is absent")
        mapped = growth_result.mapped
        mapped_growth = np.asarray(mapped.relative_growth, dtype=np.float64)
        scale = max(float(np.max(np.abs(growth))), np.finfo(np.float64).tiny)
        if np.max(np.abs(mapped_growth - growth)) / scale > 1.0e-14:
            raise ValueError(
                "mapped delta_m and Delta_d relative growth are inconsistent"
            )
        k_code = mapped.harmonic.k_code
        mapped_reference_amplitude = reference_amplitude / (-k_code**2)
        mapped_derivative = (
            mapped.d_delta_m_dln_aD
            if coordinate is GrowthCoordinate.BARE_AD
            else mapped.d_delta_m_dln_aobs
        )
        derivative_growth = np.asarray(
            mapped_derivative, dtype=np.float64
        ) / mapped_reference_amplitude
    else:
        derivative_growth = delta_derivative / reference_amplitude

    sigma_anchor = anchor.sigma8_anchor_at_reference
    anchored_amplitude = sigma_anchor * growth
    diagnostic = selected_rate * anchored_amplitude
    alternative = sigma_anchor * derivative_growth
    absolute_residual = np.abs(diagnostic - alternative)
    identity_scale = max(
        float(np.max(np.abs(diagnostic))),
        float(np.max(np.abs(alternative))),
        np.finfo(np.float64).tiny,
    )
    relative_residual = absolute_residual / identity_scale

    t = np.asarray(history.t, dtype=np.float64)
    nearest_index = int(
        np.argmin(np.abs(t - growth_result.reference.t_solver_units))
    )
    nearest_offset = float(
        t[nearest_index] - growth_result.reference.t_solver_units
    )
    # These are consequences of normalizing by the stored continuous
    # dense-reference amplitude.  This is not a second dense evaluation.
    continuous_growth = 1.0
    continuous_amplitude = float(sigma_anchor)

    return AnchoredDensityGrowthDiagnosticResult(
        scenario_identifier=scenario.identifier,
        scenario=scenario,
        perturbation_system=system,
        model_role=role,
        model_caveat=model_caveat,
        growth_coordinate=coordinate,
        resolved_reference=growth_result.reference,
        anchor=anchor,
        assumptions=assumptions,
        source_growth_provenance=history.provenance,
        phase1d_d_t_checkpoint=_PHASE1D_D_T_CHECKPOINT,
        scientific_definition_source=(
            "Phase 1D-A equations D6a-D6b; GM Eq. (4.14); "
            "Phase 1D-A tracker chain D3"
        ),
        classification=(
            AnchoredDiagnosticClassification.
            CONDITIONAL_ANCHORED_DIAGNOSTIC_NOT_OBSERVATIONAL_PREDICTION
        ),
        limitations=_GENERIC_LIMITATIONS + (model_caveat,),
        delta_d_crossing_count=len(growth_result.crossings.delta_d_roots),
        z_crossing_count=len(growth_result.crossings.z_roots),
        validity_interval_count=len(growth_result.validity_intervals),
        reference_is_sampled_grid_point=bool(nearest_offset == 0.0),
        reference_nearest_sample_index=nearest_index,
        reference_nearest_sample_time_offset=nearest_offset,
        continuous_reference_growth=continuous_growth,
        continuous_reference_anchored_amplitude=continuous_amplitude,
        t_solver_units=t,
        t_gyr=history.t_gyr(),
        dressed_redshift=history.dressed_redshift(),
        a_D=bg.a_D(t, history.background.params),
        a_obs=bg.a_w(t, history.background.params),
        relative_growth=growth,
        selected_growth_rate=selected_rate,
        anchored_density_amplitude=anchored_amplitude,
        anchored_density_growth=diagnostic,
        alternative_nonlogarithmic_evaluation=alternative,
        identity_absolute_residual=absolute_residual,
        identity_relative_residual=relative_residual,
        identity_relative_scale=identity_scale,
    )
