# Phase 1G-H — remediation of the third independent delta audit

Classification: `THIRD_DELTA_AUDIT_REMEDIATION_RECORD` (conditional,
model-internal, `NON_OBSERVATIONAL`). Date: 2026-10-09.
Third delta audit: [`phase1g_h_delta_audit_3.md`](phase1g_h_delta_audit_3.md)
and its inventory (audit commit `18bf2fbef880fdfb3c292956aa1f000720930abf`,
blind checkpoint `4d71bd4fe918ef8a0b71c178a7180c4d291294b0`, both re-hashed
from the auditing session's `d9342c4` and `c62ad87`; audited commit
`ed0ec0c9c8783519a53759a265b6ce37e6c0e607`). The auditor is OpenAI Codex,
GPT-6 family: a different model family from the author.
Companion: [`phase1g_h_delta_audit_3_remediation_inventory.json`](phase1g_h_delta_audit_3_remediation_inventory.json);
logs in [`phase1g_h_delta_audit_3_remediation_logs/`](phase1g_h_delta_audit_3_remediation_logs/).
Remediated records: [`phase1g_h_global_variance_closure.md`](phase1g_h_global_variance_closure.md)
(revised in place; the text the third delta audit read stays at `ed0ec0c`),
its inventory, the scope note of its validation record, a one-line errata
pointer in the third remediation record
([`phase1g_h_delta_audit_2_remediation.md`](phase1g_h_delta_audit_2_remediation.md))
and a block in its inventory, the
second addendum (Sec. 8) of
[`phase1g_h_publication_successor.md`](phase1g_h_publication_successor.md)
and its inventory, README.md and CLAUDE.md. New: the 1G-B successor
[`phase1g_b_contract_hardening_successor.md`](phase1g_b_contract_hardening_successor.md)
and its inventory. Code: `global_variance.py`, the evidence script (one key
and its wording) and the phase tests; in a separate commit,
`lagrangian_sigma.py` and `tests/test_phase1g_b_contract_hardening.py`.

## 0. Summary

- **Third delta-audit outcome.** `ACCEPT_WITH_CORRECTIONS`: PROVENANCE,
  SCIENCE, NUMERICS and TASK_COMPLIANCE `ACCEPT`; GOVERNANCE,
  IMPLEMENTATION, TESTS and DOCUMENTATION `ACCEPT_WITH_CORRECTIONS`. Its
  blind cross-family reconstruction of report §6 and of the main
  conditional values is `CROSS_FAMILY_VERIFIED_WITH_DEVIATION`: 58 of 58
  quantities verified, largest absolute difference 6.1×10⁻¹⁰; the deviation
  is the auditor's own initial recipe, which it disclosed and corrected.
  GH-D2F2, D2F3, D2F5 and D2F6 resolved, GH-D2F1 and D2F4 partly resolved,
  GH-D2E1 and D2E2 applied; no earlier finding regressed. Five new findings
  (GH-D3F1 … GH-D3F5: one LOW-MEDIUM, three LOW, one INFO) and three errata
  (GH-D3E1 … GH-D3E3). Readiness token:
  `NO_SCIENTIFIC_BLOCKER_PENDING_CONTRACT_TEST_P11_CORRECTIONS_WINDOWS_GATE_AND_OWNER_DECISIONS`.
- **Owner approval** (2026-10-09, verbatim «Perfetto, procedi») of the plan
  of Sec. 1, with option (a) for the owner decision GH-D3F4.
- **Result.** Every finding and erratum is addressed (Sec. 2). Whether they
  are resolved is for the owner or a further audit to judge.
- **Numbers.** Every numeric leaf of the evidence artifact is bitwise
  identical to that of `9ad5425` on the same interpreter: 3185 numeric leaves
  under unchanged keys, and the 16 renamed
  `both_walls_product_moment_excess_ball` leaves. Two text leaves change
  (the `not_shared` wording) and the figures are byte-identical. The case
  runner reproduces 0.810772, 1.121363 and 0.918157 with output files
  byte-identical to round 3. The 1G-B validation artifact is byte-identical
  before and after its successor.
- **Unchanged.** Status tokens, the five `NOT_GRANTED` authorisations,
  equations, tolerances, frozen records, tags, the files of the four audits,
  and every package module other than `global_variance.py` and, under its
  own successor, `lagrangian_sigma.py`.
- **Commits** (local, on `ccr-555e67be-u11yht` on top of the third
  delta-audit commit `18bf2fb`): `c6028e9046934ef6de234f0b58fbe18e6f3bead1` (1G-H code, tests,
  evidence script), `6926a636c100d232247e39d71d5b2d6e71a6f917` (1G-B
  contract hardening and its tests) and the commit that carries this
  record (documentation). Nothing is pushed: the push of `4d71bd4`,
  `18bf2fb` and these three commits needs a separate approval.

