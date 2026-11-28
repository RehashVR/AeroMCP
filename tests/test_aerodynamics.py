"""Comprehensive tests for the aerodynamics computation engine."""

from __future__ import annotations

import pytest

from aeromcp_engineering.aerodynamics import (
    drag_force,
    dynamic_pressure,
    lift_coefficient,
    lift_force,
    reynolds_number,
)

# ---------------------------------------------------------------------------
# Reference case: dynamic pressure
# ---------------------------------------------------------------------------


def test_dynamic_pressure_reference_case() -> None:
    """q = 0.5 * 1.225 * 50**2 = 1531.25 Pa."""
    result = dynamic_pressure(1.225, 50.0)
    assert result == pytest.approx(1531.25)


def test_dynamic_pressure_zero_velocity() -> None:
    """Zero velocity yields zero dynamic pressure."""
    result = dynamic_pressure(1.225, 0.0)
    assert result == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Reference case: lift force
# ---------------------------------------------------------------------------


def test_lift_force_reference_case() -> None:
    """L = 0.5 * 1.225 * 50**2 * 12 * 0.8 = 14700 N."""
    result = lift_force(1.225, 50.0, 12.0, 0.8)
    assert result == pytest.approx(14700.0)


def test_lift_force_zero_velocity() -> None:
    """Zero velocity yields zero lift force."""
    result = lift_force(1.225, 0.0, 12.0, 0.8)
    assert result == pytest.approx(0.0)


def test_lift_force_negative_coefficient() -> None:
    """Negative lift coefficient yields negative lift force."""
    result = lift_force(1.225, 50.0, 12.0, -0.5)
    assert result == pytest.approx(-9187.5)


def test_lift_force_zero_coefficient() -> None:
    """Zero lift coefficient yields zero lift force."""
    result = lift_force(1.225, 50.0, 12.0, 0.0)
    assert result == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Reference case: drag force
# ---------------------------------------------------------------------------


def test_drag_force_reference_case() -> None:
    """D = 0.5 * 1.225 * 50**2 * 12 * 0.03 = 551.25 N."""
    result = drag_force(1.225, 50.0, 12.0, 0.03)
    assert result == pytest.approx(551.25)


def test_drag_force_zero_velocity() -> None:
    """Zero velocity yields zero drag force."""
    result = drag_force(1.225, 0.0, 12.0, 0.03)
    assert result == pytest.approx(0.0)


def test_drag_force_zero_coefficient() -> None:
    """Zero drag coefficient yields zero drag force."""
    result = drag_force(1.225, 50.0, 12.0, 0.0)
    assert result == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Reference case: lift coefficient
# ---------------------------------------------------------------------------


def test_lift_coefficient_reference_case() -> None:
    """CL = 1200 / (0.5 * 1.225 * 50**2 * 12) approx 0.06530612245."""
    result = lift_coefficient(1200.0, 1.225, 50.0, 12.0)
    assert result == pytest.approx(0.06530612245, rel=1e-9)


def test_lift_coefficient_zero_force() -> None:
    """Zero lift force yields zero lift coefficient."""
    result = lift_coefficient(0.0, 1.225, 50.0, 12.0)
    assert result == pytest.approx(0.0)


def test_lift_coefficient_negative_force() -> None:
    """Negative lift force yields negative lift coefficient."""
    result = lift_coefficient(-500.0, 1.225, 50.0, 12.0)
    assert result == pytest.approx(-0.02721088435, rel=1e-9)


# ---------------------------------------------------------------------------
# Reference case: Reynolds number
# ---------------------------------------------------------------------------


def test_reynolds_number_reference_case() -> None:
    """Re = 1.225 * 50 * 1.5 / 1.7894e-5."""
    result = reynolds_number(1.225, 50.0, 1.5, 1.7894e-5)
    expected = 1.225 * 50.0 * 1.5 / 1.7894e-5
    assert result == pytest.approx(expected, rel=1e-9)


