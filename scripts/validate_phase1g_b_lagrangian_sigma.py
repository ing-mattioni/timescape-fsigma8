"""Validation driver for Phase 1G-B (conditional mass-labelled linear sigma(M)).

Writes ``artifacts/independent/phase1g_b_lagrangian_sigma.json`` (git-ignored,
deterministic for a given tree and environment) using the package module
``timescape_fsigma8.lagrangian_sigma``.  Report:
``reports/phase1g_b_lagrangian_sigma_validation.md``.

Cross-checks:
  V1-V3  full precision against the functions of the committed Phase 1G-A
         evidence script ``scripts/phase1g_a_sigma8_path_numerics.py``
         (imported, its ``main`` is not run, nothing of it is written);
  V7     printed precision against the committed 1G-A inventory
         ``reports/phase1g_a_sigma8_derivation_path_inventory.json``;
  V4-V6  convergence, limiting cases, invariances and the normalisation gate.

Every gate is declared below before any evaluation; the script exits nonzero
if one fails.  Planck 2018 inputs and the anchor are script-level explicit
inputs (the package ships none).  Outputs are CONDITIONAL, MODEL-INTERNAL,
NON_OBSERVATIONAL numbers; none is an observational amplitude.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import json
import math
import platform
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

import numpy as np

import timescape_fsigma8.lagrangian_sigma as ls
from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations.growing_mode import CleanPerturbationSystem
from timescape_fsigma8.perturbations.initial_conditions import PLANCK_2018_QPLUS_RECIPE
from timescape_fsigma8.presets import NOTEBOOK_REFERENCE, PAPER_REFERENCE
from timescape_fsigma8 import scientific_status, units

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "artifacts" / "independent" / "phase1g_b_lagrangian_sigma.json"
EVIDENCE_SCRIPT = ROOT / "scripts" / "phase1g_a_sigma8_path_numerics.py"
INVENTORY = ROOT / "reports" / "phase1g_a_sigma8_derivation_path_inventory.json"

# ---------------------------------------------------------------- gates (declared first)
GATES = {
    # V1-V3: package vs 1G-A evidence-script functions, full precision.
    "V1_volume_average_growth_vs_script_rel": 1e-10,   # H0=1 vs Gyr params, rtol 1e-12 solves
    "V1_wall_growth_vs_script_rel": 1e-13,
    "V2_per_photon_density_vs_script_rel": 1e-13,
    "V3_radius_vs_script_rel": 1e-13,
    "V3_early_spectrum_factor_vs_script_rel": 1e-10,
    "V3_anchored_sigma_vs_script_rel": 1e-10,
    "V3_lcdm_reference_vs_script_rel": 1e-12,
    # V4: numerical convergence (package budgets and independent refinements).
    "V4_growth_grid_refinement_abs_log": 1e-7,
    "V4_growth_early_limit_abs_log": 1e-4,
    "V4_growth_extrapolated_limit_abs_log": 1e-7,     # O(f_v(1e-8 t0)) + O(f_v(t_e)^2)
    "V4_quadrature_refinement_rel": 1e-6,
    "V4_quadrature_k_range_rel": 1e-8,
    # V5: identities, limits and invariances.
    "V5_wall_identities_max_rel": 1e-13,
    "V5_small_fv0_first_order_coefficient_abs": 1e-4,  # at f_v0 = 1e-4: O(f_v0) remainder
    "V5_H0_and_G_invariance_rel": 1e-10,
    "V5_window_threshold_continuity_rel": 1e-13,
    # V6: normalisation of the provisional import ([1G-A] Sec. 6.3).
    "V6_lcdm_reference_offset_from_anchor_abs": 0.05,
    # V7: committed 1G-A inventory at its printed precision (half a unit).
    "V7_inventory_growth_six_decimals_abs": 5e-7,
    "V7_inventory_fv0_scan_four_decimals_abs": 5e-5,
    "V7_inventory_sigma_table_four_decimals_abs": 5e-5,
    "V7_inventory_per_photon_density_five_decimals_abs": 5e-6,
}

# ---------------------------------------------------------------- explicit inputs
G = 1.0                     # cancels in every output; explicit (no package default)
IDENTITY_RTOL = 1e-13
OMEGA_M_LCDM = PLANCK_2018_QPLUS_RECIPE.omega_m * PLANCK_2018_QPLUS_RECIPE.h ** 2
R_LCDM = 8.0 / PLANCK_2018_QPLUS_RECIPE.h
PRIMARY_FB = 0.02237 / OMEGA_M_LCDM
BARYON_FRACTIONS = (0.12, PRIMARY_FB, 0.20)
ANCHOR = 0.8111
ANCHOR_PROVENANCE = "Planck 2018 VI (arXiv:1807.06209) Table 2, TT,TE,EE+lowE+lensing"
ANCHOR_TOLERANCE = 0.05
ANCHOR_RATIONALE = (
    "EH98 zero-baryon-oscillation fit omits BAO wiggles and the 0.06 eV neutrino "
    "suppression (about -1.5%); the first 1G-A run failed a 3% gate at +3.03%; "
    "anchored ratios cancel the common bias ([1G-A] Sec. 6.3)")
CGI = ls.GrowthLaw.VOLUME_AVERAGE_CGI
WALL = ls.GrowthLaw.WALL_REGIONAL_EDS_COMMON_TIME
NA = ls.NOT_APPLICABLE
LAWS = {
    "comoving": (CGI, CleanPerturbationSystem.COMOVING, ls.VOLUME_AVERAGE_GROWTH_REFERENCE_NUMERICS),
    "meszaros": (CGI, CleanPerturbationSystem.MESZAROS, ls.VOLUME_AVERAGE_GROWTH_REFERENCE_NUMERICS),
    "wall": (WALL, NA, ls.WALL_REGIONAL_GROWTH_REFERENCE_CHECKS),
}
CONVENTIONS = {  # package label -> 1G-A script/inventory label
    "equal_mass": "equal_mass_M8_planck",
    "dressed": "dressed_8_over_h_wall_comoving",
    "bare": "bare_8_over_hbar_volume_average",
}
FV0_SCAN = (0.50, 0.55, 0.60, 0.627, 0.65, 0.695, 0.70, 0.737, 0.75, 0.80)


def early_spectrum(baryon_fraction: float) -> ls.EarlySpectrumImport:
    return ls.EarlySpectrumImport(
        A_s=2.100e-9, n_s=0.9649, k_pivot_per_Mpc=0.05, baryon_fraction=baryon_fraction,
        T_cmb_K=2.7255, transfer_model=ls.EarlyTransferModel.EH98_ZERO_BARYON_OSCILLATION,
        provenance=ANCHOR_PROVENANCE + "; T_cmb 2.7255 K", import_status=ls.EARLY_SPECTRUM_IMPORT_STATUS)


def backgrounds() -> dict[str, ls.TimescapeTrackerInput]:
    return {
        "PAPER_REFERENCE": ls.TimescapeTrackerInput.from_reference_preset(preset=PAPER_REFERENCE),
        "NOTEBOOK_REFERENCE": ls.TimescapeTrackerInput.from_reference_preset(preset=NOTEBOOK_REFERENCE),
        "NW15_CMB_FIT": ls.TimescapeTrackerInput(
            label="NW15_CMB_FIT", fv0=0.627, H0_dressed_km_s_Mpc=61.0,
            source="Nazer & Wiltshire, arXiv:1410.3470 (Timescape CMB fit)"),
    }


def radius_spec(kind: str, length: float = 8.0) -> ls.LagrangianRadiusSpec:
    C = ls.LagrangianRadiusConvention
    if kind == "equal_mass":
        return ls.LagrangianRadiusSpec(
            convention=C.EQUAL_LAGRANGIAN_MASS_TO_REFERENCE, length_h_inverse_Mpc=NA,
            reference_omega_m=OMEGA_M_LCDM, reference_radius_Mpc=R_LCDM, explicit_radius_Mpc=NA)
    convention = (C.DRESSED_WALL_COMOVING_LENGTH if kind == "dressed"
                  else C.BARE_VOLUME_AVERAGE_PROPER_LENGTH)
    return ls.LagrangianRadiusSpec(convention=convention, length_h_inverse_Mpc=length,
                                   reference_omega_m=NA, reference_radius_Mpc=NA,
                                   explicit_radius_Mpc=NA)


def load_evidence_script():
    spec = importlib.util.spec_from_file_location("_phase1g_a_numerics", EVIDENCE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git_state() -> dict:
    def run(*args):
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                              check=True).stdout.strip()
    try:
        return {"repository_head": run("rev-parse", "HEAD"),
                "working_tree_changes_present": bool(run("status", "--porcelain"))}
    except (OSError, subprocess.CalledProcessError) as exc:   # recorded, not masked
        return {"repository_head": f"unavailable: {type(exc).__name__}",
                "working_tree_changes_present": None}


def rel(a: float, b: float) -> float:
    return abs(a / b - 1.0)


# ---------------------------------------------------------------- studies
def study_growth(script, cases, gates):
    rows = {}
    for name, bgi in cases.items():
        p_gyr = TrackerParams.from_dressed_H0(
            fv0=bgi.fv0, H0=units.kms_per_mpc_to_per_gyr(bgi.H0_dressed_km_s_Mpc))
        entry = {}
        for law, (growth_law, closure, numerics) in LAWS.items():
            g = ls.timescape_growth_factor(params=bgi.dimensionless_params(), growth_law=growth_law,
                                           closure=closure, numerics=numerics, G=G)
            record = g.to_json_dict()
            if growth_law is CGI:
                script_g = math.exp(script._riccati_log_growth_excess(
                    p_gyr, closure, 1e-6 * p_gyr.t0, 16001))
                d = rel(g.growth_relative_to_volume_average_eds, script_g)
                gates["V1_volume_average_growth_vs_script_rel"].append(d)
                gates["V4_growth_grid_refinement_abs_log"].append(
                    g.diagnostic("log_growth_grid_refinement_change"))
                gates["V4_growth_early_limit_abs_log"].append(
                    g.diagnostic("log_growth_early_limit_change"))
            else:
                script_g = script.wall_regional_bracket(p_gyr)["growth_vs_photon_EdS"]
                d = rel(g.growth_today_photon_normalised, script_g)
                gates["V1_wall_growth_vs_script_rel"].append(d)
                gates["V5_wall_identities_max_rel"].append(max(
                    g.diagnostic(k) for k in ("closed_form_vs_tracker_rel",
                                              "regional_scale_over_t23_rel_spread",
                                              "regional_density_eds_max_rel",
                                              "finite_te_identity_rel")))
            record["script_value"] = script_g
            record["script_rel_diff"] = d
            entry[law] = record
        rows[name] = entry
    return rows


def study_early_limit(gates):
    """Extrapolated t_e -> 0 limit: ln g(1e-6) - bias estimate vs ln g(1e-8)."""
    rows = {}
    for law in ("comoving", "meszaros"):
        _, closure, base = LAWS[law]
        params = TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0)
        by_fraction = {}
        for te in (1e-6, 1e-7, 1e-8):
            numerics = dataclasses.replace(base, early_time_fraction=te,
                                           comparison_early_time_fraction=10.0 * te)
            g = ls.timescape_growth_factor(params=params, growth_law=CGI, closure=closure,
                                           numerics=numerics, G=G)
            by_fraction[f"{te:g}"] = {
                "log_growth": g.log_growth_relative_to_volume_average_eds,
                "linear_bias_estimate": g.diagnostic("log_growth_early_limit_linear_bias_estimate")}
        extrapolated = by_fraction["1e-06"]["log_growth"] - by_fraction["1e-06"]["linear_bias_estimate"]
        deepest = by_fraction["1e-08"]["log_growth"] - by_fraction["1e-08"]["linear_bias_estimate"]
        diff = abs(extrapolated - by_fraction["1e-08"]["log_growth"])
        gates["V4_growth_extrapolated_limit_abs_log"].append(diff)
        rows[law] = {"by_early_time_fraction": by_fraction,
                     "extrapolated_from_1e-6": extrapolated,
                     "extrapolated_from_1e-8": deepest,
                     "abs_diff_extrapolated_1e-6_vs_direct_1e-8": diff,
                     "relative_bias_of_reference_growth": math.expm1(
                         by_fraction["1e-06"]["log_growth"] - deepest)}
    return rows


def study_sigma(script, cases, gates):
    spectra = {f"{f_b:.4f}": early_spectrum(f_b) for f_b in BARYON_FRACTIONS}
    primary = spectra[f"{PRIMARY_FB:.4f}"]
    quadrature = ls.LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE
    reference = ls.lcdm_reference_linear_sigma(recipe=PLANCK_2018_QPLUS_RECIPE, early_spectrum=primary,
                                               radius_Mpc=R_LCDM, quadrature=quadrature)
    script_ref = script.sigma_converged(R_LCDM, OMEGA_M_LCDM, PRIMARY_FB, 0.9649,
                                        reference.growth_today_photon_normalised)
    gates["V3_lcdm_reference_vs_script_rel"].append(rel(reference.linear_sigma, script_ref))
    gates["V6_lcdm_reference_offset_from_anchor_abs"].append(abs(reference.linear_sigma / ANCHOR - 1.0))

    # 1G-A script route: density and minimal growth dictionaries for spectrum_and_sigma.
    density = {}
    growth_min = {}
    params_gyr = {}
    for name, bgi in cases.items():
        p = TrackerParams.from_dressed_H0(fv0=bgi.fv0, H0=units.kms_per_mpc_to_per_gyr(bgi.H0_dressed_km_s_Mpc))
        params_gyr[name] = p
        density[name] = script.per_photon_matter_density(p)
        growth_min[name] = {s.value: {"g_TS_vs_volume_average_EdS": math.exp(
            script._riccati_log_growth_excess(p, s, 1e-6 * p.t0, 16001))} for s in CleanPerturbationSystem}
    script_sigma = script.spectrum_and_sigma(density, growth_min)

    rows = {}
    for name, bgi in cases.items():
        case_rows = {}
        wall_script = script.wall_regional_bracket(params_gyr[name])
        for law, (growth_law, closure, numerics) in LAWS.items():
            law_rows = {}
            for conv, script_label in CONVENTIONS.items():
                script_conv = script_sigma["cases"][name]["closures"]["comoving" if law == "wall" else law][
                    "conventions"][script_label]
                fb_rows = {}
                for fb_label, spec in spectra.items():
                    if law == "wall" and spec is not primary:
                        continue    # the 1G-A wall bracket was evaluated at the primary f_b only
                    ts = ls.conditional_lagrangian_linear_sigma(
                        background=bgi, growth_law=growth_law, closure=closure, growth_numerics=numerics,
                        early_spectrum=spec, radius=radius_spec(conv), quadrature=quadrature,
                        density_identity_tolerance=IDENTITY_RTOL, G=G)
                    anchored = ls.anchor_lagrangian_sigma(
                        timescape=ts, reference=reference, anchor_value=ANCHOR,
                        anchor_provenance=ANCHOR_PROVENANCE, anchor_consistency_tolerance=ANCHOR_TOLERANCE,
                        anchor_consistency_rationale=ANCHOR_RATIONALE)
                    if law == "wall":
                        script_value = (wall_script["X_wall_regional"] * script_conv["E_early_spectrum_factor"]
                                        * ANCHOR)
                    else:
                        script_value = script_conv["by_baryon_fraction"][f"f_b={spec.baryon_fraction:.4f}"][
                            "sigma_planck_anchored"]
                    d_sigma = rel(anchored.anchored_linear_sigma, script_value)
                    gates["V3_anchored_sigma_vs_script_rel"].append(d_sigma)
                    fb_rows[fb_label] = {
                        "linear_sigma": ts.linear_sigma, "sigma_unit_growth": ts.sigma_unit_growth,
                        "anchored_linear_sigma": anchored.anchored_linear_sigma,
                        "sigma_ratio": anchored.sigma_ratio, "growth_ratio": anchored.growth_ratio,
                        "early_spectrum_factor": anchored.early_spectrum_factor,
                        "early_spectrum_differences": list(anchored.early_spectrum_differences),
                        "quadrature_relative_change": ts.quadrature_relative_change,
                        "truncation_envelope_fraction": ts.truncation_envelope_fraction,
                        "script_anchored_value": script_value, "script_rel_diff": d_sigma}
                    if spec is primary:
                        gates["V3_radius_vs_script_rel"].append(rel(ts.radius.radius_Mpc, script_conv["R_Mpc"]))
                        gates["V3_early_spectrum_factor_vs_script_rel"].append(
                            rel(anchored.early_spectrum_factor, script_conv["E_early_spectrum_factor"]))
                        gates["V2_per_photon_density_vs_script_rel"].append(
                            rel(ts.density.omega_m_per_photon, density[name]["omega_m_per_photon"]))
                        gates["V4_quadrature_refinement_rel"].append(ts.quadrature_relative_change)
                        law_rows.setdefault("_radius", {})[conv] = ts.radius.to_json_dict()
                        if law == "comoving" and conv == "equal_mass" and name == "PAPER_REFERENCE":
                            sample = anchored.to_json_dict()
                law_rows[conv] = fb_rows
            case_rows[law] = law_rows
        rows[name] = case_rows
    return {"lcdm_reference": reference.to_json_dict(), "lcdm_reference_script_value": script_ref,
            "cases": rows, "sample_full_record_paper_comoving_equal_mass": sample}


def study_quadrature_refinement(gates):
    """Independent refinements beyond the package's own 8001-vs-4001 check."""
    spec = early_spectrum(PRIMARY_FB)
    base_q = ls.LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE
    variants = {
        "reference": base_q,
        "grid_16001": dataclasses.replace(base_q, grid_points=16001, comparison_grid_points=8001),
        "k_range_1e-7_to_1e3": dataclasses.replace(base_q, k_min_per_Mpc=1e-7, k_max_per_Mpc=1e3,
                                                   grid_points=12001, comparison_grid_points=6001),
    }
    rows = {}
    for radius in (R_LCDM, 10.0, 13.5):
        values = {label: ls.lcdm_reference_linear_sigma(
            recipe=PLANCK_2018_QPLUS_RECIPE, early_spectrum=spec, radius_Mpc=radius,
            quadrature=q).linear_sigma for label, q in variants.items()}
        grid = rel(values["grid_16001"], values["reference"])
        krange = rel(values["k_range_1e-7_to_1e3"], values["reference"])
        gates["V4_quadrature_refinement_rel"].append(grid)
        gates["V4_quadrature_k_range_rel"].append(krange)
        rows[f"R={radius:.6f}"] = {**values, "grid_rel": grid, "k_range_rel": krange}
    return rows


