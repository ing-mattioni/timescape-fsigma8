# Phase 1F-A internal adversarial compliance audit

Audit classification: `INTERNAL_ADVERSARIAL_COMPLIANCE_AUDIT`.

This audit was performed in the same implementation session. It is not an
independent scientific audit and must not be represented as one.

The later independent read-only audit is preserved separately in
`phase1f_a_h1_carrier_dressed_closure_independent_audit.md`. The v2
documentation correction below adopts its evidence-strength findings without
changing the implementation, equations, tests, validator, or artifact.

## Scope and evidence

The audit inspected every new Phase 1F-A source module, all 35 targeted tests,
the deterministic validation script/artifact, the inventory, public exports,
the complete Git diff, and the frozen Phase 1E-G operator contracts. It also
ran both complete 539-test suites and independently regenerated the validation
artifact byte-for-byte.

Allowed finding classes are `PASS`, `PASS_WITH_EXPLICIT_CONDITIONS`,
`PARTIAL`, `UNSUPPORTED`, `INCORRECT`, and `NOT_APPLICABLE`.

## Challenge matrix

| # | Adversarial challenge | Evidence | Classification |
|---:|---|---|---|
| 1 | Was `Delta` silently treated as `delta_m`? | `reconstruct_regional_density` solves `K_r delta=-M_r Delta`; source and reconstructed fields are distinct records. Multi-mode inversion error is below `1.8e-16`. | PASS |
| 2 | Was the density zero mode silently selected? | The public signature requires `RegionalZeroModeClosure`; `None` fails and a nonzero-mean source fails. The recorded `3.0` is only the applied shift magnitude; the independent audit separately verified `L_r(constant)=0` and source invariance under a constant shift. | PASS |
| 3 | Is normalization explicit and provenance-bearing? | Closure includes measure identity, scale factor, domain, frame, classification, and provenance. V1 admits specifically the required mean-zero realization; arbitrary runtime normalization physics is not exposed, and Timescape prediction of that choice is `NOT_GRANTED`. | PASS |
| 4 | Does `rho_C` come from regional physical density rather than the H1 potential? | `density.py` forms `rho_r=rho_bar_r(1+delta_r)` and partitions those arrays. The module has no `ContinuumTransfer`, target-potential recovery, or carrier inverse-scalarization call. | PASS |
| 5 | Is a wall/void density discontinuity suppressed? | No continuity/flux operation touches density; the manufactured physical jump is `1.175`. | PASS |
| 6 | Does a global Laplacian cross the sharp density interface? | Regional stiffness assembly omits every mask-crossing edge and applies each broken operator only on its own regional indices. | PASS |
| 7 | Was `b_r-1` preserved? | Unequal-background test checks the complete regional formula with errors at or below `2.22e-16`; `b_w=4/3`, `b_v=2/3`. | PASS |
| 8 | Is the intertwining check tautological? | Carrier density is assembled physically and the forbidden inverse-carrier-transfer construction is absent. For regionally constant `b_r`, however, `R_intertwine,r=b_r R_elliptic,r`; the numerical gate is not independent and is blind to the `b_r-1` constant. The identity remains derived under the selected normalization, no-flux broken operator, and affine carrier definition; unequal-background carrier assembly separately protects the offset. | PASS_WITH_EXPLICIT_CONDITIONS |
| 9 | Are physical semantics still genuinely 3-D only? | Physical carrier assembly calls the sealed Phase 1E-G dimension guard. 1-D/2-D inversions survive as mathematical fixtures and fail before physical density/volume output. | PASS |
| 10 | Does morphology remain external? | `Phase1FAScientificState` binds an explicitly supplied, already-validated H1 morphology and requires exact object identity at carrier assembly. | PASS_WITH_EXPLICIT_CONDITIONS |
| 11 | Is any theoretical spectrum mislabeled observationally? | Regional fields use `k_wall_physical`/`k_void_physical` only with explicit regional metric/scale units. Carrier modes use `lambda_Gamma_n`; no generic or observational field is exported. | PASS |
| 12 | Was mode mixing incorrectly diagonalized? | Kernel result hard-rejects `mode_diagonal_assumed=True`. The reported scalar `0.6206389035552144` is basis-dependent inside a truncated degenerate eigenspace; independent eigenvalue-block norms `sqrt(2)` and `0.787` provide basis-invariant evidence of cross-eigenvalue mode mixing. | PASS |
| 13 | Was `Z` relabeled as velocity? | Expansion result is `delta_theta` with `DUST_EXPANSION_FIELD_RECONSTRUCTED_CONDITIONALLY`; its record exposes no velocity field. | PASS |
| 14 | Is zero boost implicit? | Only explicit divergence/potential closure types exist; omission fails; no zero-boost class or default exists. | PASS |
| 15 | Is the transverse boost sector hidden? | Every longitudinal result carries `TRANSVERSE_SECTOR_UNRESOLVED`; the divergence-free ambiguity test is explicit. | PASS_WITH_EXPLICIT_CONDITIONS |
| 16 | Can dressed density appear without a map? | Map closure is a required keyword-only input, and `None` fails before mapping. | PASS |
| 17 | Is a synthetic dressed map presented as physical? | Fixture and result retain `SYNTHETIC_VALIDATION_ONLY`; current Timescape theory alone remains `NOT_GRANTED`. | PASS_WITH_EXPLICIT_CONDITIONS |
| 18 | Was Candidate A changed or promoted? | Complete diff is additive Phase 1F-A content only; no Candidate A source/report changed. | PASS |
| 19 | Were D3 branch/default policies changed? | Frozen barotropic source is unchanged; both enum values remain and the branch argument remains mandatory. | PASS |
| 20 | Did forbidden observational functionality appear? | Public export scan contains no power-spectrum, smoothing-variance, redshift-space, tracer, bias, data, fit, covariance, or likelihood capability. Negative firewall prose is documentation only. | PASS |
| 21 | Can post-assembly scientific integrity be bypassed through normal tested mutation? | Frozen records, defensive arrays, detached fingerprints, and inherited Phase 1E-G snapshot validation detect geometry, mask, density result, boost closure, dressed closure, and classification mutation before use. | PASS |
| 22 | Were existing Phase 1E-G scientific objects weakened or changed? | No existing `transfer/` source or test file changed. All frozen 504 tests pass unchanged in both environments. | PASS |

