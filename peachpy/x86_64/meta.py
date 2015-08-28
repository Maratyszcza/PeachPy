# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from enum import Enum


class RelocationType(Enum):
    """Relocation for RIP-relative disp32 offset"""
    rip_disp32 = 0


class Relocation:
    def __init__(self, offset, rtype, symbol=None):
        self.offset = offset
        self.rtype = rtype
        self.symbol = symbol


class SymbolType(Enum):
    """Literal constant"""
    literal_constant = 0
    """Label"""
    label = 1


class Symbol:
    def __init__(self, offset, stype, name=None, size=None):
        self.offset = offset
        self.stype = stype
        self.name = name
        self.size = size
