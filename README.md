# timescape-fsigma8

Reproducibility project for linear perturbation growth in the Timescape
cosmological model, based on:

> M. Galoppo & P. Mourier, *Cosmological perturbations on an averaged
> background*, JCAP 02 (2026) 066, arXiv:2511.17160.

## Current status: Phase 1B — background independently implemented

- **Phase 1A (done):** audit + clean-room re-execution of the authors'
  `ACPT_Timescape.ipynb` → `reports/upstream_reproducibility.md`.
- **Phase 1B (done, incl. gap closure):** equation-audited independent
  implementation of the Timescape **tracker background**
  (`src/timescape_fsigma8/background/`), validated against the Buchert
  identities, published reference values, and the upstream notebook as a
  numerical oracle → `reports/background_equation_audit.md` and
  `reports/background_validation.md`. The audit found one typo in the
  paper (Eq. 5.7) and one algebra error in the upstream notebook (`dQDdt`)
  affecting the published c²_s,eff; both are documented, not "fixed"
  upstream.
- **Not started:** perturbation equations, fσ8 predictions.

> **Validation scope is the background only.** The perturbation results of
> the paper have not been independently verified, and the two documented
> upstream findings await confirmation by the authors / scientific review.

## Layout

| Path | Purpose |
|---|---|
| `UPSTREAM.lock` | Exact upstream repo URL, branch, commit SHA, retrieval date |
| `.reference/` | Read-only clone of the upstream repository (git-ignored) |
| `src/timescape_fsigma8/background/` | Independent tracker-background package (`parameters`, `tracker`, `effective_fluid`, `observables`); every function cites its paper equation |
| `src/timescape_fsigma8/units.py` | Audited unit conversions from primary constants (IAU parsec, Julian year) |
| `src/timescape_fsigma8/presets.py` | Immutable parameter presets `PAPER_REFERENCE` (H0 = 73.03) and `NOTEBOOK_REFERENCE` (H0 = 73.23) |
| `tests/` | Validation suite: Buchert identities, limits, reference values, refactor equivalence, wall/dressed observables, epochs, domain validation, upstream-oracle comparison |
| `scripts/execute_upstream_notebook.py` | Executes the upstream notebook from a clean kernel |
| `scripts/extract_upstream_oracle.py` | Samples upstream background functions into the comparison oracle |
| `scripts/compare_to_oracle.py` | Full error statistics vs the oracle → `artifacts/independent/oracle_comparison_stats.json` |
| `scripts/make_independent_fig1.py` | Independent Fig.-1 reproduction (both presets) + D2 forensic figure |
| `artifacts/upstream/` | Executed notebook copy, figures, logs, oracle (git-ignored: upstream-derived content with unclear licensing) |
| `artifacts/independent/` | Outputs of our own implementation: comparison statistics, reproduced figures |
| `reports/upstream_reproducibility.md` | Phase 1A reproducibility report |
| `reports/background_equation_audit.md` | Phase 1B equation audit |
| `reports/background_validation.md` | Phase 1B validation report (metrics, figures, environments, readiness) |
| `reports/phase1b_compliance_audit.md` | Compliance audit of Phase 1B (+ gap-closure addendum) |
| `AGENTS.md` | Permanent project rules (scientific-integrity constraints) |
| `pyproject.toml` | Package + minimal dependency declaration |

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
