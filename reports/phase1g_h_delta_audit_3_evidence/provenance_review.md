# Third 1G-H delta audit: provenance, governance and document review

This is a read-only review of `e5170285e1d4b4aa72e907a3a79110d05584c0d9` →
`ed0ec0c9c8783519a53759a265b6ce37e6c0e607`. It does not authenticate private
chat transcripts, inspect Claude sessions, or make remote writes. Source
content and provenance findings do not independently prove physical claims.

## Verified object and preservation

The three parents and all four trees match the commission exactly. The
complete delta contains exactly 34 paths, 14 modified and 20 added: the
expected three source/test/script files, the named current summaries and
historical annotation files, and the two new remediation records plus their
18 logs. No unexpected path appears. Source/script differences are a typed
binding repair, input conversion, docstrings and the gate's `kind` label;
there is no altered scientific equation or gate threshold.

The following are byte-identical: 184 files of all three earlier audits
against `e517028`; all 57 pre-existing package files and 111 frozen 1G report
files against `8d3cdd0`; the runner and its three configs against `e517028`.
The live status registry and 1G-B module are among these preserved package
files. The current H inventory's `results`, `two_phase_covariance`,
`status_tokens`, `observational_authorizations`, `assumptions`, `equations`,
`definition`, `anchoring` and `missing_input` are structurally identical to
the base.

All 54 top-level report JSON files parse with unique keys and no non-finite
constants. All 22 required SHA-256 checks agree: seven H `files.added`
entries, three third-remediation entries at the audited head, and twelve
first-remediation entries at the explicitly identified historical `89cb041`.
This verifies those declarations, not the artifact raw-run hash on a
different interpreter/environment.

## Remote snapshot and events

A read-only GitHub API snapshot observes 24 branch refs, including the five
requested heads: `main=8d3cdd0`, author branch `ed0ec0c`, second auditor branch
`e517028`, first auditor `816dd00`, delta auditor `5c325e1`. The 38 tag refs
are all annotated, and their exact names/object IDs equal the first delta
audit's saved API snapshot. Their locally authenticated peeled commits give
76 logical tag/peeled-ref entries; a fresh native `git ls-remote` is not
claimed. Four PRs exist, all closed and none from a 1G-H branch; no release or
forbidden D-v2 ref is observed.

The P7, P9, P10 and P11 ancestry intervals contain exactly the recorded
commits. This verifies graph compatibility with the recorded fast-forwards.
Current refs and commit ancestry cannot independently recover the actor,
date, or preceding remote head of a historical push. P10 and P11 approvals
are directly confirmed by the owner in this audit's handoff. P9's words are
explicitly secondary evidence from a pasted transcript; they remain
`NOT_VERIFIABLE` by this auditor. That limit is not evidence of unauthorized
publication. Historical GH-F15 remains resolved by the direct confirmation
recorded in the prior auditor's report; the present handoff does not repeat
P1/P2 separately. No approval extends to this audit's new push.

The P7–P10 successor tables correctly explain every superseded statement
listed in GH-D2F1. P11 nevertheless leaves the current summaries naming
`4bf2718` as the remote head, while the verified remote head is `ed0ec0c`.
The audit can itself acknowledge P11 chronologically, but existing summaries
still need their conventional wording corrected. Record P11 once in a later
successor with the current direct owner confirmation; describe `4bf2718` as
"last recorded push event P10" rather than an unqualified current remote
head. A snapshot with an observation time can identify current remote state
separately. This avoids endlessly adding a commit merely to document its own
publication. It requires no new publication authority.

## Historical note policy

All four older remediation MD/JSON changes contain additions only: no old
line is removed. The first record explicitly narrows its historical
"same shared constraints" and points its old hashes to `89cb041`. The
second record's new note states the corrected counts and P7 successor.
Original complete files remain available in Git at the frozen audit base.
This is acceptable for these unfrozen records under the authorized
remediation plan, but repeated layered notes are becoming cumbersome. Prefer
one chronological successor as the canonical current status, with short
pointers from historical records; do not require wholesale old-file editing
or demand a new owner decision solely for this stylistic recommendation.

## Preliminary finding/errata resolutions

- GH-D2F1: `PARTIALLY_RESOLVED`. Original P7 coverage and P8/P9 provenance
  distinctions are present; P10 is recorded, but P11 recreates stale current
  publication wording.
- GH-D2F2: defer mutation/test adjudication to the implementation review.
  The H25 wording and its `numerics` relocation are correct: assembly
  consistency is useful but does not independently test the shared kernels.
- GH-D2F3: documentary `RESOLVED`; GH-D2E1's replacement is present,
  identifies physical versus gate leaves, treats six renames separately
  from 100 additional leaves, and states the 1e-12 relative threshold. The
  inventory recount exactly equals the saved recount log. The numerical
  review independently flattened the newly regenerated `248a06b` artifact
  against the saved complete `89cb041` CPython-3.12 artifact and reproduced
  every count and the exact maximum absolute differences.
