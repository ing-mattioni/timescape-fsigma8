"""Explicit post-checkpoint recipe correction, no production imports.

The initial result used the asymptotic normalization of the older verifier.
H8 specifies finite matching, which is fw0/fwLS*aLS*(t0/tLS)^(2/3).
The immutable original checkpoint is retained; the correction is disclosed.
No author centred-covariance values exist or have been read.
"""
import json, hashlib
from datetime import datetime,timezone
from pathlib import Path
import independent_science as audit

out={'date_utc':datetime.now(timezone.utc).isoformat(),
     'stage':'POST_CHECKPOINT_MATCHED_FINITE_LS_RECIPE_EXPLICITLY_NONBLIND_FOR_EXISTING_PRODUCT_VALUES',
     'author_centred_covariance_values_read':False,
     'production_module_imported':False,
     'recipe_correction':'DW=fw0/fwLS*aLS/uLS^(2/3); Dwall=DW*fwLS/fw0. Other independently derived formulas unchanged.',
     'blind_checkpoint':json.loads((audit.BASE/'INDEPENDENT_CHECKPOINT.json').read_text()),
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'cases':{}}
for label,(f,H,target,med) in audit.CASES.items():
    print('Matched finite LS',label,flush=True)
    bg=audit.tracker(f,H)
    bg['DW']=(1-f)/(1-bg['fi'])*audit.A_LS/bg['uLS']**(2/3)
    bg['Dwall']=bg['DW']*(1-bg['fi'])/(1-f)
    pair=audit.reconstruct_pair(bg,target)
    coarse=audit.reconstruct_pair(bg,target,nr=800,nk=6001)
    differences={}
    for family in ['signed','lognormal']:
        for law in ['I_independent','II_same_field']:
            differences[family+'.'+law]={k:abs(pair[family][law][k]-coarse[family][law][k]) for k in ['product_moment_excess_ball','pair_weighted_pointwise_centred_covariance','ball_conditioned_centred_covariance']}
    out['cases'][label]={'tracker':bg,'primary':audit.primary(bg,med),'pair':pair,'refinement_abs_differences':differences}
dest=audit.BASE/'independent_science_matched.json'
dest.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(dest,flush=True)
