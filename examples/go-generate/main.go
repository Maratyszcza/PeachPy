package blas
import "fmt"

func main() {
	x := make([]float32, 2048)
	y := make([]float32, len(x))
	for i := 0; i < len(x); i++ {
		x[i] = 2.0
		y[i] = 3.0
	}

	z := DotProduct(&x[0], &y[0], uint(len(x)))

	fmt.Println("hello world")
	fmt.Println("z =", z)
}

