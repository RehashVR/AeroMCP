"""Aerodynamics engineering computations for AeroMCP.

This subpackage contains aerospace aerodynamics calculations, including
lift, drag, moment coefficients, airfoil analysis, and wing theory.

The following public functions are available:

* :func:`dynamic_pressure` — compute dynamic pressure from density and velocity.
* :func:`lift_force` — compute lift force from density, velocity, area, and
  lift coefficient.
* :func:`drag_force` — compute drag force from density, velocity, area, and
  drag coefficient.
* :func:`lift_coefficient` — compute dimensionless lift coefficient from lift
  force, density, velocity, and area.
* :func:`reynolds_number` — compute dimensionless Reynolds number from density,
  velocity, characteristic length, and dynamic viscosity.

All functions use SI units and are independent of the Model Context Protocol
(MCP). They can be used directly in any Python program.
"""

from aeromcp.aerodynamics.calculations import (
    drag_force,
    dynamic_pressure,
    lift_coefficient,
    lift_force,
    reynolds_number,
)

__all__ = [
    "drag_force",
    "dynamic_pressure",
    "lift_coefficient",
    "lift_force",
    "reynolds_number",
]
