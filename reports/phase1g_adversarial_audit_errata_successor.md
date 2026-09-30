# Phase 1G adversarial audits — consolidation and errata successor record

Record classification: `AUDIT_CONSOLIDATION_AND_ERRATA_SUCCESSOR_RECORD`.
Audited checkpoint: `6f7937c`. Parent of this record: `ad1ac35` (the
approved 1G-E token), session branch `claude/zealous-rubin-1m3vf4`.
Date: 2026-09-29.
Machine-readable companion:
[`phase1g_adversarial_audit_errata_successor_inventory.json`](phase1g_adversarial_audit_errata_successor_inventory.json)
(every erratum with its frozen text, current reading and verification).

The five audits:
[1G-A](phase1g_a_adversarial_audit.md) ·
[1G-B](phase1g_b_adversarial_audit.md) ·
[1G-C](phase1g_c_adversarial_audit.md) ·
[1G-D](phase1g_d_adversarial_audit.md) ·
[1G-E](phase1g_e_adversarial_audit.md),
each with its `_inventory.json`.

## 1. What this record does

- **Consolidates** the five independent adversarial audits of Phases 1G-A to
  1G-E. Each audit ran in its own subagent, in an isolated worktree of
  `6f7937c`, without the other audits' conclusions. Each re-derived the
  load-bearing results from the arXiv LaTeX sources and recomputed the key
  numbers with its own code.
- **Applies the unambiguous errata** the audits found (typos, mis-transcribed
  numbers, broken citations, stale line references), after the lead
  verified each one (Sec. 3). The frozen reports and inventories are **not
  edited**: this record gives the current reading, as the project's
  successor records do. Four errata are in source docstrings and are applied
  there (Sec. 4).
- **Lists the owner decisions** (Sec. 6). Anything that would change a
  scientific conclusion, an equation, a status token, a tolerance, a test or
  an implementation is a decision for the owner, not a fix.
- **States tag readiness** and the tag commands (Sec. 7).

No equation, status token, tolerance, default, test or executable line
changes here.

## 2. Verdicts

| Phase | Verdict | Tag readiness | HIGH | MED-HIGH | MED | LOW-MED | LOW | Blocking owner decisions |
|---|---|---|---|---|---|---|---|---|
| 1G-A σ(M) derivation path | `ACCEPT_WITH_CORRECTIONS` | `NOT_READY_OWNER_DECISION_REQUIRED` | 0 | 0 | 2 | 1 | 8 | GA-F1 (App. B verdict), GA-F2 ([NW15] early-universe inputs), GA-F3 (the 875 unit chain) |
| 1G-B Lagrangian σ(M) runtime | `ACCEPT_WITH_CORRECTIONS` | `NOT_READY_OWNER_DECISION_REQUIRED` | 0 | 0 | 0 | 2 | 8 | GB-F1 (Linux test failure; fix option A or B) |
| 1G-C two-scale growth law | `ACCEPT_WITH_CORRECTIONS` | `NOT_READY_OWNER_DECISION_REQUIRED` | 0 | 1 | 2 | 1 | 5 | GC-F1 (what the wall σ is), GC-F2, GC-F3 |
| 1G-D separate-universe growth | `ACCEPT_WITH_CORRECTIONS` | `NOT_READY_OWNER_DECISION_REQUIRED` | 0 | 1 | 3 | 1 | 5 | GD-F1 (void-seed scale), GD-F2, GD-F3, GD-F4 |
| 1G-E two-phase variance | `ACCEPT_WITH_CORRECTIONS` | `NOT_READY_OWNER_DECISION_REQUIRED` | 0 | 2 | 2 | 1 | 2 | GE-F1 (mass conservation), GE-F2 (void population), GE-F3, GE-F4 |

**What survived everywhere.** No audit found an error in an implemented
equation, and none found a HIGH finding. The load-bearing derivations and
numbers reproduce:
- 1G-A: α = 1.70695 and the Hadamard ill-posedness; the ω_m,eff identity;
  X∞; the EH98 fit and the +3.03% Planck check (a CAMB 2.0.4 cross-check
  gives the anchored ratios to ≤ 0.5%).
