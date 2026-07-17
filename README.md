# timescape-fsigma8

Reproducibility project for linear perturbation growth in the Timescape
cosmological model, based on:

> M. Galoppo & P. Mourier, *Cosmological perturbations on an averaged
> background*, JCAP 02 (2026) 066, arXiv:2511.17160.

## Current status: Phase 1C-B2 — barotropic perturbation systems validated

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
- **Phase 1C-A (done):** equation-level audit of the Mészáros, comoving,
  and barotropic perturbation systems, including IC/epoch provenance and
  complete D2/D3 mapping → `reports/phase1c_perturbation_equation_audit.md`.
- **Phase 1C-B1 (done):** independent typed implementation and numerical
  validation of the D2-free/D3-free **Mészáros and comoving** systems,
  including explicit IC/epoch scenarios, solver convergence, oracle
  reproduction, and clean Fig. 2 →
  `reports/phase1c_b1_clean_systems_validation.md`.
- **Phase 1C-B2 (done):** independent typed implementation and numerical
  validation of the **barotropic** system (Eqs. 4.13–4.17), exposing **both**
  unresolved D3 branches (`printed_4_15`, `derived_4_10`), both tilt
  variables, and the IC-rate/epoch/wavenumber interpretations as mandatory
  explicit choices with no defaults; upstream Fig.-3 trajectories reproduced
  through an isolated forensic harness (the D2-corrupted sound speed never
  enters the scientific package) →
  `reports/phase1c_b2_barotropic_validation.md`.
- **Not implemented:** fσ8 predictions, σ8 normalisation, or likelihoods.

> **Validation scope now covers the background plus the Mészáros, comoving,
> and barotropic perturbation systems.** fσ8 remains outside the validated
> scope. Neither D3 branch is adjudicated, and the documented D1/D2/D3
> findings and IC-unit/epoch/wavenumber ambiguities await scientific review.

## Layout

| Path | Purpose |
|---|---|
| `UPSTREAM.lock` | Exact upstream repo URL, branch, commit SHA, retrieval date |
| `.reference/` | Read-only clone of the upstream repository (git-ignored) |
| `src/timescape_fsigma8/background/` | Independent tracker-background package (`parameters`, `tracker`, `effective_fluid`, `observables`); every function cites its paper equation |
| `src/timescape_fsigma8/perturbations/` | Perturbation package: pure Mészáros/comoving RHS functions (1C-B1) plus the barotropic system with mandatory explicit D3-branch/tilt/rate/epoch/wavenumber choices (1C-B2); explicit IC/epoch scenarios, solver layer, and residual diagnostics |
| `src/timescape_fsigma8/units.py` | Audited unit conversions from primary constants (IAU parsec, Julian year) |
| `src/timescape_fsigma8/presets.py` | Immutable parameter presets `PAPER_REFERENCE` (H0 = 73.03) and `NOTEBOOK_REFERENCE` (H0 = 73.23) |
| `tests/` | Validation suite: Buchert identities, limits, reference values, refactor equivalence, wall/dressed observables, epochs, domain validation, upstream-oracle comparison |
| `scripts/execute_upstream_notebook.py` | Executes the upstream notebook from a clean kernel |
| `scripts/extract_upstream_oracle.py` | Samples upstream background functions into the comparison oracle |
| `scripts/compare_to_oracle.py` | Full error statistics vs the oracle → `artifacts/independent/oracle_comparison_stats.json` |
| `scripts/make_independent_fig1.py` | Independent Fig.-1 reproduction (both presets) + D2 forensic figure |
| `scripts/extract_upstream_perturbation_oracle.py` | Read-only extraction of clean upstream Mészáros/comoving trajectories |
| `scripts/validate_clean_perturbations.py` | Oracle comparison, convergence, implicit cross-check, and IC/epoch scenario effects |
| `scripts/make_clean_fig2.py` | Independent clean Fig.-2 reproduction + local forensic overlay |
| `scripts/extract_upstream_barotropic_oracle.py` | Read-only in-memory extraction of upstream barotropic Fig.-3 trajectories |
| `scripts/validate_barotropic_perturbations.py` | Barotropic oracle comparison, convergence, D2/D3 factorial, and scenario effects |
| `scripts/make_barotropic_fig3.py` | Corrected-c²ₛ Fig.-3 variants for both D3 branches (raw and /k²) |
| `scripts/make_barotropic_fig3_forensic.py` | Forensic (D2-corrupted, upstream-reproduction) Fig.-3 variants |
| `scripts/_phase1c_b2_forensic.py` | Isolated forensic harness holding the D2-corrupted sound speed (never imported by the scientific package) |
| `artifacts/upstream/` | Executed notebook copy, figures, logs, oracles (git-ignored: upstream-derived content with unclear licensing) |
| `artifacts/independent/` | Outputs of our own implementation: comparison statistics, reproduced figures |
| `reports/upstream_reproducibility.md` | Phase 1A reproducibility report |
| `reports/background_equation_audit.md` | Phase 1B equation audit |
| `reports/background_validation.md` | Phase 1B validation report (metrics, figures, environments, readiness) |
| `reports/phase1b_compliance_audit.md` | Compliance audit of Phase 1B (+ gap-closure addendum) |
| `reports/phase1c_perturbation_equation_audit.md` | Phase 1C-A equation/IC/epoch audit and D2/D3 map |
| `reports/phase1c_equation_inventory.json` | Machine-readable Phase 1C-A equation inventory |
| `reports/phase1c_b1_clean_systems_validation.md` | Phase 1C-B1 implementation, comparison, convergence, scenario, and readiness report |
| `reports/phase1c_b2_barotropic_validation.md` | Phase 1C-B2 barotropic implementation, upstream reproduction, D2/D3 factorial, and sensitivity report |
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
