# Phase 1G-B — Independent adversarial audit

Classification: `INDEPENDENT_ADVERSARIAL_AUDIT`.
Checkpoint: `6f7937c` (`6f7937ce5681900898f5e0a6482a953f0fa3e5a0`).
Date: 2026-09-29.
Companion: [`phase1g_b_adversarial_audit_inventory.json`](phase1g_b_adversarial_audit_inventory.json).

Audited: the conditional Lagrangian σ(M) runtime (`lagrangian_sigma.py`), its
tests, driver and validation report (including the appended Sec. 14), the
Phase 1G status-additions successor record, `scientific_status.py`, and the
additions-aware 1F-C-R validator.

## 1. Verdict summary

| Item | Value |
|---|---|
| Verdict | `ACCEPT_WITH_CORRECTIONS` |
| Tag readiness | `NOT_READY_OWNER_DECISION_REQUIRED` (one small decision, GB-F1) |
| Findings | 0 HIGH, 0 MEDIUM-HIGH, 0 MEDIUM, 2 LOW-MEDIUM, 8 LOW (10 in total) |

- Every 1G-A number that 1G-B reproduces was recomputed with my own code.
  None of it came from the package. All agree:
  - E, R, ω_m,eff, the wall-law σ and the ΛCDM reference to ≤ 2.1e−11;
  - the CGI-law σ and X to the documented early-start bias (1.1e−6 to
    2.1e−6 relative).
- The equations are correct and correctly cited, with two small citation
  imprecisions (GB-F8).
- The limitation added at `6f7937c` is text only:
  - the masked AST is identical and exactly four string constants differ,
    each extending the old text;
  - every numeric artifact leaf is bit-identical at `8cf5c49` and
    `6f7937c` on both interpreters.
- The six status additions are exactly the 1G-C/1G-D proposals. The record
  is canonical JSON.
- The validator accepts additions only through a registered record. It has
  pre-existing blind spots (GB-F5).
- The Linux failure of `test_top_hat_window_limits_series_and_envelope`
  comes from NumPy's AVX-512 `power` kernel, which is not sign-symmetric.
  The test assumption is at fault, not the numerics (GB-F1).
- The validation report's commit provenance is stale: the recorded
  implementation commit `0883814` is not in the repository (GB-F2).

## 2. Scope and evidence

**Files read in full** (at `6f7937c`, isolated worktree):
- `src/timescape_fsigma8/lagrangian_sigma.py`
- `tests/test_phase1g_b_lagrangian_sigma.py`
- `tests/test_phase1g_status_additions.py`
- `tests/test_barotropic_hadamard_refutation.py` (the validator calls)
- `scripts/validate_phase1g_b_lagrangian_sigma.py` and its artifact
- `reports/phase1g_b_lagrangian_sigma_validation.md` (Secs. 1–14)
- `reports/phase1g_status_additions_successor.md` and its inventory
- `src/timescape_fsigma8/scientific_status.py`
- `scripts/validate_phase1f_c_r_astra_remediation.py`

**Consulted:** 1G-A report Secs. 5–8 and its inventory (for the numbers
only); 1G-C Sec. 10 and 1G-D Secs. 9–11 (for the proposals only); the
`qplus` recipe; and the 1D-B and 1D-C §19 firewall rules. I read no other
adversarial audit.

