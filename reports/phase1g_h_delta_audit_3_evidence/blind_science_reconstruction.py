"""Blind Section 5.C reconstruction: no import of any Phase 1G-H code.

H25 follows from binary mass masking (written derivation); Gaussian moments
follow from the Gaussian generating function and conditional tail integration.
EH98 (26),(28)-(31), [1G-A] spectrum Eq. (5), and tracker [GM](5.4),(5.6)
are implemented directly from approved frozen definitions. This is audit code,
not a changed scientific model. Every quadrature/tolerance is explicit.
"""
from __future__ import annotations
import json, math, sys, platform
from pathlib import Path
import numpy as np
from scipy.integrate import quad, simpson
from scipy.optimize import brentq
from scipy.special import ndtr, ndtri
from numpy.polynomial.legendre import leggauss

AS,NS,KP,TCMB,FB = 2.1e-9, .9649,.05,2.7255,.1563275916312396
A_LS=1/1091
# Frozen E/F adopted H construction inputs; not H output expectations.
CASES={'GM':(.737,73.03,.3264,2.40456),'NW15':(.627,61.,.3036,2.80045)}
NLOG=24001
LNK=np.linspace(math.log(1e-6),math.log(1e4),NLOG)
K=np.exp(LNK)

def phi(x): return np.exp(-np.asarray(x)**2/2)/math.sqrt(2*math.pi)
def Q(x): return ndtr(-np.asarray(x))
def window(x):
    x=np.asarray(x); y=np.ones_like(x)
    small=abs(x)<.015
    z=x[small]**2
    y[small]=1-z/10+z*z/280-z*z*z/15120
    z=x[~small]
    y[~small]=3*(np.sin(z)-z*np.cos(z))/z**3
    return y

def amp(k,om,D=1):
    """[EH98](26),(28)-(31); [1G-A] Eq.(5), D/a_photon ->1."""
    ob=om*FB
    sound=44.5*math.log(9.83/om)/math.sqrt(1+10*ob**.75)
    alpha=1-.328*math.log(431*om)*FB+.38*math.log(22.3*om)*FB*FB
    gamma=om*(alpha+(1-alpha)/(1+(.43*k*sound)**4))
    q=k*(TCMB/2.7)**2/gamma
    L=np.log(2*math.e+1.8*q); C=14.2+731/(1+62.5*q)
    T=L/(L+C*q*q)
    return .16*AS*(k/KP)**(NS-1)*(k*2997.92458)**4*T*T*D*D/om**2

def rms(om,R,transfer=None):
    shape=amp(K,om)*window(K*R)**2
    if transfer is not None: shape=shape*transfer(K)**2
    return float(np.sqrt(simpson(shape,x=LNK)))

def tracker(f,H):
    gamma=1+f/2
    HD=2*H*(2+f)/(4*f*f+f+4)
    def fv(u): return f*u/(1-f+f*u)
    def aw(u):
        return gamma*u**(2/3)*(1-f+f*u)**(1/3)/(1+fv(u)/2)
    u=brentq(lambda u:aw(u)-A_LS,1e-10,.001,xtol=1e-18,rtol=1e-14)
    fi=fv(u); wall=gamma*(1-f)**(1/3)
    DW=(1-f)*wall/(1-fi)
    # H linear two-share definitions (supplied input-only).
    DV=f/fi*A_LS
    om=.5*(1-f)*(2+f)*(HD/100)**2
    return dict(fv0=f,H0=H,HD0=HD,gamma=gamma,uLS=u,fvi=fi,Dwall=wall,DW=DW,DV=DV,om=om)

def tail_pair(c,rho):
    """Deterministic bivariate normal upper tail via Plackett integral.

    dQ2/drho = exp[-c²/(1+rho)]/(2pi sqrt(1-rho²)); substitute
    rho=sin(theta) to remove the endpoint singularity. 128-point GL.
    This is independent of author scipy stochastic bivariate CDF machinery.
    """
    rho=np.clip(np.asarray(rho),-1,1)
    x,w=leggauss(128)
    angle=np.arcsin(rho)
    t=angle[:,None]*(x+1)/2
    integral=angle/2 * np.sum(w*np.exp(-np.asarray(c)[:,None]**2/(1+np.sin(t)))/(2*math.pi),axis=1)
    return Q(c)**2+integral

