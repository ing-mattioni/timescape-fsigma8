"""Validation of the H1 background-identity and CLK-H1 gates (review finding F3).

Writes ``artifacts/independent/phase1f_c_r_f3_h1_kinematic_gates_validation.json``
using only the independent package.  Every fixture is a synthetic operator or
continuum validation object with no observational meaning.

Studies:
  K1 the consistent-background constructor satisfies every identity;
  K2 each identity detects its own violation;
  K3 unequal regional clocks violate the GM averaged equations;
  K4 the review's F3 evidence: the frozen 1E-F and 1E-G manufactured
     fixtures violate the background kinematics and fail closed when enforced;
  K5 a 1E-F state (solved free effective inputs) passes every enforced gate,
     and a clock-input shift is caught only by the J_Xi gate;
  K6 flat 1E-G continuum: rank of the gated residual map and a nontrivial
     state passing every enforced gate, for K_D = 0 and K_D != 0;
  K7 heterogeneous 1E-G void geometry: R_Z = R_eff = 0 force the trivial state.

Every tolerance is declared before evaluation; the script exits nonzero if any
gate fails.
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from dataclasses import replace
from importlib.metadata import version
from pathlib import Path

import numpy as np

from timescape_fsigma8.transfer import (
    BACKGROUND_IDENTITY_NAMES,
    CARRIER_PHYSICAL_STATUS,
    COMMON_REFERENCE_NORMAL_WALL_TO_VOID,
    DERIVED_FROM_NORMALIZED_METRIC,
    FIXED_REFERENCE_BRANCH,
    MORPHOLOGY_NORM_TARGET_METRIC_L2,
    ContinuumCarrierSpec,
    ContinuumEllipticClosureConfig,
    ContinuumH1Operator,
    DenseCarrierOperator,
    DenseH1TransmissionBackend,
    EffectiveSectorContinuumBridge,
    EffectiveSectorContract,
    FixedReferenceBranchSpec,
    H1Background,
    H1BackgroundIdentityError,
    H1ClosureError,
    H1Configuration,
    H1KinematicGatePolicy,
    MatrixJet,
    RegionalBulkState,
    RegionalMetricNormalization,
    ScalarJet,
    VectorJet,
    conformal_regional_geometry,
    evaluate_h1_realization,
    flat_regional_geometry,
    layered_morphology,
    two_region_background_identity_residuals,
    two_region_dust_flrw_background,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "independent" / "phase1f_c_r_f3_h1_kinematic_gates_validation.json"

ENFORCE = H1KinematicGatePolicy.ENFORCE
ALGEBRAIC = H1KinematicGatePolicy.ALGEBRAIC_VALIDATION_ONLY
G_FIXTURE = 1.0 / (4.0 * np.pi)
ONE = ScalarJet(1.0, 0.0, 0.0)
N_MATRIX = 6
SHAPE = (6, 3, 3)
EPSILON = 1e-3

# Gates, declared before evaluation.
GATES = {
    "K1_constructor_max_identity_residual": 1e-13,
    "K2_detected_residual_rel_error": 1e-9,
    "K3_min_gm_averaged_residual_for_unequal_clocks": 1e-2,
    "K5_consistent_state_max_gated_residual": 1e-12,
    "K5_clock_shift_increment_error": 1e-13,
    "K6_null_singular_value_rel": 1e-12,
    "K6_nonzero_singular_value_rel": 1e-6,
    "K6_consistent_state_max_gated_residual": 1e-12,
    "K6_min_nontrivial_field_magnitude": 1e-2,
    "K7_min_singular_value_rel": 1e-6,
}


def git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def h1_configuration(policy: H1KinematicGatePolicy, *, probing: bool, coercivity_min: float) -> H1Configuration:
    relaxed = 1e9 if probing else 1e-10
    return H1Configuration(
        A_P_min=1e-8,
        effective_denominator_min=1e-8,
        coercivity_min=coercivity_min,
        partition_product_min=1e-8,
        rho_d_min=1e-8,
        C_P_tolerance=1e-10,
        R_Delta_tolerance=1e-10,
        R_Z_tolerance=relaxed,
        R_eff_tolerance=relaxed,
        K_GM_tolerance=1e-10,
        transmission_value_tolerance=1e-10,
        transmission_flux_tolerance=1e-10,
        source_roundtrip_tolerance=1e-10,
        background_identity_tolerance=2e-12,
        J_Xi_tolerance=1e-10,
        kinematic_gate_policy=policy,
    )


def consistent_background(*, f_v: float, K: float, alpha_w: ScalarJet = ONE) -> H1Background:
    return two_region_dust_flrw_background(
        f_v=f_v, rho_w=1.5, rho_v=0.5, H_w=0.3, H_v=0.5,
        alpha_w=alpha_w, alpha_v=ONE, six_K_D_over_a_D_squared=K, G=G_FIXTURE,
    )


def scalar(value: float, first: float = 0.0, second: float = 0.0) -> ScalarJet:
    return ScalarJet(value, first, second)


def jet_shift(jet: ScalarJet, **shift: float) -> ScalarJet:
    return ScalarJet(jet.value + shift.get("value", 0.0), jet.first + shift.get("first", 0.0),
                     jet.second + shift.get("second", 0.0))


# --------------------------------------------------------------- K1-K3 ----
def study_constructor() -> dict:
    rows = []
    for f_v, K, G in ((0.4, 0.0, G_FIXTURE), (0.15, 0.3, G_FIXTURE), (0.85, -0.7, 0.37), (0.6, 0.0, G_FIXTURE)):
        built = two_region_dust_flrw_background(
            f_v=f_v, rho_w=1.5, rho_v=0.5, H_w=0.3, H_v=0.5, alpha_w=ONE, alpha_v=ONE,
            six_K_D_over_a_D_squared=K, G=G)
        residuals = two_region_background_identity_residuals(built)
        rows.append({"f_v": f_v, "six_K_D_over_a_D_squared": K, "G": G,
                     "max_identity_residual": max(residuals.values())})
    return {"rows": rows, "max": max(r["max_identity_residual"] for r in rows)}


def study_detection() -> dict:
    built = consistent_background(f_v=0.4, K=0.0)
    cases = {
        "regional_hamiltonian_constraint_w": {"R_bar_w": {"value": EPSILON}},
        "regional_hamiltonian_constraint_v": {"R_bar_v": {"value": EPSILON}},
        "regional_raychaudhuri_w": {"Theta_w": {"second": EPSILON}, "H_w": {"second": EPSILON / 3}},
        "regional_raychaudhuri_v": {"Theta_v": {"second": EPSILON}, "H_v": {"second": EPSILON / 3}},
        "regional_dust_continuity_w": {"rho_w": {"second": EPSILON}},
        "regional_dust_continuity_v": {"rho_v": {"second": EPSILON}},
        "partition_kinematics": {"f_v": {"second": EPSILON}},
        "average_expansion": {"Theta": {"second": EPSILON}},
        "two_region_backreaction": {"Q_bar": {"second": EPSILON}},
        "averaged_curvature_W": {"W_bar": {"value": EPSILON}},
        # [GM] (3.8) carries -Q/2: a value shift of Q_bar gives EPSILON/2.
        "averaged_hamiltonian_constraint": {"Q_bar": {"value": EPSILON}},
        # [GM] (3.9) carries +Q.
        "averaged_raychaudhuri": {"Q_bar": {"value": EPSILON}},
    }
    expected = {name: EPSILON for name in cases}
    expected["averaged_hamiltonian_constraint"] = EPSILON / 2.0
    rows = []
    for name, changes in cases.items():
        corrupted = replace(built, **{field: jet_shift(getattr(built, field), **shift)
                                      for field, shift in changes.items()})
        measured = two_region_background_identity_residuals(corrupted)[name]
        rows.append({"identity": name, "perturbation": changes, "expected": expected[name],
                     "measured": measured, "rel_error": abs(measured - expected[name]) / expected[name]})
    # [GM] (3.10) against a mass-weighted clock mismatch (value order f_w rho_w eps).
    f_v, f_w = built.f_v.value, 1.0 - built.f_v.value
    corrupted = replace(built, Xi_w=jet_shift(built.Xi_w, value=EPSILON),
                        Theta=jet_shift(built.Theta, value=f_w * EPSILON),
                        f_v=jet_shift(built.f_v, first=-f_v * f_w * EPSILON))
    mass = two_region_background_identity_residuals(corrupted)["averaged_mass_conservation"]
    return {"epsilon": EPSILON, "rows": rows,
            "max_rel_error": max(r["rel_error"] for r in rows),
            "averaged_mass_conservation_for_clock_mismatch": {
                "measured_max_over_orders": mass,
                "value_order_prediction_f_w_rho_w_epsilon": f_w * built.rho_w.value * EPSILON}}


def study_unequal_clocks() -> dict:
    rows = []
    for alpha in (0.9, 0.95, 1.0, 1.05, 1.1):
        built = consistent_background(f_v=0.4, K=0.0, alpha_w=scalar(alpha))
        residuals = two_region_background_identity_residuals(built)
        proper = 0.6 * built.Theta_w.value + 0.4 * built.Theta_v.value
        rows.append({
            "alpha_w": alpha,
            "max_regional_and_two_region_residual": max(residuals[n] for n in BACKGROUND_IDENTITY_NAMES[:10]),
            "averaged_hamiltonian_constraint": residuals["averaged_hamiltonian_constraint"],
            "averaged_raychaudhuri": residuals["averaged_raychaudhuri"],
            "averaged_mass_conservation": residuals["averaged_mass_conservation"],
            "value_order_prediction_abs_Theta2_minus_proper2_over_3": abs(built.Theta.value**2 - proper**2) / 3.0,
        })
    return {"rows": rows}


# ------------------------------------------------------------------ K4 ----
def matrix_backend(*, wall: np.ndarray, void: np.ndarray, scale: float, interval_bound: float) -> DenseH1TransmissionBackend:
    identity = np.eye(N_MATRIX)
    return DenseH1TransmissionBackend(
        operator=MatrixJet(scale * identity, np.zeros_like(identity), np.zeros_like(identity)),
        wall_source_injection=wall,
        void_source_injection=void,
        value_jump_operator=np.array([[0.0, 0.0, 1.0, -1.0, 0.0, 0.0]]),
        flux_jump_operator=np.array([[0.0, 1.0, 0.0, 0.0, -1.0, 0.0]]),
        flux_normal_convention=COMMON_REFERENCE_NORMAL_WALL_TO_VOID,
        global_mean_weights=np.ones(N_MATRIX),
        constraint_rank_tolerance=1e-12,
        symmetry_tolerance=1e-12,
        operator_time_regularity="C2_COMMON_TIME",
        fixed_reference_constraints=True,
        interval_coercivity_lower_bound=interval_bound,
    )


def identity_contract(delta_theta: VectorJet, delta_xi0: VectorJet) -> EffectiveSectorContract:
    identity = DenseCarrierOperator(MatrixJet(np.eye(N_MATRIX), np.zeros((N_MATRIX, N_MATRIX)), np.zeros((N_MATRIX, N_MATRIX))))
    zeros = np.zeros(N_MATRIX)
    return EffectiveSectorContract(
        delta_theta_operator=identity, delta_theta_inputs=delta_theta,
        delta_xi0_operator=identity, delta_xi0_inputs=delta_xi0,
        J_f_Gamma=VectorJet(zeros, zeros, zeros), partition_time_independent=True)


def frozen_1e_f_fixture_background() -> H1Background:
    """Background of the frozen 1E-F manufactured fixture (test module)."""
    return H1Background(
        f_v=scalar(0.4), rho_w=scalar(1.0), rho_v=scalar(1.0), Theta_w=scalar(0.6),
        Theta_v=scalar(1.2), H_w=scalar(0.2), H_v=scalar(0.4), alpha_w=ONE, alpha_v=ONE,
        R_bar_w=scalar(0.0), R_bar_v=scalar(2.0), Q_bar=scalar(-5.0), W_bar=scalar(-3.0),
        Theta=scalar(0.84), Xi_w=scalar(0.0), Xi_v=scalar(0.0), G=G_FIXTURE,
        six_K_D_over_a_D_squared=0.0)


def frozen_1e_g_fixture_background() -> H1Background:
    """Background of the frozen 1E-G continuum-derived dynamic fixture."""
    return H1Background(
        f_v=scalar(0.4), rho_w=scalar(1.0), rho_v=scalar(1.0), Theta_w=scalar(0.6),
        Theta_v=scalar(1.2), H_w=scalar(0.2), H_v=scalar(0.4), alpha_w=ONE, alpha_v=ONE,
        R_bar_w=scalar(0.0), R_bar_v=scalar(-0.10755555555555557),
        Q_bar=scalar(-5.0, -26.979222614841003), W_bar=scalar(-3.0), Theta=scalar(0.84),
        Xi_w=scalar(0.6), Xi_v=scalar(1.2), G=G_FIXTURE, six_K_D_over_a_D_squared=0.0)


# --------------------------------------------------------------- K5 ----
def solve_consistent_1e_f_state(background: H1Background, backend, bulk: RegionalBulkState):
    probe = h1_configuration(ALGEBRAIC, probing=True, coercivity_min=0.5)
    zeros = np.zeros(N_MATRIX)
    e0 = np.linspace(0.05, 0.3, N_MATRIX)

    def run(e1, e2, x0, configuration=probe):
        return evaluate_h1_realization(
            regional_bulk=bulk, background=background, backend=backend,
            effective_sector=identity_contract(VectorJet(e0, e1, e2), VectorJet(x0, zeros, zeros)),
            configuration=configuration)

    base, unit = run(zeros, zeros, zeros), run(np.ones(N_MATRIX), zeros, zeros)
    e1 = -base.R_eff / (unit.R_eff - base.R_eff)
    base, unit = run(e1, zeros, zeros), run(e1, np.ones(N_MATRIX), zeros)
    e2 = -base.R_Z / (unit.R_Z - base.R_Z)
    x0 = np.array(run(e1, e2, zeros).J_Xi)
    return run, e1, e2, x0


def study_1e_f() -> dict:
    backend = matrix_backend(wall=np.eye(N_MATRIX)[0], void=np.eye(N_MATRIX)[-1], scale=2.0, interval_bound=1.0)
    bulk = RegionalBulkState(Delta_w=0.3, Z_w=0.2, Delta_v=-0.1, Z_v=0.4)
    rows = []
    for K in (0.0, 0.3):
        background = consistent_background(f_v=0.4, K=K)
        run, e1, e2, x0 = solve_consistent_1e_f_state(background, backend, bulk)
        result = run(e1, e2, x0, h1_configuration(ENFORCE, probing=False, coercivity_min=0.5))
        gated = max(max(result.background_identity_residuals.values()), result.J_Xi_max_abs,
                    *(float(np.max(np.abs(x))) for x in (result.C_P, result.R_Delta, result.R_Z, result.R_eff, result.K_GM)))
        shift = 0.05 * np.linspace(-1.0, 1.0, N_MATRIX)
        shifted = run(e1, e2, x0 + shift)
        baseline = run(e1, e2, x0)
        increment_error = float(np.max(np.abs((shifted.J_Xi - baseline.J_Xi) + shift)))
        other_residuals = max(float(np.max(np.abs(x))) for x in (shifted.R_Z, shifted.R_eff, shifted.C_P))
        try:
            run(e1, e2, x0 + shift, h1_configuration(ENFORCE, probing=False, coercivity_min=0.5))
            clock_gate = "NOT_RAISED"
        except H1ClosureError as error:
            clock_gate = str(error).split()[0].split("=")[0]
        rows.append({
            "six_K_D_over_a_D_squared": K, "scientific_status": result.scientific_status,
            "max_gated_residual": gated,
            "field_max_abs": {"Delta_d": float(np.max(np.abs(result.Delta_d.value))),
                              "Z": float(np.max(np.abs(result.Z))),
                              "Delta_eff": float(np.max(np.abs(result.Delta_eff.value))),
                              "F_v": float(np.max(np.abs(result.F_v.value)))},
            "clock_shift_increment_error": increment_error,
            "clock_shift_other_residual_max": other_residuals,
            "clock_shift_enforced_error": clock_gate,
        })
    # Frozen manufactured 1E-F fixture (same backend family, phi injections).
    phi = np.array([5.0, -1.0, -1.0, -1.0, -1.0, -1.0]) / 6.0
    fixture_backend = matrix_backend(wall=phi, void=phi, scale=1.0, interval_bound=0.5)
    fixture = frozen_1e_f_fixture_background()
    zero_contract = identity_contract(VectorJet(np.zeros(N_MATRIX), np.zeros(N_MATRIX), np.zeros(N_MATRIX)),
                                      VectorJet(np.zeros(N_MATRIX), np.zeros(N_MATRIX), np.zeros(N_MATRIX)))
    try:
        evaluate_h1_realization(regional_bulk=RegionalBulkState(1.0, 0.4, 1.0, 0.8), background=fixture,
                                backend=fixture_backend, effective_sector=zero_contract,
                                configuration=h1_configuration(ENFORCE, probing=True, coercivity_min=0.5))
        fixture_enforced = "NOT_RAISED"
    except H1BackgroundIdentityError as error:
        fixture_enforced = str(error).split()[0]
    return {
        "consistent_states": rows,
        "frozen_manufactured_fixture": {
            "background_identity_residuals": dict(two_region_background_identity_residuals(fixture)),
            "enforced_first_failing_identity": fixture_enforced,
        },
    }


# ------------------------------------------------------------ K6-K7 ----
def normalization(identity: str, volume: float, convention: str = "UNIT_REFERENCE_COMOVING_METRIC") -> RegionalMetricNormalization:
    return RegionalMetricNormalization(
        normalization_id=identity, scale_factor_reference_epoch="F3_VALIDATION_EPOCH",
        scale_factor_reference_value=1.0, metric_scale_convention=convention,
        reference_comoving_volume=volume, volume_provenance=DERIVED_FROM_NORMALIZED_METRIC,
        consistency_tolerance=2e-12)


def continuum_bridge(policy: H1KinematicGatePolicy, *, probing: bool, heterogeneous: bool) -> EffectiveSectorContinuumBridge:
    weights = np.full(SHAPE, 1.0 / np.prod(SHAPE))
    morphology = layered_morphology(morphology_id="f3-consistent-one-wall-cell", grid_shape=SHAPE, axis=0,
                                    wall_cell_count=1, wall_pullback_id="Phi_w_f3", void_pullback_id="Phi_v_f3")
    configuration = ContinuumEllipticClosureConfig(
        ellipticity_min=1e-6, coercivity_min=5e-2, source_compatibility_tolerance=2e-11,
        global_mean_tolerance=2e-11, interface_value_tolerance=2e-11, interface_flux_tolerance=2e-11,
        volume_fraction_tolerance=2e-11, equal_geometry_identity_tolerance=2e-10,
        convergence_l2_min_rate=1.8, convergence_energy_min_rate=0.8,
        morphology_sensitivity_norm=MORPHOLOGY_NORM_TARGET_METRIC_L2,
        morphology_sensitivity_reference_scale=1.0, morphology_sensitivity_floor=1e-12,
        morphology_convergence_tolerance=2e-2, kernel_tolerance=1e-10, symmetry_tolerance=1e-12,
        downstream_configuration=h1_configuration(policy, probing=probing, coercivity_min=5e-2))
    target = flat_regional_geometry(region_id="target", grid_shape=SHAPE, pullback_provenance="Phi_D_f3",
                                    normalization=normalization("f3-target", 1.0),
                                    metadata={"classification": "SYNTHETIC_VALIDATION_ONLY"})
    carrier = ContinuumCarrierSpec(
        dimension=3, grid_shape=SHAPE, periodicity=(True,) * 3, reference_measure_weights=weights,
        grid_spacing=tuple(1.0 / n for n in SHAPE), target_geometry=target,
        topology="PERIODIC_REFERENCE_TORUS", physical_status=CARRIER_PHYSICAL_STATUS,
        target_scalarization_id="L_D_F3_VALIDATION")
    wall = flat_regional_geometry(region_id="wall", grid_shape=SHAPE, pullback_provenance=morphology.wall_pullback_id,
                                  normalization=normalization("f3-wall", float(np.sum(weights * morphology.wall_domain))),
                                  metadata={"classification": "SYNTHETIC_VALIDATION_ONLY"})
    if heterogeneous:
        indices = np.indices(SHAPE)
        conformal = 1.0 + 0.3 * np.cos(2.0 * np.pi * indices[1] / 3.0) * (indices[0] >= 1)
        void = conformal_regional_geometry(
            region_id="void", conformal_factor=conformal, dimension=3,
            curvature_class="SYNTHETIC_CONFORMAL_COMPARATOR", pullback_provenance=morphology.void_pullback_id,
            normalization=normalization("f3-heterogeneous-void",
                                        float(np.sum(weights * conformal**3 * morphology.void_domain)),
                                        "SYNTHETIC_HETEROGENEOUS_CONFORMAL_FACTOR"),
            metadata={"classification": "SYNTHETIC_VALIDATION_ONLY"})
    else:
        void = flat_regional_geometry(region_id="void", grid_shape=SHAPE, pullback_provenance=morphology.void_pullback_id,
                                      normalization=normalization("f3-void", float(np.sum(weights * morphology.void_domain))),
                                      metadata={"classification": "SYNTHETIC_VALIDATION_ONLY"})
    branch = FixedReferenceBranchSpec(
        branch_id=FIXED_REFERENCE_BRANCH, fixed_reference_partition=True, fixed_interface=True,
        fixed_comoving_pullback_geometries=True, fixed_target_scalarization=True,
        homogeneous_background_clock_map=True, spatial_clock_perturbation=False)
    operator = ContinuumH1Operator(carrier=carrier, morphology=morphology, wall_geometry=wall, void_geometry=void,
                                   branch=branch, configuration=configuration, continuum_coercivity_bound=0.1)
    return EffectiveSectorContinuumBridge(operator=operator, branch=branch, configuration=configuration)


def bridge_evaluate(bridge, background: H1Background, bulk, *, a_v: float):
    return bridge.evaluate(
        regional_bulk=RegionalBulkState(*(float(x) for x in bulk)), background=background,
        a_w=1.0, a_v=a_v, equal_geometry_probe=None,
        volume_fraction_consistency_classification="F3_CONSISTENT_MANUFACTURED_BACKGROUND",
        morphology_sensitivity_diagnostics={}, discretization_convergence_metrics={})


def void_scale(bridge, f_v: float) -> float:
    wall = bridge.operator.geometric_void_fraction(a_w=1.0, a_v=1.0)
    return (f_v / (1.0 - f_v) * (1.0 - wall) / wall) ** (1.0 / 3.0)


def residual_maps(bridge, background: H1Background, a_v: float) -> dict[str, np.ndarray]:
    columns: dict[str, list] = {"R_Z": [], "R_eff": [], "J_Xi": []}
    for index in range(4):
        unit = np.zeros(4)
        unit[index] = 1.0
        downstream = bridge_evaluate(bridge, background, unit, a_v=a_v).downstream_phase1e_f
        for name in columns:
            columns[name].append(np.asarray(getattr(downstream, name)))
    return {name: np.array(column).T for name, column in columns.items()}


def relative_svd(maps: dict[str, np.ndarray], blocks: tuple[str, ...]):
    _, singular, right = np.linalg.svd(np.vstack([maps[name] for name in blocks]))
    return singular / singular[0], right


def study_continuum(heterogeneous: bool) -> dict:
    probe = continuum_bridge(ALGEBRAIC, probing=True, heterogeneous=heterogeneous)
    enforced = continuum_bridge(ENFORCE, probing=False, heterogeneous=heterogeneous)
    rows = []
    for K in (0.0, 0.3):
        background = consistent_background(f_v=0.6, K=K)
        a_v = void_scale(probe, 0.6)
        maps = residual_maps(probe, background, a_v)
        row = {"six_K_D_over_a_D_squared": K}
        for label, blocks in (("R_Z", ("R_Z",)), ("R_Z+R_eff", ("R_Z", "R_eff")),
                              ("R_Z+R_eff+J_Xi", ("R_Z", "R_eff", "J_Xi"))):
            singular, _ = relative_svd(maps, blocks)
            row[f"relative_singular_values[{label}]"] = [float(x) for x in singular]
        singular, right = relative_svd(maps, ("R_Z", "R_eff", "J_Xi"))
        state = right[-1]
        row["least_squares_bulk_state"] = [float(x) for x in state]
        try:
            result = bridge_evaluate(enforced, background, state, a_v=a_v)
            downstream = result.downstream_phase1e_f
            row["enforced_outcome"] = {
                "scientific_status_1e_g": result.scientific_status,
                "scientific_status_1e_f": downstream.scientific_status,
                "max_gated_residual": max(
                    max(downstream.background_identity_residuals.values()), downstream.J_Xi_max_abs,
                    *(float(np.max(np.abs(x))) for x in (downstream.R_Z, downstream.R_eff, downstream.C_P, downstream.K_GM))),
                "field_max_abs": {
                    "Delta_d": float(np.max(np.abs(downstream.Delta_d.value))),
                    "Z": float(np.max(np.abs(downstream.Z))),
                    "Delta_eff": float(np.max(np.abs(downstream.Delta_eff.value))),
                    "F_v": float(np.max(np.abs(downstream.F_v.value))),
                    "E_DeltaTheta_Gamma": float(np.max(np.abs(result.E_DeltaTheta_Gamma.value))),
                    "E_DeltaXi_0_Gamma": float(np.max(np.abs(result.E_DeltaXi_0_Gamma.value))),
                },
            }
        except (H1ClosureError, H1BackgroundIdentityError) as error:
            row["enforced_outcome"] = {"raised": type(error).__name__, "gate": str(error).split("=")[0]}
        rows.append(row)
    result = {"rows": rows}
    if not heterogeneous:
        # Frozen 1E-G dynamic fixture: same bridge family, review F3 table.
        fixture = frozen_1e_g_fixture_background()
        a_v = (2.0 / 15.0) ** (1.0 / 3.0)
        downstream = bridge_evaluate(probe, fixture, (1.0, 0.4, 1.0, 0.8), a_v=a_v).downstream_phase1e_f
        try:
            bridge_evaluate(enforced, fixture, (1.0, 0.4, 1.0, 0.8), a_v=a_v)
            outcome = "NOT_RAISED"
        except H1BackgroundIdentityError as error:
            outcome = str(error).split()[0]
        result["frozen_dynamic_fixture"] = {
            "background_identity_residuals": dict(downstream.background_identity_residuals),
            "J_Xi_min": float(np.min(downstream.J_Xi)),
            "J_Xi_max": float(np.max(downstream.J_Xi)),
            "R_Z_max_abs": float(np.max(np.abs(downstream.R_Z))),
            "R_eff_max_abs": float(np.max(np.abs(downstream.R_eff))),
            "enforced_first_failing_identity": outcome,
        }
    return result


def main() -> int:
    constructor = study_constructor()
    detection = study_detection()
    clocks = study_unequal_clocks()
    matrix = study_1e_f()
    flat = study_continuum(heterogeneous=False)
    heterogeneous = study_continuum(heterogeneous=True)

    flat_k0, flat_k3 = flat["rows"]
    measured = {
        "K1_constructor_max_identity_residual": constructor["max"],
        "K2_detected_residual_rel_error": detection["max_rel_error"],
        "K3_min_gm_averaged_residual_for_unequal_clocks": min(
            r["averaged_hamiltonian_constraint"] for r in clocks["rows"] if r["alpha_w"] != 1.0),
        "K5_consistent_state_max_gated_residual": max(r["max_gated_residual"] for r in matrix["consistent_states"]),
        "K5_clock_shift_increment_error": max(r["clock_shift_increment_error"] for r in matrix["consistent_states"]),
        "K6_null_singular_value_rel": max(
            flat_k0["relative_singular_values[R_Z+R_eff+J_Xi]"][2],
            flat_k0["relative_singular_values[R_Z+R_eff+J_Xi]"][3],
            flat_k3["relative_singular_values[R_Z+R_eff+J_Xi]"][3]),
        "K6_nonzero_singular_value_rel": min(
            flat_k0["relative_singular_values[R_Z+R_eff+J_Xi]"][1],
            flat_k3["relative_singular_values[R_Z+R_eff+J_Xi]"][2]),
        "K6_consistent_state_max_gated_residual": max(
            r["enforced_outcome"].get("max_gated_residual", np.inf) for r in flat["rows"]),
        # Z is excluded: for K_D != 0 the closed state has Z = 0 (observation
        # recorded below); every other target and bridge field is nonzero.
        "K6_min_nontrivial_field_magnitude": min(
            min(value for name, value in r["enforced_outcome"].get("field_max_abs", {"missing": 0.0}).items()
                if name != "Z")
            for r in flat["rows"]),
        "K7_min_singular_value_rel": min(r["relative_singular_values[R_Z+R_eff]"][3] for r in heterogeneous["rows"]),
    }
    lower_bounds = {"K3_min_gm_averaged_residual_for_unequal_clocks", "K6_nonzero_singular_value_rel",
                    "K6_min_nontrivial_field_magnitude", "K7_min_singular_value_rel"}
    gates = {
        name: {"gate": GATES[name], "measured": float(value),
               "passed": bool(value >= GATES[name]) if name in lower_bounds else bool(value <= GATES[name])}
        for name, value in measured.items()
    }
    qualitative = {
        "K4_1e_f_fixture_fails_closed": matrix["frozen_manufactured_fixture"]["enforced_first_failing_identity"]
        == "regional_hamiltonian_constraint_w",
        "K4_1e_g_fixture_fails_closed": flat["frozen_dynamic_fixture"]["enforced_first_failing_identity"]
        == "regional_hamiltonian_constraint_w",
        "K5_enforced_status": all(r["scientific_status"] == "CONDITIONALLY_CLOSED" for r in matrix["consistent_states"]),
        "K5_clock_shift_caught_only_by_J_Xi": all(
            r["clock_shift_enforced_error"] == "J_Xi" and r["clock_shift_other_residual_max"] <= 1e-12
            for r in matrix["consistent_states"]),
        "K6_enforced_status": all(
            r["enforced_outcome"].get("scientific_status_1e_g") == "CONDITIONALLY_DERIVED_CONTINUUM_REALIZATION"
            for r in flat["rows"]),
        "K7_enforced_fails_closed": all(r["enforced_outcome"].get("raised") == "H1ClosureError" for r in heterogeneous["rows"]),
    }
    all_passed = all(g["passed"] for g in gates.values()) and all(qualitative.values())
    observations = {
        "K6_closed_state_Z_max_abs_by_K_D": {
            str(r["six_K_D_over_a_D_squared"]): r["enforced_outcome"]["field_max_abs"]["Z"] for r in flat["rows"]},
        "K6_note": ("numerical observation, not a derived identity: with K_D = 0 the J_Xi condition is "
                    "implied by R_Z = R_eff = 0 on the flat continuum (rank 2); with K_D != 0 it is "
                    "independent (rank 3) and the one-dimensional closed set has Z = 0 to roundoff"),
    }
    artifact = {
        "title": "H1 background-identity and CLK-H1 kinematic gates (review finding F3)",
        "schema_version": 1,
        "scope": {
            "observational_interpretation": "NOT_GRANTED",
            "fixtures": "SYNTHETIC_OPERATOR_AND_CONTINUUM_VALIDATION_ONLY",
            "states": "INSTANTANEOUS_MANUFACTURED_STATES_NOT_ALL_TIME_TRAJECTORIES",
            "clock_branch": "CLK-H1",
        },
        "provenance": {"repository_head": git_head(), "python": platform.python_version(),
                       "numpy": version("numpy"), "scipy": version("scipy"), "platform": platform.platform()},
        "gates": gates,
        "qualitative_gates": qualitative,
        "observations": observations,
        "all_gates_passed": all_passed,
        "K1_constructor": constructor,
        "K2_detection": detection,
        "K3_unequal_clocks": clocks,
        "K4_K5_matrix_runtime": matrix,
        "K4_K6_flat_continuum": flat,
        "K7_heterogeneous_continuum": heterogeneous,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(artifact, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    for name, gate in gates.items():
        print(f"{'PASS' if gate['passed'] else 'FAIL'} {name}: {gate['measured']:.3e} (gate {gate['gate']:.1e})")
    for name, passed in qualitative.items():
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
