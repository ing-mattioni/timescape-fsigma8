"""Extraction, reference, relative growth, analytic rates, and mapping."""

import numpy as np
import pytest

import timescape_fsigma8.background as bg
from timescape_fsigma8.perturbations.scenarios import PHASE1C_EPOCH_ROOT
from timescape_fsigma8.growth import (
    DensityContrastMapping,
    GrowthCoordinate,
    GrowthD3Branch,
    GrowthReference,
    GrowthReferenceCoordinate,
    GrowthSystem,
    HarmonicMetadata,
    HarmonicSignConvention,
    GrowthWavenumberConvention,
    extract_dust_mode,
    map_delta_m,
    map_delta_m_dln_a_derivative,
    run_growth_pipeline,
)
from growth_test_utils import (
    TEST_NUMERICS,
    TEST_REFERENCE_Z10,
    barotropic_scenario,
    clean_scenario,
    run_cached,
)


@pytest.fixture(scope="module")
def meszaros_run():
    return run_cached(clean_scenario(GrowthSystem.MESZAROS))


@pytest.fixture(scope="module")
def comoving_run():
    return run_cached(clean_scenario(GrowthSystem.COMOVING))


@pytest.fixture(scope="module")
def barotropic_run():
    return run_cached(
        barotropic_scenario(GrowthD3Branch.PRINTED_4_15, 2.0 * np.pi, "2pi")
    )


# ---------------------------------------------------------------- extraction
def test_extraction_requires_explicit_system_and_correct_shapes():
    y2 = np.arange(10.0).reshape(2, 5)
    with pytest.raises(ValueError, match="explicit GrowthSystem"):
        extract_dust_mode(system="meszaros", y=y2)
    with pytest.raises(ValueError, match="exactly 3"):
        extract_dust_mode(system=GrowthSystem.COMOVING, y=y2)
    with pytest.raises(ValueError, match="exactly 4"):
        extract_dust_mode(system=GrowthSystem.BAROTROPIC, y=y2)


def test_meszaros_sign_conversion_z_equals_minus_y1():
    y = np.array([[1.0, 2.0, 3.0], [0.5, -0.25, 0.125]])
    delta, z = extract_dust_mode(system=GrowthSystem.MESZAROS, y=y)
    np.testing.assert_array_equal(delta, y[0])
    np.testing.assert_array_equal(z, -y[1])


def test_comoving_and_barotropic_pass_z_through():
    y3 = np.vstack([np.ones(4), np.linspace(-1, 1, 4), np.zeros(4)])
    _, z3 = extract_dust_mode(system=GrowthSystem.COMOVING, y=y3)
    np.testing.assert_array_equal(z3, y3[1])
    y4 = np.vstack([y3, np.zeros(4)])
    _, z4 = extract_dust_mode(system=GrowthSystem.BAROTROPIC, y=y4)
    np.testing.assert_array_equal(z4, y4[1])


def test_meszaros_initial_z_matches_ic_convention(meszaros_run):
    ic = meszaros_run.history.initial_conditions
    assert meszaros_run.history.z_expansion[0] == pytest.approx(
        ic.expansion_gradient, rel=1e-12
    )


# ---------------------------------------------------------------- reference
def test_reference_resolution_records_all_coordinates(meszaros_run):
    ref = meszaros_run.reference
    params = meszaros_run.history.background.params
    assert ref.dressed_redshift == pytest.approx(10.0, abs=1e-9)
    assert ref.a_obs == pytest.approx(1.0 / 11.0, rel=1e-9)
    assert ref.a_obs == pytest.approx(
        float(bg.a_w(ref.t_solver_units, params)), rel=1e-12
    )
    assert ref.t_gyr == pytest.approx(
        ref.t_solver_units / meszaros_run.history.time_unit_per_gyr
    )


