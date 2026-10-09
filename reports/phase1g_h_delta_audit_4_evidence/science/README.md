# Fourth delta audit — reduced scientific verification

All programs and results in this folder are auditor evidence. They import no
Timescape package module, contact no author, change no production file, and
perform no remote write. The author script's formulas/input definitions and the
third auditor's independent verifier were read; its numeric result files were
not read before the first calculation. Existing rounded values in the task were
known. The centred quantities below were not present in any author value table.
This is independent numerical/algebraic verification, not a blind reinvention
of the approved model or its assumptions.

`INDEPENDENT_CHECKPOINT.json` records the initial code and result hashes, at
2026-10-09 11:05:14.295239 UTC. Both original files remain unmodified. The initial
calculation inherited the asymptotic wall-growth normalization of the earlier
independent verifier. Its deviation is an auditor recipe error, not a defect of
the author model. `matched_finite_matching.py` explicitly corrects the recipe to
the exact finite-LS H8 expression after the checkpoint, without package imports:

\[
D_W=\frac{f_{w0}}{f_{w,LS}}a_{LS}(t_0/t_{LS})^{2/3},\qquad
D_{wall}=D_W f_{w,LS}/f_{w0}.
\]

The existing product-moment values were then visible; the matched calculation
is labelled explicitly nonblind for those values. No author centred values
were available or read. The first checkpoint independently establishes the
product-versus-centred distinction even before the matched rerun.

## Definitions and independent method

Let the radial ball pair density be `w_R(r)`, `P=P11(r)`,
`C_W(r)=E[psi1 psi2 | both walls, r]`, and
`m_i(r)=E[psi_i | both walls, r]`. The three distinct statistics are:

1. Product-moment excess, the renamed author quantity:
   `int w_R P (C_W-1) / int w_R P`.
2. Pair-weighted average of the centred covariance at each separation:
   `int w_R P (C_W-m1*m2) / int w_R P`.
3. Covariance conditional on drawing two ball points both in walls:
   `int w_R P C_W / int w_R P - mean_B(psi1)*mean_B(psi2)`.

Statistics 2 and 3 differ by the variance of the conditional mean over the
separation distribution. The report's statement about subtracting the
conditional means is correct when the separation is fixed. The audit exports
both centred definitions, and does not silently substitute one for the other.

The verifier calculates the spectrum directly from EH98 (26),(28)-(31) and
1G-A spectrum Eq. (5), the tracker from the approved GM definitions, and LCDM
growth from its reduction-of-order integral. It reconstructs the actual signed
and `r_s=1 Mpc` lognormal pairs for both adopted backgrounds. Gaussian upper
tails use deterministic GL128 integration of Plackett's correlation identity,
including unequal shifted thresholds. Signed moments are Gaussian-generating-
function derivatives; lognormal moments follow exponential tilting. All ball
integrals use composite 10-point Gauss-Legendre panels, with 1600 nodes; the
spectrum uses 12001 log-k nodes for the pair reconstruction and 24001 for the
primary values. No author orthant, density or variance function is called.

Doubling radial/log-k resolution from 800/6001 to 1600/12001 changes every new
centred quantity by less than `2.1e-8` absolute. At three moderate/high
correlation separations per background, direct conditional one-dimensional
adaptive quadrature reproduces the asymmetric exponential-tilt tail to less
than `2e-16` absolute (requested epsabs/epsrel `2e-12`). These checks support six
decimal places, not an unproved all-parameter accuracy theorem.

## Matched results

