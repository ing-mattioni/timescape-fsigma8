# Phase 1G-D — Separate-universe structure of two-scale Timescape growth and the transition length scale

Audit classification: `REPORT_ONLY_THEORY_AUDIT_WITH_NUMERICAL_EVIDENCE`.
Base: `214a626` (`main` = `origin/main`), branch `phase-1g-d-growth-transition`.
Date: 2026-09-29.
Companion: [`phase1g_d_separate_universe_inventory.json`](phase1g_d_separate_universe_inventory.json).
Evidence: `scripts/phase1g_d_separate_universe_numerics.py`, which writes the
git-ignored `artifacts/independent/phase1g_d_separate_universe.json`.

References:
- [GM] arXiv:2511.17160v2 (e-print SHA-256 `f9cadfa0…77c59`);
- [W09] arXiv:0909.0749v2 (`observe.tex`, SHA-256 `2b0324d1…4b531`);
- [SvdW04] Sheth & van de Weygaert, MNRAS 350, 517, astro-ph/0311260;
- peak-background split: Kaiser 1984 (ApJ 284, L9) and Bardeen, Bond,
  Kaiser & Szalay 1986 (ApJ 304, 15);
- [1G-A], [1G-C]: the earlier phase reports.

## 1. Scope and verdict

**Authorisation.** On 2026-09-29 the project owner asked to "continue with
next theory step, Phase 1G-D". [1G-C] Sec. 10 item 3 defines 1G-D: a
growth-transition model with an explicit length scale. This phase is
report-only, with numerical evidence. No package code, equation, status token
or tolerance changes, and no observational claim is made.

**Verdict:**

1. **The tracker has exactly one time scale** `DERIVED_FROM_VERIFIED_DEFINITIONS`.
   `f_v(t) = t/(t+τ)` with `τ = (2+f_v0)(1−f_v0)/(3 f_v0 H_D0)`, verified to
   4e−16. τ is Phase 1F-D's `b`. Walls (EdS in t) and voids (empty Milne) are
   universal, so a super-cell region differs from the mean only through its
   own τ and through wall-curvature perturbations.
2. **Separate-universe (SU) modes** `DERIVED_FROM_VERIFIED_DEFINITIONS`,
   verified to machine precision. The long-wavelength (k → 0) perturbations
   of the two-scale model are:
   - a wall-curvature mode, with cell contrast `f_w δ_w` and `δ_w ∝ t^{2/3}`;
   - a void-onset mode, `ε f_v(t)` with `ε = δτ/τ`.

   Each is an exact k → 0 solution of [GM]'s general system (4.9)–(4.11). The
   effective-fluid perturbations `(Δ_eff, P̃_eff)` are fixed by the tracker
   family: a **separate-universe closure**.
3. **[GM]'s closures fail the separate-universe consistency test**
   `DERIVED + NUMERICALLY_CORROBORATED`. The comoving closure has
   `Δ_eff/Δ_d = +0.18…+0.20` and `P̃_eff = 0`. Both SU modes have
   `Δ_eff/Δ_d < 0` at all times and `P̃_eff ≠ 0`, with
   `P̃_eff/Δ_eff ≠ c²_s,eff`. Mészáros (`Δ_eff = 0`) and barotropic
   (`P̃ = c²_s Δ_eff`) fail too.

   The void response the comoving growth implies rises by a factor 63–80
   over the history, whereas an SU response is constant. **The
   volume-average CGI growth of [1G-A] is therefore not Timescape's
   long-wavelength growth.** [1G-C] Sec. 8's reading of those numbers as the
   super-cell law, and its P(k) step, are superseded.
4. **Super-cell growth law** `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`:
   `D_SU(t) = f_w(t) D_wall(t) + A_v a_LS f_v(t)` for the primordial mode.
   `A_v = dε/dδ_L(LSS)` is the void-onset response, an external closure.
   - A_v = 0 gives the lower bound `X_SU ≥ 0.293` ([GM] parameters) or 0.448
     ([NW15]).
   - The peak-background-split estimate `A_v ≈ 2.9–4.7×10³` gives
     `X_SU ≈ 2.75–3.95`: large-scale linear growth about 3–4× that of ΛCDM in
     amplitude, for the same early universe (conditional; Sec. 8).
5. **The explicit transition length scale.** The void onset responds
   non-perturbatively below `R*(ε = 1) ≈ 28–45 h⁻¹ Mpc`, and its density
   contrast drops below 10% only above **128–215 h⁻¹ Mpc** (peak-background
   split). That reproduces [W09]'s "100 h⁻¹ Mpc or somewhat larger"
   homogeneity scale. [W09]'s own "single density perturbation" seeding
   relation instead gives 1000–4750 h⁻¹ Mpc, which is internally inconsistent
   with that claim.