def study_limits_and_invariances(gates):
    out = {"small_fv0": {}, "invariance": {}, "window": {}}
    for law, coefficient in (("meszaros", -0.75), ("comoving", -0.65)):
        _, closure, numerics = LAWS[law]
        rows = {}
        for fv0 in (1e-4, 1e-3, 1e-2):
            g = ls.timescape_growth_factor(params=TrackerParams.from_dressed_H0(fv0=fv0, H0=1.0),
                                           growth_law=CGI, closure=closure, numerics=numerics, G=G)
            ratio = g.log_growth_relative_to_volume_average_eds / fv0
            rows[f"{fv0:g}"] = {"log_growth_over_fv0": ratio, "first_order_coefficient": coefficient,
                                "gamma_w0": g.gamma_w0}
        gates["V5_small_fv0_first_order_coefficient_abs"].append(
            abs(rows["0.0001"]["log_growth_over_fv0"] - coefficient))
        out["small_fv0"][law] = rows
    base_params = TrackerParams.from_dressed_H0(fv0=0.737, H0=1.0)
    variants = {"gyr_73.03": (PAPER_REFERENCE.tracker_params_gyr, G),
                "km_s_Mpc_73.23": (TrackerParams.from_dressed_H0(fv0=0.737, H0=73.23), G),
                "H0_1_G_4.30091e-9": (base_params, 4.30091e-9)}
    for law, (growth_law, closure, numerics) in LAWS.items():
        base = ls.timescape_growth_factor(params=base_params, growth_law=growth_law, closure=closure,
                                          numerics=numerics, G=G).growth_today_photon_normalised
        rows = {}
        for label, (params, g_const) in variants.items():
            value = ls.timescape_growth_factor(params=params, growth_law=growth_law, closure=closure,
                                               numerics=numerics, G=g_const).growth_today_photon_normalised
            rows[label] = rel(value, base)
            gates["V5_H0_and_G_invariance_rel"].append(rows[label])
        out["invariance"][law] = rows
    threshold = ls.TOP_HAT_SERIES_THRESHOLD
    below = float(ls.top_hat_window(x=np.nextafter(threshold, 0.0)))
    above = float(ls.top_hat_window(x=threshold))
    out["window"] = {"series_threshold": threshold, "below": below, "above": above,
                     "continuity_rel": rel(below, above)}
    gates["V5_window_threshold_continuity_rel"].append(rel(below, above))
    return out


