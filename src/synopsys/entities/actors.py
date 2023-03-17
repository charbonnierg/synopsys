import typing as t
from dataclasses import dataclass

from ..types import DataT, MetaT, ReplyMetaT, ReplyT, ScopeT
from .flows import ProducerFlow, ServiceFlow, SubscriptionFlow
from .messages import Message, Reply

if t.TYPE_CHECKING:
    from ..aio.bus import EventBus  # pragma: no cover


@dataclass
class Actor:
    """Base class for actors."""


@dataclass
class Producer(Actor):
    """An actor which produce events."""

    flow: ProducerFlow

    task_factory: t.Callable[["EventBus"], t.Coroutine[t.Any, t.Any, None]]


@dataclass
class Subscriber(Actor, t.Generic[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT]):
    """An actor which subscribes to events and may respond."""

    flow: SubscriptionFlow[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT]

    handler: t.Callable[
        [Message[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT]],
        t.Coroutine[t.Any, t.Any, None],
    ]
    """A subscriber handler must return None"""

    queue: t.Optional[str] = None
    """A subscriber may belong to a queue"""


@dataclass
class Service(Actor, t.Generic[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT]):
    """An actor which subscribes and replies to events."""

    flow: ServiceFlow[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT]

    handler: t.Callable[
        [Message[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT]],
        t.Coroutine[t.Any, t.Any, Reply[ReplyT, ReplyMetaT]],
    ]
    """A service must return a reply according to flow command definition."""

    queue: t.Optional[str] = None
    """A service may belong to a queue."""
