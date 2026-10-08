# Phase 1G-H — validation record

Date: 2026-10-06. Companion of
[`phase1g_h_global_variance_closure.md`](phase1g_h_global_variance_closure.md)
and its [inventory](phase1g_h_global_variance_closure_inventory.json).
Logs: [`phase1g_h_global_variance_closure_logs/`](phase1g_h_global_variance_closure_logs/).
Everything below was run in this session, on Linux, unless it is marked as
quoted from an earlier record.

**Scope (note of 2026-10-07, extended 2026-10-08).** This record validates
the original tree (`fd7331f` with its documentation, published at
`d4d693d`). The tree remediated after the independent audit is validated in
[`phase1g_h_audit_remediation.md`](phase1g_h_audit_remediation.md), and the
tree remediated after the delta audit in
[`phase1g_h_delta_audit_remediation.md`](phase1g_h_delta_audit_remediation.md);
later publication events are recorded in
[`phase1g_h_publication_successor.md`](phase1g_h_publication_successor.md).
Two sentences below are corrected in place (GH-F14, GH-F11); nothing else is
changed.

## 1. Environment

| Item | Value |
|---|---|
| Machine | cloud container, Linux 6.18.44 x86_64, glibc 2.39, 4 CPUs |
| Interpreter 1 | CPython 3.13.16 (`.venv`): NumPy 2.5.3, SciPy 1.18.1, matplotlib 3.11.2, pytest 9.1.1 |
| Interpreter 2 | CPython 3.11.17 (`.venv311`): NumPy 2.4.6, SciPy 1.17.1, matplotlib 3.11.2, pytest 9.1.1 |
| Install | `python3.X -m venv`, `pip install -e ".[test]"` (unpinned, as the project policy) |
| Upstream clone | `.reference/Linear-Perturbations-in-averaged-cosmological-models` cloned read-only at the pinned commit `590c6fd5332acb15f5683ebf392a0d7ce54983c5` (notebook LF SHA-256 `628c4412…5cea2a`, as `UPSTREAM.lock`); git-ignored, not committed, not edited |
| Not available | CPython 3.14.3 and 3.11.9 (the Windows interpreters of the earlier records); the upstream oracles and generated validation artifacts of earlier phases (their tests skip) |

The interpreters differ from the Windows gate of earlier phases. No
dual-interpreter certification on 3.14.3 / 3.11.9 is claimed (Sec. 6).

## 2. Base and history

- The clone was shallow; it was completed with
  `git fetch --unshallow --tags origin`. No history was rewritten.
- `main` = `origin/main` = `8d3cdd0533035858c42269cb1dff1a20dcafc7da` (PR #4
  merge, the frozen F/G checkpoint); `main` has not advanced beyond it.
- Branch `phase-1g-h-global-variance-closure`, created from `main`:
  - `79003742fb1f284693d6659e329b2c6b7f7927f0`: F/G freeze-status alignment
    (documentation only; `phase1g_fg_freeze_status_successor.md`);
  - `fd7331f321702ed8c20d32ea805e7b9537d44726`: the 1G-H runtime, evidence,
    case runner, configurations and tests;
  - the commit carrying this record, the report, the inventory, the logs and
    the README/CLAUDE updates (its hash cannot be inside itself; see
    `git log`).
- When these commits were made, nothing had been pushed. With the owner's
  approval of 2026-10-06, given afterwards, they were pushed to the session
  branch `ccr-555e67be-u11yht`: the remote branch was created at
  `0572e416504bcdfaa5831b6d482b687ef6fae582` (a descendant of `8d3cdd0`;
  corrected 2026-10-07: the creation of a remote ref is not a fast-forward),
  then fast-forwarded, with a second approval, to the documentation-only
  commit that adds this paragraph. `main` is unchanged. No tag, branch D v2,
  pull request or release was created. The two approvals are recorded in the
  inventory's `publication` block; the independent audit marks them
  `OWNER_CONFIRMATION_REQUIRED` (GH-F15).

