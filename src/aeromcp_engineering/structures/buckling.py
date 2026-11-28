"""Euler column buckling calculations (elastic, slender columns, SI units)."""

from __future__ import annotations

import math

from aeromcp_engineering.core.validation import validate_positive


def euler_buckling_load(
    youngs_modulus_pa: float,
    second_moment_of_area_m4: float,
    length_m: float,
    effective_length_factor: float = 1.0,
) -> float:
    """Compute Euler critical buckling load Pcr = pi^2 * E * I / (K * L)^2 in N."""
    e = validate_positive(youngs_modulus_pa, "youngs_modulus_pa")
    i_min = validate_positive(second_moment_of_area_m4, "second_moment_of_area_m4")
    l_col = validate_positive(length_m, "length_m")
    k = validate_positive(effective_length_factor, "effective_length_factor")
    return (math.pi**2) * e * i_min / ((k * l_col) ** 2)
