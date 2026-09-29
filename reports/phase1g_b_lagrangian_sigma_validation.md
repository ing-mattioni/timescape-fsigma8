# Phase 1G-B — conditional, mass-labelled linear σ(M): validation

Classification of every output: `CONDITIONAL_MODEL_INTERNAL_LINEAR_SIGMA_M`,
`NON_OBSERVATIONAL`, `NOT_OBSERVATIONAL_SIGMA_8`, `NOT_FSIGMA8`; the early
spectrum is a `PROVISIONAL_MODEL_IMPORT` and the radius identification is
`CONVENTION_DEPENDENT`. Nothing here is an observational σ8, and no comparison
with survey or CMB amplitude values is made or authorised.

References: [GM] Galoppo & Mourier, arXiv:2511.17160v2 (JCAP 02 (2026) 066);
[W09] Wiltshire, arXiv:0909.0749v2; [NW15] Nazer & Wiltshire,
arXiv:1410.3470; [EH98] Eisenstein & Hu, ApJ 496, 605, astro-ph/9709112;
[P18] Planck 2018 VI, arXiv:1807.06209; [1G-A]
[`phase1g_a_sigma8_derivation_path_audit.md`](phase1g_a_sigma8_derivation_path_audit.md).

## 1. Scope, authorisation and checkpoint

- **Authorisation.** On 2026-09-29 the project owner approved "let a
  sub-agent perform Phase 1G-B", i.e. recommendation 2 of [1G-A] Sec. 10: a
  package module for the conditional, model-internal, mass-labelled linear
  σ(M) of the comoving closure, with the Mészáros approximation as
  comparator. During the phase the lead added a second, explicit growth-law
  option (the wall-regional EdS law of [1G-A] Sec. 8; Sec. 5 below).
- **Parent checkpoint:** `462121c` (Phase 1G-A). Branch
  `phase-1g-b-lagrangian-sigma` (local, unpushed, untagged).
- **Implementation commit:** `0883814` (module, tests, validation driver).
  This report is committed on top of it.
- **What does not change.** `SIGMA8_AUTHORIZATION`, `FSIGMA8_AUTHORIZATION`,
  `OBSERVATIONAL_AUTHORIZATION` and `UNIQUE_TIMESCAPE_PREDICTION` stay
  `NOT_GRANTED`; `scientific_status.py` is not edited. No existing module,
  test, equation, tolerance or frozen report is edited (Sec. 13).

## 2. Files

| File | Content |
|---|---|
| `src/timescape_fsigma8/lagrangian_sigma.py` (new) | the Phase 1G-B module |
| `tests/test_phase1g_b_lagrangian_sigma.py` (new) | 92 tests (Sec. 10) |
| `scripts/validate_phase1g_b_lagrangian_sigma.py` (new) | validation driver, 21 gates |
| `artifacts/independent/phase1g_b_lagrangian_sigma.json` | generated, git-ignored |
| this report | validation record |

The module sits in its own file one layer below `perturbations/`, not in
`growth/` (the suggested location). Reason: the frozen Phase 1D-B test
`tests/test_growth_convergence_purity.py::test_growth_package_exposes_no_forbidden_observable_api`
forbids any def/class in `growth/*.py` whose name contains `sigma_r`,
`transfer_function`, `primordial` or `power_spectrum`, and the `growth`
package docstring states that no transfer function or σ_R is implemented
there. Adding the module to `growth/` would have required editing that
firewall test or evading it by naming. It imports only `background`,
`perturbations.growing_mode`, `perturbations.initial_conditions` and
`presets`; nothing imports it.

## 3. Public API

Every function argument is keyword-only and mandatory; every dataclass is
`@dataclass(frozen=True, kw_only=True)` with no field default, validated in
`__post_init__`, and raises `LagrangianSigmaContractError` (contracts),
`BarotropicClosureRefusedError` (subclass) or `LagrangianSigmaNumericalError`
(declared budgets and identities). Inapplicable choices take the explicit
value `NOT_APPLICABLE`.

