# Phase 1G-C — Independent adversarial audit

Audit classification: `INDEPENDENT_ADVERSARIAL_AUDIT`.
Checkpoint audited: `6f7937ce5681900898f5e0a6482a953f0fa3e5a0` (`6f7937c`).
Date: 2026-09-29.
Machine-readable companion:
[`phase1g_c_adversarial_audit_inventory.json`](phase1g_c_adversarial_audit_inventory.json).

Audited phase: Phase 1G-C, two-scale linear growth law
([`phase1g_c_two_scale_growth_law.md`](phase1g_c_two_scale_growth_law.md),
cited here as [1G-C]).

## 1. Verdict summary

```text
VERDICT:       ACCEPT_WITH_CORRECTIONS
TAG_READINESS: NOT_READY_OWNER_DECISION_REQUIRED
FINDINGS:      9  (HIGH 0, MEDIUM-HIGH 1, MEDIUM 2, LOW-MEDIUM 1, LOW 5)
```

- **The mathematics and the numbers hold.** I re-derived everything from
  the printed [GM] equations with my own code, not from the package's
  closed forms. These all hold:
  - the two-region kinematics;
  - the regional Friedmann, Raychaudhuri and mass-budget identities;
  - the wall law `Δ_w ∝ t^{2/3}`;
  - the photon-normalised factor `γ_w0(1−f_v0)^{1/3}`;
  - `X_wall`, every σ value in Sec. 7 and every power step in Sec. 8;
  - the wall-clock residual `γ_w0² − 1`.

  Every printed digit is reproduced. The phase script reproduces its artifact
  byte for byte (Python 3.13) and gives bit-identical numbers on Python 3.11.
- **The interpretation over-reaches in one material respect (GC-F1).** The
  report calls 0.834/0.935 the "mass-weighted σ(M8)". It says this supersedes
  1G-A for σ8-scale statistics, and that the open problem is "settled". Its
  own sources do not support this:
  - [W09] places sub-cell scales in the nonlinear regime (lines 383–386, and
    footnote foot11, lines 2648–2651). The report quotes line 383–386 without
    its words "which characterize the nonlinear regime".
  - Voids fill f_v0 = 0.74 of the volume. The dominant ones are 30 h⁻¹ Mpc
    across ([W09] lines 277–278), wider than the 16 h⁻¹ Mpc σ8 sphere.

  What the derivation supports is the *linear wall-internal* statistic,
  measured relative to the wall mean. Live records already narrow the token
  this way (via 1G-D §9). The 1G-C text itself, CLAUDE.md, README and the
  successor record's superseded-readings table do not fully say so (GC-F4).
- **Two classifications are too strong, or rest on unstated assumptions.**
  - GC-F2: the "exact two FLRW regions" structure is labelled
    `DERIVED_FROM_VERIFIED_DEFINITIONS`. Its dynamical content (`ρ_v = 0`,
    EdS walls) needs the regional dust-FLRW equations in the common time t.
    The live `REGIONAL_DUST_FLRW_EQUATIONS` token classifies these as
    `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`.
  - GC-F3: the common-time law takes t to be the proper time of the wall
    matter. [W07] and [W09] give the wall geometry and the sub-cell flow in
    wall proper time. This identification is not among A1–A4.
- **All corrections are text-only.** No equation, number, status-token value,
  tolerance or code needs to change.

## 2. Scope and evidence

**Files read in the audited worktree** (`AUDIT_TREE`, exactly `6f7937c`, with
the regenerated git-ignored artifacts copied in):

| File | SHA-256 (prefix) |
|---|---|
| `reports/phase1g_c_two_scale_growth_law.md` | `59c5e561…` |
| `reports/phase1g_c_two_scale_growth_inventory.json` | `9aec8902…` |
| `scripts/phase1g_c_two_scale_growth_numerics.py` | `b5fc40c1…` |
| `artifacts/independent/phase1g_c_two_scale_growth.json` | `bf970070…` |
| `scripts/phase1g_a_sigma8_path_numerics.py` (imported by path; context) | `65eb4235…` |
| `src/timescape_fsigma8/scientific_status.py` | `31100557…` |
| `src/timescape_fsigma8/background/{__init__,parameters,tracker,effective_fluid,observables}.py` | `e8b2ef97…`, `003fd222…`, `b7cf16a7…`, `f2ce407b…`, `67c298ef…` |

For context I also read these (conclusions not relied on):
- 1G-A §5.3 (the `a_w` notation finding);
- 1G-B §§1, 5;
- the status-additions successor record;
- 1G-D, only for its list of superseded 1G-C readings;
- the 1F-C-R remediation, for the A07 tokens;
- `CLAUDE.md` and `README.md` at the checkpoint.

**Primary sources** (LaTeX e-prints, SHA-256 checked):

| Id | File | SHA-256 |
|---|---|---|
| [GM] arXiv:2511.17160v2 | `main.tex` | `f9cadfa03ecc9a74b0a8f432ae4b13422daeb219f253756bcd877b4b75077c59` |
| [W09] arXiv:0909.0749v2 | `observe.tex` | `2b0324d127440e9a053a7cb37102d7655cca228a63cd2222843e879989b4b531` |
| [W07] arXiv:0709.0732v2 | `solution.tex` | `221662c987e454729ef8202c87fa697c5882b5b7daaecdedb50a7cba8ffe6cd8` |
| [EH98] astro-ph/9709112 | `trans.tex` | `5f2ac6b413df8b738c95f6650152b7e82d7c36f6d9b3a618da540e9739dce17f` |
| [P18] arXiv:1807.06209 | `ms.tex` | `fe0833d2d0fda17427a709c9559dc7b3a988b955f47bb7de7a02c900ffdc21cf` |

The .tex files carry no printed equation numbers. I rebuilt [GM]'s numbering
from the source: section counter, and one number per unstarred display row
without `\nonumber`. Sec. 3 = 3.x, Sec. 4 = 4.x, Sec. 5 = 5.x. Results:
- (3.8) Hamiltonian at line 377;
- (4.9)–(4.12) the dust-frame system at line 492;
- (4.27) the Mészáros equation at line 577;
- (5.1) at line 623, (5.3) at 632, (5.4) at 639, (5.5)–(5.7) at 652–660.

These agree with the numbers the report and the package cite.

**Environment.** Linux x86-64. Interpreters:
- CPython 3.13.12, NumPy 2.5.3, SciPy 1.18.1;
- CPython 3.11.15, NumPy 2.4.6, SciPy 1.17.1.

mpmath 1.3.0 and sympy 1.14.0 were installed into the scratch directory only.
The project environments were not modified.

