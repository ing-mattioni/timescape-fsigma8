"""V1--V34 validation of the conditional Phase 1E-G continuum H1 runtime.

The structured fixtures are numerical reference discretisations, not claims
about a unique physical Timescape morphology.  CGI/GM equations exercised by
the downstream evaluator retain their cited paper equations in the Phase
1E-F implementation.  New weak-form equations are the human-approved Phase
1E-G model-extension specification and have no paper equation number.
"""

from __future__ import annotations

from dataclasses import fields, replace
import inspect
from pathlib import Path

import numpy as np
import pytest

import timescape_fsigma8.transfer as transfer
from timescape_fsigma8.transfer import (
    CARRIER_PHYSICAL_STATUS,
    COMMON_REFERENCE_NORMAL_WALL_TO_VOID_1E_G,
    CONVERGED_EQUAL_GEOMETRY_MASK_PLACEMENT_DIAGNOSTIC,
    DERIVED_FROM_NORMALIZED_METRIC,
    EXTERNALLY_SUPPLIED_REFERENCE_VOLUME,
    FIXED_REFERENCE_BRANCH,
    INTERFACE_PHYSICAL_STATUS,
    MORPHOLOGY_NORM_TARGET_METRIC_L2,
    PHYSICAL_NORMALIZATION_COVARIANCE,
    PHYSICAL_VOLUME_SEMANTICS,
    REDUCED_DIMENSIONAL_MEASURE_ONLY,
    ContinuumCarrierSpec,
    ContinuumContractError,
    ContinuumDegeneracyError,
    ContinuumDimensionalContractError,
    ContinuumEllipticClosureConfig,
    ContinuumH1Operator,
    ContinuumPhase1EBackendAdapter,
    ContinuumTransfer,
    EffectiveSectorContinuumBridge,
    FixedReferenceBranchSpec,
    H1Background,
    H1ClosureError,
    H1Configuration,
    H1DegeneracyError,
    MorphologySpec,
    RegionalBulkState,
    RegionalGeometrySpec,
    RegionalMetricNormalization,
    ScalarJet,
    VectorJet,
    conformal_regional_geometry,
    flat_regional_geometry,
    island_morphology,
    layered_morphology,
    require_no_generic_spectral_label,
    target_metric_weighted_l2_difference,
    two_region_coefficients,
)


def scalar(value: float, first: float = 0.0, second: float = 0.0) -> ScalarJet:
    return ScalarJet(value, first, second)


ZERO = scalar(0.0)


def downstream_configuration(**changes: float) -> H1Configuration:
    values = {
        "A_P_min": 1e-8,
        "effective_denominator_min": 1e-8,
        "coercivity_min": 5e-2,
        "partition_product_min": 1e-8,
        "rho_d_min": 1e-8,
        "C_P_tolerance": 1e-10,
        "R_Delta_tolerance": 1e-10,
        "R_Z_tolerance": 1e-10,
        "R_eff_tolerance": 1e-10,
        "K_GM_tolerance": 1e-10,
        "transmission_value_tolerance": 1e-10,
        "transmission_flux_tolerance": 1e-10,
        "source_roundtrip_tolerance": 1e-10,
        "background_identity_tolerance": 2e-12,
    }
    values.update(changes)
    return H1Configuration(**values)


def continuum_configuration(**changes: object) -> ContinuumEllipticClosureConfig:
    values: dict[str, object] = {
        "ellipticity_min": 1e-6,
        "coercivity_min": 5e-2,
        "source_compatibility_tolerance": 2e-11,
        "global_mean_tolerance": 2e-11,
        "interface_value_tolerance": 2e-11,
        "interface_flux_tolerance": 2e-11,
        "volume_fraction_tolerance": 2e-11,
        "equal_geometry_identity_tolerance": 2e-10,
        "convergence_l2_min_rate": 1.8,
        "convergence_energy_min_rate": 0.8,
        "morphology_sensitivity_norm": MORPHOLOGY_NORM_TARGET_METRIC_L2,
        "morphology_sensitivity_reference_scale": 1.0,
        "morphology_sensitivity_floor": 1e-12,
        "morphology_convergence_tolerance": 2e-2,
        "kernel_tolerance": 1e-10,
        "symmetry_tolerance": 1e-12,
        "downstream_configuration": downstream_configuration(),
    }
    values.update(changes)
    return ContinuumEllipticClosureConfig(**values)


def fixed_branch(**changes: object) -> FixedReferenceBranchSpec:
    values: dict[str, object] = {
        "branch_id": FIXED_REFERENCE_BRANCH,
        "fixed_reference_partition": True,
        "fixed_interface": True,
        "fixed_comoving_pullback_geometries": True,
        "fixed_target_scalarization": True,
        "homogeneous_background_clock_map": True,
        "spatial_clock_perturbation": False,
    }
    values.update(changes)
    return FixedReferenceBranchSpec(**values)


def make_background(*, f_v: float = 0.5, **changes: ScalarJet | float) -> H1Background:
    values: dict[str, ScalarJet | float] = {
        "f_v": scalar(f_v),
        "rho_w": scalar(1.0),
        "rho_v": scalar(1.0),
        "Theta_w": ZERO,
        "Theta_v": ZERO,
        "H_w": ZERO,
        "H_v": ZERO,
        "alpha_w": scalar(1.0),
        "alpha_v": scalar(1.0),
        "R_bar_w": ZERO,
        "R_bar_v": scalar(2.0),
        "Q_bar": scalar(1.0),
        "W_bar": scalar(-3.0),
        "Theta": ZERO,
        "Xi_w": ZERO,
        "Xi_v": ZERO,
        "G": 1.0,
    }
    values.update(changes)
    return H1Background(**values)


def metric_normalization(
    *,
    normalization_id: str,
    reference_comoving_volume: float,
    scale_factor_reference_value: float = 1.0,
    metric_scale_convention: str = "UNIT_REFERENCE_COMOVING_METRIC",
    volume_provenance: str = DERIVED_FROM_NORMALIZED_METRIC,
    consistency_tolerance: float = 2e-12,
) -> RegionalMetricNormalization:
    return RegionalMetricNormalization(
        normalization_id=normalization_id,
        scale_factor_reference_epoch="REFERENCE_EPOCH_T_I",
        scale_factor_reference_value=scale_factor_reference_value,
        metric_scale_convention=metric_scale_convention,
        reference_comoving_volume=reference_comoving_volume,
        volume_provenance=volume_provenance,
        consistency_tolerance=consistency_tolerance,
    )


def metric_domain_volume(
    metric_volume_ratio: np.ndarray,
    domain: np.ndarray,
) -> float:
    weights = np.full(metric_volume_ratio.shape, 1.0 / metric_volume_ratio.size)
    return float(np.sum(weights * metric_volume_ratio * domain))


def make_operator(
    *,
    shape: tuple[int, ...] = (8,),
    morphology: MorphologySpec | None = None,
    wall_geometry: RegionalGeometrySpec | None = None,
    void_geometry: RegionalGeometrySpec | None = None,
    target_geometry: RegionalGeometrySpec | None = None,
    configuration: ContinuumEllipticClosureConfig | None = None,
    branch: FixedReferenceBranchSpec | None = None,
) -> ContinuumH1Operator:
    dimension = len(shape)
    weights = np.full(shape, 1.0 / np.prod(shape))
    if morphology is None:
        morphology = layered_morphology(
            morphology_id="layered-reference",
            grid_shape=shape,
            axis=0,
            wall_cell_count=shape[0] // 2,
            wall_pullback_id="Phi_w_identity",
            void_pullback_id="Phi_v_identity",
        )
    target = target_geometry or flat_regional_geometry(
        region_id="target",
        grid_shape=shape,
        pullback_provenance="identity-target-map",
        normalization=metric_normalization(
            normalization_id="target-unit-flat",
            reference_comoving_volume=1.0,
        ),
        metadata={"geometry": "flat periodic target", "K_D": "0"},
    )
    carrier = ContinuumCarrierSpec(
        dimension=dimension,
        grid_shape=shape,
        periodicity=(True,) * dimension,
        reference_measure_weights=weights,
        grid_spacing=tuple(1.0 / n for n in shape),
        target_geometry=target,
        topology="PERIODIC_REFERENCE_TORUS",
        physical_status=CARRIER_PHYSICAL_STATUS,
        target_scalarization_id="L_D_FLAT_PERIODIC_REFERENCE",
    )
    wall = wall_geometry or flat_regional_geometry(
        region_id="wall",
        grid_shape=shape,
        pullback_provenance=morphology.wall_pullback_id,
        normalization=metric_normalization(
            normalization_id=f"{morphology.morphology_id}:wall-unit-flat",
            reference_comoving_volume=float(
                np.sum(weights * morphology.wall_domain)
            ),
        ),
        metadata={"geometry": "flat wall comoving reference"},
    )
    void = void_geometry or flat_regional_geometry(
        region_id="void",
        grid_shape=shape,
        pullback_provenance=morphology.void_pullback_id,
        normalization=metric_normalization(
            normalization_id=f"{morphology.morphology_id}:void-unit-flat",
            reference_comoving_volume=float(
                np.sum(weights * morphology.void_domain)
            ),
        ),
        metadata={"geometry": "flat comparator void comoving reference"},
    )
    return ContinuumH1Operator(
        carrier=carrier,
        morphology=morphology,
        wall_geometry=wall,
        void_geometry=void,
        branch=branch or fixed_branch(),
        configuration=configuration or continuum_configuration(),
        continuum_coercivity_bound=0.1,
    )


