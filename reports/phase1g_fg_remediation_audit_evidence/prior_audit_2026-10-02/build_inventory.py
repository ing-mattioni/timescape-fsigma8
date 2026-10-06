"""Build the audit inventory (LF bytes, UTF-8) from the auditor's evidence outputs."""
import hashlib
import json
from pathlib import Path

S = Path(__file__).resolve().parent
R = Path("C:/Projects/timescape-fsigma8")
OUT = R / "reports" / "phase1g_fg_independent_scientific_audit_inventory.json"
assert not OUT.exists(), "refusing to overwrite"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(name):
    return json.loads((S / name).read_bytes())


ind_f, ind_v, ind_g, ind_s, arch = (load(n) for n in (
    "indep_f_out.json", "indep_var_out.json", "indep_g_out.json", "indep_supersede_out.json", "check_archive_out.json"))
inv_f = json.loads((R / "reports/phase1g_f_volume_budget_successor_inventory.json").read_bytes())

audited = ["CLAUDE.md", "README.md", "reports/phase1g_f_volume_budget_successor.md",
           "reports/phase1g_f_volume_budget_successor_inventory.json", "reports/phase1g_fg_successor_validation.md",
           "reports/phase1g_g_void_evolution.md", "reports/phase1g_g_void_evolution_inventory.json",
           "scripts/phase1g_f_volume_budget_successor_numerics.py", "scripts/phase1g_g_void_evolution_numerics.py",
           "tests/test_phase1g_f_volume_budget_successor.py", "tests/test_phase1g_g_void_evolution.py"]

comparison = {}
for case in ("PAPER_REFERENCE", "NW15_CMB_FIT"):
    a, b = inv_f["primary_cases"][case][0], ind_f["cases"][case]["history"][0]
    comparison[case] = {
        k: {"audited": a["fixed_domain_cumulative"][k], "independent": b["F2"][k],
            "rel": (a["fixed_domain_cumulative"][k] - b["F2"][k]) / b["F2"][k]}
        for k in ("r>=1", "r>=2", "r>=5", "r>=10", "r>=15")}
    for ka, kb in (("median_radius_h_inv_Mpc", "median_h_inv_Mpc"), ("cutoff_fixed_domain_h_inv_Mpc", "cutoff_F2"),
                   ("cutoff_truncated_universe_h_inv_Mpc", "cutoff_F3")):
        comparison[case][ka] = {"audited": a[ka], "independent": b[kb], "rel": (a[ka] - b[kb]) / b[kb]}

