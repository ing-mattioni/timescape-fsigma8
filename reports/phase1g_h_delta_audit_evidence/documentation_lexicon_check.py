import json,re
from pathlib import Path
ROOT=Path('/workspace/scratch/031c29bb1e06/repo');OUT=Path(__file__).parent
paths=['README.md','CLAUDE.md','reports/phase1g_h_global_variance_closure.md','reports/phase1g_h_audit_remediation.md','reports/phase1g_h_global_variance_closure_inventory.json','reports/phase1g_h_audit_remediation_inventory.json','src/timescape_fsigma8/global_variance.py','scripts/phase1g_h_global_variance_closure_numerics.py','scripts/phase1g_h_global_variance_case.py']
patterns={'closure_independent':r'closure.independent','closed_definition':r'closed definition|definition.*closed','any_region':r'any Lagrangian region|every Lagrangian region','only_p':r'single missing|one missing|p alone|only through','perturbative':r'perturbative|controlled.*error|epsilon.*threshold|ε.*threshold','anchor_transfer':r'corrects.*transfer|cancels.*growth|cancels exactly|transfer recalibration|fixed.closure|post.hoc','common_covariance':r'wall.density covariance|wall.field covariance|same shared constraints|sharing the acquired constraints','S1_necessary':r'S1.*required|S1.*necessary|S1.*freedom|S1.*select|but is required','pointwise_bound':r'varies by at most|position relative to the interval'}
rows=[]
for p in paths:
 lines=(ROOT/p).read_text().splitlines()
 for n,line in enumerate(lines,1):
  terms=[k for k,v in patterns.items() if re.search(v,line,re.I)]
  if not terms:continue
  ctx='\n'.join(lines[max(0,n-4):min(len(lines),n+3)])
  cat='QUALIFIED_CURRENT_STATEMENT_OR_EXPLICIT_WITHDRAWAL'
  reason='Read within adjacent stated model, history, negative or conditional qualifier; keyword presence alone is not a finding.'
  if p=='reports/phase1g_h_global_variance_closure.md' and 883<=n<=885:cat='RESIDUAL_RETIRED_CURRENT_CLAIM';reason='Self-check is not a frozen historical source and still asserts transfer-only calibration contrary to §5.4/GH-F6.'
  elif p=='reports/phase1g_h_global_variance_closure.md' and 893<=n<=894:cat='RESIDUAL_RETIRED_CURRENT_CLAIM';reason='S1 necessity remains while §3.3 restricts necessity to wall-density freedom/GH-F7.'
  elif p=='reports/phase1g_h_global_variance_closure.md' and 598<=n<=600:cat='NEW_OVERSTATEMENT';reason='G_eff/G(0)−1 is an integrated weighted deviation, not a maximum of G(k) over broad spectral support or an interval error bound.'
  elif 'common_covariance' in terms:cat='SCIENCE_REVIEW_REQUIRED';reason='New positive-density equality assertion requires normalizer comparison; independently handled by scientific workstream.'
  elif p=='reports/phase1g_h_audit_remediation.md':cat='REMEDIATION_MAP_OR_HISTORICAL_QUOTATION';reason='This record identifies replaced original claims rather than asserting each old phrase.'
  rows.append({'path':p,'line':n,'terms':terms,'text':line,'context':ctx,'classification':cat,'reason':reason})
(OUT/'lexicon_classification.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
from collections import Counter
print(len(rows),Counter(r['classification'] for r in rows))
