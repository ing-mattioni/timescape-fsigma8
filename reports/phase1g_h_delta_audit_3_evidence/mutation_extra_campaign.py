"""Third delta audit: own mutants and faithfully adapted author D1.

Run with the same arguments as the previous auditor's mutation_campaign.py:
python -B -W error THIS_FILE REPO PYTHON WORKDIR OUT.json
All executable mutants live in WORKDIR, outside the audited repository.
The previous campaign's disposable-copy runner and gate logic are retained;
its mutation list is replaced with this independently specified set.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

repo = Path(sys.argv[1])
source = (repo / "reports/phase1g_h_delta_audit_2_evidence/mutation_campaign.py").read_text()
tree = ast.parse(source)
# Extract the imports/setup through construction of BASE, and the runner
# functions below the prior mutation definitions, without executing its list.
start = source.index("first = json.loads(")
runner = source.index("def summary_line(text):")
end = source.index("cases = [(\"baseline\",", runner)
prefix, functions = source[:start], source[runner:end]
SRC = "src/timescape_fsigma8/global_variance.py"
SCR = "scripts/phase1g_h_global_variance_closure_numerics.py"
TST = "tests/test_phase1g_h_global_variance.py"
own = [
    ("AUTH_D1_binding_off_adapted", SRC,
     "    for name, expected in values.items():\n        stored = getattr(record, name)",
     "    for name, expected in ():\n        stored = getattr(record, name)"),
    ("B01_record_identity_rtol_10pct_drift", SRC,
     "RECORD_IDENTITY_RTOL = 1e-12", "RECORD_IDENTITY_RTOL = 1.1e-12"),
    ("B02_same_rejects_float_subclasses", SRC,
     "isinstance(stored, float) and math.isfinite(stored)",
     "type(stored) is float and math.isfinite(stored)"),
    # One logical mutant in two string substitutions, preserving the existing
    # rejection of Fraction and Decimal while broadening to NumPy float32.
    ("B03_same_accepts_numpy_float32", SRC,
     "isinstance(stored, float)", "isinstance(stored, (float, np.floating))"),
    ("B04_monte_carlo_budget_doubled", TST,
     "<= 5 *", "<= 10 *"),
    ("B05_simpson_error_ratio_budget_x10", TST,
     "pytest.approx(16.0, rel=1e-2, abs=0.0)",
     "pytest.approx(16.0, rel=1e-1, abs=0.0)"),
    ("B06_lognormal_calibration_inside_budget", SCR,
     "carrier_ball(l2) - ball_target", "carrier_ball(l2) - (1.0 + 1e-10) * ball_target"),
    ("B07_p11_weight_denominator_1ppm", SCR,
     "ball.integral(k_ww + 2.0 * k_pw) / ball.integral(p11),",
     "ball.integral(k_ww + 2.0 * k_pw) / (1.000001 * ball.integral(p11)),"),
    ("B08_lognormal_calibration_1ppm", SCR,
     "carrier_ball(l2) - ball_target", "carrier_ball(l2) - 1.000001 * ball_target"),
    ("B09_reported_lambda_1ppm", SCR,
     '"latent_scale_lambda": math.sqrt(lam2),',
     '"latent_scale_lambda": 1.000001 * math.sqrt(lam2),'),
    ("B10_one_growth_tolerance_not_converted", SRC,
     'object.__setattr__(self, name, _positive(getattr(self, name), name))',
     'object.__setattr__(self, name, _positive(getattr(self, name), name)) if name != "ode_atol" else _positive(getattr(self, name), name)'),
]
mutants = [("extra",) + row for row in own]
namespace = {"__name__": "__main__", "__file__": __file__}
exec(compile(prefix, __file__, "exec"), namespace)
namespace["mutants"] = mutants
exec(compile(functions + source[end:], __file__, "exec"), namespace)
