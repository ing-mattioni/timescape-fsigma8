# Phase 1E-B — Local dressed light-cone and velocity-transfer derivation

## 1. Executive verdict

**Overall bridge status: `PARTIAL_BRIDGE_NEW_DYNAMICS_REQUIRED`.**

The frozen theory supplies three rigorous but disconnected pieces: (i) the
volume-average dust-frame scalar chain from \(\Delta_d\) and \(Z\) to the
dust density and expansion perturbations; (ii) a background dressed
Timescape geometry, lapse, redshift, distance, and Hubble rate; and (iii) the
general covariant photon-energy and observed-number-count formulae applicable
once a perturbed metric, source/observer velocities, and a light-cone map are
specified. It does **not** supply a perturbed dressed metric, a perturbative
wall lapse, a dust-to-wall velocity field, a volume-average-to-wall spatial
map, or a Timescape-specific real-to-observed-redshift-space Jacobian.

Consequently no dressed Kaiser formula is derived, \(Z\) is not identified
with an observed line-of-sight velocity derivative, and the frozen Candidate
A quantity \(Q_{\rm anchor,dressed}\) remains an externally anchored density
growth diagnostic rather than observational \(f\sigma_8\). A local tetrad and
local wave covector can be defined pointwise in the background dressed metric;
promoting them to a finite-patch Fourier or plane-parallel construction is an
explicit short-wave approximation and still does not determine their map from
\(k_{\rm code}\).

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`. Supporting
evidence consists of primary-source transcription, exact coefficient checks,
and the missing-object inventory below; these supporting types are not
additional primary classifications.

## 2. Scope and preservation statement

This is an equation-level audit, not an observable implementation. It creates
only this report and its JSON companion. It does not alter Candidate A, any
background, perturbation, growth, mapping, or rate code, either D3 runtime
branch, any test, or any frozen report. It introduces no RSD API, spectrum,
\(\sigma_R\) integral, bias model, Alcock–Paczynski calculator, dataset,
likelihood, fit, or observational value.

Primary classification: `NOT_APPLICABLE` (repository-scope statement).

## 3. Repository checkpoint

The audit began and ended at commit
`f4044cbe10a7fbd59d1b14131e2d2e31100984ef` on local branch
`phase-1e-b-dressed-lightcone-velocity-derivation`. Annotated tag
`phase-1e-a-dressed-observable-bridge-audit-v1` had tag-object
`bdcbaaca20aed707d43944fc2cd5096b636243b1` and peeled to that commit.
All ten frozen tags from `phase-1b-background-v1` through the Phase 1E-A tag
resolved and were ancestors of the checkpoint. The read-only upstream clone
was clean at `590c6fd5332acb15f5683ebf392a0d7ce54983c5`; its
`ACPT_Timescape.ipynb` SHA-256 was
`86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a`.

Primary classification: `NUMERICALLY_CORROBORATED` (direct Git and hash
checks).

## 4. Frozen inputs

The following files were read completely at the checkpoint:

| Frozen evidence | Exact repository path | Role here |
|---|---|---|
| Phase 1E-A audit and inventory | `reports/phase1e_a_dressed_observable_bridge_audit.md`; `reports/phase1e_a_dressed_observable_bridge_inventory.json` | Previous NO-GO boundary and source trail |
| Phase 1D-C audit and inventory | `reports/phase1d_c_observable_closure_audit.md`; `reports/phase1d_c_closure_inventory.json` | Observable-closure conditions |
| Phase 1D-D-t audit and inventory | `reports/phase1d_d_t_d3_frame_mapping_audit.md`; `reports/phase1d_d_t_d3_frame_mapping_inventory.json` | Covariant frame dictionary and resolved D3 equation verdict |
| Candidate A validation | `reports/phase1d_d_anchored_density_growth_validation.md` | Frozen conditional diagnostic |
| Phase 1D-A audit and inventory | `reports/phase1d_a_growth_observable_audit.md`; `reports/phase1d_a_observable_inventory.json` | Density, harmonic, normalization, and \(\sigma_8\) meanings |
| Phase 1D-B validation | `reports/phase1d_b_growth_pipeline_validation.md` | Signed growth, rates, references, crossings |
| Background implementation | `src/timescape_fsigma8/background/{parameters,tracker,observables,effective_fluid}.py` | \(a_D,a_{\rm obs},\gamma_w,H_D,H,z\) |
| Perturbation implementation | `src/timescape_fsigma8/perturbations/{systems,barotropic,scenarios,solver,initial_conditions}.py` | State meanings and scientific boundaries |
| Growth implementation | `src/timescape_fsigma8/growth/{scenarios,histories,rates,mapping,pipeline,crossings,anchored_diagnostic}.py` | Candidate A and exact density-rate chain |

The immutable inputs retained here are: Candidate A is not observational
\(f\sigma_8\); its bare/dressed relation is only a background density-
derivative coordinate transformation; \(Z\) is a dust-frame
expansion-gradient harmonic coefficient; no global \(k_{\rm code}\) to
dressed observational Fourier map, dust-to-wall-to-tracer velocity transfer,
or dressed redshift-space Jacobian exists; the D3 equation-level verdict is
`RESOLVED_DERIVED_4_10` while both runtime branches remain mandatory; and the
Mészáros system remains comparison-only and formally inapplicable to
Timescape.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE` for the frozen-paper
meanings, with frozen repository files providing provenance rather than new
scientific authority.

