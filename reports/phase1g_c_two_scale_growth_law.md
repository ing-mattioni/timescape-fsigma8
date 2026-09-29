# Phase 1G-C — Two-scale linear growth law for Timescape σ(M)

Audit classification: `REPORT_ONLY_THEORY_AUDIT_WITH_NUMERICAL_EVIDENCE`.
Base: Phase 1G-A commit `462121c`, branch `phase-1g-c-two-scale-growth-law`.
Date: 2026-09-29.
Companion: [`phase1g_c_two_scale_growth_inventory.json`](phase1g_c_two_scale_growth_inventory.json).
Evidence: `scripts/phase1g_c_two_scale_growth_numerics.py`, which writes the
git-ignored `artifacts/independent/phase1g_c_two_scale_growth.json`. It reuses
the 1G-A σ machinery unchanged.

References: [GM] arXiv:2511.17160v2 (LaTeX e-print, SHA-256 `f9cadfa0…77c59`);
[W09] arXiv:0909.0749v2 (`observe.tex`, SHA-256 `2b0324d1…4b531`);
[W07] arXiv:0709.0732v2 (as source-verified in the Astra audit);
[1G-A] `reports/phase1g_a_sigma8_derivation_path_audit.md`.

## 1. Scope and verdict

**Authorisation.** On 2026-09-29 the project owner asked to "continue with
the next steps starting with Phase 1G-C". 1G-A Sec. 10 item 3 defines 1G-C as
report-only theory: derive how linear perturbations inside wall regions
evolve, the input 1G-A identified as decisive for σ8. No package code,
equation, status token or tolerance changes here, and no observational claim
is made.

**Verdict:**

1. **The tracker is exactly two FLRW regions in the common time t**
   (`DERIVED_FROM_VERIFIED_DEFINITIONS`, verified to ≤ 3e−15):
   - empty Milne voids: `a_v ∝ t`, `ρ_v = 0`;
   - Einstein–de Sitter walls: `a_w,reg ∝ t^{2/3}`, `ρ_w = 1/(6πGt²)`;
   - all matter sits in walls. Backreaction and curvature are exactly the
     wall/void partition terms of [W09].
2. **By [W09]'s own scale hierarchy, σ8 lies inside a dust cell.** [W09]
   coarse-grains its dust at the ≈100 h⁻¹ Mpc statistical-homogeneity scale.
   So the volume-average CGI growth of [GM] (1G-A) describes *super-cell*
   modes, while mass-weighted statistics at 8 h⁻¹ Mpc sit in the wall
   component.
3. **The regional wall growth law.** Apply [GM]'s dust-frame CGI system to
   the wall regional background. There ρ_eff ≡ 0, so the Mészáros form
   (4.27) is exact and gives `Δ ∝ t^{2/3}`. The alternative "flat dust in
   wall proper time τ_w" violates its own Friedmann equation by
   `γ_w² − 1 = 0.87` today and is inadmissible (consistent with the recorded
   `REJECTED_UNSUPPORTED`).
4. **Conditional σ(M8) (mass-weighted, framework-consistent):**
   - **0.834** with the [GM] parameters and **0.935** with the [NW15] CMB fit
     (equal-mass convention);
   - 0.83–0.96 across the three radius conventions;
   - Planck ΛCDM: 0.811.

   This supersedes 1G-A's volume-average values (0.52–0.69) *for σ8-scale,
   mass-weighted statistics*. Those values remain the super-cell growth.
   Classification: `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` (A1–A4, Sec. 5).
5. **Scale-dependent growth.** If both limits hold, the linear power
   spectrum today steps up by `(X_wall/X_CGI)² = 1.95–2.53` (comoving closure)
   from super-cell to sub-cell scales, across the ≈100 h⁻¹ Mpc
   homogeneity/acoustic scale. The transition shape is **not derivable** from
   the tracker, which has no length scale. It is the principal remaining
   theoretical gap and a sharp observational discriminant.

