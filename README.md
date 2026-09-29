# timescape-fsigma8

Reproducibility project for linear perturbation growth in the Timescape
cosmological model, based on:

> M. Galoppo & P. Mourier, *Cosmological perturbations on an averaged
> background*, JCAP 02 (2026) 066, arXiv:2511.17160.

## Current status: Phase 1F-C-R — Astra independent-audit remediation

The current scientific interpretation is recorded in
[the successor remediation report](reports/phase1f_c_r_astra_audit_remediation.md)
and its [machine-readable inventory](reports/phase1f_c_r_astra_audit_remediation_inventory.json).
Earlier reports and inventories are preserved historical checkpoints; their
source attributions and physical-compatibility claims are superseded by this
record where specified. The accepted 1F-C realization and kinematic verdict
remain unchanged. A minimal conditional
[Phase 1F-D scalar necessary-bound diagnostic](reports/phase1f_d_necessary_bound.md)
is now available in `timescape_fsigma8.phase1f_d`. It tests only the strict
positive-core margin; a positive result does not establish existence or
physical compatibility. No Phase 1F-D geometric or perturbative solver is
implemented, and the frozen scientific statuses are preserved.

Imported regional dust-FLRW equations are conditional on their regional
backgrounds. Their physical embedding into the common Timescape spacetime,
zeroth-order dust/wall background coincidence, all-time transfer/constitutive
compatibility, and a physical Timescape trajectory remain **NOT_DERIVED**.
The naive W09 regional common-time EdS scale interpreted as exact proper-time
flat dust using the W09 wall lapse is **REJECTED_UNSUPPORTED**.
Manufactured H1 jets establish algebraic compatibility only.

Remaining closures include regional/common background and source embedding;
all-time transfer/constitutive compatibility; H1-to-wall/dressed spatial and
density maps; perturbative wall lapse; local scale/Hubble and perturbed
geometry; initial, boundary, kernel and morphology data; and future
lightcone, tracer and statistical inputs. Lapse and pullback callbacks are
not an exhaustive irreducible-input theorem. No unique Timescape prediction
or observational, RSD, sigma8 or fsigma8 authorization is granted.

Ranks 4, 5 and the optional +1=6 count differential field species, not freely
selectable admissible initial functions after constraints and supplied
histories. Conditional forward uniqueness assumes complete admissible data;
it is not a trajectory-existence result. Finite-mode barotropic ODE uniqueness
does not establish continuum stability: the negative corrected sound speed
requires a separate validity-scale/closure analysis before unrestricted
high-wavenumber use. No such research is introduced here.

Phase 1F-C acceleration arrays explicitly distinguish coordinate covectors,
coordinate contravariant components and physical orthonormal components in
the same inverse-metric Cholesky frame as 1F-B. Optional C_W reconstruction
requires a caller-declared linear-regime limit and positive `1+2C_W` at every
accepted output time. These are validity gates, not new scientific dynamics.

### Post-remediation independent review and fixes

An independent review of Phases 1A–1F-C-R
([report](reports/phase1f_c_r_post_remediation_independent_audit.md),
findings F1–F9) confirmed the paper-level equations and every re-computed
number, and raised nine findings. They have been addressed as follows:

- **F1:** the paper ICs carry a decaying mode. An explicit, non-default
  `TIMESCAPE_REGULAR_GROWING_MODE` convention now exists for the clean
  systems ([validation](reports/phase1f_c_r_f1_growing_mode_initial_conditions_validation.md)).
- **F3:** the H1 runtime now gates `J_Xi = 0` and 13 background identities.
  Only enforced results carry closure status tokens
  ([validation](reports/phase1f_c_r_f3_h1_kinematic_gates_validation.md)).
- **F2, F4–F9:** a successor erratum, provenance records, checkout-independent
  reproducibility gates, mandatory `G`, and refreshed documentation
  ([remediation](reports/phase1f_c_r_f2_f4_f9_remediation.md)). F4 is closed
  as a documented permanent gap: three specifications and any H1 decision
  record are confirmed unavailable. The three audits were later recovered
  with matching hashes and are committed unchanged. A citation map ties every
  specification-cited equation to a committed report.

