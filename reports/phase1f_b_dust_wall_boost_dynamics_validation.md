# Phase 1F-B conditional dust-to-wall boost dynamics validation

## 1. Repository and preflight evidence

Implementation began from local and fetched `main` at
`87af7976b82b0b38e2c3e77dfc9458e664034c5d`. The Phase 1F-A implementation
and evidence-correction commits are the two linear ancestors `a56fa88b...`
and `87af7976...`; their annotated v1/v2 tag objects remain
`c9cd0c5...` and `e2ccb27...`. The pinned upstream checkout was clean at
`590c6fd5332acb15f5683ebf392a0d7ce54983c5`, and the pinned notebook SHA-256
was `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a`.

The only pre-existing tracked modification was `CLAUDE.md`, SHA-256
`27fc001a755f98f2bdb18a6cdfb7a578b12b09eb1b41a240a7bfcad212d317ce`.
It is classified `AUTHORIZED_PREEXISTING_USER_MODIFICATION`: it existed
before Phase 1F-B, was not created by this implementation, and was explicitly
authorized for carry-forward into the Phase 1F-B branch and final commit.

The untouched pre-implementation baseline passed as 539 tests on both Python
3.14.3 and Python 3.11.9, with zero failures, skips, xfails, or warnings.

The independent v1 adversarial audit is preserved as
`phase1f_b_dust_wall_boost_dynamics_adversarial_audit.md` (SHA-256
`7ef51fcd89ecdce68673791e4905a79e6db2ba5e1d2d1d3e37fb8ac3cab543ed`).
Its historical verdict is `TARGETED_CORRECTIONS_REQUIRED`; it found no
blocking scientific defect and is the provenance for the v2 corrections.

## 2. Frozen Phase 1F-A boundary

Phase 1F-B does not alter density reconstruction, the carrier density

\[
 \delta_{m,C}|_{\Omega_r}=(b_r-1)+b_r\delta_{m,r},
\]

the conditional evidence classification of broken density intertwining, the
physical three-dimensional volume guard, generalized spectra, or dressed-map
firewalls. It also does not modify Phase 1E-G state integrity, the D3 verdict
`RESOLVED_DERIVED_4_10`, the explicit `derived_4_10`/`printed_4_15` branches,
Candidate A, or any observational authorization.

## 3. Scientific realization

The exact realization is

`H1-1F-B-COMMON-SPACETIME-SCALAR-NORMAL-BOOST-DYNAMICS-V1`.

Its role is a conditional theoretical forward realization. It replaces the
need for a fully supplied boost *history* only after an explicit common-
spacetime/wall-geometry closure and explicit initial data have been supplied.
It does not predict those missing data.

## 4. Ontology and frame dictionary

| Object | Meaning | Prohibited identification |
|---|---|---|
| \(u_{d,w}\) | regional wall dust congruence | wall observer or tracer |
| \(u_{\mathcal W}\) | supplied physical wall-observer congruence | dust congruence by default |
| \(v_{d|\mathcal W}\) | dust velocity measured relative to that wall observer | galaxy, tracer, LOS, or RSD velocity |
| \(\delta\Theta_{d,w}\) | Phase 1F-A regional wall dust expansion perturbation | dressed wall-observer expansion |
| \(\delta\Theta_{\mathcal W}\) | externally supplied wall-observer expansion perturbation | dust expansion |

The convention is

\[
 u_{d,w}^a=u_{\mathcal W}^a+v_{d|\mathcal W}^a+O(v^2).
\]

The source/destination sign follows the first-order frame conventions audited
against BDE Eqs. (14)--(16) and DBE Eqs. (14)--(15), (27).

## 5. Background lapse versus perturbative lapse

The Timescape background lapse

\[
 \gamma_w=dt/d\tau_w
\]

is the W09 Eq. (B7) background clock ratio. It is not the relative Lorentz
factor \(\gamma_{d\mathcal W}=-u_d\cdot u_{\mathcal W}\), which is
\(1+O(v^2)\) at first perturbative order. The public closure accepts only a
field explicitly tagged `PERTURBATIVE_WALL_LAPSE_POTENTIAL`; it has no
`background_gamma_w` input and rejects that token as a driver.

