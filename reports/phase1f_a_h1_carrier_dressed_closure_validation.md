# Phase 1F-A H1 carrier-density, spectral, expansion and wall-boost validation

## 1. Repository checkpoint

- Parent checkpoint: `d262099ce3fe977af628ff233abed411e70a3c85`.
- Implementation branch: `phase-1f-a-h1-broken-density-spectral-boost`.
- Pinned scientific upstream: `590c6fd5332acb15f5683ebf392a0d7ce54983c5`.
- Pinned `ACPT_Timescape.ipynb` SHA-256: `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a`.
- Frozen pre-implementation regression: 504 passed on Python 3.14.3 and 504 passed on Python 3.11.9.

## 2. Frozen-result boundary

This implementation composes with, and does not edit, the validated Phase
1E-G continuum H1 operator. The regional differential state remains
`(Delta_w, Z_w, Delta_v, Z_v)`, with exact rank 4. Elliptic reconstruction,
spectral decomposition, an externally supplied boost, and an externally
supplied dressed map add no differential state.

The implementation does not change Candidate A, either D3 branch, any prior
growth equation, or any Phase 1E-F/G equation. There is no S1 fallback.

## 3. Realization

`H1-1F-A-BROKEN-DENSITY-SPECTRAL-LONGITUDINAL-BOOST-V1`

Role: `CONDITIONAL_THEORETICAL_FORWARD_REALIZATION`.

It is not a unique Timescape prediction. Morphology, regional homogeneous
density/expansion normalization, longitudinal dust-to-wall boost, and dressed
spacetime map remain explicit external closure inputs.

## 4. Implementation inventory

- `phase1f_a/models.py`: immutable closure records, numerical tolerances,
  dimensional and state-integrity gates.
- `phase1f_a/operators.py`: broken regional Laplace--Beltrami assembly,
  compatibility check, one-regional-constant normalization, and solve.
- `phase1f_a/density.py`: regional density inversion, physical sharp carrier
  density, background offsets, and regionwise intertwining.
- `phase1f_a/expansion.py`: conditional expansion-scalar inversion.
- `phase1f_a/spectral.py`: regional and carrier generalized spectra and a
  non-diagonal regional-to-carrier kernel.
- `phase1f_a/boost.py`: external divergence/potential closures and the
  scalar-longitudinal relative dust-to-wall field.
- `phase1f_a/dressed.py`: explicit physical-density-first dressed mapping.
- `phase1f_a/pipeline.py`: a thin sealed orchestrator with no closure defaults.

## 5. Public API inventory

The package exports `Phase1FAScientificState`, `Phase1FARealization`,
`RegionalDomainSpec`, `RegionalZeroModeClosure`, `BoundaryKernelPolicy`,
`Phase1FANumerics`, `ExternalBoostDivergenceClosure`,
`ExternalBoostPotentialClosure`, and `DressedSpacetimeMapClosure`.

Public operations are `reconstruct_regional_density`,
`assemble_carrier_density`, `reconstruct_regional_expansion`,
`regional_laplace_beltrami_spectrum`, `carrier_generalized_spectrum`,
`spectral_transfer_kernel`, `reconstruct_longitudinal_relative_velocity`, and
`map_carrier_density_to_dressed`. Every scientific argument is keyword-only,
and no morphology, normalization, boost, dressed map, mode count, branch, or
tolerance has a scientific default.

## 6. Mathematical definitions and provenance

The regional CGI definitions are inherited from Galoppo--Mourier (GM)
Eqs. (2.2), (2.19)--(2.24), arXiv:2511.17160v2:

```text
Delta_r = Delta_gamma_r delta_m,r
Z_r     = Delta_gamma_r deltaTheta_r
```

The carrier assembly, broken intertwining, explicit regional mean-zero
closure, scalar boost closure, and dressed-map closure are the explicitly
human-authorized Phase 1F-A model-extension equations. They have no paper
equation number and are not copied from the unlicensed upstream notebook.

## 7. Regional density inversion

On each supplied wall/void domain, the positive weak operator is assembled as
`K_r = -M_r Delta_gamma_r`. Interface-crossing edges are omitted under the
explicit `NO_FLUX_REGIONAL_INTERFACE_PERIODIC_CARRIER` boundary policy. This
is an inversion boundary policy, not a physical density interface law.

The solve is

```text
K_r delta_m,r = -M_r Delta_r
```

with a regional metric-volume mean constraint. A 4x4x4 manufactured fixture
with two nonzero transverse modes gave maximum reconstruction errors
`1.77e-16` (wall) and `9.02e-17` (void), and equation residuals `1.30e-14`
and `6.88e-15`.

## 8. Zero-mode closure

The Laplacian source does not determine a regional constant. V1 therefore
requires an immutable `RegionalZeroModeClosure` carrying the exact spatial
measure identity `a_r^3 dmu_gamma_r`, scale factor, domain, frame,
classification, and provenance. The selected closure is
`EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE`, not a Timescape prediction.

The manufactured solution and the solution shifted by 3 have the same CGI
source. The runtime refuses reconstruction without a closure and rejects a
source with forbidden nonzero regional mean. Reconstructed mean residuals
were `8.57e-18` (wall) and `2.66e-18` (void).

