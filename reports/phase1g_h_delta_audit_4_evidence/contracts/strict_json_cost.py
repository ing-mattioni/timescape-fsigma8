from pathlib import Path
import sys,importlib.util,json,timeit
repo,out=map(Path,sys.argv[1:3]);sys.path.insert(0,str(repo/'src'))
s=importlib.util.spec_from_file_location('t',repo/'tests/test_phase1g_h_global_variance.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
r=t.run(t.GM,t.constant(.05),t.radius('c'));export=r.to_json_dict();n=10000
only=min(timeit.repeat(lambda:t.gv._require_strict_json(export,'cost probe'),number=n,repeat=3))/n
whole=min(timeit.repeat(lambda:t.gv._require_strict_json(r.to_json_dict(),'cost probe'),number=n,repeat=3))/n
v={'iterations':n,'method':'minimum of3×10000 repeats; avoids constructor recomputation','check_on_precomputed_export_ms':1000*only,'export_plus_check_ms':1000*whole}
out.write_text(json.dumps(v,indent=1)+'\n');print(json.dumps(v))
