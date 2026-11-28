# AeroMCP v0.3.0 Implementation Status

| Domain | Classification | Notes |
| --- | --- | --- |
| Core (`core`) | IMPLEMENTED | Validation, SI constants, unit conversions, RK4, root solvers, structured results |
| Aerodynamics (`aerodynamics`) | IMPLEMENTED | 5 original + 9 new analytical/finite-wing functions, tests, MCP tools |
| Atmosphere (`atmosphere`) | IMPLEMENTED | ISA troposphere + 1976 layered model (0–84,852 m geopotential), Sutherland viscosity |
| Compressible Flow (`compressible_flow`) | IMPLEMENTED | Isentropic, area-Mach + inverse, normal/oblique shock, Prandtl-Meyer, Fanno, Rayleigh |
| Propulsion (`propulsion`) | IMPLEMENTED | Rockets, choked/CD nozzles, ideal turbojet, actuator-disk propeller, rotor/multirotor hover |
| Astrodynamics (`astrodynamics`) | IMPLEMENTED | 4 original + Kepler solver, COE->ECI, J2 secular, C3, RK4 two-body propagator |
| Flight Mechanics (`flight_mechanics`) | IMPLEMENTED | Turn, climb, glide, Breguet range/endurance, ground roll, static margin, neutral point |
| Structures (`structures`) | IMPLEMENTED | Axial, beams, torsion, Euler buckling, Von Mises, thin-walled pressure vessel |
| Thermal (`thermal`) | IMPLEMENTED | Conduction, convection, radiation, recovery temp, Sutton-Graves heating |
| GNC (`gnc`) | IMPLEMENTED | WGS-84 geodetic/ECEF, quaternions/ZYX Euler, discrete PID, scalar Kalman |
| Aircraft Design (`aircraft_design`) | IMPLEMENTED | Preliminary wing sizing, T/W, P/W, electric UAV endurance |
| Mission Analysis (`mission_analysis`) | IMPLEMENTED | 1D RK4 vertical rocket ascent, mission delta-V budget |
| Composite Laminates (CLT) | PLANNED | Deferred; not exposed |
| External CFD/FEA Adapters | UNSUPPORTED | No external solver bindings implemented |
