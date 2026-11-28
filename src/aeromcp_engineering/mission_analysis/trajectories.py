"""Simplified 1D vertical rocket ascent trajectory using RK4 (SI units).

Note: This is a 1-DOF vertical ascent model with constant gravity g0 and
optional constant-area quadratic drag; it is not a full 6-DOF launch simulator.
"""

from __future__ import annotations

from aeromcp_engineering.core.constants import G0_M_S2
from aeromcp_engineering.core.numerical_methods import rk4_integrate
from aeromcp_engineering.core.validation import validate_non_negative, validate_positive


def vertical_rocket_ascent_rk4(
    initial_mass_kg: float,
    propellant_mass_kg: float,
    thrust_n: float,
    mass_flow_kg_s: float,
    burn_time_s: float,
    time_step_s: float = 0.1,
    drag_area_cd_s_m2: float = 0.0,
    air_density_kg_m3: float = 0.0,
) -> dict[str, float]:
    """Integrate 1D vertical rocket ascent during burn using fixed-step RK4."""
    m0 = validate_positive(initial_mass_kg, "initial_mass_kg")
    mp = validate_positive(propellant_mass_kg, "propellant_mass_kg")
    if mp >= m0:
        raise ValueError("propellant_mass_kg must be < initial_mass_kg.")
    thrust = validate_positive(thrust_n, "thrust_n")
    m_dot = validate_positive(mass_flow_kg_s, "mass_flow_kg_s")
    t_burn = validate_positive(burn_time_s, "burn_time_s")
    dt = validate_positive(time_step_s, "time_step_s")
    cd_s = validate_non_negative(drag_area_cd_s_m2, "drag_area_cd_s_m2")
    rho = validate_non_negative(air_density_kg_m3, "air_density_kg_m3")

    if m_dot * t_burn > mp + 1e-9:
        raise ValueError("mass_flow_kg_s * burn_time_s exceeds propellant_mass_kg.")

    def derivs(_t: float, state: list[float]) -> list[float]:
        _h, v, m = state
        drag = 0.5 * rho * v * abs(v) * cd_s
        accel = (thrust - drag) / m - G0_M_S2
        return [v, accel, -m_dot]

    times, states = rk4_integrate(derivs, 0.0, [0.0, 0.0, m0], t_burn, dt)
    h_end, v_end, m_end = states[-1]
    return {
        "burnout_time_s": times[-1],
        "burnout_altitude_m": h_end,
        "burnout_velocity_m_s": v_end,
        "burnout_mass_kg": m_end,
    }
