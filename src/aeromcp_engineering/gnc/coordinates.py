"""WGS-84 geodetic <-> ECEF coordinate transformations (SI, radians)."""

from __future__ import annotations

import math

from aeromcp_engineering.core.constants import WGS84_A_M, WGS84_E2
from aeromcp_engineering.core.validation import validate_finite


def geodetic_to_ecef(
    latitude_rad: float,
    longitude_rad: float,
    altitude_m: float,
) -> dict[str, float]:
    """Convert WGS-84 geodetic (lat, lon, alt) to ECEF (x, y, z) in metres."""
    lat = validate_finite(latitude_rad, "latitude_rad")
    lon = validate_finite(longitude_rad, "longitude_rad")
    alt = validate_finite(altitude_m, "altitude_m")
    if abs(lat) > 0.5 * math.pi:
        raise ValueError("latitude_rad must be in [-pi/2, pi/2].")
    slat = math.sin(lat)
    clat = math.cos(lat)
    n = WGS84_A_M / math.sqrt(1.0 - WGS84_E2 * slat * slat)
    x = (n + alt) * clat * math.cos(lon)
    y = (n + alt) * clat * math.sin(lon)
    z = (n * (1.0 - WGS84_E2) + alt) * slat
    return {"x_m": x, "y_m": y, "z_m": z}


def ecef_to_geodetic(
    x_m: float,
    y_m: float,
    z_m: float,
    tol: float = 1e-12,
) -> dict[str, float]:
    """Convert ECEF (x, y, z) in metres to WGS-84 geodetic (lat_rad, lon_rad, alt_m)."""
    x = validate_finite(x_m, "x_m")
    y = validate_finite(y_m, "y_m")
    z = validate_finite(z_m, "z_m")
    lon = math.atan2(y, x)
    p = math.hypot(x, y)
    if p == 0.0 and z == 0.0:
        raise ValueError("ECEF origin (0, 0, 0) has undefined geodetic coordinates.")
    lat = math.atan2(z, p * (1.0 - WGS84_E2))
    alt = 0.0
    for _ in range(20):
        slat = math.sin(lat)
        n = WGS84_A_M / math.sqrt(1.0 - WGS84_E2 * slat * slat)
        alt_new = (
            p / math.cos(lat) - n
            if abs(math.cos(lat)) > 1e-12
            else abs(z) - n * (1.0 - WGS84_E2)
        )
        lat_new = math.atan2(z, p * (1.0 - WGS84_E2 * (n / (n + alt_new))))
        if abs(lat_new - lat) < tol and abs(alt_new - alt) < 1e-9:
            lat, alt = lat_new, alt_new
            break
        lat, alt = lat_new, alt_new
    return {"latitude_rad": lat, "longitude_rad": lon, "altitude_m": alt}
