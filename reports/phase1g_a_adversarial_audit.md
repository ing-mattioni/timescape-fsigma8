# Phase 1G-A — Independent adversarial audit

Audit classification: `INDEPENDENT_ADVERSARIAL_AUDIT`.
Checkpoint: `6f7937c` (`6f7937ce5681900898f5e0a6482a953f0fa3e5a0`, `main` at the
start of the audit session). Date: 2026-09-29.
Machine-readable companion:
[`phase1g_a_adversarial_audit_inventory.json`](phase1g_a_adversarial_audit_inventory.json).

Audited record: [`phase1g_a_sigma8_derivation_path_audit.md`](phase1g_a_sigma8_derivation_path_audit.md)
("[1G-A]") and its inventory, the evidence script
`scripts/phase1g_a_sigma8_path_numerics.py` and its artifact, the status
successor record
[`phase1g_a_barotropic_status_successor.md`](phase1g_a_barotropic_status_successor.md)
("[SUCC]") and its inventory, and `tests/test_barotropic_hadamard_refutation.py`.

References: [GM] Galoppo & Mourier, arXiv:2511.17160v2; [W09] Wiltshire,
arXiv:0909.0749v2; [W07] arXiv:0709.0732v2; [EH98] Eisenstein & Hu,
astro-ph/9709112; [NW15] Nazer & Wiltshire, arXiv:1410.3470; [P18] Planck 2018
VI, arXiv:1807.06209.

## 1. Verdict summary

- **Verdict:** `ACCEPT_WITH_CORRECTIONS`.
- **Tag readiness:** `NOT_READY_OWNER_DECISION_REQUIRED`. Three findings need
  an owner decision recorded in a dated successor note. None needs a code,
  equation, tolerance or token change.
- **Findings:** 11 in total. HIGH 0, MEDIUM-HIGH 0, MEDIUM 2, LOW-MEDIUM 1,
  LOW 8.

The load-bearing results survive. I re-derived them from the LaTeX sources
with my own code, which imports nothing from `timescape_fsigma8`:

- The barotropic closure is Hadamard ill-posed on the Timescape tracker. The
  corrected sound speed is negative for the whole tracker history, not only
  after z = 20. My closed form is `c²_s,eff = −(2 + 2f_v − f_v²)/(2 + f_v)²`,
  which lies in [−1/2, −1/3). α = 1.7069482 and all ten slopes reproduce to
  ≤ 2e−10. The approved token change `REFUTED_HADAMARD_ILL_POSED` is supported.
- Every σ-chain number reproduces to the printed digits. This covers ω_m,eff,
  g_TS, X∞, X at finite z_i, the f_v0 scan, EH98, the Planck validation, E,
  the radii, the σ table and X_wall.
- A Boltzmann code (CAMB 2.0.4) reproduces the [P18] anchor σ8 = 0.8111. It
  shows that the EH98 bias cancels in the anchored ratios to ≤ 0.5%.

The two MEDIUM findings:

- **GA-F1.** The homogeneous-density closure of [GM] App. B is called
  "backward-parabolic, ill-posed". That holds for the *printed* (B.3)–(B.5)
  only.
  - Printed (B.4) follows from (B.2) + (4.10) + (4.12) only with the
    `printed_4_15` sign of the ΘP̃ term, which is the D3 sign.
  - Under the project's adjudicated `D3_VERDICT = RESOLVED_DERIVED_4_10`,
    (4.10) becomes an algebraic constraint. The closure is then well-posed,
    and its growth tends to the Mészáros growth at high k.
- **GA-F2.** Planck's baryon fraction is justified as "the primary closure"
  by a misreading of [NW15]. [NW15]'s own Timescape CMB fit has f_b ≈ 0.18
  and n_s ≈ 0.99, so the "[NW15]" row mixes an [NW15] background with a
  Planck early universe. The primary [NW15] σ values would drop by 4–5%. That
  is inside the report's own f_b band.

## 2. Scope and evidence

**Files read in full at `6f7937c`:**
- `reports/phase1g_a_sigma8_derivation_path_audit.md` (556 lines) and
  `reports/phase1g_a_sigma8_derivation_path_inventory.json`;
- `scripts/phase1g_a_sigma8_path_numerics.py` (489 lines) and
  `artifacts/independent/phase1g_a_sigma8_path.json` (copied in; SHA-256
  `1b7194da…3dab95fc`);
- `reports/phase1g_a_barotropic_status_successor.md` and its inventory;
- `tests/test_barotropic_hadamard_refutation.py`;
- `AGENTS.md` and `CLAUDE.md`.

**Consulted for cross-checks:**
- 1D-A §10 and 1D-C §§5, 30, 34;
- 1C-A §8 (App. B was never re-derived there);
- the F1 growing-mode validation report (line 48);
- `scientific_status.py` and the `growing_mode.py` docstring;
- `git log` and `git diff` of the 1G-A files (462121c → 214a626 → 6f7937c).

**Primary sources.** These are the e-prints the lead supplied in the
session scratchpad. I checked every SHA-256 of the `.tex` files and all match:

| id | file | SHA-256 |
|---|---|---|
| [GM] | `2511.17160v2/main.tex` | `f9cadfa03ecc9a74b0a8f432ae4b13422daeb219f253756bcd877b4b75077c59` |
| [W09] | `0909.0749v2/observe.tex` | `2b0324d127440e9a053a7cb37102d7655cca228a63cd2222843e879989b4b531` |
| [W07] | `0709.0732v2/solution.tex` | `221662c987e454729ef8202c87fa697c5882b5b7daaecdedb50a7cba8ffe6cd8` |
| [EH98] | `astro-ph_9709112/trans.tex` | `5f2ac6b413df8b738c95f6650152b7e82d7c36f6d9b3a618da540e9739dce17f` |
| [NW15] | `1410.3470/cmb1.tex` | `6d0e6397d3877e0aaa3dba16601e1423c4bfe952c7221c1565cdd410d2669bcd` |
| [P18] | `1807.06209/ms.tex` | `fe0833d2d0fda17427a709c9559dc7b3a988b955f47bb7de7a02c900ffdc21cf` |