- 1G-B: every 1G-A number; the text-only limitation (masked AST identical,
  21/21 gates, bit-identical numbers).
- 1G-C: the Milne-void plus EdS-wall decomposition; the a_w notation
  finding.
- 1G-D: the separate-universe modes are exact k → 0 solutions of [GM]
  (4.9)–(4.11). The comoving-closure failure is stronger than reported: no
  SU combination has `P̃_eff ≡ 0`.
- 1G-E: the Boolean covariance, the pair density and its identity, and all
  60 table values (real-space route, ≤ 3.5e−6).

**What did not survive as stated.** The MEDIUM-HIGH findings are about
interpretation and inputs, not equations:
- **GC-F1.** The 1G-C wall σ is the wall-internal linear statistic, not a
  "mass-weighted σ(M8)" that "supersedes" 1G-A. 1G-D Sec. 9 already narrowed
  the token; the 1G-C text still says more.
- **GD-F1.** The 1G-D void-seed scale uses the EdS factor 1.72, but the
  tracker grows voids by `(f_v0/f_vi)^{1/3}` ≈ 4–20. With a
  tracker-consistent seed, A_v σ_LSS(R8) falls from 2.6–4.3 to 1.05–1.5, and
  X_SU from 2.75–3.95 to 1.30–1.63.
- **GE-F1.** `σ² = δ_v²σ²_part + σ²_int` breaks mass conservation for
  δ_v ≠ −1. The correct form is `δ_v²σ²_part + (f_w − f_v δ_v)²σ²_int`.
- **GE-F2.** [W09] says 30 h⁻¹ Mpc voids fill 40–50%, not all of f_v0.

## 3. Errata applied as successor readings (lead-verified)

Each row replaces the frozen text **as the current reading**; the frozen file
is unchanged. The inventory has the exact old and new strings, the auditor's
proof and the lead's verification (29 rows).

| Id | File, location | Correction (short) | Lead verification |
|---|---|---|---|
| E-1GA-1 | 1G-A l. 50 | 0.45–0.69 → **0.44–0.69** | artifact minimum 0.444745 |
| E-1GA-5 | 1G-A l. 428 | matching epoch: add ≤ 0.9% (Mészáros) | X(z_i=20)/X∞ − 1 = +0.93% |
| E-1GA-6 | 1G-A l. 340 | "Planck (0.1431)" is the recipe 0.315 × 0.674²; [P18] Table 2 gives 0.1430 | [P18] `ms.tex` l. 2309 |
| E-1GA-7, -8 | barotropic successor record l. 104 and inventory | stale line reference 482–483 → **493–494** (482–483 at `462121c`) | report lines 493–494 |
| E-1GB-1 | 1G-B validation Sec. 1 | implementation commit `0883814` does not exist; it is **`3834a63`** (parent `dee72e1`), report `9157dc4` | `git cat-file`, `git log` |
| E-1GB-2 | 1G-B Sec. 10 | tolerance count 626 = 583 + 43 is pre-rebase; at `9157dc4`: **633 = 590 + 43** | audit at the three commits |
| E-1GB-3 | 1G-B Sec. 12 | test count 1008 is pre-rebase; `9157dc4` collects **1016 = 924 + 92** | `--collect-only` at the three commits |
| E-1GB-4 | 1G-B Sec. 9.1 | "changes no four-decimal σ" is false: three printed values move one unit (0.6053 → 0.6052, 0.7646 → 0.7645, 0.5711 → 0.5710) | the +1.8e−6 ln g bias crosses a rounding boundary |
| E-1GB-8, -9 | status-additions successor Secs. 8, 3 | the "validation block" it points to does not exist | inventory keys |
| E-1GC-1 | 1G-C l. 182 | inverted redshift `1+z = a/a0` → **`1+z = a0/a`** | [GM] l. 663; the report's own l. 186 |
| E-1GC-2 | 1G-C l. 134 | radius range 11–12.6 → **10–13 Mpc**; cell scale 140–160 → **137–164 Mpc** | 1G-A radii; 100/h |
| E-1GC-3, -4 | 1G-C ll. 123, 113 | complete the [W09] l. 386 and [W07] ll. 317–321, 404–406 citations | source lines |
| E-1GD-1…3 | 1G-D Sec. 9, Sec. 1 item 6, inventory | [NW15] σ_LSS(R8) used the [GM] radius 12.57; at its own 12.226 Mpc: **9.34e−4**, A_v σ = **2.6–4.4** (PBS), 90–930 | own evaluation: 2.969 / 4.410 |
| E-1GD-4, -5 | 1G-D Sec. 8 | rounding **353** (not 354), **3744** (not 3745) | artifact 353.30, 3744.48 |
| E-1GD-6, -7 | 1G-D Secs. 4, 1 | `δR_w = 10 H_w² δ_w` holds for the growing mode (0 for t⁻¹); sign claim holds for t ≤ t0 | algebra; root at 4.14 τ > t0 |
| E-1GD-8 | 1G-D Sec. 12 | preservation statement omits the CLAUDE.md/README.md edits of `5ab2394` | `git show --numstat` |
| E-1GE-1…3 | 1G-E Secs. 3, 5 | numeric summaries: ξ_w ≈ 0.12 [GM], **0.088** [NW15]; radius factor **1.6–1.9**; mapping **+14–26%** in σ total | table ratios |
| E-1GE-4 | 1G-E Sec. 4 | R is the photon-normalised radius of [1G-A] convention (b) | script `R = 8/h` |
| E-1GE-5 | 1G-E Sec. 2 E2 | complete the [W09] quote: such voids "fill 40–50% of the universe", plus "numerous minivoids" (ll. 277–280) | source lines |
| E-1GE-6 | 1G-E Sec. 7 | runtime "a few seconds" → about 80 s per interpreter (measured here, Linux) | measured |

