# Independent post-remediation scientific review — Phases 1A to 1F-C-R

Audit classification: `INDEPENDENT_READ_ONLY_POST_REMEDIATION_REVIEW`.

Checkpoint reviewed: `118b8f3af3c1360b0da74df8e9a9cb3ba1fed83a`
(`main` = `origin/main` = HEAD of the review branch
`claude/loving-dijkstra-esoj6f`). Review date: 2026-09-23.

Machine-readable companion:
[`phase1f_c_r_post_remediation_independent_audit_inventory.json`](phase1f_c_r_post_remediation_independent_audit_inventory.json).

The Phase 1F-C-R report closes with
`INTEGRATION_READINESS: READY_FOR_INDEPENDENT_POST_REMEDIATION_AUDIT`. This
document is that audit, extended at the user's request to a complete revision
of the project: the implementation and, above all, the theoretical scientific
results of every phase from 1A to 1F-C-R. Per the user's instruction, errors
are described, not fixed.

## 1. Verdict summary

- **Phases 1A–1D (background, perturbations, growth).** No error was found in
  any implemented equation. D1, D2 and the D3 verdict `RESOLVED_DERIVED_4_10`
  are independently confirmed. Every quoted numerical result that was
  re-computed was reproduced to the printed digits by a from-scratch
  implementation (Appendix A).
- **Phases 1E–1F (theory audits and conditional runtimes).** All re-derived
  identities are correct. The no-go and conditional verdicts are sound.
  However, the "conditional closure" status of the H1 runtime is not
  demonstrated (F3), and its authorization and specification provenance is
  not in the repository (F4).
- **Findings.** Nine open findings (F1–F9): one MEDIUM-HIGH, three MEDIUM,
  two LOW-MEDIUM and three LOW. None invalidates a load-bearing implemented
  equation. The most consequential is scientific (F1): the paper's initial
  conditions carry a sizeable decaying mode. That mode inflates the
  reproduced amplitudes by about 13–14% and accounts for most of the reported
  "rate-unit" and "epoch" convention effects.

Nothing in the repository was modified to produce this review; see Sec. 9.

## 2. Checkpoint and environment

| Item | Value |
|---|---|
| repository | `ing-mattioni/timescape-fsigma8` |
| reviewed commit | `118b8f3af3c1360b0da74df8e9a9cb3ba1fed83a` (2026-09-06), equal to `main` and `origin/main` |
| upstream | `590c6fd5332acb15f5683ebf392a0d7ce54983c5`, matching `UPSTREAM.lock` |
| upstream notebook SHA-256 | `628c441288d67854e0380518841dede3680bddab610e9ef5cea04937455cea2a` for the committed file content (LF line endings, as produced by any checkout without `core.autocrlf`); the pinned `86d2534d…afe55a` is reproduced only with `core.autocrlf=true` (see F6) |
| platform | Linux cloud container (earlier phases were validated only on Windows 11) |
| environment 1 | CPython 3.13.12, NumPy 2.5.3, SciPy 1.18.1, Matplotlib 3.11.2, pytest 9.1.1 |
| environment 2 | CPython 3.11.15, NumPy 2.4.6, SciPy 1.17.1, Matplotlib 3.11.2, pytest 9.1.1 |

Python 3.14 is not installed in the container; 3.13 was used as the closest
available interpreter.

**Test suite** (`pytest -q -p no:cacheprovider`, after regenerating the
git-ignored oracles): **653 passed, 1 skipped** in both environments. The skip
is `tests/test_anchored_density_growth.py:609`. That test needs the Phase 1D-D
artifact, and the artifact's validator can only run on a historical branch
(F6).

**Validation drivers** (all from `scripts/`):

| Driver | Outcome |
|---|---|
| `execute_upstream_notebook.py` | success, 0 notebook warnings |
| `extract_upstream_oracle.py`, `extract_upstream_perturbation_oracle.py` | success |
| `extract_upstream_barotropic_oracle.py` | exit 4 on the LF checkout (hash gate, F6); success after re-cloning with `core.autocrlf=true` |
| `compare_to_oracle.py` | exit 0 (its `<1e-9` equivalence gate passed) |
| `validate_clean_perturbations.py` | oracle worst normalized L∞ `7.350e-16`; tight explicit vs reference `2.341e-10`; Radau `1.879e-11` |
| `validate_barotropic_perturbations.py` | oracle worst normalized L∞ `1.476e-14`; tight explicit `3.139e-9`; Radau `2.529e-11` |
| `validate_growth_pipeline.py` | "gates PASSED" |
| `validate_phase1f_a_h1_closure.py`, `validate_phase1f_b_dust_wall_boost_dynamics.py` | exit 0 |
| `make_independent_fig1.py`, `make_clean_fig2.py`, `make_barotropic_fig3.py`, `make_barotropic_fig3_forensic.py` | exit 0 |
| `audit_numerical_tolerances.py` | 0 missing explicit tolerances |
| `validate_anchored_density_growth.py` | cannot run: requires branch `phase-1d-d-anchored-density-growth` (F6) |
| `validate_phase1f_c_r_astra_remediation.py` | cannot run: requires `main == 63d2104…` and three untracked local files (F4, F6) |

## 3. Method, evidence policy and limitations

- **Independent derivation.** Every load-bearing equation listed in Sec. 4
  was re-derived by hand from first principles or from the cited definitions,
  not from the project's reports.
- **Independent numerics.** A from-scratch implementation of the tracker
  background and of the three CGI systems (Appendix A.0–A.2) uses no project
  code. Appendix A.3 deliberately evaluates the project's own test fixture.
- **Reading.** All 56 committed report files (40 Markdown, 16 JSON) were read.
  `background/`, `perturbations/` and `growth/` were read in full. The
  `transfer/`, `phase1f_a/`, `phase1f_b/` and `phase1f_c/` runtimes (about
  9,500 lines) were reviewed at the level of their load-bearing equations,
  closure gates and flagship fixtures, not line by line.
- **Classification vocabulary.** The project's own tokens are used, with one
  primary classification per finding.
- **Severity scale.**
  - `HIGH`: invalidates a load-bearing result. None found.
  - `MEDIUM-HIGH`: materially changes a quantitative result or its
    interpretation without invalidating the equations.
  - `MEDIUM`: incorrect statement, or a status claim not supported by the
    evidence.
  - `LOW-MEDIUM`: governance, documentation or reproducibility defect with
    scientific-record impact.
  - `LOW`: minor or cosmetic.

**Limitations.**
1. `arxiv.org` was blocked by the container's network policy, so the
   arXiv:2511.17160v2 PDF was not inspected. Statements about what the paper
   *prints* rely on the project's transcriptions. These include equation
   numbers, the printed sign in (4.15), the printed prefactor behind D1, and
   the Λ-coefficient issue recorded as 1C-A finding F5. Everything else was
   re-derived.
2. The DBE/BDE scans, W09, Kaiser and Percival–White were not re-inspected.
   Where their equations are load-bearing they were re-derived.
3. The notebook's 17-digit initial `Z` could not be reproduced bit-exactly
   under SciPy 1.18.1. The reconstruction gives `−0.16974050044476324`, versus
   `−0.16974050039281288` upstream: a difference of `5.2e-11`, inside the
   project's documented `2e-10` cross-SciPy gate. `Δ_d` remains bit-exact.

## 4. Independently verified results

These items hold. All were derived by the reviewer; numbers are from
Appendix A unless stated otherwise.

**Background (1B).**
- The tracker forms are correct: `H_D=(2+f_v)/(3t)`,
  `H=(4+f_v+4f_v²)/(6t)=γ_wH_D−γ̇_w`, `τ_w` (W09 B12), the dressed redshift and
  the three Ω's.
