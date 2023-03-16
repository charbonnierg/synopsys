import typing as t
from dataclasses import dataclass, field
from enum import Enum
from ..types import DataT, MetaT, ReplyT, ScopeT, ReplyMetaT
from .events import Event


class Kind(str, Enum):
    PRODUCER = "PRODUCER"
    SUBSCRIPTION = "SUBSCRIPTION"
    SERVICE = "SERVICE"


@dataclass
class Flow:
    """A flow is a definition of some event processing flow."""

    emits: t.List[Event[t.Any, t.Any, t.Any, t.Any, t.Any]]
    """A list of events which are published within this flow."""

    requests: t.List[Event[t.Any, t.Any, t.Any, t.Any, t.Any]]
    """A list of service events which are requested within this flow."""

    kind: Kind
    """Kind of flow"""


@dataclass
class ProducerFlow(Flow):
    """A flow is a definition of a logic step triggered by an event."""

    kind: t.Literal[Kind.PRODUCER] = Kind.PRODUCER


@dataclass
class SubscriptionFlow(Flow, t.Generic[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT]):
    """A flow is a definition of a logic step triggered by an event."""

    event: Event[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT] = field(init=True)
    """The event from which delivered messages come from."""

    filter: Event[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT] = field(init=True)
    """The subset of events triggering the flow."""

    kind: t.Literal[Kind.SUBSCRIPTION] = field(init=False, default=Kind.SUBSCRIPTION)


@dataclass
class ServiceFlow(Flow, t.Generic[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT]):
    command: Event[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT] = field(init=True)
    """The event from which delivered requests come from."""

    filter: Event[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT] = field(init=True)
    """The subset of events triggering the flow."""

    kind: t.Literal[Kind.SERVICE] = field(init=False, default=Kind.SERVICE)
