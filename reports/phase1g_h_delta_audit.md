# Phase 1G-H — independent delta audit of remediation

Classification: `INDEPENDENT_DELTA_AUDIT`. Date: 2026-10-08. Auditor: OpenAI Codex (OpenAI GPT-6 family).

Independence: the same auditor family as the first audit; separate science and implementation workstreams, no contact with the Claude author and no access to its conversation. This continuation was report-exposed; the unavailable earlier blind checkpoint is not reconstructed or attributed a guessed hash. The new formula checkpoint and its timing limitations are recorded below.

Audited base: `816dd004763f8de1a8bb09cba9e427a1bd2bb3d1`, tree `759ab21d3a36eeada67c2943e155240dc631b77a`; head: `89cb041f901b51a3f90fa6831aab1b4553c1772c`, tree `34d40316c16f5c7cc9e044ba16db662509f3c8ac`.

Environment: Linux, CPython 3.12.14 / 3.11.17; NumPy 2.3.5 / 2.4.6, SciPy 1.17.0 / 1.17.1, matplotlib 3.10.8 / 3.11.2, pytest 9.1.1. `OPENBLAS_NUM_THREADS=1`, `-B -W error`; no warning suppression. Exact dependency records and command logs are in the evidence directory.

Companion: `phase1g_h_delta_audit_inventory.json`; evidence: `phase1g_h_delta_audit_evidence/`.

## 0. Summary

**Overall: `REJECT`; merge/freeze readiness: `NOT_READY_SCIENTIFIC_CORRECTION_CONTRACT_REMEDIATION_AND_OWNER_CONFIRMATION_REQUIRED`.** The formal tangent proposal and most numerical/code repairs are valid. Rejection is directed at the remaining positive-density common-covariance proof and completeness claims, not a rejection of every conditional statistic or reproduced number.

| Area | Verdict |
|---|---|
| PROVENANCE | `ACCEPT` |
| GOVERNANCE | `ACCEPT_WITH_CORRECTIONS` |
| SCIENCE | `REJECT` |
| NUMERICS | `ACCEPT` |
| IMPLEMENTATION | `ACCEPT_WITH_CORRECTIONS` |
| TESTS | `ACCEPT_WITH_CORRECTIONS` |
| DOCUMENTATION | `ACCEPT_WITH_CORRECTIONS` |
| TASK_COMPLIANCE | `ACCEPT_WITH_CORRECTIONS` |

| Original finding | Outcome | Reason |
|---|---|---|
| GH-F1 | `RESOLVED_BY_OWNER_DECISION` | D1 correctly narrows to a proposed zero-amplitude tangent with an explicit smoothing rule; finite-small-scale ensemble response is not claimed. |
| GH-F2 | `RESOLVED_BY_OWNER_DECISION` | D2 explicitly stipulates H-A9 seed-indexed accounting; material-domain extension is unproved and W09 void/region ratios exceed one. |
| GH-F3 | `RESOLVED` | The volume-share identity and compression versus threshold-only k=0 responses are correct. |
| GH-F4 | `PARTIALLY_RESOLVED` | H15 is correctly restricted to constant shares and the step counterexample is correct; an integrated RMS deviation is still presented as a pointwise or two-window accuracy bound. |
| GH-F5 | `PARTIALLY_RESOLVED` | The signed Gaussian qualification/mechanism is repaired; the added nonnegative pair fails the claimed common unconditional wall-density covariance constraint. |
| GH-F6 | `PARTIALLY_RESOLVED` | Direct/post-hoc/PBS-reclosure variants are computed and distinguished correctly; section 8 still claims a transfer-only correction. |
| GH-F7 | `PARTIALLY_RESOLVED` | Cap fractions and wall-density-freedom conclusion are repaired; section 8 still declares the full S1 necessary. |
| GH-F8 | `PARTIALLY_RESOLVED` | W09 extrapolation and median heuristic status are present; median summary values in README/CLAUDE omit the epsilon-threshold/no-controlled-error qualifier. |
| GH-F9 | `PARTIALLY_RESOLVED` | All 19 original invalid probes reject; five additional input versus value or convergence provenance inconsistencies are accepted. |
| GH-F10 | `RESOLVED` | Panel/refinement implementation passes 99 independent two-threshold cases; 20 historical cases return accurately and one refuses at the 1024 cap. |
| GH-F11 | `RESOLVED` | The four-decimal input-plus-output rounding budget is algebraically correct and references pass; full-precision accuracy is not thereby established. |
| GH-F12 | `RESOLVED` | EH98 no-wiggle terminology and baryon-shape suppression match Eqs. 26, 28–31 of the unchanged provider. |
| GH-F13 | `RESOLVED` | All four display corrections, seven source hashes and proper-radius clarification check. |
| GH-F14 | `RESOLVED` | All 16 successor entries and source hashes/positions check; ref creation and fast-forward are separately described. |
| GH-F15 | `OPEN_OWNER_CONFIRMATION` | No direct owner confirmation of the two earlier recorded push approvals was received in this delta-audit handoff. |

Six new findings: 1 MEDIUM-HIGH, 2 MEDIUM, 2 LOW-MEDIUM, 1 LOW. No HIGH finding is introduced. All 22 exact cited errata replacements are applied, but this does not close their parent findings when related claims survive elsewhere.

This audit changed no existing tracked file. It did not correct the implementation or revised report, publish anything, alter any token, authorize observation, create a PR/tag, or merge/freeze a phase.

## 1. Object and hashes

