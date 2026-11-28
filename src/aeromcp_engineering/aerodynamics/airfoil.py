"""Thin-airfoil theoretical approximations (SI / radians).

Note: Thin-airfoil theory assumes inviscid, incompressible, 2D potential flow
at small angles of attack and does not account for viscous separation, stall,
or compressibility. It is not a substitute for experimental or CFD airfoil polars.
"""

from __future__ import annotations

import math

from aeromcp_engineering.core.validation import validate_finite


def thin_airfoil_lift_coefficient(
    angle_of_attack_rad: float,
    zero_lift_angle_rad: float = 0.0,
) -> float:
    """Compute theoretical 2D thin-airfoil lift coefficient cl = 2*pi*(alpha - alpha_0)."""
    alpha = validate_finite(angle_of_attack_rad, "angle_of_attack_rad")
    alpha_0 = validate_finite(zero_lift_angle_rad, "zero_lift_angle_rad")
    return 2.0 * math.pi * (alpha - alpha_0)
