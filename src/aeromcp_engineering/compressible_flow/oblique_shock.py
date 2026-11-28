"""Oblique shock relations (theta-beta-M) with weak/strong branch support."""

from __future__ import annotations

import math

from aeromcp_engineering.compressible_flow.normal_shock import normal_shock_relations
from aeromcp_engineering.core.constants import GAMMA_AIR
from aeromcp_engineering.core.numerical_methods import bisection
from aeromcp_engineering.core.validation import validate_non_negative, validate_positive


def _theta_from_beta(m1: float, beta_rad: float, gamma: float) -> float:
    sb = math.sin(beta_rad)
    cb = math.cos(beta_rad)
    m1_sq = m1 * m1
    num = 2.0 * (cb / sb) * (m1_sq * sb * sb - 1.0)
    den = m1_sq * (gamma + math.cos(2.0 * beta_rad)) + 2.0
    return math.atan(num / den)


def oblique_shock_relations(
    upstream_mach: float,
    deflection_angle_rad: float,
    branch: str = "weak",
    gamma: float = GAMMA_AIR,
) -> dict[str, float]:
    """Compute oblique shock wave angle beta and downstream properties.

    Rejects subsonic M1 < 1.0, negative deflection, or deflections exceeding
    theta_max (detached shock).
    """
    m1 = validate_positive(upstream_mach, "upstream_mach")
    theta = validate_non_negative(deflection_angle_rad, "deflection_angle_rad")
    g = validate_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError(f"gamma must be > 1.0. Got {g!r}.")
    if m1 <= 1.0:
        raise ValueError(f"Oblique shock requires upstream_mach > 1.0. Got {m1!r}.")
    b_name = branch.lower()
    if b_name not in ("weak", "strong"):
        raise ValueError(f"branch must be 'weak' or 'strong'. Got {branch!r}.")

    mu_rad = math.asin(1.0 / m1)
    if theta == 0.0:
        beta = mu_rad if b_name == "weak" else 0.5 * math.pi
    else:
        # Locate theta_max on [mu_rad, pi/2] by golden-section search
        phi = 0.5 * (math.sqrt(5.0) - 1.0)
        lo, hi = mu_rad, 0.5 * math.pi
        c = hi - phi * (hi - lo)
        d = lo + phi * (hi - lo)
        for _ in range(80):
            if _theta_from_beta(m1, c, g) < _theta_from_beta(m1, d, g):
                lo = c
                c = d
                d = lo + phi * (hi - lo)
            else:
                hi = d
                d = c
                c = hi - phi * (hi - lo)
        beta_max_theta = 0.5 * (lo + hi)
        theta_max = _theta_from_beta(m1, beta_max_theta, g)
        if theta > theta_max:
            raise ValueError(
                f"Deflection angle {theta:.6f} rad exceeds maximum attached-shock "
                f"deflection {theta_max:.6f} rad at M1={m1}; shock is detached."
            )

        def f(b_rad: float) -> float:
            return _theta_from_beta(m1, b_rad, g) - theta

        if b_name == "weak":
            beta = bisection(f, mu_rad, beta_max_theta, tol=1e-12).root
        else:
            beta = bisection(f, beta_max_theta, 0.5 * math.pi, tol=1e-12).root

    mn1 = m1 * math.sin(beta)
    normal = normal_shock_relations(max(mn1, 1.0), g)
    m2 = normal["downstream_mach"] / math.sin(beta - theta)
    return {
        "upstream_mach": m1,
        "deflection_angle_rad": theta,
        "shock_angle_rad": beta,
        "normal_mach_upstream": mn1,
        "downstream_mach": m2,
        "p2_over_p1": normal["p2_over_p1"],
        "rho2_over_rho1": normal["rho2_over_rho1"],
        "t2_over_t1": normal["t2_over_t1"],
        "p02_over_p01": normal["p02_over_p01"],
    }
