# Phase 1G-E successor record — one status-token addition

Record classification: `APPROVED_SCIENTIFIC_STATUS_ADDITION_SUCCESSOR_RECORD`.
Parent checkpoint: `6f7937c` (approved Phase 1G status additions), session
branch `claude/zealous-rubin-1m3vf4`. Date: 2026-09-29.
Machine-readable companion:
[`phase1g_e_status_addition_successor_inventory.json`](phase1g_e_status_addition_successor_inventory.json).

[1G-E] = [`phase1g_e_two_phase_sigma.md`](phase1g_e_two_phase_sigma.md).
Precedents: [`phase1g_a_barotropic_status_successor.md`](phase1g_a_barotropic_status_successor.md)
(changed one token) and
[`phase1g_status_additions_successor.md`](phase1g_status_additions_successor.md)
(added six). This record *adds* one token and changes none. Neither
precedent record is edited.

## 1. The addition

| Token (`scientific_status.py`) | Value | Evidence | Proposed in |
|---|---|---|---|
| `TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC` | `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` | [1G-E] Sec. 2 (model, assumptions E1–E4), Secs. 3–4 (verification, numbers) | [1G-E] Sec. 6 item 3 |

The token has an adjacent comment in `scientific_status.py` that cites the
report section and the approval date. The frozen 1F-C-R snapshot
(`phase1f_c_r_astra_audit_remediation_inventory.json`,
`current_scientific_status`) has no entry for it, and neither earlier successor
record declares it, so it is an addition, not a change.

**Meaning.** The mass variance of the two-phase (wall/void) Timescape
universe in balls of radius 8 h⁻¹ Mpc,
`σ² = δ_v² σ²_part + σ²_int`, is derived only under [1G-E]'s assumptions:
- **E1** two phases: empty voids (the tracker's `ρ_v = 0`); walls carry all
  the mass at `⟨ρ⟩/f_w`, plus the linear wall-internal field of 1G-C;
- **E2** Boolean voids: Poisson-placed balls of one radius `a` at volume
  fraction f_v0 (`λ V_a = −ln f_w`);
- **E3** the wall field is statistically independent of the void geometry;
- **E4** the wall field's Eulerian map is an isotropic compression
  `s = f_w^{1/3}` (primary) or `s = 1` (bracket).

**Not meant.**
- Not an observational σ8 and not an authorisation of any kind:
  `SIGMA8_AUTHORIZATION` and the other `NOT_GRANTED` tokens are unchanged.
- Not a statement that the void population is derived: E2's radius (15 h⁻¹
  Mpc from [W09]) is an external input. A self-consistent void population is
  the subject of Phase 1G-F (report-only).
- Not a change to the linear σ numbers of 1G-A/1G-C or to the 1G-B runtime.

**Scope.** A classification only:
- No existing token changes; `UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY`
  stays `REFUTED_HADAMARD_ILL_POSED` and the six 1G-C/1G-D additions keep
  their values.
- No equation, initial condition, unit, sign convention, independent
  variable, normalisation, default or tolerance changes. No package module
  other than `scientific_status.py` changes.

## 2. Authorisation

The project owner's task statement of 2026-09-29 lists, verbatim, the owner
approvals it gives (only these):

1. "Add the status token TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION" (reports/phase1g_e_two_phase_sigma.md §6 item 3; assumptions E1–E4)."
2. "Commit to this session's working branch, push that branch, and open ONE draft pull request against main at the end."

and states that nothing else is approved, in particular: merging the pull
request; pushing to `main` or to any other branch; creating or pushing tags;
force-pushing; changing any existing status token, equation, initial
condition, unit, sign convention or tolerance; and editing frozen historical
reports or inventories.

This record applies approval 1. Approval 2 covers how this change reaches the
remote (one draft pull request from the session branch). AGENTS.md rule 1 is
not engaged: no equation changes.

## 3. Superseded readings (frozen texts unchanged)

| Location | Frozen text | Current reading |
|---|---|---|
| `phase1f_c_r_astra_audit_remediation_inventory.json` `current_scientific_status` | no entry for the token | live addition (this record); the snapshot is unchanged and still checked |
| [1G-E] Sec. 6 ("none applied; each requires human approval") item 3; `phase1g_e_two_phase_sigma_inventory.json` `status_tokens_changed` | proposal; `false` | true of the 1G-E checkpoint; approved 2026-09-29 and applied here |
| `phase1g_status_additions_successor.md` Sec. 1 "Scope" and its inventory `human_approval.not_approved_here` | the 1G-E proposal "is not in the approved list and is **not** added" | true of that record's checkpoint (`6f7937c`); approved separately 2026-09-29 and applied here |

## 4. Validator

`scripts/validate_phase1f_c_r_astra_remediation.py` gains one entry in
`STATUS_SUCCESSOR_RECORDS`: this record's inventory. Its logic is unchanged
(the additions mechanism of the precedent record, Sec. 5 there):
- the added token must be absent from the frozen snapshot, and the live
  module must hold this record's value;
- a token added by two records, a token both changed and added, and a live
  token that no record declares all still fail.

This record carries an explicit empty `status_changes`, so the change set is
still the 1G-A token alone.

## 5. Files changed

| File | Change |
|---|---|
| `src/timescape_fsigma8/scientific_status.py` | one new token with a comment citing [1G-E] Sec. 2, Sec. 6 item 3 and the approval; module docstring names this record |
| `scripts/validate_phase1f_c_r_astra_remediation.py` | registers this record (one tuple entry and a comment) |
| `tests/test_phase1g_e_status_addition.py` | new regression (Sec. 6) |
| `tests/test_phase1g_status_additions.py` | the three checks that pinned the registry to exactly two records and the live token set to exactly six additions now allow the later registered record; every original assertion about the six tokens is kept |
| `reports/phase1g_e_status_addition_successor.md` | this record |
| `reports/phase1g_e_status_addition_successor_inventory.json` | its canonical companion |
| `CLAUDE.md`, `README.md` | σ-track entries name the token and this record |

Not changed: every frozen report and inventory (including [1G-E], its
inventory and both precedent records), `astra/`, every other package module,
and every equation and tolerance.

## 6. Regression

`tests/test_phase1g_e_status_addition.py` checks, with exact comparisons only
(no numerical tolerance is involved):
- **Token.** The live value; absence from the frozen snapshot; the live key
  set equals the frozen set plus the six earlier additions plus this one; the
  `NOT_GRANTED` tokens and the 1G-A change are unchanged.
- **Record.** Canonical JSON; classification; empty `status_changes`; exactly
  one addition; the verbatim approvals and date; the cited section heading
  exists in [1G-E]; [1G-E] proposed exactly `` `TOKEN = "VALUE"` `` and its
  frozen inventory lists the same proposal under
  `recommendations_require_human_approval`; the assumptions E1–E4 of this
  record match the frozen [1G-E] inventory verbatim.
- **Validator accepts.** The registry is the three records in order; the
  addition is read from this record; the change set is still the 1G-A token.
- **Validator rejects** (each asserted by message): the token left
  undeclared; the token already present in the frozen snapshot; a live value
  that differs from the record; the token missing from the live module; the
  token claimed by this record and the precedent record at once; and a
  tampered record value.

## 7. Validation

Recorded in the inventory's `validation` block: the 1F-C-R validator
PASSes on both interpreters (CPython 3.13.12 and 3.11.15, Linux) and the
targeted status tests pass (78 on each). The full suites are recorded in the
session pull request.
