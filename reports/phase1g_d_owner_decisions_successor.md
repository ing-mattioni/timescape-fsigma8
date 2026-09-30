# Phase 1G-D — owner decisions successor record

Record classification: `OWNER_DECISIONS_SUCCESSOR_RECORD`.
Parent checkpoint: `63ca316` (`main`, the merge of the Phase 1G audit pull
request), local branch `phase-1g-owner-decisions`. Date: 2026-09-30.
Machine-readable companion:
[`phase1g_d_owner_decisions_successor_inventory.json`](phase1g_d_owner_decisions_successor_inventory.json).

Cited as:
- [1G-D] = [`phase1g_d_separate_universe_growth.md`](phase1g_d_separate_universe_growth.md),
  its inventory and `scripts/phase1g_d_separate_universe_numerics.py` (frozen);
- [AUD] = [`phase1g_d_adversarial_audit.md`](phase1g_d_adversarial_audit.md)
  and its inventory (findings GD-F1 … GD-F10);
- [CONS] = [`phase1g_adversarial_audit_errata_successor.md`](phase1g_adversarial_audit_errata_successor.md)
  (errata E-1GD-1 … -8 are applied there);
- [ADD] = [`phase1g_status_additions_successor.md`](phase1g_status_additions_successor.md) (frozen);
- [1G-F] = [`phase1g_f_void_population.md`](phase1g_f_void_population.md);
- [WIN] = [`phase1g_windows_validation_record.md`](phase1g_windows_validation_record.md),
  the Windows validation and the final runs;
- [OD-N] = `scripts/phase1g_owner_decisions_numerics.py`, artifact
  `artifacts/independent/phase1g_owner_decisions.json`, key
  `results.GD_void_response`;
- [GM] arXiv:2511.17160v2; [W09] arXiv:0909.0749v2; [SvdW04]
  astro-ph/0311260. Source line numbers are those verified by [AUD].

The frozen [1G-D] report, inventory and script, [ADD], [AUD] and [CONS] are
**not edited**. No equation, initial condition, unit, sign convention,
normalisation of an implemented quantity, tolerance or status-token value
changes. Two token *comments* change where a ticked decision says so (Sec. 10).

## 1. Authorisation

The project owner's task statement of 2026-09-30 ("Phase 1G — Windows
validation, owner decisions for 1G-A/C/D/E, tags"), Sec. 0, gives these
approvals, verbatim:

1. "Create the local branch `phase-1g-owner-decisions` from `main` and commit there."
2. "Apply the owner decisions ticked `[x]` in Sec. 3, exactly as ticked. An unticked decision is **not** approved: leave it open and list it at the end."

Approvals 3–6 (local signed tags, push and pull request, merge, tag push) are
unticked and therefore not given. This record applies approval 2 to the
1G-D items of Sec. 3.

**Unticked, not applied** (listed again in Sec. 11): GD-OD1 "[ ] Keep the
[SvdW04] factor as an explicit additional assumption, and quote both ranges."
and "[ ] In either case, rebase the rationale comment of
`LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` on the "R8 < R_void partition"
argument. The value is unchanged."; GD-OD2 "[ ] Keep 10⁻², marked as outside
the tracker."; GD-OD6 "[ ] Wall-mode amplitude."

## 2. Decisions

| Id | Blocks the tag | Ticked option |
|---|---|---|
| GD-OD1 (GD-F1) | yes | Tracker-consistent primary seed; the [SvdW04]-factor values quoted as the alternative |
| GD-OD2 (GD-F2) | yes | f_vi restricted to the tracker's f_v(t_LS) |
| GD-OD3 (GD-F3) | yes | SU-mode identification `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` (S1); [GM] l. 620; headline and X_SU lower bound conditioned on S1 |
| GD-OD4 (GD-F4) | yes | Reword "[W09] internally inconsistent" |
| GD-OD5 (GD-F5) | yes | Correct the Mészáros/barotropic characterisation (report, inventory, token comment) |
| GD-OD6 (GD-F6) | no | δ_L = the total contrast at last scattering |
| GD-OD7 (GD-F7) | no | σ_LSS(R8) at [NW15]'s own radius in the new script; the "2.6–4.3" token comment updated |

