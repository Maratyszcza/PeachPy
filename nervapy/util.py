# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

import six


def int_size(n):
    assert is_int64(n)
    if is_int8(n):
        return 1
    elif is_int16(n):
        return 2
    elif is_int32(n):
        return 4
    else:
        return 8


def is_int(n):
    return isinstance(n, six.integer_types)


def is_int64(n):
    return isinstance(n, six.integer_types) and -9223372036854775808 <= n <= 18446744073709551615


def is_sint64(n):
    return isinstance(n, six.integer_types) and -9223372036854775808 <= n <= 9223372036854775807


def is_uint64(n):
    return isinstance(n, six.integer_types) and 0 <= n <= 18446744073709551615


def is_int32(n):
    return isinstance(n, six.integer_types) and -2147483648 <= n <= 4294967295


def is_sint32(n):
    return isinstance(n, six.integer_types) and -2147483648 <= n <= 2147483647


def is_uint32(n):
    return isinstance(n, six.integer_types) and 0 <= n <= 4294967295


def is_int16(n):
    return isinstance(n, six.integer_types) and -32768 <= n <= 65535


def is_sint16(n):
    return isinstance(n, six.integer_types) and -32768 <= n <= 32767


def is_uint16(n):
    return isinstance(n, six.integer_types) and 0 <= n <= 65535


def is_int8(n):
    return isinstance(n, six.integer_types) and -128 <= n <= 255


def is_uint8(n):
    return isinstance(n, six.integer_types) and 0 <= n <= 255


def is_sint8(n):
    return isinstance(n, six.integer_types) and -128 <= n <= 127


def roundup(n, q):
    import math
    return int(math.ceil(float(n) / float(q)) * q)


def ilog2(n):
    if n & (n - 1) != 0:
        raise ValueError("%u is not an power of 2" % n)
    if n == 0:
        return 0
    else:
        l = 0
        while n != 1:
            l += 1
            n >>= 1
        return l


def unique(seq):
    seq_values = set()
    unique_seq = []
    for value in seq:
        if value not in seq_values:
            seq_values.add(value)
            unique_seq.append(value)
    return unique_seq


def append_unique(value, sequence=None):
    if sequence is None:
        return [value]
    else:
        if value not in sequence:
            sequence.append(value)
        return sequence


def pairwise(iterable):
    import itertools
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


def diff(sequence):
    import operator
    return map(operator.__sub__, pairwise(sequence))