**Runs.**
- `scripts/phase1g_c_two_scale_growth_numerics.py` in AUDIT_TREE with
  `PYTHONPATH=$AUDIT_TREE/src`, `-B -W error`, on both interpreters. All
  budgets pass.
  - 3.13: the artifact is byte-identical to the checkpoint copy
    (`bf970070…`).
  - 3.11: every result leaf is bit-identical; only the `environment` block
    differs.
  - The checkpoint artifact bytes were restored afterwards.
- My own scratch scripts (`audit_c/indep_1gc.py` and small follow-ups).
- The full test suite was not run (the lead runs it).

## 3. Method and independence statement

- I did not read any other `phase1g_*_adversarial_audit*` file or any other
  auditor's scratch directory.
- **Identities.** Every Timescape identity was evaluated at 40 significant
  digits (mpmath), from the printed [GM] definitions only:
  - (5.5), (5.6) and (5.1) with `f_v = V_v/V_D`;
  - the text p. 25 normalisations (`a_D0/a_w0 = 1+f_v0/2`, `⟨ρ⟩(t0)`,
    `γ_w = 1+f_v/2`, `1+z = γ_w a_w0/a_D`);
  - the printed (5.7) `Q_D` and the Hamiltonian constraint (3.8).

  Derivatives were taken numerically (`mp.diff`). No package closed form was
  used.
- **Package check.** Only afterwards did I compare the package's `fv`,
  `dfv_dt`, `a_D`, `H_D`, `Q_D`, `R_D`, `rho_d`, `gamma_w`, `a_w` and
  `redshift` with these values.
- **Growth.** The volume-average CGI closures ((4.21)–(4.23), (4.27)) and the
  flat-ΛCDM growth factor were integrated with my own code.
- **Early spectrum.** The EH98 zero-baryon-oscillation T(k) (Eqs. (26),
  (28)–(31), checked against `trans.tex` lines 683, 758–780, 839–842) and the
  top-hat σ integral were written from scratch.
- **Planck inputs** were checked in `ms.tex` (σ8 = 0.8111, lines 2252 and
  2452; n_s, ω_b). The rounded Ω_m = 0.315 and h = 0.674 are inherited from
  the frozen `qplus` recipe.
- **Circularity.** Where a check in the phase script re-uses the expression
  it tests, I say so (GC-F6).

## 4. Claim C1 — exact decomposition into empty Milne voids and EdS walls

**Claim** ([1G-C] §1 verdict 1, §3): "The tracker is exactly two FLRW regions
in the common time t (`DERIVED_FROM_VERIFIED_DEFINITIONS`, verified to
≤ 3e−15)". Voids: `a_v ∝ t`, `ρ_v = 0`. Walls: `a_w,reg ∝ t^{2/3}`,
`ρ_w = 1/(6πGt²)`. It also claims:
- `H_D = f_v H_v + f_w H_w`;
- `⟨ρ⟩ = f_w ρ_w`;
- `Q_D = 6 f_v f_w (H_v−H_w)²`;
- `⟨R⟩ = −6 f_v/t²`;
- `γ_w H_w = H_D`.

**Re-derivation.**
- **Kinematics.** From (5.5)–(5.6), `a_D ∝ t (f_v0/f_v)^{1/3}` and
  `f_v = t/(t+τ)`. With (5.1), `a_v³ = f_v a_D³/f_vi ∝ t³` and
  `a_w³ = (1−f_v)a_D³/f_wi ∝ t²`, so `H_v = 1/t` and `H_w = 2/(3t)`.

  This is not only "implicit": [W07] states both explicitly.
  - solution.tex lines 317–321: "`a_w = a_w0 t^{2/3}` … exactly that of an
    Einstein–de Sitter universe, *but in volume average time not locally
    measured wall time*".
  - Lines 404–406: "the void regions expand exactly as a Milne universe in
    volume–average time".
  - [W09] lines 1763–1764 repeat `a_w = a_w0 t^{2/3}`.
- **Dynamics.** The volume-level tracker cannot fix how mass and curvature
  are split between the regions. That needs three further inputs:
  - (i) each region obeys its own dust Friedmann/Raychaudhuri equations in
    the common time t with no internal backreaction. Sources: [GM] line 618,
    "Each domain is … modelled by a dust-sourced FLRW spacetime"; [W09]
    line 510, "no backreaction within walls and voids separately";
  - (ii) walls are flat ([GM] footnote, line 620);
  - (iii) the D1-corrected `⟨R⟩_D`.

  Then `R_v = ⟨R⟩_D/f_v = −6/t² = −6H_v²`. The void Hamiltonian constraint
  forces `8πGρ_v = 3H_v² + R_v/2 = 0` exactly. The void Raychaudhuri equation
  (`ä_v = 0`) and the FLRW curvature scaling (`R_v a_v² = const`) are then
  satisfied. So the void is Milne dynamically, not only kinematically.

  The non-trivial check is the mass budget. [GM]'s p. 25 normalisation of
  `⟨ρ⟩` equals `f_w · 3H_w²/(8πG)` exactly, so all matter is in EdS walls.
  - **D1 dependence.** With the printed (5.7) prefactor, the void density
    would be negative: `8πGρ_v t² = −0.677` (f_v0 = 0.737) and `−1.095`
    (0.627). The Hamiltonian constraint independently rejects the printed
    prefactor: `R_printed/R_(3.8) − 1 = f_v0^{−2/3} − 1 = 0.226` and `0.365`.

**Independent numbers** (mpmath, 40 digits, 15 epochs from 1e−7 t0 to t0,
three parameter sets):

| Identity (from printed definitions) | max abs residual |
|---|---|
| `H_v t − 1`, `H_w t − 2/3`, `H_D t − (2+f_v)/3` | ≤ 3.4e−41 |
| (5.2) `(H_D − f_vH_v − f_wH_w)/H_D` | ≤ 2.8e−41 |
| [W09] (Q1) with the printed (5.7) `Q_D` | ≤ 2.1e−40 |
| `⟨R⟩` from (3.8) vs `−6 f_v/t²` | ≤ 1.3e−34 |
| (3.9) Raychaudhuri | ≤ 3.1e−41 |
| (5.3) `γ_w H_w/H_D − 1` | ≤ 2.3e−41 |
| void `ρ_v/⟨ρ⟩`; `R_v/(−6H_v²) − 1` | ≤ 2.8e−34; ≤ 1.3e−34 |
| mass budget `(f_wρ_w + f_vρ_v)/⟨ρ⟩ − 1` | ≤ 2.8e−40 |
| wall Raychaudhuri; wall mass conservation | ≤ 3.7e−41; ≤ 9e−51 |

The report's own table (≤ 2.9e−15; ≤ 2.2e−15 on this machine) is reproduced.
Those checks are rounding-level comparisons of algebraically identical
expressions (GC-F6).

