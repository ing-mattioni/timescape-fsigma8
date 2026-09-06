"""Equation-level and limiting-case validation of the clean B1 systems.

Algebraic identities use rtol=1e-12.  The numerical-trajectory residual uses
five-point, fourth-order finite differences and a 1.5e-7 scaled-residual gate
calibrated by explicit grid refinement.  Other solver comparisons and EdS
limits state their tolerances individually.
"""

# A06: absolute budgets use rtol=0; relative budgets use atol=0.
# Previously implicit algebraic comparisons use rtol=2e-12, atol=1e-14
# in the fixture units (roundoff allowance); explicit convergence budgets remain.

import numpy as np
import pytest

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations import (
    PHASE1C_EPOCH_ROOT,
    PLANCK_2018_QPLUS_RECIPE,
    TIGHT_DOP853,
    UPSTREAM_NOTEBOOK_TIME_UNIT,
    EpochChoice,
    EpochScenario,
    InitialConditionScenario,
    PerturbationInitialConditions,
    RateUnitConvention,
    SolverConfig,
    comoving_matrix,
    comoving_rhs,
    comoving_second_derivative,
    comoving_second_order_residuals,
    meszaros_rhs,
    solve_comoving,
    solve_meszaros,
)


RTOL_EXACT = 1e-12
G = 1.0
TRAJECTORY_RESIDUAL_GRID_SIZE = 4001
TRAJECTORY_RESIDUAL_GATE = 1.5e-7
TRAJECTORY_RESIDUAL_DOP853 = SolverConfig(
    method="DOP853",
    rtol=2e-13,
    atol=2e-15,
    max_step=np.inf,
    first_step=None,
)


@pytest.fixture(scope="module")
def perturbation_setup():
    params = TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0)
    epoch = EpochScenario(
        choice=EpochChoice.UPSTREAM_0P218_GYR,
        time_unit=UPSTREAM_NOTEBOOK_TIME_UNIT,
        root=PHASE1C_EPOCH_ROOT,
    ).resolve(params)
    initial = InitialConditionScenario(
        recipe=PLANCK_2018_QPLUS_RECIPE,
        rate_units=RateUnitConvention.UPSTREAM_UNCONVERTED,
        timescape_h=0.7323,
    ).resolve(params)
    return params, epoch, initial


def test_meszaros_rhs_is_eq_4_27(perturbation_setup):
    params, epoch, _ = perturbation_setup
    state = np.array([0.012, 0.031])
    rhs = meszaros_rhs(epoch.time, state, params=params, G=G)
    theta = float(bg.Theta(epoch.time, params))
    rho_d = float(bg.rho_d(epoch.time, params, G))
    expected_ddot = 4.0 * np.pi * G * rho_d * state[0] - (2.0 / 3.0) * theta * state[1]
    np.testing.assert_allclose(rhs, [state[1], expected_ddot], rtol=RTOL_EXACT, atol=0.0)


def test_comoving_matrix_is_eqs_4_21_to_4_23(perturbation_setup):
    params, epoch, _ = perturbation_setup
    t = epoch.time
    theta = float(bg.Theta(t, params))
    rho_d = float(bg.rho_d(t, params, G))
    rho_eff = float(bg.rho_eff(t, params, G))
    w_eff = float(bg.w_eff(t, params))
    expected = np.array(
        [
            [0.0, -1.0, 0.0],
            [-4.0 * np.pi * G * rho_d, -(2.0 / 3.0) * theta,
             -4.0 * np.pi * G * rho_eff],
            [0.0, -(1.0 + w_eff), w_eff * theta],
        ]
    )
    np.testing.assert_allclose(comoving_matrix(t, params=params, G=G), expected, rtol=RTOL_EXACT, atol=0.0)


