# Phase 1G successor record — six status-token additions and the 1G-B limitation

Record classification: `APPROVED_SCIENTIFIC_STATUS_ADDITION_SUCCESSOR_RECORD`.
Parent checkpoint: `8cf5c49` (Phase 1G-E audit), local branch
`phase-1g-status-approvals`. Date: 2026-09-29.
Machine-readable companion:
[`phase1g_status_additions_successor_inventory.json`](phase1g_status_additions_successor_inventory.json).

[GM] = Galoppo & Mourier, arXiv:2511.17160v2 (JCAP 02 (2026) 066).
[1G-C] = [`phase1g_c_two_scale_growth_law.md`](phase1g_c_two_scale_growth_law.md).
[1G-D] = [`phase1g_d_separate_universe_growth.md`](phase1g_d_separate_universe_growth.md).
[1G-B] = [`phase1g_b_lagrangian_sigma_validation.md`](phase1g_b_lagrangian_sigma_validation.md).
[1G-E] = [`phase1g_e_two_phase_sigma.md`](phase1g_e_two_phase_sigma.md).
Precedent: [`phase1g_a_barotropic_status_successor.md`](phase1g_a_barotropic_status_successor.md),
which *changed* one token. This record *adds* six and changes none.

## 1. The additions

| Token (`scientific_status.py`) | Value | Evidence | Proposed in |
|---|---|---|---|
| `TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW` | `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` | [1G-C] Sec. 5, narrowed by [1G-D] Sec. 9 | [1G-C] Sec. 10 item 2 |
| `SUPER_CELL_TO_SUB_CELL_GROWTH_TRANSITION` | `NOT_DERIVED` | [1G-C] Sec. 8 (see [1G-D] Sec. 8) | [1G-C] Sec. 10 item 2 |
| `GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY` | `FAILED_FOR_TIMESCAPE_TRACKER` | [1G-D] Sec. 5 | [1G-D] Sec. 11 item 1 |
| `TWO_SCALE_SUPER_CELL_GROWTH_LAW` | `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` | [1G-D] Sec. 6 | [1G-D] Sec. 11 item 1 |
| `VOID_ONSET_RESPONSE` | `EXTERNAL_CLOSURE_INPUT` | [1G-D] Sec. 7 | [1G-D] Sec. 11 item 1 |
| `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` | `NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY` | [1G-D] Sec. 9 | [1G-D] Sec. 11 item 1 |

Each token has an adjacent comment in `scientific_status.py` that cites its
report section and the approval date. The frozen 1F-C-R snapshot
(`phase1f_c_r_astra_audit_remediation_inventory.json`,
`current_scientific_status`) has no entry for any of them, so they are
additions, not changes.

**Meanings.**
- `TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW`: under [1G-C]'s assumptions
  A1–A4, linear sub-cell perturbations of the wall matter grow as the EdS
  growing mode of the wall region in the common time t. [1G-D] Sec. 9
  narrows the reading: the law gives the *wall-internal* linear statistic,
  relative to the wall mean, not a global-mean σ at 8 h⁻¹ Mpc.
- `SUPER_CELL_TO_SUB_CELL_GROWTH_TRANSITION`: the transition *law* (its
  shape) is not derivable from the self-similar tracker. [1G-D] Sec. 8
  derives a conditional transition *length scale* R* from a
  peak-background-split void response, but not the law.
- `GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY`: the separate-universe
  (k → 0) modes are exact solutions of [GM] (4.9)–(4.11) with
  `Δ_eff/Δ_d < 0` and `P̃_eff ≠ 0`. [GM]'s comoving (`Δ_eff/Δ_d = +0.18…+0.20`,
  `P̃_eff = 0`), Mészáros (`Δ_eff = 0`) and barotropic (`P̃ = c²_s Δ_eff`)
  closures are inconsistent with them. So the volume-average CGI growth is
  not Timescape's long-wavelength growth.
- `TWO_SCALE_SUPER_CELL_GROWTH_LAW`: `D_SU(t) = f_w D_wall + A_v a_LS f_v`
  for the primordial long-wavelength mode, under assumption S2, valid only
  for R > R*.
- `VOID_ONSET_RESPONSE`: `A_v = dε/dδ_L` is an external closure. The two
  estimates ([W09] seeding, 10⁵–10⁶; peak-background split, 2.9–4.7×10³)
  differ by orders of magnitude.
- `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC`: at 8 h⁻¹ Mpc the wall/void
  partition is non-perturbative (`A_v σ_LSS(R8) = 2.6–4.3`), so a linear,
  global-mean σ at that scale is not defined in the linear two-scale theory.
  The only linear statistic there is the wall-internal σ_wall.

