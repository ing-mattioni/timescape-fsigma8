# Phase 1C-B1 — clean Timescape perturbation implementation and validation

**Date:** 2026-07-16

**Branch:** `phase-1c-perturbations`

**Scientific specification:** M. Galoppo & P. Mourier, JCAP 02 (2026) 066,
arXiv:2511.17160v2 ([GM])

**Scope:** independent implementation and numerical validation of the
D2-free/D3-free Mészáros and comoving perturbation systems on the frozen
Phase 1B Timescape tracker background.

## 1. Outcome and scope boundary

Phase 1C-B1 is complete for the two clean systems:

- the effective Mészáros approximation, [GM] Eq. (4.27);
- the comoving effective-fluid closure, [GM] Eqs. (4.20)-(4.23).

The independently implemented upstream-compatible trajectories reproduce the
pinned notebook oracle to a worst normalized L-infinity error of
**4.2e-16** under Python 3.14/SciPy 1.18. The same comparison under Python
3.11/SciPy 1.17 is **9.2e-10**, entirely bounded by the cross-version
forward-difference drift of the reconstructed initial `Z`; both are well
inside the documented cross-environment gate of 2e-8.

Tight RK45 and DOP853 solutions converge to a higher-accuracy DOP853 reference
to at worst **2.4e-10**; the implicit Radau cross-check agrees to
**1.9e-11**. All 204 tests pass under Python 3.14 and 3.11.

Explicitly not implemented: any barotropic system, the D2-corrupted upstream
sound speed or coefficient, either D3 branch, f-sigma-8, likelihoods, or
author communication. The Phase 1B background package and upstream clone were
not modified. No commit or push was performed.

## 2. Implementation inventory

| Path | Responsibility | Scientific equations |
|---|---|---|
| `perturbations/systems.py` | Pure Mészáros and comoving RHS functions; comoving matrix | [GM] (4.20)-(4.23), (4.27) |
| `perturbations/initial_conditions.py` | Planck-2018 qplus recipe; typed IC and rate-unit scenarios | [GM] (4.21), Sec. 5.1.2; Short & Coles (11)-(12) |
| `perturbations/scenarios.py` | Mandatory epoch choice; explicit time-unit and root controls | Wiltshire (2009) (38), via Phase 1B redshift |
| `perturbations/solver.py` | Typed solve layer; explicit method, rtol, atol, max/first step | integrates [GM] (4.21)-(4.23), (4.27) |
| `perturbations/residuals.py` | Analytic state second derivative and residuals | [GM] (4.24)-(4.26), Lambda=0 |
| `scripts/extract_upstream_perturbation_oracle.py` | Read-only clean-cell oracle extraction | upstream cells 0-8, 13-16 |
| `scripts/validate_clean_perturbations.py` | Oracle statistics, convergence, implicit cross-check, scenario effects | numerical validation only |
| `scripts/make_clean_fig2.py` | Independent Figure 2 and separate forensic overlay | [GM] Fig. 2 |

All public scientific functions cite the implemented equation in a docstring
or adjacent comment. RHS functions are pure: they return derivatives from
`(t, state, TrackerParams, G)` without mutation or hidden state.

### 2.1 State variables and signs

| System | State vector | Sign convention |
|---|---|---|
| Mészáros | `(Delta_d, dDelta_d/dt)` | second-order [GM] (4.27) |
| Comoving | `(Delta_d, Z, Delta_eff)` | `Z = -dDelta_d/dt`, [GM] (4.21) |

The independent variable is Buchert volume-average (bare) time in the unit
consistent with `TrackerParams.HD0`. The matrix scale factor and background
quantities retain the Phase 1B normalisation: `a_D(t0)=1+fv0/2=1.3685`, not
one. The comoving system is scale-independent and accepts no wavenumber.

### 2.2 Equation map

The comoving matrix acting on `(Delta_d, Z, Delta_eff)` is

```
[ 0,             -1,                  0             ]
[ -4 pi G rho_d, -(2/3) Theta,        -4 pi G rho_eff]
[ 0,             -(1+w_eff),          w_eff Theta    ]
```

corresponding entry-by-entry to [GM] Eqs. (4.21), (4.23), and (4.22).
It contains neither `cs2_eff` nor any time derivative of the backreaction,
so it is D2-free. It also contains no barotropic A33 entry, so D3 is absent.

The Mészáros RHS is [GM] Eq. (4.27):

```
d2Delta_d/dt2 = 4 pi G rho_d Delta_d - (2/3) Theta dDelta_d/dt.
```

It depends only on the clean Phase 1B `Theta` and `rho_d`.

## 3. Initial-condition reconstruction

### 3.1 Independent qplus recipe