GD-OD1, OD2, OD6 and OD7 act together on the same numbers. Sec. 3 gives the
recomputation with all four applied; Secs. 4–9 give each decision's text.

## 3. The void response with GD-OD1, OD2, OD6 and OD7 applied

**Inputs** (each a ticked decision; everything else is [1G-D]'s own formula,
imported unchanged from the frozen script):
- **seed radius** (GD-OD1, primary): `R_seed = R_void (f_vi/f_v0)^{1/3}/γ_w0`,
  R_void = 15/h Mpc ([W09] l. 277: 30 h⁻¹ Mpc diameter). The tracker's void
  domain is a fixed set of fluid elements whose comoving radius grows by
  `(f_v0/f_vi)^{1/3}` (and `γ_w0⁻¹` in photon-comoving units), not by the EdS
  shell-crossing factor 1.72. The [SvdW04] factor `R_seed = R_void/1.72` is
  the quoted alternative;
- **f_vi** (GD-OD2): the tracker's own void fraction at photon-normalised
  last scattering, `f_vi = f_v(t_LS)` with z = 1090 (a_LS = 1/1091, as
  [1G-D]): **9.471e−5** ([GM]; t_LS/t0 = 3.380e−5) and **5.073e−5** ([NW15];
  3.018e−5). The frozen f_vi = 10⁻⁴ and 10⁻² are [W09]'s range (l. 1815); the
  10⁻² branch is 100–200 times the tracker's value;
- **R8** (GD-OD7): each parameter set's own equal-mass radius, 12.570 Mpc
  ([GM]) and **12.226 Mpc** ([NW15]); the frozen script uses 12.57 for both;
- **δ_L** (GD-OD6): the total contrast of the region at last scattering. S2
  sets `ε = A_v δ_L`; the wall-mode amplitude at last scattering is then
  `δ_w(LS) = δ_L (1 − A_v f_vLS)/(1 − f_vLS)`, so that the region's contrast
  `(1 − f_vLS) δ_w(LS) + f_vLS ε` equals δ_L. Hence
  `D_SU(t0) = f_w0 D_wall(t0) (1 − A_v f_vLS)/(1 − f_vLS) + A_v a_LS f_v0`.

**Results** ([OD-N]; R* in h⁻¹ Mpc, dressed h):

| | [GM] primary | [NW15] primary | [GM] [SvdW04] factor | [NW15] [SvdW04] factor |
|---|---|---|---|---|
| R_seed (Mpc) | 0.757 | 0.810 | 11.94 | 14.30 |
| σ_s = σ_LSS(R_seed) | 3.40e−3 | 3.48e−3 | 9.29e−4 | 8.38e−4 |
| ν = −Φ⁻¹(f_vi) | 3.733 | 3.887 | 3.733 | 3.887 |
| A_v | **1169** | **1185** | 4274 | 4914 |
| A_v f_v(t_LS) | 0.111 | 0.060 | 0.405 | 0.249 |
| σ_LSS(R8), own radius | 8.982e−4 | 9.336e−4 | 8.982e−4 | 9.336e−4 |
| **A_v σ_LSS(R8)** | **1.050** | **1.106** | 3.839 | 4.588 |
| **X_SU** (δ_L total; GD-OD6) | **1.263** | **1.285** | 3.839 | 3.921 |
| X_SU with the frozen S2 (wall-mode amplitude) | 1.295 | 1.312 | 3.958 | 4.033 |
| R*(ε = 1) | 9.9 | 8.6 | 45.2 | 42.4 |
| R*(10% void-fraction fluctuation) | 32.5 | 38.5 | 104.0 | 121.1 |
| R*(10% density contrast) | **84.1** | **60.8** | 215.0 | 171.5 |

