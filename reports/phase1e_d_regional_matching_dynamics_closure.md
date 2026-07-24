# Phase 1E-D - Regional Wall/Void Perturbation and GM Formal Matching-Domain Dynamics

## 1. Executive verdict

**Overall verdict: `PARTIAL_REGIONAL_DYNAMICS_REMAIN_UNDERDETERMINED`.**

The intrinsic \(k\ne0\) scalar dust problem in each exact regional FLRW
geometry is closed by two first-order variables, \((\Delta_r,Z_r)\), and two
evolution equations. A five-component regional-effective state is a formal
candidate only: current Timescape sources do not supply the common carrier,
clock maps, pullbacks, smoothing or interface realization, Green operators,
boundary data, and all-time constitutive input required to close it.

The proposed two-equation compatibility propagation was incomplete: it omitted
the effective-density mismatch \(C_{\rm eff}\). The corrected propagation has
three named mismatch components \(C_\Delta,C_Z,C_{\rm eff}\), while \(C_P\)
is a separate constitutive residual. Their independent operator rank is
`RANK_NOT_COUNTABLE_BEFORE_TRANSFER_SELECTION`; the number of components is
not a rank proof. Inverse uniqueness and nonuniqueness are both unresolved
before a transfer and its admissible spaces are selected.

Subordinate results are
`INTRINSIC_REGIONAL_BULK_EXACTLY_CLOSED`,
`FORWARD_REGIONAL_EFFECTIVE_MODEL_REQUIRES_IMPORTED_REALIZATION`,
`REQUIRED_PACKAGE_CATEGORIES_IDENTIFIED`,
`FORMAL_PACKAGE_SKELETON_SPECIFIED`,
`CONCRETE_REALIZATION_NOT_SELECTED`, and
`INVERSE_UNIQUENESS_UNRESOLVED_BEFORE_TRANSFER_SELECTION`.

**Implementation readiness: `REPORT_ONLY_MUST_CONTINUE`.**

**Implementation authorization: `NOT_GRANTED`.**

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 2. Scope and preservation statement

This is an equation-level design audit. It creates no scientific runtime,
prototype, fit, data product, or observational bridge. No equation in source
code is changed. Candidate A remains externally anchored, conditional,
clean-system-only, non-observational, and not \(f\sigma_8\).
`derived_4_10` and `printed_4_15` remain explicit branches without a default;
the D3 verdict remains `RESOLVED_DERIVED_4_10`.

The GM zero-measure domain is not identified with finite infinity. Radial-null
matching is not a spatial pullback. \(k_{\rm code}\), regional spectral labels,
wall matter velocity, tracer velocity, and \(Z\) remain distinct.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 3. Repository preflight

The local branch `phase-1e-d-regional-matching-dynamics-design` was created at
unchanged HEAD `fcbf9c29a28c586044150e6910e1637bc3f6975b`; its parent is
`8634f14a35c22983413672075fa7f37f03fd663d`. The annotated tag
`phase-1e-c-perturbed-dressed-geometry-transfer-closure-v1` has object
`0a6dbe6ac27991d6119a4ebc4e84e4a005f3d988` and peels to HEAD. Frozen
Phase 1E-C hashes are:

- Markdown: `522a77de97d06c90323d06f597f4e2b1be168da9fa7efd3965f29268e085c4e4`;
- JSON: `2ca8a47f697eb6ea6a7ed3abefe4e64d0b76cda2923c132878d81616c519f8c7`.

The ignored upstream clone is detached and clean at
`590c6fd5332acb15f5683ebf392a0d7ce54983c5`; its notebook hash is
`86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a`.
The artifact-free frozen tree produced `350 passed, 29 skipped`: 29 counts
skipped tests, not files. Restoration regenerated these ten ignored files
byte-identically by existing canonical procedures:

- `artifacts/independent/phase1c_b2_convergence.json`;
- `artifacts/independent/phase1c_b2_d2_d3_factorial.json`;
- `artifacts/independent/phase1c_b2_figure_endpoints.json`;
- `artifacts/independent/phase1c_b2_oracle_comparison.json`;
- `artifacts/independent/phase1c_b2_scenario_effects.json`;
- `artifacts/independent/phase1d_b_growth_validation.json`;
- `artifacts/independent/phase1d_d_anchored_density_growth_validation.json`;
- `artifacts/upstream/oracle_background.json`;
- `artifacts/upstream/oracle_barotropic_perturbations.json`;
- `artifacts/upstream/oracle_clean_perturbations.json`.

The earlier eight-path summary was incomplete because it omitted the
convergence and D2/D3-factorial files. With all ten restored, the full baseline
is `379 passed` in both Python 3.14.3 and Python 3.11.9. No artifact or tracked
file is changed by this correction.

Primary classification: `NUMERICALLY_CORROBORATED`.

## 4. Frozen-result boundary

The inherited verdict is `PARTIAL_CLOSURE_NEW_DYNAMICS_REQUIRED`, not
`NOT_DERIVABLE_FROM_CURRENT_TIMESCAPE_THEORY`. Phase 1E-C supplied a historical
single-vector estimate, but its first component cannot be retained as a
universal Phase 1E-D assessment: the present theory does not define the carrier,
embeddings, transfer, spaces, or boundary realization. Section 32 replaces the
historical estimate with a branchwise assessment.

\[
 C:\quad\hbox{regional wall/void perturbations plus GM formal-domain dynamics},
\]
This correction preserves the frozen report as evidence while correcting the
Phase 1E-D inference drawn from it.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 5. Scientific question and decision rules

Closure requires four independent achievements: regional bulk propagation;
partition transport; a geometrically defined regional-to-GM map; and finite
initial, elliptic, boundary, and compatibility data. Definitions, gauge
conditions, algebraic closures, and transfer normalizations do not count as
evolution equations. Unknown ranks are reported as `LOWER_BOUND`,
`NOT_COUNTABLE_BEFORE_BRANCH_SELECTION`, or `BIFURCATED`.

A generic-GR construction is retained only when it varies an existing
Timescape/GM object or is explicitly labelled imported or optional. A failure
of a falsification gate changes the branch classification or overall verdict.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 6. Evidence and classification policy

Material conclusions use exactly one of the prescribed evidence tokens.
Frameworks use exactly one of `CURRENT_TIMESCAPE_MACHINERY`,
`COMPATIBLE_IMPORTED_DYNAMICS`, `OPTIONAL_MODEL_EXTENSION`, or
`INAPPLICABLE`. Extracted PDF text was used for navigation. The image-only DBE
and BDE scans were rendered and visually read; equation signs, indices, and
numbers were not taken from OCR. Symbolic zero residuals corroborate only the
encoded identities and assumptions.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 7. Primary-source inventory

All retained PDFs are in external scratch, not the repository.

