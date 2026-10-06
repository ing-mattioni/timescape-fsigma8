"""Fixed-domain M3 regression: dimensions, limits, additivity and source values."""

from pathlib import Path
from functools import lru_cache
import json
import sys

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from phase1g_f_volume_budget_successor_numerics import (
    FixedDomainBudget, build_evidence, correct_archived_populations, truncated_universe_budget,
)

# Share the moderately expensive evidence calculation between distinct checks.
build_evidence = lru_cache(maxsize=1)(build_evidence)


def test_volume_is_additive_and_matches_direct_mass_density_accounting():
    # Independently compute physical volumes for two disjoint void bins and walls.
    # M_domain=17 mass units; rho_wall=3 mass/length^3; x=0.2.
    mass = np.array([1.7, 1.7, 13.6])
    density = np.array([0.6, 0.6, 3.0])
    volumes = mass / density
    expected = volumes[:2].sum() / volumes.sum()
    budget = FixedDomainBudget(total_void_mass_fraction=0.2, density_ratio=0.2)
    bin_fraction = budget.cumulative(selected_void_mass_fraction=0.1)
    assert 2.0 * bin_fraction == pytest.approx(expected, rel=0.0, abs=2e-15)
    assert budget.total_void_volume_fraction == pytest.approx(expected, rel=0.0, abs=2e-15)
    # Independent unit rescaling does not change the fraction.
    rescaled = (mass * 1000.0) / (density * 1000.0 / 1e6)
    assert rescaled[:2].sum() / rescaled.sum() == pytest.approx(expected, rel=0.0, abs=2e-15)
    # The old operation genuinely denotes different universes: it is not additive.
    old_bin = truncated_universe_budget(selected_mass=0.1, density_ratio=0.2)
    assert 2 * old_bin == pytest.approx(5.0 / 7.0, rel=0.0, abs=2e-15)
    assert expected == pytest.approx(5.0 / 9.0, rel=0.0, abs=2e-15)


@pytest.mark.parametrize("m,x", [(0.0, 0.2), (0.2, 1.0), (0.8, 0.1), (1.0, 0.2)])
def test_endpoints_and_partition_normalization(m, x):
    b = FixedDomainBudget(total_void_mass_fraction=m, density_ratio=x)
    assert b.cumulative(selected_void_mass_fraction=0.0) == 0.0
    wall_fraction = (1.0 - m) / b.volume_in_mass_over_wall_density_units
    assert wall_fraction + b.total_void_volume_fraction == pytest.approx(1.0, rel=0.0, abs=2e-15)
    assert b.total_void_volume_fraction == pytest.approx(
        truncated_universe_budget(selected_mass=m, density_ratio=x), rel=0.0, abs=2e-15)
    if x == 1.0:
        assert b.cumulative(selected_void_mass_fraction=m / 2) == m / 2


def test_near_vacuum_limit_at_fixed_positive_mass_is_singular_not_empty_tracker():
    b = FixedDomainBudget(total_void_mass_fraction=0.2, density_ratio=1e-12)
    assert b.total_void_volume_fraction == pytest.approx(1.0, rel=0.0, abs=5e-12)
    assert b.cumulative(selected_void_mass_fraction=0.1) == pytest.approx(0.5, rel=0.0, abs=3e-12)
    with pytest.raises(ValueError):
        FixedDomainBudget(total_void_mass_fraction=0.2, density_ratio=0.0)


@pytest.mark.parametrize("m,x", [(-0.1, 0.2), (1.1, 0.2), (float("nan"), 0.2),
                                 (0.2, -1.0), (0.2, float("inf")), (0.2, 1.1)])
def test_invalid_model_inputs_fail_closed(m, x):
    with pytest.raises(ValueError):
        FixedDomainBudget(total_void_mass_fraction=m, density_ratio=x)


@pytest.mark.parametrize("selected", [-0.1, 0.3, float("nan"), float("inf")])
def test_selection_cannot_exceed_domain(selected):
    b = FixedDomainBudget(total_void_mass_fraction=0.2, density_ratio=0.2)
    with pytest.raises(ValueError):
        b.cumulative(selected_void_mass_fraction=selected)


