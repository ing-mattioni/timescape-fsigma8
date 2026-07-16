# Phase 1C-A — Equation-level audit of the Timescape perturbation systems

**Scope.** Evidence-backed audit of the three linear-perturbation systems used in
arXiv:2511.17160v2 ([GM], Galoppo & Mourier, JCAP 02 (2026) 066) Sec. 4 and
implemented in the pinned upstream `ACPT_Timescape.ipynb` (cells 12–19):
the effective **Mészáros** approximation, the **comoving** closure, and the
**barotropic** closure. The Phase 1B tracker background is treated as validated
and is not modified. The papers are the scientific specification; the upstream
notebook is a read-only reproduction oracle. Machine-readable companion:
[`phase1c_equation_inventory.json`](phase1c_equation_inventory.json).

**Method.** (i) Full transcription of [GM] Secs. 2.1–2.3, 4.1–4.4, 5.1,
Appendices A–B and the reference list from the arXiv v2 PDF (pypdf), with every
sign-critical equation independently re-extracted with pdfminer.six;
(ii) cell-by-cell reading of the pinned notebook and of the three sibling
notebooks (`ACPT_RZA/GMC/GMP.ipynb`) as read-only provenance evidence;
(iii) symbolic verification (sympy 1.14) of every derivation step connecting
the printed equations to the notebook matrices; (iv) numerical forensics for
initial conditions, epochs and wavenumbers (scipy, plus the Phase 1B package
used read-only). No repository code, tests, upstream files or artifacts were
modified; the only new files are the two Phase 1C-A reports. Nothing was
committed.

---

## 1. Variable dictionary (paper ↔ notebook)

[GM] uses the covariant and gauge-invariant (CGI) scalar variables of
Ellis–Bruni–Dunsby ([GM] Eqs. (2.2), (2.20), (2.21)), on the dust frame
(observer = dust, V⁽ᵈ⁾ = F⁽ᵈ⁾ = 0, aµ = 0):

| Paper symbol | Definition | Notebook state | Notes |
|---|---|---|---|
| ∆⁽ᵈ⁾ | a Dᵘ[(a/ϱd) Dµ ϱd] | `v[0]` "Delta_dust" | dust density scalar (∝ comoving Laplacian of ϱd) |
| Z | a Dᵘ[a Dµ Θ] | `v[1]` "Expansion" | expansion-gradient scalar; **Z = −∆̇⁽ᵈ⁾** by (4.14) |
| ∆⁽ᵉᶠᶠ⁾ | a Dᵘ[(a/ρ_eff) Dµ ρ_eff] | `v[2]` "Delta_morphon" | effective-fluid density scalar |
| Ṽ⁽ᵉᶠᶠ⁾ = (1+w_eff)V⁽ᵉᶠᶠ⁾ | rescaled tilt ([GM] p. 16) | — (RZA/GMC use this) | paper's system (4.9)–(4.12) |
| V⁽ᵉᶠᶠ⁾ | unrescaled tilt scalar | `v[3]` "Tilt_morphon" | **the Timescape/GMP notebooks use the unrescaled V** |
| P̃⁽ᵉᶠᶠ⁾ = (1+w_eff)P⁽ᵉᶠᶠ⁾ | rescaled pressure perturbation | eliminated by closure | (4.13): P̃ = c²ₛ ∆⁽ᵉᶠᶠ⁾ |

Background coefficients reduce to their averaged values ([GM] p. 15): ρ⁽ᵈ⁾ →
⟨ϱd⟩_D, ρ⁽ᵉᶠᶠ⁾ → ρ_eff,D, w → w_eff,D, c²ₛ → c²ₛ,eff,D := ṗ_eff/ρ̇_eff,
Θ → 3ȧ_D/a_D, a → a_D. All of these are supplied by the Phase 1B tracker
background (with D1 corrected and D2-correct c²ₛ available).