**Primary ranges:** A_v = 1169 / 1185; **A_v σ_LSS(R8) = 1.05–1.11**;
**X_SU = 1.26–1.28**; R*(ε = 1) = 9–10, R*(10% density) = 61–84 h⁻¹ Mpc.
**Alternative ([SvdW04] factor):** A_v σ_LSS(R8) = 3.8–4.6, X_SU = 3.8–3.9,
R*(10% density) = 172–215 h⁻¹ Mpc.

**Relation to the ticked text.** The tick quotes [AUD]'s ranges "A_v σ(R8)
1.05–1.5 and X_SU 1.30–1.63". Those are the tracker-consistent seed at [W09]'s
f_vi = 10⁻⁴ and 10⁻² with the frozen S2 normalisation ([AUD] Sec. 4.5 table).
[OD-N] reproduces all 24 of those values to their printed digits (gated).
With GD-OD2 (f_vi = f_v(t_LS), which removes the 10⁻² branch) and GD-OD6
(δ_L total) also applied, the ranges become 1.05–1.11 and 1.26–1.28.

**Gates** (every one in [OD-N] `gates`, all passing):
- the generalised functions equal the frozen [1G-D] functions for the frozen
  inputs (A_v, X_SU and all R*: relative difference 0; budget 1e−12);
- [AUD]'s GD-F1 table (A_v 1172/1465/1235/1623; A_v σ 1.05/1.32/1.15/1.52;
  X_SU 1.30/1.55/1.35/1.63; all twelve R*), GD-F2 values (A_v 4274 / 4914;
  X_SU 3.96 / 4.03; [NW15] A_v σ 4.59 and R* 42.44 / 121.1 / 171.5, the digits
  recorded in the [AUD] inventory; its report rounds 171.5 to "172") and GD-F6
  values (3.95 → 3.83, 2.75 → 2.67);
- [CONS] E-1GD-1…3 at [NW15]'s own radius: σ_LSS = 9.336e−4, PBS
  A_v σ = 4.410 and 2.969;
- [1G-F] observation L3: A_v = 1169 / 1185 for the primary.

## 4. GD-OD1 — the void-seed scale (GD-F1)

**Tick (verbatim).** "[B] **GD-OD1, void-seed scale (GD-F1).**" — "[x] Tracker-consistent primary, `R_seed = R_void (f_vi/f_v0)^{1/3}/γ_w0`, giving A_v σ(R8) 1.05–1.5 and X_SU 1.30–1.63. Quote the [SvdW04]-factor values as the alternative."

**Frozen texts and current readings.**

