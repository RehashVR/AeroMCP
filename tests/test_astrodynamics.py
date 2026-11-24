"""Tests for the astrodynamics orbital mechanics module."""

from __future__ import annotations

import math

import pytest

from aeromcp.astrodynamics import (
    circular_orbital_velocity,
    escape_velocity,
    hohmann_transfer,
    orbital_period,
)

MU_EARTH = 3.986004418e14


# ---------------------------------------------------------------------------
# Reference case 1: Circular orbital velocity
# ---------------------------------------------------------------------------


def test_circular_orbital_velocity_reference_case() -> None:
    """v = sqrt(mu / r) at r = 7,000,000 m around Earth."""
    result = circular_orbital_velocity(MU_EARTH, 7_000_000.0)
    assert result == pytest.approx(7546.053290107542)


def test_circular_orbital_velocity_zero_radius() -> None:
    """Zero orbital radius must raise ValueError."""
    with pytest.raises(ValueError):
        circular_orbital_velocity(MU_EARTH, 0.0)


def test_circular_orbital_velocity_negative_radius() -> None:
    """Negative orbital radius must raise ValueError."""
    with pytest.raises(ValueError):
        circular_orbital_velocity(MU_EARTH, -7_000_000.0)


# ---------------------------------------------------------------------------
# Reference case 2: Orbital period
# ---------------------------------------------------------------------------


def test_orbital_period_reference_case() -> None:
    """T = 2*pi*sqrt(a**3/mu) at a = 7,000,000 m around Earth."""
    result = orbital_period(MU_EARTH, 7_000_000.0)
    assert result == pytest.approx(5828.516637686015)


def test_orbital_period_zero_semi_major_axis() -> None:
    """Zero semi-major axis must raise ValueError."""
    with pytest.raises(ValueError):
        orbital_period(MU_EARTH, 0.0)


def test_orbital_period_negative_semi_major_axis() -> None:
    """Negative semi-major axis must raise ValueError."""
    with pytest.raises(ValueError):
        orbital_period(MU_EARTH, -7_000_000.0)


# ---------------------------------------------------------------------------
# Reference case 3: Escape velocity
# ---------------------------------------------------------------------------


def test_escape_velocity_reference_case() -> None:
    """v_escape = sqrt(2*mu/r) at r = 7,000,000 m around Earth."""
    result = escape_velocity(MU_EARTH, 7_000_000.0)
    assert result == pytest.approx(10671.730905260201)


def test_escape_velocity_equals_sqrt2_times_circular_velocity() -> None:
    """Escape velocity must equal sqrt(2) times circular orbital velocity
    at the same radius."""
    r = 7_000_000.0
    v_circ = circular_orbital_velocity(MU_EARTH, r)
    v_esc = escape_velocity(MU_EARTH, r)
    assert v_esc == pytest.approx(math.sqrt(2.0) * v_circ)


def test_escape_velocity_zero_distance() -> None:
    """Zero distance from centre must raise ValueError."""
    with pytest.raises(ValueError):
        escape_velocity(MU_EARTH, 0.0)


# ---------------------------------------------------------------------------
# Reference case 4: Outward Hohmann transfer
# ---------------------------------------------------------------------------


def test_hohmann_transfer_outward_reference_case() -> None:
    """Outward Hohmann transfer from 7,000 km to 42,164 km around Earth."""
    result = hohmann_transfer(MU_EARTH, 7_000_000.0, 42_164_000.0)

    assert result["initial_orbit_radius_m"] == pytest.approx(7_000_000.0)
    assert result["final_orbit_radius_m"] == pytest.approx(42_164_000.0)
    assert result["transfer_semi_major_axis_m"] == pytest.approx(24_582_000.0)
    assert result["departure_delta_v_m_s"] == pytest.approx(
        2336.7957823862034, rel=1e-9
    )
    assert result["arrival_delta_v_m_s"] == pytest.approx(1433.9314509179262, rel=1e-9)
    assert result["total_delta_v_m_s"] == pytest.approx(3770.7272333041296, rel=1e-9)
    assert result["transfer_time_s"] == pytest.approx(19178.15420570903, rel=1e-9)
    assert result["transfer_direction"] == "outward"
    assert result["burn_direction"] == "prograde"


# ---------------------------------------------------------------------------
# Reference case 5: Inward Hohmann transfer
# ---------------------------------------------------------------------------


