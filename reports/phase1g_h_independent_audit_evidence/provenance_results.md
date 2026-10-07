# Independent provenance and governance synthesis

Audit object: `d4d693d73f995e2245a5720be227273b3639eda9`, tree `963b6e8e42103c27f329e265056c9624be3f11bd`, against F/G base `8d3cdd0533035858c42269cb1dff1a20dcafc7da`. This synthesis uses the authenticated Git objects and saved read-only GitHub responses obtained by the main auditor. It performs no remote mutation, test run or edit to an existing repository file.

## Result

**ACCEPT_WITH_CORRECTIONS for provenance and governance**, with the two later push approvals **OWNER_CONFIRMATION_REQUIRED**. No evidence supports an unauthorized scientific firewall change: the original task §1 expressly authorizes isolated experimental modules, new derivations, tests, examples and current-documentation updates. Its §§2 and 10 expressly permit Linux, available supported interpreter versions, and disclosed skips for unavailable historical artifacts. These exceptions are specific owner instructions and take precedence over the generic workflow in CLAUDE.md. Scientific validity and the adequacy of the numerical contracts remain separate findings.

The remote state is a timestamped observation. The first saved snapshot is 2026-10-06T19:20:54.939Z; the main/session branch and absence of a PR were refreshed at 2026-10-07T04:55:46.522Z. Do not describe these as continuous monitoring or proof that no temporary ref was ever created and deleted.

## Object identity and preservation

The four commits have the expected ancestry and roles:

| Commit | Role | Tree |
|---|---|---|
| `79003742fb1f284693d6659e329b2c6b7f7927f0` | Separate F/G documentation alignment | `fc2ce9da6837f083a9497c9c2656f8a7748f9aae` |
| `fd7331f321702ed8c20d32ea805e7b9537d44726` | Runtime, scripts, configs and tests | `90db4855e87c299b0fc36278cba8be8adc441b1a` |
| `0572e416504bcdfaa5831b6d482b687ef6fae582` | Science report, inventory, evidence logs, status documentation | `b709ba71a91c5cac478187bd81c6c774e8c2c760` |
| `d4d693d73f995e2245a5720be227273b3639eda9` | Publication-status documentation only | `963b6e8e42103c27f329e265056c9624be3f11bd` |

The base has 334 tracked files and HEAD 351. Of preexisting files only README.md and CLAUDE.md changed; 17 files were added. Therefore every existing package module, test, historical report, audit, inventory, evidence log and manifest has the same Git blob identity as the base. The SHA-256 checks for the S1–S12 pinned historical records also match. In particular `scientific_status.py` and `lagrangian_sigma.py` are byte-identical to the base. The historical remediation inventory retains `actual_remediation_commit: null`; the later integration record correctly records the actual commit separately.

The merge has parents `fb5d95245bc0cb19ce6cd1438177f1a597bb232f` and `3d3d46ed68fde7e6d4100fe518a76731bd2cf9e9`. Its tree and the latter commit's tree are exactly `5bcea4170c92c034af0045afb7f9898c2f28359d`. The remediation/integration commit `8f3131fe19cccd44a29287617145f3300818dfa3` precedes that provenance commit. The saved PR #4 response confirms the merge commit and `merged_at = 2026-10-06T13:12:04Z`.

HEAD's seven-file delta from `0572e41` contains only README, CLAUDE, the two freeze-status files, the H report, H inventory and H validation record. No runtime, test or numerical-result content changed in that commit.

## Remote state and signatures

The saved responses show main at the base, `ccr-555e67be-u11yht` at the audited HEAD, no PR from that branch, 38 tags, no release, and no D-v2 tag or matching branch. The five A–E tags target `fb5d952…`; F and G target `8d3cdd0…`. F's annotated object is `ca52c94d6ecad2be62016b019d652d9bc6e89dd2`; G's is `d151bd45242eff50ca7fa62bbd50453375737117`. Both tagger timestamps are 2026-10-06T15:32:56+02:00. This agrees with the author record and the original owner's task. Identity of the currently observed tag objects is verified; unchanged tags throughout an unobserved author session cannot be established from a final snapshot alone.

The seven 1G tag objects were reconstructed from retrieved authenticated object content and their exact Git object SHA-1 was checked. A mathematical signature check using `ssh-keygen -Y check-novalidate -n git` succeeds for all seven. All use the embedded ED25519 fingerprint `SHA256:65hFn8HnIB5jIzkHfWCR7Em0D500qriDfGl+8moqz8Y`. GitHub separately marks each verified/valid. **This is not a local verification of the owner's identity using established trust.** No project allowed-signers configuration was available or modified. The author's statement that signatures were not cryptographically verified in that author's session is neither contradicted nor retrospectively changed by this audit's additional mathematical check.

Freeze suite counts (1136/0/0, Python 3.14.3 and 3.11.9) are accurately quoted from owner records and tag messages. The integration times 524/538 s and later freeze times 505/501 s remain separate. Their execution is historical testimony, not a run independently observed here. The Linux author logs and this audit's reruns establish different, explicitly recorded coverage.

The inventory quotes two later approvals: “Sì, procedi con il push sul branch designato” and “Sì, correggi la documentazione e fai il push”. Only the owner can confirm those statements and their scope. Mark **OWNER_CONFIRMATION_REQUIRED / NOT_VERIFIABLE**, without treating repository text or remote ref existence as proof of permission. No author conversation was consulted. The first push's ref transaction cannot be recovered from the saved snapshot: a new remote ref should be called a branch creation even though its commit history is a fast-forward descendant of the base.

## S1–S13

