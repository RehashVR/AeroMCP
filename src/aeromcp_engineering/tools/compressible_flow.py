"""MCP tools for compressible flow."""

from __future__ import annotations

from mcp.server import MCPServer

from aeromcp_engineering.compressible_flow import (
    area_mach_ratio,
    fanno_flow_ratios,
    inverse_prandtl_meyer,
    isentropic_ratios,
    normal_shock_relations,
    oblique_shock_relations,
    prandtl_meyer_angle,
    rayleigh_flow_ratios,
    solve_mach_from_area_ratio,
)
from aeromcp_engineering.core.constants import GAMMA_AIR
from aeromcp_engineering.core.results import build_result


def register_compressible_flow_tools(mcp: MCPServer) -> None:
    """Register compressible flow MCP tools."""

    @mcp.tool()
    def calculate_isentropic_ratios(mach: float, gamma: float = GAMMA_AIR) -> dict:
        """Calculate isentropic stagnation-to-static ratios T0/T, p0/p, rho0/rho."""
        res = isentropic_ratios(mach, gamma)
        return build_result(
            calculation_name="calculate_isentropic_ratios",
            engineering_domain="compressible_flow",
            inputs={"mach": mach, "gamma": gamma},
            results=res,
            output_units={
                "t0_over_t": "dimensionless",
                "p0_over_p": "dimensionless",
                "rho0_over_rho": "dimensionless",
            },
            equations=["T0/T = 1 + 0.5*(gamma-1)*M^2"],
            assumptions=["Adiabatic, reversible, calorically perfect ideal gas"],
            model="1D isentropic flow",
            validity_limits=["mach >= 0", "gamma > 1.0"],
        )

    @mcp.tool()
    def calculate_area_mach_ratio(mach: float, gamma: float = GAMMA_AIR) -> dict:
        """Calculate isentropic area ratio A/A* for a given Mach number."""
        ar = area_mach_ratio(mach, gamma)
        return build_result(
            calculation_name="calculate_area_mach_ratio",
            engineering_domain="compressible_flow",
            inputs={"mach": mach, "gamma": gamma},
            results={"area_ratio": ar},
            output_units={"area_ratio": "dimensionless"},
            equations=[
                "A/A* = (1/M)*((2/(gamma+1))*(1+0.5*(gamma-1)*M^2))^((gamma+1)/(2*(gamma-1)))"
            ],
            assumptions=["Isentropic quasi-1D flow"],
            model="Isentropic area-Mach relation",
            validity_limits=["mach > 0", "gamma > 1.0"],
        )

    @mcp.tool()
    def solve_mach_from_area_mach(
        area_ratio: float, branch: str = "supersonic", gamma: float = GAMMA_AIR
    ) -> dict:
        """Solve for subsonic or supersonic Mach number from area ratio A/A* >= 1.0."""
        m = solve_mach_from_area_ratio(area_ratio, branch, gamma)
        return build_result(
            calculation_name="solve_mach_from_area_mach",
            engineering_domain="compressible_flow",
            inputs={"area_ratio": area_ratio, "branch": branch, "gamma": gamma},
            results={"mach": m},
            output_units={"mach": "dimensionless"},
            equations=["Bisection inversion of A/A*(M)"],
            assumptions=["Isentropic quasi-1D flow"],
            model="Inverse area-Mach solver",
            validity_limits=[
                "area_ratio >= 1.0",
                "branch in {'subsonic', 'supersonic'}",
            ],
        )

    @mcp.tool()
    def calculate_normal_shock(upstream_mach: float, gamma: float = GAMMA_AIR) -> dict:
        """Calculate normal shock downstream Mach and property ratios (M1 >= 1.0)."""
        res = normal_shock_relations(upstream_mach, gamma)
        return build_result(
            calculation_name="calculate_normal_shock",
            engineering_domain="compressible_flow",
            inputs={"upstream_mach": upstream_mach, "gamma": gamma},
            results=res,
            output_units={
                "downstream_mach": "dimensionless",
                "p2_over_p1": "dimensionless",
            },
            equations=["Rankine-Hugoniot normal shock relations"],
            assumptions=["1D steady normal shock, calorically perfect ideal gas"],
            model="Normal shock relations",
            validity_limits=["upstream_mach >= 1.0", "gamma > 1.0"],
        )

    @mcp.tool()
    def calculate_oblique_shock(
        upstream_mach: float,
        deflection_angle_rad: float,
        branch: str = "weak",
        gamma: float = GAMMA_AIR,
    ) -> dict:
        """Calculate oblique shock wave angle and downstream properties (weak/strong)."""
        res = oblique_shock_relations(
            upstream_mach, deflection_angle_rad, branch, gamma
        )
        return build_result(
            calculation_name="calculate_oblique_shock",
            engineering_domain="compressible_flow",
            inputs={
                "upstream_mach": upstream_mach,
                "deflection_angle_rad": deflection_angle_rad,
                "branch": branch,
                "gamma": gamma,
            },
            results=res,
            output_units={"shock_angle_rad": "rad", "downstream_mach": "dimensionless"},
            equations=["theta-beta-M relation"],
            assumptions=[
                "2D steady attached oblique shock, calorically perfect ideal gas"
            ],
            model="Oblique shock relations",
            validity_limits=["upstream_mach > 1.0", "0 <= deflection <= theta_max"],
        )

    @mcp.tool()
    def calculate_prandtl_meyer(mach: float, gamma: float = GAMMA_AIR) -> dict:
        """Calculate Prandtl-Meyer expansion angle nu(M) in radians (M >= 1.0)."""
        nu = prandtl_meyer_angle(mach, gamma)
        return build_result(
            calculation_name="calculate_prandtl_meyer",
            engineering_domain="compressible_flow",
            inputs={"mach": mach, "gamma": gamma},
            results={"prandtl_meyer_angle_rad": nu},
            output_units={"prandtl_meyer_angle_rad": "rad"},
            equations=[
                "nu(M) = sqrt((g+1)/(g-1))*atan(sqrt((g-1)/(g+1)*(M^2-1))) - atan(sqrt(M^2-1))"
            ],
            assumptions=["Isentropic supersonic expansion"],
            model="Prandtl-Meyer function",
            validity_limits=["mach >= 1.0", "gamma > 1.0"],
        )

    @mcp.tool()
    def solve_inverse_prandtl_meyer(nu_rad: float, gamma: float = GAMMA_AIR) -> dict:
        """Solve for supersonic Mach number from Prandtl-Meyer angle nu (rad)."""
        m = inverse_prandtl_meyer(nu_rad, gamma)
        return build_result(
            calculation_name="solve_inverse_prandtl_meyer",
            engineering_domain="compressible_flow",
            inputs={"nu_rad": nu_rad, "gamma": gamma},
            results={"mach": m},
            output_units={"mach": "dimensionless"},
            equations=["Bisection inversion of nu(M)"],
            assumptions=["Isentropic supersonic expansion"],
            model="Inverse Prandtl-Meyer solver",
            validity_limits=["0 <= nu_rad < nu_max"],
        )

    @mcp.tool()
    def calculate_fanno_flow(mach: float, gamma: float = GAMMA_AIR) -> dict:
        """Calculate Fanno flow sonic reference ratios and 4fL*/D."""
        res = fanno_flow_ratios(mach, gamma)
        return build_result(
            calculation_name="calculate_fanno_flow",
            engineering_domain="compressible_flow",
            inputs={"mach": mach, "gamma": gamma},
            results=res,
            output_units={"four_f_lstar_over_d": "dimensionless"},
            equations=["Fanno flow adiabatic frictional duct relations"],
            assumptions=["1D adiabatic constant-area duct with friction"],
            model="Fanno flow",
            validity_limits=["mach > 0", "gamma > 1.0"],
        )

    @mcp.tool()
    def calculate_rayleigh_flow(mach: float, gamma: float = GAMMA_AIR) -> dict:
        """Calculate Rayleigh flow sonic reference ratios."""
        res = rayleigh_flow_ratios(mach, gamma)
        return build_result(
            calculation_name="calculate_rayleigh_flow",
            engineering_domain="compressible_flow",
            inputs={"mach": mach, "gamma": gamma},
            results=res,
            output_units={"p_over_pstar": "dimensionless"},
            equations=["Rayleigh flow frictionless diabatic duct relations"],
            assumptions=["1D frictionless constant-area duct with heat addition"],
            model="Rayleigh flow",
            validity_limits=["mach > 0", "gamma > 1.0"],
        )
