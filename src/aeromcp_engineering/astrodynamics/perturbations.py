"""J2 secular orbital perturbation rates (Vallado conventions, SI/rad/s)."""

from __future__ import annotations

import math

from aeromcp_engineering.core.constants import (
    J2_EARTH,
    MU_EARTH_M3_S2,
    R_EARTH_EQUATORIAL_M,
)
from aeromcp_engineering.core.validation import (
    validate_finite,
    validate_non_negative,
    validate_positive,
)


def j2_secular_rates(
    semi_major_axis_m: float,
    eccentricity: float,
    inclination_rad: float,
    gravitational_parameter_m3_s2: float = MU_EARTH_M3_S2,
    body_radius_m: float = R_EARTH_EQUATORIAL_M,
    j2: float = J2_EARTH,
) -> dict[str, float]:
    """Compute secular rates of RAAN and argument of periapsis due to J2 (rad/s)."""
    a = validate_positive(semi_major_axis_m, "semi_major_axis_m")
    e = validate_non_negative(eccentricity, "eccentricity")
    if e >= 1.0:
        raise ValueError(f"Elliptic orbit requires 0 <= e < 1.0. Got {e!r}.")
    inc = validate_finite(inclination_rad, "inclination_rad")
    mu = validate_positive(
        gravitational_parameter_m3_s2, "gravitational_parameter_m3_s2"
    )
    re = validate_positive(body_radius_m, "body_radius_m")
    j2_val = validate_finite(j2, "j2")

    p = a * (1.0 - e * e)
    n = math.sqrt(mu / (a**3))
    factor = -1.5 * n * j2_val * ((re / p) ** 2)
    raan_dot = factor * math.cos(inc)
    argp_dot = 0.75 * n * j2_val * ((re / p) ** 2) * (4.0 - 5.0 * (math.sin(inc) ** 2))
    return {
        "raan_rate_rad_s": raan_dot,
        "arg_periapsis_rate_rad_s": argp_dot,
        "mean_motion_rad_s": n,
    }
