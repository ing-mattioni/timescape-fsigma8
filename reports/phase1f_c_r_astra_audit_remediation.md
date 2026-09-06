# Phase 1F-C-R — Astra independent-audit remediation

This is a corrective checkpoint, not a new scientific realization. It preserves
`H1-1F-C-CLOCK-ANCHORED-SCALAR-NORMAL-KINEMATIC-GEOMETRY-V1` and the verdict
`PARTIAL_GEOMETRIC_CLOSURE_DERIVED_NEW_PERTURBED_GEOMETRIC_DYNAMICS_REQUIRED`.
The verdict denotes conditional local kinematics, not derived Timescape
gravitational dynamics. Phase 1F-D and observational development have not begun.

## Checkpoint and scope

The complete user-supplied `astra/INDEPENDENT_SCIENTIFIC_AUDIT.md` was read.
Its SHA-256 is `4b8f8b3959ddce4510054bd314b8af99fd80e5668e5adf51cec1629c56354518`.
The user explicitly authorized preserving this additional untracked file.
The audit checkpoint is `63d2104575c6a249e5177e47f4a354b660e70e32`, global
verdict `ACCEPT_WITH_TARGETED_CORRECTIONS`: zero load-bearing scientific errors,
six S2 corrections, one S3 classification correction, no hidden circularity,
and `D3_VERDICT: RESOLVED_DERIVED_4_10`.

Fetch confirmed `HEAD=main=origin/main` at that checkpoint before branching.
The tracked tree/index were clean. All 27 local phase tag objects and their
peeled commits were recorded unchanged. All remotely present tags matched;
the 1F-B v1/v2/v3 tags are local-only. The companion inventory records all
full object IDs, the two unchanged historical untracked audit hashes, and
the pinned upstream commit and notebook hash. The pre-existing inaccessible
`.pytest_cache` causes a Git status warning; tests run with cache disabled.
No test warning is suppressed.

Baseline: Python 3.14.3, 617 passed in 69.06 s; Python 3.11.9, 617 passed in
70.54 s. Both had zero failures/skips/xfails/warnings, with `-W error`,
`-B`, `PYTHONDONTWRITEBYTECODE=1`, and `-p no:cacheprovider`.

All earlier report/inventory contents remain historical checkpoint evidence.
This successor record and `scientific_status.CURRENT_SCIENTIFIC_STATUS` are
the current cross-phase interpretation. In particular, the old 1F-B/C
validation reports and inventories' BDE attribution, the 1C initial-condition
source attribution, and the old closure-completeness wording are superseded
below. Their historical text is not silently rewritten.

## Finding matrix

| Finding | Disposition and exact implementation locations | Classification / validation |
|---|---|---|
| A01 metric/measure | `transfer/continuum_geometry.py:RegionalGeometrySpec`, `ContinuumCarrierSpec`; `transfer/continuum_backend.py:_isotropic_tensor_density` | Metric-consistent LB remains `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`; inconsistent J/metric inputs are rejected. Mean-preserving regional/target adversaries, dimension/normalization and preassembly-tamper tests added. |
| A02 acceleration components | `components.py`; `phase1f_b/dynamics.py`, `phase1f_b/models.py`; `phase1f_c/models.py`, `phase1f_c/geometry.py`, `phase1f_c/__init__.py` | Generic acceleration remains `DERIVED_FROM_GENERIC_GR`; selected component realization is `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`. Nonunit scale, nontrivial metric, coordinate derivative and non-diagonal frame/norm tests. |
| A03 C validity | `phase1f_c/models.py:ScalarMetricTraceInitialData`, `ScalarMetricTraceDiagnostics`, `ScalarMetricTraceResult`; `phase1f_c/geometry.py:reconstruct_optional_scalar_metric_trace` | Formula remains conditional; invalid metric interpretations rejected. Initial +/-1, positivity boundary, amplitude limit, long-time exit and small analytic-integral/convergence tests. |
| A04 BDE attribution | `phase1f_b/dynamics.py`, `phase1f_b/models.py`, `phase1f_c/geometry.py`; source-metadata tests in `test_phase1f_b_dust_wall_boost_dynamics.py` and `test_phase1f_c_wall_common_geometry.py` | Exact old source attribution becomes `SOURCE_DOES_NOT_SUPPORT_CLAIM`; independently derived formulas retained. Citation metadata explicitly does not prove mathematics. Existing independent sign/clock/ADM tests preserved. |
| A05 Short–Coles | `perturbations/initial_conditions.py`; `test_perturbation_initial_conditions.py`; new independent-reference tests | Printed literal attribution becomes `SOURCE_DOES_NOT_SUPPORT_CLAIM`. Implemented growth solution remains conditional flat dust+Lambda; IC amplitude and transfer remain external. 18 independent quadratures plus early-time and dust limits. |
| A06 tolerance semantics | 25 existing test files; `scripts/audit_numerical_tolerances.py` | 309 existing comparisons now explicit. No equation reclassification; no exposed discrepancy. Full exact file list and tolerance categories are in the inventory. |
| A07 background embedding | `scientific_status.py`; transfer framework constants and regional function documentation; 1F-B/C closure documentation; package exports; manufactured-jet descriptions; README | Imported equations conditional, physical embedding and all-time compatibility `NOT_DERIVED`; naive W09 clock identification `REJECTED_UNSUPPORTED`. Current status regression tests prevent promotion. |

