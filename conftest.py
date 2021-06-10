"""Setup global fixture to parametrize a test by module."""
import pkgutil

from _pytest.python import Metafunc


def pytest_generate_tests(metafunc: Metafunc) -> None:
    """Expand module fixture to a full list of modules in this distribution."""
    if "module" in metafunc.fixturenames:
        modules = list(pkgutil.walk_packages(path=["src", "tests"]))
        metafunc.parametrize(
            "module",
            modules,
            ids=[m.name for m in modules],
        )
