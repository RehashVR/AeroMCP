"""Preliminary aircraft wing sizing calculations (SI units)."""

from __future__ import annotations

import math

from aeromcp_engineering.core.validation import validate_positive


def wing_area_from_loading(weight_n: float, wing_loading_n_m2: float) -> float:
    """Compute required wing area S = W / (W/S) in m^2."""
    w = validate_positive(weight_n, "weight_n")
    ws = validate_positive(wing_loading_n_m2, "wing_loading_n_m2")
    return w / ws


def wingspan_from_aspect_ratio(aspect_ratio_val: float, wing_area_m2: float) -> float:
    """Compute wingspan b = sqrt(AR * S) in m."""
    ar = validate_positive(aspect_ratio_val, "aspect_ratio_val")
    s = validate_positive(wing_area_m2, "wing_area_m2")
    return math.sqrt(ar * s)


def rectangular_wing_mac(wing_area_m2: float, wingspan_m: float) -> float:
    """Compute mean aerodynamic chord c_bar = S / b for a rectangular wing (m)."""
    s = validate_positive(wing_area_m2, "wing_area_m2")
    b = validate_positive(wingspan_m, "wingspan_m")
    return s / b
