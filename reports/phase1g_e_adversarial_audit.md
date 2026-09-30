# Phase 1G-E — Independent adversarial audit

Audit classification: `INDEPENDENT_ADVERSARIAL_AUDIT`.
Checkpoint: `6f7937c` (`6f7937ce5681900898f5e0a6482a953f0fa3e5a0`), audited in a
clean, isolated worktree of exactly that commit. The 1G-E content was added in
`8cf5c49`.
Date: 2026-09-29.
Companion: [`phase1g_e_adversarial_audit_inventory.json`](phase1g_e_adversarial_audit_inventory.json).
Audited report: [`phase1g_e_two_phase_sigma.md`](phase1g_e_two_phase_sigma.md) (cited as [1G-E]).

## 1. Verdict summary

| Item | Result |
|---|---|
| Verdict | `ACCEPT_WITH_CORRECTIONS` |
| Tag readiness | `NOT_READY_OWNER_DECISION_REQUIRED` |
| Findings | 0 HIGH, 2 MEDIUM-HIGH, 2 MEDIUM, 1 LOW-MEDIUM, 2 LOW (7 in total) |

**What survives.** The core mathematics is correct. I re-derived it from first
principles:
- the Boolean-model covariance `ξ_w = exp(λγ) − 1`;
- the ball covariogram, and the limits 1.674 and 1.297;
- the pair-separation density and the identity `∫P_R j0 = W²`;
- the decomposition at δ_v = −1;
- the equivalence of `ξ_E(r) = ξ_L(r/s)` and `Δ²_E(k) = Δ²_L(ks)`.

My own code reproduces all 60 numbers of the [1G-E] Sec. 4 table. It takes a
different route (real space, QAWF for ξ_L), and the largest relative difference
from the artifact is 3.5e−6. It also reproduces the Planck anchor 0.970577,
D_wall, the radii and the recovery of [1G-C]'s σ_wall. A 24-realisation
lattice Monte Carlo, independent of the phase's method, confirms the Boolean
formula. It matches σ²_part to −0.3 ± 0.4% ([GM]) and 0.0 ± 0.3% ([NW15]) at the
realised intensity. The ensemble mean matches the nominal formula within its
1σ error. The script gives bit-identical results on both interpreters here;
only the environment block differs.

**What does not survive:**
- **GE-F1:** the non-empty-void formula `σ² = δ_v² σ²_part + σ²_int` breaks
  mass conservation. The δ_v sensitivity is understated by about a factor 2,
  and the lower edges of the headline ranges fall from 0.93/0.89 to 0.82/0.80.
- **GE-F2:** [W09] line 277 does not support voids of a single 15 h⁻¹ Mpc
  radius filling all of f_v0. The same sentence says these voids fill 40–50%,
  and the next sentences add minivoids.
- **GE-F3:** "s = 1 is the upper bracket" is misleading as an uncertainty
  statement.
- **GE-F4:** the ratio to Planck uses radius convention (b), not 1G-A's
  frame-free convention (a).
- **GE-F5:** the Monte Carlo precision is overstated. With another seed the
  phase's own gate fails.
- **GE-F6, GE-F7:** small numeric and cosmetic errata.

The approved token value `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` is the
right class for the δ_v = −1 result under E1–E4. Its recorded wording needs
the corrections in Sec. 4.8.

## 2. Scope and evidence

**Files read in full** (audit tree at `6f7937c`, SHA-256):

| File | SHA-256 |
|---|---|
| `reports/phase1g_e_two_phase_sigma.md` | `421b47b531701dd8b575d689f608f84a80679c6d9f00c4abd04a4c4c2b737be8` |
| `reports/phase1g_e_two_phase_sigma_inventory.json` | `0dd5ff4fe37069e3cb57eaabafb6edaa8b626d1b7f9a7200adaf8b9bbcf54d7d` |
| `scripts/phase1g_e_two_phase_sigma_numerics.py` | `030eb7f649ac523cafc799c1ac304a8a3a664578a12a5b1a9a2ff39266c8ff09` |
| `scripts/phase1g_a_sigma8_path_numerics.py` (imported by path) | `65eb42352aed1c9d26f4fba8b6e7bac3c4ed6e336e8910c150180f0c161c08f9` |
| `artifacts/independent/phase1g_e_two_phase_sigma.json` (regenerated, git-ignored) | `94c16cc15d3dee14ad1de4a8b5833c752f76e9d7289c237b1a18cd9751393612` |

Context read: AGENTS.md, CLAUDE.md, [1G-A] Secs. 6.1 and 6.4,
[1G-C] Secs. 3, 5 and 7, [1G-D] Secs. 9 and 11, the frozen `qplus` and
`presets.py`, and the 1G-A and 1G-C artifacts.

**Primary sources** (the hashes match the brief):

