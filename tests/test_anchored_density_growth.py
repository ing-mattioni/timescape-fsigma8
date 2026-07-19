"""Phase 1D-D Candidate A: construction, identities, purity, provenance."""

from __future__ import annotations

import ast
import dataclasses
import inspect
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

import timescape_fsigma8.growth as growth_pkg
from timescape_fsigma8.growth import (
    AnchorProvenanceKind,
    AnchoredDensityGrowthDiagnosticResult,
    AnchoredDiagnosticAssumptions,
    AnchoredDiagnosticClassification,
    AnchoredGrowthModelRole,
    DensityContrastMapping,
    ExternalDensityAmplitudeAnchor,
    GrowthCoordinate,
    GrowthD3Branch,
    GrowthProvenance,
    GrowthSystem,
    anchored_density_growth_diagnostic,
)
from growth_test_utils import barotropic_scenario, clean_scenario, run_cached


FROZEN_PROVENANCE = GrowthProvenance(
    repository_commit="f960a9054ae9db3a7c378557ac3a2938c5ff7ef0",
    upstream_commit="590c6fd5332acb15f5683ebf392a0d7ce54983c5",
    upstream_notebook_sha256=(
        "86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a"
    ),
)


def explicit_assumptions() -> AnchoredDiagnosticAssumptions:
    return AnchoredDiagnosticAssumptions(
        a1_linear_evolution_acknowledged=True,
        a2_scale_independent_growth_acknowledged=True,
        a3_fixed_reference_spectrum_shape_acknowledged=True,
        a4_fixed_smoothing_convention_acknowledged=True,
        a5_positive_differentiable_growth_acknowledged=True,
        a6_anchor_at_resolved_reference_acknowledged=True,
    )


def with_provenance(result):
    return replace(
        result,
        history=replace(result.history, provenance=FROZEN_PROVENANCE),
    )


def explicit_anchor(result, value: float = 0.8):
    return ExternalDensityAmplitudeAnchor(
        sigma8_anchor_at_reference=value,
        provenance_label="synthetic Phase 1D-D validation amplitude",
        provenance_kind=AnchorProvenanceKind.SYNTHETIC_VALIDATION_ONLY,
        resolved_reference=result.reference,
        smoothing_radius_definition="synthetic fixed radius label only",
        h_convention="synthetic fixed h-convention label",
        spatial_frame="synthetic matched spatial-frame label",
        reciprocal_units_statement=(
            "synthetic k and radius labels use reciprocal units in one frame"
        ),
    )


def diagnose(result, value: float = 0.8):
    result = with_provenance(result)
    return anchored_density_growth_diagnostic(
        growth_result=result,
        anchor=explicit_anchor(result, value),
        assumptions=explicit_assumptions(),
    )


@pytest.fixture(scope="module")
def comoving_pipeline():
    return with_provenance(run_cached(clean_scenario(GrowthSystem.COMOVING)))


@pytest.fixture(scope="module")
def meszaros_pipeline():
    return with_provenance(run_cached(clean_scenario(GrowthSystem.MESZAROS)))


@pytest.fixture(scope="module")
def comoving_diagnostic(comoving_pipeline):
    return anchored_density_growth_diagnostic(
        growth_result=comoving_pipeline,
        anchor=explicit_anchor(comoving_pipeline),
        assumptions=explicit_assumptions(),
    )


# ------------------------------------------------ construction and validation
def test_new_dataclasses_are_frozen_and_have_no_field_defaults(
    comoving_diagnostic,
):
    classes = (
        AnchoredDiagnosticAssumptions,
        ExternalDensityAmplitudeAnchor,
        AnchoredDensityGrowthDiagnosticResult,
    )
    for cls in classes:
        assert cls.__dataclass_params__.frozen
        for field in dataclasses.fields(cls):
            assert field.default is dataclasses.MISSING, (cls, field.name)
            assert field.default_factory is dataclasses.MISSING, (cls, field.name)
    with pytest.raises(dataclasses.FrozenInstanceError):
        comoving_diagnostic.model_caveat = "changed"


