"""Phase 1F-A explicit dressed-spacetime density-map gating tests."""

# A06: absolute budgets use rtol=0; relative budgets use atol=0.
# Previously implicit algebraic comparisons use rtol=2e-12, atol=1e-14
# in the fixture units (roundoff allowance); explicit convergence budgets remain.

from __future__ import annotations

import inspect

import numpy as np
import pytest

from phase1f_a_test_utils import carrier_density, make_realization
from timescape_fsigma8.phase1f_a import (
    SYNTHETIC_VALIDATION_ONLY,
    DressedSpacetimeMapClosure,
    Phase1FAContractError,
    map_carrier_density_to_dressed,
)


def synthetic_map(size: int) -> DressedSpacetimeMapClosure:
    indices = np.arange(size - 1, -1, -1)
    weights = np.full(size, 1.0 / size)
    ratio = np.linspace(0.8, 1.2, size)
    jacobian = np.linspace(1.1, 0.9, size)
    return DressedSpacetimeMapClosure(
        source_frame="H1_PHYSICAL_CARRIER_DENSITY_FRAME",
        destination_frame="SYNTHETIC_DRESSED_VALIDATION_FRAME",
        time_mapping="IDENTITY_COMMON_TIME_VALIDATION_ONLY",
        spatial_mapping="EXPLICIT_REVERSE_INDEX_PULLBACK_VALIDATION_ONLY",
        destination_spatial_metric="SYNTHETIC_POSITIVE_DIAGONAL_METRIC",
        destination_source_indices=indices,
        destination_reference_weights=weights,
        destination_metric_volume_ratio=ratio,
        destination_measure_jacobian=jacobian,
        provenance="SYNTHETIC_DRESSED_MAP_VALIDATION_ONLY",
        scientific_classification=SYNTHETIC_VALIDATION_ONLY,
        spatial_dimension=3,
    )


def test_t22_dressed_density_requires_explicit_map_closure() -> None:
    realization = make_realization()
    carrier = carrier_density(realization)
    signature = inspect.signature(map_carrier_density_to_dressed)
    assert signature.parameters["dressed_map_closure"].default is inspect.Parameter.empty
    with pytest.raises(Phase1FAContractError, match="explicit dressed"):
        map_carrier_density_to_dressed(
            carrier_density=carrier,
            dressed_map_closure=None,  # type: ignore[arg-type]
            numerics=realization.numerics,
        )


def test_t23_density_is_mapped_before_destination_mean_is_recomputed() -> None:
    realization = make_realization()
    carrier = carrier_density(realization)
    closure = synthetic_map(carrier.rho_carrier.size)
    result = realization.map_dressed_density(
        carrier_density=carrier,
        dressed_map_closure=closure,
    )
    expected_rho = carrier.rho_carrier[closure.destination_source_indices]
    measure = (
        closure.destination_reference_weights
        * closure.destination_metric_volume_ratio
        * closure.destination_measure_jacobian
    )
    expected_mean = np.dot(measure, expected_rho) / np.sum(measure)
    np.testing.assert_allclose(result.rho_dressed, expected_rho, rtol=2e-12, atol=1e-14)
    assert result.rho_bar_dressed == pytest.approx(expected_mean, rel=2e-12, abs=1e-14)
    np.testing.assert_allclose(result.delta_m_dressed, expected_rho / expected_mean - 1.0, rtol=2e-12, atol=1e-14)
    assert abs(result.destination_mean_residual) <= realization.numerics.dressed_mean_tolerance
    assert result.map_classification == SYNTHETIC_VALIDATION_ONLY
    direct_delta_pullback = carrier.delta_m_carrier[closure.destination_source_indices]
    assert np.max(np.abs(result.delta_m_dressed - direct_delta_pullback)) > 1e-5


def test_dressed_map_frame_mismatch_fails_closed() -> None:
    realization = make_realization()
    carrier = carrier_density(realization)
    closure = synthetic_map(carrier.rho_carrier.size)
    wrong = DressedSpacetimeMapClosure(
        source_frame="UNRELATED_FRAME",
        destination_frame=closure.destination_frame,
        time_mapping=closure.time_mapping,
        spatial_mapping=closure.spatial_mapping,
        destination_spatial_metric=closure.destination_spatial_metric,
        destination_source_indices=closure.destination_source_indices,
        destination_reference_weights=closure.destination_reference_weights,
        destination_metric_volume_ratio=closure.destination_metric_volume_ratio,
        destination_measure_jacobian=closure.destination_measure_jacobian,
        provenance=closure.provenance,
        scientific_classification=closure.scientific_classification,
        spatial_dimension=3,
    )
    with pytest.raises(Phase1FAContractError, match="source frame"):
        realization.map_dressed_density(carrier_density=carrier, dressed_map_closure=wrong)
