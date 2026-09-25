# LTB--CMC experiment: single-age evolution of the section family

## Provenance, scope and status

Date: 2026-09-23. Documentary corrections: 2026-09-24, see "Documentary
corrections" below.

This is an extension of the isolated conditional LTB--CMC
experiment documented in `reports/experimental_ltb_cmc.md`. It adds the
derivative d/ds_c of the CMC section family **inside one fixed LTB
geometry**, at fixed r and fixed physical model parameters (m0, kappa profile,
anchors, G). From it the code computes P_lambda, J_s and the mean
acceleration q_c. It also adds an instantaneous comparison of these rates
with the tracker clock.

This is not:

- a remediation of an established scientific error;
- the completion, revision or integration of Phase 1F-D;
- a perturbation between geometries, a tangent solver or an H1 response;
- a unit rescaling or model homothety.

No Phase 1F-D criterion is asserted and Phase 1F-D is **not** declared
complete. Every assumption of the first solver is kept unchanged:

- GR with Lambda=0;
- geodesic irrotational dust;
- spherical symmetry;
- simultaneous bang and the expanding branch;
- the material domain r in [0,1];
- `m=m0*r**3`, `2*E_LTB=r**2*kappa(r)` and the same chi profile;
- `S(s_c,0)=S(s_c,1)=s_c`.

Classification of all new results: `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`.
The differentiated equations below are conditional research derivations of
the user-supplied contract. They are built on published relations, but they
are **not** published theorems and are **not** derived from the frozen
Timescape runtime. The primary sources used for conventions are:

- [Gourgoulhon, gr-qc/0703035](https://arxiv.org/pdf/gr-qc/0703035), Eqs. (4.63) and (6.90) (G07): the negative-divergence convention and the ADM trace/lapse equation;
- [Buchert--Mourier--Roy, arXiv:1912.04213v2](https://arxiv.org/pdf/1912.04213v2), Eqs. (4.5), (4.9), (4.12), (4.18) and (4.20) (BMR): the dust-intrinsic averages, their commutation rule and the averaged equations;
- [Sussman, arXiv:1002.0173v2](https://arxiv.org/pdf/1002.0173v2), Eqs. (1)--(3), (5)--(7): the LTB relations, with the conventions of the first report;
- [Wiltshire, arXiv:0909.0749v2](https://arxiv.org/pdf/0909.0749v2), Eqs. (B2), (B3), (B6), (B7) and (B12) (W09): the separate tracker clock, translated to b through f=t/(t+b).

## Documentary corrections (2026-09-24)

This file is the only one changed by the correction. No source, test,
tolerance, profile, anchor, dependency, `scientific_status.py` or Phase 1F-D
file was touched.

- **The seven Python files are unchanged.** The five experiment modules and the two test files are byte-identical to the versions recorded in `MANIFEST.sha256` of the 2026-09-24 export.
- **No suite was re-run** for this documentary change.
- **No retroactive baseline was reconstructed.**

1. **Sign error in the uniqueness paragraph of this report.**
   - The earlier text read `L[delta_X] = -delta_K_ss` and `delta_X = -delta_K_ss*phi`.
   - The correct statements are `L[delta_X] = delta_K_ss` and `delta_X = delta_K_ss*phi`.
   - The error was in this report's prose only. The user contract and the code were already correct: the flux equation `Z_r = e*(U*X - K_ss) + …` gives `L[X] = K_ss + …`.
   - The uniqueness conclusion is unchanged.
   - This is a correction of the report text, not a remediation of the original derivation or of the solver.
2. **Representability.** The earlier "Numerical limits" section claimed that representable background outputs imply representable evolution outputs. That claim was wrong and has been removed. The corrected text, with the counterexample from the independent review, is under "Numerical limits".
3. **Test evidence and provenance.** The precisions already recorded in `NOTA_EXPORT.md` and `logs/INDEX.md` of the export are now part of this report:
   - the qualified baseline;
   - the separate contexts of the later runs;
   - the scope of the 801-pass result;
   - the runs on the tree of commit `28a87a1`.

   The end of the implementation task, the later publication and the export are now kept distinct under "Later events". No new frozen checkpoint is promoted.

## Initial state actually verified

The instructions' historical checkpoint (`118b8f3…`), their test counts
(50 targeted tests, 768 full-suite passes on 3.14.3/3.11.9) and their Git
status were **reported information**. The working tree was not changed to
match them. What was verified in this environment, before any
modification:

- Repository `ing-mattioni/timescape-fsigma8`, branch `claude/loving-dijkstra-esoj6f`.
- HEAD `4f28a095e6401c31e0a90dfc4c35ae92cbc0592d`, equal to `origin/main` at the time; it already contains the remediation work of this session.
- `git status --short` showed exactly the six untracked experiment files:
  - `reports/experimental_ltb_cmc.md`;
  - `src/timescape_fsigma8/experimental_ltb_cmc/{__init__,clock,geometry,solver}.py`;
  - `tests/test_experimental_ltb_cmc.py`.
- These six files were not present in the fresh cloud clone. The user published them on the separate branch `experiment/ltb-cmc-background` (commit `586a1fb586c9f14d952f2b8f6d9d48f62cfd4ce7`). They were copied from there with read-only `git show`: no checkout, stage or merge. Their blob contents were verified identical.
- `astra/`, the Phase 1F-D files (`phase1f_d.py`, its test and report), the preexisting untracked audits and the README modification mentioned in the first report exist only on the user's machine. They are **absent** from this environment, so nothing here could touch them.
- SHA-256 of the six experiment files, `scientific_status.py` and `README.md` were recorded before the work began.

**Baseline full suite: qualified evidence (correction 3).**

- **The run.** A full suite with warnings as errors was **started** on both interpreters at 2026-09-23T12:54:48Z, running in parallel. The six files were present and no edit had yet been made.
- **The result.** Both runs reported 774 passed:
  - Python 3.13.12: 774 passed;
  - Python 3.11.15: 774 passed.

  The 774 is 724 preexisting tests plus the 50 targeted tests of the first solver.
- **Not isolated from the implementation work.** `solver.py` was modified on disk between 12:55:11Z and 12:55:50Z, while both runs were in progress. The logs end at 12:56:40Z and 12:56:47Z.
- **Version exercised: not verified.** pytest normally imports the modules during collection, at the start of the run, so the executed code is expected to be the `586a1fb` version. Which complete version was actually exercised is **not verified**.
- **One test reads the source at run time.** `test_firewall_and_readonly_profiles` in the first solver's tests reads the text of `solver.py` during execution. Its assertions hold for both versions.
- **`evolution.py` did not exist yet.** It was created only at 12:57:55Z.
- **No reconstruction.** This baseline is reported as observed. It has not been reconstructed after the fact.

## Files

New:

```text
src/timescape_fsigma8/experimental_ltb_cmc/evolution.py
tests/test_experimental_ltb_cmc_evolution.py
reports/experimental_ltb_cmc_evolution.md
```

Modified, minimally, inside the allowed set:

- `solver.py`
  - Adds the private frozen record `_Background` and `_checked_background`/`_solve_background`.
  - `_Background` holds the accepted dense collocation interpolants (`cmc.sol`, `lapse.sol`), the `section`/`sample` evaluators, the internal K, K_s and gamma_b, and the public `CMCSolution`.
  - `solve_cmc` now returns `_checked_background(...).solution`. Its validation, arithmetic policy, outputs and signature are unchanged, and the preexisting private `_solve` keeps its behaviour.
  - The public `CMCSolution` is built exactly as before.
- `clock.py`
  - The preexisting comparison is factored into `_comparison` (same arithmetic) and `_log_one_minus_f` (same expression).
  - Adds `EvolutionClockComparison`, `_signed_product` and `solve_evolution_at_tracker_clock`.
  - `solve_at_tracker_clock` and `tracker_clock` keep their signatures and results.
- `__init__.py`: exports `CMCEvolution`, `EvolutionResiduals` and `solve_cmc_evolution`. The clock adapters stay importable from `.clock`, as in the first design.

Unchanged, verified by SHA-256 at the end: `geometry.py` (no helper was needed), `tests/test_experimental_ltb_cmc.py`, `reports/experimental_ltb_cmc.md`, `scientific_status.py` and `README.md`. No dependency, lock, profile, anchor, upstream file or other package was touched.

The first report's closing list says "P_lambda/P_ell, mean acceleration …
remain unimplemented". That file was deliberately left unchanged, because it
is outside the allowed modification set. For this conditional branch only,
that sentence is superseded by the present report. Everything else in that
list remains unimplemented.

## API

```python
from timescape_fsigma8.experimental_ltb_cmc import solve_cmc_evolution
from timescape_fsigma8.experimental_ltb_cmc.clock import solve_evolution_at_tracker_clock

evolution = solve_cmc_evolution(s_c=1.0, model=model, numerics=num)
comparison = solve_evolution_at_tracker_clock(t=1.0, b=2.0, C=0.1,
                                              model=model, numerics=num)
```

`CMCEvolution` contains:

- the accepted background `solution` (a `CMCSolution`, not re-solved);
- K_ss [length^-3];
- the read-only profiles N_c_s, lambda_s and gamma_s [length^-1], on `solution.r`;
- P_lambda, J_s, `lambda2_D=<lambda**2 D>` and `var_E=Var(lambda*Theta)` [length^-2];
- q_c [dimensionless];
- `EvolutionResiduals`.

`EvolutionClockComparison` contains:

- the preexisting `ClockComparison` for the **same** accepted solution object;
- the `CMCEvolution`;
- alpha_dot and J_D [length^-1];
- P_ell, H_dot, H_D_dot and H_dot_residual [length^-2];
- q_required and q_residual [dimensionless].

No embedding, existence or all-time compatibility field exists.

Error handling follows the existing policy:

- `LTBDomainError` means invalid or nonfinite input.
- `LTBNumericalError` means a BVP, arithmetic, representability or post-check failure.
- No partial evolution is ever returned.
- No warnings are suppressed.

## Conventions and normalization

The suffix `_s` means d/ds_c at fixed r and fixed physical parameters along
S(s_c, r). The suffix `_age` means a local derivative with respect to dust
proper age. `K_star=-div(n)` and `lambda=N_c/gamma=dS/ds_c`. `gamma` is the
dust/section tilt, not the tracker's gamma_w or alpha_W.

The background solver scales lengths by L = s_c of the evaluated section. The
evolution keeps that L **fixed** while differentiating. In internal units
u = age/L, the evaluated section has u = 1 and m0/L is held constant, so

```text
K_hat = L*K_star,  dK_hat/du = L**2*K_s,  d2K_hat/du2 = L**3*K_ss,
dN_c/du = L*N_c_s, dlambda/du = L*lambda_s
```

and the physical outputs restore these powers of s_c through the package's
`dimensional` helper. That helper uses log scaling and rejects nonzero values
lost outside the normal binary64 range. m0/s_c is never held fixed during
the differentiation. Outputs of distinct solves are never differenced by the
production code: the method is a linear BVP built on the dense interpolants
of ONE accepted background.

Because kappa vanishes identically for r <= r_c > 0, the centre is exactly
EdS. The contract's centre formulas use this. In internal units they are:

```text
a_center = (9*m/2)**(1/3)
lim xi/r   = -a_center*(K+2)/3
lim xi_s/r = -(a_center/3)*((2/3)*(K+2) + K_s - 2)
gamma_s(0) = 0,  kperp_s(0) = kparallel_s(0) = K_s/3
U_s(0)     = 2*K*K_s/3 - 4/3
```

In physical units these match the contract, with `s_c` powers restored.

## Equations implemented (user contract)

Local sources on the section, with `F=sqrt(1+r**2*kappa)`:

```text
Hperp = a_age/a,  Hparallel = Theta - 2*Hperp
Hperp_age = -m0/a**3 - Hperp**2
D = Theta**2/3 + 2*sigma2 + 4*pi*G*rho,  Theta_age = -D,  rho_age = -Theta*rho
gamma_r = xi*xi_r/gamma,  lambda_r = (N_c_r - lambda*gamma_r)/gamma
v = xi/gamma,  v_s = lambda_r/A - v*Hparallel*lambda
xi_s = gamma**3*v_s,  gamma_s = gamma**3*v*v_s
kperp_s = -gamma_s*Hperp - gamma*Hperp_age*lambda - (F/R)*xi_s + xi*(F/R)*Hperp*lambda
kparallel_s = K_s - 2*kperp_s
U_s = 2*kparallel*kparallel_s + 4*kperp*kperp_s
      + 4*pi*G*rho*(-Theta*lambda*(2*gamma**2-1) + 4*gamma*gamma_s)
```

Two quantities come from the background, never from differencing:

- `xi_r` comes from the CMC ODE (G07 (4.63) reduction of the first report).
- `N_c_r = d*z` comes from the lapse flux. The flux z is rebuilt from the same superposition `gamma_b*w0 + K_s*phi` as N_c, applied to the dense flux interpolants.

`xi/r` and `xi_s/r` use the exact centre limits above, so no 0/0 is
evaluated. The contract also lists `A_s=A*Hparallel*lambda`,
`R_s=R*Hperp*lambda` and `Hparallel_age`. The flux form below uses A_s and
R_s through `d_s` and `e_s`. `Hparallel_age` is not needed; it was checked
algebraically consistent with `Theta_age=-D`.

Flux-form linear BVP, with `B=A/gamma`, `d=B/a**2`, `e=B*a**2` and
`z=(a**2/B)*N_c_r`:

```text
d_s = d*((Hparallel - 2*Hperp)*lambda - gamma_s/gamma)
e_s = e*(Theta*lambda - gamma_s/gamma)
X_r = d*Z + d_s*z
Z_r = e*(U*X - K_ss) + e_s*(U*N_c - K_s) + e*U_s*N_c - 2*Z/r
X(0) = 0,  Z(0) = 0,  X(1) = gamma_s(1)
lambda_s = X/gamma - lambda*gamma_s/gamma
```

Here X=N_c_s, Z=z_s (not the flux of X alone: the derivative of `a**2/B`
enters through `d_s`) and K_ss=d2K_star/ds_c**2 is the eigenparameter. No
sign is imposed on X, lambda_s, K_ss or P_lambda.

Uniqueness follows the contract. The difference of two solutions solves
`L[delta_X] = delta_K_ss` with homogeneous data: `delta_X(1)=0` and a regular
flux at the centre. Since `L[phi]=1` with `phi(1)=0`, this gives
`delta_X=delta_K_ss*phi`. Then `delta_X(0)=0` with `phi(0)>0` forces
`delta_K_ss=0`.

This is an existence-conditional uniqueness statement, not a uniform
conditioning guarantee. `phi(0)` is therefore exported as the diagnostic
`phi_center`.

(Corrected 2026-09-24: an earlier version of this report wrote
`L[delta_X] = -delta_K_ss` and `delta_X=-delta_K_ss*phi`. That was a sign
error in the report text only; see "Documentary corrections".)

Averages use **only** the dust-intrinsic measure `dmu=4*pi*A*R**2 dr` (BMR),
never B:

```text
E = lambda*Theta,  J = <E>/3,  P_lambda = <Theta*lambda_s>
J_s = (P_lambda - <lambda**2*D> + Var(E))/3      (centred variance)
q_c = -1 - J_s/J**2
```

J_s follows from `d(dmu)/ds_c = lambda*Theta*dmu` (BMR commutation rule)
and `Theta_s = Theta_age*lambda = -D*lambda`. P_lambda is computed directly
from the lambda_s profile. It is never back-solved from Raychaudhuri.

## Algorithm

1. `_checked_background` performs the single accepted background solve, with all of the first solver's gates. There is no second background solve; this is enforced by a test counting `_solve_background` calls.
2. The coefficients `d, e, d_s, e_s, U, U_s, N_c, z, gamma_s` are evaluated at any radius from `cmc.sol` and `lapse.sol` (the SciPy collocation interpolants) and from the analytic local geometry. Exact centre limits are selected by `np.where`. The results are cached per radius array.
3. SciPy `solve_bvp` solves the linear 2x2 flux system with the unknown parameter K_ss. The settings are:
   - it starts on the accepted background mesh, from a zero initial guess and `p=-4`;
   - the singular matrix `S=diag(0,-2)` supplies `-2*Z/r`, the same mechanism as the background;
   - `tol=bvp_tol`, `bc_tol=bc_tol`, `max_nodes=max_nodes`;
   - SciPy's forward-difference Jacobian.

   Non-convergence raises `LTBNumericalError`.
4. Post-checks run on the union of the public sample grid, the evolution nodes and their midpoints, and they re-apply the background acceptance bounds. Any failure raises; nothing partial is returned. The checks are:
   - the residuals of both flux ODEs, each normalized by max(1, |terms|), must be at most `check_tol`;
   - `X(0)`, `Z(0)` and `X(1)-gamma_s(1)` must be at most `4*bc_tol`;
   - `lambda_s(0)` and `lambda_s(1)` must be at most `4*bc_tol*(1+|gamma_s(1)|)`;
   - Gauss--Legendre orders n and 2n on the three segments [0,r_c], [r_c,r_o] and [r_o,1] must agree for J, P_lambda, `<lambda**2 D>`, Var(E) and J_s to within `check_tol`;
   - the algebraic averaged Raychaudhuri identity must hold to within `check_tol`;
   - J must agree with the accepted background J to within `check_tol`;
   - J must be positive, since q_c needs J>0.
5. Physical outputs are returned with the dimensional powers restored.

The tolerances are the explicit `Numerics` engineering controls, with the same
meaning as in the first report. The factors 4 are explicit gates. None of
these is a rigorous error bound.

## Tracker adapter

`solve_evolution_at_tracker_clock` first selects `s_c=tau_w(t;b)+C` with the
unchanged `tracker_clock`. It then calls `solve_cmc_evolution`, which never
receives t, b or C, and only afterwards computes:

```text
alpha = 2/(2+f),  f = t/(t+b)
alpha_dot = -2*b/(3*t+2*b)**2   (= -2*f*(1-f)/(t*(2+f)**2))
H_dot = alpha_dot*J + alpha**2*J_s
P_ell = alpha**2*P_lambda + 3*alpha_dot*J
H_D_dot = -(2+f**2)/(3*t**2),  J_D = H_D/alpha = (2+f)**2/(6*t)
q_required = (1-f)*(2-5*f)/(2+f)**2 = b*(2*b-3*t)/(3*t+2*b)**2
q_residual = q_c - q_required,  H_dot_residual = H_dot - H_D_dot
```

The robust evaluation works as follows:

- t and b are divided by max(t, b) before forming `(3t+2b)**2`, so the squares cannot overflow.
- alpha_dot and q_required are evaluated in logarithms.
- log(1-f) is always taken from b directly (`_log_one_minus_f`), so q_required stays nonzero when f rounds to 1. It is exactly 0 when 3t=2b.
- Products go through `_signed_product`, which returns 0 when a factor is 0 and otherwise applies the package's normal-binary64 policy.

The preexisting residuals are `e_H=H_Omega-H_D` and
`e_rho=log(rho_D*V/M_rest)`. They obey the contract's propagation identities:

```text
d(e_rho)/dt = 3*e_H
d(e_H)/dt = (alpha_dot/alpha - alpha*(1+q_required)*(J+J_D))*e_H - alpha**2*J**2*q_residual
```

Both identities were re-derived algebraically. The first uses
`d log rho_D/dt=-3H_D`, `dV/ds_c=3JV` and `ds_c/dt=alpha`. The second uses
`H_D=alpha*J_D` and the definition of q_required as the value that keeps
`H_D_dot=alpha_dot*J_D-alpha**2*(1+q_required)*J_D**2`. They are
interpretation and verification tools only. They are not BVP sources or
fitting targets, and nothing is fed back into the geometry. A small
q_residual at one instant does not show compatibility over an interval.

## Verification

### Independent verifications

These use information not shared with the evolution BVP.

- **Flat branch** (kappa_star=0, s_c=1.3, TIGHT). The contract's exact values are reproduced to within about 1e-16 relative: K_ss=-4/s_c**3, N_c_s=lambda_s=gamma_s=P_lambda=0, J=2/(3s_c), J_s=-2/(3s_c**2), q_c=1/2, `<lambda**2 D>=2/s_c**2`. The asserted tolerances are 2e-9 rel / 2e-10 abs.
- **Flat adapter** (t,b,C)=(1,2,0.1). The results satisfy `P_ell=2*alpha_dot/s_c` and `H_dot=2*alpha_dot/(3s_c)-2*alpha**2/(3s_c**2)` to about 4e-16 relative. Here P_ell≈-0.161 comes entirely from the alpha_dot term. Dropping that term would move H_dot by |2*alpha_dot/(3s_c)|≈0.054, which the test would catch.
- **Curved nearby ages at fixed physical m0.** Model BASE is (s_c,m0,kappa_star,r_c,r_o,G)=(1,.2,.2,.25,.7,1.7); the second model is (.7,.08,.4,.2,.8,2.3). Central differences of independent background solves were taken with h=4e-3, 2e-3 and 1e-3. All errors fall by a factor between 3.8 and 4.2 per halving, so they are truncation-dominated second-order errors. Richardson extrapolation then agrees with the evolution, as the table below shows.
- **Spatial versus BVP error, separated.**
  - The profile differences are taken at the knots `linspace(0,1,601)`, which belong to every TIGHT sample grid, so they carry no interpolation error.
  - The spatial-interpolation error was measured separately at 480 off-knot midpoints, with CubicSpline on the public grids. At h=1e-3 its maximum is 2.27e-11 against 2.27e-11 at the knots: interpolation adds nothing visible. Interpolating the background profiles themselves on 601 against 2401 check nodes gives errors of at most 5e-13.
  - The evolution BVP error was measured by comparing default and TIGHT numerics at the same age: |ΔK_ss|=5.5e-10, |ΔJ_s|=1.6e-11, |ΔP_lambda|=5.7e-12, |Δq_c|=3.2e-12 and profile differences of at most 9e-12.
  - Beyond h≈5e-4, background-solver noise amplified by 1/h dominates: the Richardson error rises from 6e-12 to 3e-10 for K_ss. No further convergence is claimed or tested there.
- **P_lambda from finite-difference lambda_s.** Richardson-extrapolated lambda_s, averaged with an independent Simpson rule on the knots, gives P_lambda to within 3e-14 of the returned -3.937e-4.
- **Independent Simpson averages** on the returned profiles with the A measure reproduce P_lambda, `<lambda**2 D>`, Var(E) and J_s to within 1e-11 (largest: 8.8e-12 for `<lambda**2 D>`). With the B measure, J_s differs by 7.6e-8, so a measure swap would be detected.
- **q_c** from the Richardson-extrapolated dJ/ds_c agrees to within 3.3e-11.
- **Clock at nearby t** (b, C and the model fixed; background-only solves at t±h, h=2e-3 and 1e-3). The following are all second order (error ratios 4.00), and after Richardson extrapolation they agree as listed; the asserted tolerance is rtol 1e-8, atol 1e-9:
  - dH_Omega/dt against H_dot: 1.3e-10;
  - d(e_rho)/dt against 3*e_H: 4.7e-10;
  - d(e_H)/dt against H_dot_residual: 1.3e-10.
- **Homothety.** s_c and m0, and in the adapter t, b and C, are scaled by 1e-4 and 1e4 (adapter: 1e-3 and 10), with G and the dimensionless profile fixed. It confirms every dimensional power: K_ss -3; N_c_s, lambda_s, gamma_s -1; P_lambda, J_s, `<lambda**2 D>`, Var(E) -2; q_c 0; alpha_dot and J_D -1; P_ell, H_dot, H_D_dot, H_dot_residual -2; q_required and q_residual 0. The observed relative differences are at most 1.6e-11. This check does not replace the fixed-m0 checks.

| Case (TIGHT) | Quantity | Richardson error | Returned value |
|---|---|---|---|
| BASE, h=2e-3/1e-3 | K_ss vs dK_s/ds_c | 6.2e-12 | -4.0581420631 |
| BASE, h=2e-3/1e-3 | J_s vs dJ/ds_c | 1.7e-11 | -0.69040998689 |
| BASE, h=2e-3/1e-3 | N_c_s, lambda_s, gamma_s at the knots | ≤ 5.4e-13 | max ≈ 3.1e-4, 3.1e-4, 4.5e-5 |
| BASE | P_lambda (FD lambda_s + Simpson) | 3.1e-14 | -3.9374938e-4 |
| BASE | q_c | 3.3e-11 | 0.32752246742 |
| second model, h=2e-3/1e-3 | K_ss, J_s (error ratios 4.000) | 4.3e-10, 4.9e-11 | -12.184971941, -1.5013395147 |
| second model | q_c | 3.9e-11 | 0.18233860319 |

### Algebraic verifications

These share identities with the construction, so they check the code, not
the physics.

- The averaged Raychaudhuri identity `3*(J_s+J**2)+4*pi*G*rho_lambda-Q_lambda-P_lambda=0` holds to at most 1e-15: 3e-16 for the internal normalized residual, 8.5e-16 absolute from the public outputs. It is an algebraic consequence of the J_s formula, the definition of Q_lambda and `<lambda**2*Theta**2>/3=Var(E)/3+3J**2`. It shares those identities with the J_s computation and **does not by itself validate lambda_s**, which is why the nearby-age checks above are necessary.
- The boundary values `lambda_s(0)=lambda_s(1)=0` follow automatically from `X(0)=0`, `gamma_s(0)=0`, `X(1)=gamma_s(1)` and `lambda(1)=1`. They check only the reconstruction formula and rounding.
- The e_H propagation identity evaluated with the returned numbers equals H_dot_residual to about 3e-17. This is an algebraic check of the adapter's formulas; the nearby-t check above is the independent one.
- The adapter compositions are checked in several equivalent forms: alpha_dot, J_D=H_D/alpha, and q_required in both forms.

### Numerical controls and failures

The tests cover:

- **Gates:** every residual gate, the boundary values and `phi_center` (0.1385 for BASE, 0.1212 for the second model), plus read-only, finite profiles.
- **Fault injection with monkeypatched `solve_bvp` in `evolution` only:**
  - forced non-convergence raises "Evolution BVP status";
  - an eigenparameter perturbed by 1e-3 relative is caught by the equation gate ("Unresolved evolution checks") through both APIs.
- **Propagated failures:** a background BVP failure propagates.
- **Input errors:** invalid ages, types and clock inputs raise `LTBDomainError`.
- **Representability:** an unrepresentable scale raises `LTBNumericalError`, and `_signed_product` enforces its range. The tested scales are ones at which the background itself already fails; see "Numerical limits" for the window in which only the evolution fails.
- **Clock limits:**
  - with f rounding to 1 (t=1e20, b=1), q_required = -3.33e-21 exactly as `b(2b-3t)/(3t+2b)**2` and is not collapsed to 0;
  - with 3t=2b, q_required is exactly 0.
- **Firewall:**
  - no forbidden fields (embedding, exists, H1, nu_W, observable, all-time/compatible, Q_lambda_s, R_lambda_s, sigma8, fsigma8);
  - unchanged signatures of `solve_cmc` and `solve_at_tracker_clock`;
  - `solver.py` and `evolution.py` import neither the clock nor Phase 1F-D nor `scientific_status`;
  - unchanged status constants.

`scripts/audit_numerical_tolerances.py` reports 510 comparisons in `tests/`
with zero missing explicit rtol/atol (rel/abs). 49 of those comparisons are
in the new test file.

## Test results actually observed

All runs used bytecode and cache writes disabled and warnings as errors.
Dependencies were neither installed nor updated.

The evidence is kept separate by context (correction 3). None of it
constitutes a new frozen checkpoint.

The logs of contexts 1–4 are preserved, unmodified, in the 2026-09-24 export
archive: `logs/`, with commands, times and hashes in `logs/INDEX.md`. The log
files contain only pytest output; the commands in `INDEX.md` come from the
session transcript. Some development runs were visible only on the console
and are not preserved as logs: the first run of the new file alone (27 passed
on 3.13) and a first targeted run on 3.11 (77 passed).

1. **Baseline**, started 2026-09-23T12:54:48Z. 774 passed on each interpreter, but it was not isolated from the edits to `solver.py`; see "Initial state actually verified".
2. **Intermediate full runs**, started 13:09:58Z, one interpreter after the other.
   - **Result:** 801 passed on each interpreter.
   - **Test file used:** they executed `tests/test_experimental_ltb_cmc_evolution.py` as it was *before* three tolerances were widened. That edit was made between 13:14:02Z and 13:14:11Z. The 3.13 run had already finished; the 3.11 run was still in progress, but had imported the module during collection.
   - **Sources:** unchanged during these runs; the last source edit was at 12:59:07Z.
3. **Final runs on the final file state**, started 13:15:34Z, after the last source or test edit (13:14:11Z).
   - **What ran:** "targeted" means the new file plus the first solver's 50 tests. The runs went in the order targeted 3.13, full 3.13, targeted 3.11, full 3.11.
   - **Which files:** this report was retouched afterwards, between 13:23:42Z and 13:23:45Z, but the tests do not execute it.
   - **Scope of the 801 passes:** they refer to the checkout at HEAD `4f28a095e6401c31e0a90dfc4c35ae92cbc0592d` with the nine experiment files added as untracked files: 724 preexisting + 50 + 27.

```text
.venv/bin/python -B -W error -m pytest -q -p no:cacheprovider \
    tests/test_experimental_ltb_cmc_evolution.py tests/test_experimental_ltb_cmc.py
Python 3.13.12: 77 passed in 72.82 s

.venv311/bin/python -B -W error -m pytest -q -p no:cacheprovider \
    tests/test_experimental_ltb_cmc_evolution.py tests/test_experimental_ltb_cmc.py
Python 3.11.15: 77 passed in 71.31 s

.venv/bin/python -B -W error -m pytest -q -p no:cacheprovider
Python 3.13.12: 801 passed in 161.69 s

.venv311/bin/python -B -W error -m pytest -q -p no:cacheprovider
Python 3.11.15: 801 passed in 168.51 s
```

4. **Tree of commit `28a87a1`**, run on 2026-09-23 from 14:06:11Z. This happened after the end of the implementation task, in connection with the publication described under "Later events".
   - **Setup:** the commit's tree was extracted with `git archive`, and `PYTHONPATH` pointed to that copy. That tree is base `118b8f3` plus the nine files.
   - **Targeted:** 77 passed on both interpreters.
   - **Full suite, Python 3.13 only:** 702 passed and 29 skipped. The skips come from oracle and validation artifacts that are excluded by `.gitignore` and so were absent from the extracted tree.
   - No full 3.11 run was made on that tree.

The three tolerances widened between contexts 2 and 3 were:

- the knot-Richardson atol, from 3e-12 to 5e-12;
- the h=1e-3 profile bound, from 1e-10 to 2e-10;
- the clock Richardson tolerance, from 3e-9/3e-10 to 1e-8/1e-9.

They were widened because their margins over the observed errors were only
4–5x. Wall times are not performance benchmarks.

Environments:

- Python 3.13.12 with numpy 2.5.3, scipy 1.18.1, pytest 9.1.1;
- Python 3.11.15 with numpy 2.4.6, scipy 1.17.1, pytest 9.1.1.

This Linux cloud environment does not have the user's Windows Python 3.14.
The full-suite total of contexts 2 and 3 is 724 preexisting tests, plus the
50 tests of the first solver, plus the 27 new tests. The 50 tests of the
first solver pass unchanged after the `solver.py`/`clock.py` refactoring.

Other executed checks:

- all new and modified files: no trailing whitespace, tabs or CRLF, and every file ends with a newline;
- the tolerance audit quoted above;
- the SHA-256 and Git status checks below.

`git diff --check` does not apply here, because every touched file is
untracked. Historical validation scripts were not run, so that out-of-scope
artifacts are preserved.

## Numerical limits

- **Accuracy is bounded by the background.** The evolution coefficients use the background's C¹ piecewise-cubic collocation interpolants, so the accuracy of K_ss and the profiles is bounded by the background `bvp_tol`. The observed default-vs-TIGHT difference in K_ss (5.5e-10) reflects this.
- **Conditioning of K_ss.** K_ss is fixed through the centre condition and `phi(0)`; a small `phi_center` signals poor conditioning. No uniform conditioning bound is claimed. Large tilt, thin transitions, large scale separation or an exponentially small central w0 can make the solve fail, as in the first solver.
- **Scope of the checks.** The checks are on samples (nodes, midpoints, check grid and quadrature points). They do not prove bounds between samples.
- **Representability.** Representable background outputs do **not** imply representable evolution outputs.
  - **Why.** The new outputs carry their own powers of s_c. In particular K_ss scales as s_c**-3, while the background volume V scales as s_c**3. So the background can be accepted while restoring K_ss to physical units leaves the normal binary64 range.
  - **How the code handles it.** The code already covers this case: `dimensional` raises `LTBNumericalError("Dimensional output outside normal binary64 range")`, and no partial evolution is returned.
  - **Counterexample**, reproduced in the independent review; it is not a new execution made for this correction:
    - s_c=2e-103, m0=0.2*s_c, kappa_star=0.2, r_c=0.25, r_o=0.7, G=1.7, with explicit units and default `Numerics`;
    - the background was accepted, with V ≈ 3.7455948021e-308;
    - the evolution raised `LTBNumericalError` "Dimensional output outside normal binary64 range".
  - **Consistency with this report.** The numbers match, by arithmetic only, the scalings of the s_c=1 values: V/s_c**3 ≈ 4.682 (first report) and K_ss*s_c**3 ≈ -4.058 (this report). Together they give |K_ss| ≈ 5.1e308 at that age, above the binary64 maximum of about 1.8e308.
  - **Not covered by the tests.** `test_representability_policy` uses scales at which the background itself already fails, plus `_signed_product`, so it does not reach this window.

  (Corrected 2026-09-24: an earlier version stated that the new outputs are representable within the representable range of the background outputs, and that the background fails first outside it. That statement was wrong.)
- **No sweep.** There is no claim over the whole parameter domain and no temporal or parameter scan. The nearby-age steps are test tools only.

## Contract review and discrepancies

Every contract formula was re-derived before implementation, and no concrete
sign, factor or boundary-condition contradiction was found:

- the flat values;
- the centre limits (they require kappa≡0 near r=0, which r_c>0 guarantees);
- `U_s(0)`, `d_s`, `e_s`;
- `kperp_s` (from `kperp=-(gamma*Hperp+xi*F/R)`);
- `Hparallel_age`;
- the J_s formula and the Raychaudhuri reduction;
- both alpha_dot forms, H_D_dot, J_D and q_required;
- the two propagation identities.

Remarks, none of which is a contradiction:

1. `Hparallel_age`, `A_s` and `R_s` appear in the contract but are only implicitly needed: A_s and R_s enter through `d_s` and `e_s`.
2. The lambda_s boundary checks are consequences of the imposed conditions, as noted above.
3. The centre values assume that the section's central worldline is always at age s_c. This is implied by `S(s_c,0)=s_c`.

## State at the end of the implementation task, and firewall

- HEAD is unchanged at `4f28a095e6401c31e0a90dfc4c35ae92cbc0592d`.
- There was no commit, stage, merge, push, stash, reset, checkout or history operation during the implementation task.
- The final Git status has only untracked entries: the six first-experiment files (three of them modified as described) plus the three new files.
- SHA-256 is unchanged for `geometry.py`, `tests/test_experimental_ltb_cmc.py`, `reports/experimental_ltb_cmc.md`, `scientific_status.py` and `README.md`.

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

Still not implemented:

- root finding on f, b or C;
- fitting and temporal or parameter scans;
- changes to the kappa profile or the anchors;
- the bang-time limit;
- Q_lambda_s and R_lambda_s;
- perturbations between geometries and the H1 response;
- nu_W and the boost;
- RSD, sigma8 and fsigma8;
- identification of the core with the whole wall or with finite infinity;
- use of the dressed geometry as an Einstein dust solution;
- integration into main.

Phase 1F-D is not declared complete.

## Later events (not part of the implementation task)

1. **Publication, 2026-09-23**, after the implementation task and on the user's explicit request.
   - Commit `28a87a18aed9f85a0e65624fea76b26dfd459a0f` (parent `586a1fb`) contains the nine files.
   - It was created with a temporary index, leaving the current branch, index and working tree untouched.
   - It was pushed to `experiment/ltb-cmc-background`. This is the publication referred to in `NOTA_EXPORT.md` of the export.
   - That commit contains the version of this report *before* the documentary corrections.
   - It is neither a tag nor a frozen checkpoint.
2. **Export, 2026-09-24.** The archive `ltb_cmc_export_20260924.zip` was created outside the repository.
   - It holds the nine files, `MANIFEST.sha256`, local Git provenance and the existing test logs.
   - During the export there was no commit, stage, push, fetch or remote operation.
   - The archive also contains the pre-correction version of this report. It is preserved unchanged.
3. **Documentary correction, 2026-09-24.** Only this file was changed.
   - The corrected report is local and untracked. It is contained neither in `28a87a1` nor in the export archive.
   - There was no commit, stage, merge, push, fetch or history change.

No new frozen checkpoint is promoted by these events. The relationship
between `118b8f3` and the current history has still to be examined. Local
ancestry is recorded in the export provenance: `118b8f3` is an ancestor of
both `586a1fb` and HEAD, and neither of those two is an ancestor of the
other. That ancestry is not a judgement on the status of `118b8f3`.