| Location ([1G-D]) | Frozen text | Current reading |
|---|---|---|
| Sec. 7 item 2, "Seed scale" | "[W09]'s 30 h⁻¹ Mpc void diameter (line 277) divided by the [SvdW04] shell-crossing radius factor 1.72, giving R_seed = 11.9 Mpc ([GM]) or 14.3 Mpc ([NW15])" | Primary: the tracker-consistent seed, R_seed = 0.757 / 0.810 Mpc (Sec. 3). Alternative: the [SvdW04] factor, an explicit additional assumption that ignores the tracker's own void growth. ([SvdW04]'s printed 1.7151 does not satisfy its own shell-crossing condition; the root gives 1.6967 ([AUD], [1G-F] Sec. 5), a +0.9% effect on A_v, immaterial here.) |
| Sec. 1 item 4; Sec. 6 table and "The dilution" | "`A_v ≈ 2.9–4.7×10³` gives `X_SU ≈ 2.75–3.95`: large-scale linear growth about 3–4× that of ΛCDM in amplitude"; "about 3–4× ΛCDM's in amplitude (8–16× in power)" | Primary: A_v ≈ 1.17–1.18×10³ and **X_SU = 1.26–1.28** (δ_L total), i.e. about 1.3× ΛCDM's amplitude (about 1.6× in power). With the [SvdW04] factor: X_SU = 3.8–3.9. The dilution statement stands qualitatively (without a void response the cell contrast grows only as f_w D_wall); "dominated by the void-onset mode" holds for both seeds (the void term is 79% ([GM]) and 67% ([NW15]) of D_SU for the primary). |
| Sec. 1 item 5; Sec. 8 table and "Reading" | "`R*(ε = 1) ≈ 28–45 h⁻¹ Mpc`, and its density contrast drops below 10% only above **128–215 h⁻¹ Mpc** … That reproduces [W09]'s "100 h⁻¹ Mpc or somewhat larger" homogeneity scale." | Primary: R*(ε = 1) = 9–10 h⁻¹ Mpc and 10% density contrast at **61–84 h⁻¹ Mpc**; the [SvdW04] factor gives 42–45 and 172–215. The claim that the model *reproduces* [W09]'s ≥ 100 h⁻¹ Mpc homogeneity scale is **not robust**: it holds for the alternative, not for the primary. The model still predicts a homogeneity scale of order 10² h⁻¹ Mpc, set by the void-seed statistics. |
| Sec. 1 item 6; Sec. 9 | "`A_v σ_LSS(R8) ≈ 2.6–4.3 ≫ 1`"; "At R8 (Lagrangian 12.6 Mpc) … `A_v σ_LSS(R8) = 2.6–4.3` (PBS) … Both are ≫ 1." | Primary: **A_v σ_LSS(R8) = 1.05–1.11**, i.e. an rms void-onset shift |ε| ≈ 1 at R8, and R*(ε = 1) ≈ R8. The "≫ 1" holds only for the alternative (3.8–4.6). σ8 sits at the edge of the non-perturbative regime of the void onset. Independently of the seed, R8 < R_void (the dominant voids are 30 h⁻¹ Mpc across), so the wall/void partition at 8 h⁻¹ Mpc is O(1) (partition variance → f_v/f_w ≈ 2.8 for R ≪ R_void; [1G-D] Sec. 9 item 3). The conclusion that no linear global-mean σ8 is defined therefore stands; its PBS figure is convention-dependent corroboration. |
| inventory `void_response_at_R8`, `findings.sigma8_location` | "2.6-4.3 (PBS) >> 1" | as the Sec. 9 row |
| `README.md`, `CLAUDE.md` | "10% density at 128–215 h⁻¹ Mpc"; "non-perturbative" | updated to the primary with the alternative (Sec. 10) |

## 5. GD-OD2 — f_vi (GD-F2)

**Tick (verbatim).** "[B] **GD-OD2, f_vi (GD-F2).**" — "[x] Restrict f_vi to the tracker's f_v(t_LS): 9.47e−5 ([GM]) and 5.07e−5 ([NW15])."

**Frozen text.** [1G-D] Sec. 7 item 2, "Result": "for f_vi ∈ {10⁻⁴, 10⁻²} (line 1815), ν = 3.72 or 2.33 and A_v = 4260 / 2869 ([GM]) or 4724 / 3181 ([NW15])"; the step "since τ ∝ 1/f_vi".

**Current reading.** The step "τ ∝ 1/f_vi" is derived inside the tracker
(`d ln τ/d ln f_vi = −1/(1 − f_vi)`), and inside the tracker f_vi is fixed:
`f_vi = f_v(t_LS)` = 9.471e−5 ([GM]) and 5.073e−5 ([NW15]). f_vi is
restricted to these values. [W09]'s range {10⁻⁴, 10⁻²} (l. 1814–1815) and
the frozen A_v values built on it are superseded; the 10⁻² branch, which set
every lower end of the frozen ranges, is outside the tracker. [W09]'s own
fits used f_vi = 10⁻⁴ (footT, l. 2412–2418), close to the [GM] value.

## 6. GD-OD3 — the separate-universe mode set rests on S1 (GD-F3)