**Outcome: `CONFIRMED_WITH_CAVEAT`.**
- The kinematics are `VERIFIED_FROM_PRIMARY_SOURCE` ([W07]) and derived.
- The dynamical statements are `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`:
  `ρ_v = 0`, "FLRW regions", and "backreaction and curvature are exactly the
  partition terms". They hold under the regional dust-FLRW equations in t.
  That is the assumption the live token `REGIONAL_DUST_FLRW_EQUATIONS` records
  as `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` (with
  `REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING = NOT_DERIVED`).
- The report does not show the step that gives `ρ_v = 0`. The check it lists
  for `⟨ρ⟩ = f_w/(6πGt²)` holds whatever `ρ_v` is, because `ρ_w` is defined
  as `1/(6πGt²)` in the script.
- [W09]'s own assumption is weaker than FLRW. Its footnote foot2, lines
  2399–2404, allows `Q_M = 0` with `δ²H_M = ⅓⟨σ²⟩_M`, i.e. inhomogeneous
  regions.

See GC-F2.

## 5. Claim C2 — the [GM] `a_w` notation finding

**Claim** (1G-A §5.3, on which [1G-C] §§3, 5 build): [GM] use one symbol for
two scale factors. (5.1) is the regional wall *volume* scale factor,
`∝ t^{2/3}`. (5.4) is the null-matched dressed factor `a_w = γ_w^{−1} a_D`.
The two differ by `γ_w(1−f_v)^{1/3} f_wi^{−1/3}`, and the dressed
`a_w/t^{2/3}` varies by 16.6% (f_v0 = 0.737).

**Re-derivation.**
- [GM] line 622 defines `a_Y := (V_Y(t)/V_Y(t_init))^{1/3}`, Y = D, v, w,
  used in (5.1) (line 623).
- Lines 638–641 then state "radial null geodesics match … a direct link
  between the scale factors of the two geometries, `a_w = γ_w^{−1} a_D`"
  (5.4).
- [W09] keeps them apart:
  - `a_w` in (wgeom), lines 269–272, and in (bav), line 294;
  - `a ≡ γ̄_w^{−1} ā` in (dgeom), lines 617–623.
- [W09]'s matching (etarel, line 606) gives `a_w dη_w = (ā/γ̄) dη̄`. So
  identifying `a_w` with `ā/γ̄` needs `dη_w = dη̄`, which is not [W09]'s
  matching.
- Read literally together, (5.1) and (5.4) would require
  `1 − f_v ∝ γ_w^{−3}`, which the tracker violates: `(1−f_v)γ_w³` is not
  constant.
- The ratio `a_w(5.1)/a_w(5.4) = γ_w(1−f_v)^{1/3} f_wi^{−1/3}` holds to
  2.3e−41.
- The dressed `a_w/t^{2/3} ∝ 2(1+s)^{4/3}/(2+3s)`, with `s = t/τ`, has a
  minimum at `s = 1/3`. Over 1e−6 t0 … t0 its max/min − 1 is **0.16576**.

**Outcome: `CONFIRMED`** (`VERIFIED_FROM_PRIMARY_SOURCE`).
- The inconsistency is genuine: one symbol, two incompatible time
  dependences, in one subsection. It is not a harmless reuse.
- It does not affect [GM]'s numerics, which use only the (5.4) meaning, via
  `1+z`.
- 1G-A's wording ("use one symbol for two scale factors", "recorded here, not
  'fixed'") is neutral and fair to the authors.

## 6. Claim C3 — assumptions A1–A4 and their citations

**Claim** ([1G-C] §5): A1–A4 as listed, with the quotes and line numbers of
§§4–5.

**Check** (every quote located):

| Citation in [1G-C] | Source text | Status |
|---|---|---|
| [W09] line 510, A1 quote | lines 510–511 | exact |
| [W09] Eq. (Q1), line 513 | line 513 (label `Q1` at 514) | exact |
| [W09] lines 311–458 (subsection), 461 | subsection 311–458; line 461 | exact |
| "100 h⁻¹ Mpc or somewhat larger" | line 327 | exact |
| "of order 110 h⁻¹ Mpc" | lines 367–368 | exact |
| "Below the scale … \|δρ/ρ\| ∼ 1" | lines 383–386 | **truncated**: the sentence goes on "which characterize the nonlinear regime" (GC-F1) |
| voids "a characteristic diameter 30 h⁻¹ Mpc" | line 277 (outside the cited 311–458); "30h⁻¹ Mpc diameter voids" at 386 | location imprecise (GC-F8) |
| [GM] line 602, both quotes (Sec. 5 preamble; RZA) | line 602 | exact |
| [GM] line 1083 (Conclusions) | line 1083 | exact |
| [GM] line 500 (over-determination, Sec. 4.1) | line 500 | exact |
| [W09] line 1764 | lines 1763–1764 (App. A, general solution) | exact |

**Assessment.**
- **A1.** It is a model postulate ([GM] line 618; [W07] lines 211–215; [W09]
  line 510), not a property "the tracker satisfies exactly". The tracker is
  exactly *consistent* with it, and was built on it ([W07]).
- **A2.** It carries an unstated clock identification (GC-F3).
- **A2's RZA precedent** ([GM] line 602) concerns a connected comoving domain,
  not a disconnected union of thin walls. The report lists this limitation
  itself (§9 item 2).
- **A3–A4.** Stated as assumptions; fine.

**Outcome: `CONFIRMED_WITH_CAVEAT`.**

## 7. Claim C4 — the regional wall law `Δ_w ∝ t^{2/3}` ([GM] (4.27) exact)

**Claim** ([1G-C] §5): on the wall regional background `ρ_eff,w ≡ 0`,
(4.9)–(4.12) reduce to the dust equations, and (4.27) is exact:
`Δ̈_w + 2H_wΔ̇_w − 4πGρ_wΔ_w = 0`, so `Δ_w ∝ t^{2/3}` or `t^{−1}`.

**Re-derivation.**
- With `Q_w = 0` and `W_w = ⟨R⟩_w = 0`, (3.12)–(3.13) give
  `ρ_eff,w = p_eff,w = 0`.
- In (4.11) the terms `4πGρ_effΔ_eff` and `12πGρ_effP̃_eff` vanish. The
  effective-fluid equations (4.10), (4.12) then have no background fluid to
  describe, and (4.9) with (4.11) gives (4.27) exactly.
- [GM]'s over-determination argument (line 500) applies only when
  `ρ_eff ≠ 0`, so it does not arise.
- `tH_w = 2/3` and `4πGρ_w t² = 2/3` hold exactly under C1's assumptions. With
  these coefficients, `t^{2/3}` and `t^{−1}` solve the equation identically
  (−2/9 + 8/9 − 6/9 = 0; 2 − 4/3 − 2/3 = 0).
- The law does not need the tracker's `ε_i = 0`. [W07] lines 311–321 give
  `a_w ∝ t^{2/3}` for the general two-scale solution. So the law is robust
  to the pre-tracker epoch (z ≳ 37, [W07]), provided the walls stay flat dust
  in t.