## 5. Primary-source inventory

Only primary sources carry load-bearing claims. Born-digital PDFs were read
using text solely for navigation and rendered pages for equations. The DBE
and BDE journal scans were rendered and visually inspected; OCR was not used
as authority for signs, indices, dots, or superscripts.

| ID and citation | Access, version, SHA-256 | Inspected pages/equations | Outcome |
|---|---|---|---|
| GM: Galoppo & Mourier, arXiv:2511.17160v2, JCAP 02 (2026) 066 | arXiv v2 PDF; frozen hash `856bd78db8f86e46c0f5d21414ad0c1d136b176c6ac1b45418dbeebc38e920dd` | Eqs. (2.2), (2.5), (2.19)–(2.24), (4.1)–(4.17), (4.19), (4.20)–(4.29), Sec. 5 and footnotes 7–8 | Defines dust-foliation CGI perturbations and background dressed clock/redshift, but no wall perturbation or RSD map |
| Wiltshire 2007, *Exact solution to the averaging problem in cosmology*, arXiv:0709.0732v2 | arXiv v2 PDF; `3abcc64ad95b95cf655f687515c8d85f38d6d0bfcebec1e0133a460b425db04f` | Eqs. (1)–(8), (19)–(22) | Background lapse, dressed scale, Hubble, and redshift only |
| Wiltshire 2009 (W09), *Average observational quantities in the timescape cosmology*, arXiv:0909.0749v2, PRD 80, 123512 | arXiv v2 PDF; `e37321e9d6021c6f5eb6bc5084ad331f4fca9dc0bc426097d1c5ce5ce7b2a8aa` | Eqs. (11)–(14), (22)–(28), (36)–(38), (51), Appendix B; rendered PDF pp. 4–8, 14 | Background dressed metric, radial-null matching, lapse, Hubble, redshift, distances, and background AP function; explicitly spherically symmetric rather than homogeneous |
| DBE: Dunsby, Bruni & Ellis, *Covariant perturbations in a multifluid cosmological medium*, ApJ 395 (1992) 54 | NASA ADS journal PDF; `3a082920b358872ec64a3706001e1a10a61a51f2e5140cf29662aa1a04b72f20` | journal pp. 56–60; Eqs. (14), (15), (18)–(21), (25)–(34), (42)–(55) | First-order frame boosts and component CGI equations; no wall-observer identification |
| BDE: Bruni, Dunsby & Ellis, *Cosmological perturbations and the physical meaning of gauge-invariant variables*, ApJ 395 (1992) 34 | NASA ADS journal PDF; `eaa273fa5982689cd55eaba7530103e8e9d77199d4b34d3d173c1e9201075b6c` | journal pp. 38–45; Eqs. (14)–(16), (24)–(29), (40), (44)–(48), (61), (63), (74), footnotes 14–15 and 21–22 | First-order frame/gauge meanings and harmonic Laplacian convention |
| Challinor & Lewis (CL), *The linear power spectrum of observed source number counts*, arXiv:1105.5292v2, PRD 84, 043516 | official arXiv born-digital PDF viewed in-session; not saved locally, so local hash is `null` | PDF pp. 2–6; Eqs. (1)–(18), (25), (30), (37), (39) | Exact redshift/Jacobi/source-count definitions and complete linear almost-FLRW number counts |
| Bonvin & Durrer (BD), *What galaxy surveys really measure*, arXiv:1105.5280v3, PRD 84, 063505 | official arXiv born-digital PDF viewed in-session; not saved locally, so local hash is `null` | PDF pp. 2–4, 8–10; Eqs. (5)–(17), (29)–(31), (37) | Independent observed-redshift and volume-distortion route |
| Kaiser, *Clustering in real space and in redshift space*, MNRAS 227 (1987) 1–21 | primary ADS scan; no reproducible local hash | journal pp. 7–9, Sec. 3.1, Eqs. (3.1)–(3.8) | Standard limiting comparison only |
| Percival & White, *Testing Cosmological Structure Formation using Redshift-Space Distortions*, arXiv:0808.0003v2 | arXiv v2 PDF; `99be19eb2893b1b7936563e9189cd0e47839b6a35f285bfc612b6feb122b9adc` | pp. 2–4, Eqs. (1)–(14), (20)–(21) | Explicit plane-parallel FLRW position map, Jacobian, velocity and bias assumptions |
| Nazer & Wiltshire, *Cosmic microwave background anisotropies in the timescape cosmology*, arXiv:1410.3470v3 | official arXiv abstract and primary PDF scope inspected; no local file retained | abstract, methodology statements on matching standard perturbation codes | Does not define a late-time perturbed dressed wall/RSD bridge |

Searches for primary Timescape papers on perturbed wall geometry, regional
lapse perturbations, finite-infinity peculiar velocities, dressed redshift
perturbations, galaxy number counts, and RSD found no source that closes the
required arrows. No load-bearing source was inaccessible. The Kaiser scan was
legible through ADS but not retained as a reproducibly hashed local file;
Percival–White provides an independently accessible statement of the limiting
Jacobian. This access limitation is non-blocking for the no-go result.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 6. Dressed-geometry status

