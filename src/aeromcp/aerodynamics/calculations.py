"""Aerodynamics engineering calculations for AeroMCP.

This module implements five fundamental aerospace engineering calculation
functions using SI units. All functions are independent of the Model Context
Protocol (MCP) and can be used directly in any Python program.

Governing equations:

* Dynamic pressure:     q = 0.5 * density * velocity**2
* Lift force:           L = q * S * CL
* Drag force:           D = q * S * CD
* Lift coefficient:     CL = L / (0.5 * density * velocity**2 * area)
* Reynolds number:      Re = density * velocity * length / viscosity
"""

from __future__ import annotations

from aeromcp.core.validation import (
    validate_finite,
    validate_non_negative,
    validate_positive,
)


def dynamic_pressure(density_kg_m3: float, velocity_m_s: float) -> float:
    """Compute dynamic pressure.

    Equation:
        q = 0.5 * density * velocity**2

    Parameters
    ----------
    density_kg_m3:
        Air density in kilograms per cubic metre (kg/m^3). Must be strictly
        positive.
    velocity_m_s:
        Flow velocity in metres per second (m/s). Must be non-negative.

    Returns
    -------
    float
        Dynamic pressure in pascals (Pa).

    Raises
    ------
    TypeError
        If either input is not a real number or is a boolean.
    ValueError
        If either input is NaN or infinite, if density is not strictly
        positive, or if velocity is negative.
    """
    density = validate_positive(density_kg_m3, "density_kg_m3")
    velocity = validate_non_negative(velocity_m_s, "velocity_m_s")
    return 0.5 * density * velocity**2


def lift_force(
    density_kg_m3: float,
    velocity_m_s: float,
    reference_area_m2: float,
    lift_coefficient: float,
) -> float:
    """Compute lift force.

    Equation:
        L = q * S * CL = 0.5 * density * velocity**2 * area * CL

    Parameters
    ----------
    density_kg_m3:
        Air density in kg/m^3. Must be strictly positive.
    velocity_m_s:
        Flow velocity in m/s. Must be non-negative.
    reference_area_m2:
        Reference area in square metres (m^2). Must be strictly positive.
    lift_coefficient:
        Dimensionless lift coefficient. May be negative, zero, or positive,
        but must be finite.

    Returns
    -------
    float
        Lift force in newtons (N).

    Raises
    ------
    TypeError
        If any input is not a real number or is a boolean.
    ValueError
        If any input is NaN or infinite, if density/area are not strictly
        positive, if velocity is negative.
    """
    density = validate_positive(density_kg_m3, "density_kg_m3")
    velocity = validate_non_negative(velocity_m_s, "velocity_m_s")
    area = validate_positive(reference_area_m2, "reference_area_m2")
    cl = validate_finite(lift_coefficient, "lift_coefficient")
    q = 0.5 * density * velocity**2
    return q * area * cl


def drag_force(
    density_kg_m3: float,
    velocity_m_s: float,
    reference_area_m2: float,
    drag_coefficient: float,
) -> float:
    """Compute drag force.

    Equation:
        D = q * S * CD = 0.5 * density * velocity**2 * area * CD

    Parameters
    ----------
    density_kg_m3:
        Air density in kg/m^3. Must be strictly positive.
    velocity_m_s:
        Flow velocity in m/s. Must be non-negative.
    reference_area_m2:
        Reference area in square metres (m^2). Must be strictly positive.
    drag_coefficient:
        Dimensionless drag coefficient. Must be finite and non-negative.

    Returns
    -------
    float
        Drag force in newtons (N).

    Raises
    ------
    TypeError
        If any input is not a real number or is a boolean.
    ValueError
        If any input is NaN or infinite, if density/area are not strictly
        positive, if velocity is negative, or if drag coefficient is negative.
    """
    density = validate_positive(density_kg_m3, "density_kg_m3")
    velocity = validate_non_negative(velocity_m_s, "velocity_m_s")
    area = validate_positive(reference_area_m2, "reference_area_m2")
    cd = validate_non_negative(drag_coefficient, "drag_coefficient")
    q = 0.5 * density * velocity**2
    return q * area * cd


def lift_coefficient(
    lift_force_n: float,
    density_kg_m3: float,
    velocity_m_s: float,
    reference_area_m2: float,
) -> float:
    """Compute dimensionless lift coefficient.

    Equation:
        CL = L / (0.5 * density * velocity**2 * area)

    Parameters
    ----------
    lift_force_n:
        Lift force in newtons (N). Must be finite; may be negative or zero.
    density_kg_m3:
        Air density in kg/m^3. Must be strictly positive.
    velocity_m_s:
        Flow velocity in m/s. Must be strictly positive (zero velocity would
        make the denominator zero).
    reference_area_m2:
        Reference area in square metres (m^2). Must be strictly positive.

    Returns
    -------
    float
        Dimensionless lift coefficient.

    Raises
    ------
    TypeError
        If any input is not a real number or is a boolean.
    ValueError
        If any input is NaN or infinite, if density/velocity/area are not
        strictly positive.
    """
    lift = validate_finite(lift_force_n, "lift_force_n")
    density = validate_positive(density_kg_m3, "density_kg_m3")
    velocity = validate_positive(velocity_m_s, "velocity_m_s")
    area = validate_positive(reference_area_m2, "reference_area_m2")
    q = 0.5 * density * velocity**2
    return lift / (q * area)


def reynolds_number(
    density_kg_m3: float,
    velocity_m_s: float,
    characteristic_length_m: float,
    dynamic_viscosity_pa_s: float,
) -> float:
    """Compute dimensionless Reynolds number.

    Equation:
        Re = density * velocity * characteristic_length / dynamic_viscosity

    Parameters
    ----------
    density_kg_m3:
        Air density in kg/m^3. Must be strictly positive.
    velocity_m_s:
        Flow velocity in m/s. Must be non-negative.
    characteristic_length_m:
        Characteristic length in metres (m). Must be strictly positive.
    dynamic_viscosity_pa_s:
        Dynamic viscosity in pascal-seconds (Pa*s). Must be strictly positive.

    Returns
    -------
    float
        Dimensionless Reynolds number.

    Raises
    ------
    TypeError
        If any input is not a real number or is a boolean.
    ValueError
        If any input is NaN or infinite, if density/length/viscosity are not
        strictly positive, or if velocity is negative.
    """
    density = validate_positive(density_kg_m3, "density_kg_m3")
    velocity = validate_non_negative(velocity_m_s, "velocity_m_s")
    length = validate_positive(characteristic_length_m, "characteristic_length_m")
    viscosity = validate_positive(dynamic_viscosity_pa_s, "dynamic_viscosity_pa_s")
    return density * velocity * length / viscosity
