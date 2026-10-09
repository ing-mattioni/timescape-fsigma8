"""Read-only scalar/serialization probes for third delta audit.

Usage: python -B -W error THIS_FILE REPO OUT.json
No repository files are changed. Each supported scalar is substituted into
each numeric field of every serializable dataclass of global_variance and
lagrangian_sigma, using fresh constructor validation via dataclasses.replace.
Values are exact type substitutions where possible; truncated int/float32
substitutions are explicitly identified, so rejection is not misreported as
a type defect. Nested configurations are tested in genuine 1G-H records.
"""
from __future__ import annotations

import dataclasses as dc
import importlib.util
import inspect
import json
import math
import sys
from collections import Counter
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np

REPO, OUT = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(REPO / "src"))


def helper(filename, name):
    spec = importlib.util.spec_from_file_location(name, REPO / "tests" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


t = helper("test_phase1g_h_global_variance.py", "audit_gh_helpers")
b = helper("test_phase1g_b_lagrangian_sigma.py", "audit_gb_helpers")
gv, ls = t.gv, t.ls


class NativeFloatSubclass(float):
    """A finite float subclass with no operator overrides."""


res = t.run(t.GM, t.constant(0.05), t.radius("c"))
pbs = t.run(t.GM, t.tracker_seed(t.GM, res.growth, 15.0,
    gv.SeedVolumeCompression.COMPRESSED_WITH_REGION), t.radius("c"))
prem = gv.HomogeneityPremise(radius=t.radius("c", 100.0), max_linear_rms=0.1,
                           provenance="independent serialization probe")
interval = gv.admissible_global_linear_interval(target=res, premise=prem)
sigma = b.sigma("PAPER_REFERENCE", "wall", "bare")
reference = b.reference()
anchor = b.anchored("PAPER_REFERENCE", "wall", "bare")

objects = [t.MATCHING, t.CHECKS, res.growth, t.constant(0.05), pbs.void_share.closure,
           res.void_share, pbs.void_share, res, pbs, prem, interval, t.GM,
           t.spectrum(), t.radius("c"), ls.VOLUME_AVERAGE_GROWTH_REFERENCE_NUMERICS,
           ls.WALL_REGIONAL_GROWTH_REFERENCE_CHECKS, t.QUAD, sigma.growth,
           sigma.density, sigma.radius, sigma, reference, anchor]


def serializer(obj):
    return obj.to_json_dict() if hasattr(obj, "to_json_dict") else obj.to_metadata()


def probe(ident, make, **metadata):
    row = {"id": ident, **metadata}
    try:
        obj = make()
        row.update(accepted=True, stored_type=type(obj).__name__)
        if metadata.get("field"):
            row["stored_scalar_type"] = type(getattr(obj, metadata["field"])).__name__
        try:
            json.dumps(serializer(obj), allow_nan=False)
            row["strict_json"] = True
        except (TypeError, ValueError) as exc:
            row.update(strict_json=False, json_error=f"{type(exc).__name__}: {exc}")
    except Exception as exc:
        row.update(accepted=False, exception=type(exc).__name__, message=str(exc)[:250])
    return row


types = {
    "Fraction": Fraction, "Decimal": lambda x: Decimal(str(x)),
    "np_float32": np.float32, "np_float64": np.float64,
    "float_subclass": NativeFloatSubclass, "int": int, "np_int64": np.int64,
    "bool": bool, "nan": lambda x: math.nan, "positive_inf": lambda x: math.inf,
    "negative_inf": lambda x: -math.inf,
}
rows = []
for i, obj in enumerate(objects):
    cls = type(obj)
    for field in dc.fields(obj):
        orig = getattr(obj, field.name)
        if isinstance(orig, bool) or not isinstance(orig, (float, int)):
            continue
        for kind, convert in types.items():
            value = convert(orig)
            try:
                equal = bool(value == orig)
            except Exception:
                equal = False
            rows.append(probe(f"{cls.__name__}_{i}.{field.name}.{kind}",
                lambda obj=obj, field=field, value=value: dc.replace(obj, **{field.name: value}),
                record=cls.__name__, module=cls.__module__, field=field.name,
                substitution=kind, same_numeric_value=equal, original_type=type(orig).__name__))

# Every numerical diagnostic of the two 1G-H growth checks is bound too.
for index, (name, original) in enumerate(res.growth.diagnostics):
    for kind, convert in types.items():
        value = convert(original)
        diag = list(res.growth.diagnostics)
        diag[index] = (name, value)
        rows.append(probe(f"growth.diagnostics.{name}.{kind}",
            lambda diag=tuple(diag): dc.replace(res.growth, diagnostics=diag),
            record="TwoPhaseGlobalGrowth", module=gv.__name__,
            substitution=kind, same_numeric_value=bool(value == original), diagnostic=name))

# Native 1G-H records can inherit non-JSON scalar types from imported configs.
for name in ("k_min_per_Mpc", "k_max_per_Mpc", "self_convergence_tolerance",
             "truncation_tolerance", "grid_points", "comparison_grid_points"):
    for kind in ("Fraction", "np_float32", "np_int64"):
        value = types[kind](getattr(t.QUAD, name))
        rows.append(probe(f"nested.quadrature.{name}.{kind}",
            lambda name=name, value=value: dc.replace(res, quadrature=dc.replace(t.QUAD, **{name: value})),
            record="ConditionalGlobalLinearSigma", module=gv.__name__,
            nested_field="quadrature." + name, substitution=kind,
            same_numeric_value=bool(value == getattr(t.QUAD, name))))

def replace_density_scalar(name):
    density = dc.replace(res.density, **{name: Fraction(getattr(res.density, name))})
    return dc.replace(res, density=density, void_share=dc.replace(res.void_share, density=density))

for name in ("omega_m_per_photon", "identity_tolerance", "G"):
    rows.append(probe(f"nested.density.{name}.Fraction", lambda name=name:
        replace_density_scalar(name), record="ConditionalGlobalLinearSigma", module=gv.__name__,
        nested_field="density." + name, substitution="Fraction", same_numeric_value=True,
        note="density shared coherently with void_share; only omega_m_per_photon is exported by 1G-H"))
for name in ("radius_Mpc", "omega_m_R_cubed_Mpc3"):
    rows.append(probe(f"nested.radius.{name}.Fraction", lambda name=name: dc.replace(res,
        radius=dc.replace(res.radius, **{name: Fraction(getattr(res.radius, name))})),
        record="ConditionalGlobalLinearSigma", module=gv.__name__,
        nested_field="radius." + name, substitution="Fraction", same_numeric_value=True))

# A field not re-evaluated from input need not retain its original value.
# This probe deliberately changes semantics to make that boundary visible.
for field in ("truncation_envelope_fraction", "quadrature_relative_change"):
    rows.append(probe(f"unbound.lcdm.{field}.nan", lambda field=field:
        dc.replace(reference, **{field: math.nan}), record="LCDMReferenceLinearSigma",
        module=ls.__name__, field=field, substitution="nan", same_numeric_value=False,
        note="preexisting imported class, direct construction"))
for field, value in (("growth_ratio", 999.0), ("early_spectrum_factor", 999.0)):
    rows.append(probe(f"unbound.anchor.{field}.999", lambda field=field, value=value:
        dc.replace(anchor, **{field: value}), record="AnchoredLagrangianSigmaRatio",
        module=ls.__name__, field=field, substitution="semantic_change", same_numeric_value=False,
        note="preexisting imported class, direct construction"))

present = {type(o).__name__ for o in objects}
serializable = {name for module in (gv, ls) for name, cls in vars(module).items()
    if inspect.isclass(cls) and cls.__module__ == module.__name__ and dc.is_dataclass(cls)
    and (hasattr(cls, "to_json_dict") or hasattr(cls, "to_metadata"))}
summary = {
    "runtime": sys.version, "repository": str(REPO), "probes": len(rows),
    "serialized_classes": sorted(present), "missing_serialized_classes": sorted(serializable - present),
    "accepted": sum(r["accepted"] for r in rows),
    "accepted_non_strict_json": [r["id"] for r in rows if r["accepted"] and not r.get("strict_json", True)],
    "accepted_nonfinite": [r["id"] for r in rows if r["accepted"] and r.get("substitution") in
        ("nan", "positive_inf", "negative_inf")],
    "non_strict_by_record": dict(Counter(r["record"] for r in rows
        if r["accepted"] and not r.get("strict_json", True))),
}
OUT.write_text(json.dumps({"summary": summary, "probes": rows}, indent=1, allow_nan=False) + "\n")
print(json.dumps({k: v for k, v in summary.items() if k != "accepted_non_strict_json"}, indent=1))
