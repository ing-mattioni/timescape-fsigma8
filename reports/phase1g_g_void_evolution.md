# Phase 1G-G — population evolution: conserved moments and missing closures

Date: 2026-10-01; audit remediation revision: 2026-10-02. Parent: `fb5d95245bc0cb19ce6cd1438177f1a597bb232f`.
Owner-authorized theoretical continuation with report-only numerical
evidence. This is a local research proposal, not a frozen implementation
phase or a new Timescape prediction. The permanent AGENTS.md rules apply.

## 1. Question and result

Can evolution and merging connect the early-spectrum void population of
1G-F to the tracker's f_v(t), large voids and a closed mass-variance model?

Three deductions constrain that route:

1. Additive void mergers conserve total void volume at a fixed epoch.
   They can redistribute sizes, but cannot independently fix a wrong
   total-volume history at a prescribed common, size- and age-independent
   regional void expansion rate.
2. A finite-density shell-crossing cohort has an instantaneous volume
   growth rate different from that of the empty-void tracker. A required
   transfer moment can be calculated, but its physical mechanism is not
   determined by the one-epoch excursion-set distribution.
3. An exactly empty regional volume at finite time cannot retain the
   finite mass of the shell-crossing seeds. A mass-transfer law, a changed
   regional background, or an explicitly approximate empty-void limit is
   needed. Merging alone does not supply that law.

These are conditional consistency statements, not a general no-go for
Timescape or realistic void evolution. Below, a solvable kinetic example
verifies the first statement without choosing a physical merger kernel.

## 2. Explicit assumptions and measures

Use the common tracker time t, keeping the 1G-C owner decision's A5 clock
assumption explicit. This is not a derivation of a local proper-time map.
Use disjoint regional volumes in one fixed material domain; the following
volume moment is not a sum of overlapping Boolean grain volumes.

