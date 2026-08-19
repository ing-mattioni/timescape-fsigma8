# Phase 1E-G continuum H1 validation

## Scope

This report validates `H1-1E-G-COMOVING-CGI-ELLIPTIC-TRANSMISSION-V1` as a
`CONDITIONAL_H1_RESEARCH_RUNTIME`. The continuum equations are explicit
Phase 1E-G model-extension equations. The structured grid is numerical
validation only. Frozen regional/GM dynamics retain the paper references in
the Phase 1E-F implementation.

## Validation matrix V1--V34

| Gate | Result | Evidence |
|---|---|---|
| V1 flat wall operator | PASS | Periodic sine is an eigenvector with the exact discrete flat-Laplacian eigenvalue. |
| V2 negative-curvature void | PASS | Documented Poincare metric has nonconstant `J`, SPD inverse metric and `K=I` in 2-D. |
| V3 single global kernel | PASS | Pre-normalization stiffness nullity is exactly one. |
| V4 no regional projections | PASS | Projected wall and void integrals are separately nonzero and globally cancelling. |
| V5 global normalization | PASS | One `dmu_0` mean constraint gives solution mean below `2e-11`. |
| V6 ellipticity | PASS | Base inverse-metric bounds are `[1,1]`; non-SPD data reject. |
| V7 coercivity | PASS | Continuum assumption `0.1` is distinct from discrete bound `4.6862915010`. |
| V8 value continuity | PASS | Reconstructed interface trace jump `1.73e-18`. |
| V9 conormal continuity | PASS | Common-normal flux jump `0`; outward fluxes sum to zero. |
| V10 flux sign adversarial | PASS | Reversing the void common-normal flux produces residual `4`. |
| V11 source compatibility | PASS | Raw/projected source means `1.0/0.0`. |
| V12 provenance roundtrip | PASS | `raw -> Qb -> solve -> -A psi -> Qb` within `2e-10`. |
| V13 equal-geometry identity | PASS | Full weighted projection/solve/`L_D` chain returns admissible source within `2e-10`. |
| V14 full equal-region limit | PASS | `A_P=0` invokes Phase 1E-F fail-closed ontology reduction. |
| V15 wall injection | PASS | Explicit wall response is linear. |
| V16 void injection | PASS | Explicit void response is linear. |
| V17 superposition | PASS | Joint response equals wall plus void responses. |
| V18 curvature bridge | PASS | `C_R_Gamma` uses only curvature derived from GM Eq. (2.13). |
| V19 `E_DeltaTheta` | PASS | Equals `T_v[Z_v]-T_w[Z_w]`; no external field. |
| V20 `E_DeltaXi_0` | PASS | Equals `alpha_v T_v[Z_v]-alpha_w T_w[Z_w]`. |
| V21 `J_f` | PASS | Zero only after fixed-branch metadata validation; moving branch rejects. |
| V22 operator derivatives | PASS | `A_dot=A_ddot=0` follows from explicit fixed-comoving metadata. |
| V23 derivative commutation | PASS | Analytic transfer jets agree with independent centered finite differences. |
| V24 volume fraction | PASS | Consistent case residual `0`; inconsistent background fails closed. |
| V25 regional relabel | PASS | Swapped wall response equals consistently relabelled void response. |
| V26 endpoints | PASS | `f_v=0,1` invoke downstream ontology reduction before division. |
| V27 spectral API | PASS | No public generic `k`; explicit adversarial label rejects. |
| V28 mode mixing | PASS | Heterogeneous coefficient generates resolved non-source Fourier content. |
| V29 morphology sensitivity | PASS | Layer/island diagnostics are resolved and reported, not treated as error. |
| V30 convergence | PASS | Nested smooth oracle rates exceed explicit `1.8/0.8` L2/energy gates. |
| V31 discrete/contract consistency | PASS | Adapter recovers the admissible projected source jet. |
| V32 Phase 1E-F compatibility | PASS | Continuum-derived nontrivial transfer keeps all five downstream diagnostics green. |
| V33 D3 firewall | PASS | `derived_4_10` and `printed_4_15` remain explicit; no default. |
| V34 observational firewall | PASS | No observational/RSD/tracer/sigma8/fsigma8 callable is exported. |

## Source-measure oracle

For a nonconstant Poincare metric-volume ratio, a manufactured potential was
converted to

