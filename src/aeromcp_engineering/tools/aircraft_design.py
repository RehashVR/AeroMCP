"""MCP tools for aircraft and UAV preliminary design."""

from __future__ import annotations

from mcp.server import MCPServer

from aeromcp_engineering.aircraft_design import (
    electric_uav_endurance,
    power_to_weight_ratio,
    rectangular_wing_mac,
    thrust_to_weight_ratio,
    wing_area_from_loading,
    wingspan_from_aspect_ratio,
)
from aeromcp_engineering.core.results import build_result


def register_aircraft_design_tools(mcp: MCPServer) -> None:
    """Register aircraft and UAV preliminary design MCP tools."""

    @mcp.tool()
    def size_wing_geometry(
        weight_n: float,
        wing_loading_n_m2: float,
        aspect_ratio_val: float,
    ) -> dict:
        """Size preliminary wing area (m^2), wingspan (m), and rectangular MAC (m)."""
        s = wing_area_from_loading(weight_n, wing_loading_n_m2)
        b = wingspan_from_aspect_ratio(aspect_ratio_val, s)
        mac = rectangular_wing_mac(s, b)
        return build_result(
            calculation_name="size_wing_geometry",
            engineering_domain="aircraft_design",
            inputs={
                "weight_n": weight_n,
                "wing_loading_n_m2": wing_loading_n_m2,
                "aspect_ratio_val": aspect_ratio_val,
            },
            results={
                "wing_area_m2": s,
                "wingspan_m": b,
                "mean_aerodynamic_chord_m": mac,
            },
            output_units={
                "wing_area_m2": "m^2",
                "wingspan_m": "m",
                "mean_aerodynamic_chord_m": "m",
            },
            equations=["S = W / (W/S)", "b = sqrt(AR * S)", "MAC = S / b"],
            assumptions=["Conceptual rectangular-wing sizing"],
            model="Preliminary wing sizing",
            validity_limits=["All inputs > 0"],
        )

    @mcp.tool()
    def calculate_thrust_and_power_to_weight(
        thrust_n: float, power_w: float, weight_n: float
    ) -> dict:
        """Calculate thrust-to-weight ratio T/W and power-to-weight ratio P/W (W/N)."""
        tw = thrust_to_weight_ratio(thrust_n, weight_n)
        pw = power_to_weight_ratio(power_w, weight_n)
        return build_result(
            calculation_name="calculate_thrust_and_power_to_weight",
            engineering_domain="aircraft_design",
            inputs={"thrust_n": thrust_n, "power_w": power_w, "weight_n": weight_n},
            results={"thrust_to_weight": tw, "power_to_weight_w_n": pw},
            output_units={
                "thrust_to_weight": "dimensionless",
                "power_to_weight_w_n": "W/N",
            },
            equations=["T/W = T / W", "P/W = P / W"],
            assumptions=["Conceptual sizing ratios"],
            model="Preliminary propulsion-to-weight sizing",
            validity_limits=["All inputs > 0"],
        )

    @mcp.tool()
    def estimate_electric_uav_endurance(
        battery_energy_wh: float,
        usable_fraction: float,
        power_draw_w: float,
        propulsion_efficiency: float = 0.75,
    ) -> dict:
        """Estimate electric UAV endurance (s and hr) from battery energy and power draw."""
        res = electric_uav_endurance(
            battery_energy_wh, usable_fraction, power_draw_w, propulsion_efficiency
        )
        return build_result(
            calculation_name="estimate_electric_uav_endurance",
            engineering_domain="aircraft_design",
            inputs={
                "battery_energy_wh": battery_energy_wh,
                "usable_fraction": usable_fraction,
                "power_draw_w": power_draw_w,
            },
            results=res,
            output_units={
                "usable_energy_j": "J",
                "endurance_s": "s",
                "endurance_hr": "hr",
            },
            equations=["t = (E_wh * 3600 * f_usable * eta) / P_draw"],
            assumptions=["Constant average power draw"],
            model="Electric UAV energy-endurance estimate",
            validity_limits=[
                "0 < usable_fraction <= 1.0",
                "0 < propulsion_efficiency <= 1.0",
            ],
        )