def make_bridge(**operator_changes: object) -> EffectiveSectorContinuumBridge:
    operator = make_operator(**operator_changes)
    return EffectiveSectorContinuumBridge(
        operator=operator,
        branch=operator.branch,
        configuration=operator.configuration,
    )


def make_result(
    *,
    bridge: EffectiveSectorContinuumBridge | None = None,
    background: H1Background | None = None,
    regional_bulk: RegionalBulkState | None = None,
    a_w: float = 1.0,
    a_v: float = 1.0,
    equal_probe: np.ndarray | None = None,
):
    # Full continuum-to-Phase-1E-F evaluation has physical three-volume
    # semantics and therefore uses an explicit d=3 fixture. Reduced-dimensional
    # operator fixtures use ContinuumTransfer directly below.
    selected = bridge or make_bridge(shape=(4, 3, 3))
    return selected.evaluate(
        regional_bulk=regional_bulk or RegionalBulkState(0.0, 1.0, 0.0, 2.0),
        background=background or make_background(),
        a_w=a_w,
        a_v=a_v,
        equal_geometry_probe=equal_probe,
        volume_fraction_consistency_classification=(
            "MANUFACTURED_BACKGROUND_CONSISTENCY_FIXTURE"
        ),
        morphology_sensitivity_diagnostics={},
        discretization_convergence_metrics={},
    )


def test_v1_flat_wall_operator_reproduces_periodic_scalarization() -> None:
    operator = make_operator(shape=(16,))
    x = np.arange(16) / 16.0
    field = np.sin(2.0 * np.pi * x)
    expected_eigenvalue = 4.0 * np.sin(np.pi / 16.0) ** 2 / (1.0 / 16.0) ** 2
    discrete_minus_laplacian = (
        operator.stiffness_matrix @ field
    ) / operator.reference_weights
    np.testing.assert_allclose(
        discrete_minus_laplacian,
        expected_eigenvalue * field,
        atol=2e-12,
    )


def test_dimension_agnostic_api_constructs_a_three_dimensional_carrier() -> None:
    operator = make_operator(shape=(3, 3, 3))
    assert operator.carrier.dimension == 3
    assert operator.size == 27
    response = ContinuumTransfer(operator).transfer_source(
        np.arange(27.0), region='global', provenance='three-dimensional-api'
    )
    assert response.transferred_field.shape == (27,)


def test_v2_negative_curvature_poincare_metric_is_spd_and_weighted() -> None:
    shape = (8, 8)
    coordinates = np.indices(shape, dtype=float)
    x = (coordinates[0] + 0.5) / shape[0] - 0.5
    y = (coordinates[1] + 0.5) / shape[1] - 0.5
    radius_squared = x**2 + y**2
    conformal_factor = 2.0 / (1.0 - radius_squared)
    void_mask = np.indices(shape)[0] >= shape[0] // 2
    void = conformal_regional_geometry(
        region_id="void",
        conformal_factor=conformal_factor,
        dimension=2,
        curvature_class="POINCARE_DISK_GAUSSIAN_CURVATURE_MINUS_ONE",
        pullback_provenance="Phi_v_poincare_patch",
        normalization=metric_normalization(
            normalization_id="poincare-void-normalization",
            reference_comoving_volume=metric_domain_volume(
                conformal_factor**2, void_mask
            ),
            metric_scale_convention="POINCARE_PATCH_CONFORMAL_SCALE",
        ),
        metadata={
            "derivation": "ds^2=4(dx^2+dy^2)/(1-r^2)^2 has Gaussian curvature -1"
        },
    )
    assert np.ptp(void.metric_volume_ratio) > 0.1
    np.testing.assert_allclose(void.elliptic_tensor_density[..., 0, 0], 1.0)
    np.testing.assert_allclose(void.elliptic_tensor_density[..., 1, 1], 1.0)
    assert void.inverse_metric_eigenvalue_bounds[0] > 0.0
    operator = make_operator(shape=shape, void_geometry=void)
    source = np.ones(np.prod(shape))
    correct = operator.source_load(source, region="void")
    wrong = (
        operator.reference_weights
        * source
        * operator.morphology.void_domain.reshape(-1)
    )
    assert np.max(np.abs(correct - wrong)) > 1e-4


def test_v3_single_global_kernel_before_normalization() -> None:
    operator = make_operator()
    assert operator.global_kernel_dimension == 1
    np.testing.assert_allclose(
        operator.stiffness_matrix @ np.ones(operator.size), 0.0, atol=1e-13
    )


def test_v4_no_independent_regional_constant_projection() -> None:
    operator = make_operator()
    raw = operator.source_load(np.ones(operator.size), region="wall")
    projected, _ = operator.project_dual_source(raw)
    wall = operator.morphology.wall_domain.reshape(-1)
    void = operator.morphology.void_domain.reshape(-1)
    assert np.sum(projected[wall]) != pytest.approx(0.0, abs=1e-13)
    assert np.sum(projected[void]) != pytest.approx(0.0, abs=1e-13)
    assert np.sum(projected) == pytest.approx(0.0, abs=1e-13)


def test_v5_one_global_normalization_removes_the_common_constant() -> None:
    response = ContinuumTransfer(make_operator()).transfer_source(
        np.arange(8.0), region="global", provenance="normalization"
    )
    assert response.solution_global_mean == pytest.approx(0.0, abs=2e-11)


def test_v6_explicit_geometric_ellipticity_bounds() -> None:
    operator = make_operator()
    assert operator.ellipticity_lower_bound == pytest.approx(1.0)
    assert operator.ellipticity_upper_bound == pytest.approx(1.0)
    assert operator.ellipticity_lower_bound >= operator.configuration.ellipticity_min


def test_v7_ordinary_generalized_and_continuum_coercivity_are_distinct() -> None:
    operator = make_operator()
    assert operator.ordinary_euclidean_constrained_stiffness_eigenvalue > 0.0
    assert operator.generalized_mass_weighted_laplacian_eigenvalue > 0.0
    assert operator.continuum_coercivity_assumption == pytest.approx(0.1)
    assert operator.ordinary_euclidean_constrained_stiffness_eigenvalue != pytest.approx(
        operator.continuum_coercivity_assumption
    )
    assert operator.generalized_mass_weighted_laplacian_eigenvalue != pytest.approx(
        operator.ordinary_euclidean_constrained_stiffness_eigenvalue
    )


def test_v8_v9_value_and_common_normal_flux_continuity() -> None:
    response = ContinuumTransfer(make_operator()).transfer_source(
        np.arange(8.0), region="wall", provenance="interface"
    )
    assert response.interface.maximum_value_jump <= 2e-11
    assert response.interface.maximum_flux_jump <= 2e-11
    np.testing.assert_allclose(
        response.interface.wall_outward_flux
        + response.interface.void_outward_flux,
        0.0,
        atol=2e-11,
    )


