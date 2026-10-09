# Phase 1G-H — remediation of the fourth independent delta audit

Classification: `FOURTH_DELTA_AUDIT_REMEDIATION_RECORD` (conditional,
model-internal, `NON_OBSERVATIONAL`). Date: 2026-10-09.
Fourth delta audit: [`phase1g_h_delta_audit_4.md`](phase1g_h_delta_audit_4.md)
and its inventory (audit commit `fc804a0f71f47904e86388f378295f72ba15cdd8`,
which the auditing session reports has the tree and parent of its local
commit `f332353`; audited commit `027b7a413fcee0786b861d5903272e4653d227ed`,
base `18bf2fb`). The auditor is OpenAI Codex, GPT-6 family: a different
model family from the author.
Companion: [`phase1g_h_delta_audit_4_remediation_inventory.json`](phase1g_h_delta_audit_4_remediation_inventory.json);
logs in [`phase1g_h_delta_audit_4_remediation_logs/`](phase1g_h_delta_audit_4_remediation_logs/).
Remediated records: [`phase1g_h_global_variance_closure.md`](phase1g_h_global_variance_closure.md)
(revised in place; the text the fourth delta audit read stays at `027b7a4`),
its inventory, the scope note of its validation record, an errata pointer
in [`phase1g_h_delta_audit_3_remediation.md`](phase1g_h_delta_audit_3_remediation.md)
and a block in its inventory, the addendum Sec. 6 of
[`phase1g_b_contract_hardening_successor.md`](phase1g_b_contract_hardening_successor.md)
and a block in its inventory, the fourth addendum (Sec. 10) of
[`phase1g_h_publication_successor.md`](phase1g_h_publication_successor.md)
and its inventory, README.md and CLAUDE.md. Tests:
`tests/test_phase1g_h_global_variance.py` and
`tests/test_phase1g_b_contract_hardening.py`. No package module and no
script changes.

## 0. Summary

- **Fourth delta-audit outcome.** `ACCEPT_WITH_CORRECTIONS`: PROVENANCE,
  GOVERNANCE, SCIENCE, NUMERICS, IMPLEMENTATION and TASK_COMPLIANCE
  `ACCEPT`; TESTS and DOCUMENTATION `ACCEPT_WITH_CORRECTIONS`. GH-D3F1 …
  GH-D3F5 resolved within their chosen scopes, GH-D3E1 … GH-D3E3 applied,
  no earlier finding regressed; every GH-D2F# finding now resolved within
  its scope. It reproduced 20 of 20 full-precision values (largest
  difference 6.05×10⁻¹⁰, within the budgets) and computed the centred
  both-walls covariances that confirm GH-D3F5. Three new findings (GH-D4F1
  LOW, tests; GH-D4F2 INFO and GH-D4F3 LOW, documentation) and four errata
  (GH-D4E1 … GH-D4E4). Readiness token:
  `NO_SCIENTIFIC_BLOCKER_PENDING_TEST_COVERAGE_DOCUMENTATION_WINDOWS_GATE_AND_OWNER_DECISIONS`.