| Id | File | SHA-256 | Lines used |
|---|---|---|---|
| [GM] 2511.17160v2 | `main.tex` | `f9cadfa0…c77c59` | 663 (⟨ρ⟩(t0), H_D0, γ_w) |
| [W09] 0909.0749v2 | `observe.tex` | `2b0324d1…b531` | 277–285, 376, 385–386, 1621 |
| [EH98] astro-ph/9709112 | `trans.tex` | `5f2ac6b4…7f` | 683, 759, 778–779, 839–842 |
| [SvdW04] astro-ph/0311260 | `voids.tex` | `e66ad192…b5` | 449–450, 503–517, 1420, 2157–2163 |
| [JLH13] 1304.6087 | `voids_mnras.tex` | `cf6fc77a…7e` | 73, 395–400, 1338–1345 |
| [NW15] 1410.3470 | `cmb1.tex` | `6d0e6397…cd` | 104–105 (H0 = 61.0, f_v0 = 0.627) |
| [P18] 1807.06209 | `ms.tex` | `fe0833d2…cf` | (Planck inputs as quoted in the 1G-A script; not re-read) |

**Environment.** Linux x86-64 with AVX-512. CPython 3.13.12 (NumPy 2.5.3, SciPy
1.18.1) and CPython 3.11.15 (NumPy 2.4.6, SciPy 1.17.1).

**What was run:**
- The phase script, on both interpreters, with `-B -W error`. Wall time was
  81 s and 77 s. The artifacts are byte-identical apart from the environment
  block. The 3.13 output is byte-identical to the artifact supplied in the
  audit tree, which I restored afterwards.
- My own scripts, in the scratch directory `audit_e/`:
  - `indep_sigma.py`: tracker closed forms, EH98, anchoring, σ_part, and
    σ_int by a real-space route;
  - `indep_mc.py`: the lattice Monte Carlo ensemble;
  - `sensitivities.py`: the [W09]-consistent populations and anisotropic
    maps;
  - `equal_mass.py`: the radius convention (a);
  - `dv_check.py`: a direct check of the δ_v algebra.
- `rerun_phase_mc_seeds.py`, for comparison only. It runs the phase's own
  `monte_carlo_boolean` with 15 other seeds.
- The full test suite was not run, as the brief requires.

## 3. Method and independence

The 1G-E report, inventory and artifact were treated as claims under test.
- **Derivations.** Every load-bearing formula was re-derived on paper:
  Boolean covariance, lens volume, pair density, variance decomposition,
  Fourier map of E4 and the δ_v algebra.
- **Recomputation.** Each number was recomputed with code that does not
  import the phase script or the package:
  - tracker quantities from the closed forms of [GM] line 663 (γ_w = 1 + f_v/2;
    H_D0 = 2H0(2+f_v0)/(4+f_v0+4f_v0²); ω_m,eff = ½(1−f_v0)(2+f_v0)h̄²,
    cross-checked against ⟨ρ⟩(t0)γ_w0³ to 1e−14);
  - EH98 transcribed from `trans.tex`;
  - the ΛCDM growth by direct quadrature. It gives 0.7878126, the same as the
    frozen `qplus(0)`.
- **σ_int by a different route.** I used real space:
  `σ_int² = σ_L²(R/s) + ∫P_R ξ_w ξ_L(r/s) dr`, with
  `ξ_L(r) = r⁻¹∫Δ²k⁻² sin(kr) dk` by QAWF. The phase script integrates K(k) in
  k-space instead. As a check of my ξ_L, `∫P_R ξ_L dr` reproduces the k-space
  σ_L² to ≤ 2e−5.
- **Monte Carlo by a different method.** I used an exact distance test at
  every node of a 320³ lattice (box 16a) and exact FFT autocorrelations. The
  ball variance is taken over all lattice positions and compared with the
  analytic value for the same lattice ball. The ensemble has 24 independent
  realisations per parameter set, from seeds 101 and 202, not 20260929.
- **Sources.** Source statements were checked against the e-print lines
  cited.

I did not read any other auditor's report or scratch directory.

## 4. Claims attacked

### 4.1 Boolean covariance and its limits (brief item 1)

**Claim** ([1G-E] Sec. 2, lines 94 and 100–110):
- `ξ_w(r) = exp(λγ(r)) − 1`;
- `γ = V(1 − 3r/4a + r³/16a³)`;
- `ξ_w(0) = f_v/f_w`, and `σ_part → √(f_v/f_w)` for R ≪ a (1.674, 1.297).

**Re-derivation:**
1. **One point.** A point is in a wall iff no centre lies within a of it. The
   count of centres in that ball is Poisson with mean λV, so
   `P = e^{−λV} = f_w`.
2. **Two points.** Both points are uncovered iff no centre lies in the union
   of the two balls. The union has volume `2V − γ(r)`, where γ is the lens
   volume. So `P₂ = exp(−λ(2V−γ))`, and `P₂/f_w² − 1 = exp(λγ) − 1`.
3. **Lens volume.** It is `(π/12)(2a−r)²(4a+r) = (π/12)(16a³ − 12a²r + r³)`,
   which equals `V(1 − 3r/4a + r³/16a³)`.
4. **Limits.** At r = 0, `e^{λV} − 1 = 1/f_w − 1 = f_v/f_w`. For R ≪ a,
   ξ_w ≈ ξ_w(0) over the whole pair range.
5. **Numbers.** √(0.737/0.263) = 1.6740 and √(0.627/0.373) = 1.2965.

**Outcome: CONFIRMED.**

### 4.2 Pair density, identity and variance decomposition (item 2)