## 2. Provenance

- **Sources:** [GM] and [W09] LaTeX e-prints (hashes above), inspected in
  the session scratchpad. Line numbers refer to those files.
- **Timescape quantities:** every one comes from frozen package functions
  (`background`: `fv`, `dfv_dt`, `a_D`, `H_D`, `rho_d`, `Q_D`, `R_D`,
  `gamma_w`).
- **σ numbers:** from the unchanged 1G-A functions (EH98 early spectrum,
  Planck anchor, radius conventions), imported by path.

## 3. Exact two-region structure of the tracker `DERIVED_FROM_VERIFIED_DEFINITIONS`

**Regional scale factors.** [GM] Eq. (5.1) defines regional scale factors
from regional volumes, `f_v = V_v/V_D`. So `a_v³ = f_v a_D³/f_vi` and
`a_w,reg³ = (1−f_v) a_D³/f_wi`.

**Tracker forms.** With [GM] (5.5)–(5.6),
`a_D ∝ t (f_v0/f_v)^{1/3}` and
`(1 − f_v)/f_v = (2+f_v0)(1−f_v0)/(3 f_v0 H_D0 t)`. Hence:

```text
a_v ∝ t              (H_v = 1/t)          — Milne,
a_w,reg ∝ t^{2/3}    (H_w = 2/(3t))       — Einstein–de Sitter, as [W09] line 1764 states,
⟨ρ⟩_D = (1−f_v)/(6πG t²) = f_w ρ_w,  ρ_w = 1/(6πG t²) = 3H_w²/(8πG),  ρ_v = 0,
H_D = f_v H_v + f_w H_w = (2+f_v)/(3t),
Q_D = 6 f_v f_w (H_v − H_w)²             ([W09] Eq. (Q1), line 513),
⟨R⟩_D = f_v · (−6 H_v²) = −6 f_v/t²      (empty Milne curvature; the D1-corrected [GM] (5.7)),
γ_w H_w = H_D                            ([GM] Eq. (5.3), uniform quasilocal flow).
```

The mean density used is [GM]'s normalisation
`⟨ρ⟩(t0) = 12H_D0²(1−f_v0)/[8πG(2+f_v0)²]` (text p. 25).

Numerical check with the package: every identity holds to ≤ 2.9e−15 for the
paper, notebook and [NW15] parameters. The table uses the notebook, CMB-fit
and paper presets.

| Identity | max rel. error |
|---|---|
| `f_v a_D³/t³` constant | 2.2e−15 |
| `(1−f_v) a_D³/t²` constant | 2.4e−15 |
| `H_D = f_v H_v + f_w H_w` | 4e−16 |
| `⟨ρ⟩ = f_w/(6πGt²)` | 2e−16 |
| `Q_D = 6 f_v f_w (H_v−H_w)²` | 1.3e−15 |
| `⟨R⟩ = −6 f_v/t²` | 5e−16 |
| `γ_w H_w = H_D` | ≤ 3e−15 |

**Consequences:**
- Timescape's backreaction, curvature and "effective fluid" are nothing but
  the partition between empty expanding voids and matter-filled EdS walls.
- All matter sits in walls. Walls are overdense relative to the mean by
  `1/(1−f_v)`: 3.80 today (f_v0 = 0.737), 2.68 ([NW15]).

These facts are implicit in [W07]/[W09]. They are recorded here as verified
identities because the growth argument rests on them.

## 4. Where σ8 sits in the Timescape scale hierarchy `VERIFIED_FROM_PRIMARY_SOURCE`

[W09] subsection "The scale of statistical homogeneity" (lines 311–458) and line 461:
- the "scale of statistical homogeneity" is "100 h⁻¹ Mpc or somewhat larger"
  and roughly coincides with the acoustic/BAO scale, "of order 110 h⁻¹ Mpc";
- "Below the scale of statistical homogeneity we will typically find density
  contrasts |δρ/ρ| ∼ 1";