- GH-D2F4: `PARTIALLY_RESOLVED`. The named recomputed floats and scalar inputs
  are protected, but the implementation reviewer reproduced non-JSON
  serializable imported quadrature fields embedded in a genuine H result.
  The universal serialization claim is false; this is an inherited hole
  missed by the preceding audit and now contradicted by a new broad claim.
- GH-D2F5: `RESOLVED`; the requested pointer, narrower constraint and
  historical hash scope are explicit without removing old text.
- GH-D2F6: wording is appropriately restricted to the latent-Gaussian
  constructions and their two-point covariance parameters; final scientific
  adjudication belongs to the independent reconstruction.
- GH-D2E1: `APPLIED`; the independent numerical recount matches every count.
- GH-D2E2: `APPLIED`; P7 and the corresponding dated notes are present.

There is no documentary/status regression in GH-F1–F15 or GH-DF1–DF6. The
prior owner-decision outcomes are retained as historical evidence, with no
new observational authorization. Serialization incompleteness is not a
regression of scientific input binding: accepted equal-valued non-native
scalar representations change the export contract rather than the
recomputed physical value.

## New corrections proposed for root adjudication

`P11_STATUS` (LOW, GOVERNANCE, relates_to GH-D2F1, CORRECTION): the remotely
published documentation commit is absent from the publication ledger and
current summaries state the preceding head. Locations: README.md 146–147;
CLAUDE.md 466–468; H report header line 13; H inventory
`publication.pushed_head_2026_10_09` and `owner_decisions_status_2026_10_09`;
publication successor §7 and its companion. Apply the dated-event convention
above. This is not an approval or scientific blocker.

`STRICT_JSON_SCOPE` (implementation reviewer supplies severity and finding):
new universal claims overstate actual exported-record validation. Exact
errata candidates:

1. Third remediation §1: "Fail-closed, and strict JSON holds by construction".
2. Third remediation §2 GH-D2F4: "The 1G-B records the runtime imports already
   store floats and are unchanged."
3. H report §10 and module top-level docstring: "A float result must be stored
   as a float, and validated scalar inputs are stored as floats, so the
   records serialise as strict JSON (GH-D2F4)."

Correct reading: the tested H recomputed float fields are typed/finite and
the two named H input records are converted; imported public records do not
all store normalized Python scalars, and genuine nested H exports can fail
strict `json.dumps`. Fix those conversions under owner-authorized scope, or
narrow the contract and reject unsupported representations consistently;
add nested serialization coverage. No frozen pre-existing module should be
edited by this report-only audit.

`INT_JSON_RATIONALE` (INFO DOCUMENTATION erratum): new `_same` docstring says
"an equal ``Fraction`` or ``int`` would pass the comparison but break the
strict-JSON contract of ``to_json_dict``". A Python `int` is a strict-JSON
number. Fraction/non-native scalars can break JSON; integer rejection is
instead the declared float-result typing policy. Preserve that policy if
intended but correct the rationale. The accompanying documentation check
shows `json.dumps({'x':1}, allow_nan=False)` succeeds.

## AGENTS rules 1–10

| Rule | Third-remediation assessment |
|---|---|
| 1 | No equation change is in this delta; authorized remediation is binding/tests/documents |
| 2 | Existing equation references preserved; new binding logic is validation, not a new physical equation |
| 3 | Changes are representation/binding and evidence labeling; numerical equivalence checked separately |
| 4 | Units, normalization, ICs, independent variables and signs unchanged |
| 5 | Seven new tests present; strength assessed by the implementation stream |
| 6 | No upstream source appears among changed/added paths; no upstream redistribution |
| 7 | P10/P11 separately directly confirmed; P9 secondary evidence limitation explicit; audit push unauthorized |
| 8 | Existing typed pure-function/frozen-record design retained |
| 9 | Gate thresholds, binding rtol, orthant controls and radial grid unchanged |
| 10 | No introduced warning suppression; logs use -W error |

Pinning gate thresholds in a regression test protects declared policy
against accidental weakening. It need not make them immutable: a later
explicit approved policy change can update the declaration and its test
together. The current task asks no such change.

Proposed area verdicts: PROVENANCE `ACCEPT`; GOVERNANCE and DOCUMENTATION
`ACCEPT_WITH_CORRECTIONS`; TASK_COMPLIANCE `ACCEPT` within this reviewed
scope. Overall science/test/numerical judgments remain with the root auditor.

The H report §9 H-OD4 (lines 1102–1105) says “Its test gaps are closed
(GH-D2F2)”. This is the author's remediation conclusion within a dated
status paragraph, not a new outcome independently rendered by the second
auditor. Read it as “the named suggested tests were added”; new mutation
and serialization gaps are adjudicated by this audit. This qualification
is included with the serialization/test discussion, not a separate finding.