def test_v10_flux_sign_and_trace_adversarial_diagnostics() -> None:
    value, flux = ContinuumH1Operator.explicit_trace_residuals(
        wall_trace=np.array([1.0]),
        void_trace=np.array([1.0]),
        wall_common_flux=np.array([2.0]),
        void_common_flux=np.array([2.0]),
        normal_convention=COMMON_REFERENCE_NORMAL_WALL_TO_VOID_1E_G,
    )
    np.testing.assert_array_equal(value, 0.0)
    np.testing.assert_array_equal(flux, 0.0)
    _, reversed_flux = ContinuumH1Operator.explicit_trace_residuals(
        wall_trace=np.array([1.0]),
        void_trace=np.array([1.0]),
        wall_common_flux=np.array([2.0]),
        void_common_flux=np.array([-2.0]),
        normal_convention=COMMON_REFERENCE_NORMAL_WALL_TO_VOID_1E_G,
    )
    assert reversed_flux[0] == pytest.approx(4.0)


def test_v11_dual_source_compatibility_records_before_and_after() -> None:
    response = ContinuumTransfer(make_operator()).transfer_source(
        np.ones(8), region="wall", provenance="source-projection"
    )
    assert abs(response.source_projection.mean_before_projection) > 0.1
    assert response.source_projection.mean_after_projection == pytest.approx(
        0.0, abs=2e-11
    )


def test_v12_constrained_provenance_roundtrip_recovers_projected_load() -> None:
    response = ContinuumTransfer(make_operator()).transfer_source(
        np.linspace(-1.0, 2.0, 8), region="void", provenance="roundtrip"
    )
    recovered = -make_operator().apply_weak_operator(response.potential)
    np.testing.assert_allclose(recovered, response.projected_source_load, atol=2e-11)
    assert response.provenance_roundtrip_error <= 1e-10


def test_v13_equal_geometry_transfer_identity_exercises_full_backend() -> None:
    bridge = make_bridge(shape=(16,))
    source = np.sin(2.0 * np.pi * np.arange(16) / 16.0)
    residual = bridge.equal_geometry_identity_residual(source)
    assert residual <= 2e-10


def test_v14_full_equal_region_constitutive_point_still_fails_closed() -> None:
    background = make_background(R_bar_v=ZERO)
    coefficients = two_region_coefficients(background)
    assert coefficients.A_P.value == 0.0
    with pytest.raises(H1DegeneracyError, match="A_P"):
        make_result(background=background)


def test_v15_v16_v17_regional_injection_linearity_and_superposition() -> None:
    continuum = ContinuumTransfer(make_operator())
    first = continuum.transfer_regional_amplitude(
        scalar(1.2), region="wall", provenance="wall-1"
    )
    second = continuum.transfer_regional_amplitude(
        scalar(-0.3), region="wall", provenance="wall-2"
    )
    summed = continuum.transfer_regional_amplitude(
        scalar(0.9), region="wall", provenance="wall-sum"
    )
    np.testing.assert_allclose(
        first.transferred_field.value + second.transferred_field.value,
        summed.transferred_field.value,
        atol=2e-12,
    )
    void = continuum.transfer_regional_amplitude(
        scalar(0.7), region="void", provenance="void"
    )
    adapter = ContinuumPhase1EBackendAdapter(continuum)
    joint = adapter.solve_joint(scalar(0.9), scalar(0.7), source_name="joint")
    np.testing.assert_allclose(
        joint.carrier_field.value,
        summed.transferred_field.value + void.transferred_field.value,
        atol=2e-12,
    )


def test_v18_curvature_bridge_uses_only_derived_regional_curvature() -> None:
    bridge = make_bridge(shape=(4, 3, 3))
    background = make_background(
        Theta_w=scalar(0.3), H_w=scalar(0.1),
        Theta_v=scalar(0.6), H_v=scalar(0.2),
        Xi_w=scalar(0.3), Xi_v=scalar(0.6),
    )
    bulk = RegionalBulkState(0.2, 0.4, -0.1, 0.7)
    fields_value = bridge.derive_fields(regional_bulk=bulk, background=background)
    expected = (
        0.5 * fields_value.curvature_wall.transferred_field.value
        + 0.5 * fields_value.curvature_void.transferred_field.value
    )
    np.testing.assert_allclose(fields_value.C_R_Gamma.value, expected)
    assert "curvature" not in {field.name for field in fields(RegionalBulkState)}


def test_v19_e_delta_theta_is_derived_from_transferred_expansions() -> None:
    fields_value = make_bridge(shape=(4, 3, 3)).derive_fields(
        regional_bulk=RegionalBulkState(0.0, 1.0, 0.0, 2.0),
        background=make_background(),
    )
    expected = (
        fields_value.expansion_void.transferred_field.value
        - fields_value.expansion_wall.transferred_field.value
    )
    np.testing.assert_allclose(fields_value.E_DeltaTheta_Gamma.value, expected)


def test_v20_e_delta_xi0_uses_homogeneous_clock_factors() -> None:
    background = make_background(alpha_w=scalar(0.8), alpha_v=scalar(1.2))
    fields_value = make_bridge(shape=(4, 3, 3)).derive_fields(
        regional_bulk=RegionalBulkState(0.0, 1.0, 0.0, 2.0),
        background=background,
    )
    expected = (
        1.2 * fields_value.expansion_void.transferred_field.value
        - 0.8 * fields_value.expansion_wall.transferred_field.value
    )
    np.testing.assert_allclose(fields_value.E_DeltaXi_0_Gamma.value, expected)


def test_v21_j_f_zero_is_branch_derived_and_unsupported_branch_fails() -> None:
    fields_value = make_bridge(shape=(4, 3, 3)).derive_fields(
        regional_bulk=RegionalBulkState(0.0, 1.0, 0.0, 2.0),
        background=make_background(),
    )
    np.testing.assert_array_equal(fields_value.J_f_Gamma.value, 0.0)
    with pytest.raises(ContinuumContractError, match="moving/time-dependent"):
        make_operator(branch=fixed_branch(fixed_interface=False))


def test_v22_operator_derivatives_are_zero_only_on_fixed_branch() -> None:
    operator = make_operator()
    assert operator.operator_first_derivative.nnz == 0
    assert operator.operator_second_derivative.nnz == 0
    assert operator.target_scalarization_first_derivative.nnz == 0
    assert operator.target_scalarization_second_derivative.nnz == 0
    assert operator.branch.fixed_comoving_pullback_geometries is True


def test_v23_transfer_derivatives_commute_and_match_finite_difference() -> None:
    continuum = ContinuumTransfer(make_operator(shape=(12,)))
    shape = np.sin(2.0 * np.pi * np.arange(12) / 12.0)
    jet = VectorJet(1.3 * shape, -0.4 * shape, 0.6 * shape)
    analytic = continuum.transfer_jet(jet, region="global", provenance="jet")
    step = 1e-4
    plus_source = jet.value + step * jet.first + 0.5 * step**2 * jet.second
    minus_source = jet.value - step * jet.first + 0.5 * step**2 * jet.second
    plus = continuum.transfer_source(
        plus_source, region="global", provenance="fd-plus"
    ).transferred_field
    zero = continuum.transfer_source(
        jet.value, region="global", provenance="fd-zero"
    ).transferred_field
    minus = continuum.transfer_source(
        minus_source, region="global", provenance="fd-minus"
    ).transferred_field
    np.testing.assert_allclose(
        (plus - minus) / (2.0 * step),
        analytic.transferred_field.first,
        rtol=2e-8,
        atol=2e-9,
    )
    np.testing.assert_allclose(
        (plus - 2.0 * zero + minus) / step**2,
        analytic.transferred_field.second,
        rtol=2e-6,
        atol=2e-7,
    )


def test_v24_manufactured_background_volume_fraction_consistency_fixture() -> None:
    result = make_result()
    assert result.f_v_geom == pytest.approx(0.5)
    assert result.volume_fraction_consistency_residual == pytest.approx(0.0)
    with pytest.raises(ContinuumContractError, match="volume-fraction"):
        make_result(background=make_background(f_v=0.4))