def test_reynolds_number_zero_velocity() -> None:
    """Zero velocity yields zero Reynolds number."""
    result = reynolds_number(1.225, 0.0, 1.5, 1.7894e-5)
    assert result == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Validation: TypeError for non-numeric and boolean inputs
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "func,args",
    [
        (dynamic_pressure, ("not_a_number", 50.0)),
        (dynamic_pressure, (1.225, "not_a_number")),
        (dynamic_pressure, (True, 50.0)),
        (dynamic_pressure, (1.225, False)),
        (lift_force, ("not_a_number", 50.0, 12.0, 0.8)),
        (lift_force, (1.225, "not_a_number", 12.0, 0.8)),
        (lift_force, (1.225, 50.0, "not_a_number", 0.8)),
        (lift_force, (1.225, 50.0, 12.0, "not_a_number")),
        (lift_force, (True, 50.0, 12.0, 0.8)),
        (drag_force, ("not_a_number", 50.0, 12.0, 0.03)),
        (drag_force, (1.225, "not_a_number", 12.0, 0.03)),
        (drag_force, (1.225, 50.0, "not_a_number", 0.03)),
        (drag_force, (1.225, 50.0, 12.0, "not_a_number")),
        (lift_coefficient, ("not_a_number", 1.225, 50.0, 12.0)),
        (lift_coefficient, (1200.0, "not_a_number", 50.0, 12.0)),
        (lift_coefficient, (1200.0, 1.225, "not_a_number", 12.0)),
        (lift_coefficient, (1200.0, 1.225, 50.0, "not_a_number")),
        (lift_coefficient, (True, 1.225, 50.0, 12.0)),
        (reynolds_number, ("not_a_number", 50.0, 1.5, 1.7894e-5)),
        (reynolds_number, (1.225, "not_a_number", 1.5, 1.7894e-5)),
        (reynolds_number, (1.225, 50.0, "not_a_number", 1.7894e-5)),
        (reynolds_number, (1.225, 50.0, 1.5, "not_a_number")),
        (reynolds_number, (True, 50.0, 1.5, 1.7894e-5)),
    ],
)
def test_type_error_for_non_numeric_and_bool(func, args) -> None:
    """Non-numeric and boolean inputs must raise TypeError."""
    with pytest.raises(TypeError):
        func(*args)


# ---------------------------------------------------------------------------
# Validation: ValueError for NaN and infinity
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "func,args",
    [
        (dynamic_pressure, (float("nan"), 50.0)),
        (dynamic_pressure, (1.225, float("nan"))),
        (dynamic_pressure, (float("inf"), 50.0)),
        (dynamic_pressure, (1.225, float("-inf"))),
        (lift_force, (float("nan"), 50.0, 12.0, 0.8)),
        (lift_force, (1.225, float("nan"), 12.0, 0.8)),
        (lift_force, (1.225, 50.0, float("inf"), 0.8)),
        (lift_force, (1.225, 50.0, 12.0, float("nan"))),
        (drag_force, (float("nan"), 50.0, 12.0, 0.03)),
        (drag_force, (1.225, 50.0, float("-inf"), 0.03)),
        (drag_force, (1.225, 50.0, 12.0, float("inf"))),
        (lift_coefficient, (float("nan"), 1.225, 50.0, 12.0)),
        (lift_coefficient, (1200.0, float("inf"), 50.0, 12.0)),
        (lift_coefficient, (1200.0, 1.225, float("-inf"), 12.0)),
        (reynolds_number, (float("nan"), 50.0, 1.5, 1.7894e-5)),
        (reynolds_number, (1.225, 50.0, 1.5, float("inf"))),
        (reynolds_number, (1.225, 50.0, float("nan"), 1.7894e-5)),
    ],
)
def test_value_error_for_non_finite(func, args) -> None:
    """NaN and infinite inputs must raise ValueError."""
    with pytest.raises(ValueError):
        func(*args)


# ---------------------------------------------------------------------------
# Validation: dynamic_pressure value errors
# ---------------------------------------------------------------------------


def test_dynamic_pressure_negative_density() -> None:
    """Negative density must raise ValueError."""
    with pytest.raises(ValueError):
        dynamic_pressure(-1.225, 50.0)


def test_dynamic_pressure_zero_density() -> None:
    """Zero density must raise ValueError."""
    with pytest.raises(ValueError):
        dynamic_pressure(0.0, 50.0)


def test_dynamic_pressure_negative_velocity() -> None:
    """Negative velocity must raise ValueError."""
    with pytest.raises(ValueError):
        dynamic_pressure(1.225, -50.0)


# ---------------------------------------------------------------------------
# Validation: lift_force value errors
# ---------------------------------------------------------------------------


def test_lift_force_negative_density() -> None:
    """Negative density must raise ValueError."""
    with pytest.raises(ValueError):
        lift_force(-1.225, 50.0, 12.0, 0.8)


def test_lift_force_zero_density() -> None:
    """Zero density must raise ValueError."""
    with pytest.raises(ValueError):
        lift_force(0.0, 50.0, 12.0, 0.8)


def test_lift_force_negative_velocity() -> None:
    """Negative velocity must raise ValueError."""
    with pytest.raises(ValueError):
        lift_force(1.225, -50.0, 12.0, 0.8)


def test_lift_force_negative_area() -> None:
    """Negative reference area must raise ValueError."""
    with pytest.raises(ValueError):
        lift_force(1.225, 50.0, -12.0, 0.8)


def test_lift_force_zero_area() -> None:
    """Zero reference area must raise ValueError."""
    with pytest.raises(ValueError):
        lift_force(1.225, 50.0, 0.0, 0.8)


def test_lift_force_nan_coefficient() -> None:
    """NaN lift coefficient must raise ValueError."""
    with pytest.raises(ValueError):
        lift_force(1.225, 50.0, 12.0, float("nan"))


# ---------------------------------------------------------------------------
# Validation: drag_force value errors
# ---------------------------------------------------------------------------


