# Phase 1E-F H1 Realization Validation

## Verdict

ALL_STRENGTHENED_SCIENTIFIC_AND_SOFTWARE_GATES_PASSED

The conditional H1 operator-contract runtime satisfies the v2 scientific
validation correction without changing its selected equations or state rank.

    H1_CLEAN_NONDEGENERATE_TRANSMISSION_REALIZATION_IMPLEMENTED_CONDITIONALLY
    SCIENTIFIC_IMPLEMENTATION_AUTHORIZATION: SATISFIED
    OBSERVATIONAL_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED

## Residual classification

The following are mandatory implementation and wiring diagnostics:

    CONSTRUCTED_IDENTITY_CHECK:
        C_P
        R_Delta
        K_GM

They are not independent dynamic evidence.

For C_P, A_P=A_W-3A_Q and B_P=-3B_Q give:

    C_P = W-3Q
        = C_R + A_P F_v + B_P E
        = 0

after substituting F_v=-(C_R+B_P E)/A_P. R_Delta vanishes because
Z=-Delta_d_dot. K_GM reconstructs the equation used to define R_GM.

The independently exercised dynamic residuals are:

    DYNAMIC_COMPATIBILITY_CHECK:
        R_Z
        R_eff

## Nontrivial manufactured compatibility fixture

The manufactured trajectory passes through evaluate_h1_realization and has:

- Delta_d = 1;
- Z = 0.56;
- Z_dot = -1.352;
- Theta = 0.84;
- Delta_eff = 0.0192;
- Delta_eff_dot = -0.831936;
- rho_d = 1;
- rho_eff = 2;
- w_eff = 0.5.

All values multiply a nonzero admissible carrier field. C_P remains zero by
the clean constitutive identity.

The independently reconstructed scalar R_Z contributions are:

    -1.352 + 0.3136 + 1.0 + 0.0384 = 0

All four clean terms are individually nonzero. The independently reconstructed
R_eff contributions are:

    -0.831936 - 0.008064 + 0.84 = 0

All three terms are individually nonzero. The runtime residual arrays agree
with these independent term-by-term reconstructions.

Adversarial cases retain 1e-10 configured tolerances:

- A second-operator-jet shift of +0.12 changes Z_dot predictably and produces
  R_Z magnitude 0.10000000000000028; the runtime fails closed on R_Z.
- An effective first-jet shift of -0.07 produces R_eff magnitude
  0.058333333333333334; the runtime fails closed on R_eff.

No tolerance was relaxed.

## Analytic second derivative

The unchanged runtime formula is:

    u_dot = A^-1 (b_dot - A_dot u)
    u_ddot = A^-1 (b_ddot - A_ddot u - 2 A_dot u_dot)

A test-only manufactured quadratic A(t) and b(t) compares u.second with
central finite differences from independent value solves. Maximum errors are:

| Step h | Maximum error |
| ---: | ---: |
| 0.02 | 6.047445224088843e-06 |
| 0.01 | 1.511909388296484e-06 |
| 0.005 | 3.7797144475382183e-07 |

The approximately fourfold reduction per halving is the expected second-order
central-difference convergence. Finite differencing is not used by runtime
science.

## Equal-region branch

Exact equality gives:

    d_Theta=A_W=A_Q=B_Q=A_P=B_P=0

and is outside |A_P|>=A_P_min. Its classification is:

    FAIL_CLOSED_DEGENERATE_ONTOLOGY_REDUCTION

The existing epsilon sequence is explicitly only the special
zero-numerator path F_v=0/epsilon=0. A finite general limit requires
C_R^Gamma+B_P E_DeltaTheta_Gamma=O(A_P), and the limiting ratio remains
path-dependent without additional structure.

## Flux orientation

The backend requires:

    flux_normal_convention =
        COMMON_REFERENCE_NORMAL_WALL_TO_VOID

The common reference normal n_Gamma points wall-to-void:

    q_w=A_w grad(u_w).n_Gamma
    q_v=A_v grad(u_v).n_Gamma
    q_w-q_v=0

Since n_w_out=n_Gamma and n_v_out=-n_Gamma, this is exactly
j_w_out+j_v_out=0.

The independent one-dimensional fixture uses nonconstant state
(-1,0,0,1). It obtains q_w=q_v=1 and outward fluxes +1 and -1. The correct
diagnostic is zero; reversing the required sign gives 2. Unsupported normal
conventions fail closed.

## Coercivity qualification

The instantaneous constrained spectral value is computed from:

    A_r=Q^T A Q
    lambda_min=eigmin((A_r+A_r^T)/2)

The exposed interval lower bound is caller-declared, positive, and checked not
to exceed the instantaneous constrained value. Matrix tests do not prove
uniform coercivity over an arbitrary continuum interval; that remains an
explicit validity contract.

## Provenance qualification

The validated roundtrip is:

    raw b -> P b -> constrained solve -> coupled operator -> P b

It is a solver/operator/provenance consistency identity, including the joint
interface and one global normalization. It is neither arbitrary raw-source
recovery nor a target-only or physical inverse.

## Environment and static checks

The established repaired environments remain:

- Python 3.14.3: NumPy 2.5.1, SciPy 1.18.0, pytest 9.1.1.
- Python 3.11.9: NumPy 2.4.6, SciPy 1.17.1, pytest 9.1.1.

No dependency declaration or third-party dependency changed. Python AST,
inventory JSON, Git whitespace, D3, spectral, frame, S1, and observational
firewall checks pass.

## Test results

Canonical targeted invocation:

    python -m pytest -q -p no:cacheprovider
        tests/test_phase1e_f_h1_transfer.py --basetemp <external-temp>

- Python 3.14.3: 42 passed in 0.21s.
- Python 3.11.9: 42 passed in 0.21s.

Canonical full invocation:

    python -m pytest -q -p no:cacheprovider --basetemp <external-temp>

- Python 3.14.3: 421 passed in 12.58s.
- Python 3.11.9: 421 passed in 12.98s.
- Failures, skips, xfails, and warnings: none reported.

The increase from the v1 total of 416 is exactly the five new validation
cases. The prior 379-test pre-Phase-1E-F baseline remains intact.

## Scope boundary

The backend remains a finite-dimensional analogue of the continuum operator
contract, not a physical Timescape discretization. It remains
non-observational and not f sigma 8.
