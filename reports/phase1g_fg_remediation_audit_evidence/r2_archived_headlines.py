"""Delta audit R2-M6: F2 values behind frozen 1G-F headline claims that used F3 (from the regenerated archive)."""
import json, sys
from pathlib import Path
ev = Path(sys.argv[1])
F = json.loads((ev / "regen/F_314.json").read_bytes())["archived_sensitivities"]["cases"]
rows = {}
for case, pops in F.items():
    for key, p in pops.items():
        clock, barrier, thr = key.split("/")
        if thr != "collapse" or barrier not in ("shell_crossing", "near_empty_0.1"):
            continue
        rows[f"{case}/{key}"] = {"F2_ge10": p["fixed_domain_cumulative"]["r>=10"], "F3_ge10": p["legacy_truncated_universe_budget"]["r>=10"]}
out = {"rows": rows}
def rng(pred, field):
    v = [r[field] for k, r in rows.items() if pred(k)]
    return [min(v), max(v)] if v else None
out["frozen_claim_62_73pct_PBS_shell_crossing_ge10"] = {
    "F3": rng(lambda k: "PBS_F_VI" in k and "shell_crossing" in k, "F3_ge10"),
    "F2": rng(lambda k: "PBS_F_VI" in k and "shell_crossing" in k, "F2_ge10")}
out["frozen_claim_40_68pct_PBS_x0.1_ge10"] = {
    "F3": rng(lambda k: "PBS_F_VI" in k and "near_empty_0.1" in k, "F3_ge10"),
    "F2": rng(lambda k: "PBS_F_VI" in k and "near_empty_0.1" in k, "F2_ge10")}
out["frozen_claim_le10pct_C1_C2_C3seed_shell_ge10"] = {
    "F3_max": rng(lambda k: ("C1_" in k or "C2_" in k or "TRACKER_SEED" in k) and "shell_crossing" in k, "F3_ge10"),
    "F2_max": rng(lambda k: ("C1_" in k or "C2_" in k or "TRACKER_SEED" in k) and "shell_crossing" in k, "F2_ge10")}
(ev / "r2_archived_headlines_out.json").write_bytes((json.dumps(out, indent=1) + "\n").encode())
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
