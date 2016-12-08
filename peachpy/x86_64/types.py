# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

from peachpy import Type


m64 = Type("__m64", size=8, is_vector=True, header="mmintrin.h")
m128 = Type("__m128", size=16, is_vector=True, header="xmmintrin.h")
m128d = Type("__m128d", size=16, is_vector=True, header="emmintrin.h")
m128i = Type("__m128i", size=16, is_vector=True, header="emmintrin.h")
m256 = Type("__m256", size=32, is_vector=True, header="immintrin.h")
m256d = Type("__m256d", size=32, is_vector=True, header="immintrin.h")
m256i = Type("__m256i", size=32, is_vector=True, header="immintrin.h")
m512 = Type("__m512", size=64, is_vector=True, header="immintrin.h")
m512d = Type("__m512d", size=64, is_vector=True, header="immintrin.h")
m512i = Type("__m512i", size=64, is_vector=True, header="immintrin.h")
mmask8 = Type("__mmask8", size=1, is_mask=True, header="immintrin.h")
mmask16 = Type("__mmask16", size=2, is_mask=True, header="immintrin.h")
