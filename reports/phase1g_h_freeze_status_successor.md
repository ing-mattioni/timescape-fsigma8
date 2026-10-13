# Phase 1G-H — freeze-status successor record

Date: 2026-10-13. Classification: `FREEZE_STATUS_SUCCESSOR_RECORD`
(documentation only; no scientific content).
Base: `main` = `origin/main` = `728dfcd3b4c661c1baf75570b8aa7496e0096799`
(the PR #5 merge, the frozen 1G-H checkpoint). Branch: the session branch
`ccr-555e67be-u11yht`, restarted from `main` by a fast-forward from
`1777ead`.
Companion: [`phase1g_h_freeze_status_successor_inventory.json`](phase1g_h_freeze_status_successor_inventory.json);
logs in [`phase1g_h_freeze_status_successor_logs/`](phase1g_h_freeze_status_successor_logs/).

Cited as:
- [1G-H] = [`phase1g_h_global_variance_closure.md`](phase1g_h_global_variance_closure.md),
  with its inventory and validation record;
- [OD] = [`phase1g_h_owner_decisions_successor.md`](phase1g_h_owner_decisions_successor.md);
- [PUB] = [`phase1g_h_publication_successor.md`](phase1g_h_publication_successor.md);
- [FG] = [`phase1g_fg_freeze_status_successor.md`](phase1g_fg_freeze_status_successor.md),
  the model for this record.

This record documents a merge, freeze and tag that have **already
happened**. It does not declare the freeze again, create or move a tag, or
certify anything new about the 1G-H science. It records:
- the push P18;
- pull request #5 and its merge commit;
- the tag;
- the status sentences in the 1G-H records that these events made out of
  date, with their current reading.

The frozen files keep their bytes. [PUB] is frozen with the other 1G-H
records ([OD] Sec. 4), so publication events after P17 are recorded here.

## 1. Authorisation

- **2026-10-09.** The owner decided the pull request, merge, freeze and
  tag. Verbatim: «Ho eseguito le test suite su windows, tutto ok. Dunque
  Implementa le raccomandazioni dell'audit su H-OD1…H-OD5 e poi fai PR,
  merge, freeze e tag» ([OD] Sec. 1 and 4, H-OD5). The push P18 of the
  commit carrying [OD] was part of that pull request ([OD] Sec. 1).
- **2026-10-13.** After creating the tag, the owner wrote, verbatim:

  > «Ho fatto il tag. Controlla, poi se è tutto ok fai tutto quello che
  > restava da fare; approvo push, PR e merge del successor di freeze.»

  This record, with README.md and CLAUDE.md, is what remained.

  The same message approves three later actions:
  - the push of this record's commit to the session branch (P19);
  - its pull request into `main`;
  - its merge.

  They follow the commit, and a commit cannot record its own push ([PUB]
  Sec. 8.3 and 10.3). So this record does not contain them; the pull
  request on GitHub records them.

The 2026-10-13 message approves nothing else: no release, no new tag, and
no change to a token, an authorisation or the science.

## 2. State verified in this session

Verified on 2026-10-13 on Linux (cloud session), read-only against
`origin`, with the GitHub API for the pull request. Raw output:
[`remote_and_tag_state.txt`](phase1g_h_freeze_status_successor_logs/remote_and_tag_state.txt).

| Item | Value | How verified |
|---|---|---|
| P18 | 2026-10-09: fast-forward of `ccr-555e67be-u11yht` from `22ace89` to `1777ead1a4993f9d6b5dba10346ad1455115ed3a`, which carries [OD] | push output `22ace89..1777ead` (session log); PR #5 head; `git ls-remote` |
| Source pull request | PR #5, `ccr-555e67be-u11yht` → `main`. Created 2026-10-09T15:56:13Z, merged 2026-10-09T15:56:28Z. 25 commits, 450 files | GitHub API read (`pull_request_read get`) |
| Who merged | this session, through the GitHub API, on the owner's decision of 2026-10-09. The API names the owner's account (`merged_by`) because the session's GitHub access uses that account | session log; GitHub API |
| Merge commit = frozen checkpoint | `728dfcd3b4c661c1baf75570b8aa7496e0096799`, committer GitHub, 2026-10-09T17:56:27+02:00, "Merge pull request #5 from ing-mattioni/ccr-555e67be-u11yht" | `git log` |
| Merge parents | `8d3cdd0533035858c42269cb1dff1a20dcafc7da` (previous `main`, the F/G checkpoint) and `1777ead1a4993f9d6b5dba10346ad1455115ed3a` (branch head) | `git log --format=%P` |
| Tree of the merge | `9f020ba18f986baeb1ccd4cd748eeea19fd62e33` | `git rev-parse 728dfcd^{tree}` |
| Tree of `1777ead` | `9f020ba18f986baeb1ccd4cd748eeea19fd62e33` (identical) | `git rev-parse 1777ead^{tree}` |
| `main` at session start | `728dfcd…` (= `origin/main`; no later commit) | `git fetch`; `git ls-remote` |
| Session branch at session start | `1777ead…` on `origin`. Here it was fast-forwarded to `728dfcd` (a merge commit that has `1777ead` as parent), so no history is rewritten | `git merge --ff-only origin/main` |

### 2.1 Tag

| Tag | Annotated tag object | Target commit | Tagger date |
|---|---|---|---|
| `phase-1g-h-global-variance-closure-v1` | `1ef6f3ee7f382ce3a2709d9b2564dd8685f5a028` | `728dfcd3b4c661c1baf75570b8aa7496e0096799` | 2026-10-13T14:26:26+02:00 |

- **Remote.** `git ls-remote origin` returns the same tag object, peeled
  to `728dfcd`.
- **Who.** The owner created, signed and pushed it on 2026-10-13; the
  tagger is the owner.
- **The session's own attempt (2026-10-09).** The session created an
  unsigned annotated tag (local object `b066833`) and tried to push it. The
  session's git proxy refused the push ("error: RPC failed; HTTP 403";
  "send-pack: unexpected disconnect while reading sideband packet"). The
  session deleted the local object; no remote tag resulted. The session
  then gave the owner the tag message and the commands.
