"""Discrete-time PID controller step with saturation and anti-windup."""

from __future__ import annotations

from aeromcp_engineering.core.validation import validate_finite, validate_positive


def pid_step(
    error: float,
    previous_error: float,
    integral_state: float,
    dt_s: float,
    kp: float,
    ki: float,
    kd: float,
    output_min: float = -float("inf"),
    output_max: float = float("inf"),
) -> dict[str, float]:
    """Compute one discrete-time PID step with clamping anti-windup."""
    e = validate_finite(error, "error")
    e_prev = validate_finite(previous_error, "previous_error")
    i_state = validate_finite(integral_state, "integral_state")
    dt = validate_positive(dt_s, "dt_s")
    p_gain = validate_finite(kp, "kp")
    i_gain = validate_finite(ki, "ki")
    d_gain = validate_finite(kd, "kd")
    if output_min >= output_max:
        raise ValueError("output_min must be < output_max.")

    p_term = p_gain * e
    d_term = d_gain * (e - e_prev) / dt
    new_integral = i_state + e * dt
    u_unsat = p_term + i_gain * new_integral + d_term

    if u_unsat > output_max:
        u = output_max
        if e > 0.0:
            new_integral = i_state
    elif u_unsat < output_min:
        u = output_min
        if e < 0.0:
            new_integral = i_state
    else:
        u = u_unsat

    return {
        "control_output": u,
        "integral_state": new_integral,
        "error": e,
    }