def test_v25_equal_geometry_mask_and_source_injection_relabel_covariance_of_transfer() -> None:
    original = make_operator()
    morphology = original.morphology
    swapped = MorphologySpec(
        morphology_id="relabelled-layer",
        wall_domain=morphology.void_domain,
        void_domain=morphology.wall_domain,
        interface_id="relabelled-interface",
        wall_pullback_id="old-void-map",
        void_pullback_id="old-wall-map",
        normal_convention=COMMON_REFERENCE_NORMAL_WALL_TO_VOID_1E_G,
        interface_physical_status=INTERFACE_PHYSICAL_STATUS,
        fixed_reference_partition=True,
        fixed_interface=True,
        pullbacks_time_independent=True,
        connected_carrier=True,
        source_injection_provenance={"wall": "old-void", "void": "old-wall"},
    )
    relabelled = make_operator(morphology=swapped)
    old_wall = ContinuumTransfer(original).transfer_regional_amplitude(
        scalar(1.0), region="wall", provenance="old-wall"
    )
    new_void = ContinuumTransfer(relabelled).transfer_regional_amplitude(
        scalar(1.0), region="void", provenance="new-void"
    )
    np.testing.assert_allclose(
        old_wall.transferred_field.value,
        new_void.transferred_field.value,
        atol=2e-12,
    )


@pytest.mark.parametrize("f_v", [0.0, 1.0])
def test_v26_single_region_endpoints_remain_fail_closed(f_v: float) -> None:
    with pytest.raises(H1DegeneracyError, match="ONTOLOGY_REDUCTION"):
        make_result(background=make_background(f_v=f_v))


def test_v27_no_public_continuum_api_accepts_generic_k() -> None:
    public_callables = (
        ContinuumCarrierSpec,
        ContinuumH1Operator,
        ContinuumTransfer,
        EffectiveSectorContinuumBridge,
        RegionalGeometrySpec,
    )
    for callable_object in public_callables:
        assert "k" not in inspect.signature(callable_object).parameters
    with pytest.raises(ContinuumContractError, match="generic k"):
        require_no_generic_spectral_label(("lambda_Gamma_n", "k"))


def test_v28_heterogeneous_geometry_mixes_target_fourier_modes() -> None:
    shape = (24,)
    void = conformal_regional_geometry(
        region_id="void",
        conformal_factor=np.full(shape, 1.7),
        dimension=1,
        curvature_class="SYNTHETIC_CONFORMAL_COMPARATOR",
        pullback_provenance="heterogeneous-void-map",
        normalization=metric_normalization(
            normalization_id="mode-mixing-void-normalization",
            reference_comoving_volume=metric_domain_volume(
                np.full(shape, 1.7), np.arange(shape[0]) >= shape[0] // 2
            ),
            metric_scale_convention="CONFORMAL_FACTOR_1_7",
        ),
        metadata={"role": "mode-mixing numerical fixture"},
    )
    operator = make_operator(shape=shape, void_geometry=void)
    source = np.sin(2.0 * np.pi * np.arange(24) / 24.0)
    transferred = ContinuumTransfer(operator).transfer_source(
        source, region="global", provenance="mode-mixing"
    ).transferred_field
    spectrum = np.fft.rfft(transferred)
    leakage = np.linalg.norm(spectrum[2:])
    assert leakage > 1e-4


def test_v29_two_explicit_morphologies_have_resolved_sensitivity() -> None:
    shape = (10, 10)
    layer = layered_morphology(
        morphology_id="layer-20-percent-void",
        grid_shape=shape,
        axis=0,
        wall_cell_count=8,
        wall_pullback_id="Phi_w_layer",
        void_pullback_id="Phi_v_layer",
    )
    island = island_morphology(
        morphology_id="island-20-percent-void",
        grid_shape=shape,
        void_lower=(3, 2),
        void_upper=(7, 7),
        wall_pullback_id="Phi_w_island",
        void_pullback_id="Phi_v_island",
    )
    operators = (
        make_operator(shape=shape, morphology=layer),
        make_operator(shape=shape, morphology=island),
    )

    def fields(operator: ContinuumH1Operator) -> tuple[np.ndarray, ...]:
        continuum = ContinuumTransfer(operator)
        wall_density = continuum.transfer_regional_amplitude(
            scalar(1.0), region="wall", provenance="common-latent-density"
        ).transferred_field.value
        void_density = continuum.transfer_regional_amplitude(
            scalar(-0.5), region="void", provenance="common-latent-density"
        ).transferred_field.value
        wall_expansion = continuum.transfer_regional_amplitude(
            scalar(1.0), region="wall", provenance="common-latent-expansion"
        ).transferred_field.value
        void_expansion = continuum.transfer_regional_amplitude(
            scalar(2.0), region="void", provenance="common-latent-expansion"
        ).transferred_field.value
        return wall_density, void_density, void_expansion - wall_expansion

    first_fields, second_fields = (fields(operator) for operator in operators)
    names = (
        "transferred_wall_density",
        "transferred_void_density",
        "E_DeltaTheta_Gamma",
    )
    diagnostics = {
        name: target_metric_weighted_l2_difference(
            first,
            second,
            target_measure_weights=operators[0].target_measure_weights,
            reference_scale=continuum_configuration().morphology_sensitivity_reference_scale,
            normalization_floor=continuum_configuration().morphology_sensitivity_floor,
        )
        for name, first, second in zip(
            names, first_fields, second_fields, strict=True
        )
    }
    assert diagnostics["transferred_wall_density"] > 1e-3
    assert diagnostics["E_DeltaTheta_Gamma"] > 1e-3
    assert operators[0].carrier.dimension == 2
    with pytest.raises(ContinuumDimensionalContractError, match="dimension 2"):
        operators[0].geometric_void_fraction(a_w=1.0, a_v=1.0)


def _convergence_errors(resolution: int) -> tuple[float, float]:
    operator = make_operator(shape=(resolution,))
    continuum = ContinuumTransfer(operator)
    x = (np.arange(resolution) + 0.5) / resolution
    exact = np.sin(2.0 * np.pi * x)
    source = -(2.0 * np.pi) ** 2 * exact
    response = continuum.transfer_source(
        source, region="global", provenance=f"convergence-{resolution}"
    )
    error = response.potential - exact
    l2 = float(np.sqrt(np.sum(operator.reference_weights * error**2)))
    energy = float(np.sqrt(error @ (operator.stiffness_matrix @ error)))
    return l2, energy


def test_v30_manufactured_continuum_discretization_converges() -> None:
    resolutions = (16, 32, 64)
    errors = [_convergence_errors(resolution) for resolution in resolutions]
    l2_rates = [np.log2(errors[i][0] / errors[i + 1][0]) for i in range(2)]
    energy_rates = [np.log2(errors[i][1] / errors[i + 1][1]) for i in range(2)]
    config = continuum_configuration()
    assert min(l2_rates) >= config.convergence_l2_min_rate
    assert min(energy_rates) >= config.convergence_energy_min_rate


def test_v31_discrete_operator_contract_consistency() -> None:
    operator = make_operator()
    adapter = ContinuumPhase1EBackendAdapter(ContinuumTransfer(operator))
    state = adapter.solve_joint(scalar(1.2), scalar(-0.4), source_name="contract")
    recovered = adapter.apply_coupled_operator_jet(state.carrier_field)
    expected = VectorJet(
        state.wall.injected_source.value + state.void.injected_source.value,
        state.wall.injected_source.first + state.void.injected_source.first,
        state.wall.injected_source.second + state.void.injected_source.second,
    )
    np.testing.assert_allclose(recovered.value, expected.value, atol=1e-10)
    np.testing.assert_allclose(recovered.first, expected.first, atol=1e-10)
    np.testing.assert_allclose(recovered.second, expected.second, atol=1e-10)


def test_v32_continuum_derived_downstream_phase1e_f_diagnostics_stay_green() -> None:
    result = make_result()
    downstream = result.downstream_phase1e_f
    assert np.max(np.abs(result.E_DeltaTheta_Gamma.value)) > 0.1
    np.testing.assert_allclose(downstream.C_P, 0.0, atol=1e-10)
    np.testing.assert_allclose(downstream.R_Delta, 0.0, atol=1e-10)
    np.testing.assert_allclose(downstream.R_Z, 0.0, atol=1e-10)
    np.testing.assert_allclose(downstream.R_eff, 0.0, atol=1e-10)
    np.testing.assert_allclose(downstream.K_GM, 0.0, atol=1e-10)


