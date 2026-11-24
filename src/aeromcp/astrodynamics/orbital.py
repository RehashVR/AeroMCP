"""Orbital mechanics calculations for AeroMCP.

This module implements fundamental astrodynamics functions using the
two-body gravitational model. All functions accept the gravitational
parameter ``mu`` as a caller-supplied parameter:

    mu = G * M

No central-body database or Earth-specific constants are hardcoded
inside the calculation functions.

Orbital radius and distance parameters are measured from the central
body's centre, not from its surface.
"""

from __future__ import annotations

import math

from aeromcp.core.validation import validate_positive


def circular_orbital_velocity(
    central_body_mu_m3_s2: float,
    orbital_radius_m: float,
) -> float:
    """Compute circular orbital velocity.

    Determines the velocity required for a circular orbit around a central
    body at a given orbital radius.

    Equation:
        v = sqrt(mu / r)

    Parameters
    ----------
    central_body_mu_m3_s2:
        Gravitational parameter of the central body in cubic metres per
        second squared (m^3/s^2). Must be strictly positive.
    orbital_radius_m:
        Orbital radius in metres (m), measured from the central body's
        centre. Must be strictly positive.

    Returns
    -------
    float
        Circular orbital velocity in metres per second (m/s).

    Raises
    ------
    TypeError
        If either input is not a real number or is a boolean.
    ValueError
        If either input is NaN, infinite, or not strictly positive.
    """
    mu = validate_positive(central_body_mu_m3_s2, "central_body_mu_m3_s2")
    r = validate_positive(orbital_radius_m, "orbital_radius_m")
    return math.sqrt(mu / r)


def orbital_period(
    central_body_mu_m3_s2: float,
    semi_major_axis_m: float,
) -> float:
    """Compute Keplerian orbital period.

    Determines the period of a bound elliptical orbit around a central
    body. For circular orbits, the semi-major axis equals the orbital
    radius.

    Equation:
        T = 2 * pi * sqrt(a**3 / mu)

    Parameters
    ----------
    central_body_mu_m3_s2:
        Gravitational parameter of the central body in cubic metres per
        second squared (m^3/s^2). Must be strictly positive.
    semi_major_axis_m:
        Semi-major axis in metres (m). Must be strictly positive.

    Returns
    -------
    float
        Orbital period in seconds (s).

    Raises
    ------
    TypeError
        If either input is not a real number or is a boolean.
    ValueError
        If either input is NaN, infinite, or not strictly positive.
    """
    mu = validate_positive(central_body_mu_m3_s2, "central_body_mu_m3_s2")
    a = validate_positive(semi_major_axis_m, "semi_major_axis_m")
    return 2.0 * math.pi * math.sqrt(a**3 / mu)


def escape_velocity(
    central_body_mu_m3_s2: float,
    distance_from_center_m: float,
) -> float:
    """Compute escape velocity.

    Determines the minimum velocity required for an object to escape the
    gravitational influence of a central body from a given distance.

    Equation:
        v_escape = sqrt(2 * mu / r)

    Parameters
    ----------
    central_body_mu_m3_s2:
        Gravitational parameter of the central body in cubic metres per
        second squared (m^3/s^2). Must be strictly positive.
    distance_from_center_m:
        Distance from the central body's centre in metres (m). Must be
        strictly positive.

    Returns
    -------
    float
        Escape velocity in metres per second (m/s).

    Raises
    ------
    TypeError
        If either input is not a real number or is a boolean.
    ValueError
        If either input is NaN, infinite, or not strictly positive.
    """
    mu = validate_positive(central_body_mu_m3_s2, "central_body_mu_m3_s2")
    r = validate_positive(distance_from_center_m, "distance_from_center_m")
    return math.sqrt(2.0 * mu / r)