**Equation numbers.** I reconstructed them from the LaTeX with my own
counter. For [GM], I used the section and appendix counters, one number per
unstarred row without `\nonumber`. For [EH98] and [W07], I counted
sequentially and skipped the `\def\beq` macro lines of [W07]. The results
agree with every number 1G-A cites:
- [GM]: (4.13) barotropic condition, l. 507; (4.14)–(4.17), l. 514–519;
  (4.19), l. 522–527; (4.21)–(4.23), l. 544–548; (4.27), l. 577;
  (5.1), l. 623; (5.4), l. 639; (5.5)–(5.7), l. 652–661; (B.2), l. 1165;
  (B.3)–(B.5), l. 1171–1176;
- [EH98]: (26), l. 682; (28), l. 758; (29), l. 775; (30)–(31), l. 838–843;
- [W07]: Eq. (11) is `sol1`, l. 310.

**Environment:**
- Linux x86-64 (AVX-512);
- CPython 3.13.12 with NumPy 2.5.3 and SciPy 1.18.1;
- CPython 3.11.15 with NumPy 2.4.6 and SciPy 1.17.1;
- CAMB 2.0.4 and SymPy 1.14.0, installed with `pip --target` into the audit
  scratch directory only. Neither is used by the project.

I did not test the owner's Windows platform.

**What I ran:**

| Run | Result |
|---|---|
| `scripts/phase1g_a_sigma8_path_numerics.py`, both interpreters, in the audit worktree | all budgets pass (about 15 s); artifact identical to the copied-in one in every non-environment field (0 differences) on both |
| `tests/test_barotropic_hadamard_refutation.py`, both interpreters | 8 passed |
| Own scripts (Sec. 3) | all results below |

I did not run the full suite; the lead runs it.

## 3. Method and independence statement

I started without any other auditor's conclusions and read no other
`phase1g_*_adversarial_audit*` file. I wrote from-scratch code in the audit
scratch directory `audit_a/`:

- `indep_background.py`: closed-form tracker from [GM] (5.5)–(5.7) and p. 25,
  with the D1-corrected R_D = −6f_v/t². It checks the averaged Hamiltonian
  constraint to 4e−16. It derives w_eff = −(4 − f_v)/(8 + f_v) and the
  c²_s,eff closed form above, and checks the latter against a finite
  difference of ṗ/ρ̇ to 1e−10.
- `indep_growth.py`:
  - the comoving closure [GM] (4.21)–(4.23) and the Mészáros equation (4.27),
    in s = ln t;
  - flat-ΛCDM growth from the integral D ∝ E(a)∫da/(aE)³;
  - the analytic early-time series u = 2/3 + c₁f_v, with c₁ = −19/60 for
    comoving and −5/12 for Mészáros.
- `indep_sigma.py`: EH98 no-wiggle and the full EH98 fit, both rewritten from
  `trans.tex`. The no-wiggle q is computed in explicit h-units with an
  arbitrary h, to test the unit chain. The top-hat is integrated with a
  4×10⁵-point trapezoid, a different rule from the script's Simpson grid.
- `camb_check.py`: CAMB σ8 and early-spectrum factors.
- `indep_barotropic.py`: [GM] (4.14)–(4.17) on both D3 branches, α, and the
  σ8-scale exponent under each radius convention.
- `appB_check.py` (SymPy) and `appB_consistent.py`: consistency of [GM]
  App. B and the consistently reduced closure.

Where 1G-A relies on frozen package functions, I replaced them with closed
forms and never imported the package. I ran the phase script only to compare
its output with mine.

## 4. Claims attacked

### 4.1 Barotropic closure: Hadamard ill-posed ([1G-A] Sec. 4.1)

**Claim (l. 119–155).** The only k-dependence of [GM] (4.19) is
`c²_s (k²/a²) Δ^(eff)`. With c²_s,eff < 0 the principal part is elliptic. The
frozen matrix gives `A23·A32 = −c²_s k²/a_D²`. The WKB exponent is
α = 1.70695, the slopes converge to α, and D3 leaves the rate unchanged.

**Re-derivation:**
- (4.19) (l. 524–527) has `+c²_s k²/a²` inside the Δ^(eff) bracket and no
  other k. Its principal part `Δ̈ − c² ³ΔΔ` is a wave operator for c² > 0 and
  a Laplace-type operator for c² < 0.
- From (4.15) and (4.17), `A23 = k²/a` and `A32 = −c²/a`, so
  `A23·A32 = −c²k²/a²`.
- (4.10) with P̃ = c²Δ gives `A33 = (w − c²)Θ` (`derived_4_10`). The printed
  (4.15) has `(w + c²)Θ` (`printed_4_15`). D3 therefore touches only A33.
- The sign of `A32` is load-bearing. It is physically right: c² > 0 gives
  acoustic oscillation, and [GM] (l. 591) say a negative EoS gives "an
  unstable growth regime at small scales".

**Independent numbers:**

| Quantity | 1G-A | Independent |
|---|---|---|
| c²_s,eff(z = 20), c²_s,eff(t0) | −0.4996, −0.3912 | −0.499568, −0.391238 |
| sign of c²_s,eff | "throughout" (z ≤ 20) | < 0 for every f_v ∈ (0, 1): range [−1/2, −1/3) |
| α (z = 20 → t0, dressed H0 = 1, a_w0 = 1) | 1.70695 | 1.7069482005 |
| slopes `derived_4_10`, k = 4π…64π | 1.4755 1.6167 1.6700 1.6907 1.6994 | 1.475512 1.616674 1.669976 1.690737 1.699439 |
| slopes `printed_4_15` | 1.3659 … 1.6996 | 1.365945 … 1.699566 |
| gap α − slope, 16π→32π and 32π→64π (printed/derived) | 0.0159/0.0162, 0.0074/0.0075 | 0.015854/0.016211, 0.007382/0.007509 |
| gap ratio | 2.15–2.16 | 2.148 / 2.159 |
| sign Δ_d(t0) at k = 2π (`derived_4_10`) | negative | negative |