**Independent numbers.** None needed beyond the exact coefficients. The
script's integration (1.6e−13) reproduces; it tests the integrator on the EdS
equation (GC-F6).

**Outcome: `CONFIRMED_WITH_CAVEAT`.** It is exact given A1, flat walls, A2
and the clock identification of GC-F3. The report's class
`DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` is correct.

## 8. Claim C5 — photon-normalised growth, `X_wall`, σ(M8) values

**Claim** ([1G-C] §§5, 7):
- `lim (t0/t_e)^{2/3}/(1+z_e) = γ_w0(1−f_v0)^{1/3} = ½(2+f_v0)(1−f_v0)^{1/3}`;
- `X_wall = γ_w0(1−f_v0)^{1/3}/g_Λ`, with `g_Λ = 0.787813`;
- `X_wall` = 1.1129 / 1.2002;
- σ = 0.834 / 0.912 / 0.960 ([GM]) and 0.935 / 0.891 / 0.958 ([NW15]);
- the volume-average rows;
- `(1−f_v0)^{1/3} = 0.641` vs CGI 0.403 / 0.342.

**Re-derivation (frame chain).**
- The dressed redshift is `1+z = a_w0/a_w(5.4) = γ_w a_w0/a_D` ([GM] line
  663; [W07] line 440).
- `a_w,reg/a_w(5.4) = f_wi^{−1/3} γ_w(1−f_v)^{1/3}` (C2).
- Hence, exactly for every t_e,
  `(t0/t_e)^{2/3}/(1+z_e) = γ_w0(1−f_v0)^{1/3}/[γ_w(t_e)(1−f_v(t_e))^{1/3}]`.
  As t_e → 0 this tends to `γ_w0(1−f_v0)^{1/3}`.
- The report's formula `1+z = a/a0` in §5 is inverted (GC-F7). The
  computation uses the correct form.

**Independent numbers** (mine vs [1G-C]):

| Quantity | Mine | [1G-C] |
|---|---|---|
| `g_Λ` (flat ΛCDM, Ω_m = 0.315, quadrature) | 0.78781260 | 0.787813 |
| `γ_w0(1−f_v0)^{1/3}` [GM] / [NW15] | 0.876792 / 0.945510 | 0.877 / 0.946 |
| finite-t_e identity (mpmath) | exact to 7e−41 | ≤ 1e−15 (1G-B) |
| naive limit at 1e−8 t0, rel. diff | −4.6705e−9 = −f_v(t_e)/6 | −4.7e−9 |
| `X_wall` [GM] / [NW15] | 1.112945 / 1.200172 | 1.1129 / 1.2002 |
| `(1−f_v0)^{1/3}`; CGI comoving; Mészáros ([GM]) | 0.640696; 0.402662; 0.341693 | 0.641; 0.403; 0.342 |
| `X_CGI` comoving [GM] / [NW15] | 0.699460 / 0.858567 | 0.6995 / 0.8586 |
| EH98 Planck σ8 (absolute) | 0.83569 (+3.03%) | +3.03% (1G-A) |
| baryon-fraction sensitivity (f_b 0.12 / 0.20) | +7.0% / −8.1% | ±7–8% |

| Parameters | Law | (a) equal mass | (b) dressed 8/h | (c) bare 8/h̄ |
|---|---|---|---|---|
| [GM] | wall | 0.83392 (R 12.570) | 0.91214 (R 10.954) | 0.95990 (R 10.104) |
| [GM] | CGI comoving | 0.52410 | 0.57326 | 0.60328 |
| [NW15] | wall | 0.93471 (R 12.226) | 0.89105 (R 13.115) | 0.95825 (R 11.781) |
| [NW15] | CGI comoving | 0.66867 | 0.63743 | 0.68550 |

- Every entry of [1G-C] §7 matches to the printed digits.
- "3–15% above" (+2.8% / +15.2%) and "+3% to +18%" (max 0.960/0.8111 =
  1.184) are correct arithmetic. So are "3.80 / 2.68" and "0.877 / 0.946".
- The volume-average CGI numbers differ from the artifact by ≤ 2e−6
  (relative). This is the recorded early-start bias of 1G-A, far below the
  printed digits.

**Outcome: `CONFIRMED`** for the algebra and the numbers
(`DERIVED_FROM_VERIFIED_DEFINITIONS` given the wall law;
`NUMERICALLY_CORROBORATED`).
- Two caveats concern what the numbers are (GC-F1) and the radius
  conventions (GC-F5).
- Wall-adapted proper-length conventions give 0.714–0.857, outside part of
  the quoted range: `R_ph = (8/h)/[γ_w0(1−f_v0)^{1/3}]`, with dressed or bare
  h.

## 9. Claim C6 — the wall-clock alternative is inadmissible

**Claim** ([1G-C] §6): a flat dust FLRW wall in wall proper time τ_w would
need `3(H_w^τ)² = 8πGρ_w` with `H_w^τ = γ_wH_w = H_D`. The residual is
`γ_w² − 1` = 0.873 / 0.725. So "the common-time law of Sec. 5 is thus the
only admissible regional law within [GM]'s dust-proper-time framework".

**Re-derivation.**
- `γ_w0² − 1` = **0.872792** / **0.725282**. Confirmed.
- **Non-circular version.** The residual as written takes `ρ_w = ⟨ρ⟩/f_w`,
  which itself comes from the t-frame regional equations (`ρ_v = 0`). The
  mass budget alone gives a stronger result. For any `ρ_v ≥ 0`,
  `ρ_w ≤ ⟨ρ⟩/f_w = 3H_w²/(8πG)`, while the τ_w wall would need
  `3H_D²/(8πG) = γ_w² · 3H_w²/(8πG)`. The deficit therefore requires
  `ρ_v/⟨ρ⟩ = (1−γ_w0²)/f_v0` = **−1.184** ([GM]) and **−1.157** ([NW15]).
  So the variant is inadmissible even if voids hold matter.
- A second candidate the report does not test also fails. That is the flat
  dust wall built on the dressed `a` of (dgeom), in τ_w. Its density
  parameter is `Ω_M = γ̄³Ω̄_M = ½(1−f_v0)(2+f_v0)` ([W09] line 638) = 0.360 /
  0.490, far from 1.
- **Flow parameterisation.** Take the regional volume `a_w,reg` with wall
  mass conservation, and require `(d ln a_w,reg/dT)² = 8πGρ_w/3` for some
  time T.
  - With `ρ_w = ⟨ρ⟩/f_w`, this forces `dT = dt`.
  - With any `ρ_v ≥ 0`, it forces `dT ≥ dt`, whereas `dτ_w = dt/γ_w < dt`.

  So t is the only time in which the regional wall volume obeys flat-dust
  Friedmann.

**Outcome: `CONFIRMED_WITH_CAVEAT`.**
- The inadmissibility is `DERIVED_FROM_VERIFIED_DEFINITIONS` (with
  `ρ_v ≥ 0`).
