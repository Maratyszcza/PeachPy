# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

import six

from peachpy.abi import Endianness


class Encoder:
    def __init__(self, endianness, bitness=None):
        assert endianness in {Endianness.Little, Endianness.Big}
        if endianness == Endianness.Little:
            self.int16 = Encoder.int16le
            self.uint16 = Encoder.uint16le
            self.int32 = Encoder.int32le
            self.uint32 = Encoder.uint32le
            self.int64 = Encoder.int64le
            self.uint64 = Encoder.uint64le
        else:
            self.int16 = Encoder.int16be
            self.uint16 = Encoder.uint16be
            self.int32 = Encoder.int32be
            self.uint32 = Encoder.uint32be
            self.int64 = Encoder.int64be
            self.uint64 = Encoder.uint64be
        self.bitness = bitness
        if bitness is not None:
            assert bitness in {32, 64}, "Only 32-bit and 64-bit encoders are supported"
            if bitness == 32:
                self.signed_offset = self.int32
                self.unsigned_offset = self.uint32
            else:
                self.signed_offset = self.int64
                self.unsigned_offset = self.uint64

    @staticmethod
    def int8(n):
        """Converts signed 8-bit integer to bytearray representation"""
        assert -128 <= n <= 127, "%u can not be represented as an 8-bit signed integer" % n
        return bytearray([n & 0xFF])

    @staticmethod
    def uint8(n):
        """Converts unsigned 8-bit integer to bytearray representation"""
        assert 0 <= n <= 255, "%u can not be represented as an 8-bit unsigned integer" % n
        return bytearray([n])

    @staticmethod
    def int16le(n):
        """Converts signed 16-bit integer to little-endian bytearray representation"""
        assert -32768 <= n <= 32767, "%u can not be represented as a 16-bit signed integer" % n
        return bytearray([n & 0xFF, (n >> 8) & 0xFF])

    @staticmethod
    def int16be(n):
        """Converts signed 16-bit integer to big-endian bytearray representation"""
        assert -32768 <= n <= 32767, "%u can not be represented as a 16-bit signed integer" % n
        return bytearray([n >> 8, (n & 0xFF) & 0xFF])

    @staticmethod
    def uint16le(n):
        """Converts unsigned 16-bit integer to little-endian bytearray representation"""
        assert 0 <= n <= 65535, "%u can not be represented as a 16-bit unsigned integer" % n
        return bytearray([n & 0xFF, n >> 8])

    @staticmethod
    def uint16be(n):
        """Converts unsigned 16-bit integer to big-endian bytearray representation"""
        assert 0 <= n <= 65535, "%u can not be represented as a 16-bit unsigned integer" % n
        return bytearray([n >> 8, n & 0xFF])

    @staticmethod
    def int32le(n):
        """Converts signed 32-bit integer to little-endian bytearray representation"""
        assert -2147483648 <= n <= 2147483647, "%u can not be represented as a 32-bit signed integer" % n
        return bytearray([n & 0xFF, (n >> 8) & 0xFF, (n >> 16) & 0xFF, (n >> 24) & 0xFF])

    @staticmethod
    def int32be(n):
        """Converts signed 32-bit integer to big-endian bytearray representation"""
        assert -2147483648 <= n <= 2147483647, "%u can not be represented as a 32-bit signed integer" % n
        return bytearray([(n >> 24) & 0xFF, (n >> 16) & 0xFF, (n >> 8) & 0xFF, n & 0xFF])

    @staticmethod
    def uint32le(n):
        """Converts unsigned 32-bit integer to little-endian bytearray representation"""
        assert 0 <= n <= 4294967295, "%u can not be represented as a 32-bit unsigned integer" % n
        return bytearray([n & 0xFF, (n >> 8) & 0xFF, (n >> 16) & 0xFF, n >> 24])

    @staticmethod
    def uint32be(n):
        """Converts unsigned 32-bit integer to big-endian bytearray representation"""
        assert 0 <= n <= 4294967295, "%u can not be represented as a 32-bit unsigned integer" % n
        return bytearray([n >> 24, (n >> 16) & 0xFF, (n >> 8) & 0xFF, n & 0xFF])

    @staticmethod
    def int64le(n):
        """Converts signed 64-bit integer to little-endian bytearray representation"""
        assert -9223372036854775808 <= n <= 9223372036854775807, \
            "%u can not be represented as a 64-bit signed integer" % n
        return bytearray([n & 0xFF, (n >> 8) & 0xFF, (n >> 16) & 0xFF, (n >> 24) & 0xFF,
                          (n >> 32) & 0xFF, (n >> 40) & 0xFF, (n >> 48) & 0xFF, (n >> 56) & 0xFF])

    @staticmethod
    def int64be(n):
        """Converts signed 64-bit integer to big-endian bytearray representation"""
        assert -9223372036854775808 <= n <= 9223372036854775807, \
            "%u can not be represented as a 64-bit signed integer" % n
        return bytearray([(n >> 56) & 0xFF, (n >> 48) & 0xFF, (n >> 40) & 0xFF, (n >> 32) & 0xFF,
                         (n >> 24) & 0xFF, (n >> 16) & 0xFF, (n >> 8) & 0xFF, n & 0xFF])

    @staticmethod
    def uint64le(n):
        """Converts unsigned 64-bit integer to little-endian bytearray representation"""
        assert 0 <= n <= 18446744073709551615, "%u can not be represented as a 64-bit unsigned integer" % n
        return bytearray([n & 0xFF, (n >> 8) & 0xFF, (n >> 16) & 0xFF, (n >> 24) & 0xFF,
                          (n >> 32) & 0xFF, (n >> 40) & 0xFF, (n >> 48) & 0xFF, (n >> 56) & 0xFF])

    @staticmethod
    def uint64be(n):
        """Converts unsigned 64-bit integer to big-endian bytearray representation"""
        assert 0 <= n <= 18446744073709551615, "%u can not be represented as a 64-bit unsigned integer" % n
        return bytearray([(n >> 56) & 0xFF, (n >> 48) & 0xFF, (n >> 40) & 0xFF, (n >> 32) & 0xFF,
                         (n >> 24) & 0xFF, (n >> 16) & 0xFF, (n >> 8) & 0xFF, n & 0xFF])

    def int16(self, n):
        """Converts signed 16-bit integer to bytearray representation according to encoder endianness"""
        pass

    def uint16(self, n):
        """Converts unsigned 16-bit integer to bytearray representation according to encoder endianness"""
        pass

    def int32(self, n):
        """Converts signed 32-bit integer to bytearray representation according to encoder endianness"""
        pass

    def uint32(self, n):
        """Converts unsigned 32-bit integer to bytearray representation according to encoder endianness"""
        pass

    def int64(self, n):
        """Converts signed 64-bit integer to bytearray representation according to encoder endianness"""
        pass

    def uint64(self, n):
        """Converts unsigned 64-bit integer to bytearray representation according to encoder endianness"""
        pass

    @staticmethod
    def fixed_string(string, size):
        """Converts string to fixed-length bytearray representation"""
        assert isinstance(size, six.integer_types) and size > 0, "size %u is not a positive integer" % size
        if string is None:
            return bytearray(size)
        import codecs
        byte_string = codecs.encode(string, "utf8")
        if len(byte_string) > size:
            raise ValueError("The length of %s exceeds the target %d" % (string, size))
        elif len(byte_string) == size:
            return byte_string
        else:
            return byte_string + bytearray(size - len(byte_string))

    def signed_offset(self, n):
        """Converts signed integer offset to bytearray representation according to encoder bitness and endianness"""
        raise ValueError("Can not encode signed offset: encoder bitness not specified")

    def unsigned_offset(self, n):
        """Converts unsigned integer offset to bytearray representation according to encoder bitness and endianness"""
        raise ValueError("Can not encode unsigned offset: encoder bitness not specified")