The slopes agree with the artifact to ≤ 2e−10. The ln|Δ^(eff)(t0)| values agree to
≤ 4e−9 absolute (6e−11 relative). Δ_d(t0) grows at
the same rate (slope 1.6855 at 64π), so the matter field inherits the
instability.

**Outcome:** `CONFIRMED`. Classification
`DERIVED_FROM_VERIFIED_DEFINITIONS` + `NUMERICALLY_CORROBORATED` is
appropriate.

**σ8-scale illustration (l. 141–144).**
- **Claim:** "kR = 1 with R = 8/h Mpc … k_matrix ≈ 513 and αk ≈ 875 > 709.8,
  not even representable". The arithmetic reproduces: k = 512.83 and
  αk = 875.378.
- **The chain is a hybrid.** It sets the present *volume-average physical*
  wavenumber `k_phys0_D = 1/R` with R = 8/h_dressed Mpc. 1D-A §10 states
  that `k_phys0_D` "cannot be inserted directly into `k_com_obs R_com_obs`
  merely because it is dimensional".
- **The report's own conventions.** In the package normalisation
  (a_w0 = 1), a_D(t_e)(1+z_e) → 1: I measure 1.000000005 at f_v = 1e−8. So
  k_code = (c/H0)/R_γ for a photon-normalised comoving radius R_γ. Under the
  report's own conventions (a)/(b)/(c) (Sec. 6.4), αk at kR = 1 is
  557.4 / 639.7 / 693.5, all below 709.8. The 875 chain corresponds to
  R_γ = 8/(h γ_w0) = 8.0 Mpc, which is smaller than every Sec. 6.4 radius.
- **Outcome:** `CONFIRMED_WITH_CAVEAT` (GA-F3). The ill-posedness is
  unaffected.

**"No linear barotropic σ_R exists" (l. 146–149).**
- **The body is scoped.** It requires a window with power-law tails and a
  spectrum bounded below by a power law. That is correct.
- **The headlines drop the scope.** This affects Sec. 1 row 5, Sec. 9 row C,
  and the [SUCC] "meaning" field.
- **A Gaussian window converges.** The result is finite but meaningless: it
  is dominated by k ≈ α/R²_code ≈ 640/R, with log-amplitude of order
  (α/R_code)² ≈ 4×10⁵.
- **Outcome:** `CONFIRMED_WITH_CAVEAT` (GA-F5).

### 4.2 Homogeneous-density closure, [GM] App. B ([1G-A] Sec. 4.2)

**Claim (l. 157–172).** The printed (B.4) contains `−k²/a²` times 1/(2Θ). The
closure is therefore a backward heat equation and the initial-value problem is
ill-posed. The inventory records the verdict `BACKWARD_PARABOLIC_ILL_POSED`
under `DERIVED_FROM_VERIFIED_DEFINITIONS`. The Sec. 4 conclusion then reads
"only the comoving closure (and the Mészáros comparator) can define a linear
σ".

**(a) The printed equations.** Their principal part is as stated. My
integration of the printed (B.3)–(B.5) on the tracker (Λ = 0, z = 20 → t0,
matrix k) gives these values of d ln|Δ^(eff)(t0)|/d(k²):

| k interval | 4→8 | 8→12 | 12→16 | 16→20 | 20→24 | limit β = ∫dt/(2Θa_D²) |
|---|---|---|---|---|---|---|
| slope | 0.2510 | 0.3121 | 0.3225 | 0.3257 | 0.3271 | 0.32951 |

This is the first numerical corroboration of that statement.
**Outcome:** `CONFIRMED`.

**(b) The closure itself.** I re-derived App. B symbolically in
`appB_check.py`, from (4.10)–(4.12) (l. 492–497), (B.2) `Δ^(eff) = aΘṼ`
(l. 1165–1167) and background Raychaudhuri:
1. (4.12) with (B.2) gives
   `ΘP̃ = −Δ̇^(eff) + (wΘ + Θ̇/Θ)Δ^(eff)`, as [GM] l. 1169 describe.
2. Inserting this into (4.10) as printed, the form the project adjudicated
   (`D3_VERDICT = RESOLVED_DERIVED_4_10`), makes **Δ̇^(eff) cancel
   identically**. Only a constraint remains:
   `(Θ̇/Θ − k²/(a²Θ)) Δ^(eff) + (1 + w) Z = 0`.
3. The printed (B.4) equals exactly ½ × [(4.10) with P̃ → −P̃]. That is the
   same sign flip that turns (4.10) + (4.13) into the printed (4.15), the D3
   discrepancy. SymPy residual: 0.
4. The printed (B.5) equals exactly (4.11) with the correct +P̃ and Δ̇^(eff)
   taken from the printed (B.4). SymPy residual: 0.

So App. B mixes the two D3 signs.

**The consistent reduction.** Under the adjudicated sign, the closure is a
constrained system. Δ^(eff) = (1 + w)Z / (k²/(a²Θ) − Θ̇/Θ) is suppressed like
1/k². The Z equation carries the factor 1 − 12πGρ_eff g/Θ, which equals
(2 − 2f_v)/(2 + f_v²) > 0 at k = 0 and is regular on the tracker. I
integrated it in `appB_consistent.py`:

| k (matrix units) | 0 | 1 | 10 | 100 | 1000 | 10⁴ | Mészáros |
|---|---|---|---|---|---|---|---|
| Δ_d(t0)/Δ_d(t_i) | 24.299 | 17.955 | 10.218 | 10.00043 | 9.998209 | 9.998187 | 9.998186 |

The consistently derived closure is bounded, well-posed for
constraint-consistent data, and tends to the Mészáros growth at high k.

**Outcome:** the closure-level verdict is `REFUTED` (GA-F1). The verdict
holds only in the `printed_4_15` sign convention. In the other convention it
fails, and D3 is not mentioned in Sec. 4.2. Assessed class:
`CONVENTION_DEPENDENT` (D3). This does not touch any σ number: [GM] do not
use App. B (l. 1187), and neither does 1G-A.