def test_v33_d3_firewall_preserves_two_explicit_variants_without_default() -> None:
    source = (
        Path(__file__).resolve().parents[1]
        / "src" / "timescape_fsigma8" / "perturbations" / "barotropic.py"
    ).read_text(encoding="utf-8")
    assert 'PRINTED_4_15 = "printed_4_15"' in source
    assert 'DERIVED_4_10 = "derived_4_10"' in source
    assert "DEFAULT" not in source


def test_v34_observational_and_frame_firewalls_export_no_runtime() -> None:
    forbidden = (
        "fsigma8", "sigma8", "rsd", "tracer", "survey", "likelihood",
        "peculiar_velocity", "dressed_velocity",
    )
    callable_names = {
        name.lower() for name in transfer.__all__ if callable(getattr(transfer, name))
    }
    for token in forbidden:
        assert not any(token in name for name in callable_names)
    assert transfer.REALIZATION_ID_1E_G.endswith("TRANSMISSION-V1")
    assert transfer.SCIENTIFIC_STATUS_1E_G == "CONDITIONALLY_DERIVED_CONTINUUM_REALIZATION"


def test_source_measure_adversarial_nonconstant_j_detects_omission() -> None:
    shape = (8, 8)
    coordinates = np.indices(shape, dtype=float)
    x = (coordinates[0] + 0.5) / shape[0] - 0.5
    y = (coordinates[1] + 0.5) / shape[1] - 0.5
    factor = 2.0 / (1.0 - x**2 - y**2)
    geometry = conformal_regional_geometry(
        region_id="void",
        conformal_factor=factor,
        dimension=2,
        curvature_class="POINCARE_DISK_GAUSSIAN_CURVATURE_MINUS_ONE",
        pullback_provenance="nonconstant-J-oracle",
        normalization=metric_normalization(
            normalization_id="nonconstant-J-void",
            reference_comoving_volume=metric_domain_volume(
                factor**2, np.indices(shape)[0] >= shape[0] // 2
            ),
            metric_scale_convention="POINCARE_PATCH_CONFORMAL_SCALE",
        ),
        metadata={"purpose": "source-measure adversarial"},
    )
    wall = replace(
        geometry,
        region_id="wall",
        normalization=metric_normalization(
            normalization_id="nonconstant-J-wall",
            reference_comoving_volume=metric_domain_volume(
                factor**2, np.indices(shape)[0] < shape[0] // 2
            ),
            metric_scale_convention="POINCARE_PATCH_CONFORMAL_SCALE",
        ),
    )
    target = replace(
        geometry,
        region_id="target",
        normalization=metric_normalization(
            normalization_id="nonconstant-J-target",
            reference_comoving_volume=metric_domain_volume(
                factor**2, np.ones(shape, dtype=bool)
            ),
            metric_scale_convention="POINCARE_PATCH_CONFORMAL_SCALE",
        ),
    )
    operator = make_operator(
        shape=shape,
        wall_geometry=wall,
        void_geometry=geometry,
        target_geometry=target,
    )
    grid_x = np.sin(2.0 * np.pi * (coordinates[0] + 0.5) / shape[0])
    potential = grid_x.reshape(-1)
    source = -(
        operator.stiffness_matrix @ potential
    ) / (operator.reference_weights * operator.metric_volume_ratio)
    correct = ContinuumTransfer(operator).transfer_source(
        source, region="global", provenance="correct-J"
    )
    np.testing.assert_allclose(correct.potential, potential, atol=2e-10)
    wrong_load = operator.reference_weights * source
    wrong_projected, _ = operator.project_dual_source(wrong_load)
    wrong_potential = operator.solve_projected_load(wrong_projected)
    assert np.max(np.abs(wrong_potential - potential)) > 1e-3


@pytest.mark.parametrize(
    ("branch_changes", "message"),
    [
        ({"fixed_reference_partition": False}, "moving/time-dependent"),
        ({"fixed_target_scalarization": False}, "moving/time-dependent"),
        ({"homogeneous_background_clock_map": False}, "moving/time-dependent"),
        ({"spatial_clock_perturbation": True}, "spatially varying"),
    ],
)
def test_unsupported_time_geometry_and_clock_branches_fail_closed(
    branch_changes: dict[str, object], message: str
) -> None:
    with pytest.raises(ContinuumContractError, match=message):
        make_operator(branch=fixed_branch(**branch_changes))


def test_non_spd_and_nonpositive_metric_data_fail_closed() -> None:
    inverse = np.ones((8, 1, 1))
    inverse[0, 0, 0] = -1.0
    with pytest.raises(ContinuumDegeneracyError, match="SPD"):
        RegionalGeometrySpec(
            region_id="void", metric_inverse=inverse,
            metric_volume_ratio=np.ones(8), curvature_class="invalid",
            pullback_provenance="invalid", metric_time_independent=True,
            isotropic_reference_backend=True,
            normalization=metric_normalization(
                normalization_id="invalid-spd", reference_comoving_volume=0.5
            ), metadata={},
        )
    with pytest.raises(ContinuumDegeneracyError, match="strictly positive"):
        RegionalGeometrySpec(
            region_id="void", metric_inverse=np.ones((8, 1, 1)),
            metric_volume_ratio=np.zeros(8), curvature_class="invalid",
            pullback_provenance="invalid", metric_time_independent=True,
            isotropic_reference_backend=True,
            normalization=metric_normalization(
                normalization_id="invalid-volume", reference_comoving_volume=0.5
            ), metadata={},
        )


def test_malformed_overlap_coverage_and_disconnected_morphology_fail_closed() -> None:
    wall = np.array([True] * 4 + [False] * 4)
    with pytest.raises(ContinuumContractError, match="overlap"):
        MorphologySpec(
            morphology_id="overlap", wall_domain=wall, void_domain=wall,
            interface_id="bad", wall_pullback_id="w", void_pullback_id="v",
            normal_convention=COMMON_REFERENCE_NORMAL_WALL_TO_VOID_1E_G,
            interface_physical_status=INTERFACE_PHYSICAL_STATUS,
            fixed_reference_partition=True, fixed_interface=True,
            pullbacks_time_independent=True, connected_carrier=True,
            source_injection_provenance={"wall": "w", "void": "v"},
        )
    with pytest.raises(ContinuumContractError, match="cover"):
        MorphologySpec(
            morphology_id="gap", wall_domain=wall, void_domain=np.zeros(8, bool),
            interface_id="bad", wall_pullback_id="w", void_pullback_id="v",
            normal_convention=COMMON_REFERENCE_NORMAL_WALL_TO_VOID_1E_G,
            interface_physical_status=INTERFACE_PHYSICAL_STATUS,
            fixed_reference_partition=True, fixed_interface=True,
            pullbacks_time_independent=True, connected_carrier=True,
            source_injection_provenance={"wall": "w", "void": "v"},
        )
    cycle = np.diag(np.full(4, 2.0))
    cycle -= np.roll(np.eye(4), 1, axis=0)
    cycle -= np.roll(np.eye(4), -1, axis=0)
    disconnected_operator = np.block(
        [[cycle, np.zeros((4, 4))], [np.zeros((4, 4)), cycle]]
    )
    assert np.count_nonzero(
        np.abs(np.linalg.eigvalsh(disconnected_operator)) < 1e-12
    ) == 2
    with pytest.raises(ContinuumDegeneracyError, match="extra kernel"):
        replace(make_operator().morphology, connected_carrier=False)


def test_missing_morphology_and_invalid_physical_metadata_fail_closed() -> None:
    signature = inspect.signature(ContinuumH1Operator)
    assert signature.parameters["morphology"].default is inspect.Parameter.empty
    with pytest.raises(ContinuumContractError, match="MATHEMATICAL_TRANSFER_INTERFACE"):
        replace(
            make_operator().morphology,
            interface_physical_status="PHYSICAL_WALL_JUNCTION",
        )


def test_unsupported_anisotropic_reference_discretization_fails_closed() -> None:
    shape = (6, 6)
    inverse = np.zeros(shape + (2, 2))
    inverse[..., 0, 0] = 1.0
    inverse[..., 1, 1] = 2.0
    anisotropic = RegionalGeometrySpec(
        region_id="void", metric_inverse=inverse,
        metric_volume_ratio=np.ones(shape), curvature_class="anisotropic-test",
        pullback_provenance="explicit-anisotropic", metric_time_independent=True,
        isotropic_reference_backend=True,
        normalization=metric_normalization(
            normalization_id="anisotropic-void", reference_comoving_volume=0.5
        ), metadata={},
    )
    with pytest.raises(ContinuumContractError, match="unequal principal"):
        make_operator(shape=shape, void_geometry=anisotropic)