## 1. Plan approved

| Finding | Choice | Why |
|---|---|---|
| **GH-D3F1** LOW | Events P11–P13 in a second addendum (Sec. 8) of the publication successor; current summaries name the last recorded publication event and point there, instead of stating the remote head | The audit's convention: a later push no longer makes a summary false, and no commit has to record its own push |
| **GH-D3F2** LOW | Every 1G-H record refuses construction unless its export, nested 1G-B inputs included, is strict JSON; `lagrangian_sigma.py` is not normalised for this | Fail-closed in the module that makes the promise; no change to frozen numerics |
| **GH-D3F3** LOW | The tests the audit lists, a literal binding-tolerance bound and a pinned `RECORD_IDENTITY_RTOL`; independent Monte Carlo normaliser and conservative-budget wording; tighter Simpson tolerances | Kills B01, B02, B03 and B10 |
| **GH-D3F4** LOW-MEDIUM, owner decision | Option (a): a separate 1G-B contract-hardening successor | Closes the gap before promotion; outputs bit-identical |
| **GH-D3F5** INFO | Wording; the key `both_walls_conditional_density_covariance_ball` becomes `both_walls_product_moment_excess_ball` | The value is a product-moment excess, not a centred covariance |
| **GH-D3E1 … E3** | E1, E2 here and in a one-line pointer; E3 in the `_same` docstring | The audit's advice: one chronological record instead of more layered notes |

## 2. Finding-by-finding resolution

**GH-D3F1 (LOW) — P11 left current summaries stale.** The publication
successor gains Sec. 8 (2026-10-09): P11, the fast-forward `4bf2718 →
ed0ec0c` («Sì, pubblica anche ed0ec0c»); P12, the owner's direct
confirmation of P10 and P11 to the third auditor («Confermo le
autorizzazioni P10 e P11», as that audit records it); P13, the third
delta audit on `phase-1g-h-delta-audit-3` at `18bf2fb`, whose authorising
words are not available in this session. Sec. 8.3 states the convention:
README.md, CLAUDE.md, the report header and the 1G-H inventory now name the
last recorded publication event (P11, `4bf2718..ed0ec0c`, 2026-10-09) and
point to the record. The remote refs were re-verified read-only
(`ccr-555e67be-u11yht` = `ed0ec0c`, `phase-1g-h-delta-audit-3` = `18bf2fb`,
`main` = `8d3cdd0`, 76 tag refs).

**GH-D3F2 (LOW) — strict JSON was not transitive.** A helper
`_require_strict_json` runs `json.dumps(export, allow_nan=False)` at the end
of `__post_init__` of all nine serialisable 1G-H records
(`LastScatteringMatching`, `TwoPhaseGrowthChecks`, `TwoPhaseGlobalGrowth`,
`ConstantVoidShare`, `GaussianThresholdSeedVoidShare`, `EvaluatedVoidShare`,
`ConditionalGlobalLinearSigma`, `HomogeneityPremise`,
`AdmissibleGlobalLinearInterval`) and refuses the record with
"the export is not strict JSON". All twelve nested counterexamples of the
audit (ten quadrature representations, a `Fraction` density and a
`Fraction` radius) are now refused. The audit's probe script, rerun
unchanged, finds no accepted 1G-H record whose export is not strict JSON
(Sec. 3); a test covers three of the counterexamples. A `Fraction` in a
nested field that 1G-H does not export (the density's `G` and identity
tolerance) is still accepted, since the export stays strict JSON. The check
costs about 0.1 ms per record. The module docstring and report §10 state exactly this guarantee.
The 1G-B records' own exports are unchanged (their successor, Sec. 2 below,
does not normalise scalars).

**GH-D3F3 (LOW) — test gaps.** Four tests and one assertion:

| Test | Checks | Kills |
|---|---|---|
| `test_gh_d3f3_every_growth_check_and_g_are_stored_as_floats` | all five `TwoPhaseGrowthChecks` tolerances and `G` given as `Fraction` are stored as `float`, equal values, strict JSON | B10 |
| `test_gh_d3f3_float_results_accept_float64_and_subclasses_but_not_float32` | `numpy.float64` and a `float` subclass accepted for a result; `numpy.float32(0.5)`, exact in single precision, refused by the type policy | B02, B03 |
| `test_gh_d3f3_binding_tolerance_boundary_with_a_literal_rtol` | a relative change of 1.05×10⁻¹² refused, 0.95×10⁻¹² accepted, without reading the module constant | B01 |
| `test_gh_d3f2_nested_inputs_must_export_as_strict_json` | nested `Fraction`, `float32` and `int64` quadrature inputs refused; genuine records export strict JSON | J01, J02 |
| `test_gh_d2f2_evidence_thresholds_are_pinned` (extended) | `RECORD_IDENTITY_RTOL == 1e-12` | B01 |

