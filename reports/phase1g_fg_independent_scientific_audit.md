# Phase 1G-F successor / Phase 1G-G — independent scientific and numerical audit

Date: 2026-10-02. Classification: `REPORT_ONLY_INDEPENDENT_AUDIT`.
Auditor: Claude Code (Claude Opus 5.5), at the project owner's request. The
auditor did not write the audited deliverables.
Companion: [`phase1g_fg_independent_scientific_audit_inventory.json`](phase1g_fg_independent_scientific_audit_inventory.json).

**Object.** The 2026-10-01 local deliverables, applied with `git apply` on
branch `phase-1g-f-successor-g-evolution` at the declared base
`fb5d95245bc0cb19ce6cd1438177f1a597bb232f`:

- edits to `CLAUDE.md` and `README.md`;
- nine untracked files: the F successor report and inventory, the G report
  and inventory, the F/G validation record, two evidence scripts and two
  test modules.

**What this audit did not do.** It modified no audited file, frozen record,
package module, status token or existing artifact. It staged, committed,
pushed and tagged nothing. Its only repository writes are this report and
its inventory.

## 0. Verdicts

| Area | Verdict | Blocks integration |
|---|---|---|
| F — fixed-domain volume-budget successor | `ACCEPT_WITH_CORRECTIONS` | FGA-F1 |
| G — conditional void-evolution research | `ACCEPT_WITH_CORRECTIONS` | none |
| Documentation and provenance | `ACCEPT_WITH_CORRECTIONS` | FGA-D1 (owner decision) |

- **Equations.** No error was found in F1–F3 or G1–G12. Each identity was
  checked in exact rational arithmetic. The conditional deductions were
  re-derived independently (Sec. 3).
- **The F correction is right.** The frozen M3 radius-cut value (F3)
  normalises each cut to a different universe and is not additive. F2 is
  the additive fixed-domain cumulative. F2 was re-applied, without
  discrepancy, to all 84 archived populations.
- **Headline numbers reproduced** by independent code: the full void
  volume (0.7519694), ≥10 h⁻¹ Mpc fractions (1.48% / 1.92%), medians
  (2.405 / 2.800 h⁻¹ Mpc), cutoffs and the variance σ = 0.98708 / 0.98814.
  - The audited tail cumulatives carry a systematic discretisation bias:
    +0.23% at ≥10 and +0.7% at ≥15 h⁻¹ Mpc (FGA-F3).
- **σ ≈ 0.99.** F2 does not change any input of the primary variance, and
  the wall-field share is 89.07% / 90.56%. The variance is a conditional
  hybrid. One ingredient is not stated: its Boolean grains are not the
  disjoint F population (FGA-F2).
- **Findings.** 0 HIGH, 3 MEDIUM, 10 LOW, 5 INFO (Sec. 8). The MEDIUM ones
  are:
  - an incomplete supersession of frozen F statements (FGA-F1);
  - a missing hybrid ingredient of σ ≈ 0.99 (FGA-F2);
  - an undecided reinterpretation of an owner-approved 1G-D status token
    (FGA-D1).
- **Tests.** Both full suites pass in the real checkout: 1125 passed,
  0 skipped, 0 failed on Python 3.14.3 and on 3.11.9, with warnings as
  errors. The historical Git-blob test passes unmodified.
- **Status.** Passing tests establish no observational prediction and no
  new authorisation. No status token changes. `SIGMA8_AUTHORIZATION` stays
  `NOT_GRANTED`.

## 1. Preflight and protection of the work

- **Repository.** Branch `phase-1g-f-successor-g-evolution`;
  `HEAD = fb5d95245bc0cb19ce6cd1438177f1a597bb232f`, the declared base and
  remote `main` (read-only `git ls-remote`).
  - Tracked files: 259. Only `CLAUDE.md` and `README.md` differ from HEAD,
    by 85 insertions and 35 deletions.
  - Untracked: exactly the nine listed files. No stash.
- **Interpreters.**
  - CPython 3.14.3 (`.venv`): NumPy 2.5.2, SciPy 1.18.1, pytest 9.1.1.
  - CPython 3.11.9 (`.venv311`): NumPy 2.4.6, SciPy 1.17.1, pytest 9.1.1.
  - Windows 11; `OPENBLAS_NUM_THREADS=1` in every run.
  - No dependency was installed or updated. SymPy and mpmath are not
    available, so symbolic checks use exact `fractions.Fraction`
    arithmetic.
- **Audited files** (SHA-256, identical at start and end; LF, no CR):

| File | SHA-256 |
|---|---|
| CLAUDE.md | `8437e67389ec94e0266d6c5c2ad1a2d30fb6808feec5a04c306a3c86d7b37ff8` |
| README.md | `c4f9b4a4f6e5ecfa9e8b8d595b25f58df25cc3ecd62480eb8c8566de8ed1097d` |
| reports/phase1g_f_volume_budget_successor.md | `7e1df34c20b17455d2b82e32b03c5b1b7cf6f9249524badd81a20a29e5fb395e` |
| reports/phase1g_f_volume_budget_successor_inventory.json | `c641a025b5fa8522a430f0a3e6e26d801293615b94eb2ffe4cfa8512d8bbe88d` |
| reports/phase1g_fg_successor_validation.md | `d395982a510e3a1dca0c8433eaa7410390136fdf6d0853e09b0a7b0d52ac31ca` |
| reports/phase1g_g_void_evolution.md | `7bf1fd384eeed5514d84f75b9c36db22d61a1529c6935b6de23d29255a1a4bbd` |
| reports/phase1g_g_void_evolution_inventory.json | `2be9d42b49dde60065ba12444a84ed4fffe76cd470ac2ecbae1696e5d2e73826` |
| scripts/phase1g_f_volume_budget_successor_numerics.py | `d0030a842f2f86e02de145d3265fc21e5c2100dd04b4a8c6f6c704b987f0beb9` |
| scripts/phase1g_g_void_evolution_numerics.py | `db11ad5cf3a3fde254118f7ba14914d57e5dd875b8138979adea21ff99137c14` |
| tests/test_phase1g_f_volume_budget_successor.py | `206cc9846a6ca5fe26e181535aef004864de1d329b96871e4b5a9b567ac0c21c` |
| tests/test_phase1g_g_void_evolution.py | `5d8b517e140ea087075391987c8ed2ac258a8efd9a2707b383fe4fb05b351478` |

- **Frozen dependencies.** The five `frozen_sha256` entries in both
  inventories match the checkout: AGENTS.md, the frozen 1G-F
  script/report/inventory, and `scientific_status.py`.
