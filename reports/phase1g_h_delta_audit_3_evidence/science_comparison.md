# Cross-family scientific comparison — Section 5.C

Auditor family: **OpenAI Codex / GPT-6**; exact served model version is not exposed. Author family: Claude. No author conversation or contact was used.

**Outcome: `CROSS_FAMILY_VERIFIED_WITH_DEVIATION`. SCIENCE: `ACCEPT`.** The analytic binary-mask and Gaussian-moment reconstruction was completed before author numerical comparison and committed in checkpoint `c62ad87d9a51c40d8959d35e0bec58c8b1048a51`, tree `6d5e848faa7b72d829e44a9a2d79e70c3a34acb6`, parent `ed0ec0c`. The five checkpoint files are unchanged. The blind role knew rounded prompt values and received sanitized construction inputs from a separate non-blind provenance role. The root was non-blind for governance, so this is compartmentalized scientific blinding, not a claim that the whole audit team was blind.

## What was independently derived before comparison

With binary wall indicator W, wall-normalized density psi, E[psi|wall]=1, and delta=W psi/f_w−1, expansion proves

`1 + xi_delta(r) = P11(r) C_W(r)/f_w^2`, where `C_W=E[psi1 psi2|both walls]`.

This is H25 and exactly the x=0 specialization of the expanded partition/cross/wall covariance assembly. Integrating against the normalized pair-separation density of the specified ball fixes a unique variance once P11 and C_W are fixed. The identity does not select either function or a spatial geometry. A numerical gate comparing two assemblages of the same kernels verifies assembly consistency; placement in `numerics` is honest and does not promote it to independent physical evidence.

For Gaussian wall-mask field Z and Gaussian carrier Y, exponential tilting proves `m_II=Q(c−kappa0)/f_w`. The conditional wall-normalized carrier is the unconditional lognormal carrier divided by m_II, so its **unconditional covariance** is the original unconditional covariance divided by m_II^2; its unconditional mean is 1/m_II. Pair tilting shifts each mask Gaussian by kappa0+kappa(r), giving `C_W=exp(KY) Q2(c−kappa0−kappa(r),c−kappa0−kappa(r);rho)/(P11 m_II^2)`. General signed-Gaussian pair moments were separately derived through the Gaussian generating function and independently checked by conditional linear regression and adaptive one-dimensional tail integration.

P11 determines the mask rho because the derivative of its Gaussian-tail probability with respect to rho is strictly positive. The carrier law supplies KY; kappa0 and kappa(r) complete the joint Gaussian covariance. They therefore determine C_W in the signed and lognormal constructions. In law I, independence fixes kappa0=kappa(r)=0. **GH-D2F6: RESOLVED.** The qualifier latent Gaussian is essential: Gaussian means/covariances determine the complete pair law, whereas those data generally do not determine mixed exponential moments of non-Gaussian fields.

## Auditor deviations preserved in the immutable blind record

The blind script used the asymptotic photon matter-era wall normalization `D_W=gamma0 f_w0^(1/3) f_w0/f_wLS`. Audited H normalizes at the finite matching epoch exactly: the growing wall contrast is proportional to t^(2/3), hence

`D_W=(f_w0/f_wLS) a_LS (t0/tLS)^(2/3)`; `D_wall=D_W f_wLS/f_w0`.

Substituting the tracker redshift identity gives the factor missing from the blind reconstruction, `1/[gamma_LS f_wLS^(1/3)]`. This changes D_W by −1.57823626e−5 relative (GM) and −8.45500517e−6 (NW15), and propagates into carrier growth/compression and all calibrated latent moments. This was an auditor reconstruction error, not an author defect or new finding. It is corrected only in the explicitly **post-checkpoint, non-blind** independent script.

The checkpoint's column labeled X_SU W09 used the compressed H share `p0=f_vLS+phi(nu)/sigma_s`. The prompt's quoted 1G-D X_SU uses threshold-only `p0=phi(nu)/sigma_s`. Calling the compressed value a 1G-D reproduction was an auditor semantic error. Both conventions are compared separately below. The initial X values remain visible in the checkpoint; they have not been relabeled or rewritten there.

| Scenario | blind D_W | exact finite-matching D_W | blind W09 rms | matched W09 rms | blind F-median rms | matched F-median rms |
|---|---:|---:|---:|---:|---:|---:|
| GM | 0.230618211973 | 0.230614572273 | 1.121366311514 | 1.121362660203 | 0.810776081989 | 0.810772266865 |
| NW15 | 0.352693308922 | 0.352690326899 | 1.056635526243 | 1.056632599471 | 0.816061805159 | 0.816058813008 |

The blinded formulas and Gaussian derivations were retained; the separate post-checkpoint reconstruction still imports no author H implementation and independently integrates EH98, tracker matching, Gaussian probabilities and the ball variance.

## Matched-recipe conditional values