| Object | Status | Evidence and consequence |
|---|---|---|
| Background wall lapse \(\gamma_w=dt/d\tau_w\) | explicitly defined | W09 Eqs. (11)–(14); converts background clocks only |
| Background dressed scale factor \(a_w=a_D/\gamma_w\), rescaled observationally as \(a_{\rm obs}=a_w/a_{w0}\) | explicitly defined | W09 Eqs. (24)–(28), (36)–(38) |
| Background dressed metric \(ds_w^2=-d\tau_w^2+a_w^2[d\bar\eta^2+r_w^2(\bar\eta,\tau_w)d\Omega^2]\) | explicitly defined | W09 Eqs. (24)–(26), constructed by conformal radial-null matching |
| Background dressed Hubble rate \(H=\gamma_w H_D-\dot\gamma_w\) | explicitly defined | W09 Eq. (28); dot is \(d/dt\) |
| Perturbed dressed metric | not defined | new scalar/vector/tensor dynamics and matching are required |
| Perturbative lapse \(\delta\gamma_w\) | not defined | cannot be inferred from the background \(\gamma_w(t)\) |
| Perturbed areal radius or radial coordinate | not defined | background \(r_w\) cannot supply its perturbation |
| Wall-frame scalar/vector/tensor perturbations | not defined | a new perturbative dressed construction is required |
| Wall-observer tetrad | derivable only for the background | pointwise tetrad below; perturbations require a perturbed metric |
| Buchert-slice to wall spatial-hypersurface map | not defined | background radial-null conformal matching is not a spatial diffeomorphism |

The absence is structural: a background lapse is a zeroth-order scalar and
cannot replace a first-order lapse perturbation, boost, or spatial map.
Writing an ansatz for any missing field would introduce new dynamics rather
than derive a Timescape prediction.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 7. Complete frame dictionary

| Frame/construction | Four-velocity, clock and derivative | Spatial structure and variables | Known relations / missing relations |
|---|---|---|---|
| Dust energy frame | \(u_d^a\), volume-average time \(t\), \(\dot{}=u_d^a\nabla_a\) | \(h^d_{ab}=g_{ab}+u^d_a u^d_b\); CGI \(\Delta_d,Z\); geodesic dust | GM/DBE equations known; equals the Buchert foliation in the frozen interpretation |
| Buchert averaging foliation | hypersurfaces orthogonal to dust in the adopted irrotational-dust model | domain average and \(a_D,H_D,\Theta=3H_D\) | background domain variables known; no local wall spatial map |
| Volume-average background | effective FLRW-like average metric and time \(t\) | harmonic label \(k_{\rm code}\), \(k_{\rm com,D}=k_{\rm code}H_{0,\rm TS}/c\) | solver frame only; no observational Fourier identification |
| Wall observer | background \(u_w^a\) with proper time \(\tau_w\) implicit in W09; \(dt=\gamma_w d\tau_w\) | dressed radial-null geometry; local wall density/velocity perturbations absent | background clock/redshift known; \(u_d\to u_w\) perturbative boost unknown |
| Local dressed tetrad | background orthonormal frame built from W09 metric | pointwise line of sight and tangent-space wave covector | exact at a point for the background; finite-patch use requires local/WKB approximation |
| Source/tracer frame | source four-velocity \(u_s^a\) in CL Eq. (1) | source density, evolution, selection, and velocity | operationally defined in general; no Timescape map from dust or wall frame |
| Galaxy frame | tracer rest frame | galaxy density and peculiar velocity | needs density bias and velocity-bias/dynamical prescription |
| Observed-redshift coordinates | observer tetrad, photon direction and measured \(z\) | sky angle, redshift, Jacobi map, observed volume element | generally covariant formula known; Timescape perturbative inputs missing |
| Survey fiducial coordinates | selected FLRW \(H_{\rm fid},D_{A,\rm fid}\) | catalogue \(k,\mu\), separations and AP scalings | survey convention, not a physical Timescape frame |

At first order, DBE/BDE frame transformations can be written only after two
admissible observers in a common perturbed spacetime are specified. With
\(\xi^a=u_{\rm destination}^a-u_{\rm source}^a\), one has, schematically,
\(\Theta_{\rm destination}=\Theta_{\rm source}+D_a\xi^a\) at first order.
The frozen theory does not provide the required \(\xi^a_{d\to w}\).

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 8. Local-coordinate strategy

For the **background** W09 dressed metric an orthonormal coframe is

\[
 \vartheta^{\hat{0}}=d\tau_w,\quad
 \vartheta^{\hat{r}}=a_w\,d\bar\eta,\quad
 \vartheta^{\hat{\theta}}=a_w r_w\,d\theta,\quad
 \vartheta^{\hat{\phi}}=a_w r_w\sin\theta\,d\phi .
\]