**Scope.** These are classifications only:
- No existing token changes. `UNIQUE_TIMESCAPE_PREDICTION`,
  `OBSERVATIONAL_AUTHORIZATION`, `RSD_AUTHORIZATION`, `SIGMA8_AUTHORIZATION`
  and `FSIGMA8_AUTHORIZATION` stay `NOT_GRANTED`;
  `UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY` stays
  `REFUTED_HADAMARD_ILL_POSED` (the 1G-A record).
- No equation, initial condition, unit, sign convention, independent
  variable, normalisation, default or tolerance changes. [GM]'s comoving,
  Mészáros and barotropic runtimes are unchanged.
- The [1G-E] proposal `TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC` is not in the
  approved list and is **not** added.

## 2. Authorisation

The project owner wrote on 2026-09-29, verbatim: "let a sub-agent do the
fast-forwarding and all the things that needed my approval that I give now
to you for all of them". The lead resolved this into an exact list, which
this record applies:
1. the two tokens of [1G-C] Sec. 10 recommendation 2;
2. the four tokens of [1G-D] Sec. 11 recommendation 1;
3. the 1G-B documented limitation of [1G-D] Sec. 11 recommendation 2 (text
   only, no numerical change);
4. a fast-forward of `main` to this branch and a plain push of `main`.

AGENTS.md rule 1 is not engaged: no equation changes.

## 3. The 1G-B documented limitation (text only)

[1G-D] Secs. 5, 9, 10: `GrowthLaw.VOLUME_AVERAGE_CGI` implements [GM]'s
closure faithfully, but that closure fails the separate-universe consistency
test for the Timescape tracker; `WALL_REGIONAL_EDS_COMMON_TIME` computes the
wall-internal linear statistic relative to the wall mean, not a global-mean σ
at 8 h⁻¹ Mpc.

In `src/timescape_fsigma8/lagrangian_sigma.py`:
- The three `_CAVEATS` texts (comoving, Mészáros, wall) each gain a
  `limitation (Phase 1G-D Secs. …; added 2026-09-29)` clause stating the
  above and quoting the matching token. Results carry it in `model_caveat`,
  in `limitations` and in `to_json_dict()`.
