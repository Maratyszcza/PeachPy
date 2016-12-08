# This file is part of PeachPy package and is licensed under the Simplified BSD license.
# See license.rst for the full text of the license.


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


class Section(object):
    header_size = 40

    _alignment_flag_map = {
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

    _flag_alignment_map = {flag: alignment for (alignment, flag) in six.iteritems(_alignment_flag_map)}

    _alignment_mask = 0x00F00000

    def __init__(self, name, flags, alignment=None):
        from peachpy.util import is_uint32
        if not isinstance(name, str):
            raise TypeError("Section name %s is not a string" % str(name))
        if not is_uint32(flags):
            raise TypeError("Flags %s are not representable as a 32-bit unsigned integer" % str(flags))

        super(Section, self).__init__()
        # Section name
        self.name = name
        # Flags for the section
        self.flags = (flags & ~Section._alignment_mask) | Section._alignment_flag_map[1]
        if alignment is not None:
            self.alignment = alignment

        self.relocations = list()
        self.content = bytearray()

    @property
    def content_size(self):
        return len(self.content)

    @property
    def alignment(self):
        return Section._flag_alignment_map.get(self.flags & Section._alignment_mask, 1)

    @alignment.setter
    def alignment(self, alignment):
        from peachpy.util import is_int
        if not is_int(alignment):
            raise TypeError("Alignment %s is not an integer" % str(alignment))
        if alignment < 0:
            raise ValueError("Alignment %d is not a positive integer" % alignment)
        if alignment & (alignment - 1) != 0:
            raise ValueError("Alignment %d is not a power of 2" % alignment)
        if alignment not in Section._alignment_flag_map:
            raise ValueError("Alignment %d exceeds maximum alignment (8192)" % alignment)
        self.flags = (self.flags & ~Section._alignment_mask) | Section._alignment_flag_map[alignment]

    def encode_header(self, encoder, name_index_map, offset, relocations_offset=None, address=None):
        from peachpy.encoder import Encoder
        assert isinstance(encoder, Encoder)
        assert isinstance(name_index_map, dict)

        if address is None:
            address = 0
        if relocations_offset is None:
            relocations_offset = 0
        line_numbers_offset = 0
        line_numbers_count = 0
        try:
            name_8_bytes = encoder.fixed_string(self.name, 8)
        except ValueError:
            name_index = name_index_map[self.name]
            name_8_bytes = encoder.fixed_string("/" + str(name_index), 8)
        return name_8_bytes + \
            encoder.uint32(self.content_size) + \
            encoder.uint32(address) + \
            encoder.uint32(self.content_size) + \
            encoder.uint32(offset) + \
            encoder.uint32(relocations_offset) + \
            encoder.uint32(line_numbers_offset) + \
            encoder.uint16(len(self.relocations)) + \
            encoder.uint16(line_numbers_count) + \
            encoder.uint32(self.flags)


class TextSection(Section):
    def __init__(self, name=".text", alignment=None):
        super(TextSection, self).__init__(name,
                                          SectionFlags.code | SectionFlags.readable | SectionFlags.executable,
                                          alignment)


class ReadOnlyDataSection(Section):
    def __init__(self, name=".rdata", alignment=None):
        super(ReadOnlyDataSection, self).__init__(name,
                                           SectionFlags.initialized_data | SectionFlags.readable,
                                           alignment)


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

    def encode(self):
        import codecs
        import peachpy.encoder

        bytestring = peachpy.encoder.Encoder.uint32le(self.size)
        for string in sorted(self._strings, key=self._strings.get):
            bytestring += codecs.encode(string, "utf8") + b"\x00"
        return bytestring
