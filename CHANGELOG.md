# Changelog

All notable changes to AeroMCP will be documented in this file.

## [0.3.0] - 2026-11-27

### Changed
- Package identity migrated to distribution `aeromcp-engineering` and import namespace `aeromcp_engineering`.
- Modularized MCP server registration into `aeromcp_engineering.tools`, `aeromcp_engineering.resources`, and `aeromcp_engineering.prompts`.

### Added
- **Core**: `constants.py`, `units.py`, `errors.py`, `results.py`, `numerical_methods.py` (bisection, safeguarded Newton, RK4, linear system solver).
- **Aerodynamics**: Mach number, L/D ratio, wing loading, aspect ratio, induced drag, stall speed, finite-wing lift-curve slope, thin-airfoil lift, force decomposition.
- **Atmosphere**: U.S. Standard Atmosphere 1976 (0–84,852 m geopotential), Sutherland viscosity, kinematic viscosity, Mach atmospheric properties, density altitude.
- **Compressible Flow**: Isentropic ratios, area-Mach + subsonic/supersonic inverse solvers, normal shock, oblique shock (weak/strong), Prandtl-Meyer + inverse, Fanno flow, Rayleigh flow.
- **Propulsion**: Rocket thrust, Isp, Tsiolkovsky delta-V, propellant mass, multistage delta-V, choked/CD nozzles, ideal turbojet cycle, actuator-disk propeller, rotor/multirotor hover power.
- **Astrodynamics**: Vis-viva, Kepler solver, anomaly conversions, COE-to-ECI, J2 secular perturbations, C3/hyperbolic excess, periapsis/apoapsis, RK4 two-body propagator.
- **Flight Mechanics**: Coordinated turn, climb, glide, jet Breguet range, propeller endurance, takeoff ground roll, static margin, neutral point.
- **Structures**: Axial bar, Euler-Bernoulli beams, circular shaft torsion, Euler buckling, Von Mises stress, thin-walled pressure vessel.
- **Thermal**: 1D conduction, series thermal resistance, convection, radiation, recovery temperature, Sutton-Graves stagnation heating.
- **GNC**: WGS-84 geodetic <-> ECEF, quaternions & ZYX Euler conversions, discrete PID with anti-windup, scalar Kalman filter.
- **Aircraft Design**: Wing area/span/MAC sizing, T/W, P/W, electric UAV endurance.
- **Mission Analysis**: 1D RK4 vertical rocket ascent, mission delta-V budget.
- **MCP**: 55+ tools, 5 reference resources (`aeromcp://*`), and 7 workflow prompts.
