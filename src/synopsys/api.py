import typing as t

from .aio.bus import EventBus
from .defaults import DEFAULT_CODEC
from .entities.events import Event
from .entities.flows import Flow, ProducerFlow, ServiceFlow, SubscriptionFlow
from .entities.syntax import SubjectSyntax
from .interfaces.codec import CodecBackend
from .interfaces.pubsub import PubSubBackend
from .operations.subjects import render_subject
from .types import NULL, DataT, MetaT, ReplyMetaT, ReplyT, ScopeT

__all__ = ["create_event"]

"""This is not funny at all, but we need to provide 32 overload implementations 😭😭"""


# 1. []
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: None = None,
    reply_schema: None = None,
    metadata_schema: None = None,
    reply_metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, None, None, None, None]:
    """Create a minimal event without scope, metadata or reply event"""
    ...  # pragma: no cover


# 2. ["schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: None = None,
    reply_schema: None = None,
    metadata_schema: None = None,
    reply_metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, DataT, None, None, None]:
    """Create an event with a schema"""
    ...  # pragma: no cover


# 3. ["scope_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: t.Type[ScopeT],
    reply_schema: None = None,
    metadata_schema: None = None,
    reply_metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, None, None, None, None]:
    """Create an event with a scope schema"""
    ...  # pragma: no cover


# 4. ["reply_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: None = None,
    reply_schema: t.Type[ReplyT],
    metadata_schema: None = None,
    reply_metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, None, None, ReplyT, None]:
    """Create an event with a reply schema"""
    ...  # pragma: no cover


# 5. ["metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: None = None,
    reply_schema: None = None,
    metadata_schema: t.Type[MetaT],
    reply_metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, None, MetaT, None, None]:
    """Create an event with a metadata schema"""
    ...  # pragma: no cover


# 6. ["reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: None = None,
    reply_schema: None = None,
    metadata_schema: None = None,
    reply_metadata_schema: t.Type[ReplyMetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, None, None, None, ReplyMetaT]:
    """Create an event with a reply metadata schema"""
    ...  # pragma: no cover


# 7. ["schema", "scope_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: t.Type[ScopeT],
    reply_schema: None = None,
    metadata_schema: None = None,
    reply_metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, DataT, None, None, None]:
    """Create an event with a schema and a scope schema"""
    ...  # pragma: no cover


# 8. ["schema", "reply_schema""]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    reply_schema: t.Type[ReplyT],
    scope_schema: None = None,
    metadata_schema: None = None,
    reply_metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, DataT, None, ReplyT, None]:
    """Create an event with a schema and a reply schema"""
    ...  # pragma: no cover


# 9. ["schema", "metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: None = None,
    reply_schema: None = None,
    metadata_schema: t.Type[MetaT],
    reply_metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, DataT, MetaT, None, None]:
    """Create an event with a schema and a metadata schema"""
    ...  # pragma: no cover


# 9. ["schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: None = None,
    reply_schema: None = None,
    metadata_schema: None = None,
    reply_metadata_schema: t.Type[ReplyMetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, DataT, None, None, ReplyMetaT]:
    """Create an event with a schema and a reply metadata schema"""
    ...  # pragma: no cover


# 10. ["scope_schema", "reply_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: t.Type[ScopeT],
    reply_schema: t.Type[ReplyT],
    metadata_schema: None = None,
    reply_metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, None, None, ReplyT, None]:
    """Create an event with a reply schema and a scope schema"""
    ...  # pragma: no cover


# ["metadata_schema", "reply_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: None = None,
    reply_schema: t.Type[ReplyT],
    metadata_schema: t.Type[MetaT],
    reply_metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, None, MetaT, ReplyT, None]:
    """Create an event with a reply schema and a metadata schema"""
    ...  # pragma: no cover


# ["metadata_schema", "scope_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: t.Type[ScopeT],
    reply_schema: None = None,
    metadata_schema: t.Type[MetaT],
    reply_metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, None, MetaT, None, None]:
    """Create an event with a metadata schema and a scope schema"""
    ...  # pragma: no cover


# ["metadata_schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: None = None,
    reply_schema: None = None,
    metadata_schema: t.Type[MetaT],
    reply_metadata_schema: t.Type[ReplyMetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, None, MetaT, None, ReplyMetaT]:
    """Create an event with a metadata schema and a scope schema"""
    ...  # pragma: no cover


