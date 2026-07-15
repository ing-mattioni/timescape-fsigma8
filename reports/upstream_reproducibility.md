# Upstream reproducibility report — `ACPT_Timescape.ipynb`

**Project:** timescape-fsigma8, Phase 1A (upstream reproduction audit)
**Date:** 2026-07-15
**Verdict:** ✅ The upstream notebook executes cleanly, end to end, in a fresh
environment, and its regenerated figures visually match both the outputs
stored in the notebook and (modulo the presentation-level differences noted
in §11) the published figures of arXiv:2511.17160v2.

**No scientific result has been independently validated.** This report
documents that the authors' code runs and reproduces itself; it does not
verify the equations against the paper's derivations (that is a later phase).

---

## 1. Environment and platform

| Item | Value |
|---|---|
| OS | Windows-11-10.0.22631-SP0 (AMD64) |
| Python (this audit) | 3.14.3 (CPython, `py -3.14` venv at `.venv/`) |
| Python (upstream authors) | 3.13.5 per notebook `language_info`; kernelspec display name `base` (Anaconda base env) |
| Execution mechanism | `scripts/execute_upstream_notebook.py` → `nbclient.NotebookClient`, fresh `python3` kernel, kernel CWD = `artifacts/upstream/` |
| Kernel warnings policy | `PYTHONWARNINGS=default` (surfaces warnings; no numerical effect) |
| Wall-clock duration | 40.2 s (all 20 cells) |
| Package index note | The machine's default pip index (corporate Artifactory) was unreachable; packages were installed from `pypi.org` (already in pip `trusted-host`) via per-command `--index-url`. No machine pip config was changed. |

Python 3.14.3 was the closest locally available version to the authors'
3.13.5 (3.14 default, 3.11, 3.10 installed). No 3.13-specific behaviour is
used by the notebook.

## 2. Upstream commit

| Item | Value |
|---|---|
| Repository | <https://github.com/MarcoGaloppo/Linear-Perturbations-in-averaged-cosmological-models> |
| Branch | `main` |
| Commit | `590c6fd5332acb15f5683ebf392a0d7ce54983c5` (2025-12-09 06:45:48 +0000) |
| Retrieved | 2026-07-15 (see `UPSTREAM.lock`) |
| Notebook | `ACPT_Timescape.ipynb` (repo root) |
| Notebook SHA-256 | `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a` |
| Integrity | Verified byte-identical before/after execution; `git status` of the clone clean. The original was never modified. |
| License | **None found** in the upstream repository → treated as all-rights-reserved, reference-only (AGENTS.md rule 6). |

## 3. Dependency inventory

**Direct imports (cell 0, the only imports in the notebook):**
`numpy`, `scipy.integrate.solve_ivp`, `matplotlib.pyplot`.

**Implicit dependencies:** a Jupyter kernel (`ipykernel`, which pulls in
`matplotlib-inline` for figure display); `nbformat`/`nbclient` for scripted
execution. No file inputs, no network access, no randomness, no compiled
extensions beyond the scientific stack itself.

**Resolved versions in this audit** (deliberately unpinned in
`pyproject.toml`; recorded per-run in `artifacts/upstream/execution_log.json`):

| Package | Version |
|---|---|
| numpy | 2.5.1 |
| scipy | 1.18.0 |
| matplotlib | 3.11.0 |
| nbformat | 5.10.4 |
| nbclient | 0.11.0 |
| ipykernel | 7.3.0 |
| jupyter_client | 8.9.1 |
| jupyter_core | 5.9.1 |

The upstream repo declares no dependency versions at all (no
requirements/environment files), so the authors' exact versions are unknown.

## 4. Notebook cell and execution-order inventory

20 cells, **all code, no markdown**. Stored execution counts are strictly
sequential (1–20): the saved state is a clean top-to-bottom run.
`nbformat` 4.5, kernelspec `base`/`python3`.

