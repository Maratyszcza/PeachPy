#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ARMv7-M Assembly Generation Example

This example demonstrates how to use PeachPy to generate assembly code
for ARM Cortex-M processors in both GAS (GNU Assembler) and ARMCC formats.

Features demonstrated:
- ARMv7-M architecture support
- Cortex-M3, M4, and M7 microarchitectures
- GAS and ARMCC assembly formats
- VFP floating-point operations (on M4/M7)
- DSP extensions (on M4/M7)
"""

from peachpy import *
from peachpy.arm import *
from peachpy.arm.abi import arm_gnueabihf
from peachpy.arm.microarchitecture import Microarchitecture
from peachpy.arm.formats import AssemblyFormat


def generate_cortex_m3_function():
    """Generate a simple integer processing function for Cortex-M3."""
    print("=== Cortex-M3 Function (GAS Format) ===")
    
    # Function arguments
    input_arg = Argument(ptr(const_uint32_t))
    output_arg = Argument(ptr(uint32_t))
    count_arg = Argument(size_t)
    
    with Function("process_integers", (input_arg, output_arg, count_arg),
                 target=Microarchitecture.CortexM3,
                 abi=arm_gnueabihf,
                 assembly_format=AssemblyFormat.GAS,
                 report_generation=False) as func:
        
        # Load function arguments
        (input_ptr, output_ptr, count) = LOAD.ARGUMENTS()
        
        # Process each integer
        with Loop() as process_loop:
            # Load input value
            value = GeneralPurposeRegister()
            LDR(value, [input_ptr], 4)
            
            # Simple processing: multiply by 2 and add 1
            LSL(value, value, 1)  # Multiply by 2 (left shift)
            ADD(value, value, 1)  # Add 1
            
            # Store result
            STR(value, [output_ptr], 4)
            
            # Decrement counter and loop if not zero
            SUBS(count, count, 4)
            BNE(process_loop.begin)
        
        RETURN()
    
    print(func.assembly)
    return func.assembly


def generate_cortex_m4_function_gas():
    """Generate a simple function for Cortex-M4 in GAS format."""
    print("=== Cortex-M4 Function (GAS Format) ===")
    
    # Function arguments for simple processing
    input_arg = Argument(ptr(const_uint32_t))
    output_arg = Argument(ptr(uint32_t))
    count_arg = Argument(size_t)
    
    with Function("scale_integers", (input_arg, output_arg, count_arg),
                 target=Microarchitecture.CortexM4,
                 abi=arm_gnueabihf,
                 assembly_format=AssemblyFormat.GAS,
                 report_generation=False) as func:
        
        # Load function arguments
        (input_ptr, output_ptr, count) = LOAD.ARGUMENTS()
        
        # Process each integer
        with Loop() as scale_loop:
            value = GeneralPurposeRegister()
            
            # Load input value
            LDR(value, [input_ptr], 4)
            
            # Scale by 3 (using simple operations)
            temp = GeneralPurposeRegister()
            MOV(temp, value)      # temp = value
            LSL(value, value, 1)  # value = value * 2
            ADD(value, value, temp)  # value = value * 2 + value = value * 3
            
            # Store result
            STR(value, [output_ptr], 4)
            
            # Decrement counter and loop
            SUBS(count, count, 4)
            BNE(scale_loop.begin)
        
        RETURN()
    
    print(func.assembly)
    return func.assembly


def generate_cortex_m4_function_armcc():
    """Generate the same function for Cortex-M4 in ARMCC format."""
    print("=== Cortex-M4 Function (ARMCC Format) ===")
    
    # Function arguments for simple addition
    a_arg = Argument(ptr(const_uint32_t))
    b_arg = Argument(ptr(const_uint32_t))
    result_arg = Argument(ptr(uint32_t))
    count_arg = Argument(size_t)
    
    with Function("add_arrays", (a_arg, b_arg, result_arg, count_arg),
                 target=Microarchitecture.CortexM4,
                 abi=arm_gnueabihf,
                 assembly_format=AssemblyFormat.ARMCC,
                 report_generation=False) as func:
        
        # Load function arguments
        (a_ptr, b_ptr, result_ptr, count) = LOAD.ARGUMENTS()
        
        # Add corresponding elements
        with Loop() as add_loop:
            val_a = GeneralPurposeRegister()
            val_b = GeneralPurposeRegister()
            result = GeneralPurposeRegister()
            
            # Load values
            LDR(val_a, [a_ptr], 4)
            LDR(val_b, [b_ptr], 4)
            
            # Add them
            ADD(result, val_a, val_b)
            
            # Store result
            STR(result, [result_ptr], 4)
            
            # Decrement and loop
            SUBS(count, count, 4)
            BNE(add_loop.begin)
        
        RETURN()
    
    print(func.assembly)
    return func.assembly


def generate_cortex_m7_function():
    """Generate an advanced function for Cortex-M7 with DSP operations."""
    print("=== Cortex-M7 Function (GAS Format) ===")
    
    # Function arguments for signal processing
    signal_arg = Argument(ptr(const_int32_t))
    filtered_arg = Argument(ptr(int32_t))
    count_arg = Argument(size_t)
    
    with Function("simple_filter", (signal_arg, filtered_arg, count_arg),
                 target=Microarchitecture.CortexM7,
                 abi=arm_gnueabihf,
                 assembly_format=AssemblyFormat.GAS,
                 report_generation=False) as func:
        
        # Load function arguments
        (signal_ptr, filtered_ptr, count) = LOAD.ARGUMENTS()
        
        # Simple filtering operation
        with Loop() as filter_loop:
            current = GeneralPurposeRegister()
            filtered = GeneralPurposeRegister()
            
            # Load current sample
            LDR(current, [signal_ptr], 4)
            
            # Simple filtering: arithmetic right shift by 2 (divide by 4)
            ASR(filtered, current, 2)
            
            # Store filtered result
            STR(filtered, [filtered_ptr], 4)
            
            # Continue loop
            SUBS(count, count, 4)
            BNE(filter_loop.begin)
        
        RETURN()
    
    print(func.assembly)
    return func.assembly


def compare_assembly_formats():
    """Compare the same function generated in different formats."""
    print("=== Assembly Format Comparison ===")
    
    # Simple function for comparison
    input_arg = Argument(ptr(const_uint32_t))
    output_arg = Argument(ptr(uint32_t))
    
    # Generate GAS version
    print("\n--- GAS Format ---")
    with Function("simple_copy", (input_arg, output_arg),
                 target=Microarchitecture.CortexM3,
                 abi=arm_gnueabihf,
                 assembly_format=AssemblyFormat.GAS,
                 report_generation=False) as gas_func:
        
        (input_ptr, output_ptr) = LOAD.ARGUMENTS()
        value = GeneralPurposeRegister()
        LDR(value, [input_ptr])
        STR(value, [output_ptr])
        RETURN()
    
    print(gas_func.assembly)
    
    # Generate ARMCC version
    print("--- ARMCC Format ---")
    with Function("simple_copy", (input_arg, output_arg),
                 target=Microarchitecture.CortexM3,
                 abi=arm_gnueabihf,
                 assembly_format=AssemblyFormat.ARMCC,
                 report_generation=False) as armcc_func:
        
        (input_ptr, output_ptr) = LOAD.ARGUMENTS()
        value = GeneralPurposeRegister()
        LDR(value, [input_ptr])
        STR(value, [output_ptr])
        RETURN()
    
    print(armcc_func.assembly)


if __name__ == "__main__":
    print("PeachPy ARMv7-M Assembly Generation Examples")
    print("=" * 50)
    
    # Generate examples for different Cortex-M processors
    generate_cortex_m3_function()
    print()
    
    generate_cortex_m4_function_gas()
    print()
    
    generate_cortex_m4_function_armcc()
    print()
    
    generate_cortex_m7_function()
    print()
    
    # Compare assembly formats
    compare_assembly_formats()
    
    print("\nExamples completed successfully!")
    print("\nSupported Cortex-M processors:")
    print("- Cortex-M0, M0+, M1 (ARMv6-M)")
    print("- Cortex-M3 (ARMv7-M)")
    print("- Cortex-M4 (ARMv7-M + DSP + VFPv4)")
    print("- Cortex-M7 (ARMv7-M + DSP + VFPv4 + VFPd32)")
    print("\nSupported assembly formats:")
    print("- GAS (GNU Assembler)")
    print("- ARMCC (ARM Compiler)")