**Claim** ([1G-E] lines 89–102): `P_R(r) = (3r²/R³)(1 − 3r/4R + r³/16R³)`;
`∫P_R j0 dr = W_TH(kR)²`; `σ² = δ_v² σ²_part + σ²_int`.

**Re-derivation:**
- **Pair density.** It is `P_R = 4πr² γ_R(r)/V_R²`, which gives the stated
  form. The identity follows from `(1/V²)∫∫e^{ik·(x−y)} = |W̃(k)|²` and the
  angular average `⟨e^{ik·r}⟩ = j0(kr)`.
- **The reported residual.** My Gauss–Legendre (600 × 20) and QAWO
  quadratures both give the same 1.69e−12 residual. It is not quadrature
  error: at kR = 0.01 the closed-form reference `3(sin x − x cos x)/x³` loses
  about 12 digits, while the series `1 − x²/10 + x⁴/280 − …` gives exactly the
  quadrature value. For 0.3 ≤ kR ≤ 10 the relative residual is ≤ 1.2e−15; at
  kR = 60 it is 7e−13 (absolute 4e−19). So the identity holds better than
  stated. It is not tested for 60 < kR ≤ 300, but there W² < 1e−8 and the
  absolute error is negligible.
- **δ_v = −1.** With `δ = (χ_w/f_w)(1+δ_w) − 1`, E3 and ⟨δ_w⟩ = 0,
  `ξ = ξ_w + (1+ξ_w)ξ_E`. The cross term vanishes by E3. This part is
  **CONFIRMED**.
- **δ_v ≠ −1.** Let the void interior be `(1+δ_v)⟨ρ⟩`, with walls carrying the
  remaining mass and the fractional field δ_w. Mass conservation fixes
  `1+δ_W = (f_w − f_v δ_v)/f_w`. Then

  ```text
  δ = −δ_v (χ_w/f_w − 1) + (f_w − f_v δ_v)(χ_w/f_w) δ_w
  σ² = δ_v² σ²_part + (f_w − f_v δ_v)² σ²_int.
  ```

  The partition term really is `δ_v² σ²_part`. The internal term is not
  unchanged; its factor is 1 only at δ_v = −1. [1G-E] keeps σ_int fixed,
  which needs walls at `⟨ρ⟩/f_w` while voids also hold mass. The mean density
  would then be `[1 + f_v(1+δ_v)]⟨ρ⟩`.
- **Direct check.** `dv_check.py` builds the density field on a lattice with
  exact mean density 1.000000, using an antithetic pair to cancel the
  realisation cross term. The measured ball variance equals the
  mass-consistent formula to every printed digit, and the [1G-E] formula
  overestimates it:

  | f_v | δ_v | measured | [1G-E] formula | mass-consistent |
  |---|---|---|---|---|
  | 0.737 | −0.8 | 1.0896 | 1.1412 | 1.0896 |
  | 0.627 | −0.8 | 0.8434 | 0.8777 | 0.8434 |

- **Alternative closure.** Void matter might carry the same field δ_w. Then
  `σ²_int → ∫P_R(1 + δ_v² ξ_w)ξ_E dr`. This also gives values below [1G-E]'s.

**Outcome:** the decomposition at δ_v = −1 is **CONFIRMED**. The δ_v scaling
is **REFUTED** (GE-F1).

### 4.3 Closures E3 and E4 (item 3)

**Fourier map.** `P_E(k) = ∫ξ_L(r/s)e^{−ik·r}d³r = s³P_L(ks)`, so
`Δ²_E(k) = k³s³P_L(ks)/2π² = Δ²_L(ks)` exactly: the Jacobian cancels in Δ².
The script evaluates the spectrum at `kl = k·s` and the kernel at k (lines
162–167), which is right. My real-space route with `ξ_L(r/s)` gives the same
σ_int to 3.5e−6. **CONFIRMED.**

**Direction.** Walls hold all the mass in the fraction f_w of the volume. In
the mass-conserving comoving coordinate, a Lagrangian volume therefore maps
to `f_w` times itself: lengths scale by `s = f_w^{1/3} < 1`, and Eulerian r
corresponds to Lagrangian r/s. So the compressed σ_int is the smaller one.
This agrees with the tracker's regional law `a_w,reg³ = (1−f_v)a_D³/f_wi`
([1G-C] Sec. 5), since `D_wall/γ_w0 = f_w^{1/3}`. **CONFIRMED.**

**"s = 1 is the upper bracket"** (lines 86–87). This is true only within E3. With
pair orientation independent of wall orientation, every volume-f_w map I
tried gives σ_int below the s = 1 value. It also gives σ_int *below the
isotropic primary*, so the primary is not the lower end of the E4 range.

σ_int at a = 15 (the last three rows are illustrative maps):

| Map | [GM] σ_int | [GM] σ total | [NW15] σ_int | [NW15] σ total |
|---|---|---|---|---|
| isotropic s = f_w^{1/3} (primary) | 1.093 | 1.572 | 1.006 | 1.357 |
| uncompressed s = 1 | 1.464 | 1.850 | 1.267 | 1.561 |
| sheets diag(1, 1, f_w), orientation-averaged | 0.988 | 1.501 | 0.950 | 1.316 |
| filaments diag(√f_w, √f_w, 1), orientation-averaged | 1.065 | 1.553 | 0.991 | 1.346 |
| void shell, tangential stretch 1.7, in-plane pairs (beyond E3) | 1.987 | 2.286 | 1.764 | 1.985 |

