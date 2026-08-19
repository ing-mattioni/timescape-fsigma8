# Phase 1E-F - Conditional H1 Clean Transmission Realization

**Realization ID:** H1-1E-F-CLEAN-NONDEGENERATE-TRANSMISSION-V1

**Framework:** COMPATIBLE_IMPORTED_DYNAMICS

**Scientific status:** CONDITIONALLY_CLOSED

**Observable status:** NON_OBSERVATIONAL / NOT_FSIGMA8

**Scientific implementation authorization:** GRANTED

**Prototype authorization:** GRANTED_FOR_THIS_RESEARCH_RUNTIME_ONLY

**Acceptance status:** ALL_SCIENTIFIC_AND_SOFTWARE_GATES_PASSED

## 1. Scope

This phase implements the authorized operator-contract research runtime for
the clean, nondegenerate H1 transmission branch. It does not implement a
physical finite-element model, an S1 fallback, a dressed-lightcone map, RSD,
tracer dynamics, sigma8, fsigma8, or an observational likelihood.

The carrier reference is a three-torus split into fixed Lagrangian wall and
void reference domains with a mathematical transfer interface Gamma. Gamma
is not finite infinity, a Darmois/Israel junction, a thin shell, the GM
zero-measure domain, a radial-null surface, or an observed wall boundary.
There is no interface-displacement state.

## 2. Differential state

The only independent physical perturbation state is:

    Y_bulk = (Delta_w, Z_w, Delta_v, Z_v)
    rank(Y_bulk) = 4

For each region r in {w,v}, the common-time equations are:

    d Delta_r / dt_D = -alpha_r Z_r
    d Z_r / dt_D = -2 alpha_r H_r Z_r
                    -4 pi G alpha_r rho_r Delta_r

These are the dust specialization of GM Eqs. (2.22)-(2.23), with the
authorized common-time chain rule. Regional curvature is derived from the
variation of GM Eq. (2.13):

    mathscr_R_r = -(4/3) Theta_r Z_r + 16 pi G rho_r Delta_r

It is not an additional state.

## 3. Coupled H1 operator contract

The continuum contract is represented by a broken regional H1 space, its
continuous-trace subspace, and one globally mean-zero subspace. The reference
backend constructs a single null-space basis for:

- the interface value constraints;
- the conormal-flux constraints;
- exactly one global mean constraint.

It never removes independent wall and void constant modes. The reduced
operator is solved jointly and must be symmetric and coercive. The backend
requires explicit declarations of:

- C2 common-time regularity;
- fixed Lagrangian interface constraints;
- a positive interval coercivity lower bound;
- constraint-rank and symmetry tolerances.

The matrix backend computes the instantaneous minimum eigenvalue of
Q^T A_Gamma Q on the constrained space and checks the caller-declared
interval lower bound against it. This is an instantaneous spectral
verification plus an explicit interval contract; it is not a numerical proof
of uniform coercivity over an arbitrary time interval.

Every transmission solution satisfies, to configured tolerance:

    [u]_Gamma = 0
    [A D_n u]_Gamma = 0

The normal convention is explicit and mandatory. A common reference normal
n_Gamma points wall-to-void, and both stored traces use it:

    q_w = A_w grad(u_w) . n_Gamma
    q_v = A_v grad(u_v) . n_Gamma
    q_w - q_v = 0

With outward normals n_w_out=n_Gamma and n_v_out=-n_Gamma, this is equivalent
to j_w_out+j_v_out=0. Unsupported or omitted conventions fail closed.

No surface-source input exists. The analytic solve derivative is the
authorized Phase 1E-F operator identity:

    u_dot = G_Gamma (s_dot - A_Gamma_dot u)
    u_ddot = G_Gamma (s_ddot - A_Gamma_ddot u
                      - 2 A_Gamma_dot u_dot)

The second derivative is independently checked with three central
finite-difference step sizes. Finite differences remain test-only.

The matrix backend is a finite-dimensional analogue of this contract. Its
matrices and jump rows are synthetic validation objects, not a physical
spatial discretization of Timescape.

## 4. Sharp two-region coefficients

