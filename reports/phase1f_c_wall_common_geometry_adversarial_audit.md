# Phase 1F-C — Independent adversarial audit

## 1. Executive audit verdict

```text
REQUIRES_TARGETED_CORRECTIONS
```

The selected scientific realization
`H1-1F-C-CLOCK-ANCHORED-SCALAR-NORMAL-KINEMATIC-GEOMETRY-V1` survives
adversarial scrutiny. Every load-bearing equation I re-derived independently
from ADM first principles agrees with the implementation, including all signs,
every factor of 3, the placement of `a_W^-2`, and the absence of a second
`alpha_W` on `H_W^(t)`. All firewalls (background `gamma_w`, generic-GR,
interface/morphology, observational, D3) hold.

One scientifically load-bearing defect remains, in the **contract layer** of
the blocking `a_W^2` item: the `H1ToWallSpatialPullback` docstring instructs
implementers to supply *already wall-physical* operators, which contradicts the
field names, the validated units tokens, the validated scale-factor relation,
and the code — all four of which require *reference/comoving* operators. The
runtime guard is a string comparison and cannot detect the difference, so a
caller following the docstring would silently obtain results wrong by a factor
`a_W^2`. Two further test-quality defects leave the `H_W^(t)` term of the
metric-trace equation without any effective coverage.

## 2. Independence statement

The Phase 1F-C validation report, inventory, and the prior completion message
were treated as claims under test. Every load-bearing equation was re-derived
from the ADM/generic-GR definitions and from the frozen Phase 1F-A/1F-B
implementation source, and each numerical claim was recomputed with
independently written code in an ignored scratch directory. Where the audit
brief supplied an expected value, I recomputed it rather than reading it.

No repository file was modified, staged, committed, or tagged. The only file
created is this report, left untracked.

## 3. Repository / provenance verification

All fifteen preflight items verified directly:

| # | Item | Expected | Observed |
|---|---|---|---|
| 1 | Branch | `phase-1f-c-perturbed-wall-common-spacetime-geometry` | identical |
| 2 | HEAD | `6a633903fe7355a9892ed61abefece5a7b6f2855` | identical |
| 3 | Parent | `d2f150222cb08565aa9d0822747250309d8aaa67` | identical |
| 4 | `main` | `d2f15022…` | identical |
| 5 | `origin/main` after fetch | `d2f15022…` | identical |
| 6 | Tag object / peel | `ef3b180e080e299f26316f9f5a30982776378e1e` / `6a633903…` | identical, annotated |
| 7 | Commits after the implementation commit | none | `git rev-list 6a63390..HEAD` = 0 |
| 8 | Index | empty | empty |
| 9 | Tracked worktree | clean | clean |
| 10 | Untracked files | only the authorized 1F-B v3 audit | exactly that one file |
| 11 | Its SHA-256 | `08c30893…16930` | identical |
| 12 | Pinned upstream | `590c6fd5332acb15…`, clean | identical, clean |
| 13 | Notebook SHA-256 | `86d2534d…de55a` | identical |
| 14 | Frozen 1F-B tags v1–v3 | unchanged | `d7840740…`→`27fd65fd…`, `bd1facf1…`→`16440e1a…`, `61dc9cf7…`→`d2f15022…` |
| 15 | `git diff --check` | clean | clean (and `--cached`) |

History is linear with no merge commit (`main..HEAD` = 1 commit, 0 merges).
The commit touches exactly six new Phase 1F-C files and nothing else, so no
frozen scientific source, report, or inventory was modified.

Baseline suites before the audit: **614 passed** on Python 3.14.3 and **614
passed** on Python 3.11.9, zero failures, skips, xfails, warnings (`-rsxX`, no
suppression). Targeted Phase 1F-C: **26 passed**.

## 4. Files audited

Read completely: `src/timescape_fsigma8/phase1f_c/models.py` (1002 lines),
`geometry.py` (301), `__init__.py` (74),
`tests/test_phase1f_c_wall_common_geometry.py` (586),
`reports/phase1f_c_wall_common_geometry_validation.md`,
`reports/phase1f_c_wall_common_geometry_inventory.json`.

Frozen dependencies established from the import graph rather than from the
report: Phase 1F-C imports **only** `phase1f_a.models`
(`RegionalDomainSpec`, `canonical_state`) and `phase1f_b`
(`ScalarDustWallBoostResult`). It imports **nothing** from
`timescape_fsigma8.background`, so the frozen tracker `gamma_w` cannot enter
numerically. Scientific dependencies actually relied on: the frozen 1F-B
`wall_proper_time_rate`, `wall_lapse_perturbation`, `wall_scale_factor`,
`wall_hubble_rate`, `wall_expansion_perturbation`, `scalar_potential`,
`scalar_potential_time_derivative`, the 1F-A `RegionalExpansionReconstruction`
`delta_theta`, and the sealed H1 `RegionalDomainSpec`.

## 5. Primary-source verification

`gamma_w` is **not** imported: it is a caller-supplied array
(`TimescapeWallClockBridge.timescape_background_lapse`) validated as finite and
positive. The relation `alpha_W = 1/gamma_w` is computed only inside the
`background_wall_proper_time_rate` property, gated behind the explicit branch
enum.

## 6. Clock audit

| Sub-item | Finding |
|---|---|
| A. Identification explicit | `ClockMapBranch` is a single-member enum that must be passed; `common_time_coordinate_id != timescape_time_coordinate_id` raises "selected branch requires t_common=t_Timescape"; `background_wall_proper_time_id != timescape_wall_proper_time_id` raises "selected branch requires bar(tau_W)=tau_w". |
| B. Missing/incorrect branch rejected | non-enum branch, mismatched ids, and a classification other than `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` all raise `Phase1FCClockError`. |
| C. `nu_W` never from `gamma_w` | the bridge record carries no lapse-perturbation field; `nu_W` arrives only through `ExternalWallLapsePerturbationClosure`; I probed `lapse_closure=None` → `Phase1FCLapseClosureError`. |
| D. `alpha_W` vs `gamma_dW` | the inventory records `relative_lorentz_factor = gamma_dW = -u_d,w.u_W = 1+O(v^2)` and `objects_identified: false`; no code path uses a Lorentz factor. |
| E. Positivity/finiteness | `gamma_w <= 0` or non-finite raises; time grid must be strictly increasing. |
| F. Conditional provenance | classification pinned to `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`, never `DERIVED_FROM_FROZEN_TIMESCAPE`. |