# ["scope_schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: t.Type[ScopeT],
    reply_schema: None = None,
    metadata_schema: None = None,
    reply_metadata_schema: t.Type[ReplyMetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, None, None, None, ReplyMetaT]:
    """Create an event with a metadata schema and a scope schema"""
    ...  # pragma: no cover


# ["reply_schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: None = None,
    reply_schema: t.Type[ReplyT],
    metadata_schema: None = None,
    reply_metadata_schema: t.Type[ReplyMetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, None, None, ReplyT, ReplyMetaT]:
    """Create an event with a reply schema and a reply metadata schema"""
    ...  # pragma: no cover


# ["schema", "metadata_schema", "scope_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: t.Type[ScopeT],
    reply_schema: None = None,
    metadata_schema: t.Type[MetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, DataT, MetaT, None, None]:
    """Create an event with a schema, a metadata schema and a scope schema"""
    ...  # pragma: no cover


# ["schema", "metadata_schema", "reply_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: None = None,
    reply_schema: t.Type[ReplyT],
    metadata_schema: t.Type[MetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, DataT, MetaT, ReplyT, None]:
    """Create an event with a schema, a metadata schema and a reply schema"""
    ...  # pragma: no cover


# ["metadata_schema", "scope_schema", "reply_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: t.Type[ScopeT],
    reply_schema: t.Type[ReplyT],
    metadata_schema: t.Type[MetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, None, MetaT, ReplyT, None]:
    """Create an event with a reply schema, a metadata schema and a scope schema"""
    ...  # pragma: no cover


# ["schema", "scope_schema", "reply_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: t.Type[ScopeT],
    reply_schema: t.Type[ReplyT],
    metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, DataT, None, ReplyT, None]:
    """Create an event with a schema, a reply schema, and a scope schema"""
    ...  # pragma: no cover


# ["schema", "metadata_schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: None = None,
    reply_schema: None = None,
    reply_metadata_schema: t.Type[ReplyMetaT],
    metadata_schema: t.Type[MetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, DataT, MetaT, None, ReplyMetaT]:
    """Create an event with a schema, a reply schema, and a reply metadata schema"""
    ...  # pragma: no cover


# ["schema", "scope_schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: t.Type[ScopeT],
    reply_schema: None = None,
    reply_metadata_schema: t.Type[ReplyMetaT],
    metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, DataT, None, None, ReplyMetaT]:
    """Create an event with a schema, a scope schema, and a reply metadata schema"""
    ...  # pragma: no cover


# ["schema", "reply_schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: None = None,
    reply_schema: t.Type[ReplyT],
    reply_metadata_schema: t.Type[ReplyMetaT],
    metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, DataT, None, ReplyT, ReplyMetaT]:
    """Create an event with a schema, a reply schema, and a reply metadata schema"""
    ...  # pragma: no cover


# ["metadata_schema", "scope_schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: t.Type[ScopeT],
    reply_schema: None = None,
    reply_metadata_schema: t.Type[ReplyMetaT],
    metadata_schema: t.Type[MetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, None, MetaT, None, ReplyMetaT]:
    """Create an event with a scope schema, a metadata schema, and a reply metadata schema"""
    ...  # pragma: no cover


# ["metadata_schema", "reply_schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: None = None,
    reply_schema: t.Type[ReplyT],
    reply_metadata_schema: t.Type[ReplyMetaT],
    metadata_schema: t.Type[MetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, None, MetaT, ReplyT, ReplyMetaT]:
    """Create an event with a metadata schema, a reply schema, and a reply metadata schema"""
    ...  # pragma: no cover


# ["scope_schema", "reply_schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: t.Type[ScopeT],
    reply_schema: t.Type[ReplyT],
    reply_metadata_schema: t.Type[ReplyMetaT],
    metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, None, None, ReplyT, ReplyMetaT]:
    """Create an event with a scope schema, a reply schema, and a reply metadata schema"""
    ...  # pragma: no cover


# ["schema", "metadata_schema", "scope_schema", "reply_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: t.Type[ScopeT],
    reply_schema: t.Type[ReplyT],
    metadata_schema: t.Type[MetaT],
    reply_metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, DataT, MetaT, ReplyT, None]:
    """Create an event with a schema, a reply schema, a scope schema and a metadata schema"""
    ...  # pragma: no cover


