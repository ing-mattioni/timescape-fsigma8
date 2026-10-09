# Phase 1G-H — publication status successor (2026-10-08)

Classification: `PUBLICATION_STATUS_SUCCESSOR` (provenance record; no
scientific content). Date: 2026-10-08.
Companion: [`phase1g_h_publication_successor_inventory.json`](phase1g_h_publication_successor_inventory.json).
Requested by: the independent audit (finding GH-F15) and the delta audit
([`phase1g_h_delta_audit.md`](phase1g_h_delta_audit.md) §§3 and 11, "publication
successor").

**Addendum of 2026-10-08 (after the second delta audit):** Sec. 6 records
events P7–P9 and supersedes the state of Sec. 3. Secs. 1–5 keep their
wording. **Addendum of 2026-10-09:** Sec. 7 records event P10 and supersedes
the state of Sec. 6.2. **Second addendum of 2026-10-09 (after the third delta
audit):** Sec. 8 records events P11–P13, supersedes the state of Sec. 7.2 and
sets the convention for current summaries.

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

## 7. Addendum of 2026-10-09 (push of the second delta audit and its remediation)

Remote facts verified read-only on 2026-10-09 (`git ls-remote` before and
after the push, `git log`).

### 7.1 Event

| # | Date | Event | Remote evidence | Authorisation (owner's words, verbatim) |
|---|---|---|---|---|
| P10 | 2026-10-09 | Fast-forward of `ccr-555e67be-u11yht` from `226e52d` to `4bf2718e7557ace3fdc0abffaa73587f1162f776`, carrying `6411650` and `e517028` (the second delta audit) and `9ad5425` (code) and `4bf2718` (documentation) of the second delta-audit remediation | push output `226e52d..4bf2718`; branch head `4bf2718` (the remote head was `226e52d` immediately before) | «Sì, fai push» |

The authorisation answered the request to push the fast-forward to
`4bf2718` and then to record the event here. The record of P10 is itself a
later local commit; its push needs a separate approval.

### 7.2 State on 2026-10-09 after P10 (supersedes Sec. 6.2)

- `main` = `8d3cdd0533035858c42269cb1dff1a20dcafc7da` (unchanged).
- `ccr-555e67be-u11yht` = `4bf2718` on `origin`.
- `ccr-ac582de6-vho99i` = `e517028`; `phase-1g-h-independent-audit` =
  `816dd00`; `phase-1g-h-delta-audit` = `5c325e1` (all unchanged).
- 76 tag refs (38 annotated tags), unchanged. No pull request from a 1G-H
  branch, no release, no `phase-1g-d-separate-universe-growth-v2` tag or
  branch.

### 7.3 Current reading of further dated statements

| Statement (literal) | Location | Written | Current reading |
|---|---|---|---|
| "Nothing is pushed: the push of `6411650`, `e517028` and these two commits needs a separate approval." and "**Push** of `6411650`, `e517028` and the two commits of this remediation (needs a separate approval; …)" | `phase1g_h_delta_audit_2_remediation.md` §0 and §4 | 2026-10-08 | Pushed by P10; a dated note there points here. |
| `commits.branch` "(local; on top of the second delta-audit commit e517028)", `commits.pushed: false`, the push item of `open_items` | `phase1g_h_delta_audit_2_remediation_inventory.json` | 2026-10-08 | Pushed by P10. |
| "The local branch carries, not pushed, `6411650` and `e517028` … their push needs a separate approval." | this record, Sec. 6.2, and its inventory `addendum_2026_10_08_after_second_delta_audit.state_after_p9` | 2026-10-08 | Superseded by Sec. 7.2. |
| "Its remote head is `226e52d` …; the second delta audit … and its remediation are on the local branch and not pushed"; H-OD5 "Its remediation is committed locally on top of it" and "Open: the push of the second delta audit and its remediation" | `phase1g_h_global_variance_closure.md` header and §9 | 2026-10-08 | Updated in place with this addendum. |
| `publication.not_done` (push item), `publication.h_od5_status`, `owner_decisions_requested.H-OD5` | `phase1g_h_global_variance_closure_inventory.json` | 2026-10-08 | Updated in place with this addendum; `owner_decisions_status_2026_10_08` stays dated. |
| "remote head `226e52d`"; "which are applied locally and not pushed" | README.md | 2026-10-08 | Updated with this addendum. |
| "(remote head `226e52d`; … events P1–P9)"; "remediated locally on top of it (…, not pushed)"; "(2026-10-06 and 2026-10-08)" | CLAUDE.md | 2026-10-08 | Updated with this addendum. |

### 7.4 Limits

The limits of Sec. 5 apply: the repository confirms the refs, not the
owner's words.

## 8. Second addendum of 2026-10-09 (after the third delta audit)

Added with the third delta-audit remediation
([`phase1g_h_delta_audit_3_remediation.md`](phase1g_h_delta_audit_3_remediation.md)),
as requested by the third delta audit
([`phase1g_h_delta_audit_3.md`](phase1g_h_delta_audit_3.md), finding GH-D3F1
and §11). Remote facts were verified read-only on 2026-10-09 (`git ls-remote`,
`git log`).

### 8.1 Events

| # | Date | Event | Remote evidence | Authorisation (owner's words, verbatim) |
|---|---|---|---|---|
| P11 | 2026-10-09 | Fast-forward of `ccr-555e67be-u11yht` from `4bf2718` to `ed0ec0c9c8783519a53759a265b6ce37e6c0e607`, carrying only `ed0ec0c` (the record of P10) | push output `4bf2718..ed0ec0c`; branch head `ed0ec0c`, also observed by the third delta audit | «Sì, pubblica anche ed0ec0c» |
| P12 | 2026-10-09 | The owner's direct confirmation of P10 and P11 to the auditor of the third delta audit | none (off-repository); recorded in `phase1g_h_delta_audit_3.md` §3 | «Confermo le autorizzazioni P10 e P11», as that audit records it |
| P13 | 2026-10-09 | Third delta audit published on `phase-1g-h-delta-audit-3` at `18bf2fbef880fdfb3c292956aa1f000720930abf` (parent `4d71bd4`, the blind checkpoint, whose parent is `ed0ec0c`; 57 added files, all under `reports/phase1g_h_delta_audit_3*`). The publishing connector re-hashed the auditing session's local commits `c62ad87` and `d9342c4`; `4d71bd4` has the checkpoint tree `6d5e848faa7b72d829e44a9a2d79e70c3a34acb6` recorded in the audit's inventory | branch head `18bf2fb`; `git diff --name-status ed0ec0c 18bf2fb` | the owner's authorisation in the auditing session, as the handoff pasted here on 2026-10-09 reports it; no verbatim words are available in this session |

The pushes P10 and P11 are covered by separate approvals («Sì, fai push»,
«Sì, pubblica anche ed0ec0c»), and P12 confirms both directly to an auditor.
The local fast-forward of this session's branch to `18bf2fb`, before the
third remediation, is not a remote event.

### 8.2 State on 2026-10-09 after P13 (supersedes Sec. 7.2)

- `main` = `8d3cdd0533035858c42269cb1dff1a20dcafc7da` (unchanged).
- `ccr-555e67be-u11yht` = `ed0ec0c` on `origin`. The local branch carries, not
  pushed, `4d71bd4` and `18bf2fb` (the third delta audit) and the commits of
  the third remediation; their push needs a separate approval.
- `phase-1g-h-delta-audit-3` = `18bf2fb`; `ccr-ac582de6-vho99i` = `e517028`;
  `phase-1g-h-independent-audit` = `816dd00`; `phase-1g-h-delta-audit` =
  `5c325e1`.
- 76 tag refs (38 annotated tags), unchanged. No pull request from a 1G-H
  branch, no release, no `phase-1g-d-separate-universe-growth-v2` tag or
  branch.

### 8.3 Convention for current summaries

A commit cannot record its own push. From this addendum on, README.md,
CLAUDE.md, the header of `phase1g_h_global_variance_closure.md` and its
inventory name the **last recorded publication event** (P-number, range,
date) and point here; they no longer state the remote head as a current
fact. A later push is recorded once, in the next chronological addendum of
this record, and does not make those summaries false.

### 8.4 Current reading of further dated statements

| Statement (literal) | Location | Written | Current reading |
|---|---|---|---|
| "Its remote head is `4bf2718` (2026-10-09, P10)" | `phase1g_h_global_variance_closure.md` header | 2026-10-09 | Replaced with this addendum by the last recorded event (Sec. 8.3). |
| "remote head `4bf2718`" | README.md, CLAUDE.md | 2026-10-09 | Replaced with this addendum by the last recorded event. |
| `publication.pushed_head_2026_10_09` = `4bf2718` | `phase1g_h_global_variance_closure_inventory.json` | 2026-10-09 | Historical; `publication.last_recorded_event` is added with this addendum. |
| "`ccr-555e67be-u11yht` = `4bf2718` on `origin`" | this record, Sec. 7.2, and its inventory `addendum_2026_10_09.state_after_p10` | 2026-10-09 | Superseded by Sec. 8.2. |
| "The record of P10 is itself a later local commit; its push needs a separate approval." | this record, Sec. 7.1 | 2026-10-09 | Pushed by P11. |

### 8.5 Limits

The limits of Sec. 5 apply. P13's authorisation is reported, not quoted.
The third delta audit notes that current refs show state and ancestry, not
the actor or time of a historical push.

## 9. Third addendum of 2026-10-09 (push P14)

Added in a documentation commit after the push, by the convention of
Sec. 8.3. Remote facts were verified read-only on 2026-10-09 (push output,
`git ls-remote`).

### 9.1 Event

| # | Date | Event | Remote evidence | Authorisation (owner's words, verbatim) |
|---|---|---|---|---|
| P14 | 2026-10-09 | Fast-forward of `ccr-555e67be-u11yht` from `ed0ec0c` to `36d127f8edcb306aa503cb4d8b7b10417dc33a51`, carrying the third delta audit (`4d71bd4`, `18bf2fb`) and its remediation (`c6028e9`, 1G-H code; `6926a63`, 1G-B contract hardening; `36d127f`, documentation) | push output `ed0ec0c..36d127f`; branch head `36d127f` | «Sì, fai push» |

### 9.2 State on 2026-10-09 after P14 (supersedes Sec. 8.2)

- `main` = `8d3cdd0533035858c42269cb1dff1a20dcafc7da` (unchanged).
- `ccr-555e67be-u11yht` = `36d127f` on `origin`. The record of P14 (the
  commit carrying this section) is a later local commit; its push needs a
  separate approval.
- `phase-1g-h-delta-audit-3` = `18bf2fb`, now also an ancestor of the
  session branch; the other audit branches as in Sec. 8.2.
- Tags, pull requests and releases as in Sec. 8.2.

### 9.3 Current reading of further dated statements

| Statement (literal) | Location | Written | Current reading |
|---|---|---|---|
| "Nothing is pushed: the push of `4d71bd4`, `18bf2fb` and these three commits needs a separate approval." | `phase1g_h_delta_audit_3_remediation.md` Sec. 0, and the push item of its Sec. 4 | 2026-10-09 | Pushed by P14; a dated status note in that record points here. |
| "`ccr-555e67be-u11yht` = `ed0ec0c` on `origin`. The local branch carries, not pushed, …" | this record, Sec. 8.2, and its inventory `addendum_2026_10_09_after_third_delta_audit.state_after_p13` | 2026-10-09 | Superseded by Sec. 9.2. |
| "Last recorded publication event: P11" | README.md, CLAUDE.md, the 1G-H report header and inventory | 2026-10-09 | Updated to P14 with this addendum (Sec. 8.3). |

## 10. Fourth addendum of 2026-10-09 (P15, P16)

Added with the fourth delta-audit remediation
([`phase1g_h_delta_audit_4_remediation.md`](phase1g_h_delta_audit_4_remediation.md)),
as recommended by the fourth delta audit
([`phase1g_h_delta_audit_4.md`](phase1g_h_delta_audit_4.md), Sec. 3 and
Sec. 11). Remote facts were verified read-only on 2026-10-09
(`git ls-remote`, `git log`).

### 10.1 Events

| # | Date | Event | Remote evidence | Authorisation (owner's words, verbatim) |
|---|---|---|---|---|
| P15 | 2026-10-09 | Fast-forward of `ccr-555e67be-u11yht` from `36d127f` to `027b7a413fcee0786b861d5903272e4653d227ed`, carrying only `027b7a4` (the record of P14) | push output `36d127f..027b7a4`; branch head `027b7a4`, also observed by the fourth delta audit | «Pubblica, fai il fast-forward» |
| P16 | 2026-10-09 | Fourth delta audit published on `phase-1g-h-delta-audit-4` at `fc804a0f71f47904e86388f378295f72ba15cdd8` (parent `027b7a4`; 83 added files, all under `reports/phase1g_h_delta_audit_4*`). The auditing session reports that `fc804a0` has the tree and parent of its local commit `f332353` | branch head `fc804a0`; `git diff --name-status 027b7a4 fc804a0` | the owner's authorisation in the auditing session, as the handoff pasted here on 2026-10-09 reports it; no verbatim words are available in this session |

### 10.2 State on 2026-10-09 after P16 (supersedes Sec. 9.2)

- `main` = `8d3cdd0533035858c42269cb1dff1a20dcafc7da` (unchanged).
- `ccr-555e67be-u11yht` = `027b7a4` on `origin`. The local branch carries,
  not pushed, `fc804a0` (the fourth delta audit) and the commits of the
  fourth remediation; their push needs a separate approval.
- `phase-1g-h-delta-audit-4` = `fc804a0`; the other audit branches as in
  Sec. 8.2.
- 76 tag refs (38 annotated tags), unchanged. Four pull requests exist, all
  closed and none from a 1G-H branch; no release; no
  `phase-1g-d-separate-universe-growth-v2` tag or branch.

### 10.3 Clarification of the convention of Sec. 8.3

Current summaries name the **last recorded push of the session branch**:
the event that changes its remote head (P11, then P14, now P15). Audit
publications on their own branches and confirmations are recorded here but
do not move that pointer. Secs. 8 and 9 already applied the convention this
way: the summaries named P11 while P13 was the latest event. The push of the
fourth remediation will be recorded once, in the next addendum.

### 10.4 Current reading of further dated statements

| Statement (literal) | Location | Written | Current reading |
|---|---|---|---|
| "The record of P14 (the commit carrying this section) is a later local commit; its push needs a separate approval." | this record, Sec. 9.2 | 2026-10-09 | Pushed by P15. |
| "`ccr-555e67be-u11yht` = `36d127f` on `origin`." | this record, Sec. 9.2, and its inventory `addendum_2026_10_09_after_p14.state_after_p14` | 2026-10-09 | Superseded by Sec. 10.2. |
| "Last recorded publication event: P14" (and its equivalents) | README.md, CLAUDE.md, the 1G-H report header and inventory | 2026-10-09 | Updated to the last recorded push P15 (Sec. 10.3). |

## 11. Fifth addendum of 2026-10-09 (P17; pull request, merge and tag decided)

Added with the owner decisions successor
([`phase1g_h_owner_decisions_successor.md`](phase1g_h_owner_decisions_successor.md)).
Remote facts were verified read-only on 2026-10-09 (push output,
`git ls-remote`).

### 11.1 Event

| # | Date | Event | Remote evidence | Authorisation (owner's words, verbatim) |
|---|---|---|---|---|
| P17 | 2026-10-09 | Fast-forward of `ccr-555e67be-u11yht` from `027b7a4` to `22ace890caca5e571e83d322b446db3a05f78cc0`, carrying `fc804a0` (the fourth delta audit), `a243bf1` (tests) and `22ace89` (documentation) | push output `027b7a4..22ace89`; branch head `22ace89` | «fai il fast-forward di origin/ccr-555e67be-u11yht da 027b7a4 a 22ace89» |

### 11.2 Decided, not yet performed when this section is committed

The owner decided, on 2026-10-09, a pull request from `ccr-555e67be-u11yht`
into `main`, its merge, the freeze and the tag
`phase-1g-h-global-variance-closure-v1` («… e poi fai PR, merge, freeze e
tag»; owner decisions successor, Sec. 4). The push of this section's commit
(P18), the pull request, the merge commit and the tag are recorded by a
later successor, as for the F/G freeze.

### 11.3 State on 2026-10-09 after P17 (supersedes Sec. 10.2)

- `main` = `8d3cdd0533035858c42269cb1dff1a20dcafc7da` (unchanged).
- `ccr-555e67be-u11yht` = `22ace89` on `origin`; this section's commit is a
  later local commit.
- Audit branches, tags (76 refs, 38 annotated), pull requests (four, all
  closed, none from a 1G-H branch) and releases (none) as in Sec. 10.2.

### 11.4 Current reading of further dated statements

| Statement (literal) | Location | Written | Current reading |
|---|---|---|---|
| "Nothing is pushed: the push of `fc804a0` and these two commits needs a separate approval." | `phase1g_h_delta_audit_4_remediation.md` Sec. 0 and the push item of its Sec. 4 | 2026-10-09 | Pushed by P17; a dated status note in that record points here. |
| "`ccr-555e67be-u11yht` = `027b7a4` on `origin`. The local branch carries, not pushed, `fc804a0` …" | this record, Sec. 10.2, and its inventory `addendum_2026_10_09_after_fourth_delta_audit.state_after_p16` | 2026-10-09 | Superseded by Sec. 11.3. |
| "Last recorded push of the session branch: P15" (and its equivalents) | README.md, CLAUDE.md, the 1G-H report header and inventory | 2026-10-09 | Updated to P17. |
