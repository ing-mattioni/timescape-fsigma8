"""Schema and monochrome-plot compliance tests for Phase 1C-B2 outputs."""

from copy import deepcopy
import json
from pathlib import Path
import sys

import numpy as np
import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _phase1c_b2_plot_styles import K_MODE_STYLES, style_for_k  # noqa: E402
import validate_barotropic_perturbations as validation  # noqa: E402
from timescape_fsigma8.perturbations import (  # noqa: E402
    BarotropicScenario,
    D3Branch,
    EpochChoice,
    RateUnitConvention,
    SolverConfig,
    TiltForm,
    WavenumberConvention,
)


B2_OUTPUTS = {
    "phase1c_b2_oracle_comparison.json": 6,
    "phase1c_b2_convergence.json": 42,
    "phase1c_b2_d2_d3_factorial.json": 12,
    "phase1c_b2_scenario_effects.json": 36,
    "phase1c_b2_figure_endpoints.json": 9,
}
OUTPUT_DIR = PROJECT_ROOT / "artifacts" / "independent"


def _load_outputs() -> dict[str, dict]:
    outputs = {}
    for name in B2_OUTPUTS:
        path = OUTPUT_DIR / name
        if not path.is_file():
            # Repo convention: generated artifacts are git-ignored, so on a
            # fresh clone these tests skip (like the oracle tests) instead of
            # failing.
            pytest.skip(
                f"B2 artifact absent ({name}); run "
                "scripts/validate_barotropic_perturbations.py"
            )
        outputs[name] = json.loads(path.read_text(encoding="utf-8"))
    return outputs


def test_all_five_b2_json_outputs_use_complete_run_record_schema():
    """Parse every generated B2 JSON and validate every represented run."""
    outputs = _load_outputs()
    all_records = []
    for name, expected_count in B2_OUTPUTS.items():
        data = outputs[name]
        assert data["run_record_schema"] == validation.run_record_schema()
        records = validation.collect_run_records(data)
        assert len(records) == expected_count, name
        all_records.extend(records)

    # Stable configuration identifiers may repeat for repeated execution of
    # the exact same configuration, but distinct complete records may not
    # collide and identical complete records may not receive different IDs.
    payload_to_identifier = {}
    identifier_to_payload = {}
    for record in all_records:
        validation.validate_run_record(record)
        payload = json.dumps(
            {k: v for k, v in record.items() if k != "run_identifier"},
            sort_keys=True,
            separators=(",", ":"),
        )
        identifier = record["run_identifier"]
        assert payload_to_identifier.setdefault(payload, identifier) == identifier
        assert identifier_to_payload.setdefault(identifier, payload) == payload


def test_run_identifier_covers_every_scientific_and_solver_field():
    """Changing any schema field invalidates the stable run identifier."""
    selected = BarotropicScenario(
        k=2.0 * np.pi,
        branch=D3Branch.PRINTED_4_15,
        tilt_form=TiltForm.UNRESCALED_V,
        rate_convention=RateUnitConvention.UPSTREAM_UNCONVERTED,
        epoch_choice=EpochChoice.UPSTREAM_0P218_GYR,
        wavenumber_convention=WavenumberConvention.UPSTREAM_TIMESCAPE_K,
        timescape_h=0.7323,
        lcdm_h=0.674,
    )
    config = SolverConfig(
        method="DOP853", rtol=1e-11, atol=1e-13, max_step=np.inf, first_step=None
    )
    original = validation.run_record(selected, config, "corrected_phase1b")
    replacements = {
        "branch": D3Branch.DERIVED_4_10.value,
        "tilt_form": TiltForm.RESCALED_VTILDE.value,
        "rate_unit_convention": RateUnitConvention.LCDM_TO_TIMESCAPE_CONVERTED.value,
        "epoch_choice": EpochChoice.DRESSED_Z20.value,
        "wavenumber_convention": WavenumberConvention.PAPER_LCDM_HUBBLE_K.value,
        "numerical_k": 5.0 * np.pi,
        "timescape_h": 0.73,
        "lcdm_h": 0.675,
        "sound_speed_provenance": "upstream_d2_corrupted",
    }
    for field, value in replacements.items():
        changed = deepcopy(original)
        changed[field] = value
        with pytest.raises(ValueError, match="run_identifier"):
            validation.validate_run_record(changed)

    solver_replacements = {
        "method": "RK45",
        "rtol": 2e-11,
        "atol": 2e-13,
        "max_step": 0.1,
        "first_step": 1e-5,
        "dense_output": True,
        "events": [],
        "vectorized": True,
    }
    for field, value in solver_replacements.items():
        changed = deepcopy(original)
        changed["solver"][field] = value
        with pytest.raises(ValueError, match="run_identifier"):
            validation.validate_run_record(changed)


def test_figure3_k_modes_have_distinct_shared_noncolour_styles():
    """All Figure 3 plotters share three inspectably distinct mode styles."""
    styles = [style_for_k(multiplier * np.pi) for multiplier in (2, 5, 10)]
    encodings = {(style["linestyle"], style["marker"]) for style in styles}
    assert len(encodings) == 3
    assert set(K_MODE_STYLES) == {2, 5, 10}
    for script_name in (
        "make_barotropic_fig3.py",
        "make_barotropic_fig3_forensic.py",
    ):
        source = (PROJECT_ROOT / "scripts" / script_name).read_text(encoding="utf-8")
        assert "from _phase1c_b2_plot_styles import style_for_k" in source
        assert "style_for_k(" in source
