"""Third delta audit: exact numerical and metadata regression reconciliation.

Mechanical verification is deliberately unblinded. Science reconstruction is
owned separately. Paths are explicit; environment metadata and figures are
excluded only where the comparison contract expressly allows it.
"""
import collections
import decimal
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
OLDROOT = ROOT.parent / "repro_248a06b"


def read(p):
    def unique(items):
        d = {}
        for k, v in items:
            if k in d:
                raise ValueError(f"duplicate key {k} in {p}")
            d[k] = v
        return d
    return json.loads(Path(p).read_text(), object_pairs_hook=unique)


def flat(x, path=()):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from flat(v, path + (k,))
    elif isinstance(x, list):
        for k, v in enumerate(x):
            yield from flat(v, path + (str(k),))
    else:
        yield "/".join(path), x


def number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def compare(a, b, exclude=("environment", "figures"), remap_h25=False):
    def leaves(x):
        d = {}
        for p, v in flat(x):
            if p.split("/")[0] in exclude:
                continue
            if remap_h25 and p.startswith("gates/physics/") and "(H25)" in p:
                p = p.replace("gates/physics/", "gates/numerics/", 1)
            d[p] = v
        return d
    aa, bb = leaves(a), leaves(b)
    nums, other, diffs = 0, 0, []
    for p in sorted(aa.keys() & bb.keys()):
        x, y = aa[p], bb[p]
        numeric = number(x) and number(y)
        nums += numeric
        if x != y:
            diffs.append({"path": p, "old": x, "new": y,
                          "kind": "numeric" if numeric else "other",
                          "absolute": abs(x-y) if numeric else None,
                          "relative": abs(x-y) / max(abs(x), abs(y)) if numeric and (x or y) else 0.0})
            other += not numeric
    numeric_diffs = [d for d in diffs if d["kind"] == "numeric"]
    return {"common_leaves": len(aa.keys() & bb.keys()),
            "common_numeric_leaves": nums,
            "numeric_changed": len(numeric_diffs), "other_changed": other,
            "max_absolute": max((d["absolute"] for d in numeric_diffs), default=0.0),
            "max_relative": max((d["relative"] for d in numeric_diffs), default=0.0),
            "differences": diffs,
            "only_old": sorted(aa.keys() - bb.keys()),
            "only_new": sorted(bb.keys() - aa.keys())}


def recount(a, b):
    aa = {p: v for p, v in flat(a) if p.split("/")[0] not in ("environment", "figures")}
    bb = {p: v for p, v in flat(b) if p.split("/")[0] not in ("environment", "figures")}
    out = {}
    def inside(p):
        return p.startswith("two_phase_covariance/") and "/gaussian_threshold_pair/" in p
    for label, selected in (("inside", inside), ("outside", lambda p: not inside(p))):
        common = sorted(p for p in aa.keys() & bb.keys() if selected(p))
        numeric_diffs = [(p, aa[p], bb[p]) for p in common if number(aa[p]) and number(bb[p]) and aa[p] != bb[p]]
        beyond = [d for d in numeric_diffs if abs(d[1]-d[2]) / max(abs(d[1]), abs(d[2])) > 1e-12]
        text = [p for p in common if not (number(aa[p]) and number(bb[p])) and aa[p] != bb[p]]
        out[label] = {"common": len(common), "numeric_changed": len(numeric_diffs),
                      "numeric_changed_beyond_1e-12_rel": len(beyond),
                      "text_changed": len(text),
                      "max_abs_numeric_change": max((abs(x-y) for _, x, y in numeric_diffs), default=0.0),
                      "only_old": sum(selected(p) for p in aa.keys() - bb.keys()),
                      "only_new": sum(selected(p) for p in bb.keys() - aa.keys())}
    return out


new = read(WORK / "evidence_py312_ed0ec0c.json")
other = read(WORK / "evidence_py311_ed0ec0c.json")
old = read(OLDROOT / "artifacts/independent/phase1g_h_global_variance_closure.json")
delta_saved = read(ROOT / "reports/phase1g_h_delta_audit_evidence/evidence_py312.json")
claims = []


