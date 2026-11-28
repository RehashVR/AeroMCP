"""Structured result builder for AeroMCP MCP tools."""

from __future__ import annotations

from typing import Any


def build_result(
    *,
    calculation_name: str,
    engineering_domain: str,
    inputs: dict[str, Any],
    results: dict[str, Any],
    output_units: dict[str, str],
    equations: list[str],
    assumptions: list[str],
    model: str,
    validity_limits: list[str],
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    """Build a standardized, JSON-serializable engineering result dictionary."""
    return {
        "calculation_name": calculation_name,
        "engineering_domain": engineering_domain,
        "inputs": inputs,
        "results": results,
        "output_units": output_units,
        "equations": equations,
        "assumptions": assumptions,
        "model": model,
        "validity_limits": validity_limits,
        "warnings": warnings if warnings is not None else [],
    }
