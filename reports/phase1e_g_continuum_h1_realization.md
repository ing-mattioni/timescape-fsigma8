# Phase 1E-G continuum-geometric H1 realization

## Status

```text
REALIZATION_ID:
H1-1E-G-COMOVING-CGI-ELLIPTIC-TRANSMISSION-V1

ROLE:
CONTINUUM_GEOMETRIC_REALIZATION_OF_1E_F_H1_CONTRACT

FRAMEWORK_STATUS:
COMPATIBLE_IMPORTED_DYNAMICS
EXPLICIT_MODEL_EXTENSION

SCIENTIFIC_STATUS:
CONDITIONALLY_DERIVED_CONTINUUM_REALIZATION

IMPLEMENTATION_STATUS:
CONDITIONAL_RESEARCH_RUNTIME
```

This is a `CONDITIONAL_CONTINUUM_GEOMETRIC_CLOSURE`, not a unique
Timescape prediction. It is `NON_OBSERVATIONAL` and `NOT_FSIGMA8`.

## Scientific problem and frozen inheritance

Phase 1E-F established a conditionally closed abstract H1 transmission
contract. Phase 1E-G supplies one explicit continuum geometry for that
contract. It does not change the independent regional state

\[
Y_{\rm bulk}=(\Delta_w,Z_w,\Delta_v,Z_v),\qquad \operatorname{rank}=4.
\]

The regional dust equations and derived curvature remain those already
cited to Galoppo--Mourier (GM) Eqs. (2.13), (2.20)--(2.23),
arXiv:2511.17160v2. `F_v`, `J_Xi`, regional curvature, target curvature and
effective-sector fields remain algebraic or derived. There is no interface
displacement, matching force, fifth differential state, arbitrary `F_v`
evolution, or arbitrary `J_Xi` history.

## Provenance boundary

The implementation separates three layers:

1. **DERIVED_FROM_TIMESCAPE/CGI_INPUT:** regional backgrounds, regional CGI
   scalar sources and the frozen Phase 1E-F/GM downstream equations.
2. **EXPLICIT_PHASE_1E_G_MODEL_EXTENSION:** carrier, morphology, pullbacks,
   fixed-reference branch, weak transmission operator and homogeneous-clock
   closure.
3. **NUMERICAL_REFERENCE_DISCRETIZATION:** periodic conservative structured
   grid, harmonic scalar face transmissibility and constrained sparse solve.

No upstream notebook source was copied. The Phase 1E-G carrier equations are
human-authorized model-extension equations; no paper equation number exists
for them.

## Carrier and morphology ontology

The reference carrier is a periodic `T^d` grid (`d=1,2,3` API; `T^3` is the
scientific reference topology). Its status is
`COMPUTATIONAL_REFERENCE_CARRIER_ONLY`; it is not a claim about physical
cosmological topology.

`MorphologySpec` requires `Omega_w`, `Omega_v`, `Gamma`, `Phi_w`, `Phi_v`,
orientation and source-injection provenance. A mask is accepted only as part
of this explicit object. `Gamma` is a `MATHEMATICAL_TRANSFER_INTERFACE`, not
finite infinity, a thin shell, a physical wall, a Darmois/Israel junction,
the GM zero-measure domain or radial-null matching.

The common normal is frozen wall-to-void:

\[
q_w=K_w\nabla u_w\!\cdot n_\Gamma,\qquad
q_v=K_v\nabla u_v\!\cdot n_\Gamma,\qquad q_w-q_v=0.
\]

With `n_w,out=n_Gamma` and `n_v,out=-n_Gamma`, this is equivalent to
`j_w,out+j_v,out=0`.

## Metric and pullback contract

Each regional comoving metric is

\[
h_r(t)=a_r(t)^2\gamma_r,\qquad
\widehat\gamma_r=\Phi_r^*\gamma_r.
\]

Relative to fixed `dmu_0`, the implementation stores

\[
J_r=\frac{d\mu_{\widehat\gamma_r}}{d\mu_0},\qquad
K_r^{ij}=J_r\widehat\gamma_r^{ij}.
\]

`RegionalGeometrySpec` validates symmetry, positive volume density and SPD
inverse metric. The structured backend is explicitly restricted to
isotropic/conformal tensors; unsupported anisotropic discretization fails
closed. The continuum contract itself remains the broader SPD tensor form.

