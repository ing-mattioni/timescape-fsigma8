# Evidence of the second independent delta audit of Phase 1G-H

Report: [`../phase1g_h_delta_audit_2.md`](../phase1g_h_delta_audit_2.md);
inventory: [`../phase1g_h_delta_audit_2_inventory.json`](../phase1g_h_delta_audit_2_inventory.json).

This directory is committed in two steps. The first commit holds only the
blind checkpoint (`BLIND_CHECKPOINT.md`), the code that produced it and its
outputs, before the auditor read the author's evidence artifact or the new
evidence-script functions. Later files are added by the second commit.

- `first_audit_provider.py`: verbatim copy of
  `../phase1g_h_independent_audit_evidence/independent_numerics.py` (same
  SHA-256), used only for the tracker and the EH98 no-wiggle provider.
- `blind_h25_mII_cw.py`: own reconstruction of (H25), m_II, <C_W - 1> and the
  signed/lognormal pair moments (no project import). Usage:
  `python -B -W error blind_h25_mII_cw.py <panels> <nodes_per_panel>`.
- `blind_first_panel.py`: first radial panel [0, 2R/480] contribution.
- `run_*.json`, `first_panel*.json`: outputs (4x24, 16x48, 32x64 nodes).
