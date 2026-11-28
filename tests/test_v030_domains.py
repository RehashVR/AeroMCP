"""Comprehensive tests for AeroMCP v0.3.0 engineering domains and core utilities."""

from __future__ import annotations

import math

import pytest

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
from aeromcp_engineering.aircraft_design import (
    electric_uav_endurance,
    power_to_weight_ratio,
    rectangular_wing_mac,
    thrust_to_weight_ratio,
    wing_area_from_loading,
    wingspan_from_aspect_ratio,
)
from aeromcp_engineering.astrodynamics import (
    c3_energy,
    coe_to_rv,
    hyperbolic_excess_velocity,
    j2_secular_rates,
    mean_to_true_anomaly,
    periapsis_apoapsis,
    propagate_two_body_rk4,
    solve_kepler_elliptic,
    true_to_mean_anomaly,
    vis_viva_velocity,
)
from aeromcp_engineering.atmosphere import (
    density_altitude,
    isa_atmosphere,
    mach_atmospheric_properties,
    sutherland_viscosity,
)
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
from aeromcp_engineering.core import (
    bisection,
    convert_unit,
    rk4_integrate,
    safeguarded_newton,
    solve_linear_system,
)
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
from aeromcp_engineering.gnc import (
    ecef_to_geodetic,
    euler_zyx_to_quaternion,
    geodetic_to_ecef,
    pid_step,
    quaternion_multiply,
    quaternion_normalize,
    quaternion_to_euler_zyx,
    scalar_kalman_update,
)
from aeromcp_engineering.mission_analysis import (
    mission_delta_v_budget,
    vertical_rocket_ascent_rk4,
)
from aeromcp_engineering.propulsion import (
    actuator_disk_propeller,
    choked_mass_flow,
    converging_diverging_nozzle,
    critical_pressure_ratio,
    ideal_turbojet_cycle,
    multirotor_hover_estimate,
    multistage_delta_v,
    propellant_mass_from_delta_v,
    rocket_thrust,
    rotor_hover_power,
    specific_impulse,
    tsiolkovsky_delta_v,
)
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
from aeromcp_engineering.thermal import (
    conduction_1d_heat_rate,
    convection_heat_rate,
    radiation_heat_rate,
    series_thermal_resistance_heat_rate,
    stagnation_and_recovery_temperature,
    sutton_graves_stagnation_heat_flux,
)


def test_core_numerical_and_units():
    assert bisection(lambda x: x * x - 4.0, 0.0, 5.0).root == pytest.approx(
        2.0, abs=1e-10
    )
    assert safeguarded_newton(
        lambda x: x * x - 9.0, lambda x: 2.0 * x, 0.0, 5.0
    ).root == pytest.approx(3.0, abs=1e-10)
    _, states = rk4_integrate(lambda _t, y: [-y[0]], 0.0, [1.0], 1.0, 0.05)
    assert states[-1][0] == pytest.approx(math.exp(-1.0), rel=1e-6)
    assert solve_linear_system([[2.0, 1.0], [1.0, 3.0]], [1.0, 2.0]) == pytest.approx(
        [0.2, 0.6]
    )
    assert convert_unit(100.0, "c", "k", "temperature") == pytest.approx(373.15)
    assert convert_unit(1.0, "nmi", "m", "length") == pytest.approx(1852.0)


def test_aerodynamics_domain():
    assert mach_number(340.0, 340.0) == pytest.approx(1.0)
    assert lift_to_drag_ratio(1000.0, 50.0) == pytest.approx(20.0)
    assert wing_loading(10000.0, 20.0) == pytest.approx(500.0)
    assert aspect_ratio(10.0, 20.0) == pytest.approx(5.0)
    assert induced_drag_coefficient(1.0, 8.0, 0.8) == pytest.approx(
        1.0 / (math.pi * 6.4)
    )
    assert induced_drag_force(1.225, 50.0, 20.0, 0.5, 8.0, 0.85) > 0.0
    assert stall_speed(10000.0, 1.225, 20.0, 1.5) == pytest.approx(
        math.sqrt(20000.0 / (1.225 * 30.0))
    )
    assert finite_wing_lift_slope(2.0 * math.pi, 8.0, 1.0) < 2.0 * math.pi
    assert thin_airfoil_lift_coefficient(0.1) == pytest.approx(0.2 * math.pi)
    dec = aerodynamic_force_decomposition(100.0, 10.0, 0.0)
    assert dec["lift_n"] == pytest.approx(100.0)
    assert dec["drag_n"] == pytest.approx(10.0)


