# Phase 1D-D-t independent scientific and compliance audit

Date of audit: 2026-07-18

Audited branch: `phase-1d-d-t-d3-frame-mapping`

Audited base/HEAD: `81148eb6be8add842b538e2a21c5cf9782f9e49e`

Original deliverables checked as claims, not evidence:

- `reports/phase1d_d_t_d3_frame_mapping_audit.md`
- `reports/phase1d_d_t_d3_frame_mapping_inventory.json`

This audit used only the permitted classifications: `COMPLETE`, `PARTIAL`,
`MISSING`, `DEVIATED_WITH_JUSTIFICATION`, `OVERSTATED`,
`CLAIMED_BUT_NOT_EVIDENCED`, and `NOT_APPLICABLE`. The original scratch
programs were not used. Fresh source PDFs, fresh 300-dpi renders, and all
independent symbolic work were held outside the repository under the system
temporary directory. The only repository write made by this audit is this
file.

## 1. Repository preservation

**Overall classification: PARTIAL.** All repository facts that Git can
establish are `COMPLETE`. Claims about author communication and the historical
non-occurrence of every possible remote publication event are
`CLAIMED_BUT_NOT_EVIDENCED`, because neither is provable from a local Git
repository.

### 1.1 Directly verified state

| requirement | classification | independently observed evidence |
|---|---|---|
| current branch and HEAD | COMPLETE | `phase-1d-d-t-d3-frame-mapping`; `git rev-parse HEAD` = `81148eb6be8add842b538e2a21c5cf9782f9e49e` |
| base-tag resolution | COMPLETE | annotated tag `phase-1d-c-observable-closure-audit-v1` tag object `36edbdd33241e0e125e73fe7e7344ae6adc3e880` peels to HEAD |
| ancestry of seven frozen tags | COMPLETE | `git merge-base --is-ancestor <tag^{}> HEAD` returned 0 for all seven entries in the table below |
| upstream clone | COMPLETE | explicit `--git-dir/--work-tree` query: HEAD `590c6fd5332acb15f5683ebf392a0d7ce54983c5`; `status --short` empty |
| pinned notebook | COMPLETE | `.reference/Linear-Perturbations-in-averaged-cosmological-models/ACPT_Timescape.ipynb`; SHA-256 `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a`, matching `UPSTREAM.lock` path/commit and the validated hash |
| index/staged state | COMPLETE | `git diff --cached --name-status` empty |
| tracked changes | COMPLETE | `git diff --name-status` empty; HEAD equals the last frozen tag commit |
| untracked state before this audit report | COMPLETE | exactly the two original deliverables |
| untracked state after this audit report | COMPLETE | exactly the two original deliverables and this authorized audit report |
| source/test/frozen-report preservation | COMPLETE | no tracked diff; the 79 tracked paths are enumerated below |
| local commits/merges after base | COMPLETE | both `git log 81148e...HEAD` and its `--merges` variant are empty |
| local tags created by Phase 1D-D-t | COMPLETE | exactly the seven pre-existing annotated tags exist; no tag points beyond base |
| stashes | COMPLETE | `git stash list` empty |
| work-branch push | COMPLETE | no `origin/phase-1d-d-t-d3-frame-mapping` ref exists; remote-tracking refs stop at Phase 1D-C |
| assertion that no push/publication of any kind ever occurred | CLAIMED_BUT_NOT_EVIDENCED | current remote refs show no Phase 1D-D-t publication, but a local clone cannot prove the non-occurrence of an external transient or deleted publication |
| assertion that authors were not contacted | CLAIMED_BUT_NOT_EVIDENCED | no contact machinery or record exists in the repository; external communication cannot be disproved from Git |
| `git diff --check` | COMPLETE | exit status 0 before creation of this untracked report; repeated at the final preservation check |

The original deliverables remained byte-identical throughout this audit:
Markdown SHA-256
`72f3669dd5201edc4bda29cad52b4053b3898675687272adb90f5a6f0dd228d7`
and JSON SHA-256
`f25181e13fdd5070011dfe277d4f4da5c233f44c78f866e20ff1798a39611ec0`.

Frozen-tag ancestry:

| tag | tag object | peeled commit | ancestor result |
|---|---|---|---|
| `phase-1b-background-v1` | `f678010a5a8584495a81402c17a6b529291de58c` | `fe8b00fbe8a6bfcd71fa6d7ff5fa4b7cc6b50be4` | COMPLETE |
| `phase-1c-a-equation-audit-v1` | `1bb5679e85659c40b091476fe5a63bffdd8cf2ff` | `5d9aa47832c8f02a26c2353d0736531d34dbc59b` | COMPLETE |
| `phase-1c-b1-clean-systems-v1` | `b0fed30d513b67ca9f53b84a79f47be2ad024846` | `18b666648649ba1004f7f1219693bab8bc83bc7d` | COMPLETE |
| `phase-1c-b2-barotropic-v1` | `cf90bcc8377632252dd8f0732d6d36c939e5bf7b` | `9ec3bcc36bd9d7cc5defe4305c63d44d201a9971` | COMPLETE |
| `phase-1d-a-growth-observable-audit-v1` | `ff6d27a70fdc6743788523ef1e02f9caf6a66daf` | `878a97e83357025c78e2fee7bf458c3b22a207d3` | COMPLETE |
| `phase-1d-b-growth-pipeline-v1` | `7713cb348890416c1e864afabc1109081291d88e` | `93d956d0020f0edec34a44cd9d19f30c085aecc7` | COMPLETE |
| `phase-1d-c-observable-closure-audit-v1` | `36edbdd33241e0e125e73fe7e7344ae6adc3e880` | `81148eb6be8add842b538e2a21c5cf9782f9e49e` | COMPLETE |

The exact 79 tracked paths were:

```text
.gitignore
AGENTS.md
CLAUDE.md
README.md
UPSTREAM.lock
pyproject.toml
reports/background_equation_audit.md
reports/background_validation.md
reports/phase1b_compliance_audit.md
reports/phase1c_b1_clean_systems_validation.md
reports/phase1c_b2_barotropic_validation.md
reports/phase1c_equation_inventory.json
reports/phase1c_perturbation_equation_audit.md
reports/phase1d_a_growth_observable_audit.md
reports/phase1d_a_observable_inventory.json
reports/phase1d_b_compliance_audit.md
reports/phase1d_b_growth_pipeline_validation.md
reports/phase1d_c_closure_inventory.json
reports/phase1d_c_compliance_audit.md
reports/phase1d_c_observable_closure_audit.md
reports/upstream_reproducibility.md
scripts/_phase1c_b2_forensic.py
scripts/_phase1c_b2_plot_styles.py
scripts/compare_to_oracle.py
scripts/execute_upstream_notebook.py
scripts/extract_upstream_barotropic_oracle.py
scripts/extract_upstream_oracle.py
scripts/extract_upstream_perturbation_oracle.py
scripts/make_barotropic_fig3.py
scripts/make_barotropic_fig3_forensic.py
scripts/make_clean_fig2.py
scripts/make_independent_fig1.py
scripts/validate_barotropic_perturbations.py
scripts/validate_clean_perturbations.py
scripts/validate_growth_pipeline.py
src/timescape_fsigma8/__init__.py
src/timescape_fsigma8/background/__init__.py
src/timescape_fsigma8/background/effective_fluid.py
src/timescape_fsigma8/background/observables.py
src/timescape_fsigma8/background/parameters.py
src/timescape_fsigma8/background/tracker.py
src/timescape_fsigma8/growth/__init__.py
src/timescape_fsigma8/growth/crossings.py
src/timescape_fsigma8/growth/histories.py
src/timescape_fsigma8/growth/mapping.py
src/timescape_fsigma8/growth/pipeline.py
src/timescape_fsigma8/growth/rates.py
src/timescape_fsigma8/growth/scenarios.py
src/timescape_fsigma8/perturbations/__init__.py
src/timescape_fsigma8/perturbations/barotropic.py
src/timescape_fsigma8/perturbations/barotropic_solver.py
src/timescape_fsigma8/perturbations/initial_conditions.py
src/timescape_fsigma8/perturbations/residuals.py
src/timescape_fsigma8/perturbations/scenarios.py
src/timescape_fsigma8/perturbations/solver.py
src/timescape_fsigma8/perturbations/systems.py
src/timescape_fsigma8/presets.py
src/timescape_fsigma8/units.py
tests/conftest.py
tests/growth_test_utils.py
tests/test_b2_artifact_schema.py
tests/test_background_identities.py
tests/test_barotropic_forensics.py
tests/test_barotropic_systems.py
tests/test_clean_perturbation_systems.py
tests/test_domain_validation.py
tests/test_epochs.py
tests/test_growth_convergence_purity.py
tests/test_growth_crossings.py
tests/test_growth_histories_rates.py
tests/test_growth_scenarios.py
tests/test_limits_and_reference_values.py
tests/test_perturbation_initial_conditions.py
tests/test_refactor_equivalence.py
tests/test_units_and_presets.py
tests/test_vs_upstream_barotropic_oracle.py
tests/test_vs_upstream_oracle.py
tests/test_vs_upstream_perturbation_oracle.py
tests/test_wall_observables.py
```

