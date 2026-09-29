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
| Foundations | `units.py`, `presets.py`, `components.py`, `scientific_status.py` | Audited unit conversions; immutable `PAPER_REFERENCE` (H0 = 73.03) / `NOTEBOOK_REFERENCE` (H0 = 73.23) presets; tensor-component ontology (coordinate covector / contravariant / orthonormal, 1F-C-R A02); current cross-phase scientific classifications (`CURRENT_SCIENTIFIC_STATUS`, 1F-C-R) |
| Background (1B) | `background/` | Timescape tracker solution, effective fluid, wall/dressed observables (`parameters`, `tracker`, `effective_fluid`, `observables`) |
| Perturbations (1C-B1/B2) | `perturbations/` | Pure RHS functions for the Mészáros (Eq. 4.27), comoving (4.20–4.23) and barotropic (4.13–4.17) systems, explicit IC/epoch scenarios, solver layer, residual diagnostics; `growing_mode` adds the explicit, non-default Timescape regular growing-mode IC convention for the clean systems (review F1) |
| Growth (1D-B/1D-D) | `growth/` | Signed relative growth histories, exact analytic f_bare/f_dressed via −3Z/(ΘΔ_d) (never numerical differentiation), root-refined amplitude crossings with piecewise validity intervals, solver-harmonic δ_m mapping, externally anchored density-growth diagnostic ("Candidate A") |
| Transfer (1E-F/1E-G) | `transfer/` | Non-observational regional→GM transfer research runtime: the abstract H1 transmission contract (`h1_realization`, `matrix_backend`) and its continuum-geometric realization (`continuum_*`); mandatory `H1KinematicGatePolicy` — only `ENFORCE`d results (background identities + CLK-H1 `J_Xi = 0`) carry the closure status tokens (review F3) |
| Forward runtime (1F-A) | `phase1f_a/` | Conditional theoretical forward realization over the frozen 1E-G operator: broken regional Laplace–Beltrami assembly, regional density/expansion inversion, sharp carrier density, regional/carrier spectra, external longitudinal boost, dressed map, sealed orchestrator |
| Boost dynamics (1F-B) | `phase1f_b/` | Conditional, non-observational scalar dust-to-wall boost propagation with explicit fail-closed closures |
| Wall geometry (1F-C) | `phase1f_c/` | Conditional clock-anchored wall/common-spacetime kinematic geometry and optional scalar metric-trace reconstruction |
| Necessary bound (1F-D) | `phase1f_d.py` | Conditional scalar positive-core necessary-bound diagnostic in the explicit (t, b, C) parameterization; standard library only, no solver, root finder or time scan; a positive margin establishes no existence |
| Lagrangian σ(M) (1G-B) | `lagrangian_sigma.py` | Conditional, model-internal, mass-labelled linear σ(M). Mandatory, non-default `GrowthLaw`: volume-average CGI regular growing mode (comoving, or Mészáros comparator), or wall-regional EdS in common time t (closure `NOT_APPLICABLE`). Per-photon ω_m,eff identity, EH98 early spectrum as `PROVISIONAL_MODEL_IMPORT`, explicit radius conventions, flat-ΛCDM reference and explicitly anchored ratios. Barotropic closure refused (1G-A §4.1). Lives outside `growth/` so the 1D-B firewall test stays intact |
| LTB–CMC experiment (outside the phases) | `experimental_ltb_cmc/` | Isolated, conditional spherical LTB dust background with constant-mean-curvature slicing (BVP solver), tracker-clock comparison adapter, single-age section-family evolution, kappa_star and mixed sensitivities; imports only NumPy/SciPy and its own modules; distinct from 1F-D and promotes no scientific status |

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
functions, σ_R, σ8, fσ8, RSD/Kaiser mappings, bias, AP conversion, datasets,
covariances, likelihoods, fitting. **No fσ8-shaped diagnostic exists beyond
the conditional, externally anchored Candidate A** (`Q_anchor = f·A_anchor`,
Phase 1D-D, `growth/anchored_diagnostic.py`), which 1D-A conditionally
authorised and which stays non-observational; do not add another. Phase
1E-A's verdict on identifying Candidate A with observational fσ8 is
`NOT_JUSTIFIED_FOR_OBSERVATIONAL_USE`. The `transfer/`, `phase1f_a/`,
`phase1f_b/` and `phase1f_c/` runtimes are conditional research runtimes, not
Timescape predictions; their missing closures stay explicit external inputs.

**Authorised exception (Phase 1G-B, owner approval 2026-09-29).**
`lagrangian_sigma.py` computes a conditional, model-internal, mass-labelled
linear σ(M) with an explicit `PROVISIONAL_MODEL_IMPORT` early spectrum.
- Its outputs carry `NON_OBSERVATIONAL` and `NOT_OBSERVATIONAL_SIGMA_8`.
- No public name may contain `sigma8`, `sigma_8` or `8hMpc`.
- It is not an observational σ8, and `SIGMA8_AUTHORIZATION` stays
  `NOT_GRANTED`.

Everything else in the list above stays unimplemented.

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
- **Initial conditions (review F1):** the paper/notebook ICs transplant the
  ΛCDM growing-mode rate and so carry a decaying mode (Δ_d(t0) up to ~14%
  high). The explicit `TIMESCAPE_REGULAR_GROWING_MODE` convention removes it
  for the clean systems; reproduction keeps the legacy conventions.
- **Bare→dressed rate factor (review F2):** f_dressed/f_bare =
  (2+f_v)²/(4+f_v+4f_v²) peaks at 8/7 (dressed z ≈ 2.0); the "1.025–1.084"
  range in 1D-A/1D-C is superseded (`reports/phase1f_c_r_f2_f4_f9_remediation.md`).
