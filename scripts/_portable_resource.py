"""Windows stand-in for the Unix-only ``resource`` module (owner approval 2026-09-30).

The frozen Phase 1G-F script ``scripts/phase1g_f_void_population_numerics.py``
does ``import resource``, which exists only on Unix.  It uses it in one place,
``_progress()``, to print the peak resident set size on stderr; no artifact
value depends on it.  The frozen script is not edited: a runner installs this
stand-in in ``sys.modules`` before loading it by path.

The stand-in provides only what that script calls, ``RUSAGE_SELF`` and
``getrusage(who).ru_maxrss``.  On Windows ``ru_maxrss`` is the process's peak
working set (``K32GetProcessMemoryInfo``, ``PeakWorkingSetSize``) in KiB, the
unit Linux uses for ``ru_maxrss``.  Where the real module exists, nothing is
installed.

Record: reports/phase1g_windows_validation_record.md.
"""

from __future__ import annotations

import sys
import types

RUSAGE_SELF = 0


def _peak_working_set_kib() -> int:
    import ctypes
    from ctypes import wintypes

    class _ProcessMemoryCounters(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    kernel32.K32GetProcessMemoryInfo.argtypes = [wintypes.HANDLE,
                                                 ctypes.POINTER(_ProcessMemoryCounters),
                                                 wintypes.DWORD]
    kernel32.K32GetProcessMemoryInfo.restype = wintypes.BOOL
    counters = _ProcessMemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    if not kernel32.K32GetProcessMemoryInfo(kernel32.GetCurrentProcess(), ctypes.byref(counters),
                                            counters.cb):
        raise OSError(ctypes.get_last_error(), "K32GetProcessMemoryInfo failed")
    return int(counters.PeakWorkingSetSize) // 1024


def getrusage(who: int) -> types.SimpleNamespace:
    """``resource.getrusage`` subset: only ``RUSAGE_SELF`` and ``ru_maxrss`` (KiB)."""
    if who != RUSAGE_SELF:
        raise ValueError("the stand-in supports RUSAGE_SELF only")
    return types.SimpleNamespace(ru_maxrss=_peak_working_set_kib())


def install() -> str:
    """Make ``import resource`` work; return which module is in use."""
    try:
        import resource  # noqa: F401  (Unix: the real module, nothing to do)
        return "resource (stdlib)"
    except ModuleNotFoundError:
        pass
    if sys.platform != "win32":
        raise ModuleNotFoundError("no 'resource' module and no stand-in for " + sys.platform)
    stand_in = types.ModuleType("resource")
    stand_in.RUSAGE_SELF = RUSAGE_SELF
    stand_in.getrusage = getrusage
    stand_in.__doc__ = "Windows stand-in installed by scripts/_portable_resource.py"
    sys.modules["resource"] = stand_in
    return "scripts/_portable_resource.py (Windows stand-in)"
