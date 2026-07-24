# Phase 1E-D targeted correction verification audit

## 1. Verification verdict

`FURTHER_TARGETED_CORRECTIONS_REQUIRED`

Corrections C3-C9 pass. C1 has one minor, nonblocking documentation
asymmetry. C2 is incomplete because one JSON field still presents the metric
subtraction as a physical phase-space count without the required heuristic
classification or caveats. This is a localized remaining correction, not a
major scientific regression.

## 2. Scope and independence

This is a narrow, read-only verification of corrections C1-C9. It does not
repeat the full scientific audit, revisit claims outside the correction set, or
repair either corrected deliverable. The immutable adversarial audit was used
only as historical evidence for the pre-correction findings and artifact
hashes.

## 3. Repository and input gate

The mandatory pre-verification gate passed:

- branch:
  `phase-1e-d-regional-matching-dynamics-design`;
- HEAD: `fcbf9c29a28c586044150e6910e1637bc3f6975b`;
- corrected closure SHA-256:
  `db2e43a9446334a31ba3c6a65b0800e0b98395ea236c278684415399e271c62e`;
- corrected inventory SHA-256:
  `9a968c81df20e557b32b941f9da1f0b918349c958d6f25c9f006b90a0d839e8f`;
- immutable adversarial-audit SHA-256:
  `f390f1c93384ed1fb73aaf6fed3146a407a0bdb6a24d502374ddcfb704196337`.

Before this verification, `git status --short` contained exactly the closure,
inventory, and immutable adversarial audit as untracked files. The index and
tracked diff were empty.

## 4. C1-C9 status table

| Correction | Status | Verification result |
|---|---|---|
| C1 DOI records | `PASS_WITH_MINOR_NONBLOCKING_NOTE` | Both DOI assignments, author orders, journal, volume, and page ranges are correct in Markdown §7 and JSON `primary_source_inventory[13:15]`; the JSON also gives the correct titles. No obsolete shifted DOI remains. The Markdown rows say the titles were verified but do not print the titles themselves. |
| C2 metric equation counting | `FAIL` | Markdown §14 and §28 and JSON `equation_counting` correctly use `HEURISTIC_METRIC_CROSS_CHECK`, but JSON `gauge_inventory.metric_crosscheck` retains an unqualified subtractive count claiming “two physical first-order phase-space functions.” |
| C3 framework status distinction | `PASS` | Markdown §9, JSON `framework_status_distinction`, and all 14 `candidate_framework_matrix` records consistently separate `TARGET_STATE_STATUS` from `REGIONAL_DYNAMICS_STATUS`. Generic GR machinery is not promoted to current Timescape machinery. |
| C4 bifurcated \(N_{\rm undef}\) | `PASS` | Markdown §32 and JSON `deficit_vector` contain the required current-theory and explicit-import branches. The only \(N_{\rm undef}=0\) statement is conditional on a fully defined imported realization. The former universal tuple is absent. |
| C5 mismatch components versus rank | `PASS` | \(C_\Delta,C_Z,C_{\rm eff}\) remain three named compatibility components; \(C_P\) remains a separate constitutive residual. Both deliverables use `RANK_NOT_COUNTABLE_BEFORE_TRANSFER_SELECTION` and do not infer rank three. |
| C6 transfer definition pattern | `PASS` | Markdown §23 and JSON `transfer_operator` classify \(T_r=L_DP_rG_r\) only as a formal definition pattern and enumerate the missing operator, space, elliptic, measure, commutation, CGI-preservation, and time-dependent-domain proofs. Jacobians are assigned invariantly to a transformed measure or normalized kernel, not inserted automatically into a pointwise scalar pullback. |
| C7 smooth and sharp branches | `PASS` | The smooth branch supplies every required category; the sharp branch gives all three requested distributional identities and treats traces, jumps, normal fluxes, interface distributions, and possible surface sources. Zero volume measure is explicitly rejected as a reason to discard distributional terms. |
| C8 package and readiness | `PASS` | The package is limited to required categories and a formal skeleton; no concrete realization is selected and the pre-prototype gate is not executable. `REPORT_ONLY_MUST_CONTINUE` and authorization `NOT_GRANTED` are explicit. No solver, transfer API, prototype, Candidate A change, or observational implementation is authorized. |
| C9 artifact inventory | `PASS` | Both deliverables report `350 passed, 29 skipped`, identify 29 as a skipped-test count, list ten restored ignored files including the two formerly omitted paths, and report the restored `379 passed` baseline. All ten current hashes equal the immutable audit values. |

