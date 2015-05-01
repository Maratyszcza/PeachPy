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
    "ms": peachpy.x86_64.abi.microsoft_x64_abi,
    "sysv": peachpy.x86_64.abi.system_v_x86_64_abi,
    "x32": peachpy.x86_64.abi.linux_x32_abi,
    "nacl": peachpy.x86_64.abi.native_client_x86_64_abi,
    "golang": peachpy.x86_64.abi.golang_amd64_abi,
    "golang-p32": peachpy.x86_64.abi.golang_amd64p32_abi
}
parser.add_argument("-mabi", dest="abi", required=True,
                    choices=("ms", "sysv", "x32", "nacl", "golang", "golang-p32"),
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
parser.add_argument("-mcpu", dest="cpu", required=True,
                    choices=("default", "prescott", "conroe", "penryn", "nehalem", "sandybridge", "ivybridge",
                             "haswell", "broadwell", "k8", "k10", "bulldozer", "piledriver", "steamroller",
                             "bonnell", "saltwell", "silvermont", "bobcat", "jaguar"),
                    help="Target specified microarchitecture")
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


def main():
    options = parser.parse_args()
    import peachpy.x86_64.options
    peachpy.x86_64.options.debug_level = options.debug_level
    peachpy.x86_64.options.abi = abi_map[options.abi]
    peachpy.x86_64.options.target = cpu_map[options.cpu]
    peachpy.x86_64.options.package = options.package
    peachpy.x86_64.options.generate_assembly = options.generate_assembly

    import peachpy.writer
    writer = peachpy.writer.NullWriter()
    if peachpy.x86_64.options.generate_assembly:
        if peachpy.x86_64.options.abi in [peachpy.x86_64.abi.golang_amd64_abi, peachpy.x86_64.abi.golang_amd64p32_abi]:
            writer = peachpy.writer.AssemblyWriter(options.output, "go", options.input[0])
        else:
            raise ValueError("Assembly output for %s ABI is unsupported" % str(peachpy.x86_64.options.abi))
    else:
        if peachpy.x86_64.options.abi in [peachpy.x86_64.abi.system_v_x86_64_abi,
                                          peachpy.x86_64.abi.linux_x32_abi,
                                          peachpy.x86_64.abi.native_client_x86_64_abi]:
            writer = peachpy.writer.ELFWriter(options.output, peachpy.x86_64.options.abi, options.input[0])
        else:
            raise ValueError("Binary output for %s ABI is unsupported" % str(peachpy.x86_64.options.abi))

    with writer:
        with open(options.input[0]) as input_file:
            code = compile(input_file.read(), options.input[0], 'exec')
            exec(code, globals())


if __name__ == "__main__":
    sys.exit(main())
