# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
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
    import peachpy.x86_64.function as function
    if function.active_function is None:
        return debug_level
    else:
        return function.active_function.debug_level
