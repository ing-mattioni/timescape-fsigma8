# Phase 1G-H — independent adversarial audit

**Classification:** `INDEPENDENT_ADVERSARIAL_AUDIT`
**Audit date:** 2026-10-07 (work begun 2026-10-06)
**Auditor:** OpenAI Codex, with separate scientific, implementation and provenance review contributions; final adjudication by the primary auditor.
**Audited commit:** `d4d693d73f995e2245a5720be227273b3639eda9`
**Audited tree:** `963b6e8e42103c27f329e265056c9624be3f11bd`
**Environment:** Linux, CPython 3.12.14 and 3.11.16; details and commands in §2 and the companion inventory.

**Independence warning.** This is an AI audit, not human peer review. No author conversation was accessed or sought, and there was no author contact. The audit prompt itself disclosed target numbers. A saved scientific checkpoint precedes reading the author's 1G-H derivation/runtime/self-check in that review stream; reconciliation followed it. The primary auditor also read mandatory project instructions, which summarize the proposed formulas. Thus this was a staged independent reconstruction, not a fully blinded experiment. The prompt's requested “same family” characterization is not supported: the commit attributes authorship to Claude Opus 5.5, whereas this auditor is OpenAI Codex. Commit attribution does not independently establish the actual author model.

## 0. Summary and verdicts

**Overall: `REJECT` the present claim that A is closed and B is derived for the ensemble statistic defined in H1.** The formal two-component tangent calculation is reproducible and useful as a conditional research prototype. The distinction matters: arithmetic agreement does not supply the missing ensemble response or material-region geometry.

**Merge/freeze readiness:** `NOT_READY_SCIENTIFIC_CORRECTION_AND_OWNER_DECISION_REQUIRED`.

| Area | Verdict | Reason |
|---|---|---|
| PROVENANCE | ACCEPT_WITH_CORRECTIONS | Commit/tree/refs and preservation verified; successor index and publication wording need small corrections |
| GOVERNANCE | ACCEPT_WITH_CORRECTIONS | Original task authorizes the experiment and Linux validation; recorded push approvals require owner confirmation |
| SCIENCE | REJECT | Ensemble/tangent identification and finite-region extension are not derived; interval and positive-density claims exceed demonstrated scope |
| NUMERICS | ACCEPT_WITH_CORRECTIONS | Main values reproduce; the orthant API accepts unconverged cases |
| IMPLEMENTATION | ACCEPT_WITH_CORRECTIONS | Examples work; public record validation is incomplete |
| TESTS | ACCEPT_WITH_CORRECTIONS | Distinct numerical checks and eight killed mutants; missing historical coverage and an overpermissive precision gate remain |
| DOCUMENTATION | ACCEPT_WITH_CORRECTIONS | Missing conditions, transfer terminology, normalization interpretation and minor numeric/hash errata |
| TASK_COMPLIANCE | ACCEPT_WITH_CORRECTIONS | Required artifacts and substantial implementation supplied; the scientific closure claims require narrowing; final author chat is unavailable |

Finding counts: **1 HIGH**, **3 MEDIUM-HIGH**, **7 MEDIUM**, **1 LOW-MEDIUM**, **2 LOW**, **1 INFO**.

Blocking findings are **GH-F1** (HIGH) and **GH-F2, GH-F4, GH-F5** (MEDIUM-HIGH). Their resolution can preserve the calculator by explicitly defining a narrower tangent/seed-accounting/signed-field model, or can pursue the missing physical derivations. Those alternatives are not equivalent and are not selected by this audit.

No existing repository file was corrected. No scientific status, authorization, frozen record or upstream source was changed. No push, PR, merge, issue, comment, release, new scientific tag, freeze or D-v2 branch was made. Restoring exact existing remote tag objects locally for verification is distinguished from creating a new tag. The only new tracked files are this audit's report, inventory and evidence.

## 1. Object, hashes and scope

The object is the four-commit difference above `8d3cdd0533035858c42269cb1dff1a20dcafc7da`, the frozen F/G merge of PR #4:

| Commit | Verified role |
|---|---|
| `79003742fb1f284693d6659e329b2c6b7f7927f0` | F/G freeze-status successor and README/CLAUDE alignment |
| `fd7331f321702ed8c20d32ea805e7b9537d44726` | Experimental runtime, evidence driver, case runner, three configs, 28 tests |
| `0572e416504bcdfaa5831b6d482b687ef6fae582` | Scientific report/inventory, validation record, five logs, documentation |
| `d4d693d73f995e2245a5720be227273b3639eda9` | Documentation-only publication record |

There are exactly **19 changed paths: 2 modified and 17 added**, matching the commissioned set. `scientific_status.py` and `lagrangian_sigma.py` are byte-identical to the base. All 351 files of the audited HEAD were materialized through the GitHub API and checked against their authentic Git blob IDs; authenticated commit/tree/tag objects were reconstructed with SHA verification where a direct private clone was unavailable. The report does not treat a synthetic source export as proof of Git ancestry. Authentic objects provide that proof.

The seven existing 1G tags resolve to the expected checkpoints: A–E to `fb5d95245bc0cb19ce6cd1438177f1a597bb232f`, F/G to the base. The audit is on local branch `phase-1g-h-independent-audit`, starting at the specified HEAD. Earlier approved phases are dependency context, not re-audited scientific targets. The additional uploaded 1C–1E materials do not expand this scope.

## 2. Method, environments and reproducibility

The audit separated five kinds of evidence: independent derivation, independent numerical implementation, same-code reproduction, adversarial API/mutation probes, and read-only provenance checks. These categories are identified in the claims register. A passing project test is never presented as an independent proof of a physical assumption.

The saved `BLIND_CHECKPOINT.md` records the initial mass/volume derivation, tracker integration, Gaussian response identity, covariance normalization and literal-zero-baryon discrepancy before reconciliation. The independent script imports NumPy/SciPy, **no project package**. It uses 120001 logarithmic k samples over 10⁻⁷–10⁵ Mpc⁻¹ for linear variances. The separate covariance reconstruction uses 12001 k samples and 960 separation intervals, conditional-normal adaptive integrals, Gaussian regression and seeded 2-million-sample four-variate Monte Carlo. These are numerical checks, not a rigorous universal tail bound.

| Environment | Python | NumPy | SciPy | pytest | Matplotlib |
|---|---|---|---|---|---|
| Primary | 3.12.14 | 2.3.5 | 1.17.0 | 9.1.1 | 3.10.8 |
| Secondary | 3.11.16 | 2.4.6 | 1.17.1 | 9.1.1 | 3.11.2 |

Both initial complete suites used `OPENBLAS_NUM_THREADS=1`, `-B -W error -m pytest -q -p no:cacheprovider -rs` and returned **1132 passed, 32 skipped, zero failed** (275.83 s / 279.19 s). These are this audit's versions, not the author's 3.13.16/3.11.17 or the unexecuted Windows 3.14.3/3.11.9 gate. The 1G-H evidence script passed **21/21 gates on both**, with `--no-figures` on the secondary run. Interpreter comparison is numeric, not a JSON-byte hash comparison.

The historical upstream notebook was attempted at the locked commit. Kernel networking failed with `Operation not permitted` in `ip_resolver.cpp` and a subsequent nbclient cleanup assertion. No notebook result is claimed. B2 correctly refused its absent oracle. Additional 1D-B, 1D-D and owner-decision artifact regeneration was attempted without editing scripts; outcomes and final coverage are recorded below. Session/runtime interruptions and interpreter reinstalls are environment events, not scientific failures of 1G-H.

Historical regeneration completed: **1D-B passed**, **1D-D passed** (its internal suites: 1134 passed / 30 skipped on both interpreters), and **owner decisions passed 124/124 gates**. The final audit suite is run after assembling these audit deliverables. Its actual outcome, exact skip list and exit code are in `phase1g_h_independent_audit_evidence/final_suite.log` and `final_validation.json`; the latter also records the tested report/inventory hashes, final governance result and whitespace check. These final logs are generated by verification, without changing the tested report/inventory. The remaining unavailable coverage is the upstream oracle tests and their dependent B2 artifact; no zero-skip certification is made.

The standalone tolerance audit found **716 comparisons and zero missing tolerances**. With authentic existing tags restored, the governance validator returned **PASS** on the original 47 inventories / 52 historical reports. The final run includes this additional inventory; its observed count is in the final record.

