#include <stddef.h>

void matmul_ref(
	const float a[restrict static 4*4],
	const float b[restrict static 4*4],
	float c[restrict static 4*4])
{
	for (size_t i = 0; i < 4; i++) {
		for (size_t j = 0; j < 4; j++) {
			float s = 0.0f;
			for (size_t k = 0; k < 4; k++) {
				s += a[i*4+k] * b[k*4+j];
			}
			c[i*4+j] = s;
		}
	}
}
