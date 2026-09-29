# Phase 1F-B v3 — Final narrow independent audit

Audit classification: `FINAL_NARROW_ADVERSARIAL_READ_ONLY_AUDIT`. Scope is
restricted to the v3 clock-semantics correction, its interaction with the
already validated v2 boundary closure, and Git history integrity. The v1/v2
scientific conclusions are treated as previously validated and are checked only
for regression.

Audit date (UTC): 2026-08-28. Target commit
`d2f150222cb08565aa9d0822747250309d8aaa67`, tag
`phase-1f-b-dust-wall-boost-dynamics-v3`.

Nothing was modified, staged, committed, amended, stashed, reset, restored,
rebased, merged, cherry-picked, or pushed. Neither prior audit was touched.
The only file created is this report, left untracked.

---

## 0. Repository state

| Item | Expected | Observed | Status |
|---|---|---|---|
| Branch | `phase-1f-b-dust-wall-boost-dynamics` | identical | PASS |
| v3 HEAD | `d2f150222cb08565aa9d0822747250309d8aaa67` | identical | PASS |
| v3 parent | `16440e1a682c8d62d1e1b1d15fe8fad9290fa66a` | identical | PASS |
| v2 parent | `27fd65fd2a05c5b990508d948703897f433b566e` | identical | PASS |
| v1 tag → peel | `d784074049…` → `27fd65fd…` | identical | PASS |
| v2 tag → peel | `bd1facf1fce2…` → `16440e1a…` | identical | PASS |
| v3 tag → peel | `61dc9cf76029…` → `d2f15022…` | identical, annotated | PASS |
| `main` / `origin/main` | `87af7976b82b0b38e2c3e77dfc9458e664034c5d` | identical | PASS |
| History | linear, 3 commits | 3 commits, **0 merges** | PASS |
| Worktree / index / ops / stash | clean | clean, empty, none, none | PASS |
| Upstream | `590c6fd5332acb15…`, clean | identical, clean | PASS |
| Notebook SHA-256 | `86d2534d…de55a` | identical | PASS |
| `git diff --check` / `--cached` | clean | clean before and after | PASS |
| Prior audits | unmodified | v1 `7ef51fcd…3ed`, v2 `6b443b5e…027` intact | PASS |

---

## 1. Clock definitions (F1)

Established from source, not names. `CommonSpacetimeWallGeometryClosure`
declares `common_time_units: COMMON_TIME` for the runtime grid, and
`wall_proper_time_rate` is documented and validated as
`alpha_W(t) = dtau_W/dt`. It is:

- **spatially homogeneous** — enforced structurally by the `(nt,)` shape
  contract; a `(nt, size)` array is rejected with "must match time_grid", so
  spatial dependence is impossible, not merely discouraged;
- **strictly positive and finite** — `0.0`, `-1.0`, `NaN`, `inf` all rejected;
- **explicit external closure** — a new required field
  `wall_proper_time_rate_provenance` must equal
  `REQUIRED_EXTERNAL_COMMON_SPACETIME_CLOCK_CLOSURE`;
  `TIMESCAPE_PREDICTED_CLOCK_DRIVER` is rejected;
- **load-bearing** — `wall_proper_time_rate_role` must equal
  `LOAD_BEARING_TIME_CONVERSION`; the stale v2 token
  `PROVENANCE_ONLY_NON_DYNAMICAL_METADATA` is now rejected.

**F1: `PASS`.**

---

## 2. Chain rule (F2, F3, F4) — highest priority

**Independent derivation.** The frame law is written along the wall congruence,
so its derivative is `d/dtau_W`. With `alpha_W = dtau_W/dt`,
`dpsi/dt = (dtau_W/dt)(dpsi/dtau_W) = -alpha_W Q_0 nu_W`. Exactly one factor of
`alpha_W` is required.

**Implementation inspection.** `dynamics.py` forms
`driver_regional = alpha[:, None] * projected_lapse` **once**, then uses it in
three places: the trapezoidal update, `potential_dot_regional = -driver_regional`,
and the `acceleration` gradient. No second multiplication exists anywhere.

**A — non-unit dependence.** With an identical initial state and a nonzero
driver, `alpha_W = 1` and `alpha_W = 2` are **not** bit-identical:
`max|psi(2) - psi(1)| = 1.0e-3`. Final amplitudes `0.0028 / 0.0036 / 0.0024`
for `alpha_W = 1 / 2 / 0.5`.

