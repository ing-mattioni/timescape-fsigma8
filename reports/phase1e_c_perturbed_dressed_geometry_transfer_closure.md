# Phase 1E-C — Perturbed dressed geometry and dust-to-wall transfer closure

## 1. Executive scientific verdict

**Corrected overall status: `PARTIAL_CLOSURE_NEW_DYNAMICS_REQUIRED`.**

The earlier status, `NOT_DERIVABLE_FROM_CURRENT_TIMESCAPE_THEORY`, was too
strong. The corrected two-axis ontology distinguishes an object absent from
Timescape from an unevolved perturbation of an object that Timescape already
defines. On that rule, at least two current-theory routes have
\(N_{\rm undef}=0\):

- Approach A perturbs the explicit W09 dressed background metric and treats its
  lapse and shift as components of the same metric perturbation, not as new
  ontology classes;
- Approach C perturbs the wall/void metrics and dust fields and varies the
  formal matching domain introduced by GM within a single spacetime.

Neither route is closed. The conservative selected-route lower bound is

\[
 \boxed{
 (N_{\rm undef},\Delta_{\rm dyn},\Delta_{\rm IC},
  \Delta_{\rm BC},\Delta_{\rm match},\Delta_{\rm emp})
 =(0,\ge1,\ge1,\ge1,\ge2,{\rm N/A}) } .
\]

This is a lower bound for regional/GM-matching-domain Approach C, not an exact
rank. Wall and void are two distinct regional field sectors, but no
gauge-reduced first-order state yet proves that they contribute two independent
equations or initial functions. Gauge fixing and a source choice can expose
further independent equations and data. `PARTIAL` is selected because the state
can be parameterized using
variations of current-theory metrics, dust fields, domains and matching
structures, while finite dynamics and data remain missing.

This does not derive a dressed transfer, identify \(Z\) with a wall peculiar
velocity, or authorize an observable. Candidate A remains an externally
anchored conditional density-growth diagnostic. No \(\sigma_8\) integral,
observational \(f\sigma_8\), RSD map, likelihood, or runtime default follows.

**Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.**

## 2. Scope, target and non-goals

The target is the conditional chain

\[
 \{\Delta_d,Z\}_{\rm volume\ average\ dust}
 \longrightarrow
 \{\delta\rho_w,\delta\Theta_w,\delta g^{(w)}_{ab},
   k_{\rm local,w}\}
 \longrightarrow
 \{\delta z,\delta\mathcal J\}_{\rm dressed\ light\ cone}.
\]

Closure requires a defined state, independent equations, gauge, initial and
boundary data, and matching functions. This report only decides whether that
problem is exact, conditional, finite but underdetermined, or ontologically
unavailable. It implements nothing.

**Primary classification: `NOT_APPLICABLE`.**

## 3. Repository checkpoint and preservation contract

| Item | Verified value |
|---|---|
| Branch | `phase-1e-c-perturbed-dressed-geometry-transfer-closure` |
| Starting and final HEAD | `8634f14a35c22983413672075fa7f37f03fd663d` |
| `origin/main` | `8634f14a35c22983413672075fa7f37f03fd663d` |
| Existing Phase 1E-B base tag | `phase-1e-b-dressed-lightcone-velocity-derivation-v1` |
| Tag object | `a08230b0ab275993d9e8645d55532a1336c5f637` |
| Peeled commit | `8634f14a35c22983413672075fa7f37f03fd663d` |
| Pinned upstream commit | `590c6fd5332acb15f5683ebf392a0d7ce54983c5` |
| Pinned notebook SHA-256 | `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a` |

The tag name is the exact existing name authorized for P0. No Git tag or ref
was created, renamed, moved, or deleted.

## 4. Frozen-result boundary

The frozen inputs remain:

- Phase 1E-A: `NOT_JUSTIFIED_FOR_OBSERVATIONAL_USE`;
- Phase 1E-B: `PARTIAL_BRIDGE_NEW_DYNAMICS_REQUIRED`;
- Candidate A is external-anchor, conditional, clean-system-only, and
  non-observational;
- the equation-level D3 verdict is `RESOLVED_DERIVED_4_10`;
- `derived_4_10` and `printed_4_15` remain explicit mandatory runtime choices;
- \(\Delta_{d,k}=-k_{\rm code}^2\delta_{m,k}\) holds only in the frozen
  volume-average harmonic convention;
- no observational Fourier map or RSD Jacobian is frozen.

**Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.**

## 5. Scientific question and decision rule

The decisive question is whether each indispensable object is:

1. explicitly defined by current Timescape primary theory;
2. an unambiguous perturbation or variation of a current-theory field, metric,
   congruence, domain, or map;
3. derived from such objects through verified definitions; or
4. already present in the frozen GM/CGI framework without a new physical
   object type.

Only then may a route set \(N_{\rm undef}=0\). Generic GR notation by itself is
insufficient. Conversely, a missing equation does not make a metric
perturbation or domain displacement ontologically undefined.

`PARTIAL_CLOSURE_NEW_DYNAMICS_REQUIRED` requires one viable route with
\(N_{\rm undef}=0\) and finite positive equation/data deficits.
`NOT_DERIVABLE_FROM_CURRENT_TIMESCAPE_THEORY` requires an indispensable new
object type on every viable route.

## 6. Methodology and evidence policy

Load-bearing statements use primary papers or official arXiv versions.
Sign-critical equations were checked on rendered pages. Source verification,
ontology classification, algebra, and interpretation are separate evidence
objects. A symbolic zero proves only the encoded identity.

The reassessment proceeded in this order:

1. temporarily set V1 to `SOURCE_SEARCH_INCOMPLETE`;
2. inspect Balasin completely and rerun citation/synonym searches;
3. reconcile the original 18 topics and add wall-tetrad, spatial-pullback,
   perturbed-null, Balasin, and Balasin-citation records;
