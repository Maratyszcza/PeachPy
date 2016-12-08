# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class Argument(object):
    """
    Function argument.

    An argument must have a C type and a name.

    :ivar c_type: the type of the argument in C
    :type c_type: :class:`peachpy.c.types.Type`

    :ivar name: the name of the argument
    :type name: str
    """
    def __init__(self, c_type, name=None):
        """
        :param peachpy.c.types.Type c_type: the type of the argument in C.
            When Go function is generated, the type is automatically converted to similar Go type.
            Note that the ``short``, ``int``, ``long``, and ``long long`` types do not have an equivalents in Go.
            In particular, C's ``int`` type is not an equivalent of Go's ``int`` type. To get Go's ``int`` and ``uint``
            types use ``ptrdiff_t`` and ``size_t`` correspondingly.

        :param str name: the name of the argument. If the name is not provided explicitly, PeachPy tries to parse it
            from the caller code. The name must follow the C rules for identifiers:

            - It can contain only Latin letters, digits, and underscore symbol
            - It can not start with a digit
            - It can not start with double underscore (these names are reserved for PeachPy)
            - Name must be unique among the function arguments
        """

        from peachpy.c.types import Type
        if not isinstance(c_type, Type):
            raise TypeError("%s is not a C type" % str(c_type))
        self.c_type = c_type

        if name is None:
            import inspect
            import re

            _, _, _, _, caller_lines, _ = inspect.stack()[1]
            if caller_lines is None:
                raise ValueError("Argument name is not specified and the caller context is not available")
            source_line = caller_lines[0].strip()
            match = re.match("(?:\\w+\\.)*(\\w+)\\s*=\\s*(?:\\w+\\.)*Argument\\(.+\\)", source_line)
            if match:
                name = match.group(1)
                while name.startswith("_"):
                    name = name[1:]
                if name.endswith("argument") or name.endswith("Argument"):
                    name = name[:-len("argument")]
                if name.endswith("arg") or name.endswith("Arg"):
                    name = name[:-len("arg")]
                while name.endswith("_"):
                    name = name[:-1]
            if not name:
                raise ValueError("Argument name is not specified and can not be parsed from the code")

        from peachpy.name import Name
        Name.check_name(name)
        self.name = name

    def __str__(self):
        return str(self.c_type) + " " + self.name

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return isinstance(other, Argument) and self.c_type == other.c_type and self.name == other.name

    def __ne__(self, other):
        return not isinstance(other, Argument) or self.c_type != other.c_type or self.name != other.name

    @property
    def is_floating_point(self):
        return self.c_type.is_floating_point

    @property
    def is_codeunit(self):
        return self.c_type.is_codeunit

    @property
    def is_integer(self):
        return self.c_type.is_integer

    @property
    def is_unsigned_integer(self):
        return self.c_type.is_unsigned_integer

    @property
    def is_signed_integer(self):
        return self.c_type.is_signed_integer

    @property
    def is_size_integer(self):
        return self.c_type.is_size_integer

    @property
    def is_pointer_integer(self):
        return self.c_type.is_pointer_integer

    @property
    def is_pointer(self):
        return self.c_type.is_pointer

    @property
    def is_vector(self):
        return self.c_type.is_vector

    @property
    def is_mask(self):
        return self.c_type.is_mask

    @property
    def size(self):
        return self.c_type.size


