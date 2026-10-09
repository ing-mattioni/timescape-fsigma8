# Blind scientific reconstruction — draft before author output comparison

OpenAI Codex / GPT-6 family (exact served model version not exposed) working in a compartmentalized blind role. The prompt's rounded expectations are known; no H implementation, author numerical artifact, previous H audit evidence, or author output numbers beyond that prompt have been read. Approved D/E/F reports, frozen lagrangian_sigma formulas and case input JSONs may be used.

## Binary-mask identity, reconstructed without H code

Let W_i in {0,1}, E W_i=f_w, psi_i be the wall density relative to its conditional mean, E[psi_i|W_i=1]=1, and rho_i/rhobar=W_i psi_i/f_w. For delta_i=rho_i/rhobar-1, expansion gives E[delta_1 delta_2]=E[W_1W_2psi_1psi_2]/f_w^2-1 because E[W_i psi_i]=f_w. Defining P11(r)=Pr(W1=W2=1), C_W(r)=E[psi1psi2|W1=W2=1] proves 1+xi_delta=P11 C_W/f_w^2. P11 times C_W is the joint mass moment; P11 alone is insufficient. Once both functions are fixed over r in [0,2R], the isotropic ball variance is uniquely integral p_R(r)[P11 C_W/f_w^2-1]dr. No remaining covariance freedom exists within this statistic and model.

Writing psi=1+d and A_i=W_i-f_w gives delta=A/f_w+Wd/f_w. Its covariance consists of Cov(W1,W2)/f_w^2, the two mask-wall cross moments/f_w^2, and the wall-wall joint d moment/f_w^2. This is the x=0 version of the general two-component assembly. A gate that computes both sides from already-identical intermediates is an assembly check, not independent empirical evidence.

## Latent Gaussian pair moments

For standard normal Z1,Z2 with corr rho, W_i=1[Z_i>c], c=Phi^-1(1-f_w), P11=Q2(c,c;rho). Conditional tail moments can be independently integrated: with s=sqrt(1-rho^2), z=(c-rho*x)/s,
P11=int_c^infinity phi(x) Q(z)dx;
M1=int_c^infinity x phi(x) Q(z)dx;
M12=int_c^infinity x phi(x)[rho*x Q(z)+s phi(z)]dx.
Their quotients by P11 give E[Z1|both], E[Z1Z2|both]. At rho=1 use the exact one-dimensional tail moments instead.

For signed Y_i=a Z_i+B_i with B independent of Z and Cov(B1,B2)=K_B(r), the one-wall conditional mean is mu=a phi(c)/f_w. Center psi_i=1+Y_i-mu. Then C_W=(1-mu)^2+2a(1-mu)M1/P11+a^2 M12/P11+K_B. This signed diagnostic can take negative mass densities and does not define a positive matter realization.

For lognormal psi_raw=exp(Y-v/2), Y zero-mean Gaussian with VarY=v and kappa0=Cov(Z_i,Y_i), exponential tilting shifts Z's one-point mean by kappa0. Thus m_II=E[psi_raw|wall]=Q(c-kappa0)/f_w. Divide by m_II for conditional wall mean one. With KY(r)=Cov(Y1,Y2) and kappa(r)=Cov(Z1,Y2)=Cov(Z2,Y1), exponential tilting gives E[psi1 psi2 W1W2]=exp(KY(r)) Q2(c-kappa0-kappa(r),c-kappa0-kappa(r);rho)/m_II^2. Divide by P11 for C_W. Unconditional product moments are exp(KY)/m_II^2, so the unconditional covariance relative to the unconditional mean is (exp(KY)-1)/m_II^2, exactly the claimed inverse-square normalizer.

For law I, Y and mask are independent so kappa0=kappa(r)=0, m=1, and C_W=exp(KY). Fixed f_w, rho(r) (hence P11), and the complete carrier Gaussian covariance KY(r) fix the variance; prescribing only f_w and a carrier point variance does not. For law II complete mask-carrier covariance fixes the joint Gaussian law and hence C_W. The qualifier latent Gaussian is essential: arbitrary non-Gaussian joint fields can retain first/second covariances while changing mixed exponential moments.


## General signed formula actually implemented

The signed wall field w is not generally of the local form aZ+B with B independent of both mask points. Its cross-matrix is [[kappa0,kappa(r)],[kappa(r),kappa0]]. Put rho=corr(Z1,Z2), h=c sqrt((1-rho)/(1+rho)), d=phi(c)Q(h), off=phi(c)phi(h)/sqrt(1-rho^2), diag=c*d-rho*off. Gaussian generating-function differentiation gives E[w1 1_both]=(kappa0+kappa(r))*d and E[w1w2 1_both]=K_w*P11+2*kappa0*kappa(r)*diag+(kappa0^2+kappa(r)^2)*off. Therefore, with mu=kappa0*phi(c)/f_w, C_W=(1-mu)^2+2(1-mu)E[w1|both]+E[w1w2|both]. These equations, not the simplifying aZ+B case, are used for signed law II. An independent conditional-regression/tail-integration check agrees to below 1e-15 at a nontrivial generic covariance point.

