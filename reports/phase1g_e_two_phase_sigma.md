# Phase 1G-E — Two-phase mass variance at 8 h⁻¹ Mpc in the Timescape model

Audit classification: `REPORT_ONLY_THEORY_AUDIT_WITH_NUMERICAL_EVIDENCE`.
Base: `5ab2394` (Phase 1G-D), branch `phase-1g-e-two-phase-sigma`.
Date: 2026-09-29.
Companion: [`phase1g_e_two_phase_sigma_inventory.json`](phase1g_e_two_phase_sigma_inventory.json).
Evidence: `scripts/phase1g_e_two_phase_sigma_numerics.py`, which writes the
git-ignored `artifacts/independent/phase1g_e_two_phase_sigma.json`.

References:
- [W09] arXiv:0909.0749v2;
- [1G-A], [1G-C], [1G-D]: the earlier phase reports;
- Boolean model: standard stochastic geometry, e.g. Chiu, Stoyan, Kendall &
  Mecke, *Stochastic Geometry and its Applications*, 3rd ed. (2013), Sec. 3.1.

## 1. Scope and verdict

**Authorisation.** On 2026-09-29 the project owner asked to "proceed with
Phase 1G-E". [1G-D] Sec. 11 item 3 defines it: a nonlinear two-phase
σ(R), consisting of a void-population model plus the wall-internal linear
field. It should give the first Timescape quantity comparable *in kind* to a
nonlinear σ8. This phase is report-only, with numerical evidence. No package
code, equation, status token or tolerance changes, and no observational claim
is made.

**Verdict.** In a two-phase Timescape universe the mass variance in balls of
radius R is

```text
σ²(R) = δ_v² σ²_part(R) + σ²_int(R),
```

**The two terms:**
- **σ_part:** the variance of the void/wall partition (empty voids, walls at
  `1/f_w` times the mean density), scaled by the void-interior contrast δ_v
  (δ_v = −1 on the tracker).
- **σ_int:** the linear wall-internal field of [1G-C], weighted by the
  probability that both points of a pair lie in walls.

**Model.** Voids are a Boolean model of Poisson balls of radius a at volume
fraction f_v0. Its covariance was checked against an independent Monte
Carlo to ≤ 1.5%.

**Results at R = 8 h⁻¹ Mpc** (dressed h) `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`:

| Parameters | σ_part (a = 15 h⁻¹ Mpc) | σ_int (compressed) | **σ total (tracker voids, δ_v = −1)** | range over a = 5–30, closures, δ_v |
|---|---|---|---|---|
| [GM] f_v0 = 0.737 | 1.130 | 1.093 | **1.57** | 0.93–2.12 |
| [NW15] f_v0 = 0.627 | 0.911 | 1.006 | **1.36** | 0.89–1.74 |

**Reading:**
- With the tracker's empty voids and [W09]'s characteristic void size,
  Timescape's matter distribution at 8 h⁻¹ Mpc is strongly nonlinear.
  σ ≈ 1.4–1.6 is about 1.7–1.9 times Planck-ΛCDM's *linear* σ8 (0.81).
- The void/wall partition and the wall-internal growth contribute
  comparably.
- These are the first Timescape numbers of the *nonlinear mass-variance* type.

**Status.** They are conditional and model-internal. They are **not** an
observational σ8. A comparison needs the same nonlinear statistic measured in
data under a Timescape (dressed) reduction, which this phase does not
construct.

## 2. Model `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`

**Assumptions:**
- **E1 (two phases).** Voids are empty (δ_v = −1, the tracker's `ρ_v = 0`,
  [1G-C] Sec. 3). Walls carry all the mass at mean density `ρ_w = ⟨ρ⟩/f_w`,
  plus a linear internal contrast δ_w. δ_v ∈ {−0.9, −0.8} is reported as a
  sensitivity outside the tracker.
- **E2 (void geometry).** A Boolean model: ball centres are a Poisson
  process of intensity λ, all radii equal a, and `λ V_a = −ln f_w` fixes the
  void volume fraction.
  - [W09] gives "voids of a characteristic diameter 30 h⁻¹ Mpc" (line 277),
    so a = 15 h⁻¹ Mpc is the primary value; a = 5–30 h⁻¹ Mpc is the
    sensitivity.
  - At f_v0 ≈ 0.7 the balls overlap strongly, and the walls form a
    connected, web-like complement.
- **E3 (independence).** δ_w is statistically independent of the void
  geometry.
