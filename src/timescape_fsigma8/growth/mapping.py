"""Solver-harmonic density-contrast coefficient mapping (Phase 1D-B).

Implements the frozen Phase 1D-A relation (D1b-code) only:

    delta_m,k(t) = -Delta_d,k(t) / k_code^2,

with the documented negative-Laplacian eigenvalue convention
``(3)Lap Q_k = -(k_code^2/a_D^2) Q_k`` ([GM] footnote 8 with the sign
implemented in [GM] (4.10); 1D-A audit Secs. 3-4).  ``Delta_d`` is the CGI
Laplacian density scalar, NOT the ordinary local density contrast; the
mapped ``delta_m`` values are solver-harmonic coefficients only.  No
conversion to observational or dressed comoving wavenumbers is performed
and no ``k_com_obs`` is invented (1D-A Sec. 10 blocker).

The mapping is a pure conversion: it never reruns or alters a perturbation
solution, and relative growth histories and logarithmic rates are invariant
under it because the constant harmonic factor cancels (1D-A Sec. 6).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np
from numpy.typing import NDArray

from timescape_fsigma8.growth.scenarios import GrowthWavenumberConvention


class HarmonicSignConvention(str, Enum):
    """Documented harmonic eigenvalue sign.

    The only scientifically supported value is the negative-Laplacian
    eigenvalue convention audited in Phase 1C-A/1D-A.  No other sign is
    silently accepted; the member must be passed explicitly.
    """

    NEGATIVE_LAPLACIAN_EIGENVALUE = "negative_laplacian_eigenvalue"


@dataclass(frozen=True)
class HarmonicMetadata:
    """Explicit harmonic metadata required by the delta_m mapping.

    ``k_code`` is the dimensionless matrix label of the mode (equal to the
    frozen ``ResolvedWavenumber.matrix_k`` for barotropic runs, or the
    caller-supplied explicit label for a clean-system per-mode coefficient).
    The volume-average fields repeat the 1D-A (D1c) relations as metadata
    only (units of H0_TS/c): ``k_com_D_H0TS_over_c = k_code`` and
    ``k_phys0_D_H0TS_over_c = k_code/a_D0``.  No observational/dressed
    comoving wavenumber exists here.
    """

    mode_label: str
    k_code: float
    wavenumber_convention: GrowthWavenumberConvention
    sign_convention: HarmonicSignConvention
    k_com_D_H0TS_over_c: float
    k_phys0_D_H0TS_over_c: float

    def __post_init__(self) -> None:
        if not isinstance(self.sign_convention, HarmonicSignConvention):
            raise ValueError(
                "sign_convention must be an explicit HarmonicSignConvention"
            )
        if (
            self.sign_convention
            is not HarmonicSignConvention.NEGATIVE_LAPLACIAN_EIGENVALUE
        ):  # pragma: no cover - enum has one member; guards future edits
            raise ValueError(
                "only the documented negative-Laplacian eigenvalue convention "
                "is scientifically supported"
            )
        if not isinstance(
            self.wavenumber_convention, GrowthWavenumberConvention
        ):
            raise ValueError(
                "wavenumber_convention must be an explicit "
                "GrowthWavenumberConvention"
            )
        if not np.isfinite(self.k_code) or self.k_code <= 0.0:
            raise ValueError(
                f"k_code must be finite and positive, got {self.k_code!r}"
            )
        if not self.mode_label:
            raise ValueError("mode_label must be a nonempty string")

    def to_metadata(self) -> dict:
        return {
            "mode_label": self.mode_label,
            "k_code": self.k_code,
            "wavenumber_convention": self.wavenumber_convention.value,
            "sign_convention": self.sign_convention.value,
            "k_com_D_H0TS_over_c": self.k_com_D_H0TS_over_c,
            "k_phys0_D_H0TS_over_c": self.k_phys0_D_H0TS_over_c,
        }


def map_delta_m(
    delta_d: NDArray[np.float64], *, harmonic: HarmonicMetadata
) -> NDArray[np.float64]:
    """Return the solver-harmonic coefficient delta_m = -Delta_d/k_code^2.

    1D-A Eq. (D1b-code), from [GM] (2.2)+(2.19)+(2.20) and footnote 8.
    Pure conversion; the input array is not modified.
    """
    if not isinstance(harmonic, HarmonicMetadata):
        raise ValueError("harmonic must be explicit HarmonicMetadata")
    out = np.asarray(delta_d, dtype=np.float64) / (-harmonic.k_code**2)
    out.flags.writeable = False
    return out


def map_delta_m_dln_a_derivative(
    d_delta_d_dln_a: NDArray[np.float64], *, harmonic: HarmonicMetadata
) -> NDArray[np.float64]:
    """Map a non-logarithmic Delta_d derivative to the delta_m coefficient.

    d delta_m/d ln a = -(1/k_code^2) d Delta_d/d ln a, i.e. the mapped
    non-logarithmic derivatives obey the documented -1/k_code^2 factor
    (1D-B specification Sec. 2.2; with d Delta_d/d ln a_D = -3Z/Theta this
    yields d delta_m/d ln a_D = +3Z/(Theta k_code^2)).
    """
    if not isinstance(harmonic, HarmonicMetadata):
        raise ValueError("harmonic must be explicit HarmonicMetadata")
    out = np.asarray(d_delta_d_dln_a, dtype=np.float64) / (-harmonic.k_code**2)
    out.flags.writeable = False
    return out
