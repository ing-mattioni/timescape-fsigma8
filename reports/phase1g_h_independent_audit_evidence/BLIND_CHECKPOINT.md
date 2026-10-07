# Blind scientific reconstruction checkpoint (2026-10-06)

Written before opening Phase 1G-H author's report, runtime, numerics or self-audit. Inputs read: original task; audit prompt (claimed target numbers known, never treated as evidence); AGENTS; downloaded primary TeX GM, W09, NW15, EH98. Own code imports no repository module. Same-model-family claim in task is not assumed: auditor OpenAI, author reportedly Claude Opus 5.5, hence different provider/model families.

## Independent derivation
For equal mass M, V=Vw+Vv and empty voids, Vw=M/rho_w. If wall density changes by d_w and void volume by -epsilon, at first order delta_global=w*d_w+f*epsilon. At matching, delta_i=(1-fi)*d_wi+fi*epsilon. Defining p=fi*epsilon/delta_i and delta_0=(1+zi)*delta_i gives
G=DW*(1-p)+DV*p,
DW=(1-f)/(1-fi)*(t0/ti)^(2/3)/(1+zi), DV=f/[fi*(1+zi)].
The wall growing mode assumes EdS wall growth with common t; Milne voids carry fixed relative volume epsilon. Both are assumptions beyond global background conservation.

GM tracker gives f(t)=f0*q/(1-f0+f0*q), a/a0=q*(f0/f)^(1/3), gamma=1+f/2, 1+z=gamma/(gamma0*a/a0). Therefore DW=(gamma0/gamma_i)*[(1-f0)/(1-fi)]^(4/3). Its fi->0, f0->0 limit is 1-5*f0/6. Numerical values of ti/t0, fi, DW and DV independently match audit target digits. hbar=2*h_dressed*(2+f)/(4+f+4*f²); convention c radius=8/(hbar*gamma0), b=8/h_dressed. These radii also match. Convention a not inferable from the prompt alone; pending declared definition.

For Gaussian threshold seeds I=1[delta_s<-nu*sigma_s], fi=Phi(-nu). Shifting long density changes seed fraction by -phi(nu)*delta_l/sigma_s. Adding local volume compression gives epsilon=[1+phi/(fi*sigma_s)*W(kRs)]*delta_l, hence p=fi+phi/sigma_s*W(kRs). Threshold-only drops fi. Initial sigma_s must be evaluated at matching. Long-wave p=fi*Av. Void-share positivity/monotonicity is a separate class restriction, not implied by conservation. Top-hat W oscillates, so global p(k)>=fi generally fails for the PBS kernel at sufficiently large k even if its k~R8 support is effectively positive.

For a scalar Gaussian functional F(X), E[F X]/VarX=E[F'] under integrability. Multivariate Fourier form needs translational invariance and integration by parts over each mode. It is an ensemble-averaged tangent/cross-propagator. It does NOT identify a generic nonlinear field F with G X or its full power with G²P: orthogonal residual power remains. Conditional linear Gaussian projection must be stated as the chosen object.

Mass weighting vs volume weighting agrees at leading perturbative order around homogeneous FLRW, not automatically around a finite-amplitude two-phase background. A choice of a tangent about that background is mathematically possible but not uniquely the standard primordial linear density field.

For phase indicator I (mean f), regional ratio r=rho_v/rho_w, Z=w+r*f, and conditionally centered internal contrasts, let A=(I-f)_R, B=((1-I)*delta_w)_R, C=(I*delta_v)_R. Then delta_R=[-(1-r)A+B+r*C]/Z; full variance is quadratic form of PSD covariance of A,B,C. VarA<=f*w for positive normalized smoothing. Unconditional mean delta_w=0 does not guarantee E[(1-I)delta_w]=0. Empty void limit r=0 gives Var(delta_R)=(VarA+VarB-2Cov(A,B))/w² with Cauchy bounds (sigma_A+-sigma_B)²/w².

For standard normal X,Y with corr rho and cutoff a, define P=Phi2(a,a;rho), t=a*sqrt((1-rho)/(1+rho)), phi2=bivariate pdf at (a,a). Independent truncated moments:
E[X 1(X<a,Y<a)]=-(1+rho)*phi(a)*Phi(t),
E[XY 1(X<a,Y<a)]=rho*P-2*rho*a*phi(a)*Phi(t)+(1-rho²)*phi2.

Two absorbing barriers -|dv| and dc: probability to hit lower first m(dl)=(dc-dl)/(dc+|dv|); fixing final density ratio x yields total volume Z=(1-m)+m/x and void fraction (m/x)/Z. Differentiation at fixed x yields a positive contribution (1/x-1)/[Z*(dc+|dv|)] to -d lnV/d dl, besides any explicit wall-volume response.

## Initial numerical discrepancy to inspect, not yet a finding
Using literal EH98 zero-baryon T0, with q=k*theta²/omega_eff and matter normalization omega_eff, gives sigma_u(c)=1.50014 GM /1.38221 NW15, not claimed 1.1280/1.0442. Likely distinction between EH98 zero-baryon formula and baryon-corrected no-wiggle prescription; author input/provider definitions need inspection. No author formula was used to resolve this.

## Limit of domain-level mass identity
Assigning final bubbles by seed position defines a seed-indexed volume accounting measure. It is not automatically the volume inside a transported finite material top-hat when bubbles intersect its boundary. A finite-size spatial allocation kernel or explicit seed-indexed definition is necessary at R comparable to void radius. This is separate from merely evaluating Fourier convolution at R.
