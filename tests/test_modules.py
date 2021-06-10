"""Test that all modules load quickly."""
from pkgutil import ModuleInfo

import pytest

pytestmark = pytest.mark.benchmark(group=__name__)


def test_loads(module: ModuleInfo):
    """Verify that the module can be loaded, successfully ignores sys.modules."""
    loader, _ = module.module_finder.find_loader(module.name)
    module = loader.load_module()


def test_benchmark(benchmark, module: ModuleInfo):
    """Benchmark the load performance of the module to ensure we don't slow down."""
    loader, _ = module.module_finder.find_loader(module.name)
    module = benchmark(loader.load_module)
