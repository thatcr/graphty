"""Test simple handler and context combinations."""
from graphty.context import Context
from graphty.context import get_handler
from graphty.node import make_node_type
from graphty.null import NullHandler


def test_null_handler() -> None:
    """Check null handlers does nothing."""
    null = NullHandler()

    key = make_node_type(id).from_call(1)

    assert null.__getitem__(key) is Ellipsis
    null.__setitem__(key, 2)
    assert null.__getitem__(key) is Ellipsis


def test_context_push() -> None:
    """Check we can insert a null handler into the context stack."""
    handler = NullHandler()

    with Context(handler):
        assert get_handler() is handler

    assert get_handler() is not handler
