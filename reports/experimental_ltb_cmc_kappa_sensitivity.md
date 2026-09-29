# LTB--CMC experiment: single-age sensitivity to kappa_star

## Provenance, scope and status

Date: 2026-09-24. This extends the isolated conditional LTB--CMC
experiment of `reports/experimental_ltb_cmc.md`. It adds the partial
derivative with respect to `kappa_star`, `delta = d/dkappa_star`, of **one
accepted background** at a single central age.

**What is held fixed.** The derivative is taken with `s_c`, `m0`, `r_c`,
`r_o`, `G`, the material labels r and the domain [0,1] all held fixed.
The profile obeys `kappa(r) = kappa_star*chi(r)` with the already selected
chi profile. At `kappa_star = 0` it is a right derivative, because the model
domain is `kappa_star >= 0`.

This is not:

- a remediation;
- the completion, revision or integration of Phase 1F-D;
- a perturbation towards a physically different Timescape geometry;
- an H1 response;
- a mass-compensated family: m0 is not adjusted to conserve the total mass;
- a generalization to a new function m(r).

Out of scope and not implemented:

- `delta_P_lambda` and the sensitivity of the evolution system;
- nu_W, H1 and a zero-perturbed-pressure closure;
- fitting, root finding, scans and all-time matching;
- RSD, sigma8 and fsigma8.

Every assumption of the first solver is unchanged:

- GR with Lambda=0;
- geodesic irrotational dust;
- spherical symmetry;
- simultaneous bang and the expanding branch;
- `m=m0*r**3` and `2*E_LTB=r**2*kappa`;
- `S(s_c,0)=S(s_c,1)=s_c`.

Classification of all new results: `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`.
The linearized equations below are conditional research derivations. They
are built on published relations:

