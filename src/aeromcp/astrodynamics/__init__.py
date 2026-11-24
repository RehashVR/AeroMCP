"""Astrodynamics engineering computations for AeroMCP.

This subpackage contains orbital mechanics and astrodynamics calculations,
including orbital elements, propagation, perturbations, and interplanetary
trajectories.

The following public functions are available:

* :func:`circular_orbital_velocity` — compute circular orbital velocity from
  gravitational parameter and orbital radius.
* :func:`orbital_period` — compute Keplerian orbital period from gravitational
  parameter and semi-major axis.
* :func:`escape_velocity` — compute escape velocity from gravitational
  parameter and distance from centre.
* :func:`hohmann_transfer` — compute Hohmann transfer Delta-V budget and
  transfer time between two circular orbits.

All functions use SI units and require the gravitational parameter
``mu = G * M`` to be supplied by the caller. Orbital radii are measured
from the central body's centre.
"""

from aeromcp.astrodynamics.orbital import (
    circular_orbital_velocity,
    escape_velocity,
    hohmann_transfer,
    orbital_period,
)

__all__ = [
    "circular_orbital_velocity",
    "escape_velocity",
    "hohmann_transfer",
    "orbital_period",
]
