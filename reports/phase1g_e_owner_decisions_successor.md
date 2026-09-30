# Phase 1G-E — owner decisions successor record

Record classification: `OWNER_DECISIONS_SUCCESSOR_RECORD`.
Parent checkpoint: `63ca316` (`main`, the merge of the Phase 1G audit pull
request), local branch `phase-1g-owner-decisions`. Date: 2026-09-30.
Machine-readable companion:
[`phase1g_e_owner_decisions_successor_inventory.json`](phase1g_e_owner_decisions_successor_inventory.json).

Cited as:
- [1G-E] = [`phase1g_e_two_phase_sigma.md`](phase1g_e_two_phase_sigma.md),
  its inventory and `scripts/phase1g_e_two_phase_sigma_numerics.py` (frozen);
- [AUD] = [`phase1g_e_adversarial_audit.md`](phase1g_e_adversarial_audit.md)
  (findings GE-F1 … GE-F7);
- [CONS] = [`phase1g_adversarial_audit_errata_successor.md`](phase1g_adversarial_audit_errata_successor.md)
  (errata E-1GE-1 … -7 applied there; lead observation L1 on the E4 frame);
- [TOK] = [`phase1g_e_status_addition_successor.md`](phase1g_e_status_addition_successor.md),
  the record that added `TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC` (frozen);
- [1G-F] = [`phase1g_f_void_population.md`](phase1g_f_void_population.md) and its inventory;
- [WIN] = [`phase1g_windows_validation_record.md`](phase1g_windows_validation_record.md),
  the Windows validation and the final runs;
- [OD-N] = `scripts/phase1g_owner_decisions_numerics.py`, artifact
  `artifacts/independent/phase1g_owner_decisions.json`, keys
  `results.GE_single_radius`, `results.GE_reference_population_1G_F`,
  `results.GE_mc_seed_scatter`;
- [W09] arXiv:0909.0749v2 (`observe.tex`, line numbers as verified by [AUD]).

The frozen [1G-E] report, inventory and script, [TOK], [AUD], [CONS] and
[1G-F] are **not edited**. The token value
`TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC = DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`
is unchanged. No package module changes for 1G-E.

## 1. Authorisation

The project owner's task statement of 2026-09-30 ("Phase 1G — Windows
validation, owner decisions for 1G-A/C/D/E, tags"), Sec. 0, gives these
approvals, verbatim:

1. "Create the local branch `phase-1g-owner-decisions` from `main` and commit there."
2. "Apply the owner decisions ticked `[x]` in Sec. 3, exactly as ticked. An unticked decision is **not** approved: leave it open and list it at the end."

Approvals 3–6 (local signed tags, push and pull request, merge, tag push) are
unticked and therefore not given. This record applies approval 2 to the six
1G-E items of Sec. 3. **Unticked, not applied:** GE-OD1 "[ ] Restrict 1G-E
to δ_v = −1."; GE-OD2 "[ ] Keep the single radius as an explicit
idealisation, not attributed to [W09]." and "[ ] Use the auditor's
[W09]-consistent population (σ ≈ 1.0–1.2)."; GE-OD3 "[ ] keep
`s = f_w^{1/3}` with its frame stated."; GE-OD4 "[ ] Justify (b) for the
Planck comparison."

## 2. Decisions

| Id | Blocks the tag | Ticked option |
|---|---|---|
| GE-OD1 (GE-F1) | yes | the mass-conserving σ formula; the δ_v table, "−9%" and the range updated |
| GE-OD2 (GE-F2) | yes | the 1G-F derived population as the reference (σ ≈ 0.99); the single 15 h⁻¹ Mpc radius relabelled an idealisation |
| GE-OD3 + L1 (GE-F3) | yes | E4 a two-sided sensitivity; photon-frame compression `s = D_wall` primary |
| GE-OD4 (GE-F4) | yes | the equal-mass values beside convention (b) |
| GE-OD5 (GE-F5) | yes | MC precision as the scatter across seeds; the first-run sentence corrected |
| GE-OD6 | no | the four corrections of [AUD] Sec. 4.8 recorded; value unchanged |

GE-OD1 to GE-OD4 act on the same numbers. [OD-N] recomputes the [1G-E]
one-radius model with all of them applied, and evaluates the [1G-F]
reference population at both radius conventions. Every [1G-E], [1G-F] and
[AUD] value it can reproduce is gated to its recorded digits (46 gates).