Direct substitution gives
\[
 ds^2=-(\vartheta^{\hat{0}})^2
 +(\vartheta^{\hat{r}})^2
 +(\vartheta^{\hat{\theta}})^2
 +(\vartheta^{\hat{\phi}})^2 .
\]
This supplies an exact pointwise local line of sight and a tangent-space
covector \(k_{\hat{i}}\). A patchwise
\(k_{\rm local,w}\), \(k_\parallel\), \(k_\perp\), and
\(\mu=k_\parallel/|\boldsymbol k|\) require a short-wave/locally planar
approximation, with wavelength much smaller than background-curvature,
inhomogeneity, and patch scales. This does not create a map from the global
volume-average harmonic label \(k_{\rm code}\).

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS` for the
pointwise tetrad; `CONVENTION_DEPENDENT` for the finite-patch WKB extension.

## 9. Dust-to-wall transformation

A formal first-order boost may be written
\(u_w^a=u_d^a+\xi_{dw}^a\), with \(u_{da}\xi_{dw}^a=0\). DBE/BDE then imply
coefficient inventories such as

\[
 \delta\Theta_w=\delta\Theta_d+D_a\xi_{dw}^a,
 \qquad
 D_a\rho\big|_w=D_a\rho\big|_d+\dot{\bar\rho}\,\xi^{dw}_a,
\]

With the fixed source-to-destination convention above, the sign is
unambiguous. Using \(\dot{\bar\rho}=-\Theta(\bar\rho+\bar p)\), the plus-
\(\dot{\bar\rho}\) form is equivalent to the normalized shift
\(\mathcal D_a^{(w)}=\mathcal D_a^{(d)}-a\Theta(1+w)\xi_a\), in agreement
with the frozen Phase 1D-D-t frame transformation. These equations show
exactly what must be supplied; they do not determine \(\xi_{dw}^a\). W09's
\(dt=\gamma_w d\tau_w\) fixes only the background clock
rate and neither fixes the spatial boost nor a perturbation
\(\delta\gamma_w\). No coefficient can be evaluated without a common
perturbed spacetime and a wall four-velocity field.

Arrow status: `REQUIRES_NEW_DYNAMICAL_INPUT`.
Primary classification: `NOT_JUSTIFIED`.

## 10. Density transformation

Within the solver harmonic convention,

\[
 {}^{(3)}\nabla^2 Q_k=-{k_{\rm code}^2\over a_D^2}Q_k,
 \qquad
 \Delta_{d,k}=-k_{\rm code}^2\delta_{m,k}.
\]

This exactly recovers the volume-average dust density coefficient for a
fixed nonzero harmonic label. A wall-frame density requires both the
first-order boost term above and a spatial-coordinate/tetrad pullback. Since
neither \(\xi_{dw}^a\) nor the spatial map is supplied, \(\Delta_d\) cannot
be mapped to a local dressed density field. Constant harmonic factors cancel
from same-mode relative growth, but that algebraic cancellation does not
identify the local field or smoothing convention.

Arrow \(\Delta_d\to\delta_{m,d}\): `EXACTLY_DERIVED`.
Arrow \(\delta_{m,d}\to\delta_{m,w}\):
`REQUIRES_NEW_DYNAMICAL_INPUT`.
Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS` for the first
arrow and `NOT_JUSTIFIED` for the second.

## 11. Expansion and velocity transformation

The frozen dust identities are

\[
 Z_k=-k_{\rm code}^2\,\delta\Theta_{d,k},\qquad
 \dot\Delta_{d,k}+Z_k=0,
 \qquad \dot\delta_{m,k}=-\delta\Theta_{d,k}.
\]

Thus \(Z\) fixes the scalar coefficient of the dust congruence expansion
perturbation. It does not by itself fix a three-velocity. In an almost-FLRW
scalar chart, a direct expansion gives

\[
 \delta\Theta_n=-3\dot\psi-3H\phi+{1\over a}\partial_i v_n^i,
 \quad
 \partial_i v_n^i-a\delta\Theta_n=3a(\dot\psi+H\phi).
\]

Therefore a velocity-divergence identification additionally needs the frame,
metric potentials/lapse, spatial coordinates, and a velocity convention.
For the wall frame there is also
\(\delta\Theta_w=\delta\Theta_d+D_a\xi_{dw}^a\). No line-of-sight projection
or radial derivative follows from the scalar divergence alone.

Arrow \(Z\to\delta\Theta_d\): `EXACTLY_DERIVED`.
Arrow \(Z\to\partial_\parallel v_{\parallel,w}\):
`REQUIRES_NEW_DYNAMICAL_INPUT`.
Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 12. Observed-redshift derivation

The covariant starting point is CL Eq. (1), also BD Eq. (5),

\[
 1+z_{\rm obs}={(k_a u_s^a)_s\over(k_a u_o^a)_o}.
\]

For the almost-FLRW scalar metric used by CL, their Eq. (13) separates the
first-order result into source and observer Doppler terms, local source and
observer metric terms, and the integral of time-varying potentials along the
null ray. The source time/radial displacement then follows from CL Eqs.
(14)–(15). BD Eqs. (6)–(7) give the same covariant content in their own line-
of-sight convention.

This derivation is exact at first order **given** a perturbed metric,
specified source and observer four-velocities, and a null geodesic. The
background W09 redshift \(1+z=a_{w0}/a_w\) contains none of the required
perturbations. Substituting it for CL Eq. (13) would discard precisely the
Doppler, metric, lapse, and integrated terms being audited.

