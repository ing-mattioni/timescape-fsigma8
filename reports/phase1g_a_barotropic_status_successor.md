# Phase 1G-A successor record — barotropic continuum stability refuted

Record classification: `APPROVED_SCIENTIFIC_STATUS_CHANGE_SUCCESSOR_RECORD`.
Parent checkpoint: `462121c` (Phase 1G-A audit), local branch
`phase-1g-a-barotropic-status-refutation`. Date: 2026-09-29.
Machine-readable companion:
[`phase1g_a_barotropic_status_successor_inventory.json`](phase1g_a_barotropic_status_successor_inventory.json).

[GM] = Galoppo & Mourier, arXiv:2511.17160v2 (JCAP 02 (2026) 066).
[1G-A] = [`phase1g_a_sigma8_derivation_path_audit.md`](phase1g_a_sigma8_derivation_path_audit.md).

## 1. The change

| Token (`scientific_status.py`) | Frozen value | Current value |
|---|---|---|
| `UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY` | `NOT_DERIVED` | `REFUTED_HADAMARD_ILL_POSED` |

This applies [1G-A] Sec. 10 recommendation 1. No other token changes.

**Meaning.** The token names one property: stability of the linear
barotropic closure ([GM] Eq. (4.13)) for unrestricted spatial data, that is,
continuous dependence on initial data uniformly over all wavenumbers. For the
Timescape tracker with the corrected sound speed that property is false: the
Cauchy problem is ill-posed in Hadamard's sense, and no linear barotropic
σ_R exists.

**Scope.** The change is a classification only:
- The finite-mode equations stay well defined. For each fixed k,
  [GM] Eqs. (4.14)–(4.17) are a regular linear ODE with a unique solution.
  That is what the package integrates and what [GM] Fig. 3 shows.
- The barotropic runtime is unchanged and fully available: both D3 branches
  (`printed_4_15`, `derived_4_10`) stay mandatory and explicit. Nothing is
  deprecated, removed, guarded or defaulted. `printed_4_15` remains required
  for paper/notebook reproduction.
- No equation, initial condition, unit, sign convention, independent
  variable, normalisation or tolerance changes.
- The comoving and Mészáros closures do not contain c²_s and are unaffected
  ([1G-A] Sec. 4.3–4.4).
- It grants nothing. `UNIQUE_TIMESCAPE_PREDICTION`, `OBSERVATIONAL_AUTHORIZATION`,
  `RSD_AUTHORIZATION`, `SIGMA8_AUTHORIZATION` and `FSIGMA8_AUTHORIZATION` stay
  `NOT_GRANTED`.

## 2. Authorisation

The project owner approved the change on 2026-09-29, verbatim: "let ...
another [sub-agent] mark the barothropic closure as refuted, I give you the
approval". This is the human approval that [1G-A] Sec. 10 requires for
recommendation 1 (AGENTS.md rule 1 is not engaged: no equation changes).

## 3. Evidence

Class: `DERIVED_FROM_VERIFIED_DEFINITIONS` + `NUMERICALLY_CORROBORATED`
([1G-A] Sec. 4.1; inventory `closure_admissibility.barotropic`).

- **Operator.** In [GM] Eq. (4.19) the only wavenumber dependence is
  `c²_s (k²/a²) Δ^(eff)`. With `k²/a² ↔ −³Δ` the principal part is
  `Δ̈^(eff) − c²_s ³Δ Δ^(eff)`. The corrected Timescape `c²_s,eff` is
  negative throughout, from −0.4996 at z = 20 to −0.3912 today (frozen 1B),
  so the operator is elliptic in space–time, not hyperbolic.
- **Frozen matrix.** In [GM] Eqs. (4.15), (4.17),
  `A23·A32 = −c²_s k²/a_D² > 0`. The D3 branch changes only the
  k-independent entry A33, so the symbol is the same on both branches.
- **WKB exponent.** A mode of wavenumber k grows like `exp(k α)` with
  `α = ∫_{t(z=20)}^{t0} √(−c²_s,eff) dt/a_D = 1.70695` (dressed H0 = 1,
  matrix-convention k).
- **Direct integration** of the frozen `barotropic_rhs` gives slopes
  `d ln|Δ^(eff)(t0)|/dk` between k = 32π and 64π of 1.6994 (`derived_4_10`)
  and 1.6996 (`printed_4_15`). Both approach α from below. The gap α − slope
  is 0.0159/0.0162 at 16π→32π and 0.0074/0.0075 at 32π→64π
  (`printed_4_15`/`derived_4_10`), so it roughly halves when k doubles
  (ratio 2.15–2.16), as an algebraic WKB amplitude prefactor predicts.
