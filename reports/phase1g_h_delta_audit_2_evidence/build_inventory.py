"""Assemble reports/phase1g_h_delta_audit_2_inventory.json (second delta audit of 1G-H).

    python -B build_inventory.py ARTIFACT_PY313.json ARTIFACT_PY311.json OUT.json

The two artifacts are the git-ignored evidence outputs of
scripts/phase1g_h_global_variance_closure_numerics.py at 226e52d (regenerable).
Every other input is a file of this directory.
"""
import collections
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
art313 = json.loads(Path(sys.argv[1]).read_text())
art311 = json.loads(Path(sys.argv[2]).read_text())
OUT = Path(sys.argv[3])

claims = []


def claim(text, status, declared, audit, method, tolerance, location):
    claims.append({"id": f"GH-D2C{len(claims) + 1:04d}", "claim": text, "status": status,
                   "declared": declared, "audit_value": audit, "method": method,
                   "tolerance": tolerance, "location": location})


# 1. Blind science comparison (author artifact vs own reconstruction).
for line in (HERE / "blind_vs_author_comparison.txt").read_text().splitlines():
    if line.startswith(("MAX", "n compared")) or not line.strip():
        continue
    parts = line.split()
    i = parts.index("author")
    name = " ".join(parts[:i])
    a, m, rel = float(parts[i + 1]), float(parts[i + 3]), float(parts[i + 5])
    claim(f"evidence value {name}", "VERIFIED" if rel <= 1e-7 else "VERIFIED_WITH_DEVIATION", a, m,
          "BLIND_INDEPENDENT_RECONSTRUCTION (Owen's T, Stein, tilting, QAWO, Gauss-Legendre 32x64)",
          {"relative": 1e-7}, "artifacts/independent/phase1g_h_global_variance_closure.json two_phase_covariance")

# 2. Inventory numbers vs the regenerated artifact.
rec = json.loads((HERE / "inventory_reconciliation_results.json").read_text())
manual = {"radial_quadrature/h25_identity_max_rel", "radial_quadrature/intervals",
          "radial_quadrature/refinement_max_rel_vs_half"}
claim("1G-H inventory numeric leaves (results, anchoring, two_phase_covariance, ensemble example) "
      "match the regenerated artifact within half a unit of the last printed digit",
      "VERIFIED", rec["matched"] + len(rec["unmatched"]), rec["passed"] + len(rec["unmatched"]),
      "INVENTORY_VS_REGENERATED_ARTIFACT (path rules of the delta audit; 6 radial leaves by hand)",
      {"absolute": "half a unit of the last printed digit, floor 2e-12"},
      "reports/phase1g_h_global_variance_closure_inventory.json")
assert not rec["deviations"] and all(any(u.endswith(x) for x in manual) for u in rec["unmatched"])

# 3. Evidence gates, both interpreters.
for label, art in (("CPython 3.13.16", art313), ("CPython 3.11.17", art311)):
    for group, gates in art["gates"].items():
        for name, g in gates.items():
            claim(f"evidence gate {group}/{name} ({label})", "VERIFIED" if g["pass"] else "REFUTED",
                  True, g["pass"], "SAME_CODE_GATE_RERUN", {"limit": g["limit"]}, f"/gates/{group}/{name}")