### 4.3 Comoving closure ([1G-A] Sec. 4.3)

**Claim (l. 174–197).** The closure is pointwise ODEs, scale-independent,
well-posed and ensemble-preserving. The decaying modes "fall as t^{−5/3}
relative to the growing mode".

**What holds.** The first part is correct. (4.21)–(4.23) contain no spatial
operator ([GM] l. 549), and for zero-mean fields σ_R(t) ∝ D(t) follows.

**What does not hold.** One of the two non-growing solutions is the exact
Z ≡ 0 mode that [GM] note (l. 570): Δ_d constant,
Δ^(eff) = −(⟨ρ⟩/ρ_eff)Δ_d. My integration keeps |tZ| ≤ 2e−13 and Δ_d = 1
exactly. In Δ_d this mode falls only as t^{−2/3} relative to the growing mode
(ratio 0.0080 at t0 from f_v = 1e−3). The t^{−5/3} rate of the `growing_mode`
docstring is the rate at the (u, q) fixed point, with f_v → 0 frozen. The
Z ≡ 0 mode is singular early (Δ^(eff)/Δ_d ≈ −1/(2f_v)), so regular initial
conditions exclude it, and no number changes.

**Outcome:** `CONFIRMED_WITH_CAVEAT` (GA-F6).

### 4.4 Early-universe matter density per photon ([1G-A] Sec. 6.2)

**Claim (l. 325–348).**
`ω_m,eff = ⟨ρ⟩_D0 γ_w0³/ρ_crit(100) = ½(1 − f_v0)(2 + f_v0)(H_D0/100)²`,
with values 0.12048, 0.12114 and 0.13094.

**Re-derivation.** I used [GM] l. 661–663: ⟨ρ⟩ ∝ a_D⁻³, the normalisation
⟨ρ⟩_D0 = 12H_D0²(1 − f_v0)/[8πG(2 + f_v0)²], 1 + z = a_w0/a_w = γ_w a_w0/a_D,
and a_D0/a_w0 = γ_w0. Then ρ_m/T³ = (⟨ρ⟩_D0 γ_w0³/T0³)·γ_w(t)⁻³, which tends
to ⟨ρ⟩_D0 γ_w0³/T0³ as t → 0. The closed form follows algebraically. The
statement "a_D = a_w at last scattering" is [GM]'s normalisation. The
identity needs only a_D/a_w = γ_w → 1.

**Independent values:**

| Parameters | ω_m,eff | ratio to 0.315 × 0.674² |
|---|---|---|
| paper preset | 0.1204751 | 0.8419 |
| notebook preset | 0.1211359 | 0.8465 |
| [NW15] | 0.1309372 | 0.9150 |

**H_D0 is bare.** The paper preset gives H̄0 = 57.856 and the notebook preset
58.014. [GM]'s printed "H_D0 ≈ 58.01" for H0 = 73.03 matches the notebook's
73.23. That inconsistency sits in [GM] and is already handled by the two
presets.

**External corroboration.** [NW15]'s table (l. 1534–1548) gives bare
Ω̄_M0 = 0.215, h̄ = 0.5164 and γ̄0 = 1.314, so
Ω̄_M0 h̄² γ̄0³ = 0.1301. The identity gives 0.1304 at [NW15]'s best fit, and
the difference is the table's rounding. [NW15]'s dressed Ω_M0 = 0.489
(l. 1568, 2010) equals ½(1 − f_v0)(2 + f_v0).

**Citation.** The [W09] "canonical dressed value" is at l. 880–881; the
report cites l. 880.

**Outcome:** `CONFIRMED`. The label "numerically verified to 1e−13"
re-evaluates the same p. 25 normalisation. It adds no independent evidence
(part of GA-F11).

### 4.5 Growth ratio X∞ and its numbers ([1G-A] Sec. 5)

**Claim (l. 209–287).**
- X∞ = γ_w0 g_TS/g_Λ;
- g_TS = exp∫(u − tΘ/3) d ln t;
- g_Λ = 0.787813;
- the table, the finite-z_i matching, the f_v0 scan and the precision note.

**Re-derivation.** Take equal early σ(M) at equal photon temperature. Then
σ_Λ/σ_e = g_Λ(1 + z_e) and
σ_TS/σ_e = g_TS·a_D0/a_D(t_e) = g_TS γ_w0 (1 + z_e)/γ_w(t_e). The ratio is
γ_w0 g_TS/g_Λ as t_e → 0.

**Precision note.** I derived the constants from the first-order series:
- Mészáros: `u − tH = (c₁ − 1/3)f_v`, with c₁ = −5/12, so c = −3/4;
- comoving: c₁ = −19/60 (the source is (4/3)f_v q₀, q₀ = 1/5), so
  c = −13/20.

At t_e = 1e−6 t0 these give ln-biases of 1.82e−6 and 2.10e−6. The ratios of
the script's g_TS to my t_e → 0 limits match them.

**Independent values:**

| Quantity | 1G-A | Independent |
|---|---|---|
| g_Λ | 0.787813 | 0.7878126 |
| g_TS comoving / Mészáros ([GM]), t_e → 0 | 0.4026623 / 0.3416935 | 0.40266226 / 0.34169348 |
| X∞ comoving / Mészáros ([GM]) | 0.6995 / 0.5936 | 0.699460 / 0.593552 |
| X∞ comoving / Mészáros ([NW15]) | 0.8586 / 0.7646 | 0.858567 / 0.764550 |
| X at z_i = 20, 50, 100, 300 (comoving, [GM]) | 0.703464, 0.700464, 0.699815, 0.699529 | 0.703464, 0.700464, 0.699815, 0.699529 |
| f_v0 scan (10 f_v0 × 2 closures) | table l. 277–280 | all agree to the printed 3 decimals |
| γ_w − 1 at z = 20, 50, 100, 300 | 1.73e−2, 4.65e−3, 1.68e−3, 3.3e−4 | 1.726e−2, 4.653e−3, 1.677e−3, 3.27e−4 |

**Outcome:** `CONFIRMED`.
- The paper and notebook presets agree to 1e−15, since X depends only on
  f_v0.
