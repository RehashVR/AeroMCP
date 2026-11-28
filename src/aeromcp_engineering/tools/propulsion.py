"""MCP tools for propulsion engineering."""

from __future__ import annotations

from mcp.server import MCPServer

from aeromcp_engineering.core.constants import GAMMA_AIR
from aeromcp_engineering.core.results import build_result
from aeromcp_engineering.propulsion import (
    actuator_disk_propeller,
    choked_mass_flow,
    converging_diverging_nozzle,
    ideal_turbojet_cycle,
    multirotor_hover_estimate,
    propellant_mass_from_delta_v,
    rocket_thrust,
    rotor_hover_power,
    specific_impulse,
    tsiolkovsky_delta_v,
)


def register_propulsion_tools(mcp: MCPServer) -> None:
    """Register propulsion MCP tools."""

    @mcp.tool()
    def calculate_rocket_thrust(
        mass_flow_kg_s: float,
        exhaust_velocity_m_s: float,
        exit_pressure_pa: float = 0.0,
        ambient_pressure_pa: float = 0.0,
        exit_area_m2: float = 0.0,
    ) -> dict:
        """Calculate rocket thrust F = m_dot*Ve + (pe - pa)*Ae in newtons (N)."""
        f = rocket_thrust(
            mass_flow_kg_s,
            exhaust_velocity_m_s,
            exit_pressure_pa,
            ambient_pressure_pa,
            exit_area_m2,
        )
        return build_result(
            calculation_name="calculate_rocket_thrust",
            engineering_domain="propulsion",
            inputs={
                "mass_flow_kg_s": mass_flow_kg_s,
                "exhaust_velocity_m_s": exhaust_velocity_m_s,
                "exit_pressure_pa": exit_pressure_pa,
                "ambient_pressure_pa": ambient_pressure_pa,
                "exit_area_m2": exit_area_m2,
            },
            results={"thrust_n": f},
            output_units={"thrust_n": "N"},
            equations=["F = m_dot * Ve + (pe - pa) * Ae"],
            assumptions=["1D steady rocket nozzle flow"],
            model="Rocket thrust equation",
            validity_limits=["mass_flow_kg_s > 0", "exhaust_velocity_m_s > 0"],
        )

    @mcp.tool()
    def calculate_specific_impulse(thrust_n: float, mass_flow_kg_s: float) -> dict:
        """Calculate specific impulse Isp = F / (m_dot * g0) in seconds (s)."""
        isp = specific_impulse(thrust_n, mass_flow_kg_s)
        return build_result(
            calculation_name="calculate_specific_impulse",
            engineering_domain="propulsion",
            inputs={"thrust_n": thrust_n, "mass_flow_kg_s": mass_flow_kg_s},
            results={"isp_s": isp},
            output_units={"isp_s": "s"},
            equations=["Isp = F / (m_dot * g0)"],
            assumptions=["Standard gravity g0 = 9.80665 m/s^2"],
            model="Specific impulse definition",
            validity_limits=["thrust_n > 0", "mass_flow_kg_s > 0"],
        )

    @mcp.tool()
    def calculate_tsiolkovsky_delta_v(
        isp_s: float, initial_mass_kg: float, final_mass_kg: float
    ) -> dict:
        """Calculate ideal rocket delta-V = Isp * g0 * ln(m0 / mf) in m/s."""
        dv = tsiolkovsky_delta_v(isp_s, initial_mass_kg, final_mass_kg)
        return build_result(
            calculation_name="calculate_tsiolkovsky_delta_v",
            engineering_domain="propulsion",
            inputs={
                "isp_s": isp_s,
                "initial_mass_kg": initial_mass_kg,
                "final_mass_kg": final_mass_kg,
            },
            results={"delta_v_m_s": dv},
            output_units={"delta_v_m_s": "m/s"},
            equations=["dV = Isp * g0 * ln(m0 / mf)"],
            assumptions=["No gravity or drag losses", "Constant Isp"],
            model="Tsiolkovsky rocket equation",
            validity_limits=["0 < final_mass_kg <= initial_mass_kg"],
        )

    @mcp.tool()
    def calculate_propellant_mass(
        delta_v_m_s: float, isp_s: float, final_mass_kg: float
    ) -> dict:
        """Calculate required propellant mass (kg) and mass ratio for a target delta-V."""
        res = propellant_mass_from_delta_v(delta_v_m_s, isp_s, final_mass_kg)
        return build_result(
            calculation_name="calculate_propellant_mass",
            engineering_domain="propulsion",
            inputs={
                "delta_v_m_s": delta_v_m_s,
                "isp_s": isp_s,
                "final_mass_kg": final_mass_kg,
            },
            results=res,
            output_units={
                "initial_mass_kg": "kg",
                "propellant_mass_kg": "kg",
                "mass_ratio": "dimensionless",
            },
            equations=["m0/mf = exp(dV / (Isp * g0))", "mp = m0 - mf"],
            assumptions=["Ideal Tsiolkovsky rocket equation"],
            model="Rocket propellant sizing",
            validity_limits=["delta_v_m_s >= 0", "isp_s > 0", "final_mass_kg > 0"],
        )

    @mcp.tool()
    def calculate_choked_nozzle_mass_flow(
        chamber_pressure_pa: float,
        chamber_temperature_k: float,
        throat_area_m2: float,
        gamma: float = GAMMA_AIR,
        gas_constant_j_kg_k: float = 287.05287,
    ) -> dict:
        """Calculate choked nozzle mass flow rate (kg/s) at sonic throat."""
        m_dot = choked_mass_flow(
            chamber_pressure_pa,
            chamber_temperature_k,
            throat_area_m2,
            gamma,
            gas_constant_j_kg_k,
        )
        return build_result(
            calculation_name="calculate_choked_nozzle_mass_flow",
            engineering_domain="propulsion",
            inputs={
                "chamber_pressure_pa": chamber_pressure_pa,
                "chamber_temperature_k": chamber_temperature_k,
                "throat_area_m2": throat_area_m2,
                "gamma": gamma,
                "gas_constant_j_kg_k": gas_constant_j_kg_k,
            },
            results={"mass_flow_kg_s": m_dot},
            output_units={"mass_flow_kg_s": "kg/s"},
            equations=[
                "m_dot = pc * At * sqrt(gamma / (R*Tc)) * (2/(gamma+1))^((gamma+1)/(2*(gamma-1)))"
            ],
            assumptions=["Isentropic choked throat, ideal gas"],
            model="Choked nozzle mass flow",
            validity_limits=["All inputs > 0", "gamma > 1.0"],
        )

    @mcp.tool()
    def calculate_cd_nozzle_performance(
        chamber_pressure_pa: float,
        chamber_temperature_k: float,
        throat_area_m2: float,
        exit_area_m2: float,
        ambient_pressure_pa: float = 0.0,
        gamma: float = GAMMA_AIR,
        gas_constant_j_kg_k: float = 287.05287,
        nozzle_efficiency: float = 1.0,
    ) -> dict:
        """Calculate converging-diverging supersonic nozzle exit Mach, pressure, and thrust."""
        res = converging_diverging_nozzle(
            chamber_pressure_pa,
            chamber_temperature_k,
            throat_area_m2,
            exit_area_m2,
            ambient_pressure_pa,
            gamma,
            gas_constant_j_kg_k,
            nozzle_efficiency,
        )
        return build_result(
            calculation_name="calculate_cd_nozzle_performance",
            engineering_domain="propulsion",
            inputs={
                "chamber_pressure_pa": chamber_pressure_pa,
                "chamber_temperature_k": chamber_temperature_k,
                "throat_area_m2": throat_area_m2,
                "exit_area_m2": exit_area_m2,
                "ambient_pressure_pa": ambient_pressure_pa,
            },
            results=res,
            output_units={
                "exit_mach": "dimensionless",
                "exit_pressure_pa": "Pa",
                "thrust_n": "N",
            },
            equations=["Supersonic area-Mach + choked mass flow + thrust equation"],
            assumptions=["Quasi-1D supersonic nozzle flow, no internal shock"],
            model="Converging-diverging nozzle",
            validity_limits=["exit_area_m2 >= throat_area_m2"],
        )

    @mcp.tool()
    def calculate_ideal_turbojet_cycle(
        flight_mach: float,
        ambient_temperature_k: float,
        compressor_pressure_ratio: float,
        turbine_inlet_temperature_k: float,
    ) -> dict:
        """Calculate ideal Brayton-cycle turbojet specific thrust and TSFC."""
        res = ideal_turbojet_cycle(
            flight_mach,
            ambient_temperature_k,
            compressor_pressure_ratio,
            turbine_inlet_temperature_k,
        )
        return build_result(
            calculation_name="calculate_ideal_turbojet_cycle",
            engineering_domain="propulsion",
            inputs={
                "flight_mach": flight_mach,
                "ambient_temperature_k": ambient_temperature_k,
                "compressor_pressure_ratio": compressor_pressure_ratio,
                "turbine_inlet_temperature_k": turbine_inlet_temperature_k,
            },
            results=res,
            output_units={
                "specific_thrust_n_s_kg": "N*s/kg",
                "tsfc_kg_n_s": "kg/(N*s)",
            },
            equations=["Ideal Brayton cycle"],
            assumptions=["Isentropic inlet/compressor/turbine/nozzle, ideal gas"],
            model="Ideal turbojet cycle",
            validity_limits=["compressor_pressure_ratio >= 1.0"],
        )

    @mcp.tool()
    def calculate_propeller_momentum(
        thrust_n: float,
        disk_area_m2: float,
        density_kg_m3: float,
        freestream_velocity_m_s: float = 0.0,
        propulsive_efficiency_factor: float = 1.0,
    ) -> dict:
        """Calculate actuator-disk propeller induced velocity, shaft power (W), and efficiency."""
        res = actuator_disk_propeller(
            thrust_n,
            disk_area_m2,
            density_kg_m3,
            freestream_velocity_m_s,
            propulsive_efficiency_factor,
        )
        return build_result(
            calculation_name="calculate_propeller_momentum",
            engineering_domain="propulsion",
            inputs={
                "thrust_n": thrust_n,
                "disk_area_m2": disk_area_m2,
                "density_kg_m3": density_kg_m3,
                "freestream_velocity_m_s": freestream_velocity_m_s,
            },
            results=res,
            output_units={"induced_velocity_m_s": "m/s", "shaft_power_w": "W"},
            equations=["P_ideal = T * (V0 + vi)"],
            assumptions=["1D incompressible actuator disk"],
            model="Actuator-disk momentum theory",
            validity_limits=["thrust_n > 0", "disk_area_m2 > 0", "density_kg_m3 > 0"],
        )

    @mcp.tool()
    def calculate_rotor_hover_power(
        thrust_n: float,
        rotor_radius_m: float,
        density_kg_m3: float,
        figure_of_merit: float = 0.75,
    ) -> dict:
        """Calculate ideal and actual single-rotor hover power (W)."""
        res = rotor_hover_power(
            thrust_n, rotor_radius_m, density_kg_m3, figure_of_merit
        )
        return build_result(
            calculation_name="calculate_rotor_hover_power",
            engineering_domain="propulsion",
            inputs={
                "thrust_n": thrust_n,
                "rotor_radius_m": rotor_radius_m,
                "density_kg_m3": density_kg_m3,
                "figure_of_merit": figure_of_merit,
            },
            results=res,
            output_units={"ideal_hover_power_w": "W", "actual_hover_power_w": "W"},
            equations=["P_ideal = T^(3/2) / sqrt(2*rho*A)", "P_actual = P_ideal / FM"],
            assumptions=["Uniform inflow actuator disk"],
            model="Rotor hover momentum theory",
            validity_limits=["0 < figure_of_merit <= 1.0"],
        )

    @mcp.tool()
    def calculate_multirotor_hover(
        total_weight_n: float,
        num_rotors: int,
        rotor_radius_m: float,
        density_kg_m3: float,
        figure_of_merit: float = 0.7,
    ) -> dict:
        """Estimate total hover power (W) and per-rotor thrust (N) for a multirotor."""
        res = multirotor_hover_estimate(
            total_weight_n, num_rotors, rotor_radius_m, density_kg_m3, figure_of_merit
        )
        return build_result(
            calculation_name="calculate_multirotor_hover",
            engineering_domain="propulsion",
            inputs={
                "total_weight_n": total_weight_n,
                "num_rotors": num_rotors,
                "rotor_radius_m": rotor_radius_m,
                "density_kg_m3": density_kg_m3,
            },
            results=res,
            output_units={"thrust_per_rotor_n": "N", "total_actual_hover_power_w": "W"},
            equations=["T_rotor = W / N", "P_total = N * P_rotor"],
            assumptions=["Equal thrust sharing, no rotor-rotor interference"],
            model="Multirotor hover momentum theory",
            validity_limits=["num_rotors >= 1"],
        )