def test_raw_incompatible_source_cannot_bypass_dual_projection() -> None:
    operator = make_operator()
    with pytest.raises(ContinuumContractError, match="annihilate"):
        operator.solve_projected_load(np.ones(operator.size))


def test_broken_explicit_value_and_flux_conditions_are_detected() -> None:
    value, flux = ContinuumH1Operator.explicit_trace_residuals(
        wall_trace=np.array([1.0, 2.0]),
        void_trace=np.array([1.1, 2.0]),
        wall_common_flux=np.array([0.4, -0.2]),
        void_common_flux=np.array([0.4, 0.3]),
        normal_convention=COMMON_REFERENCE_NORMAL_WALL_TO_VOID_1E_G,
    )
    assert np.max(np.abs(value)) == pytest.approx(0.1)
    assert np.max(np.abs(flux)) == pytest.approx(0.5)


def test_wrong_normal_convention_fails_closed() -> None:
    with pytest.raises(ContinuumContractError, match="normal"):
        ContinuumH1Operator.explicit_trace_residuals(
            wall_trace=np.zeros(1), void_trace=np.zeros(1),
            wall_common_flux=np.zeros(1), void_common_flux=np.zeros(1),
            normal_convention="REGIONAL_OUTWARD_NORMALS",
        )


def test_spatial_clock_or_xi_identity_cannot_be_silently_changed() -> None:
    with pytest.raises(ContinuumContractError, match="Xi_wall"):
        make_bridge(shape=(4, 3, 3)).derive_fields(
            regional_bulk=RegionalBulkState(0.0, 1.0, 0.0, 2.0),
            background=make_background(Xi_w=scalar(0.1)),
        )


def test_d5_one_dimensional_weighted_operator_survives_without_volume_promotion() -> None:
    factor = np.ones(8)
    factor[4:] = 2.0
    void = conformal_regional_geometry(
        region_id="void", conformal_factor=factor, dimension=1,
        curvature_class="weighted-volume-fixture",
        pullback_provenance="weighted-volume-map",
        normalization=metric_normalization(
            normalization_id="weighted-volume-void",
            reference_comoving_volume=metric_domain_volume(
                factor, np.arange(8) >= 4
            ),
            metric_scale_convention="PIECEWISE_CONFORMAL_1D",
        ), metadata={},
    )
    operator = make_operator(void_geometry=void)
    assert np.mean(operator.morphology.void_domain) == pytest.approx(0.5)
    wall_measure, void_measure = operator.metric_derived_regional_reference_measures()
    assert wall_measure == pytest.approx(0.5)
    assert void_measure == pytest.approx(1.0)
    assert operator.metric_normalization_diagnostics["void"].measure_semantics == (
        REDUCED_DIMENSIONAL_MEASURE_ONLY
    )
    response = ContinuumTransfer(operator).transfer_source(
        np.arange(8.0), region="void", provenance="one-dimensional-operator-only"
    )
    assert np.max(np.abs(response.transferred_field)) > 0.0
    with pytest.raises(ContinuumDimensionalContractError, match="dimension 1"):
        operator.geometric_void_fraction(a_w=1.0, a_v=1.0)


def test_phase1e_g_result_status_and_no_fifth_state() -> None:
    result = make_result()
    assert result.realization_id == "H1-1E-G-COMOVING-CGI-ELLIPTIC-TRANSMISSION-V1"
    assert result.scientific_status == "CONDITIONALLY_DERIVED_CONTINUUM_REALIZATION"
    assert result.implementation_status == "CONDITIONAL_RESEARCH_RUNTIME"
    assert [field.name for field in fields(RegionalBulkState)] == [
        "Delta_w", "Z_w", "Delta_v", "Z_v"
    ]
    assert not hasattr(result, "interface_displacement_state")
    assert not hasattr(result, "target_only_inverse")


def test_n1_time_dependent_target_metric_fails_closed() -> None:
    target = replace(
        make_operator().carrier.target_geometry,
        metric_time_independent=False,
    )
    with pytest.raises(ContinuumContractError, match="target metric"):
        make_operator(target_geometry=target)


def test_n2_regional_metric_normalization_provenance_is_required() -> None:
    assert (
        inspect.signature(RegionalGeometrySpec).parameters["normalization"].default
        is inspect.Parameter.empty
    )
    with pytest.raises(TypeError, match="normalization"):
        RegionalGeometrySpec(
            region_id="missing-normalization",
            metric_inverse=np.ones((8, 1, 1)),
            metric_volume_ratio=np.ones(8),
            curvature_class="flat",
            pullback_provenance="explicit-test",
            metric_time_independent=True,
            isotropic_reference_backend=True,
            metadata={},
        )


def test_n3_inconsistent_declared_reference_volume_fails_closed() -> None:
    base = make_operator()
    stale = replace(
        base.void_geometry,
        normalization=replace(
            base.void_geometry.normalization,
            reference_comoving_volume=0.4,
        ),
    )
    with pytest.raises(ContinuumContractError, match="reference-measure"):
        make_operator(void_geometry=stale)


def _rescaled_void_geometry(
    *,
    shape: tuple[int, int, int],
    conformal_scale: float,
    declared_volume: float,
    normalization_id: str,
    scale_factor_reference_value: float,
) -> RegionalGeometrySpec:
    return conformal_regional_geometry(
        region_id="void",
        conformal_factor=np.full(shape, conformal_scale),
        dimension=3,
        curvature_class="CONSTANT_RESCALING_GAUGE_CONVENTION_FIXTURE",
        pullback_provenance="Phi_v_constant_rescaling",
        normalization=metric_normalization(
            normalization_id=normalization_id,
            reference_comoving_volume=declared_volume,
            scale_factor_reference_value=scale_factor_reference_value,
            metric_scale_convention=f"GAMMA_PRIME_EQUALS_{conformal_scale}_SQUARED_GAMMA",
            volume_provenance=EXTERNALLY_SUPPLIED_REFERENCE_VOLUME,
        ),
        metadata={"role": "normalization-gauge fixture"},
    )


def test_n4_constant_metric_rescaling_with_stale_contract_is_rejected() -> None:
    shape = (3, 3, 3)
    stale = _rescaled_void_geometry(
        shape=shape,
        conformal_scale=2.0,
        declared_volume=2.0 / 3.0,
        normalization_id="stale-original-normalization",
        scale_factor_reference_value=1.0,
    )
    with pytest.raises(ContinuumContractError, match="reference-measure"):
        make_operator(shape=shape, void_geometry=stale)


def test_n5_consistent_metric_scale_factor_volume_transform_is_explicit() -> None:
    shape = (3, 3, 3)
    base = make_operator(shape=shape)
    transformed = _rescaled_void_geometry(
        shape=shape,
        conformal_scale=2.0,
        declared_volume=16.0 / 3.0,
        normalization_id="rescaled-gamma-and-a-convention",
        scale_factor_reference_value=0.5,
    )
    alternative = make_operator(shape=shape, void_geometry=transformed)
    assert (
        alternative.void_geometry.normalization.normalization_id
        != base.void_geometry.normalization.normalization_id
    )
    assert alternative.geometric_void_fraction(a_w=1.0, a_v=0.5) == pytest.approx(
        base.geometric_void_fraction(a_w=1.0, a_v=1.0)
    )
    assert PHYSICAL_NORMALIZATION_COVARIANCE == "PHYSICAL_NORMALIZATION_COVARIANCE"
    base_physical = base.physical_regional_volumes(a_w=1.0, a_v=1.0)
    transformed_physical = alternative.physical_regional_volumes(a_w=1.0, a_v=0.5)
    assert transformed_physical == pytest.approx(base_physical)


def test_n6_volume_fraction_fixture_is_labelled_manufactured_consistency() -> None:
    result = make_result()
    assert result.volume_fraction_consistency_classification == (
        "MANUFACTURED_BACKGROUND_CONSISTENCY_FIXTURE"
    )
    assert result.regional_metric_normalization["wall"].consistency_classification == (
        "CONSTRUCTION_CONSISTENCY_CHECK"
    )