Therefore none of background boost, wall acceleration, or lapse perturbation
is inferred from \(\gamma_w(t)\).

## 6. Common-spacetime closure contract

`CommonSpacetimeWallGeometryClosure` is immutable and binds:

- common-spacetime, wall-observer, and regional-dust congruence IDs;
- the exact H1 wall pullback and wall regional metric/operator ID;
- common-time and wall-proper-time map IDs;
- a strictly increasing common-time grid with no extrapolation;
- a detached dust-expansion time grid and time-coordinate ID that must match
  the common-spacetime grid and coordinate exactly;
- \(a_w\), \(H_{\mathcal W}\), and the positive wall proper-time rate, whose
  role is explicitly `PROVENANCE_ONLY_NON_DYNAMICAL_METADATA` because the
  implemented derivative is with respect to declared common time;
- \(\delta\Theta_{\mathcal W}\) and the perturbative lapse potential
  \(\nu_{\mathcal W}\);
- the explicit `GEOMETRIZED_C_EQUALS_ONE` unit system and all field units;
- scalar/hypersurface-orthogonal, zero-vorticity, and explicit
  `SHEAR_FREE_QUASI_FLRW_COMMON_SPACETIME` model restrictions;
- explicit normalization/kernel provenance;
- `EXTERNAL_GEOMETRIC_CLOSURE` or `SYNTHETIC_VALIDATION_ONLY` provenance.

No `TIMESCAPE_PREDICTED` provenance exists.

## 7. Load-bearing sign convention

The selected frame convention gives

\[
 \boxed{D_a v_{d|\mathcal W}^a
 =\delta\Theta_{d,w}-\delta\Theta_{\mathcal W}}.
\]

For \(v_a=D_a\psi_{dw}\),

\[
 \boxed{D^2\psi_{dw}
 =\delta\Theta_{d,w}-\delta\Theta_{\mathcal W}}.
\]

The opposite sign is exercised as an adversarial input and fails the public
compatibility gate.

## 8. Regional operator and unit conversion

Phase 1F-A implements the frozen comoving regional operator

\[
 L_w=a_w^2D_w^2=\Delta_{\gamma_w},
\]

using GM Eqs. (2.2), (2.20)--(2.24); the physical/comoving spatial-operator
distinction is also explicit in BDE Eq. (74) and footnote 22. Thus Phase 1F-B
implements

\[
 \boxed{L_w\psi_{dw}=a_w^2
 (\delta\Theta_{d,w}-\delta\Theta_{\mathcal W})},
\qquad
 D_w^2\psi_{dw}=L_w\psi_{dw}/a_w^2.
\]

At \(a_w=2\), the manufactured compatibility residual is
`1.0408340855860843e-17`. Deliberately omitting the \(a_w^{-2}\) conversion
is rejected.

## 9. Boost propagation

The acceleration frame law, audited from BDE Eqs. (14)--(16), together with
dust geodesicity from GM Eq. (2.9), gives

\[
 \boxed{\dot v_{d|\mathcal W,a}
 +H_{\mathcal W}v_{d|\mathcal W,a}=-A_{\mathcal W,a}}.
\]

For the supplied hypersurface-normal wall lapse,
\(A_{\mathcal W,a}=D_a\nu_{\mathcal W}\). The selected scalar commutator
then yields the gradient class

\[
 D_a(\dot\psi_{dw}+\nu_{\mathcal W})=0.
\]

With the explicit mean-zero representative this is

\[
 \boxed{\dot\psi_{dw}=-Q_0\nu_{\mathcal W}}.
\]

The V1 implementation uses an explicit trapezoidal common-time update.
Interpolation is declared `PIECEWISE_LINEAR_NO_EXTRAPOLATION`; no evaluation
outside the supplied time grid is exposed.

## 10. Initial-data modes

Exactly two modes exist and neither is a default:

1. `SUPPLIED_INITIAL_BOOST`: an explicit mean-zero \(\psi_{dw}(t_i)\) with
   provenance;
