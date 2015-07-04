# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
# See license.rst for the full text of the license.


from enum import IntEnum
import six


class SectionFlags:
    # Section contains executable code
    code = 0x00000020
    # Section contains initialized data
    initialized_data = 0x00000040
    # Section contains uninitialized data
    uninitialized_data = 0x00000080
    # Section contains extended relocations
    extended_relocations = 0x01000000
    # Section can be discarded as needed
    discardable = 0x02000000
    # Section can not be cached
    uncached = 0x04000000
    # Section can not be pageable
    unpaged = 0x08000000
    # Section data can be shared between process instances
    shared = 0x10000000
    # Section contains executable data during process execution
    executable = 0x20000000
    # Section contains readable data during process execution
    readable = 0x40000000
    # Section contains writable data during process execution
    writable = 0x80000000

    alignment_mask = 0x00F00000

    _alignment_to_flag_map = {
        1: 0x00100000,
        2: 0x00200000,
        4: 0x00300000,
        8: 0x00400000,
        16: 0x00500000,
        32: 0x00600000,
        64: 0x00700000,
        128: 0x00800000,
        256: 0x00900000,
        512: 0x00A00000,
        1024: 0x00B00000,
        2048: 0x00C00000,
        4096: 0x00D00000,
        8192: 0x00E00000
    }

    _flag_to_alignment_map = {flag: alignment for (alignment, flag) in six.iteritems(_alignment_to_flag_map)}

    @staticmethod
    def alignment_flag(alignment):
        return SectionFlags._alignment_to_flag_map[alignment]


class SectionHeader:
    size = 40

    def __init__(self):
        # Section name
        self.name = None
        # Size of the section in memory
        self.memory_size = 0
        # Address of section data before relocation. Normally equals zero
        self.memory_address = 0
        # Size of section on disk
        self.content_size = 0
        # Offset in the COFF file to the start of section.
        # 4-byte aligned. 0 if section data occupies no space in the file.
        self.content_offset = None
        # Offset to the beginning of relocation entries for the section. 0 if there are no relocations
        self.relocations_offset = None
        # Offset to the beginning of line-number entries for the section. 0 if there are no COFF line numbers.
        self.line_numbers_offset = None
        # Number of relocations for the section. 0 if no relocations.
        self.relocations_count = 0
        # Number of line-number entries for the section
        self.line_numbers_count = 0
        # Flags for the section
        self.flags = 0

    def set_alignment(self, alignment):
        self.flags = (self.flags & ~SectionFlags.alignment_mask) | SectionFlags.alignment_flag(alignment)

    @property
    def alignment(self):
        alignment_flag = self.flags & SectionFlags.alignment_mask
        if alignment_flag == 0:
            return 0
        else:
            return SectionFlags._flag_to_alignment_map[alignment_flag]

    @property
    def as_bytearray(self):
        from peachpy.encoder import Encoder
        from peachpy.util import is_int

        if is_int(self.name):
            header = Encoder.fixed_string("/" + str(self.name), 8)
        else:
            header = Encoder.fixed_string(self.name, 8)
        return header + \
            Encoder.uint32le(self.memory_size) + \
            Encoder.uint32le(self.memory_address) + \
            Encoder.uint32le(self.content_size) + \
            Encoder.uint32le(self.content_offset) + \
            Encoder.uint32le(self.relocations_offset or 0) + \
            Encoder.uint32le(self.line_numbers_offset or 0) + \
            Encoder.uint16le(self.relocations_count) + \
            Encoder.uint16le(self.line_numbers_count) + \
            Encoder.uint32le(self.flags)


class Section(object):
    def __init__(self, alignment=None):
        super(Section, self).__init__()
        self.header = SectionHeader()
        if alignment is not None:
            self.header.set_alignment(alignment)
        self.index = None
        self.content = bytearray()

    def write(self, data):
        self.header.content_size += len(data)
        self.content += data


class TextSection(Section):
    def __init__(self):
        super(TextSection, self).__init__()
        self.header.flags |= SectionFlags.code | SectionFlags.readable | SectionFlags.executable


class ConstSection(Section):
    def __init__(self):
        super(ConstSection, self).__init__()
        self.header.flags |= SectionFlags.initialized_data | SectionFlags.readable


class StringTable:
    def __init__(self):
        self._strings = dict()
        self.size = 4

    def add(self, string):
        import codecs

        if string in self._strings:
            return self._strings[string]
        else:
            string_index = self.size
            self._strings[string] = string_index
            bytestring = codecs.encode(string, "utf-8")
            self.size += len(bytestring) + 1
            return string_index

    @property
    def as_bytearray(self):
        import codecs
        import peachpy.encoder

        bytestring = peachpy.encoder.Encoder.uint32le(self.size)
        for string in sorted(self._strings, key=self._strings.get):
            bytestring += codecs.encode(string, "utf8") + b"\x00"
        return bytestring
