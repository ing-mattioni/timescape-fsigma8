# Phase 1G-H — third independent delta audit

**Classification:** `INDEPENDENT_DELTA_AUDIT`

**Date:** 2026-10-09

**Auditor:** OpenAI Codex, GPT-6 family; exact deployed variant/version is not exposed. The author and second delta auditor are Claude-family sessions. No author contact or conversation access occurred. Scientific blinding was compartmentalized; the root/governance roles were non-blind.

**Base:** `e5170285e1d4b4aa72e907a3a79110d05584c0d9`, tree `45ce98f9d21e93e355ba25812063aec270700116`.

**Audited head:** `ed0ec0c9c8783519a53759a265b6ce37e6c0e607`, tree `afba6630d02cb04d941ddb8b42092d7884e79786`.

**Environment:** Linux 6.18.44 / glibc 2.39, CPython 3.11.17 and 3.12.14; `OPENBLAS_NUM_THREADS=1`, `-B -W error`. See environment manifests for dependency versions. Windows owner gate: **NOT RUN**.

## 0. Summary

**Overall: `ACCEPT_WITH_CORRECTIONS`. SCIENCE: `ACCEPT`.** The Gaussian constructions, H25 identity, normalizer, weighted CW product moment and conditional main values reproduce independently. The third remediation preserves all physical outputs and closes its specified test survivors. Its universal strict-JSON statement is incomplete, and current publication summaries remain stale after P11. New defensive-contract findings require follow-up without changing the reproduced physics.

| Area | Verdict |
| --- | --- |
| PROVENANCE | ACCEPT |
| GOVERNANCE | ACCEPT_WITH_CORRECTIONS |
| SCIENCE | ACCEPT |
| NUMERICS | ACCEPT |
| IMPLEMENTATION | ACCEPT_WITH_CORRECTIONS |
| TESTS | ACCEPT_WITH_CORRECTIONS |
| DOCUMENTATION | ACCEPT_WITH_CORRECTIONS |
| TASK_COMPLIANCE | ACCEPT |
| overall | ACCEPT_WITH_CORRECTIONS |


Merge/freeze readiness: `NO_SCIENTIFIC_BLOCKER_PENDING_CONTRACT_TEST_P11_CORRECTIONS_WINDOWS_GATE_AND_OWNER_DECISIONS`. This is **not permission to merge, freeze or publish**. Runtime remains experimental, with the existing ungranted observational authorizations. Cross-family outcome: **`CROSS_FAMILY_VERIFIED_WITH_DEVIATION`**. Two auditor errors in the initial blind recipe are retained and disclosed in §6; no author scientific error follows from them.

Second-delta finding totals: four `RESOLVED`, two `PARTIALLY_RESOLVED`; both errata `APPLIED`. No original or first-delta finding regresses. New findings: one LOW-MEDIUM, three LOW, one INFO; no new scientific blocker.

| ID | Severity / area | Resolution |
| --- | --- | --- |
| GH-D3F1 | LOW / GOVERNANCE | CORRECTION |
| GH-D3F2 | LOW / IMPLEMENTATION | CORRECTION |
| GH-D3F3 | LOW / TESTS | CORRECTION |
| GH-D3F4 | LOW-MEDIUM / IMPLEMENTATION | OWNER_DECISION |
| GH-D3F5 | INFO / DOCUMENTATION | CORRECTION |


This audit adds only its report, inventory and evidence on `phase-1g-h-delta-audit-3`. It does not correct existing files, publish, create a PR/tag/release, merge, freeze, contact the author or grant observational status. The owner's P10/P11 handoff confirmations refer to historical actions, not a new audit push.

## 1. Object and authenticated hashes

The graph is exactly `e517028 → 9ad5425 → 4bf2718 → ed0ec0c`:

| Commit | Tree | Delta role |
| --- | --- | --- |
| `9ad54253c4ec40cede5690da6659be28e0bd0a2d` | `6e7d84574a0c89b240547542207c1241e4f71344` | Typed binding/input conversion, seven tests, H25 gate label |
| `4bf2718e7557ace3fdc0abffaa73587f1162f776` | `8ca972fada8dff3507616a2603ae6640fe4beedc` | Documentation and third-remediation records/logs |
| `ed0ec0c9c8783519a53759a265b6ce37e6c0e607` | `afba6630d02cb04d941ddb8b42092d7884e79786` | P10 publication addendum and summaries |

All parent/tree IDs and the expected **34-path diff (14 M, 20 A)** match. No unexpected path changed. Exact reconstructed Git object IDs were verified after a native authenticated clone was unavailable; connector acquisition was read-only. The remote author branch was still at the audited head in the timestamped snapshot, with no observed drift.

Preservation checks establish 184 earlier-audit files identical to e517028; all 57 pre-existing package files and 111 frozen 1G report files identical to 8d3cdd0; the runner and three configurations identical to the delta base. The package count excludes the H module added after the frozen base. `lagrangian_sigma.py` and `scientific_status.py` are included. The H inventory's scientific results, covariance, assumptions, equations, definition, anchoring, missing input, status and authorization subtrees are unchanged.

The three scientific code/script/test SHA declarations and seven H `files.added` entries match the head. Twelve historical first-remediation hashes match their explicitly identified 89cb041 tree: **22/22 required checks**. There is no invented requirement that an environment-specific output hash must equal a source-file hash or another interpreter's artifact.