## 5. Detailed findings

### C1: DOI records

The corrected associations are:

| ID | Title | Authors | Journal data | DOI |
|---|---|---|---|---|
| DBE92 | *Covariant perturbations in a multifluid cosmological medium* | P. K. S. Dunsby, M. Bruni, G. F. R. Ellis | *ApJ* 395 (1992) 54-74 | `10.1086/171630` |
| BDE92 | *Cosmological perturbations and the physical meaning of gauge-invariant variables* | M. Bruni, P. K. S. Dunsby, G. F. R. Ellis | *ApJ* 395 (1992) 34-53 | `10.1086/171629` |

Markdown §7 contains the correct IDs, author order, journal, volume, page
ranges, and DOI values. JSON `primary_source_inventory[13].citation` and
`[14].citation` additionally print the correct titles. Searches found no
obsolete `10.1086/171628` and no shifted use of either corrected DOI. The
classification is conditional only because the Markdown does not itself print
the two titles.

### C2: incomplete metric-count correction

The corrected material is otherwise explicit:

- Markdown §14 labels the subtraction `HEURISTIC_METRIC_CROSS_CHECK` and
  acknowledges configuration/phase-space mixing, formulation-dependent
  constraint independence and propagation, and gauge-generator dependence.
- Markdown §28 does not independently count the metric rank.
- JSON `equation_counting.formulations[1]` carries the required heuristic token,
  caveats, and `NOT_INDEPENDENTLY_DERIVED` values.
- The exact rank-two conclusion is attributed to the CGI system in Markdown
  §13 and JSON `regional_state_inventory.R_INH`, `equation_counting`, and formal
  conclusion `H-D3`.

However, JSON `gauge_inventory.metric_crosscheck` says:

> Six raw scalar functions minus two scalar coordinate gauges and two scalar
> Einstein constraints leaves two physical first-order phase-space functions.

That occurrence is not classified as `HEURISTIC_METRIC_CROSS_CHECK`, omits all
required caveats, and positively asserts the very phase-space conclusion the
correction was meant to withdraw. Therefore the requirement that *every*
metric-count occurrence be heuristic is not met. This also prevents a finding
of exact Markdown/JSON semantic consistency.

The exact remaining targeted correction is to replace or qualify only JSON
`gauge_inventory.metric_crosscheck` so it states that the subtraction is a
heuristic configuration-space illustration, does not establish physical
phase-space rank, and is subject to formulation-dependent constraints,
constraint propagation, and specified gauge generators/conditions. No
scientific equation or surviving CGI result needs to change.

### C3-C8 consistency

All 14 framework records were individually inspected. Their classifications
agree with Markdown §9: regional perturbation dynamics are compatible imports;
the frozen GM variables are current target language; and carrier geometry,
embeddings, pullbacks, kernels, Green operators, and smoothing realizations are
not current regional Timescape machinery.

The branchwise deficit is consistent in both formats. `CURRENT_TIMESCAPE_ONLY`
has the conservative object-block lower bound \(N_{\rm undef}\ge1\).
`EXPLICIT_IMPORTED_TRANSFER_REALIZATION` permits \(N_{\rm undef}=0\) only after
every listed geometric and analytic object is explicitly defined. Unknown
dynamical, initial-condition, boundary, and matching ranks are not encoded as
zero.

The transfer is consistently only a formal pattern. The smooth branch records
partition of unity, regularity, kernel/operator, scale, positivity,
normalization, support, Laplacian interaction, time transport, scale
dependence, and sharp-limit behavior. The sharp branch gives

\[
D_i\chi_r=\sigma_r n_i\delta_\Gamma,
\]

\[
D^2\chi_r=\sigma_r\left[(D_i n^i)\delta_\Gamma+
n^iD_i\delta_\Gamma\right],
\]

and

