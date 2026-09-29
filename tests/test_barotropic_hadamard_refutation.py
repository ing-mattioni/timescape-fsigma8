"""Regression for the approved barotropic continuum-stability refutation.

Evidence: reports/phase1g_a_sigma8_derivation_path_audit.md Sec. 4.1 ([1G-A]).
Status change: reports/phase1g_a_barotropic_status_successor.md (human
approval dated 2026-09-29).  [GM] = Galoppo & Mourier, arXiv:2511.17160v2.

The principal part of [GM] Eq. (4.19) is ``Delta_eff'' - c_s^2 (3)Laplacian
Delta_eff``.  With the corrected Timescape ``c_s,eff^2 < 0`` (Phase 1B) the
frozen matrix of [GM] Eqs. (4.15), (4.17) has ``A23*A32 = -c_s^2 k^2/a_D^2 >
0``, so a mode of wavenumber k grows like ``exp(k*alpha)`` with the WKB
exponent ``alpha = int sqrt(-c_s^2) dt/a_D``: the unrestricted Cauchy problem
is Hadamard ill-posed.  The reference computation is
``scripts/phase1g_a_sigma8_path_numerics.py::barotropic_evidence``; the part
needed here is re-implemented with the same configuration (dressed H0 = 1,
matrix-convention k, z = 20 to t0, EdS-like growing data, DOP853).

The frozen barotropic runtime is exercised for both D3 branches, never
changed, guarded or defaulted.  Every tolerance is stated explicitly below
(AGENTS.md rule 9).
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

import timescape_fsigma8.background as bg
from timescape_fsigma8 import scientific_status
from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations import (
    D3Branch,
    TiltForm,
    WavenumberConvention,
    barotropic_matrix,
    barotropic_rhs,
)
from timescape_fsigma8.perturbations.initial_conditions import PLANCK_2018_QPLUS_RECIPE
from timescape_fsigma8.presets import PAPER_REFERENCE
from timescape_fsigma8.scientific_status import CURRENT_SCIENTIFIC_STATUS

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

TOKEN = "UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY"
OLD_TOKEN = "NOT_DERIVED"
NEW_TOKEN = "REFUTED_HADAMARD_ILL_POSED"
SUCCESSOR = PROJECT_ROOT / "reports" / "phase1g_a_barotropic_status_successor_inventory.json"
FROZEN_1F_C_R_INVENTORY = PROJECT_ROOT / "reports" / "phase1f_c_r_astra_audit_remediation_inventory.json"
PHASE1G_A_INVENTORY = PROJECT_ROOT / "reports" / "phase1g_a_sigma8_derivation_path_inventory.json"

# Configuration of [1G-A] barotropic_evidence.  G cancels in the
# dimensionless coefficients; it is passed explicitly (no package default).
G = 1.0
Z_INITIAL = 20.0
TIMESCAPE_H = PAPER_REFERENCE.H0_dressed_km_s_Mpc / 100.0
LCDM_H = PLANCK_2018_QPLUS_RECIPE.h  # validated only; unused by UPSTREAM_TIMESCAPE_K
C_KM_S = 299792.458
R8_H_MPC = 8.0

# Numerical controls, identical to the [1G-A] evidence script.
REDSHIFT_ROOT_XTOL = 1e-18
REDSHIFT_ROOT_RTOL = 4.0 * np.finfo(float).eps
REDSHIFT_ROOT_MAXITER = 500
ALPHA_QUAD_EPSABS = 0.0
ALPHA_QUAD_EPSREL = 1e-12
ALPHA_QUAD_LIMIT = 400
BAROTROPIC_SOLVE_RTOL = 1e-10
BAROTROPIC_SOLVE_ATOL = 1e-30  # as in [1G-A]: effectively pure relative control

# Recorded [1G-A] values (inventory closure_admissibility.barotropic, Sec. 4.1).
ALPHA_1G_A = 1.706948
# Seven significant digits are recorded: rounding contributes <= 3e-7
# relative; the quadrature is requested at 1e-12.
ALPHA_RTOL = 1e-6
ALPHA_QUAD_ABSERR_MAX = 1e-10
CS2_EFF_1G_A = {"z=20": -0.4996, "t0": -0.3912}
CS2_EFF_ATOL = 5e-5  # four-decimal rounding of the recorded values
CS2_SIGN_SAMPLES = 2001  # sampled sign check of the ellipticity condition
SLOPE_32PI_64PI_1G_A = {"derived_4_10": 1.6994, "printed_4_15": 1.6996}
SLOPE_RECORD_ATOL = 1e-4  # four-decimal rounding (5e-5) plus solver margin
# WKB with an algebraic amplitude prefactor k^p predicts slopes below alpha
# with a gap O(1/k): observed 0.0074-0.0075 at 32pi->64pi.
SLOPE_GAP_BAND = (0.0, 0.01)
# Halving of that gap when k doubles (O(1/k) predicts 2; observed 2.15-2.16).
GAP_RATIO_BAND = (1.5, 3.0)
# The D3 branch changes only the k-independent A33 entry (observed 1.3e-4).
D3_SLOPE_DIFFERENCE_ATOL = 1e-3
EXPONENT_KR1_R8_1G_A = 875.4
EXPONENT_KR1_R8_ATOL = 0.05  # one-decimal rounding of the recorded value
# Exact algebraic identity of a two-factor product: roundoff only
# (observed 2.2e-16).
SYMBOL_RTOL = 1e-13

WAVENUMBERS = (16.0 * math.pi, 32.0 * math.pi, 64.0 * math.pi)


@pytest.fixture(scope="module")
def params() -> TrackerParams:
    return TrackerParams.from_dressed_H0(fv0=PAPER_REFERENCE.fv0, H0=1.0)


@pytest.fixture(scope="module")
def t_initial(params: TrackerParams) -> float:
    # Invert the dressed redshift z(t) ([GM] p. 25; frozen Phase 1B).
    return brentq(
        lambda t: float(bg.redshift(t, params)) - Z_INITIAL,
        1e-12 * params.t0, params.t0,
        xtol=REDSHIFT_ROOT_XTOL, rtol=REDSHIFT_ROOT_RTOL, maxiter=REDSHIFT_ROOT_MAXITER,
    )


@pytest.fixture(scope="module")
def wkb_alpha(params: TrackerParams, t_initial: float) -> tuple[float, float]:
    return quad(
        lambda t: math.sqrt(-float(bg.cs2_eff(t, params))) / float(bg.a_D(t, params)),
        t_initial, params.t0,
        epsabs=ALPHA_QUAD_EPSABS, epsrel=ALPHA_QUAD_EPSREL, limit=ALPHA_QUAD_LIMIT,
    )


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_status_token_is_refuted_and_successor_record_is_consistent() -> None:
    assert scientific_status.UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY == NEW_TOKEN
    assert CURRENT_SCIENTIFIC_STATUS[TOKEN] == NEW_TOKEN
    successor = load_json(SUCCESSOR)
    change = successor["status_changes"][TOKEN]
    assert (change["old_token"], change["new_token"]) == (OLD_TOKEN, NEW_TOKEN)
    assert successor["human_approval"]["date"] == "2026-09-29"
    assert successor["scope"]["barotropic_runtime_changed"] is False
    # The frozen historical records are untouched: they still hold the old
    # token and the 1G-A recommendation that this record applies.
    frozen = load_json(FROZEN_1F_C_R_INVENTORY)["current_scientific_status"]
    assert frozen[TOKEN] == OLD_TOKEN
    recommendations = load_json(PHASE1G_A_INVENTORY)["recommendations_require_human_approval"]
    assert f"{TOKEN}: {OLD_TOKEN} -> {NEW_TOKEN}" in recommendations
    # A refutation grants nothing.
    for name in ("UNIQUE_TIMESCAPE_PREDICTION", "OBSERVATIONAL_AUTHORIZATION",
                 "RSD_AUTHORIZATION", "SIGMA8_AUTHORIZATION", "FSIGMA8_AUTHORIZATION"):
        assert CURRENT_SCIENTIFIC_STATUS[name] == "NOT_GRANTED"


def test_validator_keeps_frozen_snapshot_and_reads_live_value_from_successor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(PROJECT_ROOT)
    import validate_phase1f_c_r_astra_remediation as remediation

    frozen = load_json(FROZEN_1F_C_R_INVENTORY)["current_scientific_status"]
    changes = remediation.successor_status_changes()
    assert changes == {TOKEN: {"old_token": OLD_TOKEN, "new_token": NEW_TOKEN,
                               "record": "reports/phase1g_a_barotropic_status_successor_inventory.json"}}
    remediation.check_current_scientific_status(frozen, CURRENT_SCIENTIFIC_STATUS, changes)
    # The historical check stays active: a frozen snapshot that no longer
    # records the superseded token is rejected ...
    with pytest.raises(AssertionError, match="frozen snapshot"):
        remediation.check_current_scientific_status(
            {**frozen, TOKEN: NEW_TOKEN}, CURRENT_SCIENTIFIC_STATUS, changes)
    # ... and so is a live value that disagrees with the successor record,
    with pytest.raises(AssertionError, match="successor record"):
        remediation.check_current_scientific_status(
            frozen, {**CURRENT_SCIENTIFIC_STATUS, TOKEN: OLD_TOKEN}, changes)
    # ... and any drift of a token that no successor record covers.
    with pytest.raises(AssertionError, match="D3_VERDICT"):
        remediation.check_current_scientific_status(
            frozen, {**CURRENT_SCIENTIFIC_STATUS, "D3_VERDICT": "CHANGED"}, changes)


@pytest.mark.parametrize("tilt_form", list(TiltForm))
def test_principal_symbol_is_positive_and_branch_independent(
    params: TrackerParams, t_initial: float, tilt_form: TiltForm,
) -> None:
    k = WAVENUMBERS[-1]
    for t in np.linspace(t_initial, params.t0, 5):
        matrices = {
            branch: barotropic_matrix(
                float(t), params=params, G=G, k=k, branch=branch, tilt_form=tilt_form,
                wavenumber_convention=WavenumberConvention.UPSTREAM_TIMESCAPE_K,
                timescape_h=TIMESCAPE_H, lcdm_h=LCDM_H,
            )
            for branch in D3Branch
        }
        cs2 = float(bg.cs2_eff(float(t), params))
        symbol = -cs2 * k**2 / float(bg.a_D(float(t), params)) ** 2
        assert cs2 < 0.0 and symbol > 0.0
        for matrix in matrices.values():
            # [GM] Eqs. (4.15), (4.17): A23*A32 = -c_s^2 k^2/a_D^2.
            np.testing.assert_allclose(matrix[2, 3] * matrix[3, 2], symbol,
                                       rtol=SYMBOL_RTOL, atol=0.0)
        printed, derived = matrices[D3Branch.PRINTED_4_15], matrices[D3Branch.DERIVED_4_10]
        # D3 alters only the k-independent A33 entry, never the symbol.
        assert printed[2, 3] == derived[2, 3] and printed[3, 2] == derived[3, 2]
        assert np.count_nonzero(printed != derived) == 1 and printed[2, 2] != derived[2, 2]


def test_wkb_exponent_reproduces_phase1g_a(
    params: TrackerParams, t_initial: float, wkb_alpha: tuple[float, float],
) -> None:
    alpha, abserr = wkb_alpha
    assert abserr <= ALPHA_QUAD_ABSERR_MAX
    np.testing.assert_allclose(alpha, ALPHA_1G_A, rtol=ALPHA_RTOL, atol=0.0)
    np.testing.assert_allclose(float(bg.cs2_eff(t_initial, params)), CS2_EFF_1G_A["z=20"],
                               rtol=0.0, atol=CS2_EFF_ATOL)
    np.testing.assert_allclose(float(bg.cs2_eff(params.t0, params)), CS2_EFF_1G_A["t0"],
                               rtol=0.0, atol=CS2_EFF_ATOL)
    samples = np.asarray(bg.cs2_eff(np.linspace(t_initial, params.t0, CS2_SIGN_SAMPLES), params))
    assert np.all(samples < 0.0)
    # sigma_8 scale: kR = 1 at R = 8/h Mpc, matrix k = a_D0 (c/H0) k_phys0
    # (1D-A Sec. 10 unit chain, as in [1G-A]); exp(alpha*k) overflows float64.
    k_matrix_r8 = params.aD0 * (C_KM_S / (100.0 * TIMESCAPE_H)) / (R8_H_MPC / TIMESCAPE_H)
    np.testing.assert_allclose(alpha * k_matrix_r8, EXPONENT_KR1_R8_1G_A,
                               rtol=0.0, atol=EXPONENT_KR1_R8_ATOL)
    assert alpha * k_matrix_r8 > math.log(np.finfo(float).max)


def final_log_amplitude(params: TrackerParams, t_initial: float, k: float, branch: D3Branch) -> float:
    def rhs(t, y):
        return barotropic_rhs(
            t, y, params=params, G=G, k=k, branch=branch,
            tilt_form=TiltForm.RESCALED_VTILDE,
            wavenumber_convention=WavenumberConvention.UPSTREAM_TIMESCAPE_K,
            timescape_h=TIMESCAPE_H, lcdm_h=LCDM_H,
        )

    # State (Delta_d, Z, Delta_eff, Vtilde); EdS-like growing Delta_d data.
    y0 = [1.0, -(2.0 / 3.0) / t_initial, 0.0, 0.0]
    solution = solve_ivp(
        rhs, (t_initial, params.t0), y0, method="DOP853",
        rtol=BAROTROPIC_SOLVE_RTOL, atol=BAROTROPIC_SOLVE_ATOL,
        dense_output=False, max_step=np.inf, first_step=None, vectorized=False,
    )
    assert solution.success, solution.message
    return math.log(abs(float(solution.y[2, -1])))


@pytest.fixture(scope="module")
def slopes(params: TrackerParams, t_initial: float) -> dict[D3Branch, tuple[float, float]]:
    result = {}
    for branch in D3Branch:
        logs = [final_log_amplitude(params, t_initial, k, branch) for k in WAVENUMBERS]
        result[branch] = tuple(
            (logs[i + 1] - logs[i]) / (WAVENUMBERS[i + 1] - WAVENUMBERS[i]) for i in range(2)
        )
    return result


@pytest.mark.parametrize("branch", list(D3Branch))
def test_frozen_barotropic_growth_rate_approaches_wkb_exponent(
    slopes: dict[D3Branch, tuple[float, float]], wkb_alpha: tuple[float, float],
    branch: D3Branch,
) -> None:
    alpha = wkb_alpha[0]
    coarse, fine = slopes[branch]  # 16pi->32pi and 32pi->64pi
    np.testing.assert_allclose(fine, SLOPE_32PI_64PI_1G_A[branch.value],
                               rtol=0.0, atol=SLOPE_RECORD_ATOL)
    low, high = SLOPE_GAP_BAND
    assert low < alpha - fine <= high
    ratio = (alpha - coarse) / (alpha - fine)
    assert GAP_RATIO_BAND[0] <= ratio <= GAP_RATIO_BAND[1]


def test_d3_branch_does_not_change_the_rate(
    slopes: dict[D3Branch, tuple[float, float]],
) -> None:
    np.testing.assert_allclose(
        slopes[D3Branch.DERIVED_4_10][1], slopes[D3Branch.PRINTED_4_15][1],
        rtol=0.0, atol=D3_SLOPE_DIFFERENCE_ATOL,
    )
