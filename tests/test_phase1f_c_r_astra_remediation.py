"""Independent adversaries and numerical references for Astra A01--A07.

The fixtures are algebraic validation data, not physical Timescape histories.
Equation sources: BMR (2.5)--(2.7), (3.1), arXiv:1912.04213v2;
Short--Coles growth Eq. (3), astro-ph/0605013v2; the authorized A01 contract.
"""

import ast
from dataclasses import replace
from pathlib import Path
import sys

import numpy as np
import pytest
from scipy.integrate import quad

from timescape_fsigma8.components import ComponentRepresentation, orthonormal_components
from timescape_fsigma8.perturbations.initial_conditions import PLANCK_2018_QPLUS_RECIPE, qplus
from timescape_fsigma8.phase1f_c import (
    EXTERNAL_CLOSURE_INPUT, MetricTraceBackgroundSplit,
    Phase1FCMetricReconstructionError, Phase1FCSpatialClosureError,
    ScalarMetricTraceInitialData, derive_clock_anchored_wall_kinematic_geometry,
    reconstruct_optional_scalar_metric_trace,
)
from timescape_fsigma8.scientific_status import CURRENT_SCIENTIFIC_STATUS
from timescape_fsigma8.transfer import ContinuumContractError, conformal_regional_geometry
from test_phase1e_g_continuum_h1 import make_operator, metric_normalization
from test_phase1f_c_wall_common_geometry import make_case, numerics


@pytest.mark.parametrize("role", ["wall", "void", "target"])
def test_a01_mean_preserving_inconsistent_measure_rejected(role):
    operator = make_operator(shape=(4, 4, 4))
    geometry = operator.carrier.target_geometry if role == "target" else getattr(operator, f"{role}_geometry")
    y = np.indices((4, 4, 4))[1]
    wrong = 1.0 + 0.2 * np.sin(2.0 * np.pi * y / 4.0)
    mask = np.ones_like(y, dtype=bool) if role == "target" else getattr(operator.morphology, f"{role}_domain")
    weights = operator.carrier.reference_measure_weights
    # The attack preserves the integrated measure even region by region.
    np.testing.assert_allclose(np.sum(weights * mask * wrong), np.sum(weights * mask), rtol=0.0, atol=2e-16)
    with pytest.raises(ContinuumContractError, match="pointwise metric/measure"):
        replace(geometry, metric_volume_ratio=wrong)


@pytest.mark.parametrize("dimension", [1, 2, 3])
def test_a01_conformal_determinant_and_normalization(dimension):
    shape = (4,) * dimension
    factor = 0.8 + 0.1 * np.indices(shape)[0]
    geometry = conformal_regional_geometry(
        region_id="target", conformal_factor=factor, dimension=dimension,
        curvature_class="EXTERNAL_VALIDATION_METRIC", pullback_provenance="A01",
        normalization=metric_normalization(normalization_id="A01", reference_comoving_volume=float(np.mean(factor**dimension))),
        metadata={},
    )
    # Independently invert the supplied tensor and take its determinant.
    expected = np.sqrt(np.linalg.det(np.linalg.inv(geometry.metric_inverse)))
    np.testing.assert_allclose(geometry.metric_volume_ratio, expected, rtol=2e-14, atol=0.0)
    with pytest.raises(ContinuumContractError, match="coordinate density"):
        replace(make_operator(shape=shape).carrier, reference_measure_weights=np.full(shape, 2.0 / np.prod(shape)))


def test_a01_preassembly_metric_measure_tampering_rejected():
    original = make_operator(shape=(4, 4, 4)).void_geometry
    changed = replace(original)
    wrong = 1.0 + 0.2 * np.sin(2*np.pi*np.indices((4, 4, 4))[1]/4)
    object.__setattr__(changed, "metric_volume_ratio", wrong)
    with pytest.raises(ContinuumContractError, match="pointwise metric/measure"):
        make_operator(shape=(4, 4, 4), void_geometry=changed)


