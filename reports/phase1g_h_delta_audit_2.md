# Phase 1G-H — second independent delta audit of the remediation

Classification: `INDEPENDENT_DELTA_AUDIT` (report-only). Date: 2026-10-08.
Auditor: Claude (Anthropic), in a separate Claude Code cloud session.

**Independence caveat.** The author of Phase 1G-H and of both remediations is
also a Claude session. This audit therefore comes from the **same model
family as the author**; it is not the system of the two earlier audits
(OpenAI Codex). It had no contact with the author and no access to the
author's conversation. Its independence is procedural: a separate session,
an own derivation and own code with different numerical methods, and a blind
checkpoint committed before the author's full-precision numbers were read
(Sec. 2). It cannot rule out shared blind spots of the model family; a
cross-family check remains the owner's option (Sec. 11).

Audited head: `226e52d2e4157d0130b2a9dfaffd71834c6017d9`, tree
`4db0f0f75a91321ae37b7cd7d7c6381c0c76c5c9` (branch `ccr-555e67be-u11yht`,
no drift). Delta base: `5c325e1fd05b343f6d5e93f931038794de4373a2`, tree
`a5b810e81d125827a17a9cf87b013ead51232080` (the delta-audit commit; parent
`89cb041`). Intermediate code commit: `248a06bfeb655337bc499607180c49008b5f34ea`,
tree `cb57dcf23323939f8e8260bbb303b0ec2221c185`.

Environment: Linux (kernel 6.18), CPython 3.13.16 (NumPy 2.5.3, SciPy 1.18.1,
matplotlib 3.11.2, pytest 9.1.1) and CPython 3.11.17 (NumPy 2.4.6, SciPy
1.17.1, matplotlib 3.11.2, pytest 9.1.1); `OPENBLAS_NUM_THREADS=1`,
`-B -W error`, no warning suppression. The pinned upstream clone
(`590c6fd5332acb15f5683ebf392a0d7ce54983c5`, notebook SHA-256
`628c4412…ea2a`) was used read-only. Windows was not available.

Companions: [`phase1g_h_delta_audit_2_inventory.json`](phase1g_h_delta_audit_2_inventory.json);
evidence [`phase1g_h_delta_audit_2_evidence/`](phase1g_h_delta_audit_2_evidence/).

## 0. Summary

