# Phase 1G-F — A self-consistent void population for the two-phase Timescape model

Audit classification: `REPORT_ONLY_THEORY_AUDIT_WITH_NUMERICAL_EVIDENCE`.
Base: `b96c290` (the Phase 1G adversarial audits), session branch
`claude/zealous-rubin-1m3vf4`. Date: 2026-09-29.
Companion: [`phase1g_f_void_population_inventory.json`](phase1g_f_void_population_inventory.json).
Evidence: `scripts/phase1g_f_void_population_numerics.py`, which writes the
git-ignored `artifacts/independent/phase1g_f_void_population.json`.

References (arXiv LaTeX e-prints, SHA-256 of the `.tex` in the inventory):
- [SvdW04] Sheth & van de Weygaert, MNRAS 350, 517 (astro-ph/0311260), `voids.tex`;
- [JLH13] Jennings, Li & Hu, MNRAS 434, 2167 (arXiv:1304.6087), `voids_mnras.tex`;
- [W09] arXiv:0909.0749v2 (`observe.tex`); [GM] arXiv:2511.17160v2 (`main.tex`);
- [1G-A], [1G-C], [1G-D], [1G-E]: the earlier phase reports; their
  adversarial audits and the consolidation
  [`phase1g_adversarial_audit_errata_successor.md`](phase1g_adversarial_audit_errata_successor.md).

The printed equation numbers of [SvdW04] and [JLH13] were reconstructed from
their sources: a sequential counter over numbered display rows, with
appendix letters.

## 1. Scope and verdict

**Authorisation.** The project owner's task statement of 2026-09-29 asks,
as its Item C, for Phase 1G-F: [1G-E] Sec. 6 item 1, report-only theory plus
numerics. The owner approvals given in that statement are, verbatim:
1. "Add the status token TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION" (reports/phase1g_e_two_phase_sigma.md §6 item 3; assumptions E1–E4)."
2. "Commit to this session's working branch, push that branch, and open ONE draft pull request against main at the end."

This phase adds no package code, changes no status token, equation or
tolerance, and makes no observational claim. Tokens are proposed only
(Sec. 13).

**Question.** [1G-E] placed all of the tracker's void volume f_v0 in balls
of one radius, 15 h⁻¹ Mpc. Replace that with a void size distribution derived
from the same early spectrum and void physics. Does it reproduce the
tracker's f_v0 (0.737 [GM], 0.627 [NW15]) with near-empty voids?

**Verdict** (conditional, model-internal; `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`
under F1–F6 of Sec. 4):

1. **Thresholds.** The EdS tophat void reaches shell crossing at
   `δ_v = −2.7172`, with interior density 0.2047 and radius factor 1.6967.
   These are [JLH13]'s corrected values. [SvdW04]'s printed −2.81 / 0.1982 /
   1.7151 come from Θ_sc = 3.53, which does not satisfy [SvdW04]'s own
   condition (A29). "Near-empty" interiors (ρ_v/ρ_w = 0.1, 0.05) need
   `δ_v = −5.19, −8.97`.
   `DERIVED_FROM_VERIFIED_DEFINITIONS`.
2. **The tracker's voids are the late state of excursion-set voids.** The
   tophat void interior is an open FLRW region; its expansion rate tends to
   3/2 of the background's. That is exactly the tracker's
   `H_v/H_w = (1/t)/(2/(3t))`: empty Milne voids in EdS walls ([1G-C]
   Sec. 3). `DERIVED_FROM_VERIFIED_DEFINITIONS`.
3. **The void mass fraction is clock-independent; the volume fraction
   depends on the mapping.**
   - The two-barrier walks put a fraction `1 − 𝒟` of the mass in voids of
     all sizes: 0.28–0.38 at shell crossing and 0.11–0.25 near-empty
     ([SvdW04] Eq. (3)). This holds for any growth clock and any spectrum.
   - **JLH13 volume conservation** (validated against N-body in ΛCDM)
     gives f_v = 1 − 𝒟 ≤ 0.38. It **cannot** reproduce f_v0 for any clock.
   - **SvdW04 number conservation** overfills the volume (1.4–3.2), as
     [SvdW04] itself notes.
   - The tracker's own **two-scale volume budget** (walls keep the EdS
     density of their mass; voids add volume, [1G-C] Sec. 3) gives
     f_v = 0.66–0.79 for every barrier. Both f_v0 values fall in or at the
     edge of that range.
4. **Void sizes depend on the clock, and are small for every
   tracker-consistent clock.**
   - With the wall EdS clock C1, the volume-weighted median void radius is
     2.4 ([GM]) and 2.8 ([NW15]) h⁻¹ Mpc at shell crossing. It is ≤ 1 h⁻¹
     Mpc for near-empty voids.
   - Under the two-scale budget, f_v0 is reproduced by counting voids
     larger than **0.5 h⁻¹ Mpc ([GM]) or 2.0 h⁻¹ Mpc ([NW15])**. Voids
     ≥ 10 h⁻¹ Mpc fill only 3.6–4.6%, against [W09]'s 40–50% for its
     30 h⁻¹ Mpc-diameter voids.
   - The volume-average CGI clock C2 gives smaller voids still.
   - The separate-universe clock C3 with the audit's tracker-consistent
     seed (GD-F1/F2) is barely larger than C1.
   - Only 1G-D's original peak-background-split response gives
     [W09]-sized voids: at shell crossing, median 12–22 h⁻¹ Mpc and 62–73%
     of the volume in voids ≥ 10 h⁻¹ Mpc. That response is the input the
     1G-D audit disputes.
