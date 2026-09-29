# Phase 1F-D: minimal scalar necessary-bound diagnostic

Base checkpoint: `118b8f3af3c1360b0da74df8e9a9cb3ba1fed83a`.
Classification: `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`.

The implementation follows the user's explicit ASCII mathematical contract.
It is a new, authorized conditional diagnostic. It does not record a
remediation of the project or of the original derivation. Whether formatting
was lost during transfer of the earlier message is undetermined.

## Assumptions and derivation

Assume GR, geodesic irrotational dust, Lambda=0, rho>=0; a regular material
domain of finite positive intrinsic dust volume; spacelike slices with
uniform proper expansion Theta=theta_star; a local flat-dust core with
Theta_w=2/s_w, positive density and positive intrinsic volume; and the
prescribed tracker wall-clock anchor. This scalar module assumes these
conditions; it cannot verify them or construct such a geometry.

For `sigma**2=(1/2)*sigma_ab*sigma**ab`, Raychaudhuri gives
`D=-partial_tau Theta=Theta**2/3+2*sigma**2+4*pi*G*rho`.
This is [Buchert--Mourier--Roy, arXiv:1912.04213v2](https://arxiv.org/html/1912.04213),
Eq. (4.14) specialized to the declared matter sector. Differentiating the
uniform-expansion condition and the additional anchor gives
`ell=2*alpha_W/(s_w**2*D) <= 3*alpha_W/2`. Intrinsic averaging, BMR
Eqs. (4.5)-(4.6), (4.9), (4.12), gives `3*H_Omega=theta_star*<ell>`.
The core has `D_w=2/s_w**2` and `ell_w=alpha_W`, so its positive measure
makes `H_Omega < alpha_W/s_w` strict.

With the additional matching target `H_Omega=H_D`,
[Wiltshire, arXiv:0909.0749v2](https://arxiv.org/pdf/0909.0749v2),
Eqs. (B2), (B6), (B7), (B12), yield the authorized scalar contract:

```text
t>0, b>0, C finite; all three in the same time unit
x=t/b
f=t/(t+b)
alpha_W=2/(2+f)
tau_w=2*t/3+(2*b/9)*log1p(3*t/(2*b)), tau_w(0)=0
s_w=tau_w+C > 0
H_D=(2+f)/(3*t)
H_bound=alpha_W/s_w
M=6*t/(2+f)**2-s_w
d(x)=(2/9)*log1p(3*x/2)-2*x*(6*x+5)/(3*(3*x+2)**2)
M=-b*d(x)-C
d_prime(x)=2*(x+1)*(3*x-2)/(3*x+2)**3
```

The gap, its derivative and the necessary criterion are algebra derived
from those paper equations under the added assumptions, not independently
numbered equations printed in either paper. For C=0, d decreases up to
x=2/3 and then increases; d(3)<0<d(4), so there is one positive zero.
For any fixed finite C and b>0,
`M=-C-(2*b/9)*log(3*t/(2*b))+4*b/9+O(b**2/t)` tends to minus infinity.
This excludes an exact all-future realization of this branch only; passing
the inequality on a finite interval does not establish a realization.

The core is not identified with the whole Timescape wall, finite infinity,
H1 or dressed geometry. By BMR Eq. (E.2), ell=N/gamma is a threading lapse,
not generally the ADM lapse. A coordinate choice does not derive the
identification of an intrinsic average with the tracker.

## API, units and numerical policy

`src/timescape_fsigma8/phase1f_d.py` contains one scalar evaluator:

```python
from timescape_fsigma8.phase1f_d import diagnose_positive_core_bound

result = diagnose_positive_core_bound(
    t=3.0, b=1.0, C=0.0, time_unit="Gyr", margin_rtol=1e-12,
)
# result.decision: NOT_EXCLUDED_BY_NECESSARY_CONDITION
# result.existence_status: NOT_DERIVED
```

The frozen result supplies x, f, alpha_W, tau_w, s_w, H_D, H_bound, d,
margin M, its numerical scale, normalized margin, tolerance and decision.
The time-unit string is a required label, not a unit conversion or a check
that the caller supplied consistent units. C is an external offset.

The runtime uses the explicit (t,b) parameterization, without constructing
an arbitrary TrackerParams instance. Tests compare frozen background
functions only through the exact bridge
`b=(2+fv0)*(1-fv0)/(3*fv0*HD0)`, in matching time units and with tau_w(0)=0.
No identifications with other parameters named b are assumed.

Define `L=(2*b/9)*log1p(3*x/2)` and
`Q=b*2*x*(6*x+5)/(3*(3*x+2)**2)`. The implementation sums `M=Q-L-C`,
avoiding cancellation of the large linear terms in the direct margin.
For x>1 it uses reciprocal arguments in the rational term and
`log(x)+log(1.5+1/x)` for the logarithm. These are algebraically equivalent
numerical rearrangements. Summation uses `math.fsum`.

The declared tolerance applies to `M/S`, with
`S=max(L,Q,abs(C))>0` in time units. The absolute band is `margin_rtol*S`;
the relative tolerance itself is dimensionless. S, the clock, age and
margin scale with a change of time units, and the Hubble rates scale
inversely. The caller must supply `64*epsilon <= margin_rtol < 1`, where
epsilon is binary64 machine epsilon. No library comparison default is used.

| Decision | Meaning |
|---|---|
| `NOT_EXCLUDED_BY_NECESSARY_CONDITION` | M/S exceeds the declared positive band; only this necessary condition does not exclude the candidate. |
| `NUMERICAL_VIOLATION` | M/S is below the negative band; a numerical violation under the branch assumptions, without rigorous error certification. |
| `UNRESOLVED_THRESHOLD` | abs(M/S) is within the band, including equality; no sign decision at the adopted resolution. |

Mathematically the positive-core branch requires M>0. There is no optional
non-strict branch in this API. Neither tolerance nor positive margin proves
existence, sufficiency, H1 compatibility, or a physical Timescape background.

`NecessaryBoundDomainError` reports nonfinite, non-scalar, nonpositive t/b,
invalid tolerance/unit declarations, or an age determined numerically to
be negative away from its zero boundary. `NecessaryBoundNumericalError`
separately reports range limitations and unresolved age-boundary
cancellation. The age guard is 64*epsilon relative to the largest absolute
age summand, including C. It is a conditioning policy, not an interval proof.

The supported range requires normal positive binary64 x=t/b, tau_w, s_w,
H_D, H_bound and S. Ratio overflow/underflow and subnormal values of these
quantities are rejected explicitly even when the mathematical inputs are
valid. A subnormal margin is allowed only inside the unresolved band.
Dimensional rescaling can sometimes remedy range limitations; it cannot
change an unrepresentable dimensionless ratio. Rounded H_D and H_bound
can coincide at late times while the stable margin remains negative.
Reported rates near a cancelling age are conditioned by that subtraction;
no uniform relative-accuracy or rigorous sign guarantee is claimed.

## Scope and frozen scientific status

No solver, reconstruction, time scan or root finder is introduced. delta_T,
delta_P_ell, nu_W, q_core bounds, LTB profiles, H1 transfers, growth and all
observables remain outside the implementation. Scientific status globals
are not edited. In particular:

```text
REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING: NOT_DERIVED
ALL_TIME_TRANSFER_CONSTITUTIVE_COMPATIBILITY: NOT_DERIVED
UNIQUE_TIMESCAPE_PREDICTION: NOT_GRANTED
OBSERVATIONAL_AUTHORIZATION: NOT_GRANTED
RSD_AUTHORIZATION: NOT_GRANTED
SIGMA8_AUTHORIZATION: NOT_GRANTED
FSIGMA8_AUTHORIZATION: NOT_GRANTED
```

## Validation

The focused tests use a 400-digit Decimal evaluation of the direct
dimensional margin, independent quadrature of the clock from zero,
symmetric numerical derivatives, exact-convention frozen-background
comparisons, dimensional rescaling, early/late limits, monotonicity and
sign checks, offsets, threshold bands, invalid inputs and numerical range
failures. They explicitly verify that positive M carries no existence
claim or promotion of frozen scientific status. The rounded tracker
reference H_D0~58.01 km/s/Mpc uses the already documented GM p.25 reference
and W09 (B8)-(B9); no published reference value is claimed for the new M.

Actual validation on 2026-09-22, using the existing virtual environments:

| Check | Result |
|---|---|
| Focused suite, Python 3.14.3 | 64 passed in 0.50 s |
| Complete suite, Python 3.14.3 | 718 passed in 55.09 s |
| Complete suite, Python 3.11.9 | 718 passed in 57.37 s |
| Explicit comparison audit over src/scripts/tests, Python 3.14.3 | 11/2/387 comparisons, zero missing tolerances |
| Static parsing and package imports, Python 3.14.3 | 102 Python files parsed; 47 modules imported |

Both complete runs include the unchanged 654 existing tests and 64 new
tests, with no failures, skips, xfails or warnings. Commands used
`PYTHONDONTWRITEBYTECODE=1`, `python -B -W error -m pytest -q -p no:cacheprovider`.
No dependency was installed or updated. The initial focused run exposed an
incorrect test expectation that direct late-time cancellation must produce
zero; the actual direct result had a spurious positive sign. The test now
checks that failure mode against the negative independent Decimal reference;
no mathematical formula or comparison tolerance was relaxed to make it pass.

HEAD remains the base checkpoint; no commit, branch or remote changes were
made. All pre-existing scientific source files, tests, status globals,
dependency declarations and upstream lock are unchanged. The three
pre-existing untracked audit files retain their SHA-256 values from
preflight. The only edited pre-existing file is README.md, which links this
conditional diagnostic without promoting the scientific interpretation.
The historical phase-specific 1F-C-R validator (which hard-codes an older
branch/remote tip) was not repurposed; its relevant comparison, syntax,
import and preservation checks were performed directly for this checkpoint.
