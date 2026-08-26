# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Scientific reproducibility project for Timescape linear perturbations
(arXiv:2511.17160, Galoppo & Mourier, JCAP 02 (2026) 066).

**Read `AGENTS.md` first — its ten rules are permanent, non-negotiable, and
outrank anything here.** In particular: never change an equation without a
paper reference and human approval; every implemented equation cites its
equation number; never silently change units, ICs, or sign conventions;
never push or publish anything.

## How work is organised

Work proceeds in numbered phases (1A → 1F-A so far), each of which is either
an **audit** (report-only, no code) or an **implementation** gated by a prior
audit. The pattern is rigid and should be followed for new phases:

1. Preflight on a clean tree at a frozen parent commit; both Python
   environments must pass the full suite before a branch is created.
2. Local, unpushed branch named `phase-<id>-<slug>`.
3. Deliverables: `reports/phase<id>_*.md` plus a machine-readable
   `reports/phase<id>_*_inventory.json` companion for audits, or a
   `..._validation.md` + `artifacts/independent/*.json` pair for
   implementations; generated artifacts are git-ignored and regenerable from
   the committed scripts.
4. An adversarial/compliance audit report before the phase is frozen with an
   annotated tag `phase-<id>-<slug>-v<N>` (see `git tag`).

Reports are the authoritative record of scientific status — when a question
is about *why* something is coded a particular way, the matching report in
`reports/` answers it; the code only cites the conclusion.

## Architecture

Strictly layered; each layer imports only from the ones above it.

| Layer | Package | Owns |
|---|---|---|
| Foundations | `units.py`, `presets.py` | Audited unit conversions; immutable `PAPER_REFERENCE` (H0 = 73.03) / `NOTEBOOK_REFERENCE` (H0 = 73.23) presets |
| Background (1B) | `background/` | Timescape tracker solution, effective fluid, wall/dressed observables (`parameters`, `tracker`, `effective_fluid`, `observables`) |
| Perturbations (1C-B1/B2) | `perturbations/` | Pure RHS functions for the Mészáros (Eq. 4.27), comoving (4.20–4.23) and barotropic (4.13–4.17) systems, explicit IC/epoch scenarios, solver layer, residual diagnostics |
| Growth (1D-B/1D-D) | `growth/` | Signed relative growth histories, exact analytic f_bare/f_dressed via −3Z/(ΘΔ_d) (never numerical differentiation), root-refined amplitude crossings with piecewise validity intervals, solver-harmonic δ_m mapping, externally anchored density-growth diagnostic ("Candidate A") |
| Transfer (1E-F/1E-G) | `transfer/` | Non-observational regional→GM transfer research runtime: the abstract H1 transmission contract (`h1_realization`, `matrix_backend`) and its continuum-geometric realization (`continuum_*`) |
| Forward runtime (1F-A) | `phase1f_a/` | Conditional theoretical forward realization over the frozen 1E-G operator: broken regional Laplace–Beltrami assembly, regional density/expansion inversion, sharp carrier density, regional/carrier spectra, external longitudinal boost, dressed map, sealed orchestrator |

### Conventions that pervade the scientific packages

- **No defaults for scientific choices.** Every unresolved convention (D3
  branch, tilt form, epoch, time unit, wavenumber interpretation, zero-mode
  closure, normalisation, morphology, boost, dressed map) is a mandatory
  keyword-only argument. Where a choice does not apply it must be passed as
  an explicit `not_applicable` / `NOT_APPLICABLE` value, never omitted.
- **Fail-closed contracts.** Frozen (`@dataclass(frozen=True, kw_only=True)`)
  records validate in `__post_init__` and raise dedicated errors
  (`ContinuumContractError`, `Phase1FADimensionalContractError`,
  `Phase1FAStateIntegrityError`, …). State objects are sealed, and object
  identity is required where a later stage must not silently re-derive an
  input.
- **Status constants are part of the API.** Modules export uppercase
  provenance/status strings (`REALIZATION_ID`, `SCIENTIFIC_STATUS_*`,
  `NON_OBSERVATIONAL`, `NOT_FSIGMA8`, `NOT_GRANTED`, …). They encode the
  authorisation recorded in the corresponding report — do not relabel,
  weaken, or attach an observational label to a theoretical quantity.
- Pure functions, typed arrays, read-only numpy buffers, explicitly recorded
  tolerances.

### Scope firewall (do not cross without a new audited phase)

Deliberately not implemented: power spectra, observational transfer
functions, σ_R, σ8, fσ8 **or any "fσ8-shaped" diagnostic**, RSD/Kaiser
mappings, bias, AP conversion, datasets, covariances, likelihoods, fitting.
Phase 1E-A's verdict on identifying Candidate A with observational fσ8 is
`NOT_JUSTIFIED_FOR_OBSERVATIONAL_USE`. The `transfer/` and `phase1f_a/`
runtimes are conditional research runtimes, not Timescape predictions; their
missing closures stay explicit external inputs.

### Standing scientific caveats

- **D1:** paper Eq. (5.7) has a spurious f_v0^(−2/3) in ⟨R⟩_D (correct:
  −6 f_v/t²). Documented, not silently fixed.