4. apply both ontology axes to every disputed object;
5. challenge each \(N_{\rm undef}\) count;
6. recompute A–E, V0–V13, F1–F17, and the verdict.

Unknown exact ranks are not represented as zero. Lower bounds count only
independent blocks whose absence is established before a detailed gauge
choice.

## 7. Primary-source inventory

| ID | Primary source | Version, inspected material, and role |
|---|---|---|
| SRC-GM | Galoppo & Mourier, *Cosmological perturbations on an averaged background* | arXiv:2511.17160v2; PDF pp. 4–25, 43–44; Eqs. (2.2), (2.5)–(2.24), (3.2)–(3.18), (4.1)–(4.29), (5.1)–(5.7); CGI, averaged effective system, and Timescape application |
| SRC-W07 | Wiltshire, *Exact solution to the averaging problem in cosmology* | arXiv:0709.0732v2; PDF pp. 1–4; Eqs. (1)–(8), (19)–(22); two-scale background |
| SRC-W08 | Wiltshire, *Cosmological equivalence principle and the weak-field limit* | arXiv:0809.1183v2; PDF pp. 7–12; Eqs. (10)–(14), (19)–(27); clocks, frames, and limitations |
| SRC-W09 | Wiltshire, *Average observational quantities in the timescape cosmology* | arXiv:0909.0749v2; PDF pp. 1–8, 14; Eqs. (6)–(28), (36)–(38), (51); regional metrics and explicit 4D dressed background metric |
| SRC-BAL13 | Balasin, *Timescape realized* | arXiv:1310.3124v1, 11 Oct 2013; all 15 born-digital PDF pages; Eqs. (3)–(5), (7), (9), (11); conformally-static comparator |
| SRC-B00 | Buchert, dust averaging | arXiv:gr-qc/9906015v2; PDF pp. 2–7; Eqs. (1)–(10c), including (9f) |
| SRC-B01 | Buchert, perfect-fluid averaging | arXiv:gr-qc/0102049v2; PDF pp. 5–8; Eqs. (7)–(12g) |
| SRC-BC-REG | Buchert & Carfora, regional averaging | arXiv:gr-qc/0210037v2; PDF pp. 5–10, 19–36, 44–47 |
| SRC-BC-DRESS | Buchert & Carfora, dressed parameters | arXiv:gr-qc/0210045v1; PDF pp. 1–4 |
| SRC-RB12 | Roy & Buchert, exact deviations | arXiv:1202.5766v2; PDF pp. 2–14; Eqs. (1)–(10) |
| SRC-BMR20 | Buchert, Mourier & Roy, general-fluid averaging | arXiv:1912.04213v2; PDF pp. 3–32, 51–63; lapse, shift, tilt, maps, boundaries |
| SRC-MH24 | Mourier & Heinesen, foliation dependence | arXiv:2401.09170v2, 29 Feb 2024; PDF Sections 2–4 and conclusion |
| SRC-DBE | Dunsby, Bruni & Ellis | ApJ 395 (1992) 54; journal pp. 56–60; Eqs. (14)–(15), (18)–(21), (25)–(34), (42)–(55) |
| SRC-BDE | Bruni, Dunsby & Ellis | ApJ 395 (1992) 34; journal pp. 38–45; Eqs. (14)–(16), (24)–(29), (40), (44)–(48), (61), (63), (74) |
| SRC-WMS24 | Williams et al., numerical relativity voids | arXiv:2403.15134v2; method and conclusion |
| SRC-NW15 | Nazer & Wiltshire, Timescape CMB matching | arXiv:1410.3470v3; auxiliary-FLRW method |
| SRC-CL11 | Challinor & Lewis, observed number counts | arXiv:1105.5292v2; PDF pp. 2–6; Eqs. (1)–(18), (25), (30), (37), (39) |
| SRC-BD11 | Bonvin & Durrer, galaxy-survey observables | arXiv:1105.5280v3; PDF pp. 2–4, 8–10; Eqs. (5)–(17), (29)–(31), (37) |
| SRC-V15 | Visser, conformally FLRW cosmologies | arXiv:1502.02758v3; PDF pp. 1–4; Eqs. (2.1)–(2.4) |

The JSON records access routes, local-retention status, and hashes. CL11,
BD11, and BAL13 were inspected through reproducible official arXiv identifiers
but were not retained locally; their hash is therefore `null`, never invented.

## 8. Renewed search ledger and Balasin audit

The reconciled ledger contains the original 18 topics plus five targeted
records: Balasin direct inspection, Balasin citation chaining, wall tetrads,
three-dimensional spatial pullbacks, and perturbed null/optical propagation.
Each ontology object now points to a semantically matching search record.
The load-bearing SEARCH-01, SEARCH-02, SEARCH-05, SEARCH-06, SEARCH-11,
SEARCH-14, and SEARCH-19 through SEARCH-23 records each state the
2026-07-22 search date, exact query family, search system/database, primary
results opened, and exclusion rationale. Supporting ledger entries remain
bounded topic checks rather than independent proof claims.

Balasin establishes:

- an invertible map between a static metric and a conformally static metric
  (PDF pp. 5–7, Eqs. (3)–(5));
- an observer congruence tied to the conformal Killing field and a redshift
  construction (pp. 7–11, Eqs. (7), (11));
- an Einstein-tensor calculation and hence nontrivial dynamical content
  (p. 8 onward, Eq. (9));
- geodesic dust motion distinct from the generally accelerated expansion
  observer when the spatial conformal factor varies (pp. 12–13);
- an explicit limitation: it is a “first preliminary step” and a possible
  starting point, not a completed averaged-wall perturbation theory.

It does not contain Buchert two-scale variables, the W09 wall/void dressing,
the GM \(\Delta_d,Z\) state, the GM formal wall-void matching domain, the W09
finite-infinity boundary, or their perturbative transfer. It is therefore a
genuine generic-GR comparator, not a GM/Timescape closure route.

