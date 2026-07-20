# Phase 1E-A dressed spatial and redshift-space observable bridge audit

Date of audit: 2026-07-20 (UTC date recorded in the companion inventory).  Frozen repository checkpoint: `7ea266c2cb00aac8afdef71e51a18aea5fb7d39c`.

## 1. Scope and executive scientific verdict

This is an equation-level, report-only audit of whether the frozen Phase 1D-D Candidate A diagnostic can be identified with the parameter conventionally denoted (f\sigma _8) in redshift-space-distortion (RSD) analyses. No observable code, spectrum, data value, likelihood, fit, or public (f\sigma _8) quantity is created.

**Overall primary verdict: `NOT_JUSTIFIED_FOR_OBSERVATIONAL_USE`.**  Candidate A is a valid externally anchored density-growth diagnostic in the volume-average perturbation system. Its dressed version applies an exact tracker background clock/scale-factor chain rule. The audited theory does not provide the perturbative wall/tracer velocity transfer, a common dressed spatial Fourier map, or the real-to-redshift-space Jacobian needed to identify that density derivative with the velocity field fitted by a survey. The existing dressed geometry supplies radial light propagation and background distance-redshift/AP relations, but not this missing perturbative bridge.

Primary classification: `NOT_JUSTIFIED`.

The strongest defensible conditional sub-verdict is an FLRW-like proxy: if all frame, velocity, bias, smoothing, Jacobian, and survey-template assumptions in Sec. 24 are imposed, (Q_{\rm anchor,dressed}) has the same algebraic form as (f\sigma _8). That algebraic resemblance is not a Timescape derivation of the observational identification.

## 2. Repository checkpoint and preservation

The preflight was completed before the work branch was created:

- local and fetched `origin/main` were both `7ea266c2cb00aac8afdef71e51a18aea5fb7d39c`;
- annotated tag `phase-1d-d-anchored-density-growth-v1` had tag object `d42519aff3f6028c8d71eb7ef478b79201e422c3` and peeled to that commit locally and remotely;
- all nine frozen tags named in the phase specification resolved and were ancestors;
- the tracked tree and index were clean and no Git operation was active;
- the pinned upstream clone was clean at `590c6fd5332acb15f5683ebf392a0d7ce54983c5`;
- `ACPT_Timescape.ipynb` had SHA-256 `86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a`;
- `git diff --check` passed;
- Python 3.14.3 and Python 3.11.9 each collected and passed 379 tests with zero failures, skips, xfails, or warnings.

Only after those checks, local unpushed branch `phase-1e-a-dressed-observable-bridge-audit` was created at the checkpoint.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE` (Git objects, local files, and direct test executions are the primary repository evidence).

## 3. Frozen prior results

The following are inputs, not subjects of modification:

- the Phase 1B tracker background and dressed observables;
- the Phase 1C clean/barotropic systems;
- the Phase 1D-B signed-growth pipeline;
- the equation-level D3 verdict `RESOLVED_DERIVED_4_10`, while both `derived_4_10` and `printed_4_15` remain explicit mandatory runtime branches with no default;
- the Phase 1D-C no-go on an already available global volume-average-to-dressed Fourier mapping;
- Candidate A: (G=\Delta_d(t)/\Delta_d(t_{\rm ref})), (A_{\rm anchor}=\sigma_{8,\rm anchor}G), and (Q_{\rm anchor}=fA_{\rm anchor}=\sigma_{8,\rm anchor}dG/d\ln a_{\rm coordinate}).

Candidate A accepts only clean comoving and Mészáros histories; comoving is primary and Mészáros is comparison-only and formally inapplicable to Timescape. It predicts neither its external anchor nor observational (f\sigma _8).

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE` (frozen reports and source at the checkpoint).

## 4. Scientific question and decision criteria

An exact identification requires a continuous chain

\[
\{\Delta_d,Z\}_{\rm volume\ dust}
\longrightarrow \{\delta_m,\boldsymbol v_{\rm dust}\}_{\rm dressed\ spatial}
\longrightarrow \{\delta_g,\boldsymbol v_g\}
\longrightarrow \delta_g^s
\longrightarrow \hbox{the fitted survey amplitude}.
\]

Each arrow must specify frame, time, spatial coordinates, line of sight, Hubble normalization, bias, smoothing, and fiducial conversion. A background chain rule alone cannot establish a perturbative spatial or velocity arrow. An exact GO requires all arrows; a conditional verdict may state every added assumption; otherwise the result is a no-go for observational use.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 5. Primary-source inventory

