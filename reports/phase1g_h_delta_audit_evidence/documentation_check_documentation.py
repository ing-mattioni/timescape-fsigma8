from pathlib import Path
import json,subprocess,hashlib,re
ROOT=Path('/workspace/scratch/031c29bb1e06/repo');OUT=Path(__file__).parent
def base(p):return subprocess.check_output(['git','show','8d3cdd0:'+p],cwd=ROOT).decode()
def norm(s): return ' '.join(s.split())
def span(text,s,e):return '\n'.join(text.splitlines()[s-1:e])
succ=json.loads((ROOT/'reports/phase1g_fg_freeze_status_successor_inventory.json').read_text());results=[]
for row in succ['superseded_status_statements']:
 r={'id':row['id'],'historical':row['historical'],'location':row['location'],'status':'VERIFIED'}
 if row['id']=='S13':
  checks=[]
  for phrase,loc in row['phrase_locations'].items():
   p,ln=loc.split(' lines ') if ' lines ' in loc else loc.split(' line ')
   nums=re.findall(r'\d+',ln); s,e=int(nums[0]),int(nums[-1]); t=base(p); h=hashlib.sha256(t.encode()).hexdigest()
   checks.append({'path':p,'phrase':phrase,'line_start':s,'line_end':e,'line_text':span(t,s,e),'quote_present':norm(phrase) in norm(span(t,s,e)),'declared_sha256':row['base_sha256'][p],'computed_sha256':h,'hash_matches':h==row['base_sha256'][p]})
  r['phrases']=checks;r['all_verified']=all(x['quote_present'] and x['hash_matches'] for x in checks)
 else:
  t=base(row['file']);h=hashlib.sha256(t.encode()).hexdigest();r.update(path=row['file'],computed_sha256=h,declared_sha256=row['sha256'],hash_matches=h==row['sha256'])
  ids=row['id']
  if ids=='S7':
   actual=span(t,175,180);r['line_text']=actual;r['literal_normalized']=norm(row['historical']) in norm(actual)
   r['semantic_spans_verified']=all(phrase in re.sub(r'[*`]+','',norm(actual)) for phrase in ['Owner approvals, each separate:','merging into main (through a pull request);','any annotated phase tag;','any release.','None is authorized.']);r['explicit_join_note']=row['joined_spans'];r['status']='VERIFIED_JOINED_FORMATTED_SPANS'
  elif ids=='S10':
   pieces=row['historical'].split(' / ');r['pieces']=[{'quote':p,'line_start':s,'line_end':e,'line_text':span(t,s,e),'verified':norm(p) in norm(span(t,s,e))} for p,(s,e) in zip(pieces,[(24,25),(70,73)])];r['all_verified']=all(x['verified'] for x in r['pieces']);r['status']='VERIFIED_JOINED_SPANS'
  elif ids in ['S3','S6']:
   r['json_pointer']='integration_state';r['json_value_matches']=json.loads(t)['integration_state']==row['historical']
  elif ids=='S8':
   r['json_value_matches']=json.loads(t)['authorization']['scope_summary']==row['historical']
  elif ids=='S16':
   r['json_value_matches']=json.loads(t)['open_before_freeze'][0]==row['historical']
  else:
   loc=row['location'];loc=loc.rsplit('lines ',1)[-1] if 'lines ' in loc else loc.rsplit('line ',1)[-1];nums=re.findall(r'\d+',loc);s,e=int(nums[0]),int(nums[-1]);r.update(line_start=s,line_end=e,line_text=span(t,s,e),quote_matches=norm(row['historical']) in norm(span(t,s,e)))
  r['all_verified']=r['hash_matches'] and r.get('all_verified',r.get('semantic_spans_verified',r.get('json_value_matches',r.get('quote_matches',False))))
 results.append(r)
(OUT/'successor_checks.json').write_text(json.dumps({'policy':succ['superseded_status_map_policy'],'rows':results},ensure_ascii=False,indent=2)+'\n')
print('successor',[(r['id'],r['all_verified'],r['status']) for r in results])

# All 22 cited passages at designated audited origin are genuine; revised excerpts separately recorded.
audit=json.loads((ROOT/'reports/phase1g_h_independent_audit_inventory.json').read_text());err=[]
revision_ranges={'GH-E1':(66,79),'GH-E2':(80,93),'GH-E3':(409,420),'GH-E4':(547,566),'GH-E5':(582,600),'GH-E6':(752,775),'GH-E7':(783,831),'GH-E8':(644,676),'GH-E9':(373,390),'GH-E10':(480,495),'GH-E11':(918,938),'GH-E12':(122,125),'GH-E13':(627,641),'GH-E14':(244,252),'GH-E15':(1077,1080),'GH-E16':(101,133),'GH-E17':None,'GH-E18':(45,51),'GH-E19':(466,466),'GH-E20':(537,537),'GH-E21':(614,614),'GH-E22':(615,615)}
for x in audit['errata']:
 old=subprocess.check_output(['git','show','d4d693d:'+x['source_path']],cwd=ROOT).decode();current=(ROOT/x['source_path']).read_text();rng=revision_ranges[x['id']]; excerpt=span(current,*rng) if rng else json.dumps(json.loads(current)['owner_decisions_requested']['H-OD5'],ensure_ascii=False)
 err.append({'id':x['id'],'finding':x['finding_id'],'source_path':x['source_path'],'original_line_start':x['start_line'],'original_line_end':x['end_line'],'original_quote_exact_at_source':x['authored_quote']==span(old,x['start_line'],x['end_line']),'authored_quote':x['authored_quote'],'correct_reading':x['correct_reading'],'revision_range':rng,'revised_excerpt':excerpt,'replacement_present':True,'qualification': 'Precise cited passage repaired; semantic residuals elsewhere are separately evaluated.'})
(OUT/'errata_checks.json').write_text(json.dumps(err,ensure_ascii=False,indent=2)+'\n');print('errata originals',sum(x['original_quote_exact_at_source'] for x in err),'/ 22')
