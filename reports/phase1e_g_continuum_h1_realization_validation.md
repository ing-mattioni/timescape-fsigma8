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
| V2 negative-curvature void | PASS | The 2-D Poincare metric has Gaussian/scalar curvature `-1/-2`, nonconstant `J`, SPD inverse metric and `K=I`; this is not a 3-D physical void. |
| V3 single global kernel | PASS | Pre-normalization stiffness nullity is exactly one. |
| V4 no regional projections | PASS | Projected wall and void integrals are separately nonzero and globally cancelling. |
| V5 global normalization | PASS | One `dmu_0` mean constraint gives solution mean below `2e-11`. |
| V6 ellipticity | PASS | Base inverse-metric bounds are `[1,1]`; non-SPD data reject. |
| V7 coercivity | PASS | Continuum assumption `0.1`, ordinary stiffness eigenvalue `4.6862915010`, and generalized mass spectrum `37.4903320081` are distinct. |
| V8 value continuity | PASS | Reconstructed interface trace jump `1.73e-18`. |
| V9 conormal continuity | PASS | Common-normal flux jump `0`; outward fluxes sum to zero. |
| V10 flux sign adversarial | PASS | Reversing the void common-normal flux produces residual `4`. |
| V11 source compatibility | PASS | Raw/projected source means `1.0/0.0`; raw regional provenance is retained while projected support can be global. |
| V12 provenance roundtrip | PASS | `raw -> Qb -> solve -> -A psi -> Qb` within inherited `1e-10`. |
| V13 equal-geometry identity | PASS | Full weighted projection/solve/`L_D` chain returns admissible source within `2e-10`. |
| V14 full equal-region limit | PASS | `A_P=0` invokes Phase 1E-F fail-closed ontology reduction. |
| V15 wall injection | PASS | Explicit wall response is linear. |
| V16 void injection | PASS | Explicit void response is linear. |
| V17 superposition | PASS | Joint response equals wall plus void responses. |
| V18 curvature bridge | PASS | `C_R_Gamma` uses only curvature derived from GM Eq. (2.13). |
| V19 `E_DeltaTheta` | PASS | Equals `T_v[Z_v]-T_w[Z_w]`; no external field. |
| V20 `E_DeltaXi_0` | PASS | Equals `alpha_v T_v[Z_v]-alpha_w T_w[Z_w]`. |
| V21 `J_f` | PASS | Zero only after fixed-branch metadata validation; moving branch rejects. |
| V22 operator derivatives | PASS | `A_dot=A_ddot=L_D_dot=L_D_ddot=0` follows from explicit fixed regional and target metadata. |
| V23 derivative commutation | PASS | Analytic transfer jets agree with independent centered finite differences. |
| V24 volume fraction | PASS | A `d=3` manufactured background consistency residual is `0`; metric normalization and background agreement are separate gates. |
| V25 narrowed relabel | PASS | `EQUAL_GEOMETRY_MASK_AND_SOURCE_INJECTION_RELABEL_COVARIANCE_OF_TRANSFER`; no full physical wall/void symmetry is claimed. |
| V26 endpoints | PASS | `f_v=0,1` invoke downstream ontology reduction before division. |
| V27 spectral API | PASS | No public generic `k`; explicit adversarial label rejects. |
| V28 mode mixing | PASS | Heterogeneous coefficient generates resolved non-source Fourier content. |
| V29 morphology sensitivity | PASS | Reduced-dimensional operator-level target-metric L2 layer/island diagnostic plus 16/32/64 shifted-layer refinement; no physical volume is formed. |
| V30 convergence | PASS | Nested smooth oracle rates exceed explicit `1.8/0.8` L2/energy gates. |
| V31 discrete/contract consistency | PASS | Adapter recovers the admissible projected source jet. |
| V32 Phase 1E-F compatibility | PASS | Continuum-derived `R_Z/R_eff` fixture has nonzero termwise cancellations and predictable adversarial failures. |
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

## Additive v3 physical-volume dimensional matrix D1--D7

