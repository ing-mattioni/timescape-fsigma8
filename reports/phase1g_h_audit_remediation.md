# Phase 1G-H — remediation of the independent audit

Classification: `AUDIT_REMEDIATION_RECORD` (conditional, model-internal,
`NON_OBSERVATIONAL`). Date: 2026-10-07.
Audit: [`phase1g_h_independent_audit.md`](phase1g_h_independent_audit.md) and
its inventory (audit commit `816dd004763f8de1a8bb09cba9e427a1bd2bb3d1`,
audited commit `d4d693d73f995e2245a5720be227273b3639eda9`; the auditor is
named in the audit's header).
Companion: [`phase1g_h_audit_remediation_inventory.json`](phase1g_h_audit_remediation_inventory.json);
logs in [`phase1g_h_audit_remediation_logs/`](phase1g_h_audit_remediation_logs/).
Remediated records: [`phase1g_h_global_variance_closure.md`](phase1g_h_global_variance_closure.md)
(revised in place; the audited text stays at `d4d693d`), its inventory and
validation record, and the F/G freeze-status successor.

**Status note (2026-10-08).** This record states the remediation as of
2026-10-07 and is not rewritten. The independent delta audit
([`phase1g_h_delta_audit.md`](phase1g_h_delta_audit.md)) verified 6 of the
findings below resolved, 2 resolved by owner decision (GH-F1, GH-F2), 6
partially resolved (GH-F4 … GH-F9) and 1 open (GH-F15); the "14 findings are
resolved" of Secs. 0 and 2 is superseded by that verification. In
particular, the records of GH-F9 re-validated their fields but did not bind
their results to their inputs (erratum GH-DE6, finding GH-DF2). The
corrections are in
[`phase1g_h_delta_audit_remediation.md`](phase1g_h_delta_audit_remediation.md).
The commits of this record were pushed on 2026-10-08 and the owner confirmed
the two push approvals of GH-F15 the same day
([`phase1g_h_publication_successor.md`](phase1g_h_publication_successor.md)).

## 0. Summary

- **Audit outcome.** `REJECT` for the scientific closure claims of the text
  at `d4d693d`; provenance, governance, numerics, implementation, tests,
  documentation and task compliance `ACCEPT_WITH_CORRECTIONS`; 15 findings
  (1 HIGH, 3 MEDIUM-HIGH, 7 MEDIUM, 1 LOW-MEDIUM, 2 LOW, 1 INFO). Every
  published number reproduced.
- **Owner decisions** (2026-10-07, verbatim «Procedi, usa le scelte
  raccomandate per i punti 1-4»): D1–D4 of Sec. 1.
- **Result.** The closure claims are narrowed to what is derived (D1, D2,
  GH-F4, GH-F7, GH-F8); the Gaussian constructive pair is requalified and a
  nonnegative pair is added (D3); the Planck normalisation is relabelled and
  given a reclosure variant (D4); the code contracts are hardened (GH-F9,
  GH-F10, GH-F11); the documentation errata are applied (GH-F3, GH-F12,
  GH-F13, GH-F14). 14 findings are resolved; GH-F15 stays open: it needs the
  owner's confirmation.
- **Numbers.** No previously published value changes beyond 6×10⁻¹³
  relative (orthant accuracy). New numbers come only from the new evidence
  sections (Sec. 2).
- **Unchanged.** Status tokens, the five `NOT_GRANTED` authorisations,
  frozen records, tags, the audit's files and every package module other
  than `global_variance.py`.
- **Commits** (local, on `ccr-555e67be-u11yht` on top of the audit commit
  `816dd00`): `c1b4482` (code, tests, evidence script) and the commit that
  carries this record (documentation). Nothing is pushed.

## 1. Owner decisions applied

| Decision | Finding | Choice (recommended option) | Applied in |
|---|---|---|---|
| **D1** | GH-F1 | The statistic is the *formal tangent statistic* — the early Gaussian field propagated with the zero-amplitude tangent of the regional contrast map, smoothing rule `G_R = G W(kR)`, the analogue of ΛCDM's linear σ8 — presented as a proposal, not a closed definition | report §1, §2, §7; module docstring and record texts; README, CLAUDE |
| **D2** | GH-F2 | Seed-indexed void accounting H-A9 with the scale-separation condition declared; the material-domain extension below the super-cell scale is not proved | report §1, §3.1–3.2; module; README, CLAUDE |
| **D3** | GH-F5 | The Gaussian pair is requalified as a signed-carrier surrogate and its mechanism corrected; nonnegative lognormal pairs with the same shared constraints are added | report §1, §6.3; evidence script; tests |
| **D4** | GH-F6 | Direct values primary; post-hoc (fixed-closure) normalisation and PBS reclosure under a rescaled input spectrum reported beside them; the post-hoc scaling of the interval withdrawn | report §5.1–5.5; evidence script; inventory |

## 2. Finding-by-finding resolution

**GH-F1 (HIGH, owner decision) — ensemble response vs tangent; smoothing
rule.** *Resolved by D1.* The definition no longer claims to be the
ensemble-mean response of the true contrast. The report states the tangent,
its smoothing rule (exact for the tangent of a Lagrangian top hat, stated as
part of the definition), the first-order irrelevance of mass versus volume
weighting, and what the statistic is not, with the audit's two-state example
reproduced in the evidence (`ensemble_vs_tangent_example`: mean derivative
0.274683481680 against the tangent f_w = 0.263; equal-mass mean of
`1/(1 + δ_L)` exactly 1) and in a test. "A closed" becomes "A proposed";
the ensemble statistic of the true contrast is listed under C as needing the
joint small-scale law and a transport map.

**GH-F2 (MEDIUM-HIGH, owner decision) — seed-assigned void volume.**
*Resolved by D2.* H-A9 is stated as an assumption of the statistic, with the
scale-separation ratios at `8 h̄⁻¹ Mpc` (evidence `scale_separation`):
present void radius over present proper region radius 0.326 / 0.390 (1G-F
median) and 1.485 / 1.589 ([W09] 15 h⁻¹ Mpc), [GM] / [NW15]. "Removes 1G-D's
restriction to super-cell regions" now holds for the seed-indexed statistic
only; for the material-domain volume the extension is not proved and the
approved `NOT_DERIVED` readings stand.

**GH-F3 (MEDIUM) — void-share derivative.** *Resolved.* The definition is
`p δ_L(LS) = f_v,LS ε`, i.e. `p = f_v,LS − ∂f_v,L/∂δ_L` for the region's
void volume fraction `f_v,L = f_v,LS (1 + δ_L)/(1 + ε)`, with
`p(k → 0) = f_v,LS (1 + A_v)` (seed volume compressed with its region) and
`f_v,LS A_v` (threshold shift only). A test checks the identity against
explicit volume bookkeeping and both relations against the evaluated
closures. No number changes.

**GH-F4 (MEDIUM-HIGH) — interval conditional on a constant share.**
*Resolved.* (H15) is now the constant-share interval: valid for a share
constant over the spectral support of both windows, under H-A7 and an
adopted reading of [W09]. The audit's counterexample is reproduced
(evidence `step_share_counterexample`): `p = f_v,LS` below k_cut and 1 above,
inside H-A7 at every k, premise rms 0.0999, statistic at `8 h̄⁻¹ Mpc` 7.2465
([GM], k_cut = 0.066043 Mpc⁻¹) and 10.3529 ([NW15], k_cut = 0.069093 Mpc⁻¹),
7.26 and 8.91 times the constant-share upper end; a test checks it. Every
"closure-independent" in the report, README, CLAUDE, the module and the
runner is replaced.

**GH-F5 (MEDIUM-HIGH, owner decision) — signed Gaussian laws.** *Resolved by
D3.* The Gaussian pair is labelled `SIGNED_GAUSSIAN_CARRIER_SURROGATE`, with
P(ρ < 0 | wall) = 0.4476 / 0.4429 ([GM] I / II) and 0.4548 / 0.4527
([NW15]) in the evidence; the mechanism is corrected (the drop in law II
comes from the masked wall auto-variance; the integrated cross term is
positive, +0.036 / +0.050). Nonnegative lognormal pairs are added: latent
field = carrier smoothed at r_s ∈ {1, 2, 4} Mpc, wall density ∝ e^a
normalised on the walls, λ fixed by the ball variance of the signed carrier;
law II / law I = 1.03 / 1.19 / 1.29 ([GM]) and 0.92 / 1.05 / 1.19 ([NW15]).
The signed pair is their λ → 0 limit (moments reproduced to 0.93% / 0.64%,
gated). The non-uniqueness survives within nonnegative laws, with a smaller,
construction-dependent size and sign; the kernels are tested by 4-variate
Monte Carlo.

**GH-F6 (MEDIUM, owner decision) — anchoring.** *Resolved by D4.* Direct
values are primary. The post-hoc factor 0.970577 is labelled an empirical
output normalisation at fixed closure; the reclosure variant (input spectrum
×0.970577², PBS share recomputed) is reported beside it (evidence
`pbs_reclosure_under_spectrum_rescaling`; reclosure/post-hoc 1.023 / 1.021
([GM] [W09] / median) and 1.020 / 1.017 ([NW15]); exactly 1 for a constant
share, gated). The post-hoc scaling of the interval is withdrawn (it changes
the premise); under reclosure the upper end is unchanged at fixed η. "Late
ΛCDM growth cancels exactly" is replaced by the condition under which it
would.

**GH-F7 (MEDIUM) — flat-wall cap and S1.** *Resolved.* The fraction of the
Gaussian early field above the cap at `8 h̄⁻¹ Mpc` is 0.4635 ([GM]) and
0.4789 ([NW15]) (evidence `flat_wall_cap_exceedance`), not the whole
overdense half. The cap shows that wall-density freedom is needed if exact
empty voids and the early field are kept; it does not select the full S1.

**GH-F8 (MEDIUM) — headline qualifiers.** *Resolved.* Every [W09]-seed
headline carries H-A8 (formal extrapolation, ε_rms 1.21 / 1.13); the median
seed is "below the adopted ε = 1 threshold, without a controlled error
estimate", and the 1G-F median is a heuristic seed-scale prior, not a
derived F-to-tracker bridge (report §1, §4.2–4.3, §9 H-OD2; README;
CLAUDE).

**GH-F9 (MEDIUM) — record validation.** *Resolved.* `TwoPhaseGlobalGrowth`,
`EvaluatedVoidShare`, `ConditionalGlobalLinearSigma` and
`AdmissibleGlobalLinearInterval` re-validate every field in
`__post_init__`: finite values; closure-variant consistency (a constant
share's stored p equals its closure's; the Gaussian-threshold fields obey
(H12) and the growth record); the tracker identities linking t_LS/t0,
f_v,LS and z_LS (one-time-scale law and (H23)); diagnostics present,
finite and within their tolerances; quadrature, (H9) and (H13) record
identities; every interval field against (H15). The audit's probes
(constant share 0.05 stored as 0.95; threshold share NaN; t_LS/t0 = 2; NaN
diagnostics; upper = ∞; share_upper NaN; share_lower −0.1) and twelve siblings
are refused in a test; records serialise as strict JSON, and the evidence
JSON is written with `allow_nan=False`.

**GH-F10 (MEDIUM) — orthant accuracy.** *Resolved.* The orthant integrals
split their range at the conditional step and its ±8σ edges, refine by node
doubling until two results agree to an explicit absolute tolerance, check
the Fréchet bounds and the moment symmetry, and are refused beyond
`ORTHANT_MAX_NODES` = 1024 nodes per panel (numpy's `leggauss` costs O(n³);
nodes are cached). The audit's cases now agree with their closed forms to
≤ 7×10⁻¹⁵ (ρ = 0, c = −100 → 1; c = 0, ρ = ±0.999999 → 1/4 + asin ρ/2π);
two-threshold probabilities are added for the lognormal pairs. Tests cover
the analytic cases, the scipy CDF, the refusals and the moments at ρ = 0.

**GH-F11 (LOW-MEDIUM) — reference gate.** *Resolved.* The 1G-E/F reference
components exist only to four decimals in the committed inventory, so the
gate uses the exact propagated rounding budget
`5×10⁻⁵ (σ_part/σ + σ_int/σ + 1)` = 1.137×10⁻⁴ ([GM]) and 1.129×10⁻⁴
([NW15]) instead of 6×10⁻⁴; the reproduced values differ by 2.5×10⁻⁵ and
2×10⁻⁶. A test checks it.

**GH-F12 (MEDIUM) — EH98 terminology.** *Resolved.* The transfer is named
as implemented: the zero-baryon-oscillation (no-wiggle) fit with the baryon
shape suppression, EH98 (26), (28)–(31), with f_b = 0.02237/0.14309694 held
fixed (report §5.4, module, evidence script, inventory). The predecessor
`lagrangian_sigma` is unchanged.

**GH-F13 (LOW) — errata.** *Resolved.* Rounding: [NW15] [SvdW04] ε_rms
3.47 → 3.46; [GM] (a) p = 1 6.990 → 6.989; [GM] [W09] seed at L = 10
0.972 → 0.971; [NW15] monotone lower at L = 9 0.341 → 0.340. The report's
source table now carries the full SHA-256 values (four abbreviated suffixes
were wrong; the inventory's full values were right). Convention (c) states
`R_proper·H_D0 = 800 km/s` with `R_proper = γ_w0 R`.

**GH-F14 (LOW) — successor and publication records.** *Resolved.* The F/G
freeze-status successor now states its quotation policy (literal with line
wrapping normalised; S7 and S10 join separate spans), gives S13's base
hashes and per-phrase locations, adds the three unmapped statements (S14 the
frozen F report §14 l. 638–639; S15 the integration report §3 l. 79–80; S16
the integration inventory `open_before_freeze[0]`, each verified at
`8d3cdd0` with its SHA-256) and declares the map non-exhaustive; its
inventory carries the same. The 1G-H inventory's H-OD5 text agrees with its
`publication` block, and the validation record describes the creation of
the remote ref and its later fast-forward separately. Historical bytes are
unchanged.

**GH-F15 (INFO, owner decision) — push approvals.** *Open.* The two recorded
approvals («Sì, procedi con il push sul branch designato»; «Sì, correggi la
documentazione e fai il push») still need the owner's confirmation; the
remediation exchange did not confirm them. Nothing here relies on them.

**Errata register GH-E1 … GH-E22.** Each quoted passage is replaced by the
audit's corrected reading or an equivalent one (GH-E1–E11 by D1–D4 and
GH-F3, F4, F7, F8; GH-E12 in the validation record; GH-E13 by GH-F12;
GH-E14, E15, E19–E22 by GH-F13; GH-E16–E18 by GH-F14).

**Claims marked `NOT_VERIFIABLE` by the audit.** The radiation estimate
"about 0.4%" is withdrawn (the correction is not quantified); the
universality of the Boltzmann/EH98 ratio is no longer claimed (D4); the push
approvals are GH-F15; the author's final chat summary is outside the
repository.

## 3. Validation of the remediated tree

Environment as in the original validation record: Linux, CPython 3.13.16
(NumPy 2.5.3, SciPy 1.18.1, matplotlib 3.11.2, pytest 9.1.1) and CPython
3.11.17 (NumPy 2.4.6, SciPy 1.17.1, matplotlib 3.11.2, pytest 9.1.1); the
upstream clone at the pinned commit, git-ignored and not edited.

| Check | Tree | Result |
|---|---|---|
| Full suite, CPython 3.13.16, `-W error` | this commit's tree | 1171 collected: **1139 passed, 32 skipped, 0 failed** (294 s) |
| Full suite, CPython 3.11.17, `-W error` | same | **1139 passed, 32 skipped, 0 failed** (292 s) |
| `tests/test_phase1g_h_global_variance.py` | same | 35 passed |
| Evidence script, 3.13.16 with figures, 3.11.17 `--no-figures` | `c1b4482`, `src`/`scripts`/`tests` clean | 32 / 32 gates each; 3099 numeric leaves identical (largest relative difference 0); 3.13 artifact SHA-256 `689efe81b034238de2dc56da58d824c31760c4c3777d2586fdfe1fcafcc891ab` (one exact run and environment, not a cross-platform gate) |
| Case runner, three configurations | same | 0.810772, 1.121363, 0.918157 (unchanged) |
| `scripts/audit_numerical_tolerances.py` | this commit's tree | 728 comparisons, 0 without explicit tolerances |
| `scripts/validate_phase1f_c_r_astra_remediation.py` | final bytes of this commit | `PASS`; 49 JSON round trips (the earlier 47, the audit's inventory and this record's) |
| `git diff --check` | final bytes | clean |

- **Command:** `OPENBLAS_NUM_THREADS=1 python -B -W error -m pytest -q -p no:cacheprovider -rs`.
- **Counts.** 1171 = 1136 earlier tests + 35 in the 1G-H file (28 before).
  The 32 skips have the causes of the original validation (upstream oracle
  not extracted 18, clean and barotropic oracles 4 + 4, the owner-decisions
  artifact 3, the 1D-B, 1D-D and B2 artifacts 1 each); the audit
  regenerated some of them in its own environment (1137 passed, 27
  skipped), which was not repeated here.
- **Order.** The suites ran on this commit's tree before the last edit of
  this section and of the two inventories' verification fields; the
  validator, the JSON checks and the whitespace check were rerun on the
  final bytes. No test reads those texts.
- **Logs:** `phase1g_h_audit_remediation_logs/` (evidence and full-suite
  logs, the evidence head).
- **Not run:** the Windows 3.14.3 / 3.11.9 gate; the upstream notebook and
  oracle regeneration; the 20-minute owner-decisions Monte Carlo.

## 4. Open items

- **GH-F15:** the owner's confirmation of the two recorded push approvals.
- **Delta audit** of this remediation (the audit verdict is not reversed by
  the author; an independent delta audit decides).
- **Owner decisions H-OD1…H-OD5** (report §9; H-OD2 and H-OD3
  recommendations revised with the audit).
- **Windows gate** (CPython 3.14.3 / 3.11.9; commands in the validation
  record).
- **C** (prediction, observation): not reached; the lognormal pairs are
  kinematic constructions, not dynamics.
