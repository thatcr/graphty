# format a call tree using rich
"""Rich-pretty formatted output from graphs."""
from typing import Any
from typing import cast
from typing import MutableSet

from rich.console import ConsoleRenderable
from rich.tree import Tree

from .handler import Handler
from .typing import Node


class RichTreeHandler(Handler):
    """Construct a rich Tree from graphty events."""

    def __init__(self) -> None:
        """Create initial Tree branch."""
        self.stack = [Tree("Calls", highlight=True)]
        self.seen: MutableSet[Node] = set()

    def __getitem__(self, key: Node) -> Any:
        """Addsa branch to the tree and highligh duplicated nodes."""
        branch = self.stack[-1].add(
            cast(ConsoleRenderable, key),
            style=("bold" if key not in self.seen else "#7F7F7F"),
        )
        self.stack.append(branch)
        return Ellipsis

    def __setitem__(self, key: Node, value: Any) -> None:
        """Add the current branch to the overall tree, and include value."""
        self.seen.add(key)
        branch = self.stack.pop(-1)
        branch.label = repr(key) + " = " + repr(value)

    def __rich__(self) -> Tree:
        """Print the curent tree to the rich console."""
        return self.stack[0]
