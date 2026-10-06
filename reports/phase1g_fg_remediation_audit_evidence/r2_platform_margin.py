"""Delta audit R2-M7: actual Linux-vs-Windows differences behind the rtol=1e-11/atol=1e-14 gate."""
import json, sys
from pathlib import Path
root, ev = Path(sys.argv[1]), Path(sys.argv[2])
inv_f = json.loads((root / "reports/phase1g_f_volume_budget_successor_inventory.json").read_bytes())
inv_g = json.loads((root / "reports/phase1g_g_void_evolution_inventory.json").read_bytes())
F = json.loads((ev / "regen/F_314.json").read_bytes()); G = json.loads((ev / "regen/G_314.json").read_bytes())
pairs = []
def walk(a, b, path):
    if isinstance(b, dict):
        for k in b:
            if k in a and k not in ("environment", "input_sha256"):
                walk(a[k], b[k], f"{path}/{k}")
    elif isinstance(b, list):
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f"{path}[{i}]")
    elif isinstance(b, float) and isinstance(a, (int, float)):
        pairs.append((path, a, b))
for c in ("PAPER_REFERENCE", "NW15_CMB_FIT"):
    walk(F["cases"][c]["history"], inv_f["primary_cases"][c], f"F/{c}/history")
    walk(F["cases"][c]["near_empty_C1_collapse"], inv_f["near_empty_C1_collapse"][c], f"F/{c}/near")
walk(G, inv_g["evidence"], "G")
out = {}
for floor in (0.0, 1e-12, 1e-6):
    sel = [(p, a, b) for p, a, b in pairs if abs(b) > floor]
    worst = max(sel, key=lambda t: abs(t[1] - t[2]) / abs(t[2]) if t[2] else 0)
    out[f"max_rel_for_abs_ref_gt_{floor:g}"] = {"n": len(sel), "rel": abs(worst[1] - worst[2]) / abs(worst[2]) if worst[2] else None, "path": worst[0]}
out["max_abs_diff_all"] = max(abs(a - b) for _, a, b in pairs)
out["n_leaves"] = len(pairs)
out["bitwise_equal_leaves"] = sum(1 for _, a, b in pairs if a == b)
(ev / "r2_platform_margin_out.json").write_bytes((json.dumps(out, indent=1) + "\n").encode())
print(json.dumps(out, indent=1))
