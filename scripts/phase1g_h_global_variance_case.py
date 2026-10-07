"""Run one Phase 1G-H case from an explicit JSON configuration.

    python scripts/phase1g_h_global_variance_case.py --config scripts/phase1g_h_configs/<case>.json

Every scientific choice must be present in the configuration (no defaults):
background, matching redshift, early-spectrum import, radius convention,
void-share closure, quadratures and tolerances.  Named reference
configurations of the package may be selected by name.  The optional
homogeneity premise adds the constant-share interval (H15).  Prints the
record as JSON (or writes it with --output).  Conditional, model-internal,
NON_OBSERVATIONAL; see reports/phase1g_h_global_variance_closure.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import timescape_fsigma8.global_variance as gv
import timescape_fsigma8.lagrangian_sigma as ls

NA = ls.NOT_APPLICABLE
NAMED_QUADRATURES = {"LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE": ls.LAGRANGIAN_SIGMA_REFERENCE_QUADRATURE}
NAMED_CHECKS = {"TWO_PHASE_GROWTH_REFERENCE_CHECKS": gv.TWO_PHASE_GROWTH_REFERENCE_CHECKS}
REQUIRED = ("background", "matching", "early_spectrum", "radius", "void_share", "quadrature",
            "seed_quadrature", "growth_checks", "density_identity_tolerance", "G",
            "homogeneity_premise")


def _quadrature(entry):
    if entry == NA:
        return NA
    if isinstance(entry, str):
        return NAMED_QUADRATURES[entry]
    return ls.LagrangianSigmaQuadrature(**entry)


def _radius(entry: dict) -> ls.LagrangianRadiusSpec:
    fields = dict(entry)
    fields["convention"] = ls.LagrangianRadiusConvention(fields["convention"])
    return ls.LagrangianRadiusSpec(**fields)


def _closure(entry: dict, background: ls.TimescapeTrackerInput, matching, checks, G):
    kind = entry["closure"]
    if kind == "constant":
        return gv.ConstantVoidShare(share=entry["share"], provenance=entry["provenance"],
                                    evidence_class=entry["evidence_class"])
    if kind != "gaussian_threshold_seed":
        raise SystemExit(f"unknown void-share closure {kind!r}")
    compression = gv.SeedVolumeCompression(entry["compression"])
    if "seed_radius_Mpc" in entry:
        radius = entry["seed_radius_Mpc"]
    else:
        # Tracker-consistent mapping (GD-OD1) of an explicit present void radius.
        growth = gv.two_phase_global_growth(background=background, matching=matching,
                                            checks=checks, G=G)
        density = ls.early_matter_density_per_photon(background=background,
                                                     identity_tolerance=1e-13, G=G)
        h = {"dressed": density.h_dressed, "bare": density.h_bare}[entry["h_for_void_radius"]]
        radius = gv.tracker_consistent_seed_radius(
            present_void_radius_volume_average_proper_Mpc=entry[
                "present_void_radius_h_inverse_Mpc"] / h,
            f_v_seed=growth.f_v_ls, fv0=growth.fv0, gamma_w0=growth.gamma_w0)
    return gv.GaussianThresholdSeedVoidShare(seed_radius_Mpc=radius,
                                             seed_radius_provenance=entry["provenance"],
                                             compression=compression)


def run(config: dict) -> dict:
    missing = [key for key in REQUIRED if key not in config]
    if missing:
        raise SystemExit(f"configuration lacks mandatory entries: {missing}")
    background = ls.TimescapeTrackerInput(**config["background"])
    matching = gv.LastScatteringMatching(**config["matching"])
    spec = dict(config["early_spectrum"])
    spec["transfer_model"] = ls.EarlyTransferModel(spec["transfer_model"])
    early = ls.EarlySpectrumImport(**spec)
    checks = (NAMED_CHECKS[config["growth_checks"]] if isinstance(config["growth_checks"], str)
              else gv.TwoPhaseGrowthChecks(**config["growth_checks"]))
    G = config["G"]
    closure = _closure(config["void_share"], background, matching, checks, G)
    record = gv.conditional_global_linear_sigma(
        background=background, matching=matching, growth_checks=checks,
        void_share_closure=closure, early_spectrum=early, radius=_radius(config["radius"]),
        quadrature=_quadrature(config["quadrature"]),
        seed_quadrature=_quadrature(config["seed_quadrature"]),
        density_identity_tolerance=config["density_identity_tolerance"], G=G)
    out = {"record": record.to_json_dict()}
    premise = config["homogeneity_premise"]
    if premise != NA:
        interval = gv.admissible_global_linear_interval(
            target=record,
            premise=gv.HomogeneityPremise(radius=_radius(premise["radius"]),
                                          max_linear_rms=premise["max_linear_rms"],
                                          provenance=premise["provenance"]))
        out["admissible_interval"] = interval.to_json_dict()
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    out = run(json.loads(args.config.read_text(encoding="utf-8")))
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_bytes(text.encode("utf-8"))
    else:
        sys.stdout.write(text)
    rec = out["record"]
    print(f"linear_sigma = {rec['linear_sigma']:.6f} at R = {rec['radius']['radius_Mpc']:.4f} Mpc "
          f"(void share p0 = {rec['void_share']['share_k0']:.5f}, regime "
          f"{rec['void_response_regime']})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
