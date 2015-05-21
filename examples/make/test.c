#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>

extern void matmul(
	const float a[restrict static 4*4],
	const float b[restrict static 4*4],
	float c[restrict static 4*4]);

extern void matmul_ref(
	const float a[restrict static 4*4],
	const float b[restrict static 4*4],
	float c[restrict static 4*4]);

int main(int argc, char** argv) {
	const float a[4*4] = {
		1.0f, 1.1f, 1.2f, 1.3f,
		2.0f, 2.1f, 2.2f, 2.3f,
		3.0f, 3.1f, 3.2f, 3.3f,
		4.0f, 4.1f, 4.2f, 4.3f
	};
	const float b[4*4] = {
		1.0f,  2.0f,  3.0f,  4.0f,
		5.0f,  6.0f,  7.0f,  8.0f,
		9.0f,  10.0f, 11.0f, 12.0f,
		13.0f, 14.0f, 15.0f, 16.0f
	};
	float c[4*4], c_ref[4*4];
	matmul(a, b, c);
	matmul_ref(a, b, c_ref);
	for (size_t i = 0; i < 4*4; i++) {
		const float error = fabsf(c[i] - c_ref[i]) / FLT_EPSILON;
		if (error >= 128.0f) {
			fprintf(stderr, "UNIT TEST FAILED\n");
			return 1;
		}
	}
	fprintf(stderr, "UNIT TEST PASSED\n");
	return 0;
}
