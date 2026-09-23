"""Background-identity and policy contracts of the H1 kinematic gates (F3).

Review finding F3 (reports/phase1f_c_r_post_remediation_independent_audit.md):
the Phase 1E-F/1E-G runtime never checked J_Xi=0 on CLK-H1 or the zeroth-order
identities of its two-region dust background.  These tests cover the pure
background layer: the identity residuals, the consistent-background
constructor, the explicit K_D input, and the mandatory gate policy.  Enforced
evaluations are tested next to their fixtures in test_phase1e_f_h1_transfer.py
and test_phase1e_g_continuum_h1.py.
"""

# A06: absolute budgets use rtol=0.  Constructed backgrounds are O(1) in the
# fixture units, so 1e-13 is a roundoff allowance; perturbation budgets are
# relative to the injected epsilon.

from __future__ import annotations

from dataclasses import fields, replace
import inspect

import numpy as np
import pytest

import timescape_fsigma8.transfer as transfer
from timescape_fsigma8.scientific_status import MANUFACTURED_H1_TRAJECTORIES
from timescape_fsigma8.transfer import (
    ALGEBRAIC_VALIDATION_ONLY_STATUS,
    BACKGROUND_IDENTITY_NAMES,
    CLOCK_BRANCH,
    H1Background,
    H1Configuration,
    H1ContractError,
    H1KinematicGatePolicy,
    ScalarJet,
    two_region_background_identity_residuals,
    two_region_dust_flrw_background,
)

G = 1.0 / (4.0 * np.pi)
ONE = ScalarJet(1.0, 0.0, 0.0)
ROUNDOFF = 1e-13
EPSILON = 1e-3


def background(**changes: object) -> H1Background:
    values: dict[str, object] = {
        "f_v": 0.4,
        "rho_w": 1.5,
        "rho_v": 0.5,
        "H_w": 0.3,
        "H_v": 0.5,
        "alpha_w": ONE,
        "alpha_v": ONE,
        "six_K_D_over_a_D_squared": 0.0,
        "G": G,
    }
    values.update(changes)
    return two_region_dust_flrw_background(**values)  # type: ignore[arg-type]


def shifted(jet: ScalarJet, *, value: float = 0.0, first: float = 0.0, second: float = 0.0) -> ScalarJet:
    return ScalarJet(jet.value + value, jet.first + first, jet.second + second)


def configuration(**changes: object) -> H1Configuration:
    values: dict[str, object] = {
        "A_P_min": 1e-8,
        "effective_denominator_min": 1e-8,
        "coercivity_min": 0.5,
        "partition_product_min": 1e-8,
        "rho_d_min": 1e-8,
        "C_P_tolerance": 1e-10,
        "R_Delta_tolerance": 1e-10,
        "R_Z_tolerance": 1e-10,
        "R_eff_tolerance": 1e-10,
        "K_GM_tolerance": 1e-10,
        "transmission_value_tolerance": 1e-10,
        "transmission_flux_tolerance": 1e-10,
        "source_roundtrip_tolerance": 1e-10,
        "background_identity_tolerance": 1e-12,
        "J_Xi_tolerance": 1e-10,
        "kinematic_gate_policy": H1KinematicGatePolicy.ENFORCE,
    }
    values.update(changes)
    return H1Configuration(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "changes",
    [
        {},
        {"f_v": 0.15, "rho_w": 3.0, "rho_v": 0.2, "H_w": 0.1, "H_v": 0.9},
        {"f_v": 0.85, "H_w": 0.6, "H_v": 0.2},
        {"six_K_D_over_a_D_squared": 0.3},
        {"six_K_D_over_a_D_squared": -0.7, "G": 0.37},
        {"H_w": -0.2},  # a collapsing wall region is still exact dust FLRW
    ],
)
def test_common_proper_time_constructor_satisfies_every_identity(changes) -> None:
    built = background(**changes)
    residuals = two_region_background_identity_residuals(built)
    assert tuple(residuals) == BACKGROUND_IDENTITY_NAMES
    assert max(residuals.values()) <= ROUNDOFF
    for theta, hubble in ((built.Theta_w, built.H_w), (built.Theta_v, built.H_v)):
        for a, b in zip((theta.value, theta.first, theta.second), (hubble.value, hubble.first, hubble.second)):
            assert a == pytest.approx(3.0 * b, rel=0.0, abs=ROUNDOFF)