- The fork table's "matching epoch ≤ 0.6%" holds for comoving. Mészáros at
  z_i = 20 is +0.93% (errata, GA-F9).

### 4.6 Early spectrum, EH98 and the Planck validation ([1G-A] Sec. 6.3)

**EH98 transcription.** Every coefficient matches `trans.tex`:
- (26) 44.5, 9.83, 10, 3/4;
- (31) 0.328, 431, 0.38, 22.3;
- (30) 0.43;
- (29) 2e, 1.8, 14.2, 731, 62.5;
- Θ_2.7 = T_CMB/2.7.

**Units.** (28) is q = (k/h Mpc⁻¹)Θ²/Γ_eff with Γ_eff = Ω_0 h(…). Hence
q = k[Mpc⁻¹]Θ²/(ω_m(…)), which is what the script uses (`gamma_eff_h = ω_m(…)`).
The (0.43ks) term takes k in Mpc⁻¹ and s in Mpc. My implementation works in
explicit h-units with an arbitrary h = 0.5 and gives identical σ. The unit
chain is right.

**Matter-era amplitude.**
`Δ²_δ = (4/25)A_s(k/k_p)^{n_s−1}(k/aH)⁴T²` follows from Φ = −(3/5)ζ and
δ = (2/5)(k/aH)²ζT with D/a → 1. With (aH)² = H100²ω_m/a it gives the
script's `(k/h100)⁴ … /ω_m²`. Correct.

**[P18] inputs.** They are read correctly from Table 2, whose TT,TE,EE+lowE+lensing
column is at `ms.tex` l. 2299–2315:
- Ω_b h² = 0.02237;
- n_s = 0.9649;
- 10⁹A_s = 2.100;
- σ8 = 0.8111.

The script uses Ω_m = 0.315 and h = 0.674 from the frozen `qplus` recipe
instead of Table 2's 0.3153 and 0.6736. This is documented in the script. The
report's column label "ratio to Planck (0.1431)" is that recipe product;
Table 2 gives Ω_m h² = 0.1430 (errata).

**Numbers:**

| Quantity | 1G-A | Independent |
|---|---|---|
| EH98 no-wiggle Planck σ8 | 0.8357 (+3.03%) | 0.8356887 (+3.032%) |
| EH98 full (with wiggles) | — | 0.8329851 (+2.70%) |
| CAMB, [P18] means, 0.06 eV | anchor 0.8111 | 0.81113 |
| CAMB, [P18] means, m_ν = 0 | — | 0.82276 |
| CAMB, recipe cosmology (0.315, 0.674), m_ν = 0 | — | 0.82599 |

**Where the +3.03% comes from:**
- +1.17%: EH98 no-wiggle against CAMB at the same cosmology;
- +0.39%: recipe against [P18] means;
- +1.43%: 0.06 eV neutrinos.

The product is +3.02%. Wiggles account for only 0.33% of the total, while the
report names "BAO wiggles and neutrinos" (GA-F4). Relaxing the gate from 3%
to 5% after the first run is transparent, and this decomposition justifies
it.

**E factors (EH98 → CAMB at z = 30):**

| Case | (a) equal mass | (b) dressed | (c) bare |
|---|---|---|---|
| [GM] | 0.92380 → 0.92638 | 1.01045 → 1.01410 | 1.06336 → 1.06775 |
| [NW15] | 0.96020 → 0.96161 | 0.91534 → 0.91634 | 0.98438 → 0.98602 |

The ratio bias is ≤ 0.5%, which confirms the fork-table estimate "≲ 1%".

**Outcome:** `CONFIRMED_WITH_CAVEAT` (GA-F4).

**Baryon fraction (l. 364–367).**
- **Claim:** "[NW15] report that the baryon/non-baryon ratio is pinned … so
  Planck's f_b is the primary closure".
- **The quote is accurate.** It is the [NW15] abstract, l. 110–113.
- **The inference does not follow.** [NW15]'s canonical Timescape fit
  (Table, `cmb1.tex` l. 1526–1568) has:
  - bare Ω̄_B0/Ω̄_M0 = 0.039/0.215 = 0.181 and dressed 0.089/0.489 = 0.182,
    so f_b ≈ 0.18, not 0.1563;
  - n_s = 0.992 ± 0.009 (best fit 0.995), not 0.9649;
  - A_s treated as an unconstrained nuisance parameter (l. 1421–1427).
- **The report read only the abstract.** Its Sec. 2 says so.
- **Effect on the [NW15] σ values:**

  | Early universe for the [NW15] row | σ(M8), comoving, equal mass | σ, wall bracket |
  |---|---|---|
  | as printed (f_b 0.1563, n_s 0.9649) | 0.669 | 0.935 |
  | [NW15] f_b = 0.181 | 0.637 (EH98), 0.639 (CAMB) | 0.890 (EH98), 0.893 (CAMB) |
  | [NW15] f_b = 0.181 and n_s = 0.992 | 0.643 (EH98), 0.645 (CAMB) | 0.899 (EH98), 0.902 (CAMB) |

- **Outcome:** `REFUTED` (GA-F2).

### 4.7 Radius conventions, σ table and wall bracket ([1G-A] Secs. 6.4, 7, 8)

**Radii.** All reproduce:
- R_P = 8/0.674 = 11.869 Mpc;
- (a) R_P(ω_P/ω)^{1/3} = 12.570 and 12.226;
- (b) 8/h_dressed = 10.954 and 13.115;
- (c) (8/h̄)/γ_w0 = 10.104 and 11.781.

For (c), I derived that a present volume-average proper radius L maps to the
photon-normalised radius L/γ_w0 by mass conservation. Correct.

**σ table.** All 12 entries reproduce to ≤ 1e−10 relative. Examples:
- [GM] comoving: 0.52410, 0.57326, 0.60328;
- [GM] Mészáros: 0.44474, 0.48646, 0.51193;
- [NW15] comoving: 0.66867, 0.63743, 0.68550.

The f_b rows reproduce, for example 0.5607 and 0.4817. So does the range
0.504–0.905.

