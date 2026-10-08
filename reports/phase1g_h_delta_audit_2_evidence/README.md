# Evidence of the second independent delta audit of Phase 1G-H

Report: [`../phase1g_h_delta_audit_2.md`](../phase1g_h_delta_audit_2.md);
inventory: [`../phase1g_h_delta_audit_2_inventory.json`](../phase1g_h_delta_audit_2_inventory.json).

Committed in two steps. The first commit (`64116509554cc0d711660da4d81ad95c3f450a6d`)
holds only the blind checkpoint, the code that produced it and its outputs,
before the auditor read the author's evidence artifact, logs, new
evidence-script functions or test expectations. Every other file is added by
the second commit. Large artifacts are not bundled; the scripts regenerate
them.

## Blind reconstruction (first commit)

- `BLIND_CHECKPOINT.md` (SHA-256 `c5f744e31a2a63a08c8aa0984faf6ebc9e18296e36c1cf7d7203d554162754ac`).
- `first_audit_provider.py`: verbatim copy of
  `../phase1g_h_independent_audit_evidence/independent_numerics.py` (same
  SHA-256), used only for the tracker and the EH98 no-wiggle provider.
- `blind_h25_mII_cw.py`: own reconstruction of (H25), m_II, <C_W - 1> and the
  signed/lognormal pair moments (no project import). Usage:
  `python -B -W error blind_h25_mII_cw.py <panels> <nodes_per_panel>`.
- `blind_first_panel.py`: first radial panel [0, 2R/480] contribution.
  Usage: `python -B -W error blind_first_panel.py run_16x48.json <subpanels>`.
- `run_*.json`, `first_panel*.json`: outputs (4x24, 16x48, 32x64 nodes;
  first panel with 8 and 32 sub-panels for the rest of the ball).

## Comparison and reproduction (second commit)

- `blind_vs_author_comparison.txt`: 128 quantities, blind value against the
  author's artifact (max relative difference 4.8e-8).
- `evidence_py313_226e52d.log`, `evidence_py311_226e52d.log`,
  `evidence_py313_248a06b.log`, `evidence_py313_5c325e1.log`: printed
  summaries of the evidence script; `evidence_artifact_hashes.txt` the
  SHA-256 of the regenerated artifacts (not bundled).
- `evidence_comparisons.json`: cross-interpreter, cross-commit and regression
  leaf comparisons, and the comparison with the delta audit's saved evidence.
- `inventory_reconciliation.py` and `_results.json`: 1G-H inventory numbers
  against the regenerated artifact.
- `runners.log`, `runners_summary.txt`: the three case configurations.
- `full_suite_summaries.txt`: both full suites (1178 passed, 0 skipped).
- `environment.jsonl`: interpreter and library versions.

## Implementation and tests (second commit)

- `implementation_binding_probes.py` and `_results.json`: 32 record-binding
  probes (GH-DF2). Run from the repository root:
  `python -B -W error reports/phase1g_h_delta_audit_2_evidence/implementation_binding_probes.py OUT.json`.
- `mutation_campaign.py`, `mutation_results.json`, `mutation_campaign.log`:
  56 mutants in disposable copies (`python -B mutation_campaign.py REPO PYTHON
  WORKDIR OUT.json`; WORKDIR outside the repository).
- `build_inventory.py`: assembles `../phase1g_h_delta_audit_2_inventory.json`
  from these results.
