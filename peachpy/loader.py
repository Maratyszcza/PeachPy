# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

import sys


class Loader:
    def __init__(self, code_size, data_size=0):
        from peachpy.util import is_int
        if not is_int(code_size):
            raise TypeError("code size must be an integer")
        if not is_int(data_size):
            raise TypeError("data size must be an integer")
        if code_size <= 0:
            raise ValueError("code size must be positive")
        if data_size < 0:
            raise ValueError("data size must be non-negative")

        osname = sys.platform.lower()
        if osname == "darwin" or osname.startswith("linux"):
            import peachpy.util
            import mmap
            import ctypes
            self.allocation_granularity = max(mmap.ALLOCATIONGRANULARITY, mmap.PAGESIZE)
            self.code_size = self.allocation_size(code_size)
            self.data_size = self.allocation_size(data_size)

            self._code_allocation = mmap.mmap(-1, self.code_size, mmap.MAP_PRIVATE,
                                              mmap.PROT_READ | mmap.PROT_EXEC | mmap.PROT_WRITE)
            self.code_address = ctypes.addressof(ctypes.c_ubyte.from_buffer(self._code_allocation))

            if self.data_size > 0:
                self._data_allocation = mmap.mmap(-1, self.data_size, mmap.MAP_PRIVATE,
                                              mmap.PROT_READ | mmap.PROT_WRITE)
                self.data_address = ctypes.addressof(ctypes.c_ubyte.from_buffer(self._data_allocation))
            else:
                self._data_allocation = None
                self.data_address = None
        elif osname == "win32":
            raise NotImplementedError("Windows")
        elif osname == "nacl":
            raise NotImplementedError("Native Client")
        else:
            raise ValueError("Unknown host OS: " + osname)

    def allocation_size(self, segment_size):
        import peachpy.util
        return peachpy.util.roundup(segment_size, self.allocation_granularity)

    def copy_code(self, code_segment):
        import ctypes
        ctypes.memmove(self.code_address,
                       ctypes.c_char_p(str(code_segment)),
                       len(code_segment))

    def __del__(self):
        if self._code_allocation is not None:
            self._code_allocation.close()
            self._code_allocation = None
        if self._data_allocation is not None:
            self._data_allocation.close()
            self._data_allocation = None
