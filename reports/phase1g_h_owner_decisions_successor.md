# Phase 1G-H — owner decisions successor record (H-OD1 … H-OD5)

Record classification: `OWNER_DECISIONS_SUCCESSOR_RECORD`.
Date: 2026-10-09. Branch: `ccr-555e67be-u11yht`, on top of `22ace89` (the
fourth delta-audit remediation, pushed in P17).
Machine-readable companion:
[`phase1g_h_owner_decisions_successor_inventory.json`](phase1g_h_owner_decisions_successor_inventory.json).

Cited as:
- [1G-H] = [`phase1g_h_global_variance_closure.md`](phase1g_h_global_variance_closure.md),
  its inventory and validation record; Sec. 9 lists the decisions;
- [AUD4] = [`phase1g_h_delta_audit_4.md`](phase1g_h_delta_audit_4.md), the
  fourth independent delta audit, whose Sec. 11 gives the recommendations
  applied here; [REM4] = its remediation record
  [`phase1g_h_delta_audit_4_remediation.md`](phase1g_h_delta_audit_4_remediation.md);
- [PUB] = [`phase1g_h_publication_successor.md`](phase1g_h_publication_successor.md);
- [1G-B-H] = [`phase1g_b_contract_hardening_successor.md`](phase1g_b_contract_hardening_successor.md).

No equation, initial condition, unit, sign convention, tolerance, status
token or observational authorisation changes. No package module, script or
test changes.

## 1. Authorisation

The project owner, 2026-10-09, verbatim:

> «Ho eseguito le test suite su windows, tutto ok. Dunque Implementa le
> raccomandazioni dell'audit su H-OD1…H-OD5 e poi fai PR, merge, freeze e tag»

It reports the Windows gate (Sec. 2), adopts [AUD4]'s recommendations on
H-OD1 … H-OD5 (Sec. 3) and authorises a pull request, its merge, the freeze
and the tag (Sec. 4). The push of the commit carrying this record to the
session branch is part of the authorised pull request.

## 2. Windows gate

The owner reports that the test suites pass on Windows ("tutto ok"). The
project's Windows gate uses CPython 3.14.3 and 3.11.9. The report does not
state the interpreters, the counts or the commit, so this record states
none. The commits after the last Linux-validated code (`a243bf1`) change
documentation only.

## 3. Decisions H-OD1 … H-OD5

| Decision | Choice (owner, 2026-10-09, adopting [AUD4] Sec. 11) | Meaning |
|---|---|---|
| **H-OD1**, definition and radius convention | Keep the definition as a **named research proposal**: the formal tangent statistic of [1G-H] Sec. 2. Convention (c) (`8 h̄⁻¹ Mpc`, `R_proper·H_D0 = 800 km/s`) is the preferred named convention; (a) is the fixed-mass comparison | It is **not** adopted as the project's σ8 analogue |
| **H-OD2**, void-share closure for a reference value | **No physical reference value** | The values stay reported with their qualifiers: β, the median seed, is a heuristic prior (0.811 / 0.816 at (c)); α, the [W09] seed, is a formal extrapolation (1.121 / 1.057); γ, the interval, holds for constant shares only ([0.261, 0.998] / [0.369, 1.162]) |
| **H-OD3**, status tokens | **No token change** | Neither the two proposed additions nor the change of `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` (`NOT_DERIVED`); the five observational authorisations stay `NOT_GRANTED` |
| **H-OD4**, the runtime | **`global_variance.py` stays experimental** | Imported by no other module, outputs labelled `EXPERIMENTAL_CONDITIONAL_RESEARCH_RUNTIME`; promotion would be a new decision |
| **H-OD5**, publication | **Pull request, merge, freeze and tag decided** | Sec. 4 |

## 4. Pull request, merge, freeze and tag (H-OD5)

- **Pull request** from `ccr-555e67be-u11yht` into `main`. `main` is
  `8d3cdd0`, an ancestor of the branch, so the merge has no conflicts.
- **Merge** with a merge commit, as PR #4, keeping the branch history and
  the commit hashes cited by the records. The merge commit's tree equals
  the branch head's tree.
- **Freeze.** At the merge commit, the 1G-H records become frozen historical
  records: the report, its inventory and validation record; the five
  remediation records; [PUB]; this record; and [1G-B-H], each with its
  inventory and logs. The five audit records were never edited. Later
  corrections are made by successor records only, as for the earlier
  phases.
- **Tag:** the annotated tag `phase-1g-h-global-variance-closure-v1`
  (`phase-<id>-<slug>-v<N>`, with the slug of the phase's local branch) on
  the merge commit. The session cannot sign with the owner's key, so the
  tag is unsigned (the F/G tags are SSH-signed by the owner).
- **What the merge carries.** The experimental runtime and its evidence,
  tests and records. It also carries the 1G-B contract-hardening successor
  ([1G-B-H]: record invariants of `lagrangian_sigma.py`, outputs unchanged),
  so `main` acquires them. The tag `phase-1g-b-lagrangian-sigma-v1` keeps
  attesting `fb5d952`.
- **Not decided or done:** no release; no token or authorisation change; no
  observational statistic, σ8 or fσ8; level C (prediction, observation) is
  not reached.
- **Hashes.** The pull request number, the merge commit and the tag object
  do not exist when this record is committed. As with the F/G freeze, a
  later successor records them, together with the push of this record
  (P18).

## 5. Validation of the tree to be merged

Linux, CPython 3.13.16 and 3.11.17: the full suites, the 1F-C-R validator
and `git diff --check` on the final bytes of this commit. Results are in
the inventory (`validation`). The runtime, evidence script and tests are
those of `a243bf1`, validated in [REM4] Sec. 3 (1212 passed, 0 skipped, 0
failed on both; 36 / 36 gates).
