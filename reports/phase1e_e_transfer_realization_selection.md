# Phase 1E-E — Common-Carrier and Regional-to-GM Transfer-Realization Selection

**Deliverable type:** report-only scientific selection and audit specification

**Artifact date (UTC):** `2026-07-30T21:24:00Z`

**Correction status:** `TARGETED_CORRECTIONS_APPLIED_AFTER_INDEPENDENT_AUDIT`

**Primary verdict:** `PRIMARY_REALIZATION_CLASS_SELECTED_CONDITIONALLY`

**Overall verdict:** `PARTIAL_REALIZATION_DEFICITS_REMAIN`

**Theory consequence:** `NEW_DYNAMICS_REQUIRED`

**Implementation readiness:** `REPORT_ONLY_MUST_CONTINUE`

**Implementation authorization:** `NOT_GRANTED`

> Repository limitation: these artifacts were generated in an isolated artifact workspace containing supplied Phase 1E source reports, not in the user PC Git checkout. Branch, HEAD, worktree, refs and tests are recorded from the frozen project state but were not independently Git-verified here.

## 1. Executive verdict

Phase 1E-E conditionally retains `S1-LAGRANGIAN-SMOOTH-COMPACT-MEANZERO` as the provisional author-selected baseline architecture. No theorem establishes that S1 has a uniquely minimal extension burden relative to H1. The selection is at architecture level only. Exact topology, metric extensions, embeddings, partition profile, effective-sector transfer, constitutive closure, compatibility propagation and forward well-posedness remain unresolved.

```text
PRIMARY_REALIZATION_CLASS_SELECTED_CONDITIONALLY
PARTIAL_REALIZATION_DEFICITS_REMAIN
NEW_DYNAMICS_REQUIRED
REPORT_ONLY_MUST_CONTINUE
```

## 2. Scope and preservation statement

This report consolidates the scientific definition P0–P8 and creates no source code, numerical solver, prototype, observable, dataset interface or inference machinery. Candidate A and the D3 policy remain untouched. The report preserves the distinction among theoretical regional fields, GM target fields, wall matter, tracers and observational quantities.

## 3. Repository preflight

| Field | Recorded value |

| --- | --- |

| repository | ing-mattioni/timescape-fsigma8 |

| required_branch | phase-1e-e-transfer-realization-selection |

| declared_branch_state | clean, local-only, unpushed, no upstream |

| required_starting_head | 2fd3ed2006821bc162fb740bd773f2d0b6e5e0b4 |

| declared_main | 2fd3ed2006821bc162fb740bd773f2d0b6e5e0b4 |

| declared_origin_main | 2fd3ed2006821bc162fb740bd773f2d0b6e5e0b4 |

| phase1e_d_tag | phase-1e-d-regional-matching-dynamics-v1 |

| pinned_upstream_commit | 590c6fd5332acb15f5683ebf392a0d7ce54983c5 |

| pinned_notebook_sha256 | 86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a |

| last_reported_tests | {"python_3_14_3": "379 passed", "python_3_11_9": "379 passed"} |

| verification_status | DECLARED_FROZEN_CHECKPOINT_NOT_GIT_VERIFIED_IN_ARTIFACT_SANDBOX |

| verification_limitation | The artifact workspace contains supplied reports but is not the user PC Git checkout; branch, worktree, refs, tags and test environments were not independently inspected here. |


The checkpoint is a declared frozen state. A future repository authoring task must repeat the full Git preflight in the actual checkout before integrating these files.

## 4. Frozen Phase 1E-D boundary

| ID | Frozen statement | Classification |

| --- | --- | --- |

| FROZEN-01 | For each regional exact FLRW dust geometry and intrinsic nonzero scalar mode, X_r=(Delta_r,Z_r) has rank two with dDelta_r/dtau_r=-Z_r and dZ_r/dtau_r=-2H_r Z_r-4piG rho_r Delta_r. | VERIFIED_FROM_PRIMARY_SOURCE |

| FROZEN-02 | The wall-plus-void intrinsic bulk rank is four; the metric 6-2-2 count is only a heuristic cross-check. | DERIVED_FROM_VERIFIED_DEFINITIONS |

| FROZEN-03 | k_code, k_w, k_v, carrier, dressed and survey wavenumbers remain distinct. | DERIVED_FROM_VERIFIED_DEFINITIONS |

| FROZEN-04 | The GM formal zero-measure domain, finite infinity, radial-null matching and a 3D spatial carrier remain distinct. | DERIVED_FROM_VERIFIED_DEFINITIONS |

| FROZEN-05 | Regional dust velocity, wall velocity, tracer velocity, CGI Z and observational velocity divergence remain distinct. | DERIVED_FROM_VERIFIED_DEFINITIONS |

| FROZEN-06 | Candidate A remains external, conditional, clean-only, theoretical and non-predictive in normalization. | DERIVED_FROM_VERIFIED_DEFINITIONS |

| FROZEN-07 | D3 remains RESOLVED_DERIVED_4_10 with explicit derived_4_10 and printed_4_15 branches and no default. | SYMBOLICALLY_VERIFIED |

| FROZEN-08 | Compatibility retains C_Delta, C_Z and C_eff; C_P is separate. | DERIVED_FROM_VERIFIED_DEFINITIONS |

| FROZEN-09 | Component count is not rank; matching rank remains not countable before a concrete transfer. | DERIVED_FROM_VERIFIED_DEFINITIONS |

| FROZEN-10 | T_r=L_D P_r G_r is only a formal pattern until spaces, domains, maps, kernels and data are defined. | DERIVED_FROM_VERIFIED_DEFINITIONS |

| FROZEN-11 | Inverse uniqueness and nonuniqueness remain unresolved before a concrete admissible transfer is selected. | DERIVED_FROM_VERIFIED_DEFINITIONS |

| FROZEN-12 | Current Timescape machinery does not supply the complete common carrier and regional-to-GM transfer. | VERIFIED_FROM_PRIMARY_SOURCE |


## 5. Phase 1E-E scientific question

The phase asks whether a common three-dimensional carrier and regional-to-GM transfer can be specified sufficiently to select a primary scientific architecture without silently identifying regional and carrier spectra, importing observational assumptions or claiming closure that has not been derived.

## 6. Selection, specification, closure and implementation

| Level | Meaning | P8 status |

| --- | --- | --- |

| Family selection | choose smooth, sharp, moment, local or auxiliary role | complete |

| Architecture selection | choose carrier class, spaces, transfer pattern and target scope | S1 selected conditionally |

| Concrete realization | fix topology, metrics, maps, domains and data | incomplete |

| Dynamical closure | prove compatibility, constraints and well-posedness | failed/not established |

| Implementation | create scientific runtime | not authorized |


## 7. Evidence and framework-classification policy

