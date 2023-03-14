import typing as t
from dataclasses import dataclass

from ..types import DataT, MetadataT, ReplyT, ScopeT
from .events import Event


@dataclass
class Flow:
    """A flow is a definition of some event processing flow."""

    emits: t.List[Event[t.Any, t.Any, t.Any, t.Any]]
    """A list of events which are published within this flow."""

    requests: t.List[Event[t.Any, t.Any, t.Any, t.Any]]
    """A list of service events which are requested within this flow."""


@dataclass
class Subscription(Flow, t.Generic[ScopeT, DataT, MetadataT, ReplyT]):
    """A flow is a definition of a logic step triggered by an event."""

    source: Event[ScopeT, DataT, MetadataT, ReplyT]
    """The event from which delivered messages come from."""

    filter: Event[ScopeT, DataT, MetadataT, ReplyT]
    """The subset of events triggering the flow."""
