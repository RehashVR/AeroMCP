# AeroMCP

**Bringing Aerospace Engineering Computation to AI Agents.**

## Project Description

AeroMCP is an independent aerospace engineering computation library that exposes
validated engineering calculations through the Model Context Protocol (MCP). The
core engineering calculations are designed to work independently of any AI
application. MCP serves as an interface layer that makes these calculations
accessible as tools to compatible AI clients.

## Project Purpose

AeroMCP provides open, modular, validated aerospace engineering computation
functions that can be used directly in Python, independent of AI tooling. An MCP
server exposes these calculations as tools, enabling AI agents to invoke them
through the standardized Model Context Protocol.

## Feature Overview

### Implemented Features

| Feature | Description |
|---------|-------------|
| Dynamic pressure | Compute q = 0.5 × ρ × V² from air density and flow velocity |
| Lift force | Compute L = q × S × CL from density, velocity, area, and lift coefficient |
| Drag force | Compute D = q × S × CD from density, velocity, area, and drag coefficient |
| Lift coefficient | Compute CL = L / (q × S) from lift force, density, velocity, and area |
| Reynolds number | Compute Re = ρ × V × L / μ from flow and fluid properties |
| ISA troposphere | Compute temperature, pressure, density, speed of sound for geopotential altitudes 0–11000 m (1976 U.S. Standard Atmosphere) |
| MCP server | Six registered tools exposing the above calculations via STDIO transport |

### Future Plans (Not Implemented)

- Compressible flow calculations (isentropic flow, shocks, expansion fans)
- Propulsion analysis (thrust, specific impulse, engine cycles)
- Astrodynamics (orbital mechanics, propagation)
- Multilayer ISA (stratosphere and above)
- HTTP/SSE transport for MCP server

## MCP Tools

The following six tools are registered on the AeroMCP MCP server:

| Tool | Description | Output Unit |
|------|-------------|-------------|
| `calculate_dynamic_pressure` | Dynamic pressure from density and velocity | Pa |
| `calculate_lift_force` | Lift force from density, velocity, area, lift coefficient | N |
| `calculate_drag_force` | Drag force from density, velocity, area, drag coefficient | N |
| `calculate_lift_coefficient` | Dimensionless lift coefficient from lift force, density, velocity, area | dimensionless |
| `calculate_reynolds_number` | Dimensionless Reynolds number from flow properties | dimensionless |
| `calculate_isa_troposphere` | ISA tropospheric properties from geopotential altitude | K, Pa, kg/m³, m/s |

## Architecture

AeroMCP follows a clean separation between engineering computation and MCP
communication:

- **Engineering layer** (`src/aeromcp/core/`, `aerodynamics/`, `atmosphere/`):
  Pure Python functions with no MCP dependency. Independently usable and
  testable.
- **MCP layer** (`src/aeromcp/server.py`): A thin interface that wraps
  engineering functions as MCP tools.

```mermaid
graph TD
    subgraph Engineering_Layer ["Engineering Layer (MCP-independent)"]
        Core["core/ — validation, constants"]
        Aero["aerodynamics/ — lift, drag, Reynolds number"]
        Atmos["atmosphere/ — ISA troposphere"]
    end
    subgraph MCP_Layer ["MCP Communication Layer"]
        Server["server.py — MCPServer with 6 tools"]
    end
    subgraph AI_Client ["AI Client (OpenCode, etc.)"]
        Client["MCP Client via STDIO"]
    end

    Core --> Aero
    Core --> Atmos
    Aero --> Server
    Atmos --> Server
    Server --> Client
```

## Installation Instructions for Windows

### Prerequisites

- Python 3.11 or later (Python 3.12 recommended)

### Virtual Environment Setup

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1
```

### Editable Development Installation

```powershell
# Install the package in editable mode with development dependencies
python -m pip install -e ".[dev]"
```

### OpenCode MCP Integration

Add the following to your `opencode.jsonc` configuration:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "aeromcp": {
        "type": "local",
        "command": [
          "C:\\AeroMCP\\.venv\\Scripts\\python.exe",
          "-m",
          "aeromcp.server"
        ],
        "cwd": "C:\\AeroMCP",
        "codemode": false
      }
    }
  }
}
```

