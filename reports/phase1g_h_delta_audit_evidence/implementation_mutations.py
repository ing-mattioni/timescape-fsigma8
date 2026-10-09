"""Delta-audit mutation campaign in disposable independent copies.

No mutation of the audited repository. Results identify actual test and
evidence gate failures, rather than labelling every source change killed.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess

ROOT=Path('/workspace/scratch/031c29bb1e06/repo')
OUT=Path(__file__).parent
PY=str(ROOT/'.venv/bin/python')
BASE=OUT/'mutation_base'
BASE.mkdir(exist_ok=True)
for name in ('src','scripts'):
    shutil.copytree(ROOT/name,BASE/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
(BASE/'tests').mkdir(exist_ok=True)
for name in ('test_phase1g_h_global_variance.py','conftest.py'):
    shutil.copy2(ROOT/'tests'/name,BASE/'tests'/name)
shutil.copy2(ROOT/'pyproject.toml',BASE/'pyproject.toml')
if not (BASE/'reports').exists(): (BASE/'reports').symlink_to(ROOT/'reports',target_is_directory=True)
SOURCE='src/timescape_fsigma8/global_variance.py'
SCRIPT='scripts/phase1g_h_global_variance_closure_numerics.py'
src=(BASE/SOURCE).read_text(); script=(BASE/SCRIPT).read_text()
old=json.loads((ROOT/'reports/phase1g_h_independent_audit_evidence/mutation_results.json').read_text())
mutants=[]
for m in old:
    if m['id']=='baseline':continue
    a,b=m['old'],m['new']
    if m['id']=='M7_shift_orthant_lower':
        a='lo = max(c1, -_ORTHANT_HALF_WIDTH)';b='lo = max(c1 + 0.1, -_ORTHANT_HALF_WIDTH)'
    mutants.append((m['id'],SOURCE,a,b,False))
mutants.extend([
('N1_growth_record_validation_off',SOURCE,'if self.fv0 != self.background.fv0:','if False:',False),
('N2_void_share_record_validation_off',SOURCE,'if p0 != self.closure.share:','if False:',False),
('N3_sigma_record_validation_off',SOURCE,'if self.effective_propagator != self.linear_sigma / self.unit_growth_sigma:','if False:',False),
('N4_interval_record_validation_off',SOURCE,'if self.target_inside != (self.premise_compatible\n                                  and self.lower <= self.target_value <= self.upper):','if False:',False),
('N5_orthant_centre_split_off',SOURCE,'for b in (u_star - 8.0 * width, u_star, u_star + 8.0 * width):','for b in (u_star - 8.0 * width, u_star + 8.0 * width):',False),
('N6_orthant_transition_edges_off',SOURCE,'for b in (u_star - 8.0 * width, u_star, u_star + 8.0 * width):','for b in (u_star,):',False),
('N7_orthant_refinement_off',SOURCE,'previous = evaluate(n)\n    while True:','previous = evaluate(n)\n    return previous, n, 0.0\n    while True:',False),
('N8_frechet_gate_off',SOURCE,'if not lower - tol <= p11 <= upper + tol:','if False:',False),
('N9_void_share_identity_text_sign_reversed',SOURCE,'``p = f_v,LS - d f_v,L/d delta_L``','``p = f_v,LS + d f_v,L/d delta_L``',False),
('N9b_pbs_executable_response_sign_reversed',SOURCE,'threshold = phi_nu / sigma_s','threshold = -phi_nu / sigma_s',False),
('N10_reclosure_factor_unsquared',SCRIPT,'spec_re = early_spectrum(2.100e-9 * anchor_factor ** 2)','spec_re = early_spectrum(2.100e-9 * anchor_factor)',True),
('N11_lognormal_wall_normalization_off',SCRIPT,'q0 = float(ndtr(-(c - kappa0)))','q0 = f_w',True),
('N12_lognormal_lambda_not_squared',SCRIPT,'math.exp(lam * lam * xi_lat_r)','math.exp(lam * xi_lat_r)',True),
('N13_rounding_output_half_unit_off',SCRIPT,'budget = half * (sp / var["rms"] + si / var["rms"] + 1.0)','budget = half * (sp / var["rms"] + si / var["rms"])',True),
('N14_step_cutoff_shifted',SCRIPT,'k_cut = math.exp(log_k)','k_cut = math.exp(log_k) * 0.9',True),
])

def run_case(ident,path=None,a='',b='',evidence=False):
    dest=OUT/'mutations'/ident
    shutil.copytree(BASE,dest,dirs_exist_ok=True,symlinks=True)
    if path:
        text=(dest/path).read_text()
        count=text.count(a)
        if not count: return {'id':ident,'outcome':'MUTATION_NOT_APPLIED','old':a}
        # text sign reversal deliberately affects both identical public docstring occurrences.
        (dest/path).write_text(text.replace(a,b))
    else: count=0
    env=os.environ.copy();env['PYTHONPATH']=str(dest/'src');env['PYTHONDONTWRITEBYTECODE']='1'
    log=OUT/'mutation_logs'/f'{ident}.log';log.parent.mkdir(exist_ok=True)
    tests=subprocess.run([PY,'-B','-W','error','-m','pytest','-q','--tb=short','tests/test_phase1g_h_global_variance.py'],cwd=dest,env=env,text=True,capture_output=True)
    log.write_text(tests.stdout+tests.stderr)
    row={'id':ident,'source_file':path,'old':a,'new':b,'replacement_count':count,'test_returncode':tests.returncode,'test_summary':next((line for line in reversed(tests.stdout.splitlines()) if re.search(r'\b(passed|failed|error|errors)\b',line)),''),'failed_test_names':re.findall(r'^FAILED ([^ ]+)',tests.stdout,re.M),'test_log':str(log.relative_to(OUT)),'evidence_ran':evidence}
    if path:row['mutated_source_sha256']=hashlib.sha256((dest/path).read_bytes()).hexdigest()
    if evidence:
        elog=OUT/'mutation_logs'/f'{ident}_evidence.log'
        ev=subprocess.run([PY,'-B','-W','error',SCRIPT,'--no-figures'],cwd=dest,env=env,text=True,capture_output=True)
        elog.write_text(ev.stdout+ev.stderr)
        row.update(evidence_returncode=ev.returncode,evidence_failures=ev.stdout[ev.stdout.find('GATE FAILURES:'):] if 'GATE FAILURES:' in ev.stdout else '',evidence_log=str(elog.relative_to(OUT)))
    killed=tests.returncode!=0 or row.get('evidence_returncode',0)!=0
    row['outcome']='BASELINE_PASS' if not path and not killed else ('KILLED' if killed else 'SURVIVED')
    return row

results=[]
for args in [('baseline',None,'','',False)]+mutants:
    print('starting '+args[0],flush=True)
    result=run_case(*args)
    results.append(result)
    (OUT/'mutation_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:result.get(k) for k in ('id','outcome','test_summary','evidence_returncode','evidence_failures')}),flush=True)
print('campaign complete',flush=True)
