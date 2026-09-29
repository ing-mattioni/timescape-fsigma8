# Phase 1G-A — σ(M) derivation-path audit for the Timescape CGI framework

Audit classification: `REPORT_ONLY_DERIVATION_PATH_AUDIT_WITH_NUMERICAL_EVIDENCE`.
Base checkpoint: `3213242` (`main` = `origin/main`), branch
`phase-1g-a-sigma8-derivation-path`. Date: 2026-09-29.
Machine-readable companion:
[`phase1g_a_sigma8_derivation_path_inventory.json`](phase1g_a_sigma8_derivation_path_inventory.json).
Numerical evidence: `scripts/phase1g_a_sigma8_path_numerics.py`, which writes
the git-ignored `artifacts/independent/phase1g_a_sigma8_path.json`.

References: [GM] Galoppo & Mourier, arXiv:2511.17160v2 (JCAP 02 (2026) 066);
[W09] Wiltshire, arXiv:0909.0749v2; [NW15] Nazer & Wiltshire,
arXiv:1410.3470; [DNW13] Duley, Nazer & Wiltshire, arXiv:1306.3208;
[EH98] Eisenstein & Hu, ApJ 496, 605, astro-ph/9709112; [P18] Planck 2018
VI, arXiv:1807.06209.

## 1. Scope, authorisation and verdict

**Authorisation.** On 2026-09-29 the project owner asked to "advance the
theoretical framework of the project pursuing any road that seems
promising", recalling that "the final scope of the project is to derive
sigma8". Crossing the σ8 scope firewall requires a new audited phase
(`CLAUDE.md`). This is that phase's first step: an audit with numerical
evidence. It adds no package code, changes no equation, status token or
tolerance, and makes no observational claim. `SIGMA8_AUTHORIZATION` stays
`NOT_GRANTED` until a human decides otherwise.

**Verdict.** A derivation path from the primordial spectrum to a Timescape
σ(M) now exists **inside the [GM] framework**, and every link is classified
below. It follows the route the [GM] authors themselves propose (Sec. 3). It
also removes three of the five σ-level blockers recorded in 1D-C §34:

| 1D-C §34 item | Status after this audit |
|---|---|
| 4. Ensemble interpretation | Resolved for the comoving closure (Sec. 4.3) |
| 5. Barotropic high-k regularisation | Closed negatively: the closure is Hadamard ill-posed, and no linear barotropic σ_R exists (Sec. 4.1) |
| 1. Dressed spatial Fourier map | Not needed for σ(M) at linear order. It is replaced by a Lagrangian mass label plus an explicit radius convention worth 7–15% (Sec. 6) |
| 3. Dressed redshift-space Jacobian | Unchanged (RSD; out of scope) |
| 6. Galaxy bias | Unchanged (out of scope) |

**The conditional numbers.** Assume the comoving closure, the regular
growing mode, standard early-universe physics, the same primordial spectrum
as Planck, and Planck's baryon fraction. Then the Timescape linear σ at the
Planck `M8` is:
- **0.524** with the [GM] parameters (f_v0 = 0.737);
- **0.669** with the Timescape CMB-fit parameters of [NW15] (f_v0 = 0.627);
- against **0.811** for Planck ΛCDM.

With the Mészáros approximation, or with the other radius conventions, the
values span 0.45–0.69 (Sec. 7).

**The decisive caveat.** The [GM] framework grows perturbations on the
*volume-average* background. That background has a low bare matter density
(Ω̄_M0 = 0.14–0.22), so its growth is open-universe-like. Structures,
however, live in wall regions. [W09]'s two-scale solution assumes no
backreaction inside walls, so its regional wall scale is exactly
Einstein–de Sitter in the common time t. Growing sub-wall perturbations
with that region's growing mode would instead give σ(M8) ≈ 0.83–0.96, at
or above ΛCDM (Sec. 8).

The two answers differ by a factor of about 1.4–1.6. The growth law of
sub-homogeneity perturbations inside walls is therefore the decisive open
problem for a Timescape σ8. It is the same regional-embedding problem that
1E–1F, 1F-D and the LTB–CMC experiment already address. A notational
finding supports the analysis: [GM] use `a_w` for two different scale
factors (Sec. 5.3).

