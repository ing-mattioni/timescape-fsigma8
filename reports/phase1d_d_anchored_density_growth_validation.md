# Phase 1D-D — Anchored conditional density-growth validation

Date: 2026-07-19. Work branch:
`phase-1d-d-anchored-density-growth`. Frozen parent:
`f960a9054ae9db3a7c378557ac3a2938c5ff7ef0`.

Machine-readable companion (generated and Git-ignored):
`artifacts/independent/phase1d_d_anchored_density_growth_validation.json`.

## 1. Scope and explicit exclusions

This phase implements one externally anchored conditional density-growth
diagnostic for the clean comoving and Mészáros systems. It is a
normalisation-only post-processing operation on an already resolved frozen
Phase 1D-B result.

It implements no matter or primordial power spectrum, transfer function,
window function, smoothing integral, sigma_R, sigma_8-from-a-spectrum,
standard observational f sigma_8, RSD mapping, bias, AP conversion,
observational dataset, covariance, likelihood, fit, or inference. It has no
barotropic path and no D3, tilt, or barotropic-wavenumber input. No figure or
plotting code was created.

The supplied anchor is external. The Timescape evolution does not predict
it. All validation anchors in this phase are synthetic and have no
observational interpretation.

## 2. Frozen checkpoint and preflight

Before the work branch was created, the repository was clean on
`phase-1d-d-t-d3-frame-mapping` at
`f960a9054ae9db3a7c378557ac3a2938c5ff7ef0`. The annotated tag
`phase-1d-d-t-d3-frame-mapping-v1` peeled to that commit. All eight frozen
tags were ancestors. The upstream clone was clean at
`590c6fd5332acb15f5683ebf392a0d7ce54983c5`; the pinned notebook hash was
`86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a`.
`git diff --check` passed. Both pre-existing suites passed: 337/337 on
Python 3.14.3 and 337/337 on Python 3.11.9.

Only then was the local, unpushed branch
`phase-1d-d-anchored-density-growth` created at the exact frozen commit.

The validation script treats that commit as the immutable
`base_phase1d_d_t_checkpoint`, not as the commit that must contain Candidate
A. It requires the base to be an ancestor of `execution_head`, restricts every
committed path since the base and every working-tree path to the five Phase
1D-D candidates, and requires an empty index. It therefore supports both the
present `uncommitted_permitted_working_tree` state (execution HEAD equals the
base, no committed paths since it, five permitted working paths) and a future
`clean_committed_tree` descendant. The upstream commit and notebook hash are
checked in either state.

## 3. Scientific definition

For the frozen clean-system signed relative growth

    G(t; t_ref) = Delta_d(t) / Delta_d(t_ref),

the implementation evaluates Phase 1D-A equations (D6a)–(D6b):

    A_anchor(t) = sigma8_anchor_at_reference * G(t; t_ref),
    Q_anchor(t) = f(t) * A_anchor(t)
                = sigma8_anchor_at_reference * dG/d ln(a_coordinate)
                = sigma8_anchor_at_reference / Delta_d(t_ref)
                  * dDelta_d/d ln(a_coordinate).

For `bare_aD`, the frozen analytic derivative is
`dDelta_d/d ln(a_D) = -3Z/Theta`, from [GM] Eq. (4.14). For
`dressed_redshift`, it is multiplied by the exact tracker factor

    (2 + f_v)^2 / (4 + f_v + 4 f_v^2).

No numerical differentiation is performed.

## 4. Why this is not predicted sigma8 or observational f sigma8

The scalar anchor is supplied by the caller and is not computed from a
spectrum. The package does not evaluate the sigma_8 integral and does not
predict the supplied normalisation. `Q_anchor` is a conditional density-growth
derivative in the explicitly selected theoretical growth coordinate. No
galaxy-velocity identification, dressed redshift-space map, bias prescription,
survey fiducial conversion, or RSD estimator is supplied. It is therefore not
standard observational f sigma_8 and is not likelihood-ready.

The public name deliberately remains
`anchored_density_growth_diagnostic`. No public prediction or observational
f-sigma-8 name was introduced.

## 5. A1A6 assumptions

