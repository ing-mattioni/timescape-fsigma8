"""Phase 1D-B growth-scenario model: mandatory explicit scientific choices.

Specification: reports/phase1d_a_growth_observable_audit.md Secs. 15-16 and
reports/phase1d_a_observable_inventory.json ``scenario_dimensions``.

Every scientific choice is a mandatory explicit argument with no default.
Non-applicable fields must be passed as the explicit ``not_applicable``
member, never omitted or inferred.  Inconsistent combinations are rejected,
not silently corrected.  Neither D3 branch is canonical, preferred,
physical, corrected, recommended, intended, or a default.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations.initial_conditions import RateUnitConvention
from timescape_fsigma8.perturbations.scenarios import (
    EpochChoice,
    EpochRootConfig,
    TimeUnit,
    UPSTREAM_NOTEBOOK_TIME_UNIT,
)
from timescape_fsigma8.perturbations.solver import SolverConfig
from timescape_fsigma8.presets import (
    NOTEBOOK_REFERENCE,
    PAPER_REFERENCE,
    ReferencePreset,
)


class GrowthSystem(str, Enum):
    """Mandatory perturbation-closure choice (frozen Phase 1C systems)."""

    MESZAROS = "meszaros"
    COMOVING = "comoving"
    BAROTROPIC = "barotropic"


class GrowthBackgroundPreset(str, Enum):
    """Mandatory background parametrisation (frozen Phase 1B presets)."""

    PAPER_REFERENCE = "paper_reference"
    NOTEBOOK_REFERENCE = "notebook_reference"


class GrowthD3Branch(str, Enum):
    """Unresolved Phase 1C-A F1 branch of [GM] Eq. (4.15).

    ``NOT_APPLICABLE`` is the explicit value for the clean systems.  The two
    real branches remain unresolved; neither is ranked in any way.
    """

    NOT_APPLICABLE = "not_applicable"
    PRINTED_4_15 = "printed_4_15"
    DERIVED_4_10 = "derived_4_10"


class GrowthTiltForm(str, Enum):
    """Tilt-state representation ([GM] Vtilde=(1+w_eff)V); barotropic only."""

    NOT_APPLICABLE = "not_applicable"
    UNRESCALED_V = "unrescaled_V"
    RESCALED_VTILDE = "rescaled_Vtilde"


class GrowthWavenumberConvention(str, Enum):
    """Unresolved Phase 1C-A F7 numerical meaning of a supplied k."""

    NOT_APPLICABLE = "not_applicable"
    UPSTREAM_TIMESCAPE_K = "upstream_timescape_k"
    PAPER_LCDM_HUBBLE_K = "paper_lcdm_hubble_k"


class GrowthCoordinate(str, Enum):
    """Abscissa of the growth factor and rate (1D-A Sec. 7); no default."""

    BARE_AD = "bare_aD"
    DRESSED_REDSHIFT = "dressed_redshift"


class DensityContrastMapping(str, Enum):
    """Output variable choice (1D-A Sec. 15).

    ``KEEP_DELTA_D`` retains the CGI Laplacian scalar.
    ``MAP_TO_DELTA_M_VIA_MINUS_K_CODE2`` additionally exposes the
    solver-harmonic coefficient ``delta_m = -Delta_d/k_code^2``
    (1D-A Eq. (D1b-code)); it requires explicit harmonic metadata.
    """

    KEEP_DELTA_D = "keep_Delta_d"
    MAP_TO_DELTA_M_VIA_MINUS_K_CODE2 = "map_to_delta_m_via_minus_k_code2"


# The paper preset uses the same upstream cell-2 Gyr conversion convention
# t_code = t_Gyr * h/9.778 as the frozen UPSTREAM_NOTEBOOK_TIME_UNIT, with
# the paper's h = 0.7303 ([GM] Sec. 5.1.1) instead of the notebook's 0.7323.
# This is the reproduction-era approximation, deliberately distinct from the
# exact IAU conversion in timescape_fsigma8.units (see Phase 1C-B1 report).
PAPER_REFERENCE_TIME_UNIT = TimeUnit(
    name="paper H0=1 code time (h=0.7303; 9.778 Gyr approximation)",
    target_time_per_gyr=0.7303 / 9.778,
)

# Planck 2018 dressed h of [GM] ref. [3], fixed by the frozen Phase 1C IC
# recipe (PLANCK_2018_QPLUS_RECIPE.h) and the F7 conversion.
LCDM_REFERENCE_H = 0.674


def _require_enum(value, enum_type, name: str):
    if not isinstance(value, enum_type):
        raise ValueError(
            f"{name} must be an explicit {enum_type.__name__} member, got {value!r}"
        )
    return value


@dataclass(frozen=True)
class ResolvedBackground:
    """A growth preset resolved to solver-unit tracker parameters.

    ``params`` is in code units with H0_dressed = 1 (the unit system of the
    frozen Phase 1C-B1/B2 validation infrastructure), so solver times match
    the frozen upstream-compatible epoch definitions bit-for-bit.
    """

    preset: GrowthBackgroundPreset
    params: TrackerParams
    timescape_h: float
    lcdm_h: float
    time_unit: TimeUnit
    source_preset_name: str

    @property
    def t0(self) -> float:
        """Present bare (volume-average) age in solver units."""
        return self.params.t0


def resolve_background(preset: GrowthBackgroundPreset) -> ResolvedBackground:
    """Resolve a mandatory preset choice to frozen Phase 1B parameters."""
    preset = _require_enum(preset, GrowthBackgroundPreset, "background_preset")
    source: ReferencePreset
    if preset is GrowthBackgroundPreset.NOTEBOOK_REFERENCE:
        source = NOTEBOOK_REFERENCE
        time_unit = UPSTREAM_NOTEBOOK_TIME_UNIT
    elif preset is GrowthBackgroundPreset.PAPER_REFERENCE:
        source = PAPER_REFERENCE
        time_unit = PAPER_REFERENCE_TIME_UNIT
    else:  # pragma: no cover - exhaustive defensive guard
        raise ValueError(f"unsupported background preset: {preset!r}")
    return ResolvedBackground(
        preset=preset,
        params=TrackerParams.from_dressed_H0(fv0=source.fv0, H0=1.0),
        timescape_h=source.H0_dressed_km_s_Mpc / 100.0,
        lcdm_h=LCDM_REFERENCE_H,
        time_unit=time_unit,
        source_preset_name=source.name,
    )


@dataclass(frozen=True)
class GrowthScenario:
    """Immutable Phase 1D-B scientific scenario; every field is mandatory.

    Applicability rules (1D-B specification Sec. 3/6; 1D-A Sec. 15):

    * ``meszaros``/``comoving`` require ``d3_branch``, ``tilt_form``, and
      ``wavenumber_convention`` all explicitly ``NOT_APPLICABLE``; a
      ``supplied_mode_k`` is accepted only together with the density-contrast
      mapping (as explicit harmonic metadata for the pure per-mode
      conversion) and never alters the scale-independent dynamics.
    * ``barotropic`` requires one real D3 branch, one real tilt form, one
      real wavenumber convention, and an explicit positive finite
      ``supplied_mode_k`` with a ``mode_label``.

    Inconsistent combinations raise ``ValueError``; nothing is corrected
    silently and no field has a scientific default.
    """

    perturbation_system: GrowthSystem
    background_preset: GrowthBackgroundPreset
    d3_branch: GrowthD3Branch
    tilt_form: GrowthTiltForm
    rate_unit_convention: RateUnitConvention
    epoch_choice: EpochChoice
    wavenumber_convention: GrowthWavenumberConvention
    growth_coordinate: GrowthCoordinate
    density_contrast_mapping: DensityContrastMapping
    supplied_mode_k: float | None
    mode_label: str | None

    def __post_init__(self) -> None:
        system = _require_enum(
            self.perturbation_system, GrowthSystem, "perturbation_system"
        )
        _require_enum(
            self.background_preset, GrowthBackgroundPreset, "background_preset"
        )
        branch = _require_enum(self.d3_branch, GrowthD3Branch, "d3_branch")
        tilt = _require_enum(self.tilt_form, GrowthTiltForm, "tilt_form")
        _require_enum(
            self.rate_unit_convention, RateUnitConvention, "rate_unit_convention"
        )
        _require_enum(self.epoch_choice, EpochChoice, "epoch_choice")
        kconv = _require_enum(
            self.wavenumber_convention,
            GrowthWavenumberConvention,
            "wavenumber_convention",
        )
        _require_enum(self.growth_coordinate, GrowthCoordinate, "growth_coordinate")
        mapping = _require_enum(
            self.density_contrast_mapping,
            DensityContrastMapping,
            "density_contrast_mapping",
        )

        if self.supplied_mode_k is not None:
            k = float(self.supplied_mode_k)
            if not np.isfinite(k) or k <= 0.0:
                raise ValueError(
                    f"supplied_mode_k must be finite and positive, got {k!r}"
                )
            if self.mode_label is None or not str(self.mode_label):
                raise ValueError(
                    "a supplied_mode_k requires an explicit nonempty mode_label"
                )
        elif self.mode_label is not None:
            raise ValueError("mode_label without supplied_mode_k is not allowed")

        if system is GrowthSystem.BAROTROPIC:
            if branch is GrowthD3Branch.NOT_APPLICABLE:
                raise ValueError(
                    "barotropic requires an explicit real d3_branch "
                    "(printed_4_15 or derived_4_10); not_applicable is invalid"
                )
            if tilt is GrowthTiltForm.NOT_APPLICABLE:
                raise ValueError(
                    "barotropic requires an explicit real tilt_form; "
                    "not_applicable is invalid"
                )
            if kconv is GrowthWavenumberConvention.NOT_APPLICABLE:
                raise ValueError(
                    "barotropic requires an explicit real wavenumber_convention; "
                    "not_applicable is invalid"
                )
            if self.supplied_mode_k is None:
                raise ValueError("barotropic requires an explicit supplied_mode_k")
        else:  # meszaros / comoving (clean, scale-independent systems)
            if branch is not GrowthD3Branch.NOT_APPLICABLE:
                raise ValueError(
                    f"{system.value} requires d3_branch=not_applicable; a real "
                    "D3 branch is invalid for a clean system"
                )
            if tilt is not GrowthTiltForm.NOT_APPLICABLE:
                raise ValueError(
                    f"{system.value} requires tilt_form=not_applicable; a real "
                    "tilt form is invalid for a clean system"
                )
            if kconv is not GrowthWavenumberConvention.NOT_APPLICABLE:
                raise ValueError(
                    f"{system.value} requires wavenumber_convention="
                    "not_applicable for scale-independent growth-only runs"
                )
            wants_mapping = (
                mapping is DensityContrastMapping.MAP_TO_DELTA_M_VIA_MINUS_K_CODE2
            )
            if wants_mapping and self.supplied_mode_k is None:
                raise ValueError(
                    "the density-contrast mapping requires explicit harmonic "
                    "metadata: supply a nonzero finite supplied_mode_k "
                    "(interpreted directly as k_code for a clean system)"
                )
            if not wants_mapping and self.supplied_mode_k is not None:
                raise ValueError(
                    "a clean system accepts supplied_mode_k only together "
                    "with density_contrast_mapping="
                    "map_to_delta_m_via_minus_k_code2"
                )

    @property
    def identifier(self) -> str:
        """Stable human-readable identifier covering every scientific choice."""
        mode = (
            f"|mode={self.mode_label}|k={float(self.supplied_mode_k):.17g}"
            if self.supplied_mode_k is not None
            else "|mode=none"
        )
        return (
            f"system={self.perturbation_system.value}"
            f"|preset={self.background_preset.value}"
            f"|d3={self.d3_branch.value}"
            f"|tilt={self.tilt_form.value}"
            f"|rate={self.rate_unit_convention.value}"
            f"|epoch={self.epoch_choice.value}"
            f"|kconv={self.wavenumber_convention.value}"
            f"|coord={self.growth_coordinate.value}"
            f"|map={self.density_contrast_mapping.value}"
            f"{mode}"
        )

    def to_metadata(self) -> dict:
        """Serializable record of every scientific choice (no defaults)."""
        return {
            "perturbation_system": self.perturbation_system.value,
            "background_preset": self.background_preset.value,
            "d3_branch": self.d3_branch.value,
            "tilt_form": self.tilt_form.value,
            "rate_unit_convention": self.rate_unit_convention.value,
            "epoch_choice": self.epoch_choice.value,
            "wavenumber_convention": self.wavenumber_convention.value,
            "growth_coordinate": self.growth_coordinate.value,
            "density_contrast_mapping": self.density_contrast_mapping.value,
            "supplied_mode_k": (
                float(self.supplied_mode_k)
                if self.supplied_mode_k is not None
                else None
            ),
            "mode_label": self.mode_label,
        }


class GrowthReferenceCoordinate(str, Enum):
    """Coordinate in which the mandatory growth reference epoch is stated."""

    BARE_TIME_SOLVER_UNITS = "bare_time_solver_units"
    DRESSED_REDSHIFT = "dressed_redshift"


@dataclass(frozen=True)
class GrowthReference:
    """Mandatory explicit reference epoch for relative growth.

    There is no default reference: neither the initial epoch, nor today,
    nor z=0 is assumed.  ``root`` controls the bracketed Brent solve used
    when a dressed-redshift value must be converted to bare solver time
    (frozen Phase 1B ``redshift`` mapping).  ``amplitude_floor_rel`` is the
    explicit tolerance for rejecting a reference that is numerically
    indistinguishable from a zero crossing: a reference is rejected when the
    linearised time distance to the nearest zero, ``abs(Delta_d)/abs(Z)``
    (exact since ``Z = -dDelta_d/dt``), is at or below
    ``amplitude_floor_rel * integration_span``, or when a refined Delta_d
    root lies within that same time tolerance (the refined-root proximity
    test).
    """

    coordinate: GrowthReferenceCoordinate
    value: float
    root: EpochRootConfig
    amplitude_floor_rel: float

    def __post_init__(self) -> None:
        _require_enum(
            self.coordinate, GrowthReferenceCoordinate, "reference coordinate"
        )
        if not np.isfinite(self.value):
            raise ValueError("reference value must be finite")
        if self.coordinate is GrowthReferenceCoordinate.BARE_TIME_SOLVER_UNITS:
            if self.value <= 0.0:
                raise ValueError("a bare-time reference must be positive")
        else:
            if self.value < 0.0:
                raise ValueError("a dressed-redshift reference must be >= 0")
        if not isinstance(self.root, EpochRootConfig):
            raise ValueError("root must be an explicit EpochRootConfig")
        if not 0.0 < self.amplitude_floor_rel < 1.0:
            raise ValueError("amplitude_floor_rel must lie in (0, 1)")


@dataclass(frozen=True)
class DenseSolveConfig:
    """Explicit numerics of the dense (continuous) re-integration.

    The dense solution re-integrates the identical frozen RHS with
    ``dense_output=True`` solely to provide the controlled continuous
    representation required for reference-amplitude evaluation and
    bracket-preserving root refinement.  It never replaces the sampled
    frozen-solver history.
    """

    method: str
    rtol: float
    atol: float
    max_step: float
    first_step: float | None

    def __post_init__(self) -> None:
        if self.method not in {"RK45", "DOP853", "Radau"}:
            raise ValueError(f"unsupported dense method: {self.method}")
        if self.rtol <= 0.0 or self.atol <= 0.0:
            raise ValueError("dense tolerances must be positive")
        if self.max_step <= 0.0:
            raise ValueError("dense max_step must be positive")
        if self.first_step is not None and self.first_step <= 0.0:
            raise ValueError("dense first_step must be positive or None")


@dataclass(frozen=True)
class RootRefineConfig:
    """Explicit bracket-preserving root-refinement controls (Brent)."""

    xtol: float
    rtol: float
    maxiter: int
    residual_scale_gate: float

    def __post_init__(self) -> None:
        if self.xtol <= 0.0 or self.rtol <= 0.0:
            raise ValueError("root tolerances must be positive")
        if self.maxiter <= 0:
            raise ValueError("maxiter must be positive")
        if self.residual_scale_gate <= 0.0:
            raise ValueError("residual_scale_gate must be positive")


@dataclass(frozen=True)
class GrowthNumericsConfig:
    """Every numerical choice of a growth-pipeline run; all fields required.

    ``n_samples`` sets the uniform sampled grid on [t_i, t0] in solver
    units.  ``G`` is the explicit gravitational-constant value passed to the
    frozen RHS (for the tracker closed forms, 4*pi*G*rho products are
    G-independent; the value must still be explicit).
    ``near_zero_rel_floor`` defines the explicit near-zero policy: a sample
    is flagged as near zero iff it is exactly zero or its magnitude is at or
    below ``near_zero_rel_floor`` times the larger neighbouring sample
    magnitude (a neighbour-local scale), and such a sample is never treated
    as a solver-independent root by itself.
    """

    solver: SolverConfig
    n_samples: int
    G: float
    dense: DenseSolveConfig
    root: RootRefineConfig
    near_zero_rel_floor: float

    def __post_init__(self) -> None:
        if not isinstance(self.solver, SolverConfig):
            raise ValueError("solver must be an explicit SolverConfig")
        if self.n_samples < 3:
            raise ValueError("n_samples must be at least 3")
        if not np.isfinite(self.G) or self.G <= 0.0:
            raise ValueError("G must be finite and positive")
        if not isinstance(self.dense, DenseSolveConfig):
            raise ValueError("dense must be an explicit DenseSolveConfig")
        if not isinstance(self.root, RootRefineConfig):
            raise ValueError("root must be an explicit RootRefineConfig")
        if not 0.0 < self.near_zero_rel_floor < 1.0:
            raise ValueError("near_zero_rel_floor must lie in (0, 1)")

    def to_metadata(self) -> dict:
        return {
            "solver": {
                "method": self.solver.method,
                "rtol": self.solver.rtol,
                "atol": self.solver.atol,
                "max_step": (
                    "inf" if np.isinf(self.solver.max_step) else self.solver.max_step
                ),
                "first_step": self.solver.first_step,
            },
            "n_samples": self.n_samples,
            "G": self.G,
            "dense": {
                "method": self.dense.method,
                "rtol": self.dense.rtol,
                "atol": self.dense.atol,
                "max_step": (
                    "inf" if np.isinf(self.dense.max_step) else self.dense.max_step
                ),
                "first_step": self.dense.first_step,
            },
            "root": {
                "xtol": self.root.xtol,
                "rtol": self.root.rtol,
                "maxiter": self.root.maxiter,
                "residual_scale_gate": self.root.residual_scale_gate,
            },
            "near_zero_rel_floor": self.near_zero_rel_floor,
        }