# ["schema", "metadata_schema", "scope_schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: t.Type[ScopeT],
    reply_schema: None = None,
    reply_metadata_schema: t.Type[ReplyMetaT],
    metadata_schema: t.Type[MetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, DataT, MetaT, None, ReplyMetaT]:
    """Create an event with a schema, a metadata schema, a scope schema and a reply schema"""
    ...  # pragma: no cover


# ["schema", "metadata_schema", "reply_schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: None = None,
    reply_schema: t.Type[ReplyT],
    reply_metadata_schema: t.Type[ReplyMetaT],
    metadata_schema: t.Type[MetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, DataT, MetaT, ReplyT, ReplyMetaT]:
    """Create an event with a schema, a metadata schema, a scope schema and a reply metadata schema"""
    ...  # pragma: no cover


# ["schema", "scope_schema", "reply_schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: t.Type[ScopeT],
    reply_schema: t.Type[ReplyT],
    reply_metadata_schema: t.Type[ReplyMetaT],
    metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, DataT, None, ReplyT, ReplyMetaT]:
    """Create an event with a schema, a metadata schema, a scope schema and a reply metadata schema"""
    ...  # pragma: no cover


# ["metadata_schema", "scope_schema", "reply_schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: t.Type[ScopeT],
    reply_schema: t.Type[ReplyT],
    reply_metadata_schema: t.Type[ReplyMetaT],
    metadata_schema: t.Type[MetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, None, MetaT, ReplyT, ReplyMetaT]:
    """Create an event with a schema, a metadata schema, a scope schema and a reply metadata schema"""
    ...  # pragma: no cover


# ["schema", "metadata_schema", "scope_schema", "reply_schema", "reply_metadata_schema"]
@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: t.Type[ScopeT],
    reply_schema: t.Type[ReplyT],
    reply_metadata_schema: t.Type[ReplyMetaT],
    metadata_schema: t.Type[MetaT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT]:
    """Create an event with a schema, a metadata schema, a scope schema and a reply metadata schema"""
    ...  # pragma: no cover


def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Any = NULL,
    scope_schema: t.Any = NULL,
    reply_schema: t.Any = NULL,
    metadata_schema: t.Any = NULL,
    reply_metadata_schema: t.Any = NULL,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[t.Any, t.Any, t.Any, t.Any, t.Any]:
    if schema is None:
        schema = type(None)
    if reply_schema is None:
        reply_schema = type(None)
    if metadata_schema is None:
        metadata_schema = type(None)
    if scope_schema is None:
        scope_schema = type(None)
    if reply_metadata_schema is None:
        reply_metadata_schema = type(None)
    # Handle events
    return Event(
        name=name,
        subject=subject,
        schema=schema,
        scope_schema=scope_schema,
        reply_schema=reply_schema,
        metadata_schema=metadata_schema,
        reply_metadata_schema=reply_metadata_schema,
        title=title,
        description=description,
        syntax=syntax,
    )


@t.overload
def create_flow(
    name: str,
    *,
    event: Event[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT],
    emits: t.Optional[t.List[Event[t.Any, t.Any, t.Any, t.Any, t.Any]]] = None,
    requests: t.Optional[t.List[Event[t.Any, t.Any, t.Any, t.Any, t.Any]]] = None,
    scope: t.Optional[t.Dict[str, str]] = None,
) -> SubscriptionFlow[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT]:
    ...  # pragma: no cover


@t.overload
def create_flow(
    name: str,
    *,
    command: Event[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT],
    emits: t.Optional[t.List[Event[t.Any, t.Any, t.Any, t.Any, t.Any]]] = None,
    requests: t.Optional[t.List[Event[t.Any, t.Any, t.Any, t.Any, t.Any]]] = None,
    scope: t.Optional[t.Dict[str, str]] = None,
) -> ServiceFlow[ScopeT, DataT, MetaT, ReplyT, ReplyMetaT]:
    ...  # pragma: no cover


@t.overload
def create_flow(
    name: str,
    *,
    event: None = None,
    command: None = None,
    emits: t.Optional[t.List[Event[t.Any, t.Any, t.Any, t.Any, t.Any]]] = None,
    requests: t.Optional[t.List[Event[t.Any, t.Any, t.Any, t.Any, t.Any]]] = None,
    scope: None = None,
) -> ProducerFlow:
    ...  # pragma: no cover