\[
s=-S u/(J\,w_0).
\]

The production `J s w_0` load reconstructed `u` within `2e-10`. An
independent deliberately incorrect load omitting `J` differed by more than
`1e-3`. This directly validates the weak-source measure transformation.

## Convergence

| Cells | L2 error | Discrete energy error |
|---:|---:|---:|
| 16 | 9.1575608e-3 | 5.7169648e-2 |
| 32 | 2.2761516e-3 | 1.4278520e-2 |
| 64 | 5.6821523e-4 | 3.5687680e-3 |

Successive L2 rates are `2.00837`, `2.00209`; energy rates are `2.00140`,
`2.00035`. The oracle is smooth and equal-geometry; these rates are not a
universal claim at discontinuous interfaces.

## Downstream residual classification

The Phase 1E-F v2 interpretation is preserved:

| Diagnostic | Classification | Base magnitude |
|---|---|---:|
| `C_P` | `CONSTRUCTED_IDENTITY_CHECK` | 0 |
| `R_Delta` | `CONSTRUCTED_IDENTITY_CHECK` | 0 |
| `K_GM` | `CONSTRUCTED_IDENTITY_CHECK` | 0 |
| `R_Z` | `DYNAMIC_COMPATIBILITY_CHECK` | 0 |
| `R_eff` | `DYNAMIC_COMPATIBILITY_CHECK` | 0 |

The existing nontrivial and adversarial Phase 1E-F dynamic-residual tests
remain part of the combined transfer suite.

## Additional adversarial coverage

All of the following fail closed or produce a nonzero diagnostic:

- non-SPD inverse metric and nonpositive `J`;
- overlapping/gapped regions and disconnected-carrier metadata;
- missing morphology and physical-junction metadata;
- unsupported anisotropy, moving partition/interface and time-dependent
  scalarization/clock branches;
- incompatible unprojected source;
- broken interface values, fluxes and normal convention;
- inconsistent background/geometric volume fraction;
- incorrect source-measure load;
- independent regional mean projection;
- generic `k` and observational callable creep.

## Test checkpoints

Development checkpoints:

```text
Python 3.14.3 targeted Phase 1E-G: 48 passed in 0.73s
Python 3.11.9 targeted Phase 1E-G: 48 passed in 0.79s
Python 3.14.3 combined Phase 1E-F + 1E-G: 90 passed in 0.87s
Python 3.11.9 combined Phase 1E-F + 1E-G: 90 passed in 0.91s
Python 3.14.3 complete repository: 469 passed in 10.89s
Python 3.11.9 complete repository: 469 passed in 12.26s
```

All release-gate runs reported zero failures, skips, xfails and warnings.

## Gate adjudication G0--G15

| Gate | Final status |
|---|---|
| G0 regional geometric provenance | `PASS` |
| G1 carrier/maps | `PASS_UNDER_EXPLICIT_MORPHOLOGY_CLOSURE` |
| G2 `A_Gamma` provenance | `PASS_AS_SELECTED_CGI_GEOMETRIC_CLOSURE_NOT_UNIQUE_TIMESCAPE_DERIVATION` |
| G3 source injection | `PASS` |
| G4 transmission derivation | `PASS_FROM_WEAK_FORM` |
| G5 kernel | `PASS` |
| G6 existence/coercivity | `PASS_UNDER_UNIFORM_ELLIPTICITY_AND_POINCARE` |
| G7 temporal regularity | `PASS_TIME_INDEPENDENT_OPERATOR` |
| G8 operator derivatives | `PASS_A_DOT_A_DDOT_ZERO_ON_SELECTED_BRANCH` |
| G9 effective-sector operators | `PASS_UNDER_HOMOGENEOUS_CLOCK_BRANCH` |
| G10 reproduction of Phase 1E-F contract | `PASS` |
| G11 discretization convergence | `PASS_IF_NUMERICAL_CONVERGENCE_VALIDATED` |
| G12 relabel/limits | `PASS` |
| G13 interface firewall | `PASS` |
| G14 spectral/frame firewall | `PASS` |
| G15 observational firewall | `PASS` |

## Verdict

All V1--V34 gates and the additional adversarial gates pass. This supports a
conditional continuum research realization only; it does not establish a
unique morphology, physical junction, full spacetime matching or observable.
