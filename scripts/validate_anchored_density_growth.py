"""Validate the Phase 1D-D externally anchored conditional diagnostic.

The named builders in this script are validation-only configurations, not
package defaults or scientific preferences.  Every run delegates evolution,
reference resolution, rates, crossings, and density mapping to the frozen
Phase 1D-B pipeline, then applies ``anchored_density_growth_diagnostic``.

No observational data or anchor is bundled.  Every anchor used here is
synthetic, has no observational interpretation, and exists solely to verify
the conditional algebra in Phase 1D-A equations (D6a)--(D6b).
"""

from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
import sys
import sysconfig
import tempfile
from dataclasses import replace
from importlib.metadata import version
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from timescape_fsigma8.perturbations import (  # noqa: E402
    TIGHT_DOP853,
    TIGHT_RADAU,
    TIGHT_RK45,
    EpochChoice,
    RateUnitConvention,
)
from timescape_fsigma8.perturbations.scenarios import (  # noqa: E402
    PHASE1C_EPOCH_ROOT,
)
from timescape_fsigma8.perturbations.solver import SolverConfig  # noqa: E402
from timescape_fsigma8.growth import (  # noqa: E402
    AnchorProvenanceKind,
    AnchoredDiagnosticAssumptions,
    DenseSolveConfig,
    DensityContrastMapping,
    ExternalDensityAmplitudeAnchor,
    GrowthBackgroundPreset,
    GrowthCoordinate,
    GrowthD3Branch,
    GrowthNumericsConfig,
    GrowthProvenance,
    GrowthReference,
    GrowthReferenceCoordinate,
    GrowthScenario,
    GrowthSystem,
    GrowthTiltForm,
    GrowthWavenumberConvention,
    RootRefineConfig,
    anchored_density_growth_diagnostic,
    run_growth_pipeline,
)


OUTPUT = (
    PROJECT_ROOT
    / "artifacts"
    / "independent"
    / "phase1d_d_anchored_density_growth_validation.json"
)
UPSTREAM_ROOT = (
    PROJECT_ROOT
    / ".reference"
    / "Linear-Perturbations-in-averaged-cosmological-models"
)
UPSTREAM_NOTEBOOK = UPSTREAM_ROOT / "ACPT_Timescape.ipynb"
BASE_PHASE1D_D_T_CHECKPOINT = "f960a9054ae9db3a7c378557ac3a2938c5ff7ef0"
UPSTREAM_COMMIT = "590c6fd5332acb15f5683ebf392a0d7ce54983c5"
NOTEBOOK_SHA256 = (
    "86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a"
)
# Review finding F6: NOTEBOOK_SHA256 is the raw hash of a Windows
# core.autocrlf working tree and stays the frozen provenance label of the
# growth results.  Verification uses the line-ending-independent identity
# (UPSTREAM.lock notebook_sha256_lf).
NOTEBOOK_SHA256_LF = (
    "628c441288d67854e0380518841dede3680bddab610e9ef5cea04937455cea2a"
)
PHASE1D_D_WORK_BRANCH = "phase-1d-d-anchored-density-growth"
# Peeled commit of tag phase-1d-d-anchored-density-growth-v1.
PHASE1D_D_COMMIT = "7ea266c2cb00aac8afdef71e51a18aea5fb7d39c"
POST_PHASE_DRIFT_PREFIXES = (
    "src/timescape_fsigma8/background/",
    "src/timescape_fsigma8/perturbations/",
    "src/timescape_fsigma8/growth/",
)
PERMITTED_PHASE1D_D_TRACKED_PATHS = frozenset(
    {
        "src/timescape_fsigma8/growth/anchored_diagnostic.py",
        "src/timescape_fsigma8/growth/__init__.py",
        "tests/test_anchored_density_growth.py",
        "scripts/validate_anchored_density_growth.py",
        "reports/phase1d_d_anchored_density_growth_validation.md",
    }
)
REQUIRED_ARTIFACT_TOP_LEVEL_SECTIONS = frozenset(
    {
        "a1_a6_definitions",
        "algebraic_identity_metrics",
        "anchor_scaling_study",
        "api_inventory",
        "bare_dressed_study",
        "complete_test_environments",
        "declared_gates",
        "density_basis_invariance_study",
        "exact_diagnostic_equations",
        "exact_file_inventory",
        "explicit_exclusions",
        "gate_justification",
        "gate_results",
        "meszaros_comparison_caveat",
        "one_factor_scenario_studies",
        "per_system_model_role",
        "phase_identifier",
        "reference_coordinate_equivalence",
        "reference_metadata",
        "repository_and_frozen_checkpoint_provenance",
        "repository_preservation_statement",
        "schema_note",
        "solver_convergence_metrics",
        "uncertainty_taxonomy",
        "validation_only_baseline",
    }
)


REFERENCE_SOLVER = SolverConfig(
    method="DOP853",
    rtol=2e-13,
    atol=2e-15,
    max_step=np.inf,
    first_step=None,
)
REFERENCE_DENSE = DenseSolveConfig(
    method="DOP853",
    rtol=2e-13,
    atol=2e-15,
    max_step=np.inf,
    first_step=None,
)
DENSE = DenseSolveConfig(
    method="DOP853",
    rtol=1e-11,
    atol=1e-13,
    max_step=np.inf,
    first_step=None,
)
ROOT = RootRefineConfig(
    xtol=1e-13,
    rtol=8.9e-16,
    maxiter=100,
    residual_scale_gate=1e-6,
)
N_SAMPLES = 1000
NEAR_ZERO_REL_FLOOR = 1e-9

REFERENCE_Z10 = GrowthReference(
    coordinate=GrowthReferenceCoordinate.DRESSED_REDSHIFT,
    value=10.0,
    root=PHASE1C_EPOCH_ROOT,
    amplitude_floor_rel=1e-10,
)