**Tick (verbatim).** "[B] **GD-OD3 (GD-F3).**" — "[x] Reclassify the SU-mode identification as `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` (S1), cite [GM] l. 620, and condition the headline and the X_SU lower bound on S1."

**Frozen texts.** [1G-D] Sec. 1 item 2 and Sec. 4 heading: "Separate-universe (SU) modes `DERIVED_FROM_VERIFIED_DEFINITIONS` … The long-wavelength (k → 0) perturbations of the two-scale model are: a wall-curvature mode … a void-onset mode"; Sec. 1 item 3: "**The volume-average CGI growth of [1G-A] is therefore not Timescape's long-wavelength growth.**"; Sec. 1 item 4 and Sec. 6: "A_v = 0 gives the lower bound `X_SU ≥ 0.293` ([GM] parameters) or 0.448 ([NW15])".

**Current reading.**
- **Two classes.** The *exactness* of the modes stays
  `DERIVED_FROM_VERIFIED_DEFINITIONS`: each is an exact k → 0 solution of
  [GM] (4.9)–(4.11) ([AUD] Sec. 4.2: zero residual symbolically, from an
  exact two-region cell). The *identification* "the long-wavelength
  perturbations of the two-scale model are" these modes is
  **`DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` (S1)**.
- **[GM] l. 620.** Of the timescape walls, [GM] write that "the curvature
  within such idealised wall regions is not a free choice within the
  framework, but instead must be vanishing by construction". The
  wall-curvature mode therefore goes beyond the timescape construction; S1
  admits it. S1 also keeps the wall bang-time mode (δ_w ∝ t⁻¹) and drops the
  void bang-time mode.
- **Headline, conditioned.** Under S1, the volume-average CGI growth of [1G-A]
  is not Timescape's long-wavelength growth. The token value
  `GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY = FAILED_FOR_TIMESCAPE_TRACKER`
  is unaffected: the void-onset mode alone, which needs no wall curvature,
  fails every closure, and no linear combination of SU modes has `P̃_eff ≡ 0`
  ([AUD] Sec. 4.3).
- **X_SU lower bound, conditioned.** `X_SU ≥ 0.293` ([GM]) / 0.448 ([NW15])
  with A_v = 0 exists only if wall curvature is admitted (S1). With [GM]'s
  flat walls (l. 620) the A_v = 0 bound is 0.
- `README.md` and `CLAUDE.md` state the headline under S1 (Sec. 10).

## 7. GD-OD4 — "[W09] internally inconsistent" (GD-F4)

**Tick (verbatim).** "[B] **GD-OD4 (GD-F4).**" — "[x] Reword "[W09] internally inconsistent" as the auditor proposes."

| Location ([1G-D]) | Frozen text | Current reading |
|---|---|---|
| Sec. 1 item 5 | "[W09]'s own "single density perturbation" seeding relation instead gives 1000–4750 h⁻¹ Mpc, which is internally inconsistent with that claim." | Reading [W09]'s "single density perturbation" relation (`initc`, l. 1807–1811) as a void-onset response, `A_v = 1/|δ_H|` — a construction of [1G-D], not a statement of [W09] — gives 1000–4750 h⁻¹ Mpc. This reading is therefore **not a viable response relation**. It does not show that [W09] is internally inconsistent: [W09] never states a response of a region's void fraction to a long-wavelength mode. |
| Sec. 8 "Reading" | "[W09]'s own single-perturbation seeding would push homogeneity to ≳1 h⁻¹ Gpc and is not compatible with [W09]'s homogeneity claim." | "Reading [W09]'s single-perturbation seeding as a void-onset response would push homogeneity to ≳ 1 h⁻¹ Gpc; that reading is not a viable response relation." |
| inventory (transition-scale finding) | "inconsistent with W09 homogeneity claim" | "the A_v = 1/|delta_H| reading of [W09] (initc) is not a viable response relation" |

## 8. GD-OD5 — Mészáros and barotropic characterisation (GD-F5)

