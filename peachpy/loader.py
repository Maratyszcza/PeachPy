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

        import mmap
        self.allocation_granularity = max(mmap.ALLOCATIONGRANULARITY, mmap.PAGESIZE)
        self.code_address = None
        self.code_size = self.allocation_size(code_size)
        self.data_address = None
        self.data_size = self.allocation_size(data_size)

        self._release_memory = None

        osname = sys.platform.lower()
        if osname == "darwin" or osname.startswith("linux"):
            import ctypes

            if osname == "darwin":
                libc = ctypes.cdll.LoadLibrary("libc.dylib")
            else:
                libc = ctypes.cdll.LoadLibrary("libc.so.6")

            # void* mmap(void* addr, size_t len, int prot, int flags, int fd, off_t offset)
            mmap_function = libc.mmap
            mmap_function.restype = ctypes.c_void_p
            mmap_function.argtype = [ctypes.c_void_p, ctypes.c_size_t,
                             ctypes.c_int, ctypes.c_int,
                             ctypes.c_int, ctypes.c_size_t]
            # int munmap(void* addr, size_t len)
            munmap_function = libc.munmap
            munmap_function.restype = ctypes.c_int
            munmap_function.argtype = [ctypes.c_void_p, ctypes.c_size_t]

            def munmap(address, size):
                munmap_result = munmap_function(address, size)
                assert munmap_result == 0

            self._release_memory = lambda address_size: munmap(address_size[0], address_size[1])

            # Allocate code segment
            code_address = mmap_function(None, self.code_size,
                                         mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC,
                                         mmap.MAP_ANON | mmap.MAP_PRIVATE,
                                         -1, 0)
            if code_address == -1:
                raise OSError("Failed to allocate memory for code segment")
            self.code_address = code_address

            if self.data_size > 0:
                # Allocate data segment
                data_address = mmap_function(None, self.data_size,
                                             mmap.PROT_READ | mmap.PROT_WRITE,
                                             mmap.MAP_ANON | mmap.MAP_PRIVATE,
                                             -1, 0)
                if data_address == -1:
                    raise OSError("Failed to allocate memory for data segment")
                self.data_address = data_address
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
                       ctypes.c_char_p(bytes(code_segment)),
                       len(code_segment))

    def __del__(self):
        if self._release_memory is not None:
            if self.code_address is not None:
                self._release_memory((self.code_address, self.code_size))
                self.code_address = None
            if self.data_address is not None:
                self._release_memory((self.data_address, self.data_size))
                self.data_address = None
