"""Shared input validation utilities for AeroMCP engineering calculations.

This module provides reusable validation functions that ensure all engineering
inputs are numeric, finite, and within physically meaningful ranges before any
calculation is performed.

All validation functions raise :class:`TypeError` for incorrect types and
:class:`ValueError` for values that are out of range or non-finite.
"""

from __future__ import annotations

import math
from numbers import Real
from typing import Union

# Accepted numeric types for engineering inputs. bool is explicitly excluded
# because bool is a subclass of int in Python but is not a physical measurement.
Numeric = Union[int, float]


def _reject_bool(value: object, name: str) -> None:
    """Reject boolean values, which are not valid physical measurements."""
    if isinstance(value, bool):
        raise TypeError(f"{name} must be a real number, not a boolean. Got {value!r}.")


def _reject_non_numeric(value: object, name: str) -> None:
    """Reject values that are not real numbers (int or float)."""
    if not isinstance(value, Real) or isinstance(value, bool):
        raise TypeError(
            f"{name} must be a real number (int or float). "
            f"Got {type(value).__name__}: {value!r}."
        )


def _reject_non_finite(value: float, name: str) -> None:
    """Reject NaN and infinite values."""
    if math.isnan(value):
        raise ValueError(f"{name} must be a finite number, not NaN.")
    if math.isinf(value):
        raise ValueError(
            f"{name} must be a finite number, not infinity. Got {value!r}."
        )


def validate_positive(value: object, name: str) -> float:
    """Validate that *value* is a strictly positive real number.

    Parameters
    ----------
    value:
        The input value to validate.
    name:
        A human-readable name for the parameter, used in error messages.

    Returns
    -------
    float
        The validated value as a float.

    Raises
    ------
    TypeError
        If *value* is not a real number or is a boolean.
    ValueError
        If *value* is NaN, infinite, or not strictly greater than zero.
    """
    _reject_non_numeric(value, name)
    _reject_bool(value, name)
    result = float(value)
    _reject_non_finite(result, name)
    if result <= 0.0:
        raise ValueError(f"{name} must be strictly positive. Got {result!r}.")
    return result


def validate_non_negative(value: object, name: str) -> float:
    """Validate that *value* is a non-negative real number.

    Parameters
    ----------
    value:
        The input value to validate.
    name:
        A human-readable name for the parameter, used in error messages.

    Returns
    -------
    float
        The validated value as a float.

    Raises
    ------
    TypeError
        If *value* is not a real number or is a boolean.
    ValueError
        If *value* is NaN, infinite, or less than zero.
    """
    _reject_non_numeric(value, name)
    _reject_bool(value, name)
    result = float(value)
    _reject_non_finite(result, name)
    if result < 0.0:
        raise ValueError(f"{name} must be non-negative. Got {result!r}.")
    return result


def validate_finite(value: object, name: str) -> float:
    """Validate that *value* is a finite real number.

    The value may be negative, zero, or positive; only finiteness is checked.

    Parameters
    ----------
    value:
        The input value to validate.
    name:
        A human-readable name for the parameter, used in error messages.

    Returns
    -------
    float
        The validated value as a float.

    Raises
    ------
    TypeError
        If *value* is not a real number or is a boolean.
    ValueError
        If *value* is NaN or infinite.
    """
    _reject_non_numeric(value, name)
    _reject_bool(value, name)
    result = float(value)
    _reject_non_finite(result, name)
    return result
