# Independent scientific delta assessment, commit 89cb041

## Provenance and method

This review reads the exact local target checkout and makes no repository edits.
`AGENTS.md` was read. The revised H report and remediation record were read before
the independent-formula checkpoint. The earlier delta blind checkpoint is not
available; therefore **this run is not blind** and is not evidence for the missing
blind-workflow requirement. It does not relabel the prior audit's genuine blind
checkpoint as a new one.

The formula checkpoint was saved before reading the author's new lognormal
implementation. `independent_delta_science.py` imports no project module; it reuses
the first independent audit's EH98 spectrum/tracker numerical implementation,
uses a different k grid and separation grid, derives the new lognormal masked
moments via exponential tilting, and evaluates upper bivariate probabilities by
independent adaptive conditional-normal quadrature. The Gaussian tail outside
[-12,12] is bounded by 4e-33. QUADPACK absolute and relative tolerances are 2e-12.
All runs use the requested repository interpreter and warnings as errors.

Evidence files:

- `independent_formula_checkpoint.md`: formulas and disclosed exposure.
- `independent_delta_science.py`, `.log`, `.json`: independent calculations.
- `author_comparison.json`: comparison made after the independent run.

The first independent numerical run stopped with an integration warning in a
semi-infinite transformed quadrature panel for the rs=4 member near perfect mask
correlation. Replacing that semi-infinite integration with the explicitly bounded
[-12,12] domain removed the warning; no warning was suppressed. The completed run
is recorded in the current log. All six 2,000,000-sample checks of the correlated
new kernels have max absolute z score <=1.8692, using the reported Monte Carlo
standard errors. These stochastic checks corroborate the kernels, not the claimed
equal constraints.

## New nonnegative pair: valid density laws, unequal declared covariance

Let A=lambda S have variance v, Y be the standardized Gaussian mask field,
M=1[Y>c], and fw=Q(c). For I the mask is independent; for II
b0=Cov(Y,A)>0. The conditional normalizers are

    muI = exp(v/2),
    muII = exp(v/2) Q(c-b0)/fw,
    m = muII/muI.

The declared phase-centered wall contrasts are d=e^A/mu-1. Thus

    Cov(dI(x),dI(y)) = exp(Cov(Ax,Ay))-1,
    Cov(dII(x),dII(y)) = [exp(Cov(Ax,Ay))-1]/m^2.

Both laws are nonnegative and both have E[M d]=0, hence the global empty-void
mass normalization is correct. Their underlying latent S covariance is identical;
the unmasked, phase-normalized wall contrasts do **not** have the shared
unconditional connected covariance asserted in report lines 125-132, 792-795 and
813-820, and script lines 460-462 and its `shared_constraints` output. Their
unconditional contrast means are 0 (I) and 1/m-1 (II). Normalizing II by its
unconditional mean would recover the advertised covariance, but would define a
different contrast from that relative to the common phase-conditional wall mean.
Keeping a shared pre-mask lognormal *carrier* is therefore a possible narrower
reading, which must be named expressly.

| Scenario | rs Mpc | muII/muI | CovII/CovI | unmasked ball variance I | unmasked ball variance II |
|---|---:|---:|---:|---:|---:|
| GM | 1 | 2.869413263 | 0.121454552 | 0.701045808 | 0.085145205 |
| GM | 2 | 2.139808283 | 0.218398812 | 0.701045808 | 0.153107572 |
| GM | 4 | 1.623350464 | 0.379468230 | 0.701045808 | 0.266024612 |
| NW15 | 1 | 2.474113338 | 0.163365678 | 0.734489239 | 0.119990332 |
| NW15 | 2 | 2.104324763 | 0.225826274 | 0.734489239 | 0.165866968 |
| NW15 | 4 | 1.668578493 | 0.359175510 | 0.734489239 | 0.263810547 |

The JSON contains the full independently computed ball values; the table is
rounded to nine decimals. The II/I unconditional wall
covariance reduction is 62%-88% for GM and 64%-84% for NW15. This is much larger
than integration uncertainty.

The actual displayed lognormal total-rms ratios independently reproduce:

| Scenario | rs=1 | rs=2 | rs=4 |
|---|---:|---:|---:|
| GM II/I | 1.028342474 | 1.186540160 | 1.293158119 |
| NW15 II/I | 0.919395106 | 1.049504847 | 1.187905024 |

Every author's reported three-decimal moment/rms is reproduced. Maximum relative
change among nonzero wall/total/cross values against the artifact is 9.36e-6,
consistent with the different separation grids and omission of the first tiny
pair-separation panel. Near-zero independent cross terms are compared absolutely;
the author's +/-1.11e-16 terms are roundoff. This numerical agreement does not
establish the intended fixed-physical-wall-spectrum nonuniqueness proof.

**GH-F5 assessment:** PARTIALLY_RESOLVED; signed scope, positivity of the added
laws, moment kernels, normalization, and the positive integrated cross mechanism
are verified. The new assertion that the nonnegative laws retain the intended
unconditional *wall-density* covariance remains unproved and is contradicted by
their stated normalization. Treat this as a MEDIUM-HIGH scientific residual/new
delta finding. Repair options are (a) explicitly share only latent/pre-mask carrier
covariance and withdraw the stronger fixed wall-spectrum proof, or (b) construct
and independently verify two nonnegative laws with the same intended physical
wall covariance, conditional mass normalization and partition covariance. Do not
silently modify scientific equations or normalizations during the audit.