- voids have "a characteristic diameter 30 h⁻¹ Mpc";
- "Given our identification of dust particles coarse-grained at the scale of
  statistical homogeneity…" (line 461).

[GM] intend their backgrounds "with an averaging domain well above the scale
of statistical homogeneity" (Sec. 5 preamble, line 602). They also note that
the solutions retain "a dependence on the scale and location of the averaging
domain used to construct the background if it is smaller than the statistical
homogeneity scale" (Conclusions, line 1083).

**Consequence** `DERIVED_FROM_VERIFIED_DEFINITIONS`: σ8's radius
(R ≈ 11–12.6 Mpc) is about 10× smaller than the dust-cell scale (≈140–160 Mpc for h = 0.73–0.61).
Within Timescape's own construction, the volume-average CGI background
describes perturbations of the cell-averaged fluid, i.e. modes with λ above
the cell scale. The mass inside cells is all wall matter (Sec. 3). So
mass-weighted fluctuations at 8 h⁻¹ Mpc are governed by the wall regional
dynamics, not by the volume-average background. 1G-A's volume-average σ(M8)
(0.52–0.69) therefore applies the super-cell law outside its domain.

## 5. The regional growth law

`DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`

**Assumptions:**
- **A1** — [W09]'s two-scale assumption: "no backreaction within walls and
  voids separately, but only in the combined average" (line 510). The
  tracker satisfies it exactly (Sec. 3).