Exact-title, arXiv-ID, author, conformal/static-observer, citation, and
Timescape-synonym searches found no relevant primary follow-up deriving the
missing GM wall transfer. This is a bounded search result, not an assertion
about unpublished work.

**Renewed source-completeness result: `PASS`. Primary classification:
`VERIFIED_FROM_PRIMARY_SOURCE`.**

## 9. Two-axis ontology vocabulary

Axis 1, `current_theory_definition_state`, is exactly:

- `NOT_DEFINED_IN_CURRENT_THEORY`
- `BACKGROUND_DEFINED`
- `KINEMATICALLY_DEFINED`
- `DERIVED_IF_CURRENT_THEORY_DEPENDENCIES_KNOWN`
- `DYNAMICALLY_DETERMINED`
- `AMBIGUOUS_PENDING_SOURCE_AUDIT`

Axis 2, `generic_GR_parameterizability`, is exactly:

- `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE`
- `PARAMETERIZABLE_ONLY_AFTER_NEW_EMBEDDING_OR_FIELD`
- `NOT_YET_PARAMETERIZED`
- `NOT_APPLICABLE`

The axes answer different questions. “Can be written in GR” is not “is in
Timescape”; “has no equation yet” is not “has no object type.”

## 10. Target dependency graph

```text
{tracker background, Delta_d, Z}
        |
        +--> perturb W09 dressed metric ----------------------+
        |       \--> metric lapse/shift, wall tetrad          |
        +--> vary regional wall/void metrics and dust --------+--> wall fields
        |       \--> vary formal GM boundary --> matching ----+
        +--> determine u_w and xi_dw -------------------------+
        +--> derive 3D pullback / local modes ----------------+
        +--> insert resulting metric/tetrads into general photon/Jacobi laws
```

The graph identifies dependencies but does not prove an exhaustive route set.
Approach E therefore makes no completeness or minimal-cut-set claim.

## 11. Layer ontology

The layers remain:

1. `LOCAL_SPACETIME`;
2. `REGIONAL_AVERAGE`;
3. `GLOBAL_DOMAIN_AVERAGE`;
4. `DRESSED_BACKGROUND`;
5. `PERTURBATIVE_TRANSFER`;
6. `LIGHT_CONE`;
7. `EMPIRICAL_TRACER`.

Layer equality is never inferred from notation. The corrected result instead
asks whether a target-layer object is an admissible variation of an existing
object and then records the still-missing transfer equations.

## 12. Geometry ontology

| Object | Axis 1 | Axis 2 | Admissibility result |
|---|---|---|---|
| W09 dressed background metric \(\bar g^{\rm dressed}_{ab}\) | `BACKGROUND_DEFINED` | `NOT_APPLICABLE` | current-theory background |
| \(\delta g^{\rm dressed}_{ab}\) | `KINEMATICALLY_DEFINED` | `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE` | symmetric-tensor tangent to the explicit W09 metric; dynamics/source/gauge absent |
| local metric lapse and shift | `DERIVED_IF_CURRENT_THEORY_DEPENDENCIES_KNOWN` | `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE` | ADM components of the same metric perturbation, not separate \(N_{\rm undef}\) classes |
| perturbed wall tetrad | `DERIVED_IF_CURRENT_THEORY_DEPENDENCIES_KNOWN` | `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE` | follows after metric, congruence, and Lorentz-gauge choice |
| GM averaged perturbation state | `DYNAMICALLY_DETERMINED` | `NOT_APPLICABLE` | frozen \(\Delta_d,Z\) source layer |

The tangent space is mathematically unambiguous without choosing scalar,
vector, tensor, or gauge variables. Its physical source/closure is not. This
converts the old metric ontology deficit into finite dynamics, initial-data,
and matching deficits.

**Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.**

## 13. GM matching-domain and finite-infinity ontology

GM distinguishes wall and void domain classes, models each by a dust-sourced
FLRW spacetime, and formally introduces a third zero-volume domain to ensure
general-relativistic wall/void matching “within a single spacetime” (PDF p. 22).
It also says the boundary remains ultimately unspecified. Eqs. (5.1)–(5.7)
then provide only regional/global background volumes, rates, proper times,
lapse, and radial-null matching.

Thus:

| Object | Axis 1 | Axis 2 | Admissibility result |
|---|---|---|---|
| GM formal wall-void matching domain | `BACKGROUND_DEFINED` | `NOT_APPLICABLE` | current-theory formal domain, but no embedding supplied |
| GM formal wall-void matching-domain embedding | `KINEMATICALLY_DEFINED` | `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE` | embedding of the existing formal GM domain |
| GM formal wall-void matching-domain displacement | `KINEMATICALLY_DEFINED` | `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE` | variation of that formal domain/embedding |
| W09 finite-infinity boundary as a candidate physical realization | `BACKGROUND_DEFINED` | `NOT_APPLICABLE` | operational wall-region boundary; no derivation identifies it with the GM formal matching domain |
| wall/void metric perturbations | `KINEMATICALLY_DEFINED` | `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE` | variations of explicit regional FLRW metrics |
| wall/void dust perturbations | `KINEMATICALLY_DEFINED` | `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE` | variations of current dust sources |
| junction/matching functions | `DERIVED_IF_CURRENT_THEORY_DEPENDENCIES_KNOWN` | `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE` | finite unknown functions once embedding/fields are chosen |

GM supplies a formal common-manifold intention, not an actual matching-domain
construction. W09 finite infinity is a separate physical/regional notion and
is only a candidate realization; it is not substituted for the GM formal
domain without a derivation. These distinctions support a finite partial
problem without pretending that the embedding or matching equations are known.

**Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.**

## 14. Frame and congruence ontology

GM’s general CGI formalism permits an arbitrary observer on one spacetime.
Its averaged effective-fluid application selects a volume-average dust frame.
Its Timescape section supplies background regional observers and clocks.
These three layers are not interchangeable.

