"""MCP server integration tests for AeroMCP.

These tests exercise the ten registered MCP tools through the SDK's
in-memory Client, verifying that the server correctly wraps the existing
engineering calculation functions.
"""

from __future__ import annotations

import asyncio
import json

import pytest
from mcp import Client

from aeromcp_engineering.server import mcp


async def _call_tool(tool_name: str, arguments: dict):
    """Call an MCP tool through the in-memory Client and return the result."""
    async with Client(mcp, raise_exceptions=True) as client:
        return await client.call_tool(tool_name, arguments)


def _parse_tool_result(result) -> dict:
    """Extract the structured result dict from a CallToolResult's text content."""
    assert not result.is_error, f"Tool call returned an error: {result.content[0].text}"
    text = result.content[0].text
    return json.loads(text)


def test_calculate_dynamic_pressure() -> None:
    """Dynamic pressure: q = 0.5 * 1.225 * 50**2 = 1531.25 Pa."""
    result = asyncio.run(
        _call_tool(
            "calculate_dynamic_pressure",
            {
                "density_kg_m3": 1.225,
                "velocity_m_s": 50.0,
            },
        )
    )
    data = _parse_tool_result(result)
    assert data["result"] == pytest.approx(1531.25)
    assert data["unit"] == "Pa"
    assert data["equation"] == "q = 0.5 * density * velocity**2"


def test_calculate_lift_force() -> None:
    """Lift force: L = 0.5 * 1.225 * 50**2 * 12 * 0.8 = 14700 N."""
    result = asyncio.run(
        _call_tool(
            "calculate_lift_force",
            {
                "density_kg_m3": 1.225,
                "velocity_m_s": 50.0,
                "reference_area_m2": 12.0,
                "lift_coefficient": 0.8,
            },
        )
    )
    data = _parse_tool_result(result)
    assert data["result"] == pytest.approx(14700.0)
    assert data["unit"] == "N"
    assert data["equation"] == "L = 0.5 * density * velocity**2 * area * CL"


def test_calculate_drag_force() -> None:
    """Drag force: D = 0.5 * 1.225 * 50**2 * 12 * 0.03 = 551.25 N."""
    result = asyncio.run(
        _call_tool(
            "calculate_drag_force",
            {
                "density_kg_m3": 1.225,
                "velocity_m_s": 50.0,
                "reference_area_m2": 12.0,
                "drag_coefficient": 0.03,
            },
        )
    )
    data = _parse_tool_result(result)
    assert data["result"] == pytest.approx(551.25)
    assert data["unit"] == "N"
    assert data["equation"] == "D = 0.5 * density * velocity**2 * area * CD"


def test_calculate_lift_coefficient() -> None:
    """Lift coefficient: CL = 1200 / (0.5 * 1.225 * 50**2 * 12) approx 0.06530612245."""
    result = asyncio.run(
        _call_tool(
            "calculate_lift_coefficient",
            {
                "lift_force_n": 1200.0,
                "density_kg_m3": 1.225,
                "velocity_m_s": 50.0,
                "reference_area_m2": 12.0,
            },
        )
    )
    data = _parse_tool_result(result)
    assert data["result"] == pytest.approx(0.06530612245, rel=1e-9)
    assert data["unit"] == "dimensionless"
    assert data["equation"] == "CL = L / (0.5 * density * velocity**2 * area)"


def test_calculate_reynolds_number() -> None:
    """Reynolds number: Re = 1.225 * 50 * 1.5 / 1.7894e-5 approx 5134402.59304795."""
    result = asyncio.run(
        _call_tool(
            "calculate_reynolds_number",
            {
                "density_kg_m3": 1.225,
                "velocity_m_s": 50.0,
                "characteristic_length_m": 1.5,
                "dynamic_viscosity_pa_s": 1.7894e-5,
            },
        )
    )
    data = _parse_tool_result(result)
    assert data["result"] == pytest.approx(5134402.59304795, rel=1e-9)
    assert data["unit"] == "dimensionless"
    assert (
        data["equation"]
        == "Re = density * velocity * characteristic_length / dynamic_viscosity"
    )


def test_tools_are_registered() -> None:
    """All ten expected tools are registered with the MCP server."""
    tools = asyncio.run(_list_tool_names())
    expected = {
        "calculate_dynamic_pressure",
        "calculate_lift_force",
        "calculate_drag_force",
        "calculate_lift_coefficient",
        "calculate_reynolds_number",
        "calculate_isa_troposphere",
        "calculate_circular_orbital_velocity",
        "calculate_orbital_period",
        "calculate_escape_velocity",
        "calculate_hohmann_transfer",
    }
    assert expected.issubset(tools)


