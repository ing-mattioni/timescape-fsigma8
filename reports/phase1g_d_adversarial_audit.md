# Phase 1G-D — Independent adversarial audit

Audit classification: `INDEPENDENT_ADVERSARIAL_AUDIT`.

Checkpoint: `6f7937ce5681900898f5e0a6482a953f0fa3e5a0` (`6f7937c`, `main` at
the start of the audit session). Audited phase commit: `5ab2394` (parent
`214a626`). Date: 2026-09-29.

Companion:
[`phase1g_d_adversarial_audit_inventory.json`](phase1g_d_adversarial_audit_inventory.json).

Audited record: `reports/phase1g_d_separate_universe_growth.md` ([1G-D]),
its inventory, `scripts/phase1g_d_separate_universe_numerics.py` and its
artifact, and the four approved 1G-D status tokens in
`src/timescape_fsigma8/scientific_status.py`.

## 1. Verdict summary

- **Verdict:** `ACCEPT_WITH_CORRECTIONS`.
- **Tag readiness:** `NOT_READY_OWNER_DECISION_REQUIRED`.
- **Findings:** 10 in total. HIGH 0, MEDIUM-HIGH 1, MEDIUM 3, LOW-MEDIUM 1,
  LOW 5.

What survives. Every equation-level result of Secs. 3–5 is correct. I
re-derived all of them from [GM] and [W09] with my own symbolic code, starting
from an exact two-region cell rather than from the report's linear formulas:

- the one-time-scale law `f_v = t/(t+τ)`, with `τ/t0 = f_w0/f_v0` exactly;
- every separate-universe (SU) mode formula, including `δR_w = 10 H_w² δ_w`
  for the growing wall mode and the signs of the void-onset mode;
- the exactness of the SU modes: [GM] (4.9), (4.10) and (4.11) at k → 0 have
  zero residual symbolically, for four modes;
- every number in the Sec. 5 table.

The central negative result is stronger than the report shows. No linear
combination of SU modes (wall curvature, void onset, wall and void bang time)
has `P̃_eff ≡ 0`, so the comoving closure admits no SU mode at all. The
growing modes also fail the Mészáros and barotropic closures.

What does not survive as stated.

- **Void-seed scale (GD-F1, MEDIUM-HIGH).** The peak-background-split (PBS)
  estimate takes the void-seed scale from a standard Einstein–de Sitter (EdS)
  void factor, 1.72. The tracker's own void domain grows by `(f_v0/f_vi)^{1/3}`
  ≈ 4–20 in comoving radius. With a tracker-consistent seed scale:
  - A_v falls to 1.2–1.6×10³;
  - `A_v σ_LSS(R8)` falls from 2.6–4.3 to 1.05–1.5;
  - R*(ε = 1) falls to about R8;
  - X_SU falls from 2.75–3.95 to 1.30–1.63.
- **Supporting inputs and wording (GD-F2 to GD-F4).**
  - One input (`f_vi = 10⁻²`) is inconsistent with the tracker used elsewhere.
  - One evidence class is over-strong.
  - One attribution to [W09] is over-strong.

The four approved token values stay defensible. The recorded rationale of
`LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` needs owner review (Sec. 4.8).

## 2. Scope and evidence

**Files read in full (at 6f7937c, in the isolated audit tree):**
- `reports/phase1g_d_separate_universe_growth.md` (346 lines);
- `reports/phase1g_d_separate_universe_inventory.json` (443 lines);
- `scripts/phase1g_d_separate_universe_numerics.py` (297 lines);
- `artifacts/independent/phase1g_d_separate_universe.json`;
- `src/timescape_fsigma8/scientific_status.py`;
- `background/tracker.py`, `effective_fluid.py`, `observables.py` and
  `parameters.py`;
- `perturbations/growing_mode.py`.

**Files read in part:**
- `scripts/phase1g_a_sigma8_path_numerics.py`: the functions 1G-D imports;
- 1G-A, 1G-C and 1F-D reports: the passages that 1G-D cites or supersedes;
- `git show 5ab2394`.

**Primary sources (SHA-256 of the .tex, checked):**

| Id | File | SHA-256 |
|---|---|---|
| [GM] arXiv:2511.17160v2 | `2511.17160v2/main.tex` | `f9cadfa03ecc9a74b0a8f432ae4b13422daeb219f253756bcd877b4b75077c59` |
| [W09] arXiv:0909.0749v2 | `0909.0749v2/observe.tex` | `2b0324d127440e9a053a7cb37102d7655cca228a63cd2222843e879989b4b531` |
| [SvdW04] astro-ph/0311260 | `astro-ph_0311260/voids.tex` | `e66ad192ee91a83ba88b4068cce5f6b505eb4277a6365d961a60ca10cc1c84b5` |
| [EH98] astro-ph/9709112 | `astro-ph_9709112/trans.tex` | `5f2ac6b413df8b738c95f6650152b7e82d7c36f6d9b3a618da540e9739dce17f` |
| [JLH13] arXiv:1304.6087 | `1304.6087/voids_mnras.tex` | `cf6fc77a31b395138ac3a027d008698556534e81cfb27c39853d3a99c7b07c4e` |
| [W07] arXiv:0709.0732v2 | `0709.0732v2/solution.tex` | `221662c987e454729ef8202c87fa697c5882b5b7daaecdedb50a7cba8ffe6cd8` |
| [NW15] arXiv:1410.3470 | `1410.3470/cmb1.tex` | `6d0e6397d3877e0aaa3dba16601e1423c4bfe952c7221c1565cdd410d2669bcd` |