## 9. Physical carrier-density assembly

The physical field is assembled directly:

```text
rho_r = rho_bar_r (1 + delta_m,r)
rho_C = chi_w rho_w + chi_v rho_v
rho_bar_C = f_w rho_bar_w + f_v rho_bar_v
delta_m,C = rho_C/rho_bar_C - 1
```

For `rho_bar_w=2`, `rho_bar_v=1`, and equal physical volumes, the validation
obtained `b_w=4/3`, `b_v=2/3`. It independently checked

```text
delta_m,C|r = (b_r - 1) + b_r delta_m,r
```

with maximum errors `2.22e-16` and `5.55e-17`. The `b_r-1` offset is retained.
The H1 transmission potential is not used by this path.

## 10. Broken density intertwining

Only the broken regional operator is applied:

```text
L_r delta_m,C|r = b_r Delta_r
L_r = Delta_gamma_r on Omega_r
```

The wall and void maximum residuals were `2.40e-14` and `9.77e-15`. The
implementation does not define carrier density by an inverse carrier CGI
operator applied to transferred `Delta`; the public density module has no
such call path.

## 11. Interface-density firewall

Sharp regional density is neither smoothed nor subjected to the H1 potential
trace/flux conditions. The validation deliberately retains a maximum physical
density jump of `1.175`. Gamma remains a mathematical transfer interface and
is not promoted to a physical wall boundary or junction.

## 12. Physical three-dimensional semantics

Physical `rho_C`, physical regional volume, and physical density normalization
call the inherited Phase 1E-G genuine-dimension gate. The 3-D fixture passed
with volumes `(0.5, 0.5)`. The 1-D and 2-D regional inversion fixtures remain
usable as `MATHEMATICAL_OPERATOR_FIXTURE_ONLY`, but both fail closed before
physical carrier assembly.

The inherited covariance remains unchanged: under `gamma'=c^2 gamma` and
`a'=a/c`, literal measure times `a^3` scales as `c^(d-3)`. Only `d=3` is
physical. No reduced-dimensional lift exists.

## 13. Regional expansion reconstruction

The same explicitly normalized regional operator solves

```text
Delta_gamma_r deltaTheta_r = Z_r
```

from GM Eqs. (2.20)--(2.24). The 3-D manufactured maximum error was
`5.55e-16`, with equation residual `4.26e-14`. The result is classified
`DUST_EXPANSION_FIELD_RECONSTRUCTED_CONDITIONALLY`; its public record has no
velocity or tracer alias.

## 14. Regional and carrier spectral realization

The regional problem solves `K_r q=lambda_r M_r q`; its explicitly normalized
physical regional scale is `sqrt(lambda_r)/a_r`. The carrier solves
`K_C q=lambda_C M_C q`, using the mass matrix, not the ordinary Euclidean
stiffness spectrum. The first ordinary stiffness value was `0.5`, whereas the
first mass-weighted eigenvalue was `32.0`.

The maximum eigenpair residuals were `9.28e-15` (regional) and `2.29e-14`
(carrier). Carrier modes are labelled `lambda_Gamma_n`, not by a generic or
observational wavenumber.

## 15. Non-diagonal mode mixing

The transfer kernel is evaluated as

```text
U_mn^(r->C) = <phi_m^C, T_r phi_n^r>_C.
```

No diagonal assumption exists. In the layered synthetic fixture the maximum
off-diagonal magnitude was `0.6206389035552144`, demonstrating retained mode
mixing. This is not a map from regional or carrier labels to a dressed or
observational Fourier coordinate.

## 16. Boost closure semantics

There is no `ZeroBoostClosure`, no missing-argument fallback, and no inference
from the background lapse. The only V1 closure records are an explicit scalar
divergence and an explicit scalar potential, each carrying source/destination
frames, common time, spatial metric identity, units, domain, normalization,
classification, and provenance.

## 17. Longitudinal velocity reconstruction

For explicit divergence data, the runtime solves

```text
Delta_gamma psi_dw = vartheta_dw
v_dw,L^a = gamma^{ab} partial_b psi_dw
```

on the declared regional comoving metric. This Phase 1F-A closure is external,
not a Timescape boost prediction. The manufactured divergence residual was
`2.60e-14`. A nonzero forbidden source mean was rejected.

The field is named `longitudinal_relative_dust_to_wall_velocity`. It is not a
wall peculiar velocity without qualification and is never a tracer, galaxy,
line-of-sight, observed, or redshift-space velocity.

## 18. Transverse-sector limitation

Scalar divergence cannot determine an added divergence-free vector field.
The result always carries `TRANSVERSE_SECTOR_UNRESOLVED`; no full vector wall
velocity is claimed.

## 19. Dressed-map closure semantics

No dressed result exists without `DressedSpacetimeMapClosure`. With an
explicit `SYNTHETIC_VALIDATION_ONLY` inverse index pullback and destination
metric measure, the runtime maps `rho_C` first, recomputes the destination
mean, and only then forms the contrast. The destination mean residual was
`-6.94e-17`. Directly pulling back `delta_m,C` would differ by
`0.025497933993807287` in the fixture and is not the implementation.

