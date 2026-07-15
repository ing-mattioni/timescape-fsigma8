"""timescape_fsigma8 — independent implementation of averaged-cosmology models.

Phase 1B: Timescape tracker background (`background` package), audited
unit conversions (`units`), and immutable parameter presets (`presets`:
PAPER_REFERENCE, NOTEBOOK_REFERENCE).
Scientific specification: arXiv:2511.17160v2 (Galoppo & Mourier, JCAP 02
(2026) 066) and the original Timescape references, principally Wiltshire,
PRD 80, 123512 (2009) [arXiv:0909.0749]. The upstream notebook pinned in
UPSTREAM.lock is used only as a numerical comparison oracle, never as a
source of implementation.
"""

from timescape_fsigma8.background import TrackerParams

__all__ = ["TrackerParams"]