def test_comoving_matrix_is_independent_of_G_units(perturbation_setup):
    """The products G*rho in Eqs. (4.23) are invariant under density units."""
    params, epoch, _ = perturbation_setup
    matrix_g1 = comoving_matrix(epoch.time, params=params, G=1.0)
    matrix_g7 = comoving_matrix(epoch.time, params=params, G=7.3)
    np.testing.assert_allclose(matrix_g1, matrix_g7, rtol=RTOL_EXACT, atol=0.0)


def test_rhs_dimensional_rescaling(perturbation_setup):
    """Changing time units preserves dimensionless states and scales rates."""
    params, epoch, initial = perturbation_setup
    scale = 3.7
    params_scaled = TrackerParams(fv0=params.fv0, HD0=scale * params.HD0)
    t = 0.4 * params.t0
    t_scaled = t / scale

    comoving_state = initial.comoving_vector()
    comoving_scaled_state = comoving_state * np.array([1.0, scale, 1.0])
    rhs = comoving_rhs(t, comoving_state, params=params, G=G)
    rhs_scaled = comoving_rhs(
        t_scaled, comoving_scaled_state, params=params_scaled, G=G
    )
    np.testing.assert_allclose(
        rhs_scaled, rhs * np.array([scale, scale**2, scale]), rtol=RTOL_EXACT, atol=0.0
    )

    meszaros_state = initial.meszaros_vector()
    meszaros_scaled_state = meszaros_state * np.array([1.0, scale])
    mz_rhs = meszaros_rhs(t, meszaros_state, params=params, G=G)
    mz_rhs_scaled = meszaros_rhs(
        t_scaled, meszaros_scaled_state, params=params_scaled, G=G
    )
    np.testing.assert_allclose(
        mz_rhs_scaled, mz_rhs * np.array([scale, scale**2]), rtol=RTOL_EXACT, atol=0.0
    )


def test_z_is_minus_delta_d_dot_in_rhs(perturbation_setup):
    params, epoch, initial = perturbation_setup
    state = initial.comoving_vector()
    rhs = comoving_rhs(epoch.time, state, params=params, G=G)
    assert rhs[0] == -state[1]


@pytest.mark.parametrize("fraction", [0.02, 0.1, 0.5, 1.0])
def test_second_order_residuals_4_24_to_4_26(perturbation_setup, fraction):
    params, epoch, initial = perturbation_setup
    t = epoch.time + fraction * (params.t0 - epoch.time)
    state = initial.comoving_vector() * np.array([1.0 + fraction, 0.7, 0.3])
    state_dot = comoving_rhs(t, state, params=params, G=G)
    state_ddot = comoving_second_derivative(t, state, params=params, G=G)
    residuals = comoving_second_order_residuals(
        t, state, state_dot, state_ddot, params=params, G=G
    )
    scale = max(np.max(np.abs(state_ddot)), 1.0)
    assert abs(residuals.eq_4_24) < RTOL_EXACT * scale
    assert abs(residuals.eq_4_25) < RTOL_EXACT * scale
    assert abs(residuals.eq_4_26) < RTOL_EXACT * scale


def _five_point_time_derivatives(values, step):
    """Return O(step^4) centred first and second finite differences.

    For each interior index ``i=2,...,N-3``, the documented stencils are

    ``f' = (f[i-2] - 8 f[i-1] + 8 f[i+1] - f[i+2]) / (12 step)``

    and

    ``f'' = (-f[i-2] + 16 f[i-1] - 30 f[i] + 16 f[i+1]
             - f[i+2]) / (12 step^2)``.

    Both derivatives therefore come only from the sampled numerical
    trajectory, with no use of the ODE RHS or an analytic matrix derivative.
    """
    first = (
        values[:, :-4]
        - 8.0 * values[:, 1:-3]
        + 8.0 * values[:, 3:-1]
        - values[:, 4:]
    ) / (12.0 * step)
    second = (
        -values[:, :-4]
        + 16.0 * values[:, 1:-3]
        - 30.0 * values[:, 2:-2]
        + 16.0 * values[:, 3:-1]
        - values[:, 4:]
    ) / (12.0 * step**2)
    return first, second


