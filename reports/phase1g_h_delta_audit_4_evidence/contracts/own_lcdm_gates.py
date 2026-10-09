"""Run existing 1G-B evidence gates for the three source-mutant survivors."""
from pathlib import Path
import json,shutil,subprocess,os,concurrent.futures as cf
w=Path('/workspace/scratch/1605b2925963/audit_work/contracts');repo=Path('/workspace/scratch/1605b2925963/repo');py='/workspace/scratch/1605b2925963/.venv313/bin/python'
defs=[x for x in json.loads((w/'own_definitions.json').read_text())if x['id'].split('_')[0]in ['X08','X11','X12']]
def run(m):
 d=w/'ls_gate_work'/m['id'];d.mkdir(parents=True,exist_ok=True)
 for name in ['src','scripts']:shutil.copytree(repo/name,d/name,ignore=shutil.ignore_patterns('__pycache__','*.egg-info'),dirs_exist_ok=True)
 (d/'reports').symlink_to(repo/'reports')
 p=d/m['file'];s=p.read_text();assert s.count(m['old'])==1;p.write_text(s.replace(m['old'],m['new']))
 r=subprocess.run([py,'-B','-W','error','scripts/validate_phase1g_b_lagrangian_sigma.py'],cwd=d,env={**os.environ,'PYTHONPATH':str(d/'src'),'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'},text=True,capture_output=True)
 (w/(m['id']+'_1gb_gate.log')).write_text(r.stdout+r.stderr)
 row={'id':m['id'],'gate_rc':r.returncode,'tail':(r.stdout+r.stderr).splitlines()[-5:]}
 shutil.rmtree(d);return row
with cf.ThreadPoolExecutor(max_workers=2)as pool:
 rows=list(pool.map(run,defs))
(w/'own_lcdm_gate_results.json').write_text(json.dumps(rows,indent=1)+'\n');print(json.dumps(rows,indent=1))