## 2. Provenance and method

- **[GM]** LaTeX source, arXiv e-print v2, `main.tex`, SHA-256
  `f9cadfa0…77c59`.
  - Printed equation numbers were reconstructed from the source (section
    counter, one number per unstarred display row without `\nonumber`).
  - They agree with every number the repository already cites: (4.13)–(4.17)
    barotropic, (4.21)–(4.23) comoving, (4.27) Mészáros, (5.4)–(5.7) tracker.
  - The homogeneous-density closure is (B.3)–(B.5); the general dust-frame
    system is (4.9)–(4.12).
- **[W09]** e-print `observe.tex`, SHA-256 `2b0324d1…4b531`.
- **[NW15]** and **[DNW13]:** abstracts only (arXiv API).
- **Downloads:** all live only in the session scratchpad. No upstream,
  package or frozen report file was touched.
- **Timescape quantities:** every one comes from frozen package functions.
  External formulas appear only in the script and are labelled
  `PROVISIONAL_MODEL_IMPORT` (Sec. 6.3).

Evidence classes follow 1D-C §5:
- `VERIFIED_FROM_PRIMARY_SOURCE`;
- `DERIVED_FROM_VERIFIED_DEFINITIONS`;
- `NUMERICALLY_CORROBORATED`;
- `PROVISIONAL_MODEL_IMPORT`;
- `CONVENTION_DEPENDENT`;
- `NOT_DERIVED`.

## 3. The authors' own route to σ8/fσ8 `VERIFIED_FROM_PRIMARY_SOURCE`

[GM] Conclusions (source line 1102) sketch the route verbatim:

> "As inhomogeneities remain very small in the pre-recombination Universe,
> the perturbations in the dust/radiation mixture fluid could be treated in
> the standard approach, with a homogeneous background and no additional
> effective source. After the transition to the matter-dominated era, the
> acoustic peaks in the dust perturbations would grow in a scale-independent
> way, as in the ΛCDM framework, yet with a modified growth rate. This would
> come from averaged-over nonlinear effects, modelled as in this work via an
> effective fluid, with a comoving parametrisation of its perturbations."

They also call the comoving closure "a much more physically relevant
parametrisation" (line 1097). [NW15] independently exploits the fact that
Timescape "is extremely close to the standard cosmology at early epochs"
to run standard CMB codes. This audit takes that route and closes, or
classifies, each link.

## 4. Which closures admit a σ at all?

### 4.1 Barotropic closure: Hadamard ill-posed for c²_s < 0

`DERIVED_FROM_VERIFIED_DEFINITIONS` + `NUMERICALLY_CORROBORATED`

**The operator.** In [GM] Eq. (4.19) the only wavenumber dependence is the
term `c²_s (k²/a²) Δ^(eff)` in the bracket. With `k²/a² ↔ −³Δ`, the
principal part is `Δ̈^(eff) − c²_s ³Δ Δ^(eff)`:
- for `c²_s > 0` this is a wave operator (hyperbolic);
- for Timescape `c²_s,eff < 0` throughout (from −0.4996 at z = 20 to
  −0.3912 today, frozen 1B) it is elliptic in space–time.

**Consequence.** The Cauchy problem is therefore ill-posed in Hadamard's
sense: an initial-data perturbation of wavenumber k is amplified by about
`exp(k α)`. In the frozen matrix ([GM] (4.15), (4.17)),
`A23·A32 = −c²_s k²/a_D² > 0`, so the WKB rate is `k √(−c²_s)/a_D`.

**Numbers.** With dressed H0 = 1 and the matrix-convention k:
- `α = ∫_{t(z=20)}^{t0} √(−c²_s,eff) dt/a_D = 1.70695`.
- Direct integration of the frozen `barotropic_rhs` gives slopes
  `d ln|Δ^(eff)(t0)|/dk` of 1.4755, 1.6167, 1.6700, 1.6907 and 1.6994 at
  k = 4π…64π (`derived_4_10`); `printed_4_15` gives 1.3659 … 1.6996. Both
  converge to α from below, as the WKB amplitude prefactor predicts, and D3
  does not change the rate.
