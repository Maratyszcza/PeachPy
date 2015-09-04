#include <cstdlib>
#include <iostream>

extern "C" void transpose4x4_opt(float matrix[4 * 4]);

extern void transpose4x4_ref(float matrix[4 * 4]);

int main(int argc, char** argv) {
	float matrix_ref[4 * 4], matrix_opt[4 * 4];
	for (size_t i = 0; i < 4 * 4; i++) {
		matrix_ref[i] = i;
		matrix_opt[i] = i;
	}
	transpose4x4_ref(matrix_ref);
	transpose4x4_opt(matrix_opt);
	for (size_t i = 0; i < 4 * 4; i++) {
		if (matrix_ref[i] != matrix_opt[i]) {
			std::cerr << "UNIT TEST FAILED" << std::endl;
			return 1;
		}
	}
	std::cerr << "UNIT TEST PASSED" << std::endl;
	return 0;
}
