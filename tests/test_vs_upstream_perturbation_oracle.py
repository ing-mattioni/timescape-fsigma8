"""Like-for-like validation against the local clean perturbation oracle.

The oracle is git-ignored because it derives from the unlicensed upstream
notebook. Tests skip cleanly when it is absent. The cross-environment gate is
rtol=2e-8 (far above the measured Python-3.14 error of 4.2e-16, but strict
against a meaningful equation, state-ordering, IC, epoch, or solver change).
"""

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations import (
    PLANCK_2018_QPLUS_RECIPE,
    UPSTREAM_RK45_DEFAULTS,
    InitialConditionScenario,
    RateUnitConvention,
    solve_comoving,
    solve_meszaros,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ORACLE_PATH = PROJECT_ROOT / "artifacts" / "upstream" / "oracle_clean_perturbations.json"
NOTEBOOK_PATH = (
    PROJECT_ROOT / ".reference" / "Linear-Perturbations-in-averaged-cosmological-models"
    / "ACPT_Timescape.ipynb"
)
RTOL_ORACLE = 2e-8
ATOL_ORACLE = 2e-12


@pytest.fixture(scope="module")
def oracle():
    if not ORACLE_PATH.exists():
        pytest.skip("clean perturbation oracle absent; run extraction script")
    return json.loads(ORACLE_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def reproduced(oracle):
    constants = oracle["constants"]
    params = TrackerParams(fv0=constants["fv0"], HD0=constants["HD0"])
    initial = InitialConditionScenario(
        recipe=PLANCK_2018_QPLUS_RECIPE,
        rate_units=RateUnitConvention.UPSTREAM_UNCONVERTED,
        timescape_h=constants["h"],
    ).resolve(params)
    t_eval = np.asarray(oracle["t_eval"])
    return {
        "initial": initial,
        "comoving": solve_comoving(
            params=params, initial_conditions=initial, t_eval=t_eval,
            config=UPSTREAM_RK45_DEFAULTS, G=constants["G"]
        ),
        "meszaros": solve_meszaros(
            params=params, initial_conditions=initial, t_eval=t_eval,
            config=UPSTREAM_RK45_DEFAULTS, G=constants["G"]
        ),
    }


def test_oracle_provenance_and_clean_scope(oracle):
    provenance = oracle["provenance"]
    assert provenance["source_cells"] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16]
    assert 12 not in provenance["source_cells"]  # no barotropic system in B1
    assert provenance["notebook_unmodified"] is True
    if NOTEBOOK_PATH.exists():
        digest = hashlib.sha256(NOTEBOOK_PATH.read_bytes()).hexdigest()
        assert digest == provenance["upstream_notebook_sha256"]


def test_initial_conditions_match_oracle_with_cross_scipy_bound(oracle, reproduced):
    expected = oracle["initial_conditions"][:3]
    np.testing.assert_allclose(
        reproduced["initial"].comoving_vector(), expected, rtol=0.0, atol=2e-10
    )


@pytest.mark.parametrize("system", ["comoving", "meszaros"])
def test_upstream_compatible_trajectories(oracle, reproduced, system):
    solution = reproduced[system]
    np.testing.assert_allclose(solution.t, oracle[system]["t"], rtol=0.0, atol=0.0)
    np.testing.assert_allclose(
        solution.y,
        np.asarray(oracle[system]["y"]),
        rtol=RTOL_ORACLE,
        atol=ATOL_ORACLE,
    )
