"""Current cross-phase scientific classifications after Astra A07 (1F-C-R).

These record missing derivations and, where a human-approved successor
record says so, refutations; they neither change equations nor assert
nonexistence of every possible embedding. Historical phase reports remain
checkpoint evidence and are superseded for current interpretation by 1F-C-R
and its successor records (reports/phase1g_a_barotropic_status_successor.md
changes one token; reports/phase1g_status_additions_successor.md adds six;
reports/phase1g_e_status_addition_successor.md adds one).  The owner
decisions of 2026-09-30 (reports/phase1g_c_owner_decisions_successor.md,
reports/phase1g_d_owner_decisions_successor.md) edit three comments and no
value.
"""

from types import MappingProxyType

REGIONAL_DUST_FLRW_EQUATIONS = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING = "NOT_DERIVED"
NAIVE_W09_WALL_CLOCK_AS_REGIONAL_PROPER_DUST_FLRW_CLOCK = "REJECTED_UNSUPPORTED"
ZEROTH_ORDER_DUST_WALL_BACKGROUND_COINCIDENCE = "REQUIRED_FOR_FIRST_ORDER_BOOST"
ZEROTH_ORDER_DUST_WALL_BACKGROUND_COINCIDENCE_STATUS = "NOT_DERIVED"
ALL_TIME_TRANSFER_CONSTITUTIVE_COMPATIBILITY = "NOT_DERIVED"
MANUFACTURED_H1_TRAJECTORIES = "ALGEBRAIC_VALIDATION_ONLY"
PHYSICAL_TIMESCAPE_TRAJECTORY_EXISTENCE = "NOT_DERIVED"
DIFFERENTIAL_RANK_MEANING = "FIELD_SPECIES_COUNTS_NOT_FREE_ADMISSIBLE_INITIAL_FUNCTIONS"
CONDITIONAL_FORWARD_UNIQUENESS_SCOPE = "GIVEN_COMPLETE_ADMISSIBLE_CLOSURE_DATA_NOT_EXISTENCE"
D3_VERDICT = "RESOLVED_DERIVED_4_10"
UNIQUE_TIMESCAPE_PREDICTION = "NOT_GRANTED"
OBSERVATIONAL_AUTHORIZATION = "NOT_GRANTED"
RSD_AUTHORIZATION = "NOT_GRANTED"
SIGMA8_AUTHORIZATION = "NOT_GRANTED"
FSIGMA8_AUTHORIZATION = "NOT_GRANTED"
# Phase 1G-A Sec. 4.1 (reports/phase1g_a_sigma8_derivation_path_audit.md):
# with the corrected c_s,eff^2 < 0 the principal part of [GM] Eq. (4.19) is
# elliptic in space-time, so the unrestricted barotropic Cauchy problem is
# Hadamard ill-posed (growth ~ exp(k*alpha), alpha = 1.70695) and no linear
# barotropic sigma_R exists.  Changed from NOT_DERIVED with the project
# owner's approval dated 2026-09-29; successor record
# reports/phase1g_a_barotropic_status_successor.md.  The finite-mode
# barotropic runtime and both D3 branches are unchanged.
UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY = "REFUTED_HADAMARD_ILL_POSED"

