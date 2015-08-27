# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


def parse_assigned_variable_name(stack_frames, constructor_name):
    """Analyses the provided stack frames and parses Python assignment expressions like
         some.namespace.variable_name   =   some.module.name.`constructor_name`(...)
    from the caller's call site and returns the name of the variable being assigned as a string.
    If the assignment expression is not found, returns None.
    """
    if isinstance(stack_frames, list) and len(stack_frames) > 1:
        parent_stack_frame = stack_frames[1]
        if isinstance(parent_stack_frame, tuple) and len(parent_stack_frame) == 6:
            (_, _, _, _, source_lines, _) = parent_stack_frame
            if isinstance(source_lines, list) and source_lines:
                source_line = source_lines[0]
                if source_line:
                    import re

                    assignment_regexp = r"(?:\w+\.)*(\w+)\s*=\s*(?:\w+\.)*" + re.escape(constructor_name) + r"\(.*\)"
                    match = re.match(assignment_regexp, source_line)
                    if match:
                        return match.group(1)
