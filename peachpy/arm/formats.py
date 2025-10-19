# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class AssemblyFormat:
    """Defines different assembly output formats for ARM processors."""
    
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return self.name == other.name
    
    # Assembly format constants
    GAS = None      # GNU Assembler (default)
    ARMCC = None    # ARM Compiler armasm


class HighRegisterStrategy:
    """Defines strategies for handling high registers (r8-r15) in ARMv7-M."""
    
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return self.name == other.name
    
    # High register handling strategies
    PUSH_W = None     # Use PUSH.W/POP.W for high registers (modern, efficient)
    STMDB = None      # Use STMDB sp!/LDMIA sp! for high registers (compatible)
    AUTO = None       # Automatically choose based on target and assembler


# Initialize format constants
AssemblyFormat.GAS = AssemblyFormat("GAS")
AssemblyFormat.ARMCC = AssemblyFormat("ARMCC")

# Initialize strategy constants  
HighRegisterStrategy.PUSH_W = HighRegisterStrategy("PUSH_W")
HighRegisterStrategy.STMDB = HighRegisterStrategy("STMDB")
HighRegisterStrategy.AUTO = HighRegisterStrategy("AUTO")