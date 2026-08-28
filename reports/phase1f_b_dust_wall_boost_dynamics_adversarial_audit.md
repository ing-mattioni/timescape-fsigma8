# Phase 1F-B — Independent adversarial read-only audit

Audit classification: `INDEPENDENT_ADVERSARIAL_READ_ONLY_AUDIT`.

Audit date (UTC): 2026-08-26. Performed in a session separate from the
implementation. The implementation report, inventory, and completion response
were treated as **claims under test**, never as scientific authority.

Target: commit `27fd65fd2a05c5b990508d948703897f433b566e`, tag
`phase-1f-b-dust-wall-boost-dynamics-v1`, realization
`H1-1F-B-COMMON-SPACETIME-SCALAR-NORMAL-BOOST-DYNAMICS-V1`.

Nothing in the repository was modified, staged, committed, amended, stashed,
reset, restored, rebased, merged, cherry-picked, or pushed. The only file
created is this report, left untracked. All independent computation ran from
an ignored scratch directory; the validation artifact was regenerated only to
a scratch path.

---

## 0. Preflight and preservation

| # | Check | Expected | Observed | Status |
|---|---|---|---|---|
| 1 | Branch | `phase-1f-b-dust-wall-boost-dynamics` | identical | PASS |
| 2 | HEAD | `27fd65fd2a05c5b9…` | identical | PASS |
| 3 | Parent | `87af7976b82b0b38…` | identical, single parent | PASS |
| 4 | Tag object | `d784074049148fad…` | identical, object type `tag` | PASS |
| 5 | Peeled commit | `27fd65fd2a05c5b9…` | identical | PASS |
| 6 | `main` | `87af7976b82b0b38…` | identical | PASS |
| 7 | `origin/main` | `87af7976b82b0b38…` | identical (`git ls-remote`) | PASS |
| 8 | Worktree | clean | clean | PASS |
| 9 | Index | clean | clean | PASS |
| 10 | Active Git operation | none | none; `git stash list` empty | PASS |
| 11 | Upstream commit | `590c6fd5332acb15…` | identical | PASS |
| 12 | Upstream cleanliness | clean | `git status --porcelain` empty | PASS |
| 13 | Notebook SHA-256 | `86d2534db9e9b316…de55a` | identical | PASS |
| 14 | Tracked paths in `27fd65f` | 1F-B only + CLAUDE.md | 8 files: 7 added 1F-B files, `CLAUDE.md` modified; **0 deletions** elsewhere | PASS |
| 15 | `CLAUDE.md` provenance | pre-phase, hash `27fc001a…d317ce` | see below | PASS |
| — | `git diff --check` / `--cached --check` | clean | clean before and after the audit | PASS |
| — | Remote 1F-B branch/tag | absent | absent | PASS |

**CLAUDE.md adjudication.** The blob at `27fd65f` has SHA-256
`27fc001a755f98f2bdb18a6cdfb7a578b12b09eb1b41a240a7bfcad212d317ce` — exactly
the authorized pre-phase hash — and differs from the parent
(`b1b0302fcd9c…`). Its committed text contains **no** reference to Phase 1F-B,
`phase1f_b`, or the 565-test count, so it was not edited by the Phase 1F-B
work. The validation report §1 discloses it explicitly and classifies it
`AUTHORIZED_PREEXISTING_USER_MODIFICATION`, and the inventory records the same
path and hash. **The documentation change is not falsely attributed to the
Phase 1F-B scientific implementation.** The only residual remark is
stylistic: a 270-line documentation rewrite rides inside a scientific commit,
which is disclosed but not ideal.

**Test suites.** Run by this audit, `-p no:cacheprovider -rsxX`:

| Environment | Targeted 1F-B | Full suite | Failures | Skips | XFails | Warnings |
|---|---|---|---|---|---|---|
| Python 3.14.3 (numpy 2.5.2 / scipy 1.18.1) | 26 passed | **565 passed** | 0 | 0 | 0 | 0 |
| Python 3.11.9 (numpy 2.4.6 / scipy 1.17.1) | 26 passed | **565 passed** | 0 | 0 | 0 | 0 |

No warning suppression was used. The validation artifact regenerates
byte-for-byte identically on both stacks
(SHA-256 `8c43775e8e0436c621d19a68435516e866feaa11324add95e1990d002ce4a771`).

---

## 1. Realization identity and frozen boundary

`REALIZATION_ID` is consistent across `models.py`, the result record (which
raises if it changes), the report, and the inventory. The commit is purely
additive outside `CLAUDE.md`: no frozen Phase 1E-F/1E-G/1F-A source, test,
report, or inventory file was touched (`git diff --name-status 87af797
27fd65f`). `phase1f_b` imports **only** from `phase1f_a`; it imports nothing
from `background/`, `perturbations/`, `growth/`, or `transfer/` directly.
There is no occurrence of `void` anywhere in the package.

**A02, A25 (frozen regression): `PASS`.**

---

## 2. Frame sign — independent re-derivation (A03)

**Derivation.** For `u_d = u_W + v + O(v²)` with `v ⊥ u_W` at first order,
`Θ = ∇_a u^a` gives `Θ_d = ∇_a(u_W^a + v^a) = Θ_W + D_a v^a` to first order.
Backgrounds coincide in a common-spacetime closure, hence

```
D_a v^a_{d|W} = δΘ_{d,w} − δΘ_W ,   and for v_a = D_a ψ:  D²ψ = δΘ_{d,w} − δΘ_W .
```

The implemented sign is therefore correct. (The `dynamics.py` docstring writes
this as `Θ_W = Θ_d + D_a ξ^a`, which is consistent only under `ξ = −v`; the
notation is a readability trap, not an error.)

**Independent physical counterexample.** I built the check *outside* the
implementation: take ψ > 0 at a local maximum, so `v = Dψ` converges there
(dust falling together relative to the wall observers) and the dust congruence
must expand *less* than the wall congruence — `δΘ_d − δΘ_W < 0`. Using my own
second-order divergence of my own gradient (never the package operators) I get
`div v = −0.032` at that cell, and the code's `L ψ / a² = −0.064`; both
negative, same sign, magnitudes differing only by the stencil width (wide-2h
versus compact-3-point on a 4-cell grid: −16 versus −32 eigenvalue). The
reversed convention would require a *larger* dust expansion where dust
converges, which is unphysical.

