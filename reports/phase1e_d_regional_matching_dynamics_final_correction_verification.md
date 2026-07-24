# Phase 1E-D second targeted correction verification audit

## 1. Final verification verdict

`ALL_TARGETED_CORRECTIONS_VERIFIED`

The last surgical C2 correction is complete. C1 retains its existing minor
nonblocking documentation note, C3-C9 show no regression, and all eight
surviving scientific findings remain intact. The corrected Phase 1E-D
deliverables are ready for a later human-authorized report-only commit and tag.
This finding does not authorize implementation or any Git operation in this
audit.

## 2. Scope and independence statement

This was a narrow, read-only verification of the current
`gauge_inventory.metric_crosscheck` correction and the explicitly required
C1/C3-C9 regression gates. It did not repeat the complete scientific
adversarial audit, repair an audited file, or reinterpret the historical first
verification. Conclusions were rechecked directly against the current closure
and inventory; the two earlier audit reports were treated as immutable
historical evidence.

## 3. Repository and hash preflight

The mandatory preflight passed before verification:

- branch:
  `phase-1e-d-regional-matching-dynamics-design`;
- unchanged HEAD:
  `fcbf9c29a28c586044150e6910e1637bc3f6975b`;
- closure SHA-256:
  `db2e43a9446334a31ba3c6a65b0800e0b98395ea236c278684415399e271c62e`;
- corrected inventory SHA-256:
  `b27e6f495c8524e8f5cfc3383b307772e7933ee7a0bd66f36bba807024ad1cc4`;
- immutable adversarial-audit SHA-256:
  `f390f1c93384ed1fb73aaf6fed3146a407a0bdb6a24d502374ddcfb704196337`;
- immutable first-verification SHA-256:
  `55558fa0a3063991ca576cf2dd3e14fed79e6d7291f116c4fb7eefa64165c325`.

The immediately preceding inventory hash was recorded as
`9a968c81df20e557b32b941f9da1f0b918349c958d6f25c9f006b90a0d839e8f`.
No independently retained full copy of that untracked pre-correction inventory
was found in the workspace, so this audit does not claim a direct byte-level or
structural old/new proof that only one JSON path changed. It instead verified
the current hash and corrected value and performed all specified semantic,
schema, scientific-finding, and preservation regression checks.

Before this report was created, `git status --short` contained exactly the four
expected untracked reports. The tracked worktree and index were empty, and no
Phase 1E-D tag existed.

## 4. Historical first-verification finding

The immutable first verification remains unchanged. It concluded
`FURTHER_TARGETED_CORRECTIONS_REQUIRED`, with C1
`PASS_WITH_MINOR_NONBLOCKING_NOTE`, C2 `FAIL`, and C3-C9 `PASS`. Its sole
blocker was the stale assertion in JSON `gauge_inventory.metric_crosscheck`
that informal subtraction “leaves two physical first-order phase-space
functions.” This report preserves that conclusion as historical evidence of
the pre-correction state.

## 5. C1-C9 status table

| Correction | Status |
|---|---|
| C1 | `UNCHANGED_PASS_WITH_MINOR_NONBLOCKING_NOTE` |
| C2 | `PASS` |
| C3 | `UNCHANGED_PASS` |
| C4 | `UNCHANGED_PASS` |
| C5 | `UNCHANGED_PASS` |
| C6 | `UNCHANGED_PASS` |
| C7 | `UNCHANGED_PASS` |
| C8 | `UNCHANGED_PASS` |
| C9 | `UNCHANGED_PASS` |

## 6. C2 verification

The current JSON value at `gauge_inventory.metric_crosscheck` begins with
`HEURISTIC_METRIC_CROSS_CHECK` and describes the six-variable subtraction only
as a consistency illustration. It now states all required limitations:

1. it is not an independent state-count proof;
2. it is not a phase-space-rank proof;
3. configuration-space and phase-space variables can otherwise be mixed;
4. Einstein equations and constraints need not be algebraically independent in
   an unspecified formulation;
5. constraint propagation is a separate requirement;
6. gauge generators, gauge conditions, and canonical variables require a fully
   specified formulation;
7. the exact two-state, rank-two regional result follows solely from the
   independently derived CGI propagation system.

The current value is:

> HEURISTIC_METRIC_CROSS_CHECK: Listing six raw scalar functions and
> informally subtracting two scalar coordinate-gauge directions and two scalar
> Einstein constraints is only a consistency illustration. It is not an
> independent state-count proof or a phase-space-rank proof:
> configuration-space and phase-space variables may otherwise be mixed; the
> Einstein equations and constraints need not be algebraically independent in
> an unspecified formulation; constraint propagation is a separate
> requirement; and gauge generators, gauge conditions, and canonical
> variables must be counted in a fully specified formulation. The exact
> two-state, rank-two regional result follows solely from the independently
> derived CGI propagation system, not from this arithmetic.