## 20. Validation studies

The deterministic script covers manufactured density and expansion
inversions, zero-mode non-identifiability, unequal backgrounds, carrier mean,
sharp jump, broken intertwining, 3-D volume, reduced-dimensional rejection,
generalized spectra, ordinary/generalized separation, non-diagonal transfer,
external boost reconstruction and incompatibility, transverse ambiguity,
synthetic dressed mapping, and mutation rejection.

## 21. Numerical convergence

For the continuum source `-(2 pi)^2[sin(2 pi y)+0.25 cos(2 pi z)]`, the
regional reference solver gave:

| transverse resolution | L2 error | observed rate |
|---:|---:|---:|
| 4 | 0.1703370832 | -- |
| 6 | 0.07042529764 | 2.1783 |
| 8 | 0.03865140309 | 2.0855 |

These are validation-discretization rates for this smooth fixture, not a
universal rate across a sharp physical interface.

## 22. State-integrity validation

All scientific inputs/results are frozen and numerical arrays are defensive,
read-only copies. Detached fingerprints bind live closure/result content to
validated construction. Every downstream operation validates both its
Phase 1F-A record and the inherited Phase 1E-G operator snapshot. Deliberate
post-construction boost-provenance mutation failed closed.

## 23. Explicit external dependencies

- Phase 1E-G morphology and comoving metric normalization;
- regional density/expansion zero-mode closure and boundary/kernel policy;
- regional mean background densities and scale factors/physical volumes;
- external scalar dust-to-wall boost divergence or potential;
- external dressed spacetime map and destination metric measure.

None is inferred or defaulted.

## 24. Scientific limitations

The implementation does not derive a unique morphology, normalization,
dust-to-wall boost, transverse boost sector, dressed spacetime map, global
dressed Fourier map, tracer field, or observational normalization. It does
not make the H1 interface physical and does not identify `Delta_d` with local
matter density, `Z` with a wall/tracer velocity divergence, or any regional or
carrier spectral label with an observational one.

## 25. Authorization matrix and verdict

Final validation after the audit-led fixture correction collected 35 Phase
1F-A tests and 539 repository tests. Python 3.14.3 and Python 3.11.9 each
passed all 35 targeted and all 539 full-suite tests, with zero failures,
skips, xfails, or warnings reported.

| Capability | V1 status |
|---|---|
| regional density nonzero modes | GRANTED |
| regional full density | CONDITIONAL |
| physical H1 carrier density | CONDITIONAL |
| broken density intertwining | GRANTED_UNDER_SELECTED_NORMALIZATION |
| physical 3-D carrier semantics | CONDITIONAL_3D_ONLY |
| regional physical scale | CONDITIONAL |
| H1 generalized spectrum | GRANTED_THEORETICAL |
| regional-carrier spectral kernel | GRANTED_THEORETICAL |
| global dressed Fourier k | NOT_GRANTED |
| regional expansion reconstruction | CONDITIONAL |
| Timescape-predicted dust-wall boost | NOT_GRANTED |
| external longitudinal boost realization | CONDITIONAL |
| full vector wall velocity | NOT_GRANTED |
| dressed density from current Timescape theory alone | NOT_GRANTED |
| dressed density with explicit external map | CONDITIONAL |
| tracer velocity | NOT_GRANTED |
| matter power spectrum | NOT_GRANTED |
| smoothing variance at any radius | NOT_GRANTED |
| redshift-space distortion | NOT_GRANTED |
| observational growth observable | NOT_GRANTED |
| likelihood/data comparison | NOT_GRANTED |

Final machine verdict:

```text
H1-1F-A-BROKEN-DENSITY-SPECTRAL-LONGITUDINAL-BOOST-V1
SCIENTIFIC_REALIZATION_READINESS: IMPLEMENTED_CONDITIONALLY
DENSITY_CARRIER_CLOSURE: CONDITIONALLY_DERIVED
BROKEN_DENSITY_INTERTWINING: DERIVED
SPATIAL_SCALE_CLOSURE: LAPLACE_BELTRAMI_AND_SPECTRAL_KERNEL_CLOSED
GLOBAL_DRESSED_FOURIER_MAP: NOT_DERIVED
DUST_EXPANSION_RECONSTRUCTION: CONDITIONALLY_DERIVED
DUST_TO_WALL_BOOST_PREDICTION: NOT_DERIVED
LONGITUDINAL_WALL_VELOCITY: CONDITIONALLY_CLOSED_WITH_EXPLICIT_BOOST_INPUT
DRESSED_DENSITY: CONDITIONAL_ON_EXPLICIT_DRESSED_SPACETIME_MAP
DIFFERENTIAL_STATE_RANK: 4
UNIQUE_TIMESCAPE_PREDICTION: NOT_GRANTED
OBSERVATIONAL_AUTHORIZATION: NOT_GRANTED
FSIGMA8_AUTHORIZATION: NOT_GRANTED
```
density jump of `2.75`. Gamma remains a mathematical transfer interface and
density jump of `1.175`. Gamma remains a mathematical transfer interface and
