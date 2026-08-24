# Phase 1F-A — Independent adversarial read-only audit

Audit classification: `INDEPENDENT_ADVERSARIAL_READ_ONLY_AUDIT`.

Audit date (UTC): 2026-08-24. Auditor session: separate from the
implementation session; the implementation report, inventory, internal audit,
and completion response were treated as **claims under test**, never as
scientific authority.

Audit target: commit `a56fa88b64062761fefc193d7061d1d12ba2dedd`, tag
`phase-1f-a-h1-broken-density-spectral-boost-v1`, realization
`H1-1F-A-BROKEN-DENSITY-SPECTRAL-LONGITUDINAL-BOOST-V1`.

Nothing in the repository was modified. No source, test, report, inventory,
artifact, tag, commit, or upstream file was edited, staged, committed,
tagged, or pushed. The only file created is this report, and it is
deliberately left untracked. All independent computations were executed from
an ignored scratch directory against the installed package; the committed
validation artifact was regenerated only to a scratch path and compared, never
overwritten.

---

## 0. Provenance preflight

Every item verified directly from Git objects and the filesystem.

| Check | Expected | Observed | Status |
|---|---|---|---|
| Branch | `phase-1f-a-h1-broken-density-spectral-boost` | identical | PASS |
| HEAD | `a56fa88b64062761fefc193d7061d1d12ba2dedd` | identical | PASS |
| Parent (single) | `d262099ce3fe977af628ff233abed411e70a3c85` | identical, one parent | PASS |
| Annotated tag object | `c9cd0c5519052d08cf607e725b45dbf8a0cd8a9b` | identical, object type `tag` | PASS |
| Tag peeled commit | `a56fa88b6406…` | identical | PASS |
| Index vs HEAD | clean | clean (`git diff --cached` empty) | PASS |
| Worktree vs HEAD | clean | **one modified tracked file: `CLAUDE.md`** | see deviation below |
| Active Git operation | none | no `MERGE_HEAD`, `rebase-*`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `BISECT_LOG` | PASS |
| `origin/main` | `d262099ce3fe…` | `d262099ce3fe…` locally and via `git ls-remote` | PASS |
| Remote Phase 1F-A branch | absent | absent (13 remote heads, none 1F-A) | PASS |
| Remote Phase 1F-A tag | absent | absent (remote tags stop at `phase-1e-g-…-v4`) | PASS |
| Pinned upstream clone | `590c6fd5332acb15f5683ebf392a0d7ce54983c5`, clean | identical, `git status --porcelain` empty | PASS |
| Notebook SHA-256 | `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a` | identical | PASS |
| Prior frozen tags | unchanged, ancestors of HEAD | all 20 prior tags peel to their recorded commits, all `ANCESTOR`, all identical to the remote tag objects | PASS |
| Commits above `main` | exactly 1 | exactly 1 | PASS |
| Merge commits introduced | 0 | 0 (`git rev-list --min-parents=2 --count main..HEAD` = 0) | PASS |
| Diff shape | additive only | 20 files, **4572 insertions, 0 deletions**; no pre-existing file touched | PASS |
| Python 3.14.3 full suite | 539 passed | 539 passed | PASS |
| Python 3.11.9 full suite | 539 passed | 539 passed | PASS |
| Failures / skips / xfails / warnings | zero | zero in both runs | PASS |
| Targeted Phase 1F-A tests | 35 | 35 passed | PASS |
| Artifact regeneration | byte-for-byte | SHA-256 `ed3fcdc4aa54…be47` identical to the committed artifact on **both** interpreters | PASS |

**Preflight deviation (disclosed, not a Phase 1F-A defect).** The worktree is
not pristine: `CLAUDE.md` carries an uncommitted documentation rewrite made in
this same session before the audit began, and two ignored virtual
environments (`.venv`, `.venv311`) were created to run the suites. `CLAUDE.md`
is not part of the audited Phase 1F-A tree; every audited path
(`src/timescape_fsigma8/**`, `tests/**`, `scripts/**`, `reports/phase1f_a_*`)
is identical to HEAD, and the index is clean. The audit was performed against
HEAD content. Classification: `PASS_WITH_EXPLICIT_CONDITIONS`.

**Environment note.** The two interpreters carry *different* numerical stacks
(3.14.3 with numpy 2.5.2 / scipy 1.18.1; 3.11.9 with numpy 2.4.6 /
scipy 1.17.1). The byte-identical artifact across both is therefore a
stronger reproducibility result than a same-stack rerun.

---

## 1. Regional density equation, signs, dimensions, metric convention

**Claim under test:** `Delta_r = a_r^2 D_r^2 delta_m,r` and, under the frozen
comoving-reference convention, `a_r^2 D_r^2 = Delta_gamma_r`.

Verified from the frozen Phase 1E-G geometry definitions rather than from the
1F-A prose. `RegionalGeometrySpec` fixes `metric_inverse = (Phi_r^* gamma_r)^-1`
and `metric_volume_ratio J_r = dmu_(Phi_r^* gamma_r)/dmu_0`, with weak-form
tensor density `K_r = J_r gamma_hat_r^{ij}`
(`continuum_geometry.py:145-224`). The 1F-A assembly builds the flux-form
stiffness with those coefficients and mass `M_r = w_i J_i`
(`operators.py:99-136`), and `apply_regional_laplace_beltrami` returns
`-(K u)/M` (`operators.py:167-178`). That is the standard
mass-lumped discrete Laplace–Beltrami of the comoving metric `gamma_r`.

For `g_ij = a^2 gamma_ij` with spatially constant `a`,
`Delta_g = a^-2 Delta_gamma`, hence `a^2 D^2 = Delta_gamma` exactly. The
scale factor is therefore *absent* from the operator by construction, which
is the correct behaviour, not an omission.

Independent numerical confirmation on the frozen fixture: applying the
package operator to the pure mode `sin(2 pi z)` returns eigenvalue exactly
`-32.0`, matching the analytic 7-point value `-4 sin^2(pi h)/h^2` at
`h = 1/4` (`-32.00000000000001`). The operator is negative-semidefinite, so
the code realizes `L_r = +Delta_gamma_r` and `Delta_r = Delta_gamma_r
delta_m,r` — the same sign convention as the frozen Phase 1D-A mapping
`Delta_d,k = -k^2 delta_m,k`. No sign inversion, no missing `a^2`, no
`-Delta` convention leak.

