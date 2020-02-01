# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from __future__ import absolute_import


from peachpy import *
from peachpy.x86_64 import *
import sys
import argparse
import six


parser = argparse.ArgumentParser(
    description="PeachPy: Portable Efficient Assembly Code-generation in High-level Python")
parser.add_argument("-g", dest="debug_level", type=int, default=0,
                    help="Debug information level")
parser.add_argument("-S", dest="generate_assembly", action="store_true",
                    help="Generate assembly listing on output")
parser.add_argument("-MMD", dest="generate_dependencies_makefile", action="store_true",
                    help="Generate Makefile describing the dependencies")
parser.add_argument("-MF", dest="dependencies_makefile_path",
                    help="Path to output Makefile with dependencies")
parser.add_argument("-I", dest="include", action="append", default=list(),
                    help="Add directory to module search path")
parser.add_argument("-fdump-rtl", dest="rtl_dump",
                    help="Path to output file for RTL dump")
parser.add_argument("-emit-json-metadata", dest="json_metadata_file",
                    help="Path to output file for JSON metadata")
parser.add_argument("-emit-c-header", dest="c_header_file",
                    help="Path to output file for C/C++ header")
parser.add_argument("-fname-mangling", dest="name_mangling",
                    help="Mangling of function names")


abi_map = {
    "ms": (peachpy.x86_64.abi.microsoft_x64_abi, ["masm", "nasm"], ["ms-coff"]),
    "sysv": (peachpy.x86_64.abi.system_v_x86_64_abi, ["gas", "nasm"], ["elf", "mach-o"]),
    "x32": (peachpy.x86_64.abi.linux_x32_abi, ["gas"], ["elf"]),
    "nacl": (peachpy.x86_64.abi.native_client_x86_64_abi, ["gas"], ["elf"]),
    "gosyso": (peachpy.x86_64.abi.gosyso_amd64_abi, ["gas"], ["elf", "mach-o", "ms-coff"]),
    "goasm": (peachpy.x86_64.abi.goasm_amd64_abi, ["go"], []),
    "gosyso-p32": (peachpy.x86_64.abi.gosyso_amd64p32_abi, ["gas"], ["elf", "mach-o", "ms-coff"]),
    "goasm-p32": (peachpy.x86_64.abi.goasm_amd64p32_abi, ["go"], [])
}
parser.add_argument("-mabi", dest="abi", default="native",
                    choices=("native", "ms", "sysv", "x32", "nacl", "gosyso", "gosyso-p32", "goasm", "goasm-p32"),
                    help="Generate code for specified ABI")

cpu_map = {
    "default": peachpy.x86_64.uarch.default,
    "prescott": peachpy.x86_64.uarch.prescott,
    "conroe": peachpy.x86_64.uarch.conroe,
    "penryn": peachpy.x86_64.uarch.penryn,
    "nehalem": peachpy.x86_64.uarch.nehalem,
    "sandybridge": peachpy.x86_64.uarch.sandy_bridge,
    "ivybridge": peachpy.x86_64.uarch.ivy_bridge,
    "haswell": peachpy.x86_64.uarch.haswell,
    "broadwell": peachpy.x86_64.uarch.broadwell,
    "skylake": peachpy.x86_64.uarch.skylake,
    "skylake-xeon": peachpy.x86_64.uarch.skylake_xeon,
    "cannonlake": peachpy.x86_64.uarch.cannonlake,
    "k8": peachpy.x86_64.uarch.k8,
    "k10": peachpy.x86_64.uarch.k10,
    "bulldozer": peachpy.x86_64.uarch.bulldozer,
    "piledriver": peachpy.x86_64.uarch.piledriver,
    "steamroller": peachpy.x86_64.uarch.steamroller,
    "excavator": peachpy.x86_64.uarch.excavator,
    "zen": peachpy.x86_64.uarch.zen,
    "bonnell": peachpy.x86_64.uarch.bonnell,
    "saltwell": peachpy.x86_64.uarch.saltwell,
    "silvermont": peachpy.x86_64.uarch.silvermont,
    "airmont": peachpy.x86_64.uarch.airmont,
    "goldmont": peachpy.x86_64.uarch.goldmont,
    "bobcat": peachpy.x86_64.uarch.bobcat,
    "jaguar": peachpy.x86_64.uarch.jaguar,
    "knightslanding": peachpy.x86_64.uarch.knights_landing
}
parser.add_argument("-mcpu", dest="cpu", default="default",
                    choices=("default", "prescott", "conroe", "penryn", "nehalem", "sandybridge", "ivybridge",
                             "haswell", "broadwell", "skylake", "skylake-xeon", "cannonlake",
                             "k8", "k10", "bulldozer", "piledriver", "steamroller", "excavator", "zen",
                             "bonnell", "saltwell", "silvermont", "airmont", "goldmont",
                             "bobcat", "jaguar",
                             "knightslanding"),
                    help="Target specified microarchitecture")

