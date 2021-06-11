"""Construct a simple call graph and test it's accurate."""
from collections import defaultdict
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Mapping
from typing import Set

import pytest

from graphty import Context
from graphty import get_handler
from graphty import node
from graphty.handler import Handler
from graphty.typing import Decorator
from graphty.typing import Node


class GraphHandler(Handler):
    """Store the set of calls that each call makes."""

    stack: List[Node]
    _parents: Dict[Node, Set[Node]]
    _children: Dict[Node, Set[Node]]

    _retvals: Dict[Node, Any]

    def __init__(self) -> None:
        """Create a call stack, and start with an empty call."""
        self.stack = []
        self._parents = defaultdict(set)
        self._children = defaultdict(set)
        self._retvals = dict()

    def __getitem__(self, key: Node) -> Any:
        """Register call with the parent, push onto stack."""
        if self.stack:
            self._children[self.stack[-1]].add(key)
            self._parents[key].add(self.stack[-1])

        if key in self._retvals:
            return self._retvals[key]

        self.stack.append(key)
        return Ellipsis

    def __setitem__(self, key: Node, value: Any) -> None:
        """Pop call from stack."""
        self._retvals[key] = value
        self.stack.pop()

    def bump(self, changes: Mapping[Node, Any]) -> "GraphHandler":
        """Create a new handler with some return values overridden."""
        handler = GraphHandler()

        handler._retvals = self._retvals.copy()

        # duplicate all the children of nodes we haven't bumped
        handler._children = defaultdict(
            set, {k: v.copy() for k, v in self._children.items()}
        )
        handler._parents = defaultdict(
            set, {k: v.copy() for k, v in self._parents.items()}
        )

        deps: List[Node] = list(changes.keys())
        for dep in deps:
            # if dep is not None:
            deps.extend(handler._parents.pop(dep, set()))
            handler._retvals.pop(dep, None)

            # remove the parent link from any children
            for child in handler._children.pop(dep, set()):
                if child in handler._parents:
                    handler._parents[child].remove(dep)

        # override cached values with bumps
        handler._retvals.update(changes)

        return handler

    def parents(self, key: Node) -> Set[Node]:
        """Return parents of a given node."""
        return self._parents[key]

    def children(self, key: Node) -> Set[Node]:
        """Return children of a given node."""
        return self._children[key]

    def retval(self, key: Node) -> Any:
        """Return retval of a given node."""
        return self._retvals[key]


def test_simple_graph(decorator: Decorator) -> None:
    """Verify we construct an accurate call graph."""

    @decorator
    def f(a: int, b: int) -> int:
        return a + b

    @decorator
    def g(a: int, b: int) -> int:
        return f(a, b)

    a = 1
    b = 2

    handler = GraphHandler()
    with Context(handler):
        g(a, b)
        g(a, b)

        assert node(g, a, b) not in handler._parents
        assert node(f, a, b) in handler._parents

        assert node(g, a, b).parents == set()
        assert node(f, a, b).parents == {node(g, a, b)}

        assert node(f, a, b) not in handler._children
        assert node(g, a, b) in handler._children

        assert node(f, a, b).children == set()
        assert node(g, a, b).children == {node(f, a, b)}

        assert node(f, a, b) in handler._retvals
        assert node(g, a, b) in handler._retvals

        assert node(f, a, b).result == a + b
        assert node(g, a, b).result == a + b

        assert node(f, a, b).exception is None
        assert node(g, a, b).exception is None

    # tweak the cache, check it is used
    handler._retvals[node(g, a, b)] = 123
    with Context(handler):
        assert g(a, b) == 123


def test_simple_graph_exception(decorator: Decorator) -> None:
    """Check we can construct a key, and cache in a dict."""
    # store a ref to the thrown exception outside the function
    # so we can check it's the same one returned
    exception = None

    @decorator
    def f(a: int, b: int) -> int:
        nonlocal exception
        # this exception should be cached by the wrapper
        # so we only see it once
        exception = RuntimeError("failure")

        raise exception

    @decorator
    def g(a: int, b: int) -> int:
        return f(a, b)

    a = 1
    b = 2

    handler = GraphHandler()
    with Context(handler):
        try:
            g(a, b)
        except RuntimeError as e:
            assert e is exception

        with pytest.raises(RuntimeError):
            g(a, b)

        # exceptions get cached twice - should this be the case, or do
        # we re-call an throw from source?
        assert type(handler.retval(node(f, a, b))) is Exception
        assert type(handler.retval(node(g, a, b))) is Exception
        assert node(f, a, b).exception is exception
        assert node(g, a, b).exception is exception

        with pytest.raises(RuntimeError):
            node(f, a, b).result

        with pytest.raises(RuntimeError):
            node(g, a, b).result

        assert node(g, a, b).parents == set()
        assert node(f, a, b).parents == {node(g, a, b)}


def test_simple_graph_bump(print: Callable[..., Any], decorator: Decorator) -> None:
    """Try bumping some functions and check that the graph is consistent."""

    @decorator
    def f(x: int) -> int:
        return x

    @decorator
    def g(x: int, y: int) -> int:
        return f(x) + f(y)

    handler = GraphHandler()
    with Context(handler):
        assert g(1, 2) == 3
        assert g(1, 3) == 4

    print(handler.__dict__)

    bumped = handler.bump({node(f, 1): 10})
    with Context(bumped):
        print(bumped.__dict__)

        assert get_handler() is bumped

        assert bumped._retvals == {node(f, 2): 2, node(f, 3): 3, node(f, 1): 10}

        assert node(f, 2).parents == set()
        assert node(f, 3).parents == set()

        # no nodes have any children left - we evicted them all
        assert not bumped._children
        assert node(f, 2).result == 2
        assert node(f, 3).result == 3
        assert node(f, 1).result == 10

        assert g(1, 2) == 12
