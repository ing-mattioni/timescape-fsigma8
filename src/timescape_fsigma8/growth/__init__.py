"""Phase 1D-B growth layer: signed relative growth and analytic rates.

Scientific scope and caveats (frozen by the Phase 1D-A audit,
reports/phase1d_a_growth_observable_audit.md):

* ``Delta_d`` is the CGI Laplacian density scalar of [GM] (2.19)-(2.20),
  **not** the ordinary local density contrast.
* Relative growth histories and logarithmic growth rates are invariant
  under the fixed solver-harmonic conversion
  ``delta_m = -Delta_d/k_code^2``; mapped ``delta_m`` values are
  solver-harmonic coefficients only (no observational/dressed comoving
  wavenumber is derived here).
* Growth rates are piecewise for trajectories with amplitude crossings:
  logarithmic rates are undefined at ``Delta_d`` roots and are reported
  per maximal validity interval, never joined across a pole.
* Both D3 branches (``printed_4_15``, ``derived_4_10``) remain unresolved;
  neither is canonical, preferred, physical, corrected, recommended,
  intended, or a default.
* No observational f-sigma-8, sigma_8, sigma_R, power spectrum, transfer
  function, RSD, likelihood, or fitting quantity is implemented anywhere
  in this package.
* The D2-corrupted upstream sound speed remains excluded from the
  scientific package (forensic scripts only).

Every scientific choice is a mandatory explicit argument; non-applicable
fields must be passed as explicit ``not_applicable`` values.
"""

from timescape_fsigma8.growth.crossings import (
    CrossingAnalysis,
    DenseDustSolution,
    DUST_COMPONENT,
    EXPANSION_COMPONENT,
    EndpointRoot,
    RefinedRoot,
    SignChangeBracket,
    ValidityInterval,
    analyse_crossings,
    build_dense_solution,
    build_validity_intervals,
    refine_root,
    scan_sign_changes,
)
from timescape_fsigma8.growth.histories import (
    DustModeHistory,
    GrowthProvenance,
    compute_history,
    extract_dust_mode,
    resolve_epoch_and_ics,
)
from timescape_fsigma8.growth.mapping import (
    HarmonicMetadata,
    HarmonicSignConvention,
    map_delta_m,
    map_delta_m_dln_a_derivative,
)
from timescape_fsigma8.growth.pipeline import (
    GrowthPipelineResult,
    MappedDensityContrast,
    ResolvedGrowthReference,
    relative_growth,
    resolve_reference,
    run_growth_pipeline,
)
from timescape_fsigma8.growth.rates import (
    GrowthRates,
    amplitude_near_zero_mask,
    dDelta_d_dln_aD,
    dDelta_d_dln_aobs,
    dressed_chain_factor,
    evaluate_rates,
    f_bare,
    f_dressed,
)
from timescape_fsigma8.growth.scenarios import (
    DenseSolveConfig,
    DensityContrastMapping,
    GrowthBackgroundPreset,
    GrowthCoordinate,
    GrowthD3Branch,
    GrowthNumericsConfig,
    GrowthReference,
    GrowthReferenceCoordinate,
    GrowthScenario,
    GrowthSystem,
    GrowthTiltForm,
    GrowthWavenumberConvention,
    LCDM_REFERENCE_H,
    PAPER_REFERENCE_TIME_UNIT,
    ResolvedBackground,
    RootRefineConfig,
    resolve_background,
)

__all__ = [
    "CrossingAnalysis",
    "DenseDustSolution",
    "DUST_COMPONENT",
    "EXPANSION_COMPONENT",
    "EndpointRoot",
    "RefinedRoot",
    "SignChangeBracket",
    "ValidityInterval",
    "analyse_crossings",
    "build_dense_solution",
    "build_validity_intervals",
    "refine_root",
    "scan_sign_changes",
    "DustModeHistory",
    "GrowthProvenance",
    "compute_history",
    "extract_dust_mode",
    "resolve_epoch_and_ics",
    "HarmonicMetadata",
    "HarmonicSignConvention",
    "map_delta_m",
    "map_delta_m_dln_a_derivative",
    "GrowthPipelineResult",
    "MappedDensityContrast",
    "ResolvedGrowthReference",
    "relative_growth",
    "resolve_reference",
    "run_growth_pipeline",
    "GrowthRates",
    "amplitude_near_zero_mask",
    "dDelta_d_dln_aD",
    "dDelta_d_dln_aobs",
    "dressed_chain_factor",
    "evaluate_rates",
    "f_bare",
    "f_dressed",
    "DenseSolveConfig",
    "DensityContrastMapping",
    "GrowthBackgroundPreset",
    "GrowthCoordinate",
    "GrowthD3Branch",
    "GrowthNumericsConfig",
    "GrowthReference",
    "GrowthReferenceCoordinate",
    "GrowthScenario",
    "GrowthSystem",
    "GrowthTiltForm",
    "GrowthWavenumberConvention",
    "LCDM_REFERENCE_H",
    "PAPER_REFERENCE_TIME_UNIT",
    "ResolvedBackground",
    "RootRefineConfig",
    "resolve_background",
]