- **Artifacts present before the audit.**
  - The frozen F artifact `phase1g_f_void_population.json` (SHA-256
    `4523ef03…`) equals the successor's recorded input. It carries the
    snapshot environment (Linux, CPython 3.12.14), so it is the snapshot
    run, not the original 1G-F run.
  - A successor artifact had been regenerated on Windows / 3.14.3 at
    2026-10-02 15:40, before this audit (SHA-256 `2f8931a5…`, CRLF). It is
    byte-identical to the auditor's isolated rerun.
  - No G artifact existed in the checkout.
- **Protection.**
  - All 366 files under `artifacts/` were copied and checksummed before any
    run, and were verified unchanged afterwards.
  - The F successor and G scripts were rerun only in an isolated copy, with
    outputs written outside the repository.

## 2. Primary sources and equation numbers

The arXiv LaTeX e-prints were downloaded on 2026-10-02. The SHA-256 of
`voids_mnras.tex`, `voids.tex` and `main.tex` equal those recorded in the
frozen 1G-F inventory. Printed numbers were reconstructed with an
independent parser (row counter with `\nonumber`, appendix letters, section
prefixes) and checked by hand at every cited equation.

| Source | Cited | Verified content |
|---|---|---|
| [JLH13] arXiv:1304.6087 | (2), (6)–(7), (13), (14), (15)–(17) | (2) σ²(R) definition; (6)–(7) two-barrier series and 𝒟, x; (13) cumulative volume ∫V dn (additive); (14) F(0) = (r_NL/r_L)³(1−𝒟); (15)–(17) Vdn model ✓ |
| [JLH13] App. A | (A4)–(A5), (A8), (A9), (A11), (A12) | parametric R(η), t(η); shell crossing sinh η(sinh η−η)/(cosh η−1)² = 8/9; 1+Δ = 0.2047; δ(η); δ_v = −2.717 ✓ |
| [SvdW04] astro-ph/0311260 | (1), (2), (3), (7), (C1)–(C2), (C7), (C8) | first crossing, 𝒟, mass fraction 1−𝒟, v = 1.7³ m/ρ̄, Laplace transforms, (C8) normalisation ✓ |
| [L03] cond-mat/0305670 | (2.2), (4.4)–(4.10) | (2.2) mean-field Smoluchowski equation; (4.4) K = 1; (4.10) c_j = 4(t+2)⁻²[t/(t+2)]^{j−1} ✓. Hence u = N₀∫K dt/2, as G10 states |
| [GM] arXiv:2511.17160v2 | (5.1), (5.4), (5.5), (5.6) | volume partition; a_w = γ_w⁻¹a_D; a_D(t); f_v(t) = 3f_v0 H_D0 t/[3f_v0 H_D0 t + (2+f_v0)(1−f_v0)] ✓ |

- [L03]'s text below (2.2) states its derivation assumes **no spatial
  correlations** between clusters and an averaged morphology. This bears on
  G1 (FGA-G2).
- [GM] Sec. 5.1 states walls flat and voids negatively curved dust FLRW. It
  does not write H_v = 1/t; that follows from (5.1), (5.5) and (5.6)
  (Sec. 5).
- **Not re-verified here.**
  - Eisenstein & Hu (1998), the EH98 transfer, is a 1G-A import; the
    auditor re-typed its Eqs. (26), (28)–(31) but did not fetch the paper.
  - [W09] and the Wiltshire tracker papers were not re-read. No conclusion
    of this audit depends on them beyond what [GM] states.
  - Literature continuum-percolation thresholds are not used.
- **Out of scope.** The frozen 1G-F report cites [SvdW04] (A15) for the
  velocity function g(Θ). The same counting that reproduces its (A21)–(A33)
  places g(Θ) at (A17) and H_s at (A18) (FGA-D7).

No new project deduction is attributed to a paper. F1–F3, G2–G9 and G11 are
correctly marked as project deductions, except for one docstring
(FGA-D5).

## 3. Independent methods

None of the auditor's code imports the project package or scripts.

| ID | Method | Checks |
|---|---|---|
| M1 | Tracker closed forms from [GM]: f_v = t/(t+τ), γ_w = 1+f_v/2, H_D0 from the dressed H0, ⟨ρ⟩₀; z(t) from a_w = a_D/γ_w and (5.5) | ω_m,eff = 0.120475 / 0.130937; D_wall = 0.876792 / 0.945510 (equal to the audited values) |
| M2 | EH98 no-wiggle transfer re-typed; σ(R) by adaptive Gauss–Kronrod in ln k (`epsrel` 1e−10); flat-ΛCDM growth by quadrature | g_Λ = 0.7878126; anchor 0.970577 (frozen 0.970577) |
| M3 | Two-barrier absorption probability from the diffusion eigenfunctions, P_v(S) = (1−𝒟) − Σ_j (2/jπ) sin(jπ𝒟) e^{−j²π²S/2w²}, cross-checked with an image (erfc) form | max difference 8.9e−16; **closed-form cumulatives**, no grid quadrature |
| M4 | Shell crossing from Lagrangian shells: first ∂r/∂R_i = 0 outside the edge, i.e. d ln A/d ln\|Δ_i\| = 1/3, root-found in t; density from (a/R)³; H_v t by finite differences | η_sc = 3.4875224, 1+Δ = 0.20472233, δ_v = −2.7171803, **H_v t = 0.8888888890** |
| M5 | Primary variance: own pair density, Boolean covariance ξ_w = (1−f)^{−E_V γ̃} − 1, size weights from exact bin masses of M3, Simpson quadratures (6001 r and k nodes) | σ_part, σ_int, σ (Sec. 4.9) |
| M6 | Exact rational checks of F1–F3, G3–G5, G7, G9, G11 | all identities exact |
| M7 | Direct integration of discrete [L03] (2.2) (LSODA, rtol 1e−10, atol 1e−13) with constant, additive and product kernels | first-moment conservation and its failure at gelation |
| M8 | JSON-level re-application of F2 to the frozen artifact | 84 populations |

The auditor's scripts, outputs and run logs are kept in the session
scratchpad and listed with their SHA-256 in the inventory. They are not
committed: this audit's writable scope is limited to the two named files.

## 4. Audit of F (volume-budget successor)

### 4.1 Derivation of F1–F3 — correct

- **Accounting.** Take domain mass 1, wall density ρ_w, void density
  xρ_w. Then:
  - V_w = (1−m)/ρ_w and V_A = m_A/(xρ_w);
  - V_D/(M/ρ_w) = 1−m+m/x (F1);
  - F_V(A) = (m_A/x)/(1−m+m/x) = m_A/[x(1−m)+m] (F2).
