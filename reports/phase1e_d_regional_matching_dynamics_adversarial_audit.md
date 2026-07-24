# Independent adversarial audit — Phase 1E-D regional matching dynamics

## 1. Audit verdict

**Audit verdict: `REQUIRES_TARGETED_CORRECTIONS`.**

The report's most important negative conclusion survives: the present
regional-to-GM construction is not closed and is not implementation-ready. The
intrinsic \(k\ne0\) scalar dust sector also survives as a rank-two system per
exact regional FLRW background. The effective-source algebra, two-region
backreaction identity, three-mismatch propagation equations, and the decision
not to assert inverse uniqueness or nonuniqueness are correct under their
stated branches.

The deliverables are not safe to accept unchanged. Two ApJ DOI records are
wrong. The metric count \(6-2-2=2\) is not a valid independent phase-space
derivation. More importantly, the carried-forward
\(N_{\rm undef}=0\) entry conflicts with both the frozen definition of that
component and the report's own finding that a new common carrier and regional
embeddings are absent. The transfer expression \(T_r=L_DP_rG_r\) is only a
specification pattern, not yet a mathematical operator. The smooth and sharp
partition branches and the four elliptic branches are not instantiated.

Core A1–A27 classifications:

| Classification | Count |
|---|---:|
| `PASS` | 11 |
| `PASS_WITH_EXPLICIT_CONDITIONS` | 9 |
| `PARTIAL` | 6 |
| `UNSUPPORTED` | 1 |
| `INCORRECT` | 0 |

Two additional cross-cutting findings are classified
`SOURCE_MISREPRESENTED` and `INCORRECT`, respectively. Thus, over all 29
classified findings, the requested counts remain 11 pass, 9 conditional, 6
partial, 1 unsupported, and 1 incorrect, plus 1 source-misrepresentation
finding.

## 2. Scope and independence statement

This was a hostile, read-only scientific audit of:

- `reports/phase1e_d_regional_matching_dynamics_closure.md`;
- `reports/phase1e_d_regional_matching_dynamics_inventory.json`.

Neither deliverable was treated as an authority. The primary PDFs were
downloaded or re-opened in external scratch, their relevant pages and equations
were reread, and load-bearing equations were rederived independently. The
image-only DBE92 and BDE92 scans were rendered and visually inspected.
Symbolic and synthetic checks were written independently of the report's
symbolic ledger. The completion verdict, counts, deficit vector, transfer
construction, and inverse conclusion were all challenged.

The sole repository output of this audit is this file. All PDFs, rendered
pages, extracted text, temporary Python packages, frozen-tree copies, and
synthetic calculations remained under the external directory
`C:\Users\Claudio\AppData\Local\Temp\timescape-phase1ed-adversarial-audit`
or in the pre-existing historical external validation reproduction directory.
No upstream source was copied into this report.

## 3. Repository preservation audit

### 3.1 Pre-audit checkpoint

Direct pre-audit results were:

| Check | Result | Classification |
|---|---|---|
| branch | `phase-1e-d-regional-matching-dynamics-design` | `PASS` |
| `HEAD` | `fcbf9c29a28c586044150e6910e1637bc3f6975b` | `PASS` |
| Phase 1E-C tag | tag object `0a6dbe6ac27991d6119a4ebc4e84e4a005f3d988`, peeled to `fcbf9c29a28c586044150e6910e1637bc3f6975b` | `PASS` |
| Phase 1E-C ancestry | frozen tag is an ancestor of `HEAD` | `PASS` |
| Phase 1E-D commits/tags | none; only the work branch points at frozen `HEAD` | `PASS` |
| `main` | `8634f14a35c22983413672075fa7f37f03fd663d` | `PASS` |
| `origin/main` | `8634f14a35c22983413672075fa7f37f03fd663d` | `PASS` |
| tracked work tree | no tracked modification | `PASS` |
| index | empty; `git diff --cached --check` empty | `PASS` |
| unstaged diff check | `git diff --check` empty | `PASS` |
| pre-audit untracked files | exactly the two Phase 1E-D deliverables | `PASS` |
| upstream clone | clean, detached at `590c6fd5332acb15f5683ebf392a0d7ce54983c5` | `PASS` |
| pinned notebook | SHA-256 `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a` | `PASS` |

The audited report hashes were:

- closure Markdown:
  `d6cbfc2bb4795f1b7340dd6dcf58ea1dc4716242b33beaa261b4e568175f346b`;
- inventory JSON:
  `32bc56c57eee50513707b2fedfba366bb00b24b13962e5a466cebc5d875652f1`.

The JSON parsed under Python 3.14.3. It contains 14 records at
`candidate_framework_matrix`, 35 records at `variable_ontology`, and 15
objects at `formal_conclusions`. Every formal conclusion has exactly these
nine fields:
`assumptions`, `classification`, `coordinate_dependencies`,
`derivation_summary`, `evidence_needed_to_change_status`,
`frame_dependencies`, `implementation_consequence`,
`observational_consequence`, and `source`.

### 3.2 Ignored-artifact discrepancy

The actual unit behind “29” is now independently resolved.

1. A frozen `HEAD` tree with the ignored artifacts absent produced
   `350 passed, 29 skipped` under Python 3.14.3.
2. Ten files, not 29 files, are required to restore all 379 tests.
3. The eight-path list in the completion response is incomplete. It omitted:
   `artifacts/independent/phase1c_b2_convergence.json` and
   `artifacts/independent/phase1c_b2_d2_d3_factorial.json`.
4. All ten current files are ignored and untracked.
5. All ten were regenerated in external frozen copies using the repository's
   existing procedures. Their SHA-256 hashes were byte-identical to the
   current ignored files:

| Ignored path | SHA-256 |
|---|---|
| `artifacts/independent/phase1c_b2_convergence.json` | `e3d2c0ffea9da9b3a43020c40742ce42d83bc57c90d5e6c28aaf8dda6a2b1f6e` |
| `artifacts/independent/phase1c_b2_d2_d3_factorial.json` | `f1365b551d0c305ace7022a37d2017529abc3960ca7bbe0b072e25140c199f36` |
| `artifacts/independent/phase1c_b2_figure_endpoints.json` | `b22d445b857ae0aa322d4d98cf44e607f0599e6d3d4ef20d0974da5f2ac61bab` |
| `artifacts/independent/phase1c_b2_oracle_comparison.json` | `30ee5fc2842303d47bc2c12e03ed5e5b27fe77db35fec8fa233872cf64281e0a` |
| `artifacts/independent/phase1c_b2_scenario_effects.json` | `1be0870727023015580bd320db2ea4f37668ac0fda98261b616ef84b2118655b` |
| `artifacts/independent/phase1d_b_growth_validation.json` | `e505c90280a9113aaf9dac20387372ebb3f0a0bfed9fd8f35e1cb04113d4ae43` |
| `artifacts/independent/phase1d_d_anchored_density_growth_validation.json` | `15d43d1bc2f14841db8af8bbe1ed714b64d1a6176457f2109838da38c1f4b3cc` |
| `artifacts/upstream/oracle_background.json` | `129e3e45842c05997bfff7250de552acb283bc6f7a69add2a02c3f22f9e1c4b4` |
| `artifacts/upstream/oracle_barotropic_perturbations.json` | `0339afd4eedbed79b808d0d33bc7fbd1bbf45b80506faa377c9223aeb15fe5ab` |
| `artifacts/upstream/oracle_clean_perturbations.json` | `c32ce165c31e3a00284ff76f0749c063feb38bfd0348a53c706b18a5d55f6eda` |