**Independence of the repository's own sign test.** `test_v4` and the
validator's `reverse_sign` branch flip the sign of a wall expansion that the
same fixture manufactures from ψ; they demonstrate the code is *sensitive* to
the sign, not that the sign is physically right. That test alone is
`CONSTRUCTION_IDENTITY_ONLY`; the derivation and counterexample above supply
the missing independent evidence.

**A03: `PASS`** (sign correct, independently derived; repository evidence for
it is weaker than the report implies — see A28).

---

## 3. Operator identity, `a_w²` placement, dimensions (A08, A09, A10)

**What each operator is.** From the frozen Phase 1E-G definitions
(`continuum_geometry.py:145-224`): `metric_inverse = (Φ_r^*γ_r)^{-1}`,
`metric_volume_ratio J_r = dμ_{Φ*γ}/dμ_0`, weak-form density
`K_r = J_r γ̂^{ij}`; the geometry is required to be **time-independent**
(`metric_time_independent`), and the scale factor is carried separately
(`physical_regional_volumes = V_{r,i} a_r³`). Phase 1F-A assembles
`K = flux form of K_r`, `M = w·J`, and `apply_regional_laplace_beltrami`
returns `−(Ku)/M`, i.e. the mass-lumped Laplace–Beltrami of the **comoving**
metric γ_w. Coordinates are reference/comoving; `a_w` is a per-time
regional-background scalar (shape `(nt,)`), never local, never carrier-level.

With `g = a²γ` and `a` spatially constant, `Δ_g = a^{-2}Δ_γ`, hence
`L_w = a_w² D_w² = Δ_{γ_w}` — the same convention already frozen in
`phase1f_a/operators.py`. `a_w²` is therefore **not** absorbed into the
operator, and `D²ψ = Lψ/a²` (line 236) is right.

**Independent dimensional/scaling test.** I built my own physical gradient and
divergence (`∇/a`, `div/a`) and compared their `a`-dependence with the code:

| `a` | `max｜my D²ψ − code Lψ/a²｜` | `max｜my D²ψ − code Lψ｜` (no `1/a²`) |
|---|---|---|
| 1 | 3.20e-02 | 3.20e-02 |
| 2 | 8.00e-03 | 5.60e-02 |
| 3 | 3.56e-03 | 6.04e-02 |

The `1/a²` variant tracks `|D²ψ| ∝ a^{-2}` exactly (residual falls as `a^{-2}`,
the fixed ratio being the coarse-grid stencil-width factor 2); the variant
without `1/a²` diverges from it. The `a`-placement is independently confirmed.
Units are internally consistent (`a` is declared `DIMENSIONLESS`, so
"reference length" and "physical length" carry the same dimension; the labels
lose the `a`-factor but no dimensional error follows). Time dependence is
handled correctly: the operator is assembled once because γ is frozen
time-independent, and all time dependence enters through the scalar `a(t)`.
The same relation holds for every geometry the 1E-G backend admits (isotropic
tensor density enforced at assembly).

**Circularity check.** The code and the validator do share the factor: the
fixture manufactures `wall_expansion = dust − lapᵃⁿᵃˡʸᵗⁱᶜ/a²`. However
`lapᵃⁿᵃˡʸᵗⁱᶜ` is the **closed-form discrete eigenvalue** `−4sin²(π/N)/h²·mode`,
computed independently of the assembly, and `test_v11` / the validator's
`wrong_operator_scale_factor` branch show an omitted `1/a²` is rejected. So
the factor is not validated only by itself.

**A08 `PASS` · A09 `PASS` · A10 `PASS_WITH_EXPLICIT_CONDITIONS`** (unit labels
elide the `a`-factor; harmless because `a` is dimensionless).

---

## 4. Kernel / zero-mode handling (A11)

- The kernel of the broken wall operator is the constants **iff** the wall
  domain is connected. Phase 1F-A's assembly requires kernel dimension exactly
  1 and raises otherwise. I built a genuinely disconnected wall (layers 0 and
  2 of a 4-slab) and confirmed:
  `Phase1FADegeneracyError: wall regional operator must have exactly one
  constant kernel; got 2`. **Disconnected domains fail closed; no silent
  projection.**
- `Q₀ν_W` is legitimate for every geometry the runtime admits, because the
  admitted geometries are exactly those with a one-dimensional constant
  kernel.
- Normalization is caller-supplied and never auto-created: `REQUIRE_MEAN_ZERO`
  *rejects* a non-mean-zero lapse; `EXPLICIT_Q0_PROJECTION` must be chosen
  explicitly by the caller. Verified: adding `0.01` to the lapse raises under
  the first mode and is projected (correction `0.01`) under the second.
- Stage placement: the mean-zero condition is applied to `ν` (per time step,
  before propagation), to the supplied `ψ(t_i)` (before use), to the
  expansion-matched **source** (through the frozen solver's compatibility
  gate), and re-checked on the propagated `ψ` at every time.
- One structural remark: because `ψ` is updated by `ψ − (dt/2)(ν_i + ν_{i+1})`
  and the `a³` factor cancels in a weighted *mean*, mean-zero of `ψ` is
  preserved **exactly** whenever each projected `ν` is mean-zero. The
  `potential_mean_max_abs` gate (measured `1.6e-19`) is therefore an automatic
  consequence, not an independent check.

**A11: `PASS_WITH_EXPLICIT_CONDITIONS`.**

---

## 5. Propagation law and its geometric validity (A12, A13)

`v = Dψ = ∇_γψ/a` and `A = Dν`. Then
`v̇ = ∇ψ̇/a − H v`, so `v̇ + Hv = ∇ψ̇/a`, and imposing `v̇ + Hv = −A` gives
`∇(ψ̇ + ν) = 0`, i.e. `ψ̇ = −ν + C(t)`; the mean-zero representative fixes
`C = ⟨ν⟩`. This reproduces the implemented `ψ̇ = −Q₀ν`, with the correct sign
and the correct single factor of `H`. The commutator used is the FLRW one
(`[∂_t, D_a]` producing only the `−H` term), valid for a spatially homogeneous
background expansion on a time-independent comoving metric — which is exactly
what the closure enforces: `wall_hubble_rate` has shape `(nt,)` (homogeneous
by construction), γ is frozen time-independent, and `scalar_hypersurface_
orthogonal`, `vorticity_dust_zero`, `vorticity_wall_zero` must all be `True`.

