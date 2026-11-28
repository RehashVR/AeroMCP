"""MCP tools for astrodynamics (new v0.3.0 tools)."""

from __future__ import annotations

from mcp.server import MCPServer

from aeromcp_engineering.astrodynamics import (
    c3_energy,
    coe_to_rv,
    hyperbolic_excess_velocity,
    j2_secular_rates,
    mean_to_true_anomaly,
    periapsis_apoapsis,
    propagate_two_body_rk4,
    solve_kepler_elliptic,
    vis_viva_velocity,
)
from aeromcp_engineering.core.constants import MU_EARTH_M3_S2
from aeromcp_engineering.core.results import build_result


def register_astrodynamics_tools(mcp: MCPServer) -> None:
    """Register expanded astrodynamics MCP tools."""

    @mcp.tool()
    def calculate_vis_viva_velocity(
        radius_m: float,
        semi_major_axis_m: float,
        gravitational_parameter_m3_s2: float = MU_EARTH_M3_S2,
    ) -> dict:
        """Calculate orbital speed (m/s) from the vis-viva equation."""
        v = vis_viva_velocity(
            radius_m, semi_major_axis_m, gravitational_parameter_m3_s2
        )
        return build_result(
            calculation_name="calculate_vis_viva_velocity",
            engineering_domain="astrodynamics",
            inputs={
                "radius_m": radius_m,
                "semi_major_axis_m": semi_major_axis_m,
                "gravitational_parameter_m3_s2": gravitational_parameter_m3_s2,
            },
            results={"velocity_m_s": v},
            output_units={"velocity_m_s": "m/s"},
            equations=["v = sqrt(mu * (2/r - 1/a))"],
            assumptions=["Two-body point-mass gravity"],
            model="Vis-viva equation",
            validity_limits=["radius_m > 0", "semi_major_axis_m != 0"],
        )

    @mcp.tool()
    def solve_kepler_equation(mean_anomaly_rad: float, eccentricity: float) -> dict:
        """Solve Kepler's equation M = E - e*sin(E) for eccentric and true anomaly (rad)."""
        e_anom = solve_kepler_elliptic(mean_anomaly_rad, eccentricity)
        nu = mean_to_true_anomaly(mean_anomaly_rad, eccentricity)
        return build_result(
            calculation_name="solve_kepler_equation",
            engineering_domain="astrodynamics",
            inputs={"mean_anomaly_rad": mean_anomaly_rad, "eccentricity": eccentricity},
            results={"eccentric_anomaly_rad": e_anom, "true_anomaly_rad": nu},
            output_units={"eccentric_anomaly_rad": "rad", "true_anomaly_rad": "rad"},
            equations=["M = E - e*sin(E)"],
            assumptions=["Elliptic orbit (0 <= e < 1)"],
            model="Safeguarded Newton Kepler solver",
            validity_limits=["0 <= eccentricity < 1.0"],
        )

    @mcp.tool()
    def convert_coe_to_eci(
        semi_major_axis_m: float,
        eccentricity: float,
        inclination_rad: float,
        raan_rad: float,
        arg_periapsis_rad: float,
        true_anomaly_rad: float,
        gravitational_parameter_m3_s2: float = MU_EARTH_M3_S2,
    ) -> dict:
        """Convert classical orbital elements (ECI, rad) to Cartesian position (m) and velocity (m/s)."""
        res = coe_to_rv(
            semi_major_axis_m,
            eccentricity,
            inclination_rad,
            raan_rad,
            arg_periapsis_rad,
            true_anomaly_rad,
            gravitational_parameter_m3_s2,
        )
        return build_result(
            calculation_name="convert_coe_to_eci",
            engineering_domain="astrodynamics",
            inputs={
                "semi_major_axis_m": semi_major_axis_m,
                "eccentricity": eccentricity,
                "inclination_rad": inclination_rad,
            },
            results=res,
            output_units={"position_m": "m", "velocity_m_s": "m/s"},
            equations=["Perifocal-to-ECI rotation"],
            assumptions=["Elliptic orbit, ECI frame"],
            model="Classical orbital elements transformation",
            validity_limits=["0 <= eccentricity < 1.0"],
        )

    @mcp.tool()
    def calculate_j2_perturbations(
        semi_major_axis_m: float,
        eccentricity: float,
        inclination_rad: float,
    ) -> dict:
        """Calculate Earth J2 secular rates of RAAN and argument of periapsis (rad/s)."""
        res = j2_secular_rates(semi_major_axis_m, eccentricity, inclination_rad)
        return build_result(
            calculation_name="calculate_j2_perturbations",
            engineering_domain="astrodynamics",
            inputs={
                "semi_major_axis_m": semi_major_axis_m,
                "eccentricity": eccentricity,
                "inclination_rad": inclination_rad,
            },
            results=res,
            output_units={
                "raan_rate_rad_s": "rad/s",
                "arg_periapsis_rate_rad_s": "rad/s",
            },
            equations=["dOmega/dt = -1.5 * n * J2 * (Re/p)^2 * cos(i)"],
            assumptions=["Secular J2 zonal harmonic only"],
            model="J2 secular perturbation theory",
            validity_limits=["0 <= eccentricity < 1.0"],
        )

    @mcp.tool()
    def calculate_hyperbolic_c3(v_inf_m_s: float) -> dict:
        """Calculate characteristic energy C3 (m^2/s^2) from hyperbolic excess speed (m/s)."""
        c3 = c3_energy(v_inf_m_s)
        v_inf = hyperbolic_excess_velocity(c3)
        return build_result(
            calculation_name="calculate_hyperbolic_c3",
            engineering_domain="astrodynamics",
            inputs={"v_inf_m_s": v_inf_m_s},
            results={"c3_m2_s2": c3, "v_inf_m_s": v_inf},
            output_units={"c3_m2_s2": "m^2/s^2", "v_inf_m_s": "m/s"},
            equations=["C3 = v_inf^2"],
            assumptions=["Two-body hyperbolic departure"],
            model="Hyperbolic excess energy",
            validity_limits=["v_inf_m_s >= 0"],
        )

    @mcp.tool()
    def calculate_periapsis_apoapsis(
        semi_major_axis_m: float, eccentricity: float
    ) -> dict:
        """Calculate periapsis and apoapsis radii (m) for an elliptic orbit."""
        res = periapsis_apoapsis(semi_major_axis_m, eccentricity)
        return build_result(
            calculation_name="calculate_periapsis_apoapsis",
            engineering_domain="astrodynamics",
            inputs={
                "semi_major_axis_m": semi_major_axis_m,
                "eccentricity": eccentricity,
            },
            results=res,
            output_units={"periapsis_radius_m": "m", "apoapsis_radius_m": "m"},
            equations=["rp = a*(1-e)", "ra = a*(1+e)"],
            assumptions=["Elliptic two-body orbit"],
            model="Keplerian apsides",
            validity_limits=["0 <= eccentricity < 1.0"],
        )

    @mcp.tool()
    def propagate_two_body_orbit(
        position_m: list[float],
        velocity_m_s: list[float],
        duration_s: float,
        time_step_s: float = 10.0,
    ) -> dict:
        """Propagate a two-body ECI Cartesian state using fixed-step RK4."""
        res = propagate_two_body_rk4(position_m, velocity_m_s, duration_s, time_step_s)
        return build_result(
            calculation_name="propagate_two_body_orbit",
            engineering_domain="astrodynamics",
            inputs={"duration_s": duration_s, "time_step_s": time_step_s},
            results=res,
            output_units={"final_position_m": "m", "final_velocity_m_s": "m/s"},
            equations=["d^2r/dt^2 = -mu * r / |r|^3"],
            assumptions=["Unperturbed two-body point-mass gravity"],
            model="Fixed-step RK4 two-body propagator",
            validity_limits=["duration_s > 0", "time_step_s > 0"],
        )
