"""Prandtl-Meyer expansion function and inverse solver."""

from __future__ import annotations

import math

from aeromcp_engineering.core.constants import GAMMA_AIR
from aeromcp_engineering.core.numerical_methods import bisection
from aeromcp_engineering.core.validation import validate_non_negative, validate_positive


def prandtl_meyer_angle(mach: float, gamma: float = GAMMA_AIR) -> float:
    """Compute Prandtl-Meyer function nu(M) in radians for M >= 1.0."""
    m = validate_positive(mach, "mach")
    g = validate_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError(f"gamma must be > 1.0. Got {g!r}.")
    if m < 1.0:
        raise ValueError(f"Prandtl-Meyer requires supersonic mach >= 1.0. Got {m!r}.")
    if m == 1.0:
        return 0.0
    gp1 = g + 1.0
    gm1 = g - 1.0
    term1 = math.sqrt(gp1 / gm1) * math.atan(math.sqrt((gm1 / gp1) * (m * m - 1.0)))
    term2 = math.atan(math.sqrt(m * m - 1.0))
    return term1 - term2


def inverse_prandtl_meyer(nu_rad: float, gamma: float = GAMMA_AIR) -> float:
    """Solve for supersonic Mach number given Prandtl-Meyer angle nu (rad)."""
    nu = validate_non_negative(nu_rad, "nu_rad")
    g = validate_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError(f"gamma must be > 1.0. Got {g!r}.")
    nu_max = 0.5 * math.pi * (math.sqrt((g + 1.0) / (g - 1.0)) - 1.0)
    if nu >= nu_max:
        raise ValueError(
            f"Prandtl-Meyer angle {nu:.6f} rad must be < nu_max ({nu_max:.6f} rad)."
        )
    if nu == 0.0:
        return 1.0

    def f(m: float) -> float:
        return prandtl_meyer_angle(m, g) - nu

    hi = 2.0
    while prandtl_meyer_angle(hi, g) < nu:
        hi *= 2.0
    return bisection(f, 1.0, hi, tol=1e-12).root
