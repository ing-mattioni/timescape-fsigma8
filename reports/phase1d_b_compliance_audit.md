# Phase 1D-B — Compliance and numerical audit (read-only)

Audit date: 2026-07-17.
Auditor process: independent read-only session; no source, test, report,
artifact, or upstream file was modified; the only file created is this
report.  All in-memory recomputations were run from scratch scripts in a
session-local scratch directory outside the repository.

Audited state: branch `phase-1d-b-growth-pipeline`, HEAD
`878a97e83357025c78e2fee7bf458c3b22a207d3` (uncommitted working tree with
the Phase 1D-B files).  Specifications read:
`reports/phase1d_a_growth_observable_audit.md`,
`reports/phase1d_a_observable_inventory.json`, and the Phase 1D-B
implementation prompt (its 20-section text as delivered in the working
session).  Every new or modified Phase 1D-B file was read completely
(all 7 `growth/` modules, all 5 test files, the validation script, the
validation report, and both doc diffs); the 1.4 MB artifact was read by
machine extraction of every study section.

Classification vocabulary used below: COMPLETE / PARTIAL / MISSING /
DEVIATED WITH JUSTIFICATION / CLAIMED BUT NOT EVIDENCED / NOT APPLICABLE.

---

## 1. Repository and preservation audit — COMPLETE

All verified live by direct git commands (not from the completion
message):

1. **Branch/HEAD:** `git rev-parse --abbrev-ref HEAD` →
   `phase-1d-b-growth-pipeline`; `git rev-parse HEAD` →
   `878a97e83357025c78e2fee7bf458c3b22a207d3`. ✓
2. **Frozen tags and ancestry:** `phase-1b-background-v1` → `fe8b00f…`,
   `phase-1c-a-equation-audit-v1` → `5d9aa47…`,
   `phase-1c-b1-clean-systems-v1` → `18b6666…`,
   `phase-1c-b2-barotropic-v1` → `9ec3bcc…`,
   `phase-1d-a-growth-observable-audit-v1` → `878a97e…` (= HEAD); all five
   are ancestors of HEAD (`git merge-base --is-ancestor`). ✓
3. **Upstream commit and cleanliness:** the pinned clone at
   `.reference/Linear-Perturbations-in-averaged-cosmological-models` has
   HEAD `590c6fd5332acb15f5683ebf392a0d7ce54983c5` and an empty
   `git status --short`. ✓
4. **Notebook hash:** `sha256sum ACPT_Timescape.ipynb` →
   `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a`. ✓
5. **Exact diff:** tracked modifications are only `CLAUDE.md` (+22/−3)
   and `README.md` (+30/−6); the full diffs were read and contain only
   phase-status text, the new command entry, layout-table rows, and the
   mandated caveat statements.  No equation, constant, or historical
   report line changed. ✓
6. **No frozen 1B/1C/1D-A scientific file modified:** `git status
   --porcelain -uall` lists no modification besides the two docs; every
   other path is untracked-new. ✓
7. **No generated B1/B2 artifact modified:** all
   `artifacts/independent/phase1c_*` files carry their pre-1D-B
   timestamps (Jul 16 12:22 for B1, Jul 17 09:59 for B2); the only new
   artifact is `phase1d_b_growth_validation.json` (Jul 17 15:49). ✓
8. **Nothing staged:** `git diff --cached --name-only` is empty. ✓
9. **No commit, tag, or push:** `git log 878a97e..HEAD` is empty; `git
   tag` lists only the five frozen tags; `git stash list` is empty. ✓
10. **`git diff --check`:** clean, exit 0. ✓
11. **`git status --short` (exact):**

```text
 M CLAUDE.md
 M README.md
?? reports/phase1d_b_growth_pipeline_validation.md
?? scripts/validate_growth_pipeline.py
?? src/timescape_fsigma8/growth/
?? tests/growth_test_utils.py
?? tests/test_growth_convergence_purity.py
?? tests/test_growth_crossings.py
?? tests/test_growth_histories_rates.py
?? tests/test_growth_scenarios.py
```

**"14 new files" reconciliation:** the 10-line status above collapses
`src/timescape_fsigma8/growth/` into one directory entry.
`git status --porcelain -uall` expands it to exactly 7 module files, so
the untracked-new set is 7 (growth) + 5 (tests) + 1 (script) + 1 (report)
= **14 files**, exactly matching the completion report's Sec. 24 list.
The generated artifact appears in neither listing because
`artifacts/independent/` is git-ignored (`git check-ignore -v` confirms
`.gitignore:10`).  The count difference is fully explained by directory
collapsing; there is no hidden or unlisted file.

## 2. Scope audit — COMPLETE

**Positive scope:** reading all seven modules end-to-end, the package
contains exactly: scenario/reference/numerics records with validation
(`scenarios.py`), frozen-solver histories + dust-mode extraction
(`histories.py`), analytic rates/derivatives (`rates.py`), crossing
scan/dense refinement/validity intervals (`crossings.py`), the pure
−1/k_code² mapping (`mapping.py`), and orchestration/serialization
(`pipeline.py`).  All 53 `__all__` exports were inspected; each belongs
to one of the permitted capabilities.

**Negative scope:** searched source, exports, tests, scripts, the
artifact, and documentation for spectra, transfer functions, primordial
spectra, σ_R, σ_8, fσ8/"fσ8-shaped", spectral/window-weighted growth,
RSD/Kaiser, bias, Alcock–Paczynski, datasets/covariances/likelihoods/
fitting, and D2 tokens.  Findings:

- The only textual hits in `growth/*.py` outside import lines (the
  package name itself contains "fsigma8") are the *exclusion statements*
  in `__init__.py` (lines 19–23) — statements that these quantities do
  not exist, as mandated.
- Behavioural check, not just names: no module imports `matplotlib`, no
  `interp1d`/`np.interp`/`np.gradient`/spline/`polyfit` appears anywhere
  in the package (grep: zero hits), no windowing kernel, no integral over
  k, no dataset or covariance structure exists.  The only generic
  numerical machinery is `solve_ivp` (re-integration) and `brentq`
  (root refinement / redshift inversion), both used solely for the
  permitted purposes.
- The machine artifact contains **no** forbidden field: a recursive scan
  of all JSON keys against
  {sigma_8, sigma8, sigma_r, fsigma, power_spectrum, transfer,
  primordial, kaiser, rsd, bias, alcock, likelihood, covariance,
  fitting, window} returned zero hits.
- D2: `FORBIDDEN_D2_TOKENS` (including the corrupted-coefficient literal
  `54.0 * f**5` and `_phase1c_b2_forensic`) are absent from the package
  (tested in `test_growth_package_contains_no_d2_or_forensic_path`, and
  re-grepped independently); the import-statement scan
  (`test_growth_package_does_not_import_forensic_or_scripts`) confirms no
  forensic/scripts import.
- V6's three barotropic endpoints are labelled in both artifact and
  report as "deterministic per-mode dependence … no physical
  power-spectrum scale dependence is inferred" — no spectrum
  interpretation is attached (Sec. 16 below).

## 3. Scientific formula audit — COMPLETE

Verified directly in `rates.py` (all lines read):

- `f_bare = -3.0 * z_expansion / (theta * delta_d)`
  ([rates.py:104](../src/timescape_fsigma8/growth/rates.py)) — exactly
  −3Z/(ΘΔ_d).
