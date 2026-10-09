"""Leaf-by-leaf regression count between two evidence JSONs (round 3, GH-D2E1).

Every leaf is compared except the run environment and the figure list
(paths and hashes of the run).  Numeric leaves: changed if not bitwise
equal; "beyond round-off" if the relative difference exceeds 1e-12.
Prints counts inside and outside two_phase_covariance/*/gaussian_threshold_pair.
"""
import json, sys
a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
SKIP = ("environment", "figures")
PAIR = "gaussian_threshold_pair"


def leaves(x, path=()):
    if isinstance(x, dict):
        for k, v in x.items():
            if not path and k in SKIP:
                continue
            yield from leaves(v, path + (k,))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, path + (str(i),))
    else:
        yield "/".join(path), x


la, lb = dict(leaves(a)), dict(leaves(b))
inside = lambda k: k.startswith("two_phase_covariance/") and f"/{PAIR}/" in k
out = {"inside": {}, "outside": {}}
for region in out:
    sel = (lambda k: inside(k)) if region == "inside" else (lambda k: not inside(k))
    common = [k for k in la if k in lb and sel(k)]
    num_changed, beyond, text_changed, examples = 0, 0, 0, []
    max_abs = 0.0
    for k in common:
        x, y = la[k], lb[k]
        numeric = (isinstance(x, (int, float)) and not isinstance(x, bool)
                   and isinstance(y, (int, float)) and not isinstance(y, bool))
        if numeric:
            if x != y:
                num_changed += 1
                rel = abs(x - y) / max(abs(x), abs(y))
                max_abs = max(max_abs, abs(x - y))
                if rel > 1e-12:
                    beyond += 1
                examples.append((k, x, y))
        elif x != y:
            text_changed += 1
            examples.append((k, x, y))
    removed = sorted(k for k in la if k not in lb and sel(k))
    added = sorted(k for k in lb if k not in la and sel(k))
    out[region] = {"common": len(common), "numeric_changed": num_changed,
                   "numeric_changed_beyond_1e-12_rel": beyond, "text_changed": text_changed,
                   "max_abs_numeric_change": max_abs,
                   "only_old": len(removed), "only_new": len(added),
                   "only_old_keys": removed, "examples": examples if region == "outside" else examples[:0]}
    if region == "outside":
        out[region]["only_new_keys"] = added
print(json.dumps(out, indent=1, default=str))
