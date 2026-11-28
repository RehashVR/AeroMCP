"""MCP tools for aerodynamics (new v0.3.0 tools)."""

from __future__ import annotations

from mcp.server import MCPServer

from aeromcp_engineering.aerodynamics import (
    aerodynamic_force_decomposition,
    aspect_ratio,
    finite_wing_lift_slope,
    induced_drag_coefficient,
    induced_drag_force,
    lift_to_drag_ratio,
    mach_number,
    stall_speed,
    thin_airfoil_lift_coefficient,
    wing_loading,
)
from aeromcp_engineering.core.results import build_result


def register_aerodynamics_tools(mcp: MCPServer) -> None:
    """Register expanded aerodynamics MCP tools."""

    @mcp.tool()
    def calculate_mach_number(velocity_m_s: float, speed_of_sound_m_s: float) -> dict:
        """Calculate Mach number M = V / a (SI units: m/s)."""
        m = mach_number(velocity_m_s, speed_of_sound_m_s)
        return build_result(
            calculation_name="calculate_mach_number",
            engineering_domain="aerodynamics",
            inputs={
                "velocity_m_s": velocity_m_s,
                "speed_of_sound_m_s": speed_of_sound_m_s,
            },
            results={"mach_number": m},
            output_units={"mach_number": "dimensionless"},
            equations=["M = V / a"],
            assumptions=["Continuum gas flow"],
            model="1D Mach definition",
            validity_limits=["speed_of_sound_m_s > 0"],
        )

    @mcp.tool()
    def calculate_lift_to_drag_ratio(lift_n: float, drag_n: float) -> dict:
        """Calculate aerodynamic lift-to-drag ratio L/D (inputs in N)."""
        ld = lift_to_drag_ratio(lift_n, drag_n)
        return build_result(
            calculation_name="calculate_lift_to_drag_ratio",
            engineering_domain="aerodynamics",
            inputs={"lift_n": lift_n, "drag_n": drag_n},
            results={"lift_to_drag_ratio": ld},
            output_units={"lift_to_drag_ratio": "dimensionless"},
            equations=["L/D = L / D"],
            assumptions=["Steady aerodynamic forces"],
            model="Aerodynamic efficiency ratio",
            validity_limits=["drag_n > 0"],
        )

    @mcp.tool()
    def calculate_wing_loading(weight_n: float, wing_area_m2: float) -> dict:
        """Calculate wing loading W/S in N/m^2 (Pa)."""
        ws = wing_loading(weight_n, wing_area_m2)
        return build_result(
            calculation_name="calculate_wing_loading",
            engineering_domain="aerodynamics",
            inputs={"weight_n": weight_n, "wing_area_m2": wing_area_m2},
            results={"wing_loading_n_m2": ws},
            output_units={"wing_loading_n_m2": "N/m^2"},
            equations=["W/S = W / S"],
            assumptions=["Reference wing planform area S"],
            model="Wing loading definition",
            validity_limits=["weight_n > 0", "wing_area_m2 > 0"],
        )

    @mcp.tool()
    def calculate_aspect_ratio(wingspan_m: float, wing_area_m2: float) -> dict:
        """Calculate wing aspect ratio AR = b^2 / S (inputs in m, m^2)."""
        ar = aspect_ratio(wingspan_m, wing_area_m2)
        return build_result(
            calculation_name="calculate_aspect_ratio",
            engineering_domain="aerodynamics",
            inputs={"wingspan_m": wingspan_m, "wing_area_m2": wing_area_m2},
            results={"aspect_ratio": ar},
            output_units={"aspect_ratio": "dimensionless"},
            equations=["AR = b^2 / S"],
            assumptions=["Planar wing geometry"],
            model="Geometric aspect ratio",
            validity_limits=["wingspan_m > 0", "wing_area_m2 > 0"],
        )

    @mcp.tool()
    def calculate_induced_drag(
        density_kg_m3: float,
        velocity_m_s: float,
        wing_area_m2: float,
        lift_coefficient: float,
        aspect_ratio_val: float,
        oswald_efficiency: float = 0.85,
    ) -> dict:
        """Calculate induced drag coefficient CDi and force Di (N)."""
        cdi = induced_drag_coefficient(
            lift_coefficient, aspect_ratio_val, oswald_efficiency
        )
        di = induced_drag_force(
            density_kg_m3,
            velocity_m_s,
            wing_area_m2,
            lift_coefficient,
            aspect_ratio_val,
            oswald_efficiency,
        )
        return build_result(
            calculation_name="calculate_induced_drag",
            engineering_domain="aerodynamics",
            inputs={
                "density_kg_m3": density_kg_m3,
                "velocity_m_s": velocity_m_s,
                "wing_area_m2": wing_area_m2,
                "lift_coefficient": lift_coefficient,
                "aspect_ratio_val": aspect_ratio_val,
                "oswald_efficiency": oswald_efficiency,
            },
            results={"induced_drag_coefficient": cdi, "induced_drag_n": di},
            output_units={
                "induced_drag_coefficient": "dimensionless",
                "induced_drag_n": "N",
            },
            equations=["CDi = CL^2 / (pi * AR * e)", "Di = 0.5 * rho * V^2 * S * CDi"],
            assumptions=["Subsonic attached flow", "Parabolic drag polar"],
            model="Prandtl lifting-line induced drag",
            validity_limits=["0 < oswald_efficiency <= 1.0"],
        )

    @mcp.tool()
    def calculate_stall_speed(
        weight_n: float,
        density_kg_m3: float,
        wing_area_m2: float,
        cl_max: float,
    ) -> dict:
        """Calculate steady level-flight stall speed Vs in m/s."""
        vs = stall_speed(weight_n, density_kg_m3, wing_area_m2, cl_max)
        return build_result(
            calculation_name="calculate_stall_speed",
            engineering_domain="aerodynamics",
            inputs={
                "weight_n": weight_n,
                "density_kg_m3": density_kg_m3,
                "wing_area_m2": wing_area_m2,
                "cl_max": cl_max,
            },
            results={"stall_speed_m_s": vs},
            output_units={"stall_speed_m_s": "m/s"},
            equations=["Vs = sqrt(2*W / (rho * S * CLmax))"],
            assumptions=["1g steady level flight", "Incompressible"],
            model="Level-flight stall speed",
            validity_limits=["All inputs > 0"],
        )

    @mcp.tool()
    def calculate_finite_wing_lift_slope(
        airfoil_lift_slope_per_rad: float,
        aspect_ratio_val: float,
        oswald_efficiency: float = 0.95,
    ) -> dict:
        """Calculate finite-wing lift-curve slope (per rad) from 2D airfoil slope."""
        slope = finite_wing_lift_slope(
            airfoil_lift_slope_per_rad, aspect_ratio_val, oswald_efficiency
        )
        return build_result(
            calculation_name="calculate_finite_wing_lift_slope",
            engineering_domain="aerodynamics",
            inputs={
                "airfoil_lift_slope_per_rad": airfoil_lift_slope_per_rad,
                "aspect_ratio_val": aspect_ratio_val,
                "oswald_efficiency": oswald_efficiency,
            },
            results={"finite_wing_lift_slope_per_rad": slope},
            output_units={"finite_wing_lift_slope_per_rad": "1/rad"},
            equations=["a = a0 / (1 + a0 / (pi * AR * e))"],
            assumptions=["Unswept high-AR wing", "Subsonic incompressible"],
            model="Prandtl lifting-line theory",
            validity_limits=["0 < oswald_efficiency <= 1.0"],
        )

    @mcp.tool()
    def calculate_thin_airfoil_lift(
        angle_of_attack_rad: float,
        zero_lift_angle_rad: float = 0.0,
    ) -> dict:
        """Estimate 2D thin-airfoil lift coefficient cl = 2*pi*(alpha - alpha_0)."""
        cl = thin_airfoil_lift_coefficient(angle_of_attack_rad, zero_lift_angle_rad)
        return build_result(
            calculation_name="calculate_thin_airfoil_lift",
            engineering_domain="aerodynamics",
            inputs={
                "angle_of_attack_rad": angle_of_attack_rad,
                "zero_lift_angle_rad": zero_lift_angle_rad,
            },
            results={"lift_coefficient_2d": cl},
            output_units={"lift_coefficient_2d": "dimensionless"},
            equations=["cl = 2 * pi * (alpha - alpha_0)"],
            assumptions=["Inviscid, incompressible, 2D thin airfoil, small alpha"],
            model="Thin-airfoil theory",
            validity_limits=["Small angles of attack; does not predict stall"],
        )

    @mcp.tool()
    def decompose_aerodynamic_forces(
        normal_force_n: float,
        axial_force_n: float,
        angle_of_attack_rad: float,
    ) -> dict:
        """Decompose body-frame normal and axial forces (N) into Lift and Drag (N)."""
        res = aerodynamic_force_decomposition(
            normal_force_n, axial_force_n, angle_of_attack_rad
        )
        return build_result(
            calculation_name="decompose_aerodynamic_forces",
            engineering_domain="aerodynamics",
            inputs={
                "normal_force_n": normal_force_n,
                "axial_force_n": axial_force_n,
                "angle_of_attack_rad": angle_of_attack_rad,
            },
            results=res,
            output_units={"lift_n": "N", "drag_n": "N"},
            equations=[
                "L = N*cos(alpha) - A*sin(alpha)",
                "D = N*sin(alpha) + A*cos(alpha)",
            ],
            assumptions=["2D body-to-wind axis rotation"],
            model="Aerodynamic force decomposition",
            validity_limits=["Finite inputs"],
        )
