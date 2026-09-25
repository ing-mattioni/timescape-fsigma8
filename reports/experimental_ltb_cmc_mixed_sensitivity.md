# LTB--CMC experiment: single-age mixed sensitivity and delta_P_lambda

## Provenance, scope and status

Date: 2026-09-25. This extends the isolated conditional LTB--CMC
experiment:

- `reports/experimental_ltb_cmc.md`, the background;
- `reports/experimental_ltb_cmc_evolution.md`, the section-family evolution d/dc;
- `reports/experimental_ltb_cmc_kappa_sensitivity.md`, the sensitivity d/dkappa_star.

**What it adds.** The mixed sensitivity `delta(d/dc)` of **one accepted
background** at a single central age, and from it `delta_P_lambda`,
`delta_J_c` and `delta_q_c`.

**The derivatives.**

- `delta` is `d/dkappa_star` at fixed c = s_c, m0, r_c, r_o, G, material labels r and domain [0,1]. At kappa_star = 0 it is the right derivative. There is no mass compensation and no new m(r).
- `_c` is `d/dc` at fixed physical parameters along the CMC section family.
- In internal units the length scale L = s_c of the evaluated point stays fixed. Neither L nor m0/L is differentiated.

**Out of scope, and not implemented:**

- a new tracker adapter and the effective pressure in common time;
- fitting, scans, root finding and all-time matching;
- mass compensation or new m(r);
- nu_W, H1 and imposed constitutive closures;
- RSD, sigma8, fsigma8, and integration into main.

**Status.** Classification of all new results:
`DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`. The mixed equations are
conditional research derivations of the user contract. They are built on
G07 (gr-qc/0703035, Eqs. (4.63), (6.90)), BMR (arXiv:1912.04213v2, Eqs.
(4.5), (4.9), (4.12)) and S10 (arXiv:1002.0173v2, Eqs. (1)--(3)). They are
not published theorems and not derived from the frozen Timescape runtime.
No frozen scientific status or checkpoint is promoted, and Phase 1F-D is not
declared complete.

## Preparation: state and isolated baseline

The state and the hashes of the effective inputs were recorded at
2026-09-25T11:08:42Z:

- branch `claude/loving-dijkstra-esoj6f`, HEAD `4f28a095e6401c31e0a90dfc4c35ae92cbc0592d`;
- the local ref `origin/main` also points to `4f28a09`;
- nothing staged and no tracked modification;
- twelve untracked experiment files.