| Source | Version/access and SHA-256 when locally obtained | Inspected material | Audit role |
|---|---|---|---|
| Galoppo & Mourier (GM), arXiv:2511.17160v2, JCAP 02 (2026) 066 | arXiv PDF, `856bd78db8f86e46c0f5d21414ad0c1d136b176c6ac1b45418dbeebc38e920dd` | Eqs. (2.2), (2.5), (2.19)-(2.24), (4.9), (4.20)-(4.23), (5.4)-(5.7), Secs. 5.1 and 6 | CGI density/expansion variables, dust-frame equations, tracker, and paper-level observable claims |
| Wiltshire, *Average observational quantities in the timescape cosmology*, arXiv:0909.0749v2, PRD 80, 123512 | arXiv PDF, `e37321e9d6021c6f5eb6bc5084ad331f4fca9dc0bc426097d1c5ce5ce7b2a8aa` | Sec. II, Eqs. (22)-(28), Sec. III, Eqs. (36)-(38), Sec. V and Eq. (51), Appendix B | Dressed metric, lapse, Hubble rate, redshift, distance, and Timescape AP function |
| Wiltshire, *Exact solution to the averaging problem in cosmology*, arXiv:0709.0732v2 | arXiv PDF, `3abcc64ad95b95cf655f687515c8d85f38d6d0bfcebec1e0133a460b425db04f` | Eqs. (1)-(8), (19)-(22) | Original tracker clock, dressed geometry, Hubble, and redshift relations |
| Dunsby, Bruni & Ellis, ApJ 395 (1992) 54; Bruni, Dunsby & Ellis, ApJ 395 (1992) 34 | frozen Phase 1D-C/1D-D-t visually audited primary transcriptions | CGI frames, component gradients, harmonic definitions cited in those audits | Meaning of density and expansion gradients; no dressed RSD bridge is supplied |
| Kaiser, *Clustering in real space and in redshift space*, MNRAS 227 (1987) 1 | NASA ADS scan opened in the primary PDF viewer; no reproducible local download hash (direct download timed out) | journal pp. 7-9, Sec. 3.1, Eqs. (3.1)-(3.8) | Original linear real/redshift-space density and power anisotropy |
| Percival & White, *Testing Cosmological Structure Formation using Redshift-Space Distortions*, arXiv:0808.0003v2 | arXiv PDF, `99be19eb2893b1b7936563e9189cd0e47839b6a35f285bfc612b6feb122b9adc` | Secs. 2.1-2.3, Eqs. (1)-(14), Sec. 2.6, Eqs. (20)-(21) | Explicit position map, Jacobian, continuity, bias, velocity bias, and (f\sigma_8) amplitude decomposition |
| Alcock & Paczyński, Nature 281 (1979) 358-359, DOI 10.1038/281358a0 | publisher metadata/abstract inspected; full body blocked by publisher cookie/access and ADS direct download timeout | abstract and bibliographic record only | Original conceptual AP construction; exact modern scaling equations are not attributed to inaccessible text |
| Beutler et al., BOSS DR12 Fourier-space analysis, arXiv:1607.03150v1 | arXiv PDF, `bd0ec6ecb85b4fd015cfbaa2fcf7f19ef94ecda4d2022d327e5dec25e38da742` | Secs. 2, 4, 5, Eqs. (23)-(25), Sec. 5.2 Eqs. (42)-(49), Secs. 5.3, 6, fitting ranges | Representative fitted (f\sigma_8), AP, template, window, nuisance, covariance, and scale-cut dependencies |
| Bautista et al., eBOSS DR16 LRG configuration-space analysis, arXiv:2007.08993v2 | arXiv PDF, `825f25cd55140db25b390ad0947a421aca1c4bc1814eb4301e83931ea0ff9118` | Secs. 2.5, 3.1-3.4, Eqs. (4), (7)-(8), (36)-(42), Sec. 4.2 | Fiducial coordinates/templates, nonlinear RSD models, fitted posterior compression, scale cuts, and explicit (R=8\alpha h^{-1}{\rm Mpc}) convention |
| Alam et al., eBOSS final cosmological implications, arXiv:2007.08991 | arXiv PDF, `b5c04e71129ff94401d472449f43428a86a1d7a9b028312efea32fac0fa0df1e` | methodology/consensus context and likelihood-compression discussion | Cross-survey consensus context; not used for a numerical datum |

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 6. Source-inspection methodology

All local project evidence listed in Sec. 3 was read at the frozen commit. Born-digital PDFs were downloaded into ignored scratch space, hashed, text-extracted only for navigation, and key pages rendered and visually inspected: GM PDF pp. 9, 21, 25, 27; Wiltshire 2009 pp. 6, 8, 14; Percival-White pp. 2-4; BOSS pp. 3, 8-11; eBOSS LRG pp. 6, 8-9, 11-12. Signs and equations were taken from the rendered pages, not OCR. The Kaiser ADS scan was inspected through its primary PDF page view and page transcription. The AP publisher exposed the abstract and metadata but not the body; the exact scaling equations used here are therefore cited to the accessible primary Timescape and survey sources, not reconstructed from the AP abstract.