# 4. Specific claims of the second remediation, the records and the prompt.
comp = json.loads((HERE / "evidence_comparisons.json").read_text())
probes = json.loads((HERE / "implementation_binding_probes_results.json").read_text())
muts = json.loads((HERE / "mutation_results.json").read_text())
cnt = collections.Counter((m["origin"], m["outcome"]) for m in muts)
S = [
    ("23 changed paths between 5c325e1 and 226e52d (10 M, 13 A), none outside the declared set", "VERIFIED", 23, 23, "GIT_DIFF_NAME_STATUS"),
    ("files of the first audit and of the delta audit byte-identical to 5c325e1", "VERIFIED", True, True, "GIT_DIFF_NAME_STATUS"),
    ("runner and configurations unchanged since 5c325e1", "VERIFIED", True, True, "GIT_DIFF_NAME_STATUS"),
    ("every package module other than global_variance.py equal to 8d3cdd0", "VERIFIED", True, True, "GIT_DIFF_NAME_STATUS"),
    ("remote heads: main 8d3cdd0, ccr-555e67be-u11yht 226e52d, phase-1g-h-independent-audit 816dd00, phase-1g-h-delta-audit 5c325e1", "VERIFIED", True, True, "GIT_LS_REMOTE"),
    ("38 annotated tags unchanged (76 refs); no D v2 tag or branch", "VERIFIED", 38, 38, "GIT_LS_REMOTE vs delta-audit snapshot"),
    ("pull requests #1-#4 closed, none from a 1G-H branch; no release", "VERIFIED", True, True, "GITHUB_LISTINGS"),
    ("P1: 0572e41 descends from 8d3cdd0 via 7900374, fd7331f", "VERIFIED", True, True, "GIT_ANCESTRY"),
    ("P2: d4d693d is a child of 0572e41", "VERIFIED", True, True, "GIT_ANCESTRY"),
    ("P3: 816dd00 tree 759ab21d, parent d4d693d", "VERIFIED", True, True, "GIT_OBJECTS"),
    ("P5: d4d693d..89cb041 = 816dd00, c1b4482, 89cb041", "VERIFIED", True, True, "GIT_ANCESTRY"),
    ("P6: 5c325e1 tree a5b810e8, parent 89cb041, 110 added files under reports/phase1g_h_delta_audit*", "VERIFIED", 110, 110, "GIT_DIFF_NAME_STATUS"),
    ("P6: the auditing session's local commit b4abbe8 is not on origin", "VERIFIED", True, True, "GIT_CAT_FILE (object absent)"),
    ("owner authorisations quoted for P1, P2, P4, P5, P6 and the plan approval", "NOT_VERIFIABLE", "verbatim quotes", None, "OFF_REPOSITORY"),
    ("evidence: 36 / 36 gates on CPython 3.13.16 and 3.11.17", "VERIFIED", 36, 36, "SAME_CODE_RERUN"),
    ("evidence: 3201 numeric leaves identical across interpreters", "VERIFIED", 3201, comp["cross_interpreter_226e52d_py313_vs_py311"]["numeric_common"], "LEAF_COMPARISON"),
    ("evidence artifact SHA-256 91aaca79...9884 on CPython 3.13.16 at 248a06b", "VERIFIED", "91aaca79ad0d0d86ad3208c8cd854e9d03839ef1f8c2d0026ff7a5cf8ff89884", "91aaca79ad0d0d86ad3208c8cd854e9d03839ef1f8c2d0026ff7a5cf8ff89884", "SAME_CODE_RERUN at 248a06b"),
    ("regression vs 89cb041: every common leaf outside the pairs bitwise identical; inside 130 changed, 6 renamed, 108 added", "VERIFIED_WITH_DEVIATION", "130/6/108, outside identical", "outside: 3 gate read-outs changed (<= 1.2e-5 abs); inside: 160 changed (156 numeric, 140 beyond round-off, 4 text), 6 renamed, 106 added; 16 added outside", "LEAF_COMPARISON (same interpreter, both interpreters)"),
    ("runner: 0.810772, 1.121363, 0.918157", "VERIFIED", [0.810772, 1.121363, 0.918157], [0.810772, 1.121363, 0.918157], "SAME_CODE_RERUN"),
    ("validator 1F-C-R PASS with 52 JSON (53 with this inventory)", "VERIFIED", 52, 52, "SAME_CODE_RERUN"),
    ("tolerance audit: 739 comparisons, 0 without tolerance", "VERIFIED", 739, 739, "SAME_CODE_RERUN"),
    ("full suites: 1178 collected; 1146 passed, 32 skipped (author environment without regenerated inputs)", "VERIFIED", 1178, 1178, "FULL_SUITE after regenerating every input: 1178 passed, 0 skipped, 0 failed on both interpreters"),
    ("42 phase tests pass", "VERIFIED", 42, 42, "PYTEST"),
    ("delta audit's 23 mutants: 21 killed; N5 and N9 survive", "VERIFIED", 21, cnt[("delta", "KILLED_BY_TESTS")], "MUTATION_CAMPAIGN"),
    ("author's 10 mutants all killed", "VERIFIED", 10, cnt[("author", "KILLED_BY_TESTS")], "MUTATION_CAMPAIGN"),
    ("the delta audit's five accepted replacements are refused", "VERIFIED", 5, sum(1 for p in probes["probes"] if p["id"].startswith("DA") and not p["accepted"]), "BINDING_PROBES"),
    ("unchanged copies of genuine records are accepted", "VERIFIED", True, True, "BINDING_PROBES (ID4-ID6) and phase test"),
    ("(H25) equals the (H18) assembly to <= 2.2e-16 (gate 1e-12)", "VERIFIED", 2.2e-16, 2.220446049250313e-16, "SAME_CODE_RERUN and own derivation (algebraic identity)"),
    ("(H25) is (H18) at x = 0 in other variables", "VERIFIED", True, True, "OWN_DERIVATION"),
    ("at fixed P11 and C_W the variance is unique", "VERIFIED", True, True, "OWN_DERIVATION (tautological given H25)"),
    ("the ordering of the totals follows <C_W - 1>", "VERIFIED", True, True, "OWN_DERIVATION: sigma^2 = sigma_part^2 + (1 + sigma_part^2)<C_W - 1>; residual <= 2.2e-16"),
    ("m_II = 2.869 / 2.140 / 1.623 (GM) and 2.474 / 2.104 / 1.669 (NW15)", "VERIFIED", [2.869, 2.140, 1.623, 2.474, 2.104, 1.669], [2.869413475, 2.139808561, 1.623350652, 2.474113488, 2.104325108, 1.668578791], "BLIND_RECONSTRUCTION"),
    ("covariance ratios 1/m_II^2 0.121-0.379", "VERIFIED", [0.121, 0.379], [0.121454534, 0.379468142], "BLIND_RECONSTRUCTION"),
    ("<C_W - 1> signed 0.756 / 0.043 (GM) and 0.791 / 0.069 (NW15)", "VERIFIED", [0.756, 0.043, 0.791, 0.069], [0.755929586, 0.043189407, 0.791264148, 0.069083113], "BLIND_RECONSTRUCTION"),
    ("<C_W - 1> lognormal 0.725-0.841 (law I), 0.698-1.278 (law II)", "VERIFIED", [0.725, 0.841, 0.698, 1.278], [0.725311249, 0.840794362, 0.697655402, 1.277631961], "BLIND_RECONSTRUCTION"),
    ("law II / law I = 0.92-1.29", "VERIFIED", [0.92, 1.29], [0.919394747, 1.293157998], "BLIND_RECONSTRUCTION"),
    ("unmasked law-II ball variance 0.085 (GM, 1 Mpc) against 0.701", "VERIFIED", [0.085, 0.701], [0.085145320, 0.701046864], "BLIND_RECONSTRUCTION"),
    ("signed law-II wall moments 7.82523e-4 / 3.55318e-3", "VERIFIED", [7.82523e-4, 3.55318e-3], [7.825229276e-4, 3.553181863e-3], "BLIND_RECONSTRUCTION (Gauss-Legendre)"),
    ("radial refinement observed 8.3e-7 / 1.0e-6 (gate 1e-5)", "VERIFIED", [8.3e-7, 1.0e-6], [8.271341681576061e-07, 1.011654765847858e-06], "SAME_CODE_RERUN; true error <= 2.4e-8 by Gauss-Legendre"),
    ("pair density integrates to 1 to 1e-12 (0.99999993 before)", "VERIFIED", [1.0, 0.99999993], [1.0000000000009304, 1 - 7.216842102579291e-08], "SAME_CODE_RERUN and own first-panel weight"),
    ("radial fix moves the signed law-II wall moments by 1.3e-3 / 6.6e-4 relative", "VERIFIED", [1.3e-3, 6.6e-4], [1.2747e-3, 6.64e-4], "LEAF_COMPARISON 5c325e1 vs 226e52d"),
    ("any published rms moves by at most 6.4e-4; totals at most 5.1e-5; no printed value changes", "VERIFIED", [6.4e-4, 5.1e-5], [6.379e-4, 5.063e-5], "LEAF_COMPARISON"),
    ("first radial panel share of the signed law-II wall moment", "VERIFIED", None, [8.346e-4, 3.729e-4], "OWN_COMPUTATION (informational)"),
    ("integrated scale dependence of the [W09] seed -0.08% to -0.12% over (a)-(c) and both scenarios", "VERIFIED", [-0.08, -0.12], [-0.0799, -0.1242], "ARTIFACT scale_dependence_rel"),
    ("1G-F median seed -0.004% to -0.005%; [SvdW04] seed -17% to -24%", "VERIFIED", [-0.004, -0.005, -17, -24], [-0.0037, -0.0053, -17.45, -23.93], "ARTIFACT scale_dependence_rel"),
    ("lognormal linear limit within 0.93% / 0.64% (gate 5%)", "VERIFIED", [0.0093, 0.0064], [0.009294099099422803, 0.006409916363450341], "SAME_CODE_RERUN"),
    ("records recompute every result and diagnostic from their stored inputs", "VERIFIED", True, True, "CODE_READING and 32 BINDING_PROBES"),
    ("the 1G-H inventory file SHA-256 declarations match 226e52d", "VERIFIED", 7, 7, "SHA256 of git blobs"),
    ("seven primary-source SHA-256 values", "VERIFIED", 7, 7, "FRESH_ARXIV_DOWNLOAD"),
    ("the four new gates were declared before their first evaluation", "NOT_VERIFIABLE", True, None, "same commit as the code; author's statement"),
    ("construction costs about twice the computation", "NOT_VERIFIABLE", "13-15 s vs 7 s", "phase file 9-11 s under parallel load", "TIMING (not controlled)"),
    ("evidence script takes about 80 s", "VERIFIED_WITH_DEVIATION", 80, [53, 46], "TIMING (3.13 with figures, 3.11 without)"),
]
for text, status, declared, audit, method in S:
    claim(text, status, declared, audit, method, None, "second remediation records / prompt")

