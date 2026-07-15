# timescape-fsigma8

Reproducibility project for linear perturbation growth in the Timescape
cosmological model, based on:

> M. Galoppo & P. Mourier, *Cosmological perturbations on an averaged
> background*, JCAP 02 (2026) 066, arXiv:2511.17160.

## Current status: Phase 1A — upstream reproduction audit

This repository currently does **one** thing: it audits and re-executes the
authors' published notebook `ACPT_Timescape.ipynb` in a clean, documented
environment, and records exactly what happens.

> **No scientific result has been independently validated yet.** Nothing in
> this repository should be cited or relied upon as a confirmation of the
> paper's results. The independent Timescape implementation has not started.

## Layout

| Path | Purpose |
|---|---|
| `UPSTREAM.lock` | Exact upstream repo URL, branch, commit SHA, retrieval date |
| `.reference/` | Read-only clone of the upstream repository (git-ignored) |
| `scripts/execute_upstream_notebook.py` | Executes the upstream notebook from a clean kernel |
| `artifacts/upstream/` | Executed notebook copy, figures, execution log (git-ignored: contains upstream-derived content with unclear licensing) |
| `reports/upstream_reproducibility.md` | The Phase 1A reproducibility report |
| `AGENTS.md` | Permanent project rules (scientific-integrity constraints) |
| `pyproject.toml` | Minimal dependency declaration |

## Licensing note

The upstream repository contains **no license file**. Its code is treated as
all-rights-reserved reference material: it is cloned locally for audit only,
never committed to this repository, and never redistributed. See
`UPSTREAM.lock` and rule 6 of `AGENTS.md`.

## Reproducing the audit

```
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install numpy scipy matplotlib nbformat nbclient ipykernel
.venv\Scripts\python scripts\execute_upstream_notebook.py
```

The script fails with a nonzero exit code if any notebook cell fails, writes
the executed copy to `artifacts/upstream/ACPT_Timescape.executed.ipynb`, and
records the environment and all captured output in
`artifacts/upstream/execution_log.json`. It never modifies the original
notebook.
