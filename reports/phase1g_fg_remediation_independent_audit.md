# Phase 1G-F/G — independent audit of the audit remediation

Date: 2026-10-06. Classification: `REPORT_ONLY_INDEPENDENT_DELTA_AUDIT`.
Auditor: Claude Code (Claude Opus 5.5), at the project owner's request.
Companions:
- [`phase1g_fg_remediation_independent_audit_inventory.json`](phase1g_fg_remediation_independent_audit_inventory.json);
- the evidence directory [`phase1g_fg_remediation_audit_evidence/`](phase1g_fg_remediation_audit_evidence/README.md).

**Object.** The remediation of the 18 findings of
[`phase1g_fg_independent_scientific_audit.md`](phase1g_fg_independent_scientific_audit.md)
(2026-10-02), as applied in the real checkout on branch
`phase-1g-f-successor-g-evolution` at `fb5d952`.

**Independence caveat.** This auditor also wrote the first audit, so it is
reviewing corrections to its own findings.

- Every check that the remediation's tests take from the first audit has
  been recomputed with a different numerical method (Sec. 5.2).
- Errors of the first audit are reported against it (Sec. 0.3).

**What this audit did not do.** It changed no existing file, artifact or
record. It did not stage, commit, stash, reset, check out, merge, tag or
touch the remote. Its only repository writes are this report, its inventory
and the evidence directory.

## 0. Summary

### 0.1 Verdicts

| Area | Verdict | Blocks integration |
|---|---|---|
| F/G science (successor readings, recomputed numbers, G scope) | `ACCEPT` | none |
| Implementation and status registry (validator, `scientific_status.py`, `lagrangian_sigma.py` caveat, tests) | `ACCEPT` | none |
| Provenance and documentation | `ACCEPT_WITH_CORRECTIONS` | none (corrections are freeze requirements) |

- **Ready for integration.** The corrections can be integrated: committed
  locally on the phase branch by the owner. Nothing in this audit
  authorises a merge, tag or remote action.
- **Scope of this verdict.** It holds for the exact file hashes of Sec. 1.
  Any later edit needs the two full suites again.
- **Status.** All observational authorisations stay `NOT_GRANTED`.

### 0.2 Findings

Of the 18 original findings:

- 17 are **resolved**;
- 1 is **partially resolved**: FGA-D2. One unlabelled paraphrase of the
  owner instruction survives in the F successor's header.

New findings: 3 LOW and 2 INFO (Sec. 8). None blocks integration.

### 0.3 Errata of the first audit, confirmed here

1. **The gel label.** The first audit's G2 counterexample called the
   post-gel sol mass 1/t "Flory". It is the **Stockmayer** solution,
   [L03] (4.77). Flory is [L03] (4.74)–(4.76), equivalently q = exp[−t(1−q)]:
   q(2) = 0.20318787.
2. **Gel-point convergence.** The first audit's truncated value at t = 1
   (0.9531, N = 120) was not converged. The deficit falls only as about
   N^{−1/2}: 6.7%, 4.7%, 3.3%, 2.3% and 1.6% for N = 60…960.
3. **The 2/3 coefficient.** The first audit's chat summary called the G6
   coefficient 2/3 an "upper bound". That was wrong: 2/3 is the value at
   shell crossing, and it rises toward 1 in the interior continuation. The
   upper bound 1/3 belongs to the normalised missing source. The audit
   report's own text was right, and the remediation's correction is right.

### 0.4 Tests on the final tree

Both full suites pass:

- Python 3.14.3: **1136 passed, 0 skipped, 0 failed**;
- Python 3.11.9: **1136 passed, 0 skipped, 0 failed**.

Command: `python -B -W error -m pytest -q -p no:cacheprovider`. The
historical Git-blob test passes unmodified.

## 1. Initial state, files and hashes

- **Repository.**
  - Branch `phase-1g-f-successor-g-evolution`; HEAD
    `fb5d95245bc0cb19ce6cd1438177f1a597bb232f`, the declared source base.
  - No stash.
  - `git diff --check` is clean.
  - 259 tracked files: 249 unchanged and 10 modified.
  - 16 untracked files. Two of them are the first audit's report and
    inventory, which are byte-identical to the originals (`6bb8edec…`,
    `3503a602…`).
  - That makes 24 changed files, as the owner's bundle check reports.
    That check establishes correspondence with the bundle, not correctness.
    The bundle itself, its `APPLY.md` and its `validation/` directory are
    not in the checkout and were not inspected.