| ID | Version and inspected scope | SHA-256 | Role/outcome |
|---|---|---|---|
| GM | Galoppo & Mourier, arXiv:2511.17160v2; PDF pp. 4-25, 43-44, 52-53; Eqs. (2.2), (2.12)-(2.24), (3.5)-(3.17), (4.5)-(4.23), (5.1)-(5.7) | `856bd78db8f86e46c0f5d21414ad0c1d136b176c6ac1b45418dbeebc38e920dd` | CGI, effective source, formal domain |
| W07 | Wiltshire, arXiv:0709.0732v2; pp. 1-4; Eqs. (1)-(8), (19)-(22) | `3abcc64ad95b95cf655f687515c8d85f38d6d0bfcebec1e0133a460b425db04f` | two-scale background |
| W08 | Wiltshire, arXiv:0809.1183v2; pp. 7-12; Eqs. (10)-(14), (19)-(27) | `51b189b832c8bfbc2c5d6d6af92efa61885ebff39fbbcd0415cfea8651787078` | regional clocks and frames |
| W09 | Wiltshire, arXiv:0909.0749v2; pp. 3-8, 14; Eqs. (6)-(28), (36)-(38), (51) | `e37321e9d6021c6f5eb6bc5084ad331f4fca9dc0bc426097d1c5ce5ce7b2a8aa` | finite infinity and dressed radial-null construction |
| BAL13 | Balasin, arXiv:1310.3124v1; all 15 pages; Eqs. (3)-(5), (7), (9), (11) | `ef19efcd5b3c3637c6363dea58101daa1cdd69abbc550f431a924c0a3808ef0a` | generic conformally-static comparator |
| NW15 | Nazer & Wiltshire, arXiv:1410.3470v3; Secs. II-III; Eqs. (3)-(7) | `e7d695d58b0d6b3c5b3924f07aaaca700d5a387c9d6178cf1a1c5145fff62c93` | auxiliary-FLRW CMB matching only |
| B00 | Buchert, arXiv:gr-qc/9906015v2; pp. 2-7; Eqs. (5), (9), (10a-c), (13a) | `13f41a52f6e36fdbd4be39d570ecd728d921b5c20aeb04f3c74264347b69f36d` | dust averaging |
| B01 | Buchert, arXiv:gr-qc/0102049v2; pp. 5-8; Eqs. (7)-(12g) | `5db93c67ff7398ebd4f51647ab26538dc5163e09053ee1e19f7b270b88ca1b5b` | lapse-dependent perfect-fluid averaging |
| BC-REG | Buchert & Carfora, arXiv:gr-qc/0210037v2; pp. 5-16, 19-36, 44-47 | `8f2d11f71b17ab9263e203fbd01ef4756f8e41cc39d8fa00b756782e3fa8f568` | regional smoothing and scale dependence |
| BC-DRESS | Buchert & Carfora, arXiv:gr-qc/0210045v1; pp. 1-4 | `f3d867ac3eecb22a309b454e27d76dbe5cae2ccdab6f5e6ed1df1b8c02afaabf` | bare/dressed parameter comparator |
| RB12 | Roy & Buchert, arXiv:1202.5766v2; pp. 2-10; Eqs. (4)-(10) | `fbeeaea6a26bee7453d9441d9e7e91f7dce82e8262f00d7c13055a8338f61b88` | exact deviations on an averaged domain |
| BMR20 | Buchert, Mourier & Roy, arXiv:1912.04213v2; pp. 4-18, 25-40, 51-63 | `672efe5246aa081fe2afc4048b8ac4e6d55cc77989b1cbfbefaf000b7962aabd` | lapse, shift, tilt, comoving maps, boundaries |
| MH24 | Mourier & Heinesen, arXiv:2401.09170v2; pp. 2-18, 26-30; Eqs. (2.1)-(3.31) | `cb5596800bc79430f82a39fffe6f7186dc4b93b755ecf9100d669c7e0d63931d` | foliation and boundary dependence |
| DBE92 | Dunsby, Bruni & Ellis, *ApJ* 395 (1992) 54-74, DOI `10.1086/171630`; journal pp. 55-61; Eqs. (15), (18)-(21), (25)-(55) | `3a082920b358872ec64a3706001e1a10a61a51f2e5140cf29662aa1a04b72f20` | image-only CGI scan; title, authors, volume, starting page, and DOI verified against the Crossref publisher deposit |
| BDE92 | Bruni, Dunsby & Ellis, *ApJ* 395 (1992) 34-53, DOI `10.1086/171629`; journal pp. 38-45, 48; Eqs. (14)-(16), (24)-(29), (40), (44)-(48), (61), (63), (68)-(74), (119)-(120) | `eaa273fa5982689cd55eaba7530103e8e9d77199d4b34d3d173c1e9201075b6c` | image-only scalar/harmonic scan; title, authors, volume, starting page, and DOI verified against the Crossref publisher deposit |
| MMV07 | Mars, Mena & Vera, arXiv:0704.0078v1, CQG 24 (2007) 3673, DOI 10.1088/0264-9381/24/14/008; pp. 1-6; Eqs. (1)-(4) | `f172547086325c5e61e567efc466a8ae357bdc5e4fe7e01adb6008f9a93bde55` | first-order matched-spacetime gauge theory |
| KIR03 | U. Kirchner, arXiv:gr-qc/0312003v1; pp. 1-9, 16-18; Eqs. (4)-(5), (11)-(39), (51)-(55) | `b3d699d997e4c31f289e019be3da4b1b91bf50add3a4e499b7a6ac3234c9ac19` | spherical timelike FLRW-FLRW junctions |
| BO12 | Buchert & Ostermann, arXiv:1203.6263v2, PRD 86 (2012) 023520; Secs. II-IV | `141762425f3b46897dce89b934ebfd7dc06af12e407b70019a9eec91c1920958` | relativistic Lagrangian comparator |
| KW06 | Kreiss & Winicour, arXiv:gr-qc/0602051v3, CQG 23 (2006) S405; pp. 1-16 | `4634c3a0cd350a9f659b23bf735c7a5dc97582a3a028a0624a4d654738c5964f` | constraint-preserving NR-IBVP comparator |

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 8. Exact GM-domain source audit (H-D0)

GM PDF p. 22 states that walls and voids are distinct domain classes, each
idealized by dust FLRW geometry, and that a third domain type “with zero volume
measure” is formally introduced as a boundary for matching within one
spacetime. It immediately says that this domain remains unspecified. GM gives
no intrinsic dimension, regularity, topology, causal character, normal,
induced metric, extrinsic curvature, transport law, embedding, or surface
stress tensor.

Therefore:

`FORMAL_ZERO_MEASURE_PARTITION_BOUNDARY_GEOMETRY_UNSPECIFIED`.

Zero spatial-volume measure does not imply a regular codimension-one Darmois
hypersurface. H-D0 is confirmed.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 9. Candidate-framework matrix