parser.add_argument("-mimage-format", dest="image_format", default="native",
                    choices=("native", "elf", "mach-o", "ms-coff"),
                    help="Target binary image format")
parser.add_argument("-massembly-format", dest="assembly_format",
                    choices=("golang", "nasm", "gas", "masm"),
                    help="Target assembly format")

parser.add_argument("-fpackage", dest="package", default="",
                    help="Use specified Go package name in generated Plan 9 assembly listings")
avx_group = parser.add_mutually_exclusive_group()
avx_group.add_argument("-mavx", dest="avx", action="store_true",
                       help="Enable AVX extension")
avx_group.add_argument("-mno-avx", dest="avx", action="store_false",
                       help="Disable AVX extension")
xop_group = parser.add_mutually_exclusive_group()
xop_group.add_argument("-mxop", dest="xop", action="store_true",
                       help="Enable XOP extension")
xop_group.add_argument("-mno-xop", dest="xop", action="store_false",
                       help="Disable XOP extension")
fma4_group = parser.add_mutually_exclusive_group()
fma4_group.add_argument("-mfma4", dest="fma4", action="store_true",
                        help="Enable FMA4 extension")
fma4_group.add_argument("-mno-fma4", dest="fma4", action="store_false",
                        help="Disable FMA4 extension")
fma3_group = parser.add_mutually_exclusive_group()
fma3_group.add_argument("-mfma3", dest="fma3", action="store_true",
                        help="Enable FMA3 extension")
fma3_group.add_argument("-mno-fma3", dest="fma3", action="store_false",
                        help="Disable FMA3 extension")
f16c_group = parser.add_mutually_exclusive_group()
f16c_group.add_argument("-mf16c", dest="f16c", action="store_true",
                        help="Enable F16C extension")
f16c_group.add_argument("-mno-f16c", dest="f16c", action="store_false",
                        help="Disable F16C extension")
avx2_group = parser.add_mutually_exclusive_group()
avx2_group.add_argument("-mavx2", dest="avx2", action="store_true",
                        help="Enable AVX2 extension")
avx2_group.add_argument("-mno-avx2", dest="avx2", action="store_false",
                        help="Disable AVX2 extension")
parser.add_argument("-o", dest="output", required=True,
                    help="Output file name (ELF/Mach-O/COFF image or Go assembly source)")
parser.add_argument("input", nargs=1,
                    help="Input file name (must be a PeachPy Python script)")


def guess_assembly_format_from_abi(abi):
    _, supported_assembly_formats, _ = abi_map[abi]
    return supported_assembly_formats[0]


def check_abi_assembly_format_combination(abi, assembly_format):
    _, supported_assembly_formats, _ = abi_map[abi]
    if assembly_format not in supported_assembly_formats:
        raise ValueError("Assembly format %s is not supported for %s" % (assembly_format, str(abi)))


def check_abi_image_format_combination(image_format, abi):
    _, _, supported_image_formats = abi_map[abi]
    if image_format not in supported_image_formats:
        raise ValueError("Image format %s is not supported for %s" % (image_format, str(abi)))


def detect_native_image_format():
    import platform
    osname = platform.system()
    if osname == "Darwin":
        return "mach-o"
    elif osname in ["Linux", "NaCl", "FreeBSD"]:
        return "elf"
    elif osname == "Windows":
        return "ms-coff"


