# Phase 1F-C-R corrective v2 — A06 separation semantics

This successor record corrects the only blocking finding from the independent
post-remediation audit of commit
`72d8c51433662947b8981eb970a2bd90a94bbe4e`. It does not rewrite the v1 record.

## Scope

Four negative `pytest.approx` assertions had been changed from pytest's
parent-effective defaults, `rel=1e-6` and `abs=1e-12`, to `rel=2e-12` and
`abs=1e-14`. For an assertion of the form `actual != pytest.approx(expected)`,
shrinking the equality window weakens the required separation. Corrective v2
restores the parent-effective budget explicitly and changes no scientific
source file.

```text
PHASE_1F_C_R_V1_A06_STATUS:
FOUR_UNJUSTIFIED_NEGATIVE_PREDICATE_LOOSENINGS

PHASE_1F_C_R_V2_CORRECTION_SCOPE:
NEGATIVE_APPROX_SEPARATION_BUDGET_RESTORATION

SCIENTIFIC_SOURCE_CHANGED:
NO

SCIENTIFIC_EQUATIONS_CHANGED:
NO

A01_STATUS:
PRESERVED_PASS

A02_STATUS:
PRESERVED_PASS

A03_STATUS:
PRESERVED_PASS

A04_STATUS:
PRESERVED_PASS

A05_STATUS:
PRESERVED_PASS

A06_STATUS:
CORRECTED

A07_STATUS:
PRESERVED_PASS

UNJUSTIFIED_TOLERANCE_LOOSENINGS:
0
```

## Four corrected predicates

| Test | Quantities required to differ | Purpose |
|---|---|---|
| `test_v7_ordinary_generalized_and_continuum_coercivity_are_distinct`, first predicate | ordinary Euclidean constrained stiffness eigenvalue; continuum coercivity assumption | Prevent an externally supplied continuum lower bound from being treated as the computed discrete Euclidean diagnostic. |
| `test_v7_ordinary_generalized_and_continuum_coercivity_are_distinct`, second predicate | generalized mass-weighted Laplacian eigenvalue; ordinary Euclidean constrained stiffness eigenvalue | Preserve the distinction between the generalized metric/mass eigenproblem and the ordinary Euclidean stiffness problem. |
| `test_n11_morphology_difference_uses_target_metric_weighted_l2` | target-metric-weighted L2 difference; ordinary Euclidean norm divided by the reference scale | Prove that target metric weights affect the morphology diagnostic. |
| `test_t5_unequal_backgrounds_preserve_regional_offset_term` | assembled carrier density contrast; regional wall density contrast | Prove that the unequal-background carrier offset survives assembly. |

All four used `rel=2e-12, abs=1e-14` in v1. All four now explicitly use
`rel=1e-6, abs=1e-12`, exactly restoring the parent-effective asymmetric
`pytest.approx` equality window against the expected value.

## Adversarial validation

The four-case regression uses the near-equality family `0.1`, `0.10000005`,
and `0.1000001`. Differences of `5e-8` satisfy the flawed v1 negative
predicate because they exceed its roughly `2e-13` equality window. They do
not satisfy the corrected negative predicate because they remain inside the
restored roughly `1e-7` equality window. Each case also checks that a value
separated by twice `max(1e-12, 1e-6*abs(expected))` remains accepted as
genuinely distinct.

The unchanged scientific fixtures remain well separated:

| Predicate | Actual fixture values |
|---|---|
| ordinary versus continuum | `4.6862915010152335` versus `0.1` |
| generalized versus ordinary | `37.49033200812189` versus `4.6862915010152335` |
| target-weighted versus Euclidean | `0.8660254037844386` versus `1.118033988749895` |
| carrier versus regional wall | `0.3666666666666665` versus `0.02500000000000001` |

## Global A06 re-audit

The complete parent-to-v2 ledger contains the same 309 pre-existing
comparisons changed by v1. The final classifications are:

| Classification | Count |
|---|---:|
| `SEMANTICALLY_EXPLICIT_SAME_EFFECTIVE_BUDGET` | 121 |
| `STRICTER` | 171 |
| `LOOSER_WITH_JUSTIFICATION` | 17 |
| `UNJUSTIFIED_LOOSENING` | 0 |

The four corrected predicates moved from the independent audit's unjustified
category to `SEMANTICALLY_EXPLICIT_SAME_EFFECTIVE_BUDGET`. The 17 mixed-budget
comparisons retain v1's documented float64 absolute-floor justification.

## Preservation and validation

The v2 diff touches only three test modules and this successor report and
inventory. No file under `src/` changes. The accepted equations, signs, units,
normalizations, initial conditions, scientific realization and current
classification ontology remain byte-identical to v1. A01–A05 and A07 are not
reopened.

Directly affected suites passed 133 tests on both Python stacks before the
successor artifacts were written. Four parametrized regression cases raise
the complete count from 650 to 654. The complete suite passed all 654 tests on
Python 3.14.3 in 62.82 s and on Python 3.11.9 in 63.88 s. Both runs used
warnings as errors and had zero failures, skips, xfails and warnings.

The next scientific phase remains unstarted. Integration and all remote
changes remain outside this corrective checkpoint.