## 2. Method and committed blind checkpoint

The required prompt, AGENTS/CLAUDE, prior audits and inventories/evidence, remediation/publication records, full delta, current report and frozen D/E/F/B context were examined by the independent area roles. Optional earlier prompt attachments were absent; repository records supplied their history. Scientific, implementation, reproduction and provenance work were divided among four roles as explicitly permitted by the commission; synthesis and verdicts are the root auditor's responsibility. Completed evidence was retained when agent execution reached a usage limit, and the root finished the audit.

Science was derived using separate EH98/tracker code, deterministic Plackett orthants, composite Gauss-Legendre ball integration and independent Gaussian generating-function/conditional-regression checks. The science role imported no H implementation and had not read H full outputs or prior H audit evidence at its checkpoint. It knew the rounded prompt values and received sanitized construction inputs from a non-blind role. This qualifies as compartmentalized scientific blinding, not whole-team blinding. The root's governance reading did not constitute blind scientific evidence.

**Blind checkpoint:** `c62ad87d9a51c40d8959d35e0bec58c8b1048a51`, tree `6d5e848faa7b72d829e44a9a2d79e70c3a34acb6`, parent ed0ec0c. Its five files, with SHA-256 in the inventory, remain byte-identical. Checkpoint reconstruction and analytic checks precede the full numerical comparison. Later refinement is independently identified outside the checkpoint. Post-checkpoint recipe corrections are explicitly non-blind and never overwrite the checkpoint.

Implementation probes freshly invoke constructors, compare baseline to e517028 and strict-serialize exports. Mutation testing changes temporary runtime copies outside the audited tree; committed evidence contains definitions/verifiers/results, not altered production code. Regression comparisons exclude only environment metadata and figure metadata, compare figure hashes separately, and remap exactly the six H25 gate leaves when indicated. Precision-dependent inventory/report checks use explicit half-last-printed-digit absolute tolerance with a 2e-12 floor for inventory values; exact parsed artifact comparisons use zero tolerance. See each claim's method and tolerance.

## 3. Provenance and governance, P7–P11

Read-only API snapshot **2026-10-09 05:50:56 UTC** verifies:

| Ref | Observed head |
| --- | --- |
| main | `8d3cdd0533035858c42269cb1dff1a20dcafc7da` |
| ccr-555e67be-u11yht | `ed0ec0c9c8783519a53759a265b6ce37e6c0e607` |
| ccr-ac582de6-vho99i | `e5170285e1d4b4aa72e907a3a79110d05584c0d9` |
| phase-1g-h-independent-audit | `816dd004763f8de1a8bb09cba9e427a1bd2bb3d1` |
| phase-1g-h-delta-audit | `5c325e1fd05b343f6d5e93f931038794de4373a2` |

There are 24 branch refs, 38 annotated tag refs with exactly the first-delta names/object IDs, four closed PRs (none from 1G-H), no release and no forbidden D-v2 reference. Local authenticated peeling yields 76 logical tag/peeled entries. This is not a claim that native `git ls-remote` freshly returned 76 refs.

| Event | Independently established | Authorization evidence |
| --- | --- | --- |
| P7 | Graph 89cb041→226e52d contains 5c325e1, 248a06b, 226e52d; successor records it | Historical owner quote in records, indirect here |
| P8 | Prior audit records direct GH-F15 confirmation | Retain prior `RESOLVED_OWNER_CONFIRMED`; not independently repeated in this handoff |
| P9 | 226e52d→e517028 contains exactly 6411650 and e517028, branch head observed | Secondary pasted transcript, **NOT_VERIFIABLE** as approval words here |
| P10 | 226e52d→4bf2718 contains checkpoint/audit/remediation four commits | **Direct current owner confirmation** |
| P11 | 4bf2718→ed0ec0c contains only ed0ec0c; remote head observed | **Direct current owner confirmation**, separate from P10 |

Current refs and graph compatibility do not independently recover a historical push's actor, time or preceding remote ref. The P9 limitation is not evidence of an unauthorized push. No new publication is authorized. This audit itself records the P11 confirmation: the owner wrote **“Confermo le autorizzazioni P10 e P11”** in the handoff.

P7–P10 tables correctly supersede the original GH-D2F1 statements. After P11, README, CLAUDE, H report header and inventory still use 4bf2718 as a current remote head (GH-D3F1). The proposed convention is sound: record P11 once in a chronological successor, call P10 the **last recorded publication event**, and separately timestamp the observed current ref. A commit does not need an endless successor just to document its own push.

All four older-remediation record changes contain only additions, no removed lines. Historical complete bytes remain accessible in Git. The owner-authorized plan permits these unfrozen annotations; they are acceptable, but a canonical chronological successor with short historical pointers will be clearer than repeated layered status notes. This recommendation is not a new permission barrier.

AGENTS rules 1–10 hold for the reviewed delta: no equation/units/IC/sign change; equation references preserved; binding changes are representation validation; new tests exist; no copied upstream code; P10/P11 separately confirmed; typed pure-function design retained; all 15 gate thresholds, `RECORD_IDENTITY_RTOL=1e-12`, 1440 radial intervals, orthant tolerance 1e-12/start32 unchanged; no introduced warning suppression. Pinning gate thresholds is a useful policy-regression test; an explicitly approved future policy change may update declaration and test together.

## 4. Second-delta findings and errata

