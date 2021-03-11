# SPDX-FileCopyrightText: Copyright (c) 2021 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_board_toolkit`
================================================================================

CircuitPython board identification and information


* Author(s): Dan Halbert for Adafruit Industries

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Board_Toolkit.git"

from typing import Sequence

import sys

import serial.tools.list_ports
from serial.tools.list_ports_common import ListPortInfo


def comports() -> Sequence[ListPortInfo]:
    """Return all the comports recognized as being associated with a CircuitPython board."""

    ports = serial.tools.list_ports.comports()

    if sys.platform == "darwin":
        # pyserial 3.4 and below have a bug on MacOS that returns an identical
        # interface name for a composite USB device with multiple device names.
        # For instance, a CircuitPython board with two CDC interfaces
        # "CircuitPython CDC control" and "CircuitPython CDC2 control",
        # presenting as two /dev/cu.* devices, will only show one of those interface names.
        # See https://github.com/pyserial/pyserial/pull/566.
        # Check for this bug. If so, use a fixed version of list_ports_osx.
        interface_to_device = {}
        for port in ports:
            # Have we already found a port on the same device? If so, that's a bug.
            # Use the new version for MacOS instead.
            if port.device == interface_to_device.get(port.interface, None):
                import _list_ports_osx_fixed # pylint: disable=import-outside-toplevel

                ports = _list_ports_osx_fixed.comports()
                break

    return tuple(
        port
        for port in ports
        if port.interface and port.interface.startswith("CircuitPython CDC")
    )


def repl_comports() -> Sequence[ListPortInfo]:
    """Return all comports presenting a CircuitPython REPL."""
    return tuple(
        port for port in comports() if port.interface.startswith("CircuitPython CDC ")
    )


def data_comports() -> Sequence[ListPortInfo]:
    """Return all comports presenting a CircuitPython serial connection
    used for data transfer, not the REPL.
    """
    return tuple(
        port for port in comports() if port.interface.startswith("CircuitPython CDC2 ")
    )