**Equation numbers.** [GM] equation numbers are not in the .tex. I
reconstructed them from the section counters, one number per unstarred display
row:

| Number | [GM] main.tex line |
|---|---|
| (3.12)–(3.13) | 399–400 |
| (3.17) `intcond_eff` | 414–415 |
| (4.9)–(4.12) | 493–496 |
| (4.13) | 507 |
| (4.27) | 578 |
| (5.6) | 657 |

These match the numbering the package already cites.

**Environment.** Linux x86-64. Numerics used the project interpreters
CPython 3.13.12 (NumPy 2.5.3, SciPy 1.18.1) and CPython 3.11.15 (NumPy 2.4.6,
SciPy 1.17.1). Symbolic work used SymPy 1.14.0 in a scratch virtual
environment (CPython 3.13.12).

**What was run:**
- the phase script on both interpreters;
- three from-scratch scripts in `audit_d/`:
  - `su_symbolic.py`: exact two-region cell, SU modes, residuals;
  - `su_combinations.py`: closure null spaces;
  - `su_numerics.py`: own ODE integrations, own EH98 σ quadrature, PBS, R*,
    variants.

No test suite was run.

## 3. Method and independence statement

I treated the report, inventory and artifact as claims under test. I did not
import the phase script for any recomputation.

- **Symbolic check.** An exact two-region cell is built from volumes:
  - empty Milne voids, `V_v = (t−b_v)³/(τ(1+ε))`;
  - dust walls with exact linearised curvature K and a bang-time shift `b_w`.

  Cell averages come from [W09] Q1 (line 513) and [GM] (3.12)–(3.13). The
  linear modes are derivatives with respect to (ε, K, b_w, b_v). None of the
  report's hand-linearised formulas is used.
- **Numerical check.**
  - The comoving and Mészáros growing modes are integrated in two independent
    ways from closed-form backgrounds, not from `perturbations.growing_mode`.
  - EH98 is re-implemented from trans.tex (lines 683, 758–759, 776–779,
    839–842), with an adaptive quadrature.
- **Package use.** Package functions were used only for the frozen `qplus`
  ΛCDM growth factor, the growth normalisation shared with 1G-A.

I did not read any other 1G adversarial audit or any other auditor's scratch
directory.

## 4. Claims attacked

### 4.1 One time scale and τ = 1F-D's b

**Claim** ([1G-D] Sec. 1 item 1; Sec. 3): `f_v = t/(t+τ)` with
`τ = (2+f_v0)(1−f_v0)/(3 f_v0 H_D0)`; τ/t0 = 0.3569 / 0.5949; τ is Phase
1F-D's `b`.

**Re-derivation.** [GM] (5.6), line 657, divided by `3 f_v0 H_D0` gives
`t/(t+τ)` identically. With `t0 = (2+f_v0)/(3H_D0)`, `τ/t0 = f_w0/f_v0`
exactly. That gives 0.356852 and 0.594896. The 1F-D report defines
`f=t/(t+b)` at line 37 and `b=(2+fv0)*(1-fv0)/(3*fv0*HD0)` at line 85.

**Outcome: CONFIRMED.** The class `DERIVED_FROM_VERIFIED_DEFINITIONS` is
right.

### 4.2 Separate-universe modes and their exactness

**Claim** (Sec. 1 item 2; Sec. 4):
- `δf_v = f_v f_w δ_w`;
- `δ_d = f_w δ_w`;
- `δH_w = −δ̇_w/3`;
- `δR_w = 10 H_w² δ_w`;
- void onset: `δf_v = −f_v f_w ε`, `δ_d = f_v ε`.

Each mode is an exact k → 0 solution of [GM] (4.9)–(4.11). The class given is
`DERIVED_FROM_VERIFIED_DEFINITIONS`.

**Re-derivation.**

1. *Wall curvature.* I linearised a curved dust FLRW wall with the same bang
   time. The result is `a_w = t^{2/3}(1 − (9/20) K t^{2/3})`, so
   `δ_w = (27/20) K t^{2/3}` and `δR_w = 6K/a_w²`. Hence
   `δR_w/(H_w² δ_w) = 10` exactly. The sign is closed (δR_w > 0) for an
   overdensity.
2. *Other formulas.* Every other formula and sign in Sec. 4 agrees
   symbolically with the derivative of the exact cell.
3. *Buchert equations.* The averaged Hamilton and Raychaudhuri equations hold
   to first order in all four parameters, so every mode is an exact Buchert
   two-region solution.
4. *The k → 0 correspondence.* The CGI scalars of a Fourier mode are `−k²`
   times the perturbations of the effective background of a neighbouring
   domain:
   - `Δ = −k² δρ/ρ`;
   - `Z = −k² δΘ`;
   - `P̃ = (1+w)P = −k² δp/ρ`.

   The common factor cancels in the linear equations and in every ratio.
   `Z ↔ δΘ = −δ̇_d` by (4.9). The report's correspondence is right, except
   that it leaves the common `−k²` factor implicit.
5. *Residuals.* The residuals of (4.9), (4.10) and (4.11) are identically
   zero for ε, K, b_w and b_v. The k → 0 form of (4.10) is exactly the
   linearisation of [GM] (3.17), `ρ̇_eff + Θ(ρ_eff + p_eff) = 0`. Every exact
   cell obeys it, so the report's statement that "(4.10) follows from the
   background effective conservation law of each cell" is true. (4.12) only
   fixes Ṽ; its `k²Ṽ` term enters (4.10) at higher order in k.