- The Buchert derivatives are correct: `Q̇_D=−2f_v(1−f_v)(1+2f_v)/(3t³)` and
  `Ṙ_D=6f_v(1+f_v)/t³`. The integrability condition (3.11) holds identically.
- The effective fluid is correct: `ρ_eff`, `p_eff`,
  `ρ̇_eff=−f_v(2+f_v)²/(12πGt³)` and `ṗ_eff`.
- The corrected sound speed is `c²_s=−(2+2f_v−f_v²)/(2+f_v)²`: `−0.391238` at
  `t0`, against `w_eff(t0)=−0.373469`. Since
  `c²_s−w_eff=−6f_v(1−f_v)/[(2+f_v)²(8+f_v)]<0`, `c²_s<w_eff` for every
  `f_v∈(0,1)`.
- **D2** is confirmed. In the notebook's `dQ_D/dt`, the first quotient-rule
  term multiplies by `3f_v(1−f_v)` where it must divide.
- **D1** is consistent. With `⟨R⟩_D=−6f_v/t²`, `Ω_m+Ω_R+Ω_Q=1` exactly.
- **Epochs.** `z(0.218 Gyr)=18.586475`, `z(0.18 Gyr)=21.233273`,
  `t(z=20)=0.19620643 Gyr`. The flat-ΛCDM (Planck 2018) age at `z=20` is
  `0.17906 Gyr`.
- **Presets.** `H_D0=58.01` km/s/Mpc for `H0=73.23`, and `57.86` for `73.03`.

**Perturbations (1C).**
- All Mészáros, comoving and barotropic matrix entries are correct.
- The equivalence of the `V` and `Ṽ` tilt forms via
  `ẇ=−Θ(1+w)(c²_s−w)` is confirmed.
- **D3.** A first-principles dust-frame derivation for a tilted barotropic
  fluid gives the self-coupling `(w_eff−c²_s)Θ`, using
  `h_a^b(D_bf)˙=D_aḟ−(Θ/3)D_af` and `A_a=0`. Paper Eq. (4.29) follows exactly
  from the derived chain with the adiabatic closure, and not from the printed
  one.
- Both second-order `Δ_eff` equations were re-derived coefficient by
  coefficient: `C_printed`, which is consistent with printed (4.15), and
  `C_derived`.
- The residual equations (4.24)–(4.26) at `Λ=0` were re-derived.
- The incomplete-beta closed form for `q₊` (flat ΛCDM, `D/a→1`) was
  re-derived.
- **Endpoints.** Comoving `Δ_d(t0)=0.0386165401` and `Δ_eff(t0)=0.0070813934`;
  Mészáros `0.0331504916`. All six barotropic endpoints match 1C-B2 §10: for
  example `derived_4_10`, `10π` gives `Δ_d(t0)=−2.721593e14` and
  `Δ_eff(t0)=3.545589e17`.
- The `paper_lcdm_hubble_k` factor `1.2595507305749012` is correct.

**Growth (1D).**
- `f_bare=−3Z/(ΘΔ_d)` is correct, as is the chain factor
  `γ_wH_D/H=(2+f_v)²/(4+f_v+4f_v²)`. Its range statement is wrong; see F2.
- The harmonic mapping `Δ_d,k=−k²_code δ_m,k` and its cancellation in ratios
  and logarithmic rates are correct.
- 1D-B values reproduced: the `derived_4_10`, `2π` root at
  `t=0.7851615735`; `G(t0;z_ref=10)=+4.7326` (`printed_4_15`) and `−6.1617`
  (`derived_4_10`); `f_bare(t0)=0.14661` and `4.34190`.
- Candidate A: `G(t0;z_ref=10)=6.322867` and `f_bare(t0)=0.4251006`
  (comoving).
- 1D-C Fourier-rescaling Jacobians: `P_new(k)=λ³P_old(λk)` and
  `Δ²_new(k)=Δ²_old(λk)`.

**Theory audits (1E-A to 1E-D).**
- 1E-A: Kaiser multipole coefficients, AP scalings, and the chain factors at
  z = 20, 10, 1 and 0.
- 1E-B: `δΘ=−3ψ̇−3Hφ+a⁻¹∂_iv^i`, and the plane-parallel Jacobian
  `δ_s=δ_g−(aH)⁻¹∂_∥v_∥`.
- 1E-C and 1E-D: the first-order boost laws, the Buchert commutation rule and
  the lapse-ratio variation.
- The regional CGI pair and its linearised Hamiltonian constraint,
  `ℛ_r=−(4/3)Θ_rZ_r+16πGρ_rΔ_r`.
- The partition kinematics `ḟ_v=f_vf_w(Ξ_v−Ξ_w)` and its linearisation.
- The two-region `Q_D=f_wQ_w+f_vQ_v+(2/3)f_wf_v(Θ_w−Θ_v)²`. With EdS walls and
  Milne voids it reproduces the tracker's `Q_D=(2/3)f_v(1−f_v)/t²`.
- The `Δ̂_eff` and `P̂̃_eff` normalisations, the mismatch propagation including
  its `C_P/4` coefficient, and the intertwining residual `R_T`.

**Runtimes (1E-F to 1F-C).**
- 1E-F: `A_Q`, `B_Q`, `A_W`, `A_P=A_W−3A_Q` and `B_P=−3B_Q`; the dust-transfer
  weights `m_w`, `m_v`, `d_F`; `P̃_eff=−C_P/[3(Q̄+W̄)]`; the residual forms; and
  the first- and second-derivative jets of the regional evolution.
- 1E-G: the discrete Laplacian eigenvalues `(2N sin(π/N))²`, which give
  `37.4903`, `38.9737`, `39.3517` and `39.4467` and tend to `4π²`.
- 1E-G bridge inputs: `E_ΔΘ=T_v[Z_v]−T_w[Z_w]` and
  `E_ΔΞ,0=α_vT_v[Z_v]−α_wT_w[Z_w]`.
- 1F-A: the inversions `Δ_γδ=Δ` and `Δ_γδΘ=Z`, each with an explicit
  zero-mean closure.
- 1F-B: `D·v=δΘ_d−δΘ_W`. From `A_d=A_W+v̇+Hv` with geodesic dust,
  `v̇+Hv=−Dν`, which gives `∂_tψ=−α_W Q₀ν`. The propagation diagnostic in
  physical orthonormal components is consistent.
- 1F-C: `A_i=D_iν`. The trace law
  `∂_tC_W=H^(t)_Wν_W+(α_W/3)δΘ_W` follows from `h_ij=a²(1+2C)γ_ij` and
  `N=ᾱ(1+ν)`. The orthonormal components `LᵀA/a` with `γ⁻¹=LLᵀ` are correct.

## 5. Findings

All findings have status `OPEN_NOT_FIXED`.

