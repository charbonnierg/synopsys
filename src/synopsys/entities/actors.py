import typing as t
from dataclasses import dataclass

from ..types import DataT, MetadataT, ReplyT, ScopeT
from .flows import Flow, Subscription
from .messages import Message

if t.TYPE_CHECKING:
    from ..aio.bus import EventBus  # pragma: no cover


@dataclass
class Actor:
    """Base class for actors."""

    name: str
    flow: Flow


@dataclass
class Producer(Actor):
    """An actor which produce events."""

    task_factory: t.Callable[["EventBus"], t.Coroutine[t.Any, t.Any, None]]


@dataclass
class Subscriber(Actor, t.Generic[ScopeT, DataT, MetadataT, ReplyT]):
    """An actor which subscribes to events and may respond."""

    flow: Subscription[ScopeT, DataT, MetadataT, ReplyT]
    handler: t.Callable[
        [Message[ScopeT, DataT, MetadataT, ReplyT]],
        t.Coroutine[t.Any, t.Any, ReplyT],
    ]
    queue: t.Optional[str] = None
