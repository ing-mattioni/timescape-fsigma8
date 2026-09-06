"""Crossing scan, refinement, intervals, and the frozen baseline pattern."""

# A06: absolute budgets use rtol=0; relative budgets use atol=0.
# Previously implicit algebraic comparisons use rtol=2e-12, atol=1e-14
# in the fixture units (roundoff allowance); explicit convergence budgets remain.

import numpy as np
import pytest

from timescape_fsigma8.growth import (
    DUST_COMPONENT,
    EXPANSION_COMPONENT,
    GrowthD3Branch,
    GrowthSystem,
    GrowthTiltForm,
    scan_sign_changes,
)
from growth_test_utils import (
    BASELINE_MODES,
    FROZEN_1DA_BRACKETS,
    barotropic_scenario,
    clean_scenario,
    run_cached,
)


# ---------------------------------------------------------------- scanning
def test_strict_sign_change_scan_finds_brackets_and_preserves_them():
    # 10-point grid keeps the roots at 1/6, 1/2, 5/6 strictly off-sample.
    t = np.linspace(0.0, 1.0, 10)
    y = np.cos(3.0 * np.pi * t)
    brackets, endpoints, mask = scan_sign_changes(
        component=DUST_COMPONENT, t=t, y=y, near_zero_rel_floor=1e-12
    )
    assert len(brackets) == 3
    for b in brackets:
        assert b.t_right - b.t_left == pytest.approx(1.0 / 9.0, rel=2e-12, abs=1e-14)
        assert b.y_left * b.y_right < 0.0
        assert b.right_index == b.left_index + 1
    assert not endpoints
    assert not mask.any()


def test_rounding_zero_sample_is_flagged_not_promoted_to_root():
    t = np.linspace(0.0, 1.0, 5)
    y = np.array([1.0, 0.0, 1.0, 1.0, 1.0])  # rounding zero, no sign change
    brackets, endpoints, mask = scan_sign_changes(
        component=DUST_COMPONENT, t=t, y=y, near_zero_rel_floor=1e-12
    )
    assert brackets == []
    assert mask[1]
    assert not endpoints  # interior near-zero is not an endpoint root


def test_endpoint_zero_reported_as_endpoint_root_not_strict_change():
    t = np.linspace(0.0, 1.0, 5)
    y = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    brackets, endpoints, mask = scan_sign_changes(
        component=EXPANSION_COMPONENT, t=t, y=y, near_zero_rel_floor=1e-12
    )
    assert brackets == []
    assert len(endpoints) == 1
    assert endpoints[0].index == 0
    assert endpoints[0].component == EXPANSION_COMPONENT


# ---------------------------------------------------------------- clean systems
@pytest.mark.parametrize(
    "system", [GrowthSystem.MESZAROS, GrowthSystem.COMOVING]
)
def test_clean_upstream_compatible_trajectories_have_no_crossings(system):
    run = run_cached(clean_scenario(system))
    assert run.crossings.delta_d_roots == ()
    assert run.crossings.z_roots == ()
    assert run.crossings.endpoint_roots == ()
    assert len(run.validity_intervals) == 1
    only = run.validity_intervals[0]
    assert not only.start_open and not only.end_open
    assert only.amplitude_sign == 1
    assert only.contains_reference


# ---------------------------------------------------------------- baseline pattern
@pytest.mark.parametrize("mode_label, mode_k", BASELINE_MODES)
@pytest.mark.parametrize(
    "branch", [GrowthD3Branch.PRINTED_4_15, GrowthD3Branch.DERIVED_4_10]
)
def test_baseline_crossing_pattern_matches_frozen_1da_brackets(
    branch, mode_label, mode_k
):
    """Refined roots derived from the solver, checked against frozen brackets.

    The frozen Phase 1D-A locations are sampled-grid brackets only; each
    refined root must fall inside its bracket and must not simply be a
    bracket sample.  Additional roots would be reported by these asserts.
    """
    run = run_cached(barotropic_scenario(branch, mode_k, mode_label))
    frozen = FROZEN_1DA_BRACKETS[(branch.value, mode_label)]
    expected_dd = 0 if frozen["Delta_d"] is None else 1
    expected_z = 0 if frozen["Z"] is None else 1
    assert len(run.crossings.delta_d_roots) == expected_dd, (
        f"unexpected Delta_d root count for {branch.value} {mode_label}: "
        f"{[r.t_root for r in run.crossings.delta_d_roots]}"
    )
    assert len(run.crossings.z_roots) == expected_z, (
        f"unexpected Z root count for {branch.value} {mode_label}: "
        f"{[r.t_root for r in run.crossings.z_roots]}"
    )
    if expected_dd:
        root = run.crossings.delta_d_roots[0]
        lo, hi = frozen["Delta_d"]
        assert lo < root.t_root < hi
        assert root.t_root not in (root.bracket_left, root.bracket_right)
        assert root.brentq_converged
        assert root.residual <= 1e-6 * root.residual_scale
    if expected_z:
        z_root = run.crossings.z_roots[0]
        lo, hi = frozen["Z"]
        assert lo < z_root.t_root < hi
        # Z crosses strictly before Delta_d in every sampled scenario
        if expected_dd:
            assert z_root.t_root < run.crossings.delta_d_roots[0].t_root


