"""Two-body orbital propagation using fixed-step RK4 integration (ECI, SI)."""

from __future__ import annotations

import math

from aeromcp_engineering.core.constants import MU_EARTH_M3_S2
from aeromcp_engineering.core.numerical_methods import rk4_integrate
from aeromcp_engineering.core.validation import validate_finite, validate_positive


def propagate_two_body_rk4(
    position_m: list[float],
    velocity_m_s: list[float],
    duration_s: float,
    time_step_s: float = 10.0,
    gravitational_parameter_m3_s2: float = MU_EARTH_M3_S2,
) -> dict[str, object]:
    """Propagate a two-body Cartesian state [x, y, z, vx, vy, vz] using RK4."""
    if len(position_m) != 3 or len(velocity_m_s) != 3:
        raise ValueError("position_m and velocity_m_s must each have length 3.")
    r0 = [validate_finite(x, "position_m") for x in position_m]
    v0 = [validate_finite(v, "velocity_m_s") for v in velocity_m_s]
    dur = validate_positive(duration_s, "duration_s")
    dt = validate_positive(time_step_s, "time_step_s")
    mu = validate_positive(
        gravitational_parameter_m3_s2, "gravitational_parameter_m3_s2"
    )

    def derivs(_t: float, state: list[float]) -> list[float]:
        x, y, z, vx, vy, vz = state
        r_sq = x * x + y * y + z * z
        if r_sq <= 0.0:
            raise ValueError("Position vector norm became zero during propagation.")
        r3 = r_sq * math.sqrt(r_sq)
        factor = -mu / r3
        return [vx, vy, vz, factor * x, factor * y, factor * z]

    y0 = r0 + v0
    times, states = rk4_integrate(derivs, 0.0, y0, dur, dt)
    final_state = states[-1]
    return {
        "final_time_s": times[-1],
        "final_position_m": final_state[:3],
        "final_velocity_m_s": final_state[3:],
        "steps": len(times) - 1,
    }