The Monte Carlo test now normalises ψ with the first point of each draw
only, so the normaliser's samples are independent; its docstring calls the
budget what it is, a conservative one (five times the sum of the
independent-sample standard errors, no credit for correlation). The
Simpson test's tolerances are tightened from 10⁻² to 2×10⁻³ (exact error)
and 5×10⁻³ (ratio 15.96), still far above the 10⁻⁴ round-off.

**GH-D3F4 (LOW-MEDIUM, owner decision) — frozen 1G-B records.** Option (a):
[`phase1g_b_contract_hardening_successor.md`](phase1g_b_contract_hardening_successor.md).
`LCDMReferenceLinearSigma` refuses non-finite, negative, unbound or
out-of-tolerance quadrature diagnostics; `AnchoredLagrangianSigmaRatio`
binds its ratios, the anchor offset and the list of differing early-spectrum
inputs to its stored records. The 1G-B validation artifact is byte-identical
before and after; 18 new tests; mutants L01–L05 killed. The audit's probes
confirm it: every non-finite diagnostic and both factor-999 probes are
refused, and nothing is newly accepted. Scalars are still stored as given,
and NumPy compares a `float32` rounding of an exact ratio with it in single
precision, so that rounding passes (successor Sec. 3, limits): the binding
holds to the precision of the stored scalar type.