def test_primary_population_published_threshold_and_corrected_history():
    result = build_evidence()
    # [JLH13] A9/A12 printed precision; no new tolerance for the spherical solve.
    assert result["spherical"]["one_plus_delta_sc"] == pytest.approx(0.2047, rel=0.0, abs=5e-5)
    assert result["spherical"]["delta_v"] == pytest.approx(-2.717, rel=0.0, abs=5e-4)
    # Independent audit absorption-CDF values, not a pin to the 481-node
    # trapezoid output. Budget 0.3% covers the measured 0.22-0.24% grid bias
    # at r>=10 (FGA-F3); it is not a physical uncertainty estimate.
    expected = {"PAPER_REFERENCE": 0.01478038764242879, "NW15_CMB_FIT": 0.019203715242954295}
    for name, case in result["cases"].items():
        today, early = case["history"][0], case["history"][-1]
        current = today["fixed_domain_cumulative"]
        assert current["r>=10"] == pytest.approx(expected[name], rel=3e-3, abs=0.0)
        assert current["all_sizes"] == pytest.approx(0.7519694338440862, rel=0.0, abs=2e-12)
        assert current["all_sizes"] == pytest.approx(today["legacy_truncated_universe_budget"]["all_sizes"], rel=0.0, abs=2e-15)
        values = [current[k] for k in ("all_sizes", "r>=1", "r>=2", "r>=5", "r>=10", "r>=15")]
        assert all(a >= b for a, b in zip(values, values[1:]))
        for model in ("cutoff_fixed_domain_h_inv_Mpc", "cutoff_truncated_universe_h_inv_Mpc"):
            assert today[model] is not None and early[model] is not None
            assert today[model] / early[model] > 1.5  # same threshold cannot match both epochs


def test_archive_adapter_keeps_scenarios_and_corrects_only_cumulative_normalization(tmp_path):
    pop = {"void_mass_fraction_1_minus_D": 0.2, "interior_density_ratio": 0.2,
           "lagrangian_fraction": {"all_sizes": 0.2, "r>=1": 0.1},
           "M3_two_scale_volume_budget": {"all_sizes": 5/9, "r>=1": 5/14},
           "volume_weighted_median_radius_h_inv_Mpc": 2.0,
           "resolved_mass_fraction_on_grid": 0.19, "unresolved_below_grid": 0.01}
    source = tmp_path / "frozen.json"
    source.write_text(json.dumps({"results": {"cases": {"case": {"populations": {"C1": pop, "C3": pop}}}}}), encoding="utf-8")
    original = source.read_bytes()
    result = correct_archived_populations(artifact=source)
    assert source.read_bytes() == original
    assert set(result["cases"]["case"]) == {"C1", "C3"}
    for p in result["cases"]["case"].values():
        assert p["fixed_domain_cumulative"]["r>=1"] == pytest.approx(5/18, rel=0.0, abs=2e-15)
        assert p["legacy_truncated_universe_budget"] == pop["M3_two_scale_volume_budget"]
        assert p["unresolved_below_grid"] == 0.01


def test_near_empty_cutoffs_and_tail_accuracy_against_independent_audit():
    # Audit M3 (closed absorption probability, independently integrated EH98).
    # Cutoffs: 0.2% relative covers the inherited grid interpolation. Tail at
    # r>=15: 0.8% covers its measured 0.69-0.75% bias. No claim of 3 digits.
    expected = {"PAPER_REFERENCE": {"0.1": 0.09401730837261367, "0.05": 0.018785423601659915},
                "NW15_CMB_FIT": {"0.1": 0.39359874870325073, "0.05": 0.09524648301125169}}
    tails = {"PAPER_REFERENCE": 0.0010185466556934582, "NW15_CMB_FIT": 0.001305279851462453}
    for name, case in build_evidence()["cases"].items():
        for x, cutoff in expected[name].items():
            assert case["near_empty_C1_collapse"][x]["cutoff_fixed_domain_h_inv_Mpc"] == pytest.approx(
                cutoff, rel=2e-3, abs=0.0)
        assert case["history"][0]["fixed_domain_cumulative"]["r>=15"] == pytest.approx(
            tails[name], rel=8e-3, abs=0.0)


def test_boolean_grains_have_different_volume_budget_from_disjoint_F_cells():
    # Poisson zero-hit probability P(N=0)=exp(-eta), frozen E2: overlap is
    # intrinsic. The mean multiplicity conditional on coverage is eta/f.
    for case in build_evidence()["cases"].values():
        b = case["boolean_surrogate"]
        eta, coverage = b["dimensionless_grain_volume_density_eta"], b["coverage_supplied"]
        assert 1.0 - np.exp(-eta) == pytest.approx(coverage, rel=0.0, abs=2e-15)
        assert eta > case["history"][0]["fixed_domain_cumulative"]["all_sizes"]
        assert b["mean_multiplicity_given_covered"] > 1.0
