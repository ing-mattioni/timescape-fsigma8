# Background validation report — timescape tracker (Phase 1B)

**Project:** timescape-fsigma8
**Date:** 2026-07-15
**Scope:** validation of the independent tracker-background implementation
(`src/timescape_fsigma8/`) against the scientific specification
([GM] arXiv:2511.17160v2; [W09] arXiv:0909.0749) and the upstream notebook
as a numerical oracle. Companion documents:
`reports/background_equation_audit.md` (equation-level audit and the D1/D2
evidence) and `reports/phase1b_compliance_audit.md` (+ addendum).

---

## 1. Equations implemented

Full equation-by-equation audit table: `background_equation_audit.md` §2.
Inventory by module (every function cites its equation in its docstring):

| Module | Function | Source equation |
|---|---|---|
| `background.parameters` | `TrackerParams` (fv0, HD0) | [GM] Sec. 5.1.1 (free parameters) |
| | `from_dressed_H0` / `H0_dressed` | [GM] p. 25; [W09] (B8)–(B9) at t0 |
| | `t0` | [W09] text after (B5) |
| | `aD0` = 1 + f_v0/2 | [GM] (5.4) + p. 25; [W09] (B7) |
| `background.tracker` | `fv` | [GM] (5.6); [W09] (B2) |
| | `dfv_dt`, `d2fv_dt2` | derived from (5.6) |
| | `a_D` | [GM] (5.5); [W09] (B1) |
| | `H_D`, `da_D_dt`, `Theta` | [W09] (B6); [GM] (3.6) |
| | `R_D` = −6 f_v/t² | [GM] (5.7) **with deviation D1**; [W09] (B4)+(B6) |
| | `Q_D` | [GM] (5.7); [W09] (15) |
| | `dR_D_dt`, `dQ_D_dt` | derived; **D2**: correct quotient rule |
| | `rho_d`, `drho_d_dt` | [GM] (3.16) + Sec. 5.1.1 normalisation; (3.10) |
| | `Omega_m`, `Omega_R`, `Omega_Q` | [GM] (3.18); [W09] (B3)–(B5) |
| `background.effective_fluid` | `rho_eff`, `p_eff` | [GM] (3.12), (3.13) with K_D = 0 |
| | `drho_eff_dt`, `dp_eff_dt` | derived; consistent with [GM] (3.17) |
| | `w_eff`, `cs2_eff` | [GM] Sec. 4 text definitions; `cs2_eff` carries **D2** |
| `background.observables` | `gamma_w`, `dgamma_w_dt` | [GM] p. 25; [W09] (B7); derivative derived |
| | `a_w` = a_D/γ_w | [GM] (5.4) |
| | `dtau_w_dt` = 1/γ_w | definition γ_w := dt/dτ_w ([GM] p. 24; [W09] Sec. II) |
| | `tau_w` (τ_w(0) = 0) | [W09] (B12); derived as the exact integral of 1/γ_w |
| | `H_dressed` = γ_w H_D − γ̇_w | [W09] (28)/(B8); closed form (4+f_v+4f_v²)/(6t) |
| | `redshift` | [W09] (38) ≡ 1/a_w − 1 (tested identity) |

Preserved scientific decisions (per the gap-closure instruction, both
awaiting author confirmation — §8):

- **D1:** `<R>_D = −6 f_v/t²`; the f_{v,0}^{−2/3} prefactor printed in
  [GM] Eq. (5.7) is treated as a probable paper typo.
- **D2:** analytically correct dQ_D/dt, hence
  c²_{s,eff} = −(2 + 2f_v − f_v²)/(2 + f_v)²; no compatibility bug is
  exposed anywhere in the package.

The package split (`background/` with `parameters` / `tracker` /
`effective_fluid` / `observables`) changed no formula: equivalence with the
pre-split module is pinned by `tests/test_refactor_equivalence.py` (golden
values captured from the monolith at commit `56f22ba` before the split;
agreement required at rtol 1e−13/atol 1e−15, observed bit-identical under
Python 3.14).

