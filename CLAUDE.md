# CLAUDE.md — timescape-fsigma8

Scientific reproducibility project for Timescape linear perturbations
(arXiv:2511.17160, Galoppo & Mourier, JCAP 02 (2026) 066).

**Read AGENTS.md first — its rules are permanent and non-negotiable.**

## Project phases

- **Phase 1A (current, complete when `reports/upstream_reproducibility.md`
  exists): audit + reproduce the authors' `ACPT_Timescape.ipynb` unchanged.**
- Later phases (not started): independent implementation of the Timescape
  perturbation equations, then fσ8 predictions. Do not begin these without
  explicit instruction.

## Hard constraints

- **Never push, publish, fork, or open PRs.** All work stays local.
- `.reference/` is a read-only clone of the upstream repo, pinned in
  `UPSTREAM.lock`. Never edit anything under it. Never commit it (it has no
  license; treat as all-rights-reserved).
- Never modify the original upstream notebook. Executed/patched copies go
  under `artifacts/upstream/` only, with documented diffs.
- Do not change equations, constants, initial conditions, solver options, or
  plotting code when reproducing upstream. Record discrepancies with the
  paper exactly as found — do not "fix" them.

## Environment

- Windows 11, Python launcher `py` (3.14 default; 3.11, 3.10 available).
  Project venv: `.venv` (created with `py -3.14 -m venv .venv`).
- The machine's pip default index is an internal Artifactory mirror that is
  not always reachable; if installs fail with DNS errors, add
  `--index-url https://pypi.org/simple` (pypi.org is already a trusted host).
- Dependencies: see `pyproject.toml` (numpy, scipy, matplotlib + nbformat,
  nbclient, ipykernel for notebook execution). Deliberately unpinned; exact
  versions of each run are logged in `artifacts/upstream/execution_log.json`.
- Git quirk: `C:\timescape-fsigma8` is owned by Administrators, so git
  (2.37.x) refuses to operate ("dubious ownership"). Non-invasive
  workaround: point `GIT_CONFIG_GLOBAL` at a temp config file containing
  `[safe] directory = C:/timescape-fsigma8`. The permanent fix (changes the
  user's global config — ask first) is
  `git config --global --add safe.directory C:/timescape-fsigma8`.

## Key commands

```
# Re-run the upstream notebook audit (clean kernel, nonzero exit on failure)
.venv\Scripts\python scripts\execute_upstream_notebook.py
```

## Reference material

- Upstream pin: `UPSTREAM.lock`
- Phase 1A findings: `reports/upstream_reproducibility.md`
- Paper: arXiv:2511.17160v2 — Timescape numerics are Sec. 5.1, Figs. 1–3.
