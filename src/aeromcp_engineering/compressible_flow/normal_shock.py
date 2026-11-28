"""Normal shock relations (calorically perfect ideal gas)."""

from __future__ import annotations

import math

from aeromcp_engineering.core.constants import GAMMA_AIR
from aeromcp_engineering.core.validation import validate_positive


def normal_shock_relations(
    upstream_mach: float, gamma: float = GAMMA_AIR
) -> dict[str, float]:
    """Compute normal shock downstream Mach and property ratios for M1 >= 1.0."""
    m1 = validate_positive(upstream_mach, "upstream_mach")
    g = validate_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError(f"gamma must be > 1.0. Got {g!r}.")
    if m1 < 1.0:
        raise ValueError(
            f"Normal shock requires supersonic upstream_mach >= 1.0. Got {m1!r}."
        )

    m1_sq = m1 * m1
    gm1 = g - 1.0
    gp1 = g + 1.0

    m2_sq = (1.0 + 0.5 * gm1 * m1_sq) / (g * m1_sq - 0.5 * gm1)
    m2 = math.sqrt(m2_sq)
    p2_p1 = 1.0 + (2.0 * g / gp1) * (m1_sq - 1.0)
    rho2_rho1 = (gp1 * m1_sq) / (2.0 + gm1 * m1_sq)
    t2_t1 = p2_p1 / rho2_rho1

    term1 = ((gp1 * m1_sq) / (2.0 + gm1 * m1_sq)) ** (g / gm1)
    term2 = (gp1 / (2.0 * g * m1_sq - gm1)) ** (1.0 / gm1)
    p02_p01 = term1 * term2

    return {
        "upstream_mach": m1,
        "downstream_mach": m2,
        "p2_over_p1": p2_p1,
        "rho2_over_rho1": rho2_rho1,
        "t2_over_t1": t2_t1,
        "p02_over_p01": p02_p01,
    }