- **Interpreters.**
  - CPython 3.14.3 (`.venv`): NumPy 2.5.2, SciPy 1.18.1, pytest 9.1.1.
  - CPython 3.11.9 (`.venv311`): NumPy 2.4.6, SciPy 1.17.1, pytest 9.1.1.
  - Windows 11; `OPENBLAS_NUM_THREADS=1`.
- **Protection.**
  - SHA-256 of all 500 working-tree files outside `.venv*`, `.git` and
    caches, before and after the audit (Sec. 7.4).
  - The F and G producers were run only in isolated copies.

Files examined (SHA-256 at the start of the audit; all unchanged at the
end):

| File | Status | SHA-256 |
|---|---|---|
| `CLAUDE.md` | modified (tracked) | `0eaf3c5af6b459ee27481a988bd48b28dcd0b1e0609fc4c315edba525ed5cd75` |
| `README.md` | modified (tracked) | `3c3c0355d35665782ec2abb6809438e72fa6643f0f1a9747d88d9c3683168f44` |
| `reports/phase1g_d_linear_statistic_status_successor.md` | untracked | `ece7d11f4707b410ad296f6c67f1f258ceb6be4ce2aa4008e4d6afeb39960f71` |
| `reports/phase1g_d_linear_statistic_status_successor_inventory.json` | untracked | `4026a6add8a83cd34dc7c676df75eb84a3e6be451a1928ee7a428a1b310237ea` |
| `reports/phase1g_f_volume_budget_successor.md` | untracked | `8568fe9417052ba7ed78b9901f9f54520afe53ac3dc49e40fa96631a1e196a32` |
| `reports/phase1g_f_volume_budget_successor_inventory.json` | untracked | `3b4c0ea27503d5f5d317b600ec3c6ae3708a608a65b3ead1246139e600793c16` |
| `reports/phase1g_fg_audit_remediation.md` | untracked | `2bdbbe32c56553da8843594f28ad19dafc130935d64008e97fe96f69c9ee3aff` |
| `reports/phase1g_fg_audit_remediation_inventory.json` | untracked | `ff2336e89c514b89d4b03b1adc559ea25575c57236ef2031ee5a4b86888603a7` |
| `reports/phase1g_fg_independent_scientific_audit.md` | untracked, first audit (intact) | `6bb8edecf394989186c86e3ead7f401bcbcc0ac1977bc395008db7019a0c063d` |
| `reports/phase1g_fg_independent_scientific_audit_inventory.json` | untracked, first audit (intact) | `3503a602413cb15f8daed58bf0a6d31a6c0defcc222527ce528753812d888aae` |
| `reports/phase1g_fg_successor_validation.md` | untracked | `438a0063363c78ec50ae3ce793264215cf7ba4de58e83d434a4d9ffb8e2b278a` |
| `reports/phase1g_g_void_evolution.md` | untracked | `bca7832333527f83eb750d1c39fcac92d49bc1891c761908f4e64eb861bb0d61` |
| `reports/phase1g_g_void_evolution_inventory.json` | untracked | `8e801932a64df1169294136979164b2eb3e4674e1838eac15d402a60eec0c62e` |
| `scripts/phase1g_f_volume_budget_successor_numerics.py` | untracked | `59b62454ac65a121a603b073e875f9c26d40b1a04deb0185d96d04adb4718a9e` |
| `scripts/phase1g_g_void_evolution_numerics.py` | untracked | `e5829e97009d55482890c25ca6725959078091cefe8869abccaae760435eb113` |
| `scripts/validate_phase1f_c_r_astra_remediation.py` | modified (tracked) | `e6fb92b0812f05e42b1ec4f739996440e3998a99fa07bdd77694a11fd31787c5` |
| `src/timescape_fsigma8/lagrangian_sigma.py` | modified (tracked) | `d604108b1f070928eb8b21c1e84af8b13144f914fb21892467f200d78f14a46b` |
| `src/timescape_fsigma8/scientific_status.py` | modified (tracked) | `3c626f58ce3bcccd4df242d3287266c1769b7224eeeabcc90566777af68c61bc` |
| `tests/phase1g_owner_decisions_test_utils.py` | modified (tracked) | `11789870008b7e7157a7e146745bda981c7b0bfd2d2894445b889859de87da50` |
| `tests/test_barotropic_hadamard_refutation.py` | modified (tracked) | `684de34a1ac4583342e32d36dce97301ee8a1d464e750ba1f43a3f21972d674e` |
| `tests/test_phase1g_d_linear_statistic_status_successor.py` | untracked | `48cd02d8b0299593236fedbeb8847ef5886644e6050f6979b63f53b2b325f03a` |
| `tests/test_phase1g_d_owner_decisions.py` | modified (tracked) | `49cab57c768a1edc9e0b0156f969c25e330bfb91cb1956071fb9fa9b36c4e020` |
| `tests/test_phase1g_e_status_addition.py` | modified (tracked) | `a3f7f4f6b60ab8356b69bb39ad95c5dc7fabccce2bddfa8d3095a8f049828f1c` |
| `tests/test_phase1g_f_volume_budget_successor.py` | untracked | `aee627c28cbbf6c7f76e0bb3699b1a84a22ea221bd7797b581971ab9f41c76ba` |
| `tests/test_phase1g_g_void_evolution.py` | untracked | `aaf32213ae01247577aa097f80662ff6bf2b0da5996ad825cfa9cd0de8a25de8` |
| `tests/test_phase1g_status_additions.py` | modified (tracked) | `efd6f92b2532de41fe852c8a6f3ff6d989bbbe868468789138c86acaa0a5c245` |