- **σ8 scales.** kR = 1 at R = 8/h Mpc gives `αk ≈ 875`, above
  `ln(float64 max) = 709.8`. Any spectrum bounded below by a power law and any
  window with power-law tails then give a divergent `σ_R` integrand
  ([1G-A] Sec. 4.1).

**Regression.** `tests/test_barotropic_hadamard_refutation.py` re-derives the
evidence from frozen package functions in about 3 s:
- the token, and the consistency of this record with the frozen inventories;
- the symbol identity and its positivity on both branches and both tilt
  forms (`rtol = 1e-13`, roundoff only);
- α (`rtol = 1e-6` against 1.706948), the c²_s endpoints (`atol = 5e-5`)
  and a sampled sign check on 2001 times;
- the σ8-scale exponent (`atol = 0.05` against 875.4);
- per D3 branch, the 32π→64π slope against the recorded values
  (`atol = 1e-4`), the band `0 < α − slope ≤ 0.01`, and the ratio of the
  16π→32π gap to the 32π→64π gap in `[1.5, 3.0]` (O(1/k) predicts 2);
- the branch difference of the slope (`atol = 1e-3`).

The solver controls match the [1G-A] evidence script (DOP853,
`rtol = 1e-10`, `atol = 1e-30`).

## 4. Superseded readings (frozen texts unchanged)

These files stay byte-identical. The right-hand column is their current
reading.

| Location | Frozen text | Current reading |
|---|---|---|
| `astra/INDEPENDENT_SCIENTIFIC_AUDIT.md` A13 | "a stable unrestricted continuum physical prediction is `NOT_DERIVED`" | refuted: `REFUTED_HADAMARD_ILL_POSED` |
| `phase1f_c_r_astra_audit_remediation.md` l. 272–273 | "A13's finite-mode versus unrestricted barotropic-continuum stability caveat is retained" | the caveat is resolved negatively; the finite-mode language stays correct |
| `phase1f_c_r_astra_audit_remediation_inventory.json` `current_scientific_status` | `"UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY": "NOT_DERIVED"` | `REFUTED_HADAMARD_ILL_POSED` (this record) |
| same inventory, A13 disposition | `"FINITE_MODE_BAROTROPIC_CONTINUUM_STABILITY_CAVEAT_RETAINED"` | historically accurate; the caveat is now resolved negatively |
| `phase1g_a_sigma8_derivation_path_audit.md` l. 153–155, 482–483 | token "is `NOT_DERIVED`; this audit recommends `REFUTED_HADAMARD_ILL_POSED` … requires human approval" | recommendation approved and applied |
| `phase1g_a_sigma8_derivation_path_inventory.json` | `"status_tokens_changed": false` | true of the 1G-A checkpoint; this record changes one token |

The 1D-C §34 item 5 blocker (`phase1d_c_closure_inventory.json`) was already
closed negatively by [1G-A] Sec. 1; this record does not re-supersede it.

## 5. Validator: frozen check intact, live value from this record

`scripts/validate_phase1f_c_r_astra_remediation.py` compared every live token
with the frozen 1F-C-R inventory snapshot. That comparison would now fail by
design. The frozen inventory is not edited. Instead:
- `STATUS_SUCCESSOR_RECORDS` lists this record's inventory;
  `successor_status_changes()` reads its `status_changes`.
- `check_current_scientific_status()` requires, for each superseded token,
  that the **frozen snapshot still holds the recorded old token** (the
  historical check) and that the **live module holds the new token**. Every
  other token must still equal the frozen snapshot, as before.
- A token superseded by two records, or a record naming a token the module
  lacks, fails.
- `validate()` reports the applied changes as `successor_status_changes`.

The regression test covers the helper, including rejection of a tampered
frozen snapshot, of a live value that disagrees with this record, and of
drift in an uncovered token.

## 6. Files changed

| File | Change |
|---|---|
| `src/timescape_fsigma8/scientific_status.py` | token value; adjacent comment citing [1G-A] Sec. 4.1 and the dated approval; module docstring now mentions refutations and this successor |
| `src/timescape_fsigma8/perturbations/barotropic.py` | module docstring only (the superseded "requires a separate validity-scale and closure analysis" sentence); executable AST identical |
| `README.md` | the one paragraph on barotropic continuum stability |
| `scripts/validate_phase1f_c_r_astra_remediation.py` | successor-aware live-status check (Sec. 5) |
| `tests/test_barotropic_hadamard_refutation.py` | new regression (Sec. 3) |
| `reports/phase1g_a_barotropic_status_successor.md` | this record |
| `reports/phase1g_a_barotropic_status_successor_inventory.json` | its machine-readable companion |

Not changed: every historical report and inventory, `astra/`, `CLAUDE.md`,
every other package module and test, every equation and tolerance.

## 7. Dependent checks found

