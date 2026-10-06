# Phase 1G-H — Global matter-variance definition and minimal closure

Classification: `RESEARCH_PHASE_WITH_EXPERIMENTAL_RUNTIME` (conditional,
model-internal, `NON_OBSERVATIONAL`). Date: 2026-10-06.
Base: `main` = `origin/main` = `8d3cdd0533035858c42269cb1dff1a20dcafc7da`
(PR #4 merge, the frozen F/G checkpoint), local branch
`phase-1g-h-global-variance-closure` (first commit: the F/G freeze-status
alignment, `phase1g_fg_freeze_status_successor.md`).
Remote: the session branch `ccr-555e67be-u11yht`, pushed with the owner's
approval of 2026-10-06 (Sec. 1); not merged into `main`.
Companions: [`phase1g_h_global_variance_closure_inventory.json`](phase1g_h_global_variance_closure_inventory.json),
[`phase1g_h_global_variance_closure_validation.md`](phase1g_h_global_variance_closure_validation.md).
Runtime: `src/timescape_fsigma8/global_variance.py` (experimental).
Evidence: `scripts/phase1g_h_global_variance_closure_numerics.py` (writes the
git-ignored `artifacts/independent/phase1g_h_global_variance_closure.json`
and three figures); single cases: `scripts/phase1g_h_global_variance_case.py`
with the configurations in `scripts/phase1g_h_configs/`.

Cited as [GM] arXiv:2511.17160v2; [W07] arXiv:0709.0732v2; [W09]
arXiv:0909.0749v2; [NW15] arXiv:1410.3470v2; [JLH13] arXiv:1304.6087v2;
[SvdW04] astro-ph/0311260; [EH98] astro-ph/9709112; and the frozen project
records [1G-A] … [1G-G] with their owner-decision and successor records
(Sec. 13). Equations (H1)–(H24) are new to this report unless a primary
source is named next to them.

## 1. Scope, authorisation and verdict

**Authorisation.** The owner's task statement of 2026-10-06 authorises this
research and development phase: reading the sources, new derivations,
numerical experiments, new experimental modules, scripts, configurations,
tests and reports. It authorises exploring additional hypotheses in
isolated experimental implementations, named, motivated and compared, and
does **not** authorise promoting them to project law. It authorises local
commits only: no push, pull request, merge, tag, freeze or release, and no
change of a scientific token or observational authorisation.

**Later owner approval** (2026-10-06, after these records were committed):
pushing the phase commits, and then this documentation update, to the
session branch `ccr-555e67be-u11yht`. Nothing else is approved: no pull
request, merge, tag, freeze, release or audit (Sec. 9, H-OD5).

**Distinction recorded as asked.** Everything below that goes beyond the
approved records is an explicitly named hypothesis (H-A6 … H-A8, the seed
closures, the homogeneity-premise readings). None is promoted to a Timescape
law; the owner decides (Sec. 9).

**Verdict.**

1. **A — the definition is closed** (Sec. 2). The Timescape global-mean
   linear statistic is the rms of the first-order, ensemble-mean response of
   the global density contrast of a Lagrangian top-hat region to the early
   Gaussian field, on the dust foliation, relative to the global volume mean,
   at the present epoch, with the radius fixed by an explicit convention
   (recommended: `8 h̄⁻¹ Mpc` of present volume-average proper length, i.e.
   `R·H_D0 = 800 km/s`). In the FLRW limit it is the standard linear σ8.
2. **The structure is derived** (Sec. 3). Under the regional laws A1–A5 of
   [1G-C], with each empty void expanding as Milne independently of its
   surroundings (H-A6), the global linear propagator of *any* Lagrangian
   region is exactly
   `G(k) = (1 − p(k))·D_W + p(k)·D_V` (H9), where p is the fraction of the
   early contrast carried by the void volume. `D_W` and `D_V` follow in closed
   form from the tracker and are verified independently: `D_W = 0.2306`,
   `D_V = 7.133` for [GM] (f_v0 = 0.737), `0.3527` and `11.33` for [NW15]
   (f_v0 = 0.627). This removes 1G-D's restriction of the mode decomposition
   to super-cell regions.
3. **One input is missing, and it is decisive** (Sec. 4). Nothing approved
   determines the void share p(k), which is 1G-D's void-onset response
   (`VOID_ONSET_RESPONSE = EXTERNAL_CLOSURE_INPUT`) in another normalisation.
   The statistic is affine in p with slope `D_V − D_W ≈ 6.9` ([GM]) and
   `≈ 11.0` ([NW15]), so p controls it.
4. **B — the calculation is closed conditionally** (Sec. 5). Given an explicit
   void-share closure, the chain from the declared inputs to the number is
   complete, implemented, convergent and tested. At `8 h̄⁻¹ Mpc` (direct A_s
   normalisation; Planck-anchored values in brackets), with the
   peak-background-split seed closure approved in 1G-D:
   **1.121 (1.088)** for [GM] and **1.057 (1.026)** for [NW15]; with the seed
   scale of the project's own 1G-F void population: **0.811 (0.787)** and
   **0.816 (0.792)**. A closure-independent interval from the monotone
   response and the background's own homogeneity premise ([W09], read as
   rms ≤ 10% in the top hat of 100 h̄⁻¹ Mpc) is **[0.261, 0.998]** ([GM]) and
   **[0.369, 1.162]** ([NW15]), direct normalisation.
5. **C — not reached** (Sec. 7). A Timescape *prediction* needs a derivation
   of p(k) from void formation consistent with the tracker's f_v(t); an
   observational comparison needs, in addition, the dressed light-cone and
   tracer reduction (unchanged firewall). The minimal next input is identified
   precisely in Sec. 7.
6. **Supporting results** (Sec. 6): the complete two-phase covariance with
   phase-conditional normalisation and every cross term; 1G-E's formula as its
   independent special case; and a constructive proof that the nonlinear
   hybrid variance at 8 h⁻¹ Mpc is not fixed by the acquired constraints
   (two realisable laws with identical f_v0, partition covariance,
   wall-field covariance and mass normalisation give 0.97 and 0.39).

Every number here is conditional and model-internal. `SIGMA8_AUTHORIZATION`,
`FSIGMA8_AUTHORIZATION`, `RSD_AUTHORIZATION`, `OBSERVATIONAL_AUTHORIZATION`
and `UNIQUE_TIMESCAPE_PREDICTION` remain `NOT_GRANTED`;
`LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` remains `NOT_DERIVED` (a proposal is
in Sec. 9).

## 2. Which σ8 is being defined (A)

### 2.1 Four objects kept distinct

| Object | Definition used here | Status after 1G-H |
|---|---|---|
| Wall-internal linear σ | Linear contrast relative to the **wall** mean, wall growth in t (A1–A5), [1G-C]; 0.834 / 0.935 at equal mass | unchanged; not a global statistic |
| **Global linear σ** | First-order response of the contrast relative to the **global** volume mean, Lagrangian top hat, Sec. 2.2 | defined (A); computed given p (B) |
| Global nonlinear σ | Variance of the actual (or a declared nonlinear model) mass distribution in balls | not closed; Sec. 6 shows the missing joint law |
| Data-inferred σ8 | Tracer, selection, light-cone geometry and inference specified | out of scope (firewall) |