**Wall bracket.**
- X_wall = γ_w0(1 − f_v0)^{1/3}/g_Λ = 1.112945 and 1.200172, both reproduced.
- σ: 0.8339, 0.9121, 0.9599 ([GM]) and 0.9347, 0.8910, 0.9582 ([NW15]),
  all reproduced.
- Finite-t_e identity: residual ≤ 2e−16.
- The naive limit at t_e = 1e−8 t0 differs by −4.67e−9 relative, as the
  corrected line says.
- [W07] Eq. (11) is `sol1`, `f_w^{1/3} ā ∝ t^{2/3}`. Correct.

**Two wording caveats:**
- **"Wall-comoving" in convention (b)** uses the *dressed* (5.4) a_w. Sec. 5.3
  of the same report shows this is not the wall-regional scale factor. With
  the (5.1) regional reading, R = 8/h/[γ_w0(1 − f_v0)^{1/3}] = 12.494 Mpc
  ([GM]) and 13.871 Mpc ([NW15]). The σ values then change:
  - comoving 0.573 → 0.526 ([GM]) and 0.637 → 0.613 ([NW15]);
  - wall bracket 0.912 → 0.837 and 0.891 → 0.857.

  All stay inside the stated budgets (GA-F8).
- **Sign robustness.** "every examined fork gives less linear structure … The
  sign of the effect is robust" (l. 412–416) holds within the volume-average
  closures. The same report's decisive two-scale fork (Sec. 8) gives
  0.83–0.96 > 0.811 (GA-F7).

**Outcome:** `CONFIRMED_WITH_CAVEAT`.

### 4.8 [GM] a_w notation ([1G-A] Sec. 5.3)

The two readings are verified:
- (5.1) (l. 622–625) defines a_Y := (V_Y(t)/V_Y(t_init))^{1/3};
- (5.4) (l. 639–641) is a_w = γ_w⁻¹a_D;
- [W09] l. 1763–1764 states `a_w = a_w0 t^{2/3}`;
- [W09] l. 617–623 is the dressed metric, with a ≡ γ̄_w⁻¹ā.

The factor between them, γ_w(1 − f_v)^{1/3}f_wi^{−1/3}, is correct.

**Numbers:**
- Regional a_w/t^{2/3} is constant to 9e−16.
- Dressed a_w/t^{2/3} varies by 16.576%. Analytically, the variation is
  g(f_v0)/g(1/4) − 1, with g = (1 − f_v)^{−1/3}/(1 + f_v/2) and its minimum
  at f_v = 1/4.

**Outcome:** `CONFIRMED`. The textual part is `VERIFIED_FROM_PRIMARY_SOURCE`.
The statement that the two differ is `DERIVED_FROM_VERIFIED_DEFINITIONS` plus
`NUMERICALLY_CORROBORATED`.

### 4.9 Barotropic status successor record and test

**The token change.** `UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY`:
`NOT_DERIVED` → `REFUTED_HADAMARD_ILL_POSED`. It is supported by Sec. 4.1
above and correctly scoped: finite-k ODEs are regular, and both D3 branches
are kept.

**What I verified:**
- Only that assignment changes in `scientific_status.py` (462121c → dee72e1).
- The executable AST of `barotropic.py` is identical at 462121c, dee72e1 and
  6f7937c (docstrings stripped).
- The live module holds the new token.
- The [SUCC] numbers (α, slopes, gaps, 2.15–2.16) match my values.
- The test passes on both interpreters. Its tolerances are explicit and
  sensible.
- Both inventories are canonical JSON.

**Two defects:**
- The [SUCC] "σ8 scales" bullet and the test pin 875.4 with the hybrid chain
  (GA-F3).
- [SUCC] cites the 1G-A report at "l. 482–483". The in-place edit 214a626
  moved that text to l. 493–494 (GA-F10).

**Outcome:** `CONFIRMED_WITH_CAVEAT`.

### 4.10 CLAUDE.md summary, reproducibility and evidence classes

**CLAUDE.md.** Its 1G-A entry is accurate: the route, the Hadamard verdict,
the token and validator behaviour, and the runtime and D3 preservation. It
says nothing on App. B.

**Reproducibility.** The script is deterministic and its budgets hold. Two
achieved bounds are misprinted (GA-F9):
- grid refinement 4.108e−15, printed "≤ 4e−15";
- direct vs Riccati at z_i = 20 2.25e−13, printed "≤ 2e−13".

**Evidence classes.** [1G-A] Sec. 2 says the classes "follow 1D-C §5". That
section requires one primary class per conclusion. In [1G-A]:
- Sec. 4.1 uses a composite class;
- Sec. 8 uses `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`, which is in neither
  list;
- Sec. 4.2 is `CONVENTION_DEPENDENT`, not `DERIVED_FROM_VERIFIED_DEFINITIONS`
  (GA-F1);
- the Sec. 6.2 numerical check is circular.

None of these is VERIFIED where it should be DERIVED, apart from the minor
Sec. 5.3 point (GA-F11). **Outcome:** `CONFIRMED_WITH_CAVEAT`.

## 5. Findings

