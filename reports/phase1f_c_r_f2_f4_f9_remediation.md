# Review findings F2, F4–F9: remediation, successor errata and provenance record

## 1. Purpose, authorisation and checkpoint

This change addresses findings F2 and F4–F9 of
`phase1f_c_r_post_remediation_independent_audit.md`. It follows the F1 fix
(`phase1f_c_r_f1_growing_mode_initial_conditions_validation.md`) and the F3
fix (`phase1f_c_r_f3_h1_kinematic_gates_validation.md`).

- **Authorisation.** The human request was "fix F2, F4, F5, F6, F7, F8 and
  F9".
  - No scientific equation, IC, unit, sign convention, status token or
    tolerance of any runtime changes.
  - F7 removes a default value; every caller already passed `G`.
  - F6 changes the verification mechanics of three historical scripts, not
    the claims they verify.
- **Historical reports.** Every historical report and inventory stays
  byte-identical, as the 1F-C-R validator requires. §2 and §8 are successor
  errata: they state the current reading of frozen text without editing it.
- **Parent checkpoint:** `c62bc741389233ba7bcca16346f3b2d1dbdd8a64`.
- **Machine-readable companion:**
  `phase1f_c_r_f2_f4_f9_remediation_inventory.json`.

| Finding | Severity (review) | Status after this change |
|---|---|---|
| F2 bare/dressed factor range | MEDIUM | `RESOLVED_BY_SUCCESSOR_ERRATUM` (§2) |
| F4 missing authorization, specifications and audits | MEDIUM | `CLOSED_AS_DOCUMENTED_PERMANENT_GAP` (§3; human decision 2026-09-23) |
| F5 scope-firewall wording | LOW-MEDIUM | `RESOLVED` (§4) |
| F6 checkout- and history-bound reproducibility | LOW-MEDIUM | `RESOLVED` (§5) |
| F7 `G = 1.0` defaults | LOW | `RESOLVED` (§6) |
| F8 stale governing documentation | LOW | `RESOLVED` (§7) |
| F9 1C-A wavenumber notational slip | LOW | `RESOLVED_BY_SUCCESSOR_ERRATUM` (§8) |

## 2. F2 — successor erratum: the bare→dressed growth-rate factor

The exact tracker conversion (1D-A §7, chain D3; `growth.rates.dressed_chain_factor`)
is

```text
g(f_v) = f_dressed/f_bare = (2 + f_v)² / (4 + f_v + 4 f_v²)
g'(f_v) = (2 + f_v)(6 − 15 f_v) / (4 + f_v + 4 f_v²)²
```

`g` is not monotonic. It rises to its global maximum
`g(2/5) = 8/7 = 1.142857`, which is reached at dressed `z = 2.00656`. That
corresponds to `t = 3.658 Gyr` (notebook preset) or `3.668 Gyr` (paper
preset), and the redshift is identical for both presets. After the maximum,
`g` falls to `1.084156` today.

Values recomputed by the package, identical for both presets:

| dressed z | 20 | 10 | 3 | 2 | 1 | 0.5 | 0.3 | 0 |
|---|---|---|---|---|---|---|---|---|
| `f_dressed/f_bare` | 1.0248 | 1.0579 | 1.1361 | 1.1429 | 1.1307 | 1.1124 | 1.1024 | 1.0842 |

Throughout `0.3 ≤ z ≤ 3` the factor lies in `[1.1024, 8/7]`. That is above
the previously quoted upper bound everywhere in the window, by up to 5.9
percentage points.

**Superseded statements.** These stay frozen in their files. The current
reading for each is given in the second column.

| Location | Frozen text | Current reading |
|---|---|---|
| `phase1d_a_growth_observable_audit.md` l. 688 | "rescales fσ8 by 1.02–1.08" | rescales by `g(f_v(t))`, between 1.0248 (z = 20) and 8/7 (z ≈ 2.007); 1.0842 today |
| same, l. 832 | "= 1.025–1.084" | the same correction |
| `phase1d_a_observable_inventory.json` l. 237 | "rescales f sigma_8 by 1.025-1.084" | the same correction |
| `phase1d_c_observable_closure_audit.md` l. 906 | "amplitude ×1.025–1.084156" | amplitude `× g(f_v(t))` ∈ [1.0248, 8/7] |
| `phase1d_c_closure_inventory.json` l. 263 | "amplitude x1.025-1.084156" | the same correction |
| `phase1d_c_compliance_audit.md` ll. 435, 525 | "factor 1.02475–1.084156" | the endpoint values are correct; they are not the range |
| `phase1d_c_observable_closure_audit.md` l. 471 | "1.02475 at dressed z=20 → 1.084156 at t0" | the endpoints are correct; the factor passes through 8/7 between them |

