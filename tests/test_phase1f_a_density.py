"""Phase 1F-A density inversion, carrier assembly, and dimensional tests."""

from __future__ import annotations

import inspect

import numpy as np
import pytest

from phase1f_a_test_utils import (
    boundary,
    carrier_density,
    density_pair,
    domain,
    make_operator,
    make_realization,
    manufactured_laplacian,
    manufactured_scalar,
    normalization,
    regional_full,
    zero_mode,
)
from timescape_fsigma8.phase1f_a import (
    MATHEMATICAL_OPERATOR_FIXTURE_ONLY,
    NOT_EVALUABLE_WITHOUT_CODOMAIN_ADAPTER,
    Phase1FAContractError,
    Phase1FADegeneracyError,
    Phase1FADimensionalContractError,
    reconstruct_regional_density,
)
from timescape_fsigma8.transfer import ContinuumH1Operator, conformal_regional_geometry


def test_t2_analytic_three_dimensional_regional_density_inversion_multiple_modes() -> None:
    realization = make_realization()
    wall, void, expected = density_pair(realization)
    wall_mask = realization.scientific_state.operator.morphology.wall_domain.reshape(-1)
    void_mask = ~wall_mask
    np.testing.assert_allclose(wall.delta_m[wall_mask], expected.reshape(-1)[wall_mask], atol=2e-12)
    np.testing.assert_allclose(void.delta_m[void_mask], 0.6 * expected.reshape(-1)[void_mask], atol=2e-12)
    assert wall.diagnostics.equation_residual_max_abs <= 2e-10
    assert void.diagnostics.equation_residual_max_abs <= 2e-10
    assert wall.diagnostics.condition_number > 1.0


def test_t3_zero_mode_is_not_identifiable_and_closure_is_required() -> None:
    realization = make_realization()
    shape = realization.scientific_state.operator.carrier.grid_shape
    base = manufactured_scalar(shape)
    shifted = base + 7.25
    source = manufactured_laplacian(shape)
    np.testing.assert_allclose(source, manufactured_laplacian(shape))
    assert np.max(np.abs(base - shifted)) == pytest.approx(7.25)
    with pytest.raises(Phase1FAContractError, match="zero-mode closure"):
        reconstruct_regional_density(
            delta_cgi=regional_full(source, realization, "wall"),
            regional_geometry=domain(realization, "wall"),
            boundary_policy=boundary("wall"),
            zero_mode_closure=None,  # type: ignore[arg-type]
            numerics=realization.numerics,
            provenance="MISSING_CLOSURE_ADVERSARIAL",
        )
    reconstructed = realization.reconstruct_density(
        delta_cgi=regional_full(source, realization, "wall"),
        regional_geometry=domain(realization, "wall"),
        boundary_policy=boundary("wall"),
        zero_mode_closure=zero_mode("wall"),
        provenance="EXPLICIT_ZERO_MODE",
    )
    mask = reconstructed.domain.mask
    np.testing.assert_allclose(reconstructed.delta_m[mask], base.reshape(-1)[mask], atol=2e-12)


def test_t4_explicit_regional_mean_zero_normalization() -> None:
    realization = make_realization()
    wall, void, _ = density_pair(realization)
    assert abs(wall.diagnostics.solution_mean_residual) <= 2e-11
    assert abs(void.diagnostics.solution_mean_residual) <= 2e-11
    assert wall.zero_mode_closure.classification == "EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE"
    assert wall.diagnostics.kernel_dimension_before_normalization == 1


def test_incompatible_regional_source_fails_closed_before_inversion() -> None:
    realization = make_realization()
    source = np.zeros(realization.scientific_state.operator.size)
    source[domain(realization, "wall").mask] = 1.0
    with pytest.raises(Phase1FADegeneracyError, match="constant kernel"):
        realization.reconstruct_density(
            delta_cgi=source,
            regional_geometry=domain(realization, "wall"),
            boundary_policy=boundary("wall"),
            zero_mode_closure=zero_mode("wall"),
            provenance="NONZERO_MEAN_ADVERSARIAL",
        )


def test_t5_unequal_backgrounds_preserve_regional_offset_term() -> None:
    realization = make_realization()
    wall, void, _ = density_pair(realization)
    result = carrier_density(realization)
    wall_mask = realization.scientific_state.operator.morphology.wall_domain.reshape(-1)
    void_mask = ~wall_mask
    expected_wall = (result.b_wall - 1.0) + result.b_wall * wall.delta_m[wall_mask]
    expected_void = (result.b_void - 1.0) + result.b_void * void.delta_m[void_mask]
    np.testing.assert_allclose(result.delta_m_carrier[wall_mask], expected_wall, atol=2e-12)
    np.testing.assert_allclose(result.delta_m_carrier[void_mask], expected_void, atol=2e-12)
    assert result.b_wall == pytest.approx(4.0 / 3.0)
    assert result.b_void == pytest.approx(2.0 / 3.0)
    assert result.delta_m_carrier[wall_mask][0] != pytest.approx(wall.delta_m[wall_mask][0])


def test_t6_carrier_global_mean_and_background_assembly() -> None:
    result = carrier_density(make_realization())
    assert abs(result.diagnostics.global_mean_residual) <= 2e-10
    assert abs(result.diagnostics.background_density_assembly_residual) <= 2e-10
    assert abs(result.diagnostics.carrier_volume_additivity_residual) <= 2e-11
    assert result.rho_bar_carrier == pytest.approx(1.5)


