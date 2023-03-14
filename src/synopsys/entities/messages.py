import typing as t
from dataclasses import dataclass

from ..types import DataT, MetadataT, ReplyT, ScopeT
from .events import Event


@dataclass
class Message(t.Generic[ScopeT, DataT, MetadataT, ReplyT]):
    """A message is the container of an event."""

    subject: str
    """Get subject on which message was delivered."""

    scope: ScopeT
    """Get event scope found in message subject."""

    data: DataT
    """Get event data found in message payload."""

    metadata: MetadataT
    """Get event metadata found in message headers."""

    event: Event[ScopeT, DataT, MetadataT, ReplyT]
    """Get event associated with the message."""