The authentic Git commit/tree/blob objects were reconstructed through read-only GitHub data and checked by their exact Git object hashes. Chain: `816dd00 → c1b4482 → 89cb041`, with intermediate tree `4a8d3f59946cd990fc7c50fb59882982c5a93724`. The owner-recreated first-audit commit differs from the auditor-local original commit metadata but has the prescribed identical audit tree. No hash was invented to bridge that difference.

Exactly 18 changed paths relative to 816dd00: 11 modified, 7 added. They are precisely the authorized delta. All 43 first-audit paths are identical to 816dd00, all 57 pre-existing package files are identical to 8d3cdd0, and all 12 remediation SHA-256 declarations match. Three runner configurations are preserved.

## 2. Method

Read the permanent AGENTS rules, both commit records, entire changed diff, full revised H report, original independent audit, remediation and inventories. Approved D/E/F/G context and exact primary scientific passages were read as delta context, not reaudited from scratch. Own derivation code has no project imports. The science formula checkpoint precedes reading the newly implemented evidence helper in that workstream, but follows exposure to report expectations; it is explicitly **not blind**. Hash: `d7e71077f4070ffb18832da05467f658e6ba11b3c2445b13398bc4ad37137c0d`.

Separate tests cover deterministic numerical reproduction, independent formulas/quadrature/Monte Carlo, record tampering, 99 two-threshold orthants and 23 disposable mutants. Evidence code runs outside the audited tree. Agreement of identical project code between interpreters is reproduction, not an independent derivation.

## 3. Provenance and governance

Remote read-only snapshot: `main=8d3cdd0`, `ccr-555e67be-u11yht=89cb041`, `phase-1g-h-independent-audit=816dd00`. No branch drift at the snapshot. 38 tag objects match the first audit; the seven 1G signed objects also pass embedded-key mathematical verification. No owner-trust configuration was created. Existing PRs 1–4 are closed; no H PR, release or forbidden D-v2 ref was found. A snapshot cannot prove that no transient historical remote event ever occurred.

All 16 freeze-successor citations verify. S7 and S10 explicitly identify joined/formatted spans; S13 has correct base hashes and per-phrase locations; S14–S16 have exact quoted text/JSON and pinned hashes. The map is expressly non-exhaustive. Historical pre-freeze claims are acceptable when read through this dated successor.

The remediation is explicitly committed on the session branch above the audit; this deviation from the generic phase branch is described rather than concealed. The new public orthant API is keyword-only with mandatory scientific/tolerance choices. Naming/isolation tests pass; no other package module imports `global_variance`. The scope firewall adds no observational exception.

AGENTS 1/3/4: narrowed model/evidence changes and normalization conventions are explicit; author-reported approvals are records, not independently verified chat. Rule 2: H-equation labels and primary references are adjacent to the new formulas. Rules 5/8: pure typed runtime and tests exist, subject to DF2/DF5. Rule 6: upstream is read-only/reference-only. Rule 7: this audit made no remote changes. Rule 9: 1e-12 record-identity tolerance, orthant 12-sigma truncation, 1024 per-panel cap, 1e-15 minimum tolerance, 10·tol symmetry check, 5% linear-limit gate and step-premise ratio 1 are recorded. Rule 10: no warning suppression. The 5% linear-limit threshold is an empirical local gate, not a priori physical control or a rigorous truncation bound.

Each remediation commit was assessed under the permanent rules:

| Rule | c1b4482 (code) | 89cb041 (documentation) |
|---|---|---|
| 1, equations and approval | New H identities/constructions are declared; D1–D4 choices fit the allowed corrections. Exact author chat approval is not independently verified. | Records the choices; it does not establish off-repository approval. |
| 2, equation references | H labels and primary references accompany share identity, orthant, kernels, step construction, reclosure and rounding. | Definitions and sources are stated in the revised report. |
| 3, refactoring versus model | Orthant/record hardening is distinguished from the added statistical constructions. | Remediation lists both changes; the added covariance inference is refuted by DF1. |
| 4, conventions | Latent smoothing, conditional normalization, calibration and constant-share scope are explicit. | Fixed constraints are overstated (DF1); §8 also contradicts the repaired normalization reading (DF3). |
| 5, scientific tests | Seven new cases; original and new numerical regressions pass, with coverage limits in DF5. | Test/gate counts are reproducible; they do not establish complete remediation. |
| 6, upstream license | No upstream source in the delta. | No upstream source included. |
| 7, remote publication | A local commit does not establish permission to push. | Subsequent remote presence is verified; authorization and GH-F15 still need direct owner confirmation. |
| 8, typed/pure runtime | Typed records and pure calculations retained; input/result binding remains incomplete (DF2). | Runtime is still labelled experimental. |
| 9, tolerances | Identity, panel, tail, symmetry, linear-limit and step limits are explicit. | The 5% gate is disclosed as a local check; no prospective threshold registration is claimed. |
| 10, warnings | No undocumented warning suppression introduced. | Reproduction used warnings as errors; the Jupyter transport limitation is disclosed. |

The push is physically corroborated by remote refs. “Nothing is pushed” and `pushed:false` describe the 2026-10-07 commit-time record; retain them historically and add a dated 2026-10-08 publication successor. README/CLAUDE current summaries should point to it. Remote existence does not prove authorization. GH-F15 remains `OPEN_OWNER_CONFIRMATION`; the handoff contained no direct confirmation of the two earlier approvals. D1–D4 exact chat-point mapping remains `NOT_VERIFIABLE`.

## 4. Original findings GH-F1–GH-F15

### GH-F1 — `RESOLVED_BY_OWNER_DECISION`

