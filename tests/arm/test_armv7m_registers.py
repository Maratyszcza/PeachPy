import unittest
from nervapy import *
from nervapy.arm import *
from nervapy.arm.abi import arm_gnueabihf
from nervapy.arm.microarchitecture import Microarchitecture
from nervapy.arm.formats import AssemblyFormat


class TestARMv7MRegisterConstraints(unittest.TestCase):
    def test_cortex_m3_low_register_push_pop(self):
        """Test that Cortex-M3 uses efficient PUSH/POP for low registers."""
        print("=== Testing Cortex-M3 Low Register PUSH/POP ===")
        
        # Function that should only use low registers
        input_arg = Argument(ptr(const_uint32_t))
        output_arg = Argument(ptr(uint32_t))
        temp_arg = Argument(uint32_t)
        
        with Function("low_reg_function", (input_arg, output_arg, temp_arg),
                     target=Microarchitecture.CortexM3,
                     abi=arm_gnueabihf,
                     assembly_format=AssemblyFormat.GAS,
                     report_generation=False) as func:
            
            (input_ptr, output_ptr, temp_val) = LOAD.ARGUMENTS()
            
            # Use several registers to force some to be preserved
            val1 = GeneralPurposeRegister()
            val2 = GeneralPurposeRegister()
            val3 = GeneralPurposeRegister()
            
            LDR(val1, [input_ptr])
            ADD(val2, val1, temp_val)
            ADD(val3, val2, val1)  # Use ADD instead of MUL
            STR(val3, [output_ptr])
            
            RETURN()
        
        assembly = func.assembly
        print(assembly)
        
        # Verify that we have PUSH/POP operations
        self.assertIn("PUSH", assembly)
        self.assertIn("POP", assembly)
        
        # For ARMv7-M, should prefer low register usage
        self.assertIn(".arch armv7-m", assembly)
        
        return assembly

    def test_cortex_m4_mixed_register_usage(self):
        """Test Cortex-M4 with mixed register usage patterns."""
        print("\n=== Testing Cortex-M4 Mixed Register Usage ===")
        
        # Function that might use high registers
        a_arg = Argument(ptr(const_uint32_t))
        b_arg = Argument(ptr(const_uint32_t))
        c_arg = Argument(ptr(const_uint32_t))
        result_arg = Argument(ptr(uint32_t))
        count_arg = Argument(size_t)
        
        with Function("complex_processing", (a_arg, b_arg, c_arg, result_arg, count_arg),
                     target=Microarchitecture.CortexM4,
                     abi=arm_gnueabihf,
                     assembly_format=AssemblyFormat.GAS,
                     report_generation=False) as func:
            
            (a_ptr, b_ptr, c_ptr, result_ptr, count) = LOAD.ARGUMENTS()
            
            # Complex processing that might need many registers
            with Loop() as process_loop:
                a_val = GeneralPurposeRegister()
                b_val = GeneralPurposeRegister()
                c_val = GeneralPurposeRegister()
                temp1 = GeneralPurposeRegister()
                temp2 = GeneralPurposeRegister()
                result = GeneralPurposeRegister()
                
                # Load three values
                LDR(a_val, [a_ptr], 4)
                LDR(b_val, [b_ptr], 4)
                LDR(c_val, [c_ptr], 4)
                
                # Complex computation requiring multiple temporary registers
                ADD(temp1, a_val, b_val)
                ADD(temp2, temp1, c_val)
                LSL(result, temp2, 1)
                
                # Store result
                STR(result, [result_ptr], 4)
                
                # Loop control
                SUBS(count, count, 4)
                BNE(process_loop.begin)
            
            RETURN()
        
        assembly = func.assembly
        print(assembly)
        
        # Should have ARMv7-M architecture and VFP support
        self.assertIn(".arch armv7-m", assembly)
        self.assertIn(".fpu", assembly)
        
        return assembly

    def test_register_allocation_constraints(self):
        """Test that register allocation respects ARMv7-M constraints."""
        print("\n=== Testing Register Allocation Constraints ===")
        
        # Create a function that forces register spilling
        input_arg = Argument(ptr(const_uint32_t))
        output_arg = Argument(ptr(uint32_t))
        
        with Function("register_pressure", (input_arg, output_arg),
                     target=Microarchitecture.CortexM3,
                     abi=arm_gnueabihf,
                     assembly_format=AssemblyFormat.ARMCC,
                     report_generation=False) as func:
            
            (input_ptr, output_ptr) = LOAD.ARGUMENTS()
            
            # Force allocation of many registers
            regs = []
            for i in range(6):  # Force some register pressure
                reg = GeneralPurposeRegister()
                regs.append(reg)
                LDR(reg, [input_ptr], 4)
            
            # Use all the registers in computation
            result = GeneralPurposeRegister()
            MOV(result, regs[0])
            for reg in regs[1:]:
                ADD(result, result, reg)
            
            STR(result, [output_ptr])
            RETURN()
        
        assembly = func.assembly
        print(assembly)
        
        # Verify ARMCC format
        self.assertIn("AREA", assembly)
        self.assertIn("PROC", assembly)
        self.assertIn("ENDP", assembly)
        
        return assembly

    def test_comparison_with_cortex_a(self):
        """Compare ARMv7-M register handling with Cortex-A."""
        print("\n=== Comparing ARMv7-M vs Cortex-A Register Handling ===")
        
        input_arg = Argument(ptr(const_uint32_t))
        output_arg = Argument(ptr(uint32_t))
        
        # ARMv7-M version (Cortex-M3)
        print("--- Cortex-M3 (ARMv7-M) ---")
        with Function("test_func", (input_arg, output_arg),
                     target=Microarchitecture.CortexM3,
                     abi=arm_gnueabihf,
                     assembly_format=AssemblyFormat.GAS,
                     report_generation=False) as m3_func:
            
            (input_ptr, output_ptr) = LOAD.ARGUMENTS()
            temp1 = GeneralPurposeRegister()
            temp2 = GeneralPurposeRegister()
            LDR(temp1, [input_ptr])
            ADD(temp2, temp1, 42)
            STR(temp2, [output_ptr])
            RETURN()
        
        m3_assembly = m3_func.assembly
        print(m3_assembly)
        
        # Cortex-A version (ARMv7-A)
        print("--- Cortex-A9 (ARMv7-A) ---")
        with Function("test_func", (input_arg, output_arg),
                     target=Microarchitecture.CortexA9,
                     abi=arm_gnueabihf,
                     assembly_format=AssemblyFormat.GAS,
                     report_generation=False) as a9_func:
            
            (input_ptr, output_ptr) = LOAD.ARGUMENTS()
            temp1 = GeneralPurposeRegister()
            temp2 = GeneralPurposeRegister()
            LDR(temp1, [input_ptr])
            ADD(temp2, temp1, 42)
            STR(temp2, [output_ptr])
            RETURN()
        
        a9_assembly = a9_func.assembly
        print(a9_assembly)
        
        # Verify architectural differences
        self.assertIn(".arch armv7-m", m3_assembly)
        self.assertIn(".cpu cortex-a9", a9_assembly)
        
        return m3_assembly, a9_assembly


if __name__ == '__main__':
    # Run tests with detailed output
    test_case = TestARMv7MRegisterConstraints()
    
    print("Testing ARMv7-M Register Constraint Handling")
    print("=" * 60)
    
    try:
        test_case.test_cortex_m3_low_register_push_pop()
        print("✓ Low register PUSH/POP test passed")
    except Exception as e:
        print(f"✗ Low register test failed: {e}")
    
    try:
        test_case.test_cortex_m4_mixed_register_usage()
        print("✓ Mixed register usage test passed")
    except Exception as e:
        print(f"✗ Mixed register test failed: {e}")
    
    try:
        test_case.test_register_allocation_constraints()
        print("✓ Register allocation constraints test passed")
    except Exception as e:
        print(f"✗ Register allocation test failed: {e}")
    
    try:
        test_case.test_comparison_with_cortex_a()
        print("✓ Cortex-A comparison test passed")
    except Exception as e:
        print(f"✗ Cortex-A comparison test failed: {e}")
    
    print("\nRegister constraint testing completed!")