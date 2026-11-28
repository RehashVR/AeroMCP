"""Core engineering utilities for AeroMCP."""

from __future__ import annotations

from aeromcp_engineering.core.errors import (
    AeroMCPError,
    ConvergenceError,
    PhysicalLimitError,
)
from aeromcp_engineering.core.numerical_methods import (
    RootResult,
    bisection,
    rk4_integrate,
    rk4_step,
    safeguarded_newton,
    solve_linear_system,
)
from aeromcp_engineering.core.results import build_result
from aeromcp_engineering.core.units import convert_unit
from aeromcp_engineering.core.validation import (
    validate_finite,
    validate_non_negative,
    validate_positive,
)

__all__ = [
    "AeroMCPError",
    "ConvergenceError",
    "PhysicalLimitError",
    "RootResult",
    "bisection",
    "build_result",
    "convert_unit",
    "rk4_integrate",
    "rk4_step",
    "safeguarded_newton",
    "solve_linear_system",
    "validate_finite",
    "validate_non_negative",
    "validate_positive",
]
