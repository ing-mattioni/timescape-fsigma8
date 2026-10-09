# Phase 1G-H — fourth independent delta audit

**Classification:** `INDEPENDENT_DELTA_AUDIT`

**Date:** 2026-10-09

**Auditor:** OpenAI Codex, GPT-6 family; the exact deployed variant/version is not exposed. This is a different model family from the Claude author. No author contact or author-conversation access occurred. The root and governance roles were not blind. The science role calculated the new centred diagnostics before reading author output values, and retained both its initial recipe error and the separately identified correction.

**Base:** `18bf2fbef880fdfb3c292956aa1f000720930abf`, tree `b191b76c9976d21aad82bf9ff6d133af5a822bf2`.

**Audited head:** `027b7a413fcee0786b861d5903272e4653d227ed`, tree `4431f10aa7269e67466dab4859ab20f4beac4059`.

**Environment:** Linux 6.18.44 / glibc 2.39; CPython 3.13.16 with NumPy 2.5.3 / SciPy 1.18.1, and CPython 3.11.17 with NumPy 2.4.6 / SciPy 1.17.1; matplotlib 3.11.2 / pytest 9.1.1. `OPENBLAS_NUM_THREADS=1`; acceptance runs use `-B -W error`. Windows owner gate: **NOT RUN**.

## 0. Summary

**Overall: `ACCEPT_WITH_CORRECTIONS`. No scientific or current implementation blocker was found.** All five third-delta findings are `RESOLVED` within their expressly chosen scopes, and all three errata are `APPLIED`. No earlier scoped finding regresses. The three new findings comprise two LOW and one INFO: defensive test coverage and documentation need corrections.

This report-only audit adds its own new report, inventory and evidence and makes local commits. It performs no push, PR, merge, tag, freeze, release, existing-file edit, author contact or authorization promotion.

| Area | Verdict |
|---|---|
| PROVENANCE | ACCEPT |
| GOVERNANCE | ACCEPT |
| SCIENCE | ACCEPT |
| NUMERICS | ACCEPT |
| IMPLEMENTATION | ACCEPT |
| TASK_COMPLIANCE | ACCEPT |
| TESTS | ACCEPT_WITH_CORRECTIONS |
| DOCUMENTATION | ACCEPT_WITH_CORRECTIONS |
| overall | ACCEPT_WITH_CORRECTIONS |

Merge/freeze readiness: **`NO_SCIENTIFIC_BLOCKER_PENDING_TEST_COVERAGE_DOCUMENTATION_WINDOWS_GATE_AND_OWNER_DECISIONS`**. This token is not approval to merge, freeze or publish. The mandatory Windows gate and owner decisions remain open.

The ordinary Jupyter execution pathway was blocked by host socket permissions. Execution of the original cells in fresh processes is a disclosed infrastructure deviation. Scientific values reproduce. Raw 1G-B artifacts generated at different committed HEADs differ solely because their metadata identifies those HEADs; the historical byte-equivalence claim needs that provenance qualification.

## 1. Object and hashes

The graph is exactly `18bf2fb → c6028e9 → 6926a63 → 36d127f → 027b7a4`. Every declared tree and single parent is confirmed. The delta contains **54 paths: 13 modified and 41 added**, including exactly **36** log/evidence files; no unexpected file changed.

Authenticated connector reads reconstructed the exact Git SHA-1 objects after a native private clone lacked credentials. The commission fixes the immutable audited head, and the timestamped remote snapshot agrees with it. The companion inventory retains the full source and artifact hash ledgers.

## 2. Method

Independent area roles read all mandatory reports, inventories, the full relevant diff and all 36 logs, as the commission permits. The optional previous prompt was absent; repository records supplied the continuity. The root auditor owns synthesis and final adjudication.

Verification combines immutable Git-blob comparisons, fresh executions on the specified sources, independent leaf-by-leaf comparisons, disposable mutant copies outside the audited tree, and independent EH98, tracker and Plackett/Gaussian calculations. No altered runtime copy is committed. No upstream scientific source is copied into the redistribution artifacts.