6. *Is the report's check circular?* No, but it is an identity check. The
   script defines `Z = −δ̇_d`, so (4.9) holds by construction. The (4.11)
   residual then checks that the hand-linearised δQ, δ⟨R⟩, δH_w and δR_w are
   consistent with the averaged Raychaudhuri equation. My exact-cell
   derivation confirms them independently.

**Closed forms** (auditor):
- void onset: `Δ_eff/δ_d = −2τ(5t+4τ)/(t(9t+8τ))` and
  `P̃/Δ_eff = −(t+2τ)/(5t+4τ)`;
- wall curvature: `Δ_eff/δ_d = 2(3t²−10tτ−10τ²)/(3t(9t+8τ))`.

**Attack on scope.** The mode set rests on Assumption S1, which Sec. 4 itself
states. [GM] main.tex line 620 says of the timescape walls: "the curvature
within such idealised wall regions is not a free choice within the framework,
but instead must be vanishing by construction". The wall-curvature mode
therefore goes beyond the timescape construction. S1 also keeps the wall
bang-time mode (`δ_w ∝ t⁻¹`) but drops the void bang-time mode. The
identification "the long-wavelength perturbations of the two-scale model are"
these modes is therefore conditional (GD-F3).

**Outcome: CONFIRMED_WITH_CAVEAT.**
- Exactness: `DERIVED_FROM_VERIFIED_DEFINITIONS`. Confirmed.
- Identification of the mode set: `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`
  (S1).

The formula `δR_w = 10 H_w² δ_w` is stated for the wall mode "or C t⁻¹" too.
For the decaying mode, `δR_w = 0` (GD-F9).

### 4.3 [GM]'s closures fail the separate-universe test

**Claim** (Sec. 1 item 3; Sec. 5 table). The claim is the table below, with
the conclusion that the comoving, Mészáros and barotropic closures fail the
test.

**Independent numbers** ([GM] preset; SU columns from the auditor's closed
forms; comoving from two independent integrations):

| t/t0 | SU wall Δ_eff/Δ_d | SU wall P̃/Δ_eff | SU void Δ_eff/Δ_d | SU void P̃/Δ_eff | comoving Δ_eff/Δ_d | c²_s |
|---|---|---|---|---|---|---|
| 0.001 | −297.27 | −0.3320 | −356.98 | −0.4990 | +0.20001 | −0.49999 |
| 0.01 | −29.630 | −0.3206 | −35.806 | −0.4898 | +0.20004 | −0.49973 |
| 0.1 | −2.8413 | −0.2251 | −3.6636 | −0.4222 | +0.19952 | −0.48540 |
| 0.3 | −0.8297 | −0.0635 | −1.2537 | −0.3463 | +0.19610 | −0.44816 |
| 1 | −0.1036 | +0.9327 | −0.3870 | −0.2666 | +0.18330 | −0.39124 |

**Agreement.** Maximum relative differences against the artifact:
- SU ratios: 2.4e−15;
- comoving ratio: 1.0e−12.

[NW15] agrees to the same precision. The report's table matches to every
printed digit.

**Can a combination of SU modes reproduce a closure?** I solved exactly for
constants (c_ε, c_K, c_bw, c_bv) that make each closure hold identically in t:

| Closure at k → 0 | SU combinations satisfying it identically |
|---|---|
| comoving: `P̃ = 0` | none (only the trivial one) |
| Mészáros, (4.27) vs (4.11): `Δ_eff + 3P̃ = 0`, i.e. `δQ = 0` | only `c_bw = 1.5 c_bv` (decaying) |
| literal `Δ_eff = 0` | none |
| barotropic: `P̃ = c²_s Δ_eff` | only `c_bw = c_bv`, the global bang-time shift (decaying) |

**Is the comoving growing mode an SU combination?** No.
- Near t = 0 the SU growing wall mode is `t^{2/3}` times a series in `t/τ`.
  The other modes are `t`, `t⁰` or `t⁻¹` times such series.
- An SU combination with the comoving regular mode's leading `t^{2/3}` must
  therefore be the pure wall mode. It would have `u = t dln δ_d/dt = 2/3 − f_v`
  exactly.
- The regular comoving mode has `u = 2/3 − (19/60) f_v + O(f_v²)`. I derived
  this analytically and confirmed it numerically (−0.316667). For Mészáros,
  `u = 2/3 − (5/12) f_v + O(f_v²)`.
- Both differ at `O(t^{5/3})`, so neither is an SU mode.

**Outcome: CONFIRMED_WITH_CAVEAT.** The failure is robust for the growing
modes and holds even without the wall-curvature mode. Three caveats:
- The result is conditional on S1 (GD-F3).
- Mészáros consistency means `δQ = 0`. It does not mean `Δ_eff = 0`. [GM]
  line 500 notes that `Δ_eff = P̃ = 0` together would force all perturbations
  to zero (GD-F5).
- The barotropic closure holds exactly for the global bang-time mode. The
  report says it agrees "only asymptotically early, and only for the
  void-onset mode" (GD-F5).

### 4.4 Implied void response r(t)

**Claim** (Sec. 5): `r = (D_CGI − f_w D_wall)/f_v` rises 0.006 → 0.435
(×72.6). For Mészáros the factor is ×62.9; for [NW15] ×80 and ×72.

**Independent values.** At the exact times the factors are ×72.61 and ×62.93
([GM]) and ×79.93 and ×72.22 ([NW15]). The report's 72.59, 62.91, 79.91 and
72.20 come from the nearest grid points. Both are right to the quoted digits.