## 3. Test suites

Command (both interpreters, warnings as errors):

```bash
OPENBLAS_NUM_THREADS=1 python -B -W error -m pytest -q -p no:cacheprovider -rs
```

| Run | Tree | Collected | Passed | Skipped | Failed | Time |
|---|---|---:|---:|---:|---:|---:|
| Baseline, 3.13.16 | `8d3cdd0` (before any change) | 1136 | 1103 | 33 | 0 | 365 s |
| Baseline, 3.11.17 | `8d3cdd0` | 1136 | 1103 | 33 | 0 | 358 s |
| **Final, 3.13.16** | `fd7331f` + the report, inventory and README/CLAUDE of this commit | **1164** | **1132** | **32** | **0** | 378 s |
| **Final, 3.11.17** | same | **1164** | **1132** | **32** | **0** | 378 s |

- **Counts.** The 28 new tests of `tests/test_phase1g_h_global_variance.py`
  account for 1164 − 1136. The pre-existing 1136 tests all ran: 1103 passed at
  baseline, 1104 in the final run. One fewer skip, because the upstream clone
  now exists (`tests/test_reproducibility_gates.py`); no test or expectation
  was changed.
- **Skips (32), all from absent inputs, which were not fabricated:** upstream
  oracle not extracted (18), clean perturbation oracle absent (4), barotropic
  oracle absent (4), the owner-decisions artifact (3; the 20-minute 16-seed
  Monte Carlo of `phase1g_owner_decisions_numerics.py`, not rerun to rebuild
  a documented baseline), and one each for the 1D-B growth validation
  artifact, the 1D-D validation artifact and the B2 artifact. The full lists
  are in the logs.
- **Provenance kept distinct.** The F/G freeze preflight (1136 passed,
  0 skipped, 0 failed on Windows CPython 3.14.3 and 3.11.9, 505 s / 501 s) is
  the owner's run at `8d3cdd0`. The baseline above is this session's Linux
  run of the same tree, with missing artifacts. Neither is a re-certification
  of the other.
- **Targeted, during development:** `tests/test_phase1g_h_global_variance.py`
  28 passed (about 7 s on 3.13.16); together with the 1G-B owner-decision and
  1F-C-R tests, 97 passed.

Logs: `full_suite_py313.log`, `full_suite_py311.log` (final runs, with the
skip reasons). The baseline logs stayed in the session scratchpad; their
counts are recorded here.

## 4. Evidence script

```bash
OPENBLAS_NUM_THREADS=1 python -B -W error scripts/phase1g_h_global_variance_closure_numerics.py
```

| Interpreter | Tree | Gates | Exit | Time |
|---|---|---|---|---:|
| 3.13.16 | `fd7331f`, clean `src`/`scripts`/`tests` | 21 / 21 pass | 0 | 101 s |
| 3.11.17 (`--no-figures`) | same | 21 / 21 pass | 0 | 91 s |

- **Cross-interpreter comparison:** 2779 numeric leaves agree to the rule
  rtol 10⁻¹¹ / atol 10⁻¹⁴ (environment and figure entries ignored, labels
  and keys compared exactly); the largest relative difference is 0.
- **Artifact:** `artifacts/independent/phase1g_h_global_variance_closure.json`
  (git-ignored, regenerable). Its raw SHA-256 for the 3.13.16 run,
  `99c4aad4…880aa12`, identifies one exact run and environment (it includes
  the git head); it is not a cross-platform gate.
- **Figures:** `artifacts/independent/phase1g_h/sigma_vs_void_share.png`,
  `radius_scan.png`, `propagator_scale_dependence.png` (git-ignored).