**Gap: background shear.** The law also requires a shear-free background wall
congruence. The string `shear` appears **nowhere** in `phase1f_b/`, in the
validation report, or in the inventory. Vorticity is gated by explicit
booleans and homogeneity by array shape; the shear-free assumption is excluded
only by not being representable. "Quasi-FLRW" is therefore *partly* enforced
(homogeneity, vorticity, time-independent metric) and *partly* undeclared
(shear).

**A12 `PASS` · A13 `PASS` · A04 `PASS_WITH_EXPLICIT_CONDITIONS`** (see also
the inert proper-time field in §11).

---

## 6. Background wall lapse firewall (A05, A06)

`phase1f_b` imports nothing from `timescape_fsigma8.background`, where the
Timescape tracker and `γ_w = dt/dτ_w` live, so the background lapse is
**structurally unreachable**, not merely forbidden by a token check. The
closure has no `background_gamma_w` parameter, and `lapse_driver_kind` must
equal `PERTURBATIVE_WALL_LAPSE_POTENTIAL` — I confirmed
`BACKGROUND_TIMESCAPE_GAMMA_W` is rejected at construction. There is no naming
collision: the only lapse-bearing field is `wall_lapse_perturbation`, typed,
unit-tagged `DIMENSIONLESS_PERTURBATION`, and separate from the (absent)
background clock ratio. No wall acceleration or boost source can be
instantiated from `γ_w`.

**A05 `PASS` · A06 `PASS`.**

---

## 7. Expansion reconstruction (A07)

`Z_w → δΘ_{d,w}` is consumed as a tuple of frozen Phase 1F-A
`RegionalExpansionReconstruction` records. The scenario validator requires:
each entry is that exact type, `domain.region == "wall"`, the sealed H1
scientific state is the **same object** as the geometry closure's, the
background-expansion identity matches, and the history length equals the time
grid. Only `regional_values` (the wall-regional solve output) is read. There is
no void access anywhere, and no path converts `Z` to a velocity except through
`D²ψ = δΘ_d − δΘ_W`; the only velocity-bearing field in the package is
`dust_velocity_relative_to_wall`, produced solely from `ψ`.

**A07 `PASS`.**

---

## 8. Residual independence — the load-bearing evidence question (A14, A15, A16)

The two residuals are

```
C_Θ = δΘ_d,w − δΘ_W − Lψ/a²        R_A = A_W + v̇ + H_W v
```

**`R_A` is a construction identity.** Given the implemented construction
(`ψ` evolved by `ψ̇ = −ν`; `v := Dψ`; `A := Dν`), `v̇ + Hv + A ≡ 0` holds
identically in the continuum, as derived in §5. Three independent
demonstrations:

1. **No functional dependence on the expansion sector.** Three runs with
   completely different dust/wall expansion histories (`dust = 0.01`, `0.05`,
   `−0.03`) give `R_A = 5.204170e-18` in all three — *bit-identical* — while
   `C_Θ` changes (`5.55e-17`, `1.11e-16`, `6.94e-17`). `R_A` cannot see
   `δΘ_d` or `δΘ_W` at all.
2. **Machine-zero for arbitrary drivers.** With `a` constant and `H = 0`,
   `R_A` is `0.0`, `1.7e-18`, `6.7e-18` for three unrelated lapse histories.
3. **Analytically**, the discrete residual is exactly the trapezoid/midpoint
   truncation of an identity, nothing else.

**Case B (`R_A` passes, `C_Θ` fails): realizable.** Scaling the wall expansion
inconsistently raises `Phase1FBCompatibilityError` while the same dynamics with
a consistent expansion give `R_A = 5.20e-18`. Also `test_v3`, `test_v4`,
`test_v11`.

**Case A (`C_Θ` passes, `R_A` fails): realizable, but only through truncation.**
The coarse `dt = 1`, `a = e^t`, `H = 1` fixture raises
`Phase1FBPropagationError` at a `1e-12` gate. I verified the mechanism
analytically: with `ψ` constant and `A = 0`, the continuum residual is exactly
zero and the discrete one is `[(1/a₁−1/a₀)/dt + H̄(1/a₁+1/a₀)/2]·|g| ≈ 0.052|g|`
— pure discretisation error. **`R_A` can fail only for numerical-resolution
reasons, never for physical ones.**

**Verdict.** The two residuals are numerically decoupled, so the inventory's
`independent_of_expansion_compatibility = True` is literally true. But that
literal independence is achieved by `R_A` carrying *no information about the
physics under test*. The project already owns the correct vocabulary and
applies it to the curl —
`CONSTRUCTION_INVARIANT_NOT_INDEPENDENT_NUMERICAL_EVIDENCE` — and `R_A` merits
the same classification for the same reason. The report instead calls it "the
independently evaluated interval residual … evaluated … independently of
`C_Θ`", which overstates its evidential value.

`C_Θ` **is** a genuine constraint on the supplied data: `ψ` is fully
determined by `ψ(t_i)` and `ν`, so the externally supplied `δΘ_d`, `δΘ_W`,
`a` must satisfy an integrability condition that is checked, not imposed.

**A14 `PASS` · A15 `PASS` (as a discretisation diagnostic) ·
A16 `PARTIAL` (+`SOURCE_MISREPRESENTED` for the "independent" wording).**

---

## 9. Interface-condition firewall and domain semantics (A22, A23)

**What is reused.** The boost solver calls the Phase 1F-A *broken regional*
assembly, which omits every mask-crossing edge. It does **not** touch
`ContinuumH1Operator._stiffness` (the global transmission operator with
interface faces), `ContinuumTransfer`, `solve_projected_load`, or any
continuity/conormal-flux machinery. So no H1 density-transmission condition —
`[ψ]_Γ = 0` or `[aD_nψ]_Γ = 0` — is inherited. The policy record declares
`BOOST_WALL_INTERIOR_NO_FLUX_PERIODIC_TANGENTIAL`,
`EXPLICIT_BOOST_SPECIFIC_BOUNDARY_MODEL`, and rejects
`inherited_from_h1_density_transmission=True`.