| id | severity | resolution class | title |
|---|---|---|---|
| GA-F1 | MEDIUM | OWNER_DECISION | The App. B "backward-parabolic" verdict belongs to the printed (B.4), which carries the `printed_4_15` sign. Under `RESOLVED_DERIVED_4_10` the closure is a well-posed constrained system |
| GA-F2 | MEDIUM | OWNER_DECISION | Planck's f_b is justified by a misreading of [NW15]. [NW15]'s own fit has f_b ≈ 0.18 and n_s ≈ 0.99, so the [NW15] row is a hybrid |
| GA-F3 | LOW-MEDIUM | OWNER_DECISION | "αk ≈ 875 > 709.8 at kR = 1" uses a hybrid unit chain that 1D-A §10 excludes. The report's own conventions give 557–694. This propagates to [SUCC] and the test |
| GA-F4 | LOW | OWNER_DECISION | The EH98 bias is attributed mainly to omitted wiggles. CAMB attributes it to fit error (+1.2%), recipe cosmology (+0.4%) and neutrinos (+1.4%) |
| GA-F5 | LOW | OWNER_DECISION | Headline "no linear barotropic σ_R exists" drops the window and spectrum qualifiers |
| GA-F6 | LOW | OWNER_DECISION | The "t^{−5/3}" decay statement misses [GM]'s exact Z ≡ 0 mode, which falls as t^{−2/3} in Δ_d |
| GA-F7 | LOW | OWNER_DECISION | "Every examined fork … sign robust" holds only within the volume-average closures. The same report's decisive fork reverses the sign |
| GA-F8 | LOW | OWNER_DECISION | Convention (b) "wall-comoving" uses the dressed (5.4) a_w, which Sec. 5.3 shows is not the wall-regional scale |
| GA-F9 | LOW | UNAMBIGUOUS_ERRATUM | Misprinted numbers and labels: 0.45–0.69; ≤ 4e−15 (twice); ≤ 2e−13; "≤ 0.6%" without closure; "Planck (0.1431)" |
| GA-F10 | LOW | UNAMBIGUOUS_ERRATUM | [SUCC] line reference "l. 482–483" became stale after the in-place edit 214a626; it is now l. 493–494 |
| GA-F11 | LOW | OWNER_DECISION | Evidence-class bookkeeping: single-primary-class rule, an undeclared class, and a circular "numerically verified" check |

### GA-F1 — App. B verdict is D3-dependent (MEDIUM)

- **Statement.** [1G-A] Sec. 4.2 and the inventory classify the App. B closure
  as backward-parabolic and ill-posed, from the printed (B.4). The printed
  (B.4) is ½[(4.10) with P̃ → −P̃] (Sec. 4.2 above). With the (4.10) sign
  that the project adjudicated, (4.10) reduces to a constraint. The closure
  is then well-posed, and its growth tends to the Mészáros value at high k.
- **Consequence.** No σ number changes. Three statements are not supported
  as closure-level statements:
  - the Sec. 4 conclusion "only the comoving closure (and Mészáros) can
    define a linear σ";
  - the inventory verdict `BACKWARD_PARABOLIC_ILL_POSED`;
  - its class `DERIVED_FROM_VERIFIED_DEFINITIONS`.

  A new printed-vs-derived sign discrepancy in [GM] (App. B) is also
  identified. It has the same sign pattern as D3.
- **Suggested resolution.** Record a successor reading: "ill-posed in the
  `printed_4_15` sign convention, as printed; under
  `RESOLVED_DERIVED_4_10` the closure reduces to a constraint and is not
  shown to be ill-posed". Qualify the Sec. 4 conclusion. Consider adding an
  author question on the sign of ΘP̃ in (B.4).

### GA-F2 — Planck f_b justified by misreading [NW15] (MEDIUM)

- **Statement.** See Sec. 4.6. The [NW15] abstract says that the relation
  between the baryon/non-baryon ratio and the peak heights is fixed. [NW15]'s
  own Timescape fit gives f_b = 0.181, n_s = 0.992, and an unconstrained A_s.
- **Consequence.** The [NW15] row pairs the [NW15] background with a Planck
  early universe. Its primary σ values fall by about 4–5% when [NW15]'s own
  inputs are used:
  - 0.669 → 0.637–0.645;
  - wall bracket 0.935 → 0.890–0.902.

  This stays inside the report's f_b band. CLAUDE.md quotes [NW15]-row
  numbers from later phases ("0.935 for the [NW15] CMB fit", 1G-C; 1.36,
  1G-E). Whether they inherit the Planck f_b is outside this audit.
- **Suggested resolution.** The owner decides which early-universe inputs
  are primary for the [NW15] row. A successor note should correct the
  justification sentence and record [NW15]'s own f_b and n_s.

### GA-F3 — σ8-scale exponent uses a hybrid unit chain (LOW-MEDIUM)

- **Statement.** See Sec. 4.1. `αk ≈ 875` pairs `k_phys0_D` with R8, which
  1D-A §10 excludes. Under the report's photon-normalised conventions
  (a)/(b)/(c), αk at kR = 1 is 557 / 640 / 694, all below ln(float64 max)
  = 709.8.
- **Consequence.** "Not even representable at kR = 1" is convention-dependent.
  The ill-posedness and divergence are unaffected, and every convention
  exceeds 709.8 for kR ≳ 1.27. The number is repeated in the [1G-A]
  inventory, in [SUCC] and its inventory, and in the regression test, which
  pins 875.4.
- **Suggested resolution.** A successor note should name the chain and give
  the Sec. 6.4 values. The test pin may stay as a regression of that chain,
  but its comment should say which chain.

### GA-F4 to GA-F11 (LOW)

- **F4.** Sec. 4.6 above. A successor note should record the CAMB
  decomposition. The anchored-ratio bias is ≤ 0.5%.
- **F5.** Carry "(power-law-tailed window, power-law-bounded spectrum)" into
  Sec. 1 row 5, Sec. 9 row C and the [SUCC] meaning. Alternatively say "no
  finite, IR-controlled linear σ_R".
- **F6.** Qualify the decay rate. Near the fixed point, deviations fall as
  t^{−5/3}. The exact Z ≡ 0 mode falls as t^{−2/3} in Δ_d. It is singular
  early and excluded by regular initial conditions. The same imprecision is
  in the frozen `growing_mode` docstring. I note it only; that is package
  scope.
- **F7.** Add "within the volume-average CGI closures" to l. 412–416.
- **F8.** Relabel convention (b) as "dressed-comoving (Eq. 5.4 a_w)". Note
  the (5.1) reading, R = 12.49 and 13.87 Mpc.
- **F9, F10.** See the errata below.
- **F11.** Make Sec. 2 match the classes actually used. Drop "numerically
  verified to 1e−13" or call it an arithmetic check. Split the Sec. 5.3
  class.

## 6. Proposed errata (for a dated successor note; not applied)

