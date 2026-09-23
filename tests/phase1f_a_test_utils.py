"""Explicit validation fixtures for Phase 1F-A tests (no scientific defaults)."""

from __future__ import annotations

import numpy as np

from timescape_fsigma8.phase1f_a import (
    EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE,
    NO_FLUX_REGIONAL_INTERFACE_PERIODIC_CARRIER,
    REGIONAL_METRIC_MEAN_ZERO,
    REGIONAL_SOURCE_MEAN_ZERO,
    SINGLE_REGIONAL_CONSTANT_REMOVED,
    BoundaryKernelPolicy,
    Phase1FANumerics,
    Phase1FARealization,
    Phase1FAScientificState,
    RegionalDomainSpec,
    RegionalZeroModeClosure,
)
from timescape_fsigma8.transfer import (
    CARRIER_PHYSICAL_STATUS,
    DERIVED_FROM_NORMALIZED_METRIC,
    FIXED_REFERENCE_BRANCH,
    MORPHOLOGY_NORM_TARGET_METRIC_L2,
    ContinuumCarrierSpec,
    ContinuumEllipticClosureConfig,
    ContinuumH1Operator,
    FixedReferenceBranchSpec,
    H1Configuration,
    H1KinematicGatePolicy,
    RegionalMetricNormalization,
    flat_regional_geometry,
    layered_morphology,
)


def downstream_configuration() -> H1Configuration:
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
        downstream_configuration=downstream_configuration(),
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


def normalization(*, identity: str, volume: float) -> RegionalMetricNormalization:
    return RegionalMetricNormalization(
        normalization_id=identity,
        scale_factor_reference_epoch="PHASE1F_A_VALIDATION_EPOCH",
        scale_factor_reference_value=1.0,
        metric_scale_convention="UNIT_REFERENCE_COMOVING_METRIC",
        reference_comoving_volume=volume,
        volume_provenance=DERIVED_FROM_NORMALIZED_METRIC,
        consistency_tolerance=2e-12,
    )


def make_operator(shape: tuple[int, ...] = (4, 4, 4)) -> ContinuumH1Operator:
    dimension = len(shape)
    weights = np.full(shape, 1.0 / np.prod(shape), dtype=np.float64)
    morphology = layered_morphology(
        morphology_id=f"phase1f-a-layered-{'x'.join(map(str, shape))}",
        grid_shape=shape,
        axis=0,
        wall_cell_count=shape[0] // 2,
        wall_pullback_id="Phi_w_phase1f_a_validation",
        void_pullback_id="Phi_v_phase1f_a_validation",
    )
    wall_volume = float(np.sum(weights * morphology.wall_domain))
    void_volume = float(np.sum(weights * morphology.void_domain))
    target = flat_regional_geometry(
        region_id="target",
        grid_shape=shape,
        pullback_provenance="Phi_D_phase1f_a_validation",
        normalization=normalization(identity="target-normalization", volume=1.0),
        metadata={"frame": "TARGET_COMOVING_REFERENCE_ONLY"},
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
        target_scalarization_id="L_D_PHASE1F_A_VALIDATION",
    )
    wall = flat_regional_geometry(
        region_id="wall",
        grid_shape=shape,
        pullback_provenance=morphology.wall_pullback_id,
        normalization=normalization(identity="wall-normalization", volume=wall_volume),
        metadata={"frame": "WALL_COMOVING_REFERENCE"},
    )
    void = flat_regional_geometry(
        region_id="void",
        grid_shape=shape,
        pullback_provenance=morphology.void_pullback_id,
        normalization=normalization(identity="void-normalization", volume=void_volume),
        metadata={"frame": "VOID_COMOVING_REFERENCE"},
    )
    branch = FixedReferenceBranchSpec(
        branch_id=FIXED_REFERENCE_BRANCH,
        fixed_reference_partition=True,
        fixed_interface=True,
        fixed_comoving_pullback_geometries=True,
        fixed_target_scalarization=True,
        homogeneous_background_clock_map=True,
        spatial_clock_perturbation=False,
    )
    return ContinuumH1Operator(
        carrier=carrier,
        morphology=morphology,
        wall_geometry=wall,
        void_geometry=void,
        branch=branch,
        configuration=continuum_configuration(),
        continuum_coercivity_bound=0.1,
    )


def make_realization(shape: tuple[int, ...] = (4, 4, 4)) -> Phase1FARealization:
    operator = make_operator(shape)
    state = Phase1FAScientificState(
        operator=operator,
        morphology_provenance="EXPLICIT_PHASE1F_A_VALIDATION_MORPHOLOGY",
        normalization_provenance="EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE",
        scientific_classification="CONDITIONAL_THEORETICAL_FORWARD_REALIZATION",
    )
    return Phase1FARealization(scientific_state=state, numerics=numerics())


