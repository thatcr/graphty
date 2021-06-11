"""Test that all modules load quickly."""
from importlib.abc import PathEntryFinder
from pkgutil import ModuleInfo

import pytest
from pytest_benchmark.fixture import BenchmarkFixture  # type: ignore[import]

pytestmark = pytest.mark.benchmark(group=__name__)


def test_loads(module: ModuleInfo) -> None:
    """Verify that the module can be loaded, successfully ignores sys.modules."""
    assert isinstance(module.module_finder, PathEntryFinder)
    loader, _ = module.module_finder.find_loader(module.name)
    if loader is not None:
        loader.load_module(module.name)


def test_benchmark(benchmark: BenchmarkFixture, module: ModuleInfo) -> None:
    """Benchmark the load performance of the module to ensure we don't slow down."""
    assert isinstance(module.module_finder, PathEntryFinder)
    loader, _ = module.module_finder.find_loader(module.name)
    if loader is not None:
        benchmark(loader.load_module, module.name)
