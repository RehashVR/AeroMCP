"""Common aerospace engineering unit conversions to and from SI."""

from __future__ import annotations

from aeromcp_engineering.core.validation import validate_finite

_LENGTH_TO_M: dict[str, float] = {
    "m": 1.0,
    "km": 1000.0,
    "ft": 0.3048,
    "in": 0.0254,
    "nmi": 1852.0,
    "mi": 1609.344,
}

_VELOCITY_TO_M_S: dict[str, float] = {
    "m/s": 1.0,
    "km/h": 1.0 / 3.6,
    "kt": 1852.0 / 3600.0,
    "mph": 1609.344 / 3600.0,
    "ft/s": 0.3048,
}

_PRESSURE_TO_PA: dict[str, float] = {
    "pa": 1.0,
    "kpa": 1000.0,
    "mpa": 1.0e6,
    "bar": 1.0e5,
    "atm": 101325.0,
    "psi": 6894.757293168361,
}

_MASS_TO_KG: dict[str, float] = {
    "kg": 1.0,
    "g": 1.0e-3,
    "t": 1000.0,
    "lbm": 0.45359237,
    "slug": 14.593902937206364,
}

_FORCE_TO_N: dict[str, float] = {
    "n": 1.0,
    "kn": 1000.0,
    "lbf": 4.4482216152605,
}

_ANGLE_TO_RAD: dict[str, float] = {
    "rad": 1.0,
    "deg": 3.141592653589793 / 180.0,
}

_POWER_TO_W: dict[str, float] = {
    "w": 1.0,
    "kw": 1000.0,
    "mw": 1.0e6,
    "hp": 745.6998715822702,
}

_UNIT_TABLES: dict[str, dict[str, float]] = {
    "length": _LENGTH_TO_M,
    "velocity": _VELOCITY_TO_M_S,
    "pressure": _PRESSURE_TO_PA,
    "mass": _MASS_TO_KG,
    "force": _FORCE_TO_N,
    "angle": _ANGLE_TO_RAD,
    "power": _POWER_TO_W,
}


def convert_unit(value: float, from_unit: str, to_unit: str, quantity: str) -> float:
    """Convert a scalar value between supported units of a physical quantity."""
    val = validate_finite(value, "value")
    qty = quantity.lower()
    if qty == "temperature":
        return _convert_temperature(val, from_unit.lower(), to_unit.lower())
    if qty not in _UNIT_TABLES:
        raise ValueError(f"Unsupported quantity {quantity!r}.")
    table = _UNIT_TABLES[qty]
    f_u = from_unit.lower()
    t_u = to_unit.lower()
    if f_u not in table:
        raise ValueError(f"Unsupported source unit {from_unit!r} for {quantity}.")
    if t_u not in table:
        raise ValueError(f"Unsupported target unit {to_unit!r} for {quantity}.")
    return val * table[f_u] / table[t_u]


def _convert_temperature(value: float, from_u: str, to_u: str) -> float:
    """Convert temperature between K, C, F, and R."""
    if from_u == "k":
        kelvin = value
    elif from_u == "c":
        kelvin = value + 273.15
    elif from_u == "f":
        kelvin = (value - 32.0) * 5.0 / 9.0 + 273.15
    elif from_u == "r":
        kelvin = value * 5.0 / 9.0
    else:
        raise ValueError(f"Unsupported temperature unit {from_u!r}.")

    if to_u == "k":
        return kelvin
    if to_u == "c":
        return kelvin - 273.15
    if to_u == "f":
        return (kelvin - 273.15) * 9.0 / 5.0 + 32.0
    if to_u == "r":
        return kelvin * 9.0 / 5.0
    raise ValueError(f"Unsupported temperature unit {to_u!r}.")