The frozen-file pins `frozen_sha256` in the F and G inventories match the
checkout:

- AGENTS.md;
- the frozen 1G-F report, inventory and script.

The pre-change `scientific_status.py` hash (`146eb907…`) is now recorded as
`historical_snapshot_sha256`, and equals the HEAD blob. All 111 tracked
report and inventory files are unmodified.

## 2. Documents, code and sources examined

- **Reports and inventories.**
  - The first audit;
  - the remediation;
  - the D linear-statistic successor;
  - the F volume-budget successor;
  - the G void-evolution report;
  - the F/G validation record.
  - Also the frozen 1G-F report, the 1G-D report and owner-decision
    successor, the original status-additions record, and the E addition
    and owner-decision records.
- **Code.**
  - Both successor producers, diffed against the audited versions kept in
    the first audit's isolated copy (hashes `d0030a84…`, `db11ad5c…`);
  - the 1F-C-R validator;
  - `scientific_status.py`;
  - the `lagrangian_sigma.py` caveat;
  - five modified tests or helpers and three new or updated test modules;
  - README and CLAUDE.md.
- **Primary sources.** The arXiv LaTeX of [L03] cond-mat/0305670, with
  equation numbers reconstructed by the first audit's parser:
  - (2.2) and the text below it;
  - (4.4), (4.10);
  - (4.73)–(4.77): (4.74) the Flory equation; (4.75)–(4.76) the Flory sol
    mass; (4.77) the Stockmayer post-gel c_j ∝ 1/t.
  - Also [JLH13] 1304.6087 (A4)–(A5) and (A8)–(A12), and [SvdW04]
    astro-ph/0311260 (A17)–(A18), as hashed in the first audit's inventory.

## 3. Owner decisions — fidelity of application

The two decisions confirmed with **"si confermo"** (2026-10-02) are applied
faithfully.

- **D token.**
  - `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC`:
    `NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY` → `NOT_DERIVED`, through the
    canonical registered record
    `phase1g_d_linear_statistic_status_successor_inventory.json`, with
    `added_by_record` pointing to the original addition.
  - The original addition record is unchanged against HEAD and still holds
    the old value.
  - The live module, its comment and the `lagrangian_sigma.py` caveat
    agree.
  - It is the only changed live assignment of the 26.
  - The `lagrangian_sigma.py` AST is identical to HEAD once string
    constants are masked, so no numerical expression of σ(M) changes.
  - `SIGMA8_AUTHORIZATION`, `FSIGMA8_AUTHORIZATION`, `RSD_AUTHORIZATION`,
    `OBSERVATIONAL_AUTHORIZATION` and `UNIQUE_TIMESCAPE_PREDICTION` are all
    `NOT_GRANTED`.
- **F verdict 2 split.** The Milne-rate asymptote is
  `DERIVED_FROM_VERIFIED_DEFINITIONS`; the finite-time identification is
  `NOT_DERIVED`. The split is recorded consistently in the D successor, F
  successor §5.1, the F inventory (`frozen_verdict_2_current_reading`),
  CLAUDE.md and README. It adds no API token, as stated.
