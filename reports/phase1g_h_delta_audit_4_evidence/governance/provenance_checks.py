from pathlib import Path
import ast, hashlib, json, re, subprocess, collections

ROOT=Path('/workspace/scratch/1605b2925963/repo')
OUT=Path('/workspace/scratch/1605b2925963/audit_work/governance')
BASE='18bf2fbef880fdfb3c292956aa1f000720930abf'
HEAD='027b7a413fcee0786b861d5903272e4653d227ed'
FROZEN='8d3cdd0533035858c42269cb1dff1a20dcafc7da'
def git(*a): return subprocess.check_output(['git','-C',str(ROOT),*a])
def blob(commit,path): return git('show',commit+':'+path)
def sha(data): return hashlib.sha256(data).hexdigest()
def ls(commit): return git('ls-tree','-r','--name-only',commit).decode().splitlines()
diff=[line.split('\t') for line in git('diff','--name-status',BASE,HEAD).decode().splitlines()]
prior=ls(BASE); frozen=ls(FROZEN)
audit_files=[p for p in prior if any(p.startswith('reports/'+x) for x in ['phase1g_h_independent_audit','phase1g_h_delta_audit']) and '_remediation' not in p]
package=[p for p in frozen if p.startswith('src/') and p!='src/timescape_fsigma8/lagrangian_sigma.py']
frozen_reports=[p for p in frozen if p.startswith('reports/phase1g_')]
runner=[p for p in prior if p=='scripts/phase1g_h_global_variance_case.py' or p.startswith('scripts/phase1g_h_configs/')]
def preserve(paths,c1,c2):
 return {'count':len(paths),'changed':[p for p in paths if blob(c1,p)!=blob(c2,p)]}
r={'commits':{},'diff':{'total':len(diff),'by_status':dict(collections.Counter(x[0] for x in diff)),'paths':diff},'preservation':{'older_audits':preserve(audit_files,BASE,HEAD),'other_package_vs_frozen':preserve(package,FROZEN,HEAD),'frozen_1g_reports':preserve(frozen_reports,FROZEN,HEAD),'runner_configs':preserve(runner,BASE,HEAD),'lagrangian_sigma_base_vs_frozen':blob(BASE,'src/timescape_fsigma8/lagrangian_sigma.py')==blob(FROZEN,'src/timescape_fsigma8/lagrangian_sigma.py'),'status_module':blob(BASE,'src/timescape_fsigma8/scientific_status.py')==blob(HEAD,'src/timescape_fsigma8/scientific_status.py')}}
for c in [BASE,'c6028e9','6926a63','36d127f',HEAD,'ed0ec0c','4d71bd4']:
 a=git('show','-s','--format=%H %T %P',c).decode().split();r['commits'][a[0]]={'tree':a[1],'parents':a[2:]}
r['publication_graph']={k:git('rev-list','--reverse',*v).decode().splitlines() for k,v in {'P11':['4bf2718..ed0ec0c'],'P13':['ed0ec0c..18bf2fb'],'P14':['ed0ec0c..36d127f'],'P15':['36d127f..027b7a4']}.items()}
r['publication_graph']['P13_paths']=[x.split('\t') for x in git('diff','--name-status','ed0ec0c',BASE).decode().splitlines()]
r['declared_hash_checks']=[]
for p,dkey in [('reports/phase1g_h_global_variance_closure_inventory.json',('files','added')),('reports/phase1g_h_delta_audit_3_remediation_inventory.json',('files_changed_sha256',))]:
 d=json.loads(blob(HEAD,p));v=d
 for k in dkey:v=v[k]
 for path,expected in v.items():r['declared_hash_checks'].append({'inventory':p,'path':path,'expected':expected,'actual':sha(blob(HEAD,path)),'match':sha(blob(HEAD,path))==expected})
def no_duplicates(pairs):
 d={}
 for k,v in pairs:
  if k in d: raise ValueError('duplicate key '+k)
  d[k]=v
 return d
reports=[p for p in ls(HEAD) if p.startswith('reports/') and p.count('/')==1 and p.endswith('.json')]
r['report_json']={'count':len(reports),'invalid':[]}
for p in reports:
 try:json.loads(blob(HEAD,p),object_pairs_hook=no_duplicates,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
 except Exception as e:r['report_json']['invalid'].append([p,str(e)])
r['logs']=[]
for p in sorted((ROOT/'reports/phase1g_h_delta_audit_3_remediation_logs').iterdir()):
 data=p.read_bytes();txt=data.decode();d={'file':p.name,'bytes':len(data),'sha256':sha(data),'lines':len(txt.splitlines()),'unabbreviated_scratch_paths':re.findall(r'(?:/scratch|/tmp|/workspace/scratch)[^\s"\']*',txt),'tail':txt.splitlines()[-2:]}
 if p.suffix=='.json':
  val=json.loads(txt,object_pairs_hook=no_duplicates,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)));d['json_valid_unique_strict']=True
  if isinstance(val,list) and val and isinstance(val[0],dict) and 'outcome' in val[0]:d['outcomes']=dict(collections.Counter((v.get('origin','unspecified')+' '+v['outcome']) for v in val))
 r['logs'].append(d)
remote=json.loads((OUT/'remote_snapshot.json').read_text());old=json.loads((ROOT/'reports/phase1g_h_delta_audit_3_evidence/provenance_remote_snapshot.json').read_text())['data']
newtags={x['ref']:x['object'] for x in remote['tags']};oldtags={x['ref']:x['object'] for x in old['tags']}
r['remote']={'retrieved_at_utc':remote['retrieved_at_utc'],'branches':{v['ref']:v['object']['sha'] for v in remote['branches']},'annotated_tag_count':len(newtags),'tag_names_objects_unchanged':newtags==oldtags,'tag_count_logical_ref_plus_peeled':2*len(newtags),'peeled_tags':{},'prs':[{'number':v['number'],'state':v['state'],'head':v['head']['ref'],'merged_at':v['merged_at']} for v in remote['pull_requests']],'releases':len(remote['releases'])}
for ref,obj in newtags.items():
 raw=git('cat-file','-p',obj['sha']).decode();r['remote']['peeled_tags'][ref]={'object_sha':obj['sha'],'peeled_sha':raw.splitlines()[0].split()[1],'type':raw.splitlines()[1].split()[1]}
r['diff_check']={'rc':subprocess.run(['git','-C',str(ROOT),'diff','--check',BASE,HEAD],capture_output=True,text=True).returncode}
def constants(commit,path):
 tree=ast.parse(blob(commit,path));out={}
 for n in tree.body:
  if isinstance(n,ast.Assign):
   for t in n.targets:
    if isinstance(t,ast.Name) and t.id.isupper():out[t.id]=ast.dump(n.value,include_attributes=False)
 return out
r['status_constants_unchanged']={p:constants(BASE,p)==constants(HEAD,p) for p in ['src/timescape_fsigma8/global_variance.py','src/timescape_fsigma8/lagrangian_sigma.py']}
OUT.mkdir(parents=True,exist_ok=True);(OUT/'provenance_checks.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['logs','remote','publication_graph','declared_hash_checks','commits']},indent=2))
print('hash matches',sum(x['match'] for x in r['declared_hash_checks']),len(r['declared_hash_checks']))
print('logs',len(r['logs']),'unabbreviated scratch paths',sum(len(x['unabbreviated_scratch_paths']) for x in r['logs']))
print('tags',r['remote']['annotated_tag_count'],'unchanged',r['remote']['tag_names_objects_unchanged'],'1G-B',r['remote']['peeled_tags']['refs/tags/phase-1g-b-lagrangian-sigma-v1'])