### 2.2 The definition

- **Field.** The rest-mass density ρ of the single irrotational dust of
  [GM] Sec. 3 (cold dark matter and baryons after decoupling; no radiation).
  For dust, mass density equals energy density in the dust rest frame.
- **Foliation, time, epoch.** The dust-orthogonal foliation of [GM] Sec. 3,
  time t the dust proper time (the tracker's common, volume-average time).
  The present epoch t0 is where `f_v(t0) = f_v0` (dressed z = 0 for wall
  observers). Masses are integrated on these slices, so no projection of the
  mass current is needed: `M_L = ∫_L ρ √b d³X` is conserved exactly. Another
  foliation (for example the wall observers' proper time) would need the
  projected current `−n_μ J^μ` and its own volume measure; it is not used.
- **Global mean.** The Buchert volume average on the same slice,
  `⟨ρ⟩_D = M_D/V_D` ([GM] Sec. 3.1), D the observable-universe-sized domain.
- **Region and contrast.** A Lagrangian region L is a fixed set of dust
  elements. Its global contrast is

  ```text
  1 + δ_L(t) = [M_L / V_L(t)] / [M_D / V_D(t)]                                  (H1)
  ```

  with V the Riemannian volume on the slice.
- **Window and scale.** L is the set of elements whose Lagrangian labels (the
  photon-normalised comoving positions in the early universe, where every
  frame agrees to O(f_v)) lie in a ball of radius R. The window is normalised,
  `W_R(q) = 3/(4πR³)·1[|q| < R]`, with Fourier transform
  `W(x) = 3(sin x − x cos x)/x³`.
- **Ensemble.** Centres are uniform in Lagrangian space, so regions are
  sampled by mass, not by present volume. Mass- and volume-weighted means
  differ at second order (`E_mass[1/(1+δ_L)] = 1` for an equal-mass tiling);
  at first order `E[δ_L] = 0`. The statistic is the **connected** variance
  `⟨δ_L²⟩ − ⟨δ_L⟩²`.
- **Linear.** Write the early field as `δ_0 = δ_ℓ + δ_s`, a long mode plus
  everything else. The first-order response is the derivative of the
  ensemble mean of δ_L with respect to the long mode, at fixed small-scale
  statistics, evaluated at the statistically homogeneous two-phase tracker
  state (not at the homogeneous FLRW state, where no void exists). By
  Gaussian integration by parts this is the propagator
  `G(k) = ⟨δ_L(k) δ_0*(k)⟩′/P_0(k)`, the projection of the true region
  contrast on the early linear field. The global linear statistic is

  ```text
  σ²_lin(R) = ∫ dln k Δ²_u(k) G(k, t0)² W²(kR)                               (H10)
  ```

  with `Δ²_u` the photon-normalised matter-era spectrum at unit growth
  ([1G-A] Sec. 6.3, `D/a_photon → 1`). It is the variance of the linearly
  extrapolated field, exactly as σ8 is in ΛCDM: it does not claim that the
  physical field is linear at R.
- **Real-space form.** Equivalently

  ```text
  σ²_lin(R) = ∫_0^{2R} P_R(r) ξ_lin(r) dr,   ξ_lin(r) = ∫ dln k Δ²_u G² j0(kr),  (H11)
  P_R(r) = (3r²/R³)(1 − 3r/4R + r³/16R³),
  ```

  P_R being the pair-separation density in a ball. Nothing here needs a
  Fourier basis of the *late*, inhomogeneous geometry: the response is
  computed in Lagrangian coordinates, where the early field is statistically
  homogeneous and isotropic on a flat background ([GM] choose K_D = 0). This
  is what makes the spectral form legitimate without the underived global
  dressed spatial map.
- **FLRW limit.** Without voids `G = D(t)` and (H10) is the standard top-hat
  linear variance ([JLH13] Eq. (2)); with f_v0 → 0 the photon-normalised
  growth is EdS, `D_W → 1 − (5/6) f_v0` (tested).
- **Eulerian smoothing is a different statistic.** In FLRW, Lagrangian and
  Eulerian top hats agree at first order. Here the zeroth-order state is
  inhomogeneous below the cell scale (walls at `1/f_w` times the mean), so a
  fixed Eulerian sphere at late times is a different, nonlinear object.

### 2.3 What "8 h⁻¹ Mpc" means

The radius is a mandatory, explicit convention (the `LagrangianRadiusSpec`
of 1G-B), always resolved to photon-normalised comoving Mpc:

| Convention | R (photon-comoving) | Meaning | Needs |
|---|---|---|---|
| **(c) recommended** | `R = (L/h̄)/γ_w0`, L = 8 | the region whose present volume-average proper radius is `8/h̄` Mpc, `h̄ = H_D0/100`; equivalently `M = (4π/3)⟨ρ⟩_D0 (8/h̄ Mpc)³` (H24) and `R·H_D0 = 800 km/s` | only global-average quantities on the slice |
| (a) | `R = R_ref (ω_ref/ω_m,eff)^{1/3}` | equal Lagrangian mass to ΛCDM's M8 | a reference model; the comparison convention |
| (b) | `R = L/h_dressed` | wall-comoving length with the dressed h | the underived dressed spatial map |

Convention (c) is the faithful generalisation of ΛCDM's definition
(`R·H0 = 800 km/s` with the background's own expansion rate) to a background
whose global expansion rate is the bare H_D0. Using the dressed h in a length
(b) does not by itself establish a dressed spatial map. Fixed radius and
fixed mass are different statistics: (a) is reported side by side as a
separate diagnostic, never as an equivalent of (c). For [GM]: R = 10.104 Mpc
(c), 12.570 Mpc (a), 10.954 Mpc (b); for [NW15]: 11.781, 12.226, 13.115 Mpc.

## 3. Exact two-phase kinematics and the global propagator

### 3.1 Exact identities (mass conservation, volume additivity)

For a region with void volume fraction `f_v,L`, phase densities `ρ_w,L`,
`ρ_v,L` and the global values `f_v`, ρ_w, ρ_v = x ρ_w on the same slice,

```text
1 + δ_L = [f_w,L ρ_w,L + f_v,L ρ_v,L] / [f_w ρ_w + f_v ρ_v].                    (H2)
```

For empty voids (the tracker, ρ_v = 0) all of M_L sits in walls. Define the
region's reference wall volume `V_w0 = M_L/ρ_w`, its reference void volume
`V_v0 = V_w0 f_v/f_w`, `1 + δ_w,L = V_w0/V_w,L` and `1 + ε_L = V_v0/V_v,L`
(ε > 0: less void volume than average). Since `⟨ρ⟩ = f_w ρ_w`,

```text
1/(1 + δ_L) = f_w/(1 + δ_w,L) + f_v/(1 + ε_L)        (exact; specific volumes add)  (H3)
δ_L = f_w δ_w,L + f_v ε_L + O(2)                                                    (H4)
δ_L = [f_w δ_w + x f_v δ_v − (1 − x) δf_v] / (f_w + x f_v) + O(2)                    (H5)
```

(H5) linearises (H2) for finite-density voids (δ_v the void density contrast
relative to the global void density). With empty voids a Lagrangian region
owns the void bubbles enclosed by its wall matter; bubbles are assigned by
their seed's Lagrangian position, which is unambiguous at the matching epoch,
where bubbles are much smaller than R. Tests: (H2)–(H3) against explicit
mass/volume bookkeeping (10⁻¹²), (H4)–(H5) against central differences (10⁻⁸).

### 3.2 Regional evolution in the tracker

**Assumptions.**
- **A1–A5** ([1G-C] and its owner decisions): walls are Einstein–de Sitter
  regions in the common time t, which the wall matter clocks (A5).
- **H-A6, void autonomy (new):** each empty void region expands as Milne,
  `V_v ∝ t³`, independently of the density of the surrounding walls, with no
  wall–void volume transfer (1G-G (G5) with J = 0).
- Growing modes only (regular growing-mode initial conditions): the wall
  bang-time mode t⁻¹ and decaying void modes are absent.

Then, for any Lagrangian region, the wall contrast obeys the EdS equation in
t and the void-volume perturbation is frozen:

```text
δ_w,L(t) = C t^{2/3} + C′ t^{−1},       ε_L = const.                                  (H6)
```

Split the region's contrast at the matching epoch t_i (last scattering, an
explicit redshift z_LS = 1090 as in 1G-D/1G-F) into a void share p and a wall
share 1 − p: `f_v,i ε = p δ_L(t_i)`, `f_w,i δ_w(t_i) = (1 − p) δ_L(t_i)`. Then

```text
δ_L(t) = δ_L(t_i) [ (1 − p) (f_w(t)/f_w,i) (t/t_i)^{2/3} + p f_v(t)/f_v,i ].          (H7)
```

From [GM] Eqs. (5.4)–(5.6) and text p. 25 (`1 + z = γ_w a_w0/a_D`,
`γ_w = 1 + f_v/2`, `a_D ∝ t f_v^{−1/3}`, `f_v = t/(t + τ)`), exactly,

```text
(t0/t)^{2/3} / (1 + z(t)) = γ_w0 f_w0^{1/3} / (γ_w(t) f_w(t)^{1/3}).                   (H23)
```

With the photon normalisation `δ_L(t_i) = δ_u/(1 + z_LS)` this gives the
two growth factors

```text
D_W = γ_w0 f_w0^{4/3} / (γ_w,LS f_w,LS^{4/3}),    D_V = f_v0 / [f_v,LS (1 + z_LS)],       (H8)
G(k, t0) = (1 − p(k)) D_W + p(k) D_V.                                                 (H9)
```

**Independent checks** (`two_phase_global_growth` fails closed): the closed
forms against the package tracker (≤ 2.2×10⁻¹⁶); the wall mode integrated in
common time on the package's regional background, `H_w = H_D − ḟ_v/(3f_w)`,
`4πGρ_w = 4πG⟨ρ⟩_D/f_w` (DOP853, rtol 10⁻¹¹; agreement 4.7×10⁻¹³); the void
volume integrated as `dV/dt = 3V/t` against `f_v a_D³` (7×10⁻¹⁵). A test
also recomputes D_W and D_V from a separate implementation of (5.5)–(5.6)
(10⁻¹¹), and a test evolves the wall exactly as a closed dust FLRW
(parametric spherical solution, independent of t^{2/3}) with constant ε,
inserts both in (H3) and recovers (H9) with an error falling as the
amplitude (ratios 10.0 per decade).

**Relation to 1G-D.** p = 0 is 1G-D's wall-curvature mode and p = 1 its
void-onset mode (`τ → τ(1 + ε)`). 1G-D derived them as k → 0 solutions for
super-cell regions (S1). (H3)–(H9) show the same two-mode structure for every
Lagrangian region under A1–A5 and H-A6. The super-cell/sub-cell transition
therefore enters **only** through the scale dependence of p(k) (Sec. 4).

| Scenario | f_v0 | t_LS/t0 | f_v,LS | γ_w,LS | D_W | D_V | D_V/D_W |
|---|---|---|---|---|---|---|---|
| [GM] | 0.737 | 3.3801×10⁻⁵ | 9.4711×10⁻⁵ | 1.0000474 | **0.230615** | **7.132537** | 30.93 |
| [NW15] | 0.627 | 3.0183×10⁻⁵ | 5.0735×10⁻⁵ | 1.0000254 | **0.352690** | **11.327583** | 32.12 |

### 3.3 Consequences

- **The void-onset mode is a faster mode.** It grows as `f_v ∝ t` at early
  times, against `t^{2/3}` for walls, and gains a factor 31–32 over the wall
  mode by today. Even a small void share dominates G.
- **Strict flat walls cannot carry the early field.** If every wall is at the
  global wall density (δ_w = 0, the flat walls of [GM] l. 620 read
  regionally), (H3) gives `1/(1 + δ_L) = f_w + f_v/(1 + ε) > f_w`, so

  ```text
  δ_L < f_v/f_w   for every void volume.                                              (H13)
  ```

  At last scattering the cap is `f_v,LS/f_w,LS = 9.47×10⁻⁵` ([GM]) and
  `5.07×10⁻⁵` ([NW15]). The early rms contrast exceeds it on every scale below
  **99 h⁻¹ Mpc** ([GM], 135.6 Mpc photon-comoving) and **127 h⁻¹ Mpc**
  ([NW15], 208.8 Mpc), dressed h; at 8 h̄⁻¹ Mpc it exceeds it 10.9-fold
  ([GM]). On these scales the overdense half of the early field cannot be
  represented without wall-density perturbations: 1G-D's assumption S1
  (wall curvature, beyond [GM]'s flat walls) is *necessary*, not optional.
  That the capacity radius falls at W09's homogeneity scale is recorded as a
  numerical observation, not interpreted.
- **p = 1 is excluded by the homogeneity premise**: it gives 8.05 ([GM]) and
  11.8 ([NW15]) at 8 h̄⁻¹ Mpc, and a 10% linear rms only at 409 / 445 h̄⁻¹ Mpc
  (517 / 656 Mpc photon-comoving), four times [W09]'s 100 h⁻¹ Mpc.

## 4. The missing input: the void share p(k)

### 4.1 What the acquired ingredients do and do not fix

The tracker, A1–A5, H-A6 and the early spectrum fix D_W, D_V and Δ²_u. They
do not fix how the early contrast of a region splits between its walls and
its voids. The tracker's f_v(t) is a one-parameter family (τ) whose initial
value `f_v,LS = f_v(t_LS)` is set by the late-time parameters (f_v0, H0), not
by a formation process acting on the early field. The regional laws
propagate any split, (H7), but do not choose it. The 1G-F excursion-set
population is not the tracker's (its void fraction is constant in time),
so its response cannot be transplanted without an extra identification
(Sec. 4.4). Hence

```text
p(k) = −∂f_v,LS[region]/∂δ_L(k) |_(matching epoch, tracker ensemble),
```

the linear bias of the void-seed volume fraction with respect to the early
long-wavelength density, is the single missing input. It equals 1G-D's
void-onset response through `p = f_v,LS A_v` (k → 0) and has the same status,
`VOID_ONSET_RESPONSE = EXTERNAL_CLOSURE_INPUT`.

**Monotone class (H-A7, new).** An overdense region has neither a larger void
fraction nor underdense walls: `f_v,LS ≤ p ≤ 1`. The lower end is the
uniformly compressed region (walls and voids both compressed by δ_L); p = 0
(1G-D's pure wall mode) lies just below it, by f_v,LS.

**The transition, bounded.** Only p(k) over the R8 window matters. For a
seed scale R_s much smaller than R, `G_eff/G(0) − 1` is a small, computable
number (Sec. 5.3); the transition law need not be derived on all scales.

### 4.2 Peak-background-split seed closure

Seeds are regions of the matching-epoch linear field, smoothed with a
Lagrangian top hat of radius R_s, below `−ν σ_s`, with `Φ(−ν) = f_v,LS` (the
tracker's own value, owner decision GD-OD2). A mode k shifts the
seed-smoothed field by `W(kR_s) δ`, so `δ ln f_v,LS = −[φ(ν)/(σ_s Φ(−ν))]
W(kR_s) δ` ([1G-D] Sec. 7 at k → 0). A long mode also compresses the seed
volume with its region (derived here: at first order a long mode compresses
every volume element by δ_L), so

```text
p(k) = c + [φ(ν)/σ_s] W(k R_s),    σ_s = σ_u(R_s)/(1 + z_LS),
c = f_v,LS (COMPRESSED_WITH_REGION) or 0 (THRESHOLD_SHIFT_ONLY, 1G-D's S2 as written).   (H12)
```

The compression term changes p by f_v,LS (0.07% of G); it is kept as the
primary (`COMPRESSED_WITH_REGION`), and `THRESHOLD_SHIFT_ONLY` reproduces
1G-D's owner-decision numbers: A_v = **1169 / 1185** and X_SU = **1.263 /
1.285** (gated to their printed digits).

**The seed scale is the remaining external choice of this closure.** The
GD-OD1 mapping `R_s = R_void (f_v,LS/f_v0)^{1/3}/γ_w0` turns a present void
radius (volume-average proper length) into a seed radius. Because σ_s grows
slowly at sub-Mpc scales, p depends weakly on R_s in that regime:

| Present void radius | [GM] R_s (Mpc) | p0 | σ at 8 h̄⁻¹ Mpc (c) | ε rms | [NW15] R_s | p0 | σ (c) | ε rms |
|---|---|---|---|---|---|---|---|---|
| 1G-F volume-weighted median (2.40 / 2.80 h⁻¹ Mpc photon-comoving × γ_w0) | 0.166 | 0.0707 | **0.811** | 0.77 | 0.199 | 0.0391 | **0.816** | 0.74 |
| [W09] 7.5 h⁻¹ Mpc (sensitivity) | 0.379 | 0.0889 | 0.952 | 0.97 | 0.405 | 0.0479 | 0.918 | 0.90 |
| **[W09] 15 h⁻¹ Mpc (1G-D primary)** | 0.757 | 0.1108 | **1.121** | 1.21 | 0.810 | 0.0602 | **1.057** | 1.13 |
| [W09] 30 h⁻¹ Mpc (sensitivity) | 1.515 | 0.1427 | 1.364 | 1.55 | 1.619 | 0.0781 | 1.258 | 1.46 |
| [SvdW04] factor 1.72 (1G-D alternative) | 11.94 | 0.4049 | 2.643 | 3.36 | 14.30 | 0.2494 | 2.454 | 3.47 |

(Direct A_s normalisation; multiply by 0.97058 for the Planck-anchored
values, Sec. 5.4.)

### 4.3 Linear validity (H-A8, new)

The rms void-volume response in the region is

```text
ε_rms(R) = [(1 + z_LS) f_v,LS]⁻¹ [∫ dln k Δ²_u p(k)² W²(kR)]^{1/2}.                    (H14)
```

1G-D found the void-onset response perturbative only above R*(ε = 1) = 9.9 /
8.6 h⁻¹ Mpc. At 8 h̄⁻¹ Mpc, ε_rms = 1.21 / 1.13 for the [W09]-radius seed
(`VOID_RESPONSE_NONPERTURBATIVE`) and 0.77 / 0.74 for the 1G-F-median seed
(perturbative). Applying the linear response where ε_rms > 1 is an
extension below the closure's declared validity: **H-A8** states it
explicitly. The statistic is then formal (linearly extrapolated), as σ8 is in
ΛCDM, and must not be read as the physical variance.

### 4.4 Alternative closure: the excursion-set two-barrier response (H22)

For the two-barrier walk of [SvdW04] the total void mass fraction is
`m = δ_c/(δ_c + |δ_v|)` ([SvdW04] Eq. (3)), the gambler's-ruin probability.
A region whose long-mode contrast is δ_l (same clock as the barriers) has
walks starting at δ_l (Markov property of sharp-k walks), so, exactly within
the model,

```text
m(δ_l) = (δ_c − δ_l)/(δ_c + |δ_v|),   ∂m/∂δ_l = −1/(δ_c + |δ_v|),
δ_L = b δ_l,   b = w + (1/x − 1)/[Z (δ_c + |δ_v|)],   Z = 1 − m + m/x,                   (H22)
```

in the 1G-F M3 two-density budget (voids at x ρ_ref), with w = 1 if the long
mode compresses the walls and w = 0 if the wall density is universal; x is
held fixed at first order (an approximation). With [JLH13]'s shell crossing
(δ_v = −2.7172, x = 0.2047) and δ_c = 1.68647: m = 0.38297,
void volume fraction 0.75197 (both reproduce 1G-F), and **b = 1.3546**
(w = 1) or 0.3546 (w = 0). With 1G-F's C1 wall clock, `G = b D_wall(t0)` =
1.188 / 1.281 (w = 1), i.e. an equivalent tracker share p = 0.139 / 0.085,
and σ(c) = 1.340 / 1.337. This is a different conditional model (1G-F's
f_v = 0.752, finite-density voids), compared only through its equivalent
share; it shows that a structurally independent response lands in the same
range as the PBS closure, not that either is selected.

## 5. Results (B)

### 5.1 The global-mean linear statistic at 8 h⁻¹ Mpc

Direct A_s normalisation (Planck-anchored in brackets); p0 = p(k → 0);
`regime` refers to ε_rms (H14).

| Closure | [GM] (c) R = 10.104 | [GM] (a) R = 12.570 | [GM] (b) R = 10.954 | [NW15] (c) R = 11.781 | [NW15] (a) R = 12.226 | [NW15] (b) R = 13.115 |
|---|---|---|---|---|---|---|
| unit growth σ_u (G = 1) | 1.1280 | 0.9799 | 1.0719 | 1.0442 | 1.0186 | 0.9710 |
| wall mode, p = 0 | 0.260 (0.252) | 0.226 (0.219) | 0.247 (0.240) | 0.368 (0.357) | 0.359 (0.349) | 0.342 (0.332) |
| monotone lower end, p = f_v,LS | 0.261 (0.253) | 0.227 (0.220) | 0.248 (0.241) | 0.369 (0.358) | 0.360 (0.349) | 0.343 (0.333) |
| **PBS, 1G-F-median seed** | **0.811 (0.787)** | 0.704 (0.684) | 0.770 (0.748) | **0.816 (0.792)** | 0.796 (0.773) | 0.759 (0.737) |
| **PBS, [W09]-radius seed** | **1.121 (1.088)** | 0.975 (0.946) | 1.066 (1.034) | **1.057 (1.026)** | 1.031 (1.000) | 0.983 (0.954) |
| PBS, [SvdW04]-factor seed | 2.643 (2.566) | 2.447 (2.375) | 2.576 (2.500) | 2.454 (2.382) | 2.424 (2.352) | 2.363 (2.293) |
| M3 two-barrier, w = 1 (H22) | 1.340 | — | — | 1.337 | — | — |
| strict flat walls, p = 1 | 8.045 | 6.990 | 7.645 | 11.83 | 11.54 | 11.00 |
| Planck ΛCDM linear σ8 (anchor) | | 0.8111 | | | 0.8111 | |

The two terms of (H9) are driven by the same early mode and add in
amplitude, not in quadrature: their coherence is 1 for a constant share and
≥ 0.99998 for the small PBS seeds (0.90–0.94 for the [SvdW04] seed, whose
window is inside the R8 range). For the [W09]-radius seed at (c) the wall term is
0.231 ([GM]) and the void term 0.890: the void-onset share carries 79% of
the amplitude.

### 5.2 Closure-independent interval (H15)

If p is scale independent between R8 and R_hom, `σ(R) = G(p) σ_u(R)`. The
monotone class gives the lower end (p = f_v,LS). The background's own
homogeneity premise, read as "the global linear rms does not exceed η in the
top hat of radius R_hom", gives `G ≤ η/σ_u(R_hom)`, hence

```text
G(f_v,LS) σ_u(R8) ≤ σ_lin(R8) ≤ η σ_u(R8)/σ_u(R_hom).                                  (H15)
```

The premise is an assumption of the background construction, not a derived
bound: [W09] ll. 327–335 ("100 h⁻¹ Mpc or somewhat larger"; cells whose
density has "a standard deviation of order several percent") and ll. 455–458
("a scale above which the variance in density contrasts is bounded at the
10% level"). [GM] l. 602 places the averaging domain "well above the scale
of statistical homogeneity". Its reading is an explicit input:

| Reading (same convention as R8) | [GM] (c) interval | p upper | [W09] seed inside? | [NW15] (c) interval | p upper | [W09] seed inside? |
|---|---|---|---|---|---|---|
| **rms ≤ 0.10 at 100** | **[0.261, 0.998]** | 0.095 | no (0.112 at R_hom) | **[0.369, 1.162]** | 0.069 | yes (0.091) |
| rms ≤ 0.10 at 150 | [0.261, 1.704] | 0.185 | yes | [0.369, 2.048] | 0.147 | yes |
| rms ≤ 0.06 at 100 ("several percent") | [0.261, 0.599] | 0.044 | no | [0.369, 0.697] | 0.029 | no |
| 100 as a cell side (sphere radius 62) | [0.261, 0.570] | 0.040 | no | [0.369, 0.641] | 0.024 | no |

At equal mass (a) the first reading gives [0.227, 1.148] ([GM]) and
[0.360, 1.191] ([NW15]); Planck-anchored, [0.220, 1.114] and [0.349, 1.155].
The 1G-F-median seed lies inside the first two readings for both scenarios;
the [W09]-radius seed violates the first reading mildly for [GM] (0.1125
against 0.10 at 100 h̄⁻¹ Mpc). The interval is the strongest
closure-independent statement of this phase; its width is the residual
dependence on p.

### 5.3 Radius range and scale dependence

Propagator scale dependence across the R8 window, `G_eff/G(0) − 1`:
−0.09% to −0.12% (1G-D [W09]-radius seed), −0.005% (1G-F-median seed) and
−17% to −24% ([SvdW04] seed, whose radius is inside the R8 range). Small
seeds therefore make the statistic a scale-independent multiple of σ_u to
better than 0.2%; Figure `propagator_scale_dependence.png` shows G(k)/G(0).
Radius scan at convention (c) (direct normalisation):

| L (h̄⁻¹ Mpc) | 6 | 7 | 8 | 9 | 10 | 12 |
|---|---|---|---|---|---|---|
| [GM] monotone lower | 0.310 | 0.283 | 0.261 | 0.242 | 0.226 | 0.199 |
| [GM] PBS [W09] seed | 1.332 | 1.217 | 1.121 | 1.041 | 0.972 | 0.858 |
| [NW15] monotone lower | 0.444 | 0.403 | 0.369 | 0.341 | 0.316 | 0.277 |
| [NW15] PBS [W09] seed | 1.270 | 1.153 | 1.057 | 0.976 | 0.906 | 0.793 |

**Error budget, kept separate.** Numerical: quadrature self-convergence
≤ 10⁻⁶ and a refined grid (k from 10⁻⁷ to 10³ Mpc⁻¹, 16001 points) agrees to
< 2×10⁻⁶; the growth factors carry ≤ 10⁻¹² identity errors. Parameters: the
two scenarios differ by f_v0 and H0 and are never averaged. Closure: the
dominant uncertainty, quantified by p (Secs. 4.2, 5.2). Statistical: none
(no data). The ranges above are hypothesis scans, not confidence intervals.

### 5.4 Amplitude and normalisation

- **Inputs.** A_s = 2.100×10⁻⁹, n_s = 0.9649, k_p = 0.05 Mpc⁻¹ and
  f_b = ω_b/ω_m = 0.02237/0.14310 (Planck 2018, TT,TE,EE+lowE+lensing);
  the EH98 zero-baryon transfer at the per-photon density
  `ω_m,eff = ½(1 − f_v0)(2 + f_v0)(H_D0/100)²` = 0.12048 ([GM]) and 0.13094
  ([NW15]) ([1G-A] Sec. 6.2); T_cmb = 2.7255 K; matter-era Poisson
  normalisation `Δ² = (4/25) A_s (k/k_p)^{n_s−1} (k/aH)⁴ T²`; matching at
  z_LS = 1090. No late-time ΛCDM growth enters the spectrum.
- **A_s is an import, not a Timescape fit.** [NW15] state that they treat
  A_s "as a nuisance parameter that we cannot constrain", with τ degenerate
  (l. 1422–1428). The Planck A_s is a ΛCDM fit; this is recorded as
  `PROVISIONAL_MODEL_IMPORT`.
- **Anchoring.** The pipeline's "Planck-anchored" values multiply the direct
  values by `0.8111/σ_EH98,Planck = 0.8111/0.83569 = 0.97058`: the ratio of the
  Boltzmann-code σ8 to the EH98 value at the Planck parameters (BAO wiggles
  and the 0.06 eV neutrinos missing from EH98). The late-time ΛCDM growth
  cancels exactly; the calibration uses a known ΛCDM σ8 only to correct the
  transfer function, never the predicted quantity. Both values are given.
- **Amplitude scaling (H16).** At fixed transfer and fixed closure,
  `σ² ∝ A_s` (tested to 10⁻¹⁰ for a constant share). The PBS closure is not
  fixed under a change of A_s: with f_v,LS fixed by the tracker,
  `p ∝ 1/σ_s ∝ A_s^{−1/2}`, so the void term is independent of A_s (tested to
  10⁻¹⁰ without the compression term) and only the wall term scales. Across
  A_s × {½, 2}: `d ln σ/d ln A_s` = 0.10–0.13 ([GM]) and 0.16–0.19 ([NW15]),
  not ½. This is a property of a background whose void fraction is fixed
  independently of the early amplitude; it is not imposed on any nonlinear
  model.

### 5.5 Like-for-like comparison with ΛCDM

Planck's σ8 is, by construction, the global-mean linear statistic of
Sec. 2.2 for a flat ΛCDM background, at the Planck mass M8 (convention (a)),
with the same window, early import and linear order. The Timescape values
at (a), Planck-anchored, are 0.946 / 1.000 ([W09]-radius seed),
0.684 / 0.773 (1G-F-median seed) and the interval [0.220, 1.114] /
[0.349, 1.155]; ΛCDM gives 0.8111. These compare like with like as *model*
quantities. They are not observational: an observational σ8 or S8 is
compressed in a ΛCDM fiducial, and no Timescape reduction exists (1E-A). No
tension or consistency is claimed. The wall-internal (0.834/0.935), hybrid
two-phase (≈0.99) and ΛCDM numbers are different statistics and are not
compared.

## 6. Two-phase covariance: conservation and cross terms

### 6.1 Complete decomposition

With disjoint, complementary indicators `χ_w + χ_v = 1`, phase means ρ̄_w,
ρ̄_v = x ρ̄_w and fluctuations normalised **conditionally** on the phase,
`E[χ_w δ_w] = E[χ_v δ_v] = 0` (an unconditional zero mean is not enough when
δ_w is correlated with the partition),

```text
ρ/⟨ρ⟩ = a_w χ_w (1 + δ_w) + a_v χ_v (1 + δ_v),   a_w = 1/(f_w + f_v x),  a_v = x a_w,
δ = α (χ_w − f_w) + a_w χ_w δ_w + a_v χ_v δ_v,   α = a_w (1 − x) = −δ_v^E/f_w,              (H17)
```

with `f_w a_w + f_v a_v = 1` (mass normalisation) and `δ_v^E = a_v − 1` the
void contrast relative to the global mean. For ball averages
`A = (χ_w)_R − f_w`, `B = (χ_w δ_w)_R`, `C = (χ_v δ_v)_R`,

```text
σ²_R = w^T M w,   w = (α, a_w, a_v),   M = E[(A, B, C)^T (A, B, C)],                   (H18)
```

which keeps all three cross terms. M must be positive semidefinite and
`E[A²] ≤ f_v f_w`; the runtime refuses moments that are not
(`two_phase_global_variance`). Tested on a synthetic two-phase field with
correlated partition and fields and x > 0: (H18) equals the sample variance
to 10⁻¹⁰, with cross terms well above round-off.

### 6.2 1G-E as the independent special case

With `δ_v = 0`, E3 (`E[AB] = 0`) and 1G-E's normalisation
`σ²_part = E[A²]/f_w²`, `σ²_int = E[B²]/f_w²`:

```text
σ² = δ_v^{E2} σ²_part + (f_w − f_v δ_v^E)² σ²_int,                                     (H19)
```

1G-E's mass-conserving formula (owner decision GE-OD1), tested for several
x. From the committed 1G-E inventory: σ_part = 0.3264 / 0.3036 and
σ_int = 0.9316 / 0.9403 reproduce 0.9871 / 0.9881. For finite-density voids
(x = 0.2047, the shell-crossing value) the weights are α = 1.92,
a_w = 2.42, a_v = 0.49 ([GM]); the partition and both field terms must all
be recomputed with them, not only δ_v.

**Cross terms are not zero in general.** At linear order the long mode drives
both the partition and the wall density (Sec. 3): the response parts of A
and B are perfectly correlated, which is why the two terms of (H9) add in
amplitude. E3 is therefore an assumption about the joint law, and sharing
P(k) does not establish it. For any joint law,

```text
|σ_A − σ_B| ≤ σ_R ≤ σ_A + σ_B                                                          (H20)
```

(Cauchy–Schwarz on the two terms of 1G-E): [0.605, 1.258] ([GM]) and
[0.637, 1.244] ([NW15]) around the E3 values 0.987 / 0.988. The end points
need perfect (anti)correlation and need not be physically attainable.

### 6.3 A constructive non-uniqueness

Two realisable two-phase laws are built with exactly the same acquired
constraints: f_v0; the same partition covariance (voids are `{g < c}`,
`Φ(c) = f_v0`, for a unit Gaussian field g, calibrated so the partition rms
in the ball equals the 1G-E/F reference value); the same wall-field
covariance (the 1G-E/F wall-internal linear field: growth D_wall(t0),
photon-frame compression s = D_wall, Planck-anchored); and the same
conditional mass normalisation. **Law I:** g independent of the wall field.
**Law II:** g is the wall field itself, smoothed with a Gaussian of width ℓ
(voids where the same linear field is low; the "same primordial field"
double-counting case). All moments follow from orthant integrals of the
bivariate normal (H21), coded in `bivariate_normal_orthant_moments` and
verified against the bivariate CDF (10⁻⁹) and direct 4-variate Monte Carlo:

| Convention (b) | ℓ (Mpc) | Law I σ_part / wall / cross / **total** | Law II σ_part / wall / cross / **total** |
|---|---|---|---|
| [GM], R = 10.954 Mpc | 0.292 | 0.326 / 0.915 / 0 / **0.971** | 0.326 / 0.106 / +0.036 / **0.393** |
| [NW15], R = 13.115 Mpc | 0.599 | 0.304 / 0.930 / 0 / **0.978** | 0.304 / 0.160 / +0.050 / **0.409** |

In law II the walls sit where the field is high: after the phase-conditional
mean is removed, the long-wavelength response of the wall term nearly
cancels against the partition shift, and the ball variance falls by a factor
2.5. Both laws are admissible surrogates, not solutions of the gravitational
dynamics. The result proves that a size distribution (or a partition
covariance), a volume fraction and a wall spectrum do **not** fix the
nonlinear variance at 8 h⁻¹ Mpc: the joint law of geometry and density is a
further, independent input. This is a kinematic counterexample showing
that the statistical inputs are insufficient; it is not a no-go result for
the Einstein or Timescape equations.

## 7. Closure assessment

| Result | Status | Why |
|---|---|---|
| **A — definition** | **closed** | Sec. 2: field, frame, foliation, mean, time, epoch, window, scale (explicit convention, (c) recommended), h, linear order and ensemble are fixed; FLRW limit verified |
| **B — conditional calculation** | **closed given one external closure** | Sec. 3 derives the propagator exactly; Sec. 4 identifies p(k); with an explicit closure the chain is implemented, converged and tested; the closure-independent interval (H15) bounds the result |
| **C — Timescape prediction** | **not reached** | p(k) is not derived from the theory |
| **C — observational interpretation** | **not reached** | firewall: dressed light-cone, tracer, selection and inference |

**The missing object, precisely.** The response kernel
`p(k) = −∂f_v,LS/∂δ_L(k)`: the linear bias of the void-seed volume fraction
with respect to the early long-wavelength density, at the matching epoch, in
the tracker ensemble. Equivalently 1G-D's A_v(k) = p(k)/f_v,LS.

**Why the current inputs do not determine it.** The tracker fixes f_v,LS from
late-time parameters, not from the early field; A1–A5 and H-A6 propagate any
split; the 1G-F population is inconsistent with the tracker's f_v(t); and
the PBS closure needs a seed model and an external seed scale.

**What would determine it.**
- *Derivation:* a void-formation model whose ensemble-mean void fraction
  reproduces the tracker's f_v(t) from the early spectrum (for example an
  excursion set with a barrier calibrated to f_v(t), or an ensemble of the
  project's LTB–CMC regions). Its peak-background split then gives p(k)
  without a free seed scale. 1G-G lists the evolution inputs such a model
  needs.
- *Measurement:* any statistic that fixes G on a scale where the void
  response is linear. By (H9)–(H10), the global linear rms at ~100 h⁻¹ Mpc
  measures G directly (p = (G − D_W)/(D_V − D_W)); so would the
  cross-correlation of the void-fraction field with the large-scale density
  (the void bias). Both need the observational reduction that the firewall
  excludes, so they are routes for later phases, not inputs used here.
- *Impact:* `∂σ(c)/∂p = (D_V − D_W) σ_u(R8)` = 7.79 ([GM]) and 11.46
  ([NW15]); Δp = 0.01 moves σ(c) by 0.078 / 0.115.

## 8. Adversarial self-check (not an independent audit)

- **Means.** The contrast is relative to the global volume mean; regions are
  sampled by mass; at first order both give zero mean, and the connected
  variance is used. Mixing the wall mean (1G-C) with the global mean would
  drop the dilution factor f_w(t)/f_w,LS of (H7): checked, the wall term is
  0.23 (dilute) not 0.88.
- **Frames.** The field lives on the dust slice in common time; the photon
  frame only labels Lagrangian coordinates at early times; convention (c)
  uses h̄ and γ_w0, both global; no dressed map enters.
- **Growth.** Walls grow as EdS in t (A5), voids as Milne; the CGI comoving
  growth (which fails the separate-universe test, 1G-D) is not used.
- **Mass and volume.** The void share is volume only (empty voids); the wall
  share conserves mass; the split sums to the region's early contrast
  (p + (1 − p) = 1), so no mode is counted twice in the linear statistic.
  In the nonlinear covariance the double counting is explicit (law II).
- **Circular normalisation.** The anchor corrects the transfer function at
  Planck parameters only; the interval uses [W09]'s homogeneity statement,
  not σ8. Neither calibrates to the quantity reported.
- **Undeclared dependences found and declared:** z_LS = 1090 and the neglect
  of radiation at last scattering (it rescales δ_L(LS) and σ_s alike, so ε is
  unchanged and the wall term moves by about 0.4%); f_v,LS inherits the
  tracker fit (f_v0, H0); the single seed scale and Gaussian threshold; the
  γ_w0 ambiguity in converting the 1G-F radius (a 37% change of R_s changes
  p by roughly 10%); H-A6 ignores wall–void boundary coupling; S1 goes beyond
  [GM]'s flat walls (but is required, Sec. 3.3); H-A8 at R8.
- **Numbers that could be wrong.** The GT law-II collapse of the wall term was
  checked analytically by a linear-response estimate and numerically by
  direct 4-variate Monte Carlo of the covariance kernels.

## 9. Decisions requested from the owner

Each is separate; none is applied by this report (the owner has since
decided the push part of H-OD5).

1. **H-OD1, definition and radius convention.**
   - [ ] Adopt the definition of Sec. 2 as the project's σ8-analogue, with
     convention **(c)** (`8 h̄⁻¹ Mpc`, `R·H_D0 = 800 km/s`) as primary and (a)
     as the comparison convention at fixed mass. *(Recommended.)*
   - [ ] As above, with (a) primary.
   - [ ] Keep the definition as a research proposal only.
2. **H-OD2, the void-share closure for a reference value.**
   - [ ] **β:** PBS seed with the 1G-F volume-weighted median radius:
     0.811 / 0.816 at (c) (0.787 / 0.792 anchored); perturbative at R8;
     inside the [W09] premise for both scenarios. *(Recommended, always
     reported with the interval.)* It uses the project's own early-spectrum
     population rather than an external radius; its weak points are 1G-F's
     conditional status and the single-scale idealisation.
   - [ ] **α:** PBS seed with the [W09] 15 h⁻¹ Mpc radius (the 1G-D primary):
     1.121 / 1.057 at (c); non-perturbative at R8 (ε_rms 1.21 / 1.13); mildly
     outside the 10%-at-100 premise for [GM].
   - [ ] **γ:** no reference value; report only the interval (H15) with the
     10%-at-100 reading: [0.261, 0.998] / [0.369, 1.162] at (c).
3. **H-OD3, status tokens** (proposals; the registry rules matter).
   - [ ] Add two tokens through the existing addition mechanism (no validator
     change): `GLOBAL_MEAN_LINEAR_STATISTIC_DEFINITION =
     DERIVED_FROM_VERIFIED_DEFINITIONS` and
     `GLOBAL_MEAN_LINEAR_STATISTIC_COMPUTATION =
     DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` (A1–A5, H-A6, H-A7, H-A8 and
     the closure of H-OD2); keep `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC =
     NOT_DERIVED`, since no closure is selected by the theory.
     *(Recommended.)*
   - [ ] Change `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` to
     `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`. The 1F-C-R validator accepts
     only one registered change per added token, and this token already has
     one (the 2026-10-02 D successor). A second, chained change needs an
     approved validator extension; R2-N4 (record order is not enforced)
     becomes relevant then.
4. **H-OD4, the runtime.**
   - [ ] Keep `global_variance.py` experimental until an independent audit.
     *(Recommended.)*
   - [ ] Promote it to a package runtime.
5. **H-OD5, publication.** Push, pull request, merge, audit, freeze or tag of
   this phase: none is authorised by the task; each needs a separate
   decision.
   - *Push decided* (owner, 2026-10-06): the commits are on the session
     branch `ccr-555e67be-u11yht`. Pull request, merge, audit, freeze and
     tag remain open.

## 10. Implementation and usage

- **Runtime:** `timescape_fsigma8.global_variance` (experimental; imported
  by no other package module; public names free of `sigma8`, `sigma_8`,
  `8hMpc`). Every scientific choice is a mandatory keyword-only argument;
  inapplicable choices are passed as `NOT_APPLICABLE`.
  - `two_phase_global_growth` — D_W, D_V (H8) with independent checks;
  - `ConstantVoidShare`, `GaussianThresholdSeedVoidShare`,
    `tracker_consistent_seed_radius`, `evaluate_void_share` — closures (H12);
  - `global_linear_propagator` (H9), `conditional_global_linear_sigma` (H10);
  - `HomogeneityPremise`, `admissible_global_linear_interval` (H15);
  - `empty_void_region_contrast`, `two_phase_region_contrast`,
    `linear_two_phase_contrast_coefficients`, `strict_flat_wall_contrast_cap`
    (H2)–(H5), (H13);
  - `TwoPhaseSmoothedMoments`, `two_phase_global_variance`,
    `cauchy_schwarz_total_rms_interval`, `bivariate_normal_orthant_moments`
    (H17)–(H21);
  - `two_barrier_void_mass_fraction`, `two_barrier_global_linear_bias` (H22).
- **One case:**

  ```bash
  PYTHONPATH=src OPENBLAS_NUM_THREADS=1 python -B -W error \
      scripts/phase1g_h_global_variance_case.py --config scripts/phase1g_h_configs/gm_bare_pbs_f_median_seed.json
  ```

  Each configuration states every input; a missing entry is refused. The
  three examples cover the PBS seed with the [W09] radius, with the 1G-F
  median radius, and an explicit constant share at equal mass.
- **All evidence:**

  ```bash
  PYTHONPATH=src OPENBLAS_NUM_THREADS=1 python -B -W error scripts/phase1g_h_global_variance_closure_numerics.py
  ```

  It takes about 100 s, writes the JSON artifact and three figures
  (`sigma_vs_void_share.png`, `radius_scan.png`,
  `propagator_scale_dependence.png`), and exits nonzero if one of its 21
  declared gates fails.

## 11. Verification summary

Details, commands, versions and logs are in the validation record.

- **Phase tests:** `tests/test_phase1g_h_global_variance.py`, 28 tests,
  covering the categories asked for. They check dimensions and k/R units
  (photon-comoving Mpc), window and mass normalisation, and the homogeneous,
  single-phase and EdS limits. They check real-space against Fourier (2×10⁻⁵)
  and A_s scaling. They check positive-semidefiniteness and cross-term
  bounds, and recover 1G-D, 1G-E and 1G-F numbers. They check perturbative
  convergence of the exact spherical region, quadrature and k-tail
  convergence, and the refusal of incomplete or out-of-class configurations.
- **Evidence gates:** 21 declared gates, all passing (1G-D reproduction, A_s
  scaling, refined quadrature, 1G-E reproduction, orthant CDF, two-barrier
  finite differences).
- **Governance:** the tolerance audit reports 0 comparisons without explicit
  tolerances; the 1F-C-R validator reports `PASS`.
- **Full suites** (warnings as errors) on CPython 3.13.16 and 3.11.17 (Linux):
  see the validation record. The Windows 3.14.3 / 3.11.9 gate was not run in
  this session; its commands are listed there.

## 12. Preservation, status and limitations

- **Unchanged:** every frozen report, inventory, audit, evidence file and
  tag; every existing package module, test and status token. The only files
  touched outside the new ones are README.md and CLAUDE.md (current-status
  text).
- **F/G freeze.** The F/G freeze attests its own checkpoint. It does not
  derive σ8; 1G-H builds on it without editing it. R2-N4 is relevant only if
  H-OD3's second option is chosen.
- **No D v2.** No `phase-1g-d-separate-universe-growth-v2` tag or branch is
  created; the approved D successor is part of the F/G checkpoint.
- **Limitations:** H-A6 (no wall–void boundary coupling); a single-scale
  Gaussian-threshold seed; the 1G-F radius conversion ambiguity; matching at
  z = 1090 without radiation; the EH98 no-wiggle transfer; A_s from a ΛCDM
  fit; empty voids in the propagator (finite-density voids are treated only
  in the covariance and the M3 alternative); no time-dependent mergers or
  mass transfer (1G-G); and nothing observational.

## 13. Sources, versions and equation numbering

| Source | Version and file | SHA-256 | Used |
|---|---|---|---|
| [GM] | arXiv:2511.17160v2, `main.tex` | `f9cadfa0…77c59` (as 1G-A) | (5.1)–(5.7), text p. 25 (γ_w, 1+z, ⟨ρ⟩ normalisation), Sec. 3 (averaging), l. 602, l. 620 |
| [W09] | arXiv:0909.0749v2, `observe.tex` | `2b0324d1…4b531` (as 1G-A) | l. 277 (void size), ll. 327–335, 455–458 (homogeneity), (Q1), ll. 1807–1811 (f_vi) |
| [W07] | arXiv:0709.0732v2, `solution.tex` | `221662c9…7c6cd8` | regional EdS/Milne laws (via 1G-C) |
| [NW15] | arXiv:1410.3470v2, `cmb1.tex` | `5688c9ac…4b74673` | A_s a nuisance parameter (ll. 1422–1428); f_v0 = 0.627, H0 ≈ 61 |
| [JLH13] | arXiv:1304.6087v2, `voids_mnras.tex` | `cf6fc77a…dce17f` | Eq. (2) (linear variance); (A8)–(A12) via 1G-F |
| [SvdW04] | astro-ph/0311260v1, `voids.tex` | e-print `4b7ad599…16f8841` | Eqs. (1)–(3), Eq. (3) the void mass fraction |
| [EH98] | astro-ph/9709112v1, `trans.tex` | `5f2ac6b4…739dce17f` | (26), (28)–(31) through `lagrangian_sigma` |

Equation numbers are those of the e-print LaTeX sources (sequential display
numbering, as reconstructed in 1G-A for [GM]); the journal HTML may differ.
Downloads stayed in the session scratchpad; no upstream code was copied.
(H1)–(H24) are this report's: (H1)–(H5), (H13), (H17)–(H20) and (H23)
follow from the definitions with [GM] Sec. 3 and (5.4)–(5.6). (H6)–(H9) add
A1–A5 and H-A6. (H12) is 1G-D's Sec. 7 response with the compression term
and window added here. (H22) applies [SvdW04] Eq. (3) to conditional walks.
None of them is attributed to a source as already derived.