def test_physical_carrier_rejects_nonpositive_regional_density() -> None:
    realization = make_realization()
    shape = realization.scientific_state.operator.carrier.grid_shape
    wall = realization.reconstruct_density(
        delta_cgi=regional_full(2.0 * manufactured_laplacian(shape), realization, "wall"),
        regional_geometry=domain(realization, "wall"),
        boundary_policy=boundary("wall"),
        zero_mode_closure=zero_mode("wall"),
        provenance="NONPOSITIVE_PHYSICAL_DENSITY_ADVERSARIAL",
    )
    void = realization.reconstruct_density(
        delta_cgi=np.zeros(realization.scientific_state.operator.size),
        regional_geometry=domain(realization, "void"),
        boundary_policy=boundary("void"),
        zero_mode_closure=zero_mode("void"),
        provenance="ZERO_VOID_COMPARATOR",
    )
    with pytest.raises(Phase1FAContractError, match="strictly positive"):
        realization.assemble_density(
            wall_density=wall,
            void_density=void,
            wall_background_density=2.0,
            void_background_density=1.0,
            wall_physical_volume=0.5,
            void_physical_volume=0.5,
            h1_partition=realization.scientific_state.operator.morphology,
        )


def test_t7_sharp_physical_density_jump_is_preserved() -> None:
    result = carrier_density(make_realization())
    assert result.diagnostics.maximum_interface_density_jump > 0.1
    source = inspect.getsource(type(result)) + inspect.getsource(carrier_density)
    assert "transmission" not in source.lower()
    assert "smooth" not in source.lower()


def test_t8_broken_intertwining_is_regionwise_and_non_tautological() -> None:
    result = carrier_density(make_realization())
    assert result.diagnostics.wall_intertwining_residual <= 5e-10
    assert result.diagnostics.void_intertwining_residual <= 5e-10
    assert result.diagnostics.frozen_delta_comparison_status == NOT_EVALUABLE_WITHOUT_CODOMAIN_ADAPTER


def test_t9_public_density_path_does_not_use_h1_inverse_transfer_definition() -> None:
    from timescape_fsigma8.phase1f_a import density as density_module

    source = inspect.getsource(density_module)
    forbidden = (
        "ContinuumTransfer(",
        "recover_potential_from_transfer",
        "solve_projected_load",
    )
    assert all(token not in source for token in forbidden)
    assert "apply_regional_laplace_beltrami" in source


@pytest.mark.parametrize("shape", [(8,), (6, 6)])
def test_t10_reduced_dimensional_density_inversion_survives_but_physical_carrier_fails(
    shape: tuple[int, ...],
) -> None:
    realization = make_realization(shape)
    if len(shape) == 1:
        source = np.tile(np.array([1.0, -1.0]), shape[0] // 2)
    else:
        coordinate = np.indices(shape, dtype=float)[-1]
        source = np.sin(2.0 * np.pi * coordinate / shape[-1])
    wall = realization.reconstruct_density(
        delta_cgi=regional_full(source, realization, "wall"),
        regional_geometry=domain(realization, "wall"),
        boundary_policy=boundary("wall"),
        zero_mode_closure=zero_mode("wall"),
        provenance="REDUCED_DIMENSIONAL_OPERATOR_FIXTURE",
    )
    void = realization.reconstruct_density(
        delta_cgi=regional_full(source, realization, "void"),
        regional_geometry=domain(realization, "void"),
        boundary_policy=boundary("void"),
        zero_mode_closure=zero_mode("void"),
        provenance="REDUCED_DIMENSIONAL_OPERATOR_FIXTURE",
    )
    assert wall.scientific_classification == MATHEMATICAL_OPERATOR_FIXTURE_ONLY
    with pytest.raises(Phase1FADimensionalContractError, match="spatial_dimension == 3"):
        realization.assemble_density(
            wall_density=wall,
            void_density=void,
            wall_background_density=2.0,
            void_background_density=1.0,
            wall_physical_volume=0.5,
            void_physical_volume=0.5,
            h1_partition=realization.scientific_state.operator.morphology,
        )


def test_t11_three_dimensional_metric_scale_factor_volume_covariance() -> None:
    base = make_operator()
    c = 2.0
    void_volume = base.void_geometry.normalization.reference_comoving_volume
    scaled_void = conformal_regional_geometry(
        region_id="void",
        conformal_factor=np.full(base.carrier.grid_shape, c),
        dimension=3,
        curvature_class="FLAT_CONSTANT_RESCALING_VALIDATION",
        pullback_provenance="Phi_v_scaled_validation",
        normalization=normalization(identity="void-scaled-c2", volume=c**3 * void_volume),
        metadata={"classification": "PHYSICAL_NORMALIZATION_COVARIANCE"},
    )
    transformed = ContinuumH1Operator(
        carrier=base.carrier,
        morphology=base.morphology,
        wall_geometry=base.wall_geometry,
        void_geometry=scaled_void,
        branch=base.branch,
        configuration=base.configuration,
        continuum_coercivity_bound=0.1,
    )
    base_volumes = base.physical_regional_volumes(a_w=1.0, a_v=1.0)
    transformed_volumes = transformed.physical_regional_volumes(a_w=1.0, a_v=1.0 / c)
    assert transformed_volumes == pytest.approx(base_volumes)
    assert scaled_void.metadata["classification"] == "PHYSICAL_NORMALIZATION_COVARIANCE"
