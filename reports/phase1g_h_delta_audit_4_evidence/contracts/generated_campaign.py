"""Second delta audit of Phase 1G-H: mutation campaign in disposable copies.

    OPENBLAS_NUM_THREADS=1 python -B mutation_campaign.py REPO PYTHON WORKDIR OUT.json

REPO is the audited tree (read only), WORKDIR a scratch directory outside it.
Each mutant is one exact string replacement in a fresh copy of src/, scripts/,
tests/test_phase1g_h_global_variance.py and tests/conftest.py (reports/ is a
read-only symlink).  The 42-case phase test file runs with ``-W error``;
script mutants, and source mutants that survive the tests, also run the
evidence script (``--no-figures``) so that its gates are reported.
Mutants: the delta audit's 23 (M1-M8 from the first audit, N1-N14 and N9b;
M7 and N13 adapted as recorded in
reports/phase1g_h_delta_audit_remediation_logs/delta_audit_mutants_adaptations.json),
the author's 10 (own_mutants_definitions.json) and this audit's own (A*).
"""
from __future__ import annotations

import concurrent.futures as cf
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO, PY, WORK, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
SRC = "src/timescape_fsigma8/global_variance.py"
SCR = "scripts/phase1g_h_global_variance_closure_numerics.py"
BASE = WORK / "base"
if BASE.exists():
    shutil.rmtree(BASE)