## 2. Conventions and units

**Frames and symbols** (explicit throughout the code):

| Symbol | Meaning | Where |
|---|---|---|
| `t` | Buchert volume-average (bare) cosmic time | all functions' time argument |
| `tau_w` | wall-observer proper time, τ_w(0) = 0, dτ_w/dt = 1/γ_w | `observables.tau_w` |
| `a_D` | volume-average scale factor, normalised to a_{w,0} = 1 | `tracker.a_D` |
| `a_w` | dressed (wall) scale factor = a_D/γ_w, a_w(t0) = 1 | `observables.a_w` |
| `HD0` (bare) | H_D(t0), stored in `TrackerParams` in inverse time units | `parameters` |
| `H0_dressed` | γ_w H_D − γ̇_w at t0; what SNe calibrate | `parameters.H0_dressed`, `observables.H_dressed` |

**Core is unit-agnostic:** time in any unit consistent with 1/HD0; c = 1;
Λ = 0; K_D = 0; G passed explicitly (default 1.0 = code units). Physical
parametrisation enters only through `presets.py` (Gyr units).

**Audited conversions** (`units.py`; tests
`test_units_and_presets.py`): from exact primaries only —
1 au = 149 597 870.700 km (IAU 2012 B2), 1 pc = (648 000/π) au (IAU 2015
B2), 1 day = 86 400 s, 1 Julian yr = 365.25 d = 31 557 600 s. Derived:
1 Mpc = 3.0856775814913673×10¹⁹ km (matches the IAU-quoted value to
1e−15); H0 = 100 km/s/Mpc ⇒ Hubble time 9.7779222 Gyr. The upstream
notebook's 9.778 convention is retained **only** as a documented
comparison constant (relative difference 8.0×10⁻⁶); no conversion uses it.

## 3. H0 discrepancy analysis

The sources give two dressed H0 values (Phase 1A §11.1); both are encoded
as immutable presets (`presets.py`), with H_{D,0} always **derived** via
the dressed→bare relation ([GM] p. 25):

| Preset | H0 dressed [km/s/Mpc] | H_D,0 bare [km/s/Mpc] (derived) | t0 [Gyr] |
|---|---|---|---|
| `PAPER_REFERENCE` | 73.03 ([GM] Sec. 5.1.1 text, from their ref. [80]) | 57.86 | 15.419 |
| `NOTEBOOK_REFERENCE` | 73.23 (upstream cell 2, h = 0.7323) | **58.01** | 15.377 |

Evidence collected in Phases 1A/1B: [GM]'s own quoted H_{D,0} ≈ 58.01
km/s/Mpc is reproduced by 73.23, not by the paper's stated 73.03 (which
gives 57.86, pinned in `test_bare_H0_reference_values`); conversely the
notebook's *unused* constant `H0_SI` equals 73.04. Both sources are
internally inconsistent, in opposite directions. Impact: the 0.27%
H0 difference rescales times/redshift mappings only (see §4); every
dimensionless curve (Ω_i, w_eff, c²_s,eff, f_v vs a_D/a_{w,0}) is
identical between presets because both share f_v0 = 0.737. Which value is
canonical requires author input (§8).

## 4. Redshift and time analysis

Method: dressed redshift z(t) from [W09] (38) (validated against the
independent 1/a_w − 1 construction, `test_wall_observables.py`);
t(z = 20) via `scipy.optimize.brentq` on z(t) − 20, bracket [10⁻⁴, t0]
Gyr, xtol = 10⁻¹² Gyr, rtol = 8.9×10⁻¹⁶, root verified by re-evaluation
(`tests/test_epochs.py`, regression rtol 1e−10).

| Quantity | PAPER_REFERENCE (73.03) | NOTEBOOK_REFERENCE (73.23) |
|---|---|---|
| z at t = 0.180 Gyr (background-figure start) | 21.273 | 21.233 |
| z at t = 0.218 Gyr (perturbation start) | 18.622 | 18.586 |
| t at z_dressed = 20 | 0.19674 Gyr | 0.19620 Gyr |
| t0 (volume-average age) | 15.419 Gyr | 15.377 Gyr |
| τ_w(t0) (wall age) | 12.296 Gyr | 12.262 Gyr |

