"""Basic package import and version tests for AeroMCP."""

from aeromcp import __version__


def test_package_imports():
    """The aeromcp package should import without error."""
    import aeromcp  # noqa: F401


def test_version():
    """The package version should be 0.1.0."""
    assert __version__ == "0.1.0"
