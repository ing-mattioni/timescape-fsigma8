# timescape-fsigma8

Reproducibility project for linear perturbation growth in the Timescape
cosmological model, based on:

> M. Galoppo & P. Mourier, *Cosmological perturbations on an averaged
> background*, JCAP 02 (2026) 066, arXiv:2511.17160.

## Current status: Phase 1G — conditional sigma(M) and void-population research

The scientific foundation through 1F-C-R is recorded in
[the successor remediation report](reports/phase1f_c_r_astra_audit_remediation.md)
and its [machine-readable inventory](reports/phase1f_c_r_astra_audit_remediation_inventory.json).
Earlier reports and inventories are preserved historical checkpoints; their
source attributions and physical-compatibility claims are superseded by this
record where specified. The accepted 1F-C realization and kinematic verdict
remain unchanged. A minimal conditional
[Phase 1F-D scalar necessary-bound diagnostic](reports/phase1f_d_necessary_bound.md)
is now available in `timescape_fsigma8.phase1f_d`. It tests only the strict
positive-core margin; a positive result does not establish existence or
physical compatibility. No Phase 1F-D geometric or perturbative solver is
implemented, and the frozen scientific statuses are preserved.

**σ(M) track:** phases 1G-A…1G-E and the 2026-09-30 owner decisions were
merged on `main` at `fb5d952` (PR #3); the 1G-A…1G-E annotated v1 tags
resolve to that commit. The F correction and G research linked below,
independently audited (2026-10-02) and delta-audited (2026-10-06), were
merged by PR #4 and frozen at `8d3cdd0`: the signed annotated tags
`phase-1g-f-void-population-v1` and `phase-1g-g-void-evolution-v1` resolve to
that commit, and the freeze preflight there gave 1136 passed, 0 skipped,
0 failed on CPython 3.14.3 and 3.11.9 (owner's report). F/G are frozen as
conditional results; the next phase toward σ8 is separate, and no
observational authorization changes. Status sentences in the F/G records
that predate the freeze are resolved in the
[freeze-status record](reports/phase1g_fg_freeze_status_successor.md).
- **Route.** The [σ(M) derivation-path audit](reports/phase1g_a_sigma8_derivation_path_audit.md)
  follows the authors' own proposal: standard early-universe physics, then
  scale-independent growth.
- **Runtime.** A conditional, model-internal, mass-labelled linear σ(M)
  runtime is available in `timescape_fsigma8.lagrangian_sigma`
  ([validation](reports/phase1g_b_lagrangian_sigma_validation.md)).
- **Two-scale structure.** [Phase 1G-C](reports/phase1g_c_two_scale_growth_law.md)
  shows that, kinematically, the tracker is empty Milne voids plus
  Einstein–de Sitter walls in common time; its dynamics are exact under the
  regional dust-FLRW assumption.
- **Results.** The wall-internal linear σ at the Planck 8 h⁻¹ Mpc mass,
  relative to the wall mean, follows the wall-regional growth law: 0.834
  ([GM]) and 0.935 ([NW15]) with a Planck early universe, under assumptions
  A1–A5 (A5: the wall matter clocks the common time). It is not a
  global-mean σ8.
- **Phase 1G-D** ([separate-universe audit](reports/phase1g_d_separate_universe_growth.md)):
  - under its separate-universe assumption S1, the paper's CGI closures fail
    Timescape's own long-wavelength consistency test, so the volume-average
    values (0.52–0.69) are not Timescape's large-scale growth;
  - with a peak-background-split void response and a tracker-consistent
    void seed, the 10% homogeneity scale is 61–84 h⁻¹ Mpc (172–215 with the
    [SvdW04] seed factor);
  - at 8 h⁻¹ Mpc the conditional void response is non-perturbative
    (|ε| ≈ 1). Its older large-void scale argument does not apply unchanged
    to F's smaller median. The current closure constructs a wall-internal
    linear statistic; a global-mean linear statistic remains unconstructed.
    The owner-approved [D successor](reports/phase1g_d_linear_statistic_status_successor.md)
    (2026-10-02) records `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC = NOT_DERIVED`;
    all observational authorizations remain `NOT_GRANTED`.
- **Phase 1G-E** ([two-phase mass variance](reports/phase1g_e_two_phase_sigma.md)):
  empty Boolean voids plus the wall-internal field, with a mass-conserving
  formula. With the 1G-F grain-radius shape σ ≈ 0.99 in 8 h⁻¹ Mpc
  spheres; a single 15 h⁻¹ Mpc void radius, an idealisation, gives
  1.52–1.76 (0.8–2.1 across the sensitivities). This is a conditional,
  hybrid quantity, not an observational σ8.
- **Phase 1G-F** ([frozen void-population report](reports/phase1g_f_void_population.md),
  [volume-budget successor](reports/phase1g_f_volume_budget_successor.md)):
  an excursion-set void size distribution from the same early spectrum,
  with the growth clock as an explicit closure. Correct cumulative volumes
  keep the full-population denominator fixed: primary voids >=10 h⁻¹ Mpc
  fill 1.48% (GM) / 1.92% (NW15); all sizes fill 0.751969 in both cases.
  No fixed cutoff matches z=0–3 under this conditional C1 model. The two-phase variance
  remains ≈0.99, conditional on the shell-crossing size shape, an externally
  supplied tracker fraction, overlapping empty Boolean grains and a linear
  wall field. The grains share F's volume-weighted radius shape, but have
  separately calibrated eta = −ln(1−f_v0); they are not F's disjoint cells.
  Their dynamical connection is not derived. Frozen F verdict 2 is explicitly
  split: the Milne-rate asymptote is derived; identification with exactly
  empty finite-time tracker voids is `NOT_DERIVED`.
- **Phase 1G-G** ([population-evolution research](reports/phase1g_g_void_evolution.md)):
  additive mergers conserve total void volume at the merger instant. At a
  prescribed common void expansion rate they cannot change its history by
  size redistribution alone.
  The report derives the volume/mass transfer constraints needed to connect
  finite-density seeds to the tracker, with a tested analytic kinetic
  benchmark. It does not select a Timescape merger law or predict σ8.
  [Local validation and integration status](reports/phase1g_fg_successor_validation.md).
- **Adversarial audits** of 1G-A to 1G-E (one independent auditor per phase;
  [consolidation](reports/phase1g_adversarial_audit_errata_successor.md)):
  every phase is accepted with corrections. No implemented equation is in
  error; the main findings concern interpretation and inputs (the 1G-C wall
  σ, the 1G-D void-seed scale, the 1G-E non-empty-void formula and void
  population).
- **Owner decisions** (2026-09-30), one successor record per phase:
  [1G-A](reports/phase1g_a_owner_decisions_successor.md),
  [1G-B](reports/phase1g_b_owner_decisions_successor.md),
  [1G-C](reports/phase1g_c_owner_decisions_successor.md),
  [1G-D](reports/phase1g_d_owner_decisions_successor.md),
  [1G-E](reports/phase1g_e_owner_decisions_successor.md). No token value,
  equation or tolerance changes in those decisions; the numbers above also
  include the separately identified 2026-10-01 F successor.
- **F/G independent audit, remediation and delta audit** (2026-10-02 /
  2026-10-06):
  [audit](reports/phase1g_fg_independent_scientific_audit.md),
  [approved corrections](reports/phase1g_fg_audit_remediation.md),
  [delta audit](reports/phase1g_fg_remediation_independent_audit.md),
  [integration record](reports/phase1g_fg_remediation_integration.md).
  - The first audit's 1125/0/0 full-suite results certify the
    pre-remediation tree.
  - The delta audit found no integration blocker and certifies the
    remediated tree (1136/0/0 on Python 3.14.3 and 3.11.9).
  - The integration record holds the final-tree runs and the residual
    corrections.
  - Merged by PR #4 and frozen at `8d3cdd0` (tags
    `phase-1g-f-void-population-v1`, `phase-1g-g-void-evolution-v1`;
    [freeze-status record](reports/phase1g_fg_freeze_status_successor.md)).
    No release exists.
- **Windows validation** ([record](reports/phase1g_windows_validation_record.md)):
  both interpreters pass the full suite, as on Linux, and every recorded
  1G-A…1G-F number reproduces.
- **Status tokens.** With owner approval (2026-09-29), six tokens record the
  1G-C/1G-D findings
  ([successor record](reports/phase1g_status_additions_successor.md)):
  - `TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW` and
    `TWO_SCALE_SUPER_CELL_GROWTH_LAW` are `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`;
  - `SUPER_CELL_TO_SUB_CELL_GROWTH_TRANSITION` is `NOT_DERIVED`;
  - `GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY` is `FAILED_FOR_TIMESCAPE_TRACKER`;
  - `VOID_ONSET_RESPONSE` is `EXTERNAL_CLOSURE_INPUT`;
  - `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` is
    `NOT_DERIVED` following the registered, owner-approved 2026-10-02 D
    successor; its original addition value remains in the frozen record.

  The σ(M) runtime's results now state the matching limitation of each
  growth law (text only; the numbers are unchanged). A seventh token,
  `TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC = DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`,
  records the 1G-E two-phase variance under its assumptions E1–E4
  ([successor record](reports/phase1g_e_status_addition_successor.md)).
- **Status.** These are conditional numbers, not an observational σ8, and no
  σ8 authorization is granted.
- **Phase 1G-H (proposed; on the branch `ccr-555e67be-u11yht`, pushed with
  owner approvals on 2026-10-06, 2026-10-08 and 2026-10-09; last recorded
  push P15, `027b7a4`, in the publication record; independently
  audited on 2026-10-07 and remediated; delta-audited on 2026-10-08 and
  remediated; a second delta audit the same day and a third and a fourth,
  cross-family, delta audit on 2026-10-09 accepted it with corrections,
  which are applied;
  not merged into `main`, frozen or tagged)**
  ([report](reports/phase1g_h_global_variance_closure.md),
  [validation](reports/phase1g_h_global_variance_closure_validation.md),
  [audit](reports/phase1g_h_independent_audit.md),
  [remediation](reports/phase1g_h_audit_remediation.md),
  [delta audit](reports/phase1g_h_delta_audit.md),
  [delta remediation](reports/phase1g_h_delta_audit_remediation.md),
  [second delta audit](reports/phase1g_h_delta_audit_2.md),
  [second remediation](reports/phase1g_h_delta_audit_2_remediation.md),
  [third delta audit](reports/phase1g_h_delta_audit_3.md),
  [third remediation](reports/phase1g_h_delta_audit_3_remediation.md),
  [fourth delta audit](reports/phase1g_h_delta_audit_4.md),
  [fourth remediation](reports/phase1g_h_delta_audit_4_remediation.md),
  [1G-B hardening](reports/phase1g_b_contract_hardening_successor.md),
  [publication](reports/phase1g_h_publication_successor.md)):
  - *Audits.* The independent audit rejected the closure claims of the
    audited text (definition "closed", structure "derived", interval
    "closure-independent", Gaussian laws as physical densities) and accepted
    the rest with corrections; the numbers reproduced. The owner's decisions
    D1–D4 (2026-10-07) were applied. The delta audit (2026-10-08) rejected
    the remaining claim that the nonnegative pairs share the wall-density
    covariance and the completeness claims, and asked for record binding,
    tests and wording fixes; all six of its findings are corrections, now
    applied. The second delta audit (2026-10-08, same model family as the
    author) found them resolved and no scientific blocker; its two LOW and
    four INFO findings (publication record, tests, typed records, wording)
    are applied. The third delta audit (2026-10-09, OpenAI GPT-6 family)
    reproduced Sec. 6 and the main conditional values independently (58 of
    58 quantities) and found no scientific blocker; its corrections (a
    publication convention, strict JSON for nested inputs, tests, wording)
    are applied, and by owner decision a separate successor hardens two
    1G-B record contracts with bit-identical outputs. The fourth delta audit
    (2026-10-09, OpenAI GPT-6 family) found those corrections resolved, every
    earlier finding unregressed and no scientific blocker; its two LOW and
    one INFO findings (tests for two strict-JSON guards, scoped wording) are
    applied, with a one-ULP test of the 1G-B bindings. The owner's Windows
    gate and the decisions on pull request, merge, freeze and tag remain
    open.
  - *Definition (proposed).* The formal tangent statistic: the rms of the
    early Gaussian field propagated with the zero-amplitude tangent of the
    global contrast of Lagrangian top-hat regions (dust foliation, global
    volume mean), with the smoothing rule G_R = G·W(kR) — the analogue of
    ΛCDM's linear σ8, not the ensemble-mean response of the true contrast.
    Preferred radius 8 h̄⁻¹ Mpc of present volume-average proper length
    (R_proper·H_D0 = 800 km/s).
  - *Derived within that model.* Under the regional wall/void laws, void
    autonomy and seed-indexed void accounting, every Lagrangian region has
    the propagator G = (1−p)D_W + p D_V, with D_W = 0.231 / 0.353 and
    D_V = 7.13 / 11.3 ([GM] / [NW15]); p (defined by p δ = f_v ε) is the one
    missing input (1G-D's void-onset response, an external closure). Void
    radii are not small against R at 8 h̄⁻¹ Mpc, so the sub-cell extension
    holds for the seed-indexed statistic only.
  - *Conditional values* at 8 h̄⁻¹ Mpc (direct normalisation): 1.121 / 1.057
    with 1G-D's seed closure (a formal extrapolation of the void response),
    0.811 / 0.816 with the 1G-F void size as a heuristic seed scale (its
    void response lies below the adopted ε = 1 threshold, with no
    controlled error estimate); the constant-share interval
    [0.26, 1.00] / [0.37, 1.16] under an adopted
    reading of the background's homogeneity premise, which does not bound
    scale-dependent shares. Not observational; owner decisions in the report
    (§9).
  - *Nonlinear variance.* Joint laws sharing the volume fraction, the
    partition covariance and the wall carrier law give different
    8 h⁻¹ Mpc variances: 0.97 vs 0.39 for a signed Gaussian surrogate
    (negative densities), law II / law I = 0.92–1.29 for nonnegative
    lognormal laws (which do not share the conditionally normalised
    wall-density covariance). The difference lies in the both-walls
    conditional density correlation, i.e. the joint law of geometry and
    density.
  - Experimental runtime `timescape_fsigma8.global_variance`; one case:
    `python scripts/phase1g_h_global_variance_case.py --config scripts/phase1g_h_configs/gm_bare_pbs_f_median_seed.json`.

Imported regional dust-FLRW equations are conditional on their regional
backgrounds. Their physical embedding into the common Timescape spacetime,
zeroth-order dust/wall background coincidence, all-time transfer/constitutive
compatibility, and a physical Timescape trajectory remain **NOT_DERIVED**.
The naive W09 regional common-time EdS scale interpreted as exact proper-time
flat dust using the W09 wall lapse is **REJECTED_UNSUPPORTED**.
Manufactured H1 jets establish algebraic compatibility only.

Remaining closures include regional/common background and source embedding;
all-time transfer/constitutive compatibility; H1-to-wall/dressed spatial and
density maps; perturbative wall lapse; local scale/Hubble and perturbed
geometry; initial, boundary, kernel and morphology data; and future
lightcone, tracer and statistical inputs. Lapse and pullback callbacks are
not an exhaustive irreducible-input theorem. No unique Timescape prediction
or observational, RSD, sigma8 or fsigma8 authorization is granted.

Ranks 4, 5 and the optional +1=6 count differential field species, not freely
selectable admissible initial functions after constraints and supplied
histories. Conditional forward uniqueness assumes complete admissible data;
it is not a trajectory-existence result. Finite-mode barotropic ODE uniqueness
does not establish continuum stability, and Phase 1G-A refutes it
([§4.1](reports/phase1g_a_sigma8_derivation_path_audit.md)): with the negative
corrected sound speed the unrestricted barotropic Cauchy problem is Hadamard
ill-posed (a mode of wavenumber k grows like exp(kα), α = 1.70695 from z = 20
to today in dressed H0 = 1 units), so no linear barotropic σ_R exists.
`UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY` is therefore
`REFUTED_HADAMARD_ILL_POSED` (human approval 2026-09-29;
[successor record](reports/phase1g_a_barotropic_status_successor.md)). The
finite-mode barotropic runtime and both D3 branches are unchanged and remain
required for Fig. 3 reproduction.

Phase 1F-C acceleration arrays explicitly distinguish coordinate covectors,
coordinate contravariant components and physical orthonormal components in
the same inverse-metric Cholesky frame as 1F-B. Optional C_W reconstruction
requires a caller-declared linear-regime limit and positive `1+2C_W` at every
accepted output time. These are validity gates, not new scientific dynamics.

### Post-remediation independent review and fixes

An independent review of Phases 1A–1F-C-R
([report](reports/phase1f_c_r_post_remediation_independent_audit.md),
findings F1–F9) confirmed the paper-level equations and every re-computed
number, and raised nine findings. They have been addressed as follows:

- **F1:** the paper ICs carry a decaying mode. An explicit, non-default
  `TIMESCAPE_REGULAR_GROWING_MODE` convention now exists for the clean
  systems ([validation](reports/phase1f_c_r_f1_growing_mode_initial_conditions_validation.md)).
- **F3:** the H1 runtime now gates `J_Xi = 0` and 13 background identities.
  Only enforced results carry closure status tokens
  ([validation](reports/phase1f_c_r_f3_h1_kinematic_gates_validation.md)).
- **F2, F4–F9:** a successor erratum, provenance records, checkout-independent
  reproducibility gates, mandatory `G`, and refreshed documentation
  ([remediation](reports/phase1f_c_r_f2_f4_f9_remediation.md)). F4 is closed
  as a documented permanent gap: three specifications and any H1 decision
  record are confirmed unavailable. The three audits were later recovered
  with matching hashes and are committed unchanged. A citation map ties every
  specification-cited equation to a committed report.

The earlier implementation milestones below remain useful provenance:

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
  explicit D3 branches (`printed_4_15`, `derived_4_10`), both tilt
  variables, and the IC-rate/epoch/wavenumber interpretations as mandatory
  explicit choices with no defaults; upstream Fig.-3 trajectories reproduced
  through an isolated forensic harness (the D2-corrupted sound speed never
  enters the scientific package) →
  `reports/phase1c_b2_barotropic_validation.md`.
- **Phase 1D-A (done):** equation-level audit of the observable meaning of
  the CGI perturbation variables: exact harmonic mapping
  Δ_d,k = −k_code²·δ_m,k, bare/dressed growth coordinates with the exact
  tracker chain factor, zero-crossing policy, and the blockers separating
  the present variables from σ_R/σ_8/observational fσ8 →
  `reports/phase1d_a_growth_observable_audit.md`.
- **Phase 1D-B (done):** independent typed **growth pipeline**
  (`src/timescape_fsigma8/growth/`): signed relative growth histories,
  exact analytic bare and dressed growth rates via −3Z/(ΘΔ_d) (no
  numerical differentiation), non-logarithmic derivatives, root-refined
  zero crossings with maximal piecewise validity intervals, and an
  optional solver-harmonic δ_m coefficient mapping →
  `reports/phase1d_b_growth_pipeline_validation.md`.
- **Later conditional checkpoints:** anchored density-growth Candidate A,
  H1 regional transfer and spectra, scalar dust-to-wall boost, and optional
  local wall metric-trace reconstruction. These do not supply observational
  power spectra, σ_R, σ8, fσ8, RSD/Kaiser, bias, likelihoods or fitting.

> **Read this before using the growth layer:** `Delta_d` is the CGI
> Laplacian density scalar, **not** the ordinary local density contrast;
> mapped `delta_m` values are solver-harmonic coefficients only. Relative
> growth and logarithmic rates are invariant under the fixed harmonic
> conversion. Growth rates are **piecewise** for trajectories with
> amplitude crossings (the barotropic rate has poles inside the observable
> window). D3 is **RESOLVED_DERIVED_4_10**; the printed branch remains an
> explicit forensic alternative. No observational fσ8, σ8, spectrum, or RSD quantity has been
> implemented. D2 remains excluded from the scientific package.

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
| `src/timescape_fsigma8/growth/` | Phase 1D-B growth layer: mandatory-explicit scenarios, dust-mode histories, exact analytic rates, root-refined crossings/validity intervals, solver-harmonic δ_m mapping; Phase 1D-D anchored density-growth diagnostic (Candidate A, conditional and non-observational) |
| `src/timescape_fsigma8/perturbations/growing_mode.py` | Explicit Timescape regular growing-mode ICs for the clean systems (review F1) |
| `src/timescape_fsigma8/transfer/` | Phase 1E-F/1E-G conditional H1 transmission runtime (matrix contract, continuum-geometric backend and bridge) with the F3 kinematic gates |
| `src/timescape_fsigma8/phase1f_a/` | Phase 1F-A conditional forward realization: regional density/expansion inversion, carrier density, spectra, external boost, dressed map |
| `src/timescape_fsigma8/phase1f_b/` | Phase 1F-B conditional scalar dust-to-wall boost dynamics |
| `src/timescape_fsigma8/phase1f_c/` | Phase 1F-C conditional wall/common-spacetime kinematic geometry |
| `src/timescape_fsigma8/phase1f_d.py` | Phase 1F-D conditional scalar positive-core necessary-bound diagnostic (no solver; a positive margin establishes no existence) |
| `src/timescape_fsigma8/lagrangian_sigma.py` | Phase 1G-B conditional, model-internal, mass-labelled linear σ(M) (explicit growth law, early-spectrum import and radius convention; non-observational) |
| `src/timescape_fsigma8/global_variance.py` | Phase 1G-H experimental, conditional formal tangent statistic of the global contrast (two-phase propagator, explicit void-share closures, constant-share interval, two-phase covariance, orthant integrals with an accuracy contract; non-observational) |
| `scripts/phase1g_h_global_variance_closure_numerics.py`, `scripts/phase1g_h_global_variance_case.py`, `scripts/phase1g_h_configs/` | Phase 1G-H evidence, single-case runner and example configurations |
| `src/timescape_fsigma8/experimental_ltb_cmc/` | Isolated, conditional LTB–CMC experiment outside the phase sequence: CMC-sliced LTB background, tracker-clock comparison, single-age evolution, kappa_star and mixed sensitivities |
| `src/timescape_fsigma8/components.py` | Tensor-component ontology (coordinate/orthonormal representations, 1F-C-R) |
| `src/timescape_fsigma8/scientific_status.py` | Current cross-phase scientific classifications (1F-C-R successor record) |
| `scripts/validate_anchored_density_growth.py` | Phase 1D-D Candidate A validation (regenerable on any clean descendant of the 1D-D commit) |
| `scripts/validate_phase1f_a_h1_closure.py`, `scripts/validate_phase1f_b_dust_wall_boost_dynamics.py` | Phase 1F-A/1F-B validation drivers (deterministic artifacts) |
| `scripts/validate_phase1f_c_r_astra_remediation.py` | 1F-C-R provenance, equation-preservation and JSON checks (ancestry-based; reports post-remediation drift and absent local provenance) |
| `scripts/audit_numerical_tolerances.py` | AST inventory ensuring every numerical comparison states its tolerances |
| `scripts/validate_growing_mode_initial_conditions.py`, `scripts/validate_h1_kinematic_gates.py` | Review F1 and F3 validation drivers |
| `scripts/validate_growth_pipeline.py` | Growth-pipeline validation: frozen-bracket crossing checks, analytic identities, solver/root convergence, tilt equivalence, one-factor studies |
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
| `reports/phase1d_a_growth_observable_audit.md` | Phase 1D-A observable-definition audit (+ machine-readable `phase1d_a_observable_inventory.json`) |
| `reports/phase1d_b_growth_pipeline_validation.md` | Phase 1D-B growth-pipeline implementation and validation report |
| `reports/phase1d_c_*`, `phase1d_d_*`, `phase1d_d_t_*` | Observable-closure audit, Candidate A validation, D3 frame-mapping adjudication |
| `reports/phase1e_*` | Dressed-observable bridge, light-cone velocity, transfer closure, regional matching, realization selection, H1 and continuum H1 realizations (with adversarial audits) |
| `reports/phase1f_*` | 1F-A/1F-B/1F-C conditional runtimes, 1F-C-R remediation, the post-remediation review and its F1/F3/F2–F9 fixes, the 1F-D necessary-bound diagnostic |
| `astra/INDEPENDENT_SCIENTIFIC_AUDIT.md` | The independent audit that 1F-C-R remediates (recovered F4 provenance, pinned SHA-256) |
| `reports/phase1g_*` | σ(M) track: 1G-A…1G-F reports, status and errata successor records, adversarial audits, owner-decision successor records (2026-09-30) and the Windows validation record |
| `reports/experimental_ltb_cmc*.md` | LTB–CMC experiment reports (background, evolution, kappa_star and mixed sensitivities) and the Italian P187–P189 research note |
| `AGENTS.md` | Permanent project rules (scientific-integrity constraints) |
| `pyproject.toml` | Package + minimal dependency declaration |

## Licensing note

The upstream repository contains **no license file**. Its code is treated as
all-rights-reserved reference material: it is cloned locally for audit only,
never committed to this repository, and never redistributed. See
`UPSTREAM.lock` and rule 6 of `AGENTS.md`.

## Reproducing the audit

Windows:

```
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -e ".[exec,test]"
.venv\Scripts\python scripts\execute_upstream_notebook.py
.venv\Scripts\python -m pytest -q
```

Linux/macOS (any CPython >= 3.11; phases are also validated on 3.11 in a
second environment `.venv311`):

```
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[exec,test]"
.venv/bin/python scripts/execute_upstream_notebook.py
.venv/bin/python -m pytest -q
```

The upstream clone goes in `.reference/` at the commit pinned in
`UPSTREAM.lock`. Its notebook is identified by a line-ending-independent
SHA-256 (`notebook_sha256_lf`), so LF and CRLF (`core.autocrlf`) checkouts
verify identically.

The script fails with a nonzero exit code if any notebook cell fails, writes
the executed copy to `artifacts/upstream/ACPT_Timescape.executed.ipynb`, and
records the environment and all captured output in
`artifacts/upstream/execution_log.json`. It never modifies the original
notebook.
