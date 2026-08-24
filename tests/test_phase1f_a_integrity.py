"""Phase 1F-A post-construction integrity and scientific firewall tests."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import inspect

import numpy as np
import pytest

from phase1f_a_test_utils import (
    boundary,
    carrier_density,
    domain,
    make_operator,
    make_realization,
    manufactured_laplacian,
    regional_full,
    zero_mode,
)
import timescape_fsigma8.phase1f_a as phase1f_a
from timescape_fsigma8.phase1f_a import (
    EXTERNAL_CLOSURE,
    SYNTHETIC_VALIDATION_ONLY,
    DressedSpacetimeMapClosure,
    ExternalBoostDivergenceClosure,
    Phase1FAStateIntegrityError,
)
from timescape_fsigma8.perturbations.barotropic import D3Branch


def boost_closure(realization) -> ExternalBoostDivergenceClosure:
    shape = realization.scientific_state.operator.carrier.grid_shape
    return ExternalBoostDivergenceClosure(
        divergence=regional_full(
            0.1 * manufactured_laplacian(shape), realization, "wall"
        ),
        source_frame="VOLUME_AVERAGE_DUST_FRAME",
        destination_frame="WALL_FRAME_THEORETICAL_REFERENCE",
        time_coordinate="t_D",
        spatial_metric_identity="wall-normalization",
        units="INVERSE_COMMON_TIME",
        domain="wall",
        normalization_closure_id=zero_mode("wall").provenance,
        provenance="INTEGRITY_BOOST_CLOSURE",
        classification=EXTERNAL_CLOSURE,
    )


def dressed_closure(size: int) -> DressedSpacetimeMapClosure:
    return DressedSpacetimeMapClosure(
        source_frame="H1_PHYSICAL_CARRIER_DENSITY_FRAME",
        destination_frame="SYNTHETIC_DRESSED_VALIDATION_FRAME",
        time_mapping="IDENTITY_VALIDATION_TIME",
        spatial_mapping="IDENTITY_VALIDATION_PULLBACK",
        destination_spatial_metric="SYNTHETIC_FLAT_DESTINATION",
        destination_source_indices=np.arange(size),
        destination_reference_weights=np.full(size, 1.0 / size),
        destination_metric_volume_ratio=np.ones(size),
        destination_measure_jacobian=np.ones(size),
        provenance="SYNTHETIC_DRESSED_INTEGRITY_FIXTURE",
        scientific_classification=SYNTHETIC_VALIDATION_ONLY,
        spatial_dimension=3,
    )


def test_t24_geometry_and_classification_mutation_is_rejected_or_detected() -> None:
    realization = make_realization()
    with pytest.raises(FrozenInstanceError):
        realization.scientific_state.operator = make_operator()  # type: ignore[misc]
    object.__setattr__(realization.scientific_state, "operator", make_operator())
    with pytest.raises(Phase1FAStateIntegrityError, match="validated construction"):
        realization.validate_integrity()


def test_t24_masks_and_operator_arrays_remain_phase1e_g_integrity_protected() -> None:
    realization = make_realization()
    with pytest.raises(ValueError, match="read-only"):
        realization.scientific_state.operator.morphology.wall_domain.flat[0] = False
    realization.scientific_state.operator._stiffness.data[0] += 1.0
    with pytest.raises(Exception, match="validated assembly"):
        realization.validate_integrity()


def test_t24_carrier_volume_and_density_result_tamper_is_detected() -> None:
    realization = make_realization()
    carrier = carrier_density(realization)
    object.__setattr__(carrier, "wall_physical_volume", 0.25)
    with pytest.raises(Phase1FAStateIntegrityError, match="validated construction"):
        realization.map_dressed_density(
            carrier_density=carrier,
            dressed_map_closure=dressed_closure(carrier.rho_carrier.size),
        )


def test_t24_boost_closure_mutation_is_detected_before_use() -> None:
    realization = make_realization()
    closure = boost_closure(realization)
    changed = np.array(closure.divergence, copy=True)
    changed[0] += 1.0
    object.__setattr__(closure, "divergence", changed)
    with pytest.raises(Phase1FAStateIntegrityError, match="validated construction"):
        realization.reconstruct_boost(
            regional_or_wall_geometry=domain(realization, "wall"),
            boost_closure=closure,
            boundary_policy=boundary("wall"),
            zero_mode_closure=zero_mode("wall"),
        )


def test_t24_dressed_closure_mutation_is_detected_before_use() -> None:
    realization = make_realization()
    carrier = carrier_density(realization)
    closure = dressed_closure(carrier.rho_carrier.size)
    object.__setattr__(closure, "destination_frame", "MUTATED_FRAME")
    with pytest.raises(Phase1FAStateIntegrityError, match="validated construction"):
        realization.map_dressed_density(
            carrier_density=carrier,
            dressed_map_closure=closure,
        )


def test_t24_nested_arrays_are_defensive_read_only_copies() -> None:
    realization = make_realization()
    closure = boost_closure(realization)
    with pytest.raises(ValueError, match="read-only"):
        closure.divergence.flat[0] = 4.0
    carrier = carrier_density(realization)
    with pytest.raises(ValueError, match="read-only"):
        carrier.rho_carrier.flat[0] = 0.0


def test_t25_public_firewall_has_no_forbidden_scientific_surface() -> None:
    public = {name.lower() for name in phase1f_a.__all__}
    forbidden = {
        "sigma8", "sigma_8", "sigmar", "sigma_r", "fsigma8", "f_sigma_8",
        "rsd", "kaiser", "galaxy_bias", "tracer_velocity", "likelihood",
        "covariance", "observational_dataset", "zeroBoostClosure".lower(),
    }
    assert public.isdisjoint(forbidden)
    assert "s1" not in public
    assert not hasattr(phase1f_a, "ZeroBoostClosure")


def test_d3_branches_remain_explicit_and_have_no_default() -> None:
    assert D3Branch.PRINTED_4_15.value == "printed_4_15"
    assert D3Branch.DERIVED_4_10.value == "derived_4_10"
    from timescape_fsigma8.perturbations.barotropic import barotropic_matrix

    signature = inspect.signature(barotropic_matrix)
    assert signature.parameters["branch"].default is inspect.Parameter.empty