**Normalisation.** The normalisation is consistent. D_CGI and D_wall both
start at the photon scale factor at `t_e = 10⁻⁷ t0`, and both have
`D/a_ph → 1` there. The closed form `D_wall(t0) = γ_w0 f_w0^{1/3}` agrees to
5e−8.

**Shape.** Early on `r ∝ t^{2/3}` (log slope 0.66664). This is the
`O(t^{5/3})` difference of Sec. 4.3 divided by `f_v ∝ t`. The test omits the
decaying SU modes and fixes the wall coefficient at 1, so it is incomplete.
The series argument of Sec. 4.3 closes that gap.

**Outcome: CONFIRMED.**

### 4.5 Peak-background-split A_v, seed scale and R*

**Claim** (Sec. 7; Sec. 8):
- `A_v = φ(ν)/(σ_s Φ(−ν))`, "since τ ∝ 1/f_vi";
- R_seed = (30/2)/1.72/h;
- σ_s = 9.3e−4 / 8.4e−4;
- ν = 3.72 / 2.33;
- A_v = 4260 / 2869 / 4724 / 3181;
- the R* table.

**Arithmetic, reproduced from scratch:**

| Quantity | Report | Own |
|---|---|---|
| R_seed [GM] / [NW15] (Mpc) | 11.9 / 14.3 | 11.942 / 14.297 |
| σ_s | 9.3e−4 / 8.4e−4 | 9.2912e−4 / 8.3799e−4 |
| ν (f_vi = 10⁻⁴ / 10⁻²) | 3.72 / 2.33 | 3.7190 / 2.3263 |
| A_v [GM] | 4260 / 2869 | 4260.45 / 2868.53 |
| A_v [NW15] | 4724 / 3181 | 4723.80 / 3180.50 |
| R* (all 24 cells) | table | agree to ≤ 1.3e−8 |

My own EH98 σ(R8) for Planck is 0.835689. The 1G-A value is 0.835689.

**Step "τ ∝ 1/f_vi".** Inside the tracker, `f_v(t_i) = t_i/(t_i+τ)`, so
`d ln τ/d ln f_vi = −1/(1−f_vi)`. That is −1 to O(f_vi), so the step holds.

But the tracker then fixes f_vi. At the photon-normalised last scattering
(z = 1090):
- [GM]: `t_LS/t0 = 3.380e−5`, and `f_v(t_LS) = 9.47e−5`;
- [NW15]: `t_LS/t0 = 3.018e−5`, and `f_v(t_LS) = 5.07e−5`.

The `f_vi = 10⁻²` branch is 100–200 times the tracker's own value (GD-F2).
[W09]'s fits used `f_vi = 10⁻⁴` (footT, lines 2412–2418).

**Seed factor 1.72, from the primary source.**
- [SvdW04] writes (lines 2152–2163): shell crossing when
  `sinhΘ(sinhΘ−Θ)/(coshΘ−1)² = 8/9`, "so Θ_sc ≈ 3.53". It gives
  `1+Δ = 0.1982` and "a factor of (0.1982)^{−1/3} ≈ 1.7151".
- The 8/9 condition follows from the EdS tophat void. I derived it from the
  Lagrangian map of the shells just outside the edge.
- Its root is Θ_sc = 3.4875. That gives `1+Δ = 0.2047`, a factor 1.6967 and
  `δ_v = −2.717`. My brute-force Lagrangian map (no closed-form condition)
  gives the same.
- [JLH13] quotes "−2.7" and "1.7" (lines 132–133). [SvdW04]'s own appendix
  numbers do not satisfy their stated condition.
- The effect on 1G-D is +0.9% in A_v, which is immaterial.

**The material problem (GD-F1).**
- In the tracker, the void domain of [GM] (5.1) is a fixed set of fluid
  elements. Its comoving volume relative to the mean grows ∝ f_v.
- The report identifies the seeds with that domain: `f_vi = Φ(−ν)` is the
  seed fraction at last scattering. So each seed's comoving radius grows by
  `(f_v0/f_vi)^{1/3}` (times `γ_w0⁻¹` in photon-comoving units). That is 19.5
  for f_vi = 10⁻⁴ and 4.2 for f_vi = 10⁻². It is not 1.72.
- With the EdS factor, seeds that fill 10⁻⁴ of the volume at last scattering
  fill 1.72³ × 10⁻⁴ = 5×10⁻⁴ today, not f_v0 = 0.737.

A tracker-consistent seed radius is
`R_seed = (15/h Mpc)(f_vi/f_v0)^{1/3}/γ_w0`. With it:

| Case | R_seed (Mpc) | σ_s | A_v | A_v σ_LSS(R8) | R*(ε=1) | R*(10% void fr.) | R*(10% density) | X_SU |
|---|---|---|---|---|---|---|---|---|
| [GM], f_vi = 10⁻⁴ | 0.77 | 3.38e−3 | 1172 | 1.05 | 9.9 | 32.6 | 84.3 | 1.30 |
| [GM], f_vi = 10⁻² | 3.58 | 1.82e−3 | 1465 | 1.32 | 13.6 | 40.8 | 100.8 | 1.55 |
| [NW15], f_vi = 10⁻⁴ | 1.02 | 3.21e−3 | 1235 | 1.15 | 9.2 | 40.0 | 63.0 | 1.35 |
| [NW15], f_vi = 10⁻² | 4.71 | 1.64e−3 | 1623 | 1.52 | 13.1 | 51.1 | 78.5 | 1.63 |

R* is in h⁻¹ Mpc, dressed h. The [NW15] rows use [NW15]'s own equal-mass R8.
Without the `γ_w0⁻¹` conversion, `A_v σ_LSS(R8)` is 1.18–1.76.