Digits: values are exact (≪1e−9) *for the stated input parameters*, but
the inputs (f_v0 = 0.737, H0 to 4 digits) carry 3–4 significant figures;
no more than ~4 significant figures should be read as physical.
Cross-check (tested): z depends on t only through HD0·t, so t(z = 20)
scales exactly as 1/HD0 between presets.

**Start-time status (explicitly unresolved):** under *neither* preset does
0.218 Gyr correspond to the paper's stated z = 20 (it is z ≈ 18.6; z = 20
occurs at ≈ 0.196–0.197 Gyr), and the background figures start at
0.18 Gyr ⇔ z ≈ 21.2–21.3. The provenance of 0.18 and 0.218 Gyr remains
unexplained and is flagged for the authors (§8). A bare-redshift reading
was checked and excluded in `background_equation_audit.md` §6.

## 5. Upstream notebook comparison metrics

Source: `scripts/compare_to_oracle.py` →
`artifacts/independent/oracle_comparison_stats.json` (machine-readable;
embeds oracle provenance). Oracle: 501 samples on [0.18 Gyr, t0], upstream
commit `590c6fd5332a`, notebook SHA-256 `86d2534d…` (unchanged). Gate for
equivalent quantities: max rel err < 1e−9 (script exits nonzero
otherwise); measured worst: **1.5×10⁻¹⁵**.

**Equivalent quantities** (same mathematics, independent algebra;
`U_D`, `K_D`, `dU_D/dt` compared as documented combinations of our
R_D/Q_D since [GM] does not use the morphon intermediates):

| quantity | max abs err | max rel err | RMS rel err | t(max rel) [Gyr] |
|---|---|---|---|---|
| `fv` | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0.1800 |
| `dfvdt` | 4.441e-16 | 6.349e-16 | 1.936e-16 | 14.9817 |
| `d2fvdt` | 3.553e-15 | 6.607e-16 | 2.320e-16 | 14.3131 |
| `a` | 4.441e-16 | 3.961e-16 | 1.085e-16 | 12.3375 |
| `daDdt` | 1.110e-15 | 7.015e-16 | 1.868e-16 | 0.6663 |
| `Theta` | 2.842e-14 | 7.168e-16 | 1.879e-16 | 5.3773 |
| `RD` | 3.411e-13 | 7.505e-16 | 2.648e-16 | 8.2343 |
| `QD` | 2.842e-14 | 1.336e-15 | 4.009e-16 | 14.9817 |
| `dRDdt` | 2.910e-11 | 1.461e-15 | 3.927e-16 | 5.0734 |
| `rhod` | 8.590e+09 | 1.210e-15 | 4.167e-16 | 12.0943 |
| `rhoEff` | 5.369e+08 | 8.140e-16 | 2.963e-16 | 8.2343 |
| `pEff` | 2.684e+08 | 7.703e-16 | 2.760e-16 | 7.7176 |
| `wEff` | 1.665e-16 | 4.108e-16 | 1.351e-16 | 6.4107 |
| `UD` | 4.027e+08 | 7.778e-16 | 2.649e-16 | 8.2343 |
| `KD` | 4.027e+08 | 1.006e-15 | 3.045e-16 | 6.0764 |
| `dUDdt` | 3.436e+10 | 1.515e-15 | 3.954e-16 | 5.0734 |

Note on absolute errors: densities are O(10²⁰–10²⁴) in upstream units
(M☉/HL³ and per-time powers), so absolute errors of 10⁸–10¹⁰ correspond
to relative errors of ~10⁻¹⁵ — the relative columns are the meaningful
ones. `fv` is bit-identical (same closed form on both sides). Times in
Gyr use the upstream notebook's own 9.778/h grid convention (the oracle's
definition).