| Framework | Source; supplied objects/equations/constraints | Gauge/boundary structure; GM/Timescape relation | Missing input, ontology risk | Classification and role |
|---|---|---|---|
| regional scalar FLRW dust | GM (2.2), (2.20)-(2.23); DBE (32)-(34) | dust-frame CGI; curvature in constraints/spectrum | regional-to-common maps and clocks | `COMPATIBLE_IMPORTED_DYNAMICS`; selected bulk |
| covariant \(1+3\) perturbations | GM Secs. 2, 4; DBE/BDE | covariant observer frame; CGI scalarization | regional localization | `COMPATIBLE_IMPORTED_DYNAMICS`; frozen GM target language only |
| metric/ADM scalar perturbations | BDE; BMR Sec. 2 | spacetime gauge plus lapse/shift constraints | gauge and boundary embedding | `COMPATIBLE_IMPORTED_DYNAMICS`; cross-check |
| first-order matched spacetime | MMV07 (1)-(4) | spacetime and hypersurface gauge; non-null boundary deformation \(Q^\pm,T^\pm\) | GM domain must first be codimension one | `OPTIONAL_MODEL_EXTENSION`; C-JUNC only |
| Darmois matching | MMV07 (1)-(4); KIR03 | equality of first and second forms, no shell | causal character and embeddings | `OPTIONAL_MODEL_EXTENSION`; not assumed |
| Israel/Lanczos thin shell | KIR03 (10)-(22), (27) | surface density/pressure and shell equation of state | new surface source | `OPTIONAL_MODEL_EXTENSION`; C-SHELL |
| Buchert dust averaging | B00 (9), (10), (13) | comoving flow tube, compact spatial domain | localization of domain averages | `CURRENT_TIMESCAPE_MACHINERY`; selected |
| Buchert-Carfora smoothing/dressing | BC-REG/BC-DRESS | Ricci-flow smoothing and scale-dependent regional averages | flow, scale, topology | `OPTIONAL_MODEL_EXTENSION`; smoothing-model comparator |
| Roy-Buchert deviations | RB12 (4)-(10) | exact deviations about domain averages | not a wall/void matching map | `COMPATIBLE_IMPORTED_DYNAMICS`; falsification comparator |
| BMR general-fluid averaging | BMR20 Secs. 2-4 | arbitrary lapse/shift/tilt; comoving-to-reference map and boundary terms | many additional fields | `COMPATIBLE_IMPORTED_DYNAMICS`; clock/map audit |
| relativistic Lagrangian theory | BO12 Secs. II-IV | coframes and Lagrange-Einstein constraints | tensor state and initial coframes | `OPTIONAL_MODEL_EXTENSION`; not minimum |
| multi-domain interfaces | KIR03 Sec. 5 | spherical timelike shell/transition models | symmetry, EOS, shell/transition source | `OPTIONAL_MODEL_EXTENSION`; junction comparator |
| numerical-relativity IBVP | KW06 | harmonic metric, constraint-preserving Sommerfeld-type BC | full metric PDE and boundary gauge | `INAPPLICABLE`; well-posedness comparator only |
| finite infinity | W09 (6), (22)-(28) | operational wall boundary and radial-null dressing | no derivation equating it to GM domain | `OPTIONAL_MODEL_EXTENSION`; C-FI |
| auxiliary-FLRW CMB matching | NW15 Sec. III | early-time reference-model matching | not a regional perturbative transfer | `INAPPLICABLE`; prevents category error |

The selected role is C-AVG, not a generic junction construction.

`TARGET_STATE_STATUS` and `REGIONAL_DYNAMICS_STATUS` are distinct. The frozen
GM variables and equations are current target language. Regional wall/void
perturbation equations are compatible imports; a carrier, embeddings,
pullbacks, kernels, Green operators, or smoothing realization is absent from
current regional Timescape machinery. Generic machinery is not reclassified as
current merely because it can map into GM variables. Finite infinity remains a
current background concept but its use as the GM perturbative interface is an
`OPTIONAL_MODEL_EXTENSION`.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 10. Domain-type gate (H-D2)

`C-AVG` is retained as the least-structure formal design route: a comoving
regional partition, compatible imported regional CGI dust dynamics, and a
still-undefined localized averaging transfer. It does not assign a causal
normal or extrinsic curvature to the unspecified GM domain, and it is not a
current-theory transfer realization.

`C-JUNC` is conditional on a regular non-null codimension-one worldtube;
`C-SHELL` additionally introduces \(S_{ij}\); `C-TRANS` introduces a
finite-thickness non-FLRW field region; and `C-FI` requires an explicit proof
identifying finite infinity with the GM domain. These are optional extensions,
not silent completions of C-AVG.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 11. Background junction-consistency gate (H-D1)

Kirchner assumes two spherically symmetric FLRW regions, a timelike spherical
junction, perfect fluids with constant \(\gamma\)-law equations of state
\(p=(\gamma-1)\rho\), \(\gamma\in(2/3,2]\), and Friedmann evolution with
constant curvature and cosmological constant parameters. If the junction is
comoving on both sides, \(\dot\alpha_\pm=0\), the first-form condition gives

\[
 a_+(t)=\frac{f_-(\alpha_-)}{f_+(\alpha_+)}\,a_-(t)
 \qquad\text{[Eq. (55) of arXiv:gr-qc/0312003v1].}
\]

The ratio is constant. Section 5.3 proves that two such \(\gamma\)-law FLRW
solutions with the same Hubble history are identical in \(\gamma,\Lambda\),
curvature, and density constant (up to the now-fixed scale normalization).
Thus an exact *distinct* comoving FLRW-FLRW matching is inconsistent under
these assumptions. The conclusion follows from the induced geometry and is
independent of whether a shell is present; no-shell Darmois matching is
therefore also excluded in this narrow branch.

This is not a no-go for noncomoving, nonspherical, finite-thickness,
non-\(\gamma\)-law, averaged, or non-FLRW interfaces.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 12. Regional variable ontology

| Sector | Variables | Status and role |
|---|---|---|
| frozen background | \(a_D,a_w,a_v,f_v,\bar\gamma_w,H_D,H_w,H_v,\bar Q_D,\bar W_D\) | background-defined |
| regional bulk | \(\Delta_w,Z_w,\Delta_v,Z_v\) | independent \(k\ne0\) dynamic CGI scalars |
| regional derived geometry | \(\mathscr R_r=-(4/3)\Theta_r Z_r+16\pi G\rho_r\Delta_r\) | Hamiltonian constraint |
| homogeneous tangent | \(\delta K_r,\delta f_{v0}\), tracker/density/normalization tangents | excluded from R-INH; optional R-0 |
| partition | \(\delta f_v,\mathcal F_v,\Xi_r,\mathcal E_{\Xi r}\) | one state plus required clock/expansion transfer |
| common carrier | \((\Sigma_D,h_D,\mu_D),\omega_w,\omega_v\) | required category; not defined in present theory |
| transfer/elliptic | \(\phi_r,J_r,S_\ell,\Pi_{0,r},G_r,T_r\) | formal categories/pattern only; existence not established |
| effective geometry | \(\mathscr Q,\mathscr W,\widehat\Delta_{\rm eff},\widehat{\widetilde P}_{\rm eff}\) | algebraically derived after localization |
| GM target | \(\Delta_d,Z,\Delta_{\rm eff}\) | frozen target state |
| constraints | \(C_\Delta,C_Z,C_{\rm eff}\) | compatibility state |
| closure | \(C_P=\mathscr W-3\mathscr Q\) | enforced constitutive closure |
| empirical | bias, tracer velocity, AP/RSD, likelihood data | out of scope and undefined |

Lapse objects are distinct: background \(\bar\gamma_w=dt/d\tau_w\);
\(\delta\bar\gamma_w\); averaging-foliation \(\delta N_D\); regional
\(\delta N_w\); conceptual local \(\gamma(\tau,\mathbf x)\), not defined by
Timescape; BMR Lorentz factor \(\gamma_{\rm BMR}=-u\cdot n\); ADM lapse
\(N_{\rm ADM}\); and clock maps \(\chi_r:t\mapsto\tau_r\). No equality among
them is assumed.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 13. Regional scalar-state derivation (H-D3)