## Frozen construction inputs and numerical method

The provenance agent supplied input-only H definitions: f_v0=0.737/0.627, dressed H0=73.03/61; dressed ball R=8/h; latent k range 1e-5 to 80 Mpc^-1; Gaussian smoothed mask field g at length ell chosen to match partition rms targets **0.3264/0.3036**, adopted frozen E/F reference inputs. These are construction inputs, not author H output numbers. The Eulerian carrier spectrum is Delta_L^2(k D_wall)*D_wall^2 times the frozen Planck normalization. The lognormal smoothing lengths 1,2,4 Mpc are free model inputs; lambda^2 is chosen to match the unmasked ball variance of the signed carrier. The frozen F median inputs are 2.40456/2.80045 photon-comoving h^-1 Mpc. The root and provenance agent read author materials, but this scientific agent received only these sanitized definitions.

No Phase 1G-H implementation, output artifact, prior-audit numerical evidence or numerical output other than rounded prompt expectations was read/imported. A broad search of approved initial-condition definitions returned H filenames and function-call line names, but no H result values or operative H formula bodies were inspected.

Bivariate normal probabilities are evaluated deterministically from the Plackett derivative integral with rho=sin(theta), using 128-point Gauss-Legendre. Ball averages use independent composite 10-point Gauss-Legendre (1600 nodes), rather than author radial Simpson quadrature. Carrier Fourier correlations use a 12001-point logarithmic k grid; main first-panel spectra use 24001 points across 1e-6..1e4. The LCDM normalization is independently integrated from the growth integral, using the frozen recipe Omega_m=0.315, h=0.674; it is not copied from author output. No stochastic multivariate normal CDF routine is used.

## Blind results

All values below are the independent script's results before author comparison; numerical differences versus author full-precision output are not yet assessed. Conditional values are model-internal, not an observational sigma8 prediction.

| Scenario | D_W | D_V | W09 direct rms | F-median direct rms | constant-share rms interval | A_v W09 | X_SU W09 |
|---|---:|---:|---:|---:|---|---:|---:|
| GM | 0.2306182120 | 7.1325373332 | 1.1213663115 | 0.8107760820 | 0.2608697302–0.9982675559 | 1168.9147238 | 1.2634654085 |
| NW15 | 0.3526933089 | 11.3275833145 | 1.0566355262 | 0.8160618052 | 0.3688625468–1.1617844843 | 1184.6621826 | 1.2856862811 |

| Scenario | signed I weighted CW−1 | signed II weighted CW−1 |
|---|---:|---:|
| GM | 0.7559684956 | 0.0431915135 |
| NW15 | 0.7912864721 | 0.0690848314 |

| Scenario | smoothing Mpc | lambda | m_II | I weighted CW−1 | II weighted CW−1 | total rms II/I |
|---|---:|---:|---:|---:|---:|---:|
| GM | 1 | 0.8137299288 | 2.8694306554 | 0.7869621783 | 0.8377340200 | 1.0283401739 |
| GM | 2 | 0.8695286549 | 2.1398241269 | 0.7515305175 | 1.0973286034 | 1.1865378549 |
| GM | 4 | 0.9984266841 | 1.6233614180 | 0.7253493317 | 1.2776914500 | 1.2931560232 |
| NW15 | 1 | 0.7851459719 | 2.4741175757 | 0.8408191643 | 0.6976752224 | 0.9193940743 |
| NW15 | 2 | 0.8391893280 | 2.1043309423 | 0.7975489355 | 0.8870287629 | 1.0495035034 |
| NW15 | 4 | 0.9493381529 | 1.6685840664 | 0.7661806232 | 1.1158644583 | 1.1879035194 |

The independent mask algebra, bivariate-tail normalization/limits, wall lognormal normalizer, signed general pair moments and spherical Fourier window identity pass explicit 1e-12 (or 1e-11 at the coincident tail limit) checks. Residuals are stored in blind_science_checks_results.json. This pre-comparison reconstruction checks analytic formulas and independently chosen quadrature; it does not yet claim agreement to all digits with the author's finite grids.

## Checkpoint and independence statement

These files must be committed by the root auditor before this scientific agent reads author full-precision H numbers, H implementation, or previous H audit evidence. This file's blinding claim applies to that scientific role and is compartmentalized; the root and provenance roles necessarily inspected author documents for governance and input extraction. Exact served model revision is not exposed; the system identifies OpenAI Codex / GPT-6 family, different from the Claude author. No contact with the author or their conversation occurred.
