"""Fanno flow (adiabatic, constant-area duct with friction) relations."""

from __future__ import annotations

import math

from aeromcp_engineering.core.constants import GAMMA_AIR
from aeromcp_engineering.core.validation import validate_positive


def fanno_flow_ratios(mach: float, gamma: float = GAMMA_AIR) -> dict[str, float]:
    """Compute Fanno flow sonic reference ratios T/T*, p/p*, p0/p0*, and 4fL*/D."""
    m = validate_positive(mach, "mach")
    g = validate_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError(f"gamma must be > 1.0. Got {g!r}.")
    gp1 = g + 1.0
    gm1 = g - 1.0
    m_sq = m * m
    factor = (2.0 / gp1) * (1.0 + 0.5 * gm1 * m_sq)

    t_tstar = 1.0 / factor
    p_pstar = (1.0 / m) * math.sqrt(t_tstar)
    p0_p0star = (1.0 / m) * (factor ** (gp1 / (2.0 * gm1)))
    fanno_param = ((1.0 - m_sq) / (g * m_sq)) + (gp1 / (2.0 * g)) * math.log(
        (gp1 * m_sq) / (2.0 + gm1 * m_sq)
    )
    return {
        "mach": m,
        "t_over_tstar": t_tstar,
        "p_over_pstar": p_pstar,
        "p0_over_p0star": p0_p0star,
        "four_f_lstar_over_d": fanno_param,
    }