**D2-affected upstream quantities** (separate table by design — NOT
equivalent; the statistics quantify the *documented upstream defect*
relative to the correct derivatives, not an error of this
implementation):

| quantity | max abs err | max rel err | RMS rel err | t(max rel) [Gyr] |
|---|---|---|---|---|
| `dQDdt` | 1.054e+03 | 3.732e+00 | 1.661e+00 | 15.3769 |
| `dKDdt` | 3.602e+24 | 1.660e-01 | 1.172e-01 | 1.4869 |
| `drhoEffdt` | 1.801e+24 | 4.869e-02 | 3.599e-02 | 1.5477 |
| `dpEffdt` | 1.801e+24 | 1.181e-01 | 9.440e-02 | 1.6389 |
| `cs2Eff` | 7.232e-02 | 1.753e-01 | 1.353e-01 | 1.6085 |

(The independent evidence that *upstream's own sampled data* side with our
derivatives — np.gradient of the oracle's Q_D/ρ_eff/p_eff — is in
`tests/test_vs_upstream_oracle.py` and `background_equation_audit.md` §4.)

## 6. Independent Figure 1 comparison

Generated by `scripts/make_independent_fig1.py` from the independent
package only (no upstream plotting code; oracle read solely for the
forensic overlay):

- `artifacts/independent/fig1_reproduction_PAPER_REFERENCE.png/.pdf`
- `artifacts/independent/fig1_reproduction_NOTEBOOK_REFERENCE.png/.pdf`
- `artifacts/independent/fig1_right_forensic_D2.png/.pdf`

**Left panel** (Ω_d, Ω_R, Ω_Q vs a_D/a_{w,0}): visually matches the
published [GM] Fig. 1 left; endpoints pinned by tests
(0.1404 / 0.8854 / −0.0259 at t0).

**Right panel** (w_eff, c²_s,eff): the **canonical panel carries the
corrected c²_s,eff** and is explicitly labelled "(corrected; D2)" plus a
figure-level note that it intentionally differs from the published curve.
Where the published Fig. 1 right panel shows c²_s,eff *above* w_eff ending
at −0.3452, the corrected curve lies *below* w_eff, from −1/2 (early) to
−0.3912 (today). w_eff itself matches the published curve (−0.494 →
−0.3735).

**Forensic figure:** overlays the correct c²_s,eff with the D2-affected
upstream curve sampled from the local oracle (skipped gracefully if the
oracle is absent), endpoints annotated (−0.3912 correct vs −0.3452
published). No buggy function exists in the package — the D2-affected
curve is read from oracle *data* only.

**Preset note (as required):** both presets share f_v0 = 0.737 and all
Fig.-1 curves are dimensionless functions plotted against the
dimensionless a_D/a_{w,0}, so the two presets' curves coincide
identically; the H0 difference changes only the physical time/redshift
mapping of the axis (each figure is annotated with its own t-range and
z(0.18 Gyr)). Both figures are still emitted, parameter-stamped, for
traceability.

Accessibility note: colors deliberately match the published figure's
semantics for side-by-side comparability; since that red/green pairing is
not CVD-safe (checked: deutan ΔE ≈ 3), every curve additionally carries a
distinct linestyle and legend entry, so identity is never encoded by
color alone.

## 7. Test and environment results

Suite: **177 tests**, 8 files — identities (Buchert (3.8)–(3.11), (3.17),
definitions, derivatives), limits and reference values, refactor
equivalence (golden values), units and presets, wall/dressed observables,
epochs, domain validation (t ≤ 0), upstream-oracle comparison. Oracle
tests auto-skip if the oracle file is absent; it was present in both runs
below. Installs used `--index-url https://pypi.org/simple` (machine's
default index unreachable); no global Python or pip configuration was
altered (per-command venvs `.venv`, `.venv311`, both git-ignored).

