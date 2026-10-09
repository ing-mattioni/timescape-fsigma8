"""A missing EvaluatedVoidShare JSON-check witness; copies only outside repo."""
import sys,shutil,os,subprocess,json
from pathlib import Path
repo,py,w,out=Path(sys.argv[1]),sys.argv[2],Path(sys.argv[3]),Path(sys.argv[4]);w.mkdir(exist_ok=True)
code=r'''
from pathlib import Path
import sys,importlib.util,dataclasses as dc,json
from fractions import Fraction
root=Path.cwd();sys.path.insert(0,str(root/'src'))
s=importlib.util.spec_from_file_location('t',root/'tests/test_phase1g_h_global_variance.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
growth=t.gv.two_phase_global_growth(background=t.GM,matching=t.MATCHING,checks=t.CHECKS,G=1.0)
density=t.ls.early_matter_density_per_photon(background=t.GM,identity_tolerance=1e-13,G=1.0)
sp=importlib.util.spec_from_file_location('b',root/'tests/test_phase1g_b_contract_hardening.py');b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
record=b.anchored()
import math
changed=math.nextafter(record.growth_ratio,math.inf)
rows=[]
try:
 value=dc.replace(record,growth_ratio=changed)
 row={'exact_native_equality':changed==record.growth_ratio,'original':record.growth_ratio,'one_ulp_change':changed,'accepted':True,'stored_type':type(value.growth_ratio).__name__}
 try:json.dumps(value.to_json_dict(),allow_nan=False);row['strict_json']=True
 except (TypeError,ValueError) as e:row.update(strict_json=False,message=str(e))
except Exception as e:row={'accepted':False,'exception':type(e).__name__,'message':str(e)}
print(json.dumps(row))
'''
results=[]
for name,mutate in [('baseline',False),('X11_growth_ratio_approximate_1e12',True)]:
 d=w/name
 if d.exists():shutil.rmtree(d)
 (d/'tests').mkdir(parents=True)
 shutil.copytree(repo/'src',d/'src',ignore=shutil.ignore_patterns('__pycache__','*.egg-info'))
 shutil.copy2(repo/'tests/test_phase1g_h_global_variance.py',d/'tests/test_phase1g_h_global_variance.py')
 shutil.copy2(repo/'tests/test_phase1g_b_contract_hardening.py',d/'tests/test_phase1g_b_contract_hardening.py')
 if mutate:
  definition=next(x for x in json.loads(Path('/workspace/scratch/1605b2925963/audit_work/contracts/own_definitions.json').read_text()) if x['id']=='X11_growth_ratio_approximate_1e12')
  p=d/definition['file'];s=p.read_text();assert s.count(definition['old'])==1;p.write_text(s.replace(definition['old'],definition['new']))
 r=subprocess.run([py,'-B','-W','error','-c',code],cwd=d,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True,check=True)
 results.append({'variant':name,**json.loads(r.stdout)})
 shutil.rmtree(d)
out.write_text(json.dumps(results,indent=1)+'\n');print(json.dumps(results,indent=1))
