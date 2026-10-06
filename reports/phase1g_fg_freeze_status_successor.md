# Phase 1G-F/G — freeze-status successor record

Date: 2026-10-06. Classification: `FREEZE_STATUS_SUCCESSOR_RECORD`
(documentation only; no scientific content).
Base: `main` = `origin/main` = `8d3cdd0533035858c42269cb1dff1a20dcafc7da`,
local branch `phase-1g-h-global-variance-closure`.
Companion: [`phase1g_fg_freeze_status_successor_inventory.json`](phase1g_fg_freeze_status_successor_inventory.json).

This record documents a freeze that has **already happened**. It does not
declare the freeze again, create or move a tag, or certify anything new
about the F/G science. It lists the status sentences in the F/G records
that the merge, the freeze and the published tags have made out of date,
and gives their current reading. The historical files keep their bytes.

## 1. Authorization

The owner's task statement of 2026-10-06 ("Timescape-fsigma8 — incarico
cloud per chiudere la definizione di σ₈"), §2.1, verbatim:

> «Allinea lo stato corrente di F/G al merge, al freeze e ai tag già
> pubblicati. Questo lavoro è espressamente autorizzato e non richiede
> un'altra conferma.»

The same section asks to keep the bytes of the frozen or hash-bound F/G
reports and inventories, to resolve outdated sentences through this
successor, and to update README.md and CLAUDE.md directly. It also states
that this record documents a freeze that has already happened. The task
grants local commits on a dedicated branch. It grants no push, pull
request, merge, tag, freeze or release (§1 of the task). With a separate
approval of 2026-10-06, given after this record was committed, the owner
had its commit pushed, together with the Phase 1G-H commits, to the session
branch `ccr-555e67be-u11yht`; no pull request, merge, tag, freeze or release
followed.

The task also records an explicit decision, verbatim: «non creare
`phase-1g-d-separate-universe-growth-v2`, né come tag né come branch.»
None is created. The approved D successor
(`phase1g_d_linear_statistic_status_successor.md`, 2026-10-02) is already
part of the checkpoint covered by the F/G tags. The D v1 tag and its
historical record are unchanged.

## 2. State verified in this session

Verified on Linux (cloud session, 2026-10-06), read-only against `origin`.

| Item | Value | How verified |
|---|---|---|
| Source pull request | PR #4, `phase-1g-f-successor-g-evolution` → `main`, merged 2026-10-06T13:12:04Z | GitHub API read |
| Merge commit = frozen checkpoint | `8d3cdd0533035858c42269cb1dff1a20dcafc7da` | `git rev-parse` |
| Merge parents | `fb5d95245bc0cb19ce6cd1438177f1a597bb232f` (previous `main`), `3d3d46ed68fde7e6d4100fe518a76731bd2cf9e9` (phase branch) | `git log --format=%P` |
| Tree of the merge | `5bcea4170c92c034af0045afb7f9898c2f28359d` | `git rev-parse 8d3cdd0^{tree}` |
| Tree of `3d3d46e` | `5bcea4170c92c034af0045afb7f9898c2f28359d` (identical) | `git rev-parse 3d3d46e^{tree}` |
| F/G integration commit | `8f3131fe19cccd44a29287617145f3300818dfa3` (successors, remediation, audits, evidence) | ancestor of `main` |
| Provenance commit | `3d3d46ed68fde7e6d4100fe518a76731bd2cf9e9` (records `8f3131f…` in the integration record) | ancestor of `main` |
| `main` at session start | `8d3cdd0…` (= `origin/main`; no later commit) | `git fetch`; `git rev-parse` |

The clone was shallow at session start. It was completed with
`git fetch --unshallow --tags origin`; no history was rewritten or
reconstructed.

### 2.1 Tags

| Tag | Annotated tag object | Target commit | Tagger date |
|---|---|---|---|
| `phase-1g-f-void-population-v1` | `ca52c94d6ecad2be62016b019d652d9bc6e89dd2` | `8d3cdd0533035858c42269cb1dff1a20dcafc7da` | 2026-10-06T15:32:56+02:00 |
| `phase-1g-g-void-evolution-v1` | `d151bd45242eff50ca7fa62bbd50453375737117` | `8d3cdd0533035858c42269cb1dff1a20dcafc7da` | 2026-10-06T15:32:56+02:00 |

- **Remote.** `git ls-remote origin` returns the same two tag objects.
- **Messages, read in full.** Both summarise the conditional results, the
  first audit, the remediation, the delta audit and the integration
  record. Both state "Freeze preflight at this commit: 1136 passed,
  0 skipped, 0 failed on CPython 3.14.3 and 3.11.9 (-W error)" and that
  `SIGMA8_AUTHORIZATION` remains `NOT_GRANTED`. The 1G-F message also
  records the D successor (`LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC =
  NOT_DERIVED`).
