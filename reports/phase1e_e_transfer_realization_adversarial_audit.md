# Independent adversarial audit — Phase 1E-E transfer-realization selection

## 1. Audit verdict

**Audit verdict: `REQUIRES_TARGETED_CORRECTIONS`.**

The two Phase 1E-E deliverables preserve the principal negative boundary of
Phase 1E-D: current Timescape machinery still does not provide a complete
common spatial carrier, regional-to-GM transfer, effective-sector transfer,
compatibility propagation theorem, or implementation-ready forward problem.
The regional nonzero-mode scalar dust sector remains correctly frozen as a
rank-two first-order system per exact regional FLRW geometry, the three named
mismatch blocks remain distinct from their unknown operator rank, and the
observational and implementation firewalls are intact.

The deliverables are nevertheless **not safe to accept unchanged**. The main
blocking issues are:

1. the selected S1 scalarization operator is written as
   \(L_C=-D_C^2\), whereas the frozen CGI scalars use an operator of the form
   \(L_r=a_r^2D_r^2\); the carrier sign, dimensions, normalization, and relation
   to the regional operators are therefore not fixed;
2. S1 assigns universal regional spaces \(L^2_0(\Sigma_r)\) and
   \(H^2_0(\Sigma_r)\) without selecting regional topology, boundary, decay,
   or full elliptic kernels, so its regional Green operators are not yet
   defined;
3. consequently, the S1 verdicts for G2 and G4 and the entry
   \(\Delta_{\rm BC}=\texttt{NOT_APPLICABLE}\) are too strong;
4. fixing the reference partition and embeddings does not close temporal
   transport of the evolving metric, measure, projectors, domains, and Green
   operators, so G5 is also too strong;
5. the frozen clean-comoving constitutive residual
   \(C_P=\mathscr W-3\mathscr Q\) and its exact \(+C_P/4\) forcing in the
   \(C_Z\) equation were omitted and \(C_P\) was misclassified as a generic
   optional model extension;
6. \(Q_CL_C\) is redundant on the stated compact boundaryless \(H^2\) branch,
   so the selected ZM-S2 output projection is not the load-bearing zero-mode
   decision claimed in the packet;
7. the claim that S1 is the *derived* minimum-extension architecture is a
   selection convention, not a result derivable from verified equations;
8. the Markdown contains corrupted TeX/control characters in the commutator,
   M1, and L1 sections.

The primary selection does **not** have to be reopened at this stage. S1 may
survive as a **provisional, author-selected baseline architecture**, with H1
retained as the mandatory sharp comparator. It may not retain its current
scientific gate scores or the classification that its preference over H1 is a
verified derivation.

Implementation readiness remains:

```text
REPORT_ONLY_MUST_CONTINUE
```

Implementation authorization remains:

```text
NOT_GRANTED
```

---

## 2. Scope and independence

This audit was performed against local immutable copies of:

- `phase1e_e_transfer_realization_selection.md`;
- `phase1e_e_transfer_realization_inventory.json`;
- the supplied Phase 1E-A through Phase 1E-D reports and inventories.

The audited files were treated as claims, not as authority. Load-bearing
claims were compared with the frozen Phase 1E-D closure and inventory, and the
relevant operator statements were rederived independently.

This environment is not the user's Git checkout. The audit therefore does not
claim to have verified branch, HEAD, tags, worktree status, repository tests,
or remote refs. No audited file was modified.

---

## 3. Audited artifacts

| Artifact | SHA-256 before audit |
|---|---|
| `phase1e_e_transfer_realization_selection.md` | `6c1f2caac8a7749878e4afe505c61430754cf4fd5048c92f965f7714589ec688` |
| `phase1e_e_transfer_realization_inventory.json` | `8d027addd7604602a878951162c6079915636c7e168d868b6e9cdb19f04893e4` |

Primary frozen comparison sources:

