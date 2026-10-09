# Independent formula checkpoint, delta audit at 89cb041

This checkpoint was written after reading the revised report and the remediation
record (therefore exposed to formulas and headline results), before reading the
author's implementation of its new lognormal evidence. It is an independent
derivation and is **not blind**. It cannot recreate the missing earlier blind
checkpoint.

Let Y be a standard Gaussian, M=1[Y>c], w=Q(c), and A=lambda S a zero-mean
Gaussian latent density with variance v. At separation r define rho=Cov(Y1,Y2),
q=Cov(A1,A2), b0=Cov(Y1,A1), br=Cov(Y1,A2). Joint Gaussian exponential tilting
shifts Y's means by its covariances with the exponent and multiplies probabilities
by the corresponding Gaussian moment-generating factor.

For an independent mask I, mu_I=E[e^A|M=1]=exp(v/2).
For the correlated mask II,

    mu_II=exp(v/2) Q(c-b0)/w,
    m=mu_II/mu_I=Q(c-b0)/w.

The wall contrast is d=e^A/mu-1, normalized by E[M d]=0. Although both
constructions have the same latent covariance q(r), their **unconditional,
connected contrast covariance** differs:

    Cov(d_I1,d_I2)=exp(q)-1,
    Cov(d_II1,d_II2)=(exp(q)-1)/m^2.

The unmasked unconditional mean is 0 for I and 1/m-1 for II. Thus the
report's simultaneous assertions of conditional-on-wall normalization and shared
unconditional wall-density covariance exp(q)-1 are incompatible if b0 != 0.
The same distinction applies to wall density expressed in common density units;
if instead the unmasked field is normalized by its own unconditional mean, its
covariance *relative to that new mean* is shared, but this field is different
from the declared wall contrast relative to the phase-conditional wall mean.

With P(a,b;rho)=Pr[Y1>a,Y2>b], T=exp(v/2)/mu, the independent moment reconstruction
is

    Kww(r)=T^2 exp(q) P(c-b0-br,c-b0-br;rho)
           -2 T P(c-b0,c-br;rho)+P(c,c;rho),
    Kpw(r)=T P(c-br,c-b0;rho)-P(c,c;rho),
    Kpp(r)=P(c,c;rho)-w^2.

For I set b0=br=0 and T=1. The global contrast in empty voids is
(M-w+M d)/w. Its connected covariance is

    [Kpp+Kww+2 Kpw]/w^2.

The top-hat variance is the pair-separation integral with density
3 u^2(1-3u/4+u^3/16), u=r/R in [0,2]. This independent calculation can
reproduce the output numbers without establishing equal unconditional
wall-contrast covariance between laws.

For PBS with sigma_s scaled by factor a, p_a(k)=c+(p(k)-c)/a. Hence
the rescaled spectrum gives amplitude a G_a(k)=a D_W+(D_V-D_W)
[a c+p(k)-c]. Compared with post-hoc a G(k), the reclosure correction is
(1-a)(D_V-D_W)(p(k)-c). For constant p held fixed, the reclosure and
post-hoc results agree exactly. A constant-share homogeneity upper endpoint
eta sigma_u(R8)/sigma_u(Rhom) is independent of a, provided the same premise
and active cap hold, whereas its lower endpoint scales by a.

The cap-exceedance probability at last scattering is Q(cap/sigma_LS),
cap=fv_LS/(1-fv_LS), sigma_LS=sigma_u(R)/(1+z_LS).

For a two-state equal-mass H3 example with epsilon=0,
1+delta=[fw/(1+delta_w)+fv]^-1 and
partial delta/partial delta_w=fw(1+delta)^2/(1+delta_w)^2.
The mean derivative generally differs from fw, its zero-amplitude tangent.