**Overall: `ACCEPT_WITH_CORRECTIONS`.** Readiness token:
**`NO_SCIENTIFIC_BLOCKER_READY_FOR_OWNER_DECISION_AFTER_LOW_CORRECTIONS_P7_RECORD_AND_WINDOWS_GATE`.**
The second remediation resolves every finding and erratum of the delta
audit. No HIGH, MEDIUM-HIGH or MEDIUM finding remains. What is left is a
recording task (today's push, P7, and the direct GH-F15 confirmation), two
LOW corrections and four INFO items. The owner's Windows gate has still
never run on a 1G-H tree. Merge and freeze remain owner decisions (H-OD5).

| Area | Verdict |
|---|---|
| PROVENANCE | `ACCEPT` |
| GOVERNANCE | `ACCEPT_WITH_CORRECTIONS` |
| SCIENCE | `ACCEPT` |
| NUMERICS | `ACCEPT` |
| IMPLEMENTATION | `ACCEPT` |
| TESTS | `ACCEPT_WITH_CORRECTIONS` |
| DOCUMENTATION | `ACCEPT_WITH_CORRECTIONS` |
| TASK_COMPLIANCE | `ACCEPT` |

| Delta finding | Outcome | Reason |
|---|---|---|
| GH-DF1 | `RESOLVED` | Shared constraints narrowed to f_v0, P11(r), the latent carrier law and the wall normalisation E[ψ \| wall] = 1 at every current location; m_II, 1/m_II² and ⟨C_W − 1⟩ reproduce blind to ≤ 1.5×10⁻¹⁰; (H25) is exact |
| GH-DF2 | `RESOLVED` | All five accepted replacements are refused; of 27 further probes, only tolerance-looser, metadata and type substitutions pass, none with a changed scientific input |
| GH-DF3 | `RESOLVED` | §8 states the current readings; the dated note supersedes the "14 resolved" count; no retired claim is active |
| GH-DF4 | `RESOLVED` | "Integrated", no pointwise or placement bound; −0.0799% … −0.1242% over six cases reproduces "−0.08% to −0.12%" |
| GH-DF5 | `RESOLVED` | The four requested tests exist and kill their mutants; new coverage gaps are a separate finding (GH-D2F2) |
| GH-DF6 | `RESOLVED` | Qualifier beside every README/CLAUDE median value |

| Erratum | Outcome |
|---|---|
| GH-DE1 | `APPLIED` (§6.3 paragraph and Reading) |
| GH-DE2 | `APPLIED` (§8 "Circular normalisation") |
| GH-DE3 | `APPLIED` (§8 "Undeclared dependences"; §3.3 consistent) |
| GH-DE4 | `APPLIED` (§5.2 and §5.3) |
| GH-DE5 | `APPLIED` (§8 "Mass and volume") |
| GH-DE6 | `APPLIED_EQUIVALENT` (dated status note; historical sentence kept) |

Original findings: GH-F1, GH-F2 `RESOLVED_BY_OWNER_DECISION`; GH-F3 … GH-F14
`RESOLVED` (GH-F4 … GH-F9 now completed); GH-F15 `RESOLVED_OWNER_CONFIRMED`
(the owner confirmed the two recorded push approvals directly to this auditor
on 2026-10-08, «Confermo le due approvazioni di push registrate (GH-F15)»,
and P4 records the earlier confirmation in the tree).

New findings: 2 LOW (GH-D2F1 governance, GH-D2F2 tests), 4 INFO (GH-D2F3 …
GH-D2F6). Two remediation statements are recorded as errata (GH-D2E1,
GH-D2E2).

Reproduction: full suites **1178 passed, 0 skipped, 0 failed** on both
interpreters after regenerating every oracle and historical artifact; 36/36
evidence gates on both; 3201 numeric leaves identical across interpreters;
the author's artifact SHA-256 `91aaca79…9884` reproduced byte for byte at
`248a06b`; runner 0.810772 / 1.121363 / 0.918157; validator `PASS` (53 JSON
with this inventory); tolerance audit 739 comparisons, 0 missing; the seven
primary sources re-downloaded and re-hashed.

**Not done.** No existing file was changed, nothing was pushed, no token or
authorisation was touched, no PR, tag, freeze, merge or release, and no D v2
reference was created. Not run: Windows (the owner's gate). Not
re-audited: the unchanged parts of 1G-H beyond regression checks, and the
frozen phases 1G-A … 1G-G.

## 1. Object and hashes

| Commit | Parent | Tree | Content |
|---|---|---|---|
| `5c325e1` (base) | `89cb041` | `a5b810e8…2080` | delta audit, 110 added files under `reports/phase1g_h_delta_audit*` |
| `248a06b` | `5c325e1` | `cb57dcf2…c185` | code: module, evidence script, phase tests |
| `226e52d` (head) | `248a06b` | `4db0f0f7…c5c9` | documentation |

`git diff --name-status 5c325e1 226e52d` lists exactly the 23 declared paths:
10 `M` (CLAUDE.md, README.md, the first remediation record and inventory, the
1G-H report, inventory and validation record, the evidence script, the module
and the test file) and 13 `A` (the second remediation record, its inventory,
its 9 logs, the publication successor and its inventory). Preserved and
verified:

- every file of the first audit and of the delta audit, byte for byte at
  `5c325e1` (no path under `reports/phase1g_h_independent_audit*` or
  `reports/phase1g_h_delta_audit.md`, `_inventory.json`, `_evidence/` in the
  diff);
- the runner `scripts/phase1g_h_global_variance_case.py` and
  `scripts/phase1g_h_configs/` (unchanged since `5c325e1`; SHA-256 equal to
  the 1G-H inventory);
- every package module other than `global_variance.py` equal to `8d3cdd0`
  (`git diff --name-status 8d3cdd0 226e52d -- src` lists only that module as
  added), including `scientific_status.py` and `lagrangian_sigma.py`.

The 1G-H inventory's seven file SHA-256 declarations match the blobs at
`226e52d`; its seven primary-source hashes match fresh arXiv downloads
(Sec. 13).

## 2. Method and blind checkpoint

Read: AGENTS.md and CLAUDE.md; the delta audit, its inventory and the evidence
named in the prompt; the first audit and first remediation as history; the
second remediation record, inventory, logs and both commit messages; the
publication successor; `git diff 5c325e1 226e52d` in full; the revised 1G-H
report in full.

**Blind order.** The model definitions were taken from the revised report
§6.1/§6.3 and from the first audit's provider. Own code
(`blind_h25_mII_cw.py`, `blind_first_panel.py`; no project import) uses:

- Owen's T for the bivariate orthants (the author uses adaptive panel
  quadrature, the delta audit 1-D QUADPACK);
- Gaussian integration by parts (Stein) for the signed-pair moments;
- exponential tilting for the lognormal kernels;
- QUADPACK Fourier (QAWO) Hankel transforms on [10⁻⁵, 80] Mpc⁻¹;
- composite Gauss–Legendre ball quadrature on [0, 2R], which contains the
  first panel by construction, checked at 4×24, 16×48 and 32×64 nodes.

The tracker and the EH98 no-wiggle provider were reused verbatim from the
first audit (`first_audit_provider.py`, same SHA-256 as its committed
`independent_numerics.py`). The checkpoint `BLIND_CHECKPOINT.md`,
SHA-256 **`c5f744e31a2a63a08c8aa0984faf6ebc9e18296e36c1cf7d7203d554162754ac`**,
was committed locally on this branch as `64116509554cc0d711660da4d81ad95c3f450a6d`
(2026-10-08 16:54:01 UTC) **before** this audit read the author's artifact,
logs, new evidence-script functions or test expectations. It is not blind to
the three-decimal values quoted in the prompt, the report and the
remediation record, which were read for the definitions; the checkpoint
states this. Only then were the author's numbers compared (Sec. 6).

Other workstreams: reproduction on both interpreters and regression against
`5c325e1`; 32 record-binding probes; a 56-mutant campaign in disposable
copies outside the tree; leaf-by-leaf reconciliation of the 1G-H inventory;
lexical search; remote state read-only (`git ls-remote`, GitHub pull-request
and release listings). Subagents were not used.

## 3. Provenance and governance

**Remote state (read-only, 2026-10-08).** `main` = `8d3cdd0`;
`ccr-555e67be-u11yht` = `226e52d`; `phase-1g-h-independent-audit` = `816dd00`;
`phase-1g-h-delta-audit` = `5c325e1`. Pull requests #1–#4 are closed and none
comes from a 1G-H branch; no release; 38 annotated tags (76 refs), every tag
object identical to the delta audit's snapshot; no
`phase-1g-d-separate-universe-growth-v2` tag or branch; no
`phase-1g-h-delta-audit-2` on `origin`.

**Publication successor, P1–P6.** Verified as remote facts: `0572e41`
descends from `8d3cdd0` through `7900374`, `fd7331f`; `d4d693d` is a child of
`0572e41`; `816dd00` has tree `759ab21d…b77a` and parent `d4d693d`;
`d4d693d..89cb041` is `816dd00`, `c1b4482`, `89cb041`; `5c325e1` has tree
`a5b810e8…2080`, parent `89cb041` and 110 added files, all under
`reports/phase1g_h_delta_audit*`; `b4abbe8` is not an object of `origin`,
as stated. The authorisations of P1, P2, P4, P5 and P6 are the owner's words
quoted from other sessions: `NOT_VERIFIABLE` here, and kept distinct from the
verified facts.

**P7, not recorded.** On 2026-10-08, after the two remediation commits, the
branch was fast-forwarded `89cb041 → 226e52d` (carrying `5c325e1`, `248a06b`,
`226e52d`); the remote head confirms it. The owner's audit handoff gives the
authorisation as «Fai push e prepara il prompt per un nuovo audit». Because
the push followed the commits, several statements in the tree that read as
current are now superseded, and the successor's table of dated statements
lists only one of them (GH-D2F1, with the full list).

**Dated note in the first remediation record.** The note is purely additive
(the diff of the record and of its inventory only inserts lines), dated,
and states that the record "is not rewritten"; every historical sentence is
intact. The delta audit asked for the resolution counts there to be updated
(GH-DF3 locations). Adding a dated note rather than a separate successor is
acceptable for an unfrozen phase. Two side effects are not stated in the
note (GH-D2F5): the record's `files_changed_sha256` describe the `89cb041`
bytes, and its GH-F5/D3 lines keep the "same shared constraints" wording
that GH-DF1 refuted.

**Plan versus the delta audit's suggested resolutions.** GH-DF1 takes the
first suggested option (narrow to the pre-normalisation carrier), reports the
normaliser ratio, and declares the free choices. GH-DF2 takes recomputation
binding, recomputes the premise rms and validates the quadrature through
recomputation. GH-DF3 … GH-DF6 follow the suggested corrections. Every
choice is inside the `suggested_resolution`. The approval «Perfetto, procedi»
is author-reported (`NOT_VERIFIABLE`).

**AGENTS.md rules, both commits.**

| Rule | `248a06b` (code) | `226e52d` (documentation) |
|---|---|---|
| 1, 3 | (H25) is a new identity, not a change of (H17)/(H18), whose text is unchanged; the radial fix is numerical (first panel, finer grid) and changes no printed value; the binding is a refactor (factories call the same pure helpers; evidence outside the pairs bitwise unchanged) | records the narrowing; no equation changed |
| 2 | (H25) cited in the `_law_summary` docstring; m_II cited to [1G-H] Sec. 6.3 / GH-DF1 (no H label; a minor gap, noted here only) | (H25) labelled in §6.1; (H1)–(H25) ranges updated in §13 |
| 4 | E[ψ \| wall] = 1, P11-weighted ⟨C_W − 1⟩, free r_s and λ calibration all explicit | same in §6.3 |
| 5 | seven new tests (Sec. 8) | — |
| 6 | no upstream code | no upstream code |
| 7 | committed locally; pushed later with the owner's approval as reported (P7) | same |
| 8 | pure helpers `_two_phase_growth_values`, `_void_share_values`, `_global_sigma_values`, `_interval_values` | — |
| 9 | `RADIAL_INTERVALS = 1440`, `radial_refinement_rel = 1e-5` ("protects the printed fourth decimal by a factor 5": checked), `h25_identity_rel = 1e-12`, `RECORD_IDENTITY_RTOL` comment extended to the binding; tolerance audit 739 / 0 missing | — |
| 10 | no `filterwarnings`, `catch_warnings` or `errstate` added; suites and evidence run with `-W error` | — |

## 4. Delta-audit findings and errata

### GH-DF1 — `RESOLVED`

- Every current location narrows the shared constraints: report §1 (verdict
  item 6) and §6.3, inventory (`two_phase_covariance.*.nonnegative_lognormal_pairs`),
  evidence metadata (`shared_constraints`, `not_shared`,
  `free_construction_choices`), README and CLAUDE. The only remaining
  "same shared constraints" phrases are in historical 2026-10-07 blocks
  (GH-D2F5).
- m_II = Q(c − κ0)/f_w, the covariance ratio 1/m_II², the law-II unmasked
  ball variance and the P11-weighted ⟨C_W − 1⟩ reproduce blind (Sec. 6).
- (H25) is exact and equivalent to (H18) at x = 0 (Sec. 6.1). "At fixed P11
  and C_W the variance is unique" is correct and, by (H25), a tautology; the
  informative content is that f_v0, P11 and the carrier law do not fix C_W,
  which the pairs show by explicit construction (Sec. 6.4).
- The ordering of the totals is an exact consequence: within a pair
  σ² = σ²_part + (1 + σ²_part)⟨C_W − 1⟩ with a common σ_part, so no assumption
  on the pair weight is needed beyond its normalisation (checked to
  ≤ 2.2×10⁻¹⁶ on every law).

### GH-DF2 — `RESOLVED`

Every public result record (`TwoPhaseGlobalGrowth`, `EvaluatedVoidShare`,
`ConditionalGlobalLinearSigma`, `AdmissibleGlobalLinearInterval`) recomputes
every result and diagnostic with the factory's pure helper and compares field
by field (`_same`: floats within `RECORD_IDENTITY_RTOL`, bools by type and
value, tuples element-wise, everything else by equality). The input-only
records (`TwoPhaseSmoothedMoments`, `HomogeneityPremise`, the closures, the
checks and the matching) carry no results.

32 probes (`implementation_binding_probes.py`):

- the delta audit's five accepted replacements (A_s ×4, radius ×2,
  quadrature 33/17, seed radius ×2, premise rms 999) are all refused with
  `GlobalVarianceContractError`;
