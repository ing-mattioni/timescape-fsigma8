# Phase 1G-H — remediation of the second independent delta audit

Classification: `SECOND_DELTA_AUDIT_REMEDIATION_RECORD` (conditional,
model-internal, `NON_OBSERVATIONAL`). Date: 2026-10-08.
Second delta audit: [`phase1g_h_delta_audit_2.md`](phase1g_h_delta_audit_2.md)
and its inventory (audit commit `e5170285e1d4b4aa72e907a3a79110d05584c0d9`,
blind checkpoint `64116509554cc0d711660da4d81ad95c3f450a6d`, audited commit
`226e52d2e4157d0130b2a9dfaffd71834c6017d9`; the auditor is named in the
audit's header and shares the author's model family).
Companion: [`phase1g_h_delta_audit_2_remediation_inventory.json`](phase1g_h_delta_audit_2_remediation_inventory.json);
logs in [`phase1g_h_delta_audit_2_remediation_logs/`](phase1g_h_delta_audit_2_remediation_logs/).
Remediated records: [`phase1g_h_global_variance_closure.md`](phase1g_h_global_variance_closure.md)
(revised in place; the text the second delta audit read stays at `226e52d`),
its inventory, the scope note of its validation record, dated notes in both
earlier remediation records and their inventories, a dated addendum
(Sec. 6) of [`phase1g_h_publication_successor.md`](phase1g_h_publication_successor.md)
and its inventory, README.md and CLAUDE.md. Code: `global_variance.py`, the
phase tests, and a gate label and docstrings of the evidence script.

## 0. Summary

- **Second delta-audit outcome.** `ACCEPT_WITH_CORRECTIONS`: PROVENANCE,
  SCIENCE, NUMERICS, IMPLEMENTATION and TASK_COMPLIANCE `ACCEPT`;
  GOVERNANCE, TESTS and DOCUMENTATION `ACCEPT_WITH_CORRECTIONS`. GH-DF1 …
  GH-DF6 resolved, GH-DE1 … GH-DE5 applied, GH-DE6 applied in an equivalent
  form; GH-F1 and GH-F2 resolved by owner decision, GH-F3 … GH-F14 resolved,
  GH-F15 `RESOLVED_OWNER_CONFIRMED`. Six new findings: GH-D2F1 and GH-D2F2
  (LOW), GH-D2F3 … GH-D2F6 (INFO); two errata of the second remediation,
  GH-D2E1 and GH-D2E2. Readiness token:
  `NO_SCIENTIFIC_BLOCKER_READY_FOR_OWNER_DECISION_AFTER_LOW_CORRECTIONS_P7_RECORD_AND_WINDOWS_GATE`.
- **Owner approval** (2026-10-08, verbatim «Perfetto, procedi») of the plan of
  Sec. 1. No owner decision was needed.
- **Result.** Every finding and erratum is addressed (Sec. 2): the
  publication events P7–P9 are recorded; seven tests are added and kill the
  mutants that survived the audit; a float result must be stored as a
  float; the wording is corrected. Whether the findings are resolved is for
  the owner or a further audit to judge.
- **Numbers.** Every numeric leaf of the evidence artifact is bitwise
  identical to that of `248a06b` on the same interpreter (3197 numeric
  leaves); the two (H25) gate entries move from the `physics` to the
  `numerics` block with the same values, and the figures are
  byte-identical. The case runner reproduces 0.810772, 1.121363 and
  0.918157. No value printed in any report changes.
- **Unchanged.** Status tokens, the five `NOT_GRANTED` authorisations,
  equations, tolerances, frozen records, tags, the files of the three
  audits and every package module other than `global_variance.py`.
- **Commits** (local, on `ccr-555e67be-u11yht` on top of the second
  delta-audit commit `e517028`): `9ad54253c4ec40cede5690da6659be28e0bd0a2d`
  (code, tests, evidence script) and the commit that carries this record
  (documentation). Nothing is pushed: the push of `6411650`, `e517028` and
  these two commits needs a separate approval.