def test_atmosphere_domain():
    atm0 = isa_atmosphere(0.0)
    assert atm0["temperature_k"] == pytest.approx(288.15)
    assert atm0["pressure_pa"] == pytest.approx(101325.0)
    atm25 = isa_atmosphere(25_000.0)
    assert atm25["temperature_k"] > 216.65
    assert sutherland_viscosity(288.15) == pytest.approx(1.789e-5, rel=1e-2)
    mp = mach_atmospheric_properties(10_000.0, 250.0)
    assert 0.8 < mp["mach_number"] < 0.9
    assert density_altitude(1.225) == pytest.approx(0.0, abs=1.0)
    with pytest.raises(ValueError):
        isa_atmosphere(100_000.0)


def test_compressible_flow_domain():
    iso = isentropic_ratios(2.0)
    assert iso["t0_over_t"] == pytest.approx(1.8)
    assert iso["p0_over_p"] == pytest.approx(7.824449, rel=1e-5)
    ar = area_mach_ratio(2.0)
    assert ar == pytest.approx(1.6875, rel=1e-5)
    assert solve_mach_from_area_ratio(ar, "supersonic") == pytest.approx(2.0, rel=1e-6)
    assert 0.0 < solve_mach_from_area_ratio(ar, "subsonic") < 1.0
    ns = normal_shock_relations(2.0)
    assert ns["downstream_mach"] == pytest.approx(0.57735, rel=1e-4)
    os_weak = oblique_shock_relations(2.0, math.radians(10.0), "weak")
    assert os_weak["downstream_mach"] > 1.0
    with pytest.raises(ValueError):
        oblique_shock_relations(2.0, math.radians(40.0), "weak")
    nu = prandtl_meyer_angle(2.0)
    assert math.degrees(nu) == pytest.approx(26.37976, rel=1e-4)
    assert inverse_prandtl_meyer(nu) == pytest.approx(2.0, rel=1e-6)
    assert fanno_flow_ratios(2.0)["four_f_lstar_over_d"] > 0.0
    assert rayleigh_flow_ratios(1.0)["p_over_pstar"] == pytest.approx(1.0)


def test_propulsion_domain():
    assert rocket_thrust(100.0, 3000.0) == pytest.approx(300_000.0)
    assert specific_impulse(300_000.0, 100.0) == pytest.approx(
        300_000.0 / (100.0 * 9.80665)
    )
    assert tsiolkovsky_delta_v(300.0, 1000.0, 500.0) == pytest.approx(
        300.0 * 9.80665 * math.log(2.0)
    )
    pm = propellant_mass_from_delta_v(2000.0, 300.0, 500.0)
    assert pm["propellant_mass_kg"] > 0.0
    ms = multistage_delta_v(
        [
            {"structural_mass_kg": 100.0, "propellant_mass_kg": 900.0, "isp_s": 300.0},
            {"structural_mass_kg": 50.0, "propellant_mass_kg": 450.0, "isp_s": 320.0},
        ],
        payload_mass_kg=100.0,
    )
    assert ms["total_delta_v_m_s"] > 5000.0
    assert critical_pressure_ratio(1.4) == pytest.approx(0.52828, rel=1e-4)
    assert choked_mass_flow(1e6, 300.0, 0.01) > 0.0
    cd = converging_diverging_nozzle(2e6, 3000.0, 0.01, 0.05)
    assert cd["exit_mach"] > 2.0
    tj = ideal_turbojet_cycle(0.8, 220.0, 15.0, 1500.0)
    assert tj["specific_thrust_n_s_kg"] > 0.0
    prop = actuator_disk_propeller(100.0, 0.5, 1.225, 20.0)
    assert 0.0 < prop["ideal_propulsive_efficiency"] < 1.0
    assert rotor_hover_power(10.0, 0.2, 1.225)["actual_hover_power_w"] > 0.0
    assert multirotor_hover_estimate(20.0, 4, 0.15, 1.225)[
        "thrust_per_rotor_n"
    ] == pytest.approx(5.0)