| Source | SHA-256 |
|---|---|
| Phase 1E-D closure | `db2e43a9446334a31ba3c6a65b0800e0b98395ea236c278684415399e271c62e` |
| Phase 1E-D adversarial audit | `f390f1c93384ed1fb73aaf6fed3146a407a0bdb6a24d502374ddcfb704196337` |
| Phase 1E-D inventory | `b27e6f495c8524e8f5cfc3383b307772e7933ee7a0bd66f36bba807024ad1cc4` |
| Phase 1E-C closure | `522a77de97d06c90323d06f597f4e2b1be168da9fa7efd3965f29268e085c4e4` |
| Phase 1E-B derivation | `9ef5ff401a70d533071e75b33726b2fd40ed1fffb9d90c4aa26e3603f1ae8444` |
| Phase 1E-A audit | `760dba223e3f9aaafd35b9b33208c114df7319581db1f55fda211fc89a3dc926` |

---

## 4. Automated structural checks

| Check | Result |
|---|---|
| JSON parses | `PASS` |
| Top-level JSON block count | `PASS` — 40 blocks |
| Realization packet count | `PASS` — 5 packets |
| Gate completeness | `PASS` — G0–G15 present for each packet |
| Formal-conclusion count | `PASS` — 20 |
| Exactly nine formal-conclusion fields | `PASS` |
| Allowed gate vocabulary | `PASS` |
| Duplicate stable IDs | `PASS` |
| Cross-file final verdicts | `PASS` |
| Markdown numbered sections 1–46 | `PASS` |
| Markdown control-character scan | `FAIL` |
| Exact cumulative decision records | `PARTIAL` — phase summaries rather than the full ledger |
| True repository preflight | `NOT_APPLICABLE_IN_THIS_ENVIRONMENT` |

The Markdown contains one ASCII bell character and four carriage-return bytes
inside TeX strings. It also splits `\neq`, `\rm`, and `\alpha` sequences into
invalid text.

---

## 5. Classification counts

The audit contains 34 classified findings.

| Classification | Count |
|---|---:|
| `PASS` | 10 |
| `PASS_WITH_EXPLICIT_CONDITIONS` | 8 |
| `PARTIAL` | 6 |
| `UNSUPPORTED` | 3 |
| `INCORRECT` | 7 |

No primary source was found to be falsely quoted by bibliographic identity,
but several source-derived classifications and consequences were too strong.

---

## 6. Detailed findings

### A01 — Artifact scope and repository limitation

**Classification: `PASS`.**

The report clearly states that it was produced outside the user's real Git
checkout and does not falsely claim a live Git preflight, test run, commit,
tag, or push.

### A02 — JSON deterministic structure

**Classification: `PASS`.**

The inventory parses, uses stable top-level blocks, includes all five packet
records, and preserves explicit unknown-rank tokens rather than inventing
numeric zeros.

### A03 — Cross-file verdict consistency

**Classification: `PASS`.**

Markdown and JSON agree on:

```text
PRIMARY_REALIZATION_CLASS_SELECTED_CONDITIONALLY
PARTIAL_REALIZATION_DEFICITS_REMAIN
NEW_DYNAMICS_REQUIRED
REPORT_ONLY_MUST_CONTINUE
NOT_GRANTED
```

### A04 — Regional rank-two bulk

**Classification: `PASS`.**

The report correctly preserves, for each regional exact FLRW dust geometry,

\[
\frac{d\Delta_r}{d\tau_r}=-Z_r,
\qquad
\frac{dZ_r}{d\tau_r}
=-2H_rZ_r-4\pi G\rho_r\Delta_r,
\]

and correctly treats the wall-plus-void bulk rank as four. It does not use the
heuristic metric count as an independent proof.

### A05 — Present Timescape carrier no-go boundary

**Classification: `PASS`.**

The deliverables correctly preserve that current Timescape sources do not
construct the complete three-dimensional common carrier and regional-to-GM
transfer.

### A06 — R1–R8 heterogeneous-layer taxonomy

**Classification: `PASS_WITH_EXPLICIT_CONDITIONS`.**

Treating R1–R8 as carrier, formulation, operator, scale, and target layers is a
useful design taxonomy. It is a Phase 1E-E organizing convention, not a
primary-source theorem, and should remain classified accordingly.

### A07 — Positivity of the convex metric blend

**Classification: `PASS_WITH_EXPLICIT_CONDITIONS`.**

For nonnegative \(\chi_w,\chi_v\) with \(\chi_w+\chi_v=1\), and positive
definite metrics \(\widetilde h_w,\widetilde h_v\) on the **same tangent
space**, one has for any nonzero vector \(v\):

