"""Scientific validation for the conditional Phase 1E-F H1 realization.

The matrix fixtures below are operator-contract analogues only.  They are not
physical spatial discretisations of Timescape.  Equations under test are the
human-approved Phase 1E-F specification, with inherited CGI/GM equations
cited in the implementation docstrings.
"""

from __future__ import annotations

from dataclasses import fields
import inspect
from pathlib import Path

import numpy as np
import pytest

import timescape_fsigma8.transfer as transfer
from timescape_fsigma8.transfer import (
    DenseCarrierOperator,
    DenseH1TransmissionBackend,
    EffectiveSectorContract,
    H1Background,
    H1ClosureError,
    H1Configuration,
    H1ContractError,
    H1DegeneracyError,
    H1EffectiveNormalizationError,
    MatrixJet,
    RegionalBulkState,
    ScalarJet,
    VectorJet,
    compatibility_mismatch_rhs,
    evaluate_h1_realization,
    regional_evolution,
    two_region_coefficients,
    validate_clean_diagnostics,
)


N = 6
ZERO = ScalarJet(0.0, 0.0, 0.0)


def scalar(value: float, first: float = 0.0, second: float = 0.0) -> ScalarJet:
    return ScalarJet(value, first, second)


def matrix_jet(
    value: np.ndarray,
    first: np.ndarray | None = None,
    second: np.ndarray | None = None,
) -> MatrixJet:
    if first is None:
        first = np.zeros_like(value)
    if second is None:
        second = np.zeros_like(value)
    return MatrixJet(value, first, second)


def make_backend(
    *,
    scale: float = 2.0,
    scale_first: float = 0.0,
    scale_second: float = 0.0,
    interval_bound: float = 1.0,
    reverse_regions: bool = False,
    operator_value: np.ndarray | None = None,
) -> DenseH1TransmissionBackend:
    """Build a synthetic coupled, constrained operator-contract fixture."""
    identity = np.eye(N)
    value = scale * identity if operator_value is None else operator_value
    operator = matrix_jet(
        value,
        scale_first * identity,
        scale_second * identity,
    )
    wall = np.eye(N)[0]
    void = np.eye(N)[-1]
    value_jump = np.array([[0.0, 0.0, 1.0, -1.0, 0.0, 0.0]])
    flux_jump = np.array([[0.0, 1.0, 0.0, 0.0, -1.0, 0.0]])
    if reverse_regions:
        permutation = np.eye(N)[::-1]
        wall, void = void, wall
        value_jump = value_jump @ permutation
        flux_jump = flux_jump @ permutation
    return DenseH1TransmissionBackend(
        operator=operator,
        wall_source_injection=wall,
        void_source_injection=void,
        value_jump_operator=value_jump,
        flux_jump_operator=flux_jump,
        global_mean_weights=np.ones(N),
        constraint_rank_tolerance=1e-12,
        symmetry_tolerance=1e-12,
        operator_time_regularity="C2_COMMON_TIME",
        fixed_reference_constraints=True,
        interval_coercivity_lower_bound=interval_bound,
    )


