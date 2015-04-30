package blas
 
import (
	"testing"
	"math/rand"
)
 
func benchmarkDotProduct(bench *testing.B, size int, useGo bool) {
	x := make([]float32, size)
	y := make([]float32, size)

	r := rand.New(rand.NewSource(42))
	for i := 0; i < size; i++ {
		x[i] = r.Float32()
		y[i] = r.Float32()
	}

	bench.ResetTimer()
	if useGo {
		for i := 0; i < bench.N; i++ {
			var z float32 = 0.0
			for j := 0; j < size; j++ {
				z += x[j] * y[j]
			}
		}
	} else {
		for i := 0; i < bench.N; i++ {
			DotProduct(&x[0], &y[0], uint(size))
		}
	}
}

func BenchmarkDotProduct_L1_PeachPy(bench *testing.B) {
	benchmarkDotProduct(bench, 4096, false)
}

func BenchmarkDotProduct_L2_PeachPy(bench *testing.B) {
	benchmarkDotProduct(bench, 32768, false)
}

func BenchmarkDotProduct_L3_PeachPy(bench *testing.B) {
	benchmarkDotProduct(bench, 262144, false)
}

func BenchmarkDotProduct_L1_Go(bench *testing.B) {
	benchmarkDotProduct(bench, 4096, true)
}

func BenchmarkDotProduct_L2_Go(bench *testing.B) {
	benchmarkDotProduct(bench, 32768, true)
}

func BenchmarkDotProduct_L3_Go(bench *testing.B) {
	benchmarkDotProduct(bench, 262144, true)
}