\[
h_C(v,v)
=\chi_w\widetilde h_w(v,v)
+\chi_v\widetilde h_v(v,v)>0.
\]

This proves pointwise positivity only after both global extension metrics
exist. It does not prove existence, regularity, uniqueness, naturality, or
regional restriction properties of the extensions.

### A08 — Existence of the required global metric extensions

**Classification: `UNSUPPORTED`.**

The packet requires operators \(E_r^{(h)}\) that extend regional metrics to a
single compact carrier, but does not specify whether the regional objects are
whole complete FLRW slices or finite patches, their topology, compatibility
on overlap, or extension regularity. Positivity of a blend does not establish
that these extensions exist with the required pullback properties.

Required correction: change the S1 carrier metric from a selected construction
to a **conditional template**, and specify regional finite domains or an
extension theorem before G1 can pass beyond class level.

### A09 — Carrier scalarization sign and dimensional normalization

**Classification: `INCORRECT`.**

The frozen CGI definitions use operators of the form

\[
L_r=a_r^2D_r^2,
\]

whereas S1 records

\[
L_C=-D_C^2.
\]

The report does not define whether \(h_C\) is physical or comoving, does not
supply a carrier length/scale normalization, and does not reconcile the sign
convention with \(L_r\). Thus the displayed map

\[
T_r^{(a)}=Q_CL_CM_{\chi_r}E_r\mathcal U_rG_rQ_r
\]

has no demonstrated units or source-identity preservation.

Required correction: introduce an explicitly normalized carrier scalarization
operator \(\mathcal L_C\), with declared sign and dimensions, and require an
intertwining or dimensional-consistency audit against each \(L_r\). Do not
identify it with \(-D_C^2\) by default.

### A10 — Regional Green domains

**Classification: `INCORRECT`.**

The inventory assigns every region

```text
L2_0(Sigma_r) -> H2_0(Sigma_r)
```

without selecting whether \(\Sigma_r\) is compact, noncompact, a finite
regional patch, or a domain with boundary. Mean-zero projection removes only
the constant kernel in a compact connected branch; it does not supply decay,
boundary conditions, transmission data, zero-resonance control, or the full
elliptic kernel in other branches.

This contradicts the frozen Phase 1E-D requirement that the regional Green
operator be defined only after topology, domain, full kernel, boundary/decay
conditions, and functional spaces are fixed.

### A11 — Ambiguous use of `H2_0`

**Classification: `PARTIAL`.**

The report appears to use \(H^2_0\) to mean “mean-zero \(H^2\).” Standard PDE
notation often uses \(H^2_0\) for the closure of compactly supported smooth
functions, which can encode boundary traces rather than a zero spatial mean.

Required correction: use an unambiguous notation such as

\[
H^2_{\perp 0}(\Sigma)
:=H^2(\Sigma)\cap L^2_0(\Sigma),
\]

and separately name any Dirichlet closure space.

### A12 — S1 G2 verdict

**Classification: `INCORRECT`.**

Because the regional topology and elliptic realization are not selected, S1
cannot currently receive

```text
G2 = PASS_UNDER_EXPLICIT_ASSUMPTIONS
```

for its complete functional package. A defensible replacement is:

```text
G2 = DEFINED_BUT_UNDERDETERMINED
```

or a split verdict:

```text
G2_CARRIER = PASS_UNDER_EXPLICIT_ASSUMPTIONS
G2_REGIONAL_GREEN = FAIL_NOT_DEFINED
```

### A13 — S1 G4 verdict

**Classification: `INCORRECT`.**

Mean-zero compatibility is sufficient only for the specifically selected
compact connected boundaryless elliptic branch, after regularity and operator
normalization are fixed. It is not sufficient for the unselected regional
operators. Therefore

```text
G4 = PASS_UNDER_MEAN_ZERO_ASSUMPTIONS
```

is too strong for the complete S1 composition.

Recommended replacement:

```text
G4 = DEFINED_BUT_UNDERDETERMINED
```

### A14 — S1 boundary deficit

**Classification: `INCORRECT`.**

The packet records

```text
Delta_BC = NOT_APPLICABLE
```

because the carrier is boundaryless. This ignores regional inverse-Laplacian
boundary or decay data and extension/overlap trace data. A boundaryless carrier
does not eliminate elliptic boundary/asymptotic choices in the regional
sectors.

