# AeroMCP Architecture

## Overall System Architecture

AeroMCP follows a clean separation between domain engineering computation and
the Model Context Protocol (MCP) communication layer. The system is organized
as a Python package using the src-layout:

```
src/aeromcp/
    __init__.py        # Package initialization, version
    server.py          # MCP server interface with 10 registered tools
    core/
        __init__.py    # Package marker
        validation.py  # Shared input validation utilities
    aerodynamics/
        __init__.py    # Package marker, public function exports
        calculations.py # Dynamic pressure, lift, drag, Reynolds number
    atmosphere/
        __init__.py    # Package marker, public function exports
        isa.py         # ISA troposphere model (0-11000 m)
    astrodynamics/
        __init__.py    # Package marker, public function exports
        orbital.py     # Orbital mechanics calculations
    compressible_flow/
        __init__.py    # Package marker (placeholder, not implemented)
    propulsion/
        __init__.py    # Package marker (placeholder, not implemented)
```

## Separation Between Engineering Calculations and MCP Communication

AeroMCP is designed so that engineering calculations are **independent of MCP**:

- **Engineering layer** (`src/aeromcp/core/`, `aerodynamics/`, `atmosphere/`,
  `astrodynamics/`): Pure Python functions that accept numeric inputs and
  return computed results. These functions have no dependency on the MCP SDK
  and can be imported and used directly in any Python program.

- **MCP layer** (`src/aeromcp/server.py`): A thin interface that wraps
  selected engineering functions as MCP tools. It handles protocol
  communication, parameter validation at the tool boundary, and result
  serialization. It imports from the engineering layer but the engineering
  layer never imports from the MCP layer.

This separation ensures that aerospace engineers can use the calculation
library without installing or depending on MCP, while AI clients can access
the same calculations through standardized MCP tool calls.

## Responsibilities of Each Module

| Module | Responsibility | Status |
|--------|---------------|--------|
| `core` | Physical constants, unit conversions, input validation helpers shared across all disciplines. | Implemented |
| `aerodynamics` | Dynamic pressure, lift force, drag force, lift coefficient, Reynolds number calculations. | Implemented |
| `atmosphere` | ISA tropospheric model (0–11000 m geopotential altitude): temperature, pressure, density, speed of sound. | Implemented |
| `astrodynamics` | Circular orbital velocity, orbital period, escape velocity, Hohmann transfer calculations. | Implemented |
| `compressible_flow` | Package placeholder only. Compressible aerodynamics not yet implemented. | Not implemented |
| `propulsion` | Package placeholder only. Propulsion analysis not yet implemented. | Not implemented |
| `server.py` | MCP server definition, ten registered tool wrappers, STDIO transport. | Implemented |

## MCP Communication Flow

AI clients compatible with the Model Context Protocol connect to the AeroMCP
MCP server and invoke registered tools:

1. **Tool discovery:** AI client lists available AeroMCP tools via MCP.
2. **Tool invocation:** Client sends a tool call with engineering parameters
   (e.g., density, velocity, altitude, gravitational parameter, orbit radius).
3. **Server handling:** `server.py` receives the call, delegates to the
   appropriate engineering module function.
4. **Computation:** The engineering module validates inputs and returns a
   numeric result.
5. **Response:** `server.py` serializes the result back to the AI client
   through MCP as a structured dictionary with `result`, `units`, `model`,
   and (where applicable) `valid_altitude_range_m` or `assumptions` fields.

Transport: Local STDIO only. No HTTP/SSE transport is implemented.

## Testing Architecture

| Test File | Purpose | Test Count |
|-----------|---------|------------|
| `tests/test_package.py` | Package import and version verification | 2 |
| `tests/test_aerodynamics.py` | Aerodynamics calculation reference cases, edge cases, input validation | 84 |
| `tests/test_astrodynamics.py` | Orbital mechanics reference cases, edge cases, input validation | 62 |
| `tests/test_atmosphere.py` | ISA troposphere sea level, upper boundary, intermediate altitude, physical trends, invalid inputs | 15 |
| `tests/test_server.py` | MCP tool integration via in-memory Client, tool discovery, error handling | 27 |

Total: 190 tests.

Testing uses pytest. Code quality is enforced with ruff (lint and format).

## Proposed Development Sequence

1. **Project scaffolding** — package structure, packaging, CI, tests (complete).
2. **Core module** — validation, shared utilities (complete).
3. **Aerodynamics module** — dynamic pressure, lift, drag, lift coefficient, Reynolds number (complete).
4. **Atmosphere module** — ISA troposphere model (complete).
5. **Astrodynamics module** — circular orbital velocity, orbital period, escape velocity, Hohmann transfer (complete).
6. **MCP server** — ten registered tools exposing calculations (complete).
7. **Compressible flow module** — isentropic flow, shocks (planned).
8. **Propulsion module** — thrust, engine performance (planned).
9. **Packaging and release** — PyPI publication (planned).

## Limitations

- ISA implementation covers only the tropospheric layer (0–11000 m geopotential
  altitude). Stratosphere and higher layers are not implemented.
- Orbital calculations use ideal two-body models. Atmospheric drag and
  perturbations are not modelled.
- Hohmann transfers use impulsive burns and assume circular, coplanar orbits.
- MCP uses local STDIO transport only. No remote HTTP deployment is implemented.
- AeroMCP is an engineering computation toolkit, not certified aircraft or
  spacecraft design software.