Generic arrow to \(z_{\rm obs}\): `EXACTLY_DERIVED`.
Timescape specialization: `REQUIRES_NEW_DYNAMICAL_INPUT`.
Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 13. Null-geodesic and integrated terms

The inventory required by CL Eqs. (13)–(18), (25), and (30), corroborated by
BD Eqs. (29)–(31), is:

1. source and observer line-of-sight Doppler terms;
2. local gravitational/time-slicing terms at source and observer;
3. integrated potential evolution (ISW-type) terms;
4. radial/time-delay and source-position perturbations;
5. the Jacobi-map determinant and lensing convergence;
6. radial velocity-gradient/RSD terms;
7. source-evolution, selection, and magnification terms for an actual sample;
8. observer monopole/dipole terms required by the chosen observable.

The sign of the displayed radial velocity term differs between CL Eq. (30)
and BD Eq. (31) because their radial-direction/velocity conventions differ;
the underlying covariant photon-energy formula agrees. None of these terms
can be assigned a Timescape value without the missing perturbative dressed
geometry and source/observer transfer.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 14. Local spatial mapping

The pointwise dressed tetrad in Sec. 8 defines local physical components.
A local Fourier/WKB treatment additionally assumes a patch small enough that
the tetrad and coefficients vary negligibly and a wavelength short enough
for a local plane wave. Its local volume element is the tetrad/metric volume
element; its line of sight is observer centered. A survey-wide Fourier
coordinate, by contrast, requires a distance–redshift map and fiducial
coordinate assignment.

No primary Timescape source supplies the spatial Jacobian between Buchert
volume-average slices and W09 wall hypersurfaces. W09 Eqs. (24)–(26) match
radial null geometries conformally and do not establish a global spatial
diffeomorphism. Hence neither \(k_{\rm code}\to k_{\rm local,w}\) nor
\(k_{\rm code}\to k_{\rm com,obs}\) is derived. A WKB label can be defined
locally but cannot be populated from the solver mode without new input.

Arrow status: `NOT_MAPPABLE_WITH_CURRENT_THEORY`.
Primary classification: `NOT_JUSTIFIED`.

## 15. Real-to-redshift-space mapping

In a fully specified spacetime, the observed source position follows from
the photon map, redshift, and observer tetrad—not solely from a radial
peculiar velocity. CL Eqs. (2)–(4) give the exact Jacobi/source-count
relation, while Eqs. (25) and (30) give its first-order almost-FLRW
specialization. The observed density therefore contains the radial velocity
gradient plus lensing, metric, integrated, source-evolution, and selection
terms.

Percival–White Eqs. (1)–(6) recover the familiar local plane-parallel map
only after choosing a common FLRW real-space coordinate, a Hubble-velocity
unit, an irrotational velocity, and a distant observer. Those assumptions are
a limiting model, not a derivation from the W09 background metric.

Timescape arrow from local real-space tracer field to observed redshift
space: `REQUIRES_NEW_DYNAMICAL_INPUT`.
Primary classification: `NOT_JUSTIFIED`.

## 16. Jacobian derivation

For a declared local FLRW limit and the sign convention
\(s_\parallel=x_\parallel+v_\parallel/(aH)\), number conservation gives

\[
 (1+\delta_s)d^3s=(1+\delta_g)d^3x,
 \qquad
 \delta_s=\delta_g-{1\over aH}\partial_\parallel v_\parallel
\]

at first order. This is the local part of the CL/BD radial distortion term.
The complete observed-count Jacobian adds the terms catalogued in Sec. 13.
The exact denominator in CL is the conformal expansion
\(\mathcal H=aH\) in its almost-FLRW coordinates; Percival–White absorbs
the Hubble conversion into its velocity variable. In a future dressed
construction the natural background candidate is the local dressed \(H\),
but that choice is not established until the wall perturbation, spatial map,
and photon mapping are derived. \(H_D\), dressed \(H\), and survey
\(H_{\rm fid}\) are not interchangeable.