For a common regional void expansion factor g_v(t), normalized to one at
t_ref, write individual physical volume as v=g_v q. Let n(q,t)dq be the
number per **fixed reference volume**, not per evolving physical volume.
Thus no cosmological dilution term appears in the count equation.
For Milne expansion, g_v=(t/t_ref)^3. Binary mergers have q_new=q+q'.
The effective symmetric kernel K(q,q',t) uses this reference-volume
convention; a physical-density collision kernel would require the
corresponding dilution factor before use here.

Assume finite first moments, convergent collision integrals, no untracked
boundary flux at q=0 or infinity, and no loss into an omitted gel component.
Allowing different regional expansion rates requires volume-weighted rates
below; number counts alone would no longer close the problem. If H_v depends on
size or age, even volume-conserving mergers can change subsequent expansion
by redistributing volume among rate classes. G2 still conserves volume at
the merger instant; it does not fix that future weighted rate.

## 3. Evolution equation and first-moment identity

As an explicitly imported kinetic description, adapt [L03] Eq. (2.2):

\[
 \partial_t n(q)=\tfrac12\int_0^q K(q',q-q')n(q')n(q-q')dq'
 -n(q)\int_0^\infty K(q,q')n(q')dq'+S(q,t). \tag{G1}
\]

Here q is reduced **volume**, not particle mass. Assigning this kinetic
description to voids is an additional model assumption. As stated below
[L03] (2.2), it neglects spatial cluster correlations and either neglects
morphological dependence of rates or averages over it. These mean-field
assumptions are not derived for spatially connected cosmic voids. For
Q_1=integral q n dq, the collision contribution is

\[
 \dot Q_1\big|_K=\tfrac12\iint K nn'[q+q'-q-q']dq\,dq'=0,
 \qquad \dot Q_1=\int q S\,dq. \tag{G2}
\]

With no source, V_v is proportional to g_v Q_1 and V_w to t^2; hence

\[
 \dot V_v=3H_vV_v,\quad\dot V_w=3H_wV_w,\quad
 \dot f_v=3f_v(1-f_v)(H_v-H_w). \tag{G3}
\]

Putting H_v=1/t and H_w=2/(3t) gives

\[
 f_v(t)=\frac{f_{\rm ref}(t/t_{\rm ref})}
 {1-f_{\rm ref}+f_{\rm ref}(t/t_{\rm ref})}
 =\frac{t}{t+\tau},\quad
 \tau=t_{\rm ref}\frac{1-f_{\rm ref}}{f_{\rm ref}}. \tag{G4}
\]

This is [GM] Eq. (5.6), as a conditional volume identity. Recovering it
after supplying f_ref does not derive its normalization from the early
spectrum. Changing a volume-conserving kernel K cannot change G4 while
holding these expansion laws and normalization fixed.

Actual void mergers can absorb walls, alter expansion, or change the
classification boundary. Those effects violate the additive/no-transfer
assumptions and must appear explicitly. Let J be net physical volume per
unit t transferred from walls to voids, with opposite signs in the two
regional volume equations. Then

\[
 \dot V_v=3H_vV_v+J,\quad\dot V_w=3H_wV_w-J,\quad
 \dot f_v=3f_v(1-f_v)(H_v-H_w)+J/V_D. \tag{G5}
\]

For a non-additive merger v_new=v+v'+epsilon, the first collision moment
acquires the integral of epsilon times the collision rate. G2 no longer
sets it to zero. This is a volume-transfer closure, not the conservative
kernel already tested here.

## 4. A calculable mismatch at shell crossing

For the simultaneous-bang EdS spherical model, [JLH13] (A4)-(A5) gives
`H_v t = sinh(eta)(sinh(eta)-eta)/(cosh(eta)-1)^2`.
Its corrected shell condition (A8) sets this to 8/9, while H_w t=2/3.
Consequently, for a common shell-crossing cohort,

\[
 \dot f_v\big|_{J=0,\,sc}=\frac{2}{3}\frac{f_v(1-f_v)}{t},
 \qquad
 \frac{J_{\rm required}}{V_D}=\frac{1}{3}\frac{f_v(1-f_v)}{t}
 \quad\text{if the tracker rate is imposed}. \tag{G6}
\]

At the supplied present f_v, `t J_required/V_D` is 0.0646103 (GM) and
0.0779570 (NW15). This is an instantaneous necessary source moment for
these assumptions, not a measured flux or a derived formation mechanism.
This cohort is **not** F's population, which is reidentified at a fixed
density threshold independently at each epoch; its all-size F2 fraction
is constant. Reinterpreting that fraction as a persistent shell-crossing
cohort with zero derivative would require t*J/V_D approximately -0.12434,
not the positive tracker-target source above.

For a homogeneous open-interior continuation after shell crossing,
H_v*t rises from 8/9 toward 1. The zero-transfer coefficient 3*H_v*t-2
therefore rises from 2/3 toward 1; **2/3 is not an upper bound**.
The normalized required source J/[V_D*f_v*(1-f_v)/t] is instead bounded
above by 1/3 within this continuation, decreasing toward zero. At
t/t_sc = 1.5, 2, 10, the audit finds H_v*t approximately 0.9095, 0.9227,
0.9727. These are conditional interior continuations, not F evolution.

A polydisperse population need not cross shells simultaneously; its
age distribution and volume-weighted H_v must be supplied. Continuing a
homogeneous open-FLRW interior beyond shell crossing also does not derive
the subsequent boundary/ridge dynamics of an actual spherical void.

## 5. Mass accounting prevents a silent empty-void replacement

For x=rho_v/rho_w and m=M_v/M_D, physical mass accounting gives

\[
 m=\frac{f_v x}{1-f_v+f_v x},\qquad
 f_v=\frac{m/x}{1-m+m/x},\qquad
 \delta_v^{\rm global}=\frac{x}{1-f_v+f_vx}-1. \tag{G7}
\]

The second equation is successor F1-F2 for the full population; the third
distinguishes wall-reference density from global density contrast. For
the shell x=0.204722334 and tracker present fractions, m is 0.364551
(GM) / 0.256025 (NW15), whereas exactly empty voids imply m=0 at f_v<1.
These are **different normalizations** from F's full excursion-set mass
fraction 0.382971; here the tracker f_v has been supplied explicitly.

At fixed positive m, x tending to zero sends f_v to one and, with fixed
wall density unit, the domain volume to infinity. It does not produce a
finite-time tracker state with f_v=0.737 or 0.627. For a fixed finite
material domain with total mass conserved, a prescribed m(t) requires

\[
 \dot M_v=-\Phi,\quad \dot M_w=\Phi,\quad
 \Phi=-M_D\frac{d}{dt}\left[\frac{f_vx}{1-f_v+f_vx}\right]. \tag{G8}
\]

Phi is net mass transfer, distinct from the volume transfer J. If m>0 is
constant and G4 is imposed, then

\[
 x(t)=\frac{m}{1-m}\frac{\tau}{t}. \tag{G9}
\]

This cannot remain an underdensity (x<=1) back to t=0. A population of
identified voids needs a formation/reclassification history. Moreover,
exact dust-FLRW Milne dynamics with a(t) proportional to t is vacuum:
its dust acceleration equation has ddot(a)=0 and rho=0. A positive-mass
open dust region may approach Milne asymptotically, but it is not exactly
that regional background at finite time. These conclusions are conditional
on the regional dust-FLRW assumption, not a new global embedding theorem.

## 6. Analytic kinetic benchmark

For a constant effective kernel and monodisperse reduced-volume seeds
q0 with number density N0, define external exposure
`u=N0 integral K_eff(t) dt/2`. Rescaling [L03] Eq. (4.10) gives

\[
 n_k=\frac{N_0}{(1+u)^2}\left(\frac{u}{1+u}\right)^{k-1},
 \quad \sum n_k=\frac{N_0}{1+u},\quad
 \sum kq_0 n_k=N_0q_0. \tag{G10}
\]

For beta=u/(1+u), the exact volume tail above class k_min is

\[
 P_V(k\ge k_{\min})=\beta^{k_{\min}-1}
 [1+(k_{\min}-1)(1-\beta)]. \tag{G11}
\]

The equal-volume radius of class k is proportional to k^(1/3). At a
fixed epoch the radius at the mean volume grows as (1+u)^(1/3); this is
not the mean radius or the volume-weighted median.

| supplied u | N/N0 | conserved Q1/Q1_initial | radius at mean volume / seed radius | volume share in k>=125 |
|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 1 | 0 |
| 1 | 0.5 | 1 | 1.25992 | 2.96e-36 |
| 10 | 0.0909091 | 1 | 2.22398 | 0.0000904 |
| 100 | 0.00990099 | 1 | 4.65701 | 0.648651 |

Since 125=5^3, large changes in the volume above five seed radii coexist
with an unchanged total void volume. A rate fitted to make voids large
would therefore not independently solve the total-fraction problem.
This is a monodisperse benchmark, **not an evolution of the 1G-F
polydisperse population** and not a suggested physical value for u.

## 7. What is still needed for a predictive implementation

The one-epoch first-crossing distribution does not specify temporal
merger histories uniquely. Before implementing a physical evolution,
the following inputs or derivations must be explicit:

| Missing element | Required consistency check |
|---|---|
| Formation/age distribution of voids | Avoid counting the same Lagrangian mass in new seeds and existing descendants |
| Merger kernel and boundary rule | State whether volume is additive; account for absorbed wall volume |
| Regional density/expansion evolution | Check G5 and the regional gravitational equations in the chosen clock |
| Mass transport and ridge definition | Check G7-G8 and total mass conservation |
| Spatial positions, exclusion, correlations | One-point size counts are insufficient for the two-point mass variance |
| Common-spacetime and dressed mapping | Retain the existing embedding and observable firewalls |

In particular, n(q,t) fixes a size distribution but not the spatial
wall-indicator covariance. If the Boolean Poisson construction of 1G-E/F
is retained at every epoch, it is a new spatial closure: real merging
does not establish that the point process remains Poisson. To obtain
the ball variance one still needs

\[
 \sigma_R^2=V_R^{-2}\int_{B_R}\int_{B_R}
 \langle\delta(\mathbf x)\delta(\mathbf y)\rangle\,d^3x\,d^3y. \tag{G12}
\]

This is the real-space counterpart of [JLH13] Eq. (2), not a new
observational map. No sigma_R or f-sigma statistic is added by this phase.
The immediate useful next implementation would evolve a jointly labelled
mass/volume population with explicitly supplied formation, transfer and
merger laws, and reject histories violating these moments. Selecting
those physical laws remains an open scientific task; a constant kernel
must not be promoted to a default to fill that gap.

## 8. Evidence and scope

`scripts/phase1g_g_void_evolution_numerics.py` verifies G4 against the
existing tracker at five redshifts for both parameter sets, evaluates
G6-G7 and G10-G11, and records numerical tolerances. The associated tests
independently integrate the kinetic collision equation and the regional
volume-fraction ODE, check dimensions, vacuum/zero-merger limits, exact
tails and published reference values. Maximum tracker residual in this
run is 1.67e-16; the largest displayed moment error is 2.11e-15.

```bash
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 python -B -W error scripts/phase1g_g_void_evolution_numerics.py
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 python -B -W error -m pytest -q tests/test_phase1g_g_void_evolution.py
```

See the F/G validation record for observed test results and limitations.
The script is report evidence only. No package runtime or scientific-status
value changes. The original version was independently audited with corrections required
on 2026-10-02. The remediated tree passed an independent delta audit on
2026-10-06 (`phase1g_fg_remediation_independent_audit.md`). The final
two-interpreter runs and the phase-branch integration are recorded in
`phase1g_fg_remediation_integration.md`. No freeze, tag, merge or release
is implied. The 2026-10-02 D token successor is a separate classification
change, not a G runtime change.

## Windows reproduction and evidence identity

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH = "src"
$env:OPENBLAS_NUM_THREADS = "1"
.\.venv\Scripts\python.exe -B -W error scripts/phase1g_g_void_evolution_numerics.py
```

Use `.venv311` for the second interpreter. JSON is now written as UTF-8
bytes with LF on all platforms. Raw SHA-256 identifies one exact run;
it is not a cross-platform numerical-equivalence gate. Compare numeric
leaves with rtol=1e-11, atol=1e-14, ignoring environment and raw provenance
hash fields, and compare scientific labels and keys exactly. This budget
allows floating-point library differences; it is separate from the much
larger F radius-grid accuracy error. The inventory records the run's
environment, raw hash and these tolerances.

## References

- [L03] F. Leyvraz, *Scaling theory and exactly solved models in the
  kinetics of irreversible aggregation*, Physics Reports 383 (2003),
  https://arxiv.org/abs/cond-mat/0305670, Eqs. (2.2), (4.4)-(4.10).
- [JLH13] Jennings, Li & Hu, https://arxiv.org/abs/1304.6087,
  Eqs. (2), (13), (A4)-(A5), (A8)-(A9).
- [GM] Galoppo & Mourier, https://arxiv.org/abs/2511.17160v2,
  Eqs. (5.1), (5.5)-(5.6); regional dynamics as qualified in the
  1G-C and 1G-D owner-decision successors.
- [SvdW04] Sheth & van de Weygaert,
  https://arxiv.org/abs/astro-ph/0311260, void hierarchy and Eq. (C8).

G1 imports a kinetic equation; G2-G9 and G11 are the present conditional
deductions; G10 is a rescaling of a published analytic solution; G12 is the standard
covariance definition. None is
attributed to a Timescape source as an already derived population closure.
