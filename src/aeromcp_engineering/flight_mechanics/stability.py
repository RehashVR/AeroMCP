"""Foundational longitudinal static stability calculations."""

from __future__ import annotations

from aeromcp_engineering.core.validation import validate_finite, validate_positive


def static_margin(
    neutral_point_mac: float,
    cg_position_mac: float,
) -> float:
    """Compute longitudinal static margin SM = (x_np - x_cg) / MAC (dimensionless)."""
    x_np = validate_finite(neutral_point_mac, "neutral_point_mac")
    x_cg = validate_finite(cg_position_mac, "cg_position_mac")
    return x_np - x_cg


def neutral_point_position(
    aerodynamic_center_mac: float,
    tail_volume_ratio: float,
    tail_lift_slope_per_rad: float,
    wing_lift_slope_per_rad: float,
    downwash_gradient: float = 0.0,
    tail_efficiency: float = 1.0,
) -> float:
    """Compute stick-fixed neutral point position as a fraction of MAC."""
    x_ac = validate_finite(aerodynamic_center_mac, "aerodynamic_center_mac")
    v_h = validate_finite(tail_volume_ratio, "tail_volume_ratio")
    a_t = validate_positive(tail_lift_slope_per_rad, "tail_lift_slope_per_rad")
    a_w = validate_positive(wing_lift_slope_per_rad, "wing_lift_slope_per_rad")
    deda = validate_finite(downwash_gradient, "downwash_gradient")
    eta_t = validate_positive(tail_efficiency, "tail_efficiency")
    return x_ac + eta_t * v_h * (a_t / a_w) * (1.0 - deda)