2. `EXPANSION_MATCHED_INITIAL_BOOST`: a boost-specific constrained solve of
   \(L_w\psi_i=a_{w,i}^2(\delta\Theta_{d,w,i}-
   \delta\Theta_{\mathcal W,i})\).

The expansion-matched initial-potential error was
`1.3010426069826053e-18`; its compatibility residual was
`1.3877787807814457e-16`. There is no zero-boost class or implicit zero
initial value.

## 11. Scalar, transverse, and harmonic policy

The runtime accepts only the enum value
`SCALAR_LONGITUDINAL_HYPERSURFACE_ORTHOGONAL`. The transverse sector is
`EXCLUDED_BY_EXPLICIT_SCALAR_MODEL_RESTRICTION`, not predicted to vanish.
No transverse velocity field is returned and no vector-theory rank is
assigned.

Non-gradient harmonic vector modes are likewise outside the scalar-potential
state. On a topology such as \(T^3\), a constant vector can have zero
divergence and curl while remaining invisible to \(\psi_{dw}\). Thus
`HARMONIC_VECTOR_SECTOR: EXCLUDED_BY_EXPLICIT_SCALAR_MODEL_RESTRICTION` and
`HARMONIC_VECTOR_ZERO_AS_TIMESCAPE_PREDICTION: NOT_GRANTED`. Mean-zero
normalization of the scalar potential does not resolve that vector sector.

The mean-zero representative removes one regional constant. Lapse data must
either already satisfy `REQUIRE_MEAN_ZERO` or the caller must explicitly
select `EXPLICIT_Q0_PROJECTION`. No projection is implicit.

## 12. Interface firewall

The regional matrix is reused only after the caller supplies the explicit
boost-specific boundary classification
`EXPLICIT_EXTERNAL_BOOST_BOUNDARY_CLOSURE` with the mathematical condition

\[
 D_n\psi_{dw}|_\Gamma=v_{d|\mathcal W}^a n_a|_\Gamma=0.
\]

This is an `EXPLICIT_EXTERNAL_NO_PENETRATION_CLOSURE` for the selected
wall-interior realization. It is not derived from Timescape, is not inherited
from H1 density transmission, does not turn \(\Gamma\) into a physical
material wall, and leaves `PHYSICAL_INTERFACE_CLAIM: NOT_GRANTED`.

Runtime enforcement is `FAIL_CLOSED`: the supplied or elliptically
reconstructed initial potential, the full supplied lapse-driver history
through \(D_n\nu_{\mathcal W}|_\Gamma=0\), and every propagated potential are
checked independently against explicit `2e-11` boundary tolerances. No
incompatible field is projected into the boundary model.

## 13. Differential state rank

The frozen Phase 1F-A differential rank remains four for
\((\Delta_w,Z_w,\Delta_v,Z_v)\). The selected scalar Phase 1F-B realization
adds the propagated scalar field \(\psi_{dw}\), so its selected rank is five.
This statement does not assign rank five to a full vector theory.

## 14. Expansion compatibility residual

The independent load-bearing residual is

\[
 C_\Theta=\delta\Theta_{d,w}-\delta\Theta_{\mathcal W}
 -L_w\psi_{dw}/a_w^2.
\]

For the manufactured 3-D fixture:

- maximum absolute residual: `5.551115123125783e-17`;
- normalized L-infinity residual: `4.956352788505162e-16`;
- tolerance: `5e-10` inverse common time;
- worst time: `0.5`;
- worst carrier index: `1`.

Perturbing only \(\delta\Theta_{\mathcal W}\) by `1e-4` fails closed.
Its evidence classification is
`INDEPENDENT_SCIENTIFIC_COMPATIBILITY_GATE`; it is not aggregated with the
construction diagnostics below.

## 15. Propagation/geodesicity construction diagnostic

The interval residual is the Crank--Nicolson diagnostic form of

\[
 R_A=A_{\mathcal W}+\dot v+H_{\mathcal W}v.
\]