- `Δ_d(t0)` changes sign on `derived_4_10` already at k = 2π: the reversal
  [GM] report.

**At σ8 scales.** Take kR = 1 with R = 8/h Mpc (h = 0.7303) and the 1D-A §10
unit chain: k_matrix ≈ 513 and `αk ≈ 875`. That exceeds
`ln(float64 max) = 709.8`, so the linear barotropic amplitude is not even
representable.

**Result.** Take any smoothing radius R > 0, a window with power-law tails,
and any spectrum bounded below by a power law. The integrand of
`σ_R² = ∫ dlnk Δ²_δ D²(k) W²(kR)` then grows like `e^{2α'k}` (α' < α), and
σ_R diverges. **No linear barotropic σ_R exists** for the Timescape tracker.

This closes 1D-C §34 item 5 negatively. It also explains the
"instabilities" and sign "reversals" of [GM] Fig. 3 as ill-posedness of the
closure, not as physics. The token `UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY`
is `NOT_DERIVED`; this audit recommends `REFUTED_HADAMARD_ILL_POSED`
(Sec. 10; requires human approval).

### 4.2 Homogeneous-density closure ([GM] App. B): backward-parabolic

`DERIVED_FROM_VERIFIED_DEFINITIONS`

**The operator.** In [GM] Eq. (B.4) the bracket contains `−k²/a²`
multiplied by `1/(2Θ)`, so the principal part is
`Δ̇^(eff) = +(k²/2Θa²) Δ^(eff) = −(1/2Θ) ³Δ Δ^(eff)`. For an expanding
background (Θ > 0) this is a **backward heat equation**. The k²-dependent
entry of (B.5) couples to Δ^(eff) only through an O(1) entry, so the
leading eigenvalue of the high-k system is `+k²/(2Θa²)`.

**Consequence.** The initial-value problem is ill-posed, and modes grow like
`exp(k² ∫dt/2Θa²)`, faster than the barotropic case. [GM] did not use this
closure. It is recorded here to complete the classification. It was not
numerically corroborated, because the package has no (B.3)–(B.5)
implementation.

### 4.3 Comoving closure: pointwise ODEs, scale-independent, ensemble-preserving

`DERIVED_FROM_VERIFIED_DEFINITIONS`

**Pointwise ODEs.** [GM] Eqs. (4.21)–(4.23) contain no spatial operator: the
system is ODEs "even when not written in spatial frequency space" ([GM]
Sec. 4.3). It is well-posed. After the decaying modes have decayed (they
fall as `t^{-5/3}` relative to the growing mode, per the `growing_mode`
module), the solution is, at every point,

```text
Δ_d(x, t) = [D(t)/D(t_e)] Δ_d(x, t_e),     δ_m(x, t) = [D(t)/D(t_e)] δ_m(x, t_e),
```

with the δ_m statement following from the exact harmonic map
`Δ_d = −k²_code δ_m` of 1D-A §4 for zero-mean fields.

**Consequences:**
- Statistical homogeneity, isotropy and Gaussianity of the early field are
  inherited exactly in the background's comoving coordinates. This is the
  ensemble interpretation that 1D-C §34 item 4 asked for.
- For any window and any R fixed in background comoving coordinates,
  `σ_R(t) = [D(t)/D(t_e)] σ_R(t_e)`. The kernel, the spectrum shape and
  the choice of background curvature all cancel, as [GM] note.

### 4.4 Mészáros approximation `VERIFIED_FROM_PRIMARY_SOURCE`

[GM] Eq. (4.27) is an approximation, not a closure. [GM] (Sec. 5.1.1) state
it "should not be applicable in the timescape framework". It is kept only as
the comparator [GM] use.

**Conclusion of Sec. 4.** Among the closures in [GM], only the comoving
closure (and the Mészáros comparator) can define a linear σ. That agrees
with the authors' stated preference.

## 5. Growth factor: Timescape against ΛCDM at equal early photon temperature

### 5.1 Early-time frame coincidence `DERIVED_FROM_VERIFIED_DEFINITIONS`

[GM] text p. 25 gives `1 + z = a_w0/a_w = γ_w (a_D/a_w0)^{-1}` and
`γ_w = 1 + f_v/2`, with `a_D = a_w` at last scattering. So
`a_D(t)/a_D0 = [γ_w(t)/γ_w0] · 1/(1+z)`. Early on, frames agree to
`O(f_v/2)`:

| z | 20 | 50 | 100 | 300 |
|---|---|---|---|---|
| γ_w − 1 (f_v0 = 0.737) | 1.73e−2 | 4.65e−3 | 1.68e−3 | 3.3e−4 |

In the matter era both backgrounds are Einstein–de Sitter:
- Timescape in `a_D` ([GM] (5.5)–(5.6) with f_v → 0);
- ΛCDM in `a = 1/(1+z)`.

Normalise each growing mode by `D/a_photon → 1` early, with
`a_photon := 1/(1+z)`. Matching equal δ at equal early photon temperature
(the [GM] IC convention, taken deep in the matter era) then gives

```text
X∞ := σ_TS(M, t0)/σ_ΛCDM(M, t0)|_(same early σ(M))  =  γ_w0 · g_TS / g_Λ ,
g_TS := lim_{t_e→0} [D(t0)/D(t_e)]·[a_D(t_e)/a_D0]   (growth relative to volume-average EdS),
g_Λ  := qplus(0) = 0.787813                          (frozen flat-ΛCDM recipe, Ω_m = 0.315).
```

`γ_w0` is the extra expansion of the volume average relative to the
photon redshift. `g_TS` is the suppression of growth relative to
volume-average EdS.

### 5.2 Numbers `NUMERICALLY_CORROBORATED`

g_TS is computed as `exp ∫ (u − tΘ/3) d ln t` on the regular growing
solution, where `u = t d lnΔ_d/dt` comes from the frozen `growing_mode`
module. It is cross-checked by direct integration of the frozen
`comoving_rhs` / `meszaros_rhs`.

| Parameters | f_v0 | γ_w0 | Ω̄_M0 (bare) | g_TS comoving | X∞ comoving | g_TS Mészáros | X∞ Mészáros |
|---|---|---|---|---|---|---|---|
| [GM] paper / notebook | 0.737 | 1.3685 | 0.1404 | 0.402663 | **0.6995** | 0.341694 | 0.5936 |
| [NW15] CMB fit | 0.627 | 1.3135 | 0.2162 | 0.514953 | **0.8586** | 0.458563 | 0.7646 |

**Convergence and checks:**
- Simpson grid refinement changes ln g by ≤ 4e−15.
- The early limit (t_e/t0 = 1e−5 → 1e−6) changes it by ≤ 2e−5.
- Direct integration agrees with the Riccati integral to ≤ 2e−13 at
  z_i = 20 and ≤ 2e−11 over all z_i (both closures, all cases).
- X depends only on f_v0: the paper and notebook presets agree to every
  digit.
- **Precision note (from Phase 1G-B, 2026-09-29):**
  - Starting at t_e = 1e−6 t0 leaves out a piece `c·f_v(t_e)` to first
    order, with c = −13/20 (comoving) and −3/4 (Mészáros).
  - This biases ln g by +1.8e−6 and +2.1e−6.
  - The t_e → 0 limits are g_TS = 0.4026623 (comoving) and 0.3416935
    (Mészáros), compared with the printed 0.402663 and 0.341694.
  - This is inside the stated budget and changes no four-decimal X or σ.

**Matching at finite z_i.** Matching at z_i = 20, the [GM] convention, gives
X = 0.7035 (comoving). That is 0.6% above X∞; z_i = 100 gives 0.6998. So the
[GM] matching epoch is harmless *once the regular growing mode is used*. The
[GM] legacy ICs inject a decaying mode worth up to about +14% on Δ_d(t0)
(F1 report, line 48). This is exactly why F1's
`TIMESCAPE_REGULAR_GROWING_MODE` is the correct initial-condition convention
for σ.

**f_v0 scan:**

| f_v0 | 0.50 | 0.55 | 0.60 | 0.627 | 0.65 | 0.695 | 0.737 | 0.75 | 0.80 |
|---|---|---|---|---|---|---|---|---|---|
| X∞ comoving | 1.000 | 0.949 | 0.892 | 0.859 | 0.829 | 0.765 | 0.700 | 0.678 | 0.588 |
| X∞ Mészáros | 0.925 | 0.866 | 0.802 | 0.765 | 0.732 | 0.663 | 0.594 | 0.571 | 0.479 |

**Interpretation.** Timescape's volume-average matter density is low
(Ω̄_M0 = 0.14 for f_v0 = 0.737). Its effective fluid (curvature plus
backreaction, w_eff < −1/3) suppresses growth like an open or accelerating
universe. The γ_w0 ≈ 1.3–1.4 extra expansion only partly compensates. The
comoving coupling (Δ^(eff) sourcing Δ_d) makes growth faster than Mészáros,
as [GM] Fig. 2 shows.

### 5.3 Notational finding: two different `a_w` in [GM] `VERIFIED_FROM_PRIMARY_SOURCE`

[GM] use one symbol for two scale factors:

- **(5.1):** `a_w` is the regional wall *volume* scale factor,
  `a_Y := (V_Y(t)/V_Y(t_init))^{1/3}`. Then `a_w³ = (1−f_v) a_D³ / f_wi`, and
  on the tracker `a_w ∝ t^{2/3}` exactly. [W09] (source lines 1763–1764)
  states this: "a_w = a_w0 t^{2/3}". Numerically,
  `(1−f_v)^{1/3} a_D / t^{2/3}` is constant to rounding.
- **(5.4):** `a_w = γ_w^{-1} a_D` is the null-matched *dressed* scale factor,
  [W09]'s `a ≡ γ̄_w^{-1} ā` (dressed metric `dgeom`, lines 617–623). It enters
  `1+z = a_w0/a_w`. It is not ∝ t^{2/3}: `a_w/t^{2/3}` varies by 16.6% over
  the tracker history for f_v0 = 0.737.

The two differ by `γ_w (1−f_v)^{1/3} f_wi^{-1/3}`. The package's `a_w` (with
its docstring) implements the (5.4) dressed object. Nothing in the package
depends on the (5.1) meaning, so no code is affected. The finding is recorded
here, not "fixed" (AGENTS.md rule 1). It matters only for any regional-growth
construction (Sec. 8).

