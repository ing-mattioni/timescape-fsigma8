# Phase 1G-H — Global matter-variance definition and minimal closure

Classification: `RESEARCH_PHASE_WITH_EXPERIMENTAL_RUNTIME` (conditional,
model-internal, `NON_OBSERVATIONAL`). Date: 2026-10-06, revised 2026-10-07
and twice on 2026-10-08.
Base: `main` = `origin/main` = `8d3cdd0533035858c42269cb1dff1a20dcafc7da`
(PR #4 merge, the frozen F/G checkpoint), local branch
`phase-1g-h-global-variance-closure` (first commit: the F/G freeze-status
alignment, `phase1g_fg_freeze_status_successor.md`).
Remote: the session branch `ccr-555e67be-u11yht`, pushed with the owner's
approvals of 2026-10-06 and 2026-10-08 (Sec. 1;
[`phase1g_h_publication_successor.md`](phase1g_h_publication_successor.md));
not merged into `main`. Its remote head is `226e52d` (2026-10-08, P7); the
second delta audit (published on `ccr-ac582de6-vho99i` at `e517028`) and
its remediation are on the local branch and not pushed.
Companions: [`phase1g_h_global_variance_closure_inventory.json`](phase1g_h_global_variance_closure_inventory.json),
[`phase1g_h_global_variance_closure_validation.md`](phase1g_h_global_variance_closure_validation.md),
the independent audit [`phase1g_h_independent_audit.md`](phase1g_h_independent_audit.md),
the remediation record [`phase1g_h_audit_remediation.md`](phase1g_h_audit_remediation.md),
the delta audit [`phase1g_h_delta_audit.md`](phase1g_h_delta_audit.md) and its
remediation record [`phase1g_h_delta_audit_remediation.md`](phase1g_h_delta_audit_remediation.md),
the second delta audit [`phase1g_h_delta_audit_2.md`](phase1g_h_delta_audit_2.md) and its
remediation record [`phase1g_h_delta_audit_2_remediation.md`](phase1g_h_delta_audit_2_remediation.md).

**Revision of 2026-10-07.** An independent audit of the text at `d4d693d`
returned `REJECT` for its closure claims (15 findings, GH-F1 … GH-F15), with
every other area `ACCEPT_WITH_CORRECTIONS`; the numbers reproduced. This
revision applies the owner's decisions D1–D4 of 2026-10-07 and the audit's
corrections. The audited text stays in Git at `d4d693d`; the remediation
record maps every finding to its change.

**Revision of 2026-10-08.** An independent delta audit of the remediated
text at `89cb041` (published at `5c325e1`) returned `REJECT` for the
remaining positive-density common-covariance claim and for completeness
claims, with provenance and numerics `ACCEPT` and every other area
`ACCEPT_WITH_CORRECTIONS`; it resolved 8 of the 15 original findings, found
6 partly resolved and 1 open, and raised six new findings (GH-DF1 …
GH-DF6). This revision applies its corrections; the text it audited stays in
Git at `89cb041`, and the delta-audit remediation record maps every finding
to its change.

**Second revision of 2026-10-08.** A second independent delta audit of the
text at `226e52d` (published at `e517028`) returned
`ACCEPT_WITH_CORRECTIONS`: provenance, science, numerics, implementation and
task compliance `ACCEPT`; governance, tests and documentation
`ACCEPT_WITH_CORRECTIONS`. It found GH-DF1 … GH-DF6 and GH-F3 … GH-F14
resolved and GH-F15 confirmed by the owner, and raised two LOW and four INFO
findings (GH-D2F1 … GH-D2F6), none a scientific blocker. This revision
applies them: publication records, tests, typed records and wording; no
number changes. The text it audited stays in Git at `226e52d`; the second
remediation record maps every finding to its change.
Runtime: `src/timescape_fsigma8/global_variance.py` (experimental).
Evidence: `scripts/phase1g_h_global_variance_closure_numerics.py` (writes the
git-ignored `artifacts/independent/phase1g_h_global_variance_closure.json`
and three figures); single cases: `scripts/phase1g_h_global_variance_case.py`
with the configurations in `scripts/phase1g_h_configs/`.

Cited as [GM] arXiv:2511.17160v2; [W07] arXiv:0709.0732v2; [W09]
arXiv:0909.0749v2; [NW15] arXiv:1410.3470v2; [JLH13] arXiv:1304.6087v2;
[SvdW04] astro-ph/0311260; [EH98] astro-ph/9709112; and the frozen project
records [1G-A] … [1G-G] with their owner-decision and successor records
(Sec. 13). Equations (H1)–(H25) are new to this report unless a primary
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

**Remediation (2026-10-07).** The owner approved the audit remediation with
the recommended choices D1–D4 («Procedi, usa le scelte raccomandate per i
punti 1-4»): D1, the formal tangent statistic as a proposed definition; D2,
seed-indexed void accounting with its scale-separation condition; D3, the
Gaussian pair requalified as a signed surrogate plus a nonnegative lognormal
pair; D4, direct values primary, with post-hoc normalised and reclosure
variants. Local commits only; any push needs a separate approval.

**Publication and confirmation (2026-10-08).** The owner approved pushing
the audit commit and the two remediation commits to the session branch
(«Si, fai push») and confirmed the two push approvals of 2026-10-06
(«Si, confermo», audit finding GH-F15); the record is
`phase1g_h_publication_successor.md`. The delta audit was then published,
with the owner's authorisation, on the branch `phase-1g-h-delta-audit`.

**Delta-audit remediation (2026-10-08).** The owner approved the remediation
plan for the delta audit («Perfetto, procedi»): every new finding is a
correction (no owner decision); local commits only, any push needs a
separate approval.

**Distinction recorded as asked.** Everything below that goes beyond the
approved records is an explicitly named hypothesis (H-A6 … H-A9, the seed
closures, the homogeneity-premise readings). None is promoted to a Timescape
law; the owner decides (Sec. 9).

**Verdict** (revised 2026-10-07 and 2026-10-08).

1. **A — a proposed definition, not a closed one** (Sec. 2; owner decision
   D1). The statistic is the *formal tangent statistic*: the rms of the
   linearly propagated early Gaussian field, i.e. the zero-amplitude tangent
   G(k) of the global-contrast map of a Lagrangian top-hat region around the
   smooth two-phase tracker state, with the smoothing rule
   `G_R(k) = G(k) W(kR)`, on the dust foliation, relative to the global
   volume mean, at the present epoch, with an explicit radius convention
   (preferred: (c), `8 h̄⁻¹ Mpc` of present volume-average proper radius,
   `R_proper·H_D0 = 800 km/s`). It is the analogue of ΛCDM's linear σ8 (the
   growth factor applied to the early field) and reduces to it without voids.
   It is **not** the ensemble-mean response of the true region contrast:
   averaging the derivative of the exact identity (H3) over finite
   small-scale fluctuations differs from the tangent (audit GH-F1), and the
   tangent treats the two-phase state as smooth on the region scale.
2. **The propagator is derived within the tangent model** (Sec. 3). Under the
   regional laws A1–A5 of [1G-C], void autonomy H-A6 and seed-indexed void
   accounting H-A9 (owner decision D2: each bubble's volume belongs to the
   region containing its seed), the propagator of any Lagrangian region is
   `G(k) = (1 − p(k))·D_W + p(k)·D_V` (H9), with `D_W = 0.2306`,
   `D_V = 7.133` for [GM] (f_v0 = 0.737) and `0.3527`, `11.33` for [NW15]
   (f_v0 = 0.627), verified independently. The seed-indexed void volume equals
   the volume of the transported material region only when void radii are
   much smaller than R; at `8 h̄⁻¹ Mpc` the ratio is 0.33 / 0.39 (1G-F median)
   and 1.49 / 1.59 ([W09] radius). The extension of 1G-D's mode structure
   below the super-cell scale therefore holds for the seed-indexed statistic,
   not for the material-domain volume (GH-F2).