Recommended replacement:

```text
Delta_BC = BIFURCATED
```

with a note that *carrier outer boundary* is not applicable but regional
elliptic boundary/decay data remain unresolved.

### A15 — Output zero-mode projector

**Classification: `PARTIAL`.**

For a compact boundaryless carrier and \(\psi\in H^2(\Sigma_C)\),

\[
\int_{\Sigma_C}(-D_C^2\psi)\,d\mu_C=0.
\]

Hence on the stated domain:

\[
Q_CL_C=L_C.
\]

The ZM-S2 projector placed **after** the carrier Laplacian is therefore
redundant, not a load-bearing branch choice. The load-bearing decisions are the
regional inverse kernels and any projection before an inverse or separate
homogeneous target sector.

Required correction: either remove \(Q_C\) from the output factorization and
retain it as a range check, or move the zero-mode policy to the source of an
actual carrier inverse problem.

### A16 — Smooth commutator policy

**Classification: `PASS_WITH_EXPLICIT_CONDITIONS`.**

For \(L_C=-D_C^2\),

\[
[L_C,M_\chi]u
=-(D_C^2\chi)u-2D^i\chi D_i u,
\]

up to the declared sign convention. The report correctly rejects automatic
commutation, although the Markdown rendering of `\neq 0` is corrupted.

### A17 — Lagrangian partition law

**Classification: `PASS_WITH_EXPLICIT_CONDITIONS`.**

The assumption \(\partial_{t_C}\chi_r=0\) in reference coordinates preserves
\(\chi_w+\chi_v=1\) and positivity, and reduces an arbitrary all-time
partition history to initial structural data plus an explicit law. It remains
an optional kinematic model extension, not a Timescape derivation.

### A18 — Volume-fraction consistency

**Classification: `PASS_WITH_EXPLICIT_CONDITIONS`.**

The condition

\[
K_f(t)=
\frac{\int\chi_v\,d\mu_C(t)}{\int d\mu_C(t)}-f_v^{\rm TS}(t)=0
\]

is a valid required consistency test. The report correctly treats it as a
condition, but the selection does not derive or propagate it. G6 should not be
interpreted as proving physical volume closure.

### A19 — Temporal transport and S1 G5

**Classification: `INCORRECT`.**

Fixing \(\chi_r\) and reference embeddings does not define temporal transport
for:

- \(h_C(t)\) and \(d\mu_C(t)\);
- the Hilbert/Sobolev norms;
- \(Q_C(t)\);
- \(L_C(t)\);
- \(G_r(t)\);
- their domains and adjoints.

The P3–P5 design explicitly required a fixed-reference trivialization,
Hilbert-bundle connection, or equivalent transport before \(\dot T\) is
well-defined. Therefore

```text
G5 = PASS_UNDER_LAGRANGIAN_RESTRICTION
```

is too strong.

Recommended replacement:

```text
G5 = DEFINED_BUT_UNDERDETERMINED
```

### A20 — Homogeneous regional clocks

**Classification: `PASS_WITH_EXPLICIT_CONDITIONS`.**

Using positive homogeneous maps \(\tau_r(t_D)\) as a background
reparameterization is admissible as a selected restriction. It does not provide
a perturbative lapse, boost, tilt, or spatial clock map. The report preserves
that exclusion.

The inventory should, however, describe the clock maps as
`KINEMATICALLY_DEFINED / SELECTED_CONDITIONALLY`, rather than implying that the
complete regional-to-carrier clock package is already background-defined
current machinery.

### A21 — Frozen constitutive residual \(C_P\)

**Classification: `INCORRECT`.**

The Phase 1E-D clean-comoving branch defines

\[
C_P=\mathscr W-3\mathscr Q
\]

and requires \(C_P(t)=0\) for all time. It is an **enforced constitutive
closure**, not a fourth mismatch state and not merely an arbitrary optional
model extension.

The new report omits the exact definition and classifies `OBJ-COMP-P` as
`OPTIONAL_MODEL_EXTENSION / NOT_DEFINED_IN_CURRENT_THEORY`. This loses a frozen
branch result. The *regional reconstruction* needed to evaluate \(C_P\) is
missing, but the target closure itself is already fixed in the clean-comoving
branch.