- **E4 (Eulerian mapping of the wall field).** The wall-internal field was
  derived in Lagrangian (mass) coordinates ([1G-C], [1G-A] Sec. 6). In
  Eulerian space the walls occupy the fraction f_w of the volume.
  - The primary closure is *isotropic compression*: `ξ_E(r) = ξ_L(r/s)` with
    `s = f_w^{1/3}`.
  - `s = 1` (no compression) is the upper bracket. Real walls are sheets
    and filaments, so their compression is anisotropic.

**The variance.** With `χ_w` the wall indicator, the contrast relative to the
global mean is `(χ_w/f_w)(1+δ_w) − 1`. Under E1–E3, and with non-empty voids
scaling the partition amplitude by δ_v²:

```text
σ²_part(R) = ∫ P_R(r) ξ_w(r) dr,                 ξ_w(r) = exp(λ γ(r)) − 1,
σ²_int(R)  = ∫ P_R(r) (1 + ξ_w(r)) ξ_E(r) dr = ∫ dln k Δ²_E(k) K(k),
K(k) = ∫ P_R(r) (1 + ξ_w(r)) j0(kr) dr,           Δ²_E(k) = Δ²_L(k s).
```

**The ingredients:**
- `γ(r) = V_a(1 − 3r/4a + r³/16a³)` for `r < 2a` is the ball covariogram.
- `P_R(r) = (3r²/R³)(1 − 3r/4R + r³/16R³)` is the pair-separation density in
  a ball.
- `Δ²_L` is the wall-internal linear spectrum today: the 1G-A early spectrum
  (EH98, per-photon ω_m,eff, Planck A_s, n_s, f_b) times the wall growth
  `D_wall(t0) = γ_w0(1−f_v0)^{1/3}` ([1G-C] Sec. 5). It is Planck-anchored
  like [1G-A] (factor 0.97058).

**Limits:**
- `ξ_w(0) = f_v/f_w`, so `σ_part → √(f_v/f_w)` as R ≪ a: 1.674 ([GM]),
  1.297 ([NW15]).
- `σ_part → 0` as R ≫ a.

## 3. Verification `NUMERICALLY_CORROBORATED`

- **Pair-density identity.** `∫P_R(r) j0(kr) dr = W_TH(kR)²` holds to
  1.7e−12 (composite Gauss–Legendre, 400 × 16 nodes). This validates the
  r-quadrature of K(k).
- **Consistency with [1G-C].** Switching the partition off (ξ_w = 0, s = 1)
  gives σ_int = 0.9121 ([GM]) and 0.8910 ([NW15]). These are exactly
  [1G-C]'s σ_wall at the dressed 8/h radius.
- **Monte Carlo of the Boolean model** (fixed seed 20260929):
  - setup: a periodic box of side 30a, with 8569 ([GM]) or 6322 ([NW15])
    balls;
  - 2×10⁶ points for the covariance, and 4000 balls of radius R × 1500
    points each for the ball variance, with shot noise subtracted;
  - comparison is against the formula at the realisation's own intensity.

  | Quantity | [GM] | [NW15] |
  |---|---|---|
  | σ²_part, MC / analytic | 1.280 / 1.268 | 0.820 / 0.823 |
  | max gated relative error (f_w, σ²_part, ξ_w where ξ_w ≥ 0.4) | 1.5% | 0.9% |
  | ungated u = 1.5 (ξ_w ≈ 0.12, noise-dominated) | 4.7% | 7.4% |

  The first run fixed the formula at the nominal intensity and failed a 5%
  gate at 14%. The cause was the Poisson fluctuation of the ball count in one
  finite box (2% fewer balls, which shifts f_w by 4.5%), not the model. The
  comparison was then made at the realisation's own intensity, and the box
  and sample sizes were enlarged. The gate itself was not loosened.

## 4. Results

**R = 8 h⁻¹ Mpc** (10.95 Mpc for [GM], 13.11 Mpc for [NW15]). In the table,
σ_int and σ total are given as compressed / uncompressed, and σ total is at
δ_v = −1.

| a (h⁻¹ Mpc) | [GM] σ_part | [GM] σ_int | [GM] σ total | [NW15] σ_part | [NW15] σ_int | [NW15] σ total |
|---|---|---|---|---|---|---|
| 5 | 0.483 | 0.848 / 1.126 | 0.976 / 1.226 | 0.399 | 0.833 / 1.043 | 0.923 / 1.117 |
| 7.5 | 0.734 | 0.942 / 1.254 | 1.195 / 1.453 | 0.603 | 0.901 / 1.130 | 1.084 / 1.281 |
| 10 | 0.915 | 1.010 / 1.348 | 1.362 / 1.629 | 0.746 | 0.948 / 1.192 | 1.207 / 1.406 |
| **15** | **1.130** | **1.093** / 1.464 | **1.572** / 1.850 | **0.911** | **1.006** / 1.267 | **1.357** / 1.561 |
| 20 | 1.251 | 1.141 / 1.532 | 1.693 / 1.978 | 1.000 | 1.038 / 1.310 | 1.442 / 1.648 |
| 30 | 1.382 | 1.193 / 1.607 | 1.826 / 2.120 | 1.095 | 1.073 / 1.356 | 1.533 / 1.743 |