The historical anchored validator was rerun at its recorded branch
`phase-1d-d-anchored-density-growth`, commit
`7ea266c2cb00aac8afdef71e51a18aea5fb7d39c`, and recorded Python
environments. It reproduced the final hash exactly. No generator changed a
tracked file in the audited tree; the tracked status remained empty.

The historical statement “ten absent files caused 29 skips” is reconstructed
rather than observed before the authors' regeneration. The frozen absent-file
test, skip reasons, current ten-file inventory, byte-identical regeneration,
and common creation interval make that reconstruction decisive. A1 is
therefore conditional only on this unavoidable historical-state qualification.

### 3.3 Test baseline

Using `PYTHONPATH=<external-dependencies>;$PWD\src`,
`PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`, and external
`--basetemp` directories:

- Python 3.14.3: `379 passed in 15.01s`;
- Python 3.11.9: `379 passed in 19.24s`.

The different durations from the completion report are not failures. Running
collect-only under Python 3.14.3 without `PYTHONPATH=src` failed in
`tests/conftest.py` with
`ModuleNotFoundError: No module named 'timescape_fsigma8'`. This independently
confirms an invocation-path error before collection, not a scientific or test
failure.

## 4. Primary-source reinspection

The source distinction in the final column uses the required phrases
literally.

| Source and exact load-bearing location | Independent result | Source distinction |
|---|---|---|
| Galoppo & Mourier (GM), arXiv:2511.17160v2, Eqs. (2.2), (2.13), (2.20)–(2.24), (3.12)–(3.13), (4.12), (4.20)–(4.23), and printed p. 22 | CGI normalizations, Hamiltonian constraint, effective fluid, clean-comoving equations, and the only matching-domain paragraph were reread. | equation directly verified |
| Wiltshire 2007, arXiv:0709.0732v2, Eqs. (1)–(8), (19)–(22) | Regional wall/void background metrics, volume fractions, regional times, and lapse structure are present; no perturbed three-dimensional pullback is supplied. | equation directly verified |
| Wiltshire 2008, arXiv:0809.1183v2, Eqs. (10)–(14), (19)–(27) | Finite-infinity and cosmological-equivalence-principle structure is background ontology, not the GM matching-domain construction. | equation directly verified |
| Wiltshire 2009, arXiv:0909.0749v2, Eqs. (6), (22)–(28), (36)–(38), (51) | The dressed geometry is obtained through spherically averaged radial-null matching. It does not define a three-dimensional spatial carrier. | equation directly verified |
| Buchert 2000, arXiv:gr-qc/9906015v2, Eqs. (9), (10a)–(10c), (13a) | Dust averaging, \(Q_D\), and the averaged Raychaudhuri identity were checked. | equation directly verified |
| Buchert 2001, arXiv:gr-qc/0102049v2, Eqs. (7)–(12g) | General-fluid averaged equations do not provide the selected regional localization or transfer. | claim not actually supported |
| Buchert & Carfora 2002, arXiv:gr-qc/0210037v2, Eqs. (6)–(7), (15), (34), (46), (52), printed pp. 15–24 and Sec. 3 | Regional averaging uses geodesic balls and a declared scale; smoothing changes the geometry and averages. It is not neutral. | equation directly verified |
| Buchert & Carfora 2002, arXiv:gr-qc/0210045v1, Eqs. (1)–(7) | Dressing relates smoothed and bare regional parameters, but supplies no wall/void perturbation-transfer map. | equation directly verified |
| Roy & Buchert 2012, arXiv:1202.5766v2, Eqs. (4)–(10) | Exact deviations are defined inside an averaged dust domain. Applying them as a wall/void-to-GM map would be an extra assumption. | interpretation inferred |
| Buchert, Mourier & Roy 2020, arXiv:1912.04213v2, Eqs. (2.2)–(2.3), (2.7), (2.10), (3.9), (3.19), (3.23)–(3.24), and (B.2)–(B.5) | Lapse, shift, coordinate velocity, tilt, Lorentz factor, proper expansion, and volume rate are distinct. | equation directly verified |
| Mourier & Heinesen 2024, arXiv:2401.09170v2, Eqs. (2.1)–(3.31) | Foliation and threading choices affect averaging and transport; using its general language for Timescape requires a declared specialization. | applicability assumption |
| Dunsby, Bruni & Ellis 1992, *ApJ* 395, 54–74, Eqs. (15), (18)–(21), (25)–(55) | Multifluid CGI equations and frame variables were visually checked. Correct DOI: `10.1086/171630`. | equation directly verified |
| Bruni, Dunsby & Ellis 1992, *ApJ* 395, 34–53, Eqs. (14)–(16), (24)–(29), (40), (44)–(48), (61), (63), (68)–(74), (119)–(120), and Appendix B | Scalar constraints, curvature, shear/Weyl reconstruction, and constant-curvature harmonics were visually checked. Correct DOI: `10.1086/171629`. | equation directly verified |
| Mars, Mena & Vera, “Linear perturbations of matched spacetimes: the gauge problem and background symmetries,” arXiv:0704.0078v1, *Class. Quantum Grav.* 24 (2007) 3673–3689, DOI `10.1088/0264-9381/24/14/008`, Eqs. (1)–(4) and Sec. 2 | Perturbed first/second fundamental forms require independent spacetime and hypersurface gauge/deformation data. | equation directly verified |
| Ulrich Kirchner, “A new approach to spherically symmetric junction surfaces and the matching of FLRW regions,” arXiv:gr-qc/0312003, *Class. Quantum Grav.* 21 (2004) 3845–3869, DOI `10.1088/0264-9381/21/16/002`, Eqs. (51)–(55), Secs. 5.1, 5.3, 5.5 | The no-go used by the report is bounded to spherical, timelike, comoving, exact-FLRW junctions and \(\gamma\)-law fluids. | equation directly verified |
| Brown & Olver 2012, arXiv:1203.6263v2, junction-condition sections | Thin-shell and junction data do not provide the selected averaging transfer. | claim not actually supported |
| Khakshournia & Wiltshire 2006, arXiv:gr-qc/0602051v3, matching sections | Swiss-cheese matching is a comparator, not a derivation of the selected branch. | applicability assumption |
| Balasin 2013, arXiv:1310.3124v1, Eqs. (3)–(11) | Provides a possible realization/comparator, not the missing perturbative carrier. | applicability assumption |
| Nazer & Wiltshire 2015, arXiv:1410.3470v3, Secs. II–III, Eqs. (3)–(7) | Auxiliary-FLRW CMB matching is not a regional interface or late-time regional transfer. | equation directly verified |

