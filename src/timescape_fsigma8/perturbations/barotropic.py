"""Pure Timescape barotropic perturbation matrices with corrected sound speed.

References use [GM] for Galoppo & Mourier, JCAP 02 (2026) 066,
arXiv:2511.17160v2.  The closure is [GM] Eq. (4.13), and the state is
``(Delta_d, Z, Delta_eff, tilt)``.  ``tilt`` is either the unrescaled
``V`` used by the Timescape notebook or the paper variable
``Vtilde=(1+w_eff)V``.

Phase 1D-D-t resolved D3 as RESOLVED_DERIVED_4_10. The printed branch remains
an explicit forensic alternative, not an equally supported derived equation.
Finite-mode ODE uniqueness does not establish continuum stability. With the
negative corrected sound speed the unrestricted continuum Cauchy problem is
Hadamard ill-posed (Phase 1G-A Sec. 4.1; scientific_status
UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY = REFUTED_HADAMARD_ILL_POSED,
approved 2026-09-29).  Each fixed-k system below remains a regular linear
ODE and is kept unchanged for reproduction on both D3 branches.
Only the corrected Phase 1B ``cs2_eff`` is used in this module; reproduction
of the upstream D2 defect is deliberately outside the scientific package.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np
from numpy.typing import ArrayLike, NDArray

import timescape_fsigma8.background as bg
from timescape_fsigma8.background import TrackerParams


FloatArray = NDArray[np.float64]


class D3Branch(str, Enum):
    """Mandatory explicit derived-versus-forensic choice for [GM] Eq. (4.15).

    ``PRINTED_4_15`` uses ``(w_eff+cs2_eff)Theta`` as printed in Eq. (4.15)
    and implemented by the notebooks.  ``DERIVED_4_10`` uses
    ``(w_eff-cs2_eff)Theta`` obtained from Eqs. (4.10) and (4.13).
    """

    PRINTED_4_15 = "printed_4_15"
    DERIVED_4_10 = "derived_4_10"


class TiltForm(str, Enum):
    """Mandatory choice of the tilt variable in [GM] Eqs. (4.10)-(4.17)."""

    UNRESCALED_V = "unrescaled_V"
    RESCALED_VTILDE = "rescaled_Vtilde"


class WavenumberConvention(str, Enum):
    """Mandatory interpretation of the numerical wavenumber.

    ``UPSTREAM_TIMESCAPE_K`` injects the notebook's numerical ``k`` directly.
    ``PAPER_LCDM_HUBBLE_K`` interprets the supplied value in the Planck-2018
    present-Hubble-length convention stated in the [GM] Figure 3 caption.
    """

    UPSTREAM_TIMESCAPE_K = "upstream_timescape_k"
    PAPER_LCDM_HUBBLE_K = "paper_lcdm_hubble_k"


@dataclass(frozen=True)
class ResolvedWavenumber:
    """A supplied mode and its value in the Timescape matrix convention."""

    supplied_k: float
    matrix_k: float
    convention: WavenumberConvention
    timescape_h: float
    lcdm_h: float


def _require_enum(value, enum_type, name: str):
    if not isinstance(value, enum_type):
        raise ValueError(f"{name} must be an explicit {enum_type.__name__}, got {value!r}")
    return value


def resolve_wavenumber(
    k: float,
    *,
    params: TrackerParams,
    convention: WavenumberConvention,
    timescape_h: float,
    lcdm_h: float,
) -> ResolvedWavenumber:
    """Resolve ``k`` for the Laplacian term of [GM] footnote 8.

    The eigenvalue is ``(3)Laplacian -> -k^2/a_D^2``.  For the paper-caption
    convention, equality of the present physical wavenumber requires
    ``k_matrix = k_paper * a_D(t0) * h_LCDM/h_Timescape`` because the tracker
    uses ``a_D(t0)=1+fv0/2`` rather than one.  No convention is a default.
    """
    convention = _require_enum(convention, WavenumberConvention, "convention")
    if not np.isfinite(k) or k <= 0.0:
        raise ValueError(f"k must be finite and positive, got {k}")
    if not np.isfinite(timescape_h) or timescape_h <= 0.0:
        raise ValueError("timescape_h must be finite and positive")
    if not np.isfinite(lcdm_h) or lcdm_h <= 0.0:
        raise ValueError("lcdm_h must be finite and positive")
    if convention is WavenumberConvention.UPSTREAM_TIMESCAPE_K:
        matrix_k = float(k)
    elif convention is WavenumberConvention.PAPER_LCDM_HUBBLE_K:
        matrix_k = float(k * params.aD0 * lcdm_h / timescape_h)
    else:  # pragma: no cover - exhaustive defensive guard
        raise ValueError(f"unsupported wavenumber convention: {convention!r}")
    return ResolvedWavenumber(
        supplied_k=float(k),
        matrix_k=matrix_k,
        convention=convention,
        timescape_h=float(timescape_h),
        lcdm_h=float(lcdm_h),
    )


def _state(values: ArrayLike) -> FloatArray:
    state = np.asarray(values, dtype=np.float64)
    if state.shape != (4,):
        raise ValueError(f"barotropic state must have shape (4,), got {state.shape}")
    if not np.all(np.isfinite(state)):
        raise ValueError("barotropic state must contain only finite values")
    return state


def _a33(theta: float, w_eff: float, cs2_eff: float, branch: D3Branch) -> float:
    branch = _require_enum(branch, D3Branch, "branch")
    if branch is D3Branch.PRINTED_4_15:
        # [GM] Eq. (4.15) as printed.
        return (w_eff + cs2_eff) * theta
    if branch is D3Branch.DERIVED_4_10:
        # [GM] Eqs. (4.10) and (4.13).
        return (w_eff - cs2_eff) * theta
    raise ValueError(f"unsupported D3 branch: {branch!r}")  # pragma: no cover


def barotropic_matrix(
    t: float,
    *,
    params: TrackerParams,
    G: float,
    k: float,
    branch: D3Branch,
    tilt_form: TiltForm,
    wavenumber_convention: WavenumberConvention,
    timescape_h: float,
    lcdm_h: float,
) -> FloatArray:
    """Return the corrected-sound-speed barotropic coefficient matrix.

    Implements [GM] Eqs. (4.14)-(4.17) with closure Eq. (4.13).  The
    ``RESCALED_VTILDE`` form implements the paper equations directly.
    ``UNRESCALED_V`` implements Eq. (4.15) in ``V=Vtilde/(1+w_eff)`` and
    Eq. (4.8) with the same closure.  Their equivalence uses the exact
    background identity
    ``w_dot=-Theta(1+w)(cs2-w)`` from [GM] Eq. (3.17).

    Every scientific coefficient uses the corrected Phase 1B
    ``cs2_eff=dp_eff/dt / drho_eff/dt`` definition from [GM] Sec. 4.
    """
    if G <= 0.0 or not np.isfinite(G):
        raise ValueError(f"G must be finite and positive, got {G}")
    branch = _require_enum(branch, D3Branch, "branch")
    tilt_form = _require_enum(tilt_form, TiltForm, "tilt_form")
    resolved_k = resolve_wavenumber(
        k,
        params=params,
        convention=wavenumber_convention,
        timescape_h=timescape_h,
        lcdm_h=lcdm_h,
    )
    theta = float(bg.Theta(t, params))
    rho_d = float(bg.rho_d(t, params, G))
    rho_eff = float(bg.rho_eff(t, params, G))
    w_eff = float(bg.w_eff(t, params))
    cs2_eff = float(bg.cs2_eff(t, params))
    scale_factor = float(bg.a_D(t, params))
    one_plus_w = 1.0 + w_eff
    four_pi_G = 4.0 * np.pi * G
    k2_over_a = resolved_k.matrix_k**2 / scale_factor

    matrix = np.zeros((4, 4), dtype=np.float64)
    # [GM] Eq. (4.14).
    matrix[0, 1] = -1.0
    # [GM] Eq. (4.16).
    matrix[1, 0] = -four_pi_G * rho_d
    matrix[1, 1] = -(2.0 / 3.0) * theta
    matrix[1, 2] = -four_pi_G * rho_eff * (1.0 + 3.0 * cs2_eff)
    # [GM] Eq. (4.15) forensic branch versus derived Eqs. (4.10)+(4.13).
    matrix[2, 1] = -one_plus_w
    matrix[2, 2] = _a33(theta, w_eff, cs2_eff, branch)

    if tilt_form is TiltForm.RESCALED_VTILDE:
        # [GM] Eqs. (4.15) and (4.17) in Vtilde.
        matrix[2, 3] = k2_over_a
        matrix[3, 2] = -cs2_eff / scale_factor
        matrix[3, 3] = (theta / 3.0) * (3.0 * w_eff - 1.0)
    elif tilt_form is TiltForm.UNRESCALED_V:
        # [GM] Eq. (4.15) transformed with Vtilde=(1+w)V; row 4 is
        # Eq. (4.8) plus barotropic closure Eq. (4.13).
        matrix[2, 3] = k2_over_a * one_plus_w
        matrix[3, 2] = -cs2_eff / (scale_factor * one_plus_w)
        matrix[3, 3] = (theta / 3.0) * (3.0 * cs2_eff - 1.0)
    else:  # pragma: no cover - exhaustive defensive guard
        raise ValueError(f"unsupported tilt form: {tilt_form!r}")
    return matrix


def barotropic_rhs(
    t: float,
    state: ArrayLike,
    *,
    params: TrackerParams,
    G: float,
    k: float,
    branch: D3Branch,
    tilt_form: TiltForm,
    wavenumber_convention: WavenumberConvention,
    timescape_h: float,
    lcdm_h: float,
) -> FloatArray:
    """Return the RHS of [GM] Eqs. (4.14)-(4.17), with explicit choices."""
    return barotropic_matrix(
        t,
        params=params,
        G=G,
        k=k,
        branch=branch,
        tilt_form=tilt_form,
        wavenumber_convention=wavenumber_convention,
        timescape_h=timescape_h,
        lcdm_h=lcdm_h,
    ) @ _state(state)


def transform_barotropic_state(
    t: float,
    state: ArrayLike,
    *,
    params: TrackerParams,
    from_tilt_form: TiltForm,
    to_tilt_form: TiltForm,
) -> FloatArray:
    """Transform ``Vtilde=(1+w_eff)V`` from [GM] text before Eq. (4.9)."""
    from_tilt_form = _require_enum(from_tilt_form, TiltForm, "from_tilt_form")
    to_tilt_form = _require_enum(to_tilt_form, TiltForm, "to_tilt_form")
    transformed = _state(state).copy()
    if from_tilt_form is to_tilt_form:
        return transformed
    one_plus_w = 1.0 + float(bg.w_eff(t, params))
    if from_tilt_form is TiltForm.UNRESCALED_V:
        transformed[3] *= one_plus_w
    elif from_tilt_form is TiltForm.RESCALED_VTILDE:
        transformed[3] /= one_plus_w
    return transformed


def tilt_state_transform(
    t: float,
    *,
    params: TrackerParams,
    from_tilt_form: TiltForm,
    to_tilt_form: TiltForm,
) -> FloatArray:
    """Return the diagonal state transform implied by [GM] ``Vtilde=(1+w)V``."""
    from_tilt_form = _require_enum(from_tilt_form, TiltForm, "from_tilt_form")
    to_tilt_form = _require_enum(to_tilt_form, TiltForm, "to_tilt_form")
    factor = 1.0
    if from_tilt_form is not to_tilt_form:
        one_plus_w = 1.0 + float(bg.w_eff(t, params))
        factor = (
            one_plus_w
            if from_tilt_form is TiltForm.UNRESCALED_V
            else 1.0 / one_plus_w
        )
    return np.diag([1.0, 1.0, 1.0, factor]).astype(np.float64)


def tilt_state_transform_dot(
    t: float,
    *,
    params: TrackerParams,
    from_tilt_form: TiltForm,
    to_tilt_form: TiltForm,
) -> FloatArray:
    """Return ``dT/dt`` using [GM] Eq. (3.17)'s exact ``w_dot`` identity."""
    from_tilt_form = _require_enum(from_tilt_form, TiltForm, "from_tilt_form")
    to_tilt_form = _require_enum(to_tilt_form, TiltForm, "to_tilt_form")
    derivative = np.zeros((4, 4), dtype=np.float64)
    if from_tilt_form is to_tilt_form:
        return derivative
    theta = float(bg.Theta(t, params))
    w_eff = float(bg.w_eff(t, params))
    cs2_eff = float(bg.cs2_eff(t, params))
    # [GM] Eq. (3.17) and cs2=dp/drho: w_dot=-Theta(1+w)(cs2-w).
    w_dot = -theta * (1.0 + w_eff) * (cs2_eff - w_eff)
    derivative[3, 3] = (
        w_dot
        if from_tilt_form is TiltForm.UNRESCALED_V
        else -w_dot / (1.0 + w_eff) ** 2
    )
    return derivative