| Kind | Names |
|---|---|
| Enums | `GrowthLaw` {`VOLUME_AVERAGE_CGI`, `WALL_REGIONAL_EDS_COMMON_TIME`}; `EarlyTransferModel` {`EH98_ZERO_BARYON_OSCILLATION`}; `LagrangianRadiusConvention` {`EQUAL_LAGRANGIAN_MASS_TO_REFERENCE`, `DRESSED_WALL_COMOVING_LENGTH`, `BARE_VOLUME_AVERAGE_PROPER_LENGTH`, `EXPLICIT_PHOTON_NORMALISED_RADIUS`} |
| Inputs | `TimescapeTrackerInput` (f_v0, dressed H0 in km/s/Mpc, label, source; `from_reference_preset(preset=...)`); `EarlySpectrumImport` (A_s, n_s, k_pivot, baryon fraction, T_cmb, transfer model, provenance, `import_status` that must be passed as `PROVISIONAL_MODEL_IMPORT`); `LagrangianRadiusSpec` |
| Numerics | `VolumeAverageGrowthNumerics`, `WallRegionalGrowthChecks`, `LagrangianSigmaQuadrature`; named reference instances `VOLUME_AVERAGE_GROWTH_REFERENCE_NUMERICS`, `WALL_REGIONAL_GROWTH_REFERENCE_CHECKS`, `LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE` (passed explicitly, never defaults) |
| Functions | `top_hat_window`, `eh98_zero_baryon_transfer`, `matter_era_linear_amplitude`, `timescape_growth_factor`, `early_matter_density_per_photon`, `resolve_lagrangian_radius`, `conditional_lagrangian_linear_sigma`, `lcdm_reference_linear_sigma`, `anchor_lagrangian_sigma` |
| Results | `TimescapeGrowthFactor`, `EarlyMatterDensityPerPhoton`, `ResolvedLagrangianRadius`, `ConditionalLagrangianSigma`, `LCDMReferenceLinearSigma`, `AnchoredLagrangianSigmaRatio` (each with `to_json_dict()`) |
| Status constants | `SCIENTIFIC_CLASSIFICATION`, `OBSERVATIONAL_STATUS = "NON_OBSERVATIONAL"`, `SIGMA8_STATUS = "NOT_OBSERVATIONAL_SIGMA_8"`, `FSIGMA8_STATUS = "NOT_FSIGMA8"`, `EARLY_SPECTRUM_IMPORT_STATUS`, `RADIUS_CONVENTION_STATUS`, `VOLUME_AVERAGE_CGI_EVIDENCE_CLASS`, `WALL_REGIONAL_EVIDENCE_CLASS` |

**Contracts worth naming:**
- The barotropic closure (`GrowthSystem.BAROTROPIC`, or the string
  `"barotropic"` in any letter case) is refused under both growth laws with a message citing
  [1G-A] Sec. 4.1 (Hadamard ill-posed for c²_s,eff < 0, no finite linear σ).
- `VOLUME_AVERAGE_CGI` requires a `CleanPerturbationSystem` and
  `VolumeAverageGrowthNumerics`; `WALL_REGIONAL_EDS_COMMON_TIME` requires
  `closure=NOT_APPLICABLE` and `WallRegionalGrowthChecks`.
- Every result record re-checks its status fields and refuses relabelling;
  `linear_sigma` must equal growth × unit-growth σ; the density record must
  be for the *same* background object.
- `anchor_lagrangian_sigma` requires the same quadrature configuration, the
  same transfer model and the same T_cmb (the photon normalisation), and,
  for the equal-mass convention, that the reference (ω_ref, R_ref) *is* the
  ΛCDM reference (relative 1e-12). It fails closed if
  |σ_ΛCDM/anchor − 1| exceeds the explicit tolerance, whose rationale is a
  mandatory argument. Other early-spectrum differences (A_s, n_s, k_pivot,
  f_b) are allowed and recorded by name.
- The module ships no anchor, no Planck parameter set and no survey value;
  those are explicit caller inputs (here: test fixtures and driver
  constants).
- Naming (1D-C §19): no public function/class/member name and no output key
  contains `sigma_8`, `sigma8` or `8hMpc`. They occur only inside the two
  negative status values `NOT_OBSERVATIONAL_SIGMA_8` and `NOT_FSIGMA8` (the
  latter as in `transfer.h1_realization`). The "8" of a radius is always an
  explicit `length_h_inverse_Mpc` argument.

## 4. Equations and sources