## 6. Smoothing scale without a global dressed map

### 6.1 Lagrangian mass label `DERIVED_FROM_VERIFIED_DEFINITIONS`

`⟨ρ⟩_D a_D³` is constant ([GM] text p. 25). The mass
`M = (4π/3)⟨ρ⟩_D a_D³ R_com³` in a sphere fixed in background comoving
coordinates is therefore conserved. By Sec. 4.3, `σ(M, t0) = [D(t0)/D(t_e)]
σ(M, t_e)`, and at t_e all frames coincide to O(f_v(t_e)) (Sec. 5.1).

So the **global dressed spatial map of 1D-C §34 item 1 is not needed for a
linear σ(M)**. What remains is only the convention that identifies the
observational "8 h⁻¹ Mpc" with a mass M (Sec. 6.4). This does not solve the
dressed map for light-cone or RSD observables, which remain blocked.

### 6.2 Early-universe matter density per photon

`DERIVED_FROM_VERIFIED_DEFINITIONS`, numerically verified to 1e−13

Combine `⟨ρ⟩_D ∝ a_D^{-3}`, `a_D = a_w` at last scattering,
`1+z = a_w0/a_w` and `a_D0/a_w0 = γ_w0` ([GM] (5.4), p. 25). The early
matter density per photon, as seen by a standard code with T0 = 2.7255 K, is