- **Verbatim vs summary.**
  - The quotes "Ottimo, procedi con entrambe le cose (e sistema anche
    CLAUDE.md se riesci)" (2026-10-01) and "si confermo" (2026-10-02) are
    reproduced verbatim.
  - The scope is marked as a summary in the remediation report, the D
    successor and every inventory: `proposal_summary_is_verbatim: false`
    and `scope_is_summary_not_verbatim: true`.
  - One residue: the F successor's header (l. 4–5) still carries the old
    unlabelled paraphrase "Owner instruction: proceed with…" (R2-N3).

## 4. Disposition of the 18 original findings

| Finding | Original severity | Disposition | Evidence |
|---|---|---|---|
| FGA-F1 | MEDIUM | **Resolved** (residual R2-N2) | F §5.1 maps every superseded category. The near-empty C1/collapse F2 cutoffs are recomputed (≤ 1.94e−4 from R2-M1). GM z = 3 r ≥ 1 is 0.0052. The archived r_min values are declared F3-only in the map, the artifact and the inventory. Verdict 2 is split as approved. |
| FGA-F2 | MEDIUM | **Resolved** | F §4, inventory `boolean_surrogate` and a new test. Verified: η = 1.33560 / 0.98618; ratio to F 1.776 / 1.311; multiplicity 1.812 / 1.573; the mass accounting (Sec. 5.6). |
| FGA-F3 | LOW | **Resolved** | Precision reduced (≥15 to two significant figures) and the bias quantified. Tests use independent references with accuracy budgets 0.3% / 0.8% / 0.2%, kept separate from the reproducibility gate (Sec. 5.4). |
| FGA-F4 | LOW | **Resolved** | The five assumptions are listed and separated from the F1–F3 algebra (Sec. 5.5). |
| FGA-F5 | INFO | **Resolved** | Restricted to C1, z = 0–3. The z = 0.5 near-match (≈1.5%), the −11% at z = 1 and the non-monotone sequence are stated. README and CLAUDE.md are qualified. |
| FGA-F6 | INFO | **Resolved** | Signed quadrature residual, unclipped; the artifact carries an `unresolved_interpretation` field. |
| FGA-G1 | LOW | **Resolved** | G §4: the cohort is not F's population; t J/V_D ≈ −0.12434; the coefficient rises 2/3 → 1; the source is bounded above by 1/3. This also corrects the first audit's summary error. |
| FGA-G2 | LOW | **Resolved** | The [L03] (2.2) mean-field and morphology hypotheses are transcribed in G §3 and in the script's `assumptions`. |
| FGA-G3 | LOW | **Resolved** | The claim is restricted to a common, size- and age-independent rate. The difference between instantaneous conservation and the future weighted rate is stated. |
| FGA-G4 | INFO | **Resolved** | G12 is classified as a standard definition. The optional radius numbers were omitted, which is acceptable. |
| FGA-T1 | LOW | **Resolved** | The references are independent (now reproducible from the evidence directory). The new Lagrangian test is non-circular (Sec. 5.7). |
| FGA-D1 | MEDIUM | **Resolved** (owner-approved; residual R2-N1) | The D successor is registered. The validator is fail-closed (Sec. 6). The original addition is preserved, only one live assignment changes, and the authorisations stay `NOT_GRANTED`. |
| FGA-D2 | LOW | **Partially resolved** | Verbatim quotes with summary flags appear in the remediation, the D successor and every inventory. The F successor header still has an unlabelled paraphrase (R2-N3). |
| FGA-D3 | LOW | **Resolved** | LF byte writes verified (0 CR on both interpreters). Raw hashes are per run. The declared numeric gate passes with 0 mismatches. |
| FGA-D4 | LOW | **Resolved** | PowerShell commands added. Run in an isolated copy, they give identical outputs. |
| FGA-D5 | LOW | **Resolved** | Both docstrings now separate the project's M3 accounting from [JLH13] (13). |
| FGA-D6 | INFO | **Resolved** | The historical runs are scoped. This audit supplies the final-tree two-interpreter suites (Sec. 7). |
| FGA-D7 | INFO | **Resolved** | Errata are recorded in the remediation (A17/A18; the E comment put in context) without editing frozen records. |