Required correction: restore the exact definition, classify the target closure
as inherited/required by the selected GM branch, and separately identify the
missing regional reconstruction or dynamics.

### A22 — Exact mismatch propagation

**Classification: `PARTIAL`.**

The generic matrix equation

\[
\dot{\boldsymbol C}=M_C\boldsymbol C+B_PC_P-\boldsymbol R_T
\]

is structurally sound, and the density equation

\[
\dot C_\Delta=-C_Z-R_\Delta
\]

is retained. The report should also preserve the frozen exact branch equations:

\[
\dot C_{\rm eff}
=w\Theta C_{\rm eff}-(1+w)C_Z-R_{\rm eff},
\]

\[
\dot C_Z
=-\frac23\Theta C_Z
-4\pi G\rho_dC_\Delta
-4\pi G\rho_{\rm eff}C_{\rm eff}
+\frac14C_P-R_Z.
\]

Their omission weakens the equation-level audit and hides the exact role of
\(C_P\).

### A23 — Effective-density mismatch

**Classification: `PASS`.**

The report consistently retains \(C_{\rm eff}\) as a load-bearing third named
mismatch block and does not infer rank three from the number of components.

### A24 — Constraint-intertwining condition

**Classification: `PASS_WITH_EXPLICIT_CONDITIONS`.**

The abstract condition

\[
\mathcal K_{\rm GM}T=S_K\mathcal K_{\rm reg}
\]

is an appropriate necessary template for constraint preservation. No concrete
operator proof is claimed, so G8 correctly remains underdetermined.

### A25 — Forward well-posedness

**Classification: `PASS`.**

The report correctly distinguishes snapshot definability, externally driven
forward evolution, and predictively closed well-posedness. It does not claim
existence, uniqueness, or continuous dependence for S1 or H1.

### A26 — Inverse status

**Classification: `PASS`.**

The report correctly keeps S1 and fixed-interface H1 inverse uniqueness
unresolved and distinguishes exact injectivity from stable inversion.

### A27 — Finite moment information loss

**Classification: `PASS`.**

Under the stated assumption of an infinite-dimensional parent field space, a
finite linear map to \(\mathbb R^N\) has a nontrivial kernel. M1 is correctly
restricted to a reduced target.

### A28 — Finite spectral truncation

**Classification: `PASS`.**

A finite truncation is noninjective as a full-field map because omitted modes
lie in its kernel. The report correctly rejects a full-field inverse claim.

### A29 — H1 source-free transmission comparator

**Classification: `PASS_WITH_EXPLICIT_CONDITIONS`.**

Selecting continuous reconstructed potential, continuous conormal flux, and
zero surface source is a mathematically recognizable comparator branch. It is
correctly labeled a falsifiable imported assumption and not a Timescape
junction derivation.

### A30 — S1 “minimum-extension” selection

**Classification: `UNSUPPORTED`.**

The statement that S1 has the least unsupported physical burden is not a
consequence of verified equations. The criteria SC-1–SC-10 have no weighting,
partial order, or proof that smooth partition data are less substantive than
sharp interface data. S1 also introduces a compact global topology class,
metric extensions, overlap interpolation, and a partition profile.

S1 may be retained as the author's provisional baseline, but formal conclusion
FC-1E-E-004 should be classified `CONVENTION_DEPENDENT` or
`REQUIRES_AUTHOR_INPUT`, not `DERIVED_FROM_VERIFIED_DEFINITIONS`.

### A31 — H1 mandatory-comparator status

**Classification: `PARTIAL`.**

Retaining H1 as an adversarial comparator is scientifically prudent, but
“mandatory” is a project governance decision. FC-1E-E-006 should use
`CONVENTION_DEPENDENT`, not a derived-evidence token.

### A32 — Target naming

**Classification: `UNSUPPORTED`.**

S1 is labeled `GLOBAL_THEORETICAL_GM_SCALAR_FIELD`, although the report also
states that \(\mathcal T_{\rm eff}\), source-identity preservation, constraint
intertwining, and compatibility propagation are unresolved. The output is
therefore more accurately a **candidate carrier scalar representation intended
for the GM target**, not yet a demonstrated GM scalar field.

Required correction: downgrade the target token until G8 and the effective
sector are closed.

### A33 — Evidence classifications in formal conclusions

**Classification: `PARTIAL`.**