```text
ω_m,eff = ⟨ρ⟩_D0 γ_w0³ / ρ_crit(100) = ½(1 − f_v0)(2 + f_v0) · (H_D0/100)²,
```

using `⟨ρ⟩_D0 = 12 H_D0²(1−f_v0)/[8πG(2+f_v0)²]` ([GM] p. 25).
`½(1−f_v0)(2+f_v0)` is [W09]'s "canonical dressed value" of Ω_M0 (source
line 880). The identity shows that it is exactly the per-photon matter
density in units of the *bare* critical density.

| Parameters | ω_m,eff | ratio to Planck (0.1431) |
|---|---|---|
| [GM] paper preset | 0.12048 | 0.842 |
| [GM] notebook preset | 0.12114 | 0.847 |
| [NW15] CMB fit | 0.13094 | 0.915 |

The Timescape early universe is Planck-like to 8–16%. That supports the
[GM]/[NW15] early-time matching, but the transfer function must use
ω_m,eff and not Planck's ω_m (Sec. 6.3).

### 6.3 Early spectrum `PROVISIONAL_MODEL_IMPORT`

**Formulas.** At equal photon temperature in the matter era, the Poisson
equation with Φ = −(3/5)ζ gives
`Δ²_δ = (4/25) A_s (k/k_p)^{n_s−1} (k/aH)^4 T²(k)`. With
`(aH)² = H100² ω_m / a_photon`, the Timescape spectrum differs from Planck's
only through T(k; ω_m,eff, ω_b) and the 1/ω_m² factor. T(k) is [EH98]'s
zero-baryon-oscillation fit, Eqs. (26), (28)–(31), which depends only on the
physical densities.

