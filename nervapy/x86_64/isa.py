# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.


class Extension:
    def __init__(self, name, safe_name=None):
        assert isinstance(name, str), "name must be a string"
        self.name = name
        if safe_name is None:
            self.safe_name = self.name
        else:
            self.safe_name = safe_name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __gt__(self, other):
        return other in self.prerequisites

    def __lt__(self, other):
        return self in other.prerequisites

    @property
    def prerequisites(self):
        return {
            "RDTSC": (rdtsc,),
            "RDTSCP": (rdtsc, rdtscp),
            "CPUID": (cpuid,),
            "MMX": (mmx,),
            "MMX+": (mmx, mmx_plus),
            "3dnow!": (mmx, three_d_now, prefetch, prefetchw),
            "3dnow!+": (mmx, three_d_now, three_d_now_plus, prefetch, prefetchw),
            "FEMMS": (mmx, femms),
            "SSE": (mmx, mmx_plus, sse),
            "SSE2": (mmx, mmx_plus, sse, sse2),
            "SSE3": (mmx, mmx_plus, sse, sse2, sse3),
            "SSSE3": (mmx, mmx_plus, sse, sse2, sse3, ssse3),
            "SSE4A": (mmx, mmx_plus, sse, sse2, sse3, sse4a),
            "SSE4.1": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1),
            "SSE4.2": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2),
            "AES": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, aes),
            "PCLMULQDQ": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, pclmulqdq),
            "RDRAND": (rdrand,),
            "RDSEED": (rdrand, rdseed),
            'SHA': (sha,),
            "AVX": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, avx),
            "F16C": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, avx, f16c),
            "AVX2": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, sse4_2, avx, f16c, fma3, avx2),
            "XOP": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, avx, xop),
            "FMA3": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, avx, fma3),
            "FMA4": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, avx, fma4),
            "AVX512F": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, sse4_2, avx, f16c, fma3, avx2, avx512f),
            "AVX512BW": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, sse4_2, avx, f16c, fma3, avx2,
                         avx512f, avx512bw),
            "AVX512DQ": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, sse4_2, avx, f16c, fma3, avx2,
                         avx512f, avx512dq),
            "AVX512VL": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, sse4_2, avx, f16c, fma3, avx2,
                         avx512f, avx512vl),
            "AVX512CD": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, sse4_2, avx, f16c, fma3, avx2,
                         avx512f, avx512cd),
            "AVX512PF": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, sse4_2, avx, f16c, fma3, avx2,
                         avx512f, avx512pf),
            "AVX512ER": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, sse4_2, avx, f16c, fma3, avx2,
                         avx512f, avx512er),
            "AVX512VBMI": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, sse4_2, avx, f16c, fma3, avx2,
                           avx512f, avx512vbmi),
            "AVX512IFMA": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, sse4_2, avx, f16c, fma3, avx2,
                           avx512f, avx512ifma),
            "AVX512VPOPCNTDQ": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, sse4_2, avx, f16c, fma3, avx2,
                           avx512f, avx512vpopcntdq),
            "AVX512_4VNNIW": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, sse4_2, avx, f16c, fma3, avx2,
                              avx512f, avx512_4vnniw),
            "AVX512_4FMAPS": (mmx, mmx_plus, sse, sse2, sse3, ssse3, sse4_1, sse4_2, sse4_2, avx, f16c, fma3, avx2,
                              avx512f, avx512_4fmaps),
            "PREFETCH": (prefetch,),
            "PREFETCHW": (prefetchw,),
            "PREFETCHWT1": (prefetchwt1,),
            "CLFLUSH": (clflush,),
            "CLFLUSHOPT": (clflush, clflushopt,),
            "CLWB": (clwb,),
            "CLZERO": (clzero,),
            "CMOV": (cmov,),
            "POPCNT": (popcnt,),
            "LZCNT": (lzcnt,),
            "MOVBE": (movbe,),
            "BMI": (bmi,),
            "BMI2": (bmi, bmi2),
            "TBM": (tbm,),
            "ADX": (adx,)
        }[self.name]

    @property
    def ancestors(self):
        return {
            "RDTSC": (rdtsc,),
            "RDTSCP": (rdtsc, rdtscp),
            "CPUID": (cpuid,),
            "MMX": (mmx,),
            "MMX+": (mmx, mmx_plus),
            "3dnow!": (mmx, three_d_now),
            "3dnow!+": (mmx, three_d_now, three_d_now_plus),
            "FEMMS": (femms,),
            "SSE": (sse,),
            "SSE2": (sse, sse2),
            "SSE3": (sse, sse2, sse3),
            "SSSE3": (sse, sse2, sse3, ssse3),
            "SSE4A": (sse, sse2, sse3, sse4a),
            "SSE4.1": (sse, sse2, sse3, ssse3, sse4_1),
            "SSE4.2": (sse, sse2, sse3, ssse3, sse4_1, sse4_2),
            "AES": (aes,),
            "PCLMULQDQ": (pclmulqdq,),
            "RDRAND": (rdrand,),
            "RDSEED": (rdrand, rdseed),
            "SHA": (sha,),
            "AVX": (avx,),
            "F16C": (f16c,),
            "AVX2": (avx, avx2),
            "XOP": (xop,),
            "FMA3": (fma3,),
            "FMA4": (fma4,),
            "AVX512F": (avx, fma3, f16c, avx2, avx512f),
            "AVX512BW": (avx, fma3, f16c, avx2, avx512f, avx512bw),
            "AVX512DQ": (avx, fma3, f16c, avx2, avx512f, avx512dq),
            "AVX512VL": (avx, fma3, f16c, avx2, avx512f, avx512vl),
            "AVX512ER": (avx, fma3, f16c, avx2, avx512f, avx512er),
            "AVX512PF": (avx, fma3, f16c, avx2, avx512f, avx512pf),
            "AVX512CD": (avx, fma3, f16c, avx2, avx512f, avx512cd),
            "AVX512VBMI": (avx, fma3, f16c, avx2, avx512f, avx512vbmi),
            "AVX512IFMA": (avx, fma3, f16c, avx2, avx512f, avx512ifma),
            "AVX512VPOPCNTDQ": (avx, f16c, fma3, avx2, avx512f, avx512vpopcntdq),
            "AVX512_4VNNIW": (avx, f16c, fma3, avx2, avx512f, avx512_4vnniw),
            "AVX512_4FMAPS": (avx, f16c, fma3, avx2, avx512f, avx512_4fmaps),
            "PREFETCH": (prefetch,),
            "PREFETCHW": (prefetchw,),
            "PREFETCHWT1": (prefetchwt1,),
            "CLFLUSH": (clflush,),
            "CLFLUSHOPT": (clflush, clflushopt,),
            "CLWB": (clwb,),
            "CLZERO": (clzero,),
            "CMOV": (cmov,),
            "POPCNT": (popcnt,),
            "LZCNT": (lzcnt,),
            "MOVBE": (movbe,),
            "BMI": (bmi,),
            "BMI2": (bmi, bmi2),
            "TBM": (tbm,),
            "ADX": (adx,)
        }[self.name]

    def __add__(self, extension):
        return Extensions(self, extension)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