Notebook and three-oracle regeneration used the unchanged original runners through an external adapter that starts a fresh Python process. Both TCP and IPC kernel startup failed before any scientific cell ran. The adapter executes each original cell verbatim and retains stream-output parsing. Source hashes and numerical outputs are checked. This does not establish that the ordinary `nbclient` fresh-kernel protocol worked. An upstream plotting warning is retained and documented, rather than suppressed; the initial infrastructure failures remain in the evidence.

## 3. Provenance and governance

Blob comparison establishes that **241** previous-audit files are unchanged against `18bf2fb`; **56** other pre-existing package files and **111** frozen 1G report paths are unchanged against `8d3cdd0`. The base `lagrangian_sigma.py` is identical to frozen main, and this successor changes only two post-init validators. The runner, three configurations, scientific status module, uppercase constants and all five `NOT_GRANTED` authorizations remain unchanged.

All **12** required current file-hash declarations and **56** third-audit hashes match. All **57** existing top-level report JSON files parse with unique keys and finite JSON numbers. All **36** new logs were read and checked; scratch paths are appropriately abbreviated.

Fresh read-only GitHub queries return these heads: `main` at `8d3cdd0`, the session branch at `027b7a4`, the third-audit branch at `18bf2fb`, the second-audit branch at `e517028`, the original-audit branch at `816dd00`, and the first-delta branch at `5c325e1`. The **38** annotated tag objects exactly match the prior snapshot; native local peeling gives **76** logical ref-plus-peeled entries. The 1G-B v1 tag still targets `fb5d95245bc0cb19ce6cd1438177f1a597bb232f`. There are four closed and merged PRs, none from 1G-H; no release and no forbidden D-v2 reference exists.

| Event | Independently verified facts | Authorization limitation |
|---|---|---|
| P11 | Exactly one commit in `4bf2718..ed0ec0c` | Historical quote and prior audit; not reconfirmed here |
| P12 | The third report records direct confirmation of P10/P11 | Not repeated in this handoff |
| P13 | `ed0ec0c→4d71bd4→18bf2fb`; 57 added third-audit paths; checkpoint tree `6d5e848…` | Private historical approval is not recoverable here |
| P14 | Two audit and three remediation commits in `ed0ec0c..36d127f` | Distinct reported approval |
| P15 | One documentation commit in `36d127f..027b7a4`; current ref observed | Separate approval reported; event awaits the next addendum |

The current handoff says only “Eccolo” and directly confirms none of the cited historical approvals. Earlier directly confirmed statuses are retained. Current refs and ancestry do not establish a historical push's actor, time or immediately preceding remote value. This evidence limit is not proof of unauthorized publication.

The last-recorded-event convention is sound. Current summaries accurately identify P14, while publication successor §9.2 explicitly describes the historical state after P14. Its later-local-commit sentence is legitimate within that dated scope. Record P15 once in the next authorized substantive addendum, superseding `state_after_p14` and its companion. No endless chain of self-recording push commits is necessary.

The 1G-B successor follows the GB-OD precedent: a separate owner-approved scope, code commit, record and invariant tests, with unchanged historical tags. A tag attests its own immutable commit, not every later descendant. Main retains the old constructor behavior until a separately authorized merge; successor §5 already places the change on the H session branch.

AGENTS rules 1–10 hold for the reviewed delta: no scientific-model change, copied unlicensed source, auditor remote write, silent runtime threshold change or introduced warning suppression. Runtime and evidence numerical budgets are unchanged. The Simpson **test** acceptance thresholds were deliberately tightened and are explicitly documented.

## 4. Third-delta findings and errata

| ID | Outcome | Reason |
|---|---|---|
| GH-D3F1 | RESOLVED | P11-P14 successor and last-recorded-event convention correctly scope dated states; P15 is a disclosed next-addendum item. |
| GH-D3F2 | RESOLVED | All nine serializable H records check the final export after normalization/binding; 12 nested witnesses refused and zero H non-strict exports in 1446 probes. |
| GH-D3F3 | RESOLVED | B01/B02/B03/B10 genuinely killed; one-point Monte Carlo normalizer and conservative wording correct; literal boundary passes both interpreters. New coverage gap separately GH-D4F1. |
| GH-D3F4 | RESOLVED | Chosen successor scope implemented: finite/nonnegative/capped diagnostics, relative-change binding, four anchored ratios and exact difference list; old nonfinite and factor999 witnesses refused. Disclosed scalar-precision and factory-only limits retained. |
| GH-D3F5 | RESOLVED | Product excess terminology, active-key rename and explicit historical annotation correct; independent centred calculations prove law-II distinction. |