def make_background(**changes: ScalarJet | float) -> H1Background:
    values: dict[str, ScalarJet | float] = {
        "f_v": scalar(0.4),
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


def make_effective_contract(
    *,
    J_f: VectorJet | None = None,
    partition_time_independent: bool = True,
) -> EffectiveSectorContract:
    zero_operator = DenseCarrierOperator(matrix_jet(np.zeros((N, 4))))
    zero_inputs = VectorJet(np.zeros(4), np.zeros(4), np.zeros(4))
    if J_f is None:
        J_f = VectorJet(np.zeros(N), np.zeros(N), np.zeros(N))
    return EffectiveSectorContract(
        delta_theta_operator=zero_operator,
        delta_theta_inputs=zero_inputs,
        delta_xi0_operator=zero_operator,
        delta_xi0_inputs=zero_inputs,
        J_f_Gamma=J_f,
        partition_time_independent=partition_time_independent,
    )


def make_configuration(**changes: float) -> H1Configuration:
    values = {
        "A_P_min": 1e-8,
        "effective_denominator_min": 1e-8,
        "coercivity_min": 0.5,
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
        "background_identity_tolerance": 1e-12,
    }
    values.update(changes)
    return H1Configuration(**values)


def make_result(
    *,
    regional_bulk: RegionalBulkState | None = None,
    background: H1Background | None = None,
    backend: DenseH1TransmissionBackend | None = None,
    effective_sector: EffectiveSectorContract | None = None,
    configuration: H1Configuration | None = None,
):
    return evaluate_h1_realization(
        regional_bulk=regional_bulk
        or RegionalBulkState(Delta_w=0.0, Z_w=1.0, Delta_v=0.0, Z_v=1.0),
        background=background or make_background(),
        backend=backend or make_backend(),
        effective_sector=effective_sector or make_effective_contract(),
        configuration=configuration or make_configuration(),
    )


def test_v1_regional_exact_equations_include_common_time_alpha() -> None:
    regional_cases = (
        (0.3, -0.4, 1.7, 0.2, 0.8, 0.9),
        (-0.2, 0.6, 0.75, 0.5, 1.1, 0.9),
    )
    for delta, Z, alpha, H, rho, G in regional_cases:
        result = regional_evolution(
            delta,
            Z,
            alpha=scalar(alpha),
            H=scalar(H),
            rho=scalar(rho),
            Theta=scalar(3.0 * H),
            G=G,
        )
        assert result.delta.first == pytest.approx(-alpha * Z)
        expected_z = (
            -2.0 * alpha * H * Z
            - 4.0 * np.pi * G * alpha * rho * delta
        )
        assert result.Z.first == pytest.approx(expected_z)


def test_v2_global_constant_mode_is_removed_exactly_once() -> None:
    backend = make_backend()
    projected = backend.project_source(np.eye(N)[0])
    assert backend.global_mean_constraint_count == 1
    assert backend.total_constraint_rank == backend.interface_constraint_rank + 1
    assert backend.global_mean(projected) == pytest.approx(0.0, abs=1e-14)
    assert np.sum(projected[:3]) != pytest.approx(0.0, abs=1e-14)
    assert np.sum(projected[3:]) != pytest.approx(0.0, abs=1e-14)
    assert np.sum(projected[:3]) == pytest.approx(-np.sum(projected[3:]))


def test_v3_v4_transmission_value_and_conormal_flux_continuity() -> None:
    backend = make_backend()
    state = backend.solve_joint(
        scalar(2.0, 0.4, -0.3),
        scalar(-1.0, 0.2, 0.5),
        source_name="test",
    )
    for jet in (state.wall.field, state.void.field, state.carrier_field):
        for field in (jet.value, jet.first, jet.second):
            np.testing.assert_allclose(backend.value_jump(field), 0.0, atol=1e-14)
            np.testing.assert_allclose(backend.flux_jump(field), 0.0, atol=1e-14)


def test_v5_coercivity_guard_fails_closed() -> None:
    with pytest.raises(H1DegeneracyError, match="c_Gamma"):
        make_result(configuration=make_configuration(coercivity_min=1.1))


def test_v6_equal_region_clean_limit_and_exact_degeneracy() -> None:
    bulk = RegionalBulkState(0.0, 0.0, 0.0, 0.0)
    equal_background = make_background(R_bar_v=ZERO)
    equal_coefficients = two_region_coefficients(equal_background)
    for coefficient in (
        equal_coefficients.d_Theta,
        equal_coefficients.A_W,
        equal_coefficients.A_Q,
        equal_coefficients.B_Q,
        equal_coefficients.A_P,
        equal_coefficients.B_P,
    ):
        assert coefficient.value == 0.0
    for contrast in (1.0, 0.1, 0.01):
        result = make_result(
            regional_bulk=bulk,
            background=make_background(R_bar_v=scalar(contrast)),
        )
        np.testing.assert_allclose(result.F_v.value, 0.0, atol=1e-14)
    with pytest.raises(H1DegeneracyError, match=r"A_P"):
        make_result(
            regional_bulk=bulk,
            background=equal_background,
        )


def test_v7_wall_void_relabelling_is_carrier_covariant() -> None:
    original = make_result(
        regional_bulk=RegionalBulkState(0.0, 1.0, 0.0, 2.0),
    )
    swapped_background = make_background(
        f_v=scalar(0.6),
        R_bar_w=scalar(2.0),
        R_bar_v=ZERO,
    )
    swapped = make_result(
        regional_bulk=RegionalBulkState(0.0, 2.0, 0.0, 1.0),
        background=swapped_background,
        backend=make_backend(reverse_regions=True),
    )
    np.testing.assert_allclose(swapped.Delta_d.value, original.Delta_d.value)
    np.testing.assert_allclose(swapped.Z, original.Z)
    np.testing.assert_allclose(swapped.Delta_eff.value, original.Delta_eff.value)


@pytest.mark.parametrize("f_v", [0.0, 1.0])
def test_v8_single_region_endpoints_are_explicit_ontology_reductions(f_v: float) -> None:
    with pytest.raises(
        H1DegeneracyError,
        match="SINGLE_REGION_ONTOLOGY_REDUCTION_REQUIRED",
    ):
        make_result(background=make_background(f_v=scalar(f_v)))


def test_v9_normalized_effective_density_rejects_zero_denominator() -> None:
    try:
        make_result(background=make_background(W_bar=scalar(-1.0)))
    except H1EffectiveNormalizationError as error:
        diagnostics = error.diagnostics
        assert diagnostics.background_Q_plus_W.value == 0.0
        np.testing.assert_allclose(
            diagnostics.C_P.value,
            diagnostics.mathscr_W.value - 3.0 * diagnostics.mathscr_Q.value,
            atol=1e-14,
        )
        assert "normalized Delta_eff and w_eff were not evaluated" in str(error)
    else:
        raise AssertionError("effective normalization degeneracy was not rejected")


def test_v10_constitutive_clean_closure_is_verified() -> None:
    result = make_result()
    np.testing.assert_allclose(result.C_P, 0.0, atol=1e-14)
    np.testing.assert_allclose(
        result.mathscr_W.value - 3.0 * result.mathscr_Q.value,
        result.C_P,
        atol=1e-14,
    )


def test_v11_v12_v13_all_three_canonical_gm_residuals_vanish() -> None:
    result = make_result()
    np.testing.assert_allclose(result.R_Delta, 0.0, atol=1e-14)
    np.testing.assert_allclose(result.R_Z, 0.0, atol=1e-14)
    np.testing.assert_allclose(result.R_eff, 0.0, atol=1e-14)
    np.testing.assert_allclose(result.P_tilde_eff, 0.0, atol=1e-14)


def test_v14_gm_curvature_is_derived_and_constraint_residual_vanishes() -> None:
    result = make_result()
    expected = (
        -(4.0 / 3.0) * make_background().Theta.value * result.Z
        + 16.0
        * np.pi
        * (result.rho_d * result.Delta_d.value + result.rho_eff * result.Delta_eff.value)
    )
    np.testing.assert_allclose(result.R_GM, expected, atol=1e-14)
    np.testing.assert_allclose(result.K_GM, 0.0, atol=1e-14)
    assert "R_GM" not in {field.name for field in fields(RegionalBulkState)}


def test_v15_zero_compatibility_mismatch_propagates_as_zero() -> None:
    result = make_result()
    np.testing.assert_array_equal(result.compatibility_zero_rhs, np.zeros(3))
    np.testing.assert_array_equal(
        compatibility_mismatch_rhs(
            np.zeros(3),
            Theta=0.7,
            rho_d=1.2,
            rho_eff=-0.1,
            w_eff=-0.8,
            G=1.0,
        ),
        np.zeros(3),
    )


def test_v16_deliberately_broken_transmission_is_detected() -> None:
    backend = make_backend()
    field = backend.solve_joint(scalar(1.0), scalar(0.0), source_name="broken").carrier_field.value
    broken = field.copy()
    broken[2] += 1e-3
    assert np.max(np.abs(backend.value_jump(broken))) == pytest.approx(1e-3)
    broken_flux = field.copy()
    broken_flux[1] += 2e-3
    assert np.max(np.abs(backend.flux_jump(broken_flux))) == pytest.approx(2e-3)


def test_v17_broken_constitutive_closure_stays_separate_from_c_eff() -> None:
    with pytest.raises(H1ClosureError, match=r"^C_P="):
        validate_clean_diagnostics(
            C_P=np.array([1e-3]),
            R_Delta=np.zeros(1),
            R_Z=np.zeros(1),
            R_eff=np.zeros(1),
            K_GM=np.zeros(1),
            configuration=make_configuration(),
        )


def test_v18_public_h1_api_has_no_ambiguous_generic_k_parameter() -> None:
    public_callables = (
        DenseH1TransmissionBackend,
        EffectiveSectorContract,
        H1Background,
        RegionalBulkState,
        evaluate_h1_realization,
        regional_evolution,
        two_region_coefficients,
    )
    for callable_object in public_callables:
        assert "k" not in inspect.signature(callable_object).parameters


def test_v19_no_observational_runtime_is_exported() -> None:
    forbidden = ("rsd", "tracer", "survey", "likelihood", "sigma8", "fsigma8")
    callable_names = {
        name.lower()
        for name in transfer.__all__
        if callable(getattr(transfer, name))
    }
    for token in forbidden:
        assert not any(token in name for name in callable_names)
    assert transfer.OBSERVATIONAL_IMPLEMENTATION_AUTHORIZATION == "NOT_GRANTED"
    assert transfer.RSD_IMPLEMENTATION_AUTHORIZATION == "NOT_GRANTED"
    assert transfer.FSIGMA8_IMPLEMENTATION_AUTHORIZATION == "NOT_GRANTED"


def test_v20_provenance_source_roundtrip_includes_analytic_derivatives() -> None:
    backend = make_backend(scale_first=0.3, scale_second=-0.1)
    state = backend.solve_joint(
        scalar(2.0, 0.7, -0.2),
        scalar(-1.0, 0.5, 0.9),
        source_name="roundtrip",
    )
    for solution in (state.wall, state.void):
        recovered = backend.apply_coupled_operator_jet(solution.field)
        np.testing.assert_allclose(
            recovered.value, solution.injected_source.value, atol=1e-13
        )
        np.testing.assert_allclose(
            recovered.first, solution.injected_source.first, atol=1e-13
        )
        np.testing.assert_allclose(
            recovered.second, solution.injected_source.second, atol=1e-13
        )


def test_result_exposes_required_scientific_record_without_target_inverse() -> None:
    result = make_result()
    required = {
        "regional_bulk",
        "transmission_state",
        "F_v",
        "J_Xi",
        "mathscr_Q",
        "mathscr_W",
        "Delta_d",
        "Z",
        "Delta_eff",
        "R_GM",
        "C_P",
        "R_Delta",
        "R_Z",
        "R_eff",
        "K_GM",
        "transmission_value_jump",
        "transmission_flux_jump",
        "coercivity_lower_bound",
        "nondegeneracy_margins",
    }
    assert required <= {field.name for field in fields(type(result))}
    assert result.framework_status == "COMPATIBLE_IMPORTED_DYNAMICS"
    assert result.scientific_status == "CONDITIONALLY_CLOSED"
    assert result.observational_status == "NON_OBSERVATIONAL"
    assert result.fsigma8_status == "NOT_FSIGMA8"
    assert result.scientific_implementation_authorization == "GRANTED"
    assert result.prototype_authorization == "GRANTED"
    assert result.observational_implementation_authorization == "NOT_GRANTED"
    assert {
        "f_v",
        "f_w",
        "f_v * f_w",
        "|A_P|",
        "|Q_bar + W_bar|",
        "c_Gamma",
    } <= set(result.nondegeneracy_margins)
    assert not hasattr(result, "inverse")
    assert not hasattr(result, "regional_state_from_target")


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"R_bar_v": ZERO}, "A_P"),
        ({"W_bar": scalar(-1.0)}, r"Q_bar.W_bar"),
        ({"alpha_w": ZERO}, "alpha"),
    ],
)
def test_named_nondegeneracy_guards_fail_closed(
    changes: dict[str, ScalarJet],
    message: str,
) -> None:
    with pytest.raises(H1DegeneracyError, match=message):
        make_result(background=make_background(**changes))