**Outcome: CONFIRMED_WITH_CAVEAT** for the arithmetic. The seed-scale and
f_vi inputs are additional, tracker-inconsistent assumptions (GD-F1, GD-F2).

### 4.6 Reading of [W09]

The quotes are accurate. Verbatim, from observe.tex:

- Lines 277–278: "Voids of a characteristic diameter $30h^{-1}$ Mpc are
  observed to fill 40--50\% of the universe at the present epoch \cite{HV}."
- Lines 326–327: "Here we take a ``dust particle'' to be of at least the scale
  of statistical homogeneity, 100$h^{-1}$ Mpc or somewhat larger
  \cite{footD}."
- Lines 455–457: "represents a scale above which the variance in density
  contrasts is bounded at the 10\% level, and below which density constrasts
  become as large as they can possibly be."
- Lines 1807–1811: "If this uncompensated fraction is viewed as a single
  density perturbation then
  \de\Z{\cal H}\equiv\left(\de\rh\over\rh\right)_{\!\cal H\hbox{\sevenrm i}}
  =\fvi\left(\de\rh\over\rh\right)\ns{vi}.\label{initc}"
- Lines 1814–1817: "We might demand $\de\Z{\cal H}\in\{-10^{-6},-10^{-5}\}$,
  which means we might take $\fvi\in\{10^{-4},10^{-2}\}$, depending on what
  values of $(\de\rh/\rh)\ns{vi}$ are acceptable for the nonbaryonic dark
  matter power spectrum."
- Lines 2414–2415 (footT): "were fit using the full exact solution for
  $\hri=0.99999$, $\fvi=10^{-4}$, and $z_i=1100$."

**The attribution.** `A_v = 1/|δ_H|` is the report's own construction. It
comes from perturbing f_vi at fixed `(δρ/ρ)_vi` in (initc). The sign is
right: overdense means later void onset. But [W09] never states a response of
a region's void fraction to a long-wavelength mode. The resulting
1000–4750 h⁻¹ Mpc shows that this reading is not a viable response relation.
It does not show that [W09] is "internally inconsistent" (GD-F4).

**Outcome: CONFIRMED_WITH_CAVEAT.**

### 4.7 Super-cell law, X_SU and the Sec. 9 conclusion

**Claim** (Secs. 6, 9):
- `D_SU = f_w D_wall + A_v a_LS f_v`;
- X_SU ≥ 0.293 / 0.448;
- PBS X_SU = 2.75–3.95;
- `A_v σ_LSS(R8) = 2.6–4.3 ≫ 1`, hence no linear global-mean σ8.

**Independent values.**
- X_SU (A_v = 0) = 0.29270 / 0.44766.
- PBS X_SU = 2.7524 and 3.9459 ([GM]); 2.7678 and 3.8936 ([NW15]).
- These agree with the artifact to 5e−9.

**Attacks.**

1. *The R8 radius.* The script uses R8 = 12.57 Mpc for both parameter sets
   (lines 254–255). That is the [GM] equal-mass radius. [NW15]'s own is
   12.226 Mpc (1G-A artifact). There, σ_LSS = 9.336e−4 and
   `A_v σ = 2.969 / 4.410`, so the overall range is 2.6–4.4 (GD-F7).
2. *Why the numbers are what they are.* R_seed ≈ R8, so
   `A_v σ_LSS(R8) ≈ φ(ν)/Φ(−ν)` = 2.67 or 3.96. That is the inverse Mills
   ratio of the seed threshold. The "≫ 1" is fixed by the seed-scale choice
   (GD-F1).
3. *Normalisation at last scattering.* S2 sets `δ_w(LS) = δ_L` and
   `ε = A_v δ_L`. The cell contrast at last scattering is then
   `(1 − f_vLS + A_v f_vLS) δ_L`, with `A_v f_vLS` = 0.40 / 0.27 ([GM]) and
   0.24 / 0.16 ([NW15]). If δ_L is the region's early-universe contrast, the
   wall term must shrink. X_SU then moves from 3.95 to 3.83 and from 2.75 to
   2.67 (GD-F6).
4. *The lower bound needs curved walls.* The bound X_SU ≥ 0.293 exists only
   if wall curvature is admitted. With [GM] line 620's flat walls, it is 0
   (GD-F3).

**Outcome: CONFIRMED_WITH_CAVEAT.** The numbers reproduce. The PBS
conclusions depend on inputs that the report does not flag as
convention-dependent.

### 4.8 Wording of the four approved tokens

| Token | Value | Assessment |
|---|---|---|
| `GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY` | `FAILED_FOR_TIMESCAPE_TRACKER` | Value supported for all growing SU modes, even with the void-onset mode alone. It is conditional on S1. The code comment's "Meszaros (Delta_eff = 0)" is imprecise (GD-F5). |
| `TWO_SCALE_SUPER_CELL_GROWTH_LAW` | `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` | Appropriate. Add the S1 wall-curvature and last-scattering normalisation caveats (GD-F3, GD-F6). |
| `VOID_ONSET_RESPONSE` | `EXTERNAL_CLOSURE_INPUT` | Confirmed and strengthened. The PBS estimate alone spans 1.2×10³–4.9×10³ across seed and f_vi conventions. |
| `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` | `NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY` | Value defensible: \|ε\| ≳ 1 at R8 under every seed convention tested, and R8 < R_void makes the wall/void partition O(1) (variance f_v/f_w ≈ 2.8). The recorded rationale "A_v sigma_LSS(R8) = 2.6-4.3" depends on the seed convention (1.05–1.5 tracker-consistent) and uses the [GM] radius for [NW15] (GD-F1, GD-F7). |

