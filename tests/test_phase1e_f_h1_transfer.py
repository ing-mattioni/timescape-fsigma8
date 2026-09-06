"""Scientific validation for the conditional Phase 1E-F H1 realization.

The matrix fixtures below are operator-contract analogues only.  They are not
physical spatial discretisations of Timescape.  Equations under test are the
human-approved Phase 1E-F specification, with inherited CGI/GM equations
cited in the implementation docstrings.
"""

# A06: absolute budgets use rtol=0; relative budgets use atol=0.
# Previously implicit algebraic comparisons use rtol=2e-12, atol=1e-14
# in the fixture units (roundoff allowance); explicit convergence budgets remain.

from __future__ import annotations

from dataclasses import fields
import inspect
from pathlib import Path

import numpy as np
import pytest

import timescape_fsigma8.transfer as transfer
from timescape_fsigma8.transfer import (
    COMMON_REFERENCE_NORMAL_WALL_TO_VOID,
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
    wall_source_injection: np.ndarray | None = None,
    void_source_injection: np.ndarray | None = None,
    flux_normal_convention: str = COMMON_REFERENCE_NORMAL_WALL_TO_VOID,
) -> DenseH1TransmissionBackend:
    """Build a synthetic coupled, constrained operator-contract fixture."""
    identity = np.eye(N)
    value = scale * identity if operator_value is None else operator_value
    operator = matrix_jet(
        value,
        scale_first * identity,
        scale_second * identity,
    )
    wall = (
        np.eye(N)[0]
        if wall_source_injection is None
        else np.asarray(wall_source_injection, dtype=np.float64)
    )
    void = (
        np.eye(N)[-1]
        if void_source_injection is None
        else np.asarray(void_source_injection, dtype=np.float64)
    )
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
        flux_normal_convention=flux_normal_convention,
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


MANUFACTURED_PHI = np.array([5.0, -1.0, -1.0, -1.0, -1.0, -1.0]) / 6.0