| ID | Outcome | Reason |
| --- | --- | --- |
| GH-D2F1 | PARTIALLY_RESOLVED | P7–P10 and historical wording are covered; P11 leaves current remote-head summaries stale. New GH-D3F1. |
| GH-D2F2 | RESOLVED | Requested tests kill the previously targeted mutants; H25 is honestly labeled numerical assembly consistency. New branch-coverage limitations are GH-D3F3. |
| GH-D2F3 | RESOLVED | Dated erratum and inventory/log agree with independent recount, including six renames, 100 additional inside leaves and the 1e-12 relative criterion. |
| GH-D2F4 | PARTIALLY_RESOLVED | Named H float outputs/input conversions are correct; genuine H records retain nested non-JSON scalars. New GH-D3F2; universal strict-JSON claim is false. |
| GH-D2F5 | RESOLVED | Historical shared-constraints wording and hash scope clarified by additions only; original records remain available in Git. |
| GH-D2F6 | RESOLVED | Independent derivation confirms signed/lognormal latent-Gaussian identifiability with mask–carrier covariances fixed. Independence fixes law I. |
| GH-D2E1 | APPLIED | Independent saved-89cb041 versus freshly regenerated-248a06b recount matches the correction exactly. |
| GH-D2E2 | APPLIED | P7 is recorded and dated historical publication statements are explicitly superseded. |


The record says findings were “addressed,” not independently declared resolved. Four are now resolved; two are only partial. Gate relabeling is honest and does not hide a scientific failure. New test-coverage discoveries are separately scoped rather than falsely claiming the requested A/R mutations still survive.

## 5. Earlier findings: regression review

| IDs | Retained status | Basis |
| --- | --- | --- |
| GH-F1, GH-F2 | RESOLVED_BY_OWNER_DECISION | Conditional formal proposal and no physical/observational closure promotion |
| GH-F3…GH-F14 | RESOLVED | Preserved corrections, scientific inputs and explicit limitations; no delta regression |
| GH-F15 | RESOLVED_OWNER_CONFIRMED | Prior direct owner confirmation retained; present P10/P11 independently confirmed |
| GH-DF1…GH-DF6 | RESOLVED | Shared constraints narrowed, H inputs bound, counts superseded, linear-limit interpretation and prior tests/median qualifiers retained |

The 32 prior binding probes were rerun. Equal Fraction result substitutions are now refused as intended, while documented tolerance/metadata substitutions remain distinct. No malformed physical H result was newly accepted. Imported-class probe behavior is unchanged. Newly discovered frozen 1G-B direct-construction gaps (GH-D3F4) were missed earlier; they are not regressions introduced by this remediation or a reversal of the specifically scoped GH-DF2 H binding result.

## 6. Cross-family scientific reconstruction

**Outcome: `CROSS_FAMILY_VERIFIED_WITH_DEVIATION`; SCIENCE `ACCEPT`.** Starting with W binary and E[ψ|wall]=1, δ=Wψ/f_w−1 gives

`1 + ξδ(r) = P11(r) E[ψ1ψ2 | both walls] / f_w² = P11(r) CW(r) / f_w²`.

This proves H25 and its equivalence to the full partition/cross/wall assembly H18 at x=0. Fixing P11 and CW on the specified ball fixes the integral variance uniquely. It does not choose spatial geometry, covariance kernels or the missing physics. The gate comparing assemblies of the same arrays is useful numerical consistency; retain it under `numerics`, without claiming independent physical validation.

Gaussian tilting gives `mII=Q(c−κ0)/f_w` and unconditional wall-normalized density covariance equal to the unnormalized carrier covariance divided by mII². The unconditional normalized mean is 1/mII; do not confuse unconditional covariance with a both-walls conditional moment. Pair tilting gives

`CW = exp(KY(r)) Q2(c−κ0−κ(r), c−κ0−κ(r); ρ) / [P11(r) mII²]`.

For signed carriers the independent generating-function derivation agrees with conditional Gaussian regression/tail integration. P11 fixes mask ρ monotonically; the Gaussian carrier law fixes KY, and κ0/κ(r) complete the joint Gaussian pair covariance. They fix CW in both signed and lognormal classes; law I fixes them to zero by independence. The latent-Gaussian qualifier is essential for this identifiability claim. It is not a non-Gaussian closure theorem. **GH-D2F6 is resolved.**

The immutable blind reconstruction had two auditor errors. First, it used asymptotic matter-era normalization instead of finite last-scattering matching. The correct independent tracker propagation is `DW=(fw0/fwLS) aLS (t0/tLS)^(2/3)`; the blind formula missed `1/[gammaLS fwLS^(1/3)]`. Relative DW correction: −1.57823626e−5 GM / −8.45500517e−6 NW15. Second, its X_SU label referred to the compressed H share rather than threshold-only 1G-D share. These are explicitly corrected in the separate **post-checkpoint, non-blind** own-code comparison; no author H code is imported. They explain the deviation outcome and are not author findings.

### Matched-recipe conditional values


| Scenario | D_V | W09 direct rms | F-median direct rms | constant-share direct rms interval | A_v W09 | X_SU threshold-only | X_SU compressed |
|---|---:|---:|---:|---|---:|---:|---:|
| GM | 7.132537333228 | 1.121362660203 | 0.810772266865 | 0.260865625127–0.998267555902 | 1168.914723790 | 1.262631553125 | 1.263461300439 |
| NW15 | 11.327583314531 | 1.056632599471 | 0.816058813008 | 0.368859433130–1.161784484341 | 1184.662182614 | 1.284975945824 | 1.285682723618 |

