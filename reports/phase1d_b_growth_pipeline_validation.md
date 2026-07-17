# Phase 1D-B — Growth-pipeline implementation and validation

Date: 2026-07-17

Branch: `phase-1d-b-growth-pipeline`

Starting/verified HEAD: `878a97e83357025c78e2fee7bf458c3b22a207d3`
(= tag `phase-1d-a-growth-observable-audit-v1`)

Scientific specification: `reports/phase1d_a_growth_observable_audit.md`
and `reports/phase1d_a_observable_inventory.json` (both read completely
before design); underlying sources cited there as [GM] (arXiv:2511.17160v2)
and [W09] (arXiv:0909.0749).

## 1. Scope and explicit exclusions

Implemented: signed relative growth histories; exact analytic bare and
dressed growth rates; bare and dressed non-logarithmic derivatives;
optional solver-harmonic `delta_m` coefficients; zero-crossing detection
with bracket-preserving numerical root refinement; maximal piecewise
validity intervals; mandatory-explicit scenario validation; solver and
root convergence validation; machine-readable provenance/validation
output.

**Not implemented, not even as placeholders:** matter power spectra,
transfer functions, primordial spectra, σ_R, σ_8, anchored or unanchored
fσ8, any "fσ8-shaped" diagnostic, spectral or window-weighted growth, RSD
or Kaiser mappings, galaxy bias, peculiar-velocity observables,
Alcock–Paczynski or fiducial conversions, datasets, covariances,
likelihoods, fitting, parameter inference, author communication.  The
Phase 1D-A fields for spectrum models, normalisation strategies, and
sigma-radius h conventions were **not** added to any executable API; they
remain documented future blockers.  D2 remains forensic-only: no
D2-corrupted quantity, fallback, switch, or hidden path exists in the
scientific package (tested).

## 2. Preflight and repository preservation

| check | result |
|---|---|
| branch `phase-1d-b-growth-pipeline` | ✓ |
| HEAD `878a97e83357025c78e2fee7bf458c3b22a207d3` | ✓ |
| tag `phase-1d-a-growth-observable-audit-v1` → HEAD | ✓ |
| earlier frozen tags resolve and are ancestors (`phase-1b-background-v1` → `fe8b00f`, `phase-1c-a-equation-audit-v1` → `5d9aa47`, `phase-1c-b1-clean-systems-v1` → `18b6666`, `phase-1c-b2-barotropic-v1` → `9ec3bcc`) | ✓ all ancestors |
| working tree and index clean | ✓ |
| upstream clone at `590c6fd5332acb15f5683ebf392a0d7ce54983c5`, clean | ✓ (unchanged after the work) |
| notebook SHA-256 `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a` | ✓ (unchanged after the work) |
| complete pre-implementation suite | 268 passed |

No frozen Phase 1B/1C scientific equation, solver, test, report, figure,
upstream file, or generated B1/B2 artifact was modified.  The frozen
perturbation solver layer needed **no change**: dense output for root
refinement is obtained by re-integrating the identical frozen public RHS
functions inside the growth layer (Sec. 11), so the "solver-layer changes
only when technically necessary" clause was never invoked.

## 3. Implementation inventory

New public growth layer `src/timescape_fsigma8/growth/` following the
suggested module split exactly:

| module | responsibility |
|---|---|
| `scenarios.py` | enums with the exact required labels; immutable `GrowthScenario` (no defaults, applicability validation); `GrowthReference`; explicit numerics records (`GrowthNumericsConfig`, `DenseSolveConfig`, `RootRefineConfig`); preset resolution to the frozen Phase 1B parametrisations |
| `histories.py` | generic dust-mode extraction with explicit system labels and the Mészáros `Z = -y[1]` sign; frozen-solver sampled histories with complete metadata; frozen epoch/IC resolution; enum bridging to the frozen Phase 1C types |
| `rates.py` | exact analytic `f_bare`, `f_dressed`, `dDelta_d/d ln a_D`, `dDelta_d/d ln a_obs`, chain factor; scale-free near-zero policy; NaN-masked logarithmic rates (never ±inf) |
| `crossings.py` | strict sign-change scan with preserved brackets; dense re-integration of the frozen RHS (`dense_output=True`); bracket-preserving Brent refinement with residual gate; endpoint-root handling; maximal validity intervals with explicit open/closed semantics |
| `mapping.py` | pure solver-harmonic `delta_m = -Delta_d/k_code²` conversion; `HarmonicMetadata` with the single supported negative-Laplacian sign convention; volume-average `k_com_D`/`k_phys0_D` metadata only (no `k_com_obs` invented) |
| `pipeline.py` | orchestration; explicit reference resolution; signed relative growth; per-interval rate serialization (never joined across a pole); provenance output |

