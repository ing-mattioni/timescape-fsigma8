"""Independent Phase 1G-H audit calculations. No project imports.

Blind tracker/mass bookkeeping precedes this reconciliation script (see
BLIND_CHECKPOINT.md). Transfer is now explicitly EH98 baryon-corrected no-wiggle,
not literal zero baryon. Inputs are the author's declared inputs; equations are
independently evaluated with a different dense integration grid. Covariance uses
conditional-normal integration for the bivariate CDF; analytic moments are
checked against independent 1-D integration and seeded Monte Carlo.
"""
import hashlib,json,math,pathlib,os
import numpy as np
from scipy.integrate import quad,quad_vec,simpson
from scipy.optimize import brentq
from scipy.special import ndtr,ndtri,spherical_jn
from scipy.stats import multivariate_normal

ROOT=pathlib.Path(__file__).resolve().parent
REPO=ROOT.parents[1]
SOURCE_ROOT=pathlib.Path(os.environ.get('TIMESCAPE_AUDIT_SOURCE_DIR',str(ROOT/'sources')))
OMREF=.315*.674**2
FB=.02237/OMREF
K=np.geomspace(1e-7,1e5,120001); L=np.log(K)
PHI=lambda x: np.exp(-np.asarray(x)**2/2)/np.sqrt(2*np.pi)
def W(x):
 x=np.asarray(x); a=np.abs(x)<1e-3; y=np.empty_like(x)
 y[a]=1-x[a]**2/10+x[a]**4/280-x[a]**6/15120
 y[~a]=3*(np.sin(x[~a])-x[~a]*np.cos(x[~a]))/x[~a]**3
 return y
def spectrum(k,om,fb=FB):
 s=44.5*np.log(9.83/om)/np.sqrt(1+10*(om*fb)**.75)
 ag=1-.328*np.log(431*om)*fb+.38*np.log(22.3*om)*fb*fb
 shape=om*(ag+(1-ag)/(1+(.43*k*s)**4))
 q=k*(2.7255/2.7)**2/shape
 ll=np.log(2*np.e+1.8*q); tt=ll/(ll+(14.2+731/(1+62.5*q))*q*q)
 return .16*2.1e-9*(k/.05)**(-.0351)*(k*2997.92458)**4*tt**2/om**2
def sig(S,R,G=1,k=K):
 return float(np.sqrt(simpson(S*W(k*R)**2*G**2,x=np.log(k))))
def tracker(f,H):
 gamma=1+f/2; hb=H/100*2*(2+f)/(4+f+4*f*f)
 def fi_at(q):return f*q/(1-f+f*q)
 def zin(q):return (1+fi_at(q)/2)/(gamma*q*(f/fi_at(q))**(1/3))-1
 q=brentq(lambda q:zin(q)-1090,1e-8,.01,xtol=1e-19,rtol=1e-14)
 fi=fi_at(q); dw=(1-f)/(1-fi)*q**(-2/3)/1091; dv=f/fi/1091
 om=.5*(1-f)*(2+f)*hb*hb
 return dict(f=f,H=H,hbar=hb,gamma=gamma,q=q,fi=fi,DW=dw,DV=dv,omega_eff=om)
def cdf_upper(c,rho):
 s=np.sqrt(1-rho*rho)
 return quad(lambda x:float(PHI(x)*ndtr((rho*x-c)/s)),c,np.inf,epsabs=2e-12,epsrel=2e-12,limit=200)[0]
def moments(c,r):
 P=cdf_upper(c,r); z=c*np.sqrt((1-r)/(1+r)); q=ndtr(-z)
 pdf2=np.exp(-c*c/(1+r))/(2*np.pi*np.sqrt(1-r*r))
 m1=(1+r)*PHI(c)*q
 m11=P+c*(1+r*r)*PHI(c)*q+r*(1-r*r)*pdf2
 m12=r*P+2*r*c*PHI(c)*q+(1-r*r)*pdf2
 return np.array([P,m1,m11,m12])