The remediation's remaining gate "preserve the external auditor's scratch scripts and logs" is closed. All 14 files were recovered with SHA-256 identical to the first audit's inventory, and are committed here as evidence (`prior_audit_2026-10-02/`).

## 5. Scientific verification of the corrections

### 5.1 Completeness of the frozen → current map (F successor §5.1)

The map covers every category of frozen F3-based or superseded reading:

- the synthesis (§1, Reading, §12);
- the ≥10 fill;
- the primary r_min;
- the near-empty range;
- the §9 history;
- the proposed §13 classifications;
- all archived radius cuts;
- all archived r_min values;
- verdict 2.

Archived r_min values are explicitly F3-only:

- the map row;
- the artifact's `cutoff_status`;
- the inventory's `frozen_r_min_current_meaning`.

No archived entry carries an F2 cutoff key (verified on all 84). The only
F2 cutoffs supplied are the primary and C1/collapse near-empty ones, as
stated.

Two residual imprecisions (R2-N2):

- **Location labels.** "§13 verdict 2" should cite §1 item 2 and §5. The
  0.06–0.8 near-empty range is in §1 item 5 and §8.2, not in §12 item 1.
- **Unstated numbers.** Three frozen [W09]-comparison percentages are
  marked superseded only generically ("F2 corrections available"). Their
  F2 values, from the regenerated archive (R2-M6), are:
  - PBS shell-crossing r ≥ 10: 62–73% (F3) → 49–71% (F2);
  - PBS x = 0.1: 40–68% → 20–54%;
  - C1/C2/C3-seed: ≤ 10% → ≤ 4.3%.

  These populations use the historical C3 normalisation.

### 5.2 Near-empty cutoffs and the z = 3 fraction — method-diverse recomputation

The remediation's tests take their references from the first audit's
closed-form values. To avoid a circular check, R2-M1 recomputes them by
another route:

- the backward Kolmogorov equation for the two-barrier absorption
  probability, solved with Crank–Nicolson on two grids;
- σ(R) by fixed Gauss–Legendre panels;
- shell crossing from Lagrangian shells.

The two grids agree to ≤ 1.4e−7. The fine-grid results also agree with the
first audit's closed form to ≤ 1e−7.

| Case, x | Audited F2 cutoff (grid) | R2-M1 reference | Relative | Frozen F3 |
|---|---:|---:|---:|---:|
| GM, 0.10 | 0.093999 | 0.094017 | −1.94e−4 | 0.18769 |
| GM, 0.05 | 0.018783 | 0.018785 | −1.09e−4 | 0.06198 |
| NW15, 0.10 | 0.393561 | 0.393599 | −0.96e−4 | 0.80955 |
| NW15, 0.05 | 0.095238 | 0.095246 | −0.94e−4 | 0.28594 |

- The claim "within 0.02%" holds; the largest deviation is 0.0194%.
- The test budget of 0.2% covers it with a margin of ten.
- GM r ≥ 1 at z = 3: audited 0.0052522, reference 0.0052491 (+5.9e−4). The
  successor's "about 0.0052" is right. NW15: 0.0043813 vs 0.0043764.
- Primary cutoffs and tails reproduce the first audit's accuracy figures:
  cutoffs −3.0e−4 / −1.6e−4; ≥10 +0.23% / +0.22%; ≥15 +0.70% / +0.75%.

### 5.3 The 84 archived populations

The F producer was regenerated with
`--frozen-artifact artifacts/independent/phase1g_f_void_population.json`
in an isolated copy (R2-M2).

- The input SHA-256 is `4523ef03…` before and after, and equals the
  recorded `input_sha256`.
- All 84 populations keep m, x and the legacy F3 values exactly. F2 agrees
  with a direct recomputation at relative difference 0.
- The frozen clocks, including C3 (D_t0 = 1.020230 / 1.033503), are read,
  not altered.

### 5.4 Tolerances: reproducibility versus accuracy

These are distinguished correctly in the successors and the remediation.

- **Reproducibility gate** (rtol = 1e−11, atol = 1e−14, numeric leaves;
  keys and labels exact; `environment` and `input_sha256` excluded).
  - Both Windows interpreters match the Linux inventory with **0
    mismatches**: F primary, near-empty and Boolean blocks; the full G
    evidence.
  - Across 418 leaves the largest absolute difference is 1.8e−14, and 111
    leaves are bit-identical.
  - 3.14 and 3.11 agree apart from `environment` (F); G is byte-identical
    across interpreters and to the repository's 12:13 artifact.
  - The gate certifies floating-point equivalence across platforms, nothing
    more. For tiny leaves (residuals ~1e−16, z = 3 tails ~1e−26) the atol
    makes the comparison vacuous. That is acceptable, because those values
    are scientifically null.