def make_nontrivial_dynamic_arguments(
    *,
    operator_second_shift: float = 0.0,
    delta_eff_first_shift: float = 0.0,
) -> tuple[dict[str, object], dict[str, object]]:
    """Build independently specified algebraically compatible manufactured jets.

    The target jets below are manufactured before the realization is called.
    They satisfy the human-approved Phase 1E-F R_Z and R_eff equations with
    nonzero clean-branch terms. The effective-sector input is then solved
    algebraically so the real H1 realization must reproduce those target jets.
    This is not a physical regional dust background or evidence of an all-time
    Timescape trajectory; rho_w.first=0 violates dust conservation for Theta_w=0.6.
    """
    G = 1.0 / (4.0 * np.pi)
    background = make_background(
        f_v=scalar(0.4),
        rho_w=scalar(1.0),
        rho_v=scalar(1.0),
        Theta_w=scalar(0.6),
        Theta_v=scalar(1.2),
        H_w=scalar(0.2),
        H_v=scalar(0.4),
        R_bar_w=scalar(0.0),
        R_bar_v=scalar(2.0),
        Q_bar=scalar(-5.0),
        W_bar=scalar(-3.0),
        Theta=scalar(0.84),
        G=G,
    )
    regional_bulk = RegionalBulkState(
        Delta_w=1.0,
        Z_w=0.4,
        Delta_v=1.0,
        Z_v=0.8,
    )
    backend = make_backend(
        scale=1.0,
        scale_second=operator_second_shift,
        interval_bound=0.5,
        wall_source_injection=MANUFACTURED_PHI,
        void_source_injection=MANUFACTURED_PHI,
    )

    target_Delta_d = 1.0
    target_Z = 0.56
    target_Z_dot = -1.352 + operator_second_shift * target_Delta_d
    target_Delta_eff = 0.0192
    target_Delta_eff_dot = -0.831936 + delta_eff_first_shift
    target_Delta_eff_second = 0.3

    wall = regional_evolution(
        regional_bulk.Delta_w,
        regional_bulk.Z_w,
        alpha=background.alpha_w,
        H=background.H_w,
        rho=background.rho_w,
        Theta=background.Theta_w,
        G=background.G,
    )
    void = regional_evolution(
        regional_bulk.Delta_v,
        regional_bulk.Z_v,
        alpha=background.alpha_v,
        H=background.H_v,
        rho=background.rho_v,
        Theta=background.Theta_v,
        G=background.G,
    )
    curvature_state = backend.solve_joint(
        wall.curvature,
        void.curvature,
        source_name="manufactured-curvature",
    )
    C_R = VectorJet(
        0.6 * curvature_state.wall.field.value
        + 0.4 * curvature_state.void.field.value,
        0.6 * curvature_state.wall.field.first
        + 0.4 * curvature_state.void.field.first,
        0.6 * curvature_state.wall.field.second
        + 0.4 * curvature_state.void.field.second,
    )
    coefficients = two_region_coefficients(background)
    target_effective = VectorJet(
        MANUFACTURED_PHI * target_Delta_eff,
        MANUFACTURED_PHI * target_Delta_eff_dot,
        MANUFACTURED_PHI * target_Delta_eff_second,
    )
    S_eff = background.Q_bar.value + background.W_bar.value
    target_Q = VectorJet(
        (S_eff / 4.0) * target_effective.value,
        (S_eff / 4.0) * target_effective.first,
        (S_eff / 4.0) * target_effective.second,
    )
    effective_scale = coefficients.B_Q.value * coefficients.A_W.value
    E_delta_theta = VectorJet(
        (
            coefficients.A_P.value * target_Q.value
            + coefficients.A_Q.value * C_R.value
        )
        / effective_scale,
        (
            coefficients.A_P.value * target_Q.first
            + coefficients.A_Q.value * C_R.first
        )
        / effective_scale,
        (
            coefficients.A_P.value * target_Q.second
            + coefficients.A_Q.value * C_R.second
        )
        / effective_scale,
    )
    identity_operator = DenseCarrierOperator(matrix_jet(np.eye(N)))
    zero_operator = DenseCarrierOperator(matrix_jet(np.zeros((N, 1))))
    effective_sector = EffectiveSectorContract(
        delta_theta_operator=identity_operator,
        delta_theta_inputs=E_delta_theta,
        delta_xi0_operator=zero_operator,
        delta_xi0_inputs=VectorJet(np.zeros(1), np.zeros(1), np.zeros(1)),
        J_f_Gamma=VectorJet(np.zeros(N), np.zeros(N), np.zeros(N)),
        partition_time_independent=True,
    )
    configuration = make_configuration()
    arguments: dict[str, object] = {
        "regional_bulk": regional_bulk,
        "background": background,
        "backend": backend,
        "effective_sector": effective_sector,
        "configuration": configuration,
    }
    expected: dict[str, object] = {
        "phi": MANUFACTURED_PHI,
        "Delta_d": target_Delta_d,
        "Z": target_Z,
        "Z_dot": target_Z_dot,
        "Delta_eff": target_Delta_eff,
        "Delta_eff_dot": target_Delta_eff_dot,
        "rho_d": 1.0,
        "rho_eff": 2.0,
        "w_eff": 0.5,
        "Theta": 0.84,
        "configuration": configuration,
    }
    return arguments, expected


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
        assert result.delta.first == pytest.approx(-alpha * Z, rel=2e-12, abs=1e-14)
        expected_z = (
            -2.0 * alpha * H * Z
            - 4.0 * np.pi * G * alpha * rho * delta
        )
        assert result.Z.first == pytest.approx(expected_z, rel=2e-12, abs=1e-14)


def test_v2_global_constant_mode_is_removed_exactly_once() -> None:
    backend = make_backend()
    projected = backend.project_source(np.eye(N)[0])
    assert backend.global_mean_constraint_count == 1
    assert backend.total_constraint_rank == backend.interface_constraint_rank + 1
    assert backend.global_mean(projected) == pytest.approx(0.0, abs=1e-14, rel=0.0)
    assert np.sum(projected[:3]) != pytest.approx(0.0, abs=1e-14, rel=0.0)
    assert np.sum(projected[3:]) != pytest.approx(0.0, abs=1e-14, rel=0.0)
    assert np.sum(projected[:3]) == pytest.approx(-np.sum(projected[3:]), rel=2e-12, abs=1e-14)