def create_flow(
    name: str,
    *,
    event: t.Optional[Event[t.Any, t.Any, t.Any, t.Any, t.Any]] = None,
    command: t.Optional[Event[t.Any, t.Any, t.Any, t.Any, t.Any]] = None,
    emits: t.Optional[t.List[Event[t.Any, t.Any, t.Any, t.Any, t.Any]]] = None,
    requests: t.Optional[t.List[Event[t.Any, t.Any, t.Any, t.Any, t.Any]]] = None,
    scope: t.Optional[t.Dict[str, str]] = None,
) -> Flow:
    """Create a new flow for an event."""
    emits = emits or []
    requests = requests or []
    if event and command:
        raise ValueError("A single event or command may be provided, but not both")
    if scope:
        if event and command:
            raise ValueError(
                "scope can only be used when an event or a command is provided"
            )
        if event:
            source = event
        elif command:
            source = command
        else:
            raise ValueError(
                "Either command or source must be provided when scope is used"
            )
        source_filter = Event(
            source.name,
            subject=render_subject(
                tokens=source._tokens,
                placeholders=source._placeholders,
                context=scope,
                syntax=source.syntax,
                is_filter=True,
            ),
            schema=source.schema,
            scope_schema=source.scope_schema,
            reply_schema=source.reply_schema,
            metadata_schema=source.metadata_schema,
            reply_metadata_schema=source.reply_metadata_schema,
            title=source.title,
            description=source.description,
            syntax=source.syntax,
            is_filter=True,
        )
        # Return a subscription flow for events
        if event:
            return SubscriptionFlow(
                name=name,
                emits=emits,
                requests=requests,
                event=source,
                filter=source_filter,
            )
        # Return a service flow for commands
        return ServiceFlow(
            name=name,
            emits=emits,
            requests=requests,
            command=source,
            filter=source_filter,
        )
    elif event:
        return SubscriptionFlow(
            name=name, emits=emits, requests=requests, event=event, filter=event
        )
    elif command:
        return ServiceFlow(
            name=name,
            emits=emits,
            requests=requests,
            command=command,
            filter=command,
        )
    return ProducerFlow(name=name, emits=emits, requests=requests)


def create_bus(
    pubsub: PubSubBackend,
    flow: t.Optional[Flow] = None,
    *,
    codec: CodecBackend = DEFAULT_CODEC,
) -> EventBus:
    return EventBus(flow=flow, pubsub=pubsub, codec=codec)