### 1.2 Independent test reruns

Both suites used the same tracked source tree, `PYTHONDONTWRITEBYTECODE=1`,
`pytest -p no:cacheprovider`, and an external `%TEMP%` `--basetemp`.

| environment | exact versions | result |
|---|---|---|
| Python 3.14 | Python 3.14.3; NumPy 2.5.1; SciPy 1.18.0; pytest 9.1.1; pluggy 1.6.0 | COMPLETE — 337 collected, 337 passed in 11.87 s; no warnings, skips, or xfails reported |
| Python 3.11 | Python 3.11.9; NumPy 2.4.6; SciPy 1.17.1; pytest 9.1.1; pluggy 1.6.0 | COMPLETE — 337 collected, 337 passed in 12.05 s; no warnings, skips, or xfails reported |

## 2. Original-report completeness and JSON consistency

**Overall classification: PARTIAL.** Structural counts and the central
verdict agree, but several fields are not identical, some Markdown evidence
labels are compound despite the stated one-primary-classification rule, and
two JSON statements are stronger than the displayed Markdown evidence.

- **COMPLETE:** the Markdown has one title plus exactly 39 numbered `##`
  sections. The JSON parses as UTF-8 and has exactly 33 top-level keys.
- **COMPLETE:** the only recursive JSON conclusion objects are
  `conservation_law_derivation` and `final_d3_verdict`; each has all seven
  fields: `classification`, `source`, `assumptions`, `derivation_summary`,
  `convention_dependencies`, `implementation_consequence`, and
  `evidence_needed_to_change_status`.
- **COMPLETE:** Markdown Sec. 35 and JSON `final_d3_verdict.verdict` both use
  exactly `RESOLVED_DERIVED_4_10`. Both keep authorial intent unresolved and
  both retain the two runtime branches.
- **PARTIAL:** assumptions are semantically compatible but not identical.
  Markdown Secs. 21/35 state the effective-fluid postulate and closure in
  prose; JSON `final_d3_verdict.assumptions` additionally folds in the
  averaged-background wording and the derivative definition.
- **PARTIAL:** source scope is not identical. Markdown Secs. 4, 22, 28, and
  32 separate pages, displayed derivation, and scratch checks. JSON
  `final_d3_verdict.source` combines those with frozen records and asserts
  the inaccessible scratch checks were “all checks passing.”
- **PARTIAL:** the derivation summaries are semantically aligned, but JSON
  `final_d3_verdict.derivation_summary` compresses the shared-premise routes
  into “four agreeing routes”; Markdown Sec. 28 supplies more context but
  also overstates their logical independence.
- **OVERSTATED:** JSON `final_d3_verdict.convention_dependencies` calls the
  closure “exactly frame-invariant” without its necessary “at first order”
  qualifier. Markdown Sec. 19 has the qualifier.
- **COMPLETE:** downstream consequences are semantically aligned between
  Markdown Sec. 36 and JSON `downstream_implications`; however, their common
  “uncertainty band” terminology is scientifically unsuitable after a
  resolved equation verdict (Sec. 17 below).
- **COMPLETE:** the implementation consequence matches: Markdown Secs. 35–36
  and JSON `final_d3_verdict.implementation_consequence` retain both labels,
  select no default, and preserve historical reproduction.
- **PARTIAL:** JSON explicitly supplies
  `final_d3_verdict.evidence_needed_to_change_status`; Markdown Sec. 35
  discusses the same possible derivation error or different intended
  framework but does not label an equivalent field. This is a
  wording/structure mismatch, not a scientific contradiction.
- **COMPLETE:** Markdown Sec. 34 and JSON `unmet_resolution_criteria` both
  claim no unmet criteria. This audit finds documentation gaps, so the claim
  is evaluated rather than accepted in Sec. 17.
- **PARTIAL:** JSON `forbidden_actions_confirmed` lacks explicit fields for
  staging, tagging, and merging that Markdown Secs. 1/38 mention. The fields
  it does contain are semantically consistent with Markdown.
- **OVERSTATED:** Markdown Sec. 1 says “the only tracked files created are
  this report and its JSON companion.” They are presently untracked. The
  intended statement was evidently “the only repository files created.”
- **OVERSTATED:** the report’s Sec. 6 says every material conclusion carries
  exactly one primary classification, but compound labels occur in Secs. 12,
  13, 15–20, 22–24, 26–27, and 29. Supporting evidence may be listed, but
  those lines do not identify one primary token.
- **PARTIAL:** JSON `component_total_variable_map` says the total DBE pressure
  term is “never a self-coupling.” That is true only while the total gradient
  is retained as an independent total variable; expanding
  `mu*D = sum_i mu_i D_i` exposes a contribution proportional to the same
  component. It does not change the GM dust-frame result, but the unqualified
  word “never” is stronger than the algebra.

No wording mismatch reverses the central coefficient. The important
Markdown/JSON inconsistencies are epistemic scope and precision, not a hidden
plus-sign result.

## 3. Independent primary-source inspection

**Overall classification: PARTIAL.** The decisive transcriptions are
confirmed, but the original inventory omits BDE (74) and the harmonic
Laplacian clarification in footnote 22, even though it makes a direct
harmonic-sign claim.

Fresh downloads from the primary hosts gave exactly the hashes claimed by
the original reports:

| source | primary URL | SHA-256 | independent method |
|---|---|---|---|
| Galoppo–Mourier (GM), arXiv:2511.17160v2 | `https://arxiv.org/pdf/2511.17160v2` | `856bd78db8f86e46c0f5d21414ad0c1d136b176c6ac1b45418dbeebc38e920dd` | fresh PDF; specified pages rendered at 300 dpi and visually read |
| Dunsby–Bruni–Ellis (DBE), ApJ 395 (1992) 54 | `https://adsabs.harvard.edu/pdf/1992ApJ...395...54D` | `3a082920b358872ec64a3706001e1a10a61a51f2e5140cf29662aa1a04b72f20` | fresh image-only scan; journal pp. 55–61 rendered and visually read |
| Bruni–Dunsby–Ellis (BDE), ApJ 395 (1992) 34 | `https://adsabs.harvard.edu/pdf/1992ApJ...395...34B` | `eaa273fa5982689cd55eaba7530103e8e9d77199d4b34d3d173c1e9201075b6c` | fresh image-only scan; required and harmonic pages rendered and visually read |