**But the reused operator's domain does embed a boost boundary condition.**
Its natural condition is zero normal flux at Γ, i.e. a **no-penetration
condition on the dust-to-wall relative velocity**. I quantified it: for a field
varying along the interface normal, the broken operator differs from the
unbroken periodic Laplacian by `16.0` (O(1) relative). This is declared, not
hidden — but the report §12 says only that no no-penetration condition
"follows from the H1 transmission interface", and never states plainly that
the selected model *is* one.

**The condition is not enforced on the data.** In `SUPPLIED_INITIAL_BOOST`
mode, `ψ` is a caller-supplied full-grid field; the operator enters only
through the residual and the expansion-matched solve. I supplied a mean-zero
`ψ` with a normal jump of `0.004` across Γ. The runtime **accepted** it,
returned `|v_normal| = 0.016` at Γ-adjacent cells — a flow crossing Γ — and
evaluated `C_Θ` with an operator whose natural condition asserts the opposite.
There is no gate on `D_nψ|_Γ`.

**The condition is never exercised.** Every field in every test and in the
validator is `sin(2πz/N) + 0.25cos(2πy/N)` — exactly constant along axis 0,
the interface normal. Consequences I measured: the broken and unbroken
Laplacians agree to `3.55e-15` on every fixture field, and `|v_normal| = 0.0`
identically. **The phase's most load-bearing new modeling choice has zero
numerical evidence.**

**Domain classification: `WALL_INTERIOR_ONLY`** (broken wall operator, no-flux
at Γ, periodic tangential). No global broken-carrier path exists. The
inventory's `selected_sector[5] = WALL_INTERIOR_OR_EXPLICIT_BOUNDARY` is
vaguer than the runtime, which admits only `domain_id == "wall"`.

**A22 `PARTIAL` · A23 `PASS_WITH_EXPLICIT_CONDITIONS`.**

---

## 10. Returned velocity versus the constrained quantity

The velocity is built by `_regional_gradient` (2h central differences,
one-sided at mask edges); the constraint uses the compact 3-point `L`. **These
are not a discrete gradient/divergence pair.** On the standard fixture:

```
max|div(v_returned)| = 0.040      max|L ψ / a²| = 0.080      ratio = 0.5000
```

Both operators are consistent (`O(h²)`) and converge to the continuum — I
tabulated `N = 4…64`, where the mismatch falls `0.5000 → 0.1464 → 0.0381 →
0.0096 → 0.0024` — so this is a discretisation gap, **not** an equation error.
But no fixture ever refines the *spatial* grid: every scientific result is
computed at `4³`. At that resolution the certified residual `5.55e-17`
certifies `D²ψ = δΘ_d − δΘ_W` for `Lψ/a²`, while the divergence of the
velocity field actually returned differs from it by 100 %.

**Classification: `PARTIAL`.**

---

## 11. Initial data and external-closure semantics (A17, A18, A19, and §18 of the brief)

- Exactly two modes, no default; `initialization_mode=None` is rejected and
  the constructor parameter has no default.
- `SUPPLIED_INITIAL_BOOST` checks off-domain support and the mean-zero
  representative; both rejections verified.
- `EXPANSION_MATCHED_INITIAL_BOOST` performs a genuinely separate elliptic
  solve `Lψ_i = a_i²(δΘ_{d,i} − δΘ_{W,i})` through the frozen gated solver,
  with explicit boundary policy, kernel policy, and zero-mode closure; a
  non-mean-zero source is rejected. Reproduced initial-potential error
  `1.3010426069826053e-18`.
- **`A_W = 0` does not imply `v = 0`**, re-derived independently in closed
  form. With `ψ = 0.002·scalar`, the code's central differences give
  `|∇scalar|_max = √17 = 4.123105625617661`, so
  `v₀ = 0.002√17 = 0.00824621125123532` — identical to the reported value — and
  the potential change over the whole run is exactly `0.0`.
- Geometry/domain compatibility of the supplied potential is checked for
  *support* and *mean*, but **not** for the declared boundary model (§9).

**External-closure semantics.** The public API does achieve the intended
improvement: a full boost *history* is no longer required. The caller supplies
wall geometry (`a_w`, `H_W`, `δΘ_W`, `ν_W`) plus initial data, and the boost
evolution is derived. **The stale Phase 1F-A tokens the brief warned about are
not present**: the final verdict block contains no `BOOST:
REQUIRED_EXTERNAL_CLOSURE_INPUT` and no `LONGITUDINAL_WALL_VELOCITY:
CONDITIONALLY_CLOSED_WITH_EXPLICIT_BOOST_INPUT`; it uses
`LONGITUDINAL_BOOST_RECONSTRUCTION: CONDITIONALLY_DERIVED`,
`WALL_GEOMETRY_DRIVER: REQUIRED_EXTERNAL_CLOSURE_INPUT`, and
`FULL_EXTERNAL_BOOST_HISTORY: NOT_REQUIRED_IN_SELECTED_REALIZATION`. This
concern is **not confirmed**.

**One inert closure field.** `wall_proper_time_rate` is validated (positive,
shape-checked, unit-tagged) and then **never used** — zero references in
`dynamics.py`. Every equation is written in common time `t`. The wall
proper-time mapping is precisely the element that makes a "common spacetime"
non-trivial in Timescape, so a reader may reasonably infer it participates in
the dynamics. It does not.

**A17 `PASS` · A18 `PASS` · A19 `PASS` · external-closure semantics
`PASS_WITH_EXPLICIT_CONDITIONS`.**

---

## 12. Scalar / transverse / harmonic policy (A20, A21)

No transverse field is computed, returned, or named; `requested_sector` admits
one enum value and anything else is rejected; the result record raises unless
`transverse_sector_status == EXCLUDED_BY_EXPLICIT_SCALAR_MODEL_RESTRICTION`
and `transverse_zero_as_timescape_prediction == NOT_GRANTED`. Curl-freeness is
correctly self-classified `CONSTRUCTION_INVARIANT_NOT_INDEPENDENT_NUMERICAL_
EVIDENCE` — a `MODEL_RESTRICTION`, not a Timescape prediction. This is exactly
the right handling.

