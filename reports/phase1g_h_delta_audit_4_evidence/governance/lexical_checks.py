from pathlib import Path
import subprocess,re,json,collections
repo=Path('/workspace/scratch/1605b2925963/repo');out=Path('/workspace/scratch/1605b2925963/audit_work/governance')
terms=['not pushed','Nothing is pushed','remote head','P11','P1–P13','49 phase tests','49 tests','conditional_density_covariance_ball','both-walls conditional covariance','strict JSON holds by construction','store floats','32 skipped']
paths=subprocess.check_output(['git','-C',str(repo),'ls-tree','-r','--name-only','027b7a4']).decode().splitlines();rows=[]
for p in paths:
 if Path(p).suffix not in ['.py','.md','.json','.txt','.log','.sh']:continue
 try:txt=(repo/p).read_text()
 except (UnicodeError,FileNotFoundError):continue
 for i,line in enumerate(txt.splitlines(),1):
  found=[t for t in terms if t.lower() in line.lower()]
  if not found:continue
  category='LEGITIMATE'
  if p.startswith('reports/phase1g_h_'):
   if any(x in p for x in ['_audit','_logs/','_evidence/','_validation']):category='HISTORICAL_OR_EXPLICIT_EVIDENCE'
   elif 'publication_successor' in p:category='HISTORICAL_EVENT_OR_CONVENTION'
   elif 'global_variance_closure_inventory' in p and any(t in found for t in ['both-walls conditional covariance','conditional_density_covariance_ball']):category='HISTORICAL_LABEL_WITH_EXPLICIT_RENAME_NOTE'
   else:category='LEGITIMATE_CURRENT_REFERENCE_OR_FORMULA'
  elif p in ['README.md','CLAUDE.md']:
   category='HISTORICAL_DATED_AUDIT_SUMMARY' if '49 phase tests' in found else 'LEGITIMATE_CURRENT_REFERENCE_OR_CONVENTION'
  elif p=='scripts/phase1g_h_global_variance_closure_numerics.py' and 'conditional_density_covariance_ball' in found:category='EXPLICIT_FORMER_KEY_DOCSTRING'
  elif p.startswith('reports/') and any(t.lower() in line.lower() for t in ['not pushed','remote head','32 skipped','Nothing is pushed']):category='FROZEN_OR_DATED_HISTORICAL_RECORD'
  rows.append({'path':p,'line':i,'terms':found,'classification':category,'text':line})
summary={'scope':'All tracked text paths at 027b7a4; classifications concern requested phrases, not wholesale proof of every surrounding historical assertion. P11 also names a wall probability in formulas.','rows':rows,'count':len(rows),'category_counts':dict(collections.Counter(r['classification'] for r in rows)),'term_counts':{t:sum(t in r['terms'] for r in rows) for t in terms},'residuals':[]}
(out/'lexical_checks.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='rows'},indent=2))
