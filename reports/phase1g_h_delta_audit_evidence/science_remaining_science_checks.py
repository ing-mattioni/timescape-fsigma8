"""Complete the independent delta checks; no project imports and not blind.

Signed Gaussian conditional moments are independently evaluated from Gaussian
regression and orthant moments [1G-H] H21. The conditional-normal probability
integrator is the independent one in independent_delta_science.py.
Gates (set before this extension executes): central nonzero moment discrepancy
2e-5 relative (different k/separation grids, adequate for three decimals),
negative-density probability 2e-8 absolute, near-zero cross moment 2e-12 absolute,
finite-lambda moment comparison 2e-2 relative (lambda sigma=0.01, error O(0.01)),
linear-limit numerical reproduction 2e-5 relative. No project tests are imported.
"""
from pathlib import Path
import importlib.util,json,math
import numpy as np
from scipy.integrate import quad,simpson
from scipy.special import ndtr,ndtri,spherical_jn

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('delta',HERE/'independent_delta_science.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
ind=d.ind
TOL={'negative_density_abs':2e-8,'near_zero_cross_abs':2e-12,
     'central_moment_rel':2e-5,'finite_lambda_limit_rel':2e-2,'linear_limit_reproduction_rel':2e-5}

def signed_and_limit(t,anchor,ell,segments=720,include_zero=False):
 k=np.geomspace(1e-5,80,12001);lk=np.log(k);R=800/t['H'];fw=1-t['f'];c=float(ndtri(t['f']))
 D=t['DW']*(1-t['fi'])/fw;S=ind.spectrum(k*D,t['omega_eff'])*D*D*anchor*anchor
 w=np.ones(len(k));w[1:-1:2]=4;w[2:-1:2]=2;w*=np.diff(lk)[0]/3
 r=np.linspace(0,2*R,segments+1)[1:];pair=3*r*r/R**3*(1-3*r/(4*R)+r**3/(16*R**3))
 def radial_integral(a):
  if include_zero:return float(simpson(np.r_[0.,pair*a],x=np.r_[0.,r]))
  return float(simpson(pair*a,x=r))
 bd=spherical_jn(0,r[:,None]*k[None,:])*(S*w)[None,:]
 xi=bd.sum(axis=1);v0=float(np.dot(S,w));gl=np.exp(-.5*(k*ell)**2)
 vg=float(np.dot(S*gl*gl,w));rho=bd@(gl*gl)/vg
 x0=float(np.dot(S*gl,w))/math.sqrt(vg);xr=bd@gl/math.sqrt(vg)
 phi=math.exp(-c*c/2)/math.sqrt(2*math.pi);mu=x0*phi/fw
 P=np.array([d.upper(c,c,rr) for rr in rho]);z=c*np.sqrt((1-rho)/(1+rho));Q=ndtr(-z)
 pdf=np.exp(-c*c/(1+rho))/(2*np.pi*np.sqrt(1-rho*rho))
 m1=(1+rho)*phi*Q
 m11=P+c*(1+rho*rho)*phi*Q+rho*(1-rho*rho)*pdf
 m12=rho*P+2*rho*c*phi*Q+(1-rho*rho)*pdf
 plus=(x0+xr)/(2*(1+rho));minus=(x0-xr)/(2*(1-rho))
 regxy=(x0+xr)**2/(2*(1+rho))-(x0-xr)**2/(2*(1-rho))
 eww=2*plus*plus*(m11+m12)-2*minus*minus*(m11-m12)+(xi-regxy)*P
 ew=2*plus*m1
 kw=eww-2*mu*ew+mu*mu*P;kp=ew-mu*P
 signed={}
 for name,a,b in [('I',P*xi,np.zeros_like(xi)),('II',kw,kp)]:
  signed[name]={'wall_moment':radial_integral(a),
                'partition_wall_moment':radial_integral(b)}
 negI=float(ndtr(-1/math.sqrt(v0)));ss=math.sqrt(v0-x0*x0)
 negII=quad(lambda g:math.exp(-g*g/2)/math.sqrt(2*math.pi)*float(ndtr((mu-1-x0*g)/ss)),
            c,np.inf,epsabs=2e-12,epsrel=2e-12,limit=200)[0]/fw
 lam=math.sqrt(1e-4/v0);limits={}
 for name,corr in [('I',False),('II',True)]:
  kk=np.array([d.kernels(c,fw,float(rho[i]),lam*lam*float(xi[i]),
                        lam*x0 if corr else 0.,lam*float(xr[i]) if corr else 0.) for i in range(len(r))])
  wm=radial_integral(kk[:,1])/(lam*lam)
  cm=radial_integral(kk[:,2])/lam
  wr=wm/signed[name]['wall_moment']-1
  cr=cm/signed[name]['partition_wall_moment']-1 if corr else None
  assert abs(wr)<=TOL['finite_lambda_limit_rel']
  if corr:assert abs(cr)<=TOL['finite_lambda_limit_rel']
  else:assert abs(cm)<=TOL['near_zero_cross_abs']
  limits[name]=dict(wall_moment_over_lambda2=wm,partition_wall_moment_over_lambda=cm,
                    wall_relative_to_signed=wr,cross_relative_to_signed=cr)
 return dict(signed_moments=signed,negative_density_given_wall={'I':negI,'II':negII},
             linear_limit=dict(lambda_latent=lam,latent_variance=1e-4,laws=limits),
             conditional_mean_signed_II=mu)

def run():
 first=json.loads((HERE/'independent_delta_science.json').read_text());anchor=first['anchor']
 author=json.loads((HERE.parents[1]/'repo/artifacts/independent/phase1g_h_global_variance_closure.json').read_text())
 result=dict(tolerances=TOL,cases={},max_discrepancies={})
 maxneg=maxlim=maxsigned=0.;rows=[]
 for name,an,f,H,fmed in [('GM','PAPER_REFERENCE',.737,73.03,2.40456),('NW15','NW15_CMB_FIT',.627,61,2.80045)]:
  t=ind.tracker(f,H);S=ind.spectrum(ind.K,t['omega_eff']);dg=t['DV']-t['DW']
  R=8/.674*(ind.OMREF/t['omega_eff'])**(1/3);factor=(t['fi']/f)**(1/3)
  nu=-float(ndtri(t['fi']));phi=math.exp(-nu*nu/2)/math.sqrt(2*math.pi)
  rec={}
  for seed,rs in [('W09',1500/H*factor/t['gamma']),('F_median',fmed/(H/100)*factor)]:
   p=t['fi']+phi/(ind.sig(S,rs)/1091)*ind.W(ind.K*rs)
   direct=ind.sig(S,R,t['DW']+dg*p);post=anchor*direct
   re=ind.sig(S*anchor*anchor,R,t['DW']+dg*(t['fi']+(p-t['fi'])/anchor))
   rec[seed]=dict(direct=direct,post_hoc=post,reclosure=re,ratio=re/post)
   rows.append(dict(scenario=name,convention='a_equal_lagrangian_mass',seed=seed,**rec[seed]))
  for seed,r in first['cases'][name]['direct_reclosure_cap']['reclosure'].items():
   rows.append(dict(scenario=name,convention='c_bare_volume_average',seed=seed,
                    direct=r['direct'],post_hoc=r['post'],reclosure=r['reclosure'],ratio=r['ratio_reclosure_over_post']))
  signed=signed_and_limit(t,anchor,first['cases'][name]['nonnegative_pair']['ell_Mpc'])
  ap=author['two_phase_covariance'][an]['gaussian_threshold_pair'];comparison={}
  for law,al in [('I','I_independent'),('II','II_same_field')]:
   nr=abs(signed['negative_density_given_wall'][law]-ap['negative_wall_density_probability'][al]);maxneg=max(maxneg,nr)
   assert nr<=TOL['negative_density_abs']
   comparison[law]={'negative_density_abs_difference':nr}
   for key in ('wall_moment','partition_wall_moment'):
    av=ap['laws'][al][key];iv=signed['signed_moments'][law][key]
    if abs(av)<=1e-14:assert abs(iv-av)<=TOL['near_zero_cross_abs'];continue
    err=abs(iv/av-1);maxsigned=max(maxsigned,err)
    comparison[law][key+'_rel_discrepancy']=err
   for ik,ak in [('wall_moment_over_lambda2','wall_moment_over_lam2'),('partition_wall_moment_over_lambda','partition_wall_moment_over_lam')]:
    av=ap['nonnegative_lognormal_pair']['linear_limit']['laws'][al][ak];iv=signed['linear_limit']['laws'][law][ik]
    if abs(av)<=1e-14:assert abs(iv-av)<=TOL['near_zero_cross_abs'];continue
    err=abs(iv/av-1);maxlim=max(maxlim,err)
    comparison[law][ik+'_rel_discrepancy']=err
  result['cases'][name]=dict(convention_a_reclosure=rec,signed_and_linear_limit=signed,author_comparison=comparison)
 result['reclosure_table']=rows
 result['max_discrepancies']=dict(negative_density_absolute=maxneg,central_signed_moment_relative=maxsigned,linear_limit_moment_relative=maxlim)
 result['central_moment_gate_met']=maxsigned<=TOL['central_moment_rel']
 result['linear_limit_reproduction_gate_met']=maxlim<=TOL['linear_limit_reproduction_rel']
 result['gate_status']='VERIFIED_WITH_DEVIATION' if not (result['central_moment_gate_met'] and result['linear_limit_reproduction_gate_met']) else 'VERIFIED'
 (HERE/'remaining_science_checks.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 print(json.dumps(result,indent=2,allow_nan=False))

if __name__=='__main__':run()
