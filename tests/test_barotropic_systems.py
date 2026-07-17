"""Equation, convention, and transformation tests for Phase 1C-B2."""

from dataclasses import MISSING, fields
import inspect

import numpy as np
import pytest

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations import (
    PHASE1C_EPOCH_ROOT,
    PLANCK_2018_QPLUS_RECIPE,
    UPSTREAM_NOTEBOOK_TIME_UNIT,
    BarotropicScenario,
    D3Branch,
    EpochChoice,
    EpochScenario,
    InitialConditionScenario,
    RateUnitConvention,
    SolverConfig,
    TiltForm,
    WavenumberConvention,
    barotropic_matrix,
    barotropic_rhs,
    comoving_rhs,
    meszaros_rhs,
    resolve_wavenumber,
    solve_comoving,
    solve_barotropic,
    tilt_state_transform,
    tilt_state_transform_dot,
    transform_barotropic_state,
)


G = 1.0
TIMESCAPE_H = 0.7323
LCDM_H = 0.674
K = 2.0 * np.pi
REFERENCE_DOP853 = SolverConfig(
    method="DOP853", rtol=2e-13, atol=2e-15, max_step=np.inf, first_step=None
)
EFFECTIVE_SECOND_ORDER_RESIDUAL_GATE = 2e-7


@pytest.fixture(scope="module")
def params():
    return TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0)


def scenario(
    *,
    branch: D3Branch,
    tilt_form: TiltForm,
    rate: RateUnitConvention = RateUnitConvention.UPSTREAM_UNCONVERTED,
    epoch: EpochChoice = EpochChoice.UPSTREAM_0P218_GYR,
    k_convention: WavenumberConvention = WavenumberConvention.UPSTREAM_TIMESCAPE_K,
    k: float = K,
) -> BarotropicScenario:
    return BarotropicScenario(
        k=k,
        branch=branch,
        tilt_form=tilt_form,
        rate_convention=rate,
        epoch_choice=epoch,
        wavenumber_convention=k_convention,
        timescape_h=TIMESCAPE_H,
        lcdm_h=LCDM_H,
    )


@pytest.mark.parametrize("branch", list(D3Branch))
@pytest.mark.parametrize("tilt_form", list(TiltForm))
def test_every_barotropic_matrix_entry(params, branch, tilt_form):
    """Map every entry of [GM] Eqs. (4.14)-(4.17), including both A33 branches."""
    t = 0.41 * params.t0
    theta = float(bg.Theta(t, params))
    rho_d = float(bg.rho_d(t, params, G))
    rho_eff = float(bg.rho_eff(t, params, G))
    w_eff = float(bg.w_eff(t, params))
    cs2_eff = float(bg.cs2_eff(t, params))
    scale_factor = float(bg.a_D(t, params))
    branch_sign = 1.0 if branch is D3Branch.PRINTED_4_15 else -1.0
    matrix = barotropic_matrix(
        t,
        params=params,
        G=G,
        k=K,
        branch=branch,
        tilt_form=tilt_form,
        wavenumber_convention=WavenumberConvention.UPSTREAM_TIMESCAPE_K,
        timescape_h=TIMESCAPE_H,
        lcdm_h=LCDM_H,
    )
    expected = np.zeros((4, 4))
    # [GM] Eq. (4.14).
    expected[0, 1] = -1.0
    # [GM] Eq. (4.16).
    expected[1, 0] = -4.0 * np.pi * G * rho_d
    expected[1, 1] = -(2.0 / 3.0) * theta
    expected[1, 2] = -4.0 * np.pi * G * rho_eff * (1.0 + 3.0 * cs2_eff)
    # [GM] Eq. (4.15), using the explicitly selected coefficient provenance.
    expected[2, 1] = -(1.0 + w_eff)
    expected[2, 2] = (w_eff + branch_sign * cs2_eff) * theta
    if tilt_form is TiltForm.RESCALED_VTILDE:
        # [GM] Eqs. (4.15), (4.17).
        expected[2, 3] = K**2 / scale_factor
        expected[3, 2] = -cs2_eff / scale_factor
        expected[3, 3] = (theta / 3.0) * (3.0 * w_eff - 1.0)
    else:
        # [GM] Eq. (4.15) in V and Eq. (4.8) with closure (4.13).
        expected[2, 3] = K**2 * (1.0 + w_eff) / scale_factor
        expected[3, 2] = -cs2_eff / (scale_factor * (1.0 + w_eff))
        expected[3, 3] = (theta / 3.0) * (3.0 * cs2_eff - 1.0)
    np.testing.assert_allclose(matrix, expected, rtol=2e-14, atol=0.0)


