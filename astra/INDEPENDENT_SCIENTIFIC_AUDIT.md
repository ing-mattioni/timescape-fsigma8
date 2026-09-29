# Independent scientific audit — timescape-fsigma8

Audit date: 2026-09-05. Authoritative checkpoint: `63d2104575c6a249e5177e47f4a354b660e70e32`.

This is a read-only review, not approval to change equations or develop an observational model. All audit files are outside the repository. Source equations, repository equations, and their physical interpretation are assessed separately.

## 1. EXECUTIVE VERDICT

**GLOBAL_PROJECT_VERDICT: ACCEPT_WITH_TARGETED_CORRECTIONS**

The project is defensible as a verified tracker background followed by explicitly conditional perturbation and geometric constructions. It is **not yet a demonstrated, dynamically consistent end-to-end Timescape perturbation model**, and it does not predict observational growth or fσ8.

I found no uncorrected S4/S5 error that establishes invalidation of the accepted tracker, clean perturbation algebra, D3 adjudication, or first-order boost/ADM identities. I did find six concrete implementation, test, or citation corrections, plus one scientific-classification/embedding correction. Acceptance is limited to the stated conditional meaning; it is not certification of every historical source-completeness claim.

The important results are:

- The tracker background is correct on its stated dust, zero-Λ, late-time tracker branch. D1 and D2 were correctly corrected; agreement with the upstream notebook is not the reason to accept those corrections.
- D3 independently resolves to `RESOLVED_DERIVED_4_10`. The printed `w+c_s²` coefficient is incompatible with the stated dust-frame conservation equation and barotropic closure. Keeping it as an explicit reproduction branch is legitimate; treating it as the derived branch is not.
- The boost sign, the scalar proper/common-time conversion, the negative ADM extrinsic-curvature convention, and the metric-trace evolution equation are correct under the selected assumptions.
- Phase 1F-C's numerical acceleration has an insufficiently specified component representation: its `1/a_W` scaling describes physical orthonormal components, not a coordinate covector `A_i`.
- The continuum API accepts inconsistent metric/volume-measure data. A nonconstant, mean-preserving counterexample produces a weighted diffusion operator instead of the advertised metric's Laplace–Beltrami operator.
- Optional metric reconstruction accepts perturbations so large that `1+2 C_W` becomes negative. The small-perturbation validity check is incomplete.
- Exact citations to BDE (14)–(16) for acceleration/expansion transformations are wrong. The printed Short–Coles (11)–(12) are also not the formula implemented for initial conditions. These are source-support defects, not evidence that the independently derived numerical formulas should be reversed or replaced by the misprints.
- Intrinsic ranks 4, 5, and optionally 6 are defensible as **field-species differential counts**. They are not counts of independent admissible initial functions after all constraints and external histories have been imposed.
- `nu_W` and the H1-to-wall realization remain external. But a prior compatibility problem also remains: the imported regional proper-time dust-FLRW backgrounds have not been shown to embed consistently into the frozen Timescape background and the common wall spacetime.