def test_v3_v4_transmission_value_and_conormal_flux_continuity() -> None:
    backend = make_backend()
    state = backend.solve_joint(
        scalar(2.0, 0.4, -0.3),
        scalar(-1.0, 0.2, 0.5),
        source_name="test",
    )
    for jet in (state.wall.field, state.void.field, state.carrier_field):
        for field in (jet.value, jet.first, jet.second):
            np.testing.assert_allclose(backend.value_jump(field), 0.0, atol=1e-14, rtol=0.0)
            np.testing.assert_allclose(backend.flux_jump(field), 0.0, atol=1e-14, rtol=0.0)


def test_v5_coercivity_guard_fails_closed() -> None:
    with pytest.raises(H1DegeneracyError, match="c_Gamma"):
        make_result(configuration=make_configuration(coercivity_min=1.1))


def test_v6_equal_region_is_fail_closed_degenerate_with_special_zero_numerator_path() -> None:
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
        np.testing.assert_allclose(result.F_v.value, 0.0, atol=1e-14, rtol=0.0)
        # This is only the special numerator-identically-zero path 0/contrast.
        # No generic equal-region limit is inferred.
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
    np.testing.assert_allclose(swapped.Delta_d.value, original.Delta_d.value, rtol=2e-12, atol=1e-14)
    np.testing.assert_allclose(swapped.Z, original.Z, rtol=2e-12, atol=1e-14)
    np.testing.assert_allclose(swapped.Delta_eff.value, original.Delta_eff.value, rtol=2e-12, atol=1e-14)


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
            atol=1e-14, rtol=0.0,
        )
        assert "normalized Delta_eff and w_eff were not evaluated" in str(error)
    else:
        raise AssertionError("effective normalization degeneracy was not rejected")


def test_v10_constitutive_clean_closure_is_verified() -> None:
    result = make_result()
    np.testing.assert_allclose(result.C_P, 0.0, atol=1e-14, rtol=0.0)
    np.testing.assert_allclose(
        result.mathscr_W.value - 3.0 * result.mathscr_Q.value,
        result.C_P,
        atol=1e-14, rtol=0.0,
    )


def test_v11_v12_v13_all_three_canonical_gm_residuals_vanish() -> None:
    result = make_result()
    np.testing.assert_allclose(result.R_Delta, 0.0, atol=1e-14, rtol=0.0)
    np.testing.assert_allclose(result.R_Z, 0.0, atol=1e-14, rtol=0.0)
    np.testing.assert_allclose(result.R_eff, 0.0, atol=1e-14, rtol=0.0)
    np.testing.assert_allclose(result.P_tilde_eff, 0.0, atol=1e-14, rtol=0.0)