## F1-F8 scientific disposition

These are advisory dispositions for integration into the full finding matrix.
Use the prompt's exact vocabulary in the final inventory if different.

| Original | Science outcome | Basis |
|---|---|---|
| GH-F1 | RESOLVED for the narrowed proposal | Report 69-81, 205-243 and 829-840 explicitly choose the formal zero-amplitude tangent, specify unsmoothed G and G_R=G W_R, and exclude finite-small-scale derivative averaging. Uniform early centers/mass weighting agree only to first order. Independent two-state mean derivative=0.274683481680 versus tangent=0.263, reciprocal mean=1. |
| GH-F2 | RESOLVED for the seed-indexed scope | H-A9 and no material-domain extension below cell scale are explicit at 290-304 and 350-359. Ratios reproduce 0.325864869/0.389672894 for medians and 1.485416972/1.589035338 for W09. This establishes an accounting statistic, not a material boundary map. |
| GH-F3 | RESOLVED | f_v,L=f_vi(1+delta)/(1+epsilon) implies p=f_vi-df_v,L/ddelta, as corrected in 412-420 and 834-837. Threshold-only and compressed PBS remain distinct. |
| GH-F4 | Substantive interval repair RESOLVED; residual wording correction | H15 now requires constant share over both windows, and the step counterexample reproduces. Lines 598-600 still call the effective rms ratio a pointwise 'at most' propagator variation; see correction below. |
| GH-F5 | PARTIALLY_RESOLVED, scientific residual blocks stronger claim | Valid signed requalification and nonnegative kernels; unequal phase-normalized unconditional covariance invalidates the claimed shared physical wall-spectrum proof. |
| GH-F6 | Substantive science repair RESOLVED; stale contradiction remains | Direct/post-hoc/reclosure are distinguished; reclosure numbers and unscaled homogeneity upper end reproduce. Lines 883-885 still say the anchor corrects the transfer function. |
| GH-F7 | Substantive cap repair RESOLVED; stale contradiction remains | The independent cap-exceedance probabilities are 0.463502204966 and 0.478861373864; report 377-386 narrows necessity to wall-density freedom if emptiness/early field remain. Lines 893-894 still require the full S1. |
| GH-F8 | RESOLVED | W09 headlines carry formal extrapolation/H-A8, median values are a heuristic prior below epsilon=1 without a controlled error bound in report, README 171-177 and CLAUDE 500-504. No derived F-to-tracker bridge is asserted. |

## Independent new numeric checks

| Check | GM | NW15 |
|---|---:|---:|
| step kcut Mpc^-1 | 0.06604319911744 | 0.06909269510439 |
| step premise rms | 0.099900000000 | 0.099900000000 |
| step R8 rms | 7.246489589412 | 10.352904721362 |
| step constant-share upper | 0.998267555894 | 1.161784484326 |
| step/upper | 7.259065514675 | 8.911209317246 |
| PBS W09 direct | 1.121362660203 | 1.056632599471 |
| PBS W09 post-hoc | 1.088368548207 | 1.025543054970 |
| PBS W09 reclosure | 1.113687196377 | 1.045779604398 |
| PBS median direct | 0.810772266865 | 0.816058813008 |
| PBS median post-hoc | 0.786916727595 | 0.792047726472 |
| PBS median reclosure | 0.803096757651 | 0.805205777136 |

Step high/low spectral integrals are split at the independently solved cut and
recomputed at 16001 and 8001 k points per interval; R8 fractional changes are
2.69e-13/2.03e-13. The analytic PBS reclosure relation derived in the checkpoint
explains the numerical changes: a(p_a-c)=p-c; the fixed constant-share reclosure
agrees with output scaling, while a constant-share H15 upper *ratio* remains
unchanged at fixed eta and active premise cap. This is no Boltzmann calculation.

## Remaining report inconsistencies and proposed wording

1. Report 598-600: replace 'the propagator varies by at most 0.12% across the R8
   window' with 'the window-integrated rms ratio sigma/[G(0) sigma_u]-1 is
   -0.09% to -0.12% for the W09 small-seed cases and about -0.005% for the median
   cases. This is an effective statistic, not a pointwise bound over the broad
   window support. The explicit homogeneity-window calculations determine whether
   each PBS case satisfies the premise.' A closure-independent near-constant
   bound would need a separate spectral proof.
2. Report 882: shared primordial dependence is correlation, not intrinsic double
   counting. Replace with 'In law II the phase and wall-density fluctuations are
   correlated; the complete covariance retains their cross contribution.'
3. Report 883-885: replace with 'The post-hoc factor is an empirical output
   normalization at fixed closure. The reclosure variant rescales the input and
   recomputes PBS; neither establishes a verified transfer recalibration. The
   interval uses an additional adopted homogeneity premise.'
4. Report 893-894: replace 'S1 ... is required' with 'wall-density freedom is
   needed if exact empty voids and the early field are kept; the complete S1 is
   not selected by H13.'

Section 8's historical-preface sentence does not make these statements inert:
the section is partly revised in place, retains current prose, and points to
current sections. Either correct it throughout or explicitly preserve a quoted,
dated superseded block with a per-claim correction map. These residuals do not
invalidate the correctly narrowed tangent calculator, but do invalidate the
remediation record's unqualified claim that all fourteen findings are resolved.