The inaccessible AP body is non-blocking for the present no-go because the load-bearing negative result follows from the missing Timescape perturbative spatial/velocity map; W09 Eq. (51), BOSS Eqs. (42)-(46), and eBOSS Eqs. (7)-(8) are sufficient to audit what background AP information exists and what surveys fit. A verbatim audit of the two-page original would still improve source completeness.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE`.

## 7. Evidence-classification policy

Every material conclusion uses one primary token from the required vocabulary. Source verification, derivation, symbolic checking, numerical corroboration, convention dependence, and an observational no-go remain separate claims. Symbolic checks prove only encoded equations. Numerical background checks cannot supply a missing frame transformation.

Primary classification: `NOT_APPLICABLE` (policy statement).

## 8. Complete frame and observer dictionary

| Frame/congruence | Definition, clock, scale/expansion | Spatial/perturbative content | Known bridge |
|---|---|---|---|
| Buchert volume-average dust foliation | averaging hypersurfaces; volume time (t), (a_D=\bar a), (H_D=\dot a_D/a_D=\Theta/3) | volume-average spatial derivatives and harmonic label (k_{\rm code}) | identical to the dust energy frame for the frozen perturbation specialization |
| Dust energy frame | (u_d^a), (q_d^a=0), geodesic dust; clock (t) | (D_a^{(d)}), (Z_a=a_D D_a\Theta), scalar (\Delta_d,Z) | GM Eqs. (4.9), (4.20)-(4.23); no wall/tracer transfer |
| Effective-fluid frame | (u_{\rm eff}^a), zero effective flux in its own rest frame | tilt variables (V_{\rm eff}), pressure/density gradients | relevant to barotropic systems only; excluded from Candidate A |
| Wall/dressed observer | finite-infinity observer with proper time (\tau_w), (dt=\gamma_w d\tau_w), (a_{\rm obs}=a_w/a_{w0}), (H=(1/a_w)da_w/d\tau_w) | W09 effective dressed metric and light-cone distances; no audited wall-frame matter perturbation/velocity transfer | background time and radial-null bridge only |
| Redshift observer | central wall observer operationally assigning (1+z=a_{w0}/a_w) along matched radial null geodesics | observed direction and light-cone redshift | W09 Eqs. (36)-(38); no peculiar-redshift perturbation equation |
| Galaxy/tracer rest frame | four-velocity (u_g^a), inferred through galaxy redshift positions | (\delta_g), tracer velocity and bias | absent from GM/Timescape perturbation system |
| Total-matter frame | total material energy or particle frame, depending definition | may differ from dust and tracer frames in a multifluid model | not identified with wall or tracer frame here |
| Survey fiducial FLRW coordinates | algorithmic coordinates obtained from observed angles/redshifts using (D_{A,\rm fid},H_{\rm fid}) | Fourier/correlation bins, LOS (\hat n), (k,\mu), window and selection | survey-specific AP mapping, not a physical Timescape frame transformation |

No source establishes that the dust, wall, galaxy, or fiducial congruences coincide at first perturbative order. Primary classification: `UNRESOLVED_EXTERNAL_DEPENDENCY`.

## 9. Time variables, clocks, lapses, and scale factors

W09 Eqs. (23)-(28) give (dt=\gamma_w d\tau_w), (a_w=a_D/\gamma_w), and

\[
H\equiv {1\over a_w}{da_w\over d\tau_w}=\gamma_w H_D-\dot\gamma_w.
\]

With (a_{\rm obs}=a_w/a_{w0}=1/(1+z)), the frozen chain rule is

\[
{d\ln a_{\rm obs}\over dt}={H\over\gamma_w},\qquad
{f_{\rm dressed}\over f_{\rm bare}}
={\gamma_w H_D\over H}
={(2+f_v)^2\over 4+f_v+4f_v^2}.
\]

This is an exact tracker background identity. It transforms the independent variable of a density derivative; it is not a boost or spatial transformation of a peculiar velocity. Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 10. Spatial coordinates and harmonic labels

The frozen volume-average harmonic convention is

\[
{}^{(3)}\nabla^2Q_k=-{k_{\rm code}^2\over a_D^2}Q_k,
\quad k_{\rm com,D}=k_{\rm code}{H_{0,\rm TS}\over c},
\quad k_{\rm phys,D}(t)={k_{\rm com,D}\over a_D(t)}.
\]

W09 Eq. (26) instead gives an observer-centred dressed metric

\[
ds^2=-d\tau_w^2+a_w^2(\tau_w)
\left[d\bar\eta^2+r_w^2(\bar\eta,\tau_w)d\Omega^2\right],
\]

and explicitly states that it is spherically symmetric but not homogeneous. A global translation-invariant plane-wave basis, hence a single global (k_{\rm com,obs}), does not follow. A local thin-shell/tangent Fourier convention could be introduced only with additional construction and validation.

Primary classification: `NOT_JUSTIFIED`.

## 11. (k_{\rm code}) to observational-scale mapping

No observational spatial scale can presently be assigned uniquely to (k_{\rm code}). W09 Eqs. (36)-(38) provide the light-cone effective comoving distance (D(z)=a_{w0}r_w) and redshift, and Eq. (51) supplies an AP background function. These define radial and transverse background conversions at an observed redshift, not a global off-light-cone Fourier isomorphism from the Buchert averaging slice.

The constant (k_{\rm code}) factor cancels exactly from the same-mode relative density growth:

\[
{[-\Delta_d(t)/k_{\rm code}^2]\over[-\Delta_d(t_{\rm ref})/k_{\rm code}^2]}
={\Delta_d(t)\over\Delta_d(t_{\rm ref})}.
\]

Thus Candidate A's scale-independent (G) does not need the dimensional map. Absolute amplitudes, spectrum/smoothing definitions, survey (k)-bins, (\mu), scale cuts, and the redshift-space Jacobian do need it.

Primary classification for the cancellation: `SYMBOLICALLY_VERIFIED`. Primary classification for the observational map: `UNRESOLVED_EXTERNAL_DEPENDENCY`.

## 12. (R_8) and (h)-convention audit

A standard (\sigma_R) pairs a comoving wavenumber and comoving smoothing radius in the same spatial coordinates. A volume-average (k_{\rm com,D}) could pair only with a volume-average comoving radius. The survey quantity (R_8=8h^{-1}{\rm Mpc}) belongs to its matter-spectrum/fiducial convention. It cannot be assigned automatically to the dressed Timescape (h), the bare (H_{D0}), or a survey-fiducial (h).

The issue is operational, not semantic: eBOSS Sec. 3.2.4, Eq. (36), explicitly computes (\sigma_R) from its fiducial (P_{\rm lin}) and then uses (R=8\alpha h^{-1}{\rm Mpc}) to reduce fiducial dependence. Candidate A merely records the external anchor's smoothing/h/frame metadata. It neither constructs that radius in a dressed slice nor proves equivalence to a survey's convention.

Which (h) defines an observational (R_8) is therefore the (h) attached to the survey/model spectrum definition being fitted; matching it to a Timescape anchor is unresolved. Primary classification: `CONVENTION_DEPENDENT`.

## 13. (\Delta_d,\delta_m,Z,delta\Theta) chain

GM Eqs. (2.2), (2.20)-(2.24), (4.9), and (4.20)-(4.23), with the frozen harmonic sign convention, give

\[
\Delta_{d,k}=-k_{\rm code}^2\delta_{m,k},\qquad
Z_k=-k_{\rm code}^2\delta\Theta_k,\qquad
\dot\Delta_{d,k}+Z_k=0.
\]

For (k_{\rm code}\ne0), substitution gives

\[
\dot\delta_{m,k}=-\delta\Theta_k,
\qquad
f_{\rm bare}={\dot\delta_m\over H_D\delta_m}
=-{\delta\Theta\over H_D\delta_m}
=-{3Z\over\Theta\Delta_d}.
\]

Here (\delta\Theta) is the scalar harmonic coefficient of the perturbation of the dust expansion scalar measured in the volume-average dust frame. It is not, by definition alone, a coordinate divergence of a galaxy velocity.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 14. Dust velocity and tracer velocity

In a single FLRW coordinate frame, linear dust kinematics may yield

\[
\delta\Theta={1\over a}\nabla\!\cdot\boldsymbol v_d,
\]

after specifying the coordinate velocity, scalar sector, slicing, and observer. Under those extra assumptions, Sec. 13 gives the familiar continuity relation. The audited Timescape sources do not derive the corresponding wall-coordinate velocity, do not transform the dust CGI expansion perturbation into the dressed metric, and introduce no galaxy four-velocity.

Equality (\boldsymbol v_g=\boldsymbol v_d) would require galaxies to follow that same dust congruence on the fitted scales and zero velocity bias. Percival-White Secs. 2.2-2.3 and BOSS Sec. 5 explicitly treat this as an assumption; BOSS states (\theta_g=\theta). It is not implied by Candidate A.

Primary classification: `NOT_JUSTIFIED`.

## 15. Hubble-normalised velocity divergence

Three distinct dimensionless objects must not be conflated:

\[
\theta_D:={\delta\Theta\over H_D}=-f_{\rm bare}\delta_m,
\]

which is a dust-frame CGI-derived normalization;

\[
\theta_{\rm clock}:={\gamma_w\delta\Theta\over H}=-f_{\rm dressed}\delta_m,
\]

which follows algebraically if only the derivative clock is changed; and the survey (\theta=\nabla\cdot\boldsymbol u) in Percival-White Eqs. (4)-(6), where (\boldsymbol u) is a galaxy velocity in the survey's Hubble-velocity units and (\theta=-f\delta_m) follows in its FLRW linear model.

The second expression is a useful clock-rescaled candidate, not a demonstrated wall/tracer velocity divergence. (H_D=\Theta/3) normalizes the first; dressed (H) appears in the second; (H_{\rm fid}(z)) converts observed redshifts into a survey's fiducial radial coordinates. No equality among these normalizations is assumed.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS` for the first two algebraic identities; `NOT_JUSTIFIED` for their observational identification.

