# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


def is_int(n):
    return isinstance(n, (int, long))


def is_int64(n):
    return isinstance(n, (int, long)) and -9223372036854775808L <= n <= 18446744073709551615L


def is_int32(n):
    return isinstance(n, (int, long)) and -2147483648 <= n <= 4294967295


def is_sint32(n):
    return isinstance(n, (int, long)) and -2147483648 <= n <= 2147483647


def is_int16(n):
    return isinstance(n, (int, long)) and -32768 <= n <= 65535


def is_sint16(n):
    return isinstance(n, (int, long)) and -32768 <= n <= 32767


def is_uint16(n):
    return isinstance(n, (int, long)) and 0 <= n <= 65535


def is_int8(n):
    return isinstance(n, (int, long)) and -128 <= n <= 255


def is_uint8(n):
    return isinstance(n, (int, long)) and 0 <= n <= 255


def is_sint8(n):
    return isinstance(n, (int, long)) and -128 <= n <= 127


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