**Inputs:**
- A_s = 2.100e−9, n_s = 0.9649, k_p = 0.05 Mpc⁻¹ [P18];
- baryon fraction f_b = ω_b/ω_m = 0.1563 (Planck).

[NW15] report that the baryon/non-baryon ratio is pinned by the 2nd/3rd peak
ratio "as long as the standard cosmology is assumed up to the surface of last
scattering", so Planck's f_b is the primary closure. f_b = 0.12 and 0.20 are
reported as sensitivity.

**Validation.** EH98 plus these inputs gives Planck σ8 = 0.8357, +3.03%
against the [P18] anchor 0.8111. The expected bias sources are omitted BAO
wiggles and Planck's 0.06 eV neutrino suppression (about −1.5%). The first
run failed a 3% gate; the gate was set to 5% with this reason recorded in
the script. All reported σ values are **Planck-anchored ratios**, in which
the common EH98 bias largely cancels.

### 6.4 Radius conventions `CONVENTION_DEPENDENT`

Three identifications of "8 h⁻¹ Mpc" are carried side by side. All radii are
in photon-normalised comoving Mpc; Planck R8 = 11.869 Mpc.

| Convention | [GM] preset R | [NW15] R |
|---|---|---|
| (a) equal Lagrangian mass, Planck `M8` | 12.570 | 12.226 |
| (b) 8/h_dressed Mpc of wall-comoving length | 10.954 | 13.115 |
| (c) 8/h̄ Mpc of present volume-average proper length | 10.104 | 11.781 |

(a) is frame-free and is the right comparison with ΛCDM predictions at
fixed mass. (b) assumes wall rulers measure wall-comoving length with the
dressed h. (c) uses bare units. (b) and (c) presuppose parts of the
underived dressed map.

## 7. Conditional σ(M8) — the numbers

`σ = X∞ · E · σ8^Planck`. E is the early-spectrum factor at the chosen
radius (EH98), and σ8^Planck = 0.8111. The primary baryon fraction is
f_b = 0.1563; the f_b = 0.12 and 0.20 values are in the artifact.

| Parameters | Closure | (a) equal mass | (b) dressed 8/h | (c) bare 8/h̄ |
|---|---|---|---|---|
| [GM] f_v0 = 0.737 | comoving | **0.524** (E 0.924) | 0.573 (E 1.010) | 0.603 (E 1.063) |
| [GM] f_v0 = 0.737 | Mészáros | 0.445 | 0.487 | 0.512 |
| [NW15] f_v0 = 0.627 | comoving | **0.669** (E 0.960) | 0.637 (E 0.915) | 0.686 (E 0.984) |
| [NW15] f_v0 = 0.627 | Mészáros | 0.595 | 0.568 | 0.610 |
| Planck ΛCDM | — | 0.811 | | |

The baryon-fraction sensitivity (f_b 0.12 → 0.20) is about +7% / −8%
around each entry.

**Status of these numbers.** They are **conditional, model-internal linear
σ(M)**. They are not observational σ8: observational σ8 and S8 values are
compressed in a ΛCDM fiducial (1D-C §23; 1E-A), and no comparison is
authorised. Within the [GM] framework, though, every examined fork gives
**less linear structure than Planck-ΛCDM with the same early universe**:
15–45% less at the primary baryon fraction, and 9–50% less including the
f_b sensitivity rows. The sign of the effect is robust across closures,
presets, conventions and baryon fractions.

