"""Capture fourth-audit commands/environment/artifacts without mutating sources."""
from pathlib import Path
import hashlib,json,os,platform,subprocess,sys
ROOT=Path(os.environ.get("TIMESCAPE_AUDIT4_WORKSPACE", str(Path(__file__).resolve().parents[2]))).resolve()
OUT=ROOT/"audit_work/reproduction"
REPO=ROOT/"repo"
def git(*args,cwd=REPO):return subprocess.check_output(["git",*args],cwd=cwd,text=True).strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
environments={}
probe="import json,sys,platform,numpy,scipy,matplotlib,pytest,pluggy,timescape_fsigma8.global_variance as gv; print(json.dumps({'python':platform.python_version(),'full_python':sys.version,'executable':sys.executable,'platform':platform.platform(),'numpy':numpy.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__,'pytest':pytest.__version__,'pluggy':pluggy.__version__,'module_path':gv.__file__}))"
for py in ("313","311"):
    env=dict(os.environ,OPENBLAS_NUM_THREADS="1",PYTHONPATH=str(REPO/"src"))
    environments[py]=json.loads(subprocess.check_output([str(ROOT/f".venv{py}/bin/python"),"-B","-W","error","-c",probe],cwd=REPO,env=env,text=True))
upstream=REPO/".reference/Linear-Perturbations-in-averaged-cosmological-models"
exec_log=json.loads((REPO/"artifacts/upstream/execution_log.json").read_text())
manifest={"repository_head_at_manifest":git("rev-parse","HEAD"),"tree_at_manifest":git("rev-parse","HEAD^{tree}"),
    "audited_head":"027b7a413fcee0786b861d5903272e4653d227ed", "baseline_head":git("rev-parse","HEAD",cwd=ROOT/"baseline"),
    "environments":environments,"upstream":{"head":git("rev-parse","HEAD",cwd=upstream),"status":git("status","--short",cwd=upstream),
    "notebook_sha256":sha(upstream/"ACPT_Timescape.ipynb")},"notebook_execution":{
       "method":"Fresh Python process with external no-socket adapter; exact notebook cells compiled verbatim, sequential fresh namespace; original notebook and project scripts unchanged.",
       "deviation":"Published nbclient/Jupyter-kernel execution could not start: sandbox denied TCP and IPC ZMQ socket bind. This adapter does not reproduce Jupyter transport or rich display outputs; numeric cells and declared savefig outputs regenerated.",
       "success":exec_log["success"],"code_cells":len(exec_log["cells"]),"warnings":exec_log["warnings"],"figures":exec_log["figures_written"]},
    "regenerated_artifact_hashes":{str(p.relative_to(REPO)):sha(p) for folder in (REPO/"artifacts/upstream",REPO/"artifacts/independent") for p in sorted(folder.glob("*.json"))},
    "executions":{p.stem:json.loads(p.read_text()) for p in sorted(OUT.glob("*_execution.json"))},
    "windows_owner_gate":"NOT_RUN: Linux host, CPython3.14.3/3.11.9 Windows unavailable", "no_source_edits":git("diff","--name-only","--","src","tests","scripts")==""}
(OUT/"reproduction_manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
print(json.dumps({"head":manifest["repository_head_at_manifest"],"python_versions":{k:v["python"] for k,v in environments.items()},"no_source_edits":manifest["no_source_edits"],"regenerated_artifacts":len(manifest["regenerated_artifact_hashes"]),"execution_records":len(manifest["executions"])},indent=2))