`AnchoredDiagnosticAssumptions` is a frozen, no-default record. It contains
six explicit booleans, all of which must be literal `True`:

| condition | recorded meaning | independent enforcement |
|---|---|---|
| A1 | linear evolution over the evaluated interval | caller acknowledgement; no nonlinear extension exists |
| A2 | k-free operator and k-independent initial mixture over the matched support | API accepts only the two clean systems |
| A3 | reference spectrum shape fixed apart from common growth | caller acknowledgement; no spectrum is inferred |
| A4 | one fixed radius/h/frame/reciprocal-unit convention | acknowledgement plus mandatory anchor metadata |
| A5 | positive differentiable G over the full interval | actual G, rates, derivative, and crossing metadata checked |
| A6 | anchor is consistent at exactly the resolved reference | direct `ResolvedGrowthReference` binding and equality check |

False acknowledgements, non-boolean lookalikes, and incomplete construction
raise. A2 and A5 are not accepted solely on trust.

## 6. System eligibility

The API accepts only `GrowthSystem.COMOVING` and `GrowthSystem.MESZAROS`.
Barotropic `GrowthPipelineResult` objects are rejected before a diagnostic is
formed. A Delta_d root, endpoint zero, non-positive or non-finite G, or any
non-finite selected logarithmic rate or non-logarithmic derivative also
raises.

The function signature is exactly:

    anchored_density_growth_diagnostic(*, growth_result, anchor, assumptions)

It has no system, D3 branch, tilt form, or wavenumber-convention parameter.

## 7. Comoving primary interpretation

The comoving result carries the machine token `comoving_primary`. It is the
primary clean, scale-independent carrier of this conditional diagnostic.
For the declared validation-only baseline at the present endpoint:

| quantity | value |
|---|---:|
| G | 6.322866885745406 |
| f_bare | 0.4251005809546847 |
| A_anchor (synthetic anchor 0.8) | 5.058293508596325 |
| Q_anchor,bare | 2.150283509143608 |

These are conditional validation numbers, not observational predictions.

## 8. Mészáros comparison-only caveat

Every Mészáros result carries `meszaros_comparison_only` and the mandatory
human-readable caveat:

> comparison_baseline_only: the Meszaros approximation is formally
> inapplicable to the Timescape framework and is retained only as a
> comparison baseline.

Its validation endpoint is `G=5.437251164528154`,
`f_bare=0.3102677844342826`, `A_anchor=4.349800931622523`, and
`Q_anchor=1.3496030977846987`. The Mészáros and comoving results are never
averaged, enveloped, aggregated, or interpreted as a statistical uncertainty.

## 9. Anchor and reference model

`ExternalDensityAmplitudeAnchor` is frozen and has no defaults. It records a
positive finite dimensionless `sigma8_anchor_at_reference`, a nonempty
provenance label, an enum provenance kind (`external_import` or
`synthetic_validation_only`), the exact resolved reference object, smoothing
radius definition, h convention, spatial frame, and reciprocal-unit
statement. Missing or empty metadata and raw enum lookalikes raise.

The validation anchor is exactly 0.8 with provenance
`synthetic_validation_only`; it is not imported from any measurement. The
reference is dressed `z_ref=10`, resolved continuously by the frozen pipeline.
It is not a sampled grid point: the nearest sample is index 20, offset by
`-1.0529863713541754e-4` solver-time units. The reference value is constructed
from the stored continuous dense-reference amplitude: normalising that
amplitude by itself gives `G(t_ref)=1`, hence `A_anchor(t_ref)=0.8`. This is a
consequence of the stored amplitude, not a second independent dense
evaluation. Separately, the sampled `G` array is checked against
`history.delta_d / Delta_d(t_ref)` with a global zero-safe `1e-14` gate; it
does not pretend the nearest sample is the reference.

## 10. Public API and no-default policy

Minimal public exports are:

- `anchored_density_growth_diagnostic`;
- `AnchoredDiagnosticAssumptions`;
- `ExternalDensityAmplitudeAnchor`;
- `AnchoredDensityGrowthDiagnosticResult`;
- `AnchorProvenanceKind`;
- `AnchoredGrowthModelRole`;
- `AnchoredDiagnosticClassification`.