Every formal conclusion uses exactly one evidence classification. Generic GR, PDE and functional-analysis machinery is `COMPATIBLE_IMPORTED_DYNAMICS`, not `CURRENT_TIMESCAPE_MACHINERY`, unless a primary Timescape source supplies it. Unknown ranks or deficits are represented by explicit tokens rather than zero.

## 8. Common Realization Record

Every concrete realization must instantiate the following mandatory record:

```text
id
title
parent_families
scientific_role
target_scope
framework_status
selection_status
carrier_geometry
regional_maps
clock_branch
functional_spaces
operator_factorization
zero_mode_policy
dynamical_inputs
initial_data
boundary_or_interface_data
compatibility_system
constraint_system
forward_status
inverse_status
approximation_status
information_loss_status
gate_results
deficit_vector
falsification_conditions
implementation_readiness
```

## 9. Common object dictionary

| ID | Object | Framework | Definition state | Notes |
| --- | --- | --- | --- | --- |
| OBJ-REG-STATE-r | \(X_r=(\Delta_r,Z_r)\) | COMPATIBLE_IMPORTED_DYNAMICS | DYNAMICALLY_DETERMINED | rank-two regional nonzero-mode scalar state |
| OBJ-REG-TIME-r | \(\tau_r\) | CURRENT_TIMESCAPE_MACHINERY | BACKGROUND_DEFINED | regional proper time |
| OBJ-REG-LAP-r | \(L_r=a_r^2D_r^2\) | COMPATIBLE_IMPORTED_DYNAMICS | KINEMATICALLY_DEFINED | sign convention inherited from the frozen CGI branch; domain, full kernel and boundary/decay data remain branch-dependent |
| OBJ-CAR-MAN | \(\Sigma_C\) | COMPATIBLE_IMPORTED_DYNAMICS | KINEMATICALLY_DEFINED | compact connected boundaryless reference-manifold class; orientation is optional because a volume density suffices |
| OBJ-CAR-GEO | \(h_C\) | OPTIONAL_MODEL_EXTENSION | NOT_DEFINED_IN_CURRENT_THEORY | conditional convex-blend template; existence and regularity of global metric extensions are unproved |
| OBJ-CAR-MEASURE | \(d\mu_C\) | COMPATIBLE_IMPORTED_DYNAMICS | DERIVED_IF_CURRENT_THEORY_DEPENDENCIES_KNOWN | derived from \(h_C\) once the metric exists |
| OBJ-CAR-TIME | \(t_D\) | CURRENT_TIMESCAPE_MACHINERY | BACKGROUND_DEFINED | selected S1 carrier time |
| OBJ-MAP-EMB-r | \(\iota_r\) | COMPATIBLE_IMPORTED_DYNAMICS | NOT_DEFINED_IN_CURRENT_THEORY | whole-slice versus finite-domain maps and exact embeddings remain unresolved |
| OBJ-MAP-CLOCK-r | \(\tau_r(t_D)\) | COMPATIBLE_IMPORTED_DYNAMICS | KINEMATICALLY_DEFINED | selected homogeneous background reparameterization only; no perturbative or spatial clock map |
| OBJ-PART-SMOOTH-r | \(\chi_r\) | OPTIONAL_MODEL_EXTENSION | KINEMATICALLY_DEFINED | smooth Lagrangian-fixed partition of unity |
| OBJ-PART-IFACE | \(\Gamma\) | OPTIONAL_MODEL_EXTENSION | KINEMATICALLY_DEFINED | H1 comparator only |
| OBJ-OP-GREEN-r | \(G_r\) | COMPATIBLE_IMPORTED_DYNAMICS | NOT_DEFINED_IN_CURRENT_THEORY | regional elliptic branch, domain, full kernel and boundary/decay data unresolved |
| OBJ-OP-LAP-C | \(\mathcal L_C\) | COMPATIBLE_IMPORTED_DYNAMICS | NOT_DEFINED_IN_CURRENT_THEORY | normalized carrier scalarization; \(-D_C^2\) is only a conditional subbranch after sign, dimensions and metric convention are fixed |
| OBJ-OP-Q-C | \(Q_C\) | COMPATIBLE_IMPORTED_DYNAMICS | KINEMATICALLY_DEFINED | output mean-zero range check; redundant after a compact-boundaryless Laplacian subbranch whose range is already mean-zero |
| OBJ-OP-T-EFF | \(\mathcal T_{\rm eff}\) | COMPATIBLE_IMPORTED_DYNAMICS | NOT_DEFINED_IN_CURRENT_THEORY | primary unresolved S1 block |
| OBJ-COMP-DELTA | \(C_\Delta\) | COMPATIBLE_IMPORTED_DYNAMICS | DERIVED_IF_CURRENT_THEORY_DEPENDENCIES_KNOWN | density mismatch |
| OBJ-COMP-Z | \(C_Z\) | COMPATIBLE_IMPORTED_DYNAMICS | DERIVED_IF_CURRENT_THEORY_DEPENDENCIES_KNOWN | expansion mismatch |
| OBJ-COMP-EFF | \(C_{\rm eff}\) | COMPATIBLE_IMPORTED_DYNAMICS | DERIVED_IF_CURRENT_THEORY_DEPENDENCIES_KNOWN | load-bearing effective-density mismatch |
| OBJ-COMP-P | \(C_P=\mathscr W-3\mathscr Q\) | CURRENT_TIMESCAPE_MACHINERY | KINEMATICALLY_DEFINED | inherited clean-comoving target closure \(C_P(t)=0\); regional reconstruction/evaluation remains missing |

## 10. Geometry dictionary

### S1

| Property | Value |
| --- | --- |
| carrier_class | COMPACT_CONNECTED_BOUNDARYLESS_REFERENCE_3_MANIFOLD |
| orientation | OPTIONAL_VOLUME_DENSITY_BRANCH |
| exact_topology | UNSELECTED |
| regional_cover | \(U_w\cup U_v=\Sigma_C\) |
| partition | smooth partition of unity |
| metric_template | CONDITIONAL_TEMPLATE: \(h_C=\chi_w\widetilde h_w+\chi_v\widetilde h_v\) |
| extension_status | existence, regularity, uniqueness and naturality of \(\widetilde h_r\) are unproved |
| volume_constraint | \(K_f=0\) must be imposed and propagated |
| outer_boundary | NOT_APPLICABLE_FOR_CARRIER_ONLY |

### H1

| Property | Value |
| --- | --- |
| carrier_class | same compact reference class |
| regional_domains | \(\Omega_w,\Omega_v\) |
| interface | Lipschitz-or-better \(\Gamma\) |
| metric | piecewise smooth |
| transmission | SH-1 source-free comparator |
| outer_boundary | NOT_APPLICABLE_FOR_CARRIER_ONLY |