Source paths in this table are relative to `src/timescape_fsigma8/`; test
paths are relative to `tests/`. The inventory's `changed_files` lists every
modified/new path, including this report and its inventory. New independent
tests are in `tests/test_phase1f_c_r_astra_remediation.py`.

## A01: pointwise Riemannian contract

The structured backend's supported reference measure is **unit coordinate
density**, `dmu_0=d^d x`, with quadrature weights `prod(dx)`. Inspection of
all existing factories, fixtures and validation producers found this choice:
unit periodic boxes use weights `1/prod(grid_shape)` and spacing `1/n_i`.
RegionalMetricNormalization records integrated metric measure; it is not an
independent pointwise density multiplier.

In general, if `dmu_0=c_0 d^d x`, `g=Phi^* gamma`, and `M=g^-1`, then
`dmu_g=sqrt(det g)d^d x`, `J=sqrt(det g)/c_0`, and
`c_0 J sqrt(det M)=1`. This realization fixes `c_0=1` and now enforces both
that pointwise relation and the coordinate quadrature normalization. It
does not normalize either metric or J to make an inconsistent input pass.
Metric homogeneity scaling still gives `g -> c^2 g`, `J -> c^d J` and
`M -> c^-2 M`; the pre-existing three-volume dimensional firewall is retained.

The float64 metric relation uses `rtol=2e-12`, `atol=0`, implemented as
logarithmic bounds on `J/sqrt(det g)` to avoid product/determinant overflow.
The budget covers small-matrix determinant roundoff relative to the metric's
own scale. This is not an integrated-volume test. Constructor validation and
all three operator coefficient constructions recheck the relation; existing
post-assembly integrity checks protect subsequent use.

The independent adversary is `J=1+0.2 sin(2*pi*y/4)` with flat inverse metric
on a 4x4x4 carrier. It preserves total and each regional integrated volume
but fails pointwise. Wall, void and target variants are rejected. Conformal
factories satisfy the relation in dimensions 1, 2 and 3. Every actually
consumed accepted fixture passed; no accepted scientific fixture was changed.
The intentionally unsupported anisotropy test now uses diagonal inverse
entries `(0.5,2)` with determinant one, preserving J and integrated volume
while isolating its intended unequal-principal-values rejection.

Independent weighted diffusion requires a future, separately named abstraction;
it cannot enter through `RegionalGeometrySpec`. No blanket downstream
recomputation is indicated for validated metric-consistent inputs.

## A02: exact component ontology

