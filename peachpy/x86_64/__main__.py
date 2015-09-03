# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from peachpy import *
from peachpy.x86_64 import *
import sys
import argparse


parser = argparse.ArgumentParser(
    description="Peach-Py: Portable Efficient Assembly Code-generation in High-level Python")
parser.add_argument("-g", dest="debug_level", type=int, default=0,
                    help="Debug information level")
parser.add_argument("-S", dest="generate_assembly", action="store_true",
                    help="Generate assembly listing on output")

abi_map = {
    "ms": (peachpy.x86_64.abi.microsoft_x64_abi, ["masm", "nasm"], ["ms-coff"]),
    "sysv": (peachpy.x86_64.abi.system_v_x86_64_abi, ["gas", "nasm"], ["elf", "mach-o"]),
    "x32": (peachpy.x86_64.abi.linux_x32_abi, ["gas"], ["elf"]),
    "nacl": (peachpy.x86_64.abi.native_client_x86_64_abi, ["gas"], ["elf"]),
    "gosyso": (peachpy.x86_64.abi.goasm_amd64_abi, ["go"], []),
    "goasm": (peachpy.x86_64.abi.gosyso_amd64_abi, ["go"], []),
    "gosyso-p32": (peachpy.x86_64.abi.gosyso_amd64p32_abi, ["gas"], []),
    "goasm-p32": (peachpy.x86_64.abi.goasm_amd64p32_abi, ["gas"], [])
}
parser.add_argument("-mabi", dest="abi", required=True,
                    choices=("ms", "sysv", "x32", "nacl", "gosyso", "gosyso-p32", "goasm", "goasm-p32"),
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
    "k8": peachpy.x86_64.uarch.k8,
    "k10": peachpy.x86_64.uarch.k10,
    "bulldozer": peachpy.x86_64.uarch.bulldozer,
    "piledriver": peachpy.x86_64.uarch.piledriver,
    "steamroller": peachpy.x86_64.uarch.steamroller,
    "bonnell": peachpy.x86_64.uarch.bonnell,
    "saltwell": peachpy.x86_64.uarch.saltwell,
    "silvermont": peachpy.x86_64.uarch.silvermont,
    "bobcat": peachpy.x86_64.uarch.bobcat,
    "jaguar": peachpy.x86_64.uarch.jaguar
}
parser.add_argument("-mcpu", dest="cpu", default="default",
                    choices=("default", "prescott", "conroe", "penryn", "nehalem", "sandybridge", "ivybridge",
                             "haswell", "broadwell", "k8", "k10", "bulldozer", "piledriver", "steamroller",
                             "bonnell", "saltwell", "silvermont", "bobcat", "jaguar"),
                    help="Target specified microarchitecture")

parser.add_argument("-mimage-format", dest="image_format",
                    choices=("elf", "mach-o", "ms-coff"),
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
                    help="Input file name (must be a Peach-Py Python script)")


def guess_assembly_format_from_abi(abi):
    _, supported_assembly_formats, _ = abi_map[abi]
    return supported_assembly_formats[0]


def check_abi_assembly_format_combination(assembly_format, abi):
    _, supported_assembly_formats, _ = abi_map[abi]
    if assembly_format not in supported_assembly_formats:
        raise ValueError("Assembly format %s is not supported for %s" % (assembly_format, str(abi)))


def check_abi_image_format_combination(image_format, abi):
    _, _, supported_image_formats = abi_map[abi]
    if image_format not in supported_image_formats:
        raise ValueError("Image format %s is not supported for %s" % (image_format, str(abi)))


def main():
    options = parser.parse_args()
    import peachpy.x86_64.options
    peachpy.x86_64.options.debug_level = options.debug_level
    abi, _, _ = abi_map[options.abi]
    peachpy.x86_64.options.abi = abi
    peachpy.x86_64.options.target = cpu_map[options.cpu]
    peachpy.x86_64.options.package = options.package
    peachpy.x86_64.options.generate_assembly = options.generate_assembly

    import peachpy.writer
    writer = peachpy.writer.NullWriter()
    if peachpy.x86_64.options.generate_assembly:
        assembly_format = options.assembly_format
        if assembly_format is None:
            assembly_format = guess_assembly_format_from_abi(options.abi)
        else:
            check_abi_assembly_format_combination(options.abi, assembly_format)
        writer = peachpy.writer.AssemblyWriter(options.output, assembly_format, options.input[0])
    else:
        image_format = options.image_format
        if image_format is None:
            raise ValueError("Image format is not specified")
        check_abi_image_format_combination(image_format, options.abi)
        if image_format == "elf":
            writer = peachpy.writer.ELFWriter(options.output, abi, options.input[0])
        elif image_format == "mach-o":
            writer = peachpy.writer.MachOWriter(options.output, abi)
        elif image_format == "ms-coff":
            writer = peachpy.writer.MSCOFFWriter(options.output, abi, options.input[0])
        else:
            raise ValueError("Image format %s is not supported" % image_format)

    with writer:
        import os
        sys.path.append(os.path.dirname(options.input[0]))
        with open(options.input[0]) as input_file:
            code = compile(input_file.read(), options.input[0], 'exec')
            exec(code, globals())


if __name__ == "__main__":
    sys.exit(main())