The twelve files are identical to the `MANIFEST.sha256` of the 2026-09-25
export. Their SHA-256 before modification:

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
f7e017ea4f57909c213449ae0e813c249ec9105279b597a4db06f1304508750b  reports/experimental_ltb_cmc.md
73a8da5686d0718ea9080d05452ce7dcce82fa805d66016ddee72c1b51efe41d  reports/experimental_ltb_cmc_evolution.md
6506d535b8b99ed3092ab7f61e936dddc076cacc1909a6b5064d8b1a3a54eaf3  reports/experimental_ltb_cmc_kappa_sensitivity.md
```

`scientific_status.py`, `README.md` and `pyproject.toml` were also recorded
before and verified afterwards.

| Interpreter | numpy | scipy | pytest |
|---|---|---|---|
| `.venv`, Python 3.13.12 | 2.5.3 | 1.18.1 | 9.1.1 |
| `.venv311`, Python 3.11.15 | 2.4.6 | 1.17.1 | 9.1.1 |

Both import the package from the checkout's `src/`.

**Isolated baseline.**

- **The snapshot.** A full copy of the checkout, without the venvs, was made in the session scratchpad, outside the repository. It has 462 files outside `.git`, and its listing is recorded.
- **How it was run.** The full suite ran there with `PYTHONPATH=<snapshot>/src` and `-B -W error -m pytest -q -p no:cacheprovider`, one interpreter after the other.
- **Results:**

  | Interpreter | Result | Time (UTC) |
  |---|---|---|
  | Python 3.13.12 | 828 passed in 161.62 s, exit 0 | 11:09:12Z–11:11:55Z |
  | Python 3.11.15 | 828 passed in 168.71 s, exit 0 | 11:11:55Z–11:14:45Z |
- **Isolation verified.** The snapshot listing was unchanged after both runs.
- **No assumed counts.** No historical count or checkpoint was assumed; 828 is the observed count.

## Files

New:

```text
src/timescape_fsigma8/experimental_ltb_cmc/mixed_sensitivity.py
tests/test_experimental_ltb_cmc_mixed_sensitivity.py
reports/experimental_ltb_cmc_mixed_sensitivity.md
```

Minimal internal refactors, to expose accepted states. Public signatures and
behaviour are unchanged:

- **`evolution.py`.**
  - `_evolve` now returns `_evolve_state(...).result`.
  - The new private record `_EvolutionState` holds the public `CMCEvolution`, the accepted SciPy solution (the dense interpolant of X and Z), the coefficient evaluator, and the internal `K_ss` and `gamma_s(1)`.
  - The private `_Coefficients` record also exposes intermediate section quantities it already computed: xi, a, Hp, Hl, Hp_age, F/a, xi/r, xi_r, gamma_r, lambda_r, v, v_c, xi_c, xi_c/r, kperp, kpar, kperp_c and kpar_c.
  - No arithmetic changed.
- **`kappa_sensitivity.py`.**
  - `_sensitivity` now returns `_sensitivity_state(...).result`, backed by the new private records `_KappaState` and `_LapseVariations`.
  - The lapse-variation expressions were moved, unchanged and in the same order, into `lapse_variations`. `lapse_terms` uses it.
- **`__init__.py`.** Two import lines were added and the last `__all__` line was extended with `MixedSensitivity`, `MixedSensitivityResiduals` and `solve_mixed_sensitivity`. Every preexisting export is preserved.

**Behaviour-identity check** (test tool; `refactor_identity.py` in the
export). The public outputs of the refactored code and of the preexisting
code, taken from the isolated snapshot, were compared field by field. There
were 0 differences over 790 fields in 9 cases:

- `solve_cmc_evolution` and `solve_kappa_sensitivity`, on BASE with TIGHT and with default numerics, on the second model with TIGHT, and on the flat model with TIGHT;
- `solve_evolution_at_tracker_clock`.

**Documentary corrections**, report text only, to
`reports/experimental_ltb_cmc_kappa_sensitivity.md`. These are not method
changes, and the kappa report now carries a section stating so:

1. the description of the `__init__.py` change (a line extended, exports preserved);
2. the scope of the normal-binary64 policy (outputs under dimensional rescaling; dimensionless outputs only finite);
3. "`eta_s = Theta`" replaced by "`partial_s ln(A*R**2) = Theta`", with the shift contribution `Theta*delta_S` to the measure variation.

**Unchanged:** `solver.py`, `clock.py`, `geometry.py`, the three preexisting
experiment test files, the first report, the evolution report
(`73a8da56…`), `scientific_status.py`, README, `pyproject.toml` and the
previous export archives. Phase 1F-D files are absent from this environment.

## Mixed BVP (contract)

Abbreviate N = N_c. The background and evolution quantities are
X = N_c, Z = z_c, K1 = K_s, K2 = K_ss, d = B/a², e = B·a², B = A/gamma, with
coefficient derivatives d_c, e_c, U_c. The kappa_star sensitivities are
n = delta_N, zeta = delta_z and k1 = delta_K_s. The unknowns are
MX = delta_X, MZ = delta_Z and MK2 = delta_K2:

```text
MX_r = d*MZ + delta_d*Z + d_c*zeta + delta_d_c*z
MZ_r = e*(U*MX - MK2) - 2*MZ/r + source
source = delta_e*(U*X-K2) + e*delta_U*X + delta_e_c*(U*N-K1) + e_c*(delta_U*N + U*n - k1)
         + delta_e*U_c*N + e*delta_U_c*N + e*U_c*n