- **Owner approval** (2026-10-09, verbatim «Procedi con il piano e
  l'opzione (a)») of the plan of Sec. 1, with option (a) for the 1G-B
  scalar-precision policy: keep the documented limit.
- **Result.** Every finding, erratum and recommendation in scope is
  addressed (Sec. 2). Whether they are resolved is for the owner or a
  further audit to judge.
- **Numbers.** No runtime or script changes, so every value is unchanged:
  the evidence artifact matches that of `6926a63` leaf by leaf on the same
  interpreter (3201 numeric leaves, no text leaf changed, figures
  byte-identical). The case runner reproduces 0.810772, 1.121363 and
  0.918157 with output files byte-identical to round 4.
- **Unchanged.** Status tokens, the five `NOT_GRANTED` authorisations,
  equations, runtime and evidence tolerances, every package module (also
  `global_variance.py` and `lagrangian_sigma.py`), every script, frozen
  records, tags, and the files of the five audits.
- **Commits** (local, on `ccr-555e67be-u11yht` on top of the fourth
  delta-audit commit `fc804a0`): `a243bf13bb27fb77c54ff05be004c47efe6e6784` (tests) and the commit that carries this
  record (documentation). Nothing is pushed: the push of `fc804a0` and these
  two commits needs a separate approval.

## 1. Plan approved

| Item | Choice | Why |
|---|---|---|
| **GH-D4F1** LOW, tests | One test requiring each record's own strict-JSON refusal for an equal `Fraction` in the seed quadrature of `EvaluatedVoidShare` and in the premise radius of `AdmissibleGlobalLinearInterval` | Kills the audit's mutants X02 and X04 without changing the runtime |
| **GH-D4F2** INFO and **GH-D4E1** | Report Sec. 11 names the five remediation records and the latest one | The count "two" was stale |
| **GH-D4F3** LOW and **GH-D4E3** | The 1G-B byte-equality is scoped: same HEAD `18bf2fb`, same platform, before and after the code change in the working tree; across commits only `provenance.repository_head` differs | The statement must not read as a committed-tree gate |
| **GH-D4E2** | "Tolerances" unchanged means runtime and evidence tolerances; the Simpson test thresholds were tightened | Narrower and exact |
| **GH-D4E4** | Only the relative change of `LCDMReferenceLinearSigma` is recomputed; the truncation envelope is bounded, not recomputed | Exact statement of the binding |
| **Mutant X11** (recommendation) | One-ULP tests of the native-float bindings of the two 1G-B records | Exact equality stays the policy, so it is now covered |
| **P15** (recommendation) | Recorded with P16 in the fourth addendum of the publication successor; the convention is clarified | Recorded once, in the next substantive addendum |
| **float32 policy** (owner decision) | Option (a): the documented limit stays; a uniform policy would need a separate successor | The audit found the disclosure sufficient for the current contract |

## 2. Finding-by-finding resolution

**GH-D4F1 (LOW) — two strict-JSON guards had no behavioural test.** New
test `test_gh_d4f1_seed_share_and_interval_exports_must_be_strict_json`:
`evaluate_void_share` with a seed quadrature whose `truncation_tolerance`
is an equal `Fraction`, and `dataclasses.replace` of an interval with a
premise radius whose `radius_Mpc` is an equal `Fraction`. Each must raise
the dedicated error whose message begins with that record's own name
("void share: …", "interval record: …"), so removing either guard fails the
test. Rerun of the audit's own mutants (Sec. 3): X02 and X04 are now
killed. X01 and X03 (the growth and premise guards) still survive. The
audit classified them as redundant: no distinct counterexample reaches
those exports.

**GH-D4F2 (INFO) and GH-D4E1 — stale count.** Report Sec. 11 now reads
"the five remediation records (remediated trees; the latest,
`phase1g_h_delta_audit_4_remediation.md`, covers the current tree)". The
italic note of report Sec. 8, which says "the two remediation records", is
dated to the delta audit of 2026-10-08 and is left as written.

**GH-D4F3 (LOW) and GH-D4E3 — scope of the 1G-B byte-equality.** Correct
reading of "The 1G-B validation artifact is byte-identical before and after
its successor" (third remediation record, Secs. 0 and 3) and of successor
Sec. 4: the SHA-256 `5746cc76…c13c8d` was obtained twice at the unchanged
HEAD `18bf2fb`, on the same platform, before and after the code change in
the working tree. Artifacts generated at different committed heads differ
only in `provenance.repository_head`. The audit reconstructed `5746cc76…`
from both by restoring that provenance, and the scientific content is
identical. Applied in successor Sec. 6, its inventory, CLAUDE.md and the
errata pointer of the third remediation record.

**GH-D4E2 — "tolerances" in the third remediation record, Sec. 0.**
Correct reading: runtime and evidence tolerances are unchanged. The
Simpson test thresholds were deliberately tightened from 10⁻² to 2×10⁻³
and 5×10⁻³, as that record's Sec. 2 states. This record states the
narrower scope in Sec. 0.

**GH-D4E4 — "LCDMReferenceLinearSigma refuses non-finite, negative,
unbound or out-of-tolerance quadrature diagnostics" (third remediation
record, Sec. 2).** Correct reading: both diagnostics must be finite,
non-negative and within the declared tolerances. Only
`quadrature_relative_change` is bound to a recomputation, from the two
stored unit sigmas. `truncation_envelope_fraction` is not re-integrated
from the spectrum, so another value within its budget (for example 0) is
accepted. Successor Sec. 6 also states that `omega_m`,
`growth_today_photon_normalised` and `omega_m_R_cubed_Mpc3` are checked
for their domain only.

**Recommendation — exactness to one ULP (mutant X11).** The 1G-B test
file gains four cases (22 in all): `growth_ratio`, `early_spectrum_factor`
and `reference_offset_from_anchor`, and the LCDM relative change, each
refused one ULP above and one ULP below the factory value. X11 (a
relative tolerance of 10⁻¹²) is now killed. X08 and X12 (comparison after
`float()`) still survive: they are stricter than the chosen policy, not
weaker.

**Owner decision — scalar precision of the 1G-B records.** Option (a): the
limit of successor Sec. 3 stays as documented. Native floats are compared
exactly. A `numpy.float32` rounding of the exact value passes and is stored
as `float32`, so that record's own export is not strict JSON. 1G-H does not
import these two classes, and its own records refuse such nested exports.

**Recommendation — P15.** Recorded in the fourth addendum (Sec. 10) of the
publication successor, with P16 (the fourth delta audit on
`phase-1g-h-delta-audit-4`). Sec. 10.3 states the convention as already
applied: summaries name the last recorded push of the session branch (now
P15, `36d127f..027b7a4`), not the latest event of every kind.

