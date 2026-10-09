import json,sys
from pathlib import Path
from collections import Counter
w=Path(sys.argv[1]); a=json.loads((w/'scalar_old.json').read_text());b=json.loads((w/'scalar_new.json').read_text())
ad={r['id']:r for r in a['probes']};bd={r['id']:r for r in b['probes']};changed=[{'id':k,'record':ad[k]['record'],'old_accepted':ad[k]['accepted'],'new_accepted':bd[k]['accepted'],'new_message':bd[k].get('message')}for k in ad if ad[k]['accepted']!=bd[k]['accepted']]
summary={'count_old':a['summary']['probes'],'count_new':b['summary']['probes'],'accepted_old':a['summary']['accepted'],'accepted_new':b['summary']['accepted'],'non_strict_old':len(a['summary']['accepted_non_strict_json']),'non_strict_new':len(b['summary']['accepted_non_strict_json']),'nonfinite_old':len(a['summary']['accepted_nonfinite']),'nonfinite_new':len(b['summary']['accepted_nonfinite']),'changed_by_record':dict(Counter(r['record']for r in changed)),'new_acceptances':[r for r in changed if r['new_accepted']],'changes':changed}
(w/'scalar_comparison.json').write_text(json.dumps(summary,indent=1)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='changes'},indent=1))