Dimensions: `lambda_r` carries inverse-comoving-length-squared, and
`physical_wavenumbers = sqrt(lambda_r)/a_r` (`spectral.py:192`) therefore
carries inverse physical length. Consistent.

**Finding 1: `PASS`.**

---

## 2. Zero-mode theorem and the character of the closure

**2a. The theorem.** `Delta_gamma_r (delta_m,r + C_r) = Delta_gamma_r
delta_m,r` because the broken regional stiffness has exactly-zero row sums
(each edge contributes `+c` to the two diagonal entries and `-c` to the two
off-diagonal entries), so the constant vector is in the exact kernel.
I confirmed this is not merely small but **exactly zero in floating point**:
`max|L_r(1)| = 0.0` and `max|L_r(10^6 · 1)| = 0.0`. Consequently
`max|L_r(delta + C) - L_r(delta)|` is pure cancellation noise:
`1.95e-14` at `C = 3`, `9.06e-14` at `C = 7.25`, `1.02e-11` at
`C = -1234.5` — i.e. relative machine precision scaling with `|C|`. The
shifted field satisfies the *same* CGI source to `5.6e-14`. The theorem
holds; the regional constant is not identifiable from the source.

**2b. The evidence in the frozen deliverables is vacuous.** The committed
validator records
`density_inversion.zero_mode_shift_demonstration = 3.0`, computed as
`max|(scalar + 3) - scalar|` (`validate_phase1f_a_h1_closure.py:299`). That
quantity is `3` by arithmetic and demonstrates nothing about the operator.
`tests/test_phase1f_a_density.py:53` asserts the same vacuity
(`max|base - shifted| == 7.25`). Report §8 states "The manufactured solution
and the solution shifted by 3 have the same CGI source" — a true statement
that **no recorded computation supports**. The demonstration in 2a above is
supplied here for the first time.

**2c. The closure is mandatory but its admissible set has exactly one
member.** `RegionalZeroModeClosure.__post_init__` rejects any
`mean_condition` other than `REGIONAL_METRIC_MEAN_ZERO`
(`models.py:198-199`); I confirmed rejection of
`REGIONAL_METRIC_FIXED_POINT_VALUE`, `EXTERNAL_NONZERO_MEAN`, and even the
lower-case spelling. Omission fails closed (`None` raises), the measure
identity is checked against the region, and provenance/frame/domain are
required — so it is genuinely *not* an internal automatic projection in the
sense of being silently applied without declaration. But the caller cannot
select any other homogeneous-mode value: the runtime always imposes
`<delta_m,r>_r = 0` through the KKT constraint
(`operators.py:213-221`).

Under the audit's own instruction, this must be classified as a scientific
problem of *labelling*, not of numerics: mean-zero is not a neutral gauge. It
asserts that the declared regional background density is exactly the regional
mean, which is precisely what makes `rho_bar_C = f_w rho_bar_w + f_v
rho_bar_v` and the global-mean gate consistent. Calling it
`EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE` overstates its externality: the
declaration is external, the value is fixed by the runtime.

**2d. The declared `scale_factor` is analytically inert in the solve.**
`mass = mass_weights * a^3` and `rhs = -(mass * values)/a^3`
(`operators.py:207-213`), so `a^3` cancels from both the constraint row and
the load; the solution is independent of it. Measured: `a = 1.0` versus
`a = 2.5` differ by `1.94e-16` (round-off only). This is *correct* given
`a^2 D^2 = Delta_gamma` (§1), and the scale factor is used meaningfully
elsewhere (physical volumes, the region-dependent `a_r^3` weighting of the
carrier global mean). It is recorded here so that no future reader mistakes
the closure's scale factor for something that influences the inversion.

**Finding 2: `PARTIAL`** — theorem correct and independently demonstrated
here; closure mandatory and provenance-bearing; but the recorded
"demonstration" is vacuous (`SOURCE_MISREPRESENTED` for report §8 and the
artifact key `zero_mode_shift_demonstration`), and the single-member
admissible set makes `EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE` an overstated
label.

---

## 3. Physical carrier-density construction and the `b_r - 1` term

The executable order in `assemble_carrier_density` (`density.py:290-303`) is
exactly:

```
rho_r   = rho_bar_r (1 + delta_m,r)      # lines 292-297, masked per region
rho_C   = chi_w rho_w + chi_v rho_v      # line 302 (disjoint supports)
rho_bar = f_w rho_bar_w + f_v rho_bar_v  # line 281, f_r from physical volumes
delta_C = rho_C / rho_bar - 1            # line 303
```

with `f_r` from `physical_regional_volumes(a_w, a_v)`, cross-checked against
the caller-supplied volumes to `volume_consistency_tolerance` before use. The
H1 transmission potential is never consulted: `density.py` imports nothing
from `timescape_fsigma8.transfer` (verified by import listing, not by the
substring test the suite uses).

Algebraically `delta_C|_r = rho_bar_r/rho_bar (1 + delta_r) - 1 =
(b_r - 1) + b_r delta_r`. Independently recomputed from scratch: my
reconstruction of `rho_C` and `delta_C` matches the package **bit-for-bit**
(`0.0` difference), and the offset formula holds to `2.22e-16` (wall) and
`5.55e-17` (void) with `b_w = 4/3`, `b_v = 2/3`, `rho_bar = 1.5`. The
identity also holds to `4.44e-16` under a stress configuration I built with
*unequal regional geometries* (conformal void, `c = 1.5`) and unequal
backgrounds (`3.0`/`0.7`), giving `b_w = 2.4476`, `b_v = 0.5711`.

**Alternate paths that could drop `b_r - 1`: none exist.** `delta_m_carrier`
is written at exactly one place (`density.py:303`); the only other consumer
of carrier density in the package is `dressed.py`, which re-derives its
contrast from `rho_carrier` and never from `delta_m_carrier`
(`dressed.py:223-235`). Grep over `src/` confirms `delta_m_carrier` has no
consumer outside `density.py`.

**Finding 3: `PASS`.**

---

## 4. Non-tautological broken intertwining — the primary gate