## 16. Real-space to redshift-space Jacobian

Percival-White Eq. (1), in its stated plane-parallel FLRW convention, writes (\boldsymbol s=\boldsymbol x-u_z\hat{\boldsymbol z}). Number conservation and its exact Jacobian give Eqs. (2)-(3); linearization, irrotationality, and the distant-observer limit give Eqs. (4)-(6),

\[
\delta_g^s(\boldsymbol k)=\delta_g(\boldsymbol k)-\mu^2\theta(\boldsymbol k),
\qquad \theta=-f\delta_m.
\]

To reproduce this in dressed Timescape one would need: a perturbed observed-redshift law; a real-space tracer position in the dressed coordinates; a LOS velocity-to-redshift displacement; the derivative of the dressed radial distance-redshift relation; a 3-Jacobian; a line-of-sight and local plane-parallel limit; and a transfer of dust to tracer density/velocity. W09's background radial-null matching does not supply these perturbative terms. Lapse, spatial-coordinate, light-cone, and relativistic terms therefore cannot be proven absent.

Primary classification: `NOT_JUSTIFIED`.

## 17. Kaiser-form derivation or no-go

Within the explicit FLRW assumptions

\[
\delta_g=b\delta_m,\quad \boldsymbol v_g=\boldsymbol v_m,
\quad \theta=-f\delta_m,
\]

