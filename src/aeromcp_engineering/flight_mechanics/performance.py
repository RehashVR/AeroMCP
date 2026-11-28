"""Aircraft performance calculations (SI units)."""

from __future__ import annotations

import math

from aeromcp_engineering.core.constants import G0_M_S2
from aeromcp_engineering.core.validation import validate_non_negative, validate_positive


def coordinated_turn_performance(
    velocity_m_s: float,
    bank_angle_rad: float,
) -> dict[str, float]:
    """Compute coordinated level-turn load factor, turn radius (m), and turn rate (rad/s)."""
    v = validate_positive(velocity_m_s, "velocity_m_s")
    phi = validate_non_negative(abs(bank_angle_rad), "bank_angle_rad")
    if phi >= 0.5 * math.pi:
        raise ValueError("bank_angle_rad magnitude must be < pi/2.")
    n = 1.0 / math.cos(phi)
    if phi == 0.0:
        return {
            "load_factor": 1.0,
            "turn_radius_m": float("inf"),
            "turn_rate_rad_s": 0.0,
        }
    tan_phi = math.tan(phi)
    radius = (v * v) / (G0_M_S2 * tan_phi)
    omega = (G0_M_S2 * tan_phi) / v
    return {
        "load_factor": n,
        "turn_radius_m": radius,
        "turn_rate_rad_s": omega,
    }


def climb_performance(
    thrust_n: float,
    drag_n: float,
    weight_n: float,
    velocity_m_s: float,
) -> dict[str, float]:
    """Compute steady climb rate (m/s) and climb gradient (sin(gamma))."""
    t = validate_non_negative(thrust_n, "thrust_n")
    d = validate_non_negative(drag_n, "drag_n")
    w = validate_positive(weight_n, "weight_n")
    v = validate_positive(velocity_m_s, "velocity_m_s")
    sin_gamma = (t - d) / w
    if abs(sin_gamma) > 1.0:
        raise ValueError(
            f"(thrust - drag)/weight = {sin_gamma:.4f} exceeds [-1, 1]; "
            "steady climb assumption invalid."
        )
    roc = v * sin_gamma
    return {
        "rate_of_climb_m_s": roc,
        "climb_gradient": sin_gamma,
        "flight_path_angle_rad": math.asin(sin_gamma),
    }


def glide_performance(
    lift_to_drag: float,
    altitude_m: float,
) -> dict[str, float]:
    """Compute steady unpowered glide range (m) and glide angle (rad)."""
    ld = validate_positive(lift_to_drag, "lift_to_drag")
    h = validate_non_negative(altitude_m, "altitude_m")
    return {
        "glide_range_m": h * ld,
        "glide_angle_rad": math.atan(1.0 / ld),
    }


def jet_breguet_range(
    velocity_m_s: float,
    tsfc_kg_n_s: float,
    lift_to_drag: float,
    initial_mass_kg: float,
    final_mass_kg: float,
) -> float:
    """Compute jet aircraft Breguet range (m) at constant V, TSFC, and L/D."""
    v = validate_positive(velocity_m_s, "velocity_m_s")
    c_t = validate_positive(tsfc_kg_n_s, "tsfc_kg_n_s")
    ld = validate_positive(lift_to_drag, "lift_to_drag")
    m0 = validate_positive(initial_mass_kg, "initial_mass_kg")
    mf = validate_positive(final_mass_kg, "final_mass_kg")
    if mf > m0:
        raise ValueError("final_mass_kg cannot exceed initial_mass_kg.")
    return (v / (G0_M_S2 * c_t)) * ld * math.log(m0 / mf)


def propeller_breguet_endurance(
    propeller_efficiency: float,
    bsfc_kg_w_s: float,
    lift_to_drag: float,
    velocity_m_s: float,
    initial_mass_kg: float,
    final_mass_kg: float,
) -> float:
    """Compute propeller aircraft endurance (s) at constant eta_p, BSFC, L/D, and V."""
    eta = validate_positive(propeller_efficiency, "propeller_efficiency")
    if eta > 1.0:
        raise ValueError("propeller_efficiency must be <= 1.0.")
    c_p = validate_positive(bsfc_kg_w_s, "bsfc_kg_w_s")
    ld = validate_positive(lift_to_drag, "lift_to_drag")
    v = validate_positive(velocity_m_s, "velocity_m_s")
    m0 = validate_positive(initial_mass_kg, "initial_mass_kg")
    mf = validate_positive(final_mass_kg, "final_mass_kg")
    if mf > m0:
        raise ValueError("final_mass_kg cannot exceed initial_mass_kg.")
    return (eta / (G0_M_S2 * c_p * v)) * ld * math.log(m0 / mf)


def takeoff_ground_roll(
    weight_n: float,
    thrust_n: float,
    drag_n: float,
    lift_n: float,
    liftoff_velocity_m_s: float,
    rolling_friction_coeff: float = 0.02,
) -> float:
    """Estimate constant-acceleration takeoff ground-roll distance (m)."""
    w = validate_positive(weight_n, "weight_n")
    t = validate_positive(thrust_n, "thrust_n")
    d = validate_non_negative(drag_n, "drag_n")
    lift = validate_non_negative(lift_n, "lift_n")
    v_lo = validate_positive(liftoff_velocity_m_s, "liftoff_velocity_m_s")
    mu_r = validate_non_negative(rolling_friction_coeff, "rolling_friction_coeff")
    net_force = t - d - mu_r * max(0.0, w - lift)
    if net_force <= 0.0:
        raise ValueError("Net accelerating force must be positive for takeoff.")
    accel = (net_force / w) * G0_M_S2
    return (v_lo * v_lo) / (2.0 * accel)