@pytest.mark.parametrize("branch", list(D3Branch))
@pytest.mark.parametrize("tilt_form", list(TiltForm))
def test_a34_a43_recombines_pressure_laplacian(params, branch, tilt_form):
    """Both [GM] tilt forms give A34*A43=-cs2*k^2/a_D^2."""
    t = 0.63 * params.t0
    matrix = barotropic_matrix(
        t,
        params=params,
        G=G,
        k=K,
        branch=branch,
        tilt_form=tilt_form,
        wavenumber_convention=WavenumberConvention.UPSTREAM_TIMESCAPE_K,
        timescape_h=TIMESCAPE_H,
        lcdm_h=LCDM_H,
    )
    expected = -float(bg.cs2_eff(t, params)) * K**2 / float(bg.a_D(t, params)) ** 2
    assert matrix[2, 3] * matrix[3, 2] == pytest.approx(expected, rel=2e-14)


@pytest.mark.parametrize("branch", list(D3Branch))
@pytest.mark.parametrize("tilt_form", list(TiltForm))
def test_long_wavelength_limit_removes_only_k2_source(params, branch, tilt_form):
    """The [GM] Laplacian source A34 vanishes as k^2 when k approaches zero."""
    t = 0.44 * params.t0
    common = dict(
        params=params,
        G=G,
        branch=branch,
        tilt_form=tilt_form,
        wavenumber_convention=WavenumberConvention.UPSTREAM_TIMESCAPE_K,
        timescape_h=TIMESCAPE_H,
        lcdm_h=LCDM_H,
    )
    matrix_k1 = barotropic_matrix(t, k=1e-5, **common)
    matrix_k2 = barotropic_matrix(t, k=2e-5, **common)
    assert matrix_k2[2, 3] == pytest.approx(4.0 * matrix_k1[2, 3], rel=2e-14)
    matrix_k1[2, 3] = 0.0
    matrix_k2[2, 3] = 0.0
    np.testing.assert_array_equal(matrix_k1, matrix_k2)


def test_paper_wavenumber_conversion_matches_present_physical_mode(params):
    """Implement footnote 8 and the [GM] Figure-3 LCDM Hubble-unit caption."""
    resolved = resolve_wavenumber(
        K,
        params=params,
        convention=WavenumberConvention.PAPER_LCDM_HUBBLE_K,
        timescape_h=TIMESCAPE_H,
        lcdm_h=LCDM_H,
    )
    expected_factor = params.aD0 * LCDM_H / TIMESCAPE_H
    assert resolved.matrix_k == pytest.approx(K * expected_factor, rel=2e-15)
    upstream_wavelength_in_lcdm_hubble_lengths = params.aD0 * LCDM_H / TIMESCAPE_H
    assert upstream_wavelength_in_lcdm_hubble_lengths == pytest.approx(
        1.2596, abs=1e-4
    )


