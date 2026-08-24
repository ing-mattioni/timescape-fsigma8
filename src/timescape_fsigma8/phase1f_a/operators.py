"""Regional broken Laplace--Beltrami reference operators for Phase 1F-A.

The strong CGI scalarizations follow Eqs. (2.2), (2.19)--(2.24) of
arXiv:2511.17160v2.  The no-flux regional discretisation is the explicitly
authorised Phase 1F-A V1 boundary closure, not a physical interface law.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike
from scipy import linalg as scipy_linalg
from scipy import sparse
from scipy.sparse import linalg as sparse_linalg

from timescape_fsigma8.phase1f_a.models import (
    BoundaryKernelPolicy,
    FloatArray,
    Phase1FAContractError,
    Phase1FADegeneracyError,
    Phase1FANumerics,
    RegionalDomainSpec,
    RegionalZeroModeClosure,
    readonly_float,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class RegionalEllipticDiagnostics:
    source_compatibility_residual: float
    solution_mean_residual: float
    equation_residual_max_abs: float
    equation_residual_normalized: float
    kernel_dimension_before_normalization: int
    condition_number: float


@dataclass(frozen=True, slots=True, kw_only=True)
class RegionalEllipticSystem:
    domain: RegionalDomainSpec
    regional_indices: np.ndarray
    stiffness: sparse.csr_matrix
    mass_weights: FloatArray
    generalized_eigenvalues: FloatArray
    condition_number: float


def _isotropic_coefficient(domain: RegionalDomainSpec, numerics: Phase1FANumerics) -> FloatArray:
    tensor = domain.geometry.elliptic_tensor_density
    diagonal = np.diagonal(tensor, axis1=-2, axis2=-1)
    off_diagonal = np.array(tensor, copy=True)
    for axis in range(domain.geometry.dimension):
        off_diagonal[..., axis, axis] = 0.0
    if np.max(np.abs(off_diagonal)) > numerics.eigenpair_tolerance:
        raise Phase1FAContractError(
            "Phase 1F-A structured regional inversion supports isotropic tensor density only"
        )
    if not np.allclose(
        diagonal,
        diagonal[..., :1],
        rtol=0.0,
        atol=numerics.eigenpair_tolerance,
    ):
        raise Phase1FAContractError(
            "Phase 1F-A structured regional inversion supports equal principal coefficients only"
        )
    result = np.array(diagonal[..., 0], dtype=np.float64, copy=True)
    result.setflags(write=False)
    return result


def assemble_regional_elliptic_system(
    *,
    domain: RegionalDomainSpec,
    boundary_policy: BoundaryKernelPolicy,
    numerics: Phase1FANumerics,
) -> RegionalEllipticSystem:
    """Assemble the broken regional positive operator ``K_r=-M_r L_r``.

    ``L_r=a_r^2 D_r^2=Delta_gamma_r`` is the regional CGI operator from
    Eqs. (2.2), (2.19)--(2.24) of arXiv:2511.17160v2.  Interface-crossing
    faces are omitted to implement the explicit V1 no-flux boundary policy;
    this does not impose a physical density junction condition.
    """
    domain.validate_integrity()
    if boundary_policy.domain != domain.region:
        raise Phase1FAContractError("boundary policy domain does not match region")
    operator = domain.operator
    shape = operator.carrier.grid_shape
    mask_grid = domain.mask.reshape(shape)
    full_indices = np.flatnonzero(mask_grid.reshape(-1))
    local_index = {int(full): local for local, full in enumerate(full_indices)}
    coefficient = _isotropic_coefficient(domain, numerics).reshape(shape)
    reference_weights = operator.reference_weights.reshape(shape)
    ratio = domain.geometry.metric_volume_ratio.reshape(shape)

    rows: list[int] = []
    columns: list[int] = []
    data: list[float] = []
    for index in np.ndindex(shape):
        if not mask_grid[index]:
            continue
        left_full = int(np.ravel_multi_index(index, shape))
        left = local_index[left_full]
        for axis, spacing in enumerate(operator.carrier.grid_spacing):
            neighbor = list(index)
            neighbor[axis] = (neighbor[axis] + 1) % shape[axis]
            neighbor_tuple = tuple(neighbor)
            if not mask_grid[neighbor_tuple]:
                continue
            right_full = int(np.ravel_multi_index(neighbor_tuple, shape))
            right = local_index[right_full]
            k_left = float(coefficient[index])
            k_right = float(coefficient[neighbor_tuple])
            harmonic = 2.0 * k_left * k_right / (k_left + k_right)
            conductance = harmonic * float(reference_weights[index]) / spacing**2
            rows.extend((left, left, right, right))
            columns.extend((left, right, left, right))
            data.extend((conductance, -conductance, -conductance, conductance))
    size = len(full_indices)
    stiffness = sparse.coo_matrix(
        (data, (rows, columns)), shape=(size, size), dtype=np.float64
    ).tocsr()
    dense = stiffness.toarray()
    eigenvalues = np.linalg.eigvalsh(0.5 * (dense + dense.T))
    kernel = int(np.count_nonzero(np.abs(eigenvalues) <= numerics.eigenpair_tolerance))
    if kernel != 1:
        raise Phase1FADegeneracyError(
            f"{domain.region} regional operator must have exactly one constant kernel; got {kernel}"
        )
    mass = (
        reference_weights.reshape(-1)[full_indices]
        * ratio.reshape(-1)[full_indices]
    )
    basis = scipy_linalg.null_space(mass[np.newaxis, :])
    reduced_k = basis.T @ dense @ basis
    reduced_m = basis.T @ np.diag(mass) @ basis
    positive = scipy_linalg.eigvalsh(
        0.5 * (reduced_k + reduced_k.T),
        0.5 * (reduced_m + reduced_m.T),
    )
    if positive.size == 0 or np.min(positive) <= numerics.eigenpair_tolerance:
        raise Phase1FADegeneracyError("regional constrained operator is not coercive")
    condition_number = float(np.max(positive) / np.min(positive))
    if condition_number > numerics.maximum_condition_number:
        raise Phase1FADegeneracyError(
            "regional elliptic condition number exceeds configured maximum"
        )
    full_indices = np.array(full_indices, dtype=np.int64, copy=True)
    full_indices.setflags(write=False)
    mass = np.array(mass, dtype=np.float64, copy=True)
    mass.setflags(write=False)
    positive = np.array(positive, dtype=np.float64, copy=True)
    positive.setflags(write=False)
    return RegionalEllipticSystem(
        domain=domain,
        regional_indices=full_indices,
        stiffness=stiffness,
        mass_weights=mass,
        generalized_eigenvalues=positive,
        condition_number=condition_number,
    )


def apply_regional_laplace_beltrami(
    *, system: RegionalEllipticSystem, field: ArrayLike
) -> FloatArray:
    """Apply ``L_r=-M_r^-1 K_r`` (GM Eqs. (2.19)--(2.24))."""
    system.domain.validate_integrity()
    values = readonly_float(field, "regional field").reshape(-1)
    if values.shape != (system.regional_indices.size,):
        raise Phase1FAContractError("regional field has the wrong size")
    result = -(system.stiffness @ values) / system.mass_weights
    result = np.asarray(result, dtype=np.float64)
    result.setflags(write=False)
    return result


def solve_regional_laplace_beltrami(
    *,
    source: ArrayLike,
    system: RegionalEllipticSystem,
    zero_mode_closure: RegionalZeroModeClosure,
    numerics: Phase1FANumerics,
) -> tuple[FloatArray, RegionalEllipticDiagnostics]:
    """Solve ``Delta_gamma_r u=source`` with explicit regional mean zero.

    The scalarization is inherited from GM Eqs. (2.2), (2.19)--(2.24).
    The regional homogeneous-mode value is the explicit Phase 1F-A V1
    external normalization closure, never inferred from the CGI source.
    """
    system.domain.validate_integrity()
    if zero_mode_closure.domain != system.domain.region:
        raise Phase1FAContractError("zero-mode closure domain does not match region")
    expected_measure = (
        f"a_{system.domain.region}^3 dmu_gamma_{system.domain.region}"
    )
    if zero_mode_closure.spatial_measure_identity != expected_measure:
        raise Phase1FAContractError(
            "zero-mode closure spatial measure does not match the regional metric"
        )
    values = readonly_float(source, "regional CGI source").reshape(-1)
    if values.shape != (system.regional_indices.size,):
        raise Phase1FAContractError("regional CGI source has the wrong size")
    mass = system.mass_weights * zero_mode_closure.scale_factor**3
    compatibility = float(np.dot(mass, values) / np.sum(mass))
    if abs(compatibility) > numerics.source_compatibility_tolerance:
        raise Phase1FADegeneracyError(
            "regional CGI source does not annihilate the constant kernel"
        )
    rhs = -(mass * values) / zero_mode_closure.scale_factor**3
    weights_column = sparse.csr_matrix(mass[:, np.newaxis])
    kkt = sparse.bmat(
        [[system.stiffness, weights_column], [weights_column.T, None]],
        format="csr",
    )
    augmented = np.concatenate((rhs, np.array([0.0], dtype=np.float64)))
    try:
        solution = sparse_linalg.spsolve(kkt, augmented)[:-1]
    except Exception as exc:
        raise Phase1FADegeneracyError("regional constrained elliptic solve failed") from exc
    solution = np.asarray(solution, dtype=np.float64)
    if not np.all(np.isfinite(solution)):
        raise Phase1FADegeneracyError("regional elliptic solution is nonfinite")
    reconstructed = apply_regional_laplace_beltrami(system=system, field=solution)
    residual = reconstructed - values
    mean = float(np.dot(mass, solution) / np.sum(mass))
    residual_max = float(np.max(np.abs(residual)))
    residual_normalized = float(
        np.linalg.norm(residual)
        / max(np.linalg.norm(values), numerics.residual_norm_floor)
    )
    if residual_max > numerics.elliptic_residual_tolerance:
        raise Phase1FAContractError("regional elliptic equation residual exceeds tolerance")
    if abs(mean) > numerics.mean_tolerance:
        raise Phase1FAContractError("regional mean-zero normalization failed")
    solution.setflags(write=False)
    diagnostics = RegionalEllipticDiagnostics(
        source_compatibility_residual=compatibility,
        solution_mean_residual=mean,
        equation_residual_max_abs=residual_max,
        equation_residual_normalized=residual_normalized,
        kernel_dimension_before_normalization=1,
        condition_number=system.condition_number,
    )
    return solution, diagnostics


def embed_regional_field(
    *, system: RegionalEllipticSystem, regional_field: ArrayLike
) -> FloatArray:
    """Embed regional values by zero extension; the mask retains provenance."""
    values = readonly_float(regional_field, "regional_field").reshape(-1)
    if values.shape != (system.regional_indices.size,):
        raise Phase1FAContractError("regional field has the wrong size")
    full = np.zeros(system.domain.operator.size, dtype=np.float64)
    full[system.regional_indices] = values
    full.setflags(write=False)
    return full