**Harmonic sector: excluded accidentally, not explicitly.** I computed the
mass-weighted mean of `Dψ` over the wall for two profiles (a periodic mode and
a ramp): `[0, 0, 0]` in both cases. A uniform bulk drift — the constant/harmonic
vector mode on the periodic carrier — is **unrepresentable by any scalar
potential** on this domain. Report §11 is titled "Scalar, transverse, and
harmonic policy" but discusses only the scalar constant kernel; the harmonic
*vector* sector is never mentioned in the report, the inventory, or the code.

**A20 `PASS` · A21 `PARTIAL`.**

---

## 13. Differential-state rank (A24)

Independent DAE accounting of the 1F-B runtime:

| Field | Character |
|---|---|
| `ψ_dw` | **differential** — one ODE `ψ̇ = −Q₀ν`, trapezoidally integrated |
| `δΘ_{d,w}` | elliptically reconstructed upstream (1F-A), consumed as a supplied history |
| `ψ(t_i)` in expansion-matched mode | elliptic, not a DOF |
| `a_w`, `H_W`, `δΘ_W`, `ν_W` | external data, not evolved |
| `v`, `A`, `Lψ` | algebraic/derived diagnostics |

So the 1F-B solver integrates **exactly one** independent differential field.
`FROZEN_DIFFERENTIAL_STATE_RANK: 4` + `ψ` = `5` is a correct *union* accounting
for the selected realization, and no external wall field is secretly evolved,
no elliptic field is miscounted. The report is careful to add that rank 5 "does
not assign rank five to a full vector theory". Worth stating explicitly that
1F-B itself integrates one field and inherits four.

**A24 `PASS`.**

---

## 14. Geometry mutability and integrity (A26, A27)

| Attack | Result |
|---|---|
| ordinary attribute assignment on any frozen record | `FrozenInstanceError` |
| in-place write to any closure array | `ValueError: … read-only` |
| re-enable the write flag (arrays own their data) — **possible** | then write and run → `Phase1FBStateIntegrityError` (SHA-256 fingerprint) |
| `object.__setattr__` substitution of an array/metadata field | `Phase1FBStateIntegrityError` before any residual is evaluated |
| loosen a tolerance on a sealed `ScalarDustWallBoostNumerics` | `Phase1FBStateIntegrityError` |
| flip `inherited_from_h1_density_transmission` after construction | `Phase1FBStateIntegrityError` |
| tamper with a returned result | `Phase1FBStateIntegrityError` |
| stale/mismatched sealed H1 state between expansion history and closure | `Phase1FBContractError` |
| `a_w`/`H_W` mutually inconsistent | `Phase1FBGeometryClosureError` |
| disconnected wall domain | `Phase1FADegeneracyError` (kernel dim 2) |

Integrity does **not** rest on frozen dataclass attributes alone: content
fingerprints catch in-place mutation even after the write flag is restored.

**A26 `PASS` · A27 `PASS`.**

---

## 15. Test and validation-script independence (A28, A29)

| Test | Evidence class | Reason |
|---|---|---|
| `v1` zero driver | `INDEPENDENT_EVIDENCE` | `A_W = 0 ⇒ v ≠ 0` reproduced in closed form (`0.002√17`) |
| `v2` manufactured lapse | `PARTIAL_EVIDENCE` | true oracle `ψ(t)` cubic/linear-`ν`, but the trapezoid is *exact* for a linear `ν`, so the integrator is untested away from exactness |
| `v3` expansion perturbation | `INDEPENDENT_EVIDENCE` | perturbs only the supplied `δΘ_W`; `C_Θ` detects it |
| `v4` reversed sign | `CONSTRUCTION_IDENTITY_ONLY` | fixture sign chosen to match the code; shows sensitivity, not correctness |
| `v5` background `γ_w` | `INDEPENDENT_EVIDENCE` | structural + token rejection |
| `v6`,`v7`,`v9`,`v12` | `INDEPENDENT_EVIDENCE` | contract gates |
| `v8` kernel/Q0 | `PARTIAL_EVIDENCE` | adding a constant to `ν` leaves the projected trajectory unchanged, so the Q0 branch cannot alter the outcome |
| `v10` linear gate | `INDEPENDENT_EVIDENCE` | amplitude raised, gate fires |
| `v11` `a_w²` | `INDEPENDENT_EVIDENCE` | omitted `1/a²` detected; oracle is the closed-form discrete eigenvalue |
| expansion-matched init | `PARTIAL_EVIDENCE` | solve validated against the analytic profile, but with the same manufactured source |
| propagation-residual fail/pass pair | `PARTIAL_EVIDENCE` | demonstrates decoupling; mechanism is truncation only |
| integrity/rank/firewall tests | `INDEPENDENT_EVIDENCE` | contract-level |

**Vacuous-pass sweep.** No test passes because a prior gate intercepts the
input; no residual asserted by a test is zero by construction *without being
labelled as such* except `R_A` (§8) and the automatic `ψ` mean-zero gate (§4).

**Validation script.** Its fixture builder is the same
`wall = dust − lapᵃⁿᵃˡʸᵗⁱᶜ/a²` construction as the tests, so script and tests
share one oracle convention. All twelve `fail_closed` flags reproduce `True`.

**The convergence study re-implements the production integrator.** Lines
409–439 hand-code the *same* trapezoid recursion, feed the result in as
`potential_amplitudes`, and then measure the deviation of the production output
from the closed-form cubic. I reproduced all four values analytically: the
composite-trapezoid error of `∫₀¹0.0006t²dt` is `(h²/12)(f′(1)−f′(0)) = 10⁻⁴h²`,
times `max|scalar| = 1.25` on the wall:

| intervals | closed form | reported |
|---|---|---|
| 4 | `7.8125e-06` | `7.81249999999914e-06` |
| 8 | `1.953125e-06` | `1.953124999999785e-06` |
| 16 | `4.8828125e-07` | `4.882812500001631e-07` |
| 32 | `1.220703125e-07` | `1.2207031250014919e-07` |

The rate `2.0` is therefore analytically guaranteed, and the study verifies
(a) that the production loop equals a re-implementation of itself and (b) a
textbook quadrature error. The report's claim that it "establishes second-order
time-integration convergence" is true but conveys less than it appears to.

**A28 `PARTIAL` · A29 `PARTIAL`.**

---

## 16. Reported numerical metrics (A30)

Every value reproduced. Where possible I recomputed in closed form rather than
by rerunning the script.