### F1 — The initial conditions are not the Timescape growing mode (MEDIUM-HIGH)

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS` (supporting:
`NUMERICALLY_CORROBORATED`).

**Locations:**
- `src/timescape_fsigma8/perturbations/initial_conditions.py`
  (`RateUnitConvention`, `InitialConditionScenario.resolve`);
- `reports/phase1c_perturbation_equation_audit.md` §5 (F3);
- `phase1c_b1_clean_systems_validation.md` §9;
- `phase1c_b2_barotropic_validation.md` §9;
- `phase1d_a_growth_observable_audit.md` §6 (lines 349–363);
- `phase1d_b_growth_pipeline_validation.md` §19;
- `phase1d_d_anchored_density_growth_validation.md` §17.

**Statement.** The dust initial conditions are the flat-ΛCDM growing mode at
`z=20`, expressed as a ΛCDM rate. The rate is `−Z_i/Δ_d,i=54.0106` in H₀ units
(`upstream_unconverted`), or `49.7107` after the `lcdm_to_timescape_converted`
rescaling. On the frozen tracker background, the regular (growing-mode)
solution of the same equations has at `0.218 Gyr`:
- `−Z/Δ_d=40.0878` (comoving) and `d ln Δ_d/dt=39.8503` (Mészáros);
- `Δ_eff/Δ_d=0.20005`, the comoving attractor `Δ_d/5` for `w_eff→−1/2`.

At the dressed `z=20` epoch the corresponding rates are `44.6209` and
`44.3828`. The initial conditions therefore excite the decaying solution,
which falls off relative to the growing mode as `(t_i/t)^{5/3}` in the EdS
limit.

**Size of the effect** (Appendix A.2). Each ratio compares a run with the
notebook dust ICs to a growing-mode run with the same `Δ_d(t_i)`; entries are
comoving / Mészáros.

| IC convention | `Δ_d(t0)` ratio | bias in `G(t0; z_ref=10)` | bias in `f_bare` at z = 0 / 1 / 2 / 5 (comoving) |
|---|---|---|---|
| unconverted, 0.218 Gyr (notebook) | 1.1312 / 1.1398 | +2.58% / +2.99% | +0.05% / +0.12% / +0.27% / +1.45% |
| unconverted, dressed z=20 | 1.0771 / 1.0855 | +1.17% / +1.59% | −0.02% / +0.01% / +0.07% / +0.65% |
| converted, 0.218 Gyr | 1.0882 / 1.0974 | +1.66% / +2.15% | −0.01% / +0.03% / +0.12% / +0.92% |
| converted, dressed z=20 | 1.0384 / 1.0473 | +0.43% / +0.91% | −0.06% / −0.07% / −0.06% / +0.21% |

Almost all of the excess comes from the transplanted dust rate `Z_i`. The
paper's deliberate choice `Δ_eff(t_i)=0` contributes only about `−0.8%`: at
the notebook epoch, `Δ_d(t0)` relative to the growing mode is `1.1312`
(notebook ICs), `0.9920` (growing-mode `Z_i` with `Δ_eff=0`) and `1.1392`
(notebook `Z_i` with the attractor `Δ_eff`).

**Consequences.**
1. The reproduced Fig. 2 amplitudes, and every quoted endpoint amplitude, are
   about 13–14% above the growing-mode evolution of the same initial `Δ_d`.
   This is a property of the paper's IC prescription, which the project
   reproduces faithfully but never identified as such.
2. The "rate-unit" and "epoch" one-factor effects are not independent
   physical conventions. The effects in question are −3.8% and +2.0% in
   1C-B1 §9, the corresponding 1C-B2/1D-B/1D-D rows, and ΔG = −0.056 and
   −0.086 in 1D-D §17. They mostly measure how much of the same decaying
   transient each choice injects. Even the combination closest to the growing
   mode (converted rate, dressed z = 20) leaves `+3.8%` in the comoving
   `Δ_d(t0)`.
3. Candidate A inherits a `+0.4%` to `+2.6%` bias in `G(t0;z_ref=10)`. The
   baseline gives `6.322867`, against `6.164012` for the growing mode. The
   bias in `f` is below 0.3% at `z≤2` but 1–1.8% at `z=5`. Growing-mode
   `f_bare(t0)` is `0.42491` (comoving) and `0.31000` (Mészáros).
4. 1D-A §6 (lines 349–363) states that "a physical spectrum satisfies [the
   k-independent mixture condition] only under growing-mode dominance at t_i.
   This assumption must be stated by any future implementation." No later
   phase checks it, and no available IC option realises the Timescape growing
   mode.

This is not an implementation error: the systems and the reconstruction of the
paper's ICs are correct. The issue is that the IC prescription is
inconsistent with the background it is used in.

**Suggested resolution** (non-binding; an IC change requires human approval
under AGENTS.md rules 1 and 4):
- add an explicit, non-default IC convention that places the dust on the
  tracker's regular solution;
- report the decaying-mode fraction of every other convention;
- restate the convention studies relative to that growing mode.

### F2 — The bare-to-dressed growth-rate factor is not bounded by 1.025–1.084 (MEDIUM)

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS` (supporting:
`NUMERICALLY_CORROBORATED`).