- `dressed_chain_factor = (2+f_v)²/(4+f_v+4f_v²)` (rates.py:50);
  `f_dressed = f_bare × chain factor` (rates.py:123–132).
- `dDelta_d_dln_aD = −3Z/Θ` (rates.py:145); dressed counterpart = that ×
  chain factor (rates.py:154–156).
- `map_delta_m = delta_d / (−k_code²)` (mapping.py:110) and the same
  −1/k_code² factor on the non-logarithmic derivatives (mapping.py:127),
  which with −3Z/Θ yields +3Z/(Θk_code²) as documented.
- Z is never re-derived by differentiation: it is the state variable.
  Mészáros extraction `Z = −y[1]` (histories.py:119, and in the dense
  wrapper crossings.py:76 `sign = −1.0 if MESZAROS`); comoving and
  barotropic pass `y[1]` through unchanged (histories.py:123, 127).
  Verified against the frozen state conventions in
  `perturbations/systems.py` (Mészáros y=(Δ, Δ̇)) and the barotropic
  matrix `matrix[0,1] = −1.0` ([GM] 4.14 ⇒ Δ̇ = −Z ⇒ y[1] = Z).
- **No finite difference / gradient / spline / interpolation / fit** in
  any primary path (grep: zero hits in the package).  The single
  `np.gradient` in the codebase's new files is in
  `test_growth_histories_rates.py::test_f_bare_against_independent_finite_difference`,
  explicitly labelled "Validation-only cross-check, not a rate
  implementation".
- **Citations:** every anchor cited in the docstrings was located in the
  frozen 1D-A audit: (D1b-code) at line 187, (D1c) at 210,
  H_dressed [W09 (28)/(B8)] at 380, chain D3 + sympy S3b–S3f at 409,
  chain-factor value 1.08416 at 433, chain D4 + sympy S4 with
  f_bare = −3Z/(ΘΔ_d) at 456–462, "sampled-grid brackets" at 480, the
  `map_to_delta_m_via_minus_k_code2` label at 833.
- **Numerical confirmation** (artifact V2, machine-checked): identity
  |f·D − dD/dln a| ≤ 3.9e−16 relative; chain-factor identity ≤ 2.1e−16;
  G_Δ = G_m to 1.9e−16; mapped-derivative factor deviation exactly 0.0.
  Independently recomputed in this audit: chain factor at t0 = 1.084156
  from f_v(t0) alone, matching f_dressed/f_bare = 0.158947/0.146609.

## 4. Public API and no-default audit — COMPLETE (package); test/script helpers noted

Every public constructor and dataclass in the package was inspected:
`GrowthScenario` (11 fields), `GrowthReference` (4), `GrowthNumericsConfig`
(6), `DenseSolveConfig` (5), `RootRefineConfig` (4), `HarmonicMetadata`
(6), `GrowthProvenance` (3), plus all functions.  Findings:

- **No dataclass default or default factory anywhere** in the package
  (verified by reading and by
  `test_growth_configs_have_no_field_defaults` +
  `test_scenario_has_no_scientific_field_defaults`, which use dataclass
  introspection).  Every pipeline entry point (`run_growth_pipeline`,
  `compute_history`, `resolve_reference`, `evaluate_rates`,
  `build_dense_solution`, `refine_root`, `map_delta_m`) takes
  keyword-only mandatory arguments; `provenance` may be `None` but that
  is a provenance field, not a scientific choice.
- **No singleton or module-level "standard" scenario** exists in the
  package (grep for module-level `GrowthScenario(` in `src/`: none).
- **No inference/fallback:** enum fields reject string lookalikes
  (`_require_enum`, tested); `not_applicable` must be passed explicitly;
  omitted `supplied_mode_k` with the mapping selected raises; `None`
  never triggers a substituted value.
- **Exported constants:** `PAPER_REFERENCE_TIME_UNIT` (0.7303/9.778) and
  `LCDM_REFERENCE_H` (0.674) are resolutions of the explicit preset
  choice, documented in place; 0.674 was verified equal to the frozen
  `PLANCK_2018_QPLUS_RECIPE.h`, so neither introduces a new free choice.
- **Exact labels verified** (source + `test_every_scenario_enum_value_is_
  exactly_the_required_label`): meszaros/comoving/barotropic;
  paper_reference/notebook_reference; not_applicable/printed_4_15/
  derived_4_10; not_applicable/unrescaled_V/rescaled_Vtilde; the frozen
  upstream_unconverted/lcdm_to_timescape_converted and
  upstream_0p218_gyr/dressed_z20 enums reused; not_applicable/
  upstream_timescape_k/paper_lcdm_hubble_k; bare_aD/dressed_redshift;
  keep_Delta_d/map_to_delta_m_via_minus_k_code2.
- **Applicability rules** (scenarios.py:235–283, all tested): barotropic
  rejects `not_applicable` D3/tilt/k-convention and missing mode; clean
  systems reject any real D3/tilt/k-convention, reject mode metadata
  without the mapping, and reject the mapping without explicit k.
- **Ranking language:** grep for canonical/preferred/recommended/intended
  over the package returns only the *negation* sentences; "corrected"
  appears only inside "not silently corrected" and the negation list
  (and, in reports, only for the adjudicated D2 sound-speed finding,
  which is a documented upstream algebra error, not an unresolved
  choice); "physical" appears only in the negation list and the Mészáros
  disclaimer; "default" appears only in "no default" statements.
- **Noted (not a violation):** the *test* builders
  (`tests/growth_test_utils.py::clean_scenario/barotropic_scenario`) and
  the *validation-script* helpers use Python keyword defaults for
  brevity.  These are not exported by the package, are documented as
  "test/validation configurations … not package defaults and carry no
  scientific preference", and every produced scenario still passes
  through the full mandatory validation.  See C-list.

## 5. Solver architecture audit — COMPLETE (one orchestration duplication noted)

1. **Frozen RHS reused, not copied:** `crossings.build_dense_solution`
   imports `meszaros_rhs`, `comoving_rhs` from
   `perturbations.systems` and `barotropic_rhs` from `perturbations`
   (crossings.py:32–33) and wraps them with `functools.partial`; no RHS
   body, matrix entry, or coefficient is redefined anywhere in `growth/`
   (verified by reading every module; the only equations present are the
   audited rate/mapping formulas of Sec. 3).
2. **No scientific matrix duplicated.** ✓ (same reading.)
3. **ICs and scenario resolution reuse frozen APIs:**
   `resolve_epoch_and_ics` calls the frozen `EpochScenario(…,
   root=PHASE1C_EPOCH_ROOT).resolve` and
   `InitialConditionScenario(recipe=PLANCK_2018_QPLUS_RECIPE, …).resolve`;
   barotropic runs construct the frozen `BarotropicScenario` and call
   the frozen `solve_barotropic` unchanged.
4. **All solver options explicit:** both the sampled solve (frozen
   `SolverConfig`) and the dense solve (`DenseSolveConfig`) carry
   method/rtol/atol/max_step/first_step; `build_dense_solution` passes
   every `solve_ivp` argument explicitly, including `t_eval=None`,
   `events=None`, `vectorized=False`, `dense_output=True`
   (crossings.py:125–138); the frozen `_solve`/`solve_barotropic` do the
   same on their side.  **No silent SciPy default** is relied on in any
   new call site.