D1 correctly narrows to a proposed zero-amplitude tangent with an explicit smoothing rule; finite-small-scale ensemble response is not claimed.

### GH-F2 — `RESOLVED_BY_OWNER_DECISION`

D2 explicitly stipulates H-A9 seed-indexed accounting; material-domain extension is unproved and W09 void/region ratios exceed one.

### GH-F3 — `RESOLVED`

The volume-share identity and compression versus threshold-only k=0 responses are correct.

### GH-F4 — `PARTIALLY_RESOLVED`

H15 is correctly restricted to constant shares and the step counterexample is correct; an integrated RMS deviation is still presented as a pointwise or two-window accuracy bound.

### GH-F5 — `PARTIALLY_RESOLVED`

The signed Gaussian qualification/mechanism is repaired; the added nonnegative pair fails the claimed common unconditional wall-density covariance constraint.

### GH-F6 — `PARTIALLY_RESOLVED`

Direct/post-hoc/PBS-reclosure variants are computed and distinguished correctly; section 8 still claims a transfer-only correction.

### GH-F7 — `PARTIALLY_RESOLVED`

Cap fractions and wall-density-freedom conclusion are repaired; section 8 still declares the full S1 necessary.

### GH-F8 — `PARTIALLY_RESOLVED`

W09 extrapolation and median heuristic status are present; median summary values in README/CLAUDE omit the epsilon-threshold/no-controlled-error qualifier.

### GH-F9 — `PARTIALLY_RESOLVED`

All 19 original invalid probes reject; five additional input versus value or convergence provenance inconsistencies are accepted.

### GH-F10 — `RESOLVED`

Panel/refinement implementation passes 99 independent two-threshold cases; 20 historical cases return accurately and one refuses at the 1024 cap.

### GH-F11 — `RESOLVED`

The four-decimal input-plus-output rounding budget is algebraically correct and references pass; full-precision accuracy is not thereby established.

### GH-F12 — `RESOLVED`

EH98 no-wiggle terminology and baryon-shape suppression match Eqs. 26, 28–31 of the unchanged provider.

### GH-F13 — `RESOLVED`

All four display corrections, seven source hashes and proper-radius clarification check.

### GH-F14 — `RESOLVED`

All 16 successor entries and source hashes/positions check; ref creation and fast-forward are separately described.

### GH-F15 — `OPEN_OWNER_CONFIRMATION`

No direct owner confirmation of the two earlier recorded push approvals was received in this delta-audit handoff.

D1 and D2 implement allowed narrowing choices. D3 correctly requalifies the signed pair but fails its stronger added nonnegative fixed-density-covariance claim. D4 correctly computes three conventions, while its self-audit wording is incomplete. The choice-content correspondence is within the first-audit suggested resolutions; exact off-repository authorization wording is not inferred.

## 5. Original errata and withdrawn claims

| Erratum | Outcome | Revised location |
|---|---|---|
| GH-E1 | `APPLIED_EQUIVALENT` | reports/phase1g_h_global_variance_closure.md: 66–79 |
| GH-E2 | `APPLIED_EQUIVALENT` | reports/phase1g_h_global_variance_closure.md: 80–93 |
| GH-E3 | `APPLIED` | reports/phase1g_h_global_variance_closure.md: 409–420 |
| GH-E4 | `APPLIED` | reports/phase1g_h_global_variance_closure.md: 547–566 |
| GH-E5 | `APPLIED` | reports/phase1g_h_global_variance_closure.md: 582–600 |
| GH-E6 | `APPLIED_EQUIVALENT` | reports/phase1g_h_global_variance_closure.md: 752–775 |
| GH-E7 | `APPLIED_EQUIVALENT` | reports/phase1g_h_global_variance_closure.md: 783–831 |
| GH-E8 | `APPLIED_EQUIVALENT` | reports/phase1g_h_global_variance_closure.md: 644–676 |
| GH-E9 | `APPLIED_EQUIVALENT` | reports/phase1g_h_global_variance_closure.md: 373–390 |
| GH-E10 | `APPLIED` | reports/phase1g_h_global_variance_closure.md: 480–495 |
| GH-E11 | `APPLIED` | reports/phase1g_h_global_variance_closure.md: 918–938 |
| GH-E12 | `APPLIED` | reports/phase1g_h_global_variance_closure_validation.md: 122–125 |
| GH-E13 | `APPLIED` | reports/phase1g_h_global_variance_closure.md: 627–641 |
| GH-E14 | `APPLIED` | reports/phase1g_h_global_variance_closure.md: 244–252 |
| GH-E15 | `APPLIED` | reports/phase1g_h_global_variance_closure.md: 1077–1080 |
| GH-E16 | `APPLIED` | reports/phase1g_fg_freeze_status_successor.md: 101–133 |
| GH-E17 | `APPLIED` | reports/phase1g_h_global_variance_closure_inventory.json:owner_decisions.H-OD5 |
| GH-E18 | `APPLIED` | reports/phase1g_h_global_variance_closure_validation.md: 45–51 |
| GH-E19 | `APPLIED` | reports/phase1g_h_global_variance_closure.md: 466–466 |
| GH-E20 | `APPLIED` | reports/phase1g_h_global_variance_closure.md: 537–537 |
| GH-E21 | `APPLIED` | reports/phase1g_h_global_variance_closure.md: 614–614 |
| GH-E22 | `APPLIED` | reports/phase1g_h_global_variance_closure.md: 615–615 |

All 22 original quotations match their exact d4d693d source ranges and have the requested replacement or an equivalent. Four display values now round correctly: 3.46, 6.989, 0.971, 0.340. Full hashes and `R_proper=γ_w0R`, `R_properH_D0=800km/s` check.

