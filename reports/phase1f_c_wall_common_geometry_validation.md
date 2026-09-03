# Phase 1F-C clock-anchored wall/common-spacetime geometry validation

## 1. Repository checkpoint and preflight

Implementation began on `main` at
`d2f150222cb08565aa9d0822747250309d8aaa67`, equal to fetched
`origin/main`. The three frozen Phase 1F-B annotated tag objects and peels were
verified as:

- v1 `d784074049148fad65632fe91848eada8923bb7a` -> `27fd65fd2a05c5b990508d948703897f433b566e`;
- v2 `bd1facf1fce246ef6fb42d02f03c5da6c2eef3a0` -> `16440e1a682c8d62d1e1b1d15fe8fad9290fa66a`;
- v3 `61dc9cf7602908b563158554d1b991a8d7059ab7` -> `d2f150222cb08565aa9d0822747250309d8aaa67`.

The pinned upstream checkout was clean at
`590c6fd5332acb15f5683ebf392a0d7ce54983c5`; the pinned notebook SHA-256
was `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a`.
Both frozen baselines passed 588 tests with no failures, skips, xfails, or
warnings on Python 3.14.3 and 3.11.9.

The untracked Phase 1F-B final audit at
`reports/phase1f_b_dust_wall_boost_dynamics_v3_final_audit.md`, SHA-256
`08c30893e8df88818760a91d85c9839770d7234f263c226446b634fddc216930`,
is an authorised pre-existing exception. It is neither a Phase 1F-C
deliverable nor staged or modified here.

## 2. Frozen scientific boundary

The Phase 1F-B state

\[
 (\Delta_w,Z_w,\Delta_v,Z_v,\psi_{dw})
\]

retains rank five. Phase 1F-C consumes its sealed scalar boost result and does
not modify its equations, D3 semantics, Candidate A, Phase 1F-A density
science, H1 morphology, or any observational authorization. Driver-only
Phase 1F-C adds no differential state variable.

## 3. Realization

The exact realization is
`H1-1F-C-CLOCK-ANCHORED-SCALAR-NORMAL-KINEMATIC-GEOMETRY-V1`
(`H1-1F-C-CA-SNKG-V1`). Its readiness is
`READY_FOR_CONDITIONAL_IMPLEMENTATION`; its scientific verdict is
`PARTIAL_GEOMETRIC_CLOSURE_DERIVED_NEW_PERTURBED_GEOMETRIC_DYNAMICS_REQUIRED`.

## 4. Clock ontology

The implementation keeps four objects distinct:

| Object | Meaning | Status |
|---|---|---|
| \(\gamma_w=dt/d\tau_w\) | Timescape background lapse, W09 Eq. (B7) | frozen background input |
| \(\alpha_W=d\tau_W/dt\) | common-time to background wall-proper-time rate | conditionally closed |
| \(N_W(t,x)\) | local ADM wall lapse | conditionally parameterized |
| \(\gamma_{dW}=-u_d\cdot u_W\) | relative Lorentz factor | distinct; no first-order scalar boost data |

Only `TIMESCAPE_COMMON_TIME_TO_BACKGROUND_WALL_PROPER_TIME` identifies
\(t_{common}=t_{Timescape}\) and \(\bar\tau_W=\tau_w\), giving

\[
 \bar\alpha_W=\gamma_w^{-1}.
\]

This follows from W09 Eq. (B7) only under the explicit clock map and is
`DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`. Positive finite \(\gamma_w\) is
mandatory. The clock object cannot carry or infer \(\nu_W\).

## 5. Wall-congruence ontology

The regional wall dust congruence \(u_{d,w}\) and physical wall-observer
congruence \(u_W\) have distinct required IDs. The selected relation remains

\[
 u_{d,w}^a=u_W^a+v_{d|W}^a+O(v^2),
\]

with the Phase 1F-B sign convention audited from BDE Eqs. (14)--(16).
The new API rejects equal wall-dust and wall-observer identities.

## 6. Scale-factor ontology

The external spatial realization records, rather than assumes, the relation

\[
 D_W=a_W^{-1}D_{\gamma_W},\qquad
 D_W^2=a_W^{-2}\Delta_{\gamma_W},
\]

following the physical/comoving harmonic distinction in BDE Eq. (74). The
pullback requires explicit `wall_scale_factor_mapping_id` and
`wall_hubble_mapping_id` tokens classified `EXTERNAL_CLOSURE_INPUT`; it does
not identify the H1 regional, finite-infinity, and local dressed-wall scale
factors globally. In a synthetic \(a_W=2\) check, the implemented
operator residual was exactly zero; omitting \(a_W^{-2}\) changed the result
by `0.08400000000000006`.

## 7. Selected scalar-normal ADM sector

The supported sector is scalar, longitudinal, hypersurface-normal, zero
shift, shear-free, linear, and local. The signature is `(-,+,+,+)` and