Minimal reproduction from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 .venv/bin/python -B -W error -m pytest -q -p no:cacheprovider -rs
.venv/bin/python -B -W error scripts/phase1g_h_global_variance_closure_numerics.py
.venv311/bin/python -B -W error scripts/phase1g_h_global_variance_closure_numerics.py --no-figures
.venv/bin/python -B -W error scripts/validate_phase1f_c_r_astra_remediation.py
.venv/bin/python -B scripts/audit_numerical_tolerances.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python -B -W error reports/phase1g_h_independent_audit_evidence/independent_numerics.py
```

Run each of the three committed configurations with `scripts/phase1g_h_global_variance_case.py --config <path>`. The evidence README explains source-cache verification and the independent script's output. Full sources, upstream code and mutated source copies are not distributed with this audit.

## 3. Provenance and governance

### S1–S13 status map

| Row | Verdict | Qualification |
|---|---|---|
| S1 | VERIFIED | Historical SHA-256, exact text modulo line wrapping, location and current freeze reading agree. Audit-scope clause remains true. |
| S2 | VERIFIED | Same checks; no release is observed. |
| S3 | VERIFIED | Exact historical inventory value and current checkpoint reading agree. |
| S4 | VERIFIED | Frozen research/report phase; still no G package runtime or new prediction. |
| S5 | VERIFIED | Historical text and later merge/freeze/tag reading agree. |
| S6 | VERIFIED | Historical inventory value and current checkpoint reading agree. |
| S7 | VERIFIED_WITH_QUALIFICATION | Source bullets are correct and explicitly labelled as joined; this is not one literal verbatim sentence. Later actions rest on distinct owner authority. |
| S8 | VERIFIED | Earlier authorization scope remains historical; it did not authorize the later merge/tags. |
| S9 | VERIFIED | Historical no-tag observation and later F tag are both correctly distinguished. |
| S10 | VERIFIED_WITH_QUALIFICATION | Two source spans, separately correct, are joined with a slash. Later audit records/tags exist; owner freeze execution remains reported. |
| S11 | VERIFIED | Old audit observation is preserved and new main/tag state is correct. |
| S12 | VERIFIED | Old audit conferred no permission; later separate owner action is not permission from that audit. |
| S13 | VERIFIED_WITH_QUALIFICATION | All six phrases exist at the base and current documents were updated, but the published row lacks source hashes and precise per-phrase positions. |

For S13, base README SHA-256 is `85d78ff8583a30d340a16c545eab5e972b8ffcabbcc409e337345bc4c70d149c`; base CLAUDE SHA-256 is `2d96e25cf4632395ebe45d9429738198dba9ec06c6f87f5a8bc01b9683f899c6`. Locations: README lines29–30 and114; CLAUDE line106, line259, lines260–261, lines434–435. See `provenance_claims.json` for per-phrase mapping.

The successor is not exhaustive. It omits the historical F report `phase1g_f_void_population.md` §14 lines638–639 (“Nothing is merged or tagged.”), the integration report §3 lines79–80 ('“Not merged, frozen or tagged” is kept.'), and integration inventory `open_before_freeze[0]` (“separate owner approvals for merge into main (PR), annotated tag, release”). Add later-reading rows in a successor, preserving those historical bytes, or clearly describe the map as a selection. These omissions do not reverse the independently confirmed freeze.


The companion provenance evidence also contains the 40-cell AGENTS rule/commit matrix. The base has 334 files; only README/CLAUDE among those changed in the author phase. PR #4 merged at `2026-10-06T13:12:04Z`, parents `fb5d95245bc0cb19ce6cd1438177f1a597bb232f` / `3d3d46ed68fde7e6d4100fe518a76731bd2cf9e9`; merge and phase branch share tree `5bcea4170c92c034af0045afb7f9898c2f28359d`. F/G annotated objects are `ca52c94d6ecad2be62016b019d652d9bc6e89dd2` / `d151bd45242eff50ca7fa62bbd50453375737117`, both tagged at `2026-10-06T15:32:56+02:00`. Main/branch/PR snapshot was refreshed at `2026-10-07T04:55:46.522Z`; the tag/release snapshot is `2026-10-06T19:20:54.939Z`.

The current snapshot corroborates main at the base, the designated author branch at the audited HEAD, 38 tags, no PR from that branch, no release and no D-v2 ref. It cannot prove that no transient ref ever existed, nor recover push events merely from commit chronology. A first remote branch creation is not literally a fast-forward update of an existing remote ref; the subsequent advance is consistent with ancestry.

The original task was recovered as a supplied Library file (version 2) and read, without accessing author chat. It explicitly permits an isolated experimental runtime, focused README/CLAUDE changes, supported cloud interpreters, and disclosed historical-artifact skips. Consequently the 1G-H firewall exception and Linux environment are authorized; the rigid generic CLAUDE preflight wording must be read with that task. The historical logs support the declared 1132/32 outcome. They identify the implementation checkpoint plus documentation work, not a cryptographic certification of every later documentation byte. This audit independently reran the designated HEAD.

The two quoted publication approvals remain **`OWNER_CONFIRMATION_REQUIRED`**. Their presence in inventories proves what the author recorded, not that the owner uttered them. No missing-chat search was performed. This is a verification limit, not evidence of an unauthorized push.

All seven 1G tag signatures pass the SSH mathematical signature check against their embedded key, fingerprint `SHA256:65hFn8HnIB5jIzkHfWCR7Em0D500qriDfGl+8moqz8Y`; GitHub also reports verified signatures. No established local owner-trust configuration was available. No trust configuration was created or modified. Mathematical signature validity and signer-identity trust are different claims. The author's statement that *their session* did not cryptographically verify signatures is not refuted by this later audit.

## 4. Scientific adjudication

### 4.1 Definition, ensemble and tangent (GH-F1)

The mass/volume ratio in H1 is meaningful once its material domain, foliation, measure and ensemble are defined. Choosing a dust slice, common time and a mass-weighted Lagrangian ensemble is defensible; choosing Eulerian spheres, volume weighting or a dressed-frame construction defines other quantities. The background does not select one uniquely. Uniform early coordinate centres imply exact mass weighting only if those coordinates are mass coordinates; ordinary early photon coordinates are not automatically such coordinates at finite perturbation amplitude.

For empty voids, conservation and additive **actual** phase volumes give

\[
\frac1{1+\delta}=\frac{f_w}{1+\delta_w}+\frac{f_v}{1+\epsilon},\qquad
\delta=f_w\delta_w+f_v\epsilon+O(2).
\]

H2, H3 and the homogeneous tangent H4 are correct. Linearizing H2 with finite void density x also gives H5, with the denominator `f_w+x f_v` and the negative `(1−x) δf_v` term. But differentiating the nonlinear identity at a finite small-scale realization gives

\[
\partial\delta=(1+\delta)^2\left[
 \frac{f_w}{(1+\delta_w)^2}\partial\delta_w+
 \frac{f_v}{(1+\epsilon)^2}\partial\epsilon\right].
\]

Gaussian integration by parts identifies a cross-propagator with the **ensemble average** of that derivative, subject to Gaussianity, integrability and translation invariance. It does not replace the random coefficients by their values at `δ_w=ε=0`. H1 explicitly keeps small-scale statistics fixed; H4/H9 instead calculate the zero-amplitude regional tangent. Connected mean subtraction does not repair this mismatch.

An independently evaluated positive-density example sets `f_v=.737`, `ε=0`, and two equal-mass wall contrasts `−1/3, 1`. For `F(s)=f_w s/(1+f_v s)`, the equal-mass mean reciprocal density is exactly 1. Nevertheless `E[F′]=0.274683481680`, while `F′(0)=0.263`; a central difference gives `0.274683481738`. This is a counterexample to the asserted algebraic implication, not a claimed full Timescape cosmology. It identifies the extra response/statistical closure that a physical ensemble calculation needs.

There is also a window-definition ambiguity: H1's `δ_L` is already a regional average. Its regional cross response contains the window in the linear homogeneous limit; multiplying by another `W_R` in H10 double counts smoothing unless an **unsmoothed carrier** `G` and a relation `G_R=G W_R` are separately specified. The ratio `M_L/V_L` does not generically commute with smoothing. The standard linear FLRW result is recovered by a perturbative tangent around homogeneous FLRW, not automatically by a nonlinear finite-small-scale ensemble propagator.

**Minimum repair:** explicitly choose the formal tangent carrier and its smoothing rule as an additional phenomenological definition, or derive the joint small-scale response and boundary transport needed for the actual H1 ensemble. Under the second choice, p alone is not the only missing object.

### 4.2 Tracker growth, region geometry and approved predecessors (GH-F2, GH-F7)

Independently, with `q=t/t0`, `f=f0 q/(1−f0+f0 q)`, `a_D/a_D0=q(f0/f)^(1/3)` and `γ=1+f/2`, redshift gives H23. EdS wall growth in common time and autonomous Milne void volumes give

\[
D_W=\frac{f_{w0}}{f_{wi}}\frac{q_i^{-2/3}}{1+z_i}
=\frac{\gamma_0 f_{w0}^{4/3}}{\gamma_i f_{wi}^{4/3}},\quad
D_V=\frac{f_{v0}}{f_{vi}(1+z_i)},\quad G=(1-p)D_W+pD_V.
\]

These reproduce H6–H9 **within that regional tangent model** and its growing-mode ICs. The EdS limit gives `D_W=1−5 f_v0/6+O(f_v0²)`. GM's flat effective averaging geometry does not by itself provide a late material-boundary transport map.

Assigning an entire expanded bubble to the initial region containing its seed defines a seed-indexed volume statistic. It has not been shown to equal the Riemannian volume of the transported material ball in H1 when bubbles cross its boundary. H-A6 fixes total void growth, not the allocation of intersecting volume. Empty interiors also lack dust mass labels. At convention (c), characteristic present void radii divided by the present mean proper reference radius are about **0.326/0.390** for the F medians and **1.486/1.589** for W09 (GM/NW15). The latter plainly do not provide a small-bubble limit. The unconditional “every Lagrangian region” and “only through p(k)” extension is therefore unproved.

H-A6 with `H_v=1/t`, `H_w=2/(3t)` and J=0 is consistent with the exact-empty tracker identity `df_v/dt=f_v f_w/t` in approved G. **There is no blanket J=0 contradiction.** G's nonzero-transfer conclusion for a finite-density shell-crossing cohort uses a different `H_v t=8/9` premise. G and the D successor do forbid silently identifying finite-mass F seeds with exactly empty finite-time tracker voids. H admits the populations differ; importing the F median only as a numerical scale prior is permissible if that distinction stays explicit. It is not a derived F→H dynamical bridge.

H13's empty-void/uniform-wall-density cap is correct. Its capacity radii are approximately 99/127 dressed-h⁻¹ Mpc, and the GM early rms at (c) is 10.9 times the cap. A Gaussian field exceeds any finite cap with nonzero probability; at that ratio about 46.4%, rather than literally the whole overdense half, exceeds it. If exact emptiness and the given early field are held fixed, wall-density variation is needed. The entire super-cell/separate-universe assumption S1 is not uniquely forced: relaxing another model premise is an alternative. No status change follows from this cap.

### 4.3 Void share, compression, seeds and perturbative control (GH-F3, GH-F8)

The amplitude definition `p δ_i=f_vi ε` is coherent and gives `p=f_vi A_v`. But H3 implies

\[
f_{v,L}=f_{vi}\frac{1+\delta_i}{1+\epsilon},\qquad
p=f_{vi}-\frac{\partial f_{v,L}}{\partial\delta_i}.
\]

The report's negative-derivative-only definition omits `f_vi`. Void specific volume per fixed reference mass and the regional void volume **fraction** are not interchangeable. The Gaussian threshold derivative is `−φ(ν)/σ_s`; with the declared compression convention this correctly leads to `p=f_vi+[φ(ν)/σ_s]W(kR_s)`. Fixing the definition need not change the existing H12 numbers. The threshold-only convention remains distinct and reproduces the approved D response.

The monotone range `f_vi≤p≤1` is an added class assumption H-A7, not a tracker theorem. A top-hat kernel has negative lobes, so the PBS expression is not globally in that class at every k. Small seeds can make the departure negligible under a particular R window, but this is numerical support, not exact pointwise membership.

Seed-radius conversions, including the F median's gamma ambiguity, must be explicit. An F median used in a tracker closure is a heuristic prior. W09 seeds give `ε_rms≈1.21/1.13`; H-A8 authorizes a formal extrapolation in the report, but README/CLAUDE headlines omit the qualification. F medians give about `.77/.74`; being less than one does not demonstrate a controlled `ε≪1` expansion or bound its error. “Perturbative” should be narrowed to the stated diagnostic threshold.

H22 follows from gambler's ruin: `m(δ_l)=(δ_c−δ_l)/(δ_c+|δ_v|)`. At fixed x and with the same barrier clock, `Z=1−m+m/x` and differentiating it gives the stated positive volume-response contribution. The numerical mass fraction, void fraction, bias and alternative growth reproduce. This is a separately assumed two-barrier model, not a derivation selecting tracker p.

### 4.4 Interval and homogeneity premise (GH-F4)

If p is constant over the spectral support relevant to **both** windows, then `σ(R)=G(p) σ_u(R)`. H-A7 and the chosen `σ(R_hom)≤η` premise yield H15 (with the upper end also capped by p≤1 where applicable). Merely saying “between R8 and R_hom” must not hide the broad k support of both windows. The bound does not apply to arbitrary scale-dependent p.

An explicit counterexample uses `p(k)=f_vi+(1−f_vi) 1[k>k_cut]`, always inside H-A7. For GM, `k_cut=.0660693448 Mpc⁻¹` gives `σ_hom=.0998770` but `σ_R8=7.24602`, exceeding `.998268`. For NW15, `.0691830971` gives `.0997361` and `10.34911`, exceeding `1.161784`. Smooth approximations to the step retain the violation. These are counterexamples within the formally extrapolated linear class, not physical positive-density cosmologies.

W09 discusses late density fluctuations of coarse dust cells, a scale around 100 h⁻¹ Mpc, several-percent standard deviation, and a 10% bound. Reading it as precisely this mass-weighted Lagrangian linear projection, a top-hat radius rather than a cell side, and the bare-h convention is an **additional premise**. The report partly acknowledges this in §5.2; the headline interval must carry the same conditions everywhere.

### 4.5 Covariance and realizability (GH-F5)

For complementary indicators and phase-conditionally centered fields, direct expansion gives H17. With `A=(χ_w)_R−f_w`, `B=(χ_w δ_w)_R`, `C=(χ_v δ_v)_R`, the total variance is `(α,a_w,a_v) M (α,a_w,a_v)^T`. This independently verifies H18, including all cross terms. Positive semidefiniteness and `E[A²]≤f_v f_w` are necessary consistency conditions. H19 follows after imposing E3 and the stated internal normalization; H20 is Cauchy–Schwarz for its two weighted components. Attainment of the endpoints is not guaranteed.

The orthant identities were independently integrated and checked by bivariate CDF and Monte Carlo. The I/II total variances reproduce (see §5). The two constructions are realizable **signed Gaussian carrier fields and masks**. They are not nonnegative matter-density fields: the conditional probability of negative wall density is approximately **44.76%/44.29%** (GM I/II) and **45.48%/45.27%** (NW15). Subtracting the phase-conditional mean enforces normalization, not positivity. A clipping or positive transform would change the covariance and require recomputation.

The common covariance is that of the unconditioned latent wall carrier, not its phase-conditioned or masked density field. The latter deliberately changes between I and II. The integrated cross contribution in II is **positive**, `.0364775/.0499120`; the decrease in total variance primarily comes from the changed wall auto-variance, not a negative cancellation of the two integrated contributions. Fitting ℓ to one partition rms does not establish equality to F's entire spatial covariance. Between the two constructed laws their common partition covariance is indeed identical.

Retain the example as a proof of statistical underdetermination within the signed-field class, or construct two nonnegative density laws with the intended shared constraints. The stronger physical-admissibility wording is not established by PSD or Monte Carlo.

### 4.6 Early spectrum and normalization (GH-F6, GH-F12)

The actual provider is EH98's **baryon-corrected no-wiggle** prescription: the T0 form with the effective shape and sound-scale corrections, not the literal zero-baryon transfer. Literal zero-baryon reconstruction gives unit variances near 1.50014/1.38221 rather than 1.12798/1.04420. Reconstructing the actual documented predecessor formula removes the discrepancy. Inputs use `ω_ref=.315×.674²=.14309694`, printed as `.14310`, and `f_b=.02237/ω_ref` held fixed when changing effective density. Correct the terminology; do not modify the approved predecessor in this audit.

The Planck-reference EH value `.835688660049` and ratio `.8111/σ_EH=.970576769526` reproduce. No Timescape target value was fitted, so this is not that kind of circular calibration. But multiplying a final PBS answer by this factor **holds a spectrum-dependent closure fixed**. Uniformly rescaling the input spectrum amplitude instead requires `p−f_vi` to scale inversely with the amplitude and gives different answers:

| Scenario/seed | Post-hoc factor | Recomputed PBS under uniform spectrum rescaling |
|---|---:|---:|
| GM W09 | 1.08836855 | 1.11368720 |
| GM F median | 0.78691673 | 0.80309676 |
| NW15 W09 | 1.02554305 | 1.04577960 |
| NW15 F median | 0.79204773 | 0.80520578 |

This is a diagnostic counterexample, not a claim that a true Boltzmann transfer correction is uniform. Likewise the H15 upper ratio is invariant under uniform spectrum rescaling at fixed η; scaling the finished interval changes the premise. The claimed exact cancellation of late ΛCDM growth requires a common scale-independent factorization, which was not independently established for the imported massive-neutrino Boltzmann reference. Specify post-hoc normalization, spectrum recalibration or a new homogeneity convention explicitly. H16's PBS amplitude dependence itself reproduces.

The reported radiation correction of “about 0.4%” lacks a reproducible radiation-inclusive model/control in the delivered evidence. The common-rescaling cancellation in ε is algebraically checkable; that particular physical correction is **NOT_VERIFIABLE** here. No independent CAMB/CLASS run was made.

## 5. Numbers and claim register

1216 explicit checks: 1192 VERIFIED, 12 VERIFIED_WITH_DEVIATION, 11 REFUTED, 1 NOT_VERIFIABLE.

Python 3.12 vs 3.11: 2779 numeric leaves; maximum absolute difference 0, relative 0. This is same-code reproduction. Non-numeric mismatches: 0; unmatched non-metadata paths: 0.

Independent direct-sigma comparisons differ by at most **1.10822×10⁻¹⁰**. Independent core: 895 scalar comparisons, maximum absolute difference 2.36368578044e-08 (on the large A_v≈4914 coefficient, relative difference about 4.8×10⁻¹²). Independent covariance total maximum absolute difference 1.90093575465e-05; all printed 3-decimal total values survive. Serialized last digits are not validated to their full length.

| Quantity | GM | NW15 |
|---|---:|---:|
| D_W | 0.230614572273 | 0.352690326899 |
| D_V | 7.13253733323 | 11.3275833145 |
| p=0, convention c | 0.260128282054 | 0.368278015676 |
| p=fi, convention c | 0.260865625127 | 0.36885943313 |
| F median, convention c | 0.810772266865 | 0.816058813008 |
| W09, convention c | 1.1213626602 | 1.05663259947 |
| SvdW, convention c | 2.64338857468 | 2.45413356403 |
| p=1, convention c | 8.04534884719 | 11.8282231956 |
| Law I total | 0.971081474274 | 0.977941023012 |
| Law II total | 0.392843811615 | 0.409416977214 |
| Capacity radius, dressed h^-1 Mpc | 99.0165866107 | 127.367785635 |

Independent Planck EH98 sigma=0.83568866004935; multiplier=0.97057676952575. All seven full source hashes match. Orthant analytic vs adaptive integral maximum error=2.22045e-16; seeded bivariate MC maximum standardized error=2.41561 (1.5 million draws/case). Four-variate covariance MC maxima are 1.1317146687821966 / 1.1829832020413298.

Printed table deviations (small documentation errors; author unrounded values agree with independent results):

- Printed seed table NW15/SvdW epsilon: printed 3.47, independent 3.4647112955254, half-last-digit tolerance 0.005; report line 381.
- Printed principal table GM/a/p1 value 0: printed 6.99, independent 6.989454191171, half-last-digit tolerance 0.0005; report line 443.
- Printed radius scan GM L=10 W09: printed 0.972, independent 0.97149064298414, half-last-digit tolerance 0.0005; report line 498.
- Printed radius scan NW15 L=9 lower: printed 0.341, independent 0.34049865183372, half-last-digit tolerance 0.0005; report line 499.

The scientific interpretation counterexamples are intentionally separate from the reproduced values: H1 ensemble tangent, unrestricted H15 p(k), positive-mass interpretation of signed Gaussian laws and self-consistent PBS reclosure under the anchor are not established by correct implementation. See individual REFUTED rows; these refute the broad identified claims, not the conditional numerical outputs.

Coverage limits:

- Radius scans at conventions a,b and SvdW radius scans were reproduced with author code; own independently recomputed saved radius scan covers c lower/W09. Full a,b closure and interval tables were independently checked.
- Existing wall-internal 0.834/0.935 summary numbers are imported from 1G-C and were not independently reconstructed in this new H numerical calculation.
- Individual 121-point propagator plotting arrays reproduced across interpreters; independent saved outputs verify integrated scale dependence and low-k values rather than every plotting abscissa.
- Mass-fraction finite-difference numbers in artifact compared to independent analytical derivative; author finite-difference routine itself is not an independent implementation.
- No CAMB/CLASS computation; no claim for physical accuracy of EH98 import or universal anchor correction.
- All observational matching, tracer, nonlinear dynamics and positive-density completions remain outside numerical verification.

Inventory consistency: 856 matched numeric leaves; 856 within inferred rounding tolerance; 0 unmatched numeric leaves. See JSON for exact paths and all claims.


The machine-readable `claims` list records declared and independent values, methods, tolerances and status. It includes negative and unavailable results; `VERIFIED` always applies to the stated mathematical/numerical scope, not implicitly to physical observability. Different tolerances distinguish display rounding, quadrature error, Monte Carlo sampling, same-code reproduction and exact hashes. Small one-unit display-rounding errors are listed as errata rather than scientific failures. Source hashes match the full inventory; several abbreviated report suffixes do not.

## 6. Implementation, tests and mutations

All 16 exported functions use mandatory keyword-only arguments; all ten exported dataclasses are frozen and keyword-only. Public names and recursively inspected keys of the three runner outputs obey the naming rule. Scientific inapplicability is explicit, arrays reject direct assignment, and no other package module imports `global_variance.py`. Tests and source scans show no new undocumented warning suppression. H labels and source references accompany implemented equations.

Deleting all 33 required top-level fields across the three configs, and 89 tested immediate nested fields, caused rejection. These tests cover the supplied structures, not all possible custom nesting. Twenty repeated CDF probes in SciPy 1.17.0 had zero observed spread; Monte Carlo seeds are explicit. No unobserved nondeterminism defect is asserted.

The standard factories produce the published values. Nevertheless exported records accept incompatible replacements: constant share `.05` with stored `.95`, PBS threshold coefficient NaN, last-scattering time ratio 2, NaN growth diagnostics, and negative/NaN/infinite interval fields. Frozen assignment does not validate construction. GH-F9 requests finite values and variant-specific consistency checks, including strict JSON finiteness.

For the orthant integrator, valid accepted inputs `ρ=0,c=−100,n=16` return probability `.659442450894` instead of 1; `n=64` returns `1.002185860138`. At `ρ=.999999,c=0`, 200 nodes err by `1.59298×10⁻⁶`; 400/800 nodes reduce this to `6.71×10⁻¹¹/5.77×10⁻¹⁵`. The analytic check is `1/4+asin(ρ)/(2π)`. GH-F10 requests a converged accuracy contract or a bounded supported domain; silent clipping would not resolve integration error. Published central cases pass.

The root tolerance `root_xtol_fraction=10⁻¹⁷` is meaningful: it is absolute on the time fraction and scaled by t0, about `2.96×10⁻¹³` relative at the GM root, larger than its ulp `6.78×10⁻²¹`. It is not a request for relative 10⁻¹⁷ accuracy. No finding is raised on that example.

The 28 tests include explicit mass sums, finite differences, a separately coded tracker, exact closed-FLRW spherical evolution, real-space pair integration, synthetic correlated fields, bivariate CDF, Monte Carlo and predecessor references. They have meaningful independent routes but share some spectrum/provider code; not all 28 are independent physics derivations. Interval tests mostly check algebra/contracts. The complete I/II spatial construction lacks its own dedicated k/r refinement gate, although this audit's separate finer calculation recovers printed digits.

All 21 evidence gates are declared before evaluation and failures return a nonzero exit. The E/F gate at `6×10⁻⁴` cannot certify the claimed fourth decimal (GH-F11); even propagation of four-decimal rounded inputs suggests about `1.2×10⁻⁴`, and full-precision references are preferable. The actual values pass a substantially tighter comparison.

| Isolated mutation | Failed | Passed | Fixture errors | Outcome |
|---|---:|---:|---:|---|
| Wall exponent 4/3 → 1 | 12 | 12 | 4 | KILLED |
| Remove wall gamma factors | 12 | 12 | 4 | KILLED |
| Remove void `(1+z_LS)` factor | 12 | 12 | 4 | KILLED |
| Reverse compression sign | 1 | 27 | 0 | KILLED |
| Seed window → 1 | 1 | 27 | 0 | KILLED |
| Swap phase weights | 2 | 26 | 0 | KILLED |
| Shift orthant lower limit +0.1 | 2 | 26 | 0 | KILLED |
| Reverse barrier response | 1 | 27 | 0 | KILLED |

Baseline: 28/28. Survivors: **0/8**. The first three produce genuine runtime consistency failures as well as assertion failures, not broken imports. The quiet-output parser left `failed_tests` arrays empty; raw logs contain the assertion/fixture failures and summary counts, which were inspected. All mutation copies remained outside the audited tree and are not committed. The source SHA-256 before/after is `a7c57606bfebf2abb3c87a0f480832f5df1ef98f87741489c760d41cc229b5d2`.

## 7. Documentation and original-task compliance

The original task required A (unambiguous definition), B (complete conditional calculation with additional assumptions tracked), and a separate account of C (theory-selected prediction/observational interpretation). Required reports, inventory, validation record, examples, figures, tests, usage guide and separated commits exist. The implementation is substantive and authorized; it is not merely a plan. The self-check is correctly labelled as such. No observational tension/consistency inference or permission was introduced in the audited phase.

A/B closure is overstated for the definition actually written. The owner may accept a narrower formal statistic, but the report cannot silently substitute it for H1's ensemble response. C is correctly not reached. An audit rejection of the current identification does not establish a no-go theorem for global linear statistics.

README/CLAUDE omit conditions needed for “derived”, “closed”, “closure-independent”, and the sub-cell extension. They also omit the W09 H-A8 qualifier next to headline values. GH-F13 collects harmless numerical rounding, incorrect abbreviated hashes and H24's coordinate-radius shorthand: `R H_D0=800 km/s` applies to the **present proper reference radius** `γ_w0 R`, not the photon-comoving R printed in the same table. Convention (c) is a named defensible convention, not uniquely selected by the background.

F/G successor records should remain additive corrections to frozen history. The S1–S13 index is useful but not exhaustive, and must not call joined snippets unqualified literal quotes. H-OD5's inventory text also needs alignment with its publication block. Exact errata and corrected readings are machine-readable and summarized in §8.

The author's final Italian conversation response is unavailable and was not sought, so that particular task deliverable is `NOT_VERIFIABLE`. Recorded claims about the author's actions are distinguished from this audit's independently observed results.

## 8. Findings and errata

### GH-F1 — Ensemble response is not the homogeneous tangent; regional smoothing is unresolved

**HIGH · SCIENCE · OWNER_DECISION**

H1 defines a finite-small-scale ensemble cross-response, whereas H4/H9 evaluate the derivative of H3 at zero regional perturbations. Averaging and this evaluation do not generally commute. The H1 contrast is already regional; H10 adds another window without deriving the unsmoothed carrier relation. Uniform photon-position labels also do not establish exact finite-amplitude mass weighting.

Evidence: The positive-density equal-mass two-state counterexample has averaged derivative 0.274683481680 and homogeneous derivative 0.263; a central difference independently confirms the former.

Consequence: The arithmetic establishes a conditional linear tangent surrogate, not the stated H1 statistic. Claims that definition A and calculation B close with only p(k) are not established.

Suggested resolution: Choose explicitly between a narrower formal tangent statistic and the full ensemble response. For the latter, supply small-scale joint statistics, derivative averaging, mass-coordinate sampling and the regional smoothing relation. Do not promote definition/computation status before this choice is resolved.

Locations: `reports/phase1g_h_global_variance_closure.md:49-65,125-159,240-267,645-653`; `README.md:150-160`; `CLAUDE.md:473-481`.

### GH-F2 — Seed-assigned void volume does not establish a material-domain volume map

**MEDIUM-HIGH · SCIENCE · OWNER_DECISION**

Total Milne bubble growth and initial seed ownership do not imply that a sum assigning whole bubbles to seed labels equals the Riemannian volume of a transported dust ball. Boundary intersections and empty interiors require a spatial allocation or transport prescription.

Evidence: At convention (c), present characteristic void radius / mean-region radius is about 0.326/0.390 for F medians and 1.486/1.589 for W09 radii (GM/NW15). Small initial seeds do not ensure a negligible final boundary effect.

Consequence: The extension from super-cell accounting to every material Lagrangian region, including sub-cell scales, remains unproved; p(k) alone need not encode boundary response.

Suggested resolution: Supply a transported-domain volume allocation and its response, or narrow the definition to a seed-indexed statistic / explicitly scale-separated aggregate. Preserve the approved NOT_DERIVED reading; this finding is not a no-go for a future sub-cell construction.

Locations: `reports/phase1g_h_global_variance_closure.md:56-65,125-139,229-244,286-290`; `README.md:156-160`; `CLAUDE.md:477-479`.

### GH-F3 — The derivative definition of the void share omits the initial void fraction

**MEDIUM · SCIENCE · CORRECTION**

For the actual regional void fraction, H3 gives f_v,L=f_i(1+delta_i)/(1+epsilon). Thus p=f_i-d f_v,L/d delta_i, rather than the displayed minus derivative alone. The amplitude definition p delta_i=f_i epsilon and the H12 compression term are mutually consistent.

Evidence: The independently reproduced compressed and threshold-only values differ by the expected f_i contribution to p; the current numerical chain need not change.

Consequence: The report conflates a regional fraction response with a void-specific-volume response and misidentifies the single missing object.

Suggested resolution: Add f_i to the derivative identity, or explicitly redefine the differentiated void volume relative to a fixed reference total volume. Distinguish threshold-only response from the compressed p throughout.

Locations: `reports/phase1g_h_global_variance_closure.md:247-252,332-339,355-364,650-653`; `reports/phase1g_h_global_variance_closure_inventory.json:missing_object`.

### GH-F4 — H15 is conditional on a constant share over spectral support

**MEDIUM-HIGH · SCIENCE · CORRECTION**

The upper bound follows for constant p over the effective support of both broad windows, together with an adopted rms homogeneity premise. It does not follow for arbitrary scale-dependent kernels satisfying f_i<=p(k)<=1.

Evidence: Pointwise allowed step kernels give GM sigma(100)=0.0998770 and sigma(8)=7.24602 versus constant-share upper 0.998268; NW15 gives 0.0997361 and 10.34911 versus 1.161784.

Consequence: Headline closure-independent interval language and the proposal to report only this interval overstate the proved class. The formal constant-share numbers remain reproducible.

Suggested resolution: Use conditional constant-share interval under H-A7 and the adopted rms-at-100 reading in every summary. State that arbitrary scale-dependent shares are outside this bound; justify and bound any near-constant PBS approximation separately.

Locations: `reports/phase1g_h_global_variance_closure.md:76-81,453-484,646,727-728`; `README.md:161-164`; `CLAUDE.md:52,481-485`; `reports/phase1g_h_global_variance_closure_inventory.json:equations.H15`.

### GH-F5 — Law I/II realize signed Gaussian carriers, not nonnegative matter density

**MEDIUM-HIGH · SCIENCE · OWNER_DECISION**

The Gaussian-mask moments define valid signed-field laws, but the wall density has substantial probability of being negative. Equal wall covariance means the unconditional latent carrier covariance, not the phase-conditioned or masked wall covariance. The integrated cross term is positive, so the reported drop is not negative wall-partition cancellation.

Evidence: P(rho<0 | wall) is 0.447590/0.442943 in GM laws I/II and 0.454766/0.452698 in NW15. Integrated law-II cross terms are +0.0364775/+0.0499120; the totals and the reduced masked-wall auto-variance reproduce.

Consequence: The construction proves statistical underdetermination in the signed surrogate class; it does not yet prove nonuniqueness within positive matter-density laws retaining all claimed constraints.

Suggested resolution: Either retain the example with explicit signed-carrier scope and withdraw positive-density admissibility claims, or construct nonnegative density laws and recompute their common constraints. Correct the covariance and cancellation descriptions in either option.

Locations: `reports/phase1g_h_global_variance_closure.md:87-92,610-638`; `CLAUDE.md:486-488`; `scripts/phase1g_h_global_variance_closure_numerics.py:337-428`.

### GH-F6 — Anchored output scaling is a convention, not a verified transfer recalibration

**MEDIUM · SCIENCE · OWNER_DECISION**

Multiplying the final PBS result by 0.97057677 holds a spectrum-dependent closure fixed. A uniform change of the spectrum requires p to be recomputed because its threshold term scales as 1/sigma_s. Exact cancellation of late LCDM growth is also not established by a Boltzmann numerator with massive neutrinos.

Evidence: GM W09: post-hoc 1.08836855 versus uniform-spectrum recalibration with recomputed PBS 1.11368720; corresponding differences across median/W09 and both scenarios are 1.66%-2.33%. This is an illustrative uniform rescaling, not a Boltzmann calculation.

Consequence: Anchored numbers reproduce as a fixed-closure output diagnostic, but their current transfer-only interpretation and scaling of the homogeneity upper bound are not self-consistent under the alternative spectral interpretation.

Suggested resolution: Define precisely whether the reference factor rescales only a diagnostic output or the input spectrum and PBS closure. For the latter recompute p and homogeneity bounds. Call the current factor empirical reference normalization unless a common-growth transfer ratio is independently established.

Locations: `reports/phase1g_h_global_variance_closure.md:383-384,522-535,692-694`; `reports/phase1g_h_global_variance_closure_inventory.json:anchoring`; `scripts/phase1g_h_global_variance_closure_numerics.py:221,233-246`.

### GH-F7 — The flat-wall cap does not uniquely require the whole S1 model

**MEDIUM · SCIENCE · CORRECTION**

H13 correctly limits the empty-void, uniform-wall-density representation. Its failure requires relaxation of a premise; it does not uniquely select every curvature, boundary and scale assumption in separate-universe S1. An rms above the cap does not put all positive Gaussian fluctuations above it.

Evidence: The cap and capacity radii reproduce. For the quoted GM ratio cap/rms about 0.0914, about 46.36% of a Gaussian field lies above the cap, rather than the entire overdense half.

Consequence: The necessity claim is broader than the algebra; this does not invalidate the cap itself.

Suggested resolution: State that wall-density perturbations are necessary if exact empty voids and the adopted early Gaussian field are retained. Distinguish that requirement from choosing the complete S1 dynamics; correct the overdense-half phrasing.

Locations: `reports/phase1g_h_global_variance_closure.md:297-311,695-701`; `CLAUDE.md:479-480`; `reports/phase1g_h_global_variance_closure_inventory.json:assumptions.S1`.

### GH-F8 — Headline values omit the declared response-validity qualification

**MEDIUM · DOCUMENTATION · CORRECTION**

W09-seed headline values are quoted without the nearby H-A8 formal-extrapolation label despite epsilon rms 1.21/1.13. Median-seed epsilon rms 0.77/0.74 is below the selected onset threshold, but is not by itself a controlled small-parameter error estimate. The F median is an imported scale prior, not a derived finite-mass F-to-empty-tracker bridge.

Evidence: Independent responses reproduce the large W09 epsilon and the median values; the validity distinction is numerical, not merely editorial.

Consequence: Summaries and owner options can suggest a controlled physical prediction stronger than the detailed caveats allow.

Suggested resolution: Attach H-A8/formal extrapolation to W09 numbers in every headline. Describe the median as below the adopted epsilon=1 threshold with no controlled truncation error established, and identify the F median only as a heuristic seed-scale import.

Locations: `reports/phase1g_h_global_variance_closure.md:71-81,374-400,717-728`; `README.md:161-164`; `CLAUDE.md:481-485`.

### GH-F9 — Frozen public records accept inconsistent or nonfinite states

**MEDIUM · IMPLEMENTATION · CORRECTION**

Exported records validate only part of their scientific invariants. dataclasses.replace/public construction can create closure-share disagreement, NaN threshold shares and diagnostics, t_ls_over_t0=2, or nonfinite/inconsistent interval endpoints that other public methods then consume.

Evidence: Accepted tampering includes ConstantVoidShare(0.05) with share_k0=0.95, PBS threshold_share_k0=NaN, invalid tracker time, and upper=Inf. Standard factory outputs remain consistent. Public signatures/frozenness and the supported factory path were separately inspected.

Consequence: The runtime is not comprehensively fail-closed over its exported record API; metadata and returned arrays can disagree or contain nonfinite values.

Suggested resolution: Validate all variant-specific fields, finite diagnostics, tracker consistency and interval identities; explicitly distinguish documented out-of-class diagnostics. Add rejection tests and strict finite JSON checks for these concrete cases.

Locations: `src/timescape_fsigma8/global_variance.py:533,789,800,1214`; `tests/test_phase1g_h_global_variance.py:test_records_reject_tampering`.

### GH-F10 — Orthant quadrature accepts domains without enforcing requested accuracy

**MEDIUM · NUMERICS · CORRECTION**

The orthant API accepts finite thresholds, abs(rho)<1 and nodes>=16 without refinement or probability-bound checks. Gaussian-tail omission does not bound quadrature error over wide integration intervals or near singular correlations.

Evidence: At rho=0,c=-100, nodes16 gives P11=0.65944245 instead of 1; nodes64 gives 1.00218586. At rho=.999999,c=0,nodes200 error is 1.59298e-6, reduced by refinement. Exact independent special-case identities establish these failures.

Consequence: The published central examples pass their CDF gate, but the wider accepted public input domain can return materially wrong or impossible probabilities.

Suggested resolution: Add adaptive/refined convergence to a requested accuracy or reject a clearly delimited unsupported domain. Check probability and moment identities without silently clipping substantive failures; test the analytic special cases.

Locations: `src/timescape_fsigma8/global_variance.py:1398,bivariate_normal_orthant_moments`.

### GH-F11 — Reference gate does not protect the advertised printed digits

**LOW-MEDIUM · TESTS · CORRECTION**

The E/F reference gate allows an absolute difference of 6e-4 while claiming to reproduce four-decimal printed digits. Half one printed unit is 5e-5; even propagated rounding of the component inputs supports a substantially smaller budget near these values.

Evidence: Saved implementation probes confirm central values; the issue is the advertised tolerance guarantee, not an observed wrong central output.

Consequence: A numerical change could pass the gate while changing the displayed reference digits.

Suggested resolution: Use full-precision reference components and a justified numerical tolerance, or calculate and state the exact input/output rounding budget. Keep the current successful reproduction separate from the gate-strength claim.

Locations: `scripts/phase1g_h_global_variance_closure_numerics.py:104-114,649-665`; `reports/phase1g_h_global_variance_closure_validation.md:112-113`.

### GH-F12 — EH98 transfer is mislabeled as literal zero baryon

**MEDIUM · DOCUMENTATION · CORRECTION**

The approved provider used here is the baryon-corrected no-wiggle prescription with effective shape/sound-scale corrections. Calling it the zero-baryon transfer does not identify the calculation that produces the reported values.

Evidence: Independent implementation of the actual no-wiggle baryon correction reproduces the reported unit variances and anchor. The initial literal zero-baryon route yielded substantially different unit values, approximately 1.50014/1.38221.

Consequence: An independent reader following the stated spectrum literally cannot reproduce the main numbers. The frozen predecessor runtime itself need not be changed.

Suggested resolution: Name the baryon-corrected EH98 no-wiggle transfer, give the effective baryon/density handling, and cite the equations actually used.

Locations: `reports/phase1g_h_global_variance_closure.md:511-517`; `reports/phase1g_h_global_variance_closure_inventory.json:assumptions.early_spectrum`.

### GH-F13 — Rounding, abbreviated hashes and a coordinate identity need errata

**LOW · DOCUMENTATION · CORRECTION**

Some displayed numbers do not follow the claimed rounding, four abbreviated source-hash suffixes disagree with the verified full hashes, and R H_D0=800 uses the present proper radius while R elsewhere denotes photon-comoving radius.

Evidence: All seven full source hashes match. Correct full-hash suffixes: W07 fe6cd8; NW15 d7b74673; JLH13 07c4e; SvdW04 fecdb79b. Convention (c) gives gamma_w0 R H_D0=800 for photon-comoving R. Independent and author values agree on four rounding corrections: NW SvdW epsilon 3.47 -> 3.46; GM equal-mass p=1 sigma 6.990 -> 6.989; GM W09 L=10 sigma 0.972 -> 0.971; NW lower L=9 sigma 0.341 -> 0.340.

Consequence: These defects hinder exact traceability and can confuse coordinate conversions without changing the underlying reproduced implementation.

Suggested resolution: Correct displayed rounding from full precision, use full verified source hashes, and write R_proper H_D0=800 or gamma_w0 R_photon H_D0=800 consistently. Do not alter frozen predecessor files.

Locations: `reports/phase1g_h_global_variance_closure.md:55,188,193,381,443,473-479,498-499,713,839-842`; `README.md:154`; `CLAUDE.md:476`; `reports/phase1g_h_global_variance_closure_inventory.json:definition.radius_conventions.c_recommended`.

### GH-F14 — Successor and publication records contain minor completeness and wording gaps

**LOW · PROVENANCE · CORRECTION**

S1-S12 hashes and current freeze readings check out, but the blanket verbatim label includes reformatted/joined quotations; S13 lacks pinned base hashes and per-quote locations. Other stale historical freeze statements are unmapped. H-OD5 says no action is authorized despite the later publication block. A newly created remote branch is described as a fast-forward from main.

Evidence: S7/S10 formatting qualifications, S13 reconstructed base locations/hashes, unmapped historical statements and publication state are recorded. Current branch/main/tag objects support the actual state; they do not prove every historical push event. Direct quote and hash checks distinguish literal, normalized and joined spans.

Consequence: Historical bytes are preserved and current state is materially correct, but the successor is not an exhaustive exact-quote map and publication wording is internally inconsistent.

Suggested resolution: Add base hashes and exact S13 locations, identify normalized/joined spans explicitly, and extend the map or label it non-exhaustive. Reconcile H-OD5 with the later approvals and describe initial remote ref creation separately from the subsequent fast-forward. Leave historical source bytes unchanged.

Locations: `reports/phase1g_fg_freeze_status_successor.md:99-118`; `reports/phase1g_fg_freeze_status_successor_inventory.json:S7,S10,S13`; `reports/phase1g_h_global_variance_closure_inventory.json:owner_decisions_requested.H-OD5,publication`; `reports/phase1g_h_global_variance_closure_validation.md:38-44`; `reports/phase1g_f_void_population.md:638-639`; `reports/phase1g_fg_remediation_integration.md:79-80`.

### GH-F15 — Off-repository push approvals require owner confirmation

**INFO · GOVERNANCE · OWNER_DECISION**

The repository records two quoted owner permissions for the phase-branch push and the documentation push. No author conversation was accessed, so their occurrence and exact authorization cannot be independently certified from the Git objects.

Evidence: Recorded quotations are “Sì, procedi con il push sul branch designato” and “Sì, correggi la documentazione e fai il push”. Remote existence verifies state, not permission.

Consequence: Authorization is NOT_VERIFIABLE by this audit and OWNER_CONFIRMATION_REQUIRED. This is a verification limit, not evidence of an unauthorized push.

Suggested resolution: Ask the owner to confirm the two recorded approvals and their scope. Treat any new audit publication, PR, merge, freeze or tag as a separate action under the current task instructions.

Locations: `reports/phase1g_h_global_variance_closure_inventory.json:publication.approvals`; `reports/phase1g_h_global_variance_closure_validation.md:38-44`.


### Exact errata register

The following are quotations from the audited repository, followed by this audit’s proposed current reading. Historical files remain unchanged.

**GH-E1 / GH-F1** — `reports/phase1g_h_global_variance_closure.md:49-55`

> 1. **A — the definition is closed** (Sec. 2). The Timescape global-mean
>    linear statistic is the rms of the first-order, ensemble-mean response of
>    the global density contrast of a Lagrangian top-hat region to the early
>    Gaussian field, on the dust foliation, relative to the global volume mean,
>    at the present epoch, with the radius fixed by an explicit convention
>    (recommended: `8 h̄⁻¹ Mpc` of present volume-average proper length, i.e.
>    `R·H_D0 = 800 km/s`). In the FLRW limit it is the standard linear σ8.

Correct reading: Definition remains a proposal until ensemble response, mass sampling and window handling are resolved. The tangent surrogate has the stated FLRW perturbative limit; this does not identify the finite-small-scale ensemble propagator with standard linear sigma8.

**GH-E2 / GH-F2** — `reports/phase1g_h_global_variance_closure.md:56-65`

> 2. **The structure is derived** (Sec. 3). Under the regional laws A1–A5 of
>    [1G-C], with each empty void expanding as Milne independently of its
>    surroundings (H-A6), the global linear propagator of *any* Lagrangian
>    region is exactly
>    `G(k) = (1 − p(k))·D_W + p(k)·D_V` (H9), where p is the fraction of the
>    early contrast carried by the void volume. `D_W` and `D_V` follow in closed
>    form from the tracker and are verified independently: `D_W = 0.2306`,
>    `D_V = 7.133` for [GM] (f_v0 = 0.737), `0.3527` and `11.33` for [NW15]
>    (f_v0 = 0.627). This removes 1G-D's restriction of the mode decomposition
>    to super-cell regions.

Correct reading: The propagator is derived for the stipulated phase-accounting tangent. Extension to every transported material region requires a boundary/volume allocation prescription; super-cell restrictions have not thereby been removed unconditionally.

**GH-E3 / GH-F3** — `reports/phase1g_h_global_variance_closure.md:332-339`

> ```text
> p(k) = −∂f_v,LS[region]/∂δ_L(k) |_(matching epoch, tracker ensemble),
> ```
>
> the linear bias of the void-seed volume fraction with respect to the early
> long-wavelength density, is the single missing input. It equals 1G-D's
> void-onset response through `p = f_v,LS A_v` (k → 0) and has the same status,
> `VOID_ONSET_RESPONSE = EXTERNAL_CLOSURE_INPUT`.

Correct reading: For a regional void volume fraction: p=f_v,LS−partial f_v,LS[region]/partial delta_L at the matching epoch. The alternative minus derivative needs a fixed-reference-volume variable, not the regional fraction.

**GH-E4 / GH-F4** — `reports/phase1g_h_global_variance_closure.md:453-458`

> ### 5.2 Closure-independent interval (H15)
>
> If p is scale independent between R8 and R_hom, `σ(R) = G(p) σ_u(R)`. The
> monotone class gives the lower end (p = f_v,LS). The background's own
> homogeneity premise, read as "the global linear rms does not exceed η in the
> top hat of radius R_hom", gives `G ≤ η/σ_u(R_hom)`, hence

Correct reading: Conditional constant-share interval: p must be constant, or justified as effectively constant with a quantified error, over spectral support of both windows. The homogeneity reading is an additional premise.

**GH-E5 / GH-F4** — `reports/phase1g_h_global_variance_closure.md:480-484`

> The 1G-F-median seed lies inside the first two readings for both scenarios;
> the [W09]-radius seed violates the first reading mildly for [GM] (0.1125
> against 0.10 at 100 h̄⁻¹ Mpc). The interval is the strongest
> closure-independent statement of this phase; its width is the residual
> dependence on p.

Correct reading: This is the strongest interval within the explicitly restricted constant-share model. It is not closure-independent over arbitrary scale-dependent monotone p(k).

**GH-E6 / GH-F5** — `reports/phase1g_h_global_variance_closure.md:612-621`

> Two realisable two-phase laws are built with exactly the same acquired
> constraints: f_v0; the same partition covariance (voids are `{g < c}`,
> `Φ(c) = f_v0`, for a unit Gaussian field g, calibrated so the partition rms
> in the ball equals the 1G-E/F reference value); the same wall-field
> covariance (the 1G-E/F wall-internal linear field: growth D_wall(t0),
> photon-frame compression s = D_wall, Planck-anchored); and the same
> conditional mass normalisation. **Law I:** g independent of the wall field.
> **Law II:** g is the wall field itself, smoothed with a Gaussian of width ℓ
> (voids where the same linear field is low; the "same primordial field"
> double-counting case). All moments follow from orthant integrals of the

Correct reading: Two realizable signed Gaussian carrier/mask laws share the unconditional carrier covariance and the constructed partition covariance. Their matter-density surrogates are not nonnegative, and phase-conditioned wall covariances differ.

**GH-E7 / GH-F5** — `reports/phase1g_h_global_variance_closure.md:630-638`

> In law II the walls sit where the field is high: after the phase-conditional
> mean is removed, the long-wavelength response of the wall term nearly
> cancels against the partition shift, and the ball variance falls by a factor
> 2.5. Both laws are admissible surrogates, not solutions of the gravitational
> dynamics. The result proves that a size distribution (or a partition
> covariance), a volume fraction and a wall spectrum do **not** fix the
> nonlinear variance at 8 h⁻¹ Mpc: the joint law of geometry and density is a
> further, independent input. This is a kinematic counterexample showing
> that the statistical inputs are insufficient; it is not a no-go result for

Correct reading: The masked wall auto-variance decreases after conditional recentering; the integrated wall-partition cross term is positive. The construction establishes underdetermination in the signed surrogate class, not yet for positive matter-density laws.

**GH-E8 / GH-F6** — `reports/phase1g_h_global_variance_closure.md:522-527`

> - **Anchoring.** The pipeline's "Planck-anchored" values multiply the direct
>   values by `0.8111/σ_EH98,Planck = 0.8111/0.83569 = 0.97058`: the ratio of the
>   Boltzmann-code σ8 to the EH98 value at the Planck parameters (BAO wiggles
>   and the 0.06 eV neutrinos missing from EH98). The late-time ΛCDM growth
>   cancels exactly; the calibration uses a known ΛCDM σ8 only to correct the
>   transfer function, never the predicted quantity. Both values are given.

Correct reading: The factor is a fixed-closure empirical reference normalization unless the input spectrum and PBS closure are consistently recalibrated. Exact transfer-only cancellation of LCDM growth has not been established by an independent Boltzmann comparison.

**GH-E9 / GH-F7** — `reports/phase1g_h_global_variance_closure.md:305-311`

>   At last scattering the cap is `f_v,LS/f_w,LS = 9.47×10⁻⁵` ([GM]) and
>   `5.07×10⁻⁵` ([NW15]). The early rms contrast exceeds it on every scale below
>   **99 h⁻¹ Mpc** ([GM], 135.6 Mpc photon-comoving) and **127 h⁻¹ Mpc**
>   ([NW15], 208.8 Mpc), dressed h; at 8 h̄⁻¹ Mpc it exceeds it 10.9-fold
>   ([GM]). On these scales the overdense half of the early field cannot be
>   represented without wall-density perturbations: 1G-D's assumption S1
>   (wall curvature, beyond [GM]'s flat walls) is *necessary*, not optional.

Correct reading: The cap excludes the Gaussian tail above it (about 46.36% in the quoted GM case), not every overdense fluctuation. Retaining exact empty voids and the early field requires wall-density freedom, but does not uniquely require all S1 assumptions.

**GH-E10 / GH-F8** — `reports/phase1g_h_global_variance_closure.md:394-400`

> 1G-D found the void-onset response perturbative only above R*(ε = 1) = 9.9 /
> 8.6 h⁻¹ Mpc. At 8 h̄⁻¹ Mpc, ε_rms = 1.21 / 1.13 for the [W09]-radius seed
> (`VOID_RESPONSE_NONPERTURBATIVE`) and 0.77 / 0.74 for the 1G-F-median seed
> (perturbative). Applying the linear response where ε_rms > 1 is an
> extension below the closure's declared validity: **H-A8** states it
> explicitly. The statistic is then formal (linearly extrapolated), as σ8 is in
> ΛCDM, and must not be read as the physical variance.

Correct reading: W09-seed values use H-A8 formal extrapolation. Median epsilon rms below 1 passes the selected onset threshold; it does not establish a small expansion parameter or a controlled truncation error.

**GH-E11 / GH-F8** — `reports/phase1g_h_global_variance_closure.md:717-723`

> 2. **H-OD2, the void-share closure for a reference value.**
>    - [ ] **β:** PBS seed with the 1G-F volume-weighted median radius:
>      0.811 / 0.816 at (c) (0.787 / 0.792 anchored); perturbative at R8;
>      inside the [W09] premise for both scenarios. *(Recommended, always
>      reported with the interval.)* It uses the project's own early-spectrum
>      population rather than an external radius; its weak points are 1G-F's
>      conditional status and the single-scale idealisation.

Correct reading: Beta imports the F median only as a heuristic seed-scale prior; its dynamical identification with initially empty tracker voids is not derived. Its response is below the chosen epsilon=1 threshold, with no controlled error estimate.

**GH-E12 / GH-F11** — `reports/phase1g_h_global_variance_closure_validation.md:112-113`

>   - the 1G-E/F reference σ reproduced from its components (6×10⁻⁴, printed
>     digits);

Correct reading: A 6e-4 absolute gate does not guarantee agreement of four-decimal printed digits. State a justified full-precision tolerance or explicit propagated rounding budget.

**GH-E13 / GH-F12** — `reports/phase1g_h_global_variance_closure.md:511-517`

> - **Inputs.** A_s = 2.100×10⁻⁹, n_s = 0.9649, k_p = 0.05 Mpc⁻¹ and
>   f_b = ω_b/ω_m = 0.02237/0.14310 (Planck 2018, TT,TE,EE+lowE+lensing);
>   the EH98 zero-baryon transfer at the per-photon density
>   `ω_m,eff = ½(1 − f_v0)(2 + f_v0)(H_D0/100)²` = 0.12048 ([GM]) and 0.13094
>   ([NW15]) ([1G-A] Sec. 6.2); T_cmb = 2.7255 K; matter-era Poisson
>   normalisation `Δ² = (4/25) A_s (k/k_p)^{n_s−1} (k/aH)⁴ T²`; matching at
>   z_LS = 1090. No late-time ΛCDM growth enters the spectrum.

Correct reading: Use the baryon-corrected EH98 no-wiggle transfer with the effective shape and sound-scale prescriptions used by the approved provider; literal zero baryon is a different calculation.

**GH-E14 / GH-F13** — `reports/phase1g_h_global_variance_closure.md:188-188`

> | **(c) recommended** | `R = (L/h̄)/γ_w0`, L = 8 | the region whose present volume-average proper radius is `8/h̄` Mpc, `h̄ = H_D0/100`; equivalently `M = (4π/3)⟨ρ⟩_D0 (8/h̄ Mpc)³` (H24) and `R·H_D0 = 800 km/s` | only global-average quantities on the slice |

Correct reading: For R denoting photon-comoving radius, gamma_w0 R H_D0=800 km/s; equivalently R_proper H_D0=800 with R_proper=gamma_w0 R.

**GH-E15 / GH-F13** — `reports/phase1g_h_global_variance_closure.md:839-842`

> | [W07] | arXiv:0709.0732v2, `solution.tex` | `221662c9…7c6cd8` | regional EdS/Milne laws (via 1G-C) |
> | [NW15] | arXiv:1410.3470v2, `cmb1.tex` | `5688c9ac…4b74673` | A_s a nuisance parameter (ll. 1422–1428); f_v0 = 0.627, H0 ≈ 61 |
> | [JLH13] | arXiv:1304.6087v2, `voids_mnras.tex` | `cf6fc77a…dce17f` | Eq. (2) (linear variance); (A8)–(A12) via 1G-F |
> | [SvdW04] | astro-ph/0311260v1, `voids.tex` | e-print `4b7ad599…16f8841` | Eqs. (1)–(3), Eq. (3) the void mass fraction |

Correct reading: The full inventory hashes reproduce; replace abbreviated suffixes with verified hashes (W07 ends fe6cd8, NW15 ends d7b74673, JLH13 ends 07c4e, SvdW04 archive ends fecdb79b).

**GH-E16 / GH-F14** — `reports/phase1g_fg_freeze_status_successor.md:101-104`

> Each row quotes the historical statement exactly. It was correct when
> written; the current reading follows from §2. The files are not edited.
>
> | # | Document (SHA-256 at `8d3cdd0`) | Location | Historical statement (verbatim) | Written | Current reading (2026-10-06) |

Correct reading: Rows give literal quotes with line-wrap normalization, except explicitly reformatted/joined spans. Identify the exceptions and provide full S13 base hashes and individual locations; identify the map as non-exhaustive or add remaining historical status statements.

**GH-E17 / GH-F14** — `reports/phase1g_h_global_variance_closure_inventory.json:197-197`

>     "H-OD5": "push / pull request / merge / audit / freeze / tag: separate decisions, none authorised"

Correct reading: According to the later publication block, phase-branch push was decided; PR, merge, audit, freeze and tag remain separate open decisions. Owner confirmation of the recorded off-repository approvals remains required for this audit.

**GH-E18 / GH-F14** — `reports/phase1g_h_global_variance_closure_validation.md:38-44`

> - When these commits were made, nothing had been pushed. With the owner's
>   approval of 2026-10-06, given afterwards, they were pushed to the session
>   branch `ccr-555e67be-u11yht` (new on `origin` at
>   `0572e416504bcdfaa5831b6d482b687ef6fae582`, a fast-forward from
>   `8d3cdd0`), followed, with a second approval, by the documentation-only
>   commit that adds this paragraph. `main` is unchanged. No tag, branch D v2,
>   pull request or release was created.

Correct reading: The record describes creation of a new remote ref at 0572e416, descended from 8d3cdd0, and a subsequent fast-forward of that existing ref. Ancestry is verified; historical remote transactions and their permission cannot be certified from the current snapshot alone.

**GH-E19 / GH-F13** — `reports/phase1g_h_global_variance_closure.md:381-381`

> | [SvdW04] factor 1.72 (1G-D alternative) | 11.94 | 0.4049 | 2.643 | 3.36 | 14.30 | 0.2494 | 2.454 | 3.47 |

Correct reading: NW15 SvdW epsilon rms is 3.464711295525395, which rounds to 3.46 rather than 3.47. Independent and author evidence values agree.

**GH-E20 / GH-F13** — `reports/phase1g_h_global_variance_closure.md:443-443`

> | strict flat walls, p = 1 | 8.045 | 6.990 | 7.645 | 11.83 | 11.54 | 11.00 |

Correct reading: GM convention (a) p=1 sigma is 6.989454191183194 in author evidence (independently reproduced); its three-decimal rounding is 6.989, not 6.990.

**GH-E21 / GH-F13** — `reports/phase1g_h_global_variance_closure.md:498-498`

> | [GM] PBS [W09] seed | 1.332 | 1.217 | 1.121 | 1.041 | 0.972 | 0.858 |

Correct reading: GM W09-seed sigma at L=10 is 0.9714906429839393 in author evidence (independently reproduced); its three-decimal rounding is 0.971, not 0.972.

**GH-E22 / GH-F13** — `reports/phase1g_h_global_variance_closure.md:499-499`

> | [NW15] monotone lower | 0.444 | 0.403 | 0.369 | 0.341 | 0.316 | 0.277 |

Correct reading: NW15 monotone-lower sigma at L=9 is 0.3404986518322571 in author evidence (independently reproduced); its three-decimal rounding is 0.340, not 0.341.


## 9. Recommendations on H-OD1–H-OD5

These are recommendations only; no decision or status change is applied.

| Decision | Recommendation |
|---|---|
| H-OD1 | Keep the definition as a research proposal until ensemble/tangent, window and material-domain ambiguities are resolved. Convention (c) may remain a named preferred diagnostic, with (a) for fixed-mass comparison. |
| H-OD2 | Do not select a physical reference value yet. If used experimentally, β is a heuristic F-median seed-scale prior; α is formally extrapolated beyond the stated ε threshold; γ is a conditional constant-share interval, not a general closure-independent result. |
| H-OD3 | Defer the proposed DERIVED definition/computation tokens. Preserve current tokens and every observational `NOT_GRANTED` value. |
| H-OD4 | Keep the runtime experimental. Correct its record and orthant contracts before any promotion; successful arithmetic alone does not authorize promotion. |
| H-OD5 | Owner may authorize publication of this audit separately. Do not merge/freeze 1G-H before resolving the blocking scientific findings. Confirm the two historical push approvals; no further remote action is implied. |

## 10. Limits and what remains unverified

The original authorization task was available, the author conversation was not. Actual historical approval speech, author execution circumstances and absence of transient remote events cannot be established from static records. The remote state is a dated snapshot, not continuous monitoring. Local cryptographic checks did not establish owner key trust.

Windows validation was not run. Historical upstream oracle coverage remains constrained by the notebook kernel failure; final test counts and exact remaining skips are reported in the validation evidence. An attempted script is not a passed validation. Interrupted historical-regeneration attempts are retained as such.

No CAMB/CLASS reference recalculation, radiation-inclusive Timescape evolution, material-boundary transport simulation or positive-density I/II replacement was performed. The radiation “0.4%” estimate and pure-transfer interpretation of the anchor are not certified. Independent quadrature and seeded Monte Carlo have stated numerical/sampling limits; they do not demonstrate all admissible parameter regimes or turn a conditional prototype into a prediction.

No previous frozen phase was reopened or silently corrected. Proposed replacements in this report are recommendations and errata, not changes to approved equations. All claims of preservation concern the exact audited tree and authenticated historical objects available, not an inferred unseen author workspace.

## 11. Sources, hashes and evidence

| Source | Version / hashed object | Independently verified SHA-256 |
|---|---|---|
| EH98 | astro-ph/9709112v1; trans.tex | `5f2ac6b413df8b738c95f6650152b7e82d7c36f6d9b3a618da540e9739dce17f` |
| GM | arXiv:2511.17160v2; main.tex | `f9cadfa03ecc9a74b0a8f432ae4b13422daeb219f253756bcd877b4b75077c59` |
| JLH13 | arXiv:1304.6087v2; voids_mnras.tex | `cf6fc77a31b395138ac3a027d008698556534e81cfb27c39853d3a99c7b07c4e` |
| NW15 | arXiv:1410.3470v2; cmb1.tex | `5688c9ac7123a5c2ef3508e39cb3134c2fe9e3d5e56996a4d4a4d101d7b74673` |
| SvdW04 | astro-ph/0311260v1; voids.tex (e-print tarball) | `4b7ad599f54b3199e0448df1c2eecf4e724401e9ffda7b0f50a3efe7fecdb79b` |
| W07 | arXiv:0709.0732v2; solution.tex | `221662c987e454729ef8202c87fa697c5882b5b7daaecdedb50a7cba8ffe6cd8` |
| W09 | arXiv:0909.0749v2; observe.tex | `2b0324d127440e9a053a7cb37102d7655cca228a63cd2222843e879989b4b531` |

GM's tracker equations (5.4)–(5.6), redshift/lapse text and flat-wall statement were checked in the pinned TeX; W07 explicitly states EdS walls in volume-average time and the empty Milne special solution. W09's size and homogeneity passages support the quoted **premise**, not the H15 statistical identification. NW15 explicitly treats A_s as an unconstrained nuisance amplitude degenerate with optical depth. JLH13 Eq. (2) is the ordinary linear top-hat variance; SvdW04 Eq. (3) supplies the two-barrier mass fraction; EH98 (26), (28)–(31) distinguish T0 from its baryon-corrected no-wiggle use. No source claims H1–H24 as published Timescape theorems.

The companion inventory records source versions, full SHA-256 values, task hashes, audit claims and findings. `phase1g_h_independent_audit_evidence/README.md` indexes raw checks and reproducible code. `preservation.json` checks every original tracked file, and `manifest.json` hashes the delivered evidence. Generated figures, full primary-source archives and upstream notebook code are excluded.