5. ✓ (same as 4.)
6. **Drift analysis (the key re-integration risk):** the dense solve uses
   the identical rhs *function objects*, the identical
   `history.numerics.G`, the identical resolved background params, the
   identical interval `[history.t[0], history.t[-1]]`, and for
   barotropic the identical y0 construction
   `[delta_d, expansion_gradient, delta_eff, 0.0]` — verified equal,
   line for line, to `solve_barotropic`'s own
   `y0 = [initial.delta_d, initial.expansion_gradient,
   initial.delta_eff, 0.0]`.  Wavenumber handling cannot diverge: the
   frozen `barotropic_rhs` takes the *raw* supplied k plus the explicit
   convention and resolves `matrix_k` internally
   (barotropic.py:207–232 → `resolve_wavenumber`), and the dense wrapper
   passes exactly `k=b2.k` with the same convention — the same code path
   the production solver uses.  Time units and state ordering are the
   frozen ones throughout.  `refine_root` additionally *raises* if the
   dense solution does not change sign inside a sampled bracket
   (crossings.py:293–298), so a dense/sampled disagreement cannot pass
   silently.
7. **Existing solver behaviour unchanged:** no frozen module was edited
   (Sec. 1), and all 268 pre-existing tests pass unchanged inside the
   337 (Sec. 17).
8. **Immutability:** every output array is frozen with
   `flags.writeable = False` (`_frozen`/`_frozen_array` in rates.py,
   histories.py, pipeline.py; masks too); all result records are frozen
   dataclasses; `test_output_arrays_are_immutable` confirms writes raise.
9. **Duplicated orchestration (classified separately from science):**
   the barotropic y0 assembly line in `build_dense_solution`
   (crossings.py:119–122) repeats the assembly inside the frozen
   `solve_barotropic` rather than calling a shared helper (none is
   exported by the frozen layer).  This is orchestration duplication
   only — no coefficient or equation — and it is pinned by the
   sign-consistency raise and the V3 agreement.  C-list.

## 6. Reference-epoch audit — COMPLETE

- Both coordinates implemented (`bare_time_solver_units`,
  `dressed_redshift`); the dressed→bare conversion is an explicitly
  configured bracketed `brentq` on the validated Phase 1B `bg.redshift`
  (pipeline.py:139–149) with the caller's `EpochRootConfig` — no root
  option defaulted.
- Continuous evaluation method documented and real: the reference
  amplitude is read from the dense re-integrated solution
  (pipeline.py:150), not from nearest-sample lookup.
- Range checking: bare-time outside `[t_lo, t_hi]` and dressed-z outside
  the integrated redshift range both raise (tested:
  `test_reference_outside_integrated_solution_is_rejected`).
- Zero/near-zero rejection: three explicit criteria — exact zero;
  linearised (Newton) time distance `|Δ_d|/|Z|` ≤
  `amplitude_floor_rel × span` (exact relation since Z = −Δ̇_d); or any
  refined Δ_d root within that same time tolerance (pipeline.py:150–173).
  The tolerance's dimensional meaning is therefore an explicit *time*
  tolerance, a fixed fraction of the integrated span — scale-free across
  the ~10¹⁴ amplitude range (an amplitude-based floor would not be).
- **Adjacency check performed live in this audit** (derived_4_10|2π,
  root t\*=0.785161573556246, span 1.13529, tolerance 1.135e−10): a
  bare-time reference at t\*±0.5·tol is **rejected** with the
  "numerically indistinguishable from a zero crossing" error; at
  t\*±5·tol it is **accepted**, with amplitude ∓4.25e−11 and the correct
  validity-interval membership on each side ([False, True] above the
  root, [True, False] below).  Behaviour on both sides of the crossing
  is exactly as specified.
- Metadata: `ResolvedGrowthReference` records t (solver units), Gyr,
  dressed z, a_D, a_obs, the dense amplitude, and amplitude/max
  (tested: `test_reference_resolution_records_all_coordinates`).
- No default reference of any kind exists; `GrowthReference` has no
  field defaults (tested), and `run_growth_pipeline` requires it.
- **Docstring discrepancy (B-list):** `GrowthReference.amplitude_floor_rel`'s
  docstring in scenarios.py (lines 342–345) still describes the floor as
  "relative to the trajectory's maximum |Delta_d|", which is the
  *superseded* policy; the implemented and report-documented policy is
  the span-based time tolerance above.  Implementation and validation
  report agree with each other; only this docstring is stale.

## 7. Root detection and refinement audit — COMPLETE

Mechanics verified in source and by tests: strict scan `y[i]·y[i+1] < 0`
(never involves an exact zero); near-zero samples flagged by the
neighbour-local mask and never promoted to roots
(`test_rounding_zero_sample_is_flagged_not_promoted_to_root`); endpoint
near-zeros reported separately as `EndpointRoot`s
(`test_endpoint_zero_reported_as_endpoint_root_not_strict_change`);
original sample brackets preserved verbatim in `SignChangeBracket` and on
each `RefinedRoot`; brentq is bracket-preserving with explicit
xtol=1e−13, rtol=8.9e−16, maxiter=100 and `full_output` status capture;
in-bracket containment re-verified after the solve; residual evaluated at
the root and gated; conversions to Gyr, dressed z, a_D, a_obs on every
root; complete scenario identifier and both configs embedded.

**All ten baseline refined roots** (artifact V1; scenario: notebook
preset, upstream conventions, `unrescaled_V`, tight DOP853, n=1000;
"scale" = max(|y_left|, |y_right|) of the *sampled bracket*, i.e. a local
bracket-sample magnitude, never a global amplitude):

