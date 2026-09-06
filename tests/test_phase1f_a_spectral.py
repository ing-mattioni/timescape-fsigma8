"""Phase 1F-A regional/carrier generalized spectral tests."""

# A06: absolute budgets use rtol=0; relative budgets use atol=0.
# Previously implicit algebraic comparisons use rtol=2e-12, atol=1e-14
# in the fixture units (roundoff allowance); explicit convergence budgets remain.

from __future__ import annotations

from dataclasses import fields
import inspect

import numpy as np

from phase1f_a_test_utils import boundary, domain, make_realization
from timescape_fsigma8.phase1f_a import (
    CarrierGeneralizedSpectrum,
    RegionalSpectrum,
    carrier_generalized_spectrum,
    regional_laplace_beltrami_spectrum,
    spectral_transfer_kernel,
)
from timescape_fsigma8.transfer import ContinuumTransfer


def test_t14_regional_and_carrier_generalized_eigenpair_residuals() -> None:
    realization = make_realization()
    regional = regional_laplace_beltrami_spectrum(
        regional_geometry=domain(realization, "wall"),
        boundary_policy=boundary("wall"),
        scale_factor=0.8,
        scale_units="INVERSE_REFERENCE_LENGTH",
        mode_count=4,
        numerics=realization.numerics,
        provenance="REGIONAL_GENERALIZED_SPECTRAL_VALIDATION",
    )
    carrier = carrier_generalized_spectrum(
        scientific_state=realization.scientific_state,
        mode_count=8,
        numerics=realization.numerics,
        provenance="CARRIER_GENERALIZED_SPECTRAL_VALIDATION",
    )
    assert np.max(regional.eigenpair_residuals) <= realization.numerics.eigenpair_tolerance
    assert np.max(carrier.eigenpair_residuals) <= realization.numerics.eigenpair_tolerance
    assert regional.basis_normalization_residual <= realization.numerics.basis_normalization_tolerance
    assert carrier.basis_normalization_residual <= realization.numerics.basis_normalization_tolerance
    np.testing.assert_allclose(
        regional.physical_wavenumbers,
        np.sqrt(regional.generalized_eigenvalues) / 0.8, rtol=2e-12, atol=1e-14,
    )


def test_t15_ordinary_stiffness_and_generalized_mass_spectra_remain_distinct() -> None:
    realization = make_realization()
    operator = realization.scientific_state.operator
    carrier = carrier_generalized_spectrum(
        scientific_state=realization.scientific_state,
        mode_count=2,
        numerics=realization.numerics,
        provenance="ORDINARY_GENERALIZED_DISTINCTION",
    )
    assert operator.ordinary_euclidean_constrained_stiffness_eigenvalue != carrier.generalized_eigenvalues[0]
    assert carrier.generalized_eigenvalues[0] > 0.0
    assert all(label.startswith("lambda_Gamma_") for label in carrier.spectral_labels)


def test_t16_regional_to_carrier_kernel_preserves_nondiagonal_mode_mixing() -> None:
    realization = make_realization()
    regional = regional_laplace_beltrami_spectrum(
        regional_geometry=domain(realization, "wall"),
        boundary_policy=boundary("wall"),
        scale_factor=1.0,
        scale_units="INVERSE_REFERENCE_LENGTH",
        mode_count=4,
        numerics=realization.numerics,
        provenance="NONDIGONAL_REGIONAL_BASIS",
    )
    carrier = carrier_generalized_spectrum(
        scientific_state=realization.scientific_state,
        mode_count=10,
        numerics=realization.numerics,
        provenance="NONDIGONAL_CARRIER_BASIS",
    )
    kernel = spectral_transfer_kernel(
        regional_spectrum=regional,
        carrier_spectrum=carrier,
        continuum_transfer=ContinuumTransfer(realization.scientific_state.operator),
        numerics=realization.numerics,
        provenance="MODE_MIXING_VALIDATION",
    )
    assert kernel.mode_diagonal_assumed is False
    off_diagonal = kernel.kernel.copy()
    for index in range(min(off_diagonal.shape)):
        off_diagonal[index, index] = 0.0
    assert np.max(np.abs(off_diagonal)) > 1e-6


def test_t17_public_spectral_api_has_no_observational_or_generic_k_field() -> None:
    names = {
        item.name
        for cls in (RegionalSpectrum, CarrierGeneralizedSpectrum)
        for item in fields(cls)
    }
    assert "k" not in names
    assert "k_observational" not in names
    assert "survey_k" not in names
    source = inspect.getsource(regional_laplace_beltrami_spectrum) + inspect.getsource(
        carrier_generalized_spectrum
    )
    assert "observational Fourier" in source
    assert "k_observational" not in source