**Counterfactual discrimination.** I re-integrated with my own trapezoid and
compared against the production output:

| `alpha_W` | vs my `alpha`-scaled update | vs UNSCALED (v2) update | vs DOUBLE-`alpha` update |
|---|---|---|---|
| 1.0 | `0.0` | `0.0` | `0.0` |
| 2.0 | `0.0` | `1.0e-3` | `2.0e-3` |
| 0.5 | `0.0` | `5.0e-4` | `2.5e-4` |

The production result matches the single-`alpha` law exactly and is separated
from both the zero-`alpha` and double-`alpha` alternatives whenever
`alpha_W != 1`.

**B — zero-driver exception.** With `nu_W = 0`, `alpha_W = 1` and
`alpha_W = 7.3` give bit-identical `psi`. This is correct: `alpha_W` multiplies
zero. The repository records this in a dedicated test whose docstring states it
is "the only regime in which the superseded v2 invariance assertion was true",
so the exception is not generalized.

**C — time-dependent rate.** `alpha_W(t) = 1 + t` with a constant lapse
amplitude keeps the driver linear, so the analytic integral
`psi = psi_i - int alpha_W Q_0 nu_W ds = 0.002 + 0.001(t + t^2/2)` is exact.
Production versus that oracle: `4.34e-19`. The chain-rule contribution relative
to a unit clock is `5.0e-4`, i.e. the `t^2/2` term is entirely due to
`alpha_W(t)`.

**F2 `PASS` · F3 `PASS` · F4 `PASS`.**

---

## 3. `H_wall` time convention (F5) and double conversion (F6) — highest priority

**Contract evidence.** `wall_hubble_units` must equal `INVERSE_COMMON_TIME`
(validated at construction). The runtime enforces

```
log(a[i+1]/a[i]) / dt  -  0.5 (H[i] + H[i+1])  <=  scale_factor_rate_tolerance
```

where `dt = diff(time_grid)` on the **common-time** grid. This ties `H_wall`
numerically to `d ln a_w/dt`, so `H_wall` is a common-time rate — Case B. It
already equals `alpha_W H^tau_W`; applying `alpha_W` again would be a double
conversion.

**Implementation.** `hubble` enters the propagation diagnostic directly; no
expression multiplies it by `alpha`. Confirmed by reading the v3 diff: the only
new `alpha` use sites are the three driver sites above.

**Double-conversion detector.** I built a case with `a(t) = exp(0.05t)`,
`H = 0.05`, `alpha_W = 2`, nonzero driver, 201 points:

- observed `R_A = 1.16e-09` (trapezoid truncation on that grid);
- had `H` been replaced by `alpha_W H`, the residual would shift by
  `7.05e-04` — six orders of magnitude larger than the observed value and far
  above any tolerance in use.

So the detector has real power and reports no double conversion.

**F5 `PASS` · F6 `PASS`.**

---

## 4. `C_Theta` clock-factor firewall (F7)

`compatibility_regional = difference - laplacian/scale**2`. No `alpha` appears
anywhere in the expansion-difference path — verified by reading the v3 diff
(that region is untouched) and numerically: with wall expansion built **without**
any clock factor, `C_Theta` is `5.55e-17`, `8.33e-17`, `5.55e-17` at
`alpha_W = 1, 2, 0.5`. The same `alpha`-free relation holds at every clock rate,
as required for a constraint containing no time derivative. Both expansion
perturbations remain declared `INVERSE_COMMON_TIME`.

```text
CLOCK_FACTOR_IN_C_THETA: ABSENT_AS_REQUIRED
```

**F7: `PASS`.**

---

## 5. `R_A` clock consistency (F8)

The implemented residual is
`(v[i+1]-v[i])/dt + H_bar v_bar + mean(acceleration)` with
`acceleration = D(alpha_W Q_0 nu_W)/a`. Every term is common-time: a
common-time numerical derivative, the common-time `H_W = d ln a_w/dt`, and a
source carrying exactly one `alpha_W`. No mixed wall-proper/common-time term
remains. The classification is unchanged and not upgraded:
`propagation_evidence_classification = CONSTRUCTION_INVARIANT_WITH_TIME_DISCRETIZATION_ERROR`,
against `expansion_compatibility_evidence_classification =
INDEPENDENT_SCIENTIFIC_COMPATIBILITY_GATE`.