def test_numerical_trajectory_residuals_4_24_to_4_26(perturbation_setup):
    """Finite-difference a numerical trajectory in [GM] Eqs. (4.24)-(4.26).

    A 1001/2001/4001-point refinement gave worst scaled residuals
    1.5141e-5, 1.2409e-6, and 8.965e-8.  The successive factors 12.2 and
    13.8 approach the factor 16 expected for the fourth-order stencil before
    differentiation roundoff becomes visible.  The 4001-point gate 1.5e-7
    is above both measured Python-environment results but below the
    2001-point residual, so it detects loss of the demonstrated convergence.
    """
    params, epoch, initial = perturbation_setup
    t_eval = np.linspace(epoch.time, params.t0, TRAJECTORY_RESIDUAL_GRID_SIZE)
    solution = solve_comoving(
        params=params,
        initial_conditions=initial,
        t_eval=t_eval,
        config=TRAJECTORY_RESIDUAL_DOP853,
        G=G,
    )
    step = t_eval[1] - t_eval[0]
    state = solution.y[:, 2:-2]
    state_dot, state_ddot = _five_point_time_derivatives(solution.y, step)
    interior_times = t_eval[2:-2]
    assert interior_times.size >= 200

    theta = bg.Theta(interior_times, params)
    rho_d = bg.rho_d(interior_times, params, G)
    rho_eff = bg.rho_eff(interior_times, params, G)
    w_eff = bg.w_eff(interior_times, params)
    cs2_eff = bg.cs2_eff(interior_times, params)
    four_pi_G = 4.0 * np.pi * G

    # Terms of the Lambda=0 form of [GM] Eq. (4.24).
    terms_4_24 = np.stack(
        (
            state_ddot[0],
            (2.0 / 3.0) * theta * state_dot[0],
            -four_pi_G * rho_d * state[0],
            -four_pi_G * rho_eff * state[2],
        )
    )

    coefficient_4_25 = (
        (cs2_eff - (4.0 / 3.0) * w_eff) * theta**2
        + four_pi_G * rho_d * w_eff
        - four_pi_G * rho_eff * (1.0 - 3.0 * w_eff**2)
    )
    # Terms of the Lambda=0 form of [GM] Eq. (4.25).
    terms_4_25 = np.stack(
        (
            state_ddot[2],
            ((2.0 / 3.0) + cs2_eff - 2.0 * w_eff)
            * theta
            * state_dot[2],
            coefficient_4_25 * state[2],
            -four_pi_G * rho_d * (1.0 + w_eff) * state[0],
        )
    )

    coefficient_4_26 = (
        (4.0 / 9.0) * theta**2
        - (20.0 * np.pi * G / 3.0) * rho_d
        - (four_pi_G / 3.0) * rho_eff * (5.0 + 9.0 * w_eff)
    )
    # Terms of the Lambda=0 form of [GM] Eq. (4.26).
    terms_4_26 = np.stack(
        (
            state_ddot[1],
            (5.0 / 3.0) * theta * state_dot[1],
            coefficient_4_26 * state[1],
        )
    )

    maxima = {}
    for equation, terms in {
        "4.24": terms_4_24,
        "4.25": terms_4_25,
        "4.26": terms_4_26,
    }.items():
        # The pointwise scale is the sum of the absolute magnitudes of every
        # term entering that equation; 1e-300 handles an all-zero scale.
        scale = np.maximum(np.sum(np.abs(terms), axis=0), 1e-300)
        scaled_residual = np.abs(np.sum(terms, axis=0)) / scale
        maxima[equation] = float(np.max(scaled_residual))

    assert max(maxima.values()) < TRAJECTORY_RESIDUAL_GATE, (
        f"finite-difference residual gate {TRAJECTORY_RESIDUAL_GATE} exceeded: "
        f"{maxima}"
    )