- **Message, read in full.** It is byte-identical to the message the
  session prepared for the owner. It summarises:
  - the statistic and the experimental runtime;
  - the five audits, the five remediation records, [PUB] (P1–P17) and [OD];
  - the 1G-B contract-hardening successor.

  It also states: "Freeze preflight: 1212 passed, 0 skipped, 0 failed on
  Linux CPython 3.13.16 and 3.11.17 (-W error); Windows gate reported
  passing by the owner"; that no status token is added or changed; and
  that `SIGMA8_AUTHORIZATION` remains `NOT_GRANTED`.
- **Signature.** An SSH signature (`ssh-ed25519`, namespace `git`,
  SHA-512).
  - The embedded public key has the fingerprint
    `SHA256:65hFn8HnIB5jIzkHfWCR7Em0D500qriDfGl+8moqz8Y`. All seven earlier
    Phase 1G tags (1G-A…1G-G) carry the same key ([FG] Sec. 2.1).
  - This session checked every signature cryptographically against its
    embedded key:
    [`verify_tag_ssh_signatures.py`](phase1g_h_freeze_status_successor_logs/verify_tag_ssh_signatures.py),
    output
    [`verify_tag_ssh_signatures_output.json`](phase1g_h_freeze_status_successor_logs/verify_tag_ssh_signatures_output.json).
  - The script reimplements the OpenSSH SSHSIG check with the Python
    `cryptography` package, because `ssh-keygen` is not installed here. It
    also checks that a one-byte change of the signed payload is rejected.
  - Result: all eight Phase 1G signatures, 1G-A…1G-H, are valid for the
    same embedded key, and each tampered payload is rejected.
- **What the check shows.** The tag object is unchanged since it was
  signed, and the key that signed it signed the 1G-A…1G-G tags too.
- **What it does not show.** Whose key it is. Binding the key to the owner
  needs the owner's allowed-signers file (`git tag -v`), which this session
  does not have.
- **Relation to [FG].** For the F and G tags this check goes beyond [FG]
  Sec. 2.1, which checked only that the embedded keys were the same. That
  statement was correct for its session; [FG] is not edited.

### 2.2 Suite results: three provenances, kept distinct

| Run | Tree | Result | Source |
|---|---|---|---|
| Linux freeze preflight on the branch head before the merge | `1777ead`, whose tree equals that of the merge `728dfcd` | 1212 passed, 0 skipped, 0 failed on CPython 3.13.16 (363 s) and 3.11.17 (369 s), warnings as errors | [OD] inventory `validation` (scope: the final bytes of that commit except its own validation entry); the tag message gives the counts |
| Windows gate | not stated | reported passing ("tutto ok") | owner, 2026-10-09 ([OD] Sec. 2); interpreters, counts and commit not stated |
| This session, on this record's commit (documentation only on top of `728dfcd`) | this commit, except its validation entries | 1212 passed, 0 skipped, 0 failed on CPython 3.13.16 and 3.11.17 (614 s each, run concurrently), warnings as errors; 1F-C-R validator PASS (61 JSON round trips); 750 tolerance comparisons, none missing; `git diff --check` clean | session run, 2026-10-13; inventory `validation` |

