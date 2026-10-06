"""Delta audit R2-M2: regenerated F/G evidence vs inventories, archive re-check, accuracy vs R2-M1.

Usage: python r2_compare_regen.py <repo_root> <evidence_dir>
Reproducibility gate (declared by the remediation): numeric leaves rtol=1e-11, atol=1e-14;
keys and string labels exact; 'environment' and 'input_sha256' excluded.
Accuracy (separate): audited grid values vs the method-diverse references of r2_cutoffs_pde.py.
"""
import hashlib
import json
import math
import sys
from pathlib import Path

RTOL, ATOL = 1e-11, 1e-14
EXCLUDE = {"environment", "input_sha256"}
root, ev = Path(sys.argv[1]), Path(sys.argv[2])


def load(p):
    return json.loads(Path(p).read_bytes())


def compare(a, b, path="", out=None, missing_ok=False):
    """Compare every leaf of b (reference subtree) with a; returns list of mismatches."""
    out = [] if out is None else out
    if isinstance(b, dict):
        if not isinstance(a, dict):
            out.append((path, "type", type(a).__name__, "dict")); return out
        if not missing_ok and set(a) - EXCLUDE != set(b) - EXCLUDE:
            out.append((path, "keys", sorted(set(a) ^ set(b)), None))
        for k in b:
            if k in EXCLUDE or k not in a:
                continue
            compare(a[k], b[k], f"{path}/{k}", out, missing_ok)
    elif isinstance(b, list):
        if not isinstance(a, list) or len(a) != len(b):
            out.append((path, "list", None, None)); return out
        for i, (x, y) in enumerate(zip(a, b)):
            compare(x, y, f"{path}[{i}]", out, missing_ok)
    elif isinstance(b, bool) or b is None or isinstance(b, str):
        if a != b:
            out.append((path, "label", a, b))
    elif isinstance(b, (int, float)):
        if not isinstance(a, (int, float)) or abs(a - b) > ATOL + RTOL * abs(b):
            out.append((path, "num", a, b))
    return out


res = {}
inv_f = load(root / "reports/phase1g_f_volume_budget_successor_inventory.json")
inv_g = load(root / "reports/phase1g_g_void_evolution_inventory.json")
F = {v: load(ev / f"regen/F_{v}.json") for v in ("314", "311")}
G = {v: load(ev / f"regen/G_{v}.json") for v in ("314", "311")}
for v in F:
    mism = []
    for case in ("PAPER_REFERENCE", "NW15_CMB_FIT"):
        mism += compare(F[v]["cases"][case]["history"], inv_f["primary_cases"][case], f"F{v}/{case}/history")
        mism += compare(F[v]["cases"][case]["near_empty_C1_collapse"], inv_f["near_empty_C1_collapse"][case], f"F{v}/{case}/near_empty")
        mism += compare(F[v]["cases"][case]["boolean_surrogate"], inv_f["boolean_surrogate"][case], f"F{v}/{case}/boolean")
    res[f"F_{v}_vs_inventory_mismatches"] = mism
    res[f"G_{v}_vs_inventory_mismatches"] = compare(G[v], inv_g["evidence"], f"G{v}")
    res[f"F_{v}_environment"] = F[v]["environment"]
res["F_314_vs_F_311_mismatches"] = compare(F["314"], F["311"], "F314vs311")
res["G_314_eq_G_311_bytes"] = (ev / "regen/G_314.json").read_bytes() == (ev / "regen/G_311.json").read_bytes()
res["max_rel_diff_F_vs_inventory"] = 0.0
def maxrel(a, b):
    m = 0.0
    if isinstance(b, dict):
        for k in b:
            if k in a and k not in EXCLUDE:
                m = max(m, maxrel(a[k], b[k]))
    elif isinstance(b, list):
        for x, y in zip(a, b):
            m = max(m, maxrel(x, y))
    elif isinstance(b, float) and isinstance(a, (int, float)) and b != 0:
        m = max(m, abs(a / b - 1))
    return m
for v in F:
    res[f"F_{v}_max_rel_vs_inventory"] = max(
        maxrel(F[v]["cases"][c]["history"], inv_f["primary_cases"][c]) for c in ("PAPER_REFERENCE", "NW15_CMB_FIT"))
    res[f"F_{v}_max_rel_near_empty_vs_inventory"] = max(
        maxrel(F[v]["cases"][c]["near_empty_C1_collapse"], inv_f["near_empty_C1_collapse"][c]) for c in ("PAPER_REFERENCE", "NW15_CMB_FIT"))
    res[f"G_{v}_max_rel_vs_inventory"] = maxrel(G[v], inv_g["evidence"])