| Cell | Role | Depends on state from |
|---|---|---|
| 0 | imports | — |
| 1 | physical constants (`G_SI`, `c_SI`, `fv0`, `H0_SI`) | — |
| 2 | unit conversions (`h`, `GyrstoHT`, `MpctoHL`, `c=1`, `G`, `H0=1`) | 1 |
| 3 | derived background quantities (`HD0`, `rho0`, `a0`, `alpha`, `t0`) | 1–2 |
| 4 | `fv`, `dfvdt`, `d2fvdt` (void fraction) | 3 |
| 5 | `a`, `daDdt`, `Theta` (scale factor, expansion) | 3–4 |
| 6 | `rhod`, `RD`, `QD`, `dRDdt`, `dQDdt` (density, curvature, backreaction) | 3–5 |
| 7 | `UD`, `KD`, `dUDdt`, `dKDdt` (morphon energies) | 6 |
| 8 | `rhoEff`, `pEff`, derivatives, `wEff`, `cs2Eff` (effective fluid) | 7 |
| 9 | background arrays on `tf` (100 000 pts, 0.18 Gyr → `t0`); Ω variables | 4–8 |
| 10 | figure: energy balance → `TImescape_energy_balance.pdf` | 9 |
| 11 | figure: w_eff, c²_s,eff → `Timescape_wcs.pdf` | 9 |
| 12 | `solnum_barotropic(k, t_eval, ic)` — 4×4 linear ODE system | 4–8 |
| 13 | `solnum_comoving(t_eval, ic)` — 3×3 system (drops Ṽ(eff); its header comment still says "4x4") | 4–8 |
| 14 | `solnum_mezaros(t_eval, ic)` — 2nd-order Mészáros equation | 4–8 |
| 15 | `t_eval` (1000 pts, 0.218 Gyr → `t0`) and `ic` | 2–3 |
| 16 | run comoving + Mészáros solvers | 13–15 |
| 17 | figure: comoving vs Mészáros → `All_Perturbations_Timescape.pdf` | 16 |
| 18 | run barotropic for k ∈ {2π, 5π, 10π}; figure → `Bar_Dusts_Timescape.pdf` | 12, 15 |
| 19 | figure from cell 18's `sol_bar` dict → `Bar_Eff_Timescape.pdf` | 18 |

**Execution-order reliance:** strictly linear; every cell depends only on
cells above it. Cross-cell state: module-level constants (cells 1–3),
function definitions (4–8, 12–14), `tf` (9→10–11), `t_eval`/`ic` (15→16,18),
`sol_comoving`/`sol_mezaros` (16→17), `sol_bar`/`k_vector`/`colors`/`labels_k`
(18→19). **No nonlocal or hidden state**: no `%magics`, no globals mutated
inside functions, no file reads, no seeds.

Minor dead code: `zf = []` (cell 9) is created and never filled or used;
`c_SI` and `H0_SI` (cell 1) are defined but never used (see §11.1).

## 5. Scientific parameter inventory

Constants exactly as defined upstream (do not alter — AGENTS.md rules 1, 4):

| Name | Value | Units / meaning | Notes |
|---|---|---|---|
| `G_SI` | 4.49×10⁻¹⁵ | Mpc³/(Gyr²·M☉) | gravitational constant (CODATA ≈ 4.498×10⁻¹⁵) |
| `c_SI` | 3.06×10² | Mpc/Gyr | speed of light; **never used** (true value ≈ 306.6) |
| `fv0` | 0.737 | — | void fraction today; matches paper §5.1 |
| `H0_SI` | 7.47×10⁻² | Gyr⁻¹ | **never used**; equals 73.04 km/s/Mpc, though its comment claims 73.23 (see §11.1) |
| `h` | 0.7323 | — | dimensionless Hubble parameter actually used in all unit conversions (⇒ H0 = 73.23 km/s/Mpc) |
| `GyrstoHT` | h/9.778 | Gyr → Hubble-time | |
| `MpctoHL` | h/3000 | Mpc → Hubble-length | |
| `c` | 1 | code units | consistent with HL/HT units |
| `G` | ≈1.16432×10⁻²³ | HL³/(HT²·M☉) | converted from `G_SI` |
| `H0` | 1 | HT⁻¹ | code units |

Derived (cell 3), with values recomputed for this audit:

