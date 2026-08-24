"""Conditional regional dust-expansion scalar reconstruction for Phase 1F-A."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import ArrayLike

from timescape_fsigma8.phase1f_a.models import (
    DUST_EXPANSION_FIELD_RECONSTRUCTED_CONDITIONALLY,
    MATHEMATICAL_OPERATOR_FIXTURE_ONLY,
    BoundaryKernelPolicy,
    FloatArray,
    Phase1FAContractError,
    Phase1FANumerics,
    RegionalDomainSpec,
    RegionalZeroModeClosure,
    readonly_float,
    seal_integrity,
    validate_integrity,
)
from timescape_fsigma8.phase1f_a.operators import (
    RegionalEllipticDiagnostics,
    RegionalEllipticSystem,
    assemble_regional_elliptic_system,
    embed_regional_field,
    solve_regional_laplace_beltrami,
)


@dataclass(frozen=True, kw_only=True)
class RegionalExpansionReconstruction:
    """Reconstructed ``delta Theta_r``; explicitly not a velocity field."""

    delta_theta: FloatArray
    z_cgi: FloatArray
    regional_values: FloatArray
    regional_source: FloatArray
    regional_indices: np.ndarray
    domain: RegionalDomainSpec
    zero_mode_closure: RegionalZeroModeClosure
    boundary_policy: BoundaryKernelPolicy
    diagnostics: RegionalEllipticDiagnostics
    background_expansion_identity: str
    scientific_classification: str
    provenance: str
    _system: RegionalEllipticSystem = field(repr=False, compare=False)
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for name in ("delta_theta", "z_cgi", "regional_values", "regional_source"):
            object.__setattr__(self, name, readonly_float(getattr(self, name), name))
        indices = np.array(self.regional_indices, dtype=np.int64, copy=True)
        indices.setflags(write=False)
        object.__setattr__(self, "regional_indices", indices)
        seal_integrity(self, self._live_state())

    def _live_state(self) -> object:
        return (
            self.delta_theta,
            self.z_cgi,
            self.regional_values,
            self.regional_source,
            self.regional_indices,
            id(self.domain),
            self.zero_mode_closure,
            self.boundary_policy,
            self.diagnostics,
            self.background_expansion_identity,
            self.scientific_classification,
            self.provenance,
            id(self._system),
        )

    def validate_integrity(self) -> None:
        self.domain.validate_integrity()
        validate_integrity(self, self._live_state())


def reconstruct_regional_expansion(
    *,
    z_cgi: ArrayLike,
    regional_geometry: RegionalDomainSpec,
    boundary_policy: BoundaryKernelPolicy,
    zero_mode_closure: RegionalZeroModeClosure,
    numerics: Phase1FANumerics,
    background_expansion_identity: str,
    provenance: str,
) -> RegionalExpansionReconstruction:
    """Solve ``Delta_gamma_r deltaTheta_r=Z_r`` with explicit zero mean.

    ``Z`` is the Laplacian expansion-gradient CGI scalar from GM Eqs.
    (2.20)--(2.24), arXiv:2511.17160v2.  This function reconstructs only the
    regional dust expansion-scalar perturbation and never a wall, tracer,
    peculiar, line-of-sight, or observational velocity divergence.
    """
    regional_geometry.validate_integrity()
    if zero_mode_closure is None:
        raise Phase1FAContractError("regional expansion zero-mode closure is required")
    if not background_expansion_identity.strip() or not provenance.strip():
        raise Phase1FAContractError("expansion background identity and provenance are required")
    source_full = readonly_float(z_cgi, "z_cgi").reshape(-1)
    if source_full.shape != (regional_geometry.operator.size,):
        raise Phase1FAContractError("z_cgi must use the complete carrier grid")
    system = assemble_regional_elliptic_system(
        domain=regional_geometry,
        boundary_policy=boundary_policy,
        numerics=numerics,
    )
    source_regional = source_full[system.regional_indices]
    solution, diagnostics = solve_regional_laplace_beltrami(
        source=source_regional,
        system=system,
        zero_mode_closure=zero_mode_closure,
        numerics=numerics,
    )
    classification = (
        DUST_EXPANSION_FIELD_RECONSTRUCTED_CONDITIONALLY
        if regional_geometry.operator.carrier.dimension == 3
        else MATHEMATICAL_OPERATOR_FIXTURE_ONLY
    )
    return RegionalExpansionReconstruction(
        delta_theta=embed_regional_field(system=system, regional_field=solution),
        z_cgi=embed_regional_field(system=system, regional_field=source_regional),
        regional_values=solution,
        regional_source=source_regional,
        regional_indices=system.regional_indices,
        domain=regional_geometry,
        zero_mode_closure=zero_mode_closure,
        boundary_policy=boundary_policy,
        diagnostics=diagnostics,
        background_expansion_identity=background_expansion_identity,
        scientific_classification=classification,
        provenance=provenance,
        _system=system,
    )