**4a. What the code actually checks.** `density.py:307-322` restricts the
already-assembled `delta_C` to each region's own indices, applies that
region's broken operator, and compares against `b_r * regional_source`, where
`regional_source` is the **original input** `Delta_r` stored at reconstruction
time. So the right-hand side is the untouched input; the left-hand side
traverses solve → physical density → partition → carrier contrast →
restriction → broken apply.

**4b. `P_rho` is not an inverse carrier operator.** There is no
`ContinuumTransfer` construction, no `solve_projected_load`, and no
target-potential recovery anywhere in `density.py`. The prolongation is the
affine map `delta_r -> (b_r - 1) + b_r delta_r` realized physically through
`rho`, and `P_Delta^rho` is `Delta_r -> b_r Delta_r`. Both are defined from
the regional physical densities and backgrounds, which is the intended
physical definition; neither is defined by inverting the carrier operator on
a transferred CGI field. This specific tautology is absent.

**4c. The identity is a theorem, and I verified it is exact.** Since
`L_r(constant) = 0` **exactly** (§2a) and `L_r` is linear,
`L_r(delta_C|_r) = L_r((b_r - 1) + b_r delta_r) = b_r L_r(delta_r) = b_r Delta_r`
whenever `delta_r` solves the regional equation. It holds in both regions,
and I confirmed it survives unequal regional geometry *and* unequal
backgrounds (residuals `5.24e-14` / `6.22e-15` in my conformal-void stress
fixture).

**4d. But the numerical residual is a round-trip restatement.** From 4c the
residual reduces identically to `b_r × (L_r delta_r - Delta_r)`, i.e. `b_r`
times the elliptic equation residual that `solve_regional_laplace_beltrami`
has *already* checked and gated. Measured on the frozen fixture:

| quantity | wall | void |
|---|---|---|
| elliptic equation residual | `1.2989609388114332e-14` | `6.88e-15` |
| intertwining residual | `2.398081733190338e-14` | `9.769962616701378e-15` |
| `max｜intertwining − b_r·elliptic｜` | `1.42e-14` | `8.44e-15` |

The two diagnostics differ only by floating-point summation order. The
intertwining number is not independent evidence.

**4e. The residual is blind to the very term §3 exists to protect.** I built
a counterfixture that drops the `(b_r - 1)` offset entirely
(`delta_C := b_r delta_r`), changing the carrier field by `0.333`. The
intertwining residuals become `1.78e-14` (wall) and `4.55e-15` (void) —
*smaller* than the as-implemented values and far inside the `5e-10`
tolerance. **The gate cannot detect removal of the background offset**,
because the broken operator annihilates it exactly. Retention of `b_r - 1` is
in fact protected by the carrier global-mean gate and by
`test_t5`, not by the intertwining check.

**4f. What the residual does detect.** Four further counterfixtures show the
check is not empty:

| counterfixture | wall residual | void residual | detected? |
|---|---|---|---|
| C1 drop `(b_r - 1)` | `1.78e-14` | `4.55e-15` | **no** |
| C2 swap `b_w` ↔ `b_v` | `2.667` | `1.600` | yes |
| C3 `delta_C := delta_r` (no `b_r`) | `1.333` | `0.800` | yes |
| C4 one wall cell perturbed by `1e-6` | `8.0e-5` | `9.77e-15` | yes |
| C5 apply the **global** interface-crossing Laplacian | `12.533` | `12.533` | yes |

C5 is the meaningful one: had the implementation used the carrier's global
operator instead of the region-local broken operators, the residual would
exceed tolerance by ten orders of magnitude. Region-locality and the `b_r`
bookkeeping are genuinely tested.

**4g. Interface points are not removed — but the fixture cannot separate
them.** All regional cells, including every cell adjacent to `Gamma`, appear
as rows; only mask-crossing *edges* are omitted (the declared no-flux
policy). However, in the frozen `(4,4,4)` layered fixture the wall slab is
two cells thick and periodic wrap places `Gamma` on both of its faces, so
**all 32 wall cells are interface-adjacent and there are zero interior wall
cells**. Interface-row behaviour and interior-row behaviour therefore cannot
be distinguished in this fixture at all. Nothing is hidden, but nothing is
discriminated either.

**4h. Classification of the claim.**
`L_rho,C^br P_rho = P_Delta^rho L_rho,reg` is
**`DERIVED_ONLY_UNDER_ADDITIONAL_CONDITIONS`**. It is a genuine theorem of
the discrete construction — not `TAUTOLOGICAL_VALIDATION`, since C2/C3/C5
show real detection power, and not `NOT_ESTABLISHED`, since I reproved and
reproduced it independently — but it is conditional on (i) the selected
regional mean-zero normalization, (ii) the no-flux broken-operator
definition, (iii) the affine carrier definition, and its *numerical*
validation re-uses the inversion it is meant to corroborate and is blind to
the constant sector.

**Finding 4: `PARTIAL`.** Additionally, `tests/test_phase1f_a_density.py:157`
is named `test_t8_broken_intertwining_is_regionwise_and_non_tautological`
while its body asserts only two residual bounds and one status string. No
counterfixture, perturbation, or negative control appears anywhere in the
frozen suite. The test name asserts a property the test does not exercise:
`SOURCE_MISREPRESENTED` at test-name level.

---

## 5. Interface firewall

Physical density jumps freely across `Gamma`. Independently recomputed on the
frozen fixture: 32 interface faces, `max|rho jump| = 1.175` (exactly the
reported value), `min = 0.825`, `mean = 1.000`, against a pure background
discontinuity `|rho_bar_w - rho_bar_v| = 1.0`. The jump is dominated by the
declared background contrast, which is the point: nothing smooths it.

- H1 transmission-potential continuity is not reused as density continuity:
  `interface_faces` is consulted **only** to measure the jump
  (`density.py:346-349`); no continuity, flux, trace, or junction operation
  touches `rho`.
- No smoothing or interpolation exists on the density path.
- No naive global Laplacian is applied to the sharp field. The global
  `stiffness_matrix` is used only in the spectral sector, on eigenvectors,
  never on `rho_C` or `delta_C` (verified by consumer grep). C5 in §4f
  quantifies what would happen if it were: residual `12.53`.
- The broken operators are region-local by construction: mask-crossing edges
  are skipped at assembly (`operators.py:111-112`), and each operator acts
  only on its own index set.

**Finding 5: `PASS`,** with the §4g caveat that the fixture has no interior
wall cell, so region-locality is exercised only in the all-boundary regime.