For one dust FLRW region \(r\), in its comoving geodesic proper-time frame,
GM defines

\[
\Delta_r=\frac{a_r^2}{\rho_r}D_r^2\rho_r,\qquad
Z_r=a_r^2D_r^2\Theta_r
\quad\text{[Eqs. (2.2), (2.20)-(2.21) of arXiv:2511.17160v2].}
\]

Set \(w=P=V=F=0\) in GM (2.22)-(2.23), or in DBE (32)-(33).
With \(\Theta_r=3H_r\),

\[
\frac{d\Delta_r}{d\tau_r}=-Z_r,\qquad
\frac{dZ_r}{d\tau_r}=-2H_rZ_r-4\pi G\rho_r\Delta_r .
\]

Therefore \(N_{\rm state,r}=2\), \(\operatorname{rank}E_r=2\), and two
initial functions are required. Eliminating \(Z_r\) gives

\[
\frac{d^2\Delta_r}{d\tau_r^2}
+2H_r\frac{d\Delta_r}{d\tau_r}-4\pi G\rho_r\Delta_r=0.
\]

Curvature affects background coefficients, spatial constraints, and harmonic
spectra, but not this dust-frame scalar propagation pair. This is regional
linear dust dynamics, not the global Timescape Mészáros approximation.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 14. Heuristic metric/gauge/constraint cross-check

`HEURISTIC_METRIC_CROSS_CHECK`: listing four scalar metric variables plus
density and velocity, then informally subtracting two scalar gauge directions
and two scalar Einstein constraints, is a consistency illustration only. It is
not an independent state-count proof: configuration-space and phase-space
variables may otherwise be mixed; Einstein equations need not be algebraically
independent; constraint propagation is separate; and gauge generators and
gauge conditions must be counted in a specified formulation. The exact
two-state, rank-two result comes from the independently derived CGI regional
system in Section 13. The linear Hamiltonian constraint obtained by varying GM
(2.13) is

\[
\mathscr R_r:=a_r^2D_r^2\delta{}^{(3)}R_r
=-\frac43\Theta_r Z_r+16\pi G\rho_r\Delta_r .
\]

Within a fully specified scalar metric formulation, shear and electric-Weyl
quantities can be reconstructed subject to its constraints, gauge, propagation,
and boundary data. Vector/tensor modes are outside the proposed scalar state.
The metric arithmetic is not used to prove the absence of a third scalar; that
conclusion rests on the CGI propagation pair under its stated assumptions.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 15. \(k=0\) versus \(k\ne0\) (H-D4)

Because \(\Delta_r\) and \(Z_r\) are Laplacian scalars, a spatially homogeneous
perturbation is annihilated:

\[
\Delta_{r,k=0}=Z_{r,k=0}=0
\quad\text{[GM (2.20)-(2.21); BDE (74)].}
\]

R-INH therefore fixes \(K_r,f_{v0}\), tracker parameters, regional background
densities, and scale-factor normalizations. R-0 is a separate background
tangent branch with its own parameter constraints. A Green operator is defined
only after projecting out its full elliptic kernel, not merely by writing
\(k\ne0\).

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 16. Common-clock and frame-transfer analysis

Regional equations use \(\tau_r\), while partition transport and GM evolution
use a common averaging time \(t\). Define clock maps
\(\chi_r:t\mapsto\tau_r\), with positive
\(\lambda_r=d\tau_r/dt\). Then

\[
\partial_t\Delta_r=-\lambda_r Z_r,\qquad
\partial_tZ_r=-\lambda_r(2H_rZ_r+4\pi G\rho_r\Delta_r).
\]

A perturbed \(\lambda_r\), tilt, shift, or carrier map contributes additional
first-order terms. BMR20 explicitly keeps lapse, shift, and fluid-foliation
tilt separate; MH24 shows that averages and boundaries are generally
foliation-dependent. Consequently \(\Xi_r=\dot V_r/V_r\) cannot be silently
set equal to \(\Theta_r\). A clock/expansion transfer function is required.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 17. Partition dynamics (H-D5)

For comoving subdomains with common-time rates
\(\Xi_r=\dot V_r/V_r\),

\[
 f_v=\frac{V_v}{V_v+V_w},\qquad
\dot f_v=f_vf_w(\Xi_v-\Xi_w),\quad f_w=1-f_v .
\]

Linearizing around background \(f_v,\Xi_r\) gives

\[
\delta\dot f_v=(1-2f_v)(\Xi_v-\Xi_w)\delta f_v
+f_vf_w(\delta\Xi_v-\delta\Xi_w).
\]

For \(L_D=a_D^2D_D^2\) and
\(\mathcal F_v=L_D\delta f_v\),

\[
\dot{\mathcal F}_v=(1-2f_v)(\Xi_v-\Xi_w)\mathcal F_v
+f_vf_w\mathcal E_{\Delta\Xi}
+[\partial_t,L_D]\delta f_v ,
\]
\[
\mathcal E_{\Delta\Xi}:=L_D(\delta\Xi_v-\delta\Xi_w).
\]

The commutator vanishes only on a fixed comoving FLRW carrier with the declared
normalization. Closure therefore requires an expansion-transfer scalar and, in
general, an operator-transport residual.

Primary classification: `SYMBOLICALLY_VERIFIED`.

## 18. Two-region backreaction and curvature decomposition (H-D7)

For a common foliation, Buchert (10c) and variance decomposition give

\[
Q_D=f_wQ_w+f_vQ_v+\frac23 f_wf_v(\Theta_w-\Theta_v)^2 .
\]

Exact regional FLRW backgrounds have \(Q_w=Q_v=0\). Writing
\(d_\Theta=\Theta_v-\Theta_w\), the first variation is

\[
\delta Q_D=f_w\delta Q_w+f_v\delta Q_v
+\frac23(1-2f_v)d_\Theta^2\delta f_v
+\frac43 f_vf_wd_\Theta(\delta\Theta_v-\delta\Theta_w).
\]

For R-INH, \(\delta Q_r\) vanishes at first order because regional variance and
shear-square terms start quadratically. After a declared common transfer,

\[
\mathscr Q=\frac23(1-2f_v)d_\Theta^2\mathcal F_v
+\frac43f_vf_wd_\Theta\,\mathcal E_{\Delta\Theta}
+\mathcal R_Q .
\]

Likewise, with
\(\langle R\rangle_D=f_wR_w+f_vR_v\),

\[
\mathscr W=f_wT_w\mathscr R_w+f_vT_v\mathscr R_v
+(\bar R_v-\bar R_w)\mathcal F_v+\mathcal R_W ,
\]

for inhomogeneous modes, since \(L_D(6K_D/a_D^2)=0\). The residuals record
moving maps, smoothing, and clock/foliation effects. Thus the candidate
five-state reduction has rank five only if
\(\mathcal E_{\Delta\Xi},\mathcal E_{\Delta\Theta},\mathcal R_Q,\mathcal R_W\)
are derived from specified transfer data. They are not presently supplied.

Primary classification: `SYMBOLICALLY_VERIFIED`.

