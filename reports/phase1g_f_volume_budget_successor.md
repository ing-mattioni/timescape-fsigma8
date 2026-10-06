# Phase 1G-F — fixed-domain volume-budget successor

Date: 2026-10-01; audit remediation revision: 2026-10-02; integration
revision (R2-N1 to R2-N3): 2026-10-06. Base: `fb5d95245bc0cb19ce6cd1438177f1a597bb232f`
(main, merge of PR #3).

**Authorization, distinguished by kind:**

- **Verbatim owner instruction**, dated 2026-10-01 in the session record:
  «Ottimo, procedi con entrambe le cose (e sistema anche CLAUDE.md se
  riesci)».
- **Scope interpretation, a paraphrase rather than a quotation.** "Both
  things" was read as the proposed 1G-F cumulative-volume rectification and
  the 1G-G theoretical continuation. The parenthesis covers the CLAUDE.md
  repair.
- **Later, separate decisions.** On 2026-10-02 the owner confirmed with
  «si confermo» two decisions, recorded in
  `phase1g_d_linear_statistic_status_successor.md`:
  - the D token reclassification to `NOT_DERIVED`;
  - the split of frozen F verdict 2.
- **The integration step.** On 2026-10-06 the owner separately authorized
  commits and an ordinary push of the phase branch.
  `phase1g_fg_remediation_integration.md` records that authorization. It
  grants no scientific or observational status.

This is a **scientific correction of the cumulative interpretation**, not
a numerical refactor. The frozen 1G-F report, inventory and script are
preserved. No package equation, initial condition or observational authorization changes.
The separately approved 2026-10-02 D successor changes one classification
token to `NOT_DERIVED`; see `phase1g_d_linear_statistic_status_successor.md`.
The 2026-10-01 version was independently audited with corrections required.
This revised local deliverable has not been frozen; the audit does not
certify subsequent edits. Exact owner instructions and validation are in
`phase1g_fg_audit_remediation.md`.

## 1. What is corrected

The frozen `M3_two_scale_volume_budget` applies a new denominator after
each radius cut. Its all-size value is a valid two-density budget. Its
cut-dependent values describe **different truncated universes** in which
excluded void mass becomes wall mass. They are not cumulative fractions
of one fixed population in one domain.

The additive interpretation of a cumulative volume is [JLH13] Eq. (13).
For the conditional M3 model, let the conserved domain mass be unity,
the full void mass fraction be `m`, the wall density set the density unit,
and `x = rho_void/rho_wall > 0` be constant across void sizes. Then

\[
 Z=V_D/(M_D/\rho_w)=1-m+m/x. \tag{F1}
\]

For a subset of voids with mass fraction `m_A`,

\[
 F_V(A)=\frac{m_A/x}{1-m+m/x}
       =\frac{m_A}{x(1-m)+m}. \tag{F2}
\]

For disjoint subsets A and B, `F_V(A union B)=F_V(A)+F_V(B)`.
Wall volume plus full void volume is unity. If x=1, volume and mass
fractions coincide. Units cancel between mass and density.

The frozen operation is instead

\[
 B(m_A)=\frac{m_A/x}{1-m_A+m_A/x}. \tag{F3}
\]

For m_A=m_B=0.1 and x=0.2, `B(m_A)+B(m_B)=5/7`, whereas
`B(m_A+m_B)=5/9`. F2 yields 5/9 both ways. This is a normalization error
only when F3 is labelled as a cumulative volume in a fixed domain.

The density interpretation is an M3 assumption. [JLH13]'s spherical x is
relative to the EdS reference density; identifying that reference with
the wall density is inherited from the two-scale budget. This successor
does not prove that identification or identify M3 with the [JLH13] Vdn
model. For size-dependent x, replace m_A/x by an integral of `dm/x`; a
single x must not be silently used.

Importing the spherical density into M3 needs five physical identifications:
(i) a simultaneous bang and the C1/A5 common wall age; (ii) unperturbed,
spatially flat EdS walls; (iii) a spherical isolated seed evolving against
that wall background, an approximation increasingly strained at large
filling factor; (iv) the early Lagrangian mean identified with the wall
reference density; (v) all non-void mass, including cloud-absorbed walks,
assigned to the wall phase at rho_w. These are assumptions of this import,
not hypotheses needed to prove the elementary F1-F3 mass/volume identities.
No spatial embedding follows from the identities.

## 2. Recomputed primary results

Same inputs as frozen 1G-F: C1 wall EdS common-time clock, corrected
[JLH13] shell crossing, collapse upper barrier, photon-comoving radii,
Planck-anchored EH98 early spectrum. No growth, frame, barrier or
quadrature change. [SvdW04] Eq. (3)/(C8) gives
`m=0.3829709426561785`; [JLH13] (A8)-(A12) gives
`x=0.20472233400490963`, `delta_v=-2.7171803438378705`.
Thus `Z=2.487713780228009` and full void volume is
`0.7519694338440862` in both parameter cases.

| Minimum radius, h^-1 Mpc | GM frozen F3 | GM fixed F2 | NW15 frozen F3 | NW15 fixed F2 |
|---|---:|---:|---:|---:|
| all sizes | 0.751969 | 0.751969 | 0.751969 | 0.751969 |
| 1 | 0.694832 | 0.624265 | 0.714902 | 0.666057 |
| 2 | 0.583835 | 0.438104 | 0.622001 | 0.494778 |
| 5 | 0.265214 | 0.135106 | 0.310706 | 0.165886 |
| 10 | 0.035806 | 0.014815 | 0.046123 | 0.019246 |
| 15 | 0.002546 | 0.001026 | 0.003263 | 0.001315 |

Six decimals distinguish the two definitions, not physical precision.
The inherited grid overestimates the z=0 primary >=10 tails by 0.22–0.24%
and the >=15 tails by 0.69–0.75%, compared with the independent audit's
absorption-CDF calculation. At >=15 quote at most two significant figures
(about 0.0010 / 0.0013). Extra digits below identify the grid computation;
they are not numerical accuracy or physical error bars. Independent values
are 0.01478039 / 0.01920372 at >=10 and 0.00101855 / 0.00130528 at >=15.
The model and quadrature are retained; this revision corrects the precision
claim rather than silently replacing the archived radius grid.
In particular, >=10 h^-1 Mpc voids fill **1.48% / 1.92%**, replacing
the frozen ~4% fixed-domain reading. The volume-weighted median stays
2.40456 / 2.80045 h^-1 Mpc: constant normalization does not change the
size distribution's normalized shape. The primary below-grid mass is
3.36e-9 / 4.04e-9; no renormalization or tail clipping is introduced.

The disagreement with a population dominated by much larger voids is
strengthened within this model. It is not an observational exclusion:
void definitions, selection, spatial embedding and evolution remain
external. F2 does not derive a spatial tessellation or resolve overlap.

## 3. History and cutoff meanings

The full two-barrier mass fraction is independent of the growth clock
when integrating all scales; x is also held fixed in the threshold
model. Consequently the full M3 fraction stays 0.751969 with redshift,
unlike the tracker. This failure of the all-size history is unaffected
by the correction.

Cutoffs that select a fraction equal to the tracker target are:

| Case | z | tracker f_v | fixed-domain F2 cutoff | truncated-universe F3 cutoff |
|---|---:|---:|---:|---:|
| GM | 0 | 0.737000 | 0.346454 | 0.505672 |
| GM | 3 | 0.305585 | 0.061074 | 0.149942 |
| NW15 | 0 | 0.627000 | 1.229907 | 1.951538 |
| NW15 | 3 | 0.190740 | 0.129494 | 0.261278 |

All cutoffs use h^-1 Mpc in the inherited photon-comoving convention and
piecewise linear interpolation of volume fraction against log radius on
the inherited 481-node grid. They are diagnostics, not fitted parameters.
For this C1 threshold model over z=0–3, a fixed cutoff fails the two-epoch
test under **either** meaning. This is not a universal evolution theorem:
the GM z=0 cutoff stays within about 1.5% of the tracker at z=0.5 but is
about 11% low by z=1. Its required cutoff is non-monotone
(0.346, 0.369, 0.260, 0.124, 0.061 h^-1 Mpc).
Matching a selected subset to f_v is not predicting the full fraction:
the smaller voids still exist in the F2 domain. The two operations must
not be interchanged when discussing this test.

## 4. What the sigma approximately 0.99 result establishes

The primary 1G-E/1G-F variance uses the F volume-weighted **grain-radius
shape**, **externally supplied tracker f_v0**, and overlapping empty Boolean
grains. These grains are not the disjoint F population. Its
calculation never uses the radius-cut M3 cumulative as its normalization.
F2 therefore does not, by itself, change the previously reproduced values
0.987075 (GM) and 0.988136 (NW15) at 8 h^-1 Mpc in the photon frame.
Those values are inherited evidence, not a newly rerun variance/MC result
in this successor. The previous independent full F run reproduced them.

The correct description is **conditional hybrid variance**:

- the size mapping uses finite-density shell-crossing interiors (x=0.2047);
- the variance illustration sets global void contrast to -1 and supplies
  the tracker volume fraction;
- the Boolean intensity is independently calibrated: with number intensity
  lambda (inverse volume), eta=lambda*E[V_grain]=-ln(1-f_v0) is dimensionless.
  Eta is the summed grain volume per domain volume, not the covered fraction.
  It is 1.33560 / 0.98618, or 1.776 / 1.311 times F's full 0.751969.
  Conditional on coverage, the mean multiplicity is eta/f_v0=1.812 / 1.573;
- M3 retains 61.7% of the primary mass in walls at 2.49 times the global
  density; the empty Boolean surrogate assigns all mass to walls at
  1/(1-f_v0)=3.80 / 2.68 times the global mean;
- a derivation of the intervening evolution, geometry and mass redistribution
  is absent;
- approximately 89.1% / 90.6% of the total primary variance comes from
  the wall-internal linear field, extrapolated to fluctuations of order
  unity. This is not a fully nonlinear evolution of both phases.

Thus "self-consistent" means at most reuse of the early spectrum for the
size distribution. It does not establish one dynamically closed Timescape
population. The open-interior Milne asymptote alone does not identify
finite-mass seed voids with the tracker's exactly empty regions at finite
time. The next report derives the missing moment constraints.

## 5. Other current readings

The frozen C3 tracker-seed sensitivity uses the older wall-amplitude
normalization. The D owner-decision successor's total-delta_L definition
gives `X_SU=1.26264 / 1.28498`, not 1.295 / 1.312. Frozen C3 tables are
historical sensitivities, not the current D normalization. The primary
C1 correction here does not depend on C3. Recomputing all C3 sensitivities
is not part of this primary successor.

The D scale argument assuming dominant radii around 15 h^-1 Mpc cannot
be applied unchanged to F's median 2.4-2.8 h^-1 Mpc. Current wording:
**a global-mean linear statistic has not been constructed by this closure**.
Nonlinear amplitudes alone are not a theorem forbidding a linearly
extrapolated statistic. The owner approved `LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC = NOT_DERIVED`
on 2026-10-02 in the registered D successor. This replaces the earlier
wording-only treatment and its `NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY`
value, while preserving the historical records and all `NOT_GRANTED` gates.

## 5.1 Complete frozen-to-current supersession map (FGA-F1)

The following readings explicitly supersede frozen F §§1, 5, 8.2, 9, 12
and the proposed classifications of §13. None of those historical files
is edited. Radii below are photon-comoving h^-1 Mpc; cutoff values are the
inherited-grid diagnostics, rounded to avoid false precision.

| Frozen location / claim | Frozen reading | Current reading |
|---|---|---|
| §1 item 2 (verdict 2); §5 "Milne limit" paragraph | Same objects at different stages; jointly derived identification | Milne-rate asymptote `DERIVED_FROM_VERIFIED_DEFINITIONS`; finite-mass seeds = exactly empty finite-time tracker voids `NOT_DERIVED` (owner confirmation 2026-10-02) |
| §1 items 4–6; §8.2 primary large-void fill | F3 cuts interpreted as cumulative volumes, approximately 4% at >=10 | F2 fixed denominator, 1.48% / 1.92% at >=10; full fraction remains 0.751969 |
| §8.2 primary r_min matching present tracker | 0.51 / 1.95 | F2 approximately 0.35 / 1.23; old values remain F3 truncated-universe cutoffs |
| §1 item 5; §8.2 near-empty (C1, ρ_v/ρ_w = 0.1, 0.05) r_min column | 0.06–0.8 | F2 approximately 0.019–0.39; detailed cases below |
| §9 history, >=1 at z=3 | GM approximately 0.013 (NW15 approximately 0.011) | F2 GM approximately 0.0052 (NW15 approximately 0.0044) |
| §1/§12 synthesis and Reading; §13 proposed F classifications | Shared early spectrum treated as self-consistent variance closure | Conditional hybrid: shared radius shape, separately calibrated overlapping Boolean grains, tracker coverage and extrapolated linear wall field |
| §1 item 4 (PBS bullet); §8.2 "The dominant voids": original 1G-D PBS clocks (f_vi = 10⁻², 10⁻⁴), shell-crossing barrier, voids >=10 | 62–73% | F2 49–71% (historical C3 sensitivity; see the note below) |
| §8.2 "The dominant voids": the same PBS clocks at ρ_v = 0.1 ρ_w, voids >=10 | 40–68% | F2 20–54% (historical C3 sensitivity) |
| §8.2 "The dominant voids": C1, C2 (comoving, Mészáros) or C3 tracker seed, voids >=10 | <= 10% | F2 <= 4.3% (maximum: C3 tracker seed, [GM], shell crossing) |
| All archived `M3_two_scale_volume_budget` radius cuts, including C2/C3 and turnaround | Cut-dependent F3 normalization | F2 corrections available for all 84 archived populations, retaining each scenario's old clock |
| All archived `M3_r_min_h_inv_Mpc_reproducing`, including C2/C3 and turnaround | Frozen F3 cutoffs | Valid only under the F3 truncated-universe meaning. F2 cutoffs not supplied except for the explicitly recomputed C1/collapse cases; do not reuse old r_min as F2 |

**Note on the three [W09]-comparison rows** (added 2026-10-06, R2-N2 of
`phase1g_fg_remediation_independent_audit.md`).

- **Source of the values.** They are the archived F2 corrections at z = 0
  for both parameter sets ([GM], [NW15]). They use the collapse threshold
  δ_c = 1.686, the threshold of frozen §8.2.
  - The values are taken from the regenerated archive
    `reports/phase1g_fg_remediation_audit_evidence/r2_archived_headlines_out.json`
    (method R2-M6).
  - They equal F2 applied to the frozen artifact's mass fractions, each
    population with its own clock and interior density x (0.2047 at shell
    crossing, 0.1 near-empty).
- **Ranges, F3 → F2:**
  - PBS at shell crossing: 0.620–0.734 → 0.492–0.709;
  - PBS at x = 0.1: 0.401–0.675 → 0.195–0.536;
  - C1/C2/C3 tracker seed: maximum 0.098 → 0.043.
- **Scope of the <= 4.3% row.** It holds for the collapse threshold of
  frozen §8.2. The turnaround threshold (δ_c = 1.062), outside that claim,
  would give a maximum F2 of 5.05% (F3 9.74%).
- **What the PBS rows rest on.** They use the original 1G-D PBS response
  and the older wall-amplitude C3 normalization, which the 1G-D audit and
  owner decisions superseded. They are historical sensitivities, not
  current Timescape readings.
- **Status.** All rows remain conditional, model-internal M3 two-density
  budgets in photon-comoving radii. They are not observational predictions
  or exclusions, and do not test [W09]'s 40–50% observationally.

No proposed F API token is introduced. The existing finite-density versus
exact-vacuum mismatch is not resolved by renaming the verdict.

| Case | interior x | frozen F3 cutoff | corrected F2 cutoff | F2 fraction >=1 |
|---|---:|---:|---:|---:|
| GM | 0.10 | 0.18769 | 0.09400 | 0.30406 |
| GM | 0.05 | 0.06198 | 0.01878 | 0.04549 |
| NW15 | 0.10 | 0.80955 | 0.39356 | 0.38240 |
| NW15 | 0.05 | 0.28594 | 0.09524 | 0.08216 |

The new cutoffs agree with the independent audit's CDF inversions within
0.02%; the regression budget is 0.2% for retained grid interpolation.
They are C1 common-time, collapse-barrier, present-epoch diagnostics;
the near-empty continuation is not a derived post-shell-crossing boundary law.

| z | GM F3 >=1 | GM F2 >=1 | NW15 F3 >=1 | NW15 F2 >=1 |
|---:|---:|---:|---:|---:|
| 0 | 0.69483 | 0.62426 | 0.71490 | 0.66606 |
| 0.5 | 0.55864 | 0.40408 | 0.58819 | 0.44424 |
| 1 | 0.38257 | 0.22103 | 0.40341 | 0.23876 |
| 2 | 0.10187 | 0.04456 | 0.09922 | 0.04330 |
| 3 | 0.01293 | 0.00525 | 0.01081 | 0.00438 |

Twelve archived rows have `unresolved_below_grid` below zero, down to
-1.72e-7. This is a signed quadrature residual (grid overshoot), not
negative physical mass. Values remain visible, unclipped and unrenormalized.

## 6. Reproduction and integration status

```bash
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 python -B -W error scripts/phase1g_f_volume_budget_successor_numerics.py
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 python -B -W error -m pytest -q tests/test_phase1g_f_volume_budget_successor.py
```

The script writes `artifacts/independent/phase1g_f_volume_budget_successor.json`.
Passing `--frozen-artifact artifacts/independent/phase1g_f_void_population.json`
also rectifies every archived population with F2, preserving its original
clock, barrier and density, and records the input SHA-256. The delivered
evidence includes all 84 such populations (42 per parameter case). This
optional step does not rerun the frozen Monte Carlo or update historical
C3 normalization; primary C1 histories are recomputed independently.
The successor implements F1-F3 in a validated immutable record, keeps the
two cumulative meanings under distinct keys, and uses the existing portable
resource shim to load the frozen script on Windows. Tests cover physical
volume accounting, additivity, unit rescaling, normalization, limits,
invalid inputs, published threshold values and the two-epoch mismatch.
All tolerances appear in test arguments or the inherited script.

See `phase1g_fg_successor_validation.md` for observed validation, preserved
file hashes, environment limitations and packaging. The companion
inventory records the base and scope. The original successor was audited on 2026-10-02 with corrections required.
The remediated revision received an independent delta audit on 2026-10-06
(`phase1g_fg_remediation_independent_audit.md`; no integration blocker).
Its residual R2-N1–N3 corrections and the phase-branch integration are
recorded in `phase1g_fg_remediation_integration.md`. It is not frozen, and
no tag, merge or release is implied.

## Windows reproduction and evidence identity

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH = "src"
$env:OPENBLAS_NUM_THREADS = "1"
.\.venv\Scripts\python.exe -B -W error scripts/phase1g_f_volume_budget_successor_numerics.py --frozen-artifact artifacts/independent/phase1g_f_void_population.json
```

Use `.venv311` for the second interpreter. JSON is now written as UTF-8
bytes with LF on all platforms. Raw SHA-256 identifies one exact run;
it is not a cross-platform numerical-equivalence gate. Compare numeric
leaves with rtol=1e-11, atol=1e-14, ignoring environment and raw provenance
hash fields, and compare scientific labels and keys exactly. This budget
allows floating-point library differences; it is separate from the much
larger F radius-grid accuracy error. The inventory records the run's
environment, raw hash and these tolerances.

## References

- [JLH13] Jennings, Li & Hu, MNRAS 434, 2167 (2013),
  https://arxiv.org/abs/1304.6087, Eqs. (6)-(7), (13)-(17), (A8)-(A12).
- [SvdW04] Sheth & van de Weygaert, MNRAS 350, 517 (2004),
  https://arxiv.org/abs/astro-ph/0311260, Eqs. (3), (C8).
- Frozen `phase1g_f_void_population.md`, and D/E owner-decision successor
  reports. Source formulas are distinguished above from new deductions.