| Scenario | signed law I weighted CW−1 | signed law II weighted CW−1 |
|---|---:|---:|
| GM | 0.755929586089 | 0.043189407474 |
| NW15 | 0.791264148143 | 0.069083112915 |

| Scenario | r_s Mpc | lambda | m_II | I weighted CW−1 | II weighted CW−1 | total rms II/I |
|---|---:|---:|---:|---:|---:|---:|
| GM | 1 | 0.813736670976 | 2.869413474886 | 0.786920193781 | 0.837693200838 | 1.028342144077 |
| GM | 2 | 0.869535108737 | 2.139808561227 | 0.751490944555 | 1.097277234245 | 1.186540014377 |
| GM | 4 | 0.998433753819 | 1.623350651791 | 0.725311248556 | 1.277631960576 | 1.293157997502 |
| NW15 | 1 | 0.785149918566 | 2.474113487926 | 0.840794361798 | 0.697655401753 | 0.919394747059 |
| NW15 | 2 | 0.839193025704 | 2.104325108486 | 0.797525865215 | 0.887005537703 | 1.049504684094 |
| NW15 | 4 | 0.949341994318 | 1.668578791219 | 0.766158582157 | 1.115836139975 | 1.187904897141 |

Digits identify numerical calculations, not physical precision. These are conditional model-internal diagnostics. The signed carrier permits negative wall densities and is a signed diagnostic; lognormal construction yields nonnegative densities but retains free resolution and calibration assumptions. No observational sigma8, fsigma8, RSD or unique Timescape prediction is authorized by this verification.

### Error budget and independent checks

The post-checkpoint table compares **58 quantities, all VERIFIED**, against the independently regenerated audited-tree artifact. The full machine-readable ledger gives each value, absolute/relative difference, method and tolerance. The largest absolute difference is 6.05261e−10 (constant-share upper endpoint); the largest relative difference is 1.05745e−8 (the small signed law-II moment).

| Quantity family | maximum absolute error |
|---|---:|
| D_W / D_V | 3.01981e-14 |
| W09 direct rms | 8.55538e-13 |
| F-median direct rms | 1.50002e-12 |
| constant-share endpoints | 6.05261e-10 |
| A_v | 3.81306e-10 |
| X_SU, both conventions | 2.91545e-13 |
| lambda | 2.42802e-11 |
| m_II | 4.89893e-11 |
| m_II inverse-square ratio | 1.13212e-11 |
| CW−1, signed and lognormal | 5.61585e-10 |
| total rms ratio II/I | 5.38944e-11 |

Main propagation values use absolute audit tolerances 1e−12 for D_W/D_V, 1e−9 for rms/interval/X, 1e−6 for A_v; latent read-outs use 1e−6 absolute, compatible with the archived numerical radial error scale. Actual discrepancies are much smaller and are reported above rather than implied by those budgets.

The blind analytic tests independently validate mask H25 algebra, bivariate orthant vs conditional-tail integration, rho=0/1 limits, lognormal one-wall normalization, signed pair moments via regression versus generating-function derivatives, and the ball Fourier/top-hat identity. Maximum residual is 5.7e−15. An independent halving experiment on the blind code (800 radial Gauss-Legendre nodes/6001 spectral nodes versus 1600/12001) changes weighted CW−1 by at most 1.45e−10 GM / 2.15e−8 NW15, m_II by 6.62e−11 / 6.55e−9, and lambda by 4.84e−11 / 7.74e−9. These refinement results were produced from the blind script before comparison, outside the checkpoint, and are preserved separately.

### Terminology

CW−1 is the conditional **product-moment excess relative to the one-wall mean**, and is exactly the defined H25 ingredient. Under dependent law II, E[psi_i|both walls] need not equal 1, so CW−1 need not equal the literal covariance conditional on both walls, which subtracts the product of those conditional means. This terminology distinction does not alter any H25 formula or output.



The detailed supplement contains the retained blind/matched side-by-side values and full tolerance ledger. All results are conditional model-internal diagnostics. No unique Timescape prediction, observational σ8 or fσ8 authorization follows.

## 7. Numerical reproduction and claim ledger

Both interpreters regenerate **36/36 gates**, split 10 numerics / 20 physics / 6 reproduction. All **3201 numeric leaves and all compared text leaves are bitwise identical** across CPython 3.11.17/3.12.14. Regenerating 248a06b and ed0ec0c on the same 3.12 interpreter gives 3197 common numeric leaves identical, and exactly six gate leaves relocated physics→numerics with their values unchanged. After path remapping, all 3201 match; no other added/removed leaves. All three figure SHA-256 hashes match.

Three runner values reproduce old/new exactly: GM F-median ≈0.810772266865, GM W09 ≈1.121362660204, NW15 constant-share ≈0.918157 (full outputs in runner evidence). The frozen D/E/F construction inputs are not independently promoted into physical closure.

The inventory reconciliation maps **1193 scientific scalar leaves**, zero unmatched/zero deviations; **310 numeric report-table cells**, zero deviations; independent science adds **58 verified values**. The complete ledger contains **1734 claims**:

| Status | Count |
| --- | --- |
| VERIFIED | 1722 |
| NOT_VERIFIABLE | 6 |
| REFUTED | 4 |
| VERIFIED_WITH_DEVIATION | 2 |


Each inventory entry identifies declared/auditor values, method, tolerance and source where applicable. Four refuted claims are current P11 head wording and the three overbroad JSON/type rationales, not a scientific table value. Two deviation claims disclose auditor errors. Unverifiable entries distinguish historical approval/execution evidence, unavailable interpreters/Windows and unexposed model version. Counts measure explicit checks, not independent scientific degrees of freedom.

Independent GH-D2E1 recount, saved 89cb041 artifact versus freshly regenerated 248a06b:

| Region | Common leaves | Numeric changed | Beyond 1e-12 relative | Text changed | Only old / only new | Max absolute change |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| Gaussian-threshold subtree | 204 | 156 | 140 | 4 | 6 / 106 | 0.0007719476316552232 |
| Outside subtree | 3517 | 3 gate diagnostics | 3 | 0 | 0 / 16 | 0.000011450464257434234 |

Inside: six old names are renamed in the new artifact; therefore 106 only-new paths comprise six renames plus **100 additional** paths. Outside physical outputs are unchanged; three diagnostic values changed. Relative criterion is `abs(new−old)/max(abs(new),abs(old)) > 1e-12`, exact inequality counts separately. The author correction agrees with this independent recount.

Prior saved whole-artifact hashes were also reconstructed exactly by remapping H25 leaves back and substituting the **recorded prior environment**. Three earlier hashes match (see reconstruction evidence). This authenticates a deterministic reconstruction, not execution of Python 3.13 in this audit. The declared current 3.13 hash is environment-specific and not a gate; our 3.12 artifact SHA-256 is `b15b070b067a756ecc067d26d057a71501fc7aa238b07178832b0bf93e24a35c`, 3.11 is `0ca46384b46f31042052185067357848a9c23392efde84b5d26d3fd8de0a40c0`.

Fresh historical inputs: all three upstream notebook oracles at pinned commit/notebook hash; 1D-B growth; 1D-D anchored density (clean separate worktree as required by its validator); all five B2 artifacts; owner-decision Monte Carlo **124/124 gates**. The historical 32 skips disappear after these inputs are available. A setup-time 3.12 run had 23 skips while regeneration was in progress; an interrupted 3.11 setup run is excluded. Only completed all-input runs count as full-suite acceptance.

Validation record: `PASS`. Completed 3.11: **1185 passed, 0 skipped, 0 failed**, 236.46 s. Final-tree 3.12: **1185 passed, 0 skipped, 0 failed**, 231.22 s. Governance validator: **PASS**, 55 top-level report JSON files. Full commands and closure checks are recorded in `final_validation.json` and the final logs. The numerical tolerance audit is **749 comparisons, 0 missing**. Unique-key/non-finite checks also cover the optional evidence. Windows CPython 3.14.3/3.11.9 remains **NOT RUN** and mandatory before promotion.

## 8. Implementation, seven tests and mutation testing

The finite-float branch of `_same` is coherent for factory-produced H fields, which recompute to native floats. `isinstance(x,float)` accepts NumPy float64 and ordinary float subclasses; it excludes float32. Equal Fraction/int/Decimal result substitutions are refused by the declared typed-output policy. Fraction inputs accepted by the Real-valued input contract are converted; Decimal is not a Real and is legitimately refused there. `_bind_recomputed` identifies the offending field/type. G and all five named check tolerances store floats. No physical formula or threshold changed.

The scalar campaign covers **1446 probes / 21 serializable classes / zero missing classes**: 456 accepted, 129 accepted exports fail strict JSON (base 216), 104 outcome/storage changes including 78 new refusals and 13 conversion improvements; no imported-class changes and no new acceptances. Integer/float32 substitutions that change value are explicitly marked, so their refusal is not misreported as legitimate-input rejection. The critical H-export counterexamples are nested quadrature/density/radius inputs, not legitimate factory float32 outputs. Complete-result serialization is therefore incomplete (GH-D3F2).

Unchanged 1G-B result constructors also permit NaN/infinity diagnostic fields and arbitrary positive decomposition factors, now recorded as a new scope decision (GH-D3F4). These LCDM/anchored classes are not directly imported by the H module. The finding does not invalidate frozen numerical outputs or authorize modifying a frozen module.

| New test | Strength and practical limit |
| --- | --- |
| Pair-weighted CW summary (A18) | Explicit synthetic P11 weighting catches readout/denominator changes; integrated calculation still shares supplied kernels |
| mII inverse-square reporting (A20) | Protects normalizer/calibration/readouts, but mostly restates the same analytic identity; not a separate physics oracle |
| Sample-normalized Monte Carlo | Independent random sample normalization tests two-point kernels and m; one seed/configuration, coarse finite-amplitude tolerance |
| Simpson half-resolution ratio (A15/A16) | Quintic exact-error identity plus independent adaptive quadrature is strong numerical evidence |
| Binding boundary/record identity (A01/A07/A09) | Meaningful recomputation/object checks; boundary scales with the imported tolerance and misses small policy drift |
| Pinned thresholds (A22/A23) | Useful accidental-policy-change protection; approved future choices can update declaration/test together |
| Typed floats/input conversion (R01–R04) | Catches intended Fraction/Decimal branches, but misses accepted float64/rejected float32, all five conversions and nested imported exports |