## 11. Clock and frame dictionary

| ID | Carrier time | Regional time | Rate | Spatial dependence | Perturbative lapse |

| --- | --- | --- | --- | --- | --- |

| CLK-S1 | t_D | tau_r(t_D) | alpha_r=d tau_r/d t_D > 0 | EXCLUDED | NOT_DEFINED |

| CLK-H1 | t_D | tau_r(t_D) | homogeneous | EXCLUDED | NOT_DEFINED |

| CLK-L1 | local inherited time | local restriction | UNDERDETERMINED | local branch only |  |


## 12. Spectral-scale dictionary

| ID | Meaning | Policy |

| --- | --- | --- |

| K-CODE | implementation/notebook label | distinct |

| K-W | wall regional eigenvalue or wavenumber | distinct |

| K-V | void regional eigenvalue or wavenumber | distinct |

| K-C | carrier spectral label | distinct |

| K-DRESSED | dressed theoretical label | distinct |

| K-SURVEY | observational label | outside Phase 1E-E |

| KERNEL-RC | regional-to-carrier spectral kernel K_nm^(r) | non-diagonal mode mixing allowed |


## 13. Candidate families R1–R8

| ID | Family | Layer | Standalone | Status |

| --- | --- | --- | --- | --- |

| R1 | smooth partition carrier | carrier/localization | False | retained |

| R2 | sharp interface carrier | carrier/interface | False | retained comparator |

| R3 | weak or finite-volume formulation | formulation | False | retained |

| R4 | spectral representation | representation/operator | False | DEMOTED_TO_REPRESENTATION_LAYER |

| R5 | Green operator | operator | False | DEMOTED_TO_REPRESENTATION_LAYER |

| R6 | auxiliary-FLRW carrier | alternative carrier | False | background-only rejected; full field extension only |

| R7 | local patch or WKB | local approximation | False | local comparator |

| R8 | direct moments | target reduction | False | reduced target only |


## 14. Layer decomposition of a realization

A complete realization is not one R-label. Its meta-model is

\[\mathfrak R=(\mathfrak C,\mathfrak F,\mathfrak O,\mathfrak S,\mathfrak T,\mathfrak D,\mathfrak B,\mathfrak K).\]

These entries denote carrier, formulation, operators, scale regime, target, dynamics, data and compatibility/constraints.

## 15. Candidate compound architectures CR-1–CR-7

| ID | Composition | Target | Normalized role |

| --- | --- | --- | --- |

| CR-1 | R1, R3, R5 | global weak/full field | S1 |

| CR-2 | R1, R4, R5 | global spectral/full field | spectral variant of S1 |

| CR-3 | R2, R3, R5 | global sharp weak field | H1 |

| CR-4 | R2, R3, R8 | sharp finite moments | M1 parent H1 |

| CR-5 | R1, R3, R8 | smooth finite moments | M1 parent S1 |

| CR-6 | R6, R4/R5 | auxiliary effective/full field | X1 extension |

| CR-7 | R7, local R3/R4/R5 | local patch state | L1 |


## 16. Normalized candidate classes after P6

| ID | Packet | Class | Status |

| --- | --- | --- | --- |

| P6-C1 | S1 | global smooth full-field | PRIMARY_SELECTED_CONDITIONALLY |

| P6-C2 | H1 | global sharp weak full-field | MANDATORY_SECONDARY_COMPARATOR |

| P6-C3 | M1 | reduced moment target | REDUCED_TARGET_COMPARATOR |

| P6-C4 | L1 | local WKB | LOCAL_DIAGNOSTIC_COMPARATOR |

| P6-X1 | X1 | auxiliary full-field extension | OPTIONAL_MODEL_EXTENSION |


## 17. Carrier-geometry branches

S1 uses a compact connected orientable boundaryless reference 3-manifold class and a smooth partition. H1 uses the same carrier class with piecewise-smooth regional domains and an explicit interface. M1 inherits a parent geometry; L1 is local only. No exact topology is selected.

## 18. Functional-space branches

| ID | Space | Domain | Packet | Status |
| --- | --- | --- | --- | --- |
| FS-REG | BRANCHWISE_REGIONAL_SOURCE_SPACES | compact mean-zero, finite-patch boundary-value, noncompact weighted-decay or another explicit elliptic branch | S1/H1 | DEFINED_BUT_UNDERDETERMINED |
| FS-S1 | \(L^2_0(\Sigma_C)\) | \(H^2_{\perp0}(\Sigma_C):=H^2(\Sigma_C)\cap L^2_0(\Sigma_C)\) | S1 carrier subbranch | selected conditionally |
| FS-H1 | \(H^1(\Omega_w)\oplus H^1(\Omega_v)\) | coupled transmission domain | H1 | selected comparator |
| FS-M1 | \(\mathbb R^{3N}\) | inherited parent fields | M1 | finite reduced target |
| FS-L1 | \(H^s_{\rm loc}(U_\alpha)\) or a local distribution space | local parametrix domain | L1 | local only |

The notation \(H^2_{\perp0}\) means mean-zero \(H^2\); it is deliberately distinct from a Dirichlet closure convention sometimes denoted \(H^2_0\).

## 19. Operator-domain inventory

| ID | Operator | Domain | Codomain | Kernel status | Status |
| --- | --- | --- | --- | --- | --- |
| OP-U-r | homogeneous clock transport | regional state at \(\tau_r\) | regional state at \(t_D\) | not load-bearing if \(d\tau_r/dt_D>0\) | selected conditionally |
| OP-G-r | regional Green inverse | unselected regional elliptic source space | unselected regional potential domain | full kernel unresolved; constants are only one compact-branch possibility | DEFINED_BUT_UNDERDETERMINED |
| OP-E-r | regional lifting | \(D(G_r)\) after regional branch selection | carrier regularity space selected for \(\mathcal L_C\) | must be injective or declared quotient | not concretely defined |
| OP-M-chi | partition multiplication | carrier Sobolev space | same carrier space under sufficient multiplier regularity | support-dependent | selected class |
| OP-L-C | normalized carrier scalarization \(\mathcal L_C\) | unselected scalarization domain | unselected carrier target space | sign, dimensions, scale and kernel unresolved | NOT_DEFINED_IN_CURRENT_THEORY |
| OP-Q-C | output mean-zero range check | \(L^2(\Sigma_C)\) | \(L^2_0(\Sigma_C)\) | constants | range check only; redundant after a compact Laplacian output |
| OP-A-GAMMA | coupled transmission operator | broken \(H^1\) with SH-1 conditions | dual weak space | unresolved | H1 comparator |
| OP-MOM | finite moment projection | parent field space | \(\mathbb R^{3N}\) | nontrivial infinite-dimensional field kernel | M1 |
| OP-PARAM | local parametrix | local patch source space | local patch state | local branch | L1 |