3. **One input is missing, and it is decisive** (Sec. 4): the void share
   p(k), defined by `p δ_L(LS) = f_v,LS ε`, i.e. `p = f_v,LS − ∂f_v,L/∂δ_L`
   for the region's void volume fraction (corrected, GH-F3). It is 1G-D's
   void-onset response in another normalisation
   (`VOID_ONSET_RESPONSE = EXTERNAL_CLOSURE_INPUT`). The statistic is affine
   in p with slope `D_V − D_W ≈ 6.9` ([GM]) and `≈ 11.0` ([NW15]).
4. **B — the formal statistic is computed conditionally** (Sec. 5). Given an
   explicit void-share closure, the chain from the declared inputs to the
   number is implemented, convergent and tested. At `8 h̄⁻¹ Mpc`, direct A_s
   normalisation (primary, D4):
   - peak-background-split seed with 1G-D's [W09]-radius seed: **1.121**
     ([GM]) and **1.057** ([NW15]), a formal extrapolation beyond the void
     response's declared validity (H-A8; ε_rms 1.21 / 1.13);
   - the same with the 1G-F median radius as a heuristic seed-scale prior:
     **0.811** and **0.816** (ε_rms 0.77 / 0.74, below the adopted ε = 1
     threshold, with no controlled error estimate of the truncation);
   - the constant-share interval (H15) under H-A7 and the adopted reading
     "rms ≤ 10% at 100 h̄⁻¹ Mpc" of [W09]'s homogeneity premise:
     **[0.261, 0.998]** ([GM]) and **[0.369, 1.162]** ([NW15]). It holds only
     for a void share constant over the spectral support of both windows: a
     pointwise-monotone, scale-dependent share satisfies the same premise and
     gives 7.25 / 10.35 at `8 h̄⁻¹ Mpc` (GH-F4).
   Planck-normalised variants (post-hoc at fixed closure, and the reclosure
   with a rescaled input spectrum) are in Sec. 5.4.
5. **C — not reached** (Sec. 7). A Timescape *prediction* needs a derivation
   of p(k) from void formation consistent with the tracker's f_v(t); the
   ensemble statistic of the true contrast needs, in addition, the joint
   small-scale statistics and a material-boundary transport map; an
   observational comparison needs the dressed light-cone and tracer reduction
   (unchanged firewall).
6. **Supporting results** (Sec. 6): the complete two-phase covariance with
   phase-conditional normalisation and every cross term; 1G-E's formula as
   its special case; and a constructive non-uniqueness of the nonlinear
   hybrid variance at 8 h⁻¹ Mpc. The original Gaussian pair (0.97 against
   0.39) is a signed-carrier surrogate whose wall density is negative with
   conditional probability ≈ 0.45 (GH-F5). Nonnegative lognormal pairs that
   share f_v0, the partition covariance and the latent carrier law still
   differ: law II / law I = 0.92–1.29 across lognormal resolution radii of
   1–4 Mpc and both scenarios. They do not share the conditionally
   normalised wall-density covariance, which in law II is law I's divided by
   m_II² = 2.6–8.2 (delta audit GH-DF1). By the identity (H25) the total is
   fixed by the two-point wall probability P11(r) and the both-walls
   conditional density correlation C_W(r); the pairs differ through C_W,
   i.e. the joint law of geometry and density. The non-uniqueness survives
   within nonnegative density laws at a fixed carrier law, with a smaller
   and construction-dependent size and sign.

Every number here is conditional and model-internal. `SIGMA8_AUTHORIZATION`,
`FSIGMA8_AUTHORIZATION`, `RSD_AUTHORIZATION`, `OBSERVATIONAL_AUTHORIZATION`
and `UNIQUE_TIMESCAPE_PREDICTION` remain `NOT_GRANTED`;
`LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` remains `NOT_DERIVED` (the token
proposals of Sec. 9 are deferred after the audit).

## 2. Which σ8 is being defined (A)

### 2.1 Four objects kept distinct

| Object | Definition used here | Status after 1G-H |
|---|---|---|
| Wall-internal linear σ | Linear contrast relative to the **wall** mean, wall growth in t (A1–A5), [1G-C]; 0.834 / 0.935 at equal mass | unchanged; not a global statistic |
| **Formal tangent statistic** | Zero-amplitude tangent of the contrast relative to the **global** volume mean, Lagrangian top hat, applied to the early field, Sec. 2.2 | proposed (A, D1); computed given p (B) |
| Ensemble-mean response of the true contrast | Cross-propagator `⟨δ_L(k) δ_0*(k)⟩′/P_0(k)` of the actual region contrast | not computed; differs from the tangent at finite small-scale amplitude (GH-F1) |
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
- **Linear: the formal tangent statistic (D1).** Linearise the map from the
  early field to the region contrast (H1) at zero amplitude around the
  smooth two-phase tracker state (regional f_v equal to the global one, walls
  at the global wall density): the tangent `δ_L^(1) = ∫ G_R(k) δ_0(k)` with
  `G_R(k) = G(k) W(kR)`, G the unsmoothed carrier of a Lagrangian point. For
  a Lagrangian top hat the regional average of a linear field is its
  window-weighted Fourier sum, so the smoothing rule is exact for the tangent
  (it does not commute with the nonlinear ratio `M_L/V_L`, which is why it is
  stated as part of the definition). The statistic is

  ```text
  σ²_lin(R) = ∫ dln k Δ²_u(k) G(k, t0)² W²(kR)                               (H10)
  ```

  with `Δ²_u` the photon-normalised matter-era spectrum at unit growth
  ([1G-A] Sec. 6.3, `D/a_photon → 1`). It is the variance of the linearly
  extrapolated field, exactly as σ8 is in ΛCDM (growth factor times early
  field): it does not claim that the physical field is linear at R.
- **Ensemble.** The tangent statistic is a statistic of the early Gaussian
  field: centres uniform in Lagrangian (early photon-normalised) coordinates,
  where that field is statistically homogeneous. Mass- and volume-weighted
  sampling differ only beyond first order and do not enter it; at finite
  amplitude, uniform early coordinates are mass coordinates only to first
  order. The statistic is the **connected** variance `⟨δ_L²⟩ − ⟨δ_L⟩²` of
  the tangent field, whose mean vanishes.
- **What it is not.** The ensemble-mean response of the *true* contrast to a
  long mode at fixed small-scale statistics is, by Gaussian integration by
  parts, the cross-propagator `⟨δ_L(k) δ_0*(k)⟩′/P_0(k)`: the ensemble
  average of the derivative of (H3), with the random coefficients
  `(1 + δ)²/(1 + δ_w)²` and `(1 + δ)²/(1 + ε)²` at their finite small-scale
  values. It differs from the tangent. In the audit's example — f_v = 0.737,
  ε = 0, two equal-mass regions with wall contrasts −1/3 and 1, mass-weighted
  mean of `1/(1 + δ_L)` exactly 1 — the mean derivative `∂δ_L/∂δ_w` is
  0.27468 against the tangent value f_w = 0.263 (evidence
  `ensemble_vs_tangent_example`). Computing that ensemble statistic needs the
  joint small-scale statistics and a material-boundary transport map, which
  are not available; the tangent statistic is therefore the defined object.
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
| **(c) preferred** | `R = (L/h̄)/γ_w0`, L = 8 | the region whose present volume-average proper radius is `R_proper = γ_w0 R = 8/h̄` Mpc, `h̄ = H_D0/100`; equivalently `M = (4π/3)⟨ρ⟩_D0 (8/h̄ Mpc)³` (H24) and `R_proper·H_D0 = 800 km/s` | only global-average quantities on the slice |
| (a) | `R = R_ref (ω_ref/ω_m,eff)^{1/3}` | equal Lagrangian mass to ΛCDM's M8 | a reference model; the comparison convention |
| (b) | `R = L/h_dressed` | wall-comoving length with the dressed h | the underived dressed spatial map |

