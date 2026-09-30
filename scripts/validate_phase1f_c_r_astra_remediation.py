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
# Peeled commit of tag phase-1f-c-r-astra-audit-remediation-v2: the frozen
# state this validator certified.  Review finding F6 replaced the former
# ``main == origin/main == BASE`` and working-tree equality gates with
# ancestry checks against these recorded commits, so the historical claims
# stay verifiable on any descendant checkout.
REMEDIATION = "118b8f3af3c1360b0da74df8e9a9cb3ba1fed83a"
INVENTORY = Path("reports/phase1f_c_r_astra_audit_remediation_inventory.json")
# Raw working-tree hashes that are line-ending encodings of the same content:
# the upstream notebook pinned in UPSTREAM.lock (CRLF -> LF-normalised).
LINE_ENDING_EQUIVALENTS = {
    "86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a":
        "628c441288d67854e0380518841dede3680bddab610e9ef5cea04937455cea2a",
}
# Human-approved successor records that supersede values of the frozen
# inventory's ``current_scientific_status`` snapshot, or add tokens to it.
# The frozen inventory is never edited and is still checked: each superseded
# token must hold the record's ``old_token`` there, and the live module its
# ``new_token``; each added token must be absent there, and the live module
# must hold the record's ``value``.
STATUS_SUCCESSOR_RECORDS = (
    # Phase 1G-A Sec. 4.1, approved 2026-09-29 (one change).
    Path("reports/phase1g_a_barotropic_status_successor_inventory.json"),
    # Phase 1G-C Secs. 5, 8 and 1G-D Secs. 5-7, 9, approved 2026-09-29 (six
    # additions).
    Path("reports/phase1g_status_additions_successor_inventory.json"),
    # Phase 1G-E Secs. 2, 6 item 3, approved 2026-09-29 (one addition).
    Path("reports/phase1g_e_status_addition_successor_inventory.json"),
)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, encoding="utf-8").strip()


def is_ancestor(commit: str, descendant: str = "HEAD") -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", commit, descendant]).returncode == 0


def local_file_status(path: str, expected: str) -> str:
    """Verify one inventory-pinned local file; absence is reported, not hidden."""
    candidate = Path(path)
    if not candidate.is_file():
        return "ABSENT_FROM_CHECKOUT"
    data = candidate.read_bytes()
    if hashlib.sha256(data).hexdigest() == expected:
        return "VERIFIED"
    normalized = LINE_ENDING_EQUIVALENTS.get(expected)
    if normalized and hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest() == normalized:
        return "VERIFIED_LINE_ENDING_EQUIVALENT"
    raise AssertionError(f"{path}: SHA-256 differs from the inventory pin")


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


def successor_status_changes() -> dict[str, dict[str, str]]:
    """Read the approved token changes of every registered successor record."""
    changes: dict[str, dict[str, str]] = {}
    for path in STATUS_SUCCESSOR_RECORDS:
        record = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)
        for key, change in record["status_changes"].items():
            assert key not in changes, f"{key}: superseded by more than one successor record"
            changes[key] = {"old_token": change["old_token"], "new_token": change["new_token"],
                            "record": path.as_posix()}
    return changes


def successor_status_additions() -> dict[str, dict[str, str]]:
    """Read the approved token additions of every registered successor record.

    A record without ``status_additions`` adds nothing (the Phase 1G-A record
    predates additions and stays byte-identical).
    """
    additions: dict[str, dict[str, str]] = {}
    for path in STATUS_SUCCESSOR_RECORDS:
        record = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)
        for key, addition in record.get("status_additions", {}).items():
            assert key not in additions, f"{key}: added by more than one successor record"
            additions[key] = {"value": addition["value"], "record": path.as_posix()}
    return additions


def check_current_scientific_status(frozen, live, changes, *, additions) -> None:
    """Frozen snapshot versus live module, with approved successor records.

    A superseded token must still hold its old value in the frozen snapshot
    (the historical check) and the successor's new value in the live module.
    An added token must be absent from the frozen snapshot (the historical
    check) and hold the successor's value in the live module.  Every other
    token must equal the frozen snapshot.
    """
    assert set(changes) <= set(live), "successor record names a token the live module lacks"
    assert set(additions) <= set(live), "successor record adds a token the live module lacks"
    assert not set(changes) & set(additions), "token both changed and added by successor records"
    for key, value in live.items():
        current = list(value) if isinstance(value, tuple) else value
        if key in changes:
            assert frozen[key] == changes[key]["old_token"], (
                f"{key}: frozen snapshot does not hold the superseded token")
            assert current == changes[key]["new_token"], (
                f"{key}: live value differs from the successor record")
        elif key in additions:
            assert key not in frozen, f"{key}: frozen snapshot already holds an added token"
            assert current == additions[key]["value"], (
                f"{key}: live value differs from the successor record")
        else:
            assert key in frozen, (
                f"{key}: token absent from the frozen snapshot and added by no successor record")
            assert frozen[key] == current, key