@pytest.mark.parametrize("branch", list(D3Branch))
@pytest.mark.parametrize("k_convention", list(WavenumberConvention))
def test_exact_corrected_tilt_matrix_transformation(params, branch, k_convention):
    """Prove the V-to-Vtilde transform using [GM] Eq. (3.17)'s w-dot identity."""
    t = 0.37 * params.t0
    common = dict(
        params=params,
        G=G,
        k=K,
        branch=branch,
        wavenumber_convention=k_convention,
        timescape_h=TIMESCAPE_H,
        lcdm_h=LCDM_H,
    )
    matrix_v = barotropic_matrix(t, tilt_form=TiltForm.UNRESCALED_V, **common)
    matrix_tilde = barotropic_matrix(t, tilt_form=TiltForm.RESCALED_VTILDE, **common)
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
    transformed_matrix = (
        transform_dot @ np.linalg.inv(transform)
        + transform @ matrix_v @ np.linalg.inv(transform)
    )
    np.testing.assert_allclose(matrix_tilde, transformed_matrix, rtol=2e-14, atol=2e-14)


def test_barotropic_state_transform_roundtrip(params):
    """State normalisation follows [GM] Vtilde=(1+w_eff)V exactly."""
    t = 0.52 * params.t0
    state_v = np.array([0.02, -0.03, 0.004, 0.15])
    state_tilde = transform_barotropic_state(
        t,
        state_v,
        params=params,
        from_tilt_form=TiltForm.UNRESCALED_V,
        to_tilt_form=TiltForm.RESCALED_VTILDE,
    )
    assert state_tilde[3] == pytest.approx(
        (1.0 + float(bg.w_eff(t, params))) * state_v[3], rel=2e-15
    )
    roundtrip = transform_barotropic_state(
        t,
        state_tilde,
        params=params,
        from_tilt_form=TiltForm.RESCALED_VTILDE,
        to_tilt_form=TiltForm.UNRESCALED_V,
    )
    np.testing.assert_array_equal(roundtrip, state_v)


@pytest.mark.parametrize("tilt_form", list(TiltForm))
def test_barotropic_rhs_time_unit_scaling(params, tilt_form):
    """[GM] Eqs. (4.14)-(4.17) transform consistently under time units."""
    unit_scale = 3.7
    scaled_params = TrackerParams(fv0=params.fv0, HD0=unit_scale * params.HD0)
    t = 0.48 * params.t0
    state = np.array([0.02, -0.03, 0.004, 0.15])
    state_scale = np.array([1.0, unit_scale, 1.0, 1.0 / unit_scale])
    common = dict(
        G=G,
        branch=D3Branch.PRINTED_4_15,
        tilt_form=tilt_form,
        wavenumber_convention=WavenumberConvention.UPSTREAM_TIMESCAPE_K,
        timescape_h=TIMESCAPE_H,
        lcdm_h=LCDM_H,
    )
    rhs = barotropic_rhs(t, state, params=params, k=K, **common)
    rhs_scaled = barotropic_rhs(
        t / unit_scale,
        state * state_scale,
        params=scaled_params,
        k=unit_scale * K,
        **common,
    )
    np.testing.assert_allclose(
        rhs_scaled,
        unit_scale * state_scale * rhs,
        rtol=2e-13,
        atol=2e-13,
    )


def test_barotropic_matrix_is_independent_of_density_G_units(params):
    kwargs = dict(
        params=params,
        k=K,
        branch=D3Branch.DERIVED_4_10,
        tilt_form=TiltForm.RESCALED_VTILDE,
        wavenumber_convention=WavenumberConvention.UPSTREAM_TIMESCAPE_K,
        timescape_h=TIMESCAPE_H,
        lcdm_h=LCDM_H,
    )
    np.testing.assert_allclose(
        barotropic_matrix(0.4 * params.t0, G=1.0, **kwargs),
        barotropic_matrix(0.4 * params.t0, G=7.3, **kwargs),
        rtol=2e-14,
        atol=0.0,
    )


def test_all_barotropic_choices_are_mandatory_without_defaults():
    matrix_signature = inspect.signature(barotropic_matrix)
    for name in (
        "branch",
        "tilt_form",
        "wavenumber_convention",
        "timescape_h",
        "lcdm_h",
    ):
        assert matrix_signature.parameters[name].default is inspect.Parameter.empty
    solver_signature = inspect.signature(solve_barotropic)
    assert solver_signature.parameters["scenario"].default is inspect.Parameter.empty
    for field in fields(BarotropicScenario):
        assert field.default is MISSING
        assert field.default_factory is MISSING