---

## 6. Dimensional semantics

`physical_regional_volumes`, `regional_comoving_volumes`, and
`metric_derived_regional_comoving_volumes` all route through
`carrier.require_physical_volume_semantics`, which fails closed unless
`dimension == 3` (`continuum_geometry.py:302-315`,
`continuum_backend.py:941-985`). Phase 1F-A delegates through
`Phase1FAScientificState.require_physical_three_dimensions`
(`models.py:269-274`), called by `assemble_carrier_density` and
`map_carrier_density_to_dressed`. `DressedSpacetimeMapClosure` independently
rejects `spatial_dimension != 3` (`models.py:440-441`).

Probes executed against a live `d = 2` state, all closed:
`physical_regional_volumes` → `ContinuumDimensionalContractError`;
`require_physical_three_dimensions` → `Phase1FADimensionalContractError`;
`assemble_density` → `Phase1FADimensionalContractError`. The `d = 1` and
`d = 2` regional inversions survive and self-classify
`MATHEMATICAL_OPERATOR_FIXTURE_ONLY`, as documented.

One residual, narrow exposure: `CarrierDensityResult` is exported in
`__all__` and its `__post_init__` runs no dimension gate, so a caller can
hand-mint a record carrying
`scientific_classification = PHYSICAL_H1_CARRIER_DENSITY_CONDITIONAL_3D_ONLY`
bound to a 2-D state. I did exactly that. It is a **label-only** exposure:
feeding it to `map_dressed_density` still failed closed with
`Phase1FADimensionalContractError`, since every consumer re-gates through the
sealed state. No physical *number* escapes; only a self-applied label.

`reconstruct_regional_expansion` does not call the 3-D gate. That is
defensible — `deltaTheta` carries no volume semantics — and the `d != 3` path
still self-classifies as a fixture. Recorded for completeness.

**Finding 6: `PASS_WITH_EXPLICIT_CONDITIONS`.**

---

## 7. Spectral sector

Generalized problem `K q = lambda M q` with `M = diag(w_i J_i)`: correct mass
matrix in both the regional (`spectral.py:165-167`) and carrier
(`spectral.py:223-226`) paths. Eigenvectors are `M`-orthonormalized and the
normalization residual is gated (`spectral.py:181-186`, `240-246`);
`eigh(K, M)` returns `M`-orthonormal vectors and the residual gate confirms
it. Eigenpair residuals reproduce: regional `9.28e-15`, carrier `2.29e-14`.
Carrier labels are `lambda_Gamma_n`; the record hard-rejects any label equal
to `k` or containing `observ`. Regional labels are `k_wall_physical` /
`k_void_physical`, always paired with the metric identity and explicit scale
units. No carrier eigenvalue is observationally named.

**The `0.5` vs `32.0` distinction is reproducible but not discriminating.** I
recomputed both: ordinary constrained stiffness minimum `0.49999999999999944`,
first generalized eigenvalue `31.999999999999957`, ratio
`0.015625000000000003` — exactly the uniform mass `w·J = 1/64`. In this
fixture the two spectra are related by a *global constant*, because
`flat_regional_geometry` gives `J ≡ 1` and the carrier weights are uniform.
The code is right to use `M`; the validation fixture simply cannot exhibit a
genuinely non-proportional difference, so the reported pair does not
substantiate "deliberately distinct" beyond a scale.

**The off-diagonal number is basis-dependent within degenerate eigenspaces.**
The carrier spectrum is `{0, 32×6, 64×15, …}` and the four retained regional
eigenvalues are **all** `32`. The 10 retained carrier modes therefore consist
of the whole `lambda = 32` sextet plus an arbitrary 4 of the 15-dimensional
`lambda = 64` eigenspace, and both bases are arbitrary orthonormal frames
inside degenerate subspaces. `kernel_max_off_diagonal = 0.6206389035552144`
reproduced exactly (and is also the maximum of `|U|` overall), but it is not
an invariant of the problem: any LAPACK-level change of eigenvector
convention could move it, and with a `10 × 4` kernel "off-diagonal" is not a
well-defined notion to begin with.

I therefore computed the basis-**invariant** substitute — Frobenius norms of
the blocks grouped by eigenvalue, which are unchanged under any rotation
inside a degenerate eigenspace:

| carrier λ | regional λ | ‖block‖_F |
|---|---|---|
| 32 | 32 | `1.41421356` (= √2) |
| 64 | 32 | `0.78702612` |

The nonzero `(64, 32)` block is genuine, basis-independent mode mixing: a
regional `lambda = 32` eigenmode is transferred with substantial weight onto
carrier modes of a *different* eigenvalue. **The scientific conclusion —
non-diagonal mode transfer — survives adversarial scrutiny; the specific
number recorded in the artifact does not qualify as an invariant.** No hidden
sorting or relabelling was found: `eigh` output order is used as-is and the
kept indices are the first `mode_count` above tolerance. Projection
remainders are large (`0.53`–`0.63`), consistent with the internal audit's
own truncation caveat. Empirically the value did reproduce byte-for-byte
across numpy 2.5.2/scipy 1.18.1 and numpy 2.4.6/scipy 1.17.1.

**Finding 7: `PARTIAL`** — implementation correct; two reported numbers
(`0.5` vs `32.0`, and `0.6206389036`) are weaker evidence than the prose
around them implies.

---

## 8. Expansion reconstruction

`reconstruct_regional_expansion` solves `Delta_gamma_r deltaTheta_r = Z_r`
through the identical gated regional solver. Independently reproduced:
`max error = 5.551115123125783e-16` (exact match), equation residual
`4.26e-14`. The record's public fields are `delta_theta`, `z_cgi`,
`regional_values`, `regional_source`, `regional_indices`, `domain`,
`zero_mode_closure`, `boundary_policy`, `diagnostics`,
`background_expansion_identity`, `scientific_classification`, `provenance` —
no velocity, peculiar-velocity, or velocity-divergence field, and no aliasing
path anywhere in the package converts `delta_theta` into a velocity. The only
field in the whole package containing "veloc" is
`LongitudinalRelativeVelocityResult.longitudinal_relative_dust_to_wall_velocity`,
which is reachable only through an explicit boost closure (§9).

**Finding 8: `PASS`.**

---

