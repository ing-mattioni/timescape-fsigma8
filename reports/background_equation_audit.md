# Timescape tracker background — equation audit and independent validation

**Project:** timescape-fsigma8, Phase 1B
**Date:** 2026-07-15
**Deliverable:** [`src/timescape_fsigma8/background.py`](../src/timescape_fsigma8/background.py) + test suite (`tests/`, 49 tests, all passing)

**Verdict:** ✅ The Timescape tracker background is independently implemented
from the published equations and numerically validated. All quantities whose
upstream expressions are algebraically equivalent agree with the upstream
notebook oracle to ≤ 1.5×10⁻¹⁵ relative (machine precision). The audit found
**two defects in the published sources**, both documented below and both
requiring confirmation by scientific review / the authors:

- **(D1)** a typo in the printed Eq. (5.7) of arXiv:2511.17160v2 (spurious
  f_{v,0}^{−2/3} prefactor in ⟨R⟩_D);
- **(D2)** an algebra error in the upstream notebook's `dQDdt` (cell 6),
  which propagates into the published Fig. 1 (right panel) c²_s,eff curve
  and into the barotropic perturbation runs of Fig. 3.

## 1. Method and sources

Scientific specification (implementation source):

- **[GM]** Galoppo & Mourier, JCAP 02 (2026) 066, arXiv:2511.17160v2 —
  Buchert scheme Eqs. (3.6)–(3.18), timescape tracker Sec. 5.1.1
  (Eqs. (5.3)–(5.7) + surrounding text).
- **[W09]** Wiltshire, PRD 80, 123512 (2009), arXiv:0909.0749 — tracker
  solution Eqs. (15)–(20), (38), Appendix B (B1)–(B12).

Numerical comparison oracle (never an implementation source): the pinned
upstream notebook (`UPSTREAM.lock`, commit `590c6fd5…`), background cells
0–8 only, sampled at 501 times on [0.18 Gyr, t₀] by
`scripts/extract_upstream_oracle.py` into
`artifacts/upstream/oracle_background.json` (git-ignored, upstream-derived).

Independence of implementation: our module uses tracker-reduced closed
forms derived by hand from the cited equations (all derivations reproduced
in docstrings), e.g. `ḟ_v = f_v(1−f_v)/t`, `Q_D = 2f_v(1−f_v)/(3t²)`,
`8πG ρ_d = 4(1−f_v)/(3t²)`, `w_eff = −(4−f_v)/(8+f_v)` — none of which
appear in the upstream notebook, which composes generic (non-reduced)
expressions. Agreement between the two routes is therefore a meaningful
cross-check, not a re-typing of the same code.

## 2. Equation-by-equation audit

