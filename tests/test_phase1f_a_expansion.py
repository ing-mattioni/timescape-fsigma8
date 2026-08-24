"""Phase 1F-A regional expansion-scalar reconstruction tests."""

from __future__ import annotations

import inspect

import numpy as np

from phase1f_a_test_utils import (
    boundary,
    domain,
    make_realization,
    manufactured_laplacian,
    manufactured_scalar,
    regional_full,
    zero_mode,
)
from timescape_fsigma8.phase1f_a import (
    DUST_EXPANSION_FIELD_RECONSTRUCTED_CONDITIONALLY,
    RegionalExpansionReconstruction,
)


def test_t12_manufactured_regional_expansion_inversion() -> None:
    realization = make_realization()
    shape = realization.scientific_state.operator.carrier.grid_shape
    expected = 0.35 * manufactured_scalar(shape)
    source = 0.35 * manufactured_laplacian(shape)
    result = realization.reconstruct_expansion(
        z_cgi=regional_full(source, realization, "wall"),
        regional_geometry=domain(realization, "wall"),
        boundary_policy=boundary("wall"),
        zero_mode_closure=zero_mode("wall"),
        background_expansion_identity="bar_Theta_w=3H_w",
        provenance="MANUFACTURED_EXPANSION_SCALAR",
    )
    mask = result.domain.mask
    np.testing.assert_allclose(result.delta_theta[mask], expected.reshape(-1)[mask], atol=2e-12)
    assert result.diagnostics.equation_residual_max_abs <= 2e-10
    assert result.scientific_classification == DUST_EXPANSION_FIELD_RECONSTRUCTED_CONDITIONALLY


def test_t13_expansion_result_has_no_velocity_alias() -> None:
    public_fields = set(RegionalExpansionReconstruction.__dataclass_fields__)
    forbidden = {"velocity", "peculiar_velocity", "velocity_divergence", "tracer_velocity"}
    assert not (public_fields & forbidden)
    source = inspect.getsource(RegionalExpansionReconstruction)
    assert "not a velocity" in source.lower()
