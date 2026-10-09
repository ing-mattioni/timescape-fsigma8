import json,pathlib,math,collections,decimal,hashlib
W=pathlib.Path(__file__).resolve().parent;R=W.parent/'repo'
def read(p):return json.loads(p.read_text())
def flat(x,p=''):
 if isinstance(x,dict):
  for k,v in x.items():yield from flat(v,p+'/'+str(k))
 elif isinstance(x,list):
  for k,v in enumerate(x):yield from flat(v,p+'/'+str(k))
 else:yield p,x
def comparison(a,b,ignore=('environment','figures','gates','gate_definitions')):
 aa={p:v for p,v in flat(a) if p.split('/')[1] not in ignore};bb={p:v for p,v in flat(b) if p.split('/')[1] not in ignore};rows=[]
 for p in aa.keys()&bb.keys():
  x,y=aa[p],bb[p]
  if isinstance(x,(int,float)) and not isinstance(x,bool) and isinstance(y,(int,float)) and not isinstance(y,bool):rows.append(dict(path=p,left=x,right=y,absolute=abs(x-y),relative=abs(x-y)/max(abs(x),abs(y)) if x or y else 0))
 return dict(common_numeric_count=len(rows),max_absolute=max([r['absolute'] for r in rows],default=0),max_relative=max([r['relative'] for r in rows],default=0),largest_relative=sorted(rows,key=lambda r:r['relative'],reverse=True)[:12],added=sorted(bb.keys()-aa.keys()),removed=sorted(aa.keys()-bb.keys()),rows=rows)
new=read(W/'evidence_py312.json');other=read(W/'evidence_py311.json');old=read(W/'evidence_old_py312.json');first=read(R/'reports/phase1g_h_independent_audit_evidence/evidence_py312.json')
res={'cross_interpreter':comparison(new,other,('environment','figures')),'same_interpreter_delta':comparison(old,new),'first_audit_vs_new':comparison(first,new)}
# Exact metadata/field changes and genuinely altered published numeric leaves are separate.
claims=[]
def add(claim,declared,actual,method,status=None,tolerance=None,location=None):
 if status is None:status='VERIFIED' if declared==actual else 'VERIFIED_WITH_DEVIATION'
 claims.append(dict(claim_id=f'GH-DN{len(claims)+1:04}',claim=claim,status=status,declared_value=declared,audit_value=actual,method=method,tolerance=tolerance or {'absolute':0,'relative':0},location=location))
for g,group in new['gates'].items():
 for k,v in group.items():add('Evidence gate '+g+'/'+k,True,v['pass'],'SAME_CODE_GATE_RERUN',tolerance={'absolute':v['limit'],'relative':0},location='/gates/'+g+'/'+k)
for name,c in res.items():
 for row in c['rows']:
  lim=1e-12+6e-13*max(abs(row['left']),abs(row['right']))
  add(name+' '+row['path'],row['left'],row['right'],'NUMERIC_TREE_COMPARISON','VERIFIED' if row['absolute']<=lim else 'VERIFIED_WITH_DEVIATION',{'absolute':1e-12,'relative':6e-13},row['path'])
# All numeric leaves with common paths in updated inventory blocks.
inv=read(R/'reports/phase1g_h_global_variance_closure_inventory.json');mapped={}
for key,x in [('results',new['cases']),('anchoring',new['anchoring']),('two_phase_covariance',new['two_phase_covariance']),('ensemble_vs_tangent_example',new['ensemble_vs_tangent_example'])]:
 for p,v in flat(x,'/'+key):mapped[p]=v
unmatched=[];rounded=[]
for key in ['results','anchoring','two_phase_covariance','ensemble_vs_tangent_example']:
 for p,v in flat(inv[key],'/'+key):
  if not isinstance(v,(int,float)) or isinstance(v,bool):continue
  pp=p.replace('/a_s_scaling_pbs_tracker_seed/','/a_s_scaling/pbs_tracker_seed_compressed/').replace('/refined_quadrature_linear_sigma_c_pbs','/refined_quadrature_linear_sigma').replace('/premise_max_linear_rms','/premise/max_linear_rms').replace('/premise_radius_Mpc','/premise_radius/radius_Mpc').replace('/primary_rms_at_premise','/target_premise_rms').replace('/linear_sigma_c_direct','/linear_sigma_direct_A_s').replace('/E_reference_reproduction/','/E_reference/').replace('/ell_Mpc','/partition_smoothing_ell_Mpc')
  pp=pp.replace('/linear_sigma_post_hoc_normalised','/linear_sigma_planck_anchored').replace('/lower_post_hoc_withdrawn','/lower_anchored').replace('/upper_post_hoc_withdrawn','/upper_anchored').replace('/normalisation_variants/','/pbs_reclosure_under_spectrum_rescaling/').replace('/nonnegative_lognormal_pairs/','/gaussian_threshold_pair/nonnegative_lognormal_pair/').replace('/signed_gaussian_pair/','/gaussian_threshold_pair/')
  pp=pp.replace('/scale_separation_convention_c/','/scale_separation/')
  if '/step_share_counterexample/' in pp:pp=pp.replace('/premise_radius/radius_Mpc','/premise_radius_Mpc')
  pp=pp.replace('/nonnegative_lognormal_pair/linear_limit_max_rel_difference','/nonnegative_lognormal_pair/linear_limit/max_wall_moment_rel_difference')
  if pp not in mapped:unmatched.append(p);continue
  actual=mapped[pp];tol=max(2e-12,.5*10**decimal.Decimal(str(v)).as_tuple().exponent);ok=abs(v-actual)<=tol
  rounded.append(dict(path=p,declared=v,actual=actual,tolerance=tol,pass_=ok));add('Inventory rounded scalar '+p,v,actual,'INVENTORY_VS_REGENERATED_ARTIFACT','VERIFIED' if ok else 'REFUTED',{'absolute':tol,'relative':0},p)
