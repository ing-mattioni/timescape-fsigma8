"""Deterministic validation studies for the conditional Phase 1F-A runtime.

All fixtures are synthetic theoretical/operator validations.  They have no
observational, tracer, spectrum-normalisation, or physical-interface meaning.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from timescape_fsigma8.phase1f_a import (
    EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE,
    EXTERNAL_CLOSURE,
    NO_FLUX_REGIONAL_INTERFACE_PERIODIC_CARRIER,
    REGIONAL_METRIC_MEAN_ZERO,
    REGIONAL_SOURCE_MEAN_ZERO,
    SINGLE_REGIONAL_CONSTANT_REMOVED,
    SYNTHETIC_VALIDATION_ONLY,
    BoundaryKernelPolicy,
    DressedSpacetimeMapClosure,
    ExternalBoostDivergenceClosure,
    Phase1FAContractError,
    Phase1FADegeneracyError,
    Phase1FADimensionalContractError,
    Phase1FANumerics,
    Phase1FARealization,
    Phase1FAScientificState,
    RegionalDomainSpec,
    RegionalZeroModeClosure,
    carrier_generalized_spectrum,
    regional_laplace_beltrami_spectrum,
    spectral_transfer_kernel,
)
from timescape_fsigma8.transfer import (
    CARRIER_PHYSICAL_STATUS,
    DERIVED_FROM_NORMALIZED_METRIC,
    FIXED_REFERENCE_BRANCH,
    MORPHOLOGY_NORM_TARGET_METRIC_L2,
    ContinuumCarrierSpec,
    ContinuumEllipticClosureConfig,
    ContinuumH1Operator,
    ContinuumTransfer,
    FixedReferenceBranchSpec,
    H1Configuration,
    H1KinematicGatePolicy,
    RegionalMetricNormalization,
    flat_regional_geometry,
    layered_morphology,
)


OUTPUT_DEFAULT = Path(
    "artifacts/independent/phase1f_a_h1_carrier_dressed_closure_validation.json"
)


def numerics() -> Phase1FANumerics:
    return Phase1FANumerics(
        elliptic_residual_tolerance=2e-10,
        mean_tolerance=2e-11,
        source_compatibility_tolerance=2e-11,
        volume_consistency_tolerance=2e-11,
        carrier_mean_tolerance=2e-10,
        intertwining_tolerance=5e-10,
        eigenpair_tolerance=2e-9,
        basis_normalization_tolerance=2e-10,
        boost_residual_tolerance=2e-10,
        dressed_mean_tolerance=2e-11,
        residual_norm_floor=1e-14,
        maximum_condition_number=1e12,
    )


def h1_configuration() -> H1Configuration:
    return H1Configuration(
        A_P_min=1e-8,
        effective_denominator_min=1e-8,
        coercivity_min=5e-2,
        partition_product_min=1e-8,
        rho_d_min=1e-8,
        C_P_tolerance=1e-10,
        R_Delta_tolerance=1e-10,
        R_Z_tolerance=1e-10,
        R_eff_tolerance=1e-10,
        K_GM_tolerance=1e-10,
        transmission_value_tolerance=1e-10,
        transmission_flux_tolerance=1e-10,
        source_roundtrip_tolerance=1e-10,
        background_identity_tolerance=2e-12,
        J_Xi_tolerance=1e-10,
        kinematic_gate_policy=H1KinematicGatePolicy.ENFORCE,
    )


def continuum_configuration() -> ContinuumEllipticClosureConfig:
    return ContinuumEllipticClosureConfig(
        ellipticity_min=1e-6,
        coercivity_min=5e-2,
        source_compatibility_tolerance=2e-11,
        global_mean_tolerance=2e-11,
        interface_value_tolerance=2e-11,
        interface_flux_tolerance=2e-11,
        volume_fraction_tolerance=2e-11,
        equal_geometry_identity_tolerance=2e-10,
        convergence_l2_min_rate=1.8,
        convergence_energy_min_rate=0.8,
        morphology_sensitivity_norm=MORPHOLOGY_NORM_TARGET_METRIC_L2,
        morphology_sensitivity_reference_scale=1.0,
        morphology_sensitivity_floor=1e-12,
        morphology_convergence_tolerance=2e-2,
        kernel_tolerance=1e-10,
        symmetry_tolerance=1e-12,
        downstream_configuration=h1_configuration(),
    )


def normalization(identity: str, volume: float) -> RegionalMetricNormalization:
    return RegionalMetricNormalization(
        normalization_id=identity,
        scale_factor_reference_epoch="PHASE1F_A_VALIDATION_EPOCH",
        scale_factor_reference_value=1.0,
        metric_scale_convention="UNIT_REFERENCE_COMOVING_METRIC",
        reference_comoving_volume=volume,
        volume_provenance=DERIVED_FROM_NORMALIZED_METRIC,
        consistency_tolerance=2e-12,
    )


def make_realization(shape: tuple[int, ...]) -> Phase1FARealization:
    dimension = len(shape)
    weights = np.full(shape, 1.0 / np.prod(shape))
    morphology = layered_morphology(
        morphology_id=f"validation-layered-{'x'.join(map(str, shape))}",
        grid_shape=shape,
        axis=0,
        wall_cell_count=shape[0] // 2,
        wall_pullback_id="Phi_w_validation",
        void_pullback_id="Phi_v_validation",
    )
    wall_measure = float(np.sum(weights * morphology.wall_domain))
    void_measure = float(np.sum(weights * morphology.void_domain))
    target = flat_regional_geometry(
        region_id="target",
        grid_shape=shape,
        pullback_provenance="Phi_D_validation",
        normalization=normalization("target-validation", 1.0),
        metadata={"classification": "SYNTHETIC_VALIDATION_ONLY"},
    )
    carrier = ContinuumCarrierSpec(
        dimension=dimension,
        grid_shape=shape,
        periodicity=(True,) * dimension,
        reference_measure_weights=weights,
        grid_spacing=tuple(1.0 / n for n in shape),
        target_geometry=target,
        topology="PERIODIC_REFERENCE_TORUS",
        physical_status=CARRIER_PHYSICAL_STATUS,
        target_scalarization_id="L_D_VALIDATION_ONLY",
    )
    wall = flat_regional_geometry(
        region_id="wall",
        grid_shape=shape,
        pullback_provenance=morphology.wall_pullback_id,
        normalization=normalization("wall-validation", wall_measure),
        metadata={"classification": "SYNTHETIC_VALIDATION_ONLY"},
    )
    void = flat_regional_geometry(
        region_id="void",
        grid_shape=shape,
        pullback_provenance=morphology.void_pullback_id,
        normalization=normalization("void-validation", void_measure),
        metadata={"classification": "SYNTHETIC_VALIDATION_ONLY"},
    )
    operator = ContinuumH1Operator(
        carrier=carrier,
        morphology=morphology,
        wall_geometry=wall,
        void_geometry=void,
        branch=FixedReferenceBranchSpec(
            branch_id=FIXED_REFERENCE_BRANCH,
            fixed_reference_partition=True,
            fixed_interface=True,
            fixed_comoving_pullback_geometries=True,
            fixed_target_scalarization=True,
            homogeneous_background_clock_map=True,
            spatial_clock_perturbation=False,
        ),
        configuration=continuum_configuration(),
        continuum_coercivity_bound=0.1,
    )
    state = Phase1FAScientificState(
        operator=operator,
        morphology_provenance="EXPLICIT_SYNTHETIC_VALIDATION_MORPHOLOGY",
        normalization_provenance="EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE",
        scientific_classification="CONDITIONAL_THEORETICAL_FORWARD_REALIZATION",
    )
    return Phase1FARealization(scientific_state=state, numerics=numerics())


def domain(runtime: Phase1FARealization, region: str) -> RegionalDomainSpec:
    return RegionalDomainSpec(scientific_state=runtime.scientific_state, region=region)


def boundary(region: str) -> BoundaryKernelPolicy:
    return BoundaryKernelPolicy(
        domain=region,
        boundary_condition_kind=NO_FLUX_REGIONAL_INTERFACE_PERIODIC_CARRIER,
        nullspace_handling=SINGLE_REGIONAL_CONSTANT_REMOVED,
        compatibility_condition=REGIONAL_SOURCE_MEAN_ZERO,
        provenance="EXPLICIT_VALIDATION_REGIONAL_BOUNDARY_POLICY",
    )


def zero_mode(region: str) -> RegionalZeroModeClosure:
    return RegionalZeroModeClosure(
        mean_condition=REGIONAL_METRIC_MEAN_ZERO,
        spatial_measure_identity=f"a_{region}^3 dmu_gamma_{region}",
        scale_factor=1.0,
        provenance=f"{region}-validation-mean-zero",
        classification=EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE,
        frame=f"{region.upper()}_COMOVING_DUST_FRAME",
        domain=region,
    )


def fields(shape: tuple[int, ...]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    grid = np.indices(shape, dtype=float)
    scalar = np.sin(2.0 * np.pi * grid[-1] / shape[-1])
    if len(shape) > 1:
        scalar = scalar + 0.25 * np.cos(2.0 * np.pi * grid[-2] / shape[-2])
    discrete = (
        -4.0 * np.sin(np.pi / shape[-1]) ** 2 / (1.0 / shape[-1]) ** 2
        * np.sin(2.0 * np.pi * grid[-1] / shape[-1])
    )
    continuum = -(2.0 * np.pi) ** 2 * np.sin(2.0 * np.pi * grid[-1] / shape[-1])
    if len(shape) > 1:
        discrete += (
            0.25
            * -4.0
            * np.sin(np.pi / shape[-2]) ** 2
            / (1.0 / shape[-2]) ** 2
            * np.cos(2.0 * np.pi * grid[-2] / shape[-2])
        )
        continuum += -0.25 * (2.0 * np.pi) ** 2 * np.cos(
            2.0 * np.pi * grid[-2] / shape[-2]
        )
    return scalar, discrete, continuum


def supported(runtime: Phase1FARealization, values: np.ndarray, region: str) -> np.ndarray:
    mask = (
        runtime.scientific_state.operator.morphology.wall_domain
        if region == "wall"
        else runtime.scientific_state.operator.morphology.void_domain
    )
    return np.where(mask, values, 0.0).reshape(-1)


def reconstruct_pair(runtime: Phase1FARealization):
    shape = runtime.scientific_state.operator.carrier.grid_shape
    scalar, source, _ = fields(shape)
    scalar = 0.1 * scalar
    source = 0.1 * source
    wall = runtime.reconstruct_density(
        delta_cgi=supported(runtime, source, "wall"),
        regional_geometry=domain(runtime, "wall"),
        boundary_policy=boundary("wall"),
        zero_mode_closure=zero_mode("wall"),
        provenance="VALIDATION_WALL_DENSITY",
    )
    void = runtime.reconstruct_density(
        delta_cgi=supported(runtime, 0.6 * source, "void"),
        regional_geometry=domain(runtime, "void"),
        boundary_policy=boundary("void"),
        zero_mode_closure=zero_mode("void"),
        provenance="VALIDATION_VOID_DENSITY",
    )
    return wall, void, scalar


def validate() -> dict[str, object]:
    runtime = make_realization((4, 4, 4))
    operator = runtime.scientific_state.operator
    wall, void, scalar = reconstruct_pair(runtime)
    wall_mask = operator.morphology.wall_domain.reshape(-1)
    void_mask = ~wall_mask
    volumes = operator.physical_regional_volumes(a_w=1.0, a_v=1.0)
    carrier = runtime.assemble_density(
        wall_density=wall,
        void_density=void,
        wall_background_density=2.0,
        void_background_density=1.0,
        wall_physical_volume=volumes[0],
        void_physical_volume=volumes[1],
        h1_partition=operator.morphology,
    )

    zero_mode_difference = float(np.max(np.abs((scalar + 3.0) - scalar)))
    expected_wall_contrast = (carrier.b_wall - 1.0) + carrier.b_wall * wall.delta_m[wall_mask]
    expected_void_contrast = (carrier.b_void - 1.0) + carrier.b_void * void.delta_m[void_mask]

    expansion = runtime.reconstruct_expansion(
        z_cgi=supported(runtime, 0.35 * fields((4, 4, 4))[1], "wall"),
        regional_geometry=domain(runtime, "wall"),
        boundary_policy=boundary("wall"),
        zero_mode_closure=zero_mode("wall"),
        background_expansion_identity="bar_Theta_w=3H_w",
        provenance="VALIDATION_EXPANSION_SCALAR",
    )
    expansion_exact = 0.35 * fields((4, 4, 4))[0]

    regional_spectrum = regional_laplace_beltrami_spectrum(
        regional_geometry=domain(runtime, "wall"),
        boundary_policy=boundary("wall"),
        scale_factor=0.8,
        scale_units="INVERSE_REFERENCE_LENGTH",
        mode_count=4,
        numerics=runtime.numerics,
        provenance="VALIDATION_REGIONAL_SPECTRUM",
    )
    carrier_spectrum = carrier_generalized_spectrum(
        scientific_state=runtime.scientific_state,
        mode_count=10,
        numerics=runtime.numerics,
        provenance="VALIDATION_CARRIER_SPECTRUM",
    )
    kernel = spectral_transfer_kernel(
        regional_spectrum=regional_spectrum,
        carrier_spectrum=carrier_spectrum,
        continuum_transfer=ContinuumTransfer(operator),
        numerics=runtime.numerics,
        provenance="VALIDATION_MODE_TRANSFER",
    )
    off_diagonal = np.array(kernel.kernel, copy=True)
    for index in range(min(off_diagonal.shape)):
        off_diagonal[index, index] = 0.0

    boost_source = supported(runtime, 0.2 * fields((4, 4, 4))[1], "wall")
    boost = runtime.reconstruct_boost(
        regional_or_wall_geometry=domain(runtime, "wall"),
        boost_closure=ExternalBoostDivergenceClosure(
            divergence=boost_source,
            source_frame="VOLUME_AVERAGE_DUST_FRAME",
            destination_frame="WALL_FRAME_THEORETICAL_REFERENCE",
            time_coordinate="t_D",
            spatial_metric_identity="wall-validation",
            units="INVERSE_COMMON_TIME",
            domain="wall",
            normalization_closure_id=zero_mode("wall").provenance,
            provenance="EXTERNAL_SYNTHETIC_BOOST_VALIDATION",
            classification=EXTERNAL_CLOSURE,
        ),
        boundary_policy=boundary("wall"),
        zero_mode_closure=zero_mode("wall"),
    )
    incompatible_boost_rejected = False
    try:
        bad = np.zeros(operator.size)
        bad[wall_mask] = 1.0
        runtime.reconstruct_boost(
            regional_or_wall_geometry=domain(runtime, "wall"),
            boost_closure=ExternalBoostDivergenceClosure(
                divergence=bad,
                source_frame="VOLUME_AVERAGE_DUST_FRAME",
                destination_frame="WALL_FRAME_THEORETICAL_REFERENCE",
                time_coordinate="t_D",
                spatial_metric_identity="wall-validation",
                units="INVERSE_COMMON_TIME",
                domain="wall",
                normalization_closure_id=zero_mode("wall").provenance,
                provenance="INCOMPATIBLE_BOOST_ADVERSARIAL",
                classification=EXTERNAL_CLOSURE,
            ),
            boundary_policy=boundary("wall"),
            zero_mode_closure=zero_mode("wall"),
        )
    except Phase1FADegeneracyError:
        incompatible_boost_rejected = True

    size = operator.size
    dressed_closure = DressedSpacetimeMapClosure(
        source_frame="H1_PHYSICAL_CARRIER_DENSITY_FRAME",
        destination_frame="SYNTHETIC_DRESSED_VALIDATION_FRAME",
        time_mapping="IDENTITY_VALIDATION_TIME",
        spatial_mapping="REVERSE_INDEX_VALIDATION_PULLBACK",
        destination_spatial_metric="SYNTHETIC_POSITIVE_DESTINATION_METRIC",
        destination_source_indices=np.arange(size - 1, -1, -1),
        destination_reference_weights=np.full(size, 1.0 / size),
        destination_metric_volume_ratio=np.linspace(0.8, 1.2, size),
        destination_measure_jacobian=np.linspace(1.1, 0.9, size),
        provenance="SYNTHETIC_DRESSED_MAP_VALIDATION_ONLY",
        scientific_classification=SYNTHETIC_VALIDATION_ONLY,
        spatial_dimension=3,
    )
    dressed = runtime.map_dressed_density(
        carrier_density=carrier, dressed_map_closure=dressed_closure
    )
    direct_delta = carrier.delta_m_carrier[dressed_closure.destination_source_indices]

    reduced_rejections: dict[str, bool] = {}
    for reduced_shape in ((8,), (6, 6)):
        reduced = make_realization(reduced_shape)
        coordinate = np.indices(reduced_shape, dtype=float)[-1]
        reduced_source = np.sin(2.0 * np.pi * coordinate / reduced_shape[-1])
        if len(reduced_shape) == 1:
            reduced_source = np.tile(np.array([1.0, -1.0]), reduced_shape[0] // 2)
        reduced_wall = reduced.reconstruct_density(
            delta_cgi=supported(reduced, reduced_source, "wall"),
            regional_geometry=domain(reduced, "wall"),
            boundary_policy=boundary("wall"),
            zero_mode_closure=zero_mode("wall"),
            provenance="REDUCED_OPERATOR_VALIDATION",
        )
        reduced_void = reduced.reconstruct_density(
            delta_cgi=supported(reduced, reduced_source, "void"),
            regional_geometry=domain(reduced, "void"),
            boundary_policy=boundary("void"),
            zero_mode_closure=zero_mode("void"),
            provenance="REDUCED_OPERATOR_VALIDATION",
        )
        rejected = False
        try:
            reduced.assemble_density(
                wall_density=reduced_wall,
                void_density=reduced_void,
                wall_background_density=2.0,
                void_background_density=1.0,
                wall_physical_volume=0.5,
                void_physical_volume=0.5,
                h1_partition=reduced.scientific_state.operator.morphology,
            )
        except Phase1FADimensionalContractError:
            rejected = True
        reduced_rejections[f"d{len(reduced_shape)}"] = rejected

    convergence: list[dict[str, float | int]] = []
    for resolution in (4, 6, 8):
        refined = make_realization((4, resolution, resolution))
        exact, _, continuum_source = fields((4, resolution, resolution))
        reconstructed = refined.reconstruct_density(
            delta_cgi=supported(refined, continuum_source, "wall"),
            regional_geometry=domain(refined, "wall"),
            boundary_policy=boundary("wall"),
            zero_mode_closure=zero_mode("wall"),
            provenance="CONTINUUM_REFINEMENT_STUDY",
        )
        refined_mask = reconstructed.domain.mask
        error = float(
            np.sqrt(np.mean((reconstructed.delta_m[refined_mask] - exact.reshape(-1)[refined_mask]) ** 2))
        )
        convergence.append({"resolution": resolution, "l2_error": error})
    for index in range(1, len(convergence)):
        coarse = convergence[index - 1]
        fine = convergence[index]
        coarse_h = 1.0 / float(coarse["resolution"])
        fine_h = 1.0 / float(fine["resolution"])
        fine["observed_rate"] = float(
            np.log(float(coarse["l2_error"]) / float(fine["l2_error"]))
            / np.log(coarse_h / fine_h)
        )

    mutation_rejected = False
    closure_for_tamper = ExternalBoostDivergenceClosure(
        divergence=boost_source,
        source_frame="VOLUME_AVERAGE_DUST_FRAME",
        destination_frame="WALL_FRAME_THEORETICAL_REFERENCE",
        time_coordinate="t_D",
        spatial_metric_identity="wall-validation",
        units="INVERSE_COMMON_TIME",
        domain="wall",
        normalization_closure_id=zero_mode("wall").provenance,
        provenance="STATE_INTEGRITY_ADVERSARIAL",
        classification=EXTERNAL_CLOSURE,
    )
    object.__setattr__(closure_for_tamper, "provenance", "MUTATED")
    try:
        runtime.reconstruct_boost(
            regional_or_wall_geometry=domain(runtime, "wall"),
            boost_closure=closure_for_tamper,
            boundary_policy=boundary("wall"),
            zero_mode_closure=zero_mode("wall"),
        )
    except Phase1FAContractError:
        mutation_rejected = True

    return {
        "realization_id": "H1-1F-A-BROKEN-DENSITY-SPECTRAL-LONGITUDINAL-BOOST-V1",
        "classification": "SYNTHETIC_VALIDATION_ONLY",
        "density_inversion": {
            "wall_max_error": float(np.max(np.abs(wall.delta_m[wall_mask] - scalar.reshape(-1)[wall_mask]))),
            "void_max_error": float(np.max(np.abs(void.delta_m[void_mask] - 0.6 * scalar.reshape(-1)[void_mask]))),
            "wall_equation_residual": wall.diagnostics.equation_residual_max_abs,
            "void_equation_residual": void.diagnostics.equation_residual_max_abs,
            "wall_mean_residual": wall.diagnostics.solution_mean_residual,
            "void_mean_residual": void.diagnostics.solution_mean_residual,
            "zero_mode_shift_demonstration": zero_mode_difference,
        },
        "carrier_density": {
            "b_wall": carrier.b_wall,
            "b_void": carrier.b_void,
            "wall_offset_formula_error": float(np.max(np.abs(carrier.delta_m_carrier[wall_mask] - expected_wall_contrast))),
            "void_offset_formula_error": float(np.max(np.abs(carrier.delta_m_carrier[void_mask] - expected_void_contrast))),
            "global_mean_residual": carrier.diagnostics.global_mean_residual,
            "maximum_interface_density_jump": carrier.diagnostics.maximum_interface_density_jump,
            "wall_intertwining_residual": carrier.diagnostics.wall_intertwining_residual,
            "void_intertwining_residual": carrier.diagnostics.void_intertwining_residual,
            "physical_volumes": list(volumes),
        },
        "dimensional_contract": {
            "d1_physical_carrier_rejected": reduced_rejections["d1"],
            "d2_physical_carrier_rejected": reduced_rejections["d2"],
            "d3_physical_carrier_accepted": True,
        },
        "expansion": {
            "max_error": float(np.max(np.abs(expansion.delta_theta[wall_mask] - expansion_exact.reshape(-1)[wall_mask]))),
            "equation_residual": expansion.diagnostics.equation_residual_max_abs,
            "classification": expansion.scientific_classification,
        },
        "spectral": {
            "regional_eigenvalues": regional_spectrum.generalized_eigenvalues.tolist(),
            "carrier_eigenvalues": carrier_spectrum.generalized_eigenvalues.tolist(),
            "regional_max_eigenpair_residual": float(np.max(regional_spectrum.eigenpair_residuals)),
            "carrier_max_eigenpair_residual": float(np.max(carrier_spectrum.eigenpair_residuals)),
            "ordinary_stiffness_first": operator.ordinary_euclidean_constrained_stiffness_eigenvalue,
            "generalized_mass_weighted_first": float(carrier_spectrum.generalized_eigenvalues[0]),
            "kernel_max_off_diagonal": float(np.max(np.abs(off_diagonal))),
            "mode_diagonal_assumed": kernel.mode_diagonal_assumed,
        },
        "boost": {
            "residual": boost.boost_residual_max_abs,
            "incompatible_source_rejected": incompatible_boost_rejected,
            "transverse_status": boost.transverse_sector_status,
        },
        "dressed": {
            "destination_mean_residual": dressed.destination_mean_residual,
            "direct_contrast_pullback_difference": float(np.max(np.abs(dressed.delta_m_dressed - direct_delta))),
            "classification": dressed.map_classification,
        },
        "convergence": convergence,
        "state_integrity": {"post_construction_mutation_rejected": mutation_rejected},
        "observational_interpretation": "NOT_GRANTED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT_DEFAULT)
    args = parser.parse_args()
    result = validate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