- **Signatures.** Each tag carries an SSH signature (`ssh-ed25519`,
  namespace `git`, SHA-512). The public key embedded in all seven Phase 1G
  tag signatures (1G-A…1G-G) has the same fingerprint,
  `SHA256:65hFn8HnIB5jIzkHfWCR7Em0D500qriDfGl+8moqz8Y`. That is an identity
  consistency check of the embedded key, **not** a signature verification.
  No trust configuration of the project was used in this session, so the
  signatures were **not** cryptographically verified here. In the wording
  the task prescribes: «freeze e pubblicazione confermati dal resoconto;
  verifica locale incompleta» (for the signatures only; the tag objects,
  targets and messages were verified).

### 2.2 Suite results: two provenances, kept distinct

| Run | Tree | Result | Source |
|---|---|---|---|
| Integration runs on the final content (before the merge) | `8f3131f…` content | 1136 passed, 0 skipped, 0 failed on CPython 3.14.3 (524 s) and 3.11.9 (538 s) | `phase1g_fg_remediation_integration.md` §5.2 |
| Freeze preflight at the merge | `8d3cdd0…` | 1136 passed, 0 skipped, 0 failed on CPython 3.14.3 (505 s) and 3.11.9 (501 s), warnings as errors | owner's report of 2026-10-06; tag messages (counts only) |
| This session's baseline (not a freeze certification) | `8d3cdd0…` | 1103 passed, 33 skipped, 0 failed on CPython 3.13.16 and 3.11.17 (Linux) | session log; the skips are the oracle and generated-artifact tests whose inputs are absent in a fresh clone |

The owner-reported freeze runs were not repeated to copy their numbers.
The Linux baseline only establishes that this environment reproduces the
suite before new work; it does not certify the freeze.

## 3. Superseded status statements

Each row quotes the historical statement exactly. It was correct when
written; the current reading follows from §2. The files are not edited.

