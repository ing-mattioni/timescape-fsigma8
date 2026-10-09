"""Independent fourth-delta probes; no audited repository mutations."""
from pathlib import Path
import dataclasses as dc,importlib.util,json,sys,math
from fractions import Fraction
import numpy as np
repo,out=map(Path,sys.argv[1:3]);sys.path.insert(0,str(repo/'src'))
def helper(f,n):
 sp=importlib.util.spec_from_file_location(n,repo/'tests'/f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
t=helper('test_phase1g_h_global_variance.py','gh'); b=helper('test_phase1g_b_contract_hardening.py','gb')
a=b.anchored();ref=b.reference();gv=t.gv;rows=[]
def try_(id,fn,**meta):
 r={'id':id,**meta}
 try:
  value=fn();r['accepted']=True
  try:json.dumps(value.to_json_dict() if hasattr(value,'to_json_dict') else value.to_metadata(),allow_nan=False);r['strict_json']=True
  except (TypeError,ValueError) as e:r['strict_json']=False;r['json_error']=str(e)
 except Exception as e:r.update(accepted=False,exception=type(e).__name__,message=str(e))
 rows.append(r)
for field in ['growth_ratio','early_spectrum_factor','reference_offset_from_anchor']:
 old=getattr(a,field);v=np.float32(old)
 try_('float32_anchor_'+field,lambda field=field,v=v:dc.replace(a,**{field:v}),old_value=old,stored_as_python_float=float(v),exact_native_equality=float(v)==old,numpy_equality=bool(v==old),relative_error=abs(float(v)-old)/max(abs(old),1e-300))
for field in ['quadrature_relative_change','truncation_envelope_fraction']:
 old=getattr(ref,field);v=np.float32(old)
 try_('float32_reference_'+field,lambda field=field,v=v:dc.replace(ref,**{field:v}),old_value=old,stored_as_python_float=float(v),exact_native_equality=float(v)==old,numpy_equality=bool(v==old),relative_error=abs(float(v)-old)/max(abs(old),1e-300))
try_('reference_truncation_zero',lambda:dc.replace(ref,truncation_envelope_fraction=0.0),original_value=ref.truncation_envelope_fraction,note='finite bounded diagnostic, intentionally not recomputed')
try_('premise_nonjson_radius',lambda:gv.HomogeneityPremise(radius=dc.replace(t.radius('c',100.0),length_h_inverse_Mpc=Fraction(100)),max_linear_rms=0.1,provenance='independent fourth audit'))
try_('growth_nonjson_background',lambda:gv.two_phase_global_growth(background=dc.replace(t.GM,H0_dressed_km_s_Mpc=Fraction(t.GM.H0_dressed_km_s_Mpc)),matching=t.MATCHING,checks=t.CHECKS,G=1.0))
res=t.run(t.GM,t.constant(0.05),t.radius('c'))
for eps in [0.95e-12,1.05e-12]:
 x=res.void_volume_response_rms;y=x*(1+eps)
 try_('identity_boundary_'+str(eps),lambda y=y:dc.replace(res,void_volume_response_rms=y),requested_relative_drift=eps,actual_relative_drift=abs(y-x)/max(abs(x),abs(y)),margin_vs_rtol=(abs(y-x)/max(abs(x),abs(y)))/1e-12)
# Discover nine serialized dataclasses and AST-shape assertion that strict JSON is last statement.
import ast
s=ast.parse((repo/'src/timescape_fsigma8/global_variance.py').read_text());checks=[]
for node in s.body:
 if not isinstance(node,ast.ClassDef):continue
 methods={m.name:m for m in node.body if isinstance(m,ast.FunctionDef)}
 if not ('to_json_dict' in methods or 'to_metadata' in methods):continue
 p=methods['__post_init__'];last=ast.unparse(p.body[-1]);checks.append({'class':node.name,'last_statement':last,'json_last':last.startswith('_require_strict_json(')})
out.write_text(json.dumps({'environment':{'python':sys.version,'numpy':np.__version__},'probes':rows,'json_coverage':checks},indent=1,allow_nan=False)+'\n')
print(json.dumps(rows,indent=1))