**Conventions established (all verified):**
- Independent variable: volume-average (bare) time t, code units "HT" where the
  dressed H₀ = 1 (`GyrstoHT = h/9.778`, h = 0.7323 in the notebook).
- Overdot = d/dt along the dust congruence; systems integrated as dv/dt = A(t)v.
- Scale factor in the matrices is a_D(t) normalised so a_w,0 = 1, i.e.
  **a_D(t₀) = 1 + f_v0/2 = 1.3685, not 1** (notebook cell 3 `a0`).
- Laplacian eigenvalue convention ([GM] footnote 8): ⁽³⁾∆ → −k²/a_D².
- Λ = 0, c = 1, K_D = 0 for timescape.
- Solver: `solve_ivp` with **all defaults** (RK45, rtol = 1e-3, atol = 1e-6),
  `t_eval = np.linspace(0.218*GyrstoHT, t0, 1000)` — reproduction-relevant.

## 2. Cell-by-cell mapping of every matrix entry

### 2.1 Mészáros (cell 14) ≡ [GM] (4.27) — VERIFIED EXACT

`delta_ddot = 4πG ρ_d δ − 2H δ̇` with H = Θ/3 is literally
∆̈⁽ᵈ⁾ + (2/3)Θ∆̇⁽ᵈ⁾ − 4πGρ⁽ᵈ⁾∆⁽ᵈ⁾ = 0, Eq. (4.27), on the tracker background.
The IC transformation `ic_new = [ic[0], −ic[1]]` converts Z(tᵢ) to
δ̇(tᵢ) = −Z(tᵢ), consistent with (4.14); the same convention (additionally
divided by ż for z-space integration) appears in ACPT_RZA/GMC — the sign
convention is verified system-wide. [GM] Sec. 5.1.1 stresses this
approximation is *formally inapplicable* in timescape (w_eff < 0, c²ₛ < 0) and
is shown for comparison only. No D2 exposure (uses only Θ, ρ_d).

### 2.2 Comoving closure (cell 13) ≡ [GM] (4.21)–(4.23) — VERIFIED EXACT

Closure (4.20): V⁽ᵉᶠᶠ⁾ ≡ 0, which via (4.12) forces P̃⁽ᵉᶠᶠ⁾ ≃ 0. State
(∆⁽ᵈ⁾, Z, ∆⁽ᵉᶠᶠ⁾); `ic[:-1]` correctly drops the tilt IC.

| Entry | Upstream expression | Paper source | Status |
|---|---|---|---|
| row 1 | (0, −1, 0) | (4.21) ∆̇⁽ᵈ⁾ = −Z | VERIFIED |
| A21 | −4πG ρ_d | (4.23) | VERIFIED |
| A22 | −(2/3)Θ | (4.23) | VERIFIED |
| A23 | −4πG ρ_eff | (4.23) | VERIFIED |
| A32 | −(1+w_eff) | (4.22) | VERIFIED |
| A33 | w_eff Θ | (4.22) | VERIFIED |

The system is scale-independent (no k) exactly as [GM] Sec. 4.3 states.
Sympy checks: (4.24) derives exactly from (4.21)+(4.23); the second-order forms
(4.25) and (4.26) derive exactly from the system plus the background rules
**provided the Raychaudhuri equation carries the standard −Λ** (see finding F5;
irrelevant here since Λ = 0). **No D2 exposure anywhere** (no c²ₛ in any
entry; ρ_eff and w_eff = p_eff/ρ_eff are algebraic in Q_D, ⟨R⟩_D — no time
derivatives). Cosmetic: the cell comment says "4x4" for this 3×3 system.

### 2.3 Barotropic closure (cell 12) ≡ (4.14)–(4.17) in the unrescaled tilt — MAPPED, one unresolved sign