| Scenario | D_V | W09 direct rms | F-median direct rms | constant-share direct rms interval | A_v W09 | X_SU threshold-only | X_SU compressed |
|---|---:|---:|---:|---|---:|---:|---:|
| GM | 7.132537333228 | 1.121362660203 | 0.810772266865 | 0.260865625127–0.998267555902 | 1168.914723790 | 1.262631553125 | 1.263461300439 |
| NW15 | 11.327583314531 | 1.056632599471 | 0.816058813008 | 0.368859433130–1.161784484341 | 1184.662182614 | 1.284975945824 | 1.285682723618 |

| Scenario | signed law I weighted CW−1 | signed law II weighted CW−1 |
|---|---:|---:|
| GM | 0.755929586089 | 0.043189407474 |
| NW15 | 0.791264148143 | 0.069083112915 |

| Scenario | r_s Mpc | lambda | m_II | I weighted CW−1 | II weighted CW−1 | total rms II/I |
|---|---:|---:|---:|---:|---:|---:|
| GM | 1 | 0.813736670976 | 2.869413474886 | 0.786920193781 | 0.837693200838 | 1.028342144077 |
| GM | 2 | 0.869535108737 | 2.139808561227 | 0.751490944555 | 1.097277234245 | 1.186540014377 |
| GM | 4 | 0.998433753819 | 1.623350651791 | 0.725311248556 | 1.277631960576 | 1.293157997502 |
| NW15 | 1 | 0.785149918566 | 2.474113487926 | 0.840794361798 | 0.697655401753 | 0.919394747059 |
| NW15 | 2 | 0.839193025704 | 2.104325108486 | 0.797525865215 | 0.887005537703 | 1.049504684094 |
| NW15 | 4 | 0.949341994318 | 1.668578791219 | 0.766158582157 | 1.115836139975 | 1.187904897141 |

Digits identify numerical calculations, not physical precision. These are conditional model-internal diagnostics. The signed carrier permits negative wall densities and is a signed diagnostic; lognormal construction yields nonnegative densities but retains free resolution and calibration assumptions. No observational sigma8, fsigma8, RSD or unique Timescape prediction is authorized by this verification.

## Error budget and independent checks

The post-checkpoint table compares **58 quantities, all VERIFIED**, against the independently regenerated audited-tree artifact. The full machine-readable ledger gives each value, absolute/relative difference, method and tolerance. The largest absolute difference is 6.05261e−10 (constant-share upper endpoint); the largest relative difference is 1.05745e−8 (the small signed law-II moment).

| Quantity family | maximum absolute error |
|---|---:|
| D_W / D_V | 3.01981e-14 |
| W09 direct rms | 8.55538e-13 |
| F-median direct rms | 1.50002e-12 |
| constant-share endpoints | 6.05261e-10 |
| A_v | 3.81306e-10 |
| X_SU, both conventions | 2.91545e-13 |
| lambda | 2.42802e-11 |
| m_II | 4.89893e-11 |
| m_II inverse-square ratio | 1.13212e-11 |
| CW−1, signed and lognormal | 5.61585e-10 |
| total rms ratio II/I | 5.38944e-11 |

Main propagation values use absolute audit tolerances 1e−12 for D_W/D_V, 1e−9 for rms/interval/X, 1e−6 for A_v; latent read-outs use 1e−6 absolute, compatible with the archived numerical radial error scale. Actual discrepancies are much smaller and are reported above rather than implied by those budgets.

The blind analytic tests independently validate mask H25 algebra, bivariate orthant vs conditional-tail integration, rho=0/1 limits, lognormal one-wall normalization, signed pair moments via regression versus generating-function derivatives, and the ball Fourier/top-hat identity. Maximum residual is 5.7e−15. An independent halving experiment on the blind code (800 radial Gauss-Legendre nodes/6001 spectral nodes versus 1600/12001) changes weighted CW−1 by at most 1.45e−10 GM / 2.15e−8 NW15, m_II by 6.62e−11 / 6.55e−9, and lambda by 4.84e−11 / 7.74e−9. These refinement results were produced from the blind script before comparison, outside the checkpoint, and are preserved separately.

## Terminology

CW−1 is the conditional **product-moment excess relative to the one-wall mean**, and is exactly the defined H25 ingredient. Under dependent law II, E[psi_i|both walls] need not equal 1, so CW−1 need not equal the literal covariance conditional on both walls, which subtracts the product of those conditional means. This terminology distinction does not alter any H25 formula or output.

## Sources and scope

Construction parameters came from the supplied case JSONs and sanitized input-only extract. Approved frozen D/E/F context, lagrangian_sigma and initial-condition recipe supplied spectrum and background definitions. Source equations cited in the independent script are [GM](5.4),(5.6), [EH98](26),(28)–(31), and [1G-A] Eq.(5); Gaussian-tail identities are derived in the checkpoint. The matched-recipe comparison is explicitly non-blind after the checkpoint. The adopted E/F partition targets are rounded construction inputs, not independently inferred physical geometry. This audit does not derive a new Timescape closure, conduct a Windows gate, or prove a unique nonlinear global statistic.