The wall proper-time metric defines a background comoving wall congruence.
A normalized first-order perturbation \(\delta u_w^a\) is therefore
`KINEMATICALLY_DEFINED` and
`PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE`; its dynamics and eventwise matching
to GM’s \(u_d^a\) are missing.

For a declared common event map,

\[
 \xi_{dw}^a=u_w^a-u_d^a,\qquad u_{d\,a}\xi_{dw}^a=0
\]

is kinematic. GM’s formal single-spacetime matching makes this a legitimate
conditional state variable, not a derived boost solution.

**Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.**

## 15. Six-object lapse ontology

No lapse pair is identified without a derivation.

| Object | Layer | Axis 1 / Axis 2 | Gauge status | Dependencies, equation, and independence |
|---|---|---|---|---|
| local/conceptual \(\gamma(\tau,\mathbf x)\) | local clocks | `NOT_DEFINED_IN_CURRENT_THEORY` / `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE` | scalar ratio only after two local clock congruences are supplied | current Timescape defines the regional background lapse, not this pointwise field; it remains distinct from \(\delta\bar\gamma_w\), \(\delta N_D\), and \(\delta N_w\) |
| \(\bar\gamma_w(t)=dt/d\tau_w\) | regional background | `DYNAMICALLY_DETERMINED` / `NOT_APPLICABLE` | background convention fixed | tracker equation; independent background output |
| \(\delta\bar\gamma_w(t)\) | perturbed regional background | `KINEMATICALLY_DEFINED` / `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE` | time-reparameterization dependent | variation of \(\bar\gamma_w\); determining perturbation equation missing |
| pointwise \(\delta\gamma(\tau,\mathbf x)\) | local transfer | `KINEMATICALLY_DEFINED` / `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE` | slicing dependent | variation of a pointwise clock ratio if defined; not equal to \(\delta\bar\gamma_w\) |
| \(\delta N_D\) | average-frame ADM metric | `DERIVED_IF_CURRENT_THEORY_DEPENDENCIES_KNOWN` / `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE` | gauge dependent | lapse component of a perturbed average/reference metric |
| \(\delta N_w\) | wall-frame ADM metric | `DERIVED_IF_CURRENT_THEORY_DEPENDENCIES_KNOWN` / `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE` | gauge dependent | lapse component of \(\delta g^{\rm dressed}_{ab}\) or regional wall metric |

If a particular common 3+1 construction defines \(\gamma=N_D/N_w\), then

\[
 \frac{\delta\gamma}{\bar\gamma}
 =\frac{\delta N_D}{\bar N_D}
  -\frac{\delta N_w}{\bar N_w}.
\]

This identity does not equate \(\delta\gamma\) with either lapse perturbation,
does not equate pointwise and regional variations, and supplies no dynamics.

**Primary classification: `SYMBOLICALLY_VERIFIED`.**

## 16. Scale, averaging and regional variables

Buchert’s commutator,

\[
 \partial_t\langle\psi\rangle_{\mathcal D}
 -\langle\partial_t\psi\rangle_{\mathcal D}
 =\langle\psi\Theta\rangle_{\mathcal D}
 -\langle\psi\rangle_{\mathcal D}\langle\Theta\rangle_{\mathcal D},
\]

prevents inversion of a domain average into a unique local field. A regional
perturbation state can nevertheless be parameterized; it must then be evolved
and constrained so that its averages reproduce the GM variables. This is a
matching/closure problem, not automatic reconstruction.

**Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.**

## 17. Common-spacetime and pullback audit

GM’s Timescape application formally places wall, void, and matching domains in
one spacetime but does not give their embeddings or tensor pullbacks. The
correct classification is therefore:

- formal common-spacetime/domain object: `BACKGROUND_DEFINED`;
- actual event map and three-dimensional pullback:
  `DERIVED_IF_CURRENT_THEORY_DEPENDENCIES_KNOWN`;
- generic parameterizability:
  `PARAMETERIZABLE_WITHOUT_NEW_OBJECT_TYPE` for variations of the stated
  domain and its charts;
- determining equations/data: absent.

BMR20 supplies applicable machinery after a common foliation, map, lapse,
shift, and congruence are specified. It does not select those data for
Timescape. The map is a finite matching deficit on Approach C; it is not
silently treated as already solved.

**Primary classification: `UNRESOLVED_EXTERNAL_DEPENDENCY`.**

## 18. Independent-equation ontology

Available independent families are:

- `EQ-01`: frozen GM volume-average perturbation evolution;
- `EQ-02`: Buchert background evolution/integrability;
- `EQ-03`: Timescape tracker/dressing background closure;
- `EQ-04`: W09 background radial-null matching;
- `EQ-13`: general photon, geodesic-deviation, and Jacobi propagation,
  conditional on a metric and optical data.

Kinematic identities `EQ-05` (density boost), `EQ-06` (expansion boost), and
`EQ-07` (lapse-ratio variation) do not evolve their inputs.

Missing finite equation/data blocks are:

- `EQ-08`: wall-congruence/boost dynamics;
- `EQ-09`: perturbative dressed or regional metric/source equations;
- `EQ-10`: GM formal matching-domain evolution and matching conditions;
- `EQ-11`: gauge/constraint closure;
- `EQ-12`: three-dimensional pullback and mode-transfer conditions.

## 19. Gauge, constraints, and finite rank

The exact rank cannot be reported before a gauge and source representation are
chosen. It is nevertheless finite for A and C because their state variables are
standard perturbations of finite tensor/field/domain types. Wall and void are
two distinct regional field sectors requiring separate or coupled treatment,
but this sector distinction is not itself a proof of two independent dynamical
equations or two independent initial functions. Lapse and shift are
not counted twice as new ontology; constraints and gauge equations must be
removed from the independent dynamics count.

The reported vectors are therefore conservative lower bounds, not exact
degrees of freedom. Gate V10 becomes `DEFINED_BUT_UNDERDETERMINED`, not
`PASS`.

**Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.**

## 20. Closure-deficit methodology

Each route is recorded as

\[
 (N_{\rm undef},\Delta_{\rm dyn},\Delta_{\rm IC},
  \Delta_{\rm BC},\Delta_{\rm match},\Delta_{\rm emp}).
\]

\(N_{\rm undef}\) counts indispensable object types failing the admissibility
rule. The \(\Delta\) entries count finite missing equation or data blocks after
the state is admitted. Lower bounds do not claim exact rank.

The verdict rule is:

- exact: \(N_{\rm undef}=0\) and every required deficit is zero;
- conditional: the same after a fully enumerated approximation;
- partial: \(N_{\rm undef}=0\) and at least one finite positive deficit;
- not derivable: every viable route retains an indispensable inadmissible new
  object type.

## 21. Candidate approach A — direct dressed-metric perturbation

W09 supplies an explicit four-dimensional dressed background metric. Its
symmetric-tensor tangent

\[
 g^{\rm dressed}_{ab}(\epsilon)
 =\bar g^{\rm dressed}_{ab}+\epsilon h^{\rm dressed}_{ab}+O(\epsilon^2)
\]

defines \(h^{\rm dressed}_{ab}\) without choosing gauge or scalar variables.
Lapse and shift are a decomposition of \(h_{ab}\), not extra ontology classes.
The source interpretation, field/closure equations, constraints, gauge,
initial data, and match to GM are absent.

Conservative lower bound:

\[
 (0,\Delta_{\rm dyn}\ge1,\Delta_{\rm IC}\ge1,
   {\rm N/A},\Delta_{\rm match}\ge1,{\rm N/A}).
\]

**Best-status ceiling: `PARTIAL_CLOSURE_NEW_DYNAMICS_REQUIRED`.**
This route is admissible but not closed and not unique.

**Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.**

## 22. Candidate approach B — covariant dust-to-wall boost

On the formal common spacetime, first-order frame identities give

\[
 \mathcal D_a^{(w)}
 =\mathcal D_a^{(d)}-a\Theta(1+w)\xi^{dw}_a,
 \qquad
 \Theta_w=\Theta_d+D_a\xi_{dw}^a .
\]

For the explicit scalar-sector challenge

\[
 \xi_{dw}^a=D^a\chi_{dw},
\]

both shifts are fixed operators on one scalar. The identities do not determine
\(\chi_{dw}\). The conservative deficit is

\[
 (0,\Delta_{\rm dyn}\ge1,\Delta_{\rm IC}\ge1,
   {\rm N/A},\Delta_{\rm match}\ge1,{\rm N/A}),
\]

conditional on interpreting GM’s formal single-spacetime matching domain as the
eventwise comparison arena. Its ontology count is explicitly bifurcated:

- \(N_{\rm undef}=0\) if that formal domain is accepted as the comparison
  arena;
- \(N_{\rm undef}\ge1\) if a distinct eventwise embedding must first be
  introduced.

Approach B remains unselected. Approach C keeps the formal matching-domain
embedding as an explicit finite state/matching variable.

**Best-status ceiling: `PARTIAL_CLOSURE_NEW_DYNAMICS_REQUIRED`.**

**Primary classification: `UNRESOLVED_EXTERNAL_DEPENDENCY`.**

## 23. Candidate approach C — regional/GM-matching-domain closure

The strongest finite-parameterization challenge uses:

- wall and void metric perturbations;
- wall and void dust perturbations;
- a GM formal wall-void matching-domain embedding and displacement;
- regional lapse variations;
- induced matching/junction data;
- averaged backreaction/deformation variables constrained to the GM state.

These are variations of current regional metrics, dust sources, domain, and
averaging variables. No new physical object type is required merely to write
the state. The missing evolution, initial, boundary, and matching laws are
finite independent blocks:

\[
 \boxed{
 (0,\Delta_{\rm dyn}\ge1,\Delta_{\rm IC}\ge1,
   \Delta_{\rm BC}\ge1,\Delta_{\rm match}\ge2,{\rm N/A}) } .
\]

The one-block dynamics/IC lower bounds follow the original definitions without
claiming a gauge-reduced rank. Wall and void remain distinct regional field
sectors and must receive separate or coupled dynamical treatment in the next
phase. The BC lower bound is the GM formal matching-domain displacement data.
The two matching blocks distinguish geometry and matter/averaging
compatibility. These are not assertions that Israel matching is automatically
appropriate, and W09 finite infinity is not identified with this formal domain.

**Best-status ceiling: `PARTIAL_CLOSURE_NEW_DYNAMICS_REQUIRED`.**
This is the selected viable path.

**Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.**

## 24. Candidate approach D — local tetrad/Fermi/WKB patch

A local tetrad and local wavevector can be derived after a wall metric,
congruence, and spatial pullback are determined. They are not new object types,
but a Fermi or WKB approximation cannot determine the missing upstream state.

Conservative inherited lower bound:

\[
 (0,\Delta_{\rm dyn}\ge1,\Delta_{\rm IC}\ge1,
   {\rm N/A},\Delta_{\rm match}\ge2,{\rm N/A}),
\]

plus an explicit locality/short-wave approximation. The old one-radial-
constraint versus nine-Jacobian-components check only proves
underdetermination; it does not count physical modes after gauge reduction.

**Best-status ceiling: `PARTIAL_CLOSURE_NEW_DYNAMICS_REQUIRED`.**

**Primary classification: `NOT_JUSTIFIED`** for using D as an independent
closure.

## 25. Candidate approach E — bounded dependency challenge

Approach E is not a fifth physical model and is not a proof over all imaginable
routes. Its declared route universe is A–D plus
`finite_parameterization_challenge`. A route is included only if it begins
with frozen GM/Timescape objects and aims at the same wall-transfer target.

Edges mean either:

- `CURRENT_THEORY_VARIATION`: a definition or variation satisfying the
  admissibility rule; or