- tolerance objects with looser tolerances and identical values are accepted
  (quadrature, seed quadrature, growth checks), and stricter ones that the
  stored result does not meet are refused. This is consistent: the record
  then truthfully carries a contract it satisfies, so it is not a gap;
- G ×2 is accepted (G cancels and the ODE diagnostics are reproduced);
- free-text provenance of the premise and matching is accepted (metadata,
  not a result);
- an equal but distinct density or spectrum object in the sigma record is
  refused by the identity contract. This is stricter than needed, but
  consistent with the project convention ("object identity is required where
  a later stage must not silently re-derive an input") and harmless for the
  factory path. `copy.deepcopy` and pickle round trips keep shared
  references and are accepted;
- `int` or `numpy.bool_` in a bool field, a string in a float field and a
  relabelled regime are refused; a sigma changed by 5×10⁻¹³ relative, inside
  `RECORD_IDENTITY_RTOL`, is refused as well, by the earlier
  `effective_propagator` invariant;
- a `fractions.Fraction` equal to the stored float is accepted and then
  fails strict JSON. This already happened at `5c325e1` (GH-D2F4, INFO).

Every refusal raises `GlobalVarianceContractError`; none raised another
exception type. Converting `GlobalVarianceNumericalError` into a contract
error is appropriate: a record whose inputs cannot reproduce a valid result
is an invalid record, and the message keeps the cause. Recomputation calls
pure value helpers, never the record classes, so there is no recursion. The
cost is one extra evaluation per construction (phase file 9–11 s here).

### GH-DF3 — `RESOLVED`

§8 now states the empirical post-hoc normalisation and the distinct
reclosure (DE2), the masked-wall mechanism (DE5) and the scope of the cap
(DE3). The "14 findings are resolved" count is superseded by the dated note
(DE6). Lexical search (Sec. 9): no retired assertion is active.

### GH-DF4 — `RESOLVED`

"At most 0.12%" and "−0.09%" are gone; §5.2 and §5.3 call `G_eff/G(0) − 1` an
integrated, spectrum- and window-weighted average and withdraw the pointwise
and placement readings. From the artifact, the [W09] seed gives −0.0862%,
−0.1085%, −0.1242% ([GM] a/b/c) and −0.0898%, −0.0799%, −0.0955% ([NW15]),
hence "−0.08% to −0.12%". The 1G-F median seed gives −0.0037% … −0.0053%
("−0.004% to −0.005%"), [SvdW04] −17.4% … −23.9% ("−17% to −24%"). The
corrected range appears at all three loci (report §5.2, §5.3; remediation
record §0).

### GH-DF5 — `RESOLVED`

Requested tests now exist: growth background consistency, interval
`target_inside`, Fréchet and symmetry refusals via a monkeypatched
quadrature, and the output half unit (`e_reference_rounding_budget` with a
boundary case). The tamper test matches each invariant's message. The
corresponding mutants are killed (Sec. 8). Coverage of the *new* quantities
is incomplete: that is GH-D2F2, not a residue of GH-DF5.

### GH-DF6 — `RESOLVED`

README §1G-H and CLAUDE §1G-H put "below the adopted ε = 1 threshold, with no
controlled error estimate" beside the median values 0.811 / 0.816, with
"heuristic seed-scale prior" and the [W09] "formal extrapolation".

### Errata GH-DE1 … GH-DE6

- **GH-DE1** `APPLIED`: §6.3 now reads "Both laws share f_v0, P11(r), the
  latent carrier law … They do **not** share the conditionally normalised
  wall density itself … its unconditional covariance is law I's divided by
  m_II²", and the Reading paragraph says that the result "does not show
  non-uniqueness at a fixed conditionally normalised wall-density
  covariance".
- **GH-DE2** `APPLIED`: "The post-hoc factor is an empirical output
  normalisation at fixed closure; rescaling the input spectrum and
  recomputing the PBS share is a distinct variant; neither is a verified
  transfer recalibration."
- **GH-DE3** `APPLIED`: "the flat-wall cap requires wall-density freedom if
  exact empty voids and the early Gaussian field are kept, but it does not
  select the whole of S1".
- **GH-DE4** `APPLIED`: "it is not a pointwise bound on `G(k)/G(0) − 1` …
  and it does not bound the premise integral. No accuracy is derived for the
  position of these closures relative to the interval".
- **GH-DE5** `APPLIED`: "law II changes the masked wall auto-variance, with a
  positive integrated wall–partition cross term …; double counting is not the
  mechanism".
- **GH-DE6** `APPLIED_EQUIVALENT`: the sentence "re-validate every field in"
  stays as history (first remediation record, l. 146). The dated note states
  that the records "re-validated their fields but did not bind their results
  to their inputs (erratum GH-DE6, finding GH-DF2)".

### Radial quadrature (the four `VERIFIED_WITH_DEVIATION` claims)

The ball integrals include the first panel, and 1440 Simpson intervals carry
a refinement gate. Independent Gauss–Legendre values (32×64 nodes, converged
to 1.3×10⁻¹³) give signed law-II wall moments
E[B²] = 7.825229276×10⁻⁴ ([GM]) and 3.553181863×10⁻³ ([NW15]), against the
author's 7.82522965×10⁻⁴ and 3.55318191×10⁻³ (4.8×10⁻⁸ and 1.4×10⁻⁸
relative).