**GH-D3F5 (INFO) — C_W − 1 is not a centred covariance.** Report §6.3 and the
evidence script now call ⟨C_W − 1⟩ the excess of the both-walls product
moment over the one-wall normalisation and say that the centred both-walls
covariance subtracts E[ψ1 | both] E[ψ2 | both], which differs from 1 in
law II. The exported key is renamed to `both_walls_product_moment_excess_ball`
(the script's docstring records the former name); the value is unchanged.

**Errata.**

- **GH-D3E1** (`phase1g_h_delta_audit_2_remediation.md` §1, "Fail-closed, and strict JSON
  holds by construction"). Correct reading at `ed0ec0c`: the named 1G-H
  float results were typed and the module's own scalar inputs converted,
  but nested 1G-B inputs could still carry non-JSON scalars. Since this
  remediation the statement holds through the strict-JSON check (GH-D3F2).
- **GH-D3E2** (same record §2, "The 1G-B records the runtime imports already
  store floats and are unchanged."). Correct reading: they are unchanged, but
  they validate scalars as `numbers.Real` without converting them, so not
  every field stores a native float.
- **GH-D3E3** (`_same` docstring). Corrected: refusing an equal `int` is the
  typed-output policy; an `int` is valid JSON, a `Fraction` is not.

A one-line pointer in `phase1g_h_delta_audit_2_remediation.md` (after its dated note)
and a block in its inventory lead here.

## 3. Validation of the remediated tree

Environment: Linux, CPython 3.13.16 (NumPy 2.5.3, SciPy 1.18.1, matplotlib
3.11.2, pytest 9.1.1) and CPython 3.11.17 (NumPy 2.4.6, SciPy 1.17.1,
matplotlib 3.11.2, pytest 9.1.1); the upstream clone at the pinned commit,
git-ignored and not edited; nbformat, nbclient and ipykernel installed for
the oracle regeneration.

| Check | Tree | Result |
|---|---|---|
| Full suite, CPython 3.13.16, `-W error` | `6926a63` (code) | 1207 collected: **1207 passed, 0 skipped, 0 failed** (338 s) |
| Full suite, CPython 3.11.17, `-W error` | same | 1207 collected: **1207 passed, 0 skipped, 0 failed** (337 s) |
| `tests/test_phase1g_h_global_variance.py`, `tests/test_phase1g_b_contract_hardening.py` | same | 53 and 18 passed on both interpreters |
| Evidence script, 3.13.16 with figures, 3.11.17 `--no-figures` | `6926a63`, `src`/`scripts`/`tests` clean | 36 / 36 gates each; 3201 numeric leaves identical across interpreters (largest difference 0); 3.13 artifact SHA-256 `027b8e124488f2f6bffa71c2082dfb73da60083435cca207a3f0f546ae1a34a2` (one exact run and environment, not a cross-platform gate) |
| Regression against the evidence of `9ad5425` (CPython 3.13.16) | — | 3185 numeric leaves under unchanged keys bitwise equal; 16 leaves renamed (`both_walls_conditional_density_covariance_ball` → `both_walls_product_moment_excess_ball`), values bitwise equal; 2 text leaves changed (the `not_shared` wording); figure hashes identical |
| Case runner, three configurations | `6926a63` | 0.810772, 1.121363, 0.918157; output files byte-identical to round 3 |
| `scripts/validate_phase1g_b_lagrangian_sigma.py`, before and after the 1G-B change | `18bf2fb`, then the change | artifact byte-identical (SHA-256 `5746cc76…c13c8d`), every gate passing |
| The third delta audit's scalar probes (its script, unchanged), CPython 3.13.16 | `ed0ec0c`, then `6926a63` | 1446 probes; accepted 456 → 416, none newly accepted; accepted exports that are not strict JSON 129 → 98, in 1G-H records 12 → 0 (the rest are 1G-B records); accepted non-finite values 8 → 0; all 12 nested counterexamples and both factor-999 probes refused |
| Mutation testing, round 4 (scratch copies, `run_mutants_r4.py`) | `6926a63` | the audit's B01–B10: B01, B02, B03, B07, B08, B09, B10 killed; B04, B05 (test-tolerance loosening) and B06 (inside the 1e-9 calibration budget) survive, as the audit classified them; J01–J03 (strict JSON) and L01–L05 (1G-B) killed |
| Mutation testing, the second delta audit's campaign rerun | `6926a63` | as in round 3: the delta audit's 23: 21 killed, N5 and N9 survive as classified; the author's 10: 9 killed, D1 killed in its adapted form; the second delta audit's 23: 22 killed, A02 survives (benign); R01–R04 killed |
| `scripts/audit_numerical_tolerances.py` | `6926a63` | 750 comparisons (one more than round 3: the `pytest.approx` of the 1G-B decomposition test), 0 without explicit tolerances |
| `scripts/validate_phase1f_c_r_astra_remediation.py` | final bytes of this commit | `PASS`; 57 JSON round trips (the earlier 54, the third audit's inventory, the 1G-B successor's and this record's) |
| `git diff --check` | final bytes | clean |

- **Command:** `OPENBLAS_NUM_THREADS=1 python -B -W error -m pytest -q -p no:cacheprovider -rs`.
- **Counts.** 1207 = 1136 earlier tests + 53 in the 1G-H file (49 before)
  + 18 in the new 1G-B file. **0 skips**: the git-ignored inputs whose
  absence skipped 32 tests in round 3 were regenerated with the project's
  scripts: the upstream notebook and its three oracles, the 1D-B growth
  and B2 artifacts, the owner-decisions Monte Carlo (898 s, 124 / 124
  gates), and the 1D-D artifact (731 s, in a clean worktree at `18bf2fb`,
  since its validator needs a clean descendant of the 1D-D commit). No
  tracked file changed; the upstream clone was only read.
- **Order.** The suites, the evidence, the case runner and the mutation runs
  used the code commits. The working-tree diff of `src`, `scripts` and
  `tests` had the same hash at the start of the campaign and at the commits,
  so the mutation bases match them. The documentation was written meanwhile.
  Both full suites were then rerun on the final bytes of this
  documentation (all but this sentence and the two logs it names): 1207
  passed, 0 skipped, 0 failed on each (333 s and 332 s;
  `full_suite_final_py3*.log`).
- **Mutation baseline.** In the scratch copies one 1G-B owner-decisions test
  fails because a copy is not a git repository (it reads a certified blob
  with git); it passes in the repository. Every mutant counted as killed
  also fails at least one other test (`round4_kills_beyond_baseline.json`).
- **Logs** (`phase1g_h_delta_audit_3_remediation_logs/`): full-suite,
  evidence and validator logs with their heads, the cross-interpreter and
  regression comparisons (and `compare_evidence.py`), the tolerance audit,
  the round-4 mutant definitions, runner, log and results, the rerun of the
  second delta audit's campaign and of the adapted D1 mutant, the 1G-B
  validation logs before and after, the scalar-probe comparison, and the
  input-regeneration scripts and logs (scratch paths abbreviated).
- **Not run:** the Windows 3.14.3 / 3.11.9 gate.

## 4. Open items

- **Push** of `4d71bd4`, `18bf2fb` and the three commits of this
  remediation (needs a separate approval; the publication successor will
  then record it as P14).
- **Windows gate** (CPython 3.14.3 / 3.11.9), never run on a 1G-H tree.
- **Owner decisions H-OD1 … H-OD5** (report §9): pull request, merge,
  freeze and tag are separate decisions.
- **C** (prediction, observation): not reached.