| # | Equation | Source |
|---|---|---|
| (1) | σ²(R) = ∫ dln k Δ²(k) W²(kR) | standard; [1G-A] Sec. 7 |
| (2) | g_TS = exp ∫_{t_e}^{t0} (u − tΘ/3) d ln t, u = t dlnΔ_d/dt on the regular growing mode | [GM] (4.21)–(4.23) / (4.27), (3.6); `perturbations.growing_mode`; [1G-A] Sec. 5.1–5.2 |
| (3) | g_wall = (1 − f_v0)^{1/3}; D0 = γ_w0 g = ½(2+f_v0)(1−f_v0)^{1/3} | [1G-A] Secs. 5.3, 8; [GM] (5.1), (5.4); [W09] e-print lines 1763–1764 |
| (—) | D0 = γ_w0 g, γ_w = 1 + f_v/2, 1+z = a_w0/a_w, a_w = a_D/γ_w | [GM] (5.4), text p. 25; [1G-A] Sec. 5.1 |
| (4) | ω_m,eff = ⟨ρ⟩_D0 γ_w0³/ρ_crit(100) = ½(1−f_v0)(2+f_v0)(H_D0/100)² | [GM] p. 25; [1G-A] Sec. 6.2 |
| (5) | Δ²(k) = (4/25) A_s (k/k_p)^{n_s−1} (k c/100)⁴ T²(k) D0²/ω_m² | matter-era Poisson, Φ = −(3/5)ζ, (aH)² = H100² ω_m/a; [1G-A] Sec. 6.3 |
| (6) | EH98 no-wiggle T(k): s (26), q (28), L0/C0 (29), Γ_eff (30), α_Γ (31) | [EH98] |
| (7) | W(x) = 3(sin x − x cos x)/x³; series 1 − x²/10 + x⁴/280 − x⁶/15120 + x⁸/1330560 for \|x\| < 0.1 | 1D-A chain D5; series derived from sin x − x cos x = Σ (−1)^{n+1} 2n x^{2n+1}/(2n+1)! |
| (8) | R: equal mass R_ref(ω_ref/ω_m,eff)^{1/3}; dressed L/h; bare (L/h̄)/γ_w0; explicit | [1G-A] Secs. 6.1, 6.4 |
| (9) | ΛCDM reference: D0 = qplus(0), ω_m = Ω_m h² | Short & Coles astro-ph/0605013 Eq. (3) via the frozen `qplus` |
| (10) | anchored σ = (σ_TS/σ_ΛCDM) × anchor = X · E × anchor | [1G-A] Sec. 7 |

Every function docstring in the module cites its row. Equations (2), (4),
(5), (6), (8), (9) and (10) are those of the 1G-A evidence script; the
package reproduces them (Sec. 8, V1–V3). No equation of [GM] is changed.

### 4.1 Small-f_v0 limit of (2) (derived here, used as a limiting-case test)

Along the regular solution write u = 2/3 + δ. The tracker coefficients are
T = tΘ = 2 + f_v, A = t²4πGρ_d = (2/3)(1 − f_v), and, for the comoving
closure, B = t²4πGρ_eff = f_v(16 + 2f_v)/12 → (4/3)f_v and q → 1/5. To
first order in f_v the logarithmic-rate equations of `growing_mode` give

```text
Mészáros:  dδ/ds = −(5/3)δ − (10/9) f_v
comoving:  dδ/ds = −(5/3)δ − (10/9) f_v + (4/15) f_v = −(5/3)δ − (38/45) f_v
```

With f_v ∝ t = e^s at small f_v0, the regular solution is δ = α f_v with
α = −5/12 (Mészáros) and −19/60 (comoving). The integrand of (2) is
u − T/3 = δ − f_v/3, so

```text
ln g_TS = −(3/4) f_v0 + O(f_v0²)   (Mészáros),    ln g_TS = −(13/20) f_v0 + O(f_v0²)   (comoving).
```

Measured ln g/f_v0 at f_v0 = 1e−4: −0.750041 and −0.650034; at 1e−3:
−0.750417 and −0.650348. The remainder is linear in f_v0, as expected.
The same first-order tail, c·f_v(t_e), is the part of (2) omitted by starting
at t_e (Sec. 9.1).

### 4.2 Wall law: the finite-t_e identity

From 1 + z = γ_w/a_D (a_w0 = 1) and a_D(1 − f_v)^{1/3} ∝ t^{2/3}, for every t_e

```text
(t0/t_e)^{2/3} / (1 + z_e) = γ_w0 (1 − f_v0)^{1/3} / [γ_w(t_e) (1 − f_v(t_e))^{1/3}].
```

The package checks this corrected form to 1e−13 (measured ≤ 1e−15). The
*uncorrected* limit (t0/t_e)^{2/3}/(1+z_e) at t_e = 1e−8 t0 is below the
closed form by −4.67e−9 (f_v0 = 0.737) and −2.80e−9 (f_v0 = 0.627), which
is −f_v(t_e)/6 to first order (tested to relative 1e−6). The 1G-A artifact's
`growth_vs_photon_EdS_numeric_limit` (0.876792277 vs 0.876792281) shows the
same −4.7e−9; the closed form itself is exact.