\[
 K_{ij}=-\tfrac12\mathcal L_n h_{ij},\qquad \Theta_W=-K,
\]

consistent with BMR Eq. (3.1) and its definition of \(K_{ij}\). Here
\(u_W=n\) and \(\sigma_W=0\) are `MODEL_SECTOR_RESTRICTION`; zero shift is
`GAUGE_CHOICE`; \(\omega_W=0\) is `DERIVED_FROM_GENERIC_GR` from
hypersurface normality (BMR Eq. (2.34)). None is a new Timescape prediction.

## 8. Spatial pullback contract

`H1ToWallSpatialPullback` requires an explicit matrix from the sealed H1 wall
domain to a separately identified local wall grid, explicit reference
gradient and Laplace--Beltrami matrices, positive measure weights, dimension,
metric/measure IDs, morphology ID, boundary/domain realization, units,
scale-factor relation, provenance, and a constant-preservation tolerance.
No identity map or H1 regional Laplacian is a default. The constructor checks
shapes, actual H1 identity, wall-mask support, and annihilation of constants.
It also verifies weighted self-adjointness, exactly one scalar constant
kernel, and positive coercivity off that kernel using explicit tolerances.

This is `EXTERNAL_CLOSURE_INPUT`. Its boundary realization is mathematical
input only: no H1 transmission condition becomes a gravitational junction or
physical statement about \(\Gamma\).

## 9. External lapse/congruence closure

`ExternalWallLapsePerturbationClosure` is mandatory. It supplies finite
\(\nu_W(t,x)\), time/frame/domain/metric IDs, explicit no-extrapolation
policy, units, and either external or `SYNTHETIC_VALIDATION_ONLY` provenance.
There is no default provider, zero fallback, CMC path, Einstein-equation
fallback, or map from background \(\gamma_w\).

The first-order local ADM lapse is

\[
 N_W=\bar\alpha_W(1+\nu_W),
\]

the authorised first-order split of the ADM lapse in BMR Eq. (2.5).

## 10. Acceleration derivation

For the explicitly normal congruence and spatially homogeneous
\(\bar\alpha_W\), BMR Eq. (2.6) gives at first order

\[
 A_{W,i}=D_{W,i}\nu_W.
\]

It is `DERIVED_FROM_GENERIC_GR`, conditional on the external lapse and
selected branch. The synthetic maximum was `0.004`; a spatial constant is
annihilated by the explicit gradient operator.

## 11. Expansion derivation and frozen sign

The load-bearing Phase 1F-B compatibility sign is retained:

\[
 D_W^2\psi_{dw}=\delta\Theta_{d,w}-\delta\Theta_W,
\qquad
 \delta\Theta_W=\delta\Theta_{d,w}-D_W^2\psi_{dw}.
\]

It follows from the first-order frame expansion law in BDE Eqs. (14)--(16),
conditional on the common-spacetime realization. The operation compares the
derived wall expansion with the sealed wall-expansion field that made the
Phase 1F-B boost admissible. Its worst residual was
`6.938893903907228e-17` (normalized L-infinity
`5.064886061246151e-16`) against
`5e-10`. Reversing the sign fails closed. A nonzero Laplacian fixture verifies
\(\delta\Theta_W\ne\delta\Theta_{d,w}\).

The compatibility equation contains no \(\alpha_W\).

## 12. Boost clock consistency

The frozen wall-proper-time equation, converted using the explicit clock map,
is

\[
 \partial_t\psi_{dw}=-\alpha_W Q_0\nu_W.
\]

The conversion is the chain rule in BMR Eqs. (2.29)--(2.30), applied to
Phase 1F-B v3. The extra perturbative lapse in
\(d\tau_{loc}/dt=\alpha_W(1+\nu_W)\) contributes only at second order. The
runtime independently aligns the external Phase 1F-C lapse with the lapse
that drove the frozen result and checks the clock equation. Residuals were
`2.710505431213761e-20` for unit \(\alpha_W\) and
`5.421010862427522e-20` for a time-dependent non-unit clock.

## 13. Optional metric-trace reconstruction

Only the explicit optional API accepts initial \(C_W\). The initial field,
time, weighted-mean-zero background split, measure/frame IDs, provenance, and
classification are mandatory. With the chosen sign convention, BMR Eq.
(3.1), and BMR Eqs. (2.37)--(2.39),

\[
 \partial_t C_W
 =H_W^{(t)}\nu_W+\frac{\alpha_W}{3}
  (\delta\Theta_{d,w}-D_W^2\psi_{dw})
 =H_W^{(t)}\nu_W+\frac{\alpha_W}{3}\delta\Theta_W.
\]

