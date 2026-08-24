"""Regional and carrier spectral diagnostics for Phase 1F-A.

The spectral representation diagonalises the Laplace--Beltrami operators
appearing in GM Eqs. (2.19)--(2.24), arXiv:2511.17160v2.  It is a theoretical
metric spectrum, never a global dressed or observational Fourier map.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import linalg as scipy_linalg

from timescape_fsigma8.phase1f_a.models import (
    BoundaryKernelPolicy,
    FloatArray,
    Phase1FAContractError,
    Phase1FANumerics,
    Phase1FAScientificState,
    RegionalDomainSpec,
    readonly_float,
    seal_integrity,
    validate_integrity,
)
from timescape_fsigma8.phase1f_a.operators import assemble_regional_elliptic_system
from timescape_fsigma8.transfer import ContinuumTransfer


@dataclass(frozen=True, kw_only=True)
class RegionalSpectrum:
    region: str
    generalized_eigenvalues: FloatArray
    physical_wavenumbers: FloatArray
    eigenvectors: FloatArray
    regional_indices: np.ndarray
    eigenpair_residuals: FloatArray
    basis_normalization_residual: float
    metric_identity: str
    scale_factor: float
    scale_units: str
    spectral_label: str
    provenance: str
    domain: RegionalDomainSpec = field(repr=False, compare=False)
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for name in (
            "generalized_eigenvalues", "physical_wavenumbers", "eigenvectors",
            "eigenpair_residuals",
        ):
            object.__setattr__(self, name, readonly_float(getattr(self, name), name))
        indices = np.array(self.regional_indices, dtype=np.int64, copy=True)
        indices.setflags(write=False)
        object.__setattr__(self, "regional_indices", indices)
        seal_integrity(self, self._live_state())

    def _live_state(self) -> object:
        return (
            self.region, self.generalized_eigenvalues, self.physical_wavenumbers,
            self.eigenvectors, self.regional_indices, self.eigenpair_residuals,
            self.basis_normalization_residual, self.metric_identity,
            self.scale_factor, self.scale_units, self.spectral_label,
            self.provenance, id(self.domain),
        )

    def validate_integrity(self) -> None:
        self.domain.validate_integrity()
        validate_integrity(self, self._live_state())


@dataclass(frozen=True, kw_only=True)
class CarrierGeneralizedSpectrum:
    generalized_eigenvalues: FloatArray
    eigenvectors: FloatArray
    eigenpair_residuals: FloatArray
    basis_normalization_residual: float
    spectral_labels: tuple[str, ...]
    metric_identity: str
    provenance: str
    scientific_state: Phase1FAScientificState = field(repr=False, compare=False)
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for name in ("generalized_eigenvalues", "eigenvectors", "eigenpair_residuals"):
            object.__setattr__(self, name, readonly_float(getattr(self, name), name))
        if any("observ" in label.lower() or label == "k" for label in self.spectral_labels):
            raise Phase1FAContractError("carrier spectrum cannot use observational/generic k labels")
        seal_integrity(self, self._live_state())

    def _live_state(self) -> object:
        return (
            self.generalized_eigenvalues, self.eigenvectors,
            self.eigenpair_residuals, self.basis_normalization_residual,
            self.spectral_labels, self.metric_identity, self.provenance,
            id(self.scientific_state),
        )

    def validate_integrity(self) -> None:
        self.scientific_state.validate_integrity()
        validate_integrity(self, self._live_state())


@dataclass(frozen=True, kw_only=True)
class SpectralTransferKernel:
    region: str
    kernel: FloatArray
    projection_residuals: FloatArray
    carrier_labels: tuple[str, ...]
    regional_label: str
    mode_diagonal_assumed: bool
    provenance: str
    _integrity_token: object = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "kernel", readonly_float(self.kernel, "kernel"))
        object.__setattr__(
            self,
            "projection_residuals",
            readonly_float(self.projection_residuals, "projection_residuals"),
        )
        if self.mode_diagonal_assumed:
            raise Phase1FAContractError("Phase 1F-A never assumes diagonal mode transfer")
        seal_integrity(self, self._live_state())

    def _live_state(self) -> object:
        return (
            self.region, self.kernel, self.projection_residuals,
            self.carrier_labels, self.regional_label,
            self.mode_diagonal_assumed, self.provenance,
        )

    def validate_integrity(self) -> None:
        validate_integrity(self, self._live_state())


def regional_laplace_beltrami_spectrum(
    *,
    regional_geometry: RegionalDomainSpec,
    boundary_policy: BoundaryKernelPolicy,
    scale_factor: float,
    scale_units: str,
    mode_count: int,
    numerics: Phase1FANumerics,
    provenance: str,
) -> RegionalSpectrum:
    """Solve ``K_r q=lambda M_r q`` and report ``sqrt(lambda)/a_r``.

    The eigenmode interpretation is the declared regional basis for the CGI
    Laplacian of GM Eqs. (2.19)--(2.24).  It is not a carrier, dressed, survey,
    or observational wavenumber map.
    """
    regional_geometry.validate_integrity()
    if not np.isfinite(scale_factor) or scale_factor <= 0.0:
        raise Phase1FAContractError("regional scale_factor must be explicit and positive")
    if not scale_units.strip() or not provenance.strip():
        raise Phase1FAContractError("regional spectral units and provenance are required")
    if mode_count <= 0:
        raise Phase1FAContractError("mode_count must be explicitly positive")
    system = assemble_regional_elliptic_system(
        domain=regional_geometry,
        boundary_policy=boundary_policy,
        numerics=numerics,
    )
    dense_k = system.stiffness.toarray()
    dense_m = np.diag(system.mass_weights)
    values, vectors = scipy_linalg.eigh(dense_k, dense_m)
    keep = np.flatnonzero(values > numerics.eigenpair_tolerance)
    if keep.size < mode_count:
        raise Phase1FAContractError("requested more regional modes than available")
    keep = keep[:mode_count]
    eigenvalues = values[keep]
    regional_vectors = vectors[:, keep]
    residuals = np.array(
        [
            np.linalg.norm(dense_k @ regional_vectors[:, i] - eigenvalues[i] * dense_m @ regional_vectors[:, i])
            for i in range(mode_count)
        ],
        dtype=np.float64,
    )
    normalization = regional_vectors.T @ dense_m @ regional_vectors
    normalization_residual = float(np.max(np.abs(normalization - np.eye(mode_count))))
    if np.max(residuals) > numerics.eigenpair_tolerance:
        raise Phase1FAContractError("regional generalized eigenpair residual exceeds tolerance")
    if normalization_residual > numerics.basis_normalization_tolerance:
        raise Phase1FAContractError("regional spectral basis normalization failed")
    full_vectors = np.zeros((regional_geometry.operator.size, mode_count), dtype=np.float64)
    full_vectors[system.regional_indices, :] = regional_vectors
    return RegionalSpectrum(
        region=regional_geometry.region,
        generalized_eigenvalues=eigenvalues,
        physical_wavenumbers=np.sqrt(eigenvalues) / scale_factor,
        eigenvectors=full_vectors,
        regional_indices=system.regional_indices,
        eigenpair_residuals=residuals,
        basis_normalization_residual=normalization_residual,
        metric_identity=regional_geometry.geometry.normalization.normalization_id,
        scale_factor=scale_factor,
        scale_units=scale_units,
        spectral_label=f"k_{regional_geometry.region}_physical",
        provenance=provenance,
        domain=regional_geometry,
    )


def carrier_generalized_spectrum(
    *,
    scientific_state: Phase1FAScientificState,
    mode_count: int,
    numerics: Phase1FANumerics,
    provenance: str,
) -> CarrierGeneralizedSpectrum:
    """Solve the physical mass-weighted carrier problem ``K_C q=lambda M_C q``.

    This is the authorised Phase 1F-A section 11.1 generalized spectrum.  It
    is deliberately distinct from the ordinary Euclidean stiffness spectrum
    and carries ``lambda_Gamma_n`` labels, not an observational Fourier ``k``.
    """
    scientific_state.validate_integrity()
    if mode_count <= 0 or not provenance.strip():
        raise Phase1FAContractError("carrier mode_count and provenance are required")
    operator = scientific_state.operator
    dense_k = operator.stiffness_matrix.toarray()
    mass_weights = operator.reference_weights * operator.metric_volume_ratio
    dense_m = np.diag(mass_weights)
    values, vectors = scipy_linalg.eigh(dense_k, dense_m)
    keep = np.flatnonzero(values > numerics.eigenpair_tolerance)
    if keep.size < mode_count:
        raise Phase1FAContractError("requested more carrier modes than available")
    keep = keep[:mode_count]
    eigenvalues = values[keep]
    eigenvectors = vectors[:, keep]
    residuals = np.array(
        [
            np.linalg.norm(dense_k @ eigenvectors[:, i] - eigenvalues[i] * dense_m @ eigenvectors[:, i])
            for i in range(mode_count)
        ],
        dtype=np.float64,
    )
    normalization_residual = float(
        np.max(np.abs(eigenvectors.T @ dense_m @ eigenvectors - np.eye(mode_count)))
    )
    if np.max(residuals) > numerics.eigenpair_tolerance:
        raise Phase1FAContractError("carrier generalized eigenpair residual exceeds tolerance")
    if normalization_residual > numerics.basis_normalization_tolerance:
        raise Phase1FAContractError("carrier spectral basis normalization failed")
    return CarrierGeneralizedSpectrum(
        generalized_eigenvalues=eigenvalues,
        eigenvectors=eigenvectors,
        eigenpair_residuals=residuals,
        basis_normalization_residual=normalization_residual,
        spectral_labels=tuple(f"lambda_Gamma_{index + 1}" for index in range(mode_count)),
        metric_identity="H1_CARRIER_GENERALIZED_MASS_MATRIX",
        provenance=provenance,
        scientific_state=scientific_state,
    )


def spectral_transfer_kernel(
    *,
    regional_spectrum: RegionalSpectrum,
    carrier_spectrum: CarrierGeneralizedSpectrum,
    continuum_transfer: ContinuumTransfer,
    numerics: Phase1FANumerics,
    provenance: str,
) -> SpectralTransferKernel:
    """Compute ``U_mn=<phi_m^C,T_r phi_n^r>_C`` without diagonality.

    The kernel is the authorised Phase 1F-A section 11.2 theoretical transfer
    representation.  It supplies no global dressed or observational Fourier
    mapping.
    """
    regional_spectrum.validate_integrity()
    carrier_spectrum.validate_integrity()
    if continuum_transfer.operator is not carrier_spectrum.scientific_state.operator:
        raise Phase1FAContractError("spectral transfer/operator state mismatch")
    if regional_spectrum.domain.scientific_state is not carrier_spectrum.scientific_state:
        raise Phase1FAContractError("regional and carrier spectra must share scientific state")
    if not provenance.strip():
        raise Phase1FAContractError("spectral transfer provenance is required")
    continuum_transfer._validate_assembled_state_integrity()
    basis_c = carrier_spectrum.eigenvectors
    mass = np.diag(
        continuum_transfer.operator.reference_weights
        * continuum_transfer.operator.metric_volume_ratio
    )
    kernel = np.zeros((basis_c.shape[1], regional_spectrum.eigenvectors.shape[1]))
    projection_residuals = np.zeros(regional_spectrum.eigenvectors.shape[1])
    for column in range(regional_spectrum.eigenvectors.shape[1]):
        response = continuum_transfer.transfer_source(
            regional_spectrum.eigenvectors[:, column],
            region=regional_spectrum.region,
            provenance=f"{provenance}:mode-{column + 1}",
        )
        transferred = response.transferred_field
        coefficients = basis_c.T @ mass @ transferred
        kernel[:, column] = coefficients
        remainder = transferred - basis_c @ coefficients
        projection_residuals[column] = np.sqrt(max(float(remainder.T @ mass @ remainder), 0.0))
    return SpectralTransferKernel(
        region=regional_spectrum.region,
        kernel=kernel,
        projection_residuals=projection_residuals,
        carrier_labels=carrier_spectrum.spectral_labels,
        regional_label=regional_spectrum.spectral_label,
        mode_diagonal_assumed=False,
        provenance=provenance,
    )