The implementation evaluates the authorized algebraic forms:

    d_Theta = Theta_v - Theta_w
    A_W = R_bar_v - R_bar_w
    A_Q = (2/3)(1-2 f_v) d_Theta^2
    B_Q = (4/3) f_v f_w d_Theta
    A_P = A_W - 3 A_Q
        = A_W - 2(1-2 f_v) d_Theta^2
    B_P = -3 B_Q
        = -4 f_v f_w d_Theta

The equivalent A_P and B_P forms are tested directly.

## 5. Provenance-preserving transfer and clean closure

Separate wall and void source injections are retained in each joint density
and curvature solve. With:

    rho_d = f_w rho_w + f_v rho_v
    m_w = f_w rho_w / rho_d
    m_v = f_v rho_v / rho_d
    d_F = (rho_v-rho_w) / rho_d

the target dust-density field is:

    Delta_d = m_w T_w^Gamma[Delta_w]
            + m_v T_v^Gamma[Delta_v]
            + d_F F_v

The old zero-partition-transfer assumption is not present. Regional
curvature enters only through its derived value:

    C_R^Gamma = f_w T_w^Gamma[mathscr_R_w]
              + f_v T_v^Gamma[mathscr_R_v]

An explicit effective-sector Frechet operator supplies
E_DeltaTheta_Gamma. There is no default operator. On the nondegenerate
branch:

    F_v = -(C_R^Gamma + B_P E_DeltaTheta_Gamma) / A_P
    mathscr_Q = A_Q F_v + B_Q E_DeltaTheta_Gamma
    mathscr_W = C_R^Gamma + A_W F_v
    C_P = mathscr_W - 3 mathscr_Q

F_v is algebraically slaved. Because A_P=A_W-3A_Q and B_P=-3B_Q,

    C_P = C_R^Gamma + A_P F_v + B_P E_DeltaTheta_Gamma = 0

is a CONSTRUCTED_IDENTITY_CHECK. It remains mandatory as a wiring diagnostic
and is never absorbed into C_eff, but it is not independent dynamic evidence.

## 6. Effective fluid, analytic Z, and partition closure

The effective background follows GM Eqs. (3.12)-(3.13):

    rho_eff = -(Q_bar+W_bar)/(16 pi G)
    p_eff = -Q_bar/(16 pi G) + W_bar/(48 pi G)
    w_eff = p_eff/rho_eff

The normalized transfer and clean pressure diagnostic are:

    Delta_eff = (mathscr_Q+mathscr_W)/(Q_bar+W_bar)
    P_tilde_eff = -C_P/[3(Q_bar+W_bar)]

Target expansion is defined only by the analytic operator derivative:

    Z = -d Delta_d/dt_D

The backend requires E_DeltaXi_0_Gamma and an explicit J_f_Gamma. A
time-independent partition is accepted only with explicitly zero J_f_Gamma.
The clock mismatch is algebraic:

    J_Xi = [F_v_dot - A_f F_v
            - f_v f_w E_DeltaXi_0_Gamma - J_f_Gamma] / (f_v f_w)

No external J_Xi history is accepted.

## 7. Residual and constraint gates

The canonical GM residuals retain the effective-pressure term:

    R_Delta = Delta_d_dot + Z
    R_Z = Z_dot + (2/3)Theta Z
        + 4 pi G(rho_d Delta_d + rho_eff Delta_eff)
        + 12 pi G rho_eff P_tilde_eff
    R_eff = Delta_eff_dot - w_eff Theta Delta_eff
          + (1+w_eff)Z + Theta P_tilde_eff

The target curvature and Hamiltonian check are derived quantities:

    R_GM = -(4/3)Theta Z
         + 16 pi G(rho_d Delta_d + rho_eff Delta_eff)
    K_GM = R_GM + (4/3)Theta Z
         - 16 pi G(rho_d Delta_d + rho_eff Delta_eff)

The residual classifications are:

    CONSTRUCTED_IDENTITY_CHECK:
        C_P
        R_Delta, because Z = -Delta_d_dot
        K_GM, because R_GM is defined by the displayed relation

    DYNAMIC_COMPATIBILITY_CHECK:
        R_Z
        R_eff