| Quantity | Reported | Independently obtained |
|---|---|---|
| Compatibility residual | `5.551115123125783e-17` | identical |
| Propagation residual | `5.204170427930421e-18` | identical (and bit-identical across three unrelated expansion sectors) |
| Maximum velocity ratio | `0.01154469575172945` | identical; **closed form** `amp(1)·√17 = 0.0028 × 4.123105625617661` |
| Expansion-matched initial-potential error | `1.3010426069826053e-18` | identical |
| Expansion-matched compatibility | `1.3877787807814457e-16` | identical |
| `a_w²` conversion residual | `1.0408340855860843e-17` | identical |
| Zero-driver initial velocity | `0.00824621125123532` | identical; **closed form** `0.002√17` |
| Zero-driver potential change | `0` | exactly `0.0` |
| Time-refinement errors | `7.8125e-06 … 1.2207031e-07` | identical; **closed form** `1.25×10⁻⁴h²` |
| Convergence rate | ≈ 2 | exactly 2 by construction |
| Manufactured potential error | `8.673617379884035e-19` | identical |

**A30 `PASS`** — with the caveat that three of these (propagation residual,
convergence errors, potential mean) are analytically determined rather than
measured.

---

## 17. Linear-regime gate (A-linear)

`velocity_ratio = max‖v‖₂ / c` over **all** times and all wall cells, with
`‖·‖₂` the metric-orthonormal Cholesky norm — the correct physical norm
`a^{-2}γ^{ij}D_iψ D_jψ`, not a coordinate-component norm, so a large velocity
cannot hide in the metric. `c` is an explicit required field
(`speed_of_light`, units `REFERENCE_LENGTH_PER_COMMON_TIME`, validated
positive, no default); `unit_system` must be `GEOMETRIZED_C_EQUALS_ONE`. The
threshold is a mandatory scientific input. Violation **raises**
`Phase1FBLinearRegimeError` — no result is returned and no warning path exists,
so the scientific result is invalidated, not annotated. Measured
`0.01154469575172945` against `0.1`.

**`PASS`.**

---

## 18. Observational firewall (A31)

Searched `phase1f_b/`, the 26 tests, the validator, the report, the inventory,
and the artifact keys for `sigma_R`, `sigma8`, `fσ8`, power spectrum, RSD,
Kaiser, tracer/galaxy velocity, observational `k`, dressed Fourier map,
likelihood, fit, physical H1 interface, and autonomous Timescape boost
prediction. Every hit is prohibition prose or the package name
`timescape_fsigma8` inside an import line. `phase1f_b.__all__` contains none of
them. No `ZeroBoostClosure`. No `TIMESCAPE_PREDICTED` provenance value exists.
Public names are appropriately hedged: the field is
`dust_velocity_relative_to_wall`, classified
`CONDITIONAL_SCALAR_LONGITUDINAL_REGIONAL_DUST_VELOCITY_RELATIVE_TO_EXPLICIT_
WALL_OBSERVER_CONGRUENCE`. There is no `wall_velocity`, `physical_velocity`, or
`predicted_velocity` anywhere.

**A31 `PASS` · public API semantics `PASS`.**

---

## 19. Required audit matrix

| ID | Item | Classification |
|---|---|---|
| A01 | Repository preservation | `PASS` |
| A02 | Realization identity | `PASS` |
| A03 | Boost direction/sign | `PASS` (repository evidence `CONSTRUCTION_IDENTITY_ONLY`; independent derivation supplied here) |
| A04 | Common-spacetime requirement | `PASS_WITH_EXPLICIT_CONDITIONS` |
| A05 | Background lapse firewall | `PASS` |
| A06 | Wall perturbative lapse semantics | `PASS` |
| A07 | Regional dust-expansion reconstruction | `PASS` |
| A08 | Laplace–Beltrami operator identity | `PASS` |
| A09 | `a_w²` placement | `PASS` |
| A10 | Dimensional consistency | `PASS_WITH_EXPLICIT_CONDITIONS` |
| A11 | Kernel / zero-mode handling | `PASS_WITH_EXPLICIT_CONDITIONS` |
| A12 | Scalar propagation equation | `PASS` |
| A13 | Time-derivative convention | `PASS` |
| A14 | Expansion compatibility residual | `PASS` |
| A15 | Propagation/geodesic residual | `PASS` (as a discretisation diagnostic only) |
| A16 | Residual independence | `PARTIAL` + `SOURCE_MISREPRESENTED` |
| A17 | Supplied-initial-boost branch | `PASS` |
| A18 | Expansion-matched branch | `PASS` |
| A19 | Zero-boost-default firewall | `PASS` |
| A20 | Scalar/transverse distinction | `PASS` |
| A21 | Harmonic-mode policy | `PARTIAL` |
| A22 | Interface-condition firewall | `PARTIAL` |
| A23 | Wall-interior/global-domain semantics | `PASS_WITH_EXPLICIT_CONDITIONS` |
| A24 | Differential-state rank | `PASS` |
| A25 | Conditional uniqueness / frozen regression | `PASS` |
| A26 | Geometry mutability/integrity | `PASS` |
| A27 | Fail-closed API behaviour | `PASS` |
| A28 | Tests independent versus tautological | `PARTIAL` |
| A29 | Validation-script independence | `PARTIAL` |
| A30 | Reported numerical metrics | `PASS` |
| A31 | Observational firewall | `PASS` |
| A32 | Final verdict-token consistency | `PASS_WITH_EXPLICIT_CONDITIONS` |

Counts: `PASS` 21 · `PASS_WITH_EXPLICIT_CONDITIONS` 6 · `PARTIAL` 5 ·
`UNSUPPORTED` 0 · `INCORRECT` 0 · `SOURCE_MISREPRESENTED` 1 (co-classified with
A16) · `NOT_APPLICABLE` 0.

---

## 20. Adjudication of final tokens (A32)