| Quantity | Our function | Specification | Upstream (cell) | Status |
|---|---|---|---|---|
| f_v(t) | `fv` | [GM] (5.6); [W09] (B2) | `fv` (4) | ✅ identical spec; oracle match 0 ulp |
| ḟ_v | `dfv_dt` = f_v(1−f_v)/t | derived from (5.6) | `dfvdt` (4) | ✅ equivalent; ≤6e−16 |
| f̈_v | `d2fv_dt2` = −2f_v²(1−f_v)/t² | derived | `d2fvdt` (4) | ✅ equivalent; ≤7e−16 |
| a_D(t) | `a_D` | [GM] (5.5); [W09] (B1) | `a` (5) | ✅ ≤4e−16 |
| ȧ_D | `da_D_dt` = a_D·H_D | [GM] (3.6) | `daDdt` (5) | ✅ ≤7e−16 |
| H_D | `H_D` = (2+f_v)/(3t) | [W09] (B6); [GM] (3.6) | `Theta/3` (5) | ✅ ≤8e−16 |
| ⟨Θ⟩_D | `Theta` = 3H_D | [GM] (3.6) | `Theta` (5) | ✅ |
| ⟨R⟩_D | `R_D` = −6f_v/t² | [GM] (5.7) **corrected**; [W09] (B4)+(B6) | `RD` (6) | ⚠️ **(D1)**: paper prints extra f_{v,0}^{−2/3}; upstream & we agree on −6f_v/t²; ≤8e−16 |
| Q_D | `Q_D` = 2f_v(1−f_v)/(3t²) | [GM] (5.7); [W09] (15) | `QD` (6) | ✅ ≤2e−15 |
| d⟨R⟩_D/dt | `dR_D_dt` = 6f_v(1+f_v)/t³ | derived | `dRDdt` (6) | ✅ ≤2e−15 |
| dQ_D/dt | `dQ_D_dt` = −2f_v(1−f_v)(1+2f_v)/(3t³) | derived | `dQDdt` (6) | ❌ **(D2)**: upstream algebra error (median 54% off its own Q_D) |
| ⟨ϱ_d⟩_D | `rho_d` = (1−f_v)/(6πGt²) | [GM] (3.16) + norm. text after (5.7); [W09] (B3) | `rhod` (6) | ✅ ≤2e−15 |
| ρ_eff | `rho_eff` = f_v(8+f_v)/(24πGt²) | [GM] (3.12), K_D=0 | `rhoEff` (8, via morphon UD/KD, cell 7) | ✅ ≤9e−16 |
| p_eff | `p_eff` = −f_v(4−f_v)/(24πGt²) | [GM] (3.13), K_D=0 | `pEff` (8) | ✅ ≤8e−16 |
| dρ_eff/dt | `drho_eff_dt` = −f_v(2+f_v)²/(12πGt³) | derived; equals (3.17) | `drhoEffdt` (8) | ❌ inherits (D2): upstream 3.4–5.1% off its own ρ_eff |
| dp_eff/dt | `dp_eff_dt` = f_v(2+2f_v−f_v²)/(12πGt³) | derived | `dpEffdt` (8) | ❌ inherits (D2): upstream 7.9–10.6% off its own p_eff |
| w_eff | `w_eff` = −(4−f_v)/(8+f_v) | [GM] Sec. 4 text (p:=p/ρ) | `wEff` (8) | ✅ ≤5e−16 |
| c²_s,eff | `cs2_eff` = −(2+2f_v−f_v²)/(2+f_v)² | [GM] Sec. 4 text (ṗ/ρ̇) | `cs2Eff` (8) | ❌ inherits (D2): −0.3912 vs upstream −0.3452 today |
| Ω_d, Ω_R, Ω_Q | `Omega_m/R/Q` | [GM] (3.18); [W09] (B3)–(B5) | cell 9 arrays | ✅ (validated against definitions + sum = 1) |
| γ_w | `gamma_w` = 1+f_v/2 | [GM] p. 25; [W09] (B7) | `a0` (t₀ only, cell 3) | ✅ |
| z(t) | `redshift` | [W09] (38); [GM] p. 25 | — (absent upstream) | ✅ new; z(t₀)=0 exact |
| H_{D,0}(H₀) | `from_dressed_H0` | [GM] p. 25; [W09] (B8) | `HD0` (3) | ✅ |
| t₀ | `TrackerParams.t0` | [W09] after (B5) | `t0` (3) | ✅ |

Conventions audited: c = 1, Λ = 0, K_D = 0 ([GM] Sec. 5 preamble — hence
W_D = ⟨R⟩_D in (3.12)–(3.13)); a_D normalised to a_{w,0} = 1 with
a_{D,0} = 1 + f_v0/2 ([GM] (5.4) + p. 25) — identical to upstream's `a0`.

## 3. Finding (D1): typo in [GM] Eq. (5.7), averaged curvature

**As printed** (arXiv:2511.17160v2, p. 23):
⟨R⟩_D(t) = −6 f_{v,0}^{−2/3} f_v(t)/t².

**Evidence that the f_{v,0}^{−2/3} prefactor is a typo** (correct form
⟨R⟩_D = −6 f_v(t)/t²):

