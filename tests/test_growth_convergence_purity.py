"""Tilt equivalence, convergence, schema, and scope-purity tests."""

import dataclasses
import inspect
import json
import pathlib
import re

import numpy as np
import pytest

import timescape_fsigma8.growth as growth_pkg
from timescape_fsigma8.perturbations import TIGHT_RADAU, TIGHT_RK45
from timescape_fsigma8.growth import (
    GrowthD3Branch,
    GrowthNumericsConfig,
    GrowthSystem,
    GrowthTiltForm,
    run_growth_pipeline,
)
from growth_test_utils import (
    TEST_NUMERICS,
    TEST_REFERENCE_Z10,
    barotropic_scenario,
    clean_scenario,
    run_cached,
)

GROWTH_DIR = pathlib.Path(growth_pkg.__file__).resolve().parent


def _numerics(**overrides) -> GrowthNumericsConfig:
    base = dict(
        solver=TEST_NUMERICS.solver,
        n_samples=TEST_NUMERICS.n_samples,
        G=TEST_NUMERICS.G,
        dense=TEST_NUMERICS.dense,
        root=TEST_NUMERICS.root,
        near_zero_rel_floor=TEST_NUMERICS.near_zero_rel_floor,
    )
    base.update(overrides)
    return GrowthNumericsConfig(**base)


# ---------------------------------------------------------------- tilt equivalence
def test_tilt_forms_agree_for_identical_corrected_physics():
    runs = {}
    for tilt in (GrowthTiltForm.UNRESCALED_V, GrowthTiltForm.RESCALED_VTILDE):
        runs[tilt] = run_cached(
            barotropic_scenario(
                GrowthD3Branch.PRINTED_4_15, 5.0 * np.pi, "5pi", tilt=tilt
            )
        )
    a = runs[GrowthTiltForm.UNRESCALED_V]
    b = runs[GrowthTiltForm.RESCALED_VTILDE]
    scale = np.max(np.abs(a.history.delta_d))
    assert np.max(np.abs(a.history.delta_d - b.history.delta_d)) / scale < 1e-8
    # same roots to documented tolerance
    for ra, rb in zip(
        a.crossings.delta_d_roots + a.crossings.z_roots,
        b.crossings.delta_d_roots + b.crossings.z_roots,
    ):
        assert ra.t_root == pytest.approx(rb.t_root, abs=1e-8)
    # same rates and non-logarithmic derivatives away from roots
    ok = ~(a.rates.near_zero_mask | b.rates.near_zero_mask)
    np.testing.assert_allclose(
        a.rates.f_bare[ok], b.rates.f_bare[ok], rtol=1e-6
    )
    np.testing.assert_allclose(
        a.rates.dDelta_d_dln_aD, b.rates.dDelta_d_dln_aD, rtol=0, atol=1e-8 * scale
    )
    # both labels remain visible in metadata
    assert a.history.to_metadata()["scenario"]["tilt_form"] == "unrescaled_V"
    assert b.history.to_metadata()["scenario"]["tilt_form"] == "rescaled_Vtilde"


# ---------------------------------------------------------------- solver convergence
def test_solver_convergence_of_growth_quantities():
    scenario = clean_scenario(GrowthSystem.COMOVING)
    results = {}
    for name, solver in (
        ("tight_dop853", TEST_NUMERICS.solver),
        ("tight_rk45", TIGHT_RK45),
        ("tight_radau", TIGHT_RADAU),
    ):
        results[name] = run_growth_pipeline(
            scenario=scenario,
            reference=TEST_REFERENCE_Z10,
            numerics=_numerics(solver=solver),
            provenance=None,
        )
    ref = results["tight_dop853"]
    for name in ("tight_rk45", "tight_radau"):
        other = results[name]
        for attr in ("relative_growth_delta_d",):
            scale = np.max(np.abs(getattr(ref, attr)))
            err = np.max(np.abs(getattr(ref, attr) - getattr(other, attr)))
            assert err / scale < 1e-7, (name, attr, err / scale)
        f_err = np.nanmax(np.abs(ref.rates.f_bare - other.rates.f_bare))
        assert f_err < 1e-7, (name, f_err)


# ---------------------------------------------------------------- root convergence
def test_root_convergence_across_methods_and_grids():
    scenario = barotropic_scenario(
        GrowthD3Branch.DERIVED_4_10, 2.0 * np.pi, "2pi"
    )
    roots = {}
    for label, numerics in (
        ("dop853_n600", _numerics()),
        ("dop853_n1000", _numerics(n_samples=1000)),
        ("radau_n600", _numerics(solver=TIGHT_RADAU)),
    ):
        run = run_growth_pipeline(
            scenario=scenario,
            reference=TEST_REFERENCE_Z10,
            numerics=numerics,
            provenance=None,
        )
        roots[label] = run.crossings.delta_d_roots[0]
    times = [r.t_root for r in roots.values()]
    assert max(times) - min(times) < 5e-9
    # the refined root is not merely the left sample of its bracket
    for r in roots.values():
        assert abs(r.t_root - r.bracket_left) > 10.0 * r.root_uncertainty