| Token | Value | Adjudication |
|---|---|---|
| `SCIENTIFIC_REALIZATION_READINESS` | `IMPLEMENTED_CONDITIONALLY` | `CONFIRMED` |
| `PHASE_1F_B_SCIENTIFIC_VERDICT` | `PARTIAL_CLOSURE_NEW_GEOMETRIC_DYNAMICS_REQUIRED` | `CONFIRMED` |
| `COMMON_SPACETIME_FRAME_CLOSURE` | `REQUIRED_EXTERNAL_GEOMETRIC_COMPLETION` | `CONFIRMED` |
| `DUST_TO_WALL_BOOST_PROPAGATION` | `CONDITIONALLY_DERIVED` | `CONFIRMED` |
| `DUST_TO_WALL_BOOST_FROM_Y_ALONE` | `NOT_DERIVED` | `CONFIRMED` |
| `EXPANSION_DIFFERENCE_CONSTRAINT` | `CONDITIONALLY_DERIVED` | `CONFIRMED` |
| `LONGITUDINAL_BOOST_RECONSTRUCTION` | `CONDITIONALLY_DERIVED` | `CONFIRMED` |
| `TRANSVERSE_BOOST` | `NONIDENTIFIABLE_FROM_FROZEN_SCALAR_STATE` | `CONFIRMED` |
| `BACKGROUND_WALL_LAPSE_TO_BOOST` | `NOT_DERIVABLE` | `CONFIRMED` (structurally unreachable) |
| `FULL_EXTERNAL_BOOST_HISTORY` | `NOT_REQUIRED_IN_SELECTED_REALIZATION` | `CONFIRMED` |
| `WALL_GEOMETRY_DRIVER` | `REQUIRED_EXTERNAL_CLOSURE_INPUT` | `CONFIRMED` |
| `INITIAL_BOOST_DATA` | `REQUIRED_OR_EXPLICITLY_ELLIPTICALLY_RECONSTRUCTED` | `CONFIRMED` |
| `BOOST_INTERFACE_CONDITIONS` | `NOT_DERIVED` | `NEEDS_REWORDING` — accurate that nothing is *derived*, but the runtime **imposes** a no-penetration condition through the reused operator, and does not enforce it on supplied data |
| `FROZEN_DIFFERENTIAL_STATE_RANK` | `4` | `CONFIRMED` |
| `SELECTED_SCALAR_REALIZATION_DIFFERENTIAL_STATE_RANK` | `5` | `CONFIRMED` (1F-B itself integrates one field and inherits four) |
| `CONDITIONAL_FORWARD_UNIQUENESS` | `GRANTED` | `CONFIRMED` |
| `UNIQUE_FROM_FROZEN_Y_ALONE` | `NOT_GRANTED` | `CONFIRMED` |
| `UNIQUE_TIMESCAPE_PREDICTION` | `NOT_GRANTED` | `CONFIRMED` |
| `PHYSICAL_INTERFACE_CLAIM` | `NOT_GRANTED` | `CONFIRMED` |
| `OBSERVATIONAL_AUTHORIZATION` | `NOT_GRANTED` | `CONFIRMED` |
| `RSD_AUTHORIZATION` | `NOT_GRANTED` | `CONFIRMED` |
| `SIGMA8_AUTHORIZATION` | `NOT_GRANTED` | `CONFIRMED` |
| `FSIGMA8_AUTHORIZATION` | `NOT_GRANTED` | `CONFIRMED` |
| `residuals/propagation_geodesic/independent_of_expansion_compatibility` | `True` | `NEEDS_REWORDING` — literally true, but `R_A` is a construction identity carrying no evidence about the physics |
| Suspected stale 1F-A tokens (`BOOST: REQUIRED_EXTERNAL_CLOSURE_INPUT`, `LONGITUDINAL_WALL_VELOCITY: CONDITIONALLY_CLOSED_WITH_EXPLICIT_BOOST_INPUT`) | — | **NOT PRESENT** in the 1F-B report or inventory; the concern is not confirmed |

---

## A. FINAL AUDIT VERDICT

```text
TARGETED_CORRECTIONS_REQUIRED
```

The implemented realization survives adversarial scrutiny. The frame sign, the
operator identity `L_w = a_w²D_w² = Δ_{γ_w}`, the `a_w²` placement, the
propagation law `ψ̇ = −Q₀ν_W`, the kernel handling, the background-lapse
firewall, the observational firewall, fail-closed behaviour, state integrity,
and the frozen-phase boundary are all independently confirmed. Every reported
number reproduces exactly, several in closed form, on two different numerical
stacks. No blocking scientific defect was found. The required corrections are
evidence-classification and boundary-enforcement issues local to the reports,
one runtime gate, and the fixture design.

## B. BLOCKING SCIENTIFIC FINDINGS

None. Specifically ruled out by independent derivation and experiment: wrong
boost sign; wrong operator normalization; boost reconstructed from the
background Timescape lapse; a full vector claimed from scalar data; a physical
interface silently assumed; H1 density-transmission boundary conditions
silently inherited; and validation so circular that the core equations retain
no evidence (`C_Θ`, the `a_w²` rejection test, and the closed-form fixtures do
leave real evidence).

## C. TARGETED CORRECTIONS IF ANY

1. **Reclassify `R_A`.** It is a construction identity: with `v := Dψ`,
   `A := Dν`, `ψ̇ = −ν`, the residual `A + v̇ + Hv ≡ 0` in the continuum. It is
   bit-identical across three unrelated expansion sectors and machine-zero for
   arbitrary lapse histories at constant `a`, `H = 0`. Give it the label the
   project already applies to the curl —
   `CONSTRUCTION_INVARIANT_NOT_INDEPENDENT_NUMERICAL_EVIDENCE`, qualified as a
   *time-discretisation consistency diagnostic* — in report §15 and in
   `residuals/propagation_geodesic` of the inventory.
2. **Gate the declared boost boundary on the supplied data.** Add a fail-closed
   check that `D_nψ|_Γ` is within tolerance of zero (or explicitly document
   that `BOOST_WALL_INTERIOR_NO_FLUX_PERIODIC_TANGENTIAL` constrains only the
   operator). Today a supplied `ψ` with a normal jump across Γ is accepted and
   returns `|v_normal| = 0.016` while `C_Θ` is evaluated with an operator whose
   natural condition asserts zero normal flux.
3. **State the interface model in physical terms.** Report §12 should say
   plainly that the selected boundary model **is** a no-penetration condition
   on the dust-to-wall relative velocity at Γ — declared, not derived — rather
   than only that no such condition follows from H1.