## 5. The two growth laws (scope addition)

Neither law is a default; `growth_law` is a mandatory argument.

- `VOLUME_AVERAGE_CGI` — the [GM] framework as written: the regular growing
  mode of the comoving closure (Mészáros as comparator) on the
  volume-average background. Evidence class
  `DERIVED_FROM_VERIFIED_DEFINITIONS` ([1G-A] Sec. 4.3).
- `WALL_REGIONAL_EDS_COMMON_TIME` — sub-homogeneity modes grow as the EdS
  growing mode of the wall region in the common Buchert time t ([1G-A]
  Sec. 8). On the tracker, walls are exactly EdS in t: the package verifies
  (1 − f_v)^{1/3} a_D ∝ t^{2/3} and 6πG t² ⟨ρ⟩_D/(1 − f_v) = 1 to ≤ 1.6e−15.
  Evidence class `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`; the regional
  embedding stays `NOT_DERIVED` (`scientific_status`). The closure argument is
  `NOT_APPLICABLE`.

**Scale dependence.** The choice between the two laws is scale-dependent:
the volume-average CGI law is the relevant one for super-homogeneity modes,
and the wall law for mass-weighted sub-homogeneity statistics such as a
σ(M) at cluster-mass scales. The lead's Phase 1G-C work in progress argues
that [W09] coarse-grains at the ~100 h⁻¹ Mpc statistical-homogeneity scale,
so σ8-scale modes evolve on the wall regional background. That analysis
belongs to Phase 1G-C and is not adjudicated here. Every result carries this
caveat in its `limitations`.

## 6. Numerical configuration and tolerances

| Item | Reference value | Budget (fail-closed) |
|---|---|---|
| Growth grid, (2) | 16001 geometric points, Simpson in ln t; comparison 8001 | \|Δ ln g\| ≤ 1e−7 |
| Early start, (2) | t_e = 1e−6 t0; comparison 1e−5 t0 | \|Δ ln g\| ≤ 1e−4 |
| Growing mode | `REGULAR_GROWING_MODE_REFERENCE_CONFIG` (start 1e−6 t_e, DOP853, rtol 1e−12, atol 1e−14, EdS guard 1e−5) | as frozen (F1) |
| Wall identities | 2001-point grid over [1e−8 t0, t0]; t_e = 1e−8 t0 | each ≤ 1e−13 (relative) |
| Per-photon identity, (4) | — | ≤ 1e−13 (relative) |
| σ quadrature | ln k ∈ [ln 1e−6, ln 300] Mpc⁻¹, 8001 points, Simpson; comparison 4001 | relative change ≤ 1e−6 |
| k-range truncation | end envelope Δ² min(1, 3/x² + 3/x³)² relative to max integrand | ≤ 1e−8 |
| Window series threshold | \|x\| < 0.1 | truncation < 1e−18 |
| Anchor consistency | caller-supplied; here 0.05 | \|σ_ΛCDM/anchor − 1\| |

All values reproduce the 1G-A evidence script, so the numbers of [1G-A]
are reproduced by construction of the same numerics, not by re-tuning.
The anchor tolerance of 0.05 has the documented reason of [1G-A] Sec. 6.3:
EH98 omits BAO wiggles and the 0.06 eV neutrino suppression (about −1.5%),
and the first 1G-A run failed a 3% gate at +3.03%. A test checks that the 3%
gate still fails closed.

## 7. Results (Planck-anchored, primary f_b = 0.15633)

Inputs (driver and test fixtures, [P18] Table 2): A_s = 2.100e−9,
n_s = 0.9649, k_p = 0.05 Mpc⁻¹, ω_b = 0.02237, T_cmb = 2.7255 K; ΛCDM
Ω_m = 0.315, h = 0.674 (frozen `PLANCK_2018_QPLUS_RECIPE`), R_ref = 8/h =
11.869436 Mpc; anchor 0.8111.

### 7.1 Growth

