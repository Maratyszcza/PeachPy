import unittest


class FileHeaderSize(unittest.TestCase):
    def runTest(self):
        from nervapy.formats.elf.file import FileHeader
        import nervapy.arm.abi
        file_header = FileHeader(nervapy.arm.abi.arm_gnueabi)
        file_header_bytes = file_header.as_bytearray
        self.assertEqual(len(file_header_bytes), file_header.file_header_size,
                         "ELF header size must match the value specified in the ELF header")