@pytest.mark.parametrize(
    "field_name,bad_value",
    [
        ("branch", "printed_4_15"),
        ("tilt_form", "unrescaled_V"),
        ("rate_convention", "upstream_unconverted"),
        ("epoch_choice", "upstream_0p218_gyr"),
        ("wavenumber_convention", "upstream_timescape_k"),
    ],
)
def test_scenario_rejects_implicit_string_choices(field_name, bad_value):
    values = dict(
        k=K,
        branch=D3Branch.PRINTED_4_15,
        tilt_form=TiltForm.UNRESCALED_V,
        rate_convention=RateUnitConvention.UPSTREAM_UNCONVERTED,
        epoch_choice=EpochChoice.UPSTREAM_0P218_GYR,
        wavenumber_convention=WavenumberConvention.UPSTREAM_TIMESCAPE_K,
        timescape_h=TIMESCAPE_H,
        lcdm_h=LCDM_H,
    )
    values[field_name] = bad_value
    with pytest.raises(ValueError):
        BarotropicScenario(**values)


def test_scenario_identifier_contains_every_choice():
    selected = scenario(
        branch=D3Branch.DERIVED_4_10,
        tilt_form=TiltForm.RESCALED_VTILDE,
        rate=RateUnitConvention.LCDM_TO_TIMESCAPE_CONVERTED,
        epoch=EpochChoice.DRESSED_Z20,
        k_convention=WavenumberConvention.PAPER_LCDM_HUBBLE_K,
        k=5.0 * np.pi,
    )
    identifier = selected.identifier
    for value in (
        selected.branch.value,
        selected.tilt_form.value,
        selected.rate_convention.value,
        selected.epoch_choice.value,
        selected.wavenumber_convention.value,
    ):
        assert value in identifier


def test_solve_barotropic_requires_epoch_consistent_grid(params):
    selected = scenario(
        branch=D3Branch.PRINTED_4_15,
        tilt_form=TiltForm.UNRESCALED_V,
    )
    with pytest.raises(ValueError, match="explicit epoch"):
        solve_barotropic(
            params=params,
            scenario=selected,
            recipe=PLANCK_2018_QPLUS_RECIPE,
            time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
            epoch_root=PHASE1C_EPOCH_ROOT,
            t_eval=np.linspace(0.1 * params.t0, params.t0, 20),
            config=REFERENCE_DOP853,
            G=G,
        )


def _five_point_first(values: np.ndarray, spacing: float) -> np.ndarray:
    """Fourth-order centred derivative, independent of the ODE RHS."""
    return (
        values[:, :-4]
        - 8.0 * values[:, 1:-3]
        + 8.0 * values[:, 3:-1]
        - values[:, 4:]
    ) / (12.0 * spacing)


def _five_point_second(values: np.ndarray, spacing: float) -> np.ndarray:
    """Fourth-order centred second derivative, independent of the ODE RHS."""
    return (
        -values[4:]
        + 16.0 * values[3:-1]
        - 30.0 * values[2:-2]
        + 16.0 * values[1:-3]
        - values[:-4]
    ) / (12.0 * spacing**2)