- [Sussman, arXiv:1002.0173v2](https://arxiv.org/pdf/1002.0173v2) (S10), Eqs. (1)--(3), (5)--(7), (A.1);
- [Gourgoulhon, gr-qc/0703035](https://arxiv.org/pdf/gr-qc/0703035) (G07), Eqs. (4.63), (6.90);
- [Buchert--Mourier--Roy, arXiv:1912.04213v2](https://arxiv.org/pdf/1912.04213v2) (BMR), Eqs. (4.5), (4.9), (4.12), (4.16), (4.18), (4.20).

They are not published theorems and are not derived from the frozen
Timescape runtime. The preserved statuses are listed at the end. No frozen
scientific status or checkpoint is promoted, and Phase 1F-D is not declared
complete.

## Documentary corrections (2026-09-25)

Three passages of this report were corrected. These are corrections of the
**report text only**. They change neither the method nor the tests, nor the
code as tested on 2026-09-24, whose SHA-256 values are listed under "Test
results".

1. **`__init__.py` description.** The change was described as "additions
   only". In fact two import lines were added and the last line of `__all__`
   was extended; every preexisting export is preserved. The correction
   appears in "Files" and in "Final state and firewall".
2. **Scope of the normal-binary64 policy.** It applies to the outputs that
   undergo dimensional rescaling. The dimensionless outputs are only required
   to be finite. The correction appears in "Algorithm and gates", step 4.
3. **Measure variation.** "`eta_s = Theta`" is replaced by
   "`partial_s ln(A*R**2) = Theta`". The shift therefore contributes
   `Theta*delta_S` to the measure variation `eta`. The correction appears in
   "Contract review", remark 3.

**A separate code change, not documented here.** The 2026-09-25
mixed-sensitivity task refactored `kappa_sensitivity.py` internally, to
expose its accepted state for reuse: `_sensitivity_state`, `_KappaState` and
`_LapseVariations`. The public outputs were verified bit-identical to the
code tested here. That change is documented in
`reports/experimental_ltb_cmc_mixed_sensitivity.md`, not in this report.

## State verified before any modification

Recorded at 2026-09-24T20:52:20Z:

- branch `claude/loving-dijkstra-esoj6f`;
- HEAD `4f28a095e6401c31e0a90dfc4c35ae92cbc0592d`;
- the local ref `origin/main` also points to `4f28a09`. It was not re-checked remotely;
- nothing staged and no tracked modification;
- nine untracked files: the five experiment modules, the two experiment test files and the two experiment reports;
- git-ignored `__pycache__` directories left by earlier sessions in several other packages. They were not touched.

Both interpreters import the package from this checkout's `src/`:

| Interpreter | numpy | scipy | pytest |
|---|---|---|---|
| `.venv`, Python 3.13.12 | 2.5.3 | 1.18.1 | 9.1.1 |
| `.venv311`, Python 3.11.15 | 2.4.6 | 1.17.1 | 9.1.1 |

Sources used, with their SHA-256 before modification:

```text
f8e431e1ebc31c4be0aa4b4b4deff7f79654c38cf6a61399666ff846e93c81f7  src/timescape_fsigma8/experimental_ltb_cmc/geometry.py
29e5bf7205cfd78778465e47c4332190a52fef8e092ce56829d223c3c746d980  src/timescape_fsigma8/experimental_ltb_cmc/solver.py
ecc8d5495dff4d17dbe2c11c3d052207406cd8eced3d27c4d678c7614d1d9ac1  src/timescape_fsigma8/experimental_ltb_cmc/clock.py
900c8007fa464b0c5e8be3be5ed5421373f525e6a6970a81333f4bf4df0c6b46  src/timescape_fsigma8/experimental_ltb_cmc/evolution.py
41dfeeeddb53c1708f881a5d6144938c513cf216e833a5ba9be17a8308baa671  src/timescape_fsigma8/experimental_ltb_cmc/__init__.py
33fcf4664ecf87d3dc81cf79ff2f44dd5daf05f34a6c305db3335299daa3810d  tests/test_experimental_ltb_cmc.py
dcbfec4641d00786c2f8384b180d1412b7036c695a84a4e83fe9ac9909bec120  tests/test_experimental_ltb_cmc_evolution.py
f7e017ea4f57909c213449ae0e813c249ec9105279b597a4db06f1304508750b  reports/experimental_ltb_cmc.md
73a8da5686d0718ea9080d05452ce7dcce82fa805d66016ddee72c1b51efe41d  reports/experimental_ltb_cmc_evolution.md
16bef0c8f2cdd3ad5dead6d07555fbe2c3061930bbc2dd519e0d1ad0379544a8  src/timescape_fsigma8/scientific_status.py
2160a13506042cf7d735e9fadc91e957bffe166c9875c2bd235cd613173a1de3  README.md
```

The seven Python files match the `MANIFEST.sha256` of the 2026-09-24
export; the evolution report is its documentarily corrected version. The new
module depends only on `geometry.py` and `solver.py`.

**Isolated baseline.**

- **The snapshot.** A snapshot of the whole checkout was made in the session scratchpad, outside the repository, with `tar` excluding `.venv`/`.venv311`. It includes `.git` and the git-ignored artifacts, and has 459 files outside `.git`.
- **How it was run.** Both interpreters ran there with `PYTHONPATH=<snapshot>/src` and the snapshot as working directory. The package imports were verified to resolve into the snapshot.
- **Commands:**

  ```text
  PYTHONPATH=<snapshot>/src .venv/bin/python    -B -W error -m pytest -q -p no:cacheprovider
  PYTHONPATH=<snapshot>/src .venv311/bin/python -B -W error -m pytest -q -p no:cacheprovider
  ```
- **Results:**

  | Interpreter | Started | Result |
  |---|---|---|
  | Python 3.13.12 | 20:53:04Z | 801 passed in 204.95 s, exit 0 |
  | Python 3.11.15 | 20:56:30Z, after the first | 801 passed in 213.76 s, exit 0 |
- **Isolation verified.** The snapshot's SHA-256 listing was identical before and after both runs. The baseline is therefore isolated from every later edit of the checkout.
- **No assumed counts.** No historical count or checkpoint was assumed; 801 is the observed count.

## Files

New:

```text
src/timescape_fsigma8/experimental_ltb_cmc/kappa_sensitivity.py
tests/test_experimental_ltb_cmc_kappa_sensitivity.py
reports/experimental_ltb_cmc_kappa_sensitivity.md
```

Modified:

- **`geometry.py`**, by additions only, the geometric supports:
  - `chi_profile(r, model)`;
  - the frozen record `LocalKappaTerms`;
  - `Geometry._integral5`;
  - `Geometry.kappa_terms(s, r)`.

  `curvature`, `Geometry.at` and every preexisting line are unchanged; a diff against the previous version shows no removed lines.
- **`__init__.py`**: exports `KappaSensitivity`, `KappaSensitivityResiduals` and `solve_kappa_sensitivity`. Two import lines were added and the last line of `__all__` was extended: it was replaced by the same line with a trailing comma, plus a new line with the three new names. Every preexisting export is preserved. (Corrected 2026-09-25: an earlier version called this change "additions only".)

Unchanged: `solver.py`, `clock.py`, `evolution.py`, the two preexisting
experiment test files and reports, `scientific_status.py`, README, the
dependencies and every Phase 1F-D file. Phase 1F-D files are absent from
this environment. The existing APIs stay separate: the new module imports
neither `clock` nor `evolution`.

## API and dimensions

```python
from timescape_fsigma8.experimental_ltb_cmc import solve_kappa_sensitivity
sens = solve_kappa_sensitivity(s_c=1.0, model=model, numerics=num)
```

`KappaSensitivity` holds:

- the accepted background `solution`, solved once;
- `one_sided`, which is True at `kappa_star=0`;
- `delta_K_star` [length^-1] and `delta_K_s` [length^-2];
- read-only profiles on `solution.r`:
  - `delta_S` [length];
  - `delta_xi`, `delta_gamma`, `delta_N_c`, `delta_lambda` [dimensionless];
- `delta_ln_V`, `delta_ln_M_rest`, `delta_ln_rho0` [dimensionless];
- `delta_J` [length^-1];
- `delta_rho_lambda` [mass/length^3];
- `delta_Q_lambda` and `delta_R_lambda` [length^-2];
- `KappaSensitivityResiduals`.

Since kappa_star is dimensionless, each delta has the dimensions of its
quantity. No sign is imposed on any output. There is no embedding,
existence, H1 or observable field. The error handling follows the package
policy:

- `LTBDomainError` means invalid input;
- `LTBNumericalError` means a numerical, check or representability failure;
- no partial sensitivity is ever returned.

## Analytic geometric sources

All quantities are in the background's internal units: lengths divided by
`s_c`, with `m = m0/s_c`.

- **Prefix `d_`**: `d/dkappa_star` at fixed dust age s and fixed r, with `d(kappa) = chi` and `d(kappa_r) = chi_r`.
- **Suffix `_s`**: the dust proper-age derivative at fixed r.

`chi` and `chi_r` come from `chi_profile`, which evaluates the fixed logistic
shape directly, never as `kappa/kappa_star`.

The age equation S10 (2), `I(a,k) = int_0^a da'/sqrt(2m/a'+k) = s`, is
differentiated twice in `k`:

```text
a_k  = -I_k/I_a = (a_s/2) * int_0^a (2m/a'+k)**(-3/2) da'             (first solver)
a_kk = -(I_aa*a_k**2 + 2*I_ak*a_k + I_kk)/I_a
     = -m*a_k**2/(a**2*a_s**2) + a_k/a_s**2 - (3/4)*a_s*int_0^a (2m/a'+k)**(-5/2) da'
I_a = 1/a_s, I_aa = m/(a**2*a_s**3), I_ak = -1/(2*a_s**3)
a_sk  = (1 - 2*m*a_k/a**2)/(2*a_s)
a_skk = -m*(a_kk/a**2 - 2*a_k**2/a**3)/a_s - a_sk**2/a_s
```

- **Numerical evaluation of the new integral.** Substituting `a' = a*z**2`, it becomes `2*a*(a/(2m))**(5/2) * int_0^1 z**6/(1+h z**2)**(5/2) dz`, with `h = k*a/(2m)`. It is evaluated with the same Gauss orders 2n and n as the first solver. If they disagree by more than `8*age_rtol`, `LTBNumericalError` is raised.
- **Parabolic limit, k=0.** Here the formulas are analytic: `a_k = a**2/(10*m)` and `a_kk = -3*a**3/(350*m**2)`.

Fixed-age variations, with `R = r*a`, `R_r = a + r*a_k*kappa_r`,
`R_rs = a_s + r*a_sk*kappa_r` and `F = sqrt(1+r**2*kappa)`:

```text
d_a = chi*a_k,  d(a_k kappa_r) = chi*a_kk*kappa_r + a_k*chi_r
d_R_r = d_a + r*d(a_k kappa_r),  d_R_rs = chi*a_sk + r*(chi*a_skk*kappa_r + a_sk*chi_r)
d_ln_F = r**2*chi/(2*F**2),      d_A = A*(d_R_r/R_r - d_ln_F)
d_Hp = (chi*a_sk - Hp*d_a)/a,    d_Hl = (d_R_rs - Hl*d_R_r)/R_r,  d_Theta = d_Hl + 2*d_Hp
d_ln_rho = -2*d_a/a - d_R_r/R_r
d_e = d(a_k kappa_r)/a - e*d_a/a                      (e = R_r/R - 1/r = a_k*kappa_r/a)
d_sigma2 = (2/3)*(Hl-Hp)*(d_Hl-d_Hp)
d_R_u = -2*d_nu/(a**2*R_r) - R_u*(2*a*d_a*R_r + a**2*d_R_r)/(a**2*R_r)
d_nu = 3*chi*a + 3*kappa*d_a + r*(chi_r*(a+kappa*a_k) + kappa_r*(2*chi*a_k + kappa*chi*a_kk))
```

Dust-age derivatives:

```text
Hp_s = -m/a**3 - Hp**2
Hl_s = -4*pi*G*rho + 2*m/a**3 - Hl**2
Theta_s = -D,  D = Theta**2/3 + 2*sigma2 + 4*pi*G*rho
(ln rho)_s = -Theta,  A_s = A*Hl
e_s = kappa_r*(a_sk - a_k*Hp)/a                       (regular: no 1/r)
sigma2_s = (2/3)*(Hl-Hp)*(Hl_s-Hp_s)
R_u_s = -2*(3*kappa*a_s + r*kappa_r*(a_s + kappa*a_sk))/(a**2*R_r) - R_u*(2*Hp + Hl)
```

The total variation on the section at fixed r is
`delta_X = d_X + X_s*delta_S`. For r <= r_c, chi = 0 exactly, so every `d_X`
vanishes there and the centre is exactly EdS.

## Linearized CMC problem

The first solver's G07 (4.63) reduction is:

```text
S_r = A*xi/gamma
xi_r = -A*(K + gamma*Theta) - 2*e*xi - 2*xi/r
gamma = sqrt(1+xi**2)
```

It is linearized in the unknowns `delta_S`, `delta_xi` and the
eigenparameter `delta_K`:

```text
delta_S_r  = delta_A*xi/gamma + A*delta_xi/gamma**3
delta_xi_r = -delta_A*(K+gamma*Theta) - A*(delta_K + delta_gamma*Theta + gamma*delta_Theta)
             - 2*delta_e*xi - 2*e*delta_xi - 2*delta_xi/r
delta_A = d_A + A*Hl*delta_S,  delta_Theta = d_Theta - D*delta_S,  delta_e = d_e + e_s*delta_S
delta_gamma = xi*delta_xi/gamma
delta_S(0) = delta_S(1) = delta_xi(0) = 0
```

**Central regularity.** It is treated analytically:

- `-2*delta_xi/r` uses SciPy's singular-matrix mechanism, with `S = diag(0,-2)`, exactly as the background.
- The right-hand side is finite at r=0, where it reduces to `delta_xi_r(0) = -A(0)*delta_K/3`.
- So `lim delta_xi/r = -a_center*delta_K/3`, consistent with differentiating the background limit `-a_center*(K+2/s_c)/3` at a fixed central age.

**Mesh and start.** The solve starts on the accepted background CMC mesh from zero with `p = 0`, and uses the explicit `Numerics` tolerances.

## Linearized lapse problem

The first solver's G07 (6.90) flux problem is:

```text
N_r = d*z
z_r = e2*(U*N_c - K_s) - 2*z/r
d = B/a**2,  e2 = B*a**2,  B = A/gamma
```

The flux `z` is rebuilt from the same superposition `gamma_b*w0 + K_s*phi`
as N_c. The problem is linearized in `delta_N_c`, `delta_z` and
`delta_K_s`:

```text
delta_N_r = d*delta_ln_d*z + d*delta_z
delta_z_r = e2*delta_ln_e2*(U*N_c-K_s) + e2*(delta_U*N_c + U*delta_N_c - delta_K_s) - 2*delta_z/r
delta_ln_d  = delta_A/A - delta_gamma/gamma - 2*delta_a/a
delta_ln_e2 = delta_A/A - delta_gamma/gamma + 2*delta_a/a,   delta_a = d_a + a_s*delta_S
delta_kperp = -(delta_gamma*Hp + gamma*delta_Hp + delta(xi/r)*F/a + (xi/r)*(F/a)*(d_ln_F - delta_a/a))
delta_kpar  = delta_K - 2*delta_kperp
delta_U = 2*kpar*delta_kpar + 4*kperp*delta_kperp
          + 4*pi*G*rho*(delta_ln_rho*(2*gamma**2-1) + 4*gamma*delta_gamma)
delta_N_c(0) = 0,  delta_z(0) = 0,  delta_N_c(1) = delta_gamma(1)
delta_lambda = delta_N_c/gamma - lambda*delta_gamma/gamma
```

**Centre.** `delta_kperp(0) = delta_K/3` and `delta(xi/r)(0) = -a_center*delta_K/3`, so no 0/0 is evaluated.

**Boundary conditions.** They follow from the fixed anchors. `N_c(0) = 1`
holds because the central age is `s_c` for every section. `N_c(1) = gamma(1)`
holds because `lambda(1) = 1`.

**How `delta_K_s` is fixed.** By the same argument as the evolution BVP: a
difference solves `L[delta_N] = delta(delta_K_s)` with homogeneous data, is
proportional to phi, and `phi(0) > 0` forces uniqueness. This is not a
conditioning bound; `phi(0)` is exported as `phi_center`.

**Mesh.** The solve starts on the union of the background lapse mesh and the linearized CMC mesh.

## Averages with the variation of the measure

The intrinsic measure is `dmu = 4*pi*A*R**2 dr` (BMR, A not B). Its total
variation is `eta = delta_A/A + 2*delta_R/R`, with `delta_R/R = delta_a/a`.
For every average:

```text
delta<X> = <delta_X> + Cov(X, eta)          (centred covariance)
```

The averaged sensitivities are then:

```text
delta_ln_V      = <eta>
delta_ln_M_rest = <rho*(eta + delta_ln_rho)>/<rho>,   delta_ln_rho0 = delta_ln_M_rest - delta_ln_V
delta_J         = (<delta_E> + Cov(E, eta))/3,  E = lambda*Theta, delta_E = delta_lambda*Theta + lambda*delta_Theta
delta_rho_lambda = <2*lambda*delta_lambda*rho + lambda**2*rho*delta_ln_rho> + Cov(lambda**2*rho, eta)
delta_Var(E)    = 2*<(E-<E>)*delta_E> + Cov((E-<E>)**2, eta)
delta_Q_lambda  = (2/3)*delta_Var(E) - 2*delta<lambda**2*sigma2>
delta_R_lambda  = <2*lambda*delta_lambda*R_u + lambda**2*delta_R_u> + Cov(lambda**2*R_u, eta)
```

Here `delta_sigma2 = d_sigma2 + sigma2_s*delta_S`,
`delta_R_u = d_R_u + R_u_s*delta_S` and
`delta_ln_rho = d_ln_rho - Theta*delta_S`.

The averages use Gauss--Legendre orders n and 2n on [0,r_c], [r_c,r_o] and
[r_o,1]; the 2n value is accepted. All averages are computed directly. None
is obtained from an identity.

## Algorithm and gates

1. **One background solve.** `_checked_background` performs the single accepted background solve, with all of the first solver's gates. It is not re-solved; a test counts `_solve_background` calls. No finite difference and no second solve is used in production.
2. **Linearized CMC BVP**, then the **linearized lapse BVP**. Both run on SciPy `solve_bvp`, with the forward-difference Jacobian and explicit `bvp_tol`, `bc_tol` and `max_nodes`. Non-convergence raises.
3. **Post-checks.** They run on the union of the sample grid, both node sets and their midpoints, and re-apply the background acceptance bounds. The gates, all in s_c-scaled variables, are:
   - both ODE pairs' residuals, each normalized by max(1, |terms|), at most `check_tol`;
   - `delta_S(0)`, `delta_S(1)`, `delta_xi(0)`, `delta_N_c(0)`, `delta_z(0)` and `delta_N_c(1)-delta_gamma(1)`: at most `4*bc_tol`;
   - `delta_lambda(0)` and `delta_lambda(1)`: at most `4*bc_tol*(1+|delta_gamma(1)|)`;
   - the n vs 2n quadrature agreement, at most `check_tol`;
   - three algebraic identities: the local mass identity, and the differentiated local and averaged Hamilton constraints;
   - J consistency with the accepted background.

   Any failure raises `LTBNumericalError`; nothing partial is returned.
4. **Physical outputs.** The normal-binary64 policy applies to the outputs that undergo dimensional rescaling through `dimensional`: `delta_K_star`, `delta_K_s`, the `delta_S` profile, `delta_J`, `delta_rho_lambda`, `delta_Q_lambda` and `delta_R_lambda`. Each nonzero value must lie in the normal binary64 range, independently of the background's acceptance. The dimensionless outputs are not rescaled and are only required to be finite. They are `delta_ln_V`, `delta_ln_M_rest`, `delta_ln_rho0` and the `delta_xi`, `delta_gamma`, `delta_N_c` and `delta_lambda` profiles. (Corrected 2026-09-25: an earlier version applied the normal-range wording to every output.)

The algebraic identities are:

- `delta_ln_rho + eta = -r**2*chi/(2*(1+r**2*kappa))`, because `rho*A*R**2 = 3*m0*r**2/(4*pi*G*F)` holds on every section (S10 (3));
- `(4/3)*Theta*d_Theta - 2*d_sigma2 + d_R_u = 16*pi*G*rho*d_ln_rho`, and the same identity for the `_s` derivatives;
- `6*J*delta_J = 8*pi*G*delta_rho_lambda - (delta_R_lambda + delta_Q_lambda)/2`.

All three are consequences of the construction. They check algebra and
measure handling, and **do not replace** the independent derivative checks
below.

## Verification

**How the finite differences are taken.** They are test tools only:
independent background solves at fixed `s_c`, `m0`, `r_c`, `r_o`, `G` and
labels r, with only `kappa_star` moved.

- **Steps:** `h = 4e-3, 2e-3, 1e-3`.
- **Formula:** central differences on curved models; a second-order forward rule at `kappa_star=0`.
- **Where compared:** at the knots `linspace(0,1,601)`, which belong to every TIGHT sample grid, so there is no interpolation.
- **TIGHT numerics:** `bvp_tol=1e-8, bc_tol=1e-12, check_tol=2e-6, initial_nodes=101, check_nodes=601, quadrature_order=48`.

**Independent verifications.** The observed values are:

- **Local geometric derivatives at fixed dust age** (all `d_*`, `chi*a_kk` against d(a_k), and `chi*a_skk` against d(a_sk)), on both curved models and on the flat model:
  - every FD error falls by ×4 per halving;
  - central Richardson errors are ≤ 5e-11 on O(1) values;
  - the one-sided Richardson at kappa_star=0 leaves an O(h³) remainder ≤ 3.5e-7.
- **Dust-age derivatives:** an FD in s with h=1e-4 agrees to O(h²), at most about 1e-7.
- **The limit of `a_kk`:** `a_kk(k -> 0+)` tends linearly to the analytic `-3a³/(350m²)`, with a defect of about 5e-6 at k=1e-5.
- **Flat limits** (kappa_star=0; s_c=1 and 1.3):
  - `delta_R_lambda = -6/a(s_c)**2` to 2e-16 relative;
  - `delta_Q_lambda` ≈ 1e-16 (asserted ≤ 1e-12/s_c**2);
  - `delta_ln_M_rest = -(3/2)*int r**4 chi dr` to 2e-16 (s_c=1) and 8e-16 (s_c=1.3) relative (scipy `quad`, separate scalar chi);
  - `delta_lambda(0) = delta_lambda(1) = 0`.
- **Rest-mass integral:** `delta_ln_M_rest` against `quad` of `d/dkappa_star int 3*m0*r**2/(G*F) dr` agrees to 2e-16 (BASE) and 3e-16 (second model).
- **Right derivative at kappa_star=0.** The second-order forward FD of all nine scalar quantities converges with ratios 3.90–4.00. The Richardson residual is about 0.6 of `rtol=1e-7`; the test allows `rtol=5e-7, atol=5e-9`, for the O(h³) remainder.
- **Curved scalars.** The models are BASE `(s_c,m0,kappa_star,r_c,r_o,G)=(1,.2,.2,.25,.7,1.7)` and the second model `(.7,.08,.4,.2,.8,2.3)`.
  - Error ratios per halving are 3.99–4.04 for all nine scalars.
  - Richardson errors are ≤ 3.6e-10 on BASE and ≤ 8e-10 on the second model, against values of O(0.1–10).
  - `delta_Q_lambda` (6.2e-5 and 3.8e-4) agrees to 2e-13 and 7e-12.
- **Curved profiles** (BASE, at the knots):
  - ratios 3.99–4.00;
  - Richardson errors: `delta_S` 4.5e-10, `delta_xi` 5.3e-9, `delta_gamma` 2.1e-11, `delta_N_c` 8.0e-11, `delta_lambda` 8.0e-11;
  - asserted with explicit atol, at least 5x the observed error.

  Below h≈5e-4 the background-solver noise, amplified by 1/h, dominates `delta_S`/`delta_xi`. No convergence is claimed there.

Representative TIGHT values (not predictions):

| Quantity | BASE, s_c=1 | second model, s_c=0.7 | flat (BASE, kappa_star=0), s_c=1 |
|---|---|---|---|
| delta_K_star | -0.51929 | -0.672755 | -0.713446 |
| delta_K_s | 0.246904 | 0.665168 | 0.218899 |
| delta_ln_V | 0.995519 | 1.17263 | 1.18112 |
| delta_ln_M_rest | -0.251119 | -0.217628 | -0.290947 |
| delta_ln_rho0 | -1.24664 | -1.39026 | -1.47207 |
| delta_J | 0.230419 | 0.283303 | 0.321892 |
| delta_rho_lambda | -0.029399 | -0.033006 | -0.045189 |
| delta_Q_lambda | 6.16445e-5 | 3.80397e-4 | ≈ 0 (-4.7e-17) |
| delta_R_lambda | -4.50628 | -7.64713 | -6.43660 = -6/a(1)² |

**Error sources, separated** (BASE, s_c=1). All differences are measured at the same age:

- **Linearized BVPs only.** Same TIGHT background, BVP numerics default vs TIGHT: |Δ| ≤ 1.3e-10 on the scalars and ≤ 8e-11 on the profiles.
- **Background only.** Default vs TIGHT background, TIGHT linearized BVPs: |Δ| ≤ 1.3e-10 on the scalars and ≤ 8e-11 on the profiles.
- **Quadrature only.** Order 16 vs 48 on the same background and BVPs:
  - `delta_K_star`, `delta_K_s` and all profiles are bit-identical;
  - the averages change by at most 5.7e-10;
  - the internal n vs 2n `quadrature` residual at TIGHT is 5.6e-13.

**Dimensions and representability.**

- **Homothety.** Scaling s_c and m0 by 1e-4 and 1e4, with G fixed, reproduces every dimensional power to 4.4e-13. This is a homothety check, distinct from the fixed-m0 derivative checks. (Linux record. On Windows, `delta_Q_lambda` reaches 4.9e-11; see the 2026-09-29 addendum.)
- **Scaling in G.** Multiplying G by 3 changes only `delta_rho_lambda`, by exactly 1/3; every other output is bit-identical.
- **Representability with an accepted background.** Take s_c=1e-50, m0=0.02*s_c, G=3.5e-210, kappa_star=0.2, r_c=0.25, r_o=0.7.
  - The background is accepted. Its largest density-type output is `rho(0) = 1.516e308`, below the binary64 maximum.
  - For this model `|delta_rho_lambda|` is about 1.37 times larger: 10^308.32.
  - `solve_kappa_sensitivity` therefore raises `LTBNumericalError("Dimensional output outside normal binary64 range")`, with no partial result.
  - The sensitivity outputs are thus checked on their own and not assumed representable because the background was.

**Numerical controls and failures.** The tests also cover:

- **Gates:** every residual gate and boundary value, plus read-only and finite profiles.
- **Fault injection** (`solve_bvp` monkeypatched in the new module only):
  - forced non-convergence of the CMC step raises "Sensitivity CMC BVP status";
  - forced non-convergence of the lapse step raises "Sensitivity lapse BVP status";
  - a perturbed eigenparameter is caught by "Unresolved sensitivity checks".
- **Propagated failure:** a background failure propagates.
- **Input errors:** invalid ages and types raise `LTBDomainError`, and `kappa_star < 0` is rejected by the model.
- **Firewall:**
  - no forbidden fields;
  - unchanged signatures of every preexisting API;
  - the new module imports neither `clock`, `evolution`, Phase 1F-D nor `scientific_status`;
  - unchanged status constants.

`scripts/audit_numerical_tolerances.py`: 540 comparisons in `tests/`, zero
missing explicit tolerances, 30 of them in the new file.

## Test results

All runs used bytecode and cache writes disabled and warnings as errors,
in the checkout at HEAD `4f28a095e6401c31e0a90dfc4c35ae92cbc0592d` plus
the untracked experiment files. They ran sequentially, starting at
2026-09-24T21:07:54Z. Dependencies were neither installed nor updated. The
state under test is recorded by these SHA-256 values; the same listing was
re-verified, unchanged, after the last run:

```text
3e642e99fb5aeb74057122b9691663b39cfbfcd0e76bd2262da84bc56a26b624  src/timescape_fsigma8/experimental_ltb_cmc/__init__.py
ecc8d5495dff4d17dbe2c11c3d052207406cd8eced3d27c4d678c7614d1d9ac1  src/timescape_fsigma8/experimental_ltb_cmc/clock.py
900c8007fa464b0c5e8be3be5ed5421373f525e6a6970a81333f4bf4df0c6b46  src/timescape_fsigma8/experimental_ltb_cmc/evolution.py
18e91aa2052329e0f53d81fb8b2cb9cad3d09f2746d58e2115b3389a3e0edaea  src/timescape_fsigma8/experimental_ltb_cmc/geometry.py
713f84ae710c9d63560c27f0ca04a95523465cd6fa87f83de541f7f2ec18d869  src/timescape_fsigma8/experimental_ltb_cmc/kappa_sensitivity.py
29e5bf7205cfd78778465e47c4332190a52fef8e092ce56829d223c3c746d980  src/timescape_fsigma8/experimental_ltb_cmc/solver.py
33fcf4664ecf87d3dc81cf79ff2f44dd5daf05f34a6c305db3335299daa3810d  tests/test_experimental_ltb_cmc.py
dcbfec4641d00786c2f8384b180d1412b7036c695a84a4e83fe9ac9909bec120  tests/test_experimental_ltb_cmc_evolution.py
d61a3d10b945f9af727fd4c1a9e91799ea5ef1d561e1e410022f075679219948  tests/test_experimental_ltb_cmc_kappa_sensitivity.py
```

```text
.venv/bin/python -B -W error -m pytest -q -p no:cacheprovider \
    tests/test_experimental_ltb_cmc_kappa_sensitivity.py tests/test_experimental_ltb_cmc_evolution.py \
    tests/test_experimental_ltb_cmc.py
Python 3.13.12: 104 passed in 190.46 s, exit 0

.venv/bin/python -B -W error -m pytest -q -p no:cacheprovider
Python 3.13.12: 828 passed in 289.75 s, exit 0

.venv311/bin/python -B -W error -m pytest -q -p no:cacheprovider \
    tests/test_experimental_ltb_cmc_kappa_sensitivity.py tests/test_experimental_ltb_cmc_evolution.py \
    tests/test_experimental_ltb_cmc.py
Python 3.11.15: 104 passed in 181.75 s, exit 0

.venv311/bin/python -B -W error -m pytest -q -p no:cacheprovider
Python 3.11.15: 828 passed in 290.82 s, exit 0
```

**What the counts are.** The 104 targeted tests are 27 new, 27 for the
evolution and 50 for the first solver. The 828 full-suite tests are the
isolated baseline's 801 plus the 27 new ones.

**What else was run, and when.** Before the final state, the new test file
was run alone on 3.13 twice.

1. **First run: stopped at the first failure (`-x`).** The flat-branch local check of `d_sigma2` failed. Its exact value is 0, and the one-sided Richardson leaves an O(h³) remainder of 1.8e-8, above the initial atol of 1e-8. That tolerance was recalibrated from the measured errors, and the rule stayed the same.
2. **Second run: 27 passed.** Three tolerances were then widened: the one-sided Richardson bound, the small-Q atol and the coarse-quadrature bound, each because its observed margin was below about 3x.

The final runs above are all after that edit. The scratch verification
scripts that produced the figures in "Verification" were run during the
work. They are test tools only and not part of the package.

Wall times are not performance benchmarks.

## Limits

- **Accuracy is bounded by the background.** The coefficients use the background's C¹ collocation interpolants and the age inversion. The accuracy of the sensitivities is bounded by the background tolerances, about 1e-10 here.
- **Conditioning is not bounded.** `delta_K` and `delta_K_s` are fixed through central conditions (`phi(0)` for `delta_K_s`). No uniform conditioning bound is claimed. Large tilt, thin transitions or large scale separation can make the solves fail, as in the first solver.
- **Scope of the checks.** They are sample-based and do not prove bounds between samples. The tolerances are engineering gates, not certificates.
- **The one-sided case.** Only the right derivative is defined at `kappa_star=0`. Its FD verification is one-sided and O(h²).
- **Only two curved models were checked.** No claim is made over the parameter domain. There is no scan, fitting or root finding.
- **Dimensionless outputs.** The `delta_ln_*` outputs are plain finite floats and the dimensionless profiles are stored unscaled, as in the background.
- **Representability.** It is checked for every dimensional sensitivity output separately. As the case above shows, background acceptance does not imply it.

## Contract review

Every requested formula was re-derived, and no concrete contradiction was found:

- the flat limits `a_k = a²/(10 m0)`, `a_kk = -3a³/(350 m0²)`, `delta_Q_lambda = 0` and `delta_R_lambda = -6/a(s_c)²`;
- the local identity `delta_ln_rho + eta = -r²chi/[2(1+r²kappa)]`;
- the boundary conditions of both linearized problems;
- `delta_lambda = delta_N_c/gamma - lambda*delta_gamma/gamma`.

Remarks:

1. **`delta_ln_rho0`** is derived as `delta_ln_M_rest - delta_ln_V`. It is not independent.
2. **The flat `delta_Q_lambda = 0`** holds only up to the background's representation of `lambda = 1`, which is about 1e-11. The observed value is about 1e-16.
3. **The local mass identity** is exact per section and independent of `delta_S`, because the shift terms cancel. On one side `(ln rho)_s = -Theta`. On the other `partial_s ln(A*R**2) = Theta`, since `A_s/A = Hparallel` and `R_s/R = Hperp`. The shift therefore contributes `Theta*delta_S` to the measure variation `eta` and `-Theta*delta_S` to `delta_ln_rho`. (Corrected 2026-09-25: an earlier version wrote this as "`eta_s = Theta`".)

## Final state and firewall

- HEAD is unchanged at `4f28a095e6401c31e0a90dfc4c35ae92cbc0592d`.
- Nothing is staged and no tracked file is modified.
- There was no commit, stage, merge, push, fetch, stash, reset, checkout, history change or dependency update.
- The final Git status has only untracked entries:
  - the nine preexisting experiment files;
  - the three new files (`kappa_sensitivity.py`, its test file and this report).
- **Re-verified after the runs, identical to the preflight SHA-256:**
  - `solver.py`, `clock.py`, `evolution.py`;
  - the two preexisting experiment test files;
  - the two preexisting experiment reports;
  - `scientific_status.py` and `README.md`.
- **Changed:** `geometry.py`, by additions only, and `__init__.py`, by two added import lines and one extended `__all__` line with every preexisting export preserved. (Corrected 2026-09-25.)
- **Preserved:** the git-ignored `__pycache__` directories of other packages were left as found. The isolated baseline snapshot lives only in the session scratchpad.

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

No frozen scientific status or checkpoint is promoted. Phase 1F-D is not
declared complete. The result is left local for review.

## Addendum: Windows homothety tolerance (2026-09-29)

On Windows 11, `test_dimensional_powers[0.0001]` and `[10000.0]` failed on
Python 3.14.3 (NumPy 2.5.2, SciPy 1.18.1) and on Python 3.11.9 (NumPy 2.4.6,
SciPy 1.17.1).

Measured on both Windows interpreters, identically at both scales:
- `delta_Q_lambda`: 4.94e-11 relative, 3.05e-15 absolute. The common gate
  (`rel=3e-11`, `abs=1e-15`) allows 1.8e-15.
- The other eight scalars: at most 4.65e-13 relative.
- The five profiles: at most 2.1e-14 absolute, against `atol=1e-13`.
- Scaling in G: `delta_rho_lambda` agrees to 3.5e-16; every other scalar is
  bit-identical.
- The final collocation mesh (1211 nodes) is identical in the scaled and
  unscaled solves. The difference therefore arises in floating-point
  evaluation, not in mesh selection. Its root cause was not investigated.

`delta_Q_lambda` is the kappa_star derivative of a centred variance. Its
absolute rounding floor is large relative to its small value (6.2e-5).

**Change (approved by the project owner).** On `win32` only, `delta_Q_lambda`
uses `rel=1e-10`, about twice the measured deviation. Everything else keeps
its original gate:
- the other eight scalars on Windows;
- all scalars on other platforms;
- the profile and G checks.

No solver code, equation or other tolerance changed. The two tests pass on
both Windows interpreters after the change.
