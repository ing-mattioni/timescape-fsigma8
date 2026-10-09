# Phase 1G-B — contract-hardening successor (2026-10-09)

Classification: `CONTRACT_HARDENING_SUCCESSOR_RECORD` (record invariants of
the conditional, model-internal σ(M) runtime; no scientific content).
Date: 2026-10-09.
Companion: [`phase1g_b_contract_hardening_successor_inventory.json`](phase1g_b_contract_hardening_successor_inventory.json).

Cited as:
- [1G-B] = [`phase1g_b_lagrangian_sigma_validation.md`](phase1g_b_lagrangian_sigma_validation.md)
  (frozen) and `src/timescape_fsigma8/lagrangian_sigma.py`;
- [OD] = [`phase1g_b_owner_decisions_successor.md`](phase1g_b_owner_decisions_successor.md)
  (GB-OD2 … GB-OD6, 2026-09-30, the precedent for record hardening);
- [H-D3] = [`phase1g_h_delta_audit_3.md`](phase1g_h_delta_audit_3.md), the
  third delta audit of Phase 1G-H, finding GH-D3F4.

The frozen [1G-B] report, [OD], the audit records and every tag are
unchanged; the tags keep pointing at their commits.

## 1. Authorisation

[H-D3] classed GH-D3F4 `OWNER_DECISION`. On 2026-10-09 the session that
remediates 1G-H proposed three options: (a) a 1G-B contract-hardening
successor in a separate commit and record, with bit-identical numerical
outputs and no tag change; (b) defer; (c) documentation only. The owner
approved the plan with option (a), verbatim: «Perfetto, procedi».

## 2. Finding GH-D3F4

[H-D3] §10, LOW-MEDIUM, IMPLEMENTATION: "Unchanged LCDMReferenceLinearSigma
accepts non-finite error diagnostics; AnchoredLagrangianSigmaRatio accepts
arbitrary positive growth_ratio/early_spectrum_factor without binding their
decomposition." Direct construction could therefore export non-finite
diagnostics or a factor of 999. No computed 1G-B, 1G-C … 1G-H value was
affected: the factories produce consistent records. 1G-H does not import
either class.

## 3. Changes (`src/timescape_fsigma8/lagrangian_sigma.py`)

- **`LCDMReferenceLinearSigma.__post_init__`.** `quadrature_relative_change`
  and `truncation_envelope_fraction` must be finite real numbers and
  non-negative, as `ConditionalLagrangianSigma` has required since GB-OD4.
  The relative change must equal `abs(sigma_unit_growth /
  sigma_unit_growth_comparison_grid - 1)`, the expression of `_quadrature`,
  and both diagnostics must lie within the quadrature's declared
  `self_convergence_tolerance` and `truncation_tolerance`, as `_quadrature`
  already enforces when it computes them.
- **`AnchoredLagrangianSigmaRatio.__post_init__`.** `growth_ratio`,
  `early_spectrum_factor`, `sigma_ratio` and `reference_offset_from_anchor`
  must equal the expressions of `anchor_lagrangian_sigma` on the stored
  `timescape`, `reference` and `anchor_value`. `early_spectrum_differences`
  must name exactly the early-spectrum inputs (`A_s`, `n_s`,
  `k_pivot_per_Mpc`, `baryon_fraction`) that differ. The documented
  decomposition `sigma_ratio = growth_ratio × early_spectrum_factor` then
  holds through its factors to rounding (a test checks 10⁻¹⁴).

The comparisons are exact equalities of the factory's own expressions, the
convention of the existing 1G-B invariants (for example `linear_sigma`). No
equation, tolerance, default, factory, output key or status token changes.

**Not changed (limits).** The factory-only contracts of
`anchor_lagrangian_sigma` (same quadrature, transfer model and T_cmb, the
equal-mass reference match, the anchor-consistency rationale) are not
repeated in the record. Scalars are not normalised: 1G-B records,
these two included, validate scalars as `numbers.Real` without converting
them, so a `Fraction` or NumPy scalar is stored as given and their own
exports can fail strict JSON ([H-D3] GH-D3F2). The exact equalities follow
Python and NumPy comparison rules. NumPy compares a `numpy.float32` with a
Python float in single precision, so a `float32` rounding of the exact
value passes and is stored as `float32`. The binding then holds to the
precision of the stored scalar type: this is the GH-D3F2 scalar
representation, not an unbound value. 1G-H now refuses such nested inputs
in its own records; the 1G-B exports are unchanged.

## 4. Equivalence (AGENTS.md rule 3)

- `scripts/validate_phase1g_b_lagrangian_sigma.py` before and after the
  change: artifact `artifacts/independent/phase1g_b_lagrangian_sigma.json`
  byte-identical (SHA-256
  `5746cc76e932ad0db3e253ee5aa5f0032227e65afba1699a09ea1f2c32d13c8d` both
  times, CPython 3.13.16), every gate passing.
- The existing 1G-B tests (124 in `test_phase1g_b_lagrangian_sigma.py` and
  `test_phase1g_b_owner_decisions.py`) pass unchanged.
- New tests: `tests/test_phase1g_b_contract_hardening.py`, 18 cases (genuine
  records accepted; NaN, ±∞, negative and `Decimal` diagnostics refused;
  diagnostics bound to the quadrature; each ratio, the offset, a consistent
  but unbound `sigma_ratio = 999` and the difference list refused; the
  decomposition to rounding).
- Mutants of each new check (L01–L05 in the 1G-H third-remediation logs):
  all killed by these tests.
- The third delta audit's scalar probes
  (`reports/phase1g_h_delta_audit_3_evidence/implementation_scalar_probes.py`,
  run unchanged on `ed0ec0c` and on this tree, CPython 3.13.16): of 1446
  probes, 18 on `LCDMReferenceLinearSigma` and 10 on
  `AnchoredLagrangianSigmaRatio` change from accepted to refused, among them
  every non-finite diagnostic and both factor-999 probes; none changes from
  refused to accepted. 32 accepted probes on these two records still export
  non-strict JSON (`Fraction`, `float32` or `int64` substitutions of an
  equal or single-precision-equal value; limits above).
- The full suites are recorded in
  [`phase1g_h_delta_audit_3_remediation.md`](phase1g_h_delta_audit_3_remediation.md) §3.

## 5. Status

No status token, observational authorisation or frozen record changes; the
five authorisations stay `NOT_GRANTED`. The change is part of the 1G-H
session branch, in its own commit, and follows that branch's publication
decisions.