- `EXTENDED_THEORY_INPUT`: a genuinely new embedding, field ontology, or
  physical identification.

Path completeness means every target dependency is represented; it does not
mean the route has equations. Candidate cut sets are diagnostic coverage sets
only. No cut minimality or universe completeness is claimed.

The adversarial `finite_parameterization_challenge` succeeds for A and C:
every disputed object on those routes is an admissible current-theory
variation, leaving finite equation/data blocks. Thus the old universal
no-derivation claim is falsified.

**Best-status ceiling: `PARTIAL_CLOSURE_NEW_DYNAMICS_REQUIRED`.**

**Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.**

## 26. Cross-approach closure matrix

| Approach | \(N_{\rm undef}\) | \(\Delta_{\rm dyn}\) | \(\Delta_{\rm IC}\) | \(\Delta_{\rm BC}\) | \(\Delta_{\rm match}\) | Ceiling |
|---|---:|---:|---:|---:|---:|---|
| A direct dressed metric | 0 | \(\ge1\) | \(\ge1\) | N/A | \(\ge1\) | `PARTIAL_CLOSURE_NEW_DYNAMICS_REQUIRED` |
| B scalar boost | bifurcated: 0 with GM formal comparison arena; \(\ge1\) if a distinct eventwise embedding is required | \(\ge1\) | \(\ge1\) | N/A | \(\ge1\) | `PARTIAL_CLOSURE_NEW_DYNAMICS_REQUIRED` under the first branch; unselected |
| C regional/GM matching domain | 0 | \(\ge1\) | \(\ge1\) | \(\ge1\) | \(\ge2\) | `PARTIAL_CLOSURE_NEW_DYNAMICS_REQUIRED` |
| D local patch downstream of A/C | 0 | \(\ge1\) | \(\ge1\) | N/A | \(\ge2\) | `PARTIAL_CLOSURE_NEW_DYNAMICS_REQUIRED` |
| E bounded challenge | 0 on A/C | finite lower bounds above | finite | route-dependent | finite | `PARTIAL_CLOSURE_NEW_DYNAMICS_REQUIRED` |

Only C is selected for the next-phase specification because it exposes the
wall/void/formal-matching-domain content instead of hiding it in an effective
source.

## 27. Recomputed gates V0–V13

| Gate | Question | Corrected outcome |
|---|---|---|
| V0 | frozen inputs preserved? | `PASS` |
| V1 | renewed scoped source search complete? | `PASS` |
| V2 | common spacetime/pullback status? | `DEFINED_BUT_UNDERDETERMINED` |
| V3 | perturbed dressed metric status? | `DEFINED_BUT_UNDERDETERMINED` |
| V4 | perturbed wall congruence status? | `DEFINED_BUT_UNDERDETERMINED` |
| V5 | six lapse objects distinguished and determined? | `DEFINED_BUT_UNDERDETERMINED` |
| V6 | dust-to-wall boost determined? | `DEFINED_BUT_UNDERDETERMINED` |
| V7 | regional GM formal matching-domain relations determined? | `DEFINED_BUT_UNDERDETERMINED` |
| V8 | spatial/harmonic transfer determined? | `DEFINED_BUT_UNDERDETERMINED` |
| V9 | light-cone ontology and Timescape inputs? | `DEFINED_BUT_UNDERDETERMINED` |
| V10 | finite independent-equation rank available? | `DEFINED_BUT_UNDERDETERMINED` |
| V11 | sufficient IC/BC/matching data specified? | `DEFINED_BUT_UNDERDETERMINED` |
| V12 | approximations explicit? | `PASS` |
| V13 | algebra, dimensions, frames, and limits consistent? | `PASS` |

V2–V11 do not pass closure. They say the relevant object types can be
parameterized but their maps, equations, gauge, and data remain missing.

## 28. Split bridge relation matrix

| From | To | Relation status | Limitation |
|---|---|---|---|
| \(\Delta_d,Z\) | volume-average \(\delta_m\), expansion-gradient variables | `EXACTLY_DERIVED` | frozen harmonic/frame only |
| \(t\) | \(\tau_w\) | `EXACTLY_DERIVED` | background lapse only |
| \(\bar\gamma_w\) | any lapse perturbation | `REQUIRES_NEW_DYNAMICAL_INPUT` | six-object dictionary and gauge required |
| \(u_d\) | \(u_w\) | `REQUIRES_NEW_DYNAMICAL_INPUT` | embedding/matching and wall dynamics |
| dust density gradient | wall density gradient | `REQUIRES_NEW_DYNAMICAL_INPUT` | conditional boost plus pullback |
| \(Z\) | wall expansion perturbation | `REQUIRES_NEW_DYNAMICAL_INPUT` | conditional congruence identity; \(\xi_{dw}\) not evolved |
| \(Z\) | local wall peculiar-velocity divergence | `REQUIRES_NEW_DYNAMICAL_INPUT` | additionally needs wall slicing, background subtraction, velocity definition, and spatial/mode map |
| \(k_{\rm code}\) | \(k_{\rm local,w},\mu\) | `REQUIRES_NEW_DYNAMICAL_INPUT` | 3D pullback underdetermined |
| general photon/redshift/Jacobi variables | Timescape perturbed light cone | `REQUIRES_NEW_DYNAMICAL_INPUT` | metric, tetrads, endpoint velocities, optical data, curvature, and source evolution |
| Candidate A \(Q_{\rm anchor,dressed}\) | wall velocity amplitude | `NOT_MAPPABLE_WITH_CURRENT_THEORY` | no solved transfer |
| local matter | tracer | `REQUIRES_EMPIRICAL_ASSUMPTION` | bias and selection |
| frozen outputs | observational \(f\sigma_8\) | `NOT_MAPPABLE_WITH_CURRENT_THEORY` | all preceding dependencies |

The expansion and peculiar-velocity targets are deliberately separate.

## 29. Falsification suite F1–F17

