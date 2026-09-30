# Phase 1G-B — owner decisions successor record

Record classification: `OWNER_DECISIONS_SUCCESSOR_RECORD`.
Parent checkpoint: `63ca316` (`main`, the merge of the Phase 1G audit pull
request), local branch `phase-1g-owner-decisions`. Date: 2026-09-30.
Machine-readable companion:
[`phase1g_b_owner_decisions_successor_inventory.json`](phase1g_b_owner_decisions_successor_inventory.json).

Cited as:
- [1G-B] = [`phase1g_b_lagrangian_sigma_validation.md`](phase1g_b_lagrangian_sigma_validation.md)
  (frozen) and `src/timescape_fsigma8/lagrangian_sigma.py`;
- [AUD] = [`phase1g_b_adversarial_audit.md`](phase1g_b_adversarial_audit.md)
  (findings GB-F1 … GB-F10; owner decisions OD1 … OD6);
- [CONS] = [`phase1g_adversarial_audit_errata_successor.md`](phase1g_adversarial_audit_errata_successor.md)
  (errata E-1GB-1 … -9 applied there; GB-OD1 resolved with option A, Sec. 10);
- [WIN] = [`phase1g_windows_validation_record.md`](phase1g_windows_validation_record.md).

These decisions are **code changes** ("These are code changes: apply them
only if ticked, with tests."). All five are ticked. None changes an
equation, a computed value, a default, a status token or a numerical budget
of the σ(M) chain; AGENTS.md rule 3 (demonstrable equivalence) is met in
Sec. 8. The frozen [1G-B] report, [AUD] and [CONS] are not edited.

## 1. Authorisation

The project owner's task statement of 2026-09-30 ("Phase 1G — Windows
validation, owner decisions for 1G-A/C/D/E, tags"), Sec. 0, gives these
approvals, verbatim:

1. "Create the local branch `phase-1g-owner-decisions` from `main` and commit there."
2. "Apply the owner decisions ticked `[x]` in Sec. 3, exactly as ticked. An unticked decision is **not** approved: leave it open and list it at the end."

Approvals 3–6 (local signed tags, push and pull request, merge, tag push) are
unticked and therefore not given.

**Ticks (verbatim, Sec. 3 "1G-B (optional, non-blocking)").** "[x] OD2
naming-firewall wording" · "[x] OD3 status-validator hardening" · "[x] OD4
contract hardening" · "[x] OD5 caveat on `TimescapeGrowthFactor`" · "[x] OD6
independent g_TS regression" · "These are code changes: apply them only if
ticked, with tests."

**GB-OD1** (the blocking GB-F1 test fix) was decided on 2026-09-30 with
option A and is on `main` (`738f3c3`, merge `63ca316`; [CONS] Sec. 10). The
auditor asked for it to be run on Linux and Windows; [WIN] records the
Windows run (both suites pass, including the changed test). With that, 1G-B
has no open blocking decision.

## 2. GB-OD2 — naming-firewall wording (GB-F4)

**Frozen text.** `CLAUDE.md` (Phase 1G-B exception): "No public name may
contain `sigma8`, `sigma_8` or `8hMpc`." `lagrangian_sigma.py` module
docstring: "no public function/class name or output key carries the
observational tokens; they appear only inside the negative status values
`SIGMA8_STATUS = "NOT_OBSERVATIONAL_SIGMA_8"` and `FSIGMA8_STATUS =
"NOT_FSIGMA8"`". [AUD] Sec. 4.3: `SIGMA8_STATUS` and `FSIGMA8_STATUS` are
public names in `__all__` that contain `sigma8`; the firewall test skipped
constants.

**Change (the audit's recommended wording, no rename).**
- `CLAUDE.md`: "No public function, class, member or output-key name may
  contain `sigma8`, `sigma_8` or `8hMpc` (case-insensitive). The negative
  status constants `SIGMA8_STATUS` and `FSIGMA8_STATUS`, whose values state
  the negation, are the only exception."
- The module docstring says the same.
- **Enforced**: a new test lower-cases every name in `__all__` (constants
  included, as the 1D-B growth firewall does) and requires the flagged set to
  be exactly `{SIGMA8_STATUS, FSIGMA8_STATUS}`, each with a value starting
  `NOT_`; the new `model_caveat` output (GB-OD5) is checked too.

**Not decided here.** [AUD] OD2 also asks whether 1D-C §19's "any spelling"
rule applies to caveat text ("sigma at 8 h^-1 Mpc" in the wall caveat). The
tick covers the wording; that sub-question stays open (Sec. 9).

## 3. GB-OD3 — status-validator hardening (GB-F5)

**Frozen behaviour** ([AUD] Sec. 4.9): a frozen token deleted from the live
module (`D3_VERDICT`, `SIGMA8_AUTHORIZATION`) passed silently; a change
record naming a token absent from the snapshot raised a bare `KeyError`; an
in-tree edit of the frozen inventory went undetected (only canonical bytes
were checked).

**Change** (`scripts/validate_phase1f_c_r_astra_remediation.py`):
- `check_current_scientific_status(..., removals=None)`: every frozen token
  must be in the live module unless a registered `status_removals` entry
  covers it (named failure "frozen token missing from the live module and
  removed by no successor record"). A removal must name a frozen token with
  its frozen value and be absent from the live module; it may not also be
  changed or added. `removals=None` is the strict case (no removal); no
  registered record has one (`successor_status_removals()` returns `{}`).
- A change naming a token absent from the snapshot fails by name ("successor
  record changes a token absent from the frozen snapshot").
- `check_frozen_inventory_pinned`: the frozen 1F-C-R inventory must be
  byte-identical to its blob at the certified commit `REMEDIATION`
  (`git show REMEDIATION:<inventory>`).
- `check_successor_records_canonical`: every registered status successor
  record must be canonical UTF-8/LF JSON (the optional item; all three are).
- The report gains `successor_status_removals`.

Every existing failure mode and message is kept; the existing tests pass
unchanged.

## 4. GB-OD4 — contract hardening (GB-F6)

All three optional items of [AUD] OD4 are applied; none changes a computed
value.
- **Array inputs.** `top_hat_window`, `eh98_zero_baryon_transfer` and
  `matter_era_linear_amplitude` accept only integer, unsigned or floating
  arrays. str, bytes, bool, complex and object inputs are refused
  (`LagrangianSigmaContractError`, "real numeric array") instead of being
  coerced or, for complex, truncated with a warning. Valid inputs are
  converted exactly as before (`np.asarray(value, dtype=float64)`).
- **EH98 validity range.** `EH98_OMEGA_M_FIT_RANGE = (0.025, 0.5)` (the
  stated range of [EH98] Eq. (26), `trans.tex` l. 686–687 as read by [AUD])
  is enforced: `eh98_zero_baryon_transfer` refuses ω_m outside it (for
  ω_m ≥ 9.83 the sound horizon was s ≤ 0). The baryon limits of the same
  source (Ω_b h² ≳ 0.0125; the no-wiggle form poor for Ω_b/Ω_0 ≳ 0.5) are
  documented, not enforced: f_b = 0 is the exact zero-baryon limit of
  Eq. (31) and is used as such. The production inputs (ω_m 0.120–0.143,
  f_b ≤ 0.2) are inside.
- **Record invariants** (budget `RECORD_IDENTITY_RTOL = 1e-13`, round-off
  only; observed ≤ 9e−16 for f_v0 ∈ [0.01, 0.99]):
  - `TimescapeGrowthFactor`: `gamma_w0 = 1 + f_v0/2` ([GM] text after
    Eq. (5.7));
  - `EarlyMatterDensityPerPhoton`: `gamma_w0 = 1 + f_v0/2`;
    `H_D0 = 2 H0 (2+f_v0)/(4+f_v0+4f_v0²)` ([W09] (B8)–(B9));
    `Ω̄_M0 = 4(1−f_v0)/(2+f_v0)²` ([W09] (B3)); `ω_m,bare = Ω̄_M0 (H_D0/100)²`;
    the per-photon closed form `½(1−f_v0)(2+f_v0)(H_D0/100)²`; and the stored
    residual equals `|ω_m,eff/closed − 1|` exactly (this rejects the audit's
    forging example `omega_m_per_photon = 0.3`);
  - `ResolvedLagrangianRadius`: the formula is the convention's own, and an
    explicit radius is the supplied one;
  - `ConditionalLagrangianSigma`: the radius is the one resolved from the
    record's own density.

## 5. GB-OD5 — caveat on `TimescapeGrowthFactor` (GB-F7)

**Frozen behaviour.** `TimescapeGrowthFactor.to_json_dict()` and the 1G-B
driver's `V1_growth` exported g and X with no caveat, although the 1G-D
limitation applies to them.

**Change.** `TimescapeGrowthFactor` has a new mandatory field
`model_caveat`, validated to equal the growth law's caveat (the same text as
`ConditionalLagrangianSigma.model_caveat`), and exported by `to_json_dict()`.
`timescape_growth_factor` fills it. The field has no default (the
"every field mandatory" contract test still holds, 12 dataclasses). The
driver artifact gains the 10 `model_caveat` strings of `V1_growth`; nothing
else in it changes (Sec. 8).

## 6. GB-OD6 — independent g_TS regression (GB-F9)

**New test** (`tests/test_phase1g_b_owner_decisions.py`,
`test_gb_od6_independent_g_ts_regression`). It imports nothing from the
package for the reference value:
- closed-form tracker ([GM] (5.5)–(5.7), D1-corrected; `f_v = t/(t+τ)`,
  `τ/t0 = f_w0/f_v0`), `Θt = 2 + f_v`, `4πG⟨ρ⟩t² = (2/3)(1−f_v)`,
  `4πGρ_eff t² = f_v(8+f_v)/6`, `w_eff = −(4−f_v)/(8+f_v)`;
- [GM] (4.21)–(4.23) (comoving) and (4.27) (Mészáros) in the normalised
  variables `x1 = Δ_d t^{−2/3}`, `x2 = −Z t^{1/3}`, `x3 = Δ_eff t^{−2/3}`,
  from t_e = 10⁻¹² t0 on the regular mode, DOP853 (rtol 1e−12, atol 1e−14);
- g_TS = 0.40266226 (comoving) and 0.34169348 (Mészáros) for the [GM] preset,
  equal to [AUD]'s independent values to their eight printed decimals.

The package's g carries its documented early-start bias (1.8e−6 and 2.1e−6
in ln g; budget 3e−6); after subtracting the package's own
`log_growth_early_limit_linear_bias_estimate` the two agree to ≤ 2e−10
(budget 1e−9). Measured on Windows (both interpreters): see Sec. 10.

## 7. Tests

`tests/test_phase1g_b_owner_decisions.py` (new; 32 tests): the naming rule
and its `CLAUDE.md` wording (OD2); deletion, removal, absent-token change,
pinned inventory and canonical records (OD3, each asserted by message);
refused array inputs, exact conversion of valid ones, the EH98 range and its
boundaries, and every record invariant (OD4); the growth caveat per law
(OD5); the independent g_TS (OD6); and this record's inventory. No existing
test or assertion is changed.

## 8. Equivalence (AGENTS.md rule 3)

- The 1G-B validation driver (`scripts/validate_phase1g_b_lagrangian_sigma.py`),
  run before and after the change: all 21 gates pass; the artifact's 1471
  numeric leaves are bit-identical; the only additions are the 10
  `model_caveat` strings of GB-OD5; the only other string that differs is
  the `working_tree_changes_present` provenance flag.
- The existing 1G-B tests (92) and status tests pass unchanged.
- No computation path changed: the new checks run after the values are
  computed, and the array check converts valid inputs exactly as before.

## 9. Open items (not decided here)

- [AUD] OD2 sub-question: does 1D-C §19's "any spelling" rule apply to caveat
  text?
- [AUD] OD4's forging route through `dataclasses.replace` of a
  `TimescapeGrowthFactor` with an arbitrary g (deliberate misuse) remains
  possible; the invariants bind only closed forms.

## 10. Files changed, validation and tag readiness

| File | Change |
|---|---|
| `src/timescape_fsigma8/lagrangian_sigma.py` | OD2 docstring; OD4 array check, EH98 range, record invariants (two new public constants `RECORD_IDENTITY_RTOL`, `EH98_OMEGA_M_FIT_RANGE`); OD5 `TimescapeGrowthFactor.model_caveat` |
| `scripts/validate_phase1f_c_r_astra_remediation.py` | OD3 |
| `tests/test_phase1g_b_owner_decisions.py` | new regression (OD2–OD6) |
| `CLAUDE.md` | OD2 wording |
| `reports/phase1g_b_owner_decisions_successor.md`, `_inventory.json` | this record |

- **Driver.** `scripts/validate_phase1g_b_lagrangian_sigma.py`: 21/21 gates
  PASS before and after on both interpreters; numeric leaves bit-identical
  (Sec. 8).
- **Regression.** `tests/test_phase1g_b_owner_decisions.py` (32 tests) and
  the unchanged 1G-B, status and 1F-C-R tests pass on both interpreters.
- **Final runs** (both full suites, the 1F-C-R validator, the tolerance
  audit and every Phase 1G script, on both interpreters): [WIN] Sec. 7.
- **Tag readiness.** 1G-B's only blocking decision, GB-OD1, is resolved on
  `main` (`738f3c3`, merge `63ca316`), and [WIN] records its Windows run:
  **1G-B is ready for `phase-1g-b-lagrangian-sigma-v1`.** Approvals 4–5
  are not given, so per task Sec. 5 the tag goes on `63ca316` with the
  Windows results in its message; GB-OD2–OD6 (non-blocking) reach `main`
  with this branch. Approval 3 is not given either: the tag command is
  printed for the owner, not run.