**Sources** (e-prints in the lead's scratch `sources/`, SHA-256 checked):

| Id | File | SHA-256 |
|---|---|---|
| [GM] arXiv:2511.17160v2 | `main.tex` | `f9cadfa03ecc9a74b0a8f432ae4b13422daeb219f253756bcd877b4b75077c59` |
| [EH98] astro-ph/9709112 | `trans.tex` | `5f2ac6b413df8b738c95f6650152b7e82d7c36f6d9b3a618da540e9739dce17f` |
| [W09] arXiv:0909.0749v2 | `observe.tex` | `2b0324d127440e9a053a7cb37102d7655cca228a63cd2222843e879989b4b531` |
| [P18] arXiv:1807.06209 | `ms.tex` | `fe0833d2d0fda17427a709c9559dc7b3a988b955f47bb7de7a02c900ffdc21cf` |
| [NW15] arXiv:1410.3470 | `cmb1.tex` | `6d0e6397d3877e0aaa3dba16601e1423c4bfe952c7221c1565cdd410d2669bcd` |

**Environment.** Linux x86-64 with AVX-512 (NumPy dispatch targets
`X86_V3`, `X86_V4`, `AVX512_ICL`, `AVX512_SPR`). Two interpreters:
- CPython 3.13.12, NumPy 2.5.3, SciPy 1.18.1;
- CPython 3.11.15, NumPy 2.4.6, SciPy 1.17.1.

**What was run.** My scratch worktrees were at `8cf5c49`, `6f7937c`,
`9157dc4`, `dee72e1` and `462121c`; every run used
`PYTHONPATH=<tree>/src`.

| Run | Result |
|---|---|
| Own recomputation (`audit_b/independent.py`; no package import) | all numbers of Sec. 4.5; identical on both interpreters |
| 1G-B driver at `8cf5c49` and `6f7937c`, both interpreters | 21/21 gates PASS in all four runs; gate lines identical |
| Artifact leaf comparison (4 artifacts) | 1471 int/float leaves bit-identical in every pair; string differences in Sec. 4.7 |
| AST comparison, `8cf5c49` vs `6f7937c` module | masked AST equal; 4 string constants differ, all prefix-extending |
| `pytest` on the 3 in-scope test files, both interpreters | 127 passed, 1 failed (the window test) on each |
| Window test with `NPY_DISABLE_CPU_FEATURES="X86_V4 AVX512_ICL AVX512_SPR"` | passes on both interpreters |
| `validate_phase1f_c_r_astra_remediation.py` at `6f7937c` (3.13) | `PASS`; six additions reported |
| Validator and contract attack scripts | Secs. 4.2 and 4.9 |
| `pytest --collect-only` and the tolerance audit at 5 commits | Sec. 4.11 |
| Equation-number reconstruction from the `.tex` (my counters) | Sec. 4.4 |

## 3. Method and independence statement

- **Independence.** The report, inventory, driver and tests were treated as
  claims under test.
  - The recomputation script imports neither `timescape_fsigma8` nor the
    1G-A evidence script.
  - **Growth law.** I transcribed the growth law from [GM] (4.21)–(4.23)
    and (4.27). The background coefficients are the [W09] Appendix B
    closed forms: (B2) f_v, (B3) Ω̄_M and (B6) H̄. The effective density
    and pressure come from [GM] (3.14) with K_D = 0 and (3.17).
  - **Growth ODE.** It is integrated from t_e = 1e−8, 1e−10 and 1e−12 t0 in
    the normalised variables x1 = Δ_d t^(−2/3), x2 = −Z t^(1/3) and
    x3 = Δ_eff t^(−2/3). The solver is DOP853 with rtol 1e−13.
  - **EH98 and the σ integral.** I transcribed [EH98] from `trans.tex`.
    σ² is a composite 16-point Gauss–Legendre sum on 3000 panels over
    ln k ∈ [ln 1e−7, ln 1e4], with the window W = 3 j1(x)/x from
    `scipy.special.spherical_jn`. The package uses Simpson on
    [1e−6, 300] with the closed-form window.
  - **ΛCDM growth.** g_Λ comes from the Heath integral by adaptive
    quadrature, not from `qplus`.
- **Equation numbers.** Printed numbers are not in the `.tex`. I rebuilt
  them with counters: one number per unstarred display row without
  `\nonumber`, and section or appendix prefixes where the journal style
  uses them. [EH98] Eqs. (4), (26) and (28)–(31) come out as the known
  published numbers.
- **Adversarial tests.** Wrong types, NaN/inf, booleans, strings,
  `Decimal`, `Fraction`, complex input, enum and string spoofing, and every
  barotropic spelling. Forged records, mutation of returned arrays, and
  validator edge cases (deletion, double claims, reordering, snapshot
  tampering).
- **Root cause (claim 5).** Isolated by comparing `np.power` with
  `x*x*x` and libm `pow`, and by turning the AVX-512 dispatch off.

## 4. Claims attacked

### 4.1 Contract compliance with the CLAUDE.md conventions

**Claim** (validation report Sec. 3; module docstring lines 118–121):
- every scientific choice is a mandatory keyword-only argument;
- inapplicable choices are an explicit `NOT_APPLICABLE`;
- records are frozen kw-only dataclasses validated in `__post_init__`;
- arrays are read-only;
- tolerances are explicit.

**Re-examination.**
- All 9 public functions take only mandatory keyword-only arguments.
  `from_reference_preset` does too.
- All 12 public dataclasses are `frozen=True, kw_only=True` with no
  defaults. The only exception is the private `_QuadratureOutcome`.
- Errors are dedicated: `LagrangianSigmaContractError`, its subclass
  `BarotropicClosureRefusedError`, and `LagrangianSigmaNumericalError`.
- Scalar inputs are strict: NaN, inf, bool, `np.bool_`, `Decimal`, str,
  0-d arrays and complex are all refused. `Fraction` is accepted and
  converted.
- Enum spoofing by plain strings is refused. A foreign enum whose value is
  `"NOT_APPLICABLE"` is refused too.
- Returned arrays are read-only copies. A caller can re-enable `writeable`
  on its own copy, but no record holds an array, so this is harmless.
- Tolerances are explicit named constants or arguments.

**Gaps** (GB-F6, GB-F7):
- Array inputs accept `"1.0"` and `True`. Complex arrays are only warned
  about (`ComplexWarning`) and truncated.
- The [EH98] fit range is not enforced: ω_m ≥ 9.83 gives s ≤ 0 silently.
- Records are internally consistent but not bound to a computation. For
  example, `gamma_w0 = 5` or `omega_m_per_photon = 0.3` can be built
  directly.
- `TimescapeGrowthFactor`, a public result, carries no caveat.

**Outcome:** `CONFIRMED_WITH_CAVEAT`.

### 4.2 Barotropic refusal (1G-A Sec. 4.1)

**Claim** (report Sec. 3): the barotropic closure is refused under both laws
with a message citing 1G-A Sec. 4.1.

**Attack.** I tried the closure under `VOLUME_AVERAGE_CGI` and
`WALL_REGIONAL_EDS_COMMON_TIME`, through `conditional_lagrangian_linear_sigma`
and `timescape_growth_factor`, in these forms:
- `GrowthSystem.BAROTROPIC`;
- `"barotropic"`, `" barotropic "`, `"BAROTROPIC"` and `"barotropic\n"`;
- `b"barotropic"`, `"baro-tropic"`, `"printed_4_15"` and `"derived_4_10"`.

**Result.**
- Every string spelling is refused with `BarotropicClosureRefusedError`.
- The other forms are refused with `LagrangianSigmaContractError`.
- `CleanPerturbationSystem` has only `MESZAROS` and `COMOVING`, so no enum
  path reaches a barotropic solve.
- The one remaining route is forging. A caller can build a
  `TimescapeGrowthFactor` with `closure=COMOVING` and any g, then pass it
  through `dataclasses.replace` into a `ConditionalLagrangianSigma`, which
  accepts it (GB-F6). This needs deliberate misuse, and the package's
  other records behave the same way.

**Outcome:** `CONFIRMED_WITH_CAVEAT` (all computation paths refuse).

### 4.3 Naming firewall and status labels

**Claims:**
- CLAUDE.md line 91: "No public name may contain `sigma8`, `sigma_8` or
  `8hMpc`";
- report Sec. 3 and module lines 22–26: no public function/class/member
  name and no output key contains them;
- outputs carry `NON_OBSERVATIONAL` and `NOT_OBSERVATIONAL_SIGMA_8`;
- `SIGMA8_AUTHORIZATION` stays `NOT_GRANTED`.

**Re-examination:**
- No function, class, member or JSON key matches the tokens,
  case-insensitively.
- The 1G-B artifact's keys are clean. Its matching strings are the two
  negative status values and two 1G-A file paths in `provenance`.
- `SIGMA8_AUTHORIZATION` is unchanged, and so are the other `NOT_GRANTED`
  tokens. The validator confirms their frozen equality.
- Status fields refuse relabelling (`_check_statuses`).

**Mismatches** (GB-F4):
- `SIGMA8_STATUS` and `FSIGMA8_STATUS` are public names in `__all__` that
  contain `sigma8` case-insensitively.
- The 1G-B firewall test skips constants (`inspect.isfunction or
  isclass`). The 1D-B growth firewall
  (`test_growth_convergence_purity.py` lines 179–217) lower-cases every
  `__all__` name and would reject both constants.
- 1D-C §19 forbids "any spelling of the observational quantity" in the
  quantity's labels. The wall caveat writes "sigma at 8 h^-1 Mpc", which
  passes a literal-token check.
- All occurrences are negative statements, and the report discloses the
  constant names (Sec. 11 item 2).

**Outcome:** `CONFIRMED_WITH_CAVEAT`.

### 4.4 Equation citations (AGENTS.md rule 2)

**Claim** (report Sec. 4): every implemented equation cites its source
number.

**Re-derived numbers** (from my counters):

| Cited | Source content at the rebuilt number | Verdict |
|---|---|---|
| [EH98] (26) | s = 44.5 ln(9.83/Ω0h²)/√(1+10(Ωbh²)^¾) Mpc, `trans.tex` 682–685 | correct |
| [EH98] (28) | q = (k/h Mpc⁻¹) Θ²_2.7/Γ, line 758 | correct (the code's k Θ²/(Γ_eff h) is the same with k in Mpc⁻¹) |
| [EH98] (29) | T0 = L0/(L0+C0q²), L0 = ln(2e+1.8q), C0 = 14.2+731/(1+62.5q), lines 775–780 | correct |
| [EH98] (30), (31) | Γ_eff, α_Γ, lines 838–844 | correct |
| [GM] (3.6) | H_D = ȧ_D/a_D = ⟨Θ⟩/3, line 364 | correct |
| [GM] (4.13)–(4.17) | barotropic condition and system, lines 507–520 | correct |
| [GM] (4.21)–(4.23) | comoving system, lines 544–548 | correct |
| [GM] (4.27) | Mészáros equation, line 577 | correct |
| [GM] (5.1) | a_D³ = f_v(t_i)a_v³ + f_w(t_i)a_w³, line 624 | correct as "meaning of a_w" |
| [GM] (5.4) | a_w = γ_w⁻¹ a_D, line 641 | correct for a_D0/a_w0 = γ_w0 |
| [GM] (5.4) for γ_w = 1 + f_v/2 | the value is in the text after (5.7), line 663 | imprecise (GB-F8) |
| [W09] (B3), (B8)–(B9); e-print lines 1763–1764 | Ω̄_M = 4(1−f_v)/(2+f_v)²; H–H̄ relation; "a_w = a_w0 t^{2/3}" | correct |

Also checked:
- The [GM] "p. 25" page references cannot be checked from the `.tex`
  (limitation).
- The module docstring's "a_w,reg³ = (1 − f_v) a_D³" leaves out
  1/f_w(t_init), the normalisation of (5.1). It should read "∝" or carry
  the factor (GB-F8).
- The window series coefficients 1, −1/10, 1/280, −1/15120 and 1/1330560
  are correct.
- The next term, −x¹⁰/172972800, keeps the truncation below 5.8e−19 at
  x = 0.1.
- The 4/25 matter-era amplitude re-derives from δ = (2/5)(k/aH)²ζ with
  (aH)² = H100²ω_m/a.

**Outcome:** `CONFIRMED_WITH_CAVEAT`.

### 4.5 Reproduction of the 1G-A numbers

**Claim** (report Secs. 7–8): the package reproduces every 1G-A number.

**Independent values vs the report.** "pkg" is the Linux 3.13 artifact at
`6f7937c`; "indep" is my code.

| Quantity | Report / 1G-A | pkg | indep |
|---|---|---|---|
| g_TS comoving, Mészáros [GM] | 0.40266299, 0.34169420 | 0.402662991, 0.341694199 | 0.402662257, 0.341693481 (t_e→0) |
| g_TS comoving, Mészáros [NW15] | 0.51495288, 0.45856306 | 0.514952876, 0.458563060 | 0.514952313, 0.458562482 |
| X∞ comoving, Mészáros [GM] | 0.699461, 0.593553 | 0.6994611, 0.5935530 | 0.6994599, 0.5935517 |
| X∞ comoving, Mészáros [NW15] | 0.858568, 0.764551 | 0.8585679, 0.7645506 | 0.8585670, 0.7645496 |
| X_wall [GM], [NW15] | 1.112945, 1.200172 | 1.1129452, 1.2001718 | 1.1129452, 1.2001718 |
| g_Λ = qplus(0) | 0.787813 | 0.78781260218560 | 0.78781260218560 |
| H_D0 (paper, notebook, NW15) | 57.8560, 58.0144, 51.6966 | same | 57.85600, 58.01445, 51.69662 |
| ω_m,eff | 0.1204751, 0.1211359, 0.1309372 | same | 0.12047512, 0.12113589, 0.13093723 |
| σ_ΛCDM(EH98) and offset | 0.835689, +3.03% | 0.83568866006 | 0.83568866005, +3.0315% |
| R (a)/(b)/(c) [GM] | 12.5702 / 10.9544 / 10.1041 | same | 12.570168 / 10.954402 / 10.104080 |
| R [NW15] | 12.2260 / 13.1148 / 11.7814 | same | 12.226040 / 13.114754 / 11.781424 |
| E [GM] | 0.9238 / 1.0104 / 1.0634 | same | 0.923799 / 1.010450 / 1.063357 |
| E [NW15] | 0.9602 / 0.9153 / 0.9844 | same | 0.960198 / 0.915339 / 0.984375 |
| σ wall, equal mass [GM], [NW15] | 0.8339, 0.9347 | 0.8339227, 0.9347140 | 0.8339227, 0.9347140 |
| σ CGI comoving, equal mass [GM], [NW15] | 0.5241, 0.6687 | 0.5241018, 0.6686671 | 0.5241008, 0.6686664 |
| f_b 0.12 / 0.20 ([GM], comoving, equal mass) | 0.5607 / 0.4817 | — | 0.560714 / 0.481747 |
| ln g/f_v0 at 1e−4 (comoving, Mészáros) | −0.650034, −0.750041 | −0.6500342, −0.7500408 | −0.6500348, −0.7500418 |

What the comparison shows:
- **27 σ entries at the primary f_b.** Across all three presets, three laws
  and three conventions, pkg and indep agree:
  - to ≤ 2.1e−11 relative for R, E, ω and the wall law;
  - for the CGI laws, to the package's own recorded early-limit bias
    (1.82e−6 / 2.10e−6 for [GM], 1.09e−6 / 1.26e−6 for [NW15]).
- **f_v0 scan.** All 30 X values agree to within one unit of the fourth
  decimal.
- **The first-order coefficients** −13/20, −3/4 and −1/3 of report
  Sec. 4.1 re-derive exactly: α = −19/60 comoving and −5/12 Mészáros.
- **The wall identities** of report Sec. 4.2 hold. The uncorrected limit
  falls below the closed form by −f_v(t_e)/6.

**Precision caveat** (GB-F3). The package starts the growth integral at
t_e = 1e−6 t0, so every CGI value carries a bias of +1.1e−6 to +2.1e−6.
- **All eight six-decimal g and X values** (report Sec. 7.1, 1G-A
  inventory) sit 5.2e−7 to 1.39e−6 from the t_e → 0 limit. That is more
  than half a unit of the printed digit.
- **Three printed four-decimal values** move by one unit at the limit:
  - Sec. 7.3, notebook preset, CGI comoving, bare: 0.60525003, so 0.6053
    becomes 0.6052;
  - Sec. 7.6, X Mészáros at f_v0 = 0.627: 0.7646 becomes 0.7645;
  - Sec. 7.6, X Mészáros at f_v0 = 0.75: 0.5711 becomes 0.5710.
- **So Sec. 9.1's "changes no four-decimal σ" is false for one entry.** The
  reproduction tests (at 5e−7) and the V7 fv0-scan gate lock in the biased
  values: a more accurate start would fail them.
- **The same X flip is in 1G-A's inventory `fv0_scan`** and in its Sec. 5.2
  NW15 Mészáros X (0.7646). I pass this to the lead for the 1G-A audit.

**Evidence class.** Reported: `DERIVED_FROM_VERIFIED_DEFINITIONS` (growth,
ω), `PROVISIONAL_MODEL_IMPORT` (spectrum), `CONVENTION_DEPENDENT` (R).
Assessed: the same, now with independent `NUMERICALLY_CORROBORATED` support.

**Outcome:** `CONFIRMED_WITH_CAVEAT`.

### 4.6 Do the tests compare against independent values?

Partly. The comparisons fall into three groups.

**Same code lineage (not independent):**
- the printed 1G-A values;
- the "full-precision" checks, which reuse `regular_growing_mode_coefficients`
  and `background` through `scripts/phase1g_a_sigma8_path_numerics.py`
  lines 51–54 and 156–180;
- V1–V3 of the driver, for the same reason.

**Re-evaluating the implementation formula (circular):**
- the window "exact" check;
- the f_b = 0 EH98 check.

**Independent:**
- the analytic small-f_v0 coefficients;
- the wall closed form;
- T(k→0) → 1, W(0) = 1 and the series.

The report is transparent about this (Sec. 6: "reproduced by construction
of the same numerics"). My independent recomputation (Sec. 4.5) closes the
gap for this audit (GB-F9).

**Outcome:** `CONFIRMED_WITH_CAVEAT`.

### 4.7 The limitation added at `6f7937c` is text only

**Claim** (report Sec. 14; successor Sec. 3):
- with docstrings stripped and string constants masked, the AST equals
  `8cf5c49`'s;
- exactly four string constants differ, each extending its old text;
- all numeric outputs are bit-identical.

**Re-examination** (my own AST transform, not the validator's):

| Check | Result |
|---|---|
| String constants, old / new | 441 / 441 |
| Constants that differ | 4: `_SCALE_DEPENDENCE_CAVEAT` and the three `_CAVEATS` texts |
| New text starts with the old text | yes, for all four |
| Masked ASTs | equal |
| Docstrings changed | 2 (module and `GrowthLaw`) |
| Dict keys and all other constants | unchanged |

Driver runs at `8cf5c49` and `6f7937c`:
- 21/21 PASS on each interpreter.
- The gate lines are identical across commits and across interpreters.
- The artifact has 1923 leaves: 1421 float, 50 int, 24 bool, 428 str.
- Numeric leaves are bit-identical across commits and across interpreters.
- The strings that differ across commits are:
  - `limitations[5]` and `limitations[6]`;
  - `model_caveat`;
  - `provenance.repository_head`, because my runs were at two committed
    HEADs.

The record's "1494 numeric leaves" matches only if booleans count as
numeric and the one boolean that differed in its pre-commit run is
excluded. I count 1471 non-boolean numeric leaves. This is a counting
convention, not a defect.

**Outcome:** `CONFIRMED`.

### 4.8 Status additions and the successor record

**Claim** (successor Secs. 1–2, 7): six additions, exactly as proposed,
changing no existing token.

**Re-examination:**

| Token | Value | Proposal found in |
|---|---|---|
| `TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW` | `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` | [1G-C] Sec. 10 item 2 |
| `SUPER_CELL_TO_SUB_CELL_GROWTH_TRANSITION` | `NOT_DERIVED` | [1G-C] Sec. 10 item 2 |
| `GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY` | `FAILED_FOR_TIMESCAPE_TRACKER` | [1G-D] Sec. 11 item 1 |
| `TWO_SCALE_SUPER_CELL_GROWTH_LAW` | `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` | [1G-D] Sec. 11 item 1 |
| `VOID_ONSET_RESPONSE` | `EXTERNAL_CLOSURE_INPUT` | [1G-D] Sec. 11 item 1 |
| `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` | `NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY` | [1G-D] Sec. 11 item 1 |

- Each value and evidence section matches the proposal, word for word.
- No existing token changed. The six are absent from the frozen 1F-C-R
  snapshot.
- The 1G-E proposal `TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC` is correctly
  not added.
- The record inventory is byte-canonical: LF, ASCII,
  `indent=2, sort_keys=True`, trailing newline.
- The verbatim approval and its date are identical in the md, the JSON and
  the test.
- The frozen reports and inventories (1F-C-R, 1G-A, 1G-C, 1G-D) are
  byte-unchanged between `8cf5c49` and `6f7937c`. The 1G-B report change
  is append-only (no removed lines).
- **Observation.** The owner's wording is generic ("all the things that
  needed my approval"). The six-token list was resolved by the lead, and
  the record says so openly. The resolution is conservative: it leaves out
  1G-E.
- **Sec. 8 is empty.** It says "see the inventory's `validation` block",
  but the inventory has no such key (GB-F10).

**Outcome:** `CONFIRMED_WITH_CAVEAT`.

### 4.9 Validator extension

**Claim** (successor Sec. 5): additions are accepted only through a
registered record, with six new named failure modes and five kept ones.

**Attacks** (on `check_current_scientific_status`):

| Attack | Result |
|---|---|
| Undeclared addition; new live token with no record | rejected (named) |
| Addition already in the frozen snapshot | rejected (named) |
| Live value differs from the record | rejected (named) |
| Addition missing from live; token both changed and added | rejected (named) |
| Double claim by two records | rejected (named) |
| `SIGMA8_AUTHORIZATION` → `GRANTED` with no record | rejected |
| Registry order reversed | same result (no order dependence) |
| **Frozen token deleted from the live module** (`D3_VERDICT`, `SIGMA8_AUTHORIZATION`) | **accepted silently** |
| Change record naming a token absent from the snapshot | bare `KeyError`, not a named assertion |
| In-tree edit of the frozen inventory (content not pinned to `REMEDIATION`) | not detected; only canonical bytes are checked |
| `reports/*.json` "round-trip" loop | checks idempotence only, not canonical bytes |

- These gaps are pre-existing: the live-only loop dates from `72d8c51`. The
  extension did not widen them. At this checkpoint the new pytest set
  equality (`test_six_added_tokens_hold_the_approved_values`) catches a
  deletion, but the validator does not (GB-F5).
- The tests exercise every failure mode they claim, asserted by message.
- The validator itself passes at `6f7937c`.

**Outcome:** `CONFIRMED_WITH_CAVEAT`.

### 4.10 Linux platform failure

**Claim tested:** `test_top_hat_window_limits_series_and_envelope` line 428
asserts `np.array_equal(W(−x), W(x))` bitwise.

**Root cause, confirmed.**
- sin is exactly odd and cos exactly even. `x*x*x` and `math.pow` are
  exactly odd.
- NumPy's vectorised `x ** 3` (`np.power`) is not sign-symmetric here:
  - 51 of the test's 997 cubes differ by 1 ulp between `(−x)**3` and
    `−(x**3)`;
  - 46 W values differ, by ≤ 3.3e−16 relative.
- Positive bases take the `X86_V4` (AVX-512) SIMD kernel, which has up to
  0.61 ulp error. Negative bases are correctly rounded (≤ 0.4961 ulp).
- With `NPY_DISABLE_CPU_FEATURES="X86_V4 AVX512_ICL AVX512_SPR"`, the
  mismatch count drops to 0 and the test passes on both interpreters.
- Both interpreters show the same failure.

**Who is at fault.** The implementation is numerically correct: W is
accurate to a few ulp, and the physics uses x = kR > 0 only. The test
relies on undocumented library behaviour (AGENTS.md rule 9). It passes on
the owner's Windows build and fails here.

**Minimal fixes** (owner decision OD1; neither applied):
- **A (test only).** Replace line 428 with
  `np.testing.assert_allclose(ls.top_hat_window(x=-x), ls.top_hat_window(x=x), rtol=1e-15, atol=0.0)`.
  The comment should say that `np.power` is not guaranteed sign-symmetric
  (1 ulp measured on Linux AVX-512 builds).
- **B (implementation, output-preserving).** In `top_hat_window`, evaluate
  the closed form on `xl = np.abs(arr[~small])`.
  - W is even, so this makes evenness exact by construction.
  - I verified bit-identical outputs for all x > 0, over 2.0e5 points in
    [1e−9, 1e4] plus the test grid. Every artifact number therefore stays
    bit-identical.
  - The bitwise test can then stay.
  - AGENTS.md rule 3 still asks for the equivalence to be recorded.

**Outcome:** `CONFIRMED` (root cause); the test assumption is at fault.

### 4.11 Validation-report claims (gates, tests, environments, provenance)

| Claim | Check | Outcome |
|---|---|---|
| 21 gates, with the n per gate of Sec. 8 | every n matches the artifact; all PASS on Linux (e.g. V1 5.1e−13, V5 invariance 9.0e−12, V7 table 4.99e−5) | confirmed |
| 92 tests (Sec. 10) | 92 collected | confirmed |
| Truncation envelopes ≤ 5.8e−12 | max 5.80e−12 over 66 values | confirmed |
| "92 passed" | 91 pass on Linux (GB-F1) | platform caveat |
| Windows 3.14.3 / 3.11.9 runs | cannot be run here | not verified |
| Implementation commit `0883814`, parent `462121c` (Sec. 1) | `0883814` does not exist; the module is `3834a63` with parent `dee72e1`, the report is `9157dc4` | refuted (GB-F2) |
| Tolerance audit "626 = 583 + 43" (Sec. 10) | `tests/` count is 583 at `462121c`, 590 at `dee72e1`, 633 at `9157dc4` (590 + 43) | true of the pre-rebase tree only (GB-F2) |
| Suite "916 + 92 = 1008 = 978 + 30" (Sec. 12) | collected: 916 at `462121c`, 924 at `dee72e1`, 1016 at `9157dc4`, 1044 at `6f7937c` | true of the pre-rebase tree only (GB-F2) |
| Sec. 9.1 "changes no four-decimal σ" | one printed σ moves 0.6053 → 0.6052 | refuted (GB-F3) |
| Sec. 2 "nothing imports it" | only its test, the status test and its driver import it | confirmed |

## 5. Findings

| Id | Severity | Resolution class | Title |
|---|---|---|---|
| GB-F1 | LOW-MEDIUM | OWNER_DECISION | Window evenness test asserts bitwise sign symmetry of `np.power`; fails on Linux AVX-512 |
| GB-F2 | LOW-MEDIUM | UNAMBIGUOUS_ERRATUM | Validation report records a non-existent implementation commit and pre-rebase counts |
| GB-F3 | LOW | UNAMBIGUOUS_ERRATUM | "Changes no four-decimal σ" is false; six-decimal g/X carry the t_e bias |
| GB-F4 | LOW | OWNER_DECISION | Naming-firewall wording (CLAUDE.md line 91) is broader than what is enforced |
| GB-F5 | LOW | OWNER_DECISION | Status validator: deletions and snapshot edits pass; one bare `KeyError` |
| GB-F6 | LOW | OWNER_DECISION | Contract-hardening gaps: array coercion, EH98 range, forgeable records |
| GB-F7 | LOW | OWNER_DECISION | Public `TimescapeGrowthFactor` results do not carry the growth-law limitation |
| GB-F8 | LOW | UNAMBIGUOUS_ERRATUM | Docstring citation of γ_w = 1 + f_v/2 as "Eq. (5.4)"; missing 1/f_w(t_init) |
| GB-F9 | LOW | OWNER_DECISION | Reproduction tests are same-lineage regressions; no independent implementation |
| GB-F10 | LOW | UNAMBIGUOUS_ERRATUM | Successor record Sec. 8 points to a `validation` block that does not exist |

**Details.**
- **GB-F1.** See Sec. 4.10. The phase's "92 passed" does not hold on
  Linux x86-64 with AVX-512 on either interpreter. A Linux session's
  preflight (CLAUDE.md, "How work is organised" item 1) fails at this
  checkpoint.
- **GB-F2.** Proof: `git log --format='%h %p'` shows `3834a63` with parent
  `dee72e1`, and `9157dc4` with parent `3834a63`. `git cat-file -t 0883814`
  fails. The counts are in Sec. 4.11. The numbers of the report are
  unaffected, but the validated checkpoint recorded in it is not the
  committed one.
- **GB-F3.** See Sec. 4.5. No scientific conclusion changes. The quantities
  shift by about 2e−6 relative, well within the declared 1e−4 budget.
- **GB-F4.** See Sec. 4.3.
- **GB-F5.** See Sec. 4.9. The gaps are pre-existing, and the pytest set
  equality currently covers deletion.
- **GB-F6.** See Secs. 4.1 and 4.2. The EH98 validity range is in
  `trans.tex` lines 686–687 (0.025 ≲ Ω0h² ≲ 0.5, Ωbh² ≳ 0.0125) and 855–856
  (no-wiggle form poor for Ωb/Ω0 ≳ 0.5). The production inputs are inside
  it: ω_m 0.120–0.143, ω_b ≥ 0.0145.
- **GB-F7.** The 1G-D limitation (not Timescape's long-wavelength growth)
  applies to g and X, but `TimescapeGrowthFactor.to_json_dict()` and the
  driver's `V1_growth` export them with no caveat. Adding a caveat field is
  a code change beyond the approved text-only scope.
- **GB-F8.** See Sec. 4.4.
- **GB-F9.** See Sec. 4.6.
- **GB-F10.** See Sec. 4.8. Successor Sec. 3 also points to "(Sec. 8)".

## 6. Proposed errata

The frozen texts are not edited. The lead applies these through a dated
successor note.

1. **GB-F2** — `reports/phase1g_b_lagrangian_sigma_validation.md`, Sec. 1,
   lines 23–26.
   - Old: "- **Parent checkpoint:** `462121c` (Phase 1G-A). Branch
     `phase-1g-b-lagrangian-sigma` (local, unpushed, untagged).
     - **Implementation commit:** `0883814` (module, tests, validation
     driver). This report is committed on top of it."
   - New: "- **Parent checkpoint:** `dee72e1` (Phase 1G-A barotropic status
     record; child of `462121c`). Branch `phase-1g-b-lagrangian-sigma`
     (local, unpushed, untagged). - **Implementation commit:** `3834a63`
     (module, tests, validation driver); this report is `9157dc4`. The runs
     of Secs. 10 and 12 were made on a pre-rebase commit `0883814` (parent
     `462121c`) that is not in the repository history."
   - Proof: `git log --format='%h %p'`; `git cat-file -t 0883814` fails.
2. **GB-F2** — same file, Sec. 10, lines 353–355.
   - Old: "The tolerance audit (`scripts/audit_numerical_tolerances.py`)
     now counts 626 comparisons, 583 before plus 43 new, with none missing
     a tolerance."
   - New: "The tolerance audit (`scripts/audit_numerical_tolerances.py`)
     counts 633 comparisons in `tests/` at `9157dc4`: 590 at the parent
     `dee72e1` plus 43 new (626 = 583 + 43 on the pre-rebase tree). None is
     missing a tolerance."
   - Proof: `audit(Path("tests"))` gives 583 at `462121c`, 590 at `dee72e1`
     and 633 at `9157dc4`, with 0 missing.
3. **GB-F2** — same file, Sec. 12, lines 448–449.
   - Old: "The 1G-A base recorded 916 passed with every input present; 916
     + 92 new = 1008 = 978 + 30."
   - New: "The 1G-A base recorded 916 passed with every input present; 916
     + 92 new = 1008 = 978 + 30. These counts are for the pre-rebase tree
     (parent `462121c`). The committed checkpoint `9157dc4` (parent
     `dee72e1`, which adds 8 tests) collects 1016 tests = 924 + 92, and no
     full-suite run of it is recorded here."
   - Proof: `pytest --collect-only` gives 916 at `462121c`, 924 at
     `dee72e1` and 1016 at `9157dc4`.
4. **GB-F3** — same file, Sec. 9.1, lines 329–330.
   - Old: "This is inside the declared 1e−4 early-limit budget of [1G-A]
     and changes no four-decimal σ."
   - New: "This is inside the declared 1e−4 early-limit budget of [1G-A].
     At the t_e → 0 limit, three printed four-decimal values move by one
     unit in the last digit:
     - σ for the [GM] notebook preset, CGI comoving, bare convention
       (Sec. 7.3: 0.60525003 → 0.6052489, i.e. 0.6053 → 0.6052);
     - X for CGI Mészáros at f_v0 = 0.627 (0.7646 → 0.7645, Sec. 7.6);
     - X for CGI Mészáros at f_v0 = 0.75 (0.5711 → 0.5710, Sec. 7.6).

     Every six-decimal g and X of Sec. 7.1 carries the same bias. The
     limits are:
     - g = 0.402662 / 0.341693 ([GM]) and 0.514952 / 0.458562 ([NW15]);
     - X = 0.699460 / 0.593552 ([GM]) and 0.858567 / 0.764550 ([NW15]),
       each pair comoving / Mészáros."
   - Proof: independent integration (Sec. 4.5). The package's own
     `log_growth_early_limit_linear_bias_estimate` gives the same limits,
     to 1e−9.
5. **GB-F8** — `src/timescape_fsigma8/lagrangian_sigma.py` docstrings (text
   only; the masked AST is unchanged).
   - Line 1083. Old: "In both, ``gamma_w0 = 1 + f_v0/2`` ([GM] Eq. (5.4))."
     New: "In both, ``gamma_w0 = 1 + f_v0/2`` ([GM] text after Eq. (5.7);
     Eq. (5.4) defines ``a_w = gamma_w^-1 a_D``)."
   - Line 1177. Old: "``gamma_w0 = 1 + f_v0/2`` ([GM] Eq. (5.4))". New:
     "``gamma_w0 = 1 + f_v0/2`` ([GM] text after Eq. (5.7))".
   - Line 49. Old: "a_w,reg^3 = (1 - f_v) a_D^3 proportional to t^2". New:
     "a_w,reg^3 = (1 - f_v) a_D^3 / f_w(t_init) proportional to t^2".
   - Proof: [GM] `main.tex` line 641 is (5.4), a_w = γ_w⁻¹ a_D. Line 663
     states γ_w = 1 + f_v/2. Line 624 is (5.1), whose normalisation gives
     a_w³ = (1 − f_v) a_D³/f_w(t_init).
6. **GB-F10** — `reports/phase1g_status_additions_successor.md`, Sec. 8,
   line 223.
   - Old: "Filled in after the runs; see the inventory's `validation`
     block."
   - New: "Not filled in: the companion inventory has no `validation`
     block. The full-suite result for this checkpoint is recorded only in
     CLAUDE.md ("1044 passed on Windows, Python 3.14.3 and 3.11.9"). The
     1G-B driver comparison is in Sec. 3."
   - Also, lines 119–121. Old: "the driver's
     `working_tree_changes_present` flag (Sec. 8)." New: "the driver's
     `working_tree_changes_present` flag."
   - Proof: the inventory's top-level keys do not include `validation`.

## 7. Items for owner decision

- **OD1 (GB-F1, blocks tagging).** Choose one fix for the Linux window
  test, then re-run on Linux and Windows:
  - A: a test-only relative tolerance of 1e−15, atol 0, with the reason
    documented;
  - B: the closed form on |x|, bit-identical for x > 0, keeping the
    bitwise test.

  I recommend B; A is acceptable if the module must not change.
- **OD2 (GB-F4).** Choose one:
  - amend CLAUDE.md line 91 to "no public function, class, member or
    output-key name; negative status constants and values excepted";
  - or rename `SIGMA8_STATUS` / `FSIGMA8_STATUS` (an API change).

  I recommend the wording amendment. Also decide whether 1D-C §19's "any
  spelling" rule applies to caveat text.
- **OD3 (GB-F5).** Harden `check_current_scientific_status`:
  - reject frozen tokens missing from the live module, unless a registered
    removal covers them;
  - raise a named assertion for a change naming a token absent from the
    snapshot;
  - pin the frozen inventory to `git show REMEDIATION:<inventory>`;
  - optionally, byte-check successor records for canonical form.
- **OD4 (GB-F6).** Optionally:
  - type-check array inputs and refuse str, bool and complex;
  - enforce or document the EH98 validity range;
  - add record invariants: γ_w0 = 1 + f_v0/2, a recomputed per-photon
    closed form, and radius consistency.
- **OD5 (GB-F7).** Decide whether `TimescapeGrowthFactor` should carry the
  growth-law caveat. This is a code change outside the approved text-only
  scope.
- **OD6 (GB-F9).** Optionally add an independent regression test, e.g. the
  normalised-variable ODE of Sec. 3, for g_TS at one f_v0.

## 8. Verdict and readiness for tagging

**Verdict: `ACCEPT_WITH_CORRECTIONS`.**
- No finding touches an equation, a status token, a load-bearing number or
  an interpretation.
- Every 1G-A number is reproduced by an independent implementation.
- The text-only claim of `6f7937c` holds exactly.

**Tag readiness: `NOT_READY_OWNER_DECISION_REQUIRED`.**
- One decision blocks the tag: OD1. The phase's own test suite fails on a
  supported platform class, Linux with AVX-512, on both interpreters.
  Freezing it would break Linux preflights of later phases.
- Choosing fix A or B is small.
- After that decision, and after the errata of Sec. 6 are recorded, the
  phase is ready to tag. OD2–OD6 do not block.

## 9. Limitations

- I could not run the Windows 3.14.3 / 3.11.9 environments. Their gate
  values and test results are taken from the report and not verified.
- The [GM] page references ("p. 25") cannot be checked from the `.tex`
  source.
- Equation numbers are rebuilt with my counters. For [EH98] they reproduce
  the known published numbering. For [GM] and [W09] they depend on the
  counters being right for `align` rows with nested environments. I
  inspected every row cited here.
- EH98 was checked by an independent transcription and quadrature, not
  against a Boltzmann code or published tables (none is offline). The
  EH98 → Boltzmann bias is taken from the report, which calls it
  provisional.
- I did not run the full test suite (the lead does). I ran only the three
  in-scope test files, collect-only counts, and the 1G-B and 1F-C-R drivers.
- I did not audit the scientific content of 1G-C and 1G-D beyond matching
  the proposed tokens to the record.

## 10. Preservation statement

- In the main tree I created only this report and its inventory.
- I edited, staged, committed, pushed or tagged nothing else. The
  `AUDIT_TREE` worktree was only read.
- Every other file I made is in my scratch directory `audit_b/`:
  - scripts, run logs and artifacts;
  - a `.reference` symlink inside my own scratch worktree;
  - five detached scratch worktrees (`8cf5c49`, `6f7937c`, `9157dc4`,
    `dee72e1`, `462121c`), added with `git worktree add` as the brief
    allows, and removed again at the end of the audit.
