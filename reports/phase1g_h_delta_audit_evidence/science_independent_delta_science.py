"""Independent numerical delta audit at 89cb041; no project module imports.

Formulas: independent_formula_checkpoint.md (not a blind checkpoint), [1G-H]
H3/H8/H9/H10/H12/H13/H15/H21; EH98 no-wiggle transfer (26),(28)-(31), with
the declared Planck fixed baryon fraction. The latter numerical implementation
is reused from the first independent audit, independent_numerics.py.
New lognormal moments use independent scipy.integrate.quad rather than the
author's orthant integration. Output does not certify equal covariance.
"""
from pathlib import Path
import importlib.util
import json
import math
import numpy as np
from scipy.integrate import quad, simpson
from scipy.optimize import brentq
from scipy.special import ndtr, ndtri, spherical_jn

HERE=Path(__file__).resolve().parent
OLD=Path('/workspace/scratch/7660b169d7d7/audit_work/blind_science')
REPO=Path('/workspace/scratch/031c29bb1e06/repo')
module_spec=importlib.util.spec_from_file_location('first_independent',OLD/'independent_numerics.py')
ind=importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(ind)

def upper(a,b,rho):
    """Independent upper bivariate Gaussian probability; explicit 2e-12 tolerance."""
    ss=math.sqrt(1-rho*rho)
    # Bound the discarded standard-normal tail at |x|>12 by 2 Q(12),
    # <4e-33, rather than use QUADPACK's semi-infinite transformation. The
    # latter emitted a false slow-convergence warning for a narrow transition
    # near rho=1 on the rs=4 member. No warning is suppressed.
    lower=max(a,-12.)
    if lower>=12.:return 0.
    knots=sorted({lower,12.,*(max(lower,min(12.,v/rho))
                 for v in (b-8*ss,b,b+8*ss))}) if rho>0 else [lower,12.]
    fun=lambda x:math.exp(-x*x/2)/math.sqrt(2*math.pi)*float(ndtr((rho*x-b)/ss))
    return sum(quad(fun,l,h,epsabs=2e-12,epsrel=2e-12,limit=200)[0]
               for l,h in zip(knots[:-1],knots[1:]) if h>l)

def kernels(c,fw,rho,q,b0,br):
    """Exponential tilting derived in independent_formula_checkpoint.md."""
    T=fw/float(ndtr(b0-c))
    P=upper(c,c,rho)
    Ep=T*upper(c-br,c-b0,rho)
    Epp=T*T*math.exp(q)*upper(c-b0-br,c-b0-br,rho)
    return P-fw*fw,Epp-2*Ep+P,Ep-P

