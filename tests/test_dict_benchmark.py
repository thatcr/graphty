import pytest
from collections import defaultdict

pytestmark = pytest.mark.benchmark(group=__name__)


def test_defaultdict(benchmark):
    d = defaultdict(set)

    def insert(d, key, value):
        d[key].add(value)

    benchmark(insert, d, 1, 2)


def test_dict(benchmark):

    d = dict()

    def insert(d, key, value):
        if key not in d:
            d[key] = set()
        d[key].add(value)

    benchmark(insert, d, 1, 2)


def test_setdefault(benchmark):
    d = dict()

    def insert(d, key, value):
        d.setdefault(key, set()).add(value)

    benchmark(insert, d, 1, 2)