rdtsc = Extension("RDTSC")
rdtscp = Extension("RDTSCP")
cpuid = Extension("CPUID")
mmx = Extension("MMX")
mmx_plus = Extension("MMX+", safe_name="MMXPlus")
three_d_now = Extension("3dnow!", safe_name="3dnow")
three_d_now_plus = Extension("3dnow!+", safe_name="3dnowPlus")
femms = Extension("FEMMS")
sse = Extension("SSE")
sse2 = Extension("SSE2")
sse3 = Extension("SSE3")
ssse3 = Extension("SSSE3")
sse4a = Extension("SSE4A")
sse4_1 = Extension("SSE4.1", safe_name="SSE4_1")
sse4_2 = Extension("SSE4.2", safe_name="SSE4_2")
aes = Extension("AES")
pclmulqdq = Extension("PCLMULQDQ")
rdrand = Extension("RDRAND")
rdseed = Extension("RDSEED")
sha = Extension("SHA")
avx = Extension("AVX")
avx2 = Extension("AVX2")
avx512f = Extension("AVX512F")
avx512pf = Extension("AVX512PF")
avx512cd = Extension("AVX512CD")
avx512er = Extension("AVX512ER")
avx512dq = Extension("AVX512DQ")
avx512bw = Extension("AVX512BW")
avx512vl = Extension("AVX512VL")
avx512ifma = Extension("AVX512IFMA")
avx512vbmi = Extension("AVX512VBMI")
avx512vpopcntdq = Extension("AVX512VPOPCNTDQ")
avx512_4vnniw = Extension("AVX512_4VNNIW")
avx512_4fmaps = Extension("AVX512_4FMAPS")
prefetch = Extension("PREFETCH")
prefetchw = Extension("PREFETCHW")
prefetchwt1 = Extension("PREFETCHWT1")
clflush = Extension("CLFLUSH")
clflushopt = Extension("CLFLUSHOPT")
clwb = Extension("CLWB")
clzero = Extension("CLZERO")
xop = Extension("XOP")
f16c = Extension("F16C")
fma3 = Extension("FMA3")
fma4 = Extension("FMA4")
cmov = Extension("CMOV")
popcnt = Extension("POPCNT")
lzcnt = Extension("LZCNT")
movbe = Extension("MOVBE")
bmi = Extension("BMI")
bmi2 = Extension("BMI2")
tbm = Extension("TBM")
adx = Extension("ADX")
default = (cpuid, rdtsc, cmov, mmx, mmx_plus, sse, sse2)


class Extensions:
    def __init__(self, *args):
        self.extensions = set()
        for extension in args:
            assert extension is None or isinstance(extension, (Extension, Extensions)), \
                "Each argument must be an Extension or Extensions object"
            if isinstance(extension, Extensions):
                self.extensions.add(extension.extensions)
            elif isinstance(extension, Extension):
                self.extensions.add(extension)

    def minify(self):
        extensions = list(reversed(sorted(self.extensions)))
        for extension in extensions:
            for ancestor in extension.ancestors:
                if ancestor != extension and ancestor in extensions:
                    extensions.remove(ancestor)
        return extensions

    def __add__(self, extension):
        return Extensions(extension, *self.extensions)

    def __sub__(self, extension):
        extensions = set(self.extensions)
        if extension in extensions:
            del extensions[extension]
        else:
            raise KeyError("Extension set does not contain {0}".format(extension))
        return Extensions(*extensions)

    def __str__(self):
        return ", ".join(sorted(map(str, self.minify())))

    def __contains__(self, extension):
        return extension in self.extensions

    def __len__(self):
        return len(self.extensions)

    def __not__(self):
        return not self.extensions

    def __iter__(self):
        return iter(self.extensions)