## 1. Plan approved

| Finding | Choice | Why |
|---|---|---|
| **GH-D2F1** | An additive dated section of the publication successor (the audit's second option) with P7, P8 and P9; its current-reading table extended to every statement the finding lists; the current summaries (phase report §9, its inventory, README, CLAUDE) updated in place, the dated records annotated | One publication record; no historical byte rewritten |
| **GH-D2F2** | The audit's suggested tests, a test that pins every gate threshold, and the (H25) gate described as what it is | Each surviving mutant gets a test that kills it |
| **GH-D2F4** | Require a float wherever the recomputation gives a float (the audit's second option); store `G` and the growth checks as floats (its first option) | Fail-closed, and strict JSON holds by construction |
| **GH-D2F3, F5, F6; GH-D2E1, E2** | The audit's corrections (F6 is optional and applied) | — |

## 2. Finding-by-finding resolution

**GH-D2F1 (LOW) — the push P7 is unrecorded.** The publication successor
gains Sec. 6, dated 2026-10-08:

- **P7**, the fast-forward `89cb041 → 226e52d` carrying `5c325e1`, `248a06b`
  and `226e52d`, authorised with «Fai push e prepara il prompt per un nuovo
  audit»;
- **P8**, the owner's direct confirmation to the second delta auditor, «Confermo
  le due approvazioni di push registrate (GH-F15)», as that audit records it;
- **P9**, the second delta audit on `ccr-ac582de6-vho99i` at `e517028`,
  published on the owner's instruction in the auditing session, quoted as
  it appears in the transcript the owner pasted into this session.

The remote refs were re-verified read-only (`ccr-555e67be-u11yht` =
`226e52d`, `ccr-ac582de6-vho99i` = `e517028`, `main` = `8d3cdd0`, 76 tag
refs; pull requests #1–#4 closed, none from a 1G-H branch; no release). The
current-reading table now lists every statement of GH-D2F1. The second
remediation record and its inventory keep their text and gain a dated note;
the phase report §9, its inventory's publication block, README and CLAUDE
are current summaries and are updated in place.

**GH-D2F2 (LOW) — weakly protected quantities and gates.** Seven tests in
`tests/test_phase1g_h_global_variance.py`; the last column names the
mutants each one kills (A: survivors of the second delta audit's campaign;
R: this round's own mutants; Sec. 3 gives the whole campaign):

| Test | What it checks | Mutants |
|---|---|---|
| `test_gh_d2f2_law_summary_reports_the_pair_weighted_both_walls_covariance` | synthetic kernels with a strongly varying P11; ⟨C_W − 1⟩ = ∫P11 (C_W − 1)/∫P11 with C_W formed pointwise from its definition; the variance from (H25) | A18 |
| `test_gh_d2f2_lognormal_pairs_report_the_inverse_square_of_the_law_ii_normaliser` | `lognormal_pairs` on a synthetic spectrum at nine separations; m_II re-derived from λ and the one-point mask–carrier covariance; 1/m_II², carrier/m_II² and 1/m_II − 1 | A20 |
| `test_gh_d2f2_conditional_wall_density_by_sample_normalised_monte_carlo` | 2×10⁶ draws of `(g1, g2, s1, s2)` per law; ψ normalised by the *sample* wall mean; m_II, C_W(r) and the m_II⁻² covariance within 5σ, the normaliser's own error included | the audit's remark that the m⁻² ratio held by construction |
| `test_gh_d2f2_ball_half_resolution_estimate_has_the_simpson_error_ratio` | the pair density is a quintic with unit integral, so Simpson's error is exactly (h⁴/180)·45/R⁴ (9.30×10⁻¹³ at R = 10 Mpc) and 16 times that on the half grid; for a kernel with a 0.3 Mpc scale the error ratio is 15.96 against an adaptive-quadrature reference | A15, A16 |
| `test_gh_d2f2_binding_boundary_and_record_identities` | a change of 2×`RECORD_IDENTITY_RTOL` in `void_volume_response_rms`, which only the binding checks, is refused and a quarter of it accepted; the interval's `class_assumptions`; a density built on an equal copy of the background, which reproduces every value, is refused by the identity check alone | A01, A07, A09 |
| `test_gh_d2f2_evidence_thresholds_are_pinned` | the 15 gate thresholds, the radial grid (1440) and the orthant controls | A22, A23 |
| `test_gh_d2f4_float_results_must_be_floats_and_scalar_inputs_are_stored_as_floats` | GH-D2F4, below | R01–R04 |

The (H25) gate compares two sums of the same kernel arrays. It is now
described (evidence script, report §6.1 and §11) as a consistency check of
the (H18) assembly at x = 0, and it moves from the `physics` to the
`numerics` gate block; the kernels are checked by the Monte Carlo tests.

**GH-D2F3 (INFO) — the regression statement.** Erratum GH-D2E1, below.

**GH-D2F4 (INFO) — a `Fraction` passed the binding.** `_same` now requires
a finite `float` wherever the recomputation gives a float (`numpy.float64`
is a `float`), and `_bind_recomputed` names the field and its type
("sigma record: linear_sigma must be a float, not Fraction"); an integer
inside the diagnostics tuple is refused as a difference.
`TwoPhaseGlobalGrowth.G` and the five `TwoPhaseGrowthChecks` tolerances are
stored as floats; the other input records already were. `Decimal` was and
is refused as not a real scalar. The 1G-B records the runtime imports
already store floats and are unchanged.

**GH-D2F5 (INFO) — historical wording.** The first remediation record's
dated note gains the GH-DF1 narrowing and says that its inventory's
`files_changed_sha256` describe the bytes of `89cb041`; its inventory gains
a dated block, and the 1G-H inventory's `revision` block is marked
historical.

**GH-D2F6 (INFO, optional) — the missing input.** Report §6.3 now says
that, in the latent-Gaussian constructions of that section, the missing
input is the mask–carrier dependence (κ0, κ(r)): once it is specified,
f_v0, P11(r) and the carrier law fix C_W(r) and the variance, and law I
(the E3 case) fixes them with no further input. The qualifier is added
because for general laws the dependence is a joint law, not two
covariances.

**Errata of the second remediation.**

- **GH-D2E1** is applied by a dated note in the second remediation record
  and its inventory. Recount with the same artifacts (the evidence of
  `c1b4482`, the code of `89cb041`, against that of `248a06b`, CPython
  3.13.16, every leaf except the run environment and the figure list):
  outside the pairs, 3517 common leaves, every physical one bitwise
  identical; three gate read-outs changed (at most 1.15×10⁻⁵ absolute) and
  16 leaves were added. Inside `gaussian_threshold_pair`, of 204 common
  leaves 156 numeric ones changed (140 by more than 10⁻¹² relative) and 4
  texts; 6 were renamed (`ball_variance_unmasked_density` →
  `ball_variance_unconditionally_normalised_carrier`) and 106 exist only in
  the new artifact (those 6 and 100 new ones). The auditor's numbers are
  confirmed.
- **GH-D2E2** is applied by the same note and by the publication
  successor's Sec. 6.

**GH-F15.** `RESOLVED_OWNER_CONFIRMED`; recorded as P8.

**Minor.** "It takes about 80 s" becomes "about 50–80 s" (the second delta
audit measured 53 s and 46 s).

## 3. Validation of the remediated tree

Environment as in the earlier records: Linux, CPython 3.13.16 (NumPy 2.5.3,
SciPy 1.18.1, matplotlib 3.11.2, pytest 9.1.1) and CPython 3.11.17 (NumPy
2.4.6, SciPy 1.17.1, matplotlib 3.11.2, pytest 9.1.1); the upstream clone at
the pinned commit, git-ignored and not edited.

| Check | Tree | Result |
|---|---|---|
| Full suite, CPython 3.13.16, `-W error` | `9ad5425` (code) | 1185 collected: **1153 passed, 32 skipped, 0 failed** (281 s) |
| Full suite, CPython 3.11.17, `-W error` | same | 1185 collected: **1153 passed, 32 skipped, 0 failed** (281 s) |
| `tests/test_phase1g_h_global_variance.py` | same | 49 passed on both interpreters |
| Evidence script, 3.13.16 with figures, 3.11.17 `--no-figures` | `9ad5425`, `src`/`scripts`/`tests` clean | 36 / 36 gates each; 3201 numeric leaves identical across interpreters (largest difference 0); 3.13 artifact SHA-256 `357a7035cedabf17a63437d72e348fcdee2ad9e529c4c50f4e2e95a7926b44c2` (one exact run and environment, not a cross-platform gate) |
| Regression against the evidence of `248a06b` (CPython 3.13.16) | — | every leaf but the run environment compared: 3197 numeric and every text leaf equal; 6 leaves moved (the two (H25) gate entries, `physics` → `numerics`, same values); none added or removed otherwise; figure hashes identical |
| Recount of GH-D2E1 (`c1b4482`, the code of `89cb041`, against `248a06b`) | — | the auditor's counts confirmed (Sec. 2) |
| Case runner, three configurations | `9ad5425` | 0.810772, 1.121363, 0.918157; output files identical to the round-2 ones |
| Mutation testing (scratch copies; the second delta audit's script with A01 adapted and R01–R04 added) | `9ad5425` | delta audit's 23 mutants: 21 killed, N5 and N9 survive as classified; the author's 10: 9 killed, D1 (target string changed) killed after adaptation; the second delta audit's 23: 22 killed, A02 survives (benign, as that audit classified it); R01–R04: 4 killed |
| `scripts/audit_numerical_tolerances.py` | `9ad5425` | 749 comparisons, 0 without explicit tolerances |
| `scripts/validate_phase1f_c_r_astra_remediation.py` | final bytes of this commit | `PASS`; 54 JSON round trips (the earlier 53 plus this record's inventory) |
| `git diff --check` | final bytes | clean |

- **Command:** `OPENBLAS_NUM_THREADS=1 python -B -W error -m pytest -q -p no:cacheprovider -rs`.
- **Counts.** 1185 = 1136 earlier tests + 49 in the 1G-H file (42 before).
  The 32 skips have the causes recorded before (inputs not generated in
  this container: the upstream, clean and barotropic oracles, the
  owner-decisions artifact and the 1D-B, 1D-D and B2 artifacts). The second
  delta audit regenerated these inputs and reached 0 skips on `226e52d`;
  that was not repeated here.
- **Order.** The suites, the evidence and the mutation runs used the code
  commit `9ad5425` (the mutation base was checked to be byte-identical to
  it) while this record's documentation was being written; no test reads
  those texts. The validator, the JSON checks and the whitespace check were
  rerun on the final bytes.
- **Logs** (`phase1g_h_delta_audit_2_remediation_logs/`): evidence and
  full-suite logs, the evidence head, the tolerance audit, the mutation
  definitions, log and results (with the scripts that built and ran them),
  the regression comparison against `248a06b` and the GH-D2E1 recount with
  its script.
- **Not run:** the Windows 3.14.3 / 3.11.9 gate; the upstream notebook and
  oracle regeneration; the 20-minute owner-decisions Monte Carlo.

## 4. Open items

- **Push** of `6411650`, `e517028` and the two commits of this remediation
  (needs a separate approval; the publication successor would then record
  it).
- **Windows gate** (CPython 3.14.3 / 3.11.9), never run on a 1G-H tree.
- **A cross-family check** of report §6, optional: the second delta audit
  shares the author's model family.
- **Owner decisions H-OD1 … H-OD5** (report §9): pull request, merge,
  freeze and tag are separate decisions.
- **C** (prediction, observation): not reached.
