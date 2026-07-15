"""Audited unit conversions for Hubble rates and times.

Primary constants, each exact by definition of its standards body:

  AU_KM          1 astronomical unit = 149 597 870.700 km
                 (IAU 2012 Resolution B2, exact).
  PC_KM          1 parsec = (648 000 / pi) au
                 (IAU 2015 Resolution B2, exact definition).
  DAY_S          1 day = 86 400 s (exact).
  JULIAN_YEAR_S  1 Julian year = 365.25 day = 31 557 600 s (IAU, exact).

Everything else is derived here from these primaries — no rounded
intermediate values enter any conversion. The derived megaparsec,
MPC_KM = 3.0856775814913673e19 km, is cross-checked in tests against the
IAU-quoted value.

Comparison only (NOT used in any conversion): the upstream notebook
(cell 2) uses the approximation 1/H0 = (9.778/h) Gyr, i.e. a Hubble time
of 9.778 Gyr at H0 = 100 km/s/Mpc. The exact value from the primaries is
HUBBLE_TIME_GYR_AT_H100 = 9.77792222... Gyr (relative difference ~8e-6);
the approximation is retained as UPSTREAM_HUBBLE_TIME_GYR_AT_H100 solely
so tests and reports can quantify that difference.
"""

from __future__ import annotations

import math

# --- primary constants (exact by definition) -------------------------------
AU_KM = 149_597_870.700          # km per astronomical unit (IAU 2012 B2)
PC_KM = AU_KM * 648_000.0 / math.pi   # km per parsec (IAU 2015 B2)
MPC_KM = 1.0e6 * PC_KM           # km per megaparsec
DAY_S = 86_400.0                 # seconds per day
JULIAN_YEAR_S = 365.25 * DAY_S   # seconds per Julian year (= 31 557 600 s)
GYR_S = 1.0e9 * JULIAN_YEAR_S    # seconds per gigayear (Julian)

# --- upstream approximation, documented for comparison only ----------------
UPSTREAM_HUBBLE_TIME_GYR_AT_H100 = 9.778   # upstream notebook cell 2; approx


def kms_per_mpc_to_per_s(H: float) -> float:
    """Convert a rate from km s^-1 Mpc^-1 to s^-1 (divide by km per Mpc)."""
    return H / MPC_KM


def kms_per_mpc_to_per_gyr(H: float) -> float:
    """Convert a rate from km s^-1 Mpc^-1 to Gyr^-1."""
    return H * GYR_S / MPC_KM


def per_gyr_to_kms_per_mpc(H: float) -> float:
    """Convert a rate from Gyr^-1 to km s^-1 Mpc^-1."""
    return H * MPC_KM / GYR_S


def per_s_to_per_gyr(H: float) -> float:
    """Convert a rate from s^-1 to Gyr^-1."""
    return H * GYR_S


def per_gyr_to_per_s(H: float) -> float:
    """Convert a rate from Gyr^-1 to s^-1."""
    return H / GYR_S


def hubble_time_gyr(H0_kms_per_mpc: float) -> float:
    """Hubble time 1/H0 in Gyr for H0 given in km s^-1 Mpc^-1."""
    return 1.0 / kms_per_mpc_to_per_gyr(H0_kms_per_mpc)


# Exact Hubble time at H0 = 100 km/s/Mpc, for comparison with the upstream
# 9.778 Gyr approximation (module docstring).
HUBBLE_TIME_GYR_AT_H100 = hubble_time_gyr(100.0)