## 8. Fork budget and the decisive open problem

| Fork | Typical effect on σ | Class |
|---|---|---|
| Two-scale growth law (volume average vs wall region) | **factor about 1.4–1.6** (X from 0.70–0.86 to 1.11–1.20) | `NOT_DERIVED` — decisive |
| f_v0 (SN-preferred 0.737 vs CMB 0.627) | about 20–25% | external parameter |
| Closure (comoving vs Mészáros) | about 11–15% | [GM] prefers comoving |
| Radius convention (a)/(b)/(c) | 7–15% | `CONVENTION_DEPENDENT` |
| Baryon fraction (0.12–0.20) | ±7–8% | closure; [NW15] pins it near Planck |
| Growing mode vs [GM] legacy ICs | +up to 14% (legacy) | F1: growing mode is correct |
| Matching epoch z_i ≥ 20 | ≤ 0.6% | negligible |
| EH98 vs Boltzmann code (ratio) | ≲ 1% (estimate) | import |

**Two-scale bracket `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`.** In
Timescape, matter and structure sit in walls, and voids are nearly empty.
[W09]'s two-scale Buchert solution assumes "no backreaction within walls and
voids separately" (source line 510). The wall region is then flat and
backreaction-free, so its regional Buchert equations in the common dust time
t are Einstein–de Sitter: `a_w,reg ∝ t^{2/3}` and `⟨ρ⟩_w ∝ t^{-2}`
(Sec. 5.3; [W07] Eq. (11), source-verified by the Astra audit).

**Additional assumption:** sub-wall linear perturbations follow the standard
growing mode of that region, `δ ∝ a_w,reg`. Early on, walls are the whole
universe (f_v → 0), so the early spectrum is shared. Relative to
photon-normalised EdS growth, the growth to t0 is then

```text
lim_{t_e→0} (t0/t_e)^{2/3}/(1+z_e) = γ_w0 (1 − f_v0)^{1/3} = ½(2+f_v0)(1−f_v0)^{1/3},
X_wall = γ_w0 (1 − f_v0)^{1/3} / g_Λ .
```

The closed form equals the exact finite-t_e identity
`(t0/t_e)^{2/3}/(1+z_e) = γ_w0(1−f_v0)^{1/3}/[γ_w(t_e)(1−f_v(t_e))^{1/3}]`
to ≤ 1e−15 (Phase 1G-B). The naive limit at t_e = 1e−8 t0 differs by
−f_v(t_e)/6 ≈ −4.7e−9, as expected. (Corrected 2026-09-29: this line first
claimed 1e−13 agreement with the naive limit.)

| Parameters | X_wall | σ(M8), (a) equal mass | (b) dressed | (c) bare |
|---|---|---|---|---|
| [GM] f_v0 = 0.737 | 1.1129 | 0.834 | 0.912 | 0.960 |
| [NW15] f_v0 = 0.627 | 1.2002 | 0.935 | 0.891 | 0.958 |

This uses *common time t*, not wall proper time τ_w. It therefore does not
conflict with the recorded `REJECTED_UNSUPPORTED` status of the naive
*proper-time* flat-dust identification. It is still not a derived Timescape
prediction:
- the regional embedding stays `NOT_DERIVED`;
- the assumption ignores the coupling of sub-wall modes to wall–void
  boundaries and to the evolving wall fraction.

**The result.** Volume-average CGI growth gives σ(M8) = 0.52–0.69, while
wall-regional growth gives 0.83–0.96 (equal-mass and other conventions).
The σ8 values quoted from low-redshift probes fall between these, but none
of them is comparable without a Timescape reduction of the data (1E-A), so
no consistency or tension claim is made.

**The growth law of perturbations inside wall regions decides where a
Timescape σ8 lies.** That law is the physics of the
`REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING` problem that 1E–1F, 1F-D
and the LTB–CMC experiment investigate. The [GM] comoving closure gives the
volume-average answer. The wall-regional EdS law is the simplest regional
answer. A derived answer that interpolates between them does not yet exist.

