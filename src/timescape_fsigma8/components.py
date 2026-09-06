"""Component ontology for the selected first-order spatial tensor realization.

BMR Eq. (2.6), arXiv:1912.04213v2, gives the coordinate covector
``A_i=partial_i ln N``. Raising its index and changing its frame are tensor
representations of that identity, not new dynamics. Phase 1F-C-R A02 declares
the same positive-diagonal inverse-metric Cholesky frame as Phase 1F-B.
"""

from enum import Enum

import numpy as np
from numpy.typing import ArrayLike, NDArray


class ComponentRepresentation(str, Enum):
    COORDINATE_COVECTOR = "COORDINATE_COVECTOR"
    COORDINATE_CONTRAVARIANT = "COORDINATE_CONTRAVARIANT"
    PHYSICAL_ORTHONORMAL = "PHYSICAL_ORTHONORMAL"


def orthonormal_components(
    covector: NDArray[np.float64],
    inverse_reference_metric: NDArray[np.float64],
    scale_factor: ArrayLike,
) -> NDArray[np.float64]:
    """Return ``L^T A/a`` with ``gamma^-1=L L^T`` (BMR Eq. (2.6)).

    The declared frame is ``e_hat^i=L^i_hat/a``; hence ``e h e^T=I``
    for ``h=a^2 gamma``. First-order metric corrections times first-order
    acceleration are second order. Inputs have shape (..., points, dimension)
    and (points, dimension, dimension); callers validate metric and scale.
    This is the frozen Phase 1F-B component conversion, shared with 1F-C.
    """
    cholesky = np.linalg.cholesky(inverse_reference_metric)
    return np.einsum("nji,...nj->...ni", cholesky, covector, optimize=True) / scale_factor
