import enum
import sys
from _typeshed import Unused
from collections import deque
from collections.abc import Callable, Generator
from types import TracebackType
from typing import Any, TypeVar
from typing_extensions import Literal, Self

from .events import AbstractEventLoop
from .futures import Future

if sys.version_info >= (3, 10):
    from .mixins import _LoopBoundMixin
else:
    _LoopBoundMixin = object

if sys.version_info >= (3, 11):
    __all__ = ("Lock", "Event", "Condition", "Semaphore", "BoundedSemaphore", "Barrier")
else:
    __all__ = ("Lock", "Event", "Condition", "Semaphore", "BoundedSemaphore")

_T = TypeVar("_T")

if sys.version_info >= (3, 9):
    class _ContextManagerMixin:
        async def __aenter__(self) -> None: ...
        async def __aexit__(
            self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
        ) -> None: ...

else:
    class _ContextManager:
        def __init__(self, lock: Lock | Semaphore) -> None: ...
        def __enter__(self) -> None: ...
        def __exit__(self, *args: Unused) -> None: ...

    class _ContextManagerMixin:
        # Apparently this exists to *prohibit* use as a context manager.
        # def __enter__(self) -> NoReturn: ... see: https://github.com/python/typing/issues/1043
        # def __exit__(self, *args: Any) -> None: ...
        def __iter__(self) -> Generator[Any, None, _ContextManager]: ...
        def __await__(self) -> Generator[Any, None, _ContextManager]: ...
        async def __aenter__(self) -> None: ...
        async def __aexit__(
            self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
        ) -> None: ...

class Lock(_ContextManagerMixin, _LoopBoundMixin):
    if sys.version_info >= (3, 10):
        def __init__(self) -> None: ...
    else:
        def __init__(self, *, loop: AbstractEventLoop | None = None) -> None: ...

    def locked(self) -> bool: ...
    async def acquire(self) -> Literal[True]: ...
    def release(self) -> None: ...

class Event(_LoopBoundMixin):
    if sys.version_info >= (3, 10):
        def __init__(self) -> None: ...
    else:
        def __init__(self, *, loop: AbstractEventLoop | None = None) -> None: ...

    def is_set(self) -> bool: ...
    def set(self) -> None: ...
    def clear(self) -> None: ...
    async def wait(self) -> Literal[True]: ...

class Condition(_ContextManagerMixin, _LoopBoundMixin):
    if sys.version_info >= (3, 10):
        def __init__(self, lock: Lock | None = None) -> None: ...
    else:
        def __init__(self, lock: Lock | None = None, *, loop: AbstractEventLoop | None = None) -> None: ...

    def locked(self) -> bool: ...
    async def acquire(self) -> Literal[True]: ...
    def release(self) -> None: ...
    async def wait(self) -> Literal[True]: ...
    async def wait_for(self, predicate: Callable[[], _T]) -> _T: ...
    def notify(self, n: int = 1) -> None: ...
    def notify_all(self) -> None: ...

class Semaphore(_ContextManagerMixin, _LoopBoundMixin):
    _value: int
    _waiters: deque[Future[Any]]
    if sys.version_info >= (3, 10):
        def __init__(self, value: int = 1) -> None: ...
    else:
        def __init__(self, value: int = 1, *, loop: AbstractEventLoop | None = None) -> None: ...

    def locked(self) -> bool: ...
    async def acquire(self) -> Literal[True]: ...
    def release(self) -> None: ...
    def _wake_up_next(self) -> None: ...

class BoundedSemaphore(Semaphore): ...

if sys.version_info >= (3, 11):
    class _BarrierState(enum.Enum):  # undocumented
        FILLING: str
        DRAINING: str
        RESETTING: str
        BROKEN: str

    class Barrier(_LoopBoundMixin):
        def __init__(self, parties: int) -> None: ...
        async def __aenter__(self) -> Self: ...
        async def __aexit__(self, *args: Unused) -> None: ...
        async def wait(self) -> int: ...
        async def abort(self) -> None: ...
        async def reset(self) -> None: ...
        @property
        def parties(self) -> int: ...
        @property
        def n_waiting(self) -> int: ...
        @property
        def broken(self) -> bool: ...