counts = dict(collections.Counter(c["status"] for c in claims))

findings = [
    {"id": "GH-D2F1", "title": "Today's push (P7) is unrecorded and its superseded statements are incompletely listed",
     "area": "GOVERNANCE", "severity": "LOW", "relates_to": "NEW",
     "statement": "The fast-forward 89cb041 -> 226e52d of 2026-10-08 followed the commits; statements that read as current are superseded and the publication successor's dated-statement table lists only one of them.",
     "evidence": "git ls-remote (head 226e52d); lexical search (report section 9)",
     "consequence": "README, CLAUDE and the inventories present the second remediation as unpublished.",
     "locations": ["reports/phase1g_h_delta_audit_remediation.md sections 0 and 4",
                   "reports/phase1g_h_delta_audit_remediation_inventory.json commits, open_items",
                   "reports/phase1g_h_publication_successor.md section 3 and section 4 last row",
                   "reports/phase1g_h_publication_successor_inventory.json state_2026_10_08",
                   "reports/phase1g_h_global_variance_closure.md section 9 H-OD5",
                   "reports/phase1g_h_global_variance_closure_inventory.json publication.pushed_head_2026_10_08, publication.not_done, publication.h_od5_status, owner_decisions_status_2026_10_08.H-OD5",
                   "README.md 1G-H entry ('remediated locally')",
                   "CLAUDE.md 1G-H entry ('at 89cb041', 'remediated locally on top of it')"],
     "resolution_class": "CORRECTION",
     "suggested_resolution": "Add a dated 2026-10-08 publication entry P7 (89cb041 -> 226e52d carrying 5c325e1, 248a06b, 226e52d; remote head verified; authorisation as quoted by the owner) and the direct GH-F15 confirmation; extend the current-reading table to the listed statements; keep historical text; update the README/CLAUDE current summaries."},
    {"id": "GH-D2F2", "title": "New reported quantities and the new gates are weakly protected",
     "area": "TESTS", "severity": "LOW", "relates_to": "GH-DF5",
     "statement": "<C_W - 1> and 1/m_II^2 are untested (mutants A18, A20 survive tests and gates); the radial refinement estimator can be made vacuous (A15); the binding tolerance (A01) and the interval class_assumptions binding (A07) are untested; the (H25) gate compares two sums of the same kernel arrays; in the GH-DF1 test the m^-2 ratio holds by construction and m cancels in the E[chi chi psi psi] check.",
     "evidence": "mutation_results.json; implementation code reading; blind reconstruction (values correct)",
     "consequence": "Future edits could change printed <C_W - 1> or 1/m_II^2 values or weaken the binding without a failing test or gate. No present numerical error.",
     "locations": ["scripts/phase1g_h_global_variance_closure_numerics.py:_law_summary, _Ball.integral, lognormal_pairs",
                   "src/timescape_fsigma8/global_variance.py:_same, AdmissibleGlobalLinearInterval.__post_init__",
                   "tests/test_phase1g_h_global_variance.py:test_gh_df1_*"],
     "resolution_class": "CORRECTION",
     "suggested_resolution": "Add a synthetic-kernel test of both_walls_conditional_density_covariance_ball and of conditional_density_covariance_ratio_II_over_I; a Monte Carlo test of E[psi1 psi2 | both walls] with psi normalised by the sample conditional mean; a _Ball test with a known coarse/fine difference; tampers at 2*RECORD_IDENTITY_RTOL and of class_assumptions; describe the (H25) gate as a consistency check of the (H18) assembly."},
    {"id": "GH-D2F3", "title": "The regression statement of the second remediation is not literally reproducible",
     "area": "DOCUMENTATION", "severity": "INFO", "relates_to": "GH-DF1",
     "statement": "Three gate read-outs outside the pairs changed; counts inside are 160 changed (156 numeric, 140 beyond round-off, 4 text), 6 renamed, 106 added (16 added outside), not 130 / 6 / 108.",
     "evidence": "evidence_comparisons.json",
     "consequence": "None for physical values; the verification record overstates its precision.",
     "locations": ["reports/phase1g_h_delta_audit_remediation.md section 3", "reports/phase1g_h_delta_audit_remediation_inventory.json verification.regression_vs_89cb041"],
     "resolution_class": "CORRECTION", "suggested_resolution": "Erratum GH-D2E1."},
    {"id": "GH-D2F4", "title": "Typed records accept any numbers.Real; a Fraction breaks strict JSON",
     "area": "IMPLEMENTATION", "severity": "INFO", "relates_to": "GH-F9",
     "statement": "dataclasses.replace(record, linear_sigma=Fraction(record.linear_sigma)) passes every invariant and the binding; to_json_dict then fails json.dumps (TypeError). Pre-existing at 5c325e1; not reported by earlier audits (NEW).",
     "evidence": "implementation_binding_probes_results.json (TY1); check at 5c325e1",
     "consequence": "The strict-JSON contract is not enforced at construction.",
     "locations": ["src/timescape_fsigma8/global_variance.py:_real, _positive and record __post_init__"],
     "resolution_class": "CORRECTION", "suggested_resolution": "Coerce validated scalars to float in __post_init__ (as LastScatteringMatching does) or require float."},
    {"id": "GH-D2F5", "title": "Historical blocks keep the refuted 'same shared constraints' wording without a pointer",
     "area": "DOCUMENTATION", "severity": "INFO", "relates_to": "GH-DF1",
     "statement": "The first remediation record (D3 row, l. 61), its inventory (l. 113) and the regenerated 1G-H inventory revision.owner_decisions.D3 still say 'with the same shared constraints'; the dated status note names the counts and GH-DE6 but not GH-DF1; the record's files_changed_sha256 describe 89cb041 without saying so.",
     "evidence": "lexical search; SHA-256 of blobs",
     "consequence": "Minor risk of reading a 2026-10-07 statement as current.",
     "locations": ["reports/phase1g_h_audit_remediation.md:61", "reports/phase1g_h_audit_remediation_inventory.json:113",
                   "reports/phase1g_h_global_variance_closure_inventory.json revision.owner_decisions.D3"],
     "resolution_class": "CORRECTION", "suggested_resolution": "One sentence in the dated note (pairs share the carrier law, not the conditionally normalised density, GH-DF1; hashes refer to 89cb041); mark the inventory block historical."},
    {"id": "GH-D2F6", "title": "State the missing input as the mask-carrier dependence",
     "area": "SCIENCE", "severity": "INFO", "relates_to": "GH-DF1",
     "statement": "Under mask-carrier independence (E3, law I) f_v0, P11 and the carrier law fix C_W and the hybrid variance; the pairs show that the mask-carrier dependence (kappa0, kappa(r)) is the further input.",
     "evidence": "own derivation (report section 6.4)",
     "consequence": "None; the current reading is correct.",
     "locations": ["reports/phase1g_h_global_variance_closure.md section 6.3 Reading"],
     "resolution_class": "NO_ACTION", "suggested_resolution": "Optional sharper wording in section 6.3."},
]