findings = [
    dict(id="FGA-F1", severity="MEDIUM", cls="OMISSION", blocking="INTEGRATION",
         where=["reports/phase1g_f_volume_budget_successor.md Secs. 2-5 (no mapping table)",
                "reports/phase1g_f_void_population.md Sec. 1 items 2, 4-6; Sec. 5 Milne limit; Sec. 8.2; Sec. 9; Sec. 12 item 1; Reading; Sec. 13"],
         claim="Successor is the current reading but leaves frozen F3-based numbers and frozen verdict 2 unmapped.",
         evidence="near-empty r_min 0.06-0.8 -> 0.019-0.39 h^-1 Mpc (F2); z=3 r>=1 0.013 -> 0.0052; token wording 0.5-2 -> 0.35-1.23; verdict 2 (DERIVED_FROM_VERIFIED_DEFINITIONS) contradicted by successor Sec. 4 without supersession.",
         impact="Superseded values read as current; a frozen verdict's status changes silently.",
         correction="Add frozen-text -> current-reading table; recompute F2 r_min for archived C1 near-empty (or flag all frozen r_min as F3/truncated-universe); state current label of frozen verdict 2.",
         owner_decision="Confirm the new label for frozen verdict 2."),
    dict(id="FGA-F2", severity="MEDIUM", cls="OMISSION", blocking="FREEZE",
         where=["reports/phase1g_f_volume_budget_successor.md l. 116-141", "CLAUDE.md l. 388-392", "README.md l. 66-69"],
         claim="Hybrid-ingredient list of sigma~0.99 omits that the Boolean void phase is not the F population.",
         evidence="-ln(1-f_v0)=1.3356/0.9862 = 1.78x/1.31x the excursion-set void volume 0.75197; mean grain multiplicity 1.81/1.57 at covered points; F1-F3 assume disjoint volumes.",
         impact="sigma~0.99 (reproduced) is the variance of an overlapping surrogate sharing only the grain-size shape.",
         correction="Add as fifth hybrid ingredient; reword 'empty Boolean voids' accordingly.", owner_decision="none"),
    dict(id="FGA-F3", severity="LOW", cls="ERROR", blocking="FREEZE",
         where=["reports/phase1g_f_volume_budget_successor.md l. 69-79", "scripts/phase1g_f_volume_budget_successor_numerics.py l. 199"],
         claim="'Interpret ... at about three significant figures.'",
         evidence="481-node trapezoid + log-linear interpolation bias: r>=10 +0.22-0.23%, r>=15 +0.70-0.75% vs closed-form absorption probability.",
         impact="Headline 1.48%/1.92% and cutoffs unaffected at 3 s.f.; r>=15 entries wrong in third digit.",
         correction="Quantify discretisation error; quote r>=15 to 2 s.f. or use closed-form cumulative.", owner_decision="none"),
    dict(id="FGA-F4", severity="LOW", cls="OMISSION", blocking="FREEZE",
         where=["reports/phase1g_f_volume_budget_successor.md l. 51-56"],
         claim="Wall identification of x flagged as inherited, conditions not listed.",
         evidence="Conditions: C1+A5; walls = unperturbed flat EdS; isolated uncompensated tophats (strained at f_v~0.75); Lagrangian mean = early wall density; delta_c-crossing mass at rho_w.",
         impact="Scope of F1-F3 numbers under-specified.", correction="List the five conditions.", owner_decision="none"),
    dict(id="FGA-F5", severity="INFO", cls="OPTIONAL", blocking="NONE",
         where=["successor Sec. 3", "tests/test_phase1g_f_volume_budget_successor.py l. 84-86", "README.md l. 66"],
         claim="Fixed-cutoff failure not quantified by epoch.",
         evidence="GM fixed z=0 cutoff: +1.5% at z=0.5, -11% at z=1; NW15 -23% at z=0.5; GM cutoff sequence non-monotone.",
         impact="none on conclusion", correction="State epoch range; qualify README sentence.", owner_decision="none"),
    dict(id="FGA-F6", severity="INFO", cls="OPTIONAL", blocking="NONE",
         where=["artifacts/independent/phase1g_f_void_population.json (12 populations)"],
         claim="Negative unresolved_below_grid values.", evidence="min -1.72e-7 (trapezoid overshoot)",
         impact="none on F2", correction="Mention in successor.", owner_decision="none"),
    dict(id="FGA-G1", severity="LOW", cls="OMISSION", blocking="FREEZE",
         where=["reports/phase1g_g_void_evolution.md Sec. 1 item 2, Sec. 4 (l. 107-127)", "CLAUDE.md l. 399-401"],
         claim="Reference population of the 2/3 rate not made explicit.",
         evidence="Aged homogeneous interiors have H_v t in (8/9,1) -> J_req/tracker rate = 3(1-H_v t) in (0,1/3]; F all-size history has fdot=0 (t J/V_D = -0.124 rel. to shell-crossing interiors).",
         impact="2/3 could be misread as the F population's evolution.", correction="Two sentences in Sec. 4.", owner_decision="none"),
    dict(id="FGA-G2", severity="LOW", cls="OMISSION", blocking="FREEZE",
         where=["reports/phase1g_g_void_evolution.md l. 54-62", "G inventory 'assumptions'"],
         claim="G1 called 'an additional model assumption' without [L03]'s stated hypotheses.",
         evidence="[L03] below (2.2): no spatial correlations, averaged morphology; voids at f_v~0.6-0.75 are space-filling.",
         impact="Applicability of mean-field kinetics under-stated.", correction="Transcribe hypotheses.", owner_decision="none"),
    dict(id="FGA-G3", severity="LOW", cls="ERROR", blocking="FREEZE",
         where=["reports/phase1g_g_void_evolution.md l. 15-17", "CLAUDE.md l. 397-398"],
         claim="Mergers 'cannot independently fix a wrong total-volume history when the regional expansion laws are prescribed'.",
         evidence="True only for a common g_v; with prescribed size/age-dependent rates mergers change the volume-weighted H_v.",
         impact="Over-general headline.", correction="'at a prescribed common regional rate'.", owner_decision="none"),
    dict(id="FGA-G4", severity="INFO", cls="OPTIONAL", blocking="NONE",
         where=["reports/phase1g_g_void_evolution.md l. 274-276"],
         claim="Closing classification omits G12.", evidence="G12 is a standard definition.",
         impact="none", correction="Classify G12; optionally add radius-measure numbers (u=100: 4.66 / 4.17 / 5.53).", owner_decision="none"),
    dict(id="FGA-T1", severity="LOW", cls="OPTIONAL", blocking="NONE",
         where=["tests/test_phase1g_f_volume_budget_successor.py l. 75-79", "tests/test_phase1g_g_void_evolution.py l. 92"],
         claim="Self-referential checks.", evidence="r>=10 regression at rel 2e-7 pins a value with +0.23% bias; H_v t = 8/9 is the brentq target.",
         impact="Regression guards, not validation.", correction="Add closed-form cumulative test and Lagrangian-shell (A8) test.", owner_decision="none"),
    dict(id="FGA-D1", severity="MEDIUM", cls="GOVERNANCE", blocking="INTEGRATION",
         where=["CLAUDE.md l. 346-352", "README.md l. 50-53", "reports/phase1g_f_volume_budget_successor.md l. 152-157",
                "src/timescape_fsigma8/scientific_status.py l. 84-95 (unchanged)", "reports/phase1g_d_owner_decisions_successor.md l. 47, 141, 251 (unchanged)"],
         claim="Documented reading of owner-approved LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC = NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY weakened without a dated owner decision.",
         evidence="D successor rests the token on seed-independent 'R8 < R_void'; F median 2.4-2.8 < 8 h^-1 Mpc and sigma_part^2 = 0.107/0.092 << f_v/f_w, so the premise fails (auditor agrees scientifically); remaining support A_v sigma_LSS(R8)=1.05-1.11.",
         impact="CLAUDE.md/README vs token comment vs D successor inconsistent.",
         correction="Owner decision: (a) keep value, re-justify comment via PBS amplitude in a dated D successor; (b) reclassify via registered successor; (c) revert wording pending decision.",
         owner_decision="required"),
    dict(id="FGA-D2", severity="LOW", cls="GOVERNANCE", blocking="FREEZE",
         where=["successor l. 4-5", "G report l. 4", "both inventories 'authorization'", "validation record 'Scope'"],
         claim="Authorisation for a scientific reinterpretation paraphrased; covered items not enumerated.",
         evidence="Project practice quotes owner ticks verbatim.", impact="Provenance gap.",
         correction="Quote verbatim with date; list covered items.", owner_decision="provide verbatim text"),
    dict(id="FGA-D3", severity="LOW", cls="REPRODUCIBILITY", blocking="FREEZE",
         where=["scripts/phase1g_f_volume_budget_successor_numerics.py l. 212", "scripts/phase1g_g_void_evolution_numerics.py l. 161", "inventories 'evidence_sha256'"],
         claim="Recorded evidence hashes not reproducible cross-platform.",
         evidence="CRLF text-mode writes on Windows (2370/138 CR bytes); F environment block; G last-ulp differences <=1.2e-15; Windows reruns deterministic but != recorded hashes.",
         impact="Hash-based provenance cannot be re-verified on the primary machine.",
         correction="LF byte writes; hash canonical content without 'environment' or record numerical-equivalence tolerance.", owner_decision="none"),
    dict(id="FGA-D4", severity="LOW", cls="OPTIONAL", blocking="NONE",
         where=["successor Sec. 6", "G report Sec. 8"], claim="POSIX-only reproduction commands.",
         evidence="Scripts run unchanged on Windows (verified).", impact="minor", correction="Add .venv\\Scripts\\python forms.", owner_decision="none"),
    dict(id="FGA-D5", severity="LOW", cls="ERROR", blocking="FREEZE",
         where=["scripts/phase1g_f_volume_budget_successor_numerics.py l. 36-37", "scripts/phase1g_g_void_evolution_numerics.py l. 59"],
         claim="'Eq. F1 derives from [JLH13] (13) and V = M/rho'.",
         evidence="[JLH13] (13) gives only the additive definition relative to the background volume; Z = 1-m+m/x is a project deduction ([JLH13] number-conserving case gives m/x, Eq. (14)).",
         impact="Attribution overreach (AGENTS.md rule 2 context).", correction="Reword docstrings as successor Sec. 1.", owner_decision="none"),
    dict(id="FGA-D6", severity="INFO", cls="OPTIONAL", blocking="NONE",
         where=["reports/phase1g_fg_successor_validation.md", "CLAUDE.md l. 12, 142-145"],
         claim="Validation-record limitations superseded; suite counts stale; AGENTS rule-7 summary now equals AGENTS.md.",
         evidence="1125/0/0 on both interpreters in the real checkout.", impact="none",
         correction="Update counts and record in the integration commit.", owner_decision="awareness"),
    dict(id="FGA-D7", severity="INFO", cls="OPTIONAL", blocking="NONE",
         where=["src/timescape_fsigma8/scientific_status.py (TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC comment)", "reports/phase1g_f_void_population.md / frozen script ([SvdW04] (A15))"],
         claim="Pre-existing: token E2 says 'one radius' while GE-OD2 reference is polydisperse; frozen F cites (A15) for g(Theta).",
         evidence="Equation reconstruction gives g at (A17), H_s at (A18) with the counting that reproduces (A21)-(A33).",
         impact="none on audited changes", correction="Owner may address in a later record.", owner_decision="optional"),
]