def new_pairs(t,anchor,target_partition,known_ell):
    k=np.geomspace(1e-5,80,12001);lnk=np.log(k)
    dwall=t['DW']*(1-t['fi'])/(1-t['f']);R=800/t['H']
    d2=ind.spectrum(k*dwall,t['omega_eff'])*dwall*dwall*anchor*anchor
    r=np.linspace(0,2*R,721)[1:]
    pair=3*r*r/R**3*(1-3*r/(4*R)+r**3/(16*R**3))
    weights=np.ones(len(k));weights[1:-1:2]=4;weights[2:-1:2]=2;weights*=np.diff(lnk)[0]/3
    bd=spherical_jn(0,r[:,None]*k[None,:])*(d2*weights)[None,:]
    xi=bd.sum(axis=1);fw=1-t['f'];c=float(ndtri(t['f']))
    # Independent re-calibration of partition covariance, local bracket around
    # previous independent audit ell; old ell is disclosed, not an author result.
    def tables(ell):
        gl=np.exp(-.5*(k*ell)**2);vg=float(np.dot(d2*gl*gl,weights))
        return gl,vg,bd@(gl*gl)/vg
    def partition_var(ell):
        _,_,rho=tables(ell)
        P=np.array([upper(c,c,rr) for rr in rho])
        return float(simpson(pair*(P-fw*fw),x=r))/fw**2
    ell=brentq(lambda e:partition_var(e)-target_partition**2,
               known_ell*.9,known_ell*1.1,xtol=2e-10,rtol=1e-12)
    gl,vg,rho=tables(ell)
    target=float(simpson(pair*xi,x=r))
    members={}
    for rs in (1.,2.,4.):
        gs=np.exp(-.5*(k*rs)**2);vs=float(np.dot(d2*gs*gs,weights))
        xs=bd@(gs*gs);b0s=float(np.dot(d2*gs*gl,weights))/math.sqrt(vg)
        brs=bd@(gs*gl)/math.sqrt(vg)
        def ball(l2):return float(simpson(pair*np.expm1(l2*xs),x=r))
        l2=brentq(lambda v:ball(v)-target,1e-8,50,xtol=1e-14,rtol=1e-13)
        lam=math.sqrt(l2);b0=lam*b0s;m=float(ndtr(b0-c))/fw
        laws={};allk={}
        for name,corr in [('I',False),('II',True)]:
            kk=np.array([kernels(c,fw,float(rho[i]),l2*float(xs[i]),
                               b0 if corr else 0.,lam*float(brs[i]) if corr else 0.)
                         for i in range(len(r))])
            ints=simpson(pair[:,None]*kk,x=r,axis=0)/fw**2
            laws[name]=dict(partition_rms=math.sqrt(ints[0]),wall_rms=math.sqrt(ints[1]),
                            cross_term=2*ints[2],total=math.sqrt(ints[0]+ints[1]+2*ints[2]))
            allk[name]=kk
        j=int(np.argmin(abs(r-R/2)))
        Cov=np.array([[1,rho[j],b0s,brs[j]], [rho[j],1,brs[j],b0s],
                      [b0s,brs[j],vs,xs[j]],[brs[j],b0s,xs[j],vs]])
        rng=np.random.default_rng(20261008+int(rs)*100+int(t['f']*1000))
        samples=rng.multivariate_normal(np.zeros(4),Cov,size=2000000)
        M=samples[:,:2]>c
        mu=math.exp(l2*vs/2)*m
        delta=np.exp(lam*samples[:,2:])/mu-1
        vals=np.stack(((M[:,0]-fw)*(M[:,1]-fw),
                       M[:,0]*M[:,1]*delta[:,0]*delta[:,1],
                       (M[:,0]-fw)*M[:,1]*delta[:,1]),axis=1)
        av=vals.mean(axis=0);se=vals.std(axis=0,ddof=1)/math.sqrt(len(vals))
        expected=allk['II'][j]
        members[str(rs)]=dict(lambda_latent=lam,latent_variance=l2*vs,
          unmasked_I_ball_variance=target,unmasked_II_ball_variance=target/(m*m),
          muII_over_muI=m,unconditional_mean_declared_II_contrast=1/m-1,
          unconditional_covariance_II_over_I=1/(m*m),
          unconditional_point_variance_I=math.expm1(l2*vs),
          unconditional_point_variance_II=math.expm1(l2*vs)/(m*m),
          b0=b0,laws=laws,total_II_over_I=laws['II']['total']/laws['I']['total'],
          MC=dict(r=r[j],seed=20261008+int(rs)*100+int(t['f']*1000),n=len(vals),
                  expected=expected.tolist(),observed=av.tolist(),sem=se.tolist(),
                  abs_z=np.abs((av-expected)/se).tolist()))
        print('PAIR',t['f'],rs,json.dumps(members[str(rs)]),flush=True)
    return dict(R_Mpc=R,ell_Mpc=ell,pair_norm=float(simpson(pair,x=r)),members=members)