“A closed”, unrestricted “any material region”, “closure-independent H15”, positive-mass “realisable/admissible Gaussian laws”, exact late-ΛCDM cancellation and the quantified radiation correction are withdrawn or explicitly qualified at their corrected loci. Legitimate occurrences such as “closed form”, a conditional “closed given p”, class names and quoted history are not misclassified by keyword. The lexical review classifies 279 matches. Active §8 transfer-only and S1-necessity claims remain; see DF3. Legacy anchored scalar fields retain the numerical fixed-closure convention, not a verified transfer recalibration or an authorized interval.

## 6. New science and independent reconstruction (blind-order limitation disclosed)

### 6.1 Tangent, phase allocation and volume share

For the two-state wall example, independently averaged derivative is 0.2746834816803183 versus tangent f_w=0.263; equal-mass mean of 1/(1+δ_L) is 1. The chosen zero-amplitude tangent and `G_R=G·W(kR)` are consistent for a stipulated translation-invariant Lagrangian top-hat statistic. This is not the finite-amplitude ensemble response or a derived transported material-domain rule. First-order weighting changes do not alter a quadratic connected variance at leading perturbative order.

H-A9 radius ratios at convention (c): median 0.3258648693 / 0.3896728936; W09 radius 1.4854169718 / 1.5890353376. The latter fails scale separation; it remains a named formal seed extrapolation.

Explicit bookkeeping gives `f_v,L=f_v,LS(1+δ_L)/(1+ε)` and `p=f_v,LS−∂f_v,L/∂δ_L`. Thus compressed p0=f_v,LS(1+A_v), threshold-only p0=f_v,LSA_v. The implementation uses compression f_v,LS or 0 plus threshold φ(ν)/σ_s; no sign ambiguity remains.

### 6.2 Constant-share counterexample and cap

| Independent quantity | GM | NW15 |
|---|---:|---:|
| k_cut (Mpc^-1) |0.0660431991174|0.0690926951044|
| Premise RMS |0.0999|0.0999|
| R8 RMS |7.24648958941|10.35290472136|
| Ratio to constant-share upper |7.25906551468|8.91120931725|
| Fraction above flat-wall cap |0.463502204966|0.478861373864|

Premise and target use the same convention (c) and top-hat windows; p(k) lies in [f_v,LS, 1] at every k. Relative radial/k-refinement changes for the step value are about 2–3e-13. The premise 0.0999 is below 0.1 by 1e-4, far larger than numerical error. The counterexample refutes the unrestricted bound, not the correctly restricted constant-share interval.

The cap requires some wall-density freedom if the exact-empty-void and Gaussian early-field assumptions are retained; it does not uniquely impose all of S1. Capacity radii 135.58 / 208.80 Mpc (about 99 / 127 dressed h^-1 Mpc) reproduce.

### 6.3 Positive-density construction: failed shared constraint

Let Gaussian Y select walls Y>c, let A=λZ_s with Cov(A1,A2)=a(r), let f_w=P(Y>c), and let b=Cov(Y,A). The independent law has μ_I=E[e^A]=e^(VarA/2). The correlated law normalized to unit conditional wall mass has μ_II=e^(VarA/2) Q(c−b)/f_w. Define `m=μ_II/μ_I=Q(c−b)/f_w`.

For the declared wall-density contrast `δ_w=e^A/μ−1`, its *unconditional connected* covariance is `(exp(a(r))−1)/m²` in law II and `exp(a(r))−1` in law I. Its unconditional law II mean is 1/m−1. The conditional mass normalization is correct; it is precisely why the declared unconditional covariance differs. A contrast separately renormalized by its unconditional mean, or the unnormalized carrier, can share a covariance, but that is a different fixed-input statement.

| Scenario | r_s=1 Mpc: covariance II/I |2 Mpc|4 Mpc|
|---|---:|---:|---:|
|GM|0.1214545522|0.2183988118|0.3794682297|
|NW15|0.1633656778|0.2258262736|0.3591755098|

Normalizer ratios m are 2.8694/2.1398/1.62335 (GM), 2.4741/2.10432/1.66858 (NW15). These are order-unity constraint changes, not a rounding effect. For GM at 1 Mpc the conditionally normalized law II unmasked ball variance is 0.0851452 instead of law I 0.7010458; for NW15 it is 0.1199903 instead of 0.7344892. Calibration to the signed-carrier ball variance therefore fixes the pre-normalized/unconditionally normalized latent-density construction, not both declared conditional wall-density covariances.

The six positive-density totals and ratios reproduce: GM II/I=1.02834, 1.18654, 1.29316; NW15=0.91940, 1.04950, 1.18791. Six independent 2-million-draw four-variate Gaussian Monte Carlo checks validate the kernels (max |z|=1.8692). They do not test the false equality constraint; no spatial-lattice check was performed. Smoothing r_s=1, 2, 4 Mpc and signed-ball calibration are free choices of the construction and must remain declared. The generic need for a joint geometry/density law is plausible and consistent with the covariance identity, but this pair does not establish the stronger fixed-density-spectrum nonuniqueness proof it claims.

The small-λ expansion `e^A/μ=1+A−E[A|wall]+O(A²)` explains the signed-moment limit, with the appropriate λ or λ² factors. A single finite-point-variance 1e-4 test and a 5% gate are a local numerical check, not a full asymptotic convergence theorem. Refining the radial integration changes the small signed masked-wall moment at about 1e-3 relative; printed three-decimal totals survive. Details and any last-digit deviations are in the independent science evidence.

