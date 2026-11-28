"""Reusable MCP prompts for AeroMCP aerospace engineering workflows."""

from __future__ import annotations

from mcp.server import MCPServer


def register_prompts(mcp: MCPServer) -> None:
    """Register reusable engineering workflow prompts."""

    @mcp.prompt()
    def preliminary_aircraft_design_analysis(
        weight_n: float, wing_loading_n_m2: float, aspect_ratio: float
    ) -> str:
        """Guide an agent through preliminary aircraft wing sizing and stall/induced-drag checks."""
        return (
            f"Perform a preliminary aircraft design analysis for W={weight_n} N, "
            f"W/S={wing_loading_n_m2} N/m^2, AR={aspect_ratio}. "
            "Use `size_wing_geometry`, `calculate_isa_atmosphere`, `calculate_stall_speed`, "
            "and `calculate_induced_drag`. Report all results in SI units and state assumptions."
        )

    @mcp.prompt()
    def rocket_stage_sizing(
        delta_v_m_s: float, isp_s: float, payload_mass_kg: float
    ) -> str:
        """Guide an agent through Tsiolkovsky rocket stage propellant sizing."""
        return (
            f"Size a rocket stage for delta_v={delta_v_m_s} m/s, Isp={isp_s} s, "
            f"and final/payload mass={payload_mass_kg} kg. "
            "Use `calculate_propellant_mass` and `calculate_tsiolkovsky_delta_v` to verify."
        )

    @mcp.prompt()
    def compressible_nozzle_analysis(
        chamber_pressure_pa: float,
        chamber_temperature_k: float,
        throat_area_m2: float,
        exit_area_m2: float,
    ) -> str:
        """Guide an agent through converging-diverging nozzle performance analysis."""
        return (
            f"Analyze a converging-diverging nozzle with pc={chamber_pressure_pa} Pa, "
            f"Tc={chamber_temperature_k} K, At={throat_area_m2} m^2, Ae={exit_area_m2} m^2. "
            "Use `calculate_cd_nozzle_performance` and `calculate_isentropic_ratios`."
        )

    @mcp.prompt()
    def orbital_transfer_analysis(
        initial_radius_m: float, target_radius_m: float
    ) -> str:
        """Guide an agent through Hohmann orbital transfer and vis-viva verification."""
        return (
            f"Analyze a coplanar Hohmann transfer from r1={initial_radius_m} m to "
            f"r2={target_radius_m} m. Use `calculate_hohmann_transfer`, "
            "`calculate_circular_orbital_velocity`, and `calculate_orbital_period`."
        )

    @mcp.prompt()
    def aircraft_performance_analysis(
        velocity_m_s: float, weight_n: float, lift_to_drag: float
    ) -> str:
        """Guide an agent through aircraft climb, glide, and turn performance."""
        return (
            f"Evaluate aircraft performance at V={velocity_m_s} m/s, W={weight_n} N, "
            f"L/D={lift_to_drag}. Use `calculate_glide_performance` and `calculate_coordinated_turn`."
        )

    @mcp.prompt()
    def structural_preliminary_sizing(
        load_n: float, length_m: float, youngs_modulus_pa: float
    ) -> str:
        """Guide an agent through preliminary structural beam and buckling checks."""
        return (
            f"Perform preliminary structural checks for load={load_n} N, L={length_m} m, "
            f"E={youngs_modulus_pa} Pa. Use `calculate_cantilever_deflection`, "
            "`calculate_euler_buckling`, and `calculate_von_mises_stress`."
        )

    @mcp.prompt()
    def uav_performance_estimation(
        weight_n: float,
        num_rotors: int,
        rotor_radius_m: float,
        battery_energy_wh: float,
    ) -> str:
        """Guide an agent through multirotor UAV hover power and endurance estimation."""
        return (
            f"Estimate multirotor UAV hover power and endurance for W={weight_n} N, "
            f"N={num_rotors} rotors of radius {rotor_radius_m} m, battery={battery_energy_wh} Wh. "
            "Use `calculate_isa_atmosphere`, `calculate_multirotor_hover`, and "
            "`estimate_electric_uav_endurance`."
        )