All scientific function arguments are keyword-only and mandatory. Every
field in the three dataclasses has neither a default nor a default factory.
No validation baseline, anchor value, reference, system, coordinate, preset,
rate convention, epoch, h convention, or spatial frame is a package default.

## 11. Implementation inventory

The new scientific module is
`src/timescape_fsigma8/growth/anchored_diagnostic.py`. It consumes
`GrowthPipelineResult` and reuses its exact signed G, resolved reference,
analytic rates, non-logarithmic derivatives, grids, background coordinates,
crossing record, scenario identifier, and provenance.

It performs only finite-array validation, multiplication, division by the
already validated nonzero reference amplitude, and residual evaluation. It
does not import the perturbation package, a barotropic or forensic module,
or a script. It calls no solver, root finder, interpolator, finite-difference
routine, fit, smoothing routine, or integration routine. No frozen growth
module was changed; `growth/__init__.py` received only the minimal exports and
the corrected explanatory D3/sigma8 scope wording, with no executable change.

## 12. Algebraic identity validation

Normalization is zero-safe and global: each normalized L-infinity residual
uses `max(max(abs(left)), max(abs(right)), float64 tiny)`. No pointwise
division by a zero-crossing component is used.

| system | identity | max absolute residual | normalized L-infinity | gate |
|---|---|---:|---:|---:|
| comoving | sampled G = history Delta_d / stored reference amplitude | 0 | 0 | 1e-14 |
| comoving | Q = f A | 0 | 0 | 1e-12 |
| comoving | Q = anchor dG/dln a | 8.881784197001252e-16 | 4.1305177476520724e-16 | 1e-11 |
| Mészáros | sampled G = history Delta_d / stored reference amplitude | 0 | 0 | 1e-14 |
| Mészáros | Q = f A | 0 | 0 | 1e-12 |
| Mészáros | Q = anchor dG/dln a | 6.661338147750939e-16 | 4.277286500499717e-16 | 1e-11 |

All gates were declared before evaluation and passed without relaxation.

## 13. Anchor scaling

Changing only the synthetic anchor from 0.5 to 1.0 produced exactly a factor
2 in both A_anchor and Q_anchor. Both normalized residuals were exactly zero.
G and f were bitwise unchanged, and the scenario identifier, resolved
reference, and crossing metadata were unchanged. This is external-anchor
normalisation dependence, not a Timescape prediction.

## 14. Bare versus dressed coordinate

G and A_anchor were exactly unchanged when only the growth coordinate changed.
The exact tracker relation was verified:

    Q_anchor,dressed / Q_anchor,bare
    = f_dressed / f_bare
    = (2+f_v)^2/(4+f_v+4f_v^2).

The f identity residual was exactly zero. The Q identity had max absolute
residual `4.440892098500626e-16` and normalized residual
`1.904945633219968e-16`, below the `1e-12` gate. At the endpoint the factor
is `1.084156333813626`; `Q_bare=2.150283509143608` and
`Q_dressed=2.3312434859330327`.

## 15. Delta_d versus delta_m basis invariance

The keep-Delta_d result was compared with mapped coefficients at two explicit
nonzero solver labels, `k_code=7` and `k_code=13`. The frozen mapping
`delta_m=-Delta_d/k_code^2` was used; neither k entered the clean dynamics.
G, f, A_anchor, and Q_anchor were exactly equal to the canonical Delta_d
outputs. The largest alternative-identity normalized difference was
`2.0652588738260362e-16` for each label, below the `1e-14` gate. No physical
or observational wavenumber map was inferred.

## 16. Reference-coordinate equivalence

The dressed-redshift reference `z_ref=10` was resolved once, then supplied to
a separate pipeline run as its exact bare solver time. The two resolved times
differed by exactly zero and every compared G, f, A_anchor, Q_anchor, and
alternative-identity array had normalized L-infinity error zero. No new
reference solver or interpolation was introduced.

## 17. Controlled one-factor scenario studies

