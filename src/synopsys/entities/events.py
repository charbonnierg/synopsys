"""An attempt to implement a Python API to define events in a declarative fashion.

In this module, an event is a specification, it is not a message which is delivered accross the network.

In practice, messages are the interfaces holding event data, and message bus are the interfaces delivering messages.

This specification does not make assumptions on the underlying messaging system, but still provides
a type safe API which can be used to publish, request and subscribe to event messages.

The main motivation is to stop writing code at the domain level interacting with subject or addresses,
but instead, target domain events.

Use cases should not care about message bus or messages, but should care about events.

This API has been designed in order to allow integration with messaging system as easy as possible.

See ..interfaces subpackage in order to learn more about integration with messaging systems.
"""
import typing as t

from ..defaults import DEFAULT_CODEC, DEFAULT_SYNTAX
from ..interfaces.codec import CodecBackend
from ..operations.subjects import (
    extract_scope,
    match_subject,
    normalize_subject,
    render_subject,
)
from ..types import DataT, MetadataT, ReplyT, ScopeT
from .syntax import SubjectSyntax


class Event(t.Generic[ScopeT, DataT, MetadataT, ReplyT]):
    """An event is a specification.

    In practice, events are delivered through messages.

    A message is addressed on a subject, with a payload, and some headers.

    - The Scope type defines the typed attributes which can be extracted from the message subject.
    - The Data type defines the typed object which can be extract from the message payload.
    - The MetadataT type defines the typed object which can be extracted from the message headers.
    - The Reply type defines the typed object which can be extracted from the reply message payload.
    """

    name: str
    """The event name."""

    title: str
    """The event title."""

    description: str
    """A short description for the event."""

    subject: str
    """The event subject. Similar to NATS subjects, MQTT topics, or Kafka topics."""

    schema: t.Type[DataT]
    """The event schema, I.E, the schema of the data found in event messages."""

    scope_schema: t.Type[ScopeT]
    """The parameters used to construct a valid event subject."""

    reply_schema: t.Type[ReplyT]
    """The reply schema, I.E, the schema of the data found in event reply."""

    metadata_schema: t.Type[MetadataT]
    """The metadata schema, I.E, the schema of the data found in the headers of event messages."""

    def __init__(
        self,
        name: str,
        subject: str,
        schema: t.Type[DataT],
        scope_schema: t.Type[ScopeT],
        reply_schema: t.Type[ReplyT],
        metadata_schema: t.Type[MetadataT],
        title: t.Optional[str] = None,
        description: t.Optional[str] = None,
        syntax: t.Optional[SubjectSyntax] = None,
        is_filter: bool = False,
    ) -> None:
        """Create a new event using a subjet and a schema."""
        if not name:
            raise ValueError("Name cannot be empty")
        if not subject:
            raise ValueError("Subject cannot be empty")
        self.name = name
        self.subject = subject
        self.scope_schema = scope_schema
        self.schema = schema
        self.reply_schema = reply_schema
        self.metadata_schema = metadata_schema
        self.title = title or name
        self.description = description or ""
        self.syntax = syntax or DEFAULT_SYNTAX
        # Save some attributes to easily match or extract subjects
        self._subject, self._placeholders = normalize_subject(self.subject, self.syntax)
        self._tokens = self._subject.split(self.syntax.match_sep)
        # Do not validate the subject if scope does not have annotations
        if not hasattr(self.scope_schema, "__annotations__"):
            return
        # Ensure that subject is valid according to scope annotations
        if (
            len(self.scope_schema.__annotations__) > len(self._placeholders)
            and not is_filter
        ):
            missing = list(
                set(self.scope_schema.__annotations__).difference(self._placeholders)
            )
            raise ValueError(
                f"Not enough placeholders in subject or unexpected scope variable. Missing in subject: {missing}"
            )
        if len(self.scope_schema.__annotations__) < len(self._placeholders):
            unexpected = list(
                set(self._placeholders).difference(self.scope_schema.__annotations__)
            )
            raise ValueError(
                f"Too many placeholders in subject or missing scope variables. Did not expect in subject: {unexpected}"
            )

    def __repr__(self) -> str:
        return f"Event(name='{self.name}', subject='{self.subject}', schema={getattr(self.schema, '__name__', str(self.schema))})"

    def match_subject(self, subject: str) -> bool:
        """Return True if event matches given subject."""
        return match_subject(self._subject, subject, self.syntax)

    def get_subject(
        self, scope: t.Optional[ScopeT] = None, codec: CodecBackend = DEFAULT_CODEC
    ) -> str:
        """Construct a subject using given scope."""
        return render_subject(
            tokens=self._tokens,
            placeholders=self._placeholders,
            context=codec.encode_headers(scope),
            syntax=self.syntax,
        )

    def extract_scope(
        self, subject: str, codec: CodecBackend = DEFAULT_CODEC
    ) -> ScopeT:
        """Extract placeholders from subject"""
        scope_str = extract_scope(subject, self._placeholders, self.syntax)
        return codec.decode_headers(scope_str, schema=self.scope_schema)