PROVENANCE = GrowthProvenance(
    repository_commit=BASE_PHASE1D_D_T_CHECKPOINT,
    upstream_commit=UPSTREAM_COMMIT,
    upstream_notebook_sha256=NOTEBOOK_SHA256,
)

ASSUMPTIONS = AnchoredDiagnosticAssumptions(
    a1_linear_evolution_acknowledged=True,
    a2_scale_independent_growth_acknowledged=True,
    a3_fixed_reference_spectrum_shape_acknowledged=True,
    a4_fixed_smoothing_convention_acknowledged=True,
    a5_positive_differentiable_growth_acknowledged=True,
    a6_anchor_at_resolved_reference_acknowledged=True,
)

GATES = {
    "sampled_growth_consistency_normalized_max": 1e-14,
    "solver_convergence_normalized_linf_max": 2e-8,
    "q_equals_f_times_a_normalized_max": 1e-12,
    "q_equals_anchor_dg_dln_a_normalized_max": 1e-11,
    "anchor_scaling_normalized_max": 1e-14,
    "bare_dressed_chain_normalized_max": 1e-12,
    "density_basis_invariance_normalized_max": 1e-14,
    "reference_coordinate_equivalence_normalized_max": 1e-12,
}

GATE_JUSTIFICATION = {
    "solver_convergence_normalized_linf_max": (
        "declared before evaluation; inherited Phase 1C-B2/1D-B tight-solver "
        "gate against an independent DOP853 rtol=2e-13, atol=2e-15 run"
    ),
    "identity_gates": (
        "algebraic identities reuse only frozen analytic rates and the frozen "
        "non-logarithmic derivative, so roundoff-scale residuals are expected; "
        "the declared gates leave several safety decades and are not relaxed"
    ),
    "normalization": (
        "all normalized errors divide by max(max(abs(reference)), float64 "
        "tiny); no pointwise division by a potentially zero reference occurs"
    ),
}


def git(*args: str, cwd: Path = PROJECT_ROOT) -> str:
    command = ["git", "-c", f"safe.directory={PROJECT_ROOT.as_posix()}"]
    if cwd.resolve() == UPSTREAM_ROOT.resolve():
        command.extend(
            [
                f"--git-dir={(UPSTREAM_ROOT / '.git').resolve()}",
                f"--work-tree={UPSTREAM_ROOT.resolve()}",
            ]
        )
    command.extend(args)
    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    # Preserve the leading index/work-tree status columns used by porcelain;
    # callers that consume scalar output do not contain leading whitespace.
    return result.stdout.rstrip()