def test_a02_nontrivial_metric_coordinate_derivative_and_frame():
    scenario, _ = make_case(scale_factor_value=2.0)
    pullback = scenario.spatial_pullback
    # Passive coordinate change x_new=3*x_old: gamma_new=I/9.
    # d/dx_new=(1/3)d/dx_old; gamma^-1 cancels this in the Laplacian.
    changed = replace(pullback,
        wall_reference_gradient_operators=pullback.wall_reference_gradient_operators / 3.0,
        wall_reference_metric_inverse=np.broadcast_to(9.0 * np.eye(3), (pullback.wall_size, 3, 3)),
    )
    result = derive_clock_anchored_wall_kinematic_geometry(scenario=replace(scenario, spatial_pullback=changed), numerics=numerics())
    values = scenario.lapse_closure.perturbative_wall_lapse.reshape((-1, *pullback.wall_grid_shape))
    # Independently apply centered coordinate differences, without the supplied matrix.
    coordinate = np.stack([
        ((np.roll(values, -1, axis=axis+1) - np.roll(values, 1, axis=axis+1)) / (6.0 * step)).reshape(values.shape[0], -1)
        for axis, step in enumerate(pullback.h1_wall_domain.operator.carrier.grid_spacing)
    ], axis=-1)
    physical = 1.5 * coordinate
    raised = 2.25 * coordinate
    np.testing.assert_allclose(result.wall_acceleration_coordinate_covector, coordinate, rtol=0.0, atol=2e-18)
    np.testing.assert_allclose(result.wall_acceleration_orthonormal, physical, rtol=0.0, atol=2e-18)
    np.testing.assert_allclose(result.wall_acceleration_coordinate_contravariant, raised, rtol=0.0, atol=2e-18)
    assert np.max(np.abs(physical - coordinate)) > 1e-4
    assert result.acceleration_component_representations["wall_acceleration_orthonormal"] is ComponentRepresentation.PHYSICAL_ORTHONORMAL
    assert scenario.boost_result.velocity_component_kind is ComponentRepresentation.PHYSICAL_ORTHONORMAL
    assert result.acceleration_classification == "DERIVED_FROM_GENERIC_GR"
    assert result.acceleration_component_realization_classification == "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
    with pytest.raises(Phase1FCSpatialClosureError, match="COORDINATE_COVECTOR"):
        replace(pullback, wall_gradient_component_representation=ComponentRepresentation.COORDINATE_CONTRAVARIANT)
    with pytest.raises(Phase1FCSpatialClosureError, match="SPD"):
        replace(pullback, wall_reference_metric_inverse=-pullback.wall_reference_metric_inverse)


def test_a02_nondiagonal_frame_and_metric_contraction():
    # Explicit positive-diagonal triangular frame, not obtained from the implementation.
    frame = np.array([[2.0, 0.0, 0.0], [0.5, 1.0, 0.0], [-0.25, 0.3, 1.5]])
    inverse = (frame @ frame.T)[None, :, :]
    coordinate = np.array([[0.002, -0.003, 0.001]])
    expected = (coordinate @ frame) / 2.5
    actual = orthonormal_components(coordinate, inverse, 2.5)
    np.testing.assert_allclose(actual, expected, rtol=2e-15, atol=0.0)
    np.testing.assert_allclose(np.sum(actual**2), (coordinate @ inverse[0] @ coordinate.T)[0, 0] / 2.5**2, rtol=2e-15, atol=0.0)


def initial_data(geometry, limit=0.05, values=None):
    return ScalarMetricTraceInitialData(
        initial_metric_trace=np.zeros(geometry.scenario.spatial_pullback.wall_size) if values is None else values,
        linear_regime_limit=limit, initial_time=float(geometry.time_grid[0]),
        background_split_policy=MetricTraceBackgroundSplit.EXPLICIT_WEIGHTED_MEAN_ZERO_PERTURBATION,
        spatial_measure_id=geometry.scenario.spatial_pullback.wall_measure_id,
        frame_id=geometry.scenario.wall_congruence_id,
        provenance="A03_SYNTHETIC_VALIDITY_TEST", scientific_classification=EXTERNAL_CLOSURE_INPUT,
    )


def test_a03_alternating_unit_and_positivity_boundary_rejected():
    _, geometry = make_case()
    size = geometry.scenario.spatial_pullback.wall_size
    for amplitude in (1.0, 0.5):
        with pytest.raises(Phase1FCMetricReconstructionError, match="positive metric"):
            initial_data(geometry, limit=0.9, values=np.resize([amplitude, -amplitude], size))
    with pytest.raises(Phase1FCMetricReconstructionError, match="linear-regime"):
        initial_data(geometry, values=np.resize([0.1, -0.1], size))
    for limit in (0.0, 1.0, float("nan"), float("inf")):
        with pytest.raises(Phase1FCMetricReconstructionError, match="limit"):
            initial_data(geometry, limit=limit)


