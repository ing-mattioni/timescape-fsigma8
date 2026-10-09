import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import simpson
from blind_science_reconstruction import tracker, first_panel, CASES, latent, amp, window, lcdm_growth
base=json.loads(Path(__file__).with_name('blind_science_results.json').read_text())
result={}
for name,(f,H,target,med) in CASES.items():
 bg=tracker(f,H)
 # Compare own independent GL scheme at doubled k, halved r grids.
 coarse=latent(bg,target,nr=800,nk=6001)
 fine=base['cases'][name]['latent']
 ds={}
 for key in ['ell_Mpc','carrier_ball_variance','signed_kappa0','signed_mu_wall']:
  ds[key]=abs(coarse[key]-fine[key])
 for law in ['signed_I','signed_II']:
  ds[law]=abs(coarse[law]['P11_weighted_CW_minus_one']-fine[law]['P11_weighted_CW_minus_one'])
 ds['lognormal_lambda_max_abs']=max(abs(x['lambda']-y['lambda']) for x,y in zip(coarse['lognormal'],fine['lognormal']))
 ds['lognormal_mII_max_abs']=max(abs(x['m_II']-y['m_II']) for x,y in zip(coarse['lognormal'],fine['lognormal']))
 ds['lognormal_CW_max_abs']=max(abs(x[law]['P11_weighted_CW_minus_one']-y[law]['P11_weighted_CW_minus_one']) for x,y in zip(coarse['lognormal'],fine['lognormal']) for law in ['I','II'])
 result[name]=ds
Path(__file__).with_name('blind_science_refinement_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