## 20. Elliptic classes E1–E7

| ID | Class | Status | Solvability |
| --- | --- | --- | --- |
| E1 | compact boundaryless mean-zero | selected conditionally for the S1 carrier subbranch only | mean-zero range or quotient by constants after operator normalization |
| E2 | bounded Dirichlet | regional or carrier branch not selected | conditional |
| E3 | bounded Neumann | regional or carrier branch not selected | flux compatibility plus normalization |
| E4 | coercive Robin | not selected | coefficient and coercivity required |
| E5 | noncompact weighted decay | regional branch possible but not selected | decay and zero-resonance control unresolved |
| E6 | sharp coupled transmission | selected for H1 comparator | coupled kernel and coercivity underdetermined |
| E7 | local parametrix | selected for L1 comparator | local only |

S1 does not yet select a universal regional elliptic class. Whole regional FLRW slices, finite regional domains and noncompact weighted realizations remain separate branches.

## 21. Smooth transfer construction

For each scalar sector \(a\in\{\Delta,Z\}\), S1 retains the conditional architecture

\[
T_r^{(a)}=\mathcal L_C M_{\chi_r}E_r\mathcal U_rG_rQ_r,
\]

with an optional output check

\[
Q_C T_r^{(a)}=T_r^{(a)}
\]

only after the range of \(\mathcal L_C\) has been shown to be mean-zero. In the compact boundaryless subbranch \(\mathcal L_C=-D_C^2\), one has \(Q_C\mathcal L_C=\mathcal L_C\), so the final projector is redundant rather than a load-bearing transfer choice.

The carrier scalarization \(\mathcal L_C\) is not yet defined. A concrete subbranch must declare:

- sign convention;
- whether \(h_C\) is physical or comoving;
- carrier length or scale normalization;
- dimensions;
- domain and codomain;
- relation to the frozen regional operators \(L_r=a_r^2D_r^2\);
- preservation of the intended CGI source identity.

The smooth partition is a finite model input. No separate field-smoothing operator is selected. Automatic commutation is forbidden:

\[
[\mathcal L_C,M_{\chi_r}]\neq 0
\]

in general, with the explicit differential expression depending on the selected \(\mathcal L_C\) subbranch.

## 22. Sharp weak-transfer construction

H1 uses a broken weak space and a coupled transmission operator:

\[T_{\rm sharp}=L_{\rm GM}G_\Gamma Q_\Gamma J_\Gamma\mathcal U_{\rm reg}.\]

The comparator selects continuous reconstructed potential and continuous conormal flux with zero surface source as a falsifiable assumption. It does not identify the interface with finite infinity or the GM formal zero-measure domain.

## 23. Smooth-to-sharp convergence requirements SL0–SL5

| Level | Requirement |

| --- | --- |

| SL0 | partition-value convergence |

| SL1 | distributional derivative convergence |

| SL2 | geometry and measure convergence |

| SL3 | source convergence in a declared dual space |

| SL4 | operator/form or resolvent convergence |

| SL5 | target and compatibility convergence |


S1 makes no smooth-to-sharp equivalence claim.

## 24. Initial, boundary and interface data

**bulk_initial_data:** \(\Delta_{w,i},Z_{w,i},\Delta_{v,i},Z_{v,i}\)

**carrier_structural_data:** topology class, regional cover and conditional metric-extension prescription

**clock_data:** \(\tau_r(t_D)\), \(d\tau_r/dt_D>0\)

**partition_data:** \(\chi_v(x)\), \(\chi_w=1-\chi_v\), fixed Lagrangian transport

**sharp_interface_data:** \(\Gamma_i\), SH-1 trace continuity, SH-1 conormal-flux continuity

**carrier_elliptic_data:** mean-zero range compatibility for the selected compact carrier subbranch

**regional_elliptic_data:** topology, full kernel, boundary/decay conditions and operator domains remain bifurcated and unresolved

**constitutive_target_condition:**

\[
C_P=\mathscr W-3\mathscr Q,
\qquad C_P(t)=0
\]

for the inherited clean-comoving GM branch.

**missing_constitutive_block:** the regional-to-target reconstruction or dynamics needed to evaluate \(\mathscr W\) and \(\mathscr Q\)

**effective_sector_data:** \(\mathcal T_{\rm eff}\) unresolved

**initial_compatibility:** \(C_\Delta=0\), \(C_Z=0\), \(C_{\rm eff}=0\), \(K_f=0\)

The compact S1 carrier has no outer boundary, but regional inverse-Laplacian boundary or decay data remain unresolved. Consequently \(\Delta_{\rm BC}\) is `BIFURCATED`, not `NOT_APPLICABLE`.

## 25. Zero-mode branches

| ID | Description | Status |
| --- | --- | --- |
| ZM-REG | select the regional inverse zero-mode/full-kernel policy after choosing the regional elliptic branch | DEFINED_BUT_UNDERDETERMINED |
| ZM-S1 | project each regional contribution before assembly | not selected |
| ZM-S2 | use \(Q_C\) only as an explicit output range check | selected as a range check; not load-bearing |
| ZM-S3 | impose total carrier-source compatibility without projection | not selected |
| ZM-S4 | retain a separate homogeneous GM sector | not selected |

In a compact boundaryless carrier-Laplacian subbranch, \(Q_C\mathcal L_C=\mathcal L_C\). The unresolved zero-mode choices therefore reside primarily in the regional inverses and in any future carrier inverse problem, not in a projector applied after scalarization.

## 26. Constraint inventory

| ID | Constraint class | Status |

| --- | --- | --- |

| K1 | regional bulk evolution identities | frozen |

| K2 | regional CGI admissibility and zero-mode restrictions | branch-dependent |

| K3 | elliptic range constraints | selected mean-zero class for S1 |

| K4 | transfer compatibility constraints | not propagated |

| K5 | interface or boundary constraints | H1 comparator only |

| K-INTERTWINE | K_GM T = S_K K_reg | not demonstrated |


The required intertwining condition is \(\mathcal K_{\rm GM}T=S_K\mathcal K_{\rm reg}\), possibly modulo controlled boundary/interface residuals.

## 27. Mismatch propagation

\[
\boldsymbol C=(C_\Delta,C_Z,C_{\rm eff})^T,
\qquad
R_T=\dot T+TA_{\rm reg}-A_{\rm GM}T.
\]

The generic structure is

\[
\dot{\boldsymbol C}=M_C\boldsymbol C+B_PC_P-\boldsymbol R_T.
\]

The inherited clean-comoving branch must retain the exact relations

\[
\dot C_\Delta=-C_Z-R_\Delta,
\]

\[
\dot C_{\rm eff}
=w\Theta C_{\rm eff}-(1+w)C_Z-R_{\rm eff},
\]

