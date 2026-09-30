# Phase 1G-A — owner decisions successor record

Record classification: `OWNER_DECISIONS_SUCCESSOR_RECORD`.
Parent checkpoint: `63ca316` (`main`, the merge of the Phase 1G audit pull
request), local branch `phase-1g-owner-decisions`. Date: 2026-09-30.
Machine-readable companion:
[`phase1g_a_owner_decisions_successor_inventory.json`](phase1g_a_owner_decisions_successor_inventory.json).

Cited as:
- [1G-A] = [`phase1g_a_sigma8_derivation_path_audit.md`](phase1g_a_sigma8_derivation_path_audit.md)
  and its inventory (frozen);
- [SUCC] = [`phase1g_a_barotropic_status_successor.md`](phase1g_a_barotropic_status_successor.md)
  and its inventory (frozen);
- [AUD] = [`phase1g_a_adversarial_audit.md`](phase1g_a_adversarial_audit.md), the
  independent adversarial audit (findings GA-F1 … GA-F11);
- [CONS] = [`phase1g_adversarial_audit_errata_successor.md`](phase1g_adversarial_audit_errata_successor.md),
  the consolidation (errata E-1GA-1 … -8 are already applied there as
  successor readings);
- [WIN] = [`phase1g_windows_validation_record.md`](phase1g_windows_validation_record.md),
  the Windows validation and the final runs;
- [OD-N] = `scripts/phase1g_owner_decisions_numerics.py` and its git-ignored
  artifact `artifacts/independent/phase1g_owner_decisions.json`, key
  `results.GA_*`.

The frozen [1G-A], [SUCC], [AUD] and [CONS] texts are **not edited**. Each
section below gives the verbatim tick, the frozen text, the current reading
and the evidence. Nothing here changes an equation, a status token, a
tolerance, a default, an initial condition, a unit or a sign convention.

## 1. Authorisation

The project owner's task statement of 2026-09-30 ("Phase 1G — Windows
validation, owner decisions for 1G-A/C/D/E, tags"), Sec. 0, gives these
approvals, verbatim:

1. "Create the local branch `phase-1g-owner-decisions` from `main` and commit there."
2. "Apply the owner decisions ticked `[x]` in Sec. 3, exactly as ticked. An unticked decision is **not** approved: leave it open and list it at the end."

and leaves these unticked, so **not** approved: "[ ] Create signed annotated
tags **locally** for the phases that Sec. 5 finds ready.", "[ ] Push
`phase-1g-owner-decisions` and open ONE pull request against `main`.",
"[ ] Merge that pull request (merge commit, as PR #1 and PR #2).", "[ ] Push
the tags created under approval 3."

This record applies approval 2 to the four 1G-A items of Sec. 3. All four are
ticked; the ticks are quoted verbatim in each section.

## 2. Decisions

| Id | Blocks the tag | Ticked option (verbatim, abridged in Secs. 3–6) | Applied in |
|---|---|---|---|
| GA-OD1 (GA-F1) | yes | Accept: convention-dependent verdict, qualified Sec. 4 conclusion, author question | Sec. 3, Sec. 7 |
| GA-OD2 (GA-F2) | yes | (i) Planck early universe as a declared hybrid primary; corrected f_b justification; [NW15]'s own inputs as a sensitivity | Sec. 4 |
| GA-OD3 (GA-F3) | yes | Name the unit chain; 557–694 under the report's radius conventions; keep the test pin with a comment naming the chain | Sec. 5 |
| GA-OD4 (GA-F4–F8, F11) | no | Accept all, in one successor note | Sec. 6 |

## 3. GA-OD1 — App. B "backward-parabolic" verdict (GA-F1)

**Tick (verbatim).** "[B] **GA-OD1, App. B "backward-parabolic" verdict (GA-F1).** The verdict holds only for the printed (B.4) sign; under `RESOLVED_DERIVED_4_10` the closure reduces to a constraint." — "[x] Accept: record it as convention-dependent, qualify "only the comoving closure (and Mészáros) can define a linear σ", and add an author question on the (B.4) sign."