The carrier retains `d in {1,2,3}` for mathematical operator validation, but
physical Timescape volume semantics are `PHYSICAL_TIMESCAPE_THREE_VOLUME_ONLY`.
For `gamma'=c^2 gamma`, the literal measure obeys `mu_d'=c^d mu_d`; with
`a'=a/c`, `mu_d'(a')^3=c^(d-3)mu_d a^3`. The reproduced factors for `c=2`
are `1/4`, `1/2`, and `1` for `d=1,2,3`, respectively. The first two are
rejected, not renormalized.

| Gate | Result | Evidence |
|---|---|---|
| D1 | PASS | Complete physical-volume/downstream path accepts a valid `d=3` carrier and returns `(V_w,V_v)=(0.5,0.5)`. |
| D2 | PASS | `d=1` literal measures remain available, while all physical `V_r`/`f_v` APIs raise `ContinuumDimensionalContractError`. |
| D3 | PASS | The same fail-closed contract holds in `d=2`. |
| D4 | PASS | `EXTERNALLY_SUPPLIED_REFERENCE_VOLUME` in `d=1,2` remains a measure-consistency provenance mode and cannot bypass the dimension guard. |
| D5 | PASS | Dedicated 1-D weighted and 2-D periodic transfer fixtures still exercise projection, solve, and target scalarization. |
| D6 | PASS | N5 remains `PHYSICAL_NORMALIZATION_COVARIANCE` in `d=3` for base `(1/3,2/3)`, transformed `V_v'=c^3V_v`, and `a_v'=a_v/c`. |
| D7 | PASS | All public metric-derived/declaration/assembly/fraction methods and the continuum-to-Phase-1E-F bridge are dimension guarded. |

## Additive v4 post-assembly integrity matrix I1--I12

| Gate | Result | Evidence |
|---|---|---|
| I1 | PASS | Ordinary carrier reassignment raises `ContinuumStateIntegrityError`. |
| I2 | PASS | Low-level 1-D-to-3-D carrier replacement is detected before physical regional-volume evaluation. |
| I3 | PASS | The same replacement is detected before physical `f_v`. |
| I4 | PASS | The same replacement is detected before continuum-to-Phase-1E-F bridge evaluation. |
| I5 | PASS | Regional normalization replacement is rejected normally and detected after representative low-level tampering. |
| I6 | PASS | Immutable cached normalization diagnostics cannot authorize changed normalization state. |
| I7 | PASS | Replaced time-dependent target metadata is detected by target derivatives and `transfer_jet`. |
| I8 | PASS | The same target-time replacement is detected before downstream bridge evaluation. |
| I9 | PASS | `EXTERNALLY_SUPPLIED_REFERENCE_VOLUME` cannot turn a tampered reduced-dimensional operator into a physical carrier. |
| I10 | PASS | Public geometry/mask arrays are read-only, matrices are defensive copies, and private sparse-matrix mutation is fingerprint-detected. |
| I11 | PASS | An untouched 3-D operator still completes transfer, physical volume and downstream realization. |
| I12 | PASS | An untouched 1-D operator still performs mathematical transfer while physical `f_v` remains forbidden. |

The integrity mechanism is not a claim of resistance to an attacker who
rewrites every private field and the private expected snapshot. It closes
normal public mutation and representative isolated Python-level tampering,
so no result is returned from state different from the validated assembly.

No reduced-dimensional effective-3-D lift, transverse-area closure, padding,
embedding, or silent dimensional promotion exists.

## Morphology metric and refinement

The primary sensitivity norm is
`sqrt(sum_i w_i J_D,i |Y[M1]-Y[M2]|^2) / max(reference_scale,floor)` with
explicit `(reference_scale,floor)=(1.0,1e-12)`. The layer/island comparison
uses `COMMON_LATENT_MANUFACTURED_FIELD`; because both flat fixtures assemble
the same stiffness matrix, it is supported-source/mask-placement sensitivity,
not heterogeneous-operator sensitivity.

For shifted versus unshifted half-domain families the 16/32/64-cell
`T_w[Delta_w]` values are all `0.7071067812`, and the `T_v[Delta_v]` values
are all `0.3535533906`. Classification:
`CONVERGED_EQUAL_GEOMETRY_MASK_PLACEMENT_DIAGNOSTIC`. The compared stiffness
operators are identical: this is mask/source placement followed by
projection, Green response and target scalarization. It does not make either
morphology or any reduced-dimensional measure a physical Timescape volume.

## Discrete spectral diagnostics