def test_hohmann_transfer_inward_reference_case() -> None:
    """Inward Hohmann transfer from 42,164 km to 7,000 km around Earth."""
    result = hohmann_transfer(MU_EARTH, 42_164_000.0, 7_000_000.0)

    assert result["initial_orbit_radius_m"] == pytest.approx(42_164_000.0)
    assert result["final_orbit_radius_m"] == pytest.approx(7_000_000.0)
    assert result["transfer_semi_major_axis_m"] == pytest.approx(24_582_000.0)
    assert result["departure_delta_v_m_s"] == pytest.approx(
        1433.9314509179262, rel=1e-9
    )
    assert result["arrival_delta_v_m_s"] == pytest.approx(2336.7957823862034, rel=1e-9)
    assert result["total_delta_v_m_s"] == pytest.approx(3770.7272333041296, rel=1e-9)
    assert result["transfer_direction"] == "inward"
    assert result["burn_direction"] == "retrograde"


# ---------------------------------------------------------------------------
# Consistency tests
# ---------------------------------------------------------------------------


def test_hohmann_outward_inward_consistent_total_delta_v() -> None:
    """Outward and inward Hohmann transfers must produce the same total
    Delta-V when radii are swapped."""
    outward = hohmann_transfer(MU_EARTH, 7_000_000.0, 42_164_000.0)
    inward = hohmann_transfer(MU_EARTH, 42_164_000.0, 7_000_000.0)
    assert outward["total_delta_v_m_s"] == pytest.approx(
        inward["total_delta_v_m_s"], rel=1e-9
    )


def test_orbital_period_is_positive() -> None:
    """Orbital period must always be positive for valid inputs."""
    result = orbital_period(MU_EARTH, 7_000_000.0)
    assert result > 0.0


# ---------------------------------------------------------------------------
# Validation: TypeError for non-numeric and boolean inputs
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "func,args",
    [
        (circular_orbital_velocity, ("not_a_number", 7_000_000.0)),
        (circular_orbital_velocity, (MU_EARTH, "not_a_number")),
        (circular_orbital_velocity, (True, 7_000_000.0)),
        (circular_orbital_velocity, (MU_EARTH, False)),
        (orbital_period, ("not_a_number", 7_000_000.0)),
        (orbital_period, (MU_EARTH, "not_a_number")),
        (orbital_period, (True, 7_000_000.0)),
        (orbital_period, (MU_EARTH, False)),
        (escape_velocity, ("not_a_number", 7_000_000.0)),
        (escape_velocity, (MU_EARTH, "not_a_number")),
        (escape_velocity, (True, 7_000_000.0)),
        (escape_velocity, (MU_EARTH, False)),
        (hohmann_transfer, ("not_a_number", 7_000_000.0, 42_164_000.0)),
        (hohmann_transfer, (MU_EARTH, "not_a_number", 42_164_000.0)),
        (hohmann_transfer, (MU_EARTH, 7_000_000.0, "not_a_number")),
        (hohmann_transfer, (True, 7_000_000.0, 42_164_000.0)),
        (hohmann_transfer, (MU_EARTH, True, 42_164_000.0)),
        (hohmann_transfer, (MU_EARTH, 7_000_000.0, False)),
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
        (circular_orbital_velocity, (float("nan"), 7_000_000.0)),
        (circular_orbital_velocity, (MU_EARTH, float("nan"))),
        (circular_orbital_velocity, (float("inf"), 7_000_000.0)),
        (circular_orbital_velocity, (MU_EARTH, float("-inf"))),
        (orbital_period, (float("nan"), 7_000_000.0)),
        (orbital_period, (MU_EARTH, float("nan"))),
        (orbital_period, (float("inf"), 7_000_000.0)),
        (orbital_period, (MU_EARTH, float("-inf"))),
        (escape_velocity, (float("nan"), 7_000_000.0)),
        (escape_velocity, (MU_EARTH, float("nan"))),
        (escape_velocity, (float("inf"), 7_000_000.0)),
        (escape_velocity, (MU_EARTH, float("-inf"))),
        (hohmann_transfer, (float("nan"), 7_000_000.0, 42_164_000.0)),
        (hohmann_transfer, (MU_EARTH, float("nan"), 42_164_000.0)),
        (hohmann_transfer, (MU_EARTH, 7_000_000.0, float("nan"))),
        (hohmann_transfer, (MU_EARTH, float("inf"), 42_164_000.0)),
        (hohmann_transfer, (MU_EARTH, 7_000_000.0, float("-inf"))),
    ],
)
def test_value_error_for_non_finite(func, args) -> None:
    """NaN and infinite inputs must raise ValueError."""
    with pytest.raises(ValueError):
        func(*args)