def test_partition_product_guard_fails_before_any_division() -> None:
    with pytest.raises(H1DegeneracyError, match=r"f_v.f_w"):
        make_result(
            background=make_background(f_v=scalar(1e-4)),
            configuration=make_configuration(partition_product_min=1e-3),
        )


def test_explicit_effective_operators_and_partition_commutator_are_required() -> None:
    signature = inspect.signature(EffectiveSectorContract)
    for name in (
        "delta_theta_operator",
        "delta_theta_inputs",
        "delta_xi0_operator",
        "delta_xi0_inputs",
        "J_f_Gamma",
        "partition_time_independent",
    ):
        assert signature.parameters[name].default is inspect.Parameter.empty
    with pytest.raises(TypeError):
        EffectiveSectorContract()  # type: ignore[call-arg]


def test_time_independent_partition_requires_explicit_zero_commutator() -> None:
    nonzero = VectorJet(np.ones(N), np.zeros(N), np.zeros(N))
    with pytest.raises(H1ContractError, match="explicitly zero J_f_Gamma"):
        make_effective_contract(J_f=nonzero, partition_time_independent=True)
    contract = make_effective_contract(
        J_f=nonzero,
        partition_time_independent=False,
    )
    baseline = make_result()
    result = make_result(effective_sector=contract)
    np.testing.assert_allclose(
        result.J_Xi,
        baseline.J_Xi - np.ones(N) / 0.24,
        atol=1e-13,
    )


