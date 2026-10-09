"""Fourth H delta audit: independently centred pair statistics.

No package imports. The spectrum implements EH98 (26),(28)-(31), 1G-A (5);
the tracker implements GM (5.4),(5.6), and H8/H9 inputs. For a Gaussian mask,
tails are obtained by the Plackett correlation integral (GL128), not the
author's orthant code. Signed pair moments follow derivatives of the Gaussian
moment generating function; lognormal moments follow exponential tilting.
The new centred statistics are calculated before opening author value tables.
"""
from pathlib import Path
import hashlib, json, math, platform, sys
from datetime import datetime, timezone
import numpy as np
import scipy
from scipy.integrate import quad, simpson
from scipy.optimize import brentq
from scipy.special import ndtr, ndtri
from numpy.polynomial.legendre import leggauss

BASE=Path(__file__).resolve().parent
REPO=Path('/workspace/scratch/1605b2925963/repo')
AS,NS,KP,TCMB=2.1e-9,.9649,.05,2.7255
OM_LCDM,H_LCDM=.315,.674
FB=.02237/(OM_LCDM*H_LCDM**2)
A_LS=1/1091
CASES={'PAPER_REFERENCE':(.737,73.03,.3264,2.40456),'NW15_CMB_FIT':(.627,61.,.3036,2.80045)}

def phi(a): return np.exp(-np.asarray(a)**2/2)/math.sqrt(2*math.pi)
def Q(a): return ndtr(-np.asarray(a))
def window(x):
    x=np.asarray(x); y=np.ones_like(x); small=abs(x)<.015
    z=x[small]**2; y[small]=1-z/10+z*z/280-z*z*z/15120
    z=x[~small]; y[~small]=3*(np.sin(z)-z*np.cos(z))/z**3
    return y

def power(k,om,growth=1):
    ob=om*FB
    sound=44.5*math.log(9.83/om)/math.sqrt(1+10*ob**.75)
    alpha=1-.328*math.log(431*om)*FB+.38*math.log(22.3*om)*FB**2
    shape=om*(alpha+(1-alpha)/(1+(.43*k*sound)**4))
    q=k*(TCMB/2.7)**2/shape
    L=np.log(2*math.e+1.8*q); C=14.2+731/(1+62.5*q)
    T=L/(L+C*q*q)
    return .16*AS*(k/KP)**(NS-1)*(k*2997.92458)**4*T*T*growth**2/om**2

LN=np.linspace(math.log(1e-6),math.log(1e4),24001); K=np.exp(LN)
def rms(om,R,propagator=None):
    y=power(K,om)*window(K*R)**2
    if propagator is not None: y*=propagator(K)**2
    return math.sqrt(float(simpson(y,x=LN)))

def tracker(f,H):
    gamma=1+f/2; HD=2*H*(2+f)/(4*f*f+f+4)
    def fv(u): return f*u/(1-f+f*u)
    def photon_a(u): return gamma*u**(2/3)*(1-f+f*u)**(1/3)/(1+fv(u)/2)
    u=brentq(lambda u:photon_a(u)-A_LS,1e-10,.001,xtol=1e-18,rtol=1e-14)
    fi=fv(u); Dwall=gamma*(1-f)**(1/3)
    return dict(f=f,H=H,gamma=gamma,HD=HD,uLS=u,fi=fi,Dwall=Dwall,
                DW=(1-f)*Dwall/(1-fi),DV=f/fi*A_LS,
                om=.5*(1-f)*(2+f)*(HD/100)**2)

GL,GLW=leggauss(128)
def upper_pair(a,b,rho):
    a,b,rho=np.broadcast_arrays(np.asarray(a),np.asarray(b),np.asarray(rho))
    angle=np.arcsin(np.clip(rho,-1,1)); theta=angle[:,None]*(GL+1)/2
    st=np.sin(theta);ct2=np.cos(theta)**2
    exponent=-(a[:,None]**2-2*a[:,None]*b[:,None]*st+b[:,None]**2)/(2*ct2)
    return Q(a)*Q(b)+angle/2*np.sum(GLW*np.exp(exponent)/(2*math.pi),axis=1)