| Parameters | f_v0 | γ_w0 | law | g | D0 = γ_w0 g | X = D0/qplus(0) |
|---|---|---|---|---|---|---|
| [GM] paper / notebook | 0.737 | 1.3685 | CGI comoving | 0.40266299 | 0.551044 | **0.699461** |
| | | | CGI Mészáros | 0.34169420 | 0.467609 | 0.593553 |
| | | | wall EdS | 0.64069586 | 0.876792 | **1.112945** |
| [NW15] | 0.627 | 1.3135 | CGI comoving | 0.51495288 | 0.676391 | **0.858568** |
| | | | CGI Mészáros | 0.45856306 | 0.602323 | 0.764551 |
| | | | wall EdS | 0.71984050 | 0.945510 | **1.200172** |

qplus(0) = 0.787813. The paper and notebook presets give identical g and X
(self-similarity in H_D0 t; Sec. 8, V5).

### 7.2 Per-photon early matter density

| Parameters | H_D0 (km/s/Mpc) | ω_m,eff | ratio to Planck 0.14310 |
|---|---|---|---|
| [GM] paper | 57.8560 | 0.1204751 | 0.8419 |
| [GM] notebook | 58.0144 | 0.1211359 | 0.8465 |
| [NW15] | 51.6966 | 0.1309372 | 0.9150 |

The closed form of (4) agrees with ⟨ρ⟩_D0 γ_w0³/ρ_crit(100) to ≤ 4.4e−16.

### 7.3 Anchored σ at the three radius conventions

| Parameters | R (Mpc): equal / dressed / bare | E: equal / dressed / bare | law | σ equal mass | σ dressed | σ bare |
|---|---|---|---|---|---|---|
| [GM] paper | 12.5702 / 10.9544 / 10.1041 | 0.9238 / 1.0104 / 1.0634 | CGI comoving | **0.5241** | 0.5733 | 0.6033 |
| | | | CGI Mészáros | 0.4447 | 0.4865 | 0.5119 |
| | | | wall EdS | **0.8339** | 0.9121 | 0.9599 |
| [GM] notebook | 12.5473 / 10.9245 / 10.0765 | 0.9262 / 1.0137 / 1.0668 | CGI comoving | 0.5254 | 0.5751 | 0.6053 |
| | | | CGI Mészáros | 0.4459 | 0.4880 | 0.5136 |
| | | | wall EdS | 0.8361 | 0.9151 | 0.9630 |
| [NW15] | 12.2260 / 13.1148 / 11.7814 | 0.9602 / 0.9153 / 0.9844 | CGI comoving | **0.6687** | 0.6374 | 0.6855 |
| | | | CGI Mészáros | 0.5954 | 0.5676 | 0.6104 |
| | | | wall EdS | **0.9347** | 0.8910 | 0.9582 |

Each σ is X · E × 0.8111 with the ratio identity holding to round-off.
The paper and NW15 rows reproduce [1G-A] Secs. 7–8 and the lead's wall-law
reference values (0.8339 / 0.9347, 0.9121 / 0.8910, 0.9599 / 0.9582).

### 7.4 ΛCDM reference and normalisation

σ_ΛCDM(EH98) = 0.835689 (unit-growth σ 1.060771 × qplus(0) 0.787813), i.e.
+3.03% from the 0.8111 anchor: inside the 5% gate, outside the original 3%
gate, as recorded in [1G-A].

### 7.5 Baryon-fraction sensitivity (reference keeps the primary f_b)

[GM] paper, comoving, equal mass: 0.5607 (f_b = 0.12), 0.5241 (0.1563),
0.4817 (0.20), i.e. +7.0% / −8.1%, as in [1G-A] Sec. 7. All 54 CGI rows of
the three presets × two closures × three conventions × three f_b are in the
artifact and agree with the 1G-A script (V3).

### 7.6 f_v0 scan of X

| f_v0 | 0.50 | 0.55 | 0.60 | 0.627 | 0.65 | 0.695 | 0.70 | 0.737 | 0.75 | 0.80 |
|---|---|---|---|---|---|---|---|---|---|---|
| CGI comoving | 0.9999 | 0.9489 | 0.8920 | 0.8586 | 0.8285 | 0.7650 | 0.7575 | 0.6995 | 0.6778 | 0.5878 |
| CGI Mészáros | 0.9247 | 0.8660 | 0.8017 | 0.7646 | 0.7315 | 0.6628 | 0.6548 | 0.5936 | 0.5711 | 0.4794 |
| wall EdS | 1.2593 | 1.2402 | 1.2158 | 1.2002 | 1.1853 | 1.1513 | 1.1471 | 1.1129 | 1.0995 | 1.0392 |

The CGI rows reproduce the [1G-A] inventory `fv0_scan` (V7).

## 8. Validation gates

