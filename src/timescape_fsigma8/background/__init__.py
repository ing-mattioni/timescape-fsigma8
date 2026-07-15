"""Timescape tracker-solution background quantities.

Independent implementation from the published equations. Scientific
specification (in order of precedence):

  [GM]  M. Galoppo & P. Mourier, "Cosmological perturbations on an averaged
        background", JCAP 02 (2026) 066, arXiv:2511.17160v2.
        Background scheme: Eqs. (3.6)-(3.18); timescape tracker: Sec. 5.1.1,
        Eqs. (5.3)-(5.7) and surrounding text.
  [W09] D. L. Wiltshire, "Average observational quantities in the timescape
        cosmology", PRD 80, 123512 (2009), arXiv:0909.0749.
        Tracker solution: Appendix B, Eqs. (B1)-(B12); Eqs. (15)-(20),
        (28), (38).

Module layout (all public names are re-exported here, so
`import timescape_fsigma8.background as bg` exposes the same API as the
original single-module implementation — pinned by
tests/test_refactor_equivalence.py):

  parameters       TrackerParams (the two tracker free parameters) and
                   shared input validation
  tracker          f_v, a_D, H_D, Theta, <R>_D, Q_D, <rho_d>_D, their
                   time derivatives, and the bare density parameters
  effective_fluid  rho_eff, p_eff, their derivatives, w_eff, c^2_{s,eff}
                   ([GM] (3.12)-(3.13))
  observables      wall/dressed quantities: gamma_w, a_w, tau_w,
                   H_dressed, redshift and derivatives

Every function cites its equation number(s) (AGENTS.md rule 2). Closed
forms marked "derived" are our own algebra from the cited equations; each
is validated in tests/ against numerical differentiation, the Buchert
identities (3.8)-(3.11), (3.17), and the upstream oracle.

DOCUMENTED DEVIATIONS FROM PRINTED SOURCES (flagged for human review; see
reports/background_equation_audit.md for the full evidence):

  (D1) [GM] Eq. (5.7) prints <R>_D(t) = -6 f_{v,0}^{-2/3} f_v(t)/t^2. The
       f_{v,0}^{-2/3} prefactor is inconsistent with the Hamiltonian
       constraint (3.8) applied to (5.5)-(5.6), with [W09] (B4)+(B6), and
       with the upstream notebook. We implement <R>_D = -6 f_v(t)/t^2
       (no prefactor) and treat the printed prefactor as a typo.

  (D2) The upstream notebook's d(Q_D)/dt (cell 6, `dQDdt`) multiplies by
       3 f_v (1-f_v) where the quotient rule requires dividing by it. We
       implement the correct derivative. Consequently our c^2_{s,eff}
       (:= dp_eff/dt / drho_eff/dt, [GM] Sec. 4 text) intentionally
       DISAGREES with the upstream notebook and with the published Fig. 1
       (right panel): upstream c^2_{s,eff}(t0) ~ -0.3452, correct value
       -(2 + 2 f_v0 - f_v0^2)/(2 + f_v0)^2 ~ -0.3912.

Conventions: c = 1; Lambda = 0; K_D = 0 ([GM] Sec. 5 preamble), so the
curvature deviation W_D := <R>_D - 6 K_D / a_D^2 equals <R>_D. Time t is
the Buchert volume-average (cosmic) time in any unit consistent with
1/HD0; all outputs carry the corresponding powers of that unit. G enters
only densities and is passed explicitly (AGENTS.md rule 4: no hidden
unit choices). The tracker domain is t > 0, enforced by input validation
(ValueError on t <= 0; only tau_w admits t = 0, where tau_w(0) = 0). For
physically parametrised inputs see timescape_fsigma8.presets (Gyr units)
and timescape_fsigma8.units (audited conversions).
"""

from timescape_fsigma8.background.effective_fluid import (
    cs2_eff,
    dp_eff_dt,
    drho_eff_dt,
    p_eff,
    rho_eff,
    w_eff,
)
from timescape_fsigma8.background.observables import (
    H_dressed,
    a_w,
    dgamma_w_dt,
    dtau_w_dt,
    gamma_w,
    redshift,
    tau_w,
)
from timescape_fsigma8.background.parameters import TrackerParams
from timescape_fsigma8.background.tracker import (
    H_D,
    Omega_Q,
    Omega_R,
    Omega_m,
    Q_D,
    R_D,
    Theta,
    a_D,
    d2fv_dt2,
    dQ_D_dt,
    dR_D_dt,
    da_D_dt,
    dfv_dt,
    drho_d_dt,
    fv,
    rho_d,
)

__all__ = [
    "TrackerParams",
    # tracker
    "fv", "dfv_dt", "d2fv_dt2",
    "a_D", "da_D_dt", "H_D", "Theta",
    "R_D", "Q_D", "dR_D_dt", "dQ_D_dt",
    "rho_d", "drho_d_dt",
    "Omega_m", "Omega_R", "Omega_Q",
    # effective fluid
    "rho_eff", "p_eff", "drho_eff_dt", "dp_eff_dt", "w_eff", "cs2_eff",
    # observables (wall/dressed)
    "gamma_w", "dgamma_w_dt", "a_w", "dtau_w_dt", "tau_w",
    "H_dressed", "redshift",
]