It is evaluated separately from \(C_\Theta\), but it is not independent
physical validation in this scalar construction: \(v=D\psi\),
\(A_{\mathcal W}=D\nu_{\mathcal W}\), and
\(\dot\psi=-Q_0\nu_{\mathcal W}\) make it a construction identity up to the
implemented time-discretization error and selected commutator. Its machine
classification is
`CONSTRUCTION_INVARIANT_WITH_TIME_DISCRETIZATION_ERROR`. Finite differences
are used only for this diagnostic; they do not define the propagation law.
The manufactured values are:

- maximum absolute residual: `5.204170427930421e-18`;
- normalized L-infinity residual: `1.2621967275337053e-15`;
- tolerance: `2e-10` reference length/common-time squared;
- worst interval midpoint: `0.875`;
- worst carrier index: `0`.

A coarse nonzero-\(H_{\mathcal W}\) adversary at a `1e-12` gate fails closed,
while a resolved nonzero-Hubble homogeneous case passes.

## 16. Curl classification

Because the returned field is constructed as a scalar gradient, the curl-
free property is a construction invariant. It is recorded as
`CONSTRUCTION_INVARIANT_NOT_INDEPENDENT_NUMERICAL_EVIDENCE`, not counted as
independent validation.

## 17. Linear-regime gate

The explicit gate is

\[
 \max |v_{d|\mathcal W}|/c < 0.1,
\]

with explicit validation units \(c=1\). The measured maximum was
`0.01154469575172945`. A deliberately excessive amplitude is rejected, not
returned with a warning.

Velocity is returned in wall-reference-metric orthonormal Cholesky
components. This realizes the natural physical norm
\(a_w^{-2}\gamma_w^{ij}D_i\psi D_j\psi\), rather than an unweighted
coordinate-component norm.

## 18. Synthetic validation fixtures

| ID | Result |
|---|---|
| V1 | zero driver, nonzero initial boost: initial velocity `0.00824621125123532`, potential change `0` |
| V2 | manufactured lapse/potential: max potential error `8.673617379884035e-19` |
| V3 | compatibility passes; isolated wall-expansion perturbation rejected |
| V4 | reversed expansion-difference sign rejected |
| V5 | background `gamma_w` driver rejected |
| V6 | absent initial mode rejected |
| V7 | transverse request rejected |
| V8 | lapse/potential/source kernel mismatches rejected; explicit Q0 branch tested |
| V9 | H1 density/transmission BC inheritance rejected |
| V10 | excessive velocity rejected by the linear gate |
| V11 | correct \(a_w^2\) conversion passes; wrong factor rejected |
| V12 | embedding, metric, domain/frame identity mismatches rejected |
| V13 | 3-D normal-varying admissible initial/driver fields pass all boundary gates |
| V14 | mean-zero but boundary-penetrating supplied potential rejected |
| V15 | boundary-incompatible time-dependent lapse driver rejected |
| V16 | broken wall-interior and unbroken periodic Laplacians differ by `0.128` |
| V17 | explicit nonzero-background-shear declaration rejected |

All integrated scientific validation uses a genuine 3-D synthetic carrier.
The reduced-dimensional test is explicitly
`MATHEMATICAL_OPERATOR_FIXTURE_ONLY`.

## 19. Convergence

For a cubic manufactured potential evolved from its quadratic lapse driver,
trapezoidal common-time refinement gives:

| intervals | max potential error | rate |
|---:|---:|---:|
| 4 | `7.81249999999914e-06` | N/A |
| 8 | `1.953124999999785e-06` | `2.0` |
| 16 | `4.882812500001631e-07` | `1.9999999999993594` |
| 32 | `1.2207031250014919e-07` | `1.9999999999987186` |

This is classified
`SECOND_ORDER_NUMERICAL_SELF_CONVERGENCE_OF_THE_IMPLEMENTED_TIME_INTEGRATOR`.
The script reimplements the same trapezoidal update and measures its
closed-form truncation scaling, so it is numerical implementation evidence,
not independent validation of the physical propagation law. It is not an
interface-refinement or physical-Timescape convergence theorem.

## 20. Fail-closed behavior and state integrity

