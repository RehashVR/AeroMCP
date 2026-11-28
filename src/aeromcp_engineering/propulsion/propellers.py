"""Actuator-disk propeller momentum theory calculations (SI units)."""

from __future__ import annotations

import math

from aeromcp_engineering.core.validation import validate_non_negative, validate_positive


def actuator_disk_propeller(
    thrust_n: float,
    disk_area_m2: float,
    density_kg_m3: float,
    freestream_velocity_m_s: float = 0.0,
    propulsive_efficiency_factor: float = 1.0,
) -> dict[str, float]:
    """Compute ideal actuator-disk induced velocity, shaft power, and efficiency."""
    t = validate_positive(thrust_n, "thrust_n")
    area = validate_positive(disk_area_m2, "disk_area_m2")
    rho = validate_positive(density_kg_m3, "density_kg_m3")
    v0 = validate_non_negative(freestream_velocity_m_s, "freestream_velocity_m_s")
    eta_f = validate_positive(
        propulsive_efficiency_factor, "propulsive_efficiency_factor"
    )
    if eta_f > 1.0:
        raise ValueError(f"propulsive_efficiency_factor must be <= 1.0. Got {eta_f!r}.")

    vi_static = math.sqrt(t / (2.0 * rho * area))
    # Momentum theory: vi^2 + v0*vi - T/(2*rho*A) = 0
    vi = 0.5 * (-v0 + math.sqrt(v0 * v0 + 4.0 * vi_static * vi_static))
    p_ideal = t * (v0 + vi)
    p_shaft = p_ideal / eta_f
    eta_ideal = v0 / (v0 + vi) if (v0 + vi) > 0.0 else 0.0
    return {
        "static_induced_velocity_m_s": vi_static,
        "induced_velocity_m_s": vi,
        "ideal_power_w": p_ideal,
        "shaft_power_w": p_shaft,
        "ideal_propulsive_efficiency": eta_ideal,
        "disk_loading_n_m2": t / area,
    }