(BASE / "tests").mkdir(parents=True)
for name in ("src", "scripts"):
    shutil.copytree(REPO / name, BASE / name, ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"))
for name in ("test_phase1g_h_global_variance.py", "conftest.py"):
    shutil.copy2(REPO / "tests" / name, BASE / "tests" / name)
shutil.copy2(REPO / "pyproject.toml", BASE / "pyproject.toml")
(BASE / "reports").symlink_to(REPO / "reports", target_is_directory=True)

first = json.loads((REPO / "reports/phase1g_h_independent_audit_evidence/mutation_results.json").read_text())
adapt = {m["id"]: m for m in json.loads(
    (REPO / "reports/phase1g_h_delta_audit_remediation_logs/delta_audit_mutants_adaptations.json").read_text())}
mutants = []
for m in first:
    if m["id"] == "baseline":
        continue
    a, b = m["old"], m["new"]
    if m["id"] in adapt:
        a, b = adapt[m["id"]]["old"], adapt[m["id"]]["new"]
    mutants.append(("delta", m["id"], SRC, a, b))
delta_new = [
    ("N1_growth_record_validation_off", SRC, "if self.fv0 != self.background.fv0:", "if False:"),
    ("N2_void_share_record_validation_off", SRC, "if p0 != self.closure.share:", "if False:"),
    ("N3_sigma_record_validation_off", SRC,
     "if self.effective_propagator != self.linear_sigma / self.unit_growth_sigma:", "if False:"),
    ("N4_interval_record_validation_off", SRC,
     "if self.target_inside != (self.premise_compatible\n                                  and self.lower <= self.target_value <= self.upper):",
     "if False:"),
    ("N5_orthant_centre_split_off", SRC, "for b in (u_star - 8.0 * width, u_star, u_star + 8.0 * width):",
     "for b in (u_star - 8.0 * width, u_star + 8.0 * width):"),
    ("N6_orthant_transition_edges_off", SRC, "for b in (u_star - 8.0 * width, u_star, u_star + 8.0 * width):",
     "for b in (u_star,):"),
    ("N7_orthant_refinement_off", SRC, "previous = evaluate(n)\n    while True:",
     "previous = evaluate(n)\n    return previous, n, 0.0\n    while True:"),
    ("N8_frechet_gate_off", SRC, "if not lower - tol <= p11 <= upper + tol:", "if False:"),
    ("N9_void_share_identity_text_sign_reversed", SRC, "``p = f_v,LS - d f_v,L/d delta_L``",
     "``p = f_v,LS + d f_v,L/d delta_L``"),
    ("N9b_pbs_executable_response_sign_reversed", SRC, "threshold = phi_nu / sigma_s", "threshold = -phi_nu / sigma_s"),
    ("N10_reclosure_factor_unsquared", SCR, "spec_re = early_spectrum(2.100e-9 * anchor_factor ** 2)",
     "spec_re = early_spectrum(2.100e-9 * anchor_factor)"),
    ("N11_lognormal_wall_normalization_off", SCR, "q0 = float(ndtr(-(c - kappa0)))", "q0 = f_w"),
    ("N12_lognormal_lambda_not_squared", SCR, "math.exp(lam * lam * xi_lat_r)", "math.exp(lam * xi_lat_r)"),
    ("N13_rounding_output_half_unit_off", SCR, adapt["N13_rounding_output_half_unit_off"]["old"],
     adapt["N13_rounding_output_half_unit_off"]["new"]),
    ("N14_step_cutoff_shifted", SCR, "k_cut = math.exp(log_k)", "k_cut = math.exp(log_k) * 0.9"),
]
mutants += [("delta",) + m for m in delta_new]
for m in json.loads((REPO / "reports/phase1g_h_delta_audit_remediation_logs/own_mutants_definitions.json").read_text()):
    mutants.append(("author", "AUTH_" + m["id"], m["file"], m["old"], m["new"]))

OFF = "(lambda *_a, **_k: None)(self, lambda: "
own = [
    ("A01_same_tolerance_widened", SRC, 'and _close(stored, expected))',
     'and math.isclose(stored, expected, rel_tol=1e-3))'),
    ("A02_same_bool_type_check_off", SRC, "return type(stored) is type(expected) and stored == expected",
     "return stored == expected"),
    ("A03_same_tuple_elements_unchecked", SRC, "and all(_same(a, b) for a, b in zip(stored, expected)))",
     "and True)"),
    ("A04_interval_convention_check_off", SRC,
     "    if premise.radius.convention is not target.radius.spec.convention:\n        raise",
     "    if False:\n        raise"),
    ("A05_growth_assumptions_check_off", SRC,
     'if _strings(self.assumptions, "assumptions") != _GROWTH_ASSUMPTIONS:', "if False:"),
    ("A06_sigma_caveats_check_off", SRC, 'if _strings(self.caveats, "caveats") != _GLOBAL_CAVEATS:', "if False:"),
    ("A07_interval_assumptions_check_off", SRC,
     'if _strings(self.class_assumptions, "class_assumptions") != _INTERVAL_ASSUMPTIONS:', "if False:"),
    ("A08_numerical_error_not_converted", SRC, "except GlobalVarianceNumericalError as exc:",
     "except ZeroDivisionError as exc:"),
    ("A09_void_share_background_identity_off", SRC,
     "if self.density.background is not self.growth.background:", "if False:"),
    ("A10_growth_binding_off", SRC, "_bind_recomputed(self, lambda: _two_phase_growth_values(",
     OFF + "_two_phase_growth_values("),
    ("A11_void_share_binding_off", SRC, "_bind_recomputed(self, lambda: _void_share_values(",
     OFF + "_void_share_values("),
    ("A12_sigma_binding_off", SRC, "_bind_recomputed(self, lambda: _global_sigma_values(",
     OFF + "_global_sigma_values("),
    ("A13_interval_binding_off", SRC, "_bind_recomputed(self, lambda: _interval_values(self.target, self.premise),",
     OFF + "_interval_values(self.target, self.premise),"),
    ("A14_record_identity_rtol_5pct", SRC, "RECORD_IDENTITY_RTOL = 1e-12", "RECORD_IDENTITY_RTOL = 5e-2"),
    ("A15_ball_coarse_equals_fine", SCR, "return float(simpson(y[::2], x=self.u_full[::2]))",
     "return float(simpson(y, x=self.u_full))"),
    ("A16_ball_coarse_stride_3", SCR, "return float(simpson(y[::2], x=self.u_full[::2]))",
     "return float(simpson(y[::3], x=self.u_full[::3]))"),
    ("A17_h25_sum_cross_once", SCR, "math.sqrt(ball.integral(c_chi + k_ww + 2.0 * k_pw) / f_w ** 2)",
     "math.sqrt(ball.integral(c_chi + k_ww + k_pw) / f_w ** 2)"),
    ("A18_cw_unweighted_average", SCR, "ball.integral(k_ww + 2.0 * k_pw) / ball.integral(p11),",
     "ball.integral(k_ww + 2.0 * k_pw) / ball.integral(np.ones_like(p11)),"),
    ("A19_lambda_calibration_off_by_1pct", SCR, "carrier_ball(l2) - ball_target",
     "carrier_ball(l2) - 1.01 * ball_target"),
    ("A20_covariance_ratio_not_squared", SCR, "1.0 / m_ii ** 2", "1.0 / m_ii"),
    ("A21_lognormal_cross_kernel_normaliser_off", SCR,
     "e_p = f_w * _orthant_p(rho, c - kappa_r, c - kappa0) / q0",
     "e_p = f_w * _orthant_p(rho, c - kappa_r, c - kappa0) / f_w"),
    ("A22_h25_gate_disabled", SCR, '"h25_identity_rel": 1e-12', '"h25_identity_rel": 1.0'),
    ("A23_radial_gate_disabled", SCR, '"radial_refinement_rel": 1e-5', '"radial_refinement_rel": 1.0'),
]
mutants += [("own",) + m for m in own]
own_r3 = [
    ('R01_same_accepts_any_real', SRC, '    if isinstance(expected, float):\n        return (isinstance(stored, float) and math.isfinite(stored)', '    if isinstance(expected, float):\n        return (isinstance(stored, Real) and math.isfinite(float(stored))'),
    ('R02_float_type_message_off', SRC, '        if isinstance(expected, float) and not isinstance(stored, float):', '        if False:'),
    ('R03_G_not_stored_as_float', SRC, '        object.__setattr__(self, "G", G)\n', ''),
    ('R04_checks_not_stored_as_float', SRC, '            object.__setattr__(self, name, _positive(getattr(self, name), name))', '            _positive(getattr(self, name), name)'),
]
mutants += [("round3",) + m for m in own_r3]


def summary_line(text):
    return next((ln for ln in reversed(text.splitlines()) if re.search(r"\b(passed|failed|error)\b", ln)), "")


def run(case):
    origin, ident, path, a, b = case
    dest = WORK / "m" / ident
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(BASE, dest, symlinks=True)
    row = {"origin": origin, "id": ident, "file": path, "old": a, "new": b}
    if path:
        text = (dest / path).read_text()
        row["replacements"] = text.count(a)
        if not row["replacements"]:
            row["outcome"] = "NOT_APPLIED"
            return row
        (dest / path).write_text(text.replace(a, b))
        row["mutated_sha256"] = hashlib.sha256((dest / path).read_bytes()).hexdigest()
    env = dict(os.environ, PYTHONPATH=str(dest / "src"), PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
    t = subprocess.run([PY, "-B", "-W", "error", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=line",
                        "tests/test_phase1g_h_global_variance.py"], cwd=dest, env=env, text=True,
                       capture_output=True)
    row["tests_rc"] = t.returncode
    row["tests_summary"] = summary_line(t.stdout)
    row["failed_tests"] = re.findall(r"^FAILED (\S+)", t.stdout, re.M)
    run_ev = path == SCR or (path and t.returncode == 0)
    if run_ev or not path:
        e = subprocess.run([PY, "-B", "-W", "error", SCR, "--no-figures"], cwd=dest, env=env, text=True,
                           capture_output=True)
        row["evidence_rc"] = e.returncode
        row["evidence_failures"] = [ln.strip() for ln in e.stdout.splitlines() if "FAIL" in ln][:8]
        row["evidence_tail"] = (e.stdout + e.stderr).strip().splitlines()[-2:]
    killed_t = t.returncode != 0
    killed_e = row.get("evidence_rc", 0) != 0
    if not path:
        row["outcome"] = "BASELINE_PASS" if not (killed_t or killed_e) else "BASELINE_FAIL"
    else:
        row["outcome"] = ("KILLED_BY_TESTS" if killed_t else
                          "KILLED_BY_EVIDENCE_ONLY" if killed_e else "SURVIVED")
    shutil.rmtree(dest, ignore_errors=True)
    return row


cases = [("baseline", "baseline", None, "", "")] + mutants
results = []
with cf.ThreadPoolExecutor(max_workers=int(os.environ.get("WORKERS", "3"))) as pool:
    for row in pool.map(run, cases):
        results.append(row)
        print(json.dumps({k: row.get(k) for k in ("id", "outcome", "tests_summary", "evidence_rc")}), flush=True)
OUT.write_text(json.dumps(results, indent=1) + "\n")
counts = {}
for r in results:
    counts.setdefault(r["origin"], {}).setdefault(r["outcome"], 0)
    counts[r["origin"]][r["outcome"]] += 1
print(json.dumps(counts, indent=1))