def _trajectory_residual_maxima(params, branch, tilt_form):
    """Evaluate [GM] (4.14)-(4.18) from finite-differenced trajectories."""
    selected = scenario(
        branch=branch,
        tilt_form=tilt_form,
        k=10.0 * np.pi,
    )
    epoch = EpochScenario(
        choice=selected.epoch_choice,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        root=PHASE1C_EPOCH_ROOT,
    ).resolve(params)
    times = np.linspace(epoch.time, params.t0, 8001)
    solution = solve_barotropic(
        params=params,
        scenario=selected,
        recipe=PLANCK_2018_QPLUS_RECIPE,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        epoch_root=PHASE1C_EPOCH_ROOT,
        t_eval=times,
        config=REFERENCE_DOP853,
        G=G,
    )
    spacing = float(times[1] - times[0])
    interior = slice(2, -2)
    t = times[interior]
    y = solution.y[:, interior]
    y_dot = _five_point_first(solution.y, spacing)
    theta = bg.Theta(t, params)
    rho_d = bg.rho_d(t, params, G)
    rho_eff = bg.rho_eff(t, params, G)
    w_eff = bg.w_eff(t, params)
    cs2_eff = bg.cs2_eff(t, params)
    scale_factor = bg.a_D(t, params)
    branch_sign = 1.0 if branch is D3Branch.PRINTED_4_15 else -1.0
    k2_over_a = selected.k**2 / scale_factor

    # Each list contains the terms on the RHS of the corresponding equation.
    # This is deliberately independent of barotropic_matrix/barotropic_rhs.
    rhs_terms = [
        [-y[1]],  # [GM] Eq. (4.14)
        [  # [GM] Eq. (4.16)
            -4.0 * np.pi * G * rho_d * y[0],
            -(2.0 / 3.0) * theta * y[1],
            -4.0 * np.pi * G * rho_eff * (1.0 + 3.0 * cs2_eff) * y[2],
        ],
        [  # [GM] Eq. (4.15), with the selected unresolved branch.
            -(1.0 + w_eff) * y[1],
            (w_eff + branch_sign * cs2_eff) * theta * y[2],
            (
                k2_over_a * y[3]
                if tilt_form is TiltForm.RESCALED_VTILDE
                else k2_over_a * (1.0 + w_eff) * y[3]
            ),
        ],
        [  # [GM] Eq. (4.17), or Eq. (4.8)+(4.13) in unrescaled V.
            (
                -cs2_eff * y[2] / scale_factor
                if tilt_form is TiltForm.RESCALED_VTILDE
                else -cs2_eff * y[2] / (scale_factor * (1.0 + w_eff))
            ),
            (
                (theta / 3.0) * (3.0 * w_eff - 1.0) * y[3]
                if tilt_form is TiltForm.RESCALED_VTILDE
                else (theta / 3.0) * (3.0 * cs2_eff - 1.0) * y[3]
            ),
        ],
    ]
    first_order_maxima = []
    for index, terms in enumerate(rhs_terms):
        rhs = np.sum(terms, axis=0)
        # The scale is the absolute derivative plus the absolute magnitudes of
        # every term entering that equation; it remains valid through zeros.
        scale = np.abs(y_dot[index]) + np.sum(np.abs(terms), axis=0)
        scaled = np.abs(y_dot[index] - rhs) / np.maximum(scale, 1e-300)
        first_order_maxima.append(float(np.max(scaled)))

    # [GM] Eq. (4.18), obtained from (4.14)+(4.16), evaluated with an
    # independently finite-differenced second derivative.
    delta_d_ddot = _five_point_second(solution.y[0], spacing)
    second_order_terms = np.vstack(
        [
            delta_d_ddot,
            (2.0 / 3.0) * theta * y_dot[0],
            -4.0 * np.pi * G * rho_d * y[0],
            -4.0 * np.pi * G * rho_eff * (1.0 + 3.0 * cs2_eff) * y[2],
        ]
    )
    second_order_scaled = np.abs(np.sum(second_order_terms, axis=0)) / np.maximum(
        np.sum(np.abs(second_order_terms), axis=0), 1e-300
    )
    return np.asarray(first_order_maxima), float(np.max(second_order_scaled))