| # | branch | mode | comp | t_root (code) | Gyr | z_dressed | a_D | a_obs | frozen 1D-A bracket | dist left / right | abs residual | resid/scale | scale | brentq |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | printed_4_15 | 5π | Δ_d | 0.228538312270434 | 3.051547 | 2.409726 | 0.345684 | 0.293279 | [0.2277011750928674, 0.2288375975917282] | 8.37e−4 / 2.99e−4 | 4.29e−16 | 1.46e−12 | 2.94e−4 | conv, 5 it |
| 2 | printed_4_15 | 5π | Z | 0.140771268152425 | 1.879641 | 3.732965 | 0.238238 | 0.211284 | [0.1401966426805888, 0.1413330651794496] | 5.75e−4 / 5.62e−4 | 4.19e−15 | 4.30e−12 | 9.74e−4 | conv, 5 it |
| 3 | printed_4_15 | 10π | Δ_d | 0.0781747853840506 | 1.043825 | 5.984064 | 0.154625 | 0.143183 | [0.0776934052432469, 0.0788298277421077] | 4.81e−4 / 6.55e−4 | 7.20e−17 | 9.85e−14 | 7.31e−4 | conv, 6 it |
| 4 | printed_4_15 | 10π | Z | 0.0573302526295315 | 0.765499 | 7.562793 | 0.123933 | 0.116784 | [0.0572378002637532, 0.0583742227626140] | 9.25e−5 / 1.04e−3 | 4.16e−17 | 2.93e−15 | 1.42e−2 | conv, 6 it |
| 5 | derived_4_10 | 2π | Δ_d | 0.785161573556246 | 10.483832 | 0.369650 | 0.969746 | 0.730114 | [0.7845481995346406, 0.7856846220335013] | 6.13e−4 / 5.23e−4 | 6.51e−19 | 1.42e−14 | 4.59e−5 | conv, 5 it |
| 6 | derived_4_10 | 2π | Z | 0.339400981302911 | 4.531835 | 1.583578 | 0.474598 | 0.387060 | [0.3390705799812221, 0.3402070024800828] | 3.30e−4 / 8.06e−4 | 3.90e−18 | 2.55e−14 | 1.53e−4 | conv, 5 it |
| 7 | derived_4_10 | 5π | Δ_d | 0.150938581970392 | 2.015400 | 3.517382 | 0.251099 | 0.221367 | [0.1504244451703357, 0.1515608676691964] | 5.14e−4 / 6.22e−4 | 8.67e−19 | 2.78e−15 | 3.12e−4 | conv, 6 it |
| 8 | derived_4_10 | 5π | Z | 0.0977301111934385 | 1.304937 | 5.028908 | 0.181801 | 0.165868 | [0.0970125877238799, 0.0981490102227406] | 7.18e−4 / 4.19e−4 | 7.36e−14 | 2.97e−11 | 2.48e−3 | conv, 5 it |
| 9 | derived_4_10 | 10π | Δ_d | 0.0677146081323332 | 0.904156 | 6.675729 | 0.139496 | 0.130281 | [0.0674656027535001, 0.0686020252523608] | 2.49e−4 / 8.87e−4 | 7.89e−17 | 6.79e−14 | 1.16e−3 | conv, 6 it |
| 10 | derived_4_10 | 10π | Z | 0.0505504817817814 | 0.674973 | 8.300787 | 0.113406 | 0.107518 | [0.0504192652705886, 0.0515556877694494] | 1.31e−4 / 1.01e−3 | 1.18e−16 | 6.47e−15 | 1.82e−2 | conv, 6 it |

Every distance-from-endpoint is ≥ 9.2e−5 code time, i.e. ≥ 10⁸ times the
1e−13 uncertainty diagnostic — every root is strictly interior and none
is a bracket sample.  `printed_4_15|2π` has zero Δ_d and zero Z roots as
frozen.  (At n=1000 the sampled bracket numerically coincides with the
frozen 1D-A bracket because 1D-A sampled the same 1000-point grid; the
600- and 2000-point V4 runs produce *different* brackets and the same
refined roots, confirming derivation rather than copying.)

**No root silently discarded:** the scan code appends every strict sign
change with no filtering; the tests assert exact expected counts; and the
independent event-detection sweep of Sec. 8 — which monitors the
*continuous* trajectory, not sampled pairs — found exactly one Δ_d and
one Z event per crossing scenario and zero for `printed_4_15|2π`,
matching the production counts everywhere.

## 8. Independent numerical spot checks — COMPLETE (all four confirmed; extended to all ten)

Method: a scratch script (outside the repo) resolved the epoch/ICs
through the frozen perturbation layer only and integrated the frozen
`barotropic_rhs` with `solve_ivp` **event detection**
(`events=(y[0], y[1])`), under **Radau** (rtol 1e−10/atol 1e−12) and
**LSODA** (1e−11/1e−13).  This path shares only the frozen equations with
production; it does **not** use the growth package, the production dense
DOP853 interpolant, or the production brentq-on-dense refinement — the
event roots come from each integrator's own local interpolant.  It is
therefore independent in both the integrator and the root machinery.

| root | production (n=1000) | Radau event | LSODA event | worst \|diff\| |
|---|---|---|---|---|
| printed_4_15, 5π, Z | 0.14077126815242547 | 0.14077126815211227 | 0.14077126815028868 | 2.1e−12 |
| printed_4_15, 10π, Δ_d | 0.07817478538405064 | 0.07817478538198598 | 0.07817478537902381 | 5.0e−12 |
| derived_4_10, 2π, Δ_d | 0.78516157355624605 | 0.78516157355667415 | 0.78516157354661942 | 9.6e−12 |
| derived_4_10, 10π, Z | 0.05055048178178138 | 0.05055048177998812 | 0.05055048177743673 | 4.3e−12 |

The sweep was extended to **all ten** baseline roots plus the two
`printed_4_15|2π` components: worst |event − production| over every
root and both methods is **9.6e−12 code time**, fully consistent with the
integrator tolerances used, and the event counts match production
everywhere (zero events for `printed_4_15|2π`).  This independently
confirms the production roots and supplies the cross-method evidence that
V4 itself does not (Sec. 9).

## 9. Root-convergence claim audit — PARTIAL (grid convergence COMPLETE; cross-method claim not evidenced by V4 itself)

Verified from the script and artifact:

1–3. Methods: tight DOP853 (1e−11/1e−13) and tight Radau (1e−10/1e−12),
each fully specified; grids n = 600, 1000, 2000. ✓
4–6. Each run re-integrates its own *sampled* trajectory with its
solver — but the **root refinement always consumes the same dense
continuous representation**: `DenseSolveConfig` is the fixed DOP853
rtol=1e−11/atol=1e−13 configuration for every V4 run (script line 89),
and the dense solve depends only on scenario/ICs/interval, not on the
sampled method or grid.  The artifact proves the consequence: for every
root, the DOP853 and Radau rows at equal n are **bit-identical**
(e.g. printed|5π Δ_d: t = 0.22853831227043317 for both at n=600, both
residuals 6.94e−18).  The sampled method changes only which sample pair
brackets the root; at equal n the tight methods bracket identically, so
brentq receives identical inputs.
7. Per-root spreads (all six combinations): Δ_d — 1.19e−15 (p|5π),
4.19e−15 (p|10π), 0.0 (d|2π), 2.03e−15 (d|5π), 6.66e−16 (d|10π);
Z — 2.03e−14 (p|5π), 1.56e−14 (p|10π), 5.55e−16 (d|2π), 2.16e−14
(d|5π), 2.08e−17 (d|10π).  Maximum 2.16e−14 ≈ the claimed 2.2e−14. ✓
8. The 1e−8 gate sits in the module-level `GATES` dict declared before
any study executes, with a recorded a-priori justification, and is
stored in the artifact under `gates_declared_before_study`. ✓
9. Whether the gate was altered after seeing results cannot be proven
from history (nothing is committed), but the measured spreads are six
orders below the gate, which leaves no incentive for tuning; see E-list.
10. The spreads (≤ 2.2e−14) are *below* the brentq xtol floor (1e−13):
they measure the reproducibility of brentq on one shared interpolant
under different bracket endpoints — a meaningful robustness check of the
refinement, but **not** a cross-method agreement measurement.