MX(0) = 0,  MZ(0) = 0,  MX(1) = delta_gamma_c(1)
```

- **It is the kappa_star derivative of the evolution BVP.** The equations are exactly the kappa_star derivative of the evolution BVP, with every coefficient a total variation on the section.
- **Uniqueness.** The homogeneous problem is `L[MX] = MK2`, with a positive sign, so a difference of solutions is `delta_MK2*phi`. Then `MX(0) = 0` with `phi(0) > 0` fixes MK2. This is not a conditioning bound; `phi(0)` is exported as `phi_center`.
- **Centre.** `-2*MZ/r` uses SciPy's singular-matrix mechanism, as in the earlier solvers.

## Analytic sources

The sources use only the accepted background, evolution and kappa_star
states, plus the analytic local terms of `Geometry.kappa_terms`.

**How derivatives in r are obtained.** Each comes from its own equation,
never from differentiating interpolants of public sampled profiles:

- `delta_xi_r` from the linearized CMC equation, with the centre value `f(0)/3`;
- `delta_N_r = d*delta_ln_d*z + d*zeta`;
- `xi_r` and `lambda_r` from the evolution coefficients.

With `v = xi/gamma` and `delta_v = delta_xi/gamma**3`:

```text
delta_gamma_r = (delta_xi*xi_r + xi*delta_xi_r)/gamma - xi*xi_r*delta_gamma/gamma**2
delta_lambda_r = (delta_N_r - delta_lambda*gamma_r - lambda*delta_gamma_r - lambda_r*delta_gamma)/gamma
delta_v_c = delta_lambda_r/A - lambda_r*delta_A/A**2
            - (delta_v*Hpar*lambda + v*delta_Hpar*lambda + v*Hpar*delta_lambda)
delta_gamma_c = 3*gamma**2*delta_gamma*v*v_c + gamma**3*(delta_v*v_c + v*delta_v_c)
delta_xi_c = 3*gamma**2*delta_gamma*v_c + gamma**3*delta_v_c
delta_Hp_age = 3*m0*delta_a/a**4 - 2*Hp*delta_Hp
delta_kperp_c = -(delta_gamma_c*Hp + gamma_c*delta_Hp)
                - (delta_gamma*Hp_age*lambda + gamma*delta_Hp_age*lambda + gamma*Hp_age*delta_lambda)
                - (delta(F/a)*xi_c/r + (F/a)*delta_xi_c/r)
                + (delta_xi/r)*(F/a)*Hp*lambda
                + (xi/r)*(delta(F/a)*Hp*lambda + (F/a)*(delta_Hp*lambda + Hp*delta_lambda))
delta_kpar_c = delta_K1 - 2*delta_kperp_c
delta_U_c = 2*delta_kpar*kpar_c + 2*kpar*delta_kpar_c + 4*delta_kperp*kperp_c + 4*kperp*delta_kperp_c
            + 4*pi*G*rho*(delta_ln_rho*W + delta_W),   W = -Theta*lambda*(2*gamma**2-1) + 4*gamma*gamma_c
delta_d_c = delta_d*((Hpar-2*Hp)*lambda - gamma_c/gamma)
            + d*((delta_Hpar - 2*delta_Hp)*lambda + (Hpar-2*Hp)*delta_lambda
                 - delta_gamma_c/gamma + gamma_c*delta_gamma/gamma**2)
delta_e_c = delta_e*(Theta*lambda - gamma_c/gamma)
            + e*(delta_Theta*lambda + Theta*delta_lambda - delta_gamma_c/gamma + gamma_c*delta_gamma/gamma**2)
