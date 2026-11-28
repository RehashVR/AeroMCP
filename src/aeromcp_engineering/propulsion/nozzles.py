"""Isentropic and specified-efficiency rocket/gas nozzle calculations."""

from __future__ import annotations

import math

from aeromcp_engineering.compressible_flow.area_mach import solve_mach_from_area_ratio
from aeromcp_engineering.compressible_flow.isentropic import isentropic_ratios
from aeromcp_engineering.core.constants import GAMMA_AIR
from aeromcp_engineering.core.validation import validate_non_negative, validate_positive


def critical_pressure_ratio(gamma: float = GAMMA_AIR) -> float:
    """Compute critical pressure ratio p*/p0 = (2/(gamma+1))^(gamma/(gamma-1))."""
    g = validate_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError(f"gamma must be > 1.0. Got {g!r}.")
    return (2.0 / (g + 1.0)) ** (g / (g - 1.0))


def choked_mass_flow(
    chamber_pressure_pa: float,
    chamber_temperature_k: float,
    throat_area_m2: float,
    gamma: float = GAMMA_AIR,
    gas_constant_j_kg_k: float = 287.05287,
) -> float:
    """Compute choked nozzle mass flow rate (kg/s) at sonic throat."""
    pc = validate_positive(chamber_pressure_pa, "chamber_pressure_pa")
    tc = validate_positive(chamber_temperature_k, "chamber_temperature_k")
    at = validate_positive(throat_area_m2, "throat_area_m2")
    g = validate_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError(f"gamma must be > 1.0. Got {g!r}.")
    r = validate_positive(gas_constant_j_kg_k, "gas_constant_j_kg_k")
    factor = (2.0 / (g + 1.0)) ** ((g + 1.0) / (2.0 * (g - 1.0)))
    return pc * at * math.sqrt(g / (r * tc)) * factor


def converging_diverging_nozzle(
    chamber_pressure_pa: float,
    chamber_temperature_k: float,
    throat_area_m2: float,
    exit_area_m2: float,
    ambient_pressure_pa: float = 0.0,
    gamma: float = GAMMA_AIR,
    gas_constant_j_kg_k: float = 287.05287,
    nozzle_efficiency: float = 1.0,
) -> dict[str, float]:
    """Compute supersonic converging-diverging nozzle performance."""
    pc = validate_positive(chamber_pressure_pa, "chamber_pressure_pa")
    tc = validate_positive(chamber_temperature_k, "chamber_temperature_k")
    at = validate_positive(throat_area_m2, "throat_area_m2")
    ae = validate_positive(exit_area_m2, "exit_area_m2")
    pa = validate_non_negative(ambient_pressure_pa, "ambient_pressure_pa")
    eta = validate_positive(nozzle_efficiency, "nozzle_efficiency")
    if eta > 1.0:
        raise ValueError(f"nozzle_efficiency must be <= 1.0. Got {eta!r}.")
    if ae < at:
        raise ValueError(f"exit_area_m2 ({ae}) must be >= throat_area_m2 ({at}).")

    eps = ae / at
    me = solve_mach_from_area_ratio(eps, branch="supersonic", gamma=gamma)
    ratios = isentropic_ratios(me, gamma)
    pe = pc / ratios["p0_over_p"]
    te = tc / ratios["t0_over_t"]
    ve_ideal = me * math.sqrt(gamma * gas_constant_j_kg_k * te)
    ve = ve_ideal * math.sqrt(eta)
    m_dot = choked_mass_flow(pc, tc, at, gamma, gas_constant_j_kg_k)
    thrust = m_dot * ve + (pe - pa) * ae
    return {
        "expansion_ratio": eps,
        "exit_mach": me,
        "exit_pressure_pa": pe,
        "exit_temperature_k": te,
        "exit_velocity_m_s": ve,
        "mass_flow_kg_s": m_dot,
        "thrust_n": thrust,
    }