The reference gradient supplied to 1F-C must explicitly return
`COORDINATE_COVECTOR` derivatives. A caller must supply a symmetric positive
inverse reference metric at every wall point; no identity-metric default is
inserted. Its positive-diagonal Cholesky factor fixes `gamma^-1=L L^T`.
This is the frame already used by 1F-B, now implemented in a shared typed
conversion helper. The physical frame is `e_hat^i=L^i_hat/a_W`.

For the generic normal acceleration identity, [BMR Eq. (2.6)](https://arxiv.org/pdf/1912.04213v2),
the first-order arrays are:

| Public array | Representation | Value |
|---|---|---|
| `wall_acceleration_coordinate_covector` | `COORDINATE_COVECTOR` | `partial_i nu_W` |
| `wall_acceleration_coordinate_contravariant` | `COORDINATE_CONTRAVARIANT` | `a_W^-2 gamma^ij partial_j nu_W` |
| `wall_acceleration_orthonormal` | `PHYSICAL_ORTHONORMAL` | `a_W^-1 (L^T partial nu_W)_hat` |

The result exposes a read-only representation mapping for these arrays.
The misleading old `wall_acceleration_covector` name is removed: callers
using the old physical array must migrate to `wall_acceleration_orthonormal`.
Flat-metric numbers are retained. Nontrivial-metric consumers now have enough
data to perform the conversion. This is an explicit API correction, not a
change to `A_a=D_a ln N`, its sign, units or first-order approximation.

The nontrivial coordinate test makes the passive change `x_new=3*x_old`,
`gamma_new=I/9`, `a_W=2`, and computes coordinate derivatives independently
by centered differences. It compares all three representations and leaves
the physical scalar Laplacian unchanged. A separately supplied non-diagonal
triangular frame checks the transpose convention and the metric norm.
Operator labels still cannot certify an opaque caller matrix's truth; this
limitation is explicit and does not excuse missing frame data.

## A03: optional metric validity

The selected first-order metric remains `h_ij=a_W^2(1+2C_W)gamma_ij`.
Strict necessary positivity, `1+2C_W>0`, is checked independently from
`abs(C_W)<=linear_regime_limit`. Both hold initially, at every accepted output
time, and on construction of a returned trace result.

There was no established C-specific amplitude bound. Following the existing
caller-declared lapse-policy pattern, optional initial data now require a
finite positive limit below one. The caller must choose a sufficiently small
limit for their first-order error budget; `<1` alone is not a universal
accuracy certification. Tests explicitly choose `0.05`. This is a numerical/
model-validity criterion, not a Timescape prediction. No such extra input is
required by driver-only geometry. No projection, clipping or renormalization
rescues invalid C fields.

Alternating +/-1 and the degenerate +/-0.5 boundary fail positivity. A smaller
but over-budget field fails the declared linear regime. A zero-lapse,
nonzero-initial-boost history remains a valid driver but accumulates C beyond
the bound over a long interval and is rejected. A quadratic time driver is
checked against its independent analytic integral on 9/17/33 time points;
errors decrease by a factor of four. The 33-point small case has
`max|C|=0.03661067708333335`, `min(1+2C)=0.9267786458333334`; its recurrence
residual is `1.11e-16`. The independent integral, not that same-update
residual, establishes integration accuracy. Gates concern accepted output
times; they do not certify unsampled continuous-time histories.

## A04: source support and retained derivation

The primary [BDE scan](https://articles.adsabs.harvard.edu/pdf/1992ApJ...395...34B),
journal p.38, was downloaded and visually inspected. Its SHA-256 matches the
audit: `eaa273fa5982689cd55eaba7530103e8e9d77199d4b34d3d173c1e9201075b6c`.
Eqs. (14)-(16) concern matter variables and energy/particle fluxes, not the
claimed expansion or acceleration transformations.

The retained derivation starts with the normalized boost, BMR Eq. (2.7),
`u_d=gamma_dW(u_W+v)`, `u_W.v=0`, `gamma_dW=1+O(v^2)`. Its divergence gives
`Theta_d-Theta_W=nabla_a v^a=D_a v^a+O(2)` about the assumed coincident,
unaccelerated background. In the scalar sector `v_a=D_a psi`, this fixes
the positive dust-minus-wall sign of `D_W^2 psi`.

Expanding `u_d^b nabla_b u_d,a` on the shared shear-free background gives
`A_d,a=A_W,a+dot(v)_<a>+H_proper v_a+O(2)`. Dust geodesicity sets it to zero.
The scalar commutator `dot(D_a psi)=D_a(dot psi)-H_proper D_a psi` cancels the
H term. BMR (2.6) then gives `D_a(dot psi+nu)=0`; the declared kernel
representative yields `dpsi/dtau_W=-Q0 nu`, and the common-time chain rule
gives `partial_t psi=-alpha_W Q0 nu`.

Generic boost, divergence and normal acceleration identities remain
`DERIVED_FROM_GENERIC_GR`. The selected scalar/shear-free/shared-background
wall application remains `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`.
No equation or numerical sign was changed. Existing behavioral checks remain;
source-string tests now describe their limited provenance role.

```text
BDE_14_16_PREVIOUS_ATTRIBUTION: SOURCE_DOES_NOT_SUPPORT_CLAIM
FORMULA_STATUS: INDEPENDENTLY_DERIVED_AND_RETAINED
```

## A05: qplus source discrepancy and independent verification

[Short & Coles v2](https://arxiv.org/pdf/astro-ph/0605013v2), p.7 Eqs. (11)-(12),
was downloaded and visually inspected; SHA-256
`d20f3436170ffbd2280370ccb51d8dda09eca85c68d3b67ae2bf0810696d3e18` matches the
audit. Its printed cube-root prefactor contains an additional `a^-1`; its
square root contains `a^-6` instead of `a^-3`; and its incomplete-beta argument
denominator uses `Omega_m+Omega_L*a^6` instead of `Omega_m+Omega_L*a^3`.
It also uses an initial-epoch normalization. Literal transcription would
not preserve the implementation or its growing-mode limit.

The code instead independently solves the paper's verified growth Eq. (3),
`D_ddot+2H D_dot-4piG rho_m D=0`, for the selected flat dust+Lambda IC model.
The decaying solution is proportional to `E(a)=sqrt(Omega_m/a^3+Omega_L)`.
Reduction of order gives
`D(a)=(5/2)Omega_m E(a) integral_0^a dx/[x^3 E(x)^3]`, with `D/a -> 1`.
The substitution `u=Omega_L*x^3/(Omega_m+Omega_L*x^3)` reduces the integral
to an incomplete beta with indices `(5/6,2/3)`, yielding exactly the existing
implemented prefactor `(5/6)(Omega_m/Omega_L)^(1/3)` and square-root factor
`sqrt(1+Omega_m/(Omega_L*a^3))`.

The independent reference uses quadrature after `x=a*s`, on the fixed unit
interval, to avoid an early-time absolute stopping floor. `quad` uses
`epsabs=2e-14`, `epsrel=2e-13`, `limit=200`; comparisons use `rtol=3e-12`,
`atol=0`. Tests span `a=0.001,0.01,1/21,0.25,0.5,1` and
`Omega_m=0.1,0.315,0.9`, with additional early-normalization and dust-limit
checks. On Python 3.14.3 the maximum relative difference across the 18
quadratures was `8.674e-16`. The Planck-recipe values at `a=1/21,0.5,1`
remain `0.047617014830694096`, `0.47800830502238284`, `0.7878126021855968`.
The qplus executable AST, finite-difference derivative recipe, rate conversion
and initial amplitudes are unchanged. Amplitude/transfer into Timescape
remain `EXTERNAL_CLOSURE_INPUT`.

```text
SHORT_COLES_LITERAL_ATTRIBUTION: SOURCE_DOES_NOT_SUPPORT_CLAIM
QPLUS_IMPLEMENTATION: INDEPENDENTLY_VERIFIED_CORRECT_FOR_SELECTED_FLAT_DUST_LAMBDA_IC_MODEL
```

## A06: explicit tolerances

The audit covered all test families, not only 1E-G through 1F-C. Of 347
pre-existing comparator calls, 309 needed explicit semantics across 25 files:
98 relative budgets gained `atol/abs=0`; 119 absolute budgets gained
`rtol/rel=0`; 90 previously implicit algebraic/scalar comparisons use
`rtol/rel=2e-12`, `atol/abs=1e-14`; one zero endpoint is exact; one adversarial
non-equality retains NumPy's former `rtol=1e-5`, `atol=1e-8` explicitly so its
separation requirement is not weakened. Existing explicit nonzero relative
and convergence tolerances were retained.

Absolute budgets apply in the fixture's stated coordinate/field units,
typically order-one H1 algebra and order-1e-3 boost/lapse amplitudes; the
relative budgets scale with the expected background/rate or reference value.
The new algebraic budget allows accumulated float64 roundoff while being much
tighter than the previous defaults. It is not an observational error budget.
No threshold was loosened to recover a passing test. The immediate complete
3.14.3 suite passed all 617 tests after tightening, exposing no new defect.
The AST checker resolves imported comparator aliases and makes both relative
and absolute semantics mandatory; exact equality has zero tolerance by definition.

## A07 and nonblocking clarifications

The former `COMPATIBLE_IMPORTED_DYNAMICS` live framework label now reads
`DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`. This qualifies imported equations;
it does not certify their physical embedding. In particular:

```text
REGIONAL_DUST_FLRW_EQUATIONS: DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION
REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING: NOT_DERIVED
NAIVE_W09_WALL_CLOCK_AS_REGIONAL_PROPER_DUST_FLRW_CLOCK: REJECTED_UNSUPPORTED
ZEROTH_ORDER_DUST_WALL_BACKGROUND_COINCIDENCE: REQUIRED_FOR_FIRST_ORDER_BOOST
ZEROTH_ORDER_DUST_WALL_BACKGROUND_COINCIDENCE_STATUS: NOT_DERIVED
ALL_TIME_TRANSFER_CONSTITUTIVE_COMPATIBILITY: NOT_DERIVED
MANUFACTURED_H1_TRAJECTORIES: ALGEBRAIC_VALIDATION_ONLY
PHYSICAL_TIMESCAPE_TRAJECTORY_EXISTENCE: NOT_DERIVED
```

The old H1 fixture's nontrivial target residual cancellation is retained as
algebraic evidence; its `rho_w'=0` with nonzero wall expansion violates regional
dust conservation. IDs do not establish compatible zeroth-order congruences.
The audit's rejection of the naive W09 common-time EdS/proper-time identification
is recorded, not solved here. No new dynamics or embedding is introduced.

The old lapse-plus-pullback-only irreducibility statement is withdrawn.
The current closure inventory includes all seven items in the README and
`REMAINING_SCIENTIFIC_CLOSURES`. A08 clarifies ranks 4/5/+1=6 as differential
field-species counts; prescribed expansion histories and kernel choices constrain
admissible initial functions. A09 corrects live D3 wording to
`RESOLVED_DERIVED_4_10` without removing its forensic branch. A13's finite-mode
versus unrestricted barotropic-continuum stability caveat is retained.
A10 exhaustive literature recertification is outside this checkpoint.

## Equations preserved and downstream impact

Tracker background, D1/D2 corrections, accepted D3 adjudication, clean
perturbation systems, ADM sign, boost sign and clock conversion, ranks and
observation firewalls are retained. Explicitly:

```text
D_W^2 psi_dw = deltaTheta_d,w - deltaTheta_W
partial_t psi_dw = -alpha_W Q0 nu_W
deltaTheta_W = (3/alpha_W)[partial_t C_W - H_W^(t) nu_W]
partial_t C_W = H_W^(t) nu_W + (alpha_W/3)[deltaTheta_d,w - D_W^2 psi_dw]
D_W^2 phi = a_W^-2 Delta_reference phi
```

The validator compares executable ASTs for background, clean systems,
barotropic matrices, ICs and regional equations, plus the load-bearing boost,
Laplacian, wall expansion and C evolution assignments against the exact base.
The new component conversion is checked independently as a representation
change. No physical equation, independent variable, normalization, sign,
initial value or accepted scientific realization was changed.

Invalid metric/measure inputs and invalid optional reconstructions now fail
closed. Valid existing factories, driver-only histories and scalar evolution
remain supported. Consumers must supply frame metadata and, for optional C,
an explicit validity limit, and migrate the renamed acceleration array.
No hidden predictive circularity or observational authorization is introduced.

## Validation and next-phase boundary

Final dual-stack targeted/full test results and deterministic validation are
recorded in the companion inventory. The read-only validation command is:

```text
python -B scripts/validate_phase1f_c_r_astra_remediation.py --producers
```

It checks pinned files, all frozen tags, untouched historical reports,
preserved equation ASTs, explicit comparator semantics, package imports and
AST parsing, every report JSON roundtrip, canonical inventory bytes, and
repeated in-memory generation of the affected 1F-A/B JSON outputs.
Both staged and unstaged diff checks must pass before the one local commit.

The next scientific phase is
`1F-D_BACKGROUND_EMBEDDING_AND_CONSTRAINT_CLOSURE_FEASIBILITY`; it is not begun.
Integration into main and any push remain a separate, explicitly audited task.

Final validation passed:

| Python | Targeted: every changed test module | Complete suite |
|---|---|---|
| 3.14.3 | 589 passed, 62.49 s | 650 passed, 69.06 s |
| 3.11.9 | 589 passed, 67.15 s | 650 passed, 67.59 s |

All four runs had zero failures, skips, xfails and warnings. The complete
suite adds 33 independent remediation cases to the 617-test baseline.
Warnings were errors; pytest caching and bytecode writes were disabled.
Both stacks passed all provenance, equation-preservation and AST checks,
46 package imports, 15 JSON roundtrips and repeated deterministic generation
of both affected numerical inventories. Their producer hashes agree across
stacks and are recorded in the companion inventory. The tolerance scanner
found 359 test, 11 source and 2 script comparisons, all explicit.
The exact changed-file inventory contains 50 paths. Unstaged and staged
whitespace checks passed. All 27 old tag objects/peeled commits, 52 historical
reports, the upstream pin, notebook and three preserved untracked audit
files remain unchanged. Main and origin/main remain at the audit checkpoint.

```text
PHASE: 1F-C-R
PURPOSE: ASTRA_INDEPENDENT_AUDIT_REMEDIATION
SCIENTIFIC_REALIZATION_CHANGED: NO
LOAD_BEARING_SCIENTIFIC_EQUATIONS_CHANGED: NO
ASTRA_LOAD_BEARING_SCIENTIFIC_ERRORS: 0
A01_METRIC_MEASURE_CONTRACT: CORRECTED
A02_ACCELERATION_COMPONENT_ONTOLOGY: CORRECTED
A03_OPTIONAL_METRIC_VALIDITY_DOMAIN: CORRECTED
A04_BDE_ATTRIBUTION: CORRECTED
A05_SHORT_COLES_ATTRIBUTION: CORRECTED
A06_NUMERICAL_TOLERANCE_SEMANTICS: EXPLICIT
A07_BACKGROUND_EMBEDDING_CLASSIFICATION: CORRECTED
REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING: NOT_DERIVED
ALL_TIME_TRANSFER_CONSTITUTIVE_COMPATIBILITY: NOT_DERIVED
UNIQUE_TIMESCAPE_PREDICTION: NOT_GRANTED
OBSERVATIONAL_AUTHORIZATION: NOT_GRANTED
FSIGMA8_AUTHORIZATION: NOT_GRANTED
NEXT_SCIENTIFIC_PHASE: 1F-D_BACKGROUND_EMBEDDING_AND_CONSTRAINT_CLOSURE_FEASIBILITY
INTEGRATION_READINESS: READY_FOR_INDEPENDENT_POST_REMEDIATION_AUDIT
```
