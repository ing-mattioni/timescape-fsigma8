# Phase 1G-H — publication status successor (2026-10-08)

Classification: `PUBLICATION_STATUS_SUCCESSOR` (provenance record; no
scientific content). Date: 2026-10-08.
Companion: [`phase1g_h_publication_successor_inventory.json`](phase1g_h_publication_successor_inventory.json).
Requested by: the independent audit (finding GH-F15) and the delta audit
([`phase1g_h_delta_audit.md`](phase1g_h_delta_audit.md) §§3 and 11, "publication
successor").

**Addendum of 2026-10-08 (after the second delta audit):** Sec. 6 records
events P7–P9 and supersedes the state of Sec. 3. Secs. 1–5 keep their
wording.

## 1. Purpose

This record states the publication events of Phase 1G-H after the dated
records that describe them as future or absent, and records the owner's
confirmation of the two push approvals of 2026-10-06. Earlier records keep
their wording: "Nothing is pushed", `"pushed": false` and "remediated
locally" were true when they were committed (Sec. 4 gives the current
reading). No historical byte is changed.

Two kinds of evidence are kept apart:

- **Remote facts**, verified read-only on 2026-10-08 (`git ls-remote`,
  commit ancestry, GitHub pull-request and release listings).
- **Authorisations**, which are the owner's words in a session chat. They
  are quoted verbatim; a repository check cannot verify them.

## 2. Events

| # | Date | Event | Remote evidence | Authorisation (owner's words, verbatim) |
|---|---|---|---|---|
| P1 | 2026-10-06 | Creation of `ccr-555e67be-u11yht` on `origin` at `0572e416504bcdfaa5831b6d482b687ef6fae582`, carrying `7900374`, `fd7331f` and `0572e41` above `8d3cdd0` | `0572e41` descends from `8d3cdd0` | «Sì, procedi con il push sul branch designato» |
| P2 | 2026-10-06 | Fast-forward of that branch to `d4d693d73f995e2245a5720be227273b3639eda9` (documentation of P1) | `d4d693d` is a child of `0572e41` | «Sì, correggi la documentazione e fai il push» |
| P3 | 2026-10-07 | Independent audit published on `phase-1g-h-independent-audit` at `816dd004763f8de1a8bb09cba9e427a1bd2bb3d1` (tree `759ab21d3a36eeada67c2943e155240dc631b77a`, parent `d4d693d`) | branch head `816dd00` | published by the owner (records of 2026-10-07) |
| P4 | 2026-10-08 | Confirmation of P1 and P2 (audit finding GH-F15), in answer to «GH-F15: confermi le due approvazioni di push registrate in precedenza?» | none (off-repository) | «Si, confermo» |
| P5 | 2026-10-08 | Fast-forward of `ccr-555e67be-u11yht` from `d4d693d` to `89cb041f901b51a3f90fa6831aab1b4553c1772c`, carrying `816dd00`, `c1b4482` (code) and `89cb041` (documentation) of the first remediation | push output `d4d693d..89cb041`; branch head `89cb041` | «Si, fai push» |
| P6 | 2026-10-08 | Delta audit published on `phase-1g-h-delta-audit` at `5c325e1fd05b343f6d5e93f931038794de4373a2` (tree `a5b810e81d125827a17a9cf87b013ead51232080`, parent `89cb041`; 110 added files, all under `reports/phase1g_h_delta_audit*`) | branch head `5c325e1`; `git diff --name-status 89cb041 5c325e1` | the owner's authorisation in the auditing session, as the owner reported it on 2026-10-08; that session's local commit `b4abbe8` is not on `origin` (the auditor reports the same tree) |

P4 and P5 are the owner's answers to two separate questions in the session
that wrote the phase. P4 was not given directly to the delta auditor, which
therefore kept GH-F15 `OPEN_OWNER_CONFIRMATION`; a later auditor may ask the
owner to repeat it.

## 3. State on 2026-10-08