The independently reconstructed signed negative-density probabilities are 0.447590389929 / 0.442942761211 (GM, I / II) and 0.454766439087 / 0.452697911215 (NW15). Their largest author discrepancy is 4.69e-9 absolute, below the declared 2e-8 tolerance. New finite lognormal wall, cross and total moments agree to 9.36e-6 relative, below the separate 2e-5 comparison tolerance.

For the signed II wall moment and its scaled small-amplitude lognormal counterpart, the tight 2e-5 comparison gate fails: discrepancies reach 0.001012422 and 0.001003413 relative. These claims are **VERIFIED_WITH_DEVIATION**; the tolerance was not loosened. The finite-amplitude limit check itself passes the independently chosen 0.02 limit: wall deviations are 0.0092964654 / 0.0064106481 and cross deviations 0.0080681062 / 0.0053464470. Including the omitted first radial panel and refining from 720 to 1440 segments gives signed II wall moments 0.000782523140 / 0.003553182591, with final relative changes 1.65e-6 / 2.02e-6. All published three-decimal RMS values survive. See `science_remaining_science_checks.json` and `science_radial_endpoint_check.json`.

### 6.4 PBS reclosure and rounding

Reclosure means A_s→F²A_s with F=0.9705767695 and recomputing σ_s and φ(ν)/σ_s. The tracker threshold ν=−Φ^-1(f_v,LS) is unchanged because the supplied fraction is unchanged; “recompute the threshold” does not imply that it must numerically change. Direct and empirical post-hoc values remain distinct from reclosure.

| Scenario | Convention | Seed | Direct | Post-hoc | Reclosure | Reclosure/post-hoc |
|---|---|---|---:|---:|---:|---:|
| GM | (a) equal mass | W09 | 0.974562107 | 0.945887341 | 0.967893975 | 1.023265598 |
| GM | (a) equal mass | F_median | 0.704375749 | 0.683650739 | 0.697707596 | 1.020561459 |
| GM | (c) bare proper | W09 | 1.121362660 | 1.088368548 | 1.113687196 | 1.023262936 |
| GM | (c) bare proper | F_median | 0.810772267 | 0.786916728 | 0.803096758 | 1.020561299 |
| NW15 | (a) equal mass | W09 | 1.030739840 | 1.000412144 | 1.020153398 | 1.019733121 |
| NW15 | (a) equal mass | F_median | 0.796018216 | 0.772596788 | 0.785431737 | 1.016612739 |
| NW15 | (c) bare proper | W09 | 1.056632599 | 1.025543055 | 1.045779604 | 1.019732521 |
| NW15 | (c) bare proper | F_median | 0.816058813 | 0.792047726 | 0.805205777 | 1.016612699 |

Reclosure/post-hoc ratios: 1.02326294/1.01973252 (W09), 1.02056130/1.01661270 (median). At a prescribed constant share both methods coincide by algebra; that is an elementary but useful implementation check. Under the same homogeneity η, the constant-share upper RMS is unchanged after input rescaling, when a compatible share bound exists. This does not revive the withdrawn fixed-closure scaled interval. Convention (a) verification is included in the independent science evidence.

Four-decimal reference components have half-unit uncertainty 5e-5. The first-order propagated RMS budget plus output rounding is `5e-5(σ_part/σ+σ_int/σ+1)`: 1.137204081831e-4 / 1.129441809951e-4; discrepancies 2.487558566e-5 / 2.307461453e-6. It is a display-reference reproduction budget. Removing +1 still passes the central reference values, exposing a test boundary gap rather than refuting the algebra.

## 7. Numbers and reproducibility

H evidence: 32/32 gates on both interpreters; 3099 numeric leaves identical, maximum absolute/relative difference 0. On the same 3.12 interpreter, 2729 common old/new numerical leaves survive; maximum absolute difference 6.483702463811e-13. Maximum relative difference for nonzero quantities larger than 1e-12 is 5.732813945366e-13. An independent-law cross term moves 1.11e-16→0, so a naive relative maximum is 1; report the absolute floor rather than claiming a literal relative bound on numerical zero. First-audit saved 3.12 evidence gives the same comparison.

307 new non-metadata terminal paths, none removed; full path lists are in `numeric_reconciliation.json`. The gate/metadata changes are separately recorded, not mixed with published physical outputs. All 1119 numerical leaves in the four revised inventory result blocks match within recorded display precision; no unmatched leaf or rounding deviation remains. No figure-byte identity across library versions is claimed.

Three runner outputs: 0.810772, 1.121363, 0.918157. Tolerance audit: 728 comparisons, 0 missing. Initial 3.12 suite: 1152 passed, 19 skipped because markers were evaluated before historical oracle/B2 regeneration. Oracles and all five B2 artifacts were then regenerated; the same pinned notebook and scientific cells were preserved. Initial 3.11 suite completed exit 0 with 1171 passed progress events, no skips; the console omitted a summary line. Final full suites: **1171 passed, 0 failed, 0 skipped on each interpreter** (247.53 s on 3.12; 248.93 s on 3.11). The final governance validator is **PASS with 50 top-level report JSONs**; the tolerance audit has 728 comparisons and 0 missing; staged `git diff --check` passes. Exact command outcomes and JUnit counts are in `final_validation.json`. Those execution records supplement this report without changing the audited source or the findings.

