"""Second delta audit: inventory numbers of the 1G-H closure vs the regenerated artifact.

    python -B inventory_reconciliation.py INVENTORY.json ARTIFACT.json OUT.json

The path translation rules are those of the delta audit's reconcile_delta.py
(reused, documented), extended for the keys added on 2026-10-08.  Every numeric
leaf of the inventory blocks results / anchoring / two_phase_covariance /
ensemble_vs_tangent_example is compared with its artifact counterpart within
half a unit of its last printed digit (floor 2e-12).
"""
import decimal
import json
import sys


def flat(x, p=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from flat(v, p + "/" + str(k))
    elif isinstance(x, list):
        for k, v in enumerate(x):
            yield from flat(v, p + "/" + str(k))
    else:
        yield p, x


inv = json.load(open(sys.argv[1]))
art = json.load(open(sys.argv[2]))
mapped = {}
for key, x in (("results", art["cases"]), ("anchoring", art["anchoring"]),
               ("two_phase_covariance", art["two_phase_covariance"]),
               ("ensemble_vs_tangent_example", art["ensemble_vs_tangent_example"])):
    for p, v in flat(x, "/" + key):
        mapped[p] = v
RULES = [("/a_s_scaling_pbs_tracker_seed/", "/a_s_scaling/pbs_tracker_seed_compressed/"),
         ("/refined_quadrature_linear_sigma_c_pbs", "/refined_quadrature_linear_sigma"),
         ("/premise_max_linear_rms", "/premise/max_linear_rms"),
         ("/premise_radius_Mpc", "/premise_radius/radius_Mpc"),
         ("/primary_rms_at_premise", "/target_premise_rms"),
         ("/linear_sigma_c_direct", "/linear_sigma_direct_A_s"),
         ("/E_reference_reproduction/", "/E_reference/"),
         ("/ell_Mpc", "/partition_smoothing_ell_Mpc"),
         ("/linear_sigma_post_hoc_normalised", "/linear_sigma_planck_anchored"),
         ("/lower_post_hoc_withdrawn", "/lower_anchored"), ("/upper_post_hoc_withdrawn", "/upper_anchored"),
         ("/normalisation_variants/", "/pbs_reclosure_under_spectrum_rescaling/"),
         ("/nonnegative_lognormal_pairs/", "/gaussian_threshold_pair/nonnegative_lognormal_pair/"),
         ("/signed_gaussian_pair/", "/gaussian_threshold_pair/"),
         ("/scale_separation_convention_c/", "/scale_separation/")]
rows, unmatched = [], []
for key in ("results", "anchoring", "two_phase_covariance", "ensemble_vs_tangent_example"):
    for p, v in flat(inv[key], "/" + key):
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            continue
        pp = p
        for a, b in RULES:
            pp = pp.replace(a, b)
        if "/step_share_counterexample/" in pp:
            pp = pp.replace("/premise_radius/radius_Mpc", "/premise_radius_Mpc")
        pp = pp.replace("/nonnegative_lognormal_pair/linear_limit_max_rel_difference",
                        "/nonnegative_lognormal_pair/linear_limit/max_wall_moment_rel_difference")
        if pp not in mapped or not isinstance(mapped[pp], (int, float)):
            unmatched.append(p)
            continue
        actual = mapped[pp]
        tol = max(2e-12, 0.5 * 10 ** decimal.Decimal(str(v)).as_tuple().exponent)
        rows.append({"path": p, "declared": v, "actual": actual, "tolerance": tol, "pass": abs(v - actual) <= tol})
out = {"matched": len(rows), "passed": sum(r["pass"] for r in rows),
       "deviations": [r for r in rows if not r["pass"]], "unmatched": unmatched}
json.dump(out, open(sys.argv[3], "w"), indent=1)
print(json.dumps({k: (v if k != "unmatched" else len(v)) for k, v in out.items() if k != "deviations"}),
      "deviations:", out["deviations"][:10])
print("unmatched:", unmatched)
