# Phase 1F-B v2 — Independent targeted adversarial audit

Audit classification: `INDEPENDENT_ADVERSARIAL_READ_ONLY_AUDIT` (targeted:
adjudication of corrections C1–C9 from the v1 audit, plus core-physics
regression). Audit date (UTC): 2026-08-28. The v2 validation report,
inventory, tests, and script were treated as claims under test.

Nothing in the repository was modified, staged, committed, amended, stashed,
reset, restored, rebased, merged, cherry-picked, or pushed. The v1 adversarial
audit was not touched. The only file created is this report, left untracked.

---

## 0. Repository state

| Item | Expected | Resolved | Status |
|---|---|---|---|
| Branch | `phase-1f-b-dust-wall-boost-dynamics` | identical | PASS |
| v2 HEAD | `16440e1a…` | **`16440e1a682c8d62d1e1b1d15fe8fad9290fa66a`** | PASS |
| Parent | `27fd65fd2a05c5b990508d948703897f433b566e` | identical (single parent) | PASS |
| v1 tag → peel | `d784074049148fad65632fe91848eada8923bb7a` → `27fd65fd…` | identical | PASS |
| v2 tag object | `bd1facf1fce2…` | **`bd1facf1fce246ef6fb42d02f03c5da6c2eef3a0`**, annotated, SSH-signed | PASS |
| v2 tag peel | current HEAD | `16440e1a682c8d62d1e1b1d15fe8fad9290fa66a` | PASS |
| `main` / `origin/main` | `87af7976b82b0b38e2c3e77dfc9458e664034c5d` | identical (`ls-remote` confirms) | PASS |
| History `main..HEAD` | v1 then v2, linear | exactly two commits, **0 merge commits** | PASS |
| Worktree / index / ops / stash | clean | clean, empty, none, none | PASS |
| Upstream | `590c6fd5332acb15…`, clean | identical, clean | PASS |
| Notebook SHA-256 | `86d2534d…de55a` | identical | PASS |
| Remote 1F-B refs | none | none | PASS |
| `git diff --check` / `--cached --check` | clean | clean before and after the audit | PASS |

Tags re-verified after the audit: unchanged.

History:

```
87af7976b82b0b38e2c3e77dfc9458e664034c5d   main / origin/main
    |
27fd65fd2a05c5b990508d948703897f433b566e   Phase 1F-B v1   (tag d7840740…)
    |
16440e1a682c8d62d1e1b1d15fe8fad9290fa66a   Phase 1F-B v2   (tag bd1facf1…)
```

**Test suites** (`-p no:cacheprovider -rsxX`, no suppression):

| Environment | Targeted | Full | Failures | Skips | XFails | Warnings |
|---|---|---|---|---|---|---|
| Python 3.14.3 (numpy 2.5.2 / scipy 1.18.1) | 37 passed | **576 passed** | 0 | 0 | 0 | 0 |
| Python 3.11.9 (numpy 2.4.6 / scipy 1.17.1) | 37 passed | **576 passed** | 0 | 0 | 0 | 0 |

The v2 validation artifact regenerated to a scratch path on both stacks is
byte-identical and equals the inventory-recorded SHA-256
`961e491497b7c960ab4cd0a091f23a98dfdc9e2034ed3e5efeb3f4396069dce6`. That
identity is recorded as reproducibility, not as scientific validation.

---

## 1. C1 — `R_A` evidence classification

Verified everywhere materially relevant:

- **Source**: `PROPAGATION_CONSTRUCTION_DIAGNOSTIC = "CONSTRUCTION_INVARIANT_WITH_TIME_DISCRETIZATION_ERROR"` and `EXPANSION_COMPATIBILITY_EVIDENCE = "INDEPENDENT_SCIENTIFIC_COMPATIBILITY_GATE"`; both stamped into `ScalarDustWallBoostDiagnostics` (`propagation_evidence_classification`, `expansion_compatibility_evidence_classification`); `Phase1FBPropagationError` docstring reworded to "construction/time-discretisation diagnostic".
- **Report** §15 now states `R_A` "is not independent physical validation in this scalar construction … a construction identity up to the implemented time-discretization error"; §14 marks `C_Θ` as the independent gate "not aggregated with the construction diagnostics"; §22's tolerance table calls the propagation row a "construction/time-discretization diagnostic". A grep for residual "independent" wording finds no leftover overclaim.
- **Inventory**: `residuals.propagation_geodesic.independent_physical_validation = false`, `evidence_classification` set, the former `independent_of_expansion_compatibility` renamed to `evaluated_separately_from_expansion_compatibility`; `expansion_compatibility.evidence_classification` set.
- **Script**: `evidence_classification.propagation` / `.expansion_compatibility` emitted.
- **Tests**: the v1 test renamed to `test_propagation_construction_diagnostic_can_fail_its_numerical_gate`; `test_residual_evidence_hierarchy_is_explicit` asserts both tokens and the curl status.