6. **σ8 lies in the non-perturbative regime.** At R8 the void response is
   `A_v σ_LSS(R8) ≈ 2.6–4.3 ≫ 1`. A linear, global-mean σ8 does not exist in
   the two-scale linear theory. The only linear σ statistic defined at 8 h⁻¹
   Mpc is the wall-internal `σ_wall(M8)` of [1G-C] (0.83–0.96). A σ8
   comparable with observations requires a nonlinear two-phase (wall/void)
   statistic, which is the recommended Phase 1G-E.

## 2. Provenance

- **Timescape backgrounds** come from frozen package functions (`fv`, `rho_d`,
  `rho_eff`, `p_eff`, `Theta`, `cs2_eff`, `redshift`), and the comoving
  regular growing mode from `perturbations.growing_mode`.
- **The SU perturbation formulas** are analytic (Sec. 4). For the void-onset
  mode they are cross-checked against the package evaluated at a neighbouring
  tracker τ(1+10⁻⁷).
- **The early spectrum** is the unchanged 1G-A EH98 import. A σ quadrature in
  x = kR was added for large radii; it agrees with 1G-A's to 9e−9 at
  R = 12.57 Mpc.
- **Environments:** Python 3.14.3 and 3.11.9 give identical numbers.

## 3. One time scale `DERIVED_FROM_VERIFIED_DEFINITIONS`

From [GM] (5.6), `f_v = 3f_v0H_D0 t/(3f_v0H_D0 t + (2+f_v0)(1−f_v0)) = t/(t+τ)`.
Numerically, `max|f_v − t/(t+τ)|/f_v ≤ 4.4e−16`.

| Parameters | τ/t0 |
|---|---|
| [GM] f_v0 = 0.737 | 0.3569 |
| [NW15] f_v0 = 0.627 | 0.5949 |

Together with [1G-C] Sec. 3 (walls EdS in t and voids empty Milne, both
universal), the tracker is a one-parameter family in τ at fixed bang time.
The void-onset time τ is the parameter `b` of Phase 1F-D's necessary-bound
diagnostic.

## 4. Separate-universe modes `DERIVED_FROM_VERIFIED_DEFINITIONS`

**Assumption S1 (separate universe).** A region much larger than the
wall/void structure evolves as its own two-scale tracker. It has the
universal walls and voids, and differs from the mean only through its own τ
and its wall curvature. It is a Lagrangian region of fixed dust mass,
evolving in the common time t. Linearising gives two physical long-wavelength
modes.

**Wall-curvature mode.** `δ_w = C t^{2/3}` (or `C t^{−1}`) is the EdS growing
(or decaying) mode of the wall matter, and the void volume is untouched.
Then:
- `δV_w/V_w = −δ_w`, `δf_v = f_v f_w δ_w`;
- the cell contrast is `δ_d = f_w δ_w`: empty voids dilute the wall contrast;
- `δH_w = −δ̇_w/3` and `δR_w = 10 H_w² δ_w` (linearised Friedmann equation
  of a closed dust patch).

**Void-onset mode.** `τ → τ(1+ε)` with walls unperturbed. Then
`δf_v = −f_v f_w ε` and `δ_d = f_v ε`.

For both, `Q = 6 f_v f_w (H_v − H_w)²` ([W09] Q1),
`⟨R⟩ = f_v R_v + f_w R_w`, `ρ_eff = −(Q+⟨R⟩)/(16πG)` and
`p_eff = −Q/(16πG) + ⟨R⟩/(48πG)` ([GM] (3.12)–(3.13)). In the k → 0
correspondence `Δ ↔ δρ/ρ`, `P̃_eff ↔ δp_eff/ρ_eff` and `Z ↔ −δ̇_d`.

**Verification:**
- With analytic time derivatives, both modes satisfy [GM]'s perturbed
  Raychaudhuri equation (4.11) with a relative residual ≤ 2e−15 at
  t/t0 = 10⁻³…1, for both parameter sets. [GM] (4.9) holds by construction,
  and (4.10) follows from the background effective conservation law of each
  cell.
- The void-onset mode's `δ⟨ρ⟩`, `δρ_eff` and `δp_eff` agree with the package
  evaluated at τ(1+10⁻⁷) to ≤ 5e−7. That is the O(ε) nonlinearity plus
  rounding.