def orthant_verification():
 out=[]; rng=np.random.default_rng(20261007)
 for c,r in [(-1.,-.6),(0.,0.),(.634,.3),(.634,.9),(2.,.999)]:
  s=np.sqrt(1-r*r)
  def fun(x):
   q=ndtr((r*x-c)/s); dens=PHI((c-r*x)/s)
   return PHI(x)*np.array([q,x*q,x*x*q,x*(r*x*q+s*dens)])
  direct=quad_vec(fun,c,np.inf,epsabs=2e-11,epsrel=2e-11)[0]
  analytic=moments(c,r)
  x=rng.standard_normal(1500000); y=r*x+s*rng.standard_normal(len(x)); mask=(x>c)&(y>c)
  vals=np.array([mask,mask*x,mask*x*x,mask*x*y],float)
  estimates=vals.mean(axis=1); sem=vals.std(axis=1,ddof=1)/np.sqrt(len(x))
  # scipy CDF is independently randomized in modern scipy; request explicit RNG.
  cdf=float(multivariate_normal.cdf([-c,-c],cov=[[1,r],[r,1]],maxpts=2000000,abseps=1e-10,releps=1e-10,rng=rng))
  out.append(dict(c=c,rho=r,analytic=analytic.tolist(),quadrature=direct.tolist(),max_abs_error=float(np.max(np.abs(analytic-direct))),cdf=cdf,cdf_error=abs(cdf-analytic[0]),mc=estimates.tolist(),mc_sem=sem.tolist(),mc_max_z=float(np.max(np.abs(estimates-analytic)/sem))))
 return out
def covariance(t,anchor,sp,R):
 # Grid is independent (12001 k, 960 separation intervals vs author's 6001/480).
 k=np.geomspace(1e-5,80,12001); logk=np.log(k); dwall=t['DW']*(1-t['fi'])/(1-t['f'])
 d2=spectrum(k*dwall,t['omega_eff'])*dwall*dwall*anchor*anchor
 rr=np.linspace(0,2*R,961)[1:]; pair=3*rr**2/R**3*(1-3*rr/(4*R)+rr**3/(16*R**3))
 # Composite Simpson for uniform log grid.
 weights=np.ones(len(k));weights[1:-1:2]=4;weights[2:-1:2]=2;weights*=np.diff(logk)[0]/3
 bessel=spherical_jn(0,rr[:,None]*k[None,:]); bd=bessel*(d2*weights)[None,:]
 xi=bd.sum(axis=1);v0=float(np.dot(d2,weights));fw=1-t['f'];c=float(ndtri(t['f']))
 def tables(ell):
  g=np.exp(-.5*(k*ell)**2);v=float(np.dot(d2*g*g,weights))
  return bd@(g*g)/v, float(np.dot(d2*g,weights))/np.sqrt(v), bd@g/np.sqrt(v)
 def vari(ell):
  rho,_,_=tables(ell); P=np.array([cdf_upper(c,r) for r in rho]);return simpson(pair*(P-fw*fw),x=rr)/fw**2
 ell=brentq(lambda ell:vari(ell)-sp*sp,.02,20,xtol=2e-10)
 rho,x0,xr=tables(ell);mu=x0*PHI(c)/fw
 M=np.array([moments(c,r) for r in rho]);P=M[:,0]
 # Gaussian regression diagonalized into symmetric/antisymmetric components.
 # E[w1 w2 | g1,g2] = u^2*(g1+g2)^2 - v^2*(g1-g2)^2 + residual.
 plus=(x0+xr)/(2*(1+rho));minus=(x0-xr)/(2*(1-rho))
 reg_xy=(x0+xr)**2/(2*(1+rho))-(x0-xr)**2/(2*(1-rho))
 eww=2*plus**2*(M[:,2]+M[:,3])-2*minus**2*(M[:,2]-M[:,3])+(xi-reg_xy)*P
 ew=2*plus*M[:,1]
 wallII=eww-2*mu*ew+mu*mu*P;crossII=ew-mu*P
 laws={}
 for name,kw,kc in [('I',P*xi,np.zeros_like(xi)),('II',wallII,crossII)]:
  vp=float(simpson(pair*(P-fw*fw),x=rr))/fw**2
  vw=float(simpson(pair*kw,x=rr))/fw**2
  cx=2*float(simpson(pair*kc,x=rr))/fw**2
  laws[name]=dict(partition_rms=np.sqrt(vp),wall_rms=np.sqrt(vw),cross_term=cx,total=np.sqrt(vp+vw+cx))
 # One-point actual density is proportional to 1+w (law I), 1+w-mu (law II).
 residual=np.sqrt(v0-x0*x0)
 negI=float(ndtr(-1/np.sqrt(v0)))
 negII=quad(lambda gg:float(PHI(gg)*ndtr((mu-1-x0*gg)/residual)),c,np.inf,epsabs=1e-12)[0]/fw
 # 4-variate MC check at r approximately R/2 (not positivity truncated).
 j=int(np.argmin(np.abs(rr-R/2)));Cov=np.array([[1,rho[j],x0,xr[j]],[rho[j],1,xr[j],x0],[x0,xr[j],v0,xi[j]],[xr[j],x0,xi[j],v0]])
 rng=np.random.default_rng(202610071); n=2000000; samples=rng.multivariate_normal(np.zeros(4),Cov,size=n)
 i1=(samples[:,0]>c);i2=(samples[:,1]>c);b1=i1*(samples[:,2]-mu);b2=i2*(samples[:,3]-mu)
 vals=np.array([(i1-fw)*(i2-fw),b1*b2,(i1-fw)*b2]);av=vals.mean(axis=1);sem=vals.std(axis=1,ddof=1)/np.sqrt(n)
 expected=np.array([P[j]-fw*fw,wallII[j],crossII[j]])
 return dict(ell=ell,wall_point_rms=np.sqrt(v0),conditional_mean_lawII=mu,cross0=x0,laws=laws,negative_density_given_wall=dict(I=negI,II=negII),MC4=dict(r=rr[j],expected=expected.tolist(),observed=av.tolist(),sem=sem.tolist(),max_z=float(np.max(np.abs(av-expected)/sem))),pair_norm=float(simpson(pair,x=rr)))