def test_nontrivial_manufactured_r_z_and_r_eff_cancellations() -> None:
    arguments, expected = make_nontrivial_dynamic_arguments()
    result = evaluate_h1_realization(**arguments)
    phi = expected["phi"]

    np.testing.assert_allclose(result.Delta_d.value, expected["Delta_d"] * phi, rtol=2e-12, atol=1e-14)
    np.testing.assert_allclose(result.Z, expected["Z"] * phi, rtol=2e-12, atol=1e-14)
    np.testing.assert_allclose(-result.Delta_d.second, expected["Z_dot"] * phi, rtol=2e-12, atol=1e-14)
    np.testing.assert_allclose(result.Delta_eff.value, expected["Delta_eff"] * phi, rtol=2e-12, atol=1e-14)
    np.testing.assert_allclose(
        result.Delta_eff.first,
        expected["Delta_eff_dot"] * phi, rtol=2e-12, atol=1e-14,
    )
    assert result.rho_d == pytest.approx(expected["rho_d"], rel=2e-12, abs=1e-14)
    assert result.rho_eff == pytest.approx(expected["rho_eff"], rel=2e-12, abs=1e-14)
    assert result.w_eff == pytest.approx(expected["w_eff"], rel=2e-12, abs=1e-14)
    assert result.w_eff not in (-1.0, 0.0)
    np.testing.assert_allclose(result.C_P, 0.0, atol=1e-13, rtol=0.0)

    R_Z_terms = (
        -result.Delta_d.second,
        (2.0 / 3.0) * expected["Theta"] * result.Z,
        4.0 * np.pi * arguments["background"].G * result.rho_d * result.Delta_d.value,
        4.0
        * np.pi
        * arguments["background"].G
        * result.rho_eff
        * result.Delta_eff.value,
    )
    assert all(np.max(np.abs(term)) > 1e-4 for term in R_Z_terms)
    independently_reconstructed_R_Z = sum(
        R_Z_terms,
        np.zeros_like(result.R_Z),
    )
    np.testing.assert_allclose(
        independently_reconstructed_R_Z,
        result.R_Z,
        atol=2e-13, rtol=0.0,
    )
    np.testing.assert_allclose(independently_reconstructed_R_Z, 0.0, atol=2e-13, rtol=0.0)

    R_eff_terms = (
        result.Delta_eff.first,
        -result.w_eff
        * expected["Theta"]
        * result.Delta_eff.value,
        (1.0 + result.w_eff) * result.Z,
    )
    assert all(np.max(np.abs(term)) > 1e-4 for term in R_eff_terms)
    independently_reconstructed_R_eff = sum(
        R_eff_terms,
        np.zeros_like(result.R_eff),
    )
    np.testing.assert_allclose(
        independently_reconstructed_R_eff,
        result.R_eff,
        atol=2e-13, rtol=0.0,
    )
    np.testing.assert_allclose(independently_reconstructed_R_eff, 0.0, atol=2e-13, rtol=0.0)


def test_adversarial_second_density_jet_produces_predictable_r_z_failure() -> None:
    shift = 0.12
    arguments, expected = make_nontrivial_dynamic_arguments(
        operator_second_shift=shift,
    )
    expected_increment = shift * expected["Delta_d"] * expected["phi"]
    tolerance = expected["configuration"].R_Z_tolerance
    assert np.max(np.abs(expected_increment)) > tolerance
    with pytest.raises(H1ClosureError, match=r"^R_Z=") as error:
        evaluate_h1_realization(**arguments)
    measured_magnitude = float(str(error.value).split("=", 1)[1].split()[0])
    assert measured_magnitude == pytest.approx(np.max(np.abs(expected_increment)), rel=2e-12, abs=1e-14)


def test_adversarial_effective_first_jet_produces_predictable_r_eff_failure() -> None:
    shift = -0.07
    arguments, expected = make_nontrivial_dynamic_arguments(
        delta_eff_first_shift=shift,
    )
    expected_increment = shift * expected["phi"]
    tolerance = expected["configuration"].R_eff_tolerance
    assert np.max(np.abs(expected_increment)) > tolerance
    with pytest.raises(H1ClosureError, match=r"^R_eff=") as error:
        evaluate_h1_realization(**arguments)
    measured_magnitude = float(str(error.value).split("=", 1)[1].split()[0])
    assert measured_magnitude == pytest.approx(np.max(np.abs(expected_increment)), rel=2e-12, abs=1e-14)


