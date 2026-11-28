"""Custom exception hierarchy for AeroMCP engineering calculations."""

from __future__ import annotations


class AeroMCPError(Exception):
    """Base exception for all AeroMCP-specific errors."""


class ConvergenceError(AeroMCPError):
    """Raised when an iterative numerical solver fails to converge."""


class PhysicalLimitError(AeroMCPError, ValueError):
    """Raised when inputs or intermediate states violate physical limits."""
