import numpy as np
import pytest

from timescape_fsigma8.background import TrackerParams

# Paper/upstream parameter values: fv0 = 0.737 ([GM] Sec. 5.1.1);
# HD0 in "H0 = 1" code units, HD0 = 2(2+fv0)/(4 fv0^2 + fv0 + 4)
# ([GM] text p. 25). Matches the upstream notebook's derived HD0.
FV0 = 0.737


@pytest.fixture(scope="session")
def params() -> TrackerParams:
    return TrackerParams.from_dressed_H0(fv0=FV0, H0=1.0)


@pytest.fixture(scope="session")
def tgrid(params: TrackerParams) -> np.ndarray:
    """Time grid spanning early matter era to today (t0), t > 0."""
    return np.linspace(0.01 * params.t0, params.t0, 400)