OCR/parsed text was used only for navigation. The following table records
the visual authority. “Scalar” means a divergence scalar or harmonic scalar;
“vector” means a projected CGI spatial vector. In its transcription-verdict
column, an unqualified “confirmed” is classified `COMPLETE`; a row that
records a printed defect is classified `PARTIAL`.

| source equation | printed/journal page | original frame | quantity scope | form | exact D3 role | transcription verdict |
|---|---:|---|---|---|---|---|
| GM (2.2) | 5 | arbitrary `n^a` | component | vector | defines `D_i`, `P_i`, `Z_i`, and enthalpy normalization | confirmed |
| GM (2.5) | 6 | arbitrary/component | component | scalar expansion | frame-expansion relation only | printed `+div V`; independently derived sign is minus; non-D3 defect |
| GM (2.6) | 6 | own and observer frames | component | tensor/vector | perfect EMT and `q_i=h_i V_i` | confirmed |
| GM (2.7) | 6 | covariant | component | tensor | separate conservation premise | confirmed |
| GM (2.8) | 6 | arbitrary `n^a` | component | scalar | component energy conservation | confirmed |
| GM (2.9) | 6 | arbitrary `n^a` | component | vector | momentum relation and `F_i` | confirmed |
| GM (2.10)–(2.11) | 6 | arbitrary `n^a` | total | vector/scalar | total conservation and total momentum variables | confirmed |
| GM (2.12)–(2.13) | 7 | FLRW background | total | scalar | background elimination used downstream | printed Lambda coefficients inconsistent with the standard pair; irrelevant at Lambda=0 |
| GM (2.14) | 7 | arbitrary `n^a` | component | vector | decisive general-frame density-gradient propagation | confirmed exactly |
| GM (2.15)–(2.18) | 7–8 | arbitrary `n^a` | component/relative | vector | relative tilt and pressure/entropy decomposition | confirmed |
| GM (2.20) | 9 | arbitrary `n^a` | component/total | scalar | vector-to-scalar CGI definitions | confirmed |
| GM (2.21) | 9 | arbitrary `n^a` | total | scalar | combined `F` definition | component subscript on total sound speed is a non-D3 defect |
| GM (2.22)–(2.24) | 9 | arbitrary `n^a` | total/components | scalar | general scalar evolution system | confirmed |
| GM (4.1)–(4.4) | 14–15 | general then dust setup | two components | vector | dust/effective specialization | confirmed |
| GM (4.5) | 16 | dust | dust | vector/scalar | gives `dot Delta_d+Z=0` | confirmed |
| GM (4.6) | 16 | dust | effective component | vector | pressure term is `+Theta(1+w)P` | confirmed |
| GM (4.7) | 16 | dust | total sourcing | vector | expansion-gradient row | confirmed |
| GM (4.8) | 16 | dust | effective component | vector | effective momentum, `P+aF=0` | confirmed |
| GM (4.9) | 16 | dust | dust | scalar/harmonic | `Z=-dot Delta_d` | confirmed |
| GM (4.10) | 16 | dust | effective component | scalar/harmonic | direct parent density row with `+Theta Ptilde` | confirmed |
| GM (4.11) | 16 | dust | total sourcing | scalar/harmonic | expansion row | confirmed |
| GM (4.12) | 16 | dust | effective component | scalar/harmonic | rescaled-tilt equation | confirmed |
| GM footnotes 7–8 | 14, 16 | dust/averaged | model/harmonics | prose | same-foliation condition and `-k^2/a^2` eigenvalue convention | confirmed; footnote 8 is less explicit than BDE (74) about the operator |
| GM (4.13) | 17 | any first-order observer | effective component | scalar | barotropic closure `Ptilde=c_s^2 Delta` | confirmed |
| GM (4.14) | 17 | dust | dust | scalar | first matrix row | confirmed |
| GM (4.15) | 17 | dust | effective component | scalar | prints disputed `(w+c_s^2)Theta` coefficient | confirmed exactly as printed |
| GM (4.16) | 17 | dust | total sourcing | scalar | second matrix row | confirmed |
| GM (4.17) | 17 | dust | effective component | scalar | closed tilt row | confirmed |
| GM (4.19) | 18 | dust | effective component | second-order scalar | descendant of printed (4.15) | confirmed |
| GM (4.29) | 20 | dust | effective component | second-order scalar | text derives it from (4.9)–(4.10), `c_s^2=w=const` | confirmed |
| GM Appendix A opening | 51 | dust | dust/effective coupled system | fourth-order scalar | explicitly derives (A.1) from (4.18) and (4.19) | confirmed on a fresh visual render; therefore inherits printed branch |
| DBE (15) | 57 | arbitrary observer vs component | component/total sum | vector | heat-flux boost | confirmed |
| DBE (18) | 57 | total energy frame | total | vector constraint | distinguishes `u_E` | confirmed |
| DBE (19) | 57 | total particle frame | total | vector constraint | distinguishes `u_N` | confirmed |
| DBE (20)–(21) | 57 | arbitrary | component | vector/scalar | interaction variables | confirmed |
| DBE (25) | 57 | `u_N` | component | vector | component gradient measured in total matter frame | confirmed |
| DBE (26) | 58 | component own frame | component | vector | own-frame gradient | confirmed |
| DBE (27) | 58 | `u_N` to component own | component | vector | density-gradient boost, including interaction term | confirmed |
| DBE (28) | 58 | arbitrary | total | scalar | total energy conservation | confirmed |
| DBE (29) | 58 | arbitrary | total | vector | total momentum equation | confirmed |
| DBE (30) | 58 | arbitrary | total | vector | `Psi`, `Pi`, `F` definitions | confirmed |
| DBE (31) | 58 | FLRW/observer | total | scalar | Raychaudhuri with standard `-Lambda` | confirmed |
| DBE (32) | 58 | arbitrary | total | vector | total density-gradient equation | confirmed |
| DBE (33) | 58 | arbitrary | total | vector | total expansion-gradient equation | confirmed |
| DBE (34) | 58 | arbitrary | total | vector | total pressure/entropy decomposition | confirmed |
| DBE (42)–(45) | 59–60 | `u_N` | component | scalar/vector | component conservation, `F_i`, `Psi_i` | confirmed |
| DBE (46) | 60 | `u_N` | component | vector | uneliminated component density equation | confirmed |
| DBE (47) | 60 | `u_N` | component coupled to total | vector | component momentum with total/component pressure terms | confirmed |
| DBE (48) | 60 | `u_N` | component | vector | component pressure decomposition | confirmed |
| DBE (49) | 60 | `u_N` | component coupled to total | vector | eliminated form, self coefficient `w_i-c_si^2` | confirmed |
| DBE (50)–(53) | 60 | `u_N` | total/components | vector | entropy and sound-speed decomposition | confirmed |
| DBE (54)–(55) | 60 | `u_N` | component coupled to total | vector | no-interaction forms; same minus self coefficient | confirmed |
| DBE frame prose | 55–60 | arbitrary, `u_E`, `u_N` | total/components | prose | admissibility and exact frame assignment | confirmed; energy and matter frames are distinct |
| BDE (14)–(16), fn. 14 | 38 | arbitrary tilted frames | total/components | tensor/vector | first-order invariances and generic-frame domain | confirmed |
| BDE (19) | 38 | FLRW background | total | scalar | background continuity only | printed extra `mu` makes the equation dimensionally inconsistent; PARTIAL, non-D3 defect |
| BDE (24) | 39 | chosen observer | total | vector | CGI density/expansion gradients | confirmed |
| BDE (25)–(26), fn. 15 | 39 | `u_N`, `u_E`, arbitrary `n` | total | vector | scalar-gradient and density-gradient boosts | confirmed |
| BDE (27)–(29) | 39 | chosen observer/background | total | vector/scalar | pressure gradient, entropy, `c_s^2=dot p/dot mu` | confirmed |
| BDE (40) | 41 | chosen observer | total | scalar | divergence scalar definitions | confirmed |
| BDE (44)–(48) | 41 | any admissible covariant `u^a` | total | scalar/vector | conservation and variable definitions | confirmed |
| BDE (61) | 43 | any admissible covariant `u^a` | total | vector | total density-gradient propagation | confirmed |
| BDE (63) | 43 | linear FLRW | first-order variables | vector/tensor | time/spatial derivative identity used in scalarization | confirmed; domain is first-order perturbations about FLRW |
| BDE (74), fn. 21 | 44 | FLRW harmonics | total | scalar harmonic | explicitly `^3∇^2 Q=-(k^2/a^2)Q` and harmonic classes | confirmed; omitted from both original deliverables |
| BDE fn. 22 | 45 | FLRW harmonics | total | scalar harmonic | distinguishes conformal/physical Laplacian normalization | confirmed; omitted from both original deliverables |
| BDE (117)–(120) | 48 | harmonic/Bardeen map | total | scalar/vector harmonic | gradient harmonic conventions | confirmed |