evidence_files = sorted(p for p in HERE.iterdir() if p.is_file())
inv = {
    "schema_version": 1,
    "title": "Phase 1G-H second independent delta audit of the remediation",
    "phase": "1G-H",
    "report": "reports/phase1g_h_delta_audit_2.md",
    "audit_classification": "INDEPENDENT_DELTA_AUDIT",
    "audit_date": "2026-10-08",
    "auditor": {"name": "Claude (Anthropic), Claude Code cloud session",
                "independence": "same model family as the author (a Claude session); not the system of the two earlier audits (OpenAI Codex); no contact with the author or access to its conversation; procedural independence only"},
    "audited_commits": {
        "base": {"commit": "5c325e1fd05b343f6d5e93f931038794de4373a2", "tree": "a5b810e81d125827a17a9cf87b013ead51232080", "parent": "89cb041f901b51a3f90fa6831aab1b4553c1772c"},
        "code": {"commit": "248a06bfeb655337bc499607180c49008b5f34ea", "tree": "cb57dcf23323939f8e8260bbb303b0ec2221c185"},
        "head": {"commit": "226e52d2e4157d0130b2a9dfaffd71834c6017d9", "tree": "4db0f0f75a91321ae37b7cd7d7c6381c0c76c5c9"},
        "branch": "ccr-555e67be-u11yht (remote head 226e52d, no drift)",
        "changed_paths": {"M": 10, "A": 13}},
    "checkpoint": {"file": "reports/phase1g_h_delta_audit_2_evidence/BLIND_CHECKPOINT.md",
                   "sha256": "c5f744e31a2a63a08c8aa0984faf6ebc9e18296e36c1cf7d7203d554162754ac",
                   "local_commit": "64116509554cc0d711660da4d81ad95c3f450a6d",
                   "committed_utc": "2026-10-08T16:54:01Z",
                   "blind_to": "the author's full-precision artifact values, logs, new evidence-script functions and test expectations",
                   "not_blind_to": "three-decimal values quoted in the prompt, the revised report and the remediation record (read for model definitions)"},
    "environment": [json.loads(l) for l in (HERE / "environment.jsonl").read_text().splitlines()],
    "scope": {"in": ["commits 248a06b and 226e52d over 5c325e1", "GH-DF1..DF6, GH-DE1..DE6", "final status of GH-F1..F15", "regression of unchanged parts"],
              "out": ["a new full audit of unchanged 1G-H parts", "frozen phases 1G-A..1G-G", "Windows (not available)"]},
    "method": ["blind reconstruction with own code before reading the author's numbers (Owen's T, Stein moments, exponential tilting, QAWO Hankel transforms, Gauss-Legendre ball quadrature)",
               "reproduction on CPython 3.13.16 and 3.11.17 with every input regenerated",
               "regression against 5c325e1 and comparison with the delta audit's saved evidence",
               "32 record-binding probes", "56-mutant campaign in disposable copies",
               "inventory reconciliation, lexical search, SHA-256 checks, read-only remote state"],
    "verdict": {"PROVENANCE": "ACCEPT", "GOVERNANCE": "ACCEPT_WITH_CORRECTIONS", "SCIENCE": "ACCEPT",
                "NUMERICS": "ACCEPT", "IMPLEMENTATION": "ACCEPT", "TESTS": "ACCEPT_WITH_CORRECTIONS",
                "DOCUMENTATION": "ACCEPT_WITH_CORRECTIONS", "TASK_COMPLIANCE": "ACCEPT",
                "overall": "ACCEPT_WITH_CORRECTIONS"},
    "tag_readiness": "NO_SCIENTIFIC_BLOCKER_READY_FOR_OWNER_DECISION_AFTER_LOW_CORRECTIONS_P7_RECORD_AND_WINDOWS_GATE",
    "delta_finding_resolution": {
        "GH-DF1": {"outcome": "RESOLVED", "reason": "shared constraints narrowed at every current location; m_II, 1/m_II^2, <C_W - 1> reproduce blind; (H25) exact"},
        "GH-DF2": {"outcome": "RESOLVED", "reason": "five accepted replacements refused; 27 further probes pass only tolerance-looser, metadata or type substitutions"},
        "GH-DF3": {"outcome": "RESOLVED", "reason": "section 8 current; dated note supersedes the count; no active retired claim"},
        "GH-DF4": {"outcome": "RESOLVED", "reason": "integrated reading; -0.0799% .. -0.1242% reproduces -0.08% .. -0.12%"},
        "GH-DF5": {"outcome": "RESOLVED", "reason": "requested tests exist and kill their mutants; new gaps are GH-D2F2"},
        "GH-DF6": {"outcome": "RESOLVED", "reason": "qualifier beside every README/CLAUDE median value"}},
    "delta_errata_resolution": {"GH-DE1": "APPLIED", "GH-DE2": "APPLIED", "GH-DE3": "APPLIED",
                                "GH-DE4": "APPLIED", "GH-DE5": "APPLIED", "GH-DE6": "APPLIED_EQUIVALENT"},
    "radial_quadrature_claims": {"previous_status": "VERIFIED_WITH_DEVIATION (4)", "status": "VERIFIED",
                                 "signed_law_II_wall_moments_audit": [7.825229276e-4, 3.553181863e-3],
                                 "author": [7.82522965e-4, 3.55318191e-3], "first_panel_share": [8.346e-4, 3.729e-4]},
    "original_finding_status": {
        "GH-F1": "RESOLVED_BY_OWNER_DECISION", "GH-F2": "RESOLVED_BY_OWNER_DECISION",
        "GH-F3": "RESOLVED", "GH-F4": "RESOLVED", "GH-F5": "RESOLVED", "GH-F6": "RESOLVED",
        "GH-F7": "RESOLVED", "GH-F8": "RESOLVED", "GH-F9": "RESOLVED", "GH-F10": "RESOLVED",
        "GH-F11": "RESOLVED", "GH-F12": "RESOLVED", "GH-F13": "RESOLVED", "GH-F14": "RESOLVED",
        "GH-F15": "RESOLVED_OWNER_CONFIRMED"},
    "owner_confirmation_gh_f15": {"date": "2026-10-08", "verbatim": "Confermo le due approvazioni di push registrate (GH-F15)",
                                  "given_to": "the auditor of this second delta audit, in the handoff message",
                                  "tree_record": "reports/phase1g_h_publication_successor.md P4"},
    "finding_counts": dict(collections.Counter(f["severity"] for f in findings)),
    "findings": findings,
    "errata_of_second_remediation": [
        {"id": "GH-D2E1", "location": "reports/phase1g_h_delta_audit_remediation.md section 3; inventory verification.regression_vs_89cb041",
         "quoted": "every common leaf outside two_phase_covariance/*/gaussian_threshold_pair bitwise identical; inside it, 130 leaves changed (the radial panel and the narrowed constraint texts), 6 renamed, 108 added",
         "correct_reading": "every common physical leaf outside the pairs is bitwise identical; three gate read-outs of pair quantities change at <= 1.2e-5 absolute; inside, 160 changed (156 numeric, 140 beyond round-off, 4 constraint texts), 6 renamed, 106 added; 16 added outside"},
        {"id": "GH-D2E2", "location": "reports/phase1g_h_delta_audit_remediation.md section 0; reports/phase1g_h_publication_successor.md section 3",
         "quoted": "Commits ... Nothing is pushed. / ccr-555e67be-u11yht = 89cb041 ... is not pushed",
         "correct_reading": "pushed to ccr-555e67be-u11yht on 2026-10-08 (89cb041 -> 226e52d); true as of its commit, to be read through a dated P7 record"}],
    "mutation_testing": {"counts": {f"{o}:{k}": v for (o, k), v in sorted(cnt.items())},
                         "survivors": [m["id"] for m in muts if m["outcome"] == "SURVIVED"],
                         "killed_by_evidence_only": [m["id"] for m in muts if m["outcome"] == "KILLED_BY_EVIDENCE_ONLY"]},
    "binding_probes": probes["summary"],
    "reproduction": {
        "full_suites": {"CPython 3.13.16": {"collected": 1178, "passed": 1178, "skipped": 0, "failed": 0, "seconds": 236},
                        "CPython 3.11.17": {"collected": 1178, "passed": 1178, "skipped": 0, "failed": 0, "seconds": 234},
                        "command": "OPENBLAS_NUM_THREADS=1 python -B -W error -m pytest -q -p no:cacheprovider -rs",
                        "inputs_regenerated": ["execute_upstream_notebook", "extract_upstream_oracle", "extract_upstream_perturbation_oracle", "extract_upstream_barotropic_oracle", "compare_to_oracle", "validate_clean_perturbations", "validate_barotropic_perturbations", "validate_growth_pipeline", "validate_anchored_density_growth", "phase1g_owner_decisions_numerics (124/124 gates)"]},
        "evidence": {"gates": "36/36 on both", "numeric_leaves_identical": 3201,
                     "artifact_sha256_248a06b_py313": "91aaca79ad0d0d86ad3208c8cd854e9d03839ef1f8c2d0026ff7a5cf8ff89884"},
        "comparisons": {k: {a: b for a, b in v.items() if a not in ("outside_changed", "renamed_old_paths")} for k, v in comp.items()},
        "runner": [0.810772, 1.121363, 0.918157],
        "validator": "PASS (53 JSON with this inventory)", "tolerance_audit": {"comparisons": 739, "missing": 0},
        "diff_check": "clean"},
    "claims": claims,
    "claim_counts": counts,
    "owner_decisions": {
        "H-OD1": "recommend: keep the formal tangent as a named research proposal; (c) preferred, (a) comparison",
        "H-OD2": "recommend: no physical reference value",
        "H-OD3": "recommend: no token change; LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC NOT_DERIVED; five authorisations NOT_GRANTED",
        "H-OD4": "recommend: keep experimental; apply GH-D2F2 (and optionally GH-D2F4); Windows gate before promotion",
        "H-OD5": "recommend: no scientific blocker; before merge/freeze record P7 and the direct GH-F15 confirmation, apply GH-D2F1/GH-D2F2, run the Windows gate, take each action by explicit owner decision; consider a cross-family spot check; never create the D v2 reference",
        "P7_record": "dated entry: 2026-10-08 fast-forward of ccr-555e67be-u11yht 89cb041 -> 226e52d (5c325e1, 248a06b, 226e52d); remote head verified by this audit; authorisation as quoted by the owner: 'Fai push e prepara il prompt per un nuovo audit'",
        "GH-F15_record": "dated confirmation event: 'Confermo le due approvazioni di push registrate (GH-F15)', given directly to this auditor on 2026-10-08; status RESOLVED_OWNER_CONFIRMED",
        "this_audit_publication": "separate owner decision; designated session branch only if approved"},
    "preservation": {"existing_files_changed_by_this_audit": 0, "tokens_changed": 0, "authorizations_changed": 0,
                     "observational_authorizations": {"SIGMA8_AUTHORIZATION": "NOT_GRANTED", "FSIGMA8_AUTHORIZATION": "NOT_GRANTED",
                                                      "RSD_AUTHORIZATION": "NOT_GRANTED", "OBSERVATIONAL_AUTHORIZATION": "NOT_GRANTED",
                                                      "UNIQUE_TIMESCAPE_PREDICTION": "NOT_GRANTED"},
                     "remote_actions": "none (no push, PR, merge, tag, freeze, release, issue or comment)",
                     "d_v2_reference_created": False},
    "limitations": [
        "same model family as the author; procedural independence only",
        "checkpoint not blind to three-decimal values quoted in the prompt, report and records",
        "tracker and EH98 provider reused from the first audit",
        "Windows CPython 3.14.3 / 3.11.9 not available; the owner's gate remains unmet",
        "owner approvals quoted in records are not verifiable from the repository; only the GH-F15 confirmation was received directly",
        "ref snapshots do not show transient remote events",
        "mutation testing on the 42 phase tests and the evidence script only",
        "no spatial-lattice simulation, Boltzmann recalibration, dynamics or observational reduction",
        "one log of this audit's own 3.11 suite run was written by mistake to the container's filesystem root (outside the repository); its content is summarised in full_suite_summaries.txt"],
    "severity_scale": ["HIGH", "MEDIUM-HIGH", "MEDIUM", "LOW-MEDIUM", "LOW", "INFO"],
    "sources": {
        "primary": {
            "EH98": {"id": "astro-ph/9709112v1", "file": "trans.tex", "sha256": "5f2ac6b413df8b738c95f6650152b7e82d7c36f6d9b3a618da540e9739dce17f", "match": True},
            "GM": {"id": "arXiv:2511.17160v2", "file": "main.tex", "sha256": "f9cadfa03ecc9a74b0a8f432ae4b13422daeb219f253756bcd877b4b75077c59", "match": True},
            "JLH13": {"id": "arXiv:1304.6087v2", "file": "voids_mnras.tex", "sha256": "cf6fc77a31b395138ac3a027d008698556534e81cfb27c39853d3a99c7b07c4e", "match": True},
            "NW15": {"id": "arXiv:1410.3470v2", "file": "cmb1.tex", "sha256": "5688c9ac7123a5c2ef3508e39cb3134c2fe9e3d5e56996a4d4a4d101d7b74673", "match": True},
            "SvdW04": {"id": "astro-ph/0311260v1", "file": "e-print tarball", "sha256": "4b7ad599f54b3199e0448df1c2eecf4e724401e9ffda7b0f50a3efe7fecdb79b", "match": True},
            "W07": {"id": "arXiv:0709.0732v2", "file": "solution.tex", "sha256": "221662c987e454729ef8202c87fa697c5882b5b7daaecdedb50a7cba8ffe6cd8", "match": True},
            "W09": {"id": "arXiv:0909.0749v2", "file": "observe.tex", "sha256": "2b0324d127440e9a053a7cb37102d7655cca228a63cd2222843e879989b4b531", "match": True}},
        "retrieval": "fresh arXiv e-print downloads on 2026-10-08 into a scratch directory outside the repository; not bundled",
        "upstream": {"commit": "590c6fd5332acb15f5683ebf392a0d7ce54983c5", "notebook_sha256_lf": "628c441288d67854e0380518841dede3680bddab610e9ef5cea04937455cea2a"},
        "audit_evidence": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in evidence_files}},
}
OUT.write_text(json.dumps(inv, indent=1, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
print(json.dumps({"claims": len(claims), "claim_counts": counts, "findings": inv["finding_counts"]}))