| # | Document (SHA-256 at `8d3cdd0`) | Location | Historical statement (verbatim) | Written | Current reading (2026-10-06) |
|---|---|---|---|---|---|
| S1 | `phase1g_f_volume_budget_successor.md` (`3208c539…`) | header, l. 32–33 | "This revised local deliverable has not been frozen; the audit does not certify subsequent edits." | 2026-10-02 | Frozen: merged into `main` by PR #4 at `8d3cdd0…`, tagged `phase-1g-f-void-population-v1`. The second clause stays true: neither audit certifies edits after its own scope. |
| S2 | same | §6, l. 316–317 | "It is not frozen, and no tag, merge or release is implied." | 2026-10-06 (integration revision) | Merged (PR #4) and frozen at `8d3cdd0…`, tag `phase-1g-f-void-population-v1`. No release exists. |
| S3 | `phase1g_f_volume_budget_successor_inventory.json` (`6b09f475…`) | key `integration_state` | `"LOCAL_REVIEWABLE_UNMERGED_UNTAGGED"` | 2026-10-02 / 2026-10-06 | `MERGED_FROZEN_TAGGED` at `8d3cdd0…` (inventory key `current_integration_state` of this record) |
| S4 | `phase1g_g_void_evolution.md` (`41560ed5…`) | header, l. 5–6 | "This is a local research proposal, not a frozen implementation phase or a new Timescape prediction." | 2026-10-01 | Frozen report-only research phase, tag `phase-1g-g-void-evolution-v1` at `8d3cdd0…`. "Not a frozen implementation phase" stays true in the sense that G adds no package runtime; "not a new Timescape prediction" is unchanged. |
| S5 | same | §8, l. 283–284 | "No freeze, tag, merge or release is implied." | 2026-10-06 (integration revision) | Merged (PR #4), frozen and tagged (`phase-1g-g-void-evolution-v1`). No release exists. |
| S6 | `phase1g_g_void_evolution_inventory.json` (`3ce6a587…`) | key `integration_state` | `"LOCAL_REVIEWABLE_UNMERGED_UNTAGGED"` | 2026-10-01 / 2026-10-06 | `MERGED_FROZEN_TAGGED` at `8d3cdd0…` |
| S7 | `phase1g_fg_remediation_integration.md` (`ec41f322…`) | §8 item 1, l. 175–180 | "Owner approvals, each separate: merging into `main` (through a pull request); any annotated phase tag; any release. None is authorized." (bulleted list joined with semicolons) | 2026-10-06 | Merge and the two tags were later approved and executed by the owner (PR #4; tags of §2.1). A release is still neither approved nor created. Items 2–4 of that section are unchanged. |
| S8 | `phase1g_fg_remediation_integration_inventory.json` (`241054f2…`) | `authorization.…scope_summary` | "local commits and ordinary push of this phase branch to origin; no main push, force push, merge, PR, tag, release, scientific freeze, status or observational-authorization change" | 2026-10-06 | Correct as the scope of that authorization. The later merge, freeze and tags rest on separate owner actions (§2), not on that authorization. |
| S9 | `phase1g_fg_successor_validation.md` (`438a0063…`) | "Documentation state verified against GitHub", l. 114 | "No 1G-F tag was returned." | 2026-10-01 | `phase-1g-f-void-population-v1` exists (§2.1). |
| S10 | same | l. 24–25 and l. 70–73 | "No push, PR, remote mutation, phase tag or independent adversarial audit was performed." / "Before a formal phase freeze, apply in a real checkout, run the existing two-environment gates with their required artifacts, obtain the independent audit and record the actual commit." | 2026-10-01 | Those freeze requirements were met later: two independent audits (2026-10-02, 2026-10-06), the integration record (actual commit `8f3131f…`), the owner's two-interpreter freeze preflight and the tags. |
| S11 | `phase1g_fg_independent_scientific_audit.md` (`6bb8edec…`) | CLAUDE.md check table, l. 515 | "σ track: main at fb5d952, 1G-A…E v1 tags, no 1G-F tag" | 2026-10-02 | Audit observation, correct then. `main` is now at `8d3cdd0…` and carries the 1G-F and 1G-G tags. The audit is not edited. |
| S12 | `phase1g_fg_remediation_independent_audit.md` (`46f3aef7…`) | §0.1, l. 36–38 | "The corrections can be integrated: committed locally on the phase branch by the owner. Nothing in this audit authorises a merge, tag or remote action." | 2026-10-06 | Still true of the audit. The integration, merge and tags happened afterwards on separate owner authority. |
| S13 | `README.md`, `CLAUDE.md` | σ-track sections | "not merged into `main`, frozen or tagged"; "Nothing is frozen or tagged"; "no 1G-F tag was found"; "unmerged deliverables on the phase branch"; "but not frozen"; "No phase freeze, tag, merge or release is implied" | 2026-10-01 to 2026-10-06 | Current documentation: updated directly in the same commit as this record, pointing here. |

**Readings explicitly not changed:**
- `phase1g_fg_audit_remediation_inventory.json` keeps
  `"actual_remediation_commit": null`. The integration record already gives
  the actual commit, `8f3131f…`; this record does not edit either.
- The three commits stay distinct: the remediation/integration commit
  `8f3131fe…`, its provenance commit `3d3d46ed…`, and the merge, which is
  the frozen checkpoint `8d3cdd05…`.
- The approved D successor of 2026-10-02 is not a new D phase and not a
  "D v2". It is already covered by the F/G checkpoint; the D v1 tag
  (`phase-1g-d-separate-universe-growth-v1` → `fb5d952…`) is unchanged.

## 4. What the freeze does and does not mean

- It attests the checkpoint `8d3cdd0…` within its documented perimeter: the
  conditional F volume-budget successor, the G evolution research, the
  approved D successor, both independent audits, the remediation, the
  integration record and the preserved evidence.
- It derives no σ8, adds no package API, and grants no observational
  status. `SIGMA8_AUTHORIZATION`, `FSIGMA8_AUTHORIZATION`,
  `RSD_AUTHORIZATION`, `OBSERVATIONAL_AUTHORIZATION` and
  `UNIQUE_TIMESCAPE_PREDICTION` remain `NOT_GRANTED`;
  `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` remains `NOT_DERIVED`.
- New results belong to the next phase (proposed 1G-H,
  `phase1g_h_global_variance_closure.md`). Any correction of a frozen
  F/G result needs its own traced successor.

## 5. Files

| File | Change |
|---|---|
| `reports/phase1g_fg_freeze_status_successor.md` | this record (new) |
| `reports/phase1g_fg_freeze_status_successor_inventory.json` | its companion (new) |
| `README.md`, `CLAUDE.md` | current-status sections only, linking here |

Unchanged: every report, inventory, audit, log, evidence file and manifest
of F/G (including `MANIFEST.sha256`), every package module, test, status
token and tag.

## 6. Reproduction

```bash
git fetch --unshallow --tags origin        # only if the clone is shallow
git rev-parse 8d3cdd0^{tree} 3d3d46e^{tree}  # both 5bcea4170c92c034af0045afb7f9898c2f28359d
git merge-base --is-ancestor 8f3131fe19cccd44a29287617145f3300818dfa3 origin/main
git merge-base --is-ancestor 3d3d46ed68fde7e6d4100fe518a76731bd2cf9e9 origin/main
git rev-parse phase-1g-f-void-population-v1 phase-1g-g-void-evolution-v1
git rev-parse 'phase-1g-f-void-population-v1^{commit}' 'phase-1g-g-void-evolution-v1^{commit}'
git ls-remote origin 'refs/tags/phase-1g-f-*' 'refs/tags/phase-1g-g-*'
git cat-file -p phase-1g-f-void-population-v1
```

Signature verification needs the project's established trust
configuration (for example `git tag -v` with the owner's allowed-signers
file). It was not available in this session.
