"""Unit quaternion operations and ZYX Euler <-> quaternion conversions.

Convention: scalar-first quaternion q = [w, x, y, z].
Euler angles: intrinsic ZYX (yaw, pitch, roll) in radians.
"""

from __future__ import annotations

import math

from aeromcp_engineering.core.validation import validate_finite


def _validate_quat(q: list[float], name: str = "quaternion") -> list[float]:
    if len(q) != 4:
        raise ValueError(f"{name} must have length 4 [w, x, y, z].")
    return [validate_finite(v, name) for v in q]


def quaternion_normalize(q: list[float]) -> list[float]:
    """Normalize a scalar-first quaternion [w, x, y, z] to unit length."""
    qv = _validate_quat(q)
    norm = math.sqrt(sum(v * v for v in qv))
    if norm <= 0.0:
        raise ValueError("Cannot normalize zero-norm quaternion.")
    return [v / norm for v in qv]


def quaternion_multiply(q1: list[float], q2: list[float]) -> list[float]:
    """Multiply two scalar-first quaternions q1 * q2."""
    w1, x1, y1, z1 = _validate_quat(q1, "q1")
    w2, x2, y2, z2 = _validate_quat(q2, "q2")
    return [
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
        w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
    ]


def euler_zyx_to_quaternion(
    roll_rad: float,
    pitch_rad: float,
    yaw_rad: float,
) -> list[float]:
    """Convert ZYX Euler angles (roll, pitch, yaw) in rad to [w, x, y, z]."""
    phi = validate_finite(roll_rad, "roll_rad")
    theta = validate_finite(pitch_rad, "pitch_rad")
    psi = validate_finite(yaw_rad, "yaw_rad")
    cr, sr = math.cos(0.5 * phi), math.sin(0.5 * phi)
    cp, sp = math.cos(0.5 * theta), math.sin(0.5 * theta)
    cy, sy = math.cos(0.5 * psi), math.sin(0.5 * psi)
    return [
        cr * cp * cy + sr * sp * sy,
        sr * cp * cy - cr * sp * sy,
        cr * sp * cy + sr * cp * sy,
        cr * cp * sy - sr * sp * cy,
    ]


def quaternion_to_euler_zyx(q: list[float]) -> dict[str, float]:
    """Convert scalar-first quaternion [w, x, y, z] to ZYX Euler angles (rad)."""
    w, x, y, z = quaternion_normalize(q)
    sinr_cosp = 2.0 * (w * x + y * z)
    cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    sinp = max(-1.0, min(1.0, 2.0 * (w * y - z * x)))
    pitch = math.asin(sinp)

    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)
    return {"roll_rad": roll, "pitch_rad": pitch, "yaw_rad": yaw}
