"""MCP tools for aerospace structures."""

from __future__ import annotations

from mcp.server import MCPServer

from aeromcp_engineering.core.results import build_result
from aeromcp_engineering.structures import (
    axial_bar_analysis,
    beam_bending_stress,
    cantilever_tip_deflection,
    circular_shaft_torsion,
    euler_buckling_load,
    simply_supported_center_deflection,
    thin_walled_pressure_vessel,
    von_mises_stress_2d,
)


def register_structures_tools(mcp: MCPServer) -> None:
    """Register aerospace structures MCP tools."""

    @mcp.tool()
    def calculate_axial_bar(
        force_n: float, area_m2: float, length_m: float, youngs_modulus_pa: float
    ) -> dict:
        """Calculate axial stress (Pa), strain, and elongation (m)."""
        res = axial_bar_analysis(force_n, area_m2, length_m, youngs_modulus_pa)
        return build_result(
            calculation_name="calculate_axial_bar",
            engineering_domain="structures",
            inputs={
                "force_n": force_n,
                "area_m2": area_m2,
                "length_m": length_m,
                "youngs_modulus_pa": youngs_modulus_pa,
            },
            results=res,
            output_units={
                "axial_stress_pa": "Pa",
                "axial_strain": "dimensionless",
                "elongation_m": "m",
            },
            equations=["sigma = F/A", "delta = F*L/(E*A)"],
            assumptions=["Linear-elastic, uniform prismatic bar"],
            model="1D axial bar",
            validity_limits=["area_m2 > 0", "length_m > 0", "youngs_modulus_pa > 0"],
        )

    @mcp.tool()
    def calculate_beam_bending_stress(
        bending_moment_n_m: float,
        distance_from_neutral_axis_m: float,
        second_moment_of_area_m4: float,
    ) -> dict:
        """Calculate Euler-Bernoulli beam bending stress (Pa)."""
        s = beam_bending_stress(
            bending_moment_n_m, distance_from_neutral_axis_m, second_moment_of_area_m4
        )
        return build_result(
            calculation_name="calculate_beam_bending_stress",
            engineering_domain="structures",
            inputs={
                "bending_moment_n_m": bending_moment_n_m,
                "distance_from_neutral_axis_m": distance_from_neutral_axis_m,
                "second_moment_of_area_m4": second_moment_of_area_m4,
            },
            results={"bending_stress_pa": s},
            output_units={"bending_stress_pa": "Pa"},
            equations=["sigma = M * y / I"],
            assumptions=["Euler-Bernoulli beam theory, linear-elastic"],
            model="Beam bending stress",
            validity_limits=["second_moment_of_area_m4 > 0"],
        )

    @mcp.tool()
    def calculate_cantilever_deflection(
        tip_load_n: float,
        length_m: float,
        youngs_modulus_pa: float,
        second_moment_of_area_m4: float,
    ) -> dict:
        """Calculate cantilever beam tip deflection (m) under a point tip load."""
        d = cantilever_tip_deflection(
            tip_load_n, length_m, youngs_modulus_pa, second_moment_of_area_m4
        )
        return build_result(
            calculation_name="calculate_cantilever_deflection",
            engineering_domain="structures",
            inputs={"tip_load_n": tip_load_n, "length_m": length_m},
            results={"tip_deflection_m": d},
            output_units={"tip_deflection_m": "m"},
            equations=["delta = P * L^3 / (3 * E * I)"],
            assumptions=["Small deflections, Euler-Bernoulli beam"],
            model="Cantilever beam tip deflection",
            validity_limits=[
                "length_m > 0",
                "youngs_modulus_pa > 0",
                "second_moment_of_area_m4 > 0",
            ],
        )

    @mcp.tool()
    def calculate_simply_supported_deflection(
        center_load_n: float,
        length_m: float,
        youngs_modulus_pa: float,
        second_moment_of_area_m4: float,
    ) -> dict:
        """Calculate simply supported beam mid-span deflection (m) under a center load."""
        d = simply_supported_center_deflection(
            center_load_n, length_m, youngs_modulus_pa, second_moment_of_area_m4
        )
        return build_result(
            calculation_name="calculate_simply_supported_deflection",
            engineering_domain="structures",
            inputs={"center_load_n": center_load_n, "length_m": length_m},
            results={"center_deflection_m": d},
            output_units={"center_deflection_m": "m"},
            equations=["delta = P * L^3 / (48 * E * I)"],
            assumptions=["Small deflections, Euler-Bernoulli beam"],
            model="Simply supported beam deflection",
            validity_limits=[
                "length_m > 0",
                "youngs_modulus_pa > 0",
                "second_moment_of_area_m4 > 0",
            ],
        )

    @mcp.tool()
    def calculate_shaft_torsion(
        torque_n_m: float,
        outer_radius_m: float,
        polar_moment_of_inertia_m4: float,
        length_m: float,
        shear_modulus_pa: float,
    ) -> dict:
        """Calculate circular shaft maximum shear stress (Pa) and angle of twist (rad)."""
        res = circular_shaft_torsion(
            torque_n_m,
            outer_radius_m,
            polar_moment_of_inertia_m4,
            length_m,
            shear_modulus_pa,
        )
        return build_result(
            calculation_name="calculate_shaft_torsion",
            engineering_domain="structures",
            inputs={
                "torque_n_m": torque_n_m,
                "outer_radius_m": outer_radius_m,
                "length_m": length_m,
            },
            results=res,
            output_units={"max_shear_stress_pa": "Pa", "angle_of_twist_rad": "rad"},
            equations=["tau_max = T*r/J", "theta = T*L/(G*J)"],
            assumptions=["Circular cross-section, linear-elastic"],
            model="Circular shaft torsion",
            validity_limits=["outer_radius_m > 0", "polar_moment_of_inertia_m4 > 0"],
        )

    @mcp.tool()
    def calculate_euler_buckling(
        youngs_modulus_pa: float,
        second_moment_of_area_m4: float,
        length_m: float,
        effective_length_factor: float = 1.0,
    ) -> dict:
        """Calculate Euler critical buckling load (N) for a slender column."""
        pcr = euler_buckling_load(
            youngs_modulus_pa,
            second_moment_of_area_m4,
            length_m,
            effective_length_factor,
        )
        return build_result(
            calculation_name="calculate_euler_buckling",
            engineering_domain="structures",
            inputs={
                "length_m": length_m,
                "effective_length_factor": effective_length_factor,
            },
            results={"critical_buckling_load_n": pcr},
            output_units={"critical_buckling_load_n": "N"},
            equations=["Pcr = pi^2 * E * I / (K * L)^2"],
            assumptions=["Slender elastic column, no initial imperfection"],
            model="Euler column buckling",
            validity_limits=["All inputs > 0"],
        )

    @mcp.tool()
    def calculate_von_mises_stress(
        sigma_x_pa: float, sigma_y_pa: float, tau_xy_pa: float
    ) -> dict:
        """Calculate 2D plane-stress Von Mises equivalent stress (Pa)."""
        vm = von_mises_stress_2d(sigma_x_pa, sigma_y_pa, tau_xy_pa)
        return build_result(
            calculation_name="calculate_von_mises_stress",
            engineering_domain="structures",
            inputs={
                "sigma_x_pa": sigma_x_pa,
                "sigma_y_pa": sigma_y_pa,
                "tau_xy_pa": tau_xy_pa,
            },
            results={"von_mises_stress_pa": vm},
            output_units={"von_mises_stress_pa": "Pa"},
            equations=["sigma_vm = sqrt(sx^2 - sx*sy + sy^2 + 3*txy^2)"],
            assumptions=["2D plane stress, isotropic ductile yield criterion"],
            model="Von Mises yield criterion",
            validity_limits=["Finite stress inputs"],
        )

    @mcp.tool()
    def calculate_pressure_vessel_stress(
        internal_pressure_pa: float, radius_m: float, wall_thickness_m: float
    ) -> dict:
        """Calculate thin-walled cylindrical pressure-vessel hoop, axial, and Von Mises stresses (Pa)."""
        res = thin_walled_pressure_vessel(
            internal_pressure_pa, radius_m, wall_thickness_m
        )
        return build_result(
            calculation_name="calculate_pressure_vessel_stress",
            engineering_domain="structures",
            inputs={
                "internal_pressure_pa": internal_pressure_pa,
                "radius_m": radius_m,
                "wall_thickness_m": wall_thickness_m,
            },
            results=res,
            output_units={
                "hoop_stress_pa": "Pa",
                "axial_stress_pa": "Pa",
                "von_mises_stress_pa": "Pa",
            },
            equations=["sigma_hoop = p*r/t", "sigma_axial = p*r/(2*t)"],
            assumptions=["Thin-walled cylinder (t/R <= 0.1)"],
            model="Thin-walled pressure vessel",
            validity_limits=["wall_thickness_m / radius_m <= 0.1"],
        )
