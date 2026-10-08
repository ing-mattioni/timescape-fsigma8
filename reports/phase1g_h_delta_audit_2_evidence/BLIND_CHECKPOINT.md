# Blind checkpoint — second delta audit of Phase 1G-H (auditor: Claude, Anthropic)

Written: 2026-10-08 16:53:46 UTC, before reading the author's evidence artifact, evidence logs, the implementation of the new evidence-script functions (`_law_summary`, lognormal fields, `_Ball`, `e_reference_rounding_budget`) and the expected values in the test file.

**Not blind to:** the three-decimal values quoted in the audit prompt, in the revised report §1/§6.3 (read for the model definitions), in the second remediation record §2, and the delta audit's published values (m_II, 1/m_II^2, signed law-II wall moments). The reconstruction is therefore blind only to the author's full-precision artifact values and to the author's new code.

**Method:** own code, no project import; tracker and EH98 no-wiggle provider reused verbatim from the first independent audit (`first_audit_provider.py`); Owen's-T orthants; Stein (Gaussian integration-by-parts) moments for the signed pair; exponential tilting for the lognormal pair; QAWO Hankel transforms on [1e-5, 80] Mpc^-1; composite Gauss-Legendre ball quadrature on [0, 2R] (first panel included by construction). Convergence: 16x48 vs 32x64 nodes, max relative change 1.3e-13 on every reported value; ball variance of the unsmoothed carrier vs exact spectral int Delta^2 W^2: rel 1.1e-16 (GM) / 0 (NW15) at 32x64.

## File hashes (SHA-256)

- `first_audit_provider.py` `3fb848ddcae96c78825c3ed2a60b8c912c74dc1b26543a5b0cf8507ebddbd78c`
- `blind_h25_mII_cw.py` `484f44c3e0985d488162bc4d5b4d0c10df1c201af12341b9e0802df22a216796`
- `blind_first_panel.py` `4199048246e678ee7af842a042a586065274738cc17563ee77b75630b6729a10`
- `run_4x24.json` `22c87d90701ded02cf704a6a4b2b98fc5d7249c579546e03d5dedc0b06038f25`
- `run_16x48.json` `0f4cfd942a64db365814579b7c152d6cb9c7597bbc94982b77c48dc5895feedf`
- `run_32x64.json` `5de9657d114590aa34297ac0b4f4b2f4ac136d1586cc13c20640206b81f7df5d`
- `first_panel.json` `c704cae515755cd8c8c0701406dfefaa3a3f936a3896d85e91907f10a674744a`
- `first_panel_32.json` `2699892a8f27daaef2d88d59bc4db0f9aba87c49b4ff069e18f7d735be8840bd`

## Key values (32x64 Gauss-Legendre, convention (b))