def study_fv0_scan():
    g_lcdm = ls.lcdm_reference_linear_sigma(
        recipe=PLANCK_2018_QPLUS_RECIPE, early_spectrum=early_spectrum(PRIMARY_FB), radius_Mpc=R_LCDM,
        quadrature=ls.LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE).growth_today_photon_normalised
    rows = []
    for fv0 in FV0_SCAN:
        params = TrackerParams.from_dressed_H0(fv0=fv0, H0=1.0)
        row = {"fv0": fv0}
        for law, (growth_law, closure, numerics) in LAWS.items():
            g = ls.timescape_growth_factor(params=params, growth_law=growth_law, closure=closure,
                                           numerics=numerics, G=G)
            row[f"X_{law}"] = g.growth_today_photon_normalised / g_lcdm
        rows.append(row)
    return {"g_lcdm_qplus0": g_lcdm, "rows": rows}


def study_inventory(inventory, growth, sigma, fv0_scan, gates):
    """Compare with the committed 1G-A inventory at its printed precision."""
    out = []

    def check(gate, label, ours, printed):
        diff = abs(ours - printed)
        gates[gate].append(diff)
        out.append({"quantity": label, "package": ours, "inventory": printed, "abs_diff": diff})

    gr = inventory["growth_ratio"]
    for name in ("PAPER_REFERENCE", "NW15_CMB_FIT"):
        for law in ("comoving", "meszaros"):
            printed = gr["cases"][name][law]
            ours = growth[name][law]
            check("V7_inventory_growth_six_decimals_abs", f"{name}/{law}/g_TS",
                  ours["growth_relative_to_volume_average_eds"], printed["g_TS_vs_volume_average_EdS"])
            x = sigma["cases"][name][law]["equal_mass"][f"{PRIMARY_FB:.4f}"]["growth_ratio"]
            check("V7_inventory_growth_six_decimals_abs", f"{name}/{law}/X_inf", x, printed["X_inf"])
        x_wall = sigma["cases"][name]["wall"]["equal_mass"][f"{PRIMARY_FB:.4f}"]["growth_ratio"]
        check("V7_inventory_growth_six_decimals_abs", f"{name}/wall/X_wall", x_wall,
              inventory["two_scale_bracket"]["cases"][name]["X_wall_regional"])
    check("V7_inventory_growth_six_decimals_abs", "g_Lambda_qplus0", fv0_scan["g_lcdm_qplus0"],
          gr["g_Lambda_qplus0"])
    printed_scan = {row["fv0"]: row for row in gr["fv0_scan"]}
    for row in fv0_scan["rows"]:
        for law in ("comoving", "meszaros"):
            check("V7_inventory_fv0_scan_four_decimals_abs", f"fv0={row['fv0']}/X_{law}",
                  row[f"X_{law}"], printed_scan[row["fv0"]][f"X_inf_{law}"])
    table = inventory["conditional_sigma_M8"]["cases"]
    for name in ("PAPER_REFERENCE", "NW15_CMB_FIT"):
        for law in ("comoving", "meszaros"):
            for conv, label in CONVENTIONS.items():
                printed = table[name][law][label]
                ours = sigma["cases"][name][law][conv][f"{PRIMARY_FB:.4f}"]
                radius = sigma["cases"][name][law]["_radius"][conv]["radius_Mpc"]
                check("V7_inventory_sigma_table_four_decimals_abs", f"{name}/{law}/{conv}/sigma",
                      ours["anchored_linear_sigma"], printed["sigma_planck_anchored_primary_fb"])
                check("V7_inventory_sigma_table_four_decimals_abs", f"{name}/{law}/{conv}/E",
                      ours["early_spectrum_factor"], printed["E"])
                check("V7_inventory_sigma_table_four_decimals_abs", f"{name}/{law}/{conv}/R_Mpc",
                      radius, printed["R_Mpc"])
        wall_printed = inventory["two_scale_bracket"]["cases"][name]["sigma_planck_anchored_by_convention"]
        for conv, label in CONVENTIONS.items():
            check("V7_inventory_sigma_table_four_decimals_abs", f"{name}/wall/{conv}/sigma",
                  sigma["cases"][name]["wall"][conv][f"{PRIMARY_FB:.4f}"]["anchored_linear_sigma"],
                  wall_printed[label])
    early = inventory["early_spectrum"]
    check("V7_inventory_sigma_table_four_decimals_abs", "lcdm_reference_sigma",
          sigma["lcdm_reference"]["linear_sigma"], early["eh98_planck_sigma8"])
    check("V7_inventory_sigma_table_four_decimals_abs", "lcdm_reference_offset",
          sigma["lcdm_reference"]["linear_sigma"] / ANCHOR - 1.0, early["eh98_planck_rel_to_anchor"])
    for name, printed in inventory["per_photon_matter_density"]["values"].items():
        ours = sigma["cases"][name]["comoving"]["_radius"]["equal_mass"]["omega_m_R_cubed_Mpc3"] / (
            sigma["cases"][name]["comoving"]["_radius"]["equal_mass"]["radius_Mpc"] ** 3)
        check("V7_inventory_per_photon_density_five_decimals_abs", f"{name}/omega_m_eff", ours, printed)
    return out


