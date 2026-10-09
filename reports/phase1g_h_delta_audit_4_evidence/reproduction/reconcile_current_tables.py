"""Mechanically reconcile current 1G-H report tables with regenerated evidence.

The explicit row/column maps below preserve semantic labels. No value is
matched by numerical proximity. Tolerances are half a last printed digit
(absolute floor 2e-12); recorded zero cross terms use the absolute floor.
"""
import collections
import decimal
import json
from pathlib import Path
import re
import sys

ROOT, WORK = map(Path, sys.argv[1:3])
report = ROOT / "reports/phase1g_h_global_variance_closure.md"
lines = report.read_text().splitlines()
old_lines = (ROOT.parent / "baseline/reports/phase1g_h_global_variance_closure.md").read_text().splitlines()
line_map = {}
# Fourth audit: unchanged prior semantic maps; current table rows must match exact baseline bytes.
art = json.loads((WORK / "evidence_main_py313.json").read_text())
CASE = ("PAPER_REFERENCE", "NW15_CMB_FIT")
CONV = ("c_bare_volume_average", "a_equal_mass", "b_dressed_wall_comoving")
rows = []
sup = str.maketrans("⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "-0123456789")


def tokens(s):
    s = s.replace("−", "-")
    return re.findall(r"[+-]?\d+(?:\.\d+)?(?:×10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)?", s)


def check(token, actual, label, lineno, artifact_path):
    lineno = line_map.get(lineno, lineno)
    normalized = token.translate(sup).replace("×10", "e")
    d = decimal.Decimal(normalized)
    printed = float(d)
    tolerance = max(2e-12, 0.5 * 10.0 ** d.as_tuple().exponent) if printed else 2e-12
    rows.append({"claim_id": f"GH-D4T{len(rows)+1:04d}", "claim": label,
                 "source": str(report.relative_to(ROOT)), "line": lineno,
                 "printed_text": token, "declared_value": printed,
                 "audit_value": actual, "artifact_path": artifact_path,
                 "tolerance": {"absolute": tolerance, "relative": 0},
                 "status": "VERIFIED" if abs(actual-printed) <= tolerance else "REFUTED",
                 "method": "EXPLICIT_REPORT_TABLE_ROW_COLUMN_TO_ARTIFACT_PATH"})


def cell(index, column):
    candidates = [i+1 for i,row in enumerate(lines) if row == old_lines[index-1]]
    if not candidates: raise ValueError(f"current report lacks exact baseline table row {index}")
    line_map[index] = candidates[0]
    return lines[candidates[0]-1].strip().strip("|").split("|")[column].strip()


def checks(index, column, actuals, label, paths):
    ts = tokens(cell(index, column))
    if len(ts) != len(actuals):
        raise ValueError(f"{index}:{column} tokens {ts} vs {len(actuals)}")
    for t, a, p in zip(ts, actuals, paths):
        check(t, a, label, index, p)


# Table 3.2: tracker quantities, including scientific notation.
for line, case in ((419, CASE[0]), (420, CASE[1])):
    g = art["cases"][case]["growth"]
    for col, field in enumerate(("fv0", "t_ls_over_t0", "f_v_ls", "gamma_w_ls", "wall_share_growth", "void_share_growth", "void_to_wall_growth_ratio"), 1):
        checks(line, col, [g[field]], case + " tracker " + field, [f"cases/{case}/growth/{field}"])

# Table 4.2: each supplied seed-size sensitivity is a distinct explicit input.
for line, seed in ((518, "tracker_seed_F_median"), (519, "tracker_seed_W09_7.5"),
                   (520, "tracker_seed_W09_15"), (521, "tracker_seed_W09_30"), (522, "svdw04_factor_1.72")):
    for ci, case in enumerate(CASE):
        x = art["cases"][case]["seed_radius_sensitivity"][seed]
        for off, f in enumerate(("R_s_Mpc", "share_k0", "linear_sigma_direct_A_s", "void_volume_response_rms")):
            checks(line, 1+4*ci+off, [x[f]], case + " seed " + seed + " " + f,
                   [f"cases/{case}/seed_radius_sensitivity/{seed}/{f}"])

# Table 5.1: six radius/scenario combinations, direct then post-hoc values.
closure_map = {587: "wall_mode_p0", 588: "monotone_lower_p_fvLS", 589: "pbs_tracker_seed_F_median_compressed",
               590: "pbs_tracker_seed_compressed", 591: "pbs_svdw04_seed_compressed", 593: "strict_flat_walls_p1"}
for column, (case, conv) in enumerate(((c, v) for c in CASE for v in CONV), 1):
    x = art["cases"][case]["conventions"][conv]["closures"]
    checks(586, column, [x["wall_mode_p0"]["unit_growth_sigma"]], case + " " + conv + " unit growth",
           [f"cases/{case}/conventions/{conv}/closures/wall_mode_p0/unit_growth_sigma"])
    for line, key in closure_map.items():
        fields = ["linear_sigma_direct_A_s"] if line == 593 else ["linear_sigma_direct_A_s", "linear_sigma_planck_anchored"]
        checks(line, column, [x[key][f] for f in fields], case + " " + conv + " " + key,
               [f"cases/{case}/conventions/{conv}/closures/{key}/{f}" for f in fields])
for column, case in ((1, CASE[0]), (4, CASE[1])):
    checks(592, column, [art["cases"][case]["m3_two_barrier_alternative"]["compressed_with_long_mode"]["linear_sigma_direct_A_s"]],
           case + " M3 compressed", [f"cases/{case}/m3_two_barrier_alternative/compressed_with_long_mode/linear_sigma_direct_A_s"])
for column in (2, 5):
    checks(594, column, [art["anchoring"]["anchor"]], "Planck external anchor", ["anchoring/anchor"])

# Table 5.2: four explicit homogeneity premise readings.
for line, key in ((628, "W09_10pct_at_100"), (629, "W09_10pct_at_150"),
                   (630, "W09_several_pct_6pct_at_100"), (631, "cell_side_100_as_sphere_62")):
    for ci, case in enumerate(CASE):
        x = art["cases"][case]["conventions"][CONV[0]]["intervals"][key]
        p = f"cases/{case}/conventions/{CONV[0]}/intervals/{key}"
        checks(line, 1+3*ci, [x["lower"], x["upper"]], case + " interval " + key, [p+"/lower", p+"/upper"])
        checks(line, 2+3*ci, [x["share_upper"]], case + " maximum share " + key, [p+"/share_upper"])
        if line == 628:
            checks(line, 3+3*ci, [x["target_premise_rms"]], case + " target premise rms", [p+"/target_premise_rms"])

# Table 5.3: complete six-point radius scan for the two selected closures.
for line, case, key in ((676, CASE[0], "monotone_lower_p_fvLS"), (677, CASE[0], "pbs_tracker_seed_compressed"),
                        (678, CASE[1], "monotone_lower_p_fvLS"), (679, CASE[1], "pbs_tracker_seed_compressed")):
    x = art["cases"][case]["conventions"][CONV[0]]["radius_scan"]
    for i in range(6):
        checks(line, 1+i, [x[i][key]], case + " radius scan " + key,
               [f"cases/{case}/conventions/{CONV[0]}/radius_scan/{i}/{key}"])

# Table 5.4: rescaled-spectrum reclosure beside direct and fixed-closure normalisation.
for line, key in ((723, "pbs_tracker_seed_compressed"), (724, "pbs_tracker_seed_F_median_compressed"), (725, "monotone_lower_p_fvLS")):
    for col, (case, conv) in enumerate(((CASE[0], CONV[0]), (CASE[1], CONV[0]), (CASE[0], CONV[1]), (CASE[1], CONV[1])), 1):
        x = art["cases"][case]["conventions"][conv]["pbs_reclosure_under_spectrum_rescaling"][key]
        fs = ("direct", "post_hoc_fixed_closure", "reclosure")
        checks(line, col, [x[f] for f in fs], case + " " + conv + " rescaling " + key,
               [f"cases/{case}/conventions/{conv}/pbs_reclosure_under_spectrum_rescaling/{key}/{f}" for f in fs])

# Table 6.3: both Gaussian signed laws and both-walls covariance.
for line, case in ((861, CASE[0]), (862, CASE[1])):
    x = art["two_phase_covariance"][case]["gaussian_threshold_pair"]
    p = f"two_phase_covariance/{case}/gaussian_threshold_pair"
    checks(line, 1, [x["partition_smoothing_ell_Mpc"]], case + " partition smoothing", [p+"/partition_smoothing_ell_Mpc"])
    for col, law in ((2, "I_independent"), (3, "II_same_field")):
        fs = ("sigma_partition", "sigma_wall_field", "cross_term", "sigma_total")
        checks(line, col, [x["laws"][law][f] for f in fs], case + " signed " + law,
               [p+f"/laws/{law}/{f}" for f in fs])
    checks(line, 4, [x["laws"][law]["both_walls_product_moment_excess_ball"] for law in ("I_independent", "II_same_field")],
           case + " signed both-walls covariance", [p+f"/laws/{law}/both_walls_product_moment_excess_ball" for law in ("I_independent", "II_same_field")])

# Six-member nonnegative lognormal comparison, every numeric data cell.
for line, case, rs in ((895,CASE[0],1),(896,CASE[0],2),(897,CASE[0],4),(898,CASE[1],1),(899,CASE[1],2),(900,CASE[1],4)):
    x = art["two_phase_covariance"][case]["gaussian_threshold_pair"]["nonnegative_lognormal_pair"]["members"][f"r_s_{rs}_Mpc"]
    p = f"two_phase_covariance/{case}/gaussian_threshold_pair/nonnegative_lognormal_pair/members/r_s_{rs}_Mpc"
    for col, f in ((1,"resolution_radius_Mpc"),(2,"latent_point_variance"),(3,"density_point_variance"),(4,"conditional_normaliser_ratio_m_II"),(8,"sigma_ratio_II_over_I")):
        checks(line,col,[x[f]],case+" lognormal rs="+str(rs)+" "+f,[p+"/"+f])
    for col, law, fs in ((5,"I_independent",("sigma_wall_field","sigma_total")),(6,"II_same_field",("sigma_wall_field","cross_term","sigma_total"))):
        checks(line,col,[x["laws"][law][f] for f in fs],case+" lognormal rs="+str(rs)+" "+law,[p+f"/laws/{law}/{f}" for f in fs])
    checks(line,7,[x["laws"][law]["both_walls_product_moment_excess_ball"] for law in ("I_independent","II_same_field")],case+" lognormal both-walls covariance",[p+f"/laws/{law}/both_walls_product_moment_excess_ball" for law in ("I_independent","II_same_field")])

out = {"claims": rows, "claim_counts": dict(collections.Counter(r["status"] for r in rows)),
       "deviations": [r for r in rows if r["status"] != "VERIFIED"],
       "scope": "All numeric data cells in current report Tables3.2,4.2,5.1,5.2,5.3,5.4,6.3signed,6.3lognormal; source hashes and historical reference/context tables separately reconciled."}
(WORK/"current_report_tables.json").write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+"\n")
print(json.dumps({k:v for k,v in out.items() if k!='claims'},indent=2))
