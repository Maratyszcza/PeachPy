# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

import six


class RegisterAllocator:
    def __init__(self):
        # Map from virtual register id to internal id of conflicting registers (both virtual and physical)
        self.conflicting_registers = dict()
        # Map from virtual register id to physical register id
        self.register_allocations = dict()
        # Map from virtual register id to a list of available physical ids for the allocation
        self.allocation_options = dict()

    def add_conflicts(self, virtual_id, conflict_internal_ids):
        self.conflicting_registers.setdefault(virtual_id, set())
        self.conflicting_registers[virtual_id].update(conflict_internal_ids)
        for conflict_internal_id in conflict_internal_ids:
            if conflict_internal_id < 0:
                conflict_virtual_id = -conflict_internal_id
                self.conflicting_registers.setdefault(conflict_virtual_id, set())
                self.conflicting_registers[conflict_virtual_id].add(-virtual_id)

    def set_allocation_options(self, abi, register_kind):
        physical_ids = \
            [reg.physical_id for reg in abi.volatile_registers if reg.kind == register_kind] + \
            [reg.physical_id for reg in abi.argument_registers if reg.kind == register_kind][::-1] + \
            [reg.physical_id for reg in abi.callee_save_registers if reg.kind == register_kind]
        for reg in abi.restricted_registers:
            if reg.kind == register_kind and reg.physical_id in physical_ids:
                physical_ids.remove(reg.physical_id)
        # TODO: account the pre-allocated registers in allocation options
        for virtual_id, conflict_internal_ids in six.iteritems(self.conflicting_registers):
            self.allocation_options[virtual_id] = \
                [physical_id for physical_id in physical_ids if physical_id not in conflict_internal_ids]

    def _bind_register(self, virtual_id, physical_id):
        assert virtual_id > 0
        assert physical_id >= 0
        # TODO: handle situation before allocation options are initialized
        for conflict_internal_id in self.conflicting_registers[virtual_id]:
            if conflict_internal_id < 0:
                conflict_virtual_id = -conflict_internal_id
                try:
                    self.allocation_options[conflict_virtual_id].remove(physical_id)
                except ValueError:
                    pass
        self.allocation_options[virtual_id] = [physical_id]
        self.register_allocations[virtual_id] = physical_id

    def try_allocate_register(self, virtual_id, physical_id):
        assert virtual_id > 0
        if physical_id in self.allocation_options[virtual_id]:
            self._bind_register(virtual_id, physical_id)
            return True
        else:
            return False

    def _allocation_alternatives(self, virtual_id, physical_id):
        return sum(1 for reg in self.allocation_options[virtual_id] if reg != physical_id)

    def _min_conflict_allocation_alternatives(self, virtual_id, physical_id):
        try:
            return min(self._allocation_alternatives(-conflict_internal_id, physical_id)
                   for conflict_internal_id in self.conflicting_registers[virtual_id]
                   if conflict_internal_id < 0)
        except ValueError:
            return 0

    def allocate_registers(self):
        unallocated_registers = [reg for reg in six.iterkeys(self.allocation_options)
                                 if reg not in self.register_allocations]

        while unallocated_registers:
            # Choose the virtual register for which there are the least allocation options
            virtual_id = min(unallocated_registers, key=lambda reg: len(self.allocation_options[reg]))
            if not self.allocation_options[virtual_id]:
                raise Exception("No physical registers for virtual register %d" % virtual_id)
            if self.conflicting_registers[virtual_id]:
                # Choose the physical register for which there are most alternatives
                physical_id = max(self.allocation_options[virtual_id],
                                  key=lambda reg: self._min_conflict_allocation_alternatives(virtual_id, reg))
            else:
                # Choose the first available physical register
                physical_id = self.allocation_options[virtual_id].pop()
            self._bind_register(virtual_id, physical_id)
            unallocated_registers.remove(virtual_id)