def main() -> int:
    gates = {name: [] for name in GATES}
    script = load_evidence_script()
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    cases = backgrounds()
    growth = study_growth(script, cases, gates)
    early_limit = study_early_limit(gates)
    sigma = study_sigma(script, cases, gates)
    quadrature = study_quadrature_refinement(gates)
    limits = study_limits_and_invariances(gates)
    fv0_scan = study_fv0_scan()
    inventory_rows = study_inventory(inventory, growth, sigma, fv0_scan, gates)

    gate_status = {}
    for name, bound in GATES.items():
        measured = max(gates[name]) if gates[name] else float("nan")
        gate_status[name] = {"gate": bound, "measured_max": measured, "evaluations": len(gates[name]),
                             "passed": bool(gates[name]) and measured <= bound}
    artifact = {
        "schema_version": 1,
        "title": "Phase 1G-B conditional mass-labelled linear sigma(M) validation",
        "status": {"classification": ls.SCIENTIFIC_CLASSIFICATION,
                   "observational": ls.OBSERVATIONAL_STATUS,
                   "amplitude_identity": ls.SIGMA8_STATUS,
                   "growth_rate_product": ls.FSIGMA8_STATUS,
                   "early_spectrum": ls.EARLY_SPECTRUM_IMPORT_STATUS,
                   "authorization_tokens_unchanged": all(
                       getattr(scientific_status, t) == "NOT_GRANTED"
                       for t in ("SIGMA8_AUTHORIZATION", "FSIGMA8_AUTHORIZATION",
                                 "OBSERVATIONAL_AUTHORIZATION", "UNIQUE_TIMESCAPE_PREDICTION"))},
        "provenance": {**git_state(), "python": platform.python_version(),
                       "numpy": version("numpy"), "scipy": version("scipy"),
                       "platform": platform.platform(),
                       "evidence_script": EVIDENCE_SCRIPT.relative_to(ROOT).as_posix(),
                       "inventory": INVENTORY.relative_to(ROOT).as_posix()},
        "inputs": {"G": G, "density_identity_tolerance": IDENTITY_RTOL,
                   "lcdm_recipe": {"omega_m": PLANCK_2018_QPLUS_RECIPE.omega_m,
                                   "h": PLANCK_2018_QPLUS_RECIPE.h},
                   "lcdm_radius_Mpc": R_LCDM, "lcdm_omega_m_h2": OMEGA_M_LCDM,
                   "baryon_fractions": list(BARYON_FRACTIONS), "primary_baryon_fraction": PRIMARY_FB,
                   "early_spectrum_primary": early_spectrum(PRIMARY_FB).to_metadata(),
                   "anchor": {"value": ANCHOR, "provenance": ANCHOR_PROVENANCE,
                              "tolerance": ANCHOR_TOLERANCE, "rationale": ANCHOR_RATIONALE},
                   "backgrounds": {k: v.to_metadata() for k, v in cases.items()},
                   "numerics": {"volume_average": ls.VOLUME_AVERAGE_GROWTH_REFERENCE_NUMERICS.to_metadata(),
                                "wall_regional": ls.WALL_REGIONAL_GROWTH_REFERENCE_CHECKS.to_metadata(),
                                "quadrature": ls.LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE.to_metadata()}},
        "V1_growth": growth,
        "V3_sigma": sigma,
        "V4_early_limit": early_limit,
        "V4_quadrature_refinement": quadrature,
        "V5_limits_and_invariances": limits,
        "fv0_scan": fv0_scan,
        "V7_inventory_comparison": inventory_rows,
        "gates": gate_status,
        "all_gates_passed": all(v["passed"] for v in gate_status.values()),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(artifact, indent=2, sort_keys=True, allow_nan=False) + "\n",
                      encoding="utf-8")
    print(f"written {OUTPUT.relative_to(ROOT)}")
    for name, status in gate_status.items():
        print(f"{name}: max {status['measured_max']:.3e} (n={status['evaluations']}) "
              f"gate {status['gate']:.1e} {'PASS' if status['passed'] else 'FAIL'}")
    return 0 if artifact["all_gates_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