- **D2:** the upstream notebook's `dQDdt` (cell 6) uses `term1 = A1*A2`
  where the quotient rule needs `A1/A2`, corrupting `cs2Eff` (upstream
  −0.3452 today vs correct −0.3912) and the published Fig. 1 right panel and
  Fig. 3 barotropic runs. The corrupted sound speed lives **only** in
  `scripts/_phase1c_b2_forensic.py` and must never enter the package.
- **D3:** Phase 1D-D-t adjudicated the equation-level verdict as
  `RESOLVED_DERIVED_4_10`, but **both** runtime branches (`printed_4_15`,
  `derived_4_10`) remain mandatory and are always reported side by side —
  `printed_4_15` is required for paper/notebook reproduction. Neither branch
  is defaulted, deprecated, or removed.
- `Delta_d` is the CGI Laplacian density scalar of Eqs. (2.19)–(2.20), **not**
  the local density contrast; mapped `delta_m` values are solver-harmonic
  coefficients (Δ_d,k = −k_code²·δ_m,k). Growth rates are piecewise across
  amplitude crossings and are never joined across a pole.

## Key commands

```
# One-time setup (no .venv is checked in)
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -e ".[exec,test]"

# Full validation suite (539 tests at the Phase 1F-A checkpoint; oracle and
# generated-artifact tests auto-skip when their inputs are absent)
.venv\Scripts\python -m pytest -q

# A single file / single test / keyword selection
.venv\Scripts\python -m pytest tests\test_phase1f_a_density.py -q
.venv\Scripts\python -m pytest tests\test_growth_crossings.py::test_rounding_zero_sample_is_flagged_not_promoted_to_root -q
.venv\Scripts\python -m pytest -q -k "carrier and not spectral"
```

Phases are also validated on Python 3.11 (`py -3.11 -m venv .venv311`); the
phase reports record both runs.

Oracle extraction (needs the `.reference/` clone) and the validation drivers;
each writes JSON or figures into `artifacts/`:

```
.venv\Scripts\python scripts\execute_upstream_notebook.py
.venv\Scripts\python scripts\extract_upstream_oracle.py
.venv\Scripts\python scripts\extract_upstream_perturbation_oracle.py
.venv\Scripts\python scripts\extract_upstream_barotropic_oracle.py
.venv\Scripts\python scripts\compare_to_oracle.py
.venv\Scripts\python scripts\validate_clean_perturbations.py
.venv\Scripts\python scripts\validate_barotropic_perturbations.py
.venv\Scripts\python scripts\validate_growth_pipeline.py
.venv\Scripts\python scripts\validate_anchored_density_growth.py
.venv\Scripts\python scripts\validate_phase1f_a_h1_closure.py
```

Figure reproductions: `make_independent_fig1.py` (Fig. 1 + D2 forensic),
`make_clean_fig2.py`, `make_barotropic_fig3.py` (corrected c²_s, both D3
branches), `make_barotropic_fig3_forensic.py` (D2-corrupted, upstream
reproduction only). The `transfer/` and `phase1f_a/` layers produce no
figures; `validate_phase1f_a_h1_closure.py` regenerates its artifact
byte-for-byte.

## Hard constraints

- **Never push, publish, fork, or open PRs.** All work stays local.
- `.reference/` is a read-only clone of the upstream repo pinned in
  `UPSTREAM.lock` (no license — treat as all-rights-reserved). Never edit it,
  never commit it, never copy its source into package files.
- Never modify the original upstream notebook; executed or patched copies go
  to `artifacts/upstream/` with documented diffs.
- When reproducing upstream, do not change equations, constants, ICs, solver
  options, or plotting code. Record discrepancies exactly as found — do not
  "fix" them.

## Environment

- Windows 11; Python launcher `py` (3.14 default, 3.11 available). The
  project venv `.venv` is git-ignored and must be created locally.
- The machine's pip default index is an internal Artifactory mirror that is
  not always reachable; if installs fail with DNS errors add
  `--index-url https://pypi.org/simple` (pypi.org is already a trusted host).
- Dependencies (`pyproject.toml`: numpy, scipy, matplotlib; extras `exec` =
  nbformat/nbclient/ipykernel, `test` = pytest) are deliberately unpinned;
  the resolved versions of each run are logged in
  `artifacts/upstream/execution_log.json` and in the phase reports.

## Phase ledger

Done: **1A** upstream notebook audit · **1B** tracker background (+ compliance
gap closure) · **1C-A** perturbation equation audit · **1C-B1** clean
Mészáros/comoving systems · **1C-B2** barotropic system with both D3 branches
· **1D-A** growth/observable audit · **1D-B** growth pipeline · **1D-C**
observable-closure audit (report-only) · **1D-D-t** D3 frame-mapping
adjudication (report-only) · **1D-D** anchored density-growth diagnostic ·
**1E-A/B/C/D/E** dressed-observable bridge, dressed light-cone velocity,
perturbed dressed transfer closure, regional matching dynamics,
transfer-realization selection (all report-only) · **1E-F** conditional H1
transmission realization · **1E-G** continuum-geometric H1 realization ·
**1F-A** H1 carrier density, spectra, expansion and wall-boost closure
(current branch).

Each entry maps to a `reports/phase<id>_*.md` file — read it before touching
the corresponding code.

## Reference material

- Upstream pin: `UPSTREAM.lock`; project overview and full file map:
  `README.md`
- Paper: arXiv:2511.17160v2 — Timescape numerics are Sec. 5.1, Figs. 1–3.