Percival-White Eqs. (5), (6), and (10)-(12) yield

\[
\delta_g^s=(b+f\mu^2)\delta_m,
\qquad P_g^s=(b+f\mu^2)^2P_m.
\]

This also restates the large-scale result of Kaiser Sec. 3.1. The algebra is valid once those assumptions and a common Fourier frame are imposed. The Timescape bridge needed to select (f_{\rm bare}), (f_{\rm dressed}), or another velocity-transfer combination is absent. Therefore no dressed Kaiser formula has been derived, and (F(\mu)=f_{\rm dressed}\mu^2) remains a conditional FLRW-like proxy, not a Timescape result.

Primary classification: `NOT_JUSTIFIED`.

## 18. Power-spectrum and multipole-level implications

Definitional algebra only, with no spectrum evaluated, gives

\[
P_s(k,\mu)=(b+f\mu^2)^2P_m(k),
\]

and Legendre integration gives

\[
P_0=\left(b^2+{2\over3}bf+{1\over5}f^2\right)P_m,
\]
\[
P_2=\left({4\over3}bf+{4\over7}f^2\right)P_m,
\qquad
P_4={8\over35}f^2P_m.
\]

If one common spectrum shape and smoothing convention define amplitudes (b\sigma_8) and (f\sigma_8), the angular amplitude becomes ([b\sigma_8+f\sigma_8\mu^2]^2) times a unit-normalized shape, as in Percival-White Eqs. (13)-(14). This is an algebraic reparameterization. Physical identification still requires a common density field, spatial frame, normalization, and velocity law.

Primary classification: `SYMBOLICALLY_VERIFIED` (SymPy 1.14.0 reproduced all three multipole coefficients exactly).

## 19. Bias and velocity-bias assumptions

Deterministic linear density bias (\delta_g=b\delta_m) corresponds to the (r=1) case of Percival-White Eqs. (9)-(10). Their Eq. (11) additionally assumes no velocity bias. Modern BOSS/eBOSS fits introduce nonlinear bias, stochastic/noise, damping/velocity-dispersion, and other nuisance parameters. The familiar cancellation to a fitted (f\sigma_8) combination is algebraic only after the selected bias/velocity model is adopted.

Candidate A provides no density-bias or velocity-bias prescription. Zero velocity bias and deterministic linear bias are empirical assumptions, not consequences of the Timescape perturbation equations.

Primary classification: `UNRESOLVED_EXTERNAL_DEPENDENCY`.

