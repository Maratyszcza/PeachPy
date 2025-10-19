# ARMv7-M Support in PeachPy

This document describes the ARMv7-M architecture support added to PeachPy, enabling assembly generation for ARM Cortex-M processors in both GAS (GNU Assembler) and ARMCC (ARM Compiler) formats.

## Overview

ARMv7-M is the ARM architecture used in Cortex-M3, M4, and M7 processors, which are widely used in microcontrollers and embedded systems. This implementation adds:

1. **ARMv7-M ISA Extensions** - Support for the ARMv7-M instruction set architecture
2. **Cortex-M Microarchitectures** - Specific processor definitions for M0, M0+, M1, M3, M4, and M7
3. **Multiple Assembly Formats** - Generate code for both GAS and ARMCC assemblers
4. **DSP Extensions** - Support for DSP instructions on M4/M7 processors
5. **VFP Support** - Floating-point unit support for M4/M7 processors

## Supported Processors

### Cortex-M0/M0+/M1 (ARMv6-M)
- **Architecture**: ARMv6-M
- **Extensions**: Thumb2
- **Features**: Basic ARM instructions, Thumb-2 technology
- **Target Use**: Low-power, cost-sensitive applications

### Cortex-M3 (ARMv7-M)
- **Architecture**: ARMv7-M
- **Extensions**: V7M, Thumb2
- **Features**: Enhanced instruction set, hardware divide
- **Target Use**: General-purpose microcontroller applications

### Cortex-M4 (ARMv7-M + DSP)
- **Architecture**: ARMv7-M
- **Extensions**: V7M, Thumb2, DSP, VFP4
- **Features**: DSP instructions, single-precision floating-point
- **Target Use**: Digital signal processing, motor control

### Cortex-M7 (ARMv7-M + DSP + Enhanced VFP)
- **Architecture**: ARMv7-M
- **Extensions**: V7M, Thumb2, DSP, VFP4, VFPd32
- **Features**: Double-precision floating-point, cache, advanced DSP
- **Target Use**: High-performance embedded applications

## Assembly Format Support

### GAS (GNU Assembler) Format
The default format, compatible with GCC toolchain:

```assembly
.section .text.CortexM3,"ax",%progbits
BEGIN_ARM_FUNCTION function_name
    .arch armv7-m
    .fpu vfpv4
Lfunction_name.ENTRY:
    // Instructions here
    BX lr
END_ARM_FUNCTION function_name
```

### ARMCC (ARM Compiler) Format
Compatible with ARM's official compiler toolchain:

```assembly
        AREA    |.text|, CODE, READONLY
        ARM
        REQUIRE VFPv4

function_name    PROC
        EXPORT  function_name
        // Instructions here
        BX lr
        ENDP
        END
```

## Usage Examples

### Basic Setup

```python
from peachpy import *
from peachpy.arm import *
from peachpy.arm.abi import arm_gnueabihf
from peachpy.arm.microarchitecture import Microarchitecture
from peachpy.arm.formats import AssemblyFormat

# Define function arguments
input_arg = Argument(ptr(const_uint32_t))
output_arg = Argument(ptr(uint32_t))
count_arg = Argument(size_t)
```

### Cortex-M3 Function (GAS Format)

```python
with Function("process_data", (input_arg, output_arg, count_arg),
             target=Microarchitecture.CortexM3,
             abi=arm_gnueabihf,
             assembly_format=AssemblyFormat.GAS,
             report_generation=False) as func:
    
    (input_ptr, output_ptr, count) = LOAD.ARGUMENTS()
    
    with Loop() as loop:
        value = GeneralPurposeRegister()
        LDR(value, [input_ptr], 4)
        ADD(value, value, 1)  # Simple processing
        STR(value, [output_ptr], 4)
        SUBS(count, count, 4)
        BNE(loop.begin)
    
    RETURN()

print(func.assembly)
```

### Cortex-M4 Function (ARMCC Format)

```python
with Function("dsp_process", (input_arg, output_arg, count_arg),
             target=Microarchitecture.CortexM4,
             abi=arm_gnueabihf,
             assembly_format=AssemblyFormat.ARMCC,
             report_generation=False) as func:
    
    (input_ptr, output_ptr, count) = LOAD.ARGUMENTS()
    
    with Loop() as loop:
        value = GeneralPurposeRegister()
        LDR(value, [input_ptr], 4)
        LSL(value, value, 1)  # DSP operation: multiply by 2
        STR(value, [output_ptr], 4)
        SUBS(count, count, 4)
        BNE(loop.begin)
    
    RETURN()

print(func.assembly)
```

## API Reference

### Microarchitectures

- `Microarchitecture.CortexM0` - ARM Cortex-M0 processor
- `Microarchitecture.CortexM0Plus` - ARM Cortex-M0+ processor  
- `Microarchitecture.CortexM1` - ARM Cortex-M1 processor
- `Microarchitecture.CortexM3` - ARM Cortex-M3 processor
- `Microarchitecture.CortexM4` - ARM Cortex-M4 processor
- `Microarchitecture.CortexM7` - ARM Cortex-M7 processor

### Assembly Formats

- `AssemblyFormat.GAS` - GNU Assembler format (default)
- `AssemblyFormat.ARMCC` - ARM Compiler assembler format

### Function Constructor Parameters

```python
Function(name, arguments, return_type=None,
         target=Microarchitecture.Default,
         abi=None,
         assembly_format=None,  # New parameter
         collect_origin=False,
         dump_intermediate_assembly=False,
         report_generation=True,
         report_live_registers=False)
```

### New Parameter
- `assembly_format`: Specify output format (`AssemblyFormat.GAS` or `AssemblyFormat.ARMCC`)
  - Default: `AssemblyFormat.GAS` if not specified

## Examples

See `examples/arm_cortex_m_example.py` for comprehensive examples demonstrating:
- Basic integer processing functions
- VFP floating-point operations
- DSP signal processing
- Assembly format comparisons

## Testing

Run the ARMv7-M specific tests:

```bash
python -m pytest tests/arm/test_armv7m.py -v
```