So the SU modes are exact long-wavelength solutions of [GM]'s framework, and
they define the **separate-universe closure**: long-wavelength effective-fluid
perturbations determined by the tracker family.

## 5. Consistency test of [GM]'s closures `DERIVED + NUMERICALLY_CORROBORATED`

For the [GM] preset (f_v0 = 0.737); [NW15] is qualitatively identical.

| t/t0 | SU wall `Δ_eff/Δ_d` | SU wall `P̃/Δ_eff` | SU void-onset `Δ_eff/Δ_d` | SU void-onset `P̃/Δ_eff` | [GM] comoving `Δ_eff/Δ_d` (P̃ = 0) | barotropic `P̃/Δ_eff = c²_s` |
|---|---|---|---|---|---|---|
| 0.001 | −297.3 | −0.332 | −357.0 | −0.499 | +0.2000 | −0.5000 |
| 0.01 | −29.63 | −0.321 | −35.81 | −0.490 | +0.2000 | −0.4997 |
| 0.1 | −2.841 | −0.225 | −3.664 | −0.422 | +0.1995 | −0.4854 |
| 0.3 | −0.830 | −0.064 | −1.254 | −0.346 | +0.1961 | −0.4482 |
| 1 | −0.104 | +0.933 | −0.387 | −0.267 | +0.1833 | −0.3912 |

**Reading:**
- In an overdense cell (fewer voids, or a denser wall), curvature and
  backreaction are smaller, so the effective-fluid density perturbation has
  the **opposite sign** to the dust perturbation: `ρ_eff = f_v(8+f_v)/(24πGt²)`
  increases with f_v.
- The comoving closure's regular growing mode has the same sign as the dust
  (+1/5 early), and it forbids the non-zero `P̃_eff` that both SU modes carry.
- Mészáros sets `Δ_eff = 0`, which is also inconsistent.
- Barotropic imposes `P̃/Δ_eff = c²_s`. That agrees only asymptotically early,
  and only for the void-onset mode (−0.499 vs −0.500), which behaves like a
  time shift of f_v.

**Implied void response.** If [GM]'s comoving growth were an SU combination,
it would equal `f_w D_wall + β f_v` with constant β. Instead,
`r(t) = (D_CGI − f_w D_wall)/f_v` rises from 0.006 (t/t0 = 10⁻³) to 0.435
(t0), a factor 72.6. For Mészáros the rise is 0.005 → 0.322 (×62.9), and for
[NW15] ×80 and ×72. No constant response reproduces it.

**Consequences:**
- The volume-average CGI growth ([1G-A] X∞ = 0.70/0.86) does not describe
  Timescape's long-wavelength response.
- [1G-C] Sec. 8 read those numbers as the super-cell law and predicted a P(k)
  step up toward small scales. That reading is **superseded** by Secs. 6–8
  below.
- The [1G-A]/[1G-C] σ numbers themselves are unchanged as computed
  quantities. Only their interpretation changes.

## 6. Super-cell growth law `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`

**Assumption S2 (void-onset response).** The primordial long-wavelength mode
of a super-cell region, with linear contrast δ_L at last scattering, sets
`ε = A_v δ_L` as well as the wall-curvature growing mode. In photon-normalised
growth units ([1G-A] Sec. 5.1), with `a_LS = 1/1091`:

```text
D_SU(t) = f_w(t) D_wall(t) + A_v a_LS f_v(t),   D_wall(t0) = γ_w0 (1−f_v0)^{1/3}.
```

| Parameters | A_v = 0 (lower bound) | PBS, f_vi = 10⁻² | PBS, f_vi = 10⁻⁴ |
|---|---|---|---|
| [GM] f_v0 = 0.737 | D_SU = 0.231, **X_SU = 0.293** | A_v a_LS = 2.63, X_SU = 2.75 | 3.91, X_SU = 3.95 |
| [NW15] f_v0 = 0.627 | D_SU = 0.353, **X_SU = 0.448** | 2.92, X_SU = 2.77 | 4.33, X_SU = 3.89 |

These values hold only for R > R* (Sec. 8), where ε < 1.

**The dilution.** With no void response, the cell-averaged contrast grows
only as f_w D_wall. Voids carry no mass, yet their fast expansion dilutes the
cell mean. The large-scale growth is therefore *dominated by the void-onset
mode* whenever the response is of peak-background-split size. A realistic
response gives large-scale growth about 3–4× ΛCDM's in amplitude (8–16× in
power), for the same early universe.

