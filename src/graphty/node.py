"""Build a type to represent a function signature."""
import inspect
from collections import namedtuple
from typing import Any
from typing import Callable
from typing import cast
from typing import Mapping
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type

from .context import get_handler
from .typing import Node as Node


class NodeImpl(tuple[Any], Node):
    """Default implementation of call key methods that redirect to the handler."""

    __repr_fmt__: str
    __func__: Callable[..., Any]
    _fields: Tuple[str]

    @classmethod
    def from_call(cls: Any, *args: Any, **kwargs: Any) -> Node:
        """Build a call key by unpacking functionc all arguments."""
        bound = cls.__signature__.bind(*args, **kwargs)
        bound.apply_defaults()
        return cast(Node, cls(*bound.arguments.values()))

    def __repr__(self: Any) -> str:
        """Make a human readable string from the key."""
        return cast(str, self.__repr_fmt__).format(*self[:-1])

    @property
    def parents(self) -> Set[Node]:
        """Return the set of CallKeys that call this key."""
        return get_handler().parents(self)

    @property
    def children(self) -> Set[Node]:
        """Return the set of CallKeys called by this key."""
        return get_handler().children(self)

    @property
    def result(self) -> Any:
        """Return the result of the call, or raise any exception raised."""
        retval = get_handler().retval(self)
        if isinstance(retval, Exception):
            raise retval.args[0]
        return retval

    @property
    def exception(self) -> Optional[Exception]:
        """Return any exception raised by the call, or None if there is none."""
        retval = get_handler().retval(self)
        if isinstance(retval, Exception):
            return cast(Exception, retval.args[0])
        return None

    @property
    def kwargs(self) -> Mapping[str, str]:
        """Return a dictionary of parameter names to their values as strings."""
        return {self._fields[i]: repr(self[i]) for i in range(0, len(self) - 1)}

    @property
    def func(self) -> Callable[..., Any]:
        """Return the function object for this key."""
        return self.__class__.__func__

    @property
    def funcname(self) -> str:
        """Return a string for the fully qualified function name."""
        return (
            self.__func__.__name__
            if "<locals>" in self.__func__.__qualname__
            else self.__func__.__module__ + ":" + self.__func__.__qualname__
        )


def make_node_type(func: Callable[..., Any]) -> Type[Node]:
    """Construct a type representing a functions signature."""
    sig = inspect.signature(func)

    # make a format string that unpacks and names the parameters nicely
    repr_fmt = (
        (
            func.__name__
            if "<locals>" in func.__qualname__
            else func.__module__ + ":" + func.__qualname__
        )
        + "("
        + ", ".join(name + "={!r}" for name in sig.parameters.keys())
        + ")"
    )

    # NOTE we add the func to the tuple since the namedtuple type isn't in the hash
    key_type = type(
        func.__name__,
        (
            Node,
            namedtuple(
                func.__name__,
                tuple(sig.parameters.keys()) + ("func__",),
                defaults=tuple(p.default for p in sig.parameters.values()) + (func,),
                module=func.__module__,
            ),
        ),
        {
            "__repr_fmt__": repr_fmt,
            "__func__": func,
            "__module__": func.__module__,
            "__signature__": sig,
            **NodeImpl.__dict__,
        },
    )

    return key_type


def node(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Node:
    """Construct a key to a function call with the given arguments.

    Parameters:
        func (Callable): Function to construct a node from
        args (Tuple): Positionl arguments for the call
        kwargs (Dict): Keyword arguments for the call

    Returns:
        Node: node representing the function call bound to the supplied arguments

    Example:
        >>> from .wrapper import shift
        >>> n = node(shift(id), 1)
        >>> n.func
        <built-in function id>
        >>> n.obj
        1
    """
    # since we are preserving fundamental python types as far as possible
    # we disable type checking here, __key__ is an implementation detail.
    return func.__key__.from_call(*args, **kwargs)  # type: ignore