`scripts/validate_phase1g_b_lagrangian_sigma.py`; all gates declared before
evaluation; the driver exits nonzero on any failure. Measured values are the
maxima over n evaluations.

| Gate | n | Budget | Measured | |
|---|---|---|---|---|
| V1 CGI growth vs 1G-A script (`_riccati_log_growth_excess`, Gyr params) | 6 | 1e−10 rel | 5.3e−12 | PASS |
| V1 wall growth vs 1G-A script (`wall_regional_bracket`) | 3 | 1e−13 rel | 2.2e−16 | PASS |
| V2 ω_m,eff vs 1G-A script (`per_photon_matter_density`) | 27 | 1e−13 rel | 4.4e−16 | PASS |
| V3 radius vs 1G-A script | 27 | 1e−13 rel | 2.2e−16 | PASS |
| V3 early-spectrum factor E vs 1G-A script | 27 | 1e−10 rel | 2.2e−16 | PASS |
| V3 anchored σ vs 1G-A script (`spectrum_and_sigma`, all f_b; wall rows as in its `main`) | 63 | 1e−10 rel | 5.3e−12 | PASS |
| V3 ΛCDM reference vs 1G-A script | 1 | 1e−12 rel | 1.1e−16 | PASS |
| V4 growth grid refinement | 6 | 1e−7 abs (ln g) | 4.1e−15 | PASS |
| V4 growth early-limit change | 6 | 1e−4 abs (ln g) | 1.9e−5 | PASS |
| V4 extrapolated limit vs direct t_e = 1e−8 t0 | 2 | 1e−7 abs (ln g) | 2.1e−8 | PASS |
| V4 quadrature self-convergence and 16001-point refinement | 30 | 1e−6 rel | 1.9e−10 | PASS |
| V4 k-range extension to [1e−7, 1e3] Mpc⁻¹ | 3 | 1e−8 rel | 8.7e−12 | PASS |
| V5 wall identities (Sec. 4.2, Sec. 5) | 3 | 1e−13 rel | 1.6e−15 | PASS |
| V5 small-f_v0 first-order coefficient at f_v0 = 1e−4 | 2 | 1e−4 abs | 4.1e−5 | PASS |
| V5 H0 / time-unit / G invariance of D0 | 9 | 1e−10 rel | 4.9e−12 | PASS |
| V5 window series/closed-form continuity at \|x\| = 0.1 | 1 | 1e−13 rel | 2.6e−14 | PASS |
| V6 ΛCDM reference offset from the anchor | 1 | 0.05 abs | 0.0303 | PASS |
| V7 [1G-A] inventory, six-decimal growth values | 11 | 5e−7 abs | 4.2e−7 | PASS |
| V7 [1G-A] inventory, f_v0 scan (four decimals) | 20 | 5e−5 abs | 4.9e−5 | PASS |
| V7 [1G-A] inventory, σ / E / R table (four decimals) | 44 | 5e−5 abs | 5.0e−5 (4.990e−5) | PASS |
| V7 [1G-A] inventory, ω_m,eff (five decimals) | 3 | 5e−6 abs | 4.9e−6 | PASS |

V1–V3 import the committed 1G-A evidence script and call its functions
directly; its `main` is not run and nothing of it is written. The 5e−12
differences in V1/V3 come from the package evaluating the growth in H0 = 1
units and the script in Gyr units: the adaptive solve (rtol 1e−12) takes
different last-bit steps. On identical parameters the two routes are
bit-identical, and a test checks them to 1e−13. The V7 maxima sit just under
half a unit of the last printed digit because they compare with *rounded*
values, e.g. 1.0104499 printed as 1.0104. Truncation envelopes are
≤ 5.8e−12 everywhere.

## 9. Findings

### 9.1 The sixth decimal of the printed 1G-A g_TS is not converged

At the reference early start t_e = 1e−6 t0, the omitted piece of (2) is
c·f_v(t_e) (Sec. 4.1). The package records the linear estimate of this bias
in every result (`log_growth_early_limit_linear_bias_estimate`):
+1.82e−6 (comoving) and +2.10e−6 (Mészáros) at f_v0 = 0.737. Extrapolating
from t_e = 1e−6 t0 agrees with a direct t_e = 1e−8 t0 run to 2e−8 in ln g.
The t_e → 0 limits are therefore:
- **g_TS = 0.4026623** (comoving) and **0.3416935** (Mészáros);
- against the reference-config values 0.4026630 and 0.3416942, which are the
  values [1G-A] prints (0.402663, 0.341694).