5. **Near-empty voids fill f_v0 only as sub-Mpc voids.** With C1, voids at
   ρ_v ≤ 0.1 ρ_w reproduce f_v0 only when voids down to 0.06–0.8 h⁻¹ Mpc
   are counted.
6. **History.** No fixed comoving minimum radius reproduces the tracker's
   `f_v(t) = t/(t+τ)`. Counting voids ≥ 1 h⁻¹ Mpc (C1, shell crossing)
   gives 0.013 at z = 3, against the tracker's 0.31. Counting all sizes
   gives a constant 0.75.
7. **σ at 8 h⁻¹ Mpc.** Take the self-consistent C1 population, normalised
   to f_v0, with empty voids (E1) and the frame-consistent compression:
   - **σ = 0.99** for both parameter sets (0.84–0.99 across barriers);
   - σ_part is 0.33 ([GM]) and 0.30 ([NW15]), against 1.13 and 0.91 for
     [1G-E]'s single 15 h⁻¹ Mpc radius.

   With the original 1G-D PBS clock, σ = 1.42–1.88 at shell crossing,
   comparable to or above [1G-E]'s 1.36–1.57. With non-empty shell-crossing
   interiors and the mass-conserving formula (GE-F1), the C1 value falls to
   0.62–0.72.

**Reading.** The excursion set, with the tracker's own volume budget, does
account for a present void fraction of 0.63–0.74. It does so with a
population dominated by voids of a few h⁻¹ Mpc and minivoids, not by a
single population of 30 h⁻¹ Mpc voids. The [1G-E] primary number
(σ ≈ 1.4–1.6) therefore rests on a void size that no tracker-consistent
clock produces; the self-consistent value is σ ≈ 1.0. Whether real
Timescape voids are larger requires the void-onset response (1G-D, an
external closure that its audit narrows) or physics beyond the linear clock
plus a spherical threshold.

**Status.** These are conditional, nonlinear, model-internal numbers. They
are **not** an observational σ8, and `SIGMA8_AUTHORIZATION` stays
`NOT_GRANTED`.

## 2. Provenance

- **Early spectrum.** The unchanged [1G-A] import: the EH98 no-wiggle
  transfer, per-photon ω_m,eff, Planck A_s, n_s and f_b, with the [1G-A]
  Planck anchor 0.970577 (as [1G-E]).
- **Timescape quantities.** Frozen package functions (`fv`, `gamma_w`)
  and the [1G-A]/[1G-D] script functions, imported by path. That covers
  g_TS, the tracker f_v at last scattering, and the PBS machinery.
- **Void theory.** Re-derived here from [SvdW04] App. A and C and [JLH13]
  App. A; nothing is taken from memory.
- **The Boolean and variance machinery** is [1G-E]'s own functions,
  imported by path. The polydisperse form is new; its one-radius limit
  equals [1G-E] exactly (Sec. 10).
- **Environments:** CPython 3.13.12 (NumPy 2.5.3, SciPy 1.18.1) and 3.11.15
  (NumPy 2.4.6, SciPy 1.17.1), Linux x86-64. See Sec. 15 for identity.

## 3. Frames and conventions `DERIVED_FROM_VERIFIED_DEFINITIONS`

- **Radius convention.** Radii are photon-normalised comoving Mpc, and
  "h⁻¹ Mpc" uses the dressed h: [1G-A] convention (b), as [1G-E]. The ball
  is R = 8/h Mpc (10.954 [GM], 13.115 [NW15]).
- **Wall frame factor.** The wall matter expands as `a_w,reg ∝ t^{2/3}`
  ([1G-C] Sec. 3). Normalised to the photon frame early, it is compressed
  today relative to that frame by
  `a_w,reg/a_photon = γ_w0 (1−f_v0)^{1/3} = D_wall`: 0.8768 [GM], 0.9455
  [NW15]. This follows from `a_w,reg/a ∝ γ_w (1−f_v)^{1/3}` ([1G-C] Sec. 5).
  - A void of Lagrangian radius R_L and interior density x ρ_w therefore
    has Eulerian radius `r = D_wall x^{−1/3} R_L`.
  - The wall field's Eulerian compression in this frame is `s = D_wall`.
    [1G-E]'s `s = f_w^{1/3}` is the compression in the a_D frame (lead
    observation L1 of the consolidation). Both are reported.