## 3. GE-OD1 — the mass-conserving formula (GE-F1)

**Tick (verbatim).** "[B] **GE-OD1, mass conservation (GE-F1).**" — "[x] Adopt `σ² = δ_v²σ²_part + (f_w − f_v δ_v)²σ²_int`. Update the δ_v table (−0.8: 1.298/1.142), the "−9%" reading and the range (0.9–2.1 becomes 0.8–2.1)."

**Frozen text.** [1G-E] l. 29–31 and l. 89–91: "σ²(R) = δ_v² σ²_part(R) + σ²_int(R)" with "non-empty voids scaling the partition amplitude by δ_v²"; the δ_v table (l. 155–161); l. 184 "the void interior: about −9% at δ_v = −0.8"; l. 46–49 range column "0.93–2.12", "0.89–1.74"; inventory `model.formula` and `headline_8_h_inv_Mpc.range_*`; CLAUDE.md "The range is 0.9–2.1".

**Current reading.** With void interiors at `(1+δ_v)⟨ρ⟩` and walls carrying the
remaining mass, mass conservation fixes the wall weight, and

```text
σ²(R) = δ_v² σ²_part(R) + (f_w − f_v δ_v)² σ²_int(R).
```

The factor is 1 at δ_v = −1 (E1), so every tracker (empty-void) number of
[1G-E] is unchanged. [AUD] checked the form on a lattice with exact mean
density; [1G-F] derives the same wall weight independently ([CONS] L2).

**δ_v table** (a = 15 h⁻¹ Mpc, convention (b); [OD-N]):

| δ_v | s = D_wall (primary, Sec. 5) [GM] / [NW15] | s = f_w^{1/3} (frozen primary) [GM] / [NW15] | frozen [1G-E] formula, s = f_w^{1/3} |
|---|---|---|---|
| −1 | **1.759 / 1.523** | 1.572 / 1.357 | 1.572 / 1.357 |
| −0.9 | 1.610 / 1.407 | **1.435 / 1.249** | 1.493 / 1.297 |
| −0.8 | 1.462 / 1.292 | **1.298 / 1.142** | 1.418 / 1.242 |

**"−9%".** At δ_v = −0.8 the change against δ_v = −1 is **−17% / −16%**
(s = f_w^{1/3}: −17.4%, −15.8%) and −17% / −15% for the primary frame
(−16.9%, −15.1%). "About −9%" is superseded.

**Range** over a = 5–30 h⁻¹ Mpc, the E4 sensitivity from `s = f_w^{1/3}` to
`s = 1` (which contains the primary `s = D_wall`), δ_v from −1 to −0.8, at
convention (b): **0.82–2.12** ([GM]) and **0.80–1.74** ([NW15]), i.e.
**0.8–2.1** (was 0.9–2.1). The primary frame alone gives 0.97–2.02 and
0.94–1.70.

## 4. GE-OD2 — the reference void population (GE-F2)

**Tick (verbatim).** "[B] **GE-OD2, primary void population (GE-F2).**" — "[x] Adopt the 1G-F derived population as the reference (σ ≈ 0.99) and relabel the single 15 h⁻¹ Mpc radius as an idealisation."

**Frozen text.** [1G-E] l. 71–76 (E2): "[W09] gives "voids of a characteristic diameter 30 h⁻¹ Mpc" (line 277), so a = 15 h⁻¹ Mpc is the primary value"; l. 44–57 (the "primary" 1.57 / 1.36 and "σ ≈ 1.4–1.6 is about 1.7–1.9 times Planck-ΛCDM's *linear* σ8"); inventory `headline_8_h_inv_Mpc`; [TOK] "E2's radius (15 h⁻¹ Mpc from [W09])".

**Current reading.**
- **E2 is an idealisation.** [W09] l. 277–285: voids of 30 h⁻¹ Mpc
  diameter "fill 40–50% of the universe", and there are "numerous
  minivoids"; the void phase of the two-scale model (f_v0 = 0.737 or 0.627)
  includes them. A single 15 h⁻¹ Mpc radius at the full f_v0 is **not a
  statement of [W09]**; it is kept only as the one-radius idealisation of
  Secs. 3, 5 and 6. In that Boolean model `a` is not the observable void size
  (mean void chord 42 / 34 h⁻¹ Mpc, [AUD] Sec. 4.6).
