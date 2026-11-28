"""MCP tools for flight mechanics and aircraft stability."""

from __future__ import annotations

from mcp.server import MCPServer

from aeromcp_engineering.core.results import build_result
from aeromcp_engineering.flight_mechanics import (
    climb_performance,
    coordinated_turn_performance,
    glide_performance,
    jet_breguet_range,
    neutral_point_position,
    propeller_breguet_endurance,
    static_margin,
    takeoff_ground_roll,
)


def register_flight_mechanics_tools(mcp: MCPServer) -> None:
    """Register flight mechanics and stability MCP tools."""

    @mcp.tool()
    def calculate_coordinated_turn(velocity_m_s: float, bank_angle_rad: float) -> dict:
        """Calculate coordinated level-turn load factor, turn radius (m), and turn rate (rad/s)."""
        res = coordinated_turn_performance(velocity_m_s, bank_angle_rad)
        return build_result(
            calculation_name="calculate_coordinated_turn",
            engineering_domain="flight_mechanics",
            inputs={"velocity_m_s": velocity_m_s, "bank_angle_rad": bank_angle_rad},
            results=res,
            output_units={
                "load_factor": "dimensionless",
                "turn_radius_m": "m",
                "turn_rate_rad_s": "rad/s",
            },
            equations=["n = 1/cos(phi)", "R = V^2 / (g0*tan(phi))"],
            assumptions=["Steady coordinated level turn"],
            model="Coordinated turn mechanics",
            validity_limits=["|bank_angle_rad| < pi/2"],
        )

    @mcp.tool()
    def calculate_climb_performance(
        thrust_n: float, drag_n: float, weight_n: float, velocity_m_s: float
    ) -> dict:
        """Calculate steady rate of climb (m/s) and climb gradient."""
        res = climb_performance(thrust_n, drag_n, weight_n, velocity_m_s)
        return build_result(
            calculation_name="calculate_climb_performance",
            engineering_domain="flight_mechanics",
            inputs={
                "thrust_n": thrust_n,
                "drag_n": drag_n,
                "weight_n": weight_n,
                "velocity_m_s": velocity_m_s,
            },
            results=res,
            output_units={
                "rate_of_climb_m_s": "m/s",
                "climb_gradient": "dimensionless",
            },
            equations=["ROC = V * (T - D) / W"],
            assumptions=["Steady unaccelerated climb"],
            model="Excess-power climb",
            validity_limits=["|(T - D)/W| <= 1.0"],
        )

    @mcp.tool()
    def calculate_glide_performance(lift_to_drag: float, altitude_m: float) -> dict:
        """Calculate steady unpowered glide range (m) and glide angle (rad)."""
        res = glide_performance(lift_to_drag, altitude_m)
        return build_result(
            calculation_name="calculate_glide_performance",
            engineering_domain="flight_mechanics",
            inputs={"lift_to_drag": lift_to_drag, "altitude_m": altitude_m},
            results=res,
            output_units={"glide_range_m": "m", "glide_angle_rad": "rad"},
            equations=["R = h * (L/D)"],
            assumptions=["Steady unpowered glide, still air"],
            model="Steady glide",
            validity_limits=["lift_to_drag > 0"],
        )

    @mcp.tool()
    def calculate_jet_breguet_range(
        velocity_m_s: float,
        tsfc_kg_n_s: float,
        lift_to_drag: float,
        initial_mass_kg: float,
        final_mass_kg: float,
    ) -> dict:
        """Calculate jet aircraft Breguet range (m)."""
        r = jet_breguet_range(
            velocity_m_s, tsfc_kg_n_s, lift_to_drag, initial_mass_kg, final_mass_kg
        )
        return build_result(
            calculation_name="calculate_jet_breguet_range",
            engineering_domain="flight_mechanics",
            inputs={
                "velocity_m_s": velocity_m_s,
                "tsfc_kg_n_s": tsfc_kg_n_s,
                "lift_to_drag": lift_to_drag,
                "initial_mass_kg": initial_mass_kg,
                "final_mass_kg": final_mass_kg,
            },
            results={"range_m": r},
            output_units={"range_m": "m"},
            equations=["R = (V / (g0 * TSFC)) * (L/D) * ln(m0/mf)"],
            assumptions=["Constant V, TSFC, and L/D"],
            model="Jet Breguet range equation",
            validity_limits=["0 < final_mass_kg <= initial_mass_kg"],
        )

    @mcp.tool()
    def calculate_propeller_endurance(
        propeller_efficiency: float,
        bsfc_kg_w_s: float,
        lift_to_drag: float,
        velocity_m_s: float,
        initial_mass_kg: float,
        final_mass_kg: float,
    ) -> dict:
        """Calculate propeller aircraft Breguet endurance (s)."""
        e = propeller_breguet_endurance(
            propeller_efficiency,
            bsfc_kg_w_s,
            lift_to_drag,
            velocity_m_s,
            initial_mass_kg,
            final_mass_kg,
        )
        return build_result(
            calculation_name="calculate_propeller_endurance",
            engineering_domain="flight_mechanics",
            inputs={
                "propeller_efficiency": propeller_efficiency,
                "bsfc_kg_w_s": bsfc_kg_w_s,
                "lift_to_drag": lift_to_drag,
                "velocity_m_s": velocity_m_s,
            },
            results={"endurance_s": e},
            output_units={"endurance_s": "s"},
            equations=["E = (eta_p / (g0 * BSFC * V)) * (L/D) * ln(m0/mf)"],
            assumptions=["Constant eta_p, BSFC, L/D, and V"],
            model="Propeller Breguet endurance",
            validity_limits=["0 < propeller_efficiency <= 1.0"],
        )

    @mcp.tool()
    def calculate_takeoff_ground_roll(
        weight_n: float,
        thrust_n: float,
        drag_n: float,
        lift_n: float,
        liftoff_velocity_m_s: float,
        rolling_friction_coeff: float = 0.02,
    ) -> dict:
        """Estimate constant-acceleration takeoff ground-roll distance (m)."""
        dist = takeoff_ground_roll(
            weight_n,
            thrust_n,
            drag_n,
            lift_n,
            liftoff_velocity_m_s,
            rolling_friction_coeff,
        )
        return build_result(
            calculation_name="calculate_takeoff_ground_roll",
            engineering_domain="flight_mechanics",
            inputs={
                "weight_n": weight_n,
                "thrust_n": thrust_n,
                "liftoff_velocity_m_s": liftoff_velocity_m_s,
            },
            results={"ground_roll_m": dist},
            output_units={"ground_roll_m": "m"},
            equations=["s_g = V_lo^2 / (2 * a_avg)"],
            assumptions=["Constant average acceleration, level runway, no wind"],
            model="Constant-acceleration ground roll",
            validity_limits=["Net accelerating force > 0"],
        )

    @mcp.tool()
    def calculate_static_margin(
        neutral_point_mac: float,
        cg_position_mac: float,
    ) -> dict:
        """Calculate longitudinal static margin SM = x_np - x_cg (fraction of MAC)."""
        sm = static_margin(neutral_point_mac, cg_position_mac)
        return build_result(
            calculation_name="calculate_static_margin",
            engineering_domain="flight_mechanics",
            inputs={
                "neutral_point_mac": neutral_point_mac,
                "cg_position_mac": cg_position_mac,
            },
            results={"static_margin_mac": sm},
            output_units={"static_margin_mac": "MAC_fraction"},
            equations=["SM = (x_np - x_cg) / MAC"],
            assumptions=["Linear longitudinal aerodynamics"],
            model="Stick-fixed static margin",
            validity_limits=["Finite MAC-normalized positions"],
        )

    @mcp.tool()
    def calculate_neutral_point(
        aerodynamic_center_mac: float,
        tail_volume_ratio: float,
        tail_lift_slope_per_rad: float,
        wing_lift_slope_per_rad: float,
        downwash_gradient: float = 0.0,
        tail_efficiency: float = 1.0,
    ) -> dict:
        """Calculate stick-fixed neutral point position (fraction of MAC)."""
        np_mac = neutral_point_position(
            aerodynamic_center_mac,
            tail_volume_ratio,
            tail_lift_slope_per_rad,
            wing_lift_slope_per_rad,
            downwash_gradient,
            tail_efficiency,
        )
        return build_result(
            calculation_name="calculate_neutral_point",
            engineering_domain="flight_mechanics",
            inputs={
                "aerodynamic_center_mac": aerodynamic_center_mac,
                "tail_volume_ratio": tail_volume_ratio,
            },
            results={"neutral_point_mac": np_mac},
            output_units={"neutral_point_mac": "MAC_fraction"},
            equations=["x_np = x_ac + eta_t * V_H * (a_t/a_w) * (1 - de/da)"],
            assumptions=["Linear wing-tail aerodynamics"],
            model="Stick-fixed neutral point",
            validity_limits=["a_t > 0", "a_w > 0"],
        )