| Scenario | quantity | value |
|---|---|---|
| GM | ell (Mpc) | 0.291721007937 |
| GM | mu law II (signed recentring) | 5.00460672758 |
| GM | signed I: wall rms / cross / total / <C_W-1> | 0.9145840728 / 0 / 0.9710823787 / 0.7559295861 |
| GM | signed II: wall rms / cross / total / <C_W-1> | 0.106363541 / 0.03647747281 / 0.3928455621 / 0.04318940747 |
| GM | signed II wall moment E[B^2] (unnormalised) | 0.0007825229276 |
| GM | first-panel share of that moment | 0.000834617 |
| GM | r_s=1.0: lambda / latent var / density var / m_II / 1/m_II^2 / unmasked II ball var | 0.813736671 / 2.68369907 / 13.63914448 / 2.869413475 / 0.1214545343 / 0.08514532035 |
| GM | r_s=1.0 law I: wall rms / cross / total / <C_W-1> | 0.9331432253 / 0 / 0.9885814276 / 0.7869201938 |
| GM | r_s=1.0 law II: wall rms / cross / total / <C_W-1> | 0.7726995318 / 0.3298739215 / 1.016599945 / 0.8376932008 |
| GM | r_s=1.0: total II / I | 1.028342144 |
| GM | r_s=2.0: lambda / latent var / density var / m_II / 1/m_II^2 / unmasked II ball var | 0.8695351087 / 1.594972182 / 3.928191979 / 2.139808561 / 0.2183987551 / 0.1531077623 |
| GM | r_s=2.0 law I: wall rms / cross / total / <C_W-1> | 0.9118950078 / 0 / 0.9685501873 / 0.7514909446 |
| GM | r_s=2.0 law II: wall rms / cross / total / <C_W-1> | 0.9028128052 / 0.3991068538 / 1.149223553 / 1.097277234 |
| GM | r_s=2.0: total II / I | 1.186540014 |
| GM | r_s=4.0: lambda / latent var / density var / m_II / 1/m_II^2 / unmasked II ball var | 0.9984337538 / 0.9666043566 / 1.629002132 / 1.623350652 / 0.3794681417 / 0.2660249506 |
| GM | r_s=4.0 law I: wall rms / cross / total / <C_W-1> | 0.8958703612 / 0 / 0.9534781927 / 0.7253112486 |
| GM | r_s=4.0 law II: wall rms / cross / total / <C_W-1> | 0.9837830705 / 0.4459178559 / 1.23299795 / 1.277631961 |
| GM | r_s=4.0: total II / I | 1.293157998 |
| NW15 | ell (Mpc) | 0.598732248471 |
| NW15 | mu law II (signed recentring) | 3.78883587808 |
| NW15 | signed I: wall rms / cross / total / <C_W-1> | 0.9296221312 / 0 / 0.9779418525 / 0.7912641481 |
| NW15 | signed II: wall rms / cross / total / <C_W-1> | 0.1598085042 / 0.04991194991 / 0.4094186951 / 0.06908311292 |
| NW15 | signed II wall moment E[B^2] (unnormalised) | 0.003553181863 |
| NW15 | first-panel share of that moment | 0.000372908 |
| NW15 | r_s=1.0: lambda / latent var / density var / m_II / 1/m_II^2 / unmasked II ball var | 0.7851499186 / 3.353109082 / 27.59148889 / 2.474113488 / 0.1633656579 / 0.1199905366 |
| NW15 | r_s=1.0 law I: wall rms / cross / total / <C_W-1> | 0.9582759868 / 0 / 1.005219293 / 0.8407943618 |
| NW15 | r_s=1.0 law II: wall rms / cross / total / <C_W-1> | 0.7118407823 / 0.2552430659 / 0.9241933376 / 0.6976554018 |
| NW15 | r_s=1.0: total II / I | 0.9193947471 |
| NW15 | r_s=2.0: lambda / latent var / density var / m_II / 1/m_II^2 / unmasked II ball var | 0.8391930257 / 1.992534118 / 6.334095696 / 2.104325108 / 0.2258261995 / 0.1658672159 |
| NW15 | r_s=2.0 law I: wall rms / cross / total / <C_W-1> | 0.9332931934 / 0 / 0.9814321907 / 0.7975258652 |
| NW15 | r_s=2.0 law II: wall rms / cross / total / <C_W-1> | 0.8089876818 / 0.3143023944 / 1.030017681 / 0.8870055377 |
| NW15 | r_s=2.0: total II / I | 1.049504684 |
| NW15 | r_s=4.0: lambda / latent var / density var / m_II / 1/m_II^2 / unmasked II ball var | 0.9493419943 / 1.170996574 / 2.225205193 / 1.668578791 / 0.3591753816 / 0.2638109337 |
| NW15 | r_s=4.0 law I: wall rms / cross / total / <C_W-1> | 0.9147555337 / 0 / 0.9638208581 / 0.7661585822 |
| NW15 | r_s=4.0 law II: wall rms / cross / total / <C_W-1> | 0.9191434731 / 0.3738613357 / 1.144927517 / 1.11583614 |
| NW15 | r_s=4.0: total II / I | 1.187904897 |

## Derivations (stated before comparison)

- (H25): with x=0, delta = chi psi / f_w - 1 and E[chi psi] = f_w (E[psi|wall]=1), so 1 + xi_delta = E[chi1 chi2 psi1 psi2]/f_w^2 = P11 C_W / f_w^2. Expanding psi = 1 + delta_w and using E[chi delta_w] = 0 gives exactly (H18) at x=0 (alpha = a_w = 1/f_w). Exact; holds for every law with conditional normalisation.
- Consequence: sigma^2 = sigma_part^2 + (<P11>/f_w^2) <C_W - 1>, with <P11>/f_w^2 = 1 + sigma_part^2 for a unit-normalised pair density. Within a pair P11 is common, so the totals are ordered exactly as the P11-weighted <C_W - 1>; no further assumption on the pair weight is needed (checked: residual <= 2.2e-16).
- m_II = E[e^a chi]/(f_w E[e^a]) = Q(c - kappa0)/f_w by tilting (kappa0 = Cov(g, a) one-point); the unconditional covariance of psi = e^a/E[e^a|wall] in law II is (e^{a(r)} - 1)/m_II^2, law I e^{a(r)} - 1.