- "Only admissible" holds for dust-FLRW regional laws on `a_w,reg`. But the
  law it selects takes t to be the wall matter's proper time. [W07] line
  211–215 and [W09] lines 269–272, 461–475 and 483–485 assign the wall
  geometry and the sub-cell Hubble flow to local proper time τ_w. So the
  report's last §6 sentence is an assumption, not a result: "Wall observers'
  clocks enter σ8 only through the redshift–time map".
- The rejection is consistent with the live
  `NAIVE_W09_WALL_CLOCK_AS_REGIONAL_PROPER_DUST_FLRW_CLOCK = REJECTED_UNSUPPORTED`.
- What the variant rejects is [W07] (figeom) / [W09] (wgeom) read literally
  as a dust-FLRW solution. The report should say so (GC-F3).

## 10. Claim C7 — the scale hierarchy and the σ(M8) reading

**Claim** ([1G-C] §1 verdicts 2 and 4; §4; §7 "Reading"; §9 item 1; inventory
`supersedes`, `scale_hierarchy`):
- σ8 lies inside a ≈100 h⁻¹ Mpc dust cell.
- The volume-average CGI growth describes super-cell modes.
- "mass-weighted fluctuations at 8 h⁻¹ Mpc are governed by the wall regional
  dynamics" (§4, `DERIVED_FROM_VERIFIED_DEFINITIONS`).
- 0.834/0.935 is the "Conditional σ(M8) (mass-weighted,
  framework-consistent)". It "supersedes 1G-A's volume-average values …
  for σ8-scale, mass-weighted statistics", and the open problem is "settled"
  for mass-weighted σ(M8).

**Re-derivation.**
- **The scales.**
  - σ8 radius across the report's conventions and both parameter sets:
    10.1–13.1 Mpc (not "11–12.6", GC-F8).
  - 100 h⁻¹ Mpc = 136.9 Mpc (h = 0.7303) to 163.9 Mpc (h = 0.61), or
    172.8–193.4 Mpc with the bare h̄.
  - So "σ8 inside a dust cell" and "about 10× smaller" hold.
- **The CGI domain.** The reading that the volume-average CGI dust describes
  inter-cell modes identifies [GM]'s dust ("the idealised coarse-grained dust
  flow", [GM] line 636) with [W09]'s ≥ 100 h⁻¹ Mpc dust particles (line
  326–327). This is a reasonable interpretation. It is still an assumption
  (`DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`), not a derivation.
- **The σ(M8) reading does not follow.**
  - **[W09] makes sub-cell scales nonlinear.** Lines 383–386 read in full:
    "Below the scale of statistical homogeneity we will typically find
    density contrasts |δρ/ρ| ∼ 1 which characterize the nonlinear regime".
    Footnote foot11 (lines 2648–2651): "My two scales refer to largest
    relevant scales in the 'nonlinear regime'". So the wall/void partition
    that sets the mass distribution at 8 h⁻¹ Mpc is, in [W09]'s own model,
    the nonlinear product of sub-cell fluctuations.
  - **The geometry.** An 8 h⁻¹ Mpc sphere has diameter 16 h⁻¹ Mpc. The
    dominant voids are 30 h⁻¹ Mpc across and fill 40–50% of the universe
    ([W09] lines 277–278). Voids of all sizes fill f_v0 = 0.74 of the volume
    in the tracker.
    Walls are 3.80× denser than the mean. The density contrast of 8 h⁻¹ Mpc
    spheres relative to the global mean is dominated by this O(1) partition.
  - **What the wall law computes.** Its `Δ_w` is the CGI Laplacian scalar
    relative to the *wall* mean `ρ_w`. It is the linear, Lagrangian variance
    of the wall-internal field at mass M8. It is not the mass variance of
    M8 spheres relative to the global mean, which is what σ8 (0.811) means
    in ΛCDM.
- **Verdict 4's conditionality is incomplete.** It lists A1–A4 but omits
  three things:
  - (i) the reference density (wall mean);
  - (ii) the linearity of the sub-cell field, contrary to [W09] 383–386;
  - (iii) the clock identification of GC-F3.

  "Those values remain the super-cell growth" is asserted, not derived:
  1G-C does not test the CGI law against super-cell physics.

**Outcome.**
- C7a, σ8 inside a dust cell; CGI as a super-cell description: **`CONFIRMED_WITH_CAVEAT`**.
  The quotes are `VERIFIED_FROM_PRIMARY_SOURCE`, but the §4 consequence is
  over-classified.
- C7b, "Mass-weighted σ(M8) = wall law; supersedes 1G-A; settled": **`REFUTED`**
  as stated. The numbers are confirmed as the wall-internal linear statistic
  only.

The project's live records narrow the token to exactly this reading, via
1G-D §9 (owner approval 2026-09-29). I reached the same conclusion from [W09]
alone, without relying on 1G-D. See GC-F1 and GC-F4.

## 11. Claim C8 — scale-dependent step and the transition (`NOT_DERIVED`)

**Claim** ([1G-C] §1 verdict 5, §8):
- the power step `(X_wall/X_CGI)²` = 1.95–2.53 (comoving) and the f_v0 table;
- the transition shape is `NOT_DERIVED` because "the tracker is
  self-similar and has no length scale";
- "a sharp observational discriminant".

**Check.** My table, using my own CGI integrations:

| f_v0 | 0.50 | 0.60 | 0.627 | 0.695 | 0.737 | 0.80 |
|---|---|---|---|---|---|---|
| comoving | 1.5863 | 1.8579 | 1.9541 | 2.2654 | 2.5318 | 3.1255 |
| Mészáros | 1.8546 | 2.3000 | 2.4642 | 3.0176 | 3.5159 | 4.6997 |

Every entry of [1G-C] §8 matches to the printed digits.

**Outcome: `CONFIRMED_WITH_CAVEAT`.**
- The step is stated conditionally ("If both limits hold").
- `NOT_DERIVED` for the transition is supported: the tracker contains no
  sub-horizon spatial scale.
- The wording has two problems:
  - "self-similar" is imprecise. The tracker has a time scale τ, with
    `f_v = t/(t+τ)`; only the family is self-similar in `H_D0 t`.
  - "sharp observational discriminant" / "sharp, testable signature"
    attaches observational significance to a conditional theoretical step.
    1G-D has since recorded that step as superseded.

See GC-F9.

## 12. Claim C9 — status tokens resting on 1G-C

**Tokens** (`scientific_status.py` lines 44–56):
- `TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"`;
- `SUPER_CELL_TO_SUB_CELL_GROWTH_TRANSITION = "NOT_DERIVED"`.

**Check.**
- Both values are supported by the evidence (C4, C8).
- The first token's comment says "under assumptions A1–A4 … narrowed by
  Phase 1G-D Sec. 9 … wall-internal linear statistic, relative to the wall
  mean". That matches what I derived.
