"""Conditional, model-internal, mass-labelled linear sigma(M) (Phase 1G-B).

Authorisation: project owner, 2026-09-29 ("let a sub-agent perform Phase
1G-B"), implementing recommendation 2 of the report-only Phase 1G-A audit
(``reports/phase1g_a_sigma8_derivation_path_audit.md``, cited as [1G-A]).
Validation record: ``reports/phase1g_b_lagrangian_sigma_validation.md``.

What this module computes
-------------------------
The linear rms mass fluctuation today, top-hat smoothed at a Lagrangian
radius R in photon-normalised comoving Mpc,

    sigma^2(R) = integral dln k  Delta^2(k) W^2(k R),                   (1)

for the Timescape tracker, from an explicitly imported early-universe
spectrum and an explicitly selected growth law.  It is a CONDITIONAL,
MODEL-INTERNAL, LINEAR quantity labelled by the Lagrangian mass
``M = (4 pi/3) rho_crit(100 km/s/Mpc) omega_m,eff R^3``.  It is NOT the
observational sigma_8 (whose values are compressed in a LCDM fiducial,
1D-C Sec. 23; 1E-A), NOT f sigma_8, and carries no observational
authorisation: ``scientific_status.SIGMA8_AUTHORIZATION`` and
``OBSERVATIONAL_AUTHORIZATION`` stay ``NOT_GRANTED``.  Per 1D-C Sec. 19 no
public function/class name or output key carries the observational tokens;
they appear only inside the negative status values ``SIGMA8_STATUS =
"NOT_OBSERVATIONAL_SIGMA_8"`` and ``FSIGMA8_STATUS = "NOT_FSIGMA8"`` (same
pattern as ``transfer.h1_realization.FSIGMA8_STATUS``).

Ingredients and sources
-----------------------
* Growth law (mandatory ``GrowthLaw``; neither is a default; the choice is
  scale-dependent and is analysed in Phase 1G-C):

  - ``VOLUME_AVERAGE_CGI``: the regular growing mode of the [GM] comoving
    closure, Eqs. (4.21)-(4.23), or of the Meszaros comparator, Eq. (4.27),
    on the volume-average background ([1G-A] Secs. 4.3, 5).  Growth relative
    to volume-average Einstein-de Sitter (EdS) growth is

        g_TS = lim_{t_e->0} [D(t0)/D(t_e)] [a_D(t_e)/a_D0]
             = exp integral_{t_e}^{t0} (u - t Theta/3) d ln t,           (2)

    with ``u = t dln Delta_d/dt`` from ``perturbations.growing_mode`` and
    ``t Theta/3 = dln a_D/dln t`` ([GM] Eq. (3.6)).  The barotropic closure
    ([GM] Eqs. (4.13)-(4.17)) is refused: it is Hadamard ill-posed for
    c^2_s,eff < 0 and admits no finite linear sigma ([1G-A] Sec. 4.1).
  - ``WALL_REGIONAL_EDS_COMMON_TIME``: sub-homogeneity modes grow as the EdS
    growing mode of the wall region in the common Buchert time t
    ([1G-A] Sec. 8; [W09] two-scale solution with no backreaction inside
    walls).  On the tracker the regional wall volume scale obeys
    a_w,reg^3 = (1 - f_v) a_D^3 proportional to t^2 ([GM] Eq. (5.1) meaning of
    a_w, [W09] e-print lines 1763-1764; [1G-A] Sec. 5.3), and the regional
    density (1 - f_v)^-1 <rho>_D = 1/(6 pi G t^2) is exactly EdS.  Then

        g_wall = (1 - f_v0)^(1/3),                                       (3)

    and the growth today relative to photon-normalised EdS is
    ``gamma_w0 (1 - f_v0)^(1/3) = (1/2)(2 + f_v0)(1 - f_v0)^(1/3)``.
    Evidence class ``DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION``; the regional
    embedding stays ``NOT_DERIVED`` (``scientific_status``).

* Photon normalisation ([1G-A] Sec. 5.1): with ``1 + z = a_w0/a_w``,
  ``a_w = a_D/gamma_w``, ``gamma_w = 1 + f_v/2`` ([GM] Eq. (5.4), text
  p. 25), the growth today of a mode with ``D/a_photon -> 1`` early,
  ``a_photon := 1/(1+z)``, is ``gamma_w0 g``.

* Early matter density per photon ([1G-A] Sec. 6.2, derived identity):

        omega_m,eff = <rho>_D0 gamma_w0^3 / rho_crit(100)
                    = (1/2)(1 - f_v0)(2 + f_v0)(H_D0/100)^2,             (4)

  from ``<rho>_D proportional to a_D^-3`` and
  ``<rho>_D0 = 12 H_D0^2 (1-f_v0)/[8 pi G (2+f_v0)^2]`` ([GM] p. 25).

* Early spectrum, ``PROVISIONAL_MODEL_IMPORT`` ([1G-A] Sec. 6.3): at equal
  photon temperature in the matter era (Poisson equation with
  Phi = -(3/5) zeta),

        Delta^2(k) = (4/25) A_s (k/k_p)^(n_s-1) (k/aH)^4 T^2(k) D0^2 / a^2,
        (aH)^2 = H100^2 omega_m / a,                                      (5)

  i.e. ``Delta^2 = (4/25) A_s (k/k_p)^(n_s-1) (k c/100)^4 T^2 D0^2/omega_m^2``
  with k in Mpc^-1 and c in km/s.  T(k) is the Eisenstein & Hu (1998)
  zero-baryon-oscillation fit, Eqs. (26), (28)-(31) of astro-ph/9709112
  ([EH98]), which depends only on the physical densities.

* Window (1D-A chain D5): ``W(x) = 3 (sin x - x cos x)/x^3``, evaluated by
  its Maclaurin series ``1 - x^2/10 + x^4/280 - x^6/15120 + x^8/1330560``
  for ``|x| < TOP_HAT_SERIES_THRESHOLD``.

* Radius conventions ([1G-A] Sec. 6.4, ``CONVENTION_DEPENDENT``), all in
  photon-normalised comoving Mpc: equal Lagrangian mass to an explicitly
  supplied reference ``R = R_ref (omega_ref/omega_m,eff)^(1/3)``; dressed
  ``L/h_dressed`` of wall-comoving length; bare ``(L/h_bare)/gamma_w0`` of
  present volume-average proper length; or an explicit radius.  The length
  ``L`` (in h^-1 Mpc) is always an explicit input.

* Flat-LCDM reference with the same machinery: growth ``qplus(0)`` of the
  frozen recipe (``D/a -> 1``), ``omega_m = Omega_m h^2``.  Anchored ratios
  ``sigma_TS/sigma_LCDM x anchor`` use an explicitly supplied anchor value;
  the module ships no anchor, no Planck parameter set and no survey value.

References: [GM] Galoppo & Mourier, arXiv:2511.17160v2 (JCAP 02 (2026) 066);
[W09] Wiltshire, arXiv:0909.0749v2; [EH98] Eisenstein & Hu, ApJ 496, 605,
astro-ph/9709112.  Every scientific choice is a mandatory keyword-only
argument; inapplicable choices are passed as the explicit ``NOT_APPLICABLE``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from numbers import Integral, Real

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.integrate import simpson

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams
from timescape_fsigma8.perturbations.growing_mode import (
    CleanPerturbationSystem,
    GrowingModeConfig,
    REGULAR_GROWING_MODE_REFERENCE_CONFIG,
    regular_growing_mode_coefficients,
)
from timescape_fsigma8.perturbations.initial_conditions import (
    LCDMGrowthRecipe,
    qplus,
)
from timescape_fsigma8.presets import ReferencePreset

__all__ = [
    # status / provenance constants
    "SCIENTIFIC_CLASSIFICATION",
    "OBSERVATIONAL_STATUS",
    "SIGMA8_STATUS",
    "FSIGMA8_STATUS",
    "EARLY_SPECTRUM_IMPORT_STATUS",
    "RADIUS_CONVENTION_STATUS",
    "VOLUME_AVERAGE_CGI_EVIDENCE_CLASS",
    "WALL_REGIONAL_EVIDENCE_CLASS",
    "NOT_APPLICABLE",
    "SPEED_OF_LIGHT_KM_S",
    "TOP_HAT_SERIES_THRESHOLD",
    "REFERENCE_MATCH_RTOL",
    # enums
    "GrowthLaw",
    "EarlyTransferModel",
    "LagrangianRadiusConvention",
    # errors
    "LagrangianSigmaContractError",
    "BarotropicClosureRefusedError",
    "LagrangianSigmaNumericalError",
    # inputs and configurations
    "TimescapeTrackerInput",
    "EarlySpectrumImport",
    "LagrangianRadiusSpec",
    "VolumeAverageGrowthNumerics",
    "WallRegionalGrowthChecks",
    "LagrangianSigmaQuadrature",
    "VOLUME_AVERAGE_GROWTH_REFERENCE_NUMERICS",
    "WALL_REGIONAL_GROWTH_REFERENCE_CHECKS",
    "LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE",
    # result records
    "TimescapeGrowthFactor",
    "EarlyMatterDensityPerPhoton",
    "ResolvedLagrangianRadius",
    "ConditionalLagrangianSigma",
    "LCDMReferenceLinearSigma",
    "AnchoredLagrangianSigmaRatio",
    # functions
    "top_hat_window",
    "eh98_zero_baryon_transfer",
    "matter_era_linear_amplitude",
    "timescape_growth_factor",
    "early_matter_density_per_photon",
    "resolve_lagrangian_radius",
    "conditional_lagrangian_linear_sigma",
    "lcdm_reference_linear_sigma",
    "anchor_lagrangian_sigma",
]


# --------------------------------------------------------------------------
# Status and provenance constants (part of the API; do not relabel)
# --------------------------------------------------------------------------

SCIENTIFIC_CLASSIFICATION = "CONDITIONAL_MODEL_INTERNAL_LINEAR_SIGMA_M"
# Same tokens as transfer.h1_realization (OBSERVATIONAL_STATUS, FSIGMA8_STATUS).
OBSERVATIONAL_STATUS = "NON_OBSERVATIONAL"
SIGMA8_STATUS = "NOT_OBSERVATIONAL_SIGMA_8"
FSIGMA8_STATUS = "NOT_FSIGMA8"
EARLY_SPECTRUM_IMPORT_STATUS = "PROVISIONAL_MODEL_IMPORT"
RADIUS_CONVENTION_STATUS = "CONVENTION_DEPENDENT"
# Evidence classes of the two growth laws ([1G-A] Sec. 4.3 and Sec. 8).
VOLUME_AVERAGE_CGI_EVIDENCE_CLASS = "DERIVED_FROM_VERIFIED_DEFINITIONS"
WALL_REGIONAL_EVIDENCE_CLASS = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"

# Explicit value for an inapplicable choice (same spelling as phase1f_a).
NOT_APPLICABLE = "NOT_APPLICABLE"

# Speed of light in vacuum, exact by the SI definition of the metre (1983).
SPEED_OF_LIGHT_KM_S = 299_792.458

# Below this |x| the top-hat window uses its Maclaurin series through x^8.
# Truncation error < x^10/(1.6e8) < 1e-18 at the threshold; the closed form
# above it loses at most ~eps/x^2 ~ 2e-14 relative to cancellation.
TOP_HAT_SERIES_THRESHOLD = 0.1

# Relative tolerance for "the same reference" checks between the equal-mass
# radius convention and the LCDM reference record (round-off allowance for
# independently evaluated Omega_m h^2 products).
REFERENCE_MATCH_RTOL = 1e-12

_BAROTROPIC_REFUSAL = (
    "the barotropic closure ([GM] Eqs. (4.13)-(4.17)) is refused: for the "
    "Timescape c^2_s,eff < 0 its Cauchy problem is Hadamard ill-posed, the "
    "linear amplitude grows like exp(k alpha), and no finite linear sigma "
    "exists for any smoothing radius (Phase 1G-A Sec. 4.1); use "
    "CleanPerturbationSystem.COMOVING (or MESZAROS as comparator) with "
    "GrowthLaw.VOLUME_AVERAGE_CGI"
)

_SCALE_DEPENDENCE_CAVEAT = (
    "growth_law_scale_dependence: the volume-average CGI law applies to "
    "super-homogeneity modes and the wall-regional EdS law to mass-weighted "
    "sub-homogeneity statistics; the choice is scale-dependent, is analysed "
    "in Phase 1G-C, and neither law is a default"
)

_CAVEATS = {
    "volume_average_cgi:comoving": (
        "volume_average_cgi_comoving: regular growing mode of the [GM] "
        "comoving closure, Eqs. (4.21)-(4.23), on the volume-average "
        "background; the [GM]-preferred parametrisation (Phase 1G-A Sec. 4.3)"
    ),
    "volume_average_cgi:meszaros": (
        "volume_average_cgi_meszaros_comparison_only: [GM] Eq. (4.27) is "
        "formally inapplicable to the Timescape framework ([GM] Sec. 5.1.1) "
        "and is retained only as a comparison baseline"
    ),
    "wall_regional_eds_common_time:NOT_APPLICABLE": (
        "wall_regional_eds_common_time: sub-homogeneity modes assumed to grow "
        "as the EdS growing mode of the wall region in the common Buchert time "
        "t (Phase 1G-A Sec. 8; [W09] no backreaction within walls); evidence "
        "class DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION; the regional "
        "embedding stays NOT_DERIVED"
    ),
}

_GENERIC_LIMITATIONS = (
    "conditional model-internal linear sigma(M); not an observational amplitude",
    "not comparable with survey or CMB amplitude values without a Timescape "
    "reduction of the data (Phase 1D-C Sec. 23; Phase 1E-A)",
    "no RSD, bias, light-cone, Alcock-Paczynski or likelihood interpretation",
    "early spectrum is a PROVISIONAL_MODEL_IMPORT (EH98 zero-baryon-oscillation "
    "fit, explicit A_s, n_s, k_pivot, baryon fraction, T_cmb)",
    "radius identification is CONVENTION_DEPENDENT (Phase 1G-A Sec. 6.4)",
    _SCALE_DEPENDENCE_CAVEAT,
)

_LCDM_LIMITATIONS = (
    "flat-LCDM reference evaluated with the same provisional early-spectrum "
    "machinery; used only to form anchored ratios",
    "not a fit to, or a prediction of, any observational amplitude",
)


# --------------------------------------------------------------------------
# Errors
# --------------------------------------------------------------------------

class LagrangianSigmaContractError(ValueError):
    """An explicit input, convention or record contract is violated."""


class BarotropicClosureRefusedError(LagrangianSigmaContractError):
    """The barotropic closure has no linear sigma ([1G-A] Sec. 4.1)."""


class LagrangianSigmaNumericalError(ArithmeticError):
    """A declared convergence budget or machine-precision identity failed."""


# --------------------------------------------------------------------------
# Enums
# --------------------------------------------------------------------------

class GrowthLaw(str, Enum):
    """Mandatory growth law of the smoothed linear mass fluctuation.

    ``VOLUME_AVERAGE_CGI`` requires an explicit ``CleanPerturbationSystem``;
    ``WALL_REGIONAL_EDS_COMMON_TIME`` requires ``closure=NOT_APPLICABLE``.
    The choice is scale-dependent and is analysed in Phase 1G-C; neither
    member is a default.
    """

    VOLUME_AVERAGE_CGI = "volume_average_cgi"
    WALL_REGIONAL_EDS_COMMON_TIME = "wall_regional_eds_common_time"


class EarlyTransferModel(str, Enum):
    """Declared early-universe transfer model ([1G-A] Sec. 6.3)."""

    EH98_ZERO_BARYON_OSCILLATION = "eisenstein_hu_1998_zero_baryon_oscillation"


class LagrangianRadiusConvention(str, Enum):
    """Identification of the smoothing radius ([1G-A] Sec. 6.4).

    All resolved radii are in photon-normalised comoving Mpc.
    """

    EQUAL_LAGRANGIAN_MASS_TO_REFERENCE = "equal_lagrangian_mass_to_reference"
    DRESSED_WALL_COMOVING_LENGTH = "dressed_length_over_h_dressed_wall_comoving"
    BARE_VOLUME_AVERAGE_PROPER_LENGTH = "bare_length_over_h_bare_volume_average_proper"
    EXPLICIT_PHOTON_NORMALISED_RADIUS = "explicit_photon_normalised_comoving_radius"


# --------------------------------------------------------------------------
# Validation helpers
# --------------------------------------------------------------------------

def _real(value, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise LagrangianSigmaContractError(f"{name} must be a real scalar, not {value!r}")
    result = float(value)
    if not math.isfinite(result):
        raise LagrangianSigmaContractError(f"{name} must be finite")
    return result


def _positive(value, name: str) -> float:
    result = _real(value, name)
    if result <= 0.0:
        raise LagrangianSigmaContractError(f"{name} must be positive")
    return result


def _fraction_open(value, name: str) -> float:
    result = _real(value, name)
    if not 0.0 < result < 1.0:
        raise LagrangianSigmaContractError(f"{name} must lie in (0, 1)")
    return result


def _odd_count(value, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise LagrangianSigmaContractError(f"{name} must be an integer")
    result = int(value)
    if result < 3 or result % 2 == 0:
        raise LagrangianSigmaContractError(
            f"{name} must be an odd integer >= 3 (composite Simpson rule on an "
            "even number of intervals)"
        )
    return result


def _nonempty(value, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LagrangianSigmaContractError(f"{name} must be an explicit nonempty string")
    return value


def _is_not_applicable(value) -> bool:
    return isinstance(value, str) and not isinstance(value, Enum) and value == NOT_APPLICABLE


def _readonly(values) -> NDArray[np.float64]:
    out = np.array(values, dtype=np.float64, copy=True)
    out.flags.writeable = False
    return out


def _require_enum(value, enum_type, name: str):
    if not isinstance(value, enum_type):
        raise LagrangianSigmaContractError(
            f"{name} must be an explicit {enum_type.__name__} member, got {value!r}"
        )
    return value


def _is_barotropic(closure) -> bool:
    raw = getattr(closure, "value", closure)
    return isinstance(raw, str) and raw.strip().lower() == "barotropic"


def _check_law_and_closure(growth_law, closure):
    """Validate the (growth law, closure) pair; refuse the barotropic closure."""
    if _is_barotropic(closure):
        raise BarotropicClosureRefusedError(_BAROTROPIC_REFUSAL)
    law = _require_enum(growth_law, GrowthLaw, "growth_law")
    if law is GrowthLaw.VOLUME_AVERAGE_CGI:
        if not isinstance(closure, CleanPerturbationSystem):
            raise LagrangianSigmaContractError(
                "GrowthLaw.VOLUME_AVERAGE_CGI requires an explicit "
                "CleanPerturbationSystem closure (COMOVING or MESZAROS)"
            )
    elif not _is_not_applicable(closure):
        raise LagrangianSigmaContractError(
            "GrowthLaw.WALL_REGIONAL_EDS_COMMON_TIME has no perturbation "
            "closure; pass closure=NOT_APPLICABLE explicitly"
        )
    return law, closure


def _caveat(growth_law: GrowthLaw, closure) -> str:
    key = f"{growth_law.value}:{getattr(closure, 'value', closure)}"
    return _CAVEATS[key]


def _check_statuses(record, expected: dict) -> None:
    for name, value in expected.items():
        if getattr(record, name) != value:
            raise LagrangianSigmaContractError(
                f"{name} must equal {value!r}; status tokens are not relabelled"
            )


# --------------------------------------------------------------------------
# Inputs and numerical configurations (no defaults)
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class TimescapeTrackerInput:
    """The two tracker parameters with explicit physical units.

    ``fv0`` is the present void fraction and ``H0_dressed_km_s_Mpc`` the
    dressed Hubble constant; H_D0 is always derived from it ([GM] text
    p. 25; [W09] (B8)-(B9)), never inserted.  ``label``/``source`` record
    provenance.
    """

    label: str
    fv0: float
    H0_dressed_km_s_Mpc: float
    source: str

    def __post_init__(self) -> None:
        _nonempty(self.label, "label")
        _nonempty(self.source, "source")
        object.__setattr__(self, "fv0", _fraction_open(self.fv0, "fv0"))
        object.__setattr__(
            self, "H0_dressed_km_s_Mpc",
            _positive(self.H0_dressed_km_s_Mpc, "H0_dressed_km_s_Mpc"),
        )

    @classmethod
    def from_reference_preset(cls, *, preset: ReferencePreset) -> "TimescapeTrackerInput":
        """Build from a frozen ``presets.ReferencePreset`` (explicitly passed)."""
        if not isinstance(preset, ReferencePreset):
            raise LagrangianSigmaContractError("preset must be a ReferencePreset")
        return cls(label=preset.name, fv0=preset.fv0,
                   H0_dressed_km_s_Mpc=preset.H0_dressed_km_s_Mpc,
                   source=preset.source)

    def dimensionless_params(self) -> TrackerParams:
        """Tracker parameters in units where the dressed H0 equals 1."""
        return TrackerParams.from_dressed_H0(fv0=self.fv0, H0=1.0)

    def km_s_Mpc_params(self) -> TrackerParams:
        """Tracker parameters with rates in km/s/Mpc (time unit Mpc s/km)."""
        return TrackerParams.from_dressed_H0(fv0=self.fv0, H0=self.H0_dressed_km_s_Mpc)

    def to_metadata(self) -> dict:
        return {"label": self.label, "fv0": self.fv0,
                "H0_dressed_km_s_Mpc": self.H0_dressed_km_s_Mpc, "source": self.source}


@dataclass(frozen=True, kw_only=True)
class EarlySpectrumImport:
    """Explicit early-universe spectrum import ([1G-A] Sec. 6.3).

    ``A_s`` (dimensionless), ``n_s`` and ``k_pivot_per_Mpc`` define the
    curvature spectrum ``Delta^2_zeta = A_s (k/k_p)^(n_s-1)``;
    ``baryon_fraction`` is ``omega_b/omega_m`` in [0, 1); ``T_cmb_K`` is the
    photon temperature today that defines the photon normalisation.
    ``import_status`` must be passed as ``PROVISIONAL_MODEL_IMPORT``: the
    caller acknowledges that the spectrum is not a Timescape derivation.
    """

    A_s: float
    n_s: float
    k_pivot_per_Mpc: float
    baryon_fraction: float
    T_cmb_K: float
    transfer_model: EarlyTransferModel
    provenance: str
    import_status: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "A_s", _positive(self.A_s, "A_s"))
        object.__setattr__(self, "n_s", _real(self.n_s, "n_s"))
        object.__setattr__(self, "k_pivot_per_Mpc",
                           _positive(self.k_pivot_per_Mpc, "k_pivot_per_Mpc"))
        f_b = _real(self.baryon_fraction, "baryon_fraction")
        if not 0.0 <= f_b < 1.0:
            raise LagrangianSigmaContractError("baryon_fraction must lie in [0, 1)")
        object.__setattr__(self, "baryon_fraction", f_b)
        object.__setattr__(self, "T_cmb_K", _positive(self.T_cmb_K, "T_cmb_K"))
        _require_enum(self.transfer_model, EarlyTransferModel, "transfer_model")
        _nonempty(self.provenance, "provenance")
        if self.import_status != EARLY_SPECTRUM_IMPORT_STATUS:
            raise LagrangianSigmaContractError(
                "import_status must be passed explicitly as PROVISIONAL_MODEL_IMPORT"
            )

    def to_metadata(self) -> dict:
        return {"A_s": self.A_s, "n_s": self.n_s, "k_pivot_per_Mpc": self.k_pivot_per_Mpc,
                "baryon_fraction": self.baryon_fraction, "T_cmb_K": self.T_cmb_K,
                "transfer_model": self.transfer_model.value,
                "provenance": self.provenance, "import_status": self.import_status}


_RADIUS_FIELDS = ("length_h_inverse_Mpc", "reference_omega_m",
                  "reference_radius_Mpc", "explicit_radius_Mpc")
_RADIUS_REQUIRED = {
    LagrangianRadiusConvention.EQUAL_LAGRANGIAN_MASS_TO_REFERENCE:
        ("reference_omega_m", "reference_radius_Mpc"),
    LagrangianRadiusConvention.DRESSED_WALL_COMOVING_LENGTH: ("length_h_inverse_Mpc",),
    LagrangianRadiusConvention.BARE_VOLUME_AVERAGE_PROPER_LENGTH: ("length_h_inverse_Mpc",),
    LagrangianRadiusConvention.EXPLICIT_PHOTON_NORMALISED_RADIUS: ("explicit_radius_Mpc",),
}


@dataclass(frozen=True, kw_only=True)
class LagrangianRadiusSpec:
    """Explicit radius convention; inapplicable fields are ``NOT_APPLICABLE``.

    * equal mass: ``reference_omega_m`` (per-photon omega_m of the reference
      model) and ``reference_radius_Mpc``;
    * dressed / bare: ``length_h_inverse_Mpc`` (the length L in h^-1 Mpc;
      there is no hidden value);
    * explicit: ``explicit_radius_Mpc``.
    """

    convention: LagrangianRadiusConvention
    length_h_inverse_Mpc: float | str
    reference_omega_m: float | str
    reference_radius_Mpc: float | str
    explicit_radius_Mpc: float | str

    def __post_init__(self) -> None:
        convention = _require_enum(self.convention, LagrangianRadiusConvention, "convention")
        required = _RADIUS_REQUIRED[convention]
        for name in _RADIUS_FIELDS:
            value = getattr(self, name)
            if name in required:
                if _is_not_applicable(value):
                    raise LagrangianSigmaContractError(
                        f"{name} is required by {convention.value}"
                    )
                object.__setattr__(self, name, _positive(value, name))
            elif not _is_not_applicable(value):
                raise LagrangianSigmaContractError(
                    f"{name} does not apply to {convention.value}; pass NOT_APPLICABLE"
                )

    def to_metadata(self) -> dict:
        return {"convention": self.convention.value,
                **{name: getattr(self, name) for name in _RADIUS_FIELDS}}


@dataclass(frozen=True, kw_only=True)
class VolumeAverageGrowthNumerics:
    """Numerics of Eq. (2) for ``GrowthLaw.VOLUME_AVERAGE_CGI``.

    The integral is a composite Simpson rule in ``ln t`` on a geometric grid
    of ``grid_points`` from ``early_time_fraction * t0`` to ``t0``.  Two
    comparison evaluations bound the error and fail closed:
    ``comparison_grid_points`` (grid refinement; absolute change of ln g at
    most ``grid_refinement_tolerance``) and ``comparison_early_time_fraction``
    (a later start; change of ln g at most ``early_limit_tolerance``; the
    truncated early piece is O(f_v(t_e)), linear in t_e).  ``growing_mode``
    configures ``regular_growing_mode_coefficients``.  No field has a default.
    """

    grid_points: int
    comparison_grid_points: int
    early_time_fraction: float
    comparison_early_time_fraction: float
    grid_refinement_tolerance: float
    early_limit_tolerance: float
    growing_mode: GrowingModeConfig

    def __post_init__(self) -> None:
        n = _odd_count(self.grid_points, "grid_points")
        m = _odd_count(self.comparison_grid_points, "comparison_grid_points")
        if m >= n:
            raise LagrangianSigmaContractError(
                "comparison_grid_points must be smaller than grid_points"
            )
        te = _fraction_open(self.early_time_fraction, "early_time_fraction")
        tc = _fraction_open(self.comparison_early_time_fraction,
                            "comparison_early_time_fraction")
        if not tc > te:
            raise LagrangianSigmaContractError(
                "comparison_early_time_fraction must exceed early_time_fraction"
            )
        _positive(self.grid_refinement_tolerance, "grid_refinement_tolerance")
        _positive(self.early_limit_tolerance, "early_limit_tolerance")
        if not isinstance(self.growing_mode, GrowingModeConfig):
            raise LagrangianSigmaContractError("growing_mode must be a GrowingModeConfig")

    def to_metadata(self) -> dict:
        return {"grid_points": self.grid_points,
                "comparison_grid_points": self.comparison_grid_points,
                "early_time_fraction": self.early_time_fraction,
                "comparison_early_time_fraction": self.comparison_early_time_fraction,
                "grid_refinement_tolerance": self.grid_refinement_tolerance,
                "early_limit_tolerance": self.early_limit_tolerance,
                "growing_mode": self.growing_mode.to_metadata(),
                "quadrature": "composite Simpson in ln t (scipy.integrate.simpson)"}


@dataclass(frozen=True, kw_only=True)
class WallRegionalGrowthChecks:
    """Machine-precision identity checks for ``WALL_REGIONAL_EDS_COMMON_TIME``.

    ``identity_tolerance`` bounds, relatively: the closed form of Eq. (3)
    against the tracker functions; the constancy of ``(1-f_v)^(1/3) a_D /
    t^(2/3)`` and of ``6 pi G t^2 <rho>_D/(1-f_v)`` on a geometric grid of
    ``check_grid_points`` over ``[early_time_fraction t0, t0]``; and the exact
    finite-t_e photon-normalisation identity at ``early_time_fraction t0``.
    """

    identity_tolerance: float
    check_grid_points: int
    early_time_fraction: float

    def __post_init__(self) -> None:
        _positive(self.identity_tolerance, "identity_tolerance")
        _odd_count(self.check_grid_points, "check_grid_points")
        _fraction_open(self.early_time_fraction, "early_time_fraction")

    def to_metadata(self) -> dict:
        return {"identity_tolerance": self.identity_tolerance,
                "check_grid_points": self.check_grid_points,
                "early_time_fraction": self.early_time_fraction}


@dataclass(frozen=True, kw_only=True)
class LagrangianSigmaQuadrature:
    """Quadrature of Eq. (1) on a uniform ``ln k`` grid (k in Mpc^-1).

    The composite Simpson rule on ``grid_points`` is compared with
    ``comparison_grid_points`` (relative change at most
    ``self_convergence_tolerance``).  The truncation check bounds the
    integrand envelope at both ends, ``Delta^2(k) min(1, 3/x^2 + 3/x^3)^2``
    with ``x = kR`` (``|W(x)| <= 3(1+x)/x^3``), relative to the integrand
    maximum, by ``truncation_tolerance``.  Both fail closed.
    """

    k_min_per_Mpc: float
    k_max_per_Mpc: float
    grid_points: int
    comparison_grid_points: int
    self_convergence_tolerance: float
    truncation_tolerance: float

    def __post_init__(self) -> None:
        kmin = _positive(self.k_min_per_Mpc, "k_min_per_Mpc")
        kmax = _positive(self.k_max_per_Mpc, "k_max_per_Mpc")
        if not kmax > kmin:
            raise LagrangianSigmaContractError("k_max_per_Mpc must exceed k_min_per_Mpc")
        n = _odd_count(self.grid_points, "grid_points")
        m = _odd_count(self.comparison_grid_points, "comparison_grid_points")
        if m >= n:
            raise LagrangianSigmaContractError(
                "comparison_grid_points must be smaller than grid_points"
            )
        _positive(self.self_convergence_tolerance, "self_convergence_tolerance")
        _positive(self.truncation_tolerance, "truncation_tolerance")

    def to_metadata(self) -> dict:
        return {"k_min_per_Mpc": self.k_min_per_Mpc, "k_max_per_Mpc": self.k_max_per_Mpc,
                "grid_points": self.grid_points,
                "comparison_grid_points": self.comparison_grid_points,
                "self_convergence_tolerance": self.self_convergence_tolerance,
                "truncation_tolerance": self.truncation_tolerance,
                "quadrature": "composite Simpson in ln k (scipy.integrate.simpson)"}


# Named, immutable reference configurations (passed explicitly; not function
# defaults).  They reproduce the Phase 1G-A evidence script: growth grid
# 16001 vs 8001 points, t_e/t0 = 1e-6 vs 1e-5, budgets 1e-7 / 1e-4; k in
# [1e-6, 3e2] Mpc^-1 with 8001 vs 4001 points, budget 1e-6.
VOLUME_AVERAGE_GROWTH_REFERENCE_NUMERICS = VolumeAverageGrowthNumerics(
    grid_points=16001,
    comparison_grid_points=8001,
    early_time_fraction=1e-6,
    comparison_early_time_fraction=1e-5,
    grid_refinement_tolerance=1e-7,
    early_limit_tolerance=1e-4,
    growing_mode=REGULAR_GROWING_MODE_REFERENCE_CONFIG,
)

WALL_REGIONAL_GROWTH_REFERENCE_CHECKS = WallRegionalGrowthChecks(
    identity_tolerance=1e-13,
    check_grid_points=2001,
    early_time_fraction=1e-8,
)

LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE = LagrangianSigmaQuadrature(
    k_min_per_Mpc=1e-6,
    k_max_per_Mpc=3e2,
    grid_points=8001,
    comparison_grid_points=4001,
    self_convergence_tolerance=1e-6,
    truncation_tolerance=1e-8,
)


# --------------------------------------------------------------------------
# External formulas (PROVISIONAL_MODEL_IMPORT)
# --------------------------------------------------------------------------

def top_hat_window(*, x: ArrayLike) -> NDArray[np.float64]:
    """Spherical top-hat window ``W(x) = 3 (sin x - x cos x)/x^3`` (1D-A D5).

    For ``|x| < TOP_HAT_SERIES_THRESHOLD`` the Maclaurin series
    ``1 - x^2/10 + x^4/280 - x^6/15120 + x^8/1330560`` is used (derived from
    ``sin x - x cos x = sum_{n>=1} (-1)^(n+1) 2n x^(2n+1)/(2n+1)!``).
    ``x`` must be finite and real; ``W(0) = 1``.  Returns a read-only array.
    """
    arr = np.asarray(x, dtype=np.float64)
    if not np.all(np.isfinite(arr)):
        raise LagrangianSigmaContractError("x must be finite")
    out = np.empty_like(arr)
    small = np.abs(arr) < TOP_HAT_SERIES_THRESHOLD
    xs = arr[small]
    x2 = xs * xs
    out[small] = 1.0 + x2 * (-1.0 / 10.0 + x2 * (1.0 / 280.0 + x2 * (
        -1.0 / 15120.0 + x2 / 1330560.0)))
    xl = arr[~small]
    out[~small] = 3.0 * (np.sin(xl) - xl * np.cos(xl)) / xl ** 3
    return _readonly(out)


def eh98_zero_baryon_transfer(
    *, k_per_Mpc: ArrayLike, omega_m: float, baryon_fraction: float, T_cmb_K: float,
) -> NDArray[np.float64]:
    """Eisenstein & Hu (1998) zero-baryon-oscillation transfer function.

    astro-ph/9709112 ([EH98]), with k in Mpc^-1, ``omega_m = Omega_0 h^2``,
    ``omega_b = f_b omega_m`` and ``Theta_2.7 = T_cmb/2.7 K``:

    * Eq. (26): ``s = 44.5 ln(9.83/omega_m) / sqrt(1 + 10 omega_b^(3/4))`` Mpc;
    * Eq. (31): ``alpha_Gamma = 1 - 0.328 ln(431 omega_m) f_b
      + 0.38 ln(22.3 omega_m) f_b^2``;
    * Eq. (30): ``Gamma_eff h = omega_m [alpha_Gamma + (1 - alpha_Gamma)/
      (1 + (0.43 k s)^4)]``;
    * Eq. (28): ``q = k Theta_2.7^2 / (Gamma_eff h)``;
    * Eq. (29): ``T = L0/(L0 + C0 q^2)``, ``L0 = ln(2e + 1.8 q)``,
      ``C0 = 14.2 + 731/(1 + 62.5 q)``.

    Depends only on the physical densities.  PROVISIONAL_MODEL_IMPORT
    ([1G-A] Sec. 6.3); read-only output.
    """
    k = np.asarray(k_per_Mpc, dtype=np.float64)
    if not np.all(np.isfinite(k)) or np.any(k <= 0.0):
        raise LagrangianSigmaContractError("k_per_Mpc must be finite and positive")
    om = _positive(omega_m, "omega_m")
    f_b = _real(baryon_fraction, "baryon_fraction")
    if not 0.0 <= f_b < 1.0:
        raise LagrangianSigmaContractError("baryon_fraction must lie in [0, 1)")
    theta = _positive(T_cmb_K, "T_cmb_K") / 2.7
    omega_b = f_b * om
    s = 44.5 * math.log(9.83 / om) / math.sqrt(1.0 + 10.0 * omega_b ** 0.75)   # (26)
    alpha_g = (1.0 - 0.328 * math.log(431.0 * om) * f_b
               + 0.38 * math.log(22.3 * om) * f_b ** 2)                        # (31)
    gamma_eff_h = om * (alpha_g + (1.0 - alpha_g) / (1.0 + (0.43 * k * s) ** 4))  # (30)
    q = k * theta ** 2 / gamma_eff_h                                           # (28)
    L0 = np.log(2.0 * math.e + 1.8 * q)                                        # (29)
    C0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return _readonly(L0 / (L0 + C0 * q ** 2))


def matter_era_linear_amplitude(
    *,
    k_per_Mpc: ArrayLike,
    early_spectrum: EarlySpectrumImport,
    omega_m: float,
    growth_today_photon_normalised: float,
) -> NDArray[np.float64]:
    """Dimensionless linear density amplitude today, Eq. (5) ([1G-A] Sec. 6.3).

    ``Delta^2(k) = (4/25) A_s (k/k_p)^(n_s-1) (k c/100)^4 T^2(k) D0^2 /
    omega_m^2`` with k in Mpc^-1, ``c/100`` in Mpc (the Hubble length at
    100 km/s/Mpc), T from :func:`eh98_zero_baryon_transfer` and ``D0`` the
    growth today normalised to ``D/a_photon -> 1`` in the matter era.  The
    factor 4/25 follows from the matter-era Poisson equation with
    ``Phi = -(3/5) zeta`` and ``(aH)^2 = H100^2 omega_m / a``.
    """
    if not isinstance(early_spectrum, EarlySpectrumImport):
        raise LagrangianSigmaContractError("early_spectrum must be an EarlySpectrumImport")
    if early_spectrum.transfer_model is not EarlyTransferModel.EH98_ZERO_BARYON_OSCILLATION:
        raise LagrangianSigmaContractError("unsupported transfer model")  # pragma: no cover
    om = _positive(omega_m, "omega_m")
    growth = _positive(growth_today_photon_normalised, "growth_today_photon_normalised")
    k = np.asarray(k_per_Mpc, dtype=np.float64)
    transfer = eh98_zero_baryon_transfer(
        k_per_Mpc=k, omega_m=om, baryon_fraction=early_spectrum.baryon_fraction,
        T_cmb_K=early_spectrum.T_cmb_K)
    hubble_length_100 = SPEED_OF_LIGHT_KM_S / 100.0          # Mpc
    amplitude = (4.0 / 25.0) * early_spectrum.A_s * (
        k / early_spectrum.k_pivot_per_Mpc) ** (early_spectrum.n_s - 1.0)
    return _readonly(amplitude * (k * hubble_length_100) ** 4 * transfer ** 2
                     * growth ** 2 / om ** 2)


@dataclass(frozen=True)
class _QuadratureOutcome:
    sigma_unit_growth: float
    sigma_unit_growth_comparison: float
    relative_change: float
    truncation_envelope_fraction: float


def _sigma_unit_growth(n: int, *, radius_Mpc: float, omega_m: float,
                       early_spectrum: EarlySpectrumImport,
                       quadrature: LagrangianSigmaQuadrature) -> tuple[float, float]:
    lnk = np.linspace(math.log(quadrature.k_min_per_Mpc),
                      math.log(quadrature.k_max_per_Mpc), n)
    k = np.exp(lnk)
    amplitude = matter_era_linear_amplitude(
        k_per_Mpc=k, early_spectrum=early_spectrum, omega_m=omega_m,
        growth_today_photon_normalised=1.0)
    integrand = amplitude * top_hat_window(x=k * radius_Mpc) ** 2
    x_ends = np.array([k[0], k[-1]]) * radius_Mpc
    envelope = np.minimum(1.0, 3.0 / x_ends ** 2 + 3.0 / x_ends ** 3) ** 2
    edge = float(np.max(np.array([amplitude[0], amplitude[-1]]) * envelope))
    return math.sqrt(float(simpson(integrand, x=lnk))), edge / float(np.max(integrand))


def _quadrature(*, radius_Mpc: float, omega_m: float, early_spectrum: EarlySpectrumImport,
                quadrature: LagrangianSigmaQuadrature) -> _QuadratureOutcome:
    """Eq. (1) at unit growth, with fail-closed convergence and truncation checks."""
    kwargs = dict(radius_Mpc=radius_Mpc, omega_m=omega_m,
                  early_spectrum=early_spectrum, quadrature=quadrature)
    fine, edge = _sigma_unit_growth(quadrature.grid_points, **kwargs)
    coarse, _ = _sigma_unit_growth(quadrature.comparison_grid_points, **kwargs)
    change = abs(fine / coarse - 1.0)
    if not change <= quadrature.self_convergence_tolerance:
        raise LagrangianSigmaNumericalError(
            f"sigma quadrature not converged: relative change {change:.3e} exceeds "
            f"{quadrature.self_convergence_tolerance:.3e}"
        )
    if not edge <= quadrature.truncation_tolerance:
        raise LagrangianSigmaNumericalError(
            f"k range truncates the integrand: end envelope fraction {edge:.3e} "
            f"exceeds {quadrature.truncation_tolerance:.3e}"
        )
    return _QuadratureOutcome(fine, coarse, change, edge)


# --------------------------------------------------------------------------
# Growth factor
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class TimescapeGrowthFactor:
    """Growth today of the smoothed linear fluctuation (Eqs. (2)/(3)).

    ``growth_relative_to_volume_average_eds`` is g (``g_TS`` or
    ``(1-f_v0)^(1/3)``); ``growth_today_photon_normalised`` is
    ``gamma_w0 g``, the growth today of a mode with ``D/a_photon -> 1``
    early ([1G-A] Sec. 5.1).  ``diagnostics`` holds the convergence budget
    (volume-average law) or identity residuals (wall law), each checked
    against the explicit numerics before the record is built.
    """

    growth_law: GrowthLaw
    closure: CleanPerturbationSystem | str
    evidence_class: str
    fv0: float
    gamma_w0: float
    log_growth_relative_to_volume_average_eds: float
    growth_relative_to_volume_average_eds: float
    growth_today_photon_normalised: float
    numerics: VolumeAverageGrowthNumerics | WallRegionalGrowthChecks
    diagnostics: tuple[tuple[str, float], ...]
    G: float

    def __post_init__(self) -> None:
        law, _ = _check_law_and_closure(self.growth_law, self.closure)
        expected_class = (VOLUME_AVERAGE_CGI_EVIDENCE_CLASS
                          if law is GrowthLaw.VOLUME_AVERAGE_CGI
                          else WALL_REGIONAL_EVIDENCE_CLASS)
        if self.evidence_class != expected_class:
            raise LagrangianSigmaContractError("evidence_class is inconsistent with growth_law")
        expected_numerics = (VolumeAverageGrowthNumerics
                             if law is GrowthLaw.VOLUME_AVERAGE_CGI
                             else WallRegionalGrowthChecks)
        if not isinstance(self.numerics, expected_numerics):
            raise LagrangianSigmaContractError(
                f"{law.value} requires {expected_numerics.__name__} numerics"
            )
        for name in ("fv0", "gamma_w0", "log_growth_relative_to_volume_average_eds",
                     "growth_relative_to_volume_average_eds",
                     "growth_today_photon_normalised", "G"):
            _real(getattr(self, name), name)
        _positive(self.growth_relative_to_volume_average_eds,
                  "growth_relative_to_volume_average_eds")
        g = self.growth_relative_to_volume_average_eds
        if not math.isclose(g, math.exp(self.log_growth_relative_to_volume_average_eds),
                            rel_tol=4.0 * np.finfo(float).eps, abs_tol=0.0):
            raise LagrangianSigmaContractError("growth and its logarithm are inconsistent")
        if self.growth_today_photon_normalised != self.gamma_w0 * g:
            raise LagrangianSigmaContractError(
                "growth_today_photon_normalised must equal gamma_w0 * g"
            )
        if not isinstance(self.diagnostics, tuple) or not all(
            isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str)
            and isinstance(item[1], float) and math.isfinite(item[1])
            for item in self.diagnostics
        ):
            raise LagrangianSigmaContractError(
                "diagnostics must be a tuple of (name, finite float) pairs"
            )

    def diagnostic(self, name: str) -> float:
        return dict(self.diagnostics)[name]

    def to_json_dict(self) -> dict:
        return {
            "growth_law": self.growth_law.value,
            "closure": getattr(self.closure, "value", self.closure),
            "evidence_class": self.evidence_class,
            "fv0": self.fv0,
            "gamma_w0": self.gamma_w0,
            "log_growth_relative_to_volume_average_eds":
                self.log_growth_relative_to_volume_average_eds,
            "growth_relative_to_volume_average_eds": self.growth_relative_to_volume_average_eds,
            "growth_today_photon_normalised": self.growth_today_photon_normalised,
            "numerics": self.numerics.to_metadata(),
            "diagnostics": dict(self.diagnostics),
            "G": self.G,
        }


def _cgi_log_growth(params: TrackerParams, system: CleanPerturbationSystem,
                    fraction: float, n: int, config: GrowingModeConfig, G: float):
    """Composite Simpson evaluation of Eq. (2) from ``fraction * t0`` to t0."""
    ts = np.geomspace(fraction * params.t0, params.t0, n)
    coeff = regular_growing_mode_coefficients(
        params, system=system, times=ts, config=config, G=G)
    excess = coeff.log_rate - ts * np.asarray(bg.Theta(ts, params)) / 3.0
    return float(simpson(excess, x=np.log(ts))), coeff


def _volume_average_growth(params, closure, numerics: VolumeAverageGrowthNumerics, G):
    te, tc = numerics.early_time_fraction, numerics.comparison_early_time_fraction
    ln_g, coeff = _cgi_log_growth(params, closure, te, numerics.grid_points,
                                  numerics.growing_mode, G)
    ln_g_grid, _ = _cgi_log_growth(params, closure, te, numerics.comparison_grid_points,
                                   numerics.growing_mode, G)
    ln_g_early, _ = _cgi_log_growth(params, closure, tc, numerics.grid_points,
                                    numerics.growing_mode, G)
    grid_change = abs(ln_g - ln_g_grid)
    early_change = abs(ln_g - ln_g_early)
    if not grid_change <= numerics.grid_refinement_tolerance:
        raise LagrangianSigmaNumericalError(
            f"growth grid refinement change {grid_change:.3e} exceeds "
            f"{numerics.grid_refinement_tolerance:.3e}"
        )
    if not early_change <= numerics.early_limit_tolerance:
        raise LagrangianSigmaNumericalError(
            f"growth early-limit change {early_change:.3e} exceeds "
            f"{numerics.early_limit_tolerance:.3e}"
        )
    diagnostics = (
        ("log_growth_grid_refinement_change", float(grid_change)),
        ("log_growth_early_limit_change", float(early_change)),
        # The omitted piece integral_0^{t_e} is c f_v(t_e) to first order
        # (c = -13/20 comoving, -3/4 Meszaros), linear in t_e; the two starts
        # give the estimate of (computed ln g) - (t_e -> 0 limit).  Recorded,
        # never applied, so the reference numbers stay those of [1G-A].
        ("log_growth_early_limit_linear_bias_estimate",
         float((ln_g_early - ln_g) * te / (tc - te))),
        ("growing_mode_start_time_over_t0", float(coeff.start_time / params.t0)),
        ("growing_mode_eds_limit_deviation", float(coeff.eds_limit_deviation)),
        ("growing_mode_nfev", float(coeff.nfev)),
    )
    return ln_g, diagnostics


def _relative_spread(values: NDArray[np.float64]) -> float:
    return float(np.max(values) / np.min(values) - 1.0)


def _wall_regional_growth(params: TrackerParams, checks: WallRegionalGrowthChecks, G: float):
    """Eq. (3) with its machine-precision identities ([1G-A] Secs. 5.3, 8)."""
    t0 = params.t0
    fv0 = params.fv0
    closed_form = 0.5 * (2.0 + fv0) * (1.0 - fv0) ** (1.0 / 3.0)
    from_tracker = float(bg.gamma_w(t0, params)) * float(np.cbrt(1.0 - bg.fv(t0, params)))
    ts = np.geomspace(checks.early_time_fraction * t0, t0, checks.check_grid_points)
    f = np.asarray(bg.fv(ts, params))
    regional_scale = np.cbrt(1.0 - f) * np.asarray(bg.a_D(ts, params)) / ts ** (2.0 / 3.0)
    regional_density = 6.0 * math.pi * G * ts ** 2 * np.asarray(bg.rho_d(ts, params, G)) / (1.0 - f)
    t_e = ts[0]
    uncorrected_limit = (t0 / t_e) ** (2.0 / 3.0) / (1.0 + float(bg.redshift(t_e, params)))
    # Exact for every t_e: (t0/t_e)^(2/3)/(1+z_e) = gamma_w0 (1-f_v0)^(1/3) /
    # [gamma_w(t_e) (1-f_v(t_e))^(1/3)], from 1+z = gamma_w/a_D ([GM] (5.4)).
    corrected_limit = uncorrected_limit * float(bg.gamma_w(t_e, params)) * float(
        np.cbrt(1.0 - bg.fv(t_e, params)))
    residuals = {
        "closed_form_vs_tracker_rel": abs(from_tracker / closed_form - 1.0),
        "regional_scale_over_t23_rel_spread": _relative_spread(regional_scale),
        "regional_density_eds_max_rel": float(np.max(np.abs(regional_density - 1.0))),
        "finite_te_identity_rel": abs(corrected_limit / closed_form - 1.0),
    }
    for name, value in residuals.items():
        if not value <= checks.identity_tolerance:
            raise LagrangianSigmaNumericalError(
                f"wall-regional identity {name} = {value:.3e} exceeds "
                f"{checks.identity_tolerance:.3e}"
            )
    diagnostics = tuple((name, float(value)) for name, value in residuals.items()) + (
        ("uncorrected_finite_te_limit_rel", float(uncorrected_limit / closed_form - 1.0)),
        ("fv_at_te", float(bg.fv(t_e, params))),
    )
    return math.log((1.0 - fv0) ** (1.0 / 3.0)), diagnostics


def timescape_growth_factor(
    *,
    params: TrackerParams,
    growth_law: GrowthLaw,
    closure: CleanPerturbationSystem | str,
    numerics: VolumeAverageGrowthNumerics | WallRegionalGrowthChecks,
    G: float,
) -> TimescapeGrowthFactor:
    """Growth today relative to photon-normalised EdS ([1G-A] Secs. 5, 8).

    ``VOLUME_AVERAGE_CGI``: Eq. (2) on the regular growing mode of the
    selected clean closure ([GM] Eqs. (4.21)-(4.23) or (4.27)).
    ``WALL_REGIONAL_EDS_COMMON_TIME``: Eq. (3) (``closure=NOT_APPLICABLE``).
    In both, ``gamma_w0 = 1 + f_v0/2`` ([GM] Eq. (5.4)).  ``params`` may use
    any time unit: g is dimensionless and depends on f_v0 only (the tracker
    is self-similar in ``H_D0 t``); ``G`` cancels in ``t^2 4 pi G rho``.
    The barotropic closure is refused ([1G-A] Sec. 4.1).
    """
    law, closure = _check_law_and_closure(growth_law, closure)
    if not isinstance(params, TrackerParams):
        raise LagrangianSigmaContractError("params must be TrackerParams")
    G = _positive(G, "G")
    if law is GrowthLaw.VOLUME_AVERAGE_CGI:
        if not isinstance(numerics, VolumeAverageGrowthNumerics):
            raise LagrangianSigmaContractError(
                "VOLUME_AVERAGE_CGI requires VolumeAverageGrowthNumerics")
        ln_g, diagnostics = _volume_average_growth(params, closure, numerics, G)
        evidence = VOLUME_AVERAGE_CGI_EVIDENCE_CLASS
    else:
        if not isinstance(numerics, WallRegionalGrowthChecks):
            raise LagrangianSigmaContractError(
                "WALL_REGIONAL_EDS_COMMON_TIME requires WallRegionalGrowthChecks")
        ln_g, diagnostics = _wall_regional_growth(params, numerics, G)
        evidence = WALL_REGIONAL_EVIDENCE_CLASS
    gamma0 = float(bg.gamma_w(params.t0, params))
    g = math.exp(ln_g)
    return TimescapeGrowthFactor(
        growth_law=law, closure=closure, evidence_class=evidence, fv0=params.fv0,
        gamma_w0=gamma0, log_growth_relative_to_volume_average_eds=ln_g,
        growth_relative_to_volume_average_eds=g,
        growth_today_photon_normalised=gamma0 * g, numerics=numerics,
        diagnostics=diagnostics, G=G)


# --------------------------------------------------------------------------
# Early matter density per photon
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class EarlyMatterDensityPerPhoton:
    """Eq. (4): per-photon early matter density in units of rho_crit(100).

    ``omega_m_per_photon`` is the numerical ``<rho>_D0 gamma_w0^3 /
    rho_crit(100)``; ``closed_form`` is ``(1/2)(1-f_v0)(2+f_v0)(H_D0/100)^2``;
    their relative residual is bounded by ``identity_tolerance``.
    ``omega_m_bare`` is ``<rho>_D0/rho_crit(100)`` and ``bare_Omega_M0`` the
    bare density parameter ``4(1-f_v0)/(2+f_v0)^2`` ([W09] (B3)).
    """

    background: TimescapeTrackerInput
    HD0_bare_km_s_Mpc: float
    gamma_w0: float
    bare_Omega_M0: float
    omega_m_bare: float
    omega_m_per_photon: float
    closed_form: float
    identity_relative_residual: float
    identity_tolerance: float
    G: float

    def __post_init__(self) -> None:
        if not isinstance(self.background, TimescapeTrackerInput):
            raise LagrangianSigmaContractError("background must be TimescapeTrackerInput")
        for name in ("HD0_bare_km_s_Mpc", "gamma_w0", "bare_Omega_M0", "omega_m_bare",
                     "omega_m_per_photon", "closed_form", "identity_tolerance", "G"):
            _positive(getattr(self, name), name)
        if not self.identity_relative_residual <= self.identity_tolerance:
            raise LagrangianSigmaNumericalError(
                "per-photon density identity residual exceeds its tolerance"
            )

    @property
    def h_dressed(self) -> float:
        return self.background.H0_dressed_km_s_Mpc / 100.0

    @property
    def h_bare(self) -> float:
        return self.HD0_bare_km_s_Mpc / 100.0

    def to_json_dict(self) -> dict:
        return {"background": self.background.to_metadata(),
                "HD0_bare_km_s_Mpc": self.HD0_bare_km_s_Mpc, "gamma_w0": self.gamma_w0,
                "bare_Omega_M0": self.bare_Omega_M0, "omega_m_bare": self.omega_m_bare,
                "omega_m_per_photon": self.omega_m_per_photon,
                "closed_form": self.closed_form,
                "identity_relative_residual": self.identity_relative_residual,
                "identity_tolerance": self.identity_tolerance, "G": self.G}


def early_matter_density_per_photon(
    *, background: TimescapeTrackerInput, identity_tolerance: float, G: float,
) -> EarlyMatterDensityPerPhoton:
    """Evaluate Eq. (4) ([1G-A] Sec. 6.2) and check its closed form.

    Rates are expressed in km/s/Mpc (time unit Mpc s/km), so
    ``rho_crit(100) = 3 x 100^2/(8 pi G)`` with the same ``G`` as
    ``<rho>_D0`` ([GM] text p. 25, via ``background.rho_d``); G cancels.
    ``gamma_w0 = 1 + f_v0/2`` ([GM] Eq. (5.4)); H_D0 from the dressed H0
    ([GM] p. 25).  Fails closed if the relative residual exceeds
    ``identity_tolerance``.
    """
    if not isinstance(background, TimescapeTrackerInput):
        raise LagrangianSigmaContractError("background must be TimescapeTrackerInput")
    tol = _positive(identity_tolerance, "identity_tolerance")
    G = _positive(G, "G")
    p = background.km_s_Mpc_params()
    rho_crit_100 = 3.0 * 100.0 ** 2 / (8.0 * math.pi * G)
    gamma0 = float(bg.gamma_w(p.t0, p))
    rho0 = float(bg.rho_d(p.t0, p, G))
    numeric = rho0 * gamma0 ** 3 / rho_crit_100
    closed = 0.5 * (1.0 - p.fv0) * (2.0 + p.fv0) * (p.HD0 / 100.0) ** 2
    residual = abs(numeric / closed - 1.0)
    if not residual <= tol:
        raise LagrangianSigmaNumericalError(
            f"per-photon density identity residual {residual:.3e} exceeds {tol:.3e}"
        )
    return EarlyMatterDensityPerPhoton(
        background=background, HD0_bare_km_s_Mpc=p.HD0, gamma_w0=gamma0,
        bare_Omega_M0=float(bg.Omega_m(p.t0, p)), omega_m_bare=rho0 / rho_crit_100,
        omega_m_per_photon=numeric, closed_form=closed,
        identity_relative_residual=residual, identity_tolerance=tol, G=G)


# --------------------------------------------------------------------------
# Radius
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class ResolvedLagrangianRadius:
    """A radius in photon-normalised comoving Mpc and its mass label.

    ``omega_m_R_cubed_Mpc3 = omega_m,eff R^3`` is proportional to the
    Lagrangian mass ``M = (4 pi/3) rho_crit(100) omega_m,eff R^3``.
    """

    spec: LagrangianRadiusSpec
    radius_Mpc: float
    omega_m_R_cubed_Mpc3: float
    formula: str
    convention_status: str

    def __post_init__(self) -> None:
        if not isinstance(self.spec, LagrangianRadiusSpec):
            raise LagrangianSigmaContractError("spec must be LagrangianRadiusSpec")
        _positive(self.radius_Mpc, "radius_Mpc")
        _positive(self.omega_m_R_cubed_Mpc3, "omega_m_R_cubed_Mpc3")
        _nonempty(self.formula, "formula")
        _check_statuses(self, {"convention_status": RADIUS_CONVENTION_STATUS})

    def to_json_dict(self) -> dict:
        return {"spec": self.spec.to_metadata(), "radius_Mpc": self.radius_Mpc,
                "omega_m_R_cubed_Mpc3": self.omega_m_R_cubed_Mpc3,
                "formula": self.formula, "convention_status": self.convention_status,
                "frame": "photon_normalised_comoving_Mpc"}


def resolve_lagrangian_radius(
    *, spec: LagrangianRadiusSpec, density: EarlyMatterDensityPerPhoton,
) -> ResolvedLagrangianRadius:
    """Resolve a radius convention ([1G-A] Sec. 6.4) to photon-normalised Mpc.

    * equal mass: ``R = R_ref (omega_ref/omega_m,eff)^(1/3)`` (Lagrangian
      mass conservation, ``<rho>_D a_D^3`` constant, [1G-A] Sec. 6.1);
    * dressed: ``R = L/h_dressed`` of wall-comoving length;
    * bare: ``R = (L/h_bare)/gamma_w0`` (present volume-average proper length
      mapped to photon-normalised comoving length, ``a_D0/a_w0 = gamma_w0``,
      [GM] Eq. (5.4));
    * explicit: the supplied radius.
    """
    if not isinstance(spec, LagrangianRadiusSpec):
        raise LagrangianSigmaContractError("spec must be LagrangianRadiusSpec")
    if not isinstance(density, EarlyMatterDensityPerPhoton):
        raise LagrangianSigmaContractError("density must be EarlyMatterDensityPerPhoton")
    om = density.omega_m_per_photon
    convention = spec.convention
    if convention is LagrangianRadiusConvention.EQUAL_LAGRANGIAN_MASS_TO_REFERENCE:
        radius = spec.reference_radius_Mpc * (spec.reference_omega_m / om) ** (1.0 / 3.0)
        formula = "R = R_ref (omega_ref / omega_m_eff)^(1/3)"
    elif convention is LagrangianRadiusConvention.DRESSED_WALL_COMOVING_LENGTH:
        radius = spec.length_h_inverse_Mpc / density.h_dressed
        formula = "R = L / h_dressed"
    elif convention is LagrangianRadiusConvention.BARE_VOLUME_AVERAGE_PROPER_LENGTH:
        radius = (spec.length_h_inverse_Mpc / density.h_bare) / density.gamma_w0
        formula = "R = (L / h_bare) / gamma_w0"
    else:
        radius = spec.explicit_radius_Mpc
        formula = "R = explicit photon-normalised comoving radius"
    return ResolvedLagrangianRadius(
        spec=spec, radius_Mpc=float(radius), omega_m_R_cubed_Mpc3=float(om * radius ** 3),
        formula=formula, convention_status=RADIUS_CONVENTION_STATUS)


# --------------------------------------------------------------------------
# Timescape conditional sigma(M)
# --------------------------------------------------------------------------

_RESULT_STATUSES = {
    "classification": SCIENTIFIC_CLASSIFICATION,
    "observational_status": OBSERVATIONAL_STATUS,
    "amplitude_status": SIGMA8_STATUS,
    "growth_rate_product_status": FSIGMA8_STATUS,
    "early_spectrum_status": EARLY_SPECTRUM_IMPORT_STATUS,
}


def _status_json(record) -> dict:
    return {"classification": record.classification,
            "observational": record.observational_status,
            "amplitude_identity": record.amplitude_status,
            "growth_rate_product": record.growth_rate_product_status,
            "early_spectrum": record.early_spectrum_status}


@dataclass(frozen=True, kw_only=True)
class ConditionalLagrangianSigma:
    """Conditional model-internal linear sigma(M) of the Timescape tracker.

    ``linear_sigma = growth_today_photon_normalised * sigma_unit_growth``
    with ``sigma_unit_growth`` Eq. (1) at ``D0 = 1``.  Not an observational
    amplitude (see the module docstring); every status field must equal the
    module constant.
    """

    background: TimescapeTrackerInput
    growth: TimescapeGrowthFactor
    density: EarlyMatterDensityPerPhoton
    radius: ResolvedLagrangianRadius
    early_spectrum: EarlySpectrumImport
    quadrature: LagrangianSigmaQuadrature
    sigma_unit_growth: float
    sigma_unit_growth_comparison_grid: float
    quadrature_relative_change: float
    truncation_envelope_fraction: float
    linear_sigma: float
    model_caveat: str
    limitations: tuple[str, ...]
    classification: str
    observational_status: str
    amplitude_status: str
    growth_rate_product_status: str
    early_spectrum_status: str

    def __post_init__(self) -> None:
        for name, cls in (("background", TimescapeTrackerInput),
                          ("growth", TimescapeGrowthFactor),
                          ("density", EarlyMatterDensityPerPhoton),
                          ("radius", ResolvedLagrangianRadius),
                          ("early_spectrum", EarlySpectrumImport),
                          ("quadrature", LagrangianSigmaQuadrature)):
            if not isinstance(getattr(self, name), cls):
                raise LagrangianSigmaContractError(f"{name} must be {cls.__name__}")
        if self.density.background is not self.background:
            raise LagrangianSigmaContractError(
                "density must be evaluated for this exact background object")
        if self.growth.fv0 != self.background.fv0:
            raise LagrangianSigmaContractError("growth and background f_v0 differ")
        for name in ("sigma_unit_growth", "sigma_unit_growth_comparison_grid",
                     "linear_sigma"):
            _positive(getattr(self, name), name)
        for name in ("quadrature_relative_change", "truncation_envelope_fraction"):
            if _real(getattr(self, name), name) < 0.0:
                raise LagrangianSigmaContractError(f"{name} must be nonnegative")
        if self.linear_sigma != self.growth.growth_today_photon_normalised * self.sigma_unit_growth:
            raise LagrangianSigmaContractError(
                "linear_sigma must equal growth_today_photon_normalised * sigma_unit_growth")
        if self.model_caveat != _caveat(self.growth.growth_law, self.growth.closure):
            raise LagrangianSigmaContractError("model_caveat is inconsistent with growth law")
        if not isinstance(self.limitations, tuple) or self.model_caveat not in self.limitations:
            raise LagrangianSigmaContractError(
                "limitations must be a tuple containing the model caveat")
        if any(item not in self.limitations for item in _GENERIC_LIMITATIONS):
            raise LagrangianSigmaContractError("limitations must contain the generic caveats")
        _check_statuses(self, _RESULT_STATUSES)

    def to_json_dict(self) -> dict:
        return {
            "quantity_label": "conditional_lagrangian_linear_sigma_M",
            "status": _status_json(self),
            "frames": {
                "growth_background": (
                    "volume_average_D" if self.growth.growth_law is GrowthLaw.VOLUME_AVERAGE_CGI
                    else "wall_regional_common_time"),
                "radius": "photon_normalised_comoving_Mpc",
                "mass_label": "lagrangian_omega_m_eff_R3",
            },
            "background": self.background.to_metadata(),
            "growth": self.growth.to_json_dict(),
            "early_matter_density": self.density.to_json_dict(),
            "radius": self.radius.to_json_dict(),
            "early_spectrum": self.early_spectrum.to_metadata(),
            "quadrature": {
                "config": self.quadrature.to_metadata(),
                "relative_change": self.quadrature_relative_change,
                "truncation_envelope_fraction": self.truncation_envelope_fraction,
                "unit_growth_value": self.sigma_unit_growth,
                "unit_growth_value_comparison_grid": self.sigma_unit_growth_comparison_grid,
            },
            "linear_sigma": self.linear_sigma,
            "model_caveat": self.model_caveat,
            "limitations": list(self.limitations),
        }


def conditional_lagrangian_linear_sigma(
    *,
    background: TimescapeTrackerInput,
    growth_law: GrowthLaw,
    closure: CleanPerturbationSystem | str,
    growth_numerics: VolumeAverageGrowthNumerics | WallRegionalGrowthChecks,
    early_spectrum: EarlySpectrumImport,
    radius: LagrangianRadiusSpec,
    quadrature: LagrangianSigmaQuadrature,
    density_identity_tolerance: float,
    G: float,
) -> ConditionalLagrangianSigma:
    """Conditional mass-labelled linear sigma(M) today, Eq. (1).

    Chain ([1G-A] Secs. 4-7): growth law (Eq. (2) or (3)) ->
    ``D0 = gamma_w0 g`` -> ``omega_m,eff`` (Eq. (4)) -> early spectrum
    (Eq. (5), EH98) -> radius convention -> top-hat quadrature.  Every
    argument is mandatory and keyword-only; for the wall law pass
    ``closure=NOT_APPLICABLE``.  The barotropic closure is refused
    ([1G-A] Sec. 4.1).  The result is conditional and model-internal.
    """
    if _is_barotropic(closure):
        raise BarotropicClosureRefusedError(_BAROTROPIC_REFUSAL)
    for name, value, cls in (("background", background, TimescapeTrackerInput),
                             ("early_spectrum", early_spectrum, EarlySpectrumImport),
                             ("radius", radius, LagrangianRadiusSpec),
                             ("quadrature", quadrature, LagrangianSigmaQuadrature)):
        if not isinstance(value, cls):
            raise LagrangianSigmaContractError(f"{name} must be {cls.__name__}")
    growth = timescape_growth_factor(
        params=background.dimensionless_params(), growth_law=growth_law,
        closure=closure, numerics=growth_numerics, G=G)
    density = early_matter_density_per_photon(
        background=background, identity_tolerance=density_identity_tolerance, G=G)
    resolved = resolve_lagrangian_radius(spec=radius, density=density)
    outcome = _quadrature(radius_Mpc=resolved.radius_Mpc,
                          omega_m=density.omega_m_per_photon,
                          early_spectrum=early_spectrum, quadrature=quadrature)
    caveat = _caveat(growth.growth_law, growth.closure)
    return ConditionalLagrangianSigma(
        background=background, growth=growth, density=density, radius=resolved,
        early_spectrum=early_spectrum, quadrature=quadrature,
        sigma_unit_growth=outcome.sigma_unit_growth,
        sigma_unit_growth_comparison_grid=outcome.sigma_unit_growth_comparison,
        quadrature_relative_change=outcome.relative_change,
        truncation_envelope_fraction=outcome.truncation_envelope_fraction,
        linear_sigma=growth.growth_today_photon_normalised * outcome.sigma_unit_growth,
        model_caveat=caveat, limitations=_GENERIC_LIMITATIONS + (caveat,),
        **_RESULT_STATUSES)


# --------------------------------------------------------------------------
# Flat-LCDM reference and anchored ratios
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class LCDMReferenceLinearSigma:
    """Flat-LCDM linear sigma with the same machinery (anchoring reference).

    ``growth_today_photon_normalised = qplus(0)`` (``D/a -> 1``, frozen
    recipe of ``perturbations.initial_conditions``); ``omega_m = Omega_m h^2``
    of the recipe; the radius is an explicit comoving radius in Mpc.
    """

    recipe: LCDMGrowthRecipe
    omega_m: float
    growth_today_photon_normalised: float
    radius_Mpc: float
    omega_m_R_cubed_Mpc3: float
    early_spectrum: EarlySpectrumImport
    quadrature: LagrangianSigmaQuadrature
    sigma_unit_growth: float
    sigma_unit_growth_comparison_grid: float
    quadrature_relative_change: float
    truncation_envelope_fraction: float
    linear_sigma: float
    limitations: tuple[str, ...]
    classification: str
    observational_status: str
    amplitude_status: str
    growth_rate_product_status: str
    early_spectrum_status: str

    def __post_init__(self) -> None:
        if not isinstance(self.recipe, LCDMGrowthRecipe):
            raise LagrangianSigmaContractError("recipe must be LCDMGrowthRecipe")
        if not isinstance(self.early_spectrum, EarlySpectrumImport):
            raise LagrangianSigmaContractError("early_spectrum must be EarlySpectrumImport")
        if not isinstance(self.quadrature, LagrangianSigmaQuadrature):
            raise LagrangianSigmaContractError("quadrature must be LagrangianSigmaQuadrature")
        for name in ("omega_m", "growth_today_photon_normalised", "radius_Mpc",
                     "omega_m_R_cubed_Mpc3", "sigma_unit_growth",
                     "sigma_unit_growth_comparison_grid", "linear_sigma"):
            _positive(getattr(self, name), name)
        if self.linear_sigma != self.growth_today_photon_normalised * self.sigma_unit_growth:
            raise LagrangianSigmaContractError(
                "linear_sigma must equal growth_today_photon_normalised * sigma_unit_growth")
        if self.limitations != _LCDM_LIMITATIONS:
            raise LagrangianSigmaContractError("limitations must be the LCDM reference caveats")
        _check_statuses(self, _RESULT_STATUSES)

    def to_json_dict(self) -> dict:
        r = self.recipe
        return {
            "quantity_label": "lcdm_reference_lagrangian_linear_sigma",
            "status": _status_json(self),
            "recipe": {"omega_m": r.omega_m, "omega_lambda": r.omega_lambda, "h": r.h},
            "omega_m_h2": self.omega_m,
            "growth_today_photon_normalised": self.growth_today_photon_normalised,
            "radius_Mpc": self.radius_Mpc,
            "omega_m_R_cubed_Mpc3": self.omega_m_R_cubed_Mpc3,
            "early_spectrum": self.early_spectrum.to_metadata(),
            "quadrature": {
                "config": self.quadrature.to_metadata(),
                "relative_change": self.quadrature_relative_change,
                "truncation_envelope_fraction": self.truncation_envelope_fraction,
                "unit_growth_value": self.sigma_unit_growth,
                "unit_growth_value_comparison_grid": self.sigma_unit_growth_comparison_grid,
            },
            "linear_sigma": self.linear_sigma,
            "limitations": list(self.limitations),
        }


def lcdm_reference_linear_sigma(
    *,
    recipe: LCDMGrowthRecipe,
    early_spectrum: EarlySpectrumImport,
    radius_Mpc: float,
    quadrature: LagrangianSigmaQuadrature,
) -> LCDMReferenceLinearSigma:
    """Flat-LCDM reference sigma at an explicit radius (Eqs. (1), (5)).

    Growth today relative to photon-normalised EdS is ``qplus(0)`` of the
    frozen flat-LCDM recipe (Short & Coles, astro-ph/0605013v2, Eq. (3);
    ``perturbations.initial_conditions.qplus``); ``omega_m = Omega_m h^2``.
    """
    if not isinstance(recipe, LCDMGrowthRecipe):
        raise LagrangianSigmaContractError("recipe must be LCDMGrowthRecipe")
    if not isinstance(early_spectrum, EarlySpectrumImport):
        raise LagrangianSigmaContractError("early_spectrum must be EarlySpectrumImport")
    if not isinstance(quadrature, LagrangianSigmaQuadrature):
        raise LagrangianSigmaContractError("quadrature must be LagrangianSigmaQuadrature")
    radius = _positive(radius_Mpc, "radius_Mpc")
    omega_m = recipe.omega_m * recipe.h ** 2
    growth = float(qplus(0.0, recipe))
    outcome = _quadrature(radius_Mpc=radius, omega_m=omega_m,
                          early_spectrum=early_spectrum, quadrature=quadrature)
    return LCDMReferenceLinearSigma(
        recipe=recipe, omega_m=omega_m, growth_today_photon_normalised=growth,
        radius_Mpc=radius, omega_m_R_cubed_Mpc3=omega_m * radius ** 3,
        early_spectrum=early_spectrum, quadrature=quadrature,
        sigma_unit_growth=outcome.sigma_unit_growth,
        sigma_unit_growth_comparison_grid=outcome.sigma_unit_growth_comparison,
        quadrature_relative_change=outcome.relative_change,
        truncation_envelope_fraction=outcome.truncation_envelope_fraction,
        linear_sigma=growth * outcome.sigma_unit_growth,
        limitations=_LCDM_LIMITATIONS, **_RESULT_STATUSES)


_EARLY_SPECTRUM_COMPARED = ("A_s", "n_s", "k_pivot_per_Mpc", "baryon_fraction")


@dataclass(frozen=True, kw_only=True)
class AnchoredLagrangianSigmaRatio:
    """``sigma_TS/sigma_LCDM`` and its anchored value ([1G-A] Sec. 7).

    ``sigma_ratio = growth_ratio * early_spectrum_factor`` with
    ``growth_ratio = D0_TS/D0_LCDM`` (X of [1G-A] Secs. 5.1, 8) and
    ``early_spectrum_factor`` the unit-growth ratio (E of [1G-A] Sec. 7).
    ``anchored_linear_sigma = sigma_ratio * anchor_value``; the anchor is an
    explicit external input and ``reference_offset_from_anchor`` records how
    far the provisional machinery places the reference from it.
    """

    timescape: ConditionalLagrangianSigma
    reference: LCDMReferenceLinearSigma
    anchor_value: float
    anchor_provenance: str
    anchor_consistency_tolerance: float
    anchor_consistency_rationale: str
    reference_offset_from_anchor: float
    early_spectrum_differences: tuple[str, ...]
    growth_ratio: float
    early_spectrum_factor: float
    sigma_ratio: float
    anchored_linear_sigma: float
    classification: str
    observational_status: str
    amplitude_status: str
    growth_rate_product_status: str
    early_spectrum_status: str

    def __post_init__(self) -> None:
        if not isinstance(self.timescape, ConditionalLagrangianSigma):
            raise LagrangianSigmaContractError("timescape must be ConditionalLagrangianSigma")
        if not isinstance(self.reference, LCDMReferenceLinearSigma):
            raise LagrangianSigmaContractError("reference must be LCDMReferenceLinearSigma")
        for name in ("anchor_value", "anchor_consistency_tolerance", "growth_ratio",
                     "early_spectrum_factor", "sigma_ratio", "anchored_linear_sigma"):
            _positive(getattr(self, name), name)
        _nonempty(self.anchor_provenance, "anchor_provenance")
        _nonempty(self.anchor_consistency_rationale, "anchor_consistency_rationale")
        if not abs(self.reference_offset_from_anchor) <= self.anchor_consistency_tolerance:
            raise LagrangianSigmaContractError("reference offset exceeds the anchor tolerance")
        if not isinstance(self.early_spectrum_differences, tuple):
            raise LagrangianSigmaContractError("early_spectrum_differences must be a tuple")
        if self.anchored_linear_sigma != self.sigma_ratio * self.anchor_value:
            raise LagrangianSigmaContractError(
                "anchored_linear_sigma must equal sigma_ratio * anchor_value")
        _check_statuses(self, _RESULT_STATUSES)

    def to_json_dict(self) -> dict:
        return {
            "quantity_label": "anchored_conditional_lagrangian_linear_sigma_ratio",
            "status": _status_json(self),
            "anchor": {"value": self.anchor_value, "provenance": self.anchor_provenance,
                       "consistency_tolerance": self.anchor_consistency_tolerance,
                       "consistency_rationale": self.anchor_consistency_rationale,
                       "reference_offset_from_anchor": self.reference_offset_from_anchor},
            "early_spectrum_differences": list(self.early_spectrum_differences),
            "growth_ratio": self.growth_ratio,
            "early_spectrum_factor": self.early_spectrum_factor,
            "sigma_ratio": self.sigma_ratio,
            "anchored_linear_sigma": self.anchored_linear_sigma,
            "timescape": self.timescape.to_json_dict(),
            "reference": self.reference.to_json_dict(),
        }


def anchor_lagrangian_sigma(
    *,
    timescape: ConditionalLagrangianSigma,
    reference: LCDMReferenceLinearSigma,
    anchor_value: float,
    anchor_provenance: str,
    anchor_consistency_tolerance: float,
    anchor_consistency_rationale: str,
) -> AnchoredLagrangianSigmaRatio:
    """Form the anchored ratio ``sigma_TS/sigma_LCDM x anchor`` ([1G-A] Sec. 7).

    Contracts (fail closed): identical quadrature configuration; identical
    transfer model and ``T_cmb`` (the photon normalisation); for the
    equal-mass convention, the Timescape reference ``(omega_ref, R_ref)``
    must be this LCDM reference (relative ``REFERENCE_MATCH_RTOL``); and
    ``|sigma_LCDM/anchor - 1| <= anchor_consistency_tolerance``, whose
    justification is the explicit ``anchor_consistency_rationale``.  Other
    early-spectrum differences (A_s, n_s, k_pivot, baryon fraction) are
    allowed but recorded by name.  The anchor value is never defaulted.
    """
    if not isinstance(timescape, ConditionalLagrangianSigma):
        raise LagrangianSigmaContractError("timescape must be ConditionalLagrangianSigma")
    if not isinstance(reference, LCDMReferenceLinearSigma):
        raise LagrangianSigmaContractError("reference must be LCDMReferenceLinearSigma")
    anchor = _positive(anchor_value, "anchor_value")
    _nonempty(anchor_provenance, "anchor_provenance")
    tol = _positive(anchor_consistency_tolerance, "anchor_consistency_tolerance")
    _nonempty(anchor_consistency_rationale, "anchor_consistency_rationale")
    if timescape.quadrature != reference.quadrature:
        raise LagrangianSigmaContractError(
            "timescape and reference must use the same quadrature configuration")
    ts_spec, ref_spec = timescape.early_spectrum, reference.early_spectrum
    if ts_spec.transfer_model is not ref_spec.transfer_model:
        raise LagrangianSigmaContractError("transfer models differ")
    if ts_spec.T_cmb_K != ref_spec.T_cmb_K:
        raise LagrangianSigmaContractError(
            "T_cmb differs: the photon normalisation must be common")
    spec = timescape.radius.spec
    if spec.convention is LagrangianRadiusConvention.EQUAL_LAGRANGIAN_MASS_TO_REFERENCE:
        if not (math.isclose(spec.reference_omega_m, reference.omega_m,
                             rel_tol=REFERENCE_MATCH_RTOL, abs_tol=0.0)
                and math.isclose(spec.reference_radius_Mpc, reference.radius_Mpc,
                                 rel_tol=REFERENCE_MATCH_RTOL, abs_tol=0.0)):
            raise LagrangianSigmaContractError(
                "equal-mass convention: reference (omega_m, R) must match the LCDM reference")
    offset = reference.linear_sigma / anchor - 1.0
    if not abs(offset) <= tol:
        raise LagrangianSigmaContractError(
            f"LCDM reference sigma {reference.linear_sigma:.6f} is {offset:+.3%} from the "
            f"anchor {anchor}; tolerance {tol:.3%}"
        )
    differences = tuple(name for name in _EARLY_SPECTRUM_COMPARED
                        if getattr(ts_spec, name) != getattr(ref_spec, name))
    growth_ratio = (timescape.growth.growth_today_photon_normalised
                    / reference.growth_today_photon_normalised)
    sigma_ratio = timescape.linear_sigma / reference.linear_sigma
    return AnchoredLagrangianSigmaRatio(
        timescape=timescape, reference=reference, anchor_value=anchor,
        anchor_provenance=anchor_provenance, anchor_consistency_tolerance=tol,
        anchor_consistency_rationale=anchor_consistency_rationale,
        reference_offset_from_anchor=offset, early_spectrum_differences=differences,
        growth_ratio=growth_ratio,
        early_spectrum_factor=timescape.sigma_unit_growth / reference.sigma_unit_growth,
        sigma_ratio=sigma_ratio, anchored_linear_sigma=sigma_ratio * anchor,
        **_RESULT_STATUSES)