\[
\dot C_Z
=-\frac23\Theta C_Z
-4\pi G\rho_dC_\Delta
-4\pi G\rho_{\rm eff}C_{\rm eff}
+\frac14C_P-R_Z,
\]

with

\[
C_P=\mathscr W-3\mathscr Q,
\qquad C_P(t)=0
\]

as the inherited target constitutive condition. Initial compatibility does not prove all-time compatibility because \(R_\Delta,R_Z,R_{\rm eff}\) and the regional reconstruction of \(C_P\) remain uncontrolled.

## 28. Forward well-posedness

The regional bulk is well posed under the frozen background. S1 and H1 are conditionally definable at snapshot level but are not predictively forward-closed. Existence, uniqueness and continuous dependence have not been established for the complete regional-to-GM system.

## 29. Inverse injectivity and stability

Stable injectivity requires \(\beta_T=\inf_{\|y\|=1}\|Ty\|>0\). Exact injectivity and stable inversion are distinct. For a two-region linear transfer, individual kernels must vanish and \(\operatorname{Ran}T_w\cap\operatorname{Ran}T_v=\{0\}\). S1 and fixed-interface H1 remain unresolved. Finite linear moments and finite spectral truncations are noninjective as full-field maps.

## 30. Approximation hierarchy

| ID | Approximation | Readiness |

| --- | --- | --- |

| A-ELL | finite smooth-scale family | AR0 pass; AR1 partial; no error bound |

| A-SHARP | smooth-to-sharp limit | SL0-SL5 required; not established |

| A-N | spectral truncation | finite truncation creates field kernel; no tail bound |

| A-M | moment truncation | finite-moment field information loss proved; hierarchy not closed |

| A-WKB | local WKB | parameter identified; no error bound |


The scientific error budget is \[E_{\rm total}\le E_{\rm geometry}+E_{\rm clock}+E_{\rm operator}+E_{\rm dynamics}+E_{\rm compatibility}+E_{\rm constitutive}+E_{\rm approximation}.\]

## 31. Packet S1

| Property | Value |
| --- | --- |
| id | S1-LAGRANGIAN-SMOOTH-COMPACT-MEANZERO |
| title | Global smooth Lagrangian partition carrier with regional-potential reconstruction |
| parent_families | ["R1", "R3", "R5"] |
| scientific_role | GLOBAL_CANDIDATE_CARRIER_REPRESENTATION_FOR_GM_TARGET |
| target_scope | GLOBAL_CANDIDATE_CARRIER_SCALAR_REPRESENTATION_FOR_GM_TARGET |
| framework_status | ["COMPATIBLE_IMPORTED_DYNAMICS", "OPTIONAL_MODEL_EXTENSION"] |
| selection_status | PRIMARY_SELECTED_CONDITIONALLY |
| selection_evidence | CONVENTION_DEPENDENT_PROVISIONAL_AUTHOR_BASELINE |
| carrier_geometry | compact connected boundaryless reference-manifold class; exact topology unselected; conditional convex metric-blend template; carrier outer boundary not applicable |
| regional_maps | finite-domain versus whole-slice choice unresolved; exact embeddings unselected |
| clock_branch | homogeneous background reparameterization only |
| functional_spaces | carrier \(L^2_0\) with \(H^2_{\perp0}\); regional elliptic spaces branchwise and underdetermined |
| operator_factorization | \(T_r^{(a)}=\mathcal L_CM_{\chi_r}E_r\mathcal U_rG_rQ_r\); \(Q_C\) is only an optional output range check |
| zero_mode_policy | regional inverse zero-mode/full-kernel branch unresolved; output \(Q_C\) non-load-bearing |
| dynamical_inputs | fixed partition; background regional evolution; metric/measure/operator transport unresolved; effective-sector dynamics missing; inherited \(C_P=\mathscr W-3\mathscr Q=0\) target closure with missing regional reconstruction |
| initial_data | regional \(X_w,X_v\), initial partition profile, metric-extension-compatible carrier data |
| boundary_or_interface_data | carrier outer boundary not applicable; regional boundary/decay data and full-kernel policy unresolved |
| compatibility_system | MISMATCH-SYSTEM |
| constraint_system | K1–K5 and K-INTERTWINE |
| forward_status | snapshot conditional; predictive closure and continuous dependence not established |
| inverse_status | INVERSE_UNIQUENESS_UNRESOLVED_FOR_SELECTED_S1 |
| approximation_status | finite smooth model; partition and metric-extension sensitivity required |
| information_loss_status | regional kernels, range overlap and candidate scalarization losses unresolved |
| deficit_vector | \(N_{\rm undef}\): LOWER_BOUND; \(\Delta_{\rm dyn}\): LOWER_BOUND; \(\Delta_{\rm IC}\): LOWER_BOUND; \(\Delta_{\rm BC}\): BIFURCATED; \(\Delta_{\rm match}\): NOT_COUNTABLE_BEFORE_CONCRETE_OPERATOR_LINEARIZATION; \(\Delta_{\rm emp}\): NOT_APPLICABLE |
| implementation_readiness | REPORT_ONLY_MUST_CONTINUE |

The carrier metric remains only the conditional template

\[
h_C=\chi_w\widetilde h_w+\chi_v\widetilde h_v,
\]

whose extension existence and regularity have not been proved. The required background consistency test is

\[
K_f(t)=\frac{\int_{\Sigma_C}\chi_v\,d\mu_C}{\int_{\Sigma_C}d\mu_C}-f_v^{\rm TS}(t)=0.
\]

## 32. Packet H1

| Property | Value |

| --- | --- |

| id | H1-LAGRANGIAN-SHARP-COMPACT-TRANSMISSION |

| title | Global sharp Lagrangian carrier with source-free weak transmission |

| parent_families | ["R2", "R3", "R5"] |

| scientific_role | GLOBAL_WEAK_FIELD_TRANSFER |

| target_scope | GLOBAL_WEAK_PIECEWISE_GM_FIELD |

| framework_status | ["COMPATIBLE_IMPORTED_DYNAMICS", "OPTIONAL_MODEL_EXTENSION"] |

| selection_status | MANDATORY_SECONDARY_COMPARATOR |

| carrier_geometry | {"carrier_class": "same compact reference class", "exact_topology": "UNSELECTED", "regional_domains": "Omega_w, Omega_v", "interface": "Lipschitz-or-better Gamma", "metric": "piecewise smooth", "transmission": "SH-1 source-free comparator", "outer_boundary": "NOT_APPLICABLE"} |

| regional_maps | EXACT_EMBEDDINGS_UNSELECTED |

| clock_branch | CLK-H1 |

| functional_spaces | broken H1 with coupled transmission domain |

| operator_factorization | T_sharp=L_GM G_Gamma Q_Gamma J_Gamma U_reg |

