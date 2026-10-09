"""Separate numerical invariance from environment/HEAD-bearing artifact hashes."""
from pathlib import Path
import copy, hashlib, json, os, subprocess
ROOT=Path(os.environ.get("TIMESCAPE_AUDIT4_WORKSPACE", str(Path(__file__).resolve().parents[2]))).resolve()
OUT=ROOT/"audit_work/reproduction"
TARGET="5746cc76e932ad0db3e253ee5aa5f0032227e65afba1699a09ea1f2c32d13c8d"
a=json.loads((OUT/"phase1g_b_baseline.json").read_text())
b=json.loads((OUT/"phase1g_b_main.json").read_text())
def sha(x):return hashlib.sha256((json.dumps(x,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()).hexdigest()
heads={short:subprocess.check_output(["git","rev-parse",short],cwd=ROOT/"repo",text=True).strip()
       for short in ("18bf2fb","c6028e9","6926a63","36d127f","027b7a4")}
results=[]
for source,data in (("baseline",a),("audited",b)):
    for label,head in heads.items():
        x=copy.deepcopy(data);x["provenance"]["repository_head"]=head
        results.append({"source":source,"head":label,"altered_fields":["provenance.repository_head"],"sha256":sha(x),"target_match":sha(x)==TARGET})
# The author's platform is explicitly recorded in its immutable comparison log.
author_platform=json.loads((ROOT/"repo/reports/phase1g_h_delta_audit_3_remediation_logs/regression_vs_9ad5425.json").read_text())["new_environment"]["platform"]
for source,data in (("baseline",a),("audited",b)):
    for label,head in heads.items():
        for dirty in (False,True):
            x=copy.deepcopy(data);x["provenance"].update(repository_head=head,platform=author_platform,working_tree_changes_present=dirty)
            results.append({"source":source,"head":label,"dirty":dirty,"author_platform":author_platform,
                 "altered_fields":["provenance.repository_head","provenance.platform","provenance.working_tree_changes_present"],
                 "sha256":sha(x),"target_match":sha(x)==TARGET})
aa=copy.deepcopy(a);bb=copy.deepcopy(b)
aa["provenance"].pop("repository_head");bb["provenance"].pop("repository_head")
out={"target":TARGET,"actual_baseline_hash":sha(a),"actual_audited_hash":sha(b),
     "only_changed_actual_leaf":"provenance.repository_head","identical_with_that_one_leaf_removed":aa==bb,
     "historical_hash_matches":[x for x in results if x["target_match"]],"reconstructions":results,
     "interpretation":"Present executions are committed worktrees with different HEAD values. Historical same-HEAD/working-state artifact equivalence is consistent with numeric equivalence; it must not be generalized to byte identity across committed trees."}
(OUT/"phase1g_b_hash_scope.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({k:v for k,v in out.items() if k!="reconstructions"},indent=2))