# ---------------------------------------------------------------- refinement details
@pytest.fixture(scope="module")
def derived_2pi_run():
    return run_cached(
        barotropic_scenario(GrowthD3Branch.DERIVED_4_10, 2.0 * np.pi, "2pi")
    )


def test_refined_root_lies_strictly_inside_its_sampled_bracket(derived_2pi_run):
    for root in (
        derived_2pi_run.crossings.delta_d_roots
        + derived_2pi_run.crossings.z_roots
    ):
        assert root.bracket_left < root.t_root < root.bracket_right
        assert root.root_uncertainty > 0.0
        assert root.brentq_iterations > 0


def test_root_records_carry_every_required_coordinate(derived_2pi_run):
    import timescape_fsigma8.background as bg

    params = derived_2pi_run.history.background.params
    root = derived_2pi_run.crossings.delta_d_roots[0]
    assert root.t_root_gyr == pytest.approx(
        root.t_root / derived_2pi_run.history.time_unit_per_gyr, rel=2e-12, abs=1e-14
    )
    assert root.dressed_redshift == pytest.approx(
        float(bg.redshift(root.t_root, params)), rel=1e-12, abs=0.0
    )
    assert root.a_D == pytest.approx(
        float(bg.a_D(root.t_root, params)), rel=1e-12, abs=0.0
    )
    assert root.a_obs == pytest.approx(
        float(bg.a_w(root.t_root, params)), rel=1e-12, abs=0.0
    )
    meta = root.to_metadata()
    for key in (
        "component",
        "t_root_solver_units",
        "t_root_gyr",
        "dressed_redshift",
        "a_D",
        "a_obs",
        "bracket_solver_units",
        "root_uncertainty_solver_units",
        "residual",
        "residual_over_scale",
        "scenario_identifier",
    ):
        assert key in meta


def test_root_residual_gate_is_enforced(derived_2pi_run):
    root = derived_2pi_run.crossings.delta_d_roots[0]
    gate = derived_2pi_run.history.numerics.root.residual_scale_gate
    assert root.residual <= gate * root.residual_scale


# ---------------------------------------------------------------- intervals
def test_validity_intervals_are_maximal_with_explicit_semantics(derived_2pi_run):
    intervals = derived_2pi_run.validity_intervals
    assert len(intervals) == 2
    first, second = intervals
    root_t = derived_2pi_run.crossings.delta_d_roots[0].t_root
    assert first.end == pytest.approx(root_t, rel=2e-12, abs=1e-14)
    assert second.start == pytest.approx(root_t, rel=2e-12, abs=1e-14)
    # closed at integration endpoints, open at the amplitude root
    assert not first.start_open and first.end_open
    assert second.start_open and not second.end_open
    assert first.amplitude_sign == 1 and second.amplitude_sign == -1
    assert first.contains_reference and not second.contains_reference
    # sample masks partition the grid around the root
    assert first.sample_start_index == 0
    assert second.sample_end_index == derived_2pi_run.history.t.size - 1
    assert first.sample_end_index + 1 == second.sample_start_index


def test_serialization_never_joins_rate_arrays_across_a_pole(derived_2pi_run):
    segments = derived_2pi_run.rate_segments()
    assert len(segments) == 2
    t_first = segments[0]["t_solver_units"]
    t_second = segments[1]["t_solver_units"]
    root_t = derived_2pi_run.crossings.delta_d_roots[0].t_root
    assert max(t_first) < root_t < min(t_second)
    payload = derived_2pi_run.to_json_dict()
    assert "rate_segments" in payload
    assert "f_bare" not in payload  # no joined top-level rate array