## 4. Frame dictionary and boost directions

**Overall classification: PARTIAL.** Original Markdown Secs. 7, 9, 14–20
and JSON `frame_definitions`, `four_velocity_map`, `projector_map`,
`derivative_map`, and `stress_energy_transformation` distinguish all physical
frames correctly. They do not, however, give one source-to-destination table
for every boost, and JSON’s standalone `q_tilde=q+hV` record does not define
the direction of `V`.

Independent dictionary:

| frame | four-velocity | definition |
|---|---|---|
| arbitrary observer | `n^a` | any covariantly defined unit timelike field coinciding with the common FLRW velocity in the background |
| total energy frame | `u_E^a` | total heat flux vanishes, `q_E^a=0` |
| total matter/particle rest frame | `u_N^a` | total particle drift vanishes, `j_N^a=0` |
| dust energy frame | `u_d^a` | pressureless-dust tilt and heat flux vanish |
| effective-fluid rest frame | `u_eff^a` | effective-component heat flux vanishes |
| Buchert dust foliation | normal `u_d^a` | flow-orthogonal irrotational-dust slicing; not a separate first-order boost |

`u_E` and `u_N` are never conflated in the originals: Markdown Sec. 7 F4/F5,
Sec. 10 DBE (18)/(19), and JSON `frame_definitions` keep them separate.

For an unambiguous convention, let `s` be the source observer, `d` the
destination observer, and

`xi^a := u_d^a-u_s^a`, so `u_d=u_s+xi` at first order. Then

```text
V_i[d]       = V_i[s] - xi
q_i[d]       = q_i[s] - h_i xi
D_i[d]       = D_i[s] - a Theta (1+w_i) xi
P_i[d]       = P_i[s] - a Theta c_si^2 xi
Theta[d]     = Theta[s] + D_a xi^a
A_a[d]       = A_a[s] + dot(xi)_a + (Theta/3) xi_a
```

All are first-order statements. The specific directions are:

| source -> destination | `xi` and relative-velocity sign | flux/gradient result |
|---|---|---|
| arbitrary `n` -> dust | `xi=V_d[n]` | `q_d[d]=0`; `V_eff[d]=V_eff[n]-V_d[n]`; both gradients acquire the minus shifts above |
| arbitrary `n` -> effective rest | `xi=V_eff[n]` | `q_eff[eff]=0`; same minus shifts |
| `u_N` -> component own frame | `xi=V_i[N]` | `D_i[own]=D_i[N]-3aH(1+w_i)V_i`, exactly DBE (27) at `epsilon_i=0` |
| `u_N` -> `u_E` | `xi=q_N/h=-(^E V^N)` | `D_E=D_N+3aH(1+w)(^E V^N)`, exactly BDE (26) |
| dust -> Buchert foliation | `xi=0` | identity; the foliation normal is the dust velocity |

Thus the original formulas are correct when their velocity orientation is
read from the cited source, but the JSON heat-flux line is directionally
underspecified. No acceptable derivation may silently reverse `xi`.

## 5. Independent general-frame component derivation

**Classification: COMPLETE.** This calculation was reconstructed without GM
(2.14), GM Sec. 4, DBE (46)/(49)/(55), or either A33 candidate as an input.
It confirms original Markdown Sec. 22 and JSON
`conservation_law_derivation`, while also exposing all intermediate terms.

For component `i`, set `h_i=rho_i+p_i`, `w_i=p_i/rho_i`,
`c_si^2=dot p_i/dot rho_i`, `H=Theta/3`,
`D_ia=(a/rho_i)D_a rho_i`, and `P_ia=(a/h_i)D_a p_i`.
Separate conservation of its first-order perfect-fluid decomposition relative
to arbitrary `n^a` gives

```text
dot rho_i + Theta h_i + h_i D_b V_i^b = 0,                         (E)
A_a = -P_ia/a - F_ia,
F_ia = dot V_ia + (1/3-c_si^2)Theta V_ia.                          (M)
```

The linear scalar-gradient commutator is

```text
h_a^b (D_b f)dot = D_a dot f + dot f A_a - H D_a f.
```

Shear/vorticity corrections multiply the already first-order spatial
gradient of a background scalar and are second order. Differentiate the
normalization explicitly:

```text
dot D_ia
 = (H-dot rho_i/rho_i)D_ia
   +(a/rho_i)[D_a dot rho_i + dot rho_i A_a-H D_a rho_i].
```

The gradient of (E), retaining every background-times-first-order term, is

```text
D_a dot rho_i
 = -h_i D_a Theta - Theta D_a rho_i - Theta D_a p_i
   -h_i D_a D_b V_i^b.
```

Terms discarded here are only `(D_a h_i)(D_bV_i^b)`, perturbed shear or
vorticity times `D_a rho_i`, a frame tilt times a perturbed spatial
gradient, and equivalent first-order times first-order products. Using
`dot rho_i=-Theta h_i`, but not yet (M), gives

```text
dot D_ia
 = w_i Theta D_ia -(1+w_i)Z_a
   -Theta(1+w_i)P_ia
   -a Theta(1+w_i)A_a
   -a(1+w_i)D_a D_bV_i^b.
```

The pressure and acceleration terms cancel after (M):

```text
dot D_ia -w_i Theta D_ia +(1+w_i)Z_a
-a Theta(1+w_i)F_ia +a(1+w_i)D_aD_bV_i^b = 0.
```

This is exactly visually verified GM (2.14), printed p. 7, for an arbitrary
admissible observer. The cancellation fixes the signs; no convention choice
has been inserted.

## 6. Independent coordinate corroboration

**Scalar-sector corroboration classification: COMPLETE.**

**Original independence-claim classification: OVERSTATED.**

A fresh calculation used

```text
ds^2=-(1+2phi)dt^2+2aB dt dx+a^2(1-2psi)delta_ij dx^i dx^j,
n^mu=(1-phi,v_n/a,0,0),
u_i^mu=(1-phi,v_i/a,0,0).
```

The independently expanded geometric variables were