The constructed checks detect implementation or wiring faults but are not
independent dynamic evidence. R_Z and R_eff are validated with a nontrivial
manufactured trajectory and independent term-by-term reconstruction. Separate
second-density-jet and effective-first-jet corruptions produce predictable
fail-closed residuals.

The clean mismatch system contains exactly C_Delta, C_Z, and C_eff. C_P is
separate. Zero mismatch has zero propagation RHS when all clean gates hold.

## 8. Fail-closed validity domain

Evaluation is rejected before division unless all conditions hold:

    0 < f_v < 1
    f_v f_w >= partition_product_min > 0
    |A_P| >= A_P_min > 0
    |Q_bar+W_bar| >= effective_denominator_min > 0
    |rho_d| >= rho_d_min > 0
    c_Gamma >= coercivity_min > 0
    alpha_w > 0 and alpha_v > 0
    Theta_r = 3 H_r through second declared derivative order

Every scientific tolerance is supplied explicitly by H1Configuration. No
scientifically meaningful default threshold exists.

At exact regional equality, d_Theta=A_W=A_Q=B_Q=A_P=B_P=0. The point is
outside the nondegenerate A_P branch and is classified:

    FAIL_CLOSED_DEGENERATE_ONTOLOGY_REDUCTION

The tested near-equal path has a numerator identically equal to zero and only
establishes F_v=0/epsilon=0 along that special path. A finite general limit
would require C_R^Gamma+B_P E_DeltaTheta_Gamma=O(A_P); even then the ratio is
path-dependent without additional structure. No equal-region branch is added.

If the effective denominator fails, H1EffectiveNormalizationError exposes
only the already-computed unnormalized F_v, mathscr_Q, mathscr_W, C_P, and
background Q_bar+W_bar diagnostics. Delta_eff and w_eff are not evaluated.

## 9. Provenance and inverse boundary

The result retains wall/void injection responses, transmitted fields, raw and
admissible dual sources, and analytic derivative jets. The precise roundtrip
is:

    raw source b
        -> admissible projected source P b
        -> constrained H1 solution
        -> coupled operator
        -> recovered admissible source P b

This is a solver/operator/provenance consistency identity through second
common-time order, not independent evidence of physical invertibility.

There is no target-only inverse from (Delta_d,Z,Delta_eff) to the regional
bulk state.

## 10. Validation status and limitations

The historical v1 direct harness covered 37 cases. The strengthened v2 suite
contains 42 normal-pytest cases under both Python 3.14.3 and Python 3.11.9.
The complete repository suite passes 421 tests in each environment,
with no failures, skips, xfails, or warnings reported.

The manufactured clean cancellation uses nonzero Delta_d, Z, Z_dot, Theta,
Delta_eff, Delta_eff_dot, rho_d, and rho_eff, with w_eff=0.5. Its scalar
R_Z contributions are -1.352, 0.3136, 1.0, and 0.0384; its R_eff
contributions are -0.831936, -0.008064, and 0.84. Adversarial perturbations
produce R_Z magnitude 0.10000000000000028 and R_eff magnitude
0.058333333333333334 against 1e-10 tolerances.

The two corrupted external validation environments were recreated without
changing repository dependencies or any Phase 1E-F bytes. The established
NumPy, SciPy, Matplotlib, pytest, and pluggy versions were restored before
the suites ran.

The runtime remains an operator-contract research implementation. It does not
select a physical mesh, interface geometry, continuum coefficient field, or
observational interpretation.

The existing D3 adjudication remains RESOLVED_DERIVED_4_10, while the
derived_4_10 and printed_4_15 runtime labels remain distinct with no default.
The runtime accepts no generic wavenumber and makes no identification among
regional dust Z, wall velocity, tracer velocity, peculiar-velocity
divergence, or observational RSD divergence.

    H1_CLEAN_NONDEGENERATE_TRANSMISSION_REALIZATION_IMPLEMENTED_CONDITIONALLY
    SCIENTIFIC_IMPLEMENTATION_AUTHORIZATION: SATISFIED
    OBSERVATIONAL_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
