"""MCP tools for atmospheric science (new v0.3.0 tools)."""

from __future__ import annotations

from mcp.server import MCPServer

from aeromcp_engineering.atmosphere import (
    density_altitude,
    isa_atmosphere,
    mach_atmospheric_properties,
    sutherland_viscosity,
)
from aeromcp_engineering.core.results import build_result


def register_atmosphere_tools(mcp: MCPServer) -> None:
    """Register expanded atmospheric science MCP tools."""

    @mcp.tool()
    def calculate_isa_atmosphere(altitude_m: float) -> dict:
        """Calculate U.S. Standard Atmosphere 1976 properties up to 84,852 m geopotential."""
        res = isa_atmosphere(altitude_m)
        return build_result(
            calculation_name="calculate_isa_atmosphere",
            engineering_domain="atmosphere",
            inputs={"altitude_m": altitude_m},
            results=res,
            output_units={
                "geometric_altitude_m": "m",
                "geopotential_altitude_m": "m",
                "temperature_k": "K",
                "pressure_pa": "Pa",
                "density_kg_m3": "kg/m^3",
                "speed_of_sound_m_s": "m/s",
                "dynamic_viscosity_pa_s": "Pa*s",
                "kinematic_viscosity_m2_s": "m^2/s",
            },
            equations=["Hydrostatic equilibrium + ideal gas law + Sutherland's law"],
            assumptions=["Dry air, ideal gas, hydrostatic equilibrium"],
            model="U.S. Standard Atmosphere 1976",
            validity_limits=["0 <= geopotential_altitude_m <= 84852 m"],
        )

    @mcp.tool()
    def calculate_sutherland_viscosity(temperature_k: float) -> dict:
        """Calculate dynamic viscosity of air (Pa*s) using Sutherland's law."""
        mu = sutherland_viscosity(temperature_k)
        return build_result(
            calculation_name="calculate_sutherland_viscosity",
            engineering_domain="atmosphere",
            inputs={"temperature_k": temperature_k},
            results={"dynamic_viscosity_pa_s": mu},
            output_units={"dynamic_viscosity_pa_s": "Pa*s"},
            equations=["mu = mu0 * (T/T0)^1.5 * (T0 + S)/(T + S)"],
            assumptions=["Dry air"],
            model="Sutherland's law",
            validity_limits=["temperature_k > 0"],
        )

    @mcp.tool()
    def calculate_mach_atmospheric_properties(
        altitude_m: float, velocity_m_s: float
    ) -> dict:
        """Calculate ISA 1976 properties, Mach number, and dynamic pressure at altitude."""
        res = mach_atmospheric_properties(altitude_m, velocity_m_s)
        return build_result(
            calculation_name="calculate_mach_atmospheric_properties",
            engineering_domain="atmosphere",
            inputs={"altitude_m": altitude_m, "velocity_m_s": velocity_m_s},
            results=res,
            output_units={
                "temperature_k": "K",
                "pressure_pa": "Pa",
                "density_kg_m3": "kg/m^3",
                "speed_of_sound_m_s": "m/s",
                "mach_number": "dimensionless",
                "dynamic_pressure_pa": "Pa",
            },
            equations=["M = V / a", "q = 0.5 * rho * V^2"],
            assumptions=["U.S. Standard Atmosphere 1976"],
            model="ISA 1976 + Mach/dynamic pressure",
            validity_limits=[
                "0 <= geopotential_altitude_m <= 84852 m",
                "velocity_m_s >= 0",
            ],
        )

    @mcp.tool()
    def calculate_density_altitude(density_kg_m3: float) -> dict:
        """Calculate ISA troposphere density altitude (m) from air density (kg/m^3)."""
        h = density_altitude(density_kg_m3)
        return build_result(
            calculation_name="calculate_density_altitude",
            engineering_domain="atmosphere",
            inputs={"density_kg_m3": density_kg_m3},
            results={"density_altitude_m": h},
            output_units={"density_altitude_m": "m"},
            equations=["ISA troposphere density-altitude inversion"],
            assumptions=["Standard troposphere lapse rate -0.0065 K/m"],
            model="ISA Troposphere",
            validity_limits=["-1000 m <= h <= 11000 m"],
        )