Tests: `tests/test_growth_scenarios.py`, `tests/test_growth_histories_rates.py`,
`tests/test_growth_crossings.py`, `tests/test_growth_convergence_purity.py`,
shared builders in `tests/growth_test_utils.py`.
Validation: `scripts/validate_growth_pipeline.py` →
`artifacts/independent/phase1d_b_growth_validation.json` (git-ignored).

## 4. Public API and scenario model

`GrowthScenario` requires every field explicitly (none has a default):
`perturbation_system` ∈ {meszaros, comoving, barotropic};
`background_preset` ∈ {paper_reference, notebook_reference};
`d3_branch` ∈ {not_applicable, printed_4_15, derived_4_10};
`tilt_form` ∈ {not_applicable, unrescaled_V, rescaled_Vtilde};
`rate_unit_convention` ∈ {upstream_unconverted, lcdm_to_timescape_converted}
(the frozen Phase 1C enum, reused);
`epoch_choice` ∈ {upstream_0p218_gyr, dressed_z20} (frozen enum, reused);
`wavenumber_convention` ∈ {not_applicable, upstream_timescape_k, paper_lcdm_hubble_k};
`growth_coordinate` ∈ {bare_aD, dressed_redshift};
`density_contrast_mapping` ∈ {keep_Delta_d, map_to_delta_m_via_minus_k_code2};
plus `supplied_mode_k`/`mode_label`.

Validated rejections (tested): a real D3 branch, tilt form, or wavenumber
convention on a clean system; `not_applicable` D3/tilt/wavenumber on
barotropic; density mapping without explicit harmonic metadata; nonfinite
or zero `k_code`; mode metadata without the mapping on clean systems;
string lookalikes for every enum; reference epochs outside the integrated
solution; references at or numerically indistinguishable from a crossing.
Inconsistent combinations raise; nothing is silently corrected.  Neither
D3 branch is called canonical, preferred, physical, corrected,
recommended, intended, or a default anywhere.

## 5. Scientific equation map

Every public rate function cites its chain ([GM]/[W09]/1D-A):

```text
Delta_d,k = -k_code² delta_m,k          1D-A (D1b-code); [GM] (2.19)-(2.20), fn. 8
Z = -dDelta_d/dt                        [GM] (4.14)
d ln a_D/dt = Theta/3                   [GM] (3.6); Phase 1B tracker
f_bare = -3 Z/(Theta Delta_d)           1D-A (D4), exact
f_dressed = f_bare (2+f_v)²/(4+f_v+4f_v²)   1D-A (D3), exact tracker
a_obs = 1/(1+z_dressed) = a_w/a_w0      [GM] p. 25; [W09] (38)
dDelta_d/d ln a_D = -3Z/Theta           finite through crossings
dDelta_d/d ln a_obs = (-3Z/Theta)(2+f_v)²/(4+f_v+4f_v²)
delta_m = -Delta_d/k_code²  ⇒  d delta_m/d ln a_D = +3Z/(Theta k_code²)
```

No finite differences, gradients, splines, or fits implement any primary
rate; the only finite-difference calculation is a clearly labelled
low-priority cross-check inside one validation test.

## 6. Reference-epoch policy

`GrowthReference` states the coordinate (`bare_time_solver_units` or
`dressed_redshift`), the value, explicit Brent root controls for the
dressed→bare conversion (via the validated Phase 1B `redshift`), and the
explicit crossing tolerance.  There is no default reference (not the
initial epoch, not today, not z=0).  At the resolved reference the
amplitude is evaluated on the documented dense continuous solution and
rejected if (i) exactly zero, (ii) its linearised distance to the nearest
zero, |Δ_d|/|Z| (exact, since Z = −Δ̇_d), is at or below
`amplitude_floor_rel` × integrated span, or (iii) any refined Δ_d root
lies within that time tolerance.  Resolved references store bare solver
time, Gyr, dressed redshift, a_D, and a_obs.  Validation runs use dressed
z = 10 as an explicit *validation* choice, recorded as such.

## 7. Relative-growth definitions