- **The reference is the [1G-F] derived population**: the excursion-set voids
  of [1G-F] with the wall EdS clock C1, the shell-crossing void barrier and
  the collapse threshold δ_c = 1.686, normalised to the tracker's f_v0,
  empty voids (E1) and the photon-frame compression (Sec. 5); volume-weighted
  median radius 2.4 ([GM]) and 2.8 ([NW15]) h⁻¹ Mpc. It is conditional on
  [1G-F]'s F1–F6 (in particular the C1 clock and the two-scale volume
  budget M3).

| Reference population ([OD-N]) | [GM] σ_part | [GM] σ_int | **[GM] σ** | [NW15] σ_part | [NW15] σ_int | **[NW15] σ** |
|---|---|---|---|---|---|---|
| (b) R = 8/h_dressed | 0.326 | 0.932 | **0.987** | 0.304 | 0.940 | **0.988** |
| (a) equal mass | 0.285 | 0.837 | **0.884** | 0.324 | 0.994 | **1.045** |

The (b) row reproduces the [1G-F] inventory to four decimals (gated). With
the frozen a_D-frame compression the (b) values are 0.823 / 0.833.

**The "1.7–1.9×" reading, restated.** With the reference population, the
two-phase σ in 8 h⁻¹ Mpc balls is ≈ 0.99 at convention (b) (about 1.2 times
Planck-ΛCDM's *linear* σ8 = 0.811) and 0.88–1.05 at equal mass (1.09–1.29
times). The one-radius idealisation gives 1.52–1.76 (b) and 1.59–1.60 (a)
with the primary frame. The comparison still mixes kinds (Sec. 8, correction 4).

## 5. GE-OD3 with lead observation L1 — E4 and its frame (GE-F3)

**Tick (verbatim).** "[B] **GE-OD3 plus lead observation L1, the E4 wall mapping.** Reword E4 as a two-sided sensitivity, and choose the frame:" — "[x] photon-frame compression `s = D_wall` as primary (σ = 1.759 / 1.523 at a = 15);"

**Frozen text.** [1G-E] l. 81–87 (E4): "The primary closure is *isotropic compression*: `ξ_E(r) = ξ_L(r/s)` with `s = f_w^{1/3}`. `s = 1` (no compression) is the upper bracket. Real walls are sheets and filaments, so their compression is anisotropic."; l. 181–182 "+15–26% (uncompressed vs compressed)" ([CONS] E-1GE-3: +14–26%).

**Current reading.**
- **Frame.** The ball radius R = 8/h is in photon-normalised comoving Mpc
  ([1G-A] convention (b); [CONS] E-1GE-4). In those coordinates the wall
  matter is compressed by `a_w,reg/a_photon = γ_w0(1−f_v0)^{1/3} = D_wall`
  (0.877 [GM], 0.946 [NW15]). `s = f_w^{1/3}` (0.641, 0.720) is the
  compression in the a_D (volume-average) frame, which does not match R's
  frame ([CONS] L1; [1G-F] Sec. 3). **The primary E4 is the isotropic
  compression `s = D_wall`.**
- **Two-sided sensitivity.** E4 is not bracketed by `s = 1`. Under E3,
  anisotropic maps of volume f_w (sheets, filaments, orientation-averaged)
  give σ_int *below* the isotropic value; void-shell tangential stretching
  with pairs correlated with the wall orientation (beyond E3) gives values
  *above* `s = 1` ([AUD] Sec. 4.3 table, illustrative). The uncertainty runs
  both ways. `s = f_w^{1/3}` and `s = 1` are reported as the sensitivity.

| a = 15 h⁻¹ Mpc, (b), δ_v = −1 | [GM] σ_int | [GM] σ | [NW15] σ_int | [NW15] σ |
|---|---|---|---|---|
| **s = D_wall (primary)** | 1.348 | **1.759** | 1.220 | **1.523** |
| s = f_w^{1/3} (a_D frame; frozen primary) | 1.093 | 1.572 | 1.006 | 1.357 |
| s = 1 (uncompressed) | 1.464 | 1.850 | 1.267 | 1.561 |

