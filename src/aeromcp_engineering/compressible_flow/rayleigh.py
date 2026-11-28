"""Rayleigh flow (frictionless, constant-area duct with heat addition) relations."""

from __future__ import annotations

from aeromcp_engineering.core.constants import GAMMA_AIR
from aeromcp_engineering.core.validation import validate_positive


def rayleigh_flow_ratios(mach: float, gamma: float = GAMMA_AIR) -> dict[str, float]:
    """Compute Rayleigh flow sonic reference ratios p/p*, T/T*, T0/T0*, p0/p0*."""
    m = validate_positive(mach, "mach")
    g = validate_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError(f"gamma must be > 1.0. Got {g!r}.")
    gp1 = g + 1.0
    gm1 = g - 1.0
    m_sq = m * m
    denom = 1.0 + g * m_sq

    p_pstar = gp1 / denom
    t_tstar = m_sq * (p_pstar**2)
    t0_t0star = (gp1 * m_sq * (2.0 + gm1 * m_sq)) / (denom**2)
    p0_p0star = p_pstar * (((2.0 + gm1 * m_sq) / gp1) ** (g / gm1))
    return {
        "mach": m,
        "p_over_pstar": p_pstar,
        "t_over_tstar": t_tstar,
        "t0_over_t0star": t0_t0star,
        "p0_over_p0star": p0_p0star,
    }