This is inside the declared 1e−4 early-limit budget of [1G-A] and changes no
four-decimal σ. The bias is recorded, not applied, so the package
reproduces [1G-A]. Anyone quoting g_TS to six decimals should use the limit
values, or run with a smaller `early_time_fraction`.

### 9.2 The wall-law "numeric limit" agrees to 5e−9, the exact identity to 1e−15

The scope addition quoted agreement of the numeric limit
lim (t0/t_e)^{2/3}/(1+z_e) with the closed form "to 1e−13". At finite t_e
the uncorrected expression differs by −f_v(t_e)/6, which is −4.7e−9 at
t_e = 1e−8 t0. The 1e−13 statement holds for the exact finite-t_e identity
of Sec. 4.2 and for the closed form against the tracker functions (0.0 and
≤ 1e−15). The closed form and every reference value are unaffected.

### 9.3 Ordering

For every f_v0 of the scan (and in the small-f_v0 limit, where the
first-order coefficients are −3/4 < −13/20 < −1/3), D0(Mészáros) <
D0(comoving) < D0(wall). At f_v0 = 0.5 the CGI comoving X is 0.99990, within
1e−4 of the photon-normalised ΛCDM growth.

## 10. Tests

`tests/test_phase1g_b_lagrangian_sigma.py`: 92 tests, about 6 s. Tolerances
are stated in the file header (A06 convention). The tolerance audit
(`scripts/audit_numerical_tolerances.py`) now counts 626 comparisons, 583
before plus 43 new, with none missing a tolerance.

**What the tests cover:**
- **1G-A reference values** (half a unit of the printed digit):
  - growth g and X for both closures, both presets;
  - X_wall and the wall-law closed form;
  - ω_m,eff for three presets;
  - the full 18-row σ / E / R table for paper and NW15 × three laws × three
    conventions;
  - the ΛCDM value and the 3.03% offset;
  - the f_b band.
- **Full-precision cross-check** against the 1G-A script: growth on identical
  params (1e−13), ω_m,eff (1e−13), σ and the ΛCDM σ (1e−12).
- **Dimensions and self-similarity:**
  - D0 is independent of H0, of the time unit (H0 = 1, Gyr, km/s/Mpc) and of
    G (1e−10);
  - ω_m,eff ∝ H0² and is G-independent;
  - H_D0 and γ_w0 match the frozen presets;
  - the Gyr-unit route of (4) agrees;
  - radii scale linearly with L, and equal-mass ω R³ is preserved;
  - σ ∝ D0 and σ ∝ √A_s.
- **Limiting cases:**
  - T(k → 0) → 1, T is monotone, and f_b = 0 reduces EH98 (30)–(31) to
    Γ_eff h = ω_m;
  - W(0) = 1, the series and the envelope, and W is even;
  - the first-order small-f_v0 coefficients −3/4 and −13/20 and the wall
    law's −1/3, with γ_w0 → 1;
  - the early-limit bias estimate equals the first-order tail;
  - the ordering Mészáros < comoving < wall;
  - σ decreases with R;
  - a vanishing radius fails the truncation check instead of truncating.
- **Normalisation:** the 5% gate passes and the original 3% gate fails
  closed.
- **API:**
  - all 9 functions take keyword-only arguments with no defaults, and all
    12 dataclasses are keyword-only with no field defaults;
  - barotropic refusal under both laws (enum and string spellings), citing
    1G-A Sec. 4.1;
  - law, closure and numerics pairing;
  - the naming firewall (names, members, JSON keys, string values);
  - no packaged Planck or anchor constant;
  - status tokens are fixed, and relabelling is refused;
  - the scientific-status authorisations stay `NOT_GRANTED`;
  - records are frozen and arrays read-only;
  - consistency is validated on construction;
  - JSON is deterministic.
- **Invalid inputs:** early spectrum, background, radius spec, numerics and
  quadrature are each refused on bad input. Convergence, identity and
  density-identity budgets fail closed, and so do the anchor contracts
  (quadrature, T_cmb, equal-mass reference, anchor inputs).

## 11. Deviations from the specification

1. **Module location** (Sec. 2): `src/timescape_fsigma8/lagrangian_sigma.py`,
   not `growth/lagrangian_sigma.py`. This avoids editing or evading the
   frozen growth-package firewall test. It is not exported from `growth`.
