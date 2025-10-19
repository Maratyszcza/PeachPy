# ARMv7-M Register Push/Pop Analysis
#
# For ARMv7-M (Cortex-M), when dealing with high registers (r8-r15), we have options:
#
# 1. PUSH.W / POP.W (32-bit Thumb-2 instructions)
#    - Pros: Explicit wide encoding, clear intent, compact syntax
#    - Cons: Newer syntax, might not be supported by older assemblers
#    - Example: PUSH.W {r8, r9, r10, lr}
#
# 2. STMDB sp!, {...} / LDMIA sp!, {...} 
#    - Pros: Universal ARM/Thumb support, explicit stack operations
#    - Cons: More verbose, requires sp register specification
#    - Example: STMDB sp!, {r8, r9, r10, lr}
#
# 3. Mixed approach:
#    - Use PUSH/POP for r0-r7 (16-bit efficient)
#    - Use PUSH.W/POP.W or STMDB/LDMIA for r8-r15
#
# Recommendation: Implement both PUSH.W and STMDB options with configuration

ARM_HIGH_REG_STRATEGIES = {
    "PUSH_W": "Use PUSH.W/POP.W for high registers",
    "STMDB": "Use STMDB sp!/LDMIA sp! for high registers", 
    "MIXED": "Use PUSH for low regs, STMDB for high regs"
}

def analyze_register_strategy():
    """Analyze which strategy works best for different scenarios."""
    
    scenarios = {
        "Cortex-M3": {
            "low_regs_only": "PUSH {r4, r5, r6, r7}",  # 16-bit
            "high_regs_only": "STMDB sp!, {r8, r9, r10}",  # More compatible
            "mixed": "PUSH {r4, r5}; STMDB sp!, {r8, r9}"
        },
        "Cortex-M4": {
            "low_regs_only": "PUSH {r4, r5, r6, r7}",  # 16-bit  
            "high_regs_only": "PUSH.W {r8, r9, r10}",  # Modern syntax
            "mixed": "PUSH {r4, r5}; PUSH.W {r8, r9}"
        },
        "Cortex-M7": {
            "low_regs_only": "PUSH {r4, r5, r6, r7}",  # 16-bit
            "high_regs_only": "PUSH.W {r8, r9, r10}",  # Best performance
            "mixed": "PUSH {r4, r5}; PUSH.W {r8, r9}"
        }
    }
    
    return scenarios

# Assembly format considerations:
# 
# GAS (GNU Assembler):
# - Supports both PUSH.W and STMDB
# - Automatically chooses encoding based on registers
# - .syntax unified for Thumb-2 support
#
# ARMCC (ARM Compiler):
# - Supports both syntaxes
# - PUSH.W preferred for Thumb-2
# - STMDB more explicit about stack operations

if __name__ == "__main__":
    scenarios = analyze_register_strategy()
    for processor, strategies in scenarios.items():
        print(f"{processor}:")
        for scenario, instruction in strategies.items():
            print(f"  {scenario}: {instruction}")
        print()