def __test_annotations_create_event() -> None:  # pragma: no cover
    """This function can be considered as a typechecking test.

    When running mypy, it will evaluate all the assertions in the function
    body.
    A runtime, no error is raised so there is no benefit in actually running the
    function (for example using pytest).
    Moreover, untyped definitions are allowed in tests modules, and mypy does not
    check assertions on untyped definitions. That's why this function is located in
    this module and not in the tests module.
    """
    from typing_extensions import assert_type

    # No schema: []
    evt = create_event("test", "test")
    assert_type(evt, Event[None, None, None, None, None])

    # ["schema"] (null)
    evt2 = create_event("test", "test", schema=None)
    assert_type(evt2, Event[None, None, None, None, None])

    # ["schema"]
    evt3 = create_event("test", "test", schema=int)
    assert_type(evt3, Event[None, int, None, None, None])

    # ["scope_schema"] (null)
    evt4 = create_event("test", "test", scope_schema=None)
    assert_type(evt4, Event[None, None, None, None, None])

    # ["scope_schema"]
    evt5 = create_event("test", "test", scope_schema=t.Dict[str, str])
    assert_type(evt5, Event[t.Dict[str, str], None, None, None, None])

    # ["reply_schema"] (null)
    evt6 = create_event("test", "test", reply_schema=int)
    assert_type(evt6, Event[None, None, None, int, None])

    # ["reply_schema"]
    evt7 = create_event("test", "test", reply_schema=None)
    assert_type(evt7, Event[None, None, None, None, None])

    # ["metadata_schema"] (null)
    evt8 = create_event("test", "test", metadata_schema=None)
    assert_type(evt8, Event[None, None, None, None, None])

    # ["metadata_schema"]
    evt9 = create_event("test", "test", metadata_schema=t.Dict[str, str])
    assert_type(evt9, Event[None, None, t.Dict[str, str], None, None])

    # ["reply_metadata_schema"] (null)
    evt10 = create_event("test", "test", reply_metadata_schema=None)
    assert_type(evt10, Event[None, None, None, None, None])

    # ["reply_metadata_schema"]
    evt11 = create_event("test", "test", reply_metadata_schema=t.Dict[str, str])
    assert_type(evt11, Event[None, None, None, None, t.Dict[str, str]])

    # ["schema", "scope_schema"]
    evt12 = create_event("test", "test", schema=int, scope_schema=t.Dict[str, str])
    assert_type(evt12, Event[t.Dict[str, str], int, None, None, None])

    # ["schema", "reply_schema"]
    evt13 = create_event("test", "test", schema=int, reply_schema=int)
    assert_type(evt13, Event[None, int, None, int, None])

    # ["schema", "metadata_schema"]
    evt14 = create_event("test", "test", schema=int, metadata_schema=t.Dict[str, str])
    assert_type(evt14, Event[None, int, t.Dict[str, str], None, None])

    # ["scope_schema", "metadata_schema"]
    evt15 = create_event(
        "test", "test", scope_schema=t.Dict[str, str], metadata_schema=t.Dict[str, str]
    )
    assert_type(evt15, Event[t.Dict[str, str], None, t.Dict[str, str], None, None])

    # ["scope_schema," "reply_schema"]
    evt16 = create_event(
        "test", "test", reply_schema=int, scope_schema=t.Dict[str, str]
    )
    assert_type(evt16, Event[t.Dict[str, str], None, None, int, None])

    # ["reply_schema", "metadata_schema"]
    evt17 = create_event(
        "test", "test", reply_schema=int, metadata_schema=t.Dict[str, str]
    )
    assert_type(evt17, Event[None, None, t.Dict[str, str], int, None])

    # ["schema", "reply_schema", "reply_metadata_schema"]
    evt18 = create_event(
        "service-command",
        subject="test.service",
        schema=str,
        reply_schema=bytes,
        reply_metadata_schema=None,
    )
    assert_type(evt18, Event[None, str, None, bytes, None])

    # ["schema", "reply_schema", "reply_metadata_schema"]
    evt19 = create_event(
        "service-command",
        subject="test.service",
        schema=str,
        reply_schema=bytes,
        reply_metadata_schema=t.Dict[str, str],
    )
    assert_type(evt19, Event[None, str, None, bytes, t.Dict[str, str]])

    # ["schema", "scope_schema," "metadata_schema"]
    evt30 = create_event(
        "test",
        "test",
        schema=int,
        scope_schema=t.Dict[str, str],
        metadata_schema=t.Dict[str, str],
    )
    assert_type(evt30, Event[t.Dict[str, str], int, t.Dict[str, str], None, None])

    # ["reply_schema", "scope_schema", "metadata_schema"]
    evt31 = create_event(
        "test",
        "test",
        reply_schema=int,
        scope_schema=t.Dict[str, str],
        metadata_schema=t.Dict[str, str],
    )
    assert_type(evt31, Event[t.Dict[str, str], None, t.Dict[str, str], int, None])

    # ["schema", "reply_schema", "scope_schema"]
    evt32 = create_event(
        "test",
        "test",
        schema=int,
        reply_schema=int,
        scope_schema=t.Dict[str, str],
    )
    assert_type(evt32, Event[t.Dict[str, str], int, None, int, None])

    # ["schema", "reply_schema", "metadata_schema"]
    evt33 = create_event(
        "test",
        "test",
        schema=int,
        reply_schema=int,
        metadata_schema=t.Dict[str, str],
    )
    assert_type(evt33, Event[None, int, t.Dict[str, str], int, None])

    # ["schema", "reply_schema", "scope_schema", "metadata_schema"]
    evt34 = create_event(
        "test",
        "test",
        schema=int,
        reply_schema=int,
        scope_schema=t.Dict[str, str],
        metadata_schema=t.Dict[str, str],
    )
    assert_type(evt34, Event[t.Dict[str, str], int, t.Dict[str, str], int, None])