- `main` = `8d3cdd0533035858c42269cb1dff1a20dcafc7da` (unchanged since the
  F/G freeze).
- `ccr-555e67be-u11yht` = `89cb041`. The delta-audit remediation
  ([`phase1g_h_delta_audit_remediation.md`](phase1g_h_delta_audit_remediation.md))
  is committed locally on top of `5c325e1` and is **not** pushed; its push
  needs a separate approval.
- `phase-1g-h-independent-audit` = `816dd00`; `phase-1g-h-delta-audit` =
  `5c325e1`.
- 38 annotated tags, unchanged (76 tag refs on `origin`).
- Pull requests #1–#4 are closed; none comes from a 1G-H branch. No release
  exists. No `phase-1g-d-separate-universe-growth-v2` tag or branch exists.

## 4. Current reading of the dated statements

| Statement (literal) | Location | Written | Current reading |
|---|---|---|---|
| "When these commits were made, nothing had been pushed." | `phase1g_h_global_variance_closure_validation.md` §2 | 2026-10-06 | P1 and P2 followed; the same paragraph describes them. |
| "Commits (local, on `ccr-555e67be-u11yht` on top of the audit commit `816dd00`) … Nothing is pushed." | `phase1g_h_audit_remediation.md` §0 | 2026-10-07 | Pushed by P5 (2026-10-08). |
| `"branch": "ccr-555e67be-u11yht (local; on top of the audit commit 816dd00)"`, `"pushed": false` | `phase1g_h_audit_remediation_inventory.json`, `commits` | 2026-10-07 | Pushed by P5. |
| "GH-F15 … *Open.* The two recorded approvals … still need the owner's confirmation" | `phase1g_h_audit_remediation.md` §2 and §4; its inventory | 2026-10-07 | Confirmed by the owner, P4. |
| "remediated locally the same day" / "remediated locally on top of it" | README.md, CLAUDE.md (1G-H entries at `89cb041`) | 2026-10-07 | Pushed by P5; both files are updated with this record. |
| "Nothing is pushed" of the delta-audit remediation | `phase1g_h_delta_audit_remediation.md` and its inventory | 2026-10-08 | Dated; a later record states its push, if approved. |

## 5. Limits

- The authorisations are quoted from session chats; the repository can
  confirm the resulting refs, not the words.
- A ref snapshot shows the current state, not every transient remote event.
- This record adds no scientific statement, token or authorisation; the five
  observational authorisations stay `NOT_GRANTED`.

## 6. Addendum of 2026-10-08 (after the second delta audit)

Added with the second delta-audit remediation
([`phase1g_h_delta_audit_2_remediation.md`](phase1g_h_delta_audit_2_remediation.md)),
as requested by the second delta audit
([`phase1g_h_delta_audit_2.md`](phase1g_h_delta_audit_2.md), GH-D2F1, erratum
GH-D2E2 and §11, "Recording P7" and "Recording GH-F15"). Remote facts were
verified read-only again on 2026-10-08 (`git ls-remote`, `git log`, GitHub
pull-request and release listings).

### 6.1 Events

| # | Date | Event | Remote evidence | Authorisation (owner's words, verbatim) |
|---|---|---|---|---|
| P7 | 2026-10-08 | Fast-forward of `ccr-555e67be-u11yht` from `89cb041` to `226e52d2e4157d0130b2a9dfaffd71834c6017d9`, carrying `5c325e1` (the delta audit), `248a06b` (code) and `226e52d` (documentation) of the delta-audit remediation | push output `89cb041..226e52d`; branch head `226e52d`, also verified by the second delta audit | «Fai push e prepara il prompt per un nuovo audit» |
| P8 | 2026-10-08 | The owner's direct confirmation of P1 and P2 to the auditor of the second delta audit; GH-F15 becomes `RESOLVED_OWNER_CONFIRMED` | none (off-repository); recorded in `phase1g_h_delta_audit_2.md` §5 (row GH-F15) and §11 | «Confermo le due approvazioni di push registrate (GH-F15)», as that audit records it |
| P9 | 2026-10-08 | Second delta audit published on the auditing session's designated branch `ccr-ac582de6-vho99i`, created at `e5170285e1d4b4aa72e907a3a79110d05584c0d9` (tree `45ce98f9d21e93e355ba25812063aec270700116`); its parent `6411650` (the blind checkpoint) is a child of `226e52d` | branch head `e517028`; `git log 226e52d..e517028` lists exactly `6411650` and `e517028` | the owner's instruction in the auditing session, as it appears in the transcript of that session that the owner pasted here on 2026-10-08: «Pubblichati i due commit (`6411650`, `e517028`) sul branch designato di questa sessione, `ccr-ac582de6-vho99i`» |