- **Barrier densities** refer to the EdS background of the spherical model,
  which is the wall density ρ_w (the tracker's walls are EdS in t).

## 4. Model and closures

- **F1 — excursion set.** The early field is Gaussian, with the [1G-A]
  spectrum. The walks are Markovian (sharp-k), with σ(R) from the
  real-space top-hat. This is the standard approximation of [SvdW04] and
  [JLH13].
- **F2 — barriers.** EdS spherical-model thresholds (Sec. 5):
  - void: `δ_v(x)` for an interior density ratio x (shell crossing, 0.1,
    0.05);
  - collapse: `δ_c ∈ {1.0624 (turnaround), 1.6865 (collapse)}`, the
    [SvdW04]/[JLH13] range for the void-in-cloud barrier.

  The same thresholds are used with every clock. [JLH13] report that ΛCDM
  moves δ_v by 0.5% (−2.731).
- **F3 — growth clock (explicit closure).** It maps the early field to void
  formation today: `σ(R_L, t0) = D(t0) σ_1(R_L)`, with D normalised so that
  `D/a_photon → 1` early.
  - **C1** wall EdS in common t ([1G-C] Sec. 5): `D = γ_w0 (1−f_v0)^{1/3}`.
    This is the only clock under which the EdS thresholds are exact.
  - **C2** volume-average CGI ([1G-A] Sec. 5): `D = γ_w0 g_TS`, comoving
    and Mészáros.
  - **C3** separate-universe void onset ([1G-D] Sec. 6):
    `D = f_w0 D_wall + A_v a_LS f_v0`. Four variants: A_v = 0; [1G-D]'s PBS
    A_v for f_vi = 10⁻² and 10⁻⁴; and the 1G-D audit's tracker-consistent
    seed (GD-F1/F2: f_vi = the tracker's f_v at z = 1090, seed radius
    `R_void (f_vi/f_v0)^{1/3}/γ_w0`). C3 is used here below its stated
    validity scale R*, which is recorded as a limitation.
- **F4 — Lagrangian → Eulerian volume.** Let M be the void mass fraction
  (above a minimum radius) and x the interior density ratio.
  - **M1** ([SvdW04] Eq. (7); [JLH13] Eq. (12)): number conserving,
    `f_v = M/x`, which can exceed 1 ([JLH13] Eq. (14)).
  - **M2** ([JLH13] Eqs. (15)–(17)): volume conserving, `f_v = M`.
  - **M3** (two-scale volume budget, this phase): the walls hold mass
    1 − M at the tracker's EdS density ρ_w; the voids hold M at x ρ_w. In
    units of the EdS volume of the mass,
    `f_v = (M/x) / (1 − M + M/x)`.
    - This never exceeds 1.
    - It predicts the domain's extra expansion,
      `(a_D/a_w,reg)³ = 1 − M + M/x`.
    - It contains the tracker as the limit x → 0, M → 0 at fixed
      `M/x = (1−M) f_v/f_w`.
- **F5 — Boolean geometry.** Voids are Poisson-placed balls with the derived
  size distribution: [1G-E]'s E2, generalised.
- **F6 — variance.** [1G-E]'s E1, E3 and E4, with two changes, each
  reported beside the [1G-E] convention:
  - the mass-conserving wall weight (GE-F1);
  - the photon-frame compression (Sec. 3).

## 5. Spherical model `DERIVED_FROM_VERIFIED_DEFINITIONS`

The EdS tophat underdensity has `1+Δ = (9/2)(sinh η − η)²/(cosh η − 1)³`
and linear contrast `δ = −(3/20)[6(sinh η − η)]^{2/3}` ([JLH13] (A9), (A11);
[SvdW04] (A26), (A27)). Shell crossing at the edge requires
`sinh η (sinh η − η)/(cosh η − 1)² = 8/9` ([JLH13] (A8); [SvdW04] (A29)).
Roots are solved with brentq at xtol 1e−15.

| Quantity | this phase | [JLH13] (A8)–(A12) | [SvdW04] (A29)–(A31) |
|---|---|---|---|
| η_sc | 3.487522 | 3.488 | 3.53 |
| 1 + Δ_sc | 0.204722 | 0.2047 | 0.1982 |
| r_NL/r_L | 1.696726 | 1.697 | 1.7151 |
| δ_v | −2.717180 | −2.717 | −2.81 |
| H_shell/H_u at shell crossing | 4/3 | — | 4/3 ((A33)) |

- **Gate.** Every [JLH13] value is reproduced to its printed digit
  (asserted).
- **[SvdW04]'s root.** Θ_sc = 3.53 leaves a residual of +0.00268 in (A29),
  which explains its −2.81; [JLH13] (below (A12)) call their value "a
  correction".
- **Other thresholds.** `δ_c = (3/5)(3π/2)^{2/3} = 1.686470`,
  `δ_ta = (3/5)(3π/4)^{2/3} = 1.062410` ([SvdW04] (A21)–(A22)).
- **[1G-D]'s factor.** [1G-D] uses 1.72 for r_NL/r_L; the effect is
  immaterial there (1G-D audit: +0.9% in A_v).

**Near-empty barriers.** The homogeneous interior evolves as an open FLRW
region after the edge has shell-crossed, so the relation still holds:

| ρ_v/ρ_w | η | δ_v | r_NL/r_L |
|---|---|---|---|
| 0.2047 (shell crossing) | 3.4875 | −2.7172 | 1.6967 |
| 0.1 | 4.3377 | −5.1901 | 2.1544 |
| 0.05 | 5.1012 | −8.9651 | 2.7144 |

**Milne limit.** `H_interior/H_u = g(η)/(2/3)` ([SvdW04] (A15)) is 1.4371
at η = 5 and 1.4989 at η = 10, and tends to 3/2 (asserted to 1e−12 at
η = 40). The tophat void interior thus tends to the tracker's empty Milne
void. The excursion-set voids and the tracker's voids are the same objects
at different stages.

## 6. Two-barrier first crossing `VERIFIED_FROM_PRIMARY_SOURCE` + `DERIVED` + `NUMERICALLY_CORROBORATED`

**The primary-source form.** [SvdW04] Eq. (1), in [JLH13]'s notation
Eq. (6):

```text
f_lnσ(σ) = 2 Σ_{j≥1} exp(−(jπx)²/2) jπ x² sin(jπ𝒟),   x = 𝒟σ/|δ_v|,   𝒟 = |δ_v|/(δ_c+|δ_v|).
```

([JLH13] note `f_lnσ = 2 S𝓕` of [SvdW04].)

**An independent image form.** Derived here from [SvdW04] (C7). With
`w = δ_c + |δ_v|` and `s = √(2t)`, the Laplace transform
`sinh(δ_c s)/sinh(w s)` expands as
`Σ_{n≥0} [e^{−(|δ_v|+2nw)s} − e^{−(|δ_v|+2δ_c+2nw)s}]`. Each term is the
transform (C2) of a single-barrier density (C1), so

```text
f_lnσ(σ) = Σ_{n≥0} [g(|δ_v| + 2nw) − g(|δ_v| + 2δ_c + 2nw)],   g(B) = √(2/π) (B/σ) e^{−B²/2σ²}.
```

The image series converges fast for σ ≤ w and the Fourier series for
σ > w; production uses each on its side, with 60 terms. The checks:

| barrier / δ_c | 𝒟 | void mass fraction 1 − 𝒟 | \|∫f dlnσ − (1−𝒟)\| | max \|images − Fourier\| (σ/w ∈ [0.2, 5], 400 terms) |
|---|---|---|---|---|
| shell crossing / 1.686 | 0.6170 | **0.3830** | 6e−17 | 3.5e−16 |
| shell crossing / 1.062 | 0.7189 | **0.2811** | 0 | 5.3e−16 |
| 0.1 / 1.686 | 0.7548 | 0.2452 | 8e−17 | 3.7e−16 |
| 0.1 / 1.062 | 0.8301 | 0.1699 | 6e−17 | 3.6e−16 |
| 0.05 / 1.686 | 0.8417 | 0.1583 | 0 | 4.9e−16 |
| 0.05 / 1.062 | 0.8941 | 0.1059 | 3e−17 | 2.8e−16 |

The normalisation equals [SvdW04] Eq. (3)/(C8) (gate 1e−11), and the two
series agree (gate 1e−13).

## 7. Growth clocks

Here `D(t0)` is in photon-normalised units and `X = D/g_Λ` (g_Λ = 0.787813).

| Clock | [GM] D (X) | [NW15] D (X) |
|---|---|---|
| C1 wall EdS in t | 0.8768 (1.113) | 0.9455 (1.200) |
| C2 CGI comoving | 0.5510 (0.699) | 0.6764 (0.859) |
| C2 CGI Mészáros | 0.4676 (0.594) | 0.6023 (0.765) |
| C3 A_v = 0 | 0.2306 (0.293) | 0.3527 (0.448) |
| C3 PBS, f_vi = 10⁻² (A_v 2869 / 3180) | 2.1684 (2.752) | 2.1805 (2.768) |
| C3 PBS, f_vi = 10⁻⁴ (A_v 4260 / 4724) | 3.1086 (3.946) | 3.0675 (3.894) |
| C3 PBS, tracker-consistent seed (A_v 1169 / 1185) | 1.0202 (1.295) | 1.0335 (1.312) |

The tracker-seed row uses f_vi = 9.47e−5 ([GM]) and 5.07e−5 ([NW15]), with
seed radii 0.757 and 0.810 Mpc. It reproduces the 1G-D auditor's values
(A_v 1172/1235 at f_vi = 10⁻⁴) to ≤ 4%, the difference being the exact
tracker f_vi.

## 8. Void fractions today

### 8.1 All sizes (r → 0): clock-independent

| Barrier | δ_c | M = 1 − 𝒟 (= M2 f_v) | M1 f_v (SvdW) | **M3 f_v (two-scale)** |
|---|---|---|---|---|
| shell crossing | 1.686 | 0.383 | 1.87 (> 1) | **0.752** |
| shell crossing | 1.062 | 0.281 | 1.37 (> 1) | **0.656** |
| ρ_v = 0.1 ρ_w | 1.686 | 0.245 | 2.45 (> 1) | **0.765** |
| ρ_v = 0.1 ρ_w | 1.062 | 0.170 | 1.70 (> 1) | **0.672** |
| ρ_v = 0.05 ρ_w | 1.686 | 0.158 | 3.17 (> 1) | **0.790** |
| ρ_v = 0.05 ρ_w | 1.062 | 0.106 | 2.12 (> 1) | **0.703** |

- **M2 fails.** It is at most 0.38, below both f_v0 values, for any clock.
- **M1 is unphysical** at all sizes.
- **M3 spans 0.66–0.79.** That includes [GM]'s 0.737 (with the collapse
  barrier) and lies just above [NW15]'s 0.627, which is reached with a
  small minimum radius (Sec. 8.2).

