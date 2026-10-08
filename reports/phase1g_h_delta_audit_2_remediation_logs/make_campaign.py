"""Build the round-3 rerun of the second delta audit's mutation campaign.

The audit's script is copied unchanged except: (1) mutant A01 targets the
float comparison of the revised ``_same`` (its original string no longer
exists after GH-D2F4); (2) four round-3 mutants (R01-R04) of the GH-D2F4
changes are appended to the audit's own list.
"""
import json, sys
from pathlib import Path

src = Path(sys.argv[1]).read_text()
out = Path(sys.argv[2])
adapt = {
    "A01_same_tolerance_widened": {
        "old_audit": ["and _close(float(stored), float(expected)))",
                      "and math.isclose(float(stored), float(expected), rel_tol=1e-3))"],
        "old": "and _close(stored, expected))",
        "new": "and math.isclose(stored, expected, rel_tol=1e-3))",
        "reason": "GH-D2F4 changed the float branch of _same to compare floats directly; "
                  "the mutant widens the same comparison to rel_tol 1e-3"},
}
own_r3 = [
    ("R01_same_accepts_any_real", "SRC",
     "    if isinstance(expected, float):\n        return (isinstance(stored, float) and math.isfinite(stored)",
     "    if isinstance(expected, float):\n        return (isinstance(stored, Real) and math.isfinite(float(stored))"),
    ("R02_float_type_message_off", "SRC",
     "        if isinstance(expected, float) and not isinstance(stored, float):",
     "        if False:"),
    ("R03_G_not_stored_as_float", "SRC",
     '        object.__setattr__(self, "G", G)\n', ""),
    ("R04_checks_not_stored_as_float", "SRC",
     "            object.__setattr__(self, name, _positive(getattr(self, name), name))",
     "            _positive(getattr(self, name), name)"),
]
a = adapt["A01_same_tolerance_widened"]
old_line = '    ("A01_same_tolerance_widened", SRC, "and _close(float(stored), float(expected)))",\n     "and math.isclose(float(stored), float(expected), rel_tol=1e-3))"),\n'
assert src.count(old_line) == 1, "A01 definition not found"
src = src.replace(old_line, '    ("A01_same_tolerance_widened", SRC, %r,\n     %r),\n' % (a["old"], a["new"]))
anchor = "mutants += [(\"own\",) + m for m in own]\n"
assert src.count(anchor) == 1
extra = "own_r3 = [\n" + "".join("    (%r, %s, %r, %r),\n" % (i, f, o, n) for i, f, o, n in own_r3) + "]\n"
src = src.replace(anchor, anchor + extra + "mutants += [(\"round3\",) + m for m in own_r3]\n")
out.write_text(src)
defs = {"adaptations": [{"id": k, **v} for k, v in adapt.items()],
        "round3_mutants": [{"id": i, "file": "src/timescape_fsigma8/global_variance.py", "old": o, "new": n}
                           for i, f, o, n in own_r3]}
Path(sys.argv[3]).write_text(json.dumps(defs, indent=1) + "\n")
print("ok")