The earlier implementation milestones below remain useful provenance:

- **Phase 1A (done):** audit + clean-room re-execution of the authors'
  `ACPT_Timescape.ipynb` → `reports/upstream_reproducibility.md`.
- **Phase 1B (done, incl. gap closure):** equation-audited independent
  implementation of the Timescape **tracker background**
  (`src/timescape_fsigma8/background/`), validated against the Buchert
  identities, published reference values, and the upstream notebook as a
  numerical oracle → `reports/background_equation_audit.md` and
  `reports/background_validation.md`. The audit found one typo in the
  paper (Eq. 5.7) and one algebra error in the upstream notebook (`dQDdt`)
  affecting the published c²_s,eff; both are documented, not "fixed"
  upstream.
- **Phase 1C-A (done):** equation-level audit of the Mészáros, comoving,
  and barotropic perturbation systems, including IC/epoch provenance and
  complete D2/D3 mapping → `reports/phase1c_perturbation_equation_audit.md`.
- **Phase 1C-B1 (done):** independent typed implementation and numerical
  validation of the D2-free/D3-free **Mészáros and comoving** systems,
  including explicit IC/epoch scenarios, solver convergence, oracle
  reproduction, and clean Fig. 2 →
  `reports/phase1c_b1_clean_systems_validation.md`.
- **Phase 1C-B2 (done):** independent typed implementation and numerical
  validation of the **barotropic** system (Eqs. 4.13–4.17), exposing **both**
  explicit D3 branches (`printed_4_15`, `derived_4_10`), both tilt
  variables, and the IC-rate/epoch/wavenumber interpretations as mandatory
  explicit choices with no defaults; upstream Fig.-3 trajectories reproduced
  through an isolated forensic harness (the D2-corrupted sound speed never
  enters the scientific package) →
  `reports/phase1c_b2_barotropic_validation.md`.
- **Phase 1D-A (done):** equation-level audit of the observable meaning of
  the CGI perturbation variables: exact harmonic mapping
  Δ_d,k = −k_code²·δ_m,k, bare/dressed growth coordinates with the exact
  tracker chain factor, zero-crossing policy, and the blockers separating
  the present variables from σ_R/σ_8/observational fσ8 →
  `reports/phase1d_a_growth_observable_audit.md`.
- **Phase 1D-B (done):** independent typed **growth pipeline**
  (`src/timescape_fsigma8/growth/`): signed relative growth histories,
  exact analytic bare and dressed growth rates via −3Z/(ΘΔ_d) (no
  numerical differentiation), non-logarithmic derivatives, root-refined
  zero crossings with maximal piecewise validity intervals, and an
  optional solver-harmonic δ_m coefficient mapping →
  `reports/phase1d_b_growth_pipeline_validation.md`.
- **Later conditional checkpoints:** anchored density-growth Candidate A,
  H1 regional transfer and spectra, scalar dust-to-wall boost, and optional
  local wall metric-trace reconstruction. These do not supply observational
  power spectra, σ_R, σ8, fσ8, RSD/Kaiser, bias, likelihoods or fitting.

> **Read this before using the growth layer:** `Delta_d` is the CGI
> Laplacian density scalar, **not** the ordinary local density contrast;
> mapped `delta_m` values are solver-harmonic coefficients only. Relative
> growth and logarithmic rates are invariant under the fixed harmonic
> conversion. Growth rates are **piecewise** for trajectories with
> amplitude crossings (the barotropic rate has poles inside the observable
> window). D3 is **RESOLVED_DERIVED_4_10**; the printed branch remains an
> explicit forensic alternative. No observational fσ8, σ8, spectrum, or RSD quantity has been
> implemented. D2 remains excluded from the scientific package.

## Layout