Replace `C:\\AeroMCP` with the actual path to your AeroMCP installation.

## Example Tool Calls

### Dynamic Pressure

```python
from aeromcp.aerodynamics import dynamic_pressure

q = dynamic_pressure(density_kg_m3=1.225, velocity_m_s=50.0)
# Result: 1531.25 Pa
```

### ISA Troposphere

```python
from aeromcp.atmosphere import isa_troposphere

props = isa_troposphere(geopotential_altitude_m=0.0)
# Result: temperature=288.15 K, pressure=101325 Pa,
#         density=1.225 kg/m³, speed_of_sound=340.294 m/s
```

### Via MCP Tool

```json
{
  "tool": "calculate_isa_troposphere",
  "arguments": {
    "geopotential_altitude_m": 5000
  }
}
```

## Engineering Equations

| Calculation | Equation | SI Units |
|-------------|----------|----------|
| Dynamic pressure | q = 0.5 × ρ × V² | Pa |
| Lift force | L = q × S × CL | N |
| Drag force | D = q × S × CD | N |
| Lift coefficient | CL = L / (q × S) | dimensionless |
| Reynolds number | Re = ρ × V × L / μ | dimensionless |
| ISA temperature | T = T₀ − L × H | K |
| ISA pressure | P = P₀ × (T/T₀)^(g₀/(R×L)) | Pa |
| ISA density | ρ = P / (R × T) | kg/m³ |
| ISA speed of sound | a = √(γ × R × T) | m/s |

## ISA Model Scope and Assumptions

- **Model:** 1976 U.S. Standard Atmosphere, tropospheric layer only
- **Valid altitude range:** 0 to 11000 metres (geopotential altitude)
- **Input:** Geopotential altitude (not geometric altitude)
- **Assumptions:** Dry air, hydrostatic equilibrium, ideal gas behaviour,
  constant gravitational acceleration, constant specific gas constant,
  constant ratio of specific heats

## Testing

```powershell
# Run the full test suite
python -m pytest

# Run with verbose output
python -m pytest -v
```

### Test Coverage

| Test File | Tests |
|-----------|-------|
| tests/test_aerodynamics.py | 84 |
| tests/test_atmosphere.py | 15 |
| tests/test_package.py | 2 |
| tests/test_server.py | 17 |
| **Total** | **118** |

## Contribution Instructions

See [CONTRIBUTING.md](CONTRIBUTING.md) for local development setup, testing,
linting, branch conventions, and pull request guidelines.

See [SECURITY.md](SECURITY.md) for responsible vulnerability disclosure and
credential handling policies.

## Project Roadmap

The following items are planned for future releases:

1. **Atmosphere module** — ISA troposphere (complete)
2. **Aerodynamics module** — lift, drag, Reynolds number (complete)
3. **MCP server** — six registered tools (complete)
4. **Compressible flow module** — isentropic flow, shocks (planned)
5. **Propulsion module** — thrust, engine performance (planned)
6. **Astrodynamics module** — orbital mechanics (planned)
7. **Packaging and release** — PyPI publication (planned)

## Technology Stack

- **Language:** Python 3.11+
- **Packaging:** setuptools with src-layout
- **MCP SDK:** mcp Python SDK v2 (`mcp>=2.3,<3`)
- **Testing:** pytest
- **Linting & Formatting:** ruff

## Limitations

- ISA implementation currently covers only 0–11000 m geopotential altitude
  (tropospheric layer only). Stratosphere and higher layers are not implemented.
- MCP currently uses local STDIO transport only. No remote HTTP deployment
  is implemented.
- AeroMCP is an engineering computation toolkit. It is **not** certified
  aircraft or spacecraft design software and should not be used for
  safety-critical aerospace applications without independent validation.

## Licence

AeroMCP is licensed under the MIT License. See [LICENSE](LICENSE) for details.
