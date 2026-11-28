"""Rocket propulsion calculations (SI units)."""

from __future__ import annotations

import math
from typing import Sequence

from aeromcp_engineering.core.constants import G0_M_S2
from aeromcp_engineering.core.validation import (
    validate_finite,
    validate_non_negative,
    validate_positive,
)


def rocket_thrust(
    mass_flow_kg_s: float,
    exhaust_velocity_m_s: float,
    exit_pressure_pa: float = 0.0,
    ambient_pressure_pa: float = 0.0,
    exit_area_m2: float = 0.0,
) -> float:
    """Compute rocket thrust F = m_dot * Ve + (pe - pa) * Ae in newtons (N)."""
    m_dot = validate_positive(mass_flow_kg_s, "mass_flow_kg_s")
    ve = validate_positive(exhaust_velocity_m_s, "exhaust_velocity_m_s")
    pe = validate_non_negative(exit_pressure_pa, "exit_pressure_pa")
    pa = validate_non_negative(ambient_pressure_pa, "ambient_pressure_pa")
    ae = validate_non_negative(exit_area_m2, "exit_area_m2")
    return m_dot * ve + (pe - pa) * ae


def specific_impulse(thrust_n: float, mass_flow_kg_s: float) -> float:
    """Compute specific impulse Isp = F / (m_dot * g0) in seconds (s)."""
    f = validate_positive(thrust_n, "thrust_n")
    m_dot = validate_positive(mass_flow_kg_s, "mass_flow_kg_s")
    return f / (m_dot * G0_M_S2)


def effective_exhaust_velocity(isp_s: float) -> float:
    """Compute effective exhaust velocity c = Isp * g0 in m/s."""
    isp = validate_positive(isp_s, "isp_s")
    return isp * G0_M_S2


def tsiolkovsky_delta_v(
    isp_s: float,
    initial_mass_kg: float,
    final_mass_kg: float,
) -> float:
    """Compute ideal rocket delta-V = Isp * g0 * ln(m0 / mf) in m/s."""
    c = effective_exhaust_velocity(isp_s)
    m0 = validate_positive(initial_mass_kg, "initial_mass_kg")
    mf = validate_positive(final_mass_kg, "final_mass_kg")
    if mf > m0:
        raise ValueError(f"final_mass_kg ({mf}) cannot exceed initial_mass_kg ({m0}).")
    return c * math.log(m0 / mf)


def propellant_mass_from_delta_v(
    delta_v_m_s: float,
    isp_s: float,
    final_mass_kg: float,
) -> dict[str, float]:
    """Compute required propellant mass and initial mass for a target delta-V."""
    dv = validate_non_negative(delta_v_m_s, "delta_v_m_s")
    c = effective_exhaust_velocity(isp_s)
    mf = validate_positive(final_mass_kg, "final_mass_kg")
    mass_ratio = math.exp(dv / c)
    m0 = mf * mass_ratio
    mp = m0 - mf
    return {
        "initial_mass_kg": m0,
        "final_mass_kg": mf,
        "propellant_mass_kg": mp,
        "mass_ratio": mass_ratio,
    }


def multistage_delta_v(
    stages: Sequence[dict[str, float]],
    payload_mass_kg: float,
) -> dict[str, float]:
    """Compute total ideal delta-V for stacked stages.

    Each stage dict must contain: 'structural_mass_kg', 'propellant_mass_kg', 'isp_s'.
    Stages are ordered from 1st (bottom) to Nth (top).
    """
    m_pay = validate_positive(payload_mass_kg, "payload_mass_kg")
    if not stages:
        raise ValueError("stages must be a non-empty sequence.")

    total_dv = 0.0
    upper_mass = m_pay
    stage_dvs: list[float] = []
    # Compute from top stage down to bottom stage
    for idx in range(len(stages) - 1, -1, -1):
        st = stages[idx]
        ms = validate_positive(
            st["structural_mass_kg"], f"stage[{idx}].structural_mass_kg"
        )
        mp = validate_positive(
            st["propellant_mass_kg"], f"stage[{idx}].propellant_mass_kg"
        )
        isp = validate_positive(st["isp_s"], f"stage[{idx}].isp_s")
        m0 = upper_mass + ms + mp
        mf = upper_mass + ms
        dv = tsiolkovsky_delta_v(isp, m0, mf)
        stage_dvs.append(dv)
        total_dv += dv
        upper_mass = m0

    stage_dvs.reverse()
    return {
        "total_delta_v_m_s": total_dv,
        "gross_liftoff_mass_kg": upper_mass,
        "payload_fraction": m_pay / upper_mass,
        "stage_delta_vs_m_s": stage_dvs,
    }


def thrust_coefficient(
    thrust_n: float,
    chamber_pressure_pa: float,
    throat_area_m2: float,
) -> float:
    """Compute nozzle thrust coefficient Cf = F / (pc * At)."""
    f = validate_finite(thrust_n, "thrust_n")
    pc = validate_positive(chamber_pressure_pa, "chamber_pressure_pa")
    at = validate_positive(throat_area_m2, "throat_area_m2")
    return f / (pc * at)