def run():
 om_l=.315;growth=2.5*om_l*quad(lambda a:1/(a**3*(om_l/a**3+1-om_l)**1.5),0,1,epsabs=1e-12)[0]
 ref=sig(spectrum(K,OMREF),8/.674)*growth;anchor=.8111/ref
 results=dict(method='no project imports; independent logarithmic grid / conditional-normal integration',omega_reference=OMREF,lcdm_growth=growth,planck_eh_sigma=ref,anchor=anchor,cases={})
 for name,f,H,fmed,sp,si in [('GM',.737,73.03,2.40456,.3264,.9316),('NW15',.627,61,2.80045,.3036,.9403)]:
  t=tracker(f,H);S=spectrum(K,t['omega_eff']);fi=t['fi'];dW=t['DW'];dV=t['DV'];dg=dV-dW
  radii=dict(c=8/(t['hbar']*t['gamma']),a=8/.674*(OMREF/t['omega_eff'])**(1/3),b=800/H)
  nu=-ndtri(fi);factor=(fi/f)**(1/3)
  seeds=dict(W09=1500/H*factor/t['gamma'],F_median=fmed/(H/100)*factor,SvdW=1500/H/1.72,W09_half=750/H*factor/t['gamma'],W09_double=3000/H*factor/t['gamma'])
  shapes={key:fi+PHI(nu)/(sig(S,rs)/1091)*W(K*rs) for key,rs in seeds.items()}
  shapes['W09_threshold_only']=shapes['W09']-fi
  rows={}
  for conv,R in radii.items():
   clos={}
   for key,p in dict(p0=np.zeros_like(K),pmin=np.full_like(K,fi),p1=np.ones_like(K),**shapes).items():
    G=dW+dg*p;su=sig(S,R);sv=sig(S,R,G);wvec=dW*(1-p);vvec=dV*p
    sw=sig(S,R,wvec);svv=sig(S,R,vvec)
    cross=float(simpson(S*W(K*R)**2*wvec*vvec,x=L));g0=float(G[0])
    clos[key]=dict(sigma=sv,anchored=sv*anchor,p0=float(p[0]),G0=g0,Av=float(p[0])/fi,X_SU=g0/growth,epsilon_rms=sig(S,R,p)/(1091*fi),scale_dependence=sv/su/g0-1,coherence=cross/sw/svv if sw*svv else None,wall_rms=sw,void_rms=svv)
   intervals={}
   for key,l,eta in [('100_10',100,.1),('150_10',150,.1),('100_06',100,.06),('cell100',100*(3/(4*np.pi))**(1/3),.1)]:
    rh=R*l/8;hi=min(dV,eta/sig(S,rh));low=dW+dg*fi
    intervals[key]=dict(lower=low*su,upper=hi*su,p_upper=(hi-dW)/dg,W09_hom=sig(S,rh,dW+dg*shapes['W09']))
   rows[conv]=dict(R=R,unit_sigma=su,closures=clos,intervals=intervals)
  R=radii['c'];scan=[]
  for ll in [6,7,8,9,10,12]:scan.append(dict(L=ll,lower=sig(S,R*ll/8,dW+dg*fi),W09=sig(S,R*ll/8,dW+dg*shapes['W09'])))
  capR=np.exp(brentq(lambda lr:sig(S,np.exp(lr))/1091-fi/(1-fi),np.log(20),np.log(3000),xtol=2e-12))
  p1R=np.exp(brentq(lambda lr:sig(S,np.exp(lr),dV)-.1,np.log(20),np.log(3000),xtol=2e-12))
  dc=3*(12*np.pi)**(2/3)/20;dv=-2.7171803438378705;x=.20472233400490963;m=dc/(dc+abs(dv));z=1-m+m/x;bias=1+(1/x-1)/(z*(dc+abs(dv)));wall0=dW*(1-fi)/(1-f)
  As=[]
  for fac in [.5,2]:
   p=fi+(shapes['W09']-fi)/np.sqrt(fac); ratio=sig(S*fac,R,dW+dg*p)/rows['c']['closures']['W09']['sigma']
   As.append(dict(factor=fac,ratio=ratio,derivative=np.log(ratio)/np.log(fac)))
  # Counterexample to using H15 on the full pointwise-monotone class.
  rhoH=R*100/8
  def stepped(kcut):return fi+(1-fi)*(K>kcut)
  # Search actual grid cut since this is discontinuous in kcut.
  cuts=np.geomspace(.01,1,401);valid=[q for q in cuts if sig(S,rhoH,dW+dg*stepped(q))<=.1];cut=valid[0];ps=stepped(cut)
  out=dict(tracker=t,radii=radii,seeds=seeds,conventions=rows,radius_scan=scan,capacity_R=capR,capacity_dressed_h=capR*H/100,capacity_ratio_c=sig(S,R)/(1091*fi/(1-fi)),p1_hom_R=p1R,p1_hom_bare_h=p1R*t['gamma']*t['hbar'],sigma_slope_p=dg*sig(S,R),two_barrier=dict(m=m,fv=m/x/z,b=bias,G=bias*wall0,sigma=bias*wall0*sig(S,R)),As=As,H15_scale_dependent_counterexample=dict(kcut=cut,sigma_hom=sig(S,rhoH,dW+dg*ps),sigma_R8=sig(S,R,dW+dg*ps),constant_share_upper=rows['c']['intervals']['100_10']['upper']),E_reference=dict(rms=np.hypot(sp,si),cauchy=[si-sp,si+sp]))
  out['covariance']=covariance(t,anchor,sp,radii['b'])
  results['cases'][name]=out
 sources=json.loads((REPO/'reports/phase1g_h_global_variance_closure_inventory.json').read_text())['sources'];hashes={}
 for name,rec in sources.items():
  if not isinstance(rec,dict):continue
  file=SOURCE_ROOT/(name+'.tar') if name=='SvdW04' else SOURCE_ROOT/name/rec['file']
  if not file.exists():
   hashes[name]=dict(status='NOT_REPEATED_SOURCE_CACHE_ABSENT',expected=rec.get('sha256',rec.get('eprint_sha256')))
   continue
  actual=hashlib.sha256(file.read_bytes()).hexdigest();expected=rec.get('sha256',rec.get('eprint_sha256'))
  hashes[name]=dict(path=str(file),expected=expected,actual=actual,match=actual==expected)
 results['source_hashes']=hashes;results['orthant_checks']=orthant_verification()
 # Exact H3 ensemble derivative at normalized, positive, non-degenerate small scales.
 f=.737;w=1-f;u=.5;s=np.array([-u/(1+u),u/(1-u)])
 F=lambda x:1/(w/(1+x)+f)-1
 results['ensemble_counterexample']=dict(f=f,u=u,small_wall_contrasts=s.tolist(),equal_mass_mean_reciprocal=float(np.mean(1/(1+F(s)))),mean_contrast=float(F(s).mean()),mean_tangent=float(np.mean(w/(1+f*s)**2)),deterministic_H4_tangent=w,central_difference=float(np.mean((F(s+1e-6)-F(s-1e-6))/(2e-6))))
 (ROOT/'independent_results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps({k:results[k] for k in ['planck_eh_sigma','anchor','source_hashes','ensemble_counterexample']},indent=2))
 for n,c in results['cases'].items():print(n,json.dumps({k:c[k] for k in ['radii','covariance','H15_scale_dependent_counterexample']},indent=2))
if __name__=='__main__':run()
