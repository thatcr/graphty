"""Test the overhead from wrapping a simple fibonacci function."""
import pytest


pytestmark = pytest.mark.benchmark(group=__name__)


def test_benchmark_fib(benchmark):  # type: ignore
    """Benchmark an unadulterated function, for comparison."""

    def fib(x: int) -> int:
        if x <= 1:
            return 1
        return fib(x - 1) + fib(x - 2)

    benchmark(fib, 9)


def test_benchmark_wrapper_fib(benchmark):  # type: ignore
    """Apply the wrapper with no context."""
    from graphty.wrapper import shift

    @shift
    def fib(x: int) -> int:
        if x <= 1:
            return 1
        return fib(x - 1) + fib(x - 2)

    benchmark(fib, 9)
