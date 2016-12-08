# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


abi = None
target = None
debug_level = 0
package = None
assembly_format = "go"
generate_assembly = None
rtl_dump_file = None
name_mangling = "${Name}"


def get_debug_level():
    from peachpy.common.function import active_function
    if active_function is None:
        return debug_level
    else:
        return active_function.debug_level