def _effective_second_order_residual_maximum(
    params,
    *,
    trajectory_branch: D3Branch,
    equation_branch: D3Branch,
    tilt_form: TiltForm,
    k: float,
    n_points: int,
) -> float:
    """Finite-difference the effective-fluid second-order equation.

    For ``PRINTED_4_15`` this is [GM] Eq. (4.19), with Lambda=0.  For
    ``DERIVED_4_10`` it is the distinct analogue derived by differentiating
    [GM] Eqs. (4.10)+(4.13), then eliminating Z and Vtilde with Eqs.
    (4.14), (4.16), and (4.17).  It must not be identified as printed
    Eq. (4.19).

    Both trajectory derivatives and cs2_dot are estimated on a uniform grid
    by five-point, fourth-order centred finite differences.  No RHS, A@y,
    matrix derivative, or dense-output derivative is used.  The scale at each
    sample is the sum of the absolute magnitudes of every additive equation
    term below, with a 1e-300 denominator floor.
    """
    selected = scenario(
        branch=trajectory_branch,
        tilt_form=tilt_form,
        k=k,
    )
    epoch = EpochScenario(
        choice=selected.epoch_choice,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        root=PHASE1C_EPOCH_ROOT,
    ).resolve(params)
    times = np.linspace(epoch.time, params.t0, n_points)
    solution = solve_barotropic(
        params=params,
        scenario=selected,
        recipe=PLANCK_2018_QPLUS_RECIPE,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        epoch_root=PHASE1C_EPOCH_ROOT,
        t_eval=times,
        config=REFERENCE_DOP853,
        G=G,
    )
    spacing = float(times[1] - times[0])
    interior = slice(2, -2)
    t = times[interior]
    y = solution.y[:, interior]
    y_dot = _five_point_first(solution.y, spacing)
    delta_eff_ddot = _five_point_second(solution.y[2], spacing)
    cs2_all = np.asarray(bg.cs2_eff(times, params), dtype=np.float64)[None, :]
    cs2_dot = _five_point_first(cs2_all, spacing)[0]

    theta = bg.Theta(t, params)
    rho_d = bg.rho_d(t, params, G)
    rho_eff = bg.rho_eff(t, params, G)
    w_eff = bg.w_eff(t, params)
    cs2_eff = bg.cs2_eff(t, params)
    scale_factor = bg.a_D(t, params)
    delta_d = y[0]
    delta_eff = y[2]
    delta_d_dot = y_dot[0]
    delta_eff_dot = y_dot[2]

    if equation_branch is D3Branch.PRINTED_4_15:
        # [GM] Eq. (4.19), Lambda=0, split into additive terms so the
        # cancellation-aware scale does not hide coefficient cancellation.
        terms = np.vstack(
            [
                delta_eff_ddot,
                (2.0 / 3.0 - 2.0 * w_eff - cs2_eff)
                * theta
                * delta_eff_dot,
                (2.0 / 3.0)
                * theta**2
                * (-2.0 * w_eff + cs2_eff * (1.0 + 3.0 * w_eff))
                * delta_eff,
                -theta * cs2_dot * delta_eff,
                4.0
                * np.pi
                * G
                * rho_d
                * (w_eff + cs2_eff)
                * delta_eff,
                -4.0
                * np.pi
                * G
                * rho_eff
                * (1.0 - 3.0 * w_eff**2 + 2.0 * cs2_eff)
                * delta_eff,
                cs2_eff * k**2 / scale_factor**2 * delta_eff,
                -4.0 * np.pi * G * rho_d * (1.0 + w_eff) * delta_d,
                cs2_eff * (1.0 + w_eff) * theta * delta_d_dot,
            ]
        )
    elif equation_branch is D3Branch.DERIVED_4_10:
        # Derived only from [GM] Eqs. (4.10), (4.13), (4.14), (4.16),
        # and (4.17), with Lambda=0.  Unlike printed Eq. (4.19), its damping
        # contains +cs2 and its Delta_eff coefficient follows the w-cs2
        # first-order branch.
        terms = np.vstack(
            [
                delta_eff_ddot,
                (2.0 / 3.0 - 2.0 * w_eff + cs2_eff)
                * theta
                * delta_eff_dot,
                (4.0 / 3.0)
                * theta**2
                * (cs2_eff - w_eff)
                * delta_eff,
                theta * cs2_dot * delta_eff,
                4.0
                * np.pi
                * G
                * rho_d
                * (w_eff - cs2_eff)
                * delta_eff,
                4.0
                * np.pi
                * G
                * rho_eff
                * (
                    3.0 * w_eff**2
                    - 1.0
                    - 4.0 * cs2_eff
                    - 6.0 * w_eff * cs2_eff
                )
                * delta_eff,
                cs2_eff * k**2 / scale_factor**2 * delta_eff,
                -4.0 * np.pi * G * rho_d * (1.0 + w_eff) * delta_d,
                cs2_eff * (1.0 + w_eff) * theta * delta_d_dot,
            ]
        )
    else:  # pragma: no cover - enum exhaustiveness guard
        raise ValueError(f"unsupported equation branch {equation_branch!r}")

    scale = np.maximum(np.sum(np.abs(terms), axis=0), 1e-300)
    return float(np.max(np.abs(np.sum(terms, axis=0)) / scale))


