"""Rotorcraft and multirotor hover momentum-theory calculations (SI units)."""

from __future__ import annotations

import math

from aeromcp_engineering.core.validation import validate_positive


def rotor_hover_power(
    thrust_n: float,
    rotor_radius_m: float,
    density_kg_m3: float,
    figure_of_merit: float = 0.75,
) -> dict[str, float]:
    """Compute ideal and actual rotor hover power using momentum theory."""
    t = validate_positive(thrust_n, "thrust_n")
    r = validate_positive(rotor_radius_m, "rotor_radius_m")
    rho = validate_positive(density_kg_m3, "density_kg_m3")
    fm = validate_positive(figure_of_merit, "figure_of_merit")
    if fm > 1.0:
        raise ValueError(f"figure_of_merit must be <= 1.0. Got {fm!r}.")

    area = math.pi * r * r
    dl = t / area
    vi = math.sqrt(t / (2.0 * rho * area))
    p_ideal = t * vi
    p_actual = p_ideal / fm
    return {
        "disk_area_m2": area,
        "disk_loading_n_m2": dl,
        "induced_velocity_m_s": vi,
        "ideal_hover_power_w": p_ideal,
        "actual_hover_power_w": p_actual,
    }


def multirotor_hover_estimate(
    total_weight_n: float,
    num_rotors: int,
    rotor_radius_m: float,
    density_kg_m3: float,
    figure_of_merit: float = 0.7,
) -> dict[str, float]:
    """Estimate total hover power and per-rotor thrust for a multirotor."""
    w = validate_positive(total_weight_n, "total_weight_n")
    if (
        isinstance(num_rotors, bool)
        or not isinstance(num_rotors, int)
        or num_rotors < 1
    ):
        raise ValueError(f"num_rotors must be a positive integer. Got {num_rotors!r}.")
    t_per_rotor = w / num_rotors
    single = rotor_hover_power(
        t_per_rotor, rotor_radius_m, density_kg_m3, figure_of_merit
    )
    return {
        "thrust_per_rotor_n": t_per_rotor,
        "total_ideal_hover_power_w": single["ideal_hover_power_w"] * num_rotors,
        "total_actual_hover_power_w": single["actual_hover_power_w"] * num_rotors,
        "disk_loading_n_m2": single["disk_loading_n_m2"],
    }