| zero_mode_policy | coupled mean-zero policy |

| dynamical_inputs | ["fixed reference interface", "SH-1 transmission", "effective-sector dynamics missing"] |

| initial_data | ["regional X_w,X_v", "initial Gamma", "transmission-compatible data"] |

| boundary_or_interface_data | ["[psi]_Gamma=0", "[a D_n psi]_Gamma=0", "surface source zero as comparator assumption"] |

| compatibility_system | MISMATCH-SYSTEM |

| constraint_system | ["K1", "K2", "K3", "K4", "K5", "K-INTERTWINE"] |

| forward_status | {"snapshot": "CONDITIONAL", "predictive": "NOT_CLOSED", "continuous_dependence": "NOT_ESTABLISHED", "inverse": "UNRESOLVED"} |

| inverse_status | FIXED_INTERFACE_INJECTIVITY_UNRESOLVED |

| approximation_status | exact sharp comparator; no smooth-limit claim |

| information_loss_status | joint state/interface inverse unresolved |

| deficit_vector | {"N_undef": "LOWER_BOUND", "Delta_dyn": "LOWER_BOUND", "Delta_IC": "LOWER_BOUND", "Delta_BC": "BIFURCATED", "Delta_match": "NOT_COUNTABLE_BEFORE_CONCRETE_OPERATOR_LINEARIZATION", "Delta_emp": "NOT_APPLICABLE"} |

| implementation_readiness | REPORT_ONLY_MUST_CONTINUE |


## 33. Packet M1

M1 is a finite-dimensional target inherited from S1 or H1. Its target may contain a selected set of carrier moments of \(\Delta\), \(Z\) and \(\Delta_{\rm eff}\). It is not a full-field realization. Field-information loss is proved for a finite linear moment map on an infinite-dimensional field space.

## 34. Packet L1

L1 is a local frozen-coefficient or WKB comparator on a patch \(U_\alpha\), with parameter \(\epsilon_{\rm WKB}=\lambda_{\rm local}/L_{\rm carrier}\). It does not supply global gluing, a global spectrum or a global inverse.

## 35. Auxiliary-field extension status

A full auxiliary-field transfer remains an optional model extension and must explicitly map the regional perturbation state. A background-only auxiliary-FLRW matching is rejected as a regional perturbation transfer because it ignores the perturbations and is therefore noninjective with respect to them.

## 36. Rejected and demoted branches

| ID | Status | Reason |

| --- | --- | --- |

| R6-BACKGROUND-ONLY-AUXILIARY | REJECTED | regional perturbation state is absent from the auxiliary map |

| SHORTCUT-K-EQUALITY | REJECTED | no default identification k_w=k_v=k_C |

| SHORTCUT-DIAGONAL-KERNEL | REJECTED | mode-diagonal transfer requires proof |

| SHORTCUT-FULL-L2-INVERSE | REJECTED | compact Laplacian requires zero-mode treatment |

| SHORTCUT-SHARP-DIRECT-SUM | REJECTED | coupled transmission is not G_w direct-sum G_v |

| SHORTCUT-SMOOTH-SHARP | REJECTED | pointwise partition convergence is insufficient |

| SHORTCUT-MOMENT-FIELD | REJECTED | finite moments are not a full field |

| SHORTCUT-TRUNCATED-INVERSE | REJECTED | finite spectral truncation creates a field kernel |

| SHORTCUT-LOCAL-GLOBAL | REJECTED | local WKB cannot be promoted globally without gluing |

| SHORTCUT-INITIAL-ALLTIME | REJECTED | initial compatibility is not all-time compatibility |

| SHORTCUT-CP-ABSORPTION | REJECTED | C_P remains separate from C_eff |


## 37. Selection criteria

| Criterion | Meaning |

| --- | --- |

| SC-1 | ontological economy |

| SC-2 | regional fidelity |

| SC-3 | carrier completeness |

| SC-4 | functional well-definedness |

| SC-5 | data economy |

| SC-6 | dynamical extensibility |

| SC-7 | falsifiability |

| SC-8 | honest target resolution |

| SC-9 | no hidden spectral assumptions |

| SC-10 | observational firewall |


## 38. Comparative extension burden and provisional selection

| Property | S1 | H1 |
| --- | --- | --- |
| Carrier | compact smooth reference class | compact piecewise reference class |
| Added structure | partition profile and metric extensions | interface and transmission law |
| Surface data | not required at finite smoothness | potentially required |
| Regional identity | weighted | piecewise explicit |
| Elliptic burden | normalized scalarization and unresolved regional Green branches | coupled transmission |
| Missing dynamics | temporal operator transport, effective/constitutive/compatibility | interface/effective/constitutive/compatibility |
| Project role | provisional author-selected baseline | project-governance sharp comparator |

S1 is retained as a provisional baseline by a convention-dependent project choice. The available equations do not prove that its unsupported extension burden is lower than H1 under every admissible weighting of the selection criteria. H1 remains the required adversarial comparator and can reopen the selection under FS10.

## 39. Full G0–G15 gate audit

| Gate | S1 | H1 | M1 | L1 |
| --- | --- | --- | --- | --- |
| G0 | PASS_UNDER_EXPLICIT_ASSUMPTIONS | PASS_UNDER_EXPLICIT_ASSUMPTIONS | PASS_UNDER_SELECTED_BRANCH | PASS_LOCAL_ONLY |
| G1 | PASS_AT_CLASS_LEVEL_ONLY | PASS_AT_CLASS_LEVEL_ONLY | PASS_UNDER_SELECTED_BRANCH | PASS_LOCAL_ONLY |
| G2 | DEFINED_BUT_UNDERDETERMINED | PASS_UNDER_EXPLICIT_ASSUMPTIONS | PASS | PASS_LOCAL_ONLY |
| G3 | PASS_AT_TEMPLATE_LEVEL | PASS_AT_TEMPLATE_LEVEL | PASS_AT_TEMPLATE_LEVEL | PASS_LOCAL_ONLY |
| G4 | DEFINED_BUT_UNDERDETERMINED | DEFINED_BUT_UNDERDETERMINED | PASS_UNDER_SELECTED_BRANCH | PASS_LOCAL_ONLY |
| G5 | DEFINED_BUT_UNDERDETERMINED | PASS_UNDER_LAGRANGIAN_RESTRICTION | PASS_UNDER_SELECTED_BRANCH | DEFINED_BUT_UNDERDETERMINED |
| G6 | PASS_UNDER_SELECTED_PARTITION_LAW | PASS_UNDER_SELECTED_BRANCH | PASS_UNDER_SELECTED_BRANCH | DEFINED_BUT_UNDERDETERMINED |
| G7 | FAIL_PROPAGATION_NOT_CLOSED | FAIL_PROPAGATION_NOT_CLOSED | FAIL_PROPAGATION_NOT_CLOSED | DEFINED_BUT_UNDERDETERMINED |
| G8 | DEFINED_BUT_UNDERDETERMINED | DEFINED_BUT_UNDERDETERMINED | DEFINED_BUT_UNDERDETERMINED | DEFINED_BUT_UNDERDETERMINED |
| G9 | PASS_UNDER_HOMOGENEOUS_CLOCK_RESTRICTION | PASS_UNDER_HOMOGENEOUS_CLOCK_RESTRICTION | PASS_UNDER_SELECTED_BRANCH | DEFINED_BUT_UNDERDETERMINED |
| G10 | PASS_AT_POLICY_LEVEL | PASS_AT_POLICY_LEVEL | PASS_AT_POLICY_LEVEL | PASS_AT_POLICY_LEVEL |
| G11 | PARTIAL_CONDITIONAL_ONLY | PARTIAL_CONDITIONAL_ONLY | PARTIAL_REDUCED_FORWARD_ONLY | PARTIAL_CONDITIONAL_ONLY |
| G12 | FAIL_NOT_ESTABLISHED | FAIL_NOT_ESTABLISHED | NOT_APPLICABLE | NOT_APPLICABLE_GLOBALLY |
| G13 | SENSITIVITY_REQUIRED | NOT_APPLICABLE | FAIL_NOT_ESTABLISHED | FAIL_NOT_ESTABLISHED |
| G14 | PASS | PASS | PASS | PASS |
| G15 | FAIL_NOT_ESTABLISHED | FAIL_NOT_ESTABLISHED | FAIL_NOT_ESTABLISHED | FAIL_NOT_ESTABLISHED |