**Locations:**
- `phase1d_a_growth_observable_audit.md` line 688 ("rescales fσ8 by
  1.02–1.08") and line 832 ("= 1.025–1.084");
- `phase1d_a_observable_inventory.json` line 237;
- `phase1d_c_observable_closure_audit.md` line 906;
- `phase1d_c_closure_inventory.json` line 263;
- `phase1d_c_compliance_audit.md` line 525.

Line 435 of 1D-A is correctly restricted to "these audited epochs".

**Statement.** Write `g(f)=(2+f)²/(4+f+4f²)`. Then

    g'(f) = (2+f)(6−15f)/(4+f+4f²)²,

so `g` is not monotonic. Its maximum is `g(2/5)=8/7=1.142857`, reached at
dressed `z=2.007` (`t=3.66 Gyr`). Values along the tracker history:

| z | 20 | 10 | 3 | 2 | 1 | 0.5 | 0.3 | 0 |
|---|---|---|---|---|---|---|---|---|
| `f_dressed/f_bare` | 1.0248 | 1.0579 | 1.1361 | 1.1429 | 1.1307 | 1.1124 | 1.1024 | 1.0842 |

Throughout `0.3≲z≲3` the factor is 1.10–1.14, above the quoted upper bound.
The quoted range came from three sampled epochs (z = 20, 18.6 and 0).

**Consequence.** Any statement about the size of the bare-versus-dressed
spread of an fσ8-like number understates it by up to about 6 percentage
points in the observable window. The 1E-A report later quotes `1.1307` at
`z=1`, but the earlier range statements were never corrected.

**Suggested resolution:** a successor erratum. Historical reports remain
frozen.

### F3 — The H1 realization's "conditional closure" is not demonstrated (MEDIUM)

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS` (supporting:
`NUMERICALLY_CORROBORATED`).

**Locations:**
- `src/timescape_fsigma8/transfer/h1_realization.py` lines 487–765: `J_Xi` is
  computed at 627–633 and returned at 742 without any gate;
- `tests/test_phase1e_g_continuum_h1.py` lines 1185–1246
  (`_continuum_dynamic_fixture`) and 1249 (`test_n7_n8_…`);
- `tests/test_phase1e_f_h1_transfer.py` lines 205–262;
- reports 1E-E §11 (clock dictionary, row `CLK-H1`), 1E-F §§6–7, 1E-G
  "Effective-sector bridge" and status block, and 1F-C-R A07.

**(a) The clock mismatch `J_Ξ` is unconstrained.** The runtime fixes `F_v`
algebraically from the constitutive closure `C_P=0` and then computes

    J_Ξ = [Ḟ_v − A_f F_v − f_v f_w E_ΔΞ,0 − J_f]/(f_v f_w),

which is the residual of the linearised partition kinematics (1E-D §17,
H-D5). It is returned but never tested. Under the H1 clock branch `CLK-H1` of
1E-E §11 (rate homogeneous, spatial dependence `EXCLUDED`, perturbative lapse
`NOT_DEFINED`), a clock mismatch has no admissible source. The same holds
explicitly on the 1E-G branch: homogeneous clock, fixed Lagrangian partition,
`J_f=0`, and `E_ΔΞ,0=α_vT_v[Z_v]−α_wT_w[Z_w]` equal to the complete
`ℰ_ΔΞ=L_D(δΞ_v−δΞ_w)`. Consistency therefore requires `J_Ξ≡0`. The adversarial
audits of 1E-F and 1E-G record only "no arbitrary `J_Xi` history: PASS".

**(b) No zeroth-order identity of the two-region model is validated.** The
runtime checks `Θ_r=3H_r`, positivity and non-degeneracy, but none of the
following, all of which hold for two exact dust-FLRW regions at `Λ=0`:
- the regional Friedmann constraints `R̄_r=16πGρ_r−6H_r²`;
- regional dust conservation `ρ̇_r=−α_rΘ_rρ_r`;
- background partition kinematics `ḟ_v=f_vf_w(Ξ_v−Ξ_w)`;
- the two-region backreaction `Q̄=(2/3)f_vf_w(Θ_v−Θ_w)²`, which is never
  negative;
- `W̄=f_wR̄_w+f_vR̄_v−6K_D/a_D²` (`K_D` is not an input; GM Timescape uses
  `K_D=0`);
- `Θ=f_wΞ_w+f_vΞ_v`.

**(c) Evidence.** The project's "nontrivial continuum-derived manufactured
trajectory" is the evidence 1E-G cites for non-trivial `R_Z`/`R_eff`
cancellation. It passes every gate, with `|R_Z|≤4.8e-15`, `|R_eff|≤1.5e-15`
and `|C_P|≤1.1e-16`, yet it violates the model's own kinematics (Appendix
A.3):

| Quantity | Fixture | Model requirement |
|---|---|---|
| `J_Ξ` (`E_ΔΞ,0∈[−1,0.2]`, `J_f=0`) | `[−26.65, 5.33]` | `0` |
| wall Friedmann residual | `−3.760` | `0` |
| void Friedmann residual | `−3.148` | `0` |
| dust conservation residuals, wall / void | `+0.6` / `+1.2` (the wall value is acknowledged by A07) | `0` |
| partition-kinematics residual | `−0.144` | `0` |
| `Q̄` | `−5` | `+0.0576` |
| `W̄` | `−3` | `−0.043` at `K_D=0` (the fixture needs `6K_D/a_D²=2.957`) |
| `Θ` vs `f_wΞ_w+f_vΞ_v` | `0.84` vs `0.84` | satisfied |

The fixture's `Q̄` time derivative (`−26.979…`) is tuned so that `R_eff`
cancels.

**Consequence.** The status tokens `CONDITIONALLY_CLOSED` (1E-F, 1E-G) and
`CONDITIONALLY_DERIVED_CONTINUUM_REALIZATION` (1E-G) are not supported by any
exhibited state that satisfies the model's zeroth- and first-order
kinematics, not even at a single instant. Of the closure gates, only `R_Z`
and `R_eff` are independent; `C_P`, `R_Δ` and `K_GM` are identities by
construction, as the project states. 1F-C-R's reclassification of
manufactured trajectories as `ALGEBRAIC_VALIDATION_ONLY` is correct, but it
names only the dust-conservation defect. Whether any non-trivial state
satisfies `C_P=0`, `R_Z=R_eff=0`, `J_Ξ=0` and the background identities
simultaneously is an open question.

**Suggested resolution:**
- add fail-closed gates for `J_Ξ=0` on `CLK-H1`, and for the background
  identities with `K_D` as an explicit input;
- exhibit at least one manufactured state satisfying all of them;
- or downgrade the status tokens.

### F4 — Authorization, specification and audit provenance missing from the repository (MEDIUM)

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

**Locations:**
- `phase1e_e_transfer_realization_selection.md` lines 9, 17, 19, §11, §38 and
  902–919;
- `phase1e_e_transfer_realization_correction_verification.md` lines 167–177;
- `phase1e_f_h1_transfer_realization.md` lines 7–13;
- `transfer/matrix_backend.py` lines 7 and 133;
- `transfer/continuum_backend.py` lines 4, 597, 976, 991, 1098 and 1293;
- `transfer/continuum_bridge.py` line 9;
- `transfer/continuum_geometry.py` lines 95 and 345;
- `transfer/h1_realization.py` lines 393, 579, 584, 608, 618 and 627;
- `phase1f_c_r_astra_audit_remediation_inventory.json` lines 458–463.

**Statement.**
1. **The H1 decision and grant are unrecorded.** 1E-E (committed 2026-08-12)
   ends with:
   - S1 as `PRIMARY_SELECTED_CONDITIONALLY`;
   - H1 as `MANDATORY_SECONDARY_COMPARATOR`;
   - implementation and prototype authorization `NOT_GRANTED`;
   - overall `PARTIAL_REALIZATION_DEFICITS_REMAIN` / `NEW_DYNAMICS_REQUIRED`.

   Its correction verification repeats `NOT_GRANTED`. 1E-F (committed
   2026-08-18) implements H1 with "Scientific implementation authorization:
   GRANTED" and "Scientific status: CONDITIONALLY_CLOSED". No committed
   document records the S1-to-H1 change, the grant, or how the 1E-E deficits
   were closed. 1E-E itself states (line 19) that it was produced outside the
   Git checkout and was not Git-verified.
2. **The specifications are not in the repository.** The scientific authority
   cited for the load-bearing transfer-runtime equations is "the
   user-approved Phase 1E-F specification" and "the human-approved Phase 1E-G
   specification", both cited by section. Neither document is in the
   repository. The 1E-G carrier equations have no paper equation number (this
   is disclosed), so these specifications are their only source.
3. **Three cited audits are untracked.** The following are required by the
   1F-C-R validator and absent from the repository:
   - `astra/INDEPENDENT_SCIENTIFIC_AUDIT.md`, the audit that 1F-C-R
     remediates;
   - `reports/phase1f_b_dust_wall_boost_dynamics_v3_final_audit.md`;
   - `reports/phase1f_c_wall_common_geometry_adversarial_audit.md`, the audit
     that triggered the 1F-C v2 corrections.

**Consequence.** The scientific basis of Phase 1E-F onward cannot be audited
from the repository alone, contrary to CLAUDE.md's "Reports are the
authoritative record of scientific status".

**Suggested resolution:**
- commit the two specifications, or faithful excerpts of the load-bearing
  sections;
- commit the three audits;
- add a short decision record for the H1 implementation.

### F5 — CLAUDE.md's scope firewall contradicts the implemented Candidate A (LOW-MEDIUM)

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

**Locations:**
- `CLAUDE.md` line 72 ("fσ8 **or any "fσ8-shaped" diagnostic**"), against its
  own growth-layer row and phase ledger, which list Candidate A as
  implemented;
- `src/timescape_fsigma8/growth/anchored_diagnostic.py` line 479, where
  `Q_anchor=f·A_anchor`;
- `phase1d_a_growth_observable_audit.md` §16 item 4 ("an fσ8-*shaped*
  diagnostic").

**Statement.** Candidate A is exactly the fσ8-shaped diagnostic that 1D-A
conditionally authorised. CLAUDE.md both lists it as implemented and states
that no fσ8-shaped diagnostic is implemented. Candidate A's own labelling
(conditional, externally anchored, non-observational) is appropriate; only the
governing documentation is inconsistent.

**Suggested resolution:** state that no fσ8-shaped diagnostic exists beyond
the conditional, anchored Candidate A.

### F6 — Reproducibility is tied to a Windows checkout and to historical Git state (LOW-MEDIUM)

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE` (supporting:
`NUMERICALLY_CORROBORATED`).

**Locations:**
- `scripts/extract_upstream_barotropic_oracle.py` lines 35–36 and 115;
- `tests/test_vs_upstream_barotropic_oracle.py` lines 47, 76–77 and 88;
- `tests/test_anchored_density_growth.py` line 37;
- `scripts/validate_anchored_density_growth.py` lines 82 and 250–252;
- `scripts/validate_phase1f_c_r_astra_remediation.py` lines 22 and 94–101.

**Statement.**
1. **The notebook hash depends on line endings.** The pinned SHA-256
   `86d2534d…afe55a` is the hash of the working-tree file after Windows
   `core.autocrlf` conversion. The committed file content, which any LF
   checkout produces, hashes to `628c4412…5cea2a`. On Linux or macOS the barotropic
   oracle extraction exits with "FATAL: upstream commit or notebook hash
   differs", and the barotropic-oracle tests then auto-skip, so the Fig. 3
   reproduction goes silently unverified. `UPSTREAM.lock` pins only the
   commit.
2. **The Phase 1D-D validator is branch-bound.**
   `validate_anchored_density_growth.py` refuses to run unless the current
   branch is `phase-1d-d-anchored-density-growth`. Its artifact therefore
   cannot be regenerated from `main`, and the dependent test is always
   skipped elsewhere.
3. **The 1F-C-R validator is bound to a past state.**
   `validate_phase1f_c_r_astra_remediation.py` asserts
   `main == origin/main == 63d2104…`, which no longer holds (both are now
   `118b8f3…`). It also needs the three untracked files of F4, so it cannot
   pass on any current checkout.

**Suggested resolution:**
- pin the Git blob hash (`git hash-object`) or a hash of line-ending-normalised
  content;
- replace branch-name and `main`-equality gates with ancestry checks against
  recorded commits.

### F7 — Density functions default to `G = 1.0` (LOW)

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

**Locations:**
- `background/tracker.py` lines 156 and 170;
- `background/effective_fluid.py` lines 18, 29, 40 and 51;
- the policy statement in `background/__init__.py` line 55;
- the documented default in `background_validation.md` line 74.

**Statement.** The package docstring says G "is passed explicitly (AGENTS.md
rule 4: no hidden unit choices)", and CLAUDE.md forbids defaults for
scientific choices. These six functions nevertheless default to `G=1.0`. The
default is harmless for every current caller: all CGI coefficients use
`4πGρ`, in which G cancels, and callers pass G explicitly. It is simply
inconsistent with the stated policy.

