# Phase 1F-A internal adversarial compliance audit

Audit classification: `INTERNAL_ADVERSARIAL_COMPLIANCE_AUDIT`.

This audit was performed in the same implementation session. It is not an
independent scientific audit and must not be represented as one.

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
| 2 | Was the density zero mode silently selected? | The public signature requires `RegionalZeroModeClosure`; `None` fails, a nonzero-mean source fails, and the shift-by-constant study demonstrates non-identifiability. | PASS |
| 3 | Is normalization explicit and provenance-bearing? | Closure includes measure identity, scale factor, domain, frame, classification, and provenance. Exact measure identity is checked at solve time. | PASS |
| 4 | Does `rho_C` come from regional physical density rather than the H1 potential? | `density.py` forms `rho_r=rho_bar_r(1+delta_r)` and partitions those arrays. The module has no `ContinuumTransfer`, target-potential recovery, or carrier inverse-scalarization call. | PASS |
| 5 | Is a wall/void density discontinuity suppressed? | No continuity/flux operation touches density; the manufactured physical jump is `1.175`. | PASS |
| 6 | Does a global Laplacian cross the sharp density interface? | Regional stiffness assembly omits every mask-crossing edge and applies each broken operator only on its own regional indices. | PASS |
| 7 | Was `b_r-1` preserved? | Unequal-background test checks the complete regional formula with errors at or below `2.22e-16`; `b_w=4/3`, `b_v=2/3`. | PASS |
| 8 | Is the intertwining check tautological? | Carrier density is assembled before and independently of the regional operator. The broken operator is then applied as a diagnostic; the carrier inverse-transfer construction is absent. Residuals are below `2.4e-14`. | PASS |
| 9 | Are physical semantics still genuinely 3-D only? | Physical carrier assembly calls the sealed Phase 1E-G dimension guard. 1-D/2-D inversions survive as mathematical fixtures and fail before physical density/volume output. | PASS |
| 10 | Does morphology remain external? | `Phase1FAScientificState` binds an explicitly supplied, already-validated H1 morphology and requires exact object identity at carrier assembly. | PASS_WITH_EXPLICIT_CONDITIONS |
| 11 | Is any theoretical spectrum mislabeled observationally? | Regional fields use `k_wall_physical`/`k_void_physical` only with explicit regional metric/scale units. Carrier modes use `lambda_Gamma_n`; no generic or observational field is exported. | PASS |
| 12 | Was mode mixing incorrectly diagonalized? | Kernel result hard-rejects `mode_diagonal_assumed=True`; the fixture has maximum off-diagonal magnitude `0.6206389035552144`. | PASS |
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

- `PASS`: 19
- `PASS_WITH_EXPLICIT_CONDITIONS`: 3
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

## Blocking corrections

None remain.

## Non-blocking issues

- The structured regional reference solver currently supports the isotropic
  tensor-density case inherited from the Phase 1E-G reference backend.
- Regional scale labels depend on the explicit metric/scale-factor
  normalization closure.
- A truncated carrier spectral basis can leave an explicitly reported
  projection remainder; no completeness claim is made for a selected finite
  mode count.

## Frozen scientific limitations

- Morphology and normalization are external closure inputs.
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