The claim registry contains 1,357 entries: 1,331 VERIFIED, 4 VERIFIED_WITH_DEVIATION, 17 REFUTED and 5 NOT_VERIFIABLE. It distinguishes VERIFIED, VERIFIED_WITH_DEVIATION, REFUTED and NOT_VERIFIABLE. Per-leaf reproduction data are evidence; they do not establish a failed scientific fixed constraint. The record declares 10 RESOLVED, 4 RESOLVED_BY_OWNER_DECISION and 1 OPEN. Its “14 resolved” claim is refuted: 6 resolved, 2 resolved by owner decision, 6 partial, 1 open.

EH98’s implemented sound scale, effective Γ, α_Γ and no-wiggle T agree with Eqs. 26, 28–31. Fixed f_b=0.02237/0.14309694 derives from the declared Planck comparator ω_m=0.315·0.674², consistent with 1G-A/B. It is not a literal zero-baryon model and not a verified universal Boltzmann correction.

## 8. Implementation, tests and mutation testing

All 19 historical invalid constructions reject. Five new coherent-metadata replacements are accepted as strict JSON:

| Tamper | Stored | Recomputed/required |
|---|---|---|
|A_s×4|σ 0.649389310315|σ 1.298778620631|
|Resolved radius×2|σ 0.649389310315|σ 0.402178283454|
|Nodes 33/17|relative change 6.037e-11|factory refuses 9.387e-3|
|Seed radius×2|σ_s 0.003397573500|0.002637733511|
|target_premise_rms|999|0.065051629333|

For identity 1e-12 checks, recomputation is in the same process; this audit found no cross-library failure in the tested factories. That does not validate Windows or bind integral results to changed inputs. Missing diagnostic/name and nonfinite probes reject.

The 99 orthant comparisons include ρ of either sign within 1e-12 of ±1, unequal thresholds, c=-100 and c1>12. Independent adaptive conditional-normal integration uses ±14 tails, epsabs = 2e-14/epsrel = 2e-13. Maximum discrepancy 6.66e-15. Original 21 unique probes: 20 return with maximum analytic error 5.18e-14, one start-count 800 refuses when necessary doubling exceeds 1024. ±12 Gaussian tails are negligible at the allowed absolute tolerance; transition-edge panels matter near singular ρ. Empirical agreement of two refinements is not a general mathematical error guarantee.

Baseline 35 H tests pass. Original 8 mutants all die; 15 added mutants give total 23, 17 killed, 6 survived. Survivors: background consistency, interval target_inside, centre split with intact edges, Frechet defensive check, docstring-only derivative sign, output half-unit rounding contribution. Additional independent probes detect the first, second and Frechet omission; they are not coverage of unchanged project tests. The centre-split deletion remains accurate across 99 cases and is benign in that tested scope. The executable PBS sign counterpart is killed.

For script mutants N10–N14, separately run H evidence: unsquared rescale kills constant-share gates; normalization removal triggers MC-test/PSD refusal; λ²→λ kills MC-test/linear-limit gates; rounding +1 deletion survives; cutoff×0.9 fails premise gates. Existing tests that import the evidence script are coupled implementation regression checks, not independent scientific oracles; imports alone write no artifact. They are useful but insufficient to test the unimplemented shared-constraint equality.

## 9. Documentation consistency

Proposed, constant-share interval, formal extrapolation, heuristic prior and signed surrogate labels appear in the detailed corrected sections. Summary median error-control qualification remains incomplete (DF6). The positive-law common-covariance assertion appears in report, inventory, remediation, script metadata, README and CLAUDE (DF1). Section 8 is current revised text despite its note that the self-check was originally written before the audit; unrequalified retired assertions there remain active contradictions (DF3).

Date-limited historical publication statements can remain. Add a successor instead of rewriting frozen records or pretending a commit knew a later push. No new status reading or observational grant follows from a successful numerical reproduction.

## 10. New findings in detail

### GH-DF1 — Nonnegative laws do not share the declared unconditional wall-density covariance

Severity: `MEDIUM-HIGH`. Area: `SCIENCE`. Related: `GH-F5`. Resolution: `CORRECTION`.

Conditional wall-mass normalization is different in the two laws and rescales their unconditional wall-density covariance. Matching the latent Gaussian field is not matching the declared density field.

**Evidence:** science_independent_delta_science.json, science_independent_formula_checkpoint.md.

**Consequence:** The added construction does not prove nonuniqueness while holding all stated constraints fixed; its computed positive-density examples remain valid under weaker constraints.

**Locations:** reports/phase1g_h_global_variance_closure.md: 122-127, 790-796, 813-821; reports/phase1g_h_audit_remediation.md: 93-108; reports/phase1g_h_global_variance_closure_inventory.json:two_phase_covariance.*.nonnegative_lognormal_pairs.shared_constraints; scripts/phase1g_h_global_variance_closure_numerics.py:lognormal kernels and shared_constraints; README.md: 179-183; CLAUDE.md: 514-517.

**Suggested correction:** Declare exactly whether the fixed spectrum is the pre-normalization carrier, the contrast normalized to its unconditional mean, or the conditionally normalized wall density. Narrow the proof to the first if intended, or construct laws with the actually declared density covariance held fixed. Remove the stronger conclusion until that is demonstrated; report both normalizers and the free smoothing/calibration choices.

### GH-DF2 — Records can retain numerical results after changing their scientific inputs

Severity: `MEDIUM`. Area: `IMPLEMENTATION`. Related: `GH-F9`. Resolution: `CORRECTION`.

Public frozen records check internal algebra but do not bind every result/diagnostic to the declared spectrum, radius, seed radius or grid. target_premise_rms is only checked for finiteness and positivity.

**Evidence:** implementation_probes_results.json, implementation_nodes_factory_check.json.

