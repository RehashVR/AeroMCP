"""Circular shaft torsion mechanics (linear-elastic, SI units)."""

from __future__ import annotations

from aeromcp_engineering.core.validation import validate_finite, validate_positive


def circular_shaft_torsion(
    torque_n_m: float,
    outer_radius_m: float,
    polar_moment_of_inertia_m4: float,
    length_m: float,
    shear_modulus_pa: float,
) -> dict[str, float]:
    """Compute maximum shear stress (Pa) and angle of twist (rad)."""
    t = validate_finite(torque_n_m, "torque_n_m")
    r = validate_positive(outer_radius_m, "outer_radius_m")
    j = validate_positive(polar_moment_of_inertia_m4, "polar_moment_of_inertia_m4")
    l_shaft = validate_positive(length_m, "length_m")
    g = validate_positive(shear_modulus_pa, "shear_modulus_pa")
    tau_max = (t * r) / j
    theta = (t * l_shaft) / (g * j)
    return {
        "max_shear_stress_pa": tau_max,
        "angle_of_twist_rad": theta,
    }