def step(t):
    R=8/(t['hbar']*t['gamma']);rh=R*12.5
    lo=t['DW']+(t['DV']-t['DW'])*t['fi'];hi=t['DV']
    def sigma(R,cut,n=16001):
        out=0.
        for l,h,g in [(1e-7,cut,lo),(cut,1e3,hi)]:
            k=np.geomspace(l,h,n)
            out+=g*g*float(simpson(ind.spectrum(k,t['omega_eff'])*ind.W(k*R)**2,x=np.log(k)))
        return math.sqrt(out)
    cut=math.exp(brentq(lambda x:sigma(rh,math.exp(x))-.0999,math.log(.001),math.log(1),xtol=1e-12))
    sh=sigma(rh,cut);s8=sigma(R,cut);su=ind.sig(ind.spectrum(ind.K,t['omega_eff']),R)
    su_h=ind.sig(ind.spectrum(ind.K,t['omega_eff']),rh);up=.1*su/su_h
    return dict(kcut=cut,premise_rms=sh,R8_rms=s8,constant_upper=up,ratio=s8/up,
                self_convergence_R8=abs(s8/sigma(R,cut,8001)-1))

def reclosure_and_cap(t,anchor,fmed):
    S=ind.spectrum(ind.K,t['omega_eff']);R=8/(t['hbar']*t['gamma'])
    nu=-float(ndtri(t['fi']));phi=math.exp(-nu*nu/2)/math.sqrt(2*math.pi)
    dg=t['DV']-t['DW'];factor=(t['fi']/t['f'])**(1/3)
    seeds={'W09':1500/t['H']*factor/t['gamma'], 'F_median':fmed/(t['H']/100)*factor}
    rec={}
    for name,rs in seeds.items():
        p=t['fi']+phi/(ind.sig(S,rs)/1091)*ind.W(ind.K*rs)
        direct=ind.sig(S,R,t['DW']+dg*p)
        pr=t['fi']+(p-t['fi'])/anchor
        re=ind.sig(S*anchor*anchor,R,t['DW']+dg*pr)
        rec[name]=dict(direct=direct,post=direct*anchor,reclosure=re,
                       ratio_reclosure_over_post=re/(anchor*direct))
    cap=t['fi']/(1-t['fi']);early=ind.sig(S,R)/1091
    out=dict(cap=cap,sigma_LS=early,cap_exceedance=float(ndtr(-cap/early)),
             reclosure=rec,R_Mpc=R,premise_upper=.1*ind.sig(S,R)/ind.sig(S,R*12.5),
             median_scale_ratio=(fmed*t['gamma']/(t['H']/100))/(8/t['hbar']),
             W09_scale_ratio=(1500/t['H'])/(8/t['hbar']))
    return out

def run():
    om=.315
    growth=2.5*om*quad(lambda a:1/(a**3*(om/a**3+1-om)**1.5),0,1,epsabs=1e-12)[0]
    anchor=.8111/(ind.sig(ind.spectrum(ind.K,ind.OMREF),8/.674)*growth)
    old=json.loads((OLD/'independent_results.json').read_text())
    fv=.737;fw=1-fv;states=[-1/3,1.]
    result={'method':'independent derivation and quadrature; not blind; no project imports',
            'anchor':anchor,'cases':{},
            'two_state':dict(mean_derivative=sum(fw/(1+fv*s)**2 for s in states)/2,
                            tangent=fw,mean_reciprocal=sum(fw/(1+s)+fv for s in states)/2)}
    for name,f,H,fmed,sp in [('GM',.737,73.03,2.40456,.3264),('NW15',.627,61,2.80045,.3036)]:
        t=ind.tracker(f,H)
        result['cases'][name]=dict(tracker=t,step=step(t),
                  direct_reclosure_cap=reclosure_and_cap(t,anchor,fmed),
                  nonnegative_pair=new_pairs(t,anchor,sp,old['cases'][name]['covariance']['ell']))
    (HERE/'independent_delta_science.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,allow_nan=False))

if __name__=='__main__':run()
