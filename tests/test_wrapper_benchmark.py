"""Test the overhead from wrapping a simple fibonacci function."""


def test_benchmark_fib(benchmark):
    """Benchmark an unadulterated function, for comparison."""

    def fib(x):
        if x <= 1:
            return 1
        return fib(x - 1) + fib(x - 2)

    benchmark(fib, 9)


def test_benchmark_wrapper_fib(benchmark):
    """Apply the wrapper with no context."""
    from snake.shifter.wrapper import shift

    @shift
    def fib(x):
        if x <= 1:
            return 1
        return fib(x - 1) + fib(x - 2)

    benchmark(fib, 9)