# ---------------------------------------------------------------------------
# Validation: zero and negative gravitational parameter
# ---------------------------------------------------------------------------


def test_circular_orbital_velocity_zero_mu() -> None:
    """Zero gravitational parameter must raise ValueError."""
    with pytest.raises(ValueError):
        circular_orbital_velocity(0.0, 7_000_000.0)


def test_circular_orbital_velocity_negative_mu() -> None:
    """Negative gravitational parameter must raise ValueError."""
    with pytest.raises(ValueError):
        circular_orbital_velocity(-MU_EARTH, 7_000_000.0)


def test_orbital_period_zero_mu() -> None:
    """Zero gravitational parameter must raise ValueError."""
    with pytest.raises(ValueError):
        orbital_period(0.0, 7_000_000.0)


def test_escape_velocity_zero_mu() -> None:
    """Zero gravitational parameter must raise ValueError."""
    with pytest.raises(ValueError):
        escape_velocity(0.0, 7_000_000.0)


def test_hohmann_transfer_zero_mu() -> None:
    """Zero gravitational parameter must raise ValueError."""
    with pytest.raises(ValueError):
        hohmann_transfer(0.0, 7_000_000.0, 42_164_000.0)


# ---------------------------------------------------------------------------
# Validation: zero and negative final orbit radius
# ---------------------------------------------------------------------------


def test_hohmann_transfer_zero_final_radius() -> None:
    """Zero final orbit radius must raise ValueError."""
    with pytest.raises(ValueError):
        hohmann_transfer(MU_EARTH, 7_000_000.0, 0.0)


def test_hohmann_transfer_negative_final_radius() -> None:
    """Negative final orbit radius must raise ValueError."""
    with pytest.raises(ValueError):
        hohmann_transfer(MU_EARTH, 7_000_000.0, -42_164_000.0)


# ---------------------------------------------------------------------------
# Validation: equal initial and final radii
# ---------------------------------------------------------------------------


def test_hohmann_transfer_equal_radii() -> None:
    """Equal initial and final orbit radii must raise ValueError."""
    with pytest.raises(ValueError):
        hohmann_transfer(MU_EARTH, 7_000_000.0, 7_000_000.0)


# ---------------------------------------------------------------------------
# Validation: None inputs
# ---------------------------------------------------------------------------


def test_circular_orbital_velocity_none_mu() -> None:
    """None gravitational parameter must raise TypeError."""
    with pytest.raises(TypeError):
        circular_orbital_velocity(None, 7_000_000.0)


def test_circular_orbital_velocity_none_radius() -> None:
    """None orbital radius must raise TypeError."""
    with pytest.raises(TypeError):
        circular_orbital_velocity(MU_EARTH, None)


def test_hohmann_transfer_none_inputs() -> None:
    """None Hohmann transfer inputs must raise TypeError."""
    with pytest.raises(TypeError):
        hohmann_transfer(None, 7_000_000.0, 42_164_000.0)


def test_hohmann_transfer_none_final_radius() -> None:
    """None final orbit radius must raise TypeError."""
    with pytest.raises(TypeError):
        hohmann_transfer(MU_EARTH, 7_000_000.0, None)


# ---------------------------------------------------------------------------
# Validation: return type
# ---------------------------------------------------------------------------


def test_returns_float() -> None:
    """Single-value calculation functions must return a float."""
    assert isinstance(circular_orbital_velocity(MU_EARTH, 7_000_000.0), float)
    assert isinstance(orbital_period(MU_EARTH, 7_000_000.0), float)
    assert isinstance(escape_velocity(MU_EARTH, 7_000_000.0), float)


def test_hohmann_returns_dict() -> None:
    """hohmann_transfer must return a dictionary."""
    result = hohmann_transfer(MU_EARTH, 7_000_000.0, 42_164_000.0)
    assert isinstance(result, dict)
    assert set(result.keys()) == {
        "initial_orbit_radius_m",
        "final_orbit_radius_m",
        "transfer_semi_major_axis_m",
        "departure_delta_v_m_s",
        "arrival_delta_v_m_s",
        "total_delta_v_m_s",
        "transfer_time_s",
        "transfer_direction",
        "burn_direction",
    }
