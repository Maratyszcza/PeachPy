# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from peachpy.formats.elf.image import Image
from peachpy.formats.elf.section import DataSection, TextSection
from peachpy.formats.elf.symbol import Symbol, SymbolBinding, SymbolType
import peachpy.arm.abi
import peachpy.x86_64.abi

abi = peachpy.x86_64.abi.system_v_x86_64_abi
image = Image(abi, __file__)

text = TextSection(abi)
text.append(b"\x33\xC0" + b"\xC3")
image.bind_section(text, ".text")

data = DataSection(abi)
data.append(b"\x42\x00\x00\x00")
image.bind_section(data, ".data")

# Add symbols
f = Symbol(abi)
f.name_index = image.strtab.add("f")
f.value = 0
f.content_size = 3
f.section_index = text.index
f.binding = SymbolBinding.Global
f.type = SymbolType.Function
image.symtab.add(f)

c = Symbol(abi)
c.name_index = image.strtab.add("c")
c.value = 0
c.content_size = 4
c.section_index = data.index
c.binding = SymbolBinding.Global
c.type = SymbolType.DataObject
image.symtab.add(c)

image.symtab.bind()

open("output.elf", "wb").write(image.as_bytearray)
