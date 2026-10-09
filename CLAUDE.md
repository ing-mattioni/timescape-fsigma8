# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Scientific reproducibility project for Timescape linear perturbations
(arXiv:2511.17160, Galoppo & Mourier, JCAP 02 (2026) 066).

**Read `AGENTS.md` first — its ten rules are permanent, non-negotiable, and
outrank anything here.** In particular: never change an equation without a
paper reference and human approval; every implemented equation cites its
equation number; never silently change units, ICs, or sign conventions;
never make remote changes (push, fork, PR, issue or release) without
explicit human approval.

## How work is organised

Work proceeds in numbered phases (1A → 1G-G on main, F/G frozen at `8d3cdd0`), each of which is either
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
| Global linear variance (1G-H, experimental) | `global_variance.py` | Conditional, model-internal formal tangent statistic of the global contrast of Lagrangian top-hat regions (owner decision D1, 2026-10-07): exact two-phase identities, the tracker propagator `G = (1−p)D_W + p D_V` (A1–A5, void autonomy H-A6, seed-indexed void accounting H-A9), explicit void-share closures (constant, Gaussian-threshold seed), the constant-share interval from an adopted reading of the [W09] homogeneity premise, the complete two-phase covariance with cross terms, orthant integrals with an accuracy contract, the two-barrier alternative; records re-validate their fields and recompute their results from their stored inputs (GH-DF2). Experimental: imported by no other module; reuses `lagrangian_sigma` |
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
- No public function, class, member or output-key name may contain
  `sigma8`, `sigma_8` or `8hMpc` (case-insensitive). The negative status
  constants `SIGMA8_STATUS` and `FSIGMA8_STATUS`, whose values state the
  negation, are the only exception (owner decision GB-OD2, 2026-09-30).
- It is not an observational σ8, and `SIGMA8_AUTHORIZATION` stays
  `NOT_GRANTED`.

**Authorised experimental exception (Phase 1G-H, owner task of 2026-10-06).**
`global_variance.py` computes a conditional, model-internal *global-mean*
linear statistic — the formal tangent statistic, a proposed σ8 analogue
(`phase1g_h_global_variance_closure.md` §2, owner decision D1 of
2026-10-07) — for an explicitly supplied void-share closure. It is experimental (no other module imports it), its
outputs carry `NON_OBSERVATIONAL`, `NOT_OBSERVATIONAL_SIGMA_8` and
`EXPERIMENTAL_CONDITIONAL_RESEARCH_RUNTIME`, it follows the same naming rule,
and it changes no status token. Promotion, pull request, merge, freeze and
tagging remain open owner decisions (H-OD1…H-OD5); of H-OD5 the owner
approved only pushes to the session branch `ccr-555e67be-u11yht`
(2026-10-06, 2026-10-08 and 2026-10-09), and four independent audits
(2026-10-07, 2026-10-08 twice, 2026-10-09) were published on their own
branches.

Everything else in the list above stays unimplemented.

The firewall describes package runtimes and observational outputs. The
1G-C…1G-G report-evidence scripts explore explicitly conditional models;
they do not authorize a new production runtime, a physical default for an
unclosed law, or an observational statistic. The F/G evidence is
conditional research: independently audited (2026-10-02), delta-audited
(2026-10-06), merged by PR #4 and frozen at `8d3cdd0` (tags
`phase-1g-f-void-population-v1`, `phase-1g-g-void-evolution-v1`). The
freeze attests that checkpoint; it derives no σ8 and grants nothing.

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

# Full validation suite (1049 passed on Windows, Python 3.14.3 and 3.11.9,
# and on Linux, 3.13.12 and 3.11.15, at 63ca316; 1093 collected and passed on
# Windows after the Phase 1G owner decisions of 2026-09-30; oracle and
# generated-artifact tests auto-skip when their inputs are absent).
# F/G independent audit 2026-10-02: 1125 passed / 0 skipped / 0 failed
# on Windows 3.14.3 and 3.11.9 BEFORE the audit-remediation edits.
# Delta audit 2026-10-06 (phase1g_fg_remediation_independent_audit.md):
# 1136 passed / 0 skipped / 0 failed on both for the remediated tree.
# Final integrated-tree runs: phase1g_fg_remediation_integration.md.
# Freeze preflight at the PR #4 merge 8d3cdd0 (owner's report, 2026-10-06):
# 1136 passed / 0 skipped / 0 failed on Windows 3.14.3 (505 s) and 3.11.9
# (501 s), -W error (phase1g_fg_freeze_status_successor.md).
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

