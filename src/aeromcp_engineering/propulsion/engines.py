"""Ideal analytical airbreathing engine cycle calculations (SI units).

Note: These are 1D ideal Brayton-cycle approximations with caller-supplied
component parameters and are not equivalent to a detailed engine deck.
"""

from __future__ import annotations

import math

from aeromcp_engineering.core.constants import GAMMA_AIR, R_AIR_J_KG_K
from aeromcp_engineering.core.validation import validate_non_negative, validate_positive


def ideal_turbojet_cycle(
    flight_mach: float,
    ambient_temperature_k: float,
    compressor_pressure_ratio: float,
    turbine_inlet_temperature_k: float,
    gamma: float = GAMMA_AIR,
    cp_j_kg_k: float = 1004.5,
) -> dict[str, float]:
    """Compute ideal turbojet specific thrust (N/(kg/s)) and TSFC (kg/(N*s))."""
    m0 = validate_non_negative(flight_mach, "flight_mach")
    t0 = validate_positive(ambient_temperature_k, "ambient_temperature_k")
    pi_c = validate_positive(compressor_pressure_ratio, "compressor_pressure_ratio")
    if pi_c < 1.0:
        raise ValueError(f"compressor_pressure_ratio must be >= 1.0. Got {pi_c!r}.")
    t_t4 = validate_positive(turbine_inlet_temperature_k, "turbine_inlet_temperature_k")
    cp = validate_positive(cp_j_kg_k, "cp_j_kg_k")
    g = validate_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError(f"gamma must be > 1.0. Got {g!r}.")

    a0 = math.sqrt(g * R_AIR_J_KG_K * t0)
    v0 = m0 * a0
    tau_r = 1.0 + 0.5 * (g - 1.0) * m0 * m0
    tau_c = pi_c ** ((g - 1.0) / g)
    tau_lambda = t_t4 / t0
    if tau_lambda <= tau_r * tau_c:
        raise ValueError(
            "turbine_inlet_temperature_k is too low to drive the compressor."
        )
    tau_t = 1.0 - (tau_r / tau_lambda) * (tau_c - 1.0)
    if tau_t <= 0.0:
        raise ValueError("Invalid cycle: turbine temperature ratio <= 0.")

    v9_over_a0_sq = (
        (2.0 / (g - 1.0))
        * (tau_lambda / (tau_r * tau_c))
        * (tau_r * tau_c * tau_t - 1.0)
    )
    if v9_over_a0_sq < 0.0:
        raise ValueError("Invalid cycle: negative nozzle exit velocity squared.")
    v9 = a0 * math.sqrt(v9_over_a0_sq)
    specific_thrust = v9 - v0
    # Fuel-to-air ratio assuming typical hydrocarbon heating value 42.8 MJ/kg
    q_hv = 42.8e6
    f = cp * t0 * (tau_lambda - tau_r * tau_c) / q_hv
    tsfc = f / specific_thrust if specific_thrust > 0.0 else float("inf")
    return {
        "flight_velocity_m_s": v0,
        "exhaust_velocity_m_s": v9,
        "specific_thrust_n_s_kg": specific_thrust,
        "fuel_to_air_ratio": f,
        "tsfc_kg_n_s": tsfc,
    }