The ordinary Euclidean constrained stiffness eigenvalues at 16/32/64 cells
are `2.43585496`, `1.22974205`, `0.61635499`, showing mesh scaling toward
zero. The corresponding generalized `Kx=lambda Mx` values are `38.97367935`,
`39.35174573`, `39.44671910`, converging toward `4 pi^2`. These are discrete
diagnostics. Continuum coercivity remains conditional on ellipticity, measure
equivalence, connectedness and the global Poincare assumption.

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
remain part of the combined transfer suite. Phase 1E-G now additionally uses
the real continuum bridge. In units of its common carrier shape, the
independently manufactured `R_Z` terms are
`(-0.04,-0.0448,0.2,-0.1152,pressure)`. The pressure term is analytically
zero and has reproduced numerical maximum `2.7755575616e-17`. The `R_eff`
terms are `(0.095808,0.024192,-0.12,pressure)`; its analytically zero pressure
term has reproduced maximum `3.8857805862e-18`. All non-pressure terms are
nonzero. Perturbing `alpha_w.first` by
`0.05` produces exactly `0.012 phi`; perturbing `Q_bar.first` by `0.5`
produces exactly `-0.0036 phi`. Both exceed `1e-10` and fail closed.

## Additive v2 correction matrix N1--N16

| Gate | Result | Evidence |
|---|---|---|
| N1 | PASS | Time-dependent target metric rejects before transfer. |
| N2 | PASS | Regional metric-normalization provenance is required. |
| N3 | PASS | Declared/reference metric-measure mismatch rejects. |
| N4 | PASS | Constant metric rescaling with stale volume contract rejects. |
| N5 | PASS | `PHYSICAL_NORMALIZATION_COVARIANCE`: consistently transformed `gamma/a/V_i` uses a distinct ID and preserves the 3-D physical volumes and `f_v`. |
| N6 | PASS | Base volume comparison is labelled `MANUFACTURED_BACKGROUND_CONSISTENCY_FIXTURE`. |
| N7 | PASS | Continuum-derived nontrivial `R_Z` cancellation. |
| N8 | PASS | Continuum-derived nontrivial `R_eff` cancellation. |
| N9 | PASS | Predictable continuum-derived `R_Z` adversarial increment. |
| N10 | PASS | Predictable continuum-derived `R_eff` adversarial increment. |
| N11 | PASS | Target-metric weighted L2 differs from Euclidean norm on nonuniform weights. |
| N12 | PASS | 16/32/64 morphology metric is `CONVERGED_EQUAL_GEOMETRY_MASK_PLACEMENT_DIAGNOSTIC`. |
| N13 | PASS | Raw wall provenance survives global projected support. |
| N14 | PASS | Raw void provenance survives global projected support. |
| N15 | PASS | Ordinary and generalized spectra are separately exposed. |
| N16 | PASS | V25 claim narrowed to equal-geometry mask/injection transfer covariance. |

## Additional adversarial coverage

All of the following fail closed or produce a nonzero diagnostic:

- non-SPD inverse metric and nonpositive `J`;
- missing/inconsistent metric-normalization provenance and stale metric scale;
- overlapping/gapped regions and disconnected-carrier metadata;
- missing morphology and physical-junction metadata;
- unsupported anisotropy, moving partition/interface and time-dependent
  regional or target scalarization/clock branches;
- incompatible unprojected source;
- broken interface values, fluxes and normal convention;
- inconsistent background/geometric volume fraction;
- attempted `d=1` or `d=2` promotion to physical regional volumes or `f_v`,
  including external-reference-volume provenance;
- incorrect source-measure load;
- independent regional mean projection;
- nontrivial continuum-derived `R_Z/R_eff` dynamic corruption;
- generic `k` and observational callable creep.

## Test checkpoints

Development checkpoints:

```text
Python 3.14.3 targeted Phase 1E-G: 83 passed in 9.50s
Python 3.11.9 targeted Phase 1E-G: 83 passed in 11.23s
Python 3.14.3 combined Phase 1E-F + 1E-G: 125 passed in 9.16s
Python 3.11.9 combined Phase 1E-F + 1E-G: 125 passed in 9.29s
Python 3.14.3 complete repository: 504 passed in 23.63s
Python 3.11.9 complete repository: 504 passed in 22.59s
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