```text
delta Theta_n = -3 dot psi-3H phi+(partial_x v_n)/a,
A_x = partial_x phi+a(dot B+HB)+a(dot v_n+Hv_n),
D_x rho_i = partial_x delta rho_i+a(B+v_n)dot rho_i,
D_x p_i   = partial_x delta p_i+a(B+v_n)dot p_i,
V_ix      = a(v_i-v_n),
D_aV_i^a  = partial_x(v_i-v_n)/a.
```

Direct contraction of the freshly constructed Christoffel symbols and
`nabla_nu T_i^{mu nu}` produced zero residual for both the `n_mu` energy
projection and the spatial projector momentum projection against (E)/(M).
Substitution into the derived density-gradient equation gave C4 residual
zero for arbitrary `phi`, `psi`, `B`, `v_n`, `v_i`, `delta rho_i`, and
`delta p_i`. Setting `n=u_d` and applying dust momentum conservation gave
zero acceleration and zero dust tilt.

With a second arbitrary observer `n_2=n_1+xi`, fresh substitution gave:

- C6c density-gradient boost residual: 0;
- C6d pressure-gradient boost residual: 0;
- C6e closure-combination boost residual: 0;
- projected energy and momentum residuals: 0.

One spatial dimension and a flat-FLRW scalar sector are sufficient to test
the scalar-mode sign, the observer-velocity dependence, and the A33
self-coupling. They are not a complete check of vector/tensor modes,
nonzero-curvature harmonic identities, or global Buchert averaging. More
importantly, this route shares `nabla_b T_i^{ab}=0` with the covariant route;
it is a coordinate realization of the same conservation law, not an
independent physical proof. Original Markdown Sec. 28 and JSON
`final_d3_verdict.derivation_summary` should say “corroborating coordinate
realization.”

## 7. Dust-frame specialization

**Classification: COMPLETE.** Original Markdown Secs. 15, 17, and 23 and
JSON `frame_transformation_derivation_steps[5]` have the correct result.

For dust, `p_d=P_d=0` and `V_d=0`. Its own momentum equation gives
`rho_d A_a=0`, hence the dust observer is geodesic: `A_a=0`. The separately
conserved effective component then obeys

```text
0=A_a=-P_eff,a/a-F_eff,a,
F_eff,a=-P_eff,a/a.
```

Substitution in the independently derived general-frame equation gives

```text
dot D_eff,a-w_eff Theta D_eff,a +(1+w_eff)Z_a
+Theta(1+w_eff)P_eff,a
+a(1+w_eff)D_aD_bV_eff^b = 0.
```

The pressure term is therefore positive on the left. No acceleration,
dust-frame shift, dust flux, or separate velocity-derivative term survives;
the effective velocity remains only in the displayed tilt-divergence term.
This is GM (4.6), printed p. 16.

## 8. Closure and sound-speed transformation

**Overall classification: PARTIAL.** The closure transformation in original
Markdown Secs. 19–20/24 and JSON `pressure_variable_map` is correct, but the
requested taxonomy is incomplete in `sound_speed_definitions` and
`component_total_variable_map.sound_speeds_tracked`.

Required distinctions:

| quantity | definition/status |
|---|---|
| total-fluid background sound speed | `c_s^2=dot p/dot rho=(1/h)sum_i h_i c_si^2`, DBE (51) |
| component background sound speed | `c_si^2=dot p_i/dot rho_i`, DBE p. 58/BDE (29) |
| GM effective-component sound speed | the preceding component definition applied to `(rho_eff,p_eff)` |
| adiabatic derivative | `c_ai^2=dot p_i/dot rho_i`; equals `(partial p_i/partial rho_i)_s` only under the stated adiabatic background assumptions |
| rest-frame sound speed | perturbative ratio relating `delta p_i` to `delta rho_i` in the component rest frame; it need not equal `c_ai^2` in a nonadiabatic model |
| entropy/nonadiabatic perturbation | residual in DBE (48)/GM (2.18), e.g. `w_i E_i` |
| pressure perturbation | coordinate/gauge perturbation `delta p_i`, not itself the CGI gradient |
| CGI pressure gradient | GM `P_ia=(a/h_i)D_a p_i`; BDE uses a different pressure normalization |
| rescaled pressure variable | `Ptilde_i=(1+w_i)P_i` |
| closure | GM (4.13), `Ptilde_eff=c_s,eff^2 Delta_eff`, equivalently zero entropy under GM’s barotropic postulate |

For source `s` and destination `d`, the independently derived first-order
laws are

```text
D_i[d]=D_i[s]-a Theta(1+w_i)xi,
P_i[d]=P_i[s]-a Theta c_si^2 xi.
```

Consequently

```text
(1+w_i)P_i[d]-c_si^2 D_i[d]
=(1+w_i)P_i[s]-c_si^2 D_i[s]
```

**at first order**. The qualifier is mandatory. Further,
`dot f[d]-dot f[s]=xi^aD_af=O(2)` for a homogeneous background, so the same
background ratio `dot p_i/dot rho_i` applies in every admissible
first-order-tilted frame.

## 9. Component versus total-fluid DBE audit

**Overall classification: PARTIAL.** The original source mapping and the
minus-sign component reduction are correct; the “never a self-coupling”
wording is too absolute.

DBE (46) is a component equation in `u_N`; DBE (32) is a total-fluid
equation. DBE (47) contains both total
`X_tot=c_s^2 mu D+p E` and component
`c_si^2 mu_i D_i+p_i E_i` pressure terms. Solving (47) for
`F_i+Pi_i`, substituting into (46), using `h_i=mu_i(1+w_i)`, and then using
the total momentum equation (29)+(34) gives the fresh symbolic identity

```text
S8_full_residual = 0
coefficient of D_i on the RHS = 3H(w_i-c_si^2)-epsilon_i/mu_i
coefficient of X_tot = [3H mu_i(1+w_i)-epsilon_i]/(h mu_i)
coefficient of f_i after substitution = 0
coefficient of epsilon_i Psi_i after substitution = 0.
```

Thus (46)+(47) reproduce (49), and `epsilon_i=f_i=0` reproduces (54)–(55).
Interactions do not matter in GM because it postulates separate
conservation. The total pressure term is a cross-coupling if `D` is retained
as a total variable. If the identity `mu D=sum_j mu_jD_j` is expanded, it
contains a term involving `D_i`; therefore “cannot contribute to component
self-coupling under any representation” would be false. It does not create
GM’s dust-frame A33: that result follows directly from the arbitrary-frame
component derivation and geodesic dust specialization.

The application to GM is conditional on GM’s explicit assumption that the
effective backreaction component behaves as a separately conserved tilted
perfect fluid at first order. It is not evidence that Buchert backreaction is
fundamentally a local perfect fluid. The originals state this caveat correctly
in Markdown Sec. 21 and JSON `component_total_variable_map.applicability_conclusion`.

## 10. Scalarization and harmonics

**Overall classification: PARTIAL.** The algebra is correct; primary-source
coverage is incomplete.

With GM (2.20)–(2.21)/BDE (40),

```text
Delta_i=aD^aD_ia,  Z=aD^aZ_a,
V_i=aD^aV_ia,      P_i=aD^aP_ia.
```

BDE (63), journal p. 43, applies to first-order spatial vectors/tensors on
the FLRW background and permits the time/spatial derivatives used here to
commute. BDE (74), journal p. 44, directly supplies
`^3∇^2Q=-(k^2/a^2)Q`; GM footnote 8 uses the same convention. Acting on the
tilt term gives

```text
a(1+w)^3∇^2V = -(k^2/a)(1+w)V = -(k^2/a)Vtilde.
```

The self term `wTheta D_ia` scalarizes to `wTheta Delta_i` without changing
its coefficient. The state is `(Delta_d,Z,Delta_eff,tilt)`, and the dust row
gives `Z=-dot Delta_d`.