P8 is the confirmation that Sec. 2 says "a later auditor may ask the owner to
repeat": the remark that P4 "was not given directly to the delta auditor"
stays true of the first delta audit and no longer leaves GH-F15 open. The
local fast-forward of this session's branch to `e517028`, before the second
remediation, is not a remote event.

### 6.2 State on 2026-10-08 after P9 (supersedes Sec. 3)

- `main` = `8d3cdd0533035858c42269cb1dff1a20dcafc7da` (unchanged).
- `ccr-555e67be-u11yht` = `226e52d` on `origin`. The local branch carries, not
  pushed, `6411650` and `e517028` (the second delta audit) and the commits of
  the second delta-audit remediation; their push needs a separate approval.
- `ccr-ac582de6-vho99i` = `e517028`; `phase-1g-h-independent-audit` =
  `816dd00`; `phase-1g-h-delta-audit` = `5c325e1`.
- 38 annotated tags, unchanged (76 tag refs). Pull requests #1–#4 are closed
  and none comes from a 1G-H branch; no release exists. No
  `phase-1g-d-separate-universe-growth-v2` tag or branch exists.

### 6.3 Current reading of further dated statements

Sec. 4 continues with the statements that GH-D2F1 lists:

| Statement (literal) | Location | Written | Current reading |
|---|---|---|---|
| "Commits (local, on `ccr-555e67be-u11yht` on top of the delta-audit commit `5c325e1`) … Nothing is pushed." and "Push of the two commits of this remediation (needs a separate approval)" | `phase1g_h_delta_audit_remediation.md` §0 and §4 | 2026-10-08 | Pushed by P7; a dated note there points here. |
| `commits.branch` "(local; on top of the delta-audit commit 5c325e1)", `commits.pushed: false`, the push item of `open_items` | `phase1g_h_delta_audit_remediation_inventory.json` | 2026-10-08 | Pushed by P7. |
| "`ccr-555e67be-u11yht` = `89cb041` … is **not** pushed" | this record, Sec. 3, and its inventory `state_2026_10_08` | 2026-10-08 | Superseded by Sec. 6.2. |
| "dated; a later record states its push, if approved" | this record, Sec. 4, last row | 2026-10-08 | That later record is this addendum (P7). |
| H-OD5: "committed locally"; "Open: … the push of its commits" | `phase1g_h_global_variance_closure.md` §9 | 2026-10-08 | Updated in place with this addendum (the phase report is the current summary of an unfrozen phase). |
| `publication.pushed_head_2026_10_08`, `publication.not_done`, `publication.h_od5_status`, `owner_decisions_status_2026_10_08.H-OD5` | `phase1g_h_global_variance_closure_inventory.json` | 2026-10-08 | Updated in place with this addendum. |
| "delta-audited on 2026-10-08 and remediated locally" | README.md | 2026-10-08 | Updated with this addendum. |
| "(at `89cb041`…)"; "remediated locally on top of it" | CLAUDE.md | 2026-10-08 | Updated with this addendum. |

### 6.4 Limits

The limits of Sec. 5 apply. P9's wording comes from a pasted transcript of
another session; the repository confirms the branch and its commits, not the
words. The second delta audit shares the author's model family (its §12).
