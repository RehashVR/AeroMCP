"""Failure criteria and thin-walled pressure-vessel stress (SI units)."""

from __future__ import annotations

import math

from aeromcp_engineering.core.validation import validate_finite, validate_positive


def von_mises_stress_2d(
    sigma_x_pa: float,
    sigma_y_pa: float,
    tau_xy_pa: float,
) -> float:
    """Compute 2D plane-stress Von Mises equivalent stress (Pa)."""
    sx = validate_finite(sigma_x_pa, "sigma_x_pa")
    sy = validate_finite(sigma_y_pa, "sigma_y_pa")
    txy = validate_finite(tau_xy_pa, "tau_xy_pa")
    return math.sqrt(sx * sx - sx * sy + sy * sy + 3.0 * txy * txy)


def thin_walled_pressure_vessel(
    internal_pressure_pa: float,
    radius_m: float,
    wall_thickness_m: float,
) -> dict[str, float]:
    """Compute hoop and axial stresses (Pa) in a thin-walled cylinder (t/R <= 0.1)."""
    p = validate_finite(internal_pressure_pa, "internal_pressure_pa")
    r = validate_positive(radius_m, "radius_m")
    t = validate_positive(wall_thickness_m, "wall_thickness_m")
    if t / r > 0.1:
        raise ValueError(
            f"Thin-walled assumption requires t/R <= 0.1. Got t/R = {t / r:.4f}."
        )
    hoop = (p * r) / t
    axial = 0.5 * hoop
    return {
        "hoop_stress_pa": hoop,
        "axial_stress_pa": axial,
        "von_mises_stress_pa": von_mises_stress_2d(hoop, axial, 0.0),
    }