def test_v14_gm_curvature_is_derived_and_constraint_residual_vanishes() -> None:
    result = make_result()
    expected = (
        -(4.0 / 3.0) * make_background().Theta.value * result.Z
        + 16.0
        * np.pi
        * (result.rho_d * result.Delta_d.value + result.rho_eff * result.Delta_eff.value)
    )
    np.testing.assert_allclose(result.R_GM, expected, atol=1e-14, rtol=0.0)
    np.testing.assert_allclose(result.K_GM, 0.0, atol=1e-14, rtol=0.0)
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
    assert np.max(np.abs(backend.value_jump(broken))) == pytest.approx(1e-3, rel=2e-12, abs=1e-14)
    broken_flux = field.copy()
    broken_flux[1] += 2e-3
    assert np.max(np.abs(backend.flux_jump(broken_flux))) == pytest.approx(2e-3, rel=2e-12, abs=1e-14)


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
            recovered.value, solution.injected_source.value, atol=1e-13, rtol=0.0
        )
        np.testing.assert_allclose(
            recovered.first, solution.injected_source.first, atol=1e-13, rtol=0.0
        )
        np.testing.assert_allclose(
            recovered.second, solution.injected_source.second, atol=1e-13, rtol=0.0
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
    assert result.framework_status == "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
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
        atol=1e-13, rtol=0.0,
    )


