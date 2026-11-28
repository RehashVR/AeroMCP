"""International Standard Atmosphere (ISA) tropospheric calculations.

This module implements the tropospheric layer of the 1976 U.S. Standard
Atmosphere (NASA/TM-2005-213659, Appendix A).

The model is valid for geopotential altitudes:

    0 <= H <= 11000 metres

Assumptions:
- Dry air.
- Hydrostatic equilibrium.
- Ideal gas behaviour.
- Constant gravitational acceleration.
- Constant specific gas constant.
- Constant ratio of specific heats.

IMPORTANT: The input represents geopotential altitude, not geometric
altitude. Geopotential altitude accounts for the variation of gravity
with height, whereas geometric altitude is the actual vertical distance
above mean sea level. Do not pass geometric altitude to this function.

This module implements the tropospheric layer only. It is not a complete
multilayer ISA implementation.
"""

from __future__ import annotations

import math

from aeromcp_engineering.core.validation import validate_non_negative

SEA_LEVEL_TEMPERATURE_K = 288.15
"""Sea level temperature in kelvin (K)."""

SEA_LEVEL_PRESSURE_PA = 101325.0
"""Sea level pressure in pascals (Pa)."""

TEMPERATURE_LAPSE_RATE_K_PER_M = 0.0065
"""Temperature lapse rate in kelvin per metre (K/m)."""

STANDARD_GRAVITY_M_S2 = 9.80665
"""Standard gravity in metres per second squared (m/s^2)."""

SPECIFIC_GAS_CONSTANT_J_PER_KG_K = 287.05287
"""Specific gas constant for dry air in joules per kilogram kelvin (J/(kg*K))."""

SPECIFIC_HEAT_RATIO = 1.4
"""Ratio of specific heats for dry air (dimensionless)."""

MAX_GEOPOTENTIAL_ALTITUDE_M = 11000.0
"""Maximum valid geopotential altitude in metres (m)."""


def isa_troposphere(
    geopotential_altitude_m: float,
) -> dict[str, float]:
    """Compute International Standard Atmosphere properties in the troposphere.

    Calculates temperature, pressure, density, and speed of sound for a
    given geopotential altitude within the tropospheric layer
    (0 <= H <= 11000 m) of the 1976 U.S. Standard Atmosphere.

    Parameters
    ----------
    geopotential_altitude_m:
        Geopotential altitude in metres (m). Must be between 0 and 11000
        inclusive. This is geopotential altitude, not geometric altitude.

    Returns
    -------
    dict[str, float]
        A dictionary with the following keys:

        * ``geopotential_altitude_m`` — input geopotential altitude (m)
        * ``temperature_k`` — temperature (K)
        * ``pressure_pa`` — pressure (Pa)
        * ``density_kg_m3`` — density (kg/m^3)
        * ``speed_of_sound_m_s`` — speed of sound (m/s)

    Raises
    ------
    TypeError
        If the input is not a real number or is a boolean.
    ValueError
        If the input is NaN, infinite, negative, or greater than 11000 m.
    """
    altitude = validate_non_negative(geopotential_altitude_m, "geopotential_altitude_m")
    if altitude > MAX_GEOPOTENTIAL_ALTITUDE_M:
        raise ValueError(
            f"geopotential_altitude_m must not exceed "
            f"{MAX_GEOPOTENTIAL_ALTITUDE_M} m. Got {altitude!r}."
        )

    temperature = SEA_LEVEL_TEMPERATURE_K - TEMPERATURE_LAPSE_RATE_K_PER_M * altitude

    pressure = SEA_LEVEL_PRESSURE_PA * (temperature / SEA_LEVEL_TEMPERATURE_K) ** (
        STANDARD_GRAVITY_M_S2
        / (SPECIFIC_GAS_CONSTANT_J_PER_KG_K * TEMPERATURE_LAPSE_RATE_K_PER_M)
    )

    density = pressure / (SPECIFIC_GAS_CONSTANT_J_PER_KG_K * temperature)

    speed_of_sound = math.sqrt(
        SPECIFIC_HEAT_RATIO * SPECIFIC_GAS_CONSTANT_J_PER_KG_K * temperature
    )

    return {
        "geopotential_altitude_m": altitude,
        "temperature_k": temperature,
        "pressure_pa": pressure,
        "density_kg_m3": density,
        "speed_of_sound_m_s": speed_of_sound,
    }