Monte Carlo pair-aware error analysis finds the normalizer SEM about 9.8% larger than the naive SEM because the paired observations are dependent. Its CW error budget is conservative at 1.83–2.03 times a pair-aware standard error; five budgets allow about 3.14%/2.58% relative CW error. Thus this is a useful coarse independent check, not an exact iid “5σ” calibration or a fine precision proof. Prefer paired-cluster SEM or explicitly call it a conservative budget. No observed test failure is hidden by this distinction.

| Adapted campaign | Killed / requested | Other outcomes |
| --- | --- | --- |
| First delta | 21 / 23 | N5, N9 survive |
| Author | 9 / 10 | Original D1 not applied because target string is stale; separately adapted D1 killed |
| Second delta auditor | 22 / 23 | A02 survives |
| R01–R04 | 4 / 4 | All killed |

N5 removes a redundant central orthant split while the adaptive convergence contract remains. N9 reverses a metadata equation sign, not the numerical implementation: text correctness remains a documentary obligation. A02 removes the old special bool case, but under the new finite-float branch it effectively tightens a tiny near-zero comparison; legitimate factories still pass, no misleading result was demonstrated. Classifications are supported by actual outputs, not assumed solely from author labels.

Ten additional own mutations plus adapted D1:

| ID | Tests / evidence gates | Adjudication |
| --- | --- | --- |
| B01 tolerance 1e-12→1.1e-12 | Survives / survives | Own 1.05e-12 stored-value witness switches rejection to acceptance; missing policy pin |
| B02 accept exact float only | Survives / survives | Own legitimate float64/subclass witness now rejected |
| B03 admit NumPy float32 | Survives / survives | Own zero-diagnostic witness accepted, strict JSON fails |
| B04 MC budget 5→10 | Survives / survives | Weakens test only; expected survival with correct runtime unchanged, no runtime defect demonstrated |
| B05 Simpson ratio budget 1%→10% | Survives / survives | Weakens test only; exact baseline sits within both tolerances, no runtime defect demonstrated |
| B06 calibration +1e-10 | Survives / survives | Within declared 1e-9 accuracy budget, legitimate survivor |
| B07 P11 denominator 1 ppm | Killed / survives | Synthetic CW test catches readout error; gates do not independently validate that metadata |
| B08 calibration 1 ppm | Killed / killed | Calibration/normalizer test and numerical gate catch it |
| B09 reported lambda 1 ppm | Killed / survives | New readout test catches it |
| B10 omit ode_atol conversion | Survives / survives | Own Fraction input witness now fails strict JSON |
| Adapted D1 disable binding | Killed | Binding/identity/typed-float tests catch it |

Own behavioral probes detect B01/B02/B03/B10 outside the committed test suite, so “survives” is not a claim that the defect is unobservable. All seven requested new tests kill their designated existing mutants. There is no honest 100% mutation-strength conclusion; new coverage finding GH-D3F3 records the remaining contract gaps. No runtime mutant is included in the audit commit.

## 9. Documentation coherence and errata

The lexical review records 92 occurrences of the requested phrases. Historical “not pushed,” old test counts and earlier runtimes remain legitimate when explicitly dated/superseded; current phase count is 49, not 42. The runtime estimate now says about 50–80 s, a historical environment-specific estimate, not a guarantee for this audit's machine. Physics wording around H25 is revised and the gate is in numerics. “Same shared constraints” is narrowed appropriately; README/CLAUDE median numbers retain the heuristic qualifier. The active residual is P11 remote-head wording. Historical counts/permissions are not converted into new current facts.

Three literal errata in third-remediation statements:

| ID / location | Exact erroneous wording | Correct reading |
| --- | --- | --- |
| GH-D3E1 / reports/phase1g_h_delta_audit_2_remediation.md §1 | Fail-closed, and strict JSON holds by construction | Named H recomputed float fields are finite and typed; named H scalar inputs are converted. Nested imported records still admit non-JSON scalars. The guarantee is incomplete (GH-D3F2). |
| GH-D3E2 / reports/phase1g_h_delta_audit_2_remediation.md §2, GH-D2F4 | The 1G-B records the runtime imports already store floats and are unchanged. | They are unchanged, but not every validated field stores a native float; imported quadrature, density and radius inputs give nested H counterexamples. |
| GH-D3E3 / src/timescape_fsigma8/global_variance.py _same docstring | an equal ``Fraction`` or ``int`` would pass the comparison but break the strict-JSON contract of ``to_json_dict`` | A Python int is valid strict JSON. Refusing integer substitutes is the declared typed-float output policy; Fraction/non-native scalar export failure is a different rationale. |


The corresponding universal assertion in the H module docstring and report §10 also needs narrowing or the transitive export correction. The distinction between a typed-float policy and JSON syntax matters: Python int is JSON-compatible. CW−1 terminology is a separate INFO clarification, GH-D3F5, without a formula change. The remediation is substantially successful, but its universal serialization description is more favorable than the tested contract permits.

## 10. New findings

### GH-D3F1 — P11 leaves current publication summaries stale

**LOW / GOVERNANCE / CORRECTION / relates to GH-D2F1.**

The remote author branch is ed0ec0c, but unqualified remote-head summaries name 4bf2718; P11 has no successor entry in the audited tree.

Evidence: provenance_result.json remote and publication_graph; Direct owner handoff confirms P10 and P11 separately.