- **Properties of F2.**
  - Additive over disjoint subsets.
  - Wall plus void volume equals 1.
  - Units cancel.
  - At x = 1 it reduces to m_A.
  - As x → 0 at fixed m > 0 it tends to m_A/m and the domain volume
    diverges.
- **F3 is not additive.** F3 = m_A/[x(1−m_A)+m_A]. Its denominator is
  ≤ that of F2, so F3 ≥ F2, with equality only at m_A = m.
- **Exact rational checks (M6).** The 5/7 vs 5/9 example holds. (The
  report leaves implicit that m_total = 0.2; the test makes it explicit.)
- **The reading of F3 is right.** F3 is the void fraction of a universe in
  which the excluded void mass sits at wall density. It is never a
  cumulative of one fixed domain, under any reading of the cut.
- The size-dependent generalisation (∫dm/x) is stated correctly.

### 4.2 Meaning of x and conditions for the wall identification (FGA-F4)

- **Where x is defined.** [JLH13] (A9) and (11) define 1+Δ relative to the
  EdS background of the tophat. The frozen frame convention
  r = D_wall x^{−1/3} R_L is consistent with x relative to the wall
  density only under these conditions:
  1. the C1 clock with A5 (common bang time);
  2. walls are exactly the unperturbed flat EdS background;
  3. each void is an isolated, uncompensated tophat in wall material
     (Birkhoff). At f_v ≈ 0.75 most void boundaries face other voids, so
     this is strained;
  4. the Lagrangian mean density equals the early wall density;
  5. all non-void mass (mass whose walk first crossed δ_c, at some scale)
     sits at ρ_w.
- **What the successor says.** It flags the identification as an inherited
  M3 assumption but does not list these conditions. Under C2/C3 the EdS
  barrier is not exact (frozen 1G-F Sec. 12).
- **Excursion-set reading.** Every void identified at an epoch is exactly at
  its first barrier crossing. A size-independent x is therefore implied by
  the excursion-set + tophat model, not an extra assumption.

### 4.3 M3 versus the [JLH13] Vdn model — correctly distinguished

- The models differ.
  - Vdn ((15)–(17)) conserves the linear-theory volume fraction
    (f_v = m ≤ 0.383).
  - M3 adds void volume, with the domain expanding by Z = 2.4877.
  - SvdW number conservation ((12), (14)) gives m/x = 1.87, which exceeds
    1.
- The successor does not identify M3 with Vdn. [JLH13] (13) supplies only
  the additive definition of a cumulative volume. The normalisation Z is a
  project deduction (see FGA-D5 for one docstring that overstates this).

### 4.4 The 84 archived populations — corrected exactly

- **Recomputation (M8).** F2 was recomputed from each population's own m,
  x and Lagrangian fractions.
  - The successor archive matches at relative difference 0.0 for all 84
    (42 per case). The input hash is `4523ef03…`.
  - Legacy F3 values equal the frozen M3 numbers.
  - In every population: F2 ≤ F3; the sequences are monotone; selected
    masses lie in [0, m].
  - Clocks, barriers, densities and C3 normalisations are preserved.
- **Gaps.** The adapter recomputes no r_min. The frozen F3-based r_min
  values of non-primary populations therefore remain truncated-universe
  values (FGA-F1).
- **A rounding artefact (FGA-F6).** Twelve archived populations have
  `unresolved_below_grid` < 0 (minimum −1.72e−7): trapezoid overshoot of
  the resolved mass. It is harmless here. No selection lies at the grid
  minimum, and `FixedDomainBudget` would fail closed if a selection
  exceeded m.

### 4.5 Unresolved tails, interpolation, renormalisation (FGA-F3)

- **No implicit renormalisation.**
  - F2 uses the exact m_total in its denominator. Below-grid mass
    (3.36e−9 / 4.04e−9 of the domain mass today; 0.020 / 0.013 at z = 3)
    affects only radii below the grid.
  - Medians use the exact total.
  - The variance weights are divided by the exact total; they sum to
    1 − 8.8e−9 (GM) and 1 − 1.1e−8 (NW15).
- **Discretisation bias.** The audited cumulatives use the inherited
  481-node trapezoid of dF/dln R and linear interpolation in log r. The
  closed-form M3 values show a systematic upward bias in the steep tails:

| Quantity (z = 0) | Audited GM | Independent GM | Rel. | Audited NW15 | Independent NW15 | Rel. |
|---|---:|---:|---:|---:|---:|---:|
| F2, r ≥ 1 | 0.6242648 | 0.6242902 | −4.1e−5 | 0.6660568 | 0.6660852 | −4.3e−5 |
| F2, r ≥ 5 | 0.1351057 | 0.1350904 | +1.1e−4 | 0.1658865 | 0.1658718 | +8.9e−5 |
| F2, r ≥ 10 | 0.01481496 | 0.01478039 | **+2.3e−3** | 0.01924631 | 0.01920372 | **+2.2e−3** |
| F2, r ≥ 15 | 0.001025645 | 0.001018547 | **+7.0e−3** | 0.001315045 | 0.001305280 | **+7.5e−3** |
| volume-weighted median | 2.404565 | 2.404606 | −1.7e−5 | 2.800445 | 2.800486 | −1.5e−5 |
| F2 cutoff for f_v0 | 0.3464538 | 0.3465577 | −3.0e−4 | 1.229907 | 1.230104 | −1.6e−4 |
| F3 cutoff for f_v0 | 0.505672 | 0.5057725 | −2.0e−4 | 1.951538 | 1.951735 | −1.0e−4 |

- The headline "1.48% / 1.92%" holds at three significant figures.
- "Interpret the conditional model at about three significant figures"
  (successor l. 78–79) fails for the r ≥ 15 entries: 0.00103 vs 0.00102,
  and 0.00132 vs 0.00131.
- At z = 3 the r ≥ 1 entries are biased by +6e−4 / +1.1e−3. All cutoffs
  agree to ≤ 3e−4 at every epoch.

### 4.6 Selecting a subpopulation vs reproducing the total; fixed cutoffs (FGA-F5)

- **Selection vs prediction.** The successor states correctly that matching
  a selected radius range to the tracker's f_v predicts nothing about the
  full fraction: the smaller voids remain in the F2 domain.
- **The all-size history is constant.** F2 at all sizes equals 0.751969 at
  every redshift (verified in the evidence).