E-1GD-1…3 correct the reported numbers only. The script still hard-codes
12.57 Mpc for both parameter sets; whether to change it is owner decision
GD-OD7.

**Not applied (platform-dependent round-off).** E-1GA-2, -3 and -4 would
change "≤ 4e−15" to "≤ 5e−15" (twice) and "≤ 2e−13" to "≤ 3e−13". Here, on
Linux with NumPy 2.5.3, the values are 4.108e−15 and 2.25e−13. The frozen
statements record the owner's Windows runs, which this session cannot
reproduce, and differences at this level are platform round-off. They are
recorded as a platform observation, not corrected.

## 4. Errata applied in source docstrings

These fix citations only. With docstrings stripped (the 1F-C-R validator's
`executable_tree`), both files' ASTs are identical to `ad1ac35`.

| Id | File | Change |
|---|---|---|
| E-1GB-5 | `src/timescape_fsigma8/lagrangian_sigma.py`, `timescape_growth_factor` | `γ_w0 = 1 + f_v0/2` is cited to "[GM] text after Eq. (5.7)"; Eq. (5.4) defines `a_w = γ_w⁻¹ a_D` ([GM] l. 641 vs l. 663) |
| E-1GB-6 | same file, `early_matter_density_per_photon` | same citation |
| E-1GB-7 | same file, module docstring | `a_w,reg³ = (1 − f_v) a_D³ / f_w(t_init)` (the normalisation of [GM] Eq. (5.1)) |
| E-1GE-7 | `scripts/phase1g_e_two_phase_sigma_numerics.py`, module docstring | "Model ([1G-E] Sec. 3)" → "Sec. 2" |

## 5. Lead observations across the audits

These come from the lead's consolidation and from building Phase 1G-F
([`phase1g_f_void_population.md`](phase1g_f_void_population.md)). They are
for the owner; none is applied.