The two DOI errors occur in closure report §7, lines 135–136, and JSON paths
`primary_source_inventory[13].citation` and
`primary_source_inventory[14].citation`. The scans and article titles are the
intended papers, so this is bibliographic source misrepresentation rather than
use of the wrong scientific paper.

## 5. Claim-by-claim audit table

| ID | Classification | Independent result | Exact report / JSON location |
|---|---|---|---|
| A1 | `PASS_WITH_EXPLICIT_CONDITIONS` | Frozen checkpoint, two pre-audit untracked deliverables, empty index, clean tracked tree/upstream, hashes, tests, and ten-artifact regeneration verified. Historical “before” count is necessarily reconstructed. | report §§2–4, 37; JSON `repository_checkpoint` |
| A2 | `PASS` | GM says only “zero volume measure,” formally “as a boundary,” “within a single spacetime,” and “ultimately unspecified.” The report does not promote it to zero spacetime measure, a regular hypersurface, finite infinity, or a partition boundary with matching data. | report §8; JSON `domain_type_gate`, `formal_conclusions["H-D0"]` |
| A3 | `PASS` | Kirchner's result is kept bounded to spherical, timelike, comoving exact FLRW \(\gamma\)-law junctions and is not universalized. | report §§10–11; JSON `background_matching_gate`, `formal_conclusions["H-D1"]` |
| A4 | `PARTIAL` | Most roles are correctly separated, but the selected smoothing/carrier construction is not merely a neutral compatible import. A concrete \(S_\ell,\phi_r,\Sigma_D\) branch introduces physical embedding and smoothing choices absent from current Timescape. FW-02 also uses “current Timescape” in the broader GM-target sense, not W07–W09 regional machinery. | report §9 and §§22–23; JSON `candidate_framework_matrix[1]`, `[6]`, `[12]` |
| A5 | `PARTIAL` | The CGI dust state \((\Delta_r,Z_r)\) is sufficient for the intrinsic scalar \(k\ne0\) sector, including curved FLRW backgrounds, after clock and elliptic branches are fixed. The separate metric formula \(6-2-2=2\) mixes field functions, constraints, gauge removal, and phase-space functions and is not an independent proof. | report §§13–15; JSON `regional_state_inventory`, `equation_counting.formulations[0:2]`, `formal_conclusions["H-D3"]` |
| A6 | `PASS` | The report distinguishes the globally inapplicable Timescape Mészáros approximation from exact regional dust CGI dynamics. Coincident operators do not imply coincident ontology. | report §§13, 33; JSON `equation_inventory` |
| A7 | `PASS_WITH_EXPLICIT_CONDITIONS` | Laplacian CGI scalars remove homogeneous modes, but the full elliptic kernel depends on topology/BC and may exceed the naive constant mode in the proposed inverse problem. The report records this condition. | report §15 and §23; JSON `gauge_inventory`, `formal_conclusions["H-D4"]` |
| A8 | `PASS` | \(\dot f_v=f_vf_w(\Xi_v-\Xi_w)\) follows exactly from two volumes. BMR shows \(\Xi_r\) is not generally \(\Theta_r\): lapse, shift, tilt, and \(\dot\gamma\) enter. The report does not conflate them. | report §§16–17; JSON `partition_dynamics`, `formal_conclusions["H-D5"]` |
| A9 | `PASS_WITH_EXPLICIT_CONDITIONS` | \(F_v=L_D\delta f_v\) and its displayed evolution are algebraically correct only after a carrier, time transport, and localization map exist. The report states the commutator and missing expansion transfer rather than claiming closure. | report §17; JSON `partition_dynamics` |
| A10 | `PASS` | Effective density and pressure normalizations, including factors 3, 16, 48, and enthalpy-to-density conversion for \(\widetilde P\), are correct. | report §19; JSON `effective_geometry`, `formal_conclusions["H-D6"]` |
| A11 | `PASS_WITH_EXPLICIT_CONDITIONS` | \(\widehat{\widetilde P}_{\rm eff}=0\iff\mathscr W=3\mathscr Q\) for \(\bar Q_D+\bar W_D\ne0\) and non-kernel scalar modes. It follows from the selected all-time dust-comoving effective-fluid branch plus GM Euler Eq. (4.12); it is not a Buchert identity or propagated initial constraint. | report §20; JSON `effective_geometry.clean_comoving_closure`, `formal_conclusions["H-D6"]` |
| A12 | `PASS` | The two-region \(Q_D\) decomposition and first variation are correct. For perturbations of exact regional FLRW backgrounds, internal \(\delta Q_r\) is second order because variance and shear enter quadratically. Residuals correctly retain non-FLRW/map corrections. | report §18; JSON `effective_geometry`, `formal_conclusions["H-D7"]` |
| A13 | `PASS` | \(a_r^2D_r^2\delta{}^{(3)}R_r=-(4/3)\Theta_rZ_r+16\pi G\rho_r\Delta_r\) follows from GM Eq. (2.13) with the report's curvature convention. | report §§13–14; JSON `equation_inventory` |
| A14 | `PASS_WITH_EXPLICIT_CONDITIONS` | The report does not claim present five-state closure. Rank five is explicitly conditional on supplying expansion transfer, map residuals, commutator behavior, carrier, and constitutive branch. Current rank is correctly not countable without branch selection and \(\Delta_{\rm dyn}\ge1\). | report §§18, 28, 32; JSON `equation_counting.formulations[3:5]`, `formal_conclusions["H-D7"]` |
| A15 | `PASS_WITH_EXPLICIT_CONDITIONS` | All three mismatch equations and the \(+C_P/4\) coefficient are correct. \(C_{\rm eff}\) is an independent GM state mismatch on the generic nondegenerate branch; a concrete transfer could restrict the admissible mismatch subspace, so “three-dimensional” is not yet a proved matching-constraint rank. \(C_P=0\) is correctly an enforced closure. | report §21; JSON `constraint_propagation`, `formal_conclusions["H-D8"]` |
| A16 | `PARTIAL` | A carrier is a finite GR parametrization, but its existence and sufficiency are not derived. Calling it absent is correct; retaining \(N_{\rm undef}=0\) is not. | report §22 and §32; JSON `common_carrier`, `deficit_vector` |
| A17 | `UNSUPPORTED` | \(L_DP_rG_r\) is not yet an operator: no fixed domain/codomain, topology, trace class, boundary realization, boundedness, or time transport is supplied. It is acceptable only as a candidate definition pattern. | report §23; JSON `transfer_operator`, `formal_conclusions["H-D9"]` |
| A18 | `PARTIAL` | Scale dependence is acknowledged, but no smooth kernel, scale range, partition-of-unity proof, idempotence analysis, or explicit sharp-interface \(D\chi_r,D^2\chi_r\) distributional calculation is present. | report §§23, 26, 29; JSON `transfer_operator`, `limit_tests` |
| A19 | `PASS` | The report makes only the justified generic non-diagonality claim and expressly allows engineered diagonal, equal-region, single-region, degeneracy-mixing, and WKB branches. | report §24; JSON `spectral_kernel`, `formal_conclusions["H-D10"]` |
| A20 | `PASS_WITH_EXPLICIT_CONDITIONS` | \(R_T=\dot T+TA_R-A_{\rm GM}T\) is necessary and sufficient on a common differentiable invariant domain and for the full admissible state space. A moving Hilbert/domain family requires an additional trivialization or connection, still absent. The no-target-fitting rule is enforced. | report §25; JSON `transfer_operator.temporal_intertwining`, `formal_conclusions["H-D11"]` |
| A21 | `PASS_WITH_EXPLICIT_CONDITIONS` | Five dynamic initial functions are correct only for the conditional branch. Maps, kernels, clocks, elliptic realizations, and boundary data remain external matching/model functions and do not disappear from the current count. The report correctly makes the current count non-countable before branch selection. | report §§27–28, 31; JSON `initial_data`, `equation_counting` |
| A22 | `PASS` | For nonzero effective background density, \(\Delta_{\rm eff}(t_i)=0\) gives \(\mathscr Q_i+\mathscr W_i=0\), and \(C_P=0\) gives \(\mathscr W_i-3\mathscr Q_i=0\), hence both vanish. At zero effective density the normalized statement is undefined, as the report says. | report §§19, 27, 29; JSON `initial_data`, `limit_tests` |
| A23 | `PASS` | The report correctly leaves both uniqueness and nonuniqueness unresolved until \(T:X_{\rm adm}\to Y\) and its kernel are specified. The finite \(5\to3\) analogy is explicitly illustrative only. | report §27; JSON `inverse_problem`, `formal_conclusions["H-D13"]` |
| A24 | `PARTIAL` | The report lists relevant elliptic requirements but does not instantiate or prove existence/uniqueness for compact-boundaryless, noncompact-decay, finite-patch, or sharp-interface branches. | report §26 and §31; JSON `elliptic_data`, `boundary_data` |
| A25 | `PASS_WITH_EXPLICIT_CONDITIONS` | No displayed main formula divides by \(H_v-H_w\); the equal-expansion and endpoint limits of the kinematic identities are regular. Normalized effective variables fail when \(\bar Q_D+\bar W_D=0\), and the report declares an unnormalized branch. The remaining transfer limits are gates, not completed tests. | report §29; JSON `limit_tests` |
| A26 | `PARTIAL` | Every listed failure has a stated consequence, so the gates are real. The statement that every gate is executable before a prototype is false while carrier/operator/function spaces are absent. | report §§30–31, especially line 805; JSON `falsification_tests` |
| A27 | `PASS` | Searches found only explicit prohibitions or out-of-scope records for peculiar/tracer velocity, dressed/survey wavenumber, \(\sigma_8\), \(f\sigma_8\), RSD, and likelihood readiness. | report §§2, 12, 33; JSON `frozen_result_boundary.immutable_distinctions`, `implementation_readiness.forbidden` |
| X1 | `SOURCE_MISREPRESENTED` | DBE92 and BDE92 DOI identifiers are each one article low. Correct values are `10.1086/171630` and `10.1086/171629`. | report §7 lines 135–136; JSON `primary_source_inventory[13].citation`, `[14].citation` |
| X2 | `INCORRECT` | The exact deficit \((0,\ge1,\ge1,\ge1,\ge2,\mathrm{N/A})\) does not survive. The selected branch requires a new common carrier and embeddings absent from current theory. Under the frozen Phase 1E-C rule, “an indispensable object requiring a new embedding” is precisely an \(N_{\rm undef}\) failure or bifurcation; generic GR parameterizability does not make it zero. | report §32; JSON `frozen_result_boundary.deficit_lower_bound.N_undef`, `deficit_vector.frozen_lower_bound.N_undef`, `deficit_vector.refinement.N_undef` |

