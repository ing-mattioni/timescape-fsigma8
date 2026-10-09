"""Independent delta-audit public contract probes and deterministic orthant checks.

Reads the exact audited source; writes evidence outside that tree.
"""
import dataclasses as dc
import importlib.util
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr

ROOT = Path('/workspace/scratch/031c29bb1e06/repo')
OUT = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'src'))
spec = importlib.util.spec_from_file_location('audit_test_helpers', ROOT / 'tests/test_phase1g_h_global_variance.py')
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
gv, ls = t.gv, t.ls

def probe(name, make, compare=None):
    try:
        x = make()
        row = {'id':name, 'accepted':True, 'strict_json':True}
        try:
            json.dumps(x.to_json_dict(), allow_nan=False)
        except (TypeError, ValueError):
            row['strict_json'] = False
        if compare:
            row.update(compare(x))
    except Exception as exc:
        row = {'id':name, 'accepted':False, 'exception':type(exc).__name__, 'message':str(exc)}
    return row

res = t.run(t.GM, t.constant(.05), t.radius('c'))
pbs = t.run(t.GM, t.tracker_seed(t.GM, res.growth,15.,gv.SeedVolumeCompression.COMPRESSED_WITH_REGION),t.radius('c'))
prem = gv.HomogeneityPremise(radius=t.radius('c',100),max_linear_rms=.1,provenance='delta independent probe')
iv=gv.admissible_global_linear_interval(target=res,premise=prem)
old=[]
old.append(probe('old_constant_stored_p0',lambda:dc.replace(res.void_share,share_k0=.95)))
old.append(probe('old_growth_time_2',lambda:dc.replace(res.growth,t_ls_over_t0=2.)))
old.append(probe('old_pbs_nan',lambda:dc.replace(pbs.void_share,threshold_share_k0=float('nan'))))
old.append(probe('old_growth_diagnostics_nan',lambda:dc.replace(res.growth,diagnostics=tuple((k,float('nan')) for k,_ in res.growth.diagnostics))))
for field in ('upper','lower','share_upper','unit_growth_sigma_at_premise','target_premise_rms'):
    for value in (-1.,float('nan'),float('inf')):
        old.append(probe(f'old_interval_{field}_{value}',lambda field=field,value=value:dc.replace(iv,**{field:value})))

new=[]
new.append(probe('changed_spectrum_amplitude_only',lambda:dc.replace(res,early_spectrum=t.spectrum(4*2.1e-9)),lambda x:{'stored_sigma':x.linear_sigma,'independent_factory_sigma':t.run(t.GM,t.constant(.05),t.radius('c'),A_s=4*2.1e-9).linear_sigma}))
radius2=ls.resolve_lagrangian_radius(spec=t.radius('c',16),density=res.density)
new.append(probe('changed_radius_only',lambda:dc.replace(res,radius=radius2),lambda x:{'stored_sigma':x.linear_sigma,'new_radius_Mpc':x.radius.radius_Mpc,'independent_factory_sigma':t.run(t.GM,t.constant(.05),t.radius('c',16)).linear_sigma}))
q=dc.replace(t.QUAD,grid_points=33,comparison_grid_points=17)
new.append(probe('changed_quadrature_nodes_only',lambda:dc.replace(res,quadrature=q),lambda x:{'stored_sigma':x.linear_sigma,'new_grid_points':x.quadrature.grid_points,'reported_relative_change':x.quadrature_relative_change}))
seed2=dc.replace(pbs.void_share.closure,seed_radius_Mpc=2*pbs.void_share.closure.seed_radius_Mpc)
new.append(probe('changed_pbs_seed_radius_only',lambda:dc.replace(pbs.void_share,closure=seed2),lambda x:{'stored_sigma_seed':x.sigma_seed,'new_seed_radius_Mpc':x.closure.seed_radius_Mpc,'independent_evaluation_sigma_seed':gv.evaluate_void_share(closure=seed2,growth=x.growth,density=pbs.density,early_spectrum=pbs.early_spectrum,seed_quadrature=t.SEED_QUAD).sigma_seed}))
new.append(probe('changed_interval_premise_rms_only',lambda:dc.replace(iv,target_premise_rms=999.),lambda x:{'stored_target_premise_rms':x.target_premise_rms,'original_target_premise_rms':iv.target_premise_rms}))

def independent(rho,c1,c2):
    # Conditional normal integration, adaptive QUADPACK rather than the
    # tested fixed-node Legendre/refinement implementation. ±14 normal
    # truncation gives <8e-44 probability tails. Small panels resolve the
    # conditional transition even when |rho| is almost one.
    lo=max(c1,-14.); hi=max(14.,c1+14.)
    s=math.sqrt((1-rho)*(1+rho))
    breaks={lo,hi}
    if rho:
        u=c2/rho; width=s/abs(rho)
        for scale in (-12.,-3.,0.,3.,12.):
            b=u+scale*width
            if lo<b<hi: breaks.add(b)
    edges=sorted(breaks)
    def fn(u):return math.exp(-u*u/2)/math.sqrt(2*math.pi)*float(ndtr((rho*u-c2)/s))
    vals=[quad(fn,a,b,epsabs=2e-14,epsrel=2e-13,limit=300) for a,b in zip(edges[:-1],edges[1:])]
    return sum(v for v,_ in vals),sum(e for _,e in vals)

grid=[]
rhos=(-.999999999999,-.999999,-.95,-.5,0.,.5,.95,.999999,.999999999999)
pairs=((-100.,-100.),(-12.,-11.),(0.,0.),(.634,-1.2),(2.,.5),(-3.,4.),(10.,8.),(-8.,9.),(-2.,1.),(.3,.300001),(.3,-.300001))
for rho in rhos:
    for c1,c2 in pairs:
        reference,error=independent(rho,c1,c2)
        row={'rho':rho,'c1':c1,'c2':c2,'reference':reference,'quad_error_estimate':error,'tolerance':1e-12}
        try:
            actual=gv.bivariate_normal_orthant_probability(correlation=rho,threshold_1=c1,threshold_2=c2,nodes=16,tolerance=1e-12)
            row.update(actual=actual,abs_error=abs(actual-reference),within_tolerance=abs(actual-reference)<=1e-12)
        except Exception as exc:
            row.update(exception=type(exc).__name__,message=str(exc))
        grid.append(row)

payload={'old_probes':old,'replacement_probes':new,'orthant_grid':grid,'summary':{'old_rejected':sum(not r['accepted'] for r in old),'old_total':len(old),'new_accepted':sum(r['accepted'] for r in new),'new_total':len(new),'orthant_total':len(grid),'orthant_returned':sum('actual' in r for r in grid),'orthant_bad':sum(r.get('within_tolerance') is False for r in grid),'orthant_max_absolute_error':max((r['abs_error'] for r in grid if 'abs_error' in r),default=0.)}}
(OUT/'probes_results.json').write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n')
print(json.dumps(payload['summary'],indent=2))
print(json.dumps(new,indent=2))
