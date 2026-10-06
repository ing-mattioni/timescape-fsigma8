"""Build reports/phase1g_fg_remediation_independent_audit_inventory.json (LF, refuses to overwrite).

Usage (repo root): python r2_build_inventory.py <evidence_dir> <out_json>
"""
import hashlib
import json
import sys
from pathlib import Path

ev, out = Path(sys.argv[1]), Path(sys.argv[2])
assert not out.exists(), "refusing to overwrite an existing inventory"


def load(name):
    return json.loads((ev / name).read_bytes())


initial = {}
for line in (ev / "logs/changed_files_initial.sha256").read_text(encoding="utf-8").splitlines():
    h, p = line.split(" ", 1)
    initial[p.lstrip("*")] = h
cmp_ = load("r2_compare_regen_out.json")
pde = load("r2_cutoffs_pde_out.json")
reg = load("r2_registry_adversarial_out.json")
gel = load("r2_gel_flory_stockmayer_out.json")
shell = load("r2_shell_test_probe_out.json")
heads = load("r2_archived_headlines_out.json")
margin = load("r2_platform_margin_out.json")
suite = json.loads((ev / "logs/suite_summary.json").read_bytes())

D = lambda status, evidence, residual=None: {"disposition": status, "evidence": evidence, **({"residual": residual} if residual else {})}
dispositions = {
    "FGA-F1": D("RESOLVED", "F successor 5.1 maps every frozen F3/superseded category; near-empty C1/collapse F2 cutoffs recomputed (max |rel| 1.94e-4 vs R2-M1); GM z=3 r>=1 0.0052522 vs 0.0052491; archived r_min declared F3-only in map, artifact cutoff_status and inventory; verdict 2 split per owner approval", "R2-N2"),
    "FGA-F2": D("RESOLVED", "Successor 4 + inventory boolean_surrogate + new test: eta=-ln(1-f)=1.33560/0.98618, ratio 1.7761/1.3115, multiplicity 1.8122/1.5728, mass accounting 3.80/2.68 vs 61.7% at 2.49"),
    "FGA-F3": D("RESOLVED", "Precision reduced (>=15 two significant figures); bias 0.22-0.24% / 0.69-0.75% quantified; tests use independent references with accuracy budgets 0.3%/0.8%/0.2%, separate from the rtol=1e-11 reproducibility gate"),
    "FGA-F4": D("RESOLVED", "Five identification assumptions listed in successor 1 (l. 62-70), separated from F1-F3 algebra"),
    "FGA-F5": D("RESOLVED", "Claim restricted to C1, z=0-3; z=0.5 near-match and non-monotone cutoff sequence stated; README/CLAUDE qualified"),
    "FGA-F6": D("RESOLVED", "Signed quadrature residual explained (5.1) and unresolved_interpretation field added; unclipped"),
    "FGA-G1": D("RESOLVED", "G 4: cohort is not F's re-identified population; t*J/V_D ~ -0.12434; coefficient 3H_v t-2 rises 2/3 -> 1; normalised source bounded above by 1/3"),
    "FGA-G2": D("RESOLVED", "G 3 l. 66-69 and script assumptions transcribe [L03] (2.2) hypotheses: no spatial correlations, morphology neglected or averaged"),
    "FGA-G3": D("RESOLVED", "History claim restricted to a prescribed common, size- and age-independent rate; instantaneous conservation vs future weighted rate stated"),
    "FGA-G4": D("RESOLVED", "G12 classified as standard covariance definition; optional numbers omitted (acceptable)"),
    "FGA-T1": D("RESOLVED", "Tail/cutoff tests use independent references (now reproducible from this evidence directory); Lagrangian shell test non-circular (R2-M5: p=4,6 give 5/6, 7/9)"),
    "FGA-D1": D("RESOLVED_OWNER_APPROVED", "Registered D successor with added_by_record; validator fail-closed (12/12 bypass attempts rejected); original addition unchanged; only one live assignment changed; NOT_GRANTED x5", "R2-N1"),
    "FGA-D2": D("PARTIALLY_RESOLVED", "Verbatim quotes and summary flags in remediation, D successor and all inventories", "R2-N3: F successor header l. 4-5 keeps an unlabelled paraphrase"),
    "FGA-D3": D("RESOLVED", "LF byte writes verified (0 CR, both interpreters); raw hashes per run; numeric gate rtol=1e-11, atol=1e-14 passed with 0 mismatches"),
    "FGA-D4": D("RESOLVED", "PowerShell commands added; executed in an isolated copy, identical outputs"),
    "FGA-D5": D("RESOLVED", "F and G docstrings distinguish project M3 accounting from [JLH13] (13)"),
    "FGA-D6": D("RESOLVED", "Historical results scoped; final-tree two-interpreter suites supplied by this audit"),
    "FGA-D7": D("RESOLVED", "Successor errata in remediation: [SvdW04] (A17)/(A18); E one-radius comment contextualised; frozen records untouched"),
}
new_findings = [
    {"id": "R2-N1", "severity": "LOW", "class": "DOCUMENTATION", "where": "src/timescape_fsigma8/scientific_status.py l. 1-12 (module docstring)",
     "issue": "Docstring registry summary omits the 2026-10-02 D successor (lists only A change, six additions, E addition, 2026-09-30 comment edits)",
     "correction": "Add one clause naming reports/phase1g_d_linear_statistic_status_successor.md (changes one added token)", "blocking": "NONE (freeze requirement)"},
    {"id": "R2-N2", "severity": "LOW", "class": "DOCUMENTATION", "where": "reports/phase1g_f_volume_budget_successor.md 5.1",
     "issue": "Location labels '§13 verdict 2' (should be §1 item 2/§5) and near-empty range attributed to §12 item 1 (it is §1 item 5/§8.2); frozen [W09]-comparison percentages superseded only generically",
     "evidence": {k: v for k, v in heads.items() if k != "rows"},
     "correction": "Fix labels; state F2 ranges 49-71%, 20-54%, <=4.3% (historical C3 normalisations)", "blocking": "NONE (freeze requirement)"},
    {"id": "R2-N3", "severity": "LOW", "class": "PROVENANCE", "where": "reports/phase1g_f_volume_budget_successor.md l. 4-5",
     "issue": "Unlabelled paraphrase 'Owner instruction: proceed with ...' remains (residue of FGA-D2)",
     "correction": "Replace with the verbatim 2026-10-01 quote or label as summary with pointer", "blocking": "NONE (freeze requirement)"},
    {"id": "R2-N4", "severity": "INFO", "class": "REGISTRY", "where": "scripts/validate_phase1f_c_r_astra_remediation.py",
     "issue": "Record order not enforced; validator alone accepts a rewritten original addition with the change dropped (caught by tests and Git); misleading message for a predecessor link on a frozen token",
     "correction": "Optional", "blocking": "NONE"},
    {"id": "R2-N5", "severity": "INFO", "class": "DOCUMENTATION", "where": "README.md sigma-track lead; reports/phase1g_g_void_evolution.md 8",
     "issue": "'pending ... independent audit' wording; Linux-run residual figures quoted", "correction": "Optional", "blocking": "NONE"},
]
inventory = {
    "classification": "REPORT_ONLY_INDEPENDENT_DELTA_AUDIT",
    "date": "2026-10-06",
    "auditor": "Claude Code (Claude Opus 5.5), at the project owner's request; same auditor as the 2026-10-02 audit (self-review of own findings mitigated by method-diverse recomputation)",
    "report": "reports/phase1g_fg_remediation_independent_audit.md",
    "evidence_directory": "reports/phase1g_fg_remediation_audit_evidence/",
    "repository": {"branch": "phase-1g-f-successor-g-evolution", "head": "fb5d95245bc0cb19ce6cd1438177f1a597bb232f",
                   "tracked_files": 259, "tracked_modified": 10, "untracked": 16, "changed_excluding_first_audit_files": 24,
                   "git_diff_check": "clean", "stash": "none"},
    "files_examined_sha256_initial": initial,
    "files_examined_unchanged_at_end": True,
    "environments": {"py314": "CPython 3.14.3, NumPy 2.5.2, SciPy 1.18.1, pytest 9.1.1",
                     "py311": "CPython 3.11.9, NumPy 2.4.6, SciPy 1.17.1, pytest 9.1.1",
                     "platform": "Windows 11", "OPENBLAS_NUM_THREADS": 1, "dependencies_changed": False},
    "owner_decisions_verified": {
        "verbatim": {"2026-10-01": "Ottimo, procedi con entrambe le cose (e sistema anche CLAUDE.md se riesci)", "2026-10-02": "si confermo"},
        "D_token": {"old": "NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY", "new": "NOT_DERIVED", "original_addition_preserved": True,
                    "only_live_assignment_changed": True, "lagrangian_sigma_AST_identical_modulo_strings": True},
        "F_verdict_2": {"milne_rate_asymptote": "DERIVED_FROM_VERIFIED_DEFINITIONS",
                        "finite_mass_seeds_equal_exactly_empty_finite_time_tracker_voids": "NOT_DERIVED"},
        "observational_authorizations": "NOT_GRANTED (SIGMA8, FSIGMA8, RSD, OBSERVATIONAL, UNIQUE_TIMESCAPE_PREDICTION)",
        "verbatim_vs_summary_distinguished": "yes, except F successor header (R2-N3)"},
    "dispositions_of_original_18": dispositions,
    "disposition_counts": {"RESOLVED": 17, "PARTIALLY_RESOLVED": 1, "OPEN": 0, "NOT_APPLICABLE": 0},
    "errata_of_first_audit_confirmed": [
        "G2 gel example: sol mass 1/t is Stockmayer ([L03] (4.77)), not Flory; Flory q=exp[-t(1-q)] ([L03] (4.74)-(4.76)), q(2)=0.20318787",
        "Finite-grid product-kernel value at t=1 (0.9531, N=120) not converged; deficit ~N^-1/2",
        "First audit's chat summary called the G6 coefficient 2/3 an upper bound; it is the shell-crossing value rising toward 1; the 1/3 bound applies to the normalised missing source"],
    "new_findings": new_findings,
    "new_finding_counts": {"HIGH": 0, "MEDIUM": 0, "LOW": 3, "INFO": 2},
    "results": {
        "near_empty_and_primary_accuracy_vs_R2M1": cmp_["accuracy_vs_R2M1"],
        "R2M1_grid_convergence_note": "N=3000 vs 6000 differences <=1.4e-7; agreement with first-audit closed form <=1e-7",
        "R2M1_fine": {c: {k: v for k, v in pde["fine"][c].items()} for c in ("PAPER_REFERENCE", "NW15_CMB_FIT")},
        "reproducibility_gate": {"rtol": 1e-11, "atol": 1e-14,
                                 "F_314_mismatches": len(cmp_["F_314_vs_inventory_mismatches"]),
                                 "F_311_mismatches": len(cmp_["F_311_vs_inventory_mismatches"]),
                                 "G_314_mismatches": len(cmp_["G_314_vs_inventory_mismatches"]),
                                 "G_311_mismatches": len(cmp_["G_311_vs_inventory_mismatches"]),
                                 "F_314_vs_F_311_mismatches": len(cmp_["F_314_vs_F_311_mismatches"]),
                                 "G_314_equals_G_311_bytes": cmp_["G_314_eq_G_311_bytes"],
                                 "platform_margin": margin},
        "archive": {k: cmp_[k] for k in ("archive_populations", "archive_max_rel_F2", "archive_violations",
                                          "archive_input_sha256", "archive_input_sha256_matches_frozen_file", "archive_cutoff_status")},
        "boolean_surrogate": cmp_["boolean_surrogate_check"],
        "registry_adversarial": reg,
        "gel_flory_stockmayer": gel,
        "shell_test_probe": shell,
        "archived_headlines_F2": {k: v for k, v in heads.items() if k != "rows"},
        "full_suites": suite,
        "tolerance_audit": json.loads((ev / "logs/tolerance_audit.json").read_bytes())["comparisons"],
        "tolerance_audit_missing": json.loads((ev / "logs/tolerance_audit.json").read_bytes())["missing_count"],
        "validator_1fcr_status": json.loads((ev / "logs/validator_1fcr.json").read_bytes())["status"]},
    "verdicts": {"F_G_science": "ACCEPT", "implementation_and_registry": "ACCEPT", "provenance_and_documentation": "ACCEPT_WITH_CORRECTIONS"},
    "integration_blockers": [],
    "ready_for_integration": "yes, for the exact file hashes recorded here (local commit by the owner); no merge, tag or remote action implied",
    "open_before_freeze": ["R2-N1", "R2-N2", "R2-N3",
                           "record actual integration commit (remediation inventory actual_remediation_commit is null)",
                           "rerun both full suites and F/G producers if any file changes after this audit",
                           "separate explicit owner approval for annotated tag and any remote action (AGENTS.md rule 7)"],
    "optional": ["R2-N4", "R2-N5"],
    "checks_not_performed": [
        "Linux 1101/34/1 run and the delivery's validation/ log (668cd3b8...) are not in the checkout",
        "Owner's bundle check and APPLY.md not available; only file hashes verified",
        "Literal PowerShell commands not run in the repository root (would overwrite artifacts); run in an isolated copy",
        "Eisenstein & Hu 1998 not re-fetched (shared model convention)",
        "Ziff & Stell 1980 not consulted; [L03] (4.74)-(4.77) suffice",
        "No phase-1G Monte Carlo rerun (variance inputs unchanged)"],
    "scientific_status_changes_by_this_audit": [], "package_changes_by_this_audit": [], "observational_outputs": False,
    "SIGMA8_AUTHORIZATION": "NOT_GRANTED",
}
out.write_bytes((json.dumps(inventory, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8"))
print(out, hashlib.sha256(out.read_bytes()).hexdigest())