**F8: `PASS`.**

---

## 6. Boundary preservation with a non-unit clock (F9)

The gate is applied to the quantity that drives the evolution,
`alpha_W Q_0 nu_W`. Since `alpha_W > 0` is spatially homogeneous,
`D_n(alpha_W nu_W) = alpha_W D_n nu_W`, so the v2 admissibility condition is
unchanged in content.

Adversarial case: 3-D `(8,4,4)` wall slab, genuinely normal-varying interior
driver, boundary-compatible, evaluated at every time with my own trace:

| `alpha_W` | `D_n psi` at t = 0, 0.25, 0.5 | interior `|v_n|` max | evolution drift |
|---|---|---|---|
| 1.0 | `0.0, 0.0, 0.0` | `0.0156` | `5.0e-5` |
| 1.5 | `0.0, 0.0, 0.0` | `0.0154` | `7.5e-5` |
| 0.4 | `0.0, 0.0, 0.0` | `0.0158` | `2.0e-5` |

The boundary trace is exactly zero at all times while the interior flow is
nontrivial, and the drift scales as `1 : 1.5 : 0.4` — exactly proportional to
`alpha_W`, confirming both preservation and genuine clock dependence.

**Gate-strictness probe.** Moving the gate from `nu_W` to `alpha_W nu_W` makes
it stricter for `alpha_W > 1` and looser for `alpha_W < 1`. I probed the
looser direction with a small nonzero boundary trace: at `alpha_W = 0.4` the
scaled driver trace is `1.28e-12` and the resulting propagated `D_n psi` is
`3.2e-13` — both scale by the same `alpha_W`, so the propagated-`psi` gate
remains a consistent backstop rather than being outrun. The relaxation is
therefore safe by construction, not by luck.

Spatially varying `wall_proper_time_rate` is impossible by construction
(`(nt,)` shape contract).

**F9: `PASS`.**

---

## 7. Background `gamma_w` firewall (F10)

`phase1f_b` still imports nothing from `timescape_fsigma8.background`, so no
automatic `alpha_W = 1/gamma_w` path exists structurally. The closure has no
`background_gamma_w` parameter, `lapse_driver_kind = BACKGROUND_TIMESCAPE_GAMMA_W`
is rejected, and the new clock provenance field rejects
`TIMESCAPE_PREDICTED_CLOCK_DRIVER`. The module docstring states explicitly that
`alpha_W` is never identified with `1/gamma_w`.
`BACKGROUND_WALL_LAPSE_TO_BOOST: NOT_DERIVABLE` and
`WALL_PROPER_TIME_RATE: REQUIRED_EXTERNAL_COMMON_SPACETIME_CLOCK_CLOSURE` both
stand.

**F10: `PASS`.**

---

## 8. `alpha_W` validation and consumption (F11)

| Probe | Result |
|---|---|
| `alpha_W` contains `0.0` | rejected — "must be positive" |
| contains `-1.0` | rejected — "must be positive" |
| contains `NaN` | rejected — "must contain only finite values" |
| contains `inf` | rejected — "must contain only finite values" |
| wrong length | rejected — "must match time_grid" |
| spatially varying `(nt, size)` | rejected — "must match time_grid" |
| provenance `TIMESCAPE_PREDICTED_CLOCK_DRIVER` | rejected |
| stale v2 role token | rejected |

**Consumption.** The v2 defect was "validated but unused". It cannot recur:
with a nonzero driver, changing `alpha_W` changes `psi` (§2A), and the value is
surfaced in diagnostics as `wall_proper_time_rate_min/max`. The repository test
`test_wall_proper_time_rate_is_load_bearing_not_metadata` asserts that doubling
the rate now breaks compatibility against an `alpha_W = 1` fixture.

**F11: `PASS`.**

---

## 9. Test oracles (F12)