## 19. Effective-density and pressure derivation (H-D6)

GM defines

\[
W_D=\langle R\rangle_D-\frac{6K_D}{a_D^2},\quad
\rho_{\rm eff}=-\frac{Q_D+W_D}{16\pi G},\quad
p_{\rm eff}=-\frac{Q_D}{16\pi G}+\frac{W_D}{48\pi G}
\]

[Eqs. (3.12)-(3.13) of arXiv:2511.17160v2]. With localized
\(\mathscr Q=L_D\delta Q_D\) and \(\mathscr W=L_D\delta W_D\),
GM (2.20)-(2.21) imply

\[
\widehat\Delta_{\rm eff}
=\frac{\mathscr Q+\mathscr W}{\bar Q_D+\bar W_D},
\qquad
\widehat{\widetilde P}_{\rm eff}
=\frac{3\mathscr Q-\mathscr W}
{3(\bar Q_D+\bar W_D)} .
\]

The normalization requires \(\bar Q_D+\bar W_D\ne0\); when
\(\rho_{\rm eff}=0\), normalized effective CGI variables are singular even if
unnormalized gradients are regular.

Primary classification: `SYMBOLICALLY_VERIFIED`.

## 20. Clean-comoving constitutive closure

GM (4.20) sets the effective velocity equal to the dust observer velocity.
GM (4.12) then enforces \(\widetilde P_{\rm eff}=0\). With the preceding
normalization,

\[
\widehat{\widetilde P}_{\rm eff}=0
\Longleftrightarrow \mathscr W=3\mathscr Q
\quad(\bar Q_D+\bar W_D\ne0).
\]

This is `ENFORCED_CONSTITUTIVE_CLOSURE`, not a propagated initial constraint.
It must hold for every time in this branch. No regional equation proves it.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 21. Constraint-propagation derivation (H-D8)

Let target GM variables obey (4.21)-(4.23), and let hats denote reconstructed
regional quantities. Define residuals

\[
\begin{aligned}
R_\Delta&=\dot{\widehat\Delta}_d+\widehat Z,\\
R_{\rm eff}&=\dot{\widehat\Delta}_{\rm eff}
-w\Theta\widehat\Delta_{\rm eff}+(1+w)\widehat Z,\\
R_Z&=\dot{\widehat Z}+\frac23\Theta\widehat Z
+4\pi G(\rho_d\widehat\Delta_d+\rho_{\rm eff}
\widehat\Delta_{\rm eff})
+12\pi G\rho_{\rm eff}\widehat{\widetilde P}_{\rm eff}.
\end{aligned}
\]

For
\(C_\Delta=\Delta_d-\widehat\Delta_d\),
\(C_Z=Z-\widehat Z\),
\(C_{\rm eff}=\Delta_{\rm eff}-\widehat\Delta_{\rm eff}\), and
\(C_P=\mathscr W-3\mathscr Q\), direct subtraction yields

\[
\dot C_\Delta=-C_Z-R_\Delta ,
\]
\[
\dot C_{\rm eff}=w\Theta C_{\rm eff}-(1+w)C_Z-R_{\rm eff},
\]
\[
\dot C_Z=-\frac23\Theta C_Z-4\pi G\rho_dC_\Delta
-4\pi G\rho_{\rm eff}C_{\rm eff}+\frac14C_P-R_Z .
\]

The \(+C_P/4\) coefficient follows from
\(12\pi G\rho_{\rm eff}\widehat{\widetilde P}_{\rm eff}=C_P/4\).
The candidate two-equation system omitted
\(-4\pi G\rho_{\rm eff}C_{\rm eff}\) and the evolution of \(C_{\rm eff}\).
Zero initial mismatches propagate only if all three residuals vanish and
\(C_P(t)=0\) for all time.

This is a three-*component* mismatch propagation structure, not an independent
rank proof. The components can become dependent after a transfer and its
admissible subspace have been selected; constitutive closure can change their
independence; and transfer residuals can couple them. Accordingly the matching
rank is `RANK_NOT_COUNTABLE_BEFORE_TRANSFER_SELECTION`. \(C_P\) is classified
separately as an enforced constitutive residual, not a fourth mismatch state.

Primary classification: `SYMBOLICALLY_VERIFIED`.

## 22. Common spatial carrier

The required carrier category can be represented formally by a time-indexed
Riemannian manifold
\((\Sigma_D(t),h_D(t),\mu_D(t))\), regional charts
\(\phi_r:U_r\subset\Sigma_D\to\Sigma_r\), and partition weights
\(\omega_w+\omega_v=1\) almost everywhere. It requires declared topology,
orientation, regularity, overlap/interface treatment, volume measure, and
transport in time.

GM's statement “within a single spacetime” does not construct this carrier.
W09's spherically averaged dressed radial geometry does not supply a
three-dimensional carrier. Absence of this object is a geometry/matching
deficit, not permission to identify coordinates. Thus this is a required object
category, not a selected current-theory carrier.

Primary classification: `UNRESOLVED_EXTERNAL_DEPENDENCY`.

## 23. Formal transfer-definition pattern (H-D9)

For \(L_r=a_r^2D_r^2\), a possible pattern would require
\(\Pi_{0,r}\) to project onto the full elliptic kernel and an already proved
Green operator \(G_r\) to satisfy

\[
L_rG_r=G_rL_r=1-\Pi_{0,r}
\]

on declared domains. Only then can one write the formal pattern

\[
T_r=L_D\,P_r\,G_r,\qquad
P_rX=S_\ell[\omega_r\,\phi_r^*X].
\]

This displayed expression is `FORMAL_DEFINITION_PATTERN`, not a constructed or
mathematically defined operator. It proves neither existence nor preservation
of CGI definitions. A realization must supply precise domains and codomains,
functional spaces, regularity, the full zero-mode projector, existence and
uniqueness for the inverse Laplacian, topology, boundary or decay conditions,
boundedness or continuity, pullback regularity, compatible Jacobians and
measures, and treatment of time-dependent spaces. Commutation and domain
properties must then establish any claimed definition preservation.

The original expression placed \(J_r\) directly in a pointwise scalar
pullback. That is not invariantly justified: a Jacobian belongs in the
transformed measure or in an explicitly normalized integral kernel. It may be
written inside \(P_r\) only after \(P_r\) is defined as a density-weighted
integral operator.

### Smooth partition branch

A smooth realization requires a partition of unity, a declared regularity
class for \(\omega_r\), a specified smoothing kernel or operator, smoothing
scale \(\ell\), normalization, positivity, support properties, interaction
with \(L_D\), transport in time, a scale-dependence study, and declared
sharp-limit behavior. Smoothing changes the model; it is not a neutral
rewriting of the regional fields.

### Sharp partition branch

Let \(\chi_r\) be a characteristic function and \(\Gamma=\partial U_r\). With
the orientation sign \(\sigma_r=\pm1\) declared explicitly,

\[
D_i\chi_r=\sigma_r n_i\delta_\Gamma,
\qquad
D^2\chi_r=\sigma_r\left[(D_i n^i)\delta_\Gamma
+n^iD_i\delta_\Gamma\right].
\]

The product rule gives