The report's headline "The volume-average CGI growth of [1G-A] is therefore
not Timescape's long-wavelength growth" is correct under S1 only. The same
sentence is repeated in `README.md` and `CLAUDE.md` (GD-F3).

## 5. Findings

| Id | Severity | Resolution class | Title |
|---|---|---|---|
| GD-F1 | MEDIUM-HIGH | OWNER_DECISION | PBS void-seed scale is inconsistent with the tracker's own void expansion |
| GD-F2 | MEDIUM | OWNER_DECISION | `f_vi = 10⁻²` branch is inconsistent with the tracker's f_v at last scattering |
| GD-F3 | MEDIUM | OWNER_DECISION | SU-mode identification rests on S1, and its wall-curvature mode conflicts with [GM]'s flat walls; evidence class over-strong |
| GD-F4 | MEDIUM | OWNER_DECISION | "[W09] internally inconsistent" attributes to [W09] a consequence of the report's own reading |
| GD-F5 | LOW-MEDIUM | OWNER_DECISION | Mészáros and barotropic closures are mischaracterised in the SU test and in a token comment |
| GD-F6 | LOW | OWNER_DECISION | S2 normalisation: the void-onset term is 16–40% of the cell contrast at last scattering |
| GD-F7 | LOW | UNAMBIGUOUS_ERRATUM | [NW15] σ_LSS(R8) is computed at the [GM] radius 12.57 Mpc |
| GD-F8 | LOW | UNAMBIGUOUS_ERRATUM | Two rounding errors in the Sec. 8 R* values |
| GD-F9 | LOW | UNAMBIGUOUS_ERRATUM | Two statements are too general (δR_w for the decaying mode; "at all times") |
| GD-F10 | LOW | UNAMBIGUOUS_ERRATUM | Preservation statement omits the `CLAUDE.md` and `README.md` edits |

**GD-F1.** [1G-D] Sec. 7 derives R_seed from [SvdW04]'s EdS shell-crossing
factor. It does not note that the tracker, which 1G-D uses for D_SU, grows
each void domain's comoving radius by `(f_v0/f_vi)^{1/3}`. With a
tracker-consistent seed scale the conclusions change:

| Quantity | Report | Tracker-consistent seed |
|---|---|---|
| A_v | 2.9–4.7×10³ | 1.2–1.6×10³ |
| `A_v σ_LSS(R8)` | 2.6–4.3 | 1.05–1.5 |
| R*(ε = 1) | 28–45 h⁻¹ Mpc | 9–14 h⁻¹ Mpc |
| R*(10% density) | 128–215 h⁻¹ Mpc | 63–101 h⁻¹ Mpc |
| X_SU | 2.75–3.95 | 1.30–1.63 |

The equations are unaffected. The readings "≫ 1", "3–4× ΛCDM (8–16× in
power)", "reproduces [W09]'s 100 h⁻¹ Mpc" and "σ8 lies in the
non-perturbative regime" are not robust to this input. The same readings
appear in Sec. 1 items 4–6, Secs. 6–9, the inventory, `README.md`,
`CLAUDE.md` and the rationale comment of
`LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC`.

**GD-F2.** The tracker fixes `f_v(t_LS)` = 9.47e−5 ([GM]) and 5.07e−5
([NW15]). "τ ∝ 1/f_vi" is derived only inside the tracker.
- The 10⁻² branch sets every lower end of the quoted ranges.
- With the tracker's own f_vi and the report's seed factor:
  - [GM]: A_v = 4274, X_SU = 3.96;
  - [NW15]: A_v = 4914, X_SU = 4.03, `A_v σ(R8) = 4.59`, R* = 42 / 121 /
    172 h⁻¹ Mpc.
- These [NW15] values lie outside the report's quoted ranges.

**GD-F3.** Sec. 4 is labelled `DERIVED_FROM_VERIFIED_DEFINITIONS`, yet it
opens with Assumption S1. Three points:
- The wall-curvature mode needs curved walls, which [GM] main.tex line 620
  rules out "by construction".
- S1 keeps the wall bang-time mode and drops the void bang-time mode.
- Exactness is `DERIVED_FROM_VERIFIED_DEFINITIONS`. The identification of the
  long-wavelength perturbations is `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`.

Consequences. The A_v = 0 lower bound (0.293 / 0.448) exists only if wall
curvature is admitted. The headline in Sec. 1 item 3, Sec. 5, `README.md` and
`CLAUDE.md` should be conditioned on S1. The FAILED token value is unaffected:
the void-onset mode alone fails every closure.

**GD-F4.** Sec. 1 item 5 says: "[W09]'s own 'single density perturbation'
seeding relation instead gives 1000–4750 h⁻¹ Mpc, which is internally
inconsistent with that claim". Sec. 8 says it "is not compatible with [W09]'s
homogeneity claim", and the inventory says "inconsistent with W09
homogeneity claim". The response reading `A_v = 1/|δ_H|` is 1G-D's, not
[W09]'s (Sec. 4.6). The supported statement is that this reading of (initc)
is not a viable response relation.

**GD-F5.** [GM] (4.27) is (4.11) without the source
`4πG ρ_eff(Δ_eff + 3P̃_eff)`. At k → 0 that source equals `−δQ`, so an SU
mode satisfies Mészáros if and only if `δQ = 0`.
- Where the report says "Mészáros sets Δ_eff = 0": Sec. 1 item 3, Sec. 5,
  the inventory's `gm_closures_su_consistency.meszaros`, and the artifact
  field `gm_meszaros: {"Delta_eff": 0.0}`.