| Erratum | Outcome | Reading |
|---|---|---|
| GH-D3E1 | APPLIED | Historical non-transitive JSON guarantee corrected in chronological successor and linked from old record/inventory. |
| GH-D3E2 | APPLIED | Historical 1G-B Real-valued input storage accurately described as unconverted. |
| GH-D3E3 | APPLIED | Updated _same docstring separates typed-float policy, JSON-valid integer, and JSON-invalid Fraction. |

The remediation says “addressed,” leaving independent resolution to the auditor. That distinction is accurate. Resolution of the specified B01/B02/B03/B10 gaps does not establish exhaustive coverage of future changes; GH-D4F1 identifies a new gap. The chosen 1G-B successor scope does not promise full factory replay or universal native-float storage.

## 5. Earlier findings: regression review

GH-F1/F2 retain `RESOLVED_BY_OWNER_DECISION`; GH-F3…F14 retain `RESOLVED`; GH-F15 retains `RESOLVED_OWNER_CONFIRMED`. GH-DF1…DF6 remain `RESOLVED`.

All six GH-D2 findings are now `RESOLVED` within their original scopes. The publication and transitive-JSON residuals have been removed, while earlier counts, terminology, identifiability results and specifically requested mutation checks remain correct. No earlier scoped finding is reversed. The new summary-count and hash-scope corrections do not conceal any loss of scientific closure status.

## 6. Reduced scientific control

For `δ = Wψ/f_w − 1` and `E[ψ | wall] = 1`, H25 states `1 + ξδ(r) = P11(r) C_W(r)/f_w²`, with `C_W = E[ψ1ψ2 | both walls]`. This is a conditional product moment. The pair-weighted excess averages `C_W−1`. A pair-weighted pointwise centred covariance subtracts `m1(r)m2(r)` before averaging. A fully ball-conditioned covariance subtracts the product of the ball-conditioned means after averaging. Those two centring operations can also differ when the means depend on separation.

Independent reconstructed diagnostics for `r_s = 1 Mpc` follow. These are conditional numerical results, not claims of physical precision.

| Scenario / carrier / law | Product excess | Pair-weighted pointwise covariance | Fully ball-centred covariance |
|---|---:|---:|---:|
| PAPER_REFERENCE / signed / I_independent | 0.755929586089 | 0.755929586089 | 0.755929586089 |
| PAPER_REFERENCE / signed / II_same_field | 0.043189407474 | 0.009755655881 | 0.009952291969 |
| PAPER_REFERENCE / lognormal / I_independent | 0.786920193781 | 0.786920193781 | 0.786920193781 |
| PAPER_REFERENCE / lognormal / II_same_field | 0.837693200838 | 0.506596604464 | 0.517361458556 |
| NW15_CMB_FIT / signed / I_independent | 0.791264148143 | 0.791264148143 | 0.791264148143 |
| NW15_CMB_FIT / signed / II_same_field | 0.069083112915 | 0.022517882191 | 0.022861322284 |
| NW15_CMB_FIT / lognormal / I_independent | 0.840794361798 | 0.840794361798 | 0.840794361798 |
| NW15_CMB_FIT / lognormal / II_same_field | 0.697655401753 | 0.444041205240 | 0.450299183376 |

In law I, the conditional means equal 1 and all three statistics agree. In law II, the means differ from 1 and the statistics differ substantially, confirming GH-D3F5. Independent asymmetric Gaussian tails agree with direct conditional quadrature to below `2e−16`; centred-statistic refinement changes are below `2.1e−8`. No author centred values were available or read before this calculation.