- **Accuracy.** The 481-node grid error is a separate, much larger
  quantity: +0.22–0.24% at ≥10, +0.69–0.75% at ≥15, ≤ 0.02% for the
  near-empty cutoffs.
  - The test budgets are 0.3%, 0.8% and 0.2%. They are explicit accuracy
    budgets against independent references, not reproducibility claims.
  - The ≥15 margin is narrow (0.05 percentage points), but the grid is
    fixed and deterministic.
- **Precision of quoted values.** The successor now quotes at most two
  significant figures at ≥15, as it should.

### 5.5 The five EdS/wall identifications and the negative residuals

- **The five conditions.** F successor §1 (l. 62–70) lists exactly the
  five, separated from the elementary F1–F3 identities:
  1. simultaneous bang with C1/A5;
  2. unperturbed flat EdS walls;
  3. an isolated seed, increasingly strained at large filling;
  4. the Lagrangian mean taken as the wall reference;
  5. non-void and cloud-absorbed mass at ρ_w.
- **The negative residuals.** They are described as signed quadrature
  overshoot (twelve rows, down to −1.72e−7), not negative mass. They stay
  unclipped, and the artifact carries an explicit
  `unresolved_interpretation` field.

### 5.6 The hybrid variance

R2-M2 recomputes the Boolean quantities from the coverage:

- η = λE[V_grain] = −ln(1−f_v0) = 1.33560 / 0.98618, dimensionless;
- 1 − e^{−η} = f_v0, exactly;
- η / F2_all = 1.7761 / 1.3115;
- conditional multiplicity η/f_v0 = 1.8122 / 1.5728;
- the empty-surrogate wall density 1/(1−f_v0) = 3.802 / 2.681 times the
  mean, against M3's 61.7% of the mass at 2.49 times the mean.

All match the successor and its new test. The successor now says, in
substance, that the grains share only the volume-weighted radius shape,
overlap, and carry an independently calibrated intensity. σ ≈ 0.99 stays a
conditional hybrid: no dynamical closure, no observational authorisation,
and the token values are unchanged.

### 5.7 G — scope of the deductions

- **G6.** It is restricted to a synchronous shell-crossing cohort, and
  contrasted explicitly with F's population, which is re-identified at
  every epoch. The value t J/V_D ≈ −0.12434 for a persistent cohort matches
  the first audit's.
- **The continuation.** The coefficient 3H_v t − 2 rises from 2/3 toward 1.
  The normalised missing source is bounded above by 1/3. Both statements
  are now explicit, and "2/3 is not an upper bound" is stated.
- **Mean field.** The L03 hypotheses are transcribed faithfully: no
  spatial correlations, and morphology neglected or averaged. They are
  marked as not derived for connected cosmic voids.
- **Instantaneous vs history.** G2 conserves volume at the merger instant.
  With size- or age-dependent rates, the subsequent weighted expansion can
  change. The history claim is restricted to a common, size- and
  age-independent rate (report §1, §2; CLAUDE.md; README).
- **The new Lagrangian test** (R2-M5). It is independent of the imposed
  condition. It finds the zero of ∂r/∂R_i at fixed t from (A4)–(A5), then
  measures H t by time differences.
  - It converges at second order in the label step: errors −2.06e−6,
    −2.06e−8 and −2.1e−10 for steps 1e−2, 1e−3 and 1e−4.
  - It is independent of the shell label (self-similar exterior profile).
  - With exterior profiles Δ_i ∝ R_i^{−p}, p = 4 and 6, the same algorithm
    returns 5/6 and 7/9 to ~1e−9, as the hand-derived 2(1+p)/(3p) requires.
    A procedure that imposed 8/9 could not do this.
  - The budget 2e−7 is loose (observed ~2e−10) but explicit.

### 5.8 The gel erratum (R2-M4)