def _continuum_dynamic_fixture(
    *,
    alpha_w_first: float = 0.0,
    q_bar_first_shift: float = 0.0,
    relaxed_residuals: bool = False,
):
    """Independently specified continuum-derived nontrivial GM trajectory."""
    morphology = layered_morphology(
        morphology_id="continuum-dynamic-one-wall-cell",
        grid_shape=(6, 3, 3),
        axis=0,
        wall_cell_count=1,
        wall_pullback_id="Phi_w_dynamic",
        void_pullback_id="Phi_v_dynamic",
    )
    downstream = downstream_configuration(
        **(
            {"R_Z_tolerance": 1e9, "R_eff_tolerance": 1e9}
            if relaxed_residuals
            else {}
        )
    )
    bridge = make_bridge(
        shape=(6, 3, 3),
        morphology=morphology,
        configuration=continuum_configuration(
            downstream_configuration=downstream
        ),
    )
    G = 1.0 / (4.0 * np.pi)
    background = make_background(
        f_v=0.4,
        rho_w=scalar(1.0),
        rho_v=scalar(1.0),
        Theta_w=scalar(0.6),
        Theta_v=scalar(1.2),
        H_w=scalar(0.2),
        H_v=scalar(0.4),
        alpha_w=scalar(1.0, alpha_w_first),
        alpha_v=scalar(1.0),
        R_bar_w=scalar(0.0),
        R_bar_v=scalar(-0.10755555555555557),
        Q_bar=scalar(-5.0, -26.979222614841003 + q_bar_first_shift),
        W_bar=scalar(-3.0),
        Theta=scalar(0.84),
        Xi_w=scalar(0.6, 0.6 * alpha_w_first),
        Xi_v=scalar(1.2),
        G=G,
    )
    result = make_result(
        bridge=bridge,
        background=background,
        regional_bulk=RegionalBulkState(1.0, 0.4, 1.0, 0.8),
        a_w=1.0,
        a_v=(2.0 / 15.0) ** (1.0 / 3.0),
    )
    return result, background


def test_n7_n8_continuum_derived_r_z_and_r_eff_cancel_nontrivially() -> None:
    result, background = _continuum_dynamic_fixture()
    downstream = result.downstream_phase1e_f
    assert np.max(np.abs(result.E_DeltaTheta_Gamma.value)) > 1e-3
    assert np.max(np.abs(result.E_DeltaXi_0_Gamma.value)) > 1e-3
    assert np.max(np.abs(result.C_R_Gamma.value)) > 1e-3
    np.testing.assert_array_equal(result.J_f_Gamma.value, 0.0)
    assert np.max(np.abs(downstream.Delta_d.value)) > 1e-3
    assert np.max(np.abs(downstream.Z)) > 1e-3
    assert np.max(np.abs(-downstream.Delta_d.second)) > 1e-3
    assert background.Theta.value != 0.0
    assert np.max(np.abs(downstream.Delta_eff.value)) > 1e-3
    assert np.max(np.abs(downstream.Delta_eff.first)) > 1e-3

    r_z_nonpressure_terms = (
        -downstream.Delta_d.second,
        (2.0 / 3.0) * background.Theta.value * downstream.Z,
        4.0 * np.pi * background.G * downstream.rho_d * downstream.Delta_d.value,
        4.0 * np.pi * background.G * downstream.rho_eff * downstream.Delta_eff.value,
    )
    assert all(np.max(np.abs(term)) > 1e-3 for term in r_z_nonpressure_terms)
    r_z_pressure_term = (
        12.0 * np.pi * background.G * downstream.rho_eff * downstream.P_tilde_eff
    )
    assert np.max(np.abs(r_z_pressure_term)) < 1e-12
    r_z_terms = r_z_nonpressure_terms + (r_z_pressure_term,)
    independent_r_z = sum(r_z_terms, np.zeros_like(downstream.R_Z))
    np.testing.assert_allclose(independent_r_z, 0.0, atol=1e-12)
    np.testing.assert_allclose(downstream.R_Z, independent_r_z, atol=1e-13)

    r_eff_nonpressure_terms = (
        downstream.Delta_eff.first,
        -downstream.w_eff
        * background.Theta.value
        * downstream.Delta_eff.value,
        (1.0 + downstream.w_eff) * downstream.Z,
    )
    assert all(np.max(np.abs(term)) > 1e-3 for term in r_eff_nonpressure_terms)
    r_eff_pressure_term = background.Theta.value * downstream.P_tilde_eff
    assert np.max(np.abs(r_eff_pressure_term)) < 1e-12
    r_eff_terms = r_eff_nonpressure_terms + (r_eff_pressure_term,)
    independent_r_eff = sum(r_eff_terms, np.zeros_like(downstream.R_eff))
    np.testing.assert_allclose(independent_r_eff, 0.0, atol=1e-12)
    np.testing.assert_allclose(downstream.R_eff, independent_r_eff, atol=1e-13)


def test_n9_continuum_derived_adversarial_r_z_increment_is_predictable() -> None:
    shift = 0.05
    baseline, _ = _continuum_dynamic_fixture(relaxed_residuals=True)
    corrupted, _ = _continuum_dynamic_fixture(
        alpha_w_first=shift,
        relaxed_residuals=True,
    )
    phi = baseline.bridge_fields.density_wall.transferred_field.value
    expected_increment = 0.24 * shift * phi
    np.testing.assert_allclose(
        corrupted.downstream_phase1e_f.R_Z
        - baseline.downstream_phase1e_f.R_Z,
        expected_increment,
        atol=2e-13,
    )
    with pytest.raises(H1ClosureError, match=r"^R_Z="):
        _continuum_dynamic_fixture(alpha_w_first=shift)


def test_n10_continuum_derived_adversarial_r_eff_increment_is_predictable() -> None:
    shift = 0.5
    baseline, _ = _continuum_dynamic_fixture(relaxed_residuals=True)
    corrupted, _ = _continuum_dynamic_fixture(
        q_bar_first_shift=shift,
        relaxed_residuals=True,
    )
    phi = baseline.bridge_fields.density_wall.transferred_field.value
    expected_increment = -0.0072 * shift * phi
    np.testing.assert_allclose(
        corrupted.downstream_phase1e_f.R_eff
        - baseline.downstream_phase1e_f.R_eff,
        expected_increment,
        atol=2e-13,
    )
    with pytest.raises(H1ClosureError, match=r"^R_eff="):
        _continuum_dynamic_fixture(q_bar_first_shift=shift)


def test_n11_morphology_difference_uses_target_metric_weighted_l2() -> None:
    first = np.array([0.0, 1.0, 2.0])
    second = np.zeros(3)
    target_weights = np.array([0.1, 0.2, 0.7])
    value = target_metric_weighted_l2_difference(
        first,
        second,
        target_measure_weights=target_weights,
        reference_scale=2.0,
        normalization_floor=1e-12,
    )
    assert value == pytest.approx(np.sqrt(3.0) / 2.0)
    assert value != pytest.approx(np.linalg.norm(first) / 2.0)


