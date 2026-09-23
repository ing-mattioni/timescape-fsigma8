"""Successor errata F2 and F9 of the post-remediation review.

F2: the bare-to-dressed growth-rate factor g(f_v) = (2+f_v)^2/(4+f_v+4f_v^2)
is not bounded by the "1.025-1.084" range quoted in 1D-A/1D-C; it peaks at
g(2/5) = 8/7 at dressed z ~ 2.007.  F9: the 1C-A text factor for the
paper-caption wavenumber is a_D0 * h_LCDM/h_TS = 1.25955 (as implemented), not
a_D0 * h_TS/h_LCDM.  See reports/phase1f_c_r_f2_f4_f9_remediation.md.
"""

# A06: absolute budgets use rtol=0; relative budgets use atol=0.  Table
# values are quoted to 4 decimals in the erratum (budget 5e-5 absolute);
# closed-form identities use a 1e-12 roundoff allowance.

from __future__ import annotations

import numpy as np
import pytest
from scipy.optimize import brentq

import timescape_fsigma8.background as bg
from timescape_fsigma8.growth import GrowthBackgroundPreset, resolve_background
from timescape_fsigma8.growth.rates import dressed_chain_factor
from timescape_fsigma8.perturbations import WavenumberConvention, resolve_wavenumber


def chain(f: np.ndarray) -> np.ndarray:
    return (2.0 + f) ** 2 / (4.0 + f + 4.0 * f**2)


def time_at_fv(params, value: float) -> float:
    return brentq(lambda t: float(bg.fv(t, params)) - value, 1e-6 * params.t0, params.t0,
                  xtol=1e-15, rtol=8.9e-16, maxiter=200)


def time_at_redshift(params, z: float) -> float:
    if z == 0.0:
        return params.t0
    return brentq(lambda t: float(bg.redshift(t, params)) - z, 1e-6 * params.t0, params.t0,
                  xtol=1e-15, rtol=8.9e-16, maxiter=200)


def test_f2_chain_factor_derivative_and_global_maximum() -> None:
    f = np.linspace(0.0, 1.0, 100001)
    numerical = np.gradient(chain(f), f)
    analytic = (2.0 + f) * (6.0 - 15.0 * f) / (4.0 + f + 4.0 * f**2) ** 2
    np.testing.assert_allclose(numerical[1:-1], analytic[1:-1], rtol=0.0, atol=1e-8)
    assert int(np.argmax(chain(f))) == 40000  # f_v = 2/5
    assert chain(np.array(0.4)) == pytest.approx(8.0 / 7.0, rel=1e-12, abs=0.0)


@pytest.mark.parametrize("preset", list(GrowthBackgroundPreset), ids=lambda p: p.value)
def test_f2_tracker_history_exceeds_the_superseded_range(preset) -> None:
    params = resolve_background(preset).params
    t_peak = time_at_fv(params, 0.4)
    assert float(dressed_chain_factor(t_peak, params)) == pytest.approx(8.0 / 7.0, rel=1e-12, abs=0.0)
    assert float(bg.redshift(t_peak, params)) == pytest.approx(2.00656, rel=0.0, abs=1e-4)
    expected = {20.0: 1.0248, 10.0: 1.0579, 3.0: 1.1361, 2.0: 1.1429,
                1.0: 1.1307, 0.5: 1.1124, 0.3: 1.1024, 0.0: 1.0842}
    for z, value in expected.items():
        measured = float(dressed_chain_factor(time_at_redshift(params, z), params))
        assert measured == pytest.approx(value, rel=0.0, abs=5e-5), z
    window = np.array([time_at_redshift(params, z) for z in np.linspace(0.3, 3.0, 55)])
    factors = dressed_chain_factor(window, params)
    # Everywhere in 0.3 <= z <= 3 the factor exceeds the quoted upper bound.
    assert float(np.min(factors)) > 1.084156333813626
    assert float(np.max(factors)) <= 8.0 / 7.0 + 1e-12


def test_f9_paper_caption_wavenumber_factor_is_aD0_times_hlcdm_over_hts() -> None:
    params = resolve_background(GrowthBackgroundPreset.NOTEBOOK_REFERENCE).params
    resolved = resolve_wavenumber(
        2.0 * np.pi,
        params=params,
        convention=WavenumberConvention.PAPER_LCDM_HUBBLE_K,
        timescape_h=0.7323,
        lcdm_h=0.674,
    )
    factor = resolved.matrix_k / resolved.supplied_k
    assert params.aD0 == pytest.approx(1.3685, rel=1e-12, abs=0.0)
    assert factor == pytest.approx(1.3685 * 0.674 / 0.7323, rel=1e-12, abs=0.0)
    assert factor == pytest.approx(1.25955, rel=0.0, abs=5e-6)
    # The 1C-A text wrote a_D0 * h_TS/h_LCDM while quoting 0.9204 = h_LCDM/h_TS.
    assert 0.674 / 0.7323 == pytest.approx(0.9204, rel=0.0, abs=5e-5)
    assert factor != pytest.approx(1.3685 * 0.7323 / 0.674, rel=1e-3, abs=0.0)