Convention (c) generalises ΛCDM's definition (`R·H0 = 800 km/s` with the
background's own expansion rate) to a background whose global expansion rate
is the bare H_D0. It is a named, defensible convention, not one selected by
the background (GH-F13). R in the table is photon-comoving; the 800 km/s
identity holds for the present proper radius `γ_w0 R`. Using the dressed h in a length
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
relative to the global void density). Tests: (H2)–(H3) against explicit
mass/volume bookkeeping (10⁻¹²), (H4)–(H5) against central differences (10⁻⁸).

**H-A9, seed-indexed void accounting (new; owner decision D2).** With empty
voids a region's void volume needs an allocation rule: the bubble interiors
carry no dust labels, and a bubble can straddle the boundary of the
transported material region. Here each bubble's volume is assigned to the
region containing its seed's Lagrangian position, which is unambiguous at the
matching epoch, where seeds are much smaller than R. This defines a
seed-indexed statistic. It equals the Riemannian volume of the transported
material ball only up to boundary terms of relative order `r_void/R`. At
`8 h̄⁻¹ Mpc` (convention (c)) the present void radius over the present proper
region radius is 0.326 / 0.390 for the 1G-F median radius and 1.485 / 1.589
for [W09]'s 15 h⁻¹ Mpc ([GM] / [NW15]; evidence `scale_separation`): there is
no scale separation at R8 (audit GH-F2).

### 3.2 Regional evolution in the tracker

**Assumptions.**
- **A1–A5** ([1G-C] and its owner decisions): walls are Einstein–de Sitter
  regions in the common time t, which the wall matter clocks (A5).
- **H-A6, void autonomy (new):** each empty void region expands as Milne,
  `V_v ∝ t³`, independently of the density of the surrounding walls, with no
  wall–void volume transfer (1G-G (G5) with J = 0).
- **H-A9** (above): seed-indexed void accounting.
- Growing modes only (regular growing-mode initial conditions): the wall
  bang-time mode t⁻¹ and decaying void modes are absent.

