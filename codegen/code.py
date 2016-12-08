# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

active_writer = None


class CodeWriter:
    def __init__(self):
        self.lines = list()
        self.indent = 0
        self.previous_writer = None

    def __enter__(self):
        global active_writer
        self.previous_writer = active_writer
        active_writer = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        global active_writer
        active_writer = self.previous_writer
        self.previous_writer = None

    def line(self, line="", indent=0):
        if line != "":
            self.lines.append("    "*(self.indent+int(indent)) + str(line))
        else:
            self.lines.append(line)

    def indent_line(self, line=""):
        self.line(line, indent=1)

    def __str__(self):
        return "\n".join(self.lines)


class CodeBlock:
    def __init__(self, indent=True):
        self.indent = bool(indent)

    def __enter__(self):
        global active_writer
        active_writer.indent += int(self.indent)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        global active_writer
        active_writer.indent -= int(self.indent)
