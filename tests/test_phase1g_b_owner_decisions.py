"""Regression for the Phase 1G-B owner decisions GB-OD2 to GB-OD6 (2026-09-30).

Successor record: reports/phase1g_b_owner_decisions_successor.md and its
inventory.  Findings: reports/phase1g_b_adversarial_audit.md (GB-F4 to GB-F7,
GB-F9).  Every decision is output-preserving: no computed value of
``lagrangian_sigma`` changes.

Tolerances (AGENTS.md rule 9):
- the independent growth integration uses DOP853 with rtol 1e-12, atol 1e-14
  (the package's growing-mode controls are rtol 1e-12);
- package vs independent ln g: the package's documented early-start bias,
  observed 1.1e-6 to 2.1e-6 (budget 3e-6 absolute); after subtracting the
  package's own ``log_growth_early_limit_linear_bias_estimate``: observed
  <= 2e-10 (budget 1e-9 absolute);
- the independent g against the 1G-B audit's printed eight-decimal values:
  half a unit of the last digit (5e-9 absolute).
Every other comparison is exact.
"""

from __future__ import annotations

import dataclasses
import json
import math
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import solve_ivp

import timescape_fsigma8.lagrangian_sigma as ls
from timescape_fsigma8.perturbations.growing_mode import CleanPerturbationSystem
from timescape_fsigma8.perturbations.initial_conditions import PLANCK_2018_QPLUS_RECIPE
from timescape_fsigma8.presets import PAPER_REFERENCE
from timescape_fsigma8.scientific_status import CURRENT_SCIENTIFIC_STATUS

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

NA = ls.NOT_APPLICABLE
CGI = ls.GrowthLaw.VOLUME_AVERAGE_CGI
WALL = ls.GrowthLaw.WALL_REGIONAL_EDS_COMMON_TIME
COMOVING = CleanPerturbationSystem.COMOVING
MESZAROS = CleanPerturbationSystem.MESZAROS
LAWS = {"comoving": (CGI, COMOVING, ls.VOLUME_AVERAGE_GROWTH_REFERENCE_NUMERICS),
        "meszaros": (CGI, MESZAROS, ls.VOLUME_AVERAGE_GROWTH_REFERENCE_NUMERICS),
        "wall": (WALL, NA, ls.WALL_REGIONAL_GROWTH_REFERENCE_CHECKS)}
BACKGROUND = ls.TimescapeTrackerInput.from_reference_preset(preset=PAPER_REFERENCE)
OMEGA_M_LCDM = PLANCK_2018_QPLUS_RECIPE.omega_m * PLANCK_2018_QPLUS_RECIPE.h ** 2
SPEC = ls.EarlySpectrumImport(
    A_s=2.100e-9, n_s=0.9649, k_pivot_per_Mpc=0.05, baryon_fraction=0.02237 / OMEGA_M_LCDM,
    T_cmb_K=2.7255, transfer_model=ls.EarlyTransferModel.EH98_ZERO_BARYON_OSCILLATION,
    provenance="Planck 2018 VI Table 2 (test fixture)", import_status=ls.EARLY_SPECTRUM_IMPORT_STATUS)
FORBIDDEN_TOKENS = ("sigma_8", "sigma8", "8hmpc")
FROZEN_1F_C_R_INVENTORY = PROJECT_ROOT / "reports" / "phase1f_c_r_astra_audit_remediation_inventory.json"
RECORD_JSON = PROJECT_ROOT / "reports" / "phase1g_b_owner_decisions_successor_inventory.json"

INDEPENDENT_RTOL, INDEPENDENT_ATOL = 1e-12, 1e-14
EARLY_START_BIAS_ABS = 3e-6
BIAS_CORRECTED_ABS = 1e-9
AUDIT_PRINTED_ABS = 5e-9
# Independent t_e -> 0 values of the 1G-B adversarial audit, Sec. 4.5 ([GM] preset).
AUDIT_G_TS = {"comoving": 0.40266226, "meszaros": 0.34169348}