def test_astrodynamics_domain():
    assert vis_viva_velocity(7_000_000.0, 7_000_000.0) > 7000.0
    e_anom = solve_kepler_elliptic(1.0, 0.1)
    assert e_anom - 0.1 * math.sin(e_anom) == pytest.approx(1.0, abs=1e-10)
    nu = mean_to_true_anomaly(1.0, 0.1)
    assert true_to_mean_anomaly(nu, 0.1) == pytest.approx(1.0, abs=1e-9)
    rv = coe_to_rv(7_000_000.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    assert rv["position_m"][0] == pytest.approx(7_000_000.0)
    assert (
        j2_secular_rates(7_000_000.0, 0.001, math.radians(98.0))["raan_rate_rad_s"]
        > 0.0
    )
    assert hyperbolic_excess_velocity(c3_energy(3000.0)) == pytest.approx(3000.0)
    assert periapsis_apoapsis(10_000_000.0, 0.2)["periapsis_radius_m"] == pytest.approx(
        8_000_000.0
    )
    prop = propagate_two_body_rk4(rv["position_m"], rv["velocity_m_s"], 60.0, 5.0)
    assert prop["steps"] == 12


def test_flight_mechanics_structures_thermal_gnc_design_mission():
    assert coordinated_turn_performance(100.0, math.radians(60.0))[
        "load_factor"
    ] == pytest.approx(2.0)
    assert climb_performance(2000.0, 1000.0, 10000.0, 50.0)[
        "rate_of_climb_m_s"
    ] == pytest.approx(5.0)
    assert glide_performance(15.0, 1000.0)["glide_range_m"] == pytest.approx(15_000.0)
    assert jet_breguet_range(250.0, 2e-5, 16.0, 50000.0, 40000.0) > 0.0
    assert propeller_breguet_endurance(0.8, 8e-8, 12.0, 60.0, 1500.0, 1200.0) > 0.0
    assert takeoff_ground_roll(10000.0, 3000.0, 200.0, 1000.0, 30.0) > 0.0
    assert static_margin(0.35, 0.25) == pytest.approx(0.10)
    assert neutral_point_position(0.25, 0.5, 4.0, 5.0, 0.3, 0.9) > 0.25

    assert axial_bar_analysis(1000.0, 0.01, 2.0, 70e9)[
        "axial_stress_pa"
    ] == pytest.approx(1e5)
    assert beam_bending_stress(1000.0, 0.05, 1e-5) == pytest.approx(5e6)
    assert cantilever_tip_deflection(100.0, 1.0, 70e9, 1e-6) > 0.0
    assert simply_supported_center_deflection(100.0, 1.0, 70e9, 1e-6) > 0.0
    assert circular_shaft_torsion(500.0, 0.05, 1e-5, 1.0, 26e9)[
        "max_shear_stress_pa"
    ] == pytest.approx(2.5e6)
    assert euler_buckling_load(70e9, 1e-6, 2.0) > 0.0
    assert von_mises_stress_2d(100e6, 0.0, 0.0) == pytest.approx(100e6)
    assert thin_walled_pressure_vessel(1e6, 1.0, 0.01)[
        "hoop_stress_pa"
    ] == pytest.approx(1e8)

    assert conduction_1d_heat_rate(200.0, 1.0, 10.0, 0.1) == pytest.approx(20_000.0)
    assert series_thermal_resistance_heat_rate(100.0, [1.0, 4.0])[
        "heat_rate_w"
    ] == pytest.approx(20.0)
    assert convection_heat_rate(50.0, 2.0, 350.0, 300.0) == pytest.approx(5000.0)
    assert radiation_heat_rate(0.9, 1.0, 300.0, 0.0) > 0.0
    assert stagnation_and_recovery_temperature(220.0, 2.0)[
        "stagnation_temperature_k"
    ] == pytest.approx(396.0)
    assert sutton_graves_stagnation_heat_flux(1e-3, 7000.0, 0.5) > 0.0

    ecef = geodetic_to_ecef(math.radians(45.0), math.radians(10.0), 1000.0)
    geo = ecef_to_geodetic(ecef["x_m"], ecef["y_m"], ecef["z_m"])
    assert geo["latitude_rad"] == pytest.approx(math.radians(45.0), abs=1e-9)
    assert geo["altitude_m"] == pytest.approx(1000.0, abs=1e-4)
    q = quaternion_normalize(euler_zyx_to_quaternion(0.1, -0.2, 0.3))
    eul = quaternion_to_euler_zyx(q)
    assert eul["roll_rad"] == pytest.approx(0.1, abs=1e-9)
    assert quaternion_multiply([1.0, 0.0, 0.0, 0.0], q) == pytest.approx(q)
    assert pid_step(1.0, 0.5, 0.0, 0.1, 2.0, 0.5, 0.1)["control_output"] > 0.0
    assert scalar_kalman_update(10.0, 1.0, 12.0, 0.1, 1.0)["posterior_state"] > 10.0

    s = wing_area_from_loading(10000.0, 500.0)
    b = wingspan_from_aspect_ratio(8.0, s)
    assert rectangular_wing_mac(s, b) == pytest.approx(s / b)
    assert thrust_to_weight_ratio(3000.0, 10000.0) == pytest.approx(0.3)
    assert power_to_weight_ratio(5000.0, 1000.0) == pytest.approx(5.0)
    assert electric_uav_endurance(100.0, 0.8, 200.0, 0.75)[
        "endurance_hr"
    ] == pytest.approx(0.3)

    asc = vertical_rocket_ascent_rk4(1000.0, 500.0, 20000.0, 10.0, 40.0, 0.5)
    assert asc["burnout_altitude_m"] > 0.0
    assert mission_delta_v_budget([3000.0, 1000.0], 0.1)[
        "total_budget_delta_v_m_s"
    ] == pytest.approx(4400.0)