1. **Hamiltonian constraint closure.** With [GM] (5.5)–(5.6), H_D = (2+f_v)/(3t)
   and the printed prefactor, Ω_R = 9 f_{v,0}^{−2/3} f_v/(2+f_v)² and
   Ω_d + Ω_R + Ω_Q ≠ 1, violating [GM] (3.8)/(3.18). Without it the sum is
   exactly 1 (tested to 1e−12 in `test_omega_sum_is_unity`).
2. **Original reference.** [W09] (B4): Ω̄_k = 9f_v/(2+f_v)², which with
   Ω_R := −⟨R⟩_D/(6H_D²) and (B6) gives exactly −6f_v/t².
3. **The upstream notebook itself** implements
   `RD = −6α f_v^{1/3}/a_D²` with α = 9f_v0^{2/3}a_0²H_{D,0}²/(c(2+f_v0))²,
   which simplifies algebraically to −6f_v/t² (we verified both
   symbolically and numerically to 8e−16).
4. The paper's own Fig. 1 (left) matches the notebook output, i.e. the
   *figures* were produced with the correct form.

**Implementation decision:** `R_D` implements −6f_v/t², citing (5.7) with
the documented correction. *Flagged for human/author confirmation.*

## 4. Finding (D2): algebra error in upstream `dQDdt` (notebook cell 6)

Upstream computes, for Q_D = 2ḟ_v²/(3f_v(1−f_v)) :

```python
A1 = 4*(dfvdt(t)*d2fvdt(t))
A2 = 3*fv(t)*(1-fv(t))
term1 = A1*A2          # <-- quotient rule requires A1/A2
```

The first quotient-rule term is (dQ/dt)₁ = 4ḟ_vf̈_v / (3f_v(1−f_v)); the code
**multiplies** by 3f_v(1−f_v) instead of dividing. (The second term is
correct.) The **minimum compatibility patch** to upstream would be the
single-character change `term1 = A1/A2` — recorded here per the audit
protocol, **not applied** to the upstream notebook or to any file of ours.

**Evidence** (all measured against upstream's *own* validated Q_D, ρ_eff,
p_eff samples on the oracle grid, t ∈ [0.1·t₀, t₀]; tests
`test_dQ_D_dt_matches_oracle_data_not_oracle_code` et seq.):

| Quantity | upstream vs d/dt of upstream's own data | our closed form vs same |
|---|---|---|
| dQ_D/dt | median 54% off (range 42–79%) | ≤ 3.7×10⁻⁴ (grid truncation) |
| dρ_eff/dt | 3.4–5.1% off | ≤ 3.3×10⁻⁴ |
| dp_eff/dt | 7.9–10.6% off | ≤ 3.5×10⁻⁴ |

Independent confirmations of our derivative: the integrability condition
[GM] (3.11) `Q̇ + 6HQ + Ṙ + 2H⟨R⟩ = 0` holds identically (1e−12) with our
dQ_D/dt and fails with upstream's; the effective-fluid conservation law
[GM] (3.17) likewise (our `drho_eff_dt` ≡ −3H(ρ_eff+p_eff) exactly).

**Impact on published results:**

- **c²_s,eff ([GM] Fig. 1, right panel).** Upstream's plotted curve runs
  from −0.478 (at 0.18 Gyr) to **−0.3452** today; the correct curve
  (c²_s,eff = −(2+2f_v−f_v²)/(2+f_v)², from the paper's own definition
  ṗ_eff/ρ̇_eff) runs from −0.4996 to **−0.3912**. The published figure's
  endpoint matches the buggy value to 4 decimal places, confirming the
  figure was produced with the defective code. Qualitatively the paper's
  conclusions on that panel survive (both w_eff and c²_s,eff stay negative;
  w_eff is unaffected), but the correct c²_s,eff lies *below* w_eff at all
  times, whereas the published panel shows it *above* — the visual ordering
  of the two curves is an artefact of the bug.