| Background/pair | Law | Product excess | Average centred covariance at fixed r | Fully ball-conditioned covariance | Ball-conditioned mean |
|---|---|---:|---:|---:|---:|
| GM signed | I | 0.755929586 | 0.755929586 | 0.755929586 | 1.000000000 |
| GM signed | II | 0.043189407 | 0.009755656 | 0.009952292 | 1.016482718 |
| GM lognormal, 1 Mpc | I | 0.786920194 | 0.786920194 | 0.786920194 | 1.000000000 |
| GM lognormal, 1 Mpc | II | 0.837693201 | 0.506596604 | 0.517361459 | 1.149056893 |
| NW15 signed | I | 0.791264148 | 0.791264148 | 0.791264148 | 1.000000000 |
| NW15 signed | II | 0.069083113 | 0.022517882 | 0.022861322 | 1.022849838 |
| NW15 lognormal, 1 Mpc | I | 0.840794362 | 0.840794362 | 0.840794362 | 1.000000000 |
| NW15 lognormal, 1 Mpc | II | 0.697655402 | 0.444041205 | 0.450299183 | 1.116851028 |

| Background | D_W | D_V | Convention c, W09 PBS direct | Convention c, median PBS direct | Constant-share interval |
|---|---:|---:|---:|---:|---|
| GM | 0.230614572273 | 7.132537333228 | 1.121362660203 | 0.810772266865 | [0.260865625127, 0.998267555902] |
| NW15 | 0.352690326899 | 11.327583314531 | 1.056632599471 | 0.816058813008 | [0.368859433130, 1.161784484341] |

The interval assumes a constant share and the adopted `10% at 100 hbar^-1 Mpc`
reading. It is not a bound for arbitrary scale-dependent closures. The PBS
values remain conditional research quantities; the W09 seed remains a formal
nonperturbative extrapolation and the median seed a heuristic prior without a
controlled approximation error.

`science_comparison_inventory.json` checks 20 claims against the current
inventory: 20 VERIFIED, none deviating after the declared recipe correction.
It uses `1e-12` for exact growth formulas, `5.2e-7` for six-decimal primary
values, `5e-8` for signed product values and `6e-7` for six-decimal lognormal
values. The broader pair tolerance accounts for the independent integration
scheme and checked refinement; it is not a changed runtime tolerance.
`compare_science.py` also accepts a full-precision regenerated evidence path
and writes `science_comparison_full.json` when one is available.

The fresh `evidence_main_py313.json` comparison is complete: 20 of 20 claims
VERIFIED. The exact growth values agree to at most `3.1e-14` absolute, the four
PBS primary values to at most `1.6e-12`, the constant-share endpoints to at most
`6.1e-10`, and the eight existing product-moment excesses to at most `5.7e-10`.
Declared full-precision absolute tolerances are `1e-12` (growth), `1e-9`
(primary values/interval endpoints), and `1e-6` (independent pair reconstruction,
as in the earlier audit). There is no remaining numeric discrepancy; the
initial asymptotic recipe error is preserved and disclosed.

## Scientific finding resolution and documentation

**GH-D3F5: RESOLVED.** Section 6.3 states the distinction correctly. The current
script, tests and inventory numeric entries use the new key. The old key in
the script docstring and inventory rename log is explicitly historical. The
inventory retains the historical addition string `both-walls conditional
covariance <C_W - 1> per law`, and its new
`evidence.third_delta_audit_remediation_changes` entry explicitly corrects that
exact string to product-moment excess. The two-phase inventory's complete
numeric content is unchanged after canonicalising the renamed key.

No new scientific finding is warranted. The wording correction does not
derive a physical void-share closure, establish a common regional spacetime,
or promote an observational authorization. Prior scientific caveats remain.

## Recommendations, not owner decisions

- **H-OD1:** retain the formal tangent statistic as a named research proposal;
  convention c is a clear conditional choice and a the fixed-mass comparison.
- **H-OD2:** select no physical reference value from this audit. If choosing a
  research example, keep the median PBS seed labelled heuristic, W09 PBS
  labelled formal extrapolation, and constant-share interval limited to its
  class.
- **H-OD3:** retain all tokens and observational authorizations unchanged;
  the product-moment correction belongs in the scientific report.
- **H-OD4:** retain the experimental runtime until remaining contract/test
  findings, the owner's required Windows gate, and explicit promotion decision
  are complete. This reduced check does not certify Windows.
- **H-OD5:** remote publication of an audit requires the designated branch's
  explicit approval; merge, freeze and tagging require separate decisions.

These recommendations do not enact any decision or modify scientific status.