## 9. Updated readiness (successor reading of 1D-C §30)

| Candidate | 1D-C verdict | Reading after 1G-A |
|---|---|---|
| A anchored diagnostic | GO as conditional diagnostic (done, 1D-D) | unchanged; superseded for σ by the early-universe route |
| B internal volume-average σ_R | BLOCKED_BY_EXTERNAL_INPUT | **implementable** with an explicit early-spectrum import in the photon-normalised frame (Sec. 6) |
| C barotropic σ_R | BLOCKED_BY_LINEARITY_OR_K_DOMAIN | **permanently excluded**: ill-posed closure (Sec. 4.1) |
| D observational dressed σ8 | BLOCKED_BY_MISSING_SPATIAL_MAP | reduced to (i) a declared radius convention (7–15%) and (ii) the two-scale growth law (decisive) |
| E RSD fσ8 | BLOCKED_BY_MISSING_RSD_MAPPING | unchanged |

## 10. Recommendations (none applied; each requires human approval)

1. **Status token.** Change `UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY`
   from `NOT_DERIVED` to `REFUTED_HADAMARD_ILL_POSED`, citing Sec. 4.1.
2. **Phase 1G-B (implementation):** a package module for the conditional
   mass-labelled σ(M) of the comoving closure (Mészáros as comparator).
   - Mandatory explicit inputs:
     - the early-spectrum provider (EH98 or a Boltzmann-code table, declared
       as a `PROVISIONAL_MODEL_IMPORT`);
     - A_s, n_s, f_b, the radius convention and the parameter preset.
   - Uses the regular growing mode, with deep-matter-era matching.
   - Names carry no `sigma8` token (1D-C §19 naming rules).
   - Its tests reproduce the Sec. 5–7 numbers.
3. **Phase 1G-C (theory, report-only):** the two-scale growth law. Derive how
   linear perturbations inside a wall region evolve in the common time t.
   The starting point is the wall-regional EdS bracket of Sec. 8. The
   corrections come from:
   - sub-wall modes coupling to wall–void boundaries;
   - the decreasing wall fraction;
   - the volume-average CGI limit, which it must interpolate to on
     super-homogeneity scales.

   This connects directly to 1F-D (necessary bound) and to the LTB–CMC
   section family, and it is the decisive input for any Timescape σ8.
4. **Author question** (adds to 1D-C §33): do [GM] regard the
   volume-average CGI growth as the growth of structures inside walls? If
   not, which regional growth law do they envisage for σ8/fσ8?

## 11. Reproduction and validation

```text
.venv\Scripts\python -B -W error scripts\phase1g_a_sigma8_path_numerics.py
→ wrote artifacts\independent\phase1g_a_sigma8_path.json    (about 10 s)
```

The script is deterministic and asserts every budget:
- growth grid ≤ 1e−7 (achieved ≤ 4e−15);
- early limit ≤ 1e−4 (achieved ≤ 2e−5);
- direct vs Riccati ≤ 1e−7 (achieved ≤ 2e−11);
- per-photon identity ≤ 1e−13;
- σ quadrature ≤ 1e−6;
- EH98 Planck validation ≤ 5%.

**Environments (Windows 11):**
- Python 3.14.3 with NumPy 2.5.2 and SciPy 1.18.1;
- Python 3.11.9 with NumPy 2.4.6 and SciPy 1.17.1.

The script gives identical results to every printed digit on both, including
X∞, α, σ(M8) and X_wall.

**Other checks on this branch:**
- Full suites: **916 passed** on both interpreters (`-B -W error`, no
  failures, skips or warnings). This matches `main`; the package is
  unchanged.
- `scripts/audit_numerical_tolerances.py`: 583 comparisons, none missing a
  tolerance.
- `scripts/validate_phase1f_c_r_astra_remediation.py`: `PASS`.

## 12. Preservation statement

- **Files added:** this report, its inventory, and the script.
- **Unchanged:** every package module, test, status token, tolerance,
  frozen report and upstream file.
- **Not committed:** the artifact is git-ignored; downloaded sources stay in
  the scratchpad.
- **Remote:** nothing is pushed or tagged.