- **A2** — Linear sub-cell perturbations of the wall matter evolve under
  [GM]'s CGI dust-frame equations (4.9)–(4.12) on the *wall regional*
  averaged background. [GM] apply the same CGI scheme to a local, sub-global
  averaging domain in their RZA example (line 602: "how deviations of a local
  cosmic average from the global evolution influence the development of
  local perturbations"), so regional backgrounds are within their framework.
- **A3** — σ(M) is a mass-weighted (Lagrangian) statistic (1G-A Sec. 6.1),
  and no mass lies in voids (Sec. 3).
- **A4** — Scale separation: the Lagrangian scale of M is below the dust-cell
  scale (Sec. 4). Individual walls (sheets, filaments) and their boundaries
  are not resolved by the two-scale model, which is a limitation.

**Derivation.** On the wall regional background there is no effective fluid:
the region is flat with no internal backreaction, so ρ_eff,w ≡ 0 and
[GM]'s Sec. 4.1 over-determination argument (line 500) does not arise.
[GM] (4.9)–(4.12) reduce to the dust equations. The regional form of (4.27)
is then **exact**, not an approximation:

```text
Δ̈_w + 2 H_w Δ̇_w − 4πG ρ_w Δ_w = 0,   H_w = 2/(3t),  4πG ρ_w = 2/(3t²)
⇒ Δ_w ∝ t^{2/3} (growing) or t^{−1} (decaying).
```

**Numerical check.** H_w = H_D − ḟ_v/(3(1−f_v)) and ρ_w = ⟨ρ⟩/(1−f_v) were
built from package functions, not from the closed forms. Integrating from an
EdS start at 1e−8 t0 gives t^{2/3} to 1.6e−13 (DOP853, rtol 1e−12). Also
`H_w t0 = 0.666666666667`.

Void-interior modes carry no mass, since ρ_v = 0.

**Growth relative to the photon-normalised early universe.** Normalise the
early field at equal photon temperature (1G-A Sec. 5.1). With the dressed
redshift `1+z = a/a0` ([GM] (5.4); [W09]'s dressed `a`) and
`a_w,reg/a ∝ γ_w (1−f_v)^{1/3}`:

```text
lim_{t_e→0} (t0/t_e)^{2/3} / (1+z_e) = γ_w0 (1 − f_v0)^{1/3} = ½(2+f_v0)(1−f_v0)^{1/3},
X_wall = γ_w0 (1 − f_v0)^{1/3} / g_Λ,          g_Λ = qplus(0) = 0.787813.
```

The closed form equals the exact finite-t_e identity
`γ_w0(1−f_v0)^{1/3}/[γ_w(t_e)(1−f_v(t_e))^{1/3}]` to ≤ 1e−15 (Phase 1G-B).
The naive limit at t_e = 1e−8 t0 differs by −f_v(t_e)/6 ≈ −4.7e−9, as
expected. (Corrected 2026-09-29: this line first claimed 1e−13 agreement with
the naive limit.)
Relative to *volume-average* EdS the wall growth is `(1−f_v0)^{1/3}`: 0.641
([GM] preset), compared with the CGI comoving 0.403 and Mészáros 0.342.

## 6. The wall-clock alternative is inadmissible

`DERIVED_FROM_VERIFIED_DEFINITIONS`

**The candidate.** Evolve wall perturbations in the wall observers' proper
time τ_w, treating the wall as a flat dust FLRW in τ_w. Its background would
need `3(H_w^τ)² = 8πG ρ_w` with `H_w^τ = γ_w H_w = H_D` ([GM] (5.3)).

**The failure.** The tracker has `8πG ρ_w = 3 H_w²`. The relative residual
is therefore `γ_w² − 1`: **0.873** today for f_v0 = 0.737 and 0.725 for
[NW15]. No admissible linear theory can be built on it. This quantifies, for
the tracker, the finding the project records as
`NAIVE_W09_WALL_CLOCK_AS_REGIONAL_PROPER_DUST_FLRW_CLOCK = REJECTED_UNSUPPORTED`.
The common-time law of Sec. 5 is thus the only admissible regional law within
[GM]'s dust-proper-time framework.

Wall observers' clocks enter σ8 only through the redshift–time map. That map
is fixed here by early photon-temperature matching and by evaluating at t0.

## 7. Conditional σ(M8)

`σ = X · E · σ8^Planck`. The E factors and radius conventions are those of
1G-A Sec. 6. The primary baryon fraction is 0.1563; its ±7–8% sensitivity
carries over from 1G-A.

| Parameters | Growth law | X | (a) equal mass | (b) dressed 8/h | (c) bare 8/h̄ |
|---|---|---|---|---|---|
| [GM] f_v0 = 0.737 | **wall regional** | 1.1129 | **0.834** | 0.912 | 0.960 |
| [GM] f_v0 = 0.737 | volume-average CGI, comoving (super-cell) | 0.6995 | 0.524 | 0.573 | 0.603 |
| [NW15] f_v0 = 0.627 | **wall regional** | 1.2002 | **0.935** | 0.891 | 0.958 |
| [NW15] f_v0 = 0.627 | volume-average CGI, comoving (super-cell) | 0.8586 | 0.669 | 0.637 | 0.686 |
| Planck ΛCDM | — | 1 | 0.811 | | |

**Reading.** Within the [GM] framework plus [W09]'s two-scale structure and
scale hierarchy, and under A1–A4, the mass-weighted linear σ(M8) of a
Timescape universe with Planck's early universe is about **3–15% above**
Planck-ΛCDM at equal mass. Across all three conventions the range is
+3% to +18%.

The reason is that matter lives in walls, which are EdS in t with no
Λ-like suppression. That enhancement is only partly offset by the walls
expanding less than the photon redshift implies (factor 0.877 or 0.946).

This is a conditional, model-internal number. It is **not** an observational
σ8: low-redshift σ8/S8 values are compressed in a ΛCDM fiducial, and no
Timescape reduction exists (1E-A). No consistency or tension claim is made.

## 8. Scale-dependent growth: a step across the homogeneity scale

`DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` for the two limits;
`NOT_DERIVED` for the transition.

If super-cell modes grow with the volume-average CGI law and sub-cell mass
fluctuations with the wall law, then relative to the shared early spectrum
the linear power today changes by `(X_wall/X_CGI)²` from large to small
scales:

| f_v0 | X_wall | X_CGI comoving | power step, comoving | power step, Mészáros |
|---|---|---|---|---|
| 0.50 | 1.259 | 1.000 | 1.59 | 1.85 |
| 0.60 | 1.216 | 0.892 | 1.86 | 2.30 |
| **0.627** [NW15] | 1.200 | 0.859 | **1.95** | 2.46 |
| 0.695 | 1.151 | 0.765 | 2.27 | 3.02 |
| **0.737** [GM] | 1.113 | 0.699 | **2.53** | 3.52 |
| 0.80 | 1.039 | 0.588 | 3.13 | 4.70 |

**The transition.** The tracker is self-similar and has no length scale, so
the transition's location and shape cannot be derived from it. [W09] places
the relevant scale at the statistical-homogeneity/acoustic scale
(≈100–110 h⁻¹ Mpc). A step of this size in the linear matter power near the
BAO scale would be a sharp, testable signature.

Testing it requires the dressed redshift-space map (blocked, 1D-C §22) and a
bias model; no comparison with survey P(k) shapes is made here. It is equally
possible that a derived transition law is gradual, or that the super-cell CGI
closure itself needs revision. Either way, this is now the principal open
theoretical question for Timescape structure growth.

## 9. What changes relative to 1G-A

- **The open problem is settled within the framework.** 1G-A Sec. 8 called
  the two-scale growth law the decisive open problem. Within [GM] + [W09]
  and A1–A4 it is now settled for mass-weighted σ(M8): the wall-regional law
  applies (Secs. 4–6). 1G-A's volume-average numbers are reinterpreted as
  super-cell growth.
- **Remaining open:**
  1. the super-cell/sub-cell transition law (Sec. 8). It needs a model with a
     length scale; the LTB–CMC section family and a 1F-D-type regional
     construction are natural candidates;
  2. the validity of A2 for the geometrically thin, disconnected wall
     network, including wall–void boundary couplings and the evolving wall
     fraction;
  3. the radius convention, i.e. the dressed spatial map (7–15%, 1G-A);
  4. every observational reduction (1E-A, 1D-C §§20–23).

## 10. Recommendations (none applied; each requires human approval)

1. **Phase 1G-B scope.** The runtime should expose both growth laws as an
   explicit, non-default choice: volume-average CGI (comoving/Mészáros) and
   wall-regional EdS in common time. It must document the scale domain of
   each. The lead has already sent this scope addition to the 1G-B
   implementer.
2. **New status tokens** (proposal):
   - `TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"`
     (Sec. 5);
   - `SUPER_CELL_TO_SUB_CELL_GROWTH_TRANSITION = "NOT_DERIVED"` (Sec. 8).
3. **Phase 1G-D (theory):** a growth-transition model with an explicit
   length scale.
   - One candidate: an ensemble of LTB–CMC or regional cells matched at the
     homogeneity scale, which reproduces both limits.
   - Required output: the transition shape between the two limits, and hence
     the scale dependence of P(k) around 100 h⁻¹ Mpc.
4. **Author questions** (add to 1D-C §33 and 1G-A Sec. 10):
   - do [GM] intend their CGI perturbations to apply below the statistical
     homogeneity scale;
   - do they accept the regional wall law for sub-cell mass statistics?

## 11. Reproduction and validation

```text
.venv\Scripts\python -B -W error scripts\phase1g_c_two_scale_growth_numerics.py
→ wrote artifacts\independent\phase1g_c_two_scale_growth.json
```

Asserted budgets:
- decomposition identities ≤ 1e−13 (achieved ≤ 2.9e−15);
- regional growth vs t^{2/3} ≤ 1e−8 (achieved 1.6e−13);
- all 1G-A budgets, inherited.

Environments and suite results are recorded in the integration commit.

## 12. Preservation statement

- **Added:** this report, its inventory, and one script.
- **Unchanged:** every package module, test, status token, tolerance,
  frozen report and upstream file.
- **Not committed:** the artifact is git-ignored.
- **Remote:** nothing is pushed or tagged.