`G_Delta(t;t_ref) = Delta_d(t)/Delta_d(t_ref)` — a signed ratio; no
logarithm is used in its construction.  `G_m(t;t_ref)` is defined through
the mapped coefficient and equals `G_Delta` identically (constant
harmonic factor cancels); measured agreement ≤ 1.9e−16 relative (gate
1e−14).

## 8. Optional `delta_m` coefficient mapping

`map_to_delta_m_via_minus_k_code2` is a pure conversion:
`delta_m = -Delta_d/k_code²` with mandatory `HarmonicMetadata` (mode
label, resolved `k_code`, wavenumber convention, sign convention).  The
only supported sign value is the documented negative-Laplacian eigenvalue
convention; no other sign is accepted.  Volume-average metadata repeats
the 1D-A (D1c) relations only (`k_com_D = k_code` in H0_TS/c units,
`k_phys0_D = k_code/a_D0`); **no observational/dressed `k_com_obs` is
computed or invented**.  The mapping never reruns or alters a solution.
Clean systems accept a per-mode coefficient only with an explicitly
supplied nonzero `k_code`; the metadata changes the absolute coefficient
but provably not the relative history or rate (V6: bit-identical).

## 9. Analytic bare and dressed rates

Vectorised, from the state variable Z and the validated background Θ and
f_v only.  At amplitude roots the logarithmic rates are NaN under the
explicit scale-free near-zero mask with crossing metadata alongside —
never ±inf and never an interpolated finite value.  Measured identity
errors (V2, gate 1e−11): `f_bare·D = dD/d ln a_D` ≤ 2.9e−16;
`f_dressed·D = dD/d ln a_obs` ≤ 3.9e−16; chain-factor identity
`f_dressed/f_bare = (2+f_v)²/(4+f_v+4f_v²)` ≤ 2.1e−16 (gate 1e−12).

## 10. Non-logarithmic derivatives

`dDelta_d/d ln a_D = -3Z/Θ` and its dressed counterpart are exposed
everywhere and verified finite through every Δ_d crossing (tested at the
masked samples of crossing trajectories).  Mapped derivatives obey the
−1/k_code² factor exactly (V2: 0.0 measured deviation).

## 11. Root-refinement method and numerical controls

Continuous representation: a dense re-integration of the **identical
frozen RHS** (`meszaros_rhs`, `comoving_rhs`, `barotropic_rhs`) with
`dense_output=True`, explicit `DenseSolveConfig(method=DOP853,
rtol=1e−11, atol=1e−13, max_step=inf, first_step=None)`.  Refinement:
`scipy.optimize.brentq` on the dense component within the preserved
sampled bracket, `RootRefineConfig(xtol=1e−13, rtol=8.9e−16, maxiter=100,
residual_scale_gate=1e−6)` — all immutable explicit configuration.  Each
refined root is verified inside its original bracket; the dense-component
residual is recorded and gated; a dense/sampled sign disagreement raises
instead of being repaired.  Near-zero policy: a sample is flagged iff
exactly zero or ≤ `near_zero_rel_floor` (1e−9) times the larger
neighbouring magnitude — scale-free across the ~10¹⁴ dynamic range;
flagged samples are never promoted to solver-independent roots; endpoint
near-zeros are reported separately as endpoint roots.  The frozen Phase
1D-A locations were used only as brackets to check against, never copied
as roots.

## 12. Refined root table (baseline scenario, notebook preset, upstream conventions, unrescaled_V, tight DOP853, n=1000)

| branch | k | component | t_root (code) | Gyr | z_dressed | a_D | a_obs | residual/scale |
|---|---|---|---|---|---|---|---|---|
| printed_4_15 | 5π | Δ_d | 0.228538312270 | 3.051547 | 2.409726 | 0.345684 | 0.293279 | 1.5e−12 |
| printed_4_15 | 5π | Z | 0.140771268152 | 1.879641 | 3.732965 | 0.238238 | 0.211284 | 4.3e−12 |
| printed_4_15 | 10π | Δ_d | 0.078174785384 | 1.043825 | 5.984064 | 0.154625 | 0.143183 | 9.9e−14 |
| printed_4_15 | 10π | Z | 0.057330252630 | 0.765499 | 7.562793 | 0.123933 | 0.116784 | 2.9e−15 |
| derived_4_10 | 2π | Δ_d | 0.785161573556 | 10.483832 | 0.369650 | 0.969746 | 0.730114 | 1.4e−14 |
| derived_4_10 | 2π | Z | 0.339400981303 | 4.531835 | 1.583578 | 0.474598 | 0.387060 | 2.6e−14 |
| derived_4_10 | 5π | Δ_d | 0.150938581970 | 2.015400 | 3.517382 | 0.251099 | 0.221367 | 2.8e−15 |
| derived_4_10 | 5π | Z | 0.097730111193 | 1.304937 | 5.028908 | 0.181801 | 0.165868 | 3.0e−11 |
| derived_4_10 | 10π | Δ_d | 0.067714608132 | 0.904156 | 6.675729 | 0.139496 | 0.130281 | 6.8e−14 |
| derived_4_10 | 10π | Z | 0.050550481782 | 0.674973 | 8.300787 | 0.113406 | 0.107518 | 6.5e−15 |