def domain(realization: Phase1FARealization, region: str) -> RegionalDomainSpec:
    return RegionalDomainSpec(scientific_state=realization.scientific_state, region=region)


def boundary(region: str) -> BoundaryKernelPolicy:
    return BoundaryKernelPolicy(
        domain=region,
        boundary_condition_kind=NO_FLUX_REGIONAL_INTERFACE_PERIODIC_CARRIER,
        nullspace_handling=SINGLE_REGIONAL_CONSTANT_REMOVED,
        compatibility_condition=REGIONAL_SOURCE_MEAN_ZERO,
        provenance="EXPLICIT_PHASE1F_A_REGIONAL_NEUMANN_POLICY",
    )


def zero_mode(region: str, scale_factor: float = 1.0) -> RegionalZeroModeClosure:
    return RegionalZeroModeClosure(
        mean_condition=REGIONAL_METRIC_MEAN_ZERO,
        spatial_measure_identity=f"a_{region}^3 dmu_gamma_{region}",
        scale_factor=scale_factor,
        provenance=f"{region}-mean-zero-closure-v1",
        classification=EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE,
        frame=f"{region.upper()}_COMOVING_DUST_FRAME",
        domain=region,
    )


def manufactured_scalar(shape: tuple[int, ...]) -> np.ndarray:
    coordinates = np.indices(shape, dtype=np.float64)
    if len(shape) == 1:
        return np.sin(2.0 * np.pi * coordinates[0] / shape[0])
    first = np.sin(2.0 * np.pi * coordinates[-1] / shape[-1])
    second = 0.25 * np.cos(2.0 * np.pi * coordinates[-2] / shape[-2])
    return first + second


def manufactured_laplacian(shape: tuple[int, ...]) -> np.ndarray:
    coordinates = np.indices(shape, dtype=np.float64)
    if len(shape) == 1:
        eigenvalue = -4.0 * np.sin(np.pi / shape[0]) ** 2 / (1.0 / shape[0]) ** 2
        return eigenvalue * np.sin(2.0 * np.pi * coordinates[0] / shape[0])
    last_eigenvalue = -4.0 * np.sin(np.pi / shape[-1]) ** 2 / (1.0 / shape[-1]) ** 2
    prior_eigenvalue = -4.0 * np.sin(np.pi / shape[-2]) ** 2 / (1.0 / shape[-2]) ** 2
    return (
        last_eigenvalue * np.sin(2.0 * np.pi * coordinates[-1] / shape[-1])
        + 0.25 * prior_eigenvalue * np.cos(2.0 * np.pi * coordinates[-2] / shape[-2])
    )


def regional_full(values: np.ndarray, realization: Phase1FARealization, region: str) -> np.ndarray:
    mask = (
        realization.scientific_state.operator.morphology.wall_domain
        if region == "wall"
        else realization.scientific_state.operator.morphology.void_domain
    )
    return np.where(mask, values, 0.0).reshape(-1)


def density_pair(realization: Phase1FARealization):
    shape = realization.scientific_state.operator.carrier.grid_shape
    field = 0.1 * manufactured_scalar(shape)
    source = 0.1 * manufactured_laplacian(shape)
    wall = realization.reconstruct_density(
        delta_cgi=regional_full(source, realization, "wall"),
        regional_geometry=domain(realization, "wall"),
        boundary_policy=boundary("wall"),
        zero_mode_closure=zero_mode("wall"),
        provenance="MANUFACTURED_WALL_DENSITY_INVERSION",
    )
    void = realization.reconstruct_density(
        delta_cgi=regional_full(0.6 * source, realization, "void"),
        regional_geometry=domain(realization, "void"),
        boundary_policy=boundary("void"),
        zero_mode_closure=zero_mode("void"),
        provenance="MANUFACTURED_VOID_DENSITY_INVERSION",
    )
    return wall, void, field


def carrier_density(realization: Phase1FARealization):
    wall, void, _ = density_pair(realization)
    volumes = realization.scientific_state.operator.physical_regional_volumes(a_w=1.0, a_v=1.0)
    return realization.assemble_density(
        wall_density=wall,
        void_density=void,
        wall_background_density=2.0,
        void_background_density=1.0,
        wall_physical_volume=volumes[0],
        void_physical_volume=volumes[1],
        h1_partition=realization.scientific_state.operator.morphology,
    )
