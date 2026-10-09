"""Additional audit probes, distinct from the repository's unchanged tests.

Run with PYTHONPATH pointing at each disposable mutation source tree.
These demonstrate the defensive invariant removed by selected mutations.
"""
import dataclasses as dc
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np

root=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location('focal_helpers',root/'tests/test_phase1g_h_global_variance.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
gv=t.gv
res=t.run(t.GM,t.constant(.05),t.radius('c'))
other=t.run(t.NW15,t.constant(.05),t.radius('c'))
iv=gv.admissible_global_linear_interval(target=res,premise=gv.HomogeneityPremise(radius=t.radius('c',100),max_linear_rms=.1,provenance='audit'))
checks=[]
for ident,fn in (
    ('background_fv0_consistency',lambda:dc.replace(other.growth,background=t.GM)),
    ('constant_void_share_consistency',lambda:dc.replace(res.void_share,share_k0=.95)),
    ('effective_propagator_ratio',lambda:dc.replace(res,effective_propagator=res.effective_propagator*1.01)),
    ('interval_target_inside_flag',lambda:dc.replace(iv,target_inside=not iv.target_inside)),
):
    try:fn();checks.append({'id':ident,'rejected':False})
    except gv.GlobalVarianceContractError as e:checks.append({'id':ident,'rejected':True,'message':str(e)})
saved=gv._orthant_integrals
gv._orthant_integrals=lambda *args:(np.array([2.,0.,0.,0.,0.]),32,0.)
try:
    v=gv.bivariate_normal_orthant_probability(correlation=.5,threshold_1=0.,threshold_2=0.,nodes=16,tolerance=1e-12)
    checks.append({'id':'frechet_rejects_injected_invalid_quadrature','rejected':False,'accepted_value':v})
except gv.GlobalVarianceNumericalError as e:checks.append({'id':'frechet_rejects_injected_invalid_quadrature','rejected':True,'message':str(e)})
finally:gv._orthant_integrals=saved
print(json.dumps({'source_module':gv.__file__,'checks':checks},indent=2))