For S1, G2, G4 and G5 are deliberately downgraded after the independent audit. No aggregate pass count substitutes for the load-bearing failures and underdetermined gates.

## 40. Adversarial objections

| ID | Required challenge | Status |

| --- | --- | --- |

| AA-01 | preserve frozen Phase 1E-D boundary | MANDATORY |

| AA-02 | do not classify generic functional analysis as current Timescape machinery | MANDATORY |

| AA-03 | component counts are not ranks | MANDATORY |

| AA-04 | definitions and constraints are not evolution equations | MANDATORY |

| AA-05 | metric convexity requires common tangent space and positive extensions | MANDATORY |

| AA-06 | audit metric-extension sensitivity | MANDATORY |

| AA-07 | distinguish imposed from derived K_f=0 | MANDATORY |

| AA-08 | background lapse is not perturbative lapse | MANDATORY |

| AA-09 | state Green domains, codomains and kernels | MANDATORY |

| AA-10 | do not assume [L_C,M_chi]=0 | MANDATORY |

| AA-11 | do not identify regional and carrier modes | MANDATORY |

| AA-12 | retain C_eff | MANDATORY |

| AA-13 | retain separate C_P | MANDATORY |

| AA-14 | initial compatibility is not propagation | MANDATORY |

| AA-15 | no unsupported inverse claim | MANDATORY |

| AA-16 | M1 is not full field | MANDATORY |

| AA-17 | L1 is not global | MANDATORY |

| AA-18 | auxiliary branch must transfer rather than replace regional state | MANDATORY |

| AA-19 | preserve observational firewall | MANDATORY |

| AA-20 | preserve prototype firewall | MANDATORY |


## 41. Falsification matrix FS1–FS10

| ID | Name | Condition | Consequence |

| --- | --- | --- | --- |

| FS1 | Volume-fraction inconsistency | K_f(t) cannot be made zero for admissible metric extensions | reject or modify S1 |

| FS2 | Carrier-metric failure | no positive regular h_C satisfying regional restrictions | reject S1 |

| FS3 | Unbounded lifting | E_r is not bounded in selected spaces | reject concrete realization |

| FS4 | Uncontrolled partition dependence | equally admissible partitions yield incompatible targets | reopen selection |

| FS5 | Regional cancellation kernel | load-bearing overlap of Ran(T_w) and Ran(T_v) | revise target or inverse claims |

| FS6 | Homogeneous-clock insufficiency | spatial clock gradients are unavoidable | reject S1 clock branch |

| FS7 | Effective-sector no-go | no admissible T_eff exists | reject or redesign S1 |

| FS8 | Compatibility no-go | R_T cannot be controlled | no forward-closure claim |

| FS9 | Constraint failure | CGI source identities are not preserved | reject realization |

| FS10 | Sharp-comparator dominance | H1 closes with lower burden and less arbitrariness | reopen primary selection |


## 42. Branchwise deficit vector

| Packet | N_undef | Delta_dyn | Delta_IC | Delta_BC | Delta_match | Delta_emp |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | LOWER_BOUND | LOWER_BOUND | LOWER_BOUND | BIFURCATED | NOT_COUNTABLE_BEFORE_CONCRETE_OPERATOR_LINEARIZATION | NOT_APPLICABLE |
| H1 | LOWER_BOUND | LOWER_BOUND | LOWER_BOUND | BIFURCATED | NOT_COUNTABLE_BEFORE_CONCRETE_OPERATOR_LINEARIZATION | NOT_APPLICABLE |
| M1 | LOWER_BOUND | LOWER_BOUND | LOWER_BOUND | BIFURCATED | NOT_COUNTABLE_BEFORE_CONCRETE_TRANSFER | BIFURCATED |
| L1 | LOWER_BOUND | LOWER_BOUND | LOWER_BOUND | BIFURCATED | NOT_COUNTABLE_BEFORE_CONCRETE_TRANSFER | NOT_APPLICABLE |

For S1, the carrier outer boundary is not applicable, but regional elliptic boundary or decay data remain unresolved. No universal numerical vector is assigned.

## 43. Cumulative decision ledger

| Phase | Range | Status | Summary |

| --- | --- | --- | --- |

| P0 | P0-D01..P0-D20 | PARTIALLY_RECONSTRUCTED_FROM_CURRENT_CONVERSATION | R1-R8 are heterogeneous layers; forward existence and inverse injectivity are separate; R8 may be valid only for an explicit reduced target; no family selected at P0 |

| P1 | P1-D21..P1-D38 | AVAILABLE_IN_CURRENT_CONVERSATION | Common Realization Record mandatory; compound candidates CR-1..CR-7 retained; G2 not concretely passed; no realization selected |

| P2 | exact IDs unavailable | UNRESOLVED_EXTERNAL_DEPENDENCY | geometry, embedding and clock branches were classified and inherited by P3 |

| P3 | P3-D39..P3-D58 | AVAILABLE_IN_CURRENT_CONVERSATION | ambient/domain/admissible spaces separated; zero-mode policy load-bearing; elliptic classes E1..E7 retained |

