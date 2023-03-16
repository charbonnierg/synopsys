import typing as t
from dataclasses import dataclass

from ..types import DataT, MetaT, ReplyT, ScopeT, ReplyMetaT
from .events import Event


@dataclass
class Message(t.Generic[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT]):
    """A message is the container of an event."""

    subject: str
    """Get subject on which message was delivered."""

    scope: ScopeT
    """Get event scope found in message subject."""

    data: DataT
    """Get event data found in message payload."""

    metadata: MetaT
    """Get event metadata found in message headers."""

    event: Event[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT]
    """Get event associated with the message."""


@dataclass
class Reply(t.Generic[DataT, MetaT]):
    """A reply is a message without scope. A reply cannot have a reply schema or a reply metadata schema."""

    data: DataT
    """Event data found reply message payload."""

    metadata: MetaT
    """Event metadata reply message headers."""


@dataclass
class SimpleReply(Reply[DataT, None]):
    data: DataT
    """Event data found reply message payload."""

    metadata: None = None
    """A simple reply does not have metadata."""