| t | Flory q = exp[−t(1−q)] | (4.75)–(4.76) | Stockmayer (4.77) | 1/t |
|---:|---:|---:|---:|---:|
| 1.5 | 0.4171884 | 0.4171884 | 0.6666667 | 0.6666667 |
| 2 | 0.2031879 | 0.2031879 | 0.5000000 | 0.5 |
| 3 | 0.0595202 | 0.0595202 | 0.3333333 | 0.3333333 |

- **The truncated models.**
  - Stockmayer-type truncation (inert gel beyond N) converges to 1/t for
    t ≥ 1.5 by N = 240.
  - Flory-type truncation (sol reacting with total mass 1) converges to q.
  - At t = 1 both converge only as about N^{−1/2}: Stockmayer 0.933,
    0.953, 0.967, 0.977, 0.984 for N = 60…960.
- **Consequences.**
  - The remediation's erratum and its "no certified gel-point convergence"
    are correct.
  - G2's no-gel condition remains necessary.
  - [L03] itself notes that the mean-field assumptions break down near the
    gel point.

## 6. Status registry and implementation

- **The validator change.** It is minimal and fail-closed:
  - an added token may be changed once;
  - the change record must name the adding record (`added_by_record`),
    differ from it, and carry `old_token` equal to the added value;
  - the live value must equal `new_token`;
  - duplicates are rejected by the readers;
  - a predecessor link on a non-added token is rejected.
- **The adversarial run (R2-M3).** Fifteen cases against the live
  validator:
  - all **12 bypass attempts fail as required**: no link; an unregistered
    or wrong link; an inconsistent old value; a re-addition; the same
    change twice; a chained second change; a live value not updated or
    different; a link on a frozen token; removal of the added token; an
    unrelated live token changed;
  - the real registry passes;
  - two informational cases pass (R2-N4): record order is not enforced,
    and rewriting the original addition while dropping the change passes
    the validator alone. That rewrite is caught by
    `test_phase1g_status_additions` (which compares the record with the
    original values) and by `test_phase1g_d_linear_statistic_status_successor`
    (which asserts the original value), and by Git.
- **Records.** All four registered records are canonical UTF-8/LF JSON.
  The 1F-C-R validator reports `PASS`:
  - changes `{LINEAR_GLOBAL_MEAN…, UNRESTRICTED_BAROTROPIC…}`;
  - 7 additions;
  - 43 JSON round-trips;
  - 52 historical reports unchanged.
- **Modified tests.** They keep the historical pins: the original addition
  value in the six-token record and in the D test, the frozen 1F-C-R
  snapshot, and the Git-blob gate. They assert the live value separately.
  No assertion was weakened beyond the approved value change.
- **One stale docstring.** The `scientific_status.py` module docstring
  still lists only the earlier successor records (R2-N1).

## 7. Numerical validation (this audit)

| Check | Python 3.14.3 | Python 3.11.9 |
|---|---|---|
| Full suite, `python -B -W error -m pytest -q -p no:cacheprovider` | **1136 passed, 0 skipped, 0 failed**, 525 s | **1136 passed, 0 skipped, 0 failed**, 462 s |
| Historical Git-blob test (in the suite, unmodified) | passed | passed |
| F producer `--frozen-artifact`, isolated copy (bash and the documented PowerShell form) | exit 0; LF; input unchanged | exit 0; LF |
| G producer, isolated copy | exit 0; LF | exit 0; byte-identical to 3.14 |
| Gate rtol = 1e−11, atol = 1e−14 vs inventories | 0 mismatches | 0 mismatches |
| `audit_numerical_tolerances.py` | 669 comparisons, 0 missing | — |
| `validate_phase1f_c_r_astra_remediation.py` | PASS | — |
| `git diff --check` | clean | — |

- **Count.** 1136 is the expected count for this patch. Nothing is skipped
  because the oracle and generated inputs are present.
- **Historical results.** The earlier 1125/0/0 (pre-remediation tree) and
  the Linux snapshot's 1101/34/1 do not certify this run, and were not
  relied on.
- **7.4 Preservation.** The 500-file working-tree checksum after the audit
  equals the one before, apart from the new deliverables (500/500 files identical; the only additions are this report, its inventory and the evidence directory).

## 8. New findings

### R2-N1 — LOW, documentation (implementation)
- **Where.** `src/timescape_fsigma8/scientific_status.py` l. 1–12, the
  module docstring.
- **Issue.** It lists the successor records as "barotropic changes one
  token; additions six; E adds one" plus the 2026-09-30 comment edits. It
  omits the 2026-10-02 D successor that changes one more token. The token
  comment itself is correct.
