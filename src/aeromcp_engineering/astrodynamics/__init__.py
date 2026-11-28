"""Astrodynamics engineering calculations for AeroMCP."""

from __future__ import annotations

from aeromcp_engineering.astrodynamics.anomalies import (
    eccentric_to_true_anomaly,
    mean_to_true_anomaly,
    solve_kepler_elliptic,
    true_to_eccentric_anomaly,
    true_to_mean_anomaly,
)
from aeromcp_engineering.astrodynamics.orbital import (
    circular_orbital_velocity,
    escape_velocity,
    hohmann_transfer,
    orbital_period,
)
from aeromcp_engineering.astrodynamics.perturbations import j2_secular_rates
from aeromcp_engineering.astrodynamics.propagation import propagate_two_body_rk4
from aeromcp_engineering.astrodynamics.transformations import (
    c3_energy,
    coe_to_rv,
    hyperbolic_excess_velocity,
    periapsis_apoapsis,
    vis_viva_velocity,
)

__all__ = [
    "c3_energy",
    "circular_orbital_velocity",
    "coe_to_rv",
    "eccentric_to_true_anomaly",
    "escape_velocity",
    "hohmann_transfer",
    "hyperbolic_excess_velocity",
    "j2_secular_rates",
    "mean_to_true_anomaly",
    "orbital_period",
    "periapsis_apoapsis",
    "propagate_two_body_rk4",
    "solve_kepler_elliptic",
    "true_to_eccentric_anomaly",
    "true_to_mean_anomaly",
    "vis_viva_velocity",
]