Search: the token name, `continuum stability`, `continuum_stability`,
`CURRENT_SCIENTIFIC_STATUS` and `scientific_status` over `src`, `tests`,
`scripts` and `README.md`. No test asserted the old value of this token.

| Dependent | Handling |
|---|---|
| `scripts/validate_phase1f_c_r_astra_remediation.py` l. 88–89: live module == frozen 1F-C-R snapshot, token by token | the only hard dependency; made successor-aware (Sec. 5), frozen check kept |
| `tests/test_phase1f_c_r_astra_remediation.py::test_a04_citation_regression_and_a07_live_classification` | asserts nine other tokens and the five `NOT_GRANTED`; unchanged |
| `tests/test_phase1f_d_necessary_bound.py::test_positive_margin_carries_no_existence_or_global_promotion` | in-process before/after invariance plus fixed `NOT_DERIVED`/`NOT_GRANTED` tokens, none this one; unchanged |
| `tests/test_experimental_ltb_cmc{,_evolution,_kappa_sensitivity,_mixed_sensitivity}.py` firewall tests | assert other `NOT_DERIVED`/`NOT_GRANTED` tokens; unchanged |
| `tests/test_reproducibility_gates.py` | exercises validator helpers only; unchanged |
| `tests/test_phase1e_f_h1_transfer.py::test_d3_variant_firewall_is_unchanged_and_has_no_default`, `tests/test_phase1e_g_continuum_h1.py::test_v33_d3_firewall_preserves_two_explicit_variants_without_default` | read `barotropic.py` text: both enum literals present, no upper-case default token; still pass after the docstring edit |
| `src/timescape_fsigma8/perturbations/barotropic.py` docstring; `README.md` paragraph | stated the superseded reading; updated |
| `astra/INDEPENDENT_SCIENTIFIC_AUDIT.md`, frozen reports and inventories | never edited; Sec. 4 gives their current reading |

## 8. Validation

Windows 11, run in an isolated worktree with `PYTHONPATH` on its `src`
(`timescape_fsigma8.__file__` verified inside the worktree):
- Python 3.14.3 with NumPy 2.5.2 and SciPy 1.18.1;
- Python 3.11.9 with NumPy 2.4.6 and SciPy 1.17.1.

The worktree has no `.reference/` clone and no `artifacts/`, so the oracle
and generated-artifact tests skip, exactly as on the parent.

| Check (`-B -W error`, no cache) | Python 3.14 | Python 3.11 |
|---|---|---|
| Full suite on parent `462121c` (baseline) | 886 passed, 30 skipped | 886 passed, 30 skipped |
| Full suite after this change | **894 passed, 30 skipped** | **894 passed, 30 skipped** |
| `tests/test_barotropic_hadamard_refutation.py` | 8 passed, ~3 s | 8 passed, ~4 s |

- **Skips.** The 30 skipped tests are identical to the baseline on both
  interpreters. No failures, errors or warnings.
  - Absent upstream oracles account for 26:
    `test_vs_upstream_oracle.py` 18, `test_vs_upstream_barotropic_oracle.py` 4
    and `test_vs_upstream_perturbation_oracle.py` 4.
  - The absent upstream clone accounts for 1 (`test_reproducibility_gates.py`).
  - Absent generated artifacts account for 3: `test_anchored_density_growth.py`,
    `test_b2_artifact_schema.py` and `test_growth_convergence_purity.py`, one
    each.
- **Mutation check.** With the old token restored in a scratch copy of the
  package, the two status tests of the new file fail, and the other six pass.
- **Runtime preservation.** The executable AST of `barotropic.py` (docstrings
  stripped, using the validator's `executable_tree`) is identical to the
  parent. The only changed assignment in `scientific_status.py` is this
  token.
- **Tolerances.** `scripts/audit_numerical_tolerances.py`: 590 comparisons
  (583 at 1G-A plus 7 new), none missing a tolerance.
- **1F-C-R validator.** `validate()` was run on both interpreters with one
  call stubbed: `git -C .reference/… rev-parse HEAD`, whose clone is absent
  in the worktree. That check was therefore **not exercised**; it is
  untouched by this change. Every other check ran, and the outputs are
  identical on both interpreters:
  - status `PASS_WITH_ABSENT_LOCAL_PROVENANCE`, only because the notebook
    clone is absent;
  - 27 frozen tags verified, 52 historical reports unchanged, 20 JSON
    round-trips, 55 package imports;
  - `successor_status_changes` = this token, `NOT_DERIVED` →
    `REFUTED_HADAMARD_ILL_POSED`;
  - `post_remediation_drift` lists only the pre-existing F1/F7 files
    (`initial_conditions.py`, `tracker.py`, `effective_fluid.py`), not
    `barotropic.py`.
- **Remote.** Nothing was pushed or tagged.