Hidden-path search for `nu_W = delta gamma_w`, `-delta gamma_w`, or `0`: none
exists. There is no zero/default lapse provider in `__all__`, every scenario
constructor parameter is mandatory, and a `nu_W` that differs from the lapse
that drove Phase 1F-B is rejected (`lapse_alignment` gate). A clock whose
`alpha_W` differs from the frozen 1F-B `wall_proper_time_rate` is rejected
(`clock_alignment` gate). **No blocking clock path found.**

**Status: `PASS`. Provenance: `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`.**

## 7. ADM lapse audit

Independent derivation. With `dtau_local/dt = N_W = bar(alpha_W)(1+nu_W)` and
the frozen wall-proper-time law `dpsi/dtau_W = -Q_0 nu_W` (whose `tau_W` is the
*background* wall proper time, per frozen 1F-B v3), the chain rule gives
`partial_t psi = bar(alpha_W) dpsi/dtau_W = -bar(alpha_W) Q_0 nu_W` exactly.
Had the *local* proper time been used, `partial_t psi = -bar(alpha_W)(1+nu_W)
Q_0 nu_W = -bar(alpha_W) Q_0 nu_W + O(2)` — the same first-order result. The
implementation applies exactly one `alpha_W` and no additional first-order
factor.

Verified numerically: `adm_lapse_first_order` equals
`alpha[:,None]*(1+nu)` to `0.0`; positivity is gated.

**Boost-clock residual independence.** The residual
`potential_dot + alpha * Q_0 nu` compares the frozen 1F-B output
(`scalar_potential_time_derivative`, produced by 1F-B's own `Q_0` with its
regional mass weights) against a projection recomputed in 1F-C with the
pullback's `wall_measure_weights`. These are two separately specified measures,
so the check is not a same-helper comparison. Measured `2.710505431213761e-20`
(unit clock) — I reproduced this exactly with my own projection — and the
report's `5.421010862427522e-20` for the time-dependent non-unit clock. It has
real power: omitting `alpha_W` on the 1F-C side would leave `(1-alpha)Q_0 nu`,
nonzero whenever `alpha != 1`, and the non-unit-clock test exercises that.

*Explicit condition:* in the shipped fixture both measures are uniform over the
same 32 cells, so the two `Q_0` projections coincide; the gate therefore does
not currently discriminate *measure conventions*, only the `alpha_W` factor.

**Status: `PASS_WITH_EXPLICIT_CONDITIONS`. Provenance: `DERIVED_FROM_GENERIC_GR`
(chain rule) applied to a `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` clock.**

## 8. ADM sign and wall-expansion derivation

Independent derivation, signature `(-,+,+,+)`, `K_ij = -(1/2)L_n h_ij`, zero
shift so `K_ij = -(1/(2N)) partial_t h_ij`, and `Theta = -K` for the
hypersurface-normal congruence.

For `ds^2 = -alpha_W^2(1+2nu_W)dt^2 + a_W^2(1+2C_W) gamma_ij dx^i dx^j`:

```
N        = alpha_W(1+nu_W) + O(2)
h_ij     = a_W^2 (1+2C_W) gamma_ij
h^ij d_t h_ij = 6 (H_W^(t) + d_t C_W) + O(2),   H_W^(t) = d_t a_W / a_W
K        = -(1/(2N)) h^ij d_t h_ij = -3 (H_W^(t) + d_t C_W) / N
Theta_W  = -K = 3 (H_W^(t) + d_t C_W) / [alpha_W (1+nu_W)]
         = (3/alpha_W) [H_W^(t) + d_t C_W - H_W^(t) nu_W] + O(2)
```

Hence

```
bar(Theta_W)   = 3 H_W^(t) / alpha_W                        (background)
deltaTheta_W   = (3/alpha_W) [ d_t C_W - H_W^(t) nu_W ]      (perturbation)
```

Every sign, every factor of 3, and every `alpha_W` matches the implementation,
and `H_W^(t)` appears with **no** extra `alpha_W`. Inverting gives
`d_t C_W = H_W^(t) nu_W + (alpha_W/3) deltaTheta_W`, which is exactly
`geometry.py:243-248`.

Independent numerical confirmation on a configuration I built with `H = 0.05`,
`a_W = exp(0.05 t)`, `alpha_W(t) = 1+0.2t`:
`max| (3/alpha_W)(d_t C_W - H nu) - deltaTheta_W | = 2.78e-17`.

**Status: `PASS`. Provenance: `DERIVED_FROM_GENERIC_GR`.**

## 9. Boost-sign audit

The frozen Phase 1F-B sign is `D_W^2 psi_dw = deltaTheta_d,w - deltaTheta_W`,
so `deltaTheta_W = deltaTheta_d,w - D_W^2 psi_dw`. `geometry.py:124` implements
`wall_expansion = dust - laplacian` ✓, and the residual at line 126 checks the
derived field against the frozen supplied `wall_expansion_perturbation`.

Independent counterexample (not the repository regression test): I formed
`deltaTheta_W^rev = deltaTheta_d + D^2 psi` — the opposite sign — from the
frozen 1F-B fields and fed it through. The gate fires with
`Phase1FCCompatibilityError: derived deltaTheta_W is incompatible with the
frozen Phase 1F-B geometry`, because the residual becomes `2 D^2 psi` (order
`0.1`) against a `5e-10` tolerance. The repository's own
`test_opposite_expansion_sign_fails_closed` reaches the same gate and is not
intercepted earlier (the lapse-alignment and clock gates pass unchanged).

Measured compatibility residual `6.938893903907228e-17`, normalized
`5.064886061246151e-16` — both reproduce the report exactly.

**Status: `PASS`. Provenance: `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`
(inherits the external pullback).**