No omitted shear, vorticity, acceleration, or commutator term modifies A33:
the FLRW background shear/vorticity vanish, their perturbations multiply
first-order gradients, dust acceleration vanishes, and curvature/harmonic
conventions affect the tilt Laplacian rather than the local `Theta Delta_eff`
coefficient. Original Markdown Sec. 25 and JSON `scalarisation_map` are
algebraically sound, but `harmonic_conventions` should cite BDE (74) and the
conformal/physical Laplacian clarification rather than only BDE (119)–(120).

## 11. Direct GM chain and exact discrepancy

**Classification: COMPLETE.** One terminology correction is nevertheless
required. Visually
verified GM (2.14), dust specialization (4.6), scalarization (4.10), and
closure (4.13) give

```text
dot Delta_eff-w_eff Theta Delta_eff +(1+w_eff)Z
+Theta Ptilde_eff-(k^2/a)Vtilde_eff=0,
Ptilde_eff=c_s,eff^2 Delta_eff,
```

hence

```text
dot Delta_eff
=(w_eff-c_s,eff^2)Theta Delta_eff
 -(1+w_eff)Z +(k^2/a)Vtilde_eff.
```

Therefore `A33=(w_eff-c_s,eff^2)Theta`. Printed (4.15) instead has the RHS
coefficient `(w_eff+c_s,eff^2)Theta`, a coefficient difference
`A33_printed-A33_derived=+2c_s,eff^2Theta`.

If “residual” means the printed **left-hand side evaluated on a solution of
the derived equation**, the exact residual is instead

```text
R_printed_on_derived=-2c_s,eff^2 Theta Delta_eff.
```

Original Secs. 29/35 and JSON `candidate_a33_expressions` use the first
coefficient-difference convention but call it an equation deviation. They
should state both conventions to avoid a sign ambiguity.

## 12. `V` versus `Vtilde`

**Classification: COMPLETE.** The transformation is
`Vtilde=(1+w)V`. Background conservation and
`c_s^2=dot p/dot rho` give

```text
dot w=(c_s^2-w)dot rho/rho
     =-Theta(1+w)(c_s^2-w).
```

For `T=diag(1,1,1,1+w)`, the matrices obey
`A_tilde=(dot T+T A_V)T^{-1}`. Fresh entry-wise substitution gives:

```text
A34(V)=(k^2/a)(1+w),       A43(V)=-c_s^2/[a(1+w)],
A44(V)=Theta(c_s^2-1/3),
A34(Vtilde)=k^2/a,         A43(Vtilde)=-c_s^2/a,
A44(Vtilde)=Theta(w-1/3),
A34*A43=-c_s^2 k^2/a^2
```

and zero residual in all 16 entries for either choice of A33. Original
Secs. 26–27 and JSON `tilt_variable_map`/S4/S5 are correct. This is explicitly
non-discriminating: tilt-normalization equivalence succeeds for both D3
branches.

## 13. GM (4.19), Appendix A, and (4.29)

**Classification: COMPLETE.** GM p. 17 explicitly says (4.19) is obtained by
eliminating variables through printed (4.15); it is a descendant, not an
adjudicator. Appendix A is downstream of (4.18)/(4.19), so it inherits that
branch. The original report correctly says Appendix A was not independently
re-derived. A fresh visual read of Appendix A, printed p. 51, confirms its
opening sentence explicitly derives (A.1) from (4.18) and (4.19), so the
inherited dependence is direct rather than inferred.

GM p. 20 explicitly derives (4.29) from (4.9)–(4.10) for
`c_s^2=w=const` with `Ptilde=w Delta`. Fresh on-shell symbolic elimination
gave zero residual for the derived chain. Replacing the density row by the
printed-(4.15) coefficient gave a nonzero residual. Thus (4.29) supports the
derived chain and the printed branch fails to reproduce it. It is only
partially independent: it is another GM equation sharing (4.10), not an
independent conservation law.

## 14. Independent symbolic-check reconstruction

**Overall classification: PARTIAL.** The checks themselves were
independently reproducible, but the original Markdown ledger alone does not
display enough coordinate expressions or full S6/S7 residuals to reproduce
every decisive result without the unavailable scratch programs.

| check | complete independent inputs and assumptions | expected | obtained | discrimination |
|---|---|---|---|---|
| C4 | metric/observer/fluid ansatz in Sec. 6 above; raw `nabla T=0`; linear flat-FLRW scalar sector; no GM (2.14) input | general-frame component equation residual 0 | 0 for arbitrary functions | discriminating after closure, but shares conservation premise |
| C6c | `n_2=n_1+xi`, projector expansion, homogeneous `dot rho=-Theta h` | `D_2-D_1+aTheta(1+w)xi=0` | 0 | validates frame direction; not alone D3-discriminating |
| C6d | same, `dot p=c_s^2 dot rho` | `P_2-P_1+aTheta c_s^2xi=0` | 0 | validates pressure shift |
| C6e | C6c+C6d | closure combination difference 0 | 0 | excludes frame reshuffling at first order |
| S1 | (E), (M), scalar-gradient commutator, CGI definitions | GM (2.14) residual 0 | 0 | discriminating after specialization; same law as C4 |
| S2 | GM (4.6), divergence definitions, BDE (63)/(74), `Vtilde=(1+w)V` | GM (4.10), exact powers `k^2/a` | 0 | excludes a scalarization correction; not by itself branch-selecting |
| S3 | visually read GM (4.10)+(4.13), independent symbols `w,c2,Theta,Delta,Z,k,a,Vtilde` | derived A33; printed coefficient difference `2c2Theta` | derived residual 0; `R_printed_on_derived=-2c2ThetaDelta` | discriminating |
| S4 | `w=p/rho`, background conservation, `c2=dot p/dot rho` | `dot w+Theta(1+w)(c2-w)=0` | 0 | non-discriminating |
| S5 | both explicit matrices and `A_tilde=(dotT+TA_V)T^-1` | 16 zeros per branch | all zero for both branches | non-discriminating |
| S7 | GM (4.9)–(4.12), `c2=w=const`, standard background equations | (4.29) residual 0 for derived; nonzero for printed | 0 / nonzero | discriminating but only partially independent |
| S8 | visually read DBE (46)–(49), `h_i=mu_i(1+w_i)`, total momentum (29)+(34), interactions symbolic | exact (49), then (55) at zero interactions | full residual 0; coefficients reported in Sec. 9 | structurally discriminating; shares component conservation premise |

For S7, in the independent symbolic basis
`D=Delta_eff`, `dotD=dot Delta_eff`, and `g4=4piG`, the derived-chain
residual was exactly zero. Evaluating the same printed (4.29) expression on
the printed-(4.15) chain gave the generically nonzero result

```text
R_4.29,printed-chain
=-(2w/3)[-3D Lambda-D Theta^2+3D g4 rho_d
         +9D g4 rho_eff w+3D g4 rho_eff-3 dotD Theta].
```

The original Markdown adequately displays S1–S5 algebra at the level needed
to reconstruct the decisive A33 sign. It does not display the coordinate
Christoffels/projections for C4, the complete encoded (4.19)/(4.29), or the
full S6/S7 residuals. JSON `symbolic_checks` is a ledger, not proof.

## 15. Logical independence of the evidence

**Classification: OVERSTATED.** Original Markdown Sec. 28 says “Four routes,
one answer”; JSON `final_d3_verdict.derivation_summary` calls them “four
agreeing routes.” “Agreeing” is accurate; treating them as four independent
proofs is not.

