# Contributing to AeroMCP

Thank you for considering a contribution to AeroMCP. This project is in its
early scaffolding stage. Contributions are welcome as the engineering modules
and MCP server are implemented.

## Local Development Setup

1. **Clone the repository** and navigate into `C:\AeroMCP` (or your local copy).
2. **Create a virtual environment** using Python 3.11 or later:

   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:

   - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
   - Windows (cmd): `.venv\Scripts\activate.bat`
   - macOS/Linux: `source .venv/bin/activate`

4. **Install the package with development dependencies**:

   ```bash
   python -m pip install -e ".[dev]"
   ```

## Testing

Run the test suite with pytest:

```bash
python -m pytest
```

For verbose output:

```bash
python -m pytest -v
```

Tests live in the `tests/` directory. Add tests for each new engineering
module as it is implemented.

## Linting and Formatting

AeroMCP uses [Ruff](https://docs.astral.sh/ruff/) for both linting and
formatting.

### Linting

```bash
python -m ruff check .
```

### Formatting check

```bash
python -m ruff format --check .
```

### Apply formatting

```bash
python -m ruff format .
```

## Branches and Pull Requests

1. Create a feature branch from `main` using a descriptive name, e.g.:
   `feature/atmosphere-isa-model` or `fix/core-unit-conversions`.
2. Implement your changes, including tests for new functionality.
3. Run the test suite, ruff check, and ruff format check locally before
   pushing.
4. Push your branch and open a pull request against `main`.
5. Ensure all CI checks pass before requesting review.

Pull requests should include:

- A clear description of the change.
- Tests covering new behavior.
- Updates to documentation when behavior or API changes.

## Code Style

- Follow PEP 8 as enforced by Ruff.
- Use double quotes for strings (configured in `pyproject.toml`).
- Target Python 3.12 features and typing.