**Recommendations on H-OD1 … H-OD5.** Recorded, not acted on. The audit
recommends a formal proposal with convention (c) and comparison (a), no
reference value, no token change, the experimental status until the
Windows gate, and separate decisions on pull request, merge, freeze and
tag. These are the report's own recommendations; the decisions remain the
owner's.

## 3. Validation of the remediated tree

Environment: Linux, CPython 3.13.16 (NumPy 2.5.3, SciPy 1.18.1, matplotlib
3.11.2, pytest 9.1.1) and CPython 3.11.17 (NumPy 2.4.6, SciPy 1.17.1,
matplotlib 3.11.2, pytest 9.1.1); the upstream clone at the pinned commit,
git-ignored and not edited; the git-ignored inputs regenerated in the
previous round still present.

| Check | Tree | Result |
|---|---|---|
| Full suite, CPython 3.13.16, `-W error` | `a243bf1` (tests) | 1212 collected: **1212 passed, 0 skipped, 0 failed** (364 s) |
| Full suite, CPython 3.11.17, `-W error` | same | 1212 collected: **1212 passed, 0 skipped, 0 failed** (361 s) |
| `tests/test_phase1g_h_global_variance.py`, `tests/test_phase1g_b_contract_hardening.py` | same | 54 and 22 passed on both interpreters |
| Evidence script, 3.13.16 with figures, 3.11.17 `--no-figures` | `a243bf1`, `src`/`scripts`/`tests` clean | 36 / 36 gates each; 3201 numeric leaves identical across interpreters; 3.13 artifact SHA-256 `942723389409d1e5f04a4a80fea84be2c6f1d2501b4218fc56faa2e844de9624` (one exact run and environment, including the git head; not a cross-platform gate) |
| Regression against the evidence of `6926a63` (CPython 3.13.16) | — | 3201 numeric leaves bitwise equal; no text leaf changed; no leaf added or removed; figure hashes identical |
| Case runner, three configurations | `a243bf1` | 0.810772, 1.121363, 0.918157; output files byte-identical to round 4 |
| The fourth delta audit's 13 mutants (`own_definitions.json`), scratch copies | `a243bf1` | X02, X04 and X11 now killed; X05, X06, X07 and the adapted D1 killed; X01 and X03 survive (redundant guards), X08 and X12 survive (stricter than the chosen policy), X09 and X10 survive (test-threshold loosening), as the audit classified them |
| Round-4 mutants rerun (`round4_mutant_definitions.json`) | `a243bf1` | as in round 4: B01, B02, B03, B07 … B10, J01 … J03, L01 … L05 killed; B04, B05 (test-threshold loosening) and B06 (inside the 1e-9 calibration budget) survive |
| `scripts/audit_numerical_tolerances.py` | `a243bf1` | 750 comparisons (unchanged: the new tests compare exactly), 0 without explicit tolerances |
| `scripts/validate_phase1f_c_r_astra_remediation.py` | final bytes of this commit | `PASS`; 59 JSON round trips (the earlier 57, the fourth audit's inventory and this record's) |
| `git diff --check` | final bytes | clean |

- **Command:** `OPENBLAS_NUM_THREADS=1 python -B -W error -m pytest -q -p no:cacheprovider -rs`.
- **Counts.** 1212 = 1207 of round 4 + 1 in the 1G-H file + 4 in the 1G-B
  file. 0 skips: the git-ignored inputs regenerated in round 4 are still
  present in this container.
- **Mutation baseline.** As in round 4, one 1G-B owner-decisions test fails
  in each scratch copy because a copy is not a git repository. A mutant
  counts as killed only when another test also fails
  (`*_effective.json`); the test passes in the repository.
- **Order.** The suites, the evidence, the case runner and the mutation
  runs used the tests commit `a243bf1`, and the mutation bases were checked
  against its bytes. This record's documentation was written meanwhile.
  Both full suites were then rerun on the final bytes of this
  documentation (all but this sentence and the two logs it names): 1212
  passed, 0 skipped, 0 failed on each (351 s and 352 s;
  `full_suite_final_py3*.log`).
- **Logs** (`phase1g_h_delta_audit_4_remediation_logs/`): full-suite,
  evidence and validator logs with their heads, the cross-interpreter and
  regression comparisons (and `compare_evidence.py`), the tolerance audit,
  the mutant runner, the two mutant sets with results, logs and the
  effective classification.
- **Not run:** the Windows 3.14.3 / 3.11.9 gate.

## 4. Open items

- **Push** of `fc804a0` and the two commits of this remediation (needs a
  separate approval; the publication successor will then record it).
- **Windows gate** (CPython 3.14.3 / 3.11.9), never run on a 1G-H tree.
- **Owner decisions H-OD1 … H-OD5** (report §9): pull request, merge,
  freeze and tag are separate decisions.
- **A uniform scalar-precision policy for 1G-B records**, if ever wanted:
  a separate successor.
- **C** (prediction, observation): not reached.
