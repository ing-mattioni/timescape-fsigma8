"""Shared non-colour encoding for all Phase 1C-B2 Figure 3 modes."""

from __future__ import annotations

from math import isclose, pi


# A mode has both a distinct dash pattern and marker, so printed and screen
# figures remain unambiguous in monochrome.  The mapping is common to the
# independent corrected-background and upstream-forensic plotters.
K_MODE_STYLES = {
    2: {
        "linestyle": "-",
        "marker": "o",
        "markevery": 80,
        "markersize": 4.0,
        "description": "solid + circle",
    },
    5: {
        "linestyle": "--",
        "marker": "s",
        "markevery": 80,
        "markersize": 4.0,
        "description": "dashed + square",
    },
    10: {
        "linestyle": "-.",
        "marker": "^",
        "markevery": 80,
        "markersize": 4.5,
        "description": "dash-dot + triangle",
    },
}


def style_for_k(k: float) -> dict:
    """Return the immutable-by-copy non-colour style for k=2,5,10 times pi."""
    ratio = k / pi
    for multiplier, style in K_MODE_STYLES.items():
        if isclose(ratio, multiplier, rel_tol=0.0, abs_tol=1e-12):
            return dict(style)
    raise ValueError(f"no Phase 1C-B2 Figure 3 style for k={k!r}")