def claim(description, expected, actual, tolerance=0.0, method="MECHANICAL_REPRODUCTION", location=None):
    if number(expected) and number(actual):
        ok = abs(actual - expected) <= tolerance
    else:
        ok = actual == expected
    claims.append({"claim_id": f"GH-D3N{len(claims)+1:04d}", "claim": description,
                   "declared_value": expected, "audit_value": actual,
                   "status": "VERIFIED" if ok else "REFUTED", "method": method,
                   "tolerance": {"absolute": tolerance, "relative": 0}, "location": location})


comparisons = {"cross_interpreter": compare(new, other),
               "same_interpreter_248a06b_vs_ed0ec0c": compare(old, new),
               "same_interpreter_after_H25_path_move": compare(old, new, remap_h25=True),
               "saved_delta_89cb041_vs_248a06b": compare(delta_saved, old)}
for name, c in comparisons.items():
    for p, v in c.items():
        if p in ("numeric_changed", "other_changed") and name != "saved_delta_89cb041_vs_248a06b":
            claim(name + " " + p, 0, v)
    if name == "same_interpreter_after_H25_path_move":
        claim(name + " only_old", [], c["only_old"])
        claim(name + " only_new", [], c["only_new"])

recounted = recount(delta_saved, old)
declared_recount = read(ROOT / "reports/phase1g_h_delta_audit_2_remediation_logs/regression_recount_89cb041_vs_248a06b.json")
for region, vals in recounted.items():
    for k, v in vals.items():
        claim("GH-D2E1 recount " + region + "/" + k, declared_recount[region][k], v,
              method="INDEPENDENT_FLATTEN_RECOUNT", location="reports/phase1g_h_delta_audit_2_remediation_logs/regression_recount_89cb041_vs_248a06b.json")

inv = read(ROOT / "reports/phase1g_h_global_variance_closure_inventory.json")
art_flat = {}
for k, a in (("results", new["cases"]), ("anchoring", new["anchoring"]),
             ("two_phase_covariance", new["two_phase_covariance"]),
             ("ensemble_vs_tangent_example", new["ensemble_vs_tangent_example"])):
    art_flat.update(flat(a, (k,)))