## 6. Equation and sign audit

### 6.1 Regional scalar dust equations

Setting \(w=P=F=V=0\) in GM Eqs. (2.22)–(2.23) gives, in regional
proper time,

\[
\dot\Delta_r=-Z_r,\qquad
\dot Z_r=-\frac23\Theta_rZ_r-4\pi G\rho_r\Delta_r.
\]

Since \(\Theta_r=3H_r\),

\[
\dot Z_r=-2H_rZ_r-4\pi G\rho_r\Delta_r,\qquad
\ddot\Delta_r+2H_r\dot\Delta_r-4\pi G\rho_r\Delta_r=0.
\]

The signs and coefficients in report §13 are correct. Spatial curvature affects
the regional background \(H_r,\rho_r\), the Hamiltonian reconstruction, and the
harmonic spectrum; pressureless scalar propagation adds no independent
curvature state. The conclusion is limited to exact, irrotational, geodesic
dust FLRW regional backgrounds and \(k\ne0\). It does not close the common-time
transfer.

The perturbed Hamiltonian relation follows from GM Eq. (2.13):

\[
a_r^2D_r^2\delta{}^{(3)}R_r
=-\frac43\Theta_rZ_r+16\pi G\rho_r\Delta_r.
\]

No missing \(a_r^2\), sign, or density factor was found.

### 6.2 Two-region averaged Raychaudhuri identity

Let \(f=f_v\), \(f_w=1-f\),
\(\Theta=f_w\Theta_w+f\Theta_v\), and
\(\dot f=f(1-f)(\Theta_v-\Theta_w)\) on the common proper-time dust
specialization. Substitute each regional averaged Raychaudhuri equation into
\(\dot\Theta\), and define

\[
Q_D=f_wQ_w+fQ_v+\frac23f(1-f)(\Theta_v-\Theta_w)^2.
\]

Independent SymPy expansion produced the exact residual

\[
\dot\Theta+\frac13\Theta^2+4\pi G\rho_D-\Lambda-Q_D=0.
\]

The symbolic residual was identically zero, not numerically small. This checks
the variance coefficient \(2/3\), the sign of \(\dot f\), and the absence of
double counting. The first variation in report §18 is also correct.

### 6.3 Effective-source normalization

From GM Eqs. (3.12)–(3.13),

\[
\rho_{\rm eff}=-\frac{\bar Q_D+\bar W_D}{16\pi G},\qquad
p_{\rm eff}=-\frac{\bar Q_D}{16\pi G}
 +\frac{\bar W_D}{48\pi G}.
\]

For \(\mathscr Q=L_D\delta Q_D\) and
\(\mathscr W=L_D\delta W_D\), GM Eq. (2.20) gives

