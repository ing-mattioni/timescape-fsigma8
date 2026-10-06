"""Report-only 1G-G: conditional population evolution and conservation tests.

[L03] Leyvraz, arXiv:cond-mat/0305670, Eqs. (2.2), (4.4)-(4.10).
[JLH13] arXiv:1304.6087, Eqs. (A4)-(A5), (A8)-(A9).
[GM] arXiv:2511.17160v2, Eqs. (5.5)-(5.6).
New deductions G1-G12 and their assumptions are in the companion report.
The constant kernel is an analytic benchmark, NOT a Timescape merger law.
No new package API, observational prediction, fit, or status token.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from phase1g_f_volume_budget_successor_numerics import BASE_COMMIT, frozen_module

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/independent/phase1g_g_void_evolution.json"


def _fraction(value: float) -> None:
    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError("fraction must be finite and in [0, 1]")


def fraction_rate(*, fraction: float, h_void: float, h_wall: float,
                  transfer_over_domain_volume: float) -> float:
    """G5: dot(f) = 3 f(1-f)(H_v-H_w) + J/V.

    Derived from regional volumes ([GM] (5.1), (5.5)-(5.6)) and the first
    moment of [L03] (2.2). H and J/V have inverse-time units, same clock.
    J>0 converts wall volume to void volume; it is not a merger rate.
    """
    _fraction(fraction)
    if not all(math.isfinite(v) for v in (h_void, h_wall, transfer_over_domain_volume)):
        raise ValueError("rates must be finite")
    return 3.0 * fraction * (1.0 - fraction) * (h_void - h_wall) + transfer_over_domain_volume


def tracker_fraction(*, time: float, reference_time: float, reference_fraction: float) -> float:
    """G4: Milne/EdS volumes imply [GM] (5.6), with supplied normalization.

    This is a conditional identity, not a spectrum-derived f_v0.
    """
    _fraction(reference_fraction)
    if not all(math.isfinite(t) and t > 0.0 for t in (time, reference_time)):
        raise ValueError("times must be finite and positive")
    y = time / reference_time
    return reference_fraction * y / (1.0 - reference_fraction + reference_fraction * y)


def void_mass_fraction(*, volume_fraction: float, density_ratio: float) -> float:
    """G7 from M = rho V: inverse of project two-density identities F1-F2.

    [JLH13] (13) defines a cumulative volume; it does not derive this budget.

    x = rho_void/rho_wall, not rho_void/rho_global. Vacuum allowed for f<1.
    """
    _fraction(volume_fraction)
    if not math.isfinite(density_ratio) or not 0.0 <= density_ratio <= 1.0:
        raise ValueError("void/wall density ratio must be finite and in [0, 1]")
    denominator = 1.0 - volume_fraction + volume_fraction * density_ratio
    if denominator <= 0.0:
        raise ValueError("an all-vacuum domain has no defined mass fraction")
    return volume_fraction * density_ratio / denominator


def constant_kernel_counts(*, classes: int, initial_number_density: float,
                           merger_exposure: float) -> NDArray[np.float64]:
    """G10, [L03] (4.10): n_k=N0/(1+u)^2 [u/(1+u)]^(k-1).

    u=N0*integral(K_eff dt)/2 is supplied, dimensionless. n is number per
    fixed reference volume; labels k*q0 are additive reduced void volumes.
    The output omits k>classes; no tail renormalization is performed.
    """
    if not isinstance(classes, int) or isinstance(classes, bool) or classes < 1:
        raise ValueError("classes must be a positive integer")
    if not math.isfinite(initial_number_density) or initial_number_density <= 0.0:
        raise ValueError("initial number density must be finite and positive")
    if not math.isfinite(merger_exposure) or merger_exposure < 0.0:
        raise ValueError("merger exposure must be finite and nonnegative")
    u = merger_exposure
    q = u / (1.0 + u)
    values = initial_number_density / (1.0 + u) ** 2 * q ** np.arange(classes)
    values.setflags(write=False)
    return values


def constant_kernel_volume_tail(*, minimum_class: int, merger_exposure: float) -> float:
    """G11: sum_{k>=kmin} k*n_k/N0, analytic tail of [L03] (4.10).

    Distinct from a number-weighted tail. No finite-grid truncation.
    """
    if not isinstance(minimum_class, int) or isinstance(minimum_class, bool) or minimum_class < 1:
        raise ValueError("minimum class must be a positive integer")
    if not math.isfinite(merger_exposure) or merger_exposure < 0.0:
        raise ValueError("merger exposure must be finite and nonnegative")
    k = minimum_class
    q = merger_exposure / (1.0 + merger_exposure)
    return q ** (k - 1) * (1.0 + (k - 1) * (1.0 - q))


def build_evidence() -> dict[str, Any]:
    f = frozen_module()
    sph = f.spherical_model()
    sc = sph["shell_crossing"]
    x = sc["one_plus_delta_sc"]
    hvt = sc["shell_hubble_over_background"] * 2.0 / 3.0
    # G6 uses [JLH13] (A8): H_v*t = 8/9, so 3*(H_v-H_w)*t = 2/3.
    coefficient = 3.0 * hvt - 2.0
    cases = {}
    for name in ("PAPER_REFERENCE", "NW15_CMB_FIT"):
        p = f.g1a._cases()[name]
        fv0 = float(f.bg.fv(p.t0, p))
        rows = []
        for z in (0.0, 0.5, 1.0, 2.0, 3.0):
            t = p.t0 if z == 0.0 else f.g1a.t_of_redshift(p, z)
            expected = float(f.bg.fv(t, p))
            actual = tracker_fraction(time=t, reference_time=p.t0, reference_fraction=fv0)
            rows.append({"z": z, "time_over_t0": t / p.t0, "tracker": expected,
                         "from_conditional_volume_moments": actual, "residual": actual - expected})
        cases[name] = {
            "f_v0_supplied": fv0, "history": rows,
            "mass_fraction_if_shell_density_at_f_v0": void_mass_fraction(volume_fraction=fv0, density_ratio=x),
            "mass_fraction_if_exact_vacuum_at_f_v0": void_mass_fraction(volume_fraction=fv0, density_ratio=0.0),
            "J_over_V_times_t_if_shell_rates_and_tracker_target": fv0 * (1.0 - fv0) * (1.0 - coefficient),
        }
    # Analytic merger benchmark. q0 and N0 arbitrary; dimensionless moment ratios.
    merger_rows = []
    for u in (0.0, 1.0, 10.0, 100.0):
        n = constant_kernel_counts(classes=10000, initial_number_density=1.0, merger_exposure=u)
        k = np.arange(1, len(n) + 1, dtype=float)
        merger_rows.append({"u_external": u, "number_ratio": float(n.sum()),
                            "reduced_volume_ratio": float(k @ n),
                            "omitted_volume_tail": constant_kernel_volume_tail(minimum_class=10001, merger_exposure=u),
                            "radius_at_mean_volume_over_seed_radius": (1.0 + u) ** (1.0 / 3.0),
                            "volume_share_in_k_ge_125": constant_kernel_volume_tail(minimum_class=125, merger_exposure=u)})
    return {"base_commit": BASE_COMMIT, "scope": "REPORT_ONLY_CONDITIONAL_EVOLUTION",
            "kernel_status": "EXTERNAL_BENCHMARK_NOT_A_TIMESCAPE_CLOSURE",
            "assumptions": ["mean field: spatial cluster correlations neglected", "averaged cluster morphology", "common size- and age-independent regional void expansion rate", "G6 is an instantaneous synchronous shell-crossing cohort, not F population evolution"],
            "spherical_shell_crossing": {"x_void_over_wall": x, "H_v_times_t": hvt,
                                         "fraction_growth_coefficient": coefficient,
                                         "tracker_fraction_growth_coefficient": 1.0},
            "cases": cases, "constant_kernel_benchmark": merger_rows,
            "tolerances": {"moment_absolute": 2e-12, "tracker_absolute": 2e-14},
            "observational_outputs": False}


def main() -> int:
    result = build_evidence()
    for row in result["constant_kernel_benchmark"]:
        if abs(row["reduced_volume_ratio"] + row["omitted_volume_tail"] - 1.0) > 2e-12:
            raise AssertionError("constant-kernel first moment is not conserved")
    for case in result["cases"].values():
        if max(abs(row["residual"]) for row in case["history"]) > 2e-14:
            raise AssertionError("conditional moment identity does not reproduce tracker")
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_bytes((json.dumps(result, indent=2, allow_nan=False) + "\n").encode("utf-8"))
    print(ARTIFACT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
