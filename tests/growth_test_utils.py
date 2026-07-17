"""Shared builders for the Phase 1D-B growth tests (not a test module).

The named numerics/reference records below are test/validation
configurations: every value is explicit and visible here; they are not
package defaults and carry no scientific preference.
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np

from timescape_fsigma8.perturbations import (
    TIGHT_DOP853,
    EpochChoice,
    RateUnitConvention,
)
from timescape_fsigma8.perturbations.scenarios import PHASE1C_EPOCH_ROOT
from timescape_fsigma8.growth import (
    DenseSolveConfig,
    DensityContrastMapping,
    GrowthBackgroundPreset,
    GrowthCoordinate,
    GrowthD3Branch,
    GrowthNumericsConfig,
    GrowthReference,
    GrowthReferenceCoordinate,
    GrowthScenario,
    GrowthSystem,
    GrowthTiltForm,
    GrowthWavenumberConvention,
    RootRefineConfig,
    run_growth_pipeline,
)

TEST_DENSE = DenseSolveConfig(
    method="DOP853", rtol=1e-11, atol=1e-13, max_step=np.inf, first_step=None
)
TEST_ROOT = RootRefineConfig(
    xtol=1e-13, rtol=8.9e-16, maxiter=100, residual_scale_gate=1e-6
)
TEST_NUMERICS = GrowthNumericsConfig(
    solver=TIGHT_DOP853,
    n_samples=600,
    G=1.0,
    dense=TEST_DENSE,
    root=TEST_ROOT,
    near_zero_rel_floor=1e-9,
)
TEST_REFERENCE_Z10 = GrowthReference(
    coordinate=GrowthReferenceCoordinate.DRESSED_REDSHIFT,
    value=10.0,
    root=PHASE1C_EPOCH_ROOT,
    amplitude_floor_rel=1e-10,
)


def clean_scenario(
    system: GrowthSystem,
    *,
    preset: GrowthBackgroundPreset = GrowthBackgroundPreset.NOTEBOOK_REFERENCE,
    rate: RateUnitConvention = RateUnitConvention.UPSTREAM_UNCONVERTED,
    epoch: EpochChoice = EpochChoice.UPSTREAM_0P218_GYR,
    coordinate: GrowthCoordinate = GrowthCoordinate.BARE_AD,
    mapping: DensityContrastMapping = DensityContrastMapping.KEEP_DELTA_D,
    mode_k: float | None = None,
    mode_label: str | None = None,
) -> GrowthScenario:
    return GrowthScenario(
        perturbation_system=system,
        background_preset=preset,
        d3_branch=GrowthD3Branch.NOT_APPLICABLE,
        tilt_form=GrowthTiltForm.NOT_APPLICABLE,
        rate_unit_convention=rate,
        epoch_choice=epoch,
        wavenumber_convention=GrowthWavenumberConvention.NOT_APPLICABLE,
        growth_coordinate=coordinate,
        density_contrast_mapping=mapping,
        supplied_mode_k=mode_k,
        mode_label=mode_label,
    )


def barotropic_scenario(
    branch: GrowthD3Branch,
    mode_k: float,
    mode_label: str,
    *,
    preset: GrowthBackgroundPreset = GrowthBackgroundPreset.NOTEBOOK_REFERENCE,
    tilt: GrowthTiltForm = GrowthTiltForm.UNRESCALED_V,
    rate: RateUnitConvention = RateUnitConvention.UPSTREAM_UNCONVERTED,
    epoch: EpochChoice = EpochChoice.UPSTREAM_0P218_GYR,
    kconv: GrowthWavenumberConvention = (
        GrowthWavenumberConvention.UPSTREAM_TIMESCAPE_K
    ),
    coordinate: GrowthCoordinate = GrowthCoordinate.BARE_AD,
    mapping: DensityContrastMapping = DensityContrastMapping.KEEP_DELTA_D,
) -> GrowthScenario:
    return GrowthScenario(
        perturbation_system=GrowthSystem.BAROTROPIC,
        background_preset=preset,
        d3_branch=branch,
        tilt_form=tilt,
        rate_unit_convention=rate,
        epoch_choice=epoch,
        wavenumber_convention=kconv,
        growth_coordinate=coordinate,
        density_contrast_mapping=mapping,
        supplied_mode_k=mode_k,
        mode_label=mode_label,
    )


@lru_cache(maxsize=32)
def _cached_run(scenario: GrowthScenario, n_samples: int):
    numerics = GrowthNumericsConfig(
        solver=TEST_NUMERICS.solver,
        n_samples=n_samples,
        G=TEST_NUMERICS.G,
        dense=TEST_NUMERICS.dense,
        root=TEST_NUMERICS.root,
        near_zero_rel_floor=TEST_NUMERICS.near_zero_rel_floor,
    )
    return run_growth_pipeline(
        scenario=scenario,
        reference=TEST_REFERENCE_Z10,
        numerics=numerics,
        provenance=None,
    )


def run_cached(scenario: GrowthScenario, n_samples: int = 600):
    """Session-cached pipeline run (scenarios are hashable frozen records)."""
    return _cached_run(scenario, n_samples)


# Frozen Phase 1D-A sampled-grid brackets (code time), quoted from
# reports/phase1d_a_observable_inventory.json ``crossing_brackets``.
# These are brackets only, never roots; tests verify refined roots fall
# strictly inside them and are not merely a bracket sample.
FROZEN_1DA_BRACKETS = {
    ("printed_4_15", "2pi"): {"Delta_d": None, "Z": None},
    ("printed_4_15", "5pi"): {
        "Delta_d": (0.22770117509286744, 0.2288375975917282),
        "Z": (0.1401966426805888, 0.14133306517944957),
    },
    ("printed_4_15", "10pi"): {
        "Delta_d": (0.07769340524324692, 0.07882982774210769),
        "Z": (0.05723780026375321, 0.058374222762613975),
    },
    ("derived_4_10", "2pi"): {
        "Delta_d": (0.7845481995346406, 0.7856846220335013),
        "Z": (0.3390705799812221, 0.34020700248008284),
    },
    ("derived_4_10", "5pi"): {
        "Delta_d": (0.15042444517033565, 0.1515608676691964),
        "Z": (0.09701258772387987, 0.09814901022274063),
    },
    ("derived_4_10", "10pi"): {
        "Delta_d": (0.06746560275350007, 0.06860202525236082),
        "Z": (0.05041926527058864, 0.0515556877694494),
    },
}

BASELINE_MODES = [
    ("2pi", 2.0 * np.pi),
    ("5pi", 5.0 * np.pi),
    ("10pi", 10.0 * np.pi),
]