## 10. Laplace–Beltrami / `a_W` scaling audit (blocking item)

**Independent derivation.** For `h_ij = a_W^2 gamma_ij` with spatially
homogeneous `a_W`, `sqrt(h) = a_W^3 sqrt(gamma)` and `h^ij = a_W^-2 gamma^ij`,
so `D_W^2 phi = (1/sqrt(h)) d_i (sqrt(h) h^ij d_j phi) = a_W^-2
Delta_gamma phi`. Likewise `D_W,i = a_W^-1 D_gamma,i` in orthonormal
components. This is exactly the declared `scale_factor_relation`.

**What the code does.** `geometry.py:116-120` computes
`psi @ L_ref.T / a_W^2`; `geometry.py:137-142` computes
`einsum(G_ref, nu) / a_W`. So the supplied operators are treated as
**reference/comoving** and 1F-C applies the scale powers itself.

**Which convention the fixture supplies.** I verified independently: applying
the supplied operator to a pure mode gives eigenvalue `-32.000000` at
`a_W = 1, 2, 3` alike, matching the analytic reference stencil value
`-4 sin^2(pi/N)/h^2` with the *reference* spacing. The operator is comoving,
independent of `a_W` ✓.

**Independent reproduction.** Against my own dense periodic 3-point Laplacian
divided by `a_W^2` (never the production helper):

| `a_W` | `max｜production D_W^2 psi − my independent physical Laplacian｜` | `｜D_W^2 psi｜max` |
|---|---|---|
| 1.0 | `6.94e-17` | `0.112000` |
| 2.0 | `1.74e-17` | `0.028000` |

`a_W = 2` scaling residual is machine zero ✓ (report claims "exactly zero").
Omitted-`a_W^-2` adversary: production-side
`max｜reference_laplacian − D_W^2 psi｜ = 0.08400000000000006`, **bit-identical
as a double** to the reported `0.08400000000000006` (it equals
`(1 − 1/4)·max｜reference｜`). Gradient: production/reference = `0.5` at
`a_W = 2` ✓.

Measure: `wall_measure_weights` is used for the `Q_0` projection and the `C_W`
split. Since `a_W` is spatially homogeneous, an `a_W^3` factor cancels
identically from every weighted **mean**, so the measure convention cannot
affect any implemented quantity. Consistent.

`a_W`/`H_W` mutual consistency: both are read from the frozen 1F-B closure,
where `H_W = d ln a_W/dt` is enforced on the common-time grid by the frozen
1F-B rate gate. Consistent.

**FINDING F-1 (`PARTIAL`).** The API contract is self-contradictory about which
convention the caller must supply:

- `models.py:259-266` (docstring): *"construction must provide the **already
  wall-physical** gradient and Laplace–Beltrami operators."*
- against: field names `wall_reference_gradient_operators`,
  `wall_reference_laplace_beltrami_operator`; validated tokens
  `gradient_units == "INVERSE_REFERENCE_WALL_LENGTH"`,
  `laplacian_units == "INVERSE_REFERENCE_WALL_LENGTH_SQUARED"`; validated
  `scale_factor_relation == "D_W=a_W^-1 D_gamma_W; D_W^2=a_W^-2
  Delta_gamma_W"`; and `geometry.py`, which divides by `a_W^2` and `a_W`.

Four signals say reference/comoving; the docstring says physical. A caller
obeying the docstring supplies `D_W^2` and the runtime divides by `a_W^2`
again, so `deltaTheta_W`, `C_W` and every downstream quantity are wrong by
`a_W^2` whenever `a_W != 1` — silently. **Demonstrated:** the guards are pure
string comparisons; I constructed a pullback carrying an already-physical
operator (`L/4` for `a_W = 2`) while typing the required reference token and
the contract **accepted it**. Nothing in the runtime inspects the operator's
actual scaling.

This is the "API contract could cause the factor to be applied twice" case the
brief designates blocking-priority. The audited *runtime* is numerically
correct, so this is `PARTIAL` (contract/documentation defect with a
demonstrated silent double-scaling hazard), not `INCORRECT`.

**Status: `OPERATOR_IDENTITY` `PASS` · `DIMENSIONAL_CONSISTENCY` `PASS` ·
`SCALE_FACTOR_PLACEMENT` `PASS` · `VALIDATION_INDEPENDENCE` `PARTIAL`
(contract).**

## 11. Spatial-pullback / ontology audit

All nine required distinctions are kept as separate, individually validated
fields (`h1_geometry_id` vs `wall_geometry_id`, `morphology_id`, `domain_id`,
`boundary_realization_id`, gradient operators, Laplacian operator,
`wall_measure_id`, `wall_scale_factor_mapping_id`, `wall_hubble_mapping_id`).

1. **No identity pullback default** — every constructor parameter is mandatory;
   an identity matrix fails the shape contract (`Phase1FCSpatialClosureError`).
2. **No H1 Laplacian aliased to `D_W^2`** — the fixture builds an *unbroken
   periodic* operator on a `(2,4,4)` wall grid, structurally different from the
   H1 broken regional stiffness; the test asserts the shapes differ, and I
   confirmed the H1 operator is never read in `geometry.py`.
3. **Morphology is not geometric dynamics** — `morphology_classification` must
   equal `EXTERNAL_CLOSURE_INPUT` and the id must match the sealed H1
   morphology.
4. **No H1 transmission BC becomes an Israel junction** — no junction,
   continuity or flux code exists; the report states the exclusion explicitly.
5. **No radial-null promotion** — no null/light-cone construct appears.

Direct attacks on the public constructor, all fail closed:

| Attack | Result |
|---|---|
| identity pullback (wrong shape) | `pullback matrix shape mismatch` |
| Laplacian not annihilating constants | rejected |
| non-self-adjoint Laplacian | `not self-adjoint in the declared measure` |
| degenerate (2-D kernel) Laplacian | `must have exactly one scalar constant kernel` |
| gradient not annihilating constants | rejected |
| pullback reading outside the H1 wall region | `consumes values outside H1 wall region` |
| wrong `scale_factor_relation` token | rejected |
| physical-length units token | rejected |
| scale mapping demoted from external closure | rejected |
| dimension/grid-rank mismatch | rejected |