| Test | Oracle class | Note |
|---|---|---|
| T1 `alpha = 1` | `INDEPENDENT_ANALYTIC_ORACLE` | closed-form quadratic; reproduces valid v2 behaviour |
| T2 `alpha = 2` | `INDEPENDENT_ANALYTIC_ORACLE` | `0.002 + 2(0.001t - 0.0002t^2)`; asserts separation from the unit-clock result |
| T3 `alpha = 0.5` | `INDEPENDENT_ANALYTIC_ORACLE` | same closed form |
| T4 `alpha(t) = 1 + t` | `INDEPENDENT_ANALYTIC_ORACLE` | driver kept linear so the analytic integral is exact; asserts the `5e-4` chain-rule term |
| T5 invalid / spatial / provenance | `INDEPENDENT_EVIDENCE` | contract gates |
| T6 `alpha = 1.5` boundary | `PARTIAL_EVIDENCE` | the `psi` comparison uses a hand trapezoid re-implementing the production rule; the boundary assertions are independent |
| zero-driver exception | `INDEPENDENT_EVIDENCE` | correct and correctly scoped |

I independently recomputed T1–T4's expected final amplitudes and confirmed the
reported solutions are genuinely non-identical. No clock test uses the
production integrator as its own oracle.

**F12: `PASS`.**

---

## 10. Strong-form trace limitation (F13)

The v3 report adds an explicit limitation paragraph to the interface-firewall
section: the gate is enforced through the *discrete strong-form* one-sided
boundary-normal trace, so continuum-Neumann-compatible profiles can still
exceed the declared tolerance at finite resolution; the v2 audit's smooth
cosine example with trace `0.00866` is cited; the rejection is classified as a
conservative fail-closed **numerical** restriction and explicitly not evidence
that the continuum profile violates the physical or model boundary condition.
The inventory records this machine-readably, including
`finite_resolution_limitation_is_physical_condition: false`.

Tolerances are unchanged (`boundary_normal_velocity_tolerance` and
`boundary_normal_acceleration_tolerance` both `2e-11`), and the boundary model
is unchanged. The limitation is documented, not promoted to a physical law.

**F13: `PASS`.**

---

## 11. Core regression (F14) and scientific status (F15, F16)

| Check | Result |
|---|---|
| R1 sign `D_a v^a = deltaTheta_d,w - deltaTheta_W` | my own div∘grad `-0.0320` vs code `L psi` `-0.0640`: same sign |
| R2 `D_w^2 = L_w/a_w^2` | ratio `0.5, 0.5, 0.5` for `a = 1, 2, 3` — `a`-independent |
| R3 no automatic background lapse | firewall intact (§7) |
| R4 no implicit zero initial boost | zero-driver `v_0 = 0.00824621125123532 = 0.002 sqrt(17)` |
| R5 no H1 density-interface promotion | `EXPLICIT_EXTERNAL_BOOST_BOUNDARY_CLOSURE`; `PHYSICAL_INTERFACE_CLAIM: NOT_GRANTED` |
| R6 transverse / harmonic | both `EXCLUDED_BY_EXPLICIT_SCALAR_MODEL_RESTRICTION`; harmonic zero `NOT_GRANTED` |
| R7 shear-free sector | `EXCLUDED_BY_EXPLICIT_SELECTED_GEOMETRIC_SECTOR`; shear zero `NOT_GRANTED` |

All twelve required status tokens are unchanged and no promotion occurred:
`IMPLEMENTED_CONDITIONALLY`, `PARTIAL_CLOSURE_NEW_GEOMETRIC_DYNAMICS_REQUIRED`,
`DUST_TO_WALL_BOOST_PROPAGATION: CONDITIONALLY_DERIVED`,
`DUST_TO_WALL_BOOST_FROM_Y_ALONE: NOT_DERIVED`,
`FULL_EXTERNAL_BOOST_HISTORY: NOT_REQUIRED_IN_SELECTED_REALIZATION`,
`WALL_GEOMETRY_DRIVER: REQUIRED_EXTERNAL_CLOSURE_INPUT`, and
`UNIQUE_TIMESCAPE_PREDICTION`, `PHYSICAL_INTERFACE_CLAIM`,
`OBSERVATIONAL_AUTHORIZATION`, `RSD_AUTHORIZATION`, `SIGMA8_AUTHORIZATION`,
`FSIGMA8_AUTHORIZATION` all `NOT_GRANTED`.