These remain correct:
- `phase1d_a_growth_observable_audit.md` l. 435 ("for these audited epochs",
  2.5–8.4 %);
- every single-epoch value, such as 1.084156 at `t0` in 1D-B/1D-D;
- the 1E-A value 1.13066 at z = 1.

**Consequence.** Any bare-versus-dressed spread of an fσ8-like number is up to
about 14.3 % in the observable window (at z ≈ 2), not ≤ 8.4 %. The scope
firewall is unchanged: no observational fσ8 is implemented.

The erratum is pinned by `tests/test_review_errata.py`. Those tests check:
- the derivative and its root at `f_v = 2/5`;
- `g = 8/7` on the tracker at `f_v = 0.4`;
- the peak redshift;
- the table above;
- that the factor exceeds 1.084156 throughout `0.3 ≤ z ≤ 3`.

## 3. F4 — provenance record (closed as a documented permanent gap)

F4 asked for three things: commit the specifications, commit the three
audits, and add an H1 decision record. None of the five documents exists in
this checkout, in any branch or tag of `origin`, or in any file reachable
from this session. They cannot be reconstructed without inventing content,
which would violate AGENTS.md rules 1–2. This section records exactly what
the repository does and does not establish, and what only a human can
supply.

### 3.1 Documents cited but never committed

| Document | Cited by | Pinned hash |
|---|---|---|
| Phase 1E-F specification ("user-approved") | `transfer/matrix_backend.py`, `transfer/h1_realization.py` | none recorded |
| Phase 1E-G specification ("human-approved", with v2/v3 amendments) | `transfer/continuum_*.py` | none recorded |
| Phase 1F-A specification (2026-08-24) | `phase1f_a/models.py`, `density.py`, `spectral.py`, `boost.py`, `dressed.py` | none recorded |
| `astra/INDEPENDENT_SCIENTIFIC_AUDIT.md` (the audit 1F-C-R remediates) | 1F-C-R inventory, validator | `4b8f8b39…4518` |
| `reports/phase1f_b_dust_wall_boost_dynamics_v3_final_audit.md` | 1F-C-R inventory, validator | `08c30893…6930` |
| `reports/phase1f_c_wall_common_geometry_adversarial_audit.md` | 1F-C-R inventory, validator | `345417fd…df3c` |

The Phase 1F-A specification is an additional gap. The review named only the
1E-F and 1E-G specifications.

**Tags (published after this report was first written).** The inventory
also pins three tags, `phase-1f-b-dust-wall-boost-dynamics-v1/v2/v3`, that were
not on `origin` when this report was written. The project owner has since
published the original signed tags (§11). Their tag objects and commits match
the pins, and the validator verifies them.

### 3.2 Specification citation map

Every equation the runtime attributes to an uncommitted specification was
checked against the committed reports. Each is displayed, or described in
words, in a committed report of the same phase. An auditor can therefore
verify each implemented equation against a committed document, but not
against its original authority.