The last row matters physically. Void shells are tangentially stretched: the
shell radius grows by 1.7151 at shell crossing ([SvdW04] line 2163; 1.697 in
[JLH13] line 1345). If pairs lie in the same wall (orientation correlated
with the wall, which E3 excludes), σ_int exceeds the s = 1 value.

Mass conservation on large scales also pushes cross-void pairs toward s → 1.
So [compressed, uncompressed] is a sensitivity, not a bracket, and the
uncertainty runs both ways.

**Outcome: CONFIRMED_WITH_CAVEAT** (GE-F3). E3 is an untested idealisation,
as [1G-E] says. The [SvdW04] ridge (line 450: the void "develops a ridge at its
boundary") is a mechanism that correlates wall density with void
positions.

### 4.4 Monte Carlo (item 4)

**Method review:**
- **Periodic box.** A box of 30a is 15 times the covariance support (2a). The
  k-d tree query with `boxsize` is an exact periodic coverage test.
- **Sampling.** Directions and radii (`u^{1/3}`) inside the ball are correct.
- **Shot-noise subtraction.** `E[p̂(1−p̂)] = p(1−p)(1 − 1/N)`, so
  `mean(p̂(1−p̂))/(N−1)` is an unbiased estimate of the binomial term. The
  formula is right.
- **Realisation intensity.** For a binomial process with N balls,
  `P(uncovered) = (1 − V/L³)^N`. This differs from `exp(−NV/L³)` by about 1e−4.
  So the formula evaluated at the realisation's own count is the correct
  conditional expectation. The change is a legitimate variance reduction and
  hides no model error. My lattice ensemble shows this:
  - at the nominal intensity, the ensemble means agree with the formula
    (σ²_part: [GM] +0.3 ± 1.2%, [NW15] −0.05 ± 0.9%; ξ_w within 1σ at
    u = 0.25, 0.5, 1.0 and 1.5);
  - conditioning on the realised count cuts the per-realisation rms scatter
    of σ²_part from 5.6% to 1.9% ([GM], box 16a). A single realisation at
    the nominal intensity can miss by 14%, the same size as the reported
    first-run failure.

**Robustness of the gate.** I re-ran the phase's own `monte_carlo_boolean`
with 15 other seeds (comparison only):

| | [GM] | [NW15] |
|---|---|---|
| gated max error, seed 20260929 | 1.51% | 0.91% |
| gated max error, 16 seeds: min / median / max | 1.00 / 3.1 / **5.03%** | 0.16 / 0.97 / 3.95% |
| seeds failing the 5% gate (realised intensity) | 1 of 16 (seed 12) | 0 of 16 |
| seeds failing at nominal intensity, final box | 3 of 16 | 1 of 16 |
| main driver of the gated max | σ²_part ball variance (13 of 16) | σ²_part (12 of 16) |
| spread (sd) of σ²_part MC/analytic − 1 | 3.1% | 1.5% |

So "checked … to ≤ 1.5%" (line 42) is one favourable draw; the method's
precision is about 3%. With the same seed and the final box, the
nominal-intensity comparison already passes (1.62% / 1.67%). The box
enlargement, not the change of intensity, is what removed the failure.

**The first-run note.** It says "2% fewer balls, which shifts f_w by 4.5%".
Under the model, 2% fewer balls shift f_w by λV × 2%: 2.7% ([GM]) or 2.0%
([NW15]). The first-run configuration is not recorded, so the 14% cannot be
reproduced.

**Outcome:** the formula is **CONFIRMED** independently. The stated
precision and the first-run account are **CONFIRMED_WITH_CAVEAT** (GE-F5).

### 4.5 The σ numbers (item 5)

**Inputs, recomputed independently:**

| Quantity | [1G-E] | Independent |
|---|---|---|
| ω_m,eff [GM] / [NW15] | (1G-A) 0.120475 / 0.130937 | 0.120475 / 0.130937 |
| D_wall(t0) | 0.87679 / 0.94551 | 0.876792 / 0.945510 |
| R = 8/h_dressed | 10.9544 / 13.1148 Mpc | 10.9544 / 13.1148 |
| EH98 Planck σ(8/0.674) with qplus(0) = 0.787813 | 0.835689 | 0.835689 |
| anchor 0.8111/σ | 0.970577 | 0.970577 |
| no-partition σ_int (ξ_w = 0, s = 1) | 0.9121 / 0.8910 | 0.912143 / 0.891045 ([1G-C] artifact: 0.912143 / 0.891045) |

**Results:**
- **The table.** All 60 entries of the [1G-E] Sec. 4 table (σ_part, σ_int
  compressed/uncompressed and σ total, for a = 5–30 and both sets) agree with
  the artifact and with my real-space values at 3 decimals. The largest
  relative difference is 3.5e−6.
- **The δ_v table.** It is reproduced exactly with [1G-E]'s own formula. With
  the mass-consistent formula it reads:

  | δ_v | [GM] reported | [GM] mass-consistent | [NW15] reported | [NW15] mass-consistent |
  |---|---|---|---|---|
  | −1 | 1.572 | 1.572 | 1.357 | 1.357 |
  | −0.9 | 1.493 | **1.435** | 1.297 | **1.249** |
  | −0.8 | 1.418 | **1.298** | 1.242 | **1.142** |

- **Headline ranges.** The minimum is at a = 5, compressed, δ_v = −0.8. The
  ranges become 0.82–2.12 ([GM], was 0.93–2.12) and 0.80–1.74 ([NW15], was
  0.89–1.74).
- **The [1G-C] recovery.** It holds (relative agreement 1.5e−9 and 2.0e−9),
  but it is not independent. It reuses the same spectrum, growth and anchor
  code, and with ξ_w = 0 it only re-tests the kernel quadrature that the pair
  identity already tests.

**Outcome: CONFIRMED** for δ_v = −1. For the δ_v rows, see GE-F1.

### 4.6 Interpretation and sources (item 6)

**The [W09] quote.** [1G-E] line 74 quotes "voids of a characteristic
diameter 30 h⁻¹ Mpc" (line 277). The quote is verbatim, but it stops
mid-sentence. [W09] lines 277–285 read:

> "Voids of a characteristic diameter 30h⁻¹ Mpc are observed to fill 40–50%
> of the universe at the present epoch [HV]. In addition there are numerous
> minivoids … Together voids of all sizes appear to dominate the volume …
> both the dominant voids and minivoids are assumed to be characterized by
> the same negatively spatial curvature scale."

So in [W09]'s two-scale model the void phase, and hence f_v0 (0.737 or
0.627), includes the minivoids. Only 40–50% of the volume is in 30 h⁻¹ Mpc
voids. E2 puts all of f_v0 into 15 h⁻¹ Mpc balls,
which the source does not support.

