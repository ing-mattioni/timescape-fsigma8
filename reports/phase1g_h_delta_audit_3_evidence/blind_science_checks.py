"""Independent audit normalization/limit/dimension checks, not author tests."""
import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr
from blind_science_reconstruction import tail_pair, ball_nodes, window, Q, phi, rms, tracker, first_panel, CASES, latent

checks={}
# Binary mass-mask algebra for a general valid 2-point distribution, with
# three nonconstant wall-density realizations explicitly normalized once.
p=np.array([.16,.19,.19,.46]); W=np.array([[0,0],[0,1],[1,0],[1,1]])
fw=.65;psi=np.array([[0,0],[0,1.3],[1.3,0],[.8760869565217392,.8760869565217392]])
mass=W*psi/fw
checks['mask_H25_finite_distribution_residual']=float(np.dot(p,(mass[:,0]-1)*(mass[:,1]-1))-(np.dot(p,W[:,0]*W[:,1]*psi[:,0]*psi[:,1])/fw**2-1))
assert abs(checks['mask_H25_finite_distribution_residual'])<1e-14
c=np.array([-.4,.2,.7]);rho=np.array([-.4,.35,.9])
pl=tail_pair(c,rho);direct=[]
for ci,ri in zip(c,rho):
    si=math.sqrt(1-ri*ri)
    direct.append(quad(lambda x:float(phi(x)*Q((ci-ri*x)/si)),ci,12,epsabs=1e-13,epsrel=1e-13)[0])
checks['Plackett_vs_adaptive_conditional_tail_max_abs']=float(np.max(abs(pl-direct)))
assert checks['Plackett_vs_adaptive_conditional_tail_max_abs']<1e-12
checks['tail_independent_limit_abs']=float(abs(tail_pair(np.array([.7]),np.array([0]))[0]-Q(.7)**2))
checks['tail_coincident_limit_abs']=float(abs(tail_pair(np.array([.7]),np.array([1]))[0]-Q(.7)))
assert checks['tail_coincident_limit_abs']<1e-11
# Lognormal wall normalizer via independent 1-D quadrature (exponential tilt).
ci=.7;k0=.65
m=Q(ci-k0)/Q(ci)
q=quad(lambda z:float(phi(z)*math.exp(k0*z-k0*k0/2)),ci,12,epsabs=1e-13,epsrel=1e-13)[0]/Q(ci)
checks['lognormal_m_normalisation_quadrature_residual']=float(q-m)
assert abs(q-m)<1e-12
# Dimensionless pair-weight normalization and spherical Fourier identity.
r,bw=ball_nodes(7.3,1600)
ks=np.array([0,.03,.1,.7,2,5])
checks['ball_density_norm_abs']=float(abs(sum(bw)-1))
got=np.sinc(np.outer(ks,r)/math.pi)@bw
want=window(ks*7.3)**2
checks['ball_window_pair_identity_max_abs']=float(np.max(abs(got-want)))
assert checks['ball_window_pair_identity_max_abs']<1e-12
# General signed-Gaussian Hessian formula independently compared to
# truncated 2-D covariance regression + 1-D quadratures.
ci=.4;ri=.45;k0=.35;kr=.15;KY=.12
si=math.sqrt(1-ri*ri);pp=tail_pair(np.array([ci]),np.array([ri]))[0]
integ=lambda f:quad(f,ci,12,epsabs=1e-13,epsrel=1e-13)[0]/pp
M1=integ(lambda x:float(x*phi(x)*Q((ci-ri*x)/si)))
M11=integ(lambda x:float(x*x*phi(x)*Q((ci-ri*x)/si)))
M12=integ(lambda x:float(x*phi(x)*(ri*x*Q((ci-ri*x)/si)+si*phi((ci-ri*x)/si))))
a=(k0-ri*kr)/(1-ri*ri);b=(kr-ri*k0)/(1-ri*ri)
residual=KY-(a*kr+b*k0)
EYreg=(a+b)*M1;EYYreg=2*a*b*M11+(a*a+b*b)*M12+residual
h=ci*math.sqrt((1-ri)/(1+ri));d=phi(ci)*Q(h);off=phi(ci)*phi(h)/si;diag=ci*d-ri*off
EYtilt=(k0+kr)*d/pp;EYYtilt=KY+(2*k0*kr*diag+(k0*k0+kr*kr)*off)/pp
checks['signed_Gaussian_first_moment_regression_vs_tilt_abs']=float(abs(EYreg-EYtilt))
checks['signed_Gaussian_second_moment_regression_vs_tilt_abs']=float(abs(EYYreg-EYYtilt))
assert max(abs(EYreg-EYtilt),abs(EYYreg-EYYtilt))<1e-12
checks['dimensions']='k in Mpc^-1, r/ell/r_s in Mpc, covariances and all variances dimensionless; G cancels from omega_m'
checks['limiting_interpretation']='law I kappa0=kappa(r)=0 gives m=1 and C_W=1+xi (signed), exp(KY) (lognormal); fixed P11 and C_W specify unique variance'
Path(__file__).with_name('blind_science_checks_results.json').write_text(json.dumps(checks,indent=2,allow_nan=False)+'\n')
print(json.dumps(checks,indent=2))