def test_wall_void_source_injections_are_linear_and_provenance_preserving() -> None:
    backend = make_backend()
    first = backend.solve_joint(scalar(1.2), scalar(-0.4), source_name="linear")
    second = backend.solve_joint(scalar(-0.3), scalar(0.8), source_name="linear")
    summed = backend.solve_joint(scalar(0.9), scalar(0.4), source_name="linear")
    np.testing.assert_allclose(
        first.carrier_field.value + second.carrier_field.value,
        summed.carrier_field.value,
        atol=1e-14,
    )
    assert first.wall.provenance == "wall:linear"
    assert first.void.provenance == "void:linear"


def test_mass_weighted_dust_transfer_retains_regional_weights_and_d_f_term() -> None:
    background = make_background(rho_w=scalar(2.0), rho_v=scalar(3.0))
    diagnostic_config = make_configuration(
        R_Z_tolerance=1e6,
        R_eff_tolerance=1e6,
    )
    result = make_result(
        regional_bulk=RegionalBulkState(0.2, 0.0, -0.1, 0.0),
        background=background,
        configuration=diagnostic_config,
    )
    f_v = background.f_v.value
    f_w = 1.0 - f_v
    rho_d = f_w * background.rho_w.value + f_v * background.rho_v.value
    m_w = f_w * background.rho_w.value / rho_d
    m_v = f_v * background.rho_v.value / rho_d
    d_f = (background.rho_v.value - background.rho_w.value) / rho_d
    expected = (
        m_w * result.transmission_state.density.wall.field.value
        + m_v * result.transmission_state.density.void.field.value
        + d_f * result.F_v.value
    )
    np.testing.assert_allclose(result.Delta_d.value, expected, atol=1e-14)
    assert d_f != 0.0