All closure/scenario/result records are frozen. Numerical arrays are
defensive, finite, read-only copies. Detached fingerprints cover arrays,
metadata, classifications, initial data, operator/domain identities,
geometry fields, normalization, and boundary choices. The sealed Phase 1E-G
operator validates itself before use. Ordinary assignment is rejected;
representative `object.__setattr__` replacement is detected before a result
is evaluated. Missing geometry, time/frame identity, driver, initialization,
kernel, BC, normalization, or scientific tolerance is never defaulted.

## 21. Conditional uniqueness

Once common geometry, wall congruence, lapse/acceleration driver, wall
expansion, initial scalar boost, operator/kernel, boost boundary condition,
and normalization are fixed, the selected forward scalar problem is
conditionally unique:

`CONDITIONAL_FORWARD_UNIQUENESS: GRANTED`.

It remains:

`UNIQUE_FROM_FROZEN_Y_ALONE: NOT_GRANTED` and
`UNIQUE_TIMESCAPE_PREDICTION: NOT_GRANTED`.

## 22. Numerical tolerances

| gate | value | measured worst | reason |
|---|---:|---:|---|
| compatibility max abs | `5e-10` | `5.55e-17` | independently reconstructed Phase 1F-A expansion plus elliptic application |
| propagation max abs | `2e-10` | `5.20e-18` | construction/time-discretization diagnostic |
| initial/propagated boundary normal velocity | `2e-11` | `0` | external no-penetration closure; reference length/common time |
| driver boundary normal acceleration | `2e-11` | `0` | boundary preservation; inverse common time |
| potential mean | `2e-11` | `1.63e-19` | explicit constant-kernel representative |
| lapse mean | `2e-11` | `2.63e-20` | require/project Q0 policy |
| scale-factor/H rate | `2e-11` | `0` | \(H=d\ln a/dt\) alignment |
| off-wall support | `2e-14` | `0` | wall-interior support firewall |
| velocity/c | `<0.1` | `0.01154` | explicit first-order regime |

No historical tolerance was changed.

The regenerated deterministic validation artifact has SHA-256
`961e491497b7c960ab4cd0a091f23a98dfdc9e2034ed3e5efeb3f4396069dce6`.
Python 3.14.3 and Python 3.11.9 regeneration produced byte-identical JSON.

The corrected test matrix collected 37 focused Phase 1F-B tests and 576
repository tests in each supported environment. Python 3.14.3 used NumPy
2.5.2, SciPy 1.18.1, and pytest 9.1.1; Python 3.11.9 used NumPy 2.4.6,
SciPy 1.17.1, and pytest 9.1.1. Both runs had zero failures, skips, xfails,
or warnings.

## 23. Observational firewall and limitations

The result is only a conditional scalar longitudinal regional-dust velocity
relative to an explicitly supplied wall-observer congruence in an explicitly
supplied common spacetime. It is not a wall-tracer velocity, galaxy velocity,
LOS velocity, RSD velocity, observed velocity, or observational Fourier
quantity. No power spectrum, primordial spectrum, transfer function,
\(\sigma_R\), \(\sigma_8\), \(f\sigma_8\), AP mapping, survey template,
dataset, covariance, likelihood, fit, or inference is implemented.

The unresolved next problem is the missing perturbed wall/common-spacetime
geometry itself. The transverse boost remains nonidentifiable from the frozen
scalar state and is excluded, not set to zero as a prediction.

The simplified propagation equation also requires the explicitly selected
shear-free quasi-FLRW background sector. Wall shear is excluded by this model
restriction; it is not predicted to vanish by Timescape.

## 24. Final machine verdict