def explicit_radius(value: float) -> ls.LagrangianRadiusSpec:
    return ls.LagrangianRadiusSpec(
        convention=ls.LagrangianRadiusConvention.EXPLICIT_PHOTON_NORMALISED_RADIUS,
        length_h_inverse_Mpc=NA, reference_omega_m=NA, reference_radius_Mpc=NA,
        explicit_radius_Mpc=value)


@lru_cache(maxsize=None)
def growth(law: str) -> ls.TimescapeGrowthFactor:
    growth_law, closure, numerics = LAWS[law]
    return ls.timescape_growth_factor(params=BACKGROUND.dimensionless_params(),
                                      growth_law=growth_law, closure=closure,
                                      numerics=numerics, G=1.0)


@lru_cache(maxsize=None)
def result(law: str, radius: float = 10.0) -> ls.ConditionalLagrangianSigma:
    growth_law, closure, numerics = LAWS[law]
    return ls.conditional_lagrangian_linear_sigma(
        background=BACKGROUND, growth_law=growth_law, closure=closure, growth_numerics=numerics,
        early_spectrum=SPEC, radius=explicit_radius(radius),
        quadrature=ls.LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE, density_identity_tolerance=1e-13,
        G=1.0)


# ------------------------------------------------------------ GB-OD2 naming
def test_gb_od2_only_the_negative_status_constants_carry_the_tokens():
    flagged = {name for name in ls.__all__
               if any(token in name.lower() for token in FORBIDDEN_TOKENS)}
    assert flagged == {"SIGMA8_STATUS", "FSIGMA8_STATUS"}
    for name in flagged:
        value = getattr(ls, name)
        assert isinstance(value, str) and value.startswith("NOT_")
    # The new growth-record output (GB-OD5) keeps keys clean; its strings carry
    # no token either.
    for law in LAWS:
        record = growth(law).to_json_dict()
        assert not any(t in key.lower() for key in record for t in FORBIDDEN_TOKENS)
        assert not any(t in record["model_caveat"].lower() for t in FORBIDDEN_TOKENS)


def test_gb_od2_claude_md_states_the_enforced_rule():
    text = " ".join((PROJECT_ROOT / "CLAUDE.md").read_text(encoding="utf-8").split())
    assert ("No public function, class, member or output-key name may contain "
            "`sigma8`, `sigma_8` or `8hMpc`") in text
    assert "`SIGMA8_STATUS` and `FSIGMA8_STATUS`" in text
    assert "No public name may contain" not in text