`C_Θ = δΘ_{d,w} − δΘ_W − Lψ/a²` remains the sole independent compatibility gate; its value `5.551115123125783e-17` reproduced. The v1 fact that `R_A` is bit-identical across unrelated expansion sectors is unchanged by v2 (the diagnostic code is untouched).

**C1: `PASS`.**

---

## 2. C2 — Explicit boost-specific no-penetration closure

`BoostBoundaryKernelPolicy` now requires, with no defaults:
`physical_boundary_condition == EXPLICIT_EXTERNAL_NO_PENETRATION_CLOSURE`,
`derived_from_timescape == False` (True is rejected: "not derived from
Timescape"), `inherited_from_h1_density_transmission == False` (True
rejected), and `physical_interface_claim == "NOT_GRANTED"` (anything else
rejected). The classification constant's value became
`EXPLICIT_EXTERNAL_BOOST_BOUNDARY_CLOSURE`. Report §12 now states the
condition plainly as `D_nψ|_Γ = v^a n_a|_Γ = 0`, "an explicit external
no-penetration closure … not derived from Timescape, not inherited from H1
density transmission, does not turn Γ into a physical material wall". The
inventory carries `derived_from_timescape: false`,
`inherited_from_h1_density_transmission: false`,
`physical_material_wall_claim: NOT_GRANTED`, `physical_interface_claim:
NOT_GRANTED`, `runtime_enforcement: FAIL_CLOSED`.

**Operator-domain inspection.** The reused matrix is the Phase 1F-A *broken
regional* operator (mask-crossing edges omitted; natural zero-flux), not the
H1 transmission operator; `dynamics.py` still imports only
`assemble_regional_elliptic_system` / `apply_regional_laplace_beltrami` and
nothing from `ContinuumTransfer`. The policy docstring separates the two
explicitly: "The numerical no-flux realization reuses the Phase 1F-A regional
matrix, but this record is a new explicit boost modeling choice." That is the
required `NUMERICAL_OPERATOR_REUSE` versus `PHYSICAL_BOUNDARY_DERIVATION`
distinction, expressed in prose and booleans rather than as a literal token.
The mathematically identical Neumann form is nowhere presented as a
derivation.

**C2: `PASS`.**

---

## 3. C3 — Initial normal-derivative fail-closed gate

**Implementation.** `_interface_normal_components` enumerates every wall cell
with a non-wall neighbour along any axis and evaluates
`s · γ^{aj}∂_jψ / (a √γ^{aa})` with the frozen one-sided regional gradient —
exactly the normal component of the returned velocity representation. The
gate is applied to `potential[0]` in **both** initialization modes, before the
time march, against `boundary_normal_velocity_tolerance` (a required,
unit-tagged, sealed `ScalarDustWallBoostNumerics` field; recorded in
diagnostics as `initial_boundary_normal_velocity_tolerance`).

**The v1 adversarial case now fails at the intended gate.** I rebuilt it
independently on the `(4,4,4)` two-layer wall: mean-zero `ψ` with a normal
jump of `0.004`, wall expansion manufactured so that `C_Θ` would pass, zero
driver. Result: `Phase1FBBoundaryCompatibilityError: initial scalar boost
violates the external no-penetration boundary closure`; the v2 trace at Γ is
`0.016` (identical to the v1 measured normal velocity) against tolerance
`2e-11`. No earlier gate intercepted it (off-domain, mean-zero, and driver
gates all pass for this input).

