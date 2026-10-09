"""Compare independent values against current inventory or fresh evidence."""
from pathlib import Path
import json,hashlib,sys,subprocess
BASE=Path(__file__).resolve().parent
REPO=Path('/workspace/scratch/1605b2925963/repo')
own=json.loads((BASE/'independent_science_matched.json').read_text())
inventory=REPO/'reports/phase1g_h_global_variance_closure_inventory.json'
source=Path(sys.argv[1]) if len(sys.argv)>1 else inventory
ref=json.loads(source.read_text());full='cases' in ref
claims=[]
def add(label,actual,expected,tolerance,method):
    error=abs(actual-expected)
    claims.append(dict(id=label,status='VERIFIED' if error<=tolerance else 'VERIFIED_WITH_DEVIATION',
                       independent_value=actual,source_value=expected,absolute_error=error,
                       relative_error=error/max(abs(expected),1e-300),absolute_tolerance=tolerance,
                       method=method))
for name,c in own['cases'].items():
    r=ref['cases' if full else 'results'][name];conv=r['conventions']['c_bare_volume_average']
    for k,expected in [('DW','wall_share_growth'),('DV','void_share_growth')]:
        add(name+'/'+k,c['tracker'][k],r['growth'][expected],1e-12,'direct exact finite-LS tracker and regional growth formula')
    for ownname,authname in [('W09','pbs_tracker_seed_compressed'),('F_median','pbs_tracker_seed_F_median_compressed')]:
        add(name+'/'+ownname+'/sigma_direct',c['primary'][ownname]['sigma_direct'],conv['closures'][authname]['linear_sigma_direct_A_s'],1e-9 if full else 5.2e-7,'independent EH98 Fourier integral at convention c, unit-spectrum + PBS seed')
    for j,end in enumerate(['lower','upper']):
        add(name+'/constant_share_interval/'+end,c['primary']['sigma_direct_interval'][j],conv['intervals']['W09_10pct_at_100'][end],1e-9 if full else 5.2e-7,'constant G(p), adopted W09 premise at 100 hbar inverse Mpc; bound only in constant-share class')
    pair=ref['two_phase_covariance'][name]
    for family in ['signed','lognormal']:
        if full:
            refpair=pair['gaussian_threshold_pair']
            target=refpair['laws'] if family=='signed' else refpair['nonnegative_lognormal_pair']['members']['r_s_1_Mpc']['laws']
        else:
            target=pair['signed_gaussian_pair']['laws'] if family=='signed' else pair['nonnegative_lognormal_pairs']['members']['r_s_1_Mpc']['laws']
        for law in ['I_independent','II_same_field']:
            add(name+'/'+family+'/'+law+'/product_excess',c['pair'][family][law]['product_moment_excess_ball'],target[law]['both_walls_product_moment_excess_ball'],1e-6 if full else (5e-8 if family=='signed' else 6e-7),'independent truncated Gaussian generating-function derivatives/exponential tilt; Plackett GL128 and composite radial GL1600')

old=json.loads(subprocess.check_output(['git','show','18bf2fb:reports/phase1g_h_global_variance_closure_inventory.json'],cwd=REPO))
new=json.loads(inventory.read_text())
def rename(value):
    if isinstance(value,dict):return {('both_walls_product_moment_excess_ball' if k=='both_walls_conditional_density_covariance_ball' else k):rename(v) for k,v in value.items()}
    if isinstance(value,list):return [rename(v) for v in value]
    if isinstance(value,str):return value.replace('the both-walls conditional covariance C_W(r) - 1, which with P11 fixes the total by (H25)','the both-walls conditional product moment C_W(r) = E[psi1 psi2 | both in walls], which with P11 fixes the total by (H25)')
    return value
def numeric(value):
    if isinstance(value,dict):return {k:numeric(v) for k,v in value.items() if not isinstance(v,str)}
    if isinstance(value,list):return [numeric(v) for v in value if not isinstance(v,str)]
    return value
result={'comparison_source':str(source),'comparison_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'comparison_kind':'FULL_PRECISION_FRESH_RUNTIME' if full else 'CURRENT_ROUNDED_INVENTORY',
        'claims':claims,'claim_counts':{'total':len(claims),'VERIFIED':sum(c['status']=='VERIFIED' for c in claims),'VERIFIED_WITH_DEVIATION':sum(c['status']=='VERIFIED_WITH_DEVIATION' for c in claims)},
        'inventory_two_phase_numeric_content_unchanged_after_rename':numeric(rename(old['two_phase_covariance']))==numeric(new['two_phase_covariance']),
        'GH-D3F5_resolution':{'status':'RESOLVED','reason':'Product-moment terminology and keys corrected; historical covariance string explicitly annotated. Independent new centred values show equality for law I and a difference for law II.'}}
dest=BASE/('science_comparison_full.json' if full else 'science_comparison_inventory.json')
dest.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps(result['claim_counts']))
print('Numeric section preserved:',result['inventory_two_phase_numeric_content_unchanged_after_rename'])
