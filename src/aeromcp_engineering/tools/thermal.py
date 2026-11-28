"""MCP tools for aerospace thermal engineering."""

from __future__ import annotations

from mcp.server import MCPServer

from aeromcp_engineering.core.results import build_result
from aeromcp_engineering.thermal import (
    conduction_1d_heat_rate,
    convection_heat_rate,
    radiation_heat_rate,
    stagnation_and_recovery_temperature,
    sutton_graves_stagnation_heat_flux,
)


def register_thermal_tools(mcp: MCPServer) -> None:
    """Register aerospace thermal engineering MCP tools."""

    @mcp.tool()
    def calculate_1d_conduction(
        thermal_conductivity_w_m_k: float,
        area_m2: float,
        delta_temperature_k: float,
        thickness_m: float,
    ) -> dict:
        """Calculate 1D steady-state conduction heat rate (W)."""
        q = conduction_1d_heat_rate(
            thermal_conductivity_w_m_k, area_m2, delta_temperature_k, thickness_m
        )
        return build_result(
            calculation_name="calculate_1d_conduction",
            engineering_domain="thermal",
            inputs={
                "thermal_conductivity_w_m_k": thermal_conductivity_w_m_k,
                "area_m2": area_m2,
                "thickness_m": thickness_m,
            },
            results={"heat_rate_w": q},
            output_units={"heat_rate_w": "W"},
            equations=["Q = k * A * dT / L"],
            assumptions=["1D steady-state conduction, constant k"],
            model="Fourier's law of conduction",
            validity_limits=["k > 0", "area_m2 > 0", "thickness_m > 0"],
        )

    @mcp.tool()
    def calculate_convection_heat_rate(
        heat_transfer_coeff_w_m2_k: float,
        area_m2: float,
        surface_temperature_k: float,
        fluid_temperature_k: float,
    ) -> dict:
        """Calculate convective heat transfer rate (W) using Newton's law of cooling."""
        q = convection_heat_rate(
            heat_transfer_coeff_w_m2_k,
            area_m2,
            surface_temperature_k,
            fluid_temperature_k,
        )
        return build_result(
            calculation_name="calculate_convection_heat_rate",
            engineering_domain="thermal",
            inputs={
                "heat_transfer_coeff_w_m2_k": heat_transfer_coeff_w_m2_k,
                "area_m2": area_m2,
            },
            results={"heat_rate_w": q},
            output_units={"heat_rate_w": "W"},
            equations=["Q = h * A * (Ts - Tinf)"],
            assumptions=["Uniform surface and fluid temperatures"],
            model="Newton's law of cooling",
            validity_limits=["h > 0", "area_m2 > 0"],
        )

    @mcp.tool()
    def calculate_radiation_heat_rate(
        emissivity: float,
        area_m2: float,
        surface_temperature_k: float,
        surroundings_temperature_k: float = 0.0,
    ) -> dict:
        """Calculate net radiative heat transfer rate (W) using Stefan-Boltzmann law."""
        q = radiation_heat_rate(
            emissivity, area_m2, surface_temperature_k, surroundings_temperature_k
        )
        return build_result(
            calculation_name="calculate_radiation_heat_rate",
            engineering_domain="thermal",
            inputs={
                "emissivity": emissivity,
                "area_m2": area_m2,
                "surface_temperature_k": surface_temperature_k,
            },
            results={"heat_rate_w": q},
            output_units={"heat_rate_w": "W"},
            equations=["Q = eps * sigma * A * (Ts^4 - Tsurr^4)"],
            assumptions=["Gray diffuse surface in large enclosure"],
            model="Stefan-Boltzmann radiation",
            validity_limits=["0 < emissivity <= 1.0", "Temperatures >= 0 K"],
        )

    @mcp.tool()
    def calculate_recovery_temperature(
        static_temperature_k: float,
        mach: float,
        recovery_factor: float = 0.85,
    ) -> dict:
        """Calculate stagnation and adiabatic wall recovery temperature (K)."""
        res = stagnation_and_recovery_temperature(
            static_temperature_k, mach, recovery_factor
        )
        return build_result(
            calculation_name="calculate_recovery_temperature",
            engineering_domain="thermal",
            inputs={
                "static_temperature_k": static_temperature_k,
                "mach": mach,
                "recovery_factor": recovery_factor,
            },
            results=res,
            output_units={
                "stagnation_temperature_k": "K",
                "recovery_temperature_k": "K",
            },
            equations=["Tr = Tinf * (1 + r * 0.5*(gamma-1)*M^2)"],
            assumptions=["Calorically perfect ideal gas"],
            model="Aerodynamic recovery temperature",
            validity_limits=["0 <= recovery_factor <= 1.0", "mach >= 0"],
        )

    @mcp.tool()
    def calculate_sutton_graves_heating(
        density_kg_m3: float,
        velocity_m_s: float,
        nose_radius_m: float,
    ) -> dict:
        """Estimate stagnation-point convective heat flux (W/m^2) via Sutton-Graves correlation."""
        q_dot = sutton_graves_stagnation_heat_flux(
            density_kg_m3, velocity_m_s, nose_radius_m
        )
        return build_result(
            calculation_name="calculate_sutton_graves_heating",
            engineering_domain="thermal",
            inputs={
                "density_kg_m3": density_kg_m3,
                "velocity_m_s": velocity_m_s,
                "nose_radius_m": nose_radius_m,
            },
            results={"stagnation_heat_flux_w_m2": q_dot},
            output_units={"stagnation_heat_flux_w_m2": "W/m^2"},
            equations=["q_dot = k_SG * sqrt(rho / Rn) * V^3"],
            assumptions=["Earth air, preliminary stagnation-point correlation"],
            model="Sutton-Graves correlation",
            validity_limits=["density_kg_m3 > 0", "nose_radius_m > 0"],
        )