The original checkpoint mistakenly used asymptotic wall normalization. Its original bytes are preserved, and the exact finite-last-scattering matching correction is explicitly identified as post-checkpoint. This is an auditor recipe error, not a finding against the author.

| Scenario | D_W | D_V | F-median PBS (c) | W09 PBS (c) | Constant-share interval |
|---|---:|---:|---:|---:|---|
| PAPER_REFERENCE | 0.230614572273 | 7.132537333228 | 0.810772266865 | 1.121362660203 | [0.260865625127, 0.998267555902] |
| NW15_CMB_FIT | 0.352690326899 | 11.327583314531 | 0.816058813008 | 1.056632599471 | [0.368859433130, 1.161784484341] |

All **20/20** full-precision claims are verified. Maximum absolute differences are `3.02e−14` for D_W/D_V, `1.50e−12` for PBS values, `6.05e−10` for interval endpoints, and `5.62e−10` for product excess. Their respective budgets are `1e−12`, `1e−9`, `1e−9` and `5e−8`.

The formal tangent statistic remains conditional. The W09 seed is extrapolated, the median seed is heuristic, and H15 is restricted to constant shares. No observational statistic or unique prediction is derived.

## 7. Numbers and reproduction: claim register

Each inventory claim records `VERIFIED`, `VERIFIED_WITH_DEVIATION`, `REFUTED` or `NOT_VERIFIABLE`, together with the auditor's value, method and tolerance. A reproduced scientific output is distinguished from an environment-specific hash or a historical private approval that cannot be independently recovered.

| Check | Auditor result |
|---|---|
| Complete CPython 3.13.16 suite, warnings as errors | 1207 passed, 0 skipped, 0 failed; 424.62 s |
| Complete CPython 3.11.17 suite, warnings as errors | 1207 passed, 0 skipped, 0 failed; 475.29 s |
| H evidence | 36/36 gates on both interpreters |
| Same-interpreter base → head | 3185 numeric leaves under unchanged keys identical; 16 renamed leaves identical; two expected text changes |
| Cross-interpreter comparison | 3201 numeric leaves identical; largest numeric difference 0 |
| Figures | 3/3 byte-identical; also match the saved third-audit hashes |
| Runner | 3/3 byte-identical: 0.8107722668657, 1.1213626602037, 0.9181569463963 |
| Inventory and report tables | 1193/1193 numeric paths and 310/310 table cells; zero deviations |
| Tolerance audit | 750 comparisons; zero missing explicit budgets |

The 1G-B validator's scientific content is identical. Its raw hashes at the committed base and head are respectively `6c9198bae110c0d00cea90dee20074f48a29ff142c79556f3fcb7460ce27fb7f` and `a77118bb954aba118a1445cda899a63cf9786478e3181f8e3995d63955006d5c`. The only changed leaf is `provenance.repository_head`.

The historical hash `5746cc76e932ad0db3e253ee5aa5f0032227e65afba1699a09ea1f2c32d13c8d` reconstructs exactly from either independently regenerated artifact after selecting head `18bf2fb`, `dirty=true`, and the author's `fc-v80` platform metadata. This supports a comparison before and after working-code changes at an unchanged HEAD. It does not establish byte equality between artifacts that identify different committed HEADs (GH-D4F3). Whole H artifact hashes likewise depend on environment and provenance; they are not cross-platform gates.

All missing test inputs were freshly regenerated: unchanged upstream cells and three oracles through the disclosed adapter; B2 and 1D-B artifacts; owner-decision Monte Carlo; and 1D-D from a clean descendant at `18bf2fb`. The 1D-D script internally checks that source/worktree and tests its provisional artifact. Those baseline-environment runs do not replace the separate 1207-test H acceptance suites. Final-tree closure is recorded after report and inventory creation in the evidence and inventory.

## 8. Implementation, tests and mutation testing

`_require_strict_json` calls `json.dumps(export, allow_nan=False)`, catches `TypeError` and `ValueError`, and raises the dedicated contract error. All nine serializable H records invoke this check last, after type validation, normalization of their own scalars and input/result binding. The guarantee concerns the actual export, including the nested B fields that it exports. Unexported density `G` or identity-tolerance fields may retain `Fraction` values without violating that guarantee. Representative serialization overhead is about **0.098 ms** for a prebuilt export, or **0.113 ms** including export construction; these measurements exclude constructor recomputation.

