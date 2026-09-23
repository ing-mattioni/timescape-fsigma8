"""Reproducibility gates made checkout-independent (review finding F6).

The pinned upstream notebook identity no longer depends on core.autocrlf, and
the historical validators check ancestry against recorded commits instead of
branch names or ``main`` equality.  These tests cover the helpers and pins;
the validators' full runs are recorded in
reports/phase1f_c_r_f2_f4_f9_remediation.md.
"""

from __future__ import annotations

import hashlib
import importlib
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

LF = "628c441288d67854e0380518841dede3680bddab610e9ef5cea04937455cea2a"
CRLF = "86d2534db9e9b3169835e4ce223ee8f3bff6d03b47e5677d3937fed4adafe55a"
NOTEBOOK = (
    PROJECT_ROOT
    / ".reference"
    / "Linear-Perturbations-in-averaged-cosmological-models"
    / "ACPT_Timescape.ipynb"
)


def lock_values() -> dict[str, str]:
    values = {}
    for line in (PROJECT_ROOT / "UPSTREAM.lock").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


def git_available() -> bool:
    return shutil.which("git") is not None and (PROJECT_ROOT / ".git").exists()


def test_notebook_identity_pins_agree_across_lock_and_scripts() -> None:
    values = lock_values()
    assert values["notebook_sha256_lf"] == LF
    assert values["notebook_sha256_crlf"] == CRLF
    extractor = importlib.import_module("extract_upstream_barotropic_oracle")
    assert extractor.EXPECTED_NOTEBOOK_SHA256_LF == LF
    anchored = importlib.import_module("validate_anchored_density_growth")
    assert anchored.NOTEBOOK_SHA256_LF == LF
    assert anchored.NOTEBOOK_SHA256 == CRLF  # frozen provenance label only
    remediation = importlib.import_module("validate_phase1f_c_r_astra_remediation")
    assert remediation.LINE_ENDING_EQUIVALENTS == {CRLF: LF}


def test_lf_normalised_hash_is_checkout_independent(tmp_path: Path) -> None:
    extractor = importlib.import_module("extract_upstream_barotropic_oracle")
    lf_file = tmp_path / "lf.txt"
    crlf_file = tmp_path / "crlf.txt"
    lf_file.write_bytes(b'{"a": 1}\n{"b": 2}\n')
    crlf_file.write_bytes(b'{"a": 1}\r\n{"b": 2}\r\n')
    assert extractor.sha256(lf_file) != extractor.sha256(crlf_file)
    assert extractor.sha256_lf(lf_file) == extractor.sha256_lf(crlf_file)
    assert extractor.sha256_lf(lf_file) == extractor.sha256(lf_file)


def test_pinned_notebook_matches_its_lf_identity_when_present() -> None:
    if not NOTEBOOK.is_file():
        pytest.skip("upstream clone absent")
    data = NOTEBOOK.read_bytes()
    assert hashlib.sha256(data).hexdigest() in {LF, CRLF}
    assert hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest() == LF


def test_local_provenance_status_reports_absence_and_rejects_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    remediation = importlib.import_module("validate_phase1f_c_r_astra_remediation")
    content = b"line one\r\nline two\r\n"
    path = tmp_path / "audit.md"
    path.write_bytes(content)
    raw = hashlib.sha256(content).hexdigest()
    normalized = hashlib.sha256(content.replace(b"\r\n", b"\n")).hexdigest()
    assert remediation.local_file_status(str(path), raw) == "VERIFIED"
    assert remediation.local_file_status(str(tmp_path / "missing.md"), raw) == (
        "ABSENT_FROM_CHECKOUT"
    )
    lf_copy = tmp_path / "audit_lf.md"
    lf_copy.write_bytes(content.replace(b"\r\n", b"\n"))
    monkeypatch.setattr(remediation, "LINE_ENDING_EQUIVALENTS", {raw: normalized})
    assert remediation.local_file_status(str(lf_copy), raw) == (
        "VERIFIED_LINE_ENDING_EQUIVALENT"
    )
    with pytest.raises(AssertionError, match="differs from the inventory pin"):
        remediation.local_file_status(str(path), "0" * 64)


def test_recorded_commits_are_ancestors_of_head_when_history_is_available() -> None:
    if not git_available():
        pytest.skip("git history unavailable")
    remediation = importlib.import_module("validate_phase1f_c_r_astra_remediation")
    anchored = importlib.import_module("validate_anchored_density_growth")
    commits = {
        "1F-C-R base": remediation.BASE,
        "1F-C-R certified": remediation.REMEDIATION,
        "1D-D-t base": anchored.BASE_PHASE1D_D_T_CHECKPOINT,
        "1D-D phase": anchored.PHASE1D_D_COMMIT,
    }
    for label, commit in commits.items():
        present = subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            cwd=PROJECT_ROOT,
            capture_output=True,
        )
        if present.returncode != 0:
            pytest.skip(f"shallow history lacks {label}")
        assert anchored.is_ancestor(commit, "HEAD"), label
    for tag, commit in (
        ("phase-1f-c-r-astra-audit-remediation-v2", remediation.REMEDIATION),
        ("phase-1d-d-anchored-density-growth-v1", anchored.PHASE1D_D_COMMIT),
    ):
        peeled = subprocess.run(
            ["git", "rev-parse", "-q", "--verify", f"{tag}^{{}}"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if peeled:
            assert peeled == commit, tag
