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

Every transmission solution satisfies, to configured tolerance:

    [u]_Gamma = 0
    [A D_n u]_Gamma = 0

No surface-source input exists. The analytic solve derivative is the
authorized Phase 1E-F operator identity:

    u_dot = G_Gamma (s_dot - A_Gamma_dot u)

The second derivative follows by differentiating this identity. Finite
differences are used only as an independent test.

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

F_v is algebraically slaved. C_P is verified independently and is never
absorbed into C_eff.

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

If the effective denominator fails, H1EffectiveNormalizationError exposes
only the already-computed unnormalized F_v, mathscr_Q, mathscr_W, C_P, and
background Q_bar+W_bar diagnostics. Delta_eff and w_eff are not evaluated.

## 9. Provenance and inverse boundary

The result retains wall/void injection responses, transmitted fields, raw and
admissible dual sources, and analytic derivative jets. Applying the coupled
operator reconstructs each admissible regional dual source through second
common-time order. This is the only inverse/roundtrip claim.

There is no target-only inverse from (Delta_d,Z,Delta_eff) to the regional
bulk state.

## 10. Validation status and limitations

All 37 new scientific cases pass the direct Python 3.14.3 execution harness.
The same 37 cases pass through normal pytest under Python 3.14.3 and Python
3.11.9. The complete repository suite passes 416 tests in each environment,
with no failures, skips, xfails, or warnings reported.

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