2. **Status constant names.** The status constants are `OBSERVATIONAL_STATUS
   = "NON_OBSERVATIONAL"` and `FSIGMA8_STATUS = "NOT_FSIGMA8"` (the existing
   `transfer` precedent), plus `SIGMA8_STATUS = "NOT_OBSERVATIONAL_SIGMA_8"`
   and `SCIENTIFIC_CLASSIFICATION = "CONDITIONAL_MODEL_INTERNAL_LINEAR_SIGMA_M"`.
   In JSON output they sit under neutral keys (`observational`,
   `amplitude_identity`, `growth_rate_product`), so no output key carries the
   forbidden tokens.
3. **Reference numerics as named constants.** The reference numerics are
   named module constants, like `REGULAR_GROWING_MODE_REFERENCE_CONFIG`. They
   are passed explicitly, never defaulted. Planck inputs and the anchor are
   *not* packaged.
4. **Anchored ratios allow a differing baryon fraction.** A Timescape model
   with a different f_b may be anchored to a ΛCDM reference at the primary
   f_b, as in [1G-A]'s sensitivity rows, but the difference is recorded by
   name. T_cmb, transfer model and quadrature must match.
5. **Scope addition implemented** as requested (Sec. 5). The wall-law σ is
   evaluated at the primary f_b only in the driver, matching [1G-A]; the
   API supports any f_b.

## 12. Environments and exact commands

Windows 11 (10.0.26200); worktree on branch `phase-1g-b-lagrangian-sigma`,
with `PYTHONPATH=<worktree>\src` (the venvs have the main checkout installed
editable) and `PYTHONDONTWRITEBYTECODE=1`.

| Interpreter | NumPy | SciPy | Driver | New tests | Full suite |
|---|---|---|---|---|---|
| Python 3.14.3 | 2.5.2 | 1.18.1 | 21/21 gates PASS | 92 passed | 978 passed, 30 skipped (7 min 48 s) |
| Python 3.11.9 | 2.4.6 | 1.17.1 | 21/21 gates PASS | 92 passed | 978 passed, 30 skipped (7 min 49 s) |

**Determinism.** The artifact regenerated twice on 3.14 at `0883814` is
byte-identical (SHA-256 `c111f845…4e1b`). The 3.11 artifact differs only
in its environment block: every number is bit-identical across the two
interpreters.

**Full suites.** Both ran at `0883814` with `-B -W error -p no:cacheprovider`:
no failures, errors or warnings. The pass/skip split is identical on the two
interpreters. The 1G-A base recorded 916 passed with every input present; 916
+ 92 new = 1008 = 978 + 30.

**Skips.** All 30 skips are pre-existing tests whose inputs are absent from
this fresh worktree:
- 26 upstream-oracle tests (`test_vs_upstream_oracle.py` 18,
  `..._perturbation_oracle.py` 4, `..._barotropic_oracle.py` 4), which need
  the git-ignored `.reference/` clone;
- 4 generated-artifact or reproducibility-gate tests
  (`test_anchored_density_growth.py`, `test_b2_artifact_schema.py`,
  `test_growth_convergence_purity.py`, `test_reproducibility_gates.py`, one
  each), which need the git-ignored `artifacts/`.

No new test skips.

```text
.venv\Scripts\python -B -W error scripts\validate_phase1g_b_lagrangian_sigma.py
.venv\Scripts\python -B -W error -m pytest -q -p no:cacheprovider tests\test_phase1g_b_lagrangian_sigma.py
.venv\Scripts\python -B -W error -m pytest -q -p no:cacheprovider
.venv311\Scripts\python -B -W error -m pytest -q -p no:cacheprovider
.venv\Scripts\python -B scripts\audit_numerical_tolerances.py
```

## 13. Preservation statement and status tokens

- **Files added:** the module, its tests, the driver and this report.
- **Unchanged:** every existing package module, including `growth/`,
  `perturbations/`, `background/` and `scientific_status.py`. Also unchanged
  are every existing test and script, the 1G-A report, inventory and
  evidence script (imported read-only), every frozen report, `CLAUDE.md`,
  `README.md` and the upstream files.
- **Tokens:** no equation, tolerance or status token was changed.
  - `SIGMA8_AUTHORIZATION`, `FSIGMA8_AUTHORIZATION`,
    `OBSERVATIONAL_AUTHORIZATION` and `UNIQUE_TIMESCAPE_PREDICTION` remain
    `NOT_GRANTED`.
  - `REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING` remains `NOT_DERIVED`.
- **Not committed:** the artifact, which is git-ignored.
- **Remote:** nothing is pushed or tagged.
- **Before freezing:** an adversarial/compliance audit of this phase is
  still required by the project workflow.
