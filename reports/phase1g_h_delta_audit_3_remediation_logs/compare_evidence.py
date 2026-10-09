"""Compare two evidence JSONs leaf by leaf over every leaf except the run environment.

    python compare_evidence.py OLD.json NEW.json OUT.json

Reports numeric leaves that differ (bitwise), text leaves that differ, and
leaves present in only one of them; figures (paths and hashes) are listed
separately because they depend on the run.
"""
import json, sys

a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))


def leaves(x, path=()):
    if isinstance(x, dict):
        for k, v in x.items():
            if not path and k == "environment":
                continue
            yield from leaves(v, path + (k,))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, path + (str(i),))
    else:
        yield "/".join(path), x


la, lb = dict(leaves(a)), dict(leaves(b))
num_changed, text_changed = [], []
numeric_common = 0
for k in sorted(set(la) & set(lb)):
    x, y = la[k], lb[k]
    numeric = all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (x, y))
    if numeric:
        numeric_common += 1
        if x != y:
            num_changed.append({"leaf": k, "old": x, "new": y})
    elif x != y:
        text_changed.append({"leaf": k, "old": x, "new": y})
out = {"old_environment": a.get("environment"), "new_environment": b.get("environment"),
       "common_leaves": len(set(la) & set(lb)), "numeric_common_leaves": numeric_common,
       "numeric_changed": num_changed, "text_changed": text_changed,
       "only_old": sorted(set(la) - set(lb)), "only_new": sorted(set(lb) - set(la))}
json.dump(out, open(sys.argv[3], "w"), indent=1)
print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in out.items()
                  if k not in ("old_environment", "new_environment")}, indent=1))
