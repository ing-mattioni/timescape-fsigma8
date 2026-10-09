"""Independent fourth-audit leaf/byte regression and compact continuity checks."""
from pathlib import Path
import collections, decimal, hashlib, json, os, struct
ROOT=Path(os.environ.get("TIMESCAPE_AUDIT4_WORKSPACE", str(Path(__file__).resolve().parents[2]))).resolve()
OUT=ROOT/"audit_work/reproduction"
REPO=ROOT/"repo"

def read(path):
    def unique(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError(f"duplicate JSON key {key} in {path}")
            result[key]=value
        return result
    return json.loads(Path(path).read_text(),object_pairs_hook=unique)
def flat(value,path=""):
    if isinstance(value,dict):
        for key,item in value.items():yield from flat(item,path+"/"+key)
    elif isinstance(value,list):
        for key,item in enumerate(value):yield from flat(item,path+"/"+str(key))
    else:yield path.lstrip("/"),value
def numeric(value):return isinstance(value,(int,float)) and not isinstance(value,bool)
def bit_equal(a,b):
    if type(a) is not type(b):return False
    return struct.pack("!d",a)==struct.pack("!d",b) if isinstance(a,float) else a==b
OLDKEY="both_walls_conditional_density_covariance_ball"
NEWKEY="both_walls_product_moment_excess_ball"
def comparison(a,b,remap=False):
    def leaves(obj):
        return {(p.replace(OLDKEY,NEWKEY) if remap else p):v for p,v in flat(obj)
                if p.split("/")[0] not in ("environment","figures")}
    aa,bb=leaves(a),leaves(b)
    common=sorted(aa.keys()&bb.keys())
    changed=[{"path":p,"old":aa[p],"new":bb[p],"numeric":numeric(aa[p]) and numeric(bb[p])}
             for p in common if not bit_equal(aa[p],bb[p])]
    return {"common_leaves":len(common),"numeric_common":sum(numeric(aa[p]) and numeric(bb[p]) for p in common),
            "numeric_changed":sum(x["numeric"] for x in changed),"other_changed":sum(not x["numeric"] for x in changed),
            "differences":changed,"only_old":sorted(aa.keys()-bb.keys()),"only_new":sorted(bb.keys()-aa.keys())}
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

old=read(OUT/"evidence_baseline_py313.json")
new=read(OUT/"evidence_main_py313.json")
secondary=read(OUT/"evidence_secondary_py311.json") if (OUT/"evidence_secondary_py311.json").exists() else None
out={"same_interpreter_baseline_vs_audited":comparison(old,new),
     "same_interpreter_after_key_rename":comparison(old,new,True),
     "method":"Own recursive flatten; bool excluded from numeric count; type-sensitive IEEE-754 binary64 equality; environment and figure metadata excluded; figure and validator bytes checked separately."}
of,nf=dict(flat(old)),dict(flat(new))
renamed=[{"old_path":p,"new_path":p.replace(OLDKEY,NEWKEY),"bit_equal":bit_equal(v,nf[p.replace(OLDKEY,NEWKEY)])}
         for p,v in of.items() if OLDKEY in p]
out["renamed_leaves"]={"count":len(renamed),"all_bitwise_equal":all(r["bit_equal"] for r in renamed),"rows":renamed}
if secondary:out["cross_interpreter"]=comparison(new,secondary)
out["gates"]={group:{"count":len(rows),"passed":sum(row["pass"] for row in rows.values())} for group,rows in new["gates"].items()}
out["figures"]=[{"name":p.name,"baseline_sha256":digest(p),"audited_sha256":digest(OUT/"figures_main"/p.name),
                 "byte_identical":p.read_bytes()==(OUT/"figures_main"/p.name).read_bytes()}
                for p in sorted((OUT/"figures_baseline").glob("*.png"))]
out["phase1g_b_validator"]={"baseline_sha256":digest(OUT/"phase1g_b_baseline.json"),"audited_sha256":digest(OUT/"phase1g_b_main.json"),
   "byte_identical":(OUT/"phase1g_b_baseline.json").read_bytes()==(OUT/"phase1g_b_main.json").read_bytes()}
gb_old,gb_new=[read(OUT/f"phase1g_b_{name}.json") for name in ("baseline","main")]
gb_diff=comparison(gb_old,gb_new)
out["phase1g_b_validator"]["full_leaf_comparison"]=gb_diff
gb_old["provenance"].pop("repository_head");gb_new["provenance"].pop("repository_head")
out["phase1g_b_validator"]["identical_except_repository_head"]=gb_old==gb_new
out["runner"]=[]
saved_runners={r["case"]:r["current"] for r in read(REPO/"reports/phase1g_h_delta_audit_3_evidence/runner_comparison.json")}
for p in sorted(OUT.glob("runner_baseline_*.json")):
    if p.name.endswith("_execution.json"):continue
    name=p.name.removeprefix("runner_baseline_").removesuffix(".json")
    now=OUT/("runner_main_"+name+".json")
    if now.exists():
        data=read(now)
        out["runner"].append({"case":name,"byte_identical":p.read_bytes()==now.read_bytes(),"sha256":digest(now),
            "linear_sigma":data["record"]["linear_sigma"],"vs_third_saved":comparison(saved_runners[name],data)})
out["artifact_hashes"]={p.stem:digest(p) for p in sorted(OUT.glob("evidence_*_py*.json")) if not p.name.endswith("_execution.json")}

# Reconcile the current inventory and compare against old auditor's exact saved
# numerical values, using explicit semantic field-name translations only.
rules=[("/a_s_scaling_pbs_tracker_seed/","/a_s_scaling/pbs_tracker_seed_compressed/"),
 ("/refined_quadrature_linear_sigma_c_pbs","/refined_quadrature_linear_sigma"),
 ("/premise_max_linear_rms","/premise/max_linear_rms"),("/premise_radius_Mpc","/premise_radius/radius_Mpc"),
 ("/primary_rms_at_premise","/target_premise_rms"),("/linear_sigma_c_direct","/linear_sigma_direct_A_s"),
 ("/E_reference_reproduction/","/E_reference/"),("/ell_Mpc","/partition_smoothing_ell_Mpc"),
 ("/linear_sigma_post_hoc_normalised","/linear_sigma_planck_anchored"),
 ("/lower_post_hoc_withdrawn","/lower_anchored"),("/upper_post_hoc_withdrawn","/upper_anchored"),
 ("/normalisation_variants/","/pbs_reclosure_under_spectrum_rescaling/"),
 ("/nonnegative_lognormal_pairs/","/gaussian_threshold_pair/nonnegative_lognormal_pair/"),
 ("/signed_gaussian_pair/","/gaussian_threshold_pair/"),("/scale_separation_convention_c/","/scale_separation/")]
def translate(path):
    p="/"+path
    for a,b in rules:p=p.replace(a,b)
    if "/step_share_counterexample/" in p:p=p.replace("/premise_radius/radius_Mpc","/premise_radius_Mpc")
    return p.replace("/nonnegative_lognormal_pair/linear_limit_max_rel_difference","/nonnegative_lognormal_pair/linear_limit/max_wall_moment_rel_difference").replace(
     "/radial_quadrature/h25_identity_max_rel","/gaussian_threshold_pair/h25_identity_max_rel").replace(
     "/radial_quadrature/intervals","/gaussian_threshold_pair/radial_intervals").replace(
     "/radial_quadrature/refinement_max_rel_vs_half","/gaussian_threshold_pair/radial_refinement_max_rel").replace(OLDKEY,NEWKEY).lstrip("/")
mapped={p.replace("cases/","results/",1) if p.startswith("cases/") else p:v for p,v in nf.items()}
inv=read(REPO/"reports/phase1g_h_global_variance_closure_inventory.json")
rows=[];unmatched=[]
for key in ("results","anchoring","two_phase_covariance","ensemble_vs_tangent_example"):
    for p,v in flat(inv[key],key):
        if not numeric(v):continue
        q=translate(p)
        if q not in mapped:unmatched.append(p);continue
        tolerance=max(2e-12,0.5*10**decimal.Decimal(str(v)).as_tuple().exponent)
        actual=mapped[q]
        rows.append({"inventory_path":p,"artifact_path":q,"declared":v,"actual":actual,"absolute_tolerance":tolerance,"pass":abs(actual-v)<=tolerance})
out["current_inventory"]={"matched":len(rows),"unmatched":unmatched,"deviations":[r for r in rows if not r["pass"]]}
oldclaims=read(REPO/"reports/phase1g_h_delta_audit_3_inventory.json")["claims"]
saved=[];missing=[]
for c in oldclaims:
    if c["method"]!="EXPLICIT_SEMANTIC_PATH_MAPPING_HALF_LAST_DIGIT":continue
    p=c["claim"].removeprefix("1G-H inventory rounded scalar ")
    q=translate(p)
    if q not in mapped:missing.append(p);continue
    actual=mapped[q];previous=c["audit_value"]
    saved.append({"old_claim":c["id"],"artifact_path":q,"old_audit_value":previous,"current":actual,
                  "bit_identical":bit_equal(previous,actual),"relative_change":abs(actual-previous)/max(abs(actual),abs(previous)) if actual or previous else 0})
out["vs_third_saved_audit_values"]={"count":len(saved),"exact_equal":sum(r["bit_identical"] for r in saved),
    "changed":[r for r in saved if not r["bit_identical"]],"unmatched":missing}
before,after=[read(OUT/f"scalar_{label}.json") for label in ("before","after")]
by_before={r["id"]:r for r in before["probes"]};by_after={r["id"]:r for r in after["probes"]}
changes=[{"id":k,"before":[a["accepted"],a.get("strict_json")],"after":[by_after[k]["accepted"],by_after[k].get("strict_json")],"record":a["record"]}
         for k,a in by_before.items() if (a["accepted"],a.get("strict_json"))!=(by_after[k]["accepted"],by_after[k].get("strict_json"))]
out["scalar_campaign"]={"probes":len(by_before),"accepted":[before["summary"]["accepted"],after["summary"]["accepted"]],
 "accepted_non_strict_json":[len(x["summary"]["accepted_non_strict_json"]) for x in (before,after)],
 "accepted_nonfinite":[len(x["summary"]["accepted_nonfinite"]) for x in (before,after)],"changed":len(changes),
 "changed_by_record":dict(collections.Counter(r["record"] for r in changes)),
 "new_acceptances":[k for k in by_before if not by_before[k]["accepted"] and by_after[k]["accepted"]]}
(OUT/"regression_comparison.json").write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+"\n")
(OUT/"inventory_numeric_rows.json").write_text(json.dumps(rows,indent=2,sort_keys=True,allow_nan=False)+"\n")
summary={k:v for k,v in out.items() if k not in ("runner","renamed_leaves","vs_third_saved_audit_values")}
for key in ("same_interpreter_baseline_vs_audited","same_interpreter_after_key_rename","cross_interpreter"):
    if key in summary:summary[key]={k:v for k,v in summary[key].items() if k not in ("differences","only_old","only_new")}
summary["renamed_leaves"]={k:v for k,v in out["renamed_leaves"].items() if k!="rows"}
summary["vs_third_saved_audit_values"]={k:v for k,v in out["vs_third_saved_audit_values"].items() if k!="changed"}
summary["runner"]=[{k:v for k,v in r.items() if k!="vs_third_saved"} for r in out["runner"]]
print(json.dumps(summary,indent=2))
