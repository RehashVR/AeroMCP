"""Orbital element <-> Cartesian ECI state transformations and energy/momentum."""

from __future__ import annotations

import math

from aeromcp_engineering.core.constants import MU_EARTH_M3_S2
from aeromcp_engineering.core.validation import (
    validate_finite,
    validate_non_negative,
    validate_positive,
)


def vis_viva_velocity(
    radius_m: float,
    semi_major_axis_m: float,
    gravitational_parameter_m3_s2: float = MU_EARTH_M3_S2,
) -> float:
    """Compute orbital speed from the vis-viva equation v = sqrt(mu*(2/r - 1/a))."""
    r = validate_positive(radius_m, "radius_m")
    a = validate_finite(semi_major_axis_m, "semi_major_axis_m")
    mu = validate_positive(
        gravitational_parameter_m3_s2, "gravitational_parameter_m3_s2"
    )
    if a == 0.0:
        raise ValueError("semi_major_axis_m cannot be zero.")
    v_sq = mu * (2.0 / r - 1.0 / a)
    if v_sq < 0.0:
        raise ValueError("Vis-viva equation yielded negative velocity squared.")
    return math.sqrt(v_sq)


def hyperbolic_excess_velocity(
    c3_m2_s2: float,
) -> float:
    """Compute hyperbolic excess speed v_inf = sqrt(C3) in m/s for C3 >= 0."""
    c3 = validate_non_negative(c3_m2_s2, "c3_m2_s2")
    return math.sqrt(c3)


def c3_energy(v_inf_m_s: float) -> float:
    """Compute characteristic energy C3 = v_inf^2 in m^2/s^2."""
    v_inf = validate_non_negative(v_inf_m_s, "v_inf_m_s")
    return v_inf * v_inf


def periapsis_apoapsis(
    semi_major_axis_m: float, eccentricity: float
) -> dict[str, float]:
    """Compute periapsis and apoapsis radii (m) for an elliptic orbit."""
    a = validate_positive(semi_major_axis_m, "semi_major_axis_m")
    e = validate_non_negative(eccentricity, "eccentricity")
    if e >= 1.0:
        raise ValueError(f"Elliptic orbit requires 0 <= e < 1.0. Got {e!r}.")
    return {
        "periapsis_radius_m": a * (1.0 - e),
        "apoapsis_radius_m": a * (1.0 + e),
    }


def coe_to_rv(
    semi_major_axis_m: float,
    eccentricity: float,
    inclination_rad: float,
    raan_rad: float,
    arg_periapsis_rad: float,
    true_anomaly_rad: float,
    gravitational_parameter_m3_s2: float = MU_EARTH_M3_S2,
) -> dict[str, list[float]]:
    """Convert classical orbital elements (ECI, radians) to position and velocity."""
    a = validate_positive(semi_major_axis_m, "semi_major_axis_m")
    e = validate_non_negative(eccentricity, "eccentricity")
    if e >= 1.0:
        raise ValueError(f"Elliptic orbit requires 0 <= e < 1.0. Got {e!r}.")
    inc = validate_finite(inclination_rad, "inclination_rad")
    raan = validate_finite(raan_rad, "raan_rad")
    argp = validate_finite(arg_periapsis_rad, "arg_periapsis_rad")
    nu = validate_finite(true_anomaly_rad, "true_anomaly_rad")
    mu = validate_positive(
        gravitational_parameter_m3_s2, "gravitational_parameter_m3_s2"
    )

    p = a * (1.0 - e * e)
    r_mag = p / (1.0 + e * math.cos(nu))
    r_pqw = [r_mag * math.cos(nu), r_mag * math.sin(nu), 0.0]
    v_factor = math.sqrt(mu / p)
    v_pqw = [-v_factor * math.sin(nu), v_factor * (e + math.cos(nu)), 0.0]

    co, so = math.cos(raan), math.sin(raan)
    cw, sw = math.cos(argp), math.sin(argp)
    ci, si = math.cos(inc), math.sin(inc)

    rot = [
        [co * cw - so * sw * ci, -co * sw - so * cw * ci, so * si],
        [so * cw + co * sw * ci, -so * sw + co * cw * ci, -co * si],
        [sw * si, cw * si, ci],
    ]

    r_eci = [sum(rot[i][j] * r_pqw[j] for j in range(3)) for i in range(3)]
    v_eci = [sum(rot[i][j] * v_pqw[j] for j in range(3)) for i in range(3)]
    return {"position_m": r_eci, "velocity_m_s": v_eci}