```text
REALIZATION_ID:
H1-1F-B-COMMON-SPACETIME-SCALAR-NORMAL-BOOST-DYNAMICS-V1

SCIENTIFIC_REALIZATION_READINESS:
IMPLEMENTED_CONDITIONALLY

PHASE_1F_B_SCIENTIFIC_VERDICT:
PARTIAL_CLOSURE_NEW_GEOMETRIC_DYNAMICS_REQUIRED

COMMON_SPACETIME_FRAME_CLOSURE:
REQUIRED_EXTERNAL_GEOMETRIC_COMPLETION

DUST_TO_WALL_BOOST_PROPAGATION:
CONDITIONALLY_DERIVED

DUST_TO_WALL_BOOST_FROM_Y_ALONE:
NOT_DERIVED

EXPANSION_DIFFERENCE_CONSTRAINT:
CONDITIONALLY_DERIVED

LONGITUDINAL_BOOST_RECONSTRUCTION:
CONDITIONALLY_DERIVED

TRANSVERSE_BOOST:
NONIDENTIFIABLE_FROM_FROZEN_SCALAR_STATE

TRANSVERSE_SECTOR_RUNTIME:
EXCLUDED_BY_EXPLICIT_SCALAR_MODEL_RESTRICTION

TRANSVERSE_VECTOR_SECTOR:
EXCLUDED_BY_EXPLICIT_SCALAR_MODEL_RESTRICTION

HARMONIC_VECTOR_SECTOR:
EXCLUDED_BY_EXPLICIT_SCALAR_MODEL_RESTRICTION

HARMONIC_VECTOR_ZERO_AS_TIMESCAPE_PREDICTION:
NOT_GRANTED

WALL_BACKGROUND_SHEAR:
EXCLUDED_BY_EXPLICIT_SELECTED_GEOMETRIC_SECTOR

WALL_SHEAR_PREDICTED_ZERO_BY_TIMESCAPE:
NOT_GRANTED

WALL_PROPER_TIME_RATE_ROLE:
PROVENANCE_ONLY_NON_DYNAMICAL_METADATA

BACKGROUND_WALL_LAPSE_TO_BOOST:
NOT_DERIVABLE

PERTURBATIVE_WALL_LAPSE:
REQUIRED_EXTERNAL_GEOMETRIC_DRIVER_OR_EQUIVALENT

FULL_EXTERNAL_BOOST_HISTORY:
NOT_REQUIRED_IN_SELECTED_REALIZATION

WALL_GEOMETRY_DRIVER:
REQUIRED_EXTERNAL_CLOSURE_INPUT

INITIAL_BOOST_DATA:
REQUIRED_OR_EXPLICITLY_ELLIPTICALLY_RECONSTRUCTED

BOOST_INTERFACE_CONDITIONS:
NOT_DERIVED

BOOST_BOUNDARY_CONDITION:
EXPLICIT_EXTERNAL_NO_PENETRATION_CLOSURE

BOOST_BOUNDARY_CONDITION_DERIVED_FROM_TIMESCAPE:
NO

BOOST_BOUNDARY_CONDITION_INHERITED_FROM_H1_DENSITY_TRANSMISSION:
NO

BOOST_BOUNDARY_CONDITION_RUNTIME_ENFORCEMENT:
FAIL_CLOSED

EXPANSION_COMPATIBILITY_RESIDUAL:
INDEPENDENT_SCIENTIFIC_COMPATIBILITY_GATE

PROPAGATION_CONSTRUCTION_DIAGNOSTIC:
CONSTRUCTION_INVARIANT_WITH_TIME_DISCRETIZATION_ERROR

FROZEN_DIFFERENTIAL_STATE_RANK:
4

SELECTED_SCALAR_REALIZATION_DIFFERENTIAL_STATE_RANK:
5

CONDITIONAL_FORWARD_UNIQUENESS:
GRANTED

UNIQUE_FROM_FROZEN_Y_ALONE:
NOT_GRANTED

UNIQUE_TIMESCAPE_PREDICTION:
NOT_GRANTED

PHYSICAL_INTERFACE_CLAIM:
NOT_GRANTED

DRESSED_OBSERVATIONAL_WALL_VELOCITY:
NOT_GRANTED

TRACER_VELOCITY:
NOT_GRANTED

OBSERVATIONAL_AUTHORIZATION:
NOT_GRANTED

RSD_AUTHORIZATION:
NOT_GRANTED

SIGMA8_AUTHORIZATION:
NOT_GRANTED

FSIGMA8_AUTHORIZATION:
NOT_GRANTED
```