Consequence: Current publication-state wording is inaccurate; this is not a missing authorization or a scientific defect.

Locations: README.md:146–147; CLAUDE.md:466–468; reports/phase1g_h_global_variance_closure.md header; reports/phase1g_h_global_variance_closure_inventory.json publication and owner_decisions_status_2026_10_09; reports/phase1g_h_publication_successor.md §7 and companion inventory.

Proposed resolution: Record P11 once in a chronological successor, with the direct current confirmation. Call P10 the last recorded publication event; put current remote head in a separately timestamped snapshot. Do not chase a self-referential push record.

### GH-D3F2 — Strict JSON is not guaranteed transitively for genuine H records

**LOW / IMPLEMENTATION / CORRECTION / relates to GH-D2F4.**

Imported 1G-B configurations validate scalar values without storing native scalars. A valid H result can contain Fraction/NumPy fields whose export fails strict JSON.

Evidence: implementation_scalar_probes_results.json: 1446 probes, 129 accepted exports fail strict JSON, zero imported-class behavior changes; 12 genuine nested-H counterexamples: ten quadrature representations and two density/radius Fraction inputs.

Consequence: The typed-float repair improves the intended H fields, but the universal export promise and assertion that imported records already store floats are false. Physical factory results are unchanged.

Locations: src/timescape_fsigma8/global_variance.py module docstring and ConditionalGlobalLinearSigma.to_json_dict; src/timescape_fsigma8/lagrangian_sigma.py LagrangianSigmaQuadrature, EarlyMatterDensityPerPhoton, ResolvedLagrangianRadius; reports/phase1g_h_delta_audit_2_remediation.md §§1–2; reports/phase1g_h_global_variance_closure.md §10.

Proposed resolution: Under an authorized follow-up, normalize supported nested scalar inputs or reject unsupported representations consistently, and test json.dumps(..., allow_nan=False) on nested H results. Until then narrow the documented guarantee; do not silently edit the frozen module.

### GH-D3F3 — New tests miss float branches, a conversion and binding-tolerance drift

**LOW / TESTS / CORRECTION / relates to GH-D2F2.**

Phase tests and all evidence gates accept mutations that reject legitimate float subclasses, admit non-JSON float32 diagnostics, omit one scalar conversion, or increase the binding tolerance by 10%.

Evidence: mutation_extra_results.json B01/B02/B03/B10 survive 49 phase tests and 36 gates; implementation_survivor_probes_results.json independently distinguishes all four from baseline.

Consequence: The new tests close the specified earlier survivors but do not fully protect the advertised type/conversion and tolerance policy.

Locations: tests/test_phase1g_h_global_variance.py binding-boundary and typed-float tests; src/timescape_fsigma8/global_variance.py _same, RECORD_IDENTITY_RTOL and TwoPhaseGrowthChecks.

Proposed resolution: Cover all five converted check fields and G, accepted numpy.float64/ordinary float subclasses, refused float32 outputs and nested exports. Pin RECORD_IDENTITY_RTOL independently if 1e-12 is policy. Tighten Monte Carlo/Simpson wording to their actual error budgets.

### GH-D3F4 — Previously unseen validation gaps in frozen 1G-B result records

**LOW-MEDIUM / IMPLEMENTATION / OWNER_DECISION / relates to NEW.**

Unchanged LCDMReferenceLinearSigma accepts non-finite error diagnostics; AnchoredLagrangianSigmaRatio accepts arbitrary positive growth_ratio/early_spectrum_factor without binding their decomposition.

Evidence: implementation_scalar_probes_results.json representative unbound.lcdm and unbound.anchor probes; lagrangian_sigma.py is byte-identical to 8d3cdd0; imported-class probes are unchanged against e517028.

Consequence: Public direct result construction can export non-finite diagnostics or a misleading factor of 999. These two classes are not directly imported by H and no regenerated numerical result changes. This is new discovery in unchanged material, not a regression of GH-DF2.

Locations: src/timescape_fsigma8/lagrangian_sigma.py LCDMReferenceLinearSigma.__post_init__; src/timescape_fsigma8/lagrangian_sigma.py AnchoredLagrangianSigmaRatio.__post_init__.

Proposed resolution: Authorize a narrowly scoped 1G-B contract-hardening successor: validate finite/domain-appropriate diagnostics and bind the factor decomposition or explicitly label those fields unverified metadata. Preserve frozen historical numerical records; make this follow-up scope decision explicit before promotion.

### GH-D3F5 — CW minus one is not generally a literal both-walls conditional covariance

**INFO / DOCUMENTATION / CORRECTION / relates to NEW.**

CW is explicitly E[psi1 psi2 | both walls]. Its excess over one is referenced to one-wall normalization, whereas a covariance conditioned on both walls subtracts two both-conditioned means.

Evidence: Independent Gaussian tilting derivation in science_comparison.md; law II shifts both-conditioned means away from one.

Consequence: The formulas and computed statistic are correct; the exported covariance label can suggest a different centering.

Locations: scripts/phase1g_h_global_variance_closure_numerics.py both_walls_conditional_density_covariance_ball; reports/phase1g_h_global_variance_closure.md §§6.3 and 10.

Proposed resolution: Explain CW−1 as a both-walls conditional product-moment excess relative to the one-wall mean, and distinguish it from the centered both-walls covariance. Preserve or deprecate any key with an explicit compatibility note rather than changing the science.

