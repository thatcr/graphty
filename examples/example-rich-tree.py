"""Construct a rich tree from a call graph."""
from rich import print

from graphty import Context
from graphty import shift

from graphty.rich import RichTreeHandler


@shift
def f(a, b):
    return a + b


@shift
def g(a, b):
    return f(a, b) + f(b, a)


with Context(RichTreeHandler()) as handler:
    g(1, 2)
print(handler.stack[0])


@shift
def fib(n):
    if n < 2:
        return 1
    return fib(n - 1) + fib(n - 2)


with Context(RichTreeHandler()) as handler:
    fib(7)
print(handler.stack[0])