**Frozen text.**
- [1G-A] Sec. 4.2 heading and class: "Homogeneous-density closure ([GM] App. B): backward-parabolic", `DERIVED_FROM_VERIFIED_DEFINITIONS`; l. 168: "The initial-value problem is ill-posed, and modes grow like `exp(k² ∫dt/2Θa²)`, faster than the barotropic case."
- [1G-A] l. 205–206: "Among the closures in [GM], only the comoving closure (and the Mészáros comparator) can define a linear σ."
- [1G-A] inventory `closure_admissibility.homogeneous_density_B3_B5`: `verdict = BACKWARD_PARABOLIC_ILL_POSED`, `class = DERIVED_FROM_VERIFIED_DEFINITIONS`.

**Current reading.**
- The verdict is **`CONVENTION_DEPENDENT` (D3)**. It holds for [GM]
  (B.3)–(B.5) *as printed*: the printed (B.4) equals ½ × [(4.10) with
  P̃ → −P̃], the `printed_4_15` sign of the ΘP̃ term ([AUD] Sec. 4.2, SymPy
  residual 0). There the closure is backward-parabolic and ill-posed; [AUD]
  corroborates it numerically for the first time (slope of
  ln|Δ^(eff)(t0)| in k² → β = ∫dt/(2Θa_D²) = 0.3295).
- Under the project's adjudicated `D3_VERDICT = RESOLVED_DERIVED_4_10`,
  (4.10) with (B.2) loses Δ̇^(eff) identically and reduces to the constraint
  `(Θ̇/Θ − k²/(a²Θ)) Δ^(eff) + (1 + w) Z = 0`. The closure is then a
  constrained system. It is **not shown to be ill-posed**: [AUD] integrates
  it on the tracker for k ≤ 10⁴ and finds bounded growth that tends to the
  Mészáros value at high k (Δ_d(t0)/Δ_d(t_i) = 9.998187 at k = 10⁴ against
  9.998186).
- [GM] do not use App. B ([GM] l. 1187), and neither does [1G-A]; no σ number
  changes. Both D3 branches of the barotropic runtime stay mandatory and
  unchanged; the package has no App. B implementation.

**Qualified Sec. 4 conclusion (current reading of l. 205–206).** Among the
closures in [GM], the comoving closure (and the Mészáros comparator) define
a linear σ. The barotropic closure admits none on either D3 branch (Sec. 4.1;
see Sec. 6, GA-F5, for the window and spectrum qualifiers). The App. B
homogeneous-density closure admits none in the `printed_4_15` sign convention
as printed; under `RESOLVED_DERIVED_4_10` it reduces to a constrained system
that is not shown to be ill-posed and is not evaluated here.

**Evidence.** [AUD] Sec. 4.2 and GA-F1 (SymPy re-derivation `appB_check.py`,
numerical reduction `appB_consistent.py`); [GM] l. 1165–1176, l. 1187.
Not recomputed here: the decision records a classification, not a number.

## 4. GA-OD2 — early-universe inputs of the [NW15] row (GA-F2)

**Tick (verbatim).** "[B] **GA-OD2, early-universe inputs of the [NW15] row (GA-F2).** [NW15]'s own fit has f_b ≈ 0.18 and n_s ≈ 0.99." — "[x] (i) Keep the Planck early universe as a declared hybrid primary. Correct the f_b justification and add [NW15]'s own inputs as a sensitivity (σ 0.637–0.645; wall law 0.89–0.90)." Option (ii) (switch the primary and propagate) is not ticked.

**Frozen text.** [1G-A] l. 364–366: "[NW15] report that the baryon/non-baryon ratio is pinned by the 2nd/3rd peak ratio "as long as the standard cosmology is assumed up to the surface of last scattering", so Planck's f_b is the primary closure."

**Current reading (the corrected justification).**
- The quote is accurate: it is the [NW15] abstract (l. 110–113). It states a
  relation between the baryon/non-baryon ratio and the peak heights; it does
  not fix Planck's value. [NW15]'s own Timescape fit ([NW15] table, l.
  1526–1568, as read by [AUD] Sec. 4.6) has f_b ≈ 0.18 (bare
  Ω̄_B0/Ω̄_M0 = 0.039/0.215 = 0.181; dressed 0.089/0.489 = 0.182),
  n_s = 0.992 ± 0.009, and A_s as an unconstrained nuisance parameter.
- The [NW15] row of [1G-A] is therefore a **declared hybrid**: the [NW15]
  background (f_v0 = 0.627, H0 = 61.0 km/s/Mpc) with the Planck early
  universe (f_b = 0.1563, n_s = 0.9649, A_s = 2.100e−9). By owner decision it
  stays the primary for both parameter sets. It is a choice, not a reading of
  [NW15].