def test_effective_background_matches_gm_equations_3_12_and_3_13() -> None:
    result = make_result()
    assert result.rho_eff == pytest.approx(1.0 / (8.0 * np.pi))
    assert result.p_eff == pytest.approx(-1.0 / (8.0 * np.pi))
    assert result.w_eff == pytest.approx(-1.0)


def test_target_expansion_is_only_the_analytic_density_derivative() -> None:
    result = make_result()
    np.testing.assert_allclose(result.Z, -result.Delta_d.first, atol=0.0)


def test_analytic_operator_derivative_matches_independent_finite_difference() -> None:
    scale = 2.0
    scale_dot = 0.4
    backend = make_backend(scale=scale, scale_first=scale_dot)
    analytic = backend.solve_joint(scalar(1.3), scalar(-0.2), source_name="derivative")
    combined_source = (
        analytic.wall.raw_source.value + analytic.void.raw_source.value
    )
    np.testing.assert_allclose(
        backend.apply_inverse_derivative(combined_source),
        analytic.carrier_field.first,
        atol=1e-14,
    )
    step = 1e-6
    plus = make_backend(scale=scale + step * scale_dot).solve_joint(
        scalar(1.3), scalar(-0.2), source_name="derivative"
    )
    minus = make_backend(scale=scale - step * scale_dot).solve_joint(
        scalar(1.3), scalar(-0.2), source_name="derivative"
    )
    finite_difference = (
        plus.carrier_field.value - minus.carrier_field.value
    ) / (2.0 * step)
    np.testing.assert_allclose(
        analytic.carrier_field.first,
        finite_difference,
        rtol=2e-9,
        atol=2e-11,
    )


def test_single_common_constant_null_mode_is_removed_by_global_normalization() -> None:
    constant_projector = np.ones((N, N)) / N
    operator = np.eye(N) - constant_projector
    backend = make_backend(
        operator_value=operator,
        interval_bound=0.9,
    )
    assert backend.global_mean_constraint_count == 1
    assert backend.instantaneous_coercivity_lower_bound == pytest.approx(1.0)
    state = backend.solve_joint(scalar(1.0), scalar(1.0), source_name="null-mode")
    assert backend.global_mean(state.carrier_field.value) == pytest.approx(
        0.0, abs=1e-14
    )


