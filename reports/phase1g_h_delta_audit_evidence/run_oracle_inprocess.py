"""Environment adapter: execute unmodified oracle-extraction cells in-process.

Jupyter interface discovery fails with EPERM in this container. This replaces
only the NotebookClient transport/execution layer, never notebook cell source,
scientific constants, warnings, solver choices, or extraction provenance.
The notebook content remains outside published material.
"""
import contextlib,io,runpy,sys
import nbformat
from nbclient import NotebookClient

def execute(self, **kwargs):
    namespace={'__name__':'__main__'}
    for index,cell in enumerate(self.nb.cells):
        if cell.cell_type != 'code': continue
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(compile(cell.source,f'<unmodified-oracle-cell-{index}>','exec'),namespace)
        cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=output.getvalue())]
        cell.execution_count=index+1
    return self.nb
NotebookClient.execute=execute
runpy.run_path(sys.argv[1],run_name='__main__')