The **1446** probes cover **21** serialized classes. Accepted constructions decrease **456→416**, accepted non-strict exports **129→98** (H records **12→0**), and accepted non-finite values **8→0**. There is no new acceptance. The changed outcomes comprise 18 LCDM, 10 anchored-ratio and 12 H-sigma cases. All 98 remaining non-strict exports are B records, including 32 on the two hardened classes. Every known nested counterexample and both factor-999 probes are refused.

The B diff changes only the two `__post_init__` methods. It preserves the factory expressions operation for operation and uses the factory's unchanged list of early-spectrum comparison fields. Native computed records are accepted, and the 124 existing B test cases remain unchanged. The truncation envelope is finite, nonnegative and budget-capped, but is not recomputed from the spectrum: changing it from `4.0042e−12` to 0 is accepted within the chosen limited contract. Relative quadrature change is recomputed from the stored sigma values.

The narrow B successor also leaves LCDM `omega_m`, `growth_today_photon_normalised` and `omega_m_R_cubed_Mpc3` domain-checked rather than rebound to the recipe or radius identity. The two unit-sigma fields are tied to their relative-change diagnostic but are not independently regenerated from the full spectrum. Explicit anchored inputs, such as the anchor value and its consistency tolerance, remain inputs; the four derived outputs and the comparison-field list are bound. Full factory compatibility replay is expressly outside the chosen scope. These remaining limits are disclosed, rather than silently treated as comprehensive record reconstruction.

The public naming and import firewall remains intact: the new JSON helper is private, no new public name or key introduces a forbidden observational label, and no other package module imports `global_variance`. The evidence-script diff changes the renamed diagnostic, `not_shared` text, prints and docstrings; its numerical expressions are unchanged.

Native-float comparisons are exact. `np.float32` follows its disclosed comparison precision: an anchored growth ratio of `1.1129452345080468` may be stored as float32 `1.1129451990127563`, a relative discrepancy of about `3.19e−8`, and that B record's own export is not strict JSON. H does not import these two B result classes. This is a disclosed representation limit, not continued arbitrary factor-999 acceptance or a failure of the H export guarantee. A future successor should explicitly choose a native-float or precision-independent policy; the current tests do not decide that policy for the owner.

The literal H binding boundary accepts a requested relative drift of `0.95e−12` and refuses `1.05e−12` on both available interpreters. These witnesses are comfortably separated from binary round-off. The Monte Carlo normalizer takes one point per independent draw, so its standard error matches the draw-aware calculation. The additive C_W error budget is approximately **1.85/2.00** times the covariance-aware empirical standard error under laws I/II. It shares draws with the tested statistic and conservatively gives no credit for their correlation, as documented.

Mutation counts subtract the one environmental failure caused by the disposable copy not being a Git repository. The round-4 baseline has **194 passed and one environmental failure**; every claimed kill fails at least one additional test. B01, B02, B03, B07, B08, B09 and B10 are killed. B04/B05 survive test-budget loosening; B06 survives a calibration perturbation within the declared `1e−9` budget. J01–J03 and L01–L05 are killed.

The historical campaign source hash matches `edabc3cebba2c1732d20d44ce4b644af40e76be0de59eb70081f537d4d538049`. The first-delta campaign kills **21/23**, with N5/N9 surviving; the author campaign kills **9/10**, with stale D1 separately adapted and killed; the second-delta campaign kills **22/23**, with benign A02 surviving. R01–R04 are killed.

The auditor adds **13** mutations. Removing the seed-share or interval JSON export guard (X02/X04) survives all 53 phase cases and all 36 gates, yet independent malformed-export witnesses distinguish each mutant from the correct baseline (GH-D4F1). Growth/premise guard removals have no distinct counterexample and are classified as redundancy, not current defects. Moving the JSON check before validation is killed, as are an approximate `1e−8` comparison and swapped ratio operands. Comparison after `float()` survives as a beneficial policy-tightening probe. Relaxing native exact equality to `1e−12` also survives and is distinguished by a one-ULP witness; add native-policy coverage if exact equality is retained. Restoring Simpson test budgets to 1% survives as test-only loosening. The adapted mutation disabling D1 binding is killed.