- The first panel alone contributes a fraction 8.35×10⁻⁴ ([GM]) and
  3.73×10⁻⁴ ([NW15]) of these moments. Its pair weight, 7.2×10⁻⁸, is the old normalisation deficit
  (0.99999993); the new norm is 1 + 9.3×10⁻¹³.
- The half-resolution estimate (8.3×10⁻⁷ / 1.0×10⁻⁶) overstates the true
  error of the 1440-interval rms (≤ 2.4×10⁻⁸) by a factor of about 40. The
  gate is adequate as a conservative indicator, but it is empirical and not a
  bound.
- No printed value changes; the moments moved by 1.276×10⁻³ / 6.64×10⁻⁴
  relative, every rms by ≤ 6.38×10⁻⁴ and every total by ≤ 5.06×10⁻⁵, as
  stated.

All four claims are now `VERIFIED`.

## 5. Final status of GH-F1 … GH-F15

| Finding | Final status | Basis |
|---|---|---|
| GH-F1 | `RESOLVED_BY_OWNER_DECISION` | D1, unchanged |
| GH-F2 | `RESOLVED_BY_OWNER_DECISION` | D2, unchanged |
| GH-F3 | `RESOLVED` | no regression (report §1, §7 unchanged in substance) |
| GH-F4 | `RESOLVED` | completed by GH-DF4 |
| GH-F5 | `RESOLVED` | completed by GH-DF1: the pairs are stated at a fixed carrier law, with m_II and (H25) |
| GH-F6 | `RESOLVED` | completed by GH-DE2 |
| GH-F7 | `RESOLVED` | completed by GH-DE3; §3.3 and §8 agree |
| GH-F8 | `RESOLVED` | completed by GH-DF6 |
| GH-F9 | `RESOLVED` | completed by GH-DF2 and GH-DF5; INFO residue GH-D2F4 |
| GH-F10 | `RESOLVED` | orthant mutants N6, N7, M7 killed; N5 benign as before |
| GH-F11 | `RESOLVED` | the budget's output term is now tested (N13 killed) |
| GH-F12 | `RESOLVED` | EH98 provider unchanged; no regression |
| GH-F13 | `RESOLVED` | display values unchanged |
| GH-F14 | `RESOLVED` | F/G successor unchanged |
| GH-F15 | `RESOLVED_OWNER_CONFIRMED` | owner's direct confirmation to this auditor, 2026-10-08: «Confermo le due approvazioni di push registrate (GH-F15)»; P4 in the tree. Recording of this direct confirmation: Sec. 11 |

## 6. New science: blind reconstruction

### 6.1 (H25)

With empty voids (x = 0), `ρ/⟨ρ⟩ = χ_w ψ/f_w`. Normalising on the walls,
`E[ψ | wall] = 1`, gives `E[χ_w ψ] = f_w`, so `δ = χ_w ψ/f_w − 1` and

```text
1 + ξ_δ(r) = E[χ1 χ2 ψ1 ψ2]/f_w² = P11(r) C_W(r)/f_w².
```

Writing ψ = 1 + δ_w and using `E[χ δ_w] = 0` gives
`E[χ1χ2ψ1ψ2] − f_w² = (P11 − f_w²) + E[χ1χ2 δ1δ2] + 2 E[(χ1 − f_w)χ2 δ2]`.
This is (H18) at x = 0 (α = a_w = 1/f_w). The identity is exact for every
conditionally normalised law, signed or nonnegative. The author's derivation
in §6.1 is correct.

Averaging over the ball with a unit-normalised pair density gives
`σ² = σ²_part + (1 + σ²_part)⟨C_W − 1⟩`, with ⟨·⟩ the P11-weighted pair
average. Within a pair σ_part is common, so the totals are ordered exactly
as ⟨C_W − 1⟩.

### 6.2 Normaliser m_II

By tilting, `E[e^a χ] = e^{Var a/2} Q(c − κ0)` with κ0 = Cov(g, a) at one
point. So `E[e^a | wall] = e^{Var a/2} Q(c − κ0)/f_w` and
`m_II = Q(c − κ0)/f_w`, with m_I = 1. The unconditional covariance of
ψ = e^a/E[e^a | wall] is `(e^{a(r)} − 1)/m²`.

### 6.3 Values (convention (b), 32×64 Gauss–Legendre)

Lognormal pairs:

| Scenario | r_s (Mpc) | λ | m_II (audit) | 1/m_II² | ⟨C_W − 1⟩ I | ⟨C_W − 1⟩ II | total I | total II | II / I | max rel. diff. to author |
|---|---|---|---|---|---|---|---|---|---|---|
| [GM] | 1 | 0.813736671 | 2.869413475 | 0.121454534 | 0.786920194 | 0.837693201 | 0.988581428 | 1.016599945 | 1.028342144 | 1.5e-10 |
| [GM] | 2 | 0.869535109 | 2.139808561 | 0.218398755 | 0.751490945 | 1.097277234 | 0.968550187 | 1.149223553 | 1.186540014 | 5.9e-11 |
| [GM] | 4 | 0.998433754 | 1.623350652 | 0.379468142 | 0.725311249 | 1.277631961 | 0.953478193 | 1.232997950 | 1.293157998 | 5.0e-11 |
| [NW15] | 1 | 0.785149919 | 2.474113488 | 0.163365658 | 0.840794362 | 0.697655402 | 1.005219293 | 0.924193338 | 0.919394747 | 1.4e-10 |
| [NW15] | 2 | 0.839193026 | 2.104325108 | 0.225826199 | 0.797525865 | 0.887005538 | 0.981432191 | 1.030017681 | 1.049504684 | 5.7e-11 |
| [NW15] | 4 | 0.949341994 | 1.668578791 | 0.359175382 | 0.766158582 | 1.115836140 | 0.963820858 | 1.144927517 | 1.187904897 | 4.5e-11 |

Signed pair:

| Scenario | ℓ (Mpc) | μ (law II) | law | σ_wall | cross | total | ⟨C_W − 1⟩ | E[B²] | max rel. diff. to author |
|---|---|---|---|---|---|---|---|---|---|
| [GM] | 0.291721008 | 5.004606728 | I | 0.914584073 | 0 | 0.971082379 | 0.755929586 | 5.785738023e-02 | 7.4e-10 |
| [GM] | 0.291721008 | 5.004606728 | II | 0.106363541 | 0.036477473 | 0.392845562 | 0.043189407 | 7.825229276e-04 | 4.8e-08 |
| [NW15] | 0.598732248 | 3.788835878 | I | 0.929622131 | 0 | 0.977941852 | 0.791264148 | 1.202349071e-01 | 4.1e-10 |
| [NW15] | 0.598732248 | 3.788835878 | II | 0.159808504 | 0.049911950 | 0.409418695 | 0.069083113 | 3.553181863e-03 | 1.4e-08 |

Of 128 compared quantities the largest discrepancy is 4.8×10⁻⁸ relative,
on the small signed law-II wall moment, the integral most sensitive to the
k_max = 80 Mpc⁻¹ ringing of the unsmoothed carrier. Every m_II agrees to
≤ 2×10⁻¹¹ and every lognormal quantity to ≤ 1.5×10⁻¹⁰
(`blind_vs_author_comparison.txt`). The declared ranges reproduce:

- m_II = 2.869 / 2.140 / 1.623 ([GM]) and 2.474 / 2.104 / 1.669 ([NW15]);
- 1/m_II² 0.121–0.379 (m_II² 2.64–8.23, "2.6–8.2");
- ⟨C_W − 1⟩ 0.756 / 0.043 and 0.791 / 0.069 (signed), 0.725–0.841 (law I)
  and 0.698–1.278 (law II);
- unmasked law-II ball variance 0.0851 ([GM], r_s = 1 Mpc).

### 6.4 Assessment of the reading

1. **(H25) and triviality.** (H25) makes "unique at fixed P11 and C_W" a
   tautology, and the report says so. The narrowed reading has content: the
   variance is fixed by f_v0, P11, the carrier law *and* C_W, and the pairs
   prove by explicit construction that the first three do not fix C_W. This
   is an existence proof for this construction family. Its size and sign
   (−8% to +29%) depend on the free r_s and λ calibration, as the report
   states.
2. **Usefulness for 1G-E/F.** Under mask–carrier independence (law I, the
   1G-E E3 case), f_v0, P11 and the carrier law *do* fix C_W (C_W − 1 = ξ
   for the signed law, e^{λ²ξ_s} − 1 for the lognormal one), and the total
   is unique. The pairs therefore show that the 1G-E/F inputs fix the hybrid
   variance only together with a specification of the mask–carrier
   dependence (κ0, κ(r)), of which E3 is one choice. This formulation is
   sharper than "the joint law of geometry and density" and identifies what
   a closure must supply (GH-D2F6, recommendation only). §6.2 already calls
   E3 "an assumption about the joint law", so the two readings agree.
3. **Ordering of the totals.** Exact, with no assumption on the pair weight
   beyond normalisation (Sec. 6.1).

## 7. Numbers and reproduction