The stale standalone phrase “leaves two physical first-order phase-space
functions” is absent from the current inventory. JSON
`equation_counting.formulations[1]` continues to classify every resulting
count and rank as `NOT_INDEPENDENTLY_DERIVED`. Closure Markdown §14 and §28
express the same interpretation, including configuration/phase-space,
constraint-independence and propagation, specified-gauge, and CGI-only rank
caveats. C2 therefore passes without a remaining note.

## 7. C1 regression check

C1 remains an unchanged nonblocking pass:

| ID | Complete JSON title | Author order | Journal metadata | DOI |
|---|---|---|---|---|
| DBE92 | *Covariant perturbations in a multifluid cosmological medium* | P. K. S. Dunsby, M. Bruni, G. F. R. Ellis | *ApJ* 395 (1992) 54-74 | `10.1086/171630` |
| BDE92 | *Cosmological perturbations and the physical meaning of gauge-invariant variables* | M. Bruni, P. K. S. Dunsby, G. F. R. Ellis | *ApJ* 395 (1992) 34-53 | `10.1086/171629` |

Markdown §7 retains the correct IDs, author order, journal, volume, page ranges,
and DOI values. JSON `primary_source_inventory[13]` and `[14]` retain the
complete correct citations. No obsolete DOI is present.

Minor nonblocking note: the Markdown table rows still do not print the full
article titles, while the complete JSON citations do. This is unchanged and is
not a blocker.

## 8. C3-C9 regression checks

### C3: framework-status distinction

JSON `framework_status_distinction` and Markdown §9 retain the explicit
`TARGET_STATE_STATUS` / `REGIONAL_DYNAMICS_STATUS` distinction. Frozen GM
variables remain current target language; regional perturbations remain
compatible imports; carrier geometry, embeddings, pullbacks, kernels, Green
operators, and smoothing realizations are not current regional Timescape
machinery. All 14 framework records were individually checked and none promotes
generic GR machinery merely because it can target GM variables.

### C4: branchwise undefined-object count

JSON `deficit_vector` and Markdown §32 remain bifurcated:

- `CURRENT_TIMESCAPE_ONLY` has the conservative composite-object lower bound
  \(N_{\rm undef}\ge1\);
- `EXPLICIT_IMPORTED_TRANSFER_REALIZATION` permits \(N_{\rm undef}=0\) only
  after every carrier, map, measure/Jacobian, space, smoothing or sharp
  interface, Laplacian/Green realization, boundary or decay rule, and temporal
  transport is explicitly defined.

No universal \(N_{\rm undef}=0\) or old universal vector
\((0,\ge1,\ge1,\ge1,\ge2,\mathrm{N/A})\) is presented as the Phase 1E-D
result.

### C5: mismatch components and rank

\(C_\Delta,C_Z,C_{\rm eff}\) remain the three named compatibility components.
\(C_P\) remains a separate enforced constitutive residual, not a fourth
mismatch state. Component count is explicitly not a rank proof, and the rank
status remains `RANK_NOT_COUNTABLE_BEFORE_TRANSFER_SELECTION`.

### C6: formal transfer pattern

\(T_r=L_DP_rG_r\) remains a
`FORMAL_DEFINITION_PATTERN_NOT_A_MATHEMATICALLY_DEFINED_OPERATOR`. The reports
do not claim operator existence, boundedness, continuity, self-adjointness,
correct domains/codomains, inverse-Laplacian existence or uniqueness,
commutation, CGI preservation, compatible measures/Jacobians, or transport
between time-dependent spaces. Jacobians remain assigned to transformed
measures or explicitly normalized kernels rather than automatic pointwise
scalar multiplication.

### C7: smooth and sharp branches

The smooth branch still requires partition of unity, weight regularity,
smoothing kernel or operator, scale, positivity, normalization, support,
Laplacian interaction, time transport, scale-dependence study, and declared
sharp-limit behavior.

The sharp branch still explicitly records:

\[
D_i\chi_r=\sigma_r n_i\delta_\Gamma,
\]

\[
D^2\chi_r=\sigma_r\left[(D_i n^i)\delta_\Gamma+
n^iD_i\delta_\Gamma\right],
\]

\[
D^2(\chi_rX_r)=\chi_rD^2X_r+
2D^i\chi_rD_iX_r+X_rD^2\chi_r.
\]

Interface-supported distributions, trace regularity, jump and normal-flux
conditions, and possible surface sources remain explicit. Zero spatial-volume
measure is not used to discard distributional terms.

### C8: package and readiness