def test_all_result_arrays_are_float64_finite_immutable(comoving_diagnostic):
    for field in dataclasses.fields(comoving_diagnostic):
        value = getattr(comoving_diagnostic, field.name)
        if isinstance(value, np.ndarray):
            assert value.dtype == np.float64
            assert np.all(np.isfinite(value))
            assert not value.flags.writeable
            with pytest.raises((ValueError, RuntimeError)):
                value[0] = 0.0


@pytest.mark.parametrize("bad", [0.0, -0.1, np.nan, np.inf, -np.inf])
def test_anchor_requires_positive_finite_value(comoving_pipeline, bad):
    with pytest.raises(ValueError, match="finite and positive"):
        explicit_anchor(comoving_pipeline, bad)


@pytest.mark.parametrize(
    "field",
    [
        "provenance_label",
        "smoothing_radius_definition",
        "h_convention",
        "spatial_frame",
        "reciprocal_units_statement",
    ],
)
def test_anchor_requires_all_provenance_and_convention_labels(
    comoving_pipeline, field
):
    anchor = explicit_anchor(comoving_pipeline)
    with pytest.raises(ValueError, match=field):
        replace(anchor, **{field: ""})


def test_all_a1_a6_fields_are_recorded_and_false_or_incomplete_is_rejected():
    assumptions = explicit_assumptions()
    metadata = assumptions.to_metadata()
    assert tuple(metadata) == ("A1", "A2", "A3", "A4", "A5", "A6")
    assert all(item["acknowledged"] is True for item in metadata.values())
    with pytest.raises(ValueError, match="explicitly acknowledged"):
        replace(assumptions, a3_fixed_reference_spectrum_shape_acknowledged=False)
    with pytest.raises(TypeError):
        AnchoredDiagnosticAssumptions(  # missing A6 is never inferred
            a1_linear_evolution_acknowledged=True,
            a2_scale_independent_growth_acknowledged=True,
            a3_fixed_reference_spectrum_shape_acknowledged=True,
            a4_fixed_smoothing_convention_acknowledged=True,
            a5_positive_differentiable_growth_acknowledged=True,
        )


def test_anchor_reference_mismatch_is_rejected(comoving_pipeline):
    wrong_reference = replace(
        comoving_pipeline.reference,
        t_solver_units=comoving_pipeline.reference.t_solver_units + 1e-5,
    )
    anchor = replace(
        explicit_anchor(comoving_pipeline), resolved_reference=wrong_reference
    )
    with pytest.raises(ValueError, match="does not match"):
        anchored_density_growth_diagnostic(
            growth_result=comoving_pipeline,
            anchor=anchor,
            assumptions=explicit_assumptions(),
        )


def test_raw_string_provenance_lookalike_is_rejected(comoving_pipeline):
    with pytest.raises(ValueError, match="explicit AnchorProvenanceKind"):
        replace(
            explicit_anchor(comoving_pipeline),
            provenance_kind="synthetic_validation_only",
        )


# --------------------------------------------------------- system eligibility
def test_comoving_is_primary_and_meszaros_is_comparison_only(
    comoving_diagnostic, meszaros_pipeline
):
    meszaros = anchored_density_growth_diagnostic(
        growth_result=meszaros_pipeline,
        anchor=explicit_anchor(meszaros_pipeline),
        assumptions=explicit_assumptions(),
    )
    assert comoving_diagnostic.model_role is AnchoredGrowthModelRole.COMOVING_PRIMARY
    assert meszaros.model_role is AnchoredGrowthModelRole.MESZAROS_COMPARISON_ONLY
    assert "comparison_baseline_only" in meszaros.model_caveat
    assert "formally inapplicable" in meszaros.model_caveat
    assert meszaros.model_caveat in meszaros.limitations