def hohmann_transfer(
    central_body_mu_m3_s2: float,
    initial_orbit_radius_m: float,
    final_orbit_radius_m: float,
) -> dict[str, float | str]:
    """Compute Hohmann transfer parameters between two circular orbits.

    Determines the Delta-V budget and transfer time for a two-impulse
    Hohmann transfer between two coplanar circular orbits around the same
    central body.

    Equation:
        Transfer semi-major axis:   a_t = (r1 + r2) / 2
        Initial circular velocity:  vc1 = sqrt(mu / r1)
        Final circular velocity:    vc2 = sqrt(mu / r2)
        Transfer velocity at departure: vt1 = sqrt(mu * (2/r1 - 1/a_t))
        Transfer velocity at arrival:   vt2 = sqrt(mu * (2/r2 - 1/a_t))
        Departure Delta-V:          dv1 = abs(vt1 - vc1)
        Arrival Delta-V:            dv2 = abs(vc2 - vt2)
        Total Delta-V:              dv_total = dv1 + dv2
        Transfer time:              t = pi * sqrt(a_t**3 / mu)

    Parameters
    ----------
    central_body_mu_m3_s2:
        Gravitational parameter of the central body in cubic metres per
        second squared (m^3/s^2). Must be strictly positive.
    initial_orbit_radius_m:
        Initial circular orbit radius in metres (m), measured from the
        central body's centre. Must be strictly positive.
    final_orbit_radius_m:
        Final circular orbit radius in metres (m), measured from the
        central body's centre. Must be strictly positive and not equal to
        the initial orbit radius.

    Returns
    -------
    dict[str, float | str]
        A dictionary with the following keys:

        * ``initial_orbit_radius_m`` — initial orbit radius (m)
        * ``final_orbit_radius_m`` — final orbit radius (m)
        * ``transfer_semi_major_axis_m`` — transfer ellipse semi-major
          axis (m)
        * ``departure_delta_v_m_s`` — departure Delta-V magnitude (m/s)
        * ``arrival_delta_v_m_s`` — arrival Delta-V magnitude (m/s)
        * ``total_delta_v_m_s`` — total Delta-V magnitude (m/s)
        * ``transfer_time_s`` — transfer time (s)
        * ``transfer_direction`` — ``"outward"`` or ``"inward"``
        * ``burn_direction`` — ``"prograde"`` or ``"retrograde"``

    Raises
    ------
    TypeError
        If any input is not a real number or is a boolean.
    ValueError
        If any input is NaN, infinite, or not strictly positive, or if
        the initial and final orbit radii are equal.
    """
    mu = validate_positive(central_body_mu_m3_s2, "central_body_mu_m3_s2")
    r1 = validate_positive(initial_orbit_radius_m, "initial_orbit_radius_m")
    r2 = validate_positive(final_orbit_radius_m, "final_orbit_radius_m")

    if r1 == r2:
        raise ValueError(
            "initial_orbit_radius_m and final_orbit_radius_m must not be "
            f"equal. Got r1={r1!r}, r2={r2!r}."
        )

    a_t = (r1 + r2) / 2.0
    vc1 = math.sqrt(mu / r1)
    vc2 = math.sqrt(mu / r2)
    vt1 = math.sqrt(mu * (2.0 / r1 - 1.0 / a_t))
    vt2 = math.sqrt(mu * (2.0 / r2 - 1.0 / a_t))
    dv1 = abs(vt1 - vc1)
    dv2 = abs(vc2 - vt2)
    dv_total = dv1 + dv2
    transfer_time = math.pi * math.sqrt(a_t**3 / mu)

    if r2 > r1:
        transfer_direction = "outward"
        burn_direction = "prograde"
    else:
        transfer_direction = "inward"
        burn_direction = "retrograde"

    return {
        "initial_orbit_radius_m": r1,
        "final_orbit_radius_m": r2,
        "transfer_semi_major_axis_m": a_t,
        "departure_delta_v_m_s": dv1,
        "arrival_delta_v_m_s": dv2,
        "total_delta_v_m_s": dv_total,
        "transfer_time_s": transfer_time,
        "transfer_direction": transfer_direction,
        "burn_direction": burn_direction,
    }