\(H_W^{(t)}=d\ln a_W/dt\) is already a common-time rate and is never
multiplied by a second \(\alpha_W\). Explicit trapezoidal integration yielded
a `1.3877787807814457e-17` update residual and
`8.673617379884035e-19` maximum weighted-mean drift. This local trace is not
the complete global W09 dressed metric.

## 14. State/rank accounting

| Runtime | Differential rank |
|---|---:|
| frozen Phase 1F-B scalar realization | 5 |
| Phase 1F-C driver-only | 5 |
| optional metric reconstruction contribution | 1 |
| augmented optional runtime | 6 |

The optional reconstruction does not rewrite the frozen Phase 1F-B rank.

## 15. Integrity and fail-closed gates

All arrays are detached read-only copies. Frozen records reject normal
assignment; canonical fingerprints detect representative low-level array or
attribute tampering at the next public operation. Runtime validation covers:

- exact sealed Phase 1F-B dependency identity;
- clock, time, congruence, geometry, metric, domain, morphology and frame IDs;
- `alpha_W=1/gamma_w` alignment with the clock consumed by Phase 1F-B;
- explicit-lapse alignment with the lapse consumed by Phase 1F-B;
- pullback dimensions, supports, units and constant kernel;
- perturbative lapse threshold and positive ADM lapse;
- boost-clock and wall-expansion compatibility residuals;
- explicit metric-trace initial data, split, mean and integration residual.

Changed geometry is never silently adopted or rebuilt.

## 16. Generic GR versus Timescape evidence

Normal-congruence acceleration and vorticity are generic-GR kinematics.
The clock reciprocal is derived only under the selected background clock map.
The lapse perturbation and spatial pullback remain external. No equation
\(G_{ab}[g_{dressed}]=8\pi G T_{ab}[regional\ dust]\) is implemented.
Hamiltonian, momentum, Raychaudhuri, and CMC conditions are not lapse closure
paths. In particular, the acceleration-divergence sign in a future
Raychaudhuri analysis cannot be used here to generate \(\nu_W\).

## 17. Synthetic validation and tolerances

The integrated fixture is genuinely three-dimensional and classified only
`SYNTHETIC_VALIDATION_ONLY`. Exact identities are checked near machine
precision. Numerical gates are explicit:

| Gate | Tolerance | Measured worst | Margin/status |
|---|---:|---:|---|
| clock alignment | `2e-13` | `0.0` | closed |
| lapse alignment | `2e-13` | `0.0` | closed |
| boost clock | `2e-11` | `5.421010862427522e-20` | closed |
| expansion compatibility | `5e-10` | `6.938893903907228e-17`; normalized L-infinity `5.064886061246151e-16` | closed |
| lapse linear regime | `0.05` | `0.00125` | closed |
| metric trace mean | `2e-11` | `8.673617379884035e-19` | closed |
| metric trace integration | `2e-13` | `1.3877787807814457e-17` | closed |
| pullback constants | `2e-13` | machine zero | closed |
| wall-operator weighted symmetry | `2e-13` | machine zero | closed |
| wall-operator scalar kernel | `2e-12` | dimension 1 | closed |
| wall-operator coercivity floor | `1e-8` | minimum `0.9999999999999997` | closed |

The Phase 1F-C targeted family passed 26 tests on each supported stack. The
complete repository suite passed 614 tests under Python 3.14.3 (NumPy 2.5.2,
SciPy 1.18.1, pytest 9.1.1) and Python 3.11.9 (NumPy 2.4.6, SciPy 1.17.1,
pytest 9.1.1), with zero failures, skips, xfails, or warnings.

## 18. Forbidden-shortcut verification

Tests and source review close the following routes: implicit clock branch;
nonpositive/nonfinite background lapse; inferred or default \(\nu_W\);
identity-map default; H1 Laplacian alias; opposite expansion sign; extra
\(\alpha_W\) on compatibility or common-time Hubble; equal dust/wall
congruence IDs; unsupported vector sector; missing \(C_W\) initial data or
split; low-level state tampering; CMC/Einstein/interface predictive APIs; and
observational or tracer APIs. D3 and Candidate A files are untouched.

## 19. Remaining external inputs and limitations

The irreducible inputs remain the perturbative wall-congruence lapse and the
H1-to-wall spatial pullback/operator realization. Morphology and mathematical
boundary/domain data remain external. A global perturbed dressed spacetime,
local Timescape source dynamics, physical \(\Gamma\) junction, transverse
sector, unique prediction, and every observational bridge remain ungranted.

## 20. Adversarial self-audit

