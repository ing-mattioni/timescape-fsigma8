"""Old orthant probes, explicit rounding gate values, targeted defensive tests."""
from pathlib import Path
import importlib.util
import json
import math
import sys

ROOT=Path('/workspace/scratch/031c29bb1e06/repo')
OUT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'src'))
import timescape_fsigma8.global_variance as gv
old=json.loads((ROOT/'reports/phase1g_h_independent_audit_evidence/probe_contracts.json').read_text())['orthant']
seen={(r['rho'],r['threshold'],r['nodes']) for r in old}
for row in json.loads((ROOT/'reports/phase1g_h_independent_audit_evidence/probe_extended.json').read_text())['orthant_closed_form_probes']:
    key=(row['rho'],row['threshold'],row['nodes'])
    if key not in seen:
        old.append(row);seen.add(key)
rows=[]
for r in old:
    exact=r.get('exact')
    row={'rho':r['rho'],'threshold':r['threshold'],'start_nodes':r['nodes'],'old_P11':r['P11'],'reference':exact}
    try:
        p=gv.bivariate_normal_orthant_moments(correlation=r['rho'],threshold=r['threshold'],nodes=r['nodes'],tolerance=1e-12)
        row.update(**p,abs_error=abs(p['P11']-exact) if exact is not None else None)
    except Exception as exc:
        row.update(exception=type(exc).__name__,message=str(exc))
    rows.append(row)
data=json.loads((ROOT/'reports/phase1g_e_owner_decisions_successor_inventory.json').read_text())['numbers_from_artifact']
rounding=[]
for label in ('PAPER_REFERENCE','NW15_CMB_FIT'):
    key=f'GE_reference_population_1G_F|{label}|b_dressed_8_over_h|'
    a,b,c=(float(data[key+k]) for k in ('sigma_part','sigma_int_photon_frame_D_wall','sigma_photon_frame_D_wall_empty_voids'))
    total=math.hypot(a,b);half=5e-5
    budget=half*(a/total+b/total+1)
    no_output_half=half*(a/total+b/total)
    rounding.append({'label':label,'input_partition':a,'input_wall':b,'printed_total':c,'calculated_total':total,'abs_discrepancy':abs(total-c),'budget':budget,'removed_output_half_budget':no_output_half,'passes_without_output_half':abs(total-c)<=no_output_half})
(OUT/'supplementary_results.json').write_text(json.dumps({'old_orthant_probes':rows,'reference_rounding_gate':rounding},indent=2)+'\n')
print(json.dumps({'old_orthant_count':len(rows),'refused':sum('exception' in r for r in rows),'max_error':max(r.get('abs_error') or 0 for r in rows),'rounding':rounding},indent=2))