@pytest.mark.parametrize("branch", list(D3Branch))
@pytest.mark.parametrize("tilt_form", list(TiltForm))
def test_numerical_trajectory_satisfies_barotropic_equations(
    params, branch, tilt_form
):
    """Numerically test [GM] Eqs. (4.14)-(4.18) without RHS derivatives.

    A uniform 8,001-point grid and five-point, fourth-order centred stencils
    are used.  At the deliberately difficult k=10*pi mode, refinement from
    4,001 -> 8,001 -> 16,001 points reduced the worst first-order residual
    2.752e-5 -> 4.165e-6 -> 5.740e-7 (ratios 6.61 and 7.26).  The Eq. (4.18)
    residual changed 2.068e-8 -> 3.447e-9 -> 5.192e-9, showing round-off onset
    at the last refinement.  Gates of 1e-5 and 1e-8 therefore bracket the
    measured 8,001-point maxima while still failing the coarser grid.
    """
    first_order, second_order = _trajectory_residual_maxima(
        params, branch, tilt_form
    )
    assert float(np.max(first_order)) < 1e-5
    assert second_order < 1e-8


@pytest.mark.parametrize("branch", list(D3Branch))
@pytest.mark.parametrize("tilt_form", list(TiltForm))
@pytest.mark.parametrize("k", [2.0 * np.pi, 5.0 * np.pi, 10.0 * np.pi])
def test_effective_second_order_equation_from_numerical_trajectory(
    params, branch, tilt_form, k
):
    """Validate printed [GM] (4.19) or its derived-branch analogue.

    The 8,001-point grid provides 7,997 interior samples.  The gate is based
    on the documented 4,001/8,001/16,001-point refinement study reported in
    ``reports/phase1c_b2_barotropic_validation.md``; it is not a relaxed
    version of the pre-existing first-order or Eq. (4.18) gates.
    """
    residual = _effective_second_order_residual_maximum(
        params,
        trajectory_branch=branch,
        equation_branch=branch,
        tilt_form=tilt_form,
        k=k,
        n_points=8001,
    )
    assert residual < EFFECTIVE_SECOND_ORDER_RESIDUAL_GATE


@pytest.mark.parametrize("trajectory_branch", list(D3Branch))
def test_effective_second_order_residual_rejects_wrong_d3_equation(
    params, trajectory_branch
):
    """Ensure the second-order diagnostic distinguishes the two D3 chains."""
    equation_branch = (
        D3Branch.DERIVED_4_10
        if trajectory_branch is D3Branch.PRINTED_4_15
        else D3Branch.PRINTED_4_15
    )
    matching = _effective_second_order_residual_maximum(
        params,
        trajectory_branch=trajectory_branch,
        equation_branch=trajectory_branch,
        tilt_form=TiltForm.RESCALED_VTILDE,
        k=2.0 * np.pi,
        n_points=8001,
    )
    wrong = _effective_second_order_residual_maximum(
        params,
        trajectory_branch=trajectory_branch,
        equation_branch=equation_branch,
        tilt_form=TiltForm.RESCALED_VTILDE,
        k=2.0 * np.pi,
        n_points=8001,
    )
    assert matching < EFFECTIVE_SECOND_ORDER_RESIDUAL_GATE
    assert wrong > 1e-3
    assert wrong > 1e3 * matching