**Consequence:** An accepted strict-JSON output can assert sigma=.649389 for a spectrum whose factory result is 1.298779, or a converged 33/17-node result whose factory refuses.

**Locations:** src/timescape_fsigma8/global_variance.py:EvaluatedVoidShare.__post_init__; src/timescape_fsigma8/global_variance.py:ConditionalGlobalLinearSigma.__post_init__; src/timescape_fsigma8/global_variance.py:AdmissibleGlobalLinearInterval.__post_init__; reports/phase1g_h_audit_remediation.md:GH-F9.

**Suggested correction:** Bind results to the full input/provenance tuple using recomputation or a sealed validated factory record. Recompute the target premise result, validate grid metadata, and add replacement tests for each accepted case. Do not describe algebra-only checks as complete input-integral validation.

### GH-DF3 — Current self-audit retains claims retired by the remediation

Severity: `MEDIUM`. Area: `DOCUMENTATION`. Related: `GH-F6`. Resolution: `CORRECTION`.

Section 8 still says the anchor corrects the transfer function only, correlated-law effects are double counting, and the full S1 is required. These are not explicitly superseded quotations.

**Evidence:** documentation_results.md, documentation_lexicon_classification.json.

**Consequence:** The current report contradicts its corrected sections and the resolution register overstates complete resolution.

**Locations:** reports/phase1g_h_global_variance_closure.md: 882-885, 893-894; reports/phase1g_h_audit_remediation.md: 14 findings resolved; reports/phase1g_h_audit_remediation_inventory.json:finding_resolution.

**Suggested correction:** Update or expressly supersede the current self-audit: empirical normalization at fixed closure; masked-wall/cross-covariance mechanism; wall-density freedom does not select full S1. After correcting DF1/DF2, update the resolution counts to independently verified outcomes.

### GH-DF4 — Integrated RMS closeness is presented as a maximum propagator error bound

Severity: `LOW-MEDIUM`. Area: `SCIENCE`. Related: `GH-F4`. Resolution: `CORRECTION`.

G_eff/G(0)-1 is a weighted scalar statistic. It is not sup_k|G(k)/G(0)-1| over the noncompact top-hat support, and it does not bound both target and homogeneity windows.

**Evidence:** documentation_results.md, science_independent_delta_science.json.

**Consequence:** The asserted 0.12% interval-placement accuracy for near-constant PBS kernels is not derived, though constant-share H15 and the step counterexample are correct.

**Locations:** reports/phase1g_h_global_variance_closure.md: 598-609.

**Suggested correction:** Call the quantity an integrated RMS deviation; remove the pointwise maximum and interval-placement guarantee or derive and verify a bound for both window integrals.

### GH-DF5 — Tests do not exercise several new defensive invariants and the output rounding contribution

Severity: `LOW-MEDIUM`. Area: `TESTS`. Related: `GH-F9`. Resolution: `CORRECTION`.

Six mutants survive the unchanged 35 H tests or applicable gates; three reveal defensive-coverage omissions and removing the output half-unit budget passes all evidence.

**Evidence:** implementation_mutation_results.json, implementation_defensive_results.json, implementation_findings.md.

**Consequence:** Passing 35 tests/32 gates is limited evidence for complete record validation and error-budget coverage. Survivors are not all scientific failures.

**Locations:** tests/test_phase1g_h_global_variance.py:test_records_reject_tampering; tests/test_phase1g_h_global_variance.py:test_gh_f11_reference_rounding_budget; scripts/phase1g_h_global_variance_closure_numerics.py:E reference gate.

**Suggested correction:** Add adversarial tests for growth-background consistency, interval target_inside, invalid-quadrature Frechet refusal and a rounding-budget boundary requiring the output term. Exercise actual evidence helpers. Treat centre-split removal with intact transition edges as a tested benign survivor and docstring-only sign reversal as documentation coverage.

### GH-DF6 — Median-seed summary qualifier is incompletely propagated

Severity: `LOW`. Area: `DOCUMENTATION`. Related: `GH-F8`. Resolution: `CORRECTION`.

README and CLAUDE identify a heuristic median seed but omit that its epsilon lies below an adopted threshold without a controlled error estimate beside the quoted primary values.

**Evidence:** documentation_results.md.

**Consequence:** Summary readers can infer more physical control than the detailed report establishes.

**Locations:** README.md: 172-175; CLAUDE.md: 505-507.

**Suggested correction:** Put the epsilon-threshold and no-controlled-error qualifier beside the median headline values, retaining heuristic prior and the W09 formal-extrapolation qualifications.

### Remediation errata

- GH-DE1 (reports/phase1g_h_global_variance_closure.md:813): “Both pairs share the stated constraints between their two laws”. Correct reading: The latent/pre-normalization covariance is shared; the conditionally normalized wall-density covariance differs by m^(-2).
- GH-DE2 (reports/phase1g_h_global_variance_closure.md:883-884): “The anchor corrects the transfer function at Planck parameters only”. Correct reading: The post-hoc multiplier is empirical normalization at fixed closure; rescaling input and recomputing PBS is a distinct variant, neither verified transfer recalibration.
- GH-DE3 (reports/phase1g_h_global_variance_closure.md:893-894): “S1 goes beyond [GM]'s flat walls (but is required, Sec. 3.3)”. Correct reading: The cap requires wall-density freedom under the stipulated exact-empty-void/early-field assumptions; it does not uniquely require all of S1.
- GH-DE4 (reports/phase1g_h_global_variance_closure.md:598-599): “the propagator varies by at most 0.12% across the R8 window”. Correct reading: The reported quantity is the integrated G_eff/G(0)-1. It is not a pointwise maximum or a proven two-window interval bound.

