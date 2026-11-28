"""Modular MCP tool registration for all AeroMCP engineering domains."""

from __future__ import annotations

from mcp.server import MCPServer

from aeromcp_engineering.tools.aerodynamics import register_aerodynamics_tools
from aeromcp_engineering.tools.aircraft_design import register_aircraft_design_tools
from aeromcp_engineering.tools.astrodynamics import register_astrodynamics_tools
from aeromcp_engineering.tools.atmosphere import register_atmosphere_tools
from aeromcp_engineering.tools.compressible_flow import register_compressible_flow_tools
from aeromcp_engineering.tools.flight_mechanics import register_flight_mechanics_tools
from aeromcp_engineering.tools.gnc import register_gnc_tools
from aeromcp_engineering.tools.mission_analysis import register_mission_analysis_tools
from aeromcp_engineering.tools.propulsion import register_propulsion_tools
from aeromcp_engineering.tools.structures import register_structures_tools
from aeromcp_engineering.tools.thermal import register_thermal_tools


def register_all_domain_tools(mcp: MCPServer) -> None:
    """Register all v0.3.0 domain tools on the given MCPServer."""
    register_aerodynamics_tools(mcp)
    register_atmosphere_tools(mcp)
    register_compressible_flow_tools(mcp)
    register_propulsion_tools(mcp)
    register_astrodynamics_tools(mcp)
    register_flight_mechanics_tools(mcp)
    register_structures_tools(mcp)
    register_thermal_tools(mcp)
    register_gnc_tools(mcp)
    register_aircraft_design_tools(mcp)
    register_mission_analysis_tools(mcp)
