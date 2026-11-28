"""Thermal radiation heat transfer calculations (Stefan-Boltzmann law, SI units)."""

from __future__ import annotations

from aeromcp_engineering.core.constants import STEFAN_BOLTZMANN_W_M2_K4
from aeromcp_engineering.core.validation import validate_non_negative, validate_positive


def radiation_heat_rate(
    emissivity: float,
    area_m2: float,
    surface_temperature_k: float,
    surroundings_temperature_k: float = 0.0,
) -> float:
    """Compute net radiative heat rate Q = eps * sigma * A * (Ts^4 - Tsurr^4) in W."""
    eps = validate_positive(emissivity, "emissivity")
    if eps > 1.0:
        raise ValueError(f"emissivity must be <= 1.0. Got {eps!r}.")
    a = validate_positive(area_m2, "area_m2")
    ts = validate_non_negative(surface_temperature_k, "surface_temperature_k")
    tsurr = validate_non_negative(
        surroundings_temperature_k, "surroundings_temperature_k"
    )
    return eps * STEFAN_BOLTZMANN_W_M2_K4 * a * ((ts**4) - (tsurr**4))
