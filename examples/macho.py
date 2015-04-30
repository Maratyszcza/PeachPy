# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from peachpy.formats.macho.image import Image
from peachpy.formats.macho.symbol import Symbol, SymbolType, SymbolVisibility, SymbolDescription
import peachpy.arm.abi
import peachpy.x86_64.abi

abi = peachpy.x86_64.abi.system_v_x86_64_abi
image = Image(abi)

image.text_section.append(b"\x33\xC0" + b"\xC3")
image.const_section.append(b"\x42\x00\x00\x00")

# Add symbols
f = Symbol(abi)
f.description = SymbolDescription.Defined
f.type = SymbolType.SectionRelative
f.visibility = SymbolVisibility.External
f.string_index = image.string_table.add("_f")
f.section_index = image.text_section.index
f.value = 0
image.symbols.append(f)

c = Symbol(abi)
c.description = SymbolDescription.Defined
c.type = SymbolType.SectionRelative
c.visibility = SymbolVisibility.External
c.string_index = image.string_table.add("_c")
c.section_index = image.const_section.index
c.value = 0
image.symbols.append(c)

open("output.mach", "wb").write(image.as_bytearray)
