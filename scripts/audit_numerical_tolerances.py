"""Deterministic AST inventory of explicit absolute/relative comparison semantics.

Exact equality/assert_array_equal has zero tolerance by definition. Decimal
comparisons, if introduced, need separate review; they are reported as missing.
This is a syntax gate, not proof that a chosen numerical tolerance is suitable.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path


def audit(root: Path) -> list[dict[str, object]]:
    records = []
    for path in sorted(root.rglob("*.py")):
        source = path.read_text(encoding="utf-8-sig")
        tree = ast.parse(source)
        aliases = {}
        for item in ast.walk(tree):
            if isinstance(item, ast.Import):
                for alias in item.names:
                    aliases[alias.asname or alias.name] = alias.name
            elif isinstance(item, ast.ImportFrom) and item.module:
                for alias in item.names:
                    aliases[alias.asname or alias.name] = f"{item.module}.{alias.name}"
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = ast.unparse(node.func)
            head, *tail = name.split(".")
            name = ".".join([aliases.get(head, head), *tail])
            kind = name.rsplit(".", 1)[-1]
            if kind not in {"assert_allclose", "allclose", "isclose", "approx",
                            "assert_almost_equal", "assert_array_almost_equal", "assert_approx_equal"}:
                continue
            keys = {kw.arg: ast.unparse(kw.value) for kw in node.keywords}
            expected = ("rel", "abs") if kind == "approx" else (
                ("rel_tol", "abs_tol") if name == "math.isclose" else ("rtol", "atol")
            )
            records.append({"file": path.as_posix(), "line": node.lineno,
                            "call": name, "tolerances": keys,
                            "missing": [key for key in expected if key not in keys]})
    return sorted(records, key=lambda item: (item["file"], item["line"]))


if __name__ == "__main__":
    records = audit(Path("tests"))
    missing = [item for item in records if item["missing"]]
    print(json.dumps({"comparisons": len(records), "missing_count": len(missing),
                      "missing": missing}, indent=2, sort_keys=True))