**Tick (verbatim).** "[B] **GD-OD5 (GD-F5).**" — "[x] Correct the Mészáros/barotropic characterisation in the report, the inventory and the `GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY` comment. The value is unchanged."

| Location | Frozen text | Current reading |
|---|---|---|
| [1G-D] Sec. 1 item 3 | "Mészáros (`Δ_eff = 0`) and barotropic (`P̃ = c²_s Δ_eff`) fail too." | [GM] (4.27) is (4.11) without the source `4πG ρ_eff (Δ_eff + 3P̃_eff)`, which equals `−δQ` at k → 0. An SU mode satisfies the Mészáros approximation **iff δQ = 0**, not iff Δ_eff = 0 ([GM] l. 500: Δ_eff = P̃ = 0 together would force all perturbations to zero). Only a decaying combination satisfies it (`c_bw = 1.5 c_bv`, wall and void bang times). The barotropic closure `P̃ = c²_s Δ_eff` holds **exactly, for all t**, for the global bang-time shift (`c_bw = c_bv`, decaying). **No growing SU mode** satisfies either ([AUD] Sec. 4.3, exact null-space solutions). |
| [1G-D] Sec. 5 "Reading" | "Mészáros sets `Δ_eff = 0`, which is also inconsistent."; "Barotropic imposes `P̃/Δ_eff = c²_s`. That agrees only asymptotically early, and only for the void-onset mode (−0.499 vs −0.500), which behaves like a time shift of f_v." | as the row above |
| [1G-D] inventory `gm_closures_su_consistency.meszaros`; artifact field `gm_meszaros: {"Delta_eff": 0.0}` (frozen script l. 171) | "Delta_eff = 0" | "delta Q = 0 (the (4.27) source 4 pi G rho_eff (Delta_eff + 3 P_eff) vanishes)"; the frozen script and its artifact field name are not changed |
| `scientific_status.py`, comment of `GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY` | "[GM]'s comoving (Delta_eff/Delta_d = +0.18...+0.20, P_eff = 0), Meszaros (Delta_eff = 0) and barotropic (P_eff = c_s^2 Delta_eff) closures are inconsistent with them." | the comment now states the comoving closure admits no SU mode, and that the Mészáros (δQ = 0) and barotropic conditions hold only for decaying bang-time combinations, for no growing SU mode (Sec. 10). Value `FAILED_FOR_TIMESCAPE_TRACKER` unchanged. |

## 9. GD-OD6 and GD-OD7

**GD-OD6 — tick (verbatim).** "**GD-OD6, definition of δ_L in S2.** The effect on X_SU is about 3%." — "[x] Total contrast at last scattering."

**Frozen text.** [1G-D] Sec. 6, S2: "The primordial long-wavelength mode of a super-cell region, with linear contrast δ_L at last scattering, sets `ε = A_v δ_L` as well as the wall-curvature growing mode." with `D_SU = f_w D_wall + A_v a_LS f_v`, which normalises the wall mode to δ_L.

**Current reading.** δ_L is the **total contrast of the region at last
scattering**; `D_SU` is as in Sec. 3. [AUD]'s GD-F6 values reproduce
(3.95 → 3.83 and 2.75 → 2.67 for the frozen [GM] PBS amplitudes); for the
primary the effect is −2.5% / −2.0% (1.295 → 1.263, 1.312 → 1.285).

**GD-OD7 — tick (verbatim).** "**GD-OD7.**" — "[x] Recompute σ_LSS(R8) at [NW15]'s own radius (12.226 Mpc) in the new numerics script, and update the "2.6–4.3" token comment accordingly."