This is a sharp conditional consequence. It is not compared with survey data
here: that needs the dressed map and a bias model (1D-C §§20–23), and the
closure A_v is external.

## 7. The void-onset response A_v `EXTERNAL_CLOSURE_INPUT` (two estimates)

1. **[W09]'s single-perturbation seeding** (Eq. `initc`, line 1811):
   `δ_H = f_vi (δρ/ρ)_vi`, with |δ_H| ∈ {10⁻⁶, 10⁻⁵} (line 1814).
   Attributing a cell's whole early contrast to its void fraction gives
   `A_v = 1/|δ_H| = 10⁵–10⁶`.
2. **Peak-background split (Gaussian threshold).** Void seeds are the
   fraction `f_vi = Φ(−ν)` of the early field below `−ν σ_s` at the seed
   scale. A long-wavelength mode shifts the threshold, so
   `d ln f_vi/dδ_L = −φ(ν)/(σ_s Φ(−ν))` and
   `A_v = φ(ν)/(σ_s Φ(−ν))`, since τ ∝ 1/f_vi.
   - **Seed scale:** [W09]'s 30 h⁻¹ Mpc void diameter (line 277) divided by
     the [SvdW04] shell-crossing radius factor 1.72, giving
     R_seed = 11.9 Mpc ([GM]) or 14.3 Mpc ([NW15]).
   - **Seed variance:** σ_s = σ_LSS(R_seed) = 9.3e−4 or 8.4e−4 (EH98,
     matter-era normalisation).
   - **Result:** for f_vi ∈ {10⁻⁴, 10⁻²} (line 1815), ν = 3.72 or 2.33 and
     A_v = 4260 / 2869 ([GM]) or 4724 / 3181 ([NW15]).

**Caveat.** The matter-era normalisation at last scattering ignores
radiation, which raises the true δ there by about 25%. It enters σ_s and δ_L
alike, so it largely cancels in the peak-background-split A_v and in R*.

## 8. The transition length scale R* `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`

R* is defined by `A_v σ_LSS(R*) = criterion`. The table below uses the [GM]
parameters; each cell gives R* in h⁻¹ Mpc (dressed h), with Mpc in brackets.

| A_v closure | ε = 1 (non-perturbative onset) | 10% void-fraction fluctuation (`f_w0 ε = 0.1`) | 10% density contrast (`f_v0 ε = 0.1`, [W09] criterion) |
|---|---|---|---|
| PBS f_vi = 10⁻² | 30 (41) | 75 (103) | **165 (226)** |
| PBS f_vi = 10⁻⁴ | 45 (62) | 104 (142) | **215 (294)** |
| [W09] single, \|δ_H\| = 10⁻⁵ | 438 (600) | 767 (1051) | 1365 (1870) |
| [W09] single, \|δ_H\| = 10⁻⁶ | 1615 (2212) | 2735 (3745) | 4755 (6511) |

[NW15]: PBS gives 28–41 / 88–118 / **128–167** h⁻¹ Mpc. The single-perturbation
relation gives 354–1298 / 752–2651 / 1004–3501 h⁻¹ Mpc.

**Reading.** With the peak-background-split response, the two-scale model
*predicts* its own statistical-homogeneity scale: 10% density variance at
≈130–215 h⁻¹ Mpc, in line with [W09]'s "100 h⁻¹ Mpc or somewhat larger"
(line 327). Below `R*(ε = 1) ≈ 30–45 h⁻¹ Mpc`, the void fraction is set
non-perturbatively: regions are void-dominated or wall-dominated. [W09]'s own
single-perturbation seeding would push homogeneity to ≳1 h⁻¹ Gpc and is not
compatible with [W09]'s homogeneity claim.

This is the explicit length scale 1G-D was asked for. It is set by the void
seed statistics, not by the tracker, which is self-similar.

## 9. Where σ8 sits, and what a Timescape σ8 must be

At R8 (Lagrangian 12.6 Mpc), σ_LSS = 9.0e−4 ([GM]) or 9.2e−4 ([NW15]). So
`A_v σ_LSS(R8) = 2.6–4.3` (PBS) and 90–900 ([W09] single). Both are ≫ 1.

**Conclusions** `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`:

1. **No linear global-mean σ8.** At 8 h⁻¹ Mpc the wall/void partition itself
   is non-perturbative (regimes: `R < R*(ε=1)` inside the partition,
   `R* < R < R_hom` a transitional regime, `R > R_hom` the linear SU regime).
   A *linear, global-mean* σ8 is not defined within the linear two-scale
   theory.