**State rank.** `FROZEN_DIFFERENTIAL_STATE_RANK: 4` and
`SELECTED_SCALAR_REALIZATION_DIFFERENTIAL_STATE_RANK: 5` are unchanged.
`alpha_W(t)` is an externally supplied closure function multiplying an
externally supplied driver; it is not integrated and adds no differential
degree of freedom. Rank 5 remains correct.

**F14 `PASS` · F15 `PASS` · F16 `PASS`.**

---

## 12. Tests, artifacts, history (F17)

| Stack | Targeted | Full | Failures | Skips | XFails | Warnings |
|---|---|---|---|---|---|---|
| Python 3.14.3 (numpy 2.5.2 / scipy 1.18.1) | **49 passed** | **588 passed** | 0 | 0 | 0 | 0 |
| Python 3.11.9 (numpy 2.4.6 / scipy 1.17.1) | **49 passed** | **588 passed** | 0 | 0 | 0 | 0 |

No suppression was used. The v3 validation artifact regenerates to
`30aba6abeb8f42adec771cfd26c4951bcf489b9d472a82bc6d56852a61812e71` on both
stacks — matching the value frozen in both the report and the inventory — and
the frozen Phase 1F-A artifact regenerates unchanged at
`ed3fcdc4aa544eaa7732a6923965b57c73ec7397200096b0e2ebc87b34f0be47`, so no
frozen phase regressed. Byte identity is recorded as reproducibility only, not
as scientific validation. Markdown and JSON agree on the artifact hash, the
counts (49 / 588 / 588), and every verdict token.

History is exactly linear with no merge commit:

```
87af7976b82b0b38e2c3e77dfc9458e664034c5d   main / origin/main
    |
27fd65fd2a05c5b990508d948703897f433b566e   v1  (tag d7840740…)
    |
16440e1a682c8d62d1e1b1d15fe8fad9290fa66a   v2  (tag bd1facf1…)
    |
d2f150222cb08565aa9d0822747250309d8aaa67   v3  (tag 61dc9cf7…)
```

Tags re-verified after the audit: unchanged. Nothing pushed; the remote carries
no 1F-B ref.

**F17: `PASS`.**

---

## A. FINAL V3 AUDIT VERDICT

```text
ACCEPT_V3
```

Every load-bearing clock check passes and no scientific regression was found.

## B. CLOCK-SEMANTICS ADJUDICATION

| Item | Verdict | Evidence |
| ---- | ------- | -------- |
| F1 alpha definition | `PASS` | `alpha_W = dtau_W/dt`, `(nt,)` shape, strictly positive, external provenance, load-bearing role, all fail-closed |
| F2 chain-rule scalar propagation | `PASS` | exactly one `alpha` formed once and used in update, `psi_dot`, and acceleration; matches my own `alpha`-trapezoid to `0.0` |
| F3 non-unit alpha dependence | `PASS` | `alpha = 1` vs `2` differ by `1.0e-3`; separated from unscaled (`1.0e-3`) and double-`alpha` (`2.0e-3`) alternatives |
| F4 zero-driver exception | `PASS` | `nu = 0`: `alpha = 1` and `7.3` bit-identical; scoped in code and tests, not generalized |
| F5 H_wall common-time semantics | `PASS` | `INVERSE_COMMON_TIME` contract plus runtime `ln(a[i+1]/a[i])/dt - H_bar` gate on the common-time grid |
| F6 no double H conversion | `PASS` | observed `R_A = 1.16e-09`; a double conversion would shift it by `7.05e-04` |
| F7 C_Theta clock-factor firewall | `PASS` | `alpha`-free path unchanged; `C_Theta ~ 5.6e-17` at `alpha = 1, 2, 0.5` |
| F8 R_A common-time consistency | `PASS` | common-time derivative, common-time `H`, one `alpha` on the source; classification not upgraded |
| F9 boundary preservation with alpha != 1 | `PASS` | `D_n psi = 0.0` at all times for `alpha = 1, 1.5, 0.4`; drift scales `1 : 1.5 : 0.4`; both gates scale together |
| F10 background gamma_w firewall | `PASS` | no `background` import; driver token and clock provenance both rejected |
| F11 alpha validation/provenance | `PASS` | eight adversarial probes all fail closed; value demonstrably consumed |
| F12 analytic test oracles | `PASS` | T1–T4 closed-form; T6 `PARTIAL_EVIDENCE` for its `psi` comparison |
| F13 strong-form trace limitation | `PASS` | documented, machine-readable, tolerance unchanged, not promoted |
| F14 core-v1/v2 regression | `PASS` | R1–R7 all hold |
| F15 scientific-status preservation | `PASS` | all twelve tokens unchanged |
| F16 state-rank preservation | `PASS` | 4 / 5 unchanged; `alpha_W` is a closure function, not a DOF |
| F17 history/tag integrity | `PASS` | linear, no merges, v1/v2 unchanged, v3 peels correctly, nothing pushed |