### F8 — Governing documentation is stale (LOW)

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

**`CLAUDE.md`:**
- the phase ledger ends at "1F-A … (current branch)" (line 178);
- line 105 cites "539 tests at the Phase 1F-A checkpoint", while the suite now
  collects 654;
- the architecture table omits `phase1f_b/`, `phase1f_c/`,
  `scientific_status.py` and `components.py`;
- the key-command list omits the 1F-B and 1F-C-R drivers;
- line 143 says "Never push … All work stays local", while the repository
  history (tags and branches on `origin`) shows that approved pushes are part
  of the workflow. AGENTS.md rule 7 is the operative rule.

**`README.md`:** the layout table stops at Phase 1D-B, and the setup
instructions are Windows-only.

**`pyproject.toml`:** the description still covers only the background and
the clean systems.

### F9 — Notational slip in the 1C-A wavenumber finding F7 (LOW)

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

**Location:** `phase1c_perturbation_equation_audit.md` lines 300–301.

**Statement.** The factor is written "a_D,0 × h_TS/h_ΛCDM = 1.3685 ×
0.9204". But `0.9204=h_ΛCDM/h_TS`, and the correct factor is
`a_D0·h_ΛCDM/h_TS=1.25955`, as implemented in
`barotropic.resolve_wavenumber`. The slip is in the text only.

## 6. Finding summary

| ID | Title | Severity | Primary classification | Status |
|---|---|---|---|---|
| F1 | ICs are not the Timescape growing mode | MEDIUM-HIGH | `DERIVED_FROM_VERIFIED_DEFINITIONS` | OPEN |
| F2 | Chain-factor range 1.025–1.084 is wrong (max 8/7) | MEDIUM | `DERIVED_FROM_VERIFIED_DEFINITIONS` | OPEN |
| F3 | H1 conditional closure not demonstrated (`J_Ξ`, background identities) | MEDIUM | `DERIVED_FROM_VERIFIED_DEFINITIONS` | OPEN |
| F4 | Authorization, specification and audit provenance missing | MEDIUM | `VERIFIED_FROM_PRIMARY_SOURCE` | OPEN |
| F5 | Scope firewall contradicts Candidate A | LOW-MEDIUM | `VERIFIED_FROM_PRIMARY_SOURCE` | OPEN |
| F6 | Windows-only hash pin; state-bound validators | LOW-MEDIUM | `VERIFIED_FROM_PRIMARY_SOURCE` | OPEN |
| F7 | `G=1.0` defaults | LOW | `VERIFIED_FROM_PRIMARY_SOURCE` | OPEN |
| F8 | Stale governing documentation | LOW | `VERIFIED_FROM_PRIMARY_SOURCE` | OPEN |
| F9 | 1C-A F7 notational slip | LOW | `DERIVED_FROM_VERIFIED_DEFINITIONS` | OPEN |

Counts: `HIGH` 0 · `MEDIUM-HIGH` 1 · `MEDIUM` 3 · `LOW-MEDIUM` 2 · `LOW` 3.

## 7. Overall scientific assessment

