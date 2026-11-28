"""Aircraft and UAV preliminary design calculations for AeroMCP."""

from __future__ import annotations

from aeromcp_engineering.aircraft_design.preliminary_design import (
    electric_uav_endurance,
    power_to_weight_ratio,
    thrust_to_weight_ratio,
)
from aeromcp_engineering.aircraft_design.wing_sizing import (
    rectangular_wing_mac,
    wing_area_from_loading,
    wingspan_from_aspect_ratio,
)

__all__ = [
    "electric_uav_endurance",
    "power_to_weight_ratio",
    "rectangular_wing_mac",
    "thrust_to_weight_ratio",
    "wing_area_from_loading",
    "wingspan_from_aspect_ratio",
]