### 8.2 Clock-dependent: sizes and minimum radii (collapse barrier δ_c = 1.686)

Legend: r_med = volume-weighted median radius; r ≥ … = M3 volume fraction
of voids above that radius; r_min = the minimum radius at which the M3
fraction equals f_v0. Radii are in h⁻¹ Mpc.

**[GM] (f_v0 = 0.737):**

| Clock | Barrier | r_med | r ≥ 1 | r ≥ 5 | r ≥ 10 | r ≥ 15 | r_min for f_v0 |
|---|---|---|---|---|---|---|---|
| C1 | shell crossing | 2.40 | 0.695 | 0.265 | 0.036 | 0.003 | **0.51** |
| C1 | 0.1 | 0.77 | 0.519 | 0.020 | 0.000 | 0.000 | 0.19 |
| C1 | 0.05 | 0.18 | 0.155 | 0.000 | 0.000 | 0.000 | 0.06 |
| C2 comoving | shell crossing | 0.70 | 0.446 | 0.018 | 0.000 | 0.000 | 0.09 |
| C2 Mészáros | shell crossing | 0.41 | 0.309 | 0.003 | 0.000 | 0.000 | 0.04 |
| C3 tracker seed | shell crossing | 3.39 | 0.727 | 0.394 | 0.098 | 0.014 | 0.81 |
| C3 tracker seed | 0.1 | 1.21 | 0.623 | 0.074 | 0.001 | 0.000 | 0.33 |
| C3 PBS 10⁻² | shell crossing | 13.31 | 0.752 | 0.737 | 0.637 | 0.480 | 5.00 |
| C3 PBS 10⁻² | 0.1 | 7.10 | 0.764 | 0.675 | 0.429 | 0.183 | 3.03 |
| C3 PBS 10⁻⁴ | shell crossing | 22.09 | 0.752 | 0.752 | 0.734 | 0.676 | 9.60 |
| C3 PBS 10⁻⁴ | 0.1 | 13.40 | 0.765 | 0.754 | 0.675 | 0.531 | 6.57 |
| C3 PBS 10⁻⁴ | 0.05 | 7.34 | 0.789 | 0.719 | 0.504 | 0.243 | 4.39 |