## 20. Dressed versus bare growth-rate assessment

The exact tracker identity maps the same density history between derivative coordinates:

\[
Q_{\rm anchor,dressed}={\gamma_wH_D\over H}
Q_{\rm anchor,bare}.
\]

Numerical corroboration for the frozen notebook background gives the factor 1.0247547361 at dressed \(z=20\), 1.0578767186 at \(z=10\), 1.1306676738 at \(z=1\), and 1.0841563338 today. Its time dependence shows that it is not a constant amplitude convention. In every case direct evaluation of \(\gamma_wH_D/H\) agreed with \((2+f_v)^2/(4+f_v+4f_v^2)\) to floating-point precision.

This establishes the density-derivative coordinate conversion, not an RSD velocity conversion. Primary classification: `NUMERICALLY_CORROBORATED` for the values; `NOT_JUSTIFIED` for an observational identification.

## 21. Candidate A relation matrix

| Relation | Required relation classification | Finding |
|---|---|---|
| (Q_{\rm anchor,bare}\leftrightarrow Q_{\rm anchor,dressed}) | `IDENTICAL_UNDER_EXPLICIT_ASSUMPTIONS` | exact tracker background chain for the same signed clean history, reference, and external anchor |
| (Q_{\rm anchor,dressed}\leftrightarrow) clock-rescaled dust (\delta\Theta) diagnostic | `IDENTICAL_UNDER_EXPLICIT_ASSUMPTIONS` | exact if density and dust expansion are retained in the same volume-average harmonic mode and only the time coordinate is changed |
| (Q_{\rm anchor,dressed}\leftrightarrow) putative dressed tracer velocity-growth | `NOT_MAPPABLE_WITH_CURRENT_THEORY` | wall perturbation, spatial, and dust-to-tracer velocity transfer are missing |
| (Q_{\rm anchor,dressed}\leftrightarrow) ideal FLRW-like (f\sigma_8) algebra | `PROXY_WITH_CONVENTION_DEPENDENCE` | same form only after all Sec. 24 assumptions |
| (Q_{\rm anchor,dressed}\leftrightarrow) a published survey (f\sigma_8) point | `REQUIRES_SURVEY_REANALYSIS` | AP alone does not replace the missing Timescape forward model; template/nuisance/window/cuts remain |

(A_{\rm anchor}) is an externally normalized density amplitude; neither (A_{\rm anchor}) nor either (Q\) predicts the anchor. Primary classification: `NOT_JUSTIFIED` for observational use.

## 22. Alcock-Paczynski and fiducial-cosmology dependence

BOSS Eqs. (42)-(46) define

\[
\alpha_\parallel={H_{\rm fid}r_{s,\rm fid}\over Hr_s},\qquad
\alpha_\perp={D_A r_{s,\rm fid}\over D_{A,\rm fid}r_s},
\]

with (k'_\parallel=k_\parallel/\alpha_\parallel), (k'_\perp=k_\perp/\alpha_\perp), and volume factor (1/(\alpha_\perp^2\alpha_\parallel)) after the paper's sound-horizon convention is accounted for. eBOSS Eqs. (7)-(8) give the analogous (D_M/r_d,D_H/r_d) definitions. SymPy verified the spatial determinant (\alpha_\perp^2\alpha_\parallel) and reciprocal Fourier-volume determinant.