def validate(*, producers: bool = False) -> dict[str, object]:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)
    assert INVENTORY.read_bytes() == canonical(inventory), "inventory is not canonical UTF-8/LF JSON"
    assert canonical(json.loads(canonical(inventory))) == canonical(inventory)
    status_changes = successor_status_changes()
    status_additions = successor_status_additions()
    check_current_scientific_status(
        inventory["current_scientific_status"], CURRENT_SCIENTIFIC_STATUS, status_changes,
        additions=status_additions)

    for commit in (BASE, REMEDIATION):
        assert is_ancestor(commit), f"{commit} is not an ancestor of HEAD"

    # Preservation is a claim about the remediation itself: BASE -> REMEDIATION.
    # Later, separately approved changes are reported as drift, not rejected.
    preserved, post_remediation_drift = [], []
    paths = sorted(git("ls-tree", "--name-only", REMEDIATION, "src/timescape_fsigma8/background/").splitlines())
    paths = [Path(name) for name in paths if name.endswith(".py")]
    paths += [Path("src/timescape_fsigma8/perturbations")/name for name in (
        "systems.py", "barotropic.py", "initial_conditions.py")]
    for path in paths:
        before = git("show", f"{BASE}:{path.as_posix()}")
        certified = git("show", f"{REMEDIATION}:{path.as_posix()}")
        assert executable_tree(before) == executable_tree(certified), path
        preserved.append(path.as_posix())
        if not path.is_file() or executable_tree(certified) != executable_tree(path.read_text(encoding="utf-8")):
            post_remediation_drift.append(path.as_posix())
    path = Path("src/timescape_fsigma8/transfer/h1_realization.py")
    trees = [ast.parse(git("show", f"{ref}:{path.as_posix()}")) for ref in (BASE, REMEDIATION)]
    trees.append(ast.parse(path.read_text(encoding="utf-8")))
    for name in ("regional_evolution", "two_region_coefficients"):
        dumps = [
            executable_tree(ast.unparse(next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)))
            for tree in trees
        ]
        assert dumps[0] == dumps[1], name
        preserved.append(f"{path.as_posix()}:{name}")
        if dumps[1] != dumps[2]:
            post_remediation_drift.append(f"{path.as_posix()}:{name}")

    assignments = {
        "phase1f_b/dynamics.py": ["driver_regional", "potential[index + 1]", "potential_dot_regional", "physical_laplacian_regional", "compatibility_regional", "propagation"],
        "phase1f_c/geometry.py": ["laplacian", "wall_expansion", "derivative", "trace[index]"],
    }
    for relative, targets in assignments.items():
        path = Path("src/timescape_fsigma8")/relative
        trees = [ast.parse(git("show", f"{ref}:{path.as_posix()}")) for ref in (BASE, REMEDIATION)]
        trees.append(ast.parse(path.read_text(encoding="utf-8")))
        for target in targets:
            expressions = []
            for tree in trees:
                matches = [ast.dump(n.value) for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(ast.unparse(t) == target for t in n.targets)]
                assert len(matches) == 1, (relative, target, len(matches))
                expressions.append(matches[0])
            assert expressions[0] == expressions[1], (relative, target)
            preserved.append(f"{relative}:{target}")
            if expressions[1] != expressions[2]:
                post_remediation_drift.append(f"{relative}:{target}")

    local_files = {
        path: local_file_status(path, expected)
        for path, expected in inventory["preserved_local_files_sha256"].items()
    }
    absent_local_files = sorted(path for path, state in local_files.items() if state == "ABSENT_FROM_CHECKOUT")
    assert git("-C", ".reference/Linear-Perturbations-in-averaged-cosmological-models", "rev-parse", "HEAD") == inventory["upstream_commit"]
    frozen_tags = {}
    for ref, expected in inventory["frozen_tags"].items():
        present = subprocess.run(["git", "rev-parse", "-q", "--verify", ref], capture_output=True, text=True).stdout.strip()
        if present:
            assert present == expected["tag_object"], ref
            assert git("rev-parse", ref + "^{}") == expected["peeled_commit"], ref
            frozen_tags[ref] = "VERIFIED"
        else:
            # Tag never published to this clone: the recorded commit must
            # still exist and be an ancestor; the tag object stays unverified.
            assert git("cat-file", "-t", expected["peeled_commit"]) == "commit", ref
            frozen_tags[ref] = "TAG_ABSENT_FROM_CLONE_COMMIT_VERIFIED"
        assert is_ancestor(expected["peeled_commit"]), ref
    absent_tags = sorted(ref for ref, state in frozen_tags.items() if state != "VERIFIED")

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
    return {"status": "PASS_WITH_ABSENT_LOCAL_PROVENANCE" if absent_local_files or absent_tags else "PASS",
            "frozen_tags": frozen_tags,
            "absent_frozen_tag_objects": absent_tags,
            "certified_commit": REMEDIATION,
            "preserved_equations": preserved,
            "post_remediation_drift": sorted(post_remediation_drift),
            "successor_status_changes": status_changes,
            "successor_status_additions": status_additions,
            "local_provenance_files": local_files,
            "absent_local_provenance_files": absent_local_files,
            "frozen_tags_verified": len(inventory["frozen_tags"]) - len(absent_tags),
            "historical_reports_unchanged": len(historical),
            "json_roundtrips": len(json_paths), "package_imports": len(imports),
            "explicit_comparisons": {key: len(value) for key, value in records.items()},
            "producer_determinism_sha256": producer_checks}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--producers", action="store_true")
    args = parser.parse_args()
    print(json.dumps(validate(producers=args.producers), indent=2, sort_keys=True))