`PASS` means the stated challenge was executed; it does not mean closure.

| ID | Challenge | Result |
|---|---|---|
| F1 | treat W09 metric as ontologically absent | `PASS`: corrected; its perturbation tangent is admissible |
| F2 | conflate gauge relabeling with frame boost | `PASS`: rejected |
| F3 | reverse boost direction silently | `PASS`: rejected |
| F4 | set \(\xi_{dw}=0\) | `PASS`: exposed as extra assumption |
| F5 | identify all lapse perturbations | `PASS`: six-object audit rejects it |
| F6 | infer spatial transfer from time chain | `PASS`: rejected |
| F7 | commute averaging and evolution | `PASS`: contradicted by Buchert commutator |
| F8 | hold the GM formal matching domain fixed | `PASS`: exposed as BC |
| F9 | identify \(k_{\rm code}\) with wall \(k\) | `PASS`: rejected |
| F10 | patch local charts uniquely without matching | `PASS`: rejected |
| F11 | infer perturbed light cone from background distance | `PASS`: missing inputs separated |
| F12 | replace missing dynamics with an algebraic identity | `PASS`: rejected |
| F13 | count kinematic identities as dynamics | `PASS`: rejected |
| F14 | provide IC without evolution | `PASS`: insufficient |
| F15 | promote FLRW/Fermi/WKB limit globally | `PASS`: rejected |
| F16 | promote Candidate A to observable | `PASS`: rejected |
| F17 | finite-parameterization challenge | `PASS`: A and C have admissible \(N_{\rm undef}=0\) states with finite positive deficits; old `NOT_DERIVABLE` is falsified |

F17 distinguishes current-theory variations from generic-GR inventions and
mere symbolic names. Balasin does not supply the passing route.

## 30. Limit and consistency suite L-01–L-16

| ID | Limit/check | Result |
|---|---|---|
| L-01 | FLRW | recovers a standard perturbative setting only in the limit |
| L-02 | \(\bar\gamma_w\to1\) | removes background clock difference, not transfer dynamics |
| L-03 | \(\delta\bar\gamma_w\to0\) | does not set local lapse perturbations to zero |
| L-04 | \(\xi_{dw}\to0\) | conditional frame shifts vanish |
| L-05 | zero metric perturbation | deletes the target |
| L-06 | zero peculiar velocity | deletes Doppler/RSD terms |
| L-07 | zero wall/void contrast | homogeneous limit |
| L-08 | local Fermi | requires a supplied metric/worldline |
| L-09 | WKB | requires a local mode map |
| L-10 | distant observer | downstream approximation |
| L-11 | zero shear | does not determine lapse or acceleration |
| L-12 | zero acceleration | extra wall-geodesic assumption |
| L-13 | dust only | does not close averaging/matching |
| L-14 | regional wall | regional fields remain nonlocal averages |
| L-15 | dimensional | \(k_{\rm code}\) needs a frame-specific reciprocal length |
| L-16 | matched frame/units | necessary, not sufficient |

All limits pass consistency. None closes a missing equation.

## 31. Symbolic and analytic checks

### SC-01 — normalized density-gradient sign

\[
 D_a^{(w)}\rho-D_a^{(d)}\rho=\dot{\bar\rho}\,\xi_a,\qquad
 \dot{\bar\rho}=-\Theta(\bar\rho+\bar p)
\]

implies the exact residual

\[
 \left(\mathcal D_a^{(w)}-\mathcal D_a^{(d)}\right)
 +a\Theta(1+w)\xi_a=0 .
\]

### SC-02 — direction reversal

\(\xi_{d\to w}=-\xi_{w\to d}\) reverses both first-order shifts; the
round-trip residual is zero.

### SC-03 — lapse ratio

\[
 \delta\ln\gamma-\delta\ln N_D+\delta\ln N_w=0 .
\]

### SC-04 — expansion shift

\[
 \Theta'-\Theta-D_a\xi^a=0
\]

at first order on a declared common spacetime.

### SC-05 — favourable scalar-boost rank

Two displayed shifts depending on one \(\chi_{dw}\) have Jacobian rank one.
One evolution law and one initial function remain as a lower bound.

### SC-06 — radial versus three-dimensional map

One radial matching constraint on a generic \(3\times3\) Jacobian has algebraic
rank one and nullity eight before symmetry/gauge reduction. It establishes
underdetermination only.

### SC-07 — same-mode harmonic cancellation

\[
 \frac{-\Delta_{d,k}(t)/k_{\rm code}^2}
      {-\Delta_{d,k}(t_{\rm ref})/k_{\rm code}^2}
 =\frac{\Delta_{d,k}(t)}{\Delta_{d,k}(t_{\rm ref})}.
\]

The residual is zero and says nothing about a wall Fourier map.

**Primary classification for SC-01–SC-07: `SYMBOLICALLY_VERIFIED`.**

## 32. Formal verdict selection

The corrected verdict is

\[
 \boxed{\texttt{PARTIAL\_CLOSURE\_NEW\_DYNAMICS\_REQUIRED}} .
\]

Source completeness is `PASS`. Approach C satisfies the admissibility rule and
has \(N_{\rm undef}=0\). Its positive finite lower-bound deficits are
\(\Delta_{\rm dyn}\ge1\), \(\Delta_{\rm IC}\ge1\),
\(\Delta_{\rm BC}\ge1\), and \(\Delta_{\rm match}\ge2\). Therefore the decisive
PARTIAL rule is met.

This is an ontology/equation-counting verdict, not a transfer solution. The
physical adequacy of treating regional FLRW metrics and the formal GM boundary
as a perturbative initial-boundary-value system remains unresolved.

**Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.**

## 33. Rejection of the three unselected statuses

`EXACT_DRESSED_TRANSFER_CLOSURE_DERIVED` fails because V2–V11 are
underdetermined and all selected-route deficits are positive.