## C. BOUNDARY-PRESERVATION CHECK

Preserved exactly under a non-unit clock. `D_n psi|Gamma = 0.0` at every
evaluation time for `alpha_W = 1.0, 1.5, 0.4` with a genuinely normal-varying
interior driver and nontrivial interior normal flow (`|v_n| ~ 0.0155`). The
driver gate acts on `alpha_W Q_0 nu_W`, which for spatially homogeneous
`alpha_W > 0` is equivalent to the v2 condition `D_n nu_W|Gamma = 0`; the
propagated-`psi` gate scales identically, so the looser direction
(`alpha_W < 1`) is not a safety relaxation.

## D. CORE-REGRESSION CHECK

R1 sign, R2 `L_w/a_w^2`, R3 background-lapse firewall, R4 no implicit zero
boost, R5 no H1 interface promotion, R6 transverse/harmonic exclusion, R7
shear-free sector: all confirmed. No previously validated result was weakened.

## E. TEST / ARTIFACT EVIDENCE

49 targeted and 588 full on Python 3.14.3 and 3.11.9, zero failures, skips,
xfails, warnings. v3 artifact `30aba6ab…12e71` byte-identical on both stacks
and equal to the frozen value in report and inventory; Phase 1F-A artifact
unchanged at `ed3fcdc4…0be47`. Markdown/JSON agree on hash, counts, and tokens.

## F. HISTORY / TAG INTEGRITY

`87af7976 → 27fd65fd → 16440e1a → d2f15022`, linear, zero merge commits. v1
`d784074049…` → `27fd65fd…` and v2 `bd1facf1fce2…` → `16440e1a…` unchanged; v3
tag `61dc9cf76029…` peels to `d2f15022…`. `main` and `origin/main` remain at
`87af7976…`. Nothing pushed.

## G. REMAINING SCIENTIFIC LIMITATIONS

Non-blocking, none introduced by v3 except the first:

1. **Validator clock/boundary coverage gap.** The validation script's
   `normal_varying_scenario` has no `proper_time_rate` parameter, so the
   deterministic artifact's `normal_varying_boundary` study is `alpha_W = 1`
   only. Non-unit-clock boundary preservation is covered by the test suite
   (T6, `alpha_W = 1.5`) and by this audit, but is not recorded in the
   artifact. Nothing is misreported — the artifact does not claim otherwise —
   so this is a coverage observation, not a defect.
2. The `two_clock_propagation` artifact block records no `R_A` value per clock
   rate; the double-conversion evidence exists only in this audit.
3. Carried from v2: the discrete strong-form boundary trace can reject
   continuum-Neumann-compatible profiles at finite resolution (documented);
   `div(v_returned)` and the constrained `L psi/a^2` remain different discrete
   operators, consistent and `O(h^2)`, with no spatial refinement study; the
   missing perturbed wall/common-spacetime geometry, the transverse and
   harmonic vector sectors, and all observational quantities remain outside the
   phase as declared.

## H. INTEGRATION READINESS

```text
READY_FOR_STRICT_FAST_FORWARD_INTEGRATION: YES
```

## I. EXACT NEXT STEP

The next task is a strict fast-forward integration of `main` from

```text
87af7976b82b0b38e2c3e77dfc9458e664034c5d
```

to

```text
d2f150222cb08565aa9d0822747250309d8aaa67
```

integrating exactly the three Phase 1F-B commits — `27fd65fd…` (v1),
`16440e1a…` (v2), `d2f15022…` (v3) — with no merge commit, no rebase, and no
squash, and preserving the `phase-1f-b-dust-wall-boost-dynamics-v1`, `-v2`, and
`-v3` annotated tags unchanged. That integration was **not** performed in this
audit.