The reports retain only
`REQUIRED_PACKAGE_CATEGORIES_IDENTIFIED`,
`FORMAL_PACKAGE_SKELETON_SPECIFIED`,
`CONCRETE_REALIZATION_NOT_SELECTED`, and
`PRE-PROTOTYPE_GATE_NOT_YET_EXECUTABLE`.
`REPORT_ONLY_MUST_CONTINUE` and `IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED`
remain explicit. No prototype, solver, transfer API, observational bridge,
Candidate A modification, RSD implementation, or \(f\sigma_8\) implementation
is authorized.

### C9: artifact restoration

The restoration record remains:

- artifact-free tree: `350 passed, 29 skipped`;
- 29 is the number of skipped tests, not files;
- restored ignored artifacts: 10 files;
- restored full baseline: `379 passed`.

All ten files exist, remain ignored, and have hashes equal to both the inventory
and immutable adversarial audit:

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

No artifact regeneration was required.

## 9. Surviving scientific findings

All eight findings survived the C2 edit without alteration:

1. each intrinsic regional \(k\ne0\) scalar dust sector has state
   \((\Delta_r,Z_r)\);
2. each regional sector has exact intrinsic evolution rank two, derived from
   CGI propagation;
3. the combined two-region intrinsic bulk has rank four;
4. \(C_{\rm eff}\) remains independently load-bearing in the generic mismatch
   system;
5. the number of mismatch components does not prove matching rank;
6. inverse uniqueness and nonuniqueness remain unresolved before transfer
   selection;
7. Candidate A remains non-observational;
8. no RSD, tracer, survey, \(\sigma_8\), or \(f\sigma_8\) bridge is created.

## 10. JSON structure verification

The current inventory parses successfully. Independently reproduced counts are:

- top-level keys: 34;
- framework records: 14;
- ontology records: 35;
- formal conclusions: 15.

Every formal conclusion has exactly these nine fields:

1. `classification`;
2. `source`;
3. `assumptions`;
4. `derivation_summary`;
5. `coordinate_dependencies`;
6. `frame_dependencies`;
7. `implementation_consequence`;
8. `observational_consequence`;
9. `evidence_needed_to_change_status`.

No formal conclusion has a missing or additional field.

## 11. Markdown/JSON consistency

The closure and inventory are semantically consistent for the overall verdict,
subordinate statuses, regional state and rank, heuristic metric-count status,
all framework classifications, three mismatch components, matching-rank
uncertainty, formal transfer status, branchwise deficit, unresolved inverse,
implementation readiness, artifact restoration, and prohibited
implementations.

The earlier C2 inconsistency is gone: both formats now state that the metric
arithmetic is only a heuristic consistency illustration and that exact rank two
comes exclusively from the CGI propagation system. The C1 title-presentation
asymmetry remains the already accepted nonblocking note.

## 12. Prohibited-claim search

No positive prohibited claim was found:

- the \(6-2-2\) metric arithmetic is explicitly not an independent rank proof;
- \(N_{\rm undef}=0\) occurs only under the fully defined imported branch;
- matching rank three is explicitly not inferred;
- no minimum transfer or initial-boundary package is claimed;
- no prototype or mathematical transfer operator is claimed constructed;
- inverse nonuniqueness remains unresolved;
- \(k_w=k_v=k_D=k_{\rm code}\), GM-domain/finite-infinity identity, the
  peculiar-velocity interpretation of \(Z\), and Candidate A as observational
  \(f\sigma_8\) occur only as rejected or forbidden identifications;
- 29 is explicitly a skipped-test count, not a missing-file count;
- implementation authorization remains `NOT_GRANTED`.

## 13. Test and repository preservation results

Using `PYTHONPATH` containing the tracked `src` tree and the existing external
test dependencies, cache provider disabled, bytecode writes disabled, and an
external `--basetemp`, the complete suite returned:

- Python 3.14.3: `379 passed in 10.31s`;
- Python 3.11.9: `379 passed in 11.54s`.

No ignored artifact was regenerated. `git diff --check` and
`git diff --cached --check` produced no output. HEAD and branch remained
unchanged, the index remained empty, and no tracked file changed. No Git
operation was active. No audited report, source, test, script, ignored
artifact, configuration, documentation, upstream file, Git ref, or tag was
modified. Nothing was staged, committed, tagged, pushed, merged, or published.

## 14. Final readiness statement

`ALL_TARGETED_CORRECTIONS_VERIFIED`

C2 is resolved, C1 remains an acceptable minor-note pass, and C3-C9 retain
their passing status without regression. The report-only Phase 1E-D package is
ready for a later human-authorized commit and tag. This audit performs and
authorizes neither operation.

IMPLEMENTATION_AUTHORIZATION:
NOT_GRANTED
