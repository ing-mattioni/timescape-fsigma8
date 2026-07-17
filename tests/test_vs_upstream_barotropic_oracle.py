"""Like-for-like validation against the local upstream barotropic oracle.

The oracle is git-ignored because it derives from an unlicensed upstream
notebook.  Tests skip cleanly when it is absent.  The public scientific
package is never given the D2 expression; this regression uses only the
isolated forensic harness to reproduce the pinned notebook.
"""

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import _phase1c_b2_forensic as forensic  # noqa: E402
from timescape_fsigma8.background import TrackerParams  # noqa: E402
from timescape_fsigma8.perturbations import (  # noqa: E402
    PHASE1C_EPOCH_ROOT,
    PLANCK_2018_QPLUS_RECIPE,
    UPSTREAM_NOTEBOOK_TIME_UNIT,
    UPSTREAM_RK45_DEFAULTS,
    BarotropicScenario,
    D3Branch,
    EpochChoice,
    RateUnitConvention,
    TiltForm,
    WavenumberConvention,
)


ORACLE_PATH = (
    PROJECT_ROOT / "artifacts" / "upstream" / "oracle_barotropic_perturbations.json"
)
NOTEBOOK_PATH = (
    PROJECT_ROOT
    / ".reference"
    / "Linear-Perturbations-in-averaged-cosmological-models"
    / "ACPT_Timescape.ipynb"
)
EXPECTED_COMMIT = "590c6fd5332acb15f5683ebf392a0d7ce54983c5"
EXPECTED_SHA256 = "86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a"
NORMALIZED_LINF_GATE = 2e-8


@pytest.fixture(scope="module")
def oracle():
    if not ORACLE_PATH.exists():
        pytest.skip("barotropic oracle absent; run extraction script")
    return json.loads(ORACLE_PATH.read_text(encoding="utf-8"))


def _scenario(k: float) -> BarotropicScenario:
    return BarotropicScenario(
        k=k,
        branch=D3Branch.PRINTED_4_15,
        tilt_form=TiltForm.UNRESCALED_V,
        rate_convention=RateUnitConvention.UPSTREAM_UNCONVERTED,
        epoch_choice=EpochChoice.UPSTREAM_0P218_GYR,
        wavenumber_convention=WavenumberConvention.UPSTREAM_TIMESCAPE_K,
        timescape_h=0.7323,
        lcdm_h=0.674,
    )


def test_barotropic_oracle_provenance_is_unchanged(oracle):
    provenance = oracle["provenance"]
    assert provenance["source_cells"] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 15]
    assert provenance["upstream_commit_before"] == EXPECTED_COMMIT
    assert provenance["upstream_commit_after"] == EXPECTED_COMMIT
    assert provenance["upstream_notebook_sha256_before"] == EXPECTED_SHA256
    assert provenance["upstream_notebook_sha256_after"] == EXPECTED_SHA256
    assert provenance["notebook_unmodified"] is True
    assert provenance["solver_convention"] == {
        "method": "RK45",
        "rtol": 1e-3,
        "atol": 1e-6,
        "max_step": "inf",
        "first_step": None,
        "source": "scipy.integrate.solve_ivp defaults made explicit",
    }
    if NOTEBOOK_PATH.exists():
        assert hashlib.sha256(NOTEBOOK_PATH.read_bytes()).hexdigest() == EXPECTED_SHA256


@pytest.mark.parametrize("k", [2.0 * np.pi, 5.0 * np.pi, 10.0 * np.pi])
def test_forensic_barotropic_trajectories_reproduce_upstream(oracle, k):
    constants = oracle["constants"]
    params = TrackerParams(fv0=constants["fv0"], HD0=constants["HD0"])
    solution = forensic._solve_forensic_barotropic(
        params=params,
        scenario=_scenario(k),
        sound_speed_mode=forensic._ForensicSoundSpeed.UPSTREAM_D2_CORRUPTED,
        recipe=PLANCK_2018_QPLUS_RECIPE,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        epoch_root=PHASE1C_EPOCH_ROOT,
        t_eval=np.asarray(oracle["t_eval"], dtype=np.float64),
        config=UPSTREAM_RK45_DEFAULTS,
        G=float(constants["G"]),
    )
    key = format(k, ".17g")
    reference = np.asarray(oracle["barotropic"][key]["y"], dtype=np.float64)
    np.testing.assert_array_equal(solution.t, np.asarray(oracle["barotropic"][key]["t"]))
    for index in range(4):
        scale = max(float(np.max(np.abs(reference[index]))), 1e-300)
        normalized_linf = float(
            np.max(np.abs(solution.y[index] - reference[index])) / scale
        )
        assert normalized_linf < NORMALIZED_LINF_GATE
    assert solution.nfev == oracle["barotropic"][key]["nfev"]
