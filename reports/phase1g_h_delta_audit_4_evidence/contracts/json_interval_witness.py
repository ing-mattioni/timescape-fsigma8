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
res=t.run(t.GM,t.constant(0.05),t.radius('c'))
premise=t.gv.HomogeneityPremise(radius=t.radius('c',100.0),max_linear_rms=.1,provenance='audit interval witness')
iv=t.gv.admissible_global_linear_interval(target=res,premise=premise)
rad=dc.replace(iv.premise_radius,radius_Mpc=Fraction(iv.premise_radius.radius_Mpc))
rows=[]
try:
 value=dc.replace(iv,premise_radius=rad)
 row={'accepted':True,'stored_type':type(value.premise_radius.radius_Mpc).__name__}
 try:json.dumps(value.to_json_dict(),allow_nan=False);row['strict_json']=True
 except (TypeError,ValueError) as e:row.update(strict_json=False,message=str(e))
except Exception as e:row={'accepted':False,'exception':type(e).__name__,'message':str(e)}
print(json.dumps(row))
'''
results=[]
for name,mutate in [('baseline',False),('X04_interval_json_check_removed',True)]:
 d=w/name
 if d.exists():shutil.rmtree(d)
 (d/'tests').mkdir(parents=True)
 shutil.copytree(repo/'src',d/'src',ignore=shutil.ignore_patterns('__pycache__','*.egg-info'))
 shutil.copy2(repo/'tests/test_phase1g_h_global_variance.py',d/'tests/test_phase1g_h_global_variance.py')
 if mutate:
  p=d/'src/timescape_fsigma8/global_variance.py';s=p.read_text();old='        _require_strict_json(self.to_json_dict(), "interval record")\n';assert s.count(old)==1;p.write_text(s.replace(old,''))
 r=subprocess.run([py,'-B','-W','error','-c',code],cwd=d,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True,check=True)
 results.append({'variant':name,**json.loads(r.stdout)})
 shutil.rmtree(d)
out.write_text(json.dumps(results,indent=1)+'\n');print(json.dumps(results,indent=1))