def test_reference_outside_integrated_solution_is_rejected():
    scenario = clean_scenario(GrowthSystem.MESZAROS)
    bad = GrowthReference(
        coordinate=GrowthReferenceCoordinate.BARE_TIME_SOLVER_UNITS,
        value=1e6,
        root=PHASE1C_EPOCH_ROOT,
        amplitude_floor_rel=1e-10,
    )
    with pytest.raises(ValueError, match="outside the integrated"):
        run_growth_pipeline(
            scenario=scenario,
            reference=bad,
            numerics=TEST_NUMERICS,
            provenance=None,
        )


def test_reference_near_a_crossing_is_rejected():
    # derived_4_10 2pi has its Delta_d root at dressed z ~ 0.3696; ask for a
    # reference on top of it (bare time inside the refined-root tolerance).
    scenario = barotropic_scenario(
        GrowthD3Branch.DERIVED_4_10, 2.0 * np.pi, "2pi"
    )
    base = run_cached(scenario)
    root_t = base.crossings.delta_d_roots[0].t_root
    at_crossing = GrowthReference(
        coordinate=GrowthReferenceCoordinate.BARE_TIME_SOLVER_UNITS,
        value=root_t,
        root=PHASE1C_EPOCH_ROOT,
        amplitude_floor_rel=1e-10,
    )
    with pytest.raises(ValueError, match="zero crossing|Delta_d root"):
        run_growth_pipeline(
            scenario=scenario,
            reference=at_crossing,
            numerics=TEST_NUMERICS,
            provenance=None,
        )


# ---------------------------------------------------------------- growth
def test_relative_growth_is_normalised_at_the_reference(comoving_run):
    ref = comoving_run.reference
    idx = int(np.argmin(np.abs(comoving_run.history.t - ref.t_solver_units)))
    g_near_ref = comoving_run.relative_growth_delta_d[idx]
    assert g_near_ref == pytest.approx(1.0, rel=5e-3)
    np.testing.assert_allclose(
        comoving_run.relative_growth_delta_d,
        comoving_run.history.delta_d / ref.amplitude_delta_d,
        rtol=0.0,
        atol=0.0,
    )


def test_g_delta_equals_g_m_to_numerical_precision():
    run = run_cached(
        barotropic_scenario(
            GrowthD3Branch.PRINTED_4_15,
            2.0 * np.pi,
            "2pi",
            mapping=DensityContrastMapping.MAP_TO_DELTA_M_VIA_MINUS_K_CODE2,
        )
    )
    assert run.mapped is not None
    np.testing.assert_allclose(
        run.mapped.relative_growth,
        run.relative_growth_delta_d,
        rtol=5e-16,
        atol=0.0,
    )


# ---------------------------------------------------------------- rates
def test_analytic_f_bare_identity_f_times_D(meszaros_run):
    r = meszaros_run.rates
    h = meszaros_run.history
    np.testing.assert_allclose(
        r.f_bare * h.delta_d, r.dDelta_d_dln_aD, rtol=1e-12, atol=1e-18
    )


def test_analytic_f_dressed_identity(meszaros_run):
    r = meszaros_run.rates
    h = meszaros_run.history
    np.testing.assert_allclose(
        r.f_dressed * h.delta_d, r.dDelta_d_dln_aobs, rtol=1e-12, atol=1e-18
    )


def test_exact_tracker_chain_factor(meszaros_run):
    h = meszaros_run.history
    f_v = bg.fv(h.t, h.background.params)
    expected = (2.0 + f_v) ** 2 / (4.0 + f_v + 4.0 * f_v**2)
    np.testing.assert_allclose(
        meszaros_run.rates.chain_factor, expected, rtol=1e-14
    )
    np.testing.assert_allclose(
        meszaros_run.rates.f_dressed,
        meszaros_run.rates.f_bare * expected,
        rtol=1e-13,
    )
    # audited value at t0 (1D-A Sec. 7)
    assert meszaros_run.rates.chain_factor[-1] == pytest.approx(
        1.08416, abs=5e-5
    )