@pytest.mark.parametrize("branch", list(D3Branch))
def test_corrected_tilt_trajectories_are_numerically_equivalent(params, branch):
    """Confirm [GM] Vtilde=(1+w)V along corrected-cs2 trajectories."""
    epoch = EpochScenario(
        choice=EpochChoice.UPSTREAM_0P218_GYR,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        root=PHASE1C_EPOCH_ROOT,
    ).resolve(params)
    times = np.linspace(epoch.time, params.t0, 1001)
    solutions = {}
    for tilt_form in TiltForm:
        solutions[tilt_form] = solve_barotropic(
            params=params,
            scenario=scenario(
                branch=branch, tilt_form=tilt_form, k=10.0 * np.pi
            ),
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
    for index in range(4):
        scale = max(float(np.max(np.abs(direct[index]))), 1e-300)
        assert float(np.max(np.abs(direct[index] - transformed[index]))) / scale < 1e-8


def test_initial_and_numerical_early_time_continuity_with_clean_systems(params):
    """Check physically applicable continuity with [GM] Eqs. (4.21)-(4.27)."""
    initial = InitialConditionScenario(
        recipe=PLANCK_2018_QPLUS_RECIPE,
        rate_units=RateUnitConvention.UPSTREAM_UNCONVERTED,
        timescape_h=TIMESCAPE_H,
    ).resolve(params)
    epoch = EpochScenario(
        choice=EpochChoice.UPSTREAM_0P218_GYR,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        root=PHASE1C_EPOCH_ROOT,
    ).resolve(params)
    selected = scenario(
        branch=D3Branch.PRINTED_4_15,
        tilt_form=TiltForm.UNRESCALED_V,
        k=10.0 * np.pi,
    )
    barotropic_initial = np.array(
        [initial.delta_d, initial.expansion_gradient, 0.0, 0.0]
    )
    barotropic_derivative = barotropic_rhs(
        epoch.time,
        barotropic_initial,
        params=params,
        G=G,
        k=selected.k,
        branch=selected.branch,
        tilt_form=selected.tilt_form,
        wavenumber_convention=selected.wavenumber_convention,
        timescape_h=selected.timescape_h,
        lcdm_h=selected.lcdm_h,
    )
    comoving_derivative = comoving_rhs(
        epoch.time, initial.comoving_vector(), params=params, G=G
    )
    meszaros_derivative = meszaros_rhs(
        epoch.time, initial.meszaros_vector(), params=params, G=G
    )
    np.testing.assert_allclose(
        barotropic_derivative[:3], comoving_derivative, rtol=2e-14, atol=2e-14
    )
    assert barotropic_derivative[0] == pytest.approx(meszaros_derivative[0])
    assert barotropic_derivative[1] == pytest.approx(-meszaros_derivative[1])

    # Over shrinking intervals, the barotropic and comoving states converge
    # continuously from their identical initial state/RHS.  The fine-window
    # gate is measured with a window half the coarse 1e-4 full-span window.
    errors = []
    for fraction in (1e-4, 5e-5):
        times = np.array(
            [epoch.time, epoch.time + fraction * (params.t0 - epoch.time)]
        )
        barotropic = solve_barotropic(
            params=params,
            scenario=selected,
            recipe=PLANCK_2018_QPLUS_RECIPE,
            time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
            epoch_root=PHASE1C_EPOCH_ROOT,
            t_eval=times,
            config=REFERENCE_DOP853,
            G=G,
        )
        comoving = solve_comoving(
            params=params,
            initial_conditions=initial,
            t_eval=times,
            config=REFERENCE_DOP853,
            G=G,
        )
        scale = max(abs(initial.delta_d), abs(initial.expansion_gradient))
        errors.append(
            float(np.max(np.abs(barotropic.y[:3, -1] - comoving.y[:, -1])))
            / scale
        )
    assert errors[1] < errors[0]
    assert errors[1] < 3e-7