| P4 | P4-D59..P4-D81 | AVAILABLE_IN_CURRENT_CONVERSATION | smooth and sharp operator templates defined; SL0..SL5 required; invalid shortcuts rejected |

| P5 | P5-D82..P5-D104 | AVAILABLE_IN_CURRENT_CONVERSATION | data categories separated; compatibility manifold defined; G7 fails; regional-to-GM forward not closed |

| P6 | P6-D105..P6-D132 | AVAILABLE_IN_CURRENT_CONVERSATION | forward/inverse distinctions fixed; moment and finite truncation noninjectivity proved; shortlist normalized |

| P7 | P7-D133..P7-D163 | AVAILABLE_IN_CURRENT_CONVERSATION | S1 selected conditionally; H1/M1/L1 mandatory comparators; no packet prototype-ready |

| P8 | P8-D164..P8-D179 | FINAL | deliverable and audit specifications frozen; report-only activity approved; implementation not authorized |


The exact P2 decision wording was not present in the supplied artifact snapshot. It is marked as an unresolved external dependency rather than reconstructed inventively.

## 44. Formal conclusions

| ID | Classification | Conclusion |
| --- | --- | --- |
| FC-1E-E-001 | VERIFIED_FROM_PRIMARY_SOURCE | Each region has the first-order \(\Delta_r,Z_r\) system and rank two. |
| FC-1E-E-002 | VERIFIED_FROM_PRIMARY_SOURCE | Current Timescape does not supply the complete 3D common carrier and transfer package. |
| FC-1E-E-003 | DERIVED_FROM_VERIFIED_DEFINITIONS | R1–R8 occupy carrier, formulation, operator, scale and target layers rather than one flat alternative set. |
| FC-1E-E-004 | CONVENTION_DEPENDENT | S1 is retained conditionally as the provisional author-selected baseline; no minimum-extension theorem over H1 is claimed. |
| FC-1E-E-005 | DERIVED_FROM_VERIFIED_DEFINITIONS | Exact topology, metric extensions, embeddings, regional elliptic realization, partition profile, normalized carrier scalarization, \(\mathcal T_{\rm eff}\) and regional reconstruction of \(C_P\) remain unselected. |
| FC-1E-E-006 | CONVENTION_DEPENDENT | H1 is retained by project governance as the sharp adversarial comparator. |
| FC-1E-E-007 | SYMBOLICALLY_VERIFIED | A finite-dimensional linear moment target has a nontrivial field kernel. |
| FC-1E-E-008 | DERIVED_FROM_VERIFIED_DEFINITIONS | L1 provides only a local GM patch state without global gluing. |
| FC-1E-E-009 | SYMBOLICALLY_VERIFIED | All regional perturbations lie in the kernel of a map explicitly defined to depend only on background inputs. |
| FC-1E-E-010 | DERIVED_FROM_VERIFIED_DEFINITIONS | \(C_{\rm eff}\) is load-bearing and cannot be dropped by component counting. |
| FC-1E-E-011 | DERIVED_FROM_VERIFIED_DEFINITIONS | The inherited clean-comoving closure is \(C_P=\mathscr W-3\mathscr Q=0\); it remains separate from \(C_{\rm eff}\), while regional reconstruction is missing. |
| FC-1E-E-012 | SYMBOLICALLY_VERIFIED | Initial compatibility propagates only if transfer residuals and the exact \(+C_P/4\) forcing in \(\dot C_Z\) are controlled. |
| FC-1E-E-013 | DERIVED_FROM_VERIFIED_DEFINITIONS | Three named mismatch blocks do not determine Fréchet rank. |
| FC-1E-E-014 | DERIVED_FROM_VERIFIED_DEFINITIONS | Regional inverse kernels, lifting kernels, range overlap and scalarization prevent an inverse verdict. |
| FC-1E-E-015 | DERIVED_FROM_VERIFIED_DEFINITIONS | Mode mixing is permitted and diagonal mode matching is not a default. |
| FC-1E-E-016 | DERIVED_FROM_VERIFIED_DEFINITIONS | Partition-value convergence alone does not establish operator or target convergence. |
| FC-1E-E-017 | DERIVED_FROM_VERIFIED_DEFINITIONS | Effective transfer, regional reconstruction of \(C_P\), temporal operator transport and compatibility dynamics remain missing. |
| FC-1E-E-018 | DERIVED_FROM_VERIFIED_DEFINITIONS | No packet has concrete geometry, closed compatibility and forward well-posedness. |
| FC-1E-E-019 | DERIVED_FROM_VERIFIED_DEFINITIONS | The S1 output remains a candidate carrier scalar representation intended for the GM target; observational mappings remain outside scope. |
| FC-1E-E-020 | NOT_APPLICABLE | Human authorization governs artifact scope and does not constitute a scientific derivation. |

The inventory JSON contains the full nine-field record for every conclusion.

## 45. Final selection record

| Field | Value |
| --- | --- |
| primary_realization_id | S1-LAGRANGIAN-SMOOTH-COMPACT-MEANZERO |
| selection_level | ARCHITECTURE_CLASS |
| selection_basis | CONVENTION_DEPENDENT_PROVISIONAL_AUTHOR_BASELINE |
| primary_verdict | PRIMARY_REALIZATION_CLASS_SELECTED_CONDITIONALLY |
| target_scope | GLOBAL_CANDIDATE_CARRIER_SCALAR_REPRESENTATION_FOR_GM_TARGET |
| minimum_extension_claim | NOT_JUSTIFIED |
| overall_verdict | PARTIAL_REALIZATION_DEFICITS_REMAIN |
| theory_consequence | NEW_DYNAMICS_REQUIRED |
| readiness | REPORT_ONLY_MUST_CONTINUE |
| mandatory_comparators | ["H1-LAGRANGIAN-SHARP-COMPACT-TRANSMISSION", "M1-FINITE-CARRIER-MOMENTS", "L1-LOCAL-WKB-CARRIER-PATCH"] |
| extension_only | X1-AUXILIARY-FULL-FIELD-EXTENSION |
| implementation_authorization | NOT_GRANTED |
| prototype_authorization | NOT_GRANTED |

## 46. Implementation boundary and permitted next phase

The present approval authorizes the two report artifacts only. It does not authorize scientific runtime implementation, prototype construction, source/test changes, a commit, tag, push or pull request. The next scientifically permitted activity is an independent adversarial audit of these deliverables in a separate context.

```text
PROTOTYPE_AUTHORIZATION: NOT_GRANTED
IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

---

## Validation summary

- JSON parse, required-key, ID, vocabulary, formal-conclusion-field and cross-file-verdict checks are executed by the artifact build script.

- The sandbox is not a Git checkout; `git diff --check`, branch/ref verification and the repository test suite are therefore not claimed.

- Only the Markdown and JSON files are created in the sandbox `reports` directory.