Closure (4.13): P̃⁽ᵉᶠᶠ⁾ = c²ₛ ∆⁽ᵉᶠᶠ⁾. The paper's system (4.14)–(4.17) uses
the rescaled tilt Ṽ; **the Timescape (and GMP) notebooks use the unrescaled
V = Ṽ/(1+w_eff)**, while RZA and GMC implement the paper's Ṽ-form verbatim
(their cell comments say "Tilt_eff*(1+wEff)", A34 = k²/a, A43 = −c²ₛ/a,
A44 = (Θ/3)(3w_eff−1)). The two forms are **exactly equivalent** given the
background identity

  ẇ_eff = −Θ(1+w_eff)(c²ₛ − w_eff),

which follows from the effective conservation law (3.17) and the definition
c²ₛ := ṗ_eff/ρ̇_eff (sympy-verified; this is also precisely how [GM] produce
(4.12) from (4.8) — the change of variable "eliminates the explicit c²ₛ
dependence"). With that identity, rows 3–4 of cell 12 are the exact transform
of (4.15)+(4.17); equivalently row 4 is (4.8) with P⁽ᵉᶠᶠ⁾ = c²ₛ∆⁽ᵉᶠᶠ⁾/(1+w_eff).

| Entry | Upstream expression | Paper source | Status | D2 |
|---|---|---|---|---|
| row 1 | (0, −1, 0, 0) | (4.14) | VERIFIED | – |
| A21 | −4πG ρ_d | (4.16) | VERIFIED | clean |
| A22 | −(2/3)Θ | (4.16) | VERIFIED | clean |
| A23 | −4πG ρ_eff (1+3c²ₛ) | (4.16) | VERIFIED | **corrupted** |
| A32 | −(1+w_eff) | (4.15) | VERIFIED | clean |
| A33 | (w_eff + c²ₛ)Θ | (4.15) **as printed** | see finding F1 | **corrupted** |
| A34 | (k²/a)(1+w_eff) | (4.15) in V-form | VERIFIED | clean |
| A43 | −c²ₛ/(a(1+w_eff)) | (4.8)+(4.13) ≡ (4.17) in V-form | VERIFIED | **corrupted** |
| A44 | (Θ/3)(3c²ₛ − 1) | (4.8) ≡ (4.17) in V-form via the ẇ identity | VERIFIED | **corrupted** |

Sanity check: A34·A43 = −c²ₛk²/a² — the Laplacian pressure term recombines
independently of the tilt normalisation, as it must.

**Every matrix entry of every system is now mapped to a cited equation.** The
single remaining issue is not a mapping gap but a sign inconsistency *within
the paper itself* that the notebooks inherit (next section).

## 3. Finding F1 (candidate D3): the c²ₛ sign in the ∆̇⁽ᵉᶠᶠ⁾ equation

**Classification: INTERNAL INCONSISTENCY CONFIRMED; INTENDED BRANCH UNRESOLVED.**

- **Confirmed fact** (double-extracted with two PDF tools, sympy-verified):
  Eqs. (4.10)+(4.13) imply the coefficient **(w_eff − c²ₛ)Θ** for ∆⁽ᵉᶠᶠ⁾,
  while printed Eq. (4.15) — and all four upstream notebooks via A33 — use
  **(w_eff + c²ₛ)Θ**. The symbolic difference is exactly 2c²ₛΘ∆⁽ᵉᶠᶠ⁾.
- **Unresolved question:** which branch the authors *intended*, and which
  upstream reference equation is authoritative — the paper's (2.22) is quoted
  from Dunsby–Bruni–Ellis (1992) [50], whose full text was **not independently
  inspected in Phase 1C-A**; it remains an explicit external adjudication
  dependency.

Two derivation chains coexist in the printed paper and disagree:

**Chain 1 (Secs. 2, 4.1, 4.4).** (2.22) [quoted from Dunsby–Bruni–Ellis 1992,
ref. [50]] → (4.2) → (4.6) → (4.10):
∆̇⁽ᵉᶠᶠ⁾ − w_eff Θ∆⁽ᵉᶠᶠ⁾ + (1+w_eff)Z **+ ΘP̃⁽ᵉᶠᶠ⁾** − (k²/a)Ṽ⁽ᵉᶠᶠ⁾ ≃ 0.
The `+ΘP̃` sign is forced by F⁽ⁱ⁾ = −(1/a)P⁽ⁱ⁾ in the dust frame (itself the
paper's own (4.8)/(2.24)/(2.11) chain) and was double-extracted with two PDF
tools. Substituting the barotropic closure (4.13) gives coefficient
**(w_eff − c²ₛ)Θ** for ∆⁽ᵉᶠᶠ⁾.

**Chain 2 (Sec. 4.2).** Printed (4.15) has coefficient **(w_eff + c²ₛ)Θ**.
The printed second-order equation (4.19) (and Appendix A, derived from it) is
sympy-consistent with (4.15) as printed.

**The discriminating test.** [GM]'s own Mészáros-section equation (4.29) is
derived from the general system with the adiabatic closure P̃ = w∆ (w = c²ₛ =
const). Sympy verifies that printed (4.29) follows **exactly** (all four state
coefficients zero) from Chain 1's (4.10) — where the closure makes the
∆⁽ᵉᶠᶠ⁾-coefficient cancel — and **fails** against Chain 2 (large residuals in
the ∆⁽ᵉᶠᶠ⁾, Z and Ṽ coefficients). The symbolic difference between the two
chains is exactly 2c²ₛΘ∆⁽ᵉᶠᶠ⁾.

**Who uses what.** All four upstream notebooks implement Chain 2:
A33 = (w_eff + c²ₛ)Θ. So does printed Fig. 3.

**Numerical stakes** (correct c²ₛ, NOTEBOOK preset):

| epoch | w_eff | c²ₛ | (w+c²ₛ) [Chain 2 / notebook] | (w−c²ₛ) [Chain 1] |
|---|---|---|---|---|
| tᵢ = 0.218 Gyr (f_v=0.0382) | −0.4929 | −0.4995 | −0.9923 | +0.0066 |
| t₀ (f_v=0.737) | −0.3735 | −0.3912 | −0.7647 | +0.0178 |

The ∆⁽ᵉᶠᶠ⁾ self-coupling differs by an O(1)Θ term for the entire integration —
the barotropic results (Fig. 3, both panels) depend materially on the branch.

**Resolution status.** The local sources cannot adjudicate: Chain 1 rests on
(2.22), whose fidelity to [50] (Dunsby, Bruni & Ellis, ApJ 395, 54 (1992) —
not available in this repository, full text not independently inspected in
Phase 1C-A) was not verified; Chain 2 is what was published as (4.15) and
computed. Per the audit ground rules, no branch is declared "correct".
Phase 1C-B must expose the branch as a **mandatory explicit argument with no
default**, labelled `"printed_4_15"` (Chain 2, matches the notebooks) and
`"derived_4_10"` (Chain 1), and neither label may be called "correct" in the
public API until author feedback or independent verification against
Dunsby–Bruni–Ellis (1992) (Sec. 10). Evidence examined: pypdf + pdfminer
extractions of (2.9), (2.11), (2.22)–(2.24), (4.2), (4.6), (4.8),
(4.10)–(4.17), (4.19), (4.29); ten sympy consistency checks (inventory,
`verified_derivations`).

## 4. D2 propagation — exact enumeration

D2 (Phase 1B): upstream `dQDdt` (cell 6) computes `term1 = A1*A2` where the
quotient rule requires `A1/A2`, corrupting `dKDdt`, `drhoEffdt`, `dpEffdt` and
hence `cs2Eff = dpEffdt/drhoEffdt`. On the tracker the corrupted sound speed
has the closed form (derived in this audit; c = 1):

  c²ₛ,bug(f) = (18f⁶ − 54f⁵ + 54f⁴ − 18f³ − f² − 2) / (18f⁶ − 54f⁵ + 54f⁴ − 18f³ − f² + 6f + 4)

versus the correct c²ₛ = −(2 + 2f − f²)/(2 + f)². Both share the limits −1/2
(f→0) and −1/3 (f→1); they deviate in between:

| epoch | c²ₛ correct | c²ₛ upstream | rel. err | (1+3c²ₛ) correct | (1+3c²ₛ) upstream |
|---|---|---|---|---|---|
| 0.218 Gyr | −0.49947 | −0.47372 | 5.2% | −0.49842 | −0.42116 |
| 0.196 Gyr | −0.49957 | −0.47606 | 4.7% | −0.49871 | −0.42817 |
| t₀ | −0.39124 | −0.34516 | 11.8% | −0.17371 | −0.03549 |

Note the (1+3c²ₛ) factor entering A23 is distorted by a factor ≈ 4.9 at t₀.

**Complete D2 propagation map:**
- **Barotropic (cell 12): A23, A33, A43, A44 corrupted** (each contains
  `cs2Eff`); A21, A22, A32, A34 clean (`rhod`, `Theta`, `a`, `wEff` only —
  `wEff = pEff/rhoEff` is algebraic, no time derivative, hence clean; `rhoEff`
  likewise).
- **Comoving (cell 13): fully clean.** No entry contains `cs2Eff` or any
  derivative-based quantity.
- **Mészáros (cell 14): fully clean.**
- Upstream `drhoEffdt`/`dpEffdt` are corrupted but enter the perturbation
  systems *only* through their ratio `cs2Eff`.
- Consequently **Fig. 2 (comoving + Mészáros) is D2-free; Fig. 3 (barotropic,
  all three k, both panels) is D2-affected**, consistent with Phase 1B's
  conclusions.
- Subtlety: with the *corrupted* c²ₛ the ẇ identity of Sec. 2.3 fails, so the
  unrescaled-V form (Timescape/GMP) and rescaled-Ṽ form (RZA/GMC) are *no
  longer numerically equivalent* — D2 additionally corrupts A44 in the V-form
  (via c²ₛ) but not in the Ṽ-form (which uses w_eff there). A useful Phase
  1C-B diagnostic.

**D1 relevance.** D1 is a paper-only typo in (5.7) (spurious f_v0^(−2/3) in
⟨R⟩_D); the notebook is unaffected. For Phase 1C it matters only as a warning:
an implementation transcribing paper (5.7) verbatim would corrupt ρ_eff, p_eff,
w_eff, c²ₛ and therefore every effective-fluid matrix entry. The Phase 1B
D1-corrected background must be used.

## 5. Initial conditions — provenance CONFIRMED bit-exactly

Upstream cell 15: `ic = [0.0031427229788258105, −0.16974050039281288, 0, 0]`
assigned to (∆⁽ᵈ⁾, Z, ∆⁽ᵉᶠᶠ⁾, V⁽ᵉᶠᶠ⁾)(tᵢ).

**Confirmed:** the two 17-digit values are reproduced with **exact float64
equality** by the recipe found in `ACPT_RZA.ipynb` (cells 2–4, 16):

  ic[0] = 6.6e−2 · q₊(20),  ic[1] = −6.6e−2 · q̇₊(20),

where q₊(z) is the closed-form flat-ΛCDM growing mode D₊ (incomplete-beta
form) with Planck 2018 parameters **Ωm = 0.315, h = 0.674, H₀ = 1**,
q₊′ the forward finite difference with ε = 1e−5, and q̇₊ = q₊′·(−(1+z)H(z)).
The same hard-coded values appear verbatim in `ACPT_GMC.ipynb`. The paper's
narrative checks out quantitatively: 6.6e−2·q₊(1090) = 6.05e−5 (the "typical
amplitude 6×10⁻⁵" at the CMB), growth factor q₊(20)/q₊(1100) = 52.4, and
∆⁽ᵈ⁾(tᵢ) ≈ 3.1×10⁻³ as stated. ∆⁽ᵉᶠᶠ⁾(tᵢ) = 0 and Ṽ⁽ᵉᶠᶠ⁾(tᵢ) = 0 match
Sec. 5.1.2 exactly (V = Ṽ/(1+w_eff), and 1+w_eff(tᵢ) ≈ 0.507 ≠ 0, so V = 0 ⟺
Ṽ = 0).

**Unresolved (F3) — the Z(tᵢ) unit.** ic[1] is dimensionally a rate in units
of H₀^ΛCDM (h = 0.674), but the Timescape notebook's time unit is 1/H₀^dressed
(h = 0.7323). Unit-consistent conversion gives −0.16974 × (0.674/0.7323) =
**−0.15623**; the notebook injects −0.16974 unchanged (8.65% larger initial
contraction rate than the ΛCDM-matched physical rate). Notably the paper's own
text "Z(tᵢ) ≈ −0.16 H₀" matches the *converted* value (−0.156 → −0.16) better
than the value actually used (−0.170). Intent is ambiguous; both readings will
be quantified in Phase 1C-B. (ic[0] is dimensionless — no issue.)

## 6. Epochs — one explained, one not

- **Cell 9 / Fig. 1 start, 0.18 Gyr (plausible interpretation):** equals the
  flat-ΛCDM (Planck 2018) age at z = 20, t = 0.17906 Gyr (the analytic arcsinh
  form in ACPT_RZA cell 3), rounded. In timescape's own dressed redshift,
  z(0.18 Gyr) = 21.23 — so Fig. 1's "starting from redshift z = 20" holds under
  the ΛCDM-age reading, not the timescape-redshift reading.
- **Cell 15 / Figs. 2–3 start, 0.218 Gyr (UNEXPLAINED, F4):** candidates tested
  (NOTEBOOK preset unless noted): timescape dressed z = 20 → **0.19620 Gyr**
  (and z_dressed(0.218 Gyr) = 18.59); PAPER preset → 0.19674; bare z̄ = 20 →
  0.30330; ΛCDM Planck age at z = 20 → 0.17906; ΛCDM h = 0.7323 age → 0.16480;
  volume time whose *wall* time equals the ΛCDM age → 0.18050; wall time at
  0.218 Gyr → 0.21592. A ΛCDM age of 0.218 Gyr at z = 20 would require
  Ωm ≈ 0.18–0.21 — no canonical parameter set. **No tested definition yields
  0.218 Gyr; author input needed.** An independent implementation following the
  paper's stated prescription (ICs at z = 20) should use tᵢ = t(z_dressed=20)
  = 0.19620 Gyr and treat upstream's 0.218 Gyr as a documented deviation
  (upstream-compat option retained for oracle comparison).

## 7. Wavenumber convention (F7, F8)

[GM] footnote 8 fixes the eigenvalue convention ⁽³⁾∆ → −k²/a²; Fig. 3's caption
puts k "in units of the present-day inverse Hubble length H₀/c as evaluated in
the ΛCDM model [Planck 2018]", calling k = 2π the horizon scale. That claim is
*exactly* realised in ACPT_RZA/GMC, where a₀ = 1 and the length unit is
c/H₀ (h = 0.674). In the Timescape notebook, however, the same numeric values
k ∈ {2π, 5π, 10π} act in k²/a_D² with **a_D(t₀) = 1.3685** and length unit
c/H₀ (h = 0.7323). The present-day physical wavelengths are therefore

| k | λ_phys(t₀) | in units of c/H₀^ΛCDM | caption's nominal |
|---|---|---|---|
| 2π | 5606 Mpc | 1.2596 | 1.00 |
| 5π | 2243 Mpc | 0.5038 | 0.40 |
| 10π | 1121 Mpc | 0.2519 | 0.20 |

— i.e. the "horizon-scale" mode is 26% longer than the ΛCDM horizon (factor =
a_D,0 × h_TS/h_ΛCDM = 1.3685 × 0.9204). Whether this was intended (k defined
against the last-scattering-normalised a_D) or an oversight when porting the k
values between conventions is not determinable from the sources: flagged for
author input; both readings will be reported in Phase 1C-B. The cell 15 comment
"co-moving scale of 150 Mpc/h" (F8) is inconsistent with the paper text, with
the confirmed q₊ provenance (horizon-scale c/H₀ amplitude), and with the k
values; it is classified as a stale comment.

## 8. Additional paper-level findings (no effect on Timescape numerics)

- **F5 — Λ coefficients in (2.12)/(2.13).** Printed (2.12) has "−2Λ" in the
  Raychaudhuri equation; the paper's own derived equations (4.19), (4.25),
  (4.26) are sympy-consistent **only** with the standard "−Λ" (solving for the
  coefficient gives exactly 1 in all three cases). Printed (2.13) has "−2Λ"
  where the standard Hamiltonian constraint requires "+2Λ"; moreover the
  printed pair (2.12)+(2.13) is mutually inconsistent for Λ ≠ 0 (consistency
  of d/dt applied to the constraint requires the (2.13) coefficient to be twice
  the (2.12) one, same sign). Zero impact here (Λ = 0 in timescape; the
  GMC/GMP notebooks never use (2.12)/(2.13) directly).
- **F6 — Fig. 3 right panel** plots ∆⁽ᵉᶠᶠ⁾/k² (y-range 10⁻⁵–10⁰) while
  notebook cell 19 plots raw ∆⁽ᵉᶠᶠ⁾ (10⁻⁴–10⁰) — already recorded in Phase 1A
  (`upstream_reproducibility.md` §11.2); reconfirmed against the v2 caption.
- Appendix A ((A.1)–(A.5), fourth-order dust equation) sits on the Chain 2
  branch and is not used by the notebook; not re-derived symbolically (marked
  not-verified in the inventory). Appendix B (homogeneous-density closure) is
  not implemented in any notebook.

## 9. Classification summary

**Confirmed facts (evidence: exact reproduction or double extraction).**
IC values are 6.6e−2·q₊(20) and −6.6e−2·q̇₊(20), Planck 2018, bit-exact;
notebook state ordering, sign conventions and the Mészáros IC flip; every
matrix entry ↔ equation mapping in Sec. 2; the printed signs of (4.6), (4.10),
(4.13), (4.15); D2 propagation set {A23, A33, A43, A44} and the corrupted-c²ₛ
closed form; solver settings; Λ = 0 irrelevance of F5.

**Verified derivations (sympy PASS; full list in the inventory).**
The ẇ identity; the exact equivalence of the unrescaled-V (notebook) and
rescaled-Ṽ (paper) barotropic systems; (4.16), (4.17), (4.18), (4.19)|Λ=0,
(4.24), (4.25)|λ_Λ=1, (4.26)|λ_Λ=1, (4.28), and (4.29)-from-(4.10);
w_eff = (f−4)/(f+8) and c²ₛ = −(2+2f−f²)/(2+f)² on the tracker.

**Plausible interpretations (consistent but not provable from sources).**
0.18 Gyr = ΛCDM age at z = 20; the paper's "−0.16 H₀" reflecting the
unit-converted Z IC; k ∈ {2π, 5π, 10π} chosen as nominal {1, 0.4, 0.2}× horizon.

**Unresolved questions (author input needed).**
1. **F1/D3 (INTERNAL INCONSISTENCY CONFIRMED; INTENDED BRANCH UNRESOLVED):**
   the inconsistency itself is a confirmed fact — (4.10)+(4.13) imply
   (w−c²ₛ)Θ [`"derived_4_10"`], printed (4.15)/(4.19) and all notebooks use
   (w+c²ₛ)Θ [`"printed_4_15"`]. Unresolved: which branch the authors intended,
   and which upstream reference equation is authoritative. Verification of
   (2.22) against Dunsby–Bruni–Ellis (1992) [50] would adjudicate; [50] was
   not independently inspected in Phase 1C-A (external dependency).
2. **F4:** provenance of tᵢ = 0.218 Gyr (stated z = 20 corresponds to
   0.19620 Gyr).
3. **F3:** intended unit of the Z(tᵢ) IC (−0.1697 unconverted vs −0.1562
   converted).
4. **F7:** intended physical normalisation of k in the timescape run
   (a_D,0 = 1.3685 and h = 0.7323 vs the caption's ΛCDM convention).

## 10. Proposed Phase 1C-B implementation and validation plan (not started)

**Modules** (new package `src/timescape_fsigma8/perturbations/`, background
untouched):
1. `systems.py` — pure, vectorised RHS builders for the three systems on
   `TrackerParams`; the barotropic builder takes a **mandatory explicit**
   `branch ∈ {"printed_4_15", "derived_4_10"}` argument — **no default**, and
   neither label is named "correct" in the public API until author feedback or
   independent verification against Dunsby–Bruni–Ellis (1992) — plus
   `tilt_form ∈ {"unrescaled-V", "rescaled-Vtilde"}`; the package always uses
   the D1/D2-correct background.
2. `ics.py` — the q₊ recipe with **mandatory explicit** choices (no defaults):
   `rate_units ∈ {"upstream_unconverted", "lcdm_to_timescape_converted"}` (F3)
   and `epoch ∈ {"upstream_0p218_gyr", "dressed_z20"}` (F4); wherever a
   wavenumber enters (barotropic runs), the k-normalisation convention (F7)
   must likewise be passed explicitly. **No silent scientific defaults are
   permitted anywhere in the Phase 1C-B API.**
3. `scripts/extract_upstream_perturbation_oracle.py` — execute a patched
   *copy* of the notebook (under `artifacts/upstream/`, documented diff) to
   dump `sol_comoving`, `sol_mezaros`, `sol_bar[k]` arrays as a JSON oracle.
4. `scripts/compare_perturbations_to_oracle.py` — reproduce upstream
   trajectories with `branch="printed_4_15"` (passed explicitly) plus the
   **D2-corrupted c²ₛ reimplemented only inside this forensic comparison
   harness — never in the scientific package** (Phase 1B ground rule,
   preserved unchanged), then isolate one-factor-at-a-time deltas:
   D2-only, F1-branch-only, F3-unit-only, F4-epoch-only.

**Validation gates:**
- Solver-convergence study first (upstream used rtol = 1e-3 defaults; oracle
  comparison must match tolerances before physics comparisons; then tight
  tolerances + Radau/LSODA cross-check for the science runs).
- Tilt-form equivalence test: V-form ≡ Ṽ-form to tolerance with the correct
  c²ₛ (and demonstrably *not* with the corrupted c²ₛ — a D2 diagnostic).
- Early-time checks: comoving ≡ Mészáros while ∆⁽ᵉᶠᶠ⁾ is negligible; EdS
  ∆⁽ᵈ⁾ ∝ t^(2/3) limit as f_v → 0.
- Equation-residual tests: numerical trajectories satisfy (4.18)/(4.24).
- Golden-value regression tests, Python 3.14 + 3.11, following Phase 1B.
- **Gate:** the F1 branch argument is mandatory with **no default** and no
  "correct" label until author feedback or independent verification against
  Dunsby–Bruni–Ellis (1992) [50] — whose full text was not inspected in
  Phase 1C-A and remains an explicit external adjudication dependency; both
  branches shipped and quantified. Same no-default rule for F3 rate units,
  F4 epoch, and F7 wavenumber convention. No fσ8 work.

## 11. Compliance statement

Work performed on branch `phase-1c-perturbations` only. No Phase 1B scientific
code, tests, reports, figures, upstream files (`.reference/`), or generated
artifacts were modified. The upstream notebook was read, never executed or
edited. New files: this report and `reports/phase1c_equation_inventory.json`.
Nothing was committed, pushed, or published; the authors were not contacted.