| Path | Purpose |
|---|---|
| `UPSTREAM.lock` | Exact upstream repo URL, branch, commit SHA, retrieval date |
| `.reference/` | Read-only clone of the upstream repository (git-ignored) |
| `src/timescape_fsigma8/background/` | Independent tracker-background package (`parameters`, `tracker`, `effective_fluid`, `observables`); every function cites its paper equation |
| `src/timescape_fsigma8/perturbations/` | Perturbation package: pure Mészáros/comoving RHS functions (1C-B1) plus the barotropic system with mandatory explicit D3-branch/tilt/rate/epoch/wavenumber choices (1C-B2); explicit IC/epoch scenarios, solver layer, and residual diagnostics |
| `src/timescape_fsigma8/units.py` | Audited unit conversions from primary constants (IAU parsec, Julian year) |
| `src/timescape_fsigma8/presets.py` | Immutable parameter presets `PAPER_REFERENCE` (H0 = 73.03) and `NOTEBOOK_REFERENCE` (H0 = 73.23) |
| `tests/` | Validation suite: Buchert identities, limits, reference values, refactor equivalence, wall/dressed observables, epochs, domain validation, upstream-oracle comparison |
| `scripts/execute_upstream_notebook.py` | Executes the upstream notebook from a clean kernel |
| `scripts/extract_upstream_oracle.py` | Samples upstream background functions into the comparison oracle |
| `scripts/compare_to_oracle.py` | Full error statistics vs the oracle → `artifacts/independent/oracle_comparison_stats.json` |
| `scripts/make_independent_fig1.py` | Independent Fig.-1 reproduction (both presets) + D2 forensic figure |
| `scripts/extract_upstream_perturbation_oracle.py` | Read-only extraction of clean upstream Mészáros/comoving trajectories |
| `scripts/validate_clean_perturbations.py` | Oracle comparison, convergence, implicit cross-check, and IC/epoch scenario effects |
| `scripts/make_clean_fig2.py` | Independent clean Fig.-2 reproduction + local forensic overlay |
| `scripts/extract_upstream_barotropic_oracle.py` | Read-only in-memory extraction of upstream barotropic Fig.-3 trajectories |
| `scripts/validate_barotropic_perturbations.py` | Barotropic oracle comparison, convergence, D2/D3 factorial, and scenario effects |
| `scripts/make_barotropic_fig3.py` | Corrected-c²ₛ Fig.-3 variants for both D3 branches (raw and /k²) |
| `scripts/make_barotropic_fig3_forensic.py` | Forensic (D2-corrupted, upstream-reproduction) Fig.-3 variants |
| `scripts/_phase1c_b2_forensic.py` | Isolated forensic harness holding the D2-corrupted sound speed (never imported by the scientific package) |
| `src/timescape_fsigma8/growth/` | Phase 1D-B growth layer: mandatory-explicit scenarios, dust-mode histories, exact analytic rates, root-refined crossings/validity intervals, solver-harmonic δ_m mapping; Phase 1D-D anchored density-growth diagnostic (Candidate A, conditional and non-observational) |
| `src/timescape_fsigma8/perturbations/growing_mode.py` | Explicit Timescape regular growing-mode ICs for the clean systems (review F1) |
| `src/timescape_fsigma8/transfer/` | Phase 1E-F/1E-G conditional H1 transmission runtime (matrix contract, continuum-geometric backend and bridge) with the F3 kinematic gates |
| `src/timescape_fsigma8/phase1f_a/` | Phase 1F-A conditional forward realization: regional density/expansion inversion, carrier density, spectra, external boost, dressed map |
| `src/timescape_fsigma8/phase1f_b/` | Phase 1F-B conditional scalar dust-to-wall boost dynamics |
| `src/timescape_fsigma8/phase1f_c/` | Phase 1F-C conditional wall/common-spacetime kinematic geometry |
| `src/timescape_fsigma8/components.py` | Tensor-component ontology (coordinate/orthonormal representations, 1F-C-R) |
| `src/timescape_fsigma8/scientific_status.py` | Current cross-phase scientific classifications (1F-C-R successor record) |
| `scripts/validate_anchored_density_growth.py` | Phase 1D-D Candidate A validation (regenerable on any clean descendant of the 1D-D commit) |
| `scripts/validate_phase1f_a_h1_closure.py`, `scripts/validate_phase1f_b_dust_wall_boost_dynamics.py` | Phase 1F-A/1F-B validation drivers (deterministic artifacts) |
| `scripts/validate_phase1f_c_r_astra_remediation.py` | 1F-C-R provenance, equation-preservation and JSON checks (ancestry-based; reports post-remediation drift and absent local provenance) |
| `scripts/audit_numerical_tolerances.py` | AST inventory ensuring every numerical comparison states its tolerances |
| `scripts/validate_growing_mode_initial_conditions.py`, `scripts/validate_h1_kinematic_gates.py` | Review F1 and F3 validation drivers |
| `scripts/validate_growth_pipeline.py` | Growth-pipeline validation: frozen-bracket crossing checks, analytic identities, solver/root convergence, tilt equivalence, one-factor studies |
| `artifacts/upstream/` | Executed notebook copy, figures, logs, oracles (git-ignored: upstream-derived content with unclear licensing) |
| `artifacts/independent/` | Outputs of our own implementation: comparison statistics, reproduced figures |
| `reports/upstream_reproducibility.md` | Phase 1A reproducibility report |
| `reports/background_equation_audit.md` | Phase 1B equation audit |
| `reports/background_validation.md` | Phase 1B validation report (metrics, figures, environments, readiness) |
| `reports/phase1b_compliance_audit.md` | Compliance audit of Phase 1B (+ gap-closure addendum) |
| `reports/phase1c_perturbation_equation_audit.md` | Phase 1C-A equation/IC/epoch audit and D2/D3 map |
| `reports/phase1c_equation_inventory.json` | Machine-readable Phase 1C-A equation inventory |
| `reports/phase1c_b1_clean_systems_validation.md` | Phase 1C-B1 implementation, comparison, convergence, scenario, and readiness report |
| `reports/phase1c_b2_barotropic_validation.md` | Phase 1C-B2 barotropic implementation, upstream reproduction, D2/D3 factorial, and sensitivity report |
| `reports/phase1d_a_growth_observable_audit.md` | Phase 1D-A observable-definition audit (+ machine-readable `phase1d_a_observable_inventory.json`) |
| `reports/phase1d_b_growth_pipeline_validation.md` | Phase 1D-B growth-pipeline implementation and validation report |
| `reports/phase1d_c_*`, `phase1d_d_*`, `phase1d_d_t_*` | Observable-closure audit, Candidate A validation, D3 frame-mapping adjudication |
| `reports/phase1e_*` | Dressed-observable bridge, light-cone velocity, transfer closure, regional matching, realization selection, H1 and continuum H1 realizations (with adversarial audits) |
| `reports/phase1f_*` | 1F-A/1F-B/1F-C conditional runtimes, 1F-C-R remediation, the post-remediation review and its F1/F3/F2–F9 fixes |
| `AGENTS.md` | Permanent project rules (scientific-integrity constraints) |
| `pyproject.toml` | Package + minimal dependency declaration |

## Licensing note

The upstream repository contains **no license file**. Its code is treated as
all-rights-reserved reference material: it is cloned locally for audit only,
never committed to this repository, and never redistributed. See
`UPSTREAM.lock` and rule 6 of `AGENTS.md`.

## Reproducing the audit

Windows:

```
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -e ".[exec,test]"
.venv\Scripts\python scripts\execute_upstream_notebook.py
.venv\Scripts\python -m pytest -q
```

Linux/macOS (any CPython >= 3.11; phases are also validated on 3.11 in a
second environment `.venv311`):

```
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[exec,test]"
.venv/bin/python scripts/execute_upstream_notebook.py
.venv/bin/python -m pytest -q
```

The upstream clone goes in `.reference/` at the commit pinned in
`UPSTREAM.lock`. Its notebook is identified by a line-ending-independent
SHA-256 (`notebook_sha256_lf`), so LF and CRLF (`core.autocrlf`) checkouts
verify identically.

The script fails with a nonzero exit code if any notebook cell fails, writes
the executed copy to `artifacts/upstream/ACPT_Timescape.executed.ipynb`, and
records the environment and all captured output in
`artifacts/upstream/execution_log.json`. It never modifies the original
notebook.