inventory = {
    "phase": "1G-F successor / 1G-G independent audit",
    "date": "2026-10-02",
    "classification": "REPORT_ONLY_INDEPENDENT_AUDIT",
    "auditor": "Claude Code (Claude Opus 5.5), at the project owner's request; not an author of the audited deliverables",
    "report": "reports/phase1g_fg_independent_scientific_audit.md",
    "repository": {"branch": "phase-1g-f-successor-g-evolution", "head": "fb5d95245bc0cb19ce6cd1438177f1a597bb232f",
                   "declared_base_matches": True, "remote_main": "fb5d95245bc0cb19ce6cd1438177f1a597bb232f",
                   "tracked_files": 259, "modified_tracked": ["CLAUDE.md", "README.md"], "diffstat": "85 insertions, 35 deletions",
                   "untracked_audited": audited[2:], "stash": "none"},
    "audited_files_sha256": {p: sha(R / p) for p in audited},
    "audited_files_unchanged_at_end": True,
    "frozen_dependencies_match_inventories": True,
    "artifacts": {
        "frozen_F": {"sha256": arch["frozen_sha256"], "environment": "Linux CPython 3.12.14 (snapshot run)", "equals_successor_recorded_input": True},
        "successor_F_preexisting": {"sha256": "2f8931a5bcfb4d96986de6fc18e2d2a60c3559c5e1e2601f318d462cd571cd20",
                                    "generated": "2026-10-02 15:40 local, Windows CPython 3.14.3, before this audit", "line_endings": "CRLF"},
        "G_preexisting": "absent",
        "protection": "366 files under artifacts/ checksummed before and after all runs: identical; script reruns only in an isolated copy"},
    "environments": {"py314": {"python": "3.14.3", "numpy": "2.5.2", "scipy": "1.18.1", "pytest": "9.1.1"},
                     "py311": {"python": "3.11.9", "numpy": "2.4.6", "scipy": "1.17.1", "pytest": "9.1.1"},
                     "platform": "Windows 11", "OPENBLAS_NUM_THREADS": 1,
                     "dependencies_changed": False, "cas": "none available; exact fractions.Fraction used"},
    "sources": [
        {"id": "JLH13", "arxiv": "1304.6087", "file": "voids_mnras.tex", "sha256": "cf6fc77a31b395138ac3a027d008698556534e81cfb27c39853d3a99c7b07c4e",
         "verified": ["(2) sigma^2 def", "(6)-(7)", "(12)", "(13) additive cumulative", "(14) F(0)", "(15)-(17) Vdn", "(A4)-(A5)", "(A8) 8/9", "(A9) 0.2047", "(A11)", "(A12) -2.717"]},
        {"id": "SvdW04", "arxiv": "astro-ph/0311260", "file": "voids.tex", "sha256": "e66ad192ee91a83ba88b4068cce5f6b505eb4277a6365d961a60ca10cc1c84b5",
         "verified": ["(1)", "(2)", "(3)", "(7)", "(A21)-(A22)", "(A26)-(A27)", "(A29)-(A31)", "(A33)", "(C1)-(C2)", "(C7)", "(C8)"],
         "note": "frozen 1G-F cites (A15) for g(Theta); reconstruction gives (A17), H_s (A18)"},
        {"id": "L03", "arxiv": "cond-mat/0305670", "files": {"physrep1.tex": "50ed4dcf9cbd0142ef409d4a51eeaf2460bc21d940029ae2d04495a5874e5ffc",
                                                              "physrep3.tex": "99ee85995fa1fce8d2c77b562116e979ebe333c848771425de4a44dc1be2cbc0"},
         "verified": ["(2.2) mean-field; hypotheses below it: no spatial correlations, averaged morphology", "(4.4) K=1", "(4.10) c_j=4/(t+2)^2 (t/(t+2))^(j-1) => u=N0*int K dt/2"]},
        {"id": "GM", "arxiv": "2511.17160v2", "file": "main.tex", "sha256": "f9cadfa03ecc9a74b0a8f432ae4b13422daeb219f253756bcd877b4b75077c59",
         "verified": ["(5.1)", "(5.4)", "(5.5)", "(5.6)", "gamma_w=1+f_v/2", "H_D0 relation", "<rho>_0"]}],
    "sources_not_reverified": ["Eisenstein & Hu 1998 (EH98, 1G-A import; formula re-typed, paper not fetched)", "W09 and Wiltshire tracker papers (not needed beyond GM)"],
    "independent_methods": {
        "M1": "tracker closed forms from GM", "M2": "EH98 re-typed, adaptive quad sigma(R), LCDM growth quadrature",
        "M3": "two-barrier absorption probability from diffusion eigenfunctions + image form (closed-form cumulatives)",
        "M4": "shell crossing from Lagrangian shells (d ln A / d ln|Delta_i| = 1/3)", "M5": "own Boolean variance",
        "M6": "exact rational identities", "M7": "direct Smoluchowski integration (constant/additive/product kernels)",
        "M8": "JSON-level F2 on 84 archived populations"},
    "independent_results": {
        "shell_crossing": ind_f["shell_crossing_independent"], "m_total": ind_f["m_total"], "Z": ind_f["Z"], "Fv_all": ind_f["Fv_all"],
        "g_LCDM": ind_f["g_LCDM"], "P_void_images_vs_fourier_max_abs": ind_f["P_void_images_vs_fourier_max_abs"],
        "primary_z0_comparison": comparison,
        "fixed_z0_cutoff_tracks": {c: ind_f["cases"][c]["fixed_cutoff_track"] for c in ind_f["cases"]},
        "variance": ind_v,
        "variance_audited_frozen_artifact": arch["variance_shares"],
        "superseded_frozen_values_F2": ind_s,
        "archive_check": {k: arch[k] for k in ("n_populations", "max_rel_diff_F2_vs_successor_archive", "violations", "n_negative_unresolved")},
        "archive_min_unresolved_below_grid": min(t[2] for t in arch["negative_unresolved"]),
        "C3_tracker_seed_historical": arch["C3_tracker_seed"],
        "X_SU_current_total_deltaL": {"PAPER_REFERENCE": 1.2626356505876934, "NW15_CMB_FIT": 1.284979492733487},
        "G_checks": ind_g},
    "tests": {
        "historical_claimed_not_reverifiable": {"environment": "Linux snapshot, CPython 3.12.14, NumPy 2.3.5, SciPy 1.17.0, pytest 9.1.1",
                                                "full_suite_31_new": "1089 passed, 34 skipped, 1 failed (git history), 220.20 s",
                                                "targeted": "32 passed, 5.30 s"},
        "this_audit": {"command": "python -B -W error -m pytest -W error -p no:cacheprovider (OPENBLAS_NUM_THREADS=1)",
                       "targeted_F_G": {"py314": "32 passed, 14.51 s", "py311": "32 passed, 13.74 s"},
                       "full_suite": {"py314": "1125 passed, 0 skipped, 0 failed, 606.19 s", "py311": "1125 passed, 0 skipped, 0 failed, 546.12 s"},
                       "historical_blob_test": "passed unmodified; blob 745b5b9acce2a7de71d950c7d00a4387fd0d7df2 at 118b8f3 == HEAD == working file",
                       "scripts_isolated_copy": {"F_successor_with_frozen_artifact": "exit 0 on both; outputs identical apart from environment; equal to inventory to <=5e-13",
                                                 "G": "exit 0 on both; byte-identical across interpreters; equal to inventory to <=1.2e-15"},
                       "recorded_evidence_sha256_reproducible_on_windows": False}},
    "findings": findings,
    "finding_counts": {"HIGH": 0, "MEDIUM": 3, "LOW": 10, "INFO": 5},
    "verdicts": {"F": "ACCEPT_WITH_CORRECTIONS", "G": "ACCEPT_WITH_CORRECTIONS", "documentation_provenance": "ACCEPT_WITH_CORRECTIONS"},
    "blocking_integration": ["FGA-D1", "FGA-F1"],
    "required_before_freeze": ["FGA-F2", "FGA-F3", "FGA-F4", "FGA-G1", "FGA-G2", "FGA-G3", "FGA-D2", "FGA-D3", "FGA-D5"],
    "optional": ["FGA-F5", "FGA-F6", "FGA-G4", "FGA-T1", "FGA-D4", "FGA-D6", "FGA-D7"],
    "remaining_checks_before_freeze": [
        "owner decision on FGA-D1 with consistent token comment and successor record",
        "apply corrections on the phase branch; rerun F/G modules and both full suites on the final tree",
        "regenerate evidence with LF writes; record hashes or tolerances",
        "record actual commit; update CLAUDE.md suite counts and validation record",
        "independent check of any recomputed r_min",
        "tag and publish only with explicit owner approval per action"],
    "auditor_evidence": {"location": "session scratchpad (not committed; repository write scope limited to the two named audit files)",
                         "sha256": {n: sha(S / n) for n in ("eqnum.py", "indep_f.py", "indep_var.py", "indep_g.py", "indep_supersede.py",
                                                             "check_archive.py", "build_inventory.py", "indep_f_out.json", "indep_var_out.json",
                                                             "indep_g_out.json", "indep_supersede_out.json", "check_archive_out.json",
                                                             "fullsuite_314.log", "fullsuite_311.log")}},
    "scientific_status_changes": [], "package_changes": [], "observational_outputs": False,
    "SIGMA8_AUTHORIZATION": "NOT_GRANTED",
}
OUT.write_bytes((json.dumps(inventory, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8"))
print(OUT, sha(OUT))
