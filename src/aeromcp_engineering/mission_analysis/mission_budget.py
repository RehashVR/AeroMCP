"""Mission delta-V budgeting utilities (SI units)."""

from __future__ import annotations

from typing import Sequence

from aeromcp_engineering.core.validation import validate_non_negative


def mission_delta_v_budget(
    maneuver_delta_vs_m_s: Sequence[float],
    margin_fraction: float = 0.05,
) -> dict[str, float]:
    """Sum mission maneuver delta-Vs and apply a fractional margin."""
    if not maneuver_delta_vs_m_s:
        raise ValueError("maneuver_delta_vs_m_s must be non-empty.")
    nominal = sum(validate_non_negative(dv, "delta_v") for dv in maneuver_delta_vs_m_s)
    margin = validate_non_negative(margin_fraction, "margin_fraction")
    return {
        "nominal_delta_v_m_s": nominal,
        "margin_delta_v_m_s": nominal * margin,
        "total_budget_delta_v_m_s": nominal * (1.0 + margin),
    }