def _shifted_half_morphology(resolution: int) -> MorphologySpec:
    coordinate = np.arange(resolution)
    wall = ((coordinate - resolution // 4) % resolution) < resolution // 2
    return MorphologySpec(
        morphology_id=f"shifted-half-{resolution}",
        wall_domain=wall,
        void_domain=~wall,
        interface_id=f"shifted-half-{resolution}:interface",
        wall_pullback_id="Phi_w_shifted_half",
        void_pullback_id="Phi_v_shifted_half",
        normal_convention=COMMON_REFERENCE_NORMAL_WALL_TO_VOID_1E_G,
        interface_physical_status=INTERFACE_PHYSICAL_STATUS,
        fixed_reference_partition=True,
        fixed_interface=True,
        pullbacks_time_independent=True,
        connected_carrier=True,
        source_injection_provenance={"wall": "latent-wall", "void": "latent-void"},
    )


def test_n12_morphology_metric_refinement_converges_to_resolved_diagnostic() -> None:
    diagnostics: list[dict[str, float]] = []
    for resolution in (16, 32, 64):
        first_morphology = layered_morphology(
            morphology_id=f"unshifted-half-{resolution}",
            grid_shape=(resolution,),
            axis=0,
            wall_cell_count=resolution // 2,
            wall_pullback_id="Phi_w_unshifted_half",
            void_pullback_id="Phi_v_unshifted_half",
        )
        first_operator = make_operator(
            shape=(resolution,), morphology=first_morphology
        )
        second_operator = make_operator(
            shape=(resolution,), morphology=_shifted_half_morphology(resolution)
        )
        first_transfer = ContinuumTransfer(first_operator)
        second_transfer = ContinuumTransfer(second_operator)
        first_wall = first_transfer.transfer_regional_amplitude(
            scalar(1.0), region="wall", provenance="common-latent-wall"
        ).transferred_field.value
        second_wall = second_transfer.transfer_regional_amplitude(
            scalar(1.0), region="wall", provenance="common-latent-wall"
        ).transferred_field.value
        first_void = first_transfer.transfer_regional_amplitude(
            scalar(-0.5), region="void", provenance="common-latent-void"
        ).transferred_field.value
        second_void = second_transfer.transfer_regional_amplitude(
            scalar(-0.5), region="void", provenance="common-latent-void"
        ).transferred_field.value
        config = continuum_configuration()
        diagnostics.append(
            {
                "transferred_wall_density": target_metric_weighted_l2_difference(
                    first_wall,
                    second_wall,
                    target_measure_weights=first_operator.target_measure_weights,
                    reference_scale=config.morphology_sensitivity_reference_scale,
                    normalization_floor=config.morphology_sensitivity_floor,
                ),
                "transferred_void_density": target_metric_weighted_l2_difference(
                    first_void,
                    second_void,
                    target_measure_weights=first_operator.target_measure_weights,
                    reference_scale=config.morphology_sensitivity_reference_scale,
                    normalization_floor=config.morphology_sensitivity_floor,
                ),
            }
        )
    for key in ("transferred_wall_density", "transferred_void_density"):
        values = [item[key] for item in diagnostics]
        assert values[-1] > 1e-3
        assert abs(values[-1] - values[-2]) <= (
            continuum_configuration().morphology_convergence_tolerance
        )
    assert CONVERGED_EQUAL_GEOMETRY_MASK_PLACEMENT_DIAGNOSTIC == (
        "CONVERGED_EQUAL_GEOMETRY_MASK_PLACEMENT_DIAGNOSTIC"
    )


@pytest.mark.parametrize("region", ["wall", "void"])
def test_n13_n14_raw_regional_provenance_but_projected_support_is_global(
    region: str,
) -> None:
    response = ContinuumTransfer(make_operator()).transfer_source(
        np.ones(8), region=region, provenance="raw-regional-source"
    )
    assert response.raw_source_provenance == region
    assert response.projected_admissible_source_support == (
        "GLOBAL_AFTER_CONSTANT_COMPATIBILITY_CORRECTION"
    )
    opposite = (
        make_operator().morphology.void_domain
        if region == "wall"
        else make_operator().morphology.wall_domain
    ).reshape(-1)
    assert np.max(np.abs(response.projected_source_load[opposite])) > 1e-3


def test_n15_ordinary_stiffness_and_generalized_mass_spectrum_are_distinct() -> None:
    ordinary: list[float] = []
    generalized: list[float] = []
    for resolution in (16, 32, 64):
        operator = make_operator(shape=(resolution,))
        ordinary.append(
            operator.ordinary_euclidean_constrained_stiffness_eigenvalue
        )
        generalized.append(
            operator.generalized_mass_weighted_laplacian_eigenvalue
        )
    assert ordinary[2] < ordinary[1] < ordinary[0]
    assert abs(generalized[-1] - 4.0 * np.pi**2) < abs(
        generalized[0] - 4.0 * np.pi**2
    )
    assert generalized[-1] == pytest.approx(4.0 * np.pi**2, rel=4e-3)


def test_d1_three_dimensional_physical_volume_path_is_accepted() -> None:
    result = make_result()
    operator = make_operator(shape=(4, 3, 3))
    assert result.continuum_geometry["dimension"] == 3
    assert result.physical_volume_semantics == PHYSICAL_VOLUME_SEMANTICS
    assert operator.physical_regional_volumes(a_w=1.0, a_v=1.0) == pytest.approx(
        (0.5, 0.5)
    )
    assert operator.geometric_void_fraction(a_w=1.0, a_v=1.0) == pytest.approx(0.5)


@pytest.mark.parametrize(
    ("shape", "dimension"),
    [((8,), 1), ((6, 6), 2)],
)
def test_d2_d3_d7_reduced_dimension_rejects_every_physical_volume_path(
    shape: tuple[int, ...], dimension: int
) -> None:
    operator = make_operator(shape=shape)
    assert operator.carrier.dimension == dimension
    assert all(
        measure > 0.0
        for measure in operator.metric_derived_regional_reference_measures()
    )
    for operation in (
        operator.metric_derived_regional_comoving_volumes,
        operator.regional_comoving_volumes,
        lambda: operator.physical_regional_volumes(a_w=1.0, a_v=1.0),
        lambda: operator.geometric_void_fraction(a_w=1.0, a_v=1.0),
    ):
        with pytest.raises(
            ContinuumDimensionalContractError,
            match=rf"spatial_dimension == 3; dimension {dimension}",
        ):
            operation()
    bridge = EffectiveSectorContinuumBridge(
        operator=operator,
        branch=operator.branch,
        configuration=operator.configuration,
    )
    with pytest.raises(ContinuumDimensionalContractError, match=f"dimension {dimension}"):
        bridge.derive_fields(
            regional_bulk=RegionalBulkState(0.0, 1.0, 0.0, 2.0),
            background=make_background(),
        )


@pytest.mark.parametrize("shape", [(8,), (6, 6)])
def test_d4_external_reference_volume_mode_cannot_bypass_dimension_guard(
    shape: tuple[int, ...],
) -> None:
    base = make_operator(shape=shape)

    def externalized(geometry: RegionalGeometrySpec) -> RegionalGeometrySpec:
        return replace(
            geometry,
            normalization=replace(
                geometry.normalization,
                normalization_id=f"{geometry.region_id}-external-measure",
                volume_provenance=EXTERNALLY_SUPPLIED_REFERENCE_VOLUME,
            ),
        )

    operator = make_operator(
        shape=shape,
        morphology=base.morphology,
        wall_geometry=externalized(base.wall_geometry),
        void_geometry=externalized(base.void_geometry),
        target_geometry=externalized(base.carrier.target_geometry),
    )
    assert operator.metric_normalization_diagnostics["wall"].volume_provenance == (
        EXTERNALLY_SUPPLIED_REFERENCE_VOLUME
    )
    assert operator.metric_normalization_diagnostics["wall"].measure_semantics == (
        REDUCED_DIMENSIONAL_MEASURE_ONLY
    )
    with pytest.raises(ContinuumDimensionalContractError, match="dimension"):
        operator.physical_regional_volumes(a_w=1.0, a_v=1.0)


def test_d5_two_dimensional_operator_fixture_survives_without_volume_promotion() -> None:
    operator = make_operator(shape=(6, 6))
    coordinates = np.indices((6, 6), dtype=float)
    source = np.sin(2.0 * np.pi * coordinates[0] / 6.0).reshape(-1)
    response = ContinuumTransfer(operator).transfer_source(
        source, region="global", provenance="two-dimensional-operator-only"
    )
    assert np.max(np.abs(response.transferred_field)) > 0.0
    assert operator.global_kernel_dimension == 1
    with pytest.raises(ContinuumDimensionalContractError, match="dimension 2"):
        operator.geometric_void_fraction(a_w=1.0, a_v=1.0)


@pytest.mark.parametrize(
    ("dimension", "expected_factor"),
    [(1, 0.25), (2, 0.5), (3, 1.0)],
)
def test_dimensional_covariance_factor_is_c_to_d_minus_three(
    dimension: int, expected_factor: float
) -> None:
    scale = 2.0
    literal_measure_scaling = scale**dimension
    scale_factor_cubic_scaling = (1.0 / scale) ** 3
    assert literal_measure_scaling * scale_factor_cubic_scaling == pytest.approx(
        scale ** (dimension - 3)
    )
    assert scale ** (dimension - 3) == pytest.approx(expected_factor)
    assert (dimension == 3) is (expected_factor == 1.0)
