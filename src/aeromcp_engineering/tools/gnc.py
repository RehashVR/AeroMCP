"""MCP tools for Guidance, Navigation, and Control (GNC)."""

from __future__ import annotations

from mcp.server import MCPServer

from aeromcp_engineering.core.results import build_result
from aeromcp_engineering.gnc import (
    ecef_to_geodetic,
    euler_zyx_to_quaternion,
    geodetic_to_ecef,
    pid_step,
    quaternion_to_euler_zyx,
    scalar_kalman_update,
)


def register_gnc_tools(mcp: MCPServer) -> None:
    """Register GNC MCP tools."""

    @mcp.tool()
    def convert_geodetic_to_ecef(
        latitude_rad: float, longitude_rad: float, altitude_m: float
    ) -> dict:
        """Convert WGS-84 geodetic (lat_rad, lon_rad, alt_m) to ECEF (m)."""
        res = geodetic_to_ecef(latitude_rad, longitude_rad, altitude_m)
        return build_result(
            calculation_name="convert_geodetic_to_ecef",
            engineering_domain="gnc",
            inputs={
                "latitude_rad": latitude_rad,
                "longitude_rad": longitude_rad,
                "altitude_m": altitude_m,
            },
            results=res,
            output_units={"x_m": "m", "y_m": "m", "z_m": "m"},
            equations=["WGS-84 ellipsoid geodetic-to-ECEF"],
            assumptions=["WGS-84 reference ellipsoid"],
            model="WGS-84 geodetic transformation",
            validity_limits=["|latitude_rad| <= pi/2"],
        )

    @mcp.tool()
    def convert_ecef_to_geodetic(x_m: float, y_m: float, z_m: float) -> dict:
        """Convert ECEF (m) to WGS-84 geodetic (lat_rad, lon_rad, alt_m)."""
        res = ecef_to_geodetic(x_m, y_m, z_m)
        return build_result(
            calculation_name="convert_ecef_to_geodetic",
            engineering_domain="gnc",
            inputs={"x_m": x_m, "y_m": y_m, "z_m": z_m},
            results=res,
            output_units={
                "latitude_rad": "rad",
                "longitude_rad": "rad",
                "altitude_m": "m",
            },
            equations=["Iterative WGS-84 ECEF-to-geodetic"],
            assumptions=["WGS-84 reference ellipsoid"],
            model="WGS-84 geodetic transformation",
            validity_limits=["(x, y, z) != (0, 0, 0)"],
        )

    @mcp.tool()
    def convert_euler_to_quaternion(
        roll_rad: float, pitch_rad: float, yaw_rad: float
    ) -> dict:
        """Convert ZYX Euler angles (rad) to scalar-first quaternion [w, x, y, z]."""
        q = euler_zyx_to_quaternion(roll_rad, pitch_rad, yaw_rad)
        return build_result(
            calculation_name="convert_euler_to_quaternion",
            engineering_domain="gnc",
            inputs={"roll_rad": roll_rad, "pitch_rad": pitch_rad, "yaw_rad": yaw_rad},
            results={"quaternion_wxyz": q},
            output_units={"quaternion_wxyz": "dimensionless"},
            equations=["Intrinsic ZYX Euler-to-quaternion"],
            assumptions=["Scalar-first [w, x, y, z]"],
            model="ZYX Euler-quaternion conversion",
            validity_limits=["Finite angles in radians"],
        )

    @mcp.tool()
    def convert_quaternion_to_euler(quaternion_wxyz: list[float]) -> dict:
        """Convert scalar-first quaternion [w, x, y, z] to ZYX Euler angles (rad)."""
        res = quaternion_to_euler_zyx(quaternion_wxyz)
        return build_result(
            calculation_name="convert_quaternion_to_euler",
            engineering_domain="gnc",
            inputs={"quaternion_wxyz": quaternion_wxyz},
            results=res,
            output_units={"roll_rad": "rad", "pitch_rad": "rad", "yaw_rad": "rad"},
            equations=["Quaternion-to-ZYX Euler"],
            assumptions=["Scalar-first [w, x, y, z]"],
            model="Quaternion-Euler conversion",
            validity_limits=["Non-zero quaternion"],
        )

    @mcp.tool()
    def compute_pid_step(
        error: float,
        previous_error: float,
        integral_state: float,
        dt_s: float,
        kp: float,
        ki: float,
        kd: float,
        output_min: float = -1e9,
        output_max: float = 1e9,
    ) -> dict:
        """Compute one discrete-time PID controller step with anti-windup."""
        res = pid_step(
            error,
            previous_error,
            integral_state,
            dt_s,
            kp,
            ki,
            kd,
            output_min,
            output_max,
        )
        return build_result(
            calculation_name="compute_pid_step",
            engineering_domain="gnc",
            inputs={"error": error, "dt_s": dt_s, "kp": kp, "ki": ki, "kd": kd},
            results=res,
            output_units={
                "control_output": "user_units",
                "integral_state": "user_units*s",
            },
            equations=["u = Kp*e + Ki*integral(e*dt) + Kd*(e - e_prev)/dt"],
            assumptions=["Fixed sample time dt_s > 0, clamping anti-windup"],
            model="Discrete PID controller",
            validity_limits=["dt_s > 0", "output_min < output_max"],
        )

    @mcp.tool()
    def compute_scalar_kalman_update(
        prior_state: float,
        prior_variance: float,
        measurement: float,
        process_noise_variance: float,
        measurement_noise_variance: float,
    ) -> dict:
        """Perform one scalar discrete-time Kalman filter predict and update step."""
        res = scalar_kalman_update(
            prior_state,
            prior_variance,
            measurement,
            process_noise_variance,
            measurement_noise_variance,
        )
        return build_result(
            calculation_name="compute_scalar_kalman_update",
            engineering_domain="gnc",
            inputs={"prior_state": prior_state, "measurement": measurement},
            results=res,
            output_units={
                "posterior_state": "user_units",
                "kalman_gain": "dimensionless",
            },
            equations=[
                "K = (P + Q) / (P + Q + R)",
                "x_post = x_prior + K*(z - x_prior)",
            ],
            assumptions=["Linear scalar Gaussian system"],
            model="Scalar Kalman filter",
            validity_limits=["measurement_noise_variance > 0", "prior_variance >= 0"],
        )