- GH-DE5 (reports/phase1g_h_global_variance_closure.md:882): “In the nonlinear covariance the double counting is explicit (law II).”. Correct reading: The change is in the masked wall auto-variance with a positive integrated cross term; double counting is not the demonstrated mechanism.

- GH-DE6 (reports/phase1g_h_audit_remediation.md:139): “re-validate every field in”. Correct reading: The checks reject the historical probes but do not bind all numerical results and diagnostics to changed scientific inputs.

## 11. Owner recommendations

- H-OD1: keep the formal tangent as a named research proposal; prefer convention (c) explicitly, with (a) as comparison, without claiming the actual material-domain ensemble statistic.
- H-OD2: choose no physical reference value yet. The median is a heuristic prior without controlled physical error; W09 is a nonperturbative formal extrapolation without scale separation. The conditional constant-share interval is usable only in its stipulated class.
- H-OD3: defer scientific-token promotion. Preserve `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC=NOT_DERIVED` and all five `NOT_GRANTED` authorizations.
- H-OD4: keep the runtime experimental. Correct DF2, add the defensive and boundary tests in DF5, and obtain independent validation before any package-runtime promotion. Direct A_s values should remain primary; empirical normalization and PBS reclosure remain separate research conventions.
- H-OD5: publication of this report is separate from merge/freeze/PR/tag decisions. Do not integrate or freeze the remediation while DF1/DF2 and the documentary consistency fixes remain. The audit can be published for review on its designated separate branch if explicitly authorized.
- GH-F15: obtain the owner’s direct confirmation of the two verbatim earlier approvals. Then record `CONFIRMED_OFF_REPOSITORY_RECORDING_PENDING` until a dated successor is committed. Without confirmation, retain `OPEN_OWNER_CONFIRMATION`.
- Publication successor: date 2026-10-08; record old/new refs, d4d693d→ 89cb041, chain 816dd00/c1b4482/89cb041, approved scope and actual no PR/merge/tag/release state; distinguish remotely verified events from off-repository authorization. This is a recommendation, not an existing owner confirmation.

## 12. Limits

- OpenAI Codex is the same auditor family as the first audit, not an independent institution. Independent science and implementation workstreams were used, with no contact with the Claude author or access to its conversation.
- Prior delta progress described a blind checkpoint, but that checkpoint was unavailable in this resumed workspace. This continuation records a new formula checkpoint and independent calculations after report/expected-value exposure; it does not claim a fresh blind run or recover an unverified hash.
- Linux CPython 3.12.14 and 3.11.17 were available. Windows CPython 3.14.3/3.11.9 was not run, so the owner Windows gate is unmet.
- Jupyter network-interface discovery failed with EPERM. Unmodified oracle source and sampling cells were executed through a temporary in-process NotebookClient adapter; no scientific equation, solver choice, warning policy or original notebook was changed. This does not certify the Jupyter transport.
- No CAMB/CLASS/Boltzmann recalibration, gravitational dynamics, transported material-domain ensemble, light-cone/tracer mapping, observational likelihood or observational authorization was derived.
- Remote snapshots establish current refs/objects, not the complete history of transient remote actions. SSH signatures verify against embedded keys without independently establishing owner identity trust.
- D1–D4 text choices match first-audit alternatives, but absent chat point-to-decision correspondence and earlier author approvals are not independently verified.
- Kernel Monte Carlo checks sample six four-variate Gaussian laws; no spatial lattice Monte Carlo was performed. Numerical convergence checks are empirical rather than a universal rigorous orthant-error theorem.
- All 23 mutants rerun the 35 H tests; only script mutants N10–N14 additionally rerun H evidence. No full-suite mutation campaign is claimed.

- The original phase-task prompt was not attached in this handoff. The delta instruction and repository records provide the authorization/context used here; unseen author chat and the abandoned construction described by the author were not independently verified.

## 13. Primary sources and hashes

Rehashed all seven exact primary source files/archive from the first-audit cache. All match the H inventory; cache reuse is disclosed. The files are not bundled.

| Source | Version | SHA-256 |
|---|---|---|
|EH98|astro-ph/9709112v1|`5f2ac6b413df8b738c95f6650152b7e82d7c36f6d9b3a618da540e9739dce17f`|
|GM|arXiv:2511.17160v2|`f9cadfa03ecc9a74b0a8f432ae4b13422daeb219f253756bcd877b4b75077c59`|
|JLH13|arXiv:1304.6087v2|`cf6fc77a31b395138ac3a027d008698556534e81cfb27c39853d3a99c7b07c4e`|
|NW15|arXiv:1410.3470v2|`5688c9ac7123a5c2ef3508e39cb3134c2fe9e3d5e56996a4d4a4d101d7b74673`|
|SvdW04|astro-ph/0311260v1|`4b7ad599f54b3199e0448df1c2eecf4e724401e9ffda7b0f50a3efe7fecdb79b`|
|W07|arXiv:0709.0732v2|`221662c987e454729ef8202c87fa697c5882b5b7daaecdedb50a7cba8ffe6cd8`|
|W09|arXiv:0909.0749v2|`2b0324d127440e9a053a7cb37102d7655cca228a63cd2222843e879989b4b531`|

GM tracker 5.4–5.6 and flat-wall premise; W09 homogeneity and size premise; EH98 Eq. 26, 28–31; SvdW conditional barrier shift; JLH13 volume-mapping/shell-crossing context were read. Source conventions and the non-observational firewall remain those of the prescribed checkpoints.