Classification counts:

- `PASS`: 18
- `PASS_WITH_EXPLICIT_CONDITIONS`: 4
- `PARTIAL`: 0
- `UNSUPPORTED`: 0
- `INCORRECT`: 0
- `NOT_APPLICABLE`: 0

## Correction ledger

One non-blocking validation-fixture defect was found during this audit pass:
the initial synthetic carrier contrast could fall below `-1`, inappropriate
for a result labelled physical density. The implementation added a fail-closed
strict-positive regional density guard and rescaled only the synthetic density
fixture to the linear physical branch. No equation, tolerance, closure, frame,
or authorization changed. The artifact, reports, targeted tests, and both full
suites were regenerated after this correction.

No other audit finding was fixed silently.

The subsequent independent read-only audit required documentation-only
corrections: remove the stale `2.75` interface-jump fragment; classify the
intertwining identity as `DERIVED_ONLY_UNDER_ADDITIONAL_CONDITIONS` and its
numerical gate as `NOT_INDEPENDENT_OF_REGIONAL_ELLIPTIC_RESIDUAL`; identify
`b_r-1` as separately protected by physical carrier assembly; describe `3.0`
only as the homogeneous shift magnitude; and name the selected V1 policy
`EXPLICIT_REQUIRED_MEAN_ZERO_NORMALIZATION_CLOSURE` while retaining
`NORMALIZATION_PREDICTED_BY_TIMESCAPE: NOT_GRANTED`. Those corrections are
reflected here and in the validation report/inventory; no runtime content was
changed.

## Blocking corrections

None remain.

## Non-blocking issues

- The structured regional reference solver currently supports the isotropic
  tensor-density case inherited from the Phase 1E-G reference backend.
- Regional scale labels depend on the explicit metric/scale-factor
  normalization closure.
- A truncated carrier spectral basis can leave an explicitly reported
  projection remainder; no completeness claim is made for a selected finite
  mode count. The scalar maximum off-diagonal entry is basis-dependent in the
  frozen degenerate fixture, while independently reproduced eigenvalue-block
  norms establish the retained mode-mixing conclusion.

## Frozen scientific limitations

- Morphology is an external closure input. The V1 normalization record and
  provenance are required inputs for the explicitly selected mean-zero
  realization; the choice is not uniquely predicted by Timescape and the
  runtime does not expose arbitrary normalization physics.
- The boost is externally supplied; the transverse sector is unresolved.
- Dressed density requires an external spacetime map.
- There is no unique dressed Fourier mapping or observational spectral scale.
- There is no tracer velocity, observational normalization, redshift-space
  mapping, or data-comparison authorization.

## Validation status

- Targeted Phase 1F-A tests: 35 passed on Python 3.14.3 and 35 passed on
  Python 3.11.9.
- Complete repository: 539 passed on Python 3.14.3 and 539 passed on Python
  3.11.9.
- Failures/skips/xfails/warnings: zero in both reported runs.
- Deterministic artifact regeneration: byte-for-byte SHA-256 match.
- JSON, AST, import, public API, upstream, notebook hash, and diff checks: pass.

## Implementation readiness

`IMPLEMENTED_CONDITIONALLY` for the exact realization
`H1-1F-A-BROKEN-DENSITY-SPECTRAL-LONGITUDINAL-BOOST-V1`.

## Exact final authorization status

```text
UNIQUE_TIMESCAPE_PREDICTION: NOT_GRANTED
PHYSICAL_INTERFACE_CLAIM: NOT_GRANTED
OBSERVATIONAL_AUTHORIZATION: NOT_GRANTED
FSIGMA8_AUTHORIZATION: NOT_GRANTED
```
