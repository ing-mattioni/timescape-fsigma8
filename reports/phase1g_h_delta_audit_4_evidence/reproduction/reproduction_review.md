# Fourth delta audit — reproduction review

The numerical remediation is equivalent on fresh Linux CPython 3.13.16
(NumPy 2.5.3, SciPy 1.18.1) and 3.11.17 (NumPy 2.4.6, SciPy 1.17.1).
Both H evidence scripts pass all 36 gates. Own recursive flattening with
type-sensitive binary64 equality establishes 3185 unchanged numeric leaves and
16 identically valued renamed leaves; only the two expected `not_shared`
strings differ. All 3201 primary/secondary numeric leaves are identical.
All three primary figure hashes are identical old/new and to the third audit.

The current H inventory has 1193 numerical scalar paths, all explicitly mapped
to regenerated evidence and within half the stated last digit. All 1193 are
also exactly equal to the third auditor's saved full-precision audit values.
All 310 numerical report-table data cells reconcile with the current evidence.
The old auditor's semantic table mapping is reused explicitly: each current
table row must match the immutable baseline row bytes, and only the renamed
export key is adapted. This is a continuity check, not fresh scientific
independence; the independent science role owns that derivation.

All three runner outputs are byte-identical before/after. Their amplitudes are
0.8107722668657138, 1.1213626602036537, 0.9181569463963312. The unchanged scalar
probe program on CPython 3.13.16 confirms 1446 probes; accepted 456→416,
non-strict exports 129→98 (H 12→0), non-finite 8→0; 40 changed probes in exactly
the three declared records; no newly accepted probes.

## Metadata scope correction for the B artifact

Fresh committed 18bf2fb/027b7a4 B validator artifacts differ in exactly one leaf,
`provenance.repository_head`; every other leaf and numeric result is equal.
The author's declared `5746cc76…` hash is reconstructed exactly from either
artifact by substituting only its documented platform, HEAD 18bf2fb and
dirty-working-tree=true. Thus the historical same-HEAD working-code comparison
is corroborated; a universal byte-identity claim across committed trees needs
a metadata qualifier. This is LOW documentation scope, not a numerical
regression. Likewise the author's H hash `027b8e124…` is exactly reconstructed
with only its documented environment block replaced. Complete hashes and
substitutions are retained in the two hash-scope JSON records.

## Input regeneration and execution limit

All ignored inputs were independently regenerated: upstream full 20-cell
notebook and 5 figures, three oracles, 1D-B, B2, owner MonteCarlo (124/124 gates;
924.425 s), and 1D-D in clean 18bf2fb worktree (920.61 s; all gates, final
deterministic serialization, its own two suites 1154 passed, 31 skipped each
because baseline inputs were absent). The final 1D-D artifact was copied to
the audited tree.

Original notebook runner startup failed before any scientific cell: sandbox
denied ZMQ TCP resolver and then Unix IPC bind. The external adapter executes
verbatim cells in a fresh Python process/namespace without sockets, preserving
the original project runners and upstream source. This explicitly deviates
from a fresh Jupyter kernel and does not reproduce its rich-display transport.
The three original oracle extraction scripts run through the same adapter.
The notebook's large-data `legend(loc="best")` UserWarning was surfaced and
documented; no warning suppression was added. Independent package/oracle gates
pass. All mandatory audited full suites use `-B -W error` and
`OPENBLAS_NUM_THREADS=1`.

The Windows owner gate CPython 3.14.3/3.11.9 is unavailable and NOT_RUN.
No tracked code, tests, scripts or existing reports were modified by this role.
The tolerance audit reports 750 comparisons, 0 missing tolerances.

## Full suites

Both initial audited full suites completed with 1207 passed, zero skipped,
failed or warnings: CPython 3.13.16 in 424.62 s and 3.11.17 in 475.29 s.
Completion records are in `full_py313.log`, `full_py311.log` and their
`_execution.json` companions. A separate final-tree primary run will follow
the root auditor's deliverable preparation signal.
