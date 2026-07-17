# CLAUDE.md — timescape-fsigma8

Scientific reproducibility project for Timescape linear perturbations
(arXiv:2511.17160, Galoppo & Mourier, JCAP 02 (2026) 066).

**Read AGENTS.md first — its rules are permanent and non-negotiable.**

## Project phases

- **Phase 1A (done):** audit + reproduce the authors' `ACPT_Timescape.ipynb`
  unchanged → `reports/upstream_reproducibility.md`.
- **Phase 1B (done, incl. compliance gap closure):** independent,
  equation-audited Timescape tracker **background**
  (`src/timescape_fsigma8/background/` package + `units.py`, `presets.py`),
  validated against the upstream oracle →
  `reports/background_equation_audit.md`, `reports/background_validation.md`.
  Key audit findings (documented deviations, await author/human
  confirmation):
  (D1) paper Eq. (5.7) has a spurious f_v0^(-2/3) in <R>_D (correct:
  -6 f_v/t²); (D2) upstream notebook `dQDdt` (cell 6) has `term1 = A1*A2`
  where the quotient rule needs `A1/A2`, corrupting `cs2Eff` (upstream
  -0.3452 today vs correct -0.3912) and the published Fig. 1 right panel +
  Fig. 3 barotropic runs.
- **Phase 1C-A (done):** equation-level perturbation audit →
  `reports/phase1c_perturbation_equation_audit.md` and
  `reports/phase1c_equation_inventory.json`.
- **Phase 1C-B1 (done):** D2-free/D3-free Mészáros and comoving systems,
  explicit IC/epoch scenarios, oracle reproduction, convergence, and Fig. 2
  → `src/timescape_fsigma8/perturbations/` and
  `reports/phase1c_b1_clean_systems_validation.md`.
- **Phase 1C-B2 (done):** barotropic system (Eqs. 4.13–4.17) with **both**
  unresolved D3 branches (`printed_4_15`, `derived_4_10`) and both tilt
  forms as mandatory explicit choices — neither branch adjudicated; upstream
  Fig.-3 trajectories reproduced via an isolated forensic harness (D2 code
  never in the package) → `perturbations/barotropic*.py` and
  `reports/phase1c_b2_barotropic_validation.md`.
- **Phase 1D-A (done):** equation-level growth/observable audit — exact
  Δ_d ↔ δ_m harmonic mapping (Δ_d,k = −k_code² δ_m,k), bare vs dressed
  growth coordinates (exact chain factor (2+f_v)²/(4+f_v+4f_v²)),
  zero-crossing policy, σ_R/σ_8/fσ8 blockers, RSD interpretation →
  `reports/phase1d_a_growth_observable_audit.md` + `..._inventory.json`.
- **Phase 1D-B (done):** growth pipeline `src/timescape_fsigma8/growth/` —
  signed relative growth histories, exact analytic f_bare/f_dressed via
  −3Z/(ΘΔ_d) (no numerical differentiation), non-logarithmic derivatives,
  root-refined crossings + piecewise validity intervals, optional
  solver-harmonic δ_m mapping. Δ_d is a CGI Laplacian scalar, NOT the
  local density contrast; rates are piecewise across amplitude crossings;
  both D3 branches remain unresolved →
  `reports/phase1d_b_growth_pipeline_validation.md`.
- Not implemented: power spectra, σ_R, σ8, fσ8 (incl. any "fσ8-shaped"
  diagnostic), RSD/Kaiser mappings, likelihoods; D3/IC-unit/epoch/k/h/
  coordinate conventions remain unresolved pending author input (see the
  1C-A and 1D-A audits). D2 stays forensic-only.

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
# Full validation suite (337 tests; oracle/artifact tests auto-skip if local
# oracles or generated artifacts are absent)
.venv\Scripts\python -m pytest -q

# Regenerate the upstream comparison oracle (needs .reference/ clone)
.venv\Scripts\python scripts\extract_upstream_oracle.py

# Oracle error statistics -> artifacts/independent/oracle_comparison_stats.json
.venv\Scripts\python scripts\compare_to_oracle.py

# Independent Fig.-1 reproduction + D2 forensic figure -> artifacts/independent/
.venv\Scripts\python scripts\make_independent_fig1.py

# Extract clean Mészáros/comoving oracle (read-only upstream cells)
.venv\Scripts\python scripts\extract_upstream_perturbation_oracle.py

# Clean-system comparison, convergence, and scenario effects
.venv\Scripts\python scripts\validate_clean_perturbations.py

# Independent Fig.-2 reproduction + forensic numerical overlay
.venv\Scripts\python scripts\make_clean_fig2.py

# Extract barotropic Fig.-3 oracle (in-memory, read-only upstream cells)
.venv\Scripts\python scripts\extract_upstream_barotropic_oracle.py

# Barotropic oracle comparison, convergence, D2/D3 factorial, scenario effects
.venv\Scripts\python scripts\validate_barotropic_perturbations.py

# Corrected-cs2 Fig.-3 variants (both D3 branches, raw + /k^2)
.venv\Scripts\python scripts\make_barotropic_fig3.py

# Forensic (D2-corrupted, upstream-reproduction) Fig.-3 variants
.venv\Scripts\python scripts\make_barotropic_fig3_forensic.py

# Growth-pipeline validation (crossings vs frozen 1D-A brackets, identities,
# solver/root convergence, one-factor studies) -> artifacts/independent/
.venv\Scripts\python scripts\validate_growth_pipeline.py

# Re-run the upstream notebook audit (clean kernel, nonzero exit on failure)
.venv\Scripts\python scripts\execute_upstream_notebook.py
```

## Reference material

- Upstream pin: `UPSTREAM.lock`
- Phase 1A findings: `reports/upstream_reproducibility.md`
- Paper: arXiv:2511.17160v2 — Timescape numerics are Sec. 5.1, Figs. 1–3.