def test_f_bare_against_independent_finite_difference(comoving_run):
    """Validation-only cross-check, not a rate implementation."""
    h = comoving_run.history
    ln_a = np.log(np.asarray(bg.a_D(h.t, h.background.params)))
    ln_d = np.log(np.abs(h.delta_d))
    fd = np.gradient(ln_d, ln_a)
    interior = slice(5, -5)
    np.testing.assert_allclose(
        comoving_run.rates.f_bare[interior], fd[interior], rtol=5e-3
    )


def test_non_logarithmic_derivative_matches_minus_3z_over_theta(barotropic_run):
    h = barotropic_run.history
    theta = np.asarray(bg.Theta(h.t, h.background.params))
    np.testing.assert_allclose(
        barotropic_run.rates.dDelta_d_dln_aD,
        -3.0 * h.z_expansion / theta,
        rtol=1e-14,
    )


def test_rates_masked_nan_at_amplitude_roots_never_infinite():
    run = run_cached(
        barotropic_scenario(GrowthD3Branch.DERIVED_4_10, 10.0 * np.pi, "10pi")
    )
    assert len(run.crossings.delta_d_roots) >= 1
    assert not np.any(np.isinf(run.rates.f_bare))
    assert not np.any(np.isinf(run.rates.f_dressed))
    masked = run.rates.near_zero_mask
    if masked.any():
        assert np.all(np.isnan(run.rates.f_bare[masked]))
        assert np.all(np.isnan(run.rates.f_dressed[masked]))
        # the non-logarithmic derivative stays finite at those samples
        assert np.all(np.isfinite(run.rates.dDelta_d_dln_aD[masked]))
        assert np.all(np.isfinite(run.rates.dDelta_d_dln_aobs[masked]))
    assert np.all(np.isfinite(run.rates.dDelta_d_dln_aD))


def test_z_roots_are_rate_zeros_and_do_not_split_intervals():
    run = run_cached(
        barotropic_scenario(GrowthD3Branch.DERIVED_4_10, 2.0 * np.pi, "2pi")
    )
    assert len(run.crossings.z_roots) == 1
    z_root = run.crossings.z_roots[0]
    # exactly one Delta_d root => exactly two validity intervals; the Z root
    # lies inside the first one without splitting it
    assert len(run.crossings.delta_d_roots) == 1
    assert len(run.validity_intervals) == 2
    first = run.validity_intervals[0]
    assert first.start < z_root.t_root < first.end
    # f passes through zero near the Z root
    h = run.history
    idx = int(np.argmin(np.abs(h.t - z_root.t_root)))
    window = run.rates.f_bare[max(idx - 2, 0) : idx + 3]
    assert np.nanmin(np.abs(window)) < 2e-2


# ---------------------------------------------------------------- mapping
def test_density_mapping_formula_and_derivative_factor():
    harmonic = HarmonicMetadata(
        mode_label="test",
        k_code=3.0,
        wavenumber_convention=GrowthWavenumberConvention.NOT_APPLICABLE,
        sign_convention=HarmonicSignConvention.NEGATIVE_LAPLACIAN_EIGENVALUE,
        k_com_D_H0TS_over_c=3.0,
        k_phys0_D_H0TS_over_c=3.0 / 1.3685,
    )
    delta_d = np.array([9.0, -18.0, 4.5])
    delta_m = map_delta_m(delta_d, harmonic=harmonic)
    np.testing.assert_allclose(delta_m, -delta_d / 9.0, rtol=0.0)
    deriv = map_delta_m_dln_a_derivative(delta_d, harmonic=harmonic)
    np.testing.assert_allclose(deriv, -delta_d / 9.0, rtol=0.0)


