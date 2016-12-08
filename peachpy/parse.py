# This file is part of PeachPy package and is licensed under the Simplified BSD license.
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
                    match = re.match(assignment_regexp, source_line.strip())
                    if match:
                        return match.group(1)


def parse_with_variable_name(stack_frames, constructor_name):
    """Analyses the provided stack frames and parses Python with expressions like
         with `constructor_name`(...) as variable_name:
    from the caller's call site and returns the name of the variable named in the statement as a string.
    If a with statement is not found, returns None.
    """
    if isinstance(stack_frames, list) and len(stack_frames) > 1:
        parent_stack_frame = stack_frames[1]
        if isinstance(parent_stack_frame, tuple) and len(parent_stack_frame) == 6:
            (_, _, _, _, source_lines, _) = parent_stack_frame
            if isinstance(source_lines, list) and source_lines:
                source_line = source_lines[0]
                if source_line:
                    import re

                    with_regexp = r"with\s+(?:\w+\.)*" + re.escape(constructor_name) + "\(.*\)\s+as\s+([_a-zA-Z]\w*)\s*:"
                    match = re.match(with_regexp, source_line.strip())
                    if match:
                        return match.group(1)
