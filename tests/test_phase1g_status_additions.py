"""Regression for the approved Phase 1G status-token additions and 1G-B limitation.

Successor record: reports/phase1g_status_additions_successor.md and its
inventory (human approval dated 2026-09-29).  Proposals:
reports/phase1g_c_two_scale_growth_law.md Sec. 10 item 2 ([1G-C]) and
reports/phase1g_d_separate_universe_growth.md Sec. 11 items 1-2 ([1G-D]).

The six tokens are *additions*: the frozen 1F-C-R snapshot
(reports/phase1f_c_r_astra_audit_remediation_inventory.json) has no entry for
them.  The 1F-C-R validator accepts them only through the registered
successor record and still rejects an undeclared token, an addition the
frozen snapshot already holds, a live value that differs from the record, and
a token claimed twice.  The 1G-B limitation is text only: the original caveat
texts are kept verbatim as prefixes.  Every comparison here is exact string
or key equality; no numerical tolerance is involved (AGENTS.md rule 9).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

import timescape_fsigma8.lagrangian_sigma as ls
from timescape_fsigma8 import scientific_status
from timescape_fsigma8.perturbations.growing_mode import CleanPerturbationSystem
from timescape_fsigma8.presets import PAPER_REFERENCE
from timescape_fsigma8.scientific_status import CURRENT_SCIENTIFIC_STATUS

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

RECORD_JSON = "reports/phase1g_status_additions_successor_inventory.json"
RECORD_MD = PROJECT_ROOT / "reports" / "phase1g_status_additions_successor.md"
BAROTROPIC_RECORD_JSON = "reports/phase1g_a_barotropic_status_successor_inventory.json"
FROZEN_1F_C_R_INVENTORY = PROJECT_ROOT / "reports" / "phase1f_c_r_astra_audit_remediation_inventory.json"
REPORT_1G_C = "reports/phase1g_c_two_scale_growth_law.md"
REPORT_1G_D = "reports/phase1g_d_separate_universe_growth.md"
INVENTORY_1G_C = PROJECT_ROOT / "reports" / "phase1g_c_two_scale_growth_inventory.json"
INVENTORY_1G_D = PROJECT_ROOT / "reports" / "phase1g_d_separate_universe_inventory.json"

APPROVAL_DATE = "2026-09-29"
APPROVAL_VERBATIM = (
    "let a sub-agent do the fast-forwarding and all the things that needed my "
    "approval that I give now to you for all of them"
)

# token -> (value, report that proposed it and gives the evidence, section)
ADDED = {
    "TWO_SCALE_MASS_WEIGHTED_SUB_CELL_GROWTH_LAW": (
        "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION", REPORT_1G_C, 5),
    "SUPER_CELL_TO_SUB_CELL_GROWTH_TRANSITION": ("NOT_DERIVED", REPORT_1G_C, 8),
    "GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY": (
        "FAILED_FOR_TIMESCAPE_TRACKER", REPORT_1G_D, 5),
    "TWO_SCALE_SUPER_CELL_GROWTH_LAW": (
        "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION", REPORT_1G_D, 6),
    "VOID_ONSET_RESPONSE": ("EXTERNAL_CLOSURE_INPUT", REPORT_1G_D, 7),
    "LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC": (
        "NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY", REPORT_1G_D, 9),
}
NOT_GRANTED = ("UNIQUE_TIMESCAPE_PREDICTION", "OBSERVATIONAL_AUTHORIZATION",
               "RSD_AUTHORIZATION", "SIGMA8_AUTHORIZATION", "FSIGMA8_AUTHORIZATION")
BAROTROPIC_TOKEN = "UNRESTRICTED_BAROTROPIC_CONTINUUM_STABILITY"
# Successor records registered after this one (each with its own regression):
# reports/phase1g_e_status_addition_successor.md adds one Phase 1G-E token
# (owner approval 2026-09-29, tests/test_phase1g_e_status_addition.py).  The
# checks below still pin this record's six additions exactly; they only allow
# the later registered records and their additions to exist as well.
LATER_RECORDS_JSON = ("reports/phase1g_e_status_addition_successor_inventory.json",)
LATER_ADDITIONS = {"TWO_PHASE_MASS_VARIANCE_8_H_INV_MPC": "DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture()
def remediation(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(PROJECT_ROOT)
    import validate_phase1f_c_r_astra_remediation as module
    return module


@pytest.fixture()
def frozen() -> dict:
    return load_json(FROZEN_1F_C_R_INVENTORY)["current_scientific_status"]


def test_six_added_tokens_hold_the_approved_values(frozen: dict) -> None:
    for token, (value, _report, _section) in ADDED.items():
        assert getattr(scientific_status, token) == value
        assert CURRENT_SCIENTIFIC_STATUS[token] == value
        assert token not in frozen  # an addition, not a change
    # Exactly the six tokens are new (plus the additions of the later
    # registered records); every other token is the frozen one, except the
    # separately approved Phase 1G-A change.
    assert not set(LATER_ADDITIONS) & (set(frozen) | set(ADDED))
    for token, value in LATER_ADDITIONS.items():
        assert CURRENT_SCIENTIFIC_STATUS[token] == value
    assert set(CURRENT_SCIENTIFIC_STATUS) == set(frozen) | set(ADDED) | set(LATER_ADDITIONS)
    for token, value in frozen.items():
        live = CURRENT_SCIENTIFIC_STATUS[token]
        live = list(live) if isinstance(live, tuple) else live
        if token == BAROTROPIC_TOKEN:
            assert (value, live) == ("NOT_DERIVED", "REFUTED_HADAMARD_ILL_POSED")
        else:
            assert live == value, token
    # The additions grant nothing.
    for token in NOT_GRANTED:
        assert CURRENT_SCIENTIFIC_STATUS[token] == "NOT_GRANTED"


def test_successor_record_is_canonical_and_matches_the_proposals(remediation) -> None:
    path = PROJECT_ROOT / RECORD_JSON
    record = json.loads(path.read_text(encoding="utf-8"),
                        object_pairs_hook=remediation.unique_pairs)
    assert path.read_bytes() == remediation.canonical(record)
    assert record["classification"] == "APPROVED_SCIENTIFIC_STATUS_ADDITION_SUCCESSOR_RECORD"
    assert record["report"] == "reports/phase1g_status_additions_successor.md"
    assert record["status_changes"] == {}
    assert record["human_approval"]["date"] == APPROVAL_DATE
    assert record["human_approval"]["verbatim"] == APPROVAL_VERBATIM
    assert set(record["status_additions"]) == set(ADDED)
    reports = {name: (PROJECT_ROOT / name).read_text(encoding="utf-8")
               for name in (REPORT_1G_C, REPORT_1G_D)}
    recommendations = {
        REPORT_1G_C: " ".join(load_json(INVENTORY_1G_C)["recommendations_require_human_approval"]),
        REPORT_1G_D: " ".join(load_json(INVENTORY_1G_D)["recommendations_require_human_approval"]),
    }
    record_text = RECORD_MD.read_text(encoding="utf-8")
    for token, (value, report, section) in ADDED.items():
        addition = record["status_additions"][token]
        assert addition["value"] == value
        assert addition["module"] == "src/timescape_fsigma8/scientific_status.py"
        assert addition["report"] == report
        assert addition["section"] == f"Sec. {section}"
        # The cited section exists, and the proposing report and its frozen
        # inventory proposed exactly this token and value.
        assert f"\n## {section}. " in reports[report]
        assert f'`{token} = "{value}"`' in reports[report]
        assert f"{token} = {value}" in recommendations[report]
        assert f"`{token}`" in record_text and f"`{value}`" in record_text
    scope = record["scope"]
    assert scope["existing_status_tokens_changed"] is False
    assert scope["equations_changed"] is False
    assert scope["lagrangian_sigma_numeric_outputs_changed"] is False
    assert scope["frozen_historical_reports_or_inventories_edited"] is False
    assert scope["not_granted_tokens"] == sorted(NOT_GRANTED)


def test_validator_accepts_additions_declared_by_the_registered_record(
    remediation, frozen: dict,
) -> None:
    assert remediation.STATUS_SUCCESSOR_RECORDS == (
        Path(BAROTROPIC_RECORD_JSON), Path(RECORD_JSON), *map(Path, LATER_RECORDS_JSON))
    additions = remediation.successor_status_additions()
    assert {key: value for key, value in additions.items()
            if value["record"] == RECORD_JSON} == {
        token: {"value": value, "record": RECORD_JSON}
        for token, (value, _report, _section) in ADDED.items()}
    assert set(additions) == set(ADDED) | set(LATER_ADDITIONS)
    # The new record changes no existing token: the change set is still the
    # Phase 1G-A one alone.
    changes = remediation.successor_status_changes()
    assert set(changes) == {BAROTROPIC_TOKEN}
    remediation.check_current_scientific_status(
        frozen, CURRENT_SCIENTIFIC_STATUS, changes, additions=additions)


@pytest.mark.parametrize("token", list(ADDED))
def test_validator_rejects_an_undeclared_addition(remediation, frozen: dict, token: str) -> None:
    changes = remediation.successor_status_changes()
    additions = remediation.successor_status_additions()
    undeclared = {key: value for key, value in additions.items() if key != token}
    with pytest.raises(AssertionError, match=f"{token}: token absent from the frozen snapshot"):
        remediation.check_current_scientific_status(
            frozen, CURRENT_SCIENTIFIC_STATUS, changes, additions=undeclared)


def test_validator_rejects_a_new_live_token_that_no_record_declares(
    remediation, frozen: dict,
) -> None:
    changes = remediation.successor_status_changes()
    additions = remediation.successor_status_additions()
    live = {**CURRENT_SCIENTIFIC_STATUS, "UNDECLARED_TOKEN": "NOT_DERIVED"}
    with pytest.raises(AssertionError, match="UNDECLARED_TOKEN: token absent from the frozen"):
        remediation.check_current_scientific_status(frozen, live, changes, additions=additions)


@pytest.mark.parametrize("token", list(ADDED))
def test_validator_rejects_an_addition_the_frozen_snapshot_already_holds(
    remediation, frozen: dict, token: str,
) -> None:
    changes = remediation.successor_status_changes()
    additions = remediation.successor_status_additions()
    tampered = {**frozen, token: ADDED[token][0]}
    with pytest.raises(AssertionError, match=f"{token}: frozen snapshot already holds"):
        remediation.check_current_scientific_status(
            tampered, CURRENT_SCIENTIFIC_STATUS, changes, additions=additions)


@pytest.mark.parametrize("token", list(ADDED))
def test_validator_rejects_a_live_value_that_differs_from_the_record(
    remediation, frozen: dict, token: str,
) -> None:
    changes = remediation.successor_status_changes()
    additions = remediation.successor_status_additions()
    live = {**CURRENT_SCIENTIFIC_STATUS, token: "CHANGED"}
    with pytest.raises(AssertionError, match=f"{token}: live value differs from the successor"):
        remediation.check_current_scientific_status(frozen, live, changes, additions=additions)


def test_validator_rejects_an_addition_missing_from_the_live_module(
    remediation, frozen: dict,
) -> None:
    changes = remediation.successor_status_changes()
    additions = remediation.successor_status_additions()
    token = "VOID_ONSET_RESPONSE"
    live = {key: value for key, value in CURRENT_SCIENTIFIC_STATUS.items() if key != token}
    with pytest.raises(AssertionError, match="adds a token the live module lacks"):
        remediation.check_current_scientific_status(frozen, live, changes, additions=additions)


def test_validator_rejects_a_token_both_changed_and_added(remediation, frozen: dict) -> None:
    changes = remediation.successor_status_changes()
    additions = {**remediation.successor_status_additions(),
                 BAROTROPIC_TOKEN: {"value": "REFUTED_HADAMARD_ILL_POSED", "record": RECORD_JSON}}
    with pytest.raises(AssertionError, match="both changed and added"):
        remediation.check_current_scientific_status(
            frozen, CURRENT_SCIENTIFIC_STATUS, changes, additions=additions)


def test_validator_rejects_double_claims_and_tampered_records(
    remediation, frozen: dict, monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    record_path = Path(RECORD_JSON)
    barotropic_path = Path(BAROTROPIC_RECORD_JSON)
    later_paths = tuple(map(Path, LATER_RECORDS_JSON))  # keep later additions declared
    # A token added by two records is rejected ...
    monkeypatch.setattr(remediation, "STATUS_SUCCESSOR_RECORDS", (record_path, record_path))
    with pytest.raises(AssertionError, match="added by more than one successor record"):
        remediation.successor_status_additions()
    # ... as is a token superseded by two records (pre-existing failure mode).
    monkeypatch.setattr(remediation, "STATUS_SUCCESSOR_RECORDS", (barotropic_path, barotropic_path))
    with pytest.raises(AssertionError, match="superseded by more than one successor record"):
        remediation.successor_status_changes()
    record = load_json(PROJECT_ROOT / RECORD_JSON)
    # A tampered record value no longer matches the live module ...
    tampered = json.loads(json.dumps(record))
    tampered["status_additions"]["VOID_ONSET_RESPONSE"]["value"] = "DERIVED"
    tampered_path = tmp_path / "tampered_value.json"
    tampered_path.write_text(json.dumps(tampered), encoding="utf-8")
    monkeypatch.setattr(remediation, "STATUS_SUCCESSOR_RECORDS",
                        (barotropic_path, tampered_path, *later_paths))
    with pytest.raises(AssertionError, match="VOID_ONSET_RESPONSE: live value differs"):
        remediation.check_current_scientific_status(
            frozen, CURRENT_SCIENTIFIC_STATUS, remediation.successor_status_changes(),
            additions=remediation.successor_status_additions())
    # ... and a record cannot "add" an existing frozen token to bypass the
    # historical check.
    readded = json.loads(json.dumps(record))
    readded["status_additions"]["D3_VERDICT"] = {"value": "RESOLVED_DERIVED_4_10"}
    readded_path = tmp_path / "readded.json"
    readded_path.write_text(json.dumps(readded), encoding="utf-8")
    monkeypatch.setattr(remediation, "STATUS_SUCCESSOR_RECORDS",
                        (barotropic_path, readded_path, *later_paths))
    with pytest.raises(AssertionError, match="D3_VERDICT: frozen snapshot already holds"):
        remediation.check_current_scientific_status(
            frozen, CURRENT_SCIENTIFIC_STATUS, remediation.successor_status_changes(),
            additions=remediation.successor_status_additions())


# ------------------------------------------------ 1G-B documented limitation
# The Phase 1G-B caveat texts as committed at 8cf5c49: kept verbatim as the
# start of each extended text (extended, never weakened).
ORIGINAL_CAVEATS = {
    "comoving": (
        "volume_average_cgi_comoving: regular growing mode of the [GM] "
        "comoving closure, Eqs. (4.21)-(4.23), on the volume-average "
        "background; the [GM]-preferred parametrisation (Phase 1G-A Sec. 4.3)"),
    "meszaros": (
        "volume_average_cgi_meszaros_comparison_only: [GM] Eq. (4.27) is "
        "formally inapplicable to the Timescape framework ([GM] Sec. 5.1.1) "
        "and is retained only as a comparison baseline"),
    "wall": (
        "wall_regional_eds_common_time: sub-homogeneity modes assumed to grow "
        "as the EdS growing mode of the wall region in the common Buchert time "
        "t (Phase 1G-A Sec. 8; [W09] no backreaction within walls); evidence "
        "class DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION; the regional "
        "embedding stays NOT_DERIVED"),
}
ORIGINAL_SCALE_DEPENDENCE = (
    "growth_law_scale_dependence: the volume-average CGI law applies to "
    "super-homogeneity modes and the wall-regional EdS law to mass-weighted "
    "sub-homogeneity statistics; the choice is scale-dependent, is analysed "
    "in Phase 1G-C, and neither law is a default")
CGI_LIMITATION = (
    "faithfully implements [GM]'s {closure} closure, but that closure fails the "
    "separate-universe consistency test for the Timescape tracker "
    "(GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY = FAILED_FOR_TIMESCAPE_TRACKER), "
    "so this growth is not Timescape's long-wavelength growth")
WALL_LIMITATION = (
    "computes the wall-internal linear statistic relative to the wall mean, "
    "not a global-mean sigma at 8 h^-1 Mpc, which is not defined in the linear "
    "two-scale theory (LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC = "
    "NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY)")
LAWS = {
    "comoving": (ls.GrowthLaw.VOLUME_AVERAGE_CGI, CleanPerturbationSystem.COMOVING,
                 ls.VOLUME_AVERAGE_GROWTH_REFERENCE_NUMERICS),
    "meszaros": (ls.GrowthLaw.VOLUME_AVERAGE_CGI, CleanPerturbationSystem.MESZAROS,
                 ls.VOLUME_AVERAGE_GROWTH_REFERENCE_NUMERICS),
    "wall": (ls.GrowthLaw.WALL_REGIONAL_EDS_COMMON_TIME, ls.NOT_APPLICABLE,
             ls.WALL_REGIONAL_GROWTH_REFERENCE_CHECKS),
}
# Explicit photon-normalised radius (Mpc); the text does not depend on it.
EXPLICIT_RADIUS_MPC = 12.0
IDENTITY_RTOL = 1e-13  # the 1G-B per-photon identity budget, unchanged


@pytest.mark.parametrize("law", list(LAWS))
def test_lagrangian_sigma_results_carry_the_documented_limitation(law: str) -> None:
    growth_law, closure, numerics = LAWS[law]
    NA = ls.NOT_APPLICABLE
    result = ls.conditional_lagrangian_linear_sigma(
        background=ls.TimescapeTrackerInput.from_reference_preset(preset=PAPER_REFERENCE),
        growth_law=growth_law, closure=closure, growth_numerics=numerics,
        early_spectrum=ls.EarlySpectrumImport(
            A_s=2.100e-9, n_s=0.9649, k_pivot_per_Mpc=0.05, baryon_fraction=0.15633,
            T_cmb_K=2.7255, transfer_model=ls.EarlyTransferModel.EH98_ZERO_BARYON_OSCILLATION,
            provenance="Planck 2018 VI Table 2 (test fixture)",
            import_status=ls.EARLY_SPECTRUM_IMPORT_STATUS),
        radius=ls.LagrangianRadiusSpec(
            convention=ls.LagrangianRadiusConvention.EXPLICIT_PHOTON_NORMALISED_RADIUS,
            length_h_inverse_Mpc=NA, reference_omega_m=NA, reference_radius_Mpc=NA,
            explicit_radius_Mpc=EXPLICIT_RADIUS_MPC),
        quadrature=ls.LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE,
        density_identity_tolerance=IDENTITY_RTOL, G=1.0)
    caveat = result.model_caveat
    assert caveat.startswith(ORIGINAL_CAVEATS[law] + "; limitation (Phase 1G-D Secs. ")
    assert "added 2026-09-29" in caveat
    if law == "wall":
        assert "Secs. 9, 10" in caveat and WALL_LIMITATION in caveat
    else:
        assert "Secs. 5, 10" in caveat
        assert CGI_LIMITATION.format(closure={"comoving": "comoving",
                                              "meszaros": "Meszaros"}[law]) in caveat
    assert caveat in result.limitations
    scale = [item for item in result.limitations
             if item.startswith("growth_law_scale_dependence:")]
    assert len(scale) == 1 and scale[0].startswith(ORIGINAL_SCALE_DEPENDENCE + "; Phase 1G-D")
    payload = result.to_json_dict()
    assert payload["model_caveat"] == caveat
    assert payload["limitations"] == list(result.limitations)
    # The cited status tokens exist with the values the caveat quotes.
    assert (scientific_status.GM_CGI_CLOSURES_SEPARATE_UNIVERSE_CONSISTENCY
            == "FAILED_FOR_TIMESCAPE_TRACKER")
    assert (scientific_status.LINEAR_GLOBAL_MEAN_SIGMA_AT_8_H_INV_MPC
            == "NOT_DEFINED_IN_LINEAR_TWO_SCALE_THEORY")
    # Statuses are not relabelled.
    assert result.observational_status == "NON_OBSERVATIONAL"
    assert result.amplitude_status == "NOT_OBSERVATIONAL_SIGMA_8"