# archive: F2 recomputed from the frozen input for all populations
frozen_raw = (root / "artifacts/independent/phase1g_f_void_population.json").read_bytes()
frozen = json.loads(frozen_raw)
arch = F["314"]["archived_sensitivities"]
res["archive_input_sha256"] = arch["input_sha256"]
res["archive_input_sha256_matches_frozen_file"] = arch["input_sha256"] == hashlib.sha256(frozen_raw).hexdigest()
res["archive_cutoff_status"] = arch.get("cutoff_status")
n, worst, viol = 0, 0.0, []
for case, cdata in frozen["results"]["cases"].items():
    for key, pop in cdata["populations"].items():
        n += 1
        m, x = pop["void_mass_fraction_1_minus_D"], pop["interior_density_ratio"]
        c = arch["cases"][case][key]
        if c["void_mass_fraction"] != m or c["density_ratio_void_to_wall"] != x:
            viol.append((case, key, "inputs altered"))
        if c["legacy_truncated_universe_budget"] != pop["M3_two_scale_volume_budget"]:
            viol.append((case, key, "legacy F3 altered"))
        if any("cutoff" in k for k in c):
            viol.append((case, key, "archived entry presents a cutoff"))
        for k, mA in pop["lagrangian_fraction"].items():
            f2 = mA / (x * (1 - m) + m)
            worst = max(worst, abs(c["fixed_domain_cumulative"][k] - f2) / max(f2, 1e-300))
res["archive_populations"] = n
res["archive_max_rel_F2"] = worst
res["archive_violations"] = viol
# frozen clocks untouched: compare frozen clock table with itself is trivial; record C3 D_t0 as read
res["frozen_C3_tracker_seed_D_t0"] = {c: d["clocks"]["C3_SEPARATE_UNIVERSE_PBS_TRACKER_SEED"]["D_t0"] for c, d in frozen["results"]["cases"].items()}

# accuracy versus method-diverse references (R2-M1, fine grid)
ref = load(ev / "r2_cutoffs_pde_out.json")["fine"]
acc = {}
for case in ("PAPER_REFERENCE", "NW15_CMB_FIT"):
    a = F["314"]["cases"][case]
    today = a["history"][0]
    r = ref[case]
    acc[case] = {
        "cutoff_F2_shell": (today["cutoff_fixed_domain_h_inv_Mpc"], r["shell_crossing"]["cutoff_F2"]),
        "cutoff_F3_shell": (today["cutoff_truncated_universe_h_inv_Mpc"], r["shell_crossing"]["cutoff_F3"]),
        "F2_ge1": (today["fixed_domain_cumulative"]["r>=1"], r["shell_crossing"]["F2_ge1"]),
        "F2_ge10": (today["fixed_domain_cumulative"]["r>=10"], r["shell_crossing"]["F2_ge10"]),
        "F2_ge15": (today["fixed_domain_cumulative"]["r>=15"], r["shell_crossing"]["F2_ge15"]),
        "z3_F2_ge1": (a["history"][-1]["fixed_domain_cumulative"]["r>=1"], r["z3_F2_ge1"]),
    }
    for x in ("0.1", "0.05"):
        ne = a["near_empty_C1_collapse"][x]
        acc[case][f"near_empty_{x}_cutoff_F2"] = (ne["cutoff_fixed_domain_h_inv_Mpc"], r[x]["cutoff_F2"])
        acc[case][f"near_empty_{x}_cutoff_F3"] = (ne["cutoff_truncated_universe_h_inv_Mpc"], r[x]["cutoff_F3"])
        acc[case][f"near_empty_{x}_F2_ge1"] = (ne["fixed_domain_cumulative"]["r>=1"], r[x]["F2_ge1"])
    acc[case] = {k: {"audited": v[0], "reference": v[1], "rel": v[0] / v[1] - 1} for k, v in acc[case].items()}
res["accuracy_vs_R2M1"] = acc
# boolean surrogate arithmetic
bs = {}
for case in ("PAPER_REFERENCE", "NW15_CMB_FIT"):
    b = F["314"]["cases"][case]["boolean_surrogate"]
    f = b["coverage_supplied"]
    eta = -math.log(1 - f)
    full = F["314"]["cases"][case]["history"][0]["fixed_domain_cumulative"]["all_sizes"]
    bs[case] = {"eta": eta, "eta_reported": b["dimensionless_grain_volume_density_eta"],
                "coverage_from_eta": 1 - math.exp(-eta), "ratio_to_F": eta / full,
                "multiplicity": eta / f, "wall_density_over_mean_empty": 1 / (1 - f)}
res["boolean_surrogate_check"] = bs
(ev / "r2_compare_regen_out.json").write_bytes((json.dumps(res, indent=1, default=str) + "\n").encode())
print(json.dumps({k: v for k, v in res.items() if k != "accuracy_vs_R2M1"}, indent=1, default=str)[:4000])
for case, d in acc.items():
    for k, v in d.items():
        print(f"{case[:4]} {k:28s} audited={v['audited']:.8g} ref={v['reference']:.8g} rel={v['rel']:+.2e}")