def test_constructor_reproduces_closed_form_regional_dust_flrw_jets() -> None:
    built = background()
    # Proper-time dust FLRW with Lambda=0: H_dot = -H^2 - 4 pi G rho / 3,
    # rho_dot = -3 H rho (independent closed forms, alpha_r = 1).
    for rho, hubble in ((built.rho_w, built.H_w), (built.rho_v, built.H_v)):
        H_dot = -hubble.value**2 - 4.0 * np.pi * G * rho.value / 3.0
        rho_dot = -3.0 * hubble.value * rho.value
        H_ddot = -2.0 * hubble.value * H_dot - 4.0 * np.pi * G * rho_dot / 3.0
        assert hubble.first == pytest.approx(H_dot, rel=0.0, abs=ROUNDOFF)
        assert rho.first == pytest.approx(rho_dot, rel=0.0, abs=ROUNDOFF)
        assert hubble.second == pytest.approx(H_ddot, rel=0.0, abs=ROUNDOFF)
    # Two-region backreaction of 1E-D H-D7 and the variance identity.
    d_theta = built.Theta_v.value - built.Theta_w.value
    assert built.Q_bar.value == pytest.approx(
        (2.0 / 3.0) * 0.4 * 0.6 * d_theta**2, rel=0.0, abs=ROUNDOFF
    )
    assert built.Q_bar.value >= 0.0


@pytest.mark.parametrize(
    ("name", "field", "shift", "expected"),
    [
        ("regional_hamiltonian_constraint_w", "R_bar_w", {"value": EPSILON}, EPSILON),
        ("regional_hamiltonian_constraint_v", "R_bar_v", {"value": EPSILON}, EPSILON),
        ("regional_raychaudhuri_w", ("Theta_w", "H_w"), {"second": EPSILON}, EPSILON),
        ("regional_raychaudhuri_v", ("Theta_v", "H_v"), {"second": EPSILON}, EPSILON),
        ("regional_dust_continuity_w", "rho_w", {"second": EPSILON}, EPSILON),
        ("regional_dust_continuity_v", "rho_v", {"second": EPSILON}, EPSILON),
        ("partition_kinematics", "f_v", {"second": EPSILON}, EPSILON),
        ("average_expansion", "Theta", {"second": EPSILON}, EPSILON),
        ("two_region_backreaction", "Q_bar", {"second": EPSILON}, EPSILON),
        ("averaged_curvature_W", "W_bar", {"value": EPSILON}, EPSILON),
    ],
)
def test_each_identity_detects_its_own_violation(name, field, shift, expected) -> None:
    built = background()
    if isinstance(field, tuple):
        # Keep Theta_r = 3 H_r while breaking the regional Raychaudhuri law.
        theta_name, hubble_name = field
        scaled = {key: value / 3.0 for key, value in shift.items()}
        corrupted = replace(
            built,
            **{
                theta_name: shifted(getattr(built, theta_name), **shift),
                hubble_name: shifted(getattr(built, hubble_name), **scaled),
            },
        )
    else:
        corrupted = replace(built, **{field: shifted(getattr(built, field), **shift)})
    residuals = two_region_background_identity_residuals(corrupted)
    assert residuals[name] == pytest.approx(expected, rel=1e-9, abs=0.0)


def test_backreaction_offset_propagates_into_gm_averaged_equations() -> None:
    built = background()
    corrupted = replace(built, Q_bar=shifted(built.Q_bar, value=EPSILON))
    residuals = two_region_background_identity_residuals(corrupted)
    # [GM] (3.8) carries -Q/2 and (3.9) carries +Q.
    assert residuals["two_region_backreaction"] == pytest.approx(EPSILON, rel=1e-9, abs=0.0)
    assert residuals["averaged_hamiltonian_constraint"] == pytest.approx(EPSILON / 2.0, rel=1e-9, abs=0.0)
    assert residuals["averaged_raychaudhuri"] == pytest.approx(EPSILON, rel=1e-9, abs=0.0)


def test_mass_weighted_clock_mismatch_violates_gm_mass_conservation() -> None:
    built = background()
    # Shift Xi_w away from alpha_w Theta_w while keeping the value order of
    # partition kinematics and of the average expansion: at that order
    # [GM] (3.10) sees exactly the mass-weighted mismatch f_w rho_w epsilon,
    # although every regional identity still holds.
    f_v, f_w = built.f_v.value, 1.0 - built.f_v.value
    corrupted = replace(
        built,
        Xi_w=shifted(built.Xi_w, value=EPSILON),
        Theta=shifted(built.Theta, value=f_w * EPSILON),
        f_v=shifted(built.f_v, first=-f_v * f_w * EPSILON),
    )
    residuals = two_region_background_identity_residuals(corrupted)
    for name in BACKGROUND_IDENTITY_NAMES[:6]:
        assert residuals[name] <= ROUNDOFF, name
    value_order = abs(
        corrupted.rho_w.first * f_w
        + corrupted.rho_v.first * f_v
        + (corrupted.rho_v.value - corrupted.rho_w.value) * corrupted.f_v.first
        + corrupted.Theta.value * (f_w * corrupted.rho_w.value + f_v * corrupted.rho_v.value)
    )
    assert value_order == pytest.approx(f_w * built.rho_w.value * EPSILON, rel=1e-9, abs=0.0)
    assert residuals["averaged_mass_conservation"] >= value_order * (1.0 - 1e-9)