**Current reading.** [OD-N] evaluates σ_LSS(R8) at each case's own
equal-mass radius (12.570168 / 12.226040 Mpc): 8.982e−4 and 9.336e−4. The
frozen script's hard-coded 12.57 is unchanged (frozen); its [NW15] value
(9.162e−4) is superseded. With the frozen PBS amplitudes the [NW15] figures
are 4.410 and 2.969 ([CONS] E-1GD-1…3). With GD-OD1/OD2 applied the figure is
1.05–1.11 (primary) and 3.8–4.6 ([SvdW04] factor). The token comment is
updated to these numbers (Sec. 10); its rationale is not rebased (the
GD-OD1 sub-option that would do so is unticked).

## 10. Status token comments and documentation

In `scientific_status.py` only two comments change; no value changes and
the 1F-C-R validator still passes:
- `GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY` (GD-OD5): the Mészáros and
  barotropic characterisation of Sec. 8.
- `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` (GD-OD7): "A_v sigma_LSS(R8) =
  2.6-4.3 for the peak-background split" becomes 1.05–1.11 with the
  tracker-consistent void seed (primary) and 3.8–4.6 with the [SvdW04] seed
  factor, each at its own equal-mass R8 and f_vi = f_v(t_LS), citing this
  record; the frozen figure is named as superseded.

`CLAUDE.md` (1G-D entry) and `README.md` (σ-track paragraph) carry the S1
condition (GD-OD3), the primary numbers with the alternative (GD-OD1/OD2) and
the "not a viable response relation" wording (GD-OD4).

## 11. Open items (not decided here)

- GD-OD1's unticked sub-option: rebasing the rationale of
  `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` on the "R8 < R_void partition"
  argument. With the primary seed the PBS figure is ≈ 1 (|ε| ≈ 1 at R8), so
  the comment's "non-perturbative" rests mainly on that partition argument,
  which the comment does not state.
- [AUD] OD5's sub-question whether to rename the frozen artifact field
  `gm_meszaros.Delta_eff` (not covered by the tick; the frozen script is
  unchanged).
- [1G-D] Sec. 11 item 5, author question on f_vi and the primordial density,
  stays open.

## 12. Files changed

| File | Change |
|---|---|
| `reports/phase1g_d_owner_decisions_successor.md` | this record (new) |
| `reports/phase1g_d_owner_decisions_successor_inventory.json` | its canonical companion (new) |
| `src/timescape_fsigma8/scientific_status.py` | two comments (GD-OD5, GD-OD7); no value |
| `scripts/phase1g_owner_decisions_numerics.py` | new evidence script (shared with 1G-A and 1G-E) |
| `CLAUDE.md`, `README.md` | the 1G-D entries |
| `tests/test_phase1g_d_owner_decisions.py`, `tests/phase1g_owner_decisions_test_utils.py` | new regression of this record; shared helpers |

Not changed: [1G-D], its inventory and script, [ADD], [AUD], [CONS], every
other frozen report and inventory, every token value, equation and tolerance.

## 13. Validation and tag readiness

- **Evidence script.** `scripts/phase1g_owner_decisions_numerics.py`:
  124/124 gates pass on CPython 3.14.3 and 3.11.9 (Windows); the two
  artifacts are identical apart from the environment block and one
  quadrature error estimate ([WIN] Sec. 7).
- **Regression.** `tests/test_phase1g_d_owner_decisions.py`: the record is
  canonical, carries the ticks verbatim and pins the frozen files by
  SHA-256; the two token comments changed as ticked and the rationale is not
  rebased; every token value is unchanged; every number the inventory
  quotes equals the artifact.
- **Final runs** (both full suites, the 1F-C-R validator, the tolerance
  audit and every Phase 1G script, on both interpreters): [WIN] Sec. 7.
- **Tag readiness.** Every blocking 1G-D decision (GD-OD1 to GD-OD5) is
  ticked and applied here, the consolidation errata are in place, and both
  suites pass on Windows. 1G-D is ready for
  `phase-1g-d-separate-universe-growth-v1` on the `main` commit that carries
  this record (task Sec. 5). Approvals 3–5 (local tags, push and pull
  request, merge) are not given, so nothing is tagged, pushed or merged
  here.
