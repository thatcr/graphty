# format a call tree using rich
"""Rich-pretty formatted output from graphs."""
from rich.tree import Tree

from .handler import Handler


class RichTreeHandler(Handler):
    """Construct a rich Tree from graphty events."""

    def __init__(self):
        """Create initial Tree branch."""
        self.stack = [Tree("Calls", highlight=True)]
        self.seen = set()

    def __getitem__(self, key):
        """Addsa branch to the tree and highligh duplicated nodes."""
        branch = self.stack[-1].add(
            key, style=("bold" if key not in self.seen else "#7F7F7F")
        )
        self.stack.append(branch)
        return Ellipsis

    def __setitem__(self, key, value):
        """Add the current branch to the overall tree, and include value."""
        self.seen.add(key)
        branch = self.stack.pop(-1)
        branch.label = repr(key) + " = " + repr(value)

    def __rich__(self) -> Tree:
        """Print the curent tree to the rich console."""
        return self.stack[0]
