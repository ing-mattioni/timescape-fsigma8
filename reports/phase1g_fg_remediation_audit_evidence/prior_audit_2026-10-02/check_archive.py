"""Auditor check: F2 on all archived populations, invariants, variance shares (reads JSON only)."""
import hashlib
import json
import math
import sys

frozen_path, succ_path, inv_path = sys.argv[1:4]
raw = open(frozen_path, "rb").read()
frozen = json.loads(raw)
succ = json.loads(open(succ_path, "rb").read())
inv = json.loads(open(inv_path, "rb").read())
out = {"frozen_sha256": hashlib.sha256(raw).hexdigest()}

arch = succ["archived_sensitivities"]
assert arch["input_sha256"] == out["frozen_sha256"]
n = 0
worst = 0.0
viol = []
keys_seen = set()
for case, cdata in frozen["results"]["cases"].items():
    for key, pop in cdata["populations"].items():
        n += 1
        m, x = pop["void_mass_fraction_1_minus_D"], pop["interior_density_ratio"]
        den = x * (1 - m) + m
        corr = arch["cases"][case][key]
        assert corr["void_mass_fraction"] == m and corr["density_ratio_void_to_wall"] == x
        assert corr["legacy_truncated_universe_budget"] == pop["M3_two_scale_volume_budget"]
        prev = None
        order = ["all_sizes", "r>=1", "r>=2", "r>=5", "r>=10", "r>=15"]
        for k in order:
            mA = pop["lagrangian_fraction"][k]
            f2 = mA / den
            f3 = mA / (x * (1 - mA) + mA)
            worst = max(worst, abs(corr["fixed_domain_cumulative"][k] - f2) / max(f2, 1e-300))
            if abs(pop["M3_two_scale_volume_budget"][k] - f3) > 1e-15 * max(1, f3):
                viol.append((case, key, k, "F3 legacy mismatch"))
            if f2 > f3 * (1 + 1e-15):
                viol.append((case, key, k, "F2>F3"))
            if prev is not None and f2 > prev * (1 + 1e-15):
                viol.append((case, key, k, "non-monotone"))
            prev = f2
            if not (0 <= mA <= m + 1e-12):
                viol.append((case, key, k, f"selected mass {mA} outside [0, m={m}]"))
        if pop["unresolved_below_grid"] < 0:
            keys_seen.add((case, key, pop["unresolved_below_grid"]))
out["n_populations"] = n
out["max_rel_diff_F2_vs_successor_archive"] = worst
out["violations"] = viol
out["negative_unresolved"] = sorted(keys_seen, key=lambda t: t[2])[:10]
out["n_negative_unresolved"] = len(keys_seen)

# successor artifact (local) primary vs inventory values
dmax = 0.0
for case in ("PAPER_REFERENCE", "NW15_CMB_FIT"):
    for a, b in zip(succ["cases"][case]["history"], inv["primary_cases"][case]):
        for k in ("fixed_domain_cumulative", "legacy_truncated_universe_budget"):
            for kk in a[k]:
                dmax = max(dmax, abs(a[k][kk] - b[k][kk]) / max(abs(b[k][kk]), 1e-300))
        for k in ("median_radius_h_inv_Mpc", "cutoff_fixed_domain_h_inv_Mpc", "cutoff_truncated_universe_h_inv_Mpc", "tracker_f_v", "D_wall"):
            dmax = max(dmax, abs(a[k] - b[k]) / abs(b[k]))
out["local_successor_vs_inventory_max_rel"] = dmax
out["local_successor_environment"] = succ["environment"]

# variance shares from the frozen artifact (C1 shell crossing collapse, tracker f_v0, photon frame)
shares = {}
for case, cdata in frozen["results"]["cases"].items():
    v = cdata["variance"]["C1_WALL_EDS_COMMON_TIME/shell_crossing/collapse"]["tracker_f_v0"]
    sp, si, st = v["sigma_part"], v["sigma_int_photon_frame_Dwall"], v["sigma_total_photon_frame_Dwall_empty_voids"]
    shares[case] = {"sigma_part": sp, "sigma_int": si, "sigma_total": st,
                    "wall_share": si ** 2 / st ** 2, "partition_share": sp ** 2 / st ** 2,
                    "check_total": math.sqrt(sp * sp + si * si),
                    "f_cov": v["f_cov"],
                    "barrier_interior_total": v["sigma_total_photon_frame_Dwall_barrier_interior"],
                    "M3_norm_total": cdata["variance"]["C1_WALL_EDS_COMMON_TIME/shell_crossing/collapse"]["M3_predicted_all_sizes"]["sigma_total_photon_frame_Dwall_empty_voids"]}
out["variance_shares"] = shares
# C3 tracker-seed clock values (historical normalization)
out["C3_tracker_seed"] = {c: {k: d["clocks"]["C3_SEPARATE_UNIVERSE_PBS_TRACKER_SEED"][k] for k in ("D_t0", "A_v")}
                          for c, d in frozen["results"]["cases"].items()}
out["D_wall_t0"] = {c: d["D_wall_t0"] for c, d in frozen["results"]["cases"].items()}
print(json.dumps(out, indent=1))
