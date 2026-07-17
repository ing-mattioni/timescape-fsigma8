# Phase 1C-B2 — Timescape barotropic perturbation validation

Date: 2026-07-17

Branch: `phase-1c-perturbations`

Starting/verified HEAD: `18b666648649ba1004f7f1219693bab8bc83bc7d`

Scientific specification: Galoppo & Mourier,
[arXiv:2511.17160v2](https://arxiv.org/abs/2511.17160) ([GM])

Equation audit: `reports/phase1c_perturbation_equation_audit.md`

## 1. Outcome and scientific status

Phase 1C-B2 independently implements the barotropic system of [GM]
Eqs. (4.13)–(4.17) using only the corrected Phase 1B background sound speed.
The unresolved Eq. (4.15) inconsistency is exposed as two mandatory choices:
`printed_4_15` and `derived_4_10`. Neither is ranked as correct, preferred,
canonical, or a scientific default. Both tilt variables are implemented
directly and require an explicit choice. Initial-rate, initial-epoch, and
wavenumber interpretations are likewise mandatory and have no defaults.

The pinned notebook trajectories are reproduced with their D2-corrupted
sound speed in an isolated, non-exported forensic harness. The worst
per-component normalized trajectory error is `2.834e-14`, well below the
`2e-8` reproduction gate, and the independent and upstream solver evaluation
counts agree exactly for all three modes.

The most important scientific result is sensitivity, not branch
adjudication. The strong scale-dependent growth exists in the notebook
oracle and in both corrected-background branches, but its magnitude is not
robust to D2, D3, the initial epoch, or the wavenumber normalization. At
`k=10*pi`, changing only D3 changes the corrected-background endpoint by
factors of order `10^2` relative to the `printed_4_15` value, and the modest
25.955% change in matrix `k` implied by the alternative normalization changes
the high-k endpoint by factors of order `10^5`–`10^6`. These rapidly growing
modes are numerically converged under the stated tests, but convergence does
not establish their physical applicability.

No f-sigma-8, sigma-8 normalization, likelihood, fitting, or author-contact
work was performed. Nothing was committed, tagged, pushed, or published.

## 2. Provenance preflight and read-only extraction

All required checks passed before implementation:

| check | value |
|---|---|
| repository branch | `phase-1c-perturbations` |
| repository HEAD | `18b666648649ba1004f7f1219693bab8bc83bc7d` |
| B1 tag at HEAD | `phase-1c-b1-clean-systems-v1` |
| root working tree before B2 | clean |
| pinned upstream commit | `590c6fd5332acb15f5683ebf392a0d7ce54983c5` |
| notebook path | `.reference/Linear-Perturbations-in-averaged-cosmological-models/ACPT_Timescape.ipynb` |
| validated notebook SHA-256 | `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a` |
| upstream clone before/after extraction | clean |

`scripts/extract_upstream_barotropic_oracle.py` reads the notebook and creates
an in-memory notebook containing only cells `0–8`, `12`, and `15`, plus a new
sampling cell. It does not write an executed notebook or modify the clone.
Before and after every extraction it checks both the upstream commit and the
notebook SHA-256, fails on either change, and records both values in
`artifacts/upstream/oracle_barotropic_perturbations.json`. The most recent
extraction recorded identical before/after values shown above.

The extracted upstream scenario is exactly:

```text
sound_speed=upstream_d2_corrupted
branch=printed_4_15
tilt_form=unrescaled_V
rate=upstream_unconverted
epoch=upstream_0p218_gyr
k_convention=upstream_timescape_k
k in {2*pi, 5*pi, 10*pi}
solve_ivp(method=RK45, rtol=1e-3, atol=1e-6,
          max_step=inf, first_step=None, dense_output=False,
          events=None, vectorized=False)
```

The extraction emitted, and did not suppress, Windows/Jupyter runtime
warnings: pyzmq installed a selector thread because the Proactor loop lacks
`add_reader`; ipykernel used asyncio event-loop policy APIs deprecated for
Python 3.16; and the local ephemeral kernel transport warned that its TCP
connection was unencrypted. These are kernel-launch/transport warnings, not
ODE or scientific-model warnings. The kernel was local and no remote data or
author communication was involved.

## 3. Implemented equations and conventions

### 3.1 State and independent variable

The independent variable is Buchert volume-average time `t` in the same unit
as `1/TrackerParams.HD0`. The state is

```text
y = (Delta_d, Z, Delta_eff, tilt),       Z = -d(Delta_d)/dt,
```

where `tilt` is either the paper variable `Vtilde` or the unrescaled notebook
variable `V`, related by

```text
Vtilde = (1 + w_eff) V.
```

The direct first-order equations are represented as `dy/dt=A(t)y`. Entries
common to both tilt forms are

```text
A12 = -1                                                   [GM (4.14)]
A21 = -4*pi*G*rho_d                                        [GM (4.16)]
A22 = -(2/3)*Theta                                         [GM (4.16)]
A23 = -4*pi*G*rho_eff*(1 + 3*c_s^2)                        [GM (4.16)]
A32 = -(1 + w_eff)                                         [GM (4.15)]
A33 = (w_eff + c_s^2)*Theta             [printed_4_15]
A33 = (w_eff - c_s^2)*Theta             [derived_4_10: GM (4.10)+(4.13)]
```

All unlisted entries are zero. For `rescaled_Vtilde`, implemented directly
from [GM] Eqs. (4.15) and (4.17),

```text
A34 = k^2/a_D
A43 = -c_s^2/a_D
A44 = (Theta/3)*(3*w_eff - 1).
```

For `unrescaled_V`, Eq. (4.15) is transformed with
`Vtilde=(1+w_eff)V`, while the tilt equation is [GM] Eq. (4.8) with closure
Eq. (4.13):

```text
A34 = k^2*(1+w_eff)/a_D
A43 = -c_s^2/[a_D*(1+w_eff)]
A44 = (Theta/3)*(3*c_s^2 - 1).
```

Thus both forms obey the normalization-independent identity

```text
A34*A43 = -c_s^2*k^2/a_D^2.
```

The exact transform is checked as

```text
A_Vtilde = Tdot*T^-1 + T*A_V*T^-1,
T = diag(1,1,1,1+w_eff),
w_eff_dot = -Theta*(1+w_eff)*(c_s^2-w_eff),                [GM (3.17)]
```

for both D3 choices and both wavenumber conventions. Only the corrected
Phase 1B `cs2_eff=dp_eff/dt / drho_eff/dt` enters the scientific package.

### 3.2 Mandatory scenario choices

`BarotropicScenario` requires every field below; no field or public matrix/RHS
argument has a default:

| field | allowed explicit values | interpretation |
|---|---|---|
| `branch` | `printed_4_15`, `derived_4_10` | unresolved A33 provenance |
| `tilt_form` | `unrescaled_V`, `rescaled_Vtilde` | state normalization |
| `rate_convention` | `upstream_unconverted`, `lcdm_to_timescape_converted` | units of initial Z |
| `epoch_choice` | `upstream_0p218_gyr`, `dressed_z20` | initial time |
| `wavenumber_convention` | `upstream_timescape_k`, `paper_lcdm_hubble_k` | numerical k interpretation |
| `k`, `timescape_h`, `lcdm_h` | positive finite numbers | mode and physical conversion data |

String lookalikes are rejected; callers must supply the typed enum values.
Every B2 artifact run is serialized with the complete schema-v1 run record
defined in Sec. 11. The existing public scenario identifier remains focused
on scientific choices; the artifact run identifier additionally covers sound
provenance and every explicit solver option.

The upstream epoch is `t_i=0.016326590304765798` in notebook code units,
or exactly `0.218 Gyr` under the notebook conversion; its dressed redshift is
`18.5864748995`. The alternative root is `t_i=0.014694412469902116`,
`0.196206425141 Gyr`, and dressed `z=20.0000000000`.

The shared initial amplitude is
`Delta_d=0.0031427229788258105`, with `Delta_eff=tilt=0`. The two explicit
rate values are

```text
Z_upstream_unconverted          = -0.16974050039281288
Z_lcdm_to_timescape_converted   = -0.15622708898642074.
```

The upstream k convention injects the supplied number directly. The paper
Hubble-length interpretation is made explicit by equality of the present
physical mode,

```text
k_matrix = k_paper * a_D(t0) * h_LCDM/h_Timescape,
```

which is a factor `1.2595507305749012` for `a_D(t0)=1.3685`,
`h_LCDM=0.674`, and `h_Timescape=0.7323`. This is an exposed interpretation of
the unresolved normalization, not a hidden conversion.

## 4. D2 isolation

The audited D2 expression exists only in
`scripts/_phase1c_b2_forensic.py`, outside `src/timescape_fsigma8`. Its names
begin with an underscore, it is absent from `timescape_fsigma8.perturbations`
and `__all__`, and tests search the entire scientific package to ensure the
forensic function names and closed-form polynomial are absent. The scientific
barotropic matrix always calls the corrected Phase 1B `bg.cs2_eff`.

The forensic harness implements both tilt equations directly. This is
important: substituting the D2 value while retaining the exact corrected
background `w_eff_dot` identity breaks the V-to-Vtilde transform, as expected.
It is not silently repaired.

## 5. Metrics and denominator handling

For a component trajectory `x_i` and reference `r_i`, every reported
`normalized_linf` is exactly

```text
max_i |x_i-r_i| / max(max_i |r_i|, 1e-300).
```

The denominator is a single global component scale. Therefore a reference
zero crossing causes no division by zero and is retained in the maximum. If
the entire reference component is zero, `1e-300` is used. The diagnostic
pointwise-relative metric first defines

```text
S=max_i|r_i|,
relative_floor=max(1e-14*S,1e-300),
```

and reports `|x_i-r_i|/|r_i|` only where `|r_i|>relative_floor`. Endpoint
relative differences divide by
`max(|r_endpoint|,relative_floor)`. D2/D3 interaction endpoints are signed
and normalized by `max(|corrected_printed_endpoint|,1e-300)`.

The finite-difference equation residuals use a different, cancellation-aware
scale. At each time sample, the denominator is the sum of the absolute
magnitudes of every term entering that equation, with `1e-300` only if all
terms vanish. For first-order equations this includes the absolute numerical
derivative plus every RHS term.

## 6. Upstream reproduction gate

| k | Delta_d | Z | Delta_eff | V | nfev independent/upstream |
|---:|---:|---:|---:|---:|---:|
| `2*pi` | `2.234e-16` | `3.270e-16` | `5.962e-16` | `4.912e-16` | `74/74` |
| `5*pi` | `4.168e-15` | `4.410e-15` | `1.693e-15` | `1.905e-15` | `116/116` |
| `10*pi` | `1.722e-14` | `2.834e-14` | `1.891e-15` | `1.835e-15` | `218/218` |

Entries are normalized L-infinity errors. Worst: `2.834e-14`; gate: `2e-8`.
The matching function evaluations provide a separate check that the explicit
SciPy defaults and state ordering match the notebook.

## 7. Independent equation-residual tests

### 7.1 First-order system and dust Eq. (4.18)

The numerical residual test solves a `DOP853` trajectory with
`rtol=2e-13`, `atol=2e-15` on a uniform 8,001-point grid at the deliberately
difficult `k=10*pi`. First and second derivatives come only from five-point,
fourth-order centered finite-difference stencils on the sampled trajectory;
the test does not use `barotropic_rhs`, `A*y`, `A_dot*y`, or analytic
trajectory derivatives to obtain them. It evaluates [GM] Eqs. (4.14)–(4.17)
and the Lambda=0 Eq. (4.18) at 7,997 interior samples for both branches and
both tilt forms.

| branch | tilt | Eq. 4.14 | Eq. 4.16 | Eq. 4.15 | tilt equation | Eq. 4.18 |
|---|---|---:|---:|---:|---:|---:|
| `printed_4_15` | `unrescaled_V` | `1.113e-6` | `7.420e-9` | `5.210e-7` | `4.165e-6` | `3.447e-9` |
| `printed_4_15` | `rescaled_Vtilde` | `1.117e-6` | `7.420e-9` | `5.210e-7` | `4.139e-6` | `3.348e-9` |
| `derived_4_10` | `unrescaled_V` | `8.105e-7` | `7.674e-9` | `3.195e-7` | `2.643e-6` | `3.230e-9` |
| `derived_4_10` | `rescaled_Vtilde` | `8.132e-7` | `7.674e-9` | `3.195e-7` | `2.622e-6` | `3.081e-9` |

The measured worst first-order residual refined as
`2.752e-5 -> 4.165e-6 -> 5.740e-7` for
`4001 -> 8001 -> 16001` points, factors `6.61` and `7.26`. Eq. (4.18)
refined as `2.068e-8 -> 3.447e-9 -> 5.192e-9`, with differentiation
roundoff visible at 16,001 points. The gates are therefore `1e-5` for the
first-order equations and `1e-8` for Eq. (4.18): both pass at 8,001 points and
both are below the corresponding 4,001-point worst value.

Additional tests cover every matrix entry, the `A34*A43` identity, the
long-wavelength `k^2 -> 0` limit, time/density unit rescaling, state-transform
round trips, exact matrix transformation, trajectory transformation, and
initial/short-time continuity with the validated comoving and Meszaros
systems where `Delta_eff=tilt=0`.

### 7.2 Effective-fluid second-order equations

The added diagnostic uses the same tight DOP853 configuration
(`rtol=2e-13`, `atol=2e-15`, `max_step=inf`, `first_step=None`,
`dense_output=False`, `events=None`, `vectorized=False`) and a uniform
8,001-point grid, hence 7,997 interior samples. It covers every combination
of `k in {2*pi,5*pi,10*pi}`, both tilt forms, and both D3 branches, always with
the corrected Phase 1B sound speed. `Delta_eff_dot`, `Delta_eff_ddot`,
`Delta_d_dot`, and the background `c_s^2_dot` are all obtained by five-point,
fourth-order centered finite differences applied to sampled values. No
scientific RHS, matrix product, analytic matrix derivative, or solver
dense-output derivative supplies a trajectory derivative.

Write `D=Delta_eff`, `delta=Delta_d`, `w=w_eff`, and `c=c_s^2`. For
`printed_4_15`, the test evaluates the Lambda=0 form of printed [GM]
Eq. (4.19):

```text
D_ddot + (2/3 - 2w - c) Theta D_dot + C_printed D
  = 4*pi*G*rho_d*(1+w)*delta - c*(1+w)*Theta*delta_dot,

C_printed = (2/3)*Theta^2*[-2w + c*(1+3w)] - Theta*c_dot
            + 4*pi*G*rho_d*(w+c)
            - 4*pi*G*rho_eff*(1-3w^2+2c) + c*k^2/a_D^2.
```

For `derived_4_10`, differentiating [GM] Eqs. (4.10)+(4.13) and eliminating
`Z` and `Vtilde` with Eqs. (4.14), (4.16), and (4.17) instead gives the
distinct derived-branch analogue

```text
D_ddot + (2/3 - 2w + c) Theta D_dot + C_derived D
  = 4*pi*G*rho_d*(1+w)*delta - c*(1+w)*Theta*delta_dot,

C_derived = (4/3)*Theta^2*(c-w) + Theta*c_dot
            + 4*pi*G*rho_d*(w-c)
            + 4*pi*G*rho_eff*(3w^2-1-4c-6wc) + c*k^2/a_D^2.
```

This derived equation is not printed Eq. (4.19). Its damping differs by
`+2*c*Theta`, and its `D` coefficient changes because the originating
first-order self-coupling is `(w-c)Theta` rather than `(w+c)Theta`. The dust
source terms are unchanged. This is a provenance-preserving branch
comparison, not an adjudication of either branch.

At every interior sample the residual denominator is the sum of the absolute
magnitudes of every displayed additive term after moving the right-hand side
to the left, with a `1e-300` floor only when all terms vanish. The subterms of
`C_printed` or `C_derived` are scaled separately so background coefficient
cancellation cannot artificially improve the metric.

Measured maximum scaled residuals on 8,001 points are:

| branch | tilt | `2*pi` | `5*pi` | `10*pi` |
|---|---|---:|---:|---:|
| `printed_4_15` | `unrescaled_V` | `2.2380e-8` | `3.7485e-8` | `2.6778e-8` |
| `printed_4_15` | `rescaled_Vtilde` | `2.2434e-8` | `3.7593e-8` | `2.6820e-8` |
| `derived_4_10` | `unrescaled_V` | `3.7127e-9` | `2.1546e-8` | `1.4940e-7` |
| `derived_4_10` | `rescaled_Vtilde` | `3.2863e-9` | `2.1542e-8` | `1.4943e-7` |

The branch-wise worst refinement history is:

| equation branch | 4,001 points | 8,001 points | 16,001 points |
|---|---:|---:|---:|
| printed Eq. (4.19) | `4.7218e-7` | `3.7593e-8` | `2.7184e-8` |
| derived_4_10 analogue | `1.3202e-6` | `1.4943e-7` | `6.6882e-8` |

The coarse-to-working-grid reductions are factors `12.56` and `8.84`; the
smaller fine-grid improvements and low-k reversals identify finite-precision
differentiation onset. The fixed acceptance gate is therefore `2e-7`: above
the measured 8,001-point worst but below both 4,001-point worsts. Inserting
the wrong branch equation into a `k=2*pi`, `rescaled_Vtilde` trajectory gives
`0.502974` for a printed-branch trajectory and `0.362161` for a derived-branch
trajectory, versus matching residuals below `2.3e-8`. The focused test thus
fails both on gate exceedance and on loss of branch sensitivity.

## 8. Solver convergence and trajectory diagnostics

The reference is DOP853 with `rtol=2e-13`, `atol=2e-15`. The acceptance gate
for tight RK45/DOP853 and the tight Radau cross-check is `2e-8`. Across all
three k values and both branches:

```text
worst tight explicit normalized_linf = 3.139e-9
worst tight Radau normalized_linf    = 2.703e-11
```

The largest errors from upstream-default RK45 and medium DOP853 were
`2.714e-3` and `3.873e-7`, respectively. Thus the upstream settings are
adequate for reproducing their own oracle but not used for scientific factor
comparisons. Tight DOP853, not upstream-default RK45, supplies those runs.

| branch | k | reference nfev | tight RK45 nfev | tight Radau nfev | RK45/Radau nfev | dust sign changes | dust endpoint | Delta_eff endpoint |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `printed_4_15` | `2*pi` | 1,076 | 860 | 4,729 | 0.182 | 0 | `2.883e-2` | `5.039e-2` |
| `printed_4_15` | `5*pi` | 1,520 | 2,648 | 11,105 | 0.238 | 1 | `-1.596e2` | `3.314e4` |
| `printed_4_15` | `10*pi` | 3,578 | 6,656 | 28,479 | 0.234 | 1 | `-3.139e12` | `3.531e15` |
| `derived_4_10` | `2*pi` | 1,166 | 1,142 | 4,573 | 0.250 | 1 | `-3.752e-2` | `2.424` |
| `derived_4_10` | `5*pi` | 1,478 | 3,338 | 13,242 | 0.252 | 1 | `-1.102e4` | `3.199e6` |
| `derived_4_10` | `10*pi` | 3,992 | 7,376 | 31,784 | 0.232 | 1 | `-2.722e14` | `3.546e17` |

The empirical stiffness diagnostic flags only if tight RK45/Radau nfev is
greater than 5. All ratios are `0.182–0.252`; no run is flagged and Radau is
substantially more expensive. This is not a proof that the equations are
non-stiff, but there is no evidence of stiffness under this diagnostic.

All solvers completed successfully. In every baseline convergence run,
`Delta_eff` and tilt start at zero, remain nonnegative, and have no strict
sign crossing. Dust and Z each cross once in every case except
`printed_4_15, k=2*pi`; the dust loss of positivity is therefore branch
dependent at low k and common to both branches at 5*pi and 10*pi. The first
dust crossings range from about `0.901 Gyr` (derived, 10*pi) to `10.476 Gyr`
(derived, 2*pi). High-k amplification is extreme: relative to the initial
dust amplitude, the 10*pi effective contrast reaches `1.12e18` for
`printed_4_15` and `1.13e20` for `derived_4_10`. This rapid growth and the
visible medium-tolerance sensitivity are reported even though the tight
solutions converge.

## 9. Controlled factor analysis

The corrected-background comparison baseline is explicitly

```text
sound=corrected_phase1b | branch=printed_4_15 | tilt=unrescaled_V |
rate=upstream_unconverted | epoch=upstream_0p218_gyr |
k_convention=upstream_timescape_k | solver=tight DOP853.
```

This is a comparison origin, not a declaration that the D3 branch is
scientifically preferred. The table reports absolute endpoint differences
divided by the corresponding baseline/reference endpoint magnitude.

| factor changed alone | k | Delta_d endpoint relative effect | Delta_eff endpoint relative effect |
|---|---:|---:|---:|
| D2 at `printed_4_15` | `2*pi` | 7.72% | 7.61% |
|  | `5*pi` | 86.11% | 64.31% |
|  | `10*pi` | 97.85% | 92.96% |
| D3 with corrected sound speed | `2*pi` | 230.15% | 4,710.78% |
|  | `5*pi` | 6,803.81% | 9,554.81% |
|  | `10*pi` | 8,569.10% | 9,940.34% |
| initial Z rate conversion | `2*pi` | 3.61% | 4.34% |
|  | `5*pi` | 6.19% | 6.19% |
|  | `10*pi` | 7.09% | 7.09% |
| initial epoch | `2*pi` | 1.94% | 2.13% |
|  | `5*pi` | 15.84% | 15.84% |
|  | `10*pi` | 61.28% | 61.28% |
| k normalization | `2*pi` | 32.44% | 583.49% |
|  | `5*pi` | 35,738.29% | 64,669.56% |
|  | `10*pi` | 40,686,071.32% | 68,364,995.62% |

The full 2x2 D2/D3 design shows a large, non-additive interaction. The signed
interaction endpoint normalized to the corrected-background
`printed_4_15` endpoint is, for `(Delta_d, Delta_eff)`,

```text
2*pi:  (+1.691, -22.986)
5*pi:  (+62.973, -76.628)
10*pi: (+84.651, -95.424).
```

Consequently it is invalid to estimate a “D2 correction” and a “D3
correction” independently and add them for these trajectories.

### Tilt forms

With corrected `c_s^2`, direct rescaled trajectories agree with transformed
unrescaled trajectories to worst normalized L-infinity values between
`1.095e-12` and `4.525e-10` across all k and both branches. With the forensic
D2 value, the disagreement is `0.1405–0.2290`. The exact corrected matrix
identity and the numerical trajectory result therefore agree, while the
expected D2 loss of equivalence is material rather than roundoff.

## 10. Figure 3 endpoints and plot ambiguity

| k | scenario | Delta_d(t0) | raw Delta_eff(t0) | Delta_eff(t0)/k^2 |
|---:|---|---:|---:|---:|
| `2*pi` | upstream forensic | `3.105696e-2` | `4.655478e-2` | `1.179246e-3` |
|  | corrected `printed_4_15` | `2.883229e-2` | `5.039166e-2` | `1.276436e-3` |
|  | corrected `derived_4_10` | `-3.752402e-2` | `2.424232` | `6.140650e-2` |
| `5*pi` | upstream forensic | `-2.216272e1` | `1.182187e4` | `4.791222e1` |
|  | corrected `printed_4_15` | `-1.595991e2` | `3.313648e4` | `1.342971e2` |
|  | corrected `derived_4_10` | `-1.101842e4` | `3.199264e6` | `1.296613e4` |
| `10*pi` | upstream forensic | `-6.734991e10` | `2.479321e14` | `2.512077e11` |
|  | corrected `printed_4_15` | `-3.139420e12` | `3.531343e15` | `3.577999e12` |
|  | corrected `derived_4_10` | `-2.721593e14` | `3.545589e17` | `3.592433e14` |

Six separate Figure-3 variants are generated, each as PNG and PDF:

- `fig3_forensic_upstream_raw.*`
- `fig3_forensic_upstream_over_k2.*`
- `fig3_corrected_printed_4_15_raw.*`
- `fig3_corrected_printed_4_15_over_k2.*`
- `fig3_corrected_derived_4_10_raw.*`
- `fig3_corrected_derived_4_10_over_k2.*`

“Raw” means not divided by `k^2`; the plotted log magnitude is explicitly
labelled. This exposes the notebook-cell-19 raw quantity and the paper-caption
`Delta_eff/k^2` quantity rather than silently choosing one. The two corrected
branch plotters import only the scientific package and never read oracle data.
The upstream data are confined to the separately titled “FORENSIC ONLY”
figures. Every plotted mode includes its complete scenario identifier in the
figure. Axes autoscale rather than retaining the upstream notebook's clipping
limits, so the rapid high-k growth remains visible.

Every k mode now has a shared non-colour encoding in both corrected and
forensic plotters, on both panels and in raw and divided variants:

| mode | non-colour encoding |
|---|---|
| `k=2*pi` | solid line + circle marker |
| `k=5*pi` | dashed line + square marker |
| `k=10*pi` | dash-dot line + triangle marker |

Legends state both k and the encoding. Colours remain redundant visual aids;
the mode is identifiable in monochrome. Neither D3 branch is labelled
canonical, preferred, or correct.

## 11. Machine-readable outputs

All generated JSON artifacts are local, ignored, and reproducible:

| file | SHA-256 |
|---|---|
| `artifacts/upstream/oracle_barotropic_perturbations.json` | `37e2c16cc929e42c1b02bc821c4da4b46e437db74376f92a79ad9e128bdef8a0` |
| `artifacts/independent/phase1c_b2_oracle_comparison.json` | `914e989f40dcc4e83a3c3dc7f6ecd79f3b3cfd425eb0a375a0403b02beccabfe` |
| `artifacts/independent/phase1c_b2_convergence.json` | `0dce96744dfddcec7e222ea3fcd147d657491cf43a8fca0c6d7449b4186c896b` |
| `artifacts/independent/phase1c_b2_d2_d3_factorial.json` | `6909d8e7ce24f18ce0d65dcd6a63a9af253f08ef5d7c962e6da563254ca46861` |
| `artifacts/independent/phase1c_b2_scenario_effects.json` | `1647507ac0dd559ce9cb91b66a711d7c5228a9eed4aee87536ba99d328f88192` |
| `artifacts/independent/phase1c_b2_figure_endpoints.json` | `f808f630d93912167610b6562039bec286fe4ce06bbc9b226c73d27939160cc6` |

All five files use `phase1c_b2_run_record_v1`. Every individual run record is
self-contained and has exactly this shape:

```text
schema_version
branch
tilt_form
rate_unit_convention
epoch_choice
wavenumber_convention
numerical_k
timescape_h
lcdm_h
sound_speed_provenance
solver:
  method, rtol, atol, max_step, first_step,
  dense_output, events, vectorized
run_identifier
```

`sound_speed_provenance` is exactly `corrected_phase1b` or
`upstream_d2_corrupted`. `run_identifier` is
`phase1c_b2_run_v1:` followed by SHA-256 of UTF-8 canonical JSON
(`sort_keys=true`, separators `(',', ':')`, `allow_nan=false`) over every
record field except the identifier itself. Thus any scientific choice, Hubble
normalisation, sound provenance, or solver-option change changes the stable
identifier; the algorithm gives the two D3 labels equal status.

The oracle comparison contains separate complete records for each independent
and upstream-oracle execution. Every factorial cell and convergence solver
run carries its own record; baseline and every alternative scenario-effect
run carry theirs; both tilt representations carry theirs; and every plotted
endpoint curve, including the upstream D2 curve, carries its own record. The
schema tests parse all five files and validate `6`, `42`, `12`, `36`, and `9`
records respectively. Identical configurations may reuse the same stable ID;
different complete configurations are checked not to collide.

The convergence JSON also includes per-component metrics, solver
counts/messages, extrema, sign changes, first strict zero crossings,
positivity flags, amplification, and the empirical stiffness classification.

Regenerated Figure 3 hashes are:

| file | SHA-256 |
|---|---|
| `fig3_corrected_derived_4_10_over_k2.png` | `8e5080b5a507b4260af4aa3b39f58cab9d1ce63c6235e337dce99db05daf4ec4` |
| `fig3_corrected_derived_4_10_over_k2.pdf` | `3216015919095e463e8c0aa4ede681d6761eb49e93dee386cfe1fd4f6ec21635` |
| `fig3_corrected_derived_4_10_raw.png` | `031568a5a3d0b63a5980fa1573f9cfde4f5db64071edf5491819b56160c0d92f` |
| `fig3_corrected_derived_4_10_raw.pdf` | `1e05c72edc293962d44fec1ddb6b2d84c85e83bd19efc3ffdf1c7768eccc220d` |
| `fig3_corrected_printed_4_15_over_k2.png` | `66e420524f48458e2e90ab6f8a8d0a9bfdc2220f806c40135663f508b3abd9ab` |
| `fig3_corrected_printed_4_15_over_k2.pdf` | `21b989a059d7fb3bcb967ccf621477a056b02717588d8d7d38eb2480e63343c4` |
| `fig3_corrected_printed_4_15_raw.png` | `ac8a8e2781f2fe8e9b71a82a243433b87545df51eb58dd50c12786895398ff12` |
| `fig3_corrected_printed_4_15_raw.pdf` | `c9f382e2b944903bebbfc7feb25e8705a2ece0214117afd5ae4db7a33095572e` |
| `fig3_forensic_upstream_over_k2.png` | `2ef597d330daab492043ce6e14a5f5e5527c0b58206d75fc4ed6bab913f377cd` |
| `fig3_forensic_upstream_over_k2.pdf` | `042b647710c4aad945ede8c6e80fefc044749cb67fe47ad6f5bd8b5bb0f12110` |
| `fig3_forensic_upstream_raw.png` | `9ed53e95fd146b373afa6927baee34f2167900da0260bee4a8475176a0f9ca96` |
| `fig3_forensic_upstream_raw.pdf` | `9a72b928a6ae8b4289f8b7c7a059f7425a1cb4abf467d002734a0630a9d7a9b2` |

The complete reproduction sequence is:

```powershell
$env:PYTHONPATH="$PWD\.venv\Lib\site-packages;$PWD\src"
C:\Python314\python.exe scripts/extract_upstream_barotropic_oracle.py
C:\Python314\python.exe scripts/validate_barotropic_perturbations.py
C:\Python314\python.exe scripts/make_barotropic_fig3.py
C:\Python314\python.exe scripts/make_barotropic_fig3_forensic.py
```

## 12. Tests and environments

The exact complete-suite commands were:

```powershell
$env:PYTHONPATH="$PWD\.venv\Lib\site-packages;$PWD\src"
C:\Python314\python.exe -m pytest -q

$env:PYTHONPATH="$PWD\.venv311\Lib\site-packages;$PWD\src"
C:\Python\Python3119\python.exe -m pytest -q
```

| environment | resolved versions | complete result |
|---|---|---|
| Python 3.14 | CPython 3.14.3; NumPy 2.5.1; SciPy 1.18.0; Matplotlib 3.11.0; pytest 9.1.1 | `268 passed in 7.64s` |
| Python 3.11 | CPython 3.11.9; NumPy 2.4.6; SciPy 1.17.1; Matplotlib 3.11.0; pytest 9.1.1 | `268 passed in 7.49s` |

`git diff --check` exits zero with no whitespace error. Git emits its existing
working-copy EOL advisory for `perturbations/__init__.py` (LF would become
CRLF if Git next rewrites it); this advisory was not suppressed. No test or
scientific warning was suppressed.

## 13. Frozen-file proof and change inventory

At completion, `git diff --name-only HEAD` lists only one pre-existing tracked
file:

```text
src/timescape_fsigma8/perturbations/__init__.py
```

Its only changes are the strictly necessary B2 package documentation and
public exports. Phase 1B scientific files, B1 equation/system/solver files,
B1 reports/scripts/tests, the upstream clone, `UPSTREAM.lock`, and generated
B1 artifacts are unchanged. Selected frozen SHA-256 values rechecked after
B2 include:

```text
f6590fe8bb16ec13ec81d913fbf32b27ee3dd33d4f8d37fd4dd66ce194962bca  background/effective_fluid.py
9d50270bedafbc5152f17cfd996c90d26bdbda4830a3e75a8b4e42effd0b8eb0  background/tracker.py
e8a152f2ab91e7fb59d5cbaf9c43a1ac053fde3e4fad034a74e1736a54885e42  perturbations/initial_conditions.py
33bacac0987fb1cbd2db58b62797745f230a9ebaf634b32834b4811c7cdf0335  perturbations/residuals.py
9ad45dcb404c99d088b8170dddca01e8814746623d954f200f7761d36b99f57d  perturbations/scenarios.py
9d774fdb10e0ec6d0e74ea89a910f5365f09bf9634a2260d27ab5a78e8b8ae84  perturbations/solver.py
1e619858b94b5c36467571a8b62c54c73445aebdb9f2cfcd0283b083e18777a6  perturbations/systems.py
68951ccb225885fd95485983c02e94606948a641f66e1a18a73c5536134c0c71  tests/test_clean_perturbation_systems.py
928b19a6e0fa38eec3be80e62b0f1ca0e9f3fd1c376c9184ea6eb7fd4d57f281  tests/test_perturbation_initial_conditions.py
a4bac07cdc747cc55aa4f09bb05723b64ea1bde1cf657f5a2a896de77a670793  tests/test_vs_upstream_perturbation_oracle.py
916300a153973865853a2b4875d441db948b1b1c2732691d262804888c47867b  reports/phase1c_b1_clean_systems_validation.md
```

New tracked-candidate source/report/test files are:

```text
reports/phase1c_b2_barotropic_validation.md
scripts/_phase1c_b2_forensic.py
scripts/_phase1c_b2_plot_styles.py
scripts/extract_upstream_barotropic_oracle.py
scripts/make_barotropic_fig3.py
scripts/make_barotropic_fig3_forensic.py
scripts/validate_barotropic_perturbations.py
src/timescape_fsigma8/perturbations/barotropic.py
src/timescape_fsigma8/perturbations/barotropic_solver.py
tests/test_barotropic_forensics.py
tests/test_barotropic_systems.py
tests/test_b2_artifact_schema.py
tests/test_vs_upstream_barotropic_oracle.py
```

Generated JSON, PNG, and PDF files remain under ignored
`artifacts/upstream/` and `artifacts/independent/`; none is staged.

## 14. Robust and conditional conclusions

Robust within the audited equations and performed checks:

- every barotropic matrix entry maps to [GM] Eqs. (4.13)–(4.17), with the
  unresolved A33 provenance explicit;
- the pinned upstream Figure-3 trajectories are independently reproduced;
- corrected-background V and Vtilde formulations are the same system under
  the exact [GM] Eq. (3.17) transform;
- the forensic D2 value materially breaks that equivalence;
- strong scale-dependent growth at 5*pi and 10*pi occurs in the upstream
  oracle and both corrected-background D3 branches;
- those trajectories converge under tight RK45/DOP853 and Radau checks, with
  no solver failure or empirical stiffness flag;
- the notebook/paper raw-Delta_eff versus Delta_eff/k^2 ambiguity changes the
  plotted ordinate and is now explicit.

Conditional or not robust:

- endpoint amplitudes are strongly D2- and D3-dependent, with a large D2/D3
  interaction;
- the low-k dust sign reversal depends on D3;
- high-k amplitudes are sensitive to the initial epoch and extraordinarily
  sensitive to the unresolved k normalization;
- the Z-rate conversion has a smaller but measurable 3.6–7.1% endpoint
  effect in the tested baseline;
- neither local sources nor these numerical results determine whether
  `printed_4_15` or `derived_4_10` is intended. Author input or independent
  adjudication of Dunsby–Bruni–Ellis (1992) remains required;
- the physical origin of 0.218 Gyr and the intended Z and k conventions remain
  unresolved. The API exposes each choice rather than guessing.

These dependencies must be resolved before Phase 1C results can support a
unique downstream growth observable.