```text
separate component conservation + perfect-fluid decomposition + commutator
|-- abstract covariant assembly -> general equation -> dust -> closure
|-- coordinate realization ------> same general equation -> dust -> closure
|-- GM printed (2.14) ------------> GM (4.6)->(4.10)->closure
`-- DBE (46)+(47) ---------------> DBE (49)/(55)

GM (4.10) + constant-w closure -> GM (4.29)
printed GM (4.15)              -> GM (4.19) -> Appendix A
```

The first four routes share the same local component conservation law and
linear perfect-fluid assumptions. The coordinate and abstract versions are
algebraically equivalent realizations. GM and DBE are independent printed
transcriptions/authorship paths, but their equations derive from the same
physics. GM (4.29) is downstream of (4.10). The precise replacement is:

> Four agreeing realizations, with a shared component-conservation premise,
> two independent primary-source transcriptions, and one partially
> independent internal GM consistency check.

## 16. Non-D3 printed-defect claims

**Identification classification: COMPLETE.**

**Proposed-author-communication classification: PARTIAL.** These defects
must not be counted as votes for D3.

| item | printed form | independent/standard form | confidence | D3 relevance | reporting/communication disposition |
|---|---|---|---|---|---|
| BDE (19), p. 38 | `dot mu+3mu H(mu+p)=0` | `dot mu+3H(mu+p)=0` | high; dimensional check and BDE (45)/DBE (28) | none | retain only as a separated source-transcription note; omit from a GM D3 query |
| GM (2.5), p. 6 | `Theta=Theta_i+div V_i` | with GM’s `u_i=n+V_i`, `Theta=Theta_i-div V_i` | high; direct four-velocity divergence in both signatures | none; (2.5) is not used in the D3 chain | separate future erratum question, not supporting evidence |
| GM (2.21), p. 9 | total `F` carries `c_s(i)^2` | total `F` should carry total `c_s^2` | high from surrounding total notation and GM (2.11) | none; unused in Sec. 4 chain | separate minor notation question |
| GM (2.12)/(2.13), p. 7 | Raychaudhuri `-2Lambda` and paired constraint `-2Lambda` | standard Raychaudhuri `-Lambda`; Hamiltonian contribution `+2Lambda` under the stated convention | high from DBE (31), BDE (20), and direct FLRW equations | none for Timescape, where `Lambda=0` | separate future erratum question; do not bundle as a vote for D3 |

Original Sec. 37’s courtesy question bundles D3 with GM (2.5) and the Lambda
items. A future communication should ask the D3 question alone, with unrelated
defects in a separately labeled appendix or separate message.

## 17. Resolution criteria, verdict, and terminology

**Original-checklist classification: PARTIAL.**

**Independently audited equation-level verdict classification: COMPLETE.**

| # | original criterion | audit classification | independent finding |
|---:|---|---|---|
| 1 | every relevant frame explicitly defined | COMPLETE | all six relevant frames reconstructed; `u_E` and `u_N` distinct |
| 2 | complete first-order frame transformation performed | PARTIAL | formulas are correct, but original JSON does not define every source/destination direction; this audit supplies them |
| 3 | component and total variables distinguished | PARTIAL | frames/variables are distinct, but “total term never self-couples” is too absolute after expanding the total sum |
| 4 | pressure and sound-speed definitions mapped | PARTIAL | closure map correct; rest-frame sound speed, `delta p`, and nonadiabatic distinctions incomplete |
| 5 | scalarization explicit | PARTIAL | algebra correct; original primary-source inventory omits BDE (74)/footnote 22 |
| 6 | both tilt normalizations checked | COMPLETE | full matrix transformation succeeds for both branches and is non-discriminating |
| 7 | independent conservation-law derivation agrees | COMPLETE | the coordinate route agrees mathematically, but is corroborating rather than logically independent of the covariant route |
| 8 | all sign-critical source equations visually unambiguous | COMPLETE | fresh 300-dpi inspection confirms decisive signs; noted defects are outside the D3 chain |
| 9 | no uninspected equation required | PARTIAL | the derivation closes, but the original report omitted the direct BDE harmonic eigenvalue source that it should have inspected/cited |
| 10 | no unresolved convention can reverse result | COMPLETE | explicit boosts, first-order closure invariance, scalarization, signature, tilt, `Z`, and Laplacian audits cannot change A33 |

Recommended verdict, exactly one of the permitted verdicts:

**`RESOLVED_DERIVED_4_10`**

This is an equation-level verdict only. Under GM’s explicit postulate of two
separately conserved perfect components, dust-frame CGI perturbations, and
closure (4.13), the unique density self coefficient is
`(w_eff-c_s,eff^2)Theta`. It does not establish the physical adequacy of
representing Buchert backreaction as that local effective component. It does
not determine authorial intent. It does not change which branch reproduces
the historical paper/notebook.

After equation adjudication, “D3 uncertainty band” is misleading. Use:

- **published-record discrepancy** for the disagreement between parent
  equations and printed (4.15);
- **forensic reproduction spread** for numerical differences between the
  historical printed/notebook branch and the derivation-backed branch;
- **publication-systematic** only when deliberately propagated as a
  systematic associated with the inconsistent published record.

It should not be described as unresolved theoretical uncertainty inside the
postulated GM system.

## 18. Operational consequences

**Overall classification: PARTIAL.** Runtime facts are directly verified;
the claim that no ignored numerical artifact changed historically cannot be
proved from Git.

| requirement | classification | direct evidence |
|---|---|---|
| both branches implemented | COMPLETE | `D3Branch.PRINTED_4_15="printed_4_15"` and `D3Branch.DERIVED_4_10="derived_4_10"` in `src/timescape_fsigma8/perturbations/barotropic.py` |
| no runtime default | COMPLETE | `barotropic_matrix(..., branch: D3Branch, ...)`, `barotropic_rhs(..., branch: D3Branch, ...)`, `BarotropicScenario.branch`, and growth `GrowthScenario.d3_branch` are mandatory; validation rejects missing/inapplicable values |
| neither label removed/deprecated | COMPLETE | both enum members and public export remain present; no deprecation path |
| printed branch remains reproducible | COMPLETE | `_a33` returns `(w_eff+c_s2_eff)Theta` for `PRINTED_4_15`; frozen forensic/oracle tests pass |
| no tracked numerical result changed | COMPLETE | HEAD is the Phase 1D-C frozen commit and tracked diff is empty |
| no ignored artifact changed | CLAIMED_BUT_NOT_EVIDENCED | ignored files have no Git baseline; the original completion claim is not evidence |
| Candidate A is D3-independent | COMPLETE | frozen definition uses clean comoving/Meszaros systems; growth scenarios require `d3_branch=not_applicable` for them; those matrices have no D3 entry |
| Phase 1D-D not begun | COMPLETE | no tracked or untracked implementation file exists; only report-only Phase 1D-D-t deliverables are present |
| no API/documentation promotion | COMPLETE | frozen `perturbations/__init__.py`, `growth/__init__.py`, and `growth/scenarios.py` still call both branches unresolved and explicitly deny a canonical/preferred/default branch |

## A. Evidence-backed conclusions

1. **COMPLETE:** the direct covariant derivation from separate component
   conservation yields GM (2.14), and its geodesic dust specialization gives
   the positive `Theta(1+w)P` term in GM (4.6). Evidence: original Secs.
   22–23; JSON `conservation_law_derivation` and
   `frame_transformation_derivation_steps`; GM pp. 7/16; independent Secs.
   5/7 of this audit.
2. **COMPLETE:** GM (4.10)+(4.13) uniquely gives
   `A33=(w_eff-c_s,eff^2)Theta`; printed (4.15) has the opposite sound-speed
   sign. Evidence: original Secs. 24/29; JSON `gm_equations` and
   `candidate_a33_expressions`; GM pp. 16–17; independent Sec. 11/S3.
3. **COMPLETE:** the frame shifts of `D_i` and `P_i` cancel in
   `(1+w_i)P_i-c_si^2D_i` at first order. No boost direction changes A33.
   Evidence: original Secs. 18–20; JSON
   `frame_transformation_derivation_steps` and `pressure_variable_map`; BDE
   (25)–(26), p. 39, DBE (27), p. 58, and GM (4.13), p. 17; independent
   C6c–C6e in Secs. 4/8/14.
4. **COMPLETE:** scalarization and harmonics change only the tilt-Laplacian
   term, not the density self coefficient. Evidence: original Sec. 25; JSON
   `scalarisation_map`/`harmonic_conventions`; BDE (40), (63), and (74),
   journal pp. 41/43/44; independent Sec. 10/S2.
5. **COMPLETE:** DBE (46)+(47)+(29)+(34) reproduce DBE (49), including
   interactions; the no-interaction limit reproduces (55) and the minus
   component coefficient. Evidence: original Secs. 10/13/32; JSON
   `dbe_bde_equations` and `symbolic_checks` S8; DBE journal pp. 58/60;
   independent Sec. 9/S8.
6. **COMPLETE:** GM (4.19) is downstream of printed (4.15); GM (4.29) is
   derived from (4.10), agrees with the derived branch, and is only partially
   independent. Evidence: original Secs. 30–31; JSON
   `consistency_equation_classifications`; GM pp. 17–20 and Appendix A p. 51;
   independent Secs. 13–14/S7.
7. **COMPLETE:** the equation-level verdict is
   `RESOLVED_DERIVED_4_10`, conditional on GM’s effective-fluid postulate.
   Evidence: original Secs. 21/34/35; JSON `resolution_criteria` and
   `final_d3_verdict`; GM pp. 14/17; independent Secs. 5–17.

## B. Primary-source or transcription failures

1. **PARTIAL:** both original deliverables omit BDE (74) and the harmonic
   Laplacian clarification in footnote 22 while claiming complete harmonic
   source coverage.
2. **COMPLETE:** the decisive GM/DBE/BDE signs were otherwise transcribed
   correctly from fresh visual renders.
3. **COMPLETE:** BDE (19), GM (2.5), GM (2.21), and GM (2.12)/(2.13) are
   genuine non-D3 printed defects; they must remain separate from the D3
   evidentiary chain.

## C. Mathematical and frame-mapping failures

1. **PARTIAL:** generic boost equations are right, but the original JSON
   heat-flux record lacks an explicit source/destination convention.
2. **OVERSTATED:** the DBE total pressure-gradient coupling is not literally
   incapable of containing the same component after the total sum is
   expanded; this does not change the dust-frame A33 result.
3. **PARTIAL:** the sound-speed taxonomy omits a clean distinction among
   rest-frame sound speed, adiabatic derivative, pressure perturbation, and
   CGI pressure-gradient variable.
4. **OVERSTATED:** “four independent routes” should be “four agreeing
   realizations with shared conservation-law premises.”
5. **PARTIAL:** the original equation-discrepancy wording should distinguish
   the `+2c_s^2Theta` RHS coefficient difference from the
   `-2c_s^2Theta Delta` printed-LHS residual.

## D. Reproducibility failures

1. **CLAIMED_BUT_NOT_EVIDENCED:** the original C4 coordinate ledger does not
   display its Christoffels, projections, or full residual, and its scratch
   script is not a deliverable.
2. **PARTIAL:** S1–S5 can be reconstructed from displayed algebra; S6/S7 are
   not fully reproducible from the Markdown because the complete encoded
   second-order equations and residuals are not printed.
3. **OVERSTATED:** JSON claims “all checks passing” as source evidence; a
   ledger assertion is not proof. This audit independently reproduced the
   decisive subset and reported its inputs/results.
4. **CLAIMED_BUT_NOT_EVIDENCED:** absence of author contact and all possible
   external publication events cannot be established from the repository.

## E. Overstatements and terminology corrections

1. Replace “D3 uncertainty band” with “forensic reproduction spread” or
   “published-record discrepancy” after equation-level adjudication.
2. Qualify every closure-invariance statement with “at first order.”
3. Replace “the only tracked files created” with “the only repository files
   created”; both originals are currently untracked.
4. Give one primary evidence classification per material Markdown
   conclusion and list other evidence as support, rather than using compound
   classification labels.
5. Do not describe the flat one-dimensional coordinate calculation as a
   complete independent proof of all perturbation sectors.

## F. Markdown/JSON inconsistencies

1. Verdict token: **COMPLETE**, identical.
2. Assumptions and source scope: **PARTIAL**, semantically compatible but not
   identical wording; JSON folds scratch/frozen evidence into one field.
3. Derivation summary: **PARTIAL**, semantically aligned but both formats
   obscure the routes' shared conservation-law premise.
4. Convention dependencies: **OVERSTATED** in JSON because the first-order
   qualifier is absent from the final conclusion object.
5. Implementation consequence: **COMPLETE**, dual branches/no default and
   historical reproduction match in both formats.
6. Evidence needed to change status: **PARTIAL**, present as a named JSON
   field and only implicit in Markdown Sec. 35.
7. Downstream consequences: **COMPLETE** as a cross-format match, but both
   use the unsuitable “uncertainty band” term.
8. Unmet criteria: **COMPLETE** as a cross-format match; this audit downgrades
   criteria 2–5 and 9 as documented.
9. Forbidden actions: **PARTIAL**; JSON lacks explicit staged/tagged/merged
   status fields present in Markdown prose.
10. Classification policy: **PARTIAL**; JSON conclusion fields are single
   values, while numerous Markdown conclusions use compound labels.

## G. Recommended D3 verdict

**`RESOLVED_DERIVED_4_10`**

The recommendation adjudicates the equation within GM’s stated perturbative
framework. Physical adequacy of the effective-fluid postulate remains open;
authorial intent remains unresolved; historical reproduction continues to
require `printed_4_15`; neither fact reverses the equation derivation.

## H. Exact minimal corrections before commit

1. Add BDE (74), footnote 21, and the relevant footnote-22 Laplacian
   clarification to both source inventories and cite them in scalarization.
2. Add one explicit source/destination boost table with
   `xi=u_destination-u_source`; make the JSON heat-flux sign directional.
3. Expand the sound-speed/pressure taxonomy to include rest-frame sound
   speed, `delta p`, entropy/nonadiabatic perturbation, CGI gradient, and
   rescaled pressure.
4. Qualify the DBE total-term statement: cross-coupling in the retained-total
   representation, with possible same-component content after expansion.
5. Replace independence claims with the dependency-aware formulation in
   Sec. 15.
6. Print enough C4 and S6/S7 inputs/residuals for reproduction without the
   original scratch scripts, or downgrade those claims.
7. Distinguish coefficient difference from left-hand-side residual exactly
   as in Sec. 11.
8. Replace “D3 uncertainty band” terminology and fix the “tracked files
   created” wording.
9. Make each material Markdown classification a single primary token and
   align the final seven fields explicitly with JSON, including the
   first-order qualifier and forbidden-action fields.
10. Separate unrelated printed defects from any future D3 author question.

## I. Commit authorization recommendation

**DO NOT AUTHORIZE the two original Phase 1D-D-t deliverables for commit in
their present form.** The central equation-level verdict is supported, and no
scientific code change is required, but the minimal report/JSON corrections
in Sec. H are necessary for source completeness, reproducibility, and
epistemic consistency. This audit does not authorize or perform any commit,
tag, push, merge, publication, runtime change, or author contact.