def test_numerical_trajectory_obeys_z_equals_minus_delta_dot(perturbation_setup):
    params, epoch, initial = perturbation_setup
    t_eval = np.linspace(epoch.time, params.t0, 2001)
    solution = solve_comoving(
        params=params,
        initial_conditions=initial,
        t_eval=t_eval,
        config=TIGHT_DOP853,
        G=G,
    )
    h = t_eval[1] - t_eval[0]
    delta = solution.y[0]
    derivative = (
        delta[:-4] - 8.0 * delta[1:-3] + 8.0 * delta[3:-1] - delta[4:]
    ) / (12.0 * h)
    np.testing.assert_allclose(-derivative, solution.y[1, 2:-2], rtol=1e-6, atol=2e-10)


def test_early_eds_growing_mode_and_clean_system_agreement():
    """As f_v->0, Eq. (4.27) has the EdS growing mode Delta~t^(2/3)."""
    params = TrackerParams(fv0=1e-10, HD0=1.0)
    t_initial = 1e-3 * params.t0
    t_final = 0.1 * params.t0
    amplitude = 2e-3
    delta_initial = amplitude * t_initial ** (2.0 / 3.0)
    delta_dot_initial = (2.0 / 3.0) * amplitude * t_initial ** (-1.0 / 3.0)
    initial = PerturbationInitialConditions(
        delta_d=delta_initial,
        expansion_gradient=-delta_dot_initial,
        delta_eff=0.0,
        rate_units=RateUnitConvention.UPSTREAM_UNCONVERTED,
    )
    t_eval = np.geomspace(t_initial, t_final, 600)
    meszaros = solve_meszaros(
        params=params, initial_conditions=initial, t_eval=t_eval,
        config=TIGHT_DOP853, G=G
    )
    comoving = solve_comoving(
        params=params, initial_conditions=initial, t_eval=t_eval,
        config=TIGHT_DOP853, G=G
    )
    expected = amplitude * t_eval ** (2.0 / 3.0)
    np.testing.assert_allclose(meszaros.y[0], expected, rtol=2e-7, atol=1e-13)
    np.testing.assert_allclose(comoving.y[0], meszaros.y[0], rtol=2e-7, atol=1e-13)


def test_figure_2_published_endpoint_scale(perturbation_setup):
    """[GM] Fig. 2 endpoints are approximately 0.04, 0.033, and 0.007."""
    params, epoch, initial = perturbation_setup
    t_eval = np.linspace(epoch.time, params.t0, 1000)
    comoving = solve_comoving(
        params=params, initial_conditions=initial, t_eval=t_eval,
        config=TIGHT_DOP853, G=G
    )
    meszaros = solve_meszaros(
        params=params, initial_conditions=initial, t_eval=t_eval,
        config=TIGHT_DOP853, G=G
    )
    assert comoving.y[0, -1] == pytest.approx(0.04, abs=0.003, rel=0.0)
    assert meszaros.y[0, -1] == pytest.approx(0.033, abs=0.002, rel=0.0)
    assert comoving.y[2, -1] == pytest.approx(0.007, abs=0.001, rel=0.0)


@pytest.mark.parametrize("bad_state", [[1.0], [1.0, 2.0, 3.0], [1.0, np.nan]])
def test_meszaros_state_validation(perturbation_setup, bad_state):
    params, epoch, _ = perturbation_setup
    with pytest.raises(ValueError):
        meszaros_rhs(epoch.time, bad_state, params=params, G=G)


def test_solver_rejects_unsorted_evaluation_times(perturbation_setup):
    params, epoch, initial = perturbation_setup
    with pytest.raises(ValueError):
        solve_comoving(
            params=params,
            initial_conditions=initial,
            t_eval=[epoch.time, epoch.time],
            config=TIGHT_DOP853,
            G=G,
        )