| Specification section cited | Implemented in | Shown in committed report |
|---|---|---|
| 1E-F `regional-dynamics` (common-time chain rule) | `h1_realization.regional_evolution` | `phase1e_f_h1_transfer_realization.md` §2 (displayed) |
| 1E-F `h1-functional-contract`, `implementation-architecture`, `provenance-preserving-realization` | `matrix_backend` | same, §3 and §9 (displayed and described) |
| 1E-F `two-region-background-quantities` | `two_region_coefficients` | same, §4 (displayed) |
| 1E-F `h1-curvature-transfer`, `constitutive-closure`, `mass-weighted-dust-transfer` | `evaluate_h1_realization` | same, §5 (displayed) |
| 1E-F `partition-common-time-closure` (`J_Xi`) | `evaluate_h1_realization` | same, §6 (displayed) |
| 1E-G §5 (carrier) | `continuum_backend`, `continuum_geometry` | `phase1e_g_continuum_h1_realization.md` "Carrier and morphology ontology" (described) |
| 1E-G §§7–8, 27 (metric, pullback, `J_r`, `K_r`, source functional, Poincaré oracle) | `continuum_geometry`, `continuum_backend` | same, "Metric and pullback contract" and "Weak form and source measure" (displayed) |
| 1E-G §§9–10, 13 (kernel, projection, coercivity) | `continuum_backend` | same, "Kernel, projection and coercivity" (described) |
| 1E-G §§12, 14, 15 (`L_D`, `T_r = −L_D G_Γ Q_Γ J_r`, equal-geometry identity) | `ContinuumTransfer`, bridge | same, "Green transfer and equal-geometry identity" (displayed) |
| 1E-G §§17–20 and v2 target guard (`C_R`, `E_ΔΘ`, `Ξ_r = α_rΘ_r`, `E_ΔΞ,0`, `J_f = 0`, fixed branch) | `continuum_bridge`, `FixedReferenceBranchSpec` | same, "Effective-sector bridge" (displayed) |
| 1E-G §22 and v3 (`V_r = V_r,i a_r³`, geometric `f_v`) | `ContinuumH1Operator.physical_regional_volumes` | same, "Physical-volume dimensional contract…" (displayed) |
| 1E-G §§21, 23–24 | cited only inside the range "sections 17–24" | not separately identifiable without the specification |
| 1F-A §§7–8 (regional density inversion, zero-mode closure, carrier assembly) | `phase1f_a/density.py`, `operators.py` | `phase1f_a_h1_carrier_dressed_closure_validation.md` §§6–10 (displayed) |
| 1F-A §§11.1–11.2 (generalised spectra, kernel `U_mn`) | `phase1f_a/spectral.py` | same, §§14–15 (displayed) |
| 1F-A §13 (external boost closure, `Δ_γ ψ = ϑ`, `v^a = γ^{ab}∂_bψ`) | `phase1f_a/boost.py` | same, §§16–17 (displayed) |
| 1F-A §14 (dressed-map closure) | `phase1f_a/dressed.py` | same, §19 (described) |

### 3.3 H1 decision: what the repository records

| Date | Commit | Record |
|---|---|---|
| 2026-08-12 | `1f2800c` | 1E-E: S1 `PRIMARY_SELECTED_CONDITIONALLY`; H1 `MANDATORY_SECONDARY_COMPARATOR`; implementation and prototype authorization `NOT_GRANTED`; `PARTIAL_REALIZATION_DEFICITS_REMAIN` / `NEW_DYNAMICS_REQUIRED`. Produced outside the Git checkout (its line 19). |
| — | — | 1E-E correction verification repeats `NOT_GRANTED`. |
| 2026-08-18 | `0ad10f4` | 1E-F implements H1 with "Scientific implementation authorization: GRANTED". Its inventory records `scientific_implementation: GRANTED` and `prototype: GRANTED_FOR_CONDITIONAL_H1_RESEARCH_RUNTIME_ONLY`. |

No committed document records any of the following:
- who changed the selection from S1 to H1, and when;
- the grant;
- the rationale;
- how the 1E-E deficits were judged closed.

This record does not assert that the grant occurred or what it said; only a
human can confirm that. Status: `DECISION_RECORD_INCOMPLETE_AWAITING_HUMAN_CONFIRMATION`.

### 3.4 Human decision (2026-09-23)

The project owner was asked whether the missing documents could be supplied
or committed. The answer was that they are **not available**, and that the
gap should be recorded as permanent. Accordingly:

- **F4 status: `CLOSED_AS_DOCUMENTED_PERMANENT_GAP`.** No specification,
  audit or decision text will be added.
  - The three specifications, the three audits (pinned hashes above) and any
    record of the H1 decision are permanently unavailable to this repository.
  - The three `phase-1f-b` tags are not part of the gap: the project owner
    published the originals after this decision (§11).
- **H1 decision record: `UNAVAILABLE_CONFIRMED_BY_HUMAN`.** The H1 runtime's
  "Scientific implementation authorization: GRANTED" rests only on the 1E-F
  report's own assertion. It cannot be traced to a committed decision.
- **The specifications' authority is unverifiable.** The citation map (§3.2)
  is the durable substitute. Every specification-cited equation can be checked
  against a committed report, but not against the specification that
  authorised it. Code citations of those specifications are kept as
  historical attributions.
- **The validator status is permanent.**
  `validate_phase1f_c_r_astra_remediation.py` will keep reporting
  `PASS_WITH_ABSENT_LOCAL_PROVENANCE` because of the three absent audit
  files. Any of those files that reappears is still verified against its
  pin.

## 4. F5 — scope firewall

`CLAUDE.md` said that no "fσ8-shaped" diagnostic was implemented, while
listing Candidate A as implemented. It now states that no fσ8-shaped diagnostic
exists beyond the conditional, externally anchored, non-observational
Candidate A (`Q_anchor = f·A_anchor`, 1D-D), which 1D-A conditionally
authorised. It also forbids adding another. The 1E-A verdict
`NOT_JUSTIFIED_FOR_OBSERVATIONAL_USE` is retained. Candidate A's code and
labels are unchanged.

