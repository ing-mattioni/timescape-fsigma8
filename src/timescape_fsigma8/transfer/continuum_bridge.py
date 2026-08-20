"""Continuum-geometric bridge into the frozen Phase 1E-F realization.

This module derives the formerly external Phase 1E-F effective-sector fields
from an explicit Phase 1E-G morphology and comoving elliptic transfer.  It
does not duplicate or alter the Phase 1E-F constitutive equations.  Regional
CGI dynamics and curvature retain the Galoppo--Mourier references documented
in :mod:`timescape_fsigma8.transfer.h1_realization` (Eqs. (2.13),
(2.20)--(2.23), arXiv:2511.17160v2).  New carrier bridge equations are the
human-approved Phase 1E-G model extension, sections 17--24; no paper equation
number exists for those closure choices.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np
from numpy.typing import ArrayLike

from timescape_fsigma8.transfer.continuum_backend import (
    ContinuumH1Operator,
    ContinuumPhase1EBackendAdapter,
    ContinuumTransfer,
    ContinuumTransferJetResponse,
    MetricNormalizationDiagnostics,
    target_metric_weighted_l2_difference,
)
from timescape_fsigma8.transfer.continuum_geometry import (
    FRAMEWORK_STATUS_1E_G,
    IMPLEMENTATION_STATUS_1E_G,
    PHYSICAL_VOLUME_SEMANTICS,
    REALIZATION_ID_1E_G,
    ROLE_1E_G,
    SCIENTIFIC_STATUS_1E_G,
    ContinuumContractError,
    ContinuumEllipticClosureConfig,
    ContinuumStateIntegrityError,
    FixedReferenceBranchSpec,
)
from timescape_fsigma8.transfer.h1_realization import (
    EffectiveSectorContract,
    H1Background,
    H1DegeneracyError,
    H1RealizationResult,
    RegionalBulkState,
    RegionalEvolution,
    evaluate_h1_realization,
    regional_evolution,
)
from timescape_fsigma8.transfer.matrix_backend import (
    DenseCarrierOperator,
    MatrixJet,
    ScalarJet,
    VectorJet,
)


def _scalar_multiply(first: ScalarJet, second: ScalarJet) -> ScalarJet:
    """Analytic product jet used by the authorised common-time chain rule."""
    return ScalarJet(
        first.value * second.value,
        first.first * second.value + first.value * second.first,
        first.second * second.value
        + 2.0 * first.first * second.first
        + first.value * second.second,
    )


def _vector_add(*fields: VectorJet) -> VectorJet:
    if not fields:
        raise ContinuumContractError("at least one carrier field is required")
    zeros = np.zeros_like(fields[0].value)
    return VectorJet(
        sum((field.value for field in fields), zeros.copy()),
        sum((field.first for field in fields), zeros.copy()),
        sum((field.second for field in fields), zeros.copy()),
    )


def _vector_scale(scalar: ScalarJet, field: VectorJet) -> VectorJet:
    return VectorJet(
        scalar.value * field.value,
        scalar.first * field.value + scalar.value * field.first,
        scalar.second * field.value
        + 2.0 * scalar.first * field.first
        + scalar.value * field.second,
    )


def _vector_subtract(first: VectorJet, second: VectorJet) -> VectorJet:
    minus_one = ScalarJet(-1.0, 0.0, 0.0)
    return _vector_add(first, _vector_scale(minus_one, second))


@dataclass(frozen=True)
class ContinuumBridgeFields:
    """Continuum-derived fields supplied to the Phase 1E-F contract."""

    regional_wall: RegionalEvolution
    regional_void: RegionalEvolution
    density_wall: ContinuumTransferJetResponse
    density_void: ContinuumTransferJetResponse
    expansion_wall: ContinuumTransferJetResponse
    expansion_void: ContinuumTransferJetResponse
    curvature_wall: ContinuumTransferJetResponse
    curvature_void: ContinuumTransferJetResponse
    C_R_Gamma: VectorJet
    E_DeltaTheta_Gamma: VectorJet
    E_DeltaXi_0_Gamma: VectorJet
    J_f_Gamma: VectorJet


@dataclass(frozen=True)
class ContinuumH1RealizationResult:
    """Phase 1E-G diagnostics plus the unchanged downstream 1E-F result."""

    realization_id: str
    role: str
    framework_status: str
    scientific_status: str
    implementation_status: str
    physical_volume_semantics: str
    continuum_geometry: Mapping[str, object]
    morphology_id: str
    regional_metric_metadata: Mapping[str, Mapping[str, str]]
    target_metric_metadata: Mapping[str, str]
    ellipticity_lower_bound: float
    ellipticity_upper_bound: float
    continuum_coercivity_bound_or_assumption: float
    ordinary_euclidean_constrained_stiffness_eigenvalue: float
    generalized_mass_weighted_laplacian_eigenvalue: float
    regional_metric_normalization: Mapping[str, MetricNormalizationDiagnostics]
    target_metric_time_contract: str
    global_kernel_dimension: int
    source_mean_before_projection: float
    source_mean_after_projection: float
    solution_global_mean: float
    transmission_value_jump: float
    transmission_flux_jump: float
    equal_geometry_identity_residual: float | None
    f_v_geom: float
    f_v_background: float
    volume_fraction_consistency_residual: float
    volume_fraction_consistency_classification: str
    transferred_wall_density: np.ndarray
    transferred_void_density: np.ndarray
    E_DeltaTheta_Gamma: VectorJet
    E_DeltaXi_0_Gamma: VectorJet
    C_R_Gamma: VectorJet
    J_f_Gamma: VectorJet
    morphology_sensitivity_diagnostics: Mapping[str, float]
    morphology_norm_definition: str
    morphology_normalization_reference_scale: float
    morphology_normalization_floor: float
    target_measure_weights: np.ndarray
    discretization_resolution: tuple[int, ...]
    discretization_convergence_metrics: Mapping[str, float]
    bridge_fields: ContinuumBridgeFields
    downstream_phase1e_f: H1RealizationResult


class EffectiveSectorContinuumBridge:
    """Derive continuum H1 inputs and invoke the frozen Phase 1E-F evaluator."""

    def __setattr__(self, name: str, value: object) -> None:
        if self.__dict__.get("_assembly_sealed", False):
            raise ContinuumStateIntegrityError(
                "continuum bridge is bound immutably to validated assembly state"
            )
        object.__setattr__(self, name, value)

    def __init__(
        self,
        *,
        operator: ContinuumH1Operator,
        branch: FixedReferenceBranchSpec,
        configuration: ContinuumEllipticClosureConfig,
    ) -> None:
        operator._validate_assembled_state_integrity()
        branch.validate_selected_branch()
        if operator.branch != branch:
            raise ContinuumContractError("operator/bridge branch metadata differ")
        if operator.configuration != configuration:
            raise ContinuumContractError(
                "operator/bridge continuum configurations differ"
            )
        self.operator = operator
        self.transfer = ContinuumTransfer(operator)
        self.branch = branch
        self.configuration = configuration
        self._operator_identity = id(operator)
        self._transfer_identity = id(self.transfer)
        self._branch_identity = id(branch)
        self._configuration_identity = id(configuration)
        self._assembly_sealed = True

    def _validate_assembled_state_integrity(self) -> None:
        bindings = (
            id(self.operator) == self._operator_identity,
            id(self.transfer) == self._transfer_identity,
            id(self.branch) == self._branch_identity,
            id(self.configuration) == self._configuration_identity,
            self.operator.branch is self.branch,
            self.operator.configuration is self.configuration,
        )
        if not all(bindings):
            raise ContinuumStateIntegrityError(
                "continuum bridge bindings differ from validated assembly"
            )
        self.operator._validate_assembled_state_integrity()
        self.transfer._validate_assembled_state_integrity()

    @staticmethod
    def _regional_states(
        regional_bulk: RegionalBulkState, background: H1Background
    ) -> tuple[RegionalEvolution, RegionalEvolution]:
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
        return wall, void

    def _validate_common_time_branch(self, background: H1Background) -> None:
        """Validate ``Xi_r=alpha_r Theta_r`` for the selected branch.

        This follows from ``V_r=V_ri a_r^3`` and homogeneous
        ``alpha_r=d tau_r/dt_D`` in Phase 1E-G section 18.  It is explicitly
        not claimed as a universal Timescape identity and has no paper
        equation number.
        """
        self._validate_assembled_state_integrity()
        tolerance = (
            self.configuration.downstream_configuration.background_identity_tolerance
        )
        for region, supplied, derived in (
            (
                "wall",
                background.Xi_w,
                _scalar_multiply(background.alpha_w, background.Theta_w),
            ),
            (
                "void",
                background.Xi_v,
                _scalar_multiply(background.alpha_v, background.Theta_v),
            ),
        ):
            error = max(
                abs(supplied.value - derived.value),
                abs(supplied.first - derived.first),
                abs(supplied.second - derived.second),
            )
            if error > tolerance:
                raise ContinuumContractError(
                    f"Xi_{region}=alpha_{region} Theta_{region} branch identity failed"
                )

    def derive_fields(
        self,
        *,
        regional_bulk: RegionalBulkState,
        background: H1Background,
    ) -> ContinuumBridgeFields:
        self._validate_assembled_state_integrity()
        self.branch.validate_selected_branch()
        self.operator.require_physical_volume_dimension(
            context=(
                "continuum-to-Phase-1E-F bridge fields requiring physical "
                "regional volume fractions"
            )
        )
        self._validate_common_time_branch(background)
        wall, void = self._regional_states(regional_bulk, background)
        density_wall = self.transfer.transfer_regional_amplitude(
            wall.delta, region="wall", provenance="density"
        )
        density_void = self.transfer.transfer_regional_amplitude(
            void.delta, region="void", provenance="density"
        )
        expansion_wall = self.transfer.transfer_regional_amplitude(
            wall.Z, region="wall", provenance="expansion"
        )
        expansion_void = self.transfer.transfer_regional_amplitude(
            void.Z, region="void", provenance="expansion"
        )
        curvature_wall = self.transfer.transfer_regional_amplitude(
            wall.curvature, region="wall", provenance="derived-curvature"
        )
        curvature_void = self.transfer.transfer_regional_amplitude(
            void.curvature, region="void", provenance="derived-curvature"
        )
        f_v = background.f_v
        f_w = ScalarJet(1.0 - f_v.value, -f_v.first, -f_v.second)
        # Phase 1E-G section 17; regional curvature itself is derived from
        # the first variation of GM Eq. (2.13), arXiv:2511.17160v2.
        C_R = _vector_add(
            _vector_scale(f_w, curvature_wall.transferred_field),
            _vector_scale(f_v, curvature_void.transferred_field),
        )
        # Phase 1E-G section 17 explicit bridge equation (no paper equation).
        E_delta_theta = _vector_subtract(
            expansion_void.transferred_field,
            expansion_wall.transferred_field,
        )
        # Phase 1E-G section 18, derived only on the homogeneous-clock branch.
        E_delta_xi0 = _vector_subtract(
            _vector_scale(background.alpha_v, expansion_void.transferred_field),
            _vector_scale(background.alpha_w, expansion_wall.transferred_field),
        )
        # Phase 1E-G section 19: derived zero from fixed reference geometry.
        J_f = VectorJet(
            np.zeros(self.operator.size),
            np.zeros(self.operator.size),
            np.zeros(self.operator.size),
        )
        result = ContinuumBridgeFields(
            regional_wall=wall,
            regional_void=void,
            density_wall=density_wall,
            density_void=density_void,
            expansion_wall=expansion_wall,
            expansion_void=expansion_void,
            curvature_wall=curvature_wall,
            curvature_void=curvature_void,
            C_R_Gamma=C_R,
            E_DeltaTheta_Gamma=E_delta_theta,
            E_DeltaXi_0_Gamma=E_delta_xi0,
            J_f_Gamma=J_f,
        )
        self._validate_assembled_state_integrity()
        return result

    def _effective_contract(
        self, fields: ContinuumBridgeFields
    ) -> EffectiveSectorContract:
        self._validate_assembled_state_integrity()
        identity = np.eye(self.operator.size, dtype=np.float64)
        zero = np.zeros_like(identity)
        identity_operator = DenseCarrierOperator(MatrixJet(identity, zero, zero))
        return EffectiveSectorContract(
            delta_theta_operator=identity_operator,
            delta_theta_inputs=fields.E_DeltaTheta_Gamma,
            delta_xi0_operator=identity_operator,
            delta_xi0_inputs=fields.E_DeltaXi_0_Gamma,
            J_f_Gamma=fields.J_f_Gamma,
            partition_time_independent=True,
        )

    def equal_geometry_identity_residual(self, source: ArrayLike) -> float:
        """Exercise the complete ``T[s]=s`` equal-geometry oracle.

        Phase 1E-G section 15.  This transfer identity is distinct from the
        Phase 1E-F full equal-region constitutive point, where ``A_P=0`` and
        the downstream realization remains fail-closed.
        """
        self._validate_assembled_state_integrity()
        wall = self.operator.wall_geometry
        void = self.operator.void_geometry
        target = self.operator.carrier.target_geometry
        for candidate in (void, target):
            if not np.allclose(
                wall.metric_inverse,
                candidate.metric_inverse,
                rtol=0.0,
                atol=self.configuration.symmetry_tolerance,
            ) or not np.allclose(
                wall.metric_volume_ratio,
                candidate.metric_volume_ratio,
                rtol=0.0,
                atol=self.configuration.symmetry_tolerance,
            ):
                raise ContinuumContractError(
                    "equal-geometry identity requested for unequal geometries"
                )
        source_array = np.asarray(source, dtype=np.float64).reshape(-1)
        raw_load = self.operator.source_load(source_array, region="global")
        source_mean = float(np.sum(raw_load) / np.sum(self.operator.reference_weights))
        if abs(source_mean) > self.configuration.source_compatibility_tolerance:
            raise ContinuumContractError(
                "equal-geometry oracle source must already be admissible"
            )
        response = self.transfer.transfer_source(
            source_array, region="global", provenance="equal-geometry-oracle"
        )
        residual = float(
            np.max(np.abs(response.transferred_field - source_array))
        )
        if residual > self.configuration.equal_geometry_identity_tolerance:
            raise ContinuumContractError("equal-geometry transfer identity failed")
        self._validate_assembled_state_integrity()
        return residual

    def evaluate(
        self,
        *,
        regional_bulk: RegionalBulkState,
        background: H1Background,
        a_w: float,
        a_v: float,
        equal_geometry_probe: ArrayLike | None,
        volume_fraction_consistency_classification: str,
        morphology_sensitivity_diagnostics: Mapping[str, float],
        discretization_convergence_metrics: Mapping[str, float],
    ) -> ContinuumH1RealizationResult:
        self._validate_assembled_state_integrity()
        if (
            not isinstance(volume_fraction_consistency_classification, str)
            or not volume_fraction_consistency_classification.strip()
        ):
            raise ContinuumContractError(
                "volume-fraction consistency classification is required"
            )
        if not 0.0 < background.f_v.value < 1.0:
            raise H1DegeneracyError(
                'SINGLE_REGION_ONTOLOGY_REDUCTION_REQUIRED: '
                'two-region branch requires 0 < f_v < 1'
            )
        fields = self.derive_fields(
            regional_bulk=regional_bulk, background=background
        )
        f_v_geom = self.operator.geometric_void_fraction(a_w=a_w, a_v=a_v)
        f_v_background = background.f_v.value
        volume_residual = f_v_geom - f_v_background
        if abs(volume_residual) > self.configuration.volume_fraction_tolerance:
            raise ContinuumContractError(
                "geometry/background volume-fraction consistency gate failed"
            )
        equal_residual = (
            None
            if equal_geometry_probe is None
            else self.equal_geometry_identity_residual(equal_geometry_probe)
        )
        adapter = ContinuumPhase1EBackendAdapter(self.transfer)
        downstream = evaluate_h1_realization(
            regional_bulk=regional_bulk,
            background=background,
            backend=adapter,  # type: ignore[arg-type] - explicit contract adapter.
            effective_sector=self._effective_contract(fields),
            configuration=self.configuration.downstream_configuration,
        )
        responses = (
            fields.density_wall,
            fields.density_void,
            fields.expansion_wall,
            fields.expansion_void,
            fields.curvature_wall,
            fields.curvature_void,
        )
        scalar_responses = tuple(
            response.components[0] for response in responses
        )
        source_before = max(
            abs(response.source_projection.mean_before_projection)
            for response in scalar_responses
        )
        source_after = max(
            abs(response.source_projection.mean_after_projection)
            for response in scalar_responses
        )
        solution_mean = max(
            abs(response.solution_global_mean) for response in scalar_responses
        )
        value_jump = max(
            response.interface.maximum_value_jump for response in scalar_responses
        )
        flux_jump = max(
            response.interface.maximum_flux_jump for response in scalar_responses
        )
        result = ContinuumH1RealizationResult(
            realization_id=REALIZATION_ID_1E_G,
            role=ROLE_1E_G,
            framework_status=FRAMEWORK_STATUS_1E_G,
            scientific_status=SCIENTIFIC_STATUS_1E_G,
            implementation_status=IMPLEMENTATION_STATUS_1E_G,
            physical_volume_semantics=PHYSICAL_VOLUME_SEMANTICS,
            continuum_geometry={
                "topology": self.operator.carrier.topology,
                "physical_status": self.operator.carrier.physical_status,
                "dimension": self.operator.carrier.dimension,
                "weak_form": "REGIONAL_COMOVING_LAPLACE_BELTRAMI",
                "discretization": self.operator.scientific_role,
            },
            morphology_id=self.operator.morphology.morphology_id,
            regional_metric_metadata={
                "wall": dict(self.operator.wall_geometry.metadata),
                "void": dict(self.operator.void_geometry.metadata),
            },
            target_metric_metadata=dict(
                self.operator.carrier.target_geometry.metadata
            ),
            ellipticity_lower_bound=self.operator.ellipticity_lower_bound,
            ellipticity_upper_bound=self.operator.ellipticity_upper_bound,
            continuum_coercivity_bound_or_assumption=(
                self.operator.continuum_coercivity_assumption
            ),
            ordinary_euclidean_constrained_stiffness_eigenvalue=(
                self.operator.ordinary_euclidean_constrained_stiffness_eigenvalue
            ),
            generalized_mass_weighted_laplacian_eigenvalue=(
                self.operator.generalized_mass_weighted_laplacian_eigenvalue
            ),
            regional_metric_normalization=dict(
                self.operator.metric_normalization_diagnostics
            ),
            target_metric_time_contract=(
                "FIXED_GAMMA_D_WITH_L_D_DOT_AND_L_D_DDOT_ZERO"
            ),
            global_kernel_dimension=self.operator.global_kernel_dimension,
            source_mean_before_projection=source_before,
            source_mean_after_projection=source_after,
            solution_global_mean=solution_mean,
            transmission_value_jump=value_jump,
            transmission_flux_jump=flux_jump,
            equal_geometry_identity_residual=equal_residual,
            f_v_geom=f_v_geom,
            f_v_background=f_v_background,
            volume_fraction_consistency_residual=volume_residual,
            volume_fraction_consistency_classification=(
                volume_fraction_consistency_classification
            ),
            transferred_wall_density=fields.density_wall.transferred_field.value,
            transferred_void_density=fields.density_void.transferred_field.value,
            E_DeltaTheta_Gamma=fields.E_DeltaTheta_Gamma,
            E_DeltaXi_0_Gamma=fields.E_DeltaXi_0_Gamma,
            C_R_Gamma=fields.C_R_Gamma,
            J_f_Gamma=fields.J_f_Gamma,
            morphology_sensitivity_diagnostics=dict(
                morphology_sensitivity_diagnostics
            ),
            morphology_norm_definition=(
                self.configuration.morphology_sensitivity_norm
            ),
            morphology_normalization_reference_scale=(
                self.configuration.morphology_sensitivity_reference_scale
            ),
            morphology_normalization_floor=(
                self.configuration.morphology_sensitivity_floor
            ),
            target_measure_weights=self.operator.target_measure_weights,
            discretization_resolution=self.operator.carrier.grid_shape,
            discretization_convergence_metrics=dict(
                discretization_convergence_metrics
            ),
            bridge_fields=fields,
            downstream_phase1e_f=downstream,
        )
        self._validate_assembled_state_integrity()
        return result


def compare_morphology_results(
    first: ContinuumH1RealizationResult,
    second: ContinuumH1RealizationResult,
) -> dict[str, float]:
    """Return target-metric L2 morphology sensitivity, never numerical error."""
    if first.morphology_norm_definition != second.morphology_norm_definition:
        raise ContinuumContractError("morphology norm definitions differ")
    if not np.allclose(
        first.target_measure_weights,
        second.target_measure_weights,
        rtol=0.0,
        atol=0.0,
    ):
        raise ContinuumContractError("target measures differ across morphologies")
    scale = first.morphology_normalization_reference_scale
    floor = first.morphology_normalization_floor
    if (
        scale != second.morphology_normalization_reference_scale
        or floor != second.morphology_normalization_floor
    ):
        raise ContinuumContractError("morphology normalization contracts differ")

    def difference(left: ArrayLike, right: ArrayLike) -> float:
        return target_metric_weighted_l2_difference(
            left,
            right,
            target_measure_weights=first.target_measure_weights,
            reference_scale=scale,
            normalization_floor=floor,
        )

    first_downstream = first.downstream_phase1e_f
    second_downstream = second.downstream_phase1e_f
    return {
        "transferred_wall_density": difference(
            first.transferred_wall_density,
            second.transferred_wall_density,
        ),
        "transferred_void_density": difference(
            first.transferred_void_density,
            second.transferred_void_density,
        ),
        "E_DeltaTheta_Gamma": difference(
            first.E_DeltaTheta_Gamma.value,
            second.E_DeltaTheta_Gamma.value,
        ),
        "C_R_Gamma": difference(
            first.C_R_Gamma.value,
            second.C_R_Gamma.value,
        ),
        "F_v": difference(
            first_downstream.F_v.value,
            second_downstream.F_v.value,
        ),
        "Delta_d": difference(
            first_downstream.Delta_d.value,
            second_downstream.Delta_d.value,
        ),
        "Delta_eff": difference(
            first_downstream.Delta_eff.value,
            second_downstream.Delta_eff.value,
        ),
    }