- [NW15]'s own inputs are a sensitivity. A_s stays Planck's, since [NW15] fit
  none.

**Sensitivity** ([OD-N] `results.GA_OD2_nw15_own_early_universe_inputs`; EH98
no-wiggle, Planck-anchored as [1G-A] Sec. 7; f_b = 0.039/0.215 = 0.18140):

| [NW15] early universe | CGI comoving (a) / (b) / (c) | CGI Mészáros (a) / (b) / (c) | wall law (a) / (b) / (c) |
|---|---|---|---|
| Planck hybrid (primary; [1G-A]) | **0.6687** / 0.6374 / 0.6855 | 0.5954 / 0.5676 / 0.6104 | **0.9347** / 0.8910 / 0.9582 |
| [NW15] f_b | **0.6370** / 0.6076 / 0.6528 | 0.5672 / 0.5411 / 0.5813 | **0.8904** / 0.8494 / 0.9126 |
| [NW15] f_b and n_s = 0.992 | **0.6431** / 0.6130 / 0.6594 | 0.5727 / 0.5459 / 0.5872 | **0.8990** / 0.8569 / 0.9217 |

(a) equal mass, (b) 8/h_dressed, (c) 8/h̄ ([1G-A] Sec. 6.4). The
equal-mass values reproduce [AUD]'s EH98 values (0.637, 0.643; 0.890,
0.899) to their printed digits (gated in [OD-N]). [AUD]'s CAMB 2.0.4
cross-check gives 0.639 / 0.645 and 0.893 / 0.902; CAMB is not run here. So
the sensitivity is σ = 0.637–0.645 (EH98–CAMB) for the comoving closure and
0.89–0.90 for the wall law: 4–5% below the hybrid primary, inside [1G-A]'s
own f_b band (±7–8%).

**Downstream quotes.** The [NW15] numbers quoted by 1G-C (0.935), 1G-E
(1.36) and 1G-F, and in `CLAUDE.md` and `README.md`, use the Planck hybrid.
They stay the primary; option (ii), which would have propagated [NW15]'s own
inputs, is not ticked.

## 5. GA-OD3 — the "αk ≈ 875" illustration (GA-F3)

**Tick (verbatim).** "[B] **GA-OD3, "αk ≈ 875" (GA-F3).**" — "[x] Name the unit chain, give 557–694 under the report's own radius conventions, and keep the test pin with a comment naming the chain."

**Frozen text.**
- [1G-A] l. 141–144: "Take kR = 1 with R = 8/h Mpc (h = 0.7303) and the 1D-A §10 unit chain: k_matrix ≈ 513 and `αk ≈ 875`. That exceeds `ln(float64 max) = 709.8`, so the linear barotropic amplitude is not even representable."
- [1G-A] inventory `closure_admissibility.barotropic.wkb_exponent_at_kR_1_R8 = 875.4`; [SUCC] l. 72–75 and inventory `evidence.wkb_exponent_at_kR_1_R8 = 875.4`.
- `tests/test_barotropic_hadamard_refutation.py`: `EXPONENT_KR1_R8_1G_A = 875.4` and the comment "(1D-A Sec. 10 unit chain, as in [1G-A])".

**Current reading (the chain named).** The 875 figure uses a **hybrid chain**:
`k_matrix = a_D0 (c/H0) k_phys0_D`, with the present *volume-average physical*
wavenumber `k_phys0_D = 1/R` and R = 8/h_dressed Mpc. 1D-A §10 states that
`k_phys0_D` cannot be inserted directly into `k_com R_com`; the chain is
therefore not the 1D-A §10 chain that the frozen text names. It corresponds
to a photon-normalised radius of 8.005 Mpc, smaller than every [1G-A]
Sec. 6.4 radius. In the package normalisation (a_w0 = 1, a_D(1+z) → 1
early), a photon-normalised comoving radius R_γ gives `k_code = (c/H0)/R_γ`:

| Chain at kR = 1 ([GM] preset, α = 1.7069482) | k_code | αk | kR at which αk reaches ln(float64 max) = 709.78 |
|---|---|---|---|
| hybrid (frozen [1G-A]; test pin) | 512.83 | **875.38** | 0.811 |
| (a) equal Lagrangian mass, R = 12.570 Mpc | 326.57 | **557.44** | 1.273 |
| (b) 8/h_dressed, R = 10.954 Mpc | 374.74 | **639.66** | 1.110 |
| (c) 8/h̄/γ_w0, R = 10.104 Mpc | 406.28 | **693.49** | 1.023 |

([OD-N] `results.GA_OD3_wkb_exponent_chains`; every value reproduces [AUD]'s
to its printed digits.) So "not even representable at kR = 1" is
convention-dependent: under the report's own conventions αk = 557–694 at
kR = 1, and every convention exceeds 709.8 for kR ≳ 1.27. The Hadamard
ill-posedness, the divergence of σ_R and the token
`UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY = REFUTED_HADAMARD_ILL_POSED`
are unaffected.

**Test.** The pin `EXPONENT_KR1_R8_1G_A = 875.4` and its assertions (the
value and `> ln(float64 max)`) stay exactly as they are, as a regression of
the named chain. Only the two adjacent comments change: they now name the
hybrid chain, say that 1D-A §10 excludes it, give the (a)–(c) values and
cite this record.

## 6. GA-OD4 — wording and classes (GA-F4–F8, F11)

**Tick (verbatim).** "**GA-OD4, wording and classes (GA-F4–F8, F11).**" — "[x] Accept all, in one successor note."

This section is that note. Each row replaces the frozen reading **as the
current reading**; no number, token or tolerance changes.

