# Evidence for the F/G remediation independent audit (2026-10-06)

Companion of `reports/phase1g_fg_remediation_independent_audit.md` and its
inventory. Everything here is the auditor's own code, outputs and logs. Nothing
is imported from `.reference/`, and no upstream or third-party source text is
copied: the arXiv LaTeX sources were consulted, and only their SHA-256 values
are recorded in the inventory.

## Contents

| Path | What it is |
|---|---|
| `prior_audit_2026-10-02/` | The first audit's scripts, outputs and full-suite logs, recovered from that session's scratchpad. All 14 SHA-256 values equal `auditor_evidence.sha256` in `phase1g_fg_independent_scientific_audit_inventory.json`. `build_inventory.py` refuses to run while that inventory exists, by design |
| `r2_cutoffs_pde.py` (+`_out.json`) | R2-M1. Method-diverse recomputation of the F2/F3 cutoffs, near-empty cutoffs and tails, and the z = 3 r ≥ 1 fraction. Uses the backward Kolmogorov equation (Crank–Nicolson, N = 3000 and 6000), σ(R) by Gauss–Legendre panels, and shell crossing from Lagrangian shells |
| `r2_compare_regen.py` (+`_out.json`) | R2-M2. Regenerated F/G evidence vs the inventories, under the declared gate rtol = 1e-11, atol = 1e-14. Also re-checks the 84-population archive and measures accuracy against R2-M1 |
| `r2_registry_adversarial.py` (+`_out.json`) | R2-M3. Fifteen registry cases against the live validator, read-only. Mutated records go to a temporary directory |
| `r2_gel_flory_stockmayer.py` (+`_out.json`) | R2-M4. Flory vs Stockmayer for the product kernel ([L03] (4.74)–(4.77)), and truncation convergence near t_gel |
| `r2_shell_test_probe.py` (+`_out.json`) | R2-M5. Convergence, label independence and non-circularity (profiles p = 4, 6) of the new Lagrangian shell-crossing test |
| `r2_archived_headlines.py` (+`_out.json`) | R2-M6. F2 values behind the frozen [W09]-comparison percentages |
| `r2_platform_margin.py` (+`_out.json`) | R2-M7. Actual Linux-vs-Windows leaf differences behind the numeric gate |
| `regen/` | F (with `--frozen-artifact`) and G outputs regenerated in an isolated copy on Python 3.14.3 and 3.11.9, with their logs |
| `logs/` | Both full-suite logs, the tolerance audit, the 1F-C-R validator output, the Git state, and the tree checksums before and after |
| `MANIFEST.sha256` | SHA-256 of every file in this directory, except the manifest itself |

## Reproduction

Run from the repository root:

```powershell
$env:OPENBLAS_NUM_THREADS = "1"
$E = "reports/phase1g_fg_remediation_audit_evidence"
.\.venv\Scripts\python.exe -B -W error $E/r2_cutoffs_pde.py $E
.\.venv\Scripts\python.exe -B -W error $E/r2_registry_adversarial.py $E/r2_registry_adversarial_out.json
.\.venv\Scripts\python.exe -B -W error $E/r2_gel_flory_stockmayer.py $E/r2_gel_flory_stockmayer_out.json
.\.venv\Scripts\python.exe -B -W error $E/r2_shell_test_probe.py $E/r2_shell_test_probe_out.json
.\.venv\Scripts\python.exe -B -W error $E/r2_compare_regen.py . $E
.\.venv\Scripts\python.exe -B -W error $E/r2_archived_headlines.py $E
.\.venv\Scripts\python.exe -B -W error $E/r2_platform_margin.py . $E
```

Three rules apply:

- `regen/` must first be filled by running the F and G producers in an
  isolated copy, never in the repository's own `artifacts/`.
- Rerunning a script overwrites its own `_out.json` in this directory.
  Copy the directory first if the recorded outputs must stay untouched.
- All results are conditional, model-internal research evidence. None is an
  observational statistic, and `SIGMA8_AUTHORIZATION` stays `NOT_GRANTED`.
