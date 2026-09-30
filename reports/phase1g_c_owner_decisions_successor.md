# Phase 1G-C — owner decisions successor record

Record classification: `OWNER_DECISIONS_SUCCESSOR_RECORD`.
Parent checkpoint: `63ca316` (`main`, the merge of the Phase 1G audit pull
request), local branch `phase-1g-owner-decisions`. Date: 2026-09-30.
Machine-readable companion:
[`phase1g_c_owner_decisions_successor_inventory.json`](phase1g_c_owner_decisions_successor_inventory.json).

Cited as:
- [1G-C] = [`phase1g_c_two_scale_growth_law.md`](phase1g_c_two_scale_growth_law.md)
  and its inventory (frozen);
- [AUD] = [`phase1g_c_adversarial_audit.md`](phase1g_c_adversarial_audit.md)
  (findings GC-F1 … GC-F9);
- [CONS] = [`phase1g_adversarial_audit_errata_successor.md`](phase1g_adversarial_audit_errata_successor.md)
  (errata E-1GC-1 … -4, i.e. GC-F7 and GC-F8, are already applied there);
- [ADD] = [`phase1g_status_additions_successor.md`](phase1g_status_additions_successor.md)
  (the six 1G-C/1G-D tokens; frozen);
- [1G-D] = [`phase1g_d_separate_universe_growth.md`](phase1g_d_separate_universe_growth.md);
- [WIN] = [`phase1g_windows_validation_record.md`](phase1g_windows_validation_record.md),
  the Windows validation and the final runs;
- [W09] = Wiltshire, arXiv:0909.0749v2 (`observe.tex`); [W07] =
  arXiv:0709.0732v2 (`solution.tex`); [GM] = arXiv:2511.17160v2. Line
  numbers are those of the e-print sources as verified by [AUD].

The frozen [1G-C], its inventory, [ADD], [AUD] and [CONS] are **not
edited**. Every correction here is text only: no equation, number, status
token value, tolerance or code changes.

## 1. Authorisation

The project owner's task statement of 2026-09-30 ("Phase 1G — Windows
validation, owner decisions for 1G-A/C/D/E, tags"), Sec. 0, gives these
approvals, verbatim:

1. "Create the local branch `phase-1g-owner-decisions` from `main` and commit there."
2. "Apply the owner decisions ticked `[x]` in Sec. 3, exactly as ticked. An unticked decision is **not** approved: leave it open and list it at the end."

