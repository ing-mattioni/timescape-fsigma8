"""Read-only static/delta provenance audit; emits evidence only outside audited files."""
from pathlib import Path
from collections import Counter
import subprocess,json,hashlib,re,ast,datetime,sys
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
OUT=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else ROOT.parent/'audit_work/provenance'
OUT.mkdir(parents=True,exist_ok=True)
BASE='e5170285e1d4b4aa72e907a3a79110d05584c0d9';HEAD='ed0ec0c9c8783519a53759a265b6ce37e6c0e607';FROZEN='8d3cdd0533035858c42269cb1dff1a20dcafc7da'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def gittext(*args):return git(*args).decode()
def blob(commit,path):return git('show',f'{commit}:{path}')
def sha(b):return hashlib.sha256(b).hexdigest()
def no_dupes(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate key '+k)
  d[k]=v
 return d
def jsonread(path):return json.loads(path.read_text(),object_pairs_hook=no_dupes,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def flat(x,path=()):
 if isinstance(x,dict):
  for k,v in x.items():yield from flat(v,path+(k,))
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from flat(v,path+(str(i),))
 else:yield '/'.join(path),x
changes=[x.split('\t',1) for x in gittext('diff','--name-status',BASE,HEAD).splitlines()]
expected_m=['CLAUDE.md','README.md',*[f'reports/{p}{s}' for p in ['phase1g_h_audit_remediation','phase1g_h_delta_audit_remediation','phase1g_h_publication_successor'] for s in ['.md','_inventory.json']],*[f'reports/phase1g_h_global_variance_closure{s}' for s in ['.md','_inventory.json','_validation.md']],'scripts/phase1g_h_global_variance_closure_numerics.py','src/timescape_fsigma8/global_variance.py','tests/test_phase1g_h_global_variance.py']
expected_a=['reports/phase1g_h_delta_audit_2_remediation.md','reports/phase1g_h_delta_audit_2_remediation_inventory.json']+['reports/phase1g_h_delta_audit_2_remediation_logs/'+x for x in ['compare_evidence.py','cross_interpreter_313_vs_311.json','evidence_head.txt','evidence_py311.log','evidence_py313.log','extra_mutants_definitions.json','extra_mutants_results.json','full_suite_py311.log','full_suite_py313.log','make_campaign.py','mutation_campaign.log','regression_count.py','regression_recount_89cb041_vs_248a06b.json','regression_vs_248a06b.json','round3_mutant_definitions.json','run_extra_mutants.py','second_delta_audit_mutants_rerun.json','tolerance_audit.log']]
expected={*(('M',x) for x in expected_m),*(('A',x) for x in expected_a)}
actual={tuple(x) for x in changes}
commits={}
for h in [BASE,'9ad54253c4ec40cede5690da6659be28e0bd0a2d','4bf2718e7557ace3fdc0abffaa73587f1162f776',HEAD]:
 v=gittext('show','-s','--format=%H%n%T%n%P',h).splitlines();commits[h]={'tree':v[1],'parents':v[2].split(),'changed_paths':gittext('diff-tree','--no-commit-id','--name-status','-r',h).splitlines()}
base_paths=gittext('ls-tree','-r','--name-only',BASE).splitlines()
audit_patterns=('reports/phase1g_h_independent_audit','reports/phase1g_h_delta_audit.md','reports/phase1g_h_delta_audit_inventory.json','reports/phase1g_h_delta_audit_evidence/','reports/phase1g_h_delta_audit_2.md','reports/phase1g_h_delta_audit_2_inventory.json','reports/phase1g_h_delta_audit_2_evidence/')
protected=[p for p in base_paths if p.startswith(audit_patterns)]
protected_results={p:blob(BASE,p)==blob(HEAD,p) for p in protected}
frozen_paths=gittext('ls-tree','-r','--name-only',FROZEN).splitlines()
pkg=[p for p in frozen_paths if p.startswith('src/timescape_fsigma8/')]
pkg_results={p:blob(FROZEN,p)==blob(HEAD,p) for p in pkg}
frozen_reports=[p for p in frozen_paths if p.startswith('reports/phase1g_')]
frozen_report_results={p:blob(FROZEN,p)==blob(HEAD,p) for p in frozen_reports}
runner=['scripts/phase1g_h_global_variance_case.py']+[p for p in base_paths if p.startswith('scripts/phase1g_h_configs/')]
runner_results={p:blob(BASE,p)==blob(HEAD,p) for p in runner}
hashes=[]
for inventory,block,ref in [('phase1g_h_global_variance_closure_inventory.json',('files','added'),HEAD),('phase1g_h_delta_audit_2_remediation_inventory.json',('files_changed_sha256',),HEAD),('phase1g_h_audit_remediation_inventory.json',('files_changed_sha256',),'89cb041')]:
 d=jsonread(ROOT/'reports'/inventory)
 for k in block:d=d[k]
 for p,value in d.items():
  measured=sha(blob(ref,p));hashes.append({'inventory':'reports/'+inventory,'path':p,'reference_commit':ref,'recorded_sha256':value,'measured_sha256':measured,'matches':measured==value})
json_results=[]
for p in sorted((ROOT/'reports').glob('*.json')):
 try:d=jsonread(p);json_results.append({'path':str(p.relative_to(ROOT)),'valid':True,'unique_keys':True,'strict_nonfinite':True})
 except Exception as e:json_results.append({'path':str(p.relative_to(ROOT)),'valid':False,'error':str(e)})
snapshot=Path(__file__).with_name('provenance_remote_snapshot.json')
remote=jsonread(snapshot)['data'] if snapshot.exists() else {k:jsonread(OUT/(k+'.json')) for k in ['heads','tags','prs','releases']}
old_tags=jsonread(ROOT/'reports/phase1g_h_delta_audit_evidence/documentation_remote_tags.json')['data']
current_tag_map={x['ref']:x['object']['sha'] for x in remote['tags']};old_tag_map={x['ref']:x['object']['sha'] for x in old_tags}
peeled_tags={x['ref']:gittext('rev-parse',x['object']['sha']+'^{}').strip() for x in remote['tags']}
module='src/timescape_fsigma8/global_variance.py';script='scripts/phase1g_h_global_variance_closure_numerics.py'
def assignments(commit,path):
 tree=ast.parse(blob(commit,path));d={}
 for n in tree.body:
  if isinstance(n,ast.Assign):
   for t in n.targets:
    if isinstance(t,ast.Name):
     try:d[t.id]=ast.literal_eval(n.value)
     except Exception:pass
 return d
m0,m1=assignments(BASE,module),assignments(HEAD,module);s0,s1=assignments(BASE,script),assignments(HEAD,script)
constants=['RECORD_IDENTITY_RTOL','GROWTH_LAW_REALIZATION_ID','SCIENTIFIC_STATUS','NON_OBSERVATIONAL','SIGMA8_STATUS','FSIGMA8_STATUS']
status_keys=[k for k in m0 if k.isupper() and isinstance(m0[k],str)]
constant_values={k:{'base':m0.get(k),'head':m1.get(k),'same':m0.get(k)==m1.get(k)} for k in status_keys+['RECORD_IDENTITY_RTOL']}
tolerances={k:{'base':s0[k],'head':s1[k],'same':s0[k]==s1[k]} for k in ['GATES','ORTHANT_TOLERANCE','ORTHANT_START_NODES','RADIAL_INTERVALS','IDENTITY_RTOL']}
oldinv=json.loads(blob(BASE,'reports/phase1g_h_global_variance_closure_inventory.json'));newinv=jsonread(ROOT/'reports/phase1g_h_global_variance_closure_inventory.json')
numeric_result_preservation={k:oldinv.get(k)==newinv.get(k) for k in ['results','two_phase_covariance','status_tokens','observational_authorizations','assumptions','equations','definition','anchoring','missing_input']}
# Additive historical bodies: no removed non-header lines in their delta.
notes={}
for p in ['reports/phase1g_h_audit_remediation.md','reports/phase1g_h_audit_remediation_inventory.json','reports/phase1g_h_delta_audit_remediation.md','reports/phase1g_h_delta_audit_remediation_inventory.json']:
 diff=gittext('diff','--unified=0',BASE,HEAD,'--',p);removed=[l for l in diff.splitlines() if l.startswith('-') and not l.startswith('---')];notes[p]={'removed_line_count':len(removed),'only_additions':not removed,'original_bytes_available_at':BASE}
patterns=[r'not pushed',r'Nothing is pushed',r'remote head',r'remediated locally',r'same shared constraints',r'42 tests',r'42 phase tests',r'about 80 s',r'P1[–-]P9',r'physics.*H25|H25.*physics']
lex=[]
for p in [ROOT/'README.md',ROOT/'CLAUDE.md',*[ROOT/x for x in base_paths if x.startswith('reports/phase1g_h') and x.endswith(('.md','.json'))],ROOT/script]:
 for line_no,line in enumerate(p.read_text().splitlines(),1):
  if any(re.search(q,line,re.I) for q in patterns):
   if p.name in ['README.md','CLAUDE.md','phase1g_h_global_variance_closure.md'] and 'remote head' in line:kind='RESIDUE_P11_REMOTE_HEAD'
   elif p.name.startswith(('phase1g_h_independent_audit','phase1g_h_delta_audit_2','phase1g_h_delta_audit.md','phase1g_h_delta_audit_inventory','phase1g_h_delta_audit_evidence')):kind='HISTORICAL_AUDIT_OR_REMEDIATION'
   elif 'publication_successor' in p.name:kind='DATED_STATE_OR_LITERAL_QUOTATION'
   elif 'same shared constraints' in line:kind='HISTORICAL_WITH_GH_DF1_POINTER'
   elif '42' in line:kind='HISTORICAL_PRIOR_REMEDIATION_TEST_COUNT'
   else:kind='HISTORICAL_WITH_STATUS_NOTE'
   lex.append({'path':str(p.relative_to(ROOT)),'line':line_no,'classification':kind,'text':line})
prior=jsonread(ROOT/'reports/phase1g_h_delta_audit_2_inventory.json')
source_hashes={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in [ROOT/'AGENTS.md',ROOT/'CLAUDE.md',ROOT/'README.md',*[ROOT/x[1] for x in changes],*[ROOT/x for x in ['reports/phase1g_h_delta_audit_2.md','reports/phase1g_h_delta_audit_2_inventory.json','reports/phase1g_h_delta_audit.md','reports/phase1g_h_delta_audit_inventory.json','reports/phase1g_h_independent_audit.md','reports/phase1g_h_independent_audit_inventory.json','src/timescape_fsigma8/scientific_status.py','src/timescape_fsigma8/lagrangian_sigma.py']]]}
result={'schema_version':1,'audit_area':'PROVENANCE_GOVERNANCE_DOCUMENTATION','generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'remote_snapshot_utc':jsonread(snapshot)['retrieved_utc'] if snapshot.exists() else None,'audited_base':BASE,'audited_head':HEAD,'commits':commits,'changed_files':changes,'expected_diff_matches':actual==expected,'unexpected':sorted(actual-expected),'missing':sorted(expected-actual),'changed_file_counts':dict(Counter(x[0] for x in changes)),'preservation':{'previous_audits':{'count':len(protected_results),'all_identical':all(protected_results.values()),'mismatches':[k for k,v in protected_results.items() if not v]},'package_vs_frozen':{'count':len(pkg_results),'all_identical':all(pkg_results.values()),'mismatches':[k for k,v in pkg_results.items() if not v]},'frozen_reports':{'count':len(frozen_report_results),'all_identical':all(frozen_report_results.values()),'mismatches':[k for k,v in frozen_report_results.items() if not v]},'runner_and_configs':runner_results,'current_inventory_subtrees':numeric_result_preservation,'historical_additions':notes},'remote':{'heads':{x['ref']:x['object']['sha'] for x in remote['heads']},'tag_count':len(remote['tags']),'all_annotated':all(x['object']['type']=='tag' for x in remote['tags']),'tag_map_identical_to_first_delta_snapshot':current_tag_map==old_tag_map,'tag_map':current_tag_map,'peeled_tag_map':peeled_tags,'virtual_ls_remote_tag_ref_count':len(current_tag_map)*2,'pull_requests':[{'number':x['number'],'state':x['state'],'head':x['head']['ref'],'base':x['base']['ref'],'merged_at':x.get('merged_at')} for x in remote['prs']],'release_count':len(remote['releases']),'forbidden_D_v2_present':any('phase-1g-d-separate-universe-growth-v2' in x['ref'] for x in remote['tags']+remote['heads'])},'publication_graph':{k:gittext('rev-list','--reverse',v).splitlines() for k,v in {'P7':'89cb041..226e52d','P9':'226e52d..e517028','P10':'226e52d..4bf2718','P11':'4bf2718..ed0ec0c'}.items()},'owner_authorizations':{'P10':'DIRECTLY_CONFIRMED_CURRENT_HANDOFF','P11':'DIRECTLY_CONFIRMED_CURRENT_HANDOFF','P1_P9':'QUOTED_OR_PRIOR_AUDITOR_RECORD_NOT_INDEPENDENTLY_AUTHENTICATED','P9_provenance':'pasted transcript from a different session, explicitly secondary evidence; current branch+ancestry verified; authorization words NOT_VERIFIABLE here','new_audit_push':'NOT_AUTHORIZED'},'publication_limits':['Current refs and exact ancestry verify graph compatibility with the recorded fast-forwards; neither proves historical push actor/date or prior remote head.','No author session or conversation was accessed.','Current owner confirmation validates P10/P11 authorization, not a newly proposed audit push.'],'json_validation':{'count':len(json_results),'all_valid':all(x['valid'] for x in json_results),'results':json_results},'sha256_validation':hashes,'all_required_hashes_match':all(x['matches'] for x in hashes),'module_status_and_binding_constants':constant_values,'evidence_tolerances_and_thresholds':tolerances,'lexical_occurrences':lex,'previous_findings_recorded_status':{k:prior.get(k) for k in ['original_finding_status','delta_finding_status']},'source_sha256':source_hashes}
(OUT/'provenance_result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
(OUT/'full_delta.diff').write_bytes(git('diff',BASE,HEAD))
print(json.dumps({'diff_ok':result['expected_diff_matches'],'preservation':result['preservation'],'json_valid':result['json_validation']['all_valid'],'json_count':len(json_results),'required_hashes_match':result['all_required_hashes_match'],'tag_unchanged':result['remote']['tag_map_identical_to_first_delta_snapshot']},indent=2))
