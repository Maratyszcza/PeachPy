# This file is part of Peach-Py package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class ImageWriter:
    def __init__(self, image_format, element):
        if image_format not in {"elf", "mach-o"}:
            raise ValueError("Unsupported image format: " + str(image_format))
        import peachpy.abi
        import peachpy.x86_64.function
        if isinstance(element, peachpy.abi.ABI):
            self.abi = element
            self.functions = list()
        elif isinstance(element, peachpy.x86_64.function.EncodedFunction):
            self.abi = element.abi
            self.functions = [element]
        else:
            raise TypeError("ElfWriter must be initialized with an EncodedFunction or ABI object")