- **L1 — the 1G-E wall-compression frame (adds to GE-F3/GE-F4).** 1G-E's
  ball radius R = 8/h is in photon-normalised comoving Mpc (E-1GE-4). In
  those coordinates the wall matter is compressed by
  `a_w,reg/a_photon = γ_w0 (1−f_v0)^{1/3} = D_wall` (0.877 [GM], 0.946
  [NW15]). The 1G-E primary `s = f_w^{1/3}` (0.641, 0.720) is the
  compression in the a_D (volume-average) frame. The 1G-E auditor confirmed
  `s = f_w^{1/3}` "in the mass-conserving comoving coordinate", but did not
  check that it matches R's frame. With the frame-consistent `s = D_wall`
  and everything else unchanged, the 1G-E a = 15 primary becomes:
  - σ_int **1.348** ([GM]) and **1.220** ([NW15]), instead of 1.093 and
    1.006;
  - σ total **1.759** and **1.523**, instead of 1.572 and 1.357.

  (1G-F artifact, `monodisperse_a15_vs_1G-E`.) The owner should decide the
  E4 frame together with GE-F3/GE-F4.
- **L2 — GE-F1 confirmed independently.** 1G-F derives the same
  mass-conserving wall factor `1 − f(1+δ_v) = f_w − f_v δ_v` from its own
  density bookkeeping. At δ_v = −0.8 it reproduces the auditor's 1.298 and
  1.142. 1G-F uses the corrected form throughout.
- **L3 — GD-F1/GD-F2 propagate into 1G-F.** 1G-F's separate-universe growth
  clock is reported with 1G-D's original A_v and with the tracker-consistent
  seed. The latter gives A_v = 1169 ([GM]) and 1185 ([NW15]), agreeing with
  the 1G-D auditor to 0.3%.
- **L4 — GB-F1 is the only failing test on Linux.** The preflight at
  `6f7937c` gave 1043 passed, 1 failed, 0 skipped on CPython 3.13.12 and on
  3.11.15. The failure is
  `test_top_hat_window_limits_series_and_envelope`, a bitwise-evenness
  assertion that NumPy's AVX-512 `x ** 3` breaks by one ulp. The owner's
  Windows baseline (1044 passed) is not contradicted. The test is not
  changed here: either fix changes a test or an implementation (owner
  decision GB-OD1; the auditor recommends option B).
- **L5 — the approved 1G-E token.** The auditor keeps the value
  `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`. Four corrections are proposed
  to its recorded meaning (GE-OD-6): the δ_v formula; E2 as an idealisation,
  not a [W09] statement; E4 as a sensitivity, not a bracket; and a note that
  the statistic is a hybrid. The Item A record
  ([`phase1g_e_status_addition_successor.md`](phase1g_e_status_addition_successor.md))
  quotes E1–E4 verbatim from the frozen 1G-E inventory, as the approval
  asked. Re-wording that meaning is an owner decision; the value is not in
  question.

## 6. Owner decisions (consolidated)