def test_wall_void_source_injections_are_linear_and_provenance_preserving() -> None:
    backend = make_backend()
    first = backend.solve_joint(scalar(1.2), scalar(-0.4), source_name="linear")
    second = backend.solve_joint(scalar(-0.3), scalar(0.8), source_name="linear")
    summed = backend.solve_joint(scalar(0.9), scalar(0.4), source_name="linear")
    np.testing.assert_allclose(
        first.carrier_field.value + second.carrier_field.value,
        summed.carrier_field.value,
        atol=1e-14, rtol=0.0,
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
    np.testing.assert_allclose(result.Delta_d.value, expected, atol=1e-14, rtol=0.0)
    assert d_f != 0.0


def test_effective_background_matches_gm_equations_3_12_and_3_13() -> None:
    result = make_result()
    assert result.rho_eff == pytest.approx(1.0 / (8.0 * np.pi), rel=2e-12, abs=1e-14)
    assert result.p_eff == pytest.approx(-1.0 / (8.0 * np.pi), rel=2e-12, abs=1e-14)
    assert result.w_eff == pytest.approx(-1.0, rel=2e-12, abs=1e-14)


def test_target_expansion_is_only_the_analytic_density_derivative() -> None:
    result = make_result()
    np.testing.assert_allclose(result.Z, -result.Delta_d.first, atol=0.0, rtol=0.0)


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
        atol=1e-14, rtol=0.0,
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


def test_analytic_second_derivative_matches_independent_finite_difference() -> None:
    phi = MANUFACTURED_PHI

    def operator_scale(time: float) -> float:
        return 2.0 + 0.3 * time + 0.2 * time**2

    def source_scale(time: float) -> float:
        return 1.1 - 0.4 * time + 0.15 * time**2

    analytic_backend = make_backend(
        scale=operator_scale(0.0),
        scale_first=0.3,
        scale_second=0.4,
        interval_bound=1.0,
    )
    analytic = analytic_backend.solve_source_jet(
        VectorJet(phi * 1.1, phi * -0.4, phi * 0.3),
        provenance="manufactured-second-derivative",
    )

    errors: list[float] = []
    finite_difference = np.zeros_like(phi)
    for step in (0.02, 0.01, 0.005):
        values = []
        for time in (step, 0.0, -step):
            backend = make_backend(
                scale=operator_scale(time),
                interval_bound=1.0,
            )
            solution = backend.solve_source_jet(
                VectorJet(
                    phi * source_scale(time),
                    np.zeros(N),
                    np.zeros(N),
                ),
                provenance="finite-difference-value-solve",
            )
            values.append(solution.field.value)
        finite_difference = (values[0] - 2.0 * values[1] + values[2]) / step**2
        errors.append(float(np.max(np.abs(finite_difference - analytic.field.second))))

    assert errors[1] < errors[0]
    assert errors[2] < errors[1]
    np.testing.assert_allclose(
        finite_difference,
        analytic.field.second,
        rtol=2e-5,
        atol=2e-9,
    )


def test_common_reference_normal_matches_opposite_outward_fluxes() -> None:
    wall_outward = np.array([-1.0, 1.0, 0.0, 0.0])
    void_outward = np.array([0.0, 0.0, 1.0, -1.0])
    void_common_reference = -void_outward
    common_reference_jump = wall_outward - void_common_reference
    value_jump = np.array([[0.0, 1.0, -1.0, 0.0]])
    state = np.array([-1.0, 0.0, 0.0, 1.0])

    backend = DenseH1TransmissionBackend(
        operator=matrix_jet(2.0 * np.eye(4)),
        wall_source_injection=np.eye(4)[0],
        void_source_injection=np.eye(4)[-1],
        value_jump_operator=value_jump,
        flux_jump_operator=common_reference_jump[np.newaxis, :],
        flux_normal_convention=COMMON_REFERENCE_NORMAL_WALL_TO_VOID,
        global_mean_weights=np.ones(4),
        constraint_rank_tolerance=1e-12,
        symmetry_tolerance=1e-12,
        operator_time_regularity="C2_COMMON_TIME",
        fixed_reference_constraints=True,
        interval_coercivity_lower_bound=1.0,
    )
    solution = backend.solve_source_jet(
        VectorJet(2.0 * state, np.zeros(4), np.zeros(4)),
        provenance="one-dimensional-oriented-interface",
    )
    np.testing.assert_allclose(solution.field.value, state, atol=1e-14, rtol=0.0)

    j_wall_out = wall_outward @ state
    j_void_out = void_outward @ state
    q_wall = j_wall_out
    q_void = void_common_reference @ state
    assert j_wall_out == pytest.approx(1.0, rel=2e-12, abs=1e-14)
    assert j_void_out == pytest.approx(-1.0, rel=2e-12, abs=1e-14)
    assert q_wall == pytest.approx(1.0, rel=2e-12, abs=1e-14)
    assert q_void == pytest.approx(1.0, rel=2e-12, abs=1e-14)
    assert j_wall_out + j_void_out == pytest.approx(0.0, rel=2e-12, abs=1e-14)
    assert q_wall - q_void == pytest.approx(0.0, rel=2e-12, abs=1e-14)
    np.testing.assert_allclose(backend.flux_jump(state), 0.0, atol=1e-14, rtol=0.0)

    wrong_same_outward_sign = wall_outward + void_common_reference
    assert wrong_same_outward_sign @ state == pytest.approx(2.0, rel=2e-12, abs=1e-14)


def test_single_common_constant_null_mode_is_removed_by_global_normalization() -> None:
    constant_projector = np.ones((N, N)) / N
    operator = np.eye(N) - constant_projector
    backend = make_backend(
        operator_value=operator,
        interval_bound=0.9,
    )
    assert backend.global_mean_constraint_count == 1
    assert backend.instantaneous_coercivity_lower_bound == pytest.approx(1.0, rel=2e-12, abs=1e-14)
    state = backend.solve_joint(scalar(1.0), scalar(1.0), source_name="null-mode")
    assert backend.global_mean(state.carrier_field.value) == pytest.approx(
        0.0, abs=1e-14, rel=0.0
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
    assert signature.parameters[
        "flux_normal_convention"
    ].default is inspect.Parameter.empty
    backend = make_backend()
    assert backend.operator_time_regularity == "C2_COMMON_TIME"
    assert backend.fixed_reference_constraints is True
    assert (
        backend.flux_normal_convention
        == COMMON_REFERENCE_NORMAL_WALL_TO_VOID
    )
    with pytest.raises(ValueError, match="flux_normal_convention"):
        make_backend(flux_normal_convention="REGIONAL_OUTWARD_NORMALS")
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
    assert coefficients.A_P.value == pytest.approx(expected_a_p, rel=2e-12, abs=1e-14)
    assert coefficients.A_P.value == pytest.approx(
        coefficients.A_W.value - 3.0 * coefficients.A_Q.value, rel=2e-12, abs=1e-14
    )
    assert coefficients.B_P.value == pytest.approx(expected_b_p, rel=2e-12, abs=1e-14)
    assert coefficients.B_P.value == pytest.approx(-3.0 * coefficients.B_Q.value, rel=2e-12, abs=1e-14)


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
    assert transfer.FRAMEWORK_STATUS == "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
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