These survivors have different meanings: they do not all establish a scientific failure. The evidence does not justify a claim of 100% mutation strength.

## 9. Documentation consistency and errata

All 16 renamed values are identical. Old-key and “conditional covariance” occurrences are historical or explicitly annotated. Earlier audit verifiers retain old keys because they target historical trees. The lexical scan classifies **711** matching lines, including mathematical uses of P11. Old “49 tests,” “32 skipped,” “not pushed,” “store floats” and strict-JSON assertions occur in historical records or have successor interpretations. Current P14 summaries remain accurate under the declared last-recorded-event convention after P15.

| Erratum | Literal quote | Correct reading |
|---|---|---|
| GH-D4E1 | see the validation record (original tree) and the two remediation records (remediated trees). | Four remediation records now exist; point explicitly to the latest third-delta remediation record. |
| GH-D4E2 | Status tokens, the five `NOT_GRANTED` authorisations, equations, tolerances, frozen records, tags, the files of the four audits, and every package module other than `global_variance.py` and, under its own successor, `lagrangian_sigma.py`. | Runtime/evidence numerical tolerances are unchanged. Simpson TEST acceptance tolerances were deliberately tightened from 1e-2 to 2e-3/5e-3, fully disclosed in §2; this broad summary should specify its narrower scope. |
| GH-D4E3 | The 1G-B validation artifact is byte-identical before and after its successor. | Scientific content is identical. Raw historical before/after working-code artifacts at the same head/platform/dirty state are identical; artifacts generated at different committed HEADs differ in repository_head metadata. |
| GH-D4E4 | LCDMReferenceLinearSigma refuses non-finite, negative, unbound or out-of-tolerance quadrature diagnostics; | Both diagnostics are finite/nonnegative/capped; only relative change is bound to a recomputation from stored sigma values. The truncation envelope is not re-integrated from the spectrum and a within-budget zero can still be stored. |

These are interpretation corrections proposed by this audit; no existing source is edited. Each quoted author statement is associated with its immutable audited source in the inventory. The stale two-record summary is an unchanged sentence missed earlier. Its INFO classification does not reopen an already scoped scientific finding. Documentation should explicitly distinguish runtime budgets from test thresholds, and budget-capped truncation diagnostics from diagnostics recomputed from the spectrum.

## 10. New findings

### GH-D4F1 — Nested strict-JSON guards for seed-share and interval exports lack behavioral tests

**LOW / TESTS / CORRECTION**, relates to `GH-D3F2`.

The current strict-JSON implementation correctly rejects malformed nested exports, but removing the EvaluatedVoidShare or AdmissibleGlobalLinearInterval export check survives all 53 phase tests and all 36 evidence gates. These are behaviorally distinct survivors, rather than redundant guards: exact Fraction substitutions in the seed quadrature and the interval's resolved premise radius remain numerically bound yet are not JSON serializable.

Evidence: contracts/own_independent_results.json: X02 and X04 survive phase tests and H evidence; contracts/json_seed_witness_results.json: baseline rejects equal Fraction seed_quadrature.truncation_tolerance; X02 accepts a non-strict export; contracts/json_interval_witness_results.json: baseline rejects equal Fraction premise_radius.radius_Mpc; X04 accepts a non-strict export.

Locations: src/timescape_fsigma8/global_variance.py: EvaluatedVoidShare.__post_init__/to_json_dict; src/timescape_fsigma8/global_variance.py: AdmissibleGlobalLinearInterval.__post_init__/to_json_dict; tests/test_phase1g_h_global_variance.py: test_gh_d3f2_nested_inputs_must_export_as_strict_json.

Consequence: A future refactoring could omit either export guard without any committed phase test or numerical gate detecting loss of the public strict-JSON contract. No current implementation counterexample or changed scientific number was found.

