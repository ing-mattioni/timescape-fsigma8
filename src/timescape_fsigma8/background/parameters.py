"""Tracker parameters and shared input validation.

References: [GM] = arXiv:2511.17160v2 (Galoppo & Mourier, JCAP 02 (2026)
066); [W09] = arXiv:0909.0749 (Wiltshire, PRD 80, 123512 (2009)). See the
`timescape_fsigma8.background` package docstring for conventions and the
documented deviations (D1), (D2).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray


@dataclass(frozen=True)
class TrackerParams:
    """The two free parameters of the timescape tracker ([GM] Sec. 5.1.1).

    fv0 : present-day void volume fraction, 0 < fv0 < 1.
    HD0 : present-day *bare* (volume-average) Hubble parameter H_{D,0},
          in inverse units of the time variable passed to all functions.
    """

    fv0: float
    HD0: float

    def __post_init__(self) -> None:
        if not 0.0 < self.fv0 < 1.0:
            raise ValueError(f"fv0 must be in (0, 1), got {self.fv0}")
        if self.HD0 <= 0.0:
            raise ValueError(f"HD0 must be positive, got {self.HD0}")

    @classmethod
    def from_dressed_H0(cls, fv0: float, H0: float) -> "TrackerParams":
        """Construct from the dressed (observed) Hubble constant H0.

        H_{D,0} = 2 H0 (2 + fv0) / (4 fv0^2 + fv0 + 4)
        [GM] text p. 25 ("one gets at present time the relation..."),
        equivalent to [W09] (B8)-(B9) at t = t0.
        """
        return cls(fv0=fv0, HD0=2.0 * H0 * (2.0 + fv0) / (4.0 * fv0**2 + fv0 + 4.0))

    @property
    def H0_dressed(self) -> float:
        """Dressed Hubble constant H0 = H_{D,0} (4 fv0^2 + fv0 + 4) / (2 (2+fv0)).

        Inverse of the relation in `from_dressed_H0`; [W09] (B8) at t0.
        """
        return self.HD0 * (4.0 * self.fv0**2 + self.fv0 + 4.0) / (2.0 * (2.0 + self.fv0))

    @property
    def t0(self) -> float:
        """Present volume-average age, t0 = (2 + fv0) / (3 H_{D,0}).

        [W09] text after (B5); equivalently H_D(t0) = HD0 in [W09] (B6).
        """
        return (2.0 + self.fv0) / (3.0 * self.HD0)

    @property
    def aD0(self) -> float:
        """Present-day scale-factor normalisation a_{D,0}/a_{w,0} = 1 + fv0/2.

        From the wall-lapse closure gamma_w = 1 + f_v/2 evaluated today,
        with a_w = gamma_w^{-1} a_D normalised to a_{w,0} = 1:
        [GM] Eq. (5.4) and text p. 25 ("a_{D,0}/a_{w,0} = 1 + f_{v,0}/2");
        [W09] (B7).
        """
        return 1.0 + self.fv0 / 2.0


def _t(t: ArrayLike, *, allow_zero: bool = False) -> NDArray[np.float64]:
    """Coerce `t` to a float64 array and enforce the tracker domain.

    The tracker solution [GM] (5.5)-(5.6) is defined for t > 0 only; all
    background functions reject t <= 0 with a ValueError rather than
    returning silent infinities/NaNs. This is input validation, not a
    formula change (AGENTS.md rule 3). `tau_w` alone admits t = 0
    (allow_zero=True), where its closed form has the exact finite limit
    tau_w(0) = 0 ([W09] (B12)).
    """
    arr = np.asarray(t, dtype=np.float64)
    if allow_zero:
        if np.any(arr < 0.0):
            raise ValueError("tracker time t must be >= 0")
    elif np.any(arr <= 0.0):
        raise ValueError("tracker time t must be > 0 (tracker domain, [GM] (5.5)-(5.6))")
    return arr
