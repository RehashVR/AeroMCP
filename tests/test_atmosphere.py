"""Tests for the International Standard Atmosphere (ISA) troposphere module."""

from __future__ import annotations

import math

import pytest

from aeromcp.atmosphere import isa_troposphere

SEA_LEVEL_TEMPERATURE_K = 288.15
SEA_LEVEL_PRESSURE_PA = 101325.0
TEMPERATURE_LAPSE_RATE_K_PER_M = 0.0065
STANDARD_GRAVITY_M_S2 = 9.80665
SPECIFIC_GAS_CONSTANT_J_PER_KG_K = 287.05287
SPECIFIC_HEAT_RATIO = 1.4


def test_sea_level() -> None:
    """At H = 0 m: T = 288.15 K, P = 101325 Pa, rho approx 1.225 kg/m^3,
    a approx 340.294 m/s."""
    result = isa_troposphere(0.0)

    assert result["geopotential_altitude_m"] == pytest.approx(0.0)
    assert result["temperature_k"] == pytest.approx(SEA_LEVEL_TEMPERATURE_K)
    assert result["pressure_pa"] == pytest.approx(SEA_LEVEL_PRESSURE_PA)
    assert result["density_kg_m3"] == pytest.approx(1.225, rel=1e-2)
    assert result["speed_of_sound_m_s"] == pytest.approx(340.294, rel=1e-3)


def test_troposphere_upper_boundary() -> None:
    """At H = 11000 m: T = 216.65 K, P approx 22632.06 Pa."""
    result = isa_troposphere(11000.0)

    assert result["geopotential_altitude_m"] == pytest.approx(11000.0)
    assert result["temperature_k"] == pytest.approx(216.65)
    assert result["pressure_pa"] == pytest.approx(22632.06, rel=1e-4)


def test_intermediate_altitude_5000m() -> None:
    """Independently evaluate each governing equation at H = 5000 m."""
    h = 5000.0

    # Temperature: T = T0 - L * H
    expected_temperature = SEA_LEVEL_TEMPERATURE_K - TEMPERATURE_LAPSE_RATE_K_PER_M * h

    # Pressure: P = P0 * (T / T0) ** (g0 / (R * L))
    exponent = STANDARD_GRAVITY_M_S2 / (
        SPECIFIC_GAS_CONSTANT_J_PER_KG_K * TEMPERATURE_LAPSE_RATE_K_PER_M
    )
    expected_pressure = (
        SEA_LEVEL_PRESSURE_PA
        * (expected_temperature / SEA_LEVEL_TEMPERATURE_K) ** exponent
    )

    # Density: rho = P / (R * T)
    expected_density = expected_pressure / (
        SPECIFIC_GAS_CONSTANT_J_PER_KG_K * expected_temperature
    )

    # Speed of sound: a = sqrt(gamma * R * T)
    expected_speed_of_sound = math.sqrt(
        SPECIFIC_HEAT_RATIO * SPECIFIC_GAS_CONSTANT_J_PER_KG_K * expected_temperature
    )

    result = isa_troposphere(h)

    assert result["geopotential_altitude_m"] == pytest.approx(h)
    assert result["temperature_k"] == pytest.approx(expected_temperature, rel=1e-9)
    assert result["pressure_pa"] == pytest.approx(expected_pressure, rel=1e-9)
    assert result["density_kg_m3"] == pytest.approx(expected_density, rel=1e-9)
    assert result["speed_of_sound_m_s"] == pytest.approx(
        expected_speed_of_sound, rel=1e-9
    )


def test_temperature_decreases_with_altitude() -> None:
    """Temperature must decrease as geopotential altitude increases."""
    previous = None
    for h in [0, 1000, 2000, 5000, 8000, 11000]:
        result = isa_troposphere(float(h))
        if previous is not None:
            assert result["temperature_k"] < previous
        previous = result["temperature_k"]


def test_pressure_decreases_with_altitude() -> None:
    """Pressure must decrease as geopotential altitude increases."""
    previous = None
    for h in [0, 1000, 2000, 5000, 8000, 11000]:
        result = isa_troposphere(float(h))
        if previous is not None:
            assert result["pressure_pa"] < previous
        previous = result["pressure_pa"]


def test_density_decreases_with_altitude() -> None:
    """Density must decrease as geopotential altitude increases."""
    previous = None
    for h in [0, 1000, 2000, 5000, 8000, 11000]:
        result = isa_troposphere(float(h))
        if previous is not None:
            assert result["density_kg_m3"] < previous
        previous = result["density_kg_m3"]


def test_speed_of_sound_decreases_with_altitude() -> None:
    """Speed of sound must decrease as geopotential altitude increases."""
    previous = None
    for h in [0, 1000, 2000, 5000, 8000, 11000]:
        result = isa_troposphere(float(h))
        if previous is not None:
            assert result["speed_of_sound_m_s"] < previous
        previous = result["speed_of_sound_m_s"]


def test_negative_altitude() -> None:
    """Negative geopotential altitude must raise ValueError."""
    with pytest.raises(ValueError):
        isa_troposphere(-1.0)


def test_altitude_above_max() -> None:
    """Altitude above 11000 m must raise ValueError."""
    with pytest.raises(ValueError):
        isa_troposphere(11001.0)


def test_nan_altitude() -> None:
    """NaN altitude must raise ValueError."""
    with pytest.raises(ValueError):
        isa_troposphere(float("nan"))


def test_positive_infinity_altitude() -> None:
    """Positive infinity altitude must raise ValueError."""
    with pytest.raises(ValueError):
        isa_troposphere(float("inf"))


def test_negative_infinity_altitude() -> None:
    """Negative infinity altitude must raise ValueError."""
    with pytest.raises(ValueError):
        isa_troposphere(float("-inf"))


def test_boolean_altitude() -> None:
    """Boolean altitude must raise TypeError."""
    with pytest.raises(TypeError):
        isa_troposphere(True)


def test_string_altitude() -> None:
    """String altitude must raise TypeError."""
    with pytest.raises(TypeError):
        isa_troposphere("1000")


def test_none_altitude() -> None:
    """None altitude must raise TypeError."""
    with pytest.raises(TypeError):
        isa_troposphere(None)