4. **Add at least one fixture that varies along the interface normal.** Every
   current test and validator field is exactly constant along axis 0, so
   `|v_normal| = 0.0` identically and the broken operator agrees with the
   unbroken periodic Laplacian to `3.55e-15`. The phase's core new modeling
   choice currently has zero numerical evidence.
5. **Restate the convergence study's scope.** It re-implements the production
   trapezoid recursion and then measures a closed-form quadrature error
   (`1.25×10⁻⁴h²`, reproduced analytically for all four points). Report §19
   should say it verifies the integrator's implementation and a textbook
   truncation law, not the scientific content.
6. **Disclose the `wall_proper_time_rate` field as inert**, or consume it. It
   is validated and never used; all dynamics are in common time.
7. **Declare the shear-free background assumption.** `shear` appears nowhere in
   the package, report, or inventory, yet `v̇ + Hv = −A` requires it.
8. **Address the harmonic vector sector** in report §11, which is titled
   "…and harmonic policy" but covers only the scalar constant kernel. A uniform
   bulk drift is unrepresentable by any `Dψ` on this domain (mass-weighted mean
   of `Dψ` is exactly zero) — a `MODEL_RESTRICTION`, not a prediction.

## D. NON-BLOCKING FINDINGS

- At the only validated resolution (`4³`), `div(v_returned)` and the constrained
  `Lψ/a²` differ by exactly a factor 2, because the 2h-central gradient and the
  compact 3-point Laplacian are not a discrete grad/div pair. Both are `O(h²)`
  consistent (mismatch falls `0.500 → 0.146 → 0.038 → 0.010 → 0.002` for
  `N = 4…64`), so this vanishes on refinement — but no fixture refines the
  spatial grid.
- The `ψ` mean-zero gate (`1.6e-19`) is automatic whenever `ν` is mean-zero,
  since `a³` cancels in the weighted mean; it is not an independent check.
- `test_v2` and the validator's manufactured case use a *linear* `ν`, for which
  the trapezoid rule is exact; the integrator is never tested where it is
  inexact except through the closed-form convergence study.
- `test_v8`'s Q0 branch adds a spatial constant to `ν`, which the projection
  removes exactly, so the branch cannot change the trajectory.
- The inventory's `selected_sector[5] = WALL_INTERIOR_OR_EXPLICIT_BOUNDARY` is
  vaguer than the runtime, which admits only `domain_id == "wall"`.
- `dynamics.py`'s docstring writes the frame law as `Θ_W = Θ_d + D_aξ^a`, which
  is consistent only under `ξ = −v`; a reader checking the sign against that
  line will conclude the opposite of what the code does.
- A 270-line `CLAUDE.md` documentation rewrite rides inside the scientific
  commit. Its content and hash are correct and it is disclosed and classified,
  but mixing it into a scientific commit is not ideal.

## E. VERIFIED SCIENTIFIC CLAIMS

- `D_a v^a_{d|W} = δΘ_{d,w} − δΘ_W` — re-derived from first principles and
  confirmed against an independent physical counterexample (converging dust
  ⇒ smaller dust expansion).
- `L_w = a_w²D_w² = Δ_{γ_w}` and `D²ψ = Lψ/a²` — confirmed from the frozen 1E-G
  metric semantics and by an independent `a`-scaling experiment.
- `ψ̇ = −Q₀ν_W` follows from `v̇ + H_Wv = −A_W` with `v = Dψ`, `A = Dν`;
  correct sign, correct single `H` factor, FLRW commutator valid on the
  enforced geometry class.
- Disconnected wall domains fail closed at kernel dimension 2.
- The background Timescape lapse `γ_w` is structurally unreachable.
- `A_W = 0` does not imply `v = 0`: `v₀ = 0.002√17 = 0.00824621125123532`,
  potential change exactly `0`.
- All twelve `fail_closed` gates reproduce `True`; every mutation and
  stale-reference attack fails closed.
- No frozen Phase 1E-F/1E-G/1F-A scientific result was weakened; the commit is
  additive outside `CLAUDE.md`.
- 565 passed on Python 3.14.3 and 3.11.9, zero failures, skips, xfails,
  warnings; artifact byte-identical across both stacks.
- Every reported numerical metric reproduced exactly.

## F. CLAIMS REQUIRING REWORDING

- Report §15 and inventory `residuals/propagation_geodesic`: `R_A` described as
  "independently evaluated … independently of `C_Θ`" and
  `independent_of_expansion_compatibility = True`. Literally true, evidentially
  misleading — `R_A` is a construction identity.
- Report §12 / token `BOOST_INTERFACE_CONDITIONS: NOT_DERIVED`: correct that
  nothing is derived, silent that a no-penetration condition is imposed and
  unenforced on data.
- Report §19: "establishes second-order time-integration convergence" — it
  establishes a closed-form quadrature law against a re-implementation of the
  same recursion.
- Report §11 "…and harmonic policy" — the harmonic vector sector is not
  discussed.
- Report §6 lists "the positive wall proper-time rate" among the closure's
  bindings without noting it never enters the dynamics.

## G. EXACT MINIMAL FOLLOW-UP TASK

On the existing branch, without amending commit
`27fd65fd2a05c5b990508d948703897f433b566e` and without moving or recreating tag
`phase-1f-b-dust-wall-boost-dynamics-v1`, land **one** follow-up commit that:

1. edits `reports/phase1f_b_dust_wall_boost_dynamics_validation.md` §§11, 12,
   15, 19 and the `residuals/propagation_geodesic`, `boundary_and_interface`
   entries of `reports/phase1f_b_dust_wall_boost_dynamics_inventory.json` to
   apply corrections C1, C3, C5, C6, C7, C8 (evidence reclassification and
   disclosure only — no equation, tolerance, closure, or authorization changes);
2. adds a fail-closed `D_nψ|_Γ` gate for supplied initial potentials (C2) with
   its tolerance declared in `ScalarDustWallBoostNumerics`; and
3. adds one test fixture whose scalar profile varies along the interface normal,
   exercising that gate and the no-flux operator (C4).

Then freeze as `phase-1f-b-dust-wall-boost-dynamics-v2`, matching the
`1e-f v1→v2`, `1e-g v1→v4`, and `1f-a v1→v2` precedent.

```text
READY_FOR_STRICT_FAST_FORWARD_INTEGRATION:
NO
```