\[
D^2(\chi_rX_r)=\chi_rD^2X_r+
2D^i\chi_rD_iX_r+X_rD^2\chi_r.
\]

The readiness vocabulary is uniformly weaker than a concrete scientific
specification: `REQUIRED_PACKAGE_CATEGORIES_IDENTIFIED`,
`FORMAL_PACKAGE_SKELETON_SPECIFIED`,
`CONCRETE_REALIZATION_NOT_SELECTED`, and
`PRE-PROTOTYPE_GATE_NOT_YET_EXECUTABLE`.

### C9: artifact inventory

The artifact-free result, restoration count, and restored baseline agree:

- artifact-free tree: `350 passed, 29 skipped`;
- 29 is the skipped-test count, not a file count;
- restored ignored artifacts: 10 files;
- restored baseline: `379 passed`.

All files exist, are ignored, and match the immutable adversarial audit:

| Path | SHA-256 |
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

No regeneration was required during this verification.

## 6. Surviving scientific findings

All eight required findings survived the corrections without an unsupported
promotion:

1. the intrinsic regional \(k\ne0\) dust scalar state remains
   \((\Delta_r,Z_r)\);
2. each exact regional FLRW dust sector retains rank-two intrinsic evolution,
   derived from the CGI equations rather than the metric heuristic;
3. the exact two-region intrinsic bulk rank remains four;
4. \(C_{\rm eff}\) remains independently load-bearing in generic mismatch
   propagation;
5. three named mismatch components do not prove matching rank three;
6. inverse uniqueness and nonuniqueness remain unresolved before transfer and
   admissible-space selection;
7. Candidate A remains non-observational;
8. no RSD, \(f\sigma_8\), tracer, or survey bridge was created.

## 7. Markdown/JSON consistency and schema

The following counts were independently reproduced:

- top-level JSON keys: 34;
- framework records: 14;
- ontology records: 35;
- formal conclusions: 15.

Every formal conclusion has exactly these nine fields:
`classification`, `source`, `assumptions`, `derivation_summary`,
`coordinate_dependencies`, `frame_dependencies`,
`implementation_consequence`, `observational_consequence`, and
`evidence_needed_to_change_status`. There are no missing or extra fields.

The Markdown and JSON agree on the overall verdict, subordinate statuses,
framework classifications, CGI regional rank, three mismatch components,
transfer status, branchwise deficit, unresolved inverse, implementation
readiness, artifact restoration, and prohibited implementations. Exact semantic
consistency fails only at JSON `gauge_inventory.metric_crosscheck`, as described
under C2. The unprinted Markdown titles under C1 are a minor documentation
asymmetry, not conflicting metadata.

## 8. Prohibited-claim search

No affirmative prohibited claim was found:

- \(N_{\rm undef}=0\) occurs only under the fully explicit imported branch;
- matching rank three is explicitly rejected;
- no minimum transfer or initial-boundary package is claimed;
- prototype and operator construction are explicitly denied or conditional;
- inverse nonuniqueness is explicitly unresolved;
- \(k_w=k_v=k_D=k_{\rm code}\), GM-domain/finite-infinity identity,
  peculiar-velocity interpretation of \(Z\), and Candidate A/\(f\sigma_8\)
  identity occur only as forbidden or rejected identifications;
- 29 is explicitly a skipped-test count, not a missing-artifact-file count.

## 9. Validation and preservation

Canonical full-suite validation with `PYTHONPATH` containing `src`, cache
provider disabled, and an external base temporary directory returned:

- Python 3.14.3: `379 passed in 14.06s`;
- Python 3.11.9: `379 passed in 14.92s`.

`git diff --check` and `git diff --cached --check` produced no output. The
index remained empty. No audited report, source, test, script, artifact,
configuration, dependency, or notebook was modified. Nothing was staged,
committed, tagged, pushed, merged, or published.

## 10. Final decision

`FURTHER_TARGETED_CORRECTIONS_REQUIRED`

The only blocking correction defect is the stale unqualified metric-count
sentence at JSON `gauge_inventory.metric_crosscheck`. C1's omitted Markdown
titles are a minor nonblocking documentation note. All findings that survived
the adversarial audit remain intact.

IMPLEMENTATION_AUTHORIZATION:
NOT_GRANTED