| Requirement group | Classification | Evidence |
|---|---|---|
| frozen repository and Phase 1F-B boundary | COMPLETE | hashes, tags, two 588-test baselines |
| explicit selected clock branch | COMPLETE | reciprocal, positivity, identity, non-unit-clock tests |
| four-object lapse/Lorentz ontology | COMPLETE | separate types and forbidden inference paths |
| scalar-normal ADM sign and sector | COMPLETE | typed sector/gauge and exact sign tokens |
| explicit spatial pullback/operator | COMPLETE | no default, identity, shape, support, kernel, symmetry and coercivity gates |
| external perturbative lapse | COMPLETE | required typed closure; only external/synthetic provenance |
| acceleration and vorticity kinematics | COMPLETE | generic-GR classifications and analytic tests |
| wall expansion compatibility/sign | COMPLETE | independent frozen-field residual and opposite-sign adversary |
| clock factor placement | COMPLETE | non-unit clock and no-second-alpha regressions |
| optional metric trace and state counting | COMPLETE | mandatory initial data/split; rank 5/5/+1/6 tests |
| post-assembly integrity | COMPLETE | defensive copies, frozen records, operation-time fingerprints |
| generic-GR/Timescape/interface firewalls | COMPLETE | no predictive source or junction path |
| observational and D3/Candidate A firewalls | COMPLETE | no new path; complete frozen suite |
| reporting and deterministic inventory | COMPLETE | matching verdicts and explicit classifications |

No load-bearing requirement is `PARTIAL`, `MISSING`, or unjustifiably
deviated. The statuses `NOT_DERIVED` and `EXTERNAL_CLOSURE_INPUT` are intended
scientific boundaries, not implementation omissions.

## 21. Final verdict

```text
PHASE: 1F-C
SCIENTIFIC_REALIZATION: H1-1F-C-CLOCK-ANCHORED-SCALAR-NORMAL-KINEMATIC-GEOMETRY-V1
SCIENTIFIC_REALIZATION_READINESS: READY_FOR_CONDITIONAL_IMPLEMENTATION
PHASE_1F_C_SCIENTIFIC_VERDICT: PARTIAL_GEOMETRIC_CLOSURE_DERIVED_NEW_PERTURBED_GEOMETRIC_DYNAMICS_REQUIRED
COMMON_BACKGROUND_CLOCK: CONDITIONALLY_CLOSED
COMMON_BACKGROUND_CLOCK_RATE: alpha_W_EQUALS_INVERSE_gamma_w_UNDER_SELECTED_CLOCK_MAP
COMMON_PERTURBED_4D_SPACETIME: CONDITIONALLY_PARAMETERIZED_LOCALLY
GLOBAL_PERTURBED_DRESSED_SPACETIME: NOT_DERIVED
PERTURBED_WALL_CONGRUENCE: CONDITIONALLY_DEFINED_AS_HYPERSURFACE_NORMAL
WALL_ADM_LAPSE_BACKGROUND: CONDITIONALLY_DERIVED
WALL_LAPSE_PERTURBATION: NOT_DERIVED_FROM_FROZEN_TIMESCAPE
WALL_ACCELERATION: CONDITIONALLY_DERIVED_FROM_LAPSE_PERTURBATION
WALL_EXPANSION_PERTURBATION: CONDITIONALLY_DERIVED_FROM_FROZEN_COMPATIBILITY
WALL_VORTICITY: ZERO_IN_SELECTED_NORMAL_BRANCH
WALL_SHEAR: ZERO_BY_MODEL_SECTOR_RESTRICTION
H1_TO_WALL_SPATIAL_PULLBACK: REQUIRED_EXTERNAL_CLOSURE_INPUT
WALL_GEOMETRY_DRIVER: PARTIALLY_DERIVED_REDUCED_EXTERNAL_GEOMETRIC_CLOSURE_REQUIRED
IRREDUCIBLE_GEOMETRIC_INPUT: PERTURBED_WALL_CONGRUENCE_LAPSE_PLUS_SPATIAL_PULLBACK
FROZEN_PHASE_1F_B_DIFFERENTIAL_STATE_RANK: 5
DRIVER_ONLY_DIFFERENTIAL_STATE_RANK: 5
OPTIONAL_METRIC_RECONSTRUCTION_DIFFERENTIAL_RANK: 1
AUGMENTED_FULL_METRIC_RUNTIME_RANK: 6
CONDITIONAL_FORWARD_UNIQUENESS: GRANTED
UNIQUE_FROM_FROZEN_Y_ALONE: NOT_GRANTED
UNIQUE_TIMESCAPE_PREDICTION: NOT_GRANTED
FULL_GEOMETRIC_CLOSURE_DERIVED: NO
NEW_PERTURBED_GEOMETRIC_DYNAMICS_REQUIRED: YES
PHYSICAL_INTERFACE_CLAIM: NOT_GRANTED
OBSERVATIONAL_AUTHORIZATION: NOT_GRANTED
RSD_AUTHORIZATION: NOT_GRANTED
SIGMA8_AUTHORIZATION: NOT_GRANTED
FSIGMA8_AUTHORIZATION: NOT_GRANTED
```