\[
\widehat\Delta_{\rm eff}
=\frac{\mathscr Q+\mathscr W}{\bar Q_D+\bar W_D},
\]

and because GM defines \(P=a^2D^2p/(\rho+p)\) while
\(\widetilde P=(1+w)P=a^2D^2p/\rho\),

\[
\widehat{\widetilde P}_{\rm eff}
=\frac{3\mathscr Q-\mathscr W}
 {3(\bar Q_D+\bar W_D)}.
\]

Independent symbolic simplification reproduced both expressions and

\[
12\pi G\rho_{\rm eff}\widehat{\widetilde P}_{\rm eff}
=\frac{\mathscr W-3\mathscr Q}{4}.
\]

All factors 3, 16, and 48 and the pressure sign are correct.

### 6.4 Partition and backreaction equations

Direct differentiation of
\(f_v=V_v/(V_v+V_w)\) gives

\[
\dot f_v=f_vf_w(\Xi_v-\Xi_w).
\]

Its first variation and the report's \(F_v\) equation have correct product-rule
coefficients and commutator sign. This is purely a common-time volume identity.
BMR Eqs. (3.19), (3.23), and (B.2) show

\[
-NK+(Nv^i)_{\|i}
=\frac N\gamma\Theta-\frac1\gamma\frac{d\gamma}{dt},
\]

so \(\Xi_r=\Theta_r\) is not valid without the corresponding lapse, tilt,
shift, domain, and clock specialization.

### 6.5 Three-mismatch propagation

With the report's target-minus-reconstruction definitions, direct subtraction
of GM Eqs. (4.21)–(4.23) gives

\[
\dot C_\Delta=-C_Z-R_\Delta,
\]

\[
\dot C_{\rm eff}
=w\Theta C_{\rm eff}-(1+w)C_Z-R_{\rm eff},
\]

\[
\dot C_Z=-\frac23\Theta C_Z-4\pi G\rho_dC_\Delta
-4\pi G\rho_{\rm eff}C_{\rm eff}
+\frac14C_P-R_Z.
\]

An independent symbolic check recovered every sign and coefficient. On the
generic GM clean system there is no algebraic equation eliminating
\(C_{\rm eff}\), so its evolution is genuinely independent of the earlier
two-mismatch proposal. Degenerate zero-effective-density and restricted-image
branches must be counted separately. \(C_P=0\) is an all-time constitutive
condition, not a propagated constraint.

### 6.6 Required synthetic tests

The required adversarial tests gave:

| Test | Independent result |
|---|---|
| finite \(3\times5\) transfer | rank 3 and nullity 2, as rank-nullity requires for that truncation |
| infinite-dimensional counterexample | coefficient interleaving gives an injective map between separable five-field and three-field sequence Hilbert spaces; component count alone proves no functional kernel |
| diagonal-transfer counterexample | for diagonal \(A_R,A_{\rm GM}\), \(T_{ii}(t)=\exp[(a_{{\rm GM},i}-a_{R,i})t]\) gives \(R_T=0\) diagonally without an isometry or common eigenvalue spectrum |
| \(H_v-H_w\to0\) | the linear partition equation tends to \(f_vf_w(\delta\Xi_v-\delta\Xi_w)\); denominator is 1 |
| zero effective density | normalized \(\Delta_{\rm eff}\) diverges/is undefined for generic nonzero numerator; unnormalized \(\delta\rho_{\rm eff}\) remains finite |
| smoothing dependence | on a periodic Fourier mode, Gaussian smoothing multiplies by \(\exp(-\ell^2k^2/2)\); its \(\ell\)-derivative is nonzero for \(\ell k\ne0\) |
| \(R_T\) full-basis test | an exact diagonal intertwiner gave zero residual on both basis vectors; a trajectory-fitted map gave zero on the selected first vector but residual \(-3e_2\) on the independent second vector |
| GM domain text search | one load-bearing paragraph; “zero volume measure,” “boundary,” “single spacetime,” and “ultimately unspecified”; no zero-spacetime-measure, regular-hypersurface, normal, induced metric, or extrinsic-curvature statement |

Synthetic examples are falsification tools only and are not Timescape
predictions.

## 7. Ontology audit

GM printed p. 22 supplies less structure than the word “boundary” may suggest:

- **zero spatial-volume measure:** supported in the averaging context;
- **zero spacetime measure:** not stated;
- **partition boundary:** not constructed;
- **regular hypersurface:** not stated;
- **matching domain:** named formally;
- **finite infinity:** not identified;
- **eventwise comparison arena:** not constructed;
- **single-spacetime construction:** asserted as motivation, not supplied as a
  manifold/gluing construction.

Report §8 correctly preserves these distinctions. Later sections do not
silently attach a normal or junction data to the GM domain. They instead
introduce \(\Sigma_D,\phi_r,\omega_r\) as missing candidate data. That honesty,
however, makes the exact \(N_{\rm undef}=0\) claim untenable under the frozen
rule: a generic name for a new embedding is not an existing Timescape
embedding.

W09 finite infinity is an operational wall-boundary/background concept and its
dressed radial geometry is not the GM object. MMV's matching hypersurface is a
regular non-null surface with deformation data and first/second fundamental
forms; adopting it would select C-JUNC or C-SHELL. These three notions remain
distinct.

## 8. Framework-classification audit

The regional CGI import, perturbed matching, junction, shell, deviation,
general-fluid averaging, and auxiliary-FLRW roles are mostly classified
correctly.

Two labels need qualification:

1. `candidate_framework_matrix[1]` calls covariant \(1+3\) perturbations
   `CURRENT_TIMESCAPE_MACHINERY`. They are current in the selected GM target
   formalism, but not a regional perturbation-and-transfer construction in
   W07–W09. The record must say which meaning of “current” it uses.
2. A concrete \((\Sigma_D,\phi_r,S_\ell)\) branch is not licensed merely by
   classifying Buchert-Carfora as `COMPATIBLE_IMPORTED_DYNAMICS`. The source
   establishes that scale, region, topology, and smoothing flow matter. A
   selected smoothing kernel/scale and embedding are
   `OPTIONAL_MODEL_EXTENSION` until derived for Timescape.

The report does not actually smuggle these choices into an implementation; its
conditionality is preserved. The problem is classification precision, not a
hidden numerical model change.

## 9. State and equation-counting audit

The independent ledger is:

