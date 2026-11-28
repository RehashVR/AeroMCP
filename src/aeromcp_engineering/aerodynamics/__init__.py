"""Aerodynamics engineering calculations for AeroMCP."""

from __future__ import annotations

from aeromcp_engineering.aerodynamics.airfoil import thin_airfoil_lift_coefficient
from aeromcp_engineering.aerodynamics.calculations import (
    drag_force,
    dynamic_pressure,
    lift_coefficient,
    lift_force,
    reynolds_number,
)
from aeromcp_engineering.aerodynamics.wings import (
    aerodynamic_force_decomposition,
    aspect_ratio,
    finite_wing_lift_slope,
    induced_drag_coefficient,
    induced_drag_force,
    lift_to_drag_ratio,
    mach_number,
    stall_speed,
    wing_loading,
)

__all__ = [
    "aerodynamic_force_decomposition",
    "aspect_ratio",
    "drag_force",
    "dynamic_pressure",
    "finite_wing_lift_slope",
    "induced_drag_coefficient",
    "induced_drag_force",
    "lift_coefficient",
    "lift_force",
    "lift_to_drag_ratio",
    "mach_number",
    "reynolds_number",
    "stall_speed",
    "thin_airfoil_lift_coefficient",
    "wing_loading",
]
