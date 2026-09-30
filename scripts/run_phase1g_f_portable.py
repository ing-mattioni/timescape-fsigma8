"""Run the frozen Phase 1G-F numerics script on any platform (owner approval 2026-09-30).

``scripts/phase1g_f_void_population_numerics.py`` imports the Unix-only
``resource`` module for its stderr progress line.  This runner installs the
Windows stand-in of ``scripts/_portable_resource.py`` (a no-op on Unix) and
then executes the frozen script, unchanged, as ``__main__`` by path.  Its
stdout, its gates and its artifact
(``artifacts/independent/phase1g_f_void_population.json``) are the frozen
script's own.

Usage: ``python scripts/run_phase1g_f_portable.py``.
Record: reports/phase1g_windows_validation_record.md.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
FROZEN = SCRIPTS / "phase1g_f_void_population_numerics.py"


def main() -> int:
    sys.path.insert(0, str(SCRIPTS))
    import _portable_resource

    source = _portable_resource.install()
    print(f"[runner] resource module: {source}", file=sys.stderr, flush=True)
    try:
        runpy.run_path(str(FROZEN), run_name="__main__")
    except SystemExit as exit_:
        return int(exit_.code or 0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