Phase 1G evidence scripts are `scripts\phase1g_*_numerics.py`. On Windows,
run the 1G-F one as `scripts\run_phase1g_f_portable.py`: the frozen script
imports the Unix-only `resource` module (owner approval 2026-09-30).
`scripts\phase1g_owner_decisions_numerics.py` recomputes what the owner
decisions of 2026-09-30 change (about 20 min: a 16-seed Monte Carlo).

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

σ track (remote state checked 2026-10-06): phases 1G-A…1G-E and the
2026-09-30 owner decisions were merged on `main` at
`fb5d95245bc0cb19ce6cd1438177f1a597bb232f` (PR #3); the annotated v1 tags
for 1G-A, B, C, D and E all resolve to that commit. The 2026-10-01 F
successor, the G research, the approved D successor, both F/G audits and
the remediation were merged by PR #4 at
`8d3cdd0533035858c42269cb1dff1a20dcafc7da` (tree identical to the phase
branch head `3d3d46e`) and frozen there: the signed annotated tags
`phase-1g-f-void-population-v1` and `phase-1g-g-void-evolution-v1` resolve
to that commit. Freeze preflight: 1136 passed, 0 skipped, 0 failed on
CPython 3.14.3 and 3.11.9 (owner's report). Status sentences in the F/G
records that predate the merge and freeze are resolved, without editing
them, in `phase1g_fg_freeze_status_successor.md`. F/G are frozen as
conditional results; the next phase toward σ8 is separate, and no
observational authorization changes. Read the successor reports for the
current interpretation; frozen records remain unchanged.
- **Adversarial audits of 1G-A to 1G-E** (2026-09-29; one independent
  auditor per phase, `reports/phase1g_<x>_adversarial_audit.md` + inventory;
  consolidation `phase1g_adversarial_audit_errata_successor.md`).
  - Every phase: `ACCEPT_WITH_CORRECTIONS`. No HIGH finding and no error in an
    implemented equation. The errata are applied as successor readings; the
    frozen reports are unchanged.
  - GB-F1 (a Linux-only bitwise-evenness test failure) was fixed with owner
    approval (2026-09-30, option A): the test compares with `rtol=1e-15`.
- **Owner decisions (2026-09-30).** One dated successor record per phase,
  `reports/phase1g_<x>_owner_decisions_successor.md` + inventory; evidence
  `scripts/phase1g_owner_decisions_numerics.py`.
  - Every blocking decision of 1G-A, 1G-C, 1G-D and 1G-E is applied as
    ticked; 1G-B's optional OD2–OD6 are applied as code with tests.
  - No token value, equation, IC or tolerance changes. Three token comments
    change: A5 (1G-C), the Mészáros/barotropic characterisation and the
    void-response figure (1G-D). Unticked options stay open (listed in each
    record).
- **Windows validation** (`phase1g_windows_validation_record.md`).
  - 1049 passed, 0 failed, 0 skipped on 3.14.3 and 3.11.9 at `63ca316` (plus
    the 1G-F runner), as on Linux; every recorded 1G-A…1G-F number
    reproduces.
  - The frozen 1G-F script imports the Unix-only `resource`: run it with
    `scripts/run_phase1g_f_portable.py` (owner approval 2026-09-30).
  - The decisions have since been merged and the 1G-A…1G-E v1 tags exist.
    The historical validation record retains its original pre-merge wording.
- **1G-A:** σ(M) derivation-path audit (report-only,
  `phase1g_a_sigma8_derivation_path_audit.md`). The route is standard early
  universe plus scale-independent growth; the barotropic closure is Hadamard
  ill-posed.
  - With owner approval (2026-09-29), `UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY`
    is `REFUTED_HADAMARD_ILL_POSED` (`phase1g_a_barotropic_status_successor.md`;
    the 1F-C-R validator reads the live value from that record).
  - The barotropic runtime and both D3 branches are unchanged.
  - Owner decisions: the App. B "backward-parabolic" verdict is
    `CONVENTION_DEPENDENT` (it holds for the printed (B.4) sign; under
    `RESOLVED_DERIVED_4_10` the closure is a constraint; author question).
    The [NW15] row is a declared hybrid with the Planck early universe;
    [NW15]'s own f_b ≈ 0.18 and n_s = 0.992 give 0.637–0.645 (wall law
    0.89–0.90) as a sensitivity. "αk ≈ 875" is a hybrid unit chain; 1G-A's
    own radius conventions give 557–694.
- **1G-B:** conditional Lagrangian σ(M) runtime (`lagrangian_sigma.py`,
  `phase1g_b_lagrangian_sigma_validation.md`). It reproduces every 1G-A
  number.
  - With owner approval (2026-09-29), results carry a documented limitation
    (1G-D §§5, 9; validation report §14). `VOLUME_AVERAGE_CGI` faithfully
    implements [GM]'s closure, but that closure fails the separate-universe
    test. `WALL_REGIONAL_EDS_COMMON_TIME` gives the wall-internal linear
    statistic, not a global-mean σ at 8 h⁻¹ Mpc.
  - The change is text only: the executable AST differs only in string
    constants, and every numeric output is bit-identical.
  - Owner decisions GB-OD2–OD6 (2026-09-30): the naming rule above; a
    hardened 1F-C-R status validator; real-numeric array inputs, the EH98
    ω_m fit range [0.025, 0.5] and record invariants; a `model_caveat` on
    `TimescapeGrowthFactor`; an independent g_TS regression. Every numeric
    output is bit-identical.
  - Contract-hardening successor (owner approval 2026-10-09, on finding
    GH-D3F4 of the third 1G-H delta audit;
    `phase1g_b_contract_hardening_successor.md`): `LCDMReferenceLinearSigma`
    refuses non-finite or unbound quadrature diagnostics and
    `AnchoredLagrangianSigmaRatio` binds its ratios, offset and listed
    early-spectrum differences to its stored records. Record invariants
    only; the 1G-B validation artifact is byte-identical.
- **1G-C:** two-scale growth law (report-only,
  `phase1g_c_two_scale_growth_law.md`).
  - Kinematically, the tracker is empty Milne voids plus EdS walls in common
    time t ([W07]); its dynamics are exact under the regional dust-FLRW
    assumption (`DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`).
  - σ8 lies inside [W09]'s ≈100 h⁻¹ Mpc dust cells. The wall law gives the
    wall-internal linear σ at mass M8, relative to the wall mean (not a
    global-mean σ8): 0.834 for [GM] and 0.935 for the [NW15] CMB fit at
    equal mass, under A1–A5 (A5: the wall matter clocks the common time t).
    The "supersedes", "settled" and "0.83–0.96" readings are withdrawn.
  - The volume-average CGI values, 0.52–0.69, are [GM]'s CGI growth, not the
    super-cell law (1G-D).
  - The super-cell/sub-cell transition law is `NOT_DERIVED`.
  - Tokens (owner approval 2026-09-29):
    - `TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW = DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`
      (§5), narrowed by 1G-D §9 to the wall-internal linear statistic;
      A5 added to its comment (2026-09-30);
    - `SUPER_CELL_TO_SUB_CELL_GROWTH_TRANSITION = NOT_DERIVED` (§8). 1G-D §8
      gives a conditional length scale, not the law.
- **1G-D:** separate-universe structure (report-only,
  `phase1g_d_separate_universe_growth.md`).
  - The tracker has one time scale: `f_v = t/(t+τ)`, with τ = 1F-D's `b`.
  - The wall-curvature mode (`f_w δ_w`) and the void-onset mode (`ε f_v`)
    are exact k→0 solutions of [GM] (4.9)–(4.11). That they are *the*
    long-wavelength modes rests on assumption S1
    (`DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`; [GM] l. 620 makes walls flat).
  - Under S1, **[GM]'s comoving closure admits no separate-universe mode,
    and the Mészáros (δQ = 0) and barotropic conditions hold only for
    decaying modes,** so the volume-average CGI growth is not Timescape's
    long-wavelength growth.
  - Peak-background-split void response with the tracker-consistent seed
    and f_vi = f_v(t_LS) (owner decisions 2026-09-30): A_v ≈ 1.2×10³,
    X_SU = 1.26–1.28, 10% density at 61–84 h⁻¹ Mpc (the [SvdW04] seed
    factor gives 172–215). Reading [W09]'s single-perturbation relation as a
    response is not viable.
  - At 8 h⁻¹ Mpc the conditional void response is non-perturbative
    (A_v σ_LSS(R8) = 1.05–1.11; 3.8–4.6 with the [SvdW04] factor).
    The R8 < R_void argument assumes the older large-void population and
    does not transfer to F's much smaller median. The closure constructs
    σ_wall; it has not constructed a global-mean linear statistic. This is
    not a theorem excluding any linearly extrapolated statistic. Token
    reclassification below is approved in the 2026-10-02 D successor
    (`phase1g_d_linear_statistic_status_successor.md`).
  - Tokens (owner approval 2026-09-29):
    - `GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY = FAILED_FOR_TIMESCAPE_TRACKER` (§5);
    - `TWO_SCALE_SUPER_CELL_GROWTH_LAW = DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` (§6);
    - `VOID_ONSET_RESPONSE = EXTERNAL_CLOSURE_INPUT` (§7);
    - `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC = NOT_DERIVED`
      (2026-10-02 approved successor to the frozen §9 classification).
- **1G-E:** two-phase mass variance (report-only,
  `phase1g_e_two_phase_sigma.md`).
  - Formula (mass-conserving, owner decision 2026-09-30):
    `σ² = δ_v² σ²_part + (f_w − f_v δ_v)² σ²_int`, equal to the frozen form
    for empty voids, with Boolean voids and the wall-internal linear field
    compressed by `s = D_wall` (photon frame; `f_w^{1/3}` and 1 are a
    two-sided sensitivity).
  - Reference: the 1G-F volume-weighted grain-radius shape, σ ≈ 0.99 in 8 h⁻¹ Mpc balls
    (0.88–1.05 at equal mass). A single 15 h⁻¹ Mpc radius at the full f_v0
    is an idealisation, not a [W09] statement: 1.76 ([GM]) and 1.52 ([NW15]),
    1.60 and 1.59 at equal mass. The range is 0.8–2.1.
  - This is a conditional, hybrid (nonlinear partition, linear wall field),
    model-internal quantity.
- **1G-F:** conditional excursion-set void population (report-only;
  frozen `phase1g_f_void_population.md`, corrected reading in
  `phase1g_f_volume_budget_successor.md`, 2026-10-01 successor; frozen at
  `8d3cdd0`, tag `phase-1g-f-void-population-v1`).
  - Excursion-set voids ([SvdW04] two barriers; [JLH13]'s corrected EdS
    shell crossing δ_v = −2.717, r_NL/r_L = 1.697) from the 1G-A early
    spectrum, with the growth clock as an explicit closure (wall EdS in t,
    volume-average CGI, 1G-D separate-universe response).
  - The void mass fraction 1 − 𝒟 is clock-independent. The two-scale budget
    gives f_v=0.751969 for the primary full population; [JLH13]'s Vdn
    mapping gives ≤0.38. Matching a selected radius range to the supplied
    tracker fraction is not a prediction of its full population history.
  - Fixed-domain cumulative volumes use `m_>r/[x(1-m_total)+m_total]`.
    Frozen M3 radius-cut values instead reclassify excluded void mass as
    wall mass and remain valid only as separate truncated-universe budgets.
  - With the wall clock the voids are small (median 2.4–2.8 h⁻¹ Mpc;
    ≥10 h⁻¹ Mpc voids fill 1.48% / 1.92% in the primary fixed domain),
    and no fixed threshold reproduces f_v(t) over z=0–3 under either
    cutoff meaning in this conditional C1 model.
  - The conditional hybrid variance at 8 h⁻¹ Mpc remains ≈0.99: a
    shell-crossing size shape, externally supplied tracker f_v0, empty
    Boolean grains and a linear wall field. The grains overlap and have an
    independently calibrated eta=−ln(1−f_v0), so they are not F's disjoint
    population. They share only its volume-weighted grain-radius shape.
    The F correction alone changes
    no variance input. Frozen verdict 2 now separates the derived Milne-rate asymptote from the
    `NOT_DERIVED` identification with exactly empty finite-time tracker
    voids (owner approval 2026-10-02); about
    89–91% of the variance is the extrapolated linear wall contribution.
  - Frozen C3 tracker-seed tables use the older wall-amplitude normalization;
    the current D owner decision uses total delta_L (X_SU=1.26–1.28).
    The primary C1 results do not use C3. No F token is added.
- **1G-G:** report-only evolution research (`phase1g_g_void_evolution.md`;
  frozen at `8d3cdd0`, tag `phase-1g-g-void-evolution-v1`).
  - Additive mergers conserve the first void-volume moment; they can change
    sizes but cannot fix the full-volume history at a prescribed common,
    size- and age-independent regional void expansion rate.
  - Milne/EdS regional volumes reproduce the tracker only with a supplied
    normalization. A synchronous shell-crossing cohort gives 2/3 of its
    fractional growth rate; this is not F's epochwise threshold population.
    The required transfer is J/V=f_v(1-f_v)/(3t) at that instant. In the
    homogeneous interior continuation the coefficient increases toward 1;
    the normalized missing source decreases from its upper bound 1/3.
  - Finite seed mass cannot silently become exact finite-time vacuum.
    Formation, volume/mass transfer, regional dynamics, clock embedding
    and spatial correlations remain explicit missing inputs.
  - A constant-kernel analytic merger example is a tested benchmark, not
    a chosen Timescape law or an evolution of the F population.
  - F/G scripts and tests are research evidence only; see
    `phase1g_fg_successor_validation.md` and `phase1g_fg_audit_remediation.md`.
    The original tree was audited with corrections required (2026-10-02).
    The remediated tree passed an independent delta audit with no
    integration blocker (2026-10-06, `phase1g_fg_remediation_independent_audit.md`).
    Residual corrections and the phase-branch integration are recorded in
    `phase1g_fg_remediation_integration.md`. G adds no package API or status;
    the separate approved D successor changes one classification. The merge
    (PR #4), freeze and tags followed on the owner's separate authority
    (`phase1g_fg_freeze_status_successor.md`); no release exists.
- **1G-H (proposed; pushed with owner approvals of 2026-10-06, 2026-10-08 and
  2026-10-09 to the session branch `ccr-555e67be-u11yht` (last recorded
  publication event P11, `ed0ec0c`; record `phase1g_h_publication_successor.md`,
  events P1–P13; summaries name the last recorded event, not the remote head),
  developed locally as `phase-1g-h-global-variance-closure`; independently
  audited 2026-10-07 (`phase1g_h_independent_audit.md`, published by the owner on
  `phase-1g-h-independent-audit` at `816dd00`) and remediated
  (`phase1g_h_audit_remediation.md`); delta-audited 2026-10-08
  (`phase1g_h_delta_audit.md`, published with the owner's authorisation on
  `phase-1g-h-delta-audit` at `5c325e1`) and remediated on top of it
  (`phase1g_h_delta_audit_remediation.md`, pushed in P7); second delta audit
  2026-10-08 (`phase1g_h_delta_audit_2.md`, published on the owner's
  instruction on `ccr-ac582de6-vho99i` at `e517028`) and remediated on top
  of it (`phase1g_h_delta_audit_2_remediation.md`, pushed in P10); third
  delta audit 2026-10-09 (`phase1g_h_delta_audit_3.md`, OpenAI GPT-6 family,
  published on `phase-1g-h-delta-audit-3` at `18bf2fb`) and remediated on
  top of it (`phase1g_h_delta_audit_3_remediation.md`, with the separate
  `phase1g_b_contract_hardening_successor.md`); not merged into `main`,
  frozen or tagged; no pull request):** global
  matter-variance definition and minimal closure
  (`phase1g_h_global_variance_closure.md`, inventory, validation record;
  runtime `global_variance.py`; evidence
  `scripts/phase1g_h_global_variance_closure_numerics.py`; single cases
  `scripts/phase1g_h_global_variance_case.py` with `scripts/phase1g_h_configs/`).
  - Audit (2026-10-07): `REJECT` of the closure claims of the text at
    `d4d693d`, every other area `ACCEPT_WITH_CORRECTIONS`, 15 findings (GH-F1
    HIGH; GH-F2, F4, F5 MEDIUM-HIGH); the numbers reproduced. Owner decisions
    D1–D4 (2026-10-07, "Procedi, usa le scelte raccomandate per i punti 1-4")
    are applied. The owner confirmed the two recorded push approvals on
    2026-10-08 (GH-F15, "Si, confermo"), and again directly to the second
    delta auditor ("Confermo le due approvazioni di push registrate
    (GH-F15)"; `RESOLVED_OWNER_CONFIRMED`).
  - Delta audit (2026-10-08): `REJECT` of the remaining claim that the
    nonnegative pairs share the wall-density covariance and of the
    completeness claims; provenance and numerics `ACCEPT`, other areas
    `ACCEPT_WITH_CORRECTIONS`; of GH-F1…F15, 8 resolved, 6 partly, 1 open;
    six new findings, all corrections (GH-DF1 MEDIUM-HIGH: lognormal
    constraint; DF2: records not bound to inputs; DF3: §8 contradictions;
    DF4: integrated vs pointwise scale dependence; DF5: tests; DF6: summary
    qualifier). Applied with owner approval ("Perfetto, procedi"): records
    recompute their results from their inputs; the pairs fix the carrier law;
    identity (H25); first radial panel included; 42 phase tests, 36 gates.
  - Second delta audit (2026-10-08; same model family as the author,
    procedural independence only): `ACCEPT_WITH_CORRECTIONS`, no scientific
    blocker; GH-DF1…DF6 and GH-F3…F14 resolved, GH-F15 confirmed; two LOW
    (GH-D2F1: push P7 unrecorded; D2F2: weakly protected new quantities and
    gates) and four INFO findings (D2F3: regression counts; D2F4: a
    `Fraction` passed the binding and broke strict JSON; D2F5: historical
    wording; D2F6: name the missing input as the mask–carrier dependence).
    Applied with owner approval ("Perfetto, procedi"): publication events
    P7–P9; float results must be floats; the (H25) gate is a consistency
    check of the (H18) assembly; 49 phase tests, 36 gates; no number changes.
  - Third delta audit (2026-10-09; OpenAI GPT-6 family):
    `ACCEPT_WITH_CORRECTIONS`, SCIENCE `ACCEPT`, no scientific blocker; the
    blind cross-family reconstruction of §6 and of the main conditional
    values is `CROSS_FAMILY_VERIFIED_WITH_DEVIATION` (58/58; the deviation
    is the auditor's own initial recipe). GH-D2F1 and D2F4 partly
    resolved, the rest resolved; findings GH-D3F1 (LOW: P11 and stale
    remote-head summaries), D3F2 (LOW: nested inputs broke strict JSON),
    D3F3 (LOW: test gaps), D3F4 (LOW-MEDIUM, owner decision: unbound fields
    in two frozen 1G-B records), D3F5 (INFO: C_W − 1 is a product-moment
    excess, not a centred covariance). Applied with owner approval
    ("Perfetto, procedi", option (a) for D3F4): events P11–P13 and the
    last-recorded-event convention; every H record refuses a non-strict-JSON
    export; 53 phase tests; key `both_walls_product_moment_excess_ball`; a
    1G-B contract-hardening successor (two records, outputs bit-identical).
    Open: the Windows gate, H-OD1…H-OD5.
  - A (definition) proposed, not closed (D1): the formal tangent statistic —
    the early Gaussian field propagated with the zero-amplitude tangent of
    the global contrast `(M_L/V_L)/(M_D/V_D) − 1` of Lagrangian top hats,
    smoothing rule `G_R = G W(kR)`, dust foliation, common time, global
    volume mean; preferred radius `8 h̄⁻¹ Mpc` of present volume-average
    proper length (`R_proper·H_D0 = 800 km/s`, `R_proper = γ_w0 R`). It is
    not the ensemble-mean response of the true contrast (GH-F1).
  - Derived within the tangent model (A1–A5, void autonomy H-A6,
    seed-indexed void accounting H-A9 = D2): the propagator is
    `G = (1−p)D_W + p D_V`; D_W = 0.2306 / 0.3527, D_V = 7.133 / 11.33
    ([GM] / [NW15]). Void/region radius ratios at R8 are 0.33 / 0.39 (1G-F
    median) and 1.49 / 1.59 ([W09]): the sub-cell extension holds for the
    seed-indexed statistic, not the material-domain volume (GH-F2). With
    exact empty voids and the early field, wall-density freedom is needed
    below ≈ 99 / 127 h⁻¹ Mpc; this does not select the full S1 (GH-F7).
  - B (formal statistic) closed only given the void share p, defined by
    `p δ_L = f_v,LS ε` (`p = f_v,LS − ∂f_v,L/∂δ_L`, GH-F3; 1G-D's
    `VOID_ONSET_RESPONSE`, still `EXTERNAL_CLOSURE_INPUT`): at 8 h̄⁻¹ Mpc,
    direct normalisation (D4), 1.121 / 1.057 (1G-D's [W09]-radius seed, a
    formal extrapolation, H-A8), 0.811 / 0.816 (1G-F median as a heuristic
    seed-scale prior, below the adopted ε = 1 threshold with no controlled
    error estimate); constant-share interval [0.261, 0.998] /
    [0.369, 1.162] under H-A7 and the adopted 10%-at-100 reading, not a
    bound for scale-dependent shares (GH-F4). Planck normalisation:
    post-hoc at fixed closure (×0.970577) and PBS reclosure reported beside
    them (GH-F6).
  - Two-phase covariance with cross terms; the signed Gaussian pair (0.97 vs
    0.39) has negative wall densities (P ≈ 0.45); nonnegative lognormal
    pairs sharing f_v0, the partition covariance and the latent carrier law
    (not the conditionally normalised wall-density covariance, ratio
    1/m_II² with m_II = 1.6–2.9, GH-DF1) give law II / law I = 0.92–1.29.
    By (H25) the total depends on P11(r) and the both-walls conditional
    density correlation C_W(r): the nonlinear hybrid variance needs the
    joint law of geometry and density (GH-F5).
  - C (prediction, observation) not reached; owner decisions H-OD1…H-OD5 in
    §9 (H-OD2, H-OD3 recommendations revised with the audit and confirmed by
    the delta audit: no reference value, tokens deferred). No token,
    authorization, equation or frozen record changes.
- **Status-token additions:** the six 1G-C/1G-D tokens are *additions*, not
  changes (`phase1g_status_additions_successor.md`). The frozen 1F-C-R
  snapshot has no entry for them. The 1F-C-R validator accepts a new token
  only if a registered successor record declares it; it must still be absent
  from the snapshot. The live value must match the addition or its explicitly
  linked approved successor, preserving the original added value. One D
  token was reclassified on 2026-10-02; duplicate claims remain rejected.
  - With owner approval (2026-09-29, a separate record,
    `phase1g_e_status_addition_successor.md`), the 1G-E proposal
    `TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC = DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`
    (assumptions E1–E4) is added the same way. It is the seventh addition;
    the validator now registers four successor records including the D change.
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