def test_deliberately_noncoercive_matrix_fixture_is_rejected() -> None:
    for operator in (np.zeros((N, N)), -np.eye(N)):
        with pytest.raises(ValueError, match="coercivity"):
            make_backend(
                operator_value=operator,
                interval_bound=0.1,
            )


def test_operator_regularities_and_fixed_lagrangian_constraints_are_explicit() -> None:
    signature = inspect.signature(DenseH1TransmissionBackend)
    assert signature.parameters["operator_time_regularity"].default is inspect.Parameter.empty
    assert signature.parameters["fixed_reference_constraints"].default is inspect.Parameter.empty
    assert signature.parameters[
        "interval_coercivity_lower_bound"
    ].default is inspect.Parameter.empty
    backend = make_backend()
    assert backend.operator_time_regularity == "C2_COMMON_TIME"
    assert backend.fixed_reference_constraints is True
    configuration_signature = inspect.signature(H1Configuration)
    assert all(
        parameter.default is inspect.Parameter.empty
        for parameter in configuration_signature.parameters.values()
    )


def test_two_region_coefficients_evaluate_both_authorized_algebraic_forms() -> None:
    background = make_background(
        f_v=scalar(0.3),
        Theta_w=scalar(0.6),
        Theta_v=scalar(1.5),
        H_w=scalar(0.2),
        H_v=scalar(0.5),
    )
    coefficients = two_region_coefficients(background)
    d_theta = 0.9
    expected_a_p = (
        background.R_bar_v.value
        - background.R_bar_w.value
        - 2.0 * (1.0 - 2.0 * background.f_v.value) * d_theta**2
    )
    expected_b_p = -4.0 * background.f_v.value * (1.0 - background.f_v.value) * d_theta
    assert coefficients.A_P.value == pytest.approx(expected_a_p)
    assert coefficients.A_P.value == pytest.approx(
        coefficients.A_W.value - 3.0 * coefficients.A_Q.value
    )
    assert coefficients.B_P.value == pytest.approx(expected_b_p)
    assert coefficients.B_P.value == pytest.approx(-3.0 * coefficients.B_Q.value)


def test_regional_bulk_rank_and_algebraic_variables_do_not_add_differential_states() -> None:
    assert [field.name for field in fields(RegionalBulkState)] == [
        "Delta_w",
        "Z_w",
        "Delta_v",
        "Z_v",
    ]
    result = make_result()
    assert isinstance(result.F_v, VectorJet)
    assert isinstance(result.J_Xi, np.ndarray)


def test_d3_variant_firewall_is_unchanged_and_has_no_default() -> None:
    source = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "timescape_fsigma8"
        / "perturbations"
        / "barotropic.py"
    ).read_text(encoding="utf-8")
    assert 'PRINTED_4_15 = "printed_4_15"' in source
    assert 'DERIVED_4_10 = "derived_4_10"' in source
    assert "DEFAULT" not in source


def test_phase1e_f_authorization_and_nonobservational_status_tokens() -> None:
    assert transfer.REALIZATION_ID == "H1-1E-F-CLEAN-NONDEGENERATE-TRANSMISSION-V1"
    assert transfer.FRAMEWORK_STATUS == "COMPATIBLE_IMPORTED_DYNAMICS"
    assert transfer.SCIENTIFIC_STATUS == "CONDITIONALLY_CLOSED"
    assert transfer.OBSERVATIONAL_STATUS == "NON_OBSERVATIONAL"
    assert transfer.FSIGMA8_STATUS == "NOT_FSIGMA8"
    assert (
        transfer.CARRIER_REFERENCE_TOPOLOGY
        == "T3_TWO_DOMAIN_FIXED_LAGRANGIAN_REFERENCE"
    )
    assert transfer.INTERFACE_ONTOLOGY == "MATHEMATICAL_CARRIER_TRANSFER_INTERFACE"
    assert transfer.SCIENTIFIC_IMPLEMENTATION_AUTHORIZATION == "GRANTED"
    assert transfer.PROTOTYPE_AUTHORIZATION == "GRANTED"
