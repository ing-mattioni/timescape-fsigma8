# Phase 1D-C — Compliance and scientific audit (read-only)

Date (UTC): 2026-07-18

Audited work: the Phase 1D-C observable-closure audit — deliverables
`reports/phase1d_c_observable_closure_audit.md` ("the report") and
`reports/phase1d_c_closure_inventory.json` ("the JSON") — against the full
Phase 1D-C implementation prompt. This audit is read-only: it created only
this file, corrected nothing, and did not stage, commit, tag, push, or
contact authors. Independent re-checks were executed in the ignored session
scratchpad (`phase1dc_audit_d3_recheck.py`) without modifying or
overwriting any Phase 1D-C scratch result.

Evidence provenance is separated throughout as: **[D]** = found in the
Phase 1D-C deliverables; **[A]** = independently reproduced or directly
re-read during this audit; **[C]** = asserted only in the Phase 1D-C
completion response. No conclusion below rests on [C] alone.

---

## 1. Required repository state — verified

All eleven checks executed before anything else; all passed [A]:

| # | check | result |
|---|---|---|
| 1 | branch / HEAD | `phase-1d-c-observable-closure-audit` / `93d956d0020f0edec34a44cd9d19f30c085aecc7` ✓ |
| 2 | base tag `phase-1d-b-growth-pipeline-v1` | resolves to `93d956d…` = HEAD ✓ |
| 3 | earlier frozen tags | all six ancestors of HEAD ✓ |
| 4 | untracked files | exactly `reports/phase1d_c_observable_closure_audit.md`, `reports/phase1d_c_closure_inventory.json` ✓ |
| 5 | tracked modifications | none (`git status --porcelain -uall` shows only the two `??` lines) ✓ |
| 6 | staged | nothing (`git diff --cached --name-only` empty) ✓ |
| 7 | 1D-C commit/tag | none (`git tag -l 'phase-1d-c*'` empty; HEAD is the 1D-B commit) ✓ |
| 8 | branch not pushed | `git ls-remote origin refs/heads/phase-1d-c-observable-closure-audit` empty ✓ |
| 9 | upstream | `590c6fd5332acb15f5683ebf392a0d7ce54983c5`, clean ✓ |
| 10 | notebook SHA-256 | `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a` ✓ |
| 11 | `git diff --check` | clean ✓ |

## 2. Audit inputs read

Read for this audit: both 1D-C deliverables in full (all 36 report
sections; every JSON object — programmatic walk over the complete
structure) [A]; the full Phase 1D-C implementation prompt [A];
`reports/phase1d_a_growth_observable_audit.md` and
`reports/phase1d_a_observable_inventory.json` in full (read during this
session) [A]; `reports/phase1d_b_growth_pipeline_validation.md` and
`reports/phase1d_b_compliance_audit.md` (read in full earlier in this
project; key cited facts spot-re-verified this audit: the 1D-B verdict
line `READY_AFTER_NON_SCIENTIFIC_CLEANUP` at line 928, one-factor table,
independent-root corroboration) [A]; the 1D-C evidence base in the ignored
scratchpad: source PDFs and hashes, rendered page images (21 DBE + 20 BDE
+ 9 GM pages present, counted), extracted full texts, and
`phase1dc_d3_symbolic.py` [A]. The completion response was used only as a
claims list to audit, never as evidence.

## 3. Deliverable-scope audit — COMPLETE

- Exactly two tracked deliverables created; no other tracked file touched:
  `git status --porcelain -uall` shows only the two `??` entries and
  `git diff`/`git diff --cached` are empty, so no tracked source, test,
  report, artifact, README.md, or CLAUDE.md changed [A].
- Implementation search: the complete repository diff vs HEAD is empty;
  the only new repository content is two non-executable report files
  (Markdown + JSON). Neither contains executable code: the report contains
  equations, labels, and design prose only (checked; the only fenced
  blocks are equations/text) [A]. Therefore no spectrum reader,
  transfer-function interface, CAMB/CLASS wrapper, sigma_R/sigma_8/
  anchored-sigma8/f-sigma-8 implementation, continuous-k solver,
  k interpolation, top-hat integrator, RSD/Kaiser mapping, bias model,
  AP conversion, data loader, covariance/likelihood/fitting code, or
  public API placeholder exists — **COMPLETE**.
- Auxiliary tooling (pdfminer.six, pypdfium2, sympy) was installed into a
  scratchpad-only `--target` directory; independently corroborated: the
  pre-install probe `import sympy` **failed** under `.venv` (visible in the
  session transcript) and all Phase 1D-C scripts ran with
  `PYTHONPATH` pointing at the scratchpad `pylibs` [A]. `.venv`/`.venv311`
  behaviour unchanged (both suites still pass with the frozen versions,
  Sec. 15 below).
- Equations/pseudocode inside the reports: allowed by the prompt;
  correctly confined there — **COMPLETE**.

## 4. Report-structure and JSON-schema audit

- Markdown: exactly **36** top-level `##` sections; titles and order match
  the 36 required prompt sections one-for-one (listing reproduced during
  this audit) [A] — **COMPLETE**.
- JSON parses; **35** top-level keys present as claimed [A] — COMPLETE.
- Required inventory categories: all present **except** that
  "unresolved dependencies" has **no dedicated category**; its content is
  real but distributed across `observable_chain.edges[].blockers`,
  `candidate_readiness.*`, `d3_investigation`, and `rsd_links`
  — **PARTIAL** (correction B-3).
- Conclusion objects: 13 conclusion-like objects (carrying
  `classification` + `source`) were found by an extended matcher that also
  catches keys named `conclusion` (which the deliverable's own
  `*_conclusion` validator would miss). **12 of 13** carry exactly the
  seven required fields. The exception is
  `spectrum_input_strategies.gm_own_envisaged_route`, a verbatim-quote
  record carrying `classification: VERIFIED_FROM_PRIMARY_SOURCE` with only
  `quote` and `source` — compliant with the deliverable's declared
  schema_note (its key does not end in `_conclusion`) but not with the
  prompt's stricter "every conclusion object" reading — **PARTIAL**
  (correction B-4) [A].
- Classification vocabulary: every `classification` string anywhere in the
  JSON belongs to the allowed ten-value set (programmatic walk; zero
  violations) [A] — **COMPLETE**. No conclusion combines evidence levels:
  primary classifications are single-valued with qualifications confined
  to `assumptions`/`convention_dependencies` (spot-checked all 13) —
  COMPLETE.
