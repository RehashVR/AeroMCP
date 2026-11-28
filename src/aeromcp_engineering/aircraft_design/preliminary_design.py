"""Preliminary aircraft and electric UAV sizing calculations (SI units)."""

from __future__ import annotations

from aeromcp_engineering.core.validation import validate_positive


def thrust_to_weight_ratio(thrust_n: float, weight_n: float) -> float:
    """Compute thrust-to-weight ratio T / W (dimensionless)."""
    t = validate_positive(thrust_n, "thrust_n")
    w = validate_positive(weight_n, "weight_n")
    return t / w


def power_to_weight_ratio(power_w: float, weight_n: float) -> float:
    """Compute power-to-weight ratio P / W in W/N."""
    p = validate_positive(power_w, "power_w")
    w = validate_positive(weight_n, "weight_n")
    return p / w


def electric_uav_endurance(
    battery_energy_wh: float,
    usable_fraction: float,
    power_draw_w: float,
    propulsion_efficiency: float = 0.75,
) -> dict[str, float]:
    """Estimate electric UAV endurance (s and hours) from battery energy and power draw."""
    e_wh = validate_positive(battery_energy_wh, "battery_energy_wh")
    frac = validate_positive(usable_fraction, "usable_fraction")
    if frac > 1.0:
        raise ValueError("usable_fraction must be <= 1.0.")
    p_draw = validate_positive(power_draw_w, "power_draw_w")
    eta = validate_positive(propulsion_efficiency, "propulsion_efficiency")
    if eta > 1.0:
        raise ValueError("propulsion_efficiency must be <= 1.0.")

    usable_j = e_wh * 3600.0 * frac * eta
    endurance_s = usable_j / p_draw
    return {
        "usable_energy_j": usable_j,
        "endurance_s": endurance_s,
        "endurance_hr": endurance_s / 3600.0,
    }