def test_a03_long_time_accumulation_rejected_driver_unchanged():
    _, geometry = make_case(time_values=(0.0, 10.0, 20.0), lapse_amplitude_values=(0.0, 0.0, 0.0))
    geometry.validate_integrity()  # Driver-only geometry remains admissible.
    with pytest.raises(Phase1FCMetricReconstructionError, match="linear-regime"):
        reconstruct_optional_scalar_metric_trace(geometry=geometry, initial_data=initial_data(geometry), numerics=numerics())


def test_a03_small_trace_independent_time_integral_converges():
    # psi=p0+b*t-c*t^2/2, nu=-b+c*t, H=0, alpha=a=1.
    # The known discrete spatial eigenvalue is -32 on the four-cell directions.
    # Integrate C_dot=(0.01+32*psi)*phi/3 analytically, not by trapezoidal recurrence.
    errors = []
    for count in (9, 17, 33):
        time = np.linspace(0.0, 1.0, count)
        _, geometry = make_case(time_values=tuple(time))
        output = reconstruct_optional_scalar_metric_trace(geometry=geometry, initial_data=initial_data(geometry), numerics=numerics())
        shape = geometry.scenario.spatial_pullback.wall_grid_shape
        coordinates = np.indices(shape)
        phi = (np.sin(2*np.pi*coordinates[2]/4) + 0.25*np.cos(2*np.pi*coordinates[1]/4)).reshape(-1)
        exact = ((0.01*time + 32*(0.002*time + 0.001*time**2/2 - 0.0004*time**3/6))/3)[:, None]*phi
        error = float(np.max(np.abs(output.metric_trace_perturbation - exact)))
        # Trapezoidal error for a quadratic driver is exactly O(dt^2).
        expected_error = 32*0.0004/36/(count-1)**2 * np.max(np.abs(phi))
        np.testing.assert_allclose(error, expected_error, rtol=2e-8, atol=2e-16)
        assert output.diagnostics.minimum_metric_factor > 0.0
        assert output.diagnostics.metric_trace_max_abs < 0.05
        errors.append(error)
    np.testing.assert_allclose(np.array(errors[:-1])/errors[1:], 4.0, rtol=2e-8, atol=0.0)


@pytest.mark.parametrize("omega_m", [0.1, 0.315, 0.9])
@pytest.mark.parametrize("a", [0.001, 0.01, 1/21, 0.25, 0.5, 1.0])
def test_a05_qplus_independent_reduction_of_order(omega_m, a):
    recipe = replace(PLANCK_2018_QPLUS_RECIPE, omega_m=omega_m, omega_lambda=1-omega_m)
    ratio = recipe.omega_lambda/recipe.omega_m
    # Substitute x=a*u into (5/2) Om E(a) integral dx/(x^3 E(x)^3).
    # This dimensionless form avoids an absolute quadrature floor at early a.
    integral, estimate = quad(lambda u: u**1.5/(1+ratio*a**3*u**3)**1.5, 0.0, 1.0, epsabs=2e-14, epsrel=2e-13, limit=200)
    reference = 2.5*a*np.sqrt(1+ratio*a**3)*integral
    assert estimate < 2e-13
    np.testing.assert_allclose(qplus(1/a-1, recipe), reference, rtol=3e-12, atol=0.0)


def test_a05_early_normalization_and_dust_limit():
    recipe = PLANCK_2018_QPLUS_RECIPE
    a = 1e-5
    np.testing.assert_allclose(qplus(1/a-1, recipe)/a, 1.0, rtol=3e-14, atol=0.0)
    dust = replace(recipe, omega_m=1-1e-8, omega_lambda=1e-8)
    np.testing.assert_allclose(qplus(0.0, dust), 1.0, rtol=3e-9, atol=0.0)