def test_barotropic_pipeline_result_is_rejected_at_api_boundary():
    result = with_provenance(
        run_cached(
            barotropic_scenario(
                GrowthD3Branch.PRINTED_4_15,
                2.0 * np.pi,
                "2pi",
            )
        )
    )
    with pytest.raises(ValueError, match="only clean comoving or Meszaros"):
        anchored_density_growth_diagnostic(
            growth_result=result,
            anchor=explicit_anchor(result),
            assumptions=explicit_assumptions(),
        )


def test_public_function_has_only_three_keyword_only_mandatory_inputs():
    signature = inspect.signature(anchored_density_growth_diagnostic)
    assert tuple(signature.parameters) == ("growth_result", "anchor", "assumptions")
    for parameter in signature.parameters.values():
        assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
        assert parameter.default is inspect.Parameter.empty
    forbidden = {"d3_branch", "branch", "tilt_form", "wavenumber_convention"}
    assert forbidden.isdisjoint(signature.parameters)


def test_missing_growth_provenance_is_rejected():
    result = run_cached(clean_scenario(GrowthSystem.COMOVING))
    with pytest.raises(ValueError, match="explicit frozen-result provenance"):
        anchored_density_growth_diagnostic(
            growth_result=result,
            anchor=explicit_anchor(result),
            assumptions=explicit_assumptions(),
        )


# ---------------------------------------------------- mathematical identities
def test_anchored_amplitude_and_product_identity(comoving_diagnostic):
    d = comoving_diagnostic
    s = d.anchor.sigma8_anchor_at_reference
    np.testing.assert_array_equal(d.anchored_density_amplitude, s * d.relative_growth)
    np.testing.assert_array_equal(
        d.anchored_density_growth,
        d.selected_growth_rate * d.anchored_density_amplitude,
    )


def test_nonlogarithmic_identity_and_residual_gate(comoving_diagnostic):
    d = comoving_diagnostic
    assert d.max_identity_relative_residual <= 1e-11
    np.testing.assert_allclose(
        d.anchored_density_growth,
        d.alternative_nonlogarithmic_evaluation,
        rtol=1e-12,
        atol=1e-15,
    )


def test_continuous_reference_amplitude_equals_anchor(comoving_diagnostic):
    d = comoving_diagnostic
    assert d.continuous_reference_growth == 1.0
    assert (
        d.continuous_reference_anchored_amplitude
        == d.anchor.sigma8_anchor_at_reference
    )
    # z=10 generally lies between samples: the metadata preserve that fact.
    assert d.reference_nearest_sample_index >= 0
    assert np.isfinite(d.reference_nearest_sample_time_offset)


def test_anchor_scaling_is_exactly_linear_and_changes_no_growth_metadata(
    comoving_pipeline,
):
    d1 = anchored_density_growth_diagnostic(
        growth_result=comoving_pipeline,
        anchor=explicit_anchor(comoving_pipeline, 0.5),
        assumptions=explicit_assumptions(),
    )
    d2 = anchored_density_growth_diagnostic(
        growth_result=comoving_pipeline,
        anchor=explicit_anchor(comoving_pipeline, 1.0),
        assumptions=explicit_assumptions(),
    )
    np.testing.assert_array_equal(d2.anchored_density_amplitude, 2.0 * d1.anchored_density_amplitude)
    np.testing.assert_array_equal(d2.anchored_density_growth, 2.0 * d1.anchored_density_growth)
    np.testing.assert_array_equal(d1.relative_growth, d2.relative_growth)
    np.testing.assert_array_equal(d1.selected_growth_rate, d2.selected_growth_rate)
    assert d1.scenario_identifier == d2.scenario_identifier
    assert d1.resolved_reference == d2.resolved_reference