- **Fixed cutoffs.** Holding the z = 0 F2 cutoff fixed (M1–M3):

| z | GM tracker f_v | GM F2 at 0.3466 h⁻¹ Mpc | NW15 tracker f_v | NW15 F2 at 1.2301 h⁻¹ Mpc |
|---:|---:|---:|---:|---:|
| 0 | 0.737 | 0.737 | 0.627 | 0.627 |
| 0.5 | 0.630 | 0.640 (+1.5%) | 0.496 | 0.382 (−23%) |
| 1 | 0.540 | 0.480 (−11%) | 0.397 | 0.186 |
| 2 | 0.401 | 0.198 | 0.267 | 0.026 |
| 3 | 0.306 | 0.060 | 0.191 | 0.0019 |

- The conclusion holds: no fixed cutoff reproduces f_v(t) over z = 0–3,
  under either meaning.
- **Where it fails.** For [GM] a fixed cutoff is within 1.5% up to z = 0.5
  and fails from z ≈ 1. The GM cutoff sequence is non-monotone (0.346,
  0.369, 0.260, 0.124, 0.061 h⁻¹ Mpc).
- **The test.** It checks only z = 0 against z = 3, a ratio > 1.5.
- README's "No fixed cutoff matches the tracker history" needs "in this
  conditional model".

### 4.7 Recomputed primary results — reproduced

| Quantity | Audited | Independent |
|---|---|---|
| m = 1 − 𝒟 | 0.3829709426561785 | 0.3829709426692 (from the M4 root; 3e−11) |
| x = 1 + Δ_sc | 0.20472233400490963 | 0.2047223340162 (M4) |
| δ_v | −2.7171803438378705 | −2.7171803436881 (M4) |
| Z (F1) | 2.487713780228009 | 2.4877137801755 |
| full void volume (F2 at all sizes) | 0.7519694338440862 | 0.7519694338440863 |
| F2 ≥ 10 h⁻¹ Mpc (GM / NW15) | 0.014815 / 0.019246 | 0.014780 / 0.019204 |
| median (GM / NW15), h⁻¹ Mpc | 2.40456 / 2.80045 | 2.40461 / 2.80049 |

The successor artifact regenerated on Windows matches the inventory's
primary values to ≤ 5e−13 (relative). The 3.14 and 3.11 outputs are
identical apart from the environment block.

### 4.8 C3 sensitivities — correctly identified as historical

- **The numbers.** The frozen C3 tracker-seed clock gives D(t0) =
  1.020230 / 1.033503, i.e. X = 1.29502 / 1.31186 (wall-mode amplitude).
  The owner-decision artifact gives 1.26264 / 1.28498 (total δ_L,
  GD-OD6), as the successor states.
- **The labelling.**
  - Successor Sec. 5, the inventory (`C3_sensitivity`) and CLAUDE.md mark
    the frozen C3 tables as historical.
  - The corrected archive keeps the old clocks, with the method string
    saying so.
  - The archive has no per-entry flag. This is optional, and part of
    FGA-F1.

### 4.9 The primary variance and what σ ≈ 0.99 establishes (FGA-F2)

- **Inputs are unchanged by F2.** The frozen calculation takes:
  - the size shape from dF/dln R divided by the exact total;
  - the covered fraction = the tracker's f_v0;
  - δ_v = −1;
  - the wall field at growth and compression D_wall.

  No radius-cut cumulative enters, and F2 = F3 at all sizes.
- **Independent recomputation (M5):**

| | σ_part | σ_int | σ | wall share σ²_int/σ² |
|---|---:|---:|---:|---:|
| GM audited (frozen artifact) | 0.3263653 | 0.9315591 | 0.9870747 | 0.890678 |
| GM independent | 0.3263657 | 0.9315592 | 0.9870750 | 0.890678 |
| NW15 audited | 0.3036278 | 0.9403317 | 0.9881365 | 0.905583 |
| NW15 independent | 0.3036282 | 0.9403318 | 0.9881367 | 0.905583 |

  The declared 89.1% / 90.6% wall contribution is confirmed. The linear wall
  field enters at σ_int ≈ 0.93, an order-unity extrapolation, as stated.
- **The hybrid ingredients.** The successor lists finite-density sizes
  (x = 0.2047), a void contrast set to −1, the supplied f_v0, missing
  evolution, and the wall share. One more ingredient is not stated:
  - Boolean grains at coverage f have grain-volume density −ln(1−f):
    1.3356 (GM) and 0.9862 (NW15).
  - That is 1.78× and 1.31× the excursion-set void volume 0.75197 (F2,
    all sizes).
  - A covered point lies on average inside 1.81 (GM) / 1.57 (NW15) grains.
  - So the variance's void phase is neither the disjoint F population
    (under any normalisation) nor an F2 subset. It is an overlapping
    surrogate that shares only the grain-size shape. F1–F3, which assume
    disjoint volumes, do not apply to it.
- **The mass bookkeeping also differs.**
  - The variance's walls hold all the mass at ρ̄/f_w (3.80 ρ̄ for GM).
  - M3's walls hold 61.7% of the mass at 2.49 ρ̄.
  - G Sec. 5 (G7–G8) quantifies this gap correctly.

### 4.10 Completeness of the supersession (FGA-F1)

The successor corrects the ≥10 h⁻¹ Mpc fill, the r_min for f_v0 and the
cutoff history. It does not map several frozen 1G-F statements that used F3
as a fixed-domain cumulative:

| Frozen 1G-F text | Frozen (F3) | Current F2 reading (auditor, M1–M3) |
|---|---|---|
| Sec. 1 item 4 and token proposal Sec. 13: "voids larger than 0.5 ([GM]) or 2.0 ([NW15])", "down to 0.5–2 h⁻¹ Mpc" | 0.51 / 1.95 | 0.35 / 1.23 (successor table) |
| Sec. 1 item 5, Sec. 8.2: near-empty C1 voids reproduce f_v0 "down to 0.06–0.8 h⁻¹ Mpc" | x = 0.1: 0.19 / 0.81; x = 0.05: 0.06 / 0.29 | x = 0.1: **0.094 / 0.39**; x = 0.05: **0.019 / 0.095** |
| Sec. 8.2: C1 near-empty r ≥ 1 | 0.519 / 0.155 (GM) | 0.304 / 0.045 |
| Sec. 1 item 6, Sec. 9: "≥ 1 h⁻¹ Mpc … gives 0.013 at z = 3"; Sec. 9 column "M3, r ≥ 1" | GM 0.695, 0.559, 0.383, 0.102, 0.013; NW15 0.715, 0.588, 0.403, 0.099, 0.011 | GM 0.624, 0.404, 0.221, 0.0445, 0.0052; NW15 0.666, 0.444, 0.239, 0.0433, 0.0044 |
| Sec. 8.2 all "r ≥ …" and "r_min" columns for C2, C3 and near-empty | F3 values | not recomputed (adapter covers r ≥ 1…15 only) |
| Sec. 1 item 2 and Sec. 5 "the same objects at different stages", `DERIVED_FROM_VERIFIED_DEFINITIONS` | identification asserted | successor Sec. 4 says the Milne asymptote "does not identify" seeds with exactly empty tracker voids. The verdict's status is changed without being named |

