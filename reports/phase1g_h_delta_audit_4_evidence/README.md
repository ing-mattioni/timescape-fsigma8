# Fourth independent delta-audit evidence

All files are auditor evidence. Production sources, existing tests, frozen records and older audit files were not changed. Two infrastructure failure logs have trailing spaces stripped for git diff --check; original and archived hashes and the exact transformation are recorded in the inventory. Script source bytes are preserved.

The root report/inventory are the authority for findings and interpretation. Evidence includes exact Git-blob preservation proofs, read-only remote snapshot, immutable initial science checkpoint plus explicitly post-checkpoint recipe correction, scalar and mutation probes, and independent numerical comparisons.

Rerun verification scripts only from copies in external scratch. Several scripts retain their original acquisition layout and repository paths as execution evidence; update those paths only in the external copy. The reproduction driver expects an external root containing repo/, baseline/, oldscalar/, .venv313/, .venv311/, and audit_work/reproduction/. Scientific scripts run together in an external science directory. They write their results beside themselves and must not overwrite this archive.

The generated historical mutation runner requires an external work directory and definitions. Altered runtime copies are never committed. The environmental non-git baseline failure is explicitly subtracted before counting kills.

NoSocketNotebookClient is an external execution adapter, not a modified project/notebook source. Both ordinary TCP and IPC kernel startup were blocked before any notebook cell by sandbox socket permissions. The adapter runs each original runner in a fresh Python process, executes original notebook cells verbatim, and preserves stream output parsing. This is a declared infrastructure deviation; no standard Jupyter execution success is claimed. The original upstream source is not copied into this evidence.

Large regenerated artifacts and figures remain ignored, with hashes, exact numeric comparison summaries and logs retained here. The 1G-B raw historical hash is metadata-scoped; committed-tree equality excludes only the explicitly identified provenance.repository_head difference. Full final validation closure is recorded after the report/inventory exist.