| Row | Verdict | Qualification |
|---|---|---|
| S1 | VERIFIED | Historical SHA-256, exact text modulo line wrapping, location and current freeze reading agree. Audit-scope clause remains true. |
| S2 | VERIFIED | Same checks; no release is observed. |
| S3 | VERIFIED | Exact historical inventory value and current checkpoint reading agree. |
| S4 | VERIFIED | Frozen research/report phase; still no G package runtime or new prediction. |
| S5 | VERIFIED | Historical text and later merge/freeze/tag reading agree. |
| S6 | VERIFIED | Historical inventory value and current checkpoint reading agree. |
| S7 | VERIFIED_WITH_QUALIFICATION | Source bullets are correct and explicitly labelled as joined; this is not one literal verbatim sentence. Later actions rest on distinct owner authority. |
| S8 | VERIFIED | Earlier authorization scope remains historical; it did not authorize the later merge/tags. |
| S9 | VERIFIED | Historical no-tag observation and later F tag are both correctly distinguished. |
| S10 | VERIFIED_WITH_QUALIFICATION | Two source spans, separately correct, are joined with a slash. Later audit records/tags exist; owner freeze execution remains reported. |
| S11 | VERIFIED | Old audit observation is preserved and new main/tag state is correct. |
| S12 | VERIFIED | Old audit conferred no permission; later separate owner action is not permission from that audit. |
| S13 | VERIFIED_WITH_QUALIFICATION | All six phrases exist at the base and current documents were updated, but the published row lacks source hashes and precise per-phrase positions. |

For S13, base README SHA-256 is `85d78ff8583a30d340a16c545eab5e972b8ffcabbcc409e337345bc4c70d149c`; base CLAUDE SHA-256 is `2d96e25cf4632395ebe45d9429738198dba9ec06c6f87f5a8bc01b9683f899c6`. Locations: README lines29–30 and114; CLAUDE line106, line259, lines260–261, lines434–435. See `provenance_claims.json` for per-phrase mapping.

The successor is not exhaustive. It omits the historical F report `phase1g_f_void_population.md` §14 lines638–639 (“Nothing is merged or tagged.”), the integration report §3 lines79–80 ('“Not merged, frozen or tagged” is kept.'), and integration inventory `open_before_freeze[0]` (“separate owner approvals for merge into main (PR), annotated tag, release”). Add later-reading rows in a successor, preserving those historical bytes, or clearly describe the map as a selection. These omissions do not reverse the independently confirmed freeze.

## AGENTS rules 1–10 and CLAUDE process

The JSON companion contains a 40-cell commit/rule matrix. For the three documentation-only commits, executable requirements have no relevant code delta. For `fd7331f`:

1. New scientific experiments and definitions are authorized; no existing equation was modified.
2. H-number equation citations and primary-source lineage are present; their scientific sufficiency is assessed by the independent science review.
3. Model additions and new assumptions are labelled and isolated, rather than represented as equivalent refactoring.
4. Units, normalization, clock, ICs and signs are explicit. The p-definition algebraic error is a scientific correction, not evidence that the runtime secretly changed an older convention.
5. The 28 added tests cover the required categories. Author and audit reruns do not cover the skipped historical oracle/artifact checks until their inputs exist. Contract and precision-test gaps are recorded separately.
6. No upstream notebook code occurs among the added distributable files. The pinned upstream clone remains reference-only.
7. Local work/read-only queries are authorized; later pushes require the owner's confirmation of the recorded separate approvals.
8. The module follows the typed pure-function and immutable-record design. Incomplete validation of manually constructed records is an implementation finding.
9. Tolerances are explicit (saved audit: 716 comparisons, zero missing); explicitness does not establish adequacy. The E/F printed-precision tolerance needs correction. The small absolute root tolerance is not itself below the representable precision of the root.
10. No new undocumented warning suppression is identified; the complete suite commands use `-W error`.

Original task §§1,2.1 authorize the experimental firewall exception and the dedicated documentation alignment; §10 authorizes supported Linux interpreters and disclosed missing-artifact skips. Therefore CLAUDE's generic clean dual-environment preflight is qualified by the more specific task, not covertly weakened. The author records a dedicated local `phase-1g-h-global-variance-closure` branch, then a separately approved push to the session branch. Actual historical branch-creation timing is not recoverable from Git commit objects. No final freeze certification is inferred from a skipped Linux suite.

The first documentation commit is separate, the science implementation and report commits are separate, and the publication update is documentation-only. The mandatory output types exist and are in English. Runtime examples are concrete. Status tokens and authorizations are preserved, including `NOT_DERIVED` and five `NOT_GRANTED` authorizations. R2-N4 remains optional because there is no registry amendment. Whether the definition and conditional calculation satisfy the task's scientific A/B criteria is determined by the independent scientific findings, not by deliverable presence. The author's final Italian chat response cannot be audited without the author conversation, which this audit intentionally did not access.

## Exact documentation errata

The JSON `errata` array gives seven localized corrections: qualify “Each row quotes … exactly”; complete S13 identifiers; add the three omitted historical readings; update stale `owner_decisions_requested.H-OD5` (“none authorised”) to agree with `publication.h_od5_status`; distinguish descendant ancestry from an unverified remote push transaction. These are LOW severity. The immutable historic commit message cannot be edited; clarify it through the audit or a later successor. No existing repository file was edited by this synthesis.

## Coverage limits

No complete per-file reading ledger was found under `audit_work`. The main auditor and scientific/implementation reviewers have separately attested reading source equations, runtime and tests; their contributions substantiate those parts of coverage. This synthesis directly read AGENTS, the original task, relevant CLAUDE sections, the current freeze successor, all saved S1–S13 checks, signature checks, commit contents/deltas, remote snapshots and relevant current validation/inventory passages. It does not claim that every mandatory historical scientific document was read in full by this sub-review. Remaining scientific mandatory-read coverage must be accounted for in the main audit. No additional remote call or test was needed for this synthesis.