## 3. Superseded status statements

Each row quotes the historical statement literally, with line wrapping
normalised. Each statement was correct when written; the current reading
follows from Sec. 2. The files are not edited. The map is not claimed to be
exhaustive.

The five audit records describe remote heads and publication states
observed at their own dates. Those are audit observations, correct then,
and are not mapped one by one (as [FG] S11–S12).

| # | Document (SHA-256 at `728dfcd`) | Location | Historical statement (literal) | Written | Current reading (2026-10-13) |
|---|---|---|---|---|---|
| T1 | `phase1g_h_global_variance_closure.md` (`25189497…`) | header, l. 13–15 | "not merged into `main` when this text was last revised. Last recorded push of the session branch: P17 (`027b7a4..22ace89`, 2026-10-09); later events are recorded there, not here" | 2026-10-09 | Merged by PR #5 and frozen at `728dfcd`, tag `phase-1g-h-global-variance-closure-v1`. The last recorded push is P18 (`22ace89..1777ead`). Events after the freeze are recorded in this record, not in the frozen [PUB]. |
| T2 | same | Sec. 1, l. 124–125 | "Nothing else is approved: no pull request, merge, tag, freeze, release or audit (Sec. 9, H-OD5)." | 2026-10-06 | The audits were approved later and performed. The pull request, merge, freeze and tag were decided on 2026-10-09 and performed (Sec. 2). No release exists. |
| T3 | same | Sec. 9, H-OD5, l. 1248–1251 | "*Pull request, merge, freeze and tag decided* (owner, 2026-10-09): … The resulting hashes are recorded by a later successor." | 2026-10-09 | Performed. The hashes are in Sec. 2 of this record. |
| T4 | same | Sec. 12, l. 1367–1368 | "decided for merge, freeze and tag" | 2026-10-09 | Merged, frozen and tagged at `728dfcd`. |
| T5 | `phase1g_h_global_variance_closure_inventory.json` (`864c9d99…`) | `publication.last_recorded_event`, `publication.main`, `publication.decided_not_yet_performed_when_committed`, `publication.h_od5_status`, `owner_decisions_status_2026_10_09.H-OD5` | `"id": "P17"`; `"8d3cdd0533035858c42269cb1dff1a20dcafc7da (unchanged)"`; the list of five actions starting with P18; `"decided 2026-10-09: pull request, merge, freeze and tag …"`; `"… Windows gate, pull request, merge, freeze and tag open"` | 2026-10-09 | Last recorded push P18. `main` = `728dfcd`. The five actions were performed (Sec. 2). The Windows gate was reported passing ([OD] Sec. 2). Machine-readable reading in this record's inventory, `current_integration_state`. |
| T6 | `phase1g_h_global_variance_closure_validation.md` (`9785b35d…`) | l. 62–63 | "`main` is unchanged. No tag, branch D v2, pull request or release was created." | 2026-10-06, corrected 2026-10-07 | `main` is now `728dfcd` (PR #5), and the tag exists (Sec. 2.1). Still true: no D v2 tag or branch, no release. |
| T7 | `phase1g_h_owner_decisions_successor.md` (`b97064c2…`) and inventory (`ba04fabc…`) | Sec. 4, l. 68–69; inventory `decisions.H-OD5.tag` | "The session cannot sign with the owner's key, so the tag is unsigned (the F/G tags are SSH-signed by the owner)."; `"signed": false` | 2026-10-09 | The session's push of its unsigned tag was refused (Sec. 2.1). The owner created the tag and SSH-signed it with the key of the F/G tags. **The tag is signed.** |
| T8 | same | Sec. 4, l. 79–81; inventory `decisions.H-OD5.hashes` | "As with the F/G freeze, a later successor records them, together with the push of this record (P18)." | 2026-10-09 | This record, Sec. 2. |
| T9 | `phase1g_h_publication_successor.md` (`fc4ce8f6…`) and inventory (`3b4f7702…`) | Sec. 11.2–11.3, l. 329–344; inventory `addendum_2026_10_09_after_p17.decided_not_yet_performed`, `.state_after_p17` | "Decided, not yet performed when this section is committed"; "`main` = `8d3cdd0…` (unchanged)"; "`ccr-555e67be-u11yht` = `22ace89` on `origin`; this section's commit is a later local commit" | 2026-10-09 | Performed: P18, PR #5, the merge `728dfcd` and the tag (Sec. 2). `main` = `728dfcd`. The commit carrying that section was pushed in P18. Tags on `origin`: 78 refs, 39 annotated (the new one is Sec. 2.1). |
| T10 | `phase1g_h_delta_audit_4_remediation_inventory.json` (`60a987ea…`) | `open_items[1]`, `open_items[2]` | "Windows gate (CPython 3.14.3 / 3.11.9)"; "owner decisions H-OD1 ... H-OD5" | 2026-10-09 | Both done in [OD] (Windows gate reported passing; H-OD1…H-OD5 decided). The other open items are unchanged: a uniform 1G-B scalar-precision policy is optional, and level C is not reached. |
| T11 | `README.md` (`4d5815f8…`), `CLAUDE.md` (`6ae6d5f9…`) | README l. 145–155; CLAUDE l. 17, l. 108–112, l. 481–506 and l. 572–575 | "last recorded push P17, `22ace89`"; "whose hashes a later successor records"; "1G-H decided for merge, freeze and tag on 2026-10-09"; "freeze and tag `phase-1g-h-global-variance-closure-v1` are decided"; "1G-H (proposed; …"; "with the hashes recorded by a later successor"; "the annotated, unsigned tag"; "The hashes are recorded by a later successor." (separate phrases) | 2026-10-09 | Current documentation: updated directly in the same commit as this record, pointing here. |

**Readings explicitly not changed:**
- The tag message lists "the publication successor (P1-P17)". That is
  correct: [PUB] records P1–P17, and P18 is recorded here.
- Five commits stay distinct:
  - `a243bf1`, the last code commit validated in the fourth remediation;
  - `22ace89`, its documentation commit (P17);
  - `1777ead`, the owner decisions commit (P18) and the branch head merged;
  - `728dfcd`, the merge, which is the frozen checkpoint;
  - `1ef6f3e`, the tag object.
- The tag `phase-1g-b-lagrangian-sigma-v1` still points at `fb5d952`. The
  1G-B contract-hardening successor is part of the 1G-H checkpoint, not a
  new 1G-B phase or tag.

## 4. What the freeze does and does not mean

- **What it attests.** The checkpoint `728dfcd`, within its documented
  perimeter. That perimeter is the records frozen by [OD] Sec. 4, each with
  its inventory and logs:
  - the report, its inventory and validation record;
  - the five remediation records;
  - [PUB] and [OD];
  - the 1G-B contract-hardening successor.

  It also covers the five audit records, which were never edited, and the
  runtime, evidence, tests and configurations at that commit.
- **What the owner decided** (H-OD1…H-OD4), unchanged:
  - the formal tangent statistic is a named research proposal, not the
    project's σ8 analogue;
  - there is no physical reference value;
  - no status token changes;
  - `global_variance.py` stays experimental, imported by no other module.
- **What it does not do.** It derives no σ8, adds no observational
  statistic and grants no observational status.
  - `SIGMA8_AUTHORIZATION`, `FSIGMA8_AUTHORIZATION`, `RSD_AUTHORIZATION`,
    `OBSERVATIONAL_AUTHORIZATION` and `UNIQUE_TIMESCAPE_PREDICTION`
    remain `NOT_GRANTED`.
  - `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` remains `NOT_DERIVED`.
  - No release exists.
- **Later work.** A correction of a frozen 1G-H result needs its own traced
  successor. Publication events after this record's commit are recorded by
  later records, if any are written.

## 5. Files

| File | Change |
|---|---|
| `reports/phase1g_h_freeze_status_successor.md` | this record (new) |
| `reports/phase1g_h_freeze_status_successor_inventory.json` | its companion (new) |
| `reports/phase1g_h_freeze_status_successor_logs/` | the state log, the signature-check script and its output, the two suite summaries (new) |
| `README.md`, `CLAUDE.md` | current-status text only, linking here |

Unchanged: every 1G-H report, inventory, validation record, audit, log and
evidence file; every package module, script and test; every status token;
every tag.

## 6. Reproduction

```bash
git fetch --tags origin
git rev-parse 728dfcd^{tree} 1777ead^{tree}   # both 9f020ba18f986baeb1ccd4cd748eeea19fd62e33
git log -1 --format=%P 728dfcd                # 8d3cdd0… 1777ead…
git rev-parse phase-1g-h-global-variance-closure-v1             # 1ef6f3ee…
git rev-parse 'phase-1g-h-global-variance-closure-v1^{commit}'  # 728dfcd3…
git ls-remote origin 'refs/tags/phase-1g-h-*'
git cat-file -p phase-1g-h-global-variance-closure-v1
python3 reports/phase1g_h_freeze_status_successor_logs/verify_tag_ssh_signatures.py  # needs the cryptography package
git tag -v phase-1g-h-global-variance-closure-v1   # with the owner's allowed-signers file
```
