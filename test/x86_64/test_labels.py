import unittest
from test import equal_codes
from peachpy.x86_64 import *


class TestInvalidLabelName(unittest.TestCase):
    """Test that Label constructor rejects invalid names"""
    def runTest(self):
        with self.assertRaises(TypeError):
            Label(1)
        with self.assertRaises(ValueError):
            Label("1")
        with self.assertRaises(ValueError):
            Label("lbl:")
        with self.assertRaises(ValueError):
            Label(".lbl")
        with self.assertRaises(ValueError):
            Label("__lbl")


class TestAutonamedLabel(unittest.TestCase):
    """Test that Label name is parsed from Python code whenever possible"""
    def runTest(self):
        with Function("autonamed_label", tuple()) as function:
            skip_nop = Label()
            JMP(skip_nop)
            NOP()
            LABEL(skip_nop)
            RETURN()

        code = function.format()
        ref_code = """
void autonamed_label()
    JMP skip_nop
    NOP
skip_nop:
    RETURN
"""
        assert equal_codes(code, ref_code), "Unexpected PeachPy code:\n" + code


class TestDuplicateNamedLabels(unittest.TestCase):
    """Test that defining an already defined label immediately produces an error"""
    def runTest(self):
        with Function("duplicate_labels", tuple()):
            label1 = Label("lbl")
            label2 = Label("lbl")
            LABEL(label1)
            with self.assertRaises(ValueError):
                LABEL(label2)
            RETURN()


class TestDuplicateAutonamedLabels(unittest.TestCase):
    """Test that conflicts in parsed label names resolve automatically"""
    def runTest(self):
        with Function("duplicate_autonamed_labels", tuple()) as function:
            # One "skip" label
            skip = Label()
            JMP(skip)
            INT(3)
            LABEL(skip)

            # Another "skip" label
            skip = Label()
            JMP(skip)
            NOP()
            LABEL(skip)

            RETURN()

        code = function.format()
        ref_code0 = """
void duplicate_autonamed_labels()
    JMP skip0
    INT 3
skip0:
    JMP skip1
    NOP
skip1:
    RETURN
"""
        ref_code1 = """
void duplicate_autonamed_labels()
    JMP skip1
    INT 3
skip1:
    JMP skip0
    NOP
skip0:
    RETURN
"""
        assert equal_codes(code, ref_code0) or equal_codes(code, ref_code1), \
            "Unexpected PeachPy code:\n" + code


class TestUndefinedLabels(unittest.TestCase):
    """Test that referencing undefined labels produces an error"""
    def runTest(self):
        with self.assertRaises(ValueError):
            with Function("undefined_label", tuple()):
                label = Label("lbl")
                JMP(label)
                RETURN()


class TestDefaultLabels(unittest.TestCase):
    """Test that entry label can be referenced even if it is not defined"""
    def runTest(self):
        with Function("jump_to_entry", tuple()) as function:
            JMP(function.entry)
            RETURN()


class TestUnreferencedLabels(unittest.TestCase):
    """Test that unreferenced labels are removed from the function"""
    def runTest(self):
        with Function("unreferenced_labels", tuple()) as function:
            used_label = Label("used")
            unused_label = Label("unused")
            LABEL(unused_label)
            JMP(used_label)
            LABEL(used_label)
            RETURN()

        code = function.format()
        ref_code = """
void unreferenced_labels()
    JMP used
used:
    RETURN
"""
        assert equal_codes(code, ref_code), "Unexpected PeachPy code:\n" + code