| Finding | Frozen text ([1G-A]) | Current reading |
|---|---|---|
| GA-F4 | l. 370–371: "The expected bias sources are omitted BAO wiggles and Planck's 0.06 eV neutrino suppression (about −1.5%)." | The EH98 no-wiggle +3.03% against the Planck anchor decomposes ([AUD] Sec. 4.6, CAMB 2.0.4) as +1.17% fit error (no-wiggle against CAMB at the same cosmology), +0.39% recipe cosmology (0.315, 0.674 against the [P18] means) and +1.43% the 0.06 eV neutrinos; wiggles account for 0.33%. The anchored-ratio bias is ≤ 0.5% ([AUD] E-factor table), confirming the "≲ 1%" fork estimate. |
| GA-F5 | Sec. 1 row 5 "no linear barotropic σ_R exists"; Sec. 9 row C "permanently excluded"; [SUCC] "meaning" | "No linear barotropic σ_R exists **for a window with power-law tails and a spectrum bounded below by a power law**" (the scope already stated in Sec. 4.1, l. 146–149). Equivalently: no finite, IR-controlled linear barotropic σ_R. A Gaussian window gives a finite but meaningless value dominated by k ≈ α/R²_code ([AUD] Sec. 4.1). |
| GA-F6 | l. 180–181: decaying modes "fall as `t^{-5/3}` relative to the growing mode, per the `growing_mode` module" | Near the regular (u, q) fixed point, deviations fall as t^{−5/3}. [GM]'s exact Z ≡ 0 mode ([GM] l. 570; Δ_d constant) falls only as t^{−2/3} in Δ_d relative to the growing mode. It is singular early (Δ^(eff)/Δ_d ≈ −1/(2f_v)), so regular initial conditions exclude it and no number changes. The same imprecision in the frozen `perturbations/growing_mode.py` docstring is noted only (package scope; not edited). |
| GA-F7 | l. 412–416: "every examined fork gives **less linear structure than Planck-ΛCDM** … The sign of the effect is robust across closures, presets, conventions and baryon fractions." | The sign holds **within the volume-average CGI closures**. The same report's two-scale fork (Sec. 8) gives values above 0.811 (0.83–0.96); after the 1G-C owner decisions that fork is the wall-internal linear statistic relative to the wall mean, not a global-mean σ ([`phase1g_c_owner_decisions_successor.md`](phase1g_c_owner_decisions_successor.md)). |
| GA-F8 | l. 384, 388: convention (b) "8/h_dressed Mpc of wall-comoving length"; "(b) assumes wall rulers measure wall-comoving length with the dressed h" | Convention (b) is **dressed-comoving ([GM] Eq. (5.4) a_w)**; Sec. 5.3 of the same report shows the (5.4) a_w is not the wall-regional scale factor. With the (5.1) regional reading, R = (8/h)/[γ_w0(1−f_v0)^{1/3}] = **12.494 Mpc** ([GM]) and **13.871 Mpc** ([NW15]); the comoving σ becomes 0.526 / 0.613 and the wall σ 0.837 / 0.857 ([OD-N] `results.GA_F8_regional_radius_reading`; [AUD]'s values reproduced). All stay inside the stated budgets. |
| GA-F11 | l. 86–92: "Evidence classes follow 1D-C §5" (one primary class per conclusion); l. 325 "numerically verified to 1e−13"; Sec. 5.3 `VERIFIED_FROM_PRIMARY_SOURCE` | The classes actually used also include composites (Sec. 4.1, `DERIVED_FROM_VERIFIED_DEFINITIONS` + `NUMERICALLY_CORROBORATED`), `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` (Sec. 8) and, after GA-OD1, `CONVENTION_DEPENDENT` (Sec. 4.2); Sec. 2's list is read to include them. The Sec. 6.2 "numerically verified to 1e−13" is an **arithmetic consistency check** of the same p. 25 normalisation, not independent evidence. Sec. 5.3 is split: the textual finding (two meanings of a_w in [GM]) is `VERIFIED_FROM_PRIMARY_SOURCE`; the statement that the two differ, with its 16.6%, is `DERIVED_FROM_VERIFIED_DEFINITIONS` + `NUMERICALLY_CORROBORATED`. |

The unambiguous errata GA-F9 and GA-F10 were applied by [CONS] (E-1GA-1,
-5, -6, -7, -8), except the platform round-off statements E-1GA-2, -3, -4.
The Windows values of those three bounds are recorded as a platform
observation in [`phase1g_windows_validation_record.md`](phase1g_windows_validation_record.md).

## 7. Author question (added under GA-OD1)

For the Timescape authors ([GM]): in App. B, is the sign of the ΘP̃ term in
the printed (B.4) intended? The printed (B.4) equals ½ × [(4.10) with
P̃ → −P̃], the same sign flip that separates the printed (4.15) from
(4.10) + (4.13) (the project's D3 discrepancy, adjudicated
`RESOLVED_DERIVED_4_10`), while the printed (B.5) equals (4.11) with +P̃.
With the (4.10) sign, (B.2) turns (4.10) into a constraint. Which form do the
authors intend for the homogeneous-density closure?

## 8. Files changed

| File | Change |
|---|---|
| `reports/phase1g_a_owner_decisions_successor.md` | this record (new) |
| `reports/phase1g_a_owner_decisions_successor_inventory.json` | its canonical companion (new) |
| `tests/test_barotropic_hadamard_refutation.py` | two comments name the hybrid chain (GA-OD3); no assertion, value or tolerance changes |
| `scripts/phase1g_owner_decisions_numerics.py` | new evidence script (shared with 1G-D and 1G-E) |
| `tests/test_phase1g_a_owner_decisions.py`, `tests/phase1g_owner_decisions_test_utils.py` | new regression of this record; shared helpers |

Not changed: [1G-A], [SUCC], [AUD], [CONS] and every other frozen report and
inventory; every package module; every status token, equation and tolerance.

## 9. Validation and tag readiness

- **Evidence script.** `scripts/phase1g_owner_decisions_numerics.py`:
  124/124 gates pass on CPython 3.14.3 and 3.11.9 (Windows); the two
  artifacts are identical apart from the environment block and one
  quadrature error estimate ([WIN] Sec. 7).
- **Regression.** `tests/test_phase1g_a_owner_decisions.py`: the record is
  canonical, carries the ticks verbatim and pins the frozen files by
  SHA-256; the token values are unchanged; the test pin is kept with its new
  comment; every number the inventory quotes equals the artifact.
- **Final runs** (both full suites, the 1F-C-R validator, the tolerance
  audit and every Phase 1G script, on both interpreters): [WIN] Sec. 7.
- **Tag readiness.** Every blocking 1G-A decision (GA-OD1, GA-OD2 and
  GA-OD3) is ticked and applied here, the consolidation errata are in place,
  and both suites pass on Windows. 1G-A is ready for
  `phase-1g-a-sigma8-derivation-path-v1` on the `main` commit that carries
  this record (task Sec. 5). Approvals 3–5 (local tags, push and pull
  request, merge) are not given, so nothing is tagged, pushed or merged
  here.
