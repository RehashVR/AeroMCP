"""Propulsion engineering calculations for AeroMCP."""

from __future__ import annotations

from aeromcp_engineering.propulsion.engines import ideal_turbojet_cycle
from aeromcp_engineering.propulsion.nozzles import (
    choked_mass_flow,
    converging_diverging_nozzle,
    critical_pressure_ratio,
)
from aeromcp_engineering.propulsion.propellers import actuator_disk_propeller
from aeromcp_engineering.propulsion.rockets import (
    effective_exhaust_velocity,
    multistage_delta_v,
    propellant_mass_from_delta_v,
    rocket_thrust,
    specific_impulse,
    thrust_coefficient,
    tsiolkovsky_delta_v,
)
from aeromcp_engineering.propulsion.rotors import (
    multirotor_hover_estimate,
    rotor_hover_power,
)

__all__ = [
    "actuator_disk_propeller",
    "choked_mass_flow",
    "converging_diverging_nozzle",
    "critical_pressure_ratio",
    "effective_exhaust_velocity",
    "ideal_turbojet_cycle",
    "multirotor_hover_estimate",
    "multistage_delta_v",
    "propellant_mass_from_delta_v",
    "rocket_thrust",
    "rotor_hover_power",
    "specific_impulse",
    "thrust_coefficient",
    "tsiolkovsky_delta_v",
]
