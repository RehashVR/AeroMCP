"""Isentropic compressible flow relations (calorically perfect ideal gas)."""

from __future__ import annotations

from aeromcp_engineering.core.constants import GAMMA_AIR
from aeromcp_engineering.core.validation import validate_non_negative, validate_positive


def _validate_gamma(gamma: float) -> float:
    g = validate_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError(f"gamma must be > 1.0. Got {g!r}.")
    return g


def isentropic_ratios(mach: float, gamma: float = GAMMA_AIR) -> dict[str, float]:
    """Compute stagnation-to-static ratios T0/T, p0/p, rho0/rho for Mach number."""
    m = validate_non_negative(mach, "mach")
    g = _validate_gamma(gamma)
    factor = 1.0 + 0.5 * (g - 1.0) * m * m
    p0_p = factor ** (g / (g - 1.0))
    rho0_rho = factor ** (1.0 / (g - 1.0))
    return {
        "mach": m,
        "gamma": g,
        "t0_over_t": factor,
        "p0_over_p": p0_p,
        "rho0_over_rho": rho0_rho,
    }


def isentropic_static_properties(
    mach: float,
    stagnation_temperature_k: float,
    stagnation_pressure_pa: float,
    gamma: float = GAMMA_AIR,
) -> dict[str, float]:
    """Compute static T (K) and p (Pa) from stagnation conditions and Mach number."""
    t0 = validate_positive(stagnation_temperature_k, "stagnation_temperature_k")
    p0 = validate_positive(stagnation_pressure_pa, "stagnation_pressure_pa")
    ratios = isentropic_ratios(mach, gamma)
    return {
        "static_temperature_k": t0 / ratios["t0_over_t"],
        "static_pressure_pa": p0 / ratios["p0_over_p"],
        **ratios,
    }