**[NW15] (f_v0 = 0.627):**

| Clock | Barrier | r_med | r ≥ 1 | r ≥ 5 | r ≥ 10 | r ≥ 15 | r_min for f_v0 |
|---|---|---|---|---|---|---|---|
| C1 | shell crossing | 2.80 | 0.715 | 0.311 | 0.046 | 0.003 | **1.95** |
| C1 | 0.1 | 1.00 | 0.583 | 0.035 | 0.000 | 0.000 | 0.81 |
| C1 | 0.05 | 0.28 | 0.251 | 0.000 | 0.000 | 0.000 | 0.29 |
| C2 comoving | shell crossing | 1.26 | 0.590 | 0.073 | 0.001 | 0.000 | 0.82 |
| C2 Mészáros | shell crossing | 0.93 | 0.517 | 0.032 | 0.000 | 0.000 | 0.58 |
| C3 tracker seed | shell crossing | 3.38 | 0.730 | 0.386 | 0.083 | 0.009 | 2.40 |
| C3 tracker seed | 0.1 | 1.28 | 0.636 | 0.072 | 0.001 | 0.000 | 1.05 |
| C3 PBS 10⁻² | shell crossing | 12.46 | 0.752 | 0.735 | 0.620 | 0.441 | 9.78 |
| C3 PBS 10⁻² | 0.1 | 6.85 | 0.764 | 0.671 | 0.401 | 0.147 | 5.98 |
| C3 PBS 10⁻⁴ | shell crossing | 19.86 | 0.752 | 0.751 | 0.726 | 0.650 | 16.10 |
| C3 PBS 10⁻⁴ | 0.1 | 12.27 | 0.765 | 0.751 | 0.654 | 0.480 | 10.92 |
| C3 PBS 10⁻⁴ | 0.05 | 6.88 | 0.789 | 0.710 | 0.462 | 0.184 | 7.00 |

- **The turnaround barrier.** δ_c = 1.062 lowers the all-size M3 fraction
  to 0.656 (shell crossing), which is below [GM]'s f_v0. It gives [NW15]'s
  f_v0 at r_min = 1.26 (C1). The artifact has every combination.
- **The other variants.** C3 with A_v = 0 gives voids smaller than
  0.25 h⁻¹ Mpc. Every M1 and M2 entry is in the artifact.
- **The dominant voids.** [W09] (ll. 277–285) says 30 h⁻¹ Mpc-diameter
  voids "fill 40–50% of the universe", with "numerous minivoids" besides,
  all with the same curvature scale.
  - With C1, C2 or the C3 tracker seed, voids ≥ 10 h⁻¹ Mpc fill ≤ 10%.
  - Only 1G-D's original PBS clock reaches [W09]'s range: 62–73% at shell
    crossing and 40–68% at ρ_v = 0.1 ρ_w (f_vi = 10⁻² and 10⁻⁴).
- **The resolution.** The part of the void mass below the R_L grid
  (10⁻³ Mpc) is below 4e−4 for every row of these tables. It is larger only
  for the near-empty C2 populations (≤ 4.3%) and for C3 with A_v = 0
  (≤ 15%); it is recorded per entry.

## 9. History (clock C1) versus the tracker

M3 volume fraction at earlier times, compared with the tracker's
`f_v(t) = t/(t+τ)`. The clock and the frame factor are evaluated at t:
`D(t) = γ_w(1−f_v)^{1/3}/(1+z)`. Shell-crossing barrier, δ_c = 1.686.

| z | [GM] tracker f_v | [GM] M3, r ≥ 1 | [GM] M3, all sizes | [NW15] tracker f_v | [NW15] M3, r ≥ 1 | [NW15] M3, all sizes |
|---|---|---|---|---|---|---|
| 0 | 0.737 | 0.695 | 0.752 | 0.627 | 0.715 | 0.752 |
| 0.5 | 0.630 | 0.559 | 0.752 | 0.496 | 0.588 | 0.752 |
| 1 | 0.540 | 0.383 | 0.752 | 0.397 | 0.403 | 0.752 |
| 2 | 0.401 | 0.102 | 0.752 | 0.267 | 0.099 | 0.752 |
| 3 | 0.306 | 0.013 | 0.752 | 0.191 | 0.011 | 0.752 |

- **All sizes.** The excursion-set fraction is constant in time, since
  𝒟 is.
- **A fixed comoving r_min.** The fraction then rises much faster than the
  tracker's (the voids above the threshold appear only as σ(t) grows).
