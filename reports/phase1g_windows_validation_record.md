# Phase 1G — Windows validation record

Record classification: `WINDOWS_VALIDATION_RECORD`.
Date: 2026-09-30. Local branch `phase-1g-owner-decisions` (from `main` at
`63ca316`, the merge of the Phase 1G audit pull request).
Machine-readable companion:
[`phase1g_windows_validation_record_inventory.json`](phase1g_windows_validation_record_inventory.json).

This is the Windows run that the 1G-B adversarial audit asked for after the
GB-F1 fix ([`phase1g_b_adversarial_audit.md`](phase1g_b_adversarial_audit.md)
Sec. 7; [`phase1g_adversarial_audit_errata_successor.md`](phase1g_adversarial_audit_errata_successor.md)
Sec. 10). It also cross-checks the Linux results of Phases 1G-A to 1G-F on
the owner's platform, and records the final runs after the owner decisions
of 2026-09-30.

## 1. Authorisation

The project owner's task statement of 2026-09-30 ("Phase 1G — Windows
validation, owner decisions for 1G-A/C/D/E, tags"), Sec. 0, gives these
approvals, verbatim:

1. "Create the local branch `phase-1g-owner-decisions` from `main` and commit there."
2. "Apply the owner decisions ticked `[x]` in Sec. 3, exactly as ticked. An unticked decision is **not** approved: leave it open and list it at the end."