- **Gates (declared before any evaluation):**
  - 1G-D owner-decision A_v (1169 / 1185, half a unit) and X_SU (1.263 / 1.285,
    5×10⁻⁴);
  - σ² ∝ A_s at a fixed constant share (10⁻¹⁰);
  - A_s-independence of the PBS void term (2×10⁻³, the compression term);
  - refined quadrature (2×10⁻⁶);
  - the 1G-E/F reference σ reproduced from its components (6×10⁻⁴; corrected
    2026-10-07: that limit did not protect the printed fourth decimal, GH-F11;
    the remediated gate uses the propagated rounding budget of the
    four-decimal inputs, about 1.1×10⁻⁴);
  - orthant P11 against the bivariate CDF (10⁻¹⁰);
  - two-barrier bias against central differences of the M3 budget (10⁻⁶).

  Logs: `evidence_py313.log`, `evidence_py311.log`, `evidence_head.txt`.
- **Single-case runner:** the three configurations in
  `scripts/phase1g_h_configs/` run and reproduce the evidence values (0.8108,
  1.1214, 0.9182); a test checks the runner against a direct module call
  (10⁻¹⁴) and that missing configuration entries are refused.

## 5. Governance checks

- `python scripts/audit_numerical_tolerances.py`: 0 comparisons without
  explicit tolerances (every `pytest.approx` in the new tests states `rel`
  and `abs`; every `math.isclose` in the module states `rel_tol` and
  `abs_tol`).
- `python scripts/validate_phase1f_c_r_astra_remediation.py`: `PASS`. It
  imports 57 package modules, including `global_variance`, checks 716 test
  comparisons, verifies 27 frozen tags and 52 historical reports, and
  round-trips all 47 `reports/*.json` with unique keys, including the two new
  inventories. It was rerun on the final bytes of this commit. Before the upstream clone existed, this validator stopped at
  its upstream-commit assertion; it needs `.reference/`.
- `git diff --check` and `git diff --cached --check`: clean for every commit.
- **Status registry:** no token value or comment changed;
  `scientific_status.py` is untouched. A test asserts
  `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC = NOT_DERIVED`,
  `VOID_ONSET_RESPONSE = EXTERNAL_CLOSURE_INPUT` and the five `NOT_GRANTED`
  authorisations.
- **Naming rule:** no public name of `global_variance` and no output key
  contains `sigma8`, `sigma_8` or `8hMpc` (tested); the module is imported by
  no other package module (tested).

## 6. Not run here, and the Windows gate

- **Not run:** Windows CPython 3.14.3 and 3.11.9; the upstream notebook
  execution and oracle extraction (the `exec` extra was not installed); the
  earlier phases' long evidence scripts (not needed: no existing code
  changed).
- **Windows commands** for the owner's dual-interpreter gate, from the
  repository root in PowerShell:

  ```powershell
  $env:OPENBLAS_NUM_THREADS = "1"
  .\.venv\Scripts\python.exe -B -W error -m pytest -q -p no:cacheprovider -rs
  .\.venv311\Scripts\python.exe -B -W error -m pytest -q -p no:cacheprovider -rs
  .\.venv\Scripts\python.exe -B -W error scripts\phase1g_h_global_variance_closure_numerics.py
  .\.venv311\Scripts\python.exe -B -W error scripts\phase1g_h_global_variance_closure_numerics.py --no-figures
  .\.venv\Scripts\python.exe -B -W error scripts\validate_phase1f_c_r_astra_remediation.py
  .\.venv\Scripts\python.exe -B scripts\audit_numerical_tolerances.py
  ```

  With the Windows artifacts present, the expected count is 1164 passed,
  0 skipped. Compare the evidence JSON numerically with the rule of Sec. 4,
  not by raw hash.

## 7. Limits of this validation

- **Self-validation.** The checks are by the author of the phase; no
  independent audit has been performed (an owner decision, H-OD5).
- **Hypothesis scans.** Interval widths, seed-scale sensitivities and premise
  readings are scans over hypotheses, not confidence intervals.
- **Not observational.** Nothing here is an observational validation; the
  firewall is unchanged.