def test_unequal_regional_clocks_violate_gm_averaged_constraint() -> None:
    # With Q_bar built from the proper regional rates Theta_r (1E-D H-D7) and
    # the common-time average Theta = sum f_r alpha_r Theta_r, [GM] (3.8)
    # holds at the value order iff Theta^2 = (sum f_r Theta_r)^2.
    built = background(alpha_w=ScalarJet(1.1, 0.0, 0.0))
    residuals = two_region_background_identity_residuals(built)
    for name in BACKGROUND_IDENTITY_NAMES[:10]:
        assert residuals[name] <= ROUNDOFF, name
    assert residuals["averaged_mass_conservation"] <= ROUNDOFF
    proper = 0.6 * built.Theta_w.value + 0.4 * built.Theta_v.value
    predicted = abs(built.Theta.value**2 - proper**2) / 3.0
    assert predicted > 1e-2
    assert residuals["averaged_hamiltonian_constraint"] >= predicted * (1.0 - 1e-9)
    assert residuals["averaged_raychaudhuri"] > 1e-2


def test_K_D_is_an_explicit_input_that_enters_only_W() -> None:
    curved = background(six_K_D_over_a_D_squared=0.3)
    assert max(two_region_background_identity_residuals(curved).values()) <= ROUNDOFF
    omitted = replace(curved, six_K_D_over_a_D_squared=0.0)
    residuals = two_region_background_identity_residuals(omitted)
    theta = curved.Theta
    k1 = -(2.0 / 3.0) * theta.value * 0.3
    k2 = -(2.0 / 3.0) * (theta.first * 0.3 + theta.value * k1)
    assert residuals["averaged_curvature_W"] == pytest.approx(
        max(0.3, abs(k1), abs(k2)), rel=1e-12, abs=0.0
    )
    for name in BACKGROUND_IDENTITY_NAMES:
        if name != "averaged_curvature_W":
            assert residuals[name] <= ROUNDOFF, name
    assert "six_K_D_over_a_D_squared" in {field.name for field in fields(H1Background)}
    with pytest.raises(TypeError):
        H1Background(**{  # type: ignore[call-arg]
            field.name: getattr(curved, field.name)
            for field in fields(H1Background)
            if field.name != "six_K_D_over_a_D_squared"
        })
    with pytest.raises(ValueError, match="six_K_D_over_a_D_squared"):
        replace(curved, six_K_D_over_a_D_squared=float("nan"))


def test_gate_policy_and_new_tolerances_are_mandatory_and_typed() -> None:
    signature = inspect.signature(H1Configuration)
    for name in ("J_Xi_tolerance", "kinematic_gate_policy"):
        assert signature.parameters[name].default is inspect.Parameter.empty
    with pytest.raises(H1ContractError, match="kinematic_gate_policy"):
        configuration(kinematic_gate_policy="ENFORCE_TWO_REGION_BACKGROUND_AND_CLK_H1_KINEMATICS")
    with pytest.raises(ValueError, match="J_Xi_tolerance"):
        configuration(J_Xi_tolerance=-1.0)
    assert {policy.value for policy in H1KinematicGatePolicy} == {
        "ENFORCE_TWO_REGION_BACKGROUND_AND_CLK_H1_KINEMATICS",
        "ALGEBRAIC_VALIDATION_ONLY",
    }


def test_constructor_has_no_defaults_and_fails_closed() -> None:
    signature = inspect.signature(two_region_dust_flrw_background)
    assert all(
        parameter.default is inspect.Parameter.empty
        and parameter.kind is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )
    with pytest.raises(H1ContractError, match="0 < f_v < 1"):
        background(f_v=1.0)
    with pytest.raises(H1ContractError, match="alpha_w"):
        background(alpha_w=1.0)
    with pytest.raises(H1ContractError, match="G must be positive"):
        background(G=-1.0)
    with pytest.raises(H1ContractError, match="explicit H1Background"):
        two_region_background_identity_residuals("background")  # type: ignore[arg-type]


def test_status_tokens_for_enforced_and_algebraic_results() -> None:
    assert transfer.SCIENTIFIC_STATUS == "CONDITIONALLY_CLOSED"
    assert ALGEBRAIC_VALIDATION_ONLY_STATUS == MANUFACTURED_H1_TRAJECTORIES
    assert CLOCK_BRANCH == "CLK-H1"
    assert transfer.OBSERVATIONAL_STATUS == "NON_OBSERVATIONAL"
    assert transfer.FSIGMA8_STATUS == "NOT_FSIGMA8"