**Classification:** grid-density convergence and bracket-robustness —
COMPLETE.  The *cross-method* component of the claim ("two solver
methods … spread 2.2e−14") — **PARTIAL / CLAIMED BUT NOT EVIDENCED by
V4 alone**, because both method rows share the dense DOP853
representation.  Genuine cross-method root evidence exists elsewhere:
V3 shows the sampled trajectories of DOP853/RK45/Radau agree to
normalized-L∞ ≤ 3.1e−9, and this audit's Radau/LSODA event detection
(Sec. 8) reproduces every root to ≤ 9.6e−12 with entirely different
machinery.  The roots are right; the V4 *presentation* (report Sec. 18
and the artifact taxonomy line "V4 spreads across solver methods at
fixed grid") overstates what V4 measured and should be reworded (B-list).

## 10. Piecewise validity audit — COMPLETE

- Intervals are built from Δ_d roots only (`build_validity_intervals`
  filters `component == DUST_COMPONENT`); Z roots never appear as
  boundaries.  Tested: `test_z_roots_are_rate_zeros_and_do_not_split_
  intervals` (derived|2π: 1 Z root strictly inside the first of exactly
  2 intervals).
- Full interval listing for every crossing scenario (artifact V1;
  endpoints in solver units; semantics: closed `[` at integration
  endpoints, open `)` at the refined root):
  - printed|5π: [0.0163266, 0.2285383) sign +1, samples [0,186], contains
    reference; (0.2285383, 1.1516127] sign −1, samples [187,999], not.
  - printed|10π: [0.0163266, 0.0781748) +1, [0,54], ref;
    (0.0781748, 1.1516127] −1, [55,999], not.
  - derived|2π: [0.0163266, 0.7851616) +1, [0,676], ref;
    (0.7851616, 1.1516127] −1, [677,999], not.
  - derived|5π: [0.0163266, 0.1509386) +1, [0,118], ref;
    (0.1509386, 1.1516127] −1, [119,999], not.
  - derived|10π: [0.0163266, 0.0677146) +1, [0,45], ref;
    (0.0677146, 1.1516127] −1, [46,999], not.
  - printed|2π and both clean systems: one interval
    [0.0163266, 1.1516127], both ends closed, sign +1, samples [0,999],
    contains the reference.
  The exact root time belongs to no interval (strict `<`/`>` in the
  sample masks; adjacent index ranges partition the grid:
  e.g. [0,676] ∪ [677,999]).
- Logarithmic rates at Δ_d roots: NaN under the explicit mask, never
  ±inf (`test_rates_masked_nan_at_amplitude_roots_never_infinite`
  asserts no inf anywhere and NaN exactly on the mask); non-logarithmic
  derivatives verified finite at every sample including masked ones.
- Z roots ⇒ rate zeros: f_bare passes through zero near the Z root
  (tested, window min < 2e−2), no interval split.
- Serialization: `rate_segments()` emits one segment per interval;
  `test_serialization_never_joins_rate_arrays_across_a_pole` verifies
  max(t_first) < t_root < min(t_second) and that no joined top-level
  `f_bare` array exists in the JSON payload.
- No convenience function plots, interpolates, or smooths across the
  pole: the package has no plotting/interpolation import at all (Sec. 2
  grep), and the only interpolant (dense OdeSolution) is used solely for
  root refinement and reference evaluation, never to fill the pole.

## 11. Validation-metric audit — COMPLETE (denominator caveat documented below)

`error_metrics` (script lines 224–250) defines exactly:
max_abs_error = max|ref − other| (non-finite diffs excluded);
normalized_linf = max_abs / max(global max|ref| per array, 1e−300);
rms_error = √mean(diff²); denominator_policy string recorded in every
entry; worst_time = argmax location; worst_is_near_crossing = within
2 grid steps of a Δ_d root.  Near-zero exclusion: relative error is
never evaluated pointwise at all (single global scale), so no division
at a true zero occurs; for the V2 identities the near-zero mask
additionally excludes crossing samples before the max is taken.

**"residual/scale ≤ 3e−11":** for both Δ_d and Z roots, `scale` is
`max(|y_left|, |y_right|)` over the two *sampled bracket* samples of that
component (crossings.py:316) — a local, crossing-adjacent magnitude, not
a global amplitude.  Because the trajectory is essentially linear inside
one grid cell, this scale is of order (grid step)×(slope at the root),
so residual/scale ≈ the root's *time* error over the grid step — a
conservative, locally meaningful normalisation.  It **cannot** be
inflated by the 10¹⁴ endpoint amplitudes: measured scales in the table
of Sec. 7 are 4.6e−5 … 1.8e−2, all O(bracket samples).  Absolute
residuals are reported per root in Sec. 7 (max 7.36e−14, for
derived|5π Z — exactly the root behind the quoted 3.0e−11 ratio).
- **Caveat (documented, not a defect):** the *V3* normalized-L∞
  denominator is the global max|reference| per array, which for
  crossing barotropic runs is dominated by the enormous late-time
  amplitude; early-epoch errors on O(1) values are therefore invisible
  in the normalized number.  The policy is stated verbatim in the
  artifact and report, matches the frozen Phase 1C-B2 metric, and the
  max-abs and RMS values are stored alongside, so the information is
  not lost (see Sec. 12 for the absolute numbers).  Worst-discrepancy
  locations and near-crossing flags are present in every entry (all
  worst points sit at the integration endpoint or early epoch, none
  near a crossing).

## 12. Large-amplitude and conditioning audit — COMPLETE

- **Exact identity of the reported endpoints:** the "+4.73 → −5.2e14"
  range is the **endpoint signed relative growth**
  `G_end = Δ_d(t0)/Δ_d(t_ref)` (z_ref = 10) of the `printed_4_15`
  branch across modes: +4.732561 (2π), −26205.85 (5π),
  −5.17167e14 (10π) — artifact V6.  The corresponding raw state
  endpoints (artifact V1) are Δ_d(t0) = +0.028832 / −159.599 /
  −3.13942e12 with Z(t0) = −0.003349 / +809.449 / +3.83638e13; the
  derived_4_10|10π run reaches Δ_d(t0) = −2.72159e14
  (G_end = −4.50069e16).  All post-crossing endpoints follow one Δ_d
  sign change (root table, Sec. 7); the 2π printed run has no crossing
  and stays positive.
- **Solver agreement in absolute terms** (artifact V3,
  derived_4_10|10π): vs the independent DOP853 2e−13/2e−15 reference,
  max-abs on Δ_d is 9.11e4 (tight DOP853), 8.54e5 (tight RK45),
  7.05e3 (tight Radau) — i.e. agreement to ~9–11 significant digits on
  a 2.7e14 endpoint (normalized 2.6e−11 … 3.1e−9).  A small relative
  error on an enormous value is *not* presented alone: these absolute
  errors are in the artifact and now quoted here.
- **Floating-point health:** re-run in this audit with warnings
  captured: zero warnings of any category (no overflow, underflow,
  invalid, or stiffness message), `solver_message` = "The solver
  successfully reached the end of the integration interval", every
  sample finite.  2.7e14 is ~10²⁹⁴ below the float64 overflow
  threshold; loss of significance is confined to the crossing
  neighbourhood, which is exactly what the near-zero mask and the pole
  policy handle.
- **Convergence at that amplitude:** demonstrated by three tight
  methods against the independent reference (above) plus grid halving/
  doubling in V4 leaving the root (the sensitive quantity) unchanged to
  ≤ 2.2e−14.
- **Mathematical vs physical:** the report separates them explicitly —
  Sec. 20 "No physical power-spectrum scale dependence is inferred from
  this deterministic three-mode normalisation", Sec. 23 limitations,
  and the linear-theory caveat inherited from 1D-A (these amplitudes
  are far outside any linear-validity regime; they are properties of
  the linear ODE system, reported as such).  Flagged for human review
  (F-list) since the paper's own Fig. 3 shows the same qualitative
  blow-up.

## 13. One-factor scenario-delta audit — COMPLETE (one labelling improvement, B-list)

For every factor: observable = endpoint signed relative growth
`G_end = Δ_d(t0)/Δ_d(t_ref)`, evaluated at t0 (the integration
endpoint) with the z=10 dressed reference; numerator = G_end(variant) −
G_end(baseline); denominator = |G_end(baseline)| = 4.732561016455046;
convention = signed; formula = (end − base)/|base|, re-verified
arithmetically in this audit from the raw artifact endpoints:

| factor | G_end | recomputed delta | report | sign flip? |
|---|---|---|---|---|
| preset → paper_reference | +4.730549 | −0.0425 % | −0.042 % | no |
| rate → lcdm_to_timescape_converted | +4.699341 | −0.702 % | −0.70 % | no |
| epoch → dressed_z20 | +4.666239 | −1.401 % | −1.40 % | no |
| growth_coordinate → dressed_redshift | +4.732561 | 0 (exact) | 0 | no (rate ×1.084156) |
| d3_branch → derived_4_10 | −6.161738 | −230.2 % | −230.2 % | **yes** (1 root) |
| tilt → rescaled_Vtilde | +4.732561 | −3.47e−14 % | −3e−14 % | no |
| kconv → paper_lcdm_hubble_k | +3.197590 | −32.43 % | −32.4 % | no (G); the *rate* flips: +0.1466 → −0.9199 |
| mapping → map_to_delta_m | +4.732561 | 0 (exact) | 0 | no |

Baseline = the named `validation_baseline` (printed_4_15|2π, notebook,
upstream conventions), recorded in the artifact with the mandatory note
"not a public API default and not a scientific preference".  All other
fields held fixed (verified: each variant scenario differs in exactly
the one field; `changed_to` recorded per factor).  Neither endpoint is
near zero (|G| ≥ 3.2 in every row).

- The D3 delta **crosses a sign reversal** (baseline +4.73, variant
  −6.16; the variant trajectory has one Δ_d root, and its root count is
  stored in the artifact row).  The artifact and report give both signed
  endpoint values, so the reversal is visible, and the taxonomy
  explicitly forbids reading any of this as a confidence interval — but
  neither artifact nor report *states in words* that the −230 % figure
  spans a sign change and is therefore a signed trajectory difference,
  not an uncertainty magnitude.  B-list wording item.  The same note
  applies to the k-convention row's endpoint *rate* (+0.147 → −0.920),
  where the variant sits past its Z crossing.
- Convention spreads are never called confidence intervals, statistical
  errors, or probabilities anywhere (grep over report + artifact:
  the only occurrences are the negations "never a confidence
  interval"). ✓

## 14. Density-mapping audit — COMPLETE

- Formula `delta_m = −Delta_d/k_code²` and the −1/k_code² derivative
  factor: verified in source (Sec. 3) and numerically exact in V2
  (0.0 deviation on the factor).
- Negative-Laplacian sign: `HarmonicSignConvention` has a single member;
  the mapping divides by −k², preserving the (D1b-code) sign; a
  hypothetical other sign is rejected in `__post_init__`.
- k_code > 0, finite, explicit: enforced in both `GrowthScenario` and
  `HarmonicMetadata` (`test_zero_k_code_is_rejected_for_mapped_output`,
  `test_nonfinite_or_zero_mode_k_is_rejected`).
- Clean-system metadata changes only absolute coefficients: V6
  bit-identical relative growth and rates for k_code 7 vs 13 with the
  absolute mapped coefficient differing (also
  `test_clean_relative_growth_invariant_under_harmonic_metadata`).
- Supplied label vs resolved k_code remain distinct: the scenario keeps
  `supplied_mode_k`, the history separately records `resolved_k_code` =
  frozen `ResolvedWavenumber.matrix_k` (equal only under
  `upstream_timescape_k`; under `paper_lcdm_hubble_k` matrix_k =
  k·a_D0·h_lcdm/h_ts ≈ 1.2596·k, computed by the frozen
  `resolve_wavenumber`, and the V7 k-convention row demonstrates the
  distinct dynamics).
- No `k_com_obs` exists anywhere (grep: only the *statements* that it is
  not invented); `k_com_D`/`k_phys0_D` appear as metadata fields only,
  with the (D1c) values k_code and k_code/a_D0.
- No power-spectrum interpretation attached (Sec. 2, Sec. 16).
- **Numerical equality of G_Δ and G_m and of their rates on both sides
  of a crossing — recomputed live in this audit** for derived|2π,
  printed|10π, derived|5π: |G_Δ − G_m| ≤ 1.9e−16 relative and
  |f(δ_m) − f_bare| ≤ 3.6e−16 relative, separately on the left
  (n = 677/55/119 samples) and right (n = 323/945/881) of each pole,
  excluding only masked samples.

## 15. Tilt equivalence audit — COMPLETE (scope of comparison stated)

Claimed vs artifact: history normalized-L∞ 3.9306e−11 (claim 3.9e−11 ✓);
root time diffs 1.5503e−12 (Δ_d) and 6.481e−14 (Z), both ≤ the claimed
1.6e−12 ✓; worst f_bare relative difference 4.581e−9 (report: 4.6e−9 ✓).
Components compared: the dust quantities Δ_d (normalisation: global
max|Δ_d| of the unrescaled run), the refined root times, and f_bare away
from masked samples — i.e. **dust-sector equivalence only**; the tilt
component itself (V vs Ṽ) is not compared in V5, and no state-variable
conversion was needed because both runs start from V(t_i)=Ṽ(t_i)=0
(equivalent under Ṽ=(1+w_eff)V for finite w_eff) and only tilt-invariant
quantities are compared.  The frozen `transform_barotropic_state`
implements the analytic conversion but V5 does not require it.
Scenarios tested: `printed_4_15|5π` under both tilt labels (numerics:
tight DOP853, n=1000, the fixed dense/root configs).  The V7 tilt factor
adds `printed_4_15|2π` (delta −3.5e−14 %); the derived branch and the
other modes were not given a dedicated tilt study — a coverage note, not
a defect, since the tilt equivalence is an algebraic property of the
frozen B2 layer already validated in Phase 1C-B2 across branches.  Both
labels are retained in metadata (tested) and never ranked.

## 16. Scale-independence audit — COMPLETE

- **Not an artifact of ignoring the scenario:** the two clean V6 runs
  differ *only* in harmonic metadata, and the mapped outputs *do*
  differ (absolute δ_m endpoints differ; asserted non-close in
  `test_clean_relative_growth_invariant_under_harmonic_metadata`), so
  the scenario object demonstrably reaches the output; only the
  dynamics are k-free.
- **Equations:** the frozen Mészáros and comoving RHS
  (`perturbations/systems.py`) contain no k anywhere in their matrices
  — verified by reading; the growth layer's clean path never passes
  `supplied_mode_k` into any dynamical call (it is consumed only by
  `HarmonicMetadata` after integration; histories.py:285–288).
- **Identical initial mode mixtures:** both V6 runs resolve the same
  frozen `PLANCK_2018_QPLUS_RECIPE` ICs (same recipe, rate units, h).
- Mapped absolute δ_m scales as −1/k_code² exactly (V2 factor 0.0;
  49/169 ratio implied by k=7 vs 13 runs).
- Relative histories and rates: **bit-identical**
  (`np.array_equal` in both the test and V6). ✓
- **Barotropic resolved k_code values** (upstream_timescape_k ⇒
  matrix_k = supplied): 2π = 6.283185307179586,
  5π = 15.707963267948966, 10π = 31.41592653589793.  Scale dependence
  demonstrated: printed-branch endpoint relative growth
  +4.7326 / −2.6206e4 / −5.1717e14 at 2π/5π/10π (and the crossing
  pattern itself changes with k).  Both artifact and report attach the
  "deterministic three-mode … no spectrum" disclaimer; nothing
  interprets the three modes as a spectrum. ✓

## 17. Test-suite audit — COMPLETE

Re-run in this audit session (commands exact):

| environment | command | result |
|---|---|---|
| CPython 3.14.3, NumPy 2.5.1, SciPy 1.18.0 | `.venv\Scripts\python -m pytest -q` | **337 passed in 9.86 s** |
| CPython 3.11.9, NumPy 2.4.6, SciPy 1.17.1 | `.venv311\Scripts\python -m pytest -q` | **337 passed in 12.16 s** |

Collected = 337 in both (`--collect-only -q` re-verified); failed = 0,
skipped = 0 (the artifact exists, so the artifact-schema test ran),
xfailed = 0, xpassed = 0, warnings = 0 (no warnings summary emitted).
Arithmetic: 337 total − 69 collected from the four new growth test
modules (re-verified by targeted collection) = 268 pre-1D-B tests, the
number the preflight reports. ✓

Qualitative classification of the 69 new tests:

- **Independently calculated expectations:** frozen 1D-A brackets
  (external data, 6 parametrised scenarios × both components); analytic
  `cos(3πt)` scan roots off-sample; synthetic extraction arrays; the
  finite-difference f_bare cross-check; the audited chain-factor value
  1.08416 at t0; a_obs/a_D/redshift cross-checks against the Phase 1B
  background; the mapped-derivative +3Z/(Θk²) recomputed from state +
  background.
- **Identity/wiring tests** (recompute the same formula from the state
  to catch mis-wiring, not re-derive it): f·D = dD/dlna, chain-factor
  product, −3Z/Θ comparison.
- **Structural/behavioural:** enum labels, no-defaults, rejections,
  immutability, serialization split, purity scans.
- **Artifact-content only:** exactly one
  (`test_validation_artifact_schema_when_present`), which checks schema
  keys/taxonomy strings, not numbers — it cannot mask a shared numeric
  error, and the numeric gates live in the script itself.
- **Shared-error risk:** the identity tests would pass if the
  implementation and the test both used a wrong formula; that risk is
  covered by the *independent* anchors above (frozen brackets, FD
  cross-check, 1D-A audited values) and now additionally by this
  audit's event-detection reproduction.  Coverage is scientific, not
  merely structural. ✓

## 18. Artifact and report consistency audit — COMPLETE

- Script ↔ artifact: gates, configurations, scenario labels, taxonomy
  strings, and every study structure in the artifact match the script's
  literal declarations (Sec. 9–13 extractions).  Provenance block:
  repository commit 878a97e…, upstream 590c6fd…, notebook 86d2534…,
  environment CPython 3.14.3 / NumPy 2.5.1 / SciPy 1.18.0.
  `gate_failures = []`, `all_gates_passed = true`.
- Report ↔ artifact: **every manually quoted number in the report was
  located in the artifact and matches**, including the full 10-root
  table (all five columns per root), all residual/scale values
  (1.46e−12→"1.5e−12", 2.97e−11→"3.0e−11", …), the V3 table (all 12
  worst-normalized entries), V5 (3.93e−11, 1.55e−12, 4.58e−9), V6
  endpoints, V7 (all eight rows, baseline 4.7326/0.14661), clean
  f_bare(t0)=0.31027→"≈0.3103", and G_Δ=G_m 1.877e−16→"≤1.9e−16".
  Two rounding nits only (B-list): report Sec. 18 says dressed-z
  spreads "≤ 1.5e−12" where the artifact maximum is 1.531e−12, and
  Sec. 19 prints the chain factor as "1.08417" by dividing
  already-rounded values (exact quotient 1.084156, i.e. 1.08416 — the
  1D-A audited value).
- Completion-message claims ↔ artifact: all reproduced (identities
  ≤ 3.9e−16, solver ≤ 3.1e−9, spreads ≤ 2.2e−14, tilt 3.9e−11 /
  ≤ 1.6e−12, one-factor deltas as in Sec. 13).
- Fresh recomputation without overwriting: this audit did **not** run
  the validation script (it would overwrite the artifact in place — see
  C-list); instead the key artifact quantities were recomputed fresh in
  memory: all ten roots by an independent path (≤ 9.6e−12, Sec. 8),
  G_Δ=G_m and rate equalities (Sec. 14), the reference-adjacency
  behaviour (Sec. 6), the one-factor arithmetic (Sec. 13), and the
  chain factor (Sec. 3).  The artifact SHA-256
  (`6e7deae8927261d30c012a8609b3b92a8242ed9b054a8475b5119080382244b5`)
  is unchanged after the audit.
- Schema: contains every required element (provenance, environment,
  numerical configuration incl. the reference solver, pre-declared
  gates + justification, V1–V7, uncertainty taxonomy, gate failures)
  and **no** forbidden spectrum/σ/RSD/likelihood/fitting field
  (recursive key scan: zero hits).

## 19. Documentation-language audit — COMPLETE (two stale docstrings, B-list)

All seven mandated statements verified present in README.md (quote
block, lines 55–63), CLAUDE.md (Phase 1D-B entry), the package
docstring (`growth/__init__.py` lines 3–26), and report Secs. 1/23:
Δ_d ≠ ordinary density contrast; mapped δ_m = solver-harmonic
coefficient only; relative histories/rates invariant under the fixed
harmonic factor; logarithmic rates piecewise across crossings; both D3
branches unresolved; D2 excluded; no spectrum/σ_8/observational
fσ8/RSD observable exists.

Improper-authority scan (correct/corrected/canonical/preferred/
physical/intended/recommended/default over all new files): every hit is
either (i) a negation ("neither is canonical…", "no default"), (ii) the
adjudicated D2 finding ("corrected c²ₛ", "D2-corrupted") — a documented
upstream algebra error, not an unresolved convention, and consistent
with the frozen Phase 1B/1C language, or (iii) a historical quotation.
No unresolved choice is ranked anywhere in the new implementation.

Two *internal* docstring inaccuracies found (both describe superseded
policies; the implementation, tests, artifact, and report all document
the actual policy correctly):

1. `scenarios.py` `GrowthNumericsConfig` docstring (lines 424–427):
   describes the near-zero floor as relative to "max|y|" (global);
   implemented policy is neighbour-local
   (`rates.amplitude_near_zero_mask`, correctly documented there and in
   report Sec. 11).
2. `scenarios.py` `GrowthReference` docstring (lines 342–345):
   describes the amplitude floor as "relative to the trajectory's
   maximum |Delta_d|"; implemented policy is the span-based
   Newton-distance/root-proximity time tolerance (correctly documented
   in `resolve_reference` and report Sec. 6).

## 20. Final verdict

### A. Blocking defects before commit

**None.**  No defect was found that invalidates scientific correctness,
reproducibility, scenario explicitness, root handling, or scope
preservation.  All ten roots were reproduced by an independent method;
all identities, interval semantics, rejection rules, and scope
exclusions verified.

### B. Required corrections before commit

All documentation-only; no code behaviour, number, or test changes:

1. `src/timescape_fsigma8/growth/scenarios.py` —
   `GrowthNumericsConfig` docstring: replace the stale global-max
   near-zero description with the neighbour-local policy actually
   implemented in `rates.amplitude_near_zero_mask`.
2. `src/timescape_fsigma8/growth/scenarios.py` — `GrowthReference`
   docstring: replace "relative to the trajectory's maximum |Delta_d|"
   with the implemented span-based Newton-distance/root-proximity time
   tolerance.
3. `reports/phase1d_b_growth_pipeline_validation.md` Sec. 18 (and, on
   its next regeneration, the artifact taxonomy line "V4 spreads across
   solver methods at fixed grid"): state explicitly that all V4
   refinements consume the same dense DOP853 continuous representation,
   so the ≤ 2.2e−14 spread measures grid/bracket robustness of the
   refinement, not cross-method agreement (cross-method evidence: V3,
   and the event-detection reproduction of this audit).
4. `reports/phase1d_b_growth_pipeline_validation.md` Sec. 19: add one
   sentence noting that the −230 % D3 delta (and the k-convention
   endpoint-rate flip) spans a sign reversal and is a signed trajectory
   difference, not an uncertainty magnitude.
5. Same report, two rounding nits: "≤ 1.5e−12" → "≤ 1.6e−12" (measured
   1.531e−12) in Sec. 18; "1.08417" → "1.08416" (exact 1.084156) in
   Sec. 19.

### C. Non-blocking improvements

- *Architecture:* deduplicate the barotropic y0 assembly
  (crossings.py:119–122 repeats solve_barotropic's line); give
  `scripts/validate_growth_pipeline.py` an output-path argument so the
  artifact can be regenerated to a scratch location for audits.
- *Documentation:* note in growth_test_utils.py that at n=1000 the
  sampled brackets coincide with the frozen 1D-A brackets by grid
  identity (pre-empts a "copied roots" misreading).
- *Performance:* V4 re-runs the identical dense solve 6× per scenario;
  a cached dense solution (or per-method dense configs, which would
  also fix the Sec. 9 finding properly) would be both faster and more
  informative.
- *Test quality:* add a dense-Radau (or event-based) root cross-check
  test so cross-method root independence is covered inside the suite;
  optionally extend V5 tilt equivalence to the derived branch.

### D. Claims independently verified (reproduced, not merely located)

1. Branch/HEAD/tags/ancestry/upstream/notebook-hash/clean-index state
   (all re-executed).
2. **337 passed** on CPython 3.14.3 and CPython 3.11.9 (both suites
   re-run in this audit); 268 + 69 = 337 collection arithmetic.
3. **All ten baseline refined roots** — reproduced to ≤ 9.6e−12 code
   time by solve_ivp event detection under Radau and LSODA, a path
   sharing neither the integrator nor the root machinery with
   production; root *counts* (including zero for printed|2π)
   reproduced continuously, confirming no discarded root.
4. Every root strictly inside its frozen 1D-A bracket (distances
   recomputed from artifact endpoints; brackets verified verbatim
   against `phase1d_a_observable_inventory.json`
   `crossing_brackets_code_Gyr_dressed_z`, in both copies used by
   tests and script).
5. Chain factor at t0 = 1.084156 recomputed from f_v(t0) alone; equals
   the V7 f_dressed/f_bare quotient.
6. One-factor deltas recomputed arithmetically from raw artifact
   endpoints: −0.0425 %, −0.702 %, −1.401 %, −230.2 %, −32.43 %.
7. G_Δ = G_m (≤ 1.9e−16) and rate equality from the mapped coefficient
   (≤ 3.6e−16) recomputed live on both sides of the pole for three
   modes.
8. Reference-adjacency policy exercised live on both sides of a
   refined crossing (rejected inside tolerance, accepted outside, with
   correct interval membership).
9. Large-amplitude runs re-executed with warning capture: no
   overflow/underflow/stiffness warnings, all samples finite.
10. Scope purity re-checked by independent greps (source, tests,
    script, report, artifact keys) beyond the packaged purity tests.
11. Report-vs-artifact number equality for every manually quoted value
    (10-root table, V3 table, V5/V6/V7 numbers).

### E. Claims not independently verified

1. **"268 pre-implementation tests passed" as a historical preflight
   event** — the pre-implementation state cannot be re-run without
   moving the new files (prohibited here); the figure is consistent
   with 337 − 69 and with the committed Phase 1C-B2 record.
2. **"Both 1D-A specification documents were read completely before
   design"** — a process claim with no verifiable artifact; the
   implementation's fidelity to both documents is indirect evidence.
3. **"Gates declared before execution and never relaxed"** — the gates
   are declared before the studies *in program order* and carry an
   a-priori justification, but with nothing committed there is no
   version history to prove the file's edit sequence; the 10³–10⁷
   margins make post-hoc tuning implausible but unproven.
4. **V4 as evidence of cross-method root agreement** — disproved as
   stated (shared dense representation; DOP853/Radau rows bit-identical);
   the underlying agreement was instead established by this audit's
   independent path (Sec. 8/9).  Classified PARTIAL, remedied by B.3.
5. The 3.11 environment's historical run during the implementation
   session (only today's re-run is verified — same result).

### F. Scientific findings requiring human review

1. **Extreme barotropic amplitudes:** |Δ_d(t0)| reaches ~3e12 (printed,
   10π) and ~2.7e14 (derived, 10π); endpoint relative growth −5.2e14 /
   −4.5e16.  Numerically converged (Sec. 12) but far outside any linear
   regime; physical meaning, and whether the k-mode normalisation is
   even comparable across branches, needs expert judgement (mirrors the
   paper's own Fig. 3 blow-up).
2. **Signed percentage deltas across sign reversals:** the D3 −230 %
   and the k-convention rate flip are trajectory sign changes; they
   must not be quoted downstream as error bars (B.4 adds the label).
3. **Crossing policy:** logarithmic growth rates are undefined at Δ_d
   roots and reported piecewise; any downstream consumer wanting a
   single global "f(z)" for barotropic modes must confront the poles —
   the policy (NaN + intervals, non-log derivatives always finite) is
   a *choice* frozen from 1D-A that a human should ratify.
4. **Unresolved convention/closure dependence:** the one-factor spreads
   (D3 branch dominant, then k convention, epoch, rate units, preset)
   and the Mészáros-as-comparison-system caveat mean no single growth
   history is yet identifiable as "the" Timescape prediction; D3/F7/
   epoch/IC-unit resolutions still require author input, as documented.
5. **σ_R/σ_8/fσ8 remain impossible by construction** in this layer
   (no spectrum, normalisation, or dressed-comoving map); the 1D-A
   blocker verdicts stand unchanged.

### G. Commit readiness

**READY_AFTER_NON_SCIENTIFIC_CLEANUP**

The implementation is scientifically correct, scope-clean,
reproducible, and fully explicit; every blocking-class check passed and
the numerical claims were independently reproduced.  The B-list
consists solely of documentation wording (two stale docstrings, one
overstated convergence framing, one sign-reversal label, two rounding
nits); no code path, number, test, or artifact value requires change.