Most formal conclusions use defensible evidence labels. At least the following
must change:

- FC-1E-E-004: `DERIVED_FROM_VERIFIED_DEFINITIONS` → `CONVENTION_DEPENDENT` or
  `REQUIRES_AUTHOR_INPUT`;
- FC-1E-E-006: same correction;
- FC-1E-E-020 is an authorization/governance statement, not a scientific
  derivation, and should be `NOT_APPLICABLE` or moved outside
  `formal_conclusions`.

FC-1E-E-009 should be `SYMBOLICALLY_VERIFIED` if the map is explicitly defined
to depend only on background inputs.

### A34 — Markdown and ledger quality

**Classification: `PARTIAL`.**

The Markdown contains corrupted TeX/control characters:

- `\neq 0` is split into a newline plus `eq0`;
- `\Delta_{\rm eff}` is split by carriage return;
- `U_\alpha` contains an ASCII bell;
- `\epsilon_{\rm WKB}`, `\lambda_{\rm local}`, and `L_{\rm carrier}` contain
  carriage returns.

The decision ledger is transparent about incomplete P0/P2 reconstruction, but
it stores phase summaries rather than the full P0–P8 decisions promised by the
specification. This is acceptable only as an explicitly incomplete artifact,
not as a complete frozen ledger.

---

## 7. Required blocking corrections

The following corrections are required before acceptance.

### C1 — Replace the carrier scalarization operator

Replace the unqualified

\[
L_C=-D_C^2
\]

with a declared operator \(\mathcal L_C\) that specifies:

- sign convention;
- physical or comoving metric convention;
- dimensional normalization or carrier length scale;
- domain and codomain;
- relation to \(L_r=a_r^2D_r^2\);
- source-identity implications.

The report may retain \(-D_C^2\) only as one conditional subbranch after these
choices are explicit.

### C2 — Reopen the regional elliptic branch inside S1

Do not assign universal \(L^2_0/H^2_0\) regional Green spaces. Select or branch
between:

- compact boundaryless regional spaces;
- finite regional patches with BC;
- noncompact weighted spaces with decay;
- another explicit elliptic realization.

Define the full kernel, not only constants.

### C3 — Correct S1 gates and deficits

At minimum, change:

```text
G2: PASS_UNDER_EXPLICIT_ASSUMPTIONS
 -> DEFINED_BUT_UNDERDETERMINED

G4: PASS_UNDER_MEAN_ZERO_ASSUMPTIONS
 -> DEFINED_BUT_UNDERDETERMINED

G5: PASS_UNDER_LAGRANGIAN_RESTRICTION
 -> DEFINED_BUT_UNDERDETERMINED

Delta_BC: NOT_APPLICABLE
 -> BIFURCATED
```

A split carrier/regional gate record would be even clearer.

### C4 — Correct zero-mode placement

Record that \(Q_CL_C=L_C\) on the stated compact boundaryless domain. Move the
load-bearing zero-mode policy to the actual inverse/source spaces, or retain
\(Q_C\) merely as an explicit range check.

### C5 — Restore the exact \(C_P\) branch

Add:

\[
C_P=\mathscr W-3\mathscr Q,
\qquad C_P(t)=0
\]

for the clean-comoving target branch, and restore the exact \(+C_P/4\) term in
\(\dot C_Z\). Distinguish the inherited target closure from the missing
regional reconstruction needed to evaluate it.

### C6 — Reclassify the selection evidence

Keep S1 only as:

```text
PROVISIONAL_AUTHOR_SELECTED_BASELINE_ARCHITECTURE
```

or retain the existing selection token with an explicit
`CONVENTION_DEPENDENT` evidence classification. Do not describe its preference
over H1 as mathematically derived.

### C7 — Downgrade target naming

Replace `GLOBAL_THEORETICAL_GM_SCALAR_FIELD` with a token such as:

```text
GLOBAL_CANDIDATE_CARRIER_SCALAR_REPRESENTATION_FOR_GM_TARGET
```

until source identities, \(\mathcal T_{\rm eff}\), and G8 are established.

### C8 — Repair Markdown corruption

Regenerate the Markdown using raw strings or escaped backslashes and verify
that it contains no control bytes other than tab/newline.

---

## 8. Nonblocking improvements