- The scientific_status.py comment reads "Meszaros (Delta_eff = 0)".
- For the barotropic closure, Sec. 5 says it "agrees only asymptotically
  early, and only for the void-onset mode". The global bang-time shift
  satisfies it exactly, for all t.

The conclusion stands. No growing SU mode has δQ ≡ 0 or `P̃ ≡ c²_s Δ_eff`.

**GD-F6.** `A_v f_v(t_LS)` = 0.404 / 0.272 ([GM]) and 0.240 / 0.161 ([NW15]).
The SU cell contrast at last scattering is therefore not δ_L. Normalising the
total contrast to δ_L lowers X_SU by about 3%. S2 should state which of the
two quantities δ_L is.

**GD-F7.** Script lines 254–255 evaluate `sigma_large_R(12.57, …)` for every
case. That affects Sec. 9, Sec. 1 item 6, the inventory
`void_response_at_R8` for [NW15], and the token comment "2.6-4.3". The
correct [NW15] values at 12.226 Mpc are:
- σ_LSS = 9.336e−4;
- PBS `A_v σ` = 4.410 and 2.969;
- single `A_v σ` = 93.36 and 933.59.

**GD-F8.** Two values are rounded wrongly:
- The [NW15] single-perturbation ε = 1 value is 353.295 h⁻¹ Mpc. It is
  printed "354".
- The [GM] 10⁻⁶ void-fraction value is 3744.48 Mpc. It is printed "3745".

**GD-F9.** Two statements are too general:
- Sec. 4 applies `δR_w = 10 H_w² δ_w` to "δ_w = C t^{2/3} (or C t^{−1})".
  For the t⁻¹ mode, `δR_w = 0`. In general,
  `δR_w = (8/3)(δ_w/t² + δ̇_w/t)`.
- Sec. 1 item 3 says "Δ_eff/Δ_d < 0 at all times". The wall mode's ratio
  changes sign at `t = (5+√55)τ/3 ≈ 4.14τ` (f_v ≈ 0.805), after t0 for both
  presets.

**GD-F10.** `git show --stat 5ab2394` shows that the commit also modified
`CLAUDE.md` (+16/−1 lines) and `README.md` (+10/−3 lines). Sec. 12 lists only the report, its
inventory and one script.

## 6. Proposed errata

The lead applies these through a dated successor note.