**Void-interior sensitivity** (a = 15, compressed; outside the tracker):

| δ_v | [GM] σ total | [NW15] σ total |
|---|---|---|
| −1 | 1.572 | 1.357 |
| −0.9 | 1.493 | 1.297 |
| −0.8 | 1.418 | 1.242 |

## 5. Interpretation and limits

1. **What the number is.** σ_2φ(8 h⁻¹ Mpc) is the rms mass contrast in
   8 h⁻¹ Mpc balls of the two-phase Timescape universe. It is the object
   [1G-D] Sec. 9 identified as the only meaningful σ at this scale. It is
   *nonlinear*: the partition is intrinsically nonlinear (empty voids,
   `ρ_w = 3.8⟨ρ⟩` for [GM]). The wall-internal part is linear in δ_w but is
   amplified by the pair-in-wall weighting.
2. **What it is compared with.** Planck-ΛCDM's σ8 = 0.81 is a *linear* amplitude.
   The ΛCDM *nonlinear* matter variance at 8 h⁻¹ Mpc is larger than the linear
   value, but this phase computes no ΛCDM nonlinear statistic. The honest
   statement:
   - with the tracker's empty voids and [W09]'s 30 h⁻¹ Mpc voids, the
     two-phase Timescape variance is about 1.7–1.9× the ΛCDM linear σ8;
   - a quantitative verdict against data or against ΛCDM's nonlinear
     variance needs the same statistic computed on both sides (Sec. 6).
3. **What dominates the uncertainty.**
   - the void radius: a factor 1.7–1.9 in σ between a = 5 and 30 h⁻¹ Mpc;
   - the Eulerian mapping of the wall field: +15–26% (uncompressed vs
     compressed);
   - f_v0: about 16% at a = 15;
   - the void interior: about −9% at δ_v = −0.8;
   - E3 and the single-radius Boolean geometry are untested idealisations.
     Real void populations have a size distribution and correlated,
     non-spherical shapes.
4. **Relation to earlier phases.**
   - The linear σ numbers of [1G-A] and [1G-C] are unchanged as computed
     quantities.
   - [1G-C]'s σ_wall is recovered here as the no-partition limit.
   - [1G-D]'s conclusion that no linear global-mean σ8 exists at 8 h⁻¹ Mpc
     is reinforced: the partition term alone is 0.4–1.4.

## 6. Recommendations (none applied; each requires human approval)

1. **Phase 1G-F: a self-consistent void population.**
   - Replace [W09]'s characteristic radius with a void size distribution
     derived from the same early spectrum and void-onset response as [1G-D]
     (an excursion-set, [SvdW04]-type size function, with ΛCDM replaced by
     the Timescape clock).
   - Test whether it reproduces the tracker's f_v0 (0.63–0.74) with
     near-empty voids. This is a sharp self-consistency test of the
     two-scale model.
2. **Matched observable.** Choose one nonlinear statistic that can be
   computed identically for data, ΛCDM and Timescape, e.g. the variance of
   counts-in-cells or the aperture-mass variance at about 8 h⁻¹ Mpc.
   Specify the Timescape reduction (dressed distances, 1D-C §§20–23) needed
   to compare it.
3. **Status token** (proposal):
   `TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"`,
   with assumptions E1–E4.
4. **Nothing to add to the 1G-B runtime yet.** The two-phase model is
   report-level until 1G-F fixes the void population.

## 7. Reproduction and preservation

```text
.venv\Scripts\python -B -W error scripts\phase1g_e_two_phase_sigma_numerics.py
→ wrote artifacts\independent\phase1g_e_two_phase_sigma.json    (a few seconds)
```

Asserted budgets:
- quadrature 1e−11;
- pair identity ≤ 1e−10 (achieved 1.7e−12);
- Monte Carlo vs analytic ≤ 5% where gated (achieved ≤ 1.5%);
- the 1G-A budgets, inherited.

Environments: Python 3.14.3 (NumPy 2.5.2, SciPy 1.18.1) and 3.11.9
(NumPy 2.4.6, SciPy 1.17.1). Every printed number is identical on both,
including the seeded Monte Carlo.

- **Added:** this report, its inventory, and one script.
- **Unchanged:** every package module, test, status token, tolerance and
  frozen report.
- **Remote:** nothing is pushed or tagged.
