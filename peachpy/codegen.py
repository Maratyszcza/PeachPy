# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class CodeGenerator(object):
    def __init__(self, use_tabs=True):
        self.indentationLevel = 0
        self.use_tabs = use_tabs
        self.code = []

    def indent(self):
        self.indentationLevel += 1
        return self

    def dedent(self):
        self.indentationLevel -= 1
        return self

    def add_line(self, string='', indent=None):
        if indent == None:
            indent = self.indentationLevel
        elif indent < 0:
            indent += self.indentationLevel
        if string == '':
            self.code.append(string)
        else:
            if self.use_tabs:
                self.code.append("\t" * indent + string)
            else:
                self.code.append("    " * indent + string)
        return self

    def add_lines(self, lines, indent=None):
        for line in lines:
            self.add_line(line, indent)

    def add_empty_lines(self, count):
        for i in range(count):
            self.add_line()
        return self

    def add_c_comment(self, lines, doxygen=False):
        if isinstance(lines, str) and lines.find("\n") != -1:
            lines = lines.split("\n")
        if isinstance(lines, list) and len(lines) > 1:
            if doxygen:
                self.add_line("/**")
            else:
                self.add_line("/*")
            for line in lines:
                self.add_line(" * " + line)
            self.add_line(" */")
        else:
            line = lines[0] if isinstance(lines, list) else str(lines)
            if doxygen:
                self.add_line("/** " + line + "*/")
            else:
                self.add_line("/* " + line + "*/")

    def add_assembly_comment(self, lines, indent=None):
        for line in lines:
            self.add_line("; " + line, indent)

    def add_fortran90_comment(self, lines, doxygen=False):
        if isinstance(lines, str) and lines.find("\n") != -1:
            lines = lines.split("\n")
        elif isinstance(lines, str):
            lines = [lines]
        for index, line in enumerate(lines):
            if doxygen:
                if index == 0:
                    self.add_line("!> " + line)
                else:
                    self.add_line("!! " + line)
            else:
                self.add_line("! " + line)

    def add_csharp_comment(self, lines, doxygen=False):
        if isinstance(lines, str) and lines.find("\n") != -1:
            lines = lines.split("\n")
        if isinstance(lines, list) and len(lines) > 1:
            if not doxygen:
                self.add_line("/*")
            for line in lines:
                if doxygen:
                    self.add_line("/// " + line)
                else:
                    self.add_line(" * " + line)
            if not doxygen:
                self.add_line(" */")
        else:
            line = lines[0] if isinstance(lines, list) else str(lines)
            if doxygen:
                self.add_line("/// " + line)
            else:
                self.add_line("// " + line)

    def get_code(self):
        return "\n".join(self.code)