Every refined root lies strictly inside its frozen Phase 1D-A
sampled-grid bracket, is not a bracket sample, converged in Brent
iteration, and satisfies the residual gate.  `printed_4_15|2π` has no
sampled crossing, matching the frozen expectation.  No additional roots
were found.  Root uncertainty diagnostic: 1e−13 code units (xtol-level).

## 13. Piecewise validity intervals

For each crossing trajectory: two maximal intervals, closed at the
integration endpoints, open at the refined Δ_d root; each records solver
time, Gyr, dressed redshift, amplitude sign, its sample-index range, and
whether the explicit reference belongs to it.  Example
(`derived_4_10|2π`): [0.016327, 0.785162) sign +1 containing the z=10
reference; (0.785162, 1.151613] sign −1.  Z roots do not split intervals;
they are exposed as stationary points where f passes through zero
(tested).  Serialization emits logarithmic rates strictly per interval —
arrays are never joined across a pole (tested).

## 14. Clean-system results

Mészáros and comoving baselines (upstream-compatible conventions): zero
Δ_d/Z crossings, a single closed validity interval containing the
reference, f defined globally.  End-of-history rates (notebook preset):
f_bare(t0) ≈ 0.3103 (Mészáros); the comoving history gives its own f
via the identical exact expression.  The Mészáros system remains a
mathematical comparison system: nothing here claims physical validity for
Timescape ([GM] p. 26 states the approximation should not be applicable).

## 15. Both D3 branches side by side

All quantities above are reported for `printed_4_15` and `derived_4_10`
under identical scenarios (root table, intervals, one-factor D3 study:
endpoint relative growth +4.73 vs −6.16 at 2π, a −230 % delta; crossing
patterns per branch as in Sec. 12).  Neither branch is ranked; the
difference is an unresolved-convention spread (Sec. 22).

## 16. Tilt-form equivalence

`printed_4_15|5π` with `unrescaled_V` vs `rescaled_Vtilde` (identical
corrected physics): history normalized-Linf 3.9e−11 (gate 1e−8); root
time differences ≤ 1.6e−12 code units (gate 1e−8); worst f_bare relative
difference 4.6e−9; non-logarithmic derivatives agree at the same level.
Both labels are retained in the output metadata (tested).

## 17. Solver convergence

Independent high-accuracy reference: DOP853 with rtol=2e−13, atol=2e−15,
every option explicit.  Per component and derived quantity (Δ_d, Z,
relative growth, dD/d ln a_D) the study reports max-abs, normalized-Linf
(documented denominator: global max |reference| per array — relative
error is never taken at a true zero), RMS, worst-discrepancy time, and a
near-crossing flag.  Worst normalized-Linf per scenario (gate 2e−8):

| scenario | tight_DOP853 | tight_RK45 | tight_Radau |
|---|---|---|---|
| meszaros | 7.1e−12 | 2.2e−10 | 2.9e−11 |
| comoving | 8.3e−12 | 2.3e−10 | 3.2e−11 |
| printed_4_15\|2π | 1.0e−11 | 1.4e−10 | 3.6e−11 |
| derived_4_10\|10π | 3.4e−10 | 3.1e−09 | 2.6e−11 |

## 18. Root convergence

For every baseline barotropic root: two solver methods (tight DOP853,
tight Radau) × three sampling densities (600, 1000 — the existing
~1000-point convention — and 2000).  Gate, declared before the study and
not relaxed: spread ≤ 1e−8 code time (justification recorded in the
artifact: brentq xtol=1e−13 on a dense rtol=1e−11 representation).
Measured spreads: ≤ 2.2e−14 code time across all six method/grid
combinations for every root; dressed-z spreads ≤ 1.6e−12; every refined
root is demonstrably not the left bracket sample (distance ≫ the
uncertainty diagnostic); residuals as in Sec. 12.