- `_SCALE_DEPENDENCE_CAVEAT`, which every result carries, still says that the
  volume-average law applies to super-homogeneity modes ([1G-C]'s reading).
  It gains a clause saying that [1G-D] Secs. 5 and 9 narrow this reading.
  Otherwise one result would carry both a superseded claim and its
  correction without linking them.
- The module docstring and the `GrowthLaw` docstring gain the same statement.
- Every original text is kept verbatim as the start of its extended text
  (extended, never weakened). No equation, value, default, argument or
  status constant changes.

**Verification.**
- **AST.** With docstrings stripped (the validator's `executable_tree`
  transform) and every string constant masked, the AST is identical to
  `8cf5c49`. Exactly four string constants differ (the four texts above),
  and each new text starts with the old one.
- **Numbers.** `scripts/validate_phase1g_b_lagrangian_sigma.py` was run at
  `8cf5c49` and after the change, on both interpreters. All 21 gates pass,
  and the printed gate lines are identical. In the artifact, all 1494
  numeric leaves are bit-identical. Only three strings differ: two
  `limitations` entries and one `model_caveat`. One boolean also differed
  before the commit: the driver's `working_tree_changes_present` flag
  (Sec. 8).
- **Tests.** No existing test asserted the exact caveat text. The 1G-B
  naming firewall (no `sigma8`, `sigma_8` or `8hmpc` in output strings)
  still passes. The new texts write "sigma at 8 h^-1 Mpc" and
  `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC`, neither of which contains a
  forbidden token.

[1G-B] gains an appended, dated Sec. 14 that records this limitation.

## 4. Superseded readings (frozen texts unchanged)

| Location | Frozen text | Current reading |
|---|---|---|
| `phase1f_c_r_astra_audit_remediation_inventory.json` `current_scientific_status` | no entry for the six tokens | live additions (this record); the snapshot is unchanged and still checked |
| [1G-C] Sec. 10 item 2, Sec. 12; `phase1g_c_two_scale_growth_inventory.json` `status_tokens_changed` | proposal, "none applied"; `false` | true of the 1G-C checkpoint; approved and applied here |
| [1G-D] Sec. 11 items 1–2, Sec. 10 ("No code change is made here"), Sec. 12; `phase1g_d_separate_universe_inventory.json` `status_tokens_changed` | proposal, "none applied"; `false` | true of the 1G-D checkpoint; approved and applied here (tokens and 1G-B text) |
| [1G-B] Sec. 5 "Scale dependence", Sec. 13 "`scientific_status.py` is not edited" | CGI law for super-homogeneity modes; no token changed | true of the 1G-B checkpoint; narrowed by [1G-D] Secs. 5, 9 (appended Sec. 14) |

## 5. Validator: additions accepted only through a registered record

`scripts/validate_phase1f_c_r_astra_remediation.py` compared every live
token with the frozen 1F-C-R snapshot, allowing only the recorded changes.
A new token would fail that comparison (as a `KeyError`). The frozen
inventory is not edited. Instead:
- `STATUS_SUCCESSOR_RECORDS` now lists both records (the 1G-A one and this
  one).
- The new `successor_status_additions()` reads each record's
  `status_additions`. A record without that key adds nothing, so the 1G-A
  record stays byte-identical. This record carries an explicit empty
  `status_changes`, so `successor_status_changes()` is unchanged.
- `check_current_scientific_status(frozen, live, changes, *, additions)`
  requires, for each added token, that the **frozen snapshot does not hold
  it** (the historical check) and that the **live module holds the record's
  value**. Every other live token must be in the frozen snapshot and equal to
  it, or be a registered change.
- New failures: a token added by two records; a token both changed and
  added; an added token missing from the live module; an added token that
  the frozen snapshot already holds; a live value that differs from the
  record; and a live token that no record declares. The last one used to be
  a bare `KeyError` and is now a named assertion.
- Kept failures: a token superseded twice; a change naming a missing token;
  a frozen snapshot that no longer holds the old token; a live value that
  differs from the change record; drift of any uncovered token.
- `validate()` also reports `successor_status_additions`.

`additions` is a mandatory keyword argument. So the four calls in
`tests/test_barotropic_hadamard_refutation.py` now pass the registered
additions. All their assertions are unchanged, and the test also asserts
that the barotropic token is not among the additions.

## 6. Files changed

| File | Change |
|---|---|
| `src/timescape_fsigma8/scientific_status.py` | six new tokens, each with a comment citing its report section and the approval; module docstring names this record |
| `src/timescape_fsigma8/lagrangian_sigma.py` | four caveat texts extended, and two docstrings (Sec. 3); string constants only |
| `scripts/validate_phase1f_c_r_astra_remediation.py` | additions-aware live-status check (Sec. 5) |
| `tests/test_phase1g_status_additions.py` | new regression (Sec. 7) |
| `tests/test_barotropic_hadamard_refutation.py` | passes `additions=` to the extended helper; assertions unchanged |
| `reports/phase1g_b_lagrangian_sigma_validation.md` | appended Sec. 14 (dated limitation) |
| `reports/phase1g_status_additions_successor.md` | this record |
| `reports/phase1g_status_additions_successor_inventory.json` | its canonical companion |
| `CLAUDE.md`, `README.md` | σ-track entries name the six tokens and the 1G-B limitation |

Not changed: every frozen report and inventory (including the 1F-C-R
inventory, the 1G-A record and the 1G-C/1G-D/1G-E reports), `astra/`, every
other package module, test and script, and every equation and tolerance.

## 7. Regression

`tests/test_phase1g_status_additions.py` checks the following.
- **Tokens.** The six tokens hold their values, and none is in the frozen
  snapshot. The live key set is exactly the frozen set plus the six. Every
  other token equals the frozen one, apart from the 1G-A change, and the
  `NOT_GRANTED` tokens are unchanged.
- **Record.** It is canonical JSON with an empty `status_changes`, the
  verbatim approval and six additions. For each addition, the cited section
  heading exists in the cited report. That report proposed exactly
  `` `TOKEN = "VALUE"` ``, and its frozen inventory lists the same proposal
  under `recommendations_require_human_approval`.
- **Validator accepts.** The declared additions pass, the registry lists
  both records, and the change set is still the 1G-A token alone.
- **Validator rejects** (each asserted by message):
  - each of the six tokens left undeclared;
  - an undeclared new live token;
  - each token already present in the frozen snapshot;
  - each token with a live value that differs from the record;
  - an addition missing from the live module;
  - a token both changed and added;
  - an addition claimed by two records, and a change claimed by two records;
  - a tampered record value;
  - a record that tries to "add" an existing frozen token (`D3_VERDICT`).
- **1G-B limitation.** For each law (comoving, Mészáros, wall), a real
  `conditional_lagrangian_linear_sigma` result carries the extended caveat,
  in `model_caveat`, in `limitations` and in its JSON. The 8cf5c49 text is
  its verbatim prefix. The extended scale-dependence caveat is present, and
  the statuses are not relabelled.

All comparisons are exact; no numerical tolerance is involved.

## 8. Validation

Filled in after the runs; see the inventory's `validation` block.