- The one gap: the listed assumptions omit the identification of t with the
  wall matter's proper time (GC-F3).
- The token *name* keeps "MASS_WEIGHTED_SUB_CELL". The comment narrows it.
  Renaming is not proposed; token names are API.

**Outcome: `CONFIRMED_WITH_CAVEAT`.**

## 13. Claim C10 — frozen package background functions

**Check.**
- The package's `fv`, `dfv_dt`, `a_D`, `H_D`, `Q_D`, `R_D` (D1-corrected),
  `rho_d`, `gamma_w`, `a_w` (the (5.4) dressed object) and `1 + redshift`
  agree with my mpmath evaluation of the printed definitions to ≤ 4.4e−16
  (relative). This holds at 15 epochs for [GM] and [NW15].
- The script's `H_w = H_D − ḟ_v/(3(1−f_v))` and `ρ_w = ⟨ρ⟩/(1−f_v)` are the
  correct (5.1) regional forms (the latter under `ρ_v = 0`).

**Outcome: `CONFIRMED`.**

## 14. Claim C11 — reproducibility and record consistency

**Check.**
- The script and artifact reproduce (Sec. 2).
- Inventory values match the artifact and the report to their printed
  digits. The recorded `max_identity_error` 2.886579864025407e−15 is from
  the owner's platform; this machine gives ≤ 2.2205e−15. Both are far inside
  the 1e−13 budget.
- The in-place "(Corrected 2026-09-29 …)" note in §5 was made in the
  integration commit `214a626`, before any tag. It is correct: the
  finite-t_e identity is exact and the naive limit differs by −f_v(t_e)/6.

**Outcome: `CONFIRMED`.**

## 15. Findings

| Id | Severity | Resolution class | Title |
|---|---|---|---|
| GC-F1 | MEDIUM-HIGH | OWNER_DECISION | The "mass-weighted σ(M8)" identification, "supersedes" and "settled" are not supported; the result is the wall-internal linear statistic |
| GC-F2 | MEDIUM | OWNER_DECISION | "Exactly two FLRW regions" is over-classified: its dynamical content rests on the regional dust-FLRW equations in t |
| GC-F3 | MEDIUM | OWNER_DECISION | The common-time law identifies t with the wall matter's proper time; the assumption is unstated, and "only admissible" depends on it |
| GC-F4 | LOW-MEDIUM | OWNER_DECISION | Superseded 1G-C readings are flagged incompletely in the current records |
| GC-F5 | LOW | OWNER_DECISION | Radius conventions (b), (c) are volume-average conventions; 0.83–0.96 is not a convention envelope for the wall law |
| GC-F6 | LOW | OWNER_DECISION | The §3 identity table and the §5 integration are algebraically circular checks |
| GC-F7 | LOW | UNAMBIGUOUS_ERRATUM | Inverted dressed-redshift formula in §5 (`1+z = a/a0`) |
| GC-F8 | LOW | UNAMBIGUOUS_ERRATUM | Imprecise σ8-radius range and two source-location statements |
| GC-F9 | LOW | OWNER_DECISION | Wording and governance: "none applied" vs "already sent"; "sharp observational discriminant"; "self-similar" |

### GC-F1 (MEDIUM-HIGH, OWNER_DECISION)

**Statement.** The wall law, `X_wall` and the σ values are correct, but they
describe the linear variance of the wall-internal field relative to the wall
mean. [1G-C] presents them as more than that, in four places:
- §1 verdict 4: "Conditional σ(M8) (mass-weighted, framework-consistent)";
  "supersedes 1G-A's volume-average values … for σ8-scale, mass-weighted
  statistics";
- §4 "Consequence" (`DERIVED_FROM_VERIFIED_DEFINITIONS`);
- §7 "Reading" ("the mass-weighted linear σ(M8) of a Timescape universe");
- §9 item 1 ("settled … for mass-weighted σ(M8)").

**Evidence.**
- [W09] lines 383–386 (the full sentence, truncated in [1G-C] §4) and foot11
  (lines 2648–2651).
- The geometry: void diameter 30 h⁻¹ Mpc (line 277) > σ8 sphere diameter
  16 h⁻¹ Mpc; f_v0 = 0.737; `ρ_w/⟨ρ⟩ = 3.80`.
- `Δ_w` is defined relative to `ρ_w` ([GM] CGI variables on the regional
  background).

**Consequence.** The headline comparison "3–15% above Planck-ΛCDM" compares a
wall-internal statistic with a global-mean σ8. The "supersedes" and "settled"
statements, and the inventory's `supersedes` field, overstate the result.

The report already says the number is conditional, model-internal and not an
observational σ8, with no consistency or tension claim (§7, lines 241–243).
The defect is in its *model-internal* meaning, not in an observational claim.

**Suggested resolution.** A dated successor note for 1G-C. It should:
- narrow §1 V4, §4, §7 and §9 item 1 and the inventory fields `supersedes` /
  `scale_hierarchy` to "wall-internal linear σ at mass M8, relative to the
  wall mean";
- quote [W09] 383–386 in full, with foot11;
- withdraw "settled".

This matches the owner-approved token comment. No number changes.

### GC-F2 (MEDIUM, OWNER_DECISION)

**Statement.** [1G-C] §1 V1 and §3 classify the claim "The tracker is exactly
two FLRW regions in the common time t" as `DERIVED_FROM_VERIFIED_DEFINITIONS`.
The claim covers `ρ_v = 0`, `ρ_w = 1/(6πGt²)`, the void curvature and "all
matter sits in walls". Only the kinematics follow from [GM] (5.1),
(5.5)–(5.6); they are also stated explicitly in [W07] lines 317–321 and
404–406.

**Evidence.**
- The dynamics need three inputs: the regional dust Friedmann equations in
  t with `Q_v = Q_w = 0` ([GM] line 618; [W09] line 510), flat walls ([GM]
  line 620) and D1. With the printed (5.7), `ρ_v < 0`.
- The report does not show the `ρ_v = 0` step. Its listed check is
  independent of `ρ_v`.
- The live token `REGIONAL_DUST_FLRW_EQUATIONS = DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`
  and 1G-B §5 ("the regional embedding stays `NOT_DERIVED`") classify the
  same step more cautiously.
- [W09] foot2 allows non-FLRW regions with `Q = 0`.

**Consequence.** An evidence class stronger than the evidence. The same
wording propagates to `CLAUDE.md` (line 254) and `README.md` (lines 31–33):
"exactly empty Milne voids plus EdS walls". Under the stated assumptions the
result is exact; I confirm it to 1e−34.

**Suggested resolution.** Split the class:
- kinematics `VERIFIED_FROM_PRIMARY_SOURCE` (+ derived);
- dynamics `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`, naming the regional
  dust-FLRW-in-t assumption and D1.

