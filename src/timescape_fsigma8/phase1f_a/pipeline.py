"""Thin fail-closed orchestrator for the Phase 1F-A forward realization."""

from __future__ import annotations

from dataclasses import dataclass, field

from numpy.typing import ArrayLike

from timescape_fsigma8.phase1f_a.boost import (
    BoostClosure,
    LongitudinalRelativeVelocityResult,
    reconstruct_longitudinal_relative_velocity,
)
from timescape_fsigma8.phase1f_a.density import (
    CarrierDensityResult,
    RegionalDensityReconstruction,
    assemble_carrier_density,
    reconstruct_regional_density,
)
from timescape_fsigma8.phase1f_a.dressed import (
    DressedDensityResult,
    map_carrier_density_to_dressed,
)
from timescape_fsigma8.phase1f_a.expansion import (
    RegionalExpansionReconstruction,
    reconstruct_regional_expansion,
)
from timescape_fsigma8.phase1f_a.models import (
    BoundaryKernelPolicy,
    DressedSpacetimeMapClosure,
    Phase1FANumerics,
    Phase1FAScientificState,
    RegionalDomainSpec,
    RegionalZeroModeClosure,
    seal_integrity,
    validate_integrity,
)


@dataclass(frozen=True, kw_only=True)
class Phase1FARealization:
    """Bind explicit numerics to one sealed scientific state.

    No morphology, normalization, boost, dressed map, spectral branch, or
    observational choice is selected here.  Every closure remains a required
    argument to the operation that consumes it.
    """

    scientific_state: Phase1FAScientificState
    numerics: Phase1FANumerics
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.scientific_state.validate_integrity()
        seal_integrity(self, self._live_state())

    def _live_state(self) -> object:
        return (id(self.scientific_state), self.numerics)

    def validate_integrity(self) -> None:
        self.scientific_state.validate_integrity()
        validate_integrity(self, self._live_state())

    def reconstruct_density(
        self,
        *,
        delta_cgi: ArrayLike,
        regional_geometry: RegionalDomainSpec,
        boundary_policy: BoundaryKernelPolicy,
        zero_mode_closure: RegionalZeroModeClosure,
        provenance: str,
    ) -> RegionalDensityReconstruction:
        self.validate_integrity()
        return reconstruct_regional_density(
            delta_cgi=delta_cgi,
            regional_geometry=regional_geometry,
            boundary_policy=boundary_policy,
            zero_mode_closure=zero_mode_closure,
            numerics=self.numerics,
            provenance=provenance,
        )

    def assemble_density(
        self,
        *,
        wall_density: RegionalDensityReconstruction,
        void_density: RegionalDensityReconstruction,
        wall_background_density: float,
        void_background_density: float,
        wall_physical_volume: float,
        void_physical_volume: float,
        h1_partition,
    ) -> CarrierDensityResult:
        self.validate_integrity()
        return assemble_carrier_density(
            wall_density=wall_density,
            void_density=void_density,
            wall_background_density=wall_background_density,
            void_background_density=void_background_density,
            wall_physical_volume=wall_physical_volume,
            void_physical_volume=void_physical_volume,
            h1_partition=h1_partition,
            scientific_state=self.scientific_state,
            numerics=self.numerics,
        )

    def reconstruct_expansion(
        self,
        *,
        z_cgi: ArrayLike,
        regional_geometry: RegionalDomainSpec,
        boundary_policy: BoundaryKernelPolicy,
        zero_mode_closure: RegionalZeroModeClosure,
        background_expansion_identity: str,
        provenance: str,
    ) -> RegionalExpansionReconstruction:
        self.validate_integrity()
        return reconstruct_regional_expansion(
            z_cgi=z_cgi,
            regional_geometry=regional_geometry,
            boundary_policy=boundary_policy,
            zero_mode_closure=zero_mode_closure,
            numerics=self.numerics,
            background_expansion_identity=background_expansion_identity,
            provenance=provenance,
        )

    def reconstruct_boost(
        self,
        *,
        regional_or_wall_geometry: RegionalDomainSpec,
        boost_closure: BoostClosure,
        boundary_policy: BoundaryKernelPolicy,
        zero_mode_closure: RegionalZeroModeClosure,
    ) -> LongitudinalRelativeVelocityResult:
        self.validate_integrity()
        return reconstruct_longitudinal_relative_velocity(
            regional_or_wall_geometry=regional_or_wall_geometry,
            boost_closure=boost_closure,
            boundary_policy=boundary_policy,
            zero_mode_closure=zero_mode_closure,
            numerics=self.numerics,
        )

    def map_dressed_density(
        self,
        *,
        carrier_density: CarrierDensityResult,
        dressed_map_closure: DressedSpacetimeMapClosure,
    ) -> DressedDensityResult:
        self.validate_integrity()
        return map_carrier_density_to_dressed(
            carrier_density=carrier_density,
            dressed_map_closure=dressed_map_closure,
            numerics=self.numerics,
        )
