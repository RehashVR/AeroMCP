"""Scalar discrete-time Kalman filter predict/update step."""

from __future__ import annotations

from aeromcp_engineering.core.validation import (
    validate_finite,
    validate_non_negative,
    validate_positive,
)


def scalar_kalman_update(
    prior_state: float,
    prior_variance: float,
    measurement: float,
    process_noise_variance: float,
    measurement_noise_variance: float,
) -> dict[str, float]:
    """Perform one scalar Kalman filter predict + measurement update step."""
    x_prev = validate_finite(prior_state, "prior_state")
    p_prev = validate_non_negative(prior_variance, "prior_variance")
    z = validate_finite(measurement, "measurement")
    q = validate_non_negative(process_noise_variance, "process_noise_variance")
    r = validate_positive(measurement_noise_variance, "measurement_noise_variance")

    p_pred = p_prev + q
    k_gain = p_pred / (p_pred + r)
    x_post = x_prev + k_gain * (z - x_prev)
    p_post = (1.0 - k_gain) * p_pred
    return {
        "posterior_state": x_post,
        "posterior_variance": p_post,
        "kalman_gain": k_gain,
    }