def test_mapped_run_exposes_harmonic_metadata_and_derivatives():
    run = run_cached(
        barotropic_scenario(
            GrowthD3Branch.PRINTED_4_15,
            5.0 * np.pi,
            "5pi",
            mapping=DensityContrastMapping.MAP_TO_DELTA_M_VIA_MINUS_K_CODE2,
        )
    )
    assert run.mapped is not None
    hm = run.mapped.harmonic
    assert hm.k_code == pytest.approx(5.0 * np.pi)
    assert hm.k_com_D_H0TS_over_c == pytest.approx(hm.k_code)
    assert hm.k_phys0_D_H0TS_over_c == pytest.approx(
        hm.k_code / run.history.background.params.aD0
    )
    # d delta_m/d ln a_D = +3Z/(Theta k^2)
    theta = np.asarray(
        bg.Theta(run.history.t, run.history.background.params)
    )
    np.testing.assert_allclose(
        run.mapped.d_delta_m_dln_aD,
        3.0 * run.history.z_expansion / (theta * hm.k_code**2),
        rtol=1e-13,
    )
    # logarithmic rates identical for Delta_d and delta_m (C cancels)
    ok = ~run.rates.near_zero_mask
    f_from_dm = np.full_like(run.rates.f_bare, np.nan)
    f_from_dm[ok] = (
        run.mapped.d_delta_m_dln_aD[ok] / run.mapped.delta_m[ok]
    )
    np.testing.assert_allclose(
        f_from_dm[ok], run.rates.f_bare[ok], rtol=1e-12
    )


def test_zero_k_code_is_rejected_for_mapped_output():
    with pytest.raises(ValueError, match="finite and positive"):
        HarmonicMetadata(
            mode_label="bad",
            k_code=0.0,
            wavenumber_convention=GrowthWavenumberConvention.NOT_APPLICABLE,
            sign_convention=(
                HarmonicSignConvention.NEGATIVE_LAPLACIAN_EIGENVALUE
            ),
            k_com_D_H0TS_over_c=0.0,
            k_phys0_D_H0TS_over_c=0.0,
        )


# ---------------------------------------------------------------- scale (in)dependence
def test_clean_relative_growth_invariant_under_harmonic_metadata():
    runs = [
        run_cached(
            clean_scenario(
                GrowthSystem.COMOVING,
                mapping=(
                    DensityContrastMapping.MAP_TO_DELTA_M_VIA_MINUS_K_CODE2
                ),
                mode_k=k,
                mode_label=label,
            )
        )
        for k, label in [(7.0, "meta7"), (13.0, "meta13")]
    ]
    np.testing.assert_array_equal(
        runs[0].relative_growth_delta_d, runs[1].relative_growth_delta_d
    )
    np.testing.assert_array_equal(runs[0].rates.f_bare, runs[1].rates.f_bare)
    # while the absolute mapped coefficient does change
    assert not np.allclose(
        runs[0].mapped.delta_m[-1], runs[1].mapped.delta_m[-1]
    )


def test_barotropic_histories_differ_across_k_code():
    r2 = run_cached(
        barotropic_scenario(GrowthD3Branch.PRINTED_4_15, 2.0 * np.pi, "2pi")
    )
    r5 = run_cached(
        barotropic_scenario(GrowthD3Branch.PRINTED_4_15, 5.0 * np.pi, "5pi")
    )
    end2 = r2.relative_growth_delta_d[-1]
    end5 = r5.relative_growth_delta_d[-1]
    assert abs(end5 / end2) > 10.0


# ---------------------------------------------------------------- immutability
def test_output_arrays_are_immutable(meszaros_run):
    for arr in (
        meszaros_run.history.t,
        meszaros_run.history.delta_d,
        meszaros_run.history.z_expansion,
        meszaros_run.relative_growth_delta_d,
        meszaros_run.rates.f_bare,
        meszaros_run.rates.dDelta_d_dln_aD,
    ):
        with pytest.raises((ValueError, RuntimeError)):
            arr[0] = 123.0
