# Phase 1B compliance audit (read-only)

**Project:** timescape-fsigma8
**Date:** 2026-07-15
**Auditor:** Claude (session audit; no source, test, report, figure, or
upstream file was modified — this report is the only file produced)

**Audit basis.** The 27-point specification audited here is richer than the
Phase 1B brief as executed in this workspace ("produce an equation-audited,
independently implemented and numerically validated Timescape tracker
background… upstream notebook only as a numerical comparison oracle").
Items with no counterpart in the executed brief (notably 6, 18, 20, 22, and
the modular layout of 26) are classified factually against the delivered
work, with that context noted. Verification evidence gathered read-only on
2026-07-15: `pytest -q` → 49 passed; upstream clone clean at
`590c6fd5332a…`; notebook SHA-256 `86d2534d…` unchanged; `main` ==
`origin/main` at `d33f4a0` (Phase 1B uncommitted).

## Summary

| Status | Items |
|---|---|
| COMPLETE | 1, 2, 3, 4, 9, 10, 11, 15, 16, 19, 21, 23, 24, 25, 27 |
| PARTIAL | 5, 8, 12, 13, 14, 17 |
| MISSING | 6, 18, 20, 22 |
| DEVIATED WITH JUSTIFICATION | 7, 26 |
| NOT APPLICABLE | — |

---

## Item-by-item findings

### 1. Independent implementation without copied upstream code — **COMPLETE**

`src/timescape_fsigma8/background.py` is built from hand-derived,
tracker-reduced closed forms that do not appear in the upstream notebook:
`dfv_dt` = f_v(1−f_v)/t, `Q_D` = 2f_v(1−f_v)/(3t²), `rho_d` =
(1−f_v)/(6πGt²), `w_eff` = −(4−f_v)/(8+f_v), `cs2_eff` =
−(2+2f_v−f_v²)/(2+f_v)², `dR_D_dt`, `dQ_D_dt`, `drho_eff_dt`, `dp_eff_dt`.
Upstream instead composes generic expressions (α-coefficient curvature,
morphon U_D/K_D detour, quotient-rule derivative code). Structural
independence: frozen `TrackerParams` dataclass, explicit `G` argument,
vectorised NumPy, no notebook-style globals. Two decisive negatives: our
`cs2_eff` and `dQ_D_dt` *disagree* with upstream (finding D2), impossible
for copied code; agreement elsewhere is at machine precision *through
different algebra* (`reports/background_equation_audit.md` §1, §5).

### 2. Equation inventory completed before implementation — **COMPLETE**

The inventory exists as the equation-by-equation table in
`reports/background_equation_audit.md` §2 (23 rows: symbol → our function →
[GM]/[W09] equation → upstream cell → status). Process evidence that it
preceded implementation: the typeset equations ([GM] pp. 11–13, 23–25
rendered from the PDF; [W09] Eqs. (15)–(20), (38), (B1)–(B12)) were
extracted and cross-checked — including the detection of the Eq. (5.7)
typo (D1) — before `background.py` was written, as recorded in this
session's transcript. *Limitation:* the repository contains no separately
timestamped pre-implementation inventory artifact; the audit table was
written up after the code. The chronology is session-verifiable only.

### 3. Equation-number citations for every scientific function — **COMPLETE**

Mechanical check (read-only script, this audit): of the 30 defs in
`background.py`, all 28 scientific functions/properties cite [GM] and/or
[W09] equation numbers, or are marked "(derived)" with the parent equation
cited and the derivation reproduced in the docstring (`dfv_dt`,
`d2fv_dt2`, `dR_D_dt`, `dQ_D_dt`, `drho_d_dt`, `drho_eff_dt`, `dp_eff_dt`,
and the closed forms inside `Q_D`, `rho_d`, `rho_eff`, `p_eff`, `w_eff`,
`cs2_eff`). The only uncited defs are non-scientific: `__post_init__`
(parameter validation) and `_t` (private array coercion).

### 4. Explicit bare/dressed distinction — **COMPLETE**

Every Hubble-type and density-parameter quantity is explicitly labelled:
`TrackerParams.HD0` ("present-day *bare* (volume-average) Hubble
parameter"), `TrackerParams.H0_dressed`, `from_dressed_H0` (citing the
bare↔dressed relation, [GM] p. 25 / [W09] (B8)–(B9)), `H_D` ("Bare
(volume-average) Hubble parameter"), `Omega_m/R/Q` ("Bare … density
parameter"), `redshift` ("Observed (dressed) cosmological redshift"),
`gamma_w` (the lapse connecting the two). Round-trip test:
`test_dressed_bare_H0_relation`. (Completeness of the *set* of dressed
quantities is item 5.)

### 5. Explicit distinction among t, τ_w, a_D, dressed scale factor, H_D0_bare, H0_dressed — **PARTIAL**

Present and explicit: `t` (volume-average time; module docstring
conventions paragraph), `a_D` (normalisation to a_w,0 = 1 documented in
`TrackerParams.aD0` and `a_D`), `HD0` bare vs `H0_dressed` (item 4).
**Missing:** (a) wall proper time **τ_w** — [W09] Eq. (B12) is not
implemented and τ_w appears nowhere in the package; (b) the **dressed
scale factor** a_w = γ_w⁻¹ a_D ([GM] Eq. (5.4)) exists only implicitly
(computable as `a_D/gamma_w`; referenced inside the `redshift` docstring)
but has no named function. Neither was requested in the executed brief;
both will matter for dressed observables in later phases.

### 6. Immutable PAPER_REFERENCE and NOTEBOOK_REFERENCE presets — **MISSING**

No such presets exist. `TrackerParams` is immutable (`frozen=True`), but
there are no module-level preset instances encoding the paper's parameters
(f_v0 = 0.737, H0 = 73.03 km/s/Mpc) versus the notebook's effective
parameters (f_v0 = 0.737, h = 0.7323 ⇒ 73.23 km/s/Mpc). The 73.03/73.23
ambiguity is documented in both reports (`upstream_reproducibility.md`
§11.1; `background_equation_audit.md` §7.4) but not encoded in code.
Tests hardcode f_v0 = 0.737 with H0 = 1 code units (`tests/conftest.py`).
Not part of the executed brief.

### 7. H_D0 always derived rather than manually inserted — **DEVIATED WITH JUSTIFICATION**

The derivation path exists (`TrackerParams.from_dressed_H0`, citing [GM]
p. 25 / [W09] (B8)) and is used wherever physical values matter
(`tests/conftest.py`; `test_HD0_paper_value`;
`test_dressed_bare_H0_relation` round-trips it to 1e−14). However, the
constructor also accepts `HD0` directly, and two places use that:
`test_void_dominated_Milne_limit` (arbitrary units in a limit test) and
the oracle fixture `oparams` (inserts upstream's own derived `HD0`;
guarded by `test_oracle_constants_consistency`, which checks
`H0_dressed ≈ 1` against the upstream constants). **Justification:** [GM]
Sec. 5.1.1 designates (f_v0, H_D,0) as *the* two free parameters of the
tracker, so accepting H_D,0 directly is specification-faithful; for the
oracle comparison, re-deriving H_D0 rather than using upstream's value
would weaken the consistency check that is instead performed explicitly.

### 8. Audited SI / Gyr / km s⁻¹ Mpc⁻¹ conversions — **PARTIAL**

Audited in reports: `upstream_reproducibility.md` §5 checks G_SI
(4.49e−15 vs reference 4.498e−15 Mpc³/(Gyr²·M☉)), c_SI (306 vs 306.6
Mpc/Gyr), and H0_SI (7.47e−2 Gyr⁻¹ ↔ 73.04 km/s/Mpc). Exercised in tests:
`test_age_of_universe_in_Gyr` (Hubble time 9.778/h Gyr → t0 ≈ 15.38 Gyr)
and `test_HD0_paper_value` (km/s/Mpc). The implementation itself is
deliberately unit-agnostic (t in units of 1/H_D0, explicit `G`; module
docstring "Conventions" paragraph). **Missing:** first-class, individually
audited conversion constants in the package (e.g. km/s/Mpc → Gyr⁻¹); the
9.778 figure is inherited from the upstream convention inside a test
rather than derived from CODATA-grade constants in source.

### 9. Tracker identities and Hamiltonian closure tests — **COMPLETE**

`tests/test_background_identities.py`:
`test_hamiltonian_constraint_3_8`, `test_raychaudhuri_3_9`,
`test_mass_conservation_3_10`, `test_integrability_condition_3_11`,
`test_effective_conservation_3_17`, `test_rho_eff_definition_3_12`,
`test_p_eff_definition_3_13`, `test_w_eff_definition`,
`test_cs2_eff_definition`, `test_omega_definitions_3_18`,
`test_omega_sum_is_unity`, `test_rho_d_scaling_and_normalisation`, plus 8
parametrised analytic-vs-numerical derivative checks. Algebraic identities
at rtol 1e−12; the numerically differentiated Raychaudhuri check at 1e−7.

### 10. Early-time EdS and late-time Milne limits — **COMPLETE**

`test_early_time_EdS_limit` (H → 2/(3t), a ∝ t^{2/3}, Ω_m → 1, w_eff and
c²_s,eff → −1/2, with O(f_v)-scaled tolerances) and
`test_void_dominated_Milne_limit` (f_v → 1: H → 1/t, Ω_R → 1, Ω_m, Ω_Q →
0), in `tests/test_limits_and_reference_values.py`. Note the Milne limit
is exercised via f_v0 = 0.999999 at large t, as documented in the test.

### 11. Analytical rather than finite-difference primary derivatives — **COMPLETE**

All eight derivative quantities are closed-form analytic in
`background.py` (`dfv_dt`, `d2fv_dt2`, `da_D_dt`, `dR_D_dt`, `dQ_D_dt`,
`drho_d_dt`, `drho_eff_dt`, `dp_eff_dt`), as is `cs2_eff`. Finite
differences appear only inside tests, as independent checks
(`num_deriv` central differences; `np.gradient` on oracle samples).

### 12. Exact dressed-redshift derivation and equation source — **PARTIAL**

`redshift` implements [W09] Eq. (38) exactly, citing it and the [GM] p. 25
equivalence (1+z = a_w,0 γ_w / (a_D γ_w,0)) in the docstring; z(t0) = 0 is
tested (`test_present_day_values`). The numerical equivalence of (38) with
the (5.4)-based wall-scale-factor construction was verified in-session
(both give z = 18.586 at 0.218 Gyr) and is asserted in
`background_equation_audit.md` §6. **Missing:** a regression test pinning
`redshift` against the independent `a_D/gamma_w` construction, and a
written step-by-step derivation of (38) from (5.4)+(5.5)+(5.6) (currently
cited, not re-derived).

### 13. z_dressed at t = 0.218 Gyr for both presets — **PARTIAL**

Computed and recorded for the notebook parametrisation only (h = 0.7323):
z ≈ 18.59 (`background_equation_audit.md` §6; addendum to
`upstream_reproducibility.md`). Not computed for a paper preset
(H0 = 73.03), because presets (item 6) do not exist. Not encoded as a test.

### 14. Solved t(z_dressed = 20) for both presets — **PARTIAL**

Solved for the notebook parametrisation only: t = 0.196 Gyr
(`background_equation_audit.md` §6, via Brent root-finding on the
validated `redshift`). Paper preset absent, same reason as item 13.

### 15. Explanation or explicitly unresolved status of the 0.18 / 0.218 Gyr start times — **COMPLETE**

Explicitly unresolved, with measurements: `background_equation_audit.md`
§6 (0.18 Gyr ↔ z ≈ 21.23; 0.218 Gyr ↔ z ≈ 18.59; z = 20 ↔ 0.196 Gyr;
bare-redshift convention also checked and excluded) and §7.3 ("Open
question for the authors"); mirrored in the Phase 1A addendum
(`upstream_reproducibility.md`).

### 16. Comparison against at least 100 upstream sample points — **COMPLETE**

501 samples on [0.18 Gyr, t0], 21 upstream quantities
(`artifacts/upstream/oracle_background.json`, produced by
`scripts/extract_upstream_oracle.py`; verified this audit: 501 points,
upstream commit `590c6fd5332a`, notebook SHA-256 matching UPSTREAM.lock).
All oracle tests compare over the full grid.

### 17. Per-quantity max abs error, max rel error, RMS rel error, worst-discrepancy location — **PARTIAL**

Delivered: per-quantity **maximum relative** difference for all 13
equivalent quantities (table in `background_equation_audit.md` §2, worst
1.5×10⁻¹⁵) and measured deviation statistics (median/range) for the three
D2-affected quantities (§4 table). **Missing:** maximum *absolute* error,
*RMS* relative error, and the *location* (t value) of the worst
discrepancy — none are tabulated in the reports or asserted in tests
(tests use `rtol` bounds only).

### 18. Independent reproduction of Figure 1 for both presets — **MISSING**

No figures are generated from the independent implementation; the package
contains no plotting code. What exists instead is endpoint-value testing
against the published Fig. 1: `test_bare_omegas_today_match_paper_fig1`
(Ω_d, Ω_R, Ω_Q at t0 to ±0.001) and `test_w_eff_today_matches_paper_fig1`;
plus the audit's statement of the *correct* c²_s,eff curve versus the
published (D2-affected) one. Figure reproduction was not in the executed
brief. Note: a faithful reproduction of the published Fig. 1 right panel
is impossible with correct code — the published c²_s,eff curve embeds the
D2 defect; a reproduction task must define which curve is intended.

### 19. Explicit numerical tolerances with no silent relaxation — **COMPLETE**

All tolerances are named module-level constants with written rationale:
`RTOL_EXACT = 1e-12`, `RTOL_NUM = 1e-7` (+ step size) in
`test_background_identities.py` (module docstring, per AGENTS.md rule 9);
`RTOL_ORACLE = 1e-9` with measured values recorded (§5 of the audit
report: observed ≤ 1.5e−15); `GRAD_WINDOW`/`GRAD_RTOL = 1e-3` with the
truncation-error analysis and measured maxima (3.7e−4) in an adjacent
comment. The one recalibration during development (gradient window and D2
thresholds, initially guessed, then replaced by measured values) is
documented in the test docstrings/comments ("measured median 0.035",
etc.) — evidence-based, not silent. Minor nit: the
`test_vs_upstream_oracle.py` module docstring says observed differences
are "~1e-13" while the measured worst is 1.5e−15 (conservative
overstatement, in the safe direction).

### 20. Tests under at least two Python configurations — **MISSING**

Run only under CPython 3.14.3 (`.venv`). Python 3.11 and 3.10 are locally
available via the `py` launcher, so the "if locally available" condition
is met and a second configuration was feasible (requires a second venv
with PyPI installs, as documented for the pip/Artifactory quirk in
CLAUDE.md). No second-configuration run and no documented reason exist in
the repository. Not part of the executed brief.

### 21. reports/background_equation_audit.md — **COMPLETE**

Exists; sections: 1 Method and sources, 2 equation-by-equation audit
table, 3 finding D1, 4 finding D2, 5 validation summary, 6 initial-epoch
timing, 7 open questions.

### 22. reports/background_validation.md with all ten requested sections — **MISSING**

No file of that name exists, and the ten-section outline it should follow
is not on record in this workspace (it was not part of the executed
brief). Validation *content* is currently distributed across
`background_equation_audit.md` §5 (test inventory, tolerances, oracle
statistics), the test suite itself, and §6 (timing checks). Producing the
file requires the ten-section specification.

### 23. No perturbations, closures, fσ8, or likelihoods implemented — **COMPLETE**

Verified by grep over `src/` and `tests/`: no `solve_ivp`, no perturbation
variables, no fσ8/likelihood code (the only textual matches are the
package name `timescape_fsigma8`, a docstring citation of the paper
title, and the phrase "wall-lapse closure" describing γ_w). The
`redshift`/`gamma_w` functions are background observables ([W09] (38),
(B7)), not perturbation machinery.

### 24. Upstream clone remains untouched — **COMPLETE**

Verified this audit: `git -C .reference/… status --porcelain` clean; HEAD
= `590c6fd5332acb15f5683ebf392a0d7ce54983c5` (matches UPSTREAM.lock);
`ACPT_Timescape.ipynb` SHA-256 = `86d2534d…` (matches Phase 1A record and
the oracle's embedded hash). The oracle extractor reads the notebook and
executes upstream cells only in memory
(`scripts/extract_upstream_oracle.py`; nothing written back).

### 25. No commit or push performed — **COMPLETE**

`git status -sb`: `main...origin/main` with no ahead/behind markers; sole
commit remains `d33f4a0` (Phase 1A, committed and pushed earlier at the
user's explicit request). All Phase 1B work is uncommitted working-tree
state (modified: CLAUDE.md, README.md, pyproject.toml,
reports/upstream_reproducibility.md; untracked:
reports/background_equation_audit.md, scripts/extract_upstream_oracle.py,
src/, tests/).

### 26. Modular package structure vs delivered single background.py — **DEVIATED WITH JUSTIFICATION**

Delivered: one scientific module (`background.py`, ~460 lines, 24 public
functions/properties) plus `__init__.py`. A multi-module layout (e.g.
`params` / `units` / `background` / `observables`) was not specified in
the executed brief. **Assessment:** at current scope this is purely
architectural, not a scientific or testability concern — every function
is pure, independently importable, and independently tested; there is no
shared mutable state, and test files already partition by concern
(identities / limits+references / oracle). The deviation *becomes*
structural debt at Phase 1C: parameter presets (item 6), audited unit
constants (item 8), and dressed-observable functions (item 5) each belong
in their own module, and perturbation code must not grow inside
`background.py`. Refactoring later is low-risk precisely because the
functions are pure (AGENTS.md rule 3 applies: any such refactor must be
demonstrably equivalent).

### 27. Defect documentation for D1 and D2 — **COMPLETE**

**D1 (paper Eq. (5.7) curvature prefactor):**
- *Exact source:* [GM] arXiv:2511.17160v2, Eq. (5.7), p. 23, quoted as
  printed in `background_equation_audit.md` §3 (verified against a
  300-dpi render of the typeset PDF equation during the audit).
- *Symbolic derivation:* §3 evidence 1–3 — closure of Ω_d+Ω_R+Ω_Q = 1
  under (5.5)–(5.6) forces ⟨R⟩_D = −6f_v/t²; reduction of [W09]
  (B4)+(B6); algebraic simplification of upstream's α-form to the same.
- *Independent numerical evidence:* oracle agreement of `R_D` to 8e−16;
  Hamiltonian-constraint and Ω-sum identities at 1e−12.
- *Regression tests:* `test_hamiltonian_constraint_3_8`,
  `test_omega_sum_is_unity`, `test_omega_definitions_3_18`, and the
  oracle `RD` row — all four fail if the printed prefactor is adopted.
  (No test *names* D1; coverage is real but indirect.)
- *Confirmed vs interpretation:* classified as a typo (interpretation)
  with the correct form confirmed against three independent sources;
  explicitly flagged for author confirmation (§3 "Implementation
  decision", §7.1; module docstring deviation (D1)).

**D2 (upstream `dQDdt`, notebook cell 6):**
- *Exact source:* cell 6, the three-line code fragment quoted verbatim in
  §4, with the minimum patch (`term1 = A1/A2`) recorded and not applied.
- *Symbolic derivation:* quotient rule spelled out in §4 and in the
  `dQ_D_dt` docstring.
- *Independent numerical evidence:* §4 table — upstream's derivative vs
  d/dt of upstream's *own* Q_D/ρ_eff/p_eff samples (median 54% / 3.4–5.1%
  / 7.9–10.6% off), our closed forms ≤ 3.7e−4 (grid truncation) on the
  same data; integrability (3.11) and conservation (3.17) identities
  hold with ours and fail with upstream's; published Fig. 1 endpoint
  (−0.3452) matches the buggy value to 4 decimals.
- *Regression tests:* `test_dQ_D_dt_matches_oracle_data_not_oracle_code`,
  `test_effective_derivatives_match_oracle_data[drho_eff_dt]`,
  `test_effective_derivatives_match_oracle_data[dp_eff_dt]`,
  `test_cs2_eff_deviation_D2_quantified`,
  `test_cs2_eff_today_documented_deviation_D2` — both endpoints pinned so
  a change in either understanding fails loudly.
- *Confirmed vs interpretation:* the algebra error is **confirmed**
  (upstream's derivative contradicts upstream's own sampled data); the
  *impact on published Fig. 3* is stated as inference pending the
  perturbation phase (§4 "Impact", third bullet) — correctly separated.

---

## A. Blocking omissions before Phase 1C

1. **`reports/background_validation.md`** (item 22) — requires the
   ten-section outline, which is not on record; request it or confirm the
   section list.
2. **Immutable `PAPER_REFERENCE` / `NOTEBOOK_REFERENCE` presets**
   (item 6) — Phase 1C perturbation runs must be parameter-pinned;
   encoding the 73.03/73.23 fork in code prevents silent parameter drift.
3. **Both-preset epoch numbers** (items 13, 14) — z(0.218 Gyr) and
   t(z = 20) under the paper preset; trivial once presets exist.
4. **Per-quantity error-statistics table** (item 17) — max abs, max rel,
   RMS rel, and worst-t location per quantity, emitted to the validation
   report.
5. **τ_w and a_w as named, cited functions** (item 5) — [W09] (B12) and
   [GM] (5.4); dressed observables (and eventually fσ8) depend on them.
6. **Second-Python-configuration test run** (item 20) — 3.11 is locally
   available; one venv + one pytest run, recorded in the validation
   report.

## B. Non-blocking architectural differences

- Single `background.py` vs modular layout (item 26): defer the split to
  the start of Phase 1C (`params`/`units`/`observables`); pure functions
  make it a mechanical, equivalence-testable refactor.
- `TrackerParams` accepting bare `HD0` directly (item 7): justified by
  [GM]'s own parametrisation; keep, but route all *physical* instantiation
  through presets once item 6 lands.
- No first-class audited unit constants (item 8): fold into the modular
  split; derive km/s/Mpc → Gyr⁻¹ from CODATA-grade values rather than the
  inherited 9.778 convention.
- Docstring nit in `test_vs_upstream_oracle.py` ("~1e-13" vs measured
  1.5e−15) — conservative direction; fix opportunistically.
- Missing `redshift` ≡ `a_D/gamma_w` equivalence regression test
  (item 12) — small addition, natural to include with item 5's `a_w`.

## C. Scientific findings requiring human verification

1. **D1** — spurious f_{v,0}^{−2/3} in [GM] Eq. (5.7) (typo per three
   independent lines of evidence; notebook unaffected).
2. **D2** — `dQDdt` algebra error in the upstream notebook; corrupts
   c²_s,eff (−0.3452 published vs −0.3912 correct today), the published
   Fig. 1 right panel (including the w_eff/c²_s,eff curve ordering), and
   quantitatively the barotropic Fig. 3 runs. Consider reporting both to
   the authors.
3. **H0 identity** — 73.03 (paper text) vs 73.23 km/s/Mpc (notebook's
   effective value; consistent with the paper's own H_D,0 ≈ 58.01).
4. **Initial-epoch mismatch** — 0.218 Gyr ↔ z ≈ 18.6, not the stated
   z = 20; 0.18 Gyr background start unexplained.
5. **IC provenance** — the 17-digit initial-condition values' generating
   ΛCDM parameters (Phase 1A §12.4; feeds Phase 1C).
6. **Upstream solver tolerances** — `solve_ivp` defaults throughout the
   notebook (Phase 1A §12.3; convergence study belongs to Phase 1C).

## D. Exact minimal follow-up task list

1. Obtain/confirm the ten-section outline; write
   `reports/background_validation.md` populating it from existing test and
   oracle evidence plus tasks 3–6 below.
2. Add `presets.py` (or equivalent): frozen `PAPER_REFERENCE`
   (f_v0 = 0.737, H0_dressed = 73.03 km/s/Mpc) and `NOTEBOOK_REFERENCE`
   (f_v0 = 0.737, h = 0.7323), each citing its source; route conftest
   fixtures through them.
3. Add audited unit constants (km/s/Mpc ↔ Gyr⁻¹, Hubble time) derived
   from primary values, with a citation and a test.
4. Compute and tabulate z(0.218 Gyr), z(0.18 Gyr), t(z = 20) for both
   presets; add regression tests.
5. Implement `a_w(t)` ([GM] (5.4)) and `tau_w(t)` ([W09] (B12)) with
   citations; add the `redshift` ≡ γ_w/a_D-construction equivalence test.
6. Extend the oracle comparison script/test to emit per-quantity max abs,
   max rel, RMS rel errors and worst-t location; paste table into the
   validation report.
7. Create a Python 3.11 venv, run `pytest -q`, record both configuration
   results in the validation report.
8. Generate Fig.-1-style plots (both panels, both presets) from
   `background.py` only, into a non-upstream artifacts directory (e.g.
   `artifacts/independent/`), noting that the right panel *intentionally*
   differs from the published figure per D2.
9. (Housekeeping) Correct the "~1e-13" docstring nit; add a `[D1]` marker
   comment near the four tests that jointly pin D1.

*No changes were made to any existing file. This report is the audit's
sole output.*

---

## Addendum — gap-closure status (2026-07-15, later the same day)

The historical findings above are preserved unchanged. A dedicated
gap-closure task subsequently addressed the open items; current status
(evidence in `reports/background_validation.md`):

| Item | Was | Now |
|---|---|---|
| 5 (τ_w, a_w named functions) | PARTIAL | **CLOSED** — `background/observables.py`: `a_w`, `tau_w`, `dtau_w_dt`, `dgamma_w_dt`, `H_dressed`, all cited and tested |
| 6 (immutable presets) | MISSING | **CLOSED** — `presets.py`: `PAPER_REFERENCE`, `NOTEBOOK_REFERENCE` (frozen; H_D0 always derived) |
| 8 (audited unit constants) | PARTIAL | **CLOSED** — `units.py` from IAU/exact primaries; upstream 9.778 retained as documented comparison only |
| 12 (redshift equivalence test) | PARTIAL | **CLOSED** — `test_redshift_is_inverse_dressed_scale_factor`, `test_redshift_matches_W09_38` |
| 13/14 (both-preset epochs) | PARTIAL | **CLOSED** — `tests/test_epochs.py`, both presets, documented brentq |
| 17 (full error statistics) | PARTIAL | **CLOSED** — `scripts/compare_to_oracle.py` → `artifacts/independent/oracle_comparison_stats.json` |
| 18 (Fig. 1 reproduction) | MISSING | **CLOSED** — `scripts/make_independent_fig1.py`, both presets + D2 forensic figure (corrected c²_s,eff, labelled) |
| 20 (second Python config) | MISSING | **CLOSED** — suite run under 3.14.3 and 3.11.x (validation report §7) |
| 22 (background_validation.md) | MISSING | **CLOSED** — created with the ten specified sections |
| 26 (modular layout) | DEVIATED | **CLOSED** — `background/` package split; equivalence pinned by `tests/test_refactor_equivalence.py` (golden values from the pre-split module) |
| B (docstring nit, D1 markers) | — | **CLOSED** — oracle-test docstring corrected to the measured ≤ 1.5e−15; `[D1]` markers added to the four pinning tests |
| — (t ≤ 0 handling) | — | **CLOSED** — domain validation with `tests/test_domain_validation.py` |

Section C (scientific findings requiring human verification) is
unaffected: D1, D2, the H0 fork, the z = 20 timing question, IC
provenance, and upstream solver tolerances still await human/author
review.