The negative-curvature oracle uses the documented two-dimensional Poincare
metric `ds^2=4(dx^2+dy^2)/(1-r^2)^2`, of Gaussian curvature `-1`, on a
regional patch. In two dimensions its nonconstant `J` and inverse metric give
the positive tensor density `K=I`. This is a geometry/measure test, not a
complete physical void model.

## Weak form and source measure

On

\[
V_\Gamma=\{(u_w,u_v)\in H^1(\Omega_w)\oplus H^1(\Omega_v):[u]_\Gamma=0\},
\]

the explicit model-extension bilinear form is

\[
a_\Gamma(U,V)=\sum_r\int_{\Omega_r}
\widehat\gamma_r^{ij}\partial_i u_r\partial_j v_r,d\mu_{\widehat\gamma_r}
=\sum_r\int_{\Omega_r}K_r^{ij}\partial_i u_r\partial_jv_r,d\mu_0.
\]

The source functional for `-Delta_gamma psi=-s` is

\[
F_s(V)=-\sum_r\int_{\Omega_r}J_r s_r v_r,d\mu_0.
\]

The production load therefore includes `J_r`. The mandatory nonconstant-`J`
adversarial test reconstructs the manufactured potential with this load and
detects an error greater than `1e-3` when `J_r` is deliberately omitted.

## Kernel, projection and coercivity

The connected conservative operator has one pre-normalization kernel:
`span{1}`. The implementation performs two distinct operations:

- dual compatibility: project the metric-weighted source so `<Qb,1>=0`;
- primal normalization: solve with exactly one global `dmu_0`-mean constraint.

It never subtracts regional means separately. For the base fixture the raw
source mean is `1.0`, the projected mean is `0.0`, the solution mean is
`2.17e-19`, and the kernel dimension is one.

Continuum existence and uniqueness are conditional on connected Lipschitz
domains/interface, positive bounded `J_r`, uniform ellipticity and a global
Poincare inequality. The caller-declared continuum coercivity assumption is
`0.1` in the reference fixture. The independently computed constrained-grid
spectral lower bound is `4.6862915010`. The latter validates the discrete
fixture; it does not prove an arbitrary-domain uniform continuum bound.

## Green transfer and equal-geometry identity

On the single globally normalized space,

\[
G_\Gamma=A_\Gamma^{-1},\qquad
\Psi_r[s_r]=-G_\Gamma Q_\Gamma J_{{\rm source},r}[s_r],
\qquad T_r^\Gamma[s_r]=L_D\Psi_r[s_r].
\]

Metric `J_r` and regional source injection have distinct names and types.
The target `L_D=Delta_gamma_D` is separately named; there is no generic
Laplacian or generic `k` API.

When wall, void and target geometries coincide and the source is admissible,
`A_Gamma=-L_D`, hence `T[s]=s`. The full backend identity residual is below
`2e-10`. This is `TRANSFER_EQUAL_GEOMETRY_IDENTITY`, not the full regional
constitutive limit. At physical regional equality `A_P=0`; Phase 1E-F still
returns `FAIL_CLOSED_DEGENERATE_ONTOLOGY_REDUCTION`.

## Effective-sector bridge

Regional curvature is reconstructed only from the frozen derived relation,
then transferred:

\[
C_R^\Gamma=f_wT_w^\Gamma[\mathscr R_w]+f_vT_v^\Gamma[\mathscr R_v].
\]

The selected continuum path supplies, rather than accepts arbitrarily,

\[
E_{\Delta\Theta}^\Gamma=T_v^\Gamma[Z_v]-T_w^\Gamma[Z_w].
\]

On the explicitly selected homogeneous-clock branch,

\[
V_r=V_{r,i}a_r^3,\qquad \Xi_r=V_r^{-1}dV_r/dt_D=\alpha_r\Theta_r,
\]

and spatially homogeneous `alpha_r` gives

\[
E_{\Delta\Xi,0}^\Gamma=
\alpha_vT_v^\Gamma[Z_v]-\alpha_wT_w^\Gamma[Z_w].
\]

This `Xi` equality is a derived consequence of the selected branch, not a
universal imported Timescape identity.

The branch metadata require fixed partition, interface, comoving pullbacks,
target scalarization and homogeneous clock. Therefore

