# format a call tree using rich
from rich import print
from rich.tree import Tree

from .handler import Handler


class RichTreeHandler(Handler):
    def __init__(self):
        self.stack = [Tree("Calls", highlight=True)]
        self.seen = set()

    def __getitem__(self, key):
        branch = self.stack[-1].add(
            key, style=("bold" if key not in self.seen else "#7F7F7F")
        )
        self.stack.append(branch)
        return Ellipsis

    def __setitem__(self, key, value):
        self.seen.add(key)
        branch = self.stack.pop(-1)
        branch.label = repr(key) + " = " + repr(value)