def ball_nodes(R,n=1600):
    # Composite 10-point Gauss-Legendre avoids high-degree instability;
    # deterministic independent quadrature unlike the H Simpson r-grid.
    q,w=leggauss(10); panels=n//10
    edges=np.linspace(0,2*R,panels+1); m=(edges[:-1]+edges[1:])/2; h=np.diff(edges)/2
    r=(m[:,None]+h[:,None]*q).ravel(); weights=(h[:,None]*w).ravel()
    x=r/R; weights*=3*r*r/R**3*(1-.75*x+x**3/16)
    return r,weights

def covariance(k,lnk,d2,r,sm1,sm2=None):
    if sm2 is None: sm2=sm1
    weighted=d2*sm1*sm2
    vals=np.empty(len(r))
    for i in range(0,len(r),200):
        j=np.sinc(np.outer(r[i:i+200],k)/math.pi)
        vals[i:i+200]=simpson(j*weighted[None,:],x=lnk,axis=1)
    return vals

# Independent LCDM normalization from growth integral; [Short&Coles](3).
OM=.315; HL=.674; OL=1-OM
lcdm_growth=2.5*OM*quad(lambda a:(a/(OM+OL*a**3))**1.5,0,1,epsabs=1e-13,epsrel=1e-13)[0]
ref_sigma=rms(OM*HL*HL,8/HL)*lcdm_growth
anchor=.8111/ref_sigma


def first_panel(bg,median):
    om=bg['om']; gamma=bg['gamma']; f=bg['fv0']; fi=bg['fvi']
    DW,DV=bg['DW'],bg['DV']
    R=8/(bg['HD0']/100)/gamma; Rhom=100/(bg['HD0']/100)/gamma
    unit=rms(om,R); uh=rms(om,Rhom)
    pmin=fi; gmin=DW+(DV-DW)*pmin; gmax=min(.1/uh,DV)
    out={'R_c_Mpc':R,'R_hom_c_Mpc':Rhom,'unit_sigma_direct':unit,
         'constant_share_sigma_range':[gmin*unit,gmax*unit],
         'constant_share_p_range':[pmin,(gmax-DW)/(DV-DW)]}
    for name,proper in [('W09',15/(bg['H0']/100)),('F_median',median*gamma/(bg['H0']/100))]:
        seed=proper/gamma*(fi/f)**(1/3)
        sigseed=rms(om,seed)*A_LS
        nu=-ndtri(fi); amp_p=phi(nu)/sigseed
        def transfer(k):
            p=fi+amp_p*window(k*seed)
            return DW+(DV-DW)*p
        out[name]={'seed_radius_Mpc':seed,'sigma_seed_direct':sigseed,
                   'p_coefficient':float(amp_p),'sigma_direct':rms(om,R,transfer),
                   'A_v_PBS':float(phi(nu)/(sigseed*fi)),
                   'D_SU_PBS':float(DW+(DV-DW)*(fi+amp_p)),
                   'X_SU_PBS':float((DW+(DV-DW)*(fi+amp_p))/lcdm_growth)}
    return out