def test_drag_force_negative_density() -> None:
    """Negative density must raise ValueError."""
    with pytest.raises(ValueError):
        drag_force(-1.225, 50.0, 12.0, 0.03)


def test_drag_force_zero_density() -> None:
    """Zero density must raise ValueError."""
    with pytest.raises(ValueError):
        drag_force(0.0, 50.0, 12.0, 0.03)


def test_drag_force_negative_velocity() -> None:
    """Negative velocity must raise ValueError."""
    with pytest.raises(ValueError):
        drag_force(1.225, -50.0, 12.0, 0.03)


def test_drag_force_negative_area() -> None:
    """Negative reference area must raise ValueError."""
    with pytest.raises(ValueError):
        drag_force(1.225, 50.0, -12.0, 0.03)


def test_drag_force_zero_area() -> None:
    """Zero reference area must raise ValueError."""
    with pytest.raises(ValueError):
        drag_force(1.225, 50.0, 0.0, 0.03)


def test_drag_force_negative_coefficient() -> None:
    """Negative drag coefficient must raise ValueError."""
    with pytest.raises(ValueError):
        drag_force(1.225, 50.0, 12.0, -0.03)


# ---------------------------------------------------------------------------
# Validation: lift_coefficient value errors
# ---------------------------------------------------------------------------


def test_lift_coefficient_negative_density() -> None:
    """Negative density must raise ValueError."""
    with pytest.raises(ValueError):
        lift_coefficient(1200.0, -1.225, 50.0, 12.0)


def test_lift_coefficient_zero_density() -> None:
    """Zero density must raise ValueError."""
    with pytest.raises(ValueError):
        lift_coefficient(1200.0, 0.0, 50.0, 12.0)


def test_lift_coefficient_zero_velocity() -> None:
    """Zero velocity must raise ValueError (denominator would be zero)."""
    with pytest.raises(ValueError):
        lift_coefficient(1200.0, 1.225, 0.0, 12.0)


def test_lift_coefficient_negative_velocity() -> None:
    """Negative velocity must raise ValueError."""
    with pytest.raises(ValueError):
        lift_coefficient(1200.0, 1.225, -50.0, 12.0)


def test_lift_coefficient_negative_area() -> None:
    """Negative reference area must raise ValueError."""
    with pytest.raises(ValueError):
        lift_coefficient(1200.0, 1.225, 50.0, -12.0)


def test_lift_coefficient_zero_area() -> None:
    """Zero reference area must raise ValueError."""
    with pytest.raises(ValueError):
        lift_coefficient(1200.0, 1.225, 50.0, 0.0)


def test_lift_coefficient_nan_force() -> None:
    """NaN lift force must raise ValueError."""
    with pytest.raises(ValueError):
        lift_coefficient(float("nan"), 1.225, 50.0, 12.0)


# ---------------------------------------------------------------------------
# Validation: reynolds_number value errors
# ---------------------------------------------------------------------------


def test_reynolds_number_negative_density() -> None:
    """Negative density must raise ValueError."""
    with pytest.raises(ValueError):
        reynolds_number(-1.225, 50.0, 1.5, 1.7894e-5)


def test_reynolds_number_zero_density() -> None:
    """Zero density must raise ValueError."""
    with pytest.raises(ValueError):
        reynolds_number(0.0, 50.0, 1.5, 1.7894e-5)


def test_reynolds_number_negative_velocity() -> None:
    """Negative velocity must raise ValueError."""
    with pytest.raises(ValueError):
        reynolds_number(1.225, -50.0, 1.5, 1.7894e-5)


def test_reynolds_number_negative_length() -> None:
    """Negative characteristic length must raise ValueError."""
    with pytest.raises(ValueError):
        reynolds_number(1.225, 50.0, -1.5, 1.7894e-5)


def test_reynolds_number_zero_length() -> None:
    """Zero characteristic length must raise ValueError."""
    with pytest.raises(ValueError):
        reynolds_number(1.225, 50.0, 0.0, 1.7894e-5)


def test_reynolds_number_zero_viscosity() -> None:
    """Zero viscosity must raise ValueError."""
    with pytest.raises(ValueError):
        reynolds_number(1.225, 50.0, 1.5, 0.0)


def test_reynolds_number_negative_viscosity() -> None:
    """Negative viscosity must raise ValueError."""
    with pytest.raises(ValueError):
        reynolds_number(1.225, 50.0, 1.5, -1.7894e-5)


# ---------------------------------------------------------------------------
# Validation: returns are float
# ---------------------------------------------------------------------------


def test_returns_float() -> None:
    """All calculation functions must return a float."""
    assert isinstance(dynamic_pressure(1.225, 50.0), float)
    assert isinstance(lift_force(1.225, 50.0, 12.0, 0.8), float)
    assert isinstance(drag_force(1.225, 50.0, 12.0, 0.03), float)
    assert isinstance(lift_coefficient(1200.0, 1.225, 50.0, 12.0), float)
    assert isinstance(reynolds_number(1.225, 50.0, 1.5, 1.7894e-5), float)
