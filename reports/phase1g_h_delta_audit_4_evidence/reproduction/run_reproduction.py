"""Fourth delta audit reproduction driver; writes only ignored artifacts and external evidence."""
from pathlib import Path
import argparse, hashlib, json, os, platform, shutil, subprocess, time

ROOT = Path(os.environ.get("TIMESCAPE_AUDIT4_WORKSPACE", str(Path(__file__).resolve().parents[2]))).resolve()
OUT = ROOT / "audit_work/reproduction"
REPO = ROOT / "repo"
BASE = ROOT / "baseline"
OLD = ROOT / "oldscalar"
OUT.mkdir(parents=True, exist_ok=True)

def run(name, command, cwd=REPO, python="313", strict=True):
    exe = ROOT / f".venv{python}/bin/python"
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", PYTHONPATH=str(cwd / "src"),
               PATH=str(exe.parent) + os.pathsep + os.environ["PATH"])
    full = [str(exe), "-B"] + (["-W", "error"] if strict else []) + command
    start = time.monotonic()
    with (OUT / f"{name}.log").open("w") as log:
        result = subprocess.run(full, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
    record = {"name":name, "command":full, "cwd":str(cwd), "returncode":result.returncode,
              "elapsed_seconds":round(time.monotonic()-start, 3),
              "environment":{"OPENBLAS_NUM_THREADS":"1","PYTHONPATH":env["PYTHONPATH"]}}
    (OUT / f"{name}_execution.json").write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps(record), flush=True)
    if result.returncode:
        print((OUT / f"{name}.log").read_text()[-5000:], flush=True)
        raise SystemExit(result.returncode)
    return record

parser=argparse.ArgumentParser()
parser.add_argument("mode", choices=["regen", "owner", "anchored", "baseline", "main", "secondary", "scalar", "suite313", "suite311", "final313"])
args=parser.parse_args()
if args.mode == "regen":
    for script in ["execute_upstream_notebook", "extract_upstream_oracle", "extract_upstream_perturbation_oracle",
                   "extract_upstream_barotropic_oracle", "validate_growth_pipeline", "validate_barotropic_perturbations"]:
        if script.startswith(("execute_upstream", "extract_upstream")):
            run("regen_local_"+script, [str(OUT/"execute_notebook_local.py"),script], strict=False)
        else:
            run("regen_"+script, [f"scripts/{script}.py"])
elif args.mode == "owner":
    run("regen_phase1g_owner_decisions_numerics", ["scripts/phase1g_owner_decisions_numerics.py"])
elif args.mode == "anchored":
    for link,target in [(BASE/".reference",REPO/".reference"),(BASE/".venv311",ROOT/".venv311")]:
        if not link.exists(): link.symlink_to(target, target_is_directory=True)
    run("regen_validate_anchored_density_growth", ["scripts/validate_anchored_density_growth.py"], cwd=BASE)
    shutil.copy2(BASE/"artifacts/independent/phase1d_d_anchored_density_growth_validation.json",
                 REPO/"artifacts/independent/phase1d_d_anchored_density_growth_validation.json")
elif args.mode in ("baseline", "main", "secondary"):
    cwd = BASE if args.mode=="baseline" else REPO
    py = "311" if args.mode=="secondary" else "313"
    label = f"evidence_{args.mode}_py{py}"
    run(label, ["scripts/phase1g_h_global_variance_closure_numerics.py"] + (["--no-figures"] if py=="311" else []), cwd=cwd, python=py)
    shutil.copy2(cwd/"artifacts/independent/phase1g_h_global_variance_closure.json", OUT/f"{label}.json")
    if py=="313":
        target=OUT/f"figures_{args.mode}"
        if target.exists():shutil.rmtree(target)
        shutil.copytree(cwd/"artifacts/independent/phase1g_h", target)
    if args.mode != "secondary":
        run("phase1g_b_"+args.mode, ["scripts/validate_phase1g_b_lagrangian_sigma.py"], cwd=cwd)
        shutil.copy2(cwd/"artifacts/independent/phase1g_b_lagrangian_sigma.json", OUT/f"phase1g_b_{args.mode}.json")
        for config in sorted((cwd/"scripts/phase1g_h_configs").glob("*.json")):
            run("runner_"+args.mode+"_"+config.stem, ["scripts/phase1g_h_global_variance_case.py", "--config", str(config),
                "--output", str(OUT/f"runner_{args.mode}_{config.stem}.json")], cwd=cwd)
elif args.mode=="scalar":
    script=str(REPO/"reports/phase1g_h_delta_audit_3_evidence/implementation_scalar_probes.py")
    for label,cwd in [("before",OLD),("after",REPO)]:
        run("scalar_"+label, [script,str(cwd),str(OUT/f"scalar_{label}.json")],cwd=cwd)
else:
    py=args.mode.replace("suite","").replace("final","")
    suffix="_final" if args.mode.startswith("final") else ""
    run("full_py"+py+suffix, ["-m", "pytest", "-q", "-p", "no:cacheprovider", "-rs"], python=py)