def add_module_files(module_files, module, roots):
    """Recursively adds Python source files for module and its submodules inside the roots directories"""
    if not hasattr(module, "__file__"):
        return

    module_file = module.__file__
    if module_file is None:
        return

    import os
    if not any(module_file.startswith(root + os.sep) for root in roots):
        # The file is not inside any of the monitored roots
        # This is typical for system modules
        return

    if module_file.endswith(".pyc") or module_file.endswith(".pyo"):
        module_source_file = module_file[:-4] + ".py"
        if os.path.isfile(module_source_file):
            module_file = module_source_file

    if module_file in module_files:
        # This module was already added under a different name
        return
    module_files.add(module_file)

    from types import ModuleType
    for variable_name in dir(module):
        if variable_name.startswith("__"):
            continue

        variable = getattr(module, variable_name)
        if isinstance(variable, ModuleType):
            add_module_files(module_files, variable, roots)


def execute_script(writers, source_filename):
    if writers:
        writer = writers.pop()
        with writer:
            execute_script(writers, source_filename)
    else:
        with open(source_filename) as input_file:
            code = compile(input_file.read(), source_filename, 'exec')
            exec(code, globals())


def main():
    options = parser.parse_args()
    import peachpy.x86_64.options
    peachpy.x86_64.options.debug_level = options.debug_level
    if options.abi == "native":
        abi = peachpy.x86_64.abi.detect(system_abi=True)
        if abi is None:
            raise ValueError("Could not auto-detect ABI: specify it with -mabi option")
        # Set options.abi to the corresponding string value because it is used later on
        options.abi = {abi: name for name, (abi, _, _) in six.iteritems(abi_map)}[abi]
    else:
        abi, _, _ = abi_map[options.abi]
    peachpy.x86_64.options.abi = abi
    peachpy.x86_64.options.target = cpu_map[options.cpu]
    peachpy.x86_64.options.package = options.package
    peachpy.x86_64.options.generate_assembly = options.generate_assembly
    if options.name_mangling:
        peachpy.x86_64.options.name_mangling = options.name_mangling

    from peachpy.writer import ELFWriter, MachOWriter, MSCOFFWriter, AssemblyWriter, JSONMetadataWriter, CHeaderWriter
    writers = []
    if peachpy.x86_64.options.generate_assembly:
        assembly_format = options.assembly_format
        if assembly_format is None:
            assembly_format = guess_assembly_format_from_abi(options.abi)
        else:
            check_abi_assembly_format_combination(options.abi, assembly_format)
        writers.append(AssemblyWriter(options.output, assembly_format, options.input[0]))
    else:
        image_format = options.image_format
        if image_format == "native":
            image_format = detect_native_image_format()
            if image_format is None:
                raise ValueError("Could not auto-detect image format: specify it with -mimage-format option")
        check_abi_image_format_combination(image_format, options.abi)
        if image_format == "elf":
            writers.append(ELFWriter(options.output, abi, options.input[0]))
        elif image_format == "mach-o":
            writers.append(MachOWriter(options.output, abi))
        elif image_format == "ms-coff":
            writers.append(MSCOFFWriter(options.output, abi, options.input[0]))
        else:
            raise ValueError("Image format %s is not supported" % image_format)
    dependencies_makefile_path = options.output + ".d"
    if options.dependencies_makefile_path:
        dependencies_makefile_path = options.dependencies_makefile_path
    if options.rtl_dump:
        peachpy.x86_64.options.rtl_dump_file = open(options.rtl_dump, "w")
    if options.c_header_file:
        writers.append(CHeaderWriter(options.c_header_file, options.input[0]))
    if options.json_metadata_file:
        writers.append(JSONMetadataWriter(options.json_metadata_file))

    # PeachPy sources can import other modules or files from the same directory
    import os
    include_directories = [os.path.abspath(include_dir) for include_dir in options.include]
    include_directories.insert(0, os.path.abspath(os.path.dirname(options.input[0])))
    sys.path.extend(include_directories)

    # We would like to avoid situations where source file has changed, but Python uses its old precompiled version
    sys.dont_write_bytecode = True

    execute_script(writers, options.input[0])

    if options.generate_dependencies_makefile:
        module_files = set()
        for module in sys.modules.values():
            add_module_files(module_files, module, include_directories)

        dependencies = list(sorted(module_files))
        dependencies.insert(0, options.input[0])
        with open(dependencies_makefile_path, "w") as dependencies_makefile:
            dependencies_makefile.write(options.output + ": \\\n  " + " \\\n  ".join(dependencies) + "\n")

if __name__ == "__main__":
    main()
