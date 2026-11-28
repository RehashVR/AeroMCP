"""MCP tools for mission analysis and trajectory."""

from __future__ import annotations

from mcp.server import MCPServer

from aeromcp_engineering.core.results import build_result
from aeromcp_engineering.mission_analysis import (
    mission_delta_v_budget,
    vertical_rocket_ascent_rk4,
)


def register_mission_analysis_tools(mcp: MCPServer) -> None:
    """Register mission analysis and trajectory MCP tools."""

    @mcp.tool()
    def simulate_vertical_rocket_ascent(
        initial_mass_kg: float,
        propellant_mass_kg: float,
        thrust_n: float,
        mass_flow_kg_s: float,
        burn_time_s: float,
        time_step_s: float = 0.1,
        drag_area_cd_s_m2: float = 0.0,
        air_density_kg_m3: float = 0.0,
    ) -> dict:
        """Simulate 1D vertical rocket ascent during burn using fixed-step RK4."""
        res = vertical_rocket_ascent_rk4(
            initial_mass_kg,
            propellant_mass_kg,
            thrust_n,
            mass_flow_kg_s,
            burn_time_s,
            time_step_s,
            drag_area_cd_s_m2,
            air_density_kg_m3,
        )
        return build_result(
            calculation_name="simulate_vertical_rocket_ascent",
            engineering_domain="mission_analysis",
            inputs={
                "initial_mass_kg": initial_mass_kg,
                "propellant_mass_kg": propellant_mass_kg,
                "thrust_n": thrust_n,
                "burn_time_s": burn_time_s,
            },
            results=res,
            output_units={
                "burnout_time_s": "s",
                "burnout_altitude_m": "m",
                "burnout_velocity_m_s": "m/s",
                "burnout_mass_kg": "kg",
            },
            equations=["dv/dt = (T - D)/m - g0", "dh/dt = v", "dm/dt = -m_dot"],
            assumptions=["1D vertical ascent, constant g0, constant thrust"],
            model="1D RK4 vertical ascent",
            validity_limits=[
                "propellant_mass_kg < initial_mass_kg",
                "m_dot * burn_time <= propellant_mass",
            ],
        )

    @mcp.tool()
    def calculate_mission_delta_v_budget(
        maneuver_delta_vs_m_s: list[float],
        margin_fraction: float = 0.05,
    ) -> dict:
        """Sum mission maneuver delta-Vs (m/s) and apply a fractional margin."""
        res = mission_delta_v_budget(maneuver_delta_vs_m_s, margin_fraction)
        return build_result(
            calculation_name="calculate_mission_delta_v_budget",
            engineering_domain="mission_analysis",
            inputs={
                "maneuver_delta_vs_m_s": maneuver_delta_vs_m_s,
                "margin_fraction": margin_fraction,
            },
            results=res,
            output_units={
                "nominal_delta_v_m_s": "m/s",
                "total_budget_delta_v_m_s": "m/s",
            },
            equations=["dV_total = sum(dV_i) * (1 + margin)"],
            assumptions=["Linear sum of impulsive maneuvers"],
            model="Mission delta-V budget",
            validity_limits=["All delta-Vs >= 0", "margin_fraction >= 0"],
        )