\[
D^2(\chi_rX_r)=\chi_rD^2X_r
+2D^i\chi_rD_iX_r+X_rD^2\chi_r .
\]

The last two terms are interface-supported distributions; after summing
regions they are controlled by jumps in traces and normal fluxes, and can also
contain derivatives of \(\delta_\Gamma\). Eliminating them requires demonstrated
weak matching conditions, trace regularity, jump conditions, normal-flux
conditions, or a surface-source model. Zero spatial-volume measure does not
discard these distributional contributions.

Primary classification: `NOT_JUSTIFIED` as an existing operator;
`CONVENTION_DEPENDENT` as a future pattern after all analytic data are chosen.

## 24. Spectral kernel and mode mixing (H-D10)

If a genuine transfer operator has first been constructed, normalized bases
would define

\[
M_r(k_D,k_r;t)=
\langle Q^{D}_{k_D},T_rQ^r_{k_r}\rangle_D .
\]

Flat-wall and negatively curved void Laplacians generally have different
spectra, degeneracies, topology, and boundary conditions. Multiplication by
\(\omega_r\), restriction to \(U_r\), pullback, and smoothing also fail to
commute with the Laplacians. Hence \(M_r\) is generically non-diagonal.

Geometry does not prove an absolute impossibility theorem for every engineered
operator; it shows that a global simultaneous mode-diagonal transfer is not
justified. Diagonality can occur in equal-region or single-region limits, or
approximately in a controlled local-WKB patch. It never establishes
\(k_w=k_v=k_D=k_{\rm code}\).

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 25. Temporal intertwining (H-D11)

Let \(S_R\) obey \(\dot S_R=A_RS_R\), and
\(\widehat Y=T(t)S_R\). Then

\[
\dot{\widehat Y}-A_{\rm GM}\widehat Y
=\left(\dot T+TA_R-A_{\rm GM}T\right)S_R .
\]

Therefore

\[
R_T:=\dot T+TA_R-A_{\rm GM}T=0
\]

is necessary and sufficient for every allowed initial regional state when the
operators share a common differentiable domain. If admissible data occupy a
proper subspace, only the restriction of \(R_T\) to that subspace must vanish.

The equation may test or propagate an independently geometrically derived
transfer. It may not fit \(T(t_i)\) from frozen GM trajectories.

Primary classification: `SYMBOLICALLY_VERIFIED`.

## 26. Elliptic and boundary data

Each \(G_r\) needs topology, function space, kernel projector, operator domain,
and either boundary conditions (Dirichlet, Neumann, Robin, transmission) or
decay/compactness conditions. Neumann data require the compatibility integral;
noncompact data require weighted spaces and decay. Interface traces must be
regular enough for pullback and smoothing. The smoothing length \(\ell\) is a
declared parameter and its variation is a falsification test.

No library-default tolerance, solver convention, or self-adjoint extension is
scientific input. Numerical tolerances would have to be explicit in a later,
separately approved phase.

Primary classification: `UNRESOLVED_EXTERNAL_DEPENDENCY`.

## 27. Initial data and inverse nullspace (H-D12, H-D13)

Conditional dynamic initial functions are

\[
\Delta_w(t_i),Z_w(t_i),\Delta_v(t_i),Z_v(t_i),\mathcal F_v(t_i).
\]

They must satisfy zero-mode, regularity, positivity, mass/volume, and GM
compatibility conditions. If
\(\Delta_{\rm eff}(t_i)=0\) and \(C_P(t_i)=0\), then
\[
\mathscr Q_i+\mathscr W_i=0,\qquad
\mathscr W_i-3\mathscr Q_i=0
\quad\Rightarrow\quad
\mathscr Q_i=\mathscr W_i=0,
\]
provided \(\bar Q_D+\bar W_D\ne0\).

For a bounded linear transfer \(T:X_R\to Y_{\rm GM}\), the inverse at
\(y\in\operatorname{Ran}T\) is unique exactly when
\(\ker(T|_{X_{\rm adm}})=\{0\}\). If the kernel is nontrivial, all solutions
are \(x_0+\ker T\). Since current theory does not specify \(T\) or its spaces,
neither injectivity nor a kernel dimension is known. A five-to-three
finite-mode count is only an illustration.

Current status:
`INVERSE_UNIQUENESS_UNRESOLVED_BEFORE_TRANSFER_SELECTION`. Neither uniqueness
nor nonuniqueness is claimed, and no unconditional nullspace dimension is
assigned.

All proposed selectors are `OPTIONAL_MODEL_EXTENSION`:
minimum norm (requires a chosen Hilbert norm), adiabatic regional mode, no
compensated isocurvature, fixed wall/void ratio, primordial regional covariance,
or an external simulation prior. None is a Timescape default.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 28. Independent-equation counting

| Formulation | \(N_{\rm raw}\) | definitions | algebraic constraints | gauge | \(N_{\rm phys}\) | evolution rank | \(\Delta_{\rm dyn}\) |
|---|---:|---:|---:|---:|---:|---:|---|
| one regional CGI dust scalar sector | 2 | 0 | 0 | 0 | 2 | 2 | 0 |
| one regional metric+dust scalar cross-check | six configuration variables (illustrative) | formulation-dependent | formulation-dependent | formulation-dependent | `HEURISTIC_METRIC_CROSS_CHECK` | not independently counted | not independently counted |
| two regional CGI sectors | 4 | 0 | 0 | 0 | 4 | 4 | 0 |
| conditional C-AVG-com state | 5 | 0 | closures not counted | CGI gauge fixed; carrier gauge external | 5 | 5 only after transfer assumptions | 0 conditional |
| current C-AVG design | 5 plus map/clock functions | map definitions not dynamics | compatibility/closure ranks branch-dependent | carrier gauge unspecified | `NOT_COUNTABLE_BEFORE_BRANCH_SELECTION` | bulk 4; partition rank unresolved | `LOWER_BOUND >=1` |
| C-JUNC | bulk plus \(Q^\pm,T^\pm\) | induced forms | first/second-form blocks | spacetime+hypersurface gauge | `BIFURCATED` | `NOT_COUNTABLE_BEFORE_BRANCH_SELECTION` | at least one block |
| C-SHELL | C-JUNC plus surface state | shell definitions | Lanczos constraints | as above | `BIFURCATED` | needs surface EOS/evolution | at least one added block |

Separate exact counts are limited to the CGI regional bulk: rank \(4\) for two
regions. Partition rank \(1\) is conditional; effective geometry has algebraic
rank \(2\) only after localization. Geometric and matter/averaging matching
remain at least two required object blocks, but their operator rank is not
countable before transfer selection. There are at least two regional
Green-operator data blocks, five candidate dynamic IC functions before an
unknown compatibility-rank reduction, and no assigned inverse-nullspace rank.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 29. Mandatory limits