**A [W09]-consistent population.** I used two independent Boolean
populations: `1+ξ_w = exp(Σλ_iγ_i)`, with 15 h⁻¹ Mpc voids filling 40–50% and
minivoids of radius 1–4 h⁻¹ Mpc filling the rest up to f_v0. This gives:

| Parameters | σ_part | σ total, compressed | σ total, uncompressed | ratio to 0.8111 (compressed) |
|---|---|---|---|---|
| [GM] | 0.61–0.79 | 1.02–1.23 | 1.26–1.48 | 1.25–1.52 |
| [NW15] | 0.60–0.75 | 1.04–1.20 | 1.23–1.40 | 1.29–1.48 |

These values lie inside [1G-E]'s a = 5–30 range. They are 22–35% ([GM]) and
11–23% ([NW15]) below the "primary" 1.57/1.36 (GE-F2).

**The model's void size.** In the Boolean model at λV = 1.34, a void point is
covered by 1.8 balls on average, and the void phase is a merged network. The
mean void chord is 42 h⁻¹ Mpc ([GM]) or 34 h⁻¹ Mpc ([NW15]), against 20 h⁻¹ Mpc
for an isolated 15 h⁻¹ Mpc ball. The mean wall chord is 15 or 20 h⁻¹ Mpc. So
`a` is not the observable void radius. The walls are thick, not thin sheets.

**"1.7–1.9 × Planck's linear σ8"** (lines 54 and 175–176):
- The arithmetic is right: 1.572/0.8111 = 1.94 and 1.357/0.8111 = 1.67.
- The comparison mixes kinds, which [1G-E] states. The partition is
  nonlinear, while the wall part is linear theory extrapolated to
  σ_int ≈ 1.1. So the quantity is a hybrid, not a full nonlinear variance.
- It also compares balls of different Lagrangian mass. The [GM] dressed ball
  holds 0.66 of the mass in Planck's R8 sphere, and the [NW15] ball holds
  1.23 of it. At [1G-A] Sec. 6.4's frame-free equal-mass convention (a), σ is
  1.437 ([GM]) and 1.419 ([NW15]), ratios 1.77 and 1.75.
- Together with the W09-consistent populations, the fair statement is
  "about 1.25–1.9×, depending on the void population and radius convention".