| Name | Expression | Value |
|---|---|---|
| `HD0` | 2H₀(2+fv0)/(4fv0²+fv0+4) | 0.792222 H₀ → **58.01 km/s/Mpc** for h=0.7323 |
| `rho0` | 12 HD0²(1−fv0)/(8πG(2+fv0)²) | ≈9.0359×10²⁰ M☉/HL³ |
| `a0` | 1+fv0/2 | 1.3685 (= a_D,0/a_w,0; paper: ≈1.37 ✓) |
| `alpha` | 9 fv0^(2/3) a0² HD0²/(c(2+fv0))² | ≈1.152184 |
| `t0` | (2+fv0)/(3 HD0) | ≈1.151613/H₀ ≈ 15.38 Gyr |

Numerical grids: background `tf` = 100 000 points on [0.18 Gyr, t0];
perturbations `t_eval` = 1000 points on [0.218 Gyr, t0] (times in code units
via `GyrstoHT`). Wavenumbers `k_vector = [2π, 5π, 10π]` in units of H₀/c
(matches paper Fig. 3 ✓).

## 6. Initial-condition inventory

Cell 15, applied at t = 0.218 Gyr × `GyrstoHT` (≈0.016327/H₀):

```
ic = [0.0031427229788258105, -0.16974050039281288, 0, 0]
```

ordered as [Δ(d), Z, Δ(eff), Ṽ(eff)] (barotropic system of cell 12).

- **Comoving solver** (cell 13) uses `ic[:-1]` — drops Ṽ(eff).
- **Mészáros solver** (cell 14) uses `[ic[0], -ic[1]]` for [δ, δ̇]. The sign
  flip is consistent with the first-order system's convention Δ′ = −Z
  (row 1 of the A matrix), so δ̇(tᵢ) = +0.16974….
- Paper cross-check (§5.1.2): Δ(d)(tᵢ) ≈ 3.1×10⁻³ ✓ (from ΛCDM growing mode,
  6×10⁻⁵ at CMB evolved to z=20); Z(tᵢ) ≈ −0.16 H₀ ✓ (notebook −0.16974,
  which rounds to −0.17; presentation-level difference only); Δ(eff)(tᵢ)=0 ✓;
  Ṽ(eff)(tᵢ)=0 ✓.
- The notebook's own comment describes the IC as "a typical dust perturbation
  on a co-moving scale of **150 Mpc/h at present time**", whereas the paper
  says the amplitude corresponds to **comoving wavelength c/H₀** seeded at
  the CMB epoch — see §11.3.
- The exact provenance of the 17-significant-digit values (which ΛCDM
  parameters produced them) is not documented anywhere in the notebook —
  see §12.

## 7. Solver and tolerance inventory

All three solvers use `scipy.integrate.solve_ivp` **with no options at all**
beyond `t_span`, `y0`, `t_eval`:

| Solver | System | Method | rtol | atol |
|---|---|---|---|---|
| `solnum_barotropic` | 4×4 linear, time-dependent A(t) | RK45 (default) | 1e-3 (default) | 1e-6 (default) |
| `solnum_comoving` | 3×3 linear | RK45 (default) | 1e-3 (default) | 1e-6 (default) |
| `solnum_mezaros` | 2nd-order scalar | RK45 (default) | 1e-3 (default) | 1e-6 (default) |

No Jacobian, no max_step, no dense_output, no stiffness handling. The paper
states only that "numerical solvers from the scipy Python library" were used;
**no tolerances are documented anywhere**. Whether the default rtol=1e-3 is
converged (especially for the unstable barotropic k=10π mode) is an open
question for scientific review (§12) — per the task constraints it was *not*
tightened here.

## 8. Generated-figure inventory

All five figures regenerated, written to `artifacts/upstream/` (the kernel's
CWD; relative `savefig` paths — the reference clone stays clean):