| ID | Pass criterion | Failure consequence |
|---|---|---|
| L0 zero perturbation | all regional, partition, effective, and GM perturbations/residuals vanish | formulation inconsistent |
| L1 background recovery | W07/W09/GM (5.1)-(5.7) recovered with unchanged parameters | reject branch |
| L2 equal-region | \(H_w=H_v,\rho_w=\rho_v,R_w=R_v\) removes partition variance and relabelling effects | transfer/partition formula rejected |
| L3 single-region | \(f_v\to0\) or \(1\) gives the surviving regional dust system without singular weights | branch invalid near physical endpoints |
| L4 global FLRW | \(Q_D=W_D=0\) handled with unnormalized variables; standard FLRW growth recovered | normalization/limit redesign |
| L5 zero mode | \(L_rG_r=1-\Pi_{0,r}\); R-INH cannot change background parameters | reject inverse |
| L6 wall/void relabelling | \(v\leftrightarrow w,\ f_v\leftrightarrow f_w\) leaves physical equations covariant | algebra/sign failure |
| L7 carrier diffeomorphism | pullbacks, measures, kernels, and inner products transform covariantly | carrier rejected |
| L8 mass/volume conservation | \(f_v+f_w=1\), comoving mass and partition-volume identities propagate | reject partition transport |
| L9 constraint propagation | corrected three-mismatch system stays zero under zero residuals and \(C_P(t)=0\) | conditional closure fails |
| L10 intertwining | \(R_T\) vanishes on the entire admissible state space | transfer incompatible |
| L11 local WKB/flat | controlled high-frequency patch yields declared diagonal approximation and error order | WKB branch rejected |
| L12 smoothing scale | conclusions stable over a predeclared admissible \(\ell\)-range or dependence is modelled | uncontrolled extension |
| L13 sharp interface | \(\ell\to0\) converges in stated spaces with controlled \(D\chi_r,D^2\chi_r\) terms, or explicitly changes to C-JUNC/C-SHELL/C-TRANS | C-AVG sharp limit rejected |
| L14 independent basis | reconstructed results invariant under complete admissible basis changes; truncation error explicit | spectral conclusion rejected |

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 30. Falsification matrix

| Gate | Fail condition | Mandatory branch/verdict change |
|---|---|---|
| no common carrier | no regular \(\Sigma_D,\phi_r,\mu_D\) exists | C-AVG becomes inconsistent; test C-TRANS or stop |
| elliptic ill-posedness | \(G_r\) has no closed admissible realization | reject candidate transfer |
| transfer incompatibility | \(R_T\ne0\) for allowed data | forward model remains partial |
| only trivial compatible state | compatibility forces all perturbations zero | `REGIONAL_MATCHING_FORMULATION_INCONSISTENT` for that branch |
| unavoidable surface source | distributional stress is required | reclassify C-AVG/C-JUNC to C-SHELL |
| singular physical limits | L2, L3, L4, or L13 diverges without physical source | reject branch |
| fitted kernel | \(T(t_i)\) inferred from GM target trajectories | evidence invalid; no closure claim |
| smoothing dependence | output changes without controlled \(\ell\) law | C-AVG becomes optional model extension |
| hidden wavenumber identification | any \(k_r,k_D,k_{\rm code}\) silently equated | spectral result invalid |
| hidden finite-infinity identification | GM boundary set to W09 finite infinity without derivation | C-FI rejected |
| false inverse uniqueness | unique regional solution asserted without injectivity proof/selector | inverse conclusion invalid |

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 31. Required initial-boundary-value package categories

This section is `FORMAL_PACKAGE_SKELETON_SPECIFIED`: it identifies required
categories but selects no concrete transfer realization. “Required” below is
not evidence that a value, space, map, kernel, or boundary condition has been
chosen. `PRE-PROTOTYPE_GATE_NOT_YET_EXECUTABLE`.

### BACKGROUND

Available frozen input: tracker \(a_D,a_r,f_v,H_D,H_r,\rho_r,\bar Q_D,\bar W_D\),
with R-INH background parameters fixed.

### DYNAMICAL STATE

Formal branch-dependent candidate:
\((\Delta_w,Z_w,\Delta_v,Z_v,\mathcal F_v)\) for conditional C-AVG-com.

### EVOLUTION EQUATIONS

Derived: four regional dust equations. Required but unselected: one partition
equation after expansion/clock transfer. Constitutive closure is not dynamics.

### CONSTRAINTS

Derived regionally: Hamiltonian constraints. Required after transfer selection:
reconstructed \(C_\Delta=C_Z=C_{\rm eff}=0\), with branch-dependent
independence. Mass and volume identities remain constraints.

### CONSTITUTIVE CLOSURES

Required branch choice: \(C_P(t)=\mathscr W-3\mathscr Q=0\) for the formal
clean-comoving branch. It is not current regional dynamics; other closures
define different model branches.

### GAUGE OR FRAME CHOICES

Required but not fully selected: regional dust-comoving CGI frames, common
foliation, carrier gauge, clock maps, and map transport. BMR tilt and ADM lapse
remain distinct.

### INITIAL FUNCTIONS

Candidate category: five dynamic functions before compatibility-rank reduction.
R-0 data are separate and optional.

### INITIAL COMPATIBILITY

Required after realization: \(C_\Delta=C_Z=C_{\rm eff}=0\), zero-mode removal,
Green compatibility integrals, positivity, and regularity. Their independent
rank is not inferred from the three component labels.

### PARTITION DATA

Required but not selected: initial partition, weights, comoving transport,
interface regularity, and expansion-transfer rule.

### COMMON-CARRIER DATA

Required but not selected: topology, \(h_D,\mu_D,U_r,\phi_r\), orientation,
overlap/interface convention, and temporal transport.

### TRANSFER DATA

Required but not selected: scalar pullback convention, smooth or sharp branch,
Jacobian/measure placement, spaces, and temporal transport. \(T_r=L_DP_rG_r\)
is only a formal pattern; no mapped CGI scalar is presently derived from it.

### ELLIPTIC DATA

Required but not selected: function spaces, \(\Pi_{0,r}\), domains of
\(L_r,G_r\), inverse existence/uniqueness, self-adjoint extension if used, and
compatibility conditions.

### BOUNDARY OR DECAY CONDITIONS

Required and branch-dependent, but not selected: regional and carrier
boundary/transmission conditions, or asymptotic decay; shell/transition rules
only in their branches.

### INVERSE-SELECTION DATA

Optional extension: one explicit selector if an inverse is requested. No
runtime default is allowed.

### CONSTRAINT-PROPAGATION CONDITIONS

Future acceptance requirement after operator construction:
\(R_\Delta=R_{\rm eff}=R_Z=0\), \(C_P(t)=0\), and \(R_T=0\) on admissible
states.

### REGULARITY AND POSITIVITY

Required/constrained: positive volumes and lapse factors, \(0<f_v<1\) away
from tested limits, positive dust density, bounded maps, and sufficient Sobolev
regularity.

### BACKGROUND AND FLRW LIMITS

Constrained: L0-L6, especially unnormalized treatment when
\(\rho_{\rm eff}=0\).

### FALSIFICATION CONDITIONS

Future mandatory gates: every gate in Section 30 must become executable only
after a branch is instantiated. At present the pre-prototype gate is not
executable; once instantiated, a failure changes or rejects the branch.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 32. Branchwise detailed deficit assessment

The Phase 1E-D deficit is `BIFURCATED`; no universal tuple is justified.

