# Phase 1D-D-t — Formal D3 frame-mapping derivation

Date: 2026-07-18. Branch: `phase-1d-d-t-d3-frame-mapping` (local only, not
pushed), created at the frozen Phase 1D-C checkpoint
`81148eb6be8add842b538e2a21c5cf9782f9e49e`
(tag `phase-1d-c-observable-closure-audit-v1`).

Machine-readable companion:
[`phase1d_d_t_d3_frame_mapping_inventory.json`](phase1d_d_t_d3_frame_mapping_inventory.json).

Abbreviations: [GM] = Galoppo & Mourier, arXiv:2511.17160v2 / JCAP 02 (2026)
066; [DBE] = Dunsby, Bruni & Ellis, ApJ 395 (1992) 54 ("Covariant
perturbations in a multifluid cosmological medium"); [BDE] = Bruni, Dunsby &
Ellis, ApJ 395 (1992) 34 ("Cosmological perturbations and the physical
meaning of gauge-invariant variables", Paper I). Equation numbers are as
printed in each source.

## 1. Scope and no-code statement

This phase is theoretical, equation-level, and report-only. Its single
objective is to determine, by carrying out the complete frame and variable
transformation from the original covariant multifluid formalism ([DBE],
[BDE]) to the dust-frame system of [GM] Sec. 4, whether the unresolved D3
sign in the barotropic effective-fluid density equation ([GM] Eq. (4.15) vs
Eqs. (4.10)+(4.13)) can be adjudicated.

No scientific code was modified or created. The frozen dual-branch
barotropic implementation (`printed_4_15`, `derived_4_10`) is untouched;
neither branch label was changed, deprecated, or given default status. No
growth, spectrum, sigma_R, sigma_8, f-sigma-8, RSD, likelihood, fitting,
data-ingestion, transfer-function, or observational API work was performed.
No commit, tag, stage, push, merge, or pull request was made. The authors
were not contacted (a user/agent process declaration, not a fact inferred
from Git). At original phase completion, the only repository files created
were this report and its JSON companion; the later independent compliance
audit is the third repository file, and all three remain untracked. All
downloaded sources, rendered pages, and scratch
calculations remain in the ignored session scratchpad.

## 2. Repository and provenance preflight

All twelve required checks passed before any work:

| check | value |
|---|---|
| starting branch | `phase-1d-c-observable-closure-audit` |
| starting HEAD | `81148eb6be8add842b538e2a21c5cf9782f9e49e` |
| base tag `phase-1d-c-observable-closure-audit-v1` | resolves to HEAD |
| all 7 frozen tags (`phase-1b-background-v1` … `phase-1d-c-observable-closure-audit-v1`) | ancestors of HEAD |
| working tree / index / staged | clean / clean / empty |
| upstream clone commit | `590c6fd5332acb15f5683ebf392a0d7ce54983c5`, clean |
| notebook SHA-256 | `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a` |
| Python 3.14.3 suite | 337 passed |
| Python 3.11.9 suite | 337 passed |
| `git diff --check` | clean |

The work branch `phase-1d-d-t-d3-frame-mapping` was then created at exactly
that HEAD and was not pushed.

## 3. Frozen D3 status entering the phase

Phase 1D-C closed with the verdict
`STRUCTURALLY_FAVOURS_DERIVED_4_10_BUT_UNRESOLVED`, on the evidence: (i)
[GM] (4.10)+(4.13) imply the self-coupling `(w_eff − c²_s,eff)Θ`; (ii)
printed [GM] (4.15) has `(w_eff + c²_s,eff)Θ`; (iii) [DBE]'s own barotropic
reduction ((49)/(55)) carries the minus combination; (iv) no plus-sign
counterpart was found in the inspected pages; (v) **the complete
total-frame → dust-frame transformation had not been performed** — [DBE]'s
component equations are written in the total matter rest frame `u_N` while
[GM] Sec. 4 uses the dust energy frame, and differentiating the frame law
[DBE] (27) injects `V̇` terms that could in principle reshuffle `c_s²Δ`
terms between the density and tilt rows; and (vi) [DBE] journal pp. 56–57
had not been inspected. Both branches therefore remained mandatory explicit
choices with no default. This phase executes exactly the missing
transformation (v) and closes the inspection gap (vi).

## 4. Primary-source inventory

| source | file (ignored scratchpad) | SHA-256 | access outcome |
|---|---|---|---|
| [GM] arXiv:2511.17160v2 PDF | `gm_2511.17160v2.pdf` | `856bd78db8f86e46c0f5d21414ad0c1d136b176c6ac1b45418dbeebc38e920dd` (bit-identical to the frozen 1D-A hash) | full PDF; pages rendered at 300 dpi with pypdfium2 and read visually |
| [DBE] ApJ 395, 54 | ADS full-journal scan (21 pages, image-only, no text layer) | `3a082920b358872ec64a3706001e1a10a61a51f2e5140cf29662aa1a04b72f20` | retained from 1D-C; rendered pages `dbe54_p01..21.png` read visually |
| [BDE] ApJ 395, 34 | ADS full-journal scan (20 pages, image-only, no text layer) | `eaa273fa5982689cd55eaba7530103e8e9d77199d4b34d3d173c1e9201075b6c` | retained from 1D-C; rendered pages `bde34_p01..20.png` read visually; correction audit additionally verified (74), fn. 21, and fn. 22 on journal pp. 44–45 |

Pages inspected **in this phase** (scan page ↔ printed journal page):

- [GM] PDF pages 6, 7, 8, 9, 10, 15, 16, 17, 18, 19, 20, 21 = printed
  pp. 5, 6, 7, 8, 9, 14, 15, 16, 17, 18, 19, 20 (Secs. 2.1–2.3, 4.1–4.4:
  Eqs. (2.2)–(2.24), (4.1)–(4.29); pages 8, 9, 16 newly rendered this
  phase, the rest re-read from 1D-C renders).
  The independent compliance audit later rendered PDF p. 52 = printed
  p. 51 and visually confirmed the Appendix A opening used in Sec. 30.
- [DBE] scan p02–p08 = journal pp. 55, 56, 57, 58, 59, 60, 61. **Journal
  pp. 56–57 (scan p03–p04) were inspected for the first time in the
  project**, closing the 1D-C gap; pp. 55 and 61 are also newly inspected;
  pp. 58–60 were re-read in full. (Journal p. 54 = title/abstract was
  inspected in 1D-C.)
- [BDE] scan p05, p06, p08, p09, p10, p11, p12, p15 = journal pp. 38, 39,
  41, 42, 43, 44, 45, 48. **Pages 38, 39, 41, 42, 43 were newly inspected
  in the original phase**; p. 48 ((119)–(120)) was re-verified. The
  independent compliance audit then supplied the source-completeness
  correction by visually verifying (74), footnote 21, and the relevant
  footnote-22 conformal-versus-physical Laplacian clarification on pp. 44–45.
  This additional source anchor does not change A33.

No other external source was required: the transformation closes from the
two ApJ papers plus [GM] (Sec. 33). Equations that [DBE]/[BDE] quote from
earlier work (Ellis 1971; Ellis–Bruni 1989 "EB"; Dunsby 1991) are printed
in full in the inspected pages and are additionally re-derived from first
principles here, so no further upstream source is load-bearing. No claim of
inspection is made for any page not listed.

## 5. Image-scan inspection method

Both ApJ scans are image-only (JBIG2-compressed, no text layer). Pages were
rendered to PNG at 300 dpi (pypdfium2 5.12.1, pip `--target` install in the
ignored scratchpad; project venvs untouched) and read visually. No OCR
output was used as an authority for any sign, index, dot, prime, projected
derivative, or superscript; where a symbol was not fully legible at page
scale, the region was cropped and enlarged (2× on top of 300 dpi) and
re-read (`zoom_bde19*.png`, `zoom_gm221.png`). Scan-page and printed
journal-page numbers are recorded separately throughout (the [DBE] scan has
p01 = journal p. 54; the [BDE] scan has p01 = journal p. 34; footer markers
"– N –" identify [GM] printed pages). Every visually ambiguous symbol found
is listed in Sec. 33.

## 6. Evidence-classification policy

Every material conclusion in this report and the JSON carries exactly one
primary classification from: `VERIFIED_FROM_PRIMARY_SOURCE`,
`DERIVED_FROM_VERIFIED_DEFINITIONS`, `SYMBOLICALLY_VERIFIED`,
`NUMERICALLY_CORROBORATED`, `CONVENTION_DEPENDENT`, `REQUIRES_AUTHOR_INPUT`,
`UNRESOLVED_EXTERNAL_DEPENDENCY`, `NOT_APPLICABLE`, `NOT_JUSTIFIED`; formal
conclusion objects in the JSON additionally carry all seven fields
(`classification`, `source`, `assumptions`, `derivation_summary`,
`convention_dependencies`, `implementation_consequence`,
`evidence_needed_to_change_status`). Source evidence, algebraic derivation,
machine symbolic checking, and interpretive judgement are kept in separate
conclusion objects and are never merged into one evidence level: what a
printed page shows is classified `VERIFIED_FROM_PRIMARY_SOURCE`; what
follows from verified definitions by displayed algebra is
`DERIVED_FROM_VERIFIED_DEFINITIONS`; what a sympy script confirms is
`SYMBOLICALLY_VERIFIED` (and proves only the encoded equations); judgement
calls are labelled as such.

## 7. Complete frame dictionary

All frames are first-order-tilted relative to the shared FLRW background;
in the background all listed four-velocities coincide ([DBE] p. 56: "all
the fluid components share the same hydrodynamical 4-velocity u^a_(i) =
u^a_E(i) in the background FLRW model"). Signature (−,+,+,+) ([BDE] (22),
Ellis-1971 conventions; [GM] standard). Distinct symbols are used per frame;
a dot or `D_µ` always belongs to the stated congruence.

| # | frame | 4-velocity | defining condition | projector | dot / spatial derivative | Θ | acceleration | heat flux seen | anisotropic stress | tilt vs dust |
|---|---|---|---|---|---|---|---|---|---|---|
| F1 | generic CGI observer ([GM] Sec. 2; [BDE] (44) text, fn. 14) | `n^µ` | any covariantly defined unit timelike field coinciding with `u_E` in the background | `h_µν = g_µν + n_µn_ν` | `Ẋ = n^µ∇_µX`; `D_µ = h_µ^ν∇_ν` | `Θ = ∇_µn^µ` | `a_µ = n^ν∇_νn_µ` (first order) | `q^(i)_µ = h^(i)V^(i)_µ` per component | 0 (perfect components) | `V^(d)_µ − V^(eff)_µ` bookkeeping |
| F2 | dust energy frame ([GM] (4.20) context, Sec. 4.1) | `u_d^µ` | `V^(d) = 0`; comoving with the irrotational dust | `h^{(d)}_µν` | dust proper-time dot | `Θ_d` | **0 at first order** (geodesic; derived Sec. 17) | `q^(d)=0`, `q^(eff)=h^(eff)V^(eff)` | 0 | 0 (reference) |
| F3 | effective-fluid energy frame | `u_e^µ` | eff fluid perfect in this frame ([GM] (2.6) first line) | `h^{(e)}_µν` | eff proper-time dot | `Θ_e = Θ − ∇·V^{(eff)}` (Sec. 17) | `−D_µp_e/h_e`-type (non-geodesic) | 0 by definition | 0 by assumption | `V^(eff)_µ` |
| F4 | total energy frame (Landau–Lifshitz; [DBE] p. 56, (18)) | `u_E^µ` | total `q_µ = 0` ⟺ `Σ_i h_i V^(i)`|`_E = 0` | `h^{(E)}_µν` | E-frame dot | `Θ_E` | from total momentum eq. | 0 by definition | Σπ^(i) | enthalpy-weighted mix |
| F5 | total matter (particle/Eckart) rest frame ([DBE] p. 56, (19); §3.2 default `u^a = u_N^a`) | `u_N^µ` | total particle drift `j^µ = 0` | `h^{(N)}_µν` | N-frame dot | `Θ_N` | `a_µ` of [DBE] (43)/(46) | `q_N ≠ 0` in general | Σπ^(i) | mix |
| F6 | Buchert averaging foliation ([GM] Sec. 3, p. 14) | normal = `u_d^µ` | flow-orthogonal slicing of the irrotational dust; domain `D` comoving with dust | same as F2 | volume-time dot = dust dot | `⟨Θ⟩_D → 3ȧ_D/a_D` at background | 0 | — | — | 0 |
| F7 | wall/dressed observer (Phase 1B `W09`) | wall clocks | finite-infinity walls | — | wall proper time | dressed `H` | — | — | — | not needed at first order here |

Notes. (a) [DBE] §2 keeps `u^a` general ("we have not fixed u^a, which
could, for example, be u_N^a or u_E^a", p. 56) and fixes `u^a = u_N^a` only
at §3.2 (p. 59) for the component equations; [BDE] defaults to `u_N` with
footnote 14 stating the equations keep the same form for any admissible
covariant frame. (b) [GM] keep `n^µ` unspecified through (2.14)–(2.24)
(p. 8: "the observer frame n^µ, which we have kept unspecified in the above
derivation") and choose the dust frame in Sec. 4. (c) The dust frame F2
satisfies [DBE]/[BDE]'s admissibility requirement (covariantly defined,
coincides with `u_E` in the background). (d) The wall/dressed frame F7 does
not enter the D3 question: the perturbation systems are formulated entirely
in volume-average time on the F2/F6 congruence (frozen 1D-A audit).
Primary classification of the dictionary: `VERIFIED_FROM_PRIMARY_SOURCE`.
Supporting derived evidence for geodesy and the Θ shift is displayed below;
it is not a second primary classification.

## 8. Stress-energy decomposition

Component `i` is a perfect fluid in its own energy frame,

    T^(i)_µν = (ρ^(i) + p^(i)) u^(i)_µ u^(i)_ν + p^(i) g_µν            [GM (2.6), line 1, p. 6]

with the tilt decomposition `u^(i)_µ =: (−n^νu^(i)_ν)(n_µ + V^(i)_µ)`,
`n^µV^(i)_µ = 0` [GM p. 5]. Re-decomposed with respect to the observer
frame `n^µ` at first order,

    T^(i)_µν ≃ (ρ^(i) + p^(i)) n_µ n_ν + p^(i) g_µν + q^(i)_µ n_ν + q^(i)_ν n_µ ,
    q^(i)_µ := h^(i) V^(i)_µ ,   h^(i) := ρ^(i) + p^(i)                 [GM (2.6), line 2]

which is [DBE] (9) with intrinsic (own-frame) flux `q^(i)_a = 0` and
`π^(i)_ab = 0`. The general [DBE] decomposition (7)/(9) allows intrinsic
imperfect terms; [GM]'s two-fluid system (irrotational dust + effective
perfect fluid, "a set of two non-interacting perfect fluids, one being
pressureless", printed p. 14) sets them to zero. Components are separately
conserved, `∇^νT^(i)_µν = 0` [GM (2.7)]; interactions ([DBE] (20)–(21)
`ε_(i)`, `f^(i)_a`) vanish. Classification:
`VERIFIED_FROM_PRIMARY_SOURCE`.

## 9. First-order boost derivation

For two unit timelike fields `n_1^µ`, `n_2^µ` differing at first order
(`ξ_µ := n_{2µ} − n_{1µ}`, spatial at first order), the decomposition of a
fixed `T^(i)_ab` transforms as follows. Derivation: insert `n_2 = n_1 + ξ`
into the projections `ρ = T_{ab}n^an^b`, `q_a = −h_a^bT_{bc}n^c − ρn_a`,
`p = h^{ab}T_{ab}/3`, `π_ab = T_{⟨ab⟩}`, discard `O(ξ²)` and
`ξ ×`(first-order) products:

- energy density: `ρ(n_2) = ρ(n_1) + 2q·ξ + O(2) = ρ(n_1) + O(2)` —
  invariant at first order (both `q` and `ξ` are first order);
- isotropic pressure: invariant at first order (same mechanism);
- anisotropic stress: invariant at first order;
- heat flux: `q̃^(i)_a = q^(i)_a + (µ_(i)+p_(i))V^(i)_a` — the convective
  boost;
- four-velocity: `u^(i)` unchanged (a physical field); its tilt relabels,
  `V^(i)[n_2] = V^(i)[n_1] − ξ + O(2)`;
- expansion: `Θ(n_2) = Θ(n_1) + ∇^µξ_µ + O(2)`;
- four-acceleration: `a_µ(n_2) = a_µ(n_1) + ξ̇_µ + (Θ/3)ξ_µ + O(2)`;
- density gradient: `𝒟^(i)_a(n_2) = 𝒟^(i)_a(n_1) + (a/ρ_i)ρ̇_i ξ_a =
  𝒟^(i)_a(n_1) − aΘ(1+w_i)ξ_a + O(2)` (projector change injects the
  background time derivative);
- pressure gradient (enthalpy-normalised): `𝒫^(i)_a(n_2) = 𝒫^(i)_a(n_1) +
  (a/h_i)ṗ_i ξ_a = 𝒫^(i)_a(n_1) − aΘc²_s(i)ξ_a + O(2)`;
- expansion gradient: `𝒵_µ` shifts by `aΘ̇ξ_µ + aD_µ(D^νξ_ν)`-type terms;
- projected time derivatives: for any first-order quantity `X`,
  `Ẋ[n_2] = Ẋ[n_1] + O(2)`; for background quantities the dots agree at
  first order (differences are `ξ·∇(background) = ξ ×` spatial gradient
  `= O(2)` since background spatial gradients vanish);
- relative velocity divergence: `D^µV^(i)_µ` shifts by `−D·ξ` at first
  order.

For all applications below, the transformation direction is fixed once and
for all by

    ξ^a := u_destination^a − u_source^a .

The complete first-order source-to-destination laws are therefore:

| quantity | source → destination law |
|---|---|
| component tilt | `V_i[destination] = V_i[source] − ξ` |
| component heat flux | `q_i[destination] = q_i[source] − h_i ξ` |
| component density gradient | `𝒟_i[destination] = 𝒟_i[source] − aΘ(1+w_i)ξ` |
| enthalpy-normalised pressure gradient | `𝒫_i[destination] = 𝒫_i[source] − aΘc²_s(i)ξ` |
| expansion | `Θ[destination] = Θ[source] + D_aξ^a` |
| acceleration | `a_a[destination] = a_a[source] + ξ̇_a + (Θ/3)ξ_a` |

The required concrete directions are:

| source → destination | `ξ` | reconciliation/result |
|---|---|---|
| arbitrary observer `n` → dust frame `u_d` | `ξ = V_d[n]` | `q_d[u_d]=0`; `V_eff[u_d]=V_eff[n]−V_d[n]` |
| arbitrary observer `n` → effective-fluid rest frame `u_eff` | `ξ = V_eff[n]` | `q_eff[u_eff]=0` |
| `u_N` → component rest frame `u_i` | `ξ=V_i[N]` | `𝒟_i[u_i]=𝒟_i[N]−3aH(1+w_i)V_i`, DBE (27) at `ε_i=0` |
| `u_N` → `u_E` | `ξ=q_N/h=−{}^EV^N` | `𝒟_E=𝒟_N+3aH(1+w){}^EV^N`, BDE (25)–(26) |
| dust frame → Buchert dust foliation | `ξ=0` | identity: the foliation normal is `u_d` |

DBE (15) uses a source-oriented relative velocity: the component-own-frame
flux is boosted to the observer frame as `q̃_i=q_i+h_iV_i`. With the
destination-minus-source definition above, that same statement is
`q_i[destination]=q_i[source]−h_iξ`, because DBE's `V_i` points from the
observer to the component. DBE (27) and BDE (25)–(26) give the density-law
instances displayed in the table. Thus no heat-flux or gradient sign is left
without a declared direction.

These are not merely quoted: the flux boost is printed as [DBE] (15) (p. 57,
`q̃_a^(i) = q_a^(i) + (µ_(i)+p_(i))V_a^(i)`) and [BDE] (15); the
invariances are printed as [BDE] (14) (p. 38, `µ ≃ µ̃, p ≃ p̃, n ≃ ñ,
π_ab ≃ π̃_ab`); the density-gradient law is printed as [BDE] (25)–(26)
(p. 39) and its arbitrary-frame footnote 15, and as [DBE] (27) (p. 58); and
every one of these laws was additionally verified by direct coordinate
computation on a perturbed FLRW metric with two independent arbitrary
observers (checks C6a–C6e, Sec. 32), including the flux boost
`q_x = h^(eff)V^(eff)_x` (C6b) and the exact first-order frame invariance
of the closure combination (C6e). Track of discarded products: every
discarded term is a product of two first-order factors (`ξ·q`, `ξ·δρ`,
`ξ·V`, `ξ·`metric perturbation); no background×first-order term is
discarded anywhere.

Effective-fluid applicability under boosts: the effective fluid enters
these transformations exactly as an ordinary component **because [GM]
postulate it to be a separately conserved perfect fluid at the
perturbative level**; that postulate (not the boost algebra) is the
additional assumption, examined in Sec. 21. Primary classification of the
boost-law conclusion: `DERIVED_FROM_VERIFIED_DEFINITIONS`. Supporting
evidence: the printed instances are `VERIFIED_FROM_PRIMARY_SOURCE`, and the
coordinate checks are `SYMBOLICALLY_VERIFIED`.

## 10. Original DBE/BDE equation transcription

All equations below were transcribed by direct visual inspection of the
scan renders in this phase. Frame, signature (−,+,+,+), overdot = covariant
derivative along the stated congruence, `Θ = 3H`, `κ = 8πG`, `c = 1`
throughout ([DBE] p. 55; [BDE] p. 38). The full per-equation records
(original notation, scan page, journal page, frame, component/total,
closure and flux assumptions, real-space form, sign of every pressure term)
are in the JSON `dbe_bde_equations`. Key equations verbatim:

**[DBE], journal pp. 55–61 (scan p02–p08):**

- (5) `T^{ab}_{;b} = 0, S^a_{;a} ≥ 0` (p. 56); (6) perfect-fluid form; (7)
  general-frame form with `q_a`, `π_ab`, drift `j^a`; (8) `T_ab = Σ_i
  T^(i)_ab`; (9) component form **in the component's own frame** with
  intrinsic `q^(i)_a`, `π^(i)_ab`; (10) component particle flux.
- (11)–(14) linear tilt: `u^a_(i) − u^a ≈ β_(i)c̃^a_(i) = V^a_(i)` — the
  GI relative velocity (p. 56).
- (15) `q_a = Σ_i q̃_a^(i)`, `q̃_a^(i) = q_a^(i) + (µ_(i)+p_(i))V_a^(i)`
  (p. 57) — first-order flux boost.
- (16) totals `µ = Σµ_(i)`, `p = Σp_(i)`, `π_ab = Σπ^(i)_ab` (p. 57).
- (18) energy-frame condition `Σ_i(µ_(i)+p_(i))V_a^(i) = 0`; (19) particle-
  frame condition `Σ_i n_(i)V_a^(i) = 0`; (20)–(21) interaction variables
  `J^(i)_a = ε_(i)u_a + f^(i)_a` (p. 57).
- Frame admissibility (p. 57, text): u^a must be "covariantly defined and
  coincide with u_E^a in the background".
- (23) `X_a ≡ ⁽³⁾∇_aµ, Y_a ≡ ⁽³⁾∇_ap, Z_a ≡ ⁽³⁾∇_aΘ`; "Y_a = 0 ⇒ a_a = 0";
  (24) `𝒟_a = aX_a/µ`, `𝒵_a = aZ_a` (p. 57).
- (25) component gradients **"with respect to the total matter rest frame,
  taken to be u^a = u_N^a"**: `𝒟_a^(i) = aX_a^(i)/µ_(i)`,
  `𝒵_a^(i) = aZ_a^(i)`, `X_a^(i) = h^b_a µ_(i);b` (pp. 57–58).
- (26) own-frame component gradients `^N𝒟_a^(i) = a\,^NX_a^(i)/µ_(i)` with
  `^NX_a^(i) = h_{(i)a}^b µ_(i);b` (p. 58).
- (27) **frame law** (p. 58):
  `^N𝒟_a^(i) = 𝒟_a^(i) − 3Ha(1+w_(i))V_a^(i) + (a/µ_(i))ε_(i)V_a^(i)`;
  the `ε_(i)` term is the interaction energy-transfer rate, zero for
  non-interacting fluids. (The 1D-C reconstruction of (27) is confirmed
  exactly; no transcription discrepancy found.)
- (28) `µ̇ + 3hH + h⁽³⁾∇_aΨ^a = 0`; (29) `ha_a + Y_a + h(F_a + Π_a) = 0`;
  (30) `Ψ_a = q_a/h`, `Π_a = (1/h)⁽³⁾∇^bπ_ab`,
  `F_a = Ψ̇_a − (3c_s² − 1)HΨ_a`; (31) Raychaudhuri
  `3Ḣ + 3H² − A + ½κ(µ+3p) − Λ = 0` (standard `−Λ`) (p. 58).
- (32) total density-gradient equation (p. 58):
  `𝒟̇_a − 3Hw𝒟_a + (1+w)𝒵_a = 3a(1+w)H(F_a+Π_a) − a(1+w)⁽³⁾∇_a⁽³⁾∇^bΨ_b`;
  self-coupling `+3Hw`; `c_s²` absent.
- (34) `aY_a = c_s²µ𝒟_a + p𝓔_a`, `𝓔_a = (a/p)(∂p/∂s)_µ⁽³⁾∇_a s`,
  `c_s² = ṗ/µ̇` (p. 58, verbatim).
- (42)–(43) component conservation **in the frame `u^a = u_N^a`** (§3.2
  opening, p. 59): `µ̇_(i) + 3h_(i)H + h_(i)⁽³⁾∇_aΨ^a_(i) = ε_(i)`;
  `h_(i)a_a + Y_a^(i) + h_(i)(F_a^(i)+Π_a^(i)) + (1+c²_s(i))ε_(i)Ψ_a^(i)
  = f_a^(i)`.
- (44) `F_a^(i) = Ψ̇_a^(i) − (3c²_s(i)−1)HΨ_a^(i)`; (45)
  `Ψ_a^(i) = q̃_a^(i)/h_(i) = q_a^(i)/h_(i) + V_a^(i)` — for perfect-fluid
  components `Ψ^(i) = V^(i)` (pp. 59–60).
- (46) component density-gradient equation (p. 60), self-coupling
  `−3Hw_(i)` on the LHS, with interaction terms
  `(3aH/µ_(i))(1+c²_s(i))ε_(i)Ψ^(i)_a`, `−(3Ha/µ_(i))f^(i)_a`,
  `(a/µ_(i))⁽³⁾∇_aε_(i)`, `(a/µ_(i))ε_(i)a_a`, `−(1/µ_(i))ε_(i)𝒟^(i)_a`
  and the tilt-Laplacian `−a(1+w_(i))⁽³⁾∇_a⁽³⁾∇_bΨ^b_(i)`.
- (47) momentum equation for `Ψ^(i)` "relative to the frame u_N^a" (p. 60),
  including the total-fluid coupling
  `(1/(ahh_(i)))(h_(i)c_s²µ𝒟_a − hc²_s(i)µ_(i)𝒟^(i)_a + h_(i)p𝓔_a −
  hp_(i)𝓔^(i)_a)`; (48) `aY_a^(i) = c²_s(i)µ_(i)𝒟_a^(i) + p_(i)𝓔_a^(i)`.
- (49) "useful form" (p. 60): self-coupling **`−3(w_(i) − c²_s(i))H`** on
  the LHS, with the total coupling `(1/(µ_(i)h))(3Hh_(i) − ε_(i))
  (c_s²µ𝒟_a + p𝓔_a)` and `−3Hw_(i)𝓔^(i)_a`.
- (50)–(53) entropy decomposition; (51) `c_s² = (1/h)Σ_i h_(i)c²_s(i)`.
- (54)/(55) the no-interaction forms of (47)/(49); (55) self-coupling
  `−3(w_(i) − c²_s(i))H` as printed.
- §3.3 (56)–(66) relative equations (p. 61): relative variables only; no
  further density self-coupling structure (inspected for completeness).

**[BDE], journal pp. 38–43, 48 (scan p05, p06, p08, p09, p10, p15):**

- (14)–(16) first-order frame invariances and flux/drift boosts (p. 38).
- Frame defaults and footnote 14 (p. 38): equations keep the same form for
  any admissible covariant `u^a`.
- (17)–(23) FLRW characterisation; metric (22)–(23) with signature
  (−,+,+,+) explicit; (19) prints `µ̇ + 3µH(µ+p) = 0` — a typographical
  slip (Sec. 33); (20) Raychaudhuri with standard `−Λ`.
- (24) `𝒟_a = (a/µ)⁽³⁾∇_aµ`, `𝒵_a = a⁽³⁾∇_aΘ` (p. 39).
- (25) gradient frame-change law (p. 39):
  `⁽³⁾∇_a^E f = ⁽³⁾∇_a^N f + (ḟ/(µ+p))q_a^N`; (26)
  `𝒟_a^E = 𝒟_a^N + 3aH(1+w)\,^EV_a^N`; footnote 15: for a general frame
  `n^a`, `𝒟_a^E = 𝒟̃_a + 3aH(1+w)(u_a^E − n_a)`.
- (27)–(29) `P_a = (a/p)⁽³⁾∇_a p` (pressure-normalised), entropy
  perturbation, `c_s² = ṗ/µ̇` (p. 39).
- (40) scalar variables `Δ = a⁽³⁾∇_a𝒟^a`, `𝒵 = a⁽³⁾∇_a𝒵^a`, … (p. 41).
- (44) text (p. 41): "from now on the fluid 4-velocity will be taken as any
  covariantly defined u^a constrained to coincide with u_E^a in the
  background … for u^a = u_E^a we must set q^a = 0 … for u^a = u_N^a we
  have q^a = q_N^a."
- (45)–(48) conservation + definitions + Raychaudhuri (p. 41), identical
  in structure to [DBE] (28)–(31).
- (61) single-fluid density-gradient equation (p. 43), same structure as
  [DBE] (32), stated for the generic admissible frame; (62) the `𝒵̇`
  equation.
- (63) **printed scalarisation identities** (p. 43): for any first-order
  vector `V_a` and tensor `T_ab`, `a⁽³⁾∇_a V̇_b = (a⁽³⁾∇_a V_b)˙`.
- (74) **scalar-harmonic eigenvalue** (p. 44), in the relevant FLRW
  convention:

      ⁽³⁾∇² Q = −(k²/a²) Q .

  Footnote 21 classifies the scalar/vector/tensor harmonics. The relevant
  footnote-22 clarification on p. 45 distinguishes the conformal spatial
  operator from the physical Laplacian and accounts for the displayed
  `a⁻²`. These entries were added as a source-completeness correction after
  the independent compliance audit; they do not alter the A33 derivation.
- (117)–(120) GI-gradient harmonic expansion (p. 48); (119)–(120)
  `𝒟_α = aε_m|α − 3a′(1+w)V_Cα = −kaε_m(η)Y_α^(0) − 3a′(1+w)V_C(η)Y_α^(1)`
  (re-verified; identical to the 1D-C record).

No discrepancy against the Phase 1D-C reconstructions was found; the 1D-C
records of DBE (32)/(46)/(49)/(55) and BDE (119)–(120) are confirmed
exactly, and are now embedded in their complete printed context.
Classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 11. DBE/BDE notation map

| [DBE]/[BDE] | meaning | [GM] counterpart |
|---|---|---|
| `u^a` (unfixed §2; `u_N` in [DBE] §3.2; fn. 14/(44) generic in [BDE]) | fundamental observer | `n^µ` (unspecified in Sec. 2; dust in Sec. 4) |
| `µ_(i)`, `p_(i)`, `h_(i) = µ_(i)+p_(i)` | component density/pressure/enthalpy | `ρ^(i)`, `p^(i)`, `h^(i)` |
| `V_a^(i)` (14) | component tilt vs observer | `V_µ^(i)` |
| `Ψ_a^(i) = q̃_a^(i)/h_(i) = V_a^(i)` (perfect) (45) | flux-per-enthalpy | `V_µ^(i)` (via `q^(i) = h^(i)V^(i)`) |
| `F_a^(i) = Ψ̇_a^(i) − (3c²_s(i)−1)HΨ_a^(i)` (44) | momentum combination | `F_µ^(i) = V̇_µ^(i) + (1/3 − c²_s(i))ΘV_µ^(i)` (2.9 text) — identical after `Θ = 3H` |
| `𝒟_a^(i) = aX_a^(i)/µ_(i)` (25) | comoving fractional density gradient | `𝒟_µ^(i) = (a/ρ^(i))D_µρ^(i)` (2.2) — identical construction |
| `𝒵_a = aZ_a` (24) | comoving expansion gradient | `𝒵_µ = aD_µΘ` (2.2)/(2.4) — identical |
| `Y_a^(i)`; `aY_a^(i) = c²_s(i)µ_(i)𝒟_a^(i) + p_(i)𝓔_a^(i)` (48) | pressure gradient + decomposition | `𝒫_µ^(i) = (a/h^(i))D_µp^(i)` (2.2); decomposition (2.18) `(1+w_(i))𝒫^(i) = c²_s(i)𝒟^(i) + w_(i)𝓔^(i)` — **exactly (48) divided by `h_(i)`** (verified algebraically) |
| [BDE] `P_a = (a/p)⁽³⁾∇_ap` (27) | pressure-normalised gradient | superseded: [GM] fn. 2 states the enthalpy normalisation is deliberately different from [45–50] |
| `𝓔_a^(i)` | entropy perturbation | `𝓔_µ^(i)` (2.18); zero under the barotropic closure |
| `c²_s(i) = ṗ^(i)/µ̇^(i)` ([DBE] p. 58; [BDE] (29)) | background sound speed | `c²_s(i) := ṗ^(i)/ρ̇^(i)` (2.9 text)/(4.13) — identical |
| `w_(i) = p_(i)/µ_(i)` | EoS parameter | `w^(i) := p^(i)/ρ^(i)` (2.14 text) |
| `a` with `ȧ/a = Θ/3 = H` ([DBE] (4)) | local scale factor | `a` with `ȧ/a := Θ/3` (2.2 text) — identical |
| `ε_(i)`, `f_a^(i)` (21) | interaction transfer rates | absent (non-interacting, (2.7)) |
| `Π_a^(i)` (44) | anisotropic-stress divergence | absent (perfect components) |
| scalarisation `Δ = a⁽³⁾∇_a𝒟^a` ([BDE] (40)) | scalar CGI variables | `Δ^(i) := aD^µ𝒟_µ^(i)` etc. (2.20)–(2.21) — identical |

Classification: `VERIFIED_FROM_PRIMARY_SOURCE` (each row anchored to the
cited printed equations).

## 12. Galoppo–Mourier notation map (chain to the Phase 1C state)

| [DBE]/[BDE] original | [GM] general covariant | [GM] dust-frame / frequency space | Phase 1C state component |
|---|---|---|---|
| `𝒟_a^(i)`, scalar `Δ^(i)` (i = dust) | `𝒟_µ^(d)`, `Δ^(d)` | `Δ^(d)` | `v[0] = Delta_d` |
| `𝒵_a`, scalar `𝒵` | `𝒵_µ`, `𝒵` | `𝒵` | `v[1] = Z` (`𝒵 = −Δ̇^(d)`, (4.9)/(4.14)) |
| `𝒟_a^(i)`, scalar (i = eff) | `𝒟_µ^(eff)`, `Δ^(eff)` | `Δ^(eff)` | `v[2] = Delta_eff` |
| `Ψ_a^(i) = V_a^(i)`, scalar `V^(i)` | `V_µ^(eff)`, `V^(eff) = aD^µV^(eff)_µ` | `Ṽ^(eff) := (1+w_eff)V^(eff)` | `v[3]` (`rescaled_Vtilde`) or `V^(eff)` (`unrescaled_V`) |
| `aY^(i)/…` pressure gradient | `𝒫_µ^(eff)`, `𝒫^(eff)` | `𝒫̃^(eff) := (1+w_eff)𝒫^(eff)` | eliminated by closure (4.13) |
| total `𝒟_a`, `Δ` | `𝒟_µ`, `Δ = Σ(ρ^(i)/ρ)Δ^(i)` | eliminated in favour of `Δ^(d)`, `Δ^(eff)` in (4.7) | — |
| `Θ = 3H` | `Θ` | background `3ȧ_D/a_D` | tracker `Theta(t)` |
| `a` (local scale factor) | `a` | background `a_D(t)`, `a_D(t₀)=1+f_v0/2` | tracker `a_D` |
| `⁽³⁾∇²` | `⁽³⁾Δ` | `−k²/a_D²` (fn. 8) | matrix `k` |

Normalisation factors identified: `a` enters once per gradient
(`𝒟 ∝ aD_µ`) and once per scalarisation (`Δ ∝ aD^µ𝒟_µ`, hence
`Δ ≃ (a²/ρ)⁽³⁾Δρ`, (2.19)); `ρ^(i)` normalises density gradients;
`h^(i) = ρ^(i)+p^(i)` normalises [GM] pressure gradients ([BDE] used `p`);
`1+w` converts between unrescaled (`V`, `𝒫`) and rescaled (`Ṽ`, `𝒫̃`)
variables; `k` enters only through `⁽³⁾Δ → −k²/a²` acting on the tilt term
(`a(1+w)⁽³⁾ΔV → −(k²/a)Ṽ`); the background expansion enters as `Θ` factors
in the self-couplings and `F`-combinations. Primary classification:
`VERIFIED_FROM_PRIMARY_SOURCE`. The normalization bookkeeping is supporting
derived evidence, not a second primary classification.

## 13. Component versus total-fluid distinction

Rigorous determination (from the printed frames and the re-derivations):

- [DBE] (32)/[BDE] (61) describe the **total-fluid** density gradient in
  the fundamental frame; `c_s²` (total) is absent from (32) and enters the
  system only via `Y_a` and the `𝒵̇` equation.
- [DBE] (46) describes an **individual component measured in the total
  matter rest frame `u_N`** (component quantities, observer `u_N`); the
  component's own `c²_s(i)` appears only inside `F^(i)` (via (44)) and the
  interaction terms.
- [DBE] (26) `^N𝒟^(i)` is the component measured **in its own frame**;
  (27) converts between the two.
- [DBE] (49)/(55) are (46) after eliminating `F^(i)` with the momentum
  equations (29)+(43) — still observer `u_N`. The elimination brings in
  **both** the component's own `c²_s(i)𝒟^(i)` (producing the
  `−3(w_(i)−c²_s(i))H` self-coupling) and the **total** combination
  `(3H/h)(1+w_(i))(c_s²µ𝒟_a + p𝓔_a)` (a cross-coupling to the total
  gradient when the total gradient is retained as an independent total
  variable). If `µ𝒟 = Σ_j µ_(j)𝒟^(j)` is expanded, the same total term can
  contain a contribution proportional to `𝒟^(i)`. This representation issue
  does not modify the independently derived GM dust-frame A33 coefficient.
  The symbolic re-derivation (check S8) confirms the explicit DBE
  retained-total-variable form and its component coefficient.
- Four distinct sound speeds are tracked and never conflated: total
  `c_s² = ṗ/µ̇ = (1/h)Σh_(i)c²_s(i)` ([DBE] (51)); component
  `c²_s(i) = ṗ^(i)/µ̇^(i)`; the adiabatic `(∂p/∂µ)_s` (equal to `ṗ/µ̇`
  for the standard background, [BDE] (29)); and [GM]'s effective-fluid
  `c²_s,eff = ṗ_eff/ρ̇_eff` — a component sound speed in this taxonomy.
  Relative entropy perturbations `S^(ij)`/`𝓔^(i)` vanish under the
  barotropic closure.
- **Applicability of the [DBE] reduction to [GM]'s effective component:**
  no longer merely analogous. The general-frame component equation is
  derived here from first principles for an arbitrary admissible observer
  (Secs. 22, 28), so the dust-frame [GM] system is obtained directly, not
  by porting the `u_N`-frame [DBE] result. The single assumption required
  is [GM]'s own effective-fluid postulate (Sec. 21). The 1D-C caution that
  the [DBE] comparison was "structural, not verbatim" is hereby closed by
  derivation rather than by source look-up.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE` (frames and equations
as printed). Supporting evidence: the S8 and general-frame reconstructions
are `DERIVED_FROM_VERIFIED_DEFINITIONS` and `SYMBOLICALLY_VERIFIED`.

## 14. Total-frame variables

In the total matter rest frame `u_N` ([DBE] §3.2): observer quantities
`Θ_N`, `a_µ(u_N) ≠ 0` (determined by the total momentum equation (29):
`ha_a = −Y_a − h(F_a+Π_a)`); component tilts `V^(i)` with
`Σ_i n_(i)V^(i) = 0` ((19)); component flux seen: `q̃^(i) = h_(i)V^(i)`;
component variables `𝒟^(i)`, `𝒵`, `Y^(i)`, `Ψ^(i) = V^(i)`, `F^(i)`.
For [GM]'s two-fluid case the corresponding total-frame equations are the
`n = u_N` instance of the general-frame system (2.14)–(2.17). These
variables enter this audit only as the source frame of the transformation;
all final statements are made in the dust frame. Classification:
`VERIFIED_FROM_PRIMARY_SOURCE`.

## 15. Dust-frame variables

In the dust energy frame (`n = u_d`, `V^(d) = 0`): the dust is geodesic at
first order (`a_µ ≃ 0`, derived in Sec. 17 and verified in coordinates,
check C5), so `F^(d) = 0` and `𝒫^(d) = 0` (pressureless); the effective
fluid carries the only tilt `V^(eff)` and flux `q^(eff) = h^(eff)V^(eff)`;
its momentum relation ([GM] (2.9) with `a_µ = 0`, printed as (4.8)) is
`F^(eff) = −(1/a)𝒫^(eff)` — [GM]'s `𝒫 + aF = 0` relation (p. 16 text).
State variables: `Δ^(d)`, `𝒵`, `Δ^(eff)`, `Ṽ^(eff)` (or `V^(eff)`), with
`𝒫̃^(eff)` eliminated by the closure. Primary classification:
`DERIVED_FROM_VERIFIED_DEFINITIONS`. The cited printed equations are
supporting source evidence.

## 16. Heat-flux transformation

Under `n_1 → n_2 = n_1 + ξ`: `q^(i)[n_2] = q^(i)[n_1] − h^(i)ξ` (from
`q^(i) = h^(i)V^(i)` and `V^(i)[n_2] = V^(i)[n_1] − ξ`), i.e. the flux
boost [DBE] (15)/[BDE] (15) read in reverse. Passing from the total frame
(where both components generally carry flux) to the dust frame: the dust
flux is removed exactly (`q^(d) → 0`, defining condition), and the
effective-fluid flux becomes `q^(eff) = h^(eff)V^(eff)` with `V^(eff)` now
the dust-relative tilt. No flux term is generated or lost beyond this
relabelling at first order; in particular no flux enters the closure
combination (C6e). Verified in coordinates (C6b). Classification:
`DERIVED_FROM_VERIFIED_DEFINITIONS`. C6b/C6e are supporting symbolic
evidence.

## 17. Expansion and acceleration transformation

**Expansion.** `Θ(n_2) = Θ(n_1) + ∇^µξ_µ + O(2)`; consequently
`𝒵_µ` changes by `a Θ̇ ξ_µ + aD_µ(D^νξ_ν)`-type first-order terms. In the
scalar equations the expansion gradient that appears is always the
observer-frame `𝒵` of the *chosen* frame; after fixing `n = u_d` no
residual expansion-shift terms remain. A by-product of the coordinate work
(check C3b): the exact first-order relation between component and observer
expansions is `Θ = Θ^(i) − ∇^µV^(i)_µ`, whereas printed [GM] (2.5) has
`Θ ≃ Θ^(i) + ∇^µV^(i)_µ` — a sign slip in (2.5) as printed
(non-propagating: (2.5) is not used in the (2.14)→(4.15) chain; Sec. 33).

**Acceleration.** `a_µ(n_2) = a_µ(n_1) + ξ̇_µ + (Θ/3)ξ_µ + O(2)`. The dust
geodesic property is not an assumption: momentum conservation for the
pressureless dust in its own frame forces `ρ^(d)a_µ = 0` at first order
([DBE] (23) text "Y_a = 0 ⇒ a_a = 0"; [GM] (2.9) with `𝒫^(d) = F^(d) = 0`),
verified by direct coordinate computation (check C5: the dust-frame
acceleration vanishes identically once dust momentum conservation is
imposed, for arbitrary metric functions). Hence **the dust-frame choice
removes all acceleration terms**, and with them the mechanism by which the
observer acceleration feeds pressure gradients into the density equation in
non-geodesic frames. Primary classification:
`DERIVED_FROM_VERIFIED_DEFINITIONS`. C5 supplies supporting symbolic
evidence, and the cited equations supply supporting source evidence.

## 18. Density-gradient transformation

The frame law, derived in Sec. 9 and printed in both sources:

    𝒟^(i)_a[n_2] = 𝒟^(i)_a[n_1] − aΘ(1+w_(i))ξ_a + O(2) ,   ξ = n_2 − n_1 .

Instances: [BDE] (26) (`n_1 = u_N`, `n_2 = u_E`, `ξ = −^EV^N`); [BDE]
fn. 15 (arbitrary `n`); [DBE] (27) (`n_1 = u_N`, `n_2 = u_(i)` own frame,
`ξ = V^(i)`, plus the interaction term `(a/µ_(i))ε_(i)V^(i)_a` — zero
here). Coordinate check C6c verifies the law with two independent arbitrary
observers. **The differentiation concern from 1D-C is resolved
constructively:** rather than differentiating the frame law (which injects
`V̇` terms), this phase derives the density-gradient *evolution equation*
directly in an arbitrary frame (Sec. 22); the frame law is then only needed
to relate initial data between frames, and the `V̇` bookkeeping is
automatically consistent because the same equation form holds in every
admissible frame (verified for arbitrary `ξ`). Primary classification:
`DERIVED_FROM_VERIFIED_DEFINITIONS`. The cited source equations and C6c are
supporting evidence.

## 19. Pressure-gradient transformation

From Sec. 9: `𝒫^(i)_a[n_2] = 𝒫^(i)_a[n_1] − aΘc²_s(i)ξ_a + O(2)` — the
pressure-gradient variable *does* pick up a sound-speed term under a frame
change (coordinate check C6d). This is precisely the mechanism the 1D-C
audit feared could "reshuffle c_s²Δ-terms between the density and tilt
rows". The resolution: the density-gradient shift is `−aΘ(1+w_(i))ξ_a`
(Sec. 18), and therefore the closure combination transforms as

    (1+w_(i))𝒫^(i)_a − c²_s(i)𝒟^(i)_a  →
    (1+w_(i))[𝒫^(i)_a − aΘc²_s(i)ξ_a] − c²_s(i)[𝒟^(i)_a − aΘ(1+w_(i))ξ_a]
    = (1+w_(i))𝒫^(i)_a − c²_s(i)𝒟^(i)_a   (exactly, at first order).

The two shifts cancel **because** `c²_s(i) := ṗ^(i)/ρ̇^(i)`: the shift of
any scalar's gradient is its background time derivative times `ξ`, so the
combination `D_µp − (ṗ/ρ̇)D_µρ` is frame-invariant at first order by
construction.
Verified in coordinates (check C6e, both signatures). Hence **the
barotropic closure (4.13) is exactly frame-invariant at first order, and no
frame change can alter the `c_s²` self-coupling it induces** — [GM]'s
"(valid) in any observer frame n^µ" statement for (4.13) is confirmed.
Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`. C6d/C6e are
supporting symbolic evidence.

## 20. Sound-speed derivative convention

`c²_s(i) = ṗ^(i)/µ̇^(i)` in [DBE] (p. 58 verbatim), [BDE] (29), and [GM]
((2.9) text, (4.13) text: "equivalently as ∂p^(i)/∂ρ^(i) or as
ṗ^(i)/ρ̇^(i)", "evaluated for the background"). The dot is the covariant
derivative along the respective congruence — but at background level all
first-order-tilted congruences share the same time derivative (frame
differences act on background quantities as `ξ·`(spatial gradient) `= 0`).
Hence the same numeric background function `c²_s,eff,D(t) =
ṗ_eff/ρ̇_eff` (the corrected Phase 1B tracker quantity) serves every frame
in this audit; no `ẇ` term and no derivative-convention ambiguity is
introduced by the frame mapping. In Buchert-average terms both dots are the
volume-time derivative of the averaged sources — the substitution of
averaged background values commutes with the frame transformation because
the transformation only reshuffles first-order variables while background
coefficients are frame-common (this addresses transformation question 11 of
the specification).

The pressure and sound-speed taxonomy used in the adjudication is:

| quantity | definition and scope |
|---|---|
| total-fluid background sound speed | `c_s² := ṗ/ρ̇ = (1/h)Σ_i h_i c²_s(i)`; DBE (51) |
| component background/adiabatic sound speed | `c²_s(i) := ṗ_i/ρ̇_i`; equal to `(∂p_i/∂ρ_i)_s` under the stated adiabatic-background assumptions |
| GM effective-component sound speed | `c²_s,eff := ṗ_eff/ρ̇_eff`, the preceding component coefficient applied to the postulated effective fluid |
| rest-frame perturbative sound speed | coefficient relating `δp_i` and `δρ_i` in the component rest frame; in a general nonadiabatic model it need not equal `ṗ_i/ρ̇_i` |
| coordinate pressure perturbation | `δp_i`, a gauge-dependent coordinate perturbation, not itself a CGI gradient |
| entropy/nonadiabatic pressure perturbation | the residual `w_i𝓔_i` in GM (2.18)/DBE (48) after the adiabatic part is removed |
| GM CGI pressure gradient | `𝒫^(i)_a := (a/h_i)D_ap_i`, enthalpy-normalised; GM (2.2) |
| BDE pressure gradient | `P_a := (a/p)⁽³⁾∇_ap`, pressure-normalised; BDE (27), not identical to GM's variable |
| rescaled pressure variable | `𝒫̃_i := (1+w_i)𝒫_i` |
| GM barotropic closure | `𝒫̃_eff = c²_s,eff Δ_eff`, GM (4.13), i.e. the zero-entropy specialization within GM's postulate |

The boost calculation of Sec. 19 proves only a first-order perturbative
identity:

    (1+w_i)𝒫_i − c²_s(i)𝒟_i

is frame-invariant **at first order**. It is not asserted as a nonlinear
identity or as an identification of a general rest-frame perturbative sound
speed with the background adiabatic derivative.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`. Supporting algebra
is `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 21. Effective-fluid applicability

The effective (backreaction) fluid is **not** a fundamental fluid: [GM]
state that its energy-momentum contribution "is only uniquely defined at
the background level (as ρ_D^(eff)(t), p_D^(eff)(t))" and that "in a
perturbed setting, further assumptions must be made in order to
characterise the spatial gradients of its energy density and pressure, and
its velocity relative to the dust flow, besides considering, as above, that
it remains a perfect fluid" (printed p. 17); the two-fluid description is
"a set of two non-interacting perfect fluids, one being pressureless"
(p. 14). The frame-mapping derivation of this report is therefore
**conditional on [GM]'s own perturbative postulate**: the effective fluid
is treated as a separately conserved, tilted perfect fluid with a barotropic
closure. Under these postulates it transforms as an ordinary component
under all frame changes (Secs. 8–9); no additional backreaction-specific
term arises at first order **within the postulated framework**. Whether the
postulate itself faithfully represents perturbed Buchert backreaction is a
physics question outside D3 and outside this phase's scope (it belongs to
the 1D-C uncertainty taxonomy as a model-import item). The D3 question —
which printed equation follows from [GM]'s own framework — is unaffected by
this caveat. Primary classification of the postulate as a stated assumption:
`VERIFIED_FROM_PRIMARY_SOURCE`. The distinct conclusion about its physical
adequacy has primary classification `REQUIRES_AUTHOR_INPUT` and is outside
this equation-level audit.

## 22. General-frame density equation

Route-1 derivation (displayed; no [GM] Sec. 4 equation used as input).
Component energy conservation in the observer frame `n` at first order
([GM] (2.8) = [DBE] (42) with `ε = 0`):

    ρ̇^(i) + Θ(ρ^(i)+p^(i)) + h^(i) D^µV^(i)_µ ≃ 0 .                    (E)

Component momentum conservation ([GM] (2.9) = [DBE] (43)–(45) with
`f = ε = Π = 0`):

    a_µ ≃ −(1/a)𝒫^(i)_µ − F^(i)_µ ,   F^(i)_µ := V̇^(i)_µ + (1/3 − c²_s(i))ΘV^(i)_µ .   (M)

Linear commutator for a scalar `f` with nonzero background evolution
(derived in Sec. 9 context; verified as coordinate check C1):

    h_µ^ν (D_ν f)˙ = D_µ ḟ + ḟ a_µ − (Θ/3) D_µ f + O(2) .              (K)

Assemble `𝒟̇^(i)_µ` for `𝒟^(i)_µ = (a/ρ^(i))D_µρ^(i)`:

    𝒟̇^(i)_µ = (Θ/3)𝒟^(i)_µ − (ρ̇^(i)/ρ^(i))𝒟^(i)_µ + (a/ρ^(i))(D_µρ^(i))˙
             = (Θ/3)𝒟^(i)_µ + Θ(1+w_(i))𝒟^(i)_µ
               + (a/ρ^(i))[D_µρ̇^(i) + ρ̇^(i)a_µ − (Θ/3)D_µρ^(i)] .

Insert `D_µρ̇^(i)` from the gradient of (E),
`D_µρ̇^(i) = −(ρ^(i)+p^(i))D_µΘ − ΘD_µρ^(i) − ΘD_µp^(i) −
h^(i)D_µ(D^νV^(i)_ν)`, use `ρ̇^(i) = −Θh^(i)` in the `ρ̇^(i)a_µ` term, and
eliminate `a_µ` with (M):

    𝒟̇^(i)_µ = w_(i)Θ𝒟^(i)_µ − (1+w_(i))𝒵_µ + aΘ(1+w_(i))F^(i)_µ
               − a(1+w_(i))D_µD^νV^(i)_ν ,

i.e. exactly [GM] (2.14) as printed,

    𝒟̇_µ^(i) − w_(i)Θ𝒟_µ^(i) + (1+w_(i))𝒵_µ − aΘ(1+w_(i))F_µ^(i)
    + a(1+w_(i))D_µD^αV_α^(i) ≃ 0 ,                                    [GM (2.14)]

**valid for an arbitrary admissible observer frame** — [GM] derived it with
`n^µ` "kept unspecified" (p. 8), [BDE] fn. 14/(44) state the same
frame-generality, and this phase proves it: symbolic check S1 verifies the
assembly above, and coordinate check C4 verifies (2.14) directly from
`∇_νT^(i)µν = 0` on a perturbed FLRW metric with arbitrary gauge functions
(φ, ψ, B) **and an arbitrary first-order observer velocity** — no Einstein
equations, no frame fixing, no use of (2.14) itself. The 1D-C residual
concern that [GM]'s generic-frame (2.22) was "a scope generalisation made
without derivation shown" is closed: the generalisation is correct.
Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`. S1/C4 and the
printed (2.14) are supporting symbolic and source evidence, respectively.

## 23. Dust-frame density equation

Specialise (2.14) to `i = eff`, `n = u_d`: the dust is geodesic (`a_µ ≃ 0`,
Sec. 17), so (M) for the effective component gives
`F^(eff)_µ = −(1/a)𝒫^(eff)_µ` ([GM] (4.8) scalarised; the `𝒫 + aF = 0`
relation). Substituting,

    𝒟̇_µ^(eff) − w_effΘ𝒟_µ^(eff) + (1+w_eff)𝒵_µ + Θ(1+w_eff)𝒫_µ^(eff)
    + a(1+w_eff)D_µD^αV_α^(eff) ≃ 0 ,

whose scalarised form is exactly printed [GM] (4.6). The sign of the
pressure term (`+Θ(1+w_eff)𝒫^(eff)`) is forced by the two independently
verified inputs (2.14) and (2.9)|`a_µ=0`; no sign freedom remains.
Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`. Printed (4.6)
is supporting source evidence.

## 24. Barotropic closure substitution

The closure [GM] (4.13), `𝒫̃^(eff) = c²_s(eff)Δ^(eff)` with
`𝒫̃ := (1+w_eff)𝒫`, is the `𝓔 = 0` case of the general decomposition
(2.18) `(1+w_(i))𝒫^(i) = c²_s(i)𝒟^(i) + w_(i)𝓔^(i)`, which is [DBE] (48)
divided by `h_(i)` (Sec. 11). It is exactly frame-invariant at first order
(Sec. 19, C6e), so it may be imposed in any frame with the same content.
Substituting into the frequency-space (4.10) (Sec. 25) gives

    Δ̇^(eff) = (w_eff − c²_s(eff))ΘΔ^(eff) − (1+w_eff)𝒵 + (k²/a)Ṽ^(eff) .

Dependence audit of the resulting sign (specification Sec. 13): the
`−c²ΘΔ` contribution (i) does not depend on which side terms are written
(pure algebra; S3); (ii) follows from the definition `𝒫̃ = (1+w)𝒫` with
`1+w_eff > 0` on the tracker (no sign flip; and the same result holds
working with unrescaled `𝒫`); (iii) uses `𝒫^(i) = (a/h^(i))D_µp^(i)` — an
enthalpy-normalised gradient whose sign convention is fixed by (2.2) and
anchored to [DBE] (48); (iv) is independent of the flux-sign convention
(flux enters only the tilt-Laplacian term); (v) is signature-robust (the
self-coupling is built from signature scalars; both signatures checked,
Sec. 32); (vi) is independent of the Laplacian sign convention (the
Θ-self-coupling carries no Laplacian; fn. 8 affects only the `k²` tilt
term, whose sign was separately verified); (vii) is independent of the `Z`
definition (`𝒵` enters its own separate term); (viii) is frame-independent
(closure invariance, Sec. 19); (ix) uses the background `ṗ/ρ̇` common to
all frames (Sec. 20); (x) generates no `ẇ` term (S3 coefficient
inventory). All ten are algebraic rearrangements or verified conventions;
none is a genuine convention change that could flip the sign.
Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`. S3 is
supporting symbolic evidence.

## 25. Scalarisation and harmonic reduction

From the vector (4.6)-form to the scalar frequency-space system:

- **divergence scalars**: `Δ^(i) := aD^µ𝒟^(i)_µ`, `𝒵 := aD^µ𝒵_µ`,
  `V^(i) := aD^µV^(i)_µ`, `𝒫^(i) := aD^µ𝒫^(i)_µ` ([GM] (2.20)–(2.21) =
  [BDE] (40));
- **commutation**: for first-order vectors the printed identities [BDE]
  (63), `a⁽³⁾∇_aV̇_b = (a⁽³⁾∇_aV_b)˙`, make scalarisation commute with the
  evolution at first order — scalarisation introduces no new terms and no
  sign (the boundary/commutator content is exactly (63); verified for the
  assembled equation by the coordinate check, which never scalarises);
- **harmonics**: BDE (74), journal p. 44, gives explicitly
  `⁽³⁾∇²Q = −(k²/a²)Q` in the relevant FLRW scalar-harmonic convention;
  BDE footnote 21 classifies the harmonic sectors, and the relevant
  footnote-22 clarification distinguishes the conformal spatial operator
  from the physical Laplacian and supplies the displayed `a⁻²`. This agrees
  with [GM] footnote 8 and the negative-Laplacian convention frozen since
  1C-A. The tilt term
  `a(1+w)⁽³⁾ΔV^(eff) → a(1+w)(−k²/a²)V^(eff) = −(k²/a)Ṽ^(eff)` — one
  factor `a` from the equation, `a^{-2}` from the eigenvalue, and the
  `(1+w)` absorbed into `Ṽ`; powers of `a` and `k` verified symbolically
  (S2);
- **state ordering**: `(Δ^(d), 𝒵, Δ^(eff), tilt)` exactly as the frozen
  Phase 1C solver state;
- **`𝒵 = −Δ̇^(d)`**: the `i = dust` instance of (2.14) in the dust frame
  (`w_d = 0`, `F^(d) = V^(d) = 0`) is `Δ̇^(d) + 𝒵 ≃ 0` — printed (4.5)/
  (4.9)/(4.14) — reproducing the Phase 1C sign convention `Z = −Δ̇^(d)`.

Scalarisation itself introduces no D3-relevant sign: the self-coupling
term `w_(i)Θ𝒟^(i)_µ` maps to `w_(i)ΘΔ^(i)` with coefficient unchanged
(S2 residual zero). The result is exactly printed [GM] (4.10):

    Δ̇^(eff) − w_effΘΔ^(eff) + (1+w_eff)𝒵 + Θ𝒫̃^(eff) − (k²/a)Ṽ^(eff) ≃ 0 .

This BDE (74)/footnote addition is a source-completeness correction only and
does not change A33. Primary classification:
`DERIVED_FROM_VERIFIED_DEFINITIONS`. Supporting evidence: BDE (63), (74),
footnotes 21–22, GM footnote 8, and GM (4.10) are
`VERIFIED_FROM_PRIMARY_SOURCE`; S2 is `SYMBOLICALLY_VERIFIED`.

## 26. Rescaled-tilt derivation

Independent derivation of the `Ṽ`-form tilt equation: start from the
dust-frame momentum relation (4.8),
`V̇^(eff) + Θ(1/3 − c²_s(eff))V^(eff) + (1/a)𝒫^(eff) ≃ 0`; define
`Ṽ := (1+w_eff)V^(eff)`, `𝒫̃ := (1+w_eff)𝒫^(eff)`; use the background
identity `ẇ_eff = −Θ(1+w_eff)(c²_s(eff) − w_eff)` — itself derived here
(check S4) from `ρ̇_eff = −Θ(1+w_eff)ρ_eff` (the effective conservation
law, [GM] (3.17) at background) and `c²_s(eff) = ṗ_eff/ρ̇_eff`, both in
volume-average time along the dust congruence. Then

    Ṽ̇ = (1+w)V̇ + ẇV = −Θ(1/3 − w)Ṽ − (1/a)𝒫̃ ,

exactly printed (4.12), "eliminating the explicit c²_s,eff dependence" as
[GM] state; with the closure it becomes printed (4.17),
`Ṽ̇ + Θ(1/3 − w_eff)Ṽ + (1/a)c²_s(eff)Δ^(eff) ≃ 0`. Primary
classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`. S4 and printed
(4.12)/(4.17) are supporting symbolic and source evidence.

## 27. Unrescaled-tilt derivation

Independent derivation of the `V`-form: keep (4.8) with the closure
`𝒫^(eff) = c²_s(eff)Δ^(eff)/(1+w_eff)`:

    V̇^(eff) = −(Θ/3)(1 − 3c²_s(eff))V^(eff) − c²_s(eff)Δ^(eff)/(a(1+w_eff)) ,

and the density-row tilt term `−(k²/a)Ṽ = −(k²/a)(1+w_eff)V`. This
reproduces the Phase 1C `unrescaled_V` rows
`A34 = (k²/a)(1+w)`, `A43 = −c²/(a(1+w))`, `A44 = (Θ/3)(3c² − 1)`.
**Equivalence of the two forms, every row, both branches** (check S5): with
`T = diag(1,1,1,1+w_eff)` and the S4 identity, the exact matrix transform
`A_Ṽ = (Ṫ + T A_V)T^{-1}` reproduces all sixteen entries of the `Ṽ`-form
matrix for `A33 = (w+c²)Θ` **and** for `A33 = (w−c²)Θ`; residual zero in
every entry. The tilt normalisation therefore cannot influence the D3
adjudication (consistent with the frozen 1C-B2 numerical equivalence), and
the normalisation-independent combination `A34·A43 = −c²k²/a²` holds in
both forms. Equivalence does not fail for either candidate.
Primary classification: `SYMBOLICALLY_VERIFIED`. Frozen 1C-B2 numerical
equivalence is supporting context, not a second primary classification.

## 28. Coordinate conservation-law realisation and evidence dependencies

This is a coordinate realisation of the same component-conservation premise
used by the abstract covariant assembly, not a logically independent physical
proof. It never uses [GM] Sec. 4, [DBE] §3, or either D3 candidate as input.
The linearly perturbed flat-FLRW scalar ansatz is

    ds² = −(1+2φ)dt² + 2aB dt dx + a²(1−2ψ)δ_ij dx^i dx^j ,
    n^µ = (1−φ, v_n/a, 0, 0),
    u_i^µ = (1−φ, v_i/a, 0, 0),

with arbitrary first-order functions `φ(t,x)`, `ψ(t,x)`, `B(t,x)`, observer
velocity `v_n(t,x)`, and component velocity `v_i(t,x)`. Direct expansion
gives

    δΘ_n = −3ψ̇ − 3Hφ + (∂_x v_n)/a,
    a_x = ∂_xφ + a(Ḃ+HB) + a(v̇_n+Hv_n),
    D_xρ_i = ∂_xδρ_i + a(B+v_n)ρ̇_i,
    D_xp_i = ∂_xδp_i + a(B+v_n)ṗ_i,
    V_(i)x = a(v_i−v_n),
    D_aV_i^a = ∂_x(v_i−v_n)/a.

The direct time and spatial projections of the independently constructed
`∇_νT_i^{µν}=0` reduce, at first order, to

    E_i := ρ̇_i + Θ(ρ_i+p_i) + (ρ_i+p_i)D_aV_i^a = 0,
    M_(i)x := a_x + 𝒫_(i)x/a + F_(i)x = 0,
    F_(i)x := V̇_(i)x + (1/3−c²_s(i))ΘV_(i)x.

No Einstein equation is imposed. Substituting the six displayed coordinate
quantities and `E_i=M_(i)x=0` into

    R_C4,x := 𝒟̇_(i)x − w_iΘ𝒟_(i)x + (1+w_i)𝒵_x
              − aΘ(1+w_i)F_(i)x
              + a(1+w_i)D_xD_aV_i^a

gives the complete symbolic statement

    R_C4,x ≡ 0

coefficient by coefficient for arbitrary `φ,ψ,B,v_n,v_i,δρ_i,δp_i` after
the background component conservation law is applied. This reproduces GM
(2.14), corroborates dust-frame geodesicity in this scalar sector after
setting `n=u_d`, and reproduces
the C6 density/pressure shifts and closure-combination invariance **at first
order**.

The one-dimensional flat scalar sector is sufficient to corroborate the
scalar-mode sign, observer-velocity dependence, and A33 coefficient. It is
not a proof of vector modes, tensor modes, curved-space harmonic identities,
or global Buchert averaging.

The dependency graph is:

    component conservation + perfect-fluid decomposition + commutator
      ├─ abstract covariant assembly → general equation → dust → closure
      ├─ coordinate realisation ─────→ same general equation → dust → closure
      ├─ GM transcription (2.14) ────→ (4.6) → (4.10) → closure
      └─ DBE transcription (46)+(47) → (49)/(55)

    GM (4.10) + constant-w closure → GM (4.29)  [partially independent]
    printed GM (4.15)              → GM (4.19) → Appendix A [dependent]

The accurate evidence description is: **Four agreeing realizations, with a
shared component-conservation premise, two independent primary-source
transcriptions, and one partially independent internal GM consistency
check.** GM and DBE are independent transcription paths but share the same
physical conservation premise; the abstract and coordinate calculations are
two realizations of that premise.

Primary classification: `SYMBOLICALLY_VERIFIED`. The displayed derivation is
the reproducible evidence; the original scratch script is corroborating
provenance, not primary evidence.

## 29. Candidate A33 expressions

For the state `(Δ^(d), 𝒵, Δ^(eff), Ṽ^(eff))`, the effective-fluid density
row determined by the derivation is

    Δ̇^(eff) = (w_eff − c²_s(eff))Θ Δ^(eff) − (1+w_eff)𝒵 + (k²/a)Ṽ^(eff) ,

with the complete coefficient inventory asserted symbolically (S3): the
`Δ^(eff)` coefficient is exactly `(w_eff − c²_s(eff))Θ`; the `𝒵` and `Ṽ`
coefficients are `−(1+w_eff)` and `k²/a`; the `Δ^(d)` coupling is zero; and
**no additional frame, flux, acceleration, tilt, or
background-derivative (`ẇ`, `ċ²`) term appears**. The three candidate
outcomes of the specification therefore resolve as:

- `(w_eff − c²_s(eff))Θ` — **the derived coefficient** (all four agreeing
  realizations with the shared premise of Sec. 28);
- `(w_eff + c²_s(eff))Θ` — printed (4.15); differs from the derivation by
  the RHS/A33 coefficient difference
  `A33_printed − A33_derived = +2c²_s(eff)Θ`; equivalently, the printed
  left-hand side evaluated on a derived-branch solution has residual
  `R_printed_on_derived = −2c²_s(eff)ΘΔ^(eff)` (S3); it is not reproducible
  from any inspected or derived equation set;
- "another expression with extra terms" — **excluded** by the coefficient
  inventory.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`. Supporting
evidence: S3 is `SYMBOLICALLY_VERIFIED`.

## 30. Eq. (4.19) consistency analysis

Write `D=Δ^(eff)`, `δ=Δ^(d)`, `w=w_eff`, and `c=c²_s(eff)` (so `ċ` means
the derivative of the background quantity `c²_s(eff)`). The complete
symbolic form transcribed from printed [GM] (4.19), p. 18, is

    D̈ + (2/3 − 2w − c)ΘḊ
      + { (2/3)Θ²[−2w + c(1+3w)] − Θċ
          + (4πGρ_d−Λ)(w+c)
          − 4πGρ_eff(1−3w²+2c) + c k²/a² }D
      ≃ 4πGρ_d(1+w)δ − c(1+w)Θδ̇ .                    (4.19)

S6 assumes the closed printed-branch first-order system {(4.14), printed
(4.15), (4.16), (4.17)},
`ρ̇_d=−Θρ_d`, `ρ̇_eff=−Θ(1+w)ρ_eff`,
`ẇ=−Θ(1+w)(c−w)`, and the standard background Raychaudhuri equation
`Θ̇=−Θ²/3−4πG[ρ_d+(1+3w)ρ_eff]+Λ`. Direct differentiation and elimination
then give the explicit on-shell result

    R_S6 := LHS_(4.19) − RHS_(4.19) ≡ 0 .

This zero proves only internal consistency with the printed branch. The
check is non-discriminating because [GM] explicitly derives (4.19) by
eliminating variables through printed (4.15). On the derived branch the
printed expression has a nonzero residual, while the distinct derived-branch
second-order analogue reproduces the frozen 1C-B2 `C_derived` form at
`Λ=0`; that analogue is not printed (4.19).

Appendix A is likewise dependent: its opening on printed p. 51 explicitly
derives (A.1) from (4.18) and (4.19). Primary classification:
`DERIVED_FROM_VERIFIED_DEFINITIONS`. Supporting evidence: the on-shell
algebra is `SYMBOLICALLY_VERIFIED`.

## 31. Eq. (4.29) discriminating analysis

Write `D=Δ^(eff)`, `δ=Δ^(d)`, `V=Ṽ^(eff)`, and `w=w_eff`. The complete
encoded target is printed [GM] (4.29), p. 20:

    D̈ + (2/3)ΘḊ + (k²/a²)w(D−aΘV)
      ≃ 4πG(1+w)[(1+3w)ρ_eff D + ρ_d δ] .              (4.29)

S7 uses exactly the parent equations named in [GM] Sec. 4.4:
`(4.9)`, `(4.10)`, `(4.11)`, and `(4.12)`, with
`c²_s(eff)=w=const` and the adiabatic closure `𝒫̃_eff=wD`, plus the standard
background component-conservation and Raychaudhuri identities. It does not
use (4.15) to obtain the derived-chain result. On that chain,

    R_S7,derived := LHS_(4.29) − RHS_(4.29) ≡ 0 .

For the printed-(4.15) chain, define `g4=4πG`. The independently reproduced
nonzero residual is

    R_S7,printed
      = −(2w/3)[−3DΛ − DΘ² + 3D g4ρ_d + 9D g4ρ_eff w
                 + 3D g4ρ_eff − 3ḊΘ] ,

which is generically nonzero. This check is only **partially independent**:
it is an internal GM consistency check downstream of (4.10), while remaining
derivationally independent of disputed (4.15). GM (4.19) and Appendix A are,
by contrast, dependent descendants of printed (4.15).

The exact equation discrepancy is reported without conflating signs:
`A33_printed−A33_derived=+2c²Θ`, whereas the printed left-hand-side residual
on a derived solution is `−2c²ΘΔ^(eff)`. Primary classification:
`SYMBOLICALLY_VERIFIED`. Supporting interpretation is
`DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 32. Symbolic verification ledger

The original scratch scripts are inaccessible implementation provenance, not
primary evidence. The decisive inputs, equations, and residuals are displayed
in Secs. 22, 28–31 so that the checks below can be reproduced without those
files. The scripts remained in the ignored scratchpad and were never part of
the package.

**`phase1ddt_coordinate_check.py`** — perturbed-FLRW coordinate
verification; arbitrary gauge (φ, ψ, b), arbitrary observer `v_n`,
arbitrary second observer `v_n2`, two tilted fluids; first-order
truncation by differentiation in ε; background continuity and
`c² := ṗ/ρ̇` imposed as substitution rules (including chained second
derivatives). Checks and results (papers' signature (−,+,+,+) / flipped
(+,−,−,−)):

| check | content | inputs | expected | actual |
|---|---|---|---|---|
| C1 | linear commutator (K) | geometry only | 0 | 0 / 0 (with the `ḟa_µ` term sign `+`/`−` respectively — the flip is a documented signature dependence) |
| C2 | GM (2.8) ≡ n-projected `∇T^(e)=0` | conservation | 0 | 0 / 0 |
| C3 | GM (2.9) ≡ h-projected `∇T^(e)=0` | conservation | exact GM form | exact (A +, F +, overall +) / covector-flipped pattern (A −, F −, overall −) |
| C3b | `Θ` vs `Θ^(e)` and `∇·V` | geometry | — | `Θ = Θ^(e) − ∇·V^(e)` exactly (both signatures); printed (2.5) `+` sign inconsistent (Sec. 33) |
| C4 | GM (2.14), arbitrary observer; full ansatz and residual in Sec. 28 | conservation only | 0 | 0 / (F-term covector-flipped, divV unflipped) |
| C5 | dust-frame geodesy; `V^(d)=0` | dust conservation | 0 | 0 / 0 |
| C6a | `ρ(n_1) = ρ(n_2)` at first order | geometry | 0 | 0 / 0 |
| C6b | flux boost `q_x = h^(e)V^(e)_x` | geometry | 0 | 0 (papers only) |
| C6c | `Δ`-shift law `−aΘ(1+w)ξ` | geometry | 0 | 0 / 0 (signature-aware sign) |
| C6d | `𝒫`-shift law `−aΘc²ξ` | geometry | 0 | 0 / 0 (signature-aware sign) |
| C6e | closure combination frame-invariant at first order | geometry | 0 | 0 / 0 |

**`phase1ddt_system_checks.py`** — covariant/algebraic chain:

| check | content | expected | actual |
|---|---|---|---|
| S1 | covariant realisation of the shared conservation premise ⇒ (2.14) | 0 | 0 |
| S2 | (4.6) → (4.10) rescaling + harmonics (powers of a, k) | 0 | 0 |
| S3 | (4.10)+(4.13) ⇒ A33 = `(w−c²)Θ`; coefficient inventory; `A33_printed−A33_derived=+2c²Θ`; `R_printed_on_derived=−2c²ΘΔ` | all pass | all pass |
| S4 | `ẇ = −Θ(1+w)(c²−w)` from conservation + `c² := ṗ/ρ̇` | 0 | 0 |
| S5 | V ↔ Ṽ exact matrix equivalence, all 16 entries, both branches | 0 | 0 (both) |
| S6 | complete printed (4.19) and assumptions in Sec. 30; printed-branch on-shell residual | 0 | 0; dependent/non-discriminating; distinct derived analogue at `Λ=0`: 0 |
| S7 | complete printed (4.29), assumptions, and both residuals in Sec. 31 | 0 / nonzero | derived chain 0; printed-chain residual equals the explicit Sec. 31 expression |
| S8 | [DBE] (46)+(47) ⇒ (49); interactions off ⇒ (55); retained-total-variable form has explicit `3(w_i−c²_i)H`; total term is a cross-coupling in that representation and may contain `D_i` if the total sum is expanded; interactions-ON reconciliation uses (29)+(34) | all pass | all pass |

Honesty statements (required): a zero residual proves only the encoded
equations; every encoded printed equation was transcribed from page renders
inspected in this phase (the transcription step is anchored by Secs. 4–5
and 10, not by the scripts). No check assumes the sign it claims to test:
C4/S1 derive the density equation without any D3 input; S3's inventory is
computed, not asserted from a candidate; S6/S7 test both branches
symmetrically. The two scripts are different encodings (coordinate-based
versus covariant/algebraic) of one shared component-conservation premise;
they are not counted as logically separate physical evidence. The
retained 1D-C scripts (`phase1dc_d3_symbolic.py`,
`phase1dc_audit_d3_recheck.py`) were re-read but not reused; their checks
are subsumed by S3/S8. Classification: `SYMBOLICALLY_VERIFIED`.

## 33. Source ambiguities and unresolved dependencies

Visually ambiguous or defective printed symbols found (none sign-critical
for D3):

1. **[BDE] (19)** (p. 38): printed `µ̇ + 3µH(µ + p) = 0` — dimensionally
   inconsistent as printed (spurious `µ` or `(µ+p)` for `(1+w)`);
   resolved by [BDE] (45) and [DBE] (28), which print the standard form.
   Non-propagating typo (zoom-verified).
2. **[GM] (2.21)** (printed p. 9): the combined-fluid
   `F := aD^µF_µ ≃ V̇ + (1/3 − c²_s(i))ΘV` carries a component subscript
   `s(i)` where the combined-fluid `c_s²` is expected (cf. (2.11) text).
   Non-propagating (the combined `F` is not used in the dust-frame
   two-fluid chain); zoom-verified.
3. **[GM] (2.5)** (printed p. 6): printed `Θ ≃ Θ^(i) + ∇^µV^(i)_µ`; the
   exact first-order relation computed in coordinates (C3b, both
   signatures) is `Θ = Θ^(i) − ∇^µV^(i)_µ`. Non-propagating for D3 ((2.5)
   is not used in the (2.14)→(4.15) chain); recorded as a new documented
   observation for the authors (Sec. 37).
4. **[GM] (2.12)/(2.13)** `Λ` coefficients — known finding F5 (frozen
   1C-A); `Λ = 0` here; S6 used the standard Raychaudhuri.
5. **[DBE] (49) interaction bookkeeping**: reconciling (46)+(47) with (49)
   with interactions ON requires substituting the total momentum equation
   (29) with (34) (S8); with that substitution the match is exact. Not an
   ambiguity of the printed equations, but recorded because the 1D-C
   check had only verified the interactions-off case.

Unresolved external dependencies remaining after this phase: none for the
D3 equation question itself. The following remain open and are *not* D3:
authorial intent/errata status (`REQUIRES_AUTHOR_INPUT`, Sec. 37); the
physical adequacy of the effective-fluid perturbative postulate (Sec. 21);
and every non-D3 frozen unresolved item (F3, F4, F7, h-convention,
spectrum/normalisation blockers) exactly as catalogued in the 1D-C
inventory, unchanged by this phase.

## 34. Exact D3 adjudication checklist

The independent compliance audit found documentation/source-completeness
defects in the pre-correction presentation, not a mathematical contradiction.
This revision closes those defects while preserving the distinction between
equation-level sufficiency and documentation readiness:

| # | condition | equation-level status | corrected evidence/documentation status |
|---|---|---|---|
| 1 | every relevant frame explicitly defined | met | Sec. 7 retains seven distinct frames; `u_E` and `u_N` remain separate |
| 2 | complete first-order frame transformation performed | met | Sec. 9 now declares `ξ=u_destination−u_source`, gives every law and five required source→destination instances; Secs. 16–19 and C6 corroborate |
| 3 | component and total variables distinguished | met | Sec. 13 and S8 now qualify the retained-total-variable cross-coupling and its possible `D_i` content after expansion; GM dust-frame A33 is unchanged |
| 4 | pressure and sound-speed definitions mapped | met | Secs. 11, 19, 20, 24 now distinguish ten pressure/sound concepts and qualify closure invariance at first order |
| 5 | scalarisation explicit | met | Secs. 4, 10, 25 and S2 now cite BDE (63), (74), footnotes 21–22, GM footnote 8, and all powers of `a,k` |
| 6 | both tilt normalisations checked | met | Secs. 26–27; S5 gives all 16 entries for both branches and remains non-discriminating |
| 7 | conservation-law derivations agree | met | Secs. 22/28 display abstract and coordinate realizations of one shared premise; GM/DBE are independent transcription paths; dependency graph explicit |
| 8 | all sign-critical source equations visually unambiguous | met | Secs. 5, 10, 33; all non-D3 printed defects are isolated and do not enter the D3 chain |
| 9 | no uninspected source equation still required | met | Secs. 4/10 add the compliance audit's visual verification of BDE (74), footnote 21, and footnote 22; the derivation now has complete cited harmonic support |
| 10 | no unresolved convention can reverse the result | met | Secs. 9, 19, 24–25, 32: explicit boost direction, first-order closure invariance, both signatures, and Laplacian/tilt/Z/flux conventions are non-reversing |

All ten equation-level criteria support `RESOLVED_DERIVED_4_10`. The
pre-correction documents did not yet satisfy every documentation criterion;
the corrections are the additions and qualifications cited in the final
column. No runtime or scientific-code consequence follows automatically.

## 35. Final D3 verdict

**`RESOLVED_DERIVED_4_10`**

Precise content of the verdict (seven-field conclusion object in the JSON):
within [GM]'s own stated framework — two non-interacting perfect fluids
(irrotational pressureless dust + effective barotropic perfect fluid),
dust-energy-frame observer, CGI first-order perturbations, closure (4.13) —
the displayed conservation-law derivation, explicit frame transformation,
and primary-source reconstruction all yield the
dust-frame effective-fluid density equation

    Δ̇^(eff) − (w_eff − c²_s(eff))ΘΔ^(eff) + (1+w_eff)𝒵 − (k²/a)Ṽ^(eff) ≃ 0 ,

i.e. the `derived_4_10` coefficient, with no additional terms. Printed
(4.15) is not reproducible from any inspected or derived equation set. The
two distinct comparison quantities are

    A33_printed − A33_derived = +2c²_s(eff)Θ,
    R_printed_on_derived = −2c²_s(eff)ΘΔ^(eff).

[GM]'s own Sec. 4.4 ((4.29)) is downstream of (4.10), zero-residual on the
derived chain, and only partially independent; (4.19)/App. A are dependent
internal descendants of printed (4.15).

The Markdown/JSON conclusion fields are aligned as follows:

| field | final content |
|---|---|
| verdict | `RESOLVED_DERIVED_4_10` |
| primary classification | `DERIVED_FROM_VERIFIED_DEFINITIONS` |
| source scope | visually inspected GM (2.2)–(2.24), (4.1)–(4.19), (4.29), and Appendix A opening; DBE pp. 55–61; BDE pp. 38–45, 48 including (74), fn. 21, fn. 22; displayed Secs. 22, 28–31; independent compliance audit; scratch ledgers only corroborating |
| assumptions | GM's two non-interacting components; irrotational pressureless dust; effective barotropic perfect fluid separately conserved at first order; dust-energy observer; CGI linear perturbations; closure (4.13); background `c²_s,eff=ṗ_eff/ρ̇_eff` |
| derivation summary | four agreeing realizations with a shared component-conservation premise; abstract and coordinate forms are two realizations of that premise; GM/DBE are independent primary-source transcription paths; GM (4.29) is partially independent/downstream of (4.10); GM (4.19)/Appendix A depend on printed (4.15) |
| convention dependencies | robust against the checked signature, Laplacian, tilt-normalisation, pressure-normalisation, `𝒵`, flux-direction, and background-derivative conventions; closure-combination invariance is asserted only at first order |
| implementation consequence | none here: both branch labels remain mandatory, neither is a default, and historical paper/notebook reproduction still requires `printed_4_15`; runtime changes require a separate approved phase |
| evidence needed to change status | a demonstrated error in the displayed derivation/checks, or evidence of a different intended framework/closure/variable definition that derives printed (4.15) |

Scope limits of the verdict, stated explicitly: (i) it resolves the
*equation*, not the authors' *intent* — what the authors meant to print,
and whether they will issue an erratum, remains `REQUIRES_AUTHOR_INPUT`;
(ii) it is conditional on [GM]'s effective-fluid perturbative postulate
(Sec. 21), which is the framework D3 is defined in; (iii) it does **not**
select an executable default, deprecate either branch label, or alter any
frozen code or result — per the standing adjudication rules, any code
change requires a separate reviewed implementation phase; (iv) historical
reproduction of the published Fig. 3 and the pinned notebook continues to
require `printed_4_15` regardless of this verdict. Primary classification
of the verdict: `DERIVED_FROM_VERIFIED_DEFINITIONS`. Supporting evidence is
`VERIFIED_FROM_PRIMARY_SOURCE` source anchoring and
`SYMBOLICALLY_VERIFIED` machine corroboration, held separately per the
evidence policy.

Numerical corroboration (optional, non-adjudicating, no new runs): the
frozen 1C-B2/1D-B artifacts quantify the forensic reproduction spread (e.g. corrected-
background endpoint factors up to ~10² at `k = 10π`; signed relative-growth
endpoint difference −230.2 % at `2π` in the 1D-B one-factor study). These
numbers measure the *consequence* of the branch choice, not its
correctness, and played no role in the verdict.

## 36. Downstream implementation consequences

- **Frozen dual-branch B2 implementation**: unchanged, and must remain
  dual-branch. `printed_4_15` retains its indispensable role for
  reproducing the published Fig. 3, the pinned notebook, and (4.19)/App. A;
  `derived_4_10` is now the derivation-backed equation. Neither label
  becomes a runtime default; promoting the verdict into any API behaviour
  (documentation wording, warnings, or defaults) is exclusively a matter
  for a future reviewed implementation phase and is **not** recommended as
  a side effect of this report.
- **Phase 1D-B growth results**: all frozen per-branch results remain
  valid as labelled; the verdict adds interpretive weight to the
  `derived_4_10` rows but changes no number and no validity interval.
- **Forensic reproduction spread**: the two-branch numerical difference
  quantifies the consequence of the published-record discrepancy while the
  upstream paper/notebooks still use `printed_4_15`. It is not unresolved
  theoretical uncertainty inside the adjudicated GM equation chain. If a
  future analysis deliberately propagates it as a systematic associated with
  the inconsistent publication record, call it a **publication-systematic**;
  historical comparisons should continue to report both labeled branches.
- **Phase 1D-D Candidate A** (anchored density-growth diagnostic): built
  exclusively on the clean comoving and Mészáros systems, which contain no
  `c²_s` in any matrix entry and are D3-independent (frozen 1C-A). The
  verdict has **no effect** on Candidate A, and no modification of
  Candidate A is recommended.
- **Future barotropic continuous-k work**: would still require both
  branches while the published record stands, but the derivation gives a
  principled basis for labelling `derived_4_10` as the
  internally-consistent equation of [GM]'s framework in any future
  scientific analysis — subject to the separate reviewed phase rule.
- **Historical reproduction of [GM] Fig. 3**: unchanged — `printed_4_15`
  (plus the D2-corrupted sound speed in the forensic harness) remains the
  reproduction configuration.
- **Scientific communication with the authors**: the courtesy question
  (Sec. 37) can now present a complete derivation instead of a structural
  observation; it is non-blocking for this project's own work.

## 37. Updated author-input question

Status: **non-blocking courtesy verification** (D3 is resolved from
primary evidence at the equation level; only authorial intent/erratum
status remains theirs to state). This message was not sent; that is a
user/agent process declaration, not a repository-proven fact. It is retained
for possible future human-approved contact:

> Dear Dr. Galoppo and Dr. Mourier,
>
> in arXiv:2511.17160v2, Eq. (4.10) reads
> Δ̇^(eff) − w_(eff)ΘΔ^(eff) + (1+w_(eff))𝒵 + Θ𝒫̃^(eff) − (k²/a)Ṽ^(eff) ≃ 0,
> and the barotropic closure Eq. (4.13) reads 𝒫̃^(eff) = c²_s(eff)Δ^(eff).
> Substituting (4.13) into (4.10) gives the self-coupling coefficient
> (w_(eff) − c²_s(eff))Θ, whereas the printed Eq. (4.15) carries
> (w_(eff) + c²_s(eff))Θ. Thus the printed-minus-derived A33 coefficient
> difference is +2c²_s(eff)Θ; equivalently, the printed left-hand-side
> residual evaluated on a derived-branch solution is
> −2c²_s(eff)ΘΔ^(eff). We have
> carried out the complete first-order derivation from the covariant
> multifluid formalism of Dunsby, Bruni & Ellis (ApJ 395, 54) and Bruni,
> Dunsby & Ellis (ApJ 395, 34) — including the frame transformation from
> the total-matter frame used there to your dust energy frame, in which we
> confirm your Eq. (2.14) holds for an arbitrary first-order observer
> frame and that the closure (4.13) is exactly frame-invariant at first
> order — and consistently obtain the (w_(eff) − c²_s(eff))Θ form; we also
> note that your Eq. (4.29) in Sec. 4.4 follows exactly from Eqs.
> (4.9)–(4.10) with the adiabatic closure, while Eq. (4.19) and Appendix A
> are consistent with (4.15) as printed. Could you kindly confirm which
> coefficient was intended in Eq. (4.15)? We distinguish this from the
> reproduction of the published Fig. 3, which we can reproduce exactly
> with the (w_(eff) + c²_s(eff))Θ form as implemented in the released
> notebooks; our question concerns only the intended general derivation.

The unrelated printed-form issues BDE (19), GM (2.5), GM (2.21), and GM
(2.12)–(2.13) are explicitly outside the D3 evidentiary chain. They must
not be appended as cumulative support for the question above. If human
approval is later given, they should be handled in a clearly separate
optional appendix or, preferably, a separate communication. No message is
sent in this task.

## 38. Repository preservation statement

The only repository files created are the two Phase 1D-D-t reports and the
later independent compliance audit; all three remain untracked. No tracked
or frozen file was modified. The Phase 1B/1C/1D-A/1D-B/1D-C code,
tests, reports, artifacts, the upstream clone
(`590c6fd5332acb15f5683ebf392a0d7ce54983c5`), and the pinned notebook
(SHA-256 `86d2534d…afe55a`) are untouched. Both D3 branch labels remain
implemented and mandatory; no default was selected. Nothing was staged,
committed, tagged, pushed, or merged. Git can directly verify repository
state; the absence of publication or author contact is a user/agent process
declaration and is not asserted as proof of all external or historically
deleted events. All downloaded
sources, page renders, zooms, and the two scratch scripts remain in the
ignored session scratchpad. The complete Python 3.14.3 and 3.11.9 test
suites pass (337 each) after the phase (Sec. 2 values re-verified at
completion; see the completion response).

## 39. Final recommendation

1. Freeze this phase as the D3 adjudication record (commit/tag only under
   an explicit user instruction, as for previous checkpoints).
2. Keep the dual-branch barotropic implementation exactly as is; do not
   promote `derived_4_10` to any default or preferred status in code or
   docs without a separate reviewed implementation phase (and author
   confirmation remains valuable before any such step).
3. Proceed with Phase 1D-D (Candidate A on the clean systems) unchanged —
   it is independent of D3 by construction and must remain so.
4. If author contact is ever authorised, use the Sec. 37 courtesy question
   (now backed by a complete derivation), explicitly separating the
   general-derivation question from the Fig.-3 reproduction.
5. Any future barotropic scientific analysis should cite this report for
   the equation-level status of (4.15) while continuing to report both
   branches wherever comparison with the published record is claimed.