\[
\dot A_\Gamma=\ddot A_\Gamma=\dot G_\Gamma=\ddot G_\Gamma=0,
\qquad J_f^\Gamma=0.
\]

Unsupported moving/time-dependent geometry fails closed. Transfer jets use
`T[s_dot]` and `T[s_ddot]` analytically; finite differences appear only as
independent tests.

The bridge invokes the existing Phase 1E-F evaluator unchanged. Its base
fixture gives zero `C_P`, `R_Delta`, `R_Z`, `R_eff`, and `K_GM`. The inherited
classification remains: `C_P`, `R_Delta`, `K_GM` are constructed identity
checks; `R_Z`, `R_eff` are dynamic compatibility checks.

## Volume fraction consistency

The geometry supplies initial comoving volumes from regional metric measures:

\[
V_r(t)=V_{r,i}a_r^3,\qquad
f_{v,\rm geom}=\frac{V_v}{V_v+V_w}.
\]

The runtime compares this with explicit background `f_v` and fails closed on
disagreement. The base fixture has `0.5-0.5=0`. A nonconstant metric-volume
fixture demonstrates that a 50% coordinate-cell fraction can represent a
physical measure fraction of `2/3`.

## Morphology sensitivity

Two explicit equal-volume comparators were tested at fixed background data:
a layered 20%-void partition and a connected interior island. With explicit
unit L2 normalization, measured differences were:

| Quantity | `delta_morph` |
|---|---:|
| `T_w[Delta_w]` | 6.3245553203 |
| `T_v[Delta_v]` | 3.1622776602 |
| `E_DeltaTheta_Gamma` | 18.9736659610 |
| `C_R_Gamma` | 286.1161420549 |
| `F_v` | 143.0580710275 |
| `Delta_d` | 5.6920997883 |
| `Delta_eff` | 0.0 |

The resolved zero in `Delta_eff` is specific to the clean manufactured
fixture. Morphology sensitivity is model-closure sensitivity, not numerical
error, and was not tuned away.

## Structured discretization and convergence

The numerical backend uses a periodic cell-centered conservative stiffness
matrix and harmonic scalar face transmissibility. It is a
`FLUX_CONSERVATIVE_STRUCTURED_REFERENCE_DISCRETIZATION`, not the continuum
definition. For a smooth equal-geometry sine oracle at resolutions 16, 32,
64, the L2 errors were `9.1576e-3`, `2.2762e-3`, `5.6822e-4`; energy errors
were `5.7170e-2`, `1.4279e-2`, `3.5688e-3`. Observed successive rates were
`2.0084/2.0021` (L2) and `2.0014/2.0003` (energy). These fixture-specific
rates are not asserted at arbitrary discontinuous interfaces.

## Limitations and authorization

- Morphology and pullbacks remain required external model inputs.
- The backend supports isotropic/conformal structured coefficients, not a
  general anisotropic FEM realization.
- A structured grid does not establish a physical interface, global
  spacetime matching, unique morphology or observational validity.
- Heterogeneous transfer is not mode diagonal; mode mixing was observed.
- No Ricci-flow smoothing or moving-interface dynamics exists.
- No target-only physical inverse is claimed; the roundtrip recovers only the
  admissible projected source through the constrained operator chain.
- No RSD, tracer, survey, sigma8, f sigma_8 or likelihood API exists.

```text
PHASE_1E_G_SCIENTIFIC_STATUS:
CONDITIONALLY_CLOSED

MORPHOLOGY_STATUS:
REQUIRED_EXTERNAL_MODEL_INPUT

CONTINUUM_EXISTENCE:
PROVED_UNDER_EXPLICIT_REGULARITY_AND_UNIFORM_ELLIPTICITY

CONTINUUM_UNIQUENESS:
PROVED_AFTER_SINGLE_GLOBAL_MEAN_NORMALIZATION

COERCIVITY:
CONDITIONALLY_PROVED

DIFFERENTIAL_STATE_RANK:
4

UNIQUE_TIMESCAPE_PREDICTION:
NOT_GRANTED

PHYSICAL_INTERFACE_CLAIM:
NOT_GRANTED

OBSERVATIONAL_IMPLEMENTATION_AUTHORIZATION:
NOT_GRANTED

FSIGMA8_IMPLEMENTATION_AUTHORIZATION:
NOT_GRANTED
```
