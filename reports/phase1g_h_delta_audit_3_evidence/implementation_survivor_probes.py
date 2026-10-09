"""Behavioral witnesses for source-mutant survivors, in disposable copies.

Usage: python -B -W error THIS_FILE REPO PYTHON WORK OUT.json
WORK must be outside REPO. Only copied files in WORK are changed. This is
independent from the phase tests and complements the mutation outcomes.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO, PY, WORK, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
assert not WORK.resolve().is_relative_to(REPO.resolve())
SOURCE = "src/timescape_fsigma8/global_variance.py"
variants = [
    ("baseline", "", ""),
    ("B01_record_identity_rtol_10pct_drift", "RECORD_IDENTITY_RTOL = 1e-12", "RECORD_IDENTITY_RTOL = 1.1e-12"),
    ("B02_same_rejects_float_subclasses", "isinstance(stored, float) and math.isfinite(stored)",
     "type(stored) is float and math.isfinite(stored)"),
    ("B03_same_accepts_numpy_float32", "isinstance(stored, float)", "isinstance(stored, (float, np.floating))"),
    ("B10_one_growth_tolerance_not_converted",
     'object.__setattr__(self, name, _positive(getattr(self, name), name))',
     'object.__setattr__(self, name, _positive(getattr(self, name), name)) if name != "ode_atol" else _positive(getattr(self, name), name)'),
]
probe_code = r'''
import dataclasses as dc, importlib.util, json, sys
from fractions import Fraction
from pathlib import Path
import numpy as np
root=Path.cwd();sys.path.insert(0,str(root/'src'))
spec=importlib.util.spec_from_file_location('helpers',root/'tests/test_phase1g_h_global_variance.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
res=t.run(t.GM,t.constant(0.05),t.radius('c'))
class FloatSubclass(float): pass
rows=[]
def probe(ident,make):
 r={'probe':ident}
 try:
  obj=make();r['accepted']=True
  if hasattr(obj,'to_json_dict'):value=obj.to_json_dict()
  else:value=obj.to_metadata()
  try: json.dumps(value,allow_nan=False);r['strict_json']=True
  except Exception as e:r['strict_json']=False;r['json_error']=type(e).__name__+': '+str(e)
 except Exception as e:r['accepted']=False;r['exception']=type(e).__name__;r['message']=str(e)
 rows.append(r)
probe('eps_rms_relative_delta_1_05e_minus_12',lambda:dc.replace(res,void_volume_response_rms=res.void_volume_response_rms*(1+1.05e-12)))
probe('linear_sigma_numpy_float64',lambda:dc.replace(res,linear_sigma=np.float64(res.linear_sigma)))
probe('linear_sigma_float_subclass',lambda:dc.replace(res,linear_sigma=FloatSubclass(res.linear_sigma)))
diag=tuple((k,np.float32(v) if v==0.0 else v) for k,v in res.growth.diagnostics)
assert any(type(v) is np.float32 for k,v in diag)
probe('zero_diagnostics_numpy_float32',lambda:dc.replace(res.growth,diagnostics=diag))
probe('ode_atol_Fraction',lambda:dc.replace(t.CHECKS,ode_atol=Fraction(t.CHECKS.ode_atol)))
print(json.dumps(rows))
'''
results=[]
for ident, before, after in variants:
    dest = WORK / ident
    if dest.exists(): shutil.rmtree(dest)
    (dest / "tests").mkdir(parents=True)
    shutil.copytree(REPO / "src", dest / "src", ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"))
    shutil.copy2(REPO / "tests/test_phase1g_h_global_variance.py", dest / "tests/test_phase1g_h_global_variance.py")
    if before:
        path=dest / SOURCE
        content=path.read_text()
        assert before in content
        path.write_text(content.replace(before,after))
    env=dict(os.environ,OPENBLAS_NUM_THREADS="1",PYTHONDONTWRITEBYTECODE="1")
    run=subprocess.run([PY,"-B","-W","error","-c",probe_code],cwd=dest,env=env,
                       text=True,capture_output=True,check=True)
    results.append({"variant":ident,"probes":json.loads(run.stdout)})
    shutil.rmtree(dest)
OUT.write_text(json.dumps({"results":results},indent=1)+"\n")
print(json.dumps({"variants":len(results),"probes_per_variant":len(results[0]["probes"])}))