W09 Eq. (51) supplies a Timescape background AP function from dressed (H(z)) and distance. This is enough to propose background radial/transverse dilation factors for a survey bin. It is not enough to create the missing redshift-space velocity/Jacobian law or a global dressed Fourier field. AP conversion is necessary for fiducial coordinates but not sufficient for observational reuse.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS` for the AP identities; `NOT_JUSTIFIED` for sufficiency.

## 23. Survey-compression taxonomy

Representative primary analyses demonstrate that a reported (f\sigma_8) is a fitted, model-compressed parameter:

- BOSS converts angles/redshifts with a fiducial flat FLRW model, convolves model multipoles with the survey window, fits a TNS density/velocity/bias model, assumes no velocity bias, jointly fits (f\sigma_8,\alpha_\parallel,\alpha_\perp), marginalizes nuisance parameters, uses mock covariance, and imposes distinct (k)-cuts for (P_0,P_2,P_4).
- eBOSS converts to fiducial comoving coordinates, supplies a fiducial CAMB shape, fits TNS and CLPT-GS correlation multipoles with bias/damping parameters and scale cuts, compresses posteriors in ((\alpha_\perp,\alpha_\parallel,f\sigma_8)), combines correlated methods using mocks, and explicitly adjusts the radius at which (\sigma_8) is evaluated.

Current classification:

- direct reuse under an exact transformation: not available;
- AP-only conversion: insufficient;
- published point: a compressed FLRW-dependent proxy for Timescape;
- scientifically controlled next comparison: reanalyse published multipoles/correlation functions with a derived dressed Timescape forward model, survey window, and nuisance model;
- catalogue/likelihood-code access: required if public multipoles and covariance do not retain the needed information.

Primary classification: `REQUIRES_AUTHOR_INPUT` is **not** used: the missing information is theoretical and survey-methodological, not something only the Timescape authors can answer. Primary classification: `UNRESOLVED_EXTERNAL_DEPENDENCY`.

## 24. Necessary and sufficient conditions

Necessary mathematical conditions:

1. linear evolution over the fitted interval;
2. scale-independent growth and (k)-independent mode mixture on the matched smoothing/fit support;
3. a fixed spectrum shape apart from common growth;
4. matched spatial frame and reciprocal (k/R) units;
5. a finite, nonzero density amplitude and a differentiable signed history;
6. an externally supplied anchor defined at the same reference epoch and in the same smoothing convention;
7. an explicit perturbative transformation from volume-average dust density/expansion to dressed density/velocity;
8. a dressed observed-redshift and real-to-redshift-space Jacobian with an identified LOS and Hubble normalization.

Empirical assumptions:

9. galaxies trace the chosen matter density through a specified deterministic/stochastic bias model;
10. dust and tracer velocities coincide on the fitted scales, or a calibrated velocity bias is supplied;
11. irrotationality, distant-observer, and linear/quasi-linear approximations are valid at the adopted cuts;
12. light-cone, relativistic, wide-angle, nonlinear, and virial effects are absent or controlled.

Convention and survey requirements:

13. the anchor's (R_8,h), spectrum shape, and spatial frame match the survey parameterization;
14. (D_A,H), (\alpha_\perp,\alpha_\parallel), sound-horizon conventions, and fiducial coordinates are explicitly converted;
15. template, bias, damping, reconstruction/nonlinear prescription, window, scale cuts, and covariance are represented;
16. the fitted likelihood retains enough information for the new forward model.

A sufficient condition set is all 1-16 plus a proof that the resulting dressed Jacobian reduces on the selected scales to (\delta_g^s=(b+f_{\rm dressed}\mu^2)\delta_m), with the same (\sigma_8) normalization as the anchor. None of items 7-8 has been derived; items 9-16 are not supplied by Candidate A.

Primary classification: `DERIVED_FROM_VERIFIED_DEFINITIONS`.

## 25. Uncertainty and convention taxonomy

- **Numerical:** solver/reference error already validated for Candidate A; irrelevant to the missing bridge.
- **Solver:** controlled by the frozen growth pipeline; not an RSD theory uncertainty.
- **External-anchor normalization:** an explicit imported amplitude uncertainty, if later supplied, not predicted by Timescape.
- **Convention/scenario:** clock, background preset, rate units, epoch, spatial/smoothing/fiducial choices; not statistical error bars.
- **Model/approximation dependence:** bias, velocity bias, nonlinear RSD, scale cuts, plane-parallel and light-cone approximations.
- **Structural unresolved dependencies:** dressed spatial Fourier/velocity/Jacobian theory; these are blockers, not uncertainties to be combined into a band.

No spread between (Q_{\rm bare}), (Q_{\rm dressed}), or survey conventions is an error bar or confidence interval. Primary classification: `CONVENTION_DEPENDENT`.

## 26. Overall GO / CONDITIONAL / NO-GO verdict

**Primary verdict: `NOT_JUSTIFIED_FOR_OBSERVATIONAL_USE`.**

Answers to the completion questions:

1. No unique observational spatial scale currently corresponds to (k_{\rm code}).
2. A global (k_{\rm com,obs}) is not derived from the existing non-homogeneous dressed geometry; background radial/transverse distances are available.
3. (R_8) uses the (h) of the chosen survey/model spectrum convention; its Timescape match is unresolved.
4. (a_{\rm obs}) is the dressed density-derivative coordinate, but it becomes the RSD growth coordinate only after a dressed continuity/Jacobian derivation.
5. (\delta\Theta) is the dust-frame expansion-scalar perturbation harmonic coefficient.
6. (Z) determines that dust expansion coefficient for the same harmonic; it does not determine the observed tracer velocity without new transfers.
7. (H_D) normalizes the dust CGI relation; (H) enters the clock-rescaled candidate; (H_{\rm fid}) defines survey coordinates. The RSD normalization is unresolved.
8. Dust equals galaxy velocity only under an explicit zero-velocity-bias/tracer-congruence assumption.
9. No dressed Kaiser formula was derived.
10. Consequently no Timescape growth rate is established as the Kaiser coefficient; (f_{\rm dressed}) is only the conditional proxy candidate.
11. (Q_{\rm anchor,dressed}) is not identical to observational (f\sigma_8).
12. Published points are not directly reusable.
13. AP conversion is necessary but insufficient.
14. A controlled comparison presently requires reanalysis of multipoles/correlation functions (and possibly likelihood/catalogue infrastructure).
15. Missing: dressed perturbative spatial and velocity transfer, observed-redshift Jacobian, tracer/bias model, normalization/frame match, and survey forward model.
16. The scientifically justified next work is a derivation-only dressed light-cone and velocity-transfer phase, not an observable implementation.

Primary classification: `NOT_JUSTIFIED`.

## 27. Implementation consequences

No observational API, proxy API, spectrum, (\sigma_R), (\sigma_8) integral, bias model, AP routine, likelihood, or dataset implementation is justified in this phase. Candidate A remains unchanged and correctly named. Both D3 runtime branches remain explicit with no default; D3 does not enter Candidate A and does not cure the missing observable bridge.

An internal theoretical derivation may next define covariant wall/dust/tracer transfers and a dressed light-cone Jacobian. It must not expose an observational quantity until its limiting cases reproduce the appropriate FLRW result and its frame/units are validated.

Primary classification: `NOT_JUSTIFIED`.

## 28. Observational consequences

Existing (f\sigma_8) numbers are not raw observables. They are posterior compressions under fiducial distances, spectral templates, RSD/bias models, windows, scale cuts, reconstruction/nonlinear prescriptions, and covariances. Quoting them against (Q_{\rm anchor,dressed}) would hide all missing transformations and double-count the anchor as though Timescape predicted it.

The no-go does not say that Timescape can never predict RSD. It says that the frozen equations and dressed background do not yet justify that identification. Primary classification: `NOT_JUSTIFIED`.

## 29. Exact next-step matrix

| Option | Triggering evidence | Required inputs | Permitted scope | Forbidden interpretation | Validation |
|---|---|---|---|---|---|
| A. Phase 1E-B — Dressed RSD observable implementation | exact wall/tracer Jacobian and spatial map already derived | complete bridge and survey convention | implement audited observable | none of the prerequisites may be assumed | FLRW limits, frame/unit tests, survey forward checks |
| B. Phase 1E-B — Conditional RSD proxy implementation | only proxy desired with all assumptions accepted | explicit assumption record | separately named conditional proxy | not observational (f\sigma_8), no likelihood use | algebraic identities and assumption rejection |
| **C. Phase 1E-B — Dressed light-cone and velocity-transfer derivation (recommended)** | current structural blockers in Secs. 10-17 | perturbed dressed metric/redshift, dust-to-wall/tracer transfer, LOS Jacobian | report/symbolic derivation only | no observational API or data comparison | covariance, gauge/frame consistency, FLRW and zero-lapse limits |
| D. Stop at Candidate A | missing theory cannot be constructed from accessible inputs | none | document blocker | do not relabel Candidate A | preservation audit |

The selected recommendation is **C: `Phase 1E-B — Dressed light-cone and velocity-transfer derivation`**. If the required perturbative geometry cannot be derived, option D follows. This report does not begin either phase.

Primary classification: `UNRESOLVED_EXTERNAL_DEPENDENCY`.

## 30. Repository preservation statement

The final audit creates only this Markdown report and `reports/phase1e_a_dressed_observable_bridge_inventory.json`. No pre-existing tracked file, source, test, report, artifact, notebook, configuration, documentation, runtime behavior, D3 branch, or Candidate A code was modified. Downloaded sources, rendered pages, and symbolic/numerical scratch work are confined to ignored scratch space. Nothing is staged, committed, tagged, pushed, merged, published, or sent to an author. The work branch remains local and unpushed.

The symbolic checks encoded the tracker chain, cancellation of \(k_{\rm code}\), Kaiser multipoles, and AP determinant; software was Python 3.14.3 and SymPy 1.14.0. Numerical corroboration used the frozen package with NumPy 2.5.1 and SciPy 1.18.0 and explicit Brent root tolerances \(10^{-14}\) for the displayed redshift epochs. These checks do not substitute for the missing observable derivation.

Final complete-suite reruns used the same tracked source tree: Python 3.14.3 / NumPy 2.5.1 / SciPy 1.18.0 / pytest 9.1.1 / pluggy 1.6.0 passed all 379 tests in 14.75 s; Python 3.11.9 / NumPy 2.4.6 / SciPy 1.17.1 / pytest 9.1.1 / pluggy 1.6.0 passed all 379 tests in 15.21 s. Both runs had zero failures, skips, xfails, and warnings.

Primary classification: `VERIFIED_FROM_PRIMARY_SOURCE` (final Git and filesystem checks are recorded in the companion JSON).