```

Every `delta_*` here is a total variation, `d_geom + (d/ds)*delta_S`, as in
the kappa_star module.

**Exact centre limits** (internal units, where m0 means m0/L):

```text
delta_gamma_c(0) = 0
delta_kperp_c(0) = delta_K1/3
delta_U_c(0) = (2/3)*(delta_K*K1 + K*delta_K1)
lim delta_xi_c/r = -(a_center/3)*((2/3)*delta_K + delta_K1)
lim delta_xi/r = -a_center*delta_K/3
```

Here `a_center = (9*m0/2)**(1/3)`. The `delta_xi_c/r` limit is the
kappa_star derivative of the evolution's centre limit; it holds because the
centre is exactly EdS, since chi = 0 for r ≤ r_c.

## Reconstruction and averages

```text
delta_lambda_c = (MX - lambda_c*delta_gamma - gamma_c*delta_lambda - lambda*delta_gamma_c)/gamma
delta_P_lambda = <delta_Theta*lambda_c + Theta*delta_lambda_c> + Cov(Theta*lambda_c, eta)
3*delta_J_c = delta_P_lambda - delta<lambda**2*D> + delta Var(E)
delta<lambda**2 D> = <2*lambda*delta_lambda*D + lambda**2*delta_D> + Cov(lambda**2*D, eta)
delta_D = (2/3)*Theta*delta_Theta + 2*delta_sigma2 + 4*pi*G*rho*delta_ln_rho
delta Var(E) = 2*<(E-<E>)*delta_E> + Cov((E-<E>)**2, eta),   E = lambda*Theta
delta_q_c = -delta_J_c/J**2 + 2*J_c*delta_J/J**3
```

- **Measure.** Only the intrinsic measure `4*pi*A*R**2 dr` is used, with `eta = delta_A/A + 2*delta_R/R`. The measure variation always enters.
- **No identity is imposed.** `delta_P_lambda` is averaged directly. It is not obtained by imposing Raychaudhuri.
- **No signs imposed.** No sign is imposed on any sensitivity.
- **Anchors.** `delta_lambda_c(0) = delta_lambda_c(1) = 0` follow from the boundary conditions and the anchors. They are checked, and they test only the reconstruction.

## Algorithm and gates

1. **One background solve.** `_checked_background` solves the background once. A test counts `_solve_background` calls.
2. **Accepted evolution and kappa_star states.** `_evolve_state` and `_sensitivity_state` produce them, with all their gates, on the same background object. A test counts one call each. Nothing is re-solved to recover missing quantities.
3. **The mixed BVP.** It runs on SciPy `solve_bvp`, from zero with `p = 0`, starting on the union of the evolution and lapse-sensitivity meshes. It uses the explicit `Numerics` tolerances. Non-convergence raises.
4. **Post-checks.** They run on the union of the sample grid, the mixed nodes and their midpoints, and re-apply the background acceptance bounds. The gates are:
   - the residuals of both ODEs, each normalized by max(1, |terms|), at most `check_tol`;
   - `MX(0)`, `MZ(0)` and `MX(1)-delta_gamma_c(1)`: at most `4*bc_tol`;
   - `delta_lambda_c(0)` and `delta_lambda_c(1)`: at most `4*bc_tol*(1+|delta_gamma_c(1)|)`;
   - the n vs 2n Gauss quadrature on the three segments, for delta_P, delta_J_c, delta<lambda²D> and delta Var(E);
   - the algebraic differentiated Raychaudhuri identity `3*(delta_J_c + 2*J*delta_J) + 4*pi*G*delta_rho_lambda - delta_Q - delta_P = 0`;
   - consistency of J, P_lambda, J_c, delta_J, delta_rho_lambda and delta_Q, recomputed here, with the accepted background, evolution and kappa_star values.

   Any failure raises; nothing partial is returned.
5. **Dimensional restoration.** The outputs are restored with `dimensional` (normal-binary64 policy):
   - `delta_K2`: length^-3;
   - `delta_N_c_c`, `delta_gamma_c`, `delta_lambda_c`: length^-1;
   - `delta_P_lambda`, `delta_J_c`, `delta_lambda2_D`, `delta_var_E`: length^-2.

   `delta_q_c` is dimensionless and only required to be finite.

## API

```python
from timescape_fsigma8.experimental_ltb_cmc import solve_mixed_sensitivity
mixed = solve_mixed_sensitivity(s_c=1.0, model=model, numerics=num)
```

`MixedSensitivity` holds:

- the accepted intermediates: `solution` (background), `evolution` (`CMCEvolution`) and `kappa` (`KappaSensitivity`);
- `one_sided`;
- `delta_K2`;
- the read-only profiles on `solution.r`: `delta_N_c_c`, `delta_gamma_c`, `delta_lambda_c`;
- `delta_P_lambda`, `delta_J_c`, `delta_q_c`, `delta_lambda2_D`, `delta_var_E`;
- `MixedSensitivityResiduals`: residuals, boundary values, quadrature, the algebraic Raychaudhuri identity, consistency, `phi_center` and nodes.

`LTBDomainError` means invalid input. `LTBNumericalError` means a numerical,
check or representability failure. There is no embedding, existence, H1 or
observable field.

## Verification

TIGHT numerics: `bvp_tol=1e-8, bc_tol=1e-12, check_tol=2e-6, initial_nodes=101,
check_nodes=601, quadrature_order=48`. Finite differences are test tools
only. Profiles are compared at the knots `linspace(0,1,601)`, common to every
TIGHT sample grid, so there is no interpolation. Steps are h = 4e-3, 2e-3
and 1e-3.

**Independent verifications.**

- **1. kappa_star differences of the preexisting evolution**, at fixed c and m0.
  - Models: BASE `(c,m0,kappa_star,r_c,r_o,G)=(1,.2,.2,.25,.7,1.7)` and the second model `(.7,.08,.4,.2,.8,2.3)`.
  - All four scalars and three profiles converge at second order, with ratios 3.8–4.2.

  | Model | K2 | P | J_c | q_c | Profiles N_c_c, lambda_c, gamma_c |
  |---|---|---|---|---|---|
  | BASE (Richardson) | 8.4e-10 | 9.6e-13 | 1.6e-11 | 8.0e-12 | 2.0e-11, 2.5e-11, 1.1e-11 |
  | second model (Richardson) | 1.0e-9 | 6.6e-12 | 2.9e-10 | 3.1e-12 | 4.7e-12, 2.9e-11, 2.5e-11 |
- **2. c-derivative of the preexisting kappa_star sensitivity**, at fixed physical parameters with m0 fixed.
  - Compared: `d/dc delta_K_s` against `delta_K2`, `d/dc delta_J` against `delta_J_c`, and `d/dc` of the profiles `delta_N_c`, `delta_lambda` and `delta_gamma`.
  - Ratios are ≈ 4.0.

  | Model | K2 | J_c | Profiles |
  |---|---|---|---|
  | BASE (Richardson) | 2.2e-11 | 4.3e-12 | ≤ 1.3e-12 |
  | second model (Richardson) | 1.8e-10 | 3.2e-12 | ≤ 3.0e-12 |

  Together, checks 1 and 2 confirm that the mixed partial derivatives commute from both directions.
- **3. Independent flat benchmark (user formula).**
  - **Method.** Built with scipy `quad` on a separate scalar chi, with analytic mu-derivatives of the kernels Phi and g. Neither the mixed BVP nor Raychaudhuri is used.
  - **Kernel accuracy.** The analytic kernel derivatives were checked against central differences in mu: clean O(h²), error ratio 4.00, at most 3.7e-9 at h=5e-4.
  - **Quadrature.** The error estimates are ≤ 5.8e-15.

  | (m0, c) | mu | Relative agreement of `delta_P_lambda` |
  |---|---|---|
  | (0.2, 1) | 1.365 | 1.5e-9 |
  | (0.2, 1.3) | 1.251 | 1.4e-9 |
  | (0.08, 0.7) | 1.133 | 1.3e-9 |

  The absolute differences are about 1e-13, and `delta_P_lambda` is of order 5e-5.
- **4. Right derivative at kappa_star=0.**
  - **P, J_c and q_c.** The second-order forward FD of the evolution converges with ratios 3.96–3.99. The Richardson residuals are 1.1e-10, 3.6e-9 and 5.4e-8, leaving an O(h³) remainder.
  - **K_ss is noise-limited.** Its forward FD is limited by background-solver noise: `K_ss` at kappa_star=2e-3 differs by 7.6e-11 between TIGHT and a tighter setting, and the forward rule amplifies this by about 2/h. The TIGHT ratios are therefore 4.90, 5.18, 2.30 and 7.25 for h = 1.6e-2 … 1e-3. With tighter numerics (`bvp_tol=1e-10`) they are 4.91, 4.55, 4.31 and 4.03, and `delta_K2` is unchanged to 1e-13. So only a bound, 1e-6, is asserted on the h=1e-3 FD of K_ss (observed 4.2e-8).
  - **`delta_K2` is checked cleanly instead.** It is checked through the flat c-derivative of `delta_K_s`, with ratio 4.000 and Richardson 8.7e-13.
- **5. Anchors.** `delta_lambda_c(0)` and `delta_lambda_c(1)` are ≤ 2.2e-15 on BASE and ≤ 1.9e-22 on the flat model. The flat model also checks `one_sided`.

Representative TIGHT values (not predictions):

| Quantity | BASE, c=1 | second model, c=0.7 | flat (BASE, kappa_star=0), c=1 |
|---|---|---|---|
| delta_K2 | -0.304654 | -1.342097 | -0.273453 |
| delta_P_lambda | -3.50306e-3 | -1.21473e-2 | 5.63357e-5 |
| delta_J_c | -0.124137 | -0.324420 | -0.107383 |
| delta_q_c | -0.609625 | -0.339016 | -1.206904 |
| max\|delta_N_c_c\| | 2.70e-3 | 5.83e-3 | |
| max\|delta_lambda_c\| | 2.73e-3 | 5.84e-3 | |

**Algebraic checks** (they do not replace the above). The differentiated
averaged Raychaudhuri identity holds to about 2e-17 (BASE). The consistency
of the recomputed J, P, J_c, delta_J, delta_rho_lambda and delta_Q with the
accepted values holds to about 3e-17.

**Error sources, separated** (BASE, c=1):

| Source | How isolated | Scalars | Profiles |
|---|---|---|---|
| BVPs (evolution, kappa_star and mixed) | same TIGHT background; default vs TIGHT numerics | ≤ 2.3e-10 (`delta_K2`), ≤ 2.1e-11 otherwise | ≤ 3.1e-12 |
| Background | default vs TIGHT background; TIGHT BVPs | ≤ 1.4e-10 | ≤ 1.5e-11 |
| Quadrature | order 16 vs 48 | the averages change by ≤ 6.6e-11 | `delta_K2` and profiles bit-identical |

The internal n vs 2n quadrature residual at TIGHT is 3.7e-13.

**Dimensions and representability.**

- **Homothety.** Scaling c and m0 by 1e-4 and 1e4 (G fixed) reproduces every dimensional power to 1.9e-13. It is distinct from the fixed-m0 derivative checks.
- **G.** No mixed output depends on G: they are bit-identical when G is multiplied by 3.
- **Representability of the new outputs, with accepted intermediates.** At c = 3e102 with m0 = 0.2·c, the background, the evolution and the kappa_star sensitivity are all accepted; V = 1.26e308, below the maximum. `delta_K2` ∝ c⁻³ would, however, be 1.1e-308, below the normal range. `solve_mixed_sensitivity` therefore raises `LTBNumericalError("Dimensional output outside normal binary64 range")`, with no partial result.

**Controls and failures.** The tests also cover:

- **Gates:** every residual gate and boundary value, and read-only profiles.
- **Accepted intermediates:** they equal the separately obtained evolution and kappa_star results.
- **The `delta_q_c` formula:** checked against the public intermediates.
- **Fault injection** (`solve_bvp` in the new module only): non-convergence raises "Mixed sensitivity BVP status"; a perturbed eigenparameter raises "Unresolved mixed sensitivity checks".
- **Propagated failure:** a background failure propagates.
- **Input errors:** invalid ages and types raise `LTBDomainError`.
- **Firewall:**
  - no forbidden fields;
  - unchanged public signatures;
  - no imports of clock, tracker, Phase 1F-D or `scientific_status`;
  - no `solve_cmc(`, `solve_cmc_evolution(`, `solve_kappa_sensitivity(` or `replace(` in the module;
  - unchanged status constants.

`scripts/audit_numerical_tolerances.py`: 558 comparisons in `tests/`, zero
missing explicit tolerances, 18 of them in the new file.

## Tolerances

The tolerances were set before the first run, from the measured errors
recorded above. Each keeps a margin of at least 5x over the observed values:

- Richardson residuals of second-order central differences;
- O(h³) remainders of the one-sided rule;
- solver-noise floors;
- rounding for bit-level identities.

They are engineering bounds, not rigorous certificates.

Two recalibrations were made, both to the kernel-derivative test:

| Comparison | Previous | Final | Reason |
|---|---|---|---|
| kernel FD check, monotonic guard | `errors[1] <= errors[0]` | `errors[1] <= errors[0] + 1e-14` | the g kernel is constant at r=0, so both errors are rounding-level. Changed **before any run**; the previous form was never executed. |
| kernel FD check, bound | `errors[1] < 1e-8` | `errors[1] < 3e-8`, plus the order test `3.5 < errors[0]/errors[1] < 4.5` (when errors[0] > 1e-12), replacing the monotonic guard | the first run passed, but the observed worst error was 3.7e-9, using 0.37 of the bound, a margin below 3x. The error ratio 4.00 shows clean O(h²) truncation, which is now asserted directly. |

## Test results

All runs used bytecode and cache writes disabled and warnings as errors.
Dependencies were neither installed nor updated. The full logs are kept and
are included in the export archive (`logs/`).

**State under test.** It was recorded before the final runs
(`tested_state.sha256`) and re-verified, unchanged, after the last run:

```text
622e1b3d974f2858148d5afeb76c6005f456f68bedde663d1fd3409cf799e97e  src/timescape_fsigma8/experimental_ltb_cmc/__init__.py
ecc8d5495dff4d17dbe2c11c3d052207406cd8eced3d27c4d678c7614d1d9ac1  src/timescape_fsigma8/experimental_ltb_cmc/clock.py
16b0c5983cca8947ea42535f92d4adc56bf00395b6f4ab8d4467dd9712d1a34f  src/timescape_fsigma8/experimental_ltb_cmc/evolution.py
18e91aa2052329e0f53d81fb8b2cb9cad3d09f2746d58e2115b3389a3e0edaea  src/timescape_fsigma8/experimental_ltb_cmc/geometry.py
e485e43141742b92b39636e884f182a752452fb400a5c70ebdf5baef0b5dacbf  src/timescape_fsigma8/experimental_ltb_cmc/kappa_sensitivity.py
3b6518ea16e27deb949102dc056316466abad6f3990bf886bed35889dc1f464a  src/timescape_fsigma8/experimental_ltb_cmc/mixed_sensitivity.py
29e5bf7205cfd78778465e47c4332190a52fef8e092ce56829d223c3c746d980  src/timescape_fsigma8/experimental_ltb_cmc/solver.py
33fcf4664ecf87d3dc81cf79ff2f44dd5daf05f34a6c305db3335299daa3810d  tests/test_experimental_ltb_cmc.py
dcbfec4641d00786c2f8384b180d1412b7036c695a84a4e83fe9ac9909bec120  tests/test_experimental_ltb_cmc_evolution.py
d61a3d10b945f9af727fd4c1a9e91799ea5ef1d561e1e410022f075679219948  tests/test_experimental_ltb_cmc_kappa_sensitivity.py
b576156d462a2a7a2c629d550114d3e9772459d044b0c0dc2f2c59a7ba8c73ce  tests/test_experimental_ltb_cmc_mixed_sensitivity.py
```

**Final runs.** They ran in the checkout at HEAD `4f28a09` with the
experiment files untracked, one after the other, starting at
2026-09-25T11:24:55Z. "Targeted" means the four experiment test files.

| Interpreter | Targeted | Full suite |
|---|---|---|
| Python 3.13.12 | 128 passed in 190.81 s, exit 0 | 852 passed in 243.05 s, exit 0 |
| Python 3.11.15 | 128 passed in 182.62 s, exit 0 | 852 passed in 239.19 s, exit 0 |

- **What the counts are.**
  - Targeted: 128 = 50 (first solver) + 27 (evolution) + 27 (kappa_star) + 24 (mixed).
  - Full suite: 852 = the isolated baseline's 828 + 24 new tests.
- **Previous APIs.** The previous experiment tests (104) pass unchanged on the refactored code.
- **Scope of the counts.** They refer to the checkout (HEAD `4f28a095e6401c31e0a90dfc4c35ae92cbc0592d` plus the untracked experiment files), not to an export archive alone.

**Development runs of the new file alone, on Python 3.13, before the final
state:**

1. **First run: 24 passed.** Console output only, complete within `| tail -30`, preserved as a transcript extract in the export.
2. **After the kernel-tolerance recalibration: 24 passed.** Logged in `dev_run_2.log`.

No failure occurred in this task's test runs. Wall times are not
performance benchmarks.

## Limits

- **Accuracy is bounded by the background and intermediate tolerances.** The coefficients use the C¹ collocation interpolants of the background, evolution and kappa_star states. The accuracy is about 1e-10 here.
- **Conditioning is not bounded.** MK2 is fixed through `phi(0)`, and no uniform conditioning bound is claimed. Large tilt, thin transitions or large scale separation can make any of the four solves fail.
- **Scope of the checks.** They are sample-based. The flat benchmark covers moderate mu only, and only two curved models were checked, with no scan.
- **The one-sided case.** At kappa_star=0 only the right derivative is defined. The forward FD of K_ss is noise-limited, as documented above.
- **Representability.** It is checked for each dimensional output separately. Acceptance of the background or of the intermediates does not imply it, as the case above shows.

## Contract review

No concrete contradiction was found. The following were re-derived:

- the mixed equations, as the kappa_star derivative of the evolution BVP;
- the positive sign of the homogeneous problem;
- the boundary and centre values, including `delta_U_c(0)`;
- the reconstruction formula for `delta_lambda_c` and its anchors;
- the averaged formulas and `delta_q_c`.

Remarks:

1. The contract's `delta_v = delta_xi/gamma**3` follows from `d(xi/gamma)/dxi = 1/gamma**3`.
2. The centre limit of `delta(xi_c/r)` is not listed in the contract; it follows from differentiating the evolution's centre limit.
3. The flat benchmark was reproduced to about 1e-9 relative. It is an independent confirmation, and was not used to build or tune the method.

## Final state and firewall

- HEAD is unchanged at `4f28a095e6401c31e0a90dfc4c35ae92cbc0592d`.
- Nothing is staged and no tracked file is modified.
- There was no commit, stage, merge, push, fetch, stash, reset, checkout, history change or dependency update.
- The final Git status has only untracked entries: the twelve preexisting experiment files and the three new ones, 15 in total.
- **Identical to the preflight SHA-256:**
  - `solver.py`, `clock.py`, `geometry.py`;
  - the three preexisting experiment test files;
  - the first report and the evolution report;
  - `scientific_status.py`, README and `pyproject.toml`.
- **Changed:**
  - `evolution.py` and `kappa_sensitivity.py`, by internal refactoring with verified bit-identical public outputs;
  - `__init__.py`, with exports added and none removed;
  - the kappa_star report, by documentary corrections only.
- **Earlier archives unchanged.** `ltb_cmc_export_20260924.zip` (`0dc20c49…`) and `ltb_cmc_kappa_export_20260925.zip` (`1a0a2d5b…`) were verified unchanged.
- **Where the baseline snapshot lives.** Only in the session scratchpad.

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