def test_bare_dressed_ratio_is_exact_tracker_chain_factor():
    bare_pipeline = with_provenance(
        run_cached(
            clean_scenario(
                GrowthSystem.COMOVING,
                coordinate=GrowthCoordinate.BARE_AD,
            )
        )
    )
    dressed_pipeline = with_provenance(
        run_cached(
            clean_scenario(
                GrowthSystem.COMOVING,
                coordinate=GrowthCoordinate.DRESSED_REDSHIFT,
            )
        )
    )
    bare = anchored_density_growth_diagnostic(
        growth_result=bare_pipeline,
        anchor=explicit_anchor(bare_pipeline),
        assumptions=explicit_assumptions(),
    )
    dressed = anchored_density_growth_diagnostic(
        growth_result=dressed_pipeline,
        anchor=explicit_anchor(dressed_pipeline),
        assumptions=explicit_assumptions(),
    )
    np.testing.assert_array_equal(bare.relative_growth, dressed.relative_growth)
    expected = bare_pipeline.rates.chain_factor
    nonzero = bare.anchored_density_growth != 0.0
    np.testing.assert_allclose(
        dressed.anchored_density_growth[nonzero]
        / bare.anchored_density_growth[nonzero],
        expected[nonzero],
        rtol=2e-13,
        atol=0.0,
    )


def test_delta_d_and_two_mapped_delta_m_labels_give_identical_diagnostic():
    scenarios = [clean_scenario(GrowthSystem.COMOVING)]
    scenarios.extend(
        clean_scenario(
            GrowthSystem.COMOVING,
            mapping=DensityContrastMapping.MAP_TO_DELTA_M_VIA_MINUS_K_CODE2,
            mode_k=k,
            mode_label=label,
        )
        for k, label in ((7.0, "synthetic_k7"), (13.0, "synthetic_k13"))
    )
    diagnostics = [diagnose(run_cached(scenario)) for scenario in scenarios]
    reference = diagnostics[0]
    for other in diagnostics[1:]:
        np.testing.assert_array_equal(other.relative_growth, reference.relative_growth)
        np.testing.assert_array_equal(other.selected_growth_rate, reference.selected_growth_rate)
        np.testing.assert_array_equal(
            other.anchored_density_amplitude,
            reference.anchored_density_amplitude,
        )
        np.testing.assert_array_equal(
            other.anchored_density_growth,
            reference.anchored_density_growth,
        )
        assert other.max_identity_relative_residual <= 1e-11


def test_nonpositive_duplicate_history_is_rejected(comoving_pipeline):
    bad_growth = np.array(comoving_pipeline.relative_growth_delta_d, copy=True)
    bad_growth[-1] = 0.0
    bad = replace(comoving_pipeline, relative_growth_delta_d=bad_growth)
    with pytest.raises(ValueError, match="finite and positive"):
        anchored_density_growth_diagnostic(
            growth_result=bad,
            anchor=explicit_anchor(bad),
            assumptions=explicit_assumptions(),
        )


def test_positive_relative_growth_inconsistent_with_history_is_rejected(
    comoving_pipeline,
):
    bad_growth = np.array(comoving_pipeline.relative_growth_delta_d, copy=True)
    bad_growth[10] *= 1.0 + 1.0e-8
    assert bad_growth[10] > 0.0
    bad = replace(comoving_pipeline, relative_growth_delta_d=bad_growth)
    with pytest.raises(ValueError, match="inconsistent with history.delta_d"):
        anchored_density_growth_diagnostic(
            growth_result=bad,
            anchor=explicit_anchor(bad),
            assumptions=explicit_assumptions(),
        )


def test_nonfinite_rate_or_history_is_rejected(comoving_pipeline):
    bad_rate = np.array(comoving_pipeline.rates.f_bare, copy=True)
    bad_rate[10] = np.nan
    bad = replace(
        comoving_pipeline,
        rates=replace(comoving_pipeline.rates, f_bare=bad_rate),
    )
    with pytest.raises(ValueError, match="rate is not finite"):
        anchored_density_growth_diagnostic(
            growth_result=bad,
            anchor=explicit_anchor(bad),
            assumptions=explicit_assumptions(),
        )


