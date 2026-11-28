"""Convective heat transfer calculations (Newton's law of cooling, SI units)."""

from __future__ import annotations

from aeromcp_engineering.core.validation import validate_finite, validate_positive


def convection_heat_rate(
    heat_transfer_coeff_w_m2_k: float,
    area_m2: float,
    surface_temperature_k: float,
    fluid_temperature_k: float,
) -> float:
    """Compute convective heat transfer rate Q = h * A * (Ts - Tinf) in watts (W)."""
    h = validate_positive(heat_transfer_coeff_w_m2_k, "heat_transfer_coeff_w_m2_k")
    a = validate_positive(area_m2, "area_m2")
    ts = validate_finite(surface_temperature_k, "surface_temperature_k")
    tinf = validate_finite(fluid_temperature_k, "fluid_temperature_k")
    return h * a * (ts - tinf)
