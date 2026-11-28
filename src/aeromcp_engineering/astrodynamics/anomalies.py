"""Orbital anomaly conversions and Kepler equation solver (radians)."""

from __future__ import annotations

import math

from aeromcp_engineering.core.numerical_methods import safeguarded_newton
from aeromcp_engineering.core.validation import validate_finite, validate_non_negative


def _validate_elliptic_eccentricity(eccentricity: float) -> float:
    e = validate_non_negative(eccentricity, "eccentricity")
    if e >= 1.0:
        raise ValueError(f"Elliptic orbit requires 0 <= e < 1.0. Got {e!r}.")
    return e


def solve_kepler_elliptic(
    mean_anomaly_rad: float,
    eccentricity: float,
    tol: float = 1e-12,
) -> float:
    """Solve Kepler's equation M = E - e*sin(E) for eccentric anomaly E (rad)."""
    m_raw = validate_finite(mean_anomaly_rad, "mean_anomaly_rad")
    e = _validate_elliptic_eccentricity(eccentricity)
    m = m_raw % (2.0 * math.pi)
    if e == 0.0:
        return m

    def f(ecc_anom: float) -> float:
        return ecc_anom - e * math.sin(ecc_anom) - m

    def df(ecc_anom: float) -> float:
        return 1.0 - e * math.cos(ecc_anom)

    res = safeguarded_newton(f, df, 0.0, 2.0 * math.pi, x0=m, tol=tol)
    return res.root


def eccentric_to_true_anomaly(
    eccentric_anomaly_rad: float, eccentricity: float
) -> float:
    """Convert eccentric anomaly E (rad) to true anomaly nu (rad) in [0, 2*pi)."""
    e_anom = validate_finite(eccentric_anomaly_rad, "eccentric_anomaly_rad")
    e = _validate_elliptic_eccentricity(eccentricity)
    nu = 2.0 * math.atan2(
        math.sqrt(1.0 + e) * math.sin(0.5 * e_anom),
        math.sqrt(1.0 - e) * math.cos(0.5 * e_anom),
    )
    return nu % (2.0 * math.pi)


def true_to_eccentric_anomaly(true_anomaly_rad: float, eccentricity: float) -> float:
    """Convert true anomaly nu (rad) to eccentric anomaly E (rad) in [0, 2*pi)."""
    nu = validate_finite(true_anomaly_rad, "true_anomaly_rad")
    e = _validate_elliptic_eccentricity(eccentricity)
    e_anom = 2.0 * math.atan2(
        math.sqrt(1.0 - e) * math.sin(0.5 * nu),
        math.sqrt(1.0 + e) * math.cos(0.5 * nu),
    )
    return e_anom % (2.0 * math.pi)


def mean_to_true_anomaly(mean_anomaly_rad: float, eccentricity: float) -> float:
    """Convert mean anomaly M (rad) to true anomaly nu (rad)."""
    e_anom = solve_kepler_elliptic(mean_anomaly_rad, eccentricity)
    return eccentric_to_true_anomaly(e_anom, eccentricity)


def true_to_mean_anomaly(true_anomaly_rad: float, eccentricity: float) -> float:
    """Convert true anomaly nu (rad) to mean anomaly M (rad)."""
    e = _validate_elliptic_eccentricity(eccentricity)
    e_anom = true_to_eccentric_anomaly(true_anomaly_rad, e)
    return (e_anom - e * math.sin(e_anom)) % (2.0 * math.pi)
