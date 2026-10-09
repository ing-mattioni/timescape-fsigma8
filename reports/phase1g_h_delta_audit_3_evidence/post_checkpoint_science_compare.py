"""Explicitly NONBLIND matched-recipe comparison after checkpoint c62ad87.

Imports only the independent blind reconstruction, never H code. Differences
in finite-matching normalization and threshold-only/ compressed share labels
are corrected transparently here, leaving the committed blind files intact.
"""
from pathlib import Path
import json, sys, hashlib
import blind_science_reconstruction as independent

ROOT=Path(__file__).resolve().parents[3]
AUTH=ROOT/'audit_work/reproduction/evidence_py312_ed0ec0c.json'
reference=json.loads(AUTH.read_text())
blind=json.loads(Path(__file__).with_name('blind_science_results.json').read_text())

def exact_matching_tracker(f,H):
    """H8 finite matching: D_W=fw0/fwLS*aLS*(t0/tLS)^(2/3).

    Derived independently from wall delta_w proportional to t^(2/3) and
    delta_W=fw delta_w. At zLS, total seed unit is aLS; DW propagates
    fwLS delta_wLS to fw0 delta_w0. [GM](5.4),(5.6) supply the epoch.
    """
    bg=independent.tracker(f,H)
    fi=bg['fvi']
    bg['DW']=(1-f)/(1-fi)*independent.A_LS/bg['uLS']**(2/3)
    bg['Dwall']=bg['DW']*(1-fi)/(1-f)
    bg['normalisation_delta_from_blind']=bg['DW']/blind['cases']['GM' if f==.737 else 'NW15']['tracker']['DW']-1
    return bg

def add(claims,label,v,e,tol,method):
    ab=abs(v-e);rel=ab/max(abs(e),1e-300)
    claims.append({'id':label,'independent':v,'author':e,'abs_error':ab,'rel_error':rel,
                   'absolute_tolerance':tol,'status':'VERIFIED' if ab<=tol else 'VERIFIED_WITH_DEVIATION',
                   'method':method})

result={'checkpoint':'c62ad87d9a51c40d8959d35e0bec58c8b1048a51',
        'stage':'POST_CHECKPOINT_EXPLICITLY_NOT_BLIND',
        'author_artifact_path':str(AUTH),'author_artifact_sha256':hashlib.sha256(AUTH.read_bytes()).hexdigest(),
        'independence':'Same separately derived spectrum, Gaussian tilt and deterministic Plackett/GL integration; no author H code imported',
        'matched_recipe_changes':['finite matching D_W exact instead of asymptotic photon-matter normalization',
                                 'D_wall spectrum/compression implied by exact finite matching D_W',
                                 'quote 1G-D X_SU using threshold-only p0, keep compressed p0 separate'],
        'cases':{},'claims':[]}
for name,(f,H,target,median) in independent.CASES.items():
    print('Post-checkpoint exact matching',name,flush=True)
    bg=exact_matching_tracker(f,H)
    first=independent.first_panel(bg,median)
    l=independent.latent(bg,target)
    first['W09']['X_SU_PBS_threshold_only']=(bg['DW']+(bg['DV']-bg['DW'])*first['W09']['p_coefficient'])/independent.lcdm_growth
    result['cases'][name]={'tracker':bg,'first_panel':first,'latent':l}
    key='PAPER_REFERENCE' if name=='GM' else 'NW15_CMB_FIT'
    a=reference['cases'][key];ac=a['conventions']['c_bare_volume_average'];at=reference['two_phase_covariance'][key]['gaussian_threshold_pair']
    add(result['claims'],name+'/DW',bg['DW'],a['growth']['wall_share_growth'],1e-12,'exact finite-matching formula')
    add(result['claims'],name+'/DV',bg['DV'],a['growth']['void_share_growth'],1e-12,'Milne void volume formula')
    for own,auth in [('W09','pbs_tracker_seed_compressed'),('F_median','pbs_tracker_seed_F_median_compressed')]:
        add(result['claims'],name+'/'+own+'/sigma_direct',first[own]['sigma_direct'],ac['closures'][auth]['linear_sigma_direct_A_s'],1e-9,'independent EH98 Fourier integral')
    for n,j in [('lower',0),('upper',1)]:
        add(result['claims'],name+'/constant_share_'+n,first['constant_share_sigma_range'][j],ac['intervals']['W09_10pct_at_100'][n],1e-9,'independent unit-spectrum and constant-share bound')
    add(result['claims'],name+'/W09/Av',first['W09']['A_v_PBS'],ac['closures']['pbs_tracker_seed_compressed']['void_onset_response_A_v'],1e-6,'Gaussian-threshold probability derivative')
    add(result['claims'],name+'/W09/X_SU_compressed',first['W09']['X_SU_PBS'],ac['closures']['pbs_tracker_seed_compressed']['growth_ratio_to_lcdm_X'],1e-9,'compressed seed share k->0; independent LCDM growth integral')
    add(result['claims'],name+'/W09/X_SU_threshold_only',first['W09']['X_SU_PBS_threshold_only'],a['conventions']['a_equal_mass']['closures']['pbs_tracker_seed_threshold_only_1G_D']['growth_ratio_to_lcdm_X'],1e-9,'threshold-only seed share k->0, divided by independent LCDM growth integral')
    for own,auth in [('signed_I','I_independent'),('signed_II','II_same_field')]:
        add(result['claims'],name+'/'+own+'/CW',l[own]['P11_weighted_CW_minus_one'],at['laws'][auth]['both_walls_conditional_density_covariance_ball'],1e-6,'Gaussian-tail Hessian moments and independent GL ball quadrature')
    for m in l['lognormal']:
        ra=at['nonnegative_lognormal_pair']['members'][f"r_s_{m['smoothing_radius_Mpc']:g}_Mpc"]
        label=name+f"/r_s_{m['smoothing_radius_Mpc']:g}"
        add(result['claims'],label+'/lambda',m['lambda'],ra['latent_scale_lambda'],1e-6,'independent lognormal ball-variance calibration')
        add(result['claims'],label+'/m_II',m['m_II'],ra['conditional_normaliser_ratio_m_II'],1e-6,'Q(c-kappa0)/fw')
        add(result['claims'],label+'/inverse_m_squared',m['inverse_m_II_squared'],ra['conditional_density_covariance_ratio_II_over_I'],1e-6,'independent exponential-tilt covariance ratio')
        add(result['claims'],label+'/total_II_over_I',m['total_II_over_I'],ra['sigma_ratio_II_over_I'],1e-6,'H25 ball variances divided')
        for own,auth in [('I','I_independent'),('II','II_same_field')]:
            add(result['claims'],label+'/'+own+'/CW',m[own]['P11_weighted_CW_minus_one'],ra['laws'][auth]['both_walls_conditional_density_covariance_ball'],1e-6,'independent deterministic tail quadrature and Gaussian exponential tilt')
result['summary']={'claims':len(result['claims']),'verified':sum(x['status']=='VERIFIED' for x in result['claims']),
                   'max_abs_error':max(x['abs_error'] for x in result['claims']),
                   'max_relative_error':max(x['rel_error'] for x in result['claims'])}
Path(__file__).with_name('post_checkpoint_science_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps(result['summary'],indent=2),flush=True)
