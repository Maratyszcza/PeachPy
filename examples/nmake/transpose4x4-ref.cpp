#include <algorithm>
#include <cstddef>

void transpose4x4_ref(float matrix[4 * 4])
{
	for (size_t i = 0; i < 4; i++) {
		for (size_t j = 0; j < i; j++) {
			std::swap(matrix[i*4+j], matrix[j*4+i]);
		}
	}
}