The successor is the declared current reading (CLAUDE.md, "Reports and
inventories older than a successor erratum…"). Without this mapping, the
superseded near-empty r_min values and frozen verdict 2 read as current.

## 5. Audit of G (void-evolution research)

### 5.1 Equation by equation

| Eq. | Content | Class | Independent check | Result |
|---|---|---|---|---|
| G1 | Smoluchowski equation with reduced-volume label q and source S | imported model ([L03] (2.2), mean field) plus model assumption | dimensions: [K] = V_ref/time, u dimensionless | correct; hypotheses incomplete (FGA-G2) |
| G2 | Q̇₁\|_K = 0 for additive mergers | identity under the stated conditions | symmetrisation; M7: constant and additive kernels conserve Q₁; **product kernel loses 50% of the sol moment at t = 2 t_gel** (Flory 1/t) | correct; the stated no-gel condition is necessary |
| G3 | ḟ = 3f(1−f)(H_v−H_w) | identity (common g_v, J = 0) | exact rationals | correct |
| G4 | Milne/EdS volumes give t/(t+τ) | conditional deduction with supplied f_ref | exact rationals; [GM] (5.1), (5.5), (5.6) imply a_v ∝ t, a_w ∝ t^{2/3} | correct; reproduces [GM] (5.6) |
| G5 | with volume transfer J | identity | numeric, residual 6e−17 | correct |
| G6 | J = 0 shell-crossing rate is 2/3 of the tracker's; J_req/V = f(1−f)/(3t) | conditional deduction ([JLH13] (A4)–(A5), (A8); A5 clock) | M4: H_v t = 0.8888888890 from Lagrangian shells; 0.0646103 / 0.0779570 | correct; scope (FGA-G1) |
| G7 | m = fx/(1−f+fx), the inverse, δ_v^global | identity | exact | correct; 0.364551 / 0.256025 |
| G8 | Φ = −M_D dm/dt | identity (definition) | — | correct; distinct from J |
| G9 | x(t) = (m/(1−m)) τ/t | conditional deduction | exact | correct; x ≤ 1 needs t ≥ τm/(1−m) |
| G10 | constant-kernel solution with exposure u | imported ([L03] (4.10), K = 1 → u = t/2) and rescaled | kinetic integration | correct |
| G11 | volume tail β^{k−1}[1+(k−1)(1−β)] | identity | exact Fractions to k = 900 plus exact remainder; table 2.96e−36, 9.04e−5, 0.648651 | correct |
| G12 | ball variance as a double integral of ⟨δδ⟩ | standard definition (real space of [JLH13] (2)) | — | correct; missing from the closing classification (FGA-G4) |

### 5.2 Specific points

- **Measure and reference volume.**
  - n(q,t) dq is the number per fixed reference volume, and q = v/g_v is a
    reduced volume.
  - A physical-density kernel needs the dilution factor, as stated.
  - The common g_v (Sec. 2) is what makes V_v ∝ g_v Q₁. With size- or
    age-dependent H_v, mergers redistribute volume among rate classes and
    *can* change the total history (FGA-G3).
- **J versus Φ.** J (volume, walls → voids) and Φ (mass, voids → walls)
  are kept apart correctly. A non-additive merger (v + v′ + ε) is
  correctly identified as a volume source.
- **The 2/3 factor.**
  - 3(8/9 − 2/3) = 2/3 relative to the tracker's 3(1 − 2/3) = 1.
  - J_req = f(1−f)/(3t).
  - The time variable is the tophat's own EdS age. Its identification with
    the wall age t is A5, stated in Sec. 2.
- **Synchronous vs aged cohorts (FGA-G1).**
  - A homogeneous open interior after shell crossing has H_v t rising
    monotonically to 1: 0.9095 at 1.5 t_sc, 0.9227 at 2 t_sc, 0.9727 at
    10 t_sc.
  - The near-empty barriers give 0.934 (x = 0.1) and 0.961 (x = 0.05).
  - So J_req/(tracker rate) = 3(1 − H_v t) lies in (0, 1/3]. **G6 is the
    upper bound** for such cohorts, not a population value.
  - The F excursion-set all-size bookkeeping has ḟ = 0. In G5 terms that is
    H_v,eff = H_w, or t J/V_D = −0.124 relative to shell-crossing
    interiors. F's own "history" is re-identification at fixed x, not the
    J = 0 evolution of any cohort.
- **Interior vs boundary.** Sec. 4 states correctly that a homogeneous
  open-FLRW interior continued past shell crossing does not derive the
  ridge/boundary dynamics.
- **Mass, volume and the vacuum limit (G7–G9).**
  - Correct.
  - The exact Milne a ∝ t solution of dust FLRW is vacuum (ä = 0 ⇒ ρ = 0).
  - A finite-mass seed cannot silently become an exactly empty region at
    finite time.
  - These are deductions within regional dust FLRW, as stated.
- **The benchmark.**
  - The factor 1/2 in u and the moments N₀/(1+u) and N₀q₀ are correct.
  - The table values are reproduced.
  - At u = 100 three radius measures differ by 33%: radius at the mean
    volume 4.66, number-mean radius 4.17, volume-weighted median 5.53 seed
    radii. This supports the report's distinction among them.
  - The constant kernel is labelled everywhere as a benchmark
    (`EXTERNAL_BENCHMARK_NOT_A_TIMESCAPE_CLOSURE`), and is nowhere
    promoted to a physical law or applied to the F population.
- **Correlations.** The G report says correctly that n(q,t) does not fix
  the wall-indicator covariance, and that keeping the Boolean model at
  every epoch is a new spatial closure.
- **Conditional vs general.** Sec. 1 ("not a general no-go"), Sec. 5 and
  Sec. 7 keep the statements conditional. The only over-general phrasing
  is Sec. 1 item 1 and the CLAUDE.md G line ("at prescribed regional
  rates"), which hold only for a common rate (FGA-G3).

## 6. Numerical validation

### 6.1 Historical claims (validation record) — not re-verifiable here

The record reports runs in a Linux snapshot without Git history, on CPython
3.12.14, NumPy 2.3.5, SciPy 1.17.0 and pytest 9.1.1:

- a full suite with 31 new tests: 1089 passed, 34 skipped, 1 failed
  (the Git-history test), 220.20 s;
- 32 targeted tests passed, 5.30 s;
- the F and G evidence completed.

No logs of these runs exist in the checkout. They are recorded here as
claims. The record correctly says that the two-interpreter gates were not
certified.

### 6.2 This audit's runs

All runs use `python -B -W error -m pytest -W error -p no:cacheprovider`
and `OPENBLAS_NUM_THREADS=1`, in the real checkout.

| Run | 3.14.3 | 3.11.9 |
|---|---|---|
| F and G modules (32 tests) | 32 passed, 14.5 s | 32 passed, 13.7 s |
| Full suite | **1125 passed, 0 skipped, 0 failed**, 606 s | **1125 passed, 0 skipped, 0 failed**, 546 s |
| `test_gb_od3_the_frozen_inventory_is_pinned_to_its_certified_blob` alone | passed, unmodified | (in full suite) |
| F successor script `--frozen-artifact`, isolated copy | exit 0, 15 s | exit 0, 14 s |
| G script, isolated copy | exit 0 | exit 0, byte-identical to 3.14 |

- **Counts.** 1125 = 1093 + 32. Nothing is skipped because the oracle and
  generated artifacts are present in this checkout.
- **The historical blob.** It is `745b5b9acce2a7de71d950c7d00a4387fd0d7df2`
  at `118b8f3`, and equal to HEAD and to the working file.
- **Artifacts.** The 366-file checksum list is identical before and after
  all runs.
- **Evidence comparison.**
  - F: equal to the inventory to ≤ 5e−13.
  - G: equal to the inventory to ≤ 1.2e−15. The Windows shell-crossing root
    differs in the last ulp.
  - The recorded `evidence_sha256` values cannot be reproduced on Windows
    (FGA-D3).
- **Test independence (FGA-T1).**
  - Independent:
    - the physical-volume additivity test;
    - the [JLH13] printed digits;
    - the kinetic integration;
    - the ODE test.
  - Self-referential:
    - the `r>=10` regression at `rel=2e-7` pins the implementation's own
      output, which carries the +0.23% bias of Sec. 4.5;
    - `H_v_times_t == 8/9` is the brentq target, a tautology.

## 7. Documentation and provenance

### 7.1 CLAUDE.md

| Lines | Change | Assessment |
|---|---|---|
| 12 | "never push or publish anything" → "…without explicit human approval" | now equals AGENTS.md rule 7. Acceptable; owner awareness (FGA-D6) |
| 16, 100–104 | phase range; firewall paragraph for report-evidence scripts | correct and restrictive |
| 249–255 | σ track: main at fb5d952, 1G-A…E v1 tags, no 1G-F tag | verified locally and on the remote (read-only) |
| 279–280 | validation note | correct |
| 346–352 | 1G-D: "R8 < R_void … does not transfer … not a theorem…" | **governance issue, FGA-D1** |
| 371–395 | 1G-F | numbers verified; "empty Boolean voids" understates FGA-F2 |
| 396–409 | 1G-G | correct; one over-general phrase (FGA-G3) |
| 142–145 | suite counts (1049 / 1093) | not updated; now 1125 (FGA-D6) |

### 7.2 README.md

- The status heading and the merge/tag statement are verified.
- The 1G-D bullet (l. 50–53) has the same issue as FGA-D1.
- The F and G bullets are verified, with the FGA-F2 and FGA-F5 nuances.

### 7.3 Validation record and inventories

- **Verified in the real checkout:**
  - 259 tracked files, of which exactly 2 are modified;
  - the blob identity;
  - the five tag-object SHA-256 values and their targets;
  - the 32 targeted tests.
- **Inventories.** `frozen_sha256` entries match. `independent_audit:
  NOT_PERFORMED` is now superseded by this report.
- **Authorisation.** It is recorded as a paraphrase (FGA-D2).

## 8. Findings register

Severity: **HIGH**, an implemented equation or headline value is wrong or a
firewall is crossed; **MEDIUM**, a reading, supersession or governance step
is missing or misleading; **LOW**, local imprecision, clarity,
reproducibility or attribution; **INFO**, no change required.

Class: `ERROR` (an actual error), `OMISSION` (a missing assumption or
supersession), `GOVERNANCE`, `OPTIONAL`.

### FGA-F1 — MEDIUM, OMISSION — blocks integration
- **Where.** `phase1g_f_volume_budget_successor.md` Secs. 2–5, which have
  no mapping table. Frozen `phase1g_f_void_population.md`:
  - Sec. 1 items 2, 4–6;
  - Sec. 5, the Milne limit;
  - Sec. 8.2 tables;
  - Sec. 9 r ≥ 1 column;
  - Sec. 12 item 1;
  - "Reading";
  - Sec. 13 token wording.
- **Contested.** The successor is declared the current reading, but several
  frozen F3-based numbers and frozen verdict 2 are neither corrected nor
  marked superseded.
- **Evidence.** Sec. 4.10 table:
  - near-empty r_min 0.06–0.8 → 0.019–0.39 h⁻¹ Mpc;
  - z = 3 r ≥ 1: 0.013 → 0.0052;
  - token wording "0.5–2" → 0.35–1.23;
  - verdict 2 (`DERIVED_FROM_VERIFIED_DEFINITIONS`) is contradicted by
    successor Sec. 4 without being named.
- **Impact.** Superseded numbers read as current. The status label of a
  frozen verdict changes silently.
- **Minimal correction.**
  - Add a "frozen text → current reading" table.
  - Recompute F2 r_min for the archived C1 near-empty populations, or flag
    every frozen r_min column as truncated-universe (F3) only.
  - State the current label of frozen verdict 2. For example, the
    Milne-rate asymptote is `DERIVED_FROM_VERIFIED_DEFINITIONS`; its
    identification with exactly empty tracker voids is not derived (G8).
- **Owner decision.** Confirm the new label for frozen verdict 2.

### FGA-F2 — MEDIUM, OMISSION — required before freeze
- **Where.** Successor Sec. 4 (l. 116–141); CLAUDE.md l. 388–392; README
  l. 66–69.
- **Contested.** "The primary … variance uses the full population's size
  shape … and empty Boolean voids." The list of hybrid ingredients omits
  that the Boolean void phase is not the F population.
- **Evidence.** Sec. 4.9:
  - grain-volume density −ln(1−f_v0) = 1.336 / 0.986, i.e. 1.78× / 1.31×
    the excursion-set volume 0.752;
  - mean multiplicity 1.81 / 1.57 at covered points;
  - overlapping grains, whereas F1–F3 assume disjoint volumes.
- **Impact.** σ ≈ 0.99 (reproduced exactly) is the variance of a surrogate
  sharing the grain-size shape. Under no normalisation is it the variance
  of the derived population.
- **Minimal correction.** Add this as a fifth hybrid ingredient. Write
  "overlapping Boolean grains with the F grain-size shape at intensity
  −ln(1−f_v0)" in CLAUDE.md and README.
- **Owner decision.** None. The E1–E4 token assumptions are unchanged.

### FGA-F3 — LOW, ERROR (precision claim) — required before freeze
- **Where.** Successor l. 69–79; inventory `primary_cases`;
  `precision` string in the script (l. 199).
- **Contested.** "Interpret … at about three significant figures."
- **Evidence.** Sec. 4.5: the inherited 481-node trapezoid and log-linear
  interpolation bias the tails by +0.23% (≥10) and +0.70–0.75% (≥15). The
  r ≥ 15 entries differ in the third significant figure.
- **Impact.** Small. The headline 1.48% / 1.92% and all cutoffs are
  unaffected at three significant figures.
- **Minimal correction.** Quantify the discretisation error and quote
  r ≥ 15 at two significant figures. Alternatively, evaluate cumulatives
  from the closed-form absorption probability (M3).
- **Owner decision.** None.

### FGA-F4 — LOW, OMISSION — required before freeze
- **Where.** Successor l. 51–56.
- **Contested.** The wall identification of x is called an inherited M3
  assumption, but its conditions are not listed.
- **Evidence.** Sec. 4.2, conditions 1–5. Condition 3 (isolated voids
  embedded in walls) is strained at f_v ≈ 0.75. Condition 5 assigns
  δ_c-crossing mass to ρ_w.
- **Minimal correction.** List the five conditions.
- **Owner decision.** None.

### FGA-F5 — INFO, OPTIONAL
- **Where.** Successor Sec. 3; test l. 84–86; README l. 66.
- **Evidence.** Sec. 4.6. For GM a fixed cutoff holds within 1.5% to
  z = 0.5 and fails from z ≈ 1. The cutoff sequence is non-monotone. The
  test compares only z = 0 with z = 3.
- **Suggestion.** State the epoch range of the failure, and qualify the
  README sentence as conditional.

### FGA-F6 — INFO
- **Where.** Frozen artifact, 12 populations.
- **Evidence.** `unresolved_below_grid` < 0, down to −1.72e−7, from
  trapezoid overshoot. No effect on F2.
- **Suggestion.** One sentence in the successor.

### FGA-G1 — LOW, OMISSION — required before freeze
- **Where.** `phase1g_g_void_evolution.md` Sec. 1 item 2 and Sec. 4
  (l. 107–127); CLAUDE.md l. 399–401.
- **Contested.** The reader is not told that the 2/3 rate refers to a
  synchronous cohort followed through its homogeneous interior at the
  instant of shell crossing.
- **Evidence.** Sec. 5.2:
  - aged cohorts have H_v t ∈ (8/9, 1), so G6 is an upper bound on J_req;
  - F's own all-size history has ḟ = 0, i.e. t J/V_D = −0.124 relative to
    shell-crossing interiors.
- **Impact.** The 2/3 rate could be read as the evolution of the F
  population, which it is not.
- **Minimal correction.** Two sentences in Sec. 4.
- **Owner decision.** None.

### FGA-G2 — LOW, OMISSION — required before freeze
- **Where.** G report Secs. 2–3 (l. 54–62); inventory `assumptions`.
- **Contested.** G1 is described only as "an additional model assumption".
- **Evidence.** [L03]'s text below (2.2) states two hypotheses: no spatial
  correlations between clusters, and averaged morphology. Voids at
  f_v ≈ 0.6–0.75 are space-filling, and their mergers are neighbour
  events.
- **Minimal correction.** Transcribe both hypotheses into the assumptions
  list.
- **Owner decision.** None.

### FGA-G3 — LOW, ERROR (scope of a statement) — required before freeze
- **Where.** G report Sec. 1 item 1 (l. 15–17); CLAUDE.md l. 397–398.
- **Contested.** Additive mergers "cannot independently fix a wrong
  total-volume history when the regional expansion laws are prescribed".
- **Evidence.** The statement is true only for a common, size- and
  age-independent g_v, which Sec. 2 assumes. With prescribed but
  size-dependent rates, mergers change the volume-weighted H_v and hence
  the history. Sec. 2 hints at this ("volume-weighted rates") but does not
  restrict the headline.
- **Minimal correction.** Write "at a prescribed common regional rate".
- **Owner decision.** None.

### FGA-G4 — INFO
- **Observations.**
  - The closing classification sentence of the G report (l. 274–276)
    omits G12, a standard definition.
  - The radius-measure numbers of Sec. 5.2 could be added to Sec. 6.

### FGA-T1 — LOW, OPTIONAL
- **Where.** `tests/test_phase1g_f_volume_budget_successor.py` l. 75–79;
  `tests/test_phase1g_g_void_evolution.py` l. 92.
- **Contested.** These are self-referential checks (Sec. 6.2).
- **Suggestion.** Add two independent tests:
  - a closed-form-cumulative check of r ≥ 10;
  - a derivation of (A8) as a shell-crossing criterion (∂r/∂R_i = 0 from
    Lagrangian shells, M4).

### FGA-D1 — MEDIUM, GOVERNANCE — blocks integration; owner decision required
- **Where.**
  - CLAUDE.md l. 346–352;
  - README l. 50–53;
  - successor Sec. 5 (l. 152–157);
  - unchanged by the deliverables: `src/timescape_fsigma8/scientific_status.py`
    l. 84–95 and `phase1g_d_owner_decisions_successor.md` l. 47, 141,
    251.
- **Contested.** The approved D successor supports
  `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC = NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY`
  on "R8 < R_void (the dominant voids are 30 h⁻¹ Mpc across)", independent
  of the seed. The live token comment says the statistic "is not defined".
  The new CLAUDE.md and README text removes that reading: "not a theorem
  excluding any linearly extrapolated statistic". No dated owner decision
  or D successor records the change.
- **Evidence.**
  - Scientifically, the auditor agrees the R8 < R_void premise fails for
    the F population: median 2.4–2.8 < 8 h⁻¹ Mpc, and
    σ²_part = 0.107 / 0.092 ≪ f_v/f_w.
  - The remaining support is A_v σ_LSS(R8) = 1.05–1.11, at the edge of the
    non-perturbative regime.
  - The new reading is therefore better supported, but it changes the
    documented meaning of an owner-approved token. CLAUDE.md says
    "do not relabel, weaken…".
- **Impact.** CLAUDE.md, README, the D successor and the token comment
  become mutually inconsistent.
- **Owner decision**, one of:
  - (a) keep the value and re-justify the comment by the PBS amplitude only,
    in a dated D successor;
  - (b) propose a reclassified value through the registered-successor
    mechanism;
  - (c) revert the CLAUDE.md and README wording pending a decision.

### FGA-D2 — LOW, GOVERNANCE/PROVENANCE — required before freeze
- **Where.** Successor l. 4–5; G l. 4; both inventories `authorization`;
  validation record "Scope".
- **Contested.** The authorisation for a scientific reinterpretation
  (AGENTS.md rules 1 and 3) is recorded only as a paraphrase. It does not
  list what "the proposed rectification" covered: for instance, the D
  wording (FGA-D1) or the change to CLAUDE.md's summary of AGENTS.md
  rule 7.
- **Minimal correction.** Quote the owner instruction verbatim with its
  date, and list the items covered.

### FGA-D3 — LOW, REPRODUCIBILITY — required before freeze
- **Where.** Both scripts' `write_text(…, encoding="utf-8")` (F l. 212,
  G l. 161); inventories `evidence_sha256`.
- **Contested.** The evidence hashes are not reproducible across
  platforms.
- **Evidence.**
  - The text-mode writes give CRLF on Windows (2370 / 138 CR bytes).
  - F embeds an environment block.
  - G differs only in the last ulp (≤ 1.2e−15).
  - The Windows reruns are deterministic (3.14: `2f8931a5…`; G identical
    across interpreters), yet ≠ the recorded `fc2524d3…` and `05a0d505…`.
- **Minimal correction.**
  - Write LF bytes.
  - Hash canonical content excluding `environment`, or record a
    numerical-equivalence tolerance instead of a byte hash.

### FGA-D4 — LOW, OPTIONAL
- The reproduction commands are POSIX-only (`PYTHONPATH=src … python`).
  The primary machine is Windows; both scripts run there unchanged.
- Suggestion: add the `.venv\Scripts\python` forms.

### FGA-D5 — LOW, ERROR (attribution) — required before freeze
- **Where.** F script l. 36–37 ("Eq. F1 derives from [JLH13] (13) and
  V = M/rho"); G script l. 59 ("inverse of successor F1-F2 ([JLH13]
  (13))").
- **Contested.** [JLH13] (13) gives only the additive definition, relative
  to the background volume. The domain normalisation Z = 1−m+m/x is a
  project deduction; [JLH13]'s own number-conserving case gives m/x, their
  (14).
- **Minimal correction.** Reword both docstrings as in successor Sec. 1.

### FGA-D6 — INFO
- **Superseded by this audit.** The validation record's limitation "only
  one Python version" and its 1089 / 34 / 1 result: both interpreters now
  give 1125 / 0 / 0 here.
- **Not updated.** CLAUDE.md's suite counts.
- **For owner awareness.** CLAUDE.md's summary of AGENTS.md rule 7 now
  matches rule 7 itself, which the AGENTS.md text governs. Update the counts
  and the record's limitation in the integration commit.

### FGA-D7 — INFO (pre-existing, outside the audited changes)
- **A token comment.** The live comment of
  `TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC` states E2 as "Boolean Poisson balls
  of one radius". The reference value σ ≈ 0.99 adopted under GE-OD2 is the
  polydisperse generalisation.
- **A citation.** The frozen 1G-F cites [SvdW04] (A15) for g(Θ); the
  reconstruction gives (A17).

## 9. What blocks integration and what remains before freeze

**Blocking integration into `main`:**
1. FGA-D1: an owner decision on the 1G-D token reading, plus a consistent
   comment and successor record.
2. FGA-F1: the supersession table. This includes the r_min of the
   near-empty and archived populations, and the label of frozen verdict 2.

**Required before a phase freeze/tag:** FGA-F2, F3, F4, G1, G2, G3, D2, D3,
D5.

**Optional:** FGA-F5, F6, G4, T1, D4, D6, D7.

**Remaining checks before freezing:**
1. Apply the corrections on the phase branch, then rerun the F and G modules
   and both full suites on the final tree. This audit certifies only the
   file hashes in Sec. 1.
2. Regenerate the evidence with LF writes and record the hashes or
   tolerances (FGA-D3).
3. Record the actual commit. Update CLAUDE.md's suite counts and the
   validation record.
4. Run an independent check of any newly recomputed r_min (FGA-F1).
5. Tag and publish only with explicit owner approval for each action
   (AGENTS.md rule 7).

## 10. Status statement

This audit adds no package code, no status token and no tolerance. The F
and G results remain conditional, model-internal research evidence:

- σ ≈ 0.99 is a conditional hybrid variance, not an observational σ8;
- the constant kernel is a benchmark;
- the missing closures stay external inputs: formation and ages, kernel and
  boundary rule, regional dynamics and clock embedding, mass and volume
  transport, spatial correlations, and the dressed map.

`SIGMA8_AUTHORIZATION` stays `NOT_GRANTED`.

## References

- [JLH13] Jennings, Li & Hu, MNRAS 434, 2167 (2013), arXiv:1304.6087,
  `voids_mnras.tex` SHA-256 `cf6fc77a…7c4e`.
- [SvdW04] Sheth & van de Weygaert, MNRAS 350, 517 (2004),
  astro-ph/0311260, `voids.tex` SHA-256 `e66ad192…84b5`.
- [L03] F. Leyvraz, Phys. Rep. 383 (2003), cond-mat/0305670,
  `physrep1.tex` `50ed4dcf…`, `physrep3.tex` `99ee8599…`.
- [GM] Galoppo & Mourier, JCAP 02 (2026) 066, arXiv:2511.17160v2,
  `main.tex` SHA-256 `f9cadfa0…7b59`.
- Project records: the frozen `phase1g_f_void_population.md` and the
  1G-C/D/E owner-decision successors.