| Check | Result |
|---|---|
| Full suite, CPython 3.13.16, `-W error`, inputs regenerated | **1178 passed, 0 skipped, 0 failed** (236 s) |
| Full suite, CPython 3.11.17, same | **1178 passed, 0 skipped, 0 failed** (234 s) |
| Full suites repeated on this audit's final tree | **1178 passed, 0 skipped, 0 failed** on both (238 s / 235 s) |
| Regenerated inputs | upstream notebook executed through the normal Jupyter transport (no EPERM here), the three oracles, `compare_to_oracle`, clean/barotropic validators, 1D-B, 1D-D (480 s) and the owner-decisions Monte Carlo (634 s, 124/124 gates); after regeneration no test is skipped, consistent with the author's 32 recorded skip causes |
| Phase tests | 42 passed |
| Evidence, 3.13.16 with figures, at `226e52d` | 36/36 gates; printed summary identical to the author's log except the hash line |
| Evidence, 3.11.17 `--no-figures` | 36/36 gates; 3201 numeric leaves identical to 3.13 (max difference 0) |
| Evidence at `248a06b`, 3.13.16 | artifact SHA-256 **`91aaca79ad0d0d86ad3208c8cd854e9d03839ef1f8c2d0026ff7a5cf8ff89884`**, byte-identical to the author's (at `226e52d` only `environment.git_head` differs) |
| Regression `5c325e1 → 226e52d`, same interpreter (both) | Inside the pairs: 156 numeric leaves changed (140 beyond round-off), 4 text, 6 renamed, 106 added. Outside: 16 added (two `G_ode_cross_check`, two gate definitions, 12 gate leaves) and 3 changed gate read-outs of pair quantities. Max change 1.27×10⁻³ relative. The declared "outside bitwise identical; 130 changed, 6 renamed, 108 added" holds in substance but not literally (GH-D2E1) |
| Delta audit's saved evidence | `evidence_py311.json` and `evidence_py312.json` of `89cb041` are leaf-for-leaf identical (3099 numeric leaves, difference 0) to this audit's 3.11 / 3.13 runs at `5c325e1` |
| Runner | 0.810772, 1.121363, 0.918157 |
| 1G-H inventory | 1193 numeric leaves of `results`, `anchoring`, `two_phase_covariance`, `ensemble_vs_tangent_example` match the artifact within half a unit of the last printed digit (1187 by the delta audit's path rules, 6 radial-quadrature leaves by hand); 0 deviations |
| Validator 1F-C-R | `PASS`, 52 JSON before this inventory, 53 with it |
| Tolerance audit | 739 comparisons, 0 without tolerance |
| `git diff --check` | clean for `5c325e1..226e52d` and for this audit's tree |

Claims registry: 253 entries in the inventory (`claims`, `claim_counts`):
248 `VERIFIED`, 2 `VERIFIED_WITH_DEVIATION`, 3 `NOT_VERIFIABLE`, 0 `REFUTED`.
They comprise 128 blind science comparisons, the inventory reconciliation,
72 gate re-runs and 52 specific statements. The two deviations are the
regression count (GH-D2E1) and the "about 80 s" run time. The three
`NOT_VERIFIABLE` entries are the off-repository authorisations, the gates
being declared before their first evaluation, and the construction cost
(timing under parallel load).

## 8. Implementation, tests and mutation testing

**Firewall.** No new public name; no name or key contains `sigma8`,
`sigma_8` or `8hMpc`. No other package module imports `global_variance`.
Status constants and the seven 1G-H status reads in the artifact are
unchanged (`LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC = NOT_DERIVED`, the five
authorisations `NOT_GRANTED`, `VOID_ONSET_RESPONSE = EXTERNAL_CLOSURE_INPUT`).

**Evidence script.**

- `_Ball` includes u = 0 with a zero integrand; the coarse companion uses
  every other node.
- `_law_summary` computes (H25) from the same kernel arrays as the (H18)
  assembly, so the H25 gate tests the x = 0 weights of
  `two_phase_global_variance` and the linearity of the quadrature, not the
  kernels (GH-D2F2).
- The lognormal fields, `conditional_normaliser_ratio_m` and
  `e_reference_rounding_budget` are correct.

**Independence of tests.** Of the seven new tests,
`test_gh_df2_records_bind_results_to_their_inputs` and
`test_gh_df5_defensive_invariants_are_exercised` exercise the runtime
directly. The other five import the evidence script (`_evidence()`) and are
regression checks of that script, not independent oracles.

- In `test_gh_df1_lognormal_laws_share_the_carrier_not_the_conditional_density`
  the m⁻² ratio holds by construction (ψ = carrier/m). The normaliser m
  cancels in the `E[χχψψ]` comparison.
- `test_gh_df1_lognormal_laws_report_the_law_ii_normaliser` restates the
  formula.
- The correctness of m is nevertheless covered by the earlier
  `test_gh_f5_lognormal_mask_kernels_by_monte_carlo`, which checks
  `E[χ(ψ − 1)] = 0` by sampling, and by Sec. 6.

**Gates.** The author's statement that the four gates were declared before
their first evaluation cannot be verified from history (same commit) and is
recorded as the author's claim.

- `radial_refinement_rel` is meaningful but its estimator is unprotected:
  mutant A15 (coarse = fine) makes it vacuous and survives.
- `h25_identity_rel` is algebraic: it kills A17 (the (H25) sum mutated) but
  cannot see a kernel error. A kernel error is caught instead by the
  Monte Carlo test (A21 killed).

**Mutation campaign** (`mutation_campaign.py`, disposable copies outside the
tree, 42 phase tests with `-W error`, the evidence script for script mutants
and for test survivors):

| Set | Killed by tests | Killed by gates only | Survived |
|---|---|---|---|
| Delta audit's 23 (M7 and N13 adapted as recorded) | 21 | 0 | 2: N5 (centre split with intact edges, benign) and N9 (docstring sign) |
| Author's 10 | 10 | 0 | 0 |
| This audit's 23 | 12 | 2: A16 (coarse stride 3), A19 (λ calibration +1%) | 9 |

The author's "21 of 23 killed, N5 and N9 survive" and "10 of 10 killed" are
verified. Four of the author's ten are re-runs of N1, N4, N8 and N13 under
new names, as the record says ("again").

| Survivor | Caught by | Meaning |
|---|---|---|
| A01 `_same` tolerance 10⁻¹² → 10⁻³ | nothing | the binding tolerance is untested at its boundary |
| A02 `_same` without the bool type check | nothing | benign: the earlier invariants require `bool` (probes TY3/TY4 refused) |
| A07 interval `class_assumptions` check removed | nothing | the interval half of "assumptions … bound" is untested |
| A09 void-share background identity removed | nothing | defence in depth: a foreign background changes the recomputed values |
| A15 refinement estimator equals the fine value | nothing | the radial gate can be made vacuous |
| A18 ⟨C_W − 1⟩ unweighted | nothing | a newly reported quantity is unprotected |
| A20 1/m_II instead of 1/m_II² | nothing | a newly reported quantity is unprotected |
| A22, A23 H25 / radial gate thresholds set to 1 | nothing | expected; thresholds are not pinned by tests |

## 9. Documentation consistency

**Lexical search** (report, inventory, records, README, CLAUDE, script,
module, tests):

| Term | Occurrences | Classification |
|---|---|---|
| "shared constraints" | report l. 856 ("this was wrong"), second remediation record and inventory | legitimate (narrowing stated) |
| "same shared constraints" | first remediation record l. 61, its inventory l. 113, 1G-H inventory `revision.owner_decisions.D3` | historical 2026-10-07 blocks without a GH-DF1 pointer (GH-D2F5) |
| "unconditional wall-density covariance" | none | — |
| "double counting" | second remediation record l. 134 ("not double counting") | legitimate |
| "at most 0.12%", "−0.09%" | only the second remediation record's "the text said −0.09%" | historical citation |
| "transfer function at Planck parameters only" | none | — |
| "is required" | CLAUDE l. 66, 136 (unrelated conventions); test comment | legitimate |
| "re-validate every field" | first remediation record l. 146 | historical, superseded by the dated note |
| "remediated locally" | CLAUDE l. 474 (delta remediation); publication successor (quoted) | superseded by P7 (GH-D2F1); quotation |
| "Nothing is pushed" / "not pushed" / `"pushed": false` | second remediation record §0 and inventory `commits`; publication successor §3 and `state_2026_10_08`; first remediation record §0 (dated) | superseded by P7 (GH-D2F1); dated history |

**Numbers.** Every number in the revised §1, §5.2–5.3, §6.1–6.3, §8 and §11,
in the second remediation record, README and CLAUDE was compared with the
regenerated artifact or this audit's own values. No discrepancy beyond
display rounding was found. "It takes about 80 s" was 53 s (3.13, with
figures) and 46 s (3.11) here.

**Inventories.** All JSON files of the delta are valid with unique keys.
Their counts and outcomes match the records. The second remediation
inventory's `findings[*].status = RESOLVED` are the author's
self-assessment; the record itself defers the verdict to an independent
audit. That is honest, although its §0 "which completes the six partial
findings" reads as more settled than its own §2 ending.

**Honesty overall.** The second remediation discloses its development
history (a discarded first lognormal design), its tolerances and its
limitations. It states the m_II⁻² change of the conditional covariance
plainly and does not claim the stronger result. The one overstatement found
is the literal regression claim (GH-D2E1).

## 10. New findings

### GH-D2F1 — Today's push (P7) is unrecorded, and its superseded statements are incompletely listed

Severity `LOW`; area `GOVERNANCE`; relates to `NEW`; resolution `CORRECTION`.

The fast-forward `89cb041 → 226e52d` of 2026-10-08 (P7) followed the
commits, so the tree cannot record it. These statements now read as current
but are superseded:

- second remediation record §0 ("Nothing is pushed") and §4 ("Push of the two
  commits … needs a separate approval"); its inventory `commits.branch`
  ("local"), `commits.pushed: false` and `open_items`;
- publication successor §3 (`ccr-555e67be-u11yht` = `89cb041`; "not pushed")
  and its inventory `state_2026_10_08`;
- 1G-H report §9 H-OD5 ("committed locally"; "Open: … the push of its
  commits");
- 1G-H inventory `publication.pushed_head_2026_10_08`, `publication.not_done`,
  `publication.h_od5_status` and `owner_decisions_status_2026_10_08.H-OD5`;
- README ("delta-audited on 2026-10-08 and remediated locally");
- CLAUDE ("at `89cb041`"; "remediated locally on top of it").

The successor's dated-statement table (§4) lists only the second remediation
record and its inventory.

**Consequence:** a reader of README, CLAUDE or the inventories would conclude
that the second remediation is unpublished.

**Suggested correction:** a dated 2026-10-08 publication entry P7
(`89cb041 → 226e52d`, carrying `5c325e1`, `248a06b`, `226e52d`; remote head
`226e52d` verified by this audit; the authorisation as quoted by the owner).
Extend the table to the statements above, keep the historical text, and
update the README/CLAUDE current summaries (Sec. 11).

### GH-D2F2 — New reported quantities and the new gates are weakly protected

Severity `LOW`; area `TESTS`; relates to `GH-DF5`; resolution `CORRECTION`.

- ⟨C_W − 1⟩ and 1/m_II² are untested: mutants A18 and A20 survive tests and
  gates.
- The radial refinement estimator can be made vacuous (A15 survives).
- The binding tolerance is untested at its boundary (A01 survives), and so is
  the interval's `class_assumptions` binding (A07 survives).
- The (H25) gate compares two sums of the same kernel arrays, so it is
  insensitive to kernel errors.
- In the GH-DF1 test the m⁻² ratio holds by construction, and m cancels in
  the E[χχψψ] check.

The numbers themselves are right (Sec. 6), and m is covered by the earlier
GH-F5 test.

**Consequence:** future edits could change printed ⟨C_W − 1⟩ or 1/m_II²
values, or weaken the binding, without any test or gate failing.

**Suggested correction:**

- a synthetic-kernel test asserting `both_walls_conditional_density_covariance_ball`
  = ∫(K_ww + 2K_pw)/∫P11 and `conditional_density_covariance_ratio_II_over_I`
  = m⁻²;
- a Monte Carlo test of `E[ψ1ψ2 | both walls]` with ψ normalised by the
  *sample* conditional mean;
- a `_Ball` test whose coarse and fine integrals must differ by a known
  amount;
- a tamper at 2×`RECORD_IDENTITY_RTOL`, and one of `class_assumptions`;
- describe the (H25) gate as a consistency check of the (H18) assembly at
  x = 0.

### GH-D2F3 — The regression statement of the second remediation is not literally reproducible

Severity `INFO`; area `DOCUMENTATION`; relates to `GH-DF1`; resolution
`CORRECTION`.

"Every common leaf outside `two_phase_covariance/*/gaussian_threshold_pair`
bitwise identical; inside it, 130 changed, 6 renamed, 108 added" (record §3;
inventory `verification.regression_vs_89cb041`). Same interpreter, both
versions:

- three common leaves outside changed: the gate read-outs
  `gates/numerics/PAPER_REFERENCE lognormal ball-variance calibration/value`
  (3.3×10⁻¹⁶ → 0) and the two `lognormal linear limit` gate values;
- inside, 156 numeric (140 beyond round-off) plus 4 text leaves changed, 6
  renamed and 106 added; 16 leaves were added outside.

**Consequence:** none for any physical value. The verification record
overstates its own precision.

**Suggested correction:** erratum GH-D2E1.

### GH-D2F4 — Typed records accept any `numbers.Real`, and a `Fraction` breaks strict JSON

Severity `INFO`; area `IMPLEMENTATION`; relates to `GH-F9` (`NEW`,
pre-existing at `5c325e1`); resolution `CORRECTION`.

`dataclasses.replace(record, linear_sigma=Fraction(record.linear_sigma))`
passes every invariant and the binding (the value is exactly equal). The
record's `to_json_dict` then fails `json.dumps` with `TypeError`. Earlier
audits did not report this.

**Consequence:** the "records serialise as strict JSON" contract is not
enforced at construction.

**Suggested correction:** coerce validated scalars to `float` in
`__post_init__` (as `LastScatteringMatching` does), or require `float`.

### GH-D2F5 — Historical blocks keep the refuted "same shared constraints" wording without a pointer

Severity `INFO`; area `DOCUMENTATION`; relates to `GH-DF1` and `GH-DE6`;
resolution `CORRECTION`.

The first remediation record (D3 row, l. 61) and its inventory (l. 113)
still say "nonnegative lognormal pairs with the same shared constraints",
and the regenerated 1G-H inventory repeats it in `revision.owner_decisions.D3`.
The dated status note names the resolution counts and GH-DE6 but not
GH-DF1. The record's `files_changed_sha256` describe the `89cb041` bytes,
which the note does not say.

**Consequence:** minor risk of reading a 2026-10-07 statement as current.

**Suggested correction:** one sentence in the dated note: "the pairs share
the carrier law, not the conditionally normalised density (GH-DF1); hashes
refer to `89cb041`". Mark the inventory block as historical.

### GH-D2F6 — State the missing input as the mask–carrier dependence

Severity `INFO`; area `SCIENCE`; relates to `GH-DF1`; resolution `NO_ACTION`
(recommendation).

Under mask–carrier independence (E3, law I), f_v0, P11 and the carrier law
fix C_W and the hybrid variance (Sec. 6.4).

**Consequence:** none; the current reading is correct.

**Suggested correction:** optionally, state in §6.3 that the inputs fix the
variance once the mask–carrier dependence (κ0, κ(r)) is specified, E3 being
the independent case.

### Errata of the second remediation

- **GH-D2E1** (`phase1g_h_delta_audit_remediation.md` §3 and inventory
  `verification.regression_vs_89cb041`): "every common leaf outside
  `two_phase_covariance/*/gaussian_threshold_pair` bitwise identical; inside
  it, 130 leaves changed (the radial panel and the narrowed constraint
  texts), 6 renamed, 108 added". **Correct reading:** every common physical
  leaf outside the pairs is bitwise identical; the three gate read-outs of
  pair quantities change at ≤ 1.2×10⁻⁵ absolute. Inside, 160 leaves changed
  (156 numeric, 140 of them beyond round-off, and 4 constraint texts), 6
  renamed and 106 added; 16 leaves were added outside (gates, gate
  definitions, `G_ode_cross_check`).
- **GH-D2E2** (`phase1g_h_delta_audit_remediation.md` §0, "Commits … Nothing
  is pushed."; publication successor §3, "`ccr-555e67be-u11yht` = `89cb041`
  … is **not** pushed"). **Correct reading (after 2026-10-08):** the two
  remediation commits and the delta-audit commit were pushed to
  `ccr-555e67be-u11yht` on 2026-10-08 (`89cb041 → 226e52d`). The sentence
  is true as of its commit and must be read through a dated P7 record
  (GH-D2F1).

## 11. Recommendations (owner decisions; recommendations only)

- **H-OD1.** Keep the formal tangent statistic as a named research proposal;
  (c) preferred, with (a) as the fixed-mass comparison.
- **H-OD2.** No physical reference value. The median seed remains a heuristic
  prior below ε = 1 with no controlled truncation error, the [W09] seed a
  nonperturbative formal extrapolation, and the constant-share interval valid
  only in its class.
- **H-OD3.** No token change. `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` stays
  `NOT_DERIVED` and the five authorisations stay `NOT_GRANTED`. (H25) and the
  C_W reading belong in the report, not in a token.
- **H-OD4.** Keep the runtime experimental. Apply GH-D2F2 (tests) and
  optionally GH-D2F4. Run the Windows gate before any promotion.
- **H-OD5.** No scientific blocker remains for a decision on merging 1G-H
  as a conditional research record. Before merge or freeze:
  (i) record P7 and the direct GH-F15 confirmation (below);
  (ii) apply the LOW corrections GH-D2F1 and GH-D2F2;
  (iii) run the owner's Windows 3.14.3 / 3.11.9 gate, never run on any 1G-H
  tree;
  (iv) take the owner's explicit decision for each action (PR, merge, tag,
  freeze).
  Given that this audit shares the author's model family, a cross-family
  spot check of §6 is advisable if institutional independence is wanted.
  Never create `phase-1g-d-separate-universe-growth-v2`.
- **Recording P7.** A dated successor entry, either a new record or an
  additive dated section of the publication successor in the style of the
  first remediation record's note, with:
  - event P7, 2026-10-08: fast-forward of `ccr-555e67be-u11yht` from
    `89cb041` to `226e52d`, carrying `5c325e1`, `248a06b` and `226e52d`;
  - remote evidence: branch head `226e52d`, verified read-only by this
    audit;
  - authorisation: «Fai push e prepara il prompt per un nuovo audit», as
    quoted by the owner in the second-delta-audit handoff;
  - the superseded statements of GH-D2F1 added to the current-reading table.
- **Recording GH-F15.** A dated confirmation event: «Confermo le due
  approvazioni di push registrate (GH-F15)», given directly to the auditor
  of this second delta audit on 2026-10-08 and recorded in
  `phase1g_h_delta_audit_2.md`. Status `RESOLVED_OWNER_CONFIRMED`. The P4
  wording "not given directly to an auditor" can then be read as superseded.
- **Publication of this audit** is a separate owner decision, on this
  session's designated branch only if approved.

## 12. Limits

- **Same model family as the author** (Claude). Procedural independence
  only, with no contact with the author; the two earlier audits were OpenAI
  Codex.
- The blind checkpoint is blind to the author's full-precision values and
  new code, not to the three-decimal values quoted in the prompt, report and
  records, which were read for the model definitions. The tracker and EH98
  provider were reused from the first audit, not re-derived.
- Windows CPython 3.14.3 / 3.11.9 was not available; the owner's gate
  remains unmet. Linux results do not certify Windows.
- Owner approvals quoted in the records («Perfetto, procedi», «Si,
  confermo», «Si, fai push», «Fai push e prepara il prompt …») cannot be
  verified from the repository. The only owner words received directly are
  the GH-F15 confirmation in the handoff message.
- A ref snapshot shows current state, not every transient remote event.
- Mutation testing covered the 42 phase tests and, where relevant, the
  evidence script; no full-suite mutation campaign. Convergence checks are
  empirical, not error theorems.
- The kernel Monte Carlo of the author was rerun only through the test
  suite; this audit's independent check of the kernels is analytic (Owen's
  T, Stein, tilting), not a spatial-lattice simulation.
- No physics beyond the delta was re-derived: no Boltzmann recalibration,
  no gravitational dynamics, no material-domain transport, nothing
  observational.
- Process note: one log of this audit's own 3.11 suite run (`suite311.log`
  and `.xml`) was written by mistake to the container's filesystem root,
  outside the repository; its content was copied to the scratchpad and
  summarised in `full_suite_summaries.txt`. No repository file is affected.