Then, for any Lagrangian region (its void volume counted by H-A9), the wall
contrast obeys the EdS equation in t and the void-volume perturbation is
frozen:

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
Lagrangian region under A1–A5, H-A6 and H-A9, i.e. for the seed-indexed
tangent statistic; in it the super-cell/sub-cell transition enters only
through the scale dependence of p(k) (Sec. 4). For the volume of the
transported material region below the super-cell scale the extension is not
proved (GH-F2): the boundary response is not encoded in p(k) alone, and the
approved `NOT_DERIVED` readings of 1G-C and 1G-D stand.

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
  ([GM]) and 18.9-fold ([NW15]). The part of the Gaussian early field above
  the cap — 46.4% of it at 8 h̄⁻¹ Mpc for [GM] and 47.9% for [NW15], not the
  whole overdense half — cannot be represented with empty voids and
  universal walls. If exact empty voids and the adopted early field are
  retained, wall-density perturbations are therefore necessary. This does not
  select the complete S1 dynamics of 1G-D; relaxing another premise is an
  alternative (GH-F7). That the capacity radius falls at W09's homogeneity
  scale is recorded as a numerical observation, not interpreted.
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
p(k) δ_L(LS) = f_v,LS ε,   i.e.   p(k) = f_v,LS − ∂f_v,L/∂δ_L(k) |_(matching epoch),
```

with f_v,L the region's void volume fraction, `f_v,L = f_v,LS (1 + δ_L)/(1 + ε)`
from (H3) (corrected after audit GH-F3; the earlier form omitted f_v,LS), is
the single missing input of the tangent statistic. A uniformly compressed
region has p = f_v,LS. With 1G-D's threshold response
`A_v = φ(ν)/(σ_s Φ(−ν))`, `p(k → 0) = f_v,LS (1 + A_v)` when the seed volume
is compressed with its region and `f_v,LS A_v` for the threshold shift
alone; it has the status of 1G-D's void-onset response,
`VOID_ONSET_RESPONSE = EXTERNAL_CLOSURE_INPUT`.

**Monotone class (H-A7, new).** An overdense region has neither a larger void
fraction nor underdense walls: `f_v,LS ≤ p ≤ 1`. The lower end is the
uniformly compressed region (walls and voids both compressed by δ_L); p = 0
(1G-D's pure wall mode) lies just below it, by f_v,LS. H-A7 is an added class
assumption, not a tracker theorem, and it constrains p at k → 0: the top-hat
side lobes of the PBS kernel take p(k) slightly below f_v,LS at large k,
which is negligible for small seeds in the R8 window but is not pointwise
membership.

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
| [SvdW04] factor 1.72 (1G-D alternative) | 11.94 | 0.4049 | 2.643 | 3.36 | 14.30 | 0.2494 | 2.454 | 3.46 |

(Direct A_s normalisation; the Planck-normalised variants are in Sec. 5.4.)
The 1G-F median radius is a heuristic seed-scale prior: 1G-F's finite-density,
finite-mass population is not identified dynamically with the tracker's
initially empty voids (1G-G and the D successor forbid that identification),
and the GD-OD1 mapping and the γ_w0 conversion of its radius are explicit
choices (GH-F8). The [W09]-radius rows use the void response beyond its
declared validity (H-A8, Sec. 4.3).

### 4.3 Linear validity (H-A8, new)

The rms void-volume response in the region is

```text
ε_rms(R) = [(1 + z_LS) f_v,LS]⁻¹ [∫ dln k Δ²_u p(k)² W²(kR)]^{1/2}.                    (H14)
```

1G-D found the void-onset response perturbative only above R*(ε = 1) = 9.9 /
8.6 h⁻¹ Mpc. At 8 h̄⁻¹ Mpc, ε_rms = 1.21 / 1.13 for the [W09]-radius seed
(`VOID_RESPONSE_NONPERTURBATIVE`) and 0.77 / 0.74 for the 1G-F-median seed,
below the adopted ε = 1 threshold. That threshold is a diagnostic: being
below it does not make ε a controlled small parameter with an error bound.
Applying the linear response where ε_rms > 1 is an extension below the
closure's declared validity: **H-A8** states it explicitly, and every
[W09]-seed value carries it. The statistic is then formal (linearly
extrapolated), as σ8 is in ΛCDM, and must not be read as the physical
variance.

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

### 5.1 The formal tangent statistic at 8 h⁻¹ Mpc

Direct A_s normalisation (primary, D4); in brackets the post-hoc output
normalisation at fixed closure (Sec. 5.4, where the reclosure variant is
given too); p0 = p(k → 0); ε_rms (H14) in Secs. 4.2–4.3.

| Closure | [GM] (c) R = 10.104 | [GM] (a) R = 12.570 | [GM] (b) R = 10.954 | [NW15] (c) R = 11.781 | [NW15] (a) R = 12.226 | [NW15] (b) R = 13.115 |
|---|---|---|---|---|---|---|
| unit growth σ_u (G = 1) | 1.1280 | 0.9799 | 1.0719 | 1.0442 | 1.0186 | 0.9710 |
| wall mode, p = 0 | 0.260 (0.252) | 0.226 (0.219) | 0.247 (0.240) | 0.368 (0.357) | 0.359 (0.349) | 0.342 (0.332) |
| monotone lower end, p = f_v,LS | 0.261 (0.253) | 0.227 (0.220) | 0.248 (0.241) | 0.369 (0.358) | 0.360 (0.349) | 0.343 (0.333) |
| **PBS, 1G-F-median seed** | **0.811 (0.787)** | 0.704 (0.684) | 0.770 (0.748) | **0.816 (0.792)** | 0.796 (0.773) | 0.759 (0.737) |
| **PBS, [W09]-radius seed** (H-A8, formal) | **1.121 (1.088)** | 0.975 (0.946) | 1.066 (1.034) | **1.057 (1.026)** | 1.031 (1.000) | 0.983 (0.954) |
| PBS, [SvdW04]-factor seed | 2.643 (2.566) | 2.447 (2.375) | 2.576 (2.500) | 2.454 (2.382) | 2.424 (2.352) | 2.363 (2.293) |
| M3 two-barrier, w = 1 (H22) | 1.340 | — | — | 1.337 | — | — |
| strict flat walls, p = 1 | 8.045 | 6.989 | 7.645 | 11.83 | 11.54 | 11.00 |
| Planck ΛCDM linear σ8 (anchor) | | 0.8111 | | | 0.8111 | |

The two terms of (H9) are driven by the same early mode and add in
amplitude, not in quadrature: their coherence is 1 for a constant share and
≥ 0.99998 for the small PBS seeds (0.90–0.94 for the [SvdW04] seed, whose
window is inside the R8 range). For the [W09]-radius seed at (c) the wall term is
0.231 ([GM]) and the void term 0.890: the void-onset share carries 79% of
the amplitude.

### 5.2 Constant-share interval (H15)

If p is constant over the spectral support of both windows (the R8 and R_hom
top hats), `σ(R) = G(p) σ_u(R)`. The monotone class gives the lower end
(p = f_v,LS). The background's own homogeneity premise, read as "the global
linear rms does not exceed η in the top hat of radius R_hom", gives
`G ≤ η/σ_u(R_hom)` (capped at p = 1), hence

```text
G(f_v,LS) σ_u(R8) ≤ σ_lin(R8) ≤ η σ_u(R8)/σ_u(R_hom).                                  (H15)
```

The premise is an assumption of the background construction, not a derived
bound: [W09] ll. 327–335 ("100 h⁻¹ Mpc or somewhat larger"; cells whose
density has "a standard deviation of order several percent") and ll. 455–458
("a scale above which the variance in density contrasts is bounded at the
10% level"). [GM] l. 602 places the averaging domain "well above the scale
of statistical homogeneity". [W09] speaks of the density fluctuations of
coarse dust cells; reading it as this mass-weighted Lagrangian tangent
statistic, in a top hat of radius R_hom rather than a cell side, with the
bare h, is an additional premise, not a statement of [W09]. Its reading is an
explicit input:

| Reading (same convention as R8) | [GM] (c) interval | p upper | [W09] seed inside? | [NW15] (c) interval | p upper | [W09] seed inside? |
|---|---|---|---|---|---|---|
| **rms ≤ 0.10 at 100** | **[0.261, 0.998]** | 0.095 | no (0.112 at R_hom) | **[0.369, 1.162]** | 0.069 | yes (0.091) |
| rms ≤ 0.10 at 150 | [0.261, 1.704] | 0.185 | yes | [0.369, 2.048] | 0.147 | yes |
| rms ≤ 0.06 at 100 ("several percent") | [0.261, 0.599] | 0.044 | no | [0.369, 0.697] | 0.029 | no |
| 100 as a cell side (sphere radius 62) | [0.261, 0.570] | 0.040 | no | [0.369, 0.641] | 0.024 | no |

At equal mass (a) the first reading gives [0.227, 1.148] ([GM]) and
[0.360, 1.191] ([NW15]). Under the reclosure normalisation of Sec. 5.4 the
upper ends are unchanged at fixed η and the lower ends scale with the factor
([0.220, 1.148] and [0.349, 1.191]); the earlier "Planck-anchored" interval,
the finished interval times the factor ([0.220, 1.114] and [0.349, 1.155]),
changes the premise and is withdrawn (GH-F6). The 1G-F-median seed lies
inside the first two readings for both scenarios; the [W09]-radius seed
violates the first reading mildly for [GM] (0.1125 against 0.10 at
100 h̄⁻¹ Mpc). Within the constant-share class this interval is the strongest
statement of this phase, and its width is the residual dependence on p.

**Scale-dependent shares are not bounded (GH-F4).** The derivation needs p
constant over the spectral support of both windows; "between R8 and R_hom"
in the audited text hid the broad k support of the two top hats. A
counterexample inside H-A7 at every k: `p(k) = f_v,LS` for `k < k_cut` and 1
above, with `k_cut = 0.0660 Mpc⁻¹` ([GM]) or `0.0691 Mpc⁻¹` ([NW15]) chosen
so that the premise rms is 0.0999. At `8 h̄⁻¹ Mpc` the statistic is then
7.246 ([GM]) and 10.35 ([NW15]), 7.3 and 8.9 times the constant-share upper
end (evidence `step_share_counterexample`; the audit found 7.246 and 10.349
with a slightly different k_cut). Such a kernel is a formal object, not a
physical void response. It shows that (H15) bounds constant shares only, and
that a near-constant closure needs its own bound. For the small PBS seeds
the integrated quantity `G_eff/G(0) − 1` of Sec. 5.3 is −0.08% to −0.12%,
but it is a spectrum-weighted average at the target radius: it is not a
pointwise bound on `G(k)/G(0) − 1` over the noncompact support of the top
hat, and it does not bound the premise integral. No accuracy is derived for
the position of these closures relative to the interval (delta audit
GH-DF4).

### 5.3 Radius range and scale dependence

Integrated scale dependence at the target radius, `G_eff/G(0) − 1` with
`G_eff = σ/σ_u` (a spectrum- and window-weighted average, not a pointwise
bound on G(k)/G(0) − 1; GH-DF4), at the radii of conventions (a)–(c):
−0.08% to −0.12% (1G-D [W09]-radius seed), −0.004% to −0.005% (1G-F-median
seed) and −17% to −24% ([SvdW04] seed, whose radius is inside the R8 range;
both scenarios). For the
small seeds σ is therefore G(0)σ_u to better than 0.2% at these radii;
Figure `propagator_scale_dependence.png` shows G(k)/G(0).
Radius scan at convention (c) (direct normalisation):

| L (h̄⁻¹ Mpc) | 6 | 7 | 8 | 9 | 10 | 12 |
|---|---|---|---|---|---|---|
| [GM] monotone lower | 0.310 | 0.283 | 0.261 | 0.242 | 0.226 | 0.199 |
| [GM] PBS [W09] seed | 1.332 | 1.217 | 1.121 | 1.041 | 0.971 | 0.858 |
| [NW15] monotone lower | 0.444 | 0.403 | 0.369 | 0.340 | 0.316 | 0.277 |
| [NW15] PBS [W09] seed | 1.270 | 1.153 | 1.057 | 0.976 | 0.906 | 0.793 |

**Error budget, kept separate.** Numerical: quadrature self-convergence
≤ 10⁻⁶ and a refined grid (k from 10⁻⁷ to 10³ Mpc⁻¹, 16001 points) agrees to
< 2×10⁻⁶; the growth factors carry ≤ 10⁻¹² identity errors. Parameters: the
two scenarios differ by f_v0 and H0 and are never averaged. Closure: the
dominant uncertainty, quantified by p (Secs. 4.2, 5.2). Statistical: none
(no data). The ranges above are hypothesis scans, not confidence intervals.

### 5.4 Amplitude and normalisation

- **Inputs.** A_s = 2.100×10⁻⁹, n_s = 0.9649, k_p = 0.05 Mpc⁻¹ and
  f_b = ω_b/ω_ref = 0.02237/0.14309694 (ω_ref = 0.315 × 0.674², printed
  0.14310; Planck 2018, TT,TE,EE+lowE+lensing), held fixed when the density
  changes; the EH98 **zero-baryon-oscillation (no-wiggle)** transfer — the T0
  form with the baryon shape suppression α_Γ and the sound-horizon term,
  EH98 Eqs. (26) and (28)–(31), as implemented by `lagrangian_sigma` (1G-B),
  not the literal zero-baryon transfer, which gives different unit variances
  (≈ 1.500 / 1.382 against 1.128 / 1.044; GH-F12) — at the per-photon density
  `ω_m,eff = ½(1 − f_v0)(2 + f_v0)(H_D0/100)²` = 0.12048 ([GM]) and 0.13094
  ([NW15]) ([1G-A] Sec. 6.2); T_cmb = 2.7255 K; matter-era Poisson
  normalisation `Δ² = (4/25) A_s (k/k_p)^{n_s−1} (k/aH)⁴ T²`; matching at
  z_LS = 1090. No late-time ΛCDM growth enters the spectrum.
- **A_s is an import, not a Timescape fit.** [NW15] state that they treat
  A_s "as a nuisance parameter that we cannot constrain", with τ degenerate
  (l. 1422–1428). The Planck A_s is a ΛCDM fit; this is recorded as
  `PROVISIONAL_MODEL_IMPORT`.
- **Normalisation (owner decision D4).** The direct values are primary. Two
  Planck-normalised variants are reported beside them; neither is a
  verified transfer recalibration (GH-F6):
  - *post-hoc*: the finished value times
    `0.8111/σ_EH98,Planck = 0.8111/0.835689 = 0.970577`, the ratio of the
    Planck σ8 to the EH98 value at the Planck parameters (BAO wiggles and the
    0.06 eV neutrinos are missing from EH98): an empirical output
    normalisation at fixed closure;
  - *reclosure*: the input spectrum rescaled by the factor squared, so that
    the PBS threshold share is recomputed (`p − f_v,LS ∝ 1/σ_s`).

  For a constant share the two agree exactly; for the PBS closures they
  differ by 1.7–2.3% (direct / post-hoc / reclosure; evidence
  `pbs_reclosure_under_spectrum_rescaling`):

  | Closure | [GM] (c) | [NW15] (c) | [GM] (a) | [NW15] (a) |
  |---|---|---|---|---|
  | PBS, [W09]-radius seed (H-A8) | 1.121 / 1.088 / 1.114 | 1.057 / 1.026 / 1.046 | 0.975 / 0.946 / 0.968 | 1.031 / 1.000 / 1.020 |
  | PBS, 1G-F median seed | 0.811 / 0.787 / 0.803 | 0.816 / 0.792 / 0.805 | 0.704 / 0.684 / 0.698 | 0.796 / 0.773 / 0.785 |
  | constant share, p = f_v,LS | 0.261 / 0.253 / 0.253 | 0.369 / 0.358 / 0.358 | 0.227 / 0.220 / 0.220 | 0.360 / 0.349 / 0.349 |

  The factor cancels the late ΛCDM growth only for a common
  scale-independent growth, which the massive-neutrino Boltzmann reference
  does not establish; no Timescape value is fitted to it.
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

Planck's σ8 is, by construction, the formal tangent statistic of Sec. 2.2
for a flat ΛCDM background, at the Planck mass M8 (convention (a)), with the
same window, early import and linear order. The Timescape values at (a) are
0.975 / 1.031 ([W09]-radius seed, H-A8) and 0.704 / 0.796 (1G-F-median seed)
direct; post-hoc normalised 0.946 / 1.000 and 0.684 / 0.773; reclosure
0.968 / 1.020 and 0.698 / 0.785; the constant-share interval is
[0.227, 1.148] / [0.360, 1.191] direct. ΛCDM gives 0.8111. These compare like
with like as *model* quantities, under the stated normalisation. They are not observational: an observational σ8 or S8 is
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

**Empty voids (added 2026-10-08, delta audit GH-DF1).** With x = 0 and the
wall density written `ψ = 1 + δ_w`, normalised on the walls
(`E[ψ | wall] = 1`), the global contrast is `δ = χ_w ψ/f_w − 1`, so

```text
1 + ξ_δ(r) = P11(r) C_W(r) / f_w²,   P11(r) = P(both points in walls),
C_W(r) = E[ψ1 ψ2 | both points in walls],                                             (H25)
```

and the ball variance is the pair average of ξ_δ. (H25) is (H18) at x = 0
written in other variables. The evidence compares the two on the same kernel
arrays to 10⁻¹²: a consistency check of the (H18) assembly, not of the
kernels, which the tests check by sampling (second delta audit GH-D2F2). Two laws
with the same P11(r) and the same C_W(r) have the same variance; a
difference at fixed f_v0 and P11 is a difference of the both-walls
conditional density correlation, i.e. of the joint law of geometry and
density.

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

### 6.3 A constructive non-uniqueness (revised 2026-10-07 and 2026-10-08)

Two pairs of joint laws are built. Within each pair the two laws share
f_v0, the partition covariance P11(r) (voids are `{g < c}`, `Φ(c) = f_v0`,
g a unit Gaussian mask field; for law II g is the wall carrier smoothed with
a Gaussian of width ℓ, calibrated so that the partition rms in the ball
equals the 1G-E/F reference value, and law I uses an independent field with
the same covariance) and the law of the wall carrier as an unconditional
field. They differ in how the walls sample the carrier: law I, mask
independent of the wall field; law II, voids where the same field is low
(the "same primordial field" case). By (H25) the difference is entirely a
difference of C_W(r).

**Signed Gaussian pair (requalified, D3).** The wall field is the 1G-E/F
wall-internal linear field (growth D_wall(t0), photon-frame compression
s = D_wall, Planck normalised), recentred on the walls:
`1 + δ_w = 1 + w − μ` with `μ = E[w | wall]` (0 for law I; 5.00 /
3.79 for law II). These are realisable *signed* carrier and
mask laws, not matter-density laws: the wall density is negative with
conditional probability 0.448 / 0.443 ([GM] I / II) and
0.455 / 0.453 ([NW15]) (GH-F5). The shared covariance is that of
the unconditional carrier; the phase-conditioned (masked) wall covariance
differs between I and II by construction. All moments follow from orthant
integrals of the bivariate normal (H21), coded in
`bivariate_normal_orthant_moments` with an explicit accuracy contract and
verified against the bivariate CDF (10⁻¹⁰), analytic special cases (10⁻¹²)
and direct 4-variate Monte Carlo:

| Convention (b) | ℓ (Mpc) | Law I σ_part / wall / cross / **total** | Law II σ_part / wall / cross / **total** | ⟨C_W − 1⟩ I / II |
|---|---|---|---|---|
| [GM], R = 10.954 Mpc | 0.292 | 0.326 / 0.915 / 0 / **0.971** | 0.326 / 0.106 / +0.036 / **0.393** | 0.756 / 0.043 |
| [NW15], R = 13.115 Mpc | 0.599 | 0.304 / 0.930 / 0 / **0.978** | 0.304 / 0.160 / +0.050 / **0.409** | 0.791 / 0.069 |

⟨C_W − 1⟩ is the both-walls conditional covariance averaged with the pair
weight P11 over the ball. In law II the drop comes from the masked wall
auto-variance, which the phase-conditional recentring reduces (the walls
sit where the carrier is high); the integrated wall–partition cross term is
positive, not a cancelling negative term (the audited text described a
cancellation).

**Nonnegative lognormal pairs (D3; narrowed 2026-10-08, GH-DF1).** The latent
Gaussian field is the same carrier smoothed with a Gaussian of radius r_s,
`a = λ s`; the wall density is `ψ = e^a / E[e^a | wall] ≥ 0`, normalised on
the walls. Law II takes the signed pair's mask, law I an independent mask
with the same covariance. Both laws share f_v0, P11(r), the latent carrier
law (covariance `λ² ξ_s`; equivalently the unconditionally normalised
carrier `e^a / E[e^a]`, covariance `exp(λ² ξ_s) − 1`) and the convention
`E[ψ | wall] = 1`. They do **not** share the conditionally normalised wall
density itself: in law II its normaliser exceeds law I's by
`m_II = Q(c − κ0)/f_w` (κ0 the one-point covariance of mask and latent
field), so its unconditional covariance is law I's divided by m_II². The
2026-10-07 text listed that covariance among the shared constraints; this
was wrong (delta audit GH-DF1). Two choices are free and declared: the
latent smoothing radius r_s (1, 2, 4 Mpc; without smoothing the ball
integrals are not resolved near r = 0) and the calibration of λ, which sets
the ball variance of the unconditionally normalised carrier equal to the
signed carrier's (0.701 / 0.734). The moments follow from exponential
tilting of the Gaussian vector `(g1, g2, a1, a2)` and two-threshold orthant
probabilities (`bivariate_normal_orthant_probability`), checked by
4-variate Monte Carlo (including the shared carrier covariance and the
m_II⁻² ratio):

| Scenario, R as above | r_s (Mpc) | latent point variance | density point variance | m_II | law I wall / total | law II wall / cross / total | ⟨C_W − 1⟩ I / II | II / I |
|---|---|---|---|---|---|---|---|---|
| [GM] | 1 | 2.68 | 13.64 | 2.87 | 0.933 / 0.989 | 0.773 / +0.330 / 1.017 | 0.787 / 0.838 | 1.03 |
| [GM] | 2 | 1.59 | 3.93 | 2.14 | 0.912 / 0.969 | 0.903 / +0.399 / 1.149 | 0.751 / 1.097 | 1.19 |
| [GM] | 4 | 0.97 | 1.63 | 1.62 | 0.896 / 0.953 | 0.984 / +0.446 / 1.233 | 0.725 / 1.278 | 1.29 |
| [NW15] | 1 | 3.35 | 27.59 | 2.47 | 0.958 / 1.005 | 0.712 / +0.255 / 0.924 | 0.841 / 0.698 | 0.92 |
| [NW15] | 2 | 1.99 | 6.33 | 2.10 | 0.933 / 0.981 | 0.809 / +0.314 / 1.030 | 0.798 / 0.887 | 1.05 |
| [NW15] | 4 | 1.17 | 2.23 | 1.67 | 0.915 / 0.964 | 0.919 / +0.374 / 1.145 | 0.766 / 1.116 | 1.19 |

The signed pair is the λ → 0 limit of this construction on the unsmoothed
carrier (`e^a/E[e^a | wall] = 1 + a − E[a | wall] + O(a²)`): its wall
moments over λ² and cross moments over λ approach the signed ones, within
0.93% / 0.64% at a latent variance of 10⁻⁴. This is a local numerical check
at one small amplitude with an empirical 5% gate, not an asymptotic theorem.

**Radial quadrature (corrected 2026-10-08).** The ball pair integrals now
include the first radial panel `[0, 2R/480]`, which the 2026-10-07 grid
omitted; the integrand vanishes at r = 0, where the pair density has a
double zero. On 1440 intervals, refinement against 720 changes no rms by more
than 1.0×10⁻⁶ (an evidence gate). The small signed law-II wall moments move
by 1.3×10⁻³ / 6.6×10⁻⁴ relative, to 7.8252×10⁻⁴ / 3.5532×10⁻³ (the delta
audit's values); no value printed in this report changes.

**Reading.** Within each pair f_v0, P11(r) and the carrier law are fixed and
the ball variance differs; by (H25) the difference lies entirely in the
both-walls conditional density correlation C_W(r). Within nonnegative laws
the difference is −8% to +29% across r_s = 1–4 Mpc and both scenarios, and
its sign depends on the construction (r_s and the λ calibration are free
choices); the factor 2.5 of the signed pair is a property of that surrogate
(its negative-density fraction and recentring), not of the constraints. The
result shows that a volume fraction, a partition covariance (or a size
distribution) and a wall carrier spectrum do **not** fix the nonlinear
variance at 8 h⁻¹ Mpc: the joint law of geometry and density, through C_W,
is a further, independent input. In the latent-Gaussian constructions of
this section that input is the mask–carrier dependence, the covariances κ0
and κ(r) of mask and latent field: once it is specified, f_v0, P11(r) and
the carrier law fix C_W(r) and the variance, and mask–carrier independence
(law I, the E3 case of 1G-E) fixes them with no further input (second delta
audit GH-D2F6). It does not show non-uniqueness at a fixed
conditionally normalised wall-density covariance, and at fixed P11 and C_W
the variance is unique by (H25). Neither pair solves the gravitational
dynamics; this is a kinematic counterexample about the statistical inputs,
not a no-go result for the Einstein or Timescape equations.

## 7. Closure assessment

| Result | Status | Why |
|---|---|---|
| **A — definition** | **proposed** (D1) | Sec. 2: the formal tangent statistic, with its smoothing rule, field, frame, foliation, mean, time, epoch, window, scale convention ((c) preferred), h, linear order and ensemble; FLRW limit verified. The ensemble-mean response of the true contrast is not computed (GH-F1) |
| **B — conditional calculation** | **closed for the formal statistic, given one external closure and H-A9** | Sec. 3 derives the propagator within the tangent model; Sec. 4 identifies p(k); with an explicit closure the chain is implemented, converged and tested; the constant-share interval (H15) bounds constant shares only |
| **C — Timescape prediction** | **not reached** | p(k) is not derived from the theory; the ensemble and material-domain statistics also need the joint small-scale law and a transport map |
| **C — observational interpretation** | **not reached** | firewall: dressed light-cone, tracer, selection and inference |

**The missing object, precisely.** For the formal tangent statistic, the
response kernel p(k) defined by `p δ_L(LS) = f_v,LS ε`, i.e.
`p = f_v,LS − ∂f_v,L/∂δ_L(k)` at the matching epoch in the tracker ensemble;
`p(k → 0) = f_v,LS (1 + A_v)` with 1G-D's threshold response A_v when the
seed volume is compressed with its region. For the ensemble statistic of the
true contrast and for the material-domain volume below the super-cell scale,
p alone is not enough (GH-F1, GH-F2).

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

*Written before the independent audit of 2026-10-07 and brought up to date
with the delta audit of 2026-10-08 (GH-DF3): every item states the current
reading. The two audits are the authoritative reviews; their findings and
the corrections are mapped in the two remediation records.*

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
  In the nonlinear covariance, law II changes the masked wall auto-variance,
  with a positive integrated wall–partition cross term (Sec. 6.3); double
  counting is not the mechanism (GH-DE5).
- **Circular normalisation.** The post-hoc factor is an empirical output
  normalisation at fixed closure; rescaling the input spectrum and
  recomputing the PBS share is a distinct variant; neither is a verified
  transfer recalibration (Sec. 5.4; GH-DE2). The interval uses an adopted
  reading of [W09]'s homogeneity premise, not σ8. Neither calibrates to the
  quantity reported.
- **Undeclared dependences found and declared:** z_LS = 1090 and the neglect
  of radiation at last scattering (it rescales δ_L(LS) and σ_s alike, so ε is
  unchanged and the wall term changes through 1 − p; the earlier estimate
  "about 0.4%" had no reproducible control and is withdrawn: the correction
  is not quantified here); f_v,LS inherits the
  tracker fit (f_v0, H0); the single seed scale and Gaussian threshold; the
  γ_w0 ambiguity in converting the 1G-F radius (a 37% change of R_s changes
  p by roughly 10%); H-A6 ignores wall–void boundary coupling; S1 goes beyond
  [GM]'s flat walls; the flat-wall cap requires wall-density freedom if
  exact empty voids and the early Gaussian field are kept, but it does not
  select the whole of S1 (Sec. 3.3; GH-DE3); H-A8 at R8.
- **Numbers that could be wrong.** The GT law-II collapse of the wall term was
  checked analytically by a linear-response estimate and numerically by
  direct 4-variate Monte Carlo of the covariance kernels. That is correct for
  the signed surrogate; the audit showed that the surrogate has negative
  densities, and the nonnegative pairs of Sec. 6.3 do not collapse. Those
  pairs fix the carrier law, not the conditionally normalised wall-density
  covariance (GH-DF1); the ball integrals now include the first radial
  panel.

## 9. Decisions requested from the owner

Each is separate. Status after the independent audit and the owner's
remediation decisions D1–D4 of 2026-10-07, and after the delta audit and
the second delta audit of 2026-10-08 (whose recommendations agree with the
revised ones below), is given under each item.

1. **H-OD1, definition and radius convention.**
   - [ ] Adopt the definition of Sec. 2 as the project's σ8-analogue, with
     convention **(c)** (`8 h̄⁻¹ Mpc`, `R_proper·H_D0 = 800 km/s`) as primary
     and (a) as the comparison convention at fixed mass. *(Recommended before
     the audit; see the status line.)*
   - [ ] As above, with (a) primary.
   - [ ] Keep the definition as a research proposal only.
   - *Status (2026-10-07):* D1 narrows the definition to the formal tangent
     statistic and keeps it a proposal; adoption as the project's
     σ8-analogue is not decided. Revised recommendation, with the audit: keep
     it a proposal at least until a delta audit. Convention (c) stays the
     preferred named convention, (a) the fixed-mass comparison.
   - *Status (2026-10-08):* open; the delta audit recommends keeping the
     formal tangent a named research proposal.
   - *Status (2026-10-08, second delta audit):* open; that audit concurs,
     with (c) preferred and (a) as the fixed-mass comparison.
2. **H-OD2, the void-share closure for a reference value.**
   - [ ] **β:** PBS seed with the 1G-F volume-weighted median radius:
     0.811 / 0.816 at (c) (0.787 / 0.792 post-hoc); below the adopted ε = 1
     threshold at R8, without a controlled error estimate; inside the [W09]
     premise for both scenarios. The 1G-F median is a heuristic seed-scale
     prior; its weak points are 1G-F's conditional status, the missing
     dynamical identification with empty tracker voids and the single-scale
     idealisation.
   - [ ] **α:** PBS seed with the [W09] 15 h⁻¹ Mpc radius (the 1G-D primary):
     1.121 / 1.057 at (c); non-perturbative at R8 (ε_rms 1.21 / 1.13); mildly
     outside the 10%-at-100 premise for [GM].
   - [ ] **γ:** no reference value; report only the constant-share interval
     (H15) with the 10%-at-100 reading: [0.261, 0.998] / [0.369, 1.162] at (c).
   - *Status (2026-10-07):* open. Revised recommendation, with the audit:
     select no physical reference value yet; if one is used experimentally,
     β is a heuristic prior, α a formal extrapolation (H-A8) and γ a
     constant-share statement.
   - *Status (2026-10-08):* open; the delta audit recommends no physical
     reference value yet.
   - *Status (2026-10-08, second delta audit):* open; that audit concurs (the
     median seed a heuristic prior below ε = 1, the [W09] seed a
     nonperturbative formal extrapolation, the interval valid only in its
     class).
3. **H-OD3, status tokens** (proposals; the registry rules matter).
   - [ ] Add two tokens through the existing addition mechanism (no validator
     change): `GLOBAL_MEAN_LINEAR_STATISTIC_DEFINITION =
     DERIVED_FROM_VERIFIED_DEFINITIONS` and
     `GLOBAL_MEAN_LINEAR_STATISTIC_COMPUTATION =
     DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` (A1–A5, H-A6, H-A7, H-A8 and
     the closure of H-OD2); keep `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC =
     NOT_DERIVED`, since no closure is selected by the theory.
     *(Recommended before the audit; see the status line.)*
   - [ ] Change `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` to
     `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`. The 1F-C-R validator accepts
     only one registered change per added token, and this token already has
     one (the 2026-10-02 D successor). A second, chained change needs an
     approved validator extension; R2-N4 (record order is not enforced)
     becomes relevant then.
   - *Status (2026-10-07):* open. Revised recommendation, with the audit:
     defer both options and keep every token unchanged at least until a
     delta audit of this remediation.
   - *Status (2026-10-08):* open; the delta audit recommends deferring token
     promotion and keeping every token and authorisation unchanged.
   - *Status (2026-10-08, second delta audit):* open; that audit recommends no
     token change ((H25) and the C_W reading belong in this report, not in a
     token).
4. **H-OD4, the runtime.**
   - [ ] Keep `global_variance.py` experimental until an independent audit.
     *(Recommended.)*
   - [ ] Promote it to a package runtime.
   - *Status (2026-10-07):* open; recommendation unchanged. The record and
     orthant contracts were hardened (GH-F9, GH-F10).
   - *Status (2026-10-08):* open; the records now recompute their results
     from their inputs (GH-DF2) and the defensive checks have their own tests
     (GH-DF5).
   - *Status (2026-10-08, second delta audit):* open; that audit recommends
     keeping the runtime experimental and running the Windows gate before
     any promotion. Its test gaps are closed (GH-D2F2) and a float result
     must now be stored as a float (GH-D2F4).
5. **H-OD5, publication.** Push, pull request, merge, audit, freeze or tag of
   this phase: none is authorised by the task; each needs a separate
   decision.
   - *Push decided* (owner, 2026-10-06): the commits are on the session
     branch `ccr-555e67be-u11yht`.
   - *Audit performed* (2026-10-07): `phase1g_h_independent_audit.md`,
     `REJECT` of the closure claims; published by the owner on the branch
     `phase-1g-h-independent-audit` (`816dd00`). The remediation of
     2026-10-07 was committed on top of it.
   - *Push decided* (owner, 2026-10-08): the audit commit and the two
     remediation commits on the session branch (`89cb041`); the two approvals
     of 2026-10-06 confirmed (GH-F15); see
     `phase1g_h_publication_successor.md`.
   - *Delta audit performed* (2026-10-08): `phase1g_h_delta_audit.md`,
     `REJECT` of the remaining common-covariance and completeness claims;
     published with the owner's authorisation on the branch
     `phase-1g-h-delta-audit` (`5c325e1`). The delta-audit remediation was
     committed on top of it.
   - *Push decided* (owner, 2026-10-08): the delta-audit commit and the two
     commits of its remediation on the session branch (`226e52d`, P7 of the
     publication successor).
   - *Second delta audit performed* (2026-10-08): `phase1g_h_delta_audit_2.md`,
     `ACCEPT_WITH_CORRECTIONS`, no scientific blocker; the owner confirmed
     the GH-F15 approvals directly to its auditor (P8); published on the
     owner's instruction on the branch `ccr-ac582de6-vho99i` (`e517028`, P9).
     Its remediation is committed locally on top of it.
   - Open: the push of the second delta audit and its remediation; the
     owner's Windows gate (CPython 3.14.3 / 3.11.9, never run on a 1G-H
     tree); an optional cross-family check of Sec. 6 (the second delta audit
     shares the author's model family); pull request, merge, freeze and tag.

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
    `cauchy_schwarz_total_rms_interval` (H17)–(H20);
  - `bivariate_normal_orthant_probability`, `bivariate_normal_orthant_moments`
    (H21), refined to an explicit absolute tolerance and refused beyond
    `ORTHANT_MAX_NODES` nodes per panel (GH-F10);
  - `two_barrier_void_mass_fraction`, `two_barrier_global_linear_bias` (H22).
  - Every exported record re-validates its fields in `__post_init__`
    (finite values, variant consistency, tracker identities, interval
    identities; `RECORD_IDENTITY_RTOL`), so a replaced field that breaks an
    invariant is refused (GH-F9), and recomputes each result and diagnostic
    from its stored inputs with the factory's own function, so a replaced
    input that no longer reproduces the stored results is refused (GH-DF2).
    A float result must be stored as a float, and validated scalar inputs
    are stored as floats, so the records serialise as strict JSON (GH-D2F4).
    Construction therefore costs about twice the computation.
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

  It takes about 50–80 s, writes the JSON artifact (strict JSON, no
  non-finite numbers) and three figures (`sigma_vs_void_share.png`,
  `radius_scan.png`, `propagator_scale_dependence.png`), and exits nonzero
  if one of its 36 declared gates fails. Since the remediation it also
  writes `ensemble_vs_tangent_example`, `scale_separation`,
  `flat_wall_cap_exceedance`, `step_share_counterexample`,
  `pbs_reclosure_under_spectrum_rescaling`, the negative-density
  probabilities and the `nonnegative_lognormal_pair`; since the delta-audit
  remediation, the law-II normaliser ratios, ⟨C_W − 1⟩, the (H25) check and
  the radial refinement of the constructive pairs.

## 11. Verification summary

Details, commands, versions and logs are in the validation record.

- **Phase tests:** `tests/test_phase1g_h_global_variance.py`, 49 tests
  (28 originally; seven added for GH-F1, F3, F4, F5, F6, F10 and F11 and the
  tamper test extended for GH-F9; seven added for GH-DF1, DF2 and DF5, with
  the tamper test now requiring each invariant's own message; seven added
  for GH-D2F2 and GH-D2F4: the pair-weighted C_W and the m_II⁻² read-outs, a
  Monte Carlo of C_W and m_II with ψ normalised by the sample wall mean, the
  Simpson error ratio of the radial estimator, the binding tolerance and two
  record identities, the pinned gate thresholds, and float-typed results),
  covering the categories asked for. They check dimensions and k/R units
  (photon-comoving Mpc), window and mass normalisation, and the homogeneous,
  single-phase and EdS limits. They check real-space against Fourier (2×10⁻⁵)
  and A_s scaling. They check positive-semidefiniteness and cross-term
  bounds, and recover 1G-D, 1G-E and 1G-F numbers. They check perturbative
  convergence of the exact spherical region, quadrature and k-tail
  convergence, and the refusal of incomplete or out-of-class configurations.
- **Evidence gates:** 36 declared gates, all passing (1G-D reproduction, A_s
  scaling, refined quadrature, the 1G-E reproduction within its propagated
  rounding budget (GH-F11), orthant CDF and analytic cases, two-barrier
  finite differences, the step-kernel premise, the constant-share reclosure
  identity, the lognormal calibration and its linear limit, and, since
  2026-10-08, the radial refinement of the constructive pairs and the (H25)
  consistency check of the (H18) assembly, a numerics gate since the second
  delta audit).
- **Governance:** the tolerance audit reports 0 comparisons without explicit
  tolerances; the 1F-C-R validator reports `PASS`.
- **Full suites** (warnings as errors) on CPython 3.13.16 and 3.11.17 (Linux):
  see the validation record (original tree) and the two remediation records
  (remediated trees). The Windows 3.14.3 / 3.11.9 gate was not run in these
  sessions; its commands are listed in the validation record.

## 12. Preservation, status and limitations

- **Unchanged:** every frozen report, inventory, audit, evidence file and
  tag; every existing package module, test and status token; the
  independent audit's files. Outside the 1G-H files, the phase touched
  README.md and CLAUDE.md (current-status text) and, in the remediation, its
  own F/G freeze-status successor record (GH-F14). The files of the delta
  audit and of the second delta audit are unchanged as well.
- **F/G freeze.** The F/G freeze attests its own checkpoint. It does not
  derive σ8; 1G-H builds on it without editing it. R2-N4 is relevant only if
  H-OD3's second option is chosen.
- **No D v2.** No `phase-1g-d-separate-universe-growth-v2` tag or branch is
  created; the approved D successor is part of the F/G checkpoint.
- **Limitations:** the statistic is the formal tangent, not the ensemble
  response of the true contrast (D1); seed-indexed void accounting H-A9 with
  no scale separation at R8 (D2); H-A6 (no wall–void boundary coupling); a
  single-scale Gaussian-threshold seed; the 1G-F radius as a heuristic
  prior and its conversion ambiguity; the void response beyond its validity
  for the [W09] seed (H-A8); matching at z = 1090 without radiation (not
  quantified); the EH98 no-wiggle transfer; A_s from a ΛCDM fit and an
  empirical Planck normalisation (D4); empty voids in the propagator
  (finite-density voids are treated only in the covariance and the M3
  alternative); the lognormal pairs' resolution radius and λ calibration
  are free construction choices, and the pairs fix the carrier law, not the
  conditionally normalised wall-density covariance (GH-DF1); the integrated
  scale dependence is not a pointwise bound (GH-DF4); no time-dependent
  mergers or mass transfer (1G-G); and nothing observational.

## 13. Sources, versions and equation numbering

| Source | Version and file | SHA-256 | Used |
|---|---|---|---|
| [GM] | arXiv:2511.17160v2, `main.tex` | `f9cadfa03ecc9a74b0a8f432ae4b13422daeb219f253756bcd877b4b75077c59` (as 1G-A) | (5.1)–(5.7), text p. 25 (γ_w, 1+z, ⟨ρ⟩ normalisation), Sec. 3 (averaging), l. 602, l. 620 |
| [W09] | arXiv:0909.0749v2, `observe.tex` | `2b0324d127440e9a053a7cb37102d7655cca228a63cd2222843e879989b4b531` (as 1G-A) | l. 277 (void size), ll. 327–335, 455–458 (homogeneity), (Q1), ll. 1807–1811 (f_vi) |
| [W07] | arXiv:0709.0732v2, `solution.tex` | `221662c987e454729ef8202c87fa697c5882b5b7daaecdedb50a7cba8ffe6cd8` | regional EdS/Milne laws (via 1G-C) |
| [NW15] | arXiv:1410.3470v2, `cmb1.tex` | `5688c9ac7123a5c2ef3508e39cb3134c2fe9e3d5e56996a4d4a4d101d7b74673` | A_s a nuisance parameter (ll. 1422–1428); f_v0 = 0.627, H0 ≈ 61 |
| [JLH13] | arXiv:1304.6087v2, `voids_mnras.tex` | `cf6fc77a31b395138ac3a027d008698556534e81cfb27c39853d3a99c7b07c4e` | Eq. (2) (linear variance); (A8)–(A12) via 1G-F |
| [SvdW04] | astro-ph/0311260v1, `voids.tex` | e-print tarball `4b7ad599f54b3199e0448df1c2eecf4e724401e9ffda7b0f50a3efe7fecdb79b` | Eqs. (1)–(3), Eq. (3) the void mass fraction |
| [EH98] | astro-ph/9709112v1, `trans.tex` | `5f2ac6b413df8b738c95f6650152b7e82d7c36f6d9b3a618da540e9739dce17f` | (26), (28)–(31) through `lagrangian_sigma` |

Full hashes since the remediation: four abbreviated suffixes of the audited
text were wrong (GH-F13); the full values were always those of the inventory.

Equation numbers are those of the e-print LaTeX sources (sequential display
numbering, as reconstructed in 1G-A for [GM]); the journal HTML may differ.
Downloads stayed in the session scratchpad; no upstream code was copied.
(H1)–(H25) are this report's: (H1)–(H5), (H13), (H17)–(H20), (H23) and
(H25) follow from the definitions with [GM] Sec. 3 and (5.4)–(5.6). (H6)–(H9) add
A1–A5, H-A6 and H-A9 (the tangent model). (H12) is 1G-D's Sec. 7 response with the compression term
and window added here. (H22) applies [SvdW04] Eq. (3) to conditional walks.
None of them is attributed to a source as already derived.