| Branch | Raw dynamic variables | Definitions / algebraic constraints | Differential constraints / gauge | Evolution equations | Closures | Initial functions | Boundary / matching / elliptic / inverse data | Supported rank |
|---|---|---|---|---|---|---|---|---|
| one regional CGI dust, \(k\ne0\) | \(\Delta_r,Z_r\) | CGI definitions; Hamiltonian/shear/Weyl reconstruction | dust-comoving CGI frame; elliptic kernel excluded | two first-order equations | dust EOS | 2 | topology/spectrum/BC fixed externally | `EXACT` rank 2 |
| two independent regional CGI sectors | \(\Delta_w,Z_w,\Delta_v,Z_v\) | two copies | two regional clocks still not a common clock | four first-order equations | dust EOS in each | 4 | common-clock and transfer data external | `EXACT` bulk rank 4 |
| conditional fixed C-AVG-com | four bulk states plus \(F_v\) | \(F_v=L_D\delta f_v\); effective-source definitions | carrier CGI gauge fixed by the branch | four bulk plus one partition equation after all residuals are prescribed as known operators | \(C_P(t)=0\) | 5 before compatibility restriction | carrier, maps, kernel, scale, Green realizations, BC, clock, matching; selector only if inverse requested | `EXACT` rank 5 only for a completely selected branch |
| present C-AVG design | above plus unspecified map, clock, kernel, and domain functions | branch-dependent | carrier gauge/domain unidentified | bulk rank 4; fifth equation contains unmodelled transfer/commutator | proposed clean closure | not countable after compatibility until branch selected | all listed external functions remain | `NOT_COUNTABLE_WITHOUT_BRANCH_SELECTION`; \(\Delta_{\rm dyn}\ge1\) |
| sharp C-JUNC | two bulks plus \(Q^\pm,T^\pm\) and traces | first/second fundamental forms | spacetime and hypersurface gauge | branch-dependent junction evolution | matter/interface law | branch-dependent | surface topology, trace spaces, junction BC | `BIFURCATED` |
| C-SHELL | C-JUNC plus surface stress state | Lanczos relations | as above | requires shell evolution | surface EOS | branch-dependent | interface/regularity data | `NOT_COUNTABLE_WITHOUT_BRANCH_SELECTION` |

The report's CGI count is correct. Its metric cross-check is not. “Four metric
scalars, density, velocity” are configuration fields, while scalar Einstein
constraints restrict initial data and gauge generators remove redundant
canonical directions. Subtracting one number per item and calling the result
“phase-space functions” does not show the symplectic/initial-data rank.
BDE's constraint reconstruction and the independent CGI evolution do show the
correct physical result; §14 should be labeled a heuristic consistency check,
not a derivation.

The compatibility system has three mismatch evolution equations, but the
matching-constraint rank is
`NOT_COUNTABLE_WITHOUT_BRANCH_SELECTION`: a concrete transfer may restrict
their image or create algebraic dependence. The report mostly recognizes this
in §28; the executive phrase “three-dimensional” must not be read as a proved
constraint rank.

## 10. Partition-dynamics audit

The volume-fraction identity and linearization pass. The report also correctly
retains the expansion-transfer field
\(\mathcal E_{\Delta\Xi}\) and
\([\partial_t,L_D]\delta f_v\).

The main unresolved items are:

- regional proper-time \(\Theta_r\) has not been mapped to common-time
  \(\Xi_r\);
- the Timescape phenomenological lapse has not been identified with ADM lapse
  \(N\), BMR \(\gamma\), or any tilt variable;
- the regional domains have not been transported on a common foliation;
- \(L_D\) is not defined before the carrier exists;
- moving maps can contribute Lie-derivative/shape-derivative and interface
  terms beyond the displayed abstract commutator;
- the partition function is an extra dynamic initial function only on a smooth
  selected carrier branch.

There is no division by \(\Theta_v-\Theta_w\) or \(H_v-H_w\) in the displayed
kinematics. Any later attempt to solve the clean closure for an
expansion-transfer quantity by dividing by that difference would require a
separate equal-region branch.

## 11. Effective-geometry audit

The source algebra and curvature reconstruction pass. The clean-comoving
condition has the following exact logical chain:

1. GM Eq. (4.20) chooses the effective fluid velocity equal to the dust
   velocity.
2. GM Euler Eq. (4.12) then forces the non-kernel scalar effective pressure
   gradient/Laplacian to vanish.
3. With nonzero \(\rho_{\rm eff}\), the effective-source definitions give
   \(\mathscr W=3\mathscr Q\).

It is therefore an all-time constitutive/frame branch. It is not a theorem of
Buchert averaging and cannot be imposed only at \(t_i\). The report states this
correctly.

For exact regional FLRW backgrounds, \(Q_r=0\), and the first perturbation of
the regional variance and shear-square definition vanishes. This does not say
that a genuinely perturbed non-FLRW regional average has no backreaction; it
says the first nonzero internal \(Q_r\) contribution is second perturbative
order for this branch. The explicit residuals \(\mathcal R_Q,\mathcal R_W\)
are necessary and prevent double counting.

## 12. Constraint-propagation audit

The three-mismatch system is algebraically correct. For zero residuals and
\(C_P(t)=0\), it is a homogeneous linear system, so zero initial mismatches
remain zero on any interval where the background coefficients are regular.
This establishes propagation for every admissible state of that abstract GM
system, not merely one trajectory.

It does **not** establish that a regional transfer has an admissible initial
state satisfying all three mismatches, nor that the three matching conditions
are independent on the image of a future \(T\). Those are existence and rank
questions. It also does not propagate \(C_P\); that relation is imposed.

The three-mismatch result therefore survives with the following exact wording:
“Three evolution mismatches are required on the generic GM clean branch;
their independent matching rank remains branch-dependent.”

## 13. Transfer-operator audit

The expression

\[
T_r=L_DP_rG_r,\qquad
P_rX=S_\ell[\omega_r\phi_r^*X]
\]

has a sensible objective: invert a regional CGI Laplacian back to a base
scalar, localize/pull it to a carrier, and reapply the carrier CGI Laplacian.
The report correctly rejects an unmotivated pointwise Jacobian factor.

It is nevertheless formal:

- \(G_r\) has no declared closed domain or range;
- \(L_rG_r=1-\Pi_{0,r}\) has no selected topology or boundary realization;
- \(\phi_r^*\) has no regularity theorem or trace behavior at the region edge;
- multiplication by \(\omega_r\) is not bounded on every candidate Sobolev
  space;
- \(S_\ell\) has no kernel, normalization, support, or scale law;
- \(L_D\) can create boundary distributions after sharp localization;
- time-dependent spaces lack a common trivialization;
- self-adjointness and boundedness are not shown.

Consequently, domains/codomains, adjoints, kernels, Fredholm properties, and
operator ranks are presently undefined. The report should call this a
“definition-preserving formal pattern,” not a coherent operator
specification.

The spectral conclusion is appropriately modest. Different flat and
negatively curved spectra plus noncommuting restriction/weighting/smoothing
make a diagonal kernel non-generic. They do not make it impossible. The
synthetic diagonal intertwiner confirms that a diagonal transfer can be
engineered under weaker assumptions than isometry; it would simply be an
additional model choice, not a geometrically derived Timescape map.