def sha256(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_lf(path: Path) -> str:
    """SHA-256 of the bytes with CRLF normalised to LF (review finding F6)."""
    import hashlib

    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def is_ancestor(commit: str, descendant: str) -> bool:
    completed = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={PROJECT_ROOT.as_posix()}",
            "merge-base",
            "--is-ancestor",
            commit,
            descendant,
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode not in (0, 1):
        raise RuntimeError(f"git merge-base failed: {completed.stderr.strip()}")
    return completed.returncode == 0


def validate_post_phase_regeneration_state(branch: str) -> dict:
    """Ancestry-based provenance for regenerating the artifact later (F6).

    The frozen Phase 1D-D commit must be an ancestor of HEAD.  The phase's
    scope rule is checked on its immutable historical range
    ``BASE..PHASE1D_D_COMMIT``; later, separately approved changes are
    recorded as post-phase drift instead of being rejected.  The tree must be
    clean so that the regenerated artifact belongs to one commit.
    """
    execution_head = git("rev-parse", "HEAD")
    for commit in (BASE_PHASE1D_D_T_CHECKPOINT, PHASE1D_D_COMMIT):
        if not is_ancestor(commit, execution_head):
            raise RuntimeError(f"{commit} is not an ancestor of HEAD")
    committed_paths = sorted(
        path.replace("\\", "/")
        for path in git(
            "diff",
            "--name-only",
            f"{BASE_PHASE1D_D_T_CHECKPOINT}..{PHASE1D_D_COMMIT}",
        ).splitlines()
        if path
    )
    out_of_scope = sorted(set(committed_paths) - PERMITTED_PHASE1D_D_TRACKED_PATHS)
    if out_of_scope:
        raise RuntimeError(f"historical Phase 1D-D range is out of scope: {out_of_scope}")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("regeneration requires a clean index")
    working_paths = _porcelain_paths(
        git("status", "--porcelain=v1", "--untracked-files=all")
    )
    if working_paths:
        raise RuntimeError(
            f"regeneration requires a clean working tree: {working_paths}"
        )
    drift = sorted(
        path.replace("\\", "/")
        for path in git(
            "diff", "--name-only", f"{PHASE1D_D_COMMIT}..{execution_head}"
        ).splitlines()
        if path.startswith(POST_PHASE_DRIFT_PREFIXES)
    )
    return {
        "branch": branch,
        "base_phase1d_d_t_checkpoint": BASE_PHASE1D_D_T_CHECKPOINT,
        "execution_context": "post_phase_regeneration_by_ancestry",
        "phase1d_d_commit": PHASE1D_D_COMMIT,
        "execution_head": execution_head,
        "execution_state": "clean_committed_tree",
        "committed_paths_since_base": committed_paths,
        "committed_paths_scope": "historical range BASE..PHASE1D_D_COMMIT",
        "post_phase_scientific_module_changes": drift,
        "permitted_working_tree_paths": [],
        "staged_paths": [],
    }


def _porcelain_paths(status: str) -> list[str]:
    paths = []
    for line in status.splitlines():
        if len(line) < 4:
            raise RuntimeError(f"cannot parse Git status record: {line!r}")
        path = line[3:]
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[1]
        paths.append(path.replace("\\", "/"))
    return sorted(paths)


def validate_repository_execution_state() -> dict:
    """Validate pre-commit and future clean-commit execution provenance."""
    branch = git("branch", "--show-current")
    if branch != PHASE1D_D_WORK_BRANCH:
        # Review finding F6: off the historical work branch, validate by
        # ancestry against the recorded commits instead of the branch name.
        return validate_post_phase_regeneration_state(branch)
    execution_head = git("rev-parse", "HEAD")
    merge_base = git(
        "merge-base",
        BASE_PHASE1D_D_T_CHECKPOINT,
        execution_head,
    )
    if merge_base != BASE_PHASE1D_D_T_CHECKPOINT:
        raise RuntimeError(
            "the frozen Phase 1D-D-t checkpoint is not an ancestor of HEAD"
        )
    committed_paths = sorted(
        path.replace("\\", "/")
        for path in git(
            "diff",
            "--name-only",
            f"{BASE_PHASE1D_D_T_CHECKPOINT}..{execution_head}",
        ).splitlines()
        if path
    )
    committed_out_of_scope = sorted(
        set(committed_paths) - PERMITTED_PHASE1D_D_TRACKED_PATHS
    )
    if committed_out_of_scope:
        raise RuntimeError(
            "committed paths since the Phase 1D-D-t checkpoint are out of "
            f"scope: {committed_out_of_scope}"
        )
    staged_paths = sorted(
        path.replace("\\", "/")
        for path in git("diff", "--cached", "--name-only").splitlines()
        if path
    )
    if staged_paths:
        raise RuntimeError(
            "validation requires a clean index; staged paths: "
            f"{staged_paths}"
        )
    working_paths = _porcelain_paths(
        git("status", "--porcelain=v1", "--untracked-files=all")
    )
    working_out_of_scope = sorted(
        set(working_paths) - PERMITTED_PHASE1D_D_TRACKED_PATHS
    )
    if working_out_of_scope:
        raise RuntimeError(
            "working-tree paths are out of Phase 1D-D scope: "
            f"{working_out_of_scope}"
        )
    execution_state = (
        "uncommitted_permitted_working_tree"
        if working_paths
        else "clean_committed_tree"
    )
    return {
        "branch": branch,
        "base_phase1d_d_t_checkpoint": BASE_PHASE1D_D_T_CHECKPOINT,
        "execution_context": "phase_work_branch",
        "execution_head": execution_head,
        "execution_state": execution_state,
        "committed_paths_since_base": committed_paths,
        "permitted_working_tree_paths": working_paths,
        "staged_paths": staged_paths,
    }


def numerics(
    *,
    solver: SolverConfig,
    dense: DenseSolveConfig,
    n_samples: int,
) -> GrowthNumericsConfig:
    """Build one fully explicit validation numerics record (no API default)."""
    return GrowthNumericsConfig(
        solver=solver,
        n_samples=n_samples,
        G=1.0,
        dense=dense,
        root=ROOT,
        near_zero_rel_floor=NEAR_ZERO_REL_FLOOR,
    )


def clean_scenario(*, system: GrowthSystem, **overrides) -> GrowthScenario:
    """Build the named validation scenario; every scientific field visible."""
    values = dict(
        perturbation_system=system,
        background_preset=GrowthBackgroundPreset.NOTEBOOK_REFERENCE,
        d3_branch=GrowthD3Branch.NOT_APPLICABLE,
        tilt_form=GrowthTiltForm.NOT_APPLICABLE,
        rate_unit_convention=RateUnitConvention.UPSTREAM_UNCONVERTED,
        epoch_choice=EpochChoice.UPSTREAM_0P218_GYR,
        wavenumber_convention=GrowthWavenumberConvention.NOT_APPLICABLE,
        growth_coordinate=GrowthCoordinate.BARE_AD,
        density_contrast_mapping=DensityContrastMapping.KEEP_DELTA_D,
        supplied_mode_k=None,
        mode_label=None,
    )
    values.update(overrides)
    return GrowthScenario(**values)


def make_anchor(result, *, value: float) -> ExternalDensityAmplitudeAnchor:
    """Build an explicitly synthetic validation anchor, never an observation."""
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


def evaluate(
    *,
    scenario: GrowthScenario,
    reference: GrowthReference,
    solver: SolverConfig,
    dense: DenseSolveConfig,
    n_samples: int,
    anchor_value: float,
):
    pipeline = run_growth_pipeline(
        scenario=scenario,
        reference=reference,
        numerics=numerics(solver=solver, dense=dense, n_samples=n_samples),
        provenance=PROVENANCE,
    )
    diagnostic = anchored_density_growth_diagnostic(
        growth_result=pipeline,
        anchor=make_anchor(pipeline, value=anchor_value),
        assumptions=ASSUMPTIONS,
    )
    return pipeline, diagnostic


def zero_safe_metrics(reference, comparison, t, z) -> dict:
    reference = np.asarray(reference, dtype=np.float64)
    comparison = np.asarray(comparison, dtype=np.float64)
    difference = comparison - reference
    absolute = np.abs(difference)
    scale = max(float(np.max(np.abs(reference))), np.finfo(np.float64).tiny)
    worst = int(np.argmax(absolute))
    return {
        "max_absolute_error": float(np.max(absolute)),
        "normalized_linf_error": float(np.max(absolute) / scale),
        "rms_normalized_error": float(np.sqrt(np.mean(difference**2)) / scale),
        "worst_discrepancy_time_solver_units": float(t[worst]),
        "worst_discrepancy_dressed_redshift": float(z[worst]),
        "endpoint_error": float(difference[-1]),
        "reference_scale": scale,
        "denominator_definition": (
            "max(max(abs(reference array)), numpy.float64 tiny); "
            "never pointwise relative error"
        ),
    }


def normalized_identity(left, right) -> dict:
    left = np.asarray(left, dtype=np.float64)
    right = np.asarray(right, dtype=np.float64)
    residual = left - right
    scale = max(
        float(np.max(np.abs(left))),
        float(np.max(np.abs(right))),
        np.finfo(np.float64).tiny,
    )
    return {
        "max_absolute_residual": float(np.max(np.abs(residual))),
        "normalized_linf_residual": float(np.max(np.abs(residual)) / scale),
        "scale": scale,
        "scale_definition": (
            "max(max(abs(left)), max(abs(right)), numpy.float64 tiny)"
        ),
    }


def solver_record(pipeline) -> dict:
    solver = pipeline.history.numerics.solver
    dense = pipeline.history.numerics.dense
    return {
        "sampled_configuration": {
            "method": solver.method,
            "rtol": solver.rtol,
            "atol": solver.atol,
            "max_step": (
                "inf" if np.isinf(solver.max_step) else solver.max_step
            ),
            "first_step": solver.first_step,
            "nfev": pipeline.history.solver_nfev,
        },
        "dense_configuration": {
            "method": dense.method,
            "rtol": dense.rtol,
            "atol": dense.atol,
            "max_step": "inf" if np.isinf(dense.max_step) else dense.max_step,
            "first_step": dense.first_step,
            "nfev": pipeline.dense_nfev,
        },
        "n_samples": int(pipeline.history.t.size),
        "message": pipeline.history.solver_message,
    }


def diagnostic_summary(pipeline, diagnostic) -> dict:
    return {
        "scenario_identifier": diagnostic.scenario_identifier,
        "scenario": diagnostic.scenario.to_metadata(),
        "model_role": diagnostic.model_role.value,
        "model_caveat": diagnostic.model_caveat,
        "reference": diagnostic.resolved_reference.to_metadata(),
        "anchor": diagnostic.anchor.to_metadata(),
        "solver": solver_record(pipeline),
        "endpoints": {
            "G": float(diagnostic.relative_growth[-1]),
            "f": float(diagnostic.selected_growth_rate[-1]),
            "A_anchor": float(diagnostic.anchored_density_amplitude[-1]),
            "Q_anchor": float(diagnostic.anchored_density_growth[-1]),
            "Q_alternative": float(
                diagnostic.alternative_nonlogarithmic_evaluation[-1]
            ),
        },
        "identity_max_relative": diagnostic.max_identity_relative_residual,
        "classification": diagnostic.classification.value,
        "limitations": list(diagnostic.limitations),
    }


def compare_diagnostics(reference, comparison) -> dict:
    t = reference.t_solver_units
    z = reference.dressed_redshift
    return {
        name: zero_safe_metrics(
            getattr(reference, field), getattr(comparison, field), t, z
        )
        for name, field in (
            ("G", "relative_growth"),
            ("f", "selected_growth_rate"),
            ("A_anchor", "anchored_density_amplitude"),
            ("Q_anchor", "anchored_density_growth"),
            (
                "Q_alternative",
                "alternative_nonlogarithmic_evaluation",
            ),
        )
    }


def test_environment(python_executable: Path, extra_pythonpath: str) -> dict:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join(
        part
        for part in (extra_pythonpath, str(PROJECT_ROOT / "src"))
        if part
    )
    version_code = (
        "import json,platform,numpy,scipy,pytest,pluggy;"
        "print(json.dumps({'python':platform.python_version(),"
        "'numpy':numpy.__version__,'scipy':scipy.__version__,"
        "'pytest':pytest.__version__,'pluggy':pluggy.__version__},"
        "sort_keys=True))"
    )
    versions = subprocess.run(
        [str(python_executable), "-c", version_code],
        cwd=PROJECT_ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    python_label = json.loads(versions.stdout.strip())["python"].replace(".", "_")
    base_temp = Path(tempfile.gettempdir()) / f"timescape_phase1dd_py_{python_label}"
    if base_temp.exists():
        shutil.rmtree(base_temp)
    command = [
        str(python_executable),
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        "--basetemp",
        str(base_temp),
    ]
    completed = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    output = completed.stdout + completed.stderr
    passed_match = re.search(r"(\d+) passed", output)
    failed_match = re.search(r"(\d+) failed", output)
    skipped_match = re.search(r"(\d+) skipped", output)
    xfailed_match = re.search(r"(\d+) xfailed", output)
    warning_match = re.search(r"(\d+) warnings?", output)
    record = {
        "command": (
            f"{python_executable} -m pytest -q -p no:cacheprovider "
            f"--basetemp <system-temp>/{base_temp.name}"
        ),
        "versions": json.loads(versions.stdout.strip()),
        "returncode": completed.returncode,
        "passed": int(passed_match.group(1)) if passed_match else 0,
        "failed": int(failed_match.group(1)) if failed_match else 0,
        "skipped": int(skipped_match.group(1)) if skipped_match else 0,
        "xfailed": int(xfailed_match.group(1)) if xfailed_match else 0,
        "warnings": int(warning_match.group(1)) if warning_match else 0,
        "same_tracked_source_tree": True,
    }
    if completed.returncode != 0:
        raise RuntimeError(f"complete test suite failed:\n{output}")
    return record


def main() -> None:
    repository_execution = validate_repository_execution_state()
    if git("rev-parse", "HEAD", cwd=UPSTREAM_ROOT) != UPSTREAM_COMMIT:
        raise RuntimeError("upstream clone commit changed")
    if git("status", "--short", cwd=UPSTREAM_ROOT):
        raise RuntimeError("upstream clone is not clean")
    if sha256_lf(UPSTREAM_NOTEBOOK) != NOTEBOOK_SHA256_LF:
        raise RuntimeError("pinned notebook hash changed")

    baseline_scenario = clean_scenario(system=GrowthSystem.COMOVING)
    baseline_pipeline, baseline = evaluate(
        scenario=baseline_scenario,
        reference=REFERENCE_Z10,
        solver=TIGHT_DOP853,
        dense=DENSE,
        n_samples=N_SAMPLES,
        anchor_value=0.8,
    )
    meszaros_pipeline, meszaros = evaluate(
        scenario=clean_scenario(system=GrowthSystem.MESZAROS),
        reference=REFERENCE_Z10,
        solver=TIGHT_DOP853,
        dense=DENSE,
        n_samples=N_SAMPLES,
        anchor_value=0.8,
    )

    algebraic_identities = {
        "comoving": {
            "sampled_growth_consistency": normalized_identity(
                baseline.relative_growth,
                baseline_pipeline.history.delta_d
                / baseline.resolved_reference.amplitude_delta_d,
            ),
            "q_equals_f_times_a": normalized_identity(
                baseline.anchored_density_growth,
                baseline.selected_growth_rate
                * baseline.anchored_density_amplitude,
            ),
            "q_equals_anchor_dg_dln_a": normalized_identity(
                baseline.anchored_density_growth,
                baseline.alternative_nonlogarithmic_evaluation,
            ),
            "continuous_reference_growth": baseline.continuous_reference_growth,
            "continuous_reference_anchored_amplitude": (
                baseline.continuous_reference_anchored_amplitude
            ),
        },
        "meszaros": {
            "sampled_growth_consistency": normalized_identity(
                meszaros.relative_growth,
                meszaros_pipeline.history.delta_d
                / meszaros.resolved_reference.amplitude_delta_d,
            ),
            "q_equals_f_times_a": normalized_identity(
                meszaros.anchored_density_growth,
                meszaros.selected_growth_rate
                * meszaros.anchored_density_amplitude,
            ),
            "q_equals_anchor_dg_dln_a": normalized_identity(
                meszaros.anchored_density_growth,
                meszaros.alternative_nonlogarithmic_evaluation,
            ),
            "continuous_reference_growth": meszaros.continuous_reference_growth,
            "continuous_reference_anchored_amplitude": (
                meszaros.continuous_reference_anchored_amplitude
            ),
        },
    }

    anchor_low = anchored_density_growth_diagnostic(
        growth_result=baseline_pipeline,
        anchor=make_anchor(baseline_pipeline, value=0.5),
        assumptions=ASSUMPTIONS,
    )
    anchor_high = anchored_density_growth_diagnostic(
        growth_result=baseline_pipeline,
        anchor=make_anchor(baseline_pipeline, value=1.0),
        assumptions=ASSUMPTIONS,
    )
    anchor_scaling = {
        "s1": 0.5,
        "s2": 1.0,
        "ratio": 2.0,
        "A_anchor": normalized_identity(
            anchor_high.anchored_density_amplitude,
            2.0 * anchor_low.anchored_density_amplitude,
        ),
        "Q_anchor": normalized_identity(
            anchor_high.anchored_density_growth,
            2.0 * anchor_low.anchored_density_growth,
        ),
        "G_exactly_unchanged": bool(
            np.array_equal(anchor_low.relative_growth, anchor_high.relative_growth)
        ),
        "f_exactly_unchanged": bool(
            np.array_equal(
                anchor_low.selected_growth_rate,
                anchor_high.selected_growth_rate,
            )
        ),
        "scenario_identifier_unchanged": (
            anchor_low.scenario_identifier == anchor_high.scenario_identifier
        ),
        "reference_unchanged": (
            anchor_low.resolved_reference == anchor_high.resolved_reference
        ),
    }

    dressed_pipeline, dressed = evaluate(
        scenario=clean_scenario(
            system=GrowthSystem.COMOVING,
            growth_coordinate=GrowthCoordinate.DRESSED_REDSHIFT,
        ),
        reference=REFERENCE_Z10,
        solver=TIGHT_DOP853,
        dense=DENSE,
        n_samples=N_SAMPLES,
        anchor_value=0.8,
    )
    chain = baseline_pipeline.rates.chain_factor
    bare_dressed = {
        "bare": diagnostic_summary(baseline_pipeline, baseline),
        "dressed": diagnostic_summary(dressed_pipeline, dressed),
        "G_exactly_unchanged": bool(
            np.array_equal(baseline.relative_growth, dressed.relative_growth)
        ),
        "f_chain_identity": normalized_identity(
            dressed.selected_growth_rate,
            baseline.selected_growth_rate * chain,
        ),
        "Q_chain_identity": normalized_identity(
            dressed.anchored_density_growth,
            baseline.anchored_density_growth * chain,
        ),
        "chain_factor_end": float(chain[-1]),
    }

    basis_runs = {}
    for label, k_code in (("synthetic_k7", 7.0), ("synthetic_k13", 13.0)):
        pipeline, diagnostic = evaluate(
            scenario=clean_scenario(
                system=GrowthSystem.COMOVING,
                density_contrast_mapping=(
                    DensityContrastMapping.MAP_TO_DELTA_M_VIA_MINUS_K_CODE2
                ),
                supplied_mode_k=k_code,
                mode_label=label,
            ),
            reference=REFERENCE_Z10,
            solver=TIGHT_DOP853,
            dense=DENSE,
            n_samples=N_SAMPLES,
            anchor_value=0.8,
        )
        basis_runs[label] = {
            "k_code": k_code,
            "summary": diagnostic_summary(pipeline, diagnostic),
            "comparison_to_Delta_d": compare_diagnostics(baseline, diagnostic),
        }

    bare_reference = GrowthReference(
        coordinate=GrowthReferenceCoordinate.BARE_TIME_SOLVER_UNITS,
        value=baseline.resolved_reference.t_solver_units,
        root=PHASE1C_EPOCH_ROOT,
        amplitude_floor_rel=1e-10,
    )
    bare_ref_pipeline, bare_ref_diagnostic = evaluate(
        scenario=baseline_scenario,
        reference=bare_reference,
        solver=TIGHT_DOP853,
        dense=DENSE,
        n_samples=N_SAMPLES,
        anchor_value=0.8,
    )
    reference_equivalence = {
        "dressed_redshift_reference": baseline.resolved_reference.to_metadata(),
        "equivalent_bare_time_reference": (
            bare_ref_diagnostic.resolved_reference.to_metadata()
        ),
        "resolved_time_difference": (
            bare_ref_diagnostic.resolved_reference.t_solver_units
            - baseline.resolved_reference.t_solver_units
        ),
        "diagnostic_comparison": compare_diagnostics(
            baseline, bare_ref_diagnostic
        ),
    }

    one_factor_specs = {
        "perturbation_system": clean_scenario(system=GrowthSystem.MESZAROS),
        "background_preset": clean_scenario(
            system=GrowthSystem.COMOVING,
            background_preset=GrowthBackgroundPreset.PAPER_REFERENCE,
        ),
        "rate_unit_convention": clean_scenario(
            system=GrowthSystem.COMOVING,
            rate_unit_convention=RateUnitConvention.LCDM_TO_TIMESCAPE_CONVERTED,
        ),
        "epoch_choice": clean_scenario(
            system=GrowthSystem.COMOVING,
            epoch_choice=EpochChoice.DRESSED_Z20,
        ),
    }
    one_factor_studies = {}
    for factor, scenario in one_factor_specs.items():
        if factor == "perturbation_system":
            pipeline, diagnostic = meszaros_pipeline, meszaros
        else:
            pipeline, diagnostic = evaluate(
                scenario=scenario,
                reference=REFERENCE_Z10,
                solver=TIGHT_DOP853,
                dense=DENSE,
                n_samples=N_SAMPLES,
                anchor_value=0.8,
            )
        one_factor_studies[factor] = {
            "baseline_scenario_identifier": baseline.scenario_identifier,
            "alternative": diagnostic_summary(pipeline, diagnostic),
            "endpoint_differences_alternative_minus_baseline": {
                "G": float(
                    diagnostic.relative_growth[-1] - baseline.relative_growth[-1]
                ),
                "f": float(
                    diagnostic.selected_growth_rate[-1]
                    - baseline.selected_growth_rate[-1]
                ),
                "A_anchor": float(
                    diagnostic.anchored_density_amplitude[-1]
                    - baseline.anchored_density_amplitude[-1]
                ),
                "Q_anchor": float(
                    diagnostic.anchored_density_growth[-1]
                    - baseline.anchored_density_growth[-1]
                ),
            },
            "array_comparison_note": (
                "only endpoint differences are interpreted; an epoch or preset "
                "change can alter the time grid, so no implicit interpolation "
                "or common-time comparison is performed"
            ),
            "uncertainty_category": (
                "model/approximation dependence"
                if factor == "perturbation_system"
                else "convention/scenario"
            ),
        }

    convergence = {}
    convergence_failures = []
    for system in (GrowthSystem.COMOVING, GrowthSystem.MESZAROS):
        scenario = clean_scenario(system=system)
        reference_pipeline, reference_diagnostic = evaluate(
            scenario=scenario,
            reference=REFERENCE_Z10,
            solver=REFERENCE_SOLVER,
            dense=REFERENCE_DENSE,
            n_samples=N_SAMPLES,
            anchor_value=0.8,
        )
        runs = {}
        for label, solver in (
            ("tight_DOP853", TIGHT_DOP853),
            ("tight_RK45", TIGHT_RK45),
            ("tight_Radau", TIGHT_RADAU),
        ):
            if label == "tight_DOP853":
                if system is GrowthSystem.COMOVING:
                    pipeline, diagnostic = baseline_pipeline, baseline
                else:
                    pipeline, diagnostic = meszaros_pipeline, meszaros
            else:
                pipeline, diagnostic = evaluate(
                    scenario=scenario,
                    reference=REFERENCE_Z10,
                    solver=solver,
                    dense=DENSE,
                    n_samples=N_SAMPLES,
                    anchor_value=0.8,
                )
            metrics = compare_diagnostics(reference_diagnostic, diagnostic)
            worst = max(
                item["normalized_linf_error"] for item in metrics.values()
            )
            passed = worst <= GATES["solver_convergence_normalized_linf_max"]
            if not passed:
                convergence_failures.append(
                    {"system": system.value, "run": label, "worst": worst}
                )
            runs[label] = {
                "solver": solver_record(pipeline),
                "metrics": metrics,
                "worst_normalized_linf": worst,
                "gate": GATES["solver_convergence_normalized_linf_max"],
                "passed": passed,
            }
        convergence[system.value] = {
            "reference": {
                "solver": solver_record(reference_pipeline),
                "definition": (
                    "independent clean-system reference: sampled DOP853 and "
                    "dense DOP853 both use rtol=2e-13, atol=2e-15, "
                    "max_step=inf, first_step=None"
                ),
            },
            "runs": runs,
        }

    identity_gate_results = {
        "comoving_sampled_growth_consistency": (
            algebraic_identities["comoving"]["sampled_growth_consistency"][
                "normalized_linf_residual"
            ]
            <= GATES["sampled_growth_consistency_normalized_max"]
        ),
        "meszaros_sampled_growth_consistency": (
            algebraic_identities["meszaros"]["sampled_growth_consistency"][
                "normalized_linf_residual"
            ]
            <= GATES["sampled_growth_consistency_normalized_max"]
        ),
        "comoving_q_equals_f_times_a": (
            algebraic_identities["comoving"]["q_equals_f_times_a"][
                "normalized_linf_residual"
            ]
            <= GATES["q_equals_f_times_a_normalized_max"]
        ),
        "comoving_q_equals_anchor_dg_dln_a": (
            algebraic_identities["comoving"]["q_equals_anchor_dg_dln_a"][
                "normalized_linf_residual"
            ]
            <= GATES["q_equals_anchor_dg_dln_a_normalized_max"]
        ),
        "meszaros_q_equals_f_times_a": (
            algebraic_identities["meszaros"]["q_equals_f_times_a"][
                "normalized_linf_residual"
            ]
            <= GATES["q_equals_f_times_a_normalized_max"]
        ),
        "meszaros_q_equals_anchor_dg_dln_a": (
            algebraic_identities["meszaros"]["q_equals_anchor_dg_dln_a"][
                "normalized_linf_residual"
            ]
            <= GATES["q_equals_anchor_dg_dln_a_normalized_max"]
        ),
        "anchor_scaling_A": (
            anchor_scaling["A_anchor"]["normalized_linf_residual"]
            <= GATES["anchor_scaling_normalized_max"]
        ),
        "anchor_scaling_Q": (
            anchor_scaling["Q_anchor"]["normalized_linf_residual"]
            <= GATES["anchor_scaling_normalized_max"]
        ),
        "bare_dressed_f": (
            bare_dressed["f_chain_identity"]["normalized_linf_residual"]
            <= GATES["bare_dressed_chain_normalized_max"]
        ),
        "bare_dressed_Q": (
            bare_dressed["Q_chain_identity"]["normalized_linf_residual"]
            <= GATES["bare_dressed_chain_normalized_max"]
        ),
    }
    for label, record in basis_runs.items():
        identity_gate_results[f"basis_{label}"] = all(
            metric["normalized_linf_error"]
            <= GATES["density_basis_invariance_normalized_max"]
            for metric in record["comparison_to_Delta_d"].values()
        )
    identity_gate_results["reference_coordinate_equivalence"] = all(
        metric["normalized_linf_error"]
        <= GATES["reference_coordinate_equivalence_normalized_max"]
        for metric in reference_equivalence["diagnostic_comparison"].values()
    )

    payload = {
        "schema_note": (
            "Phase 1D-D anchored conditional density-growth validation v1; "
            "deterministic independent-package output"
        ),
        "phase_identifier": "Phase 1D-D Candidate A anchored_density_growth_diagnostic",
        "repository_and_frozen_checkpoint_provenance": {
            "repository": "ing-mattioni/timescape-fsigma8",
            **repository_execution,
            "upstream_commit": UPSTREAM_COMMIT,
            "upstream_notebook_path": str(UPSTREAM_NOTEBOOK.relative_to(PROJECT_ROOT)),
            "upstream_notebook_sha256": sha256(UPSTREAM_NOTEBOOK),
            "upstream_notebook_sha256_lf_normalized": sha256_lf(UPSTREAM_NOTEBOOK),
        },
        "exact_diagnostic_equations": {
            "G": "Delta_d(t) / Delta_d(t_ref)",
            "A_anchor": "sigma8_anchor_at_reference * G",
            "Q_anchor_product": "f * A_anchor",
            "Q_anchor_nonlogarithmic": (
                "sigma8_anchor_at_reference * dG/dln(a_coordinate) = "
                "sigma8_anchor_at_reference / Delta_d(t_ref) * "
                "dDelta_d/dln(a_coordinate)"
            ),
            "bare_dressed_chain": (
                "Q_dressed/Q_bare=(2+f_v)^2/(4+f_v+4*f_v^2)"
            ),
        },
        "a1_a6_definitions": ASSUMPTIONS.to_metadata(),
        "api_inventory": {
            "function": (
                "anchored_density_growth_diagnostic(*, growth_result, anchor, "
                "assumptions)"
            ),
            "records": [
                "AnchoredDiagnosticAssumptions",
                "ExternalDensityAmplitudeAnchor",
                "AnchoredDensityGrowthDiagnosticResult",
            ],
            "enums": [
                "AnchorProvenanceKind",
                "AnchoredGrowthModelRole",
                "AnchoredDiagnosticClassification",
            ],
            "no_scientific_defaults": True,
        },
        "explicit_exclusions": [
            "matter or primordial power spectra",
            "transfer functions",
            "window functions and smoothing integrals",
            "sigma_R or sigma8 derived from a spectrum",
            "standard observational f sigma8",
            "barotropic or scale-dependent histories",
            "D3, tilt, or barotropic wavenumber parameters",
            "RSD, Kaiser, bias, AP, survey, covariance, likelihood, fitting, or inference",
        ],
        "validation_only_baseline": {
            "label": "validation_only_baseline_not_an_api_default",
            "scenario": baseline.scenario.to_metadata(),
            "reference": REFERENCE_Z10.coordinate.value,
            "reference_value": REFERENCE_Z10.value,
            "anchor_value": 0.8,
            "anchor_status": (
                "synthetic_validation_only; no observational interpretation"
            ),
            "anchor_metadata": baseline.anchor.to_metadata(),
            "solver": solver_record(baseline_pipeline),
        },
        "per_system_model_role": {
            "comoving": diagnostic_summary(baseline_pipeline, baseline),
            "meszaros": diagnostic_summary(meszaros_pipeline, meszaros),
        },
        "reference_metadata": {
            "baseline": baseline.resolved_reference.to_metadata(),
            "continuous_reference_and_sampled_growth_check": {
                "is_sampled": baseline.reference_is_sampled_grid_point,
                "nearest_index": baseline.reference_nearest_sample_index,
                "nearest_time_offset": baseline.reference_nearest_sample_time_offset,
                "continuous_reference_growth_is_normalization_consequence": True,
                "sampled_growth_expected_definition": (
                    "history.delta_d / reference.amplitude_delta_d"
                ),
                "sampled_growth_normalized_residual": (
                    algebraic_identities["comoving"][
                        "sampled_growth_consistency"
                    ]["normalized_linf_residual"]
                ),
            },
        },
        "algebraic_identity_metrics": algebraic_identities,
        "anchor_scaling_study": anchor_scaling,
        "bare_dressed_study": bare_dressed,
        "density_basis_invariance_study": {
            "Delta_d_baseline": diagnostic_summary(baseline_pipeline, baseline),
            "mapped_delta_m_runs": basis_runs,
        },
        "reference_coordinate_equivalence": reference_equivalence,
        "meszaros_comparison_caveat": meszaros.model_caveat,
        "one_factor_scenario_studies": one_factor_studies,
        "solver_convergence_metrics": convergence,
        "declared_gates": GATES,
        "gate_justification": GATE_JUSTIFICATION,
        "gate_results": {
            "identity": identity_gate_results,
            "convergence_failures": convergence_failures,
            "all_passed": (
                all(identity_gate_results.values())
                and not convergence_failures
            ),
        },
        "uncertainty_taxonomy": {
            "numerical": "finite precision and sampling only",
            "solver": "method/tolerance convergence against the independent reference",
            "external_anchor_normalisation": (
                "linear scale supplied externally; no Timescape prediction"
            ),
            "convention_scenario": (
                "preset, rate-unit, epoch, coordinate, reference representation"
            ),
            "model_approximation_dependence": (
                "comoving primary versus Meszaros comparison-only; never averaged"
            ),
            "rule": "no envelope is a confidence interval",
        },
        "complete_test_environments": {
            "python_3_14": {"status": "pending final in-script test execution"},
            "python_3_11": {"status": "pending final in-script test execution"},
        },
        "exact_file_inventory": {
            "new_tracked_candidates": [
                "src/timescape_fsigma8/growth/anchored_diagnostic.py",
                "tests/test_anchored_density_growth.py",
                "scripts/validate_anchored_density_growth.py",
                "reports/phase1d_d_anchored_density_growth_validation.md",
            ],
            "modified_tracked_candidates": [
                "src/timescape_fsigma8/growth/__init__.py"
            ],
            "new_ignored_generated": [
                "artifacts/independent/phase1d_d_anchored_density_growth_validation.json"
            ],
        },
        "repository_preservation_statement": {
            "frozen_growth_modules_modified": False,
            "background_or_perturbation_modules_modified": False,
            "existing_tests_or_reports_modified": False,
            "upstream_clean": True,
            "upstream_notebook_unchanged": True,
            "nothing_staged": git("diff", "--cached", "--name-only") == "",
            "commit_tag_push_merge_publish_author_contact": False,
        },
    }

    if not payload["gate_results"]["all_passed"]:
        raise RuntimeError(f"validation gates failed: {payload['gate_results']}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    # Provisional write makes the generated-artifact schema available to the
    # complete suites; the final deterministic write below adds their results.
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    # Review finding F6: the phase ran under Python 3.14 (.venv) and 3.11
    # (.venv311) on Windows.  Any primary interpreter other than 3.11 plus the
    # .venv311 environment is accepted; the actual versions are recorded.
    primary_key = f"python_{sys.version_info[0]}_{sys.version_info[1]}"
    if primary_key == "python_3_11":
        raise RuntimeError("run validation with the primary (non-3.11) environment")
    primary_site = sysconfig.get_paths()["purelib"]
    py311 = next(
        (
            candidate
            for candidate in (
                PROJECT_ROOT / ".venv311" / "Scripts" / "python.exe",
                PROJECT_ROOT / ".venv311" / "bin" / "python",
            )
            if candidate.exists()
        ),
        None,
    )
    if py311 is None:
        raise RuntimeError("the Python 3.11 environment .venv311 is required")
    expected_environments = {primary_key, "python_3_11"}
    test_environments = {
        primary_key: test_environment(sys.executable, primary_site),
        "python_3_11": test_environment(py311, ""),
    }
    payload["complete_test_environments"] = test_environments
    payload["repository_preservation_statement"]["same_tracked_source_tree_tested"] = True
    payload["repository_preservation_statement"]["artifact_integrity"] = {
        "required_top_level_section_count": 25,
        "required_top_level_sections_verified": True,
        "all_gates_verified_after_final_parse": True,
        "both_test_environment_records_final": True,
        "second_serialization_byte_identical": True,
        "suite_scope_statement": (
            "complete suites tested this same source tree and the provisional "
            "schema-bearing artifact; the final artifact was parsed and "
            "integrity-checked after suite results were inserted"
        ),
    }
    final_bytes = (
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    OUTPUT.write_bytes(final_bytes)
    readback = OUTPUT.read_bytes()
    parsed = json.loads(readback.decode("utf-8"))
    if set(parsed) != REQUIRED_ARTIFACT_TOP_LEVEL_SECTIONS:
        raise RuntimeError(
            "final artifact top-level schema mismatch: "
            f"{sorted(set(parsed) ^ REQUIRED_ARTIFACT_TOP_LEVEL_SECTIONS)}"
        )
    if parsed["gate_results"]["all_passed"] is not True:
        raise RuntimeError("final artifact does not record all gates passing")
    environments = parsed["complete_test_environments"]
    if set(environments) != expected_environments or any(
        record.get("returncode") != 0
        or "versions" not in record
        or "passed" not in record
        or "status" in record
        for record in environments.values()
    ):
        raise RuntimeError("final artifact test-environment records are incomplete")
    second_serialization = (
        json.dumps(parsed, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    if readback != second_serialization:
        raise RuntimeError("final artifact serialization is not byte-identical")
    final_sha256 = sha256(OUTPUT)

    print(json.dumps({
        "output": str(OUTPUT.relative_to(PROJECT_ROOT)),
        "sha256": final_sha256,
        "top_level_section_count": len(parsed),
        "second_serialization_byte_identical": True,
        "all_gates_passed": payload["gate_results"]["all_passed"],
        "test_environments": test_environments,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