- **The tracker lies in between.** Reproducing its history would need a
  minimum radius that shrinks toward high z. The tracker's kinematic law
  `f_v/f_w = t/τ` is not the growth law of the excursion-set population for
  any fixed comoving threshold.

This is a second, independent self-consistency test, and it fails as a
constant-threshold statement.

## 10. Polydisperse Boolean variance

**Covariance** (standard stochastic geometry; [1G-E] E2 generalised). For
Poisson balls with radius measure n(ρ)dρ, a point pair at distance r is
uncovered with probability `exp(−∫n(ρ)[2V_ρ − γ_ρ(r)]dρ)`. Write
`p_V(ρ)` for the volume-weighted radius distribution and f for the
covered fraction, `∫nV = −ln(1−f)`. Then

```text
ξ_w(r) = (1−f)^{−E_V[γ̃(r/ρ)]} − 1,   γ̃(u) = 1 − 3u/4 + u³/16  (u < 2),
σ²_part(R) = ∫ P_R(r) ξ_w(r) dr,
σ²(R) = δ_v² σ²_part + [1 − f(1+δ_v)]² σ²_int,   σ²_int = ∫dlnk Δ²_L(ks) K(k),  K = ∫P_R (1+ξ_w) j0(kr) dr.
```

- **The wall weight.** `1 − f(1+δ_v) = f_w − f δ_v` follows from mass
  conservation of the walls. This is GE-F1's correction; it is 1 for empty
  voids.
- **The shape.** Every mapping M1–M3 conserves the shape of p_V; only the
  amplitude differs ([JLH13] below (17)). So the shape comes from
  (clock, barrier), and f is either the tracker's f_v0 or a mapping's
  prediction.

**One-radius limit and the [1G-E] numbers** (gates):
- ξ_w equals [1G-E]'s `xi_wall_indicator` to ≤ 1e−13.
- The composite Gauss–Legendre σ²_part equals [1G-E]'s quad to ≤ 1e−9.
- σ_int with `s = f_w^{1/3}` equals [1G-E]'s `sigma2_internal` to ≤ 1e−6.
- The a = 15 h⁻¹ Mpc case reproduces [1G-E]: σ_part 1.1298 / 0.9108,
  σ_int 1.0926 / 1.0056, σ 1.5717 / 1.3567.

The same case under the Sec. 3 conventions:

| a = 15 h⁻¹ Mpc, f_v0 | [GM] σ_int | [GM] σ | [NW15] σ_int | [NW15] σ |
|---|---|---|---|---|
| [1G-E] s = f_w^{1/3} | 1.093 | 1.572 | 1.006 | 1.357 |
| photon frame s = D_wall | 1.348 | **1.759** | 1.220 | **1.523** |
| s = 1 | 1.464 | 1.850 | 1.267 | 1.561 |
| s = f_w^{1/3}, δ_v = −0.8, [1G-E] formula | — | 1.418 | — | 1.242 |
| s = f_w^{1/3}, δ_v = −0.8, mass-conserving | — | 1.298 | — | 1.142 |

The last row reproduces the 1G-E auditor's GE-F1 values.

**The self-consistent populations.** Tracker-normalised (f = f_v0), collapse
barrier, photon-frame compression. The last column of each set uses the
barrier's own interior density
(`1+δ_v = x/(f_w + x f_v)`, e.g. −0.505 [GM] at shell crossing).

| Clock | Barrier | [GM] σ_part | [GM] σ_int | [GM] **σ (empty voids)** | [GM] σ (barrier interior) | [NW15] σ_part | [NW15] σ_int | [NW15] **σ (empty)** | [NW15] σ (barrier) |
|---|---|---|---|---|---|---|---|---|---|
| C1 | shell crossing | 0.326 | 0.932 | **0.987** | 0.615 | 0.304 | 0.940 | **0.988** | 0.722 |
| C1 | 0.1 | 0.109 | 0.856 | 0.863 | 0.673 | 0.114 | 0.877 | 0.885 | 0.756 |
| C1 | 0.05 | 0.026 | 0.839 | 0.840 | 0.737 | 0.031 | 0.860 | 0.860 | 0.794 |
| C2 comoving | shell crossing | 0.111 | 0.856 | 0.863 | 0.547 | 0.154 | 0.888 | 0.901 | 0.667 |
| C2 Mészáros | shell crossing | 0.068 | 0.846 | 0.849 | 0.539 | 0.116 | 0.877 | 0.885 | 0.656 |
| C3 tracker seed | shell crossing | 0.428 | 0.977 | 1.067 | 0.657 | 0.353 | 0.960 | 1.023 | 0.744 |
| C3 PBS 10⁻² | shell crossing | 1.022 | 1.287 | 1.644 | 0.967 | 0.808 | 1.169 | 1.421 | 0.993 |
| C3 PBS 10⁻⁴ | shell crossing | 1.246 | 1.406 | 1.879 | 1.093 | 0.969 | 1.245 | 1.578 | 1.089 |
| C3 PBS 10⁻⁴ | 0.1 | 1.025 | 1.289 | 1.647 | 1.238 | 0.801 | 1.166 | 1.415 | 1.174 |

- **The [1G-E] compression** (`s = f_w^{1/3}`) lowers each σ_int by about
  18%. C1 shell crossing then gives σ = 0.823 ([GM]) and 0.833 ([NW15]).