def latent(bg,target,nr=1600,nk=12001):
    f=bg['fv0']; fw=1-f; c=ndtri(f); R=8/(bg['H0']/100)
    r,bw=ball_nodes(R,nr)
    ln=np.linspace(math.log(1e-5),math.log(80),nk); k=np.exp(ln)
    d2=amp(k*bg['Dwall'],bg['om'],bg['Dwall'])*anchor**2
    xi=covariance(k,ln,d2,r,np.ones_like(k))
    target_carrier=float(np.dot(bw,xi))
    ell_cache={}
    def construct(ell):
        G=np.exp(-.5*(k*ell)**2)
        v=float(simpson(d2*G*G,x=ln))
        rho=covariance(k,ln,d2,r,G)/v
        pp=tail_pair(np.full_like(r,c),rho)
        part=float(np.dot(bw,pp/fw**2-1))
        ell_cache[ell]=(G,v,rho,pp)
        return part
    ell=brentq(lambda ell:construct(ell)-target**2,.02,20,xtol=1e-10,rtol=1e-12)
    construct(ell);G,v,rho,pp=ell_cache[ell]
    kcross=covariance(k,ln,d2,r,G,np.ones_like(k))/math.sqrt(v)
    k0=float(simpson(d2*G,x=ln)/math.sqrt(v))
    mu=k0*float(phi(c))/fw
    s=np.sqrt(1-rho*rho);h=c*np.sqrt((1-rho)/(1+rho))
    boundary=phi(c)*Q(h)
    off=phi(c)*phi(h)/s
    diag=c*boundary-rho*off
    EY=(k0+kcross)*boundary/pp
    EYY=xi+(2*k0*kcross*diag+(k0*k0+kcross*kcross)*off)/pp
    cwi=1+xi
    cwii=(1-mu)**2+2*(1-mu)*EY+EYY
    denom=float(np.dot(bw,pp))
    def summarise(cw):
        return {'P11_weighted_CW_minus_one':float(np.dot(bw,pp*(cw-1))/denom),
                'sigma_total':float(np.sqrt(np.dot(bw,pp*cw/fw**2-1)))}
    out={'R_dressed_Mpc':R,'target_partition_rms_input':target,'ell_Mpc':ell,
         'carrier_ball_variance':target_carrier,'mask_onepoint_c':float(c),
         'signed_kappa0':k0,'signed_mu_wall':mu,'signed_I':summarise(cwi),'signed_II':summarise(cwii),
         'lognormal':[],'ball_probability_integral':float(np.sum(bw)),
         'H25_signed_I_expansion_residual':float(np.dot(bw,pp*cwi/fw**2-1)-(np.dot(bw,pp/fw**2-1)+np.dot(bw,pp*xi/fw**2)))}
    for rs in [1.,2.,4.]:
        S=np.exp(-.5*(k*rs)**2)
        xs=covariance(k,ln,d2,r,S)
        lam2=brentq(lambda lam2:np.dot(bw,np.expm1(lam2*xs))-target_carrier,1e-8,50,xtol=1e-14,rtol=1e-13)
        lam=math.sqrt(lam2)
        cr=lam*covariance(k,ln,d2,r,G,S)/math.sqrt(v)
        c0=lam*float(simpson(d2*G*S,x=ln))/math.sqrt(v)
        m=float(Q(c-c0)/fw)
        tilted=tail_pair(c-c0-cr,rho)
        I=np.exp(lam2*xs)
        II=I*tilted/(pp*m*m)
        a=summarise(I);b=summarise(II)
        out['lognormal'].append({'smoothing_radius_Mpc':rs,'lambda':lam,'lambda_squared':lam2,
            'kappa0':c0,'m_II':m,'inverse_m_II_squared':1/m**2,
            'I':a,'II':b,'total_II_over_I':b['sigma_total']/a['sigma_total'],
            'carrier_ball_variance_calibration_residual':float(np.dot(bw,I-1)-target_carrier)})
    return out


def main():
    data={'blinding':{'model_family':'OpenAI Codex / GPT-6 family; exact served version not exposed','author_family':'Claude',
         'known_expectations':'Only rounded values explicitly printed in task prompt',
         'H_author_outputs_read':False,'H_implementation_imported':False,
         'input_definition_provenance':'Input-only extract by provenance agent; approved D/E/F and frozen lagrangian_sigma formulas'},
         'environment':{'python':sys.version,'platform':platform.platform(),'numpy':np.__version__},
         'integration':{'spectrum_log_grid':NLOG,'latent_log_k_points':12001,'latent_radial_GL_nodes':1600,
                        'latent_k_range':[1e-5,80],'bivariate_Plackett_GL_nodes':128,
                        'quad_epsrel':1e-13,'quad_epsabs':1e-13},
         'reference':{'lcdm_growth_integral':lcdm_growth,'EH98_reference_sigma':ref_sigma,'anchor':anchor},'cases':{}}
    for name,(f,H,target,med) in CASES.items():
        bg=tracker(f,H)
        print('Reconstruct',name,flush=True)
        data['cases'][name]={'tracker':bg,'first_panel':first_panel(bg,med),'latent':latent(bg,target)}
    dest=Path(__file__).with_name('blind_science_results.json')
    dest.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    print(dest,flush=True)
if __name__=='__main__':main()
