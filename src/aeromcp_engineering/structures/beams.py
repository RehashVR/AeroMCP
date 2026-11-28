"""Euler-Bernoulli analytical beam bending and deflection (SI units)."""

from __future__ import annotations

from aeromcp_engineering.core.validation import validate_finite, validate_positive


def beam_bending_stress(
    bending_moment_n_m: float,
    distance_from_neutral_axis_m: float,
    second_moment_of_area_m4: float,
) -> float:
    """Compute Euler-Bernoulli bending stress sigma = M * y / I in Pa."""
    m = validate_finite(bending_moment_n_m, "bending_moment_n_m")
    y = validate_finite(distance_from_neutral_axis_m, "distance_from_neutral_axis_m")
    i_xx = validate_positive(second_moment_of_area_m4, "second_moment_of_area_m4")
    return (m * y) / i_xx


def cantilever_tip_deflection(
    tip_load_n: float,
    length_m: float,
    youngs_modulus_pa: float,
    second_moment_of_area_m4: float,
) -> float:
    """Compute tip deflection delta = P*L^3 / (3*E*I) for a cantilever beam (m)."""
    p = validate_finite(tip_load_n, "tip_load_n")
    l_beam = validate_positive(length_m, "length_m")
    e = validate_positive(youngs_modulus_pa, "youngs_modulus_pa")
    i_xx = validate_positive(second_moment_of_area_m4, "second_moment_of_area_m4")
    return (p * (l_beam**3)) / (3.0 * e * i_xx)


def simply_supported_center_deflection(
    center_load_n: float,
    length_m: float,
    youngs_modulus_pa: float,
    second_moment_of_area_m4: float,
) -> float:
    """Compute mid-span deflection delta = P*L^3 / (48*E*I) for a simply supported beam (m)."""
    p = validate_finite(center_load_n, "center_load_n")
    l_beam = validate_positive(length_m, "length_m")
    e = validate_positive(youngs_modulus_pa, "youngs_modulus_pa")
    i_xx = validate_positive(second_moment_of_area_m4, "second_moment_of_area_m4")
    return (p * (l_beam**3)) / (48.0 * e * i_xx)
