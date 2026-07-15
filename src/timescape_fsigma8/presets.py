"""Immutable named parameter presets for the timescape tracker.

Two reference parametrisations exist in the sources because the paper text
and the upstream notebook disagree on the dressed Hubble constant
(documented in reports/upstream_reproducibility.md §11.1 and
reports/background_equation_audit.md §7.4):

  PAPER_REFERENCE      H0 = 73.03 km/s/Mpc — the value printed in
                       [GM] Sec. 5.1.1 (from the best fit of their
                       ref. [80]).
  NOTEBOOK_REFERENCE   H0 = 73.23 km/s/Mpc — the value the upstream
                       notebook actually computes with (cell 2,
                       h = 0.7323); also the value consistent with
                       [GM]'s own quoted H_{D,0} ~ 58.01 km/s/Mpc.

Both share f_v0 = 0.737 ([GM] Sec. 5.1.1). Neither preset stores H_{D,0}:
the bare rate is always *derived* from the dressed one via
TrackerParams.from_dressed_H0 ([GM] p. 25; [W09] (B8)-(B9) at t0).

Unit policy: every dimensionful field name carries its unit
(`H0_dressed_km_s_Mpc`); `tracker_params_gyr` converts through the audited
constants of timescape_fsigma8.units, yielding TrackerParams in Gyr units
(HD0 in Gyr^-1, so all background functions then take t in Gyr).
"""

from __future__ import annotations

from dataclasses import dataclass

from timescape_fsigma8 import units
from timescape_fsigma8.background import TrackerParams


@dataclass(frozen=True)
class ReferencePreset:
    """A named, immutable tracker parametrisation with explicit units."""

    name: str
    fv0: float                    # present-day void fraction (dimensionless)
    H0_dressed_km_s_Mpc: float    # dressed Hubble constant [km s^-1 Mpc^-1]
    source: str                   # citation for the parameter values

    @property
    def H0_dressed_per_gyr(self) -> float:
        """Dressed Hubble constant in Gyr^-1 (audited conversion)."""
        return units.kms_per_mpc_to_per_gyr(self.H0_dressed_km_s_Mpc)

    @property
    def tracker_params_gyr(self) -> TrackerParams:
        """TrackerParams in Gyr units: HD0 in Gyr^-1, time arguments in Gyr.

        H_{D,0} is derived from the dressed H0 (never inserted manually):
        [GM] p. 25; [W09] (B8)-(B9) at t0.
        """
        return TrackerParams.from_dressed_H0(fv0=self.fv0, H0=self.H0_dressed_per_gyr)

    @property
    def HD0_bare_km_s_Mpc(self) -> float:
        """Derived bare Hubble constant H_{D,0} in km s^-1 Mpc^-1."""
        return TrackerParams.from_dressed_H0(
            fv0=self.fv0, H0=self.H0_dressed_km_s_Mpc).HD0


PAPER_REFERENCE = ReferencePreset(
    name="PAPER_REFERENCE",
    fv0=0.737,
    H0_dressed_km_s_Mpc=73.03,
    source=("f_v0: [GM] Sec. 5.1.1; H0: [GM] Sec. 5.1.1 text / Fig. 1 "
            "caption, 'H0 = 73.03 km/(s Mpc)' from the best fit of [GM] "
            "ref. [80]"),
)

NOTEBOOK_REFERENCE = ReferencePreset(
    name="NOTEBOOK_REFERENCE",
    fv0=0.737,
    H0_dressed_km_s_Mpc=73.23,
    source=("f_v0: upstream ACPT_Timescape.ipynb cell 1; H0: cell 2, "
            "h = 0.7323 => 73.23 km/(s Mpc); consistent with [GM]'s own "
            "derived H_D,0 ~ 58.01 km/(s Mpc) (0.792222 x 73.23 = 58.01)"),
)
