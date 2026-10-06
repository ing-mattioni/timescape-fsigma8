# Phase 1G-F/G — remediation integration record

Date: 2026-10-06. Classification: `REPORT_ONLY_INTEGRATION_RECORD`.
Branch: `phase-1g-f-successor-g-evolution`. Parent commit:
`fb5d95245bc0cb19ce6cd1438177f1a597bb232f` (main, merge of PR #3).
Companion: [`phase1g_fg_remediation_integration_inventory.json`](phase1g_fg_remediation_integration_inventory.json).
Logs: [`phase1g_fg_remediation_integration_logs/`](phase1g_fg_remediation_integration_logs/).

This record closes the three residual findings of the independent delta
audit and integrates the F/G work on the phase branch. It does not rewrite
either audit:

- [`phase1g_fg_independent_scientific_audit.md`](phase1g_fg_independent_scientific_audit.md),
  2026-10-02;
- [`phase1g_fg_remediation_independent_audit.md`](phase1g_fg_remediation_independent_audit.md),
  2026-10-06.

It does not rewrite their evidence or the remediation record
[`phase1g_fg_audit_remediation.md`](phase1g_fg_audit_remediation.md) either.
That record's `actual_remediation_commit: null` describes the state when it
was written and is left unchanged. The actual commit is recorded here
(Sec. 7).

## 1. Authorization

The owner's instruction of 2026-10-06, verbatim:

> «Autorizzo esplicitamente i commit locali e il push ordinario del branch
> di fase al repository remoto del progetto. Non occorre chiedermi
> nuovamente conferma per queste operazioni. Questa autorizzazione non
> comprende push diretto su main, force push, merge, tag, release o
> dichiarazioni di freeze scientifico.»

**Scope, as a summary:**

- local commits and an ordinary push of this phase branch to `origin`;
- no push to `main`, no force push, merge, pull request, tag or release;
- no scientific freeze;
- no change to any scientific status or observational authorization.

The earlier authorizations are recorded verbatim in the remediation and the
D successor and are not reopened here:

- «Ottimo, procedi con entrambe le cose (e sistema anche CLAUDE.md se
  riesci)», dated 2026-10-01 in the session record;
- «si confermo», 2026-10-02.

## 2. Residual findings of the delta audit — closed

| Finding | Change | Files |
|---|---|---|
| R2-N1 (LOW) | The module docstring now names the registered 2026-10-02 D successor and its role: one added token changed to `NOT_DERIVED` through an explicit link to its adding record, which keeps the historical value. Docstring only: the module AST without its docstring is identical to the pre-edit state, and no assignment, registry logic or computation changes | `src/timescape_fsigma8/scientific_status.py` |
| R2-N2 (LOW) | The map's verdict-2 row now cites frozen §1 item 2 and the §5 "Milne limit" paragraph (it formerly said "§13 verdict 2"). The near-empty row now cites §1 item 5 and the §8.2 r_min column (formerly "§12 item 1"). Three rows add the F2 values behind the frozen [W09]-comparison percentages, with their historical F3 values, scope and provenance: 62–73% → 49–71%; 40–68% → 20–54%; ≤ 10% → ≤ 4.3%. The ≤ 4.3% holds for the collapse threshold of frozen §8.2; the turnaround threshold, outside that claim, would give 5.05%. The values come from the delta-audit evidence `r2_archived_headlines_out.json` (R2-M6) and were re-read here from the regenerated archive. They are historical, conditional C3/M3 sensitivities, not observational predictions | `reports/phase1g_f_volume_budget_successor.md` §5.1 and its note; inventory keys `w09_comparison_rectification`, `supersession_map_location_corrections` |
| R2-N3 (LOW) | The header now separates the verbatim 2026-10-01 instruction, the scope interpretation (explicitly labelled a paraphrase), the 2026-10-02 decisions and this 2026-10-06 integration authorization | `reports/phase1g_f_volume_budget_successor.md` header; inventory key `authorization_kinds` |

- **FGA-D2.** The delta audit recorded it as partially resolved because of
  the F header paraphrase. That residue is now removed, so FGA-D2 is closed
  in substance. This closure has **not** been re-audited independently: it
  is a text-only change, verified here by diff review.
- **R2-N4** (INFO, registry) stays optional and unchanged.
- **R2-N5** (INFO). The stale README "pending … independent audit" wording
  is updated below. The G report's run-specific residual figures are left
  as they are.

## 3. Documentation-state updates

These are status statements that would otherwise become false on
integration. They contain no scientific change.

- **F successor §6 and G report §8.** Instead of "needs a delta review /
  remains outstanding", they now point to the delta audit and to this
  record. Both still say that no freeze, tag, merge or release is implied.
- **F and G inventories.**
  - A `delta_audit` block points to the 2026-10-06 audit, with its verdicts
    and the absence of integration blockers.
  - `independent_audit.scope` no longer says that no delta audit exists.
  - An `integration_revision_date` field is added.
- **README.** The σ-track lead and the audit bullet now name the phase
  branch, the delta audit and this record. "Not merged, frozen or tagged"
  is kept.
- **CLAUDE.md.**
  - The firewall paragraph, σ-track lead, 1G-F/1G-G ledger entries and the
    suite-count comment record the delta audit and this record.
  - "local" becomes "on the phase branch".
  - No rule, firewall or status value changes.

## 4. Links

- **First audit**, with its 18 findings: its report and inventory
  (byte-identical, `6bb8edec…`, `3503a602…`).
- **Remediation:** its report and inventory (unchanged).
- **Delta audit:** its report and inventory (unchanged, `46f3aef7…`,
  `ebe7918…`).
- **Evidence:** `reports/phase1g_fg_remediation_audit_evidence/`, which
  holds:
  - the 14 recovered first-audit files (`prior_audit_2026-10-02/`), whose
    SHA-256 equal the first audit's inventory, re-verified here;
  - the delta audit's own scripts, outputs and logs.

  Its `MANIFEST.sha256` verifies unchanged.
- **D successor:** `phase1g_d_linear_statistic_status_successor.md`.
- **Successors:** F `phase1g_f_volume_budget_successor.md`, G
  `phase1g_g_void_evolution.md`, and the validation record
  `phase1g_fg_successor_validation.md` (unchanged; historical 2026-10-01
  scope).

## 5. Verification

### 5.1 Read from logs (not rerun as such)

The delta audit's logs report 1136 passed, 0 skipped, 0 failed on
CPython 3.14.3 and 3.11.9 (2026-10-06, 12:31 and 12:39). Those runs are on
the remediated tree *before* R2-N1–N3.

The following are reported by the remediation and **not verified** here,
because their inputs are absent:

- the Linux 1101/34/1 run;
- the delivery bundle;
- `APPLY.md`;
- the delivery `validation/` log.

### 5.2 Run in this session, on the final content

These are the final content runs: after R2-N1–N3 and the documentation
updates, before this record's results were filled in.

Command: the owner-specified PowerShell block, with `PYTHONPATH` set to `src`,
`OPENBLAS_NUM_THREADS=1` and `python -B -W error -m pytest -q -p no:cacheprovider`.

| Interpreter | Full suite | Time | Exit |
|---|---|---:|---:|
| CPython 3.14.3 (`.venv`; NumPy 2.5.2, SciPy 1.18.1, pytest 9.1.1) | **1136 passed, 0 skipped, 0 failed** | 524 s | 0 |
| CPython 3.11.9 (`.venv311`; NumPy 2.4.6, SciPy 1.17.1, pytest 9.1.1) | **1136 passed, 0 skipped, 0 failed** | 538 s | 0 |

Both runs include the unmodified historical Git-blob test. The count is the expected 1136; no test or expectation was changed.

- `git diff --check`: clean (exit 0).
- **Targeted tests, before the suites:** 156 passed (F/G/D modules and the registry and governance tests, 3.14.3).
- **1F-C-R validator:** `PASS`, with changes `{LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC, UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY}`.
- **New `.gitattributes` rule.** It marks the audit-evidence directory and the integration-logs directory as `-text -whitespace`, following the repository's precedent for pinned provenance files.
  - Several Windows-captured evidence logs contain CRLF, and their bytes are pinned by `MANIFEST.sha256`.
  - Line-ending conversion would break those pins; whitespace checks would flag the CRs.
  - Tested beforehand in an isolated temporary repository: bytes are preserved, and `git diff --cached --check` is clean.
- **After the results were filled in**, a registration-only step: the validator, the targeted tests and `git diff --check` were rerun on the final bytes (Sec. 6). The full suites were not rerun, because no code, test or scientific content changed after them.

## 6. Preservation and perimeter

- **Perimeter.** Files changed relative to the session start: `.gitattributes`, `CLAUDE.md`, `README.md`, `reports/phase1g_f_volume_budget_successor.md`, `reports/phase1g_f_volume_budget_successor_inventory.json`, `reports/phase1g_g_void_evolution.md`, `reports/phase1g_g_void_evolution_inventory.json`, `src/timescape_fsigma8/scientific_status.py`. Added: this record, its inventory and its logs. Nothing was removed.
- **Artifacts.** All 187 files under `artifacts/` are unchanged. The historical Monte Carlo was not rerun.
- **Frozen and tracked reports.** All 111 tracked report and inventory files are unchanged against HEAD.
- **Pins.** The `frozen_sha256` pins of the F inventory are unchanged: AGENTS.md and the frozen 1G-F report, inventory and script.
- **Audits and records.** Byte-identical: both independent audits and their inventories, the remediation record, the D successor and the validation record.
- **Evidence.** `MANIFEST.sha256` verifies with 45 entries and 0 mismatches. The 14 recovered first-audit files match the first audit's inventory.
- **Status module.** The `scientific_status.py` edit is docstring-only.
  - The pre-edit bytes, reconstructed, equal the session-start SHA-256.
  - The AST without the module docstring is identical.
  - The only assignment differing from HEAD is the approved D token (`NOT_DERIVED`).
  - The five observational authorizations are `NOT_GRANTED`.
- **Code.** No other Python file changed in this session, so no computation changed.

## 7. Commits and push

- **First commit:** the complete, validated F/G work and this record. Its
  full hash is recorded by a second, dedicated provenance commit that
  changes only this report and its inventory:
  `actual_remediation_commit` = `8f3131fe19cccd44a29287617145f3300818dfa3`.
- **The second commit:** it cannot contain its own hash.
- **Push:** the phase branch only, ordinary push with upstream. The push
  necessarily follows the last commit, so its outcome and the local/remote
  hash match are reported outside this record.

## 8. Open before a phase freeze

1. **Owner approvals, each separate:**
   - merging into `main` (through a pull request);
   - any annotated phase tag;
   - any release.

   None is authorized.
2. **Independent confirmation.** The R2-N1–N3 closures were not reviewed
   independently. They are text-only and do not affect the verdicts.
3. **Not verifiable here.** The Linux snapshot run and the delivery bundle.
4. **Optional.** R2-N4 (registry order and validator message).
5. **Status.**
   - `SIGMA8_AUTHORIZATION`, `FSIGMA8_AUTHORIZATION`, `RSD_AUTHORIZATION`,
     `OBSERVATIONAL_AUTHORIZATION` and `UNIQUE_TIMESCAPE_PREDICTION` remain
     `NOT_GRANTED`.
   - F/G results remain conditional, model-internal research evidence.