`CONDITIONAL_DRESSED_TRANSFER_CLOSURE_DERIVED` fails because no explicit
approximation supplies the missing dynamics, gauge, initial/boundary data, and
matching functions.

`NOT_DERIVABLE_FROM_CURRENT_TIMESCAPE_THEORY` fails F17: A and C represent
every indispensable object as a current-theory variation without adding a new
physical object type. Missing equations and data alone cannot sustain that
stronger token.

**Primary classification: `NOT_JUSTIFIED`** for each rejected token.

## 34. Minimum missing dynamics for the selected route

Approach C requires, at minimum:

1. at least one perturbation evolution/constraint block with a declared gauge;
   wall and void are distinct sectors, but whether their dynamics are separate
   or coupled and the exact independent rank remain to be derived;
2. at least one initial-data block, with the sector-specific data structure to
   be determined by that derivation;
3. a GM formal wall-void matching-domain displacement/embedding datum and its
   boundary prescription;
4. at least two matching blocks: geometry and matter/averaging compatibility;
5. equations relating regional averages and deformations to the frozen GM
   \(\Delta_d,Z\) state;
6. only after these, a derived wall tetrad, spatial pullback, and local mode map.

The exact rank must be recalculated after the state/gauge choice. No Israel
junction rule, fixed matching domain, or inverse averaging map is silently
assumed.

## 35. Implementation consequence

**GO/NO-GO: `NO_GO_FOR_SCIENTIFIC_RUNTIME_IMPLEMENTATION`.**

`PARTIAL` permits a next equation-level derivation of the missing regional and
GM formal matching-domain dynamics. It does not permit a metric module,
transfer solver, wall-velocity API, local-wavevector conversion, light-cone/RSD
code, or observational reinterpretation.

Both D3 branches remain explicit and mandatory with no runtime default.
Mészáros remains a comparison-only, formally inapplicable Timescape baseline.

**Primary classification: `NOT_JUSTIFIED`** for runtime implementation.

## 36. Observational consequence

Candidate A remains:

- externally normalized rather than a Timescape \(\sigma_8\) prediction;
- free of a \(\sigma_R\) or \(\sigma_8\) spectral integral;
- a volume-average clean-system density-growth diagnostic;
- without a solved dust-to-wall velocity transfer, spatial map, tracer model,
  perturbed light-cone Jacobian, AP conversion, or likelihood.

Therefore neither \(Q_{\rm anchor,bare}\) nor
\(Q_{\rm anchor,dressed}\) is observational \(f\sigma_8\). The corrected
PARTIAL verdict is not a statistical uncertainty or permission to construct
an error band.

**Primary classification: `NOT_JUSTIFIED`.**

## 37. Corrected permitted next phase

**Phase 1E-D — Regional wall/void perturbation and GM formal matching-domain dynamics.**

Permitted scope:

- write the wall and void perturbation state and gauge explicitly;
- derive or source their independent evolution and constraint blocks;
- parameterize the existing GM formal wall-void matching-domain embedding and
  displacement;
- derive geometry and matter/averaging matching alternatives;
- recalculate the exact equation, IC, BC, and matching rank;
- stop before numerical or observational implementation.

Entry requires human approval for every new physical closure or junction
assumption. Exit requires a closed or explicitly conditional transfer state
with independently verified equations. This phase must not retroactively make
Candidate A observational.

**Primary classification: `UNRESOLVED_EXTERNAL_DEPENDENCY`.**

## 38. Forbidden implementations

The following remain forbidden:

- perturbed dressed metric or wall-transfer runtime code;
- dust-to-wall velocity or local wall perturbation APIs;
- \(k_{\rm code}\)-to-wall/dressed/observational Fourier conversion;
- Kaiser/RSD/observational \(f\sigma_8\) APIs;
- spectra, transfer functions, windows, \(\sigma_R\), or \(\sigma_8\)
  integration;
- density/velocity bias, AP or survey adapters;
- datasets, covariance, likelihoods, fits, or inference;
- any Candidate A or D3 runtime change;
- silent FLRW, zero-boost, zero-lapse, fixed-GM-matching-domain, deterministic-bias, or
  zero-velocity-bias assumptions.

No author communication or publication is made.

## 39. Repository preservation and validation

The same tracked source tree at
`8634f14a35c22983413672075fa7f37f03fd663d` is used in both established
environments:

| Environment | Packages | Complete result |
|---|---|---|
| Python 3.14.3 | NumPy 2.5.1; SciPy 1.18.0; pytest 9.1.1; pluggy 1.6.0 | 379 passed, 0 failed, 0 skipped, 0 xfailed, 0 warnings in 14.37 s |
| Python 3.11.9 | NumPy 2.4.6; SciPy 1.17.1; pytest 9.1.1; pluggy 1.6.0 | 379 passed, 0 failed, 0 skipped, 0 xfailed, 0 warnings in 15.91 s |

Final structural validation requires: 39 numbered sections; 31 JSON top-level
keys; unique IDs; no dangling references; exact allowed vocabularies; six
lapse records; approaches A–E; V0–V13; F1–F17; L-01–L-16; nine-field formal
conclusions; split \(Z\) relations; explicit A–D ceilings; and agreement on
verdict, deficits, and next phase.

The expanded `local_evidence_inventory` covers the frozen Phase 1D-A through
Phase 1E-B reports/inventories and the background, perturbation, and growth
modules actually used for definitions. Each record states its inspected scope;
none claims a complete read during this correction pass where only targeted
definitions or conclusions were rechecked.

Only these repository files are created:

- `reports/phase1e_c_perturbed_dressed_geometry_transfer_closure.md`
- `reports/phase1e_c_perturbed_dressed_geometry_transfer_inventory.json`

No pre-existing tracked file, source, test, configuration, artifact, notebook,
previous report, or upstream file is modified. Nothing is staged. No commit,
tag, ref, push, merge, pull request, publication, author communication,
runtime implementation, or Phase 1E-D work occurs.