**E1 against [SvdW04] and [JLH13].** At shell crossing the void interior has
`1+Δ = 0.1982` ([SvdW04] voids.tex line 2159). [SvdW04] line 1420 calls
δ → −0.8 "the density we associate with a void". [JLH13] gives 0.2047
(voids_mnras.tex line 1343) and defines voids by `ρ_v = 0.2ρ_m` (line 73).
Voids empty further afterwards ([SvdW04] line 449: "near-empty
configuration Δ = −1 at the centre").

So E1 (δ_v = −1) is the tracker's idealisation ([1G-C] Sec. 3: `ρ_v = 0`).
It is not the excursion-set void definition that the 1G-F recommendation
would import; that definition sits at the δ_v = −0.8 end, exactly where
GE-F1 bites.

**Other readings:**
- "The void/wall partition and the wall-internal growth contribute
  comparably" is confirmed: 1.130 vs 1.093 and 0.911 vs 1.006.
- `ρ_w = 3.8⟨ρ⟩` is confirmed (3.80).
- "The partition term alone is 0.4–1.4" is confirmed (0.399–1.382).

**Outcome: CONFIRMED_WITH_CAVEAT**, except that the attribution of E2's
primary to [W09] is **REFUTED** (GE-F2).

### 4.7 Evidence classes, consistency and reproducibility

- **Section classes.**
  - Sec. 2 `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` is appropriate: the
    decomposition is derived under E1–E3, and the numbers depend on E2 and
    E4.
  - Sec. 3 `NUMERICALLY_CORROBORATED` is acceptable for the Boolean formula,
    but the [1G-C] recovery is a shared-code consistency check (Sec. 4.5).
- **Inventory.** I checked 149 numeric inventory entries against the
  artifact at their stated rounding. All agree. Four full-precision entries
  differ from this Linux machine in the last bits, for example
  `pair_identity_rel_err` 1.69435e−12 against 1.69412e−12. This is an ordinary
  platform floating-point difference. All seeded Monte Carlo values,
  including the ball counts 8569/6322, are identical across platforms.
  The inventory repeats the GE-F1 formula (`model.formula`).
- **Report tables.** They agree with the artifact, except for the numeric
  summaries listed in GE-F6.
- **Reproducibility.** The claim of identical output on both interpreters is
  **CONFIRMED** on this machine (3.13.12 and 3.11.15, byte-identical results).
  The owner's Windows runs are not verifiable here. The stated runtime "(a few
  seconds)" is wrong here: 76–81 s.
- **Section reference.** The script docstring cites "[1G-E] Sec. 3" for the
  model; the model is in Sec. 2.

### 4.8 The approved token

`TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"`
with E1–E4 ([1G-E] Sec. 6 item 3).

**The class is right.** No stronger class is justified:
- E2's population is an input;
- E4 is a closure;
- E3 is untested.

No weaker class is needed: under E1–E4 the δ_v = −1 result is derived and
reproduced.

**The recorded meaning needs four corrections:**
1. The formula holds only at δ_v = −1, or it must be replaced by the
   mass-consistent form (GE-F1).
2. E2's single radius at the full f_v0 is an idealisation, not a [W09]
   statement (GE-F2).
3. E4's s = 1 is a sensitivity, not a bracket (GE-F3).
4. The internal part is linear theory, so the statistic is a hybrid.