**Established and independently confirmed:**
- the tracker background and its effective fluid;
- D1 (the paper's ⟨R⟩_D prefactor);
- D2 (the notebook's `dQ_D/dt`, which corrupts the published c²_s,eff and
  Fig. 3);
- D3 (`RESOLVED_DERIVED_4_10`, confirmed from first principles and by (4.29));
- the bit-exact provenance of the IC recipe;
- the epoch and wavenumber ambiguities;
- the D2×D3 sensitivity analysis of Fig. 3, including the gradient
  instability from the negative `c²_s`;
- the analytic growth-rate machinery with its crossing policy;
- Candidate A as a correctly labelled, externally anchored, non-observational
  diagnostic;
- the 1D-C and 1E-A–1E-D no-go results: there is no dressed Fourier map, no
  dressed Kaiser law, and new dynamics are required.

**Qualified by this review:**
- the amplitude and IC-convention results (F1);
- the bare/dressed spread (F2);
- the "conditionally closed" status of the H1 runtime (F3).

**Not established, as the project itself states:**
- any physical Timescape trajectory beyond the clean and barotropic CGI
  systems;
- a regional or common background embedding;
- all-time transfer compatibility;
- any observational quantity.

Phases 1E-F to 1F-C are consistency checkers for externally supplied closures,
validated on manufactured data. F3 shows that even their instantaneous
consistency has not yet been exhibited. The project's planned next phase,
`1F-D_BACKGROUND_EMBEDDING_AND_CONSTRAINT_CLOSURE_FEASIBILITY`, is the right
next step; this review recommends it take priority over further runtime
infrastructure.

## 8. Recommendations

These are non-binding and prioritised. None was applied, and each requires
the project's usual approval.

1. **F1.** Add a growing-mode IC convention, quantify the decaying-mode
   fraction of each existing convention, and restate the 1C/1D convention
   studies relative to it.
2. **F3.** Add `J_Ξ=0` and background-identity gates, then exhibit a
   consistent manufactured state or downgrade the status tokens.
3. **F4.** Commit the Phase 1E-F and 1E-G specifications and the three
   untracked audits, and add an H1 decision record.
4. **F2 and F9.** Issue a successor erratum covering both.
5. **F6.** Use a portable notebook hash and ancestry-based validator gates.
6. **F5, F7 and F8.** Update the documentation.

## 9. Preservation statement

- No tracked file was modified. The only new files are this report and its
  JSON companion.
- Nothing was staged, committed, tagged or pushed, and the authors were not
  contacted.
- Git-ignored local state was created for the review:
  - `.reference/` holds the upstream clone at `590c6fd…`, checked out with
    `core.autocrlf=true` so that the pinned hash is reproduced;
  - `.venv/` (Python 3.13) and `.venv311/` (Python 3.11);
  - `artifacts/`, which holds the regenerated oracles, validation JSON and
    figures.
- The independent calculations in Appendix A were run from a temporary
  scratch directory outside the repository.

## 10. Final machine verdict

```text
AUDIT: INDEPENDENT_READ_ONLY_POST_REMEDIATION_REVIEW
SCOPE: PHASES_1A_TO_1F_C_R_COMPLETE_PROJECT
CHECKPOINT: 118b8f3af3c1360b0da74df8e9a9cb3ba1fed83a
TEST_SUITE_PY313: 653_PASSED_1_SKIPPED
TEST_SUITE_PY311: 653_PASSED_1_SKIPPED
IMPLEMENTED_EQUATION_ERRORS_PHASES_1B_1D: 0
D1_TYPO_CLASSIFICATION: CONFIRMED_CONSISTENT
D2_UPSTREAM_DEFECT: CONFIRMED
D3_VERDICT_RESOLVED_DERIVED_4_10: INDEPENDENTLY_CONFIRMED
PUBLISHED_AND_REPORTED_NUMBERS_RECOMPUTED: REPRODUCED
F1_IC_DECAYING_MODE_CONTAMINATION: OPEN
F2_CHAIN_FACTOR_RANGE_ERROR: OPEN
F3_H1_CLOSURE_NOT_DEMONSTRATED: OPEN
F4_PROVENANCE_GAPS: OPEN
F5_SCOPE_FIREWALL_CONTRADICTION: OPEN
F6_REPRODUCIBILITY_PORTABILITY: OPEN
F7_G_DEFAULTS: OPEN
F8_STALE_DOCUMENTATION: OPEN
F9_NOTATIONAL_SLIP: OPEN
CODE_OR_EQUATIONS_CHANGED: NO
UNIQUE_TIMESCAPE_PREDICTION: NOT_GRANTED
OBSERVATIONAL_AUTHORIZATION: NOT_GRANTED
FSIGMA8_AUTHORIZATION: NOT_GRANTED
```

## Appendix A — Reproduction code

The blocks below were executed exactly as shown with Python 3.13.12, NumPy
2.5.3 and SciPy 1.18.1. Run A.0 first, then A.1 or A.2 in the same session.
Run A.3 from the repository root. Only A.3 imports project code.

### A.0 — Independent tracker background and CGI systems

```python
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy import special

fv0, h_ts, h_lcdm, Om = 0.737, 0.7323, 0.674, 0.315
HD0 = 2*(2+fv0)/(4*fv0**2+fv0+4)          # bare H_D0 in units of the dressed H0
t0, aD0 = (2+fv0)/(3*HD0), 1+fv0/2
c1, c2 = 3*fv0*HD0, (2+fv0)*(1-fv0)
f     = lambda t: c1*t/(c1*t+c2)                   # void fraction f_v(t)
aD    = lambda t: aD0*(3*HD0*t)**(2/3)*(c1*t+c2)**(1/3)/(2+fv0)
Th    = lambda t: (2+f(t))/t                       # Theta = 3 H_D
g_d   = lambda t: (2/3)*(1-f(t))/t**2              # 4 pi G rho_d
g_e   = lambda t: f(t)*(8+f(t))/(6*t**2)           # 4 pi G rho_eff
w     = lambda t: -(4-f(t))/(8+f(t))               # w_eff
cs2   = lambda t: (f(t)**2-2*f(t)-2)/(2+f(t))**2   # corrected c^2_s,eff
z     = lambda t: (2+f(t))*f(t)**(1/3)/(3*fv0**(1/3)*HD0*t) - 1   # dressed z
chain = lambda fv: (2+fv)**2/(4+fv+4*fv**2)        # f_dressed / f_bare
gyr = h_ts/9.778                                   # notebook Gyr -> code time
ti = 0.218*gyr

def D_lcdm(zz):                                    # flat LCDM, D/a -> 1
    a = 1/(1+zz); x = (1-Om)*a**3/(Om+(1-Om)*a**3)
    return ((5/6)*(Om/(1-Om))**(1/3)*np.sqrt(1+Om/((1-Om)*a**3))
            * special.beta(5/6, 2/3)*special.betainc(5/6, 2/3, x))
eps = 1e-5
d0 = 0.066*D_lcdm(20)
Z0 = -0.066*(D_lcdm(20+eps)-D_lcdm(20))/eps*(-21*np.sqrt(1-Om+Om*21**3))

def com(t, y):      # comoving closure, state (Delta_d, Z, Delta_eff)
    return [-y[1], -g_d(t)*y[0]-(2/3)*Th(t)*y[1]-g_e(t)*y[2],
            -(1+w(t))*y[1]+w(t)*Th(t)*y[2]]
def mes(t, y):      # Meszaros, state (Delta_d, dDelta_d/dt)
    return [y[1], g_d(t)*y[0]-(2/3)*Th(t)*y[1]]
def baro(k, branch):  # barotropic closure, unrescaled tilt V
    def rhs(t, y):
        th, ww, cc, a = Th(t), w(t), cs2(t), aD(t)
        a33 = (ww-cc)*th if branch == 'derived_4_10' else (ww+cc)*th
        return [-y[1], -g_d(t)*y[0]-(2/3)*th*y[1]-g_e(t)*(1+3*cc)*y[2],
                -(1+ww)*y[1]+a33*y[2]+(k**2/a)*(1+ww)*y[3],
                -cc/(a*(1+ww))*y[2]+(th/3)*(3*cc-1)*y[3]]
    return solve_ivp(rhs, (ti, t0), [d0, Z0, 0, 0], dense_output=True,
                     method='DOP853', rtol=1e-13, atol=1e-16)
```

### A.1 — Reproduction of published and reported numbers (Sec. 4, F2, F9)

```python
opt = dict(method='DOP853', rtol=1e-12, atol=1e-15)
t20 = brentq(lambda t: z(t)-20, 1e-6, t0, xtol=1e-16)
print(f"z(0.218 Gyr) = {z(ti):.6f}; t(z=20) = {t20/gyr:.8f} Gyr")
print(f"c_s^2(t0) = {cs2(t0):.6f}; w_eff(t0) = {w(t0):.6f}")
print(f"IC: Delta_d = {d0:.17g}, Z = {Z0:.17g}")
c = solve_ivp(com, (ti, t0), [d0, Z0, 0.0], **opt).y[:, -1]
m = solve_ivp(mes, (ti, t0), [d0, -Z0], **opt).y[:, -1]
print(f"comoving: Delta_d(t0) = {c[0]:.10f}, Delta_eff(t0) = {c[2]:.10f}, "
      f"f_bare(t0) = {-3*c[1]/(Th(t0)*c[0]):.7f}")
print(f"Meszaros: Delta_d(t0) = {m[0]:.10f}")
for k in (2*np.pi, 5*np.pi, 10*np.pi):
    for br in ('printed_4_15', 'derived_4_10'):
        y = baro(k, br).y[:, -1]
        print(f"k={k/np.pi:.0f}pi {br}: Delta_d(t0) = {y[0]: .6e}, "
              f"Delta_eff(t0) = {y[2]: .6e}")
s = baro(2*np.pi, 'derived_4_10')
tt = np.linspace(ti, t0, 20001); yy = s.sol(tt)[0]
i = np.where(yy[:-1]*yy[1:] < 0)[0][0]
print(f"derived_4_10, k=2pi: Delta_d root at t = "
      f"{brentq(lambda t: s.sol(t)[0], tt[i], tt[i+1], xtol=1e-15):.10f}")
t10 = brentq(lambda u: z(u)-10, ti, t0, xtol=1e-16)
for br in ('printed_4_15', 'derived_4_10'):
    sb = baro(2*np.pi, br); y1 = sb.sol(t0)
    print(f"k=2pi {br}: G(t0; z_ref=10) = {y1[0]/sb.sol(t10)[0]:.4f}, "
          f"f_bare(t0) = {-3*y1[1]/(Th(t0)*y1[0]):.5f}")
for zz in (20, 10, 3, 2, 1, 0.5, 0.3):
    t = brentq(lambda u: z(u)-zz, 1e-8, t0, xtol=1e-16)
    print(f"z = {zz}: f_dressed/f_bare = {chain(f(t)):.10f}")
tpk = brentq(lambda t: f(t)-0.4, 1e-8, t0, xtol=1e-16)
print(f"z = 0: f_dressed/f_bare = {chain(f(t0)):.10f}; maximum = {chain(0.4):.10f} "
      f"(= 8/7) at f_v = 0.4, z = {z(tpk):.4f}")
print(f"paper_lcdm_hubble_k factor = {aD0*h_lcdm/h_ts:.16f}")
```

Output:

```text
z(0.218 Gyr) = 18.586475; t(z=20) = 0.19620643 Gyr
c_s^2(t0) = -0.391238; w_eff(t0) = -0.373469
IC: Delta_d = 0.0031427229788258113, Z = -0.16974050044476324
comoving: Delta_d(t0) = 0.0386165401, Delta_eff(t0) = 0.0070813934, f_bare(t0) = 0.4251006
Meszaros: Delta_d(t0) = 0.0331504916
k=2pi printed_4_15: Delta_d(t0) =  2.883229e-02, Delta_eff(t0) =  5.039166e-02
k=2pi derived_4_10: Delta_d(t0) = -3.752402e-02, Delta_eff(t0) =  2.424232e+00
k=5pi printed_4_15: Delta_d(t0) = -1.595991e+02, Delta_eff(t0) =  3.313648e+04
k=5pi derived_4_10: Delta_d(t0) = -1.101842e+04, Delta_eff(t0) =  3.199264e+06
k=10pi printed_4_15: Delta_d(t0) = -3.139420e+12, Delta_eff(t0) =  3.531343e+15
k=10pi derived_4_10: Delta_d(t0) = -2.721593e+14, Delta_eff(t0) =  3.545589e+17
derived_4_10, k=2pi: Delta_d root at t = 0.7851615735
k=2pi printed_4_15: G(t0; z_ref=10) = 4.7326, f_bare(t0) = 0.14661
k=2pi derived_4_10: G(t0; z_ref=10) = -6.1617, f_bare(t0) = 4.34190
z = 20: f_dressed/f_bare = 1.0247547361
z = 10: f_dressed/f_bare = 1.0578767186
z = 3: f_dressed/f_bare = 1.1360532044
z = 2: f_dressed/f_bare = 1.1428567452
z = 1: f_dressed/f_bare = 1.1306676738
z = 0.5: f_dressed/f_bare = 1.1124305013
z = 0.3: f_dressed/f_bare = 1.1023531127
z = 0: f_dressed/f_bare = 1.0841563338; maximum = 1.1428571429 (= 8/7) at f_v = 0.4, z = 2.0066
paper_lcdm_hubble_k factor = 1.2595507305749012
```

### A.2 — Growing-mode analysis of the initial conditions (F1)

```python
tE = 1e-8                                  # deep EdS regime, f_v ~ 2e-8
opt = dict(method='DOP853', rtol=1e-12, atol=1e-30, dense_output=True)
# Regular (growing-mode) solutions from the EdS limit: Delta_d ~ t^(2/3),
# Z = -dDelta_d/dt and the comoving attractor Delta_eff = Delta_d/5.
gc = solve_ivp(com, (tE, t0), [tE**(2/3), -(2/3)*tE**(-1/3), 0.2*tE**(2/3)], **opt)
gm = solve_ivp(mes, (tE, t0), [tE**(2/3), (2/3)*tE**(-1/3)], **opt)
epochs = {"0.218 Gyr": ti,
          "dressed z=20": brentq(lambda t: z(t)-20, 1e-6, t0, xtol=1e-16)}
for name, t in epochs.items():
    y, ym = gc.sol(t), gm.sol(t)
    print(f"[{name}] growing mode: comoving -Z/Delta_d = {-y[1]/y[0]:.4f}, "
          f"Delta_eff/Delta_d = {y[2]/y[0]:.5f}; Meszaros dlnD/dt = {ym[1]/ym[0]:.4f}")
print(f"IC -Z/Delta_d: unconverted {-Z0/d0:.4f}, converted {-Z0/d0*0.674/0.7323:.4f}")
for rate, Zi in (("unconverted", Z0), ("converted", Z0*0.674/0.7323)):
    for ep, t_i in epochs.items():
        pc = solve_ivp(com, (t_i, t0), [d0, Zi, 0.0], **opt)
        pm = solve_ivp(mes, (t_i, t0), [d0, -Zi], **opt)
        tr = brentq(lambda t: z(t)-10, t_i, t0, xtol=1e-16)
        amp_c = pc.sol(t0)[0]/(gc.sol(t0)[0]*d0/gc.sol(t_i)[0])
        amp_m = pm.sol(t0)[0]/(gm.sol(t0)[0]*d0/gm.sol(t_i)[0])
        G_c = (pc.sol(t0)[0]/pc.sol(tr)[0])/(gc.sol(t0)[0]/gc.sol(tr)[0]) - 1
        G_m = (pm.sol(t0)[0]/pm.sol(tr)[0])/(gm.sol(t0)[0]/gm.sol(tr)[0]) - 1
        fb = []
        for zz in (0, 1, 2, 5):
            t = t0 if zz == 0 else brentq(lambda u: z(u)-zz, t_i, t0, xtol=1e-16)
            fc = (pc.sol(t)[1]/pc.sol(t)[0])/(gc.sol(t)[1]/gc.sol(t)[0]) - 1
            fm = (pm.sol(t)[1]/pm.sol(t)[0])/(gm.sol(t)[1]/gm.sol(t)[0]) - 1
            fb.append(f"z={zz}: {fc:+.3%}/{fm:+.3%}")
        if rate == "unconverted" and ep == "0.218 Gyr":
            print(f"Candidate A baseline G(t0; z_ref=10): notebook IC {pc.sol(t0)[0]/pc.sol(tr)[0]:.6f}, "
                  f"growing mode {gc.sol(t0)[0]/gc.sol(tr)[0]:.6f}; growing-mode f_bare(t0) = "
                  f"{-3*gc.sol(t0)[1]/(Th(t0)*gc.sol(t0)[0]):.5f}")
        print(f"[{rate}|{ep}] Delta_d(t0) ratio com/mes = {amp_c:.4f}/{amp_m:.4f}; "
              f"G(t0;z_ref=10) bias = {G_c:+.3%}/{G_m:+.3%}; f bias: " + ", ".join(fb))
t_i = epochs["0.218 Gyr"]; y = gc.sol(t_i); rate0, ratio0 = -y[1]/y[0], y[2]/y[0]
ref = solve_ivp(com, (t_i, t0), [d0, -rate0*d0, ratio0*d0], **opt).y[0, -1]
for name, (Zi, De) in {"notebook Z_i, Delta_eff = 0": (Z0, 0.0),
                       "growing-mode Z_i, Delta_eff = 0": (-rate0*d0, 0.0),
                       "notebook Z_i, attractor Delta_eff": (Z0, ratio0*d0)}.items():
    yy = solve_ivp(com, (t_i, t0), [d0, Zi, De], **opt).y[0, -1]
    print(f"{name}: Delta_d(t0)/growing = {yy/ref:.4f}")
```

Output:

```text
[0.218 Gyr] growing mode: comoving -Z/Delta_d = 40.0878, Delta_eff/Delta_d = 0.20005; Meszaros dlnD/dt = 39.8503
[dressed z=20] growing mode: comoving -Z/Delta_d = 44.6209, Delta_eff/Delta_d = 0.20005; Meszaros dlnD/dt = 44.3828
IC -Z/Delta_d: unconverted 54.0106, converted 49.7107
Candidate A baseline G(t0; z_ref=10): notebook IC 6.322867, growing mode 6.164012; growing-mode f_bare(t0) = 0.42491
[unconverted|0.218 Gyr] Delta_d(t0) ratio com/mes = 1.1312/1.1398; G(t0;z_ref=10) bias = +2.577%/+2.991%; f bias: z=0: +0.045%/+0.085%, z=1: +0.118%/+0.210%, z=2: +0.268%/+0.421%, z=5: +1.450%/+1.813%
[unconverted|dressed z=20] Delta_d(t0) ratio com/mes = 1.0771/1.0855; G(t0;z_ref=10) bias = +1.174%/+1.591%; f bias: z=0: -0.016%/+0.046%, z=1: +0.005%/+0.113%, z=2: +0.068%/+0.227%, z=5: +0.647%/+0.975%
[converted|0.218 Gyr] Delta_d(t0) ratio com/mes = 1.0882/1.0974; G(t0;z_ref=10) bias = +1.664%/+2.145%; f bias: z=0: -0.007%/+0.062%, z=1: +0.029%/+0.152%, z=2: +0.120%/+0.304%, z=5: +0.923%/+1.309%
[converted|dressed z=20] Delta_d(t0) ratio com/mes = 1.0384/1.0473; G(t0;z_ref=10) bias = +0.429%/+0.907%; f bias: z=0: -0.060%/+0.026%, z=1: -0.070%/+0.065%, z=2: -0.057%/+0.130%, z=5: +0.208%/+0.558%
notebook Z_i, Delta_eff = 0: Delta_d(t0)/growing = 1.1312
growing-mode Z_i, Delta_eff = 0: Delta_d(t0)/growing = 0.9920
notebook Z_i, attractor Delta_eff: Delta_d(t0)/growing = 1.1392
```

For the Mészáros system the printed rate is `d ln Δ_d/dt`, the analogue of
`−Z/Δ_d` since `Z=−Δ̇_d`.

### A.3 — Consistency of the 1E-G manufactured state (F3)

```python
# Run from the repository root.
import sys
import numpy as np
sys.path.insert(0, "tests")
import test_phase1e_g_continuum_h1 as T

res, bg = T._continuum_dynamic_fixture()
d = res.downstream_phase1e_f
fv, fw, G = bg.f_v.value, 1 - bg.f_v.value, bg.G
print("closure gates passed:  max|R_Z| = %.1e, max|R_eff| = %.1e, max|C_P| = %.1e"
      % (np.max(np.abs(d.R_Z)), np.max(np.abs(d.R_eff)), np.max(np.abs(d.C_P))))
print("J_f (fixed partition) = %.1f;  E_DeltaXi_0 in [%.3f, %.3f]"
      % (np.max(np.abs(res.J_f_Gamma.value)), res.E_DeltaXi_0_Gamma.value.min(),
         res.E_DeltaXi_0_Gamma.value.max()))
print("clock mismatch J_Xi in [%.4f, %.4f]  (must vanish on the homogeneous-clock branch)"
      % (d.J_Xi.min(), d.J_Xi.max()))
# zeroth-order identities of two exact dust-FLRW regions (alpha_r = 1 in this fixture)
for r, rho, H, Rbar, Th, a in (("w", bg.rho_w, bg.H_w, bg.R_bar_w, bg.Theta_w, bg.alpha_w),
                               ("v", bg.rho_v, bg.H_v, bg.R_bar_v, bg.Theta_v, bg.alpha_v)):
    print(f"region {r}: Friedmann R_bar - (16 pi G rho - 6 H^2) = "
          f"{Rbar.value - (16*np.pi*G*rho.value - 6*H.value**2):+.4f}; "
          f"dust conservation rho_dot + alpha Theta rho = "
          f"{rho.first + a.value*Th.value*rho.value:+.4f}")
dTh = bg.Theta_v.value - bg.Theta_w.value
print("partition kinematics f_v_dot - f_v f_w (Xi_v - Xi_w) = %+.4f"
      % (bg.f_v.first - fv*fw*(bg.Xi_v.value - bg.Xi_w.value)))
print("Q_bar = %.4f vs two-FLRW-region value (2/3) f_v f_w d_Theta^2 = %.4f (never negative)"
      % (bg.Q_bar.value, (2/3)*fv*fw*dTh**2))
print("W_bar = %.4f vs f_w R_w + f_v R_v = %.4f (needs 6 K_D/a_D^2 = %.4f; GM Timescape has K_D = 0)"
      % (bg.W_bar.value, fw*bg.R_bar_w.value + fv*bg.R_bar_v.value,
         fw*bg.R_bar_w.value + fv*bg.R_bar_v.value - bg.W_bar.value))
print("Theta = %.4f vs f_w Theta_w + f_v Theta_v = %.4f"
      % (bg.Theta.value, fw*bg.Theta_w.value + fv*bg.Theta_v.value))
```

Output:

```text
closure gates passed:  max|R_Z| = 4.8e-15, max|R_eff| = 1.5e-15, max|C_P| = 1.1e-16
J_f (fixed partition) = 0.0;  E_DeltaXi_0 in [-1.000, 0.200]
clock mismatch J_Xi in [-26.6466, 5.3293]  (must vanish on the homogeneous-clock branch)
region w: Friedmann R_bar - (16 pi G rho - 6 H^2) = -3.7600; dust conservation rho_dot + alpha Theta rho = +0.6000
region v: Friedmann R_bar - (16 pi G rho - 6 H^2) = -3.1476; dust conservation rho_dot + alpha Theta rho = +1.2000
partition kinematics f_v_dot - f_v f_w (Xi_v - Xi_w) = -0.1440
Q_bar = -5.0000 vs two-FLRW-region value (2/3) f_v f_w d_Theta^2 = 0.0576 (never negative)
W_bar = -3.0000 vs f_w R_w + f_v R_v = -0.0430 (needs 6 K_D/a_D^2 = 2.9570; GM Timescape has K_D = 0)
Theta = 0.8400 vs f_w Theta_w + f_v Theta_v = 0.8400
```

In this fixture `α_w=α_v=1`, so `Ξ_r=Θ_r` and the volume-averaged-expansion
check `Θ=f_wΞ_w+f_vΞ_v` reduces to the last line printed.