## 5. F6 — checkout- and history-independent reproducibility

1. **The notebook identity no longer depends on line endings.**
   - `UPSTREAM.lock` gains three additive pins:
     `notebook_sha256_lf = 628c4412…5cea2a` (SHA-256 after CRLF → LF,
     identical to the committed blob), `notebook_sha256_crlf = 86d2534d…afe55a`
     (the Windows `core.autocrlf` working tree), and
     `notebook_git_blob = c6bef320…19ee`. All three were verified from the
     pinned commit `590c6fd`.
   - `extract_upstream_barotropic_oracle.py` and
     `validate_anchored_density_growth.py` verify the LF-normalised hash and
     still record the raw hash.
   - The barotropic-oracle test accepts either raw encoding and requires the
     LF identity.
   - Re-extracting the oracle gave data identical to the previous oracle, plus
     the two new normalised-hash provenance fields.
2. **The 1D-D validator no longer requires its work branch.**
   - On the historical branch it behaves as before.
   - Elsewhere it requires the 1D-D-t base and the 1D-D commit `7ea266c`
     (tag `phase-1d-d-anchored-density-growth-v1`) to be ancestors of `HEAD`.
   - It checks the phase scope on the immutable range `base..7ea266c` and
     requires a clean tree.
   - It records later scientific-module changes as drift.
   - It accepts any primary interpreter plus `.venv311`, on Windows or POSIX
     paths, and records the versions.
   - Result of regenerating it on this checkout: §9.
3. **The 1F-C-R validator no longer requires `main` to equal its base.**
   - The `main == origin/main == 63d2104` gate is replaced by ancestry of the
     base and of the certified commit `118b8f3`
     (`phase-1f-c-r-astra-audit-remediation-v2`).
   - Equation preservation is certified on base → `118b8f3`, which is the
     claim 1F-C-R made. Later, separately approved edits are reported as
     `post_remediation_drift`: F1 changed `initial_conditions.py`; F7 changed
     `tracker.py` and `effective_fluid.py`.
   - A local provenance file that is present must match its pin (raw or
     line-ending equivalent). An absent file is reported as
     `ABSENT_FROM_CHECKOUT`.
   - A tag absent from the clone has its recorded commit verified and its
     tag object reported as absent.
   - Overall status: `PASS` only when nothing is absent, otherwise
     `PASS_WITH_ABSENT_LOCAL_PROVENANCE`.

   On this checkout the result is `PASS_WITH_ABSENT_LOCAL_PROVENANCE`:
   - 20 preserved equations certified;
   - 27 of 27 tags verified. When this section was first written, only 24
     were verified, because the 3 `phase-1f-b` tags were unpublished (§11);
   - the 3 audits of §3.1 absent;
   - 52 historical reports byte-identical;
   - no explicit-tolerance omissions.

`tests/test_reproducibility_gates.py` covers:
- agreement of the pins across the lock file and the scripts;
- checkout independence of the LF hash;
- the notebook identity;
- the local-file status logic, including mismatch rejection;
- ancestry of every recorded commit.

## 6. F7 — mandatory `G`

`rho_d`, `drho_d_dt`, `rho_eff`, `p_eff`, `drho_eff_dt` and `dp_eff_dt` no
longer default to `G = 1.0`; `G` is a required argument. Every package,
script and test caller already passed it. The domain-validation test now
passes `G` explicitly and asserts that it has no default. The package
docstring states the rule.

`background_validation.md` l. 74 ("G passed explicitly (default 1.0 = code
units)") is superseded: there is no default.

## 7. F8 — governing documentation

- **`CLAUDE.md`:**
  - the architecture table adds `phase1f_b/`, `phase1f_c/`, `components.py`
    and `scientific_status.py`, the F1 IC convention and the F3 gate policy;
  - the scope firewall is fixed (F5);
  - F1 and F2 caveats are added;
  - the test count is updated (§9);
  - the 1F-B, 1F-C-R, F1 and F3 drivers are listed, with the F6 semantics;
  - the push rule now reads "never … without explicit human approval for that
    specific action (AGENTS.md rule 7)";
  - the environment section now covers Linux/macOS as well as Windows;
  - the phase ledger is completed through the review fixes.
- **`README.md`:** a status section for the review and its fixes; the layout
  table covers every package, driver and report family; setup instructions
  for Windows and Linux/macOS.
- **`pyproject.toml`:** the description and header cover the whole project
  scope, with the runtimes labelled conditional and non-observational.

## 8. F9 — successor erratum: 1C-A wavenumber factor