1. Replace `H2_0` with explicit mean-zero notation.
2. Remove orientability from the minimum carrier assumptions unless an actual
   volume **form**, rather than a density, is required.
3. Add source hashes to the JSON primary-source inventory.
4. Separate governance conclusions from scientific formal conclusions.
5. Include the exact P0–P8 decision entries when the missing source text is
   available; otherwise rename the block `decision_ledger_summary`.
6. Split G13 into “not an approximation to sharp” and “model sensitivity not
   controlled.”
7. Clarify whether \(E_r\) maps whole regional FLRW slices or finite regional
   patches. The latter is more compatible with a compact carrier.

---

## 9. Recommended corrected gate state for S1

| Gate | Audited recommendation |
|---|---|
| G0 | `PASS_UNDER_EXPLICIT_ASSUMPTIONS` |
| G1 | `PASS_AT_CLASS_LEVEL_ONLY` |
| G2 | `DEFINED_BUT_UNDERDETERMINED` |
| G3 | `PASS_AT_TEMPLATE_LEVEL` |
| G4 | `DEFINED_BUT_UNDERDETERMINED` |
| G5 | `DEFINED_BUT_UNDERDETERMINED` |
| G6 | `PASS_UNDER_SELECTED_PARTITION_LAW` |
| G7 | `FAIL_PROPAGATION_NOT_CLOSED` |
| G8 | `DEFINED_BUT_UNDERDETERMINED` |
| G9 | `PASS_UNDER_HOMOGENEOUS_CLOCK_RESTRICTION` |
| G10 | `PASS_AT_POLICY_LEVEL` |
| G11 | `PARTIAL_CONDITIONAL_ONLY` |
| G12 | `FAIL_NOT_ESTABLISHED` |
| G13 | `SENSITIVITY_REQUIRED` |
| G14 | `PASS` |
| G15 | `FAIL_NOT_ESTABLISHED` |

These changes do not make S1 inconsistent. They restore the distinction between
an explicit architecture template and a defined mathematical composition.

---

## 10. Recommended corrected deficit state for S1

```text
N_undef:
LOWER_BOUND

Delta_dyn:
LOWER_BOUND

Delta_IC:
LOWER_BOUND

Delta_BC:
BIFURCATED

Delta_match:
NOT_COUNTABLE_BEFORE_CONCRETE_OPERATOR_LINEARIZATION

Delta_emp:
NOT_APPLICABLE
unless partition or extensions are empirically calibrated
```

The note “carrier outer boundary not applicable” may remain, but it must not be
used to erase regional elliptic boundary/decay requirements.

---

## 11. Does S1 survive?

**Yes, conditionally.**

S1 survives as a useful baseline because it:

- keeps wall and void inputs distinct;
- introduces no observational bridge;
- avoids an assumed physical surface source;
- exposes its partition and extension choices;
- admits a mathematically meaningful future specification.

It survives only with the corrected status:

```text
PROVISIONAL_AUTHOR_SELECTED_BASELINE_ARCHITECTURE
```

It is not yet proven to be the unique or minimum-extension solution.

---

## 12. Does H1 replace S1?

**No current basis for replacement.**

H1 has stronger explicit regional separation but requires an interface,
transmission law, and coupled elliptic realization not supplied by current
Timescape theory. The audit does not establish FS10. H1 should remain the
mandatory secondary comparator.

The primary selection must be reopened later if:

- S1 cannot define consistent normalized carrier scalarization;
- metric extensions or partition sensitivity remain uncontrolled;
- H1 obtains a closed lower-burden realization;
- S1 fails constraint or effective-sector compatibility.

---

## 13. Final audit decision

```text
AUDIT_VERDICT:
REQUIRES_TARGETED_CORRECTIONS

S1_STATUS:
SURVIVES_AS_PROVISIONAL_AUTHOR_SELECTED_BASELINE

H1_STATUS:
REMAINS_MANDATORY_SECONDARY_COMPARATOR

PRIMARY_SELECTION_REOPENED:
NO

PROTOTYPE_READINESS:
NOT_ACHIEVED

IMPLEMENTATION_AUTHORIZATION:
NOT_GRANTED
```

The next permitted activity is a targeted correction of the Markdown and JSON,
followed by a separate correction-verification pass. No scientific runtime,
prototype, repository integration, commit, tag, or push follows from this
audit.