(Outside the audited checkpoint: the lead's successor record at `ad1ac35`,
`phase1g_e_status_addition_successor.md` Sec. 1, repeats
`σ² = δ_v² σ²_part + σ²_int` and describes E2's radius as "15 h⁻¹ Mpc from
[W09]"; both readings are affected.)

**Outcome: CONFIRMED_WITH_CAVEAT.**

## 5. Findings

| Id | Severity | Resolution class | Title |
|---|---|---|---|
| GE-F1 | MEDIUM-HIGH | OWNER_DECISION | The non-empty-void formula `σ² = δ_v² σ²_part + σ²_int` violates mass conservation; the δ_v sensitivity and the range lower edges are wrong |
| GE-F2 | MEDIUM-HIGH | OWNER_DECISION | The primary void model (one radius, 15 h⁻¹ Mpc, at the full f_v0) is attributed to [W09], which says such voids fill 40–50% |
| GE-F3 | MEDIUM | OWNER_DECISION | E4: [compressed, uncompressed] is not a bracket; under E3 anisotropic compression lowers σ_int below the primary |
| GE-F4 | MEDIUM | OWNER_DECISION | Radius convention (b) is used for the Planck comparison without its 1G-A status; the "f_v0: about 16%" spread is mostly the convention |
| GE-F5 | LOW-MEDIUM | OWNER_DECISION | Monte Carlo precision and gate robustness are overstated; the first-run note is inconsistent and not reproducible |
| GE-F6 | LOW | UNAMBIGUOUS_ERRATUM | Numeric summaries in Secs. 3 and 5 do not match the tables |
| GE-F7 | LOW | UNAMBIGUOUS_ERRATUM | Cosmetic: script section citation and runtime statement |

**GE-F1 (MEDIUM-HIGH).**
- **Problem.** For δ_v ≠ −1, the mass-consistent variance is
  `δ_v²σ²_part + (f_w − f_vδ_v)²σ²_int` (Sec. 4.2; checked directly on a
  lattice).
- **Effect at a = 15, compressed, δ_v = −0.8.** σ is 1.298 ([GM]) and 1.142
  ([NW15]), not 1.418 and 1.242. The change is −17%/−16%, not "about −9%".
- **Headline ranges.** The lower edges fall from 0.93 to 0.82 and from 0.89 to
  0.80. The CLAUDE.md reading "the range is 0.9–2.1" becomes 0.8–2.1.
- **Unaffected.** The δ_v = −1 (tracker) numbers.
- **Why it matters.** The [SvdW04]/[JLH13] void definition sits at δ_v ≈ −0.8.
- **Locations.** [1G-E] lines 30, 46–49 (range column), 67–70, 89–91,
  155–161 and 184; inventory `model.formula` and
  `headline_8_h_inv_Mpc.range_*`.

**GE-F2 (MEDIUM-HIGH).**
- **Problem.** [W09] lines 277–285 assign 40–50% of the volume to 30 h⁻¹ Mpc
  voids and the rest of f_v0 to minivoids.
- **Effect.** A [W09]-consistent two-population Boolean model gives 1.02–1.23
  ([GM]) and 1.04–1.20 ([NW15]), compressed, against 1.57 and 1.36. The ratio
  to Planck's linear σ8 falls to 1.25–1.52.
- **Also.** In the Boolean model, `a` is not the observable void size (mean
  void chord 42/34 h⁻¹ Mpc).
- **Unaffected.** The a = 5–30 range contains these values.
- **Locations.** [1G-E] lines 44–57, 72–78 and 175–176; inventory
  `headline_8_h_inv_Mpc`.

**GE-F3 (MEDIUM).**
- **Problem.** Lines 86–87 say "`s = 1` (no compression) is the upper bracket.
  Real walls are sheets and filaments, so their compression is anisotropic."
  This implies that anisotropy moves the value from the primary toward s = 1.
- **Evidence.** Under E3, sheets and filaments give σ_int 0.988 and 1.065
  ([GM]), below the primary 1.093. Void-shell tangential stretching with
  orientation-correlated pairs (beyond E3) gives values above s = 1.
- **Fix.** Line 181 ("+15–26% uncompressed vs compressed") should present E4
  as a two-sided sensitivity.

**GE-F4 (MEDIUM).**
- **Problem.** R = 8/h_dressed is [1G-A] Sec. 6.4 convention (b), which
  "presuppose[s] parts of the underived dressed map". [1G-A] calls (a) "the
  right comparison with ΛCDM predictions at fixed mass". [1G-C]'s primary was
  (a). [1G-E] states neither the convention nor its effect.
- **Effect.** At convention (a), σ total at a = 15 (compressed, δ_v = −1) is
  1.437 ([GM]) and 1.419 ([NW15]), against 1.572 and 1.357. The [GM]/[NW15]
  difference shrinks from 16% to 1.3%. So "f_v0: about 16% at a = 15"
  (line 183) is mostly the radius convention, since the two sets also differ
  in dressed H0.

**GE-F5 (LOW-MEDIUM).** See Sec. 4.4.
- **Precision.** The gated error is 1.0–5.03% across 16 seeds ([GM]), and
  seed 12 fails the phase's own 5% gate. "≤ 1.5%" is a single draw.
- **First-run note.** "2% fewer balls … shifts f_w by 4.5%" contradicts
  `f_w = e^{−λV}` (2.7% or 2.0%). The first-run configuration is unrecorded.
- **Unaffected.** The Boolean formula itself is confirmed independently.

**GE-F6 (LOW).** Three numeric summaries do not match the tables:
- line 180: the a = 5 → 30 factor is 1.56–1.87, not 1.7–1.9;
- lines 181–182: σ total changes by +14–26%, not +15–26% (σ_int by +25–35%);
- line 132: ξ_w ≈ 0.12 holds for [GM] only; [NW15] has 0.088.

**GE-F7 (LOW).**
- The script docstring cites "Sec. 3" for the model, which is in Sec. 2.
- The runtime "(a few seconds)" was 76–81 s here.

## 6. Proposed errata (exact old → new)

| # | File, line | Old | New | Proof |
|---|---|---|---|---|
| 1 | [1G-E] line 132 | `\| ungated u = 1.5 (ξ_w ≈ 0.12, noise-dominated) \| 4.7% \| 7.4% \|` | `\| ungated u = 1.5 (ξ_w ≈ 0.12 [GM], 0.088 [NW15]; noise-dominated) \| 4.7% \| 7.4% \|` | artifact: analytic ξ_w(u=1.5) = 0.12103 / 0.08794 |
| 2 | [1G-E] line 180 | `   - the void radius: a factor 1.7–1.9 in σ between a = 5 and 30 h⁻¹ Mpc;` | `   - the void radius: a factor 1.6–1.9 in σ between a = 5 and 30 h⁻¹ Mpc ([GM] 1.73–1.87, [NW15] 1.56–1.66);` | Sec. 4 table: 1.826/0.976, 2.120/1.226, 1.533/0.923, 1.743/1.117 |
| 3 | [1G-E] lines 181–182 | `   - the Eulerian mapping of the wall field: +15–26% (uncompressed vs`<br>`     compressed);` | `   - the Eulerian mapping of the wall field: +14–26% in σ total, +25–35% in σ_int (uncompressed vs`<br>`     compressed);` | uncompressed/compressed σ total: [GM] 1.161–1.255, [NW15] 1.137–1.210; σ_int 1.253–1.347 |
| 4 | [1G-E] line 142 | `**R = 8 h⁻¹ Mpc** (10.95 Mpc for [GM], 13.11 Mpc for [NW15]).` | `**R = 8 h⁻¹ Mpc** (photon-normalised comoving radii 10.95 Mpc for [GM], 13.11 Mpc for [NW15]; [1G-A] Sec. 6.4 convention (b)).` | script line 184 `R = R_H_MPC / h` with dressed h equals 1G-A `dressed_8_over_h_wall_comoving` (10.954 / 13.115) |
| 5 | [1G-E] line 74 | `  - [W09] gives "voids of a characteristic diameter 30 h⁻¹ Mpc" (line 277),` | `  - [W09] gives "voids of a characteristic diameter 30 h⁻¹ Mpc" that "fill 40–50% of the universe", plus "numerous minivoids" (lines 277–280),` | [W09] observe.tex lines 277–280 (quote completion; the downstream choice is OD-2) |
| 6 | [1G-E] line 220 | `→ wrote artifacts\independent\phase1g_e_two_phase_sigma.json    (a few seconds)` | `→ wrote artifacts\independent\phase1g_e_two_phase_sigma.json    (about 1–2 minutes)` | measured 81 s (3.13) and 77 s (3.11) wall time here; about 3.2e7 k-d tree queries (1.6e7 per parameter set) |
| 7 | script line 6 | `Model ([1G-E] Sec. 3): empty voids (the tracker's rho_v = 0, [1G-C] Sec. 3)` | `Model ([1G-E] Sec. 2): empty voids (the tracker's rho_v = 0, [1G-C] Sec. 3)` | [1G-E] Sec. 2 is "Model", Sec. 3 is "Verification" |

The inventory `errata` entries hold the exact strings; this table escapes `|`
and shows line breaks as `<br>`. Every old string occurs exactly once in its
file at `6f7937c`.

Errata 4 and 5 are documentary parts of GE-F4 and GE-F2. The scientific
consequences of those findings are owner decisions.

## 7. Items for owner decision

1. **OD-1 (GE-F1).** Choose one of two options:
   - replace the δ_v formula by `δ_v² σ²_part + (f_w − f_v δ_v)² σ²_int`
     (uniform void interiors, walls carry the rest) and update the δ_v table
     (−0.9: 1.435/1.249; −0.8: 1.298/1.142), the "about −9%" (about −16 to
     −17%), the range lower edges (0.82, 0.80) and the inventory;
   - or restrict the formula and the table to δ_v = −1.

   In either case, update the CLAUDE.md "range is 0.9–2.1" reading and the
   token's recorded meaning.
2. **OD-2 (GE-F2).** Decide the primary void population. Either keep one
   radius at the full f_v0 as an explicit idealisation not attributed to
   [W09], or adopt a [W09]-consistent population (σ ≈ 1.0–1.2). Restate the
   "1.7–1.9×" reading accordingly.
3. **OD-3 (GE-F3).** Reword E4 as a two-sided sensitivity, and drop "upper
   bracket" or restrict it to "within E3".
4. **OD-4 (GE-F4).** Report the equal-mass convention (a): 1.437 and 1.419,
   ratios 1.77 and 1.75. Alternatively, justify (b) for a comparison with
   Planck. Revise "f_v0: about 16%".
5. **OD-5 (GE-F5).** Restate the Monte Carlo precision as a scatter across
   seeds. Optionally, gate on an ensemble mean or a larger ball sample.
   Correct or remove the "2% → 4.5%" sentence, or record the first-run
   configuration.
6. **OD-6 (token).** Keep the approved value. Record its meaning with the
   four corrections of Sec. 4.8.

## 8. Verdict and readiness for tagging

**Verdict: `ACCEPT_WITH_CORRECTIONS`.**
- **Why not REJECT.** The phase's load-bearing result is independently
  reproduced to every printed digit: the two-phase σ at δ_v = −1 under the
  stated E1–E4, for a = 5–30 and both parameter sets. Its mathematical
  ingredients are correct, and the Boolean formula is confirmed by an
  independent Monte Carlo.
- **Why corrections are needed.** Two MEDIUM-HIGH findings change stated
  quantitative readings: the δ_v sensitivity and range, and the "primary"
  value attributed to [W09].

**Tag readiness: `NOT_READY_OWNER_DECISION_REQUIRED`.** GE-F1 to GE-F5 change
a formula, numbers, or the interpretation recorded under an approved token.
Each needs an owner decision; errata alone are not enough.

## 9. Limitations

- **Void sizes.** The minivoid radii (1–4 h⁻¹ Mpc) are illustrative. The
  cited minivoid source (Tikhonov & Karachentsev 2006) and the Hoyle & Vogeley
  void catalogue were not fetched, so the [W09]-consistent numbers are a
  sensitivity, not a replacement value.
- **Anisotropic maps.** The maps in Sec. 4.3 are simple illustrative
  closures. They show that the claimed bracket fails; they do not bound the
  true E4 uncertainty.
- **Planck inputs.** They were taken as quoted in the 1G-A script; [P18] was
  not re-read line by line.
- **Owner platform.** The Windows (3.14.3 / 3.11.9) results could not be
  run. The full test suite was not run, as the brief requires.
- **Novelty.** The claim that these are "the first Timescape numbers of the
  nonlinear mass-variance type" was not checked against the literature.
- **Approximations.** My lattice Monte Carlo resolves the ball at 0.05a. The
  lattice-to-continuum ball difference (+0.24% in σ²_part) is accounted for
  by comparing with the analytic value on the same lattice. My ξ_L
  reproduces k-space σ_L² to 2e−5.

## 10. Preservation statement

I created only this report and its inventory in the main tree. The scratch
scripts and outputs are in the session scratch directory `audit_e/`. I edited,
staged, committed, pushed or tagged nothing else. Running the phase script
rewrote the git-ignored 1G-E artifact inside the audit worktree; I restored
the supplied bytes afterwards (SHA-256 `94c16cc1…3612`).
