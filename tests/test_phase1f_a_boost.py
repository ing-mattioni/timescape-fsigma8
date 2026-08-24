"""Phase 1F-A explicit longitudinal dust-to-wall boost tests."""

from __future__ import annotations

import inspect

import numpy as np
import pytest

from phase1f_a_test_utils import (
    boundary,
    domain,
    make_realization,
    manufactured_laplacian,
    manufactured_scalar,
    regional_full,
    zero_mode,
)
import timescape_fsigma8.phase1f_a as phase1f_a
from timescape_fsigma8.phase1f_a import (
    EXTERNAL_CLOSURE,
    TRANSVERSE_SECTOR_UNRESOLVED,
    ExternalBoostDivergenceClosure,
    ExternalBoostPotentialClosure,
    Phase1FAContractError,
    Phase1FADegeneracyError,
    reconstruct_longitudinal_relative_velocity,
)


def divergence_closure(realization, values: np.ndarray) -> ExternalBoostDivergenceClosure:
    return ExternalBoostDivergenceClosure(
        divergence=values,
        source_frame="VOLUME_AVERAGE_DUST_FRAME",
        destination_frame="WALL_FRAME_THEORETICAL_REFERENCE",
        time_coordinate="t_D",
        spatial_metric_identity="wall-normalization",
        units="INVERSE_COMMON_TIME",
        domain="wall",
        normalization_closure_id=zero_mode("wall").provenance,
        provenance="EXTERNAL_MANUFACTURED_LONGITUDINAL_BOOST",
        classification=EXTERNAL_CLOSURE,
    )


def test_t18_external_boost_divergence_reconstructs_potential_and_longitudinal_field() -> None:
    realization = make_realization()
    shape = realization.scientific_state.operator.carrier.grid_shape
    potential = 0.2 * manufactured_scalar(shape)
    divergence = 0.2 * manufactured_laplacian(shape)
    result = realization.reconstruct_boost(
        regional_or_wall_geometry=domain(realization, "wall"),
        boost_closure=divergence_closure(
            realization, regional_full(divergence, realization, "wall")
        ),
        boundary_policy=boundary("wall"),
        zero_mode_closure=zero_mode("wall"),
    )
    mask = result.domain.mask
    np.testing.assert_allclose(result.scalar_potential[mask], potential.reshape(-1)[mask], atol=2e-12)
    np.testing.assert_allclose(
        result.reconstructed_divergence[mask], divergence.reshape(-1)[mask], atol=2e-10
    )
    assert result.boost_residual_max_abs <= 2e-10
    assert result.longitudinal_relative_dust_to_wall_velocity.shape == (
        realization.scientific_state.operator.size,
        3,
    )


def test_t19_incompatible_boost_divergence_fails_closed() -> None:
    realization = make_realization()
    source = np.zeros(realization.scientific_state.operator.size)
    source[domain(realization, "wall").mask] = 1.0
    with pytest.raises(Phase1FADegeneracyError, match="constant kernel"):
        realization.reconstruct_boost(
            regional_or_wall_geometry=domain(realization, "wall"),
            boost_closure=divergence_closure(realization, source),
            boundary_policy=boundary("wall"),
            zero_mode_closure=zero_mode("wall"),
        )


def test_t20_no_zero_boost_class_and_no_implicit_default() -> None:
    assert not hasattr(phase1f_a, "ZeroBoostClosure")
    signature = inspect.signature(reconstruct_longitudinal_relative_velocity)
    assert signature.parameters["boost_closure"].default is inspect.Parameter.empty
    realization = make_realization()
    with pytest.raises(Phase1FAContractError, match="explicit boost closure"):
        reconstruct_longitudinal_relative_velocity(
            regional_or_wall_geometry=domain(realization, "wall"),
            boost_closure=None,  # type: ignore[arg-type]
            boundary_policy=boundary("wall"),
            zero_mode_closure=zero_mode("wall"),
            numerics=realization.numerics,
        )


def test_t21_transverse_ambiguity_remains_explicit() -> None:
    realization = make_realization()
    shape = realization.scientific_state.operator.carrier.grid_shape
    divergence = regional_full(0.2 * manufactured_laplacian(shape), realization, "wall")
    result = realization.reconstruct_boost(
        regional_or_wall_geometry=domain(realization, "wall"),
        boost_closure=divergence_closure(realization, divergence),
        boundary_policy=boundary("wall"),
        zero_mode_closure=zero_mode("wall"),
    )
    coordinates = np.indices(shape, dtype=float)
    transverse = np.zeros((np.prod(shape), 3))
    transverse[:, 1] = np.sin(2.0 * np.pi * coordinates[0].reshape(-1) / shape[0])
    # d/dy of a y-component depending only on x is zero: the divergence data
    # cannot distinguish v_L from v_L+v_T.
    assert np.max(np.abs(transverse[:, 1])) > 0.0
    assert result.transverse_sector_status == TRANSVERSE_SECTOR_UNRESOLVED


def test_external_potential_closure_is_validated_against_metric_and_normalization() -> None:
    realization = make_realization()
    shape = realization.scientific_state.operator.carrier.grid_shape
    potential = regional_full(0.2 * manufactured_scalar(shape), realization, "wall")
    closure = ExternalBoostPotentialClosure(
        potential=potential,
        source_frame="VOLUME_AVERAGE_DUST_FRAME",
        destination_frame="WALL_FRAME_THEORETICAL_REFERENCE",
        time_coordinate="t_D",
        spatial_metric_identity="wall-normalization",
        units="REFERENCE_LENGTH_PER_COMMON_TIME",
        domain="wall",
        normalization_closure_id=zero_mode("wall").provenance,
        provenance="EXTERNAL_MANUFACTURED_POTENTIAL",
        classification=EXTERNAL_CLOSURE,
    )
    result = realization.reconstruct_boost(
        regional_or_wall_geometry=domain(realization, "wall"),
        boost_closure=closure,
        boundary_policy=boundary("wall"),
        zero_mode_closure=zero_mode("wall"),
    )
    assert result.closure_kind == "EXTERNAL_SCALAR_VELOCITY_POTENTIAL"
    wrong_metric = ExternalBoostPotentialClosure(
        potential=potential,
        source_frame=closure.source_frame,
        destination_frame=closure.destination_frame,
        time_coordinate=closure.time_coordinate,
        spatial_metric_identity="unrelated-metric",
        units=closure.units,
        domain=closure.domain,
        normalization_closure_id=closure.normalization_closure_id,
        provenance=closure.provenance,
        classification=closure.classification,
    )
    with pytest.raises(Phase1FAContractError, match="metric identity"):
        realization.reconstruct_boost(
            regional_or_wall_geometry=domain(realization, "wall"),
            boost_closure=wrong_metric,
            boundary_policy=boundary("wall"),
            zero_mode_closure=zero_mode("wall"),
        )