- **The M3-predicted and M2-predicted normalisations** are in the artifact.
  With the M3 normalisation (f = 0.752), C1 gives σ = 0.994 ([GM]) and 1.049
  ([NW15]).
- **The no-partition limit.** Near-empty C1 populations approach it: σ_int
  alone, 0.84–0.86, the 1G-C wall statistic at the photon-frame
  compression.

## 11. Monte Carlo check of the polydisperse covariance `NUMERICALLY_CORROBORATED`

**Method.** Voids are Poisson balls in a periodic box, with radii drawn
from the derived number distribution. The smallest voids, carrying ≤ 2% of
the void volume, are dropped to keep the count finite. The analytic formula
is evaluated for the realisation's own balls (its radius sample and covered
fraction), as [1G-E] did for its intensity.

**Exact coverage test.** A point x is covered iff
`min_i (|x − c_i|² − ρ_i²) < 0`.
- Radii are split into classes of width ×1.25.
- Within a class, the lifted centres `(c_i, √(ρ_hi² − ρ_i²))` and the query
  `(x, 0)` have squared 4D distance `|x − c_i|² + ρ_hi² − ρ_i²`, so one
  k-d-tree nearest-neighbour query per class decides coverage exactly.

**Samples.** Seed 29092026 (plus a fixed offset per case); 10⁶ points per
separation; 8000 balls of radius R with 1000 points each, shot noise
subtracted. Boxes are ≥ 20 × the 95th-percentile void radius and ≥ 20 R.

**Cases.** Tracker-normalised, shell crossing, δ_c = 1.686; C1 (small
voids) and C3 PBS 10⁻² (large voids), for both parameter sets.

| Case | box (Mpc) | balls | radius range (Mpc) | f_w: MC vs formula | expected box scatter of f_w | max gated ξ_w error | σ²_part: MC / formula | jackknife error |
|---|---|---|---|---|---|---|---|---|
| [GM] C1 | 219 | 1 129 532 | 0.47–18.6 | 0.21% | 1.15% | **2.3%** | 0.1059 / 0.1010 (+4.9%) | 5.6% |
| [GM] C3 PBS | 802 | 80 421 | 5.4–65.6 | 0.00% | 1.41% | **0.4%** | 1.0437 / 1.0296 (+1.4%) | 1.8% |
| [NW15] C1 | 278 | 449 752 | 0.77–24.7 | 0.20% | 1.12% | **0.8%** | 0.0983 / 0.0951 (+3.3%) | 4.5% |
| [NW15] C3 PBS | 876 | 51 664 | 6.3–67.1 | 0.01% | 1.24% | **1.3%** | 0.6707 / 0.6684 (+0.3%) | 0.9% |

**Covariance points.** The separations are 0.25, 0.5, 1 and 2 × the
volume-weighted median void radius, and 0.5, 1 and 1.5 × R (spanning the
pair density on [0, 2R]).
- Gated points (analytic ξ_w ≥ 0.2) agree to ≤ 2.3%.
- The ungated points with ξ_w < 0.2 agree to ≤ 2.2% for C3.
- For C1 they deviate by up to 9% at r = R (ξ_w ≈ 0.06) and 25% at
  r = 1.5R (ξ_w ≈ 0.013). This is sampling noise on a small covariance:
  the absolute differences are ≤ 0.005.

**Gates.**
- f_w and the gated covariance points: 5%, the [1G-E] gate.
- The ball variance: max(5%, 3 jackknife errors), where the jackknife is
  leave-one-octant-out over the ball centres.

**The first run and why the ball gate changed.** The first full run used
[1G-E]'s configuration: ball variance gated at a flat 5%, and a box of
10 R (130 Mpc for [GM] C1). It failed at 6.8%. Four seeds of that
configuration gave:
- f_w within ≤ 1.0% and all four covariance points within ≤ 1.6%;
- ball-variance errors of +6.8%, −2.8%, +5.1% and +0.9%.

The ball estimator averages over only about (L/2R)³ ≈ 200 independent
volumes of one realisation, so its own scatter is about 4%. That is a
property of the estimator, not a model error: the covariance, which the
ball variance integrates exactly (the [1G-E] pair identity), agreed
throughout. The boxes were then enlarged (10 R → 20 R, and 12 → 20 × r₉₅),
the covariance was sampled at three more separations, and the ball
variance was gated against its own jackknife error. The covariance gate
itself (5%) was not changed. The C1 ball variance is still limited to
about 1000 independent volumes; its deviations (+4.9%, +3.3%) are within
one jackknife error.

## 12. Interpretation and limits

1. **What is established.** Under F1–F6:
   - the excursion-set void population of the Timescape early universe
     accounts for the tracker's present void fraction, but only through the
     two-scale volume budget (M3);
   - it does so with small voids (median 2–3 h⁻¹ Mpc), not with a single
     15 h⁻¹ Mpc population;
   - the self-consistent two-phase σ at 8 h⁻¹ Mpc is about 1.0 with empty
     voids.
2. **What is not.**
   - M3 is the tracker's bookkeeping, not an N-body-validated mapping. The
     ΛCDM-validated mapping (M2) fails the f_v0 test outright.
   - The EdS thresholds are exact only under C1.
   - C3 is used below its validity scale R*.
   - The Markovian walks and the tophat-σ pairing are standard
     approximations.
   - Void shapes, void walls (ridges), and correlations between voids and
     between the voids and the wall field (E3) are not modelled.
   - The history test (Sec. 9) shows that the tracker's f_v(t) is not
     reproduced by a fixed threshold.