Also state that A1 is a postulate that the tracker is consistent with, not a
property it "satisfies exactly".

### GC-F3 (MEDIUM, OWNER_DECISION)

**Statement.** A2 and §6 evolve wall matter with [GM]'s dust-frame equations
in the common time t. This identifies t with the proper time of the wall
matter. It is not among A1–A4. §6 then concludes that the t-law is "the only
admissible regional law" and that "Wall observers' clocks enter σ8 only
through the redshift–time map".

**Evidence.**
- **Timescape puts the wall and sub-cell physics in local proper time.**
  - [W07] lines 211–215: the finite-infinity (wall) geometry is written in
    τ_w with the regional `a_w`; lines 229–230, 261–262: t "differs from the
    wall-time", and `H_w` is measured "by volume-average clocks".
  - [W09] lines 269–272 (wgeom): the same wall geometry in τ_w.
  - [W09] lines 461–475: t is not "the relevant parameter measured by every
    isotropic observer … within any dust cell". The sub-cell flow is "in
    terms of local proper lengths with respect to local proper times".
  - [W09] lines 483–485: `H̄ = (1/a_w) da_w/dτ_w`.
- **[W07] notes the mismatch itself.** Lines 320–321: EdS "in volume average
  time not locally measured wall time".
- **[GM]'s framework puts the dust in t.** [GM] line 441 makes t the dust
  proper time, and line 636 associates t with "the idealised coarse-grained
  dust flow".

**Consequence.** The law is consistent within [GM]'s formal framework, but it
is not a derivation within Timescape's clock ontology at sub-cell scales,
where σ8 lives. §1 V4's "framework-consistent" and §6's "only admissible"
need this qualifier. The token comment for
`TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW` lists A1–A4 only.

**Suggested resolution.** Add an explicit assumption: A5 — wall matter clocks
the common (coarse-grained dust) time t. State that the τ_w alternative fails
the mass budget for any `ρ_v ≥ 0` (Sec. 9 above). Rephrase the §6 last
sentence as an assumption.

### GC-F4 (LOW-MEDIUM, OWNER_DECISION)

**Statement.** The records that give the current reading flag 1G-C's
superseded passages only in part.
- **Successor record.** Its §4 table ("Superseded readings") lists, for 1G-C,
  only §10 item 2, §12 and the inventory's `status_tokens_changed`.
- **1G-D.** It lists §8 and §9's "settled" statement as superseded (lines
  296–298), but not §1 V4, §4 "Consequence", §7 "Reading" or the inventory
  `supersedes` field.
- **`CLAUDE.md` lines 255–257** still read "so mass-weighted σ(M8) follows
  the wall law: 0.83–0.96".
- **`README.md` lines 34–35** still read "Mass-weighted σ at the Planck
  8 h⁻¹ Mpc mass follows the wall-regional growth law: 0.83–0.96".

In both files the narrowing appears only in a neighbouring bullet.

**Consequence.** A reader of these records can take 0.83–0.96 as a σ(M8),
contrary to `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC` and the token comment.

**Suggested resolution.**
- Extend the successor record's §4 table.
- Qualify the two sentences as "the wall-internal linear σ at mass M8
  (relative to the wall mean)".

### GC-F5 (LOW, OWNER_DECISION)

**Statement.** The wall rows of §7 reuse 1G-A's radius conventions (b), (c).
These were defined for the volume-average picture. Convention (c) uses
volume-average proper length, which includes void expansion.
- For wall matter, a present proper length `r_now` maps to
  `R_ph = r_now/[γ_w0(1−f_v0)^{1/3}]`.
- With 8/h or 8/h̄ this gives σ_wall = 0.837 / 0.714 ([GM]) and
  0.857 / 0.761 ([NW15]).

**Consequence.** "0.83–0.96 across the three radius conventions" and "+3% to
+18%" are not a convention envelope for the wall law. The equal-mass headline
is unaffected, and §9 item 3 already lists the radius convention as open.

**Suggested resolution.** State that (b), (c) are volume-average-picture
conventions. Either add a wall-adapted convention or drop the range claim.

### GC-F6 (LOW, OWNER_DECISION)

**Statement.** The §3 checks compare package closed forms with algebraically
identical rearrangements:
- `Q_D = 2f(1−f)/(3t²)` against `6f(1−f)(1/t−2/(3t))²`;
- `R_D = −6f/t²` against `f·(−6/t²)`;
- `ρ_d = (1−f)/(6πGt²)` against `(1−f)·ρ_w`;
- `H_D` and `γ_wH_w`, with `H_v = 1/t` and `H_w = 2/(3t)` hard-coded (script
  line 72).

The §5 integration uses coefficients that reduce exactly to `2/(3t)` and
`1/(6πGt²)`, so it tests the integrator on EdS.

**Consequence.** The "max rel. error" column measures floating-point rounding,
not agreement with [GM]'s printed definitions. The underlying identities are
true: this audit verifies them non-circularly to ≤ 1.3e−34.

**Suggested resolution.** Describe these as algebraic consistency checks and
point to a non-circular check.

### GC-F7 (LOW, UNAMBIGUOUS_ERRATUM)

**Statement.** [1G-C] line 182 writes the dressed redshift as `1+z = a/a0`.
[GM] line 663 gives `1 + z = a_{w,0}/a_w`, which is `a0/a`.

**Consequence.** Typo only. The formula used on line 186 and in the script is
correct.

### GC-F8 (LOW, UNAMBIGUOUS_ERRATUM)

**Statement.** Three imprecisions:
- (i) §4 line 134: "R ≈ 11–12.6 Mpc … (≈140–160 Mpc …)". The report's own
  conventions and parameter sets give 10.1–13.1 Mpc and 136.9–163.9 Mpc.
- (ii) §4 line 123 quotes "a characteristic diameter 30 h⁻¹ Mpc" under
  "[W09] … (lines 311–458) and line 461". The phrase is at [W09] line 277.
- (iii) §3 line 113, "These facts are implicit in [W07]/[W09]". The
  kinematic facts are explicit in [W07] lines 317–321 and 404–406.

**Consequence.** Citation and number accuracy only; conclusions unchanged.

### GC-F9 (LOW, OWNER_DECISION)

**Statement.** Three wording and governance points:
- **"none applied" vs "already sent".** §10's heading says recommendations
  are "none applied; each requires human approval". Item 1 says "The lead has
  already sent this scope addition to the 1G-B implementer". 1G-B §1 records
  that the lead added the wall law during 1G-B.
- **Observational labels.** §1 V5 and §8 call the conditional P(k) step "a
  sharp observational discriminant" and "a sharp, testable signature". This
  is in tension with the project rule against attaching observational labels
  to theoretical quantities. The step is now recorded as superseded (1G-D).
- **"self-similar".** §8 calls the tracker "self-similar", but it has a time
  scale τ.