Proposed correction: Add constructor/replace tests that require the dedicated strict-JSON refusal for an equal unsupported scalar in an evaluated Gaussian-threshold seed quadrature and in an interval's resolved premise radius. The correction should kill X02 and X04 without changing the runtime or the scientific formulas.

### GH-D4F2 — Current validation summary still names two remediation records

**INFO / DOCUMENTATION / CORRECTION**, relates to `NEW`.

Current H report §11 points to two remediation records although four now exist.

Evidence: All four remediation report files and report header/scope-note links; Current summary lines 1283-1284.

Locations: reports/phase1g_h_global_variance_closure.md §11:1283-1284.

Consequence: The latest 1207-case validation source is underspecified in the local summary; no physical numerical, status, or authorization result changes.

Proposed correction: Point explicitly to the third-delta remediation record or say all remediation records without a stale count.

### GH-D4F3 — 1G-B byte-equivalence statement needs working-tree provenance scope

**LOW / DOCUMENTATION / CORRECTION**, relates to `GH-D3F4`.

The two committed trees do not produce byte-identical 1G-B validator artifacts: their repository_head metadata differs. All numeric/scientific output is identical. The historical hash can be reconstructed from both by selecting the same dirty-working-tree head/platform provenance.

Evidence: reproduction/regression_summary.log: 1G-B raw hashes differ; reproduction/phase1g_b_hash_scope.json: only actual changed leaf provenance.repository_head; both metadata-only historical reconstructions match 5746cc76...c13c8d.

Locations: reports/phase1g_b_contract_hardening_successor.md section4; reports/phase1g_b_contract_hardening_successor_inventory.json equivalence; reports/phase1g_h_delta_audit_3_remediation.md sections0/3.

Consequence: An unqualified byte-equality statement can be read as an impossible committed-tree gate; it does not show any scientific regression or fabricated numeric result.

Proposed correction: Specify the original comparison as before/after code changes at unchanged HEAD 18bf2fb in a dirty working tree; for committed-tree comparisons compare scientific content exactly and report provenance differences separately. Retain the raw historical hash as scoped evidence.

## 11. Recommendations, not owner decisions

| Item | Recommendation |
|---|---|
| H-OD1 | Retain the named formal tangent research proposal. Prefer convention (c), with (a) as the fixed-mass comparison. |
| H-OD2 | Select no physical reference value. Keep the median seed heuristic, W09 a formal extrapolation, and the interval conditional on constant shares. |
| H-OD3 | Change no status-registry token or any of the five `NOT_GRANTED` authorizations. |
| H-OD4 | Keep the runtime experimental. Close GH-D4F1's test gap, clarify documentation and run the mandatory Windows gate before promotion. |
| H-OD5 | Require separate explicit owner decisions for PR, merge, freeze and tag. This audit provides no such permission. |
| P15 | Record it once with the next authorized substantive addendum: exact range `36d127f..027b7a4`, superseded historical state and a dated read-only snapshot. |
| B float32 policy | Disclosure is sufficient for the currently chosen limited contract. Prefer an explicit uniform scalar/precision policy before broader API promotion, through a separately authorized successor. Add native one-ULP coverage if exact comparison remains policy. |

The frozen B tag remains valid. No new D-v2 branch or tag is authorized. Numerical success does not silently supply any owner decision.

## 12. Limits

The Windows gate was not run, and the exact deployed model variant is not exposed. No private author conversation, approval transcript, historical push actor or push time was recovered. The root was not blind. The initial independent last-scattering recipe error is retained, and its correction is explicitly post-checkpoint.

Ordinary Jupyter startup was blocked. The exact-cell fallback in fresh processes is transparently identified. Selected mutations and fixed-seed Monte Carlo checks do not prove all possible contracts. This reduced scientific and delta review is not a new full audit of unchanged phases and derives no physical geometry, closure, observational radius map or unique prediction.

Historical artifact and duration claims are distinguished from fresh measurements. Final validation metadata and log closure may be completed after execution. No product source or existing test changes occur.

## 13. Sources with hashes

The companion inventory contains complete source and evidence SHA-256 ledgers. Essential immutable audited sources are listed below.

