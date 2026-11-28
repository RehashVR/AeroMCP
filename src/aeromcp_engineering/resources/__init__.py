"""MCP resources for AeroMCP capabilities, domains, constants, units, and models."""

from __future__ import annotations

import json

from mcp.server import MCPServer

from aeromcp_engineering.core.constants import (
    G0_M_S2,
    GAMMA_AIR,
    J2_EARTH,
    MU_EARTH_M3_S2,
    P0_PA,
    R_AIR_J_KG_K,
    R_EARTH_EQUATORIAL_M,
    R_EARTH_MEAN_M,
    R_UNIVERSAL_J_MOL_K,
    RHO0_KG_M3,
    STEFAN_BOLTZMANN_W_M2_K4,
    T0_K,
    WGS84_A_M,
    WGS84_F,
)


def register_resources(mcp: MCPServer) -> None:
    """Register AeroMCP engineering reference resources."""

    @mcp.resource("aeromcp://capabilities")
    def get_capabilities() -> str:
        """Overview of AeroMCP v0.3.0 capabilities and boundaries."""
        return json.dumps(
            {
                "name": "AeroMCP",
                "version": "0.3.0",
                "package": "aeromcp-engineering",
                "namespace": "aeromcp_engineering",
                "transport": "STDIO",
                "units": "SI",
                "boundaries": (
                    "Analytical and preliminary-design aerospace engineering models. "
                    "Not a substitute for CFD, FEA, 6-DOF simulators, or certified avionics."
                ),
            },
            indent=2,
        )

    @mcp.resource("aeromcp://engineering-domains")
    def get_engineering_domains() -> str:
        """List of supported aerospace engineering domains."""
        return json.dumps(
            {
                "domains": [
                    "aerodynamics",
                    "atmosphere",
                    "compressible_flow",
                    "propulsion",
                    "astrodynamics",
                    "flight_mechanics",
                    "structures",
                    "thermal",
                    "gnc",
                    "aircraft_design",
                    "mission_analysis",
                ]
            },
            indent=2,
        )

    @mcp.resource("aeromcp://constants")
    def get_constants() -> str:
        """Standard SI physical and aerospace constants used by AeroMCP."""
        return json.dumps(
            {
                "G0_M_S2": G0_M_S2,
                "R_UNIVERSAL_J_MOL_K": R_UNIVERSAL_J_MOL_K,
                "R_AIR_J_KG_K": R_AIR_J_KG_K,
                "GAMMA_AIR": GAMMA_AIR,
                "P0_PA": P0_PA,
                "T0_K": T0_K,
                "RHO0_KG_M3": RHO0_KG_M3,
                "STEFAN_BOLTZMANN_W_M2_K4": STEFAN_BOLTZMANN_W_M2_K4,
                "MU_EARTH_M3_S2": MU_EARTH_M3_S2,
                "R_EARTH_MEAN_M": R_EARTH_MEAN_M,
                "R_EARTH_EQUATORIAL_M": R_EARTH_EQUATORIAL_M,
                "J2_EARTH": J2_EARTH,
                "WGS84_A_M": WGS84_A_M,
                "WGS84_F": WGS84_F,
            },
            indent=2,
        )

    @mcp.resource("aeromcp://units")
    def get_units() -> str:
        """SI unit conventions for AeroMCP."""
        return json.dumps(
            {
                "length": "m",
                "velocity": "m/s",
                "mass": "kg",
                "force": "N",
                "pressure": "Pa",
                "temperature": "K",
                "density": "kg/m^3",
                "power": "W",
                "energy": "J",
                "angle": "rad",
                "time": "s",
            },
            indent=2,
        )

    @mcp.resource("aeromcp://model-catalog")
    def get_model_catalog() -> str:
        """Catalog of implemented analytical and numerical models."""
        return json.dumps(
            {
                "atmosphere": "U.S. Standard Atmosphere 1976 (0 to 84,852 m geopotential)",
                "compressible_flow": "1D Isentropic, Normal/Oblique Shock, Prandtl-Meyer, Fanno, Rayleigh",
                "propulsion": "Tsiolkovsky Rocket, Choked/CD Nozzle, Ideal Turbojet, Actuator Disk, Rotor Hover",
                "astrodynamics": "Keplerian Two-Body, Kepler Solver, COE->ECI, J2 Secular, RK4 Propagator",
                "flight_mechanics": "Coordinated Turn, Climb/Glide, Breguet Range/Endurance, Static Margin",
                "structures": "Axial Bar, Euler-Bernoulli Beams, Torsion, Euler Buckling, Von Mises, Pressure Vessel",
                "thermal": "1D Conduction, Convection, Radiation, Recovery Temp, Sutton-Graves",
                "gnc": "WGS-84 Geodetic/ECEF, Quaternions/ZYX Euler, Discrete PID, Scalar Kalman",
                "aircraft_design": "Preliminary Wing Sizing, T/W, P/W, Electric UAV Endurance",
                "mission_analysis": "1D RK4 Vertical Ascent, Mission Delta-V Budget",
            },
            indent=2,
        )
