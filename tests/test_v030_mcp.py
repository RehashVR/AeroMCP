"""MCP server integration tests for AeroMCP v0.3.0 (tools, resources, prompts)."""

from __future__ import annotations

import asyncio

from aeromcp_engineering.server import mcp


def test_mcp_tool_count_and_original_tools_preserved():
    tools = asyncio.run(mcp.list_tools())
    names = {t.name for t in tools}
    assert len(names) >= 55
    original_10 = {
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
    assert original_10.issubset(names)


def test_mcp_resources_and_prompts_registered():
    resources = asyncio.run(mcp.list_resources())
    uris = {str(r.uri) for r in resources}
    assert {
        "aeromcp://capabilities",
        "aeromcp://engineering-domains",
        "aeromcp://constants",
        "aeromcp://units",
        "aeromcp://model-catalog",
    }.issubset(uris)

    prompts = asyncio.run(mcp.list_prompts())
    prompt_names = {p.name for p in prompts}
    assert len(prompt_names) >= 7
    assert "preliminary_aircraft_design_analysis" in prompt_names