## 6. GE-OD4 — the radius convention (GE-F4)

**Tick (verbatim).** "[B] **GE-OD4, radius convention (GE-F4).**" — "[x] Report the equal-mass values (1.437/1.419) beside convention (b)."

**Frozen text.** [1G-E] l. 142: "**R = 8 h⁻¹ Mpc** (10.95 Mpc for [GM], 13.11 Mpc for [NW15])" ([CONS] E-1GE-4 names it convention (b)); l. 183 "f_v0: about 16% at a = 15".

**Current reading.** Every two-phase σ is reported at convention (b)
(8/h_dressed, R = 10.954 / 13.115 Mpc) **and** at the frame-free
equal-Lagrangian-mass convention (a) of [1G-A] Sec. 6.4 (R = 12.570 /
12.226 Mpc):

| a = 15 h⁻¹ Mpc, δ_v = −1 | (b) [GM] / [NW15] | (a) equal mass [GM] / [NW15] |
|---|---|---|
| s = D_wall (primary) | 1.759 / 1.523 | **1.604 / 1.594** |
| s = f_w^{1/3} | 1.572 / 1.357 | **1.437 / 1.419** ([AUD]; gated) |
| s = 1 | 1.850 / 1.561 | 1.686 / 1.633 |
| reference population (Sec. 4) | 0.987 / 0.988 | 0.884 / 1.045 |

The [GM]/[NW15] difference at a = 15 is 16% at (b) but 0.7% (primary frame)
to 1.3% (a_D frame) at (a): the frozen "f_v0: about 16%" is mostly the radius
convention (the two sets also differ in dressed H0), and is superseded.

## 7. GE-OD5 — Monte Carlo precision (GE-F5)

**Tick (verbatim).** "[B] **GE-OD5, MC precision (GE-F5).**" — "[x] Restate the precision as the scatter across seeds, and correct the first-run sentence."

**Frozen text.** [1G-E] l. 41–42 "Its covariance was checked against an independent Monte Carlo to ≤ 1.5%."; l. 134–138 "The first run fixed the formula at the nominal intensity and failed a 5% gate at 14%. The cause was the Poisson fluctuation of the ball count in one finite box (2% fewer balls, which shifts f_w by 4.5%), not the model."

**Current reading (precision).** The frozen `monte_carlo_boolean`
(a = 15 h⁻¹ Mpc, box 30a, the frozen sample sizes), run with the 16 seeds of
[AUD] (20260929 and 1–15), gives ([OD-N] `results.GE_mc_seed_scatter`):

| | [GM] | [NW15] |
|---|---|---|
| gated maximum error over 16 seeds: min / median / max | 1.00% / 3.13% / **5.03%** | 0.16% / 0.97% / 3.95% |
| seeds above the frozen 5% gate (realised intensity) | 1 (seed 12) | 0 |
| seeds above it at the nominal intensity | 3 (seeds 9, 10, 13) | 1 (seed 10) |
| frozen seed 20260929: realised / nominal intensity | 1.51% / 1.62% | 0.91% / 1.67% |
| scatter (sd) of σ²_part MC/analytic − 1 | 3.1% | 1.5% |

Every entry reproduces [AUD] Sec. 4.4 to its printed digits (the minimum,
median, maximum and failure counts are gated in [OD-N]); the seeded Monte
Carlo gives the same values on Linux and on both Windows interpreters.

The precision of the one-realisation check is therefore **about 3% ([GM]) and
1.5% ([NW15]) (the scatter of σ²_part across seeds)**, not "≤ 1.5%", which is
one favourable draw. The frozen 5% gate, evaluated per seed, fails for one
seed of 16 for [GM] (seed 12, 5.03%) and none for [NW15] at the realised
intensity (3 and 1 at the nominal intensity). The ensemble agrees with the
Boolean formula; [AUD]'s independent 24-realisation lattice ensemble confirms
it (σ²_part −0.3 ± 0.4%
[GM], 0.0 ± 0.3% [NW15] at the realised intensity). No gate is changed: the
frozen script keeps its seed and 5% gate; [OD-N] sets the seed and lifts the
gate in memory only to record every seed's error, then applies the unchanged
5% gate per seed.