| # | File, location | Old | New | Proof |
|---|---|---|---|---|
| E1 | report Sec. 9, lines 262–263 | `At R8 (Lagrangian 12.6 Mpc), σ_LSS = 9.0e−4 ([GM]) or 9.2e−4 ([NW15]). So` / `` `A_v σ_LSS(R8) = 2.6–4.3` (PBS) and 90–900 ([W09] single). Both are ≫ 1.`` | `At R8 (Lagrangian, equal mass: 12.6 Mpc for [GM], 12.2 Mpc for [NW15]), σ_LSS = 9.0e−4 ([GM]) or 9.3e−4 ([NW15]). So` / `` `A_v σ_LSS(R8) = 2.6–4.4` (PBS) and 90–930 ([W09] single). Both are ≫ 1.`` | 1G-A artifact `radii_photon_comoving_Mpc.equal_mass_M8_planck` = 12.226040 Mpc for NW15_CMB_FIT. Script line 254 hard-codes 12.57. Own σ_LSS(12.226) = 9.33593e−4. 4723.80 × 9.33593e−4 = 4.410; 3180.50 × 9.33593e−4 = 2.969. |
| E2 | report Sec. 1 item 6, line 70 | `` `A_v σ_LSS(R8) ≈ 2.6–4.3 ≫ 1` `` | `` `A_v σ_LSS(R8) ≈ 2.6–4.4 ≫ 1` `` | As E1. The "≫ 1" is subject to owner decision OD1. |
| E3 | inventory, `cases.NW15_CMB_FIT.void_response_at_R8` and `findings.sigma8_location.void_response_at_R8` | `4.328`, `2.914`, `91.62`, `916.205`; `"2.6-4.3 (PBS) >> 1"` | `4.41`, `2.969`, `93.359`, `933.593`; `"2.6-4.4 (PBS) >> 1"` | As E1. |
| E4 | report Sec. 8, line 247 | `relation gives 354–1298 / 752–2651 / 1004–3501 h⁻¹ Mpc.` | `relation gives 353–1298 / 752–2651 / 1004–3501 h⁻¹ Mpc.` | Artifact `NW15_CMB_FIT.transition_scales.R_star["W09_single_perturbation_\|dH\|=1e-5"]["eps=1"].R_h_inv_Mpc` = 353.2952; inventory 353.3. |
| E5 | report Sec. 8 table, line 244 | `\| 1615 (2212) \| 2735 (3745) \| 4755 (6511) \|` | `\| 1615 (2212) \| 2735 (3744) \| 4755 (6511) \|` | Artifact `PAPER_REFERENCE…\|dH\|=1e-6.void_fraction_10pct.R_Mpc` = 3744.4815. |
| E6 | report Sec. 4, lines 118–119 | `` - `δH_w = −δ̇_w/3` and `δR_w = 10 H_w² δ_w` (linearised Friedmann equation `` / `  of a closed dust patch).` | `` - `δH_w = −δ̇_w/3` and, for the growing mode, `δR_w = 10 H_w² δ_w` (linearised Friedmann equation `` / `` of a closed dust patch; `δR_w = 0` for the t^{−1} mode). `` | Linearised region Friedmann equation `6H_wδH_w = 8πGρ_wδ_w − δR_w/2`, with `8πGρ_w = 4/(3t²)` and `H_w = 2/(3t)`, gives `δR_w = (8/3)(δ_w/t² + δ̇_w/t)`: 10H_w²δ_w for t^{2/3}, 0 for t⁻¹. Checked symbolically. |
| E7 | report Sec. 1 item 3, line 45 | `` `Δ_eff/Δ_d < 0` at all times and `P̃_eff ≠ 0`, with `` | `` `Δ_eff/Δ_d < 0` at all t ≤ t0 and `P̃_eff ≠ 0`, with `` | Wall-mode ratio `2(3t²−10tτ−10τ²)/(3t(9t+8τ))` has its root at t = (5+√55)τ/3 = 4.139τ > t0 (2.80τ [GM], 1.68τ [NW15]). The void-onset ratio is negative for all t. |
| E8 | report Sec. 12, line 343 | `- **Added:** this report, its inventory, and one script.` | `- **Added:** this report, its inventory, and one script. **Modified:** the phase ledger in CLAUDE.md and the summary in README.md (text only).` | `git show --stat 5ab2394`: CLAUDE.md, README.md, report, inventory and script. |

## 7. Items for owner decision

- **OD1 (GD-F1).** Choose the void-seed convention. Either:
  - adopt the tracker-consistent seed `R_seed = R_void (f_vi/f_v0)^{1/3}/γ_w0`;
    or
  - keep [SvdW04]'s factor as an explicit additional assumption and quote
    both ranges.

  Then revise:
  - Sec. 1 items 4–6 and Secs. 6–9;
  - `README.md` and `CLAUDE.md` (the "128–215 h⁻¹ Mpc" and "non-perturbative"
    lines);
  - the rationale comment of `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC`. The
    token value can stay. Its rationale should rest on the R8 < R_void
    partition argument, with the PBS figure as a convention-dependent
    corroboration.
- **OD2 (GD-F2).** Restrict f_vi to the tracker's `f_v(t_LS)`, or mark the
  10⁻² branch as outside the tracker. Update the quoted ranges.
- **OD3 (GD-F3).** Reclassify the Sec. 4 identification as
  `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` (S1). Cite [GM] line 620. Say
  that the X_SU lower bound needs curved walls. Condition the headline on S1
  in the report, `README.md` and `CLAUDE.md`.
- **OD4 (GD-F4).** Reword the "[W09] internally inconsistent" statements
  (Sec. 1 item 5, Sec. 8, inventory).
- **OD5 (GD-F5).** Correct the Mészáros and barotropic characterisation in
  Sec. 1 item 3, Sec. 5, the inventory and the comment of
  `GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY` in scientific_status.py.
  Decide whether to rename the artifact field `gm_meszaros.Delta_eff`.
- **OD6 (GD-F6).** Define δ_L in S2: either the total contrast of the region
  at last scattering, or the wall-mode amplitude.
- **OD7 (GD-F7).** Decide whether to fix the script constant 12.57 and
  regenerate the artifact. Decide whether to update the token comment
  "2.6-4.3". Both are code.

## 8. Verdict and readiness for tagging

**Verdict: `ACCEPT_WITH_CORRECTIONS`.** The theory claims of Secs. 3–5 are
correct. Every number reproduces from scratch. The status-token values are
defensible.

**Tag readiness: `NOT_READY_OWNER_DECISION_REQUIRED`.** Four reasons:
- GD-F1 materially changes the quantitative conclusions of Secs. 6–9 and
  their interpretation.
- GD-F2, GD-F3 and GD-F4 concern evidence classes and statements that the
  owner approved or that are repeated in `README.md` and `CLAUDE.md`.
- GD-F5 touches the rationale comment of an approved token.
- Errata E1–E8 alone would not resolve these.

## 9. Limitations

- **τ ∝ 1/f_vi in the full solution.** I verified it inside the tracker only.
  I did not integrate [W09]'s general solution (h_ri ≈ 1, ε_i ≠ 0) to test it
  there.
- **The alternative seed scale.** It follows from the report's own
  identification of seeds with the tracker's void domain. Converting [W09]'s
  30 h⁻¹ Mpc diameter to photon-comoving length depends on convention; I give
  results with and without `γ_w0`. I did not validate the Gaussian-threshold
  PBS itself (for example, the neglected seed-depth response). I re-derived
  the standard formula but did not fetch Kaiser (1984) or Bardeen et al.
  (1986).
- **Early-spectrum inputs.** The Planck inputs, the EH98 import and the
  ω_m,eff identity come from 1G-A. I re-implemented EH98 from trans.tex but
  did not re-audit 1G-A's choices.
- **Platform.** The owner's platform (Windows, Python 3.14.3 and 3.11.9) was
  not available. On Linux, 3.13 and 3.11 differ from each other and from the
  committed inventory only at the ulp level (for example, (4.11) residuals and
  the 17th digit of the comoving ratio).
- **Tests.** I ran no test suite, per the brief.

## 10. Preservation statement

I created exactly two files in the main tree: this report and its JSON
companion. I edited, staged, committed, pushed or tagged nothing else.

All scratch work is in
`/tmp/claude-0/-home-user-timescape-fsigma8/b43492c2-35bf-5351-8e13-b75ee0b87001/scratchpad/audit_d/`.
That includes a scratch virtual environment with SymPy.

In the isolated audit tree, running the phase script rewrote its git-ignored
artifact. I restored it byte-identical to the copy the lead placed there. The
tree's `git status` is clean, apart from the pre-existing `.reference`
symlink.
