"""Conditional global-mean linear matter variance of the two-phase tracker (Phase 1G-H).

EXPERIMENTAL, CONDITIONAL RESEARCH RUNTIME.  Authorisation: the project
owner's task statement of 2026-10-06 (Phase 1G-H, "Global matter-variance
definition and minimal closure"), which authorises new experimental modules
for this phase and does not promote any hypothesis to a project law.  Report:
``reports/phase1g_h_global_variance_closure.md`` (cited as [1G-H]; its
equation numbers (H1)-(H24) are cited below).  Nothing here is an
observational amplitude: every result carries ``NON_OBSERVATIONAL`` and
``NOT_OBSERVATIONAL_SIGMA_8``; ``scientific_status.SIGMA8_AUTHORIZATION``
and the other observational tokens stay ``NOT_GRANTED``, and
``LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC`` stays ``NOT_DERIVED`` until the
owner decides otherwise.  No public name or output key carries the
observational tokens (``sigma8``, ``sigma_8``, ``8hMpc``).

What is defined ([1G-H] Sec. 2, as remediated after the 2026-10-07 audit)
--------------------------------------------------------------------------
For a Lagrangian region L (a fixed set of dust elements) on the
dust-orthogonal foliation of [GM] Sec. 3 (Buchert averaging, dust proper
time t), the global contrast is

    1 + delta_L = (M_L / V_L) / (M_D / V_D),                              (H1)

with V the Riemannian volume on the slice and D the averaging domain.  The
smoothing region is the Lagrangian top-hat ball of radius R in
photon-normalised comoving Mpc (the early frame, in which all frames agree
to O(f_v)).  The statistic computed here is the *formal tangent statistic*
(owner decision D1 of 2026-10-07 on audit finding GH-F1; a proposal, not a
closed definition): the rms of the linearly propagated early field, i.e. the
zero-amplitude tangent G(k) of the regional contrast map around the smooth
two-phase tracker state applied to the early Gaussian field, with the
smoothing rule G_R(k) = G(k) W(k R) of a Lagrangian top hat,

    sigma^2_lin(R) = int dln k Delta^2_u(k) G(k, t0)^2 W^2(k R),          (H10)

with Delta^2_u the photon-normalised matter-era spectrum at unit growth
(``lagrangian_sigma.matter_era_linear_amplitude``, [1G-A] Sec. 6.3) and G the
global linear propagator.  It is the analogue of the linear sigma at 8 Mpc/h
of LCDM (linear extrapolation with the growth factor), not the ensemble-mean
response of the true region contrast, which differs from the tangent when
the small-scale field has finite amplitude.  The tangent treats the two-phase
state as smooth on the region scale.  In the FLRW limit G is the linear
growth factor and (H10) is the standard top-hat variance ([JLH13]
arXiv:1304.6087v2, Eq. (2)).

What is derived ([1G-H] Secs. 3-4)
-----------------------------------
* Exact two-phase identities (mass conservation and volume additivity on the
  dust slice): (H2) for finite-density phases and, for empty voids,

    1/(1 + delta_L) = f_w/(1 + delta_w,L) + f_v/(1 + epsilon_L),           (H3)

  with 1 + delta_w,L the region's wall density over the global wall density
  and 1 + epsilon_L its reference void volume over its void volume.
* In the tracker, under the regional laws A1-A5 (walls Einstein-de Sitter in
  common time t, 1G-C and its owner decisions) and void autonomy H-A6 (each
  empty void region expands as Milne, V_v proportional to t^3, with no
  wall-void volume transfer, 1G-G G3/G5 with J = 0), delta_w,L grows as
  t^(2/3) and epsilon_L is constant.  Splitting the early contrast at the
  matching epoch (last scattering, explicit redshift) into a void share p
  and a wall share 1 - p gives the exact propagator

    G(k, t0) = (1 - p(k)) D_W + p(k) D_V,                                  (H9)
    D_W = gamma_w0 f_w0^(4/3) / (gamma_w,LS f_w,LS^(4/3)),                  (H8)
    D_V = f_v0 / [f_v,LS (1 + z_LS)],

  from [GM] Eqs. (5.4)-(5.6) and text p. 25 (``1 + z = gamma_w a_w0/a_D``,
  ``gamma_w = 1 + f_v/2``, ``a_D proportional to t f_v^(-1/3)``,
  ``f_v = t/(t + tau)``).  With p = 0 this is 1G-D's wall-curvature mode and
  with p = 1 its void-onset mode.  (H9) holds for every Lagrangian region
  whose regional laws are A1-A5 and H-A6 under the seed-indexed void
  accounting H-A9 (owner decision D2 of 2026-10-07 on GH-F2): the void volume
  of a region is the volume of the bubbles whose seeds lie in its Lagrangian
  ball.  That equals the volume of the transported material region only with
  scale separation (void radii much smaller than R), which is not met at
  8 Mpc/h; the material-domain extension below the super-cell scale stays
  unproved.

What is NOT derived
-------------------
The void share p(k) is the single missing input of (H9) under these
assumptions.  It is defined by ``p delta_L(LS) = f_v,LS epsilon``, i.e.
``p = f_v,LS - d f_v,L/d delta_L`` for the region's void volume fraction
f_v,L at the matching epoch (audit GH-F3).  It carries the status of 1G-D's
void-onset response (``scientific_status.VOID_ONSET_RESPONSE =
EXTERNAL_CLOSURE_INPUT``): with 1G-D's threshold response A_v,
``p(k -> 0) = f_v,LS (1 + A_v)`` when the seed volume is compressed with its
region and ``f_v,LS A_v`` for the threshold shift alone.  It must be supplied
as an explicit closure:

* ``ConstantVoidShare``: an explicit, scale-independent p in [0, 1];
* ``GaussianThresholdSeedVoidShare``: the peak-background split of a Gaussian
  threshold for void seeds at last scattering ([1G-D] Sec. 7 and its owner
  decisions GD-OD1/OD2/OD6), p(k) = phi(nu) W(k R_s)/sigma_s (+ f_v,LS when
  the seed volume is compressed with its region), (H12).  The seed radius is
  an explicit input.

There is no default closure.  The numbers are conditional on A1-A5, H-A6,
H-A9, the monotone response H-A7 (``f_v,LS <= p <= 1`` at k -> 0 for a void
fraction that does not grow with the overdensity; an added class
assumption, not a tracker theorem), the closure, the early-spectrum import
(``PROVISIONAL_MODEL_IMPORT``) and the radius convention
(``CONVENTION_DEPENDENT``).

Supporting results ([1G-H] Secs. 5-7)
-------------------------------------
* ``strict_flat_wall_contrast_cap``: with universal (flat) walls a region's
  contrast is bounded above by f_v/f_w (H13).
* ``admissible_global_linear_interval``: the constant-share interval from the
  monotone lower end and an adopted reading of the background's homogeneity
  premise ([W09] arXiv:0909.0749v2, ll. 327-335 and 455-458), (H15).  It
  holds only for a void share constant over the spectral support of both
  windows; scale-dependent shares in the monotone class are not bounded by
  it (audit GH-F4).
* ``two_phase_global_variance``: the complete two-phase covariance with
  phase-conditional normalisation and every cross term (H17)-(H19), with a
  positive-semidefiniteness gate; ``cauchy_schwarz_total_rms_interval``
  (H20).
* ``bivariate_normal_orthant_probability`` and
  ``bivariate_normal_orthant_moments``: orthant integrals of a bivariate
  normal with an explicit accuracy contract (H21), used by the constructive
  pairs of the evidence script (a signed Gaussian surrogate pair and a
  nonnegative lognormal pair, owner decision D3 on GH-F5).
* ``two_barrier_void_mass_fraction`` and ``two_barrier_global_linear_bias``:
  the excursion-set response of the two-barrier void mass fraction of
  [SvdW04] (astro-ph/0311260, Eq. (3)), an alternative closure (H22).

Records are fail-closed: on construction every public record re-validates
its fields (audit GH-F9) and recomputes each result and diagnostic from its
stored inputs with the same pure function its factory uses, refusing any
record whose inputs do not reproduce its results (delta audit GH-DF2).  A
float result must be stored as a float, and this module's own scalar inputs
are stored as floats (second delta audit GH-D2F4); every record also refuses
construction unless its export, nested 1G-B input records included, is
strict JSON (third delta audit GH-D3F2).

References: [GM] Galoppo & Mourier, arXiv:2511.17160v2; [W07] Wiltshire,
arXiv:0709.0732v2; [W09] Wiltshire, arXiv:0909.0749v2; [JLH13] Jennings,
Li & Hu, arXiv:1304.6087v2; [SvdW04] Sheth & van de Weygaert,
astro-ph/0311260; [EH98] Eisenstein & Hu, astro-ph/9709112, the
zero-baryon-oscillation (no-wiggle) fit with the baryon shape suppression,
Eqs. (26), (28)-(31), through ``lagrangian_sigma``.  Every scientific choice
is a mandatory keyword-only argument; inapplicable choices are passed as
``NOT_APPLICABLE``.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from numbers import Real

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.integrate import simpson, solve_ivp
from scipy.optimize import brentq
from scipy.special import ndtr, ndtri

import timescape_fsigma8.background as bg
from timescape_fsigma8.lagrangian_sigma import (
    EarlyMatterDensityPerPhoton,
    EarlySpectrumImport,
    LagrangianRadiusSpec,
    LagrangianSigmaQuadrature,
    ResolvedLagrangianRadius,
    TimescapeTrackerInput,
    early_matter_density_per_photon,
    matter_era_linear_amplitude,
    resolve_lagrangian_radius,
    top_hat_window,
)

__all__ = [
    # status / provenance constants
    "PHASE",
    "MODULE_STATUS",
    "SCIENTIFIC_CLASSIFICATION",
    "OBSERVATIONAL_STATUS",
    "AMPLITUDE_STATUS",
    "GROWTH_RATE_PRODUCT_STATUS",
    "VOID_SHARE_STATUS",
    "PROPAGATOR_EVIDENCE_CLASS",
    "NOT_APPLICABLE",
    "VOID_RESPONSE_NONPERTURBATIVE_THRESHOLD",
    "VOID_RESPONSE_PERTURBATIVE",
    "VOID_RESPONSE_NONPERTURBATIVE",
    "PSD_TOLERANCE",
    "RECORD_IDENTITY_RTOL",
    "ORTHANT_MAX_NODES",
    # enums
    "SeedVolumeCompression",
    "WallLongModeResponse",
    # errors
    "GlobalVarianceContractError",
    "GlobalVarianceNumericalError",
    # inputs
    "LastScatteringMatching",
    "TwoPhaseGrowthChecks",
    "ConstantVoidShare",
    "GaussianThresholdSeedVoidShare",
    "HomogeneityPremise",
    "TwoPhaseSmoothedMoments",
    "TWO_PHASE_GROWTH_REFERENCE_CHECKS",
    # records
    "TwoPhaseGlobalGrowth",
    "EvaluatedVoidShare",
    "ConditionalGlobalLinearSigma",
    "AdmissibleGlobalLinearInterval",
    # functions
    "empty_void_region_contrast",
    "two_phase_region_contrast",
    "linear_two_phase_contrast_coefficients",
    "strict_flat_wall_contrast_cap",
    "two_phase_global_growth",
    "tracker_consistent_seed_radius",
    "unit_growth_lagrangian_sigma",
    "evaluate_void_share",
    "global_linear_propagator",
    "conditional_global_linear_sigma",
    "admissible_global_linear_interval",
    "two_phase_global_variance",
    "cauchy_schwarz_total_rms_interval",
    "bivariate_normal_orthant_probability",
    "bivariate_normal_orthant_moments",
    "two_barrier_void_mass_fraction",
    "two_barrier_global_linear_bias",
]


# --------------------------------------------------------------------------
# Status and provenance constants (part of the API; do not relabel)
# --------------------------------------------------------------------------

PHASE = "1G-H"
MODULE_STATUS = "EXPERIMENTAL_CONDITIONAL_RESEARCH_RUNTIME"
SCIENTIFIC_CLASSIFICATION = "CONDITIONAL_MODEL_INTERNAL_GLOBAL_MEAN_LINEAR_MASS_VARIANCE"
OBSERVATIONAL_STATUS = "NON_OBSERVATIONAL"
AMPLITUDE_STATUS = "NOT_OBSERVATIONAL_SIGMA_8"
GROWTH_RATE_PRODUCT_STATUS = "NOT_FSIGMA8"
# The void share is 1G-D's void-onset response in another normalisation
# (scientific_status.VOID_ONSET_RESPONSE).
VOID_SHARE_STATUS = "EXTERNAL_CLOSURE_INPUT"
# (H9) given A1-A5, H-A6 and an explicit void share ([1G-H] Sec. 3).
PROPAGATOR_EVIDENCE_CLASS = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
NOT_APPLICABLE = "NOT_APPLICABLE"

# rms void-volume response above which the linear void share is
# non-perturbative: the epsilon = 1 criterion of 1G-D Sec. 8.
VOID_RESPONSE_NONPERTURBATIVE_THRESHOLD = 1.0
VOID_RESPONSE_PERTURBATIVE = "VOID_RESPONSE_PERTURBATIVE"
VOID_RESPONSE_NONPERTURBATIVE = "VOID_RESPONSE_NONPERTURBATIVE"

# Relative tolerance of the positive-semidefiniteness gate of the smoothed
# two-phase second-moment matrix: eigenvalues >= -PSD_TOLERANCE * max|eig|.
# Round-off allowance for moments assembled from O(1) quadratures.
PSD_TOLERANCE = 1e-12

# Relative tolerance of the record invariants re-evaluated in __post_init__
# from a record's own stored fields (audit GH-F9), and of the comparison of
# every stored result and diagnostic with its recomputation from the record's
# stored inputs (delta audit GH-DF2): a round-off allowance for closed forms
# of O(1) quantities, the same order as the identity tolerance of
# TWO_PHASE_GROWTH_REFERENCE_CHECKS.  The recomputation runs the same
# deterministic code in the same process, so a genuine record agrees exactly;
# the allowance only guards against reassociation.  It is not a physics
# tolerance.
RECORD_IDENTITY_RTOL = 1e-12

# Orthant quadrature (audit GH-F10): Gauss-Legendre panels are refined by
# doubling the node count until two successive results agree to the caller's
# absolute tolerance; beyond ORTHANT_MAX_NODES per panel the evaluation is
# refused (the panels split at the conditional step converge by 64-128 nodes;
# numpy's leggauss costs O(n^3), so the cap also bounds the run time).  The
# integration range is truncated to |u| <= 12: the omitted Gaussian tails of
# the five moments are below 12^2 phi(12) < 1e-29.
ORTHANT_MAX_NODES = 1 << 10
_ORTHANT_HALF_WIDTH = 12.0


# --------------------------------------------------------------------------
# Errors
# --------------------------------------------------------------------------

class GlobalVarianceContractError(ValueError):
    """An explicit input, closure or record contract is violated."""


class GlobalVarianceNumericalError(ArithmeticError):
    """A fail-closed numerical check (convergence, identity) failed."""


# --------------------------------------------------------------------------
# Enums
# --------------------------------------------------------------------------

class SeedVolumeCompression(str, Enum):
    """How a long mode acts on the void-seed volume at last scattering ([1G-H] (H12)).

    ``COMPRESSED_WITH_REGION``: the seed volume shrinks with its region (a long
    mode compresses every volume element by delta_L at linear order) on top of
    the threshold shift, so p = f_v,LS + phi(nu) W/sigma_s; this is the
    kinematics derived in [1G-H] Sec. 4.2.
    ``THRESHOLD_SHIFT_ONLY``: only the threshold shift, as 1G-D's S2 is written
    (epsilon = A_v delta_L); it differs from the former by f_v,LS in p.
    """

    COMPRESSED_WITH_REGION = "compressed_with_region"
    THRESHOLD_SHIFT_ONLY = "threshold_shift_only_1g_d_s2"


class WallLongModeResponse(str, Enum):
    """Response of the wall density to a long mode in the two-barrier closure (H22)."""

    COMPRESSED_WITH_LONG_MODE = "compressed_with_long_mode"
    UNIVERSAL_WALL_DENSITY = "universal_wall_density"


# --------------------------------------------------------------------------
# Validation helpers
# --------------------------------------------------------------------------

def _real(value, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise GlobalVarianceContractError(f"{name} must be a real scalar, not {value!r}")
    out = float(value)
    if not math.isfinite(out):
        raise GlobalVarianceContractError(f"{name} must be finite")
    return out


def _positive(value, name: str) -> float:
    out = _real(value, name)
    if not out > 0.0:
        raise GlobalVarianceContractError(f"{name} must be positive")
    return out


def _fraction_open(value, name: str) -> float:
    out = _real(value, name)
    if not 0.0 < out < 1.0:
        raise GlobalVarianceContractError(f"{name} must lie in (0, 1)")
    return out


def _nonempty(value, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GlobalVarianceContractError(f"{name} must be a non-empty string")
    return value


def _real_array(value, name: str) -> NDArray[np.float64]:
    arr = np.asarray(value)
    if arr.dtype.kind not in "iuf":
        raise GlobalVarianceContractError(f"{name} must be a real numeric array")
    arr = np.array(arr, dtype=np.float64)
    if not np.all(np.isfinite(arr)):
        raise GlobalVarianceContractError(f"{name} must be finite")
    return arr


def _readonly(values) -> NDArray[np.float64]:
    out = np.array(values, dtype=np.float64)
    out.setflags(write=False)
    return out


def _require(value, cls, name: str):
    if not isinstance(value, cls):
        raise GlobalVarianceContractError(f"{name} must be {cls.__name__}")
    return value


def _require_enum(value, enum_type, name: str):
    if not isinstance(value, enum_type):
        raise GlobalVarianceContractError(f"{name} must be a {enum_type.__name__} member")
    return value


def _close(value: float, expected: float) -> bool:
    """Record invariant: ``value`` re-evaluated from stored fields (RECORD_IDENTITY_RTOL)."""
    return math.isclose(value, expected, rel_tol=RECORD_IDENTITY_RTOL, abs_tol=0.0)


def _same(stored, expected) -> bool:
    """A stored field equals its recomputation (floats within RECORD_IDENTITY_RTOL).

    A float result must be stored as a finite ``float`` (``numpy.float64`` and
    other ``float`` subclasses qualify; ``numpy.float32`` does not).  This is a
    typed-output policy (second delta audit GH-D2F4): an equal ``Fraction``
    would also break strict JSON, while an equal ``int`` is valid JSON but not
    the recomputed type (wording corrected after third delta audit GH-D3E3).
    """
    if isinstance(expected, bool) or isinstance(stored, bool):
        return type(stored) is type(expected) and stored == expected
    if isinstance(expected, float):
        return (isinstance(stored, float) and math.isfinite(stored)
                and _close(stored, expected))
    if isinstance(expected, tuple):
        return (isinstance(stored, tuple) and len(stored) == len(expected)
                and all(_same(a, b) for a, b in zip(stored, expected)))
    return stored == expected


def _bind_recomputed(record, compute, what: str) -> None:
    """Every stored result equals its recomputation from the stored inputs (GH-DF2).

    ``compute()`` re-derives the record's results and diagnostics with the
    same pure function its factory uses; a record whose inputs no longer
    reproduce its results (for instance after ``dataclasses.replace`` of an
    input), or whose inputs make the computation fail, is refused.
    """
    try:
        values = compute()
    except GlobalVarianceNumericalError as exc:
        raise GlobalVarianceContractError(
            f"{what}: the stored inputs do not reproduce a valid result ({exc})") from exc
    for name, expected in values.items():
        stored = getattr(record, name)
        if isinstance(expected, float) and not isinstance(stored, float):
            raise GlobalVarianceContractError(
                f"{what}: {name} must be a float, not {type(stored).__name__}")
        if not _same(stored, expected):
            raise GlobalVarianceContractError(
                f"{what}: {name} differs from its recomputation from the stored inputs")


def _require_strict_json(export: dict, what: str) -> None:
    """The record's export is strict JSON, nested input records included.

    Nested 1G-B records validate their scalars as ``numbers.Real`` without
    converting them, so a ``Fraction``, ``numpy.float32`` or ``numpy.int64``
    input would otherwise reach the export (third delta audit GH-D3F2).
    """
    try:
        json.dumps(export, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise GlobalVarianceContractError(
            f"{what}: the export is not strict JSON ({exc}); pass native float and int "
            "scalars, also inside nested input records") from exc


def _strings(value, name: str) -> tuple[str, ...]:
    if not isinstance(value, tuple) or not value:
        raise GlobalVarianceContractError(f"{name} must be a non-empty tuple")
    for item in value:
        _nonempty(item, name)
    return value


def _statuses_ok(record) -> None:
    expected = {"classification": SCIENTIFIC_CLASSIFICATION,
                "observational_status": OBSERVATIONAL_STATUS,
                "amplitude_status": AMPLITUDE_STATUS,
                "growth_rate_product_status": GROWTH_RATE_PRODUCT_STATUS,
                "module_status": MODULE_STATUS}
    for name, value in expected.items():
        if getattr(record, name) != value:
            raise GlobalVarianceContractError(f"{name} must be {value}")


_STATUS_FIELDS = {"classification": SCIENTIFIC_CLASSIFICATION,
                  "observational_status": OBSERVATIONAL_STATUS,
                  "amplitude_status": AMPLITUDE_STATUS,
                  "growth_rate_product_status": GROWTH_RATE_PRODUCT_STATUS,
                  "module_status": MODULE_STATUS}


def _status_json(record) -> dict:
    return {"classification": record.classification,
            "observational": record.observational_status,
            "amplitude_identity": record.amplitude_status,
            "growth_rate_product": record.growth_rate_product_status,
            "module": record.module_status,
            "phase": PHASE}


# --------------------------------------------------------------------------
# Exact two-phase identities ([1G-H] Sec. 3.1)
# --------------------------------------------------------------------------

def empty_void_region_contrast(
    *, void_volume_fraction: ArrayLike, wall_density_contrast: ArrayLike,
    void_volume_contrast: ArrayLike,
) -> NDArray[np.float64]:
    """Exact global contrast of a Lagrangian region with empty voids, (H3).

    ``1/(1 + delta_L) = f_w/(1 + delta_w) + f_v/(1 + epsilon)``.  The region
    holds mass M_L, all in walls.  With the global wall density rho_w and void
    fraction f_v on the same slice, its reference wall volume is
    ``V_w0 = M_L/rho_w`` and its reference void volume ``V_v0 = V_w0 f_v/f_w``;
    ``1 + delta_w = V_w0/V_w`` and ``1 + epsilon = V_v0/V_v``.  The global mean
    density is ``f_w rho_w`` (all mass in walls), so (H1) gives (H3) exactly.
    Inputs broadcast; ``delta_w > -1`` and ``epsilon > -1``.
    """
    f_v = _real_array(void_volume_fraction, "void_volume_fraction")
    d_w = _real_array(wall_density_contrast, "wall_density_contrast")
    eps = _real_array(void_volume_contrast, "void_volume_contrast")
    if np.any((f_v <= 0.0) | (f_v >= 1.0)):
        raise GlobalVarianceContractError("void_volume_fraction must lie in (0, 1)")
    if np.any(d_w <= -1.0) or np.any(eps <= -1.0):
        raise GlobalVarianceContractError("contrasts must exceed -1")
    return _readonly(1.0 / ((1.0 - f_v) / (1.0 + d_w) + f_v / (1.0 + eps)) - 1.0)


def two_phase_region_contrast(
    *, void_volume_fraction: float, void_to_wall_density_ratio: float,
    region_void_volume_fraction: ArrayLike, region_wall_density_ratio: ArrayLike,
    region_void_density_ratio: ArrayLike,
) -> NDArray[np.float64]:
    """Exact global contrast of a region with finite-density phases, (H2).

    ``1 + delta_L = [f_w,L r_w,L + f_v,L x r_v,L]/(f_w + f_v x)``, where
    ``x = rho_v/rho_w`` is the global density ratio, ``r_w,L`` and ``r_v,L``
    are the region's phase densities over the global phase densities and
    ``f_v,L`` its void volume fraction (mass and volume additivity on the dust
    slice, [GM] Sec. 3).  ``x = 0`` is the empty-void limit.
    """
    f_v = _fraction_open(void_volume_fraction, "void_volume_fraction")
    x = _real(void_to_wall_density_ratio, "void_to_wall_density_ratio")
    if x < 0.0:
        raise GlobalVarianceContractError("void_to_wall_density_ratio must be >= 0")
    f_vL = _real_array(region_void_volume_fraction, "region_void_volume_fraction")
    r_w = _real_array(region_wall_density_ratio, "region_wall_density_ratio")
    r_v = _real_array(region_void_density_ratio, "region_void_density_ratio")
    if np.any((f_vL < 0.0) | (f_vL > 1.0)) or np.any(r_w < 0.0) or np.any(r_v < 0.0):
        raise GlobalVarianceContractError("region fractions must lie in [0, 1], ratios >= 0")
    return _readonly(((1.0 - f_vL) * r_w + f_vL * x * r_v) / ((1.0 - f_v) + f_v * x) - 1.0)


def linear_two_phase_contrast_coefficients(
    *, void_volume_fraction: float, void_to_wall_density_ratio: float,
) -> dict[str, float]:
    """First-order coefficients of (H2), (H5).

    ``delta_L = c_w delta_w + c_v delta_v + c_f delta f_v`` with
    ``c_w = f_w/(f_w + f_v x)``, ``c_v = f_v x/(f_w + f_v x)`` and
    ``c_f = -(1 - x)/(f_w + f_v x)``.  For empty voids ``c_w = 1``, ``c_v = 0``
    and ``c_f = -1/f_w``; with ``delta f_v = f_v f_w (delta_w - epsilon)`` this
    is the linearisation ``delta_L = f_w delta_w + f_v epsilon`` of (H3), (H4).
    """
    f_v = _fraction_open(void_volume_fraction, "void_volume_fraction")
    x = _real(void_to_wall_density_ratio, "void_to_wall_density_ratio")
    if x < 0.0:
        raise GlobalVarianceContractError("void_to_wall_density_ratio must be >= 0")
    f_w = 1.0 - f_v
    norm = f_w + f_v * x
    return {"wall_density": f_w / norm, "void_density": f_v * x / norm,
            "void_volume_fraction": -(1.0 - x) / norm}


def strict_flat_wall_contrast_cap(*, void_volume_fraction: float) -> float:
    """Upper bound f_v/f_w of a region's contrast with universal walls, (H13).

    With every wall at the global wall density (delta_w = 0, the flat walls of
    [GM] footnote at l. 620 read regionally) (H3) gives
    ``1/(1 + delta_L) = f_w + f_v/(1 + epsilon) > f_w``, so
    ``delta_L < f_v/f_w`` for any void volume; the bound is approached when the
    region has no voids.  Underdensities are unbounded (delta_L > -1).
    """
    f_v = _fraction_open(void_volume_fraction, "void_volume_fraction")
    return f_v / (1.0 - f_v)


# --------------------------------------------------------------------------
# Two-phase global growth on the tracker ([1G-H] Sec. 3.2)
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class LastScatteringMatching:
    """Matching epoch of the void share: an explicit dressed redshift.

    The void share is defined at the dressed redshift ``z_last_scattering``
    ([GM] text p. 25 sets the scale-factor normalisation there; 1G-D and 1G-F
    use z = 1090, a_LS = 1/1091).  The early field is the matter-era
    normalisation (D/a_photon -> 1); radiation at last scattering is neglected
    (1G-D Sec. 7 caveat).
    """

    z_last_scattering: float
    provenance: str

    def __post_init__(self) -> None:
        z = _positive(self.z_last_scattering, "z_last_scattering")
        if not z > 1.0:
            raise GlobalVarianceContractError("z_last_scattering must exceed 1")
        object.__setattr__(self, "z_last_scattering", z)
        _nonempty(self.provenance, "provenance")
        _require_strict_json(self.to_metadata(), "matching")

    def to_metadata(self) -> dict:
        return {"z_last_scattering": self.z_last_scattering, "provenance": self.provenance}


@dataclass(frozen=True, kw_only=True)
class TwoPhaseGrowthChecks:
    """Fail-closed checks of the closed forms (H8) against independent routes.

    * ``identity_tolerance``: the closed forms against the package tracker
      functions (``gamma_w``, ``fv``, ``redshift``) and the finite-t identity
      ``a_ph (t0/t)^(2/3) = gamma_w0 f_w0^(1/3)/(gamma_w f_w^(1/3))``;
    * ``ode_rtol``, ``ode_atol``: ``solve_ivp`` (DOP853) controls of the
      independent integration of the wall growing mode in common time with
      the package's regional background (H_w and rho_w from ``H_D``, ``fv``,
      ``dfv_dt``, ``rho_d``) and of the void volume ``dV/dt = 3 V/t``;
    * ``ode_cross_check_tolerance``: relative agreement of those integrations
      with D_W and D_V;
    * ``root_xtol_fraction``: absolute ``brentq`` tolerance on t_LS/t0.
    """

    identity_tolerance: float
    ode_rtol: float
    ode_atol: float
    ode_cross_check_tolerance: float
    root_xtol_fraction: float

    def __post_init__(self) -> None:
        for name in ("identity_tolerance", "ode_rtol", "ode_atol",
                     "ode_cross_check_tolerance", "root_xtol_fraction"):
            object.__setattr__(self, name, _positive(getattr(self, name), name))
        _require_strict_json(self.to_metadata(), "growth checks")

    def to_metadata(self) -> dict:
        return {"identity_tolerance": self.identity_tolerance, "ode_rtol": self.ode_rtol,
                "ode_atol": self.ode_atol,
                "ode_cross_check_tolerance": self.ode_cross_check_tolerance,
                "root_xtol_fraction": self.root_xtol_fraction,
                "ode_method": "DOP853 (scipy.integrate.solve_ivp)"}


# Named reference checks (passed explicitly; not defaults).  1e-13 is a
# round-off allowance for closed forms of O(1) quantities; the ODE controls
# (rtol 1e-11) bound the integration error well below the 1e-8 cross-check.
TWO_PHASE_GROWTH_REFERENCE_CHECKS = TwoPhaseGrowthChecks(
    identity_tolerance=1e-12,
    ode_rtol=1e-11,
    ode_atol=1e-14,
    ode_cross_check_tolerance=1e-8,
    root_xtol_fraction=1e-17,
)


@dataclass(frozen=True, kw_only=True)
class TwoPhaseGlobalGrowth:
    """The two growth factors of the global linear propagator, (H8).

    ``wall_share_growth`` D_W is the photon-normalised growth today of a unit
    early contrast carried entirely by the wall density (void volume fixed),
    ``void_share_growth`` D_V that of one carried entirely by the void volume
    (walls fixed); both relative to the matter-era normalisation
    ``D/a_photon -> 1``.  ``diagnostics`` hold the independent checks.  ``G``
    is the explicit gravitational constant of the ODE cross-check (it
    cancels).  Every result and diagnostic is recomputed from ``background``,
    ``matching``, ``checks`` and ``G`` on construction (delta audit GH-DF2).
    """

    background: TimescapeTrackerInput
    matching: LastScatteringMatching
    checks: TwoPhaseGrowthChecks
    G: float
    fv0: float
    gamma_w0: float
    t_ls_over_t0: float
    f_v_ls: float
    gamma_w_ls: float
    wall_share_growth: float
    void_share_growth: float
    diagnostics: tuple[tuple[str, float], ...]
    evidence_class: str
    assumptions: tuple[str, ...]

    def __post_init__(self) -> None:
        _require(self.background, TimescapeTrackerInput, "background")
        _require(self.matching, LastScatteringMatching, "matching")
        _require(self.checks, TwoPhaseGrowthChecks, "checks")
        for name in ("fv0", "gamma_w0", "t_ls_over_t0", "f_v_ls", "gamma_w_ls",
                     "wall_share_growth", "void_share_growth"):
            _positive(getattr(self, name), name)
        if self.fv0 != self.background.fv0:
            raise GlobalVarianceContractError("fv0 must be the background's f_v0")
        if self.evidence_class != PROPAGATOR_EVIDENCE_CLASS:
            raise GlobalVarianceContractError("evidence_class must be PROPAGATOR_EVIDENCE_CLASS")
        # Record invariants: (H8) re-evaluated from the stored inputs.
        f_w0, f_wls = 1.0 - self.fv0, 1.0 - self.f_v_ls
        d_w = self.gamma_w0 * f_w0 ** (4.0 / 3.0) / (self.gamma_w_ls * f_wls ** (4.0 / 3.0))
        d_v = self.fv0 / (self.f_v_ls * (1.0 + self.matching.z_last_scattering))
        tol = self.checks.identity_tolerance
        if not (math.isclose(self.wall_share_growth, d_w, rel_tol=tol, abs_tol=0.0)
                and math.isclose(self.void_share_growth, d_v, rel_tol=tol, abs_tol=0.0)):
            raise GlobalVarianceContractError("growth factors violate (H8)")
        if not (math.isclose(self.gamma_w0, 1.0 + self.fv0 / 2.0, rel_tol=tol, abs_tol=0.0)
                and math.isclose(self.gamma_w_ls, 1.0 + self.f_v_ls / 2.0, rel_tol=tol,
                                 abs_tol=0.0)):
            raise GlobalVarianceContractError("gamma_w must equal 1 + f_v/2 ([GM] p. 25)")
        # Tracker consistency of the matching epoch (audit GH-F9): the time
        # ratio lies in (0, 1), f_v grows with t, the one-time-scale law
        # f_v = t/(t + tau) with tau/t0 = f_w0/f_v0 links t_LS to f_v,LS, and
        # the finite-t identity (H23) links t_LS to z_LS.
        t_ratio = self.t_ls_over_t0
        if not (0.0 < t_ratio < 1.0 and 0.0 < self.f_v_ls < self.fv0 < 1.0):
            raise GlobalVarianceContractError(
                "need 0 < t_LS/t0 < 1 and 0 < f_v,LS < f_v0 < 1 (tracker ordering)")
        one_scale = t_ratio / (t_ratio + f_w0 / self.fv0)
        h23 = (t_ratio ** (-2.0 / 3.0) / (1.0 + self.matching.z_last_scattering)) / (
            self.gamma_w0 * f_w0 ** (1.0 / 3.0) / (self.gamma_w_ls * f_wls ** (1.0 / 3.0)))
        if not (math.isclose(self.f_v_ls, one_scale, rel_tol=tol, abs_tol=0.0)
                and math.isclose(h23, 1.0, rel_tol=tol, abs_tol=0.0)):
            raise GlobalVarianceContractError(
                "t_LS/t0, f_v,LS and z_LS violate the tracker identities (H23)")
        # Diagnostics: finite, non-negative, every check present and within
        # its declared tolerance.
        if not isinstance(self.diagnostics, tuple):
            raise GlobalVarianceContractError("diagnostics must be a tuple of (name, value) pairs")
        diag = {}
        for item in self.diagnostics:
            if not (isinstance(item, tuple) and len(item) == 2):
                raise GlobalVarianceContractError("diagnostics must be (name, value) pairs")
            name, value = item
            diag[_nonempty(name, "diagnostic name")] = _real(value, f"diagnostic {name}")
            if diag[name] < 0.0:
                raise GlobalVarianceContractError(f"diagnostic {name} must be non-negative")
        for name in _GROWTH_IDENTITY_DIAGNOSTICS:
            if name not in diag or not diag[name] <= tol:
                raise GlobalVarianceContractError(f"identity diagnostic {name} missing or failed")
        for name in _GROWTH_CROSS_DIAGNOSTICS:
            if name not in diag or not diag[name] <= self.checks.ode_cross_check_tolerance:
                raise GlobalVarianceContractError(f"cross-check diagnostic {name} missing or failed")
        if _strings(self.assumptions, "assumptions") != _GROWTH_ASSUMPTIONS:
            raise GlobalVarianceContractError("assumptions must be the module's growth assumptions")
        # Binding (delta audit GH-DF2): results and diagnostics recomputed.
        # G is stored as a float (second delta audit GH-D2F4).
        G = _positive(self.G, "G")
        object.__setattr__(self, "G", G)
        _bind_recomputed(self, lambda: _two_phase_growth_values(
            self.background, self.matching, self.checks, G), "growth record")
        _require_strict_json(self.to_json_dict(), "growth record")

    def to_json_dict(self) -> dict:
        return {"background": self.background.to_metadata(),
                "matching": self.matching.to_metadata(),
                "checks": self.checks.to_metadata(),
                "G_ode_cross_check": self.G,
                "fv0": self.fv0, "gamma_w0": self.gamma_w0,
                "t_ls_over_t0": self.t_ls_over_t0, "f_v_ls": self.f_v_ls,
                "gamma_w_ls": self.gamma_w_ls,
                "wall_share_growth": self.wall_share_growth,
                "void_share_growth": self.void_share_growth,
                "void_to_wall_growth_ratio": self.void_share_growth / self.wall_share_growth,
                "diagnostics": dict(self.diagnostics),
                "evidence_class": self.evidence_class,
                "assumptions": list(self.assumptions)}


_GROWTH_ASSUMPTIONS = (
    "A1-A5 (1G-C and its owner decisions): walls are Einstein-de Sitter regions in "
    "the common time t, which the wall matter clocks (A5)",
    "H-A6 void autonomy: each empty void region expands as Milne, V_v proportional "
    "to t^3, independently of the surrounding wall density; no wall-void volume "
    "transfer (1G-G G5 with J = 0)",
    "all matter in walls (empty voids, the tracker's rho_v = 0)",
    "growing modes only: the wall bang-time mode t^-1 and decaying void modes are "
    "absent (regular growing-mode initial conditions)",
    "matter-era photon normalisation at the explicit matching redshift; radiation "
    "at last scattering neglected",
)
_GROWTH_IDENTITY_DIAGNOSTICS = (
    "finite_t_photon_identity_rel", "one_time_scale_identity_rel", "redshift_root_rel",
    "gamma_w0_identity_rel", "gamma_w_ls_identity_rel")
_GROWTH_CROSS_DIAGNOSTICS = (
    "wall_share_ode_vs_closed_form_rel", "void_volume_ode_vs_package_rel",
    "void_share_ode_vs_closed_form_rel")


def _t_of_redshift(p, z: float, xtol_fraction: float) -> float:
    return brentq(lambda t: float(bg.redshift(t, p)) - z, 1e-12 * p.t0, p.t0,
                  xtol=xtol_fraction * p.t0, rtol=4.0 * np.finfo(float).eps, maxiter=500)


def _two_phase_growth_values(background: TimescapeTrackerInput,
                             matching: LastScatteringMatching,
                             checks: TwoPhaseGrowthChecks, G: float) -> dict:
    """The results and diagnostics of ``two_phase_global_growth`` (pure; GH-DF2).

    Shared by the factory and by ``TwoPhaseGlobalGrowth.__post_init__``, which
    recomputes them from the stored inputs.  Raises
    ``GlobalVarianceNumericalError`` when a check fails.
    """
    p = background.dimensionless_params()
    z_ls = matching.z_last_scattering
    t0 = p.t0
    t_ls = _t_of_redshift(p, z_ls, checks.root_xtol_fraction)
    z_check = abs(float(bg.redshift(t_ls, p)) - z_ls) / z_ls
    fv0 = p.fv0
    f_vls = float(bg.fv(t_ls, p))
    g0 = float(bg.gamma_w(t0, p))
    g_ls = float(bg.gamma_w(t_ls, p))
    f_w0, f_wls = 1.0 - fv0, 1.0 - f_vls
    d_w = g0 * f_w0 ** (4.0 / 3.0) / (g_ls * f_wls ** (4.0 / 3.0))
    d_v = fv0 / (f_vls * (1.0 + z_ls))
    # Identity checks against the tracker functions.
    finite_identity = ((t0 / t_ls) ** (2.0 / 3.0) / (1.0 + z_ls)) / (
        g0 * f_w0 ** (1.0 / 3.0) / (g_ls * f_wls ** (1.0 / 3.0))) - 1.0
    tau = t0 * (1.0 - fv0) / fv0
    one_scale = f_vls / (t_ls / (t_ls + tau)) - 1.0
    identities = {"finite_t_photon_identity_rel": abs(finite_identity),
                  "one_time_scale_identity_rel": abs(one_scale),
                  "redshift_root_rel": z_check,
                  "gamma_w0_identity_rel": abs(g0 / (1.0 + fv0 / 2.0) - 1.0),
                  "gamma_w_ls_identity_rel": abs(g_ls / (1.0 + f_vls / 2.0) - 1.0)}
    for name, value in identities.items():
        if not value <= checks.identity_tolerance:
            raise GlobalVarianceNumericalError(
                f"two-phase growth identity {name} = {value:.3e} exceeds "
                f"{checks.identity_tolerance:.3e}")

    # Independent route 1: wall growing mode in common time on the package's
    # regional background (no closed form of H_w or rho_w is used).
    def wall_rhs(t, y):
        tt = np.array([t])
        fw = 1.0 - float(bg.fv(tt, p)[0])
        h_w = float(bg.H_D(tt, p)[0]) - float(bg.dfv_dt(tt, p)[0]) / (3.0 * fw)
        four_pi_g_rho_w = 4.0 * math.pi * G * float(bg.rho_d(tt, p, G)[0]) / fw
        return [y[1], -2.0 * h_w * y[1] + four_pi_g_rho_w * y[0]]

    # Growing-mode data at t_LS: delta = 1, d delta/dt = (2/3)/t_LS (EdS in t).
    sol_w = solve_ivp(wall_rhs, (t_ls, t0), [1.0, 2.0 / (3.0 * t_ls)], method="DOP853",
                      rtol=checks.ode_rtol, atol=checks.ode_atol)
    if not sol_w.success:
        raise GlobalVarianceNumericalError(f"wall-mode integration failed: {sol_w.message}")
    d_w_ode = (f_w0 / f_wls) * float(sol_w.y[0, -1]) / (1.0 + z_ls)
    # Independent route 2: void volume dV/dt = 3V/t versus f_v a_D^3.
    sol_v = solve_ivp(lambda t, y: [3.0 * y[0] / t], (t_ls, t0), [1.0], method="DOP853",
                      rtol=checks.ode_rtol, atol=checks.ode_atol)
    if not sol_v.success:
        raise GlobalVarianceNumericalError(f"void-volume integration failed: {sol_v.message}")
    vol_ratio_pkg = (fv0 * float(bg.a_D(t0, p)) ** 3) / (f_vls * float(bg.a_D(t_ls, p)) ** 3)
    domain_ratio = (float(bg.a_D(t0, p)) / float(bg.a_D(t_ls, p))) ** 3
    # V_v(t0)/V_v(LS) / [V_D(t0)/V_D(LS)] = f_v0/f_v,LS, so D_V = that/(1 + z_LS).
    d_v_ode = float(sol_v.y[0, -1]) / domain_ratio / (1.0 + z_ls)
    cross = {"wall_share_ode_vs_closed_form_rel": abs(d_w_ode / d_w - 1.0),
             "void_volume_ode_vs_package_rel": abs(float(sol_v.y[0, -1]) / vol_ratio_pkg - 1.0),
             "void_share_ode_vs_closed_form_rel": abs(d_v_ode / d_v - 1.0)}
    for name, value in cross.items():
        if not value <= checks.ode_cross_check_tolerance:
            raise GlobalVarianceNumericalError(
                f"two-phase growth cross-check {name} = {value:.3e} exceeds "
                f"{checks.ode_cross_check_tolerance:.3e}")
    diagnostics = tuple((k, float(v)) for k, v in {**identities, **cross}.items()) + (
        ("wall_ode_nfev", float(sol_w.nfev)), ("void_ode_nfev", float(sol_v.nfev)))
    return {"fv0": fv0, "gamma_w0": g0, "t_ls_over_t0": t_ls / t0, "f_v_ls": f_vls,
            "gamma_w_ls": g_ls, "wall_share_growth": d_w, "void_share_growth": d_v,
            "diagnostics": diagnostics}


def two_phase_global_growth(
    *, background: TimescapeTrackerInput, matching: LastScatteringMatching,
    checks: TwoPhaseGrowthChecks, G: float,
) -> TwoPhaseGlobalGrowth:
    """D_W and D_V of the tracker, (H8), with fail-closed independent checks.

    Closed forms from [GM] Eqs. (5.4)-(5.6) and text p. 25:
    ``(t0/t)^(2/3)/(1 + z) = gamma_w0 f_w0^(1/3)/(gamma_w(t) f_w(t)^(1/3))``
    (``1 + z = gamma_w a_w0/a_D``, ``a_D proportional to t f_v^(-1/3)``,
    ``f_v = t/(t + tau)``), hence ``D_W = (f_w0/f_w,LS)(t0/t_LS)^(2/3)/(1+z_LS)``
    and ``D_V = (f_v0/f_v,LS)/(1 + z_LS)`` (H7)-(H8).  Independent checks: the
    wall growing mode integrated in common time on the package's regional
    background ``H_w = H_D - dfv_dt/(3 f_w)``, ``4 pi G rho_w = 4 pi G <rho>_D/f_w``
    (1G-C Sec. 5), and the void volume ``dV/dt = 3V/t`` against ``f_v a_D^3``.
    ``G`` is explicit (it cancels; no default).
    """
    _require(background, TimescapeTrackerInput, "background")
    _require(matching, LastScatteringMatching, "matching")
    _require(checks, TwoPhaseGrowthChecks, "checks")
    G = _positive(G, "G")
    return TwoPhaseGlobalGrowth(
        background=background, matching=matching, checks=checks, G=G,
        **_two_phase_growth_values(background, matching, checks, G),
        evidence_class=PROPAGATOR_EVIDENCE_CLASS, assumptions=_GROWTH_ASSUMPTIONS)


# --------------------------------------------------------------------------
# Void-share closures ([1G-H] Sec. 4)
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class ConstantVoidShare:
    """Explicit scale-independent void share p (closure; no default).

    p is the fraction of a region's early (matching-epoch) linear contrast
    carried by its void-volume deficit, ``p = f_v,LS epsilon/delta_L(LS)``
    ([1G-H] (H7)), equivalently ``p = f_v,LS - d f_v,L/d delta_L`` for the
    region's void volume fraction f_v,L.  The accepted range is ``[0, 1]``:
    ``p = 0`` is 1G-D's wall-curvature mode (just below the monotone class
    H-A7, ``f_v,LS <= p <= 1``), ``p = 1`` the strict flat-wall reading.
    ``evidence_class`` records the status of the supplied value.
    """

    share: float
    provenance: str
    evidence_class: str

    def __post_init__(self) -> None:
        p = _real(self.share, "share")
        if not 0.0 <= p <= 1.0:
            raise GlobalVarianceContractError(
                "share must lie in [0, 1] (monotone response class H-A7)")
        object.__setattr__(self, "share", p)
        _nonempty(self.provenance, "provenance")
        _nonempty(self.evidence_class, "evidence_class")
        _require_strict_json(self.to_metadata(), "constant void share")

    def to_metadata(self) -> dict:
        return {"closure": "constant_void_share", "share": self.share,
                "provenance": self.provenance, "evidence_class": self.evidence_class,
                "status": VOID_SHARE_STATUS}


@dataclass(frozen=True, kw_only=True)
class GaussianThresholdSeedVoidShare:
    """Peak-background split of Gaussian-threshold void seeds, (H12).

    Seeds are the regions of the matching-epoch linear field, smoothed with a
    Lagrangian top hat of ``seed_radius_Mpc`` (photon-normalised comoving),
    below ``-nu sigma_s``, with ``Phi(-nu) = f_v,LS`` (the tracker's own void
    fraction, 1G-D owner decision GD-OD2).  A mode k shifts the threshold by
    ``W(k R_s) delta``, so ``delta ln f_v,LS = -[phi(nu)/(sigma_s Phi(-nu))]
    W(k R_s) delta`` ([1G-D] Sec. 7 for k -> 0).  ``compression`` states
    whether the seed volume is also compressed with its region
    (``SeedVolumeCompression``).  The seed radius is an explicit input with
    its provenance (1G-D's tracker-consistent primary is
    ``tracker_consistent_seed_radius``).
    """

    seed_radius_Mpc: float
    seed_radius_provenance: str
    compression: SeedVolumeCompression

    def __post_init__(self) -> None:
        object.__setattr__(self, "seed_radius_Mpc",
                           _positive(self.seed_radius_Mpc, "seed_radius_Mpc"))
        _nonempty(self.seed_radius_provenance, "seed_radius_provenance")
        _require_enum(self.compression, SeedVolumeCompression, "compression")
        _require_strict_json(self.to_metadata(), "seed void share")

    def to_metadata(self) -> dict:
        return {"closure": "gaussian_threshold_seed_peak_background_split",
                "seed_radius_Mpc": self.seed_radius_Mpc,
                "seed_radius_provenance": self.seed_radius_provenance,
                "compression": self.compression.value, "status": VOID_SHARE_STATUS}


def tracker_consistent_seed_radius(
    *, present_void_radius_volume_average_proper_Mpc: float, f_v_seed: float,
    fv0: float, gamma_w0: float,
) -> float:
    """1G-D's tracker-consistent seed radius (owner decision GD-OD1).

    ``R_s = R_void (f_v,seed/f_v0)^(1/3)/gamma_w0``: the void domain is a fixed
    set of fluid elements whose a_D-comoving radius grows by
    ``(f_v0/f_v,seed)^(1/3)``; photon-normalised comoving lengths are a_D
    lengths over ``gamma_w0`` ([GM] Eq. (5.4)).  The present void radius is an
    explicit input (1G-D uses [W09] l. 277, 15 h^-1 Mpc with the dressed h).
    """
    r = _positive(present_void_radius_volume_average_proper_Mpc,
                  "present_void_radius_volume_average_proper_Mpc")
    fs = _fraction_open(f_v_seed, "f_v_seed")
    f0 = _fraction_open(fv0, "fv0")
    g0 = _positive(gamma_w0, "gamma_w0")
    return r * (fs / f0) ** (1.0 / 3.0) / g0


@dataclass(frozen=True, kw_only=True)
class EvaluatedVoidShare:
    """A void-share closure evaluated for one background and early spectrum.

    ``share_k0`` is p at k -> 0; ``kind`` names the closure.  For the Gaussian
    threshold: ``nu``, ``sigma_seed`` (rms of the seed-scale field at the
    matching epoch), ``threshold_share_k0 = phi(nu)/sigma_s`` and the
    compression term (``f_v,LS`` or 0); ``void_onset_response`` is 1G-D's
    threshold response ``A_v = phi(nu)/(sigma_s Phi(-nu))``, so that
    ``share_k0 = f_v,LS (1 + A_v)`` with compression and ``f_v,LS A_v``
    without.  Every field is validated against the closure variant and the
    growth record (audit GH-F9); inapplicable fields are ``NOT_APPLICABLE``.
    ``density``, ``early_spectrum`` and ``seed_quadrature`` are the inputs of
    the evaluation (``seed_quadrature`` is ``NOT_APPLICABLE`` for a constant
    share); every result is recomputed from them on construction (delta audit
    GH-DF2).
    """

    closure: ConstantVoidShare | GaussianThresholdSeedVoidShare
    growth: TwoPhaseGlobalGrowth
    density: EarlyMatterDensityPerPhoton
    early_spectrum: EarlySpectrumImport
    seed_quadrature: LagrangianSigmaQuadrature | str
    kind: str
    share_k0: float
    nu: float | str
    sigma_seed: float | str
    threshold_share_k0: float | str
    compression_share: float | str
    void_onset_response: float | str

    def __post_init__(self) -> None:
        _require(self.growth, TwoPhaseGlobalGrowth, "growth")
        _require(self.density, EarlyMatterDensityPerPhoton, "density")
        _require(self.early_spectrum, EarlySpectrumImport, "early_spectrum")
        if self.density.background is not self.growth.background:
            raise GlobalVarianceContractError("density and growth must share the background object")
        if not isinstance(self.closure, (ConstantVoidShare, GaussianThresholdSeedVoidShare)):
            raise GlobalVarianceContractError("unsupported void-share closure")
        p0 = _real(self.share_k0, "share_k0")
        if not 0.0 <= p0 <= 1.0:
            raise GlobalVarianceContractError(
                f"void share {p0!r} lies outside [0, 1] (monotone class H-A7)")
        variant_fields = ("nu", "sigma_seed", "threshold_share_k0", "compression_share",
                          "void_onset_response")
        if isinstance(self.closure, ConstantVoidShare):
            if self.kind != "constant":
                raise GlobalVarianceContractError("kind must be 'constant' for a constant share")
            if p0 != self.closure.share:
                raise GlobalVarianceContractError("share_k0 must equal the closure's share")
            for name in variant_fields:
                if getattr(self, name) != NOT_APPLICABLE:
                    raise GlobalVarianceContractError(f"{name} must be NOT_APPLICABLE")
        else:
            if self.kind != "gaussian_threshold_seed":
                raise GlobalVarianceContractError("kind must be 'gaussian_threshold_seed'")
            values = {name: _real(getattr(self, name), name) for name in variant_fields}
            sigma_s = values["sigma_seed"]
            if not sigma_s > 0.0:
                raise GlobalVarianceContractError("sigma_seed must be positive")
            f_vls = self.growth.f_v_ls
            nu = -float(ndtri(f_vls))
            phi_nu = math.exp(-0.5 * nu * nu) / math.sqrt(2.0 * math.pi)
            compression = (f_vls if self.closure.compression
                           is SeedVolumeCompression.COMPRESSED_WITH_REGION else 0.0)
            if not (_close(values["nu"], nu)
                    and _close(values["threshold_share_k0"], phi_nu / sigma_s)
                    and values["compression_share"] == compression
                    and _close(p0, compression + values["threshold_share_k0"])
                    and _close(values["void_onset_response"],
                               phi_nu / (sigma_s * float(ndtr(-nu))))):
                raise GlobalVarianceContractError(
                    "Gaussian-threshold fields are inconsistent with (H12) and the growth record")
        # Binding (delta audit GH-DF2): sigma_s and every derived field
        # recomputed from the closure, growth, density, spectrum and quadrature.
        _bind_recomputed(self, lambda: _void_share_values(
            self.closure, self.growth, self.density, self.early_spectrum,
            self.seed_quadrature), "void share")
        _require_strict_json(self.to_json_dict(), "void share")

    def share(self, k_per_Mpc: ArrayLike) -> NDArray[np.float64]:
        """p(k), read-only; k in Mpc^-1 (photon-normalised comoving).

        For the Gaussian threshold p(k) follows the top-hat window of the seed
        scale; its side lobes make p(k) slightly negative near k R_s = 5.8
        (min W = -0.086).  It is a response kernel; the monotone class
        constrains its k -> 0 value only.
        """
        k = _real_array(k_per_Mpc, "k_per_Mpc")
        if np.any(k < 0.0):
            raise GlobalVarianceContractError("k_per_Mpc must be non-negative")
        if isinstance(self.closure, ConstantVoidShare):
            return _readonly(np.full_like(k, self.share_k0))
        w = top_hat_window(x=k * self.closure.seed_radius_Mpc)
        return _readonly(self.compression_share + self.threshold_share_k0 * w)

    def to_json_dict(self) -> dict:
        seed_quadrature = (self.seed_quadrature.to_metadata()
                           if isinstance(self.seed_quadrature, LagrangianSigmaQuadrature)
                           else self.seed_quadrature)
        return {"closure": self.closure.to_metadata(), "kind": self.kind,
                "seed_quadrature": seed_quadrature,
                "share_k0": self.share_k0, "nu": self.nu, "sigma_seed": self.sigma_seed,
                "threshold_share_k0": self.threshold_share_k0,
                "compression_share": self.compression_share,
                "void_onset_response": self.void_onset_response}


def _unit_sigma(radius_Mpc: float, omega_m: float, early_spectrum: EarlySpectrumImport,
                quadrature: LagrangianSigmaQuadrature, kernel=None):
    """sqrt(int dln k Delta^2_u G^2 W^2) on two grids with fail-closed checks."""
    values = []
    edge_fraction = 0.0
    for n in (quadrature.grid_points, quadrature.comparison_grid_points):
        lnk = np.linspace(math.log(quadrature.k_min_per_Mpc),
                          math.log(quadrature.k_max_per_Mpc), n)
        k = np.exp(lnk)
        amp = np.asarray(matter_era_linear_amplitude(
            k_per_Mpc=k, early_spectrum=early_spectrum, omega_m=omega_m,
            growth_today_photon_normalised=1.0))
        g2 = 1.0 if kernel is None else np.asarray(kernel(k)) ** 2
        integrand = amp * g2 * np.asarray(top_hat_window(x=k * radius_Mpc)) ** 2
        if not np.any(integrand):        # an identically vanishing kernel (e.g. p = 0)
            return 0.0, 0.0, 0.0, 0.0
        values.append(math.sqrt(float(simpson(integrand, x=lnk))))
        if n == quadrature.grid_points:
            x_ends = np.array([k[0], k[-1]]) * radius_Mpc
            envelope = np.minimum(1.0, 3.0 / x_ends ** 2 + 3.0 / x_ends ** 3) ** 2
            g2_ends = np.array([1.0, 1.0]) if kernel is None else (
                np.asarray(kernel(np.array([k[0], k[-1]]))) ** 2)
            edge = float(np.max(np.array([amp[0], amp[-1]]) * g2_ends * envelope))
            edge_fraction = edge / float(np.max(integrand))
    fine, coarse = values
    change = abs(fine / coarse - 1.0)
    if not change <= quadrature.self_convergence_tolerance:
        raise GlobalVarianceNumericalError(
            f"variance quadrature not converged at R = {radius_Mpc:.6g} Mpc: relative "
            f"change {change:.3e} exceeds {quadrature.self_convergence_tolerance:.3e}")
    if not edge_fraction <= quadrature.truncation_tolerance:
        raise GlobalVarianceNumericalError(
            f"k range truncates the integrand at R = {radius_Mpc:.6g} Mpc: end envelope "
            f"fraction {edge_fraction:.3e} exceeds {quadrature.truncation_tolerance:.3e}")
    return fine, coarse, change, edge_fraction


def unit_growth_lagrangian_sigma(
    *, radius_Mpc: float, omega_m: float, early_spectrum: EarlySpectrumImport,
    quadrature: LagrangianSigmaQuadrature,
) -> float:
    """sigma_u(R): (H10) with G = 1, the photon-normalised early rms at unit growth.

    The same quadrature (with its fail-closed convergence and truncation
    checks) as every variance of this module; ``matter_era_linear_amplitude``
    and ``top_hat_window`` of ``lagrangian_sigma`` ([1G-A] Sec. 6.3, 1D-A D5).
    """
    R = _positive(radius_Mpc, "radius_Mpc")
    om = _positive(omega_m, "omega_m")
    _require(early_spectrum, EarlySpectrumImport, "early_spectrum")
    _require(quadrature, LagrangianSigmaQuadrature, "quadrature")
    return _unit_sigma(R, om, early_spectrum, quadrature)[0]


def evaluate_void_share(
    *, closure: ConstantVoidShare | GaussianThresholdSeedVoidShare,
    growth: TwoPhaseGlobalGrowth, density: EarlyMatterDensityPerPhoton,
    early_spectrum: EarlySpectrumImport,
    seed_quadrature: LagrangianSigmaQuadrature | str,
) -> EvaluatedVoidShare:
    """Evaluate a void-share closure, (H12) for the Gaussian threshold.

    ``sigma_s = sigma_u(R_s)/(1 + z_LS)`` is the seed-scale rms at the
    matching epoch in the matter-era normalisation, ``nu = -Phi^-1(f_v,LS)``,
    ``p(k) = c + phi(nu) W(k R_s)/sigma_s`` with ``c = f_v,LS`` for
    ``COMPRESSED_WITH_REGION`` and 0 otherwise; ``A_v = phi(nu)/(sigma_s
    Phi(-nu))`` is 1G-D's void-onset response.  The share at k -> 0 must lie
    in the monotone class (H-A7), else the closure is refused.
    ``seed_quadrature`` integrates sigma_u at the (small) seed radius; it is
    ``NOT_APPLICABLE`` for a constant share.
    """
    _require(growth, TwoPhaseGlobalGrowth, "growth")
    _require(density, EarlyMatterDensityPerPhoton, "density")
    _require(early_spectrum, EarlySpectrumImport, "early_spectrum")
    if density.background is not growth.background:
        raise GlobalVarianceContractError("density and growth must share the background object")
    return EvaluatedVoidShare(
        closure=closure, growth=growth, density=density, early_spectrum=early_spectrum,
        seed_quadrature=seed_quadrature,
        **_void_share_values(closure, growth, density, early_spectrum, seed_quadrature))


def _void_share_values(closure, growth: TwoPhaseGlobalGrowth,
                       density: EarlyMatterDensityPerPhoton,
                       early_spectrum: EarlySpectrumImport, seed_quadrature) -> dict:
    """The fields of ``evaluate_void_share``, (H12) (pure; shared with the record, GH-DF2)."""
    na = NOT_APPLICABLE
    if isinstance(closure, ConstantVoidShare):
        if seed_quadrature != NOT_APPLICABLE:
            raise GlobalVarianceContractError(
                "seed_quadrature does not apply to a constant share; pass NOT_APPLICABLE")
        return {"kind": "constant", "share_k0": closure.share, "nu": na, "sigma_seed": na,
                "threshold_share_k0": na, "compression_share": na, "void_onset_response": na}
    if not isinstance(closure, GaussianThresholdSeedVoidShare):
        raise GlobalVarianceContractError("unsupported void-share closure")
    _require(seed_quadrature, LagrangianSigmaQuadrature, "seed_quadrature")
    sigma_u_seed = _unit_sigma(closure.seed_radius_Mpc, density.omega_m_per_photon,
                               early_spectrum, seed_quadrature)[0]
    sigma_s = sigma_u_seed / (1.0 + growth.matching.z_last_scattering)
    f_vls = growth.f_v_ls
    nu = -float(ndtri(f_vls))
    phi_nu = math.exp(-0.5 * nu * nu) / math.sqrt(2.0 * math.pi)
    threshold = phi_nu / sigma_s
    compression = (f_vls if closure.compression is SeedVolumeCompression.COMPRESSED_WITH_REGION
                   else 0.0)
    p0 = compression + threshold
    if not p0 <= 1.0:
        raise GlobalVarianceContractError(
            f"Gaussian-threshold void share p0 = {p0:.4g} exceeds 1: outside the monotone "
            "class H-A7 (walls would be underdense in overdense regions)")
    return {"kind": "gaussian_threshold_seed", "share_k0": p0, "nu": nu, "sigma_seed": sigma_s,
            "threshold_share_k0": threshold, "compression_share": compression,
            "void_onset_response": phi_nu / (sigma_s * float(ndtr(-nu)))}


def global_linear_propagator(
    *, growth: TwoPhaseGlobalGrowth, void_share: EvaluatedVoidShare, k_per_Mpc: ArrayLike,
) -> NDArray[np.float64]:
    """G(k, t0) = (1 - p(k)) D_W + p(k) D_V, (H9); photon-normalised, read-only."""
    _require(growth, TwoPhaseGlobalGrowth, "growth")
    _require(void_share, EvaluatedVoidShare, "void_share")
    if void_share.growth is not growth:
        raise GlobalVarianceContractError("void_share must be evaluated for this growth record")
    p = np.asarray(void_share.share(k_per_Mpc))
    return _readonly((1.0 - p) * growth.wall_share_growth + p * growth.void_share_growth)


# --------------------------------------------------------------------------
# The conditional global-mean linear statistic ([1G-H] Sec. 2, (H10))
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class ConditionalGlobalLinearSigma:
    """Conditional global-mean linear rms at one Lagrangian radius, (H10).

    ``linear_sigma`` is (H10) with the propagator (H9) of ``void_share``;
    ``unit_growth_sigma`` the same integral with G = 1; ``propagator_k0`` is
    G(k -> 0); ``effective_propagator = linear_sigma/unit_growth_sigma``.
    ``wall_share_rms`` and ``void_share_rms`` are the rms of the two terms of
    (H9); both are driven by the same early mode, so they add coherently:
    ``share_terms_coherence`` is ``(sigma^2 - W^2 - V^2)/(2 W V)``, exactly 1
    for a scale-independent share (``NOT_APPLICABLE`` if a term vanishes).
    ``void_volume_response_rms`` is the rms of epsilon over the region,
    ``[(1 + z_LS) f_v,LS]^-1 (int Delta^2_u p^2 W^2)^(1/2)`` (H14), with its
    regime flag.  ``flat_wall_capacity_ratio`` is the matching-epoch rms
    contrast over the strict flat-wall cap (H13).  On construction the radius
    is re-resolved from its specification and every result and quadrature
    diagnostic is recomputed from the stored growth, void share, density,
    early spectrum and quadrature (delta audit GH-DF2).  Not an observational
    amplitude.
    """

    background: TimescapeTrackerInput
    growth: TwoPhaseGlobalGrowth
    void_share: EvaluatedVoidShare
    density: EarlyMatterDensityPerPhoton
    radius: ResolvedLagrangianRadius
    early_spectrum: EarlySpectrumImport
    quadrature: LagrangianSigmaQuadrature
    unit_growth_sigma: float
    linear_sigma: float
    linear_sigma_comparison_grid: float
    quadrature_relative_change: float
    truncation_envelope_fraction: float
    propagator_k0: float
    effective_propagator: float
    wall_share_rms: float
    void_share_rms: float
    share_terms_coherence: float | str
    void_volume_response_rms: float
    void_response_regime: str
    flat_wall_capacity_ratio: float
    caveats: tuple[str, ...]
    classification: str
    observational_status: str
    amplitude_status: str
    growth_rate_product_status: str
    module_status: str

    def __post_init__(self) -> None:
        for name, cls in (("background", TimescapeTrackerInput), ("growth", TwoPhaseGlobalGrowth),
                          ("void_share", EvaluatedVoidShare),
                          ("density", EarlyMatterDensityPerPhoton),
                          ("radius", ResolvedLagrangianRadius),
                          ("early_spectrum", EarlySpectrumImport),
                          ("quadrature", LagrangianSigmaQuadrature)):
            _require(getattr(self, name), cls, name)
        if self.growth.background is not self.background or self.density.background is not self.background:
            raise GlobalVarianceContractError("records must share this exact background object")
        if self.void_share.growth is not self.growth:
            raise GlobalVarianceContractError("void_share must be evaluated for this growth record")
        if (self.void_share.density is not self.density
                or self.void_share.early_spectrum is not self.early_spectrum):
            raise GlobalVarianceContractError(
                "void_share must be evaluated with this record's density and early spectrum")
        for name in ("unit_growth_sigma", "linear_sigma", "linear_sigma_comparison_grid",
                     "propagator_k0", "effective_propagator", "flat_wall_capacity_ratio"):
            _positive(getattr(self, name), name)
        for name in ("quadrature_relative_change", "truncation_envelope_fraction",
                     "wall_share_rms", "void_share_rms", "void_volume_response_rms"):
            if _real(getattr(self, name), name) < 0.0:
                raise GlobalVarianceContractError(f"{name} must be non-negative")
        if self.effective_propagator != self.linear_sigma / self.unit_growth_sigma:
            raise GlobalVarianceContractError("effective_propagator must be the ratio")
        # Record invariants re-evaluated from the stored fields (audit GH-F9).
        if not (self.quadrature_relative_change
                == abs(self.linear_sigma / self.linear_sigma_comparison_grid - 1.0)
                and self.quadrature_relative_change <= self.quadrature.self_convergence_tolerance
                and self.truncation_envelope_fraction <= self.quadrature.truncation_tolerance):
            raise GlobalVarianceContractError("quadrature diagnostics are inconsistent or failed")
        p0 = float(np.asarray(self.void_share.share(np.array([0.0])))[0])
        d_w, d_v = self.growth.wall_share_growth, self.growth.void_share_growth
        if not _close(self.propagator_k0, (1.0 - p0) * d_w + p0 * d_v):
            raise GlobalVarianceContractError("propagator_k0 violates (H9) at k -> 0")
        z_ls = self.growth.matching.z_last_scattering
        capacity = (self.unit_growth_sigma / (1.0 + z_ls)) / strict_flat_wall_contrast_cap(
            void_volume_fraction=self.growth.f_v_ls)
        if not _close(self.flat_wall_capacity_ratio, capacity):
            raise GlobalVarianceContractError("flat_wall_capacity_ratio violates (H13)")
        expected_regime = (VOID_RESPONSE_NONPERTURBATIVE
                           if self.void_volume_response_rms > VOID_RESPONSE_NONPERTURBATIVE_THRESHOLD
                           else VOID_RESPONSE_PERTURBATIVE)
        if self.void_response_regime != expected_regime:
            raise GlobalVarianceContractError("void_response_regime is inconsistent")
        # Minkowski bounds for the two terms of (H9), and their coherence.
        w_rms, v_rms = self.wall_share_rms, self.void_share_rms
        slack = 1e-10 * (w_rms + v_rms)
        if not abs(w_rms - v_rms) - slack <= self.linear_sigma <= w_rms + v_rms + slack:
            raise GlobalVarianceContractError("the (H9) terms violate the Minkowski bounds")
        if w_rms > 0.0 and v_rms > 0.0:
            expected = (self.linear_sigma ** 2 - w_rms ** 2 - v_rms ** 2) / (2.0 * w_rms * v_rms)
            if self.share_terms_coherence != expected:
                raise GlobalVarianceContractError("share_terms_coherence is inconsistent")
        elif self.share_terms_coherence != NOT_APPLICABLE:
            raise GlobalVarianceContractError("share_terms_coherence must be NOT_APPLICABLE")
        if _strings(self.caveats, "caveats") != _GLOBAL_CAVEATS:
            raise GlobalVarianceContractError("caveats must be the module's declared caveats")
        _statuses_ok(self)
        # Binding (delta audit GH-DF2): the radius is re-resolved from its
        # specification and every result and quadrature diagnostic recomputed
        # from the stored growth, share, density, spectrum and quadrature.
        if resolve_lagrangian_radius(spec=self.radius.spec, density=self.density) != self.radius:
            raise GlobalVarianceContractError(
                "radius differs from the resolution of its specification for this density")
        _bind_recomputed(self, lambda: _global_sigma_values(
            self.growth, self.void_share, self.density.omega_m_per_photon,
            self.radius.radius_Mpc, self.early_spectrum, self.quadrature), "sigma record")
        _require_strict_json(self.to_json_dict(), "sigma record")

    def to_json_dict(self) -> dict:
        return {
            "quantity_label": "conditional_global_mean_linear_rms_lagrangian_top_hat",
            "status": _status_json(self),
            "frames": {"field": "dust rest-mass density on the dust-orthogonal foliation",
                       "mean": "global Buchert volume average on the same slice",
                       "time": "dust proper time t (common time), present epoch t0",
                       "radius": "photon_normalised_comoving_Mpc (Lagrangian top hat)",
                       "linear_order": "formal zero-amplitude tangent of the regional contrast "
                                       "map around the smooth two-phase tracker state, applied "
                                       "to the early Gaussian field (linear extrapolation); "
                                       "smoothing rule G_R(k) = G(k) W(kR); not the "
                                       "ensemble-mean response of the true contrast",
                       "void_accounting": "seed-indexed (H-A9): bubbles assigned to the region "
                                          "containing their seed; equals the material-domain "
                                          "volume only with scale separation"},
            "background": self.background.to_metadata(),
            "growth": self.growth.to_json_dict(),
            "void_share": self.void_share.to_json_dict(),
            "radius": self.radius.to_json_dict(),
            "early_spectrum": self.early_spectrum.to_metadata(),
            "quadrature": {"config": self.quadrature.to_metadata(),
                           "relative_change": self.quadrature_relative_change,
                           "truncation_envelope_fraction": self.truncation_envelope_fraction,
                           "comparison_grid_value": self.linear_sigma_comparison_grid},
            "omega_m_per_photon": self.density.omega_m_per_photon,
            "unit_growth_sigma": self.unit_growth_sigma,
            "propagator_k0": self.propagator_k0,
            "effective_propagator": self.effective_propagator,
            "linear_sigma": self.linear_sigma,
            "wall_share_rms": self.wall_share_rms,
            "void_share_rms": self.void_share_rms,
            "share_terms_coherence": self.share_terms_coherence,
            "void_volume_response_rms": self.void_volume_response_rms,
            "void_response_regime": self.void_response_regime,
            "flat_wall_capacity_ratio": self.flat_wall_capacity_ratio,
            "caveats": list(self.caveats),
        }


_GLOBAL_CAVEATS = (
    "conditional, model-internal global-mean linear statistic; not an observational "
    "amplitude, not comparable with survey or CMB values without a Timescape reduction",
    "the void share p(k) is an external closure (VOID_ONSET_RESPONSE = "
    "EXTERNAL_CLOSURE_INPUT); the value is conditional on it",
    "linear means the formal zero-amplitude tangent (linear extrapolation) around the "
    "smooth two-phase tracker state, a proposed definition (owner decision D1, "
    "2026-10-07); it is not the ensemble-mean response of the true region contrast and "
    "ignores the zeroth-order partition fluctuations on the region scale",
    "when the void-volume response rms exceeds 1 the linear void response is applied "
    "beyond its declared validity (H-A8, formal extrapolation); below 1 no controlled "
    "truncation error is established either",
    "seed-indexed void accounting H-A9: equal to the material-domain volume only with "
    "scale separation (void radius much smaller than the region radius)",
    "regional laws A1-A5 and void autonomy H-A6 assumed; the regional embedding stays "
    "NOT_DERIVED",
    "early spectrum is a PROVISIONAL_MODEL_IMPORT; the radius identification is "
    "CONVENTION_DEPENDENT",
)


def conditional_global_linear_sigma(
    *,
    background: TimescapeTrackerInput,
    matching: LastScatteringMatching,
    growth_checks: TwoPhaseGrowthChecks,
    void_share_closure: ConstantVoidShare | GaussianThresholdSeedVoidShare,
    early_spectrum: EarlySpectrumImport,
    radius: LagrangianRadiusSpec,
    quadrature: LagrangianSigmaQuadrature,
    seed_quadrature: LagrangianSigmaQuadrature | str,
    density_identity_tolerance: float,
    G: float,
) -> ConditionalGlobalLinearSigma:
    """Conditional global-mean linear rms in a Lagrangian top hat, (H10).

    Chain: tracker -> D_W, D_V (H8) -> explicit void share p(k) (closure) ->
    propagator (H9) -> omega_m,eff and radius convention ([1G-A] Sec. 6, via
    ``lagrangian_sigma``) -> early spectrum (EH98 import) -> (H10).  Every
    argument is mandatory and keyword-only; nothing has a default.
    """
    _require(background, TimescapeTrackerInput, "background")
    _require(radius, LagrangianRadiusSpec, "radius")
    growth = two_phase_global_growth(background=background, matching=matching,
                                     checks=growth_checks, G=G)
    density = early_matter_density_per_photon(
        background=background, identity_tolerance=density_identity_tolerance, G=G)
    share = evaluate_void_share(closure=void_share_closure, growth=growth, density=density,
                                early_spectrum=early_spectrum, seed_quadrature=seed_quadrature)
    _require(quadrature, LagrangianSigmaQuadrature, "quadrature")
    resolved = resolve_lagrangian_radius(spec=radius, density=density)
    return ConditionalGlobalLinearSigma(
        background=background, growth=growth, void_share=share, density=density,
        radius=resolved, early_spectrum=early_spectrum, quadrature=quadrature,
        **_global_sigma_values(growth, share, density.omega_m_per_photon, resolved.radius_Mpc,
                               early_spectrum, quadrature),
        caveats=_GLOBAL_CAVEATS, **_STATUS_FIELDS)


def _global_sigma_values(growth: TwoPhaseGlobalGrowth, share: EvaluatedVoidShare,
                         om: float, R: float, early_spectrum: EarlySpectrumImport,
                         quadrature: LagrangianSigmaQuadrature) -> dict:
    """The results of ``conditional_global_linear_sigma``, (H9)-(H14) (pure; GH-DF2).

    Shared by the factory and by ``ConditionalGlobalLinearSigma.__post_init__``,
    which recomputes them from the stored inputs.
    """
    def propagator(k):
        return global_linear_propagator(growth=growth, void_share=share, k_per_Mpc=k)

    fine, coarse, change, edge = _unit_sigma(R, om, early_spectrum, quadrature, propagator)
    unit = _unit_sigma(R, om, early_spectrum, quadrature)[0]
    d_w, d_v = growth.wall_share_growth, growth.void_share_growth

    def wall_part(k):
        return (1.0 - np.asarray(share.share(k))) * d_w

    def void_part(k):
        return np.asarray(share.share(k)) * d_v

    def share_kernel(k):
        return np.asarray(share.share(k))

    wall_rms = _unit_sigma(R, om, early_spectrum, quadrature, wall_part)[0]
    void_rms = _unit_sigma(R, om, early_spectrum, quadrature, void_part)[0]
    share_rms = _unit_sigma(R, om, early_spectrum, quadrature, share_kernel)[0]
    z_ls = growth.matching.z_last_scattering
    eps_rms = share_rms / ((1.0 + z_ls) * growth.f_v_ls)
    regime = (VOID_RESPONSE_NONPERTURBATIVE if eps_rms > VOID_RESPONSE_NONPERTURBATIVE_THRESHOLD
              else VOID_RESPONSE_PERTURBATIVE)
    capacity = (unit / (1.0 + z_ls)) / strict_flat_wall_contrast_cap(
        void_volume_fraction=growth.f_v_ls)
    p0 = float(np.asarray(share.share(np.array([0.0])))[0])
    coherence = (((fine ** 2 - wall_rms ** 2 - void_rms ** 2) / (2.0 * wall_rms * void_rms))
                 if wall_rms > 0.0 and void_rms > 0.0 else NOT_APPLICABLE)
    return {"unit_growth_sigma": unit, "linear_sigma": fine,
            "linear_sigma_comparison_grid": coarse, "quadrature_relative_change": change,
            "truncation_envelope_fraction": edge,
            "propagator_k0": (1.0 - p0) * d_w + p0 * d_v, "effective_propagator": fine / unit,
            "wall_share_rms": wall_rms, "void_share_rms": void_rms,
            "share_terms_coherence": coherence, "void_volume_response_rms": eps_rms,
            "void_response_regime": regime, "flat_wall_capacity_ratio": capacity}


# --------------------------------------------------------------------------
# Constant-share interval ([1G-H] Sec. 5, (H15))
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class HomogeneityPremise:
    """The background's homogeneity premise as an explicit bound.

    The global-mean linear rms in the Lagrangian top hat of radius
    ``radius`` (an explicit convention) does not exceed ``max_linear_rms``.
    [W09] ll. 327-335 and 455-458: the statistical-homogeneity scale,
    "100 h^-1 Mpc or somewhat larger", is "a scale above which the variance in
    density contrasts is bounded at the 10% level".  The reading of that
    sentence (sphere radius or cell side, rms or variance, h) is the caller's
    explicit choice, recorded in ``provenance``.
    """

    radius: LagrangianRadiusSpec
    max_linear_rms: float
    provenance: str

    def __post_init__(self) -> None:
        _require(self.radius, LagrangianRadiusSpec, "radius")
        object.__setattr__(self, "max_linear_rms",
                           _positive(self.max_linear_rms, "max_linear_rms"))
        _nonempty(self.provenance, "provenance")
        _require_strict_json(self.to_metadata(), "homogeneity premise")

    def to_metadata(self) -> dict:
        return {"radius": self.radius.to_metadata(), "max_linear_rms": self.max_linear_rms,
                "provenance": self.provenance}


@dataclass(frozen=True, kw_only=True)
class AdmissibleGlobalLinearInterval:
    """[lower, upper] for every *constant* void share in the class (H15).

    Valid only for a share constant over the spectral support of both windows
    (target and premise top hats); a scale-dependent share in the monotone
    class is not bounded by it (audit GH-F4).  ``lower``: the monotone lower
    end p = f_v,LS (void fraction not increasing with the overdensity, H-A7);
    ``upper``: the adopted homogeneity premise,
    ``G <= max_linear_rms/sigma_u(R_hom)``, capped at p = 1; ``share_upper``
    the matching upper end of p.  ``wall_mode_value`` (p = 0, 1G-D's
    wall-curvature mode) and ``strict_flat_wall_value`` (p = 1) are reported
    for reference.  ``premise_compatible`` is False when even the lower end
    violates the premise.  Every field is re-validated from the target and
    premise (audit GH-F9) and recomputed from them on construction, including
    the target's own rms at the premise radius (delta audit GH-DF2).
    """

    target: ConditionalGlobalLinearSigma
    premise: HomogeneityPremise
    premise_radius: ResolvedLagrangianRadius
    unit_growth_sigma_at_premise: float
    propagator_upper: float
    share_lower: float
    share_upper: float
    lower: float
    upper: float
    wall_mode_value: float
    strict_flat_wall_value: float
    target_value: float
    target_inside: bool
    target_premise_rms: float
    premise_compatible: bool
    class_assumptions: tuple[str, ...]

    def __post_init__(self) -> None:
        _require(self.target, ConditionalGlobalLinearSigma, "target")
        _require(self.premise, HomogeneityPremise, "premise")
        _require(self.premise_radius, ResolvedLagrangianRadius, "premise_radius")
        for name in ("unit_growth_sigma_at_premise", "propagator_upper", "lower", "upper",
                     "wall_mode_value", "strict_flat_wall_value", "target_value",
                     "target_premise_rms"):
            _positive(getattr(self, name), name)
        for name in ("share_lower", "share_upper"):
            _real(getattr(self, name), name)
        for name in ("target_inside", "premise_compatible"):
            if not isinstance(getattr(self, name), bool):
                raise GlobalVarianceContractError(f"{name} must be a bool")
        if self.premise_radius.spec is not self.premise.radius:
            raise GlobalVarianceContractError("premise_radius must resolve the premise's radius")
        # Record invariants re-evaluated from the target and the premise (GH-F9).
        growth = self.target.growth
        d_w, d_v = growth.wall_share_growth, growth.void_share_growth
        su = self.target.unit_growth_sigma
        g_upper = self.premise.max_linear_rms / self.unit_growth_sigma_at_premise
        g_lower = d_w + (d_v - d_w) * growth.f_v_ls
        if not (self.share_lower == growth.f_v_ls and self.target_value == self.target.linear_sigma
                and _close(self.propagator_upper, g_upper)
                and _close(self.share_upper, min(1.0, (g_upper - d_w) / (d_v - d_w)))
                and _close(self.lower, g_lower * su)
                and _close(self.upper, min(g_upper, d_v) * su)
                and _close(self.wall_mode_value, d_w * su)
                and _close(self.strict_flat_wall_value, d_v * su)
                and self.premise_compatible == (g_lower <= g_upper)):
            raise GlobalVarianceContractError("interval fields violate (H15) for this target")
        if self.premise_compatible and not self.lower <= self.upper:
            raise GlobalVarianceContractError("a compatible premise needs lower <= upper")
        if self.target_inside != (self.premise_compatible
                                  and self.lower <= self.target_value <= self.upper):
            raise GlobalVarianceContractError("target_inside is inconsistent")
        if _strings(self.class_assumptions, "class_assumptions") != _INTERVAL_ASSUMPTIONS:
            raise GlobalVarianceContractError(
                "class_assumptions must be the module's interval assumptions")
        # Binding (delta audit GH-DF2): the premise radius, sigma_u there and
        # the target's own rms at the premise radius recomputed.
        _bind_recomputed(self, lambda: _interval_values(self.target, self.premise),
                         "interval record")
        _require_strict_json(self.to_json_dict(), "interval record")

    def to_json_dict(self) -> dict:
        return {"premise": self.premise.to_metadata(),
                "premise_radius": self.premise_radius.to_json_dict(),
                "unit_growth_sigma_at_premise": self.unit_growth_sigma_at_premise,
                "propagator_upper": self.propagator_upper,
                "share_lower": self.share_lower, "share_upper": self.share_upper,
                "lower": self.lower, "upper": self.upper,
                "wall_mode_value": self.wall_mode_value,
                "strict_flat_wall_value": self.strict_flat_wall_value,
                "target_value": self.target_value, "target_inside": self.target_inside,
                "target_premise_rms": self.target_premise_rms,
                "premise_compatible": self.premise_compatible,
                "class_assumptions": list(self.class_assumptions),
                "radius_Mpc": self.target.radius.radius_Mpc}


_INTERVAL_ASSUMPTIONS = (
    "all assumptions of the target record (A1-A5, H-A6, empty voids, growing modes)",
    "H-A7 monotone response: f_v,LS <= p <= 1 (an added class assumption)",
    "a void share constant over the spectral support of both windows (target and "
    "premise top hats); scale-dependent shares in the monotone class are not bounded by "
    "this interval (audit GH-F4)",
    "the homogeneity premise as recorded: an adopted reading of an assumption of the "
    "background construction ([W09] ll. 327-335, 455-458), not a derived bound and not a "
    "statement of [W09] about this statistic",
)


def admissible_global_linear_interval(
    *, target: ConditionalGlobalLinearSigma, premise: HomogeneityPremise,
) -> AdmissibleGlobalLinearInterval:
    """Constant-share interval for the target radius, (H15).

    For a share p constant over the spectral support of both windows,
    ``sigma(R) = G(p) sigma_u(R)`` with ``G(p) = D_W + (D_V - D_W) p``.  H-A7
    gives ``p >= f_v,LS`` (lower end); the adopted premise
    ``G sigma_u(R_hom) <= eta`` gives the upper end (capped at p = 1).  It is
    not a bound for scale-dependent shares (audit GH-F4).  The target's own
    closure is evaluated at the premise radius with the same propagator
    (``target_premise_rms``) to test the premise directly.
    """
    _require(target, ConditionalGlobalLinearSigma, "target")
    _require(premise, HomogeneityPremise, "premise")
    return AdmissibleGlobalLinearInterval(
        target=target, premise=premise, **_interval_values(target, premise),
        class_assumptions=_INTERVAL_ASSUMPTIONS)


def _interval_values(target: ConditionalGlobalLinearSigma, premise: HomogeneityPremise) -> dict:
    """The fields of ``admissible_global_linear_interval``, (H15) (pure; GH-DF2)."""
    if premise.radius.convention is not target.radius.spec.convention:
        raise GlobalVarianceContractError(
            "the premise radius must use the target's radius convention")
    growth = target.growth
    hom = resolve_lagrangian_radius(spec=premise.radius, density=target.density)
    om = target.density.omega_m_per_photon
    unit_hom = _unit_sigma(hom.radius_Mpc, om, target.early_spectrum, target.quadrature)[0]

    def propagator(k):
        return global_linear_propagator(growth=growth, void_share=target.void_share, k_per_Mpc=k)

    target_hom = _unit_sigma(hom.radius_Mpc, om, target.early_spectrum, target.quadrature,
                             propagator)[0]
    d_w, d_v = growth.wall_share_growth, growth.void_share_growth
    g_upper = premise.max_linear_rms / unit_hom
    p_lower = growth.f_v_ls
    g_lower = d_w + (d_v - d_w) * p_lower
    p_upper = min(1.0, (g_upper - d_w) / (d_v - d_w))
    lower = g_lower * target.unit_growth_sigma
    upper = min(g_upper, d_v) * target.unit_growth_sigma
    compatible = g_lower <= g_upper
    inside = compatible and lower <= target.linear_sigma <= upper
    return {"premise_radius": hom, "unit_growth_sigma_at_premise": unit_hom,
            "propagator_upper": g_upper, "share_lower": p_lower, "share_upper": p_upper,
            "lower": lower, "upper": upper,
            "wall_mode_value": d_w * target.unit_growth_sigma,
            "strict_flat_wall_value": d_v * target.unit_growth_sigma,
            "target_value": target.linear_sigma, "target_inside": inside,
            "target_premise_rms": target_hom, "premise_compatible": compatible}


# --------------------------------------------------------------------------
# Two-phase covariance with cross terms ([1G-H] Sec. 6, (H17)-(H20))
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class TwoPhaseSmoothedMoments:
    """Smoothed second moments of the three components of (H17).

    With phase indicators chi_w + chi_v = 1, conditional fluctuations
    normalised by ``E[chi_w delta_w] = E[chi_v delta_v] = 0`` and ball
    averages ``A = (chi_w)_R - f_w``, ``B = (chi_w delta_w)_R``,
    ``C = (chi_v delta_v)_R``: ``var_partition = E[A^2]``,
    ``wall_field = E[B^2]``, ``void_field = E[C^2]``,
    ``partition_wall = E[AB]``, ``partition_void = E[AC]``,
    ``wall_void = E[BC]``.  Every entry is explicit (use 0.0 where an
    explicit hypothesis sets it to zero, and say which in ``provenance``).
    """

    var_partition: float
    wall_field: float
    void_field: float
    partition_wall: float
    partition_void: float
    wall_void: float
    provenance: str

    def __post_init__(self) -> None:
        for name in ("var_partition", "wall_field", "void_field"):
            if _real(getattr(self, name), name) < 0.0:
                raise GlobalVarianceContractError(f"{name} must be non-negative")
        for name in ("partition_wall", "partition_void", "wall_void"):
            _real(getattr(self, name), name)
        _nonempty(self.provenance, "provenance")

    def matrix(self) -> NDArray[np.float64]:
        return _readonly([[self.var_partition, self.partition_wall, self.partition_void],
                          [self.partition_wall, self.wall_field, self.wall_void],
                          [self.partition_void, self.wall_void, self.void_field]])


def two_phase_global_variance(
    *, void_volume_fraction: float, void_to_wall_density_ratio: float,
    moments: TwoPhaseSmoothedMoments,
) -> dict[str, float]:
    """Ball variance of the global contrast with every cross term, (H18).

    ``rho/<rho> = a_w chi_w (1 + delta_w) + a_v chi_v (1 + delta_v)``,
    ``a_w = 1/(f_w + f_v x)``, ``a_v = x a_w`` (mass normalisation
    ``f_w a_w + f_v a_v = 1``), so ``delta_R = alpha A + a_w B + a_v C`` with
    ``alpha = a_w (1 - x) = -delta_v^E/f_w`` (delta_v^E: the void contrast
    relative to the global mean) and
    ``sigma^2 = w^T M w``, ``w = (alpha, a_w, a_v)``.  The moment matrix M must
    be positive semidefinite (relative ``PSD_TOLERANCE``), else refused.  The
    1G-E formula is the case ``delta_v = 0``, ``E[AB] = 0`` (E3), (H19).
    """
    f_v = _fraction_open(void_volume_fraction, "void_volume_fraction")
    x = _real(void_to_wall_density_ratio, "void_to_wall_density_ratio")
    if x < 0.0:
        raise GlobalVarianceContractError("void_to_wall_density_ratio must be >= 0")
    _require(moments, TwoPhaseSmoothedMoments, "moments")
    f_w = 1.0 - f_v
    if moments.var_partition > f_v * f_w * (1.0 + 1e-12):
        raise GlobalVarianceContractError(
            "var_partition exceeds f_v f_w, the maximum variance of a smoothed indicator")
    m = np.asarray(moments.matrix())
    eig = np.linalg.eigvalsh(m)
    scale = float(np.max(np.abs(eig))) if np.any(eig) else 0.0
    if scale > 0.0 and float(np.min(eig)) < -PSD_TOLERANCE * scale:
        raise GlobalVarianceContractError(
            f"moment matrix is not positive semidefinite (min eigenvalue {float(np.min(eig)):.3e})")
    a_w = 1.0 / (f_w + f_v * x)
    a_v = x * a_w
    alpha = a_w * (1.0 - x)
    w = np.array([alpha, a_w, a_v])
    total = float(w @ m @ w)
    partition = alpha ** 2 * moments.var_partition
    wall = a_w ** 2 * moments.wall_field
    void = a_v ** 2 * moments.void_field
    return {"variance": total, "rms": math.sqrt(max(total, 0.0)),
            "partition_term": partition, "wall_field_term": wall, "void_field_term": void,
            "cross_terms": total - partition - wall - void,
            "partition_weight": alpha, "wall_weight": a_w, "void_weight": a_v,
            "void_contrast_global": a_v - 1.0}


def cauchy_schwarz_total_rms_interval(*, partition_rms: float, field_rms: float) -> dict:
    """[|a - b|, a + b] for the rms of a sum of two terms of rms a and b, (H20).

    Valid for every joint law (Cauchy-Schwarz); the independent value is
    ``sqrt(a^2 + b^2)``.  The end points need perfect (anti)correlation and
    need not be attainable by a physical two-phase model.
    """
    a = _real(partition_rms, "partition_rms")
    b = _real(field_rms, "field_rms")
    if a < 0.0 or b < 0.0:
        raise GlobalVarianceContractError("rms values must be non-negative")
    return {"lower": abs(a - b), "independent": math.hypot(a, b), "upper": a + b}


def _orthant_inputs(correlation, threshold_1, threshold_2, nodes, tolerance):
    rho = _real(correlation, "correlation")
    if not -1.0 < rho < 1.0:
        raise GlobalVarianceContractError("correlation must lie in (-1, 1)")
    c1 = _real(threshold_1, "threshold")
    c2 = _real(threshold_2, "threshold")
    if isinstance(nodes, bool) or not isinstance(nodes, int) or not 16 <= nodes <= ORTHANT_MAX_NODES:
        raise GlobalVarianceContractError(f"nodes must be an integer in [16, {ORTHANT_MAX_NODES}]")
    tol = _positive(tolerance, "tolerance")
    if tol < 1e-15:
        raise GlobalVarianceContractError("tolerance below 1e-15 is beyond double precision")
    return rho, c1, c2, nodes, tol


@lru_cache(maxsize=16)
def _gauss_legendre(n: int) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    x, w = np.polynomial.legendre.leggauss(n)
    return _readonly(x), _readonly(w)


def _orthant_integrals(rho: float, c1: float, c2: float, nodes: int,
                       tolerance: float) -> tuple[NDArray[np.float64], int, float]:
    """The five orthant integrals on {g1 > c1, g2 > c2}, refined to ``tolerance``.

    ``P11 = int_c1^inf phi(u) Q(z) du``, ``E[1 1 g1] = int phi(u) u Q(z) du``,
    ``E[1 1 g2] = int phi(u) [rho u Q(z) + s phi(z)] du``,
    ``E[1 1 g1^2] = int phi(u) u^2 Q(z) du``,
    ``E[1 1 g1 g2] = int phi(u) u [rho u Q(z) + s phi(z)] du``, with
    ``s = sqrt(1 - rho^2)``, ``z = (c2 - rho u)/s`` and Q = 1 - Phi
    (g2 | g1 = u ~ N(rho u, s^2)).  The range is truncated to
    ``[max(c1, -12), max(c1, 0) + 12]`` (omitted tails below 1e-29).  Q(z)
    turns into a step at ``u* = c2/rho`` of width ``s/|rho|`` as |rho| -> 1, so
    the range is split at u* and at u* +- 8 s/|rho| (|z| = 8, where Q is within
    1e-15 of 0 or 1).  Gauss-Legendre panels are refined by doubling the node
    count until two successive results agree to ``tolerance`` in every
    integral; beyond ``ORTHANT_MAX_NODES`` the evaluation fails closed.
    """
    s = math.sqrt(1.0 - rho * rho)
    lo = max(c1, -_ORTHANT_HALF_WIDTH)
    hi = max(c1, 0.0) + _ORTHANT_HALF_WIDTH
    breaks = {lo, hi}
    if rho != 0.0:
        u_star, width = c2 / rho, s / abs(rho)
        for b in (u_star - 8.0 * width, u_star, u_star + 8.0 * width):
            if lo < b < hi:
                breaks.add(b)
    edges = sorted(breaks)
    norm = 1.0 / math.sqrt(2.0 * math.pi)

    def evaluate(n: int) -> NDArray[np.float64]:
        x, wts = _gauss_legendre(n)
        total = np.zeros(5)
        for a, b in zip(edges[:-1], edges[1:]):
            u = 0.5 * (b - a) * x + 0.5 * (b + a)
            wq = 0.5 * (b - a) * wts * norm * np.exp(-0.5 * u * u)
            z = (c2 - rho * u) / s
            q = ndtr(-z)
            cond_g2 = rho * u * q + s * norm * np.exp(-0.5 * z * z)
            total += np.array([np.sum(wq * q), np.sum(wq * u * q), np.sum(wq * cond_g2),
                               np.sum(wq * u * u * q), np.sum(wq * u * cond_g2)])
        return total

    n = nodes
    previous = evaluate(n)
    while True:
        if 2 * n > ORTHANT_MAX_NODES:
            raise GlobalVarianceNumericalError(
                f"orthant integrals not converged to {tolerance:.1e} with {n} nodes per panel "
                f"(rho = {rho!r}, thresholds {c1!r}, {c2!r})")
        n *= 2
        current = evaluate(n)
        change = float(np.max(np.abs(current - previous)))
        if change <= tolerance:
            return current, n, change
        previous = current


def _check_orthant_probability(p11: float, c1: float, c2: float, tol: float) -> None:
    upper = min(float(ndtr(-c1)), float(ndtr(-c2)))
    lower = max(0.0, float(ndtr(-c1)) + float(ndtr(-c2)) - 1.0)      # Frechet bounds
    if not lower - tol <= p11 <= upper + tol:
        raise GlobalVarianceNumericalError(
            f"orthant probability {p11!r} outside its bounds [{lower!r}, {upper!r}]")


def bivariate_normal_orthant_probability(
    *, correlation: float, threshold_1: float, threshold_2: float, nodes: int,
    tolerance: float,
) -> float:
    """P(g1 > c1, g2 > c2) for a standard bivariate normal with correlation rho.

    The orthant probability of (H21) with two thresholds (needed for the
    exponentially tilted moments of the lognormal pair of [1G-H] Sec. 6.3).
    ``nodes`` is the starting Gauss-Legendre node count per panel and
    ``tolerance`` the absolute accuracy target of the refinement (audit
    GH-F10); the result is checked against the Frechet bounds.  Requires
    |rho| < 1.
    """
    rho, c1, c2, n, tol = _orthant_inputs(correlation, threshold_1, threshold_2, nodes,
                                          tolerance)
    values, _, _ = _orthant_integrals(rho, c1, c2, n, tol)
    p11 = float(values[0])
    _check_orthant_probability(p11, c1, c2, tol)
    return p11


def bivariate_normal_orthant_moments(
    *, correlation: float, threshold: float, nodes: int, tolerance: float,
) -> dict[str, float]:
    """Moments of a standard bivariate normal on the orthant {g1 > c, g2 > c}, (H21).

    ``P11``, ``E_g1 = E[1 1 g1]``, ``E_g2``, ``E_g1g1 = E[1 1 g1^2]`` and
    ``E_g1g2`` (formulas in ``_orthant_integrals``), refined until two
    successive node doublings agree to ``tolerance`` in every moment (audit
    GH-F10; ``nodes`` is the starting count per panel).  P11 is checked
    against the Frechet bounds and the symmetry E[1 1 g1] = E[1 1 g2]; a
    failure raises ``GlobalVarianceNumericalError``.  ``nodes_used`` and
    ``refinement_change`` record the convergence.  Requires |rho| < 1.
    """
    rho, c, _, n, tol = _orthant_inputs(correlation, threshold, threshold, nodes, tolerance)
    values, used, change = _orthant_integrals(rho, c, c, n, tol)
    p11, e1, e2, e11, e12 = (float(v) for v in values)
    _check_orthant_probability(p11, c, c, tol)
    if not abs(e1 - e2) <= 10.0 * tol:
        raise GlobalVarianceNumericalError("orthant moments violate E[1 1 g1] = E[1 1 g2]")
    return {"P11": p11, "E_g1": e1, "E_g2": e2, "E_g1g1": e11, "E_g1g2": e12,
            "nodes_used": float(used), "refinement_change": change}


# --------------------------------------------------------------------------
# Excursion-set two-barrier response, an alternative closure ([1G-H] (H22))
# --------------------------------------------------------------------------

def two_barrier_void_mass_fraction(
    *, collapse_threshold: float, void_threshold: float, long_mode_contrast: float,
) -> float:
    """Total void mass fraction of the two-barrier walk, [SvdW04] Eq. (3).

    ``m = delta_c/(delta_c + |delta_v|)`` (the gambler's-ruin probability of
    reaching the void barrier first).  A region with linear long-mode contrast
    delta_l (extrapolated with the same clock as the barriers) has walks that
    start at delta_l (Markov property of sharp-k walks), so
    ``m(delta_l) = (delta_c - delta_l)/(delta_c + |delta_v|)`` and
    ``dm/d delta_l = -1/(delta_c + |delta_v|)``, (H22).  Requires
    ``-|delta_v| < delta_l < delta_c``.
    """
    d_c = _positive(collapse_threshold, "collapse_threshold")
    d_v = _real(void_threshold, "void_threshold")
    if not d_v < 0.0:
        raise GlobalVarianceContractError("void_threshold must be negative")
    d_l = _real(long_mode_contrast, "long_mode_contrast")
    if not d_v < d_l < d_c:
        raise GlobalVarianceContractError("long_mode_contrast must lie between the barriers")
    return (d_c - d_l) / (d_c - d_v)


def two_barrier_global_linear_bias(
    *, collapse_threshold: float, void_threshold: float,
    void_to_wall_density_ratio: float, wall_response: WallLongModeResponse,
) -> dict[str, float]:
    """First-order global response of the 1G-F M3 two-density budget, (H22).

    M3 (1G-F successor Sec. 1): voids hold mass fraction m at density
    ``x rho_ref``, walls the rest at ``rho_ref``; ``Z = 1 - m + m/x`` and the
    global mean is ``rho_ref/Z``.  A long mode delta_l shifts m by
    ``dm = -delta_l/(delta_c + |delta_v|)`` and, for
    ``COMPRESSED_WITH_LONG_MODE``, the region's reference density by delta_l,
    so ``delta_L = b delta_l`` with
    ``b = w + (1/x - 1)/[Z (delta_c + |delta_v|)]``, ``w`` = 1 (compressed) or
    0 (``UNIVERSAL_WALL_DENSITY``).  The voids' interior ratio x is held fixed
    at first order (an approximation recorded in [1G-H] Sec. 4.4).
    """
    d_c = _positive(collapse_threshold, "collapse_threshold")
    d_v = _real(void_threshold, "void_threshold")
    if not d_v < 0.0:
        raise GlobalVarianceContractError("void_threshold must be negative")
    x = _real(void_to_wall_density_ratio, "void_to_wall_density_ratio")
    if not 0.0 < x < 1.0:
        raise GlobalVarianceContractError("void_to_wall_density_ratio must lie in (0, 1)")
    _require_enum(wall_response, WallLongModeResponse, "wall_response")
    span = d_c - d_v
    m = d_c / span
    z_fac = 1.0 - m + m / x
    w = 1.0 if wall_response is WallLongModeResponse.COMPRESSED_WITH_LONG_MODE else 0.0
    void_term = (1.0 / x - 1.0) / (z_fac * span)
    return {"void_mass_fraction": m, "volume_factor_Z": z_fac,
            "void_volume_fraction": (m / x) / z_fac,
            "mass_fraction_response": -1.0 / span,
            "wall_term": w, "void_term": void_term, "bias": w + void_term}