## 13. Sources and hashes

Re-downloaded from arXiv on 2026-10-08 into a scratch directory outside the
repository (not bundled); SHA-256 of the files named in the 1G-H inventory:

| Source | Version | File | SHA-256 | Match |
|---|---|---|---|---|
| [EH98] | astro-ph/9709112v1 | `trans.tex` | `5f2ac6b413df8b738c95f6650152b7e82d7c36f6d9b3a618da540e9739dce17f` | yes |
| [GM] | arXiv:2511.17160v2 | `main.tex` | `f9cadfa03ecc9a74b0a8f432ae4b13422daeb219f253756bcd877b4b75077c59` | yes |
| [JLH13] | arXiv:1304.6087v2 | `voids_mnras.tex` | `cf6fc77a31b395138ac3a027d008698556534e81cfb27c39853d3a99c7b07c4e` | yes |
| [NW15] | arXiv:1410.3470v2 | `cmb1.tex` | `5688c9ac7123a5c2ef3508e39cb3134c2fe9e3d5e56996a4d4a4d101d7b74673` | yes |
| [SvdW04] | astro-ph/0311260v1 | e-print tarball | `4b7ad599f54b3199e0448df1c2eecf4e724401e9ffda7b0f50a3efe7fecdb79b` | yes |
| [W07] | arXiv:0709.0732v2 | `solution.tex` | `221662c987e454729ef8202c87fa697c5882b5b7daaecdedb50a7cba8ffe6cd8` | yes |
| [W09] | arXiv:0909.0749v2 | `observe.tex` | `2b0324d127440e9a053a7cb37102d7655cca228a63cd2222843e879989b4b531` | yes |

Audit files: the blind checkpoint `BLIND_CHECKPOINT.md` (`c5f744e3…54ac`) and
the remaining evidence are listed with their SHA-256 in the inventory
(`sources.audit_evidence`).