- **Barotropic perturbations ([GM] Fig. 3).** The notebook's barotropic
  system feeds `cs2Eff` into four matrix entries (A23, A33, A43, A44), so
  the Fig. 3 growth curves are quantitatively affected. (The comoving-
  closure and Mészáros runs, Fig. 2, do not use c²_s,eff and are
  unaffected.) Quantifying the effect on Fig. 3 belongs to the
  perturbation phase — **not done here** (background-only scope).
- The energy-balance panel (Fig. 1 left), w_eff, all Ω's, and all
  non-derivative background quantities are unaffected.

## 5. Validation summary

Environment: same as Phase 1A (Python 3.14.3, numpy 2.5.1, scipy 1.18.0);
`pytest -q` → **49 passed**.

| Category | Tests | Tolerance (AGENTS.md rule 9) |
|---|---|---|
| Buchert identities (3.8)–(3.11), (3.17) | 5 | 1e−12 (algebraic); 1e−7 (vs numerical ä) |
| Effective-fluid definitions (3.12), (3.13), w, c²_s | 4 | 1e−12 |
| Analytic derivatives vs central differences | 8 | 1e−7 (step 1e−6·t) |
| Ω definitions (3.18) + sum = 1 + ρ scaling (3.16) | 3 | 1e−12 |
| Normalisations at t₀, dressed↔bare H₀ round trip | 2 | 1e−12…1e−15 |
| Limits: EdS (f_v→0), Milne (f_v→1), unit rescaling | 3 | stated per test |
| Published values: H_{D,0}=58.01, a_{D,0}/a_{w,0}≈1.37, Fig.-1 endpoints, age 15.38 Gyr | 5 | 0.001–0.01 |
| Upstream oracle: 13 equivalent quantities + constants | 14 | 1e−9 (measured ≤ 1.5e−15) |
| Upstream oracle: (D2) deviations pinned | 4 | measured thresholds |

Oracle agreement (max relative difference over 501 samples): f_v exact;
all other equivalent quantities ≤ 1.5×10⁻¹⁵.

## 6. Timing of the initial epoch (resolves Phase 1A uncertainty #2)

Using the tracker dressed-redshift relation [W09] (38) (implemented and
validated as `redshift`; identically 1+z = a_{w,0}γ_w/a_Dγ_{w,0}), with
h = 0.7323:

| Time (Gyr, volume-average) | dressed z | used by notebook for |
|---|---|---|
| 0.180 | 21.23 | background/Ω plots (cell 9) |
| **0.196** | **20.00** | — (nothing) |
| 0.218 | 18.59 | perturbation ICs (cell 15) |

Neither notebook start time corresponds to z = 20 exactly (nor in the
bare a_D-redshift convention: 1+z̄ = a_{D,0}/a_D gives z̄ = 28.9 / 25.3
respectively). The paper states ICs are set at z = 20. The origin of
t = 0.218 Gyr therefore remains unexplained — possibly a ΛCDM-based
conversion. **Open question for the authors.**

## 7. Open questions for scientific review

1. Confirm (D1): Eq. (5.7) curvature prefactor is a typo (evidence §3).
2. Confirm (D2) and its impact on published Figs. 1 (right) and 3
   (evidence §4); the perturbation phase should re-derive Fig. 3 with the
   correct c²_s,eff and quantify the difference.
3. The z = 20 / 0.218 Gyr / 0.18 Gyr timing mismatch (§6).
4. Canonical H₀ (73.03 vs 73.23 km/s/Mpc — Phase 1A finding §11.1,
   still open; all Phase 1B validation used the upstream's effective
   h = 0.7323 and is insensitive to the choice).
5. Independent verification here covers the *background* only. The
   perturbation equations ([GM] Sec. 4) are not yet implemented.

---
*The oracle file and everything under artifacts/upstream/ derive from the
unlicensed upstream notebook and stay local (git-ignored). This report and
the implementation contain no upstream code.*
