"""1D steady-state thermal conduction and series resistance (SI units)."""

from __future__ import annotations

from typing import Sequence

from aeromcp_engineering.core.validation import validate_finite, validate_positive


def conduction_1d_heat_rate(
    thermal_conductivity_w_m_k: float,
    area_m2: float,
    delta_temperature_k: float,
    thickness_m: float,
) -> float:
    """Compute 1D Fourier conduction heat rate Q = k * A * dT / L in watts (W)."""
    k = validate_positive(thermal_conductivity_w_m_k, "thermal_conductivity_w_m_k")
    a = validate_positive(area_m2, "area_m2")
    dt = validate_finite(delta_temperature_k, "delta_temperature_k")
    l_wall = validate_positive(thickness_m, "thickness_m")
    return k * a * dt / l_wall


def series_thermal_resistance_heat_rate(
    delta_temperature_k: float,
    resistances_k_w: Sequence[float],
) -> dict[str, float]:
    """Compute steady-state heat rate through series thermal resistances (W)."""
    dt = validate_finite(delta_temperature_k, "delta_temperature_k")
    if not resistances_k_w:
        raise ValueError("resistances_k_w must be non-empty.")
    r_total = sum(validate_positive(r, "resistance_k_w") for r in resistances_k_w)
    return {
        "total_resistance_k_w": r_total,
        "heat_rate_w": dt / r_total,
    }