| Environment | Python | NumPy | SciPy | pytest | Result |
|---|---|---|---|---|---|
| `.venv` (py -3.14) | 3.14.3 | 2.5.1 | 1.18.0 | 9.1.1 | **177 passed** |
| `.venv311` (py -3.11) | 3.11.9 | 2.4.6 | 1.17.1 | 9.1.1 | **177 passed** |

Platform: Windows-11-10.0.22631-SP0 (AMD64). The two environments differ
in interpreter *and* NumPy/SciPy generations, so the pass is a real
cross-configuration check; the golden-value equivalence test (rtol 1e−13)
passing under both bounds libm/interpreter/BLAS drift at negligible
levels. Machine-readable record:
`artifacts/independent/test_matrix.json`.

## 8. Unresolved scientific questions

Carried forward (details: `background_equation_audit.md` §7, Phase 1A
§12); all await author/human input:

1. **D1** — is the f_{v,0}^{−2/3} prefactor in [GM] Eq. (5.7) a typo?
   (Three independent lines of evidence say yes; notebook unaffected.)
2. **D2** — upstream `dQDdt` algebra defect and its published
   consequences (Fig. 1 right panel; barotropic Fig. 3 runs).
3. **Canonical H0** — 73.03 (paper text) vs 73.23 (notebook; consistent
   with the paper's own H_{D,0} ≈ 58.01).
4. **Start times** — provenance of 0.18 and 0.218 Gyr (neither is
   z = 20 under either preset; §4).
5. **Initial-condition provenance** — which ΛCDM parameters generated the
   17-digit IC values in notebook cell 15.
6. **Upstream solver tolerances** — all published perturbation runs use
   `solve_ivp` defaults (RK45, rtol 1e−3); convergence unverified.

## 9. Blockers for Phase 1C

Technical blockers from the compliance audit: **none remaining** (see the
addendum in `phase1b_compliance_audit.md`). Decision/input blockers before
perturbation work can produce science-grade output:

1. **Choice of canonical preset** (or the decision to carry both) for all
   perturbation runs — depends on §8.3.
2. **Dual-track validation policy for D2:** reproducing upstream
   perturbation results as an *oracle* requires their D2-affected
   c²_s,eff in the barotropic matrix, while science-grade runs must use
   the corrected one. The policy (oracle-comparison harness separate from
   the scientific package, mirroring Phase 1B's approach) should be
   ratified before implementation so no buggy coefficient ever enters the
   package.
3. **Initial-condition provenance** (§8.5) — needed to set perturbation
   ICs independently rather than copying the notebook's opaque values.
4. **Perturbation equation inventory** ([GM] Sec. 4, Eqs. (4.x)) —
   the same extract-before-implement discipline as Phase 1B; not started
   (by instruction).

## 10. Readiness statement

Distinguishing precisely what is and is not established:

- **Background equations: validated.** The tracker background
  implementation satisfies the Buchert system ((3.8)–(3.11), (3.17)) to
  1e−12, matches all 16 algebraically equivalent upstream quantities to
  ≤ 1.5×10⁻¹⁵ (501 samples), reproduces published reference values
  (H_{D,0} ≈ 58.01 km/s/Mpc, a_{D,0}/a_{w,0} ≈ 1.37, Fig.-1 endpoints),
  passes EdS/Milne limits, and is stable across two Python environments.
- **D1 and D2: independently confirmed, awaiting author feedback.** The
  evidence is threefold-redundant for D1 and internally conclusive for D2
  (upstream's own data contradict upstream's derivative code), but both
  remain *documented deviations from printed sources*, not
  author-acknowledged errata.
- **Barotropic perturbation consequences: not yet quantified.** D2's
  c²_s,eff enters four coefficients of the barotropic system; its
  quantitative effect on the published Fig. 3 (and any growth-rate
  conclusions) is inference until Phase 1C solves the perturbation
  equations both ways.
- **Initial-condition provenance: unresolved.** The notebook's
  perturbation ICs (and the 0.18/0.218 Gyr epochs) cannot yet be derived
  from first principles; Phase 1C must not inherit them uncritically.

Subject to the decision items in §9, the background layer is ready to
carry Phase 1C.