`phase1c_perturbation_equation_audit.md` ll. 300–301 write the factor as
"a_D,0 × h_TS/h_ΛCDM = 1.3685 × 0.9204", but `0.9204 = h_ΛCDM/h_TS`. The
correct factor, as implemented in
`barotropic.resolve_wavenumber(..., PAPER_LCDM_HUBBLE_K)`, is

```text
k_matrix / k_paper = a_D,0 · h_ΛCDM / h_TS = 1.3685 × 0.674/0.7323 = 1.25955 .
```

The slip is textual only. The table value `1.2596` in the same report and all
code are correct. `tests/test_review_errata.py` pins the implemented factor
and the identity of 0.9204.

## 9. Tests and validation

**New or changed tests:**

| File | Tests | Covers |
|---|---|---|
| `test_review_errata.py` | 4 | F2 and F9 |
| `test_reproducibility_gates.py` | 5 | F6 |
| `test_vs_upstream_barotropic_oracle.py` | +1 | lock/pin agreement |
| `test_domain_validation.py` | +6 net | explicit-`G` density cases and no-default assertions |
| `test_anchored_density_growth.py` | — | environment keys generalised |

**Suite results:**

| Run | Result |
|---|---|
| Before this change | 707 passed, 1 skipped |
| After, Python 3.13.12 | 723 passed, 1 skipped |
| After, Python 3.11.15 | 723 passed, 1 skipped |

**Validators:**
- `validate_phase1f_c_r_astra_remediation.py`: §5, item 3.
- `validate_anchored_density_growth.py`, regenerated on the clean committed
  tree `ae00246` by ancestry: exit 0.
  - `execution_context = post_phase_regeneration_by_ancestry`, off the
    historical branch.
  - All declared gates passed, and the 25-section artifact schema held.
  - Its embedded full suites passed: 724 passed on Python 3.13.12 and 724
    passed on Python 3.11.15. Its own artifact test ran rather than skipped,
    because the provisional artifact exists during the run.
  - The regenerated values agree with the frozen 1D-D report:

    | Quantity | Regenerated | Frozen report | Relative difference |
    |---|---|---|---|
    | `Q_bare` | `2.1502835091436094` | `2.150283509143608` | 6.2e−16 |
    | `Q_dressed` | `2.331243485933034` | `2.3312434859330327` | 5.7e−16 |
    | chain factor | `1.084156333813626` | `1.084156333813626` | identical |

    The residual differences come from the numpy/scipy versions.
  - Post-phase changes recorded since `7ea266c`: the F1 and F7 edits, plus
    the 1F-C-R edit to `perturbations/barotropic.py` (`72d8c51`).

## 10. What remains open

- **F4 (§3.4):** closed as a documented permanent gap by human decision.
  The specifications, audits and H1 decision record are unavailable. The
  citation map is the durable substitute.
- **Earlier fixes:** the open items of F1 (barotropic ICs, amplitude recipe)
  and F3 (heterogeneous geometry, unequal clocks, `K_D ≠ 0` observation,
  time evolution) are recorded in their own reports.

## 11. Post-merge update (2026-09-23)

After PR #1 was merged (merge commit `ce55075`), the project owner published
these tags from the original clone:

| Tag | Tag object | Commit |
|---|---|---|
| `phase-1f-b-dust-wall-boost-dynamics-v1` | `d7840740…23bb7a` | `27fd65fd…3b566e` |
| `phase-1f-b-dust-wall-boost-dynamics-v2` | `bd1facf1…eef3a0` | `16440e1a…90fa66a` |
| `phase-1f-b-dust-wall-boost-dynamics-v3` | `61dc9cf7…7059ab7` | `d2f15022…250309d8aaa67` |
| `phase-1f-c-r-post-remediation-review-v1` (this checkpoint) | `d4084287…6030998` | `ce550753…23b8bf8780` |

All four tags are signed by the owner.

The three `phase-1f-b` tag objects and their commits match the 1F-C-R
inventory pins exactly; they are the originals, not recreations. Rerunning
`validate_phase1f_c_r_astra_remediation.py` gives:
- 27 of 27 frozen tags verified;
- no absent tag objects;
- 20 preserved equations certified;
- 52 historical reports byte-identical.

The status stays `PASS_WITH_ABSENT_LOCAL_PROVENANCE`, only because of the
three unavailable audits of §3.1. F4 therefore remains
`CLOSED_AS_DOCUMENTED_PERMANENT_GAP`, now limited to the specifications, the
audits and the H1 decision record. The merged branch
`claude/loving-dijkstra-esoj6f` was deleted after the merge.
