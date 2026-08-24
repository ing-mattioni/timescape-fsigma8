"""Explicit physical-density-first carrier-to-dressed mapping for Phase 1F-A."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from timescape_fsigma8.phase1f_a.density import CarrierDensityResult
from timescape_fsigma8.phase1f_a.models import (
    CONDITIONAL,
    DressedSpacetimeMapClosure,
    FloatArray,
    Phase1FAContractError,
    Phase1FANumerics,
    readonly_float,
    seal_integrity,
    validate_integrity,
)


@dataclass(frozen=True, kw_only=True)
class DressedDensityResult:
    rho_dressed: FloatArray
    rho_bar_dressed: float
    delta_m_dressed: FloatArray
    destination_mean_residual: float
    source_frame: str
    destination_frame: str
    map_provenance: str
    map_classification: str
    scientific_classification: str
    closure: DressedSpacetimeMapClosure = field(repr=False, compare=False)
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for name in ("rho_dressed", "delta_m_dressed"):
            object.__setattr__(self, name, readonly_float(getattr(self, name), name))
        seal_integrity(self, self._live_state())

    def _live_state(self) -> object:
        return (
            self.rho_dressed,
            self.rho_bar_dressed,
            self.delta_m_dressed,
            self.destination_mean_residual,
            self.source_frame,
            self.destination_frame,
            self.map_provenance,
            self.map_classification,
            self.scientific_classification,
            id(self.closure),
        )

    def validate_integrity(self) -> None:
        self.closure.validate_integrity()
        validate_integrity(self, self._live_state())


def map_carrier_density_to_dressed(
    *,
    carrier_density: CarrierDensityResult,
    dressed_map_closure: DressedSpacetimeMapClosure,
    numerics: Phase1FANumerics,
) -> DressedDensityResult:
    """Map physical ``rho_C`` first, then recompute the dressed mean/contrast.

    The matter-density definition is the one underlying GM Eq. (2.2),
    arXiv:2511.17160v2.  The carrier-to-dressed pullback and destination
    measure are explicit Phase 1F-A section 14 external closure inputs, with
    no paper equation number and no Timescape-uniqueness claim.  Direct
    transfer of ``delta_m,C`` is intentionally absent.
    """
    if dressed_map_closure is None:
        raise Phase1FAContractError("an explicit dressed spacetime map closure is required")
    carrier_density.validate_integrity()
    carrier_density.scientific_state.require_physical_three_dimensions(
        context="physical dressed density"
    )
    dressed_map_closure.validate_integrity()
    if dressed_map_closure.source_frame != "H1_PHYSICAL_CARRIER_DENSITY_FRAME":
        raise Phase1FAContractError("dressed map source frame does not match carrier density")
    indices = dressed_map_closure.destination_source_indices
    if np.any(indices < 0) or np.any(indices >= carrier_density.rho_carrier.size):
        raise Phase1FAContractError("dressed inverse spatial map indexes outside carrier")
    rho_dressed = carrier_density.rho_carrier[indices]
    destination_measure = (
        dressed_map_closure.destination_reference_weights
        * dressed_map_closure.destination_metric_volume_ratio
        * dressed_map_closure.destination_measure_jacobian
    )
    total_measure = float(np.sum(destination_measure))
    if not np.isfinite(total_measure) or total_measure <= 0.0:
        raise Phase1FAContractError("dressed destination measure is degenerate")
    rho_bar = float(np.dot(destination_measure, rho_dressed) / total_measure)
    if not np.isfinite(rho_bar) or rho_bar <= 0.0:
        raise Phase1FAContractError("dressed mean density must be finite and positive")
    delta = rho_dressed / rho_bar - 1.0
    mean_residual = float(np.dot(destination_measure, delta) / total_measure)
    if abs(mean_residual) > numerics.dressed_mean_tolerance:
        raise Phase1FAContractError("dressed density contrast mean residual exceeds tolerance")
    return DressedDensityResult(
        rho_dressed=rho_dressed,
        rho_bar_dressed=rho_bar,
        delta_m_dressed=delta,
        destination_mean_residual=mean_residual,
        source_frame=dressed_map_closure.source_frame,
        destination_frame=dressed_map_closure.destination_frame,
        map_provenance=dressed_map_closure.provenance,
        map_classification=dressed_map_closure.scientific_classification,
        scientific_classification=CONDITIONAL,
        closure=dressed_map_closure,
    )
