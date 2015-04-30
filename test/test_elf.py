import unittest


class FileHeaderSize(unittest.TestCase):
    def runTest(self):
        from peachpy.formats.elf.file import FileHeader
        import peachpy.arm.abi
        file_header = FileHeader(peachpy.arm.abi.arm_gnueabi)
        file_header_bytes = file_header.as_bytearray
        self.assertEqual(len(file_header_bytes), file_header.file_header_size,
                         "ELF header size must match the value specified in the ELF header")
