# Phase 1G-H — remediation of the independent delta audit

Classification: `DELTA_AUDIT_REMEDIATION_RECORD` (conditional, model-internal,
`NON_OBSERVATIONAL`). Date: 2026-10-08.
Delta audit: [`phase1g_h_delta_audit.md`](phase1g_h_delta_audit.md) and its
inventory (delta-audit commit `5c325e1fd05b343f6d5e93f931038794de4373a2`,
audited commit `89cb041f901b51a3f90fa6831aab1b4553c1772c`; the auditor is
named in the audit's header).
Companion: [`phase1g_h_delta_audit_remediation_inventory.json`](phase1g_h_delta_audit_remediation_inventory.json);
logs in [`phase1g_h_delta_audit_remediation_logs/`](phase1g_h_delta_audit_remediation_logs/).
Remediated records: [`phase1g_h_global_variance_closure.md`](phase1g_h_global_variance_closure.md)
(revised in place; the text the delta audit read stays at `89cb041`), its
inventory, the scope note of its validation record, a dated status note in
the first remediation record and its inventory, README.md and CLAUDE.md.
New: [`phase1g_h_publication_successor.md`](phase1g_h_publication_successor.md)
and its inventory.

## 0. Summary

- **Delta-audit outcome.** `REJECT` (SCIENCE) for the claim that the
  nonnegative pairs share the wall-density covariance and for completeness
  claims; PROVENANCE and NUMERICS `ACCEPT`; the other areas
  `ACCEPT_WITH_CORRECTIONS`. Of GH-F1 … GH-F15: 6 resolved, 2 resolved by
  owner decision, 6 partially resolved (GH-F4 … GH-F9), 1 open (GH-F15). Six
  new findings: GH-DF1 (MEDIUM-HIGH), GH-DF2 and GH-DF3 (MEDIUM), GH-DF4 and
  GH-DF5 (LOW-MEDIUM), GH-DF6 (LOW), all of class `CORRECTION`; six
  remediation errata GH-DE1 … GH-DE6; four claims `VERIFIED_WITH_DEVIATION`
  (the radial quadrature of a small moment). All 22 original errata were
  found applied.
- **Owner approval** (2026-10-08, verbatim «Perfetto, procedi») of the plan of
  Sec. 1. No owner decision was needed.
- **Result.** Each new finding and erratum is addressed (Sec. 2), which
  completes the six partial findings. GH-F15 is confirmed by the owner and
  recorded (publication successor, P4).
- **Numbers.** Outside the constructive pairs of [1G-H] Sec. 6.3 every
  evidence value is bitwise unchanged. Inside, the radial correction moves
  the small signed law-II wall moments by 1.3×10⁻³ / 6.6×10⁻⁴ relative and
  any published rms by at most 6.4×10⁻⁴ (σ_wall of the signed law II; totals
  at most 5.1×10⁻⁵); no value printed in the report changes. One range was
  corrected in self-review: the integrated scale dependence of the [W09]
  seed is −0.08% to −0.12% over conventions (a)–(c) and both scenarios (the
  text said −0.09%).
- **Unchanged.** Status tokens, the five `NOT_GRANTED` authorisations,
  frozen records, tags, the files of both audits and every package module
  other than `global_variance.py`.
- **Commits** (local, on `ccr-555e67be-u11yht` on top of the delta-audit
  commit `5c325e1`): `248a06bfeb655337bc499607180c49008b5f34ea` (code, tests,
  evidence script) and the commit that carries this record (documentation).
  Nothing is pushed.

## 1. Plan approved

| Finding | Choice | Why |
|---|---|---|
| **GH-DF1** | Narrow the shared constraint to the latent carrier law (the audit's first option); report the law-II normaliser and the conditional-density covariance ratio; add identity (H25) | (H25) shows that P11(r) and the both-walls conditional correlation C_W(r) fix the total, so laws that also fixed C_W could not differ; the meaningful statement is the narrowed one |
| **GH-DF2** | Bind every record to its inputs by recomputation (the audit's first option) | Transparent and fail-closed: a record whose inputs do not reproduce its results is refused, whatever its origin; the cost is one extra evaluation per construction |
| **GH-DF3 … DF6** | The audit's suggested corrections | — |

## 2. Finding-by-finding resolution

**GH-DF1 (MEDIUM-HIGH) — nonnegative laws and the declared covariance.**
*Resolved.* The 2026-10-07 text listed "the unconditional wall-density
covariance exp(λ² ξ_s) − 1" among the constraints shared by laws I and II.
That covariance belongs to the unconditionally normalised carrier
`e^a/E[e^a]`. The wall density actually used is normalised on the walls,
`ψ = e^a/E[e^a | wall]`, and in law II its normaliser is larger by
`m_II = Q(c − κ0)/f_w`, so its unconditional covariance is law I's divided
by m_II². Changes:

- The shared constraints are now f_v0, P11(r), the latent carrier law and
  the convention `E[ψ | wall] = 1`, in the report (§1, §6.3), the inventory,
  the evidence metadata (`shared_constraints`, `not_shared`,
  `free_construction_choices`), README and CLAUDE.
- The evidence reports m_II = 2.869 / 2.140 / 1.623 ([GM], r_s = 1 / 2 /
  4 Mpc) and 2.474 / 2.104 / 1.669 ([NW15]), the covariance ratios 1/m_II²
  (0.121–0.379) and the unmasked ball variance of the conditionally
  normalised law-II density (0.085 for [GM] at 1 Mpc against 0.701). These
  reproduce the delta audit's values to 10⁻⁶ relative.
- Identity (H25), new in §6.1: `1 + ξ_δ(r) = P11(r) C_W(r)/f_w²` for empty
  voids, with `C_W(r) = E[ψ1 ψ2 | both points in walls]`. The evidence
  checks it against the (H18) assembly for every law (≤ 2.2×10⁻¹⁶, gate
  10⁻¹²) and reports the pair-weighted ⟨C_W − 1⟩. For the signed pair it is
  0.756 / 0.043 ([GM], I / II); for the lognormal pairs 0.725–0.841 (law I)
  and 0.698–1.278 (law II). The ordering of the totals follows ⟨C_W − 1⟩,
  as (H25) requires.
- The reading is narrowed: the pairs show non-uniqueness at fixed f_v0,
  P11 and carrier law, not at a fixed conditionally normalised density
  covariance. At fixed P11 and C_W the variance is unique.
- r_s and the λ calibration are stated as free choices of the
  construction. Disclosed development history: on 2026-10-07 a first
  lognormal design with λ calibrated on the unsmoothed carrier (latent
  point variance ≈ 20.8, ball integrals not resolved near r = 0) was
  discarded before publication. The report now states why the carrier is
  smoothed.
- Tests: `test_gh_df1_lognormal_laws_share_the_carrier_not_the_conditional_density`
  samples the 4-variate laws (2×10⁶ draws each) and checks the shared
  carrier covariance, the m_II⁻² ratio and (H25).
  `test_gh_df1_lognormal_laws_report_the_law_ii_normaliser` checks the
  reported m_II. `test_gh_df1_law_summary_satisfies_h25_and_includes_the_first_radial_panel`
  checks the (H18)–(H25) agreement and the ball quadrature.

**GH-DF2 (MEDIUM) — records bound to their inputs.** *Resolved.*

- `TwoPhaseGlobalGrowth` now stores G, and `EvaluatedVoidShare` stores its
  density, early spectrum and seed quadrature.
- On construction every public record recomputes each result and
  diagnostic from its stored inputs, with the same pure function its
  factory uses (`_two_phase_growth_values`, `_void_share_values`,
  `_global_sigma_values`, `_interval_values`). It refuses any mismatch
  beyond `RECORD_IDENTITY_RTOL` and any input that makes the computation
  fail.
- The sigma record requires its void share to be evaluated with its own
  density and spectrum objects, and re-resolves its radius from the
  specification.
- The growth assumptions, the sigma caveats and the interval class
  assumptions are bound to the module's.
- The targeted invariants of GH-F9 still run first, with their own
  messages.
- Tests: the audit's five accepted replacements are refused (A_s ×4,
  radius ×2, quadrature 33/17, seed radius ×2, premise rms 999), and so are
  a void share with another spectrum, zeroed growth diagnostics, foreign
  assumptions and caveats, and a radius relabelled with another length at
  the same `radius_Mpc`. Unchanged copies of genuine records are accepted.
- Construction costs about twice the computation (the phase tests take
  13–15 s instead of 7 s).
- Evidence values are bitwise unchanged.

**GH-DF3 (MEDIUM) — current self-audit.** *Resolved.* §8 of the report now
states the current readings, with its preface rewritten:

- the post-hoc factor is an empirical normalisation at fixed closure and
  reclosure is a distinct variant (GH-DE2);
- law II changes the masked wall auto-variance, with a positive integrated
  cross term, not double counting (GH-DE5);
- the flat-wall cap needs wall-density freedom but does not select the
  whole of S1 (GH-DE3).

The first remediation record's "14 findings are resolved" is superseded by
a dated status note giving the delta audit's verified outcomes, in the
record and its inventory, without rewriting either.

**GH-DF4 (LOW-MEDIUM) — integrated versus pointwise.** *Resolved.* §5.2 and
§5.3 name `G_eff/G(0) − 1` an integrated, spectrum- and window-weighted
average at the target radius. They state that it is no pointwise bound on
`G(k)/G(0) − 1` and does not bound the premise integral, and they withdraw
the interval-placement accuracy (GH-DE4).

**GH-DF5 (LOW-MEDIUM) — defensive tests.** *Resolved.* New tests:

- the growth record's background check;
- the interval's `target_inside`;
- the Fréchet and symmetry refusals of the orthant integrals, with a
  monkeypatched quadrature returning impossible values;
- the output half unit of the GH-F11 budget, now a function of the evidence
  script (`e_reference_rounding_budget`), with a boundary case;
- the reclosure factor (the evidence helper, constant share against PBS).

The tamper test now requires each invariant's own message.

Mutation testing, in a scratch copy outside the tree:

- The delta audit's 23 mutants, M7 adapted as in the audit and N13's target
  moved to the new function: 21 are killed by the 42 phase tests. N5 (the
  centre split with intact edges, benign as the audit found) and N9 (a
  docstring sign) survive, as classified.
- Ten new mutants are all killed: the GH-DF2 binding, the spectrum
  identity, the radius re-resolution, the moment symmetry, the lognormal
  normaliser, the first radial panel, and N1, N4, N8 and N13 again.

**GH-DF6 (LOW) — median qualifier.** *Resolved.* README and CLAUDE put "below
the adopted ε = 1 threshold, with no controlled error estimate" beside the
median-seed values, with "heuristic seed-scale prior" and the [W09] "formal
extrapolation".

**Remediation errata.** Applied as follows:

- GH-DE1: report §6.3, shared constraints;
- GH-DE2: §8, normalisation;
- GH-DE3: §8, S1;
- GH-DE4: §5.2;
- GH-DE5: §8, mechanism;
- GH-DE6: dated status note in the first remediation record.

**Radial quadrature (the four `VERIFIED_WITH_DEVIATION` claims).**
*Resolved.*

- The ball pair integrals omitted the first panel `[0, 2R/480]`, because
  zero separation means unit mask correlation, outside the orthant domain.
  The integrand vanishes there (the pair density has a double zero), so the
  panel is now included without evaluating the kernels at r = 0.
- The grid has 1440 intervals, with a refinement gate against every other
  node (`radial_refinement_rel` = 10⁻⁵, declared before its first
  evaluation; observed 8.3×10⁻⁷ / 1.0×10⁻⁶).
- The signed law-II wall moments are now 7.82523×10⁻⁴ and 3.55318×10⁻³,
  the delta audit's values. The pair density integrates to 1 to 10⁻¹²
  (0.99999993 before).

**Partial original findings.** GH-F4 is completed through GH-DF4, GH-F5
through GH-DF1, GH-F6 through GH-DF3/DE2, GH-F7 through GH-DF3/DE3, GH-F8
through GH-DF6, and GH-F9 through GH-DF2 and GH-DF5. Whether they are now
resolved is for a further independent audit to decide.

**GH-F15.** Confirmed by the owner on 2026-10-08 («Si, confermo») in the
session that wrote the phase, not directly to an auditor; recorded in the
publication successor (P4), which also records the push of 2026-10-08 (P5)
and the delta audit's publication (P6).

## 3. Validation of the remediated tree

Environment as in the earlier records: Linux, CPython 3.13.16 (NumPy 2.5.3,
SciPy 1.18.1, matplotlib 3.11.2, pytest 9.1.1) and CPython 3.11.17 (NumPy
2.4.6, SciPy 1.17.1, matplotlib 3.11.2, pytest 9.1.1); the upstream clone at
the pinned commit, git-ignored and not edited.

| Check | Tree | Result |
|---|---|---|
| Full suite, CPython 3.13.16, `-W error` | this commit's tree | 1178 collected: **1146 passed, 32 skipped, 0 failed** (339 s) |
| Full suite, CPython 3.11.17, `-W error` | same | 1178 collected: **1146 passed, 32 skipped, 0 failed** (335 s) |
| `tests/test_phase1g_h_global_variance.py` | same | 42 passed |
| Evidence script, 3.13.16 with figures, 3.11.17 `--no-figures` | `248a06b`, `src`/`scripts`/`tests` clean | 36 / 36 gates each; 3201 numeric leaves identical (largest difference 0); 3.13 artifact SHA-256 `91aaca79ad0d0d86ad3208c8cd854e9d03839ef1f8c2d0026ff7a5cf8ff89884` (one exact run and environment, not a cross-platform gate) |
| Regression against the evidence of `89cb041` (same interpreter) | — | every common leaf outside `two_phase_covariance/*/gaussian_threshold_pair` bitwise identical; inside it, 130 leaves changed (the radial panel and the narrowed constraint texts), 6 renamed, 108 added |
| Case runner, three configurations | `248a06b` | 0.810772, 1.121363, 0.918157 (unchanged) |
| Mutation testing (scratch copy) | `248a06b` | delta audit's 23 mutants: 21 killed, N5 and N9 survive as classified; 10 new mutants: 10 killed |
| `scripts/audit_numerical_tolerances.py` | this commit's tree | 739 comparisons, 0 without explicit tolerances |
| `scripts/validate_phase1f_c_r_astra_remediation.py` | final bytes of this commit | `PASS`; 52 JSON round trips (the earlier 50 plus this record's inventory and the publication successor's) |
| `git diff --check` | final bytes | clean |

- **Command:** `OPENBLAS_NUM_THREADS=1 python -B -W error -m pytest -q -p no:cacheprovider -rs`.
- **Counts.** 1178 = 1136 earlier tests + 42 in the 1G-H file (35 before).
  The 32 skips have the causes recorded before: upstream oracle not
  extracted (18), clean and barotropic oracles (4 + 4), the owner-decisions
  artifact (3), and the 1D-B, 1D-D and B2 artifacts (1 each). The delta
  audit regenerated these inputs in its own environment and reached 0 skips
  on the remediated tree; that was not repeated here.
- **Order.** The suites ran on this commit's tree before the last edit of
  this section and of the inventory's verification fields. The validator,
  the JSON checks and the whitespace check were rerun on the final bytes.
  No test reads those texts.
- **Logs:** `phase1g_h_delta_audit_remediation_logs/`: evidence and
  full-suite logs, the evidence head, the mutation results.
- **Not run:** the Windows 3.14.3 / 3.11.9 gate; the upstream notebook and
  oracle regeneration; the 20-minute owner-decisions Monte Carlo.

## 4. Open items

- **Push** of the two commits of this remediation (needs a separate
  approval).
- **A further independent audit** of this remediation before any merge or
  freeze (the delta audit's verdict is not reversed by the author).
- **Owner decisions H-OD1 … H-OD5** (report §9; the delta audit's
  recommendations agree with the revised ones).
- **Windows gate** (CPython 3.14.3 / 3.11.9; commands in the validation
  record).
- **C** (prediction, observation): not reached; the constructive pairs are
  kinematic constructions, not dynamics.
