"""Basic package import and version tests for AeroMCP."""

from aeromcp_engineering import __version__


def test_package_imports():
    """The aeromcp package should import without error."""
    import aeromcp_engineering  # noqa: F401


def test_version():
    """The package version should be 0.3.0."""
    assert __version__ == "0.3.0"
