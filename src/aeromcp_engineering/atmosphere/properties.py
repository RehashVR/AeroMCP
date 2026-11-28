"""U.S. Standard Atmosphere 1976 layered model (0 to 84,852 m geopotential)."""

from __future__ import annotations

import math

from aeromcp_engineering.atmosphere.viscosity import (
    kinematic_viscosity,
    sutherland_viscosity,
)
from aeromcp_engineering.core.constants import (
    G0_M_S2,
    GAMMA_AIR,
    P0_PA,
    R_AIR_J_KG_K,
    R_EARTH_MEAN_M,
    T0_K,
)
from aeromcp_engineering.core.validation import validate_non_negative, validate_positive

# U.S. Standard Atmosphere 1976 geopotential layers: (h_base_m, T_base_K, lapse_K_m)
_ISA_LAYERS: tuple[tuple[float, float, float], ...] = (
    (0.0, 288.15, -0.0065),
    (11_000.0, 216.65, 0.0),
    (20_000.0, 216.65, 0.0010),
    (32_000.0, 228.65, 0.0028),
    (47_000.0, 270.65, 0.0),
    (51_000.0, 270.65, -0.0028),
    (71_000.0, 214.65, -0.0020),
)
_MAX_GEOPOTENTIAL_ALTITUDE_M: float = 84_852.0


def geometric_to_geopotential(geometric_altitude_m: float) -> float:
    """Convert geometric altitude (m) to geopotential altitude (m)."""
    z = validate_non_negative(geometric_altitude_m, "geometric_altitude_m")
    return (R_EARTH_MEAN_M * z) / (R_EARTH_MEAN_M + z)


def speed_of_sound(
    temperature_k: float,
    gamma: float = GAMMA_AIR,
    gas_constant_j_kg_k: float = R_AIR_J_KG_K,
) -> float:
    """Compute speed of sound a = sqrt(gamma * R * T) in m/s."""
    t = validate_positive(temperature_k, "temperature_k")
    g = validate_positive(gamma, "gamma")
    r = validate_positive(gas_constant_j_kg_k, "gas_constant_j_kg_k")
    return math.sqrt(g * r * t)


def isa_atmosphere(altitude_m: float) -> dict[str, float]:
    """Compute U.S. Standard Atmosphere 1976 properties at geometric altitude_m.

    Valid for 0 <= geopotential_altitude <= 84,852 m (~86,000 m geometric).
    """
    z = validate_non_negative(altitude_m, "altitude_m")
    h = geometric_to_geopotential(z)
    if h > _MAX_GEOPOTENTIAL_ALTITUDE_M:
        raise ValueError(
            f"Geopotential altitude {h:.2f} m exceeds ISA 1976 limit "
            f"({_MAX_GEOPOTENTIAL_ALTITUDE_M} m)."
        )

    p_base = P0_PA
    t_out = T0_K
    p_out = P0_PA

    for idx, (h_base, t_base, lapse) in enumerate(_ISA_LAYERS):
        h_top = (
            _ISA_LAYERS[idx + 1][0]
            if idx + 1 < len(_ISA_LAYERS)
            else _MAX_GEOPOTENTIAL_ALTITUDE_M
        )
        if h <= h_top or idx == len(_ISA_LAYERS) - 1:
            dh = h - h_base
            if lapse == 0.0:
                t_out = t_base
                p_out = p_base * math.exp(-G0_M_S2 * dh / (R_AIR_J_KG_K * t_base))
            else:
                t_out = t_base + lapse * dh
                exponent = -G0_M_S2 / (R_AIR_J_KG_K * lapse)
                p_out = p_base * ((t_out / t_base) ** exponent)
            break
        # Advance p_base to top of current layer
        dh_layer = h_top - h_base
        if lapse == 0.0:
            p_base = p_base * math.exp(-G0_M_S2 * dh_layer / (R_AIR_J_KG_K * t_base))
        else:
            t_top = t_base + lapse * dh_layer
            exponent = -G0_M_S2 / (R_AIR_J_KG_K * lapse)
            p_base = p_base * ((t_top / t_base) ** exponent)

    rho = p_out / (R_AIR_J_KG_K * t_out)
    a = speed_of_sound(t_out)
    mu = sutherland_viscosity(t_out)
    nu = kinematic_viscosity(mu, rho)
    return {
        "geometric_altitude_m": z,
        "geopotential_altitude_m": h,
        "temperature_k": t_out,
        "pressure_pa": p_out,
        "density_kg_m3": rho,
        "speed_of_sound_m_s": a,
        "dynamic_viscosity_pa_s": mu,
        "kinematic_viscosity_m2_s": nu,
    }


def mach_atmospheric_properties(
    altitude_m: float, velocity_m_s: float
) -> dict[str, float]:
    """Compute atmospheric properties plus Mach number and dynamic pressure."""
    v = validate_non_negative(velocity_m_s, "velocity_m_s")
    atm = isa_atmosphere(altitude_m)
    mach = v / atm["speed_of_sound_m_s"]
    q = 0.5 * atm["density_kg_m3"] * v * v
    return {
        **atm,
        "velocity_m_s": v,
        "mach_number": mach,
        "dynamic_pressure_pa": q,
    }


def density_altitude(density_kg_m3: float) -> float:
    """Compute ISA troposphere density altitude (m) for a given air density.

    Valid within the ISA troposphere (0 <= h <= 11,000 m, rho in [0.3639, 1.225] kg/m^3).
    """
    rho = validate_positive(density_kg_m3, "density_kg_m3")
    lapse = -0.0065
    exponent = -(G0_M_S2 / (R_AIR_J_KG_K * lapse)) - 1.0
    rho0 = P0_PA / (R_AIR_J_KG_K * T0_K)
    t_ratio = (rho / rho0) ** (1.0 / exponent)
    h = (T0_K / lapse) * (t_ratio - 1.0)
    if h < -1000.0 or h > 11_000.0:
        raise ValueError(
            f"Density {rho} kg/m^3 corresponds to {h:.1f} m, outside troposphere model."
        )
    return h
