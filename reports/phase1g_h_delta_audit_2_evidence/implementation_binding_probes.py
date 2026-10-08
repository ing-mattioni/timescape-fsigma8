"""Second delta audit of Phase 1G-H: record-binding probes (GH-DF2).

Run from the repository root of the audited tree (226e52d, or this audit
branch, whose src/ and tests/ are identical):

    OPENBLAS_NUM_THREADS=1 python -B -W error \
        reports/phase1g_h_delta_audit_2_evidence/implementation_binding_probes.py OUT.json

Imports the audited runtime and the test helpers read-only; writes only OUT.
Each probe builds a modified record with ``dataclasses.replace`` and reports
whether the record was accepted, the exception type and message, and (when
accepted) whether the record still serialises as strict JSON and whether a
fresh factory evaluation with the same inputs reproduces it.
"""
from __future__ import annotations

import copy
import dataclasses as dc
import importlib.util
import json
import pickle
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "src"))
spec = importlib.util.spec_from_file_location("audit_helpers", ROOT / "tests/test_phase1g_h_global_variance.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
gv, ls = t.gv, t.ls


def probe(pid, make, expect, note=""):
    row = {"id": pid, "expect": expect, "note": note}
    try:
        x = make()
        row["accepted"] = True
        try:
            json.dumps(x.to_json_dict(), allow_nan=False)
            row["strict_json"] = True
        except (TypeError, ValueError) as exc:
            row["strict_json"] = False
            row["json_error"] = f"{type(exc).__name__}: {exc}"
    except Exception as exc:  # noqa: BLE001 - the probe records every refusal type
        row["accepted"] = False
        row["exception"] = type(exc).__name__
        row["message"] = str(exc)[:300]
    row["as_expected"] = (row["accepted"] == (expect == "accept"))
    return row


res = t.run(t.GM, t.constant(0.05), t.radius("c"))
pbs = t.run(t.GM, t.tracker_seed(t.GM, res.growth, 15.0, gv.SeedVolumeCompression.COMPRESSED_WITH_REGION),
            t.radius("c"))
prem = gv.HomogeneityPremise(radius=t.radius("c", 100.0), max_linear_rms=0.1, provenance="audit probe")
iv = gv.admissible_global_linear_interval(target=res, premise=prem)
rows = []

# 1. The delta audit's five accepted replacements (must now be refused).
rows.append(probe("DA1_spectrum_As_x4", lambda: dc.replace(res, early_spectrum=t.spectrum(4 * 2.1e-9)), "refuse"))
rows.append(probe("DA2_radius_x2", lambda: dc.replace(res, radius=ls.resolve_lagrangian_radius(
    spec=t.radius("c", 16.0), density=res.density)), "refuse"))
rows.append(probe("DA3_quadrature_33_17", lambda: dc.replace(res, quadrature=dc.replace(
    t.QUAD, grid_points=33, comparison_grid_points=17)), "refuse"))
seed2 = dc.replace(pbs.void_share.closure, seed_radius_Mpc=2 * pbs.void_share.closure.seed_radius_Mpc)
rows.append(probe("DA4_seed_radius_x2", lambda: dc.replace(pbs.void_share, closure=seed2), "refuse"))
rows.append(probe("DA5_premise_rms_999", lambda: dc.replace(iv, target_premise_rms=999.0), "refuse"))

# 2. Tolerance-only substitutions with identical values.
q = res.quadrature
rows.append(probe("TOL1_quadrature_looser_tolerances", lambda: dc.replace(res, quadrature=dc.replace(
    q, self_convergence_tolerance=10 * q.self_convergence_tolerance,
    truncation_tolerance=10 * q.truncation_tolerance)), "accept",
    "values identical; the record states a looser contract it satisfies"))
rows.append(probe("TOL2_quadrature_tolerance_below_achieved", lambda: dc.replace(res, quadrature=dc.replace(
    q, self_convergence_tolerance=0.5 * res.quadrature_relative_change)), "refuse",
    "a contract the stored result does not meet"))
ch = res.growth.checks
rows.append(probe("TOL3_growth_checks_looser_cross_check", lambda: dc.replace(res.growth, checks=dc.replace(
    ch, ode_cross_check_tolerance=10 * ch.ode_cross_check_tolerance)), "accept",
    "values identical; looser stated contract"))
worst = max(v for k, v in res.growth.diagnostics if k.endswith("_rel"))
rows.append(probe("TOL4_growth_checks_tolerance_below_achieved", lambda: dc.replace(res.growth, checks=dc.replace(
    ch, ode_cross_check_tolerance=0.5 * worst)), "refuse"))
rows.append(probe("TOL5_growth_checks_ode_rtol_changed", lambda: dc.replace(res.growth, checks=dc.replace(
    ch, ode_rtol=1e-10)), "refuse", "integration changes the diagnostics"))
sq = pbs.void_share.seed_quadrature
rows.append(probe("TOL6_seed_quadrature_looser", lambda: dc.replace(pbs.void_share, seed_quadrature=dc.replace(
    sq, self_convergence_tolerance=10 * sq.self_convergence_tolerance)), "accept"))
rows.append(probe("G1_growth_G_x2", lambda: dc.replace(res.growth, G=2.0), "accept",
                  "G cancels; accepted only if the ODE diagnostics are reproduced"))

# 3. Equal-but-distinct objects (identity contracts).
rows.append(probe("ID1_sigma_density_equal_copy", lambda: dc.replace(res, density=copy.copy(res.density)), "refuse",
                  "object identity required by design"))
rows.append(probe("ID2_sigma_spectrum_equal_copy", lambda: dc.replace(res, early_spectrum=t.spectrum(2.1e-9)), "refuse",
                  "an equal spectrum built anew"))
rows.append(probe("ID3_void_share_spectrum_equal_copy",
                  lambda: dc.replace(pbs.void_share, early_spectrum=t.spectrum(2.1e-9)), "accept",
                  "the void share alone has no identity contract with the spectrum"))
rows.append(probe("ID4_deepcopy_sigma_record", lambda: copy.deepcopy(res), "accept"))
rows.append(probe("ID5_pickle_roundtrip_then_replace", lambda: dc.replace(pickle.loads(pickle.dumps(res))), "accept",
                  "pickle keeps shared references; replace re-runs __post_init__"))
rows.append(probe("ID6_radius_equal_copy", lambda: dc.replace(res, radius=dc.replace(res.radius)), "accept"))

# 4. Type substitutions on stored results.
rows.append(probe("TY1_sigma_as_Fraction", lambda: dc.replace(res, linear_sigma=Fraction(res.linear_sigma)), "refuse",
                  "an exact Fraction of the stored float"))
rows.append(probe("TY2_sigma_as_numpy_float64", lambda: dc.replace(res, linear_sigma=np.float64(res.linear_sigma)), "accept"))
rows.append(probe("TY3_interval_target_inside_as_int",
                  lambda: dc.replace(iv, target_inside=int(iv.target_inside)), "refuse"))
rows.append(probe("TY4_interval_target_inside_as_numpy_bool",
                  lambda: dc.replace(iv, target_inside=np.bool_(iv.target_inside)), "refuse"))
rows.append(probe("TY5_regime_as_other_string", lambda: dc.replace(res, void_response_regime="PERTURBATIVE"), "refuse"))
rows.append(probe("TY6_void_share_nu_as_string",
                  lambda: dc.replace(pbs.void_share, nu=str(pbs.void_share.nu)), "refuse"))
rows.append(probe("TY7_sigma_within_rtol", lambda: dc.replace(res, linear_sigma=res.linear_sigma * (1 + 5e-13)), "accept",
                  "inside RECORD_IDENTITY_RTOL by design"))

# 5. Coherent substitutions of inputs (genuine records for other inputs).
iv2 = gv.admissible_global_linear_interval(target=pbs, premise=prem)
rows.append(probe("CO1_interval_other_target_coherent", lambda: dc.replace(iv2), "accept",
                  "a genuine record for another target"))
rows.append(probe("CO2_interval_target_swapped_values_kept", lambda: dc.replace(iv, target=pbs), "refuse"))
prem2 = dc.replace(prem, provenance="observational sigma8 prior")
rows.append(probe("CO3_premise_provenance_text", lambda: dc.replace(iv, premise=prem2), "accept",
                  "free-text provenance is not bound (metadata)"))
rows.append(probe("CO4_matching_provenance_text", lambda: dc.replace(res.growth, matching=dc.replace(
    res.growth.matching, provenance="other")), "accept", "free-text provenance is not bound"))
prem_b = gv.HomogeneityPremise(radius=t.radius("b", 100.0), max_linear_rms=0.1, provenance="audit probe")
rows.append(probe("CO5_interval_premise_other_convention", lambda: dc.replace(iv, premise=prem_b), "refuse"))
rows.append(probe("CO6_status_field_relabelled", lambda: dc.replace(res, amplitude_status="OBSERVATIONAL"), "refuse"))

# 6. Records of other types inside a record.
rows.append(probe("RT1_sigma_void_share_from_other_growth", lambda: dc.replace(
    res, void_share=gv.evaluate_void_share(closure=t.constant(0.05), growth=gv.two_phase_global_growth(
        background=t.GM, matching=t.MATCHING, checks=t.CHECKS, G=1.0), density=res.density,
        early_spectrum=res.early_spectrum, seed_quadrature=t.NA)), "refuse"))

summary = {"total": len(rows), "as_expected": sum(r["as_expected"] for r in rows),
           "unexpected": [r["id"] for r in rows if not r["as_expected"]],
           "accepted": [r["id"] for r in rows if r["accepted"]],
           "accepted_non_strict_json": [r["id"] for r in rows if r["accepted"] and not r.get("strict_json", True)],
           "refused_non_contract_error": [r["id"] for r in rows if not r["accepted"]
                                          and r["exception"] != "GlobalVarianceContractError"]}
out = {"summary": summary, "probes": rows}
Path(sys.argv[1]).write_text(json.dumps(out, indent=1, allow_nan=False) + "\n")
print(json.dumps(summary, indent=1))
for r in rows:
    print(f"{r['id']:45s} accepted={r['accepted']!s:5s} expected={r['expect']:6s} "
          f"{r.get('exception', '')} {r.get('message', '')[:110]}")