2. **σ_wall is the only defined linear statistic.** It is the
   wall-internal linear field relative to the wall mean: [1G-C]'s σ_wall(M8)
   = 0.834 ([GM]) or 0.935 ([NW15]) at equal mass, 0.83–0.96 across
   conventions. It remains a correct *conditional linear* number, but it is
   not by itself the observable mass variance.
3. **An observable σ8 needs a nonlinear two-phase statistic.** The mass
   variance in 8 h⁻¹ Mpc spheres consists of the partition variance (voids
   empty, walls at `1/f_w` times the mean) plus σ_wall. The partition
   variance depends on the void size distribution relative to R8
   (`R_void ≈ 15 h⁻¹ Mpc` vs R8 = 8 h⁻¹ Mpc). For `R ≪ R_void` it tends to
   `f_v/f_w` (≈ 2.8, i.e. σ ≈ 1.67 for f_v0 = 0.737). For `R ≳ R_void` it is
   smaller. This is the recommended Phase 1G-E.
4. **Status of earlier numbers.** The volume-average numbers of [1G-A]
   (0.52–0.69) are neither the long-wavelength growth (Sec. 5) nor the σ8
   statistic. They remain what they are: [GM]'s CGI comoving-closure growth.

## 10. Consequences for the runtime and the records

- **1G-B runtime.**
  - `GrowthLaw.VOLUME_AVERAGE_CGI` implements [GM]'s closure faithfully, but
    the closure fails SU consistency for the Timescape tracker (Sec. 5).
  - `WALL_REGIONAL_EDS_COMMON_TIME` computes the wall-internal linear
    statistic (Sec. 9).
  - A documented limitation should say both. No code change is made here.
- **Superseded readings:** [1G-C] Sec. 8 (super-cell = CGI; P(k) step) and
  [1G-C] Sec. 9's "open problem settled" statement for σ8. The latter holds
  only for the wall-internal linear statistic.
- **Unchanged:** [1G-A] Sec. 4 (barotropic ill-posedness), [1G-A] Sec. 6 (ω_m,eff
  identity; mass labels), [1G-C] Sec. 3 (two-region structure) and
  [1G-C] Sec. 5 (wall law).

## 11. Recommendations (none applied; each requires human approval)

1. **Status tokens** (proposal):
   - `GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY = "FAILED_FOR_TIMESCAPE_TRACKER"` (Sec. 5);
   - `TWO_SCALE_SUPER_CELL_GROWTH_LAW = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"` (Sec. 6);
   - `VOID_ONSET_RESPONSE = "EXTERNAL_CLOSURE_INPUT"` (Sec. 7);
   - `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC = "NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY"` (Sec. 9).
2. **1G-B runtime:** add the Sec. 10 limitation to the result caveats and the
   validation report, with no numerical change.
3. **Phase 1G-E:** a nonlinear two-phase σ(R). Model the void population with
   a Boolean or excursion-set size distribution at volume fraction f_v0 and
   characteristic radius about 15 h⁻¹ Mpc ([W09], [SvdW04]). Add σ_wall, and
   produce the mass variance in 8 h⁻¹ Mpc spheres. That is the first
   Timescape quantity directly comparable to a *nonlinear* σ8.
4. **Finite-k separate-universe closure.** Extend the Sec. 4 closure to
   finite k through [GM] (4.12) and the `k²Ṽ` term. This gives a
   physically consistent replacement for the comoving closure at super-cell
   scales.
5. **Author questions:**
   - is [GM]'s comoving closure intended to reproduce the separate-universe
     response of the underlying two-scale model;
   - how do the Timescape authors relate f_vi to the local primordial density
     (Sec. 7)?

## 12. Reproduction and preservation

```text
.venv\Scripts\python -B -W error scripts\phase1g_d_separate_universe_numerics.py
→ wrote artifacts\independent\phase1g_d_separate_universe.json     (~5 s)
```

Asserted budgets:
- one-scale identity ≤ 1e−13 (achieved 4.4e−16);
- (4.11) residual ≤ 1e−12 (achieved ≤ 2e−15);
- void-onset mode vs package ≤ 1e−5 (achieved ≤ 5.1e−7);
- large-R σ quadrature ≤ 1e−8;
- the 1G-A budgets, inherited.

Results are identical on Python 3.14.3 and 3.11.9.

- **Added:** this report, its inventory, and one script.
- **Unchanged:** every package module, test, status token, tolerance and
  frozen report.
- **Remote:** nothing is pushed or tagged.
