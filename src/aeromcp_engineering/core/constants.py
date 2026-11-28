"""Standard SI physical and aerospace engineering constants.

All constants are in strict SI units. Sources include CODATA 2018/2022,
U.S. Standard Atmosphere 1976, WGS-84, and IAU/Vallado astrodynamics
conventions.
"""

from __future__ import annotations

# Standard gravity (exact by definition, BIPM / U.S. Standard Atmosphere 1976)
G0_M_S2: float = 9.80665

# Ideal gas constants for dry air (U.S. Standard Atmosphere 1976)
R_UNIVERSAL_J_MOL_K: float = 8.314462618
MOLAR_MASS_AIR_KG_MOL: float = 0.0289644
R_AIR_J_KG_K: float = 287.05287
GAMMA_AIR: float = 1.4

# Sea-level standard atmospheric conditions (ISA)
P0_PA: float = 101325.0
T0_K: float = 288.15
RHO0_KG_M3: float = 1.225

# Sutherland's law constants for air
SUTHERLAND_MU0_PA_S: float = 1.716e-5
SUTHERLAND_T0_K: float = 273.15
SUTHERLAND_S_K: float = 110.4

# Radiation
STEFAN_BOLTZMANN_W_M2_K4: float = 5.670374419e-8

# Earth gravitational and geometric constants (WGS-84 / EGM96 / Vallado)
MU_EARTH_M3_S2: float = 3.986004418e14
R_EARTH_MEAN_M: float = 6_371_000.0
R_EARTH_EQUATORIAL_M: float = 6_378_137.0
J2_EARTH: float = 1.08262668e-3
OMEGA_EARTH_RAD_S: float = 7.2921150e-5

# WGS-84 ellipsoid parameters
WGS84_A_M: float = 6_378_137.0
WGS84_F: float = 1.0 / 298.257223563
WGS84_E2: float = WGS84_F * (2.0 - WGS84_F)
