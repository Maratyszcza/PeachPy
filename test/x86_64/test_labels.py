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


class TestDuplicateLabels(unittest.TestCase):
    """Test that defining an already defined label immediately produces an error"""
    def runTest(self):
        with Function("duplicate_labels", tuple()):
            label1 = Label("lbl")
            label2 = Label("lbl")
            LABEL(label1)
            with self.assertRaises(ValueError):
                LABEL(label2)
            RETURN()


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
        assert equal_codes(code, ref_code), "Unexpected Peach-Py code:\n" + code
