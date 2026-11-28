"""Finite-wing and aircraft aerodynamics calculations (SI units)."""

from __future__ import annotations

import math

from aeromcp_engineering.aerodynamics.calculations import dynamic_pressure
from aeromcp_engineering.core.validation import (
    validate_finite,
    validate_non_negative,
    validate_positive,
)


def mach_number(velocity_m_s: float, speed_of_sound_m_s: float) -> float:
    """Compute Mach number M = V / a."""
    v = validate_non_negative(velocity_m_s, "velocity_m_s")
    a = validate_positive(speed_of_sound_m_s, "speed_of_sound_m_s")
    return v / a


def lift_to_drag_ratio(lift_n: float, drag_n: float) -> float:
    """Compute lift-to-drag ratio L / D."""
    lift = validate_finite(lift_n, "lift_n")
    drag = validate_positive(drag_n, "drag_n")
    return lift / drag


def wing_loading(weight_n: float, wing_area_m2: float) -> float:
    """Compute wing loading W / S in N/m^2 (Pa)."""
    w = validate_positive(weight_n, "weight_n")
    s = validate_positive(wing_area_m2, "wing_area_m2")
    return w / s


def aspect_ratio(wingspan_m: float, wing_area_m2: float) -> float:
    """Compute wing aspect ratio AR = b^2 / S."""
    b = validate_positive(wingspan_m, "wingspan_m")
    s = validate_positive(wing_area_m2, "wing_area_m2")
    return (b * b) / s


def induced_drag_coefficient(
    lift_coefficient: float,
    aspect_ratio_val: float,
    oswald_efficiency: float,
) -> float:
    """Compute induced drag coefficient CDi = CL^2 / (pi * AR * e)."""
    cl = validate_finite(lift_coefficient, "lift_coefficient")
    ar = validate_positive(aspect_ratio_val, "aspect_ratio_val")
    e = validate_positive(oswald_efficiency, "oswald_efficiency")
    if e > 1.0:
        raise ValueError(f"oswald_efficiency must be <= 1.0. Got {e!r}.")
    return (cl * cl) / (math.pi * ar * e)


def induced_drag_force(
    density_kg_m3: float,
    velocity_m_s: float,
    wing_area_m2: float,
    lift_coefficient: float,
    aspect_ratio_val: float,
    oswald_efficiency: float,
) -> float:
    """Compute induced drag force Di = q * S * CDi in newtons (N)."""
    q = dynamic_pressure(density_kg_m3, velocity_m_s)
    s = validate_positive(wing_area_m2, "wing_area_m2")
    cdi = induced_drag_coefficient(
        lift_coefficient, aspect_ratio_val, oswald_efficiency
    )
    return q * s * cdi


def stall_speed(
    weight_n: float,
    density_kg_m3: float,
    wing_area_m2: float,
    cl_max: float,
) -> float:
    """Compute steady level-flight stall speed Vs = sqrt(2*W / (rho*S*CLmax)) in m/s."""
    w = validate_positive(weight_n, "weight_n")
    rho = validate_positive(density_kg_m3, "density_kg_m3")
    s = validate_positive(wing_area_m2, "wing_area_m2")
    clm = validate_positive(cl_max, "cl_max")
    return math.sqrt((2.0 * w) / (rho * s * clm))


def finite_wing_lift_slope(
    airfoil_lift_slope_per_rad: float,
    aspect_ratio_val: float,
    oswald_efficiency: float = 1.0,
) -> float:
    """Compute Prandtl lifting-line finite-wing lift-curve slope (per rad).

    a = a0 / (1 + a0 / (pi * AR * e))
    """
    a0 = validate_positive(airfoil_lift_slope_per_rad, "airfoil_lift_slope_per_rad")
    ar = validate_positive(aspect_ratio_val, "aspect_ratio_val")
    e = validate_positive(oswald_efficiency, "oswald_efficiency")
    if e > 1.0:
        raise ValueError(f"oswald_efficiency must be <= 1.0. Got {e!r}.")
    return a0 / (1.0 + a0 / (math.pi * ar * e))


def aerodynamic_force_decomposition(
    normal_force_n: float,
    axial_force_n: float,
    angle_of_attack_rad: float,
) -> dict[str, float]:
    """Decompose body-frame normal (N) and axial (A) forces into Lift and Drag.

    L = N * cos(alpha) - A * sin(alpha)
    D = N * sin(alpha) + A * cos(alpha)
    """
    n_f = validate_finite(normal_force_n, "normal_force_n")
    a_f = validate_finite(axial_force_n, "axial_force_n")
    alpha = validate_finite(angle_of_attack_rad, "angle_of_attack_rad")
    ca = math.cos(alpha)
    sa = math.sin(alpha)
    return {
        "lift_n": n_f * ca - a_f * sa,
        "drag_n": n_f * sa + a_f * ca,
    }
