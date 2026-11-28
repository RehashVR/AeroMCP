"""Analytical axial bar mechanics (linear-elastic, small-strain, SI units)."""

from __future__ import annotations

from aeromcp_engineering.core.validation import validate_finite, validate_positive


def axial_bar_analysis(
    force_n: float,
    area_m2: float,
    length_m: float,
    youngs_modulus_pa: float,
) -> dict[str, float]:
    """Compute axial stress (Pa), strain (-), and elongation (m)."""
    f = validate_finite(force_n, "force_n")
    a = validate_positive(area_m2, "area_m2")
    l_bar = validate_positive(length_m, "length_m")
    e = validate_positive(youngs_modulus_pa, "youngs_modulus_pa")
    stress = f / a
    strain = stress / e
    elongation = strain * l_bar
    return {
        "axial_stress_pa": stress,
        "axial_strain": strain,
        "elongation_m": elongation,
    }