The implementation uses the flat-LCDM incomplete-beta growing-mode solution
of Short & Coles, arXiv:astro-ph/0605013, Eqs. (11)-(12), with the audited
Planck-2018 parameters and recipe choices:

| Quantity | Value |
|---|---:|
| Omega_m | 0.315 |
| Omega_Lambda | 0.685 |
| h_LCDM | 0.674 |
| CMB factor | 6.6e-2 |
| IC redshift | 20 |
| forward-difference epsilon | 1e-5 |

The LCDM Hubble factor follows Hogg, arXiv:astro-ph/9905116, Eq. (14), and
`dqplus/dt = dqplus/dz * [-(1+z)H(z)]`. Finally, the sign follows [GM]
Eq. (4.21), `Z=-dDelta_d/dt`.

Under the Python 3.14/SciPy 1.18 oracle environment the results have exact
float64 equality with upstream:

| IC | Reconstructed | Upstream | Equality |
|---|---:|---:|---|
| `Delta_d` | 0.0031427229788258105 | 0.0031427229788258105 | bit-exact |
| `Z` | -0.16974050039281288 | -0.16974050039281288 | bit-exact |
| `Delta_eff` | 0 | 0 | exact prescription |

As an external narrative check, `6.6e-2*qplus(1090)` is approximately
`6.05e-5`, matching [GM] Sec. 5.1.2's CMB-scale amplitude.

### 3.2 Cross-SciPy forward-difference sensitivity

SciPy 1.17 returns `Z=-0.169740500548664`, differing from the upstream value
by `1.56e-10` absolute (`9.18e-10` relative). `Delta_d` remains bit-exact.
The cause is documented rather than suppressed: the prescribed derivative
subtracts two incomplete-beta evaluations separated by only `epsilon=1e-5`,
and the special-function implementation changed slightly between SciPy
versions. The test gate is an explicit 2e-10 absolute bound for the IC and
2e-8 for trajectories; bit equality remains asserted in SciPy 1.18.

### 3.3 Mandatory rate-unit choice

`InitialConditionScenario` has no defaults and requires one of:

- `upstream_unconverted`: inject the LCDM-H0-normalised number unchanged into
  the Timescape H0-normalised integration, exactly reproducing upstream;
- `lcdm_to_timescape_converted`: multiply by `0.674/0.7323`, giving
  `Z=-0.15622708898642074` in Timescape-H0 units under SciPy 1.18.

The latter is the dimensionally converted interpretation identified in
Phase 1C-A. Neither is silently selected or labelled as author-intended.

## 4. Mandatory epoch choice

`EpochScenario` likewise has no default and requires:

- `upstream_0p218_gyr`, reproducing notebook cell 15;
- `dressed_z20`, solving the Phase 1B dressed-redshift relation.

Brent controls are explicit: `xtol=1e-14`, `rtol=8.9e-16`, `maxiter=100`,
and a lower bracket of `1e-10*t0`. Results are:

| Convention | Initial time | Dressed redshift |
|---|---:|---:|
| upstream H0 code-time conversion | 0.218 Gyr | 18.58647 |
| dressed z=20 in upstream H0 code units | 0.19620643 Gyr | 20 exactly |
| dressed z=20 with exact Phase 1B Gyr conversion | 0.1962048643 Gyr | 20 exactly |

The small difference between the latter two z=20 times is only the already
documented upstream `9.778/h` approximation versus the exact IAU conversion.
No interpretation makes 0.218 Gyr equal to dressed z=20.

## 5. Read-only upstream oracle

The extractor executes an in-memory notebook containing only source cells
`0-8, 13-16`. Barotropic cell 12 and plotting cells are excluded. A final
independent sampling cell serialises `sol_comoving` and `sol_mezaros` into
`artifacts/upstream/oracle_clean_perturbations.json`.

Provenance:

- pinned commit: `590c6fd5332acb15f5683ebf392a0d7ce54983c5`;
- notebook SHA-256:
  `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a`;
- 1000 evaluation times from `0.218*h/9.778` to `t0`;
- upstream solve: RK45, `rtol=1e-3`, `atol=1e-6`, `max_step=inf`, automatic
  first step, all stated explicitly in the oracle metadata;
- source hash before and after extraction: identical.

The extraction emitted the already documented Windows/Jupyter infrastructure
warnings: pyzmq's Proactor selector-thread warning, asyncio policy
deprecations for Python 3.16, and the local unencrypted-kernel notice. No
warning was suppressed, and no numerical or notebook-cell warning occurred.

## 6. Like-for-like upstream reproduction

Machine-readable source:
`artifacts/independent/phase1c_b1_oracle_comparison.json`.

Python 3.14/SciPy 1.18 results:

| System/component | Max normalized L-infinity | Independent endpoint |
|---|---:|---:|
| comoving `Delta_d` | 1.80e-16 | 0.03861382693 |
| comoving `Z` | 3.27e-16 | -0.01300498895 |
| comoving `Delta_eff` | 3.67e-16 | 0.007080579210 |
| Mészáros `Delta_d` | 4.19e-16 | 0.03314424713 |
| Mészáros `dDelta_d/dt` | 4.09e-16 | 0.008147710957 |

Both independent and upstream solvers took 62 RHS evaluations for each
system. This exceptionally close result is meaningful because the independent
background uses tracker-reduced expressions rather than the notebook's
morphon composition and the IC recipe is reconstructed rather than copied.

The Python 3.11/SciPy 1.17 oracle comparison has worst normalized L-infinity
`9.18e-10`, traced to the IC special-function drift in Sec. 3.2.

## 7. Solver convergence and implicit cross-check

Machine-readable source: `artifacts/independent/phase1c_b1_convergence.json`.
The reference is DOP853 with `rtol=2e-13`, `atol=2e-15`. Values below are the
worst normalized L-infinity across all components.

| Solver | rtol / atol | Comoving | Mészáros |
|---|---|---:|---:|
| upstream RK45 | 1e-3 / 1e-6 | 5.88e-4 | 1.57e-3 |
| medium RK45 | 1e-6 / 1e-8 | 3.21e-6 | 2.89e-6 |
| tight RK45 | 1e-10 / 1e-12 | 2.34e-10 | 2.19e-10 |
| medium DOP853 | 1e-8 / 1e-10 | 2.81e-9 | 1.44e-9 |
| tight DOP853 | 1e-11 / 1e-13 | 7.76e-12 | 6.94e-12 |
| tight Radau | 1e-10 / 1e-12 | 1.88e-11 | 9.88e-12 |

The explicit and implicit gates are both 2e-8. They pass by more than two
orders of magnitude. The upstream default trajectories are successfully
reproduced but are not converged to the precision of the tight solutions;
science comparisons therefore use tight DOP853.

## 8. Equation, dimensional, and limiting-case tests

The validation suite establishes:

- every Mészáros RHS component equals [GM] (4.27);
- every comoving matrix entry equals [GM] (4.21)-(4.23);
- `Z=-dDelta_d/dt` both algebraically and along a tight numerical trajectory;
- the existing algebraic residual-identity test evaluates the Lambda=0 forms
  of [GM] (4.24)-(4.26) at four independently chosen states and times. It
  obtains first derivatives from the first-order RHS and second derivatives
  from the analytic `A_dot*y + A*A*y` identity, and retains its `1e-12`
  algebraic tolerance. This is an identity check, not a numerical-trajectory
  residual measurement;
- a separate numerical-trajectory test solves the comoving system with
  DOP853 (`rtol=2e-13`, `atol=2e-15`, `max_step=inf`, automatic first step)
  on a 4001-point uniform grid. It uses only five-point centred finite
  differences of the sampled trajectory for the required first and second
  derivatives, leaving 3997 interior samples for Eqs. (4.24)-(4.26);
- changing time units with `HD0 -> lambda HD0`, `t -> t/lambda`, and
  `Z -> lambda Z` produces the required first/second-derivative scaling;
- changing `G` only changes density units, leaving every `G*rho` matrix
  coefficient invariant to `1e-12`;
- in the `fv0 -> 0` early Einstein-de Sitter limit, the tight Mészáros
  solution follows `Delta_d proportional to t^(2/3)` and the comoving dust
  solution agrees with it to `2e-7`;
- Figure-2 endpoint scales agree with the published approximately
  `0.04 / 0.033 / 0.007` values.

### 8.1 Numerical-trajectory residual definition and measured gate

For each equation and interior sample, the test writes its Lambda=0 left-hand
side as a sum of terms `sum_j T_j` and defines

```
scaled residual = |sum_j T_j| / max(sum_j |T_j|, 1e-300).
```

The scale therefore contains the absolute magnitude of every term entering
that equation and remains defined only through the explicit `1e-300` floor if
all terms vanish. The derivatives are the standard five-point centred
fourth-order stencils

```
f'_i  = (f_{i-2} - 8 f_{i-1} + 8 f_{i+1} - f_{i+2}) / (12 h),
f''_i = (-f_{i-2} + 16 f_{i-1} - 30 f_i + 16 f_{i+1}
         - f_{i+2}) / (12 h^2).
```

They are applied directly to all three components of the numerical
trajectory. The test does not use `comoving_second_derivative`, `A_dot*y`, or
`A*A*y` for this measurement.

The Python 3.14 grid-refinement calibration was:

| Uniform grid | Interior samples | Eq. (4.24) | Eq. (4.25) | Eq. (4.26) | Worst |
|---:|---:|---:|---:|---:|---:|
| 1001 | 997 | 1.877e-6 | 2.898e-6 | 1.514e-5 | 1.514e-5 |
| 2001 | 1997 | 1.630e-7 | 2.398e-7 | 1.241e-6 | 1.241e-6 |
| 4001 | 3997 | 1.223e-8 | 1.732e-8 | 8.965e-8 | 8.965e-8 |

Successive worst-residual improvements are factors 12.2 and 13.8, approaching
the factor 16 expected for fourth-order truncation. A further 8001-point
diagnostic showed differentiation/interpolation roundoff beginning to affect
individual components, so 4001 points is the finest grid retained in the
clean convergence regime. The test gate is **1.5e-7**: it is above the
measured 4001-point maxima in both environments, but below the 2001-point
worst residual and therefore fails if the demonstrated refinement level is
lost.

At 4001 points, the exact Python 3.14 maxima were `1.22288694e-8`,
`1.73159006e-8`, and `8.96465472e-8` for Eqs. (4.24), (4.25), and (4.26).
Python 3.11 gave `1.22289042e-8`, `1.73157283e-8`, and `8.96463604e-8`.
The measured cross-environment worst is therefore **8.96465472e-8**.

## 9. Separate scenario effects

Machine-readable source:
`artifacts/independent/phase1c_b1_scenario_effects.json`. All values use tight
DOP853 and compare at common times from 0.218 Gyr to today. The baseline is
upstream epoch plus unconverted `Z`.

| Present-day quantity | Baseline | Converted Z only | Dressed-z20 epoch only | Both changes |
|---|---:|---:|---:|---:|
| comoving `Delta_d` | 0.03861654 | 0.03714942 (-3.80%) | 0.03939606 (+2.02%) | 0.03798335 (-1.64%) |
| comoving `Delta_eff` | 0.00708139 | 0.00680653 (-3.88%) | 0.00721742 (+1.92%) | 0.00695351 (-1.81%) |
| Mészáros `Delta_d` | 0.03315049 | 0.03191544 (-3.73%) | 0.03381257 (+2.00%) | 0.03262288 (-1.59%) |

The two choices are therefore not presentation details. They produce
percent-level shifts, are non-additive, and must remain explicit pending
author input.

## 10. Figure 2 reproduction

`scripts/make_clean_fig2.py` emits:

- `artifacts/independent/fig2_clean_independent.png/.pdf`: independent
  package only, tight DOP853, no oracle read;
- `artifacts/independent/fig2_forensic_upstream_overlay.png/.pdf`: a separate
  local forensic overlay using numerical oracle data.

The canonical figure reproduces all clean published content: comoving dust,
Mészáros dust, and comoving effective-fluid perturbations against
`a_D/a_w,0`, with the published log range. It is annotated with the explicit
upstream epoch and unconverted-Z scenario. The curves are distinguishable by
linestyle as well as colour.

## 11. Test matrix and warnings

| Environment | NumPy | SciPy | pytest | Result |
|---|---:|---:|---:|---:|
| Python 3.14.3 | 2.5.1 | 1.18.0 | 9.1.1 | **204 passed in 0.81s** |
| Python 3.11.9 | 2.4.6 | 1.17.1 | 9.1.1 | **204 passed in 0.86s** |

Both complete correction-validation runs finished without warnings. The
earlier sandbox-specific `PytestCacheWarning` was not reproduced and no
warning filter or suppression option was used.

## 12. Preservation and compliance audit

- `git diff` contains no path under `src/timescape_fsigma8/background/` and
  no change to `units.py` or `presets.py`.
- Phase 1B source SHA-256 values recorded before implementation remain
  unchanged after validation.
- The upstream notebook SHA-256 remains
  `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a`.
- All upstream-derived data remain under git-ignored `artifacts/upstream/`;
  all independent generated outputs remain under git-ignored
  `artifacts/independent/`.
- No barotropic function, D2-bug compatibility function, D3 branch,
  f-sigma-8 observable, or likelihood exists in the package.
- Nothing was committed, tagged, pushed, published, or sent to the authors.

## 13. Readiness for Phase 1C-B2

**The clean perturbation infrastructure is ready for Phase 1C-B2.** The typed
state conventions, explicit scenario objects, pure RHS pattern, solver layer,
oracle extraction, comparison metrics, convergence protocol, residual tests,
and dual-Python validation are all established and independently verified.

This readiness does **not** resolve the barotropic science. Any B2 work that
introduces the barotropic system must preserve the Phase 1C-A gates: no D2
coefficient in the scientific package, a mandatory explicit D3 branch choice
with neither branch called correct pending adjudication, an explicit tilt and
wavenumber convention, and separate forensic compatibility machinery. B1
does not authorize or prejudge those choices.