@pytest.mark.parametrize(
    ("updates", "message"),
    [
        (
            {"perturbation_system": GrowthSystem.MESZAROS},
            "must match scenario.perturbation_system",
        ),
        (
            {"model_role": AnchoredGrowthModelRole.MESZAROS_COMPARISON_ONLY},
            "model_role is inconsistent",
        ),
        (
            {"growth_coordinate": GrowthCoordinate.DRESSED_REDSHIFT},
            "must match scenario.growth_coordinate",
        ),
        (
            {"phase1d_d_t_checkpoint": "not-the-frozen-checkpoint"},
            "must equal the frozen checkpoint",
        ),
        (
            {"reference_nearest_sample_index": -1},
            "outside the sampling grid",
        ),
    ],
)
def test_result_metadata_invariants_reject_inconsistent_replacements(
    comoving_diagnostic,
    updates,
    message,
):
    with pytest.raises(ValueError, match=message):
        replace(comoving_diagnostic, **updates)


def test_result_reference_metadata_must_match_anchor(comoving_diagnostic):
    wrong_reference = replace(
        comoving_diagnostic.resolved_reference,
        t_solver_units=(
            comoving_diagnostic.resolved_reference.t_solver_units + 1.0e-5
        ),
    )
    with pytest.raises(ValueError, match="must equal anchor.resolved_reference"):
        replace(comoving_diagnostic, resolved_reference=wrong_reference)


def test_result_caveat_sample_flags_and_definition_source_are_validated(
    comoving_diagnostic,
):
    with pytest.raises(ValueError, match="model_caveat is inconsistent"):
        replace(comoving_diagnostic, model_caveat="wrong caveat")
    with pytest.raises(ValueError, match="must be a bool"):
        replace(comoving_diagnostic, reference_is_sampled_grid_point=1)
    with pytest.raises(ValueError, match="must be finite"):
        replace(comoving_diagnostic, reference_nearest_sample_time_offset=np.nan)
    with pytest.raises(ValueError, match="scientific_definition_source"):
        replace(comoving_diagnostic, scientific_definition_source="")


# ------------------------------------------------------ purity and exclusions
def test_diagnostic_calls_no_solver_or_pipeline(monkeypatch, comoving_pipeline):
    def forbidden(*args, **kwargs):
        raise AssertionError("diagnostic attempted to run a solver or pipeline")

    monkeypatch.setattr("scipy.integrate.solve_ivp", forbidden)
    monkeypatch.setattr(
        "timescape_fsigma8.growth.pipeline.run_growth_pipeline", forbidden
    )
    anchored_density_growth_diagnostic(
        growth_result=comoving_pipeline,
        anchor=explicit_anchor(comoving_pipeline),
        assumptions=explicit_assumptions(),
    )


def test_source_has_no_forbidden_import_or_numerical_reconstruction_call():
    path = Path(growth_pkg.__file__).resolve().parent / "anchored_diagnostic.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports = []
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.append(node.func.attr)
    for token in ("barotropic", "forensic", "scripts", "perturbations"):
        assert not any(token in name.lower() for name in imports), (token, imports)
    for forbidden_call in (
        "solve_ivp",
        "gradient",
        "diff",
        "interp",
        "polyfit",
        "convolve",
        "trapz",
        "trapezoid",
        "quad",
    ):
        assert forbidden_call not in calls


def test_public_api_has_no_prediction_or_observational_output_name():
    forbidden = {
        "fsigma8",
        "predicted_fsigma8",
        "observational_fsigma8",
        "timescape_sigma8_prediction",
        "sigma8_prediction",
    }
    assert "anchored_density_growth_diagnostic" in growth_pkg.__all__
    for name in growth_pkg.__all__:
        lowered = name.lower()
        assert all(token not in lowered for token in forbidden), name


def test_no_packaged_observational_anchor_or_silent_aggregation_api():
    module = inspect.getmodule(anchored_density_growth_diagnostic)
    for name in vars(module):
        lowered = name.lower()
        assert not any(
            survey in lowered
            for survey in (
                "planck_anchor",
                "desi_anchor",
                "boss_anchor",
                "survey_anchor",
            )
        )
    with pytest.raises(ValueError, match="one GrowthPipelineResult"):
        anchored_density_growth_diagnostic(
            growth_result=[run_cached(clean_scenario(GrowthSystem.COMOVING))],
            anchor=explicit_anchor(
                with_provenance(run_cached(clean_scenario(GrowthSystem.COMOVING)))
            ),
            assumptions=explicit_assumptions(),
        )