**What V4 demonstrates and what it does not.** V4 establishes
sampling-grid convergence (the refined root is stable as the sampled grid
is refined 600 → 1000 → 2000), sampled-bracket robustness (the refined
root is insensitive to which sampled pair brackets it), and
reproducibility of the Brent refinement on one fixed dense DOP853
continuous representation.  V4 alone does **not** measure cross-method
root agreement: for each root the DOP853 and Radau sampled rows refine
against the *same* dense DOP853 representation (the fixed
`DenseSolveConfig` used for every run), so their root values coincide by
construction rather than as an independent cross-method check.

**Independent corroboration (separate from V4, not part of it).** The
Phase 1D-B compliance audit reproduced all ten production roots by an
independent path — `scipy.integrate.solve_ivp` event detection under
Radau and under LSODA, each integrator using its own local continuous
interpolation for the event root (not the growth layer's dense DOP853
solution and not brentq-on-dense).  Worst absolute root-time difference
from the production roots: 9.6e−12 solver-time units; both components of
`printed_4_15|2π` returned zero events, matching the production
zero-crossing count.  This is recorded here (and in the artifact field
`independent_root_corroboration`) as corroborating evidence only; it is
not a V4 quantity.

## 19. One-factor scenario effects

From the named `validation_baseline` (label only — not an API default,
not a scientific preference): barotropic `printed_4_15`, 2π, notebook
preset, upstream conventions, `bare_aD`, `keep_Delta_d`.  One field
changed at a time (endpoint relative growth G_end; baseline
G_end = +4.7326, f_bare(t0) = 0.14661):

| factor changed alone | G_end | ΔG_end vs baseline | endpoint rate |
|---|---|---|---|
| background_preset → paper_reference | +4.7306 | −0.042 % | 0.14660 |
| rate_unit_convention → lcdm_to_timescape_converted | +4.6993 | −0.70 % | 0.14780 |
| epoch_choice → dressed_z20 | +4.6662 | −1.40 % | 0.14615 |
| growth_coordinate → dressed_redshift | +4.7326 | 0 (history unchanged) | f_dressed = 0.15895 = 1.084156 × f_bare |
| d3_branch → derived_4_10 | −6.1617 | −230.2 % | 4.3419 |
| tilt_form → rescaled_Vtilde | +4.7326 | −3e−14 % | 0.14661 |
| wavenumber_convention → paper_lcdm_hubble_k | +3.1976 | −32.4 % | −0.91992 |
| density_contrast_mapping → map_to_delta_m | +4.7326 | 0 (ratio invariant) | 0.14661 |

The growth-coordinate row confirms the exact tracker chain factor at t0
(f_dressed/f_bare = 1.084156, from the full-precision endpoint rates).
The `d3_branch → derived_4_10` row's −230.2 % is a **signed** endpoint
relative-growth difference that spans a trajectory sign reversal (baseline
G_end = +4.7326 > 0; derived_4_10 G_end = −6.1617 < 0, its trajectory
having one Δ_d root): it is a signed difference of endpoint growth, **not**
an uncertainty magnitude or error bar.  The
`wavenumber_convention → paper_lcdm_hubble_k` row likewise **flips the
sign** of the endpoint growth rate (+0.14661 → −0.91992) — a rate sign
flip, again not an uncertainty magnitude.  An envelope across these deltas
is a convention spread, not a confidence interval.

## 20. Scale-independence and scale-dependence checks

Clean systems: varying only the harmonic metadata (k_code 7 vs 13, fixed
initial mode mixture) leaves the relative growth and rates **bit-identical**
(the absolute mapped coefficient changes as −1/k_code²).  Barotropic:
relative-growth endpoints at 2π/5π/10π are +4.73/−2.6e4/−5.2e14 —
strongly k-dependent on both branches.  No physical power-spectrum scale
dependence is inferred from this deterministic three-mode normalisation.

## 21. Test results per environment

Complete suite (all phases + 69 new growth tests), no regressions:

| environment | versions | result |
|---|---|---|
| Python 3.14 (.venv) | CPython 3.14.3, NumPy 2.5.1, SciPy 1.18.0 | **337 passed** |
| Python 3.11 (.venv311) | CPython 3.11.9, NumPy 2.4.6, SciPy 1.17.1 | **337 passed** |

