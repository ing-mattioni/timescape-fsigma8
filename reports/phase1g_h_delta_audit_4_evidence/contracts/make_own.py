from pathlib import Path
import json
w=Path('/workspace/scratch/1605b2925963/audit_work/contracts')
SRC='src/timescape_fsigma8/global_variance.py'; LS='src/timescape_fsigma8/lagrangian_sigma.py'; TEST='tests/test_phase1g_h_global_variance.py'
HT=['tests/test_phase1g_h_global_variance.py']; LT=['tests/test_phase1g_b_lagrangian_sigma.py','tests/test_phase1g_b_owner_decisions.py','tests/test_phase1g_b_contract_hardening.py']
rows=[]
def add(i,f,old,new,tests=HT,note=''):
 rows.append(dict(id=i,file=f,old=old,new=new,tests=tests,origin='fourth_delta_audit',note=note))
add('X01_growth_json_check_removed',SRC,'        _require_strict_json(self.to_json_dict(), "growth record")\n','')
add('X02_void_share_json_check_removed',SRC,'        _require_strict_json(self.to_json_dict(), "void share")\n','')
add('X03_premise_json_check_removed',SRC,'        _require_strict_json(self.to_metadata(), "homogeneity premise")\n','')
add('X04_interval_json_check_removed',SRC,'        _require_strict_json(self.to_json_dict(), "interval record")\n','')
add('X05_growth_json_before_validation',SRC,'    def __post_init__(self) -> None:\n        _require(self.background, TimescapeTrackerInput, "background")','    def __post_init__(self) -> None:\n        _require_strict_json(self.to_json_dict(), "growth record")\n        _require(self.background, TimescapeTrackerInput, "background")')
add('X06_growth_ratio_approximate_1e8',LS,'self.growth_ratio == (ts.growth.growth_today_photon_normalised\n                                      / ref.growth_today_photon_normalised)','math.isclose(self.growth_ratio, ts.growth.growth_today_photon_normalised\n                                      / ref.growth_today_photon_normalised, rel_tol=1e-8, abs_tol=0.0)',LT)
add('X07_growth_ratio_operands_swapped',LS,'self.growth_ratio == (ts.growth.growth_today_photon_normalised\n                                      / ref.growth_today_photon_normalised)','self.growth_ratio == (ref.growth_today_photon_normalised\n                                      / ts.growth.growth_today_photon_normalised)',LT)
add('X08_growth_ratio_float_conversion',LS,'self.growth_ratio == (ts.growth.growth_today_photon_normalised','float(self.growth_ratio) == (ts.growth.growth_today_photon_normalised',LT,'A desirable stricter-policy change; a survivor is a precision-limit coverage gap, not an accepted unsafe defect.')
add('X09_simpson_exact_error_budget_to_1pct',TEST,'pytest.approx(error, rel=2e-3, abs=0.0)','pytest.approx(error, rel=1e-2, abs=0.0)')
add('X10_simpson_ratio_budget_to_1pct',TEST,'pytest.approx(16.0, rel=5e-3, abs=0.0)','pytest.approx(16.0, rel=1e-2, abs=0.0)')
add('X11_growth_ratio_approximate_1e12',LS,'self.growth_ratio == (ts.growth.growth_today_photon_normalised\n                                      / ref.growth_today_photon_normalised)','math.isclose(self.growth_ratio, ts.growth.growth_today_photon_normalised\n                                      / ref.growth_today_photon_normalised, rel_tol=1e-12, abs_tol=0.0)',LT)
add('D1_adapted_binding_disabled',SRC,'    for name, expected in values.items():\n        stored = getattr(record, name)','    for name, expected in ():\n        stored = getattr(record, name)')
add('X12_lcdm_relative_change_float_conversion',LS,'if not (self.quadrature_relative_change\n                == abs(self.sigma_unit_growth','if not (float(self.quadrature_relative_change)\n                == abs(self.sigma_unit_growth',LT,'Desirable stricter-policy probe.')
# Keep duplicated late check off so X05 truly moves rather than duplicates check.
r=next(r for r in rows if r['id'].startswith('X05'))
# Runner uses one string replacement, so move across exact whole post-init block.
s=(Path('/workspace/scratch/1605b2925963/repo')/SRC).read_text()
start=s.index(r['old']); end=s.index('    def to_json_dict(self)',start)
old=s[start:end];new=old.replace('        _require_strict_json(self.to_json_dict(), "growth record")\n','')
new=new.replace(r['old'],r['new'])
r['old'],r['new']=old,new
(w/'own_definitions.json').write_text(json.dumps(rows,indent=1)+'\n')
print(len(rows),'own mutants')