## 11. Owner recommendations and P11 convention

| Decision | Recommendation; no action taken |
| --- | --- |
| H-OD1 | Keep a named formal tangent research proposal. Prefer radius convention (c), with (a) as the fixed-mass comparison. This remains conditional construction, not an observation-ready Timescape closure. |
| H-OD2 | Choose no physical reference value. Median 1G-F seed is heuristic; W09 seed uses formal extrapolation; constant-share interval belongs to its closure class. |
| H-OD3 | Keep all tokens/authorizations unchanged: global linear mean remains NOT_DERIVED, σ8/fσ8/RSD/observational/unique-prediction authorizations remain NOT_GRANTED. |
| H-OD4 | Keep runtime experimental. Correct nested export/test/documentation contracts; explicitly decide scope of a frozen 1G-B hardening successor; run Windows gate before promotion. |
| H-OD5 | No scientific blocker was found. Merge/freeze/publication are distinct owner decisions after corrections and mandatory Windows gate. No forbidden phase-1g-d-separate-universe-growth-v2 ref. |

Record P11 once in the next chronological publication successor with the present direct owner confirmation; label the old summary “last recorded publication event P10” and keep timestamped current-state observations separate. This audit already acknowledges P11 without altering the old ledger. P10/P11 confirmation is sufficient for those historical actions, not a request to repeat or extend them. Ask separately to publish this audit only on its designated branch after the local final commit.

## 12. Limits

This is delta review plus the specifically requested independent scientific reconstruction, not a new full audit of frozen phases. No physical spatial geometry, observational transfer, nonlinear closure, or non-Gaussian uniqueness result is derived. Gaussian signed density can be negative and remains a diagnostic; lognormal positivity does not remove resolution/calibration assumptions.

Windows is unavailable; CPython 3.14.3/3.11.9 and 3.13 were not run. Linux success cannot satisfy that owner gate. Exact served model variant/version is not exposed. No author conversation was inspected. Compartmentalized blinding and both initial auditor errors are explicit, so the matched-recipe results are not represented as pristine blind numeric agreement.

Current remote snapshots prove current state and ancestry compatibility, not actor/time/prior-head history. P9 words are secondary and unauthenticated here; earlier approvals other than P10/P11 rely on prior records. Raw artifact hashes and runtimes depend on environment; saved prior hash reconstruction is distinct from rerunning the recorded interpreter. Monte Carlo and mutation coverage are finite and do not prove all-path correctness. Repeated frozen numerical checks were limited to preservation/regression except the new serialized-record probes requested by the prompt.

## 13. Sources and hashed evidence

Fresh pinned primary-source downloads reproduce the expected TeX/source content hashes; W07 was a single gzip transport and was hashed after decompression. These are provenance checks of the specified source versions, not endorsement of every physical assumption.

| Source / version | Hashed content | SHA-256 |
| --- | --- | --- |
| [GM 2511.17160v2](https://arxiv.org/src/2511.17160v2) | main.tex | f9cadfa03ecc9a74b0a8f432ae4b13422daeb219f253756bcd877b4b75077c59 |
| [W07 0709.0732v2](https://arxiv.org/src/0709.0732v2) | solution.tex | 221662c987e454729ef8202c87fa697c5882b5b7daaecdedb50a7cba8ffe6cd8 |
| [W09 0909.0749v2](https://arxiv.org/src/0909.0749v2) | observe.tex | 2b0324d127440e9a053a7cb37102d7655cca228a63cd2222843e879989b4b531 |
| [NW15 1410.3470v2](https://arxiv.org/src/1410.3470v2) | cmb1.tex | 5688c9ac7123a5c2ef3508e39cb3134c2fe9e3d5e56996a4d4a4d101d7b74673 |
| [JLH13 1304.6087v2](https://arxiv.org/src/1304.6087v2) | voids_mnras.tex | cf6fc77a31b395138ac3a027d008698556534e81cfb27c39853d3a99c7b07c4e |
| [EH98 astro-ph/9709112v1](https://arxiv.org/src/astro-ph/9709112v1) | trans.tex | 5f2ac6b413df8b738c95f6650152b7e82d7c36f6d9b3a618da540e9739dce17f |
| [SvdW04 astro-ph/0311260v1](https://arxiv.org/src/astro-ph/0311260v1) | downloaded source archive | 4b7ad599f54b3199e0448df1c2eecf4e724401e9ffda7b0f50a3efe7fecdb79b |


Upstream reference: [MarcoGaloppo repository](https://github.com/MarcoGaloppo/Linear-Perturbations-in-averaged-cosmological-models), pinned `590c6fd5332acb15f5683ebf392a0d7ce54983c5`; notebooks are reference-only and no upstream source was copied into publication deliverables. Fresh oracles and source manifests identify exact hashes. The inventory includes SHA-256 for every packaged audit evidence file, the five immutable checkpoint files, exact audited commits/trees, detailed claims and preservation results.

Main evidence: `science_comparison.md`, post-checkpoint/refinement results, scalar/binding/Monte Carlo/survivor probes, adapted and extra mutation results, provenance snapshot/review, numerical summary/table/runner comparisons, reconstructed prior hashes, interpreter manifests and final validation logs. Large regenerated artifacts and temporary mutated runtime copies remain git-ignored or outside the audit tree. Evidence README describes reproduction paths and scope.
