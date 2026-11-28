"""Isentropic Area-Mach relation and subsonic/supersonic inverse solvers."""

from __future__ import annotations

from aeromcp_engineering.core.constants import GAMMA_AIR
from aeromcp_engineering.core.numerical_methods import bisection
from aeromcp_engineering.core.validation import validate_positive


def area_mach_ratio(mach: float, gamma: float = GAMMA_AIR) -> float:
    """Compute isentropic area ratio A/A* for a given Mach number (M > 0)."""
    m = validate_positive(mach, "mach")
    g = validate_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError(f"gamma must be > 1.0. Got {g!r}.")
    gp1 = g + 1.0
    gm1 = g - 1.0
    term = (2.0 / gp1) * (1.0 + 0.5 * gm1 * m * m)
    return (1.0 / m) * (term ** (gp1 / (2.0 * gm1)))


def solve_mach_from_area_ratio(
    area_ratio: float,
    branch: str = "supersonic",
    gamma: float = GAMMA_AIR,
) -> float:
    """Solve for Mach number given A/A* >= 1.0 on 'subsonic' or 'supersonic' branch."""
    ar = validate_positive(area_ratio, "area_ratio")
    if ar < 1.0:
        raise ValueError(f"area_ratio A/A* must be >= 1.0. Got {ar!r}.")
    if ar == 1.0:
        return 1.0

    b = branch.lower()
    if b not in ("subsonic", "supersonic"):
        raise ValueError(f"branch must be 'subsonic' or 'supersonic'. Got {branch!r}.")

    def f(m: float) -> float:
        return area_mach_ratio(m, gamma) - ar

    if b == "subsonic":
        res = bisection(f, 1e-6, 1.0 - 1e-9, tol=1e-12)
        return res.root

    hi = 2.0
    while area_mach_ratio(hi, gamma) < ar:
        hi *= 2.0
        if hi > 1e6:
            raise ValueError(f"area_ratio {ar} is too large to bracket.")
    res = bisection(f, 1.0 + 1e-9, hi, tol=1e-12)
    return res.root
