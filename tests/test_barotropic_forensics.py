"""Isolation and diagnostic tests for the Phase 1C-B2 D2 harness."""

from pathlib import Path
import sys

import numpy as np
import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import _phase1c_b2_forensic as forensic  # noqa: E402
import timescape_fsigma8.background as bg  # noqa: E402
import timescape_fsigma8.perturbations as perturbations  # noqa: E402
from timescape_fsigma8.background import TrackerParams  # noqa: E402
from timescape_fsigma8.perturbations import (  # noqa: E402
    PHASE1C_EPOCH_ROOT,
    PLANCK_2018_QPLUS_RECIPE,
    UPSTREAM_NOTEBOOK_TIME_UNIT,
    BarotropicScenario,
    D3Branch,
    EpochChoice,
    EpochScenario,
    RateUnitConvention,
    SolverConfig,
    TiltForm,
    WavenumberConvention,
    barotropic_matrix,
    tilt_state_transform,
    tilt_state_transform_dot,
    transform_barotropic_state,
)


G = 1.0
K = 10.0 * np.pi
TIMESCAPE_H = 0.7323
LCDM_H = 0.674
REFERENCE_DOP853 = SolverConfig(
    method="DOP853", rtol=2e-13, atol=2e-15, max_step=np.inf, first_step=None
)


@pytest.fixture(scope="module")
def params():
    return TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0)


def make_scenario(tilt_form: TiltForm, branch: D3Branch) -> BarotropicScenario:
    return BarotropicScenario(
        k=K,
        branch=branch,
        tilt_form=tilt_form,
        rate_convention=RateUnitConvention.UPSTREAM_UNCONVERTED,
        epoch_choice=EpochChoice.UPSTREAM_0P218_GYR,
        wavenumber_convention=WavenumberConvention.UPSTREAM_TIMESCAPE_K,
        timescape_h=TIMESCAPE_H,
        lcdm_h=LCDM_H,
    )


def test_forensic_corrected_mode_equals_scientific_matrix(params):
    """The isolated harness changes only the explicitly selected sound speed."""
    t = 0.47 * params.t0
    for branch in D3Branch:
        for tilt_form in TiltForm:
            selected = make_scenario(tilt_form, branch)
            forensic_matrix = forensic._forensic_barotropic_matrix(
                t,
                params=params,
                G=G,
                scenario=selected,
                sound_speed_mode=forensic._ForensicSoundSpeed.CORRECTED_PHASE1B,
            )
            scientific_matrix = barotropic_matrix(
                t,
                params=params,
                G=G,
                k=selected.k,
                branch=selected.branch,
                tilt_form=selected.tilt_form,
                wavenumber_convention=selected.wavenumber_convention,
                timescape_h=selected.timescape_h,
                lcdm_h=selected.lcdm_h,
            )
            np.testing.assert_allclose(
                forensic_matrix, scientific_matrix, rtol=2e-14, atol=0.0
            )


def test_forensic_d2_sound_speed_matches_audited_values(params):
    """Pin the independently derived D2 expression from the Phase 1C-A audit."""
    t_initial = 0.218 * 0.7323 / 9.778
    values = forensic._upstream_d2_corrupted_cs2(
        np.array([t_initial, params.t0]), params
    )
    np.testing.assert_allclose(values, [-0.47372, -0.34516], atol=6e-6, rtol=0.0)
    assert values[0] != pytest.approx(float(bg.cs2_eff(t_initial, params)), abs=1e-3)
    assert values[1] != pytest.approx(float(bg.cs2_eff(params.t0, params)), abs=1e-3)