Each audit report's "Items for owner decision" section gives the full text.
"Blocks" marks the decisions the auditor says must be settled before a tag
(each audit's Sec. "Verdict and readiness for tagging"). Ids follow each
audit's own numbering where it has one (1G-B, 1G-D, 1G-E); for 1G-A and 1G-C
they follow the order of the audit's list.

| Id | Blocks | Decision |
|---|---|---|
| GA-OD1 (GA-F1) | yes | Record the App. B "backward-parabolic" verdict as dependent on the printed (4.15) sign; qualify "only the comoving closure defines a σ". |
| GA-OD2 (GA-F2) | yes | Choose the [NW15] row's early-universe inputs: the declared Planck hybrid, or [NW15]'s own fit (f_b ≈ 0.18, n_s ≈ 0.99, σ 0.637–0.645). Also fix the f_b justification. |
| GA-OD3 (GA-F3) | yes | Qualify the "αk ≈ 875" illustration (the report's own conventions give 557–694); the regression test pins it. |
| GA-OD4 | no | Wording and classification refinements (GA-F4–F8, F11). |
| GB-OD1 (GB-F1) | yes → **resolved 2026-09-30** | Fix the Linux-failing evenness test: option A (tolerance in the test) or option B (closed form on \|x\|, bit-identical for x > 0). The owner chose option A (Sec. 10). |
| GB-OD2–OD6 | no | Naming-firewall wording; status-validator hardening (deleted tokens pass silently); contract hardening; caveat on `TimescapeGrowthFactor`; an independent g_TS regression. |
| GC-OD1 (GC-F1) | yes | Narrow 1G-C verdict 4 and Secs. 4, 7, 9 to the wall-internal linear statistic; withdraw "settled" and decide on "supersedes". |
| GC-OD2 (GC-F2) | yes | Reclassify "exactly two FLRW regions": kinematics verified, dynamics `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`. |
| GC-OD3 (GC-F3) | yes | Add assumption A5 (the wall matter clocks the common time t) to the wall law and its token comment; the value is unchanged. |
| GC-OD4–OD7 | no | Superseded-reading bookkeeping; radius-convention labels; circular-check wording; governance wording. |
| GD-OD1 (GD-F1) | yes | Choose the void-seed convention (tracker-consistent, or [SvdW04]'s factor as an explicit assumption with both ranges). |
| GD-OD2–OD4 | yes | f_vi = 10⁻² branch vs the tracker's f_v(t_LS); S1 reclassification; "[W09] internally inconsistent" wording. |
| GD-OD5 (GD-F5) | yes | Mészáros/barotropic characterisation, including the rationale comment of the approved `GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY` token (value unchanged). |
| GD-OD6, OD7 | no | The definition of δ_L in S2; the 12.57 Mpc constant in the script. |
| GE-OD1 (GE-F1) | yes | Adopt the mass-conserving σ formula and update the δ_v table and ranges (0.9–2.1 → 0.8–2.1). |
| GE-OD2 (GE-F2) | yes | Choose the primary void population (idealisation, not a [W09] statement; or a [W09]-consistent one, σ ≈ 1.0–1.2). 1G-F now provides a derived alternative. |
| GE-OD3, OD4 | yes | E4 as a two-sided sensitivity (and, per L1, its frame); state the radius convention. |
| GE-OD5 (GE-F5) | yes | MC precision as a scatter across seeds; the first-run note. |
| GE-OD6 | no | The token's recorded meaning (L5); the value stays. |
| L1 | with GE-OD3 | The E4 frame (photon-frame `s = D_wall` vs `s = f_w^{1/3}`). |

## 7. Tag readiness and commands

**No phase is ready to tag.** Every audit returns
`NOT_READY_OWNER_DECISION_REQUIRED`, because each has at least one blocking
owner decision (Sec. 6). The errata of Secs. 3–4 do not block anything.

Once the owner has settled a phase's blocking decisions (and, for 1G-B,
fixed GB-F1 so that both suites pass on Linux and Windows), the tag goes on
the commit of `main` that carries that resolution. Tags must be signed with
the owner's key, which is not available in this session, so the lead
creates none. The commands have the style of the existing tags (`git tag -n1`);
`<commit>` is that resolution commit:

```text
git tag -s -a phase-1g-a-sigma8-derivation-path-v1 <commit> -m "Phase 1G-A v1: sigma(M) derivation-path audit (report-only). Barotropic closure Hadamard ill-posed (UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY = REFUTED_HADAMARD_ILL_POSED); conditional volume-average CGI sigma(M8) 0.52-0.69; adversarial audit reports/phase1g_a_adversarial_audit.md (ACCEPT_WITH_CORRECTIONS) with owner decisions GA-OD1..OD3 resolved; unique Timescape prediction, observational, sigma8 and fsigma8 authorization remain NOT_GRANTED."
git tag -s -a phase-1g-b-lagrangian-sigma-v1 <commit> -m "Phase 1G-B v1: conditional, model-internal, mass-labelled linear sigma(M) runtime (lagrangian_sigma.py) with the documented growth-law limitation; reproduces every 1G-A number; adversarial audit reports/phase1g_b_adversarial_audit.md (ACCEPT_WITH_CORRECTIONS) with GB-F1 fixed; NON_OBSERVATIONAL, NOT_OBSERVATIONAL_SIGMA_8; SIGMA8_AUTHORIZATION remains NOT_GRANTED."
git tag -s -a phase-1g-c-two-scale-growth-law-v1 <commit> -m "Phase 1G-C v1: two-scale growth law (report-only). Tracker = empty Milne voids plus EdS walls in common time; wall-internal linear statistic under A1-A4 (TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW = DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION; transition law NOT_DERIVED); adversarial audit reports/phase1g_c_adversarial_audit.md (ACCEPT_WITH_CORRECTIONS) with GC-OD1..OD3 resolved; no observational authorization."
git tag -s -a phase-1g-d-separate-universe-growth-v1 <commit> -m "Phase 1G-D v1: separate-universe structure (report-only). SU modes exact k->0 solutions of [GM] (4.9)-(4.11); [GM] CGI closures fail the SU test (FAILED_FOR_TIMESCAPE_TRACKER); void-onset response an external closure; adversarial audit reports/phase1g_d_adversarial_audit.md (ACCEPT_WITH_CORRECTIONS) with GD-OD1..OD4 resolved; no observational authorization."
git tag -s -a phase-1g-e-two-phase-sigma-v1 <commit> -m "Phase 1G-E v1: two-phase mass variance at 8 h^-1 Mpc (report-only; TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC = DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION under E1-E4); adversarial audit reports/phase1g_e_adversarial_audit.md (ACCEPT_WITH_CORRECTIONS) with GE-OD1..OD4 resolved; conditional, nonlinear, model-internal, not an observational sigma8; SIGMA8_AUTHORIZATION remains NOT_GRANTED."
```

Drop `-s` for an unsigned annotated tag, as `-a` alone creates. Push a tag
only with a separate explicit approval (AGENTS.md rule 7).

## 8. Files

| File | Change |
|---|---|
| `reports/phase1g_{a,b,c,d,e}_adversarial_audit.md` + `_inventory.json` | the five audits (new; written by the auditors) |
| `reports/phase1g_adversarial_audit_errata_successor.md` + `_inventory.json` | this record (new) |
| `src/timescape_fsigma8/lagrangian_sigma.py` | three docstring citations (Sec. 4); executable AST unchanged |
| `scripts/phase1g_e_two_phase_sigma_numerics.py` | one docstring citation (Sec. 4); executable AST unchanged |

Not changed: every frozen report and inventory, every test, every status
token, tolerance and equation.

## 9. Validation

Recorded in the inventory's `validation` block: the full suites, the 1F-C-R
validator, the tolerance audit and every `scripts/phase1g_*` script, on
CPython 3.13.12 and 3.11.15 (Linux).

## 10. Owner decision applied after this record (2026-09-30)

**GB-OD1 (GB-F1) — resolved with option A (test only).** The project owner
wrote on 2026-09-30, verbatim: "Fix the one test failure as suggested (fix
test), update the branch (and so the PR) and then merge the PR".

- **Change.** In `tests/test_phase1g_b_lagrangian_sigma.py`,
  `test_top_hat_window_limits_series_and_envelope` no longer asserts bitwise
  evenness:
  - the old line was `np.array_equal(top_hat_window(-x), top_hat_window(x))`;
  - the new one is `assert_allclose(..., rtol=1e-15, atol=0.0)`.

  An adjacent comment records the reason: NumPy's vectorised `x ** 3` is
  not exactly odd on AVX-512 builds; the measured difference is ≤ 2.9e−16
  relative.
- **Unchanged.** `lagrangian_sigma.py` and its outputs are not touched, and
  every other assertion of the test stays.
- **Tolerance.** The new tolerance is explicit (AGENTS.md rule 9). The
  tolerance audit counts one more explicit comparison and still finds none
  missing.
- **Verification (Linux, CPython 3.13.12 and 3.11.15).**
  - The test fails without the change and passes with it on both
    interpreters.
  - The full suites, the 1F-C-R validator and the tolerance audit are
    recorded in the inventory's `owner_resolutions` block.
- **Tag readiness of 1G-B.** GB-OD1 was the only blocking decision for 1G-B.
  The auditor asked for the fix to be run on Linux and Windows. It passes on
  Linux; once the owner's Windows run also passes, 1G-B is ready for its tag
  (Sec. 7). The other four phases still have blocking decisions.