# ------------------------------------------------ serialization and provenance
def test_complete_result_serializes_deterministically(comoving_diagnostic):
    first = json.dumps(
        comoving_diagnostic.to_json_dict(), sort_keys=True, separators=(",", ":")
    )
    second = json.dumps(
        comoving_diagnostic.to_json_dict(), sort_keys=True, separators=(",", ":")
    )
    assert first == second
    payload = json.loads(first)
    for key in (
        "scenario_identifier",
        "scenario",
        "resolved_reference",
        "anchor",
        "assumptions",
        "provenance",
        "classification",
        "limitations",
        "continuous_reference_check",
        "sampling_grid",
        "quantities",
        "identity_residuals",
    ):
        assert key in payload


def test_provenance_classification_caveats_and_metadata_survive_serialization(
    comoving_diagnostic,
):
    payload = comoving_diagnostic.to_json_dict()
    provenance = payload["provenance"]
    assert provenance["phase1d_d_t_checkpoint"] == FROZEN_PROVENANCE.repository_commit
    assert provenance["source_growth_result"] == FROZEN_PROVENANCE.to_metadata()
    assert payload["classification"] == (
        AnchoredDiagnosticClassification.
        CONDITIONAL_ANCHORED_DIAGNOSTIC_NOT_OBSERVATIONAL_PREDICTION.value
    )
    assert "not predict the supplied anchor" in " ".join(payload["limitations"])
    assert payload["scenario_identifier"] == comoving_diagnostic.scenario_identifier
    assert payload["resolved_reference"] == (
        comoving_diagnostic.resolved_reference.to_metadata()
    )


def test_generated_phase1d_d_artifact_schema_when_present():
    artifact = (
        Path(growth_pkg.__file__).resolve().parents[3]
        / "artifacts"
        / "independent"
        / "phase1d_d_anchored_density_growth_validation.json"
    )
    if not artifact.is_file():
        pytest.skip(
            "Phase 1D-D validation artifact absent; run "
            "scripts/validate_anchored_density_growth.py"
        )
    payload = json.loads(artifact.read_text(encoding="utf-8"))
    required = {
        "phase_identifier",
        "repository_and_frozen_checkpoint_provenance",
        "exact_diagnostic_equations",
        "a1_a6_definitions",
        "api_inventory",
        "explicit_exclusions",
        "validation_only_baseline",
        "per_system_model_role",
        "reference_metadata",
        "algebraic_identity_metrics",
        "anchor_scaling_study",
        "bare_dressed_study",
        "density_basis_invariance_study",
        "reference_coordinate_equivalence",
        "meszaros_comparison_caveat",
        "one_factor_scenario_studies",
        "solver_convergence_metrics",
        "declared_gates",
        "gate_results",
        "complete_test_environments",
        "exact_file_inventory",
        "repository_preservation_statement",
    }
    assert required <= payload.keys()
    assert len(payload) == 25
    assert payload["gate_results"]["all_passed"] is True
    assert payload["validation_only_baseline"]["anchor_status"].startswith(
        "synthetic_validation_only"
    )
    assert payload["per_system_model_role"]["comoving"]["model_role"] == (
        "comoving_primary"
    )
    assert payload["per_system_model_role"]["meszaros"]["model_role"] == (
        "meszaros_comparison_only"
    )
    environments = payload["complete_test_environments"]
    if isinstance(environments, dict):
        assert {"python_3_14", "python_3_11"} <= environments.keys()
    provenance = payload["repository_and_frozen_checkpoint_provenance"]
    assert provenance["base_phase1d_d_t_checkpoint"] == (
        FROZEN_PROVENANCE.repository_commit
    )
    assert provenance["execution_state"] in {
        "uncommitted_permitted_working_tree",
        "clean_committed_tree",
    }
    assert isinstance(provenance["committed_paths_since_base"], list)
    assert isinstance(provenance["permitted_working_tree_paths"], list)