3. **Sensitivity ranking** (for σ at 8 h⁻¹ Mpc):
   - the clock: a factor 1.9 between C1/C2 and the original PBS C3;
   - the void interior (empty vs barrier density): −25 to −40%;
   - the E4 frame: about 18%;
   - the barrier: 13–15% from shell crossing to ρ_v = 0.05 ρ_w;
   - the parameter set: ≤ 5% for C1.
4. **Relation to earlier phases.**
   - [1G-E]'s one-radius numbers are reproduced exactly as the one-radius
     limit.
   - [1G-E]'s primary radius is now seen to require 1G-D's disputed PBS
     response.
   - The 1G-C/1G-D wall-internal σ is the no-partition limit.
   - 1G-D's conclusion stands: the partition is non-perturbative at
     8 h⁻¹ Mpc (σ_part ≈ 0.3 for the C1 population at shell crossing).
5. **Comparison with ΛCDM.** Planck-ΛCDM's σ8 = 0.811 is linear. σ ≈ 1.0
   here is a nonlinear two-phase statistic. No comparison with data or with
   ΛCDM's nonlinear variance is made. [1G-E] Sec. 6 item 2 (a matched
   observable) remains the prerequisite.

## 13. Proposed status tokens (none added; each requires owner approval)

- `EXCURSION_SET_TRACKER_VOID_FRACTION_CONSISTENCY = "CONSISTENT_ONLY_UNDER_TWO_SCALE_VOLUME_BUDGET"`
  (Secs. 8–9). The excursion set reproduces f_v0 only under M3, and only
  counting voids down to 0.5–2 h⁻¹ Mpc; no fixed threshold reproduces f_v(t).
- `VOID_FORMATION_GROWTH_CLOCK = "EXTERNAL_CLOSURE_INPUT"` (Sec. 4 F3).
- `POLYDISPERSE_TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"`
  (Sec. 10, under F1–F6).

## 14. Recommendations (none applied; each requires owner approval)

1. **Owner decisions this phase informs:**
   - GE-OD2 (the 1G-E primary void population): 1G-F provides a derived
     alternative;
   - GE-OD3 with lead observation L1 (the E4 frame);
   - GD-OD1/OD2 (the void-seed scale), which decides whether C3 can give
     [W09]-sized voids.
2. **Next theory step (1G-G, proposed).** Replace the fixed-threshold
   population with a void-evolution model that carries the tracker's
   kinematics: voids expanding as Milne regions after shell crossing, with
   merging. Test it against the history of Sec. 9 and against [W09]'s 40–50%
   in dominant voids.
3. **Matched observable** ([1G-E] Sec. 6 item 2): still needed before any
   comparison.
4. **Author questions:** how do the Timescape authors relate the tracker's
   f_v to a void size distribution? Are minivoids part of the Milne phase
   ([W09] ll. 283–285 say so)?

## 15. Reproduction and validation

```text
.venv/bin/python -B -W error scripts/phase1g_f_void_population_numerics.py
→ wrote artifacts/independent/phase1g_f_void_population.json
```

**Asserted budgets:**
- tophat roots, xtol 1e−15, and every [JLH13] value to its printed digit;
- images vs Fourier ≤ 1e−13, and the normalisation 1 − 𝒟 to ≤ 1e−11;
- σ table grid convergence ≤ 1e−8 (achieved 7e−11);
- one-radius limit vs [1G-E]: ξ_w ≤ 1e−13, σ²_part ≤ 1e−9, σ_int ≤ 1e−6;
- the Milne limit to 1e−12;
- the one-scale identity (history) ≤ 1e−13;
- Monte Carlo as in Sec. 11.

**Runs.** CPython 3.13.12 (NumPy 2.5.3, SciPy 1.18.1) and 3.11.15
(NumPy 2.4.6, SciPy 1.17.1), Linux x86-64 with AVX-512:
- **1G-F script.** 568 s and 575 s, peak memory 1.5 GB. The two artifacts
  are identical in every result and budget; only the `environment` block
  differs.
- **Full suites** (`-B -W error -p no:cacheprovider`, final tree):
  **1048 passed, 1 failed, 0 skipped** on each interpreter.
  - 1049 = the owner's 1044 plus the 5 tests of
    `tests/test_phase1g_e_status_addition.py`.
  - The failure is `test_top_hat_window_limits_series_and_envelope`
    (GB-F1; platform-dependent bitwise evenness of `x ** 3`, an owner
    decision). The preflight at `6f7937c` gave 1043 passed and the same one
    failure.
- **Validator and tolerance audit.**
  `scripts/validate_phase1f_c_r_astra_remediation.py --producers`: `PASS`
  on both. `scripts/audit_numerical_tolerances.py`: 633 comparisons, 0
  missing.
- **Every other Phase 1G script** (`phase1g_a`, `_c`, `_d`, `_e` numerics
  and `validate_phase1g_b_lagrangian_sigma.py`): exit 0 on both, with
  byte-identical printed output.
  - Their artifacts agree between interpreters except the environment and
    provenance blocks.
  - For 1G-D, the [GM] (4.11) residual diagnostics also differ at round-off
    (≤ 1.9e−15, budget 1e−12).

## 16. Preservation

- **Added:** this report, its inventory, and one script.
- **Modified:** the CLAUDE.md phase ledger and the README σ-track paragraph
  (text only).
- **Unchanged:** every package module, test, status token, tolerance and
  frozen report.
- **Remote:** this session's branch is pushed and one draft pull request is
  opened, under approval 2 of Sec. 1. Nothing is merged or tagged.