Pre-implementation baseline: 268 passed (both environments previously
validated).  The 35 required coverage areas of the task specification are
mapped onto the four new test modules; regression protection is the full
suite itself.

## 22. Uncertainty taxonomy

Reported separately, never merged:

1. **Numerical sampling/root uncertainty:** V4 spreads across sampling
   densities at fixed solver (≤ 2.2e−14 code time); per-root uncertainty
   diagnostic xtol + rtol·|root| ≈ 1e−13.
2. **Solver method/tolerance uncertainty:** V3 normalized-Linf deltas
   against the independent DOP853 2e−13/2e−15 reference (≤ 3.1e−9).
   V4 is **not** a cross-method measurement (Sec. 18: the DOP853 and
   Radau rows refine against the same dense DOP853 representation);
   genuine cross-method root corroboration comes from the independent
   Radau/LSODA event-detection reproduction recorded in Sec. 18.
3. **Unresolved-convention spread:** V7 one-factor deltas (D3 branch
   −230 %, k convention −32 %, epoch −1.4 %, rate units −0.70 %, preset
   −0.042 %, coordinate ×1.084 on f).  This spread is a convention
   spread and is not a statistical confidence interval.
4. **Model/closure dependence:** Mészáros vs comoving vs barotropic
   differences (V1/V6); the Mészáros system is a mathematical comparison
   system only.

No spectrum-normalisation category exists because spectra and
normalisation are not implemented in this phase.

## 23. Explicit scientific limitations

- `Delta_d` is the CGI Laplacian density scalar, **not** the ordinary
  density contrast; mapped `delta_m` values are solver-harmonic
  coefficients only.
- Relative growth and logarithmic rates are invariant under the fixed
  harmonic conversion; absolute amplitudes, spectra, σ_R/σ_8, and
  observational k-bin comparisons still require the dimensional and
  dressed-frame mappings that remain unresolved (1D-A Secs. 10, 17).
- Growth rates are piecewise for crossing trajectories; the barotropic
  logarithmic rate has poles inside the observable window on both
  branches.
- Both D3 branches remain unresolved; every result is reported for both.
- No observational fσ8, σ_8, spectrum, or RSD quantity has been
  implemented; the corresponding readiness verdicts of 1D-A
  (NO, MISSING NORMALIZATION / NO, MISSING RSD INTERPRETATION) stand.
- D2 remains excluded from the scientific package.
- Gyr values inherit the upstream 9.778 reproduction-era conversion of
  the preset time units (documented in `scenarios.py`), consistent with
  Phases 1C-B1/B2.

## 24. Exact files changed

New files (14):

```text
src/timescape_fsigma8/growth/__init__.py
src/timescape_fsigma8/growth/scenarios.py
src/timescape_fsigma8/growth/histories.py
src/timescape_fsigma8/growth/rates.py
src/timescape_fsigma8/growth/crossings.py
src/timescape_fsigma8/growth/mapping.py
src/timescape_fsigma8/growth/pipeline.py
tests/growth_test_utils.py
tests/test_growth_scenarios.py
tests/test_growth_histories_rates.py
tests/test_growth_crossings.py
tests/test_growth_convergence_purity.py
scripts/validate_growth_pipeline.py
reports/phase1d_b_growth_pipeline_validation.md
```

Modified files (2): `CLAUDE.md`, `README.md` (Phase 1D-B discoverability
and the Sec. 23 caveat statements only; no historical report was
rewritten).  Generated (git-ignored, untracked):
`artifacts/independent/phase1d_b_growth_validation.json`.  No frozen
file, upstream file, or B1/B2 artifact was modified; no enum value or
scenario label was renamed.

## 25. Readiness assessment for the next phase

The growth layer delivers everything the 1D-A GO-list items 1–3 permit:
per-mode signed growth histories, exact analytic piecewise rates in both
explicit coordinates, and the pure harmonic mapping layer.  All declared
gates passed with margins of 10³–10⁷.  Remaining blockers for any
σ_8/fσ8-facing phase are unchanged from 1D-A Sec. 17 (external spectrum
+ normalisation; continuous k-domain; volume-average→dressed comoving
map; dressed redshift-space mapping; D3/F3/F4/F7/h/coordinate convention
resolutions).  The work is ready for human review; nothing has been
committed, tagged, or pushed.
