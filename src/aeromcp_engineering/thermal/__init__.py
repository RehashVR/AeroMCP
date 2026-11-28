"""Aerospace thermal engineering calculations for AeroMCP."""

from __future__ import annotations

from aeromcp_engineering.thermal.aerospace_heating import (
    stagnation_and_recovery_temperature,
    sutton_graves_stagnation_heat_flux,
)
from aeromcp_engineering.thermal.conduction import (
    conduction_1d_heat_rate,
    series_thermal_resistance_heat_rate,
)
from aeromcp_engineering.thermal.convection import convection_heat_rate
from aeromcp_engineering.thermal.radiation import radiation_heat_rate

__all__ = [
    "conduction_1d_heat_rate",
    "convection_heat_rate",
    "radiation_heat_rate",
    "series_thermal_resistance_heat_rate",
    "stagnation_and_recovery_temperature",
    "sutton_graves_stagnation_heat_flux",
]
