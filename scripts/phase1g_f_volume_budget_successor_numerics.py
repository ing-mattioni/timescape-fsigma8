"""Evidence for the 2026-10-01 Phase 1G-F volume-budget successor.

Scientific correction, approved by the owner in this session; frozen 1G-F
remains unchanged. See reports/phase1g_f_volume_budget_successor.md, F1-F3.
[JLH13] arXiv:1304.6087 Eq. (13) defines an additive cumulative volume;
F1-F3 derive its normalization for the conditional two-density M3 model.
No observational statistic or scientific-status token is introduced.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import sys
from typing import Any

import numpy as np
import scipy

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/independent/phase1g_f_volume_budget_successor.json"
BASE_COMMIT = "fb5d95245bc0cb19ce6cd1438177f1a597bb232f"
REDSHIFTS = (0.0, 0.5, 1.0, 2.0, 3.0)


@dataclass(frozen=True, kw_only=True)
class FixedDomainBudget:
    """One domain, total void mass fraction, and rho_void/rho_wall.

    These are explicit model inputs. Eq. F1 is this project's two-density
    accounting identity V = M/rho. [JLH13] (13) only defines an additive
    cumulative volume, not the M3 normalization. All inputs are dimensionless.
    """

    total_void_mass_fraction: float
    density_ratio: float

    def __post_init__(self) -> None:
        m, x = self.total_void_mass_fraction, self.density_ratio
        if not math.isfinite(m) or not 0.0 <= m <= 1.0:
            raise ValueError("total void mass fraction must be finite and in [0, 1]")
        if not math.isfinite(x) or not 0.0 < x <= 1.0:
            raise ValueError("rho_void/rho_wall must be finite and in (0, 1]")

    @property
    def volume_in_mass_over_wall_density_units(self) -> float:
        """Eq. F1: V / (M_domain/rho_wall)."""
        m = self.total_void_mass_fraction
        return 1.0 - m + m / self.density_ratio

    def cumulative(self, *, selected_void_mass_fraction: float) -> float:
        """Eq. F2, additive version of [JLH13] (13) in the M3 domain."""
        m = selected_void_mass_fraction
        if not math.isfinite(m) or not 0.0 <= m <= self.total_void_mass_fraction:
            raise ValueError("selected mass must lie between zero and the total void mass")
        # Algebraically F2; avoids an unnecessary small-x division.
        total = self.total_void_mass_fraction
        return m / (self.density_ratio * (1.0 - total) + total)

    @property
    def total_void_volume_fraction(self) -> float:
        return self.cumulative(selected_void_mass_fraction=self.total_void_mass_fraction)


def truncated_universe_budget(*, selected_mass: float, density_ratio: float) -> float:
    """Eq. F3: frozen M3 meaning, a new universe after every mass cut.

    NOT an additive cumulative volume in the original domain.
    """
    return FixedDomainBudget(
        total_void_mass_fraction=selected_mass, density_ratio=density_ratio
    ).total_void_volume_fraction


@lru_cache(maxsize=1)
def frozen_module() -> Any:
    """Load the byte-preserved evidence script, including its Windows shim."""
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import _portable_resource

    _portable_resource.install()
    spec = importlib.util.spec_from_file_location(
        "_phase1g_f_frozen_for_successor", ROOT / "scripts/phase1g_f_void_population_numerics.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def corrected_population(pop: dict[str, Any]) -> dict[str, Any]:
    """Apply F2 to frozen [SvdW04] (3)/(C8), [JLH13] (6)-(7) mass bins.

    No rebinning, growth-clock change, tail renormalization or clipping.
    """
    budget = FixedDomainBudget(
        total_void_mass_fraction=pop["void_mass_fraction_1_minus_D"],
        density_ratio=pop["interior_density_ratio"],
    )
    return {
        "void_mass_fraction": budget.total_void_mass_fraction,
        "density_ratio_void_to_wall": budget.density_ratio,
        "domain_volume_units": budget.volume_in_mass_over_wall_density_units,
        "fixed_domain_cumulative": {
            key: budget.cumulative(selected_void_mass_fraction=value)
            for key, value in pop["lagrangian_fraction"].items()
        },
        "legacy_truncated_universe_budget": pop["M3_two_scale_volume_budget"],
        "median_radius_h_inv_Mpc": pop["volume_weighted_median_radius_h_inv_Mpc"],
        "resolved_mass_fraction": pop["resolved_mass_fraction_on_grid"],
        "unresolved_below_grid": pop["unresolved_below_grid"],
        "unresolved_interpretation": "signed grid residual; a negative value is quadrature overshoot, not negative physical mass",
    }


def cutoff_for_target(pop: dict[str, Any], *, target: float, fixed_domain: bool) -> float | None:
    """Invert F2 or F3 on the inherited log-radius grid; no extrapolation.

    Radius unit h^-1 Mpc. Trapezoids and log interpolation are frozen
    1G-F conventions, [JLH13] (15); this is a grid diagnostic, not a fit.
    """
    if not math.isfinite(target) or not 0.0 < target < 1.0:
        raise ValueError("target must be finite and in (0, 1)")
    r = pop["_r_h"]
    d = pop["_dF_dlnr"]
    segments = 0.5 * (d[1:] + d[:-1]) * np.diff(np.log(r))
    masses = np.r_[np.cumsum(segments[::-1])[::-1], 0.0]
    m_total = pop["void_mass_fraction_1_minus_D"]
    x = pop["interior_density_ratio"]
    if fixed_domain:
        cumulative = masses / (x * (1.0 - m_total) + m_total)  # F2
    else:
        cumulative = masses / (x * (1.0 - masses) + masses)  # F3
    if not cumulative[0] >= target > cumulative[-1]:
        return None
    return float(np.exp(np.interp(target, cumulative[::-1], np.log(r)[::-1])))


def correct_archived_populations(*, artifact: Path) -> dict[str, Any]:
    """Apply F2 to every archived sensitivity without changing its inputs.

    Reads the explicit frozen artifact only; preserves historical C3 clocks.
    This is an algebraic correction of archived masses, not a rerun of MC.
    """
    raw = artifact.read_bytes()
    cases = json.loads(raw)["results"]["cases"]
    return {
        "input_filename": artifact.name, "input_sha256": hashlib.sha256(raw).hexdigest(),
        "method": "F2 applied to archived mass fractions; clocks and C3 normalization unchanged",
        "cutoff_status": "archived M3_r_min values use F3 only; not F2 cutoffs; C1 collapse near-empty cutoffs are recomputed separately",
        "cases": {name: {key: corrected_population(pop) for key, pop in case["populations"].items()}
                  for name, case in cases.items()},
    }


def build_evidence() -> dict[str, Any]:
    f = frozen_module()
    g = f.g1a
    sph = f.spherical_model()
    sc = sph["shell_crossing"]
    barrier = {"delta_v": sc["delta_v"], "interior_density_ratio": sc["one_plus_delta_sc"]}
    dc = sph["delta_c"]["collapse"]
    planck = g.PLANCK
    sig_ref = g.sigma_converged(
        8.0 / planck["h"], planck["omega_m_total_Om_h2"], g.BARYON_FRACTION_PRIMARY,
        planck["n_s"], float(g.qplus(0.0, g.PLANCK_2018_QPLUS_RECIPE)),
    )
    anchor = planck["sigma8_linear"] / sig_ref  # frozen [1G-A] Sec. 6.3
    cases = {}
    for name in ("PAPER_REFERENCE", "NW15_CMB_FIT"):
        p = g._cases()[name]
        dens = g.per_photon_matter_density(p)
        h = dens["H0_dressed_km_s_Mpc"] / 100.0
        table = f.sigma_table(dens["omega_m_per_photon"], anchor)
        history = []
        for z in REDSHIFTS:
            t = p.t0 if z == 0 else g.t_of_redshift(p, z)
            fv = float(f.bg.fv(t, p))
            # [GM] (5.4), frozen 1G-F Sec. 3: a_wall / a_photon.
            frame = float(f.bg.gamma_w(t, p)) * (1.0 - fv) ** (1.0 / 3.0)
            growth = frame / (1.0 + z)
            pop = f.void_population(table, growth, barrier, dc, frame, h)
            row = corrected_population(pop)
            row.update({"z": z, "t_over_t0": t / p.t0, "tracker_f_v": fv,
                        "D_wall": growth, "frame": frame,
                        "cutoff_fixed_domain_h_inv_Mpc": cutoff_for_target(pop, target=fv, fixed_domain=True),
                        "cutoff_truncated_universe_h_inv_Mpc": cutoff_for_target(pop, target=fv, fixed_domain=False)})
            history.append(row)
        near_empty = {}
        today = history[0]
        for label, interior in sph["near_empty"].items():
            near_barrier = {"delta_v": interior["delta_v"],
                            "interior_density_ratio": interior["interior_density_ratio"]}
            pop = f.void_population(table, today["D_wall"], near_barrier, dc, today["frame"], h)
            near_empty[label] = {
                **corrected_population(pop),
                "cutoff_fixed_domain_h_inv_Mpc": cutoff_for_target(pop, target=today["tracker_f_v"], fixed_domain=True),
                "cutoff_truncated_universe_h_inv_Mpc": cutoff_for_target(pop, target=today["tracker_f_v"], fixed_domain=False),
            }
        f_cov = today["tracker_f_v"]
        eta = -math.log1p(-f_cov)  # Boolean void probability; frozen 1G-E Sec. 2, E2.
        cases[name] = {"h_dressed": h, "history": history, "near_empty_C1_collapse": near_empty,
                       "boolean_surrogate": {
                           "coverage_supplied": f_cov, "dimensionless_grain_volume_density_eta": eta,
                           "eta_over_full_F_volume_fraction": eta / today["fixed_domain_cumulative"]["all_sizes"],
                           "mean_multiplicity_given_covered": eta / f_cov,
                           "identification": "shares volume-weighted grain-radius shape only; overlapping grains, independently calibrated intensity"}}
    return {"base_commit": BASE_COMMIT, "scope": "C1_wall_shell_crossing_and_near_empty_collapse",
            "interpretation": "CONDITIONAL_NON_OBSERVATIONAL_FIXED_DOMAIN_M3",
            "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
            "spherical": sc, "delta_c": dc, "anchor": anchor, "cases": cases,
            "precision": "Inherited 481-node grid. At z=0 primary r>=10 tails are high by 0.22-0.24%, r>=15 by 0.69-0.75% versus independent absorption CDF. Quote at most two significant figures at r>=15. These are numerical, not physical, error estimates.",
            "sigma_recomputed": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frozen-artifact", type=Path,
                        help="Explicit frozen F JSON: additionally rectify all archived sensitivity populations.")
    args = parser.parse_args()
    result = build_evidence()
    if args.frozen_artifact is not None:
        result["archived_sensitivities"] = correct_archived_populations(artifact=args.frozen_artifact)
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_bytes((json.dumps(result, indent=2, allow_nan=False) + "\n").encode("utf-8"))
    print(ARTIFACT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