Approvals 3–6 (local signed tags, push and pull request, merge, tag push) are
unticked and therefore not given. This record applies approval 2 to the
1G-C items of Sec. 3. Every 1G-C item has one ticked option; the unticked
alternatives (GC-OD1 "keep 'supersedes' in narrowed form", GC-OD5 "add a
wall-adapted convention") are not applied.

## 2. Decisions

| Id | Blocks the tag | Ticked option (verbatim in Secs. 3–8) |
|---|---|---|
| GC-OD1 (GC-F1) | yes | Accept, and withdraw "supersedes … for σ8-scale statistics" |
| GC-OD2 (GC-F2) | yes | Split the evidence class; align CLAUDE.md and README |
| GC-OD3 (GC-F3) | yes | Add assumption A5 to Secs. 5–6 and to the token comment; value unchanged |
| GC-OD4 (GC-F4) | no | Extend the superseded-readings table; qualify CLAUDE.md and README |
| GC-OD5 (GC-F5) | no | Label (b), (c) as volume-average conventions and drop the envelope |
| GC-OD6, OD7 (GC-F6, GC-F9) | no | "Algebraic consistency checks"; governance and wording changes |

## 3. GC-OD1 — what the wall σ is (GC-F1)

**Tick (verbatim).** "[B] **GC-OD1 (GC-F1).** Narrow verdict 4 and Secs. 4, 7 and 9 to "the wall-internal linear σ at M8, relative to the wall mean". Quote [W09] ll. 383–386 with its footnote, and withdraw "settled"." — "[x] Accept, and withdraw "supersedes … for σ8-scale statistics"."

**[W09] in full.** Lines 383–386: "Below the scale of statistical homogeneity
we will typically find density contrasts |δρ/ρ| ∼ 1 which characterize the
nonlinear regime". Footnote foot11 (lines 2648–2651): "My two scales refer to
largest relevant scales in the 'nonlinear regime'". [1G-C] Sec. 4 quoted the
first sentence without its last words. In [W09]'s own model, the wall/void
partition that sets the mass distribution at 8 h⁻¹ Mpc is the nonlinear
product of sub-cell fluctuations; the dominant voids (30 h⁻¹ Mpc across,
[W09] l. 277) are wider than the 16 h⁻¹ Mpc σ8 sphere.

**Frozen texts and current readings.**

| Location ([1G-C]) | Frozen text | Current reading |
|---|---|---|
| Sec. 1 verdict 4 (l. 44–52) | "**Conditional σ(M8) (mass-weighted, framework-consistent):** 0.834 … 0.935 …; 0.83–0.96 across the three radius conventions … This supersedes 1G-A's volume-average values (0.52–0.69) *for σ8-scale, mass-weighted statistics*. Those values remain the super-cell growth." | **The wall-internal linear σ at mass M8, relative to the wall mean**, under A1–A5 (Sec. 5 below): 0.834 ([GM]) and 0.935 ([NW15]) at equal mass. It is not a mass-weighted σ(M8) relative to the global mean. The "supersedes … for σ8-scale, mass-weighted statistics" statement is **withdrawn**: the wall statistic and 1G-A's volume-average values answer different questions, and neither is a global-mean σ at 8 h⁻¹ Mpc (`LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC = NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY`). "Those values remain the super-cell growth" is also superseded ([1G-D] Sec. 5). The "0.83–0.96" envelope is dropped (GC-OD5, Sec. 7). |
| Sec. 4 "Consequence" (l. 133–140), class `DERIVED_FROM_VERIFIED_DEFINITIONS` | "mass-weighted fluctuations at 8 h⁻¹ Mpc are governed by the wall regional dynamics, not by the volume-average background. 1G-A's volume-average σ(M8) (0.52–0.69) therefore applies the super-cell law outside its domain." | σ8's radius lies inside a dust cell (the quotes are `VERIFIED_FROM_PRIMARY_SOURCE`). The *linear wall-internal field* at that scale evolves under the wall regional dynamics (A1–A5). The wall/void partition at 8 h⁻¹ Mpc is nonlinear ([W09] ll. 383–386 and foot11), so the regional dynamics do **not** govern the mass variance relative to the global mean. Identifying [GM]'s coarse-grained dust with [W09]'s ≥ 100 h⁻¹ Mpc dust cells is an assumption: class `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`. |
| Sec. 7 "Reading" (l. 231–235) | "the mass-weighted linear σ(M8) of a Timescape universe with Planck's early universe is about **3–15% above** Planck-ΛCDM at equal mass. Across all three conventions the range is +3% to +18%." | Under A1–A5, the wall-internal linear σ at mass M8, relative to the wall mean, is 0.834 / 0.935 at equal mass. Its comparison with Planck-ΛCDM's global-mean linear σ8 (0.811) compares different statistics and is withdrawn as a reading; the numbers themselves are unchanged. The "+3% to +18%" envelope is dropped (Sec. 7). |
| Sec. 9 item 1 (l. 278–282) | "**The open problem is settled within the framework.** … it is now settled for mass-weighted σ(M8): the wall-regional law applies" | **Withdrawn.** The wall-regional law gives the wall-internal linear statistic only ([1G-D] Sec. 9). The global-mean mass variance at 8 h⁻¹ Mpc is a nonlinear two-phase quantity (1G-E, 1G-F). |
| Inventory `supersedes` | "1G-A volume-average sigma(M8) for sub-cell mass-weighted statistics; those values remain the super-cell growth" | withdrawn (as verdict 4) |
| Inventory `scale_hierarchy` | "W09_homogeneity_scale … dust cells coarse-grained there (W09 lines 311-461)"; class `VERIFIED_FROM_PRIMARY_SOURCE` | the quotes stay `VERIFIED_FROM_PRIMARY_SOURCE`, completed by [W09] ll. 383–386 and foot11; the consequence drawn from them is as Sec. 4 above |

This agrees with the owner-approved narrowing already in the comment of
`TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW` (via [1G-D] Sec. 9). The token
*name* keeps "MASS_WEIGHTED_SUB_CELL"; token names are API and are not
renamed ([AUD] Sec. 12).

## 4. GC-OD2 — the "exactly two FLRW regions" class (GC-F2)

**Tick (verbatim).** "[B] **GC-OD2 (GC-F2).**" — "[x] Split the evidence class: kinematics `VERIFIED_FROM_PRIMARY_SOURCE` (+ derived); dynamics `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`. Align CLAUDE.md and README."

**Frozen text.** [1G-C] Sec. 1 verdict 1 (l. 27–32) and Sec. 3 heading: "**The tracker is exactly two FLRW regions in the common time t** (`DERIVED_FROM_VERIFIED_DEFINITIONS`, verified to ≤ 3e−15)"; inventory `tracker_two_region_structure.class = "DERIVED_FROM_VERIFIED_DEFINITIONS; numerically verified <= 3e-15"`; Sec. 5 A1 (l. 147–149): "The tracker satisfies it exactly (Sec. 3)."

**Current reading (split class).**
- **Kinematics — `VERIFIED_FROM_PRIMARY_SOURCE` + derived.** `a_v ∝ t`
  (H_v = 1/t) and `a_w,reg ∝ t^{2/3}` (H_w = 2/(3t)) follow from [GM] (5.1),
  (5.5)–(5.6), and [W07] states both explicitly (solution.tex l. 317–321:
  "`a_w = a_w0 t^{2/3}` … exactly that of an Einstein–de Sitter universe, but
  in volume average time not locally measured wall time"; l. 404–406: "the
  void regions expand exactly as a Milne universe in volume–average time").
  The volume-level identities (H_D, Q_D, ⟨R⟩, γ_w H_w = H_D) are derived.
- **Dynamics — `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`.** `ρ_v = 0`,
  `ρ_w = 1/(6πGt²)`, "all matter sits in walls", "FLRW regions", and
  "backreaction and curvature are exactly the partition terms" hold under
  (i) the regional dust Friedmann/Raychaudhuri equations in the common time
  t with `Q_v = Q_w = 0` ([GM] l. 618; [W09] l. 510), (ii) flat walls ([GM]
  footnote, l. 620) and (iii) the D1-corrected `⟨R⟩_D = −6 f_v/t²`. With
  the printed (5.7) prefactor the void density would be negative. This is the
  class the live token `REGIONAL_DUST_FLRW_EQUATIONS` already records.
  Under these assumptions the result is exact ([AUD]: ≤ 1.3e−34, non-circular).
- **A1** is a model postulate ([GM] l. 618; [W07] l. 211–215; [W09] l. 510)
  that the tracker is consistent with, and was built on. It is not a property
  the tracker "satisfies exactly". [W09]'s own assumption is weaker than FLRW
  (foot2, l. 2399–2404).

**CLAUDE.md and README** now say "kinematically, the tracker is empty Milne
voids plus EdS walls in common time t; its dynamics are exact under the
regional dust-FLRW assumption" instead of "exactly empty Milne voids plus EdS
walls".

## 5. GC-OD3 — assumption A5, the clock of the wall matter (GC-F3)

**Tick (verbatim).** "[B] **GC-OD3 (GC-F3).**" — "[x] Add assumption A5 ("the wall matter clocks the common time t") to Secs. 5–6 and to the `TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW` comment. The value is unchanged."

**The assumption.** **A5 — the wall matter clocks the common (coarse-grained
dust) time t.** [1G-C] A2 and Sec. 6 evolve wall matter with [GM]'s
dust-frame equations in t, which identifies t with the proper time of the
wall matter. [GM] make t the dust proper time (l. 441) of "the idealised
coarse-grained dust flow" (l. 636). Timescape itself writes the wall geometry
and the sub-cell Hubble flow in local proper time τ_w ([W07] l. 211–215,
229–230, 261–262; [W09] l. 269–272, 461–475, 483–485), and [W07] notes the
mismatch (l. 320–321: EdS "in volume average time not locally measured wall
time").

**Current readings.**

| Location ([1G-C]) | Frozen text | Current reading |
|---|---|---|
| Sec. 5 "Assumptions" (l. 146–160), inventory `regional_growth_law.assumptions` | A1–A4 | **A1–A5.** The wall law `Δ_w ∝ t^{2/3}` and `X_wall = γ_w0(1−f_v0)^{1/3}/g_Λ` hold under A1–A5; the class stays `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`. |
| Sec. 1 verdict 4 "(A1–A4, Sec. 5)", l. 52 | A1–A4 | A1–A5 |
| Sec. 6 (l. 211–215): "The common-time law of Sec. 5 is thus the only admissible regional law within [GM]'s dust-proper-time framework. Wall observers' clocks enter σ8 only through the redshift–time map." | as quoted | Given A5, the common-time law is the only regional dust-FLRW law on the regional wall volume `a_w,reg`: t is the only time in which that volume obeys flat-dust Friedmann with the tracker's mass budget. The τ_w alternative fails the mass budget **for any `ρ_v ≥ 0`**: it would need `ρ_v/⟨ρ⟩ = (1−γ_w0²)/f_v0` = −1.184 ([GM]) or −1.157 ([NW15]) ([AUD] Sec. 9), so it is inadmissible even if voids hold matter. The last sentence is an **assumption (A5)**, not a result: it holds only if wall observers' clocks are not the clock of the wall matter's dynamics. |
| `scientific_status.py`, comment of `TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW` | "under assumptions A1-A4" | "under assumptions A1-A5 (A5, added with the owner decision of 2026-09-30: the wall matter clocks the common time t)"; the value `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` is unchanged |

The inadmissibility of the τ_w variant stays
`DERIVED_FROM_VERIFIED_DEFINITIONS` (with `ρ_v ≥ 0`) and consistent with
`NAIVE_W09_WALL_CLOCK_AS_REGIONAL_PROPER_DUST_FLRW_CLOCK = REJECTED_UNSUPPORTED`.

## 6. GC-OD4 — superseded readings (GC-F4)

**Tick (verbatim).** "**GC-OD4.**" — "[x] Extend the superseded-readings table and qualify CLAUDE.md and README."

[ADD] Sec. 4 lists, for 1G-C, only Sec. 10 item 2, Sec. 12 and the inventory's
`status_tokens_changed`; [1G-D] lists Sec. 8 and Sec. 9's "settled". [ADD] is
frozen, so the extension is this table. Together with those two lists it is
the complete set of superseded 1G-C readings.

| [1G-C] location | Superseded by |
|---|---|
| Sec. 1 verdict 1; Sec. 3 heading class; inventory `tracker_two_region_structure.class` | Sec. 4 (GC-OD2) |
| Sec. 1 verdict 4, including "0.83–0.96" and "supersedes"; inventory `supersedes` | Sec. 3 (GC-OD1), Sec. 7 (GC-OD5) |
| Sec. 1 verdict 5 ("sharp observational discriminant"); Sec. 8 "transition" paragraph ("self-similar", "sharp, testable signature") | [1G-D] Sec. 5 (the P(k) step), Sec. 8 below (GC-OD7) |
| Sec. 3 "These facts are implicit" and the identity table's "max rel. error" | [CONS] E-1GC-4; Sec. 8 below (GC-OD6) |
| Sec. 4 "Consequence" and its class | Sec. 3 (GC-OD1) |
| Sec. 5 assumptions A1–A4; A1 "satisfies it exactly"; the numerical check | Secs. 4, 5 and 8 (GC-OD2, OD3, OD6) |
| Sec. 6 last paragraph | Sec. 5 (GC-OD3) |
| Sec. 7 conventions (b), (c) and the "Reading" (3–15%, +3% to +18%) | Secs. 3 and 7 (GC-OD1, OD5) |
| Sec. 9 item 1 ("settled"; "reinterpreted as super-cell growth") | Sec. 3 (GC-OD1); [1G-D] Sec. 5 |
| Sec. 10 heading ("none applied") against item 1 ("already sent") | Sec. 8 (GC-OD7) |
| Inventory `regional_growth_law.assumptions` (A1–A4) | Sec. 5 (GC-OD3) |

**CLAUDE.md and README.** The sentences "so mass-weighted σ(M8) follows the
wall law: 0.83–0.96" (CLAUDE.md, 1G-C entry) and "Mass-weighted σ at the
Planck 8 h⁻¹ Mpc mass follows the wall-regional growth law: 0.83–0.96"
(README) now read "the wall-internal linear σ at mass M8, relative to the
wall mean, follows the wall law: 0.834 ([GM]) and 0.935 ([NW15]) at equal
mass", with the conditionality A1–A5.

## 7. GC-OD5 — radius conventions and the envelope (GC-F5)

**Tick (verbatim).** "**GC-OD5.** Label conventions (b) and (c) as volume-average conventions, and:" — "[x] drop the "0.83–0.96 / +3% to +18%" envelope".

**Current reading.** Conventions (b) (8/h_dressed) and (c) (8/h̄/γ_w0) of
[1G-A] Sec. 6.4 are **volume-average-picture conventions**; (c) uses
volume-average proper length, which includes void expansion. For the wall
law they are not a convention envelope. The (b) and (c) values (0.912,
0.960 [GM]; 0.891, 0.958 [NW15]) stay as computed numbers of those
conventions, but "0.83–0.96 across the three radius conventions" and "+3% to
+18%" are **dropped** as a range claim. The equal-mass headline (0.834 /
0.935), whose convention is frame-free, is unaffected. No wall-adapted
convention is added (the unticked alternative); [1G-C] Sec. 9 item 3 already
lists the radius convention as open.

## 8. GC-OD6, OD7 — check wording and governance (GC-F6, GC-F9)

**Tick (verbatim).** "**GC-OD6, OD7.**" — "[x] Describe the checks as "algebraic consistency checks", and apply the governance and wording changes."

| Location ([1G-C]) | Frozen text | Current reading |
|---|---|---|
| Sec. 3 identity table, column "max rel. error" (≤ 2.9e−15); inventory `max_identity_error` | presented as verification of the two-region identities | **Algebraic consistency checks**: package closed forms against algebraically identical rearrangements (for example `Q_D = 2f(1−f)/(3t²)` against `6f(1−f)(1/t − 2/(3t))²`, with `H_v`, `H_w` hard-coded); the column measures floating-point rounding. The non-circular check is [AUD] Sec. 4 (mpmath, 40 digits, printed definitions: ≤ 1.3e−34). |
| Sec. 5 "Numerical check" (1.6e−13) | integration of the regional equation | An algebraic consistency check of the integrator on the EdS equation: its coefficients reduce exactly to `2/(3t)` and `1/(6πGt²)`. |
| Sec. 10 heading "none applied; each requires human approval" with item 1 "The lead has already sent this scope addition to the 1G-B implementer" | inconsistent | Item 1 was applied: the lead added the wall-regional growth-law option to the 1G-B runtime during that phase (1G-B validation report Sec. 1, Sec. 5). The owner's tick of GC-OD7 is recorded as the confirmation GC-F9 asks for: that option stands approved. It is consistent with the owner's approval of 2026-09-29 of the 1G-B documented limitation, which names the option. |
| Sec. 1 verdict 5 "a sharp observational discriminant"; Sec. 8 "a sharp, testable signature" | observational labels | "a conditional theoretical feature (no observational comparison is made)"; the step itself is superseded ([1G-D] Sec. 5). |
| Sec. 8 "The tracker is self-similar and has no length scale" | "self-similar" | "The tracker has no sub-horizon length scale": it has a time scale τ, with `f_v = t/(t+τ)`; only the family is self-similar in `H_D0 t` ([AUD] Sec. 11). |

## 9. Status token comment

`scientific_status.py`: only the comment of
`TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW` changes (A5, Sec. 5). Its value
and every other token are unchanged; the 1F-C-R validator reads values, not
comments, and still passes.

## 10. Files changed

| File | Change |
|---|---|
| `reports/phase1g_c_owner_decisions_successor.md` | this record (new) |
| `reports/phase1g_c_owner_decisions_successor_inventory.json` | its canonical companion (new) |
| `src/timescape_fsigma8/scientific_status.py` | the comment of `TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW` (A5); value unchanged |
| `CLAUDE.md`, `README.md` | the 1G-C entries (GC-OD2, OD4, OD5) |
| `tests/test_phase1g_c_owner_decisions.py`, `tests/phase1g_owner_decisions_test_utils.py` | new regression of this record; shared helpers |

Not changed: [1G-C], its inventory and script, [ADD], [AUD], [CONS], every
other frozen report and inventory, every token value, equation and tolerance.

## 11. Validation and tag readiness

- **Regression.** `tests/test_phase1g_c_owner_decisions.py`: the record is
  canonical, carries the ticks verbatim and pins the frozen files by
  SHA-256; the token comment names A5; every token value is unchanged.
- No number is recomputed: every 1G-C decision is text only.
- **Final runs** (both full suites, the 1F-C-R validator, the tolerance
  audit and every Phase 1G script, on both interpreters): [WIN] Sec. 7.
- **Tag readiness.** Every blocking 1G-C decision (GC-OD1, GC-OD2 and
  GC-OD3) is ticked and applied here, the consolidation errata are in place,
  and both suites pass on Windows. 1G-C is ready for
  `phase-1g-c-two-scale-growth-law-v1` on the `main` commit that carries
  this record (task Sec. 5). Approvals 3–5 (local tags, push and pull
  request, merge) are not given, so nothing is tagged, pushed or merged
  here.