# ---------------------------------------------------------------- schema
def test_pipeline_json_payload_schema_and_serializability():
    run = run_cached(
        barotropic_scenario(GrowthD3Branch.PRINTED_4_15, 10.0 * np.pi, "10pi")
    )
    payload = run.to_json_dict()
    json.dumps(payload)  # fully serializable
    for key in (
        "history",
        "dense_nfev",
        "reference",
        "delta_d_roots",
        "z_roots",
        "endpoint_roots",
        "validity_intervals",
        "endpoint_summary",
        "rate_segments",
        "non_logarithmic_derivatives",
        "mapped_delta_m",
    ):
        assert key in payload, key
    hist = payload["history"]
    for key in (
        "scenario",
        "scenario_identifier",
        "timescape_h",
        "lcdm_h",
        "time_unit",
        "numerics",
        "epoch",
        "initial_conditions",
        "integration_interval_solver_units",
        "resolved_k_code",
        "provenance",
    ):
        assert key in hist, key
    assert hist["scenario"]["d3_branch"] == "printed_4_15"


# ---------------------------------------------------------------- purity
FORBIDDEN_D2_TOKENS = (
    "_upstream_d2_corrupted_cs2",
    "_ForensicSoundSpeed",
    "_phase1c_b2_forensic",
    "54.0 * f**5",
)
# Forbidden as API surface (spectra / sigma / fsigma8 / RSD / inference).
FORBIDDEN_API_PATTERNS = (
    "sigma_8",
    "sigma8",
    "sigma_r",
    "fsigma",
    "f_sigma",
    "power_spectrum",
    "transfer_function",
    "primordial",
    "kaiser",
    "rsd",
    "galaxy_bias",
    "peculiar_velocity",
    "alcock",
    "likelihood",
    "covariance",
    "fit_",
)


def _growth_sources() -> dict[str, str]:
    return {
        p.name: p.read_text(encoding="utf-8")
        for p in sorted(GROWTH_DIR.glob("*.py"))
    }


def test_growth_package_contains_no_d2_or_forensic_path():
    for name, source in _growth_sources().items():
        for token in FORBIDDEN_D2_TOKENS:
            assert token not in source, (name, token)


def test_growth_package_exposes_no_forbidden_observable_api():
    # public names must not include any spectrum/sigma/RSD/likelihood API
    for name in growth_pkg.__all__:
        lowered = name.lower()
        for pattern in FORBIDDEN_API_PATTERNS:
            assert pattern not in lowered, (name, pattern)
    # no function/class defined in the package matches either
    for module_name, source in _growth_sources().items():
        for match in re.finditer(r"^(?:def|class)\s+(\w+)", source, re.M):
            lowered = match.group(1).lower()
            for pattern in FORBIDDEN_API_PATTERNS:
                assert pattern not in lowered, (module_name, match.group(1))


def test_growth_configs_have_no_field_defaults():
    from timescape_fsigma8.growth import (
        DenseSolveConfig,
        RootRefineConfig,
    )

    for cls in (GrowthNumericsConfig, DenseSolveConfig, RootRefineConfig):
        for field in dataclasses.fields(cls):
            assert field.default is dataclasses.MISSING, (cls, field.name)


def test_validation_artifact_schema_when_present():
    """Schema of the generated validation artifact (auto-skips if absent)."""
    artifact = (
        GROWTH_DIR.parent.parent.parent
        / "artifacts"
        / "independent"
        / "phase1d_b_growth_validation.json"
    )
    if not artifact.is_file():
        pytest.skip(
            "growth validation artifact absent; run "
            "scripts/validate_growth_pipeline.py"
        )
    data = json.loads(artifact.read_text(encoding="utf-8"))
    for key in (
        "schema_note",
        "provenance",
        "environment",
        "numerical_configuration",
        "gates_declared_before_study",
        "v1_baseline_crossings",
        "v2_analytic_identities",
        "v3_solver_convergence",
        "v4_root_convergence",
        "v5_tilt_equivalence",
        "v6_scale_dependence",
        "v7_one_factor_studies",
        "uncertainty_taxonomy",
        "gate_failures",
        "all_gates_passed",
    ):
        assert key in data, key
    assert data["provenance"]["upstream_commit"].startswith("590c6fd")
    taxonomy = data["uncertainty_taxonomy"]
    assert "confidence interval" in taxonomy["unresolved_convention_spread"]
    assert "intentionally absent" in taxonomy[
        "spectrum_normalization_uncertainty"
    ]
    baseline = data["v7_one_factor_studies"]["validation_baseline"]
    assert baseline["label"] == "validation_baseline"
    assert "not a public API default" in baseline["note"]


def test_growth_package_does_not_import_forensic_or_scripts():
    # Only import statements are scanned: the package documentation is
    # required to STATE that D2 stays forensic-only, so the word itself is
    # legitimate in docstrings.
    import_pattern = re.compile(r"^\s*(?:from|import)\s+(\S+)", re.M)
    for name, source in _growth_sources().items():
        for match in import_pattern.finditer(source):
            module = match.group(1).lower()
            assert "forensic" not in module, (name, module)
            assert not module.startswith("scripts"), (name, module)