- **Impact.** A reader of the API module gets an incomplete registry
  summary. No functional effect.
- **Minimal correction.** Add "reports/phase1g_d_linear_statistic_status_successor.md
  changes one added token" to the docstring.

### R2-N2 — LOW, documentation (science record)
- **Where.** `reports/phase1g_f_volume_budget_successor.md` §5.1, map rows
  1 and 4 and the archived row.
- **Issue.** Two location labels are imprecise (Sec. 5.1). Three frozen
  [W09]-comparison percentages are superseded only generically.
- **Impact.** A reader of frozen §1 item 4 or §8.2 must open the artifact
  to find the current values: 49–71%, 20–54% and ≤ 4.3%.
- **Minimal correction.**
  - Fix the two labels.
  - State the three F2 ranges, noting that they use historical C3
    normalisations.

### R2-N3 — LOW, provenance (residue of FGA-D2)
- **Where.** `reports/phase1g_f_volume_budget_successor.md` l. 4–5.
- **Issue.** "Owner instruction: proceed with the proposed 1G-F
  rectification and 1G-G theoretical work, and update CLAUDE.md." is an
  unlabelled paraphrase. Every other record quotes verbatim and flags its
  summaries.
- **Minimal correction.** Replace it with the verbatim 2026-10-01 quote,
  or label it as a summary and point to the remediation record.

### R2-N4 — INFO, registry
- The validator does not enforce the order of registered records.
- A rewrite of the original addition is caught by tests and Git, not by
  the validator.
- Its message for a predecessor link on a frozen token ("token absent from
  the frozen snapshot …") is inaccurate, although the check fails
  correctly.
- None of these needs a change for integration.

### R2-N5 — INFO, documentation
- README's σ-track lead still says "pending integration and independent
  audit". The audit exists; the later bullet explains its scope.
- The G report's §8 residual figures (1.67e−16, 2.11e−15) are those of the
  Linux run; Windows gives ≤ 1.1e−16.
- Both are cosmetic.

## 9. Checks not performed, and why

- **Linux reproduction of 1101/34/1.** The remediation's `validation/`
  directory and log (`668cd3b8…`) are not in the checkout, and no Linux
  interpreter is available here.
- **The owner's bundle check and `APPLY.md`.** They are not in the
  checkout. Only file hashes were verified.
- **The literal PowerShell commands in the repository root.** These would
  overwrite repository artifacts. The same commands were run in an
  isolated copy with the project interpreter.
- **Eisenstein & Hu (1998).** Not re-fetched; it is a shared model
  convention, as in the first audit.
- **Ziff & Stell (1980).** Cited by [L03] for the Flory/Stockmayer
  distinction; not consulted. [L03] (4.74)–(4.77) suffice for the erratum.
- **A full phase-1G Monte Carlo rerun.** Not needed, because σ ≈ 0.99 has
  inputs unchanged by the remediation (first audit, Sec. 4.9).

## 10. Integration blockers and freeze requirements

**Blocking integration: none.** The remediation resolves the two
integration blockers of the first audit (FGA-D1, FGA-F1) and every freeze
requirement except a residue of FGA-D2.

**Open before a phase freeze/tag:**

1. R2-N1, R2-N2 and R2-N3 (text-only; no numeric or status change).
2. Record the actual integration commit in the remediation inventory
   (`actual_remediation_commit` is `null`) and in the validation record.
3. If any file changes after this audit, rerun both full suites on the
   committed tree, and the F/G producers with the declared gate.
4. Give the annotated tag and any remote action separate explicit owner
   approval (AGENTS.md rule 7). "si confermo" does not cover them.

**Optional:** R2-N4, R2-N5.

## 11. Status statement

- No equation, initial condition, tolerance or numerical output of the
  package changes in the audited remediation. The one status value changed
  (`LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` → `NOT_DERIVED`) is
  owner-approved and correctly registered.
- The F/G results remain conditional, model-internal research evidence.
  σ ≈ 0.99 is a conditional hybrid variance, not an observational σ8.
- `SIGMA8_AUTHORIZATION`, `FSIGMA8_AUTHORIZATION`, `RSD_AUTHORIZATION`,
  `OBSERVATIONAL_AUTHORIZATION` and `UNIQUE_TIMESCAPE_PREDICTION` remain
  `NOT_GRANTED`.
