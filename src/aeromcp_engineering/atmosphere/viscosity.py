"""Atmospheric viscosity calculations (Sutherland's law and kinematic viscosity)."""

from __future__ import annotations

from aeromcp_engineering.core.constants import (
    SUTHERLAND_MU0_PA_S,
    SUTHERLAND_S_K,
    SUTHERLAND_T0_K,
)
from aeromcp_engineering.core.validation import validate_positive


def sutherland_viscosity(temperature_k: float) -> float:
    """Compute dynamic viscosity of air using Sutherland's law (Pa*s)."""
    t = validate_positive(temperature_k, "temperature_k")
    return (
        SUTHERLAND_MU0_PA_S
        * ((t / SUTHERLAND_T0_K) ** 1.5)
        * ((SUTHERLAND_T0_K + SUTHERLAND_S_K) / (t + SUTHERLAND_S_K))
    )


def kinematic_viscosity(dynamic_viscosity_pa_s: float, density_kg_m3: float) -> float:
    """Compute kinematic viscosity nu = mu / rho in m^2/s."""
    mu = validate_positive(dynamic_viscosity_pa_s, "dynamic_viscosity_pa_s")
    rho = validate_positive(density_kg_m3, "density_kg_m3")
    return mu / rho
