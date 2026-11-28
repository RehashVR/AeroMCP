"""Guidance, Navigation, and Control (GNC) calculations for AeroMCP."""

from __future__ import annotations

from aeromcp_engineering.gnc.controllers import pid_step
from aeromcp_engineering.gnc.coordinates import ecef_to_geodetic, geodetic_to_ecef
from aeromcp_engineering.gnc.estimation import scalar_kalman_update
from aeromcp_engineering.gnc.quaternions import (
    euler_zyx_to_quaternion,
    quaternion_multiply,
    quaternion_normalize,
    quaternion_to_euler_zyx,
)

__all__ = [
    "ecef_to_geodetic",
    "euler_zyx_to_quaternion",
    "geodetic_to_ecef",
    "pid_step",
    "quaternion_multiply",
    "quaternion_normalize",
    "quaternion_to_euler_zyx",
    "scalar_kalman_update",
]
