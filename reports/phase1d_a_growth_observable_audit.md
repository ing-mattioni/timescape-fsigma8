# Phase 1D-A — Growth and observable audit for the Timescape CGI perturbation variables

Date (UTC): 2026-07-17

Branch: `phase-1c-perturbations`

Repository checkpoint: HEAD `c6ea04f48ecfbe0ea5477fa137fb9ab39555c72d`
(documentation-only descendant, approved by the user at preflight, of the
frozen scientific checkpoint `9ec3bcc36bd9d7cc5defe4305c63d44d201a9971`
= tag `phase-1c-b2-barotropic-v1`).

Scientific specification: Galoppo & Mourier,
[arXiv:2511.17160v2](https://arxiv.org/abs/2511.17160), JCAP 02 (2026) 066
— cited as [GM]. Wiltshire, arXiv:0909.0749 — cited as [W09].

Machine-readable companion: `reports/phase1d_a_observable_inventory.json`.

---

## 1. Scope and preservation statement

This phase is an **equation-level and observable-definition audit only**. It
derives what the Timescape CGI perturbation variables mean observationally
and under which mathematical conditions growth rates, σ_R, σ_8, and fσ8 can
be defined. It implements nothing: no growth package, no power-spectrum
integrator, no σ_8 computation, no fσ8 pipeline, no likelihood, no fit, no
data comparison. The only tracked deliverables are this report and its JSON
companion. All symbolic and numerical corroborations were executed in
memory or under the ignored session scratchpad; the frozen Phase 1B
background package and Phase 1C-B1/B2 perturbation packages were imported
strictly read-only, and the generated B1/B2 artifacts were only read.

Preflight verification (performed before any work):

| check | result |
|---|---|
| branch | `phase-1c-perturbations` ✓ |
| HEAD | `c6ea04f` (≠ `9ec3bcc`) — deviation reported; user approved proceeding |
| tag `phase-1c-b2-barotropic-v1` → `9ec3bcc` = HEAD~1 | ✓ (HEAD is its descendant; diff = CLAUDE.md, README.md, tests/test_b2_artifact_schema.py only) |
| working tree and index clean | ✓ |
| upstream clone HEAD | `590c6fd5332acb15f5683ebf392a0d7ce54983c5`, clean ✓ |
| `ACPT_Timescape.ipynb` SHA-256 | `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a` ✓ |

Every unresolved Phase 1C label is preserved verbatim: D3 branch
`printed_4_15` / `derived_4_10` (neither called correct, preferred,
canonical, physical, recommended, or default); tilt `unrescaled_V` /
`rescaled_Vtilde`; rate units `upstream_unconverted` /
`lcdm_to_timescape_converted`; epoch `upstream_0p218_gyr` / `dressed_z20`;
wavenumber `upstream_timescape_k` / `paper_lcdm_hubble_k`. The D2-corrupted
sound speed remains forensic-only and is used nowhere in this audit's
observable definitions.

## 2. Source and provenance inventory

Local primary sources (verbatim inspection):

| source | identity | role |
|---|---|---|
| arXiv:2511.17160v2 PDF | scratchpad copy, SHA-256 `856bd78db8f86e46c0f5d21414ad0c1d136b176c6ac1b45418dbeebc38e920dd` | primary specification; full text re-extracted (pdfminer.six) for Secs. 2, 4, 5, footnote 8, Figs. 2–3 captions, conclusions |
| [W09] arXiv:0909.0749 PDF | scratchpad copy, SHA-256 `e37321e9d6021c6f5eb6bc5084ad331f4fca9dc0bc426097d1c5ce5ce7b2a8aa` | dressed-observable definitions already used and validated in Phase 1B |
| pinned upstream notebooks | commit `590c6fd`, notebook SHA-256 above | read-only provenance/reproduction evidence only |
| Phase 1B/1C-A/1C-B1/1C-B2 reports and packages | frozen at `9ec3bcc` | validated local evidence |

External sources consulted in this phase (complete bibliographic record):

| ref | full citation | access outcome |
|---|---|---|
| [GM 47] | G.F.R. Ellis, M. Bruni, J. Hwang, Phys. Rev. D 42 (1990) 1035 | not inspected (no accessible full text located) — external dependency |
| [GM 48] | M. Bruni, P.K.S. Dunsby, G.F.R. Ellis, *Cosmological Perturbations and the Physical Meaning of Gauge-invariant Variables*, ApJ 395 (1992) 34–53 | bibliographic identity confirmed via [ADS](https://ui.adsabs.harvard.edu/abs/1992ApJ...395...34B/abstract) and the [author's page](http://math_research.uct.ac.za/~peter/Peter_Dunsby/index.php/publications/cosmological-perturbations-and-the-physical-meaning-of-gauge-invariant-variables/); ADS scan is image-only (JBIG2), **content not independently inspected** — UNRESOLVED_EXTERNAL_DEPENDENCY |
| [GM 50] | P.K.S. Dunsby, M. Bruni, G.F.R. Ellis, *Covariant Perturbations in a Multifluid Cosmological Medium*, ApJ 395 (1992) 54 | same access outcome as [48]; **content not independently inspected**; remains the D3 adjudication dependency. No D3 adjudication is performed or implied in this phase |
| [GM 1] | H. Kodama, M. Sasaki, Prog. Theor. Phys. Suppl. 78 (1984) 1 | not inspected; the ΛCDM growing-mode IC recipe was already reproduced bit-exactly in Phase 1C-A from the sibling notebook, so [1]'s content is a provenance note, not a blocking dependency |
| [GM 65] | P. Mészáros, Astron. Astrophys. 37 (1974) 225 | not inspected; Eq. (4.27) audited against [GM] directly |
| Percival & White | W.J. Percival, M. White, *Testing cosmological structure formation using redshift-space distortions*, MNRAS 393 (2009) 297, [arXiv:0808.0003v2](https://arxiv.org/abs/0808.0003v2) | **full primary text inspected**, especially Secs. 2.1–2.3, Eqs. (1)–(14), and Secs. 3 and 6; these passages support the linear real-to-redshift-space mapping, the deterministic linear-bias and no-velocity-bias assumptions, and the conditional fσ8 normalisation statement used in Sec. 14. They do not supply a Timescape dressed mapping or a general survey fiducial/AP prescription |

Nothing was reconstructed from secondary summaries: every equation used
below is quoted from [GM] itself, from the validated Phase 1B code (with
its own [GM]/[W09] citations), or derived here with the derivation shown.

## 3. Exact definition of Δ_d

Verbatim definitional chain from [GM]:

- **[GM] (2.2):** `D_µ^(i) := (a/ρ^(i)) D_µ ρ^(i)` — the comoving fractional
  density gradient of fluid i, where `D_µ` is the observer-orthogonal
  projected covariant derivative and the local scale factor a is defined by
  `ȧ/a := Θ/3` along the observer congruence n^µ, "complemented by an
  **arbitrary initialisation** of a to a homogeneous or near-homogeneous
  value on a given spatial slice" ([GM] p. 5, emphasis added).
- **[GM] (2.19):** `a D_µ D_ν =: ∆_µν = (1/3) h_µν ∆ + Σ_µν + W_µν`, with
  `∆ := ∆^µ_µ ≃ (a²/ρ) (3)∆ρ` — "the scalar CGI variable measuring the
  aggregation of matter".
- **[GM] (2.20):** `∆^(i) := a D^µ D_µ^(i)`; likewise `Z := a D^µ Z_µ` with
  `Z_µ := a D_µ Θ` (2.4), and `V^(i) := a D^µ V_µ^(i)`.
- **[GM] p. 10 (verbatim):** "like ∆ above, the first-order variables Z, P,
  ∆^(i) and P^(i) are all **proportional to 3−Laplacians of local source
  fields** (Θ, p, ρ^(i) and p^(i) respectively), normalised to the local
  comoving length scale via a²."

Answers to the audit questions (classifications in brackets):

1. **Is Δ_d dimensionless?** Yes in the paper/notebook harmonic system:
   Δ_d,k = a²·(eigenvalue)·δ_k and the dimensionless label entering the
   eigenvalue is `k_code`, so Δ_d,k is dimensionless. In the volume-average
   coordinates, dimensional forms require either the comoving combination
   `k_com_D(c/H0_TS)` or the present-physical combination
   `k_phys0_D(a_D0 c/H0_TS)`; neither dimensional wavenumber may appear
   without its specifically associated length. [CONVENTION_DEPENDENT]
2. **Is it a local density contrast?** **No.** It is the a²-normalised
   spatial 3-Laplacian of the dust density divided by the density —
   [GM]'s own words above; also [GM] p. 27: the equal-amplitude ICs
   "effectively reduce the initial density contrasts for smaller-scale
   perturbations, compensating for the **intrinsic scale dependence of the
   ∆^(i) variables (as Laplacians of the associated densities)**".
   [VERIFIED_FROM_PRIMARY_SOURCE]
3. **Is it a Laplacian of a density contrast?** At linear order, yes:
   Δ_d ≃ a² (3)∆ δ_m with δ_m := δρ_d/ρ̄_d (derivation in Sec. 4).
   [DERIVED_FROM_VERIFIED_DEFINITIONS]
4. **Which frame defines it?** The observer congruence n^µ, chosen in
   [GM] Sec. 4 as the **dust energy frame** (V^(d) = 0): "the dust energy
   frame … represents the natural choice in our framework. We wish to
   ultimately interpret the CGI density perturbations in terms of gradients
   in the observed density field" ([GM] pp. 15–16). All four state
   variables (Δ_d, Z, Δ_eff, Ṽ_eff/V_eff) live in this frame; the overdot
   is the dust-frame covariant time derivative. [VERIFIED_FROM_PRIMARY_SOURCE]
5. **Which gauge-invariant quantity at linear order?** Δ_d is covariantly
   defined and vanishes identically in the FLRW background, hence
   first-order gauge-invariant (Stewart–Walker). By the derivation of
   Sec. 4 it equals, at linear order and per harmonic mode, −k_code² times the
   dust-frame (comoving) fractional density perturbation. The standard
   literature identification of that quantity with the Bardeen
   comoving-gauge density contrast is made in [GM 48]/[GM 50], whose full
   text was not inspected: within this audit the correspondence is derived
   from [GM]'s own equations, and its attribution to the original
   references remains an external dependency.
   Primary classification: DERIVED_FROM_VERIFIED_DEFINITIONS. Supporting
   provenance status: attribution to [GM 48]/[GM 50] remains
   UNRESOLVED_EXTERNAL_DEPENDENCY.
6. **Contrast, other invariant, or only a gradient scalar?** It is the
   divergence-scalar of the covariant fractional-density gradient — i.e.
   a second-spatial-derivative scalar, not itself a contrast. Its harmonic
   coefficient is proportional (factor −k_code²) to the contrast's coefficient.
   [DERIVED_FROM_VERIFIED_DEFINITIONS]
7. **Does the interpretation change between closures?** No. The definition
   (2.19)–(2.20) precedes any closure; Mészáros, comoving, and barotropic
   evolve the same variable under different closure assumptions.
   [VERIFIED_FROM_PRIMARY_SOURCE]

The notebook variable named `Delta_dust` is therefore **not** the
Fourier-space matter contrast δ_m; it is −k_code²·δ_m,k per mode in the
documented solver harmonic convention (Sec. 4), and
the distinction matters everywhere a spectrum or an absolute normalisation
enters.

## 4. Harmonic mapping to δ_m

**Derivation (equation chain D1).** Write ρ_d = ρ̄_d(t)(1 + δ_m), with
D_µ ρ̄_d = 0 at background level. Then, exactly to first order:

```text
Δ_d := a D^µ D_µ^(d)                              [GM (2.20)]
     = a D^µ [ (a/ρ_d) D_µ ρ_d ]                  [GM (2.2)]
     = a (D^µ a/ρ_d) (D_µ ρ_d) + (a²/ρ_d) D^µD_µ ρ_d
     ≃ (a²/ρ̄_d) (3)∆ (ρ̄_d δ_m)                   (first term is 2nd order)
     = a² (3)∆ δ_m .                               (D1a)
```

(the discarded term is a product of two first-order gradients; [GM] states
the same result as `∆ ≃ (a²/ρ)(3)∆ρ` in (2.19)). Sympy-verified by formal
ε-expansion (check S1, scratchpad `phase1d_symbolic.py`, PASS).

**Harmonic convention and units.** [GM] footnote 8 (p. 16, verbatim):
"hereafter we denote by k²/a² the eigenvalues of the (background)
3−Laplacian operator regardless of the topology assigned to the 3−space."
With the sign implemented in [GM] (4.10), audited in Phase 1C-A, define
`k_code` to be the dimensionless harmonic label that actually enters the
current solver matrix (`ResolvedWavenumber.matrix_k`):

```text
(3)∆ Q_k = −(k_code²/a_D²) Q_k .
```

[GM] Sec. 5 chooses K_D = 0, so the eigenfunctions are ordinary Fourier
modes. Applying this eigenvalue to (D1a) gives, per mode,

```text
Δ_d,k(t) = a_D² · (−k_code²/a_D²) · δ_m,k(t)
         = −k_code² δ_m,k(t).                                  (D1b-code)
```

This statement is exact for that fixed harmonic sign and label convention.

The wavenumber names used in this audit are:

- `k_code`: the constant dimensionless harmonic label entering the solver
  eigenvalue;
- `k_com_D`: the dimensional comoving wavenumber associated with the
  volume-average spatial coordinates;
- `k_phys_D(t)`: the physical volume-average wavenumber at time `t`;
- `k_phys0_D := k_phys_D(t0)`: its present value;
- `k_com_obs` (equivalently `k_com_dressed`): a future observational/dressed
  comoving wavenumber. Its mapping from the volume-average harmonic
  coordinate has not been derived.

These roles must not be collapsed into a single hybrid wavenumber label. With
the Timescape code length unit `c/H0_TS`, their volume-average relations are

```text
k_com_D      = k_code H0_TS/c,
k_phys_D(t)  = k_com_D/a_D(t),
k_phys0_D    = k_code H0_TS/(a_D0 c).                           (D1c)
```

Thus the length accompanying `k_com_D` is `c/H0_TS`, whereas the length
accompanying `k_phys0_D` is `a_D0 c/H0_TS`:

```text
k_code = k_com_D (c/H0_TS),
Δ_d,k(t) = −(k_com_D c/H0_TS)² δ_m,k(t),                        (D1b-com-D)

k_code = k_phys0_D (a_D0 c/H0_TS),
Δ_d,k(t) = −(k_phys0_D a_D0 c/H0_TS)² δ_m,k(t).                 (D1b-phys0-D)
```

Each displayed wavenumber and its associated length must use reciprocal
units: Mpc⁻¹ with Mpc, or numerical h Mpc⁻¹ with h⁻¹ Mpc. These are
volume-average-coordinate relations; they do not supply `k_com_obs`.

The two mandatory Phase 1C wavenumber choices determine how a supplied
number reaches this matrix label:

- `upstream_timescape_k`: the supplied number is `k_code` itself;
- `paper_lcdm_hubble_k`: the supplied paper label is
  `k_paper = k_phys0_D(c/H0_LCDM)`; the frozen solver then resolves
  `k_code = k_paper a_D0 H0_LCDM/H0_TS`. Consequently
  `k_phys0_D = k_code H0_TS/(a_D0 c) = k_paper H0_LCDM/c`: the B2
  conversion preserves the intended present physical volume-average mode
  between the two numerical conventions.

Thus the unresolved F7 question is whether the published numerical values
`{2π,5π,10π}` are upstream matrix labels or paper Hubble-length labels. It
changes the `k_code`, `k_com_D`, and `k_phys0_D` associated with a supplied
number; it does not change the algebra after the label has been resolved.
Neither convention nor the B2 conversion derives `k_com_obs`, which remains
necessary for an observational comoving power-spectrum integral.

- The factor C is **time-independent and scale-dependent**. The powers of
  a_D cancel exactly; no background-density factor or frame/gauge transform
  remains. [DERIVED_FROM_VERIFIED_DEFINITIONS]
- The minus sign is fixed by the documented negative-Laplacian eigenvalue.
  Reversing the harmonic/eigenvalue sign convention reverses the amplitude
  sign, but leaves |C|, relative growth ratios, logarithmic rates, and power
  spectra invariant. The primary classification of (D1b) is
  DERIVED_FROM_VERIFIED_DEFINITIONS; its sign and unit realisation are
  supporting CONVENTION_DEPENDENT qualifications.
- Because C is time-independent, on every interval where the amplitudes are
  nonzero, `d ln|Δ_d,k|/dx = d ln|δ_m,k|/dx` for any evolution parameter x
  (S2a, symbolic PASS). Had C depended on time, the correction would be
  `d ln|C|/dx` (S2b).
- (D1b) is definitional for Mészáros, comoving, and barotropic closures and
  is unaffected by D3, tilt representation, or D2; those choices affect the
  evolution, not this mapping.

**Power-spectrum transformation (equation chain D2).** For a common fixed
dimensionless harmonic label and one Fourier/statistical normalisation,

```text
P_Δ(k_code,t) = k_code⁴ P_δ(k_code,t),
Δ²_Δ(k_code,t) = k_code⁴ Δ²_δ(k_code,t).                         (D2-code)
```

For spectra parametrised by the dimensional volume-average comoving
wavenumber, under the same Fourier/statistical normalisation,

```text
P_Δ(k_com_D,t) = (k_com_D c/H0_TS)⁴ P_δ(k_com_D,t),
Δ²_Δ(k_com_D,t) = (k_com_D c/H0_TS)⁴ Δ²_δ(k_com_D,t).           (D2-com-D)
```

If instead the same volume-average spectrum is parametrised by the present
physical volume-average wavenumber,

```text
P_Δ(k_phys0_D,t) = (k_phys0_D a_D0 c/H0_TS)⁴ P_δ(k_phys0_D,t),
Δ²_Δ(k_phys0_D,t) = (k_phys0_D a_D0 c/H0_TS)⁴ Δ²_δ(k_phys0_D,t). (D2-phys0-D)
```

The fourth-power magnitude is invariant under a harmonic-sign change. The
`a_D0` form belongs only to the `k_phys0_D` parametrisation; a spectrum
conventionally expressed in comoving Mpc⁻¹ uses `k_com_D` and the `c/H0_TS`
factor, not the present-physical relation. Neither form establishes the
mapping to observational `k_com_obs`.

The notebook supplies equal **deterministic** initial Δ_d amplitudes for
three selected trajectory comparisons. That fact alone defines neither an
ensemble nor `P_Δ`. Only conditionally—if those amplitudes were interpreted
as equal RMS amplitudes under one common statistical mode normalisation—would
(D2) imply `P_δ ∝ k_code⁻⁴` (or the corresponding relation after choosing
one of the explicit volume-average wavenumber parametrisations above). The
notebook itself makes no such statistical definition.
[Primary classification: NOT_JUSTIFIED_FOR_OBSERVABLE_USE; the conditional
scaling follows from D2 under the stated extra assumptions.]

## 5. Frame and gauge interpretation

- Observer frame: dust energy frame, V^(d) = 0 ([GM] Sec. 4, quoted in
  Sec. 3). The dust is geodesic and irrotational; the effective fluid's
  tilt V^(eff) (and Ṽ^(eff) = (1+w_eff)V^(eff)) is its velocity-divergence
  scalar **relative to the dust**, V^(i) := a D^µ V_µ^(i) ([GM] 2.20) —
  not a peculiar velocity relative to any global expansion frame.
- Gauge invariance: all CGI variables vanish identically at background
  level, hence are first-order gauge-invariant; no gauge fixing enters
  anywhere in the audit.
- The Buchert averaging foliation and the CGI observer slicing coincide by
  construction ([GM] footnote 7): the dust-frame choice is what makes the
  averaged background and the perturbation variables share one foliation.
- Consequence for observables: quantities named "velocity" in the state
  vector (V_eff, Ṽ_eff) describe the effective fluid–dust tilt and have
  **no direct galaxy-peculiar-velocity meaning** (Sec. 14).

## 6. Growth-factor normalisation

Candidate definitions audited:

```text
G_Δ(k_code,t;t_ref) := Δ_d(k_code,t)/Δ_d(k_code,t_ref)
                        (defined iff Δ_d(k_code,t_ref) ≠ 0)
G_m(k_code,t;t_ref) := δ_m(k_code,t)/δ_m(k_code,t_ref)
                        (defined iff δ_m(k_code,t_ref) ≠ 0)
```

- **Normalisation removes the conversion:** with (D1b),
  G_Δ(k_code,t;t_ref) = G_m(k_code,t;t_ref) identically — C(k_code)
  cancels. A relative growth factor built from Δ_d **is** the relative growth
  factor of δ_m for the same harmonic mode, with no dimensional spatial
  mapping required. This requires linearity, a nonzero reference amplitude,
  and the explicit sign/crossing policy below. Absolute δ_m amplitudes,
  power spectra, σ_R/σ_8, and comparisons with observational k bins do
  require the relevant dimensional wavenumber and coordinate-frame mapping.
  [DERIVED_FROM_VERIFIED_DEFINITIONS]
- **Reference epoch:** any epoch with nonzero amplitude is mathematically
  admissible; it must be specified in an explicit coordinate — the Phase 1C
  epoch ambiguity (0.218 Gyr vs dressed z=20, labels `upstream_0p218_gyr` /
  `dressed_z20`) applies unchanged to t_ref, and a future
  `growth_reference` choice must state both the value and the coordinate
  (bare time vs dressed redshift). No default is proposed.
  [FORBIDDEN_AS_A_SILENT_DEFAULT]
- **Zero/sign-changing references:** if Δ_d(k,·) crosses zero at t_ref the
  ratio is undefined; if it crosses zero elsewhere the signed ratio remains
  well-defined but the logarithm does not (Sec. 8 policy).
- **When does a scale-independent D(t) exist?** Two conditions must hold:
  (i) the evolution operator is k-independent — true for the comoving
  system ([GM] p. 19, verbatim: "in the comoving ansatz, the dynamics of
  the perturbations are independent of their scale") and for the Mészáros
  equation (4.27); false for the barotropic system (the k²/a Ṽ_eff
  coupling; A34·A43 = −c_s²k_code²/a_D² ≠ 0 on both D3 branches whenever
  c_s² ≠ 0 — [GM] p. 22: "whose growth does depend on their scale");
  (ii) the **initial data ratio** Z(t_i)/Δ_d(t_i) (and Δ_eff IC) is the
  same for all k. A k-independent ODE with k-dependent initial mode
  mixtures still produces k-dependent growth histories. The upstream ICs
  satisfy (ii) by construction (identical values for all k); a physical
  spectrum satisfies it only under growing-mode dominance at t_i. This
  assumption must be stated by any future implementation.
  [DERIVED_FROM_VERIFIED_DEFINITIONS]
- **Barotropic:** only D(k,t) exists; it is scale-dependent on both branches.
  Primary classification: VERIFIED_FROM_PRIMARY_SOURCE ([GM] p. 22).
  Supporting evidence: Phase 1C-B2 numerically corroborates that dependence.

## 7. Bare and dressed growth rates

**Coordinates (equation chain D3).** All background relations below are the
frozen, validated Phase 1B forms (tests in `tests/test_wall_observables.py`),
with their [GM]/[W09] citations:

```text
γ_w(t)  = 1 + f_v(t)/2                              [GM p. 25; W09 (B7)]
a_w(t)  = a_D(t)/γ_w(t)                             [GM (5.4)]
1 + z_dressed = a_w0/a_w                            [GM p. 25; W09 (38)]
a_obs := 1/(1+z_dressed) = a_w/a_w0                 (D3a)
H_D     = (2+f_v)/(3t) ;  ḟ_v = f_v(1−f_v)/t        [tracker, Phase 1B]
H_dressed = γ_w H_D − γ̇_w = (4+f_v+4f_v²)/(6t)     [W09 (28)/(B8)]
```

Equation (D3a) retains the original Timescape normalisation: `a_w0` denotes
the present value of the original wall scale factor and is not silently set
to one. Define explicitly

```text
a_w_rescaled := a_w/a_w0,
a_D_rescaled := a_D/a_w0.
```

Only then may one write `a_obs = a_w_rescaled` and
`a_w_rescaled = a_D_rescaled/γ_w`. The frozen Phase 1B functions named
`a_w` and `a_D` already return these rescaled quantities (they are documented
as being in units of `a_w0`); their tested present value is therefore
`a_w_rescaled(t0)=1`, not an assertion that the original paper
normalisation has `a_w0=1`. Primary classification:
DERIVED_FROM_VERIFIED_DEFINITIONS. Supporting evidence: the frozen Phase 1B
redshift identity numerically corroborates the rescaled form.

**Definitions.** For a per-mode growth amplitude D (either Δ_d,k or
δ_m,k — identical rates by Sec. 4):

```text
f_bare    := d ln D / d ln a_D
f_dressed := d ln D / d ln a_obs = −(1+z_dressed) d ln D / d z_dressed
```

**Chain rule (equation chain D3, sympy checks S3b–S3f, all PASS).**
Because both are ratios of derivatives taken with respect to the *same*
parameter, any clock (t, τ_w, z) gives the same f for a given abscissa —
the **phenomenological lapse γ_w does not enter through the clock**; it
enters only through the abscissa. Because the constant `a_w0` cancels from a
logarithmic derivative, `d ln a_obs = d ln a_w_rescaled = d ln a_w`, and

```text
d ln a_obs/dt = d ln(a_w/a_w0)/dt
              = H_D − γ̇_w/γ_w = H_dressed/γ_w ,

f_dressed(t) = f_bare(t) · H_D/(H_D − γ̇_w/γ_w)
             = f_bare(t) · γ_w H_D / H_dressed
             = f_bare(t) · (2+f_v)² / (4 + f_v + 4 f_v²)   (tracker, exact).
```

Numerical values of the conversion factor (frozen background, notebook
preset; numeric checks N2–N3, closed form vs central differences agree to
<1e-8):

| epoch | f_v | f_dressed/f_bare |
|---|---|---|
| dressed z = 20 | 0.034522 | 1.02475 |
| upstream 0.218 Gyr (z = 18.586) | 0.038210 | 1.02726 |
| today (z = 0) | 0.737 | **1.08416** |

For these audited epochs the coordinate conversion changes f by 2.5–8.4 %.
This is a computed coordinate effect, not a comparison with any survey error
budget, and it can never be silently defaulted.

**Classification.**

- relation a_D ↔ z_dressed: VERIFIED_FROM_PRIMARY_SOURCE (validated 1B);
- `a_obs = 1/(1+z_dressed) = a_w/a_w0 = a_w_rescaled`:
  DERIVED_FROM_VERIFIED_DEFINITIONS; supporting Phase 1B numerical evidence
  corroborates the identity;
- f_bare: mathematically available; **implicitly** the upstream/paper
  presentation coordinate (Figs. 2–3 plot against a_D/a_w,0) — the paper
  itself never defines any growth rate f;
- f_dressed: mathematically available and observationally motivated
  (surveys quote z); not defined in the paper either;
- the choice between them: CONVENTION_DEPENDENT — proposed future
  mandatory labels `bare_aD` and `dressed_redshift`, **no default**
  [FORBIDDEN_AS_A_SILENT_DEFAULT].

## 8. Zero crossings and logarithmic singularities

**Analytic expression (equation chain D4).** From [GM] (4.14), Z = −Δ̇_d
exactly, and d ln a_D/dt = Θ/3:

```text
f_bare(k,t) = −3 Z_k(t) / ( Θ(t) Δ_d,k(t) )          (exact; sympy S4 PASS)
f_dressed(k,t) = f_bare(k,t) · (2+f_v)²/(4+f_v+4f_v²) (tracker chain factor)
dD/d ln a_D = −3 Z_k/Θ                                (finite everywhere)
```

So the growth rate needs **no numerical differentiation at all**: the state
vector already contains it. f has a **pole** wherever Δ_d,k = 0 with
Z_k ≠ 0 and a **zero** wherever Z_k = 0.

**Numerical provenance of the crossing evidence.** The B2 artifact does not
contain root-refined events. In
`artifacts/independent/phase1c_b2_convergence.json`,
`first_strict_zero_crossing_time` is exactly the left sample `t[i]` for which
`y[i] y[i+1] < 0`; see `trajectory_diagnostics` in the frozen B2 validator.
All seven solver configurations put the first sign change in the same sampled
bin, but that agreement is not an exact-root or solver-independent precision
claim. The common oracle grid has 1000 uniform samples from code time
0.0163265903 to 1.1516126667, with
`Δt = 0.00113642250` code units = 0.0151740 Gyr.

The table therefore reports **sampled-grid brackets**, not roots. Each entry
is `[left,right]` in code time / Gyr / dressed redshift; redshift decreases
from the left endpoint to the right endpoint.

| branch | k | first Δ_d sign-change bracket | first Z sign-change bracket |
|---|---|---|---|
| printed_4_15 | 2π | none sampled | none sampled |
| printed_4_15 | 5π | [0.227701, 0.228838] / [3.040, 3.056] / [2.418, 2.407] | [0.140197, 0.141333] / [1.872, 1.887] / [3.746, 3.720] |
| printed_4_15 | 10π | [0.077693, 0.078830] / [1.037, 1.053] / [6.012, 5.946] | [0.057238, 0.058374] / [0.764, 0.779] / [7.572, 7.462] |
| derived_4_10 | 2π | [0.784548, 0.785685] / [10.476, 10.491] / [0.371, 0.369] | [0.339071, 0.340207] / [4.527, 4.543] / [1.585, 1.579] |
| derived_4_10 | 5π | [0.150424, 0.151561] / [2.009, 2.024] / [3.528, 3.505] | [0.097013, 0.098149] / [1.295, 1.311] / [5.058, 5.012] |
| derived_4_10 | 10π | [0.067466, 0.068602] / [0.901, 0.916] / [6.694, 6.610] | [0.050419, 0.051556] / [0.673, 0.688] / [8.317, 8.181] |

These brackets preserve the qualitative result: the audited barotropic
Δ_d trajectories can cross zero, producing poles in their logarithmic growth
rates, and Z crosses earlier in every scenario with a sampled crossing, so f
first passes through zero and later diverges. Precise roots remain a Phase
1D-B implementation task. For the Mészáros and comoving baselines with
upstream-convention ICs, the tight in-memory trajectories show no sign
crossing over [t_i,t0], so their dust f is globally defined on that audited
interval. The IC Δ_eff(t_i)=0 does not affect the dust growth rate, but an
analogous effective-fluid logarithmic rate is undefined at t_i.

**Mandatory future numerical policy (design, not implemented):**

1. never evaluate log of a signed amplitude silently — logs only of |D|
   with the sign tracked separately;
2. detect every strict sign change of Δ_d,k, Z_k (and Δ_eff, tilt) by sign
   scan plus root refinement, and record all crossing times;
3. report the maximal intervals on which d ln D/d ln a is defined, and
   attach every f value to its interval;
4. always retain and expose the non-logarithmic derivative
   dD/d ln a = −3Z/Θ (bare) and its dressed counterpart — finite through
   all crossings;
5. distinguish d ln|D|/d ln a (defined except at crossings, equal to
   −3Z/(ΘΔ_d) wherever Δ_d ≠ 0) from d ln D/d ln a (undefined at and
   across crossings);
6. no interpolation, smoothing, or plotting across a singularity without
   explicit annotation of the crossing.

[Policy primary classification: PROVISIONAL (design for 1D-B). Crossing
existence primary classification: NUMERICALLY_CORROBORATED, at sampled-grid
bracket precision only.]

## 9. Power-spectrum transformation

Restating (D2) with all conventions explicit. Primary classification:
DERIVED_FROM_VERIFIED_DEFINITIONS. Supporting convention status:
CONVENTION_DEPENDENT for Fourier normalisation and the selected dimensional
wavenumber parametrisation:

- Fourier convention in one declared comoving frame `X`:
  δ(x_X) = ∫ d³k_com_X/(2π)³ δ_{k_com_X} e^{ik_com_X·x_X};
  ⟨δ_{k_com_X} δ_{k'_com_X}*⟩ =
  (2π)³ δ_D(k_com_X−k'_com_X) P_δ(k_com_X).
- For the same dimensionless label, `P_Δ(k_code,t) = k_code⁴ P_δ(k_code,t)`
  and `Δ²_Δ = k_code⁴ Δ²_δ`, exactly for every closure.
- For spectra parametrised by volume-average comoving `k_com_D`, the complete
  relation is `P_Δ(k_com_D,t) = (k_com_D c/H0_TS)⁴ P_δ(k_com_D,t)` and
  likewise for dimensionless power.
- If the same volume-average spectrum is instead parametrised by present
  physical `k_phys0_D`, the relation is
  `P_Δ(k_phys0_D,t) = (k_phys0_D a_D0 c/H0_TS)⁴ P_δ(k_phys0_D,t)`.
  The `a_D0` factor belongs only to this present-physical parametrisation,
  not to a spectrum expressed in comoving Mpc⁻¹. The sign convention
  cancels; the spatial-coordinate and unit choices do not.
- Equal deterministic upstream amplitudes do not define `P_Δ` or any other
  spectrum. If, and only if, they were treated as equal RMS amplitudes under
  a common statistical mode normalisation, the inferred density-contrast
  power would scale as `k_code⁻⁴`. The notebook does not make that ensemble
  assumption (Sec. 11).

## 10. σ_R and σ_8 definitions

**Derivation (equation chain D5).** Let `X` denote one fixed spatial
coordinate system. Smooth δ_m with a spherical top-hat of comoving radius
`R_com_X`, paired with its reciprocal comoving wavenumber `k_com_X` and
Fourier image `W(k_com_X R_com_X)`,
W(x) = 3(sin x − x cos x)/x³ = 3 j₁(x)/x. Then

```text
σ_R²(z) = ⟨(δ_m ⋆ W_R)²⟩
        = ∫ d³k_com_X/(2π)³ P_δ(k_com_X,z) W²(k_com_X R_com_X)
        = 1/(2π²) ∫₀^∞ dk_com_X k_com_X² P_δ(k_com_X,z)
          · W²(k_com_X R_com_X)
        = ∫₀^∞ d ln k_com_X Δ²_δ(k_com_X,z) W²(k_com_X R_com_X),
          Δ²_δ := k_com_X³P_δ/(2π²).                            (D5)
```

The standard observational `σ_8` uses an observational/dressed comoving
radius `R_com_obs = R_8 = 8 h⁻¹ Mpc` and therefore requires the reciprocal
observational/dressed comoving wavenumber `k_com_obs`. Every factor above is
fixed once the Fourier convention and common coordinate frame are fixed; the
numerical content then depends on the unit chain:

- **Which h?** `timescape_dressed_h` (h = 0.7323 notebook / 0.7303 paper
  best fit — the dressed H0 "directly extracted by observations",
  [GM] p. 25) gives R_8 = 10.92 Mpc; `lcdm_reference_h` (h = 0.674,
  Planck [3], the convention of the Fig. 3 caption) gives R_8 = 11.87 Mpc.
  Both are proposed as explicit future choices
  (`sigma_radius_h_convention`); **neither is selected**.
  [FORBIDDEN_AS_A_SILENT_DEFAULT]
- **Which spatial units for R?** The smoothing radius must additionally be
  declared as a dressed, bare (volume-average), wall, or reference-ΛCDM
  comoving length. The dressed geometry is the natural observational
  choice but is **not derived in [GM]**, so this too is an explicit future
  choice, not a default. Primary classification: CONVENTION_DEPENDENT;
  supporting unresolved dependency: no dressed smoothing prescription was
  found in [GM].
- **Scale-factor and k normalisation.** In the original notation,
  `1+z=a_w0/a_w` and neither `a_w0` nor the original `a_w(t0)` is silently
  set to one. The frozen Phase 1B `a_D` and `a_w` are explicitly rescaled by
  `a_w0`; hence `a_D,rescaled(t0)=γ_w0≈1.3685` and
  `a_w,rescaled(t0)=1`. For the current matrix label,
  `k_com_D=k_code H0_TS/c`, `k_phys_D(t)=k_com_D/a_D(t)`, and
  `k_phys0_D=k_code H0_TS/(a_D0 c)`; the present physical wavelength is
  `λ_phys0_D=2π a_D0 c/(H0_TS k_code)`. Under
  `paper_lcdm_hubble_k`, the supplied label instead uses
  `k_paper=k_phys0_D c/H0_LCDM` before the solver's explicit F7 conversion.
  That conversion preserves `k_phys0_D`; it does not derive `k_com_obs`.
- **Which matched k–R frame?** `k_com_D` may be paired only with a
  volume-average comoving radius `R_com_D`. It cannot be combined with the
  observational `R_8` unless a mapping to `k_com_obs` and `R_com_obs` has
  been derived. Conversely, `k_phys0_D` is a present physical
  volume-average wavenumber and cannot be inserted directly into
  `k_com_obs R_com_obs` merely because it is dimensional. The missing map
  from the volume-average harmonic coordinate to the dressed observational
  comoving coordinate is an explicit blocker for observational `σ_8`.

**Why the three Fig. 3 modes cannot define σ_8**
[primary classification: DERIVED_FROM_VERIFIED_DEFINITIONS]:

1. (D5) is an integral over a continuous ln k measure; three isolated
   modes supply neither a continuous measure nor a justified quadrature or
   interpolation rule.
2. Their equal initial values are deterministic trajectory-comparison
   amplitudes, not samples of a statistically normalised `P_Δ` or `P_δ`
   (Secs. 4, 9, 11).
3. Their positions in an observational `k_com_obs R_com_obs` kernel are
   unknown because the volume-average-to-dressed comoving coordinate map is
   unresolved; the h and F7 convention forks do not supply that map.
4. **Required for a real σ_R:** a continuous statistical spectrum in one
   declared comoving coordinate frame over a
   domain demonstrated to capture the chosen window integral, an explicit
   spectrum shape and amplitude, and the complete unit chain. The necessary
   numerical k extent must be established by convergence for that spectrum;
   this audit does not prescribe one.

## 11. Initial-spectrum and amplitude requirements

The upstream initial amplitude Δ_d(t_i) = 0.0031427229788258105 (bit-exact
qplus provenance, Phase 1C-A) together with the paper's own description —
ICs "with the same values for all scales for direct comparison"
(Fig. 3 caption); "we effectively reduce the initial density contrasts for
smaller-scale perturbations" (p. 27) — defines:

- a deterministic **per-selected-mode comparison amplitude**: YES;
- equal deterministic normalisation for the three selected trajectory runs:
  YES, but this is not a statistical or spectral normalisation;
- a power-spectrum amplitude: **NO**;
- σ_8 at the initial epoch: **NO**;
- anything more without additional assumptions: **NO**.

Conditional statement only: if the equal deterministic harmonic amplitudes
were interpreted as equal RMS amplitudes under one common statistical mode
normalisation, (D2) would imply a `k_code⁻⁴` scaling for the corresponding
density-contrast power (with the appropriate explicit fourth-power factor
for `k_com_D` or `k_phys0_D`). The notebook defines no ensemble or power
spectrum, so that
conditional inference is not an upstream result.

Using this value to normalise a continuous matter power spectrum would
therefore be scientifically invalid: it fixes one number at an unspecified
effective scale, while σ_8 requires an amplitude *and shape* over the
kernel support. [NOT_JUSTIFIED_FOR_OBSERVABLE_USE]

**Future normalisation strategies (audited, none selected, none
implemented):**

| strategy | primary classification | qualification |
|---|---|---|
| `external_linear_pk_at_zref` | PROVISIONAL | implementable only with an external transfer/linear P(k); imports a ΛCDM-calibrated shape and amplitude at z_ref |
| `sigma8_anchor_at_zref` | PROVISIONAL | normalisation-only, not predictive; shape-free for scale-independent growth, but scale-dependent growth additionally requires a spectrum shape |
| `primordial_As_ns_external_transfer` | PROVISIONAL | requires an external transfer function and assumes its early-universe applicability |
| `upstream_equal_deterministic_Delta_amplitude` | NOT_JUSTIFIED_FOR_OBSERVABLE_USE | valid only for relative selected-mode comparisons; any silent use is FORBIDDEN_AS_A_SILENT_DEFAULT |

## 12. Scale-independent fσ8 identity

**Derivation (equation chains D5–D6; sympy S5 PASS).** Assume:

(A1) linear evolution throughout;
(A2) scale-independent growth: δ_m(k_com_X,z) = D(z)
     δ_m(k_com_X,z_ref) for every k_com_X in the support of the matched-frame
     kernel Δ²_δ W²(k_com_X R_com_X) (equivalently: k-free evolution
     operator **and** k-independent initial mode-mixture, Sec. 6);
(A3) fixed spectrum shape at z_ref (no shape evolution besides D);
(A4) one fixed smoothing convention (R_8, h choice, spatial-unit choice);
(A5) D(z) > 0 and differentiable on the interval considered;
(A6) a consistent reference normalisation σ_8(z_ref).

Then, directly from (D5):

```text
σ_8(z) = D(z) σ_8(z_ref)                                       (D6a)
d σ_8/d ln a = (dD/d ln a) σ_8(z_ref) = f(z) σ_8(z) ,           (D6b)
```

with f = d ln D/d ln a in the **same** a-coordinate on both sides — the
bare/dressed choice (Sec. 7) rescales fσ8 by 1.02–1.08 and must be explicit.

**Do the conditions hold?**

| system | verdict |
|---|---|
| Mészáros | (A2) holds mathematically ((4.27) is k-free; upstream ICs k-independent); (A5) corroborated (no crossings). The identity is **evaluable** — but this does not confer physical validity: [GM] itself concludes "the Mészáros approximation should not be applicable in the timescape framework" (p. 26). |
| comoving | (A2) holds under the same IC caveat ([GM] p. 19 scale-independence); (A5) corroborated (no crossings; monotone growth). Identity evaluable, same external-normalisation caveat. |
| barotropic printed_4_15 | (A2) **fails** (scale-dependent); (A5) fails at 5π, 10π (crossings). Identity not available; only the Sec. 13 generalisation applies. |
| barotropic derived_4_10 | (A2) fails; (A5) fails at all three modes. Same conclusion. |

Primary classification of (D6): DERIVED_FROM_VERIFIED_DEFINITIONS, subject
to assumptions A1–A6. This mathematical classification does not supply the
missing spectrum normalisation or RSD interpretation.

## 13. Scale-dependent generalisation

**Derivation (equation chains D7–D8; sympy S6 PASS).** In one fixed spatial
coordinate frame `X`, with per-mode growth D(k_com_X,z) normalised at z_ref
and weights defined by the evolved matched-frame kernel:

```text
σ_R²(z) = ∫ d ln k_com_X Δ²_δ(k_com_X,z_ref) D²(k_com_X,z)
          · W²(k_com_X R_com_X)                                (D7)

F_R(z) := d σ_R/d ln a
        = (1/σ_R(z)) ∫ d ln k_com_X Δ²_δ(k_com_X,z)
          · f(k_com_X,z) W²(k_com_X R_com_X)                   (D8)

f_R,eff(z) := (1/σ_R) dσ_R/d ln a
            = ∫ d ln k_com_X Δ²_δ f W²(k_com_X R_com_X)
              / ∫ d ln k_com_X Δ²_δ W²(k_com_X R_com_X)
```

— the **kernel-weighted mean of the spectral growth rate** f(k,z)
= d ln D(k,z)/d ln a. This f_R,eff is a different object from the standard
scale-independent f(z) and reduces to it only under (A2). Two important
mathematical facts:

- the integrand of F_R is Δ²_δ(k,z_ref)·D·(dD/d ln a)·W², which stays
  **finite through individual mode zero crossings** (D·D′ is finite even
  where ln D is singular); only σ_R(z) = 0 — all weighted modes vanishing
  simultaneously — would make f_R,eff singular;
- differentiation under the integral requires dominated convergence
  (locally bounded D·D′ over the kernel support) — an explicit assumption
  given the rapidly growing high-k barotropic modes.

Cautious future public labels (proposed, not implemented):
`spectral_growth_rate` (f(k,z)), `sigma_R`, `d_sigma_R_d_lna` (F_R),
`sigma_R_weighted_growth_rate` (f_R,eff). In a scale-dependent model,
`d_sigma8_d_lna` must **not** be automatically labelled fσ8.
[DERIVED_FROM_VERIFIED_DEFINITIONS]

## 14. Relation to observed redshift-space-distortion fσ8

**What the inspected RSD source establishes.** Percival & White
([arXiv:0808.0003v2](https://arxiv.org/abs/0808.0003v2)) was inspected at
full-text level, not merely at abstract level. In its FLRW/plane-parallel
linear framework:

- Sec. 2, Eqs. (1)–(4), defines the real-to-redshift-space position map and
  derives the overdensity Jacobian under number/mass conservation, the
  distant-observer approximation, and an irrotational velocity field;
- Sec. 2.1, Eqs. (5)–(8), gives the linear redshift-space overdensity/power
  decomposition and then imposes the linear-theory velocity relation;
- Sec. 2.2, Eqs. (9)–(10), introduces scale-independent deterministic local
  linear galaxy bias; Eq. (11) is explicitly conditional on galaxies
  sampling the matter velocity field (no velocity bias); Eq. (12) is the
  resulting standard linear Kaiser form;
- Sec. 2.3, Eqs. (13)–(14), states the top-hat RMS normalisation and shows
  which combinations of b, f, and σ8 the anisotropic spectrum can constrain.

These are assumptions and results inside that model, not identities already
established for the Timescape variables. Percival & White does not derive a
Timescape dressed redshift-space map. It also does not, in the passages
inspected, provide the general Alcock–Paczynski/fiducial-cosmology conversion
needed to compare a Timescape prediction to a particular survey likelihood.
Those details remain UNRESOLVED_EXTERNAL_DEPENDENCY. Its Sec. 6 simulation
k cuts test that paper's estimator and are not a universal fitted-k range;
the previous generic `~0.02–0.2 h/Mpc` claim is therefore withdrawn.

**Can the Timescape CGI variables be identified with the RSD
velocity-growth combination? (equation chain D9)**

From the definitions: Z := a D^µ(a D_µ Θ) ≃ a²(3)∆(δΘ) → per mode
Z_k = −k_code²(δΘ)_k, where δΘ is the fluctuation of the **dust congruence's
own expansion scalar**. Combining with (4.14) and (D1b):

```text
Z_k = −Δ̇_d,k = k_code² δ̇_m,k   ⇒   δ̇_m,k = −(δΘ)_k ,
```

the exact CGI dust continuity relation. A correspondence between `(δΘ)_k`
and an RSD velocity-divergence variable is PROVISIONAL: Percival & White
define their velocity divergence inside an FLRW redshift-space construction,
whereas **in the averaged model there is no global FLRW
frame** — δΘ is defined relative to the inhomogeneous dust flow itself,
and its translation into an observed redshift-space anisotropy requires a
light-propagation / redshift-space mapping built on the **dressed**
geometry, which [GM] does not derive and which no frozen local result
provides. Therefore:

- **Δ_d** → related to δ_g only through the mapping (D1b) *plus* a bias
  model: not directly identifiable. [NOT_JUSTIFIED_FOR_OBSERVABLE_USE as is]
- **Z** → the identification "Z = observed peculiar-velocity divergence"
  is **rejected as a direct identity**: Z is −k_code² times the dust-frame
  expansion fluctuation; it becomes the RSD θ only under (a) a derived
  dressed redshift-space mapping, (b) no velocity bias, (c) the FLRW-like
  continuity closure on the fitted scales, and (d) an explicit bare/dressed
  H choice in θ's normalisation. None of (a)–(d) is currently established.
  [NOT_JUSTIFIED_FOR_OBSERVABLE_USE without the listed derivations]
- **V_eff, Ṽ_eff** → tilt of the *effective fluid* relative to dust; no
  automatic galaxy-velocity interpretation. [NOT_JUSTIFIED_FOR_OBSERVABLE_USE]
- **dσ_8/d ln a** → a derived density statistic; equals the RSD-inferred
  fσ8 only under the full set of Secs. 12–13 assumptions *plus* (a)–(d)
  above *plus* a normalisation (Sec. 11).

**Classification of "the present perturbation systems predict observed
fσ8": NOT_JUSTIFIED_FOR_OBSERVABLE_USE.** Missing, independently: an
absolute normalisation (Sec. 11); the continuous k-domain (Sec. 10); the
RSD interpretation chain (this section); resolution of the D3 / rate-unit /
epoch / wavenumber / h / coordinate conventions; and — for the barotropic
system — the paper's
own assessment that its sub-horizon behaviour is "ultimately unphysical"
([GM] p. 26) with growth "too fast to be reasonably compatible with the
observed structure formation" ([GM] conclusions). Note [GM] itself claims
no fσ8 prediction: fσ8 appears there only as motivation and as "a natural
extension of this work" (conclusions). This classification is a statement
about *current evidence*, not about the framework's potential.

## 15. Scenario and convention inventory

Complete future scenario dimensions (all mandatory-explicit; **no silent
default anywhere**; `not_applicable` must be passed explicitly where marked):

| field | allowed values | meaning / applicability / interactions |
|---|---|---|
| `perturbation_system` | `meszaros`, `comoving`, `barotropic` | closure choice; determines dimensionality, scale dependence, and which fields below apply. Affects time evolution and observable interpretation |
| `background_preset` | `paper_reference` (H0=73.03, fv0=0.737), `notebook_reference` (H0=73.23, fv0=0.737) | frozen Phase 1B presets; affects all background coefficients, epochs, unit conversions (amplitude + time evolution) |
| `d3_branch` | `not_applicable` (mesz/comoving — must be passed explicitly), `printed_4_15`, `derived_4_10` | unresolved A33 provenance (1C-A F1); barotropic only; order-10²–10⁴ endpoint effect; interacts with everything downstream (crossing times, f poles) |
| `tilt_form` | `not_applicable` (mesz/comoving), `unrescaled_V`, `rescaled_Vtilde` | state normalisation of the tilt; exactly equivalent under the validated transform for corrected c_s²; bookkeeping choice, must still be explicit |
| `rate_unit_convention` | `upstream_unconverted`, `lcdm_to_timescape_converted` | 1C-A F3: units of the initial Z ([GM] "Z(t_i) ≈ −0.16 H0" leaves which H0 ambiguous); 3.6–7.1 % endpoint effect (B2); affects amplitude and phase of growth histories |
| `epoch_choice` | `upstream_0p218_gyr`, `dressed_z20` | 1C-A F4: initial-time ambiguity; up to 61 % endpoint effect at 10π (B2); also applies to any growth reference epoch (Sec. 6) |
| `wavenumber_convention` | `not_applicable` (mesz/comoving), `upstream_timescape_k`, `paper_lcdm_hubble_k` | 1C-A F7: numerical meaning of k (factor 1.259551 on matrix k); the B2 conversion preserves the intended `k_phys0_D` but does not derive `k_com_obs`; dominant high-k effect (up to 10⁵–10⁶ %, B2); propagates into every σ_R integral |
| `growth_coordinate` | `bare_aD`, `dressed_redshift` | **new (this audit)**: abscissa of D and f; exact conversion factor (2+f_v)²/(4+f_v+4f_v²) = 1.025–1.084; multiplies any fσ8-like number |
| `density_contrast_mapping` | `keep_Delta_d`, `map_to_delta_m_via_minus_k_code2` | **new**: whether outputs retain the CGI Laplacian variable or use (D1b-code); ratios/rates are invariant, while spectra require `k_code⁴`, `(k_com_D c/H0_TS)⁴`, or `(k_phys0_D a_D0 c/H0_TS)⁴` in the matching parametrisation; sign, frame, and units must be documented |
| `initial_spectrum_model` | `upstream_equal_deterministic_Delta_modes` (comparison only; not a spectrum), `external_linear_pk_at_zref`, `primordial_As_ns_external_transfer` | **new**: what carries the k-shape; the upstream option supplies no statistical shape and is forbidden for σ_R |
| `normalization_strategy` | `external_linear_pk_at_zref`, `sigma8_anchor_at_zref`, `primordial_As_ns_external_transfer`, `upstream_equal_deterministic_Delta_amplitude` (forbidden for σ_8) | **new**: what fixes the amplitude (Sec. 11 classifications); interacts with `initial_spectrum_model` (a P(k) source provides both) |
| `sigma_radius_h_convention` | `timescape_dressed_h`, `lcdm_reference_h` | **new**: which h defines R_8 = 8 h⁻¹ Mpc (10.92 vs 11.87 Mpc) and the k-unit chain; `R_com_X` must be paired with `k_com_X` in the same dressed/bare/wall/reference-ΛCDM coordinate frame |

Every field affects at least one of {shape, amplitude, time evolution,
physical scale, observable interpretation}; the JSON companion records the
per-field breakdown, applicability matrix, and unresolved status.

## 16. Implementation gates for Phase 1D-B (go/no-go design)

**GO (implementable now, under mandatory-explicit choices):**

1. per-mode signed growth histories D(k,t) (barotropic) and D(t) (clean
   systems), with the crossing scan of Sec. 8 built in from the start;
2. f_bare and f_dressed per mode via the analytic expression
   −3Z/(ΘΔ_d) and the exact tracker chain factor — no numerical
   differentiation; both coordinates as a mandatory `growth_coordinate`;
3. the per-mode δ_m mapping layer (D1b-code/D1b-com-D/D1b-phys0-D) as a pure,
   documented conversion (`density_contrast_mapping`), with mandatory
   harmonic-sign and explicit `k_code`, `k_com_D`, or `k_phys0_D` metadata;
   this does not implement a dressed comoving spectrum mapping;
4. **conditionally**: an fσ8-*shaped* diagnostic
   f(z)·D(z)·σ_8(z_ref) for the two scale-independent closures under an
   explicit `sigma8_anchor_at_zref` — labelled as a conditional diagnostic
   (assumptions A1–A6 + anchor), never as a predicted observational fσ8.

**NO-GO (blocked until the listed dependency is resolved):**

5. absolute observational σ_8 or σ_R: blocked by `initial_spectrum_model` +
   `normalization_strategy` (external spectrum required), the continuous-k
   domain (Sec. 10 — requires barotropic validation far beyond 10π, or the
   scale-independent closures plus an external shape), and the unresolved
   volume-average-to-dressed comoving coordinate map;
6. any barotropic fσ8 number: blocked by scale dependence (only the
   Sec. 13 weighted quantities are mathematically defined) and by the
   sampled Δ_d crossings/logarithmic poles in the audited trajectories;
7. any comparison to RSD data, likelihood, covariance, or fit: blocked by
   the Sec. 14 interpretation chain (dressed redshift-space mapping, bias,
   fiducial corrections) — none of which may be assumed silently.

**Standing gates carried forward:** all Phase 1C mandatory-explicit
arguments; D2 stays forensic-only; both D3 branches always implemented and
reported side by side; no branch/coordinate/h/spectrum/normalisation
default; validation per Sec. 12-design below (controlled one-factor
studies, no uncontrolled Cartesian product).

**Controlled validation design for later phases (design only):**

1. scale-independent clean-system checks: D(t) and f from Δ_d vs from the
   analytic −3Z/(ΘΔ_d) (identity to solver tolerance); cross-solver
   convergence as in B1/B2;
2. D3 branch comparisons: same scenario, branch toggled, everything else
   fixed (as in B2's factorial but extended to f and σ-level quantities);
3. one-factor-at-a-time studies for: rate units, epoch, k convention,
   background preset, growth coordinate, normalisation strategy — six
   controlled axes off one declared baseline, each axis reported as a
   separate delta;
4. scale-dependent σ_R convergence: k-grid refinement and integration-rule
   convergence of (D7)–(D8) at fixed physics, reported separately from
   physics deltas;
5. corner checks: highest validated k, epochs adjacent to crossings,
   near-phantom background epochs.

**Uncertainty taxonomy (mandatory in 1D-B reporting):** numerical
(grid/integration) vs solver (tolerance/method) vs spectrum-normalisation
(anchor/shape source) vs unresolved-convention spread (D3, units, epoch,
k, h, coordinate) vs model/closure dependence (Mészáros vs comoving vs
barotropic). An envelope across unresolved conventions is a *convention
spread* and **must not** be described as a statistical confidence interval.

## 17. Unresolved scientific dependencies

1. **D3 branch** (`printed_4_15` vs `derived_4_10`): unchanged; [GM 50]
   full text remains the adjudication dependency; not inspected (image-only
   scans); no adjudication performed here.
2. **[GM 48] full text**: attribution of the linear-order identification of
   Δ to the comoving density perturbation (Sec. 3 item 5) — derived
   internally, attribution unverified.
3. **Rate-unit convention (F3)**: [GM]'s "Z(t_i) ≈ −0.16 H0" does not state
   which H0; both readings remain implemented upstream of this audit.
4. **Epoch (F4)**: 0.218 Gyr vs dressed z = 20 (0.19621 Gyr) unexplained;
   also afflicts any growth-reference epoch.
5. **Wavenumber convention (F7)** and the KD (background curvature) choice.
   The B2 conversion preserves the intended `k_phys0_D` between its two
   numerical conventions but does not derive observational `k_com_obs`.
6. **RSD interpretation chain**: Percival & White Secs. 2.1–2.3 verifies the
   standard FLRW linear assumptions, but a dressed-geometry redshift-space
   mapping, bias/velocity interpretation, and survey fiducial/AP conversion
   for the averaged model remain unresolved external dependencies; this is a
   research task, not a convention choice.
7. **Spectrum and normalisation**: any absolute σ_8 requires an external
   linear spectrum/transfer (ΛCDM-calibrated) or an anchor datum — both
   imports, with the PROVISIONAL caveats of Sec. 11.
8. **h and matched comoving k–radius conventions** for σ_R (Sec. 10),
   including the unresolved `k_com_D`-to-`k_com_obs` coordinate map.
9. **[GM 1] (Kodama–Sasaki)**: content of the ΛCDM growing-mode formula not
   independently inspected (recipe itself reproduced bit-exactly in 1C-A).

## 18. Conclusions: what may and may not yet be computed

| quantity | verdict |
|---|---|
| relative Δ_d growth history (per mode, signed) | **YES** — fully justified now, under the mandatory-explicit Phase 1C choices |
| relative δ_m growth history (per mode) | **YES, CONDITIONALLY** — equal to the Δ_d history by (D1b)/C-cancellation; requires the same harmonic mode, a nonzero reference amplitude, the linear mapping, and an explicit sign/crossing policy; resolving the dimensional spatial map is not required because the constant harmonic factor cancels |
| f_bare | **YES, CONDITIONALLY** — analytic via −3Z/(ΘΔ_d); global for the clean systems; piecewise between crossings for barotropic (crossing policy of Sec. 8 mandatory) |
| f_dressed | **YES, CONDITIONALLY** — same conditions plus the exact validated chain factor (2+f_v)²/(4+f_v+4f_v²); coordinate must be explicit |
| σ_8 | **NO, MISSING NORMALIZATION** — also missing spectrum shape, continuous k-domain, and the observational/dressed comoving k–radius mapping |
| dσ_8/d ln a | **NO, MISSING NORMALIZATION** — inherits all σ_8 spectrum/frame blockers and additionally requires the growth-coordinate choice; evaluable as f·D·σ_8(z_ref) only under an explicit anchor + A1–A6 (then a conditional diagnostic, not a measurement-comparable number) |
| standard observational fσ8 | **NO, MISSING RSD INTERPRETATION** — also inherits the missing normalisation and observational/dressed comoving mapping; the claim that the present systems predict observed fσ8 is NOT_JUSTIFIED_FOR_OBSERVABLE_USE |

**Recommended minimal Phase 1D-B scope:** items GO-1..3 of Sec. 16 (growth
histories, analytic f in both coordinates with the crossing policy, and the
δ_m mapping layer), plus — optionally and clearly labelled conditional —
GO-4 (anchored fσ8-shaped diagnostic for the clean systems only). Nothing
else.

## 19. Repository preservation and compliance

- The original Phase 1D-A deliverables are
  `reports/phase1d_a_growth_observable_audit.md` and
  `reports/phase1d_a_observable_inventory.json`. This corrective revision
  modified exactly those two existing untracked files and created, deleted,
  renamed, or formatted no other file.
- No frozen scientific source, test, report, figure, upstream file, or
  generated B1/B2 artifact was touched; artifacts were read only. This
  corrective revision used only in-memory checks and created no scratch file.
  The original Phase 1D-A scratch provenance remains unchanged.
- Upstream clone remains at `590c6fd`, clean; notebook SHA-256 unchanged
  (verified before and after this corrective revision).
- Not committed, tagged, pushed, staged, or published; authors not
  contacted.
- `git status` / `git diff --check` outputs are reported in the phase
  completion message (deliverables intentionally left untracked).