The W09 background alone therefore produces no Timescape perturbative
Jacobian. The answer to “what Jacobian is obtained?” is: the general
covariant CL determinant and its conditional almost-FLRW limit are known;
no dressed Timescape coefficient inventory can yet be evaluated.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS` for the
conditional limit and `NOT_JUSTIFIED` for a Timescape specialization.

## 17. Relation of Z to velocity

\(Z\) determines \(\delta\Theta_d\), the perturbation of the covariant dust
expansion scalar, after harmonic inversion. It determines a coordinate
three-velocity divergence only after metric/lapse terms and frame are fixed.
Even a known divergence would not determine a line-of-sight derivative
without scalar/irrotationality assumptions, boundary conditions, and a local
spatial Fourier map. It determines neither the wall-frame velocity nor the
galaxy velocity without \(\xi_{dw}^a\) and a tracer prescription.

There is therefore no justified identity
\(Z\equiv\theta_{\rm RSD}\), nor does the background chain
\(f_{\rm dressed}/f_{\rm bare}=\gamma_wH_D/H\) supply one.

Arrow status: `REQUIRES_NEW_DYNAMICAL_INPUT`.
Primary classification: `NOT_JUSTIFIED`.

## 18. Tracer and velocity-bias dependencies

The dust-to-tracer step requires at least: a rule selecting which matter
component galaxies trace; a density-bias relation; a velocity-bias relation
or dynamical proof of shared geodesics; stochastic/noise terms; and the
sample's evolution/selection definition. Percival–White's Kaiser reduction
uses deterministic linear density bias and zero velocity bias; it explicitly
distinguishes these assumptions from the coordinate Jacobian. Neither follows
from Candidate A or from a Buchert domain average.

Arrow wall matter \(\to\) galaxy/tracer velocity:
`REQUIRES_EMPIRICAL_TRACER_ASSUMPTION`.
Primary classification: `UNRESOLVED_EXTERNAL_DEPENDENCY`.

## 19. Hubble and scale-factor normalization

The frozen density rates satisfy

\[
 f_{\rm bare}={d\ln G\over d\ln a_D},\qquad
 f_{\rm dressed}={d\ln G\over d\ln a_{\rm obs}},\qquad
 {f_{\rm dressed}\over f_{\rm bare}}
 ={\gamma_wH_D\over H}
 ={(2+f_v)^2\over4+f_v+4f_v^2}.
\]

Here \(a_{\rm obs}=a_w/a_{w0}\), \(dt=\gamma_wd\tau_w\), and
\(H=(1/a_w)da_w/d\tau_w=\gamma_wH_D-\dot\gamma_w\). This is exact for the
background density derivative. It does not transform a velocity field,
project a line of sight, or provide an RSD denominator.

CL uses \(\mathcal H\) associated with its perturbed almost-FLRW metric;
the local FLRW physical form uses \(aH\); Percival–White's velocity is in
Hubble-velocity units; and a survey fiducial \(H_{\rm fid}\) only assigns
coordinates/AP scalings. Which quantity normalizes a dressed Timescape
velocity divergence remains unresolved until the dressed perturbation and
Jacobian are derived.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 20. Gauge and covariance audit

The dust CGI gradients vanish in the background and are first-order
gauge-invariant in their specified dust frame. This does not make them
observed light-cone scalars. DBE/BDE boosts show their frame dependence when
the observer is changed. Conversely, the observed redshift and complete
observed number count are covariant/gauge-invariant constructions when all
source, observer, displacement, volume, and selection terms are retained.
Selecting only a coordinate density or radial velocity term generally
restores gauge dependence.

The local tetrad is covariant pointwise once the metric and observer are
given. A finite-patch Fourier transform introduces coordinate and WKB
conventions. No gauge choice can manufacture the absent perturbed dressed
metric or dust-to-wall four-velocity.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 21. FLRW and other limits

| Check | Result | What it does not prove |
|---|---|---|
| FLRW limit | CL/BD reduce to standard linear light-cone expressions; Percival–White/Kaiser follows after their assumptions | Timescape mapping away from FLRW |
| \(\gamma_w\to1\) | background bare/dressed clocks and rate chain coincide | perturbative wall/dust frames coincide without specifying \(\xi_{dw}\) |
| zero lapse perturbation | removes one missing class of terms by assumption | existence or smallness of the omitted perturbation |
| zero peculiar velocity | removes Doppler and radial-velocity gradient | metric, lensing, integrated, volume, and selection terms |
| homogeneous local spatial limit | background tetrad approaches a homogeneous local chart | global \(k_{\rm code}\) mapping |
| distant-observer/plane-parallel | defines a fixed line of sight and \(\mu\) locally | wide-angle/light-cone validity |
| zero metric perturbation | gives \(\delta\Theta=(1/a)\nabla\cdot v\) in the matched scalar chart | dust-to-wall/tracer equality |
| matched-frame and matched-unit | constant harmonic/unit factors cancel in relative growth | absolute density, smoothing, tracer, and observational identification |

The Kaiser form is recovered only with: an FLRW/local-flat perturbative
metric; common real/redshift spatial coordinates; a plane-parallel line of
sight; irrotational scalar velocity; number conservation; negligible
metric/lensing/integrated/selection terms on the adopted scales; the linear
continuity equation in the same frame and clock; deterministic linear density
bias; zero velocity bias; and matched normalization/units. The limit is a
consistency check, not a Timescape derivation.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 22. Symbolic checks

Exact rational-coefficient algebra was run with Python 3.14.3 standard
library `fractions.Fraction`; SymPy was not installed in the frozen
environment. No script or output was written to the repository.

| ID | Encoded identity and assumptions | Exact residual | Discrimination |
|---|---|---|---|
| S1 | background chain \(f_d/f_b=\gamma_wH_D/H\), plus tracker substitution | every polynomial coefficient `0` | verifies clock chain only |
| S2 | scalar-chart \(\delta\Theta=-3\dot\psi-3H\phi+a^{-1}\partial_i v^i\) | coefficients of \(\partial_i v^i\), \(a\dot\psi\), \(aH\phi\): `0` | proves metric terms obstruct a bare velocity identification |
| S3 | boost \(\delta\Theta_w-\delta\Theta_d-D_a\xi^a=0\) | both coefficients `0` | inventories missing boost, does not determine it |
| S4 | number conservation and \(J=1+\epsilon\) | coefficients of \(\delta\) and \(\epsilon\): `0` | local Jacobian algebra only |
| S5 | S4 plus \(\theta=-f\delta\), plane-parallel scalar mode | coefficients of \(\delta\) and \(f\mu^2\delta\): `0` | conditional Kaiser limit only |
| S6 | dressed background orthonormal coframe | metric coefficients `[-1,1,1,1]`; scale exponents all `0` | verifies pointwise tetrad, not perturbations or a global Fourier map |

Dimensional checks also require \(v_\parallel/(aH)\) to have length and
\((aH)^{-1}\partial_\parallel v_\parallel\) to be dimensionless in the
local FLRW convention. The exact zero residuals prove only the displayed
identities and assumptions; they cannot supply missing fields.

Primary classification: `SYMBOLICALLY_VERIFIED`.

## 23. Arrow-by-arrow bridge matrix

| Arrow | Status | Decisive reason |
|---|---|---|
| \((\Delta_d,Z)\to(\delta_{m,d},\delta\Theta_d)\) | `EXACTLY_DERIVED` | frozen harmonic definitions and \(\dot\Delta_d+Z=0\) |
| W09 background metric \(\to\) pointwise wall tetrad/line of sight | `EXACTLY_DERIVED` | direct orthonormal-coframe construction |
| pointwise tetrad \(\to(k_{\rm local,w},\mu)\) over a patch | `DERIVED_UNDER_EXPLICIT_APPROXIMATIONS` | WKB/local-flat/plane-parallel assumptions |
| \(k_{\rm code}\to k_{\rm local,w}\) | `NOT_MAPPABLE_WITH_CURRENT_THEORY` | no spatial Jacobian between foliations |
| \((\delta_{m,d},\delta\Theta_d)\to(\delta_{m,w},v_w)\) | `REQUIRES_NEW_DYNAMICAL_INPUT` | absent \(u_w^a\), \(\xi_{dw}^a\), perturbed metric/lapse and spatial map |
| \(Z\to\partial_\parallel v_{\parallel,w}\) | `REQUIRES_NEW_DYNAMICAL_INPUT` | expansion includes metric/boost terms and does not fix LOS derivative |
| wall matter velocity \(\to\) tracer velocity | `REQUIRES_EMPIRICAL_TRACER_ASSUMPTION` | velocity bias and tracer dynamics absent |
| specified perturbed spacetime/source/observer \(\to z_{\rm obs}\) and counts | `EXACTLY_DERIVED` | CL Eqs. (1)–(4), (13), (25), (30); BD corroboration |
| frozen Timescape fields \(\to z_{\rm obs}\)/observed-count Jacobian | `REQUIRES_NEW_DYNAMICAL_INPUT` | required perturbative dressed inputs absent |
| declared FLRW local limit \(\to\) Kaiser form | `DERIVED_UNDER_EXPLICIT_APPROXIMATIONS` | full assumption list in Sec. 21 |
| \(Q_{\rm anchor,dressed}\to\) observed velocity amplitude/\(f\sigma_8\) | `NOT_MAPPABLE_WITH_CURRENT_THEORY` | density clock chain is not a velocity/light-cone/tracer bridge |

No arrow is upgraded by a background lapse alone.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 24. Exact answers to the twenty completion questions

1. **Perturbed dressed metric?** No; only the W09 background dressed metric is available.
2. **Perturbative wall lapse?** No; only \(\gamma_w(t)\) is defined.
3. **Can \(u_d\) be mapped to \(u_w\)?** Not from frozen theory; \(\xi_{dw}^a\) is new dynamical input.
4. **Can \(\Delta_d\) map to local dressed density?** It maps exactly to volume-average \(\delta_{m,d}\), not to wall density.
5. **Can \(Z\) map to local velocity divergence?** It maps to dust \(\delta\Theta_d\), not generally to a wall coordinate divergence.
6. **Can \(Z\) determine a LOS velocity derivative?** No; spatial map, metric/boost terms, scalar velocity reconstruction, and boundary data are missing.
7. **Is local \(k,\mu\) available?** Pointwise in the background tetrad; patchwise only under WKB/plane-parallel assumptions; no \(k_{\rm code}\) map.
8. **Real-to-observed-redshift map derived?** General covariant form yes; Timescape specialization no.
9. **What Jacobian is obtained?** CL's exact Jacobi/source-count determinant and its conditional almost-FLRW linear form; no evaluated Timescape perturbative determinant.
10. **Which Hubble rate enters?** \(\mathcal H\) for the CL almost-FLRW formula or \(aH\) in its physical local form; a dressed Timescape choice is unproved, while \(H_D\) and \(H_{\rm fid}\) cannot be silently substituted.
11. **Which extra terms survive?** Doppler, local potentials/lapse, integrated potentials, radial/time displacements, lensing, observer, evolution, selection, and magnification terms unless explicitly approximated away.
12. **Dressed Kaiser form?** No.
13. **If conditional, under what assumptions?** Exactly the FLRW/local-flat, common-frame, plane-parallel, scalar-irrotational, linear-continuity, zero-velocity-bias, deterministic-density-bias, matched-unit/normalization, and negligible-extra-term conditions in Sec. 21.
14. **Which growth combination appears?** Standard \(f\) only in that conditional FLRW continuity model; frozen theory establishes neither \(f_{\rm bare}\) nor \(f_{\rm dressed}\) as the dressed velocity coefficient.
15. **Is \(Q_{\rm anchor,dressed}\) the velocity amplitude?** No; it remains an externally normalized density-derivative diagnostic.
16. **Tracer model required?** Yes, including density and velocity bias/dynamics.
17. **Matched observational \(\sigma_8\) convention required?** Yes; Candidate A's external anchor does not establish the wall/survey frame, \(R_8\), or spectrum convention.
18. **May an observable API now be implemented?** No.
19. **May compressed survey \(f\sigma_8\) points be reused?** No; the bridge is absent and a future analysis would at least require a derived map and likely survey-level reanalysis.
20. **Minimal next phase?** A report-only perturbed dressed geometry and dust-to-wall transfer closure derivation, before any RSD implementation.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 25. Permitted and forbidden future implementation

The only scientifically permitted next scope is **Phase 1E-C — Perturbed
dressed geometry and dust-to-wall transfer closure derivation**. It must
either derive, from explicit field/matching equations, a perturbed wall
metric, lapse, wall four-velocity, common spatial map, and photon transfer,
or prove that further fundamental input is required. It remains a theoretical
derivation phase. It may use the CL/BD observable equations as target
coefficient inventories and must validate covariance, gauge behavior,
dimensions, and FLRW limits.

Forbidden interpretations and implementations remain: no public RSD or
Kaiser API; no public observational \(f\sigma_8\); no power spectrum,
\(\sigma_R\), or \(\sigma_8\) integration; no bias/AP/survey adapter,
dataset, covariance, likelihood, fit, or inference; no \(k_{\rm code}\) to
observational \(k\) conversion by assumption; no silent FLRW, zero velocity-
bias, deterministic-bias, or negligible-light-cone assumptions; no relabeling
of Candidate A; no Mészáros physical interpretation; and no D3 runtime
default or branch change.

Primary classification: `NOT_JUSTIFIED` for any observable implementation.

## 26. Overall E1–E4-equivalent verdict

The four decisive criteria are:

| Criterion | Result |
|---|---|
| E1: local dressed perturbed geometry and observer | **not met**: background only |
| E2: dust-to-wall density/velocity and spatial transfer | **not met**: new dynamics required |
| E3: observed-redshift/null-geodesic/Jacobian formalism | **partly met**: general covariant formalism known, Timescape inputs absent |
| E4: tracer, smoothing, and survey identification | **not met**: empirical and survey dependencies remain |

Accordingly the strongest supported token is
`PARTIAL_BRIDGE_NEW_DYNAMICS_REQUIRED`. It is not
`CONDITIONAL_LOCAL_DRESSED_BRIDGE_DERIVED`: the missing wall perturbations
are not merely conventions or optional approximations. It is stronger than
`NOT_DERIVABLE_FROM_FROZEN_THEORY` only in the precise sense that the
dust-frame subchain, background wall tetrad, and general observed-light-cone
formalism are rigorously available; the full central bridge is not.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 27. Unresolved dependencies

Resolution requires, at minimum:

1. dynamical equations and matching conditions for a perturbed dressed wall
   metric, including scalar/vector/tensor content and \(\delta\gamma_w\);
2. explicit \(u_w^a\), \(\xi_{dw}^a\), and wall acceleration in a common
   perturbed spacetime;
3. a spatial/tetrad map from Buchert dust slices/modes to a controlled local
   wall patch, with units and validity domain;
4. null-geodesic and Jacobi-map perturbations in that geometry, including
   observer terms and integrated effects;
5. a dust/matter-to-tracer density and velocity prescription;
6. an observational smoothing/frame convention and later a survey-specific
   fiducial/selection treatment.

No accessible primary Timescape source supplied these objects. Whether they
can be uniquely derived within the intended framework, rather than posited,
is an unresolved theoretical dependency; authorial intent is not used as a
substitute and no author was contacted.

Primary classification: `UNRESOLVED_EXTERNAL_DEPENDENCY`.

## 28. Repository preservation and final test results

Final validation found exactly the two new untracked Phase 1E-B reports and
no pre-existing tracked modification or staged path. JSON parsing,
nine-field conclusion validation, token validation, Markdown/JSON verdict
and source-inventory consistency, deterministic reserialization, UTF-8/LF/
final-newline checks, incomplete-marker/terminology searches, and
`git diff --check` all passed.

The complete unchanged suite was run on the same tracked source tree:

| Environment | Package versions | Result |
|---|---|---|
| Python 3.14.3 | NumPy 2.5.1; SciPy 1.18.0; pytest 9.1.1; pluggy 1.6.0 | 379 passed; 0 failed, skipped, xfailed, or warned |
| Python 3.11.9 | NumPy 2.4.6; SciPy 1.17.1; pytest 9.1.1; pluggy 1.6.0 | 379 passed; 0 failed, skipped, xfailed, or warned |

The upstream clone remained clean at its pinned commit and the notebook hash
remained unchanged. Nothing was staged, committed, tagged, pushed, merged,
published, sent as a pull request, or communicated to an author.

Primary classification: `NUMERICALLY_CORROBORATED`.