The validation baseline is comoving, notebook reference, upstream-unconverted
rate, upstream 0.218-Gyr epoch, bare a_D, keep Delta_d, z_ref=10, synthetic
anchor 0.8, tight DOP853. Each row changes exactly one factor; values are
alternative minus baseline endpoints. Grid-bearing epoch/preset alternatives
are not silently interpolated to a common time.

| isolated factor | alternative | delta G | delta f | delta A_anchor | delta Q_anchor | category |
|---|---|---:|---:|---:|---:|---|
| system | Mészáros | -0.8856157212172526 | -0.11483279652040213 | -0.7084925769738017 | -0.8006804113589094 | model/approximation |
| preset | paper_reference | -0.002627855578010596 | -7.741391695403887e-6 | -0.0021022844624081216 | -0.0009328243030544137 | convention/scenario |
| rate units | lcdm_to_timescape_converted | -0.05626680929629657 | -0.00021776156266634095 | -0.045013447437036724 | -0.020226942356459165 | convention/scenario |
| epoch | dressed_z20 | -0.08649281047257595 | -0.0002586654508628383 | -0.06919424837806076 | -0.030705022793779957 | convention/scenario |

Growth coordinate, anchor, density basis, and reference representation are
reported separately in Secs. 13–16. No difference is labelled a confidence
interval or statistical uncertainty.

## 18. Solver convergence

The independent reference uses two separately explicit high-accuracy
configurations on 1000 samples. `REFERENCE_SOLVER` is sampled DOP853 with
`rtol=2e-13`, `atol=2e-15`, `max_step=inf`, `first_step=None`;
`REFERENCE_DENSE` is dense DOP853 with the same four controls. Thus both the
sampled trajectory and continuous reference resolution use the declared
reference tolerances. The reference sampled/dense nfev values are 1076/1076
for comoving and 1106/1106 for Mészáros.

Candidate runs retain the ordinary validation dense configuration: DOP853,
`rtol=1e-11`, `atol=1e-13`, `max_step=inf`, `first_step=None`. Their sampled
configuration is respectively tight DOP853, tight RK45, or tight Radau with
the frozen explicit solver controls recorded in the JSON. Each method was
compared for G, f, A_anchor, Q_anchor, and the alternative non-logarithmic
evaluation. Every quantity records max absolute error, global zero-safe
normalized L-infinity, RMS normalized error, worst time/redshift, endpoint
error, and scale.

| system | run | sampled nfev | worst quantity | worst normalized L-infinity | gate |
|---|---|---:|---|---:|---:|
| comoving | tight DOP853 | 701 | f | 1.1888523218651935e-11 | 2e-8 |
| comoving | tight RK45 | 848 | f | 2.6818292584457146e-10 | 2e-8 |
| comoving | tight Radau | 4656 | alternative Q | 3.2329975462668203e-11 | 2e-8 |
| Mészáros | tight DOP853 | 716 | f | 1.0671648389113698e-11 | 2e-8 |
| Mészáros | tight RK45 | 836 | f | 2.5092085582487974e-10 | 2e-8 |
| Mészáros | tight Radau | 5018 | alternative Q | 2.993102516837229e-11 | 2e-8 |

All six method/system runs passed. The gate was not changed after seeing the
results.

## 19. Numerical error taxonomy

The artifact separates:

- numerical finite-precision and sampling error;
- solver method/tolerance error;
- external-anchor normalisation dependence;
- convention/scenario dependence;
- model/approximation dependence (comoving versus comparison-only Mészáros).

There is no spectrum-normalisation calculation and no observational-systematic
claim. An envelope over alternatives is never a confidence interval.

## 20. Machine-readable artifact schema

The generated JSON records the phase/checkpoint/upstream provenance, exact
equations, A1–A6 definitions, API inventory, exclusions, synthetic baseline,
anchor and reference metadata, per-system role, identity metrics, scaling,
bare/dressed and density-basis studies, reference equivalence, controlled
one-factor results, convergence details, declared gates, uncertainty taxonomy,
both test environments, exact file inventory, and preservation statement.

It has exactly 25 top-level sections. After the final write the script reads
and parses the JSON, checks that exact section set, rechecks that every gate
passes, verifies that both test-environment records are final rather than
pending, and confirms a second deterministic serialization is byte-identical.
The current final SHA-256 is
`fda1f5bd1001ab8a113bd5f25e23b8535e408a09527c1602374ef931fc3cd44d`.

