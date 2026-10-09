# Independent audit evidence

Object: d4d693d73f995e2245a5720be227273b3639eda9. All original files remain unchanged.

- `BLIND_CHECKPOINT.md`: scientific reconstruction checkpoint, before author derivation review in that stream; known prompt targets are disclosed.
- `independent_numerics.py`, `independent_results.json`: separate NumPy/SciPy numerical reconstruction, with no project imports. Run from the repository using a scientific Python environment. The script writes its results beside itself. It requires several minutes and a few hundred MB of memory. It is an audit script, not a package runtime.
- For source rehashing, set `TIMESCAPE_AUDIT_SOURCE_DIR` to a temporary source cache containing `GM/main.tex`, `W07/solution.tex`, `W09/observe.tex`, `NW15/cmb1.tex`, `JLH13/voids_mnras.tex`, `EH98/trans.tex`, and `SvdW04.tar`. Use the exact e-print versions in the inventory. Missing cache entries are explicitly recorded as not repeated; the original verified hashes are in `source_hashes.json`. Sources/upstream code are not bundled.
- `anchor_reclosure_counterexample.json`: fixed-closure multiplication versus uniformly rescaled-spectrum PBS recomputation. This is an illustrative convention comparison, not a Boltzmann replacement.
- `evidence_py312.json`, `evidence_py311.json`: saved author-code artifacts, compared numerically. Corresponding logs record 21/21 gates.
- `numeric_reconciliation.json`: comparison summary, inventory rounding checks and coverage limits. Full classified claim rows are in the companion audit inventory.
- `probe_contracts.json`, `probe_extended.json`: public-record, orthant-domain, runner-schema, naming and determinism probes. Nonfinite API failures are described as strings/flags, not accepted as valid scientific output.
- `mutation_results.json`, `mutation_logs/`: baseline and eight existing-test mutation runs. No mutation source copies or mutation executables are committed. The raw logs substantiate failures even where the quiet-output parser left `failed_tests` empty.
- `provenance_claims.json`, `provenance_results.md`, `successor_quotes.json`, `tag_signature_checks.json`: read-only provenance, S1–S13, approvals, AGENTS matrix, exact mathematical signature checks and trust limitations.
- `preservation.json`: all 351 original HEAD files with Git blob identity and SHA-256.
- `full_py*_initial.log`: both initial complete suites, 1132 passed / 32 skipped, warnings as errors.
- `validate_*`, `owner_decisions_final_attempt.log`: successful historical regenerations; `notebook.log` and `validate_b2.log` record blocked oracle coverage.
- `final_suite.log`, `final_governance.json`, `final_validation.json`: final verification after report/inventory assembly. The verification runner writes these records after commands finish and hashes the tested deliverables. No result is inferred from a pending process.
- `manifest.json`: SHA-256 manifest of evidence files, excluding itself. No large figures, full papers, upstream notebook or mutated source trees are included.

Independent script packaging changes only the source-cache/repository path handling of the already-executed scratch calculation; numerical statements and saved results are unchanged. Later reruns may update results and require regenerating the evidence manifest. Original inputs are Planck-like imported parameters and the two declared tracker scenarios; agreement is conditional and non-observational.

`log_packaging.json` records removal of trailing line whitespace from delivered logs to satisfy git diff --check. Original and packaged hashes are listed; no test output text or outcome was changed.