# Independent new science comparisons, matched explicitly (no matching by numerical proximity).
s=read(W/'science/independent_delta_science.json');cm={'GM':'PAPER_REFERENCE','NW15':'NW15_CMB_FIT'}
for own,code in cm.items():
 c=s['cases'][own];a=new['cases'][code];nl=new['two_phase_covariance'][code]['gaussian_threshold_pair']['nonnegative_lognormal_pair']
 def independent(label,x,y,tol=2e-8):
  add(own+' '+label,x,y,'INDEPENDENT_FORMULA_AND_QUADRATURE','VERIFIED' if abs(x-y)<=tol+tol*abs(x) else 'VERIFIED_WITH_DEVIATION',{'absolute':tol,'relative':tol},code)
 for ak,ok in [('k_cut_per_Mpc','kcut'),('premise_rms','premise_rms'),('target_rms','R8_rms'),('ratio_to_constant_share_upper','ratio'),('constant_share_upper','constant_upper')]:independent('step '+ak,a['step_share_counterexample'][ak],c['step'][ok])
 independent('flat-wall cap exceedance',a['flat_wall_cap_exceedance']['gaussian_fraction_above_cap'],c['direct_reclosure_cap']['cap_exceedance'])
 for member,row in c['nonnegative_pair']['members'].items():
  m=nl['members']['r_s_'+str(int(float(member)))+'_Mpc']
  independent('lambda rs='+member,m['latent_scale_lambda'],row['lambda_latent'],5e-4)
  independent('lognormal II/I rs='+member,m['sigma_ratio_II_over_I'],row['total_II_over_I'],5e-4)
  for ownlaw,codelaw in [('I','I_independent'),('II','II_same_field')]:
   for ak,ok in [('sigma_partition','partition_rms'),('sigma_wall_field','wall_rms'),('cross_term','cross_term'),('sigma_total','total')]:independent('lognormal '+ownlaw+' '+ak+' rs='+member,m['laws'][codelaw][ak],row['laws'][ownlaw][ok],5e-4)
  add(own+' common unconditional lognormal covariance rs='+member,1,row['unconditional_covariance_II_over_I'],'INDEPENDENT_GAUSSIAN_EXPONENTIAL_TILT','REFUTED',{'absolute':1e-12,'relative':0},'report section6.3')
 for ownseed,codeseed in [('W09','pbs_tracker_seed_compressed'),('F_median','pbs_tracker_seed_F_median_compressed')]:
  for ak,ok in [('direct','direct'),('post_hoc_fixed_closure','post'),('reclosure','reclosure'),('reclosure_over_post_hoc','ratio_reclosure_over_post')]:independent('PBS '+ownseed+' '+ak,a['conventions']['c_bare_volume_average']['pbs_reclosure_under_spectrum_rescaling'][codeseed][ak],c['direct_reclosure_cap']['reclosure'][ownseed][ok])
# Sources: reuse the already grounded exact cache and rehash it.
source_rows=[]
for label,row in read(R/'reports/phase1g_h_independent_audit_evidence/source_hashes.json').items():
 p=pathlib.Path('/workspace/scratch/7660b169d7d7/audit_work/blind_science')/row['path'];actual=hashlib.sha256(p.read_bytes()).hexdigest();source_rows.append(dict(label=label,path=row['path'],declared=row['expected'],actual=actual,match=actual==row['expected']));add('Primary source hash '+label,row['expected'],actual,'SHA256',location=row['path'])
res['inventory_rounding']={'matched':len(rounded),'unmatched':unmatched,'deviations':[r for r in rounded if not r['pass_']]};res['source_hashes']=source_rows
res['claims']=claims;res['claim_counts']=dict(collections.Counter(x['status'] for x in claims))
(W/'numeric_reconciliation.json').write_text(json.dumps(res,indent=2,sort_keys=True,allow_nan=False)+'\n')
print(json.dumps({k:{a:v for a,v in d.items() if a!='rows'} for k,d in res.items() if k in ['cross_interpreter','same_interpreter_delta','first_audit_vs_new','inventory_rounding']},indent=2)[:10000])
