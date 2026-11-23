"""Atmosphere engineering computations for AeroMCP.

This subpackage contains atmospheric model calculations, including the
International Standard Atmosphere (ISA), density altitude, and properties
of air as a function of altitude.

The following public function is available:

* :func:`isa_troposphere` — compute ISA tropospheric properties from
  geopotential altitude (0 to 11000 m).

This subpackage implements the tropospheric layer only. It is not a
complete multilayer ISA implementation.
"""

from aeromcp.atmosphere.isa import isa_troposphere

__all__ = [
    "isa_troposphere",
]