Every represented anchor is explicitly `synthetic_validation_only`. No
observational dataset, survey number, spectrum, sigma_R integral, standard
observational f sigma_8, RSD comparison, likelihood, or fit is present.

## 21. Complete test results

Both suites ran against the same source tree with
`pytest -q -p no:cacheprovider` and an external system-temp basetemp. They
tested the provisional schema-bearing artifact. After their results were
inserted, the final artifact was independently parsed and subjected to the
integrity checks in Sec. 20; the suites are not claimed to have tested the
post-suite artifact bytes.

| environment | exact versions | result |
|---|---|---|
| Python 3.14 | Python 3.14.3; NumPy 2.5.1; SciPy 1.18.0; pytest 9.1.1; pluggy 1.6.0 | 379 passed; 0 failed, skipped, xfailed, warnings |
| Python 3.11 | Python 3.11.9; NumPy 2.4.6; SciPy 1.17.1; pytest 9.1.1; pluggy 1.6.0 | 379 passed; 0 failed, skipped, xfailed, warnings |

The 42 new collected cases cover construction, no defaults, immutability,
anchor validation, A1–A6, reference binding, enum rejection, both eligible
systems, Mészáros caveat, barotropic rejection, signatures, identities,
scaling, chain conversion, density-basis invariance, a positive tampered-G
regression, result-metadata invariants, A5 failures, purity, serialization,
provenance, and artifact schema.

## 22. Forbidden-scope audit

AST/import checks confirm that the new package module imports no perturbation,
barotropic, forensic, or script module. It calls no ODE solver, numerical
derivative, interpolation, fit, smoothing, quadrature, or convolution. The
diagnostic was also executed while solver and pipeline entry points were
monkeypatched to raise; no call occurred.

No public symbol uses the forbidden prediction or observational-f-sigma-8
names. No packaged observational anchor exists. Explicit exclusion strings in
docstrings/result caveats are metadata, not executable implementations.

## 23. Scientific limitations

This is an externally anchored conditional diagnostic. The Timescape
evolution does not predict the supplied anchor. A1–A6 are indispensable;
failure of scale independence or positivity invalidates this construction.
No sigma_8 integral is computed, no standard observational f sigma_8 is
computed, and no RSD interpretation is supplied.

Comoving is primary. Mészáros is comparison-only and formally inapplicable to
Timescape. Barotropic systems are rejected, and D3 does not enter the API or
implementation. Neither clean result supplies an observational spatial map,
galaxy bias, or survey estimator.

## 24. Exact files changed

New tracked candidates:

- `src/timescape_fsigma8/growth/anchored_diagnostic.py`;
- `tests/test_anchored_density_growth.py`;
- `scripts/validate_anchored_density_growth.py`;
- `reports/phase1d_d_anchored_density_growth_validation.md`.

Modified tracked candidate:

- `src/timescape_fsigma8/growth/__init__.py` (minimal exports and corrected
  explanatory D3/sigma8 scope docstring only; executable behaviour unchanged).

New generated, ignored artifact:

- `artifacts/independent/phase1d_d_anchored_density_growth_validation.json`.

No existing source module other than the permitted export file, existing
test, frozen report, artifact, notebook, upstream file, README, CLAUDE.md,
AGENTS.md, UPSTREAM.lock, or configuration file changed.

## 25. Readiness assessment

All construction, eligibility, algebraic, purity, serialization, convergence,
and full-suite gates pass. The implementation is ready for an independent
read-only compliance audit, subject to that audit’s findings. It remains
uncommitted and unstaged.

The result classification is
`CONDITIONAL_ANCHORED_DIAGNOSTIC_NOT_OBSERVATIONAL_PREDICTION`. The diagnostic
is not a Timescape sigma_8 prediction, not standard observational f sigma_8,
not an RSD observable, and not likelihood-ready. The synthetic 0.8 anchor is
validation-only. Mészáros remains comparison-only; barotropic systems and D3
remain outside this phase.