- Referenced files: all five internally referenced report files exist [A].
  The report contains no intra-document anchors; file references resolve —
  COMPLETE.
- Hash/identifier agreement report↔JSON: all seven identifiers (GM, W09,
  DBE, BDE hashes; HEAD; upstream; notebook) present and identical in both
  deliverables (programmatic check) [A] — **COMPLETE**.
- Prose-only / JSON-only conclusions: candidate verdicts, blockers, seven
  author questions, six theory questions, 20 API fields, 11 rejection
  rules, and the next-phase recommendation were compared item-by-item
  between deliverables — consistent, with two presentation gaps:
  (i) the Sec. 25 propagation table cell "background preset → mapped δ_m:
  no (mapping pure)" reads as if mapped δ_m were preset-independent,
  while the JSON says preset affects "all_downstream" — the intended
  meaning (conversion *factor* preset-invariant; *values* follow Δ_d) is
  ambiguous in the MD cell — **PARTIAL** (correction B-5);
  (ii) the relation between the inherited scenario dimension
  `initial_spectrum_model` (Sec. 26) and the API field
  `spectrum_input_kind` (Sec. 27) is not stated (C-list).

## 5. Primary-source provenance audit — COMPLETE (one page-cite error)

All hashes re-computed from the surviving scratch/tool-results files this
audit [A]; all match the values recorded in both deliverables:

| source | identity | file | SHA-256 (recomputed) | pages | method | read as |
|---|---|---|---|---|---|---|
| [GM] | arXiv:2511.17160v2, JCAP 02 (2026) 066 | scratchpad `gm_2511.17160v2.pdf` | `856bd78d…20dd` ✓ (bit-identical to frozen 1D-A hash) | 46+ | pdfminer full-text + pypdfium2 page renders | text + rendered pages |
| [W09] | arXiv:0909.0749, PRD 80 (2009) 123512 | scratchpad `w09_0909.0749.pdf` | `e37321e9…a8aa` ✓ (matches 1D-A) | — | pdfminer full-text (+ ar5iv HTML) | text |
| [DBE92] | ApJ 395 (1992) 54–74, DOI 10.1086/171629 | tool-results `webfetch-1784317200106-dxrzyk.pdf` | `3a082920…f20` ✓ | 21 (renders counted: 21) | pypdfium2 renders, visual reading | **rendered page images** |
| [BDE92] | ApJ 395 (1992) 34–53, DOI 10.1086/171628 | tool-results `webfetch-1784318228368-80ahvl.pdf` | `eaa273fa…b6c` ✓ | 20 (renders: 20) | same | **rendered page images** |
| [PW] | arXiv:0808.0003v2, MNRAS 393 (2009) 297 | frozen 1D-A record | — | — | frozen full-text inspection | inherited |
| HBW20 / NW15 | arXiv:1908.11508 / 1410.3470 | web fetches | — | — | abstract pages | **abstract only** (so recorded) |
| CAMB / CLASS | official readthedocs `results` / official `explanatory.ini` | web fetches | — | — | documentation pages | text |

- Image-only scans were inspected **visually from rendered pages** (300
  dpi), not via OCR or metadata — confirmed: the ADS PDFs have no text
  layer (WebFetch reported JBIG2/JPX image-only), and the deliverables'
  equation transcriptions correspond to the rendered images re-examined in
  this audit [A].
- Sign-critical legibility record for the scans (re-examined renders):
  DBE scan p. 5 = journal p. 58, Eqs. (26)–(34): all coefficients,
  overdots, and the script-𝒟/𝒵 distinction clearly legible; scan p. 6 =
  p. 59, Eqs. (35)–(45); scan p. 7 = journal p. 60, Eqs. (46)–(55): the
  **minus sign inside `3(w_{(i)} − c²_{s(i)})H`** in (49) and (55), the
  subscript `(i)` placements, the `Ψ` vs `V` distinction, and the primes/
  overdots are unambiguous at the rendered resolution; BDE scan p. 15 =
  journal p. 48, Eqs. (119)–(120): the `−k a ε_m(η) Y_α^{(0)}`
  coefficient, stroke-derivative subscripts, and the `V_C` vector-harmonic
  term are unambiguous. No sign-critical symbol needed to be guessed; no
  visually ambiguous equation was relied on [A].