def test_a04_citation_regression_and_a07_live_classification():
    for folder in ("phase1f_b", "phase1f_c"):
        for path in (Path("src/timescape_fsigma8")/folder).glob("*.py"):
            source = path.read_text(encoding="utf-8")
            assert "BDE Eqs. (14)--(16)" not in source
    required = {
        "REGIONAL_DUST_FLRW_EQUATIONS": "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION",
        "REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING": "NOT_DERIVED",
        "NAIVE_W09_WALL_CLOCK_AS_REGIONAL_PROPER_DUST_FLRW_CLOCK": "REJECTED_UNSUPPORTED",
        "ZEROTH_ORDER_DUST_WALL_BACKGROUND_COINCIDENCE": "REQUIRED_FOR_FIRST_ORDER_BOOST",
        "ZEROTH_ORDER_DUST_WALL_BACKGROUND_COINCIDENCE_STATUS": "NOT_DERIVED",
        "ALL_TIME_TRANSFER_CONSTITUTIVE_COMPATIBILITY": "NOT_DERIVED",
        "MANUFACTURED_H1_TRAJECTORIES": "ALGEBRAIC_VALIDATION_ONLY",
        "PHYSICAL_TIMESCAPE_TRAJECTORY_EXISTENCE": "NOT_DERIVED",
        "D3_VERDICT": "RESOLVED_DERIVED_4_10",
    }
    for key, value in required.items():
        assert CURRENT_SCIENTIFIC_STATUS[key] == value
    for key in ("UNIQUE_TIMESCAPE_PREDICTION", "OBSERVATIONAL_AUTHORIZATION", "RSD_AUTHORIZATION", "SIGMA8_AUTHORIZATION", "FSIGMA8_AUTHORIZATION"):
        assert CURRENT_SCIENTIFIC_STATUS[key] == "NOT_GRANTED"


def test_a06_no_implicit_scientific_test_comparison_tolerances():
    sys.path.insert(0, str(Path("scripts").resolve()))
    try:
        from audit_numerical_tolerances import audit
        assert not [record for record in audit(Path("tests")) if record["missing"]]
    finally:
        sys.path.pop(0)


@pytest.mark.parametrize(
    ("path", "test_name", "predicate_index", "near_actual", "near_expected"),
    [
        (
            "tests/test_phase1e_g_continuum_h1.py",
            "test_v7_ordinary_generalized_and_continuum_coercivity_are_distinct",
            0, 0.10000005, 0.1,
        ),
        (
            "tests/test_phase1e_g_continuum_h1.py",
            "test_v7_ordinary_generalized_and_continuum_coercivity_are_distinct",
            1, 0.1000001, 0.10000005,
        ),
        (
            "tests/test_phase1e_g_continuum_h1.py",
            "test_n11_morphology_difference_uses_target_metric_weighted_l2",
            0, 0.10000005, 0.1,
        ),
        (
            "tests/test_phase1f_a_density.py",
            "test_t5_unequal_backgrounds_preserve_regional_offset_term",
            0, 0.10000005, 0.1,
        ),
    ],
)
def test_a06_v2_negative_separation_budgets_restore_parent_semantics(
    path, test_name, predicate_index, near_actual, near_expected
):
    """Negative approximate predicates retain the parent's separation window."""
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    function = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == test_name
    )
    predicates = sorted(
        (
            node.comparators[0]
            for node in ast.walk(function)
            if isinstance(node, ast.Compare)
            and len(node.ops) == 1
            and isinstance(node.ops[0], ast.NotEq)
            and len(node.comparators) == 1
            and isinstance(node.comparators[0], ast.Call)
            and ast.unparse(node.comparators[0].func) == "pytest.approx"
        ),
        key=lambda node: node.lineno,
    )
    predicate = predicates[predicate_index]
    tolerances = {
        keyword.arg: ast.literal_eval(keyword.value)
        for keyword in predicate.keywords
    }
    assert tolerances == {"rel": 1e-6, "abs": 1e-12}

    # The flawed v1 equality window lets this near-equality adversary escape,
    # whereas the restored parent-effective window rejects it as separation.
    assert near_actual != pytest.approx(near_expected, rel=2e-12, abs=1e-14)
    corrected_accepts_separation = near_actual != pytest.approx(
        near_expected, rel=1e-6, abs=1e-12
    )
    assert not corrected_accepts_separation
    separation = max(1e-12, 1e-6 * abs(near_expected))
    genuinely_distinct = near_expected + 2.0 * separation
    assert genuinely_distinct != pytest.approx(
        near_expected, rel=1e-6, abs=1e-12
    )