**No projection, no modification.** For an admissible supplied potential the
returned `scalar_potential[0]` is bit-identical to the supplied array
(`np.array_equal` → `True`); the diagnostic reads `0.0`.

**Admissible nontrivial potential passes.** The `(8,4,4)` profile
`0.002·[−1,−1,+1,+1]` along the normal is accepted with initial and propagated
traces exactly `0.0`.

**Explicit condition (finite-resolution consequence, not reported by v2).**
The trace is the *strong-form* one-sided derivative. The FV natural (weak)
no-flux condition does not make that one-sided difference vanish for a
generic smooth source: I fed the expansion-matched branch a smooth cosine
normal profile whose continuum normal derivative is zero at both faces; the
reconstructed `ψ₀` has a one-sided face trace of `0.00866` (O(h)) and is
**rejected**. The gate is behaving honestly — the returned velocity would
otherwise penetrate Γ — but it means expansion-matched initialization with
genuinely normal-varying sources is, at the validated resolution, restricted
to sources whose FV solution is exactly flat at the faces. v2 does not say so.

**C3: `PASS_WITH_EXPLICIT_CONDITIONS`.**

---

## 4. C4 — Dynamic preservation of the boundary

v2 enforces both halves. The projected lapse history is gated at **every**
time against `boundary_normal_acceleration_tolerance` before the march
("wall lapse driver violates …"), and the propagated potential is gated at
every time after the march ("propagated scalar boost violates …").

**D1 (compatible `ψ₀`, boundary-incompatible time-dependent `ν_W`).** The v2
fixture uses lapse amplitude `[0, 1e-4, 2e-4]` on the penetrating profile, so
the driver is *exactly compatible at t = 0*. My independent per-time trace of
the driver: `[0.0, 8.0e-4, 1.6e-3]`. An initial-time-only check would
therefore **pass**; the all-time gate rejects with the driver message. This is
precisely the case the brief required, and it reaches the intended gate.

**D2 (compatible `ψ₀`, genuinely spatially varying compatible `ν_W`).**
Accepted. Propagated boundary trace `0.0` at all times, driver trace `0.0`,
`ψ(t)` equal to a hand trapezoid to `0.0`. The returned normal velocity per
wall layer at t = 0.5 is `[0.0, 0.0156, 0.0156, 0.0]` — real normal flow in the
interior with exact zeros at both Γ faces.

Because `ψ(t) = ψ₀ − ∫Q₀ν` is linear and `Q₀` subtracts a constant, the driver
gate plus the initial gate guarantee preservation; the propagated gate is the
independent confirmation.

**C4: `PASS`.**

---

## 5. C5 — Normal-varying fixture

Inspected the numerical field, not the test name: `normal_varying_case`
places `0.002·profile` on wall layers 0–3 of an `(8,4,4)` carrier
(`h₀ = 1/8`); layer values at t = 0 are `[−0.002, −0.002, +0.002, +0.002]`.
It varies only along the normal (constant in the tangential directions),
which is sufficient for the stated purpose.

**Sensitivity to the operator model.** Broken wall-interior Laplacian versus
the unbroken periodic Laplacian of the zero-extended field differ by `0.128`,
which I reproduced in closed form (`0.002/h₀² = 0.128`) and numerically, against
`|Lψ|_max = 0.256` — a 50 % effect, versus the v1 fixtures' `3.6e-15`.

Admissible (`[−1,−1,1,1]`) and inadmissible (`[−1.5,−0.5,0.5,1.5]`) profiles are
physically different fields, the second penetrating Γ by construction; both
the test suite (V13–V16) and the validator exercise them. Normal derivatives
are no longer identically zero by construction.

**C5: `PASS`.**

---

## 6. C6 — Convergence evidence classification

Token `SECOND_ORDER_NUMERICAL_SELF_CONVERGENCE_OF_THE_IMPLEMENTED_TIME_INTEGRATOR`
is public; the inventory records
`convergence_independent_physical_validation: false`; the script emits
`independent_physical_validation: "NO"` and the interpretation
`CLOSED_FORM_TRAPEZOIDAL_TRUNCATION_SCALING_OF_THE_IMPLEMENTED_RULE`; report
§19 states the script "reimplements the same trapezoidal update and measures
its closed-form truncation scaling … numerical implementation evidence, not
independent validation of the physical propagation law". The study is
retained.

