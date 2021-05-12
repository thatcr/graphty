"""Simple benchmarks for dictionary performance."""
from collections import defaultdict
from typing import Mapping
from typing import MutableSet

import pytest

from graphty import Handler


pytestmark = pytest.mark.benchmark(group=__name__)


def test_defaultdict(benchmark):  # type: ignore
    """Benchmark performance of initializing a defaultdict."""
    d: Handler = defaultdict(set)

    def insert(d: Mapping[int, MutableSet[int]], key: int, value: int) -> None:
        d[key].add(value)

    benchmark(insert, d, 1, 2)


def test_dict(benchmark):  # type: ignore
    """Benchmark performance of regular dict, testing for the key first."""
    d: Handler = dict()

    def insert(d: Mapping[int, MutableSet[int]], key: int, value: int) -> None:
        if key not in d:
            d[key] = set()
        d[key].add(value)

    benchmark(insert, d, 1, 2)


def test_setdefault(benchmark):  # type: ignore
    """Benchmark using setdefault to fill missing values."""
    d: Handler = dict()

    def insert(d: Mapping[int, MutableSet[int]], key: int, value: int) -> None:
        d.setdefault(key, set()).add(value)

    benchmark(insert, d, 1, 2)