For time-dependent fixed spaces,
\[
R_T=\dot T+TA_R-A_{\rm GM}T
\]
is correct. For \(X_R(t)\) and \(Y_{\rm GM}(t)\), \(\dot T\) is not defined
until those bundles are trivialized or supplied with connections. Testing one
trajectory is insufficient, as the independent-basis counterexample shows.

## 14. Functional-analysis and elliptic audit

### 14.1 Smooth and sharp partitions

For a sharp indicator \(\chi_r\),

\[
D(\chi_rX)=\chi_rDX+X\,D\chi_r,
\]

\[
D^2(\chi_rX)=\chi_rD^2X
+2D^a\chi_rD_aX+X\,D^2\chi_r.
\]

\(D\chi_r\) is supported distributionally on the interface and
\(D^2\chi_r\) contains normal-derivative/curvature distributions. These terms
can create surface sources or require transmission conditions. They are not
written in the audited report.

For a normalized linear smoothing \(S_\ell\), a sharp partition of unity is
preserved only if \(S_\ell1=1\), but exact idempotence is lost:
\((S_\ell\chi_r)^2\ne S_\ell\chi_r\) and generally
\(S_\ell^2\ne S_\ell\). The Gaussian example changes every nonzero Fourier
mode by \(\exp(-\ell^2k^2/2)\). Smoothing is thus a physical/model scale, not a
neutral numerical device.

### 14.2 Elliptic branches

| Branch | Necessary conditions | Present status |
|---|---|---|
| compact, connected, boundaryless | scalar Laplacian kernel contains constants; source must have zero integral; inverse unique modulo kernel; topology is imported | listed, not selected |
| noncompact decay | complete geometry, weighted Sobolev spaces, decay, spectrum/zero-resonance control; existence is not automatic | listed, not selected |
| finite patch | Dirichlet can give uniqueness under standard ellipticity; Neumann needs zero-integral compatibility and has constant kernel; Robin needs a coercive realization; trace regularity required | listed, not selected |
| sharp interface | transmission/jump conditions for field and conormal derivative; distributional sources must be included; interface regularity/topology imported | not derived |

No branch has a proved closed \(G_r\), so no elliptic or inverse rank should be
reported as exact.

## 15. Initial/boundary-data audit

The conditional five-state branch needs the five bulk/partition initial
functions listed in §27. It also needs, without hiding them in “matching”:

- background clock maps and lapse/tilt data;
- regional-to-carrier embeddings and their time transport;
- partition weights or an interface location/shape;
- smoothing kernel, scale, and normalization;
- regional and carrier function spaces;
- Green domains and zero-mode projectors;
- boundary, decay, or transmission functions;
- initial compatibility conditions and their actual independent rank;
- an inverse selector only if an inverse answer is demanded.

These are external functions or geometric choices, even when they are not
counted as dynamic state variables. The report's current
`NOT_COUNTABLE_BEFORE_BRANCH_SELECTION` token is correct. Its subordinate
claim `MINIMUM_INITIAL_BOUNDARY_MATCHING_PACKAGE_SPECIFIED` is too strong:
categories are enumerated, but the package is not instantiated sufficiently to
define a problem.

At zero effective density, \(\Delta_{\rm eff}\) and
\(\widetilde P_{\rm eff}\) are not valid normalized initial fields. The
unnormalized source numerators are the correct variables for that branch.

## 16. Inverse-problem audit

For a specified bounded linear
\(T:X_{\rm adm}\rightarrow Y_{\rm GM}\), an inverse at
\(y\in\operatorname{Ran}T\) is unique precisely when
\(\ker(T|_{X_{\rm adm}})=\{0\}\). This is the correct theorem stated in §27.

The finite \(3\times5\) example demonstrates a two-dimensional kernel only
after a finite truncation identifies five scalar coefficients with a
five-dimensional domain and three with a three-dimensional codomain. It does
not apply to five and three function spaces. Infinite-dimensional separable
Hilbert spaces can be isomorphic; coefficient interleaving gives an explicit
injective example. Conversely, smoothing or projection can create a kernel,
but smoothing alone is not automatically noninjective: Gaussian convolution
has nonzero multipliers on every finite Fourier mode and is injective on
suitable spaces even though its inverse is unbounded.

No kernel, range, Fredholm index, closed-range property, or admissible selector
is currently known. Additional constraints could remove or create a
nullspace. The report's exact conclusion survives:

> Inverse uniqueness is unresolved; inverse nonuniqueness is also unresolved.

## 17. Limit and falsification audit

| Limit/gate | Independent outcome |
|---|---|
| \(f_v\to0,1\) | volume and variance identities are polynomial and regular; the absent region must be removed as a separate lower-rank branch |
| \(H_v-H_w\to0\) | no current formula divides by it; partition forcing remains \(f_vf_w\delta(\Xi_v-\Xi_w)\) |
| \(\bar Q_D+\bar W_D\to0\) | normalized effective variables fail; unnormalized variables required |
| equal-region | background variance vanishes, but an arbitrary transfer need not become identity without its own limit law |
| globally FLRW | regional bulk reduces correctly; effective normalized branch is singular and transfer recovery is unproved |
| zero perturbation | algebraic equations vanish if all residuals/maps respect zero; not testable until operator exists |
| zero mode | CGI Laplacians annihilate constants; the complete kernel remains topology/BC dependent |
| WKB | local diagonality is possible with a declared error order; no such error estimate is supplied |
| sharp limit | distributional interface terms appear; convergence of the smooth branch is not proved |
| relabeling | bulk/partition algebra is covariant under \(v\leftrightarrow w\); future maps must also transform |

The falsification matrix has meaningful consequences, so its gates are not
decorative. However, carrier nonexistence, elliptic ill-posedness, transfer
incompatibility, and full-basis intertwining cannot be executed before the
objects to be tested are defined. Report §31 line 805 must be weakened from
“every gate ... is executable” to “every gate is a mandatory acceptance
criterion once its branch data are instantiated.”

## 18. Observational-boundary audit

No blocking observational promotion was found. Both deliverables explicitly
prohibit or leave undefined:

- \(Z_r\) as wall peculiar/tracer-velocity divergence;
- wall matter velocity as tracer velocity;
- \(k_w,k_v,k_D,k_{\rm code}\), dressed \(k\), or survey \(k\) identification;
- a dressed Fourier basis;
- \(\sigma_8\) or \(f\sigma_8\);
- RSD or Alcock–Paczynski prediction;
- likelihood readiness or empirical bias.

The search hits at JSON paths such as
`frozen_result_boundary.immutable_distinctions`,
`implementation_readiness.forbidden`, and each
`formal_conclusions[*].observational_consequence` are prohibitions, not
promotions.

## 19. Blocking findings

1. **Undefined common carrier/embedding under the frozen deficit rule.**
   Report §22 says the carrier and maps do not exist in current theory, while
   §32 and three JSON paths claim exact \(N_{\rm undef}=0\). This is the most
   serious inconsistency because zero was the frozen admissibility discriminator
   between finite underclosure and a missing indispensable embedding.