In particular, W07 explicitly distinguishes Einstein–de Sitter evolution of the regional wall scale in volume-average time from evolution in local wall proper time. The naive identification of the imported regional proper clock with the W09 wall clock fails an elementary flat-dust background equation. This rules out that identification, not Timescape itself and not every possible conditional H1 realization. [W07, Eq. (11) and accompanying discussion](https://arxiv.org/pdf/0709.0732v2).

The current Phase 1F-C endpoint is a reasonable place to retain as a conditional kinematic checkpoint. The next scientific phase should establish background/frame embedding and all-time constraint compatibility before attempting to choose a perturbative lapse or infer observables.

## 2. AUDIT SCOPE AND EVIDENCE

### Repository and execution

| Item | Independent observation |
|---|---|
| Repository | `C:\Projects\timescape-fsigma8`; `ing-mattioni/timescape-fsigma8` |
| HEAD, main, local origin/main | All `63d2104575c6a249e5177e47f4a354b660e70e32` |
| Remote main | Read-only `git ls-remote` returned the same commit |
| Phase 1F-C ancestry | Exactly `d2f1502 → 6a63390 → 63d2104`; each child has one parent |
| Tags | All 27 phase tags listed in §3 were inspected, including annotated-tag peeled targets |
| Python 3.14.3 | Full suite rerun: **617 passed**, 105.15 s; NumPy 2.5.2, SciPy 1.18.1, pytest 9.1.1 |
| Python 3.11.9 | Full suite rerun: **617 passed**, 99.81 s; NumPy 2.4.6, SciPy 1.17.1, pytest 9.1.1 |
| Test outcomes | No failed, skipped, xfailed tests or warning summaries in either full run |
| Read-only precautions | `PYTHONDONTWRITEBYTECODE=1`, Python `-B`, pytest `-p no:cacheprovider`; no environment installation |
| Independent probes | Metric/measure, metric positivity, vector component scaling, elliptic rank, tracker constraint, regional clock compatibility, initial-condition quadrature |
| Mutations | Four process-memory mutations; original source files never changed; all four killed by existing focused tests |

The historical Phase 1F-C report records different 3.14 NumPy/SciPy patch versions. The rerun corroborates the claimed Python/test baseline, not byte-identical dependency environments. Tests that read ignored oracle artifacts were able to run; their existence is not itself independent scientific evidence. I did not rerun the entire original notebook in a fresh kernel.

The worktree contained two **pre-existing untracked** reports: `reports/phase1f_b_dust_wall_boost_dynamics_v3_final_audit.md` and `reports/phase1f_c_wall_common_geometry_adversarial_audit.md`. They were not treated as committed checkpoint evidence. `git status` also reports an access warning for the pre-existing `.pytest_cache` directory. No tracked diff was introduced.

### Pinned upstream

`UPSTREAM.lock`, the actual local reference checkout, and the notebook bytes agree:

```text
repository: https://github.com/MarcoGaloppo/Linear-Perturbations-in-averaged-cosmological-models
commit: 590c6fd5332acb15f5683ebf392a0d7ce54983c5
notebook: ACPT_Timescape.ipynb
sha256: 86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a
```

The notebook was inspected directly, including background differentiation, barotropic/comoving matrices, ICs and start time. No later upstream revision was substituted. Its role is a pinned reproduction oracle, not authority overriding primary equations. No upstream license was found; its source remains reference-only.

### Evidence limits

The primary-source audit in §8 distinguishes actual equation inspection from partial inspection and unavailable material. Several comparator papers in old reports were not independently re-read equation-by-equation here. Accordingly, old claims of exhaustive literature search or complete rejection of every alternative framework are **not recertified**. No inference in this report substitutes “I did not find a derivation” for a theorem that no derivation can exist.

The PDF skill was used to render and visually inspect sign- and notation-critical pages. This materially exposed the BDE and Short–Coles attribution problems. Scratch scripts and retained PDFs are alongside this report.

## 3. REPOSITORY / PROVENANCE AUDIT

The actual history is linear. Short hashes below identify commits, not annotated tag objects. Each tag beginning `phase-` is shown by its suffix to keep the table readable; prepend `phase-` to recover its exact name.

| Checkpoint/tag suffix | Peeled commit | Actual role |
|---|---|---|
| Initial Phase 1A, no listed phase tag | `d33f4a0` | Upstream reproduction |
| Initial 1B development | `56f22ba` | Independent background |
| `1b-background-v1` | `fe8b00f` | Completed background and dressed quantities |
| `1c-a-equation-audit-v1` | `5d9aa47` | Equation inventory and defects |
| `1c-b1-clean-systems-v1` | `18b6666` | Clean systems and IC choices |
| `1c-b2-barotropic-v1` | `9ec3bcc` | Explicit barotropic branches |
| Documentation adjustment | `c6ea04f` | Docs/artifact-skip convention |
| `1d-a-growth-observable-audit-v1` | `878a97e` | Meaning of growth variables |
| `1d-b-growth-pipeline-v1` | `93d956d` | Growth diagnostics |
| `1d-c-observable-closure-audit-v1` | `81148eb` | Observable prerequisites |
| `1d-d-t-d3-frame-mapping-v1` | `f960a90` | D3 adjudication, before 1D-D |
| `1d-d-anchored-density-growth-v1` | `7ea266c` | Candidate A |
| `1e-a-dressed-observable-bridge-audit-v1` | `f4044cb` | Observable bridge audit |
| `1e-b-dressed-lightcone-velocity-derivation-v1` | `8634f14` | Generic lightcone/frame identities |
| `1e-c-perturbed-dressed-geometry-transfer-closure-v1` | `fcbf9c2` | Geometry/transfer alternatives |
| `1e-d-regional-matching-dynamics-v1` | `2fd3ed2` | Imported regional dynamics; three mismatch components |
| `1e-e-transfer-realization-selection-v1` | `1f2800c` | Conditional realization selection |
| `1e-f-h1-transfer-realization-v1` | `0ad10f4` | Matrix H1 runtime |
| `1e-f-h1-transfer-realization-v2` | `1e0a177` | Stronger dynamic/evidence tests |
| `1e-g-continuum-h1-realization-v1` | `75d4f30` | Continuum-backed H1 |
| `1e-g-continuum-h1-realization-v2` | `8fa4ab8` | Metric normalization and nontrivial residual tests |
| `1e-g-continuum-h1-realization-v3` | `94c5f83` | Physical three-volume dimensional firewall |
| `1e-g-continuum-h1-realization-v4` | `d262099` | Post-assembly integrity |
| `1f-a-h1-broken-density-spectral-boost-v1` | `a56fa88` | Broken density, spectra, conditional boost |
| `1f-a-h1-broken-density-spectral-boost-v2` | `87af797` | Evidence-classification correction |
| `1f-b-dust-wall-boost-dynamics-v1` | `27fd65f` | Scalar boost evolution |
| `1f-b-dust-wall-boost-dynamics-v2` | `16440e1` | Boundary enforcement and evidence corrections |
| `1f-b-dust-wall-boost-dynamics-v3` | `d2f1502` | Proper/common-time correction |
| `1f-c-wall-common-spacetime-geometry-v1` | `6a63390` | Conditional normal-wall kinematics |
| `1f-c-wall-common-spacetime-geometry-v2` | `63d2104` | Reference-operator contract and regressions |

The user-supplied phase order agrees with Git, including 1D-D-t preceding 1D-D. The two-commit fast-forward topology is verified. Git object ancestry cannot by itself prove that no equivalent history was ever rewritten elsewhere; there is no contradictory evidence in the inspected history. No remote mutation was performed.

## 4. GLOBAL ONTOLOGY

### Evidence legend

The short labels in the ledger and tables map to **exactly one** requested classification each; they are not additional categories:

| Label | Classification |
|---|---|
| FTS | `DERIVED_FROM_FROZEN_TIMESCAPE` |
| GR | `DERIVED_FROM_GENERIC_GR` |
| COND | `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` |
| EXT | `EXTERNAL_CLOSURE_INPUT` |
| GAUGE | `GAUGE_CHOICE` |
| SECTOR | `MODEL_SECTOR_RESTRICTION` |
| ND | `NOT_DERIVED` |
| REJECT | `REJECTED_UNSUPPORTED` |

### Clocks, rates, lapses

| Symbol / API | Meaning and order | Relation and classification |
|---|---|---|
| `t` in background/GM solver | Homogeneous volume-average time; not automatically local proper time everywhere | Frozen independent variable; FTS |
| `tau_w` | W09 wall proper time, background | `d tau_w/dt=1/gamma_w`; FTS |
| `tau_v` in regional discussions | Regional void proper time | Not implemented as a unique tracker-to-H1 clock history; EXT for selected realization |
| `tau_d,r`, H1 `alpha_r` | Proper time of imported regional dust system; `alpha_r=d tau_d,r/dt_common` | Homogeneous regional mappings supplied; EXT |
| `tau_W` | Proper time along selected physical/local wall normal | Background equals `tau_w` only in selected 1F-C map; COND |
| `gamma_w` | Background Timescape clock ratio `dt/dtau_w=(2+f)/2` | Homogeneous; FTS |
| `alpha_W` | Background wall proper-time rate relative to common time | 1F-B EXT; 1F-C reciprocal of `gamma_w` after explicit clock identification: COND |
| `nu_W(t,x)` | First-order spatial lapse perturbation in selected wall-normal description | EXT; not a perturbation supplied by tracker `gamma_w` |
| `N_W(t,x)` | ADM lapse, `alpha_W(1+nu_W)` to first order | COND; includes background and perturbation |
| `gamma_dW` | Lorentz factor `-u_d,w·u_W` | `1+O(v²)`; GR; no first-order boost information |
| `H_D`, `Theta` in 1B–1D | `d ln a_D/dt`, `3 H_D` | FTS background; perturbation coefficients use the same `t` |
| `H_dressed` | `d ln(a_D/gamma_w)/d tau_w` | `gamma_w H_D-dgamma_w/dt`; FTS |
| W09 regional `H_w`, `H_v` | `d ln a_r/dt`, using volume-average time | FTS; do not equate to H1 proper-time `H_r` |
| H1 `H_r`, `Theta_r` | Imported proper-time regional FLRW Hubble/expansion; `Theta_r=3H_r` | COND after exact regional FLRW restriction and supplied backgrounds |
| H1 `Xi_r` | Homogeneous common-time volume expansion `alpha_r Theta_r` on selected branch | COND |
| 1F-B/C `wall_hubble_rate=H_W^(t)` | `d ln a_W/dt_common`, already a common-time rate | EXT history with consistency checks; **not** multiplied by a second `alpha_W` |
| Coordinate time units | `H0^-1`, Gyr, or declared common-time unit | Unit conversion is not observer/clock conversion; COND |

### Congruences

| Object | Domain and meaning | Permitted identification |
|---|---|---|
| `u_D` / global GM dust frame | Averaged-background effective perturbation system | Not automatically a regional or dressed observer |
| `u_d,w` | Regional wall **dust** | Distinct from physical wall observer at first order |
| `u_d,v` | Regional void dust | Needs independent regional clock/embedding |
| `u_W` | Selected physical/local wall observer | Set equal to hypersurface normal `n` by SECTOR |
| `n` | Unit normal of chosen ADM slicing | `n_a=-N dt_a`; geometric object, not dust by definition |
| Effective-fluid frame | Auxiliary effective component with possible tilt | Not galaxy matter or wall observer |
| Tracer `u_g`, source `u_s`, observer `u_o` | Needed for observations | Their physical specification is EXT; absent from runtime |

First-order relative tilt requires common zeroth-order congruence and geometry. Thus background coincidence between mapped `u_d,w` and `u_W` is required even though first-order equality is forbidden. Strings naming backgrounds do not prove that coincidence (finding A07).

### Scale factors, metrics and bare/dressed/regional variables

| Object | Meaning | Firewall |
|---|---|---|
| `a_D=bar a` | Volume scale, `V_D ∝ a_D³`; `a_D0=gamma_w0` in current normalization | Not dressed-normalized to one |
| `background.a_w` | **Dressed** `a_D/gamma_w`, normalized to one today | GM uses this name; W09 normally calls this quantity `a`, not regional `a_w` |
| Regional `a_rw`, `a_rv` | Volume-partition scales, `f_r=f_ri a_r³/a_D³` | W09 wall branch `a_rw∝t^(2/3)`; not dressed `a_D/gamma_w` |
| Finite-infinity local scale | Spatial scale in the local wall metric with proper `tau_w` | W09 relates regional wall geometry to this construction; it is not the global dressed scale |
| H1 `a_r` | Supplied scale multiplying a selected regional reference metric | Its relation to W09 regional/FI scales remains to be established |
| 1F-B/C `a_W` | Supplied scale of the selected local wall patch | Mapping to H1 or W09 scales remains external; clock matching does not fix it |
| W09 dressed metric | Explicit spherically averaged 4D dressed background, with radial-area function | Not spatially homogeneous FLRW; radial-null construction is not a 3D perturbative pullback |
| H1 carrier | Periodic reference computational manifold with selected wall/void masks and target metric | Not itself a predicted physical four-spacetime |
| `h_r=a_r² gamma_r` | Regional spatial metric after declared pullback | Reference metric and physical scaling are distinct |
| `h_W=a_W²(1+2C_W)gamma_W` | Selected scalar-normal local metric | COND; not the complete W09 perturbed dressed geometry |
| `rho_d`, `rho_eff`, `p_eff` | Averaged dust and effective backreaction/curvature rewriting | Effective source is not automatically a local dressed Einstein source |
| `rho_r` | Imported regional background matter density | Not fixed by a regional label alone |
| `rho_C` | Sharp piecewise carrier density in 1F-A | Physical-density interpretation only conditional on selected 3D realization |

### Spatial derivatives, spectra and perturbations

| Object | Domain / metric / scaling | Meaning and restrictions |
|---|---|---|
| `D_a` in CGI | Projected derivative orthogonal to the specified congruence | Frame dependent even when CGI variables are coordinate-gauge invariant |
| `L_r=Delta_gamma_r` | Reference-comoving regional Laplace–Beltrami operator | `a_r² D_r²=L_r` for homogeneous `a_r` |
| H1 transmission operator | Weak divergence form with `K_r=J_r gamma_r^-1` on broken regional spaces | Requires metric-consistent `J_r`; finding A01 |
| Target `L_D` / `Delta_target` | Separately supplied target reference metric | Not automatically the regional or dressed Laplacian |
| 1F-C wall `D_W²` | `a_W^-2 Delta_gamma_W` | Supplied operator must be REFERENCE_COMOVING |
| Coordinate scalar gradient | `(D_i phi)_coord=partial_i phi` | No scalar `1/a` factor in lower coordinate components |
| Physical orthonormal gradient | `D_hat{i} phi=a^-1 e_hat{i}^j partial_j phi` | Requires a reference orthonormal frame; 1F-B specifies one, 1F-C underspecifies it |
| `k_code` | Dimensionless numerical mode in GM/1C system | `k_com,D=k_code H0_TS/c`; no observational map |
| `k_phys,D` | Same-mode physical background label | `k_com,D/a_D(t)` |
| `k_w`, `k_v` | Selected regional generalized spectra | `sqrt(lambda_r)/a_r`; domain, BC and metric dependent |
| `lambda_Gamma,n`, `k_C/k_D` language | Carrier/target spectral labels | Not interchangeable with regional eigenvalues; heterogeneous transfer mixes modes |
| `k_dressed` | Would require a dressed spatial spectral construction | ND from frozen physics; an externally supplied map remains EXT |
| `k_observational` | Survey-coordinate Fourier/bin label | ND; also requires observed-coordinate and fiducial-map definitions |
| `Delta_r`, `Delta_d` | CGI Laplacian density scalar, not ordinary density contrast | In a fixed harmonic `Delta_k=-k² delta_k` |
| `Z_r`, `Z` | CGI scalarized expansion perturbation | `Z_k=-k² deltaTheta_d,k`; not itself a velocity divergence |
| `G_Theta,r Z_r` | Regional inverse scalarization with explicit kernel/BC | Regional dust expansion only |
| `psi_dw` | Scalar relative boost potential | Not cosmological metric potential, background lapse or Lorentz factor |

Dimensions: use length `L`, time `T`, dimensionless scale factors and `c=1` when stated. `H,Theta,deltaTheta` have `T^-1`; `G rho`, curvature and backreaction have `T^-2` (equivalently `L^-2` in geometrized units); `nu,C,f,w,c_s²,delta` are dimensionless. If reference coordinates carry length, `Delta=L_ref delta` has `L^-2`, `Z` has `L^-2 T^-1`, and `psi_dw` has `L²/T`. If coordinates and `k_code` are nondimensionalized, the corresponding reference-length powers are absorbed in the coordinate unit. A numerical unit named COMMON_TIME does not make a proper-time expansion a common-time derivative.

## 5. GLOBAL DEPENDENCY GRAPH

```text
Tracker parameters, normalization, dust/Λ=0/tracker branch
  --DERIVED--> f, a_D, H_D, Q, R, rho_d
  --DERIVED--> effective background rho_eff, p_eff, w, c_s²
  --DERIVED--> gamma_w, tau_w, a_dressed, H_dressed, background z/distances

Effective background + imported perturbative effective-fluid framework
  --CONDITIONAL--> generic-GR component conservation/CGI system
  --MODEL_RESTRICTION--> clean comoving or barotropic closure
External ICs + epoch/rate/k conventions --EXTERNAL--> solved mode histories
  --DERIVED--> same-mode growth and logarithmic-rate diagnostics
External amplitude anchor --EXTERNAL--> Candidate A
Candidate A --MISSING--> observational fσ8

Frozen Timescape background --MISSING--> verified regional/common-spacetime embedding
Imported exact regional dust FLRW + clocks + background histories
  --CONDITIONAL--> Y=(Delta_w,Z_w,Delta_v,Z_v)
Reference carrier/morphology/metrics/BCs --EXTERNAL--> H1 realization
H1 + constitutive branch --MODEL_RESTRICTION--> F_v slaving
Y + H1 --CONDITIONAL--> effective transfer, R_Z/R_eff compatibility diagnostics
  --MISSING--> demonstrated nontrivial all-time Timescape-compatible trajectory

Regional CGI fields + regional inverses/zero modes/BCs
  --CONDITIONAL--> regional density and regional DUST expansion
Selected 3D volumes --CONDITIONAL--> sharp carrier density and metric spectra
Carrier density --MISSING--> identification with earlier target Delta_d (codomain adapter)
H1-to-local-wall realization --EXTERNAL--> wall-space fields/operators

u_W=n --MODEL_RESTRICTION--> selected wall observer
shift=0 --GAUGE--> zero-shift chart
normality --DERIVED--> omega_W=0
shear-free scalar spatial sector --MODEL_RESTRICTION--> sigma_W=0
clock identification --CONDITIONAL--> alpha_W=1/gamma_w
nu_W history --EXTERNAL--> acceleration and boost driving
psi_initial + kernel + boost BC --EXTERNAL--> scalar boost evolution
psi_dot=-alpha_W Q0 nu_W --CONDITIONAL--> psi_dw
dust expansion + wall Laplacian + psi --CONDITIONAL--> deltaTheta_W
deltaTheta_W + nu_W + a_W history --CONDITIONAL--> C_W_dot
C_W_initial --EXTERNAL--> optional C_W reconstruction

Current local kinematics --MISSING--> local dressed gravitational/source dynamics
Current local kinematics --MISSING--> global perturbed dressed/lightcone geometry
These + tracer/selection/bias/statistical initial data --MISSING--> survey observables
```

The arrows into C_W are reconstruction arrows. No independently derived metric equation feeds back to predict `nu_W` or `psi_dw`. The missing edges are not repaired by labels, state sealing, elliptic inversion or a radial-null background distance map.

## 6. PHASE-BY-PHASE AUDIT

The equation IDs refer to the independent ledger in §7. Test names below denote actual test files under `tests/`, not proofs of source correctness. Report-only phases add no runtime differential state.

| Phase | Purpose; scientific inputs and new equations | Assumptions, state, external inputs | Evidence/tests and findings | Primary verdict |
|---|---|---|---|---|
| 1B | Independent tracker; B01–B15 | Dust, Λ=0, tracker; chosen normalization and parameters; analytic background, no perturbation state | W07/W09/Buchert independently checked; background identities, units, limits, reference, wall-observable and refactor tests; D1/D2 corrections valid | **ACCEPT** |
| 1C-A | Inventory of averaged perturbations and upstream defects; P01–P08 | Separates source equations from notebook; records IC/epoch/rate/k ambiguities; no new state | GM and pinned notebook checked; exact-source inventory needs A05 correction; historical inventory is not immutable truth | **TARGETED_CORRECTIONS_REQUIRED** |
| 1C-B1 | Clean comoving rank-3 and Mészáros rank-2 systems; P03/P04, I01–I03 | Effective comoving sector versus dust-only comparison; external LCDM IC recipe and epoch/rate choices | `test_clean_perturbation_systems`, IC, oracle, residual/convergence tests; correct matrices and signs; Short–Coles attribution A05 | **TARGETED_CORRECTIONS_REQUIRED** |
| 1C-B2 | Barotropic rank-4 systems and tilt-variable transformations; P05–P08 | Barotropic closure is extra physics; D3, tilt and k conventions mandatory; upstream printed branch retained as reproduction | `test_barotropic_systems`, forensics, oracle, artifact schema; D2 corrected, D3 explicit; no unique physical barotropic Timescape prediction | **ACCEPT_WITH_CLARIFICATIONS** |
| 1D-A | Growth/observable meaning; G01–G04 | Fixed nonzero mode, chosen growth coordinate; no new evolution | Source definitions and analytical chain rule checked; ordinary density, CGI amplitude and tracer divergence kept distinct | **ACCEPT_WITH_CLARIFICATIONS** |
| 1D-B | Growth histories, crossings, rates, time/epoch scenarios | No added differential state; supplied solved history, reference epoch and conventions | `test_growth_*`; zero/pole handling, sign and unit conversion sound; numerical normalization is not a spectrum | **ACCEPT_WITH_CLARIFICATIONS** |
| 1D-C | Statistical/observational closure audit; G05–G06, O01–O04 | Spectrum, smoothing geometry, amplitude and velocity map external; report only | Definitions independently checked; no spectrum runtime authorized; generic FLRW comparator does not become Timescape | **ACCEPT_WITH_CLARIFICATIONS** |
| 1D-D-t | Fresh equation-level D3/frame adjudication | Fixed dust-frame convention and same closure; no new dynamical branch | GM actual (4.10), (4.13), (4.15), DBE component equations; §9 reproduces result independently; later BDE shorthand citations must not replace this derivation | **ACCEPT_WITH_CLARIFICATIONS** |
| 1D-D | Anchored density-growth Candidate A; G05 | External amplitude, same-mode/scale-independent assumptions, stated coordinate; no new state | `test_anchored_density_growth`; valid conditional identity, not σ8/fσ8 prediction; no downstream barotropic default | **ACCEPT** |
| 1E-A | Dressed-observable bridge audit; O01–O04 | Background dressing known; tracer, velocity, spectral and survey mapping absent | W09 and generic count identities support withheld authorization; no new runtime | **ACCEPT_WITH_CLARIFICATIONS** |
| 1E-B | Lightcone and frame coefficient inventory; O01–O04, F01–F02 | Common perturbed spacetime, chosen congruences and photon/source data required | DBE/BDE and CL checked in relevant equations; generic formulas valid; no evaluated Timescape lightcone | **ACCEPT_WITH_CLARIFICATIONS** |
| 1E-C | Comparison of perturbed dressed geometry, imported frameworks and transfer options | A 4D W09 background exists; its perturbation can be parameterized, but evolution is missing | Central kinematic conclusion supported; exhaustive comparator/source-completeness claims not fully independently recertified in this audit | **NOT_FULLY_VERIFIABLE** |
| 1E-D | Regional exact dust systems, formal matching-domain ontology and compatibility package; H01–H03/H12 | Two imported regional FLRW systems; four intrinsic variables; formal candidate fifth partition variable before selection; maps/clocks/BCs external | GM/DBE/Buchert support conditional equations; Γ not a physical junction; three mismatch components correct; A07 requires stronger background-compatibility classification | **TARGETED_CORRECTIONS_REQUIRED** |
| 1E-E | Select mathematical H1 carrier/transfer realization | Morphology, embeddings, spaces, normalization and constitutive realization selected, not derived from Timescape; no new propagated state | Design equations and later implementation agree; conditional selection is legitimate, not a uniqueness claim for morphology | **ACCEPT_WITH_CLARIFICATIONS** |
| 1E-F | Matrix H1 transfer, effective constitutive closure, partition mismatch; H04–H12 | Rank 4 intrinsic; F_v/J_Xi algebraic; nondegenerate A_P; background and operator jets external | `test_phase1e_f_h1_transfer`; dynamic versus constructed checks correctly separated in v2; no proof of generic all-time admissibility from zero-RHS identity | **ACCEPT_WITH_CLARIFICATIONS** |
| 1E-G | Continuum H1 on fixed reference geometry; H04–H13 | Fixed pulled-back metrics, homogeneous clock maps, selected interface/BC; rank 4; physical volume only in dimension 3 | `test_phase1e_g_continuum_h1`; meaningful manufactured/convergence/mutation-style tests, but A01 metric/measure inconsistency accepted; A07 embedding still absent | **TARGETED_CORRECTIONS_REQUIRED** |
| 1F-A | Regional inverse scalarization, sharp density, spectra and scalar boost; S01–S06/F01 | Explicit regional constants and Neumann BC; externally chosen density/spatial realization; no extra propagated variable here | `test_phase1f_a_*`; correct broken-density semantics and codomain firewall; eigenbasis uniqueness qualification and upstream A01 exposure | **ACCEPT_WITH_CLARIFICATIONS** |
| 1F-B | Propagate scalar relative boost; F01–F05 | External ν, α, a_W, wall expansion history, compatible initial data, kernel and boost-specific boundary; intrinsic rank 5 | `test_phase1f_b_*`; v2 boundaries and v3 clock corrections withstand review; BDE equation attribution A04; background coincidence A07 not checked by IDs | **TARGETED_CORRECTIONS_REQUIRED** |
| 1F-C | Clock anchor, normal-wall ADM kinematics and optional trace reconstruction; F06–F12 | Normality/shear sector and zero-shift gauge; ν/spatial realization external; ranks 5 or reconstruction-augmented 6 | `test_phase1f_c_*`; core signs/factors independently rederived and mutations killed; A02/A03/A04/A06 corrections | **TARGETED_CORRECTIONS_REQUIRED** |

No phase is assigned `INVALIDATED_BY_UPSTREAM_ERROR`: the known upstream mathematical errors are not blindly consumed by the accepted independent equations. `NOT_FULLY_VERIFIABLE` for 1E-C concerns exhaustive source/comparator coverage, not a discovery that its central missing-closure conclusion is false.

## 7. MASTER EQUATION LEDGER

This ledger groups equivalent implementations and algebraic derivatives, rather than counting the same equation once per wrapper, matrix, solver and test. Variables, units and spaces are inherited explicitly from the group headers and §4. A verdict of “correct” means correct in that declared context, not uniquely predicted by Timescape.

Implementation abbreviations below are relative to `src/timescape_fsigma8/`: `BG=background/`, `P=perturbations/`, `G=growth/`, `H=transfer/`, `FA=phase1f_a/`, `FB=phase1f_b/`, `FC=phase1f_c/`. Report references are under `reports/`. No paper equation number is invented for a project-selected closure.

### Background: homogeneous, volume-average time t; no perturbative spatial operator

Let `f=f_v`, `f_w=1-f`, `A=3 f0 H_D0`, `b0=(2+f0)(1-f0)`. Here `b0` is my dimensionless abbreviation, **not W09's dimensionful b**. All derivatives in B01–B14 are with respect to `t`, except where `tau_w` is displayed. Densities have dimension `1/(G T²)`.

| ID / phase | Equation and independent check | Source / derivation | Class | Implementation; protecting tests; verdict |
|---|---|---|---|---|
| B01 / 1B | `f=At/(At+b0)`, `f_w=1-f` | W09 (B2); GM (5.6) | FTS | `BG/tracker.py:fv`; background/limit tests; correct |
| B02 / 1B | `f_dot=f(1-f)/t`; `f_ddot=-2 f²(1-f)/t²` | Differentiate B01 | FTS | `dfv_dt`, `d2fv_dt2`; finite differences/identities; correct |
| B03 / 1B | `a_D=3 a_D0 H_D0 t/(2+f0) (f0/f)^(1/3)`; `a_D0=(2+f0)/2` | W09 (B1), normalized dressed scale | FTS | `BG/tracker.py:a_D`, parameters; normalization tests; correct |
| B04 / 1B | `H_D=(2+f)/(3t)`, `Theta=3H_D`, `a_D_dot=H_D a_D` | B02–B03; W09 (B3) | FTS | `H_D`, `Theta`, `da_D_dt`; identities; correct |
| B05 / 1B | `Q=2 f(1-f)/(3t²)`, `R=-6f/t²` | Two-scale Buchert Q and W09 curvature parameters | FTS | `Q_D`, `R_D`; Buchert constraint/limits; correct |
| B06 / 1B | `Q_dot=-2 f(1-f)(1+2f)/(3t³)`; `R_dot=6 f(1+f)/t³` | Differentiate B05, independently of upstream | FTS | `dQ_D_dt`, `dR_D_dt`; derivative tests; D2 corrected correctly |
| B07 / 1B | `8πG rho_d=4(1-f)/(3t²)`; `rho_d_dot=-Theta rho_d` | W09 (B4),(B6), mass conservation | FTS | `rho_d`, `drho_d_dt`; density/reference tests; D1 corrected correctly |
| B08 / 1B | `3H_D²=8πG rho_d-(R+Q)/2`; `3 a_D_ddot/a_D=-4πG rho_d+Q` | Buchert (10a)–(10b), Λ=0 | GR | `test_background_identities`; independently substituted tracker residual ≈1.32e-15 relative scale; correct |
| B09 / 1B | `Q_dot+6H_D Q+R_dot+2H_D R=0` | Buchert (13a), Λ=0 | GR | Background integrability test; correct |
| B10 / 1B | `rho_eff=-(Q+W)/(16πG)`, `p_eff=-Q/(16πG)+W/(48πG)`; `W=R-6K_D/a_D²`, tracker application `K_D=0` | GM (3.12)–(3.13) | COND | `BG/effective_fluid.py`; effective-background tests; correct rewriting, K_D split explicit |
| B11 / 1B | `rho_eff=f(8+f)/(24πGt²)`, `p_eff=-f(4-f)/(24πGt²)` | Substitute tracker into B10 | FTS | `rho_eff`, `p_eff`; reference/limits; correct |
| B12 / 1B | `w=-(4-f)/(8+f)`; `c_s²=p_dot/rho_dot=-(2+2f-f²)/(2+f)²`; `w_dot=-Theta(1+w)(c_s²-w)` | Differentiate B11; GM (3.17) | FTS | `w_eff`, `cs2_eff`; derivatives/rescaling tests; correct background quantities, not a perturbative constitutive proof |
| B13 / 1B | `Omega_m=4(1-f)/(2+f)²`, `Omega_R=9f/(2+f)²`, `Omega_Q=-f(1-f)/(2+f)²`; sum=1 | B04–B08; W09 (B4)–(B6) | FTS | `Omega_m/R/Q`; dimensionless/limit tests; correct |
| B14 / 1B | `gamma=(2+f)/2`, `gamma_dot=f(1-f)/(2t)`, `d tau_w/dt=1/gamma`; `tau_w=2t/3+2b0/(27f0 H_D0) ln[1+9f0 H_D0 t/(2b0)]` | W09 (B7),(B12), direct integration with zero origin | FTS | `BG/observables.py`; proper-time derivative and endpoint tests; correct |
| B15 / 1B | `a_dress=a_D/gamma`; `H_dress=gamma H_D-gamma_dot=(4+f+4f²)/(6t)`; `1+z=1/a_dress` | W09 (28),(38),(B8) | FTS | `a_w`, `H_dressed`, `redshift`; independent derivative/reference tests; correct **dressed**, not regional scale |

No radiation-era accuracy follows from the early-time limit of these dust tracker formulas. The EdS/Milne limits are mathematical limits of the specified branch, not complete early-universe or one-region perturbation models.

### Perturbations and ICs: dust-frame CGI system, first order

`Delta`, `Z`, pressure scalar `Ptilde` and tilt scalar `Vtilde` use the GM scalarization and fixed harmonic. `L=a² D²` is comoving; `D² Q_k=-k² Q_k/a²`. The effective component is an imported perturbative description of an averaged source. Its local perturbative closure does not follow from the background's effective-fluid rewriting.

| ID / phase | Equation | Source / independent derivation | Class | Implementation; tests; verdict |
|---|---|---|---|---|
| P01 / 1C-A onward | `Delta=L delta`, `Z=L deltaTheta`, hence harmonic `Delta=-k²delta`, `Z=-k²deltaTheta` | GM (2.19)–(2.24); BDE (74) | GR | `G/mapping.py`, FA inverses; fixed nonzero-mode tests; correct with specified metric and clock |
| P02 / 1C-A | `delta_dot=-(1+w)deltaTheta-Theta(c_s²-w)delta-(1+w)div V` | First-order effective-component energy conservation in geodesic dust frame | COND | Source reconstruction in §9; correct after effective-fluid assumptions |
| P03 / 1C-B1 | `Delta_d_dot=-Z`; `Z_dot=-2Theta Z/3-4πG(rho_d Delta_d+rho_eff Delta_eff)`; `Delta_eff_dot=wTheta Delta_eff-(1+w)Z` | GM (4.21)–(4.23); impose (4.20), nonzero scalar sector | COND | `P/systems.py:comoving_matrix`; matrix/residual/oracle tests; correct |
| P04 / 1C-B1 | `Delta_ddot+(2Theta/3)Delta_dot-4πG rho_d Delta=0` | GM (4.27); omit effective clustering for comparison | COND | `meszaros_rhs`; sign/refactor/oracle tests; correct comparison, not authorized exact Timescape growth |
| P05 / 1C-B2 | `Ptilde_eff=c_s² Delta_eff` | GM (4.13); imposed perturbative barotropy | SECTOR | `P/barotropic.py`; explicit branch; physically additional, not background-derived |
| P06 / 1C-B2 | `Delta_eff_dot=(w-c_s²)Theta Delta_eff-(1+w)Z+(k²/a_D)Vtilde` | GM (4.10)+(4.13), conservation derivation | COND | `_a33`, `barotropic_matrix`; branch tests; derived D3 branch correct |
| P07 / 1C-B2 | Replace coefficient in P06 by `(w+c_s²)Theta` | GM printed (4.15); pinned notebook | REJECT | Explicit `PRINTED_4_15`; correctly reproduced but unsupported as the derived equation |
| P08 / 1C-B2 | `Z_dot=-2Theta Z/3-4πG[rho_d Delta_d+rho_eff(1+3c_s²)Delta_eff]`; `Vtilde_dot=Theta(w-1/3)Vtilde-c_s²Delta_eff/a_D` | GM (4.16)–(4.17) | COND | `barotropic_matrix`; matrix and tilt-equivalence tests; correct |
| P09 / 1C-B2 | `Vtilde=(1+w)V`; `V_dot=Theta(c_s²-1/3)V-c_s²Delta_eff/[a_D(1+w)]`; transformed matrix `Mtilde=T M T^-1+T_dot T^-1` | GM (4.8) and B12 | COND | `transform_barotropic_state`, transform matrix; independent equivalence checks; correct |
| P10 / 1C-B2 | `k_matrix=k_paper a_D0 h_LCDM/h_TS` | Preserve same present physical mode under declared numeric Hubble-unit conventions | COND | `resolve_wavenumber`; convention tests; correct, not an observational spatial transfer |
| I01 / 1C-B1 | `q(a)=(5/6)(Omega_m/Omega_L)^(1/3) B_x(5/6,2/3) sqrt[1+Omega_m/(Omega_L a³)]`, `x=Omega_L a³/(Omega_m+Omega_L a³)` | Independently reduce flat dust+Λ growth ODE; **not** printed Short–Coles (11)–(12) as claimed | COND | `P/initial_conditions.py:qplus`; quadrature in scratch agrees; A05 citation/test correction |
| I02 / 1C-B1 | `Delta_i=.066 q(z_i)`; `Z_i=-.066 q_z[-(1+z_i)H_LCDM/H0]`; `Delta_eff,i=0` | GM §5.1.2, pinned initial recipe; Hogg (14); forward difference ε=1e-5 explicit | EXT | IC/scenario tests; valid external initialization, not independently predicted perturbation normalization |
| I03 / 1C-B1 | Converted rate `Z_target=Z_LCDM (h_LCDM/h_TS) H0_TS,target`; epoch root `z_dress(t_i)=20` is distinct from `t_i=.218 Gyr` | Units and B15 | COND | Epoch and unit tests; correct explicit alternatives; upstream-unconverted branch is reproduction only |

### Growth and observational definitions

| ID / phase | Equation | Space/clock/assumptions | Class | Location; protection; verdict |
|---|---|---|---|---|
| G01 / 1D | `G(t)=Delta(t)/Delta(t_ref)` | Same nonzero mode, reference amplitude nonzero | COND | `G/pipeline.py`, histories; normalization/crossing tests; correct signed mode growth |
| G02 / 1D | `f_bare=d ln\|Delta\|/d ln a_D=-3Z/(Theta Delta)` | Piecewise away from zeros; same dust-frame amplitude | COND | `G/rates.py:f_bare`; roots and analytic derivatives; correct |
| G03 / 1D | `f_dress-coordinate=gamma H_D/H_dress f_bare=((2+f)²/(4+f+4f²))f_bare` | Change growth coordinate, **not** density/congruence | COND | `dressed_chain_factor`, `f_dressed`; correct; factor ≈1.084156 at f0=.737 |
| G04 / 1D | `dDelta/dln a_D=-3Z/Theta`; dressed derivative multiplies G03 factor | No division by Delta; zero-crossing safe | COND | Rate/crossing tests; correct |
| G05 / 1D-D | `A_anchor=sigma_ref G`; `Q_anchor=f_coordinate A_anchor=sigma_ref dG/dln a_coordinate` | Candidate A enforces positive G/no density crossing and A1–A6; external same-frame amplitude | COND | `G/anchored_diagnostic.py:479`; positive-growth/anchor/identity tests; valid conditional diagnostic |
| G06 / 1D-C | `sigma_R²=∫ dk k² P(k) \|W_R(k)\|²/(2π²)` | Homogeneous/isotropic statistical Fourier construction, specified metric/units/window | COND | Report only; definition does not supply P, geometry or σ8; no runtime prediction |
| O01 / 1E | `1+z_obs=(k·u_s)_s/(k·u_o)_o` | Photon null geodesic and physical source/observer in one metric | GR | CL (1); reports; generic identity, missing Timescape perturbative inputs |
| O02 / 1E | `D_IJ''=T_IK D_KJ`; counts involve `det D`, source current and `dλ/dz` | Affine photon parameter; screen metric/Jacobi map | GR | CL (2)–(4); reports; correct generic optics, not an evaluated dressed observable |
| O03 / 1E | `deltaTheta=3(C_dot-H nu)+a^-1 partial_i v^i` in proper-time scalar chart | First-order almost-FLRW, zero shift; C is minus conventional spatial Ψ | COND | 1E-B expansion derivation; explains why Z alone is not peculiar divergence |
| O04 / 1E | `s_parallel=x_parallel+v_parallel/(aH)`; `delta_g^s=(b+f mu²)delta_m` | FLRW/plane-parallel/continuity/tracer and bias assumptions | COND | Comparator only; REJECT for an unqualified Timescape application; no observational runtime |

### Regional, H1 and constitutive equations

All regional equations below are first-order perturbations about **supplied exact regional dust-FLRW backgrounds**. Primes are regional proper time; dots are declared common time. Spatial transfer uses fixed reference metrics and maps unless otherwise explicitly supplied. `mathscr R/Q/W` are scalarized perturbations, not independent background quantities.

| ID / phase | Equation | Derivation / source and additional content | Class | Implementation; tests; verdict |
|---|---|---|---|---|
| H01 / 1E-D–G | `Delta_r'=-Z_r`; `Z_r'=-2H_r Z_r-4πG rho_r Delta_r` | GM (2.22)–(2.23), DBE (32)–(33), dust specialization | COND | `H/h1_realization.py:regional_evolution`; regional term checks; valid imported system, embedding A07 |
| H02 / 1E-D–G | `dot Delta_r=-alpha_r Z_r`; `dot Z_r=alpha_r(-2H_rZ_r-4πG rho_rDelta_r)`; second jets by product rule | Chain rule with homogeneous supplied alpha_r | COND | Same function; jet perturbations; correct coefficients, not proof backgrounds satisfy dust equations |
| H03 / 1E-D–G | `mathscr R_r=-(4/3)Theta_r Z_r+16πG rho_r Delta_r` | First variation of scalar Hamiltonian constraint, GM (2.13), Λ=0 | COND | `regional_evolution`; curvature derivative tests; algebraic constraint, not additional state |
| H04 / 1E-E–G | `J_r=dmu_(Phi_r*gamma_r)/dmu0`, `K_r=J_r gamma_hat_r^-1`; `A(u,v)=Σ∫ K_r^ij ∂i u ∂j v dmu0` | Selected elliptic transmission realization | COND | `H/continuum_geometry.py`, backend; SPD/flux/convergence tests; valid if J matches metric, A01 |
| H05 / 1E-E–G | `A u=-Q0(J s)` weakly; `T_r s=L_target u_r` | Green inverse on selected constrained space, source injection and target scalarization | COND | Matrix/continuum backend; projected-source roundtrip; correct conditional operator, not physical transfer derivation |
| H06 / 1E-E–G | `[u]_Gamma=0`, `[K∂u·n]_Gamma=0`; one common kernel removed | Selected mathematical transmission BC and normalization | EXT | Backend constraints; trace/flux sign/global kernel tests; not material/Israel matching |
| H07 / 1E-G | `dot T_r=0`, `d(T_r s)/dt=T_r dot s` | Only fixed pulled-back metric, morphology and target branch | COND | `continuum_bridge`; finite-difference jet tests; no general transfer/derivative commutation claim |
| H08 / 1E-F–G | `A_W=R_v-R_w`; `A_Q=(2/3)(1-2f)(Theta_v-Theta_w)²`; `B_Q=(4/3)f(1-f)(Theta_v-Theta_w)`; `A_P=A_W-3A_Q`, `B_P=-3B_Q` | Variation of selected two-region Q/W ansatz | COND | `two_region_coefficients`; term tests; requires compatible clock/congruence realization, A07 |
| H09 / 1E-F–G | `C_R=f_w T_w mathscr R_w+f_v T_v mathscr R_v`; `E=T_vZ_v-T_wZ_w`; `F_v=-(C_R+B_P E)/A_P` | Selected transfer plus `mathscr W-3 mathscr Q=0` constitutive branch | COND | `evaluate_h1_realization`; nondegeneracy and constructed-pressure tests; F_v algebraic, no fifth state |
| H10 / 1E-F–G | `mathscr Q=A_Q F_v+B_Q E`; `mathscr W=C_R+A_WF_v`; `Delta_eff=(mathscr Q+mathscr W)/(Qbar+Wbar)`; `Ptilde=-C_P/[3(Qbar+Wbar)]` | GM effective-source definitions after selected transfer | COND | H1 runtime; effective-denominator and residual tests; correct conditional algebra |
| H11 / 1E-F–G | `rho_d=Σ f_r rho_r`; `m_r=f_r rho_r/rho_d`; `Delta_d=m_w T_wDelta_w+m_v T_vDelta_v+[(rho_v-rho_w)/rho_d]F_v`; `Z=-dot Delta_d` | Mass-weighted selected transfer; expansion defined by target continuity | COND | H1 runtime; analytic source/operator jets; R_Delta is constructed |
| H12 / 1E-F–G | `Xi_r=alpha_rTheta_r`; `J_Xi=[dot F_v-A_fF_v-f_vf_w E_DeltaXi,0-J_f]/(f_vf_w)`; `A_f=(1-2f)(Xi_v-Xi_w)` | Selected partition relation solved algebraically for mismatch; fixed-reference branch has J_f=0 | COND | H1/continuum bridge; branch/clock tests; not an independently predicted clock or interface evolution |
| H13 / 1E-D–G | `R_Z=dot Z+2Theta Z/3+4πG(rho_dDelta_d+rho_effDelta_eff)+12πG rho_eff Ptilde`; `R_eff=dot Delta_eff-wTheta Delta_eff+(1+w)Z+Theta Ptilde` | Target effective equations applied to reconstructed fields | COND | Runtime fail-closed tests including nonzero cancellations; dynamic compatibility, not an automatic identity |
| H14 / 1E-D–G | `dot C_Delta=-C_Z`; `dot C_Z=-2Theta C_Z/3-4πG(rho_d C_Delta+rho_eff C_eff)`; `dot C_eff=wTheta C_eff-(1+w)C_Z` | Subtract two **already compatible** clean systems | COND | `compatibility_mismatch_rhs`; correct homogeneous mismatch system; zero input→zero RHS is not a proof of invariant admissible regional data |
| H15 / 1E-G | `V_r=V_ref,r a_r³`; `f_v=V_v/(V_v+V_w)` | Physical 3-volume with declared metric normalization | COND | Continuum volume tests, dimensional covariance; correctly rejects physical interpretation in d≠3 |

### Density, spectra and boost/geometry

| ID / phase | Equation | Context / derivation | Class | Location; protection; verdict |
|---|---|---|---|---|
| S01 / 1F-A | `L_r delta_m,r=Delta_r`, `L_r deltaTheta_d,r=Z_r` | Reference-comoving regional inverse, prescribed Neumann BC and mean | COND | FA density/expansion/operators; inverse and kernel tests; correct |
| S02 / 1F-A | `rho_C\|r=rho_r(1+delta_r)`; `rhobar_C=Σ f_r rho_r`; `delta_C\|r=(b_r-1)+b_r delta_r`, `b_r=rho_r/rhobar_C` | Sharp 3D density assembly | COND | FA density; mean/volume/intertwining tests; correct, δC includes regional background contrast |
| S03 / 1F-A | `L_broken delta_C\|r=b_r Delta_r` | Regional differentiation only, excluding interface distributions | COND | FA density; broken/unbroken tests; correct, not a global smooth perturbation identity |
| S04 / 1F-A | `K_r q=lambda_r M_r q`, `q^T M_r q=1`, `k_phys,r=sqrt(lambda_r)/a_r` | Selected regional metric spectrum | COND | FA spectral; eigenpair/mass normalization tests; eigenbasis convention remains arbitrary within degeneracies |
| S05 / 1F-A | `K_C q=lambda_Gamma M_C q`; transfer kernel by projection of T_r modes into target/carrier basis | Selected metric-weighted carrier spectrum | COND | FA spectral; no diagonal-mode assumption; not observational k |
| S06 / 1F-A | Destination density = external spatial sampling/pullback; mean recomputed with declared destination measure/Jacobian | Same-slice scalar-density prescription, no derived spacetime/time-shift transfer | COND | FA dressed; measure/mean tests; external map remains necessary |
| F01 / 1F-A–C | `u_d,w=gamma_dW(u_W+v)`, `u_W·v=0`; `gamma_dW=1+O(v²)` | Common metric, normalized timelike vectors, first-order tilt | GR | FA/FB frame contracts; independently derived; no background gamma_w identification |
| F02 / 1F-A–C | `Theta_d,w-Theta_W=D_a v^a+O(2)`; `D_W²psi=deltaTheta_d,w-deltaTheta_W` | F01 plus scalar `v_a=D_a psi`; coincident background required | COND | FA boost/FB/FC; sign mutations killed; BDE (14)–(16) attribution wrong, A04 |
| F03 / 1F-B | `A_d,a=A_W,a+dot v_<a>+(Theta_W/3)v_a+O(2)=0` | Direct acceleration expansion about common shear-free background; geodesic dust | COND | FB derivation/dynamics; correct, with projected proper derivative |
| F04 / 1F-B | `dpsi/dtau_W=-Q0 nu_W`; `partial_t psi=-alpha_W Q0 nu_W` | Normal acceleration plus scalar-gradient commutator and fixed kernel convention | COND | FB propagation; nonunit/time-varying clock tests; correct |
| F05 / 1F-B | `partial_t v_hat{i}+H_W^(t)v_hat{i}=-alpha_W D_hat{i}nu_W` | Physical orthonormal components in selected fixed-reference frame | COND | FB orthonormal-gradient implementation; nonzero-H test; **no second alpha multiplying H_W^(t)** |
| F06 / 1F-C | `t_common=t_TS`, `bar tau_W=tau_w`, hence `bar alpha_W=1/gamma_w` | Explicit clock identification, not generic Lorentz transformation | COND | FC clock bridge; identity/provenance tests; correct conditional relation |
| F07 / 1F-C | `N_W=alpha_W(1+nu_W)`; `A_W,i=partial_i ln N_W=partial_i nu_W+O(2)` | Normal congruence, homogeneous background alpha; BMR (2.5)–(2.6) | GR | FC geometry; sign correct; output component mismatch/ambiguity A02 |
| F08 / 1F-C | `K_ij=-(1/2N)partial_t h_ij`, `Theta_W=-K` | Signature −+++ and zero shift; BMR (3.1),(2.37)–(2.39) | GR | FC docstring plus independent derivation §10; sign correct |
| F09 / 1F-C | `bar Theta_W=3H_W^(t)/alpha_W`; `deltaTheta_W=(3/alpha_W)(C_dot-H_W^(t)nu_W)` | First-order selected conformally isotropic spatial metric | COND | FC trace reconstruction; direct metric derivation; correct |
| F10 / 1F-C | `C_dot=H_W^(t)nu_W+(alpha_W/3)(deltaTheta_d,w-D_W²psi)` | F02+F09, kinematic reconstruction | COND | FC geometry:195; duplicate-alpha mutation killed; linear-regime gate missing, A03 |
| F11 / 1F-C | `D_W²phi=a_W^-2 Delta_gamma_W phi` | Homogeneous a_W; terms C×phi are second order when phi is first order | GR | FC geometry wall Laplacian; omitted-a² mutation killed; correct |
| F12 / 1F-C | `omega_W=0` from normality; `sigma_W=0` in selected conformally isotropic fixed-reference sector | Frobenius versus tracefree extrinsic curvature | GR | Normality implies vorticity only; **the separate sigma_W=0 choice is SECTOR**, not inferred from normality |
| F13 / all frame audits | `dot Theta=-Theta²/3-sigma_ab sigma^ab+omega_ab omega^ab-R_ab u^a u^b+nabla_a A^a`; `nabla_a A^a=D_a A^a+A²` | Ricci identity with A=u·∇u; BMR (4.14) after conditional Einstein substitution | GR | Independent §10 derivation; first-order acceleration divergence has **plus** sign |

The equations in a row that displays a rejected alternative or a separately imposed condition are logically separate claims: e.g. O04 is a conditional FLRW comparator, not a second classification of a Timescape prediction; F12's generic vorticity implication does not classify the distinct shear restriction as GR-derived.

### Generic Einstein constraints — audited boundary, not additional runtime closure

The report-level use of ADM constraints must distinguish their generic identity from their unavailable dressed source specialization. With `E=T_ab n^a n^b` and `J_i=-h_i^a T_ab n^b`, BMR (3.3)–(3.4) gives:

| ID | Relation | Classification and disposition |
|---|---|---|
| E01 | `R^(3)+K²-K_ij K^ij=16πG E+2Λ` | GR for a metric and its actual Einstein source; not an extra implemented FC closure |
| E02 | `D_j K^j_i-D_i K=8πG J_i` | GR under the same source premise; momentum density is frame dependent |
| E03 | `G_ab[g_dressed]+Λ g_ab=8πG T_ab[regional dust]` without a demonstrated source/geometry transfer | REJECT; no such identification authorized by current runtime |
| E04 | Prescribing constant mean curvature to choose a foliation before identifying a physical observer | GAUGE as a mathematical slicing choice; it does not derive the physical wall congruence. Imposing it on an already physically fixed wall congruence would instead be a new SECTOR claim |

The effective-fluid rewriting of averaged scalar equations supplies neither all components of a local stress tensor nor a theorem that the reconstructed C and external ν solve E01/E02 with regional dust.

## 8. PRIMARY-SOURCE AUDIT

`SOURCE_VERIFIED` below is confined to the listed equation/claim scope. It does not certify every equation in a paper.

| Source | Independently inspected scope | Status and result |
|---|---|---|
| [W09, arXiv:0909.0749v2](https://arxiv.org/pdf/0909.0749v2) | Actual tracker Appendix B; regional/bare/dressed definitions; (6), (11)–(14), (22)–(28), (36)–(38) in context | **SOURCE_VERIFIED** for background and distinction between local regional and global dressed geometry. No perturbative ν_W or 3D H1 pullback supplied |
| [W07, arXiv:0709.0732v2](https://arxiv.org/pdf/0709.0732v2) | (1)–(11), (18) and tracker discussion; page 3 rendered | **SOURCE_VERIFIED**. Explicit volume-average-time regional EdS scaling; does not support the naive proper-time dust-FLRW identification |
| [GM, arXiv:2511.17160v2](https://arxiv.org/pdf/2511.17160v2) | Averaged effective sources, CGI and dust-frame systems; actual (4.10), (4.13)–(4.17); Timescape §5, known defects | **SOURCE_VERIFIED** for quoted source forms and conditional framework; source contains inconsistencies, so not a blanket endorsement |
| [Buchert 2000, gr-qc/9906015v2](https://arxiv.org/pdf/gr-qc/9906015v2) | Dust foliation/domain assumptions; (9a)–(9f), (10a)–(10c), (13a) | **SOURCE_VERIFIED** for averaging, volume, mass, integrability. Does not supply local dressed metric/source closure |
| [BMR, arXiv:1912.04213v2](https://arxiv.org/pdf/1912.04213v2) | Normal lapse/acceleration (2.4)–(2.6), time conversion, extrinsic curvature/metric evolution, (4.14) | **SOURCE_VERIFIED** for generic ADM/normal and Raychaudhuri identities; no Timescape specialization inferred |
| [DBE, ApJ 395, 54 (1992)](https://articles.adsabs.harvard.edu/pdf/1992ApJ...395...54D) | Original scan, journal pp.57–60; frame choice, conservation and component CGI equations | **SOURCE_VERIFIED** for component conservation/gradient frame change used in fresh D3 derivation |
| [BDE, ApJ 395, 34 (1992)](https://articles.adsabs.harvard.edu/pdf/1992ApJ...395...34B) | Original scan, p.38 equations (14)–(23), pp.44–45 (74), fn.22 and metric harmonics | **SOURCE_VERIFIED** for first-order matter/flux and harmonic definitions; **SOURCE_DOES_NOT_SUPPORT_CLAIM** that (14)–(16) are expansion/acceleration transformation equations |
| [Short & Coles, astro-ph/0605013v2](https://arxiv.org/pdf/astro-ph/0605013v2) | Actual page 7, (11)–(12), not OCR alone | **SOURCE_DOES_NOT_SUPPORT_CLAIM** of literal implemented formula. Printed powers and beta argument differ. Implemented function independently solves the intended growth equation |
| [Hogg, astro-ph/9905116v4](https://arxiv.org/pdf/astro-ph/9905116v4) | (14), homogeneous FLRW E(z) | **SOURCE_VERIFIED** for LCDM IC Hubble-unit conversion, not Timescape dynamics |
| [Challinor & Lewis, arXiv:1105.5292v2](https://arxiv.org/pdf/1105.5292v2) | Actual (1)–(4) and distinction between general counts and almost-FLRW application | **SOURCE_VERIFIED** for redshift/Jacobi formalism; complete Timescape observed-count prediction not supplied |
| [Nazer & Wiltshire, arXiv:1410.3470v3](https://arxiv.org/pdf/1410.3470v3) | Auxiliary-FLRW matching method and stated systematics | **SOURCE_PARTIALLY_VERIFIED**; supports method being a matching prescription, not exact late-time H1/velocity closure |
| Buchert–Carfora gr-qc/0210045v1; Mourier–Heinesen 2401.09170v2; Bonvin–Durrer 1105.5280v3 | Official records/abstracts, repository citation scope; not full equation re-audit | **SOURCE_PARTIALLY_VERIFIED**. Not used as independent numerical or sign oracles here |
| [W08, 0809.1183v2](https://arxiv.org/pdf/0809.1183v2) | Direct-PDF fallback; (19)–(28), clock/redshift and relative-deceleration discussion | **SOURCE_VERIFIED** for this scope. Treating a mean lapse as a special-relativistic gamma in an analogy is not an identification with the first-order dust-to-wall Lorentz factor |
| [Buchert 2001, gr-qc/0102049v2](https://arxiv.org/pdf/gr-qc/0102049v2) | Direct-PDF fallback; (7)–(9), (12), closure discussion | **SOURCE_VERIFIED** for acceleration divergence `D·A+A²`, lapse-dependent averaging and lack of automatic closure; not a local wall-lapse prescription |
| [Roy–Buchert, 1202.5766v2](https://arxiv.org/pdf/1202.5766v2) | Direct-PDF fallback; dust assumptions, (4)–(10), deviation definitions | **SOURCE_PARTIALLY_VERIFIED**. Exact deviation equations involve local backreaction/shear/curvature information. Their `Delta_D=delta rho/rho` is not the project's Laplacian CGI Delta |
| [Balasin, 1310.3124v1](https://arxiv.org/pdf/1310.3124v1) | Direct-PDF fallback; conformally static metric, (3)–(5) | **SOURCE_PARTIALLY_VERIFIED**. A different explicit conformal/static construction is available; no equation inspected identifies its functions with H1 fields or supplies the frozen Timescape source transfer |
| [Percival–White, 0808.0003v2](https://arxiv.org/pdf/0808.0003v2) | Direct-PDF fallback; RSD mapping, bias and normalization discussion | **SOURCE_PARTIALLY_VERIFIED**. Supports the extra tracer/velocity/statistical assumptions of the comparator; not a Timescape derivation |
| [Mars–Mena–Vera, 0704.0078v1](https://arxiv.org/pdf/0704.0078v1) | Direct-PDF fallback; (1)–(4), non-null embeddings and hypersurface gauge | **SOURCE_VERIFIED** for the need to specify a matching hypersurface and its deformation; a zero-measure partition alone supplies neither |
| Buchert–Carfora gr-qc/0210037v2 | Direct web access failed; no complete independently inspected source obtained | **SOURCE_UNAVAILABLE** in this audit; detailed source claims not recertified |
| Kaiser 1987; Kirchner gr-qc/0312003v1; Buchert–Ostermann 1203.6263v2; Kreiss–Winicour gr-qc/0602051v3; Williams et al.2403.15134v2; Visser1502.02758v3 | Repository citations located; no independently inspected complete source in this audit | **SOURCE_PARTIALLY_VERIFIED** at inventory/provenance level only; equations not recertified and not relied upon to prove exclusion of all alternative models |

The final two rows are deliberate limits, not evidence against those papers. In particular, this audit establishes missing derivations in the inspected frozen chain, not an exhaustive no-go theorem over the literature.

Retained key PDF SHA-256 values:

```text
GM      856bd78db8f86e46c0f5d21414ad0c1d136b176c6ac1b45418dbeebc38e920dd
W09     e37321e9d6021c6f5eb6bc5084ad331f4fca9dc0bc426097d1c5ce5ce7b2a8aa
W07     3abcc64ad95b95cf655f687515c8d85f38d6d0bfcebec1e0133a460b425db04f
B00     13f41a52f6e36fdbd4be39d570ecd728d921b5c20aeb04f3c74264347b69f36d
BMR     672efe5246aa081fe2afc4048b8ac4e6d55cc77989b1cbfbefaf000b7962aabd
DBE     3a082920b358872ec64a3706001e1a10a61a51f2e5140cf29662aa1a04b72f20
BDE     eaa273fa5982689cd55eaba7530103e8e9d77199d4b34d3d173c1e9201075b6c
SC      d20f3436170ffbd2280370ccb51d8dda09eca85c68d3b67ae2bf0810696d3e18
```

Source conflicts are not silently reconciled:

1. GM (5.7) versus W09 tracker density normalization: the implemented correction follows the latter and the constraint/mass equations.
2. Pinned notebook derivative versus differentiation of Q: independent implementation follows differentiation, not the notebook product error.
3. GM (4.15) versus (4.10)+(4.13): only the latter gives the derived branch.
4. GM's dressed `a_w=a_D/gamma_w` notation versus W09's regional `a_w`: same symbol, different objects.
5. BDE exact citation versus claim: matter/flux equations are not the claimed kinematic transformation equations.
6. Short–Coles printed (11)–(12) versus implemented beta formula: literal mismatch; independent reduction of order supports the implementation, not transcription of the printed formula.

## 9. D3 RE-ADJUDICATION

Start from component energy conservation, not the frozen verdict. Let the effective component be a perfect fluid to first order, separately conserved, with small velocity relative to the geodesic dust frame. Write `rho=rhobar(1+delta)`, `p=pbar+c_s² rhobar delta` for the imposed barotropic branch. The background obeys `rhobar_dot=-Theta(rhobar+pbar)`.

Linearizing the energy equation and subtracting background conservation gives

```text
delta_dot = -(1+w) deltaTheta
            -Theta(c_s²-w) delta
            -(1+w) div V.
```

Apply the fixed comoving scalarization and use the paper's rescaled tilt. This yields

```text
Delta_eff_dot = (w-c_s²)Theta Delta_eff
                -(1+w) Z + (k²/a_D) Vtilde.
```

This agrees with GM (4.10) after inserting (4.13). The `w+c_s²` coefficient in printed (4.15) differs by `2 c_s² Theta`. It cannot be fixed by choosing a different sign for a spatial harmonic or a consistent sign reversal of Delta: those changes act on other terms too and do not selectively reverse this diagonal coefficient. A frame transformation would also change the relevant gradient and flux terms, rather than replace just this one coefficient.

The exact matter-frame gradient transformation includes the projector change: `D_a rho|destination=D_a rho|source+rhobar_dot xi_a`. Energy density at a point is invariant at first order in the relative velocity, but its projected gradient need not be. DBE's component conservation and frame definitions support this distinction; a first-order density boost is not an arbitrary rescaling of the background lapse.

Independent verdict: **`RESOLVED_DERIVED_4_10`**. Classification of the resulting barotropic equation: `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`. Classification of printed (4.15) as the equation derived from that same premise set: `REJECTED_UNSUPPORTED`.

Runtime inspection found mandatory enums, explicit `_a33` branching and downstream label mapping. No automatic identification/default was found. `printed_4_15` remains meaningful for forensic reproduction, not for a derivation-backed result. Some docstrings/README still call the adjudication unresolved (A09).

Impact: barotropic trajectories depend on the chosen coefficient. The clean comoving and Mészáros matrices do not consume `c_s²` or D3. Candidate A accepts only those clean systems. The selected H1 clean target is likewise not a consumer of the disputed barotropic coefficient. D3 does not force recomputation of those downstream conditional constructions.

## 10. CLOCK / FRAME AUDIT AND INDEPENDENT KINEMATICS

### ADM expansion

For zero shift and `h_ij=a_W²(1+2C_W)gamma_ij`, with fixed reference gamma,

```text
sqrt(h)=a_W³(1+3C_W)sqrt(gamma)+O(2),
Theta_W=(1/N_W) partial_t ln sqrt(h),
N_W=alpha_W(1+nu_W).
```

Expanding, keeping `H_W^(t)=partial_t ln a_W` as an already common-time quantity,

```text
Theta_W = 3H_W^(t)/alpha_W
          +(3/alpha_W)(partial_t C_W-H_W^(t)nu_W)+O(2).
```

Equivalently, `K_ij=-(1/2N)partial_t h_ij` gives `K=-Theta_W`. Thus

```text
partial_t C_W = H_W^(t)nu_W+(alpha_W/3)deltaTheta_W
             = H_W^(t)nu_W+(alpha_W/3)(deltaTheta_d,w-D_W²psi_dw).
```

All stated signs and clock powers in this scalar equation are correct. No extra alpha belongs on the first term. This is a kinematic identity conditional on the metric ansatz, not an independent gravitational evolution equation.

### Acceleration and boost

With `n_a=-N partial_a t`, normalization and differentiation give `A_i=partial_i ln N`. A spatially homogeneous background alpha therefore gives `delta A_i=partial_i nu`. This is a coordinate-covector statement. Conversion to an orthonormal component inserts a reference tetrad and `a^-1`; raising a coordinate index inserts `a^-2 gamma^ij`. The distinction is necessary for interpreting the FC returned array (A02).

From `u_d=u_W+v+O(2)`,

```text
Theta_d-Theta_W=nabla_a v^a=D_a v^a+O(2).
```

The difference between the four-divergence and projected divergence is proportional to background acceleration times v; that acceleration vanishes in the selected homogeneous-lapse background. Thus the frozen compatibility sign is positive dust-minus-wall.

Dust geodesicity gives, on the shared shear-free background,

```text
dot v_<a>+H_W^(proper)v_a=-D_a nu_W.
```

For `v_a=D_a psi`, the projected gradient commutator contributes `-H_W^(proper)D_a psi`; it cancels the displayed H term. Hence `D_a(psi_dot+nu)=0`. A time-dependent spatial constant remains until the explicit kernel convention fixes it, producing `psi_dot=-Q0 nu`. Converting to common time gives `partial_t psi=-alpha_W Q0 nu`.

For physical orthonormal velocity components this becomes `partial_t v_hat{i}+H_W^(t)v_hat{i}=-alpha_W D_hat{i}nu`. The same expression with an ordinary partial-time derivative of **coordinate covector components** is not the same component equation. Phase 1F-B's orthonormal Cholesky representation handles this explicitly.

### Raychaudhuri sign

Apply the Ricci commutator to `u^b∇_b(∇_a u^a)` and differentiate `A^a=u^b∇_b u^a`:

```text
u·∇Theta = ∇_a A^a -(∇_a u^b)(∇_b u^a)-R_ab u^a u^b.
```

The expansion/shear/vorticity decomposition gives `Theta²/3+sigma_ab sigma^ab-omega_ab omega^ab` for the quadratic derivative contraction. Since `u_a A^a=0`, `u^a u^b∇_a A_b=-A²`, so

```text
∇_a A^a=D_a A^a+A².
```

Therefore the acceleration divergence has a **plus** sign on the evolution-equation right-hand side. At first order about zero acceleration, A² is second order. An Einstein substitution yields `-4πG(rho+3p)+Λ` only for a specified local source obeying that Einstein equation. BMR (4.14) agrees. GM's already documented Λ coefficient issues are outside the Λ=0 consumed branch; they must not be imported into a future nonzero-Λ implementation.

### The unresolved background embedding

A first-order dust-to-wall boost requires background coincidence. In a verified common realization this includes `bar Theta_d,w=3H_W^(t)/alpha_W` and consistent proper-time/scale mappings after pullback. The current records check matching identifiers and selected field relations but do not carry enough regional background history to establish all these conditions.

The naive W09 identification can be falsified directly. Take W09's regional wall scale `a_rw∝t^(2/3)` and `d tau_w/dt=2/(2+f)`. If this were an exact spatially flat, Λ=0 dust-FLRW metric **in proper tau_w**, its Hubble rate would be `(2+f)/(3t)` and it would satisfy `dH/dtau_w+(3/2)H²=0`. Instead:

```text
dH/dtau_w+(3/2)H² = (2+f)f(1-f)/(6t²) ≠ 0,  0<f<1.
```

At `f=.737,t=1`, the residual is `0.08841924116666666`. No choice of the dust density repairs this flat-dust acceleration/Friedmann combination. It vanishes in the endpoint limits only. This is a **conditional no-go for that identification**, fully consistent with W07's warning about the time coordinate. It is not a derivation that the Timescape tracker is wrong.

Thus the correct dictionary preserves regional proper-time H1 quantities, volume-average regional rates, the W09 finite-infinity clock and the dressed scale as different objects until the embedding problem is solved. `gamma_w` is not a Lorentz factor and does not determine `nu_W`.

## 11. SPATIAL-GEOMETRY AUDIT

The Laplacian scaling is exact for a homogeneous spatial scale factor:

```text
Delta_h phi = [sqrt(h)]^-1 ∂i[sqrt(h)h^ij∂j phi]
            = a^-2 Delta_gamma phi.
```

For a first-order phi, the first-order metric perturbation C multiplies another first-order object in the perturbed Laplacian and is omitted consistently at linear order. This omission does not apply to a generic background scalar with a nonzero spatial gradient, nor to second-order calculations.

For the pulled-back continuum geometry, `J` and `gamma^-1` must describe one metric. With the backend's uniform coordinate reference measure, a pointwise determinant relation fixes J up to the declared reference-density normalization. Allowing a nonconstant independent J changes the operator to a weighted Laplacian. Positivity, SPD and equality of total integrated volumes are insufficient (A01).

The reference torus and wall/void masks are valid computational devices. Their topology and interface are selected mathematical structure. The continuum transmission problem uses a common global constant kernel; the later regional density/boost inversions use separate regional mean and Neumann restrictions. These are different boundary problems, not inconsistent implementations of the same problem. The resulting no-flux condition is an external boundary closure and not proof of a physical matter boundary.

Γ is not automatically finite infinity, a timelike material wall, an Israel surface, or a velocity-continuity condition. A zero-volume-measure formal partition does not specify any of those structures. No such physical-junction assertion was found in the integrated runtime's authorization state.

The scalar carrier density contains sharp regional background contrast and is not the H1 transmission potential or automatically the earlier GM target Delta. `FA/density.py` explicitly records `NOT_EVALUABLE_WITHOUT_CODOMAIN_ADAPTER`. This is an honest missing edge, not a completed end-to-end density identity.

Physical/comoving operator declarations cannot prove the semantics of opaque supplied matrices. Correctly labeling a physical operator as physical is rejected by FC v2; lying by labeling it reference can double-scale it. Calling this a caller contract violation is appropriate. It does **not** excuse the separately testable metric-measure inconsistency or absent covector/tetrad component convention.

Spectral labels remain distinct and transfer is not generally mode diagonal. Constant-mode removal does not eliminate harmonic vector fields on a torus; the scalar longitudinal sector excludes them as a restriction, not a Timescape prediction. Degenerate eigenspaces also carry basis rotations/sign choices; eigenvalues and reconstructed fields can be unique while individual basis-dependent transfer coefficients are not canonical.

## 12. STATE / RANK / CLOSURE MATRIX

Rank here counts scalar state components/field species per declared mode or spatial ansatz. A discretized scalar field has many numerical degrees of freedom; calling it one variable does not make it one real-valued number. Constraint rank is operator- and boundary-dependent.

| Major stage | Differential state / intrinsic rank | Algebraic, elliptic and reconstruction outputs | External functional histories / data | Constraint and initial-data qualification |
|---|---|---|---|---|
| 1B | Analytic tracker family; no numerically propagated perturbation state | All tracker/dressed functions | Parameters, normalization, branch | Parameter count is not perturbation rank |
| 1C-B1 Mészáros | `(Delta,Delta_dot)` / 2 | Z=-Delta_dot | Background; 2 ICs; selected rate/epoch | 2 initial numbers per mode; comparison-only model |
| 1C-B1 comoving | `(Delta_d,Z,Delta_eff)` / 3 | Pressure/tilt restricted | Background; 3 ICs, selected closure | 3 initial numbers in the reduced effective system; not three local dressed metric DOFs |
| 1C-B2 | `(Delta_d,Z,Delta_eff,V or Vtilde)` / 4 | Explicit rescaling; no hidden fifth variable | Background, closure, k convention, D3 branch; 4 ICs | Regular linear ODE away from singular coefficients; barotropic continuum physical well-posedness not proven by finite-k integration |
| 1D-A–D | No new differential variables | Growth, derivatives, normalization and Candidate A | Reference epoch, external amplitude and assumptions | No new initial-data rank; a σ8-named anchor is not a statistical prediction |
| 1E-A–C | No new runtime | Formal coefficient inventories and missing-object records | Common perturbed metric/congruences/maps would be needed | No complete rank for the unchosen gravitational system |
| 1E-D | Regional `(Delta_w,Z_w,Delta_v,Z_v)` / 4 | Curvature constraints; formal partition/effective package | Regional backgrounds, clocks, realization and BCs | Intrinsic regional rank is 4; rank of complete transfer constraints not determined before selection |
| 1E-E–G H1 | Same regional state / 4 | Green/transmission fields; F_v; J_Xi; target Delta/Z/Delta_eff | Metrics, morphology, source profiles, background jets, clocks; chosen constitutive and transfer branch | F_v algebraic when A_P≠0; R_Z/R_eff restrict admissibility. 4 unrestricted initial functions for the **coupled** system are not established |
| 1F-A | Inherited regional rank / 4 | Regional density/expansion inversions, sharp density, spectra, elliptic boost at a snapshot | Zero modes, regional and boost BCs, volumes, spatial/dressed map, wall expansion if boost inferred | Connected regional Poisson problem has one constant kernel per region; fixed mean gives inverse uniqueness. No new boost evolution yet |
| 1F-B | Regional state plus psi_dw / 5 intrinsic | v from gradient; elliptic/expansion compatibility checks | ν(t,x), α_W(t), a_W(t), H_W^(t), wall expansion history, dust expansion history, initial ψ, BC/kernel | Once **both expansion histories** are prescribed and the Poisson kernel fixed, compatibility fixes ψ at each time; its initial function is not independently free |
| 1F-C driver | Same inherited variables / 5 | N, A, deltaTheta_W, Laplacian; no added evolution | External ν, spatial realization and local scale mapping; selected clock anchor and sectors | Actual function postprocesses a sealed FB result and checks alignment. It does not integrate the regional 4-state system anew |
| 1F-C optional metric | Add C_W quadrature / formal augmented 6 | Local scalar spatial metric trace | Mean-zero C_W initial field and background split | C_W is reconstruction-only relative to the current driver; its spatially varying initial function is not fixed by expansion kinematics |

The independent 32-point wall fixture has Laplacian rank 31 at explicit rank tolerance `2e-12`. With its one constant removed, the prescribed expansion difference fixes all 31 scalar-potential coefficients. This demonstrates why “one more evolution equation” and “one more freely selectable initial function” are different statements.

Differential rank 5 is therefore retained. It must not be advertised as a reduced, constraint-solved physical state rank. The optional C_W field does not change the frozen FB dynamics; if a later Einstein/source closure uses C_W to constrain ν or ψ, the dynamical/constraint analysis must be redone for that new system.

### Conditional uniqueness — exact prerequisites

| Claim | Complete input needed | What is actually unique |
|---|---|---|
| Clean mode ODEs | Background on interval, explicit closure/D3/tilt/k/units, initial vector, regular coefficients | Mode trajectory of that selected ODE, not the selected physics |
| H1 Green/transfer | Domain, masks, metric-consistent coefficients and measure, sources, transmission BC, coercive function space, kernel projection/mean, target scalarization, all time dependence | Elliptic solution and forward transfer for admissible source; not arbitrary raw zero modes or inverse regional recovery |
| H1 effective branch | Above plus compatible regional backgrounds/jets, constitutive branch, nonzero denominators and all-time R_Z/R_eff compatibility | Algebraic reconstruction at accepted times; existence of a nontrivial complete Timescape trajectory remains unproved |
| 1F-A regional reconstruction | Selected regional operator, source, mean, connected domain and BC | Scalar field on that domain; spectrum unique as eigenvalues/subspaces, not canonical signed eigenvectors |
| 1F-B | Complete common background/geometry and congruence realization; dust and wall expansion histories; ν, α, scale/Hubble histories; interpolation; initial ψ; boost-specific boundary and kernel convention; compatibility for all times | At most one compatible scalar forward solution; incompatible supplied histories yield no solution |
| 1F-C | Valid sealed FB result, explicit clock bridge, external reference wall operators and pullback, ν matching FB, frame/domain/measure identities and compatible histories | Kinematic outputs for those inputs; optional C also requires C_initial and valid split |

The repository's `CONDITIONAL_FORWARD_UNIQUENESS: GRANTED` is acceptable with these qualifications. It should be read as uniqueness **given admissible complete closure data**, not as existence for arbitrary inputs or a unique Timescape prediction. There is no verified target-only inverse reconstruction of the regional state.

## 13. TEST QUALITY AUDIT

### What the tests genuinely establish

| Test family | Strong evidence | Limitation / mutation vulnerability |
|---|---|---|
| Background identities, limits and reference values | Independent Buchert conservation/integrability, dressed Hubble derivative, normalization, limiting parameters | Agreement with a notebook alone would preserve upstream defects; separate identities are essential |
| Refactor equivalence | Detects unintended numerical changes relative to frozen implementation | Cannot establish frozen equations are physically correct |
| IC recipe | Explicit epoch/rate branches and original numerical reproduction | Bit-exact ICs and approximate CMB amplitude do not verify the cited beta-function equation; A05 escaped |
| Barotropic matrices and tilt transformations | Opposite D3 coefficients exercised; rescaling includes w_dot; corrected sound-speed derivatives | A consistent wrong source equation could pass algebra/equivalence/oracle checks; fresh conservation derivation needed |
| Growth/crossing tests | Separate Mészáros sign, nonzero reference, signed histories, no illegal logarithm at roots, physical-rate unit conversions | Dense output and self-convergence do not prove exact root completeness for arbitrary unresolved oscillatory histories |
| Anchored diagnostic | Enforces positive/no-crossing branch, same reference, clean systems, explicit anchor | `f A = sigma_ref dG/dln a` is a constructed identity, not evidence for observed σ8 or velocity |
| H1 normalization/flux/kernel | Wrong flux signs, wrong source weighting, missing global normalization and geometry/morphology perturbations detectable | Tests do not enforce determinant-consistency of metric and J; A01 accepted |
| H1 manufactured convergence | Analytic manufactured solutions give meaningful discretization evidence; heterogeneous metrics mix modes | Manufacturing a source with the same discrete operator proves roundtrip, not continuum consistency; self-convergent morphology diagnostics need independent interpretation |
| H1 dynamic residuals | Nonzero term cancellations and independent jet perturbations can detect dropped R_Z/R_eff contributions | Manufactured background jets can violate regional dust/background equations; not a physical Timescape trajectory (A07) |
| FA density/spectra | Mean, physical volume, separate metric spectra, broken versus unbroken operator and codomain distinctions | Shared assembly helpers are not independent metric or source oracles; eigenpair residual uses the same K/M |
| FB boundary/clock tests | Nonzero normal variation tests; invalid driver BC rejected; nonunit α and time-dependent α tested; H≠0 test | Earlier all-zero or tangential-only fixtures could not see those errors; some scalar-integration residuals remain construction checks |
| FC v2 scaling/sign tests | Nonunit a and α; nonzero Hν term; explicit wrong-space declaration; reversed compatibility tests | All-flat component fixtures cannot distinguish coordinate covector from orthonormal components; A02. No C smallness/positivity gate; A03 |
| Source-string and enum tests | Detect removed citations, renamed scientific status, defaults and API exposure | A reference token existing in source says nothing about the referenced equation. BDE citation error passes these tests |
| Integrity/tamper tests | Strong prevention/detection of selected stale cached scientific state | Do not establish the supplied state's physical truth or internal continuum metric consistency |

No warning-suppression pattern was found in the inspected `src`, `tests` and `scripts` search. A warning-free test run still does not establish a warning-free notebook or all possible future inputs.

### Actual in-memory mutations

Each mutation replaced one expression only in the imported FC module, rebound the public function, and ran `tests/test_phase1f_c_wall_common_geometry.py`. The disk module was unchanged.

| Mutation | Result | Tests failing |
|---|---|---|
| `wall_expansion=dust+laplacian` instead of minus | **KILLED**; 2 failed, 27 passed | Wall-dust distinction/sign; no-clock-factor compatibility |
| Omit `a_W^-2` on wall Laplacian | **KILLED**; 4 failed, 25 passed | Nonzero-H trace case; explicit scaling; scale-factor family; falsely labeled physical operator |
| Multiply the C-driver Hν term by a second α | **KILLED**; 1 failed, 28 passed | `test_metric_trace_nonzero_hubble_has_no_double_alpha_factor` |
| Reverse acceleration sign | **KILLED**; 2 failed, 27 passed | Operator scaling and acceleration-gradient tests |

These are real mutation runs, not merely claims that tests “should fail.” They do not constitute exhaustive mutation coverage of 617 tests.

### Accepted-invalid-input probes

1. In the 4×4×4 flat fixture, replace J by `1+0.2 sin(2π y/4)` while keeping the inverse metric equal to I and the integrated regional/target volumes unchanged. Construction succeeds; pointwise measure mismatch is 0.2; target scalarization differs from the flat metric result by **3.555555555555557** in max norm. This is not roundoff.
2. Supply alternating `C_initial=+1,-1` on the 32-point wall grid, with the required zero mean and metadata. Optional reconstruction succeeds; `min(1+2C)=-1.0731666666666664`. The object is outside linear perturbation theory and not a positive spatial metric.
3. At `a_W=2`, direct coordinate derivatives of ν have max magnitude .004 but the returned `wall_acceleration_covector` has .002. It is consistent with orthonormal scaling in that flat example, not with the advertised lower coordinate-index equation.

### Tolerances and independent references

FC has useful explicit scientific gates, but many `np.testing.assert_allclose(..., atol=...)` calls omit `rtol`. In NumPy the actual criterion includes the default relative tolerance, not just the displayed absolute number. At expected amplitude .004, a default `rtol=1e-7` permits roughly `4e-10` even if `atol=2e-15` is written. `atol=0` is not an exact-equality test. This violates the project's demand to record reliance on defaults and can mask small relative coefficient errors (A06). It does not mask the order-unity sign/a/α mutations actually killed above.

The metric-trace “evolution residual” subtracts the same trapezoidal update used to construct C. It checks arithmetic consistency, not integration accuracy. Nonlinear-in-time drivers and independent integrated reference/convergence tests should supplement it. Likewise `compatibility_mismatch_rhs(zeros)=zeros` is vacuous as a proof that reconstructed fields satisfy the effective dynamics; the separate R_Z/R_eff tests are the relevant checks.

Independent qplus reference: reduction of order gives `D(a)=(5/2)Omega_m E(a)∫_0^a dx/[x³ E(x)³]`, normalized by `D/a→1`. At a=1/21, .25, .5, 1 the implemented beta expression agrees to ≲6e-16 relative in the scratch quadrature. At a=.001 the absolute quadrature stopping criterion gives about 4e-11 relative agreement; it is not evidence of a beta-function defect. All scratch quadrature tolerances are explicitly recorded in `audit_checks.py`.

## 14. SCIENTIFIC RED-TEAM RESULTS

“Withstood” means the stated attack did not falsify the inspected conditional claim. It is not universal validation outside that claim's domain. A falsification may concern a citation or test guarantee rather than a physical equation.

| Attack | Result | Evidence / precise target |
|---|---|---|
| A. Wrong source equation | **FALSIFICATION_FOUND** | BDE exact equation attribution and Short–Coles printed formula mismatch, A04/A05; independently correct implementation must not be replaced by misprints |
| B. Wrong Timescape interpretation | **FALSIFICATION_FOUND** | Naive proper-time exact regional dust interpretation fails tracker background residual, A07. Current conditional implementation is not thereby disproved |
| C. Clock mismatch | **FALSIFICATION_FOUND** | Candidate identification of W09 common-time EdS regional evolution with proper-time EdS is false; FC reciprocal/FB chain factors themselves withstand review |
| D. Bare/dressed confusion | **ATTACK_WITHSTOOD** | Runtime background `a_w` is explicitly dressed; regional/target spectra not auto-identified; notation caveat remains |
| E. Regional/wall-observer confusion | **ATTACK_WITHSTOOD** | First-order u_d,w≠u_W preserved and expansion difference nonzero; shared-background prerequisite remains unproved, A07 |
| F. Gauge as physics | **ATTACK_WITHSTOOD** | Normality/shear sector and zero-shift gauge distinguished; no normality→zero-shear inference |
| G. Hidden local Einstein closure | **ATTACK_WITHSTOOD** | No integrated equation sets G[g_dressed]=8πG T[regional dust]; regional Einstein equations are imported regional equations, not that transfer |
| H. Wrong ADM sign | **ATTACK_WITHSTOOD** | Independent determinant/extrinsic-curvature derivation gives Θ=-K and correct C-driver |
| I. Wrong boost sign | **ATTACK_WITHSTOOD** | Direct divergence of u_d=u_W+v; actual reversed-sign mutation killed |
| J. Missing/duplicate lapse | **ATTACK_WITHSTOOD** | ψ_dot carries one α; common-time H carries no further α; duplicate in C driver killed |
| K. Laplacian scale factor | **ATTACK_WITHSTOOD** | Scalar Laplacian a^-2 independently derived; omission killed; gradient component issue separate |
| L. Comoving/physical operator spaces | **FALSIFICATION_FOUND** | Coordinate-covector versus orthonormal contract incomplete and metric/measure inconsistency accepted; opaque mislabeling itself remains caller violation |
| M. Interface as physical junction | **ATTACK_WITHSTOOD** | Selected Γ/BCs not promoted to finite infinity, Israel matching or material no-penetration |
| N. Hidden zero mode | **ATTACK_WITHSTOOD** | Regional/global scalar kernels and boost normalization explicit; transverse/harmonic vectors excluded as sector, not predicted zero |
| O. Circular closure | **ATTACK_WITHSTOOD** | C is reconstruction, ν remains external; no independent prediction claimed from substituting the same expansion constraint twice. Constructed test residuals are not physical evidence |
| P. Incorrect state rank | **ATTACK_WITHSTOOD** | Intrinsic ranks 4/5/+1 are defensible; constrained initial-data rank not thereby established, A08 |
| Q. False conditional uniqueness | **ATTACK_WITHSTOOD** | Unique conditional forward solution requires all compatible data; no claim of unique Timescape prediction. Existence/basis qualifications in §12 |
| R. Circular test oracle | **FALSIFICATION_FOUND** | Citation-presence tests miss demonstrably wrong references; same-update residuals cannot prove integration accuracy; physical trajectory interpretation of manufactured jets unsupported |
| S. Tolerance masking | **FALSIFICATION_FOUND** | Undeclared default rtol changes displayed tolerances; small relative errors could pass, A06; large mutations still fail |
| T. Premature observables | **ATTACK_WITHSTOOD** | No authorization/runtime for RSD, σ8/fσ8 or survey inference; Candidate A properly conditional |

## 15. ALL FINDINGS

Six S2 corrections and one S3 classification correction are counted as targeted corrections. S1 qualifications and S0 confirmations are reported separately. No finding below requests an unapproved change to a scientific equation.

### A01 — Metric and volume measure may describe different geometries

- **Severity:** `S2_TARGETED_IMPLEMENTATION_OR_TEST_CORRECTION`.
- **Phase/location:** 1E-G; [RegionalGeometrySpec](C:/Projects/timescape-fsigma8/src/timescape_fsigma8/transfer/continuum_geometry.py:146); `ContinuumH1Operator._validate_metric_normalization`, `target_scalarization`.
- **Description/evidence:** Positive J and SPD inverse metric are checked separately; volume normalization checks integrated J. The explicit nonconstant mean-preserving J probe in §13 is accepted with a flat inverse metric and changes the Laplacian.
- **Consequence:** An accepted inconsistent input can silently produce weighted diffusion instead of the LB operator of the named metric. Valid metric factories/known valid fixtures are not shown to be wrong.
- **Minimal correction:** State the reference coordinate-density normalization and validate the pointwise determinant/measure relation; add an adversary preserving total volumes. If independent metric-measure spaces are intentionally allowed, expose a different operator/classification instead of calling them the same Riemannian metric.
- **Classification:** Claim that the result is that declared metric's LB operator: CURRENT_CLASSIFICATION `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`; RECOMMENDED_CLASSIFICATION `REJECTED_UNSUPPORTED` **for inconsistent metric/J inputs only**. Valid inputs retain the conditional classification.
- **Downstream:** Potentially transfer fields, density/expansion inversions and spectra using the invalid operator; then boosts/geometry consuming those results. No blanket recomputation for proven-consistent inputs.

### A02 — FC acceleration component representation is under-specified

- **Severity:** `S2_TARGETED_IMPLEMENTATION_OR_TEST_CORRECTION`.
- **Phase/location:** 1F-C; [geometry derivation](C:/Projects/timescape-fsigma8/src/timescape_fsigma8/phase1f_c/geometry.py:47), `H1ToWallSpatialPullback`, `WallKinematicGeometryResult.wall_acceleration_covector`.
- **Description/evidence:** Output divides reference gradients by a but calls them a covector associated with `A_i=D_i nu`. At a=2 the returned .002 differs from coordinate derivative .004. No tetrad/component-kind field resolves the notation; FB does have explicit orthonormal Cholesky semantics.
- **Consequence:** A downstream coordinate tensor calculation can acquire a wrong factor of a or wrong metric contraction while all current flat-fixture tests pass.
- **Minimal correction:** Declare component basis/type explicitly, including reference tetrad conventions for curved metrics; distinguish coordinate covector, contravariant vector and orthonormal components; add nonunit-a/nontrivial-metric tests. Do not simply remove a^-1 without deciding the intended representation.
- **Classification:** `A_i=∂i ln N` remains `DERIVED_FROM_GENERIC_GR`; interpretation of the current array as a lower **coordinate** covector is `REJECTED_UNSUPPORTED` unless the representation is changed. Orthonormal interpretation is `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` about supplied gradient components.
- **Downstream:** FC acceleration consumers; not the scalar boost compatibility or C-driver equation.

### A03 — Optional C reconstruction can leave perturbative/metric validity domain

- **Severity:** `S2_TARGETED_IMPLEMENTATION_OR_TEST_CORRECTION`.
- **Phase/location:** 1F-C; [ScalarMetricTraceInitialData](C:/Projects/timescape-fsigma8/src/timescape_fsigma8/phase1f_c/models.py:908), [reconstruct_optional_scalar_metric_trace](C:/Projects/timescape-fsigma8/src/timescape_fsigma8/phase1f_c/geometry.py:195).
- **Description/evidence:** Finiteness and zero mean do not enforce small C. Alternating ±1 is accepted and produces negative `1+2C`.
- **Consequence:** A result labeled metric reconstruction may not represent a positive spatial metric or a valid first-order expansion. Small lapse/velocity gates do not control accumulated C or arbitrary initial C.
- **Minimal correction:** Explicit C linear-regime threshold checked initially and throughout reconstruction, plus positivity as a necessary but not sufficient check. Add long-time accumulation and independent nontrivial integration/convergence tests.
- **Classification:** Current conditional formula remains correct; a valid first-order metric interpretation of this counterexample is `REJECTED_UNSUPPORTED`.
- **Downstream:** Optional metric trace only. Driver-only rank-5 results and background need no recomputation because of this probe.

### A04 — BDE exact equation references do not support claimed frame laws

- **Severity:** `S2_TARGETED_IMPLEMENTATION_OR_TEST_CORRECTION`.
- **Phase/location:** 1F-B/C; [FB propagation docstring](C:/Projects/timescape-fsigma8/src/timescape_fsigma8/phase1f_b/dynamics.py:242), FB model docstrings, FC geometry:47 and phase validation reports.
- **Description/evidence:** Original BDE p.38 (14) gives first-order matter-variable invariance; (15)–(16) concern heat/particle flux combinations. They do not state the expansion or acceleration transformation attributed to them.
- **Consequence:** Repeated “source verified” and citation-presence claims are overstated. The independently derived kinematic sign remains correct.
- **Minimal correction:** Preserve the equations, cite a primary equation that actually supplies each relation or give the explicit derivation from the normalized boost and covariant definitions. Mark the derivation as generic GR, and the application as conditional. Fix source-verification tests/ledger entries accordingly.
- **Classification:** CURRENT_CLASSIFICATION often `DERIVED_FROM_GENERIC_GR` with claimed BDE (14)–(16) support; RECOMMENDED_CLASSIFICATION remains `DERIVED_FROM_GENERIC_GR` for the identity, but exact-source support is `SOURCE_DOES_NOT_SUPPORT_CLAIM`. Specific wall applications retain their additional assumptions.
- **Downstream:** Documentation/source evidence only; no numerical recomputation dictated by this finding.

### A05 — Initial-condition beta function is not printed Short–Coles (11)–(12)

- **Severity:** `S2_TARGETED_IMPLEMENTATION_OR_TEST_CORRECTION`.
- **Phase/location:** 1C-A/B1; [qplus](C:/Projects/timescape-fsigma8/src/timescape_fsigma8/perturbations/initial_conditions.py:76); initial-condition tests and inherited citation chain.
- **Description/evidence:** The rendered v2 page has extra a powers in the prefactor/square root and a different beta argument denominator from the implementation. Taken literally, the printed expression does not have the intended growing-mode small-a behavior. The implementation agrees with the independent reduction-of-order integral.
- **Consequence:** Code has a scientifically supportable IC function, but the claimed exact equation citation is false; matching upstream IC digits cannot catch this.
- **Minimal correction:** Document the source discrepancy and the independently derived corrected expression, with an appropriate verified growth-equation reference; add an independent integral/ODE and early-time-normalization test. Do not replace good code with the literal misprint.
- **Classification:** Implemented solution is `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` (flat dust+Λ input cosmology); IC amplitude/transfer into Timescape remains `EXTERNAL_CLOSURE_INPUT`. Literal attribution to printed (11)–(12): `SOURCE_DOES_NOT_SUPPORT_CLAIM`.
- **Downstream:** No IC or growth recomputation is indicated by the evidence. Provenance/test updates affect the IC chain, not its accepted numbers.

### A06 — Undeclared default relative tolerances

- **Severity:** `S2_TARGETED_IMPLEMENTATION_OR_TEST_CORRECTION`.
- **Phase/location:** Multiple test families, especially `test_phase1f_c_wall_common_geometry.py:504` and `:669`; continuum tests similarly omit rtol in several comparisons.
- **Description/evidence:** `assert_allclose` with only atol retains NumPy's default relative tolerance. An asserted 2e-15 absolute threshold can actually permit ~4e-10 at magnitude .004.
- **Consequence:** Some advertised near-machine-precision checks are looser than they appear; small relative errors may pass. This is not evidence that the actual large sign/scaling mutations passed.
- **Minimal correction:** Specify both tolerances or document intentional defaults and their scale implications; use rtol=0 for genuinely absolute tests; retain looser convergence tests where justified.
- **Classification:** Claim of the tighter stated numerical guarantee is `REJECTED_UNSUPPORTED` until the actual tolerance is recorded; no physical equation reclassification follows.
- **Downstream:** Re-run affected tests after tightening; numerical outputs need recomputation only if a newly exposed defect is demonstrated.

### A07 — Background embedding and physical compatibility are not established

- **Severity:** `S3_SCIENTIFIC_CLASSIFICATION_CORRECTION`.
- **Phase/location:** 1E-D–G and coupling into 1F-B/C; `H/h1_realization.py:regional_evolution`, `two_region_coefficients`; `tests/test_phase1e_g_continuum_h1.py:1177`; FB scenario background-identity checks; FC `IRREDUCIBLE_GEOMETRIC_INPUT` label.
- **Description/evidence:** (i) W09 regional common-time EdS evolution cannot be made exact proper-time flat-dust FLRW by simply using the W09 wall lapse; explicit nonzero residual in §10. (ii) The “nontrivial trajectory” continuum fixture uses constant rho_w=1 with Theta_w=.6 and alpha_w=1, so rho_dot=0 whereas proper dust conservation requires common-time rho_dot=-.6. It is a useful algebraic jet fixture, not a physically admissible regional dust background trajectory. (iii) First-order boost background coincidence is required but background IDs alone do not establish it.
- **Consequence:** The conditional regional/transfer algebra is not a verified Timescape background embedding or existence theorem. The next bottleneck is not exhausted by freely choosing ν and a spatial callback.
- **Minimal correction:** Qualify compatibility as assumed pending embedding; relabel physical-trajectory evidence as manufactured algebraic compatibility; explicitly state required background coincidence, clock/rate/scale and source-transfer conditions. Before predicting physics, exhibit a nontrivial background-consistent trajectory or prove the chosen branch has no such trajectory.
- **Classification:** CURRENT_CLASSIFICATION `COMPATIBLE_IMPORTED_DYNAMICS` / “nontrivial manufactured trajectory”; RECOMMENDED_CLASSIFICATION `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION` for imported equations, `NOT_DERIVED` for their physical Timescape embedding. The naive proper-time identification is `REJECTED_UNSUPPORTED`.
- **Downstream:** No automatic invalidation of mathematical H1/boost/ADM identities. Any physical interpretation that used the rejected identification must be reworked; an eventual verified embedding may require new regional dynamics or different mapping assumptions, with human approval.

### A08 — Rank and uniqueness need constrained-data qualifications

- **Severity:** `S1_NONBLOCKING_CLARIFICATION`.
- **Phase/location:** H1 rank statements; FB/FC `CONDITIONAL_FORWARD_UNIQUENESS`; FA spectra.
- **Evidence:** Rank-31 Poisson constraint on 32-point fixture; supplied whole wall expansion history already fixes ψ after kernel normalization; eigenvectors have phase/degeneracy freedom.
- **Consequence:** Intrinsic 4/5/6 counts do not establish independently free initial-data counts, existence or canonical spectral coefficients.
- **Minimal correction:** Publish §12-style separate differential/constraint/initial-data/external-history counts; qualify uniqueness by compatibility and basis equivalence.
- **Classification:** Rank and conditional uniqueness are `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`; unconstrained physical rank or unique Timescape prediction remains `NOT_DERIVED`.
- **Downstream:** No numerical recomputation; prevents overinterpretation.

### A09 — Historical wording remains stale

- **Severity:** `S1_NONBLOCKING_CLARIFICATION`.
- **Phase/location:** README and `P/barotropic.py` module/D3 enum/matrix comments; some old project summaries.
- **Evidence:** “Unresolved” D3 wording survives while 1D-D-t adjudicates it; README's phase status predates integrated phases.
- **Consequence:** A reader can confuse intentionally preserved runtime alternatives with unresolved scientific adjudication. `background.a_w` naming also needs its dressed qualifier everywhere.
- **Minimal correction:** Update current index/docs while preserving historical reports as historical evidence; retain explicit runtime branch separation. Clarify carrier spectrum's “physical mass” wording as reference metric measure unless a physical spatial embedding is supplied.
- **Classification:** Derived D3 verdict remains conditional derivation; source/history status is a documentation matter.
- **Downstream:** None numerically.

### A10 — Exhaustive comparator/source-completeness conclusions not fully recertified

- **Severity:** `S1_NONBLOCKING_CLARIFICATION`.
- **Phase/location:** Primarily 1E-C/D/E report-only alternative-framework searches.
- **Evidence:** Source-access and inspected-scope limits in §8; earlier audit reports are not independent primary sources.
- **Consequence:** This review cannot certify universal claims that no alternative published closure could help. It can certify that the inspected frozen chain does not provide the missing closure.
- **Minimal correction:** Preserve an exact equation/page-level verification record and complete the unverified comparator checks before a publication claims exhaustive absence. This is not permission to use a comparator as a Timescape closure.
- **Classification:** A stronger universal non-derivability/no-alternative claim is `NOT_DERIVED` here.
- **Downstream:** Limits completeness of literature claims, not validity of directly checked equations.

### A11 — Core background, D3 and first-order kinematics confirmed

- **Severity:** `S0_CONFIRMED_CORRECT`.
- **Phases/location:** 1B; 1D-D-t; FB/FC scalar propagation and trace equations.
- **Evidence:** Independent tracker substitutions; primary GM and DBE conservation; direct ADM/boost/Raychaudhuri derivations; four killed mutations.
- **Consequence/correction:** No equation change warranted. Background is FTS, generic kinematic identities GR, model applications COND as individually listed in §7.
- **Downstream:** Retain accepted equations with their precise assumptions.

### A12 — Observational and generic-GR firewalls confirmed

- **Severity:** `S0_CONFIRMED_CORRECT`.
- **Phases/location:** Growth Candidate A, transfer and FA–FC exported statuses/APIs.
- **Evidence:** No spectrum-to-σ8 or RSD/tracer/survey implementation authorized; local Einstein closure not silently introduced; ν and spatial map remain explicit.
- **Consequence/correction:** Preserve withheld observational authorization. No new observational authority follows from these tests.
- **Classification:** Required physical inputs remain EXT or ND as individually listed; an unqualified identification with observational fσ8 is REJECT.
- **Downstream:** Scientific derivation may continue; fitting/inference must remain blocked.

### A13 — Finite-mode barotropic uniqueness is not continuum stability

- **Severity:** `S1_NONBLOCKING_CLARIFICATION`.
- **Phase/location:** 1C-B2 and future spectral/statistical interpretation of its modes.
- **Evidence:** The corrected tracker `c_s²` is negative. The high-k principal part of the selected barotropic system gives `Delta_eff_ddot≈-c_s² k² Delta_eff/a_D²`, with exponentially amplifying high-k solutions. Regular finite-k ODE evolution does not establish continuous dependence for unrestricted spatial data in ordinary finite-order Sobolev norms.
- **Consequence:** Do not convert the finite-mode numerical existence/uniqueness claim into a stable continuum matter theory or extend the three deterministic modes into a spectrum without an explicit validity scale/closure analysis.
- **Minimal correction:** Retain finite-mode conditional language and state the ultraviolet well-posedness/physical-domain limitation before any continuum use of the barotropic branch.
- **Classification:** Finite-mode equations remain `DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION`; a stable unrestricted continuum physical prediction is `NOT_DERIVED`.
- **Downstream:** Does not contaminate the separately selected clean H1 branch or Candidate A. No numerical correction to the audited fixed-k matrices follows.

## 16. DOWNSTREAM IMPACT ANALYSIS

| Finding / issue | Must change or re-check | Does **not** automatically require recomputation |
|---|---|---|
| A01 metric/J inconsistency | Any run whose geometry data fail the actual determinant relation; regenerate affected transfer, density, spectra and consuming boost/geometry outputs | Tracker; independent clean/barotropic solver; all verified metric-consistent realizations |
| A02 acceleration representation | Array contract, component-aware consumers, nonflat metric tests | Scalar ψ evolution, Laplacian compatibility and scalar C-driver unless they were fed through a misinterpreted vector downstream |
| A03 invalid C | Optional reconstruction domain checks and any invalid C result | Driver-only geometry/boost, background, growth |
| A04/A05 citations | Scientific source ledger, docstrings, independent tests | Core kinematic formulas or qplus numbers; current evidence favors retaining them |
| A06 tolerances | Explicit test thresholds and rerun | All scientific results absent a newly exposed error |
| A07 rejected background identification | Any claim of actual Timescape/regional/common-spacetime embedding using it | Conditional elliptic algebra and generic GR identities; they can remain useful under a different consistent realization |
| D1 historical source error | Already corrected density implementation must remain independent of misprinted expression | No current whole-chain invalidation |
| D2 historical notebook derivative | Correct derivative/sound speed for science; notebook defect only in forensic oracle | Clean comoving and Mészáros systems do not use c_s² |
| D3 printed coefficient | Derived barotropic scientific runs must retain explicit derived branch; printed branch stays forensic | Clean systems, Candidate A and clean H1 transfer are not D3 consumers |

The critical distinction is data consumption. A defect in an optional output or report citation does not retroactively invalidate unrelated numerical histories. Conversely, if a physical source/clock embedding is changed, every quantity that uses that embedding—not merely the final FC wrapper—must be revalidated.

## 17. CURRENT PHASE 1F-C VERDICT

Primary phase verdict: **TARGETED_CORRECTIONS_REQUIRED**.

The status

```text
PARTIAL_GEOMETRIC_CLOSURE_DERIVED_NEW_PERTURBED_GEOMETRIC_DYNAMICS_REQUIRED
```

is substantively correct if “partial” means conditional **local kinematic parameterization/reconstruction**, not a partially solved Timescape Einstein system. The driver status `PARTIALLY_DERIVED_REDUCED_EXTERNAL_GEOMETRIC_CLOSURE_REQUIRED` is likewise acceptable as a reduction of kinematic bookkeeping: α is conditionally anchored and acceleration/expansion relations need not be independent callbacks. It does not mean the information in the external lapse, spatial realization or compatible history has been dynamically predicted.

Actual code consumes an already solved FB result, checks clock/lapse/expansion compatibility, and optionally integrates C. It does not produce an independent metric prediction of the boost. I found no implemented scientific circular use of ψ→Θ_W→C→independent proof of ψ. Those quantities are correctly treated as mutually constrained reconstruction outputs. A future feedback use would need a new independent equation and source closure.

The lapse statement is correct: `nu_W(t,x)` is `EXTERNAL_CLOSURE_INPUT` in this frozen system. The background fixes a homogeneous clock relation, not an arbitrary spatial field. Neither `gamma_dW=1+O(v²)`, acceleration identity, Hamiltonian identity nor Raychaudhuri alone supplies ν's evolution.

There is one overstatement to avoid: these two named external inputs have not been proved to be the **only irreducible physical bottlenecks**. Regional/common background existence, matching of zeroth-order congruences, consistent source transfer and all-time effective constraints remain prerequisites. This is why A07 is a scientific classification correction rather than an arbitrary demand for more tests.

Answers to the sixteen headline questions, in order: (1) yes for the stated tracker branch; (2) no, exact citation defects exist and imported equations are not automatically Timescape; (3) no demonstrated silent runtime promotion to a predictive dressed Einstein model, but compatibility language needs qualification; (4) mostly yes, with A02/A07/A08 qualifications; (5) selected conversions correct, full physical embedding unproved; (6) first-order observer distinction retained, common background must still be established; (7) explicit spatial distinctions largely correct, A01/A02 are real gaps; (8) audited core signs/factors correct, component typing and linear-regime gating incomplete; (9) no load-bearing predictive circularity found, several constructed tests are not independent evidence; (10) intrinsic counts yes, constrained/initial-data counts not established by those counts; (11) some tests strong, others weak or construction-only; (12) yes for admissible complete closures, not arbitrary histories or Timescape uniqueness; (13) some kinematic outputs are derivable but ν/spatial/source embedding is not supplied by earlier frozen background; (14) yes, any physical embedding or unique prediction still requires new derivation/input; (15) yes as a retained conditional kinematic endpoint, not an observational launch point; (16) establish background/source/constraint compatibility, then derive geometry and observables in sequence without substituting FLRW phenomenology for missing physics.

## 18. REMAINING SCIENTIFIC BOTTLENECKS

1. **Consistent physical background and source embedding.** Specify how regional dust solutions, volume-average time, finite-infinity clocks and the local wall observer inhabit the same spacetime or are related by a justified effective construction. Verify coincidence at zeroth order where a first-order boost is used. The naive identification in §10 fails.
2. **Existence and propagation of a nontrivial compatible regional/H1 effective branch.** Solve or characterize the admissible subspace satisfying regional background/dust equations, chosen constitutive closure and R_Z/R_eff over an interval. Manufactured instantaneous jets do not establish this. Determine whether some selected closures are mutually incompatible.
3. **Geometric realization and spatial/source transfer.** Supply a justified H1-to-local-wall/dressed map, its metric and measure, simultaneity/clock mapping, and relation of sharp carrier density to GM target variables. A selected interpolation matrix alone is not that derivation.
4. **Perturbed wall congruence and gravitational dynamics.** Derive ν and spatial metric response using a physically justified source and boundary/initial prescription, or demonstrate the need for a new model input. Generic ADM constraints/Raychaudhuri can constrain a declared local Einstein model; they cannot authorize the unproved source transfer.
5. **Global dressed null propagation and observer/source mapping.** Local conformally isotropic scalar reconstruction is not yet the full perturbed W09 geometry. Need a consistent lightcone, redshift perturbations, observer tetrad and Jacobi map.
6. **Matter-to-tracer relation and observable statistics.** Initial stochastic spectrum, normalization, smoothing radius/metric, transfer of modes, tracer/velocity bias, selection and survey coordinate conventions must be independently supplied or derived before σ8/RSD/fσ8.
7. **Numerical certification of the resulting nontrivial model.** Independent analytic/continuum limits, constraint propagation, convergence and error budgets for the new equations—not merely more frozen-source regression counts.

Are ν and the spatial realization irreducible? **Relative to the frozen equations, they are missing inputs. There is no theorem here that they must remain mutually independent under every future consistent embedding.** If a verified regional-to-common metric/source construction yields local constraints fixing ν in the chosen gauge and sector, ν may cease to be external. That result would be conditional on that construction and must not be claimed solely from the tracker lapse. Conversely, prescribing ν through a phenomenological local Einstein or CMC ansatz is additional physics/sector data unless derived from the selected source/embedding.

## 19. NEXT-PHASE RECOMMENDATION — NO IMPLEMENTATION AUTHORIZED

Recommended phase: **1F-D — Regional/common-spacetime background embedding and constraint-closure feasibility audit**.

**Exact question:** Does there exist a nontrivial regional-dust/H1/common-wall realization that simultaneously preserves the accepted tracker background, the explicit clock dictionary, the common-background prerequisite for the first-order boost, the selected transfer/constitutive constraints, and the scalar-normal wall sector? If so, which metric/congruence variables are fixed by that realization and which histories remain external?

**Success requires:**

- One explicit ontology and mapping of the regional proper clocks, W09 regional volume scales, finite-infinity/dressed clocks and selected local wall scale—not equality of names.
- A background satisfying the relevant regional and averaged equations in their stated clocks, with any non-equivalent identification rejected or explicitly approved as new physics.
- An admissible nonzero perturbative trajectory or an analytical characterization of its space; all-time R_Z/R_eff and boost compatibility, not only constructed residuals.
- A justified common metric/source relation where local Einstein constraints are invoked; otherwise an explicit proof of the remaining information deficit.
- Separate differential, constraint, external-history and initial-data counts; well-posedness stated on a nondegenerate domain with all boundary/kernel choices.
- A decision whether ν can be derived after that embedding, rather than presupposing its independence or setting it to zero.

**A scientifically useful no-go result:** Demonstrate that the selected exact regional dust-FLRW clocks, H1 constitutive/transfer restrictions and tracker/common-wall conditions have no nontrivial jointly admissible solution. State which assumption causes the incompatibility. That would motivate a new branch with human approval; it would not license quietly changing the frozen equations.

**May use:** Verified tracker equations, the derived D3 branch with explicit forensic alternative retained, generic GR identities, explicit H1/FB/FC mathematical contracts and their stated additional restrictions. None is proof of a missing physical embedding.

**Would constitute new physics or a new model restriction:** A local Einstein equation for a dressed metric with regional dust inserted as its source; a surface stress tensor or Israel junction; Γ=finite infinity/material wall; a special lapse/CMC slicing presented as the physical observer; a new relation between regional and dressed scales/clocks; a chosen smoothing/morphology/effective stress transfer; nonlinear stress/anisotropy truncations justified only by convenience. Each needs an equation reference, explicit statement and human approval where it changes the model.

**Observational work remains blocked.** Background distances and generic observational definitions may be studied; no RSD/Kaiser/tracer, σ8/fσ8 prediction, survey likelihood or fit is authorized by the current chain. After the feasibility result and targeted corrections, the next path is justified geometry/congruence closure → null/source/tracer transfer → stochastic spectrum and smoothing → observable forward model → survey inference.

## 20. FINAL MACHINE-READABLE SUMMARY

`LOAD_BEARING_SCIENTIFIC_ERRORS: 0` counts established uncorrected **S4/S5** equation/model failures in the accepted conditional chain. It does not mean no defects were found, no invalid inputs can be accepted, or a physical Timescape embedding has been proved.

```yaml
AUDITED_COMMIT: 63d2104575c6a249e5177e47f4a354b660e70e32
GLOBAL_PROJECT_VERDICT: ACCEPT_WITH_TARGETED_CORRECTIONS
EARLIEST_CONFIRMED_PHASE: 1B_TRACKER_BACKGROUND
LATEST_CONFIRMED_PHASE: 1F-C_CONDITIONAL_KINEMATIC_CORE_ONLY
D3_VERDICT: RESOLVED_DERIVED_4_10
BACKGROUND_SECTOR: ACCEPT_STATED_DUST_ZERO_LAMBDA_TRACKER_BRANCH
REGIONAL_PERTURBATIONS: CONDITIONAL_IMPORTED_DUST_FLRW_TIMESCAPE_EMBEDDING_NOT_DERIVED
H1_REALIZATION: CONDITIONAL_VALID_MATHEMATICS_METRIC_MEASURE_CORRECTION_REQUIRED
DUST_TO_WALL_BOOST: CONDITIONAL_SCALAR_DYNAMICS_CORE_CONFIRMED
WALL_COMMON_GEOMETRY: CONDITIONAL_LOCAL_KINEMATICS_TARGETED_CORRECTIONS_REQUIRED
CLOCK_CONSISTENCY: SELECTED_CHAIN_RULES_CONFIRMED_PHYSICAL_BACKGROUND_EMBEDDING_UNPROVED
FRAME_CONSISTENCY: FIRST_ORDER_DISTINCTIONS_CONFIRMED_BACKGROUND_COINCIDENCE_UNPROVED
SPATIAL_OPERATOR_CONSISTENCY: SCALAR_SCALING_CONFIRMED_MEASURE_AND_COMPONENT_CONTRACT_CORRECTIONS_REQUIRED
STATE_RANK_CONSISTENCY: INTRINSIC_4_5_AND_OPTIONAL_6_CONFIRMED_NOT_FREE_INITIAL_DATA_COUNTS
HIDDEN_CIRCULARITY_FOUND: NO
LOAD_BEARING_SCIENTIFIC_ERRORS: 0
TARGETED_CORRECTIONS: 7
S2_CORRECTIONS: 6
S3_CLASSIFICATION_CORRECTIONS: 1
UNRESOLVED_EXTERNAL_CLOSURES:
  - REGIONAL_COMMON_BACKGROUND_AND_SOURCE_EMBEDDING
  - ALL_TIME_TRANSFER_CONSTITUTIVE_COMPATIBILITY
  - H1_TO_WALL_DRESSED_SPATIAL_REALIZATION_AND_DENSITY_CODOMAIN_MAP
  - PERTURBATIVE_WALL_LAPSE_NU_W
  - LOCAL_SCALE_HUBBLE_MAPPING_AND_PERTURBED_GEOMETRIC_DYNAMICS
  - INITIAL_BOUNDARY_KERNEL_AND_MORPHOLOGY_DATA
  - GLOBAL_LIGHTCONE_TRACER_STATISTICAL_AND_SURVEY_INPUTS
UNIQUE_TIMESCAPE_PREDICTION: NOT_DERIVED
OBSERVATIONAL_AUTHORIZATION: NOT_GRANTED
RSD_AUTHORIZATION: NOT_GRANTED
SIGMA8_AUTHORIZATION: NOT_GRANTED
FSIGMA8_AUTHORIZATION: NOT_GRANTED
RECOMMENDED_NEXT_PHASE: 1F-D_BACKGROUND_EMBEDDING_AND_CONSTRAINT_CLOSURE_FEASIBILITY_AUDIT
READY_TO_CONTINUE_PROJECT: YES_FOR_TARGETED_CORRECTIONS_AND_SCIENTIFIC_FEASIBILITY_ONLY_NO_OBSERVATIONAL_DEVELOPMENT
REPOSITORY_MODIFIED: NO
SOURCE_COVERAGE: CRITICAL_EQUATIONS_CHECKED_NOT_ALL_HISTORICAL_COMPARATOR_CLAIMS_RECERTIFIED
```
