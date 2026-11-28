"""Aerodynamic heating preliminary estimates (stagnation/recovery temperature, Sutton-Graves)."""

from __future__ import annotations

import math

from aeromcp_engineering.core.constants import GAMMA_AIR
from aeromcp_engineering.core.validation import validate_non_negative, validate_positive


def stagnation_and_recovery_temperature(
    static_temperature_k: float,
    mach: float,
    recovery_factor: float = 0.85,
    gamma: float = GAMMA_AIR,
) -> dict[str, float]:
    """Compute stagnation T0 (K) and adiabatic wall recovery temperature Tr (K)."""
    t_inf = validate_positive(static_temperature_k, "static_temperature_k")
    m = validate_non_negative(mach, "mach")
    r_f = validate_non_negative(recovery_factor, "recovery_factor")
    if r_f > 1.0:
        raise ValueError(f"recovery_factor must be <= 1.0. Got {r_f!r}.")
    g = validate_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError(f"gamma must be > 1.0. Got {g!r}.")
    term = 0.5 * (g - 1.0) * m * m
    t0 = t_inf * (1.0 + term)
    t_r = t_inf * (1.0 + r_f * term)
    return {
        "stagnation_temperature_k": t0,
        "recovery_temperature_k": t_r,
    }


def sutton_graves_stagnation_heat_flux(
    density_kg_m3: float,
    velocity_m_s: float,
    nose_radius_m: float,
    sutton_graves_constant: float = 1.7415e-4,
) -> float:
    """Estimate convective stagnation-point heat flux (W/m^2) via Sutton-Graves correlation.

    Default constant 1.7415e-4 W/(m^2 * (kg/m^3)^0.5 * (m/s)^3 * m^-0.5) is for Earth air.
    """
    rho = validate_positive(density_kg_m3, "density_kg_m3")
    v = validate_non_negative(velocity_m_s, "velocity_m_s")
    rn = validate_positive(nose_radius_m, "nose_radius_m")
    k_sg = validate_positive(sutton_graves_constant, "sutton_graves_constant")
    return k_sg * math.sqrt(rho / rn) * (v**3)
