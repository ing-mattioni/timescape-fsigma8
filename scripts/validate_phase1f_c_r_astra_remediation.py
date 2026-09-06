"""Read-only provenance, equation preservation and deterministic JSON checks.

Run from the repository root under each supported Python stack. --producers
also repeats both affected Phase 1F-A/B numerical JSON producers in memory.
No upstream notebook execution, source copying or remote mutation occurs.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import json
from pathlib import Path
import pkgutil
import subprocess

from audit_numerical_tolerances import audit
from timescape_fsigma8.scientific_status import CURRENT_SCIENTIFIC_STATUS

BASE = "63d2104575c6a249e5177e47f4a354b660e70e32"
INVENTORY = Path("reports/phase1f_c_r_astra_audit_remediation_inventory.json")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, encoding="utf-8").strip()


class WithoutDocstrings(ast.NodeTransformer):
    def visit_Expr(self, node):
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            return None
        return self.generic_visit(node)


def executable_tree(source: str) -> str:
    return ast.dump(WithoutDocstrings().visit(ast.parse(source)), include_attributes=False)


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def validate(*, producers: bool = False) -> dict[str, object]:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)
    assert INVENTORY.read_bytes() == canonical(inventory), "inventory is not canonical UTF-8/LF JSON"
    assert canonical(json.loads(canonical(inventory))) == canonical(inventory)
    for key, value in CURRENT_SCIENTIFIC_STATUS.items():
        assert inventory["current_scientific_status"][key] == (list(value) if isinstance(value, tuple) else value)

    preserved = []
    paths = sorted(Path("src/timescape_fsigma8/background").glob("*.py"))
    paths += [Path("src/timescape_fsigma8/perturbations")/name for name in (
        "systems.py", "barotropic.py", "initial_conditions.py")]
    for path in paths:
        before = git("show", f"{BASE}:{path.as_posix()}")
        assert executable_tree(before) == executable_tree(path.read_text(encoding="utf-8")), path
        preserved.append(path.as_posix())
    path = Path("src/timescape_fsigma8/transfer/h1_realization.py")
    old = ast.parse(git("show", f"{BASE}:{path.as_posix()}"))
    new = ast.parse(path.read_text(encoding="utf-8"))
    for name in ("regional_evolution", "two_region_coefficients"):
        left = next(n for n in old.body if isinstance(n, ast.FunctionDef) and n.name == name)
        right = next(n for n in new.body if isinstance(n, ast.FunctionDef) and n.name == name)
        assert executable_tree(ast.unparse(left)) == executable_tree(ast.unparse(right)), name
        preserved.append(f"{path.as_posix()}:{name}")

    assignments = {
        "phase1f_b/dynamics.py": ["driver_regional", "potential[index + 1]", "potential_dot_regional", "physical_laplacian_regional", "compatibility_regional", "propagation"],
        "phase1f_c/geometry.py": ["laplacian", "wall_expansion", "derivative", "trace[index]"],
    }
    for relative, targets in assignments.items():
        path = Path("src/timescape_fsigma8")/relative
        trees = [ast.parse(git("show", f"{BASE}:{path.as_posix()}")), ast.parse(path.read_text(encoding="utf-8"))]
        for target in targets:
            expressions = []
            for tree in trees:
                matches = [ast.dump(n.value) for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(ast.unparse(t) == target for t in n.targets)]
                assert len(matches) == 1, (relative, target, len(matches))
                expressions.append(matches[0])
            assert expressions[0] == expressions[1], (relative, target)
            preserved.append(f"{relative}:{target}")

    for path, expected in inventory["preserved_local_files_sha256"].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected, path
    assert git("-C", ".reference/Linear-Perturbations-in-averaged-cosmological-models", "rev-parse", "HEAD") == inventory["upstream_commit"]
    for ref, expected in inventory["frozen_tags"].items():
        assert git("rev-parse", ref) == expected["tag_object"], ref
        assert git("rev-parse", ref + "^{}") == expected["peeled_commit"], ref
    assert git("rev-parse", "main") == BASE
    assert git("rev-parse", "origin/main") == BASE

    historical = git("ls-tree", "-r", "--name-only", BASE, "reports").splitlines()
    for name in historical:
        assert Path(name).read_text(encoding="utf-8").strip() == git("show", f"{BASE}:{name}"), name
    records = {folder: audit(Path(folder)) for folder in ("src", "scripts", "tests")}
    assert not [r for group in records.values() for r in group if r["missing"]]
    for path in [*Path("src").rglob("*.py"), *Path("scripts").rglob("*.py"), *Path("tests").rglob("*.py")]:
        ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    import timescape_fsigma8
    imports = sorted(item.name for item in pkgutil.walk_packages(timescape_fsigma8.__path__, timescape_fsigma8.__name__ + "."))
    for name in imports:
        importlib.import_module(name)

    json_paths = sorted(Path("reports").glob("*.json"))
    for path in json_paths:
        parsed = json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_pairs)
        first = canonical(parsed)
        assert first == canonical(json.loads(first)), path
    producer_checks = {}
    if producers:
        for module in ("validate_phase1f_a_h1_closure", "validate_phase1f_b_dust_wall_boost_dynamics"):
            validate_producer = importlib.import_module(module).validate
            first = canonical(validate_producer())
            second = canonical(validate_producer())
            assert first == second, module
            producer_checks[module] = hashlib.sha256(first).hexdigest()
    return {"status": "PASS", "preserved_equations": preserved,
            "frozen_tags_verified": len(inventory["frozen_tags"]),
            "historical_reports_unchanged": len(historical),
            "json_roundtrips": len(json_paths), "package_imports": len(imports),
            "explicit_comparisons": {key: len(value) for key, value in records.items()},
            "producer_determinism_sha256": producer_checks}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--producers", action="store_true")
    args = parser.parse_args()
    print(json.dumps(validate(producers=args.producers), indent=2, sort_keys=True))
