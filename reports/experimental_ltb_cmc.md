# Isolated conditional LTB--CMC experiment

## Provenance and scope

Date: 2026-09-23. Actual preflight HEAD:
`118b8f3af3c1360b0da74df8e9a9cb3ba1fed83a`, equal to the historical checkpoint.
The reported previous 718-pass results were not treated as current evidence.
The working tree already contained a modified README and untracked `astra/`,
two independent audit reports, and the Phase 1F-D source, test and report.
They are preserved; this task creates only the six files listed below.
No historical classification or audit is rewritten.

This experiment is **distinct from Phase 1F-D**. CMC means constant
`K=-div(n)`, not constant dust expansion `Theta`. No Phase 1F-D criterion,
remediation, completion, revision or integration is asserted.

Assume GR, zero cosmological constant, geodesic irrotational dust, spherical
symmetry, simultaneous bang, expanding branch, positive density and regular
material domain `0<=r<=1` of finite positive intrinsic volume. The user fixes
`m=m0*r**3`, `2*E_LTB=r**2*kappa`, the smooth chi transition, and equal central
and boundary ages. There are no other free radial profiles.

- Spherical symmetry and simultaneous bang: `MODEL_SECTOR_RESTRICTION`.
- Curvature profile, two anchors, tracker clock and offset C:
  `EXTERNAL_CLOSURE_INPUT`.
- Results of this conditional branch: `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`.

The local flat core is not the entire Timescape wall or dressed geometry.
The boundary is not finite infinity, Gamma of H1 or an Israel interface.
No matching of geometries across that boundary is constructed.

## Equations and sign audit

Primary references, not copied upstream implementation:

1. [Sussman, arXiv:1002.0173v2](https://arxiv.org/pdf/1002.0173v2),
   Eqs. (1)--(3), (5)--(7), (A.1)--(A.2). Our `m` equals the paper's M;
   **its E equals `2*E_LTB`**. Its gravitational kappa is not our profile.
   These equations give the metric, dust density, expansion, shear and
   orthogonal spatial curvature. The exact parabolic and hyperbolic solutions
   supply independent reference checks, not published CMC benchmark data.
2. [Gourgoulhon, gr-qc/0703035](https://arxiv.org/pdf/gr-qc/0703035),
   Eqs. (4.63)--(4.65), (6.90), restoring G in the matter term. These fix the
   negative-divergence convention and the lapse evolution operator.
3. [Buchert--Mourier--Roy, arXiv:1912.04213v2](https://arxiv.org/pdf/1912.04213v2),
   Eqs. (4.5)--(4.6), (4.9), (4.12), (4.16), (4.18), (4.20), (E.2).
   The measure is dust-intrinsic, not induced-slice volume. The rescaling
   uses normal lapse divided by tilt.
4. [Wiltshire, arXiv:0909.0749v2](https://arxiv.org/pdf/0909.0749v2),
   Eqs. (B2), (B3), (B6), (B7), (B12), for the separate clock comparison.
   In the project's frozen parameters the exact bridge would be
   `b=(2+fv0)*(1-fv0)/(3*fv0*HD0)`. No other parameter named b is identified
   with this b. The new core imports no frozen tracker or Phase 1F-D code.

The supplied CMC ODE, central series, lapse basis and anchors are conditional
reductions/closures, not separately numbered published Timescape equations.
No concrete sign or factor contradiction was found in the supplied contract.
The convention audit gives the following reductions:

```text
n = gamma*d_s + (xi/A)*d_r, gamma=sqrt(1+xi**2)
div(n) = gamma*Theta + xi_r/A + 2*R_r*xi/(A*R)
S_r = A*xi/gamma
xi_r = -A*(K_star+gamma*Theta) - 2*(R_r/R)*xi
```

Here `R_r` is always evaluated at fixed s. `K_star` is a BVP eigenparameter,
not a fitting function. At the centre the regular singular equation gives
`xi_r(0)=-a0*(K_star+2/s_c)/3` and the stated quadratic expansion of S.

For `R=r*a`, all density/curvature expressions have regular algebraic limits:

```text
R_r = a+r*a_kappa*kappa_r
a_skappa = (1-2*m0*a_kappa/a**2)/(2*a_s)
G*rho = 3*m0/(4*pi*a**2*R_r)
R_u = -2*(3*kappa*a+r*kappa_r*(a+kappa*a_kappa))/(a**2*R_r)
```

The normal velocity of the selected family is `N_c=gamma*S_s_c`.
The trace evolution equation has the **positive** source `K_s`:

```text
L[N_c] = K_s
U = k_parallel**2+2*k_perp**2+4*pi*G*rho*(2*gamma**2-1)
K_s = (1-gamma_b*w0(0))/phi(0)
N_c = gamma_b*w0+K_s*phi; lambda = N_c/gamma
```

For tilted dust, normal energy plus stress trace is
`rho*(2*gamma**2-1)`. At the centre both principal curvatures equal `K/3`.
No positive-sign restriction on K_s is imposed. The analytical lapse bound
is conditional on a regular geometry: positive U gives positive phi and w0;
w0 increases outwards. If K_s>=0, superposition gives
`N_c>=gamma_b*w0(0)`. If K_s<0, the regular radial flux equation starting at
`N_c(0)=1` prevents a first downward crossing, giving `N_c>=1`.
The numerical code checks the resulting lower bound on its sample points,
not as an interval-certified theorem.

The instantaneous averages use `4*pi*A*R**2 dr`, **not** `4*pi*B*R**2 dr`.
Rest mass integrates `m_r/(G*sqrt(1+2*E_LTB))`; it is generally smaller than
`m0/G` for positive kappa (negative spatial curvature). The local dust Hamilton
constraint, multiplied by lambda squared and intrinsically averaged, gives
`3*J**2=8*pi*G*rho_lambda-(R_lambda+Q_lambda)/2`. This mostly tests algebra and
measure consistency; it is not an independent existence or embedding test.
The independent nearby-age volume derivative is therefore also essential.

## API and dimensions

New source files only:

```text
src/timescape_fsigma8/experimental_ltb_cmc/__init__.py
src/timescape_fsigma8/experimental_ltb_cmc/geometry.py
src/timescape_fsigma8/experimental_ltb_cmc/solver.py
src/timescape_fsigma8/experimental_ltb_cmc/clock.py
tests/test_experimental_ltb_cmc.py
reports/experimental_ltb_cmc.md
```

Example (illustrative units and external parameters, not a Timescape fit):

```python
from timescape_fsigma8.experimental_ltb_cmc import LTBModel, Numerics, solve_cmc
from timescape_fsigma8.experimental_ltb_cmc.clock import solve_at_tracker_clock

model = LTBModel(m0=0.2, kappa_star=0.2, r_c=0.25, r_o=0.7,
                 G=1.7, length_unit="L", mass_unit="M")
num = Numerics(bvp_tol=2e-7, bc_tol=2e-10, age_rtol=2e-12,
               check_tol=2e-5, initial_nodes=81, max_nodes=4000,
               check_nodes=401, quadrature_order=32, age_maxiter=60)
geometry = solve_cmc(s_c=1.0, model=model, numerics=num)
comparison = solve_at_tracker_clock(t=1.0, b=2.0, C=0.1,
                                    model=model, numerics=num)
```

With c=1, time and length share a unit. `s_c,m0,t,b,C,S,A,R,R_r` have that
unit; r and kappa are dimensionless; G must be supplied in length/mass.
Unit labels are mandatory metadata, not automatic conversions. Internally
lengths are divided by s_c and densities are represented as G*rho: this is
not a physical choice G=1. Physical density and mass outputs restore the
supplied G. No hidden normalization of m0, age, bang time or volume occurs.

`CMCSolution` supplies sampled read-only profiles, K_star, K_s, averages and
dimensionless residual diagnostics. There is no embedding/existence flag.
`LTBDomainError` means invalid/nonfinite inputs or a nonpositive selected
age; `LTBNumericalError` means arithmetic, conditioning, resolution, BVP or
post-check failure. Neither error returns a partial solution.

The separate adapter first chooses `s_c=tau_w+C`, solves the same geometric
problem and only then calculates N, ell, H_Omega, the weighted averages and
the residuals `H_Omega-H_D` and `log(rho_D*V/M_rest)`. It never feeds either
residual back into the BVP. `tau_w(0)=0`; C is external. The clock factor
alpha_W is not tilt gamma. ell=N/gamma is not the normal/ADM lapse N.

## Numerical method and limitations

The expanding age integral is inverted by safeguarded vector Newton steps,
bounded between a0 and `a0+s*sqrt(kappa)`. Substitution `y=a*z**2` removes
the endpoint square-root singularity. Fixed-order Gauss--Legendre rules of
orders n and 2n are compared for both age and its curvature derivative.
The parabolic solution and curvature derivative are analytic. Chi and its
first derivative use log-logistic forms, avoiding subtraction of 1-chi.
Exponentially negligible transition tails are rounded to their representable
endpoints; bulk overflow or loss of representability is an error.

Adaptive SciPy `solve_bvp` collocation supplies the unknown K and treats
`-2*xi/r` with its singular-matrix mechanism, enforcing the exact central
regularity condition. No epsilon-start shooting or assumed K bracket is
used. The lapse has regular flux variables `z=(a**2/B)*y_r`:
`y_r=B*z/a**2`, `z_r=B*a**2*(U*y-source)-2*z/r`.
This avoids numerical differentiation of B or a second radial chi derivative.
The library's forward-difference Jacobian is intentionally used; all error
tolerances and node budgets are explicit. Overlapping mesh nodes are merged
within 64 binary64 epsilon to avoid zero-length collocation intervals.

Means use n and 2n Gauss rules separately on the core, transition and outer
region. Q uses a centred variance rather than a difference of second moments.
Checks include nodes, midpoints and a uniform check grid. The operator and
flux-definition residuals, boundary conditions, mass, Hamilton identity,
quadrature comparison and necessary positivity/age/K/tilt bounds must pass
before a result is returned. They do not prove bounds between all samples.

Default tolerances are in the API example. The BVP tolerance is SciPy's
dimensionless relative RMS residual; boundary tolerance is absolute in
s_c-scaled variables. Post-check residuals use `max(1, absolute terms)` in
those same dimensionless variables, except mass, normalized to rest mass.
The age tolerance is relative; its n/2n comparison gate is 8*age_rtol.
Boundary checks allow 4*bc_tol for the reconstructed lapse. These factors
are explicit engineering gates, not rigorous error estimates.

Nonzero dimensional outputs must fit the normal binary64 range; logarithmic
rescaling avoids preventable intermediate overflow. A positive clock age
lost to offset cancellation within 64 epsilon of the summand scale is
rejected. Very large dimensionless scale separation, thin transitions,
large tilt, exponentially small central w0, and unresolved age quadrature
can fail. There is no claim of convergence over the whole parameter domain,
uniqueness across BVP branches, or a rigorous floating-point certificate.
A failed solve, or an unresolved/negative lapse, is a numerical investigation
request, not a proof of geometric non-existence. No warnings are suppressed.

## Validation evidence

The 50 targeted tests exercise the exact flat solution (including the stable
analytic phi/w0 basis), Sussman's hyperbolic parametrization, independent
local derivatives and constraint, chi endpoints, two fixed inhomogeneous
cases, central series, independent Simpson/quad mass and volume checks,
nearby-age derivatives, small-curvature asymptotics, dimensional and G
rescaling, clock normalization, input failures, numerical failures and the
scientific firewall. No parameter scan is performed.

For `(s_c,m0,kappa_star,r_c,r_o,G)=(1,.2,.2,.25,.7,1.7)`, representative
tight-run values are:

```text
K_star       ~ -2.1217447595
K_s          ~  2.0475854464
V            ~  4.6819935026
M_rest       ~  0.11146251523
J            ~  0.72116159812
rho_lambda   ~  0.023902227801
Q_lambda     ~  5.1706903e-6
R_lambda     ~ -1.0779725535
```

The second fixed case is `(.7,.08,.4,.2,.8,2.3)`. Refining collocation and
quadrature preserves the means within test tolerances. At age 1 in the first
case, central volume differencing with h=.001 gives approximately
2.163485477 against `3J=2.163484794`; halving h from .002 reduces the error
by about four, and Richardson extrapolation agrees at the test tolerance.
Tests also compare the derivative of K and the full graph with K_s and lambda.

At epsilon=.01,.005,.0025, the defect in
`R_lambda=-6*epsilon/a0**2+O(epsilon**2)` decreases by about four per halving;
`abs(Q_lambda)/epsilon**2 < 3e-5` in these tests. A separate coarse/fine
calculation at the smallest epsilon keeps solver error well below the
truncation defect. No nonzero leading quadratic coefficient is presumed.

Actually executed in this task, with bytecode/cache writes disabled and
warnings as errors:

```text
.venv/Scripts/python.exe -B -W error -m pytest -q -p no:cacheprovider tests/test_experimental_ltb_cmc.py
50 passed in 34.67 s

.venv/Scripts/python.exe -B -W error -m pytest -q -p no:cacheprovider
Python 3.14.3: 768 passed in 112.71 s

.venv311/Scripts/python.exe -B -W error -m pytest -q -p no:cacheprovider
Python 3.11.9: 768 passed in 112.55 s
```

The complete suites were run concurrently; wall times are not performance
benchmarks. Current environments: numpy 2.5.2 / scipy 1.18.1 / pytest 9.1.1
on 3.14.3; numpy 2.4.6 / scipy 1.17.1 / pytest 9.1.1 on 3.11.9. No dependency
was changed. The total is the preexisting 718 plus 50 new tests; these are
current executions, not reuse of a historical baseline assertion.

Additional executed checks: AST parsing of all four new source modules and
the test module; `scripts/audit_numerical_tolerances.py` (435 comparisons,
zero missing explicit tolerances); `git diff --check` (clean); read-only
upstream HEAD/status check. Historical validation scripts that regenerate
old reports/inventories were not run, to preserve out-of-scope artifacts.

Final HEAD is still `118b8f3af3c1360b0da74df8e9a9cb3ba1fed83a`.
SHA-256 comparisons match the preflight for README, UPSTREAM.lock,
scientific_status.py, all three Phase 1F-D files, the Astra audit and the
two preexisting untracked independent audit reports. Final Git status:

```text
 M README.md                                      (preexisting)
?? astra/                                        (preexisting)
?? reports/experimental_ltb_cmc.md                (new)
?? reports/phase1f_b_dust_wall_boost_dynamics_v3_final_audit.md (preexisting)
?? reports/phase1f_c_wall_common_geometry_adversarial_audit.md (preexisting)
?? reports/phase1f_d_necessary_bound.md            (preexisting)
?? src/timescape_fsigma8/experimental_ltb_cmc/      (new: four source files)
?? src/timescape_fsigma8/phase1f_d.py               (preexisting)
?? tests/test_experimental_ltb_cmc.py              (new)
?? tests/test_phase1f_d_necessary_bound.py          (preexisting)
```

## Frozen scientific firewall

No changes to `scientific_status.py`, README, Phase 1F-D, existing audits,
dependencies, lock or upstream files. The pinned upstream checkout remains
`590c6fd5332acb15f5683ebf392a0d7ce54983c5`, clean in the current read-only check.
No commit, merge, push, stash, reset, checkout, history manipulation or
automatic integration into main is performed.

```text
REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING: NOT_DERIVED
ALL_TIME_TRANSFER_CONSTITUTIVE_COMPATIBILITY: NOT_DERIVED
PHYSICAL_TIMESCAPE_TRAJECTORY_EXISTENCE: NOT_DERIVED
UNIQUE_TIMESCAPE_PREDICTION: NOT_GRANTED
OBSERVATIONAL_AUTHORIZATION: NOT_GRANTED
RSD_AUTHORIZATION: NOT_GRANTED
SIGMA8_AUTHORIZATION: NOT_GRANTED
FSIGMA8_AUTHORIZATION: NOT_GRANTED
```

Perturbations, tangent solvers, H1, nu_W, effective pressure, P_lambda/P_ell,
mean acceleration, effective Q/R, fitting, volume-based inverse clock maps,
parameter scans and every observable remain unimplemented. Convergence on
these cases establishes neither matching all-time, nor a physical Timescape
trajectory, nor H1 compatibility.