# ------------------------------------------------------------ GB-OD3 validator
@pytest.fixture()
def remediation(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(PROJECT_ROOT)
    import validate_phase1f_c_r_astra_remediation as module
    return module


@pytest.fixture()
def frozen() -> dict:
    return json.loads(FROZEN_1F_C_R_INVENTORY.read_text(encoding="utf-8"))["current_scientific_status"]


def _records(remediation):
    return remediation.successor_status_changes(), remediation.successor_status_additions()


@pytest.mark.parametrize("token", ["D3_VERDICT", "SIGMA8_AUTHORIZATION", "REMAINING_SCIENTIFIC_CLOSURES"])
def test_gb_od3_a_deleted_frozen_token_is_rejected(remediation, frozen, token):
    changes, additions = _records(remediation)
    live = {key: value for key, value in CURRENT_SCIENTIFIC_STATUS.items() if key != token}
    with pytest.raises(AssertionError, match=f"{token}: frozen token missing from the live module"):
        remediation.check_current_scientific_status(frozen, live, changes, additions=additions)
    with pytest.raises(AssertionError, match=f"{token}: frozen token missing from the live module"):
        remediation.check_current_scientific_status(frozen, live, changes, additions=additions,
                                                    removals={})


def test_gb_od3_a_registered_removal_is_the_only_way_out(remediation, frozen):
    changes, additions = _records(remediation)
    token = "D3_VERDICT"
    live = {key: value for key, value in CURRENT_SCIENTIFIC_STATUS.items() if key != token}
    removal = {token: {"old_token": frozen[token], "record": "test"}}
    remediation.check_current_scientific_status(frozen, live, changes, additions=additions,
                                                removals=removal)
    with pytest.raises(AssertionError, match=f"{token}: removed token is still in the live module"):
        remediation.check_current_scientific_status(
            frozen, CURRENT_SCIENTIFIC_STATUS, changes, additions=additions, removals=removal)
    with pytest.raises(AssertionError, match=f"{token}: frozen snapshot does not hold the removed"):
        remediation.check_current_scientific_status(
            frozen, live, changes, additions=additions,
            removals={token: {"old_token": "OTHER", "record": "test"}})
    with pytest.raises(AssertionError, match="NOT_A_TOKEN: successor record removes a token absent"):
        remediation.check_current_scientific_status(
            frozen, live, changes, additions=additions,
            removals={**removal, "NOT_A_TOKEN": {"old_token": "X", "record": "test"}})
    # No registered record removes anything.
    assert remediation.successor_status_removals() == {}


def test_gb_od3_a_change_naming_an_absent_token_fails_by_name(remediation, frozen):
    changes, additions = _records(remediation)
    changes = {**changes, "NOT_A_TOKEN": {"old_token": "A", "new_token": "B", "record": "test"}}
    live = {**CURRENT_SCIENTIFIC_STATUS, "NOT_A_TOKEN": "B"}
    with pytest.raises(AssertionError,
                       match="NOT_A_TOKEN: successor record changes a token absent from the frozen"):
        remediation.check_current_scientific_status(frozen, live, changes, additions=additions)


def test_gb_od3_the_frozen_inventory_is_pinned_to_its_certified_blob(remediation):
    current = FROZEN_1F_C_R_INVENTORY.read_bytes()
    remediation.check_frozen_inventory_pinned(current)
    record = json.loads(current)
    record["current_scientific_status"]["D3_VERDICT"] = "EDITED"
    tampered = remediation.canonical(record)      # still canonical JSON, different content
    with pytest.raises(AssertionError, match="frozen inventory differs from its blob"):
        remediation.check_frozen_inventory_pinned(tampered)


def test_gb_od3_successor_records_must_be_canonical(remediation, tmp_path):
    remediation.check_successor_records_canonical(remediation.STATUS_SUCCESSOR_RECORDS)
    source = PROJECT_ROOT / remediation.STATUS_SUCCESSOR_RECORDS[0]
    loose = tmp_path / "loose.json"
    loose.write_text(json.dumps(json.loads(source.read_text(encoding="utf-8"))), encoding="utf-8")
    with pytest.raises(AssertionError, match="successor record is not canonical"):
        remediation.check_successor_records_canonical((loose,))


# ------------------------------------------------------------ GB-OD4 contracts
REFUSED_ARRAYS = ["1.0", b"1.0", [True, False], np.array([1.0 + 0.0j]), [Fraction(1, 2)],
                  np.array(["1.0"]), np.array([0.1], dtype=object)]


@pytest.mark.parametrize("value", REFUSED_ARRAYS, ids=repr)
def test_gb_od4_array_inputs_must_be_real_numeric(value):
    with pytest.raises(ls.LagrangianSigmaContractError, match="real numeric array"):
        ls.top_hat_window(x=value)
    with pytest.raises(ls.LagrangianSigmaContractError, match="real numeric array"):
        ls.eh98_zero_baryon_transfer(k_per_Mpc=value, omega_m=0.14, baryon_fraction=0.15,
                                     T_cmb_K=2.7255)
    with pytest.raises(ls.LagrangianSigmaContractError, match="real numeric array"):
        ls.matter_era_linear_amplitude(k_per_Mpc=value, early_spectrum=SPEC, omega_m=0.14,
                                       growth_today_photon_normalised=1.0)


def test_gb_od4_valid_array_inputs_are_converted_exactly():
    x = np.linspace(0.05, 5.0, 23)
    assert np.array_equal(ls.top_hat_window(x=x.tolist()), ls.top_hat_window(x=x))
    assert np.array_equal(ls.top_hat_window(x=[1, 2, 3]), ls.top_hat_window(x=[1.0, 2.0, 3.0]))
    single = x.astype(np.float32)
    assert np.array_equal(ls.top_hat_window(x=single),
                          ls.top_hat_window(x=single.astype(np.float64)))
    assert float(ls.top_hat_window(x=0)) == 1.0


def test_gb_od4_eh98_is_refused_outside_its_fit_range():
    low, high = ls.EH98_OMEGA_M_FIT_RANGE
    assert (low, high) == (0.025, 0.5)
    k = np.array([0.01, 0.1, 1.0])
    for omega_m in (low, 0.12, 0.143, high):
        ls.eh98_zero_baryon_transfer(k_per_Mpc=k, omega_m=omega_m, baryon_fraction=0.15,
                                     T_cmb_K=2.7255)
    for omega_m in (np.nextafter(low, 0.0), np.nextafter(high, 1.0), 9.83, 20.0):
        with pytest.raises(ls.LagrangianSigmaContractError, match="EH98 fit range"):
            ls.eh98_zero_baryon_transfer(k_per_Mpc=k, omega_m=float(omega_m), baryon_fraction=0.15,
                                         T_cmb_K=2.7255)
    # The exact zero-baryon limit stays available (documented, not enforced).
    ls.eh98_zero_baryon_transfer(k_per_Mpc=k, omega_m=0.143, baryon_fraction=0.0, T_cmb_K=2.7255)


def test_gb_od4_growth_record_binds_gamma_w0_to_f_v0():
    g = growth("wall")
    bumped = g.gamma_w0 * (1.0 + 1e-9)
    with pytest.raises(ls.LagrangianSigmaContractError, match=r"gamma_w0 must equal 1 \+ f_v0/2"):
        dataclasses.replace(g, gamma_w0=bumped,
                            growth_today_photon_normalised=bumped * g.growth_relative_to_volume_average_eds)


@pytest.mark.parametrize("field, factor, message", [
    ("gamma_w0", 5.0 / 1.3685, r"gamma_w0 = 1 \+ f_v0/2"),
    ("HD0_bare_km_s_Mpc", 1.001, r"H_D0 = 2 H0"),
    ("bare_Omega_M0", 1.001, r"bare Omega_M0"),
    ("omega_m_bare", 1.001, r"omega_m_bare"),
    # a change of a few ulp stays inside RECORD_IDENTITY_RTOL but breaks the stored residual
    ("closed_form", 1.0 + 1e-15, r"identity_relative_residual must equal"),
    # the audit's forging example (GB-F6): omega_m_per_photon = 0.3
    ("omega_m_per_photon", 0.3 / 0.12047512, r"identity_relative_residual must equal"),
])
def test_gb_od4_density_record_invariants(field, factor, message):
    density = result("wall").density
    with pytest.raises(ls.LagrangianSigmaContractError, match=message):
        dataclasses.replace(density, **{field: getattr(density, field) * factor})


def test_gb_od4_radius_records_are_bound_to_their_convention_and_density():
    res = result("wall")
    with pytest.raises(ls.LagrangianSigmaContractError, match="formula is inconsistent"):
        dataclasses.replace(res.radius, formula="R = L / h_dressed")
    with pytest.raises(ls.LagrangianSigmaContractError, match="must equal the explicit radius"):
        dataclasses.replace(res.radius, radius_Mpc=11.0)
    other = dataclasses.replace(res.radius, spec=explicit_radius(11.0), radius_Mpc=11.0)
    with pytest.raises(ls.LagrangianSigmaContractError, match="resolved from this record's density"):
        dataclasses.replace(res, radius=other)


# ------------------------------------------------------------ GB-OD5 caveat
@pytest.mark.parametrize("law", list(LAWS))
def test_gb_od5_growth_factor_carries_the_growth_law_limitation(law):
    g = growth(law)
    assert g.model_caveat == result(law).model_caveat
    assert g.to_json_dict()["model_caveat"] == g.model_caveat
    phrase = ("not Timescape's long-wavelength growth" if law != "wall"
              else "the wall-internal linear statistic")
    assert phrase in g.model_caveat
    with pytest.raises(ls.LagrangianSigmaContractError, match="model_caveat is inconsistent"):
        dataclasses.replace(g, model_caveat=result("wall" if law != "wall" else "comoving").model_caveat)


# ------------------------------------------------------------ GB-OD6 independent g_TS
def _independent_log_g(fv0: float, closure: str, te_over_t0: float) -> float:
    """ln g_TS from [GM] Eqs. (4.21)-(4.23) (comoving) or (4.27) (Meszaros), independently.

    Closed-form tracker in units t0 = 1 ([GM] Eqs. (5.5)-(5.7) with the
    D1-corrected <R>; Phase 1G-D Sec. 3): f_v = t/(t+tau), tau = f_w0/f_v0;
    Theta t = 2 + f_v; 4 pi G <rho> t^2 = (2/3)(1 - f_v); 4 pi G rho_eff t^2 =
    f_v (8 + f_v)/6 and w_eff = -(4 - f_v)/(8 + f_v) ([GM] Eqs. (3.12)-(3.13)).
    Normalised variables x1 = Delta_d t^(-2/3), x2 = -Z t^(1/3),
    x3 = Delta_eff t^(-2/3) in s = ln t, started on the regular mode
    (u = 2/3 - c1 f_v, c1 = 19/60 comoving, 5/12 Meszaros; Delta_eff/Delta_d = 1/5).
    g_TS = [D(t0)/D(t_e)] [a_D(t_e)/a_D0], a_D ~ t^(2/3) (t + tau)^(1/3).
    Imports nothing from the package.
    """
    tau = (1.0 - fv0) / fv0
    comoving = closure == "comoving"

    def rhs(s, x):
        t = math.exp(s)
        f = t / (t + tau)
        theta_t = 2.0 + f
        a = (2.0 / 3.0) * (1.0 - f)
        b = f * (8.0 + f) / 6.0 if comoving else 0.0
        w = -(4.0 - f) / (8.0 + f)
        x1, x2, x3 = x
        return [x2 - (2.0 / 3.0) * x1,
                a * x1 - (2.0 / 3.0) * theta_t * x2 + b * x3 + x2 / 3.0,
                (1.0 + w) * x2 + w * theta_t * x3 - (2.0 / 3.0) * x3]

    f_e = te_over_t0 / (te_over_t0 + tau)
    u = 2.0 / 3.0 - (19.0 / 60.0 if comoving else 5.0 / 12.0) * f_e
    sol = solve_ivp(rhs, (math.log(te_over_t0), 0.0), [1.0, u, 0.2 if comoving else 0.0],
                    method="DOP853", rtol=INDEPENDENT_RTOL, atol=INDEPENDENT_ATOL)
    assert sol.success, sol.message
    return math.log(sol.y[0, -1]) + math.log((te_over_t0 + tau) / (1.0 + tau)) / 3.0


@pytest.mark.parametrize("law", ["comoving", "meszaros"])
def test_gb_od6_independent_g_ts_regression(law):
    independent = _independent_log_g(PAPER_REFERENCE.fv0, law, 1e-12)
    np.testing.assert_allclose(math.exp(independent), AUDIT_G_TS[law], rtol=0.0, atol=AUDIT_PRINTED_ABS)
    g = growth(law)
    package = g.log_growth_relative_to_volume_average_eds
    np.testing.assert_allclose(package, independent, rtol=0.0, atol=EARLY_START_BIAS_ABS)
    corrected = package - g.diagnostic("log_growth_early_limit_linear_bias_estimate")
    np.testing.assert_allclose(corrected, independent, rtol=0.0, atol=BIAS_CORRECTED_ABS)


# ------------------------------------------------------------ record
def test_gb_owner_decisions_record_is_canonical_and_complete(remediation):
    record = json.loads(RECORD_JSON.read_text(encoding="utf-8"),
                        object_pairs_hook=remediation.unique_pairs)
    assert RECORD_JSON.read_bytes() == remediation.canonical(record)
    assert record["classification"] == "OWNER_DECISIONS_SUCCESSOR_RECORD"
    assert record["date"] == "2026-09-30"
    assert sorted(record["decisions"]) == ["GB-OD2", "GB-OD3", "GB-OD4", "GB-OD5", "GB-OD6"]
    assert all(entry["applied"] is True for entry in record["decisions"].values())
    assert record["scope"]["status_tokens_changed"] is False
    assert record["scope"]["numeric_outputs_changed"] is False