- **One citation error found [A]:** the Mészáros-inapplicability quote
  ("…the Mészáros approximation should not be applicable in the timescape
  framework") is cited as "[GM] p. 24" in report Sec. 13 and in JSON
  `a1_a6_matrix.meszaros.physical_applicability.source`. Independent
  re-location this audit (pypdfium2 per-page text + printed footer): the
  quote is on **PDF page 26, printed footer "– 25 –"**, i.e. printed
  page 25 — the cite is off by one → **INCORRECT (page pinpoint only)**;
  the quote itself is verbatim-correct and the
  VERIFIED_FROM_PRIMARY_SOURCE classification stands (correction B-1).
  All other page cites re-checked are correct: comoving scale-independence
  = printed p. 19 ✓; (2.22) = printed p. 9 ✓; (4.5)–(4.18) = printed
  pp. 16–17 ✓; "too fast"/linear-departure = printed p. 44 (conclusions,
  cited without page) ✓; envisaged-BAO route = printed p. 45 (cited as
  conclusions) ✓ [A].
- Failed/partial accesses (ADS abstract page, native arXiv HTML, DOI
  redirect) are recorded honestly in the JSON with
  `content_actually_inspected: false/"partial"` — COMPLETE.

## 6. D3 source audit — the core scientific check

Independently reconstructed from the rendered pages during this audit [A]
(equation numbering as printed):

- **DBE (32)** (p. 58): `𝒟̇_a − 3Hw𝒟_a + (1+w)𝒵_a = 3a(1+w)H(F_a+Π_a)
  − a(1+w)⁽³⁾∇_a⁽³⁾∇^bΨ_b` — total fluid; self-coupling `+3Hw`; c_s²
  absent from it (enters via (33)/(34)).
- **DBE (46)** (p. 60): component equation in the total matter rest frame
  (`u^a = u_N^a`, stated at § 3.2 opening, p. 59): self-coupling
  `+3Hw_{(i)}`; `c²_{s(i)}` appears only inside `F_a^{(i)}` and the
  interaction terms.
- **DBE (49)/(55)** (p. 60): the "useful form" (55 = no interactions),
  obtained by substituting the momentum equations (29)+(43)/(54):
  self-coupling `+3(w_{(i)} − c²_{s(i)})H`. Frame: total matter rest
  frame. Entropy terms `𝓔`, `𝓔^{(i)}` explicit; zero for barotropic
  components.
- **BDE (119)–(120)** (p. 48): `𝒟_α = aε_m|α − 3a′(1+w)V_{Cα}
  = −k a ε_m(η)Y_α^{(0)} − 3a′(1+w)V_C(η)Y_α^{(1)}`.
- **GM (2.22)** (p. 9): `Δ̇^{(i)} − w_{(i)}ΘΔ^{(i)} + (1+w_{(i)})𝒵
  − aΘ(1+w_{(i)})F^{(i)} + a(1+w_{(i)})⁽³⁾ΔV^{(i)} ≃ 0`, generic observer
  frame n^µ, citing [50].
- **GM (4.10)** (p. 16): dust frame, frequency space:
  `Δ̇^{(eff)} − w_{(eff)}ΘΔ^{(eff)} + (1+w_{(eff)})𝒵 + Θ𝒫̃^{(eff)}
  − (k²/a)Ṽ^{(eff)} ≃ 0`.
- **GM (4.13)** (p. 17): `𝒫̃^{(eff)} = c²_{s(eff)}Δ^{(eff)}` ("in any
  observer frame n^µ"; c² as ∂p/∂ρ or ṗ/ρ̇).
- **GM (4.15)** as printed (p. 17):
  `Δ̇^{(eff)} − (w_{(eff)} + c²_{s(eff)})ΘΔ^{(eff)} + (1+w_{(eff)})𝒵
  − (k²/a)Ṽ^{(eff)} ≃ 0`.

Convention audit (per element): metric/derivative conventions shared
(Ellis-school; overdot = covariant derivative along the congruence;
`Θ = 3H`; continuity `μ̇ = −3H(μ+p)`); density variables identical
constructions (DBE `𝒟_a^{(i)}` ↔ GM `D_µ^{(i)}`; scalarisation by
`a D^µ`); expansion gradient `𝒵_a = aZ_a` ↔ GM `Z_µ = aD_µΘ`;
`c_s² = ṗ/μ̇` in both (DBE p. 58 verbatim; GM (4.13)); perfect-fluid
`Ψ_a^{(i)} = V_a^{(i)}` with `F` defined identically after `Θ = 3H`;
Laplacian sign irrelevant to the Θ-self-coupling term; harmonic
decomposition enters only via GM footnote 8 (and BDE's Y-harmonics for
(120)). Symbol-mapping table: **present in the JSON**
(`d3_investigation.notation_map`) and re-verified element-by-element
against the renders [A]. The prompt's four-column chain
(DBE/BDE → GM general frame → GM dust frame → Phase 1C state variables)
is captured across `notation_map` + `equations_inspected` + the frozen
1C-A matrix labels; a single explicit four-column table is not printed as
one object (C-list improvement, content complete).

The six Phase 1D-C claims, audited independently:

| claim | verdict |
|---|---|
| 1. GM (2.22) is a faithful scalarisation of DBE (46) | **VERIFIED** for a perfect-fluid, non-interacting component: term-by-term match (self-coupling `w_iΘ`; `aΘ(1+w_i)F^{(i)}` ↔ `3aH(1+w_i)F^{(i)}`; tilt-Laplacian term; DBE's interaction/heat-flux terms have no GM counterpart and GM's system is explicitly non-interacting) [A]. Note DBE (46) is total-frame while GM (2.22) is stated for generic n^µ — a scope generalisation GM make without derivation shown; this is part of the residual gap, correctly reflected in 1D-C. |
| 2. the original barotropic reduction contains `(w − c_s²)Θ` | **VERIFIED**: DBE (49)/(55) as printed; independently re-derived symbolically from (46)+(54) with entropy terms kept symbolic and zeroed at the end (audit re-run, residual 0) [A]. |
| 3. no `(w + c_s²)Θ` structure appears in the inspected original source | **VERIFIED within the inspected scope**, which must be stated exactly: DBE scan pp. 1, 5, 6, 7 (= journal pp. 54, 58, 59, 60) and BDE pp. 34, 45, 47, 48. Journal pp. 55–57 and 61–74 of DBE and the remaining BDE pages were **not** searched. The deliverables scope this correctly everywhere except one sentence (Sec. 36 "nowhere produces the printed one" — correction B-2). |
| 4. `derived_4_10` follows from the verified chain | **VERIFIED**: (4.10)+(4.13) ⇒ `(w−c_s²)Θ` re-derived from the audit's own fresh transcription (residual 0); matches frozen 1C-A. |
| 5. printed GM (4.15) has no source counterpart | **VERIFIED within the inspected scope** (same scope caveat as claim 3); additionally the audit re-confirmed printed−derived = `+2c_s²ΘΔ^{(eff)}` exactly. |
| 6. BDE (119)–(120) verify the Bardeen/comoving-density attribution | **VERIFIED** — see Sec. 9 below. |

## 7. Missing frame-transformation audit

Why D3 remains unresolved despite the new evidence — audited
independently. The still-missing transformations between DBE (46)/(54)
(total-matter frame) and the Phase 1C dust-frame barotropic system:

1. **frame change** total energy frame `u_N` → dust energy frame `u_d`:
   DBE (27) gives the density-gradient transformation law
   (`^N𝒟^{(i)} = 𝒟^{(i)} − 3Ha(1+w_{(i)})V^{(i)} + (a/μ_{(i)})ε_{(i)}V^{(i)}`);
   differentiating it injects `V̇^{(i)}`, whose evolution ((47)/(54))
   itself contains `c²_{s(i)}μ_i𝒟^{(i)}` pieces — so the frame change can
   in principle reshuffle `c_s²Δ`-terms between the density row and the
   tilt row; this is exactly the reason a structural match is not yet an
   adjudication [A];
2. the multifluid heat-flux/acceleration bookkeeping (`Ψ` vs `V`; GM's
   dust-geodesic relation `𝒫 + aF = 0` has no printed DBE counterpart in
   the inspected pages);
3. the pressure-gradient variable chain (DBE `Y_a`/(48) ↔ GM `𝒫^{(i)}`
   normalisation);
4. tilt rescaling `Ṽ = (1+w)V` (validated equivalence at 1C-B2 — not a
   gap);
5. harmonic scalarisation (commutation of `aD^µ` with the evolution —
   standard at linear order; GM perform it; not re-derived from DBE).

**Exact symbolic derivation required to close the gap:** apply `d/dt`
along the dust congruence to DBE (27) for the effective component; insert
DBE (46) (total frame) and DBE (54) for `Ψ̇^{(i)}`; use the two-fluid
identifications (dust + effective, dust geodesic, total-frame tilt
expressed via the effective tilt); scalarise with `aD^µ`; impose the
barotropic closure; and compare the resulting dust-frame `Δ̇^{(eff)}`
self-coupling coefficient with `(w ± c_s²)Θ`. Status of the missing step:
**partly not-written-down and partly dependent on uninspected material**
(DBE § 2.2 definitions on journal pp. 56–57 were not inspected); it is
plausibly derivable from already-inspected equations plus those
definitions; it is **unlikely but not impossible** that it changes the
sign conclusion — which is precisely why Phase 1D-C's refusal to
adjudicate is correct.

**Independent D3 status (this audit):**
`STRUCTURALLY_FAVOURS_DERIVED_4_10_BUT_UNRESOLVED`.

Neither deliverable calls `derived_4_10` canonical, correct, selected,
preferred, intended, physical, or a default — verified by reading every
D3 passage; the strongest wording used is "structurally supports/
structurally corroborated", with the mandatory dual-branch statement
repeated in report Secs. 3, 24, 36 and JSON
`d3_investigation.d3_conclusion.implementation_consequence` [A] —
**COMPLETE**.

## 8. Symbolic-check audit — COMPLETE

`phase1dc_d3_symbolic.py` located in the scratchpad (3,430 bytes, intact)
[A]. For each check: inputs are the visually transcribed GM (4.10),
(4.13), printed (4.15), DBE (46) (F-term only, since the tilt-Laplacian
term carries no `𝒟^{(i)}` coupling), and DBE (54); substitutions:
`𝒫̃ = c_s²Δ`, `h_i = (1+w_i)μ_i`, entropy terms zero; expected residuals
0/0/0/nonzero; actual: 0/0/0/nonzero (original PASS transcript; JSON
`d3_investigation.symbolic_checks`).

Audit re-run [A]: an **independently re-encoded** version
(`phase1dc_audit_d3_recheck.py`, new file; originals untouched) with
different symbol names, entropy/interaction terms kept symbolic and
zeroed only at the end, and the total-fluid `c_s²`-term retained.
Results: residuals 0, 0, 0; the `(w_i + c²_{s,i})` combination does not
arise; **additionally verified that the total-fluid `c_s²μ𝒟` term never
enters the component self-coupling coefficient** (`.has(ct2) → False`).
All four checks CONFIRMED.

Honest limitation, stated as required: a zero residual validates the
*encoded* equations. The source-to-symbol transcription was **separately
verified** — the audit re-read the rendered pages (Sec. 6) and re-encoded
the equations from them rather than from the 1D-C script; the two
encodings agree. The dust-frame vs total-frame distinction is *assumed
away* in check 3 only in the sense that check 3 operates entirely inside
DBE's own frame (a self-consistency check of (46)+(54)→(55)); no check
claims to perform the frame transformation — consistent with the
deliverables' own caveats — COMPLETE.

## 9. Bardeen-attribution audit — upgrade CONFIRMED

From the re-read render of BDE p. 48 (§ 5.2.3, Eqs. 119–120) [A]:

- Variable identified: the CGI comoving fractional density gradient
  `𝒟_α` (Ellis–Bruni), expanded to first order in Bardeen's notation.
- The scalar-harmonic coefficient of `𝒟_α` is `−k a ε_m(η)` — `ε_m` is
  Bardeen's gauge-invariant **matter-rest-frame (comoving) density
  contrast**; the additional term `−3a′(1+w)V_C(η)Y_α^{(1)}` is a
  **vector-harmonic** contribution, absent in the irrotational scalar
  sector.
- Relation to the project's `delta_m`: `𝒟_α` is the *gradient*; the
  project's scalar `Δ = aD^α𝒟_α` acquires the additional harmonic
  divergence factor, reproducing exactly the frozen chain
  `Δ_k = −k²(δ_m)_k` — i.e. a Laplacian/k² factor **remains between the
  gradient variable and the contrast, and the frozen 1D-A mapping already
  accounts for it**; BDE (119)–(120) verify the *identification of the
  underlying contrast with Bardeen's ε_m*, which is precisely what the
  1D-A attribution item needed. Scale-factor and sign bookkeeping in
  (120) (the `−k a` factor, conformal-time `a(η)`) affect the
  coefficient, not the identification.
- Scope: BDE treat a single (possibly imperfect) fluid here — the
  attribution applies to the single-fluid/dust contrast; the multifluid
  extension is asserted by DBE92's abstract ("equivalent to those of
  Bardeen and of Kodama and Sasaki") — both facts are recorded as such in
  the deliverables.
- The attribution is **exact at first order in the scalar sector**, not
  merely analogous.

Verdict on the 1D-C upgrade (`UNRESOLVED_EXTERNAL_DEPENDENCY` →
`VERIFIED_FROM_PRIMARY_SOURCE`): **COMPLETE / justified**. The upgrade is
correctly reported as an upgrade (report Secs. 3, 24; JSON
`proposed_evidence_upgrades_reported_not_silently_adopted`), does not
touch frozen code, and changes an attribution footnote only.

## 10. Dressed-geometry audit — verdict wording verified

The three [W09] statements were re-verified verbatim against the locally
extracted W09 full text during the 1D-C session (grep hits for "not an
exact solution", "spherically symmetric but not homogeneous",
"conformally match radial null geodesics", "not the locally measured")
and their context re-read [A/D]. Logical-scope audit of the four distinct
claims:

1. the displayed dressed metric (W09 (26)) is unsuitable as a global
   homogeneous Fourier background — **established** by the verbatim
   inhomogeneity statement;
2. no global dressed spatial map exists anywhere in Timescape —
   **not established and not claimed**: the report explicitly says "the
   impossibility-in-principle of any alternative construction is not
   claimed" (Sec. 8, answer 3) and files the construction as new
   theoretical work;
3. approximate local/wall constructions — **not excluded**: the JSON
   records wall Fourier labels as "undefined beyond finite-infinity
   regions", leaving local constructions open;
4. no observationally useful published map — asserted **only for the
   searched scope** (W09 full text; GM full text; NW15 and HBW20
   abstracts; PW frozen full text), which the deliverables state.

The searched vocabulary (dressed spatial coordinates, finite infinity,
wall geometry, radial coordinates, conformal matching, BAO scale,
statistical homogeneity, Fourier/harmonic decomposition) is reflected in
the report's Sec. 8 bullet list; NW15/HBW20 were abstract-level only and
are so recorded — the negative conclusion for those two sources is
correspondingly abstract-level (acceptable; noted).

**Independent map status (this audit):**
`NO_MAP_FOUND_IN_SEARCHED_SOURCES` — matching the deliverables'
formulation, which correctly prefers "not found in the inspected
sources" over "does not exist" everywhere except no instance found to
violate this in Secs. 7–9 [A]. COMPLETE.

## 11. Coordinate/Jacobian audit — COMPLETE

Re-derived independently [A]: with `x_new = λ x_old`,
`k_new = k_old/λ`; `δ_{k,new}(k_new) = λ³δ_{k,old}(λk_new)` (volume
element `d³x_new = λ³d³x_old` — implicit in the report's amplitude line;
C-list note); `δ_D → λ³δ_D`; `P_new(k) = λ³P_old(λk)` (value and units
change); `Δ²_new(k) = Δ²_old(λk)` (argument only); `kR` invariant iff `R`
co-transformed; `σ_R` invariant under the matched transformation. All
five report statements reproduce exactly. The report distinguishes:
constant isotropic rescaling (Sec. 9), time-dependent rescaling
(Sec. 8 answer 5 and JSON candidate-mapping 2), radial-only light-cone
mapping (Sec. 8), and the nonhomogeneous case where global Fourier modes
are undefined (Sec. 8 answer 1). The passive-relabelling vs
physical-frame-change wording is implicit rather than named (C-list). No
missing Jacobian, power, inverse factor, or unit factor found.

## 12. Spectrum-carrier and normalisation audit — COMPLETE

All five carriers/strategies audited against the deliverables' tables
[D/A]: classifications and incompatibilities are consistent with the
frozen 1D-A classifications and with the newly fetched provider
documentation. The three upstream modes are never treated as an ensemble,
continuous spectrum, quadrature grid, transfer function, or σ_8
normalisation — verified across report Secs. 6, 10, 11, 16, 17, 27
(rules 1–2) and JSON (`three_modes_rule`,
`normalization_strategies.upstream…`, api rules) [A]. CAMB/CLASS are
described via their **configurable** output conventions
(`hubble_units`/`k_hunit`; `P_k_max_h/Mpc` vs `P_k_max_1/Mpc`; `A_s` vs
`sigma8/S8` shooting; linear vs halofit/hmcode) with explicit-metadata
requirements rather than a single assumed convention — exactly as the
audit instruction requires. Gauge/species metadata: the JSON records
CAMB transfer entries (Transfer_cdm/b/tot) and CLASS `dTk` "for each
species" plus the Bardeen-potential normalisation note; the future-schema
requirement lists units/h/frame/linear-only/provenance/z-grid. A
species-selection field (e.g. total vs CDM+baryon) is not yet an explicit
API field — noted as a C-list improvement for the future schema (it is
implied by "schema and metadata validation" in Tier 2).

## 13. A1–A6 identity audit — COMPLETE

Independently re-derived [A]: under A1–A6 with
`δ(k,z) = D(z;z_ref)δ(k,z_ref)` for every k in the kernel support,
`σ_R²(z) = D²σ_R²(z_ref)` for **every** R and in **every** frame — hence
`σ_8(z) = D σ_8(z_ref)` and `dσ_8/d ln a = f D σ_8(z_ref)` with f and the
derivative in the same coordinate. Per system: Mészáros — k-free operator
(GM (4.27)) + IC-mixture condition; comoving — GM p. 19 (cite verified
correct this audit); A5 — frozen 1D-B root-refined evidence (zero dust
crossings, whole-domain validity) [D, frozen]; reference dependence and
the bare/dressed distinction (factor 1.02475–1.084156) explicit;
**the key 1D-C derivation — that a scalar σ_8 anchor propagates without
the spectrum shape and without the spatial k map under strict A2 — is
mathematically correct** (the kernel cancels identically; verified in
three lines above). What it does and does not predict is stated
correctly: it is an anchored evolution of an imported observational
number, not a σ_8 prediction, and collapses when A2 is relaxed. The
report never labels it observational RSD fσ8; the name tokens `fsigma8`,
`f_sigma8`, `RSD` are explicitly forbidden for these quantities (report
Sec. 14; JSON `anchored_diagnostic_names`) [A]. COMPLETE.

## 14. Candidate audits

**A — `GO_ONLY_AS_CONDITIONAL_DIAGNOSTIC`: CONFIRMED.** Implementable
without a spatial map, spectrum, transfer function, k integral, or RSD
mapping (Sec. 13 above; only frozen-pipeline D(z), f(z), and a scalar
anchor are needed). The name semantics distinguish it from a σ_8
prediction, model normalisation, theoretical fσ8, observational fσ8, and
RSD prediction (report Secs. 14, 20-ranking). Comoving-primary /
Mészáros-baseline is supported by the verified GM quotes (p. 19; p. 25;
conclusions). The Mészáros caveat is specified at output level
("mandatory caveat on every Mészáros anchored output" — JSON), not
documentation-only — satisfying the audit requirement. Audit decision
among the four options: **implement only behind an explicitly conditional
diagnostic API** (= the 1D-C verdict). The naming risk is adequately
mitigated by the token bans + caveat blocks; report-only retention would
forgo the only legitimately available observational-units diagnostic.

**B — `BLOCKED_BY_EXTERNAL_INPUT`: CONFIRMED with precision note.** The
blockers beyond the missing spectrum are real: frame-declaration validity
(itself a PROVISIONAL_MODEL_IMPORT — named inside the verdict cell),
k units, h, radius convention, normalisation. Among the eight allowed
verdicts, `BLOCKED_BY_EXTERNAL_INPUT` is the most precise available
label, and the deliverables carry the frame-import caveat prominently;
sufficiently precise. Secondary blockers correctly listed.

**C — `BLOCKED_BY_LINEARITY_OR_K_DOMAIN`: CONFIRMED.** All nine stated
barotropic blockers verified present (report Secs. 16–17; JSON
`barotropic_requirements`, `high_k_and_linearity`). The finite-integrand
claim is correct and correctly separated from k-integral convergence,
dominated convergence, cutoff dependence, and physical linearity (five
distinct notions, each named). No universal high-k cutoff proposed
anywhere [A].

**D — `BLOCKED_BY_MISSING_SPATIAL_MAP`: CONFIRMED.** Secondary blockers
(spectrum/anchor, h) listed; smoothing radius appears via Secs. 10/19;
a galaxy/matter **species definition** is not explicitly listed among D's
blockers (it appears only in the Tier-2/bias context) — C-list addition.

**E — `BLOCKED_BY_MISSING_RSD_MAPPING`: CONFIRMED.** All twelve links
separately identified and classified (JSON `rsd_links` 1–12; report
Sec. 20), including density growth, expansion perturbation, peculiar
velocity, galaxy velocity, both biases, the Jacobian, line-of-sight,
dressed clock/H factors, AP/fiducial, and window/estimator. Background
distance/BAO fits are explicitly barred from being read as RSD evidence
(`rsd_source_supply.rule`) [A].

## 15. RSD-source search audit — COMPLETE

Per-source supply matrix re-checked against what was actually read [A]:
W09 (full text): background expansion, radial null propagation,
distance–redshift — yes; everything perturbative — no. GM (full text):
background + CGI perturbation dynamics; no redshift-space, velocity
observable, bias, AP, or estimator content; fσ8 only as future work
(verbatim passages verified). NW15 (abstract): CMB via matched FLRW
codes; no spatial Fourier map (abstract-scope conclusion). HBW20
(abstract): background AP/BAO scaling accuracy; no perturbative RSD
(abstract-scope). PW (frozen full text): the FLRW chain itself. Negative
conclusions are correctly limited to this inspected set; the JSON's
`content_actually_inspected` fields make the abstract-level scope
machine-readable. COMPLETE.

## 16. Linearity audit — COMPLETE

The five-level validity taxonomy is present and correctly ordered
(equations-linear ≠ converged ≠ amplitude-linear ≠ physically plausible ≠
observationally valid). The report explicitly refuses an
`|Delta_d| ≪ 1` criterion, with the correct k²-scaling reason
(re-checked: `Δ_d,k = −k²δ_m,k` makes any fixed `|Δ_d|` threshold
scale-dependent) [A]. `delta_m` amplitude assessment is correctly held
impossible without a statistical/physical normalisation, and the missing
information is named exactly (normalisation + frame scale assignment).
The mask design contains **no silent universal threshold**: thresholds
are required to be explicit with provenance. COMPLETE.

## 17. Dependency-graph audit — COMPLETE with one cell fix

All edges checked against the frozen 1D-B one-factor magnitudes and the
1D-A field inventory [A]. Correct and notable: tilt-form cancellation
(≤3e−14); growth-coordinate history-invariance with rate amplitude
1.025–1.084156; F7/frame/h cancellation inside the strict-A2 anchored
diagnostic (each verified — under A2 no kernel remains); D3
not-applicable for clean systems; signed D3 (−230.2 %) and F7
(rate-sign-flip) deltas labelled as convention spreads, never confidence
intervals (rule present in both deliverables). One presentation defect:
the MD cell "background preset → mapped δ_m: no (mapping pure)"
(ambiguous vs JSON "all_downstream") — correction B-5. No other missing
or overstated edge found.

## 18. Proposed-API audit — COMPLETE

All 20 fields carry explicit labels, applicability, and NO default
("default": "NONE" on every field; `FORBIDDEN_AS_A_SILENT_DEFAULT`
standing rule); explicit `not_applicable` where required (6 fields);
no canonical D3; no implicit h/frame/spectrum/anchor; no silent
volume-average→dressed mapping (the dressed frame is constructible only
as a blocked object); no `f_sigma8`/RSD label without a validated RSD
layer (rules 6–7; `rsd_interpretation` has **no affirmative value**);
no three-mode spectrum (rule 2); no D2 path (rule 11); no
pole-interpolation (rule 10). The 11 rejection rules cover exactly the
prompt's required rejection list [A]. `observable_target` distinguishes
the five required kinds (six labels including `per_mode_growth`).
Overclaim scan of proposed labels: none overclaims; the two
blocked-only labels (`observational_sigma8`, `rsd_fsigma8`) exist solely
so the rejection engine can name what it refuses — defensible, with a
C-list note to document that rationale prominently in any future
implementation.

## 19. Validation-blueprint audit — COMPLETE

All fifteen required error classes are covered and separated across
Tiers 1–5 + the error-separation list (mapping verified item-by-item)
[A]. Tier 5 is correctly blocked with its conditional test list.
Self-referential-test scan: one candidate found — Tier 3's "analytic
derivative identity" could degenerate into re-evaluating the
implementation formula; the blueprint's "to solver tolerance" implies an
independent numerical differentiation but does not say so explicitly —
C-list improvement (specify independent finite-difference comparison).
No other test merely restates its implementation.

## 20. Author-question audit — COMPLETE

All seven questions: scientifically necessary (each maps to a verified
open fork or missing derivation), not answered by the inspected sources
(re-checked: F3/F4/F7 remain genuinely ambiguous in [GM]; the spatial
map and RSD constructions are absent from the searched scope), neutrally
phrased, and notation-explicit. The D3 question states the discrepancy
and the DBE (49)/(55) evidence **without asserting an authors' error**
("Which sign is intended, and is (4.15) as printed the equation actually
used in the published figures?") — compliant. No contact was made [A].

## 21. Minimal-next-phase audit

1D-C recommends one Phase 1D-D = Candidate A plus a parallel pure-theory
D3 derivation. Audit assessment:

- Candidate A is **D3-safe**: it touches only the clean systems, where
  `d3_branch` must be passed as explicit `not_applicable`; no output can
  depend on the branch. Implementing A before D3 closes is therefore
  scientifically safe.
- The two activities have disjoint evidence bases, deliverables, and
  review criteria (implementation + tests vs derivation report), so they
  are **better decomposed into two separately reviewable phases**.
- Phase 1D-D (Candidate A) **should explicitly exclude** any barotropic
  API surface and any D3 input beyond the explicit `not_applicable`
  token, and ban the `fsigma8`/`RSD` name tokens at test level.

**Recommended decomposition (this audit):** Phase 1D-D-t — the formal D3
frame-mapping derivation (report-only deliverable; adjudicates or
formally fails to adjudicate D3); then Phase 1D-D — Candidate A behind
the conditional-diagnostic API with the exclusions above. Order rationale:
the theory step is small, independent, and retires the largest
equation-level ambiguity before any new public quantity ships; but since
Candidate A is D3-independent, executing them in the reverse order (or in
parallel as 1D-C proposed) is also defensible — the decomposition into
two reviewable units is the substantive recommendation.

## 22. Re-run reproducibility checks (exact commands and results)

All run read-only during this audit [A]:

| step | command | result |
|---|---|---|
| 1–3 | `python - <<json/schema walk>>` (.venv) | JSON parses; 13 conclusion-like objects; 12/13 with all 7 fields (see B-4); all classification strings in the allowed set |
| 4 | top-level key count | **35** ✓ (as claimed) |
| 5 | `grep -c "^## "` | **36** sections ✓; titles match required list |
| 6 | referenced-file existence | all resolve ✓ |
| 7 | `.venv\Scripts\python -m pytest -q` | **337 passed in 18.51s** — CPython 3.14.3, NumPy 2.5.1, SciPy 1.18.0; no warnings |
| 8 | `.venv311\Scripts\python -m pytest -q` | **337 passed in 14.87s** — CPython 3.11.9, NumPy 2.4.6, SciPy 1.17.1; no warnings |
| 9 | `git diff --check` | clean ✓ |
| 10 | `git status --porcelain -uall` | exactly the two `??` deliverables (plus, after this audit's creation, this report) |
| 11 | `git diff --cached --name-only` | empty ✓ |
| 12 | upstream `rev-parse` / notebook `sha256sum` | `590c6fd…` clean; `86d2534…` unchanged ✓ |

Additional audit-only reproductions: four source-hash recomputations
(all match); GM printed-page relocation of five key quotes (pypdfium2
per-page text + footer markers); independent symbolic re-encoding (all
four checks confirmed + one strengthening check). The pip-notice line
during earlier scratch installs is the only environmental output observed;
it does not affect the repository.

---

## A. Blocking defects before commit

**None.** No scientific, provenance, reproducibility, or scope defect was
found that invalidates a conclusion, classification, verdict, or the
evidence chain. The five findings below are citation-precision, wording-
scope, and schema-consistency items that do not change any scientific
content.

## B. Required corrections before commit (exact, minimal — NOT applied)

1. **Page cite "p. 24" → "p. 25"** for the Mészáros-inapplicability
   quote: report Sec. 13, first bullet ("[GM] p. 24:" → "[GM] p. 25:");
   JSON path `a1_a6_matrix.meszaros.physical_applicability.source`
   ("GM p. 24 verbatim" → "GM p. 25 verbatim"). (Verified: PDF page 26,
   printed footer "– 25 –".)
2. **Scope-limit one sentence** in report Sec. 36, D3 bullet: "…and
   nowhere produces the printed one" → "…and nowhere in the inspected
   pages produces the printed one" (matching the correctly scoped
   statements in Secs. 24 and the JSON).
3. **Add a dedicated `unresolved_dependencies` top-level key** to the
   JSON (consolidating the blockers already recorded in
   `observable_chain.edges[].blockers`, `candidate_readiness`,
   `d3_investigation`, and `rsd_links`), to satisfy the prompt's
   "contain at least … unresolved dependencies" category explicitly.
4. **Schema consistency for `spectrum_input_strategies.gm_own_envisaged_route`:**
   either add the five missing conclusion fields (assumptions,
   derivation_summary, convention_dependencies, implementation_consequence,
   evidence_needed_to_change_status) or rename `classification` to a
   non-reserved key (e.g. `verbatim_status`) so that no object carries a
   bare classification outside the declared conclusion schema.
5. **Clarify the Sec. 25 propagation-table cell** "background preset →
   mapped δ_m" from "no (mapping pure)" to wording such as "factor
   invariant; values follow Δ_d" (aligning the MD with the JSON's
   "all_downstream").

## C. Non-blocking improvements

*Documentation:* state the relationship between the inherited scenario
dimension `initial_spectrum_model` (Sec. 26) and the API field
`spectrum_input_kind` (Sec. 27); surface the abstract-only scope of the
NW15/HBW20 negative conclusions in report Sec. 20 prose (already
machine-readable in the JSON); note that DBE journal pp. 59 Eqs. (37)–(41)
were rendered and legible though uncited; print the four-column
DBE→GM-general→GM-dust→Phase-1C notation chain as a single table.
*Schema:* wrap `rsd_links` statuses in the full seven-field conclusion
form for uniformity; add a species/component-selection field (total vs
CDM+baryon) to the future spectrum-import schema; list species definition
among Candidate D's secondary blockers. *Architecture:* document why the
blocked-only `observable_target` labels exist (rejection-engine
addressability). *Future tests:* specify that Tier 3's derivative-identity
test uses independent numerical differentiation; make the volume-element
line of the Jacobian derivation explicit.

## D. D3 evidence verdict

**STRUCTURALLY_FAVOURS_DERIVED_4_10_BUT_UNRESOLVED.**

The remaining gap, exactly: DBE92's component equations (46)/(49)/(54)/
(55) are written in the total-matter rest frame, while GM's Sec. 4 system
lives in the dust energy frame (with the dust-geodesic relation
`𝒫 + aF = 0`); the total→dust frame transformation — whose derivative
injects tilt-evolution terms that can in principle reshuffle `c_s²Δ`
contributions between the density and tilt rows — has not been executed,
and DBE § 2.2's definitions (journal pp. 56–57) were not inspected. Until
that finite derivation (Sec. 21, Phase 1D-D-t) or author confirmation
closes it, the structural evidence (original source's own reduction gives
`(w − c_s²)Θ`; GM (2.22) matches DBE (46); printed (4.15) differs from
its own parents by exactly `+2c_s²ΘΔ`; no `(w + c_s²)` structure in the
inspected pages) favours `derived_4_10` without adjudicating it. Both
branches correctly remain mandatory in every deliverable.

## E. Dressed spatial-map verdict

**NO_MAP_FOUND_IN_SEARCHED_SOURCES.**

Searched scope, exactly: [W09] full text (dressed-geometry construction
Sec. II.4, Eqs. (22)–(27), verbatim statements re-verified); [GM] full
text (Sec. 5.1 dressing relations; footnote 8 volume-average harmonics;
conclusions); Nazer–Wiltshire 2015 and Heinesen–Blake–Wiltshire 2020 at
abstract level; Percival–White (frozen full text). Within that scope no
spatial Fourier-coordinate transformation from volume-average to dressed
observational coordinates exists; the dressed geometry is explicitly
inhomogeneous and light-cone-constructed. This audit confirms the
deliverables' formulation ("not found in the inspected sources"; the
in-principle impossibility is expressly not claimed), subject to the one
Sec. 36 wording fix (B-2) which concerns D3, not the map.

## F. Candidate readiness verdicts

| candidate | primary verdict (confirmed) | secondary blockers noted |
|---|---|---|
| A | **GO_ONLY_AS_CONDITIONAL_DIAGNOSTIC** | anchor import (A6); F3/F4 propagation; mandatory Mészáros caveat; mandatory naming rules |
| B | **BLOCKED_BY_EXTERNAL_INPUT** | frame-declaration import (the deeper issue, named in-cell); k/h/radius/normalisation metadata |
| C | **BLOCKED_BY_LINEARITY_OR_K_DOMAIN** | external spectrum; D3 dual-branch spread; [GM]'s own unphysicality assessment |
| D | **BLOCKED_BY_MISSING_SPATIAL_MAP** | spectrum/anchor; h; radius; (add: species definition — C-list) |
| E | **BLOCKED_BY_MISSING_RSD_MAPPING** | spatial map; normalisation; both biases; survey fiducial/AP |

## G. Recommended next-phase decomposition

Two separately reviewable phases (refining 1D-C's one-phase-plus-subtask):
**Phase 1D-D-t** — formal D3 frame-mapping derivation (report-only;
transforms DBE (46)+(54) into GM's dust-frame two-fluid system with every
sign tracked; adjudicates D3 or documents formal failure to adjudicate);
**Phase 1D-D** — Candidate A only, behind the conditional-diagnostic API,
with explicit exclusions: no barotropic API surface, `d3_branch` and
`wavenumber_convention` accepted only as explicit `not_applicable`,
`fsigma8`/`f_sigma8`/`RSD` tokens banned at test level, Mészáros caveat
attached to every output. Preferred order: 1D-D-t first (small,
independent, retires the largest ambiguity before a public quantity
ships); the reverse order is also safe because Candidate A is
D3-independent.

## H. Claims independently verified (reproduced or directly re-read)

1. All 11 repository/provenance preflight checks, including not-pushed
   (`ls-remote` empty) and no-1D-C-tag.
2. SHA-256 of all four source PDFs recomputed and matching (GM and W09
   additionally bit-identical to the frozen 1D-A hashes).
3. Rendered-page counts (21 DBE / 20 BDE / 9 GM) and legibility of every
   sign-critical symbol in DBE (46)/(49)/(55), BDE (119)–(120),
   GM (2.22)/(4.10)/(4.13)/(4.15) from the renders.
4. Printed-page locations of five key GM quotes via an independent
   extraction path (per-page text + footer markers) — exposing the one
   p. 24→p. 25 cite error and confirming p. 9, p. 16–17, p. 19,
   conclusions cites.
5. The D3 equation transcriptions and all four symbolic checks, re-run
   from a fresh independent encoding (residuals 0/0/0/nonzero), plus the
   strengthening check that the total-fluid c_s² term never enters the
   component self-coupling.
6. printed (4.15) − derived form = `+2c_s²ΘΔ^{(eff)}` exactly.
7. The Bardeen-attribution content of BDE (119)–(120) and its exact
   relation to the frozen `Δ_k = −k²δ_m,k` chain.
8. The A1–A6 identity and the kernel/frame/shape cancellation under
   strict A2 (three-line re-derivation).
9. The complete Jacobian set for a constant rescaling.
10. JSON parse, 35 keys, classification vocabulary, 36 sections/titles,
    hash agreement across deliverables, referenced-file existence.
11. Both test suites: 337 passed (3.14.3 / 18.51s) and 337 passed
    (3.11.9 / 14.87s).
12. That neither deliverable elevates `derived_4_10` beyond "structurally
    supported" and both retain the mandatory dual-branch rule.

## I. Claims not independently verified (and why)

1. CAMB/CLASS documentation details — recorded from the official pages
   fetched during Phase 1D-C; not re-fetched during this audit (read-only
   audit; the deliverables' claims match the fetched content preserved in
   the session record).
2. NW15 and HBW20 content beyond their abstracts — never inspected
   (correctly recorded as abstract-only in the deliverables; their
   negative RSD conclusions are accordingly abstract-scope).
3. [W09] equation numbering (22)–(27) — verified via the ar5iv rendition
   and phrase-level greps of the locally extracted text during 1D-C; the
   W09 pages were not rendered to images, so equation-number pinpoints
   rest on the HTML rendition plus text extraction rather than visual
   page reading (the verbatim statements themselves were grep-verified).
4. [PW] full-text conclusions — inherited from the frozen 1D-A
   inspection; not re-read this audit.
5. DBE journal pp. 55–57 and 61–74, and BDE pages other than 34/45/47/48
   — never inspected by 1D-C or this audit; all "absence" claims are
   scoped accordingly (see B-2 for the one sentence that was not).
6. The Kodama–Sasaki equivalence for the multifluid case — asserted by
   the DBE92 abstract only; the detailed KS-comparison sections of DBE92
   were not inspected.

## J. Commit readiness

**READY_AFTER_NON_SCIENTIFIC_CLEANUP**

No blocking defect exists; the Phase 1D-C conclusions, classifications,
verdicts, and evidence chains withstand independent verification. The
five B-list corrections (one off-by-one page cite, one scope-limiting
sentence, one missing JSON category, one schema-consistency fix, one
table-cell clarification) are documentation/schema items that do not
change any scientific statement and should be applied before commit. No
finding was repaired by this audit.