Approvals 3–6 are unticked and therefore not given: "[ ] Create signed
annotated tags **locally** for the phases that Sec. 5 finds ready.",
"[ ] Push `phase-1g-owner-decisions` and open ONE pull request against
`main`.", "[ ] Merge that pull request (merge commit, as PR #1 and PR #2).",
"[ ] Push the tags created under approval 3."

**In-session approval (2026-09-30).** Sec. 1.4 failed on Windows (Sec. 4).
The owner was asked, verbatim: "Sec. 1.4 fails on Windows:
scripts/phase1g_f_void_population_numerics.py does `import resource`
(Unix-only; ModuleNotFoundError on Windows). It is used only in `_progress()`
for the stderr peak-RSS line, never for an artifact value. The frozen script
must not be edited. How should I proceed?" The owner chose, verbatim:
"Committed wrapper (Recommended)" — "Add a new script, e.g.
scripts/phase1g_windows_run_f.py, that puts a Windows `resource` stand-in
(peak working set via ctypes) in sys.modules and runs the frozen 1G-F script
by path, unchanged. Record the portability defect in the Windows record; the
owner-decisions numerics script uses the same stand-in when it imports 1G-F."

## 2. Environment

| Item | Value |
|---|---|
| OS | Windows 11 Pro 10.0.26200 (x86-64; Intel family 6 model 141) |
| Interpreter 1 | CPython 3.14.3 (`.venv`), NumPy 2.5.2, SciPy 1.18.1, matplotlib 3.11.1, pytest 9.1.1 |
| Interpreter 2 | CPython 3.11.9 (`.venv311`), NumPy 2.4.6, SciPy 1.17.1, matplotlib 3.11.1, pytest 9.1.1 |
| Install | `python -m pip install -e ".[exec,test]"` on both; the default index answered, so no `--index-url` fallback was needed |
| Repository | `main` pulled to `63ca316` (fast-forward); HEAD contains `63ca316`; clean; not shallow |
| Upstream clone | `.reference/…` at `590c6fd5332acb15f5683ebf392a0d7ce54983c5`, clean, not shallow; notebook raw SHA-256 = `notebook_sha256_crlf`, LF-normalised = `notebook_sha256_lf` of `UPSTREAM.lock` |

## 3. Preflight (task Sec. 1)

Checkpoint `70f8c3c` = `63ca316` + the approved portable runner (Sec. 4),
which adds two scripts and touches nothing else.

**Regeneration** (CLAUDE.md "Key commands", `.venv`): every command exits 0 —
`execute_upstream_notebook`, the three oracle extractions,
`compare_to_oracle`, `validate_clean_perturbations`,
`validate_barotropic_perturbations`, `validate_growth_pipeline`,
`validate_anchored_density_growth`, `validate_phase1f_a_h1_closure`,
`validate_phase1f_b_dust_wall_boost_dynamics`,
`validate_growing_mode_initial_conditions`, `validate_h1_kinematic_gates`
and the four figure scripts. `validate_anchored_density_growth` first refused
to regenerate because the two runner files were still untracked ("regeneration
requires a clean working tree"); after they were committed it passed every
gate and, as part of its own checks, ran both full suites: 1049 passed, 0
failed, 0 skipped on each interpreter.

**Phase 1G scripts** (both interpreters): `phase1g_a`, `_c`, `_d`, `_e`
numerics and `validate_phase1g_b_lagrangian_sigma.py` exit 0 (21/21 1G-B
gates PASS). The frozen `phase1g_f_void_population_numerics.py` cannot start
on Windows (Sec. 4); through the approved runner it exits 0 on both
(1082 s on 3.11.9, 1044 s on 3.14.3, run concurrently; peak working set
1466.5 MB).

**Full suites** (`.venv\Scripts\python -B -W error -m pytest -q -p no:cacheprovider`,
both interpreters in parallel, at `70f8c3c`):

| Interpreter | Result | Time |
|---|---|---|
| CPython 3.14.3 | **1049 passed, 0 failed, 0 skipped** | 711 s |
| CPython 3.11.9 | **1049 passed, 0 failed, 0 skipped** | 716 s |

Expected: 1049 (the Linux result at `738f3c3`: the owner's earlier 1044 plus
the 5 tests of `tests/test_phase1g_e_status_addition.py`). **No difference.**
In particular `test_top_hat_window_limits_series_and_envelope`, the GB-F1
test changed with option A, passes on Windows.

**Validator and tolerance audit** (both interpreters):
- `scripts\validate_phase1f_c_r_astra_remediation.py --producers`: **`PASS`**
  (not `PASS_WITH_ABSENT_LOCAL_PROVENANCE`); explicit comparisons src 14,
  scripts 2, tests 634; `post_remediation_drift` lists the three
  pre-existing, reported-not-rejected entries (`background/effective_fluid.py`,
  `background/tracker.py`, `perturbations/initial_conditions.py`).
- `scripts\audit_numerical_tolerances.py`: **634 comparisons, 0 missing**;
  identical output on both.

## 4. Portability defect of the frozen 1G-F script

`scripts/phase1g_f_void_population_numerics.py` (Phase 1G-F, frozen) does
`import resource` at module level. `resource` exists only on Unix, so the
script stops at import on Windows (`ModuleNotFoundError: No module named
'resource'`) on both interpreters. It uses the module only in `_progress()`,
for the peak-RSS figure of its stderr progress line; no artifact value,
gate or printed result depends on it.

With the owner's in-session approval (Sec. 1), the frozen script is not
edited:
- `scripts/_portable_resource.py` provides `RUSAGE_SELF` and
  `getrusage(RUSAGE_SELF).ru_maxrss`, the process's peak working set
  (`K32GetProcessMemoryInfo`) in KiB, the unit Linux uses. Where the real
  module exists it installs nothing.
- `scripts/run_phase1g_f_portable.py` installs it and runs the frozen script
  as `__main__` by path. Stdout, gates and artifact are the frozen script's
  own.
- `scripts/phase1g_owner_decisions_numerics.py` installs the same stand-in
  before it imports the 1G-F script.

Committed as `70f8c3c`. Not a gate or tolerance change. A later 1G-F
successor could make the progress line portable; that is not done here.

## 5. Windows against Linux (task Sec. 2)

**5.1 Interpreter identity.** Printed output is byte-identical between 3.14.3
and 3.11.9 for every Phase 1G script (1G-A, C, D, E numerics; 1G-B driver;
1G-F through the runner). Artifacts, outside their environment/provenance
blocks:
- 1G-B, 1G-C, 1G-E and 1G-F: identical (1G-F: all 4728 leaves, including
  every seeded Monte Carlo value);
- 1G-A: 37 leaves differ, by ≤ 9.5e−16 relative (ΛCDM growth ratios and X
  at finite z_i), plus the quadrature *error estimate* `alpha_quad_abserr`
  (1.03e−13 on both, differing in its 8th digit);
- 1G-D: the (4.11) residual diagnostics differ at round-off (≤ 1.9e−15,
  budget 1e−12), as on Linux.

**5.2 1G-F against the Linux inventory**
(`reports/phase1g_f_void_population_inventory.json`, CPython 3.13.12/3.11.15):

| Block | Rule (task Sec. 2.2) | Entries | Agree |
|---|---|---|---|
| `spherical_model` | to the recorded digits | 11 | **11** |
| `void_mass_fraction_1_minus_D` (both cases) | to the recorded digits | 12 | **12** |
| `headline` (D_wall, f_v0, clocks, one-radius a = 15, populations, variance) | after rounding to 4 decimals (3 for the median radii, which the inventory records to 3) | 472 | **472** |
| `headline.*.monte_carlo` | may differ in the last digits; largest deviation reported | 16 | 16 equal at the recorded 4 decimals; ball counts identical (1 129 532; 80 421; 449 752; 51 664) |

The largest Monte Carlo deviation is not resolvable at the inventory's
precision: every entry rounds to the recorded value (the largest absolute
difference, 4.6e−5, is the inventory's own rounding). No gate was changed.

**5.3 1G-A, 1G-C, 1G-D, 1G-E against their reports.** Every numeric value
recorded in the four frozen inventories (at their printed digits) is found in
the Windows artifact to half a unit of its last digit: 1G-A 122/122, 1G-C
61/61, 1G-D 176/176, 1G-E 155/155. The remaining inventory numbers are two
source line numbers (1G-A) and two derived ratios (1G-E: 1.3567/0.8111 = 1.67,
1.5717/0.8111 = 1.94), checked by hand. The 1G-B driver's V7 gates compare
its values with the 1G-A inventory and pass. The 1G-E Monte Carlo reproduces
the report exactly: 8569 / 6322 balls, σ²_part 1.280 / 1.268 and
0.820 / 0.823, gated error 1.5% / 0.9%.

**5.4 Platform observations.**
- [CONS] Sec. 3 left errata E-1GA-2, -3, -4 unapplied as Linux round-off.
  Windows confirms: the maximum Simpson grid-refinement change of ln g is
  **3.997e−15** (Linux 4.108e−15) and direct-vs-Riccati at z_i = 20 is
  **1.927e−13** (Linux 2.25e−13), so the frozen "≤ 4e−15" and "≤ 2e−13" hold
  on the owner's platform.
- 1G-C's recorded `max_identity_error` 2.886579864025407e−15 (the Linux
  auditor saw ≤ 2.22e−15) is reproduced **bit for bit**.
- 1G-E's recorded `pair_identity_rel_err` 1.69435e−12 (Linux 1.69412e−12) is
  reproduced (1.6943452e−12).

## 6. 1G-B tag readiness

GB-OD1 was 1G-B's only blocking decision, resolved with option A on
2026-09-30 and on `main` (`738f3c3`, merge `63ca316`). The 1G-B audit asked
for the fix to be run on Linux and Windows. It passes on Linux ([CONS]
Sec. 10) and, per Sec. 3, on Windows on both interpreters. With this record,
**1G-B is ready for its tag.**

## 7. Final runs after the owner decisions

Commit `ac16620` (every owner decision applied; clean tree). The two
suites ran in the main tree in parallel; the Phase 1G scripts ran on each
interpreter in its own scratch worktree of the same commit, so that the
artifacts do not collide.

| Run | CPython 3.14.3 | CPython 3.11.9 |
|---|---|---|
| Full suite (`-B -W error -p no:cacheprovider`) | **1093 passed, 0 failed, 0 skipped (611 s)** | **1093 passed, 0 failed, 0 skipped (609 s)** |
| `validate_phase1f_c_r_astra_remediation.py --producers` | **PASS** | **PASS** |
| `audit_numerical_tolerances.py` | 638 comparisons, 0 missing | 638 comparisons, 0 missing |

- **Suite count.** 1093 = 1049 + 44 new tests: 32 in
  `tests/test_phase1g_b_owner_decisions.py` and 4 / 2 / 3 / 3 in
  `tests/test_phase1g_{a,c,d,e}_owner_decisions.py`. No existing test was
  removed or weakened; `tests/test_barotropic_hadamard_refutation.py` changed
  in two comments only.
- **Validator and tolerance audit** ran after the suites, at `e4851ae`
  (which differs from `ac16620` in report text only).
- **Validator.** Explicit comparisons: src 15, scripts 2, tests 638. No
  status removal is registered; the hardened checks (frozen tokens present,
  frozen inventory pinned to its `REMEDIATION` blob, canonical successor
  records) pass. `post_remediation_drift` still lists only the three
  pre-existing entries (`effective_fluid.py`, `tracker.py`, `initial_conditions.py`).
- **Tolerance audit.** 634 at the preflight plus the four new explicit
  comparisons of the new tests.

**Phase 1G scripts** (both interpreters, final commit):

| Script | 3.14.3 | 3.11.9 | printed output identical |
|---|---|---|---|
| `phase1g_a_sigma8_path_numerics` | exit 0 (13 s) | exit 0 (15 s) | yes |
| `phase1g_c_two_scale_growth_numerics` | exit 0 (8 s) | exit 0 (9 s) | yes |
| `phase1g_d_separate_universe_numerics` | exit 0 (9 s) | exit 0 (8 s) | yes |
| `phase1g_e_two_phase_sigma_numerics` | exit 0 (62 s) | exit 0 (64 s) | yes |
| `validate_phase1g_b_lagrangian_sigma` | exit 0 (19 s) | exit 0 (21 s) | yes |
| `run_phase1g_f_portable` | exit 0 (644 s) | exit 0 (666 s) | yes |
| `phase1g_owner_decisions_numerics` | exit 0 (616 s) | exit 0 (626 s) | yes |

The frozen `phase1g_f_void_population_numerics.py`, run directly, still stops
at `import resource` on both interpreters (Sec. 4); through the runner it
passes. The owner-decisions evidence script passes **124/124** gates on
both.

**Artifacts, 3.11.9 against 3.14.3** (outside the environment/provenance
blocks):
- identical: 1G-B, 1G-C, 1G-E and 1G-F (all 4732 leaves of the 1G-F
  artifact, every seeded Monte Carlo value included);
- 1G-A: 37 leaves differ, by ≤ 9.5e−16 relative (ΛCDM growth ratios and X at
  finite z_i), plus the quadrature error estimate `alpha_quad_abserr`
  (1.03e−13 on both, differing in its 8th digit);
- 1G-D: 19 (4.11) residual diagnostics differ; they are round-off values
  (≤ 1.9e−15, budget 1e−12), so their relative difference is not meaningful;
- owner decisions: one leaf, the same `alpha_quad_abserr`.

These are the preflight patterns of Sec. 5.1.

The runs above are for `ac16620`. The commits after it change report
text only: two wording fixes in the 1G-A and 1G-D successor records (a
percentage and an A_v range) and this record with its inventory.

## 8. Tag commands (printed, not run)

Approval 3 (create signed annotated tags locally) is unticked, so no tag is created; these are the commands for the owner. 1G-B: approvals 4-5 are unticked, so per task Sec. 5 its tag goes on 63ca316 with the Windows results in the message. 1G-A, 1G-C, 1G-D, 1G-E: their resolutions are on branch phase-1g-owner-decisions only; the tag goes on the main commit that carries them (the merge commit of that branch, <merge-commit>), after the owner pushes and merges it.

```text
git tag -s -a phase-1g-b-lagrangian-sigma-v1 63ca316 -m "Phase 1G-B v1: conditional, model-internal, mass-labelled linear sigma(M) runtime (lagrangian_sigma.py) with the documented growth-law limitation; reproduces every 1G-A number; adversarial audit reports/phase1g_b_adversarial_audit.md (ACCEPT_WITH_CORRECTIONS) with GB-F1 fixed (owner decision GB-OD1, option A, 738f3c3); Windows validation 2026-09-30: 1049 passed, 0 failed, 0 skipped on CPython 3.14.3 and 3.11.9 (reports/phase1g_windows_validation_record.md, branch phase-1g-owner-decisions, where the non-blocking GB-OD2..OD6 are applied); NON_OBSERVATIONAL, NOT_OBSERVATIONAL_SIGMA_8; SIGMA8_AUTHORIZATION remains NOT_GRANTED."
git tag -s -a phase-1g-a-sigma8-derivation-path-v1 <merge-commit> -m "Phase 1G-A v1: sigma(M) derivation-path audit (report-only). Barotropic closure Hadamard ill-posed (UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY = REFUTED_HADAMARD_ILL_POSED); conditional volume-average CGI sigma(M8) 0.52-0.69; adversarial audit reports/phase1g_a_adversarial_audit.md (ACCEPT_WITH_CORRECTIONS); owner decisions GA-OD1..OD4 applied (reports/phase1g_a_owner_decisions_successor.md: App. B verdict CONVENTION_DEPENDENT with an author question; the [NW15] row a declared Planck-early-universe hybrid, [NW15]'s own inputs a sensitivity 0.637-0.645; the alpha*k illustration a named hybrid chain, 557-694 under the report's conventions; GA-F4..F8, F11); Windows validation reports/phase1g_windows_validation_record.md; unique Timescape prediction, observational, sigma8 and fsigma8 authorization remain NOT_GRANTED."
git tag -s -a phase-1g-c-two-scale-growth-law-v1 <merge-commit> -m "Phase 1G-C v1: two-scale growth law (report-only). Tracker kinematically empty Milne voids plus EdS walls in common time, dynamics under the regional dust-FLRW assumption; wall-internal linear sigma at M8 relative to the wall mean (0.834 [GM], 0.935 [NW15]) under A1-A5 (TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW = DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION; transition law NOT_DERIVED); adversarial audit reports/phase1g_c_adversarial_audit.md (ACCEPT_WITH_CORRECTIONS); owner decisions GC-OD1..OD7 applied (reports/phase1g_c_owner_decisions_successor.md: supersedes and settled withdrawn, split evidence class, assumption A5, envelope dropped); no observational authorization."
git tag -s -a phase-1g-d-separate-universe-growth-v1 <merge-commit> -m "Phase 1G-D v1: separate-universe structure (report-only). SU modes exact k->0 solutions of [GM] (4.9)-(4.11); under S1 the [GM] CGI closures fail the SU test (FAILED_FOR_TIMESCAPE_TRACKER); void-onset response an external closure; with the tracker-consistent seed and f_vi = f_v(t_LS), A_v sigma_LSS(R8) = 1.05-1.11 and X_SU = 1.26-1.28; adversarial audit reports/phase1g_d_adversarial_audit.md (ACCEPT_WITH_CORRECTIONS); owner decisions GD-OD1..OD7 applied (reports/phase1g_d_owner_decisions_successor.md); no observational authorization."
git tag -s -a phase-1g-e-two-phase-sigma-v1 <merge-commit> -m "Phase 1G-E v1: two-phase mass variance at 8 h^-1 Mpc (report-only; TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC = DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION); mass-conserving formula, photon-frame compression, 1G-F derived reference population (sigma ~ 0.99); adversarial audit reports/phase1g_e_adversarial_audit.md (ACCEPT_WITH_CORRECTIONS); owner decisions GE-OD1..OD6 applied (reports/phase1g_e_owner_decisions_successor.md); conditional, hybrid, model-internal, not an observational sigma8; SIGMA8_AUTHORIZATION remains NOT_GRANTED."
```

Drop `-s` for an unsigned annotated tag. Push a tag only with the separate
approval 6.

## 9. Files

| File | Change |
|---|---|
| `scripts/_portable_resource.py`, `scripts/run_phase1g_f_portable.py` | the approved runner (commit `70f8c3c`) |
| `reports/phase1g_windows_validation_record.md` | this record (new) |
| `reports/phase1g_windows_validation_record_inventory.json` | its canonical companion (new) |

The artifacts are git-ignored and regenerable from the committed scripts.