| Cell | File | Content | Paper counterpart |
|---|---|---|---|
| 10 | `TImescape_energy_balance.pdf` (typo "TI" is upstream's) | Ω_d, Ω_R, Ω_Q vs a_D/a_w,0 | Fig. 1 left |
| 11 | `Timescape_wcs.pdf` | w_eff, c²_s,eff | Fig. 1 right |
| 17 | `All_Perturbations_Timescape.pdf` | Δ(d)_com, Δ(d)_mz, Δ(eff)_com | Fig. 2 |
| 18 | `Bar_Dusts_Timescape.pdf` | \|Δ(d)_bar\| for k=2π,5π,10π | Fig. 3 left |
| 19 | `Bar_Eff_Timescape.pdf` | Δ(eff)_bar (un-normalised) | Fig. 3 right (paper plots Δ(eff)_bar **/k²** — see §11.2) |

**Visual comparison (this audit):** the regenerated inline PNGs of cells 10,
11, 17, 18, 19 were compared side-by-side against the outputs stored in the
upstream notebook. All match: same curves, same amplitudes, same features
(e.g. growth-rate reversal zero-crossings at a_D/a_w,0 ≈ 0.17 for k=10π and
≈ 0.41 for k=5π in cell 18). No byte-level comparison is meaningful across
matplotlib versions.

## 9. Execution outcome

**SUCCESS.** All 20 cells executed in order from a clean kernel with no cell
errors. Duration 40.2 s. Artifacts:

- `artifacts/upstream/ACPT_Timescape.executed.ipynb` — executed copy
- `artifacts/upstream/execution_log.json` — full machine-readable log
  (per-cell stdout/stderr, versions, platform, commit, SHA-256)
- 5 PDF figures (see §8)

No compatibility patch was needed; no patched copy exists.

## 10. Warnings and errors

- **Notebook cells: zero warnings, zero errors** — even with
  `PYTHONWARNINGS=default` forced in the kernel. The only cell stderr was
  matplotlib's benign first-run message "building the font cache" (cell 0).
- **Runner infrastructure (not the notebook):** the host process printed
  warnings from the Jupyter stack on Python 3.14/Windows: a pyzmq
  `RuntimeWarning` about the Proactor event loop, four ipykernel
  `DeprecationWarning`s about `asyncio` event-loop-policy APIs slated for
  removal in Python 3.16, and an ipykernel notice about unencrypted local
  TCP kernel transport. These originate in `ipykernel`/`pyzmq` startup code,
  are unrelated to the notebook's science, and were not suppressed
  (AGENTS.md rule 10: cause documented here).
- No numerical warnings (overflow, divide-by-zero, `LinAlgWarning`, solver
  failures) occurred.

## 11. Apparent mismatches with arXiv:2511.17160v2

Recorded exactly; **none were "fixed"** (task constraint 5).

1. **Hubble constant 73.23 vs 73.03 km/s/Mpc.** The paper (§5.1.1, Fig. 1
   caption) states H₀ = 73.03 km/(s·Mpc) from the best fit of its ref. [80].
   The notebook's conversions all use `h = 0.7323` (⇒ 73.23). Notably:
   - the notebook's *unused* `H0_SI = 7.47e-2 Gyr⁻¹` equals **73.04**
     km/s/Mpc — i.e. it matches the *paper's* value, while its own comment
     ("which is 73.23") matches the *used* `h`;
   - the paper's own derived value H_D,0 ≈ 58.01 km/s/Mpc is reproduced by
     0.792222 × **73.23** = 58.01, whereas 0.792222 × 73.03 = 57.86. So the
     paper's quoted H_D,0 is consistent with the notebook's 73.23, not with
     the paper's own 73.03.
   Impact on results: H₀ enters only through unit conversions (`G` in code
   units; Gyr→code-unit start times), a ≲0.3 % effect. Which value is
   intended must be resolved by scientific review (or the authors).
2. **Fig. 3 right panel normalisation.** The published figure plots
   Δ(eff)_bar **/k²** (y-range 10⁻⁵–10⁰); notebook cell 19 plots the raw
   \|Δ(eff)_bar\| with ylim 10⁻⁴–10⁰. The published panel was evidently made
   with a modified version of this plotting cell. Presentation-level only;
   the underlying solutions are the same.
3. **Initial-condition description.** Notebook comment: dust perturbation on
   a comoving scale of **150 Mpc/h at present time**. Paper: typical
   amplitude at comoving wavelength **c/H₀** (≈3000/h Mpc) seeded from the
   CMB epoch and evolved to z=20. The numeric values match the paper's
   quoted ≈3.1×10⁻³ and ≈−0.16 H₀, so this appears to be a stale/incorrect
   code comment rather than a numerical difference.
4. **Start times.** The paper describes Figs. 1–3 as starting from z = 20.
   The notebook uses **0.218 Gyr** for the perturbation integration but
   **0.18 Gyr** for the background/Ω figures (cell 9). Whether 0.218 Gyr is
   exactly t(z=20) in this timescape parametrisation, and why the background
   plots start earlier, is unverified (§12).
5. **Rounding of Z(tᵢ).** Paper: ≈ −0.16 H₀; notebook: −0.16974 H₀ (rounds
   to −0.17). Cosmetic.

Consistencies confirmed: fv0 = 0.737 ✓; k ∈ {2π, 5π, 10π} in H₀/c units ✓;
a_D,0/a_w,0 = 1+fv0/2 ≈ 1.37 ✓; ICs [≈3.1×10⁻³, ≈−0.16 H₀, 0, 0] ✓;
H_D,0 ≈ 58.01 km/s/Mpc ✓ (with h=0.7323); Mészáros formally applied despite
paper's caveat that it should not hold ✓; figure content and axis ranges of
Figs. 1–3 ✓ (modulo item 2).

## 12. Uncertainties requiring scientific review

1. **Which H₀ is canonical** — 73.03 (paper text, unused `H0_SI`) or 73.23
   (used `h`, and consistent with the paper's H_D,0 ≈ 58.01)? Check ref. [80]
   of the paper (timescape SNe best fit).
2. **Epoch of the initial conditions:** verify that t = 0.218 Gyr (volume-
   average time) corresponds to z = 20 under the timescape redshift relation
   1+z = a_w,0/a_w = γ_w (a_D/a_w,0)⁻¹ with γ_w = 1+f_v/2, and identify what
   epoch 0.18 Gyr (background plots) corresponds to.
3. **Solver convergence:** all results use `solve_ivp` defaults
   (RK45, rtol=1e-3, atol=1e-6). No convergence study exists in the notebook
   or the paper. The barotropic k=10π solution grows by ~3 orders of
   magnitude and reverses sign — sensitivity to tolerances must be checked in
   the independent implementation (never by editing upstream).
4. **Provenance of the IC values** 0.0031427229788258105 and
   −0.16974050039281288: which ΛCDM parameters (Ω_m, growth normalisation)
   generated them, and are they exactly reproducible?
5. **Fig. 3 right panel:** confirm the published /k² normalisation and
   y-range against the notebook's un-normalised plot (which notebook version
   produced the paper figure?).
6. **Equation-level verification** (deferred to the independent
   implementation phase): the closed forms for f_v(t), a(t), curvature
   `RD(t)` (with the `alpha` coefficient), backreaction `QD(t)`, the morphon
   energy definitions (cells 7–8), and the A-matrix entries of the barotropic
   (4×4) and comoving (3×3) systems against the corresponding equations of
   arXiv:2511.17160 (e.g. Eq. (4.27) for Mészáros; §5.1 for the timescape
   background). Note cell 13's header comment says "4x4" for a 3×3 matrix.
7. **Unused constants** `c_SI` (3.06×10², slightly rounded from 306.6) and
   `H0_SI`: confirm they are vestigial and carry no hidden role.
8. **Physical-units sanity** of `G_SI` = 4.49×10⁻¹⁵ Mpc³/(Gyr²·M☉)
   (reference value ≈ 4.498×10⁻¹⁵; 0.2 % rounding enters `G` in code units).
9. **Radiation neglected, K_D = 0:** the paper states both assumptions; the
   notebook contains no radiation and no K_D term. Confirm intended
   equivalence (rather than omission) at the equation level.
10. **Dead variable `zf`** (cell 9) — presumably an abandoned redshift array;
    confirm nothing downstream was meant to use it.

---

*Generated by the Phase 1A audit. Upstream code remains reference-only
(no license); the executed copy and figures under `artifacts/upstream/` are
git-ignored and must not be redistributed.*
