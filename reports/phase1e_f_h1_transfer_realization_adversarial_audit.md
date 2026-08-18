# Phase 1E-F H1 Realization Adversarial Compliance Audit

## Audit verdict

ALL_SCIENTIFIC_AND_SOFTWARE_GATES_PASSED

The implementation conforms to the authorized conditional H1 research
contract under static inspection, 37 targeted cases in each required Python
environment, and 416-test complete regressions in each environment.

## Audited paths

- src/timescape_fsigma8/transfer/matrix_backend.py
- src/timescape_fsigma8/transfer/h1_realization.py
- src/timescape_fsigma8/transfer/__init__.py
- tests/test_phase1e_f_h1_transfer.py
- the four Phase 1E-F repository reports

No prior-phase source, test, report, configuration, dependency, notebook, or
artifact was modified.

## Required firewall challenges

### 1. No observational creep - PASS

The public runtime exports no tracer, bias, RSD, survey, likelihood, sigma8,
or fsigma8 callable. Authorization constants retain NOT_GRANTED for
observational, dressed-lightcone, RSD, and fsigma8 implementation.

### 2. No S1 fallback - PASS

There is no S1 solver, fallback selector, critical-set excision, weighted
rescue, smooth-to-sharp conversion, or B_chi regularization.

### 3. No physical-interface interpretation - PASS

Gamma is only a fixed Lagrangian mathematical carrier/transfer interface.
There is no interface displacement, thin-shell state, physical wall boundary,
finite-infinity junction, or radial-null matching API.

### 4. No hidden generic-k equality - PASS

No public Phase 1E-F callable accepts a parameter named k. The implementation
is not mode diagonal and equates none of the distinct wavenumber roles.

### 5. No new regional physical dynamics - PASS

RegionalBulkState has exactly Delta_w, Z_w, Delta_v, and Z_v. The authorized
alpha-weighted dust system is unchanged, curvature is derived, and no
interface force is inserted.

### 6. No fourth mismatch state - PASS

The compatibility system contains C_Delta, C_Z, and C_eff. C_P is a separate
constitutive gate and is not absorbed into C_eff.

### 7. No independent F_v state - PASS

F_v is algebraically constructed after checking A_P and is absent from the
four-dimensional differential state.

### 8. No arbitrary J_Xi history - PASS

J_Xi is derived from F_v_dot, A_f, E_DeltaXi_0_Gamma, and explicitly supplied
J_f_Gamma. There is no J_Xi input or time-history callback.

### 9. No target-only inverse claim - PASS

The result exposes no inverse method. It preserves regional transmission
responses and verifies only the authorized source/operator roundtrip.

### 10. No silent D3 default - PASS

The existing derived_4_10 and printed_4_15 labels are unchanged. No default
was added and no existing barotropic file was modified.

## Scientific challenge findings

| Challenge | Result |
| --- | --- |
| Exactly one global mean constraint | PASS |
| No independent regional constant projection | PASS |
| Joint value and conormal-flux continuity | PASS |
| Positive interval coercivity lower bound | PASS |
| Singular/noncoercive fixture rejected | PASS |
| A_P and effective denominator checked before division | PASS |
| Endpoint and partition degeneracies rejected | PASS |
| Unnormalized diagnostics retained on normalization failure | PASS |
| Wall/void mass weights and d_F term retained | PASS |
| Regional curvature remains derived | PASS |
| Required effective-sector and partition operators explicit | PASS |
| Analytic A_dot/source_dot derivatives | PASS |
| C_P independently verified as zero | PASS |
| Canonical pressure term retained in R_Z | PASS |
| R_Delta, R_Z, R_eff, and K_GM individually gated | PASS |
| Source provenance and analytic roundtrip | PASS |

## Deliberate failure tests

The suite rejects or detects partition endpoints, a too-small f_v f_w
product, A_P degeneracy, effective-normalization degeneracy, nonpositive
clock factors, insufficient coercivity, a singular/noncoercive fixture,
broken interface continuity or flux continuity, nonzero C_P without altering
C_eff, and an inconsistent time-independent J_f_Gamma declaration.

## Validation evidence

- Direct Python 3.14.3 harness: 37 passed.
- Targeted Python 3.14.3 pytest: 37 passed in 0.24s.
- Targeted Python 3.11.9 pytest: 37 passed in 0.25s.
- Full Python 3.14.3 regression: 416 passed in 31.19s.
- Full Python 3.11.9 regression: 416 passed in 24.50s.
- No failures, skips, xfails, or warnings were reported.

The previously incomplete environments were recreated without repository
dependency changes. Phase 1E-F file hashes were unchanged across remediation.

## Residual risk and limitations

1. The matrix backend validates an abstract constrained operator contract; it
   is not evidence for a physical Timescape discretization.
2. The interval coercivity bound is caller-declared and checked against the
   current reduced operator. A continuum backend must establish it over its
   complete configured interval.
3. Source recovery is a roundtrip in the admissible constrained dual
   representation, not a target-only inverse theorem.
4. No observational interpretation follows from the target GM tuple.

## Final audit disposition

    Scientific runtime created: YES, conditional H1 research runtime only
    Source equations changed outside authorized Phase 1E-F scope: NO
    Observational pipeline added: NO
    S1 fallback added: NO
    Full acceptance gate passed: YES
    Tag authorized after repository preservation checks: YES

    H1_CLEAN_NONDEGENERATE_TRANSMISSION_REALIZATION_IMPLEMENTED_CONDITIONALLY
    SCIENTIFIC_IMPLEMENTATION_AUTHORIZATION: SATISFIED
    OBSERVATIONAL_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