| Path | SHA-256 |
|---|---|
| AGENTS.md | 881050c02635ab9003b494305b3fcf43360815defb32174604b67daa6fd77ecc |
| CLAUDE.md | a7a39483cdaacde49ba101c49100a3fdfc582f2c925e5341aace769452e66ef8 |
| UPSTREAM.lock | 1ae190f3b976c752935b115b83d4b8d986635db785fba0d4b5ed0b39072694be |
| reports/phase1g_b_lagrangian_sigma_validation.md | 4f6b6246d1a08d371a5c374ab1249a3ee5e6495bf9c790153433353487f5e057 |
| reports/phase1g_b_owner_decisions_successor.md | de2648783f4748e46e9ad9e6914b290a02948ddb8f0d1421e6de073590595b55 |
| reports/phase1g_b_contract_hardening_successor.md | 3c58c8db40d563500db7606a9ffc6eeb3b11140c450e79034d8349e169119405 |
| reports/phase1g_b_contract_hardening_successor_inventory.json | 68a0fb9751c4536c1b998ead5e649be349116825306a6c36f906223a0f9c5555 |
| reports/phase1g_h_delta_audit_3.md | 7b91a8c5d3ab066432183d1124592948d3a8ccd52a649acf0f8dfa0a564c09b1 |
| reports/phase1g_h_delta_audit_3_inventory.json | 8f65f6360bc2477a7aa0b9883e7198209014e6bd558a2d79ef6c2f1dc073e9e8 |
| reports/phase1g_h_delta_audit_3_remediation.md | 6236add8d6adb11ff01c9d6b5df9df7ffe37ef34db68075ebd80c7cd9625bc16 |
| reports/phase1g_h_delta_audit_3_remediation_inventory.json | 7ea300a8810de48e638bd9415a0c19736a36e653d636172a8fb0e56179a658f5 |
| reports/phase1g_h_delta_audit_2_remediation.md | 4607537cad455943d5cb64801a57022345218adb7f5d3f6f26fe67c1b0533472 |
| reports/phase1g_h_delta_audit_2_remediation_inventory.json | 9a17cb4e9a00008d5492647c005d88bff53fff84252cfa4317f5af4d28cb777d |
| reports/phase1g_h_publication_successor.md | ac7de063f28a69f2ddc996296fddfa45b0604780f29a1932ff21af8fefe44a16 |
| reports/phase1g_h_publication_successor_inventory.json | e33d3888dfebc2c5a679076cf9686d0a6308948192a533c86f24463c4ba35013 |
| reports/phase1g_h_global_variance_closure.md | 3b3bba0b33f0fd83e9eafb762638778f9c945bc11bcce64cd5ea06a554351ef1 |
| reports/phase1g_h_global_variance_closure_inventory.json | acfbdf222de9e15af7410ffeaddfa54d6ec7937828c46e28052a6e738e7b0442 |
| reports/phase1g_h_global_variance_closure_validation.md | 96f8993bc9c3379cf013ca2c052b876451c62d4732b1d9f441dda03f1f83cf7c |
| src/timescape_fsigma8/global_variance.py | 96934ea62d22c2bff07ff6edf00631b0fe556579d29f02ea0efa27b79af9bf4b |
| src/timescape_fsigma8/lagrangian_sigma.py | e9bab68ee010df9ed249565413d578f739322ee644d8197a128615006319bd3a |
| scripts/phase1g_h_global_variance_closure_numerics.py | a5fd601fecc06c57526fd644632d2595f75086457cc7eeb825a301e45c284981 |
| scripts/validate_phase1g_b_lagrangian_sigma.py | e1a7fb39658bcd079216924cc6a8b02ffb275d88b04995e4b37845f4c59ff9bc |
| tests/test_phase1g_h_global_variance.py | 201cc8fa928bf52a333314cc52888c552b36dfc2b9ed91fa374af3eff679ca62 |
| tests/test_phase1g_b_contract_hardening.py | 90cab4583be45395b7cd996a7e8c2c3f651f1c26196245196f57658d5dee26d4 |