@pytest.mark.parametrize("branch", list(D3Branch))
def test_d2_breaks_direct_tilt_form_equivalence(params, branch):
    """D2 violates the [GM] Eq. (3.17) transform used between V and Vtilde."""
    t = 0.58 * params.t0
    scenario_v = make_scenario(TiltForm.UNRESCALED_V, branch)
    scenario_tilde = make_scenario(TiltForm.RESCALED_VTILDE, branch)
    matrix_v = forensic._forensic_barotropic_matrix(
        t,
        params=params,
        G=G,
        scenario=scenario_v,
        sound_speed_mode=forensic._ForensicSoundSpeed.UPSTREAM_D2_CORRUPTED,
    )
    matrix_tilde = forensic._forensic_barotropic_matrix(
        t,
        params=params,
        G=G,
        scenario=scenario_tilde,
        sound_speed_mode=forensic._ForensicSoundSpeed.UPSTREAM_D2_CORRUPTED,
    )
    transform = tilt_state_transform(
        t,
        params=params,
        from_tilt_form=TiltForm.UNRESCALED_V,
        to_tilt_form=TiltForm.RESCALED_VTILDE,
    )
    transform_dot = tilt_state_transform_dot(
        t,
        params=params,
        from_tilt_form=TiltForm.UNRESCALED_V,
        to_tilt_form=TiltForm.RESCALED_VTILDE,
    )
    transformed = (
        transform_dot @ np.linalg.inv(transform)
        + transform @ matrix_v @ np.linalg.inv(transform)
    )
    mismatch = matrix_tilde - transformed
    cs2_d2 = float(forensic._upstream_d2_corrupted_cs2(t, params))
    cs2_corrected = float(bg.cs2_eff(t, params))
    expected_a44_mismatch = float(bg.Theta(t, params)) * (cs2_corrected - cs2_d2)
    assert mismatch[3, 3] == pytest.approx(expected_a44_mismatch, rel=2e-13)
    assert abs(mismatch[3, 3]) > 1e-3


def test_d2_forensic_code_is_absent_from_public_api_and_scientific_source():
    forbidden_names = {
        "_ForensicSoundSpeed",
        "_upstream_d2_corrupted_cs2",
        "_forensic_barotropic_matrix",
        "_solve_forensic_barotropic",
    }
    assert forbidden_names.isdisjoint(set(perturbations.__all__))
    for name in forbidden_names:
        assert not hasattr(perturbations, name)
    scientific_source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (PROJECT_ROOT / "src" / "timescape_fsigma8").rglob("*.py")
    )
    assert "upstream_d2_corrupted" not in scientific_source
    assert "18.0 * f**6" not in scientific_source


@pytest.mark.parametrize("branch", list(D3Branch))
def test_d2_tilt_trajectories_are_numerically_nonequivalent(params, branch):
    """Show that the forensic D2 value breaks [GM] Vtilde=(1+w)V dynamically."""
    epoch = EpochScenario(
        choice=EpochChoice.UPSTREAM_0P218_GYR,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        root=PHASE1C_EPOCH_ROOT,
    ).resolve(params)
    times = np.linspace(epoch.time, params.t0, 1001)
    solutions = {}
    for tilt_form in TiltForm:
        solutions[tilt_form] = forensic._solve_forensic_barotropic(
            params=params,
            scenario=make_scenario(tilt_form, branch),
            sound_speed_mode=forensic._ForensicSoundSpeed.UPSTREAM_D2_CORRUPTED,
            recipe=PLANCK_2018_QPLUS_RECIPE,
            time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
            epoch_root=PHASE1C_EPOCH_ROOT,
            t_eval=times,
            config=REFERENCE_DOP853,
            G=G,
        )
    transformed = np.column_stack(
        [
            transform_barotropic_state(
                float(t),
                solutions[TiltForm.UNRESCALED_V].y[:, index],
                params=params,
                from_tilt_form=TiltForm.UNRESCALED_V,
                to_tilt_form=TiltForm.RESCALED_VTILDE,
            )
            for index, t in enumerate(times)
        ]
    )
    direct = solutions[TiltForm.RESCALED_VTILDE].y
    normalized_linf = []
    for index in range(4):
        scale = max(float(np.max(np.abs(direct[index]))), 1e-300)
        normalized_linf.append(
            float(np.max(np.abs(direct[index] - transformed[index]))) / scale
        )
    assert max(normalized_linf) > 0.1