**Current reading (first run).** Under the model `f_w = e^{−λV}`, 2% fewer
balls shift f_w by `λV × 2% = −ln(f_w) × 2%`: **2.7% ([GM]) and 2.0%
([NW15])**, not 4.5%. The first-run configuration is not recorded, so its
14% cannot be reproduced, and its attribution to the ball count alone is
superseded. With
the final box and the frozen seed the nominal-intensity comparison already
passes (1.62% / 1.67%, [AUD]); the box enlargement, not the change to the
realised intensity, removed the failure.

## 8. GE-OD6 — the recorded meaning of the 1G-E token

**Tick (verbatim).** "**GE-OD6, meaning of the 1G-E token.**" — "[x] Record the four corrections of the audit's Sec. 4.8 in a successor note. The value is unchanged."

[TOK] Sec. 1 records the meaning of
`TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC = DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`
with E1–E4 quoted from the frozen [1G-E] inventory. [TOK] is frozen; this is
the successor note. The value stays.

| [AUD] Sec. 4.8 | [TOK] reading | Current reading |
|---|---|---|
| 1. formula | "σ² = δ_v² σ²_part + σ²_int" | exact under E1 (δ_v = −1), where it equals the mass-conserving form; for δ_v ≠ −1 the form is `δ_v²σ²_part + (f_w − f_v δ_v)²σ²_int` (Sec. 3) |
| 2. E2 | "Boolean voids: Poisson balls of radius a … E2's radius (15 h⁻¹ Mpc from [W09]) is an external input" | the single radius at the full f_v0 is an idealisation, not a [W09] statement; the reference population is [1G-F]'s derived one (Sec. 4) |
| 3. E4 | "isotropic compression s = f_w^{1/3} (primary) or s = 1 (bracket)" | isotropic compression `s = D_wall` (photon frame, primary); `s = f_w^{1/3}` and `s = 1` a two-sided sensitivity, not a bracket (Sec. 5) |
| 4. kind | "a conditional, nonlinear, model-internal quantity" | a **hybrid**: the partition term is nonlinear; the wall-internal term is linear theory extrapolated to σ_int ≈ 1. It is not a full nonlinear variance. |

The comment of the token in `scientific_status.py` states the formula under
E1 ("empty voids"), where it is exact, and E4 generically ("isotropic
Eulerian compression of the wall field"); no ticked decision asks for a
comment change, so none is made.

## 9. Files changed

| File | Change |
|---|---|
| `reports/phase1g_e_owner_decisions_successor.md` | this record (new) |
| `reports/phase1g_e_owner_decisions_successor_inventory.json` | its canonical companion (new) |
| `scripts/phase1g_owner_decisions_numerics.py` | new evidence script (shared with 1G-A and 1G-D) |
| `CLAUDE.md`, `README.md` | the 1G-E entries |
| `tests/test_phase1g_e_owner_decisions.py`, `tests/phase1g_owner_decisions_test_utils.py` | new regression of this record; shared helpers |

Not changed: [1G-E], its inventory and script, [TOK], [AUD], [CONS], [1G-F],
every package module, every token value, equation and tolerance.

## 10. Validation and tag readiness

- **Evidence script.** `scripts/phase1g_owner_decisions_numerics.py`:
  124/124 gates pass on CPython 3.14.3 and 3.11.9 (Windows); the two
  artifacts are identical apart from the environment block and one
  quadrature error estimate ([WIN] Sec. 7).
- **Regression.** `tests/test_phase1g_e_owner_decisions.py`: the record is
  canonical, carries the ticks verbatim and pins the frozen files by
  SHA-256 (including the frozen 1G-F script and inventory); the token value
  is unchanged; every number the inventory quotes equals the artifact.
- **Final runs** (both full suites, the 1F-C-R validator, the tolerance
  audit and every Phase 1G script, on both interpreters): [WIN] Sec. 7.
- **Tag readiness.** Every blocking 1G-E decision (GE-OD1 to GE-OD5) is
  ticked and applied here, the consolidation errata are in place, and both
  suites pass on Windows. 1G-E is ready for `phase-1g-e-two-phase-sigma-v1`
  on the `main` commit that carries this record (task Sec. 5). Approvals 3–5
  (local tags, push and pull request, merge) are not given, so nothing is
  tagged, pushed or merged here.
