# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

active_stream = None


class InstructionStream(object):
    def __init__(self):
        self.instructions = list()
        self.previous_stream = None

    def __enter__(self):
        global active_stream
        self.previous_stream = active_stream
        active_stream = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        global active_stream
        active_stream = self.previous_stream
        self.previous_stream = None

    def __iter__(self):
        return iter(self.instructions)

    def __len__(self):
        return len(self.instructions)

    def __getitem__(self, i):
        try:
            return self.instructions[i]
        except IndexError:
            return None

    def add_instruction(self, instruction):
        if instruction is not None:
            self.instructions.append(instruction)

    def issue(self, count=1):
        for i in range(count):
            if self.instructions:
                active_stream.add_instruction(self.instructions.pop(0))


class NullStream:
    def __init__(self):
        self.previous_stream = None

    def __enter__(self):
        global active_stream
        self.previous_stream = active_stream
        active_stream = None
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        global active_stream
        active_stream = self.previous_stream
        self.previous_stream = None