## 9. Boost firewall

`reconstruct_longitudinal_relative_velocity` is the **only** function in the
package that returns a velocity, and `boost_closure` is a required
keyword-only parameter with no default; `None` raises before any computation.
The closure must additionally match the region, the regional metric identity,
and the zero-mode closure provenance — all three verified as live gates.

Attempts to find hidden equivalents, all negative: no `ZeroBoostClosure`
class or attribute; no `v_d = v_w` path; nothing derived from the background
lapse; no path constructing a boost from `Z`, from `delta_theta`, from the
expansion reconstruction, or from a wall/void expansion difference. The
expansion and boost modules share only the generic elliptic solver, never a
field.

Two precise observations:

- An **explicitly declared** all-zero divergence closure is accepted and
  yields `|v| = 0`. That is a caller's declared physical choice carrying full
  provenance metadata, not an implicit default; the frozen claims
  (`zero_boost_class: NOT_IMPLEMENTED`, "no missing-argument fallback") remain
  accurate as worded. Recorded so the distinction is explicit.
- In the **potential** branch the reported `boost_residual_max_abs` is
  structurally `0.0`: `supplied_divergence` is produced by
  `apply_regional_laplace_beltrami(psi)` and `reconstructed_divergence` by the
  same call on the same input, so the two arrays are bit-identical
  (verified: `np.array_equal` → `True`). The diagnostic can never be nonzero
  in that branch. No frozen report quotes it, so nothing is misrepresented,
  but it is an uninformative gate.

Longitudinal-only reconstruction confirmed: the returned field is
`gamma^{ab} partial_b psi` (`boost.py:93-138`), and every result carries
`TRANSVERSE_SECTOR_UNRESOLVED`, enforced at construction
(`boost.py:65-66`). Divergence residual reproduced exactly:
`2.5979218776228663e-14`; recovered potential matches the analytic
`0.2 · scalar` to `3.54e-16`.

**Finding 9: `PASS_WITH_EXPLICIT_CONDITIONS`** (potential-branch residual is
vacuous; explicit zero-boost input is admissible by design).

---

## 10. Dressed-map firewall

No dressed density is obtainable without `DressedSpacetimeMapClosure`:
required keyword-only, `None` raises first (`dressed.py:211-212`), followed by
carrier integrity, the 3-D gate, closure integrity, and a source-frame match.

Order verified in the executable path (`dressed.py:223-235`): map `rho_C`
through the destination indices → build the destination measure
`w · J · Jacobian` → recompute `rho_bar_dressed` → only then form
`rho/rho_bar - 1`. My independent recomputation matches the package **exactly**
(`0.0` difference).

Reported difference reproduced exactly: `0.025497933993807287`. I also
derived it analytically: since the fixture's spatial map is a *permutation*,
`delta_dressed = (rho_bar_C/rho_bar_D)(1 + delta_C) - 1`, so the discrepancy
from the forbidden direct-contrast pullback is exactly
`(rho_bar_C/rho_bar_D - 1)(1 + delta_C)`, whose maximum I computed
independently as `0.025497933993807287` — identical to the reported number,
with `rho_bar_D = 1.5259388588680012` against `rho_bar_C = 1.5`.

This confirms the two operations are inequivalent, which is the claim. It
also bounds what the demonstration shows: with a bijective index map the only
possible difference **is** the global mean renormalization. A non-injective or
measure-redistributing map would exercise more. No internal helper bypasses
the distinction — `delta_m_carrier` has no consumer in `dressed.py`.

**Finding 10: `PASS_WITH_EXPLICIT_CONDITIONS`.**

---

## 11. Physical-density positivity gate

`density.py:298-301` raises unless `rho_r = rho_bar_r (1 + delta_r) > 0` on
each region's own cells. It sits inside `assemble_carrier_density`, i.e. only
on the path that claims physical density semantics; `reconstruct_regional_density`,
`reconstruct_regional_expansion`, the spectral sector, and the boost sector
are untouched by it, so reduced-dimensional and non-physical fixtures still
run. Confirmed by diff inspection: the correction added a guard and rescaled a
*fixture*; no equation, tolerance, frame, closure, or authorization changed
(the commit is additive, and the tolerances in the inventory match those in
both the test utilities and the validator).

Scientific assessment: strict positivity is consistent with a realization
that labels `rho_C` a physical matter density, and it is the honest response
to a synthetic fixture that had wandered outside the linear branch. Two
limitations should be recorded rather than fixed:

- `rho = 0` is rejected by the same `<= 0.0` test. For a dust realization a
  vacuum cell is a legitimate boundary case, and rejecting it is a modelling
  choice, not a theorem. It deserves an explicit classification rather than
  silent inclusion in a positivity guard.
- The guard is evaluated on the *linear* reconstruction. It constrains the
  fixture amplitude rather than certifying that the linear construction is
  physically valid where it passes; passing the guard is not evidence of
  linear-regime validity.

**Finding 11: `PASS_WITH_EXPLICIT_CONDITIONS`.**

---

## 12. Scientific-state integrity under adversarial mutation

Every attack I constructed failed closed:

| attack | result |
|---|---|
| assign a new `morphology` onto the assembled operator | `ContinuumStateIntegrityError` (sealed `__setattr__`) |
| re-enable writes on `operator._weights` | `ValueError` — it is a read-only *view*; the flag cannot be restored at all |
| in-place write to `morphology.wall_domain` | `ValueError: assignment destination is read-only` |
| force-write the mask via `setflags`, then use | `ContinuumStateIntegrityError: live continuum scientific state differs from validated assembly` |
| swap `numerics` for looser tolerances on a sealed realization | `Phase1FAStateIntegrityError` |
| reuse regional densities from state A against a new state B | `Phase1FAContractError: regional densities must share the carrier scientific state` |
| pass an equal-valued but distinct morphology as `h1_partition` | `Phase1FAContractError` (object identity required) |
| inflate `wall_physical_volume` 2× | `Phase1FAContractError: regional physical-volume consistency failed` |
| negative background density | `Phase1FAContractError` |
| mutate a boost closure array / provenance after construction | `Phase1FAStateIntegrityError` (suite + validator, re-confirmed) |
| mutate `destination_frame` on a dressed closure | `Phase1FAStateIntegrityError` |
| tamper with `wall_physical_volume` on a built `CarrierDensityResult` | `Phase1FAStateIntegrityError` |
| hand-mint a physical-classification result on a 2-D state, then map | `Phase1FADimensionalContractError` (label mints, no number escapes — see §6) |