The operator contract additionally checks coercivity off the constant kernel.
The single gap is F-1: the convention guards are string-level only.

**Status: `PASS_WITH_EXPLICIT_CONDITIONS`. Provenance: `EXTERNAL_CLOSURE_INPUT`.**

## 12. External `nu_W` closure audit

`nu_W` is irreducibly external. `ExternalWallLapsePerturbationClosure` is a
mandatory scenario field with `scientific_classification` pinned to
`EXTERNAL_CLOSURE_INPUT`; `None` raises `Phase1FCLapseClosureError`. There is
no zero-lapse class, no default, and no public name suggesting one
(`__all__` contains no `zero`/`default` entry). A `nu_W` that did not drive the
frozen 1F-B run is rejected by the lapse-alignment gate. Validation closures
carry `LapseClosureProvenance.SYNTHETIC_VALIDATION_ONLY`, which is a distinct
enum member from `EXTERNAL_GEOMETRIC_CLOSURE` and cannot be selected by
omission.

Keyword scan across the Phase 1F-C source: `gamma_w` appears 9 times, all in
docstrings, an error message, and provenance tokens — never as a numerical
input to `nu_W`. `CMC`, `Hamiltonian`, `momentum`, `Raychaudhuri`, `constraint`
appear **0 times** in source. `Einstein` appears twice, both disclaimers
("does not solve a perturbed Einstein system"; "not a perturbed Timescape
Einstein closure").

**Status: `PASS`. Provenance: `EXTERNAL_CLOSURE_INPUT`.**

## 13. Acceleration audit

For a hypersurface-normal congruence, `A_i = D_i ln N_W`; with `N_W =
alpha_W(1+nu_W)` and spatially homogeneous `alpha_W`, `A_i = D_i nu_W + O(2)`.
The implementation computes `einsum(G_ref, nu)/a_W`, i.e. `D_W,i nu_W` under
the declared `D_W = a_W^-1 D_gamma_W` convention ✓.

Verified: a spatially homogeneous lapse gives exactly `0.0` acceleration;
`a_W = 2` gives production/reference `= 0.5` ✓; the fixture maximum is `0.004`,
matching the report. Zero acceleration is never a default — it arises only from
a homogeneous supplied `nu_W`.

*Non-blocking naming note:* the field is `wall_acceleration_covector`, but the
returned value carries `1/a_W`, so it is the **physical/orthonormal**
component, not the coordinate covector `partial_i nu` (which carries no metric
factor). This is internally consistent with the declared `D_W` convention and
with the frozen 1F-B orthonormal velocity representation, but the name is
loose.

**Status: `PASS_WITH_EXPLICIT_CONDITIONS`. Provenance: `DERIVED_FROM_GENERIC_GR`.**

## 14. Metric-trace audit

Independently derived (§8): `d_t C_W = H_W^(t) nu_W + (alpha_W/3)
[deltaTheta_d,w - D_W^2 psi_dw]`, which is what `geometry.py:243-248` computes
since `wall_expansion_perturbation = deltaTheta_d - D_W^2 psi`.

Reconstruction is genuinely optional (a separate public function, never called
by the driver path); requires explicit `ScalarMetricTraceInitialData`; requires
an explicit `MetricTraceBackgroundSplit`; does not default `C_W` to zero (I
supplied zeros explicitly, and a nonzero-mean initial field is rejected); does
not feed back into Phase 1F-B (the frozen `wall_scale_factor` is unchanged
after reconstruction, verified by array equality); and integrates on the
declared common-time grid with the declared trapezoidal method.

Independent reproduction: my own trapezoid reproduces `C_W` to `0.0`; the
reported update residual `1.3877787807814457e-17` and mean drift
`8.673617379884035e-19` are consistent with the measured
`3.26e-16` evolution residual on my finer 101-point grid.

**FINDING F-2 (`PARTIAL`, test quality).** The `H_W^(t) nu_W` term is **never
exercised**: `make_case` in the Phase 1F-C test module hard-codes
`hubble = np.zeros(time.size)`, so `wall_hubble_rate = [0,0,0,0,0]` in every
fixture and that term is identically zero. I confirmed that with the shipped
fixtures the correct form and a double-`alpha_W` form
(`alpha_W H nu + alpha_W deltaTheta/3`) are **numerically identical**
(difference `0.0`), so no test can distinguish them.

I therefore built the discriminating configuration myself (`H = 0.05`,
`a_W = exp(0.05t)`, `alpha_W(t) = 1+0.2t`, 101 points):

- production vs **correct** form: `0.0`
- production vs **double-alpha** form: `7.500000000000562e-06`

so the **implementation is correct**; only the coverage is missing.

**FINDING F-3 (`PARTIAL`, test quality).** The nominal guard,
`test_phase1f_b_clock_chain_rule_and_no_second_hubble_factor`
(tests:275-281), asserts only two source substrings. I demonstrated that a
double-`alpha_W` edit of the production source still contains
`"hubble_common[:, np.newaxis] * geometry.perturbative_wall_lapse"` and still
lacks `"alpha_W * hubble"`, so **both assertions pass with the defect
present**. The guard is vacuous for the property it names.

**Status: `PARTIAL`. Provenance: `DERIVED_FROM_GENERIC_GR` (equation);
implementation correct, coverage absent.**

## 15. Zero-mode audit

The policy `EXPLICIT_WEIGHTED_MEAN_ZERO_PERTURBATION` requires (i) the initial
`C_W` to be weighted-mean-zero, (ii) the *derivative* to be weighted-mean-zero,
(iii) the reconstructed trace to remain so.

This is perturbative bookkeeping, not a physical condition:

- It does **not** impose CMC. CMC would force `deltaTheta_W = 0` pointwise;
  here `deltaTheta_W` is nonzero and spatially varying, and only its weighted
  mean is constrained. Measured `<deltaTheta_W>` is `2e-18`–`5e-18`, and I
  proved analytically that `<D_W^2 psi> = 0` follows automatically from
  self-adjointness in the declared measure plus the constant kernel, so the
  mean condition is not an extra physical demand on the Laplacian sector.
- It does **not** change the background `a_W` — verified by array equality
  before and after reconstruction. A split-violating input fails closed instead
  of being silently renormalized into the background.
- With `H != 0` condition (ii) reduces to `<nu_W> = 0`; that is the correct
  requirement for the declared split (a mean lapse with nonzero `H` would drive
  a mean `C_W`, i.e. a background redefinition), and it fails closed.
- It is not converted into a Timescape prediction anywhere; the classification
  is `EXTERNAL_CLOSURE_INPUT` for the initial data and
  `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` for the result.

**Status: `PASS`. Provenance: `GAUGE_CHOICE` / background-split bookkeeping.**

## 16. Congruence / shear / vorticity audit

| Object | Required | Implementation | Verdict |
|---|---|---|---|
| `u_W = n` | `MODEL_SECTOR_RESTRICTION` | `wall_congruence_classification` must equal `MODEL_SECTOR_RESTRICTION`; JSON `wall_normal_relation.classification` identical | ✓ |
| zero shift | `GAUGE_CHOICE` | `shift_classification` must equal `GAUGE_CHOICE`; `ShiftGauge` single member | ✓ |
| `omega_W = 0` | `DERIVED_FROM_GENERIC_GR` after normality | `vorticity_classification` must equal `DERIVED_FROM_GENERIC_GR`; token `ZERO_IN_SELECTED_NORMAL_BRANCH` | ✓ |
| `sigma_W = 0` | `MODEL_SECTOR_RESTRICTION` | `shear_classification` must equal `MODEL_SECTOR_RESTRICTION`; token `ZERO_BY_MODEL_SECTOR_RESTRICTION` | ✓ |

Scientifically correct: with the selected conformally isotropic spatial ansatz
`h_ij = a_W^2(1+2C_W) gamma_ij` and zero shift, `sigma_ij` vanishes identically
— a consequence of the chosen metric sector, **not** of hypersurface normality
(which yields only `omega = 0` by Frobenius). No file claims shear-freedom
follows from Timescape or from normality. Searched source, report, JSON and
tests: no such claim.

**Status: `PASS`.**

## 17. State-rank audit

Independent accounting of what is actually integrated:

| Quantity | Character |
|---|---|
| frozen regional `(Delta_w, Z_w, Delta_v, Z_v)` | 4, inherited |
| frozen `psi_dw` | 1, integrated by 1F-B |
| `alpha_W(t)`, `nu_W(t,x)` | supplied arrays, no internal evolution |
| pullback operators, measure | static matrices |
| `N_W`, `A_W`, `deltaTheta_W`, `D_W^2 psi` | algebraic/operator outputs |
| gauge labels, provenance records | static |
| optional `C_W` | 1, integrated only in the optional function |

`derive_clock_anchored_wall_kinematic_geometry` contains **no** time-stepping
loop (verified by source inspection); `reconstruct_optional_scalar_metric_trace`
contains exactly one. Nothing labelled "external" evolves internally: every
external object is a validated frozen array or matrix.

Therefore driver-only rank = 5 (unchanged from frozen 1F-B), optional
contribution = 1, augmented = 6. The frozen rank-five statement is preserved
and re-validated at construction (`frozen_phase1f_b_rank`, `driver_only_rank`
raise if changed).

**Status: `PASS`.**

## 18. Conditional-uniqueness audit

Given (a) the frozen 1F-B result, (b) the external `nu_W`, (c) the explicit
pullback/operators, (d) morphology/domain/boundary ids, (e) the clock branch
and `gamma_w`, (f) optional `C_W` initial data, (g) the zero-mode convention —
the forward problem is algebraically determined: `alpha_W` is fixed by (e),
`N_W` and `A_W` are algebraic in `nu_W`, `deltaTheta_W` is fixed by the frozen
compatibility relation, and `C_W` is a single quadrature. I found no remaining
free choice: every enum in the scenario has exactly one admissible member, and
all tolerances are numerical gates that cannot select a branch.

`CONDITIONAL_FORWARD_UNIQUENESS: GRANTED` is therefore justified — but only in
the conditional sense. It is rigorously distinct from
`UNIQUE_TIMESCAPE_PREDICTION`, which remains `NOT_GRANTED`: items (b) and (c)
are irreducibly external, recorded as
`IRREDUCIBLE_GEOMETRIC_INPUT = PERTURBED_WALL_CONGRUENCE_LAPSE_PLUS_SPATIAL_PULLBACK`.

**Status: `PASS`.**

## 19. Generic-GR firewall audit

No Hamiltonian constraint, momentum constraint, Einstein equation,
Raychaudhuri lapse closure, CMC condition, regional dust momentum source, or
`G_ab = 8 pi G T_ab` relation appears anywhere in the Phase 1F-C source (0
occurrences of each keyword). The only implemented relations are kinematic
identities: the ADM lapse split, `A_i = D_i ln N`, `Theta = -K`, the frame
expansion law, and the chain rule. The JSON records
`hamiltonian_as_lapse_closure`, `momentum_as_lapse_closure`,
`raychaudhuri_as_lapse_closure`, `cmc_default` all as `REJECTED_UNSUPPORTED`
and `local_einstein_dressed_source: NOT_DERIVED`, consistent with the code.

**Status: `PASS`.**

## 20. Interface / morphology firewall audit

No claim that `Gamma` is finite infinity, a material wall, an Israel junction,
a no-penetration boundary, or a flux/velocity-continuity surface. Morphology
enters only as `morphology_id` bound to the sealed H1 morphology with
`morphology_classification = EXTERNAL_CLOSURE_INPUT`. The validation report
states explicitly that "no H1 transmission condition becomes a gravitational
junction". `PHYSICAL_INTERFACE_CLAIM` is pinned to `NOT_GRANTED` in code,
report and JSON.

**Status: `PASS`.**

## 21. Observational and D3 firewall audit

The commit adds six files and changes nothing else, so D3 and Candidate A are
untouched by construction. Verified live: `D3Branch` still exposes
`printed_4_15` and `derived_4_10`, `barotropic_matrix(branch=...)` still has no
default, and `RESOLVED_DERIVED_4_10` remains the frozen verdict in the earlier
inventories.

No tracer, galaxy, RSD, Kaiser, observational `k`, power spectrum, transfer
function, `sigma_R`, `sigma8`, `fsigma8`, AP, dataset, covariance, likelihood
or fitting construct exists in the Phase 1F-C source or tests. The only matches
are the `*_AUTHORIZATION = NOT_GRANTED` constants and prohibition prose.

**Status: `PASS`.**

## 22. Test-quality audit

23 test functions / 26 collected cases. Mapping and independence:

| Test (line) | Protects | Class |
|---|---|---|
| clock bridge reciprocal, no lapse inference (221) | §5 A/C | INDEPENDENT |
| non-positive / non-finite `gamma_w` (235) | §5 E | INDEPENDENT |
| branch + identifications required (243) | §5 A/B | INDEPENDENT |
| first-order ADM lapse, no hidden zero provider (251) | §6 | INDEPENDENT |
| validation lapse external/synthetic-only (267) | §11 | INDEPENDENT |
| clock chain rule / no second Hubble factor (275) | §6, §13 | **CONSTRUCTION/VACUOUS — see F-3** |
| non-unit clock load-bearing (283) | §5, §6 | INDEPENDENT (analytic `alpha` fixture) |
| pullback has no default / no H1 alias (296) | §10 | INDEPENDENT |
| reference→physical scale powers (313) | §9 | PARTIAL (shares the operator; tests the factor only) |
| acceleration = wall gradient (340) | §12 | INDEPENDENT |
| homogeneous lapse ⇒ zero acceleration (352) | §12 | INDEPENDENT |
| expansion sign and dust distinction (371) | §8 | INDEPENDENT |
| opposite sign fails closed (391) | §8 | INDEPENDENT (reaches the intended gate) |
| compatibility has no clock factor (413) | §6 | **VACUOUS numerically — see F-4** |
| metric trace requires explicit data/split (427) | §13, §14 | INDEPENDENT |
| optional metric trace equations and rank (447) | §13, §16 | PARTIAL (H term identically zero) |
| sector/gauge/vorticity/shear/rank (477) | §15, §16 | INDEPENDENT (contract) |
| unsupported sector rejected (489) | §15 | INDEPENDENT |
| clock/lapse/spatial/frame mismatches (500) | §10, §11 | INDEPENDENT |
| immutability and array tamper (519) | integrity | INDEPENDENT |
| no predictive GR / observational API (536) | §18, §20 | INDEPENDENT (name scan) |
| realization ceiling exact (555) | §16 | INDEPENDENT |
| every equation carries a reference (566) | §24 | PARTIAL (presence, not correctness) |

**FINDING F-4 (`PARTIAL`, test quality).**
`test_compatibility_constraint_contains_no_clock_factor` (413-425) computes
`expected = laplacian − wall_expansion − laplacian` and then asserts only
`expected.shape == result.wall_expansion_perturbation.shape` — a trivially true
statement about shapes. The comment claims it "algebraically isolates that the
result relation has no alpha_W factor", but the computed array is never
compared to anything; the only operative assertion is a source-string grep.
I verified the property independently instead, by varying `alpha_W` over
`1`, `1+0.2t`, `2` and confirming the compatibility residual stays at
`5.6e-17`–`6.9e-17` while `deltaTheta_W` changes — i.e. the relation genuinely
carries no clock factor.

No test was found that passes vacuously *before reaching* its target code; the
adversarial tests all reach their intended gates.

**Status: `PARTIAL`.**

## 23. Independent numerical reproduction

All computed with independently written code; inputs are the shipped fixture
unless stated.

| Quantity | Reported | Independently obtained |
|---|---|---|
| clock alignment | `0.0` | `0.0` |
| lapse alignment | `0.0` | `0.0` |
| boost-clock residual (unit clock) | `2.710505431213761e-20` | `2.710505431213761e-20` (my own `Q_0` projection) |
| boost-clock residual (non-unit clock) | `5.421010862427522e-20` | consistent |
| expansion compatibility | `6.938893903907228e-17` | `6.938893903907228e-17` |
| normalized L-infinity | `5.064886061246151e-16` | `5.064886061246151e-16` |
| acceleration max | `0.004` | `0.004` |
| homogeneous-lapse acceleration | zero | exactly `0.0` |
| ADM lapse `N = alpha(1+nu)` | — | reproduced to `0.0` |
| `a_W = 2` scaling residual | "exactly zero" | `1.74e-17` vs my independent physical Laplacian |
| omitted-`a_W^-2` adversary | `0.08400000000000006` | `0.08400000000000006` (bit-identical double) |
| metric-trace update residual | `1.3877787807814457e-17` | reproduced (`3.26e-16` on my 101-point grid) |
| metric-trace mean drift | `8.673617379884035e-19` | consistent |
| `C_W` trapezoid | — | reproduced to `0.0` |
| ADM inversion `(3/alpha)(Cdot − H nu) − deltaTheta_W` | — | `2.78e-17` (new) |
| correct vs double-`alpha` metric trace (`H≠0, alpha≠1`) | — | `7.500000000000562e-06` (new) |

Equations used for the independent side are those derived in §7, §8 and §10 of
this report; input numbers are the fixture's `alpha_W ∈ {1, 1+0.2t, 2}`,
`a_W ∈ {1,2,3}`, `H ∈ {0, 0.05}`, lapse amplitude `-0.001 + 0.0004 t`, and
initial potential amplitude `0.002`.

**No material numerical difference was found.** The one apparent discrepancy —
my first pass produced `0.084000000000000005` for the adversary — resolved on
inspection: that value compares against *my* Laplacian, whereas the reported
figure is the production-side `max|reference − D_W^2 psi|`; computing the
production-side quantity gives `0.08400000000000006` exactly.

## 24. Report / JSON consistency

The inventory is valid JSON with 21 top-level keys and parses deterministically
(SHA-256 `5b9a95f36462aa64…`). Every verdict token in
`required_machine_verdict` matches the corresponding module constant in
`models.py` and the Markdown final block: I cross-checked
`SCIENTIFIC_REALIZATION_READINESS`, `PHASE_1F_C_SCIENTIFIC_VERDICT`,
`COMMON_BACKGROUND_CLOCK_RATE`, `GLOBAL_PERTURBED_DRESSED_SPACETIME`,
`WALL_VORTICITY`, `WALL_SHEAR`, all four rank integers,
`CONDITIONAL_FORWARD_UNIQUENESS`, `UNIQUE_TIMESCAPE_PREDICTION`,
`PHYSICAL_INTERFACE_CLAIM`, and the four observational authorizations.

Beyond agreement, I checked the *evidence* behind the load-bearing
classifications: `wall_acceleration = DERIVED_FROM_GENERIC_GR` ✓ (kinematic
identity), `wall_vorticity = DERIVED_FROM_GENERIC_GR` ✓ (Frobenius),
`wall_shear = MODEL_SECTOR_RESTRICTION` ✓ (metric ansatz, not derived),
`background_clock = DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` ✓ (requires the
clock identifications), `wall_expansion = DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`
✓ (requires the external pullback), `optional_metric_trace` initial data
`EXTERNAL_CLOSURE_INPUT` ✓. None overstates its basis.

**Status: `PASS`.**

## 25. Citation audit

| Citation | Adjacent statement | Assessment |
|---|---|---|
| W09 Eq. (B7) | `gamma_w = dt/dtau_w` | Consistent with the frozen project usage of the Timescape wall lapse; the *conditional* wording ("only after the explicit clock identifications") correctly separates the source statement from the project assumption. |
| BMR Eq. (2.5) | ADM lapse `N_W = alpha_W exp(nu_W)`, used at first order as `alpha_W(1+nu_W)` | Internally coherent: `models.py` states the exponential parameterization, `geometry.py` states the first-order form, the code implements `alpha*(1+nu)`, and the docstring says the first-order form is retained. The truncation is explicit, not silent. |
| BMR Eq. (2.6) | `A_W,i = D_W,i nu_W` | Matches the generic ADM identity `A_i = D_i ln N` at first order with homogeneous `alpha_W`, which I derived independently. |
| BMR Eq. (2.34) | `omega_W,ij = 0` for `u_W = n` | Matches the generic Frobenius result. |
| BMR Eqs. (2.29)–(2.30) | clock chain rule for `partial_t psi` | The chain rule itself is elementary; the citation is topical rather than load-bearing. |
| BMR Eq. (3.1), Eqs. (2.37)–(2.39) | `K_ij = -h h nabla n` convention and the `C_W` evolution | The convention is stated explicitly in the scenario contract (`K_ij=-(1/2)L_n h_ij; Theta_W=-K`) and I verified the resulting equation independently. |
| BDE Eqs. (14)–(16) | expansion frame law sign | Matches the frozen Phase 1F-B sign, which the v1 Phase 1F-B audit derived independently. |
| BDE Eq. (74) | physical/reference derivative distinction | Consistent in topic; this is the citation adjacent to the F-1 contradiction, where the *prose* misstates which convention the caller supplies. |

**Explicit limitation:** W09, BMR and BDE are not present in this repository
(`.reference/` holds only the pinned upstream notebook) and I had no
authorization to fetch them. I therefore verified that each cited equation is
*mathematically correct as stated* and *supports the adjacent statement on
internal and generic-GR grounds*, but I could **not** verify the equation
*numbers* against the published sources. Every implemented equation does carry
a citation, and each separates source statement / project derivation /
generic-GR derivation.

**Status: `PASS_WITH_EXPLICIT_CONDITIONS` (equation numbers unverifiable
offline).**

## 26. Finding table

| ID | Item | Severity | Status | Provenance | Layer |
|---|---|---|---|---|---|
| F-1 | `H1ToWallSpatialPullback` docstring says "already wall-physical" operators, contradicting field names, units tokens, `scale_factor_relation` and `geometry.py`; guards are string-only, so an already-physical operator is accepted and silently double-scaled by `a_W^2` | **load-bearing** | `PARTIAL` | `EXTERNAL_CLOSURE_INPUT` | implementation docstring (+ optional guard), report, JSON |
| F-2 | Metric-trace `H_W^(t) nu_W` term never exercised: every fixture sets `hubble = 0`, so the correct and double-`alpha_W` forms are numerically identical | **load-bearing (coverage)** | `PARTIAL` | `DERIVED_FROM_GENERIC_GR` | tests only |
| F-3 | `test_phase1f_b_clock_chain_rule_and_no_second_hubble_factor` asserts two source substrings that both survive a double-`alpha_W` edit | supporting | `PARTIAL` | — | tests only |
| F-4 | `test_compatibility_constraint_contains_no_clock_factor` computes an array it never compares; only a shape assertion and a source grep are operative | supporting | `PARTIAL` | — | tests only |
| F-5 | `wall_acceleration_covector` carries `1/a_W`, so it is the orthonormal component rather than a coordinate covector | cosmetic | `PASS_WITH_EXPLICIT_CONDITIONS` | `DERIVED_FROM_GENERIC_GR` | naming/report |
| F-6 | Boost-clock residual cannot discriminate measure conventions in the shipped fixture (both `Q_0` measures are uniform over the same cells) | cosmetic | `PASS_WITH_EXPLICIT_CONDITIONS` | — | tests only |
| F-7 | External source equation numbers (W09/BMR/BDE) unverifiable offline | disclosure | `PASS_WITH_EXPLICIT_CONDITIONS` | — | report only |
| — | Clock audit, ADM sign/expansion, boost sign, `a_W` placement (numerics), pullback ontology, `nu_W` closure, acceleration, zero-mode, congruence, rank, uniqueness, generic-GR/interface/observational/D3 firewalls, report–JSON consistency | — | `PASS` | as tabulated above | — |

### Detail for each non-PASS finding

**F-1** — file `src/timescape_fsigma8/phase1f_c/models.py`, class
`H1ToWallSpatialPullback`, docstring lines 259-266 (the sentence "construction
must provide the already wall-physical gradient and Laplace–Beltrami
operators"), interacting with validation lines 328-336 and consumption at
`geometry.py:116-120, 137-142`.
*Scientific reason:* the contract must fix a single convention for `D_W` versus
`D_gamma_W`; it currently states both. *Counterexample:* I constructed a
pullback whose Laplacian was `L/4` (the already-physical operator for
`a_W = 2`) while declaring the required reference units token; the constructor
accepted it, and the runtime would divide by `a_W^2` again, giving a physical
Laplacian wrong by `a_W^2` with no diagnostic. *Minimal correction:* replace
the sentence with one stating that reference/comoving operators are required
and that Phase 1F-C applies `a_W^-1`/`a_W^-2` itself; optionally add a
numerical convention check (e.g. assert the supplied operator's spectrum is
`a_W`-independent, or require the caller to pass the reference spacing so the
runtime can verify one eigenvalue). *Layers:* implementation docstring
(mandatory), report §on the pullback and JSON `spatial_pullback_contract`
(recommended), tests (only if the numerical guard is added). **No equation
changes.**

**F-2** — file `tests/test_phase1f_c_wall_common_geometry.py`, `make_case`
(line 94, `hubble=np.zeros(time.size)` passed through to
`make_phase1f_b_case`), affecting
`test_optional_metric_trace_equations_and_rank` (447).
*Scientific reason:* the audit-critical property "no second `alpha_W` on
`H_W^(t)`" is untestable when `H_W^(t) = 0`. *Counterexample:* with the shipped
fixture, correct and double-`alpha_W` derivatives differ by `0.0`; with
`H = 0.05`, `alpha_W = 1+0.2t` they differ by `7.5e-06`. *Minimal correction:*
add one metric-trace test with `H != 0` and `alpha_W != 1` (a 101-point grid
with `a_W = exp(H t)` satisfies the frozen 1F-B rate and propagation gates),
asserting `d_t C_W == H nu + alpha dTheta/3` against an independently computed
array. *Layer:* tests only. **No equation or implementation changes.**

**F-3** — same file, lines 275-281. *Scientific reason:* a source-substring
assertion does not constrain behaviour; I demonstrated both assertions survive
the defect they name. *Minimal correction:* replace the substring assertions
with the numerical assertion from F-2. *Layer:* tests only.

**F-4** — same file, lines 413-425. *Scientific reason:* the computed
`expected` array is discarded; the test does not test its stated property.
*Minimal correction:* assert that the compatibility residual is unchanged when
`alpha_W` is varied with all other inputs fixed. *Layer:* tests only.

## 27. Blocking corrections

**F-1** is the only finding that must be corrected before the realization can
be accepted as v1, and the correction is confined to the contract
documentation (plus, optionally, one substantive guard). No equation, no
numerical result, and no verdict token changes.

## 28. Non-blocking improvements

- F-2/F-3/F-4: replace the three weak/vacuous tests with the numerical checks
  described above (tests only).
- F-5: rename `wall_acceleration_covector`, or document that it holds
  orthonormal components under the declared `D_W = a_W^-1 D_gamma_W`
  convention.
- F-6: give the wall measure weights a non-uniform profile in at least one
  fixture so the boost-clock gate also discriminates measure conventions.
- F-7: record in the report that the external equation numbers were not
  verified against the published sources within this repository.

## 29. Final scientific status

The Phase 1F-C realization is scientifically sound as implemented. Independently
re-derived and confirmed: the clock chain `alpha_W = 1/gamma_w` under an
explicit, gated branch; `N_W = alpha_W(1+nu_W)`;
`partial_t psi_dw = -alpha_W Q_0 nu_W` at first order; `bar(Theta_W) =
3 H_W^(t)/alpha_W` and `deltaTheta_W = (3/alpha_W)(d_t C_W - H_W^(t) nu_W)`
with all signs and factors; the frozen boost sign
`deltaTheta_W = deltaTheta_d,w - D_W^2 psi_dw`; `D_W^2 = a_W^-2
Delta_gamma_W`; `A_i = D_i nu_W`; and
`d_t C_W = H_W^(t) nu_W + (alpha_W/3) deltaTheta_W`. All authorization ceilings
hold: `UNIQUE_TIMESCAPE_PREDICTION`, `PHYSICAL_INTERFACE_CLAIM`,
`OBSERVATIONAL_AUTHORIZATION`, `RSD_AUTHORIZATION`, `SIGMA8_AUTHORIZATION`,
`FSIGMA8_AUTHORIZATION` all `NOT_GRANTED`; ranks 5 / 5 / +1 / 6 verified;
generic-GR, interface, morphology, observational and D3 firewalls intact.

The verdict is `REQUIRES_TARGETED_CORRECTIONS` solely because the blocking
`a_W^2` contract item carries a demonstrated, silent double-scaling hazard in
its documented API, and because the property the brief singles out for the
`H_W^(t)` term has no effective test coverage.

## 30. Exact recommended next action

Create one targeted correction commit on top of
`6a633903fe7355a9892ed61abefece5a7b6f2855`, without amending it and without
moving the `phase-1f-c-wall-common-spacetime-geometry-v1` tag, that:

1. corrects the `H1ToWallSpatialPullback` docstring to state that
   **reference/comoving** gradient and Laplace–Beltrami operators are required
   and that Phase 1F-C applies `a_W^-1` and `a_W^-2` itself (F-1, mandatory),
   and mirrors that statement in the validation report and the JSON
   `spatial_pullback_contract`;
2. optionally adds a substantive (non-string) guard that the supplied operator
   is `a_W`-independent;
3. replaces the three weak tests with numerical checks: a metric-trace case
   with `H != 0` and `alpha_W != 1` (F-2, F-3) and an `alpha_W`-variation check
   of the compatibility residual (F-4).

Then freeze as `phase-1f-c-wall-common-spacetime-geometry-v2` and re-audit only
those changes. Do not integrate into `main` before that re-audit.