- Reports and inventories older than a successor erratum are frozen
  historical records; the successor states the current reading.

## Key commands

```
# One-time setup (no .venv is checked in). Windows shown; on Linux/macOS use
# python3.X -m venv .venv and .venv/bin/python in place of .venv\Scripts\python
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -e ".[exec,test]"

# Full validation suite (1016 passed on Windows, Python 3.14.3 and 3.11.9, at
# the Phase 1G integration checkpoint; oracle and generated-artifact tests
# auto-skip when their inputs are absent)
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
.venv\Scripts\python scripts\validate_phase1f_b_dust_wall_boost_dynamics.py
.venv\Scripts\python scripts\validate_phase1f_c_r_astra_remediation.py [--producers]
.venv\Scripts\python scripts\validate_growing_mode_initial_conditions.py
.venv\Scripts\python scripts\validate_h1_kinematic_gates.py
```

The historical validators check ancestry against recorded commits, not branch
names (review F6): `validate_anchored_density_growth.py` regenerates from any
clean descendant of the 1D-D commit; `validate_phase1f_c_r_astra_remediation.py`
certifies base→remediation preservation, reports later drift, and reports
local-only provenance files or unpublished tags as absent rather than
crashing. The upstream notebook is identified by its line-ending-independent
hash (`UPSTREAM.lock` `notebook_sha256_lf`), so LF and CRLF checkouts agree.

Figure reproductions: `make_independent_fig1.py` (Fig. 1 + D2 forensic),
`make_clean_fig2.py`, `make_barotropic_fig3.py` (corrected c²_s, both D3
branches), `make_barotropic_fig3_forensic.py` (D2-corrupted, upstream
reproduction only). The `transfer/` and `phase1f_a/` layers produce no
figures; `validate_phase1f_a_h1_closure.py` regenerates its artifact
byte-for-byte.

## Hard constraints

- **Never push, publish, fork, or open PRs without explicit human approval**
  for that specific action (AGENTS.md rule 7 is the operative rule). An
  approval covers only the action it names; approved pushes go only to the
  designated branch.
- `.reference/` is a read-only clone of the upstream repo pinned in
  `UPSTREAM.lock` (no license — treat as all-rights-reserved). Never edit it,
  never commit it, never copy its source into package files.
- Never modify the original upstream notebook; executed or patched copies go
  to `artifacts/upstream/` with documented diffs.
- When reproducing upstream, do not change equations, constants, ICs, solver
  options, or plotting code. Record discrepancies exactly as found — do not
  "fix" them.

## Environment

- Primary development machine: Windows 11; Python launcher `py` (3.14
  default, 3.11 available). Linux/macOS work equally (`python3.X -m venv`,
  `.venv/bin/python`); remote sessions have used 3.13 + 3.11. The project
  venvs `.venv`/`.venv311` are git-ignored and must be created locally.
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
**1F-A** H1 carrier density, spectra, expansion and wall-boost closure ·
**1F-B** scalar dust-to-wall boost dynamics · **1F-C** wall/common-spacetime
geometry · **1F-C-R** Astra independent-audit remediation (v1, v2) ·
post-remediation independent review (`phase1f_c_r_post_remediation_independent_audit.md`,
findings F1–F9) and its fixes: F1 growing-mode ICs, F3 H1 kinematic gates,
F2/F4–F9 remediation (`phase1f_c_r_f2_f4_f9_remediation.md`; the three F4
audits were recovered and committed, §12) · **1F-D** minimal scalar
necessary-bound diagnostic (`phase1f_d_necessary_bound.md`, tag
`phase-1f-d-necessary-bound-v1`; conditional).

In progress (σ track; no adversarial audit or tag yet):
- **1G-A:** σ(M) derivation-path audit (report-only,
  `phase1g_a_sigma8_derivation_path_audit.md`). The route is standard early
  universe plus scale-independent growth; the barotropic closure is Hadamard
  ill-posed.
  - With owner approval (2026-09-29), `UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY`
    is `REFUTED_HADAMARD_ILL_POSED` (`phase1g_a_barotropic_status_successor.md`;
    the 1F-C-R validator reads the live value from that record).
  - The barotropic runtime and both D3 branches are unchanged.
- **1G-B:** conditional Lagrangian σ(M) runtime (`lagrangian_sigma.py`,
  `phase1g_b_lagrangian_sigma_validation.md`). It reproduces every 1G-A
  number.
- **1G-C:** two-scale growth law (report-only,
  `phase1g_c_two_scale_growth_law.md`).
  - The tracker is exactly empty Milne voids plus EdS walls in common time t.
  - σ8 lies inside [W09]'s ≈100 h⁻¹ Mpc dust cells, so mass-weighted σ(M8)
    follows the wall law: 0.83–0.96 (equal mass: 0.834 for [GM], 0.935 for
    the [NW15] CMB fit).
  - The volume-average CGI values, 0.52–0.69, are the super-cell growth.
  - The super-cell/sub-cell transition law is `NOT_DERIVED`.
- `SIGMA8_AUTHORIZATION` stays `NOT_GRANTED`.

Outside the phase sequence: the isolated, conditional **LTB–CMC experiment**
(`experimental_ltb_cmc/`). Its reports are `reports/experimental_ltb_cmc*.md`,
including the Italian research note
`experimental_ltb_cmc_p187_p189_prosecuzione.md`. It is distinct from 1F-D,
promotes no scientific status and has no phase tag.

Each entry maps to a `reports/phase<id>_*.md` file — read it before touching
the corresponding code.

## Reference material

- Upstream pin: `UPSTREAM.lock`; project overview and full file map:
  `README.md`
- Paper: arXiv:2511.17160v2 — Timescape numerics are Sec. 5.1, Figs. 1–3.