# The six tokens below are additions, not changes: the frozen 1F-C-R snapshot
# has no entry for them.  Each was proposed by the cited report and added with
# the project owner's approval dated 2026-09-29; successor record
# reports/phase1g_status_additions_successor.md.  None grants anything:
# SIGMA8_AUTHORIZATION and the other NOT_GRANTED tokens above are unchanged.
#
# Phase 1G-C Sec. 5 (reports/phase1g_c_two_scale_growth_law.md): under
# assumptions A1-A5, linear sub-cell perturbations of the wall matter grow as
# the EdS growing mode of the wall region in the common time t.  A5 (owner
# decision GC-OD3, 2026-09-30, reports/phase1g_c_owner_decisions_successor.md):
# the wall matter clocks the common time t.  The reading is narrowed by Phase
# 1G-D Sec. 9 (reports/phase1g_d_separate_universe_growth.md): the law gives
# the wall-internal linear statistic, relative to the wall mean, not a
# global-mean sigma at 8 h^-1 Mpc.  Owner approval 2026-09-29.
TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
# Phase 1G-C Sec. 8: the super-cell/sub-cell transition law (its shape) is not
# derivable from the self-similar tracker.  Phase 1G-D Sec. 8 derives a
# conditional transition *length scale* R* from a peak-background-split
# void-onset response, but not the transition law.  Owner approval 2026-09-29.
SUPER_CELL_TO_SUB_CELL_GROWTH_TRANSITION = "NOT_DERIVED"
# Phase 1G-D Sec. 5: the separate-universe (k -> 0) modes of the tracker are
# exact solutions of [GM] Eqs. (4.9)-(4.11) with Delta_eff/Delta_d < 0 and
# P_eff != 0.  [GM]'s comoving closure (Delta_eff/Delta_d = +0.18...+0.20,
# P_eff = 0) admits no separate-universe mode.  The Meszaros approximation
# holds for a separate-universe mode iff delta Q = 0 ([GM] Eq. (4.27) is
# (4.11) without 4 pi G rho_eff (Delta_eff + 3 P_eff) = -delta Q), and the
# barotropic closure (P_eff = c_s^2 Delta_eff) holds exactly for the global
# bang-time shift; both hold only for decaying bang-time combinations, for no
# growing separate-universe mode (characterisation corrected by owner
# decision GD-OD5, 2026-09-30, reports/phase1g_d_owner_decisions_successor.md).
# The closures' equations are unchanged.  Owner approval 2026-09-29.
GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY = "FAILED_FOR_TIMESCAPE_TRACKER"
# Phase 1G-D Sec. 6: D_SU(t) = f_w(t) D_wall(t) + A_v a_LS f_v(t) for the
# primordial long-wavelength mode, under assumption S2 (void-onset response)
# and only for R > R* (Sec. 8).  Owner approval 2026-09-29.
TWO_SCALE_SUPER_CELL_GROWTH_LAW = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"
# Phase 1G-D Sec. 7: the void-onset response A_v = d(epsilon)/d(delta_L) is an
# external closure; the two estimates ([W09] single-perturbation seeding,
# peak-background split) differ by orders of magnitude.  Owner approval
# 2026-09-29.
VOID_ONSET_RESPONSE = "EXTERNAL_CLOSURE_INPUT"
# Phase 1G-D Sec. 9: at 8 h^-1 Mpc the wall/void partition is
# non-perturbative (the peak-background-split void response A_v sigma_LSS(R8)
# is 1.05-1.11 with the tracker-consistent void seed and 3.8-4.6 with the
# [SvdW04] seed factor, i.e. |eps| >~ 1; each at its own equal-mass R8 with
# f_vi = f_v(t_LS); owner decisions GD-OD1, OD2, OD7 of 2026-09-30,
# reports/phase1g_d_owner_decisions_successor.md, which supersede the frozen
# 2.6-4.3), so a linear, global-mean sigma at that scale is not defined in the
# linear two-scale theory; the only linear statistic there is the
# wall-internal sigma_wall.  This is a statement about the linear theory, not
# an authorisation: SIGMA8_AUTHORIZATION stays NOT_GRANTED.  Owner approval
# 2026-09-29.
LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC = "NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY"
# Phase 1G-E Sec. 2 (reports/phase1g_e_two_phase_sigma.md), proposed in its
# Sec. 6 item 3: the two-phase mass variance in 8 h^-1 Mpc balls,
# sigma^2 = delta_v^2 sigma_part^2 + sigma_int^2, is derived only under
# assumptions E1-E4 (empty voids; Boolean Poisson balls of one radius at
# volume fraction f_v0; wall field independent of the void geometry;
# isotropic Eulerian compression of the wall field).  It is a conditional,
# nonlinear, model-internal quantity, not an observational sigma_8, and it
# grants nothing: SIGMA8_AUTHORIZATION stays NOT_GRANTED.  An addition, not a
# change, with the project owner's approval dated 2026-09-29; successor record
# reports/phase1g_e_status_addition_successor.md.
TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC = "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"

REMAINING_SCIENTIFIC_CLOSURES = (
    "REGIONAL_COMMON_BACKGROUND_AND_SOURCE_EMBEDDING",
    "ALL_TIME_TRANSFER_CONSTITUTIVE_COMPATIBILITY",
    "H1_TO_WALL_DRESSED_SPATIAL_REALIZATION_AND_DENSITY_CODOMAIN_MAP",
    "PERTURBATIVE_WALL_LAPSE_NU_W",
    "LOCAL_SCALE_HUBBLE_MAPPING_AND_PERTURBED_GEOMETRIC_DYNAMICS",
    "INITIAL_BOUNDARY_KERNEL_AND_MORPHOLOGY_DATA",
    "FUTURE_LIGHTCONE_TRACER_STATISTICAL_AND_SURVEY_INPUTS",
)

CURRENT_SCIENTIFIC_STATUS = MappingProxyType({
    name: value for name, value in tuple(globals().items())
    if name.isupper() and isinstance(value, (str, tuple))
})