| Component | `CURRENT_TIMESCAPE_ONLY` | `EXPLICIT_IMPORTED_TRANSFER_REALIZATION` |
|---|---|---|
| \(N_{\rm undef}\) | `LOWER_BOUND >=1`: at least one composite object block containing the carrier, embeddings/pullbacks, functional transfer, spaces, and boundary realization is undefined | `0` only after every carrier, map, measure/Jacobian, space, smooth/interface branch, Laplacian/Green realization, BC/decay rule, and temporal transport is explicitly defined; no such realization is selected here |
| \(\Delta_{\rm dyn}\) | `LOWER_BOUND >=1`: regional bulk rank four is exact, but partition/clock/transfer evolution is missing | `NOT_COUNTABLE_BEFORE_BRANCH_SELECTION`; reassess after the chosen operator and transport laws exist |
| \(\Delta_{\rm IC}\) | `LOWER_BOUND >=1`; candidate functions exist, but independent compatibility rank is unknown | `NOT_COUNTABLE_BEFORE_BRANCH_SELECTION`; reassess on the selected admissible space |
| \(\Delta_{\rm BC}\) | `BRANCH_DEPENDENT LOWER BOUND >=1`: elliptic and carrier/interface data are absent | `NOT_COUNTABLE_BEFORE_BRANCH_SELECTION`; depends on compact, noncompact, finite-patch, smooth, or sharp realization |
| \(\Delta_{\rm match}\) | `LOWER_BOUND >=2` required object blocks (geometry/clock and matter/averaging/effective); this is not a rank inferred from three mismatches | `RANK_NOT_COUNTABLE_BEFORE_TRANSFER_SELECTION`; reassess after closures, spaces, and residual coupling are fixed |
| \(\Delta_{\rm emp}\) | `N/A` | `N/A` |

The imported branch is an extended conditional model, not current Timescape
machinery. Unknown entries are not encoded as zero.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 33. Implementation-readiness decision

`REPORT_ONLY_MUST_CONTINUE`.

`IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED`.

Only required package categories and future gates have been identified. No
concrete branch currently specifies all of carrier topology, pullbacks,
smoothing operator and scale, elliptic domains and BC, clock maps,
constitutive closure, transfer kernel, inverse selector, IC/BC, and
constraint-propagation tests. No metric, transfer, regional solver,
\(k\)-conversion, RSD, tracer, likelihood, or Candidate A modification is
authorized.

Primary classification: `NOT_JUSTIFIED`.

## 34. Overall verdict

`PARTIAL_REGIONAL_DYNAMICS_REMAIN_UNDERDETERMINED`.

`EXACT_REGIONAL_MATCHING_DYNAMICS_DERIVED` fails because no carrier/transfer
or matching-domain dynamics is derived. `CONDITIONAL_REGIONAL_MATCHING_MODEL_CLOSED`
fails because the conditions are enumerated but not concretely supplied.
`REGIONAL_MATCHING_FORMULATION_INCONSISTENT` is too strong: regional bulk
dynamics and the formal C-AVG skeleton are internally consistent, and
no falsification gate has proved that only the trivial state exists.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 35. Exact evidence needed to change the verdict

Promotion to `CONDITIONAL_REGIONAL_MATCHING_MODEL_CLOSED` requires one
explicit branch with: a common carrier and topology; regular pullbacks and
temporal transport; clock/lapse maps; normalized smoothing with scale;
well-posed Green operators and BC; a derived partition-expansion transfer;
localized \(\mathscr Q,\mathscr W\); the enforced closure; a geometrically
derived \(T(t_i)\); \(R_T=0\); corrected compatibility propagation; finite IC
compatibility rank; and an explicit inverse selector if inversion is claimed.

Promotion to `EXACT_REGIONAL_MATCHING_DYNAMICS_DERIVED` additionally requires
deriving those ingredients from current Timescape/GM machinery without an
optional constitutive or interface model. Demotion to inconsistency requires a
proved carrier obstruction, elliptic obstruction, only-trivial-state theorem,
or unavoidable incompatible surface source for every admissible current-
theory branch.

Primary classification: `UNRESOLVED_EXTERNAL_DEPENDENCY`.

## 36. Symbolic corroboration ledger

SymPy 1.14.0 in the external Python 3.14.3 audit environment encoded:

1. \(f_v=V_v/(V_v+V_w)\), \(\dot V_r=\Xi_rV_r\): residual against
   \(f_vf_w(\Xi_v-\Xi_w)\) was exactly zero.
2. regional dust Raychaudhuri plus the preceding \(\dot f_v\): residual
   against averaged Raychaudhuri with
   \(Q_D=(2/3)f_vf_w(\Theta_v-\Theta_w)^2\) was zero.
3. the \(\epsilon\)-derivative of the two-region \(Q_D\): residual against the
   expression in Section 18 was zero.
4. the GM definitions of \(\rho_{\rm eff},p_{\rm eff}\): simplified exactly to
   the two normalizations in Section 19.
5. substituting \(\mathscr W=3\mathscr Q\): pressure residual zero.
6. regional minus GM Raychaudhuri source: retained the expected
   \(2(H_D-H_r)Z_r\), density-source, map-weight, and \(\dot T\) terms; it did
   not vanish identically.
7. the compatibility subtraction: produced the \(3\times3\) matrix
   \[
   \begin{pmatrix}
   0&-1&0\\
   -4\pi G\rho_d&-2\Theta/3&-4\pi G\rho_{\rm eff}\\
   0&-(1+w)&w\Theta
   \end{pmatrix}
   \]
   and forcing \((-R_\Delta,C_P/4-R_Z,-R_{\rm eff})^T\).
8. differentiating \(TS_R\): residual exactly
   \((\dot T+TA_R-A_{\rm GM}T)S_R\).

No numerical experiment or Timescape prediction was made.

Primary classification: `SYMBOLICALLY_VERIFIED`.

## 37. Preservation and validation

Only this Markdown report and its JSON inventory are modified by the correction;
the adversarial audit remains immutable evidence. With `PYTHONPATH=src`,
`-q -p no:cacheprovider`, and an external
`--basetemp`, final validation returned:

- Python 3.14.3: `379 passed in 12.32s`;
- Python 3.11.9: `379 passed in 14.01s`.

The final preservation audit checks both diffs, confirms an empty index,
verifies the upstream notebook hash and clean detached clone, and records
deliverable SHA-256 values outside the self-hashed artifacts. No source, test,
script, frozen report, artifact, configuration, dependency, notebook, commit,
tag, remote ref, or publication is changed.

Primary classification: `NUMERICALLY_CORROBORATED`.

## 38. Strongest surviving and weakened claims

The strongest surviving claim is that the intrinsic scalar \(k\ne0\) dust
bulk in each exact wall/void FLRW region has exactly two first-order state
functions and rank-two propagation, with regional curvature supplied by a
constraint rather than a third scalar evolution variable.

The strongest weakened claim is the proposed GM-compatibility propagation:
two mismatch equations are insufficient. Effective-density compatibility is
dynamical and contributes
\(-4\pi G\rho_{\rm eff}C_{\rm eff}\) to \(\dot C_Z\), but the three components
do not fix an independent matching rank. Separately,
`INVERSE_UNIQUENESS_UNRESOLVED_BEFORE_TRANSFER_SELECTION`: uniqueness needs an
injectivity proof and nonuniqueness needs a proved nontrivial kernel.

Primary classification: `SYMBOLICALLY_VERIFIED`.