Independent recomputation through the production function: intervals 4 →
`7.8125e-06`, 8 → `1.953125e-06`; closed form `1.25×10⁻⁴h²` gives the same
digits; ratio exactly 4 → second order.

**C6: `PASS`.**

---

## 7. C7 — `wall_proper_time_rate`

**What v2 did (outcome A).** A required closure field
`wall_proper_time_rate_role` must equal
`PROVENANCE_ONLY_NON_DYNAMICAL_METADATA`; the token is echoed in the result
record, inventory, and report §6 ("because the implemented derivative is with
respect to declared common time"). The field is still never read by
`dynamics.py`. The new test asserts that doubling the rate leaves `ψ`
identical. I confirmed the runtime accepts rates `2.0`, `0.5`, `7.3` and
returns bit-identical `ψ` in all cases.

**Why this is incomplete.** The frame law in report §9,
`v̇ + H_W v = −A_W`, is derived along the wall observers' worldlines: the dot
is the wall **proper-time** derivative and `H_W = Θ_W/3` is a proper-time
rate. The closure's `wall_proper_time_rate` is precisely `N̄ = dτ_W/dt`. With
`A_W = Dν` (a spatial gradient, rate-independent) and `d/dτ = N̄^{-1} d/dt`,
`H_τ = N̄^{-1}H_t`, the common-time form is

```
dv/dt + H_t v = −N̄ Dν        ⇒        ψ̇_t = −N̄ Q₀ ν_W .
```

The implemented `ψ̇_t = −Q₀ν_W` is the `N̄ ≡ 1` gauge. v2 neither gates
`wall_proper_time_rate ≡ 1` nor states that the supplied lapse potential is
already common-time-normalized (`N̄` absorbed into `ν_W`); it declares the
rate non-dynamical *because* the update is in common time — which is the
reason the factor appears, not the reason it vanishes. For every fixture and
every reported number `N̄ = 1`, so no result is wrong; but a closure with
`N̄ ≠ 1` is accepted and evolved with a source off by the factor `N̄`, and the
v2 test codifies that as the intended invariance.

This avoids both explicit rejection criteria of the brief (it neither
pretends the field is load-bearing while ignoring it, nor invents arbitrary
dependence), and outcome A is the right *shape* of resolution. It is missing
the one condition under which outcome A is scientifically true.

**C7: `PARTIAL`.** Minimal fix: gate `wall_proper_time_rate` to unity within
an explicit tolerance and label the role a declared gauge condition
(`COMMON_TIME_EQUALS_BACKGROUND_WALL_PROPER_TIME`), **or** define `ν_W` in the
closure/report/inventory as the common-time-normalized acceleration
potential; in either case replace the invariance test with one that reflects
the chosen convention. No dynamics need to be added.

---

## 8. C8 — Shear-free restriction

`CommonSpacetimeWallGeometryClosure` requires
`selected_background_geometry_sector` to be a `WallBackgroundGeometrySector`
(single member `SHEAR_FREE_QUASI_FLRW_COMMON_SPACETIME`) and
`wall_background_shear_free == True`. Adversarial declarations, both rejected
by me independently: `wall_background_shear_free=False` → "V1 requires the
explicit scalar, vorticity-free, shear-free sector";
`selected_background_geometry_sector="NONZERO_WALL_SHEAR"` → "the explicit
shear-free quasi-FLRW background sector is required". The result carries
`wall_background_shear_status = EXCLUDED_BY_EXPLICIT_SELECTED_GEOMETRIC_SECTOR`
and `wall_shear_zero_as_timescape_prediction = NOT_GRANTED`; report §23 says
"Wall shear is excluded by this model restriction; it is not predicted to
vanish by Timescape". The simplified equation cannot run against a geometry
that declares nonzero shear.

**C8: `PASS`.**

---

## 9. C9 — Harmonic vector sector

The result record validates `harmonic_vector_sector_status =
EXCLUDED_BY_EXPLICIT_SCALAR_MODEL_RESTRICTION` and
`harmonic_vector_zero_as_timescape_prediction = NOT_GRANTED` at construction
(any other value raises). The inventory's `vector_sector_ontology` separates
the scalar constant kernel, the transverse vector sector, and the harmonic
vector sector, and states
`scalar_mean_zero_eliminates_harmonic_vector_modes: false`, `vector_solver:
NOT_IMPLEMENTED`. Report §11 adds: "Mean-zero normalization of the scalar
potential does not resolve that vector sector." No contradictory wording found
in source, tests, script, report, or inventory. The v1 numerical fact stands:
the mass-weighted mean of any `Dψ` on the wall is exactly zero, so a uniform
drift is unrepresentable.

**C9: `PASS`.**

---

## 10. Core-physics regression (R1–R5)

| Check | Independent result | Status |
|---|---|---|
| R1 sign `D_av^a = δΘ_d − δΘ_W` | at the `ψ` maximum my own div∘grad gives `−0.032`, the code's `Lψ` gives `−0.064`: same sign (converging dust ⇒ smaller dust expansion) | PASS |
| R2 `D_w² = L_w/a_w²` | ratio `[my D²ψ]/[code Lψ/a²]` = `0.5, 0.5, 0.5` for `a = 1, 2, 3` — `a`-independent (the constant 0.5 is my wide stencil) | PASS |
| R3 `ψ̇ = −Q₀ν` | `max｜ψ_{i+1} − ψ_i + (dt/2)(ν_i + ν_{i+1})｜ = 2.2e-19` | PASS |
| R4 background `γ_w` firewall | `phase1f_b` still imports nothing from `timescape_fsigma8.background`; `BACKGROUND_TIMESCAPE_GAMMA_W` rejected | PASS |
| R5 no implicit zero boost | zero driver, `v₀ = 0.002√17 = 0.00824621125123532`, `Δψ = 0.0` | PASS |

No regression. The v2 commit adds gates, tokens, fields, and fixtures; it does
not touch the update rule, the operator, the compatibility residual, or the
1F-A/1E-G frozen code (confirmed by `git diff 27fd65f 16440e1` scope).

---

## 11. Evidence hierarchy

v2 now states the hierarchy the v1 audit asked for, and does not aggregate it:

| Tier | Item | Where declared |
|---|---|---|
| Independent scientific compatibility | `C_Θ` | source token, §14, inventory |
| Construction invariants | `R_A` (time-discretisation diagnostic), scalar curl | source tokens, §15/§16, inventory |
| Explicit model gates | boundary admissibility (initial, driver, propagated), scalar sector, shear-free sector, linear regime, kernel/normalization | §12, §17, §11, §22, inventory |
| Numerical evidence | integrator self-convergence, manufactured solutions, operator consistency (`0.128`) | §18, §19, inventory |

**Evidence-classification verdict: honest.**

---

## 12. Test independence (37 tests)

| Test | Class | Note |
|---|---|---|
| `v1` zero driver | INDEPENDENT_EVIDENCE | closed-form `0.002√17` |
| `v2` manufactured lapse | PARTIAL_EVIDENCE | trapezoid exact for linear `ν` |
| `v3` expansion perturbation | INDEPENDENT_EVIDENCE | `C_Θ` detects |
| `v4` reversed sign | CONSTRUCTION_IDENTITY_ONLY | sign chosen to match code (v1 audit supplied the derivation) |
| `v5`–`v7`, `v9`, `v12`, contract/integrity tests | INDEPENDENT_EVIDENCE | gate behaviour |
| `v8` family | PARTIAL_EVIDENCE | Q0 branch cannot alter the trajectory |
| `v10` linear gate | INDEPENDENT_EVIDENCE | |
| `v11` `a_w²` | INDEPENDENT_EVIDENCE | closed-form eigenvalue oracle |
| `propagation_construction_diagnostic_can_fail…` | PARTIAL_EVIDENCE | truncation only, now correctly named |
| `supplied_normal_varying_no_penetration…_accepted` | INDEPENDENT_EVIDENCE | genuine normal profile, trace exactly 0 |
| `supplied_normal_varying_penetrating…_rejected` | INDEPENDENT_EVIDENCE | physically different profile; intended gate reached |
| `boundary_incompatible_time_dependent_lapse…_rejected` | INDEPENDENT_EVIDENCE | driver compatible at t = 0, incompatible later |
| `boundary_compatible_driver_preserves…` | PARTIAL_EVIDENCE | `ψ(t)` oracle is a hand trapezoid; boundary preservation itself is independent |
| `normal_varying_fixture_distinguishes…` | INDEPENDENT_EVIDENCE | independently coded periodic Laplacian; `0.128` closed form |
| `shear_free_sector…` | INDEPENDENT_EVIDENCE | adversarial declarations rejected |
| `harmonic_vector_sector…` | vocabulary | classification-only correction |
| `residual_evidence_hierarchy…` | vocabulary | classification-only correction |
| `wall_proper_time_rate…provenance_only` | **asserts a physically unqualified invariance** (§7) | |
| `boundary_closure_is_external…` | INDEPENDENT_EVIDENCE | `derived_from_timescape=True` rejected |
| `evidence_only_convergence_classification…` | vocabulary | |

The normal-varying tests manufacture `δΘ_W` from the production broken
operator, so `C_Θ` is a construction identity *for those fixtures*; that does
not affect the boundary gates they test, which use physically distinct
profiles and reach the intended gate.

---

## 13. Validation artifact

Script read completely before running. New studies V13–V17 present. Reported
values reproduced independently: compatibility `5.551115123125783e-17`,
propagation diagnostic `5.204170427930421e-18`, velocity ratio
`0.01154469575172945` (= `0.0028√17`), boundary traces `0.0`/`0.0`/`0.0`,
`broken_vs_unbroken = 0.128` (closed form), convergence sequence
`7.8125e-06 … 1.2207e-07` (closed form `1.25×10⁻⁴h²`). All three new
`fail_closed` flags are `True`. Evidence classifications emitted as required.

---

## 14. State rank, public semantics, observational firewall

Only `ψ_dw` is evolved (one trapezoidal ODE); every v2 addition is a gate,
token, or field. `FROZEN_DIFFERENTIAL_STATE_RANK: 4`,
`SELECTED_SCALAR_REALIZATION_DIFFERENTIAL_STATE_RANK: 5`,
`DUST_TO_WALL_BOOST_FROM_Y_ALONE: NOT_DERIVED`, `UNIQUE_TIMESCAPE_PREDICTION:
NOT_GRANTED` all preserved. A grep of the v2 diff over `src`, `tests`,
`scripts` for tracer/galaxy/peculiar/RSD/Kaiser/σ₈/σ_R/fσ₈/likelihood/dressed
terms matches only file headers. The strongest output remains
`dust_velocity_relative_to_wall`, classified
`CONDITIONAL_SCALAR_LONGITUDINAL_REGIONAL_DUST_VELOCITY_RELATIVE_TO_EXPLICIT_WALL_OBSERVER_CONGRUENCE`.

---

## A. FINAL V2 AUDIT VERDICT

```text
TARGETED_V3_CORRECTIONS_REQUIRED
```

Eight of nine corrections pass (one with an explicit condition). The boundary
closure is genuinely fail-closed and preserved under the driver, evidence
classification is honest, shear and harmonic restrictions are explicit, and
the v1 core is unregressed. One correction, C7, is scientifically incomplete:
the "provenance-only" classification of `wall_proper_time_rate` holds only in
the `N̄ ≡ 1` gauge, which v2 neither enforces nor states.

## B. C1-C9 ADJUDICATION

| Correction                         | Verdict | Evidence |
| ---------------------------------- | ------- | -------- |
| C1 R_A classification              | `PASS` | tokens in source/diagnostics/report §15/inventory/script; no leftover "independent" wording; `C_Θ` remains the sole independent gate |
| C2 explicit boost boundary closure | `PASS` | required `physical_boundary_condition`, `derived_from_timescape=False`, `inherited…=False`, `physical_interface_claim=NOT_GRANTED`; operator reuse vs derivation stated; H1 transmission operator unused |
| C3 supplied-psi boundary gate      | `PASS_WITH_EXPLICIT_CONDITIONS` | v1 adversarial `ψ` rejected at the intended gate (trace `0.016` vs `2e-11`); admissible `ψ` returned bit-identical; strong-form trace rejects expansion-matched smooth normal sources at finite resolution (undocumented) |
| C4 dynamic boundary preservation   | `PASS` | driver gated at every time (D1 trace `[0, 8e-4, 1.6e-3]`: t=0-only check would pass); propagated `ψ` gated at every time; D2 preserved exactly with interior normal flow `0.0156` |
| C5 normal-varying fixture          | `PASS` | field `[−.002,−.002,.002,.002]` along the normal; admissible vs penetrating; broken vs unbroken `0.128` = `0.002/h₀²`, 50 % of `｜Lψ｜_max` |
| C6 convergence classification      | `PASS` | self-convergence token; `independent_physical_validation: false`; two errors reproduced in closed form |
| C7 wall_proper_time_rate           | `PARTIAL` | declared non-dynamical, but `ψ̇_t = −N̄Q₀ν` under the closure's own proper-time frame law; runtime accepts `N̄ = 2, 0.5, 7.3` with identical `ψ`; no unit-rate gate, no normalization convention |
| C8 shear-free restriction          | `PASS` | required enum + boolean; both adversarial declarations rejected; `WALL_SHEAR_PREDICTED_ZERO_BY_TIMESCAPE: NOT_GRANTED` |
| C9 harmonic-vector sector          | `PASS` | validated result tokens; `scalar_mean_zero_eliminates_harmonic_vector_modes: false`; report §11 explicit |

## C. CORE-PHYSICS REGRESSION CHECK

R1 sign, R2 `L_w/a_w²`, R3 `ψ̇ = −Q₀ν`, R4 background-lapse firewall, R5 no
implicit zero boost: all independently re-confirmed (§10). No regression.

## D. BOUNDARY-CLOSURE VERDICT

`EXPLICIT_EXTERNAL_NO_PENETRATION_CLOSURE`, declared by the scenario, not
derived from Timescape, not inherited from H1 density transmission,
`PHYSICAL_INTERFACE_CLAIM: NOT_GRANTED`, runtime enforcement genuinely
`FAIL_CLOSED` at the initial potential, over the full driver history, and on
every propagated potential. The v1 finding that supplied data could penetrate
Γ unchecked is closed.

## E. EVIDENCE-CLASSIFICATION VERDICT

Honest. `C_Θ` is the only item labelled independent; `R_A` and curl are
construction invariants; boundary/sector/linear/kernel are explicit model
gates; convergence is self-convergence of the implemented integrator; nothing
is aggregated.

## F. REMAINING SCIENTIFIC LIMITATIONS

- The common-time update is valid in the `N̄ = dτ_W/dt ≡ 1` gauge only (C7).
- Expansion-matched initialization with genuinely normal-varying smooth
  sources is rejected by the strong-form face trace at finite resolution
  (O(h) one-sided derivative, `0.00866` in my probe); the gate is honest but
  the restriction is undocumented.
- The normal-varying fixture varies only along the normal, and its operator
  distinction is against the zero-extended periodic Laplacian; no spatial
  refinement study exists for the boundary sector.
- `div(v_returned)` and the constrained `Lψ/a²` remain different discrete
  operators (v1 finding, unchanged; consistent, O(h²)).
- Missing perturbed wall/common-spacetime geometry, transverse and harmonic
  vector sectors, and all observational quantities remain outside the phase,
  as declared.

## G. INTEGRATION READINESS

```text
READY_FOR_STRICT_FAST_FORWARD_INTEGRATION: NO
```

## H. EXACT NEXT STEP

One v3 correction commit on top of `16440e1a…`, not amending v2 and not moving
either tag, that:

1. resolves C7 by **either** (a) adding a fail-closed gate
   `｜wall_proper_time_rate − 1｜ ≤ tolerance` with the tolerance declared in
   `ScalarDustWallBoostNumerics` and the role token renamed to a declared
   gauge condition, **or** (b) defining `ν_W` in the closure docstring, report
   §6/§9, and inventory as the common-time-normalized acceleration potential
   with `N̄` absorbed; and in both cases replacing
   `test_wall_proper_time_rate_is_explicit_provenance_only_metadata` with a
   test of the chosen convention;
2. adds one sentence to report §10/§12 recording the finite-resolution
   strong-form-trace restriction on expansion-matched normal-varying sources.

Then freeze as `phase-1f-b-dust-wall-boost-dynamics-v3` and re-audit that
single change.