def ball(R,n=1600):
    q,w=leggauss(10);edges=np.linspace(0,2*R,n//10+1)
    mid=(edges[:-1]+edges[1:])/2;half=np.diff(edges)/2
    r=(mid[:,None]+half[:,None]*q).ravel();weights=(half[:,None]*w).ravel()
    x=r/R;weights*=3*r*r/R**3*(1-.75*x+x**3/16)
    return r,weights

def xi(k,ln,d2,r,s1,s2=None):
    if s2 is None:s2=s1
    y=d2*s1*s2;out=np.empty(len(r))
    for p in range(0,len(r),100):
        out[p:p+100]=simpson(np.sinc(np.outer(r[p:p+100],k)/math.pi)*y[None,:],x=ln,axis=1)
    return out

G_LCDM=2.5*OM_LCDM*quad(lambda a:(a/(OM_LCDM+(1-OM_LCDM)*a**3))**1.5,0,1,
                            epsabs=1e-13,epsrel=1e-13)[0]
REF=rms(OM_LCDM*H_LCDM**2,8/H_LCDM)*G_LCDM
ANCHOR=.8111/REF

def paired_statistics(P,E1,E2,CW,weights):
    denom=float(np.dot(weights,P));norm=weights*P/denom
    e1=float(np.dot(norm,E1));e2=float(np.dot(norm,E2));prod=float(np.dot(norm,CW))
    return {'P11_integral':denom,'product_moment_excess_ball':prod-1,
            'pair_weighted_pointwise_centred_covariance':float(np.dot(norm,CW-E1*E2)),
            'ball_conditioned_centred_covariance':prod-e1*e2,
            'ball_conditioned_mean_psi1':e1,'ball_conditioned_mean_psi2':e2,
            'product_minus_pointwise_centred':float(np.dot(norm,E1*E2))-1,
            'product_minus_ball_centred':e1*e2-1,
            'mean_psi_at_separations_Mpc':[(float(r),float(E1[i])) for r,i in []]}

def reconstruct_pair(bg,target,nr=1600,nk=12001):
    f=bg['f'];fw=1-f;c=float(ndtri(f));R=8/(bg['H']/100)
    r,w=ball(R,nr);ln=np.linspace(math.log(1e-5),math.log(80),nk);k=np.exp(ln)
    d2=power(k*bg['Dwall'],bg['om'],bg['Dwall'])*ANCHOR**2
    xw=xi(k,ln,d2,r,np.ones_like(k));carrier=float(np.dot(w,xw))
    def tables(ell):
        S=np.exp(-.5*(k*ell)**2);v=float(simpson(d2*S*S,x=ln))
        rho=xi(k,ln,d2,r,S)/v;P=upper_pair(c,c,rho)
        return S,v,rho,P
    ell=brentq(lambda ell:np.dot(w,tables(ell)[3]/fw**2-1)-target**2,.02,20,
               xtol=1e-10,rtol=1e-12)
    Sg,v,rho,P=tables(ell)
    kr=xi(k,ln,d2,r,Sg,np.ones_like(k))/math.sqrt(v)
    k0=float(simpson(d2*Sg,x=ln))/math.sqrt(v)
    mu=k0*float(phi(c))/fw
    h=c*np.sqrt((1-rho)/(1+rho));boundary=phi(c)*Q(h)
    off=phi(c)*phi(h)/np.sqrt(1-rho*rho);diag=c*boundary-rho*off
    Ew=(k0+kr)*boundary/P
    Eww=xw+(2*k0*kr*diag+(k0*k0+kr*kr)*off)/P
    signed={}
    signed['I_independent']=paired_statistics(P,np.ones_like(r),np.ones_like(r),1+xw,w)
    signed['II_same_field']=paired_statistics(P,1-mu+Ew,1-mu+Ew,(1-mu)**2+2*(1-mu)*Ew+Eww,w)
    lognormal={}
    rs=1.;Ss=np.exp(-.5*(k*rs)**2);xs=xi(k,ln,d2,r,Ss)
    lam2=brentq(lambda x:np.dot(w,np.expm1(x*xs))-carrier,1e-8,50.,xtol=1e-14,rtol=1e-13)
    lam=math.sqrt(lam2);cr=lam*xi(k,ln,d2,r,Sg,Ss)/math.sqrt(v)
    c0=lam*float(simpson(d2*Sg*Ss,x=ln))/math.sqrt(v)
    m=float(Q(c-c0)/fw);CI=np.exp(lam2*xs)
    lognormal['I_independent']=paired_statistics(P,np.ones_like(r),np.ones_like(r),CI,w)
    Epsi=upper_pair(c-cr,c-c0,rho)/(P*m)
    CW=CI*upper_pair(c-c0-cr,c-c0-cr,rho)/(P*m*m)
    lognormal['II_same_field']=paired_statistics(P,Epsi,Epsi,CW,w)
    # Direct scalar quadrature independently cross-checks asymmetric tilted
    # tails, and probes at moderate/high mask correlation.
    asym=[]
    for idx in [nr//20,nr//4,nr//2]:
        a=float(c-cr[idx]);b=c-c0;rr=float(rho[idx]);s=math.sqrt(1-rr*rr)
        pquad=quad(lambda z:float(phi(z)*Q((b-rr*z)/s)),a,np.inf,epsabs=2e-12,epsrel=2e-12)[0]
        pgl=float(upper_pair([a],[b],[rr])[0])
        asym.append({'r_Mpc':float(r[idx]),'rho':rr,'P_quad':pquad,'P_GL':pgl,'abs_diff':abs(pquad-pgl)})
    return {'R_Mpc':R,'target_partition_rms':target,'ell_Mpc':ell,'signed_mu':mu,
            'signed_kappa0':k0,'carrier_ball_variance':carrier,'r_s_Mpc':rs,
            'lambda':lam,'lognormal_kappa0':c0,'conditional_normaliser_m_II':m,
            'ball_weight_norm':float(np.sum(w)),'signed':signed,'lognormal':lognormal,
            'asymmetric_tail_direct_quad_checks':asym}

def primary(bg,median):
    DW,DV,om,fi,f,gamma=tuple(bg[k] for k in ['DW','DV','om','fi','f','gamma'])
    R=8/(bg['HD']/100)/gamma;Rh=100/(bg['HD']/100)/gamma
    unit=rms(om,R);uh=rms(om,Rh);glo=DW+(DV-DW)*fi;ghi=min(.1/uh,DV)
    out={'R_c_Mpc':R,'R_hom_c_Mpc':Rh,'sigma_unit':unit,'sigma_unit_Rhom':uh,
         'p_interval':[fi,(ghi-DW)/(DV-DW)],'sigma_direct_interval':[glo*unit,ghi*unit]}
    for name,proper in [('W09',15/(bg['H']/100)),('F_median',median*gamma/(bg['H']/100))]:
        seed=proper/gamma*(fi/f)**(1/3);sigseed=rms(om,seed)*A_LS
        nu=-float(ndtri(fi));coeff=float(phi(nu))/sigseed
        def prop(k):return DW+(DV-DW)*(fi+coeff*window(k*seed))
        direct=rms(om,R,prop)
        out[name]={'seed_Mpc':seed,'sigma_seed':sigseed,'sigma_direct':direct,
                   'sigma_planck_anchored_posthoc':direct*ANCHOR,'PBS_share_k0':fi+coeff}
    return out

def main():
    dest=BASE/'independent_science_blind.json'
    data={'date_utc':datetime.now(timezone.utc).isoformat(),
          'author_new_covariance_values_read_before_calculation':False,
          'independence':'Own new verifier, no package imports. Author script formulas and input definitions read; prior independent third-audit verifier read, not its numeric output. Existing rounded task claims known. New centred values computed before author tables.',
          'environment':{'python':sys.version,'platform':platform.platform(),'numpy':np.__version__,'scipy':scipy.__version__},
          'method':{'spectrum_k_points':24001,'latent_k_points':12001,'radial_composite_GL_points':1600,'Plackett_GL_points':128,'quad_epsabs':2e-12,'quad_epsrel':2e-12,'no_production_import':True},
          'self_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'input_sources_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [REPO/'AGENTS.md',REPO/'scripts/phase1g_h_global_variance_closure_numerics.py',REPO/'reports/phase1g_h_delta_audit_3_evidence/blind_science_reconstruction.py']},
          'anchor':{'growth_LCDM_integral':G_LCDM,'sigma_LCDM_direct':REF,'anchor_factor':ANCHOR},'cases':{}}
    for label,(f,H,target,med) in CASES.items():
        bg=tracker(f,H)
        print('Computing independent case',label,flush=True)
        pair=reconstruct_pair(bg,target)
        coarse=reconstruct_pair(bg,target,nr=800,nk=6001)
        differences={}
        for family in ['signed','lognormal']:
            for law in ['I_independent','II_same_field']:
                differences[family+'.'+law]={k:abs(pair[family][law][k]-coarse[family][law][k]) for k in ['product_moment_excess_ball','pair_weighted_pointwise_centred_covariance','ball_conditioned_centred_covariance']}
        data['cases'][label]={'tracker':bg,'primary':primary(bg,med),'pair':pair,'refinement_abs_differences':differences}
    dest.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    meta={'time_utc':datetime.now(timezone.utc).isoformat(),'result_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'script_sha256':data['self_sha256'],'author_new_covariance_values_read_before_calculation':False}
    (BASE/'INDEPENDENT_CHECKPOINT.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps(meta),flush=True)
if __name__=='__main__':main()
