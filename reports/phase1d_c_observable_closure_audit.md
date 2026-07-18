# Phase 1D-C — Observable-closure audit and implementation design

Date (UTC): 2026-07-17

Branch: `phase-1d-c-observable-closure-audit` (created at the frozen
checkpoint below; not pushed).

Machine-readable companion: `reports/phase1d_c_closure_inventory.json`.

Primary specification: Galoppo & Mourier,
[arXiv:2511.17160v2](https://arxiv.org/abs/2511.17160), JCAP 02 (2026) 066
— cited as [GM]. Wiltshire, [arXiv:0909.0749](https://arxiv.org/abs/0909.0749),
Phys. Rev. D 80 (2009) 123512 — cited as [W09]. Percival & White,
[arXiv:0808.0003v2](https://arxiv.org/abs/0808.0003v2), MNRAS 393 (2009) 297
— cited as [PW]. Dunsby, Bruni & Ellis, ApJ 395 (1992) 54 — cited as
[DBE92] (= [GM 50]). Bruni, Dunsby & Ellis, ApJ 395 (1992) 34 — cited as
[BDE92] (= [GM 48]).

---

## 1. Scope and non-implementation statement

This phase is a **research, derivation, and design audit only**. It
determines the exact scientific closure status of the chain

```
validated per-mode growth -> statistical matter spectrum
  -> sigma_R / sigma_8 -> density-growth derivative
  -> observational RSD f-sigma-8
```

and designs (without implementing) the future API, validation plan, and
phase decomposition. **Nothing was implemented**: no power spectrum,
sigma_R, sigma_8, f-sigma-8 (or any f-sigma-8-shaped function), transfer
function, spectrum reader, CAMB/CLASS integration, top-hat integrator,
continuous-k solver, k-interpolation, RSD/Kaiser mapping, bias model, AP
conversion, dataset loader, covariance/likelihood/fitting code, figure, or
package placeholder was created. The only tracked files created are this
report and its JSON companion. All external reference downloads and
symbolic checks live in the ignored session scratchpad. No frozen file was
modified; nothing was committed, staged, tagged, or pushed; authors were
not contacted. `README.md` and `CLAUDE.md` were not modified.

Equations, pseudocode, proposed schemas, and test designs appear **only**
inside the two reports, as permitted.

## 2. Repository and provenance preflight

All checks executed before any research or file creation; all passed:

| check | result |
|---|---|
| branch at start | `phase-1d-b-growth-pipeline` ✓ |
| HEAD | `93d956d0020f0edec34a44cd9d19f30c085aecc7` ✓ |
| base tag `phase-1d-b-growth-pipeline-v1` → HEAD | ✓ (tag commit = HEAD) |
| ancestors: `phase-1b-background-v1`, `phase-1c-a-equation-audit-v1`, `phase-1c-b1-clean-systems-v1`, `phase-1c-b2-barotropic-v1`, `phase-1d-a-growth-observable-audit-v1`, `phase-1d-b-growth-pipeline-v1` | all ✓ |
| working tree and index clean; nothing staged | ✓ |
| upstream clone (`.reference/Linear-Perturbations-in-averaged-cosmological-models`) | `590c6fd5332acb15f5683ebf392a0d7ce54983c5`, clean ✓ |
| `ACPT_Timescape.ipynb` SHA-256 | `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a` ✓ |
| pytest, Python 3.14.3 (.venv) | **337 passed** ✓ |
| pytest, Python 3.11.9 (.venv311) | **337 passed** ✓ |
| `git diff --check` | clean ✓ |

Branch `phase-1d-c-observable-closure-audit` was then created exactly at
`93d956d0020f0edec34a44cd9d19f30c085aecc7` and is the working branch of
this phase. It was not pushed.

## 3. Frozen findings inherited from 1D-A and 1D-B

The fifteen frozen facts of the phase specification are restated in the
JSON companion (`frozen_conclusions`) and were treated as frozen
throughout. In particular: `Delta_d,k = -k_code^2 delta_m,k` (documented
harmonic convention); per-mode relative growth ratios of `Delta_d` and
`delta_m` are identical; `f_bare = -3Z/(Theta Delta_d)`;
`f_dressed = f_bare (2+f_v)^2/(4+f_v+4f_v^2)`; `Delta_d` crossings give
logarithmic-rate poles and Z crossings give rate zeros; Mészáros/comoving
growth is scale-independent only under k-independent initial mode
mixtures; barotropic growth is scale-dependent; both D3 branches
(`printed_4_15`, `derived_4_10`) remain mandatory; D2 is forensic-only; no
scientific choice has a default; the three upstream modes are
deterministic trajectory comparisons, not a spectrum; Phase 1D-B contains
no spectrum/sigma/f-sigma-8/RSD observable; barotropic large-amplitude
results are numerically converged but not automatically physically linear;
no current state variable is directly an observed peculiar velocity or RSD
quantity.

**One proposed evidence upgrade (reported, not silently adopted).** New
primary evidence obtained this phase (Sec. 24) *structurally corroborates*
the `derived_4_10` self-coupling sign and *verifies* the previously
unverified [GM 48] Bardeen attribution. Neither changes any frozen code or
label; D3 remains an unresolved dual-branch choice (Sec. 24 states the
exact residual gap).

## 4. Primary-source inventory

Local (verbatim inspection this phase unless noted):

| source | identity | inspection |
|---|---|---|
| [GM] arXiv:2511.17160v2 PDF | re-downloaded to scratchpad; SHA-256 `856bd78db8f86e46c0f5d21414ad0c1d136b176c6ac1b45418dbeebc38e920dd` — **bit-identical** to the frozen 1D-A provenance hash | full text re-extracted (pdfminer.six, scratchpad-isolated install); pp. 9, 16–17 additionally rendered to page images and equations (2.19)–(2.24), (4.5)–(4.18) read visually; Secs. 5.1–5.3 and conclusions read from extracted text |
| [W09] arXiv:0909.0749 PDF | re-downloaded; SHA-256 `e37321e9d6021c6f5eb6bc5084ad331f4fca9dc0bc426097d1c5ce5ce7b2a8aa` — bit-identical to 1D-A hash | full text extracted; dressed-geometry construction (Sec. II.4, Eqs. (22)–(27)) read verbatim; ar5iv HTML also inspected |
| frozen Phase 1B/1C/1D-A/1D-B reports, packages, inventories | at `93d956d` | 1D-A audit + inventory read in full; 1D-B validation report, compliance audit, all seven `growth/` modules, and the generated 1D-B artifact (read-only) inspected |
| pinned upstream notebook | SHA-256 above | provenance only, untouched |

External sources (full records with access outcomes in the JSON;
highlights):

| ref | citation / DOI | outcome |
|---|---|---|
| [DBE92] = [GM 50] | Dunsby, Bruni & Ellis, *Covariant Perturbations in a Multifluid Cosmological Medium*, ApJ 395 (1992) 54–74, DOI 10.1086/171629 | **INSPECTED (first time in this project).** ADS scan (image-only JBIG2) downloaded (SHA-256 `3a082920b358872ec64a3706001e1a10a61a51f2e5140cf29662aa1a04b72f20`), all 21 pages rendered to images; pp. 54, 58, 59, 60 read visually: Eqs. (26)–(36), (42)–(55) inspected, including the component equations (46), (49), (54), (55) |
| [BDE92] = [GM 48] | Bruni, Dunsby & Ellis, *Cosmological Perturbations and the Physical Meaning of Gauge-Invariant Variables*, ApJ 395 (1992) 34–53, DOI 10.1086/171628 | **INSPECTED (first time).** ADS scan (SHA-256 `eaa273fa5982689cd55eaba7530103e8e9d77199d4b34d3d173c1e9201075b6c`), pp. 34, 45, 47, 48 read visually: abstract, Sec. 5, Eqs. (75)–(79), (96)–(133), esp. (119)–(120) |
| [PW] | Percival & White, MNRAS 393 (2009) 297, arXiv:0808.0003v2 | full text inspected in frozen 1D-A (Secs. 2.1–2.3, Eqs. (1)–(14), Secs. 3, 6); conclusions carried forward unchanged |
| Heinesen, Blake & Wiltshire | *Quantifying the accuracy of the Alcock-Paczynski scaling of BAO measurements*, JCAP 01 (2020) 038, arXiv:1908.11508 | abstract inspected verbatim this phase; confirms scope = background/fiducial AP scaling of BAO, **not** a perturbative RSD mapping |
| Nazer & Wiltshire | *CMB anisotropies in the timescape cosmology*, Phys. Rev. D 91 (2015) 063519, arXiv:1410.3470 | abstract inspected verbatim this phase; CMB treated by **matching adapted FLRW codes** to the timescape expansion history; no Buchert-to-dressed spatial Fourier map |
| CAMB docs | camb.readthedocs.io `results` module (official) | inspected: `get_matter_power_spectrum` (`hubble_units`, `k_hunit`), `get_matter_power_interpolator`, `get_sigma8`/`get_sigma8_0` (8 h⁻¹ Mpc spheres), `get_matter_transfer_data`, multi-z output, optional halofit |
| CLASS docs | official `explanatory.ini` (lesgourg/class_public master) | inspected: `output=mPk/dTk/vTk`, `z_pk`, `P_k_max_h/Mpc` vs `P_k_max_1/Mpc`, `A_s`/`n_s` **or** `sigma8`/`S8` (shooting), `non_linear` optional |
| ADS abstract page for [DBE92] | ui.adsabs.harvard.edu | fetch returned no content (script-rendered page) — superseded by the direct scan download above |
| arxiv.org/html/2511.17160v2 | native HTML | partial (through Sec. 4.2); superseded by the local PDF |

Nothing was reconstructed from secondary summaries, blogs, or pedagogical
pages. Sources not actually inspected are marked so.

## 5. Evidence-classification policy

Every material conclusion in this report and the JSON carries exactly one
primary classification from:
`VERIFIED_FROM_PRIMARY_SOURCE`, `DERIVED_FROM_VERIFIED_DEFINITIONS`,
`NUMERICALLY_CORROBORATED`, `PROVISIONAL_MODEL_IMPORT`,
`CONVENTION_DEPENDENT`, `REQUIRES_AUTHOR_INPUT`,
`UNRESOLVED_EXTERNAL_DEPENDENCY`, `NOT_JUSTIFIED_FOR_OBSERVABLE_USE`,
`FORBIDDEN_AS_A_SILENT_DEFAULT`, `NOT_APPLICABLE`.
Each JSON conclusion object also carries source, assumptions,
derivation_summary, convention_dependencies, implementation_consequence,
and evidence_needed_to_change_status; confidence limitations are stated in
the prose. Derivations, numerical checks, and modelling assumptions are
never merged into one evidence level: where several apply, the primary one
is stated and the others listed as supporting qualifications.

## 6. Observable-chain dependency graph

The chain is audited arrow by arrow; a machine-readable node/edge graph is
in the JSON (`observable_chain`).

**Arrow 1 — validated per-mode growth → statistical matter spectrum.**
1. *Derivable now:* nothing that produces a spectrum. Per-mode signed
   growth `D(k,t)` and analytic rates exist (1D-B, frozen); the exact
   conversions `P_Δ = k_code⁴ P_δ` etc. (1D-A D2 chains) are available
   [DERIVED_FROM_VERIFIED_DEFINITIONS].
2. *External import required:* the spectrum itself (shape and amplitude)
   — [GM] defines no ensemble or spectrum anywhere (verified again this
   phase on the full text) [VERIFIED_FROM_PRIMARY_SOURCE]. Any continuous
   `P(k,z_ref)` is a PROVISIONAL_MODEL_IMPORT (Sec. 10).
3. *Unresolved convention:* F7 (meaning of the supplied k), h, spatial
   frame of the imported spectrum, Fourier normalisation.
4. *New physical derivation:* the ensemble/statistical interpretation of
   CGI perturbations on an averaged background (no primary source
   supplies it).
5. *Author input:* F7; whether the authors envisage a specific spectrum
   carrier (their conclusions sketch a BAO scheme with standard
   pre-recombination perturbations — Sec. 10).
6. *Not justified:* promoting the three equal deterministic modes to a
   spectrum or normalisation [frozen; NOT_JUSTIFIED_FOR_OBSERVABLE_USE].
7. *Conditional internal diagnostic:* per-mode growth-weighted comparisons
   at the three modes only, labelled deterministic.
8. *Comparable to observations:* nothing at this arrow.

**Arrow 2 — statistical spectrum → sigma_R / sigma_8.**
1. *Derivable now:* the σ_R integral identity (D5) and its scale-dependent
   generalisation (D7–D8) in one declared frame
   [DERIVED_FROM_VERIFIED_DEFINITIONS].
2. *External import:* the spectrum (arrow 1) and, for observational σ_8,
   the anchor/normalisation.
3. *Unresolved convention:* the k_com_D → k_com_obs spatial map (Sec. 7–8
   — **not found; missing geometric object identified**), h convention,
   matched k–R frame, F7.
4. *New derivation:* a dressed spatial Fourier construction (Sec. 8).
5. *Author input:* none specific beyond conventions; the spatial map is a
   research task, not a convention.
6. *Not justified:* observational σ_8 in any current frame; σ_R from three
   modes; upstream amplitude as normalisation.
7. *Conditional internal diagnostic:* model-internal `sigma_R_D` in the
   volume-average frame with an explicitly imported same-frame spectrum
   (Sec. 19) — internal quantity only.
8. *Comparable to observations:* nothing at this arrow.

**Arrow 3 — sigma_R/sigma_8 → density-growth derivative.**
1. *Derivable now:* under A1–A6 the identity
   `d sigma_8/d ln a = f D sigma_8(z_ref)` (Sec. 12); scale-dependent
   crossing-safe `d sigma_R/d ln a` (Sec. 18)
   [DERIVED_FROM_VERIFIED_DEFINITIONS].
2. *External import:* σ_8(z_ref) anchor (A6) — observational, ΛCDM-reduced.
3. *Unresolved convention:* growth coordinate (bare vs dressed; exact
   factor 1.084156 at t0), reference epoch/coordinate.
4. *New derivation:* none for the identity itself.
5. *Author input:* F3/F4 (they afflict the reference epoch and ICs).
6. *Not justified:* calling the result an observational quantity.
7. *Conditional internal diagnostic:* the anchored diagnostic of Sec. 13–14
   for the two scale-independent closures — the strongest legitimately
   available object.
8. *Comparable to observations:* not yet (frame + anchor caveats).

**Arrow 4 — density-growth derivative → observational RSD f-sigma-8.**
1. *Derivable now:* nothing.
2. *External import:* the whole FLRW RSD chain would have to be imported
   ([PW] assumptions) — but its applicability to Timescape is exactly what
   is unestablished.
3. *Unresolved convention:* all of Sec. 25's forks propagate in.
4. *New derivation required:* dressed redshift-space mapping, velocity
   interpretation, bias — Sec. 20–22. **This arrow is blocked by missing
   physics, not by missing conventions.**
5. *Author input:* whether any dressed perturbative light-propagation
   construction exists unpublished (Sec. 33).
6. *Not justified:* any label containing RSD or observational f-sigma-8.
7. *Conditional internal diagnostic:* none — an RSD-shaped diagnostic
   would be indistinguishable from an overclaim (Sec. 31).
8. *Comparable to observations:* nothing.

## 7. Spatial-frame and wavenumber audit

Frames and wavenumbers (frozen 1D-A definitions; JSON `spatial_frames`,
`wavenumber_definitions`):

```
k_com_D     = k_code H0_TS/c          (volume-average comoving)
k_phys_D(t) = k_com_D / a_D(t)        (volume-average physical)
k_phys0_D   = k_code H0_TS/(a_D0 c)   (present volume-average physical)
```

These are volume-average-coordinate relations. **They do not define
`k_com_obs`**, and no relation found in any inspected primary source does
(Sec. 8). The B2/F7 conversion (`paper_lcdm_hubble_k`,
factor `a_D0 h_lcdm/h_ts = 1.259551`) converts between two *numerical
conventions for the same volume-average mode* — it preserves `k_phys0_D`
and supplies no observational frame [frozen, re-verified].

Wall-comoving wavenumber: [W09] Sec. II.4 shows the wall geometry (its
Eq. (6)) "is not a global geometry" (verbatim) — wall-comoving Fourier
labels are undefined beyond finite-infinity regions
[VERIFIED_FROM_PRIMARY_SOURCE]. Reference-ΛCDM comoving wavenumber: a
different model's coordinate; usable only as an explicitly declared
fiducial import with an AP-style conversion (Sec. 23), never as a
Timescape frame.

## 8. Dressed-geometry search results

The dressed geometry was searched in [W09] (full text) and [GM] (full
text) for any construction that could supply the missing
`k_com_D → k_com_obs` map. Findings (all
VERIFIED_FROM_PRIMARY_SOURCE, verbatim):

- [W09] Eq. (22)ff: the average spherically symmetric geometry "is not a
  Lemaître–Tolman–Bondi (LTB) solution since it is not an exact solution
  of Einstein's equations, but rather of the Buchert average of the
  Einstein equations."
- [W09] Sec. II.4: "Since (6) is not a global geometry, we match (6) to
  (23) to obtain a dressed wall geometry, which is effectively the closest
  thing there is to a FLRW geometry adapted to the rods and clocks of wall
  observers. The matching is achieved in two steps. First we conformally
  match radial null geodesics of (6) and (23)…"
- [W09] on the dressed metric (26): it "extends as an average effective
  geometry … Since the geometry on cosmological scales does not have
  constant Gaussian curvature the average metric (26), like (22), is
  spherically symmetric but not homogeneous."
- [W09] contains **no** Fourier decomposition, wavenumber, power spectrum,
  or perturbation construction on the dressed geometry (checked across the
  full text).
- [GM] Sec. 5.1 uses the dressed geometry only for background
  time/redshift dressing (`1+z = a_w0/a_w = γ_w (a_D/a_w0)^{-1}`,
  `γ_w = 1+f_v/2`, dressed H0 "directly extracted by observations");
  footnote 8 defines spatial frequency space on the *volume-average*
  background 3-Laplacian only.
- Nazer & Wiltshire (2015) fit the CMB by adapting FLRW codes matched to
  the timescape expansion history — a background matching strategy, not a
  spatial perturbation map (abstract, verbatim, this phase).
- Heinesen, Blake & Wiltshire (2020) treat the accuracy of *background*
  AP/fiducial scaling of the BAO scale; not a perturbative spatial map.

**Answers to the ten questions of the specification:**

1. **Does the dressed metric define a global spatial coordinate suitable
   for Fourier decomposition?** **No.** It is spherically symmetric about
   the observer, explicitly *not homogeneous*, and not an exact solution;
   there is no constant-curvature spatial slice on which a Fourier (or
   other harmonic) basis is defined. [VERIFIED_FROM_PRIMARY_SOURCE]
2. **Is it only an effective radial/light-cone construction?** **Yes** —
   built by conformally matching radial null geodesics for a central
   observer; valid as an average effective geometry along the light cone.
   [VERIFIED_FROM_PRIMARY_SOURCE]
3. **Does the lapse/redshift relation define time and radial observables
   only, or also a spatial Fourier-coordinate transformation?** Time and
   radial (distance–redshift) observables only. No inspected primary
   source defines a spatial Fourier-coordinate transformation, and [W09]'s
   inhomogeneity statement implies none of the standard form exists.
   [VERIFIED_FROM_PRIMARY_SOURCE for the absence; the impossibility-in-
   principle of any alternative construction is not claimed]
4. **Can a constant rescaling (a_D/a_w = γ_w, γ_w0, a_D0, an H0 ratio)
   legitimately map k_com_D to k_com_obs?** **Not on current evidence.**
   No primary source derives such a rescaling for spatial harmonics. Any
   choice (e.g. multiplying k_com_D by γ_w0 or by an H0 ratio) is an
   undirected guess among inequivalent options and is classified
   NOT_JUSTIFIED_FOR_OBSERVABLE_USE as a claimed observational map; at
   most it could enter a future API as an explicitly labelled
   PROVISIONAL_MODEL_IMPORT with the alternatives reported side by side.
5. **Time/scale/direction/survey dependence of such a map:** γ_w(t) grows
   from ≈1 (early) to 1.3685 (today), so any γ_w-based rescaling is
   **time dependent**; a conformal factor is scale-independent at fixed
   time; the construction is isotropic about the observer but defined only
   along the past light cone, hence **light-cone/survey dependent**; a
   fixed-epoch constant (γ_w0) avoids time dependence only by fiat.
   [DERIVED_FROM_VERIFIED_DEFINITIONS]
6–7. **Jacobian:** see Sec. 9. A coordinate rescaling changes **both** the
   k argument and the numerical value and units of P(k); the dimensionless
   power Δ²(k) only remaps its argument.
8. **Internal pairing:** **Yes** — `k_com_D` may be paired with an
   internally defined volume-average comoving radius `R_com_D` to define a
   model-internal `sigma_R_D` (Sec. 19). [DERIVED_FROM_VERIFIED_DEFINITIONS]
9. **Naming:** `sigma_R_D_volume_average` with the radius always explicit
   (e.g. `R_com_D_over_c_H0TS`); the token `8` (or any `sigma_8`-like
   name) must never appear in the internal quantity's name (Sec. 19).
10. **Is observational R_8 = 8 h⁻¹ Mpc meaningful before a dressed
   comoving-frame mapping is established?** **No** — it names a radius in
   the observational comoving frame, which the model cannot yet reach; it
   also inherits the h fork (10.92 vs 11.87 Mpc). [frozen 1D-A,
   re-affirmed]

**Missing geometric object, stated exactly:** a derived correspondence
(diffeomorphism or statistical map) between the volume-average spatial
coordinates in which the harmonic label `k_code` lives and a homogeneous
dressed observational comoving 3-geometry, valid off the radial light
cone. [W09] states the dressed geometry is not homogeneous, so this object
does not exist in the inspected literature; producing it (or a defensible
substitute, e.g. a statistical light-cone projector) is **new theoretical
work** (Sec. 34). A time/redshift dressing must not be promoted to a
spatial Fourier map — none of the inspected sources does so, and this
audit does not either.

## 9. Coordinate/Jacobian derivations

For a constant spatial rescaling `x_new = λ x_old` of one comoving frame
(the simplest candidate form of any `k_com_D → k_com_obs` map), with the
Fourier convention of the frozen 1D-A audit:

```
k_new                = k_old / λ
delta_k_new(k_new)   = λ³ delta_k_old(λ k_new)
delta_D(k_new-k'_new)= λ³ delta_D(k_old-k'_old)
P_new(k_new)         = λ³ P_old(λ k_new)        [value and units change]
Δ²_new(k_new)        = Δ²_old(λ k_new)          [argument remaps only]
sigma_R:  R_new = R_old/λ pairs with k_new; the product k R is invariant,
          so sigma_R is invariant iff k and R are transformed together
          in the same frame — the matched-frame rule.
```

[DERIVED_FROM_VERIFIED_DEFINITIONS; dimensional bookkeeping only.]
Consequences: (i) quoting an imported spectrum "in Mpc⁻¹" is meaningless
until its frame is declared; (ii) a mismatched k–R pairing silently
rescales sigma_R by λ-dependent factors; (iii) for a *time-dependent*
λ(t) (any γ_w-based map), P acquires an extra time dependence that mixes
with growth — a further reason the map cannot be guessed.

## 10. Spectrum-shape audit

Carriers audited (none selected, none implemented):

| carrier | continuous shape? | amplitude? | native frame | native units | classification |
|---|---|---|---|---|---|
| `upstream_equal_deterministic_Delta_modes` | **no** (3 isolated modes) | deterministic comparison only | volume-average harmonic labels (F7-ambiguous) | dimensionless `k_code` | NOT_JUSTIFIED_FOR_OBSERVABLE_USE as a spectrum [frozen] |
| `external_linear_pk_at_zref` | yes | yes (calibrated) | FLRW comoving (provider's) | CAMB: k/h in Mpc⁻¹ or k in Mpc⁻¹; P in (Mpc/h)³ or Mpc³ (`hubble_units`, `k_hunit`); CLASS: `P_k_max_h/Mpc` vs `P_k_max_1/Mpc` | PROVISIONAL_MODEL_IMPORT |
| `primordial_As_ns_external_transfer` | yes | yes (predictive within the imported model) | FLRW comoving | provider transfer normalisation (CAMB `get_matter_transfer_data`; CLASS `dTk`) | PROVISIONAL_MODEL_IMPORT |

Every external carrier imports: a reference-FLRW transfer function
(baryons, radiation, neutrinos, primordial tilt and its running, BAO
wiggles) and, if `non_linear`/halofit is not explicitly disabled,
nonlinear corrections. CAMB/CLASS linear output is the only admissible
form; nonlinear output must be rejected by metadata. The h convention and
the k-unit flags are explicit provider parameters and must be captured as
metadata, never assumed.

**[GM]'s own envisaged route (verbatim, conclusions):** "Another natural
extension of this work would be the development of a consistent scheme for
the growth of BAO … As inhomogeneities remain very small in the
pre-recombination Universe, the perturbations in the dust/radiation
mixture fluid could be treated in the standard approach, with a
homogeneous background and no additional effective source. After the
transition to the matter-dominated era, the acoustic peaks in the dust
perturbations would grow in a scale-independent way, as in the ΛCDM
framework, yet with a modified growth rate … with a comoving
parametrisation of its perturbations."
[VERIFIED_FROM_PRIMARY_SOURCE.] This confirms that an
external-early-universe-shape + Timescape-growth composition is the
authors' own contemplated path — and equally that it does not exist yet.

Frame caveat applying to **all** external carriers: the provider's k is a
reference-FLRW comoving wavenumber. Declaring it equal to `k_com_D` (or to
any Timescape frame) is itself a PROVISIONAL_MODEL_IMPORT that must be a
separate explicit metadata field (`spatial_frame` + declared
identification), never implicit (Sec. 27).

**Interface input modes (design conclusion, not implemented):** a future
interface must accept **more than one explicit input mode** — dimensional
`P(k)` (with complete unit/h/frame metadata), dimensionless `Δ²(k)`, and
transfer-plus-primordial (`T(k)`, `A_s`, `n_s`, pivot) — because CAMB and
CLASS legitimately emit all three and silent conversion is where unit
errors enter; each mode must carry its own declared metadata and be
converted by tested, explicit code paths (Tier-2 round-trip tests,
Sec. 28).

## 11. Normalisation-strategy audit

| strategy | supplies | usable with clean scale-independent growth? | usable with barotropic scale-dependent growth? | needs k_com_obs map? | valid for internal sigma_R_D? | valid for observational sigma_8? | classification |
|---|---|---|---|---|---|---|---|
| `external_linear_pk_at_zref` | shape+amplitude | yes (shape then redundant for ratios) | shape required — yes formally | for observational use, yes | yes (with declared frame import) | no (frame + interpretation missing) | PROVISIONAL_MODEL_IMPORT |
| `sigma8_anchor_at_zref` | amplitude only | **yes — shape-free under strict A2** (Sec. 12) | no (scale-dependent growth needs shape) | **no** for the anchored diagnostic (A2 cancels the kernel); yes for any true σ_R | n/a (no shape) | not by itself | PROVISIONAL_MODEL_IMPORT |
| `primordial_As_ns_external_transfer` | shape+amplitude (predictive in imported model) | yes | yes formally | for observational use, yes | yes (declared frame) | no | PROVISIONAL_MODEL_IMPORT |
| `upstream_equal_deterministic_Delta_amplitude` | neither (deterministic comparison value) | — | — | — | no | **no — must be rejected by any future API** | NOT_JUSTIFIED_FOR_OBSERVABLE_USE; silent use FORBIDDEN_AS_A_SILENT_DEFAULT |

The upstream deterministic amplitude
(`Delta_d(t_i) = 0.0031427229788258105`) remains invalid as a statistical
σ_8 normalisation; no new evidence establishing an ensemble or spectrum
normalisation was found (the [GM] full text was re-searched this phase).
The classification of external anchors as "calibrated/anchored" vs
"predictive" is recorded per combination in the JSON: only
transfer+primordial is predictive *within the imported model*; a σ_8
anchor is calibration only; upstream amplitudes are comparative only.

## 12. A1–A6 scale-independent identity audit

Identity (frozen 1D-A D6, re-audited):
`sigma_8(z) = D(z; z_ref) sigma_8(z_ref)`;
`d sigma_8/d ln a = f(z) D(z; z_ref) sigma_8(z_ref)`, same a-coordinate on
both sides.

Assumption-by-assumption (full matrix per system in the JSON):

- **A1 linearity:** mathematically assumed by the frozen systems;
  *physically unverifiable at present* because the deterministic
  amplitudes carry no statistical normalisation (Sec. 17, 19 of the
  linearity audit). Classification: assumption, explicitly imported.
- **A2 scale-independent growth over the whole matched-frame kernel
  support (k-free operator AND k-independent initial mixture):**
  Mészáros — holds mathematically ([GM] (4.27) k-free); comoving — holds
  ([GM] p. 19 "the dynamics of the perturbations are independent of their
  scale"); both require the *stated* growing-mode/IC-mixture assumption
  for physical spectra. **Decisive consequence derived this phase:**
  under strict A2 the kernel weight cancels *identically* for every R and
  in every frame — `sigma_R(z) = D(z) sigma_R(z_ref)` for all R —
  therefore the anchored evolution **does not require the unresolved
  k_com_obs spatial map and does not require a spectrum shape**
  [DERIVED_FROM_VERIFIED_DEFINITIONS]. This is what makes Candidate A
  possible at all. The moment A2 is relaxed, the frame and shape blockers
  return in full.
- **A3 fixed spectrum shape at z_ref:** implied by A2 for the evolution;
  externally imported if any shape statement is made.
- **A4 one fixed frame-consistent smoothing convention:** under strict A2
  it cancels (above); it must still be *declared* because the anchor
  σ_8(z_ref) is defined by observers with a specific R_8/h convention —
  the label of the anchored quantity must carry the anchor's own
  convention metadata verbatim [CONVENTION_DEPENDENT].
- **A5 positive differentiable growth:** verified for the audited
  scenarios by the frozen 1D-B crossing machinery: Mészáros and comoving
  audited trajectories have **zero refined roots** — validity intervals
  span the whole integration domain; signed D stays positive from a
  positive reference [NUMERICALLY_CORROBORATED, frozen artifact +
  root-refined 1D-B evidence]. A5 must be re-checked per scenario, not
  assumed (the machinery exists).
- **A6 consistent external σ_8 anchor:** an import; the anchor value is
  itself a ΛCDM-pipeline-reduced observational number — its use is a
  PROVISIONAL_MODEL_IMPORT with a fiducial-reduction caveat (Sec. 23).

**Bare vs dressed derivatives:** distinct by the exact chain factor
`(2+f_v)²/(4+f_v+4f_v²)` (1.02475 at dressed z=20 → 1.084156 at t0,
full-precision 1D-B endpoint value); any anchored derivative must carry
`growth_coordinate` explicitly [frozen; CONVENTION_DEPENDENT].

**Anchor propagation without full spectrum shape:** possible **iff**
strict A2 holds (derivation above); classification
DERIVED_FROM_VERIFIED_DEFINITIONS *conditional on A2*, whose own physical
status for Timescape is the per-system question below.

## 13. Mészáros anchored-diagnostic status

- A2 mathematically satisfied; A5 corroborated (no crossings); identity
  evaluable [DERIVED + NUMERICALLY_CORROBORATED].
- **Physical applicability negative by the primary source itself:** [GM]
  p. 25: "following our discussion in Sec. 4.4, we conclude that the
  Mészáros approximation should not be applicable in the timescape
  framework" (verbatim; re-extracted this phase)
  [VERIFIED_FROM_PRIMARY_SOURCE].
- Verdict: an anchored Mészáros diagnostic is computable and may serve
  **only** as a comparison baseline (the role [GM] themselves give the
  Mészáros curve in Figs. 2/5); it must never be presented as the
  Timescape prediction. The caveat "mathematically scale-independent yet
  physically inapplicable per [GM]" must travel with every output
  [explicitly preserved, as required].

## 14. Comoving anchored-diagnostic status

- A2 satisfied ([GM] p. 19, verbatim, frozen); A5 corroborated
  (1D-B: zero crossings, whole-domain validity); identity evaluable.
- The comoving closure is the parametrisation [GM]'s own future-BAO sketch
  adopts ("with a comoving parametrisation of its perturbations",
  conclusions, verbatim) — the closest thing to an author-preferred
  scale-independent route [VERIFIED_FROM_PRIMARY_SOURCE].
- Still conditional on: A1 physical linearity (unverifiable without
  normalisation), the IC mixture assumption, F3/F4 IC forks, background
  preset, growth coordinate, and the anchor import (A6). Each is an
  explicit field of the future API; none has a default.
- Verdict: the comoving system is the **primary carrier** of any future
  conditional anchored diagnostic (Candidate A), with Mészáros retained
  as the comparison baseline.

**Proposed names and exact semantics (design, not implemented):**

- `anchored_sigma8_evolution` — the product `D(z; z_ref) · sigma8_anchor`
  under A1–A6 with declared anchor metadata; it is *an anchored evolution
  of the anchor*, not a measured σ_8(z).
- `d_sigma8_dln_a_anchored` — its exact derivative
  `f(z) D(z; z_ref) sigma8_anchor` in the declared growth coordinate; the
  name deliberately spells the derivative, not "f-sigma-8".
- `anchored_density_growth_diagnostic` — umbrella label for the pair,
  used in reporting; **recommended as the primary public name** because it
  contains neither "sigma_8(z)" nor any "f·σ8" juxtaposition and so
  cannot be misread as an RSD observable. All three names must carry the
  machine-readable caveat block (assumptions A1–A6, anchor provenance,
  coordinate, system, non-RSD statement). No name containing `fsigma8`,
  `f_sigma8`, or `RSD` is permitted for these quantities.

## 15. Scale-dependent sigma_R derivation

In one declared spatial frame X (frozen D7–D8, restated for completeness):

```
sigma_R²(z)      = ∫ dlnk Δ²_δ(k, z_ref) D²(k, z) W²(k R)
d sigma_R/d ln a = (1/sigma_R) ∫ dlnk Δ²_δ(k, z_ref) D(k,z)
                   [dD(k,z)/d ln a] W²(k R)
f_R_eff          = (1/sigma_R) d sigma_R/d ln a
```

with `W(x) = 3 j₁(x)/x` and `dD/d ln a_D = −3Z/Θ` (non-logarithmic,
finite everywhere; frozen).

**Crossing-safety (symbolic, re-verified):** the derivative integrand
contains `D·dD/d ln a`, which is finite at an individual mode's `Delta_d`
crossing (both factors finite; the *logarithmic* rate diverges but never
enters the integrand). Only `sigma_R = 0` — all weighted modes vanishing
simultaneously — would make `f_R_eff` singular.
[DERIVED_FROM_VERIFIED_DEFINITIONS; no numerical integral was evaluated.]

## 16. Barotropic continuous-k requirements

Prerequisites for any future barotropic sigma_R implementation (design
inventory; none satisfied today; JSON `barotropic_requirements`):

1. continuous spectrum at z_ref in a declared frame (PROVISIONAL import);
2. a continuous k-grid of **independently solved** barotropic
   trajectories — the frozen solver solves single modes; no interpolation
   in k is admissible without a separately validated interpolation-error
   budget, and interpolation across any k whose trajectory has a crossing
   in the evaluation window is categorically excluded (pole-adjacent
   non-smoothness);
3. convergence-tested quadrature (nested refinement, Tier 4);
4. k_min/k_max fixed by demonstrated kernel-capture convergence for the
   chosen spectrum — **never by convention** (no universal cutoff is
   invented in this audit; none exists in the sources);
5. crossing-aware treatment: root-refined crossing times per k (frozen
   1D-B machinery), with the crossing locus k ↦ t_cross(k) tabulated, and
   the derivative always via the non-logarithmic form;
6. both D3 branches side by side; both tilt labels (equivalence check);
7. explicit rate-unit/epoch/preset/F7/h/coordinate/frame choices;
8. a linearity policy (Sec. 17) and a dominated-convergence check
   (locally bounded D·D′ over the kernel support at every evaluated z);
9. finite dynamic range policy: |D| spans ≥ 10¹⁴ across 2π–10π already;
   log-domain accumulation and overflow-safe quadrature are mandatory;
10. treatment of modes leaving the declared linear regime (mask, drop, or
    flag — an explicit policy field, never silent);
11. treatment of sign-changing D within the window (signed integrand is
    well-defined; the *interpretation* of a negative-D contribution to a
    "growth" statistic must be flagged);
12. the strict rule that `d_sigma_R_dln_a` (and `f_R_eff`) are **never**
    named or reported as standard RSD f-sigma-8 [frozen naming rule].

## 17. High-k convergence and linearity blockers

Evidence assembled (all frozen or primary-source, no new numerics):

- Corrected effective sound speed is **negative throughout** the tracker
  evolution: c²_s,eff from −1/2 (early) to −0.3912 (today) (frozen 1B);
  [GM] Fig. 1 discussion (verbatim, re-extracted): "both the EoS parameter
  and the squared sound speed of the effective fluid remain negative
  throughout the evolution of the timescape model", and "in a barotropic
  perturbation picture the effective fluid does not suppress structure
  formation on small scales; rather, it leads to the development of
  instabilities" [VERIFIED_FROM_PRIMARY_SOURCE].
- The barotropic coupling scales as `A34·A43 = −c_s²k_code²/a_D² > 0` for
  c_s² < 0 (frozen 1C-A): the instability growth rate increases without
  bound with k on **both** D3 branches.
- Frozen 1D-B endpoints (baseline conventions, printed_4_15):
  relative growth +4.73 / −2.6e4 / −5.2e14 at 2π/5π/10π — super-polynomial
  k-growth over a factor 5 in k [NUMERICALLY_CORROBORATED].
- [GM] conclusions (verbatim): sub-horizon growth "appears too fast to be
  reasonably compatible with the observed structure formation in our
  Universe, and even more unphysical reversals in the density contrast
  sign over time occur in many cases"; and "the even faster growth of the
  effective fluid perturbations at sub-horizon scales would lead to the
  unexpected departure of the system from the linear regime while the dust
  perturbations are still very small" [VERIFIED_FROM_PRIMARY_SOURCE].

**Consequence for the sigma_R integral** [DERIVED, from the above]: with
|D(k,z0)|² growing faster than any power of k across the audited range, a
sigma_R integral against any standard damped linear spectrum is either
(i) divergent as k_max → ∞, or (ii) dominated by the numerical cutoff, or
(iii) dominated by modes that have already left the linear regime by
[GM]'s own assessment. No primary source supplies a physical cutoff or a
validity criterion. **Classification: UNRESOLVED — a barotropic sigma_R,D
is undefined without new physical regularisation**, and no universal
high-k cutoff is invented here. The three modes {2π, 5π, 10π} are never
interpolated into a spectrum or used as a quadrature rule [frozen].

Definitional ladder (required distinctions, JSON `linearity_ladder`):
**linear equations** (frozen systems are linear ODEs — true by
construction) ≠ **numerically converged solutions** (1C-B2/1D-B
convergence evidence — established) ≠ **perturbations remaining in the
linear-amplitude regime** (requires a normalisation — *not establishable
now*) ≠ **physically plausible structure growth** ([GM] answers negatively
for barotropic sub-horizon) ≠ **observational validity** (requires the
whole of Secs. 20–23 in addition). A quantitative linearity criterion:
for `delta_m` per mode, `|delta_m,k| ≪ 1` is meaningful **only** once an
absolute normalisation exists; for `Delta_d` no `|Delta_d| ≪ 1` criterion
may be imposed without derivation — `Delta_d,k = −k_code² delta_m,k`
makes any fixed `|Delta_d|` threshold scale-dependent by k² [DERIVED]; for
relative growth, no amplitude criterion applies at all; for the
effective-fluid variables, [GM]'s linear-departure warning applies first;
for extreme barotropic trajectories the mathematical solution exists but
the linear-amplitude and physical-validity levels fail on [GM]'s own
assessment. The missing information for an absolute mask is exactly: a
statistical normalisation (spectrum/anchor) plus the spatial-frame scale
assignment. **Validity-mask design** (not implemented): a per-(k, t)
five-level mask — `numerical_validity` (solver/convergence),
`equation_linearisation_validity` (first-order scheme),
`amplitude_normalisation_validity` (requires declared normalisation;
threshold and its provenance explicit), `physical_model_validity`
(closure-level flags, e.g. [GM] barotropic sub-horizon negative),
`observational_validity` (blocked pending Secs. 20–23) — each level
independently reported, never collapsed into one boolean.

## 18. Crossing-safe sigma derivative

Restating the implementable rule (design): all sigma-level derivatives use
the **non-logarithmic** integrand `D·(dD/d ln a) = −3 D Z/Θ` (bare) or its
dressed counterpart; per-mode logarithmic rates are reported only per
validity interval (frozen 1D-B piecewise policy); no interpolation through
a pole; the crossing locus in k is tabulated, not smoothed over.
`f_R_eff` inherits singularity only from `sigma_R → 0`, which the Tier-4
diagnostics must detect and report as an undefined point, never bridge.

## 19. Internal sigma_R,D versus observational sigma_8

The only sigma-like quantity definable without the missing spatial map is
the **model-internal** volume-average-frame variance
`sigma_R_D_volume_average`: (D5) evaluated with `k_com_D` and `R_com_D` in
the volume-average frame, from an explicitly imported spectrum *declared*
(as a PROVISIONAL_MODEL_IMPORT) to live in that frame. Its naming rules:
the frame token `_D_volume_average` is mandatory; the radius is an
explicit dimensional argument; the strings `sigma_8`, `sigma8`, `8hMpc`
(any spelling of the observational quantity) are forbidden in its name and
labels; every output carries `frame: volume_average` metadata and the
declared-import provenance. It is not comparable to observational σ_8 and
any comparison attempt must be rejected at the API level (Sec. 27).
Observational σ_8 additionally requires: the k_com_obs map (missing —
Sec. 8), the h convention, the anchor/spectrum in the observational frame,
and the fiducial-reduction caveat (Sec. 23). Classification: internal
quantity DERIVED_FROM_VERIFIED_DEFINITIONS conditional on the declared
import; observational σ_8 NOT_JUSTIFIED_FOR_OBSERVABLE_USE at present.

## 20. RSD and velocity interpretation

Exact local relations (frozen): `Z_k = −k_code² (δΘ)_k`;
`delta_m_dot = −δΘ` (CGI dust continuity). Link-by-link classification of
the chain from these variables to an RSD-inferred velocity-growth
combination (JSON `rsd_links`):

1. **dust-congruence expansion perturbation** (δΘ): exactly defined and
   solved [VERIFIED/DERIVED — available].
2. **peculiar-velocity divergence in a chosen effective background:**
   requires declaring an effective background flow off the dust
   congruence; no primary source defines one for Timescape
   [UNRESOLVED_EXTERNAL_DEPENDENCY].
3. **galaxy velocity:** requires a galaxy formation/selection model on the
   averaged background [UNRESOLVED_EXTERNAL_DEPENDENCY].
4. **velocity bias:** [PW] Eq. (11) *assumes* none; for Timescape even the
   unbiased statement is undefined until link 2 exists
   [NOT_JUSTIFIED_FOR_OBSERVABLE_USE as an assumption import].
5. **galaxy density bias:** [PW] Eqs. (9)–(10) linear deterministic bias
   is an FLRW-model assumption; a Timescape counterpart would need the
   averaging-consistent definition of the galaxy field
   [UNRESOLVED_EXTERNAL_DEPENDENCY].
6. **real-to-redshift-space coordinate mapping:** [PW] Eqs. (1)–(4) derive
   it in FLRW with the distant-observer approximation; the Timescape
   analogue requires perturbed light propagation on the dressed geometry,
   which no inspected source derives ([W09] is background-only; [GM] does
   not treat light propagation) [UNRESOLVED_EXTERNAL_DEPENDENCY — the
   central missing piece].
7. **line-of-sight/distant-observer approximation:** definable only after
   link 6 exists [NOT_APPLICABLE yet].
8. **dressed clock and H normalisation:** available and exact (frozen
   chain factor; dressed H_dressed = γ_w H_D − γ̇_w)
   [DERIVED_FROM_VERIFIED_DEFINITIONS] — necessary but far from
   sufficient.
9. **dressed light propagation:** background distance–redshift exists
   ([W09], validated 1B); *perturbed* dressed light propagation does not
   [UNRESOLVED_EXTERNAL_DEPENDENCY].
10. **AP/fiducial-cosmology conversion:** Heinesen–Blake–Wiltshire (2020)
    treat exactly this for the BAO *background* scale and quantify ~1%
    systematics when the true model is far from the fiducial; they do not
    supply a perturbative RSD conversion [VERIFIED_FROM_PRIMARY_SOURCE
    for scope; the RSD-level conversion remains
    UNRESOLVED_EXTERNAL_DEPENDENCY].
11. **survey window and estimator dependence:** survey-specific import;
    meaningful only after links 6–10 [NOT_APPLICABLE yet].
12. **nonlinear and scale cuts:** [PW] Sec. 6 cuts are estimator-specific
    (frozen 1D-A withdrawal of any universal range); Timescape cuts
    additionally undefined pending the linearity normalisation (Sec. 17)
    [UNRESOLVED].

**Timescape literature search result:** no dressed RSD, peculiar-velocity,
redshift-space, or survey-observable perturbation construction exists in
any inspected primary source ([W09]: background dressed observables only;
Nazer–Wiltshire 2015: matched-FLRW CMB spectra, background matching only;
Heinesen–Blake–Wiltshire 2020: background AP/BAO scaling only; [GM]: no
RSD, fσ8 named only as future work). Per-source supply matrix in the JSON
(`rsd_source_supply`): each provides a background distance–redshift
relation at most; none provides a real-space spatial map, perturbative
velocity map, RSD Jacobian, bias prescription, or survey-fiducial
conversion at perturbation level. Successful Timescape background fits
(SNe, BAO, CMB) are explicitly **not** treated as evidence of a
perturbative RSD mapping.

**Label ranking (most → least defensible):**
1. `density_growth_derivative` — justified now (exact mathematics).
2. `anchored_density_growth_diagnostic` — justified as a conditional
   diagnostic (A1–A6 + anchor + naming rules).
3. `theoretical_f_sigma8` — **not presently justified**: "σ_8" itself is
   frame-blocked and the name invites RSD reading.
4. `observational_f_sigma8` — not justified (missing links 2–12).
5. `RSD_prediction` — not justified (same, and additionally an explicit
   overclaim). Identical algebraic units or notation confer **no**
   observational status [rule preserved].

## 21. Bias and velocity-bias requirements

Any future observational comparison requires, as separate explicit model
imports with their own provenance: a galaxy density-bias model defined
against the averaged dust density `⟨ϱ_d⟩_D` (the [GM]-consistent
reference; [GM] Sec. 5.2.2 criticises perturbations defined against other
densities — verbatim quote in the JSON), and a velocity-bias statement
relative to the (currently undefined) Timescape velocity observable.
Both are UNRESOLVED_EXTERNAL_DEPENDENCY; neither may be silently set to
"unbiased".

## 22. Dressed redshift-space mapping status

**Not found; not derivable from current evidence** (Secs. 8, 20 links 6
and 9). The missing derivation, stated exactly: linear perturbations of
the dressed light-propagation/redshift relation about the timescape
background — i.e. the Timescape analogue of the FLRW redshift-space
Jacobian [PW] Eqs. (1)–(4) — including the peculiar-expansion
contribution of δΘ along the line of sight in the dressed frame, with the
bare/dressed clock choice made explicit. This is new theoretical work
(Sec. 34), not a convention choice. Any interim use of the FLRW Jacobian
with Timescape growth would be a PROVISIONAL_MODEL_IMPORT of the central
contested physics and is NOT_JUSTIFIED_FOR_OBSERVABLE_USE as a Timescape
prediction.

## 23. Survey fiducial/AP requirements

Observed RSD f-sigma-8 points are produced inside survey pipelines that
assume a fiducial FLRW cosmology for coordinates, distances, and the
template spectrum. Comparing any future Timescape quantity to them
requires: (i) an AP-style re-scaling consistent with the dressed
distance–redshift relation (background part exists: [W09]/1B); (ii) an
assessment of the template/estimator dependence (Heinesen–Blake–Wiltshire
2020 show ~1% BAO-scale systematics from AP scaling alone when models
differ strongly — a warning, verbatim abstract in the JSON, that
"caution must be taken with the error budget when extrapolating" fiducial
results); (iii) the σ_8 convention embedded in the survey's reported
fσ8. All three are explicit import steps in the future API
(`survey_fiducial_mapping`), never silent. Classification:
background-level conversion PROVISIONAL_MODEL_IMPORT once specified;
perturbation-level conversion UNRESOLVED_EXTERNAL_DEPENDENCY.

## 24. D3 original-source investigation

**Access outcome.** Both 1992 primary sources were obtained and genuinely
inspected for the first time in this project (Sec. 4: ADS scans rendered
to page images; SHA-256 hashes recorded; image-only scans — no text layer
— read visually page by page).

**Notation mapping (recorded in JSON `d3_notation_map`).** [DBE92]
`𝒟_a^((i))` (comoving fractional density gradient) ↔ [GM] `D_µ^(i)`;
[DBE92] `𝒵_a = aZ_a`, `Z_a = h_a^b Θ_;b` ↔ [GM] `Z_µ = aD_µΘ` and scalar
`𝒵`; [DBE92] `c_s² = ṗ/µ̇` (p. 58, verbatim) ↔ [GM] (4.13) c²_s(eff)
"equivalently as ∂p/∂ρ or as ṗ/ρ̇" — identical; [DBE92] `Θ = 3H`;
[DBE92] perfect-fluid `Ψ_a^{(i)} = V_a^{(i)}` and
`F_a^{(i)} = Ψ̇_a^{(i)} − (3c²_{s(i)} − 1)HΨ_a^{(i)}` ↔ [GM] (2.20)
`F^{(i)} ≃ V̇^{(i)} + (1/3 − c²_{s(i)})ΘV^{(i)}` — identical after
Θ = 3H. The Θ-self-coupling term contains no Laplacian, so the
Laplacian-sign convention does not enter the D3 comparison; both papers
use the same continuity/expansion sign conventions (μ̇ = −3H(μ+p)-type).

**Equations inspected (visual, verbatim structure):**

- [DBE92] (32) total fluid: `𝒟̇_a − 3Hw𝒟_a + (1+w)𝒵_a = …` —
  self-coupling `+3Hw = wΘ`, c_s² absent from it.
- [DBE92] (46) component, total-matter frame, interactions general:
  `𝒟̇_a^{(i)} − 3Hw_{(i)}𝒟_a^{(i)} + (1+w_{(i)})𝒵_a
  = 3a(1+w_{(i)})H(F_a^{(i)}+Π_a^{(i)}) − a(1+w_{(i)})∇∇Ψ^{(i)} + …` —
  self-coupling `w_iΘ`, with c²_{s(i)} inside `F^{(i)}`.
- [DBE92] (49)/(55) "useful form" (55 = no interactions): the same
  equation after eliminating `F^{(i)}` via the momentum equations
  (29)+(43)/(54): `𝒟̇_a^{(i)} − 3(w_{(i)} − c²_{s(i)})H𝒟_a^{(i)}
  + (1+w_{(i)})𝒵_a = …` — **self-coupling `(w_i − c²_{s,i})Θ`.**
- [GM] (2.22) (p. 9, visual): `Δ̇^{(i)} − w_{(i)}ΘΔ^{(i)} + (1+w_{(i)})𝒵
  − aΘ(1+w_{(i)})F^{(i)} + a(1+w_{(i)})⁽³⁾ΔV^{(i)} ≃ 0`, introduced as
  "the system of ordinary differential equations (ODEs) which we will
  employ in this work [50]" — **a faithful scalarization of [DBE92]
  (46)** term by term (self-coupling `w_iΘ`; F-term `aΘ(1+w_i)F^{(i)}` ↔
  `3aH(1+w_i)F^{(i)}`; tilt-Laplacian term matching; perfect fluid,
  no interactions).
- [GM] (4.10) (dust frame, frequency space, visual):
  `Δ̇^{(eff)} − w_{(eff)}ΘΔ^{(eff)} + (1+w_{(eff)})𝒵 + Θ𝒫̃^{(eff)}
  − (k²/a)Ṽ^{(eff)} ≃ 0`.
- [GM] (4.13) (visual): `𝒫̃^{(eff)} = c²_{s(eff)}Δ^{(eff)}`, stated to
  hold "in any observer frame n^µ".
- [GM] (4.15) as printed (visual): `Δ̇^{(eff)} − (w_{(eff)} +
  c²_{s(eff)})ΘΔ^{(eff)} + (1+w_{(eff)})𝒵 − (k²/a)Ṽ^{(eff)} ≃ 0`.

**Pressure-term sign derivation and symbolic checks** (scratchpad
`phase1dc_d3_symbolic.py`, all PASS, transcript in the JSON):

1. (4.10)+(4.13) ⇒ self-coupling `(w_eff − c²_s)Θ` — the `derived_4_10`
   branch (re-derivation of the 1C-A confirmed inconsistency from
   visually transcribed equations).
2. printed (4.15) − derived form = `+2c²_sΘΔ^{(eff)}` exactly.
3. [DBE92] (46)+(54) with a barotropic non-interacting component
   (entropy perturbations zero) ⇒ self-coupling `3H(w_i − c²_{s,i})
   = (w_i − c²_{s,i})Θ` — reproducing [DBE92] (55) as printed: the
   original source's own reduction generates the **minus** combination.
4. No inspected [DBE92] reduction generates a `(w_i + c²_{s,i})`
   combination.

**Verdict on the specification's menu** (supports `printed_4_15`,
`derived_4_10`, neither, or an inapplicable convention): the inspected
original source **structurally supports the `derived_4_10` combination**
— its own barotropic reduction produces `(w − c_s²)Θ`, its general
equation matches [GM] (2.22) from which `derived_4_10` follows, and no
`(w + c_s²)Θ` structure appears anywhere in the inspected pages. A
plausible mechanical origin of the printed form — collecting
`−wΘΔ + Θc_s²Δ` as if both carried the same sign — is noted as a
hypothesis, not a fact.

**Why D3 is nonetheless NOT declared resolved.** The task bar requires a
*complete unambiguous convention mapping*. Two gaps remain: (i) [DBE92]'s
component equations are written in the **total-matter rest frame**
(u^a = u_N^a), while [GM] Sec. 4 works in the **dust energy frame** with
the geodesic relation 𝒫 + aF = 0; the full frame transformation of
[DBE92] (46)/(54) into [GM]'s dust-frame two-fluid system (which can
reshuffle c_s²-terms between the density and tilt rows) was **not**
executed; (ii) [DBE92] does not print [GM]'s specific dust+effective
two-fluid barotropic system, so the comparison is structural, not verbatim.
Accordingly: **both branches remain mandatory**; the issue remains
UNRESOLVED (primary classification REQUIRES_AUTHOR_INPUT, with the formal
frame-mapping derivation listed as the alternative adjudication path in
Sec. 34). No Phase 1C or 1D-B code was changed; no branch is called
correct, canonical, preferred, physical, recommended, intended, or
default anywhere.

**Original CGI attribution ([GM 48]) — resolved.** [BDE92] was inspected:
its abstract states the covariant variables are expanded "recovering
Bardeen's variables as first-order terms … thus the two sets of variables
are equivalent to first order", and § 5.2.3, Eqs. (119)–(120) (p. 48,
visual) print the scalar-harmonic expansion
`𝒟_α = aε_m|α − 3a′(1+w)V_Cα = −k a ε_m(η)Y_α^{(0)} − 3a′(1+w)V_C(η)Y_α^{(1)}`
— the density-gradient's scalar-harmonic coefficient is proportional to
Bardeen's gauge-invariant matter-frame density contrast ε_m. The 1D-A
item "attribution to [GM 48] not independently inspected"
(UNRESOLVED_EXTERNAL_DEPENDENCY) is hereby upgraded to
**VERIFIED_FROM_PRIMARY_SOURCE**. [DBE92]'s abstract adds the multifluid
statement ("equivalent to those of Bardeen and of Kodama and Sasaki").
This changes an attribution footnote only; no frozen equation or code is
affected.

## 25. F3/F4/F7 propagation

Dependency graph (full adjacency matrix in the JSON,
`propagation_graph`, with per-edge effect class ∈ {cancels, amplitude,
shape, physical_scale, time_evolution, interpretation}):

| choice | per-mode D | per-mode f | mapped δ_m | spectrum shape | spectrum amplitude | sigma_R | sigma_8 | dσ_R/dln a | anchored diagnostic | RSD interpretation | likelihood comparability |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D3 branch | yes (t-evol; sign reversals) | yes (poles move) | yes | yes (via D(k)) | yes | yes | yes | yes | no (clean systems: not applicable — must be passed `not_applicable`) | yes (if ever reached) | yes |
| F3 rate units | yes (amplitude+phase) | yes | yes | yes (k-dependent systems) | yes | yes | yes | yes | yes (via D) | yes | yes |
| F4 epoch | yes | yes | yes | yes | yes | yes | yes | yes | yes (also afflicts z_ref) | yes | yes |
| F7 wavenumber | barotropic only (dominant high-k) | yes | yes (k_code value) | yes (physical scale of every k) | no (per-mode) | yes (kernel placement) | yes | yes | **cancels under strict A2** | yes | yes |
| background preset | yes (small: −0.042 % G_end) | yes | yes — affects per-mode time evolution of the mapped values through Δ_d (the −1/k_code² conversion factor itself is preset-invariant) | yes | yes | yes | yes | yes | yes | yes | yes |
| tilt representation | **cancels** (≤3e−14 %) | cancels | cancels | cancels | cancels | cancels | cancels | cancels | not applicable | cancels | cancels |
| growth coordinate | no (history invariant) | amplitude ×1.025–1.084156 | no | no | no | no | no | amplitude | amplitude | interpretation | yes |
| h convention | no | no | no | no (if k in matched h units) | amplitude/units | physical scale of R | yes | yes | anchor metadata only (A2) | yes | yes |
| spatial frame | no | no | no (label metadata) | argument remap + value (Sec. 9) | yes | yes | yes | yes | **cancels under strict A2** | yes | yes |
| spectrum source | no | no | no | yes (all) | yes | yes | yes | yes | no (anchor-only path) | yes | yes |
| normalisation strategy | no | no | no | no | yes | yes (amplitude) | yes | yes | yes (anchor value) | yes | yes |

Distinctions honoured: algebraically cancelling (tilt form everywhere;
F7/frame/h inside the strict-A2 anchored diagnostic; growth-history
invariance under the coordinate choice), amplitude-only (growth
coordinate on f; normalisation), shape (spectrum source; D(k) forks),
physical scale (F7, h, frame on kernel placement), time evolution (D3,
F3, F4, preset), observable interpretation (coordinate, frame, RSD).
Frozen 1D-B one-factor magnitudes are carried in the JSON (signed deltas;
the D3 delta −230.2 % spans a sign reversal and the F7 delta flips the
rate sign — convention spreads, never confidence intervals; rule
re-affirmed).

## 26. Complete future scenario inventory

The eleven 1D-A/1D-B scenario dimensions persist unchanged (JSON carries
the full field-by-field record): `perturbation_system`,
`background_preset`, `d3_branch`, `tilt_form`, `rate_unit_convention`,
`epoch_choice`, `wavenumber_convention`, `growth_coordinate`,
`density_contrast_mapping`, `initial_spectrum_model`,
`normalization_strategy`, `sigma_radius_h_convention` — now extended by
the new Phase 1D-C dimensions: `spatial_frame`, `spectrum_input_kind`,
`smoothing_radius_definition`, `growth_reference` (value + coordinate),
`linearity_policy`, `rsd_interpretation`, `bias_model`,
`survey_fiducial_mapping`, `observable_target`. Every field is
mandatory-explicit; `not_applicable` must be passed explicitly wherever
marked; **no field has a default** [FORBIDDEN_AS_A_SILENT_DEFAULT
applies to any silent choice].

## 27. Proposed no-default API

Design only (nothing implemented; no placeholder created). One frozen
construction object (e.g. `ObservableClosureSpec`) validated exhaustively
at construction time; all fields mandatory; scientific status and
required metadata per field; serialization = flat JSON of explicit labels
plus provenance blocks. The complete per-field table (allowed labels,
applicability by target/system, incompatibility rules, explicit
`not_applicable` requirements, scientific status, metadata, serialization,
source, tests) is in the JSON (`api_design`). Field list:
`observable_target` ∈ {`per_mode_growth`, `anchored_density_growth_diagnostic`,
`internal_sigma_R_D_volume_average`, `barotropic_sigma_R_D_weighted_growth`,
`observational_sigma8`, `rsd_fsigma8`} (the last two constructible only in
rejected/blocked state — they exist as labels precisely so the
incompatibility engine can name what it refuses);
`perturbation_system`; `background_preset`; `d3_branch`; `tilt_form`;
`rate_unit_convention`; `epoch_choice`; `wavenumber_convention`;
`growth_coordinate`; `density_contrast_mapping`; `spatial_frame` ∈
{`volume_average_D`, `dressed_observational` (blocked), `wall` (blocked),
`reference_lcdm_fiducial_import`, `not_applicable`}; `spectrum_input_kind`
∈ {`dimensional_pk`, `dimensionless_delta2`, `transfer_plus_primordial`,
`sigma8_anchor_only`, `not_applicable`}; `normalization_strategy`;
`sigma_radius_h_convention`; `smoothing_radius_definition` (dimensional
radius + declared frame + h pairing); `growth_reference` (epoch value +
coordinate label); `linearity_policy` (five-level mask policy of Sec. 17);
`rsd_interpretation` ∈ {`none_density_statistic_only`,
`blocked_missing_dressed_mapping`} (no affirmative value exists);
`bias_model` ∈ {`not_applicable`, `blocked_undefined_for_timescape`};
`survey_fiducial_mapping` ∈ {`not_applicable`,
`blocked_background_only_evidence`}.

**Mandatory construction-time rejections** (denied-combination matrix in
the JSON; each with a tested error message):

1. `normalization_strategy = upstream_equal_deterministic_Delta_amplitude`
   with any sigma-level target;
2. `initial_spectrum_model = upstream_equal_deterministic_Delta_modes`
   presented as a continuous spectrum (any sigma_R target);
3. mismatched k and R spatial frames (frame tokens must be equal);
4. `observable_target = observational_sigma8` without
   `spatial_frame = dressed_observational` **and** since that frame is
   blocked, the target is constructible only as an explicit
   blocked-status object — i.e. observational σ_8 without dressed-frame
   metadata can never be built;
5. barotropic sigma_R without `spectrum_input_kind` supplying a continuous
   shape **and** a continuous-k solver domain declaration;
6. any scale-dependent weighted growth labelled with a standard
   f-sigma-8 name (`f_sigma8`, `fsigma8`, `fσ8` are reserved-rejected
   tokens for those targets);
7. any RSD-labelled output while `rsd_interpretation` has no validated
   affirmative value (permanently rejected until a derived mapping
   exists);
8. any request naming a single canonical/preferred/default D3 branch
   (both-branch execution is the only mode for barotropic targets);
9. silent h, coordinate, epoch, or H0 choices (absence of any mandatory
   field is a constructor error, not a warning);
10. interpolation through a logarithmic pole (crossing-interval metadata
    make pole-crossing interpolation requests detectable and rejected);
11. any D2-corrupted sound-speed path (no such input exists in the
    package; the label is reserved-rejected defensively).

Tests needed (Tier 1/2 of Sec. 28): one rejection test per rule, one
acceptance test per legitimately constructible target, serialization
round-trips, and metadata-completeness checks.

## 28. Validation blueprint

Tiered plan (design only; nothing executed):

**Tier 1 — algebra and units:** top-hat window limits (W(0)=1, series
and large-x tail); Fourier normalisation self-consistency; P(k)
dimensional units and the `(Mpc/h)³ ↔ Mpc³` conversions; `P ↔ Δ²`
round trip; matched k–R reciprocal-unit checks; the Sec. 9 rescaling
Jacobians (P value/argument, Δ² argument-only, σ_R invariance under
matched transformation); σ_R positivity; the A1–A6 identity on synthetic
k-independent growth; the scale-dependent derivative identity on
synthetic D(k,z); invariance under a constant harmonic sign flip.

**Tier 2 — imported spectrum:** schema/metadata validation (units, h,
frame declaration, linear-only, provider provenance, redshift grid);
`P(k)` vs `Δ²(k)` vs transfer+primordial round trips; h-unit conversion
tests against provider documentation values; interpolation-error
convergence on refined provider grids; extrapolation rejected without an
explicit policy object; shape/amplitude separation (rescaling amplitude
must not move shape diagnostics).

**Tier 3 — clean-system anchored diagnostic:** Mészáros and comoving
separately; both growth coordinates (exact chain-factor test at multiple
epochs); multiple explicit anchors (value/provenance variations);
analytic-derivative identity `d/dln a [D σ8] = f D σ8` to solver
tolerance; reference-epoch consistency (change z_ref with compensating
anchor — invariance); **no spectrum dependency** when using a pure
sigma8 anchor (injecting different declared shapes must change nothing);
explicit non-RSD naming asserted in outputs (name/metadata tests).

**Tier 4 — scale-dependent internal sigma_R,D (if ever unblocked):**
independent solve at every k (no k-interpolation baseline); k-grid
refinement convergence; quadrature-rule refinement; k-domain expansion
until kernel capture is demonstrated **or divergence is exhibited and
reported** (cutoff-dominance diagnostic: dσ_R/dk_max); crossing-aware
non-logarithmic derivative (crossing-locus tabulation test); D3
side-by-side (both branches always); tilt equivalence (≤ numerical
noise); dominated-convergence diagnostics (bounded D·D′ on the support);
linear-validity mask attached to every output (five levels of Sec. 17).

**Tier 5 — observational/RSD layer: BLOCKED.** It remains blocked unless
a future audit verifies a derived dressed redshift-space mapping. Exact
tests that would then become necessary: perturbed dressed
light-propagation consistency (redshift-space Jacobian vs the derived
mapping); velocity-observable identification tests (δΘ → mapped velocity
divergence in the derived frame); bias-model injection/recovery;
AP/fiducial round-trip against synthetic surveys with a known truth;
window/estimator convolution tests; scale-cut sensitivity; end-to-end
comparison against a published fσ8 point *only* after all of the above.

**Numerical-error separation (mandatory in all tiers):** solver error
(tolerance/method deltas) vs k-grid error vs quadrature error vs
spectrum-source uncertainty (provider/version deltas) vs normalisation
uncertainty (anchor variations) vs unresolved-convention spread (D3,
F3, F4, F7, h, coordinate, frame — reported as spreads, never
confidence intervals) vs closure/model dependence (Mészáros vs comoving
vs barotropic) vs observational-systematics uncertainty (survey-side;
Tier 5 only).

## 29. Uncertainty taxonomy

Eight separated classes, extending the frozen 1D-B taxonomy (JSON
`uncertainty_taxonomy`): (1) numerical sampling/quadrature; (2) solver
method/tolerance; (3) k-grid/domain (new, Tier 4); (4) spectrum-source
(provider shape/version); (5) normalisation/anchor; (6) unresolved
convention spread — **a convention or model spread, never a statistical
confidence interval** (rule preserved verbatim); (7) closure/model
dependence; (8) observational systematics (blocked with Tier 5). Every
future reported number must name which classes its error bars contain.

## 30. Candidate-phase readiness matrix

| candidate | scope | primary verdict | other blockers |
|---|---|---|---|
| **A** | conditional anchored sigma8 evolution + density-growth derivative, scale-independent systems only | **GO_ONLY_AS_CONDITIONAL_DIAGNOSTIC** | anchor import (A6); F3/F4 forks propagate; Mészáros physical-inapplicability caveat mandatory; naming rules of Sec. 14 mandatory |
| **B** | model-internal volume-average sigma_R,D from an external same-frame spectrum | **BLOCKED_BY_EXTERNAL_INPUT** | no provider emits a volume-average-frame spectrum: the frame declaration is itself a PROVISIONAL_MODEL_IMPORT; if explicitly declared, could run as GO_ONLY_AS_INTERNAL_MODEL_QUANTITY |
| **C** | scale-dependent barotropic sigma_R,D + weighted growth, continuous k | **BLOCKED_BY_LINEARITY_OR_K_DOMAIN** | also BLOCKED_BY_EXTERNAL_INPUT (spectrum); D3 dual-branch spread; [GM]'s own unphysicality assessment |
| **D** | observational dressed sigma_8 | **BLOCKED_BY_MISSING_SPATIAL_MAP** | also external spectrum/anchor; h convention |
| **E** | RSD-comparable observational f-sigma-8 | **BLOCKED_BY_MISSING_RSD_MAPPING** | also spatial map, normalisation, bias, fiducial |

## 31. Minimal scientifically defensible next phase

**Recommendation: a small Phase 1D-D implementing Candidate A only**, as
`anchored_density_growth_diagnostic` (Sec. 14 names and caveat blocks),
for the comoving system as primary carrier and Mészáros as the
[GM]-sanctioned comparison baseline, both growth coordinates, explicit
anchors, full A1–A6 caveat propagation, plus the Sec. 27 rejection rules
for everything else — **and, in parallel as pure theory (no code), the
formal D3 frame-mapping derivation of Sec. 34** (the cheapest path to
retiring the largest outstanding equation-level ambiguity).

Candidate A was **not** assumed to be next; the risk assessment was
performed: the diagnostic's value (first Timescape-growth quantity with
observational units, exact identity, both coordinates, anchor-explicit)
outweighs the misreading risk **only** because the Sec. 14/27 naming and
rejection rules make an RSD misreading structurally difficult (no
`fsigma8` token can appear; caveat block travels with every output; the
Mészáros caveat is mandatory). Without those rules the risk assessment
would reverse, since an "fσ8-shaped" number would predictably be quoted
as a Timescape RSD prediction, which the evidence does not support.

## 32. Explicit no-go list

Not to be implemented in any next phase (re-affirmed, with this phase's
evidence): observational σ_8 or σ_R (missing spatial map + spectrum);
any barotropic σ-level quantity (Sec. 17 blockers); any f-sigma-8-named
output for any system; any RSD/Kaiser mapping, bias model, or velocity
identification; any AP/fiducial data conversion; any likelihood,
covariance, or fit; any spectrum reader/transfer wrapper/CAMB/CLASS
integration *ahead of* the phase that legitimately needs it (Candidate B
at the earliest); any k-interpolation of the three deterministic modes;
any use of the upstream deterministic amplitude as a normalisation; any
adjudicated/canonical D3 branch; any D2-corrupted path.

## 33. Questions requiring author input

1. **D3:** In Eq. (4.15) of arXiv:2511.17160v2, the Δ^(eff)
   self-coupling reads −(w_eff + c²_s,eff)ΘΔ^(eff), while substituting
   the closure (4.13) into Eq. (4.10) yields −(w_eff − c²_s,eff)ΘΔ^(eff);
   Dunsby–Bruni–Ellis (1992), Eqs. (49)/(55), likewise produce the
   (w − c²_s) combination in their own frame. Which sign is intended, and
   is (4.15) as printed the equation actually used in the published
   figures? (The pinned notebooks implement the printed form.)
2. **F3:** in "Z(t_i) ≈ −0.16 H0", which H0 (dressed 73.03/73.23 vs bare
   H_D,0 ≈ 58.01 km/s/Mpc) is intended?
3. **F4:** is the initial epoch 0.218 Gyr or dressed z = 20
   (0.19621 Gyr), and what generated the 0.218 value?
4. **F7:** are the published k values {2π, 5π, 10π} matrix labels in the
   timescape code units or ΛCDM-Hubble-length labels per the Fig. 3
   caption?
5. **Spatial map:** do the authors envisage any definite correspondence
   between the volume-average harmonic wavenumber and an
   observational/dressed comoving wavenumber (e.g. for their planned BAO
   scheme), or is that construction acknowledged as open?
6. **RSD:** does any unpublished dressed perturbative light-propagation /
   redshift-space construction exist for timescape-type averaged models?
7. **Linearity:** what amplitude normalisation (if any) do the authors
   regard as physical for the Fig. 2–3 trajectories, given the
   linear-departure warning in their conclusions?

(No author contact was made in this phase.)

## 34. Questions requiring new theoretical work

1. The **dressed spatial Fourier correspondence**: construct (or prove
   impossible) a map from volume-average harmonic coordinates to a
   homogeneous dressed observational comoving 3-geometry valid off the
   light cone — or a statistical light-cone substitute adequate for
   window-function integrals (Sec. 8).
2. The **D3 formal frame mapping**: transform [DBE92] (46)+(54) from the
   total-matter frame to the dust energy frame for the dust+effective
   two-fluid system and reduce with the barotropic closure, tracking
   every sign — a finite, well-posed calculation that would adjudicate
   D3 without author input (Sec. 24).
3. The **dressed redshift-space Jacobian**: perturbed light propagation
   on the dressed geometry including δΘ line-of-sight contributions
   (Sec. 22).
4. The **ensemble interpretation** of CGI perturbations on an averaged
   background (what plays the role of the statistically homogeneous
   ensemble underlying P(k)) (Sec. 6, arrow 1).
5. A **physical high-k regularisation or validity criterion** for the
   barotropic closure (Sec. 17), or a demonstration that no linear
   barotropic σ_R exists.
6. A **galaxy bias definition** against ⟨ϱ_d⟩_D (Sec. 21).

## 35. Repository preservation statement

- Files created by this phase: `reports/phase1d_c_observable_closure_audit.md`
  and `reports/phase1d_c_closure_inventory.json` — nothing else tracked.
- No frozen source, test, report, artifact, equation, notebook, or
  upstream file was modified; `README.md` and `CLAUDE.md` untouched; the
  generated 1D-B artifact was read only.
- All downloads (four PDFs, rendered page images) and the symbolic-check
  script live in the ignored session scratchpad; the auxiliary libraries
  (pdfminer.six, pypdfium2, sympy) were installed into a scratchpad-only
  `--target` directory, leaving `.venv`/`.venv311` unmodified.
- Upstream clone remains at `590c6fd…`, clean; notebook SHA-256 unchanged
  (verified before and after).
- Branch `phase-1d-c-observable-closure-audit` created at `93d956d…`;
  nothing committed, staged, tagged, or pushed; authors not contacted.

## 36. Final verdict

The observable chain is **closed through the density-growth derivative
under explicit assumptions, and open beyond it**. Exactly:

- **Per-mode growth → anchored density-growth derivative:** closed as a
  conditional diagnostic (A1–A6 + explicit anchor + naming rules), for
  the scale-independent closures only, because strict A2 cancels the
  kernel, the frame, and the shape [DERIVED_FROM_VERIFIED_DEFINITIONS].
- **Any statistical spectrum:** open — external import only
  [PROVISIONAL_MODEL_IMPORT], with the volume-average frame declaration
  itself an import.
- **Observational σ_8:** open — blocked by a **missing geometric object**
  (no global dressed spatial coordinate exists in the primary sources;
  the dressed geometry is spherically symmetric, inhomogeneous, and
  light-cone-constructed [VERIFIED_FROM_PRIMARY_SOURCE]).
- **Barotropic σ_R:** open — blocked by linearity/k-domain (negative
  c_s² instability; [GM]'s own unphysicality assessment)
  [UNRESOLVED, no cutoff invented].
- **RSD f-sigma-8:** open — blocked by a missing dressed redshift-space
  mapping, velocity interpretation, and bias theory; no Timescape primary
  source supplies any of them [UNRESOLVED_EXTERNAL_DEPENDENCY].
- **D3:** both 1992 original sources obtained and inspected for the
  first time; the original formalism structurally supports the
  `derived_4_10` combination, and no `(w + c_s²)Θ` counterpart of the
  printed form was found in the inspected DBE/BDE equations and rendered
  source pages (DBE journal pp. 54, 58, 59, 60; BDE journal pp. 34, 45,
  47, 48 — the remaining pages were not searched); D3
  nonetheless remains a mandatory dual-branch choice pending the formal
  frame-mapping derivation or author confirmation
  [REQUIRES_AUTHOR_INPUT].
- **[GM 48] attribution:** verified from the original source
  [VERIFIED_FROM_PRIMARY_SOURCE] — the sole evidence upgrade of this
  phase.

Recommended next step: the minimal Phase 1D-D of Sec. 31. Everything
else on the chain stays blocked, by evidence, exactly as classified
above.