The mechanism is sound: object identities plus SHA-256 array fingerprints,
re-validated at the start of every downstream operation, layered on top of the
frozen Phase 1E-G assembly snapshot.

**Finding 12: `PASS`.**

---

## 13. Firewall search for forbidden scientific surface

Searched `src/timescape_fsigma8/phase1f_a/**`, the six 1F-A test modules, the
test utilities, the validator, the three 1F-A reports, and the generated
artifact keys for: `sigma_R`, `sigma_8`, `f sigma_8`, matter power spectrum,
RSD/Kaiser, tracer/galaxy velocity, observational `k`, bias, likelihood,
covariance, fitting/data comparison, S1 fallback, automatic D3 selection, and
physical-interface promotion.

Every hit is either (a) prohibition prose in a docstring or report, which I
did not count, or (b) the package name `timescape_fsigma8` appearing in import
statements. There is **no executable or public path** implementing or implying
any forbidden quantity. `phase1f_a.__all__` contains none of the forbidden
names. `interface_physical_status` and `CARRIER_PHYSICAL_STATUS` remain the
frozen 1E-G non-physical tokens. `D3Branch` is untouched and
`barotropic_matrix(branch=...)` still has no default (re-verified). No S1
symbol exists.

**Finding 13: `PASS`.**

---

## 14. Independent numerical reproduction

I rebuilt the wall/void broken operators from scratch — my own stiffness
assembly, my own mass vector, my own KKT solve — without calling the package
operators, then compared. Results below are *my* numbers next to the frozen
claims.

| Quantity | Frozen claim | Independently obtained | Agreement |
|---|---|---|---|
| wall density inversion max error | `1.7694179454963432e-16` | `1.7694179454963432e-16` | exact |
| void density inversion max error | `9.020562075079397e-17` | `9.020562075079397e-17` | exact |
| independent solve vs package solve | — | `1.67e-16` | consistent |
| independent solve vs analytic | — | `2.78e-17` | consistent |
| zero-mode ambiguity | `3.0` (vacuous) | `L(δ+C)−L(δ)`: `1.95e-14` / `9.06e-14` / `1.02e-11` for `C = 3 / 7.25 / −1234.5`; `L(const) = 0.0` exactly | claim true, frozen evidence vacuous |
| carrier global mean residual | `-1.5612511283791264e-17` | `-1.5612511283791264e-17` | exact |
| `b_w`, `b_v`, `rho_bar_C` | `4/3`, `2/3`, `1.5` | identical | exact |
| offset formula error (wall/void) | `2.22e-16` / `5.55e-17` | identical | exact |
| wall intertwining residual | `2.398081733190338e-14` | `2.398081733190338e-14` | exact |
| void intertwining residual | `9.769962616701378e-15` | `9.769962616701378e-15` | exact |
| intertwining − `b_r`·elliptic | not reported | `1.42e-14` / `8.44e-15` | **new: the two diagnostics coincide** |
| max interface density jump | `1.175` | `1.175` (min `0.825`, mean `1.000`, 32 faces) | exact |
| expansion max error | `5.551115123125783e-16` | `5.551115123125783e-16` | exact |
| regional / carrier eigenpair residuals | `9.28e-15` / `2.29e-14` | identical | exact |
| ordinary vs generalized first eigenvalue | `0.5` vs `32.0` | `0.49999999999999944` vs `31.999999999999957`, ratio `= w·J = 1/64` | exact, but proportional |
| kernel max off-diagonal | `0.6206389035552144` | `0.6206389035552144`; invariant blocks `√2` and `0.787` | exact; invariant substitute supplied |
| boost divergence residual | `2.5979218776228663e-14` | `2.5979218776228663e-14` | exact |
| dressed destination mean residual | `-6.943283854099497e-17` | `-6.943283854099497e-17` | exact |
| dressed vs direct-contrast pullback | `0.025497933993807287` | `0.025497933993807287`, and analytically `max(ρ̄_C/ρ̄_D − 1)(1+δ_C)` | exact + derived |
| artifact regeneration | byte-for-byte | SHA-256 identical on Python 3.14.3 **and** 3.11.9 with different numpy/scipy | exact |

**No material numerical difference was found.** Every reported number that
corresponds to a real computation reproduced to the last digit. The only
discrepancies are between *numbers and the claims attached to them*
(`zero_mode_shift_demonstration`, the `0.5`/`32.0` pair, the off-diagonal
maximum), documented in §2, §4 and §7.

**Finding 14: `PASS`.**

---

## 15. Convergence

I reconstructed the definition rather than accepting the rates. The study
(`validate_phase1f_a_h1_closure.py:430-455`) builds realizations of shape
`(4, N, N)`, feeds the **continuum** Laplacian
`-(2π)²[sin(2πy) + 0.25 cos(2πz)]` as the CGI source, solves, and takes the
RMS difference against the exact scalar on the wall. Rates are
`log(e_coarse/e_fine)/log(h_coarse/h_fine)` with `h = 1/N`.

What that measures: for a pure Fourier mode the discrete operator has
eigenvalue `-4 sin²(πh)/h²` against the continuum `-(2π)²`, so the
reconstruction is the exact field scaled by `(πh/sin πh)²`, and the error is
in closed form,

```
e(N) = ((π h / sin π h)² − 1) · ‖exact‖_rms ,   h = 1/N .
```

I evaluated that formula independently and compared against the solver:

| N | solver L2 error | analytic prediction | ratio | rate |
|---|---|---|---|---|
| 4 | `0.1703370832` | `0.1703370832` | `1.000000` | — |
| 6 | `0.07042529764` | `0.07042529764` | `1.000000` | `2.1783` |
| 8 | `0.03865140309` | `0.03865140309` | `1.000000` | `2.0855` |
| 10 | `0.02445967052` | `0.02445967052` | `1.000000` | `2.0505` |
| 12 | `0.01688273313` | `0.01688273313` | `1.000000` | `2.0334` |

The first three rows reproduce the frozen table exactly; rows 4–5 are my
extension. The error is **entirely** the stencil consistency error of a single
manufactured mode, and the observed rates are the pre-asymptotic values of
`(πh/sin πh)² − 1 → π²h²/3`, descending monotonically to 2 from above.

Assessment: "second-order" is *arithmetically* justified for this quantity,
but the quantity carries no information about the object under test. The
refinement never touches axis 0 — the layering/interface axis — and both
manufactured modes are constant along it, so no-flux at `Gamma` is trivially
satisfied and the interface treatment is never exercised at any resolution.
The frozen report's caveat ("not a universal rate across a sharp physical
interface") is correct but understates the situation: this is not a solver
convergence study at all, it is a closed-form stencil identity.

**Finding 15: `PASS_WITH_EXPLICIT_CONDITIONS`.**

---

## 16. Authorization matrix, row by row

Each row challenged against the evidence actually present.

| Row | Frozen value | Independent verdict |
|---|---|---|
| regional density nonzero modes | GRANTED | survives — exact inversion independently reproduced |
| regional full density | CONDITIONAL | survives — the constant sector is not determined by the source |
| physical H1 carrier density | CONDITIONAL | survives |
| broken density intertwining | GRANTED_UNDER_SELECTED_NORMALIZATION | survives **as worded in the matrix**; the *final-verdict token* does not (see below) |
| physical 3-D carrier semantics | CONDITIONAL_3D_ONLY | survives — probes fail closed at `d = 1, 2` |
| regional physical scale | CONDITIONAL | survives |
| H1 generalized spectrum | GRANTED_THEORETICAL | survives; evidence is proportional-only in this fixture (§7) |
| regional–carrier spectral kernel | GRANTED_THEORETICAL | survives on the invariant block norms, not on the reported off-diagonal maximum |
| global dressed Fourier k | NOT_GRANTED | survives |
| regional expansion reconstruction | CONDITIONAL | survives |
| Timescape-predicted dust–wall boost | NOT_GRANTED | survives |
| external longitudinal boost realization | CONDITIONAL | survives |
| full vector wall velocity | NOT_GRANTED | survives — transverse sector enforced unresolved |
| dressed density from Timescape alone | NOT_GRANTED | survives |
| dressed density with explicit external map | CONDITIONAL | survives |
| tracer velocity | NOT_GRANTED | survives |
| matter power spectrum | NOT_GRANTED | survives |
| smoothing variance at any radius | NOT_GRANTED | survives |
| redshift-space distortion | NOT_GRANTED | survives |
| observational growth observable | NOT_GRANTED | survives |
| likelihood / data comparison | NOT_GRANTED | survives |

**The one row requiring downgrade.** The final machine verdict in
`reports/phase1f_a_h1_carrier_dressed_closure_validation.md` §25 and in
`final_verdict.broken_density_intertwining` of the inventory reads
`BROKEN_DENSITY_INTERTWINING: DERIVED` — unqualified — while the
authorization matrix in the *same two documents* reads
`GRANTED_UNDER_SELECTED_NORMALIZATION` and
`intertwining_identity.classification` reads
`DERIVED_UNDER_SELECTED_NORMALIZATION`. Those are not the same claim, and the
evidence supports only the qualified one (§4). The unqualified token should be
downgraded to match its own matrix row:
`BROKEN_DENSITY_INTERTWINING: DERIVED_UNDER_SELECTED_NORMALIZATION`.

No row is upgraded by this audit.

**Finding 16: `PARTIAL`** — one internally inconsistent verdict token,
resolved in the direction the evidence supports.

---

## Additional finding — committed report integrity

`reports/phase1f_a_h1_carrier_dressed_closure_validation.md` ends, **after**
the closing fence of the final verdict block, with two dangling truncated
sentence fragments:

```
density jump of `2.75`. Gamma remains a mathematical transfer interface and
density jump of `1.175`. Gamma remains a mathematical transfer interface and
```

These are editing residue from an earlier revision. The first states an
interface density jump of `2.75`, which **contradicts** §11 of the same
report, the inventory
(`validation_metrics.maximum_interface_density_jump = 1.175`), the generated
artifact, and my independent recomputation (`1.175`). No fixture in the frozen
commit produces `2.75`; I obtained `2.5569` only from a stress fixture I
constructed myself with different parameters, which confirms the value is
stale rather than merely mislabelled.

A frozen scientific deliverable that carries an unsupported numeric claim
contradicting its own validated result is a documentation-integrity defect,
independent of the correctness of the code.

**Finding 17: `PARTIAL`, `SOURCE_MISREPRESENTED`.**

---

## Finding classification summary

| # | Area | Classification |
|---:|---|---|
| 0 | Provenance preflight | `PASS_WITH_EXPLICIT_CONDITIONS` |
| 1 | Regional density equation, signs, dimensions | `PASS` |
| 2 | Zero-mode theorem and closure character | `PARTIAL` (+`SOURCE_MISREPRESENTED`) |
| 3 | Physical carrier construction, `b_r − 1` retention | `PASS` |
| 4 | Broken intertwining | `PARTIAL` (+`SOURCE_MISREPRESENTED`, test name) |
| 5 | Interface firewall | `PASS` |
| 6 | Dimensional semantics | `PASS_WITH_EXPLICIT_CONDITIONS` |
| 7 | Spectral sector | `PARTIAL` |
| 8 | Expansion reconstruction | `PASS` |
| 9 | Boost firewall | `PASS_WITH_EXPLICIT_CONDITIONS` |
| 10 | Dressed-map firewall | `PASS_WITH_EXPLICIT_CONDITIONS` |
| 11 | Physical-density positivity gate | `PASS_WITH_EXPLICIT_CONDITIONS` |
| 12 | State integrity | `PASS` |
| 13 | Firewall search | `PASS` |
| 14 | Numerical independence | `PASS` |
| 15 | Convergence | `PASS_WITH_EXPLICIT_CONDITIONS` |
| 16 | Authorization matrix | `PARTIAL` |
| 17 | Committed report integrity | `PARTIAL` (+`SOURCE_MISREPRESENTED`) |

Counts: `PASS` 7 · `PASS_WITH_EXPLICIT_CONDITIONS` 6 · `PARTIAL` 5 ·
`UNSUPPORTED` 0 · `INCORRECT` 0 · `NOT_APPLICABLE` 0.

Intertwining claim classification:
**`DERIVED_ONLY_UNDER_ADDITIONAL_CONDITIONS`**.