rules = [
    ("/a_s_scaling_pbs_tracker_seed/", "/a_s_scaling/pbs_tracker_seed_compressed/"),
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
unmatched = []
inventory_rows = []
for key in ("results", "anchoring", "two_phase_covariance", "ensemble_vs_tangent_example"):
    for p, declared in flat(inv[key], (key,)):
        if not number(declared):
            continue
        translated = "/" + p
        for a, b in rules:
            translated = translated.replace(a, b)
        if "/step_share_counterexample/" in translated:
            translated = translated.replace("/premise_radius/radius_Mpc", "/premise_radius_Mpc")
        translated = translated.replace("/nonnegative_lognormal_pair/linear_limit_max_rel_difference", "/nonnegative_lognormal_pair/linear_limit/max_wall_moment_rel_difference").lstrip("/")
        translated = translated.replace("/radial_quadrature/h25_identity_max_rel", "/gaussian_threshold_pair/h25_identity_max_rel")
        translated = translated.replace("/radial_quadrature/intervals", "/gaussian_threshold_pair/radial_intervals")
        translated = translated.replace("/radial_quadrature/refinement_max_rel_vs_half", "/gaussian_threshold_pair/radial_refinement_max_rel")
        if translated not in art_flat:
            unmatched.append(p)
            continue
        actual = art_flat[translated]
        tol = max(2e-12, 0.5 * 10.0 ** decimal.Decimal(str(declared)).as_tuple().exponent)
        claim("1G-H inventory rounded scalar " + p, declared, actual, tol,
              "EXPLICIT_SEMANTIC_PATH_MAPPING_HALF_LAST_DIGIT", "reports/phase1g_h_global_variance_closure_inventory.json/" + p)
        inventory_rows.append({"path": p, "artifact_path": translated, "declared": declared,
                               "actual": actual, "abs_difference": abs(actual-declared), "abs_tolerance": tol,
                               "pass": abs(actual-declared) <= tol})

gates = {}
for group, gg in new["gates"].items():
    gates[group] = {"count": len(gg), "passed": sum(g["pass"] for g in gg.values())}
    for name, row in gg.items():
        claim("1G-H gate " + group + "/" + name, True, row["pass"], row["limit"],
              "SAME_CODE_EXPLICIT_GATE", "gates/" + group + "/" + name)
claim("total gates", 36, sum(g["count"] for g in gates.values()))
for group, count in (("numerics", 10), ("physics", 20), ("reproduction", 6)):
    claim("gate block " + group, count, gates[group]["count"])
claim("cross interpreter numeric leaves", 3201, comparisons["cross_interpreter"]["common_numeric_leaves"])
claim("same interpreter numeric common leaves", 3197, comparisons["same_interpreter_248a06b_vs_ed0ec0c"]["common_numeric_leaves"])

hash_rows = []
rem = read(ROOT / "reports/phase1g_h_delta_audit_2_remediation_inventory.json")
for source, files in (("1G-H inventory files.added", inv["files"]["added"]),
                      ("third-remediation files_changed_sha256", rem["files_changed_sha256"])):
    for p, expected in files.items():
        actual = hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
        claim(source + " " + p, expected, actual, method="SHA256", location=p)
        hash_rows.append({"inventory": source, "path": p, "declared": expected, "actual": actual, "pass": expected == actual})

figure_rows = []
for p in sorted((ROOT / "artifacts/independent/phase1g_h").glob("*.png")):
    oldp = OLDROOT / "artifacts/independent/phase1g_h" / p.name
    a, b = hashlib.sha256(oldp.read_bytes()).hexdigest(), hashlib.sha256(p.read_bytes()).hexdigest()
    claim("figure old/new identical " + p.name, a, b, method="SHA256", location=str(p.relative_to(ROOT)))
    figure_rows.append({"name": p.name, "old_sha256": a, "new_sha256": b, "identical": a == b})

out = {"comparisons": comparisons, "recount": recounted,
       "inventory_rounding": {"matched": len(inventory_rows), "rows": inventory_rows, "unmatched": unmatched,
                              "deviations": [r for r in inventory_rows if not r["pass"]]},
       "gates": gates, "hashes": hash_rows, "figures": figure_rows,
       "artifact_hashes": {k: hashlib.sha256(p.read_bytes()).hexdigest() for k, p in
                           (("py312_ed0ec0c", WORK / "evidence_py312_ed0ec0c.json"),
                            ("py311_ed0ec0c", WORK / "evidence_py311_ed0ec0c.json"),
                            ("py312_248a06b", OLDROOT / "artifacts/independent/phase1g_h_global_variance_closure.json"))},
       "claims": claims, "claim_counts": dict(collections.Counter(c["status"] for c in claims)),
       "method": {"numeric_comparison": "exact parsed numeric equality; booleans excluded; environment excluded; figure hash separately",
                  "rounding": "half-unit of represented inventory precision, minimum abs tolerance 2e-12",
                  "regression_recount_threshold": "relative difference > 1e-12 using max(abs(old),abs(new))",
                  "historical_logs": "recorded prior environment/duration claims cannot be reproduced as present execution; compare semantic result summaries"}}
(WORK / "reproduction_comparisons.json").write_text(json.dumps(out, indent=2, sort_keys=True, allow_nan=False) + "\n")
print(json.dumps({"claim_counts": out["claim_counts"], "matched_inventory": len(inventory_rows),
                  "unmatched": unmatched, "deviations": out["inventory_rounding"]["deviations"],
                  "comparisons": {k: {q: v for q, v in r.items() if q not in ("differences", "only_old", "only_new")} for k, r in comparisons.items()},
                  "gates": gates, "figures": figure_rows}, indent=2))