async def _list_tool_names() -> set[str]:
    """List the names of all registered MCP tools."""
    async with Client(mcp, raise_exceptions=True) as client:
        response = await client.list_tools()
        return {tool.name for tool in response.tools}


def test_invalid_input_negative_density() -> None:
    """Negative air density must produce a meaningful tool error."""
    result = asyncio.run(
        _call_tool(
            "calculate_dynamic_pressure",
            {
                "density_kg_m3": -1.225,
                "velocity_m_s": 50.0,
            },
        )
    )
    assert result.is_error is True


def test_invalid_input_zero_density() -> None:
    """Zero air density must produce a meaningful tool error."""
    result = asyncio.run(
        _call_tool(
            "calculate_dynamic_pressure",
            {
                "density_kg_m3": 0.0,
                "velocity_m_s": 50.0,
            },
        )
    )
    assert result.is_error is True


def test_invalid_input_negative_velocity() -> None:
    """Negative velocity must produce a meaningful tool error."""
    result = asyncio.run(
        _call_tool(
            "calculate_dynamic_pressure",
            {
                "density_kg_m3": 1.225,
                "velocity_m_s": -50.0,
            },
        )
    )
    assert result.is_error is True


def test_invalid_input_negative_drag_coefficient() -> None:
    """Negative drag coefficient must produce a meaningful tool error."""
    result = asyncio.run(
        _call_tool(
            "calculate_drag_force",
            {
                "density_kg_m3": 1.225,
                "velocity_m_s": 50.0,
                "reference_area_m2": 12.0,
                "drag_coefficient": -0.03,
            },
        )
    )
    assert result.is_error is True


def test_invalid_input_zero_velocity_for_lift_coefficient() -> None:
    """Zero velocity for lift coefficient must produce a meaningful tool error."""
    result = asyncio.run(
        _call_tool(
            "calculate_lift_coefficient",
            {
                "lift_force_n": 1200.0,
                "density_kg_m3": 1.225,
                "velocity_m_s": 0.0,
                "reference_area_m2": 12.0,
            },
        )
    )
    assert result.is_error is True


def test_calculate_isa_troposphere_sea_level() -> None:
    """ISA troposphere at H = 0 m: T = 288.15 K, P = 101325 Pa,
    rho approx 1.225 kg/m^3, a approx 340.294 m/s."""
    result = asyncio.run(
        _call_tool(
            "calculate_isa_troposphere",
            {
                "geopotential_altitude_m": 0.0,
            },
        )
    )
    assert result.is_error is False
    text = result.content[0].text
    data = json.loads(text)
    assert data["model"] == "1976 U.S. Standard Atmosphere - Troposphere"
    assert data["valid_altitude_range_m"] == [0.0, 11000.0]
    assert data["units"]["geopotential_altitude_m"] == "m"
    assert data["units"]["temperature_k"] == "K"
    assert data["units"]["pressure_pa"] == "Pa"
    assert data["units"]["density_kg_m3"] == "kg/m^3"
    assert data["units"]["speed_of_sound_m_s"] == "m/s"
    res = data["result"]
    assert res["geopotential_altitude_m"] == pytest.approx(0.0)
    assert res["temperature_k"] == pytest.approx(288.15)
    assert res["pressure_pa"] == pytest.approx(101325.0)
    assert res["density_kg_m3"] == pytest.approx(1.225, rel=1e-2)
    assert res["speed_of_sound_m_s"] == pytest.approx(340.294, rel=1e-3)


def test_calculate_isa_troposphere_intermediate() -> None:
    """ISA troposphere at H = 5000 m: verify all outputs against
    independently evaluated equations."""
    h = 5000.0
    result = asyncio.run(
        _call_tool(
            "calculate_isa_troposphere",
            {
                "geopotential_altitude_m": h,
            },
        )
    )
    assert result.is_error is False
    text = result.content[0].text
    data = json.loads(text)
    res = data["result"]

    expected_temperature = 288.15 - 0.0065 * h
    exponent = 9.80665 / (287.05287 * 0.0065)
    expected_pressure = 101325.0 * (expected_temperature / 288.15) ** exponent
    expected_density = expected_pressure / (287.05287 * expected_temperature)
    expected_speed_of_sound = (1.4 * 287.05287 * expected_temperature) ** 0.5

    assert res["geopotential_altitude_m"] == pytest.approx(h)
    assert res["temperature_k"] == pytest.approx(expected_temperature, rel=1e-9)
    assert res["pressure_pa"] == pytest.approx(expected_pressure, rel=1e-9)
    assert res["density_kg_m3"] == pytest.approx(expected_density, rel=1e-9)
    assert res["speed_of_sound_m_s"] == pytest.approx(expected_speed_of_sound, rel=1e-9)