---

## Primary verdict

```text
REQUIRES_TARGETED_CORRECTIONS
```

No equation, sign, unit, dimension, firewall, or authorization *ceiling* is
wrong, and no forbidden observational surface exists. Every reported number
that corresponds to a real computation reproduced exactly, on two different
numerical stacks. The corrections required are confined to the **frozen
documentation and one verdict token**, plus optional strengthening of the
validation evidence; **no implementation change is required**.

---

### A. Blocking corrections before push or integration

1. Remove the two dangling fragments at the end of
   `reports/phase1f_a_h1_carrier_dressed_closure_validation.md`, including the
   contradictory `2.75` interface-jump value (Finding 17).
2. Downgrade the unqualified final-verdict token in both the validation report
   §25 and `final_verdict.broken_density_intertwining` of the inventory from
   `DERIVED` to `DERIVED_UNDER_SELECTED_NORMALIZATION`, matching the
   authorization matrix and `intertwining_identity.classification` in the same
   documents (Finding 16).
3. Correct report §8 and the artifact key `zero_mode_shift_demonstration` so
   the recorded quantity matches the claim. Either record a real invariance
   residual (`max|L_r(δ+C) − L_r(δ)|`, values in §2a of this report) or drop
   the word "demonstration" (Finding 2b).
4. Re-label the zero-mode closure honestly. Since `mean_condition` admits
   exactly one value, either state in the report and inventory that the
   *declaration* is external while the *value* is a fixed V1 model assumption,
   or widen the admissible set. `EXPLICIT_EXTERNAL_NORMALIZATION_CLOSURE` as
   currently worded overstates externality (Finding 2c).

### B. Non-blocking scientific limitations

1. The intertwining residual equals `b_r ×` the already-gated elliptic
   residual and is **blind to removal of the `(b_r − 1)` offset**; retention of
   that term rests on the global-mean gate and `test_t5` alone. Adding C1/C2/C5
   from §4f as negative controls would make the gate self-evidencing.
2. `test_t8_broken_intertwining_is_regionwise_and_non_tautological` asserts no
   non-tautology property. Rename it, or give it a counterfixture.
3. The `(4,4,4)` layered fixture has **zero interior wall cells** — every wall
   cell touches `Gamma` — so interface and interior rows are indistinguishable.
   A thicker slab would separate them.
4. Both regional geometries are the identical flat unit metric (`J ≡ 1`) with
   uniform carrier weights, so the ordinary/generalized spectral "distinction"
   collapses to a constant factor `1/64`. A non-unit `J` fixture would make the
   claim discriminating. (I verified separately that the carrier chain,
   intertwining, and global mean all still hold under a conformal void
   geometry with unequal backgrounds.)
5. `kernel_max_off_diagonal` is not basis-invariant: the retained carrier
   modes truncate a 15-fold degenerate eigenspace, and all four regional modes
   share one eigenvalue. Record the eigenvalue-block Frobenius norms (`√2` and
   `0.787`) instead — they are invariant and carry the same conclusion.
6. The convergence study measures a closed-form single-mode stencil
   consistency error and never refines the interface axis. It should not be
   read as evidence about the broken solver.
7. The potential-branch boost residual is structurally identically zero.
8. The dressed-map demonstration uses a permutation, so it probes only the
   global mean renormalization, not measure redistribution.
9. `rho = 0` is rejected by the positivity guard; the vacuum boundary case
   deserves an explicit classification.
10. `CarrierDensityResult` is publicly constructible with a physical
    classification bound to a reduced-dimensional state. Label-only exposure —
    every consumer re-gates — but it could be sealed at construction.

### C. Independently reproduced numerical findings

The full table is §14. Highlights: all 18 frozen numerical claims that
correspond to real computations reproduced **exactly**, including the artifact
SHA-256 `ed3fcdc4aa54…be47` on two interpreters with different numpy/scipy.
New quantities established by this audit: `L_r(const) = 0.0` exactly;
`max|intertwining − b_r·elliptic| ≈ 1.4e-14`, i.e. the two gates coincide;
the C1 counterfixture residual `1.78e-14` proving offset-blindness; the C5
global-Laplacian residual `12.53`; invariant kernel block norms `√2` and
`0.787`; the closed-form convergence identity matching the solver to ratio
`1.000000` at `N = 4, 6, 8, 10, 12`; and the analytic derivation of the
dressed difference `0.025497933993807287`.

### D. Authorization rows that survive unchanged

All 21 rows of the authorization matrix in both the report and the inventory,
and all of `unique_timescape_prediction`, `physical_interface_claim`,
`observational_authorization`, `fsigma8_authorization`,
`differential_state_rank: 4`, `morphology`, `normalization`, `boost`, and
`dressed_map` as `REQUIRED_EXTERNAL_*`. The immutable scientific ceiling
stated in the audit charter is intact in the implementation.

### E. Authorization rows requiring downgrade

One: `BROKEN_DENSITY_INTERTWINING: DERIVED` →
`DERIVED_UNDER_SELECTED_NORMALIZATION` (final-verdict token in report §25 and
in `final_verdict.broken_density_intertwining`). No other downgrade, and no
upgrade.

### F. Recommendation concerning the existing commit and tag

**Preserve both, unchanged.** Commit `a56fa88b64062761fefc193d7061d1d12ba2dedd`
and annotated tag `phase-1f-a-h1-broken-density-spectral-boost-v1`
(object `c9cd0c5519052d08cf607e725b45dbf8a0cd8a9b`) are scientifically safe to
retain as the Phase 1F-A checkpoint: the implementation is correct in every
respect this audit could test, its provenance is intact, its results are
exactly reproducible, and no firewall or authorization ceiling is breached.

Do **not** move, delete, or recreate the tag, and do not amend the commit.
Land corrections A1–A4 as a *follow-up* commit on the same branch and freeze it
as `phase-1f-a-h1-broken-density-spectral-boost-v2`, exactly the pattern
already used for `phase-1e-f-…-v1 → v2` and `phase-1e-g-…-v1 → v4`. That
preserves the audited history while making the authoritative documentation
consistent with its own evidence.

Until A1–A4 land, the `-v1` report must not be cited as the final Phase 1F-A
scientific record: it contains one contradictory numeric claim and one verdict
token stronger than its own authorization matrix.
