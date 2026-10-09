"""No-socket execution adapter for unchanged project notebook/oracle runners.

Linux sandbox denies both TCP and Unix ZMQ bind before kernel startup. Each
invocation is a fresh Python process. Notebook cells are compiled verbatim and
executed sequentially in one fresh namespace. Streams/errors are written into
the in-memory nbformat copy, preserving output parsing by the original runner.
This is an execution-infrastructure deviation, not ordinary nbclient execution.
No upstream source or project file is modified or copied into this adapter.
"""
from pathlib import Path
import contextlib, io, os, runpy, sys, traceback, warnings
import nbclient
import nbformat
from nbclient.exceptions import CellExecutionError

class NoSocketNotebookClient:
    def __init__(self, nb, **kwargs):
        self.nb=nb
        self.kwargs=kwargs
    def execute(self, **kwargs):
        scope={"__name__":"__main__"}
        workdir=self.kwargs.get("resources",{}).get("metadata",{}).get("path")
        if workdir:os.chdir(workdir)
        for idx,cell in enumerate(self.nb.cells):
            if cell.cell_type!="code":continue
            stdout,stderr=io.StringIO(),io.StringIO()
            cell.outputs=[]
            cell.execution_count=idx+1
            error=None
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                try:exec(compile(cell.source, f"<upstream-cell-{idx}>", "exec"), scope)
                except BaseException as exc:error=exc
            for kind,stream in [("stdout",stdout),("stderr",stderr)]:
                if stream.getvalue():cell.outputs.append(nbformat.v4.new_output("stream",name=kind,text=stream.getvalue()))
            if error is not None:
                cell.outputs.append(nbformat.v4.new_output("error",ename=type(error).__name__,evalue=str(error),traceback=traceback.format_exception(error)))
                raise CellExecutionError.from_cell_and_msg(cell,"socket-free adapter failed")
        return self.nb

nbclient.NotebookClient=NoSocketNotebookClient
ROOT=Path(os.environ.get("TIMESCAPE_AUDIT4_WORKSPACE", str(Path(__file__).resolve().parents[2]))).resolve()
script=ROOT/"repo/scripts"/(sys.argv[1]+".py")
sys.argv=[str(script)]
warnings.simplefilter("default")
runpy.run_path(str(script),run_name="__main__")
