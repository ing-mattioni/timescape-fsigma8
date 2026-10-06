# Phase 1G-F successor / 1G-G — local validation record

Date: 2026-10-01. Base commit:
`fb5d95245bc0cb19ce6cd1438177f1a597bb232f`.

## Current successor to this historical validation (2026-10-02)

This record below preserves the 2026-10-01 work and its limitations.
The independent audit subsequently reported 1125/0/0 full-suite results
on Windows Python 3.14.3 and 3.11.9 for that pre-remediation tree.
The approved D classification and F verdict split, audit corrections,
new local validation and remaining final-tree gates are recorded in
`phase1g_fg_audit_remediation.md` and its inventory. Statements below
such as “no independent audit” or “status values preserved” describe only
the original work, not the current successor state.

## Scope and authorization

The owner authorized the proposed F correction, theoretical G continuation
and CLAUDE.md repair. F1-F3 change the scientific interpretation of the
cumulative volume normalization; this is explicitly not a refactor. G is
conditional theory with report-evidence scripts and tests, not a new
package runtime. Original reports, inventories and scientific-status
values are preserved. No push, PR, remote mutation, phase tag or independent
adversarial audit was performed.

Work used a GitHub-downloaded source snapshot, not a checkout with Git
history. The 259-file base manifest was checked against Git blob hashes:
**257 original files remain identical**; only README.md and CLAUDE.md
change. The nine new files are two reports, two inventories, two evidence
scripts, two test modules and this validation record. The downloadable
integration bundle contains a patch, changed files, generated evidence and
SHA-256 manifest. It does not manufacture a Git history or a parent commit.

## Observed validation

Environment: CPython 3.12.14, NumPy 2.3.5, SciPy 1.17.0, pytest 9.1.1;
Linux. Test commands use `PYTHONPATH=src OPENBLAS_NUM_THREADS=1`, Python
`-B -W error`, and pytest `-q`. No warnings were suppressed. No project
dependency file was edited. The test dependency was installed in the local
execution environment when it was unavailable.

| Run | Observed result | Meaning |
|---|---|---|
| Full suite with initial 31 new tests | 1089 passed, 34 skipped, 1 failed; 220.20 s | One existing Git-history test cannot run in a snapshot |
| Final two F/G test modules, including the added archive adapter | 32 passed; 5.30 s | Final scientific code and adapter covered |
| F successor evidence | completed | Primary C1 histories recomputed; 84 archived populations corrected algebraically |
| G evidence | completed | Tracker and first-moment gates passed |
| Original-file preservation | 257 unchanged, 2 documentation edits | Frozen code/reports/statuses preserved |

The optional archived-population adapter and its additional test were added
after the full-suite collection. The final targeted run checks that change;
the full suite was not redundantly rerun. The full-suite count is therefore
not presented as a 1090-pass final full-suite result.

The sole full-suite failure is
`test_gb_od3_the_frozen_inventory_is_pinned_to_its_certified_blob` in
`tests/test_phase1g_b_owner_decisions.py`. It executes `git show` against
historical commit `118b8f3af3c1360b0da74df8e9a9cb3ba1fed83a`; the process
fails because the downloaded snapshot has no Git history. The historical
file was separately refetched through GitHub: its blob is
`745b5b9acce2a7de71d950c7d00a4387fd0d7df2`, identical to the current
certified inventory. This independent check does not turn the pytest
failure into a pass. Missing optional oracle/generated evidence accounts
for the skipped tests; those inputs were not fabricated.

Only one Python version was available. The workflow's dual-interpreter
preflight and independent-audit requirements for a frozen phase are **not
certified** by this record. The source snapshot is suitable for a reviewable
patch; it is not a clean-branch freeze claim. Before a formal phase freeze,
apply in a real checkout, run the existing two-environment gates with their
required artifacts, obtain the independent audit and record the actual
commit. Remote publication still needs explicit owner authorization under
AGENTS.md rule 7.

## Numerical checks and limits

F tests compare the corrected normalization with independently calculated
physical bin volumes, verify additivity and unit invariance, validate
normalization and vacuum limits, reject invalid selections, compare the
spherical threshold to [JLH13]'s printed values, and check corrected
cumulatives and the two-epoch cutoff mismatch. The archive adapter preserves
scenario keys and input bytes; the delivered run processed all 84 cases.
It retains historical C3 calibration and does not recompute its clocks.

G tests integrate the collision equation numerically using DOP853,
`rtol=2e-11`, `atol=2e-13`, independently of the analytic distribution.
The comparison uses `rtol=1e-8`, `atol=2e-12`. First-moment normalization
uses absolute tolerance 2e-12 with analytic tail completion. The conditional
tracker identity uses 2e-14, and an independent fraction ODE uses 3e-11.
Other exact algebraic checks use explicitly stated 2e-15 tolerances.

No new Monte Carlo variance run was needed: the correction changes only
cut-dependent cumulative volume normalization, while the inherited
variance uses the full size shape and independently supplied tracker
coverage. The earlier full frozen F run reproduced the primary variance
and passed its own MC gates. The quoted sigma approximately 0.99 remains
**conditional hybrid evidence**, with no error bar for the missing
population evolution or nonlinear wall dynamics.

## Documentation state verified against GitHub

The owner decisions were merged via PR #3. The following annotated tag
objects all target base commit `fb5d95245bc0cb19ce6cd1438177f1a597bb232f`:

| Phase tag | Tag object SHA |
|---|---|
| phase-1g-a-sigma8-derivation-path-v1 | f5fceeae4491afaa418fa1e37322e97a8a924280 |
| phase-1g-b-lagrangian-sigma-v1 | a279464a52eb767e6840be8774375eac7885d5c3 |
| phase-1g-c-two-scale-growth-law-v1 | 88e96be855e5aca117e6ac12872fdb5070494b59 |
| phase-1g-d-separate-universe-growth-v1 | e2a3b303e2441dd94971a32b7ec327a44f2af000 |
| phase-1g-e-two-phase-sigma-v1 | 2a48639c8cdf6217d6b1c8293a06722eba48e38d |

No 1G-F tag was returned. Tag existence and targets were checked, not
cryptographic signature validity. CLAUDE.md's stale pre-merge/pre-tag text
and README's current-phase heading are updated accordingly, and distinguish
the new local F/G work from the merged and tagged historical phases.

## Integration boundaries

- No edits to AGENTS.md, `src/`, frozen scripts, old reports or old tests.
- No new scientific-status token or reinterpretation of authorization.
- No derived formation history, physical merger kernel, common-spacetime
  embedding, spatial correlation evolution or observational sigma8/f-sigma8.
- G's conservation arguments assume additive regional volumes and the
  stated common clock; wall absorption and non-additive mergers require
  explicit source terms. The benchmark does not evolve the F population.

These limitations are part of the deliverable, not waived freeze gates.
