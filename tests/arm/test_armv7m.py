import unittest
from nervapy import *
from nervapy.arm import *
from nervapy.arm.abi import arm_gnueabihf
from nervapy.arm.microarchitecture import Microarchitecture
from nervapy.arm.formats import AssemblyFormat


class TestARMv7M(unittest.TestCase):
    def test_cortex_m3_gas_assembly(self):
        """Test ARMv7-M assembly generation for Cortex-M3 with GAS format."""
        # Implement function void add_1(const uint32_t *src, uint32_t *dst, size_t length)
        source_arg = Argument(ptr(const_uint32_t))
        destination_arg = Argument(ptr(uint32_t))
        length_arg = Argument(size_t)

        with Function("add_1", (source_arg, destination_arg, length_arg), 
                     target=Microarchitecture.CortexM3,
                     abi=arm_gnueabihf, 
                     assembly_format=AssemblyFormat.GAS,
                     report_generation=False) as add_function:
            # Load arguments into registers
            (source, destination, length) = LOAD.ARGUMENTS()

            # Main processing loop. Length must be a multiple of 4.
            with Loop() as loop:
                x = GeneralPurposeRegister()
                LDR(x, [source], 4)

                # Add 1 to x
                ADD(x, x, 1)

                STR(x, [destination], 4)

                SUBS(length, 4)
                BNE(loop.begin)

            RETURN()

        assembly = add_function.assembly
        print("Cortex-M3 GAS Assembly:")
        print(assembly)
        
        # Verify ARMv7-M architecture specification
        self.assertIn(".arch armv7-m", assembly)
        # Verify function structure
        self.assertIn("BEGIN_ARM_FUNCTION add_1", assembly)
        self.assertIn("END_ARM_FUNCTION add_1", assembly)

    def test_cortex_m4_armcc_assembly(self):
        """Test ARMv7-M assembly generation for Cortex-M4 with ARMCC format."""
        # Implement function void simple_add(const uint32_t *a, const uint32_t *b, uint32_t *result, size_t length)
        a_arg = Argument(ptr(const_uint32_t))
        b_arg = Argument(ptr(const_uint32_t))
        result_arg = Argument(ptr(uint32_t))
        length_arg = Argument(size_t)

        with Function("simple_add", (a_arg, b_arg, result_arg, length_arg), 
                     target=Microarchitecture.CortexM4,
                     abi=arm_gnueabihf, 
                     assembly_format=AssemblyFormat.ARMCC,
                     report_generation=False) as add_function:
            # Load arguments into registers
            (a, b, result, length) = LOAD.ARGUMENTS()

            # Main processing loop
            with Loop() as loop:
                val_a = GeneralPurposeRegister()
                val_b = GeneralPurposeRegister()
                val_result = GeneralPurposeRegister()
                
                LDR(val_a, [a], 4)
                LDR(val_b, [b], 4)
                
                # Add values
                ADD(val_result, val_a, val_b)
                
                STR(val_result, [result], 4)

                SUBS(length, 4)
                BNE(loop.begin)

            RETURN()

        assembly = add_function.assembly
        print("\nCortex-M4 ARMCC Assembly:")
        print(assembly)
        
        # Verify ARMCC format characteristics
        self.assertIn("AREA    |.text|, CODE, READONLY", assembly)
        self.assertIn("PROC", assembly)
        self.assertIn("ENDP", assembly)
        self.assertIn("EXPORT", assembly)

    def test_cortex_m7_gas_assembly_with_dsp(self):
        """Test ARMv7-M assembly generation for Cortex-M7 with DSP extensions."""
        # Simple DSP function
        input_arg = Argument(ptr(const_int32_t))
        output_arg = Argument(ptr(int32_t))
        length_arg = Argument(size_t)

        with Function("dsp_process", (input_arg, output_arg, length_arg), 
                     target=Microarchitecture.CortexM7,
                     abi=arm_gnueabihf, 
                     assembly_format=AssemblyFormat.GAS,
                     report_generation=False) as dsp_function:
            # Load arguments into registers
            (input_ptr, output_ptr, length) = LOAD.ARGUMENTS()

            # Simple processing loop
            with Loop() as loop:
                value = GeneralPurposeRegister()
                LDR(value, [input_ptr], 4)
                
                # Simple bit manipulation (shift left by 1)
                LSL(value, value, 1)
                
                STR(value, [output_ptr], 4)

                SUBS(length, 4)
                BNE(loop.begin)

            RETURN()

        assembly = dsp_function.assembly
        print("\nCortex-M7 GAS Assembly:")
        print(assembly)
        
        # Verify ARMv7-M architecture
        self.assertIn(".arch armv7-m", assembly)
        # Verify VFPv4 support for M7
        self.assertIn(".fpu", assembly)


if __name__ == '__main__':
    unittest.main()