def test_calculate_isa_troposphere_upper_boundary() -> None:
    """ISA troposphere at H = 11000 m: T = 216.65 K, P approx 22632.04 Pa."""
    result = asyncio.run(
        _call_tool(
            "calculate_isa_troposphere",
            {
                "geopotential_altitude_m": 11000.0,
            },
        )
    )
    assert result.is_error is False
    text = result.content[0].text
    data = json.loads(text)
    res = data["result"]

    assert res["geopotential_altitude_m"] == pytest.approx(11000.0)
    assert res["temperature_k"] == pytest.approx(216.65)
    assert res["pressure_pa"] == pytest.approx(22632.04, rel=1e-4)


def test_calculate_isa_troposphere_negative_altitude() -> None:
    """Negative geopotential altitude must produce a tool error."""
    result = asyncio.run(
        _call_tool(
            "calculate_isa_troposphere",
            {
                "geopotential_altitude_m": -100.0,
            },
        )
    )
    assert result.is_error is True


def test_calculate_isa_troposphere_altitude_above_max() -> None:
    """Altitude above 11000 m must produce a tool error."""
    result = asyncio.run(
        _call_tool(
            "calculate_isa_troposphere",
            {
                "geopotential_altitude_m": 11001.0,
            },
        )
    )
    assert result.is_error is True


def test_calculate_isa_troposphere_discoverable() -> None:
    """calculate_isa_troposphere is discoverable alongside all five
    existing aerodynamic tools and all four astrodynamics tools."""
    tools = asyncio.run(_list_tool_names())
    expected = {
        "calculate_dynamic_pressure",
        "calculate_lift_force",
        "calculate_drag_force",
        "calculate_lift_coefficient",
        "calculate_reynolds_number",
        "calculate_isa_troposphere",
        "calculate_circular_orbital_velocity",
        "calculate_orbital_period",
        "calculate_escape_velocity",
        "calculate_hohmann_transfer",
    }
    assert expected.issubset(tools)


MU_EARTH = 3.986004418e14


def test_calculate_circular_orbital_velocity() -> None:
    """Circular orbital velocity at r = 7,000,000 m around Earth."""
    result = asyncio.run(
        _call_tool(
            "calculate_circular_orbital_velocity",
            {
                "central_body_mu_m3_s2": MU_EARTH,
                "orbital_radius_m": 7_000_000.0,
            },
        )
    )
    data = _parse_tool_result(result)
    assert data["result"] == pytest.approx(7546.053290107542)
    assert data["unit"] == "m/s"
    assert data["equation"] == "v = sqrt(mu / r)"


def test_calculate_orbital_period() -> None:
    """Orbital period at a = 7,000,000 m around Earth."""
    result = asyncio.run(
        _call_tool(
            "calculate_orbital_period",
            {
                "central_body_mu_m3_s2": MU_EARTH,
                "semi_major_axis_m": 7_000_000.0,
            },
        )
    )
    data = _parse_tool_result(result)
    assert data["result"] == pytest.approx(5828.516637686015)
    assert data["unit"] == "s"
    assert data["equation"] == "T = 2 * pi * sqrt(a**3 / mu)"


def test_calculate_escape_velocity() -> None:
    """Escape velocity at r = 7,000,000 m around Earth."""
    result = asyncio.run(
        _call_tool(
            "calculate_escape_velocity",
            {
                "central_body_mu_m3_s2": MU_EARTH,
                "distance_from_center_m": 7_000_000.0,
            },
        )
    )
    data = _parse_tool_result(result)
    assert data["result"] == pytest.approx(10671.730905260201)
    assert data["unit"] == "m/s"
    assert data["equation"] == "v_escape = sqrt(2 * mu / r)"


def test_calculate_hohmann_transfer_outward() -> None:
    """Outward Hohmann transfer from 7,000 km to 42,164 km around Earth."""
    result = asyncio.run(
        _call_tool(
            "calculate_hohmann_transfer",
            {
                "central_body_mu_m3_s2": MU_EARTH,
                "initial_orbit_radius_m": 7_000_000.0,
                "final_orbit_radius_m": 42_164_000.0,
            },
        )
    )
    assert result.is_error is False
    text = result.content[0].text
    data = json.loads(text)
    assert data["model"] == "Two-body impulsive Hohmann transfer"
    assert data["assumptions"] == [
        "Initial and final circular orbits",
        "Coplanar transfer",
        "Two instantaneous tangential burns",
        "Constant central-body gravitational parameter",
    ]
    res = data["result"]
    assert res["initial_orbit_radius_m"] == pytest.approx(7_000_000.0)
    assert res["final_orbit_radius_m"] == pytest.approx(42_164_000.0)
    assert res["transfer_semi_major_axis_m"] == pytest.approx(24_582_000.0)
    assert res["departure_delta_v_m_s"] == pytest.approx(2336.7957823862034, rel=1e-9)
    assert res["arrival_delta_v_m_s"] == pytest.approx(1433.9314509179262, rel=1e-9)
    assert res["total_delta_v_m_s"] == pytest.approx(3770.7272333041296, rel=1e-9)
    assert res["transfer_time_s"] == pytest.approx(19178.15420570903, rel=1e-9)
    assert res["transfer_direction"] == "outward"
    assert res["burn_direction"] == "prograde"
    units = data["units"]
    assert units["initial_orbit_radius_m"] == "m"
    assert units["final_orbit_radius_m"] == "m"
    assert units["transfer_semi_major_axis_m"] == "m"
    assert units["departure_delta_v_m_s"] == "m/s"
    assert units["arrival_delta_v_m_s"] == "m/s"
    assert units["total_delta_v_m_s"] == "m/s"
    assert units["transfer_time_s"] == "s"
    assert units["transfer_direction"] == "dimensionless"
    assert units["burn_direction"] == "dimensionless"


def test_calculate_hohmann_transfer_inward() -> None:
    """Inward Hohmann transfer from 42,164 km to 7,000 km around Earth."""
    result = asyncio.run(
        _call_tool(
            "calculate_hohmann_transfer",
            {
                "central_body_mu_m3_s2": MU_EARTH,
                "initial_orbit_radius_m": 42_164_000.0,
                "final_orbit_radius_m": 7_000_000.0,
            },
        )
    )
    assert result.is_error is False
    text = result.content[0].text
    data = json.loads(text)
    res = data["result"]
    assert res["transfer_direction"] == "inward"
    assert res["burn_direction"] == "retrograde"
    assert res["total_delta_v_m_s"] == pytest.approx(3770.7272333041296, rel=1e-9)
    assert res["transfer_time_s"] == pytest.approx(19178.15420570903, rel=1e-9)


def test_calculate_circular_orbital_velocity_zero_mu() -> None:
    """Zero gravitational parameter must produce a tool error."""
    result = asyncio.run(
        _call_tool(
            "calculate_circular_orbital_velocity",
            {
                "central_body_mu_m3_s2": 0.0,
                "orbital_radius_m": 7_000_000.0,
            },
        )
    )
    assert result.is_error is True


def test_calculate_circular_orbital_velocity_negative_mu() -> None:
    """Negative gravitational parameter must produce a tool error."""
    result = asyncio.run(
        _call_tool(
            "calculate_circular_orbital_velocity",
            {
                "central_body_mu_m3_s2": -MU_EARTH,
                "orbital_radius_m": 7_000_000.0,
            },
        )
    )
    assert result.is_error is True


def test_calculate_circular_orbital_velocity_zero_radius() -> None:
    """Zero orbital radius must produce a tool error."""
    result = asyncio.run(
        _call_tool(
            "calculate_circular_orbital_velocity",
            {
                "central_body_mu_m3_s2": MU_EARTH,
                "orbital_radius_m": 0.0,
            },
        )
    )
    assert result.is_error is True


def test_calculate_circular_orbital_velocity_negative_radius() -> None:
    """Negative orbital radius must produce a tool error."""
    result = asyncio.run(
        _call_tool(
            "calculate_circular_orbital_velocity",
            {
                "central_body_mu_m3_s2": MU_EARTH,
                "orbital_radius_m": -7_000_000.0,
            },
        )
    )
    assert result.is_error is True


def test_calculate_hohmann_transfer_equal_radii() -> None:
    """Equal Hohmann orbit radii must produce a tool error."""
    result = asyncio.run(
        _call_tool(
            "calculate_hohmann_transfer",
            {
                "central_body_mu_m3_s2": MU_EARTH,
                "initial_orbit_radius_m": 7_000_000.0,
                "final_orbit_radius_m": 7_000_000.0,
            },
        )
    )
    assert result.is_error is True