**Suggested resolution.**
- The owner confirms, in the successor note, that the 1G-B wall-law option
  was approved.
- Rephrase the V5/§8 wording as "a conditional theoretical feature (no
  observational comparison is made)".
- Replace "self-similar" with "has no sub-horizon length scale".

## 16. Proposed errata (exact old → new; the lead applies them through a dated successor note)

All in `reports/phase1g_c_two_scale_growth_law.md` at `6f7937c`.

1. **GC-F7**, line 182.
   - Old: ``redshift `1+z = a/a0` ([GM] (5.4); [W09]'s dressed `a`) and``
   - New: ``redshift `1+z = a0/a` ([GM] (5.4); [W09]'s dressed `a`) and``
   - Proof: [GM] main.tex line 663, "`1 + z= a_{w,0}/a_w`"; [W07]
     solution.tex line 440; package `redshift` (observables.py lines
     98–108); the report's own line 186.
2. **GC-F8 (i)**, line 134.
   - Old: `(R ≈ 11–12.6 Mpc) is about 10× smaller than the dust-cell scale (≈140–160 Mpc for h = 0.73–0.61).`
   - New: `(R ≈ 10–13 Mpc across the three radius conventions of Sec. 7 and both parameter sets) is about 10× smaller than the dust-cell scale (≈137–164 Mpc for h = 0.73–0.61).`
   - Proof: the radii of Sec. 7 conventions (a), (b), (c):
     - [GM]: 12.570, 10.954, 10.104 Mpc;
     - notebook: 12.547, 10.924, 10.076;
     - [NW15]: 12.226, 13.115, 11.781.

     100/0.7303 = 136.93 and 100/0.61 = 163.93. Reproduced by the phase
     script's radius definitions (1G-A lines 424–431).
3. **GC-F8 (ii)**, line 123.
   - Old: `- voids have "a characteristic diameter 30 h⁻¹ Mpc";`
   - New: `- voids have "a characteristic diameter 30 h⁻¹ Mpc" (line 277; "30h⁻¹ Mpc diameter voids", line 386);`
   - Proof: [W09] observe.tex line 277 ("Voids of a characteristic diameter
     $30h^{-1}$ Mpc") and line 386.
4. **GC-F8 (iii)**, line 113.
   - Old: `These facts are implicit in [W07]/[W09]. They are recorded here as verified`
   - New: `The kinematic facts are stated explicitly in [W07] (solution.tex lines 317–321 and 404–406); the others are implicit in [W07]/[W09]. They are recorded here as verified`
   - Proof: [W07] lines 317–321 ("`a_w = a_w0 t^{2/3}` … exactly that of an
     Einstein–de Sitter universe, but in volume average time not locally
     measured wall time") and lines 404–406 ("void regions expand exactly as
     a Milne universe in volume–average time").

## 17. Items for owner decision

1. **GC-F1.** A 1G-C successor note that:
   - narrows §1 V4, §4 "Consequence", §7 "Reading", §9 item 1 and the
     inventory `supersedes` / `scale_hierarchy` fields to the wall-internal
     linear statistic relative to the wall mean;
   - quotes [W09] 383–386 in full, with foot11;
   - withdraws "settled", and decides whether "supersedes … for σ8-scale
     statistics" is withdrawn.

   Text only.
2. **GC-F2.** Reclassify §1 V1 / §3. Kinematics:
   `VERIFIED_FROM_PRIMARY_SOURCE` + derived. Dynamics:
   `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` (regional dust-FLRW in t,
   `Q_v = Q_w = 0`, flat walls, D1). Align CLAUDE.md line 254 and README
   lines 31–33.
3. **GC-F3.** Add assumption A5 (wall matter clocks the common time t) to
   §5, §6 and the `TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW` comment. The
   token value is unchanged.
4. **GC-F4.** Extend the successor record's superseded-readings table.
   Qualify CLAUDE.md lines 255–257 and README lines 34–35.
5. **GC-F5.** Label conventions (b), (c) as volume-average conventions.
   Either add a wall-adapted convention or drop the "0.83–0.96" / "+3% to
   +18%" envelope.
6. **GC-F6.** Describe the §3 and §5 checks as algebraic consistency checks.
7. **GC-F9.** Confirm the 1G-B wall-law approval. Rephrase "sharp
   observational discriminant" / "testable signature" and "self-similar".

## 18. Verdict and readiness for tagging

**Verdict: `ACCEPT_WITH_CORRECTIONS`.**
- Every load-bearing equation and number of 1G-C survives an independent,
  non-circular re-derivation from the primary sources. This covers the
  two-region identities, the wall law, the photon-normalised factor,
  `X_wall`, the σ values, the power steps and the wall-clock residual. No
  equation is wrong and no number changes.
- The corrections concern:
  - what the σ numbers mean (GC-F1);
  - two evidence classifications and an unstated clock assumption (GC-F2,
    GC-F3);
  - record hygiene (GC-F4 to GC-F9).

**Tag readiness: `NOT_READY_OWNER_DECISION_REQUIRED`.**
- GC-F1 to GC-F3 change the stated scope or evidence class of scientific
  conclusions. Under the project's rules they need the owner.
- All are text-only; none touches an equation, a token value, a tolerance or
  code.
- Once a dated successor note records the owner's decisions and the four
  errata, 1G-C is `READY_FOR_TAG`.

## 19. Limitations

- [NW15] (arXiv:1410.3470) was not opened. I used the parameters as the
  phase uses them (f_v0 = 0.627, H0 = 61.0 km/s/Mpc).
- The Planck Ω_m = 0.315, h = 0.674 rounding is inherited from the frozen
  `qplus` recipe and was not re-audited (1G-A scope).
- mpmath derivatives are numerical (`mp.diff`) at 40 digits. The residuals
  quoted (≤ 1e−34) are limited by that, not by the identities.
- The CGI growth integrations start at t_e = 1e−8 t0 with the leading
  regular-mode ratio (`Δ_eff/Δ_d = 1/5`). They agree with the artifact to
  ≤ 2e−6.
- No Windows run. The owner's platform values (e.g. max identity error
  2.9e−15) could not be reproduced bit for bit; they are within budget.
- I did not audit 1G-A, 1G-B, 1G-D or 1G-E beyond the passages named in
  Sec. 2.

## 20. Preservation statement

- **Files written:** exactly two, in the main tree: this report and its JSON
  companion. Scratch scripts and outputs are in
  `…/scratchpad/audit_c/` only.
- **Not edited, staged, committed, pushed or tagged:** no repository file,
  including every frozen report, code, test and script.
- **AUDIT_TREE:** the phase script rewrote its git-ignored artifact there.
  The original bytes (`bf970070…`) were restored.
- **Environments:** mpmath and sympy were installed only into the scratch
  directory. The project virtual environments are unchanged.
