"""Conditional Phase 1E-F H1 clean transmission realization.

Realization: ``H1-1E-F-CLEAN-NONDEGENERATE-TRANSMISSION-V1``.
Framework: ``DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION``. This module implements only
the user-authorised non-observational operator-contract research runtime.

Inherited GM equation references use Galoppo & Mourier,
arXiv:2511.17160v2: regional CGI variables Eqs. (2.2), (2.20)-(2.23),
effective-fluid background Eqs. (3.12)-(3.13), clean closure Eqs. (4.12),
(4.20), and target propagation Eqs. (4.21)-(4.23).  New carrier and
transmission formulas are cited to the authoritative Phase 1E-F
implementation specification because they are conditional imported dynamics,
not equations supplied by that paper or the unlicensed upstream notebook.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np
from numpy.typing import ArrayLike

from timescape_fsigma8.transfer.matrix_backend import (
    DenseCarrierOperator,
    DenseH1TransmissionBackend,
    JointTransmissionState,
    ScalarJet,
    TransmissionSolution,
    VectorJet,
)


REALIZATION_ID = "H1-1E-F-CLEAN-NONDEGENERATE-TRANSMISSION-V1"
FRAMEWORK_STATUS = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
SCIENTIFIC_STATUS = "CONDITIONALLY_CLOSED"
OBSERVATIONAL_STATUS = "NON_OBSERVATIONAL"
FSIGMA8_STATUS = "NOT_FSIGMA8"
CARRIER_REFERENCE_TOPOLOGY = "T3_TWO_DOMAIN_FIXED_LAGRANGIAN_REFERENCE"
INTERFACE_ONTOLOGY = "MATHEMATICAL_CARRIER_TRANSFER_INTERFACE"
SCIENTIFIC_IMPLEMENTATION_AUTHORIZATION = "GRANTED"
PROTOTYPE_AUTHORIZATION = "GRANTED"
OBSERVATIONAL_IMPLEMENTATION_AUTHORIZATION = "NOT_GRANTED"
DRESSED_LIGHTCONE_IMPLEMENTATION_AUTHORIZATION = "NOT_GRANTED"
RSD_IMPLEMENTATION_AUTHORIZATION = "NOT_GRANTED"
FSIGMA8_IMPLEMENTATION_AUTHORIZATION = "NOT_GRANTED"


class H1ContractError(ValueError):
    """An explicit H1 operator or data contract is invalid."""


class H1DegeneracyError(H1ContractError):
    """The requested point lies outside the nondegenerate H1 branch."""


class H1ClosureError(H1ContractError):
    """A transmission, constitutive, compatibility, or constraint gate fails."""


@dataclass(frozen=True)
class H1Configuration:
    """All scientific thresholds are explicit; no field has a default."""

    A_P_min: float
    effective_denominator_min: float
    coercivity_min: float
    partition_product_min: float
    rho_d_min: float
    C_P_tolerance: float
    R_Delta_tolerance: float
    R_Z_tolerance: float
    R_eff_tolerance: float
    K_GM_tolerance: float
    transmission_value_tolerance: float
    transmission_flux_tolerance: float
    source_roundtrip_tolerance: float
    background_identity_tolerance: float

    def __post_init__(self) -> None:
        minima = (
            "A_P_min",
            "effective_denominator_min",
            "coercivity_min",
            "partition_product_min",
            "rho_d_min",
        )
        tolerances = (
            "C_P_tolerance",
            "R_Delta_tolerance",
            "R_Z_tolerance",
            "R_eff_tolerance",
            "K_GM_tolerance",
            "transmission_value_tolerance",
            "transmission_flux_tolerance",
            "source_roundtrip_tolerance",
            "background_identity_tolerance",
        )
        for name in minima:
            value = float(getattr(self, name))
            if not np.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        for name in tolerances:
            value = float(getattr(self, name))
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True)
class H1UnnormalizedEffectiveDiagnostics:
    """Effective-sector quantities that do not divide by Q_bar+W_bar."""

    background_Q_plus_W: ScalarJet
    F_v: VectorJet
    mathscr_Q: VectorJet
    mathscr_W: VectorJet
    C_P: VectorJet


class H1EffectiveNormalizationError(H1DegeneracyError):
    """Normalized effective variables are unavailable; diagnostics remain."""

    def __init__(
        self,
        message: str,
        diagnostics: H1UnnormalizedEffectiveDiagnostics,
    ) -> None:
        super().__init__(message)
        self.diagnostics = diagnostics


@dataclass(frozen=True)
class RegionalBulkState:
    """The exact four-dimensional regional differential state."""

    Delta_w: float
    Z_w: float
    Delta_v: float
    Z_v: float

    def __post_init__(self) -> None:
        values = np.asarray((self.Delta_w, self.Z_w, self.Delta_v, self.Z_v))
        if not np.all(np.isfinite(values)):
            raise ValueError("regional bulk state must be finite")


@dataclass(frozen=True)
class H1Background:
    """Explicit common-time background and derivative contract."""

    f_v: ScalarJet
    rho_w: ScalarJet
    rho_v: ScalarJet
    Theta_w: ScalarJet
    Theta_v: ScalarJet
    H_w: ScalarJet
    H_v: ScalarJet
    alpha_w: ScalarJet
    alpha_v: ScalarJet
    R_bar_w: ScalarJet
    R_bar_v: ScalarJet
    Q_bar: ScalarJet
    W_bar: ScalarJet
    Theta: ScalarJet
    Xi_w: ScalarJet
    Xi_v: ScalarJet
    G: float

    def __post_init__(self) -> None:
        if not np.isfinite(self.G) or self.G <= 0.0:
            raise ValueError("G must be finite and positive")


@dataclass(frozen=True)
class EffectiveSectorContract:
    """Required explicit operators for sharp effective-sector variations."""

    delta_theta_operator: DenseCarrierOperator
    delta_theta_inputs: VectorJet
    delta_xi0_operator: DenseCarrierOperator
    delta_xi0_inputs: VectorJet
    J_f_Gamma: VectorJet
    partition_time_independent: bool

    def __post_init__(self) -> None:
        if not isinstance(self.delta_theta_operator, DenseCarrierOperator):
            raise H1ContractError("delta_theta_operator is required")
        if not isinstance(self.delta_xi0_operator, DenseCarrierOperator):
            raise H1ContractError("delta_xi0_operator is required")
        if not isinstance(self.partition_time_independent, bool):
            raise H1ContractError("partition_time_independent must be explicit")
        if self.partition_time_independent and (
            np.any(self.J_f_Gamma.value)
            or np.any(self.J_f_Gamma.first)
            or np.any(self.J_f_Gamma.second)
        ):
            raise H1ContractError(
                "a time-independent partition requires explicitly zero J_f_Gamma"
            )


@dataclass(frozen=True)
class RegionalEvolution:
    delta: ScalarJet
    Z: ScalarJet
    curvature: ScalarJet


@dataclass(frozen=True)
class TwoRegionCoefficients:
    d_Theta: ScalarJet
    A_W: ScalarJet
    A_Q: ScalarJet
    B_Q: ScalarJet
    A_P: ScalarJet
    B_P: ScalarJet
    A_f: ScalarJet


@dataclass(frozen=True)
class H1TransmissionState:
    density: JointTransmissionState
    curvature: JointTransmissionState


@dataclass(frozen=True)
class H1RealizationResult:
    """Full scientific record; target-only inversion is intentionally absent."""

    realization_id: str
    framework_status: str
    scientific_status: str
    observational_status: str
    fsigma8_status: str
    scientific_implementation_authorization: str
    prototype_authorization: str
    observational_implementation_authorization: str
    carrier_reference_topology: str
    interface_ontology: str
    regional_bulk: RegionalBulkState
    regional_wall: RegionalEvolution
    regional_void: RegionalEvolution
    transmission_state: H1TransmissionState
    coefficients: TwoRegionCoefficients
    F_v: VectorJet
    J_Xi: np.ndarray
    mathscr_Q: VectorJet
    mathscr_W: VectorJet
    Delta_d: VectorJet
    Z: np.ndarray
    Delta_eff: VectorJet
    P_tilde_eff: np.ndarray
    R_GM: np.ndarray
    C_P: np.ndarray
    R_Delta: np.ndarray
    R_Z: np.ndarray
    R_eff: np.ndarray
    K_GM: np.ndarray
    transmission_value_jump: float
    transmission_flux_jump: float
    coercivity_lower_bound: float
    nondegeneracy_margins: Mapping[str, float]
    provenance_roundtrip_errors: Mapping[str, float]
    compatibility_zero_rhs: np.ndarray
    rho_d: float
    rho_eff: float
    p_eff: float
    w_eff: float


def _s_add(a: ScalarJet, b: ScalarJet) -> ScalarJet:
    return ScalarJet(a.value + b.value, a.first + b.first, a.second + b.second)


def _s_scale(scale: float, a: ScalarJet) -> ScalarJet:
    return ScalarJet(scale * a.value, scale * a.first, scale * a.second)


def _s_sub(a: ScalarJet, b: ScalarJet) -> ScalarJet:
    return _s_add(a, _s_scale(-1.0, b))


def _s_mul(a: ScalarJet, b: ScalarJet) -> ScalarJet:
    return ScalarJet(
        a.value * b.value,
        a.first * b.value + a.value * b.first,
        a.second * b.value + 2.0 * a.first * b.first + a.value * b.second,
    )


def _s_inverse(a: ScalarJet) -> ScalarJet:
    if a.value == 0.0:
        raise H1DegeneracyError("attempted division by an exactly zero scalar jet")
    return ScalarJet(
        1.0 / a.value,
        -a.first / a.value**2,
        2.0 * a.first**2 / a.value**3 - a.second / a.value**2,
    )


def _s_div(a: ScalarJet, b: ScalarJet) -> ScalarJet:
    return _s_mul(a, _s_inverse(b))


def _v_add(*jets: VectorJet) -> VectorJet:
    if not jets:
        raise ValueError("at least one vector jet is required")
    return VectorJet(
        sum((jet.value for jet in jets), np.zeros_like(jets[0].value)),
        sum((jet.first for jet in jets), np.zeros_like(jets[0].first)),
        sum((jet.second for jet in jets), np.zeros_like(jets[0].second)),
    )


def _v_scale(scalar: ScalarJet, vector: VectorJet) -> VectorJet:
    return VectorJet(
        scalar.value * vector.value,
        scalar.first * vector.value + scalar.value * vector.first,
        scalar.second * vector.value
        + 2.0 * scalar.first * vector.first
        + scalar.value * vector.second,
    )


def _v_constant_scale(scale: float, vector: VectorJet) -> VectorJet:
    return VectorJet(scale * vector.value, scale * vector.first, scale * vector.second)


def _v_div(vector: VectorJet, scalar: ScalarJet) -> VectorJet:
    return _v_scale(_s_inverse(scalar), vector)


def _max_abs(values: ArrayLike) -> float:
    array = np.asarray(values, dtype=np.float64)
    return float(np.max(np.abs(array))) if array.size else 0.0


def regional_evolution(
    delta: float,
    Z: float,
    *,
    alpha: ScalarJet,
    H: ScalarJet,
    rho: ScalarJet,
    Theta: ScalarJet,
    G: float,
) -> RegionalEvolution:
    """Evaluate the exact common-time regional rank-two dust system.

    Exactness refers to the supplied regional proper-time dust-FLRW system.
    Its regional/common Timescape background and source embedding is
    NOT_DERIVED. Identifier equality does not establish coincident zeroth-
    order dust/wall backgrounds or all-time constitutive compatibility.

    The proper-time system is GM Eqs. (2.22)-(2.23) with ``w=P=V=F=0``
    (equivalently DBE92 Eqs. (32)-(33)); the common-time ``alpha_r`` factors
    are the authorised Phase 1E-F ``regional-dynamics`` chain rule.
    Regional curvature is the constraint derived by varying GM Eq. (2.13),
    not a new state.
    """
    four_pi_G = 4.0 * np.pi * G
    delta_first = -alpha.value * Z
    Z_first = -2.0 * alpha.value * H.value * Z - four_pi_G * alpha.value * rho.value * delta
    delta_second = -alpha.first * Z - alpha.value * Z_first
    Z_second = (
        -2.0 * (alpha.first * H.value + alpha.value * H.first) * Z
        - 2.0 * alpha.value * H.value * Z_first
        - four_pi_G
        * (
            (alpha.first * rho.value + alpha.value * rho.first) * delta
            + alpha.value * rho.value * delta_first
        )
    )
    delta_jet = ScalarJet(delta, delta_first, delta_second)
    Z_jet = ScalarJet(Z, Z_first, Z_second)
    curvature = ScalarJet(
        -(4.0 / 3.0) * Theta.value * Z + 16.0 * np.pi * G * rho.value * delta,
        -(4.0 / 3.0) * (Theta.first * Z + Theta.value * Z_first)
        + 16.0 * np.pi * G * (rho.first * delta + rho.value * delta_first),
        -(4.0 / 3.0)
        * (Theta.second * Z + 2.0 * Theta.first * Z_first + Theta.value * Z_second)
        + 16.0
        * np.pi
        * G
        * (rho.second * delta + 2.0 * rho.first * delta_first + rho.value * delta_second),
    )
    return RegionalEvolution(delta=delta_jet, Z=Z_jet, curvature=curvature)


def two_region_coefficients(background: H1Background) -> TwoRegionCoefficients:
    """Return the authorised sharp two-region coefficient jets.

    Source: Phase 1E-F specification ``two-region-background-quantities``.
    The backreaction variation is the two-region specialization of the
    Buchert quantities underlying GM Eqs. (3.8)-(3.13).
    """
    one = ScalarJet(1.0, 0.0, 0.0)
    f_v = background.f_v
    f_w = _s_sub(one, f_v)
    d_theta = _s_sub(background.Theta_v, background.Theta_w)
    one_minus_two_f = _s_sub(one, _s_scale(2.0, f_v))
    d_theta_squared = _s_mul(d_theta, d_theta)
    A_W = _s_sub(background.R_bar_v, background.R_bar_w)
    A_Q = _s_scale(2.0 / 3.0, _s_mul(one_minus_two_f, d_theta_squared))
    B_Q = _s_scale(4.0 / 3.0, _s_mul(_s_mul(f_v, f_w), d_theta))
    A_P = _s_sub(A_W, _s_scale(3.0, A_Q))
    B_P = _s_scale(-3.0, B_Q)
    A_f = _s_mul(one_minus_two_f, _s_sub(background.Xi_v, background.Xi_w))
    return TwoRegionCoefficients(d_theta, A_W, A_Q, B_Q, A_P, B_P, A_f)


def compatibility_mismatch_rhs(
    mismatches: ArrayLike,
    *,
    Theta: float,
    rho_d: float,
    rho_eff: float,
    w_eff: float,
    G: float,
) -> np.ndarray:
    """Return the clean three-component mismatch propagation RHS.

    Direct subtraction of GM Eqs. (4.21)-(4.23) gives this clean system.
    ``C_P`` is deliberately absent because it is a separate constitutive
    residual and is required to vanish on this branch.
    """
    state = np.asarray(mismatches, dtype=np.float64)
    if state.shape != (3,) or not np.all(np.isfinite(state)):
        raise ValueError("mismatches must be finite (C_Delta, C_Z, C_eff)")
    C_Delta, C_Z, C_eff = state
    return np.array(
        (
            -C_Z,
            -(2.0 / 3.0) * Theta * C_Z
            - 4.0 * np.pi * G * rho_d * C_Delta
            - 4.0 * np.pi * G * rho_eff * C_eff,
            w_eff * Theta * C_eff - (1.0 + w_eff) * C_Z,
        ),
        dtype=np.float64,
    )


def validate_clean_diagnostics(
    *,
    C_P: ArrayLike,
    R_Delta: ArrayLike,
    R_Z: ArrayLike,
    R_eff: ArrayLike,
    K_GM: ArrayLike,
    configuration: H1Configuration,
) -> None:
    """Fail closed on each named clean residual without conflating them."""
    checks = (
        ("C_P", C_P, configuration.C_P_tolerance),
        ("R_Delta", R_Delta, configuration.R_Delta_tolerance),
        ("R_Z", R_Z, configuration.R_Z_tolerance),
        ("R_eff", R_eff, configuration.R_eff_tolerance),
        ("K_GM", K_GM, configuration.K_GM_tolerance),
    )
    for name, values, tolerance in checks:
        magnitude = _max_abs(values)
        if magnitude > tolerance:
            raise H1ClosureError(f"{name}={magnitude} exceeds tolerance {tolerance}")


def _roundtrip_errors(
    backend: DenseH1TransmissionBackend,
    transmission: H1TransmissionState,
) -> dict[str, float]:
    solutions: tuple[TransmissionSolution, ...] = (
        transmission.density.wall,
        transmission.density.void,
        transmission.curvature.wall,
        transmission.curvature.void,
    )
    return {
        solution.provenance: max(
            _max_abs(applied.value - solution.injected_source.value),
            _max_abs(applied.first - solution.injected_source.first),
            _max_abs(applied.second - solution.injected_source.second),
        )
        for solution in solutions
        for applied in (backend.apply_coupled_operator_jet(solution.field),)
    }


def evaluate_h1_realization(
    *,
    regional_bulk: RegionalBulkState,
    background: H1Background,
    backend: DenseH1TransmissionBackend,
    effective_sector: EffectiveSectorContract,
    configuration: H1Configuration,
) -> H1RealizationResult:
    """Evaluate the conditionally closed Phase 1E-F H1 realization.

    Every division is preceded by its named nondegeneracy gate.  Target
    ``Z`` is the analytic ``-d(Delta_d)/dt`` from the operator/source jets,
    never a finite difference or an independently invented transfer.
    """
    f_v = background.f_v
    f_w = _s_sub(ScalarJet(1.0, 0.0, 0.0), f_v)
    f_product = _s_mul(f_v, f_w)
    coefficients = two_region_coefficients(background)
    S_eff = _s_add(background.Q_bar, background.W_bar)
    coercivity = backend.coercivity_lower_bound
    margins = {
        "f_v": f_v.value,
        "f_w": f_w.value,
        "f_v * f_w": f_product.value,
        "|A_P|": abs(coefficients.A_P.value),
        "|Q_bar + W_bar|": abs(S_eff.value),
        "c_Gamma": coercivity,
        "alpha_w": background.alpha_w.value,
        "alpha_v": background.alpha_v.value,
    }
    if not 0.0 < f_v.value < 1.0:
        raise H1DegeneracyError(
            "SINGLE_REGION_ONTOLOGY_REDUCTION_REQUIRED: "
            "two-region branch requires 0 < f_v < 1"
        )
    if f_product.value < configuration.partition_product_min:
        raise H1DegeneracyError("f_v*f_w is below partition_product_min")
    if abs(coefficients.A_P.value) < configuration.A_P_min:
        raise H1DegeneracyError("abs(A_P) is below A_P_min")
    if coercivity < configuration.coercivity_min:
        raise H1DegeneracyError("c_Gamma is below coercivity_min")
    if background.alpha_w.value <= 0.0 or background.alpha_v.value <= 0.0:
        raise H1DegeneracyError("regional common-time alpha factors must be positive")
    for region, theta, hubble in (
        ("w", background.Theta_w, background.H_w),
        ("v", background.Theta_v, background.H_v),
    ):
        errors = (
            abs(theta.value - 3.0 * hubble.value),
            abs(theta.first - 3.0 * hubble.first),
            abs(theta.second - 3.0 * hubble.second),
        )
        if max(errors) > configuration.background_identity_tolerance:
            raise H1ContractError(f"Theta_{region}=3 H_{region} jet identity failed")

    wall = regional_evolution(
        regional_bulk.Delta_w,
        regional_bulk.Z_w,
        alpha=background.alpha_w,
        H=background.H_w,
        rho=background.rho_w,
        Theta=background.Theta_w,
        G=background.G,
    )
    void = regional_evolution(
        regional_bulk.Delta_v,
        regional_bulk.Z_v,
        alpha=background.alpha_v,
        H=background.H_v,
        rho=background.rho_v,
        Theta=background.Theta_v,
        G=background.G,
    )
    density_state = backend.solve_joint(wall.delta, void.delta, source_name="density")
    curvature_state = backend.solve_joint(
        wall.curvature,
        void.curvature,
        source_name="curvature",
    )
    transmission = H1TransmissionState(density=density_state, curvature=curvature_state)

    E_delta_theta = effective_sector.delta_theta_operator.evaluate(
        effective_sector.delta_theta_inputs
    )
    E_delta_xi0 = effective_sector.delta_xi0_operator.evaluate(
        effective_sector.delta_xi0_inputs
    )
    if E_delta_theta.value.shape != (backend.size,) or E_delta_xi0.value.shape != (backend.size,):
        raise H1ContractError("effective-sector operators must output carrier-sized fields")
    if effective_sector.J_f_Gamma.value.shape != (backend.size,):
        raise H1ContractError("J_f_Gamma must be a carrier-sized explicit field")

    # Phase 1E-F specification ``h1-curvature-transfer``.
    C_R = _v_add(
        _v_scale(f_w, curvature_state.wall.field),
        _v_scale(f_v, curvature_state.void.field),
    )
    # Phase 1E-F specification ``constitutive-closure``; A_P was gated above.
    F_v = _v_div(
        _v_constant_scale(-1.0, _v_add(C_R, _v_scale(coefficients.B_P, E_delta_theta))),
        coefficients.A_P,
    )
    mathscr_Q = _v_add(
        _v_scale(coefficients.A_Q, F_v),
        _v_scale(coefficients.B_Q, E_delta_theta),
    )
    mathscr_W = _v_add(C_R, _v_scale(coefficients.A_W, F_v))
    C_P_jet = _v_add(mathscr_W, _v_constant_scale(-3.0, mathscr_Q))
    if abs(S_eff.value) < configuration.effective_denominator_min:
        raise H1EffectiveNormalizationError(
            "abs(Q_bar+W_bar) is below effective_denominator_min; "
            "normalized Delta_eff and w_eff were not evaluated",
            H1UnnormalizedEffectiveDiagnostics(
                background_Q_plus_W=S_eff,
                F_v=F_v,
                mathscr_Q=mathscr_Q,
                mathscr_W=mathscr_W,
                C_P=C_P_jet,
            ),
        )

    # Phase 1E-F specification, section mass-weighted-dust-transfer.
    rho_d = _s_add(
        _s_mul(f_w, background.rho_w),
        _s_mul(f_v, background.rho_v),
    )
    if abs(rho_d.value) < configuration.rho_d_min:
        raise H1DegeneracyError("abs(rho_d) is below rho_d_min")
    m_w = _s_div(_s_mul(f_w, background.rho_w), rho_d)
    m_v = _s_div(_s_mul(f_v, background.rho_v), rho_d)
    d_F = _s_div(_s_sub(background.rho_v, background.rho_w), rho_d)
    # Phase 1E-F specification ``mass-weighted-dust-transfer``.
    Delta_d = _v_add(
        _v_scale(m_w, density_state.wall.field),
        _v_scale(m_v, density_state.void.field),
        _v_scale(d_F, F_v),
    )
    Z = -Delta_d.first
    Z_dot = -Delta_d.second

    # Phase 1E-F specification ``partition-common-time-closure``.
    J_Xi = (
        F_v.first
        - coefficients.A_f.value * F_v.value
        - f_product.value * E_delta_xi0.value
        - effective_sector.J_f_Gamma.value
    ) / f_product.value

    # [GM] Eqs. (3.12)-(3.13), followed by the Phase 1E-F normalized transfer.
    rho_eff_jet = _s_scale(-1.0 / (16.0 * np.pi * background.G), S_eff)
    p_eff_jet = _s_add(
        _s_scale(-1.0 / (16.0 * np.pi * background.G), background.Q_bar),
        _s_scale(1.0 / (48.0 * np.pi * background.G), background.W_bar),
    )
    w_eff_jet = _s_div(p_eff_jet, rho_eff_jet)
    Delta_eff = _v_div(_v_add(mathscr_Q, mathscr_W), S_eff)
    P_tilde_eff = -C_P_jet.value / (3.0 * S_eff.value)

    # Canonical clean GM residuals, [GM] Eqs. (4.21)-(4.23), with the
    # pressure term fixed by [GM] Eq. (4.12) and Phase 1E-F conventions.
    R_Delta = Delta_d.first + Z
    R_Z = (
        Z_dot
        + (2.0 / 3.0) * background.Theta.value * Z
        + 4.0
        * np.pi
        * background.G
        * (rho_d.value * Delta_d.value + rho_eff_jet.value * Delta_eff.value)
        + 12.0 * np.pi * background.G * rho_eff_jet.value * P_tilde_eff
    )
    R_eff = (
        Delta_eff.first
        - w_eff_jet.value * background.Theta.value * Delta_eff.value
        + (1.0 + w_eff_jet.value) * Z
        + background.Theta.value * P_tilde_eff
    )
    # Derived Hamiltonian constraint from the first variation of GM Eq. (2.13).
    R_GM = (
        -(4.0 / 3.0) * background.Theta.value * Z
        + 16.0
        * np.pi
        * background.G
        * (rho_d.value * Delta_d.value + rho_eff_jet.value * Delta_eff.value)
    )
    K_GM = (
        R_GM
        + (4.0 / 3.0) * background.Theta.value * Z
        - 16.0
        * np.pi
        * background.G
        * (rho_d.value * Delta_d.value + rho_eff_jet.value * Delta_eff.value)
    )

    solutions = (
        density_state.wall,
        density_state.void,
        density_state.carrier_field,
        curvature_state.wall,
        curvature_state.void,
        curvature_state.carrier_field,
    )
    fields = tuple(
        item.field.value if isinstance(item, TransmissionSolution) else item.value
        for item in solutions
    )
    value_jump = max((_max_abs(backend.value_jump(field)) for field in fields), default=0.0)
    flux_jump = max((_max_abs(backend.flux_jump(field)) for field in fields), default=0.0)
    if value_jump > configuration.transmission_value_tolerance:
        raise H1ClosureError("transmission value jump exceeds tolerance")
    if flux_jump > configuration.transmission_flux_tolerance:
        raise H1ClosureError("transmission flux jump exceeds tolerance")

    roundtrip = _roundtrip_errors(backend, transmission)
    for provenance, error in roundtrip.items():
        if error > configuration.source_roundtrip_tolerance:
            raise H1ClosureError(
                f"source roundtrip for {provenance} exceeds tolerance: {error}"
            )
    validate_clean_diagnostics(
        C_P=C_P_jet.value,
        R_Delta=R_Delta,
        R_Z=R_Z,
        R_eff=R_eff,
        K_GM=K_GM,
        configuration=configuration,
    )
    zero_rhs = compatibility_mismatch_rhs(
        np.zeros(3),
        Theta=background.Theta.value,
        rho_d=rho_d.value,
        rho_eff=rho_eff_jet.value,
        w_eff=w_eff_jet.value,
        G=background.G,
    )
    return H1RealizationResult(
        realization_id=REALIZATION_ID,
        framework_status=FRAMEWORK_STATUS,
        scientific_status=SCIENTIFIC_STATUS,
        observational_status=OBSERVATIONAL_STATUS,
        fsigma8_status=FSIGMA8_STATUS,
        scientific_implementation_authorization=(
            SCIENTIFIC_IMPLEMENTATION_AUTHORIZATION
        ),
        prototype_authorization=PROTOTYPE_AUTHORIZATION,
        observational_implementation_authorization=(
            OBSERVATIONAL_IMPLEMENTATION_AUTHORIZATION
        ),
        carrier_reference_topology=CARRIER_REFERENCE_TOPOLOGY,
        interface_ontology=INTERFACE_ONTOLOGY,
        regional_bulk=regional_bulk,
        regional_wall=wall,
        regional_void=void,
        transmission_state=transmission,
        coefficients=coefficients,
        F_v=F_v,
        J_Xi=np.asarray(J_Xi, dtype=np.float64),
        mathscr_Q=mathscr_Q,
        mathscr_W=mathscr_W,
        Delta_d=Delta_d,
        Z=np.asarray(Z, dtype=np.float64),
        Delta_eff=Delta_eff,
        P_tilde_eff=np.asarray(P_tilde_eff, dtype=np.float64),
        R_GM=np.asarray(R_GM, dtype=np.float64),
        C_P=np.asarray(C_P_jet.value, dtype=np.float64),
        R_Delta=np.asarray(R_Delta, dtype=np.float64),
        R_Z=np.asarray(R_Z, dtype=np.float64),
        R_eff=np.asarray(R_eff, dtype=np.float64),
        K_GM=np.asarray(K_GM, dtype=np.float64),
        transmission_value_jump=value_jump,
        transmission_flux_jump=flux_jump,
        coercivity_lower_bound=coercivity,
        nondegeneracy_margins=margins,
        provenance_roundtrip_errors=roundtrip,
        compatibility_zero_rhs=zero_rhs,
        rho_d=rho_d.value,
        rho_eff=rho_eff_jet.value,
        p_eff=p_eff_jet.value,
        w_eff=w_eff_jet.value,
    )