| # | File, location | Old | New | Proof |
|---|---|---|---|---|
| 1 | 1G-A report l. 50 | `values span 0.45–0.69 (Sec. 7).` | `values span 0.44–0.69 (Sec. 7).` | artifact `sigma.cases.PAPER_REFERENCE.closures.meszaros.conventions.equal_mass_M8_planck.by_baryon_fraction["f_b=0.1563"].sigma_planck_anchored` = 0.44474, which is 0.44 at two decimals |
| 2 | 1G-A report l. 253 | `- Simpson grid refinement changes ln g by ≤ 4e−15.` | `- Simpson grid refinement changes ln g by ≤ 5e−15.` | the maximum of `growth.*.*.log_g_grid_refinement_change` over the three presets and both closures is 4.108e−15 |
| 3 | 1G-A report l. 527 | `- growth grid ≤ 1e−7 (achieved ≤ 4e−15);` | `- growth grid ≤ 1e−7 (achieved ≤ 5e−15);` | as #2 |
| 4 | 1G-A report l. 255 | `- Direct integration agrees with the Riccati integral to ≤ 2e−13 at` | `- Direct integration agrees with the Riccati integral to ≤ 3e−13 at` | max `matching["z_i=20"].direct_vs_riccati_rel_diff` = 2.2515e−13 |
| 5 | 1G-A report l. 428 | `\| Matching epoch z_i ≥ 20 \| ≤ 0.6% \| negligible \|` | `\| Matching epoch z_i ≥ 20 \| ≤ 0.6% (comoving), ≤ 0.9% (Mészáros) \| negligible \|` | artifact Mészáros PAPER_REFERENCE: X(z_i = 20) = 0.599065 against X∞ = 0.593553, so +0.93% |
| 6 | 1G-A report l. 340 | `\| Parameters \| ω_m,eff \| ratio to Planck (0.1431) \|` | `\| Parameters \| ω_m,eff \| ratio to 0.315 × 0.674² = 0.1431 (recipe; [P18] Table 2: 0.1430) \|` | script `PLANCK["omega_m_total_Om_h2"]` = 0.315 × 0.674² = 0.143101; [P18] `ms.tex` l. 2309: Ω_m h² = 0.1430 ± 0.0011 |
| 7 | [SUCC] md l. 104 | `` `phase1g_a_sigma8_derivation_path_audit.md` l. 153–155, 482–483 `` | `` `phase1g_a_sigma8_derivation_path_audit.md` l. 153–155, 493–494 (482–483 at 462121c) `` | `git diff 462121c 6f7937c` adds 7 lines at l. 259 and a net 4 at l. 442; the recommendation is now at l. 493–494 |
| 8 | [SUCC] inventory `superseded_frozen_readings[4].location` | `reports/phase1g_a_sigma8_derivation_path_audit.md l. 153-155, 482-483` | `reports/phase1g_a_sigma8_derivation_path_audit.md l. 153-155, 493-494 (482-483 at 462121c)` | as #7 (no test or script reads this field) |

## 7. Items for owner decision

1. **GA-F1.** Record the App. B verdict as convention-dependent. Qualify the
   Sec. 4 conclusion. Optionally add the (B.4) sign author question.
2. **GA-F2.** Choose the primary early-universe inputs for the [NW15] row.
   Correct the f_b justification. Check the downstream [NW15] quotes in
   1G-C, 1G-E and CLAUDE.md.
3. **GA-F3.** Qualify the 875 illustration in a successor note to [1G-A] and
   [SUCC]. Decide whether the test comment names the chain.
4. **GA-F4 to GA-F8 and GA-F11.** Wording, attribution and classification
   refinements, all in one successor note. No number, token or tolerance
   changes.

## 8. Verdict and readiness for tagging

**Verdict: `ACCEPT_WITH_CORRECTIONS`.** Every load-bearing element was
re-derived from the primary sources with independent code and confirmed:
- the Hadamard ill-posedness of the barotropic closure and the approved token
  change;
- the per-photon identity;
- X∞;
- the EH98 chain, the Planck anchor and the σ tables.

The defects are in scoping and classification, plus one misread source. None
invalidates a result of the phase.

**Tag readiness: `NOT_READY_OWNER_DECISION_REQUIRED`.** GA-F1, GA-F2 and
GA-F3 change recorded classifications, closure rationale or a recorded
illustration. Under the project rules these need the owner. Once a dated
successor note records those decisions and errata 1–8, the phase is
technically ready for a `phase-1g-a-…-v1` tag. No code or test change is
required.

## 9. Limitations

- **Platform.** Linux only. The owner's Windows 11 / Python 3.14.3
  environment was not exercised.
- **CAMB.** CAMB 2.0.4 is a numerical cross-check, not a primary source. The
  CAMB E factors are ratios at z = 30 and z = 60; they differ by ≤ 0.12%.
- **App. B.** The analysis takes (4.10)–(4.12) as printed. They were audited
  in 1C-A and 1D-D-t. I did not re-derive them from (2.22)–(2.24) here. The
  well-posedness of the consistent reduction is shown analytically at high k
  and numerically on the tracker for k ≤ 1e4 only. I did not study the DAE
  for non-Timescape backgrounds.
- **[NW15].** It gives no A_s, so the self-consistent [NW15] σ values keep
  Planck's A_s by assumption.
- **[DNW13].** Not consulted.
- **Owner approval.** The quoted approval in [SUCC] cannot be verified
  independently.
- **Other checks.** I did not run the full test suite or
  `scripts/audit_numerical_tolerances.py`.

## 10. Preservation statement

I created or modified only these two files in the main tree:
`reports/phase1g_a_adversarial_audit.md` and
`reports/phase1g_a_adversarial_audit_inventory.json`.

- **Main tree.** No other file in the main tree, and no file of the audit
  worktree, was edited, staged, committed, pushed or tagged.
- **Audit worktree.** Running the phase script rewrote its git-ignored
  artifact there. `git status` afterwards shows only the pre-existing
  untracked `.reference` symlink.
- **Scratch.** Scratch code, outputs and the CAMB/SymPy installation live
  only in the audit scratch directory `audit_a/`.
