"""Flight mechanics and aircraft stability calculations for AeroMCP."""

from __future__ import annotations

from aeromcp_engineering.flight_mechanics.performance import (
    climb_performance,
    coordinated_turn_performance,
    glide_performance,
    jet_breguet_range,
    propeller_breguet_endurance,
    takeoff_ground_roll,
)
from aeromcp_engineering.flight_mechanics.stability import (
    neutral_point_position,
    static_margin,
)

__all__ = [
    "climb_performance",
    "coordinated_turn_performance",
    "glide_performance",
    "jet_breguet_range",
    "neutral_point_position",
    "propeller_breguet_endurance",
    "static_margin",
    "takeoff_ground_roll",
]