2. **No actual transfer operator.** Without spaces, domains, topology, BC,
   traces, smoothing, and time transport, \(T_r\) has no defined kernel, rank,
   boundedness, or intertwining derivative.
3. **No selected smooth or sharp branch.** The smooth branch has uncontrolled
   scale dependence; the sharp branch has omitted distributional terms and
   possible surface sources.
4. **No instantiated elliptic problem.** Existence, uniqueness, compatibility,
   and boundary data remain unresolved for every proposed topology.
5. **The conditional five-state closure cannot be promoted.** Its fifth
   equation still contains external expansion-transfer and map/commutator
   functions. The current \(\Delta_{\rm dyn}\ge1\) lower bound survives.

These findings block implementation, but they do not invalidate the intrinsic
regional bulk equations or the report's report-only readiness conclusion.

## 20. Non-blocking findings

- The two ApJ DOI values are wrong but the correct scans and equations were
  inspected.
- The metric count is heuristic and should not be used as a proof; the CGI
  derivation independently supports the same bulk rank.
- “Three-dimensional” should describe the generic mismatch state vector, not
  an already established matching-constraint rank.
- The exact test durations differ from the completion response; counts and
  versions agree.
- The eight-artifact completion list omitted two paths, but all ten outputs are
  ignored, reproducible, and canonical.

## 21. Exact minimal correction list

No scientific equation needs to be changed. The minimum report-only
corrections are:

1. Correct closure report §7 and JSON
   `primary_source_inventory[13].citation` / `[14].citation` to DBE92 DOI
   `10.1086/171630` and BDE92 DOI `10.1086/171629`.
2. Replace the metric statement \(6-2-2=2\) as an independent phase-space
   derivation with a clearly labeled heuristic cross-check; retain the CGI and
   constraint reconstruction as the actual rank argument.
3. Make the framework matrix distinguish “current GM target language” from
   “current W07–W09 regional machinery,” and classify a concrete carrier,
   embedding, smoothing kernel, and scale as an optional model extension until
   derived.
4. Replace exact \(N_{\rm undef}=0\) and the full detailed deficit vector with
   a bifurcated entry: zero only if a primary derivation supplies the common
   carrier/embeddings as current-theory variations; otherwise
   \(N_{\rm undef}\ge1\). Update report §§4, 32, 38 and JSON
   `frozen_result_boundary.deficit_lower_bound`, `deficit_vector`, and
   `formal_conclusions.OVERALL`.
5. Qualify “three-dimensional compatibility system” as three generic
   evolution mismatches; leave the independent compatibility rank
   `NOT_COUNTABLE_BEFORE_BRANCH_SELECTION`.
6. Downgrade \(T_r=L_DP_rG_r\) from an operator construction to a formal
   definition pattern until domains/codomains, time trivialization, topology,
   trace spaces, smoothing, Green realizations, and BC are supplied.
7. Add the explicit sharp-interface product/distribution terms and require the
   smooth branch to specify kernel, scale/range, partition of unity,
   non-idempotence, and sharp-limit behavior.
8. Replace `MINIMUM_INITIAL_BOUNDARY_MATCHING_PACKAGE_SPECIFIED` and “every
   gate is executable before a prototype” with statements that the required
   categories and future acceptance gates are enumerated but not instantiated.
9. Correct the completion artifact inventory to all ten paths and state
   explicitly that 29 counts skipped tests.

## 22. Claims that survived unchanged

- The intrinsic regional scalar dust \(k\ne0\) bulk has two state functions and
  rank two per exact FLRW region.
- Two regions therefore have exact intrinsic bulk rank four before common-clock
  and transfer data.
- The global Timescape Mészáros approximation and regional exact dust dynamics
  are ontologically distinct even where their dust operator coincides.
- \(\dot f_v=f_vf_w(\Xi_v-\Xi_w)\).
- The two-region backreaction decomposition and its first variation.
- The effective-source normalizations and the \(+C_P/4\) coefficient.
- Clean-comoving \(\mathscr W=3\mathscr Q\) is an enforced branch, not a
  Buchert identity or propagated initial constraint.
- The three generic mismatch evolution equations.
- Generic spectral mode mixing is justified; absolute non-diagonality is not.
- \(R_T\) must vanish on all admissible data, not a fitted trajectory.
- Inverse uniqueness and nonuniqueness are both unresolved.
- `REPORT_ONLY_MUST_CONTINUE`.

## 23. Claims that must be weakened

- Metric \(6-2-2=2\) “count” to heuristic consistency check.
- “Three-dimensional compatibility” to a three-component generic mismatch
  system with branch-dependent independent rank.
- “Transfer-operator construction” to formal operator pattern.
- “Minimum package specified” to categories enumerated.
- “Every falsification gate executable before a prototype” to future mandatory
  gates after branch instantiation.
- Smooth/sharp neutrality to an explicit model-scale/interface bifurcation.
- Framework labels that treat a selected carrier/smoothing branch as already
  current or merely neutral compatible machinery.

## 24. Claims that must be removed

- The two incorrect DOI identifiers.
- Exact \(N_{\rm undef}=0\) for the present branch.
- The unchanged detailed deficit
  \((0,\ge1,\ge1,\ge1,\ge2,\mathrm{N/A})\).
- Any reading of conditional \(N_{\rm state}=5\),
  \(\operatorname{rank}E=5\), \(\Delta_{\rm dyn}=0\) as a result about the
  present theory rather than a future fully selected branch.

## 25. Final readiness decision

The requested addendum claims resolve as follows:

| Claim | Survived? | Audit result |
|---|---|---|
| regional \(k\ne0\) dust bulk rank two per region | yes | `PASS_WITH_EXPLICIT_CONDITIONS` |
| three-mismatch compatibility system | yes | `PASS_WITH_EXPLICIT_CONDITIONS`; three generic mismatch evolutions, not yet matching rank three |
| \(\Delta_{\rm dyn}\ge1\) | yes | `PASS` as a conservative lower bound for the current design |
| detailed deficit \((0,\ge1,\ge1,\ge1,\ge2,\mathrm{N/A})\) | no | `INCORRECT`; first component must bifurcate or be at least one |
| inverse uniqueness unresolved | yes | `PASS` |
| `REPORT_ONLY_MUST_CONTINUE` | yes | `PASS` |

The strongest surviving result is the exact two-function, rank-two intrinsic
scalar dust system for each \(k\ne0\) regional FLRW sector. The most serious
blocking issue is the absence of a derived common carrier/embedding and
well-defined transfer operator while the deficit nevertheless assigns
\(N_{\rm undef}=0\).

The audited reports must receive the nine report-only corrections in §21
before human scientific review relies on their classifications or deficit
vector. No implementation, observational bridge, or inverse API is authorized.

REQUIRES_TARGETED_CORRECTIONS

IMPLEMENTATION_AUTHORIZATION:
NOT_